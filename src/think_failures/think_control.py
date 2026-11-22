"""Think control: how each model is put into no-think / think / effort mode, and
how a reasoning trace is closed so the model gives its visible answer.

Conditions (names used in configs and result paths):
    nothink              thinking off (Qwen3: template-prefilled empty <think></think>)
    think                natural thinking, capped at `think_cap` tokens
    think_b<N>           budget N: the natural `think` trace cut at N tokens, then forced closed
    effort_<lvl>         gpt-oss reasoning effort low / medium / high (natural length, capped)
    effort_<lvl>_b<N>    budget N applied to the effort_<lvl> trace

Every think condition is generated in two stages:
  1. the reasoning, from the prompt (with the opening tag prefilled) until the model
     closes it itself or hits the cap;
  2. the answer, from prompt + reasoning + closing sequence. If the cap was hit, an
     explicit "answer now" sentence is inserted before the closing tag ("forced close").
     For Qwen3 this is the sentence Qwen documents for thinking budgets.
Budget conditions reuse stage 1 of their source condition: the model is unaware of
any budget, so cutting the natural trace at N tokens is the same as stopping it there.
This also makes budgets *paired*: every budget sees a prefix of the same trace.
Stage 2 works on token ids (prompt ids + generated ids + closing ids), so the
continuation is exact; nothing is re-tokenised except for budget conditions (where
the stored trace text is re-encoded).
"""
from __future__ import annotations

import re
from dataclasses import dataclass

COND_RE = re.compile(r"^(nothink|think|effort_(low|medium|high))(?:_b(\d+))?$")


@dataclass(frozen=True)
class Condition:
    name: str
    think: bool
    effort: str | None = None
    budget: int | None = None      # derived budget condition (None = natural)

    @property
    def source(self) -> str | None:
        """Condition whose traces a budget condition is derived from."""
        if self.budget is None:
            return None
        return f"effort_{self.effort}" if self.effort else "think"


def parse_condition(name: str) -> Condition:
    m = COND_RE.match(name)
    if not m:
        raise ValueError(f"unknown condition {name!r}")
    base, effort, budget = m.group(1), m.group(2), m.group(3)
    if base == "nothink":
        assert budget is None, name
        return Condition(name, think=False)
    return Condition(name, think=True, effort=effort, budget=int(budget) if budget else None)


class ThinkControl:
    """Interface. All strings are raw text including special-token markup."""
    eos_ids: list[int]

    def render(self, tok, user: str, cond: Condition) -> str:
        """Full prompt text, up to where generation starts. For think conditions this
        includes the opening of the reasoning block."""
        raise NotImplementedError

    def reasoning_stop(self) -> dict:
        """vLLM stop arguments that end stage 1 (the reasoning)."""
        raise NotImplementedError

    def answer_prefix(self, forced: bool) -> str:
        """Text appended after the reasoning to start the visible answer."""
        raise NotImplementedError

    def strip_reasoning_ids(self, ids: list[int]) -> tuple[list[int], bool]:
        """Drop trailing stop tokens from stage-1 output. Returns (ids, closed_by_model)."""
        raise NotImplementedError


class TagsControl(ThinkControl):
    """<think>...</think> models. presets:
       qwen3    Qwen3 / Qwen3.5: template switch `enable_thinking`; </think> is one token.
       prefill  models without a switch (MiMo, OLMo-Think): no-think = prefill an empty block.
    """
    OPEN, CLOSE, SEP = "<think>", "</think>", "\n\n"
    EMPTY = "<think>\n\n</think>\n\n"
    QWEN_FORCED = ("\n\nConsidering the limited time by the user, I have to give the solution "
                   "based on the thinking directly now.\n")

    def __init__(self, tok, preset: str, eos_ids: list[int], system: str | None = None):
        assert preset in ("qwen3", "prefill"), preset
        self.preset, self.system, self.eos_ids = preset, system, list(eos_ids)
        close_ids = tok.encode(self.CLOSE, add_special_tokens=False)
        self.close_id = close_ids[0] if len(close_ids) == 1 else None   # single token for Qwen

    def render(self, tok, user, cond):
        msgs = ([{"role": "system", "content": self.system}] if self.system is not None else []) + \
               [{"role": "user", "content": user}]
        kw = {"enable_thinking": cond.think} if self.preset == "qwen3" else {}
        p = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True, **kw)
        stripped = re.sub(r"<think>\s*$", "", p)
        if cond.think:
            return stripped + self.OPEN + "\n"
        if self.preset == "qwen3":
            assert p.endswith(self.EMPTY), "Qwen3 template no longer prefills the empty think block"
            return p
        return stripped + self.EMPTY

    def reasoning_stop(self):
        if self.close_id is not None:
            return {"stop_token_ids": [self.close_id, *self.eos_ids]}
        return {"stop": [self.CLOSE], "stop_token_ids": self.eos_ids}

    def answer_prefix(self, forced):
        return (self.QWEN_FORCED if forced else "") + self.CLOSE + self.SEP

    def strip_reasoning_ids(self, ids):
        stops = {self.close_id, *self.eos_ids} - {None}
        closed = bool(ids) and ids[-1] in stops
        while ids and ids[-1] in stops:
            ids = ids[:-1]
        return list(ids), closed


class HarmonyControl(ThinkControl):
    """gpt-oss (harmony). Reasoning goes in the `analysis` channel, the answer in `final`.
    Only effort conditions are supported: gpt-oss has no native no-think mode."""
    ANALYSIS = "<|channel|>analysis<|message|>"
    FINAL = "<|end|><|start|>assistant<|channel|>final<|message|>"
    FORCED = "\n\nI am out of time, so I will give the final answer now based on the reasoning so far."

    def __init__(self, tok, eos_ids: list[int], date: str):
        self.eos_ids = list(eos_ids)
        self.end_id = tok.convert_tokens_to_ids("<|end|>")
        tmpl = tok.chat_template
        assert 'strftime_now("%Y-%m-%d")' in tmpl, "gpt-oss template changed"
        self.template = tmpl.replace('strftime_now("%Y-%m-%d")', f'"{date}"')

    def render(self, tok, user, cond):
        if not cond.think or cond.effort is None:
            raise ValueError(f"gpt-oss supports only effort_* conditions, not {cond.name}")
        p = tok.apply_chat_template([{"role": "user", "content": user}], chat_template=self.template,
                                    tokenize=False, add_generation_prompt=True, reasoning_effort=cond.effort)
        assert p.endswith("<|start|>assistant"), p[-50:]
        return p + self.ANALYSIS

    def reasoning_stop(self):
        return {"stop_token_ids": [self.end_id, *self.eos_ids]}

    def answer_prefix(self, forced):
        return (self.FORCED if forced else "") + self.FINAL

    def strip_reasoning_ids(self, ids):
        stops = {self.end_id, *self.eos_ids}
        closed = bool(ids) and ids[-1] in stops
        while ids and ids[-1] in stops:
            ids = ids[:-1]
        return list(ids), closed


def make_control(tok, model_info: dict) -> ThinkControl:
    tc = model_info["think_control"]
    if tc["type"] == "tags":
        return TagsControl(tok, tc["preset"], model_info["stop_token_ids"], system=tc.get("system"))
    if tc["type"] == "harmony":
        return HarmonyControl(tok, model_info["stop_token_ids"], tc["date"])
    raise ValueError(tc)
