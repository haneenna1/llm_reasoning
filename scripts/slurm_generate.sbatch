#!/bin/bash
#SBATCH --job-name=gen
#SBATCH --partition=public
#SBATCH --gres=gpu:L40:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=2-00:00:00
#SBATCH --output=logs/gen_%x_%j.log
# One model per job (1x L40, bf16). Pass all of that model's configs so the
# engine is loaded once; extra flags go straight to run_generation.py.
#   sbatch -J mimo_rl scripts/slurm_generate.sbatch configs/runs/mimo_rl_{direct,think}.yaml
#   sbatch -J smoke_rl scripts/slurm_generate.sbatch --limit 50 --out_dir results/smoke configs/runs/mimo_rl_*.yaml
# Limit on newton public: 4 GPUs / 300 CPUs per user -> at most 4 of these at once.
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
