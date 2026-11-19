"""Load the raw datasets from the pinned HF cache snapshots and sample fixed
question sets.

Every question becomes one record with the same schema across datasets:
    qid       str   globally unique, "<dataset>:<source id>"
    dataset   str   triviaqa | popqa | gsm8k
    question  str
    answers   list[str]  all gold answers/aliases (for gsm8k: [number])
    meta      dict  dataset-specific extras (popularity, relation, ...)

These records (keyed by qid) are the single source of truth for every later
stage: prompting, generation, grading and the mechanistic phase.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
from huggingface_hub.constants import HF_HUB_CACHE

ROOT = Path(__file__).resolve().parents[2]
REVISIONS = ROOT / "configs/resolved_revisions.json"

HF_REPOS = {
    "triviaqa": "mandarjoshi/trivia_qa",
    "popqa": "akariasai/PopQA",
    "gsm8k": "openai/gsm8k",
}


def _snapshot(dataset: str) -> Path:
    repo = HF_REPOS[dataset]
    rev = json.loads(REVISIONS.read_text())[f"dataset:{repo}"]["revision"]
    # Only a subset of each repo is downloaded (scripts/download_assets.py), so
    # snapshot_download(local_files_only=True) rejects it as incomplete; use the
    # pinned snapshot dir directly.
    p = Path(HF_HUB_CACHE) / f"datasets--{repo.replace('/', '--')}" / "snapshots" / rev
    if not p.is_dir():
        raise FileNotFoundError(f"{p} missing; run scripts/download_assets.py --datasets")
    return p


def load_triviaqa() -> pd.DataFrame:
    """Closed-book TriviaQA validation, one row per unique question_id."""
    f = next((_snapshot("triviaqa") / "rc.nocontext").glob("validation-*.parquet"))
    df = pd.read_parquet(f, columns=["question_id", "question", "answer"])
    # rc lists each question once per evidence source -> dedupe by id.
    df = df.drop_duplicates("question_id", keep="first").reset_index(drop=True)

    def answers(a):
        out = [a["value"], *a["aliases"]]
        return list(dict.fromkeys(x for x in out if x))  # dedupe, keep order

    return pd.DataFrame({
        "qid": "triviaqa:" + df.question_id,
        "dataset": "triviaqa",
        "question": df.question.str.strip(),
        "answers": df.answer.map(answers),
        "meta": df.answer.map(lambda a: {"answer_type": a["type"]}),
    })


def load_popqa(drop_ambiguous: bool = True) -> pd.DataFrame:
    df = pd.read_csv(_snapshot("popqa") / "test.tsv", sep="\t")
    if drop_ambiguous:
        df = df[~df.question.duplicated(keep=False)]
    return pd.DataFrame({
        "qid": "popqa:" + df.id.astype(str),
        "dataset": "popqa",
        "question": df.question.str.strip(),
        "answers": df.possible_answers.map(json.loads),
        "meta": [{"s_pop": int(r.s_pop), "o_pop": int(r.o_pop), "prop": r.prop,
                  "subj": r.subj, "obj": r.obj}
                 for r in df.itertuples()],
    }).reset_index(drop=True)


_GSM_ANS = re.compile(r"####\s*(.+?)\s*$")


def load_gsm8k() -> pd.DataFrame:
    f = next((_snapshot("gsm8k") / "main").glob("test-*.parquet"))
    df = pd.read_parquet(f)

    def final(sol):
        return _GSM_ANS.search(sol).group(1).replace(",", "").replace("$", "").strip()

    return pd.DataFrame({
        "qid": [f"gsm8k:{i:04d}" for i in range(len(df))],  # row index in test split
        "dataset": "gsm8k",
        "question": df.question.str.strip(),
        "answers": df.answer.map(lambda s: [final(s)]),
        "meta": df.answer.map(lambda s: {"solution": s}),
    })


LOADERS = {"triviaqa": load_triviaqa, "popqa": load_popqa, "gsm8k": load_gsm8k}


def popularity_bins(s_pop: pd.Series, n_bins: int) -> tuple[pd.Series, list[float]]:
    """Equal-count quantile bins of s_pop. Returns (bin index 0..n-1, edges)."""
    bins, edges = pd.qcut(s_pop, q=n_bins, labels=False, retbins=True, duplicates="raise")
    return bins.astype(int), [float(e) for e in edges]


def sample(df: pd.DataFrame, n: int, n_fewshot: int, rng: np.random.Generator,
           strata: pd.Series | None = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Draw n_fewshot few-shot examples, then n eval questions from the rest.

    With strata, the eval set has n / n_strata questions per stratum and the
    few-shot examples are drawn from the full pool (not stratified).
    """
    perm = rng.permutation(len(df))
    fewshot_idx = perm[:n_fewshot]
    pool = df.drop(index=df.index[fewshot_idx])
    if strata is None:
        eval_idx = rng.choice(len(pool), size=n, replace=False)
        ev = pool.iloc[np.sort(eval_idx)]
    else:
        s = strata.loc[pool.index]
        k = s.nunique()
        assert n % k == 0, f"n={n} not divisible by {k} strata"
        parts = [pool[s == b].sample(n=n // k, random_state=rng) for b in sorted(s.unique())]
        ev = pd.concat(parts).sort_index()
    return ev.reset_index(drop=True), df.iloc[fewshot_idx].reset_index(drop=True)


def write_jsonl(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for r in df.to_dict(orient="records"):
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def read_questions(dataset: str, split: str = "eval",
                   out_dir: Path = ROOT / "data/questions") -> pd.DataFrame:
    """Load a saved question set. split: 'eval' or 'fewshot'."""
    name = dataset if split == "eval" else f"{dataset}_fewshot"
    return pd.read_json(out_dir / f"{name}.jsonl", lines=True, dtype={"qid": str})
