"""Prompt construction. Identical question text for every model and condition.

Prompt styles (chosen per model in configs/models.yaml, `prompt_style`):

  base    (pretrained model, raw text, no chat template)
    direct : INSTRUCTION + 5 few-shot QA pairs + "Question: q\nAnswer:"
    think  : zero-shot R1-Zero-style CoT (reference only; not used for
             transition labels): asks for reasoning inside <think></think>
             and then the final answer.

  chatml  (post-trained models with a ChatML chat template)
    user message = the same text block as base/direct (instruction + 5 few-shot
    pairs + question), empty system prompt (MiMo README recommendation).
    think  : chat template + generation prompt; the model opens <think> itself.
    direct : same + prefill "<think>\n\n</think>\n\n" so the model sees an
             empty, closed reasoning block and answers directly.

The only difference between direct and think for a chat model is the prefill.
"""
from __future__ import annotations

import hashlib

import pandas as pd

THINK_OPEN, THINK_CLOSE = "<think>", "</think>"
EMPTY_THINK_PREFILL = "<think>\n\n</think>\n\n"

INSTRUCTIONS = {
    "triviaqa": "Answer the following question. Give only the short final answer "
                "(a name, word, number or short phrase), with no explanation.",
    "popqa": "Answer the following question. Give only the short final answer "
             "(a name, word, number or short phrase), with no explanation.",
    "gsm8k": "Solve the following math problem. Give only the final numerical "
             "answer, with no explanation.",
}

# Base-model "thinking" condition (zero-shot CoT, R1-Zero style).
BASE_COT_TEMPLATE = (
    "A conversation between User and Assistant. The User asks a question, and the "
    "Assistant answers it. The Assistant first thinks about the reasoning process "
    "step by step and then gives the final answer. The reasoning process is enclosed "
    "within <think> </think> tags, followed by the short final answer.\n"
    "User: {instruction}\nQuestion: {question}\nAssistant: <think>"
)


def fewshot_answer(dataset: str, answers: list[str]) -> str:
    """Display form of a few-shot gold answer (first alias, cleaned)."""
    a = answers[0].strip().strip("'\"")
    if dataset == "triviaqa" and a.isupper():
        a = a.title()
    return a


def qa_block(dataset: str, question: str, fewshot: pd.DataFrame) -> str:
    """Instruction + few-shot pairs + target question. Identical for all models."""
    parts = [INSTRUCTIONS[dataset], ""]
    for r in fewshot.itertuples():
        parts += [f"Question: {r.question}", f"Answer: {fewshot_answer(dataset, r.answers)}", ""]
    parts += [f"Question: {question}", "Answer:"]
    return "\n".join(parts)


def build_prompt(style: str, condition: str, dataset: str, question: str,
                 fewshot: pd.DataFrame, tokenizer=None) -> str:
    if style == "base":
        if condition == "direct":
            return qa_block(dataset, question, fewshot)
        if condition == "think":
            return BASE_COT_TEMPLATE.format(instruction=INSTRUCTIONS[dataset], question=question)
    elif style == "chatml":
        msgs = [{"role": "system", "content": ""},
                {"role": "user", "content": qa_block(dataset, question, fewshot)}]
        p = tokenizer.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
        if condition == "think":
            return p
        if condition == "direct":
            return p + EMPTY_THINK_PREFILL
    raise ValueError(f"unknown style/condition {style}/{condition}")


def stop_strings(style: str, condition: str) -> list[str]:
    """Extra stop strings on top of the model's EOS tokens."""
    if style == "base" and condition == "direct":
        return ["\n"]                     # one-line answer, then the next "Question:"
    if style == "base" and condition == "think":
        return ["\nUser:", "\n\nUser"]    # don't let it continue the dialogue
    return []


def prompt_hash(prompt: str) -> str:
    return hashlib.sha256(prompt.encode()).hexdigest()[:16]


def split_reasoning(text: str, condition: str, style: str) -> tuple[str | None, str, bool]:
    """Split a completion into (reasoning, final_answer, closed).

    For think mode the completion starts inside an open <think> (base: opened in
    the prompt; chatml: the model emits "<think>" itself). closed=False means
    the reasoning never ended (usually truncation) and final_answer is "".
    For direct mode there is no reasoning; closed reports whether a stray
    </think> appeared (i.e. the model reasoned anyway).
    """
    if condition == "direct":
        stray = THINK_CLOSE in text or THINK_OPEN in text
        return None, text.strip(), not stray
    if THINK_CLOSE not in text:
        return text, "", False
    reasoning, _, answer = text.partition(THINK_CLOSE)
    reasoning = reasoning.split(THINK_OPEN, 1)[-1]
    return reasoning.strip(), answer.strip(), True
