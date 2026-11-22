"""Generate completions for one model of an experiment (resumable).

    python scripts/run_generation.py configs/experiments/smoke.yaml --model qwen3_1p7b
    python scripts/run_generation.py configs/experiments/discovery.yaml --model qwen3_8b \
        [--benchmarks triviaqa popqa] [--conditions nothink think] [--limit 50] [--out_dir results/tmp]

All conditions x benchmarks of the model run with one loaded vLLM engine.
"""
import argparse
import os

os.environ.setdefault("HF_HUB_OFFLINE", "1")  # everything is pre-downloaded and pinned

from think_failures.generate import run  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("experiment")
    ap.add_argument("--model", required=True)
    ap.add_argument("--benchmarks", nargs="+")
    ap.add_argument("--conditions", nargs="+")
    ap.add_argument("--split", choices=["discovery", "confirm"])
    ap.add_argument("--limit", type=int, help="first N questions per benchmark")
    ap.add_argument("--out_dir")
    a = ap.parse_args()
    run(a.experiment, a.model, limit=a.limit, out_dir=a.out_dir, benchmarks=a.benchmarks,
        split=a.split, conditions=a.conditions)


if __name__ == "__main__":
    main()
