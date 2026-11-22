"""Download pinned model checkpoints and benchmark sources.

    python scripts/download_assets.py --models core            # a group from configs/models.yaml
    python scripts/download_assets.py --models qwen3_8b gpt_oss_20b
    python scripts/download_assets.py --datasets               # every source in configs/benchmarks.yaml

Models: each revision_prefix is resolved to a full commit SHA. Datasets: HF dataset
repos are pinned to their current SHA on first download; GitHub files are pinned to
the latest commit touching that path and saved under data/raw/github/. Everything
is recorded in configs/resolved_revisions.json, and later runs read it from there.
A source that is already recorded is not re-resolved, so pins never move silently.
Pass --refresh to re-pin.
"""
import argparse
import json
import time
import urllib.request
from pathlib import Path

import yaml
from huggingface_hub import HfApi, snapshot_download

ROOT = Path(__file__).resolve().parents[1]
REV_PATH = ROOT / "configs/resolved_revisions.json"
MODEL_PATTERNS = ["*.json", "*.py", "*.safetensors", "*.txt", "*.jinja", "*.model", "*.tiktoken"]
MODEL_IGNORE = ["original/*", "metal/*"]   # gpt-oss ships duplicate non-HF weights there


def resolve_model(api, repo, prefix):
    for c in api.list_repo_commits(repo):
        if c.commit_id.startswith(prefix):
            return c.commit_id
    raise ValueError(f"{repo}: no commit starts with {prefix}")


def github_latest_sha(repo: str, path: str) -> str:
    url = f"https://api.github.com/repos/{repo}/commits?path={path}&per_page=1"
    with urllib.request.urlopen(url) as r:
        return json.load(r)[0]["sha"]


def dataset_sources() -> list[dict]:
    """Unique sources referenced by configs/benchmarks.yaml."""
    cfg = yaml.safe_load(open(ROOT / "configs/benchmarks.yaml"))
    seen, out = set(), []
    for b in cfg["benchmarks"].values():
        s = b["source"]
        key = (s["type"], s["repo"], s.get("path"))
        if key not in seen:
            seen.add(key)
            out.append(s)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="*", default=[], help="group names or model keys")
    ap.add_argument("--datasets", action="store_true")
    ap.add_argument("--refresh", action="store_true", help="re-pin dataset sources")
    a = ap.parse_args()

    api = HfApi()
    reg = yaml.safe_load(open(ROOT / "configs/models.yaml"))
    flat = {k: v for grp in reg.values() for k, v in grp.items()}
    resolved = json.loads(REV_PATH.read_text()) if REV_PATH.exists() else {}

    def save():
        REV_PATH.write_text(json.dumps(resolved, indent=2) + "\n")

    keys = []
    for m in a.models:
        keys += list(reg[m]) if m in reg else [m]
    for k in keys:
        m = flat[k]
        sha = resolve_model(api, m["hf_id"], m["revision_prefix"])
        t = time.time()
        path = snapshot_download(m["hf_id"], revision=sha, allow_patterns=MODEL_PATTERNS,
                                 ignore_patterns=MODEL_IGNORE)
        print(f"[model] {k}: {m['hf_id']}@{sha[:10]} -> {path} ({time.time() - t:.0f}s)", flush=True)
        resolved[k] = {"hf_id": m["hf_id"], "revision": sha}
        save()

    if a.datasets:
        for s in dataset_sources():
            if s["type"] == "hf":
                key = f"dataset:{s['repo']}"
                sha = resolved.get(key, {}).get("revision")
                if sha is None or a.refresh:
                    sha = api.dataset_info(s["repo"]).sha
                pats = s.get("allow_patterns")
                path = snapshot_download(s["repo"], repo_type="dataset", revision=sha, allow_patterns=pats)
                resolved[key] = {"revision": sha}
                print(f"[dataset] {s['repo']}@{sha[:10]} -> {path}", flush=True)
            elif s["type"] == "github":
                key = f"github:{s['repo']}/{s['path']}"
                sha = resolved.get(key, {}).get("revision")
                if sha is None or a.refresh:
                    sha = github_latest_sha(s["repo"], s["path"])
                dest = ROOT / "data/raw/github" / s["repo"] / s["path"]
                dest.parent.mkdir(parents=True, exist_ok=True)
                url = f"https://raw.githubusercontent.com/{s['repo']}/{sha}/{s['path']}"
                urllib.request.urlretrieve(url, dest)
                resolved[key] = {"revision": sha, "local": str(dest.relative_to(ROOT))}
                print(f"[github] {s['repo']}/{s['path']}@{sha[:10]} -> {dest}", flush=True)
            else:
                raise ValueError(s)
            save()


if __name__ == "__main__":
    main()
