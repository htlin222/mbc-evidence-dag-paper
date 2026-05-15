# Reviewer Report — Biostatistics (Round 1)

**Manuscript:** *A Computable Map of Treatment-Sequencing Evidence in HR+/HER2- Metastatic Breast Cancer: Graph-Theoretic Discordance Between Trial Chains and Guideline Pathways.*
**Reviewer role:** Adversarial biostatistics review.
**Date:** 2026-05-16.

I read `manuscript/main.tex`, `analysis/05_compute_efdpr.py`, `analysis/06_compute_odi.py`, `docs/prereg.md`, and `data/results/efdpr.json`. The framework is interesting and the preregistration is commendable, but the inferential machinery has several errors that, in their current form, do not support the manuscript's headline claim that the preregistered null was rejected. The bootstrap, the primary test, the multiple-testing accounting, and the percentile formula all need attention before this paper can claim a confirmatory rejection.

## A. Most serious issue: the primary preregistered test does NOT reject

The preregistration is explicit (`docs/prereg.md:13`):

> "Rejection threshold for the null 'evidence is complete (EFDPR = 0)': one-sided exact binomial p < 0.05."

and the primary hypothesis (`docs/prereg.md:16`) is `EFDPR > 0.25`. The two clauses together unambiguously specify a one-sided exact binomial test of H0: p ≤ 0.25 versus H1: p > 0.25 (the verbal "EFDPR = 0" is collapsed into the directional threshold 0.25 by the hypothesis statement; charitable reading required).

With n = 15 and observed k = 7, the exact one-sided p-value is

```
P(X ≥ 7 | n = 15, p = 0.25) = Σ_{k=7..15} C(15,k) · 0.25^k · 0.75^(15-k) = 0.0566.
```

This is greater than 0.05. **The preregistered test does not reject the null at the 5% level.** The manuscript nevertheless asserts rejection (`manuscript/main.tex:56`, `manuscript/main.tex:67`, `manuscript/main.tex:135`) by invoking a substitute decision rule — "the 95% bootstrap CI lower bound (0.267) exceeds 0.25." That rule is **not** the preregistered test, is not equivalent to it, and in this borderline regime gives a different decision. The bootstrap CI shown is a percentile interval on the resampled-node statistic, not a Clopper–Pearson exact interval, and the duality between CI exclusion of p0 and rejection of H0: p ≤ p0 does not hold for percentile bootstrap intervals in small-n binomial settings (see also issue B).

**Ask 1 (file:line `docs/prereg.md:13`, `manuscript/main.tex:56`, `manuscript/main.tex:67`, `manuscript/main.tex:135`).** Report the preregistered one-sided exact binomial test as the primary inferential statement: "P(X ≥ 7 | n = 15, p = 0.25) = 0.057, which does not reject H0 at α = 0.05." Then, if desired, present the bootstrap CI as a secondary descriptive measure.

**Ask 2 (file:line `manuscript/main.tex:56`, `manuscript/main.tex:67`).** Remove or qualify all language asserting that the strict-tolerance 95% CI "excluded the pre-registered null of 0.25" as evidence of rejection. The CI lower bound of 0.267 is a property of a 1,000-resample percentile bootstrap on a non-independent sampling unit (see issue C) and is not the preregistered decision rule.

**Ask 3 (file:line `manuscript/main.tex:135`).** State explicitly in Results that the preregistered primary test fails to reject at α = 0.05 under strict and ESCAT-aligned tolerance (p = 0.057) and, a fortiori, under liberal tolerance (k = 6: p = 0.148). The descriptive estimate EFDPR = 0.467 remains informative, but it must be reported as a **non-rejected directional excess**, not as a confirmed rejection.

## B. The substituted "CI lower bound > 0.25" rule is non-equivalent

Even ignoring the preregistration issue, the substituted rule is statistically non-equivalent to the preregistered exact-binomial test:

- The Clopper–Pearson 95% CI for 7/15 is (0.213, 0.734), with lower bound **below** 0.25 — consistent with non-rejection at α = 0.05.
- The Wilson 95% CI for 7/15 is (0.248, 0.699), with lower bound essentially at 0.25 — borderline non-rejection.
- The reported percentile-bootstrap CI is (0.267, 0.733), with lower bound **above** 0.25 — apparent rejection.

The three intervals disagree at the boundary precisely because the percentile bootstrap with n = 15 places its 25th-ranked replicate at the lower edge in a discrete, granular way that is sensitive to seed and to the resampling unit (issue C). Conditioning a published rejection on whichever interval happens to fall on the right side of the threshold is a Type I error inflation vehicle.

**Ask 4 (file:line `manuscript/main.tex:135`).** Report Clopper–Pearson 95% CI for the strict EFDPR (and for the liberal-tolerance EFDPR) alongside the bootstrap CI, and use the exact CI for inferential statements. Bootstrap CIs are acceptable as a complementary heterogeneity measure but should not be the primary inferential interval for a binomial proportion with n = 15.

## C. Bootstrap resampling unit is wrong: guideline nodes are not exchangeable

`analysis/05_compute_efdpr.py:159–169` resamples guideline nodes uniformly with replacement: `sample = [rng.choice(gls) for _ in range(len(gls))]`. This treats the 15 nodes as independent and identically distributed. They are not.

Inspection of `efdpr.json` and the manuscript's `manuscript/main.tex:135` shows that 5 of the 7 evidence-free nodes (G5, G6, G7, G13, G15) share the structural feature "post-CDK4/6i + biomarker-stratified" — i.e. they are clustered in a region of the DAG where pivotal trials are systematically absent. Whether any one of these nodes is evidence-free is determined by the same underlying gap in the trial corpus, not by 15 independent Bernoulli draws. The current bootstrap therefore:

1. **Understates uncertainty** in the direction relevant to the primary hypothesis: independent resampling around a clustered evidence-free region produces a tighter CI than an appropriately cluster-aware bootstrap would.
2. **Misrepresents the inferential target.** The current bootstrap answers "what is the sampling variability if the 15 nodes had been a simple random sample from a hypothetical infinite population of independent decision nodes," which is not the ESMO tree the paper claims to be making inference about.

The downstream impact on the rejection claim is direct: a properly cluster-aware bootstrap would yield a wider CI whose lower bound likely falls below 0.25, which is also what the preregistered exact-binomial test says.

**Ask 5 (file:line `analysis/05_compute_efdpr.py:159`, `manuscript/main.tex:104`).** Either:

(a) **Replace** the node-level bootstrap with a **cluster bootstrap** that resamples the *clusters* of structurally-related decision nodes (operationally: group the 15 nodes by `(prior-state-region, biomarker-family)` — e.g. pre-CDK4/6i cluster, post-CDK4/6i ER-mut cluster, post-CDK4/6i AKT/PI3K cluster, post-CDK4/6i no-actionable cluster, post-2L chemo cluster — and resample whole clusters with replacement), or

(b) **Abandon** the bootstrap CI as a primary inferential device and use the Clopper–Pearson exact CI (which assumes the 15 nodes are the fixed population of interest and reports binomial sampling variability for the underlying p, which is closer to what the preregistration intends).

I lean toward (b): the 15 ESMO HR+/HER2- decision nodes *are* the full ESMO HR+/HER2- decision tree at the freeze date — they are not a sample from a superpopulation. The honest inference is that EFDPR is exactly 7/15 = 0.467 in the population, full stop, and the only sampling-theory question is whether the 14-trial corpus could have generated this many evidence-free nodes by chance under H0: p ≤ 0.25 — which is precisely what the exact-binomial test answers. The bootstrap is, in this design, conceptually redundant.

**Ask 6 (file:line `manuscript/main.tex:104`).** State the inferential target explicitly: is the 15-node tree the population, or a sample? If the former, the bootstrap CI is descriptive at best. If the latter, justify the superpopulation model and use a cluster-aware bootstrap.

## D. Bootstrap percentile indexing is asymmetric and non-standard

`analysis/05_compute_efdpr.py:167–168`:

```python
lo = estimates[int(0.025 * n)]      # = estimates[25]
hi = estimates[int(0.975 * n) - 1]  # = estimates[974]
```

For n = 1,000 this returns the 26th-smallest value (index 25) and the 974th-smallest value (index 974). The standard textbook percentile-bootstrap interval (Efron & Tibshirani 1993, §13.3) is

```
lo = estimates[ceil(α/2 · (n+1)) - 1]      # roughly index 24 or 25
hi = estimates[floor((1 - α/2) · (n+1)) - 1]  # roughly index 974
```

with a number of acceptable variants (numpy's `np.percentile` with default `linear` interpolation; the (n+1) rule; etc.). The current asymmetry — `int(0.025 · n)` for the lower bound but `int(0.975 · n) - 1` for the upper bound — has no textbook basis. With n = 1,000 the numerical impact on this paper is one to two ranks, which is small, but in a borderline regime where the lower bound is being used as the rejection criterion (issue A), even one rank can flip the decision.

**Ask 7 (file:line `analysis/05_compute_efdpr.py:167`).** Replace with `np.percentile(estimates, [2.5, 97.5])` (interpolated) and document the choice. Alternatively, implement BCa (bias-corrected and accelerated, Efron 1987) — this is the modern default for percentile-bootstrap intervals on bounded statistics like a proportion and is preferable for n = 15 where bias is plausibly non-zero.

**Ask 8 (file:line `analysis/05_compute_efdpr.py:167`).** Re-run the analysis with the corrected percentile rule (and ideally BCa) and re-report the CI. If the strict-tolerance lower bound moves below 0.25 after the correction, this further weakens the original rejection claim and must be reported.

## E. Multiple-testing: prereg lists S1, S2, S3, but only S1 (ODI) is reported

The preregistration (`docs/prereg.md:28–31`) commits to three secondary outcomes:

- S1. Operationalization discordance index (ODI)
- S2. Temporal evidence lag
- S3. Subgroup coverage (Asian / ≥70 y / Black/African ancestry)

with Benjamini–Hochberg q < 0.05 across the three (`docs/prereg.md:45`). The manuscript reports only S1 (ODI; `manuscript/main.tex:152`) and is silent on S2 and S3. There is no deviation paragraph (`manuscript/main.tex:177` Data Availability and surrounding sections contain no prereg-deviation language).

**Ask 9 (file:line `docs/prereg.md:28`, `manuscript/main.tex:152`).** Either (a) compute and report S2 and S3 with their Benjamini–Hochberg adjustment, or (b) add an explicit "Deviations from preregistration" paragraph justifying the omission. The preregistration anticipates this requirement (`docs/prereg.md:56`: "Any deviation from this preregistration will be reported in the manuscript with a paragraph explaining the deviation and justification") but the paragraph is absent.

**Ask 10 (file:line `manuscript/main.tex:172`).** Add a "Deviations from preregistration" subsection at the end of Results or beginning of Discussion. Be explicit about what was dropped and why.

## F. ODI has no uncertainty quantification

`analysis/06_compute_odi.py` computes a point estimate of the mean pairwise Jaccard distance per biomarker variable (`analysis/06_compute_odi.py:66–88`). No confidence interval is given for ODI in the manuscript (`manuscript/main.tex:56`, `manuscript/main.tex:152`), even though ODI = 0.905 across 7 trials and ODI = 0.667 across 2 trials are quoted as if precise. For a 2-trial variable (AKTpath) the ODI is literally a single Jaccard distance and has zero degrees of freedom for variance estimation; this should be acknowledged.

**Ask 11 (file:line `analysis/06_compute_odi.py:66`, `manuscript/main.tex:152`).** Add a bootstrap CI for ODI — resample the trial pairs (or, equivalently for a small number of trials, enumerate the leave-one-trial-out values and report a range). For 2-trial variables, replace the ODI with the single Jaccard distance and note explicitly that no variance estimate is possible.

**Ask 12 (file:line `manuscript/main.tex:56`, `manuscript/main.tex:152`).** Add the n-trials denominator next to every ODI in the text (already partially present: "ODI 0.905 across 7 trials"), and footnote that variances are not estimable when n_trials = 2.

## G. ESCAT grouping has an asymmetric definition that may inflate or deflate concordance

`analysis/05_compute_efdpr.py:35–40`:

```python
ESCAT_GROUPS = {
    "AKTpath":   {"AKTpath", "PIK3CAmut"},
    "PIK3CAmut": {"PIK3CAmut"},
}
```

This is asymmetric: AKTpath accepts PIK3CAmut as an ESCAT-equivalent, but PIK3CAmut does not accept AKTpath. ESCAT tier equivalence, as I understand the framework, is intended to be symmetric (two tokens are at the same tier or they are not). The asymmetry here is unjustified in the manuscript (`manuscript/main.tex:99`).

**Ask 13 (file:line `analysis/05_compute_efdpr.py:35`, `manuscript/main.tex:99`).** Either (a) make the mapping symmetric (i.e. PIK3CAmut also accepts AKTpath) and re-run, reporting any change, or (b) justify the asymmetry in Methods with reference to the published ESCAT tier rules.

## H. Bootstrap returns ties at boundaries — discretization effect underreported

`analysis/05_compute_efdpr.py:154` computes `len(evidence_free) / len(gls)` where `len(gls) = 15`, so each bootstrap replicate's EFDPR takes values in {0/15, 1/15, ..., 15/15}. The 95% percentile CI is therefore drawn from a discrete grid of 16 possible values. The reported (0.267, 0.733) is exactly (4/15, 11/15). The reported CI thus has a granularity of 1/15 ≈ 0.067 — slightly larger than the gap between the strict-tolerance lower bound (0.267) and the preregistered threshold (0.25). One additional bootstrap "miss" would push the lower bound below 0.25.

**Ask 14 (file:line `manuscript/main.tex:55`, `analysis/05_compute_efdpr.py:167`).** Acknowledge the bootstrap granularity in Methods (1/15 ≈ 0.067 per unit). Report this alongside the CI. This is one further reason the bootstrap is a fragile primary inferential device at this sample size.

## I. Reproducibility of seed 20260516 — verified

I ran `python3 analysis/05_compute_efdpr.py` twice in the same environment. Both runs produced identical output (`efdpr.json` byte-identical across the two invocations; strict EFDPR = 0.467, CI 0.267–0.733; ESCAT identical; liberal EFDPR = 0.400, CI 0.200–0.667). The seed `seed = 20260516` at `analysis/05_compute_efdpr.py:159` is correctly threaded through `random.Random(seed)` and the bootstrap is deterministic on the same Python interpreter and the same input JSONs.

**Ask 15 (file:line `manuscript/main.tex:112`).** Add an explicit reproducibility statement to Methods documenting (a) the seed value, (b) that two consecutive invocations produce identical output, and (c) the Python version under which determinism was verified (Python 3.12, per `manuscript/main.tex:113`). This is currently implicit and would be a one-line addition.

## J. Minor: numerical reporting precision and rounding consistency

`data/results/efdpr.json` rounds to 4 decimals (`analysis/05_compute_efdpr.py:180–184`) but the manuscript reports 3 decimals inconsistently (e.g. `manuscript/main.tex:56` "0.467" but "0.267–0.733"). Choose one precision and apply it consistently.

**Ask 16 (file:line `manuscript/main.tex:56`, `manuscript/main.tex:135`).** Use 3 decimals throughout the Results text and the table.

## K. Minor: liberal tolerance threshold language

`manuscript/main.tex:56` says under liberal tolerance "the lower CI bound touched the pre-registered threshold." It is below the threshold (0.200 < 0.25). The CI lower bound and the threshold are not equal; "touched" is misleading.

**Ask 17 (file:line `manuscript/main.tex:56`).** Replace "touched" with the numerical statement: "the lower CI bound (0.200) falls below the pre-registered threshold (0.250)."

## L. Minor: subgroup_readouts has no test fixture

`analysis/05_compute_efdpr.py:137` reads `edge.get("subgroup_readouts") or []`. The fallback to `[]` means that if the field is missing, the liberal-tolerance match silently degrades to ESCAT-tolerance match without any logging. Out of scope for biostatistics review but worth a sentence in Methods.

**Ask 18 (file:line `analysis/05_compute_efdpr.py:137`, `manuscript/main.tex:99`).** State in Methods that for trials with no declared `subgroup_readouts`, the liberal-tolerance match coincides with the ESCAT match. Confirm in Results that the liberal-vs-ESCAT difference is driven entirely by EMERALD's declared ESR1mut subgroup readout (already implied by `manuscript/main.tex:172` but worth making explicit).

## Summary of asks

| #  | Issue                                                | File:line                                          |
|----|------------------------------------------------------|----------------------------------------------------|
| 1  | Report preregistered exact-binomial p-value          | `prereg.md:13`, `main.tex:56`, `135`                |
| 2  | Stop equating "CI lower bound > 0.25" with rejection | `main.tex:56`, `67`                                 |
| 3  | State primary test fails to reject                   | `main.tex:135`                                     |
| 4  | Report Clopper–Pearson 95% CI                        | `main.tex:135`                                     |
| 5  | Cluster bootstrap or drop bootstrap                  | `05_compute_efdpr.py:159`, `main.tex:104`           |
| 6  | State inferential target (population vs sample)      | `main.tex:104`                                     |
| 7  | Fix percentile-bootstrap indexing                    | `05_compute_efdpr.py:167`                          |
| 8  | Re-run with corrected percentile rule                | `05_compute_efdpr.py:167`                          |
| 9  | Report S2 and S3 or justify omission                 | `prereg.md:28`, `main.tex:152`                      |
| 10 | Add "Deviations from preregistration" subsection     | `main.tex:172`                                     |
| 11 | Add bootstrap CI for ODI                             | `06_compute_odi.py:66`, `main.tex:152`              |
| 12 | Footnote variance not estimable when n_trials = 2    | `main.tex:56`, `152`                                |
| 13 | Make ESCAT mapping symmetric or justify              | `05_compute_efdpr.py:35`, `main.tex:99`             |
| 14 | Disclose bootstrap granularity 1/15                  | `main.tex:55`, `05_compute_efdpr.py:167`            |
| 15 | Add reproducibility statement (seed verified)        | `main.tex:112`                                     |
| 16 | Consistent decimal precision                         | `main.tex:56`, `135`                                |
| 17 | Replace "touched" with numerical statement           | `main.tex:56`                                      |
| 18 | Document subgroup_readouts default behaviour         | `05_compute_efdpr.py:137`, `main.tex:99`            |

## VERDICT: MAJOR

**Justification.** The preregistered one-sided exact binomial test (p = 0.057) does not reject H0 at α = 0.05, yet the manuscript repeatedly claims a rejection on the basis of a non-equivalent bootstrap-CI rule whose own validity is undermined by an inappropriate resampling unit (cluster-correlated nodes), asymmetric percentile indexing, and 1/15 discretization — all of which the borderline rejection is sensitive to; this is fixable but requires re-running the primary inference and rewriting the headline claims.
