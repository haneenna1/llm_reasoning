"""Quick look at generation outputs (smoke tests): per model/condition/dataset
stats and a few example completions next to the gold answers.

    python scripts/inspect_outputs.py results/smoke [--examples 3] [--qid triviaqa:tc_2]

The 'rough_acc' column is a crude containment check for eyeballing only; real
grading is src/reasoning_recall/grading.py (step 4).
"""
import argparse
import re
import string
from pathlib import Path

import pandas as pd

from reasoning_recall.data import read_questions
from reasoning_recall.generate import read_rows


def norm(s):
    s = s.lower()
    s = "".join(ch for ch in s if ch not in set(string.punctuation))
    s = re.sub(r"\b(a|an|the)\b", " ", s)
    return " ".join(s.split())


def rough_correct(ans, golds, dataset):
    if dataset == "gsm8k":
        nums = re.findall(r"-?\d[\d,]*\.?\d*", ans)
        return bool(nums) and nums[-1].replace(",", "").rstrip(".") == golds[0]
    a = norm(ans)
    return any(norm(g) and norm(g) in a for g in golds)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--examples", type=int, default=3)
    ap.add_argument("--qid")
    a = ap.parse_args()
    root = Path(a.root)
    gold = {}
    for ds in ["triviaqa", "popqa", "gsm8k"]:
        q = read_questions(ds)
        gold.update(dict(zip(q.qid, zip(q.answers, q.question))))

    rows = [r for p in sorted(root.glob("*/*/*.jsonl")) if not p.name.endswith(".prompts.jsonl")
            for r in read_rows(p)]
    df = pd.DataFrame(rows).drop_duplicates(["model", "condition", "qid", "sample_id"], keep="last")
    df["rough_ok"] = [rough_correct(r.final_answer, gold[r.qid][0], r.dataset) for r in df.itertuples()]
    stats = df.groupby(["model", "condition", "dataset"]).agg(
        n_q=("qid", "nunique"), n=("qid", "size"), trunc=("truncated", "mean"),
        think_ok=("think_ok", "mean"), med_tok=("n_completion_tokens", "median"),
        max_tok=("n_completion_tokens", "max"), rough_acc=("rough_ok", "mean"))
    pd.set_option("display.width", 200)
    print(stats.round(3).to_string(), "\n")

    sel = df[df.qid == a.qid] if a.qid else df[df.sample_id == -1]
    for (m, c, ds), g in sel.groupby(["model", "condition", "dataset"]):
        print(f"=================== {m} / {c} / {ds}")
        for r in g.head(a.examples if not a.qid else 99).itertuples():
            golds, q = gold[r.qid]
            print(f"--- {r.qid} [{r.sample_id}] Q: {q[:150]}\n    gold: {golds[:4]}  "
                  f"| tokens={r.n_completion_tokens} finish={r.finish_reason} think_ok={r.think_ok}")
            if isinstance(r.reasoning, str) and r.reasoning:
                rs = r.reasoning
                print(f"    reasoning ({len(rs)} chars): {rs[:300]!r} ... {rs[-200:]!r}")
            print(f"    final: {r.final_answer[:300]!r}   rough_ok={r.rough_ok}")


if __name__ == "__main__":
    main()
