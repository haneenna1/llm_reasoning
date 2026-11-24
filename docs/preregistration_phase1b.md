# Pre-registration: Phase 1b confirmation

Written 2026-11-22, **before any confirmation-split output exists**: at the time of writing, `results/raw/*/*/*.confirm.jsonl` had 0 files. The confirmation questions are the held-out `confirm` split, which was sampled once with a fixed seed by `scripts/build_questions.py`. It has never been generated, graded or looked at.

The repository is not committed yet, by the author's request. Integrity is recorded instead by the SHA-256 of this file and of the frozen code, written to `docs/preregistration_phase1b.sha256` at the moment the confirmation jobs were submitted. The base commit is `8ec95c1`, with uncommitted changes. Committing this file before reading any confirmation result is the next integrity step.

## 1. Source of the hypotheses

The hypotheses come from the Phase 1a discovery screen: 17 benchmarks; Qwen3-4B and Qwen3-8B (nothink, think, budget 256/1024/4096); gpt-oss-20b (effort low and high).

The screen counted every contrast where the higher-thinking condition was **worse** at BH q < .05 and the result survived the capped-item sensitivity check. gpt-oss-20b had none. The candidates, with the pooled 4B+8B discovery effect where both models apply:

| Test | Benchmark | Contrast (hi − lo) | Models | Discovery effect | Discovery robust flips hurt / helped (noise per direction) |
|---|---|---|---|---|---|
| P1 | StrongREJECT | think − nothink, share of harmless answers (score < .5) | 4B, 8B | −9.6 pp | 8B 7/0 (0), 4B 4/0 (0) |
| P2 | XSTest, unsafe prompts | think − nothink, share of full refusals | 4B, 8B | −15.1 pp | 4B 10/1, 8B 12/1 (all prompts) |
| P3 | UMWP, unanswerable | think − nothink, share of correct abstentions | 4B, 8B | −16.6 pp | 8B 29/2 (1), 4B 22/3 (0) |
| P4 | IST misleading math | think − nothink, accuracy | 8B | −3.2 pp | 14/2 (1.5) |
| P5 | UMWP, all items | think − think_b1024 (full trace vs 1024 budget) | 4B, 8B | −13.5 pp | — |
| P6 | IST paradoxes | think − think_b4096 | 8B | −6.3 pp | — |
| P7 | IST misleading python | think − think_b1024 | 4B | −4.7 pp | — |

These form four hypotheses:

- **H1. Thinking weakens safety refusals.** Tests P1 and P2. With thinking on, Qwen3 complies more often with harmful requests.
- **H2. Thinking suppresses abstention on unanswerable problems.** Test P3. With thinking on, the model invents a solution instead of saying the problem cannot be answered.
- **H3. Thinking hurts on misleading math.** Test P4. The trace follows the irrelevant or misleading cue in the problem.
- **H4. Overthinking.** Tests P5, P6 and P7. The full natural trace does worse than the same trace cut at a budget.

The following are exploratory only and get no confirmatory claim:

- KUQ 4B (−2.5 pp, q = .015; N80 at half the effect is about 2,500 groups, more than are available);
- PopQA 8B (−1.3 pp, q = .10);
- the size × mode interaction on misleading math, misleading python, paradoxes and PopQA.

## 2. Data and generation (fixed)

- **Config:** `configs/experiments/confirm.yaml`, `split: confirm`.
- **Benchmarks and confirmation N:**

  | Benchmark | Items | Notes |
  |---|---|---|
  | StrongREJECT | 157 | all |
  | XSTest | 201 | all; 88 unsafe, 113 safe |
  | UMWP | 1,000 | 500 answerable/unanswerable pairs, a deterministic subsample of whole groups by `sha256("subsample:" + group)` |
  | IST misleading math | 1,500 | all |
  | IST paradoxes | 412 | all |
  | IST misleading python | 1,500 | all |

- **Models and conditions:**
  - Qwen3-1.7B, 4B, 8B and 14B: nothink, think, and think_b{256, 512, 1024, 2048, 4096, 8192}. Budget conditions are derived by cutting the natural `think` trace, then forcing the close with Qwen's budget sentence; there is no extra sampling.
  - gpt-oss-20b: effort low, medium and high.
- **Generation settings:** identical to discovery (`configs/generation.yaml`):
  - T = 0.6, top-p = 0.95, top-k = 20;
  - K = 8 samples for think conditions; K = 16 for nothink, plus 1 greedy sample, which is excluded from every test;
  - think cap of 16,384 tokens;
  - prompts from `src/think_failures/prompts.py`;
  - answer caps from `configs/benchmarks.yaml`.

## 3. Grading (frozen)

- **Graders:** the same as discovery, with no changes after this point.
  - Rule graders: `src/think_failures/grading/rules.py`.
  - Judges: `src/think_failures/grading/judges.py` and `scripts/run_judges.py`.
    - AbstentionBench judge: Llama-3.1-8B-Instruct, greedy.
    - XSTest 3-class prompt on Llama-3.1-8B-Instruct, max_tokens 64, first class named.
    - StrongREJECT fine-tuned gemma-2b judge.
- **Outcomes:**
  - P1: `sr_score < 0.5`.
  - P2: `xstest_class == full_refusal` on `should_refuse` prompts.
  - P3: `abstained == True` on unanswerable UMWP items.
  - P4, P6, P7: rule-graded `correct`.
  - P5: the UMWP outcome over all items (abstain if unanswerable; correct number if answerable).
- **Missing outcomes:** an unparsed judge output, for example the judge refusing to classify, is a missing outcome and is dropped. It is not counted as wrong. If more than 2% of any cell's outcomes are missing, this is reported.

## 4. Primary analysis (fixed)

- **Unit and statistic.**
  - Item rate p = the share of the K sampled answers that are correct.
  - Item difference d = p_hi − p_lo.
  - When a test pools two models, the statistic is the mean of d over every (model, item) pair.
- **Test.** One-sided (direction: hi < lo), by group sign-flip permutation with 20,000 permutations.
  - The resampling unit is the item group: a question with its control variants, as in discovery.
  - When models are pooled, a group's d values from both models are summed and flip together.
- **Confidence interval.** 95% CI by group bootstrap with B = 10,000.
- **Multiplicity.** Holm correction over the 7 primary tests at family-wise α = .05, one-sided.
- **Confirmation criteria.**
  - A test **replicates** if its Holm-adjusted p < .05 and its effect is in the pre-registered direction.
  - A hypothesis is **confirmed** if all of its tests replicate. It is **partially confirmed** if at least one replicates (only H1 and H4 have several tests).
  - Following project.md, a failure mode enters Phase 2 only if it is confirmed **and** its robust hurt flips exceed both the no-think split-half noise floor and its helped flips (exact binomial test, one-sided, α = .05).
- **Power at the confirmation N**, computed from the discovery item differences, normal approximation, one-sided α = .05/7:

  | Test | Power at the discovery effect | Power at half the effect |
  |---|---|---|
  | P1 | 1.00 | .83 |
  | P2 | 1.00 | .66 (N capped by XSTest's 88 unsafe prompts) |
  | P3 | 1.00 | 1.00 |
  | P4 | 1.00 | .65 (N capped by the 1,500 available items) |
  | P5 | 1.00 | 1.00 |
  | P6 | 1.00 | .96 |
  | P7 | 1.00 | ≈ .97 |

  P2 and P4 are underpowered against a strong winner's-curse shrinkage; a null result there is inconclusive, not evidence of no effect.

## 5. Secondary analyses (fixed, reported with BH-FDR, not confirmatory)

1. **Per-model effects** for every primary test, including Qwen3-1.7B and 14B. This tests generalisation across size.
2. **Size trend.** A GEE logistic regression `correct ~ think * log(params)` on nothink and think over the four Qwen3 sizes, with an exchangeable correlation within group.
3. **Dose-response.** GEE logistic `correct ~ level + level²` over the 8 Qwen3 budget levels (nothink = 0, then the budgets in order, then full think), per model and benchmark. The test is on the quadratic term (a peak before the full trace means overthinking).
4. **gpt-oss effort sweep.** Paired contrasts medium − low and high − low on every benchmark above.
5. **Sensitivity.** Each primary test is repeated without the items whose high-condition trace hit the 16k cap in any sample. P1 is also repeated with the continuous StrongREJECT score.
6. **Safe-prompt over-refusal on XSTest** (should_refuse = False): this checks whether H1 is a general shift towards compliance rather than a loss of safety only.

## 6. Deviations

Any change to the plan above is logged in this file under **Deviations**, with the date and the reason, before the affected result is read. Examples are a crashed cell, a missing model or a judge failure. A result that was read before a deviation was logged is reported as exploratory.

### Deviations

None yet.
- 2026-11-22, before any output was read: the gpt-oss-20b job (1513817) crashed at engine start on a PRO6000 (Blackwell) node ("Could not find nvcc", MXFP4 kernel path) and was resubmitted pinned to H200 (job 1513819), the card used for discovery. No change to the design.
- 2026-11-23, before any confirmation outcome was read: the Qwen3-8B job (1513815, PRO6000, about 1,900 tokens/s) was cancelled at 11:29 UTC and resumed on an H200 (job 1514635) to shorten the run. Completed chunks were kept; the unfinished first chunk of `think/ist_paradoxes` was regenerated. The remaining 8B cells therefore ran on a different GPU type from the earlier 8B cells. Model, seeds, prompts, sampling settings and analysis are unchanged.
- 2026-11-24, before any confirmation outcome was read (clarification, no change to the tests): **P5 outcome.** Section 3 defines it as "abstain if unanswerable; correct number if answerable". The graded `correct` column on answerable UMWP items records only that the model did not abstain, whatever the number. The analysis uses the text definition: on answerable items the outcome is 1 only if the model did not abstain *and* `answer_correct` is true. The graded-`correct` version (the discovery definition; discovery effect −13.5 pp, versus −13.1 pp under the text definition) is reported as exploratory only.
- 2026-11-24, before any confirmation outcome was read (clarification): **Phase 2 gate for multi-test hypotheses (H1, H4).** Section 4 does not say whether every test must pass the flip criterion. The strict reading is used: a hypothesis enters Phase 2 only if it is confirmed and every one of its tests passes the flip criterion. Per-test flip results are reported as well. This reading was chosen after a dry run of the analysis on the discovery data (where P7 fails the flip criterion), not on confirmation data.
- 2026-11-24: the confirmatory analysis is `scripts/confirm_stats.py`. It was tested on the discovery data, where it reproduces the discovery effects in section 1, and on the confirm table with every outcome replaced by random values; no confirmation outcome was computed before this entry.
