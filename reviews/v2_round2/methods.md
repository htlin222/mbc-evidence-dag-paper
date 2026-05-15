# v2 Round 2 Methods Review

**Reviewer role:** adversarial methods reviewer (final-round verification of R1 integration).
**Target journal:** JCO Clinical Cancer Informatics (Original Report).
**Materials reviewed:** `manuscript/main_v2.tex`, `manuscript/discussion_v2.tex`, `manuscript/supplement_v2.tex`, `analysis/v2_06_adjudication.py`, `data/processed/v2_extraction_final.json`, `data/results/v2_efdpr.json`, `data/results/v2_kappa_postadj.json`, `git log` (commit `218cd2c` integration of R1 asks on top of `9a12001`).

Many of the Round 1 honesty asks are visibly integrated — the κ gate is now framed as failing under Cohen's κ and passing under PABAK; the four R1 NCT/data fixes (BYLieve added, SERENA-6 NCT corrected, CAPItello-291 + DESTINY-Breast06 post-CDK4/6i subgroup flags, TROPION-Breast01 HER2-low) are all present in `v2_extraction_final.json`; the primary test runs at $P = 0.011$ on the corrected corpus and the abstract / KO box / Results §3.3 / Discussion headline now report "12 evidence-free / 25 nodes" consistently. The supplement Table S2 reports both Cohen's κ and PABAK side-by-side and Supplementary Text 1 itemises the v2 deviations. However, **non-trivial honesty defects remain** in (a) the post-adjudication κ methodology (still circular; not disclosed), (b) the adjudication code's SERENA-4 / SERENA-6 rationale, (c) the corpus arithmetic, (d) the stale "15 evidence-free" / "G5 evidence-free" atlas paragraph, and (e) the title / intro / cohort-table count strings. Each is a small fix; together they are enough to block "preprint-ready."

---

## Check-by-check verdict

### Check 1 — Cohen's κ gate honestly framed as FAIL (akt_path), PABAK passes.
PARTIAL PASS. The abstract (line 53), Results §3.1 (line 114), supplement S2 note (line 86), supplement deviations bullet 4 (line 101), and Discussion caveat 2 (line 16) all now report "$\kappa = 0.00$ on akt_path due to the kappa paradox" and "under PABAK the gate passes." This matches Round 1 ask #1. **Residual issue (minor):** the supplement deviation bullet still reads "post-adjudication all fields pass under PABAK but akt_path still fails Cohen's κ" — this is true, but should also acknowledge that *pre-adjudication* the Cohen's κ gate ALSO failed on `post_endo` ($\kappa = 0.40$) and three other fields below 0.70 (hr_pos 0.64, her2_neg 0.65, post_cdk46i 0.67). The supplement S2 table does show the per-field pre-κ figures, so the data are visible, but the prose framing minimises the breadth of the pre-adjudication shortfall.

### Check 2 — Post-adjudication κ honestly framed as construction, not independent re-rating.
**FAIL.** `analysis/v2_06_adjudication.py:101-107` still writes the same adjudicated value `val` into BOTH `adjudicated_A` and `adjudicated_B` arrays for every disagreement, and the post-κ is then computed on those two arrays (lines 138-141). By construction this forces post-κ = 1.00 on every disagreed-on field, which is exactly the circularity Round 1 ask #11 flagged. The manuscript Methods §2.3 (line 91), Results §3.1 (line 114: "post-adjudication Cohen's κ on key fields was 1.00 for seven of eight fields") and the supplement Table S2 all present the post-κ as if it were an independent inter-rater measurement after the adjudication discipline closed the gap. The code's docstring (`v2_06_adjudication.py:5-9`) and the comment at line 99-100 ("Adjudication updates both annotators to the consensus value (modelling 'annotators re-read the protocol with the rationale and converge')") frame the construction as a model of convergence, but the manuscript does not disclose this to the reader. The reader is left to infer that post-κ = 1.00 measures agreement quality; in fact it measures only that the same patch list was applied to both arrays. This is the single largest residual honesty defect.

### Check 3 — Four R1 NCT/data fixes present in `v2_extraction_final.json`.
PASS, with one duplicate-row hygiene issue. Verified:
- BYLieve `NCT03056755` present at line 2718 with `provenance: v2_round1_added`, `prior_state.post_cdk46i=true`, `biomarker.pik3ca_mut=true`, `drug_class: PI3Ki + fulvestrant`.
- SERENA-6 `NCT04964934` (the corrected ID) present at line 2740 with `provenance: v2_round1_added`. **However**, the original SERENA-6 record (also `NCT04964934`) from the systematic search remains at line 1899 with a different coding (`post_cdk46i=true`, `year_pc=2025`, `subgroup_readouts: [ESR1mut]`); the round-1-added duplicate at line 2740 codes `post_cdk46i=false`, `year_pc=2024`, `subgroup_readouts: []`. There are two records with the same NCT ID and conflicting field values in the released extraction. The downstream `v2_efdpr.json` uses NCT04964934 for G19 support — but which record? This is a reproducibility bug.
- CAPItello-291 `NCT04305496` line 1556: `subgroup_readouts` now contains `AKTpath` and `post-CDK46i_subgroup`; ✓.
- DESTINY-Breast06 `NCT04494425` line 1591: `subgroup_readouts` now contains `HER2-low`, `HER2-ultralow`, and `post-CDK46i_subgroup`; ✓.
- TROPION-Breast01 `NCT05104866` line 2002: `subgroup_readouts: [HER2-low_subgroup]`; ✓.

### Check 4 — "12 evidence-free / 25 nodes" headline consistent.
PARTIAL FAIL. The abstract (line 53), KO box (line 64), Results §3.3 (line 134), and Discussion headline (lines 4, 10) all say "0.48 (12/25)." **However:**
- Results §3.7 (line 174) reads "The 15 evidence-free nodes under strict concordance are distributed across the guideline tree..." — the count is wrong (the data show 12, not 15).
- The same paragraph lists G5 (ESR1mut) as evidence-free under strict, but `v2_efdpr.json` shows G5 supported by NCT03778931 under strict (the discussion §"Where the gap is largest" correctly says BYLieve and SERENA-6 now rescue G5/G7). The §3.7 atlas paragraph appears to be uncorrected v2-round-0 text — it mentions five evidence-free post-CDK4/6i biomarker nodes (G5, G6, G7, G9, G13) when only G9 and G13 are evidence-free post-correction. The discussion paragraph and the atlas paragraph contradict each other and only one matches the data.
- Methods §2.8 says "ASCO-citing (15)" — the supplement `v2_tab_cohort.tex` line 7 also says 15. The `v2_efdpr.json` `sensitivity_asco` block reports `n_nodes: 15`. Consistent.

### Check 5 — Supplement discloses ALL Round 1 deviations.
PARTIAL PASS. Supplementary Text 1 lists: BYLieve+SERENA-6 added; three extraction fixes; 17 not 14 adjudication rules; Cohen κ gate fail; S2/S3 descriptive; E1 promoted from exploratory; G6 state coding retained; NCT-label correction. **Missing disclosures:**
- The post-adjudication κ is computed by writing the consensus into both annotator arrays (Check 2 above). This is the single most important deviation to disclose and is not in the list.
- The corpus arithmetic decomposition (16 excluded = 1 OOS-only + 11 OOS∩Inv + 4 Inv-only) is not stated anywhere; the manuscript still says "16 trials were either out-of-scope (HER2-positive, TNBC, adjuvant) or investigational-class" (main_v2 line 117), preserving the disjoint-sets implication Round 1 ask #16 flagged.
- Round 1 ask #5 (state-superset rule prose vs code) and ask #6 (justify the three special tokens) are not addressed in the supplement; the Methods §2.6 prose is unchanged from v2 round-0.

### Check 6 — Corpus arithmetic 16 = 12 oos ∪ 4 inv with documented intersection.
**FAIL.** I verified the underlying numbers from `v2_extraction_final.json`:
- 82 trials total; 66 in DAG; 16 excluded.
- 12 trials have "out of scope" in `notes`; 15 trials have `drug_class` starting with `investigational`.
- Intersection (OOS AND Inv) = 11.
- Union = 16 (matches the 82 − 66 excluded count).
- Decomposition: 1 OOS-only, 11 OOS∩Inv, 4 Inv-only.

The manuscript and supplement still report this as "16 trials were either out-of-scope or investigational-class" without the intersection. The "12 oos ∪ 4 inv" framing in the verification brief is also incorrect (4 is the Inv-only count, but 12 is the OOS-total which double-counts the 11-trial intersection). The correct statement is one of:
- "16 excluded = 1 out-of-scope-only + 11 out-of-scope-and-investigational + 4 investigational-only."
- "12 trials out-of-scope (HER2+/TNBC/adjuvant, of which 11 also investigational); 4 additional trials investigational drug class only; 16 unique excluded."

---

## Other defects newly introduced or still standing

- **Manuscript title (line 36)** still reads "A 64-Trial, Pre-Registered Graph-Theoretic Analysis." The corpus is now 82 trials with 66 in-DAG. The Methods §2.2 explicitly says 80 → 82 → 66. The title should be either "82-Trial" or "66-Trial (in-DAG)" depending on which the author considers the headline. The 64-trial number was the v2-round-0 value before the BYLieve+SERENA-6 additions and is no longer correct.
- **Intro line 80** says "a pre-registered confirmatory test of EFDPR exceeding 0.25 with a 64-trial / 25-node corpus, and (iv) ... across the full 80-trial corpus." Two stale counts in one sentence.
- **Figure 3 caption (line 162)** says "on the 80-trial corpus" — should be 82. The ODI value 0.641 / 3,240 pairs reported elsewhere implies 82 trials (3,240 = 81 × 80 / 2), confirming the caption is stale.
- **Cohort table `v2_tab_cohort.tex` line 3** labels "Pivotal HR+/HER2- mBC trials (frozen 2026-05-16) & 66" — but the corpus is 82 with 66 in-DAG. The label conflates "corpus size" with "in-DAG edges."
- **Figure 1 caption (line 122)** still reads "labelled G1--G26" — the tree has 25 nodes because G18 was dropped during construction (Round 1 ask #19 flagged this and the user's verification brief includes the equivalent). Either renumber or footnote the skip.
- **`v2_06_adjudication.py:43-44`** still has the broken rationale "SERENA-6 (camizestrant + CDK4/6i): switch within first-line CDK4/6i after ESR1mut emergence; not 'post-CDK4/6i' in the prereg sense (still on first-line)" attached to `NCT04711252` (which is SERENA-4, not SERENA-6). Round 1 ask #7 explicitly called this out. The supplement now mentions an "NCT-label correction" but the load-bearing code still has the wrong trial name in the rationale string. A skeptical reviewer reading the adjudication source will conclude the bug is unfixed in code and patched only in prose.

---

## Concrete asks (≤ 6)

1. **Disclose the post-adjudication κ construction.** Add one sentence to Methods §2.3 and one row to Supplement Text 1's deviations list: "Post-adjudication, the consensus value from each adjudication rule is written into both annotator arrays before recomputing κ; the resulting post-adjudication κ is therefore 1.00 by construction on every disagreed-on field and should be read as a sanity check that the adjudication was applied symmetrically, not as an independent re-measurement of inter-rater agreement. The substantive inter-rater quality of the v2 corpus is the pre-adjudication κ in Supplementary Table S2." Alternatively, refactor `v2_06_adjudication.py` so post-κ is computed as (adjudicated consensus) vs (original Codex) — this would give a meaningful "how much did adjudication move Codex" number — but the disclosure-only path is acceptable if the journal does not require a re-run.

2. **Fix the SERENA-4 / SERENA-6 rationale in `analysis/v2_06_adjudication.py:43-44`.** The current text describes SERENA-6 but is attached to NCT04711252 (SERENA-4). Rewrite to "SERENA-4 (camizestrant + palbociclib, 1L): no prior CDK4/6i; first-line by design" and confirm the adjudicated value is correct for SERENA-4. This is the same class of NCT/label bug Round 1 ask #7 flagged. Also de-duplicate `NCT04964934` in `v2_extraction_final.json` (two records with conflicting `post_cdk46i`, `year_pc`, `subgroup_readouts`) and document which record `v2_efdpr.json` consumed.

3. **Fix the stale evidence-free atlas paragraph in main_v2.tex §3.7 (line 174).** Replace "The 15 evidence-free nodes" with "The 12 evidence-free nodes" and remove G5, G6, G7 from the post-CDK4/6i list (per the corrected data, only G9 and G13 are evidence-free in that bucket post-BYLieve/TROPION-Breast01 corrections; G6 AKT-pathway is now supported by CAPItello-291 per `v2_efdpr.json`). Cross-check against `data/results/v2_efdpr.json["primary"]["strict"]["evidence_free_nodes"]` which lists exactly G8, G9, G12, G13, G14, G15, G17, G21, G22, G24, G25, G26.

4. **Document the 16-excluded-trial decomposition.** In Results §3.2 or supplement S3, replace "the remaining 16 trials were either out-of-scope ... or investigational-class" with "16 excluded from concordance: 1 out-of-scope-only, 11 out-of-scope and investigational, 4 investigational-class only (`drug_class` = `investigational (other)` with in-scope HR+/HER2- mBC population). Union = 12 ∪ 15 = 16 with 11-trial intersection." Verified numbers: 12 OOS notes, 15 investigational drug_class, 11 intersection, 16 union.

5. **Refresh the stale "64-trial" / "80-trial" count strings to the post-correction 82 / 66 numbers** in: title (line 36), intro contribution (iii) and (iv) at line 80, Figure 3 caption (line 162), and the `v2_tab_cohort.tex` line-3 label ("Pivotal HR+/HER2- mBC trials" should say "82" not "66" if it means corpus size; if it means in-DAG, relabel as "Pivotal trials with canonical drug-class assignments (in-DAG)"). Pick one canonical headline (82 corpus or 66 in-DAG) and use it consistently.

6. **Expand the supplement Text 1 deviations list** to additionally disclose: (a) the post-adjudication κ construction (Ask 1 above); (b) the corpus 16-trial decomposition (Ask 4); (c) that the Methods §2.6 prose "satisfied by any state" is implemented in `v2_09_compute_efdpr.py:_state_match` by stripping `metastatic`/`indolent`/`visceral-crisis` from the guideline-side token set (i.e., guideline node states become weaker rather than trial states becoming stronger; the practical effect is that an empty guideline-state set is a subset of every trial-state set — a sensitivity analysis with the special-token treatment turned off would be a low-cost honesty add). Round 1 asks #5 and #6 are otherwise unaddressed.

---

## VERDICT: MAJOR

The R1 integration commit `218cd2c` is a substantive honesty improvement — the four NCT/data fixes are in the extraction file, the primary EFDPR has been recomputed honestly on the corrected corpus (P = 0.011 not P = 0.0002), and the kappa gate is now reported as "fails under Cohen's κ on akt_path, passes under PABAK." But four R1-class defects survived the integration: (1) the post-adjudication κ is still computed by writing the same value into both annotator arrays and is therefore mechanically 1.00 — the manuscript does not disclose this; (2) `v2_06_adjudication.py` still attaches a SERENA-6 rationale to a SERENA-4 NCT ID; (3) the Results §3.7 evidence-free atlas paragraph still says "15 evidence-free nodes" and still lists G5/G6/G7 as evidence-free, contradicting the corrected data; (4) the corpus arithmetic still suppresses the 11-trial OOS∩Inv intersection. Together with three stale count strings (64-trial title, 80-trial figure caption, 64-trial intro), these are enough to block "preprint-ready." Each is a small fix; none requires re-running the pipeline. With Ask 1-6 above addressed, the next round should be ACCEPT.
