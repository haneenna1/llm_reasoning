# Phase 0 findings: prior work, models, think control, benchmarks (2026-11-21)

## 1. Prior work: what is already known

Most closely related work. Every item was read from its arXiv abstract and HTML text; items 1–6 were checked on 2026-11-21.

| # | Paper | Same weights? | Tasks | Thinking hurts? | Mechanism? | Stats |
|---|---|---|---|---|---|---|
| 1 | **MARGO**, Wang et al., arXiv 2607.05861 (Jul 2026) | yes (Qwen3 1.7B–32B) | TriviaQA, SimpleQA(-V), NQ, PopQA, HotpotQA; math | correct→wrong flips on TriviaQA = 5.4–7.5% of *all* questions (≈10–22% of no-think-correct); flips enriched for "But wait" traces | none | transition matrix only; no CIs/seeds; Qwen3-32B judge |
| 2 | **Built-in thinking in IF**, Senthil Kumar, arXiv 2606.09662 (Jun 2026) | yes (Qwen3 1.7B–32B; Hunyuan) | IFEval | −0.6 to −3.5 pp; 10–20% prompt flips; "Precision" constraints hurt, "Planning" helped | activation patching | greedy, 3 seeds, bootstrap CIs on patching only |
| 3 | **When Thinking Backfires**, Yan et al., arXiv 2509.00544 (ICLR 2026) | yes (Qwen3 4B–32B) | HEx-PHI, HarmBench, AgentHarm | misalignment ON vs OFF: 23% vs 15% (4B), 23% vs 8% (32B) | refusal heads, steering, neuron ablation | Pearson over checkpoints |
| 4 | **Thinking to Recall**, Gekhman et al., arXiv 2603.09906 (Mar 2026) | toggle (Gemini, Qwen3-32B) | SimpleQA-V, EntityQuestions | thinking *helps* recall on average; hallucinated intermediate facts predict wrong answers; traces >2k tokens counterproductive | behavioural probes | CIs on subsets |
| 5 | **HRBench**, Ning et al., arXiv 2605.28398 (May 2026) | native hybrid (Qwen3.5, gpt-oss, …) | math, code only | no-think beats full-think at 2B; mixed at 9B | none | greedy, no tests |
| 6 | **Thinking Leakage**, Liu & Honavar, arXiv 2609.28682 (Sep 2026) | yes (Qwen3 4B/8B) | competition math | concerns *no-think post-training* drifting toward think; uses split-half placebo null + repetition filter | steering, mediation | Spearman, Cohen's d |
| 7 | Inverse Scaling in TTC, Gema et al., arXiv 2507.14417 (TMLR 2025) | mostly frontier APIs | distractor counting, spurious regression, Zebra deduction, AI-risk | longer thinking lowers accuracy | none | — |
| 8 | When Thinking Fails, Li et al., arXiv 2505.11423 (NeurIPS 2025) | CoT prompting, 15 models | IFEval, ComplexBench | consistent drops | attention to constraint tokens | — |
| 9 | AbstentionBench, Kirichenko et al., arXiv 2506.09038 (NeurIPS 2025 D&B) | different models | 20 datasets (false premise, underspecified, unknowable…) | reasoning FT degrades abstention ≈24% | none | — |
| 10 | Sycophancy: Feng et al. ACL 2026; "Yes-Bias" ICLR 2026; "Sycophantic Anchors" arXiv 2601.21183 | mixed | sycophancy | **conflicting**: reasoning lowers final-answer sycophancy but can hide it | anchors (trace sentences) | — |
| 11 | Knowledge conflict: arXiv 2605.27773, arXiv 2504.07128 | partly | PopQA conflict, context vs memory | reasoning models follow context but get erratic with long chains | partial | — |
| 12 | OptimalThinkingBench (ICLR 2026); Illusion of Thinking (2506.06941); BrainBench (2603.14761) | mixed | easy queries, puzzles, commonsense | overthinking on easy items; "initial intuition right, deliberation pulls away" | none | — |

### Implications for our novelty claim
- **Finding a single failure mode is no longer novel.** Same-weights Qwen3 ON/OFF has already been reported for factual QA (1), instruction following (2), with patching, and safety (3), with mechanism.
- **What is still missing**, and is our contribution:
  1. A **cross-task screen on the same weights** with **sampling-based statistics**. None of the papers above uses K samples per question, a noise floor for flips, FDR correction, or a held-out confirmation split. Papers (1) and (2) are greedy or single-seed. The split-half placebo idea in (6) supports our noise-floor design.
  2. **Dose–response over thinking budgets** on open same-weights models. Paper (7) does this mainly on APIs; papers (1)–(3) only compare ON/OFF.
  3. **A comparative mechanism across failure modes.** Is there one shared "the trace overrides a correct early answer" mechanism, as suggested for factual QA in (1) and IF "Precision" in (2), or several different ones? No paper compares mechanisms across tasks.
  4. **A cross-task router/monitor** (Phase 3). Existing work is single-task: classifier-selective reasoning (8), MARGO's RL (1).
- **Concrete hypotheses** inherited from prior work: (1) "But wait" self-doubt drives factual flips; (2) Precision vs Planning constraints; (4) hallucinated intermediate facts; (7) distraction/spurious features scale with length.
- **Confound to control** (from 6 and HRBench): no-think outputs that still contain reasoning. We measure reasoning-marker density in no-think outputs, and filter degenerate repetition (12-gram repetition ratio > 0.3).

### Mechanistic analysis in prior work: what has been done on think-induced failures
| Paper | Analysis of failures | Causal? | Gaps |
|---|---|---|---|
| 2606.09662 (IF) | activation patching (attn/MLP/residual, every layer) between passing and failing runs, **prompt pass only**; positions matched by absolute index; metric is the restoration rate after regenerating | interventional, but the authors call it "descriptive" | never patches the **trace** or the post-trace answer position; position alignment across templates unchecked; failure vs success populations not matched |
| 2505.11423 (IF) | attention mass on constraint tokens: think-hurt prompts show a larger drop, mostly in early–mid layers | correlational | CoT prompting, not native thinking; no tests |
| 2509.00544 (safety) | refusal heads move attention to the empty think span in no-think mode; ablating heads/neurons lowers refusal | causal | concerns refusal, not answer accuracy; mostly about reasoning *fine-tuning* |
| 2601.21183 (sycophancy) | counterfactual rollouts find "anchor" sentences; linear probes on them | correlational | no think-vs-no-think comparison |
| 2608.22332 (CoT math) | per-token, per-head patching CoT → no-CoT | causal | only cases where CoT *helps*; 0.5B model, 32 items |
| 2607.05861 (factual), 2603.09906, HRBench, 2507.14417, AbstentionBench | none | — | — |

**Open for our Phase 2:**
- **Trace-level localisation of the flip** on failure cases: early answering / logit lens along the trace, sentence resampling.
- **Patching at the post-trace answer position** between think and no-think.
- Any mechanism at all for factual, abstention, distractor or context-faithfulness failures.
- A **cross-task comparison** of mechanisms.
- A statistically matched contrast of failures vs successes.

## 2. Models (HF revisions checked 2026-11-21; all public, not gated)

| key | HF id | rev | arch | size (bf16) | notes |
|---|---|---|---|---|---|
| qwen3_1p7b | Qwen/Qwen3-1.7B | 70d244cc86 | Qwen3ForCausalLM, 28 L, d=2048 | 4.1 GB | Qwen SAEs exist for **Qwen3-1.7B-Base** |
| qwen3_4b | Qwen/Qwen3-4B | 1cfa9a7208 | 36 L, d=2560 | 8.0 GB | |
| qwen3_8b | Qwen/Qwen3-8B | b968826d9c | 36 L, d=4096 | 16.4 GB | Qwen SAEs exist for **Qwen3-8B-Base** |
| qwen3_14b | Qwen/Qwen3-14B | 40c069824f | 40 L, d=5120 | 29.5 GB | optional |
| gpt_oss_20b | openai/gpt-oss-20b | 6cee5e81ee | GptOssForCausalLM (MoE), 24 L, MXFP4 | ~13 GB of weights (the repo also holds a duplicate `original/` copy) | harmony format |
| olmo3_think | allenai/Olmo-3-7B-Think | d97e442d7c | Olmo3ForCausalLM, 32 L, no GQA | 14.6 GB | replication |
| olmo3_instruct | allenai/Olmo-3-7B-Instruct | 6e5971d9eb | same | 14.6 GB | replication reference (different weights) |
| mimo_rl | XiaomiMiMo/MiMo-7B-RL | 7c7707596b | MiMoForCausalLM | ~15 GB | replication (infra exists) |

Newer Qwen generations exist: Qwen3.5 (0.8B/2B/4B/9B/27B…, Mar 2026), Qwen3.6 (27B, 35B-A3B), Qwen3.8 (27B+). The small **Qwen3.5** models are hybrid think/no-think, but they are **multimodal** (`Qwen3_5ForConditionalGeneration`, with a vision encoder) and use **hybrid linear attention** (Gated-DeltaNet-style `linear_attention` layers mixed with full attention). That makes activation patching and attention attribution less standard, though Qwen has released SAEs for Qwen3.5-2B/9B-Base. **Recommendation:** keep **Qwen3** as the core (standard transformer, SAEs, and comparable to papers 1–3, 6). Qwen3.5-2B/9B is an optional "newer generation" replication.

**vLLM 0.34.0** (the installed env) supports `Qwen3ForCausalLM`, `GptOssForCausalLM`, `Olmo3ForCausalLM` and `Qwen3_5ForConditionalGeneration`. This is a registry check only; actually loading each model on newton GPUs happens in the step-4 smoke test.

## 3. Think control per model (rendered chat templates)

| model | think | no-think | effort levels |
|---|---|---|---|
| Qwen3 | `enable_thinking=True`: prompt ends `<|im_start|>assistant\n`, and the model opens `<think>` itself | `enable_thinking=False`: the **template itself prefills** `<think>\n\n</think>\n\n` | budget forcing: stop at N tokens, append `\n</think>\n\n` (`</think>` = single token 151668) |
| Qwen3.5 | template forces `<think>\n` open | template prefills `<think>\n\n</think>\n\n` | budget forcing |
| gpt-oss-20b | `reasoning_effort` low / medium / high, written into the system prompt (`Reasoning: high`) | **no native off.** An empty `analysis` channel could be prefilled, but that is out of distribution | native low/med/high, plus budget forcing on the `analysis` channel |
| OLMo-3-7B-Think | template ends `<think>` | prefill `</think>\n\n` (out of distribution) | budget forcing |
| OLMo-3-7B-Instruct | n/a (no thinking) | native | — |

Gotchas found:
- **gpt-oss's template inserts `Current date: <today>`**. We must pin it (e.g. 2026-11-21) or results will change from day to day.
- gpt-oss and OLMo tokenise `<think>` as plain text. Only Qwen has `<think>`/`</think>` as single special tokens.
- Qwen3 no-think uses the same mechanism as our MiMo/OLMo prefill (an empty think block), but for Qwen3 it is **in distribution**: the model was trained on it.
- Qwen's recommended sampling **differs by mode**: think T=0.6, top-p 0.95, top-k 20. No-think, from the model card, T=0.7, top-p 0.8, top-k 20. This is a confound (see decision C).

## 4. Benchmarks on the HF Hub

| category | source | status |
|---|---|---|
| factual | TriviaQA, PopQA (already sampled); `google/simpleqa-verified` | OK |
| abstention / false premise | `facebook/AbstentionBench`. It bundles FalseQA, underspecified math, unknowable questions and more, so it replaces separate FalseQA/MiP downloads | OK |
| instruction following | `google/IFEval` (OK). ComplexBench is not on HF, only on GitHub | IFEval OK; ComplexBench needs the GitHub release |
| distractors | `voidful/GSM-IC`; `inverse-scaling-ttc/inverse-scaling-ttc-main` | OK |
| sycophancy | `meg-tong/sycophancy-eval` (answer suggestion, "are you sure?") | OK |
| context faithfulness | `pminervini/NQ-Swap` | OK |
| intuitive/implicit | "Mind Your Step" tasks: GitHub only | to source |
| over-refusal / safety | `walledai/XSTest`, `walledai/StrongREJECT` (gated=auto, so terms are accepted automatically with an HF token) | OK |
| positive control | GSM8K (already sampled), `HuggingFaceH4/MATH-500` | OK |

## 5. Smoke test (step 4, 2026-11-21)
Setup: `configs/experiments/smoke.yaml`. First 20 discovery questions × 19 benchmarks; Qwen3-1.7B and Qwen3-8B (nothink / think / think_b256 / think_b1024), gpt-oss-20b (effort_low / effort_high / effort_high_b256); K=2 think samples, K=4 no-think, cap 4096; one H200 per model. All 3 jobs finished without errors in about 12 min each, including model load. Qwen3-8B generated about 2.2M tokens.

Pipeline checks that passed:
- prompts render as intended, with the gpt-oss date pinned;
- reasoning closed vs forced is recorded;
- derived budgets copy or truncate correctly;
- graders run on every benchmark.

Problems found:
1. **Thinking is skipped in think mode.** Some instructions contain "with no explanation", and Qwen3 then often closes `<think>` immediately. Rate of empty traces: 8B gsm8k 65%, gsm_ic 60%, math500 18%; 1.7B nq_swap 90%, syco 30%. It then writes the explanation in the visible answer anyway.
2. **Visible reasoning in no-think mode** on math and inverse-scaling tasks. Median no-think answer length is 100–500 tokens; zebra hits the 1024 cap. Short-answer QA no-think answers are clean (3–6 tokens). The regex-based leak detector did not catch this, so a length / step-marker measure is needed.
3. **Answer caps too low** for open-ended tasks: falseqa/kuq/xstest answers truncated 40–100% (gpt-oss writes long markdown).
4. **Floor effects:** SimpleQA accuracy 0–7% and ist_zebra 0% for all models. These cannot produce flips.
5. The judge-graded benchmarks (abstention, safety) still need the judge models. AbstentionBench's validated judge (Llama-3.1-8B-Instruct) and the StrongREJECT fine-tuned judge (LoRA on gemma-2b) both sit behind gated HF licences, and no HF token is configured on newton.

Anecdotal signals (n=20, not tested): Qwen3-1.7B ist_misleading_math no-think 0.28 → think 0.00; Qwen3-8B triviaqa 0.47 → 0.35; Qwen3-8B ist_misleading_math budget 256: 0.875 vs natural 0.775.
