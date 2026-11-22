"""Quick look at generation outputs: per model / condition / benchmark stats
(rule-based grading) and a few examples next to the gold answers.

    python scripts/inspect_outputs.py results/smoke [--examples 2] [--benchmarks triviaqa ifeval]
        [--qid triviaqa:tc_2] [--leak]

Columns: n_q questions, n samples, acc (rule-graded, judge benchmarks excluded),
closed (reasoning ended by the model), forced (cut at the cap/budget), r_tok / a_tok
median reasoning / answer tokens, a_trunc answer hit its cap, leak (no-think answers
containing reasoning markers).
"""
import argparse
import re
from pathlib import Path

import pandas as pd

from think_failures.data import benchmark_config, read_questions
from think_failures.generate import read_rows
from think_failures.grading import grade

LEAK = re.compile(r"<think>|</think>|\b(wait|hmm|let me (think|check|verify|recall)|okay, so|alternatively)\b", re.I)


def load(root: Path, benches=None) -> pd.DataFrame:
    rows = []
    for p in sorted(root.glob("*/*/*.jsonl")):
        if p.name.endswith(".prompts.jsonl"):
            continue
        if benches and p.name.split(".")[0] not in benches:
            continue
        rows += read_rows(p)
    df = pd.DataFrame([r for r in rows if "benchmark" in r])   # skip old-format (pre-rescope) outputs
    return df.drop_duplicates(["model", "condition", "qid", "sample_id"], keep="last")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--examples", type=int, default=2)
    ap.add_argument("--benchmarks", nargs="+")
    ap.add_argument("--qid")
    ap.add_argument("--leak", action="store_true", help="print no-think answers with reasoning markers")
    a = ap.parse_args()
    B = benchmark_config()["benchmarks"]
    df = load(Path(a.root), a.benchmarks)
    recs = {}
    for b, s in df[["benchmark", "split"]].drop_duplicates().itertuples(index=False):
        recs.update({r["qid"]: r for r in read_questions(b, s).to_dict("records")})
    g = [grade(B[r.benchmark], recs[r.qid], r.answer) for r in df.itertuples()]
    df["correct"] = [x["correct"] for x in g]
    df["label"] = [x["label"] for x in g]
    df["leak"] = [(r.reasoning is None) and bool(LEAK.search(r.answer or "")) for r in df.itertuples()]
    stats = df.groupby(["benchmark", "model", "condition"]).agg(
        n_q=("qid", "nunique"), n=("qid", "size"),
        acc=("correct", lambda s: s.dropna().astype(float).mean() if s.notna().any() else float("nan")),
        closed=("reasoning_closed", lambda s: s.dropna().astype(float).mean()),
        forced=("forced_close", lambda s: s.dropna().astype(float).mean()),
        r_tok=("n_reasoning_tokens", "median"), a_tok=("n_answer_tokens", "median"),
        a_trunc=("answer_truncated", "mean"), leak=("leak", "mean"))
    pd.set_option("display.width", 220, "display.max_rows", 500)
    print(stats.round(3).to_string(), "\n")

    if a.leak:
        for r in df[df.leak].head(20).itertuples():
            print(f"--- LEAK {r.model}/{r.qid}#{r.sample_id}: {r.answer[:400]!r}")
    sel = df[df.qid == a.qid] if a.qid else df[df.sample_id.isin([0, -1]) & ~df.copied.fillna(False)]
    for (b, m, c), grp in sel.groupby(["benchmark", "model", "condition"]):
        print(f"=================== {b} / {m} / {c}")
        for r in grp.drop_duplicates("qid").head(a.examples if not a.qid else 99).itertuples():
            rec = recs[r.qid]
            print(f"--- {r.qid} [{r.sample_id}] Q: {rec['question'][:200]!r}\n    gold: {rec['answers'][:3]} | "
                  f"r_tok={r.n_reasoning_tokens} closed={r.reasoning_closed} forced={r.forced_close} "
                  f"a_tok={r.n_answer_tokens} -> {r.label}")
            if isinstance(r.reasoning, str) and r.reasoning:
                print(f"    reasoning: {r.reasoning[:250]!r} ... {r.reasoning[-150:]!r}")
            print(f"    answer: {r.answer[:300]!r}")


if __name__ == "__main__":
    main()
