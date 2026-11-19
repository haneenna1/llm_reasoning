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
nvidia-smi --query-gpu=name,memory.used,memory.total --format=csv
python scripts/run_generation.py "$@"
echo "JOB DONE"
