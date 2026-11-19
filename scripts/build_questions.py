"""Step 2: sample the fixed question sets from configs/data.yaml.

    python scripts/build_questions.py [--config configs/data.yaml] [--force]

Writes data/questions/{dataset}.jsonl, {dataset}_fewshot.jsonl and
manifest.json (seed, source revisions, pool sizes, bin edges, sha256 of each
file). Refuses to overwrite existing question files unless --force is given,
because every later result is keyed to these question IDs.
"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import yaml

from reasoning_recall.data import (HF_REPOS, LOADERS, REVISIONS, ROOT,
                                   popularity_bins, sample, write_jsonl)


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=str(ROOT / "configs/data.yaml"))
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    cfg = yaml.safe_load(open(a.config))
    out = ROOT / cfg["out_dir"]
    if (out / "manifest.json").exists() and not a.force:
        raise SystemExit(f"{out} already built; pass --force to resample (invalidates results).")

    revs = json.loads(REVISIONS.read_text())
    manifest = {"seed": cfg["seed"], "n_fewshot": cfg["n_fewshot"], "datasets": {}}
    for i, (name, dcfg) in enumerate(cfg["datasets"].items()):
        # Independent stream per dataset so changing one doesn't reshuffle others.
        rng = np.random.default_rng([cfg["seed"], i])
        df = LOADERS[name](**({"drop_ambiguous": dcfg["drop_ambiguous"]} if name == "popqa" else {}))
        assert df.qid.is_unique, f"{name}: duplicate qids"
        info = {"source": HF_REPOS[name], "revision": revs[f"dataset:{HF_REPOS[name]}"]["revision"],
                "pool_size": len(df)}
        strata = None
        if name == "popqa":
            strata, edges = popularity_bins(df.meta.map(lambda m: m["s_pop"]), dcfg["n_bins"])
            df["meta"] = [{**m, "pop_bin": int(b)} for m, b in zip(df.meta, strata)]
            info["s_pop_bin_edges"] = edges
        ev, fs = sample(df, dcfg["n"], cfg["n_fewshot"], rng, strata)
        assert not set(ev.qid) & set(fs.qid)
        for split, part in [("", ev), ("_fewshot", fs)]:
            p = out / f"{name}{split}.jsonl"
            write_jsonl(part, p)
            info[f"file{split}"] = {"path": str(p.relative_to(ROOT)), "n": len(part), "sha256": sha256(p)}
        if name == "popqa":
            info["eval_per_bin"] = {int(k): int(v) for k, v in
                                    ev.meta.map(lambda m: m["pop_bin"]).value_counts().sort_index().items()}
        manifest["datasets"][name] = info
        print(f"{name}: pool {len(df)} -> eval {len(ev)}, fewshot {len(fs)}")
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
