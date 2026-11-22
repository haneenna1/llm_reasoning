"""Fixed question sets: discovery / confirmation splits per benchmark, and IO.

Splits are drawn once (scripts/build_questions.py) and saved as
data/questions/<benchmark>/{discovery,confirm}.jsonl. Every later stage
(prompting, generation, grading, mechanistic analysis) reads these files, keyed by qid.
Sampling is by *group* (a question together with its control variants), so all
variants of a question always land in the same split.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[2]
QUESTIONS_DIR = ROOT / "data/questions"
SPLITS = ("discovery", "confirm")


def benchmark_config(path: Path = ROOT / "configs/benchmarks.yaml") -> dict:
    """Benchmark registry with defaults filled in."""
    cfg = yaml.safe_load(open(path))
    cfg["benchmarks"] = {k: {**cfg["defaults"], **v} for k, v in cfg["benchmarks"].items()}
    return cfg


def split_groups(df: pd.DataFrame, n_disc: int, n_conf: int, rng: np.random.Generator,
                 strata: str | None = None) -> dict[str, pd.DataFrame]:
    """Sample disjoint discovery / confirm sets of groups.

    With `strata` (a meta field, constant within a group), both splits get an equal
    number of groups per stratum (n // n_strata, the remainder spread over the first
    strata). If the pool is smaller than n_disc + n_conf, discovery gets its n_disc
    first and confirm gets what is left.
    """
    groups = df.groupby("group", sort=True).first()
    if strata is not None:
        lab = groups.meta.map(lambda m: m[strata])
        chk = df.assign(_s=df.meta.map(lambda m: m[strata])).groupby("group")._s.nunique()
        assert (chk == 1).all(), f"stratum {strata} varies within groups"
    else:
        lab = pd.Series(0, index=groups.index)

    def take(pool: pd.Series, n: int) -> list[str]:
        cats = sorted(pool.unique().tolist(), key=str)
        per = [n // len(cats) + (i < n % len(cats)) for i in range(len(cats))]
        out = []
        for c, k in zip(cats, per):
            ids = pool.index[pool == c].to_numpy()
            ids = ids[rng.permutation(len(ids))]
            out += ids[: min(k, len(ids))].tolist()
        return out

    disc = take(lab, n_disc)
    rest = lab.drop(index=disc)
    conf = take(rest, min(n_conf, len(rest)))
    return {"discovery": df[df.group.isin(disc)].reset_index(drop=True),
            "confirm": df[df.group.isin(conf)].reset_index(drop=True)}


def write_jsonl(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for r in df.to_dict(orient="records"):
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def read_questions(benchmark: str, split: str = "discovery", out_dir: Path = QUESTIONS_DIR) -> pd.DataFrame:
    assert split in SPLITS, split
    return pd.read_json(out_dir / benchmark / f"{split}.jsonl", lines=True, dtype={"qid": str, "group": str})
