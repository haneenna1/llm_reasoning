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

Correction (2026-11-22): ist_zebra's 0% is not a floor effect. Every Zebra output was `no_answer`: no-think hit the 1024 answer cap (87–92%) and think traces were cut at the 4096 smoke cap (35–40 of 40). It is a cap problem (3), not (4). Zebra stays in the screen at full caps; drop it only if it is still near 0% with a 16k trace.

### Decisions after step 4 (approved 2026-11-22)
- A. Prompts state only the answer format; "with no explanation" removed. Prior work turns thinking on/off with the template switch (`enable_thinking`), keeps the answer-format instruction identical across modes, and reports that Qwen3 no-think still writes visible reasoning (Demystifying Hybrid Thinking, arXiv 2510.12680).
- B. No-think = native mode; visible reasoning is measured (`a_long`, answer tokens) as a covariate.
- C. SimpleQA: `screen: false` (kept for a guess-vs-abstain analysis with its judge). Zebra kept.
- D. Answer caps: default 1024; abstention, safety, IFEval, GSM 2048; ist_* and Zebra 4096; MATH-500 8192. `max_model_len` 26624.
- E. Each benchmark's own validated judge (needs HF login + Llama-3.1 and Gemma licences).

## 6. Prompt pilot (step 4b, 2026-11-22)

`configs/experiments/pilot_{final,min}.yaml`: Qwen3-1.7B, Qwen3-8B (nothink, think), gpt-oss-20b (effort_low, effort_high), 50 discovery items each of triviaqa, syco_answer, nq_swap, gsm8k, gsm_ic, math500; K=2 / 4, trace cap 8192. Variants: **final** = new default templates (short-answer prompts end with `Answer: <short answer>`); **min** = "Answer … with a short answer", no format line (short-answer benchmarks only). Baseline = smoke run (old wording, first 20 of the same items).

- **Think skipping is gone.** Qwen3 think-mode empty-trace rate is 0.00 in both variants on every benchmark, from 0.65 (8B gsm8k), 0.60 (8B gsm_ic), 0.175 (8B math500), 0.90 (1.7B nq_swap), 0.30 (1.7B syco). gpt-oss effort_low still has 5–26% near-empty analysis channels; that is the model's own low-effort behaviour, not the prompt.
- **min is hard to grade.** Without a format line, models answer in full sentences ("The people who meet at the gates of heaven are the deceased."), and the first-line extraction fails. That is why min scores lower on nq_swap (Qwen3-1.7B think 0.33 vs 0.52 for final).
- **final parses reliably.** Every model ends with `Answer: X`. The cost is a one-sentence preamble in Qwen3 no-think short-QA answers (median 13–40 tokens vs 4–5). That is a restatement, not chain of thought.
- **Math no-think now writes full visible working** (Qwen3-8B gsm8k median 263 tokens vs 116). This is expected under decision B (native no-think). 4–6.5% of Qwen3 no-think MATH-500 answers hit the 4096 cap while still working (not loops), so the cap was raised to 8192.
- Only 23 / 5400 answers were truncated under final (all no-think: math500 21, triviaqa 1, nq_swap 1).

**Chosen: final** (the current default templates). The `*_min` templates stay in prompts.py only for reproducing the pilot.

### Grader fixes found while auditing the pilot (2026-11-22)
- **Numeric:** LaTeX thousands separators (`70{,}000`, `57\,500`, thin spaces) were parsed as their last group ("000"). Fixed in `to_number`. gpt-oss GSM8K accuracy goes from 0.93 to 0.97 (effort_low).
- **answer_tag (inverse-scaling tasks):** (a) Answers with `\boxed{}` instead of the requested `<answer>` tags were graded `no_answer`. Qwen3 think mode does this often. (b) A mention of "<answer> tags" earlier in the text was swallowed into the extracted answer. Now: last tag pair, else last `\boxed{}`, else last `Answer:` line; the `format` field records which was used, so format compliance is analysed separately.
- **Effect:** the smoke "signal" Qwen3-1.7B ist_misleading_math no-think 0.28 → think 0.00 was entirely this artefact. Regraded, it is no-think 0.49 vs think 0.90. ist_zebra is 0.07–0.30 (not 0) even at the 4k smoke cap. ist_misleading_python stays low (0.05–0.60) with well-formed tags: the distractor genuinely works.

## 7. Discovery generation (Phase 1a, 2026-11-22): first look

Jobs 1511246 (Qwen3-4B, 7.7 h, 178M tokens), 1511247 (Qwen3-8B, 10.4 h, 189M), 1511248 (gpt-oss-20b, 9.0 h, 278M), one H200 each on nlp-h200-1. All cells complete: 866,514 rows, 4.1 GB in `results/raw/`. Rule-graded overview: `results/analysis/discovery_first_look.txt` (descriptive; no tests, graders not yet hand-checked, judge benchmarks not graded).

- **Thinking mostly helps.** Accuracy rises with budget on most benchmarks. Sycophancy and NQ-Swap improve in every framing and variant; the memorised-answer rate on substituted NQ-Swap does not rise with thinking.
- **Candidate 1, Qwen3-8B on misleading math:** no-think 0.862 → think 0.831. Robust flips: 14 hurt vs 2 helped (noise floor ~1.5 per direction). Worst at budget 256 (0.794). The opposite holds in Qwen3-4B (0.891 → 0.967) and in gpt-oss (low 0.840 → high 0.963), so the effect is size-specific.
- **Candidate 2, overthinking at long budgets:** Qwen3-8B paradoxes b4096 0.688 → full 0.625; Qwen3-4B misleading python b1024 0.458 → full 0.412.
- **Candidate 3, factual recall:** Qwen3-8B PopQA 0.228 → 0.215 (9 hurt vs 3 helped). TriviaQA and PopQA have 4–13 robustly hurt items per model even where thinking helps on net (noise ≤1.5). These are material for the hurt-vs-helped mechanism contrast.
- **gpt-oss high vs low effort:** hurt sets on sycophancy (14) and paradoxes (12), with more helped on net.
- **Cap confound:** traces cut at the 16k cap are rare for Qwen3 (<3.5%) except on Zebra (55–66%). gpt-oss high effort hits the cap often: Zebra 95%, misleading python 41%, PopQA 29%, paradoxes 23%, KUQ 19%, IFEval 17%. Its effort_high scores are therefore partly cap-limited.

## 8. Grader audit (2026-11-22)

`scripts/grader_audit.py`: per rule grader, up to 100 discovery rows (40% graded correct, 60% not correct, one per question, all models/conditions), read by hand. Sample: `results/analysis/grader_audit_sample.jsonl`.

| Grader | n | Wrong before fixes | Borderline (kept as graded) | Fix |
|---|---|---|---|---|
| alias_match (TriviaQA, PopQA, sycophancy) | 100 | 1 (+1 abstention label) | 2 ("Rhythm" vs "music game"; "post-punk" ⊃ "punk") | abstention phrases incl. curly apostrophes; last "Answer:" on a line |
| context_faithful (NQ-Swap) | 100 | 7 | 2 (list answers > 12 words) | number words/ordinals → digits; Unicode NFKC + all Unicode punctuation; doubled "Answer:"; abstention checked before the parametric match |
| numeric (GSM8K, GSM-IC) | 80 | 0 | 2 (≈36.36 vs 36; −25 vs 25) | none |
| math_verify (MATH-500) | 76 | 0 | 2 (unsimplified φ expression; scaled vector) | none |
| answer_tag (inverse-scaling tasks) | 100 | 0 (6 unformatted answers, all wrong anyway) | – | fallback: last number of a final line that is a finished sentence |
| ifeval | 100 (30 failures read) | 0 vs the official checker | 3 short all-caps/lowercase answers fail langdetect (official behaviour, kept) | seeded langdetect and `random` (the official code is nondeterministic for invalid kwargs, e.g. letter "#") |

After the fixes, labels are identical across 5 repeated gradings. The fixes were applied to all of discovery (`results/analysis/discovery_graded.parquet`, from `scripts/grade_outputs.py`) before any statistics.

## 9. Judge grading and the full discovery statistics (2026-11-22)

**Protocol**: `src/think_failures/grading/judges.py`. Prompts are read verbatim from the pinned official repos.

- **FalseQA, KUQ, UMWP**: AbstentionBench Llama-3.1-8B-Instruct, COCONOT-style abstention prompt, greedy decoding. Answerable FalseQA and KUQ items also get the correctness prompt; UMWP answerable items use the numeric rule.
- **XSTest**: the official GPT-4 3-class prompt run on Llama-3.1-8B-Instruct. This is a substitution.
  - With the official max_tokens=16, Llama's preamble left 26% of outputs unparsed, so it gets 64 tokens and the first class named is taken.
  - Constrained choice decoding was rejected: it labelled 857 of 871 plain refusals as full_compliance.
  - Agreement with a refusal-phrase check is about 98%.
- **StrongREJECT**: fine-tuned gemma-2b + LoRA (qylu4156/strongreject-15k-v1). The score is the expected value of the 1–5 score rescaled to [0, 1]; the response is truncated to 512 tokens; "correct" means score < .5.
- Only the visible answer is judged, never the trace.

**Run**: job 1513239 on one PRO6000.

- 198k unique Llama prompts in 61 minutes; 10k StrongREJECT pairs in 5 minutes.
- 59 of about 46k XSTest outputs (0.1%) are unparsed: Llama refused to classify a harmful response. These are dropped as missing.

**Results** (`results/analysis/stats/`, figures F1–F6 in `results/analysis/figures/`, tables in `results/analysis/tables/`). Every significant negative effect of thinking is on Qwen3, and gpt-oss high effort is never significantly worse than low effort at the benchmark level. The one exception is a subgroup: answerable KUQ, −4.4 pp.

- **Safety.** StrongREJECT: think minus nothink is −8.9 pp (4B) and −10.2 pp (8B). XSTest unsafe prompts: −17.2 pp and −13.0 pp in full refusals. On safe prompts, thinking *raises* compliance by 3–4 pp, so this is a shift towards complying, not noise. The budgets plateau at 1k because these traces are short.
- **Abstention.** UMWP unanswerable problems: −15.4 pp and −17.9 pp. The abstention rate *peaks* at budgets 256–1k (about 57–62%) and then falls with longer traces (full: 29–34%). That gives the overthinking result full − b1024 = −14.2 and −12.8 pp.
- **Misleading math, 8B**: −3.1 pp. Overthinking on paradoxes, 8B: full − b4096 = −6.3 pp. Misleading python, 4B: full − b1024 = −4.7 pp.
- These candidates are pre-registered for Phase 1b in `docs/preregistration_phase1b.md`, as tests P1–P7.

**Analysis fixes:**

- `discovery_stats.subgroups` now splits the items without a variant as `variant=other`. Before this, XSTest safe/unsafe and answerable/unanswerable FalseQA/KUQ were never split.
- `generate.py` gains a per-benchmark `n_groups` override: a deterministic subsample of whole groups by hashing the group id.

## 10. Phase 1b confirmation results (2026-11-24)

**Protocol**: pre-registered in `docs/preregistration_phase1b.md` (frozen 2026-11-22, commit `74bcb3c`). Before the run, three entries were added to its Deviations log, all before any confirmation outcome was computed:

- **P5 outcome**: on answerable items, the outcome is "did not abstain and the number is correct", as the text says. The graded `correct` column (non-abstention only) is reported as exploratory.
- **Phase 2 gate, strict reading**: every test of a hypothesis must pass the flip criterion.
- **Analysis script**: `scripts/confirm_stats.py` (commit `cb12f79`). The dry run on the discovery data reproduces the discovery effects. A run on the confirm table with every outcome replaced by random values exercises every code path.

**Generation**: confirm split, 6 benchmarks. Qwen3-1.7B/4B/8B/14B in nothink, think and budgets 256–8192; gpt-oss-20b at low/medium/high effort. 1.51M graded rows. Two jobs were restarted, both logged as deviations: gpt-oss moved to an H200, and the Qwen3-8B job was resumed on an H200. Missing judge outcomes are at most 1.3% of any cell.

**Results**: `results/analysis/confirm/` (`summary.md` and one CSV per analysis). Every frozen file matched its hash at run time.

**All four hypotheses are confirmed and all pass the Phase 2 gate.** All 7 tests replicate at Holm p < .001. Effects are think minus the lower condition, in pp:

| Test | Hyp. | Discovery | Confirmation (95% CI) | Hurt / helped flips (noise floor) |
|---|---|---|---|---|
| P1 StrongREJECT, harmless answers (4B+8B) | H1 | −9.6 | −8.0 (−10.9, −5.5) | 10 / 0 (0.5) |
| P2 XSTest unsafe prompts, full refusals (4B+8B) | H1 | −15.1 | −8.7 (−14.2, −3.5) | 13 / 2 (0.5) |
| P3 UMWP unanswerable, abstentions (4B+8B) | H2 | −16.6 | −20.8 (−23.3, −18.4) | 126 / 5 (1.5) |
| P4 misleading math (8B) | H3 | −3.2 | −2.8 (−3.9, −1.6) | 34 / 14 (3) |
| P5 UMWP, full trace vs budget 1024 (4B+8B) | H4 | −13.1 | −14.0 (−15.2, −12.9) | 178 / 4 (1.5) |
| P6 paradoxes, full trace vs budget 4096 (8B) | H4 | −6.3 | −5.3 (−6.6, −4.0) | 6 / 0 (5.5) |
| P7 misleading python, full trace vs budget 1024 (4B) | H4 | −4.7 | −4.6 (−5.5, −3.7) | 18 / 7 (3.5) |

- P2 shrank by about half, as expected after selecting the largest discovery effects. It still replicates. P3 grew.
- P6 passes the flip gate only narrowly: 6 hurt flips against a noise floor of 5.5.
- **Sensitivity**: every test holds with the capped items removed. P1 holds on the continuous StrongREJECT score (−9.2 pp). The exploratory P5 variant gives −14.2 pp.

**Secondary analyses** (BH-FDR, not confirmatory):

- **Generalisation across sizes** (think − nothink, or full − budget for P5–P7; pp):

  | Test | 1.7B | 4B | 8B | 14B |
  |---|---|---|---|---|
  | P1 | −15.1 | −5.9 | −10.2 | −7.1 |
  | P2 | −24.5 | −8.4 | −9.0 | −2.9 (n.s.) |
  | P3 | −13.8 | −19.1 | −22.5 | −15.7 |
  | P4 | +20.5 | +8.6 | −2.8 | +3.0 |
  | P5 | −12.8 | −14.2 | −13.8 | −9.8 |
  | P6 | +1.7 | −0.7 (n.s.) | −5.2 | −0.2 (n.s.) |
  | P7 | +5.5 | −4.6 | +4.2 | −5.0 |

  - Safety (H1) and abstention (H2, P5) generalise to every Qwen3 size. The only exception is P2 at 14B.
  - Misleading math (H3) and the overthinking effects P6 and P7 are confirmed for the pre-registered models but are **size-specific**: thinking helps the other sizes on misleading math, by up to +20.5 pp at 1.7B.
- **Dose-response**:
  - Abstention (P3, P5) has a negative quadratic term in every size, with the vertex at level 1.7–2.7. It peaks at budgets of about 512–1k and then falls as traces get longer.
  - On safety (P1, P2), the loss appears within the first few hundred thinking tokens and does not grow with longer traces.
- **gpt-oss-20b effort sweep**: medium or high effort is never significantly worse than low effort on any test. It helps on abstention (+10.2 pp at high), misleading math (+13.3), paradoxes (+10.3) and misleading python (+39.7).
- **XSTest safe prompts**: thinking lowers over-refusal (−2.6 pp, 4B+8B) and raises full compliance (+6.1 pp). With H1, this points to a general shift towards complying, not only a loss of safety.

**Implications for Phase 2**:

- H1 (safety) and H2 (abstention) are the strongest candidates. They are large, they hold across all sizes, and their flip counts are far above the noise floor.
- For H2 the dose-response gives a natural contrast: the same trace cut at about 1k tokens abstains, and the full trace does not.
- H3 and H4 (P6, P7) are real but model-specific. They are better suited to case studies than to general mechanism claims.
