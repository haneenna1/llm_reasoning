"""Sample graded answers for a manual grader audit (Phase 0 step 4 / Phase 1a).

    python scripts/grader_audit.py results/raw --per_grader 100 --out results/analysis/grader_audit_sample.jsonl
    python scripts/grader_audit.py ... --print alias_match      # compact view for reading

Per rule grader, draws `per_grader` rows over its benchmarks, models and conditions,
40% from rows graded correct and 60% from rows graded not correct (that is where
extraction bugs hide), one row per question. The reviewer adds a `verdict` field
(ok / grader_wrong / ambiguous) and a note; summarise with --summary <file>.
"""
import argparse
import json
import random
from collections import Counter, defaultdict
from pathlib import Path

from think_failures.data import benchmark_config, read_questions
from think_failures.generate import read_rows
from think_failures.grading import RULE_GRADERS, grade


def sample(root: Path, per_grader: int, seed: int):
    B = benchmark_config()["benchmarks"]
    by_grader = defaultdict(list)
    for b, c in B.items():
        if c["grader"] in RULE_GRADERS and c.get("screen", True):
            by_grader[c["grader"]].append(b)
    rng = random.Random(seed)
    out = []
    for g, benches in by_grader.items():
        pool = []
        for b in benches:
            recs = {r["qid"]: r for r in read_questions(b, "discovery").to_dict("records")}
            for p in sorted(root.glob(f"*/*/{b}.discovery.jsonl")):
                rows = [r for r in read_rows(p) if r["sample_id"] >= 0]
                for r in rng.sample(rows, min(60, len(rows))):
                    res = grade(B[b], recs[r["qid"]], r["answer"])
                    pool.append((r, recs[r["qid"]], res))
        rng.shuffle(pool)
        want = {True: int(per_grader * 0.4), False: per_grader - int(per_grader * 0.4)}
        seen = set()
        for r, rec, res in pool:
            k = bool(res["correct"])
            if want[k] <= 0 or r["qid"] in seen:
                continue
            want[k] -= 1
            seen.add(r["qid"])
            out.append({"grader": g, "benchmark": r["benchmark"], "model": r["model"], "condition": r["condition"],
                        "qid": r["qid"], "sample_id": r["sample_id"], "question": rec["question"][-300:],
                        "gold": rec["answers"][:5], "meta": {k: v for k, v in rec["meta"].items() if k in
                                                            ("variant", "framing", "parametric_answers")},
                        "answer": r["answer"], "label": res["label"], "extracted": res.get("extracted"),
                        "format": res.get("format")})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default="results/raw")
    ap.add_argument("--per_grader", type=int, default=100)
    ap.add_argument("--seed", type=int, default=20261122)
    ap.add_argument("--out", default="results/analysis/grader_audit_sample.jsonl")
    ap.add_argument("--print", dest="show")
    ap.add_argument("--summary")
    a = ap.parse_args()
    if a.summary:
        rows = [json.loads(l) for l in open(a.summary)]
        c = Counter((r["grader"], r.get("verdict")) for r in rows)
        for g in sorted({r["grader"] for r in rows}):
            n = sum(v for (gg, _), v in c.items() if gg == g)
            print(g, n, {k[1]: v for k, v in c.items() if k[0] == g})
        return
    out = Path(a.out)
    if not out.exists():
        out.parent.mkdir(parents=True, exist_ok=True)
        rows = sample(Path(a.root), a.per_grader, a.seed)
        out.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    rows = [json.loads(l) for l in open(out)]
    if a.show:
        for i, r in enumerate(x for x in rows if x["grader"] == a.show):
            ans = r["answer"].strip().replace("\n", " ⏎ ")
            ans = ans if len(ans) <= 260 else ans[:90] + " … " + ans[-160:]
            print(f"{i:3d} {r['label'][:9]:9s} gold={r['gold'][:3]} ext={str(r['extracted'])[:50]!r} "
                  f"{r['meta'] or ''}\n    A: {ans}")
    else:
        print(Counter(r["grader"] for r in rows))


if __name__ == "__main__":
    main()
