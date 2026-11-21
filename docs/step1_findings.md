# Step 1 findings: environment, model IDs, chat templates (2026-11-18)

## Compute (cluster `lambda`, SLURM partition `all`)
- Nodes: lambda1 (8× RTX 2080 Ti), lambda2 (6× 2080 + 2× 2080 Ti), lambda3 (7× Titan Xp), lambda4 (8× 2080 Ti). 11–12 GB per GPU. Driver 595.91, CUDA 13.2.
- GPUs are shared and not exclusive: other users' processes were seen on them (e.g. 3.4 GB in use on a lambda4 GPU).
- Limit: at most 2 GPUs per job (user instruction).
- Turing (sm_75) and Pascal (sm_61) have **no bf16**. Both families are stored in bf16, so we must run in fp16, which risks overflow. This needs an equivalence check against bf16 on CPU or with a reference.
- Titan Xp (sm_61) is below vLLM's minimum (sm_70), so only the 2080/2080 Ti nodes are usable.

## Model IDs: all verified public, not gated
| key | HF id | rev | role |
|---|---|---|---|
| mimo_base | XiaomiMiMo/MiMo-7B-Base | d892dcc601 | base |
| mimo_sft | XiaomiMiMo/MiMo-7B-SFT | 0a9f1180d9 | SFT-only |
| mimo_rl_zero | XiaomiMiMo/MiMo-7B-RL-Zero | da0bde6fbb | RL-only |
| mimo_rl | XiaomiMiMo/MiMo-7B-RL | 7c7707596b | SFT→RL |
| olmo_base | allenai/Olmo-3-1025-7B | a81bae42db | base |
| olmo_think_sft | allenai/Olmo-3-7B-Think-SFT | 6ff857587e | SFT |
| olmo_think_dpo | allenai/Olmo-3-7B-Think-DPO | 7b18bf927b | SFT→DPO (weights in .bin, not safetensors) |
| olmo_think | allenai/Olmo-3-7B-Think | d97e442d7c | SFT→DPO→RLVR |

OLMo 3 RL-Zero **is public**, in several variants, all fine-tuned from `Olmo-3-1025-7B`: `-RL-Zero-Mix`, `-Math`, `-Code`, `-IF`, `-General` (plus `Olmo-3.1-7B-RL-Zero-Math/Code`, which come from a different base and should be excluded).

Architecture: MiMo is `MiMoForCausalLM` (Qwen2-like, 36 layers, GQA with 8 KV heads, 144 KiB KV/token in fp16, plus 1 MTP layer that is unused). OLMo 3 is `Olmo3ForCausalLM` (32 layers, **no GQA**: 32 KV heads, 512 KiB/token, sliding window 4096 on some layers).

## Chat templates
### MiMo
- All four checkpoints use the **same plain ChatML (Qwen2.5) template, with no `<think>` logic**. The generation prompt is `<|im_start|>assistant\n`.
- If no system message is given, the template inserts `You are a helpful assistant.` The README recommends an **empty system prompt**, so we pass `{"role":"system","content":""}`.
- `<think>` / `</think>` are **not special tokens**; they are plain text. The SFT and RL models emit `<think>…</think>` on their own.
- EOS: SFT and RL use `<|im_end|>` (151645). Base and **RL-Zero** use `<|endoftext|>` (151643): RL-Zero shares Base's tokenizer config. The model card doesn't document the prompt format RL-Zero was trained with.
- Planned direct-answer method for SFT/RL: render the chat template, then prefill `<think>\n\n</think>\n\n`. This must be verified empirically, since the template has no native no-think switch.

### OLMo 3
- Base: no chat template.
- Think-SFT, DPO, Think and RL-Zero-Mix use a ChatML template whose generation prompt is `<|im_start|>assistant\n<think>`, so **thinking is forced open by the template**. EOS ids are [100265 `<|im_end|>`, 100257 `<|endoftext|>`].
- Default system prompts **differ**: Think-SFT says "You are Olmo… date cutoff December 2024"; DPO, Think and RL-Zero say "You are OLMo, a helpful function-calling AI assistant… November 2024… <functions></functions>".
- Planned direct-answer method: generation prompt plus prefill `</think>\n\n`, so the model sees `<think></think>`.
- Generation defaults: temperature 0.6, top_p 0.95, consistent with the project spec.

## Update 2026-11-19: moved to cluster `newton`
The project now runs on cluster `newton`, which replaces `lambda`. The compute notes above are superseded:
- GPU nodes with bf16 are available: A100, A40, L40, RTX 6000 Ada, H200, RTX PRO 6000. We have two accounts: `cs` → `public` partition (limit: 4 GPUs / 300 CPUs per user) and `nlp` → `nlp` partition (PriorityTier 100; preferred). CPU-only jobs are rejected. `scripts/submit_generate.sh` picks the fastest free card, nlp first, then public. **Models will run in bf16 (native dtype), not fp16**, so the fp16-overflow concern above no longer applies.
- A bf16 MiMo-7B checkpoint (~15 GB) fits on a single 40–48 GB GPU, so tensor parallelism is not needed.
- `nlp-2080-2` (2080 Ti, no bf16) is the interactive/dev node only, not for experiment runs.
- Env: Miniconda at `~/miniconda3`, env `reasoning-recall` (Python 3.12, vllm 0.34.0, torch 2.14.0+cu130, transformers 5.22.2). Spec: `environment.yml`; full freeze: `logs/pip_freeze.txt`. Built by `scripts/setup_env.sh`.
- Assets in the HF cache `~/.cache/huggingface` (NFS, visible from all nodes). Full revisions are in `configs/resolved_revisions.json`. Downloaded so far: Family A (4 MiMo checkpoints, 59 GB), TriviaQA rc.nocontext validation (17,944), PopQA test (14,267), GSM8K test (1,319).
- NVIDIA drivers differ between nodes. Our torch build (cu130) needs driver >= 580. `nlp-l40-1` (CUDA 12.2) fails; `houdini` (595.58) works. `scripts/slurm_generate.sbatch` checks the driver and exits early on old nodes.
- FlashInfer's JIT sampler fails with the system nvcc, so jobs set `VLLM_USE_FLASHINFER_SAMPLER=0` (vLLM's PyTorch top-p sampler).
