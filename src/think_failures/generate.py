"""vLLM generation for (model, condition, benchmark, split), resumable.

Output layout:
    <out_dir>/<model>/<condition>/<benchmark>.<split>.jsonl          one row per sample
    <out_dir>/<model>/<condition>/<benchmark>.<split>.prompts.jsonl  one row per question
    <out_dir>/<model>/<condition>/run_meta.json                      config, versions, host, GPU

Rows are keyed by (model, condition, qid, sample_id); sample_id 0..K-1 are
temperature samples, -1 is the greedy sample. A question is done when all its
sample_ids are present. On restart only unfinished questions are generated
(rows are appended per chunk; when reading, the last row per key wins).
See think_control.py for how think / budget conditions are generated.
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

from .data import ROOT, benchmark_config, read_questions
from .prompts import prompt_hash, user_message
from .think_control import Condition, make_control, parse_condition

GREEDY_ID = -1


# ---------------------------------------------------------------- config
def deep_merge(base: dict, upd: dict) -> dict:
    """Merge `upd` into a copy of `base`; nested dicts merge per key, other values are replaced."""
    out = dict(base)
    for k, v in upd.items():
        out[k] = deep_merge(out[k], v) if isinstance(v, dict) and isinstance(out.get(k), dict) else v
    return out


def model_registry() -> dict:
    return {k: v for grp in yaml.safe_load(open(ROOT / "configs/models.yaml")).values() for k, v in grp.items()}


def load_experiment(path: str | Path, overrides: dict | None = None) -> dict:
    """configs/generation.yaml <- experiment `generation:` block <- CLI overrides."""
    exp = yaml.safe_load(open(path))
    gen = yaml.safe_load(open(ROOT / "configs/generation.yaml"))
    gen = deep_merge(gen, exp.get("generation") or {})
    gen = deep_merge(gen, {k: v for k, v in (overrides or {}).items() if v is not None})
    exp["generation"] = gen
    exp["config_file"] = str(Path(path).resolve().relative_to(ROOT))
    bench = benchmark_config()["benchmarks"]
    if exp.get("benchmarks", "all") == "all":
        exp["benchmarks"] = [b for b, c in bench.items() if c.get("screen", True)]
    unknown = set(exp["benchmarks"]) - set(bench)
    assert not unknown, f"unknown benchmarks {unknown}"
    return exp


def model_info(key: str) -> dict:
    m = model_registry()[key]
    rev = json.loads((ROOT / "configs/resolved_revisions.json").read_text())[key]
    assert rev["revision"].startswith(m["revision_prefix"]), f"{key}: revision mismatch"
    return {**m, "key": key, "revision": rev["revision"]}


def conditions_for(exp: dict, model: str) -> list[Condition]:
    """Conditions of every run block that lists `model`, sources before derived budgets."""
    names = []
    for block in exp["runs"]:
        if model in block["models"]:
            names += [c for c in block["conditions"] if c not in names]
    conds = [parse_condition(n) for n in names]
    for c in conds:
        if c.budget is not None:
            assert c.source in names, f"{c.name} needs {c.source} in the same experiment"
    return sorted(conds, key=lambda c: c.budget is not None)


def cell_dir(out_dir: str, model: str, cond: str) -> Path:
    return ROOT / out_dir / model / cond


# ---------------------------------------------------------------- io helpers
def read_rows(path: Path) -> list[dict]:
    """Read JSONL, skipping a truncated last line from a crash."""
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


def latest_rows(path: Path) -> dict[tuple[str, int], dict]:
    return {(r["qid"], r["sample_id"]): r for r in read_rows(path)}


def request_seed(*parts) -> int:
    h = hashlib.sha256(":".join(map(str, parts)).encode()).digest()
    return int.from_bytes(h[:4], "little") & 0x7FFFFFFF


def env_info() -> dict:
    import torch
    import transformers
    import vllm
    try:
        commit = subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip()
        dirty = bool(subprocess.check_output(["git", "-C", str(ROOT), "status", "--porcelain",
                                              "--untracked-files=no"], text=True).strip())
    except Exception:
        commit, dirty = None, None
    return {"host": platform.node(), "slurm_job_id": os.environ.get("SLURM_JOB_ID"),
            "gpus": [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())],
            "torch": torch.__version__, "vllm": vllm.__version__, "transformers": transformers.__version__,
            "python": platform.python_version(), "git_commit": commit, "git_dirty": dirty}


# ---------------------------------------------------------------- generation
def load_engine(m: dict, gen: dict):
    from transformers import AutoTokenizer
    from vllm import LLM
    tok = AutoTokenizer.from_pretrained(m["hf_id"], revision=m["revision"],
                                        trust_remote_code=m.get("trust_remote_code", False))
    llm = LLM(model=m["hf_id"], revision=m["revision"], tokenizer_revision=m["revision"],
              trust_remote_code=m.get("trust_remote_code", False), seed=gen["seed"], **gen["vllm"])
    return llm, tok


class Cell:
    """One (model, condition, benchmark, split) output file pair."""

    def __init__(self, exp, m, cond: Condition, benchmark: str, split: str):
        self.exp, self.m, self.cond, self.benchmark, self.split = exp, m, cond, benchmark, split
        self.gen = exp["generation"]
        d = cell_dir(exp["out_dir"], m["key"], cond.name)
        d.mkdir(parents=True, exist_ok=True)
        self.path = d / f"{benchmark}.{split}.jsonl"
        self.prompt_path = d / f"{benchmark}.{split}.prompts.jsonl"
        self.k = self.gen["k"] if cond.think else self.gen["k_nothink"]
        self.greedy = cond.name in self.gen["greedy_conditions"] or \
            (cond.source is not None and cond.source in self.gen["greedy_conditions"])
        self.sample_ids = list(range(self.k)) + ([GREEDY_ID] if self.greedy else [])

    def todo(self, qids: list[str]) -> list[str]:
        seen: dict[str, set[int]] = {}
        for r in read_rows(self.path):
            seen.setdefault(r["qid"], set()).add(r["sample_id"])
        need = set(self.sample_ids)
        return [q for q in qids if not need <= seen.get(q, set())]

    def register_prompts(self, prompts: dict[str, str]) -> None:
        """Refuse to mix outputs produced from different prompts."""
        old = {r["qid"]: r["prompt_hash"] for r in read_rows(self.prompt_path)}
        clash = [q for q, p in prompts.items() if q in old and old[q] != prompt_hash(p)]
        if clash:
            raise RuntimeError(f"{self.prompt_path}: prompt changed for {len(clash)} qids "
                               f"(e.g. {clash[0]}); move old results away first.")
        with open(self.prompt_path, "a") as f:
            for q, p in prompts.items():
                if q not in old:
                    f.write(json.dumps({"qid": q, "prompt_hash": prompt_hash(p), "prompt": p},
                                       ensure_ascii=False) + "\n")


def run_cell(cell: Cell, llm, tok, ctrl, limit: int | None = None) -> None:
    from vllm import SamplingParams

    gen, cond, m = cell.gen, cell.cond, cell.m
    bcfg = dict(benchmark_config()["benchmarks"][cell.benchmark])
    # experiment-level overrides of benchmark settings, e.g. {"prompt": ..., "answer_max_tokens": ...}
    bcfg.update(cell.exp.get("benchmark_overrides", {}).get(cell.benchmark, {}))
    qs = read_questions(cell.benchmark, cell.split)
    if limit:
        qs = qs.head(limit)
    prompts = {r["qid"]: ctrl.render(tok, user_message(bcfg["prompt"], r), cond) for r in qs.to_dict("records")}
    cell.register_prompts(prompts)
    todo = cell.todo(list(prompts))
    tag = f"[{m['key']}/{cond.name}/{cell.benchmark}.{cell.split}]"
    print(f"{tag} {len(prompts) - len(todo)} done, {len(todo)} to go", flush=True)
    if not todo:
        return

    ans_max = bcfg["answer_max_tokens"]
    eos = list(m["stop_token_ids"])
    samp = dict(temperature=gen["temperature"], top_p=gen["top_p"], top_k=gen["top_k"])
    enc = lambda s: tok.encode(s, add_special_tokens=False)   # noqa: E731
    source_rows = None
    if cond.budget is not None:
        src = Cell(cell.exp, m, parse_condition(cond.source), cell.benchmark, cell.split)
        source_rows = latest_rows(src.path)

    for i in range(0, len(todo), gen["chunk_size"]):
        chunk = todo[i:i + gen["chunk_size"]]
        t0, ntok = time.time(), 0
        pids = {q: enc(prompts[q]) for q in chunk}
        # ---- stage 1: reasoning (think conditions) or the whole answer (nothink)
        # samples: list of dict(qid, sample_id, reasoning_ids, closed, forced, row extras)
        samples: list[dict] = []
        if not cond.think:
            reqs, params, keys = [], [], []
            for q in chunk:
                s = request_seed(gen["seed"], cond.name, q)
                reqs.append({"prompt_token_ids": pids[q]}); keys.append((q, False))
                params.append(SamplingParams(n=cell.k, seed=s, max_tokens=ans_max, stop_token_ids=eos, **samp))
                if cell.greedy:
                    reqs.append({"prompt_token_ids": pids[q]}); keys.append((q, True))
                    params.append(SamplingParams(n=1, temperature=0.0, seed=s, max_tokens=ans_max, stop_token_ids=eos))
            outs = llm.generate(reqs, params, use_tqdm=False)
            rows = []
            for (q, greedy), o in zip(keys, outs):
                for j, c in enumerate(o.outputs):
                    ntok += len(c.token_ids)
                    rows.append(_row(cell, q, GREEDY_ID if greedy else j, prompts[q], len(pids[q]),
                                     reasoning=None, n_reasoning=0, closed=None, forced=None,
                                     answer_out=c, tok=tok))
            _append(cell.path, rows)
            print(f"  chunk {i // gen['chunk_size'] + 1}: {len(chunk)} q, {ntok} tok in "
                  f"{time.time() - t0:.0f}s", flush=True)
            continue

        if cond.budget is None:
            reqs, params, keys = [], [], []
            stop = ctrl.reasoning_stop()
            for q in chunk:
                s = request_seed(gen["seed"], cond.name, q)
                reqs.append({"prompt_token_ids": pids[q]}); keys.append((q, False))
                params.append(SamplingParams(n=cell.k, seed=s, max_tokens=gen["think_cap"], **stop, **samp))
                if cell.greedy:
                    reqs.append({"prompt_token_ids": pids[q]}); keys.append((q, True))
                    params.append(SamplingParams(n=1, temperature=0.0, seed=s, max_tokens=gen["think_cap"], **stop))
            outs = llm.generate(reqs, params, use_tqdm=False)
            for (q, greedy), o in zip(keys, outs):
                for j, c in enumerate(o.outputs):
                    ntok += len(c.token_ids)
                    ids, closed = ctrl.strip_reasoning_ids(list(c.token_ids))
                    samples.append({"qid": q, "sample_id": GREEDY_ID if greedy else j, "rids": ids,
                                    "closed": closed, "forced": not closed})
        else:
            # derived budget: cut the source trace at `budget` tokens
            for q in chunk:
                for sid in cell.sample_ids:
                    r = source_rows.get((q, sid))
                    if r is None:
                        raise RuntimeError(f"{cond.source} has no sample {q}#{sid}; run it first")
                    ids = enc(r["reasoning"])
                    if len(ids) <= cond.budget:       # trace fits: identical to the source sample
                        samples.append({"qid": q, "sample_id": sid, "copy": r})
                    else:
                        samples.append({"qid": q, "sample_id": sid, "rids": ids[:cond.budget],
                                        "closed": False, "forced": True})

        # ---- stage 2: the visible answer
        gen_samples = [s for s in samples if "copy" not in s]
        reqs, params = [], []
        for s in gen_samples:
            ids = pids[s["qid"]] + s["rids"] + enc(ctrl.answer_prefix(s["forced"]))
            seed = request_seed(gen["seed"], cond.name, "answer", s["qid"], s["sample_id"])
            greedy = s["sample_id"] == GREEDY_ID
            reqs.append({"prompt_token_ids": ids})
            params.append(SamplingParams(n=1, seed=seed, max_tokens=ans_max, stop_token_ids=eos,
                                         **({"temperature": 0.0} if greedy else samp)))
        outs = llm.generate(reqs, params, use_tqdm=False) if reqs else []
        rows = []
        for s, o in zip(gen_samples, outs):
            c = o.outputs[0]
            ntok += len(c.token_ids)
            rows.append(_row(cell, s["qid"], s["sample_id"], prompts[s["qid"]], len(pids[s["qid"]]),
                             reasoning=tok.decode(s["rids"]), n_reasoning=len(s["rids"]),
                             closed=s["closed"], forced=s["forced"], answer_out=c, tok=tok))
        for s in samples:
            if "copy" in s:
                rows.append({**s["copy"], "condition": cond.name, "derived_from": cond.source, "copied": True})
        _append(cell.path, rows)
        print(f"  chunk {i // gen['chunk_size'] + 1}: {len(chunk)} q, {ntok} tok in "
              f"{time.time() - t0:.0f}s ({ntok / max(time.time() - t0, 1e-9):.0f} tok/s)", flush=True)


def _row(cell: Cell, qid, sample_id, prompt, n_prompt, reasoning, n_reasoning, closed, forced, answer_out, tok):
    c = answer_out
    return {
        "model": cell.m["key"], "revision": cell.m["revision"], "condition": cell.cond.name,
        "benchmark": cell.benchmark, "split": cell.split, "qid": qid, "sample_id": sample_id,
        "prompt_hash": prompt_hash(prompt), "n_prompt_tokens": n_prompt,
        # reasoning: None for nothink. closed: the model ended its reasoning itself.
        # forced: the reasoning was cut (cap or budget) and an "answer now" sentence inserted.
        "reasoning": reasoning, "n_reasoning_tokens": n_reasoning,
        "reasoning_closed": closed, "forced_close": forced,
        "answer": tok.decode(c.token_ids, skip_special_tokens=True).strip(),
        "n_answer_tokens": len(c.token_ids), "answer_finish_reason": c.finish_reason,
        "answer_truncated": c.finish_reason == "length",
        "derived_from": cell.cond.source, "copied": False,
    }


def _append(path: Path, rows: list[dict]) -> None:
    with open(path, "a") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def run(exp_path: str, model: str, limit: int | None = None, out_dir: str | None = None,
        benchmarks: list[str] | None = None, split: str | None = None,
        conditions: list[str] | None = None) -> None:
    """Run every condition × benchmark of `model` in an experiment, with one loaded engine."""
    exp = load_experiment(exp_path)
    if out_dir:
        exp["out_dir"] = out_dir
    split = split or exp.get("split", "discovery")
    limit = limit or exp.get("limit")
    benches = benchmarks or exp["benchmarks"]
    m = model_info(model)
    conds = conditions_for(exp, model)
    if conditions:
        conds = [c for c in conds if c.name in conditions]
    assert conds, f"{model} has no conditions in {exp_path}"
    llm, tok = load_engine(m, exp["generation"])
    ctrl = make_control(tok, m)
    env = env_info()
    for cond in conds:
        meta_path = cell_dir(exp["out_dir"], model, cond.name) / "run_meta.json"
        meta_path.parent.mkdir(parents=True, exist_ok=True)
        meta = json.loads(meta_path.read_text()) if meta_path.exists() else {"sessions": []}
        meta.update({"experiment": exp["config_file"], "generation": exp["generation"], "model": m,
                     "condition": cond.__dict__})
        meta["sessions"].append({"started": datetime.now(timezone.utc).isoformat(), "limit": limit,
                                 "split": split, "benchmarks": benches, **env})
        meta_path.write_text(json.dumps(meta, indent=2) + "\n")
        for b in benches:
            run_cell(Cell(exp, m, cond, b, split), llm, tok, ctrl, limit)
