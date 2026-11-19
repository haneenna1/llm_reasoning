# Project: How reasoning training affects factual recall — first experiment

## Context (research idea)
I'm an MSc student researching LLM reasoning. Prior work (Yao et al. 2025, "Are Reasoning Models More Prone to Hallucination?", arXiv 2505.23646) found that reasoning models trained with SFT-only or RL-only hallucinate more on factual QA than their base models, while SFT→RL models do not. But their comparisons mix different base models, data and rewards, so the cause is not isolated. Separately, thinking mode helps factual QA on average, but sometimes flips a correct direct answer into a wrong one (arXiv 2607.05861: ~5–7.5% of TriviaQA questions in Qwen3, ~1–2% on GSM8K).

**Goal of the thesis:** a controlled, same-base-model study of how reasoning post-training regimes (SFT-only, RL-only, SFT→RL) change factual recall, and later a mechanistic explanation (activation patching across checkpoints, probes, model diffing) comparing successes and failures.

**Goal of this first phase (~3 weeks):** run the behavioural experiment and build a labelled dataset of successes and failures. Do NOT start the mechanistic analysis yet, but design the code so the same questions and prompts can be reused for it.

## Compute

## Models (same-base families, all public on Hugging Face)
Family A — MiMo-7B (needs trust_remote_code=True):
- XiaomiMiMo/MiMo-7B-Base (pretrained base)
- XiaomiMiMo/MiMo-7B-SFT (SFT-only)
- XiaomiMiMo/MiMo-7B-RL-Zero (RL-only, from base)
- XiaomiMiMo/MiMo-7B-RL (SFT → RL)

Family B — OLMo 3 7B (replication; run after Family A works):
- allenai/Olmo-3-1025-7B (base)
- allenai/Olmo-3-7B-Think-SFT
- allenai/Olmo-3-7B-Think-DPO
- allenai/Olmo-3-7B-Think (final, after RLVR)
(Check whether an OLMo 3 RL-Zero checkpoint is public; include it if so.)

Verify every model ID and chat template before running. Do not assume template details.

## Datasets
- TriviaQA, closed-book (no context passages), validation split, sample 2,000 questions (fixed seed). Use all answer aliases.
- PopQA (akariasai/PopQA), sample 2,000 stratified by entity popularity (s_pop) into ~5 bins.
- GSM8K test, sample 500 (math control).

## Conditions
For every checkpoint × question:
1. **Direct answer:** the base model gets a fixed few-shot prompt (5 QA examples, short answers). For post-trained reasoning models, suppress thinking. Inspect each chat template and find the cleanest way (e.g. prefill an empty `<think>\n\n</think>` block). Document the method per model and check that outputs really contain no reasoning.
2. **With thinking:** the model's normal reasoning mode, max 4,096 new tokens. Record truncation.

Sampling: K=8 samples per question per condition, temperature 0.6, top-p 0.95, plus one greedy run. Use vLLM. Save full raw outputs (including reasoning traces) to disk, e.g. JSONL/Parquet keyed by (model, condition, question_id, sample_id).

## Grading
- Extract the final answer (after the reasoning block).
- Factual QA: normalised exact match / containment against all aliases (SQuAD-style normalisation). Also label "not attempted" (refusal / "I don't know").
- GSM8K: numeric match.
- Hand-check 100 random gradings and report agreement. If agreement is below 95%, add an LLM-judge pass (open-weight judge model, documented prompt).

## Analysis to produce
1. Accuracy, hallucination rate (incorrect, excluding not-attempted) and abstention rate per model × condition × dataset, with bootstrap 95% CIs.
2. Per-question accuracy = fraction of the K samples correct. Label each question as:
   - **Training transitions** (direct-answer mode): base-correct → post-trained-wrong ("training-induced failure") and the reverse ("training-induced success"), for each of SFT, RL-Zero, SFT→RL vs. base. Robust = ≥6/8 correct on one side and ≤2/8 on the other.
   - **Thinking transitions** (within each post-trained checkpoint): direct-correct → thinking-wrong and the reverse, with the same thresholds.
   - Stable-correct / stable-wrong.
3. Counts of each transition type per model and dataset, with the PopQA breakdown by popularity bin.
4. A sample of 50 failures per main comparison, with traces exported to a readable file for manual labelling (never recalled the fact / reasoning reached the right answer but final answer differs / repeated flawed reasoning / abstained).

## Go/no-go
Report whether each comparison has at least ~200 robust failures AND ~200 matched successes (for the mechanistic phase). If factual QA falls short, say so. The backup behaviour is instruction following (IFEval).

## Engineering requirements
- Python project with clear structure: `configs/` (one YAML per model+condition), `src/` (data loading, prompting, generation, grading, analysis), `scripts/`, `results/`, `notebooks/` or report.
- One command reruns everything from config. Fix seeds and log package versions.
- Keep prompts, question IDs and answer extraction identical across models.
- Make generation resumable (skip already-completed items).
- Start small: a smoke test on 50 questions with MiMo-7B-Base and MiMo-7B-RL, both conditions, before the full run.
- Write a short `RESULTS.md` with the tables above and the go/no-go verdict.

## Order of work
1. Set up the repo and environment; verify model IDs and inspect chat templates (report findings to me before the full runs).
2. Data loaders and sampling (save fixed question lists).
3. Prompting + generation with vLLM, run the smoke test, show me sample outputs.
4. Grading + manual check.
5. Full run, Family A.
6. Analysis, transition labels, failure export, RESULTS.md.
7. Family B replication.

Ask me before any decision that changes the experimental design. Report back after step 1 and step 3.