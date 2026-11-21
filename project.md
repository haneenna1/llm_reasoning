# Project: When thinking hurts — finding, explaining and preventing reasoning-induced failures

Branch: `think-failure-modes`. The previous scope (factual recall across post-training variants of one base model) is preserved on `main`.

## Context (research idea)
Test-time reasoning ("thinking") improves LLMs on average, especially on math and code, but there is growing evidence that it can make a model *worse* on specific behaviours. Examples include closed-book factual QA, instruction following, abstention on unanswerable questions, distractor-laden problems and intuitive/implicit tasks. Sometimes more thinking even makes things worse (inverse scaling in test-time compute). Each of these findings comes from a different paper, model set and protocol. Most compare different models instead of the same weights with thinking on or off, and few go beyond behaviour to mechanism.

Prior work to verify and extend (cited from memory, so check in Phase 0):
- Yao et al. 2025, "Are Reasoning Models More Prone to Hallucination?" (arXiv 2505.23646)
- arXiv 2607.05861: thinking flips correct TriviaQA answers in Qwen3 (~5–7.5%)
- Gema et al. 2025, "Inverse Scaling in Test-Time Compute"
- Li et al. 2025, "When Thinking Fails: The Pitfalls of Reasoning for Instruction-Following"
- Liu et al. 2024, "Mind Your Step (by Step): CoT can reduce performance on tasks where thinking makes humans worse"
- Kirichenko et al. 2025, AbstentionBench
- Ma et al. 2025, "Reasoning Models Can Be Effective Without Thinking" (NoThinking)
- Muennighoff et al. 2025, s1 (budget forcing)
- Bogdan et al. 2025, "Thought Anchors"
- Sprague et al. 2024, "To CoT or not to CoT"

**Main question.** Are there task types where thinking, or more thinking, makes a model reliably worse than not thinking, or thinking less, *on the same question with the same weights*? If so, what happens inside the model that turns a correct no-think answer into a wrong answer after thinking?

**Main design choice.** The core models are **hybrid models where the same weights run with thinking on or off and at controllable effort**. Any think-vs-no-think difference then comes from the generated trace alone, not from a weight difference. This makes the mechanistic phase clean, because patching between modes compares like with like. Post-training-variant comparisons (OLMo, MiMo) serve as cross-lab replication.

**Novelty claim (to confirm in Phase 0):** a cross-task, same-weights, dose–response study of thinking-induced failures, followed by a causal mechanistic explanation and (as an extension) an intervention.

## Phases and scope
1. **Behavioural discovery.** Screen many benchmarks and keep only failure modes that are statistically significant, replicate across model families, and are not artifacts of grading or truncation.
2. **Mechanistic explanation.** For 1–2 confirmed failure modes, find where and how the trace overrides an answer the model had right, contrasted with matched cases where thinking helped.
3. **Intervention** (thesis extension, after the submission). Prevent the failures with a test-time monitor and/or finetuning, without losing the gains thinking gives elsewhere.

**Deadline:** Phases 0–2 plus write-up must be finished by **2027-02-28**. Phase 3 is not required for that submission. See the timeline at the end.

## Compute
Cluster `newton` (see `docs/step1_findings.md`). bf16 GPU nodes (A100, A40, L40, RTX 6000 Ada, H200, RTX PRO 6000). Accounts `nlp` (preferred) then `cs`/`public` (≤4 GPUs, preemptible). Jobs are submitted through `scripts/submit_generate.sh`. Long jobs run detached.

## Models
Verify every model ID, chat template and think-control method in Phase 0. Do not assume template details. If newer hybrid releases exist, consider them, but keep one fixed core set for the whole study.

| Role | Models | Think control |
|---|---|---|
| **Core: same weights, size sweep** | Qwen3 hybrid: 1.7B, 4B, 8B (14B if compute allows) | native `enable_thinking` on/off; budget forcing for effort levels |
| **Core: native effort levels** | gpt-oss-20b | `reasoning_effort` low / medium / high (harmony format) |
| Replication (different lab, open data) | OLMo 3 7B: Think vs Instruct (same base) | prefill `</think>` after the template's forced `<think>` |
| Replication (existing infra) | MiMo-7B-RL (optionally MiMo-7B-SFT) | prefill an empty `<think>\n\n</think>\n\n` |

For the prefill-based models, check empirically that no-think outputs contain no reasoning, and document the method per model.

## Thinking conditions (dose–response)
- **no-think**
- **budget-forced** thinking at 256 / 1,024 / 4,096 tokens: truncate the trace at the budget, close it with `</think>`, and let the model answer
- **natural** thinking, capped at 16,384 tokens
- *(optional)* **extended** thinking: suppress `</think>` once or twice and append "Wait" (s1-style)
- gpt-oss: low / medium / high effort, in place of or in addition to the budgets

Record trace length and truncation for every sample.

## Benchmarks
Grouped by the failure mechanism we expect. Each benchmark gets a fixed **discovery** split and a disjoint **confirmation** split (fixed seed, saved question IDs).

| Category | Benchmarks (candidates) | Hypothesis |
|---|---|---|
| Factual recall | TriviaQA (closed-book), PopQA (stratified by popularity; already sampled), SimpleQA | thinking talks the model out of a fact it knew, or confabulates |
| Abstention / false premise | AbstentionBench subsets, missing-premise GSM8K, FalseQA | thinking suppresses "I don't know" / accepts a false premise |
| Instruction following | IFEval, ComplexBench | constraints get dropped during reasoning |
| Distractors / spurious features | GSM-IC, inverse-scaling test-time-compute tasks (Gema et al.) | longer thinking amplifies irrelevant information |
| Sycophancy | answer-suggestion bias, "are you sure?" flip prompts | thinking rationalises the user's suggestion |
| Context faithfulness | knowledge-conflict QA (NQ-Swap-style) | thinking overrides the given context with memorised knowledge |
| Intuitive / implicit tasks | "Mind Your Step"-style tasks | verbal overshadowing |
| Over-refusal / safety | XSTest (over-refusal), StrongREJECT (harmful compliance) | thinking shifts refusal behaviour |
| **Positive control** | GSM8K (already sampled), MATH | thinking should help here; checks the pipeline |

Phase 0 may add benchmarks found in the literature survey. Any change to the list after the screen has started needs approval.

## Generation
- vLLM, bf16, resumable, with seeds derived per request from (seed, qid) as in `main`.
- **Discovery screen:** K=8 samples per question for every think condition, and **K=16 for no-think** (cheap; split into two K=8 halves to measure the noise floor). Use each model's recommended sampling (Qwen3 thinking: temperature 0.6, top-p 0.95; no-think: the model card's settings), plus one greedy run.
- Save full raw outputs, including traces, keyed by (model, mode, budget, benchmark, qid, sample_id).
- Keep prompts, question IDs and answer extraction identical across models and conditions, except for the think-control mechanism itself.

## Grading
Each benchmark has its own grader:
- **Factual QA:** SQuAD-normalised exact match / containment over all aliases, plus a "not attempted" label.
- **Math:** numeric match.
- **IFEval:** the official checker.
- **Abstention, sycophancy, safety and open-ended items:** an open-weight LLM judge with a documented prompt.
- Extract the final answer only from after the reasoning block. Log extraction failures separately; never count them as wrong answers.
- Hand-check 100 gradings per grader type. If agreement is below 95%, fix the grader or add an LLM-judge pass.

## Statistics
- **Unit of analysis:** the question. All comparisons are paired, using per-question accuracy p = (#correct)/K.
- **Net effect:** Δ = acc(think) − acc(no-think), with a paired bootstrap 95% CI over questions and a paired permutation-test p-value.
- **Flips:**
  - A *robust flip* is ≥6/8 correct in one condition and ≤2/8 in the other. Count both directions: think-induced failures (no-think correct → think wrong) and think-induced successes.
  - **Noise floor:** the robust-flip rate between the two K=8 halves of no-think. A failure mode needs a think-induced failure rate significantly above this floor, which can happen even when net Δ > 0.
- **Dose–response:** mixed-effects logistic regression, correct ~ log(budget) + (1 | question), per model × benchmark. A significant negative slope means inverse scaling.
- **Confounds:** report every effect with and without truncated samples and extraction failures.
- **Multiple testing:** Benjamini–Hochberg FDR (q = 0.05) across all (model, benchmark, contrast) tests in discovery.
- **Confirmation:** top candidates are **pre-registered** (hypothesis, contrast, direction, required N from a power calculation on discovery effect sizes) and re-tested on the held-out confirmation split.
- **Predictors of harm** (exploratory): no-think answer confidence (log-prob), question difficulty / entity popularity, trace length, whether the correct answer appears in the trace and is later abandoned.

## Failure-mode characterisation
For each candidate, compute automatic trace features for all flips:
- whether the correct answer was mentioned and then abandoned
- position of the first answer mention
- number of backtracks ("wait", "alternatively")
- trace length
- whether a constraint is mentioned in the trace

Also export 50 flips per candidate to a readable file for manual labelling with a taxonomy. Starting labels (refine after labelling):
- never retrieved / reasoned
- talked out of the correct answer
- constraint dropped
- distracted by irrelevant information
- over-complicated a simple question
- rationalised the user's suggestion
- refused to abstain / invented a premise
- answer-format drift
- truncation

## Gate 1 (behavioural go/no-go, needs approval)
A failure mode is "research-interesting" if it:
1. survives FDR on discovery **and** replicates on the confirmation split;
2. appears in at least 2 model families (e.g. Qwen3 and gpt-oss, or Qwen3 and OLMo);
3. is not explained by grading, extraction or truncation;
4. yields at least ~200 robust think-induced failures **and** ~200 matched think-induced successes on one interpretable model (4–8B), for Phase 2.

Report every candidate against these criteria in `RESULTS_behavioural.md`. If nothing passes, report the strongest effects and the closest misses, and we decide together.

## Phase 2: mechanistic explanation
On the model where the confirmed effect is strongest and smallest:
1. **Locate the flip.** Force an answer at intermediate trace prefixes (early answering) and apply the logit lens / tuned lens to the answer tokens along the trace, to find when the correct answer's probability collapses.
2. **Latent knowledge.** Train linear probes for answer identity and correctness at the no-think answer position vs the post-trace answer position. Does the model still represent the right answer after thinking?
3. **Causal tests:**
   - activation patching between the no-think and think runs at the answer position (layers, then heads);
   - attribution from the answer to trace sentences, with counterfactual sentence resampling (Thought-Anchors style);
   - SAE/transcoder features if public ones exist for the model;
   - steering vectors (e.g. self-doubt / backtracking directions).
4. **Failures vs successes.** Which of the mechanisms above separates think-induced failures from matched think-induced successes?
5. *(Optional, ties back to `main`)*: model diffing between OLMo Think and Instruct for the same failure mode.

Gate 2: a written mechanistic account backed by at least one causal (not only correlational) result.

## Phase 3: intervention (extension after the 2027-02-28 submission)
- **Test-time monitors:**
  - a probe on the prompt's hidden states that predicts "thinking will hurt" and routes the question to no-think or a low budget;
  - an in-trace flip detector that early-exits and commits to the earlier answer;
  - activation steering.

  Baselines: always-think, never-think, prompted self-selection, and an oracle router.
- **Finetuning:** LoRA DPO on (no-think-correct, think-wrong) pairs, or mode-selection training.
- **Evaluation** on held-out benchmarks: failures prevented, and thinking's gains on the positive controls kept.

## Engineering requirements
- Rename the package `reasoning_recall` → **`think_failures`** (`src/think_failures`, `pyproject.toml`, imports, env name references).
- **Configs:**
  - `configs/benchmarks.yaml` registry: loader, prompt template, grader, task category, discovery/confirm split sizes;
  - `configs/models.yaml` with a per-model **think-control** spec (native flag / effort / prefill / budget forcing) and stop tokens;
  - `configs/runs/` generated from model × mode × budget × benchmark.
- **Modules:** `src/think_failures/{data, prompts, think_control, generate, grading/, stats, traces, analysis}`.
- Reuse from `main`: resumable vLLM generation, SLURM wrappers and GPU selection, the sampled TriviaQA/PopQA/GSM8K question sets.
- One command reruns everything from config. Fix seeds and log package versions and model revisions.
- Store hidden-state dumps for Phase 2 separately from raw generations, keyed the same way.
- Update the `.claude/agents` guides to the new scope after the refactor.

## Order of work and timeline (today: 2026-11-21)
| Dates | Step |
|---|---|
| **Phase 0** — Nov 21 → Nov 30 | 1. Literature survey: confirm novelty, verify citations, finalise benchmarks. 2. Verify models, templates, think-control methods, vLLM support on newton; **report to me**. 3. Refactor + rename to `think_failures`; benchmark registry; graders. |
| **Phase 1a** — Dec 1 → Dec 21 | 4. Smoke test: 50 questions × all benchmarks × one small Qwen3 model; hand-check graders; **show me samples**. 5. Discovery screen: Qwen3-4B/8B + gpt-oss-20b, no-think vs natural think (+ K=16 no-think). 6. Stats + ranked candidate table. 7. Flip characterisation. |
| **Phase 1b** — Dec 22 → Jan 10 (holiday buffer) | 8. Pre-register top 2–4 candidates; confirmation split; full budget sweep; all sizes; OLMo/MiMo replication. 9. `RESULTS_behavioural.md` → **Gate 1 (approval)**. |
| **Phase 2** — Jan 11 → Feb 14 | 10–14. Mechanistic analysis on 1–2 confirmed failure modes → **Gate 2**. |
| **Write-up** — Feb 15 → Feb 28 | Thesis/report draft for Phases 0–2. |
| **Phase 3** — Mar 2027 → | Intervention as the thesis extension. |

The schedule is tight. If Phase 1a slips, cut scope in this order: drop the 14B model, drop extended thinking, then drop the lowest-priority benchmarks (ranked by discovery effect size). Phase 2 time is protected.

Ask me before any decision that changes the experimental design. Report back after step 2, step 4 and each gate.
