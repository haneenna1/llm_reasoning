"""Graders. grade(benchmark_cfg, record, answer) -> dict with at least
    correct      bool | None   None = needs the LLM judge (judge_* graders) or ungradable
    label        str           grader-specific outcome, e.g. correct / incorrect /
                               not_attempted / no_answer / parametric / ...
    extracted    str | None    the part of the answer that was compared
Only the visible answer is graded (the text after the reasoning), never the trace.
"""
from __future__ import annotations

from .rules import (alias_match, answer_tag, context_faithful, ifeval, math_verify_grade, numeric)

RULE_GRADERS = {
    "alias_match": alias_match,
    "numeric": numeric,
    "math_verify": math_verify_grade,
    "answer_tag": answer_tag,
    "ifeval": ifeval,
    "context_faithful": context_faithful,
}
JUDGE_GRADERS = {"judge_abstention", "judge_refusal", "judge_strongreject", "judge_simpleqa"}


def grade(bcfg: dict, record: dict, answer: str) -> dict:
    g = bcfg["grader"]
    if g in RULE_GRADERS:
        return RULE_GRADERS[g](record, answer)
    if g in JUDGE_GRADERS:
        out = {"correct": None, "label": "needs_judge", "extracted": None}
        # cheap rule-based signals that the judge pass will later complement
        if g == "judge_abstention":
            from .rules import abstained, numeric as _num
            out["rule_abstained"] = abstained(answer)
            if record["answers"] and record["meta"].get("variant") == "answerable":
                out["rule_numeric"] = _num(record, answer)["correct"]
        if g in ("judge_refusal", "judge_strongreject"):
            from .rules import refused
            out["rule_refused"] = refused(answer)
        return out
    raise ValueError(f"unknown grader {g}")
