"""Grade every generation row and save one table for the analysis.

    python scripts/grade_outputs.py results/raw --split discovery
        -> results/analysis/<split>_graded.parquet

Rule graders run here; judge benchmarks take their outcome from results/judged/
(scripts/run_judges.py) when present, else `correct` is NaN. Text columns are dropped
(the raw JSONL stays the source of truth); answer/trace lengths and flags are kept.
Run on the dev node, detached:  setsid nohup python scripts/grade_outputs.py ... &
"""
import argparse
import json
from pathlib import Path

import pandas as pd

from think_failures.data import benchmark_config, read_questions
from think_failures.generate import read_rows
from think_failures.grading import RULE_GRADERS, grade

KEEP = ["model", "condition", "benchmark", "split", "qid", "sample_id", "n_prompt_tokens", "n_reasoning_tokens",
        "reasoning_closed", "forced_close", "n_answer_tokens", "answer_finish_reason", "answer_truncated",
        "derived_from", "copied"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default="results/raw")
    ap.add_argument("--split", default="discovery")
    ap.add_argument("--judged", default=None, help="default: <root>/../judged")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    root = Path(a.root)
    judged = Path(a.judged) if a.judged else root.parent / "judged"
    out = Path(a.out or f"results/analysis/{a.split}_graded.parquet")
    B = benchmark_config()["benchmarks"]
    frames = []
    for b, cfg in B.items():
        files = [p for p in sorted(root.glob(f"*/*/{b}.{a.split}.jsonl"))]
        if not files:
            continue
        q = read_questions(b, a.split)
        recs = {r["qid"]: r for r in q.to_dict("records")}
        rows = []
        for p in files:
            jd = {}
            jp = judged / p.relative_to(root)
            if cfg["grader"] not in RULE_GRADERS and jp.exists():
                jd = {(j["qid"], j["sample_id"]): j for j in read_rows(jp)}
            for r in {(r["qid"], r["sample_id"]): r for r in read_rows(p)}.values():
                row = {k: r.get(k) for k in KEEP}
                g = grade(cfg, recs[r["qid"]], r["answer"])
                row.update(label=g["label"], extracted=(g.get("extracted") or "")[:200], fmt=g.get("format"),
                           correct=g["correct"])
                if cfg["grader"] == "ifeval":
                    row["loose_correct"] = g["loose_prompt"]
                j = jd.get((r["qid"], r["sample_id"]))
                if j is not None:
                    row["correct"] = j["correct"]
                    row["label"] = {True: "correct", False: "incorrect", None: "judge_unparsed"}[j["correct"]]
                    for k in ("abstained", "answer_correct", "xstest_class", "sr_score"):
                        if k in j:
                            row[k] = j[k]
                rows.append(row)
        df = pd.DataFrame(rows)
        meta = q[["qid", "group", "meta"]].copy()
        meta["variant"] = meta.meta.map(lambda m: m.get("variant") or m.get("framing") or
                                        ("abstain" if m.get("should_abstain") else
                                         "refuse" if m.get("should_refuse") else None))
        meta["stratum"] = meta.meta.map(lambda m: json.dumps({k: v for k, v in m.items() if k in (
            "should_abstain", "should_refuse", "pop_bin", "num_distractors", "xstest_type", "sr_category")}))
        df = df.merge(meta.drop(columns="meta"), on="qid", how="left")
        df["category"] = cfg["category"]
        frames.append(df)
        print(f"{b}: {len(df)} rows, graded {df.correct.notna().mean():.3f}", flush=True)
    all_ = pd.concat(frames, ignore_index=True)
    all_["correct"] = all_["correct"].astype("float")
    out.parent.mkdir(parents=True, exist_ok=True)
    all_.to_parquet(out)
    print(f"wrote {out}: {len(all_)} rows", flush=True)


if __name__ == "__main__":
    main()
