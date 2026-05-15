# Round 4 Review (FINAL) — Biostatistics

**Reviewer role:** Biostatistics (final spot-check before preprint).
**Manuscript:** A Computable Map of Treatment-Sequencing Evidence in HR+/HER2- mBC.
**Files reviewed:**
- `manuscript/main.tex`, `manuscript/discussion.tex`, `manuscript/supplement.tex`
- `manuscript/tab_efdpr.tex`, `manuscript/tab_odi.tex`
- `analysis/05_compute_efdpr.py`, `analysis/06_compute_odi.py`, `analysis/08_sensitivity_no_g16.py`
- `data/results/efdpr.json`, `efdpr_sensitivity_no_g16.json`, `odi.json`
- `reviews/round[1-3]/biostatistics.md`

---

## 1. Round 4 headline spot-check (the three numbers the editor requested)

Recomputed with `math.comb` (Python 3.12). Tail formula `P(X >= k | n, p) = sum_{x=k..n} C(n,x) p^x (1-p)^(n-x)`.

| Quantity | Reviewer recomputation | Paper / JSON | Verdict |
|---|---|---|---|
| strict 5/16 point estimate | 5/16 = **0.3125** | `efdpr.json:3` = 0.3125 ; main.tex:135 = "0.31 (5/16)" | PASS |
| P(X≥5 \| n=16, p=0.25) | **0.36981** | `efdpr.json:10` = 0.3698 ; main.tex:135 / tab_efdpr.tex = "P = 0.37" | PASS |
| liberal 3/16 point estimate | 3/16 = **0.1875** | `efdpr.json:123` = 0.1875 ; main.tex:135 = "0.19 (3/16)" | PASS |
| P(X≥3 \| n=16, p=0.25) | **0.80289** | `efdpr.json:130` = 0.8029 ; main.tex:135 = "P = 0.80" | PASS |
| 15-node strict 5/15 point estimate | 5/15 = **0.33333** | `efdpr_sensitivity_no_g16.json:3` = 0.3333 ; main.tex:172 = "0.33" | PASS |
| P(X≥5 \| n=15, p=0.25) | **0.31351** | `efdpr_sensitivity_no_g16.json:14` = 0.3135 ; main.tex:172 = "P = 0.31" | PASS |

Also re-verified the Clopper-Pearson intervals and bootstrap percentile indexing (lo_idx=24, hi_idx=975 for n=1000) — all reproduce.

**Verdict on numerical correctness: every spot-checked quantity reproduces to four decimal places.** The pipeline is sound and the headline is honest.

---

## 2. Important: undocumented liberal-tolerance change since Round 3

Between Round 3 (under review on 2026-05-15) and Round 4 (current), the **liberal-tolerance headline changed from 4/16 = 0.25 (P=0.60) to 3/16 = 0.1875 (P=0.80)**. The evidence-free set under liberal shrank from {G6, G7, G9, G13} (R3 implicit) to {G7, G9, G13} (R4, `efdpr.json:132`). The `discussion.tex:14` rationale ("moving from strict to liberal converted two nodes G5 and G6...") is internally consistent with the R4 JSON, but **no place in the manuscript or in `supplement.tex` Supplementary Text 1 ("Pre-registration deviations")** discloses that this set of rescues differs from the Round 3 draft, nor explains the algorithmic change (was a token added to a trial's `subgroup_readouts`? was the `_biomarker_match_liberal` logic altered? was an edge added?).

This is not a numerical error — the current numbers are self-consistent — but a pre-registered methods paper that has gone through four reviewer rounds owes the reader a one-line provenance note when the liberal-tolerance count moves by one node between rounds, especially because that change pulls the liberal point estimate below the pre-registered 0.25 threshold and is now used as a supporting argument for non-rejection.

**Fix (Ask 1 below).**

---

## 3. Round 3 ask reconciliation

| R3 ask | Round 4 status | Resolution |
|---|---|---|
| **R3 Ask 1** ODI degenerate-CI footnote/Results sentence | `tab_odi.tex` still shows `[0.667, 0.667]`, `[0.333, 0.333]`, `[0.200, 0.200]`; `main.tex:152` does not flag that 4/5 ODI bootstrap CIs are degenerate. | **NOT RESOLVED** — see Ask 2. |
| **R3 Ask 2** Abstract CP-CI label for liberal | `main.tex:56` reads "liberal tolerance gave 0.19 (3/16; CI 0.04--0.46)" — still no "Clopper-Pearson" qualifier on the liberal CI in the abstract. (Same omission in Key Objective box at `main.tex:67`, but that box gives only the strict CI.) | **NOT RESOLVED** — see Ask 3. |
| **R3 Ask 3** Methods 2.7 S1/S2/S3 framing — all descriptive, no BH applied | `main.tex:110` still reads "S2 and S3 are reported descriptively because the small corpus precludes a meaningful Benjamini-Hochberg correction across three independent tests"; the wording still implies S1 was tested. | **NOT RESOLVED** — see Ask 4. |
| **R3 Ask 4** Post-hoc power statement (28% at p=0.40; n≈62 for 80%) | `discussion.tex:7-8` still gives only "k ≥ 8 needed to reject", no power figure. | **NOT RESOLVED** — see Ask 5. |
| **R3 Ask 5** IID-Bernoulli / cluster-structure acknowledgement | No text in Methods 2.7, no text in Discussion limitations. The clustering of G5/G6/G7/G13 under one upstream state is precisely the structure that violates the IID-Bernoulli assumption of the primary test, and three of these four are still evidence-free under strict. | **NOT RESOLVED** — see Ask 6. |
| **R3 Ask 6** Expand 15-node sensitivity interpretation | `main.tex:172` updated to include the liberal-tolerance 15-node value (0.20, CI 0.04--0.48, P=0.76) and confirms non-rejection. Inline-only; not a table. The interpretation ("the 15-node analysis is closer to prereg-as-written") is still implicit. | **PARTIAL** — minor improvement; acceptable for preprint. |
| **R3 Ask 7** Three tolerance levels = sensitivity grid, not 3 hypotheses | `main.tex:135` now reads "the three tolerance levels are reported as a pre-registered sensitivity grid, not as three independent confirmatory tests." `discussion.tex:14` echoes "reported as a sensitivity grid rather than three independent confirmatory tests." | **RESOLVED.** |
| **R3 Ask 8** Cite the two pre-registered stop rules and their non-triggering | No mention. | **NOT RESOLVED** — see Ask 7. |
| **R3 Ask 9** Quote the prereg commit short-hash inline | `main.tex:187` still reads "recorded in the repository's first commit." | **NOT RESOLVED** — see Ask 8. |
| **R3 Ask 10** ODI bootstrap uses same seed | Not stated in Methods 2.6 or 2.7. (The code at `06_compute_odi.py:66` does use seed 20260516.) | **NOT RESOLVED** — low priority. |
| **R3 Ask 11 (nit)** Bootstrap-EFDPR granularity 1/16 | Not stated. | **NOT RESOLVED** — low priority. |

**Net for Round 3:** Of 11 asks, **1 fully resolved** (Ask 7, sensitivity-grid framing — well done), **1 partially resolved** (Ask 6, 15-node sensitivity now includes liberal value), **9 unaddressed.** The two low-priority nits and Ask 6 are no longer blockers, but the cluster of unaddressed asks is now in its third unaddressed round (Ask 1 ODI CIs, Asks 5/6 IID/cluster acknowledgement, Asks 8/9 stop rules + commit hash, Ask 4 power).

---

## 4. Round 4 asks (≤ 8 concrete, in priority order)

### Ask 1 (HIGH — preprint blocker). Disclose the liberal-tolerance algorithm/data change between R3 (4/16) and R4 (3/16)

Add a bullet to `supplement.tex` Supplementary Text 1 (after the "Drug-class equivalence" bullet, ~line 156):

> **Liberal-tolerance count revised from 4/16 (R3) to 3/16 (R4).** Between the Round 3 and Round 4 internal review drafts, the count of evidence-free nodes under liberal tolerance decreased from 4 to 3 because [state the operational cause: e.g., "EMERALD's `subgroup_readouts` field was expanded to include the post-CDK4/6i ESR1mut readout, which under the liberal matcher converts G5 from evidence-free to supported"]. No change was made to the strict or ESCAT tolerance levels, the primary test, or the pre-registered threshold; the strict 5/16 result has been stable across all four review rounds.

The reader needs to know which of {trial coding, biomarker token, liberal matcher logic, guideline encoding} moved.

### Ask 2 (HIGH). Flag the degenerate ODI bootstrap CIs in Results 3.3 and add a table note

`tab_odi.tex` displays `[0.667, 0.667]`, `[0.333, 0.333]`, `[0.333, 0.333]`, `[0.200, 0.200]` as if they were intervals. They are not — for n_pairs ≤ 1 (HER2-low, ESR1mut, AKTpath) the bootstrap collapses to a point, and for PIK3CAmut (n_pairs=3) all three pairwise Jaccard distances are identical so the bootstrap collapses by a different mechanism.

Add to `main.tex` after line 152:

> "For four of the five biomarker variables (HER2-low, ESR1mut, AKTpath with one trial pair each; PIK3CAmut with three identical pairwise distances) the bootstrap CI collapses to the point estimate and no variance can be quantified at this sample size; the prior-CDK4/6i CI (0.76--1.00, 21 pairs) is the only informative ODI uncertainty interval in this pilot."

Add a footnote to `tab_odi.tex`:

> "CI collapses to point estimate when n_pairs ≤ 1 or when all pairwise distances are identical; variance is not estimable at this sample size."

### Ask 3 (MEDIUM). Abstract: name the liberal-tolerance CI type

`main.tex:56` — replace "(3/16; CI 0.04--0.46)" with "(3/16; Clopper-Pearson 95\% CI 0.04--0.46)". This was R2 Ask 1a and R3 Ask 2; closing it is a five-word edit.

### Ask 4 (MEDIUM). Methods 2.7 — tighten S1/S2/S3 framing

`main.tex:110` — replace:

> "Pre-registered secondary outcomes S1 (ODI), S2 (temporal evidence lag), and S3 (subgroup coverage) are reported in this manuscript; in the present pilot, S2 and S3 are reported descriptively because the small corpus precludes a meaningful Benjamini-Hochberg correction across three independent tests, a deviation that is disclosed here."

with:

> "Pre-registered secondary outcomes S1 (ODI), S2 (temporal evidence lag), and S3 (subgroup coverage) are all reported descriptively in this pilot: S1 as a per-biomarker mean pairwise Jaccard distance with bootstrap 95\% CI, and S2/S3 as summaries in Results 3.4. The pre-registered Benjamini-Hochberg adjustment at $q=0.05$ across the S1/S2/S3 family was therefore not applied; this deviation is disclosed in Supplementary Text 1."

### Ask 5 (MEDIUM). Add a quantitative power statement to Discussion

Reviewer-computed: at one-sided $\alpha=0.05$, critical $k^*=8$; power at p=0.30 is ~13\%, at p=0.40 ~28\%, at p=0.55 ~74\%. For 80\% power at p=0.40 one needs n≈62; for 80\% at p=0.30 one needs n≈174.

Add to `discussion.tex` after line 8:

> "At the pre-registration-expected alternative $p=0.40$ (midpoint of the [0.30, 0.55] prereg interval) the $n=16$ pilot has 28\% power at one-sided $\alpha=0.05$; reaching 80\% power at $p=0.40$ would require approximately 62 evidence nodes, and at $p=0.30$ approximately 174. The present non-rejection is therefore the expected outcome under a true EFDPR anywhere in the lower half of the prereg-expected range, and is consistent with — not contradictory to — a true positive effect."

### Ask 6 (MEDIUM). Acknowledge the IID-Bernoulli assumption and node clustering

The exact-binomial test and the percentile bootstrap (`05_compute_efdpr.py:175`) both assume the 16 nodes are exchangeable Bernoulli draws. G5/G6/G7/G13 share the post-CDK4/6i upstream state. Add to `main.tex:110` (after the bootstrap-seed sentence):

> "The exact-binomial test and percentile bootstrap both assume the per-node evidence-free indicators are independent Bernoulli draws. The 16 ESMO decision nodes are not strictly independent: G5, G6, G7, and G13 share the post-CDK4/6i upstream state and a shared evidence-vacuum mechanism. Positive within-cluster dependence reduces the effective sample size, so the one-sided exact-binomial test is conservative under positive dependence — that is, the non-rejection in this pilot is robust to (and is predicted by) the realistic dependence structure."

(One paragraph suffices; the production-scale extension can replace this with a cluster-bootstrap.)

### Ask 7 (LOW-MEDIUM). Cite the two pre-registered stop rules and their non-triggering

Add to `main.tex` after line 135:

> "The two pre-registered stop rules (refutation: 95\% CI upper bound below 0.25; clean null: point estimate below 0.10 with CI upper bound below 0.15) were both not triggered (CP upper bound 0.587 > 0.25 under strict; point estimate 0.31 > 0.10), so the prereg-mandated conclusion at this pilot scale is `neither rejected nor refuted; inconclusive,' matching the descriptive framing adopted throughout."

### Ask 8 (LOW). Quote the prereg commit short-hash

`main.tex:187` — replace "The pre-registration commit hash is recorded in the repository's first commit." with the actual seven-character short-hash, e.g.:

> "The pre-registration was committed prior to any outcome-touching analysis at commit \texttt{<7-char-hash>} (visible as the first commit of the repository linked in Code Availability)."

---

## Summary

| # | Ask | Priority | File / line |
|---|---|---|---|
| 1 | Disclose R3→R4 liberal-tolerance change (4/16 → 3/16) | **HIGH** | `supplement.tex` Supp Text 1 |
| 2 | Flag degenerate ODI bootstrap CIs (4/5 variables) | **HIGH** | `main.tex:152`, `tab_odi.tex` |
| 3 | Abstract: label liberal CI as Clopper-Pearson | MED | `main.tex:56` |
| 4 | Methods 2.7: S1/S2/S3 all descriptive, no BH applied | MED | `main.tex:110` |
| 5 | Discussion: quantitative power statement | MED | `discussion.tex:8` |
| 6 | Methods 2.7: IID-Bernoulli + node clustering + conservativeness | MED | `main.tex:110` |
| 7 | Cite the two pre-registered stop rules | LOW-MED | `main.tex:135` |
| 8 | Quote the prereg commit short-hash | LOW | `main.tex:187` |

**Numerical correctness:** every Round 4 headline reproduces to four decimal places (strict 5/16 → P=0.3698; liberal 3/16 → P=0.8029; 15-node strict 5/15 → P=0.3135). The framework, the pipeline, and the primary inferential conclusion are sound.

**Outstanding-asks footprint:** Ask 1 and Ask 2 are preprint-relevant (provenance disclosure of an inter-round numerical change; honest framing of CIs that have no variance). Asks 3--6 are tightening for a methods-flavoured paper. Asks 7--8 are cosmetic disclosure. None of these threaten the headline finding (non-rejection of the prereg primary test at strict tolerance, with descriptive identification of post-CDK4/6i evidence sparsity); Ask 1 in particular is a one-paragraph supplement edit, and Ask 2 is a one-sentence Results edit plus a table footnote.

For a preprint posting, Asks 1 and 2 should be closed; Asks 3--8 can be closed in a "v1.1" preprint update or carried into peer review. The repeated non-resolution of Asks 4, 5, 6, 7, 8 across three rounds is a process concern, not a science concern.

---

## VERDICT: MINOR
