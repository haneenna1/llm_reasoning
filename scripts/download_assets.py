"""Download pinned model checkpoints and raw datasets into the HF cache.

Usage:
    python scripts/download_assets.py --models family_a      # models only
    python scripts/download_assets.py --datasets             # datasets only
    python scripts/download_assets.py --models family_a --datasets

Each model's revision_prefix (configs/models.yaml) is resolved to a full commit
SHA, which is written to configs/resolved_revisions.json. Later runs load models
by that full SHA, so the weights cannot change underneath an experiment.
"""
import argparse
import json
import time
from pathlib import Path

import yaml
from huggingface_hub import HfApi, snapshot_download

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATTERNS = ["*.json", "*.py", "*.safetensors", "*.bin", "*.txt", "*.jinja",
                  "*.model", "*.tiktoken"]

# (repo_id, allow_patterns): only the files the project needs.
DATASETS = {
    "mandarjoshi/trivia_qa": ["rc.nocontext/validation-*", "README.md"],
    "akariasai/PopQA": ["*"],
    "openai/gsm8k": ["main/test-*", "README.md"],
}


def resolve(api, repo, prefix):
    for c in api.list_repo_commits(repo):
        if c.commit_id.startswith(prefix):
            return c.commit_id
    raise ValueError(f"{repo}: no commit starts with {prefix}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="*", default=[], help="family keys or model keys")
    ap.add_argument("--datasets", action="store_true")
    a = ap.parse_args()

    api = HfApi()
    reg = yaml.safe_load(open(ROOT / "configs/models.yaml"))
    flat = {k: v for fam in reg.values() for k, v in fam.items()}
    keys = []
    for m in a.models:
        keys += list(reg[m]) if m in reg else [m]

    out_path = ROOT / "configs/resolved_revisions.json"
    resolved = json.loads(out_path.read_text()) if out_path.exists() else {}
    for k in keys:
        m = flat[k]
        sha = resolve(api, m["hf_id"], m["revision_prefix"])
        pats = MODEL_PATTERNS if "bin" in m.get("weights", "safetensors") else \
            [p for p in MODEL_PATTERNS if p != "*.bin"]
        t = time.time()
        path = snapshot_download(m["hf_id"], revision=sha, allow_patterns=pats)
        print(f"[model] {k}: {m['hf_id']}@{sha[:10]} -> {path} ({time.time()-t:.0f}s)", flush=True)
        resolved[k] = {"hf_id": m["hf_id"], "revision": sha}
        out_path.write_text(json.dumps(resolved, indent=2) + "\n")

    if a.datasets:
        for repo, pats in DATASETS.items():
            sha = api.dataset_info(repo).sha
            path = snapshot_download(repo, repo_type="dataset", revision=sha, allow_patterns=pats)
            print(f"[dataset] {repo}@{sha[:10]} -> {path}", flush=True)
            resolved[f"dataset:{repo}"] = {"revision": sha}
            out_path.write_text(json.dumps(resolved, indent=2) + "\n")


if __name__ == "__main__":
    main()
