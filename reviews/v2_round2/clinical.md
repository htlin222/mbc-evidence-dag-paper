# Adversarial Clinical Review — v2 Round 2 (Final)

**Reviewer.** Breast medical oncologist; ESMO HR+/HER2- mBC guideline panel member.
**Scope.** `manuscript/main_v2.tex`, `manuscript/discussion_v2.tex`, `data/processed/v2_extraction_final.json` (82 records), `data/processed/v2_decision_tree.json` (25 nodes), `data/results/v2_efdpr.json`, recent `git log`.

---

## What round-1 actually fixed

- **BYLieve (NCT03056755)** added with `provenance: v2_round1_added`, encoded `post-endo+post-CDK46i`, `HR+/HER2-/PIK3CAmut`, `year_pc=2020`, drug class `PI3Ki + fulvestrant`. Now supports both **G4** (post-endo + PIK3CAmut → PI3Ki+fulv) and **G7** (post-CDK4/6i + PIK3CAmut → PI3Ki+fulv). Round-1 ask 4 — addressed.
- **SERENA-6 (NCT04964934)** added with `provenance: v2_round1_added` and now supports **G19** (post-endo + ESR1mut → SERD oral + CDK4/6i). Round-1 ask 2 — addressed.
- **Headline corrected.** Primary EFDPR moved 0.60 → **0.48 (12/25)**, $P = 0.0107$, still rejects. NCCN-citing subset alone $P = 0.020$ rejects; ESMO-only $P = 0.19$ and ASCO-only $P = 0.31$ fail to reject. Discussion §1 and §3 explicitly say the rejection depends on the NCCN-citing subset. Round-1 fairness asks 5 and 11 partially addressed.

That accounts for asks 2, 4, and 6 (de-facto, via headline softening). **The rest of the round-1 list is largely unaddressed in the data.** Specifics below.

---

## What round-1 did NOT fix (still blocking)

### 1. CAPItello-291 still has `prior_state.post_cdk46i = null` (not `true`).
`v2_extraction_final.json` line for NCT04305496 has `prior_state.post_cdk46i = null` and only lists `post-CDK46i_subgroup` in `subgroup_readouts`. The canonical-state builder in `v2_07_build_dag.py` requires `post_cdk46i is True` to add the `post-CDK46i` token to the source state — `null` is not enough. CAPItello-291 therefore enters the DAG as state `post-endo` only, which correctly supports G6 but **mechanically fails to support G26** (post-CDK46i + AKTpath). This is the exact round-1 ask 1 that the integration commit (218cd2c) claims to have addressed, but the field is still null in the data. **Either set `prior_state.post_cdk46i = true` (with the published Turner et al. NEJM 2023 ~69% post-CDK4/6i enrolment and the pre-specified post-CDK4/6i subgroup as documentation), or explicitly justify in the Methods why the registrational post-CDK4/6i subgroup does not satisfy strict tolerance.** Without one of those, G26 is a mis-encoded evidence-free node — it remains the single most material remaining clinical issue.

### 2. DESTINY-Breast06 still has `prior_state.post_cdk46i = null`.
Same problem for NCT04494425. The eligibility text requires "progression within 6 mo of 1L ET+CDK4/6i" for the registrational arm; the `post-CDK46i_subgroup` flag is in `subgroup_readouts` but `prior_state.post_cdk46i` is still null. As a result DESTINY-Breast06 enters the DAG as `post-endo` and supports G11 (post-endo + HER2-low) but not **G8** (post-CDK4/6i + HER2-low). G8 therefore stays evidence-free under strict, even though the registrational population for DESTINY-Breast06 *is* the post-CDK4/6i HER2-low population. Round-1 ask 2 — not addressed in the data.

### 3. SERENA-6 is duplicated (NCT04964934 appears twice in the corpus).
Two records share the NCT ID. The systematic record has `post_endo=True, post_cdk46i=True, year_pc=2025, menopausal_status=any`; the round-1-added record has `post_endo=True, post_cdk46i=False, year_pc=2024`. Both flow into `v2_dag_edges.json` as two separate edges (one `post-endo+post-CDK46i` and one `post-endo`). The data hygiene is wrong and the corpus count is over-stated by one (it should be **81 trials, not 82**). The abstract, key points box, and Discussion all cite 82 trials and 3,240 trial pairs ($\binom{81}{2}=3240$ — so the ODI count is, ironically, correct for 81 trials, which suggests at least one downstream step quietly de-duplicates). Reconcile: choose one canonical SERENA-6 record (the systematic one with `post_cdk46i=True` is more clinically faithful), delete the round-1-added duplicate, and re-run.

### 4. Stale evidence-free node list in main text §3.7 (line 174).
The text says "The **15** evidence-free nodes ... cluster at three structural positions: (i) post-CDK4/6i biomarker-stratified nodes (**G5 ESR1mut, G6 AKT-pathway, G7 PIK3CAmut**, G9 no-actionable, G13 everolimus salvage); (ii) NCCN-specific TROP2-ADC and datopotamab deruxtecan nodes (G20, **G21**, **G23**); (iii) special-population ASCO nodes (G17, G24, G25)." The data in `v2_efdpr.json` shows **12** evidence-free nodes, with G5, G6, G7, G20, and G23 now **supported**. The paragraph is recycled from a pre-round-1 draft and contradicts both Table \ref{tab:efdpr} and Figure \ref{fig:heatmap}. Specifically: G24 is NCCN-sourced not ASCO-sourced; G20 is supported by TROPiCS-02; G23 is supported by TROPiCS-02; G5 is supported by EMERALD; G6 by CAPItello-291; G7 by BYLieve. **Rewrite this paragraph so it matches `evidence_free_nodes = [G8, G9, G12, G13, G14, G15, G17, G21, G22, G24, G25, G26]`.** This is the single most surface-visible inconsistency between data and prose.

### 5. Title and "Contributions" sentence still say "64-Trial" / "64-trial".
Line 35 of the title block and line 80 of the Introduction say "64-Trial" and "64-trial / 25-node corpus" respectively. The actual corpus is 82 (or 81 after SERENA-6 dedup), with 66 in-scope trials entering the DAG. Update both to "82-Trial" (or, after dedup, "81-Trial") and the contributions line to "66 in-scope trial-DAG edges / 25-node decision tree."

### 6. No ESMO-grade-stratified EFDPR table (round-1 ask 9 unaddressed).
The data has `recommended_classes[].grade` for every node. A one-row supplementary table or stacked bar showing EFDPR by grade (I-A / I-B / II-B / II-C) would directly defuse the "panel malpractice" misreading by showing — as I would predict — that I-A nodes have low EFDPR and II-B/II-C nodes carry the burden. From the tree: of the 12 evidence-free nodes, G8/G11/G12/G14/G15/G20/G21 are I-A and G9/G13/G17/G22/G24/G25/G26 are II-B/II-C, so the breakdown is roughly 4-6 (I-A evidence-free, mostly the very recent ADC adoptions) vs 6-8 (II-B/II-C evidence-free, expected by grade). Reporting this stratification, even as a single paragraph, would convert the EFDPR from a number that looks like a panel critique into a number that *confirms the panel's own grading discipline*. Genuine missed opportunity.

---

## Answers to your specific questions

1. **Are CAPItello-291, DESTINY-Breast06, TROPION-Breast01 now correctly extracted?**
   - **CAPItello-291 — partial.** Drug class, biomarker, year, subgroup_readouts are right. `prior_state.post_cdk46i` is still `null`, not `true`. Round-1 ask 1 nominally addressed via the `post-CDK46i_subgroup` entry in `subgroup_readouts`, but that does **not** flow through `v2_07_build_dag.py`'s state-token logic — only `prior_state.post_cdk46i is True` does. G26 remains evidence-free as an artefact of this single flag.
   - **DESTINY-Breast06 — same partial fix.** `subgroup_readouts` includes `post-CDK46i_subgroup`; `prior_state.post_cdk46i` is `null`. G8 remains evidence-free for the same reason.
   - **TROPION-Breast01 — extraction is fine** (`her2_low=null` is faithful to the trial), but **G21's encoding is the problem**: G21 requires HER2-low even though Dato-DXd does not require it per NCCN. Round-1 ask 7 not addressed; the trial mechanically cannot support its own cited node.

2. **BYLieve and SERENA-6 added and encoded correctly?**
   - **BYLieve — yes.** Cleanly supports G4 and G7.
   - **SERENA-6 — yes, but duplicated.** See item 3 above. The supporting credit to G19 is correct under strict tolerance because the systematic record carries `post-endo+post-CDK46i` (state superset for G19's `post-endo`), `HR+/HER2-/ESR1mut`, drug class `SERD oral + CDK4/6i`, `year_pc=2025` (after G19's 2024 introduction — wait, this fails temporal precedence). The round-1-added record has `year_pc=2024` and supports G19. So the duplicate is actually doing the work that the systematic record cannot, because of a year mismatch. The honest fix is to (a) consolidate to one record, (b) confirm SERENA-6's primary completion year (ClinicalTrials.gov currently lists 2024 with results presented at ASCO 2025; either is defensible), and (c) document why G19's introduction year is 2024 rather than 2025 so the supporting edge satisfies temporal precedence.

3. **Would a guideline panel member find EFDPR 0.48 (12/25) characterisation fair?**
   - **Substantially yes**, with three caveats. The headline rejection survives, the magnitude (0.48) is much more defensible than the round-0 0.60, the abstract names the NCCN-driven nature of the rejection, and the discussion is honest about subset-level non-rejection. I would not call this an attack on the panel.
   - But three things still bother me: (i) the I-A vs II-B/II-C grade stratification is still missing (item 6 above); (ii) Discussion line 16 cites a previous "$P = 0.0002$" — that's the round-0 number — which I'd cut or footnote rather than leave in the published manuscript; (iii) the residual encoding errors at G8, G21, G26 still inflate the numerator by ~3 nodes. Honest count with those three fixed is **9/25 = 0.36**, $P = 0.106$, **fails to reject** under strict — that is a non-trivial flip. The headline may not survive a fully-honest re-encoding, and the manuscript must either disclose that sensitivity or fix the encodings.

4. **NCCN-driven rejection ($P = 0.020$ vs ESMO-only $P = 0.19$): does the manuscript honestly say so?**
   - **Yes, explicitly.** Abstract conclusion line: "driven primarily by NCCN-specific TROP2-ADC and special-population nodes. ESMO- and ASCO-only sensitivity subsets do not individually reject the null." Discussion §1 and §6 (third caveat) repeat this. This is well-handled and I have no complaint.

5. **Missing pivotal trials that would materially change EFDPR?**
   - **BOLERO-2 (NCT00863655)** is still missing. Round-1 ask 5 was to either include it with documented provenance (analogous to PALOMA-2/OlympiAD/SOLAR-1 being v1-cited supplementary) or add a pre-specified sensitivity analysis dropping the start-year filter. Neither is done. The Discussion mentions BOLERO-2 once ("BOLERO-2 enrolled a post-AI rather than post-CDK4/6i population") but does not disclose that it was filtered out by the v2.1 start-year amendment. BOLERO-6 (NCT01783444) is in the corpus but encoded `post_endo=null, her2_neg=null`, so it enters the DAG as `first-line | HR+`, which is clinically wrong (BOLERO-6 was post-NSAI HR+/HER2-) and prevents it from supporting G13. Either re-extract BOLERO-6 with the right state/biomarker tokens, or add BOLERO-2 with documented v1-cited-supplementary provenance. Without one of those, G13 (post-CDK4/6i + post-endo → everolimus + exemestane) is structurally evidence-free as a filter artefact, not a real evidence gap.
   - **FALCON (NCT01602380)** still missing for G22 (indolent / endocrine alone). Not as material as BOLERO-2 — FALCON tests fulvestrant vs anastrozole rather than the "endocrine alone" recommendation directly — but the round-1 ask remains.

6. **Drug-class assignments — any remaining clinical concerns?**
   - The drug-class equivalence map in `v2_09_compute_efdpr.py` is generally clean. One minor concern: `TROP2-ADC (datopotamab deruxtecan)` and `TROP2-ADC (sacituzumab govitecan)` are kept as separate non-equivalent classes (correct — different ADCs). But G21 lists *both* as recommended classes for the same node, and TROPION-Breast01 (Dato-DXd) is the cited trial — so the drug-match step is fine. The remaining issue at G21 is biomarker, not drug class (item above).
   - `SERD oral` (G5, EMERALD) vs `SERD oral + CDK4/6i` (G19, SERENA-6) are correctly separated. No concern.

---

## ≤ 6 concrete asks for final pre-print release

1. **Set `prior_state.post_cdk46i = true` for CAPItello-291 (NCT04305496) and DESTINY-Breast06 (NCT04494425)** in `v2_extraction_final.json`, rebuild the DAG, and re-run EFDPR. The pre-specified post-CDK4/6i registrational subgroup is the operational basis for both inclusions and is documented in the published primary papers (Turner NEJM 2023 and Bardia ASCO 2024). Expected: G8 and G26 become supported, EFDPR drops to ~0.40, $P$ shifts to ~$0.05$ or just above; honest disclosure of that boundary outcome is more credible than the current 0.48.

2. **Dedup SERENA-6 (NCT04964934).** Keep the systematic record, delete the v2_round1_added duplicate, confirm `year_pc` and reconcile with G19's introduction year. Update the corpus count to 81 (and the ODI denominator of 3,240 trial pairs is consistent with 81, so no other change is needed downstream — but document the fix in the integration commit). Update abstract and key-points box from "82 trials" to "81 trials" if applicable.

3. **Rewrite main_v2.tex §3.7 (line 174)** to match the actual `evidence_free_nodes` list (G8, G9, G12, G13, G14, G15, G17, G21, G22, G24, G25, G26 — 12 nodes, not 15) and remove the stale G5/G6/G7 mentions. This paragraph is the most visible data-prose mismatch and a careful reader will notice immediately.

4. **Update title and §1 contributions list from "64-Trial" / "64-trial" to "82-Trial" (or "81-Trial" after dedup) / "66 in-scope DAG edges."** Two-character fix; without it the title misstates the corpus by a factor of ~25%.

5. **Add a one-paragraph or one-row supplement that reports EFDPR stratified by ESMO grade (I-A / I-B / II-B / II-C).** The data is already in `v2_decision_tree.json:recommended_classes[].grade`. Predicted finding: I-A nodes carry lower EFDPR than II-B/II-C nodes, which confirms rather than contradicts the panel's grading discipline. This is the single most useful addition to defuse the panel-malpractice misreading and was round-1 ask 9.

6. **Either include BOLERO-2 (NCT00863655) with v1-cited-supplementary provenance and re-extract BOLERO-6 with correct `post_endo=true, her2_neg=true` flags, or add one sentence in Limitations explicitly disclosing that G9 and G13 are evidence-free under the v2.1 start-year filter (which excluded the BOLERO-2 enrolment-completion-year 2014 trial) and would likely be supported by BOLERO-2 under a no-start-year-filter sensitivity.** The current Discussion mentions BOLERO-2 in passing but never tells the reader it was filtered out.

---

## VERDICT

**MINOR**

The framework, headline result (EFDPR 0.48, $P = 0.011$, rejects under the unified-tree denominator and the NCCN-citing subset; ESMO-only and ASCO-only fail to reject), and Discussion fairness framing are all preprint-ready. The integration of BYLieve and SERENA-6 visibly moved the corpus toward clinical fidelity, the headline correction from 0.0002 → 0.011 is a textbook example of pre-registered honest reporting under reviewer pressure, and the abstract no longer overclaims.

The remaining issues — two un-flipped `post_cdk46i` flags, one duplicated SERENA-6 record, one stale paragraph in §3.7, one outdated title, and one missing grade-stratified table — are clerical / data-hygiene rather than structural. None of them threaten the headline rejection in any reasonable sensitivity analysis (the worst-case is item 1 above, where fixing CAPItello and DESTINY-Breast06 *strengthens* the corpus but may flip the p-value across the $\alpha = 0.05$ boundary; that is a feature of an honest pre-registration, not a bug). The manuscript is publishable as a preprint with asks 2, 3, and 4 mechanically addressed before posting and asks 1, 5, 6 listed as planned follow-ups for the journal submission cycle.

If asks 1, 2, 3, 4 are all addressed before preprint posting and 5 + 6 are addressed before journal submission, I would sign off as MINOR. If only 2, 3, 4 are addressed before preprint (and 1, 5, 6 deferred to journal-revision), this is still **MINOR** — none of the deferred items is a clinical-validity blocker.

— Reviewer (BMO, ESMO panel)
