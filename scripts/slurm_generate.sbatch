#!/bin/bash
#SBATCH --job-name=gen
#SBATCH --account=nlp
#SBATCH --partition=nlp
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=2-00:00:00
#SBATCH --output=logs/gen_%x_%j.log
# Excluded nodes: SINGLE SOURCE OF TRUTH (submit_generate.sh reads this line too).
# nlp-l40-1, bruno1: drivers < 580 (too old for cu130), found by the check below.
# nlp-2080-2: 2080ti has no bf16.
#SBATCH --exclude=nlp-l40-1,bruno1,nlp-2080-2
# Defaults: nlp account/partition (high priority), any bf16 GPU. Prefer submitting via
# scripts/submit_generate.sh, which picks the fastest free card (nlp first, then public/cs).
# One model per job (1 GPU, bf16): all of its conditions x benchmarks run with
# one loaded engine; extra flags go straight to run_generation.py.
#   scripts/submit_generate.sh -J q8_disc configs/experiments/discovery.yaml --model qwen3_8b
#   scripts/submit_generate.sh -J smoke_q2 configs/experiments/smoke.yaml --model qwen3_1p7b
#   scripts/submit_generate.sh -J q8_disc --time=12:00:00 -- configs/experiments/discovery.yaml --model qwen3_8b   (extra sbatch flags before --)
# Manual: sbatch -J mimo_rl [-A cs -p public --gres=gpu:A100:1] scripts/slurm_generate.sbatch <args>
# (don't pass --exclude on the CLI: it replaces this list instead of extending it)
# Policy on public (-A cs): 4 GPUs / 300 CPUs per user.
set -euo pipefail
cd /home/haneenna/llm_reasoning
source "$HOME/miniconda3/etc/profile.d/conda.sh"
conda activate reasoning-recall
echo "host=$(hostname) job=$SLURM_JOB_ID gpus=$CUDA_VISIBLE_DEVICES args=$*"
nvidia-smi --query-gpu=name,driver_version,memory.used,memory.total --format=csv
# torch 2.14+cu130 needs an NVIDIA driver with CUDA >= 13.0 (driver >= 580).
# Some newton nodes have older drivers (e.g. nlp-l40-1: CUDA 12.2) -> fail fast.
drv=$(nvidia-smi --query-gpu=driver_version --format=csv,noheader | head -1 | cut -d. -f1)
if [ "$drv" -lt 580 ]; then echo "FATAL: driver $drv on $(hostname) too old for cu130; add it to --exclude"; exit 3; fi
# FlashInfer's top-p sampler JIT-compiles with the system nvcc (/usr/local/cuda),
# which is too old for its flags. Use vLLM's PyTorch sampler instead (same top-p).
export VLLM_USE_FLASHINFER_SAMPLER=0
python scripts/run_generation.py "$@"
echo "JOB DONE"
