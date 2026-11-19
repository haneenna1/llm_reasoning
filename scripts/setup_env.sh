#!/bin/bash
# Build the reasoning-recall conda env, then download Family A models + datasets.
# Run detached:  setsid nohup bash scripts/setup_env.sh > logs/setup_env.log 2>&1 &
set -euo pipefail
cd /home/haneenna/llm_reasoning
source "$HOME/miniconda3/etc/profile.d/conda.sh"
conda activate reasoning-recall
echo "[$(date)] python=$(which python) pip=$(which pip)"

echo "[$(date)] pip install"
pip install "vllm==0.34.0" datasets pandas pyarrow pyyaml
pip freeze > logs/pip_freeze.txt
python -c "import torch, vllm, transformers; print('torch', torch.__version__, 'cuda', torch.version.cuda, 'gpu', torch.cuda.is_available()); print('vllm', vllm.__version__, 'transformers', transformers.__version__)"

echo "[$(date)] downloading datasets"
python scripts/download_assets.py --datasets
echo "[$(date)] downloading Family A models"
python scripts/download_assets.py --models family_a
echo "[$(date)] SETUP DONE"
