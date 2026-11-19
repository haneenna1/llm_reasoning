#!/bin/bash
#SBATCH --job-name=envcheck
#SBATCH --partition=all
#SBATCH --gres=gpu:2080ti:2
#SBATCH --cpus-per-task=4
#SBATCH --mem=64G
#SBATCH --time=02:00:00
#SBATCH --output=logs/envcheck_%j.log
# Usage: sbatch scripts/slurm_env_check.sbatch <hf_id> <revision> <mimo|olmo>
set -euo pipefail
cd /home/haneenna/llm_reasoning
source "$HOME/miniforge3/etc/profile.d/conda.sh"
conda activate reasoning-recall
MODEL=$1; REV=$2; MODE=$3
echo "host=$(hostname) gpus=$CUDA_VISIBLE_DEVICES"; nvidia-smi --query-gpu=name,memory.used,memory.total --format=csv
python - "$MODEL" "$REV" <<'EOF'
import sys, time
from huggingface_hub import snapshot_download
t = time.time()
p = snapshot_download(sys.argv[1], revision=sys.argv[2], allow_patterns=["*.json", "*.py", "*.safetensors", "*.txt", "*.jinja", "*.model"])
print("downloaded", p, f"{time.time()-t:.0f}s", flush=True)
EOF
export HF_HUB_OFFLINE=1
python scripts/env_check_vllm.py --model "$MODEL" --mode "$MODE" --tp 2
