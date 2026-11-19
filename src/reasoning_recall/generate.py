"""vLLM generation for (model, condition, dataset), resumable.

Output layout (one directory per model+condition):
    <out_dir>/<model>/<condition>/<dataset>.jsonl          one row per completion
    <out_dir>/<model>/<condition>/<dataset>.prompts.jsonl  one row per question
    <out_dir>/<model>/<condition>/run_meta.json            config, versions, host, GPU

Completion rows are keyed by (model, condition, qid, sample_id); sample_id
0..k-1 are temperature samples and -1 is the greedy completion. A question is
complete when all its sample_ids are present; on restart only incomplete
questions are generated (rows are appended per chunk, duplicates from an
interrupted chunk are resolved by keeping the last row when reading).
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

import yaml

from .data import ROOT, read_questions
from .prompts import build_prompt, prompt_hash, split_reasoning, stop_strings

GREEDY_ID = -1


# ---------------------------------------------------------------- config
def load_run_config(path: str | Path, overrides: dict | None = None) -> dict:
    cfg = yaml.safe_load(open(ROOT / "configs/generation.yaml"))
    cfg.update(yaml.safe_load(open(path)))
    cfg.update({k: v for k, v in (overrides or {}).items() if v is not None})
    models = {k: v for fam in yaml.safe_load(open(ROOT / "configs/models.yaml")).values()
              for k, v in fam.items()}
    m = models[cfg["model"]]
    rev = json.loads((ROOT / "configs/resolved_revisions.json").read_text())[cfg["model"]]
    assert rev["revision"].startswith(m["revision_prefix"]), "revision mismatch"
    cfg["model_info"] = {**m, "revision": rev["revision"]}
    cfg["config_file"] = str(Path(path).resolve().relative_to(ROOT))
    return cfg


def run_dir(cfg: dict) -> Path:
    return ROOT / cfg["out_dir"] / cfg["model"] / cfg["condition"]


# ---------------------------------------------------------------- io helpers
def read_rows(path: Path) -> list[dict]:
    """Read a JSONL file, skipping a truncated last line from a crash."""
    if not path.exists():
        return []
    rows = []
    with open(path) as f:
        for line in f:
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return rows


def completed_qids(path: Path, expected_ids: set[int]) -> set[str]:
    seen: dict[str, set[int]] = {}
    for r in read_rows(path):
        seen.setdefault(r["qid"], set()).add(r["sample_id"])
    return {q for q, ids in seen.items() if expected_ids <= ids}


def request_seed(seed: int, condition: str, qid: str) -> int:
    h = hashlib.sha256(f"{seed}:{condition}:{qid}".encode()).digest()
    return int.from_bytes(h[:4], "little") & 0x7FFFFFFF


def env_info() -> dict:
    import torch
    import transformers
    import vllm
    try:
        commit = subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"],
                                         text=True).strip()
        dirty = bool(subprocess.check_output(["git", "-C", str(ROOT), "status", "--porcelain",
                                              "--untracked-files=no"], text=True).strip())
    except Exception:
        commit, dirty = None, None
    return {
        "host": platform.node(), "slurm_job_id": os.environ.get("SLURM_JOB_ID"),
        "gpus": [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())],
        "torch": torch.__version__, "vllm": vllm.__version__,
        "transformers": transformers.__version__, "python": platform.python_version(),
        "git_commit": commit, "git_dirty": dirty,
    }


# ---------------------------------------------------------------- generation
def load_engine(cfg: dict):
    from transformers import AutoTokenizer
    from vllm import LLM
    m = cfg["model_info"]
    tok = AutoTokenizer.from_pretrained(m["hf_id"], revision=m["revision"],
                                        trust_remote_code=m.get("trust_remote_code", False))
    llm = LLM(model=m["hf_id"], revision=m["revision"], tokenizer_revision=m["revision"],
              trust_remote_code=m.get("trust_remote_code", False), seed=cfg["seed"],
              **cfg["vllm"])
    return llm, tok


def run_one(cfg: dict, llm, tok, dataset: str, limit: int | None = None) -> None:
    from vllm import SamplingParams

    m, cond = cfg["model_info"], cfg["condition"]
    style = m["prompt_style"]
    out = run_dir(cfg)
    out.mkdir(parents=True, exist_ok=True)
    comp_path, prompt_path = out / f"{dataset}.jsonl", out / f"{dataset}.prompts.jsonl"

    qs = read_questions(dataset)
    if limit:
        qs = qs.head(limit)
    fewshot = read_questions(dataset, "fewshot")
    prompts = {r.qid: build_prompt(style, cond, dataset, r.question, fewshot, tok)
               for r in qs.itertuples()}

    # Refuse to mix outputs produced from different prompts.
    old = {r["qid"]: r["prompt_hash"] for r in read_rows(prompt_path)}
    clash = [q for q, p in prompts.items() if q in old and old[q] != prompt_hash(p)]
    if clash:
        raise RuntimeError(f"{prompt_path}: prompt changed for {len(clash)} qids "
                           f"(e.g. {clash[0]}); move old results away first.")
    with open(prompt_path, "a") as f:
        for q, p in prompts.items():
            if q not in old:
                f.write(json.dumps({"qid": q, "prompt_hash": prompt_hash(p), "prompt": p}) + "\n")

    expected = set(range(cfg["k"])) | ({GREEDY_ID} if cfg["greedy"] else set())
    todo = [q for q in prompts if q not in completed_qids(comp_path, expected)]
    print(f"[{cfg['model']}/{cond}/{dataset}] {len(prompts) - len(todo)} done, {len(todo)} to go",
          flush=True)

    common = dict(max_tokens=cfg["max_tokens"][cond], stop=stop_strings(style, cond) or None,
                  stop_token_ids=m["stop_token_ids"])
    for i in range(0, len(todo), cfg["chunk_size"]):
        chunk = todo[i:i + cfg["chunk_size"]]
        reqs, params, keys = [], [], []
        for q in chunk:
            s = request_seed(cfg["seed"], cond, q)
            reqs.append(prompts[q]); keys.append((q, False))
            params.append(SamplingParams(n=cfg["k"], temperature=cfg["temperature"],
                                         top_p=cfg["top_p"], seed=s, **common))
            if cfg["greedy"]:
                reqs.append(prompts[q]); keys.append((q, True))
                params.append(SamplingParams(n=1, temperature=0.0, seed=s, **common))
        t0 = time.time()
        outs = llm.generate(reqs, params, use_tqdm=False)
        dt = time.time() - t0
        ntok = 0
        with open(comp_path, "a") as f:
            for (q, greedy), o in zip(keys, outs):
                for j, c in enumerate(o.outputs):
                    reasoning, answer, ok = split_reasoning(c.text, cond, style)
                    ntok += len(c.token_ids)
                    f.write(json.dumps({
                        "model": cfg["model"], "revision": m["revision"], "condition": cond,
                        "dataset": dataset, "qid": q,
                        "sample_id": GREEDY_ID if greedy else j,
                        "prompt_hash": prompt_hash(prompts[q]),
                        "n_prompt_tokens": len(o.prompt_token_ids),
                        "n_completion_tokens": len(c.token_ids),
                        "finish_reason": c.finish_reason,
                        "stop_reason": c.stop_reason,
                        "truncated": c.finish_reason == "length",
                        # think: True iff </think> was emitted. direct: True iff no
                        # <think>/</think> appears (i.e. no leaked reasoning block).
                        "think_ok": ok,
                        "completion": c.text,
                        "reasoning": reasoning,
                        "final_answer": answer,
                    }, ensure_ascii=False) + "\n")
        print(f"  chunk {i // cfg['chunk_size'] + 1}: {len(chunk)} q, {ntok} tok in {dt:.0f}s "
              f"({ntok / dt:.0f} tok/s)", flush=True)


def run(config_paths: list[str], limit: int | None = None, out_dir: str | None = None,
        datasets: list[str] | None = None) -> None:
    """Run several configs; configs for the same model share one loaded engine."""
    cfgs = [load_run_config(p, {"out_dir": out_dir, "datasets": datasets}) for p in config_paths]
    by_model: dict[str, list[dict]] = {}
    for c in cfgs:
        by_model.setdefault(c["model"], []).append(c)
    for model, group in by_model.items():
        llm, tok = load_engine(group[0])
        env = env_info()
        for cfg in group:
            meta_path = run_dir(cfg) / "run_meta.json"
            meta_path.parent.mkdir(parents=True, exist_ok=True)
            meta = json.loads(meta_path.read_text()) if meta_path.exists() else {"sessions": []}
            meta["config"] = {k: v for k, v in cfg.items()}
            meta["sessions"].append({"started": datetime.now(timezone.utc).isoformat(),
                                     "limit": limit, **env})
            meta_path.write_text(json.dumps(meta, indent=2) + "\n")
            for ds in cfg["datasets"]:
                run_one(cfg, llm, tok, ds, limit)
        del llm
