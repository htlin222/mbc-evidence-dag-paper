# Preregistration — mbc-evidence-dag-paper

**Date of preregistration:** 2026-05-16
**Commit hash when this file is committed:** (recorded by git automatically)

## Study title
A computable map of treatment-sequencing evidence in HR+/HER2- metastatic breast cancer: graph-theoretic discordance between trial chains and guideline pathways.

## Primary outcome
**Evidence-free decision-point ratio (EFDPR)**: the proportion of guideline-recommended decision nodes (ESMO mBC 2024 update) for which no edge in the trial-derived DAG satisfies all three concordance criteria — patient-state match, biomarker-definition equivalence, and temporal precedence — at the strict tolerance level.

Statistic: point estimate with bootstrap (1,000 resamples) 95% CI on the proportion.
Rejection threshold for the null "evidence is complete (EFDPR = 0)": one-sided exact binomial p < 0.05.

## Primary hypothesis
EFDPR > 0.25 for HR+/HER2- mBC under the ESMO 2024 guideline tree, i.e. at least one in four guideline recommendations is not directly supported by a single concordant trial-DAG edge.

Directional. Expected effect size based on prototype (6 trials → 4 evidence-free nodes in a 7-node guideline sub-tree): preregistered upper-bound estimate EFDPR ≈ 0.30–0.55. Final analysis on full trial corpus.

## Confirmatory analysis plan
1. Build guideline decision-tree graph from ESMO 2024 mBC update.
2. Build trial DAG from ClinicalTrials.gov phase 2/3 HR+/HER2- mBC trials, 2015–2026.
3. For each guideline node g, run `find_supporting_evidence(g)` against the trial DAG.
4. Point estimate EFDPR = |evidence-free g| / |total g|.
5. Bootstrap CI by resampling guideline nodes with replacement.
6. Sensitivity: vary biomarker-definition tolerance (strict / ESCAT-aligned / liberal).

## Secondary (pre-specified) outcomes
- **S1. Operationalization discordance index (ODI)** for HER2-low, ESR1mut, prior-CDK4/6i variables: mean pairwise Jaccard distance between trial-level inclusion definitions.
- **S2. Temporal evidence lag**: median years between guideline-node creation and earliest supporting trial readout, restricted to guideline nodes that became evidence-supported.
- **S3. Subgroup coverage**: percentage of trials reporting outcomes for Asian, >=70 y, and Black/African ancestry subpopulations.

## Exploratory analyses
- E1. Comparison with NCCN (sensitivity only).
- E2. Network centrality of individual drugs in the trial DAG.
- E3. Citation-network analysis of trial pairs vs. evidence-link strength.

Exploratory results are labelled explicitly and cannot be promoted to primary.

## Stop rules
- Primary hypothesis refuted if 95% CI upper bound of EFDPR < 0.25.
- Clean null: EFDPR point estimate < 0.10 with CI upper bound < 0.15.

## Multiple-testing family
Primary EFDPR is a single test. Secondary outcomes S1, S2, S3: Benjamini-Hochberg q < 0.05 across three tests.

## Data sources (frozen)
- ClinicalTrials.gov API v2 — query freeze date 2026-05-16
- OpenAlex — query freeze date 2026-05-16
- ESMO mBC 2024 update — Annals of Oncology version
- ASCO mBC guideline — most recent open-access version

## Schema version
Trial-eligibility extraction schema v1.0 (frozen). Future-cancer extensions are v1.1+ and do not retroactively modify v1.0 fields.

## Deviations
Any deviation from this preregistration will be reported in the manuscript with a paragraph explaining the deviation and justification.
