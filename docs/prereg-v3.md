# Preregistration v3 — multi-tumor extension (mBC + NSCLC)

**Date of preregistration:** 2026-05-16 (v3; supersedes scope of v2 prereg for the multi-tumor pooled analysis)
**Commit hash when this file is committed:** (recorded by git automatically at the commit that introduces this file, BEFORE any v3 outcome-touching analysis is run)
**Predecessors:** `docs/prereg.md` (v1, 16-trial pilot, frozen at `v1.0.0`); `docs/prereg-v2.md` (v2, 81-trial mBC production, frozen at `v2.0.0`).

## Relationship to v1 and v2
The v1 and v2 preregistrations and their results remain unmodified and unmoved. v3 governs the **multi-tumor pooled** analysis whose plan, scope, and inferential procedure are committed BEFORE any NSCLC outcome data (i.e., before LLM extraction or DAG construction on the NSCLC corpus) is observed.

The v2 mBC point estimate is knowable to v3 and is used here only to seed the power calculation. The v3 inferential commitment is not adjusted on the basis of v2's point estimate.

## Study title (v3)
A computable map of treatment-sequencing evidence in biomarker-driven metastatic cancer: a pre-registered, multi-tumor graph-theoretic analysis of ESMO, ASCO, and NCCN decision-tree concordance in HR+/HER2- breast cancer and EGFR-mutant/ALK-rearranged non-small-cell lung cancer.

## Scope additions to v2
The v3 analysis adds **EGFR-mutant and ALK-rearranged metastatic NSCLC** as the second tumor type, using the same frozen JSON schema v1.0 and the same concordance algorithm. The combined unified decision tree comprises:
- mBC HR+/HER2-: 25 nodes (from v2, unchanged)
- NSCLC EGFR-mutant: target 12--18 nodes
- NSCLC ALK-rearranged: target 8--12 nodes
- **Total target: 45--55 unified decision nodes** (power-adequate for the primary test under realistic effect sizes)

NSCLC scope explicitly **excludes** driver-negative NSCLC, KRAS G12C, ROS1, RET, MET ex14, NTRK, BRAF V600E, and HER2-mutant subtypes from the v3 primary analysis. These are deferred to v4. The exclusion is **pre-specified**, not data-driven.

## Primary outcome (v3; unchanged from v1/v2 definition, applied to combined denominator)
**Pooled Evidence-Free Decision-Point Ratio (EFDPR)** under strict tolerance: the proportion of the combined mBC + NSCLC HR+/HER2- and EGFR/ALK decision nodes for which no edge in the combined trial-DAG satisfies all four concordance criteria.

## Primary hypothesis (v3)
$H_1: \mathrm{EFDPR}_{\mathrm{pooled}} > 0.25$, against $H_0: \mathrm{EFDPR}_{\mathrm{pooled}} \le 0.25$.

## Pre-specified primary test (v3; unchanged inference machinery)
One-sided exact binomial test of $H_0: p \le 0.25$ at $\alpha = 0.05$, given $k$ evidence-free nodes out of $n$ pooled guideline nodes.

The test is the **single primary inferential commitment** of v3. Tumor-stratified EFDPR (mBC-only, NSCLC-only, EGFR-only, ALK-only) is reported as pre-specified sensitivity.

## Power analysis (new in v3)
Exact one-sided binomial power against $H_0: p \le 0.25$ at $\alpha = 0.05$:

| Effect $p_1$ | $n$ pooled nodes | Power |
|---:|---:|---:|
| 0.35 | 40 | 30.5% |
| 0.35 | 50 | 37.8% |
| 0.35 | 60 | 44.1% |
| 0.40 | 40 | 56.0% |
| 0.40 | 50 | 66.4% |
| 0.40 | 60 | 74.3% |
| 0.45 | 50 | 86.1% |
| 0.50 | 40 | 92.3% |
| 0.50 | 50 | 96.8% |

Given the v2 mBC point estimate (0.40) and the clinically expected NSCLC effect (likely similar or higher due to younger evidence base for many EGFR/ALK 2L+ decision nodes), the pooled $p_1$ is likely in the 0.40--0.50 range. **At $n = 50$ pooled nodes the test achieves 66--97% power.**

## Confirmatory analysis plan (v3)
1. Run a systematic ClinicalTrials.gov v2 API query for phase 2/3 NSCLC trials with EGFR or ALK biomarker tags (query frozen in `analysis/v3_01_systematic_search_nsclc.py` at the prereg-v3 commit, BEFORE any extraction).
2. Apply the v2 inclusion filters with NSCLC adaptations: phase 2/3 interventional; started 2013--2026; metastatic/advanced; eligibility text mentions EGFR mutation OR ALK rearrangement; HER2-positive breast trials excluded (cross-tumor filter); enrolment $\ge 100$ (NSCLC pivotal trials sometimes have smaller enrolments than mBC); primary completion by 2026.
3. Target NSCLC corpus size **n_NSCLC_trials $\ge 30$**.
4. Extract eligibility into frozen schema v1.0 (extending biomarker vocabulary with NSCLC-specific tokens: \texttt{egfr\_mut}, \texttt{egfr\_t790m}, \texttt{egfr\_ex19del}, \texttt{egfr\_l858r}, \texttt{egfr\_ex20ins}, \texttt{alk\_rearranged}, \texttt{alk\_resistance\_mut}). The schema extension is **additive only**; no v1.0 field is modified.
5. Two-annotator LLM extraction on a 15-trial NSCLC validation subset (seed 20260516); compute Cohen's $\kappa$ and PABAK on key fields.
6. Encode the unified ESMO/ASCO/NCCN NSCLC EGFR + ALK decision tree (target 20--30 nodes).
7. Build the combined trial-DAG (mBC + NSCLC) using shared node space.
8. Compute pooled EFDPR under strict, ESCAT-aligned, and liberal tolerance.
9. Run the pre-registered exact-binomial test on the pooled strict-tolerance EFDPR. Tumor-stratified EFDPR (mBC, NSCLC-overall, EGFR, ALK) reported as sensitivity.

## Secondary outcomes (v3)
- **S1.** Operationalization discordance index (ODI) per biomarker variable on the combined corpus.
- **S2.** Tumor-stratified EFDPR: mBC-only, NSCLC-overall, NSCLC-EGFR, NSCLC-ALK.
- **S3.** Cross-tumor consistency: do the structural patterns of evidence sparsity (which positions are evidence-free) replicate between mBC and NSCLC?
- **S4.** LLM-extraction inter-rater agreement at production scale (full Cohen's $\kappa$ and PABAK reporting across both tumor types).

## Exploratory analyses
- E1. Detailed breakdown of EGFR-mutant 2L+ post-osimertinib decision nodes (the MARIPOSA-2 vs COMPEL vs HERTHENA-Lung01 evidence space).
- E2. ALK-rearranged 1L generation choice (alectinib vs brigatinib vs lorlatinib).
- E3. Citation-network analysis if OpenAlex integration time permits.

## Stop rules
- Primary hypothesis refuted if 95% CI upper bound of pooled EFDPR < 0.25.
- Clean null: pooled point estimate < 0.10 with upper CP-CI bound < 0.15.

## Pre-specified deviations from v2
- **G18 numbering gap retained** (G18 was an early-draft placeholder that was removed; renumbering would invalidate v2 commit history).
- **NSCLC corpus enrolment threshold $\ge 100$** (vs mBC $\ge 200$ in v2 amendment v2.1). NSCLC pivotal trials in driver-defined subgroups often have smaller enrolments; the lower threshold is pre-specified, not data-driven.

## Validation gates
- **LLM-extraction Cohen's $\kappa$ or PABAK $\ge 0.70$** on key fields for the NSCLC validation subset.
- **NSCLC corpus size $\ge 30$ trials.**
- **NSCLC guideline-node count $\ge 18$.**
- **Pooled guideline-node count $\ge 40$.**

If any gate fails, the deviation is disclosed and the analysis proceeds with the available data; the primary outcome and test remain unchanged.

## Two-paper plan (post-analysis)
The v3 analysis supports two manuscripts written in parallel from the same evidence base:

- **Paper A (Clinical Application)**: "Evidence-free decision points in biomarker-driven mBC and NSCLC: a pre-registered multi-tumor audit of ESMO/ASCO/NCCN HR+/HER2-, EGFR, and ALK decision trees." **Target: JCO Precision Oncology** (or JCO Clinical Cancer Informatics as backup).
- **Paper B (Methods)**: "A graph-theoretic framework for measuring evidence-free decision points in clinical guidelines, with dual-LLM-annotator validation across two solid tumors." **Target: Research Synthesis Methods**.

Both papers cite the same underlying analysis and pre-registration. The clinical-application paper foregrounds the tumor-specific findings; the methods paper foregrounds the framework, schema, and inter-rater validation.

## Multiple-testing across the two papers
The pooled primary test is run **once**. Tumor-stratified estimates are sensitivity, not independent confirmatory tests. The two papers report the same primary finding from different framings.

## Frozen prior to outcome data
This v3 prereg is committed BEFORE the NSCLC systematic search is executed. The commit hash of THIS file is the v3 prereg timestamp.
