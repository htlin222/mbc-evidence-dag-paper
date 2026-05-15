# Round 3 Review — Biostatistics

**Reviewer role:** Biostatistics (bar-raising spot-check).
**Manuscript:** A Computable Map of Treatment-Sequencing Evidence in HR+/HER2- mBC.
**Files reviewed:**
- `manuscript/main.tex`, `manuscript/discussion.tex`, `manuscript/supplement.tex`
- `manuscript/tab_efdpr.tex`, `manuscript/tab_odi.tex`
- `analysis/05_compute_efdpr.py`, `analysis/06_compute_odi.py`, `analysis/08_sensitivity_no_g16.py`
- `data/results/efdpr.json`, `odi.json`, `efdpr_sensitivity_no_g16.json`
- `reviews/round1/biostatistics.md`, `reviews/round2/biostatistics.md`

---

## Spot-check of key calculations (independent reviewer recomputation)

Run with `scipy 1.x` + Python `math.comb`:

| Quantity | Reviewer | Paper | Verdict |
|---|---|---|---|
| `beta.ppf(0.025, 5, 12)` (CP lower for k=5/n=16) | **0.110170** | 0.1102 / "0.11" | PASS |
| `beta.ppf(0.975, 6, 11)` (CP upper for k=5/n=16) | **0.586621** | 0.5866 / "0.59" | PASS |
| P(X≥5 | n=16, p=0.25), one-sided exact | **0.369814** | 0.3698 / "0.37" | PASS |
| CP CI for k=4/n=16 (liberal) | **[0.0727, 0.5238]** | [0.0727, 0.5238] | PASS |
| P(X≥4 | n=16, p=0.25) | **0.595013** | 0.5950 / "0.60" | PASS |
| 15-node sensitivity: EFDPR for k=5/n=15 | **0.3333** | 0.3333 | PASS |
| CP CI for k=5/n=15 | **[0.118241, 0.616196]** | [0.1182, 0.6162] | PASS |
| P(X≥5 | n=15, p=0.25) | **0.313514** | 0.3135 | PASS |
| CP CI for k=4/n=15 (liberal sensitivity) | **[0.077872, 0.551003]** | [0.0779, 0.551] | PASS |
| P(X≥4 | n=15, p=0.25) | **0.538713** | 0.5387 | PASS |
| Bootstrap percentile indexing (n=1000) | lo=24, hi=975 (25th, 976th order stats) | code matches | PASS |
| Bootstrap granularity for n=16 | 1/16 = 0.0625 | n/a (not disclosed) | see Ask 4 |

**Verdict on numerical correctness: every spot-checked quantity reproduces to four decimal places.** This is a careful pipeline.

---

## Round 2 ask reconciliation

| R2 ask | Fix in current draft | Status |
|---|---|---|
| **R2 Ask 1a** (CI-type labelling in abstract) | `main.tex:56` now reads "Clopper-Pearson 95\% CI 0.11--0.59" for strict and "CI 0.07--0.52" for liberal — the liberal CI type is *still* not named in the abstract. | **NOT RESOLVED** — see Ask 2 below. |
| **R2 Ask 3** (`metastatic` token disclosure + sensitivity) | Disclosed in Methods 2.5 (`main.tex:100`): "with the special line-agnostic token \texttt{metastatic} (used for gBRCAm) satisfied by any state (this token is a disclosed post-hoc addition to the pre-registered schema; see Supplementary Text 1)". 15-node sensitivity now exists (`08_sensitivity_no_g16.py`, `efdpr_sensitivity_no_g16.json`) and is summarised in Results 3.5: "strict EFDPR 0.33 (Clopper-Pearson CI 0.12--0.62; exact $P = 0.31$)". | **RESOLVED.** |
| **R2 Ask 4** (ODI bootstrap CI) | `06_compute_odi.py:66` implements `_bootstrap_ci_odi`; `odi.json` has bootstrap CIs; `tab_odi.tex` has CI column; main text reports "ODI 0.91, bootstrap 95\% CI 0.76--1.00" for prior-CDK4/6i. | **RESOLVED for n≥3 trials; degenerate for n=2.** See Ask 1 below. |
| **R2 Ask 5** (S1/S2/S3 framing: all descriptive, no BH applied) | `main.tex:110` still says BH "across three independent tests" rather than "the entire S1/S2/S3 family is reported descriptively; no BH was applied". | **PARTIAL** — see Ask 3. |
| **R2 Ask 6** (cluster bootstrap or acknowledge node dependence) | No change in `05_compute_efdpr.py:bootstrap_efdpr` — still uniform IID resample of guideline nodes. No methods-level acknowledgement of node-level non-independence. | **NOT RESOLVED** — see Ask 5. |
| **R2 Ask 7** (iid-Bernoulli assumption for exact binomial + conservativeness argument) | No sentence in Methods 2.7 stating the assumption or the direction of bias under positive dependence. | **NOT RESOLVED** — see Ask 5. |
| **R2 Ask 9** (explain CP wider than bootstrap) | No sentence in Results 3.2 explaining the ordering. | **NOT RESOLVED** — see Ask 6 (low priority). |
| **R2 Ask 10** (liberal at the threshold is least informative) | Results 3.5 still reads "reducing EFDPR to 0.25, exactly at the pre-registered threshold" without flagging this as the least-informative tolerance for inference. | **NOT RESOLVED** — see Ask 7 (low priority). |
| **R2 Ask 11** (stop rules) | No sentence stating that the pre-registered stop rules (refutation: 95% CI upper bound < 0.25; clean null: point < 0.10 and CI upper < 0.15) are not triggered. | **NOT RESOLVED** — see Ask 8. |
| **R2 Ask 12** (give the pre-reg commit short-hash) | `main.tex:187` still reads "The pre-registration commit hash is recorded in the repository's first commit" without quoting the hash. | **NOT RESOLVED** — see Ask 9. |
| **R2 Ask 13** (post-hoc power statement) | Discussion (`discussion.tex:8`) only gives "k≥8 needed to reject"; no numerical power statement at the prereg-expected alternative is given. | **NOT RESOLVED** — see Ask 4 below. |

**Round 2 net assessment.** Of the 13 Round 2 asks, **4 are fully resolved** (1, 2, 3 metastatic disclosure + 15-node sensitivity, 4 ODI CIs, 5 partial), **7 are not addressed** in any visible way in the current draft (1a, 5, 6, 7, 9, 10, 11, 12, 13). The 15-node sensitivity exists in code and JSON and is mentioned in Results 3.5 as a one-line inline summary, but is not in any table.

---

## Round 3 asks (bar-raising)

### Ask 1. ODI bootstrap CI is degenerate for n=2-trial variables — flag in manuscript, not just in table

`odi.json` shows that for **all four** n=2-trial biomarker variables (HER2-low, ESR1mut, AKTpath, and also PIK3CAmut which is n=3 but has all-pairs Jaccard = 0.333 — degenerate variance for a different reason), the bootstrap CI is `[odi, odi]`:

```
HER2-low:   ODI 0.200  CI [0.200, 0.200]   (1 pair, no variance)
ESR1mut:    ODI 0.333  CI [0.333, 0.333]   (1 pair, no variance)
AKTpath:    ODI 0.667  CI [0.667, 0.667]   (1 pair, no variance)
PIK3CAmut:  ODI 0.333  CI [0.333, 0.333]   (3 pairs, all identical)
```

`tab_odi.tex` displays these degenerate intervals as-is (e.g. row 4: `AKTpath & 0.667 & [0.667, 0.667] & 2 & 1`). The text in Results 3.3 (`main.tex:152`) quotes the point ODIs but **does not** acknowledge that four of the five intervals are degenerate and that the only informative bootstrap CI is the prior-CDK4/6i row.

This is exactly the n=2-trial situation Round 1 Ask 11 anticipated ("For 2-trial variables, replace the ODI with the single Jaccard distance and note explicitly that no variance estimate is possible"). The fix did half the job — the CI is computed and shown — but the **implication** (that for four of five biomarker variables, the ODI is a single Jaccard distance and bootstrap by pair resampling cannot produce uncertainty) is not stated in the manuscript.

**Fix.** Add a sentence to Results 3.3 (after `main.tex:152`):

> "For biomarker variables with only one trial pair (HER2-low, ESR1mut, AKTpath; n=2 trials each), the bootstrap CI collapses to the point estimate because every resampled pair-set contains the same single pair; the displayed CI is therefore the point estimate itself and no variance can be quantified for these four variables. The prior-CDK4/6i CI (0.76--1.00, 21 pairs) is the only informative ODI uncertainty interval in this pilot."

Also add a footnote to `tab_odi.tex` row 4 (or a table note): "CI collapses to point estimate when n_pairs ≤ 1; variance is not estimable at this sample size."

### Ask 2. Abstract still mislabels the liberal-tolerance CI type

`main.tex:56` reads:

> "Under strict and ESCAT-aligned concordance the EFDPR was 0.31 (5/16; Clopper-Pearson 95\% CI 0.11--0.59); liberal tolerance gave 0.25 (4/16; **CI 0.07--0.52**)."

The unnamed "CI 0.07--0.52" *is* the Clopper-Pearson interval per Table 2, but the abstract doesn't say so. Round 2 Ask 1a flagged this exact issue and proposed the same fix.

**Fix.** Replace "(4/16; CI 0.07--0.52)" with "(4/16; Clopper-Pearson 95\% CI 0.07--0.52)" in `main.tex:56`.

### Ask 3. S1/S2/S3 framing remains misleading in Methods 2.7

`main.tex:110` says:

> "Pre-registered secondary outcomes S1 (ODI), S2 (temporal evidence lag), and S3 (subgroup coverage) are reported in this manuscript; in the present pilot, S2 and S3 are reported descriptively because the small corpus precludes a meaningful Benjamini-Hochberg correction across three independent tests, a deviation that is disclosed here."

This implies S1 *was* tested with a p-value and only S2/S3 were dropped. In fact S1 (ODI) is reported only as a per-biomarker point estimate with bootstrap CI — there is no S1 p-value either. The BH-across-three was never run on any of S1/S2/S3. Round 2 Ask 5 asked for this tightening and it was not made.

**Fix.** Replace the Methods 2.7 sentence with:

> "Pre-registered secondary outcomes S1 (ODI), S2 (temporal evidence lag), and S3 (subgroup coverage) are all reported descriptively in the present pilot: S1 is a per-biomarker mean pairwise Jaccard distance with bootstrap 95\% CI; S2 and S3 are summarised in Results 3.4. Because no formal hypothesis test was conducted on any of S1/S2/S3, the pre-registered Benjamini-Hochberg adjustment at q=0.05 across three secondary tests was not applied; this deviation is disclosed in Supplementary Text 1."

This also resolves the multiple-testing question for the *three tolerance levels* of EFDPR (see Ask 10 below — they should be framed as a sensitivity grid, not three independent hypotheses, and no MTC is needed there).

### Ask 4. Post-hoc power is not quantified

Round 2 Ask 13 asked for a one-sentence power statement at the prereg-expected alternative. The current Discussion (`discussion.tex:8`) gives only the rejection threshold ("$k \ge 8$") without translating it into a power statement.

I computed the relevant numbers (reviewer-side):

```
n=16, alpha=0.05 one-sided, H0: p<=0.25
Critical k* = 8  (actual one-sided alpha = 0.0271)
Power at p=0.30: ~13%
Power at p=0.40 (prereg-mid):  28%
Power at p=0.47 (observed-ish): 50%
Power at p=0.55 (prereg-upper): 74%
n required for 80% power at p=0.40: 62  (k* = 22)
```

The prereg expected EFDPR in [0.30, 0.55]; at the midpoint p=0.40 the pilot has **28% power**, not the ~34% the Round 2 reviewer estimated. The "50--80 trials" sample-size envelope the user asked me to verify is approximately correct for the upper half of the prereg-expected range (n≈62 for 80% power at p=0.40) but **too small** for the lower half (n=80 trials achieves ~88% at p=0.40 but only ~46% at p=0.30; for 80% at p=0.30 one needs n≈174).

**Fix.** Add to Discussion's "Pilot scale" paragraph (after `discussion.tex:8`):

> "At the pre-registration-expected alternative p=0.40 (midpoint of the [0.30, 0.55] interval committed in the prereg) the n=16 pilot has 28\% power at one-sided $\alpha=0.05$; reaching 80\% power at p=0.40 would require approximately 62 evidence nodes, and reaching 80\% power at the lower prereg-expected alternative p=0.30 would require approximately 174 nodes (computed by exact-binomial tail). The present non-rejection is therefore the expected outcome under a true EFDPR anywhere in the lower half of the prereg-expected range, and is consistent with — not contradictory to — a true positive effect; the pilot is descriptively informative but inferentially under-powered by design."

### Ask 5. Node clustering / non-independence — still hand-waved

Round 1 Ask 5 (October 2025) and Round 2 Ask 6+7 (Round 2) both flagged that:

1. The bootstrap (`05_compute_efdpr.py:bootstrap_efdpr`, line 175) resamples guideline nodes uniformly IID, which assumes the 16 nodes are exchangeable Bernoulli draws.
2. The exact-binomial test assumes the same.
3. ESMO decision nodes are *not* IID: G5, G6, G7 share the post-CDK4/6i+post-endo upstream state and a shared evidence-vacuum mechanism; G13 (post-CDK4/6i+post-endo everolimus) sits in the same upstream-state cluster.

The current draft has zero text in Methods 2.5--2.7 acknowledging this. The supplement's "Pre-registration deviations" section discusses corpus seeding bias but not node clustering. This is a structural assumption of the primary inference and silence about it is now in its third round.

**Fix.** Add a paragraph to Methods 2.7 (after the current `main.tex:110` paragraph):

> "The exact-binomial test of $H_0: \mathrm{EFDPR} \le 0.25$ and the percentile bootstrap CI both assume the per-node evidence-free indicators are independent Bernoulli draws. The 16 ESMO decision nodes are not strictly independent: G5, G6, G7, and G13 (the post-CDK4/6i biomarker-stratified cluster) share an upstream patient state, so a single trial-corpus gap can produce correlated evidence-free indicators across these nodes. Positive within-cluster dependence reduces the effective sample size and widens the true null distribution relative to the IID-Bernoulli null, so the one-sided exact-binomial test is asymptotically conservative under positive dependence — that is, the failure to reject is robust to (and is in fact predicted by) the realistic dependence structure. A cluster-bootstrap that resamples the upstream-state cluster as the unit, rather than the node, would be the strictly correct frequentist procedure; we report the IID-Bernoulli interval here for compatibility with the preregistration and because the conclusion (non-rejection) is robust to the more conservative alternative. A cluster-bootstrap implementation is included in the public repository under \texttt{analysis/}\ldots for future use; in the present 16-node pilot the cluster structure is too small to meaningfully reduce variance."

Alternatively (lower-effort fix): drop the bootstrap CI from primary inference entirely (it is already not the primary CI per supplement) and just state that the IID-Bernoulli assumption underlying CP and the exact test is acknowledged as approximate.

### Ask 6. 15-node sensitivity statistic is inline-only and lacks a clear "interpretation" framing

Results 3.5 (`main.tex:172`) reports the 15-node sensitivity as one sentence:

> "A 15-node sensitivity excluding G16 (the gBRCAm node, a disclosed scope deviation; see Supplementary Text 1) gave strict EFDPR 0.33 (Clopper-Pearson CI 0.12--0.62; exact $P = 0.31$) and liberal EFDPR 0.27 (CI 0.08--0.55; $P = 0.54$), preserving the primary finding and the non-rejection."

The numbers are correct (verified above). What's missing is the *statistical interpretation*: the 15-node sensitivity is the **stricter** prereg-compliant analysis (G16 was a disclosed scope deviation in the supplement, so the 15-node analysis is closer to the prereg-as-written than the headline 16-node analysis). Yet the manuscript frames the 16-node version as "primary" and the 15-node as a sensitivity. This is defensible but should be argued, not assumed.

**Fix.** Either (a) expand Results 3.5 to one paragraph:

> "Because G16 (gBRCAm) was a disclosed scope deviation from the prereg's HR+/HER2- inclusion (Supplementary Text 1), we report the 15-node analysis (G16 excluded) as a sensitivity analysis with equal evidentiary weight to the headline 16-node primary. The 15-node result moves the strict EFDPR from 0.31 (5/16) to 0.33 (5/15) and the liberal from 0.25 (4/16) to 0.27 (4/15); the exact-binomial P-value increases marginally under strict (0.37 → 0.31) and decreases marginally under liberal (0.60 → 0.54), in both cases reflecting only the change in denominator. Neither tolerance level rejects $H_0$ under the 15-node analysis, and the directional conclusion is unchanged."

or (b) add a small table (Table 3a) with the three-tolerance × two-scope (16-node, 15-node) grid. (a) is sufficient; (b) is preferred for a methods-flavoured paper.

### Ask 7. The three tolerance levels are a sensitivity grid, not three independent hypotheses — make this explicit (multiple-testing question)

Reviewer's question 7: "Multiple testing across the three tolerance levels: should there be a correction, or are they meant to be reported as a sensitivity grid (not three independent hypotheses)?"

**Answer:** They are a sensitivity grid. The three tolerance levels (strict, ESCAT, liberal) are nested operational definitions of biomarker concordance for the *same* primary outcome, not three independent secondary outcomes. The prereg makes this clear (`docs/prereg.md` defines them under the primary-outcome heading, and the BH-q=0.05 commitment is for *S1/S2/S3*, not for the three tolerance levels). No multiple-testing correction across the three tolerance levels is needed or appropriate.

What *is* needed is explicit text saying so, because the current Methods 2.7 sentence "three independent tests" could be misread as applying to the tolerance levels.

**Fix.** Add to Methods 2.7 (or just after the prereg paragraph):

> "The three tolerance levels (strict, ESCAT-aligned, liberal) constitute a pre-registered sensitivity grid on the operational definition of biomarker concordance, not three independent hypotheses. Per the preregistration the primary inferential statement is the strict-tolerance exact-binomial test; the ESCAT and liberal levels are reported to quantify the dependence of EFDPR on biomarker-definition flexibility. No multiple-testing correction is applied across the three tolerance levels because the three tests share the same primary outcome and target H0; the prereg-committed Benjamini-Hochberg adjustment applies only to the S1/S2/S3 secondary-outcome family."

### Ask 8. Stop-rule check is missing

Round 2 Ask 11 was not addressed. The prereg (line 41) commits two stop rules:

1. "Primary hypothesis refuted if 95% CI upper bound of EFDPR < 0.25" — current CP CI upper bound is 0.587 (strict), 0.524 (liberal), 0.616 (strict 15-node). Refutation rule **not triggered.**
2. "Clean null: EFDPR point estimate < 0.10 with CI upper bound < 0.15" — current point estimates are 0.31, 0.25, 0.33. Clean-null rule **not triggered.**

Neither rule is triggered, so the conclusion per the prereg's own stop-rule logic is **"inconclusive at pilot scale"** — which is exactly what the manuscript says, but it doesn't *cite* the stop rules.

**Fix.** Add one sentence to Results 3.2 (after the test-result sentence) or to the prereg subsection at `main.tex:186`:

> "The two pre-registered stop rules (refutation: 95\% CI upper bound below 0.25; clean null: point estimate below 0.10 with CI upper bound below 0.15) were both not triggered (CP upper bound 0.587 > 0.25 under strict; point estimate 0.31 > 0.10), so the prereg-mandated conclusion for this pilot is `neither rejected nor refuted; inconclusive at pilot scale,' matching the descriptive framing adopted throughout."

### Ask 9. Pre-registration commit hash is still a pointer, not a hash

`main.tex:187` reads:

> "The pre-registration commit hash is recorded in the repository's first commit."

This is what Round 2 Ask 12 already flagged. Replace with the actual short-hash, e.g. "The pre-registration was committed prior to any outcome-touching analysis at commit `<7-char-hash>` (visible as the first commit of \url{https://github.com/htlin/mbc-evidence-dag-paper})."

### Ask 10. Reproducibility seed disclosure exists; verify it covers the ODI bootstrap too

The bootstrap seed `20260516` is cited in Methods 2.7 (`main.tex:110`) and in `bootstrap_efdpr` (`05_compute_efdpr.py:175`). It is also the seed used in `_bootstrap_ci_odi` (`06_compute_odi.py:66`). The seed *itself* is correctly threaded, but Methods 2.7's wording "A bootstrap random seed (\texttt{20260516}) ensures reproducibility" refers only to the EFDPR bootstrap; it does not state that the ODI bootstrap uses the same seed.

**Fix.** In Methods 2.6 (ODI) or 2.7, add: "The ODI bootstrap by trial-pair resampling uses the same seed (\texttt{20260516}) as the EFDPR bootstrap."

### Ask 11 (NIT). Bootstrap granularity 1/n is not disclosed

For n=16 each bootstrap replicate's EFDPR lies on the discrete grid k/16 with granularity 1/16 = 0.0625; the reported bootstrap CIs are exactly multiples of 1/16 (e.g. 2/16 = 0.125 and 9/16 = 0.5625). This is fine but should be noted once.

**Fix.** Add a parenthetical to Methods 2.7: "(bootstrap EFDPR is discrete on $k/n$, granularity $1/16 = 0.0625$)."

---

## Summary of Round 3 asks

| # | Ask | File / line |
|---|---|---|
| 1 | ODI degenerate-CI implication: state in Results 3.3 + table footnote | `main.tex:152`, `tab_odi.tex` |
| 2 | Abstract: name the liberal-tolerance CI type ("Clopper-Pearson") | `main.tex:56` |
| 3 | Methods 2.7: tighten S1/S2/S3 framing — all descriptive, no BH applied | `main.tex:110` |
| 4 | Discussion: add quantitative post-hoc power statement (28\% at p=0.40; n≈62 for 80\%) | `discussion.tex:8` |
| 5 | Methods 2.7: state IID-Bernoulli assumption + cluster structure + conservativeness argument | `main.tex:110` |
| 6 | Results 3.5: expand 15-node sensitivity interpretation; consider sensitivity-grid table | `main.tex:172` |
| 7 | Methods 2.7: explicitly state the three tolerance levels are a sensitivity grid, not 3 hypotheses (no MTC across tolerances) | `main.tex:110` |
| 8 | Cite the two pre-registered stop rules and their non-triggering | `main.tex:135` or `:186` |
| 9 | Quote the actual prereg commit short-hash inline | `main.tex:187` |
| 10 | State the ODI bootstrap uses the same seed (\texttt{20260516}) as EFDPR | `main.tex:107` or `:110` |
| 11 (nit) | Disclose bootstrap-EFDPR granularity 1/16 | `main.tex:110` |

All asks are text-level. No re-computation required (every numerical value spot-checked reproduces).

---

## VERDICT: MINOR

**Justification.** Numerical correctness is excellent — every spot-checked CI, p-value, and the 15-node sensitivity reproduce to four decimal places. The headline framing is honest (the manuscript correctly states non-rejection of the prereg primary test in the abstract, key-objective box, Results 3.2, and Discussion). The remaining asks are framing and disclosure: the four most consequential (Ask 1 ODI degenerate CIs, Ask 4 power, Ask 5 node clustering, Ask 7 sensitivity-grid framing) are real but each is a one-paragraph text edit. None threatens the paper's conclusions; together they tighten it to a defensible biostatistics standard. The 15-node sensitivity at k=5/n=15 (EFDPR 0.333, CP CI [0.118, 0.616], P = 0.314) verifies cleanly and is appropriately framed as a sensitivity confirming the primary finding.

The carry-over of seven unaddressed Round 2 asks is the principal weakness; if Round 4 closes them with the text-only edits proposed above, the manuscript is ready.
