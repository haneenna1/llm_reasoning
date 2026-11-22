"""Sample the fixed discovery / confirmation splits for every benchmark in
configs/benchmarks.yaml.

    python scripts/build_questions.py [--only triviaqa popqa] [--force]

Writes data/questions/<benchmark>/{discovery,confirm}.jsonl and
data/questions/manifest.json (seed, source revisions, pool sizes, split sizes,
per-stratum counts, sha256 of each file). Refuses to overwrite an existing
benchmark unless --force is given, because every later result is keyed to these qids.
"""
import argparse
import hashlib
import json

import numpy as np

from think_failures.benchmarks import REVISIONS, load
from think_failures.data import QUESTIONS_DIR, ROOT, SPLITS, benchmark_config, split_groups, write_jsonl


def sha256(p) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def source_revision(src: dict, revs: dict) -> str:
    key = f"dataset:{src['repo']}" if src["type"] == "hf" else f"github:{src['repo']}/{src['path']}"
    return revs[key]["revision"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="+", help="benchmarks to (re)build")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    cfg = benchmark_config()
    revs = json.loads(REVISIONS.read_text())
    man_path = QUESTIONS_DIR / "manifest.json"
    manifest = json.loads(man_path.read_text()) if man_path.exists() else {"seed": cfg["seed"], "benchmarks": {}}
    assert manifest["seed"] == cfg["seed"], "seed changed; rebuild everything with --force"

    for name, b in cfg["benchmarks"].items():
        if a.only and name not in a.only:
            continue
        if (QUESTIONS_DIR / name).exists() and not a.force:
            print(f"{name}: exists, skipping (use --force to resample; invalidates results)")
            continue
        # Independent stream per benchmark, keyed by name, so adding/removing one
        # benchmark never reshuffles another.
        rng = np.random.default_rng([cfg["seed"], int(hashlib.sha256(name.encode()).hexdigest()[:8], 16)])
        df = load(name, b)
        splits = split_groups(df, b["n_discovery"], b["n_confirm"], rng, b.get("strata"))
        assert not set(splits["discovery"].group) & set(splits["confirm"].group)
        info = {"category": b["category"], "source": b["source"], "revision": source_revision(b["source"], revs),
                "pool_items": len(df), "pool_groups": int(df.group.nunique())}
        for s in SPLITS:
            p = QUESTIONS_DIR / name / f"{s}.jsonl"
            write_jsonl(splits[s], p)
            part = splits[s]
            info[s] = {"path": str(p.relative_to(ROOT)), "items": len(part), "groups": int(part.group.nunique()),
                       "sha256": sha256(p)}
            if b.get("strata"):
                info[s]["per_stratum"] = {str(k): int(v) for k, v in
                                          part.meta.map(lambda m: m[b["strata"]]).value_counts().sort_index().items()}
            if "variant" in (part.meta.iloc[0] if len(part) else {}):
                info[s]["per_variant"] = {str(k): int(v) for k, v in
                                          part.meta.map(lambda m: m["variant"]).value_counts().sort_index().items()}
        manifest["benchmarks"][name] = info
        print(f"{name:22s} pool {len(df):6d} items / {info['pool_groups']:6d} groups -> "
              f"discovery {info['discovery']['items']:5d} ({info['discovery']['groups']} g), "
              f"confirm {info['confirm']['items']:5d} ({info['confirm']['groups']} g)", flush=True)
        man_path.write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
