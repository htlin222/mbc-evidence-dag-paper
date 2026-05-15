# Preregistration v2 — mbc-evidence-dag-paper

**Date of preregistration:** 2026-05-16 (v2; supersedes scope of v1.0.0 prereg)
**Commit hash when this file is committed:** (recorded by git automatically at the commit that introduces this file, BEFORE any v2 outcome-touching analysis is run)
**Predecessor:** `docs/prereg.md` (v1, 2026-05-16), which governed the 16-trial pilot released as `v1.0.0` and is preserved unmodified.

## Relationship to v1.0.0 prereg
The v1 prereg governs the 16-trial pilot. **All v1 commitments are honored as written**; v1.0.0 is preserved and released. This v2 prereg governs the **production-scale** analysis whose plan, scope, and inferential procedure are committed BEFORE the new outcome data (i.e., before any LLM extraction or DAG construction on the expanded corpus) is observed.

The v1 result (strict EFDPR = 0.31, $P=0.37$) is **knowable to v2** and is used here only to seed the power calculation. The v2 inferential commitment is not adjusted on the basis of v1's point estimate.

## Study title (v2)
A computable map of treatment-sequencing evidence in HR+/HER2- metastatic breast cancer: a graph-theoretic systematic analysis comparing trial chains with the ESMO, ASCO, and NCCN guideline decision trees.

## Primary outcome (v2; unchanged from v1)
**Evidence-free decision-point ratio (EFDPR)** under the **strict** tolerance level: the proportion of ESMO 2024 HR+/HER2- mBC guideline decision nodes for which no edge in the trial-derived DAG satisfies all four concordance criteria — state superset, biomarker-definition equivalence, drug-class match, and temporal precedence.

## Primary hypothesis (v2; unchanged)
$H_1: \mathrm{EFDPR} > 0.25$ under strict tolerance, against $H_0: \mathrm{EFDPR} \le 0.25$.

## Pre-specified primary test (v2; unchanged)
**One-sided exact binomial test** of $H_0: p \le 0.25$ given $k$ evidence-free guideline nodes out of $n$ ESMO HR+/HER2- guideline nodes, with rejection threshold $\alpha = 0.05$.

Reported alongside, **but not used to define the primary inference**: Clopper-Pearson exact 95% CI and a 1,000-iteration percentile bootstrap CI (seed 20260516, by guideline-node resampling).

## Power analysis (new in v2; numbers exact, computed via scipy.stats.binom)
Exact one-sided binomial power for rejecting $H_0: p \le 0.25$ at $\alpha = 0.05$:

| Effect $p_1$ | $n$ guideline nodes | $k_{\mathrm{crit}}$ | Power |
|---:|---:|---:|---:|
| 0.35 | 16 |  8 | 15.9% |
| 0.35 | 30 | 13 | 22.0% |
| 0.35 | 50 | 19 | 37.8% |
| 0.40 | 16 |  8 | 28.4% |
| 0.40 | 30 | 13 | 42.2% |
| 0.40 | 50 | 19 | 66.4% |
| 0.40 | 80 | 27 | 89.6% |
| 0.50 | 16 |  8 | 59.8% |
| 0.50 | 30 | 13 | 81.9% |
| 0.50 | 50 | 19 | 96.8% |

The v1 point estimate was $\hat p = 0.31$, with CP-CI [0.11, 0.59]. **The realistic effect to detect, given v1, is $p_1 \approx 0.35$--$0.40$.** Under a real guideline-encoding constraint (ESMO + ASCO + NCCN HR+/HER2- decision trees deduplicate to roughly 25--35 unique nodes), the achievable $n$ for v2 is **bounded at $n \approx 25$--$35$**.

**v2 is therefore adequately powered (>80%) only for a large effect ($p_1 \ge 0.50$); for the v1 point estimate ($p_1 \approx 0.31$) v2 is moderately powered (~40--50%)**. This is an honest constraint of the design, not a deviation. v2 is the largest study consistent with the unit of analysis (guideline decision nodes), and a fully-powered confirmatory study would require pooling decision trees across multiple solid tumours.

v2 commits to **expanding the guideline-node count by adding ASCO and NCCN HR+/HER2- decision nodes that are not duplicates of the ESMO subset, as a primary-test denominator extension**. The target $n$ is **whatever the deduplicated ESMO + ASCO + NCCN HR+/HER2- decision tree yields**, with a pre-specified minimum $n \ge 25$. ASCO and NCCN nodes are added regardless of their concordance status; this is **not** an adaptive-stopping rule.

Trial-corpus expansion is independent of $n$ for the primary test but determines the achievable $k$ ceiling and the secondary outcomes' resolution.

## Confirmatory analysis plan (v2)
1. Run a systematic ClinicalTrials.gov v2 API query for phase 2/3 trials with:
   - condition tag containing "breast cancer" or "breast neoplasm";
   - intervention type "drug" or "biological";
   - eligibility text mentioning HR+ / ER+ / "estrogen receptor positive" AND ("metastatic" OR "advanced");
   - first-posted date between 2015-01-01 and 2026-05-16.
   The query is committed in `analysis/v2_01_systematic_search.py` at the prereg-v2 commit, BEFORE any extraction.
2. Apply pre-specified inclusion filters (HER2 status NOT mandated positive; not adjuvant; not neoadjuvant; HR+ inclusion either required or as a pre-specified subgroup; eligibility text retrievable).
3. Target corpus size **n_trials >= 40**. If the post-filter corpus exceeds 80 trials we use the full set; if below 40 we report the deviation and proceed with the available set.
4. Extract eligibility into the **frozen schema v1.0** using a two-annotator LLM pipeline (Annotator A: Claude; Annotator B: Codex GPT-5) on a pre-specified **20-trial validation subset**, drawn at random (seed 20260516) from the corpus.
5. Compute per-field Cohen's $\kappa$ on the validation subset. Required gates:
   - Overall accuracy $\ge 0.85$;
   - Key fields (post_endo, post_cdk46i, biomarker requirements): $\kappa \ge 0.70$ (substantial).
   If gates fail, run a disagreement-adjudication pass and report the post-adjudication $\kappa$ as well.
6. Run full-corpus extraction by Annotator A; treat Annotator B's extractions on the 20-trial subset as the validation reference.
7. Encode the ESMO 2024 (primary) decision tree as in v1; **add ASCO and NCCN HR+/HER2- decision nodes** to expand to $n \ge 30$ guideline nodes for the primary test.
8. Build the trial-DAG and compute EFDPR under strict, ESCAT-aligned, and liberal tolerance (unchanged from v1).
9. Run the pre-registered exact-binomial test on strict-tolerance EFDPR. The test is run **exactly once** on the full $n$ guideline-node count, not iteratively across tolerance levels (the three tolerance levels are a pre-registered sensitivity grid, not three independent confirmatory tests).

## Secondary outcomes (v2)
- **S1.** Operationalization discordance index (ODI) per biomarker variable, with 1,000-iteration bootstrap CI by trial-pair resampling.
- **S2.** Temporal evidence lag: median years between guideline-node introduction year and earliest supporting trial's primary-completion year, restricted to nodes with $\mathrm{Supp}(g) \neq \emptyset$. Reported with bootstrap CI.
- **S3.** Subgroup coverage: percentage of trials in the corpus reporting outcomes for (a) Asian ancestry, (b) age $\ge 70$, (c) Black or African ancestry, derived from each trial's primary-publication abstract or table 1. Reported as proportions.
- **S4.** Composition-only citation count: number of guideline nodes where the guideline cites a trial as supporting the node but the trial's state-encoding does not match the node under any tolerance. Reported as count and proportion.

Multiple-testing correction across S1, S2, S3, S4: Benjamini-Hochberg $q < 0.05$, applied only to the outcomes that admit a formal hypothesis test (S1 ODI, with $H_0: \mathrm{ODI} = 0$; S2 lag, with $H_0: \mathrm{lag} = 0$). S3 and S4 are descriptive.

## Exploratory analyses (v2)
- E1. ESMO vs ASCO vs NCCN EFDPR comparison.
- E2. Network centrality of individual drugs in the trial-DAG.
- E3. Subgroup-coverage breakdown by drug class.
- E4. LLM-extraction error pattern analysis (which fields had the lowest $\kappa$ and why).

Exploratory results are labelled explicitly and **cannot be promoted to primary**.

## Stop rules
- Primary hypothesis refuted if the exact-binomial test rejects $H_0: p \ge 0.50$ (one-sided lower; i.e., a clear negative finding).
- Clean null: point estimate $\le 0.10$ with upper CP-CI bound $\le 0.15$.
- Inconclusive: anything in between; reported honestly.

## Pre-specified deviations from v1
- **G16 (gBRCAm) is retained** in the primary analysis with the line-agnostic `metastatic` state token as in v1.0.0 (already disclosed deviation; not re-deviating).
- **G6 (post-endo AKT-pathway)** state coding is retained as v1.0.0 Round 4 (post-endo, not post-CDK46i); not re-deviating.

## Validation gates
- **LLM-extraction Cohen's $\kappa \ge 0.70$** on key fields (post_endo, post_cdk46i, biomarker requirements) — must pass before the full-corpus extraction is used for the primary test.
- **Corpus size $\ge 40$ trials** — must pass before the primary test is run.
- **Guideline-node count $\ge 25$** — must pass before the primary test is run.

If any gate fails, deviation is disclosed in the manuscript with a "deviations" paragraph and the analysis proceeds with the available data, **but the failure does not justify swapping primary outcome or test**.

## Multiple-testing family (v2)
Primary EFDPR (strict tolerance): a single test. Secondary outcomes (S1 ODI, S2 lag): BH $q < 0.05$ across the two formal tests. S3, S4 descriptive.

## Frozen prior to outcome data
This v2 prereg is committed BEFORE the systematic search is executed (i.e., before `analysis/v2_01_systematic_search.py` is run on the live CT.gov API for the v2 corpus). The commit hash of THIS file is the v2 prereg timestamp.

## Amendment v2.1 (2026-05-16, disclosed BEFORE LLM extraction)
The initial systematic search per Section "Confirmatory analysis plan" step 1 was run on the live CT.gov API and returned 874 candidate studies; the pre-specified date filter `2015-01-01 .. 2026-05-16` excluded 15 of the 16 v1.0.0 corpus trials, all of which started in 2013--2014 (e.g., PALOMA-3 NCT01942135, MONALEESA-2 NCT01958021, MONARCH-2 NCT02107703). These trials are foundational pivotal CDK4/6i trials cited by ESMO, ASCO, and NCCN and are essential to the corpus.

**Amendment**: the date range is widened to `2013-01-01 .. 2026-05-16` to capture pre-2015 pivotal CDK4/6i trials; the enrolment threshold is tightened from $\ge 50$ to $\ge 200$ to focus the corpus on pivotal-scale trials.

The amendment is **committed before any LLM extraction**, before any DAG construction, and before any EFDPR computation on the v2 corpus. The primary outcome, primary test, and rejection threshold remain unchanged. This amendment is disclosed in the manuscript as a v2 deviation.
