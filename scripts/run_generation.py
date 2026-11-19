"""Generate completions for one or more run configs (resumable).

    python scripts/run_generation.py configs/runs/mimo_rl_direct.yaml configs/runs/mimo_rl_think.yaml
    python scripts/run_generation.py --limit 50 --out_dir results/smoke configs/runs/mimo_base_*.yaml

Configs for the same model share one loaded vLLM engine.
"""
import argparse
import os

os.environ.setdefault("HF_HUB_OFFLINE", "1")  # everything is pre-downloaded and pinned

from reasoning_recall.generate import run  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("configs", nargs="+")
    ap.add_argument("--limit", type=int, help="first N questions per dataset (smoke tests)")
    ap.add_argument("--out_dir", help="override out_dir (e.g. results/smoke)")
    ap.add_argument("--datasets", nargs="+")
    a = ap.parse_args()
    run(a.configs, limit=a.limit, out_dir=a.out_dir, datasets=a.datasets)


if __name__ == "__main__":
    main()
