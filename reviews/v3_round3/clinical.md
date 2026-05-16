# Adversarial Clinical Review — v3 Round 3

**Reviewer.** Thoracic + breast medical oncologist; ESMO/ASCO guideline panel member (HR+/HER2- mBC and EGFR/ALK NSCLC).
**Scope.** Verification of v3 Round-2 integration (commit `dadf797`, "sweep 14 stale numbers + regen figures + sync cover letters + sync medRxiv kit") against the 12 clinical concerns in `reviews/v3_round2/clinical.md`. Files audited: `manuscript/paper_A_clinical_v3.tex`, `manuscript/paper_B_methods_v3.tex`, `manuscript/paper_A_clinical_v3.docx`, `release/submission_kit_paperB_medrxiv/paper_B_methods.docx`, `release/RELEASE_NOTES_v3.0.0.md`, `release/submission_plan_paperA_jcopo/AUDIT_REPORT.md`, `release/submission_plan_paperA_jcopo/POLISH_PLAN_14_DAYS.md`, `release/submission_kit_paperB_medrxiv/AUDIT_REPORT.md`, `analysis/v3_07_build_combined_dag.py`, `analysis/v3_08_compute_pooled_efdpr.py`, `analysis/v3_09_figures.py`, `data/processed/v3_nsclc_full.json`, `data/processed/v3_nsclc_decision_tree.json`, `data/processed/v3_combined_dag_edges.json`, `data/results/v3_pooled_efdpr.json`, and the three v3 figure PDFs (`figures/v3_fig{1_forest,2_per_node,3_trajectory}.pdf`) by `pdftotext`.

**Bottom line.** R2-integration commit `dadf797` is a much narrower delivery than the commit message advertises. It updated **9 lines of Paper A.tex** and synced two cover letters / one medRxiv metadata sheet. It did **NOT** sweep Paper B at all, it did **NOT** regenerate the figures (the figure script `v3_09_figures.py` still hard-codes pre-R1 numbers — `n=50`, `n=8` ALK, `P = 0.0004`, EFDPR `[0.31, 0.40, 0.48]`, `pvals=[0.37, 0.071, 0.0004]` at L142-143 — and the rendered PDFs still display "P = 0.0004", "50-node guideline tree", "Sensitivity: NSCLC ALK-only (n=8)", "Sensitivity: NSCLC-only (n=25)", EFDPR `0.48` for v3, `P < 0.001`), it did **NOT** address any R2 functional asks (B1 brain-mets, B2 TROPION-N9, B3 ALTA-1L temporal-precedence, B4 SAVANNAH), and it did **NOT** update `release/RELEASE_NOTES_v3.0.0.md` (still says "EFDPR 0.48, P=0.0004, 261 trials, NSCLC EGFR-only 0.71 P=0.0001"). The TROPION-Lung01 hand-curated record did get `egfr_mut=true` set (one of two B2 sub-fixes), but `prior_state.post_osimertinib` is still `null` and the trial's DAG edge therefore still has `source_state="post-chemo"` (not `"post-osimertinib+post-chemo"`); **N9 remains evidence-free at every tolerance**. The R2 commit message claim "TROPION egfr_mut=True fix" is technically true but functionally inert — it did not move the needle on the cited node it was supposed to fix. Paper A still has at least eight publication-blocking stale numbers; Paper B's source `.tex` is **entirely unchanged since R1** and ships stale `(180 trials, 145 in-scope)`, `(24/50 → 17/50; P=0.10)`, and `n = 50`; the regenerated Paper B `.docx` propagates the same stale content. The cover letters were updated to `P = 0.023`; that is the only fully-delivered R2 ask in this review's scope.

---

## A. R2 clinical-ask verification (12 asks the user listed)

### A1. R2 ask #1 — Fix Paper A figure captions for Figs 1, 3 ($P=0.0004 \to 0.023$; "50-node" $\to$ "49-node"); fix the trajectory figure's $-\log_{10} P$ axis label. **PARTIALLY: captions updated in `.tex`; figures themselves UNCHANGED.**

The figure captions in `paper_A_clinical_v3.tex` are now correct at L100 (`P = 0.023`, "primary 49-node analysis") and L110 (`P = 0.023`, "($-\log_{10} P = 3.4$)") — but **the rendered figures still display pre-R1 numbers**:

| Figure | Rendered title / labels (per `pdftotext`) | Should be |
|---|---|---|
| `figures/v3_fig1_forest.pdf` | "Pooled mBC + NSCLC EFDPR — pre-registered primary test rejects H₀ (**P = 0.0004**)"; row labels "Primary: pooled mBC + NSCLC (**n=50**)", "Sensitivity: NSCLC-only (**n=25**)" (actual n=24), "Sensitivity: NSCLC ALK-only (**n=8**)" (actual n=7) | n=49 / P=0.023; n=24; n=7 |
| `figures/v3_fig2_per_node.pdf` | "Per-node trial-edge support across pooled **50-node** guideline tree" | "49-node" |
| `figures/v3_fig3_trajectory.pdf` | v3 EFDPR datapoint = **0.48** (label visible); v3 P = **P < 0.001** | 0.39; P = 0.0231 |

This is mechanical: `analysis/v3_09_figures.py` L44 hard-codes `"Primary: pooled mBC + NSCLC (n=50)"`, L46 `"Sensitivity: NSCLC-only (n=25)"`, L48 `"Sensitivity: NSCLC ALK-only (n=8)"`, L83 title `"... rejects H₀ (P = 0.0004)"`, L121 `"... pooled 50-node guideline tree"`, L141 `"v3.0.0\nmBC+NSCLC pooled\n(n=50)"`, and **L142-143 hard-code `efdprs = [0.31, 0.40, 0.48]` and `pvals = [0.37, 0.071, 0.0004]`** — none of these were edited by `dadf797`, and the local figures still have these values (PDF content hashes confirm the binary is different from the pre-R2 commit, so SOMEONE re-ran the script, but the script's hard-coded inputs are still the pre-R1 inputs). The trajectory caption now claims `-\log_{10} P = 3.4` for $P = 0.023$, but $-\log_{10} 0.023 = 1.64$, not 3.4 — so even after the partial edit, the caption now contradicts itself. **A journal copy-editor will catch this in 30 seconds; a careful reviewer will lose confidence in the QC pipeline.**

R2 ask #1 is **NOT closed**.

### A2. R2 ask #2 — Discussion headline numbers in Paper A. **PARTIALLY: headline $P = 0.0004 \to 0.023$ done (L133); "24 evidence-free decision nodes" $\to$ "19" done (L142). BUT "12 of 17 EGFR evidence-free" NOT FIXED (L136); "$P=0.63$" NOT FIXED (L139); "$P = 0.10$" in Three caveats NOT FIXED (L145).**

Paper A line 136: "**Of 17 EGFR-mutant decision nodes, 12 are evidence-free at strict tolerance.**" — the per-node JSON gives `nsclc_egfr_only.strict.evidence_free_count = 7`, `n_nodes = 17`. The "12 of 17" is the pre-R1 buggy figure (0.71 inflated). Post-R1 honest figure is 7/17 (0.41). **This is the single most-cited number in the Discussion and is unchanged.**

Paper A line 139: "ALK-rearranged decisions, by contrast, were the only sensitivity subset that failed to reject (**$P = 0.63$**)". Actual `nsclc_alk_only.strict.exact_p_one_sided_vs_p25 = 0.5551`. The abstract correctly cites $P = 0.56$; the Discussion contradicts the abstract.

Paper A line 145: "First, ESCAT-aligned and liberal tolerance gave **$P = 0.10$** on the pooled denominator." Actual is $P = 0.0836$ (the abstract correctly cites $P = 0.084$). The Discussion contradicts the abstract on a number the same paragraph is highlighting.

R2 ask #2 is **PARTIALLY closed**; three of the four sub-fixes are still stale.

### A3. R2 ask #3 — Paper A Methods stale counts (L81, L87, L90, L151). **PARTIALLY: L87 (`24 nodes; 17 EGFR / 7 ALK`), L90 (`212 edges`, `48 canonical source nodes`), L151 (`259-trial pooled corpus`) done. BUT L81 "**145** in-scope" NOT FIXED (actual 147 per `jq '[.[]|select(.tumor=="NSCLC")] | length' data/processed/v3_combined_dag_edges.json` = 147). L90 "50-node pooled denominator" NOT FIXED (should be 49). L73 (Intro) "$n = 50$" NOT FIXED (should be 49).**

L81 reads: "brought the final NSCLC corpus to **178 trials**, of which **145** entered the in-scope trial-DAG." The first number is right; the second is wrong (actual 147). The +2 is exactly PAPILLON and TROPION-Lung01 re-routed in R1, both of which the manuscript later cites at L71. The R2 sweep replaced "180" with "178" but missed the in-scope count.

L73 (Introduction): "pools the two-tumor decision-tree denominator to **$n = 50$**". Actual pooled $n = 49$.

L90: "The pooled EFDPR is computed on the **50-node** pooled denominator". Should be 49-node.

R2 ask #3 is **PARTIALLY closed**.

### A4. R2 ask #4 — Brain-mets de-stripping (B1). **NOT addressed. N20 and N22 still evidence-free at every tolerance.**

Per the per-node JSON, `N20 = []` and `N22 = []` under strict, ESCAT, AND liberal tolerance. FLAURA (NCT02296125) and ALEX (NCT02075840) both have `subgroup_readouts = []` and `subgroup_readouts = ["egfr_ex19del", "egfr_l858r"]` respectively — neither carries any brain-mets-specific token. The `_bm_match_liberal` matcher at `v3_08_compute_pooled_efdpr.py:74-86` does not consume `subgroup_readouts` for state matching (it only adds them to `e_set | sub_set` for biomarker matching), so the half-implementation in R1 is still half. ALK-only stratified strict `evidence_free_nodes = ["N19", "N20"]` confirms N20 is one of the two ALK strict evidence-free flags (the other is N19, post-ALK + ALK-resistance-mut). NSCLC EGFR-only stratified strict `evidence_free_nodes = ["N9", "N10", "N12", "N21", "N22", "N23", "N24"]` confirms N22 contributes 1 of the 7 EGFR strict evidence-free flags. R2 ask #4 was the most consequential functional fix in R2's list and is **NOT addressed**.

### A5. R2 ask #5 — TROPION-Lung01 N9 fix (A3/B2). **PARTIALLY: `biomarker.egfr_mut = true` done. BUT `prior_state.post_osimertinib` still `null` and the subgroup token format unchanged. N9 remains evidence-free at every tolerance.**

Per `jq '.[]|select(.nct_id=="NCT04656652")' data/processed/v3_nsclc_full.json`:

```
"prior_state": {"post_egfr_tki": null, "post_osimertinib": null, "post_chemo_metastatic_min": 1, ...}
"biomarker": {"egfr_mut": true, ..., "tumor_type": "NSCLC-EGFR"}
"subgroup_readouts": ["non-actionable_subgroup", "actionable_genomic_alteration_subgroup", "EGFR-mut_subgroup"]
```

In the DAG edge: `source_state = "post-chemo"`, `biomarker = "EGFR-mut/NSCLC"`. N9's `state = "post-osimertinib+post-chemo"` requires `{post-osimertinib, post-chemo} \subseteq edge.state`. TROPION's edge state is `{post-chemo}`, which fails the state-superset check (`v3_07_build_combined_dag.py:22-25` only emits the `post-osimertinib` token when both `post_egfr_tki=True` AND `post_osimertinib=True`; TROPION has both `null`). So under strict and ESCAT, N9's state-match fails before biomarker is even checked. Under liberal, state-match also fails (the matcher does not strip `post-osimertinib` from the guideline state). Result: `N9 = []` strict/escat/liberal.

The R2 commit's claim of fixing TROPION is technically true (`egfr_mut=true` is set) but functionally inert (N9 is not supported). **A clinician reading Paper A line 136 sees "TROP2-ADC (TROPION-Lung01)" cited as a post-osimertinib example, but the framework's own concordance algorithm does not credit TROPION with supporting N9.** The R2 reviewer's exact prescription was (in `reviews/v3_round2/clinical.md:154`): "Set `biomarker.egfr_mut=true` and `prior_state.post_osimertinib=true` on the TROPION record, and either change the subgroup token from `EGFR-mut_subgroup` to `EGFR-mut` (so the liberal matcher resolves it) or change the liberal matcher to strip the `_subgroup` suffix when comparing." Only the first half of the first sentence was done.

R2 ask #5 is **NOT functionally closed**.

### A6. R2 ask #6 — N13 ALTA-1L temporal-precedence (B3/A4). **NOT addressed. N13 still cites both ALEX and ALTA-1L but supports only ALEX + ASCEND-4; ALTA-1L silently expelled by year_pc=2020 > year=2017.**

Per `jq '.[]|select(.node_id=="N13")' data/processed/v3_nsclc_decision_tree.json`:

```
"node_id": "N13", "state": "first-line", "biomarker": "ALK-rearranged/NSCLC",
"cited_trials": ["NCT02075840", "NCT02737501"], "year": 2017
```

Per `jq '.[]|select(.nct_id=="NCT02737501")' data/processed/v3_nsclc_full.json`:

```
"trial_name": "ALTA-1L", "year_pc": 2020, "drug_class": "ALK TKI 2nd-gen (...)", ...
```

Per `jq '.primary.strict.per_node_support.N13' data/results/v3_pooled_efdpr.json`:

```
["NCT01828099", "NCT02075840"]   ← ASCEND-4 + ALEX; ALTA-1L absent
```

The `supports()` function at `v3_08_compute_pooled_efdpr.py:148-154` enforces `int(edge["year_pc"]) > int(gl["year"])` rejection. ALTA-1L `year_pc=2020 > N13.year=2017`, so ALTA-1L fails temporal precedence even though every other criterion matches. **The node cites it but the framework expels it.** The R2 ask was (in `clinical.md:156`): "either (a) move `year=2017` $\to$ `year=2020` (admits ALTA-1L into the support set; clinically defensible because the '2nd-gen alectinib/brigatinib/ceritinib/ensartinib' 1L recommendation took its current form by 2020 with the ALTA-1L OS update), or (b) drop NCT02737501 from `cited_trials` and keep year=2017 (citation honesty)." Neither was done.

R2 ask #6 is **NOT addressed**.

### A7. R2 ask #7 — SAVANNAH / MET-amp salvage (B4). **NOT addressed. N21 still evidence-free at every tolerance; the dead-code drug-class equivalence entries (`"MET-TKI + osimertinib"`, `"EGFR TKI mutant-selective (ex20ins)"`) remain in `DRUG_CLASS_EQUIVALENCE` with no trial using them.**

SAVANNAH (`NCT03778229`) per the current full corpus: `drug_class = "investigational (other)"`, `egfr_mut = true`, `post_osimertinib = true`, and no `met_amplification` biomarker field. Stripped from DAG by `v3_07_build_combined_dag.py:95-96`. N21 (`post-osimertinib / EGFR-mut/MET-amp/NSCLC`) cannot be supported by any trial under any tolerance:

```
jq '.primary.strict.per_node_support.N21'      → []
jq '.primary.escat.per_node_support.N21'       → []
jq '.primary.liberal.per_node_support.N21'     → []
```

Three NSCLC-EGFR nodes remain mechanical strict-evidence-free flags (N12, N21, N23) for exactly the reasons documented in R1 and R2. R2 ask #7 is **NOT addressed**.

### A8. R2 ask #8 — Cluster prose (Paper A L118, abstract L50). **NOT addressed. The Paper A "evidence-free cluster" lists at L118 still name N7, N8, N11, and N25 as evidence-free.**

Per `jq '.primary.strict.per_node_support'`: `N7 = ["NCT04988295"]` (MARIPOSA-2, supported), `N8 = ["NCT04619004"]` (HERTHENA-Lung01, supported), `N11 = ["NCT04538664"]` (PAPILLON, supported), `N25 = ["NCT04035486"]` (FLAURA2, supported). Paper A line 118: "(i) NSCLC post-osimertinib (**N7** amivantamab+chemo, **N8** HER3-ADC, N9 TROP2-ADC, N10 platinum-doublet salvage, N21 MET-amp salvage, N23 post-amivantamab, N24 post-osi+post-chemo); (ii) NSCLC EGFR-mut alternative or special-population positions (N5 anti-VEGF+TKI, **N11** EGFR ex20ins 1L, N12 EGFR ex20ins post-chemo, **N25** high-risk subgroup)". **Four of the listed "evidence-free" nodes are actually supported** under strict. The honest evidence-free NSCLC list (per `evidence_free_nodes`) is N9, N10, N12, N19, N20, N21, N22, N23, N24 (9 nodes). The cluster prose inflates the evidence-free count by 4 in prose while the abstract correctly says 19. A reviewer cross-checking L118 against the per-node figure will conclude the prose is wrong.

R2 ask #8 is **NOT addressed**.

### A9. R2 ask #9 — Paper B line 130 stale arithmetic (C4). **NOT addressed. Paper B.tex is entirely unchanged since R1.**

`paper_B_methods_v3.tex` L130 still reads: "ESCAT-aligned and liberal tolerance gave 0.34 (**24/50 $\to$ 17/50; $P = 0.10$**), failing to reject." Actual: ESCAT/liberal = 0.3469 = 17/49 (not 17/50); $P = 0.0836$ (not 0.10); the "24/50 $\to$ 17/50" implies a strict-of-24 that was true in pre-R1 (matching the pre-R1 buggy strict EFDPR 0.48 × 50 = 24) but is wrong post-R1 (strict = 19/49). The whole sentence is a pre-R1 fossil. Paper B L124 also still says "**180 trials (145 in-scope)**" (R1's stale figures, not even R2's "178 trials (145 in-scope)" intermediate). Paper B L127 correctly says "49-node decision tree (25 mBC + 24 NSCLC)" (this part was R1's L127 fix) but L147 still says "$n = 50$ nodes". The regenerated `paper_B_methods_v3.docx` (which `dadf797` did update) propagates these stale numbers verbatim: `python3 -c "import zipfile,re; z=zipfile.ZipFile('manuscript/paper_B_methods_v3.docx'); print(re.sub(r'<[^>]+>','',z.open('word/document.xml').read().decode()))" | grep -E "180 trials|145 in-scope|24/50"` returns all three. **The R2 commit message claims paper B was synced; in fact only the docx render of the unchanged tex was updated.** The same applies to the medRxiv submission kit copy `release/submission_kit_paperB_medrxiv/paper_B_methods.docx` (contains "180 trials", "145 in-scope", "24/50", "17/50").

R2 ask #9 is **NOT addressed**.

### A10. R2 ask #10 — Re-class FL-ALTER (B5). **NOT addressed.**

`jq '.[]|select(.nct_id=="NCT04028778") | .drug_class' data/processed/v3_nsclc_full.json` returns `"Bevacizumab + EGFR TKI"`. Anlotinib is a multikinase VEGFR-TKI; the class is materially mis-applied. N5 strict-supports `["NCT02411448" (RELAY), "NCT04028778" (FL-ALTER)]` — and "supported" on the strength of one correctly-classed trial (RELAY) and one mis-classed trial (FL-ALTER). R2 ask #10 is **NOT addressed**.

### A11. R2 ask #11 — Rename `"EGFR TKI 3rd-gen (osimertinib)"` to `"EGFR TKI 3rd-gen"` and document the failed-development 3rd-gen TKIs (B6). **NOT addressed.**

`v3_08_compute_pooled_efdpr.py:117` still has `"EGFR TKI 3rd-gen (osimertinib)": {"EGFR TKI 3rd-gen (osimertinib)"}`. The corpus still encodes nazartinib (NCT02108964), TIGER-1 (NCT02186301), and SOLAR/ASP8273 (NCT02588261) with class `"EGFR TKI 3rd-gen (osimertinib)"`. N1's strict supports remain `["NCT02108964", "NCT02186301", "NCT02296125", "NCT02588261"]` — three failed-development 3rd-gen TKIs plus FLAURA. The class name still misleads. No Methods footnote was added.

R2 ask #11 is **NOT addressed**.

### A12. R2 ask #12 — Document the N13/N14 merge in Methods. **NOT addressed.**

Paper A Methods §"NSCLC guideline decision-tree encoding" (L87, now updated to "24 nodes ... 17 EGFR, 7 ALK") does not explain why ALK is 7 not 8. A reader who inherits the tree will have no documentation that N13 and N14 were merged in R1. Paper B does not document this either. The R2 ask was for one sentence in Methods or Supplement; absent.

R2 ask #12 is **NOT addressed**.

---

## B. NEW issues introduced or surfaced by R2

### B1. The figure script (`analysis/v3_09_figures.py`) is a stale-data landmine. **CRITICAL.**

The script hard-codes pre-R1 numbers throughout: titles (`L83: "P = 0.0004"`), row labels (`L44: "(n=50)"`, `L46: "(n=25)"` for NSCLC, `L48: "(n=8)"` for ALK), trajectory inputs (`L142: efdprs = [0.31, 0.40, 0.48]`, `L143: pvals = [0.37, 0.071, 0.0004]`). The R2 commit did not touch this file (`git show dadf797 --stat` confirms). Anyone running `uv run python analysis/v3_09_figures.py` per the release-notes reproduction recipe (line 82) will get pre-R1 figures. The PDFs in the repo (which `dadf797` did re-commit) are inconsistent with the script — meaning the reproduction recipe in `RELEASE_NOTES_v3.0.0.md` does NOT regenerate the committed figures. **This breaks reproducibility, which is the framework's signature claim.**

### B2. `release/RELEASE_NOTES_v3.0.0.md` is the GitHub release page and is entirely pre-R1. **PUBLICATION-BLOCKING for the release surface.**

L9: "On a pooled **50-node** ESMO+ASCO+NCCN decision tree (25 mBC HR+/HER2- + **25 NSCLC** EGFR/ALK) against a **210-edge** trial-DAG from **261** systematically-searched pivotal trials" — every number wrong.
L11-12: "**EFDPR = 0.48** (Clopper-Pearson 95% CI **0.34--0.63**); ... REJECTS at α = 0.05 (**P = 0.0004**)" — every number wrong.
L16-18: "NSCLC-only (n=25): EFDPR **0.56**, **P = 0.0009**; NSCLC EGFR-only (n=17): EFDPR **0.71**, **P = 0.0001** (strongly rejects); NSCLC ALK-only (n=8): EFDPR **0.25**, P = 0.63" — every number wrong (actual: 0.38 P=0.12; 0.41 P=0.11; 0.29 P=0.56).
L26: trajectory table v3.0.0 row: "EFDPR **0.48**, P **0.0004**" — wrong.
L47: prereg trail row: "v3 pooled analysis: REJECT H₀ at **P=0.0004**" — wrong.
L61: "Strict-tolerance test rejects (P=0.0004) but ESCAT-aligned and liberal tolerance give P=0.10" — both numbers wrong.

The release page is **what GitHub users see first**. R2 did not touch it. Anyone clicking the `v3.0.0` release tag will see numbers that flatly contradict the current abstract and the cover letters. This is worse than R2-A1 (figure captions) because it is the public-facing release surface and there is no abstract on the page to compare against.

### B3. `release/submission_plan_paperA_jcopo/AUDIT_REPORT.md` and `POLISH_PLAN_14_DAYS.md` are pre-R1 fossils. **MAJOR for editor pre-submission QA.**

`AUDIT_REPORT.md` L15: "Headline result (**P=0.0004 REJECT**) | ✅ | Consistently throughout" — wrong twice (the number and the assertion of consistency).
`POLISH_PLAN_14_DAYS.md` L73: "Confirm all P-values to 4 decimal places consistent across abstract/KO box/results/discussion (**P=0.0004** throughout)" — the polish-plan itself instructs the editor to consistently use the pre-R1 number; a careful editor following this plan would re-introduce the bug.
`POLISH_PLAN_14_DAYS.md` L76: "Add one sentence to Limitations about the ESCAT/liberal **P=0.10** explicitly" — wrong number.
`POLISH_PLAN_14_DAYS.md` L81: "Table S2: per-trial structured-extraction excerpts (NSCLC + mBC, **n=261**)" — wrong (n=259).
`POLISH_PLAN_14_DAYS.md` L82: "Table S3: per-node ESMO/ASCO/NCCN decision tree (**n=50**)" — wrong (n=49).

These files were not touched by R2 even though the R2 commit message says "sync cover letters" — the submission-plan documents that the editor will read alongside the cover letter are not synced.

### B4. The "honest 0.71 → 0.41 correction" disclosure paragraph (R2 editor ask) is still absent from the Discussion. **MAJOR for transparency.**

The R2 editor reviewer (`reviews/v3_round2/editor.md:175-194`) explicitly asked for a one-paragraph disclosure in Paper A Discussion §"Three caveats" (L145) acknowledging the R1 bug-fix trajectory: "An internal round-1 adversarial review identified six encoding bugs that materially changed the result numbers (pre-fix pooled EFDPR 0.48, P=0.0004; post-fix 0.39, P=0.023; EGFR-only pre-fix 0.71, post-fix 0.41)." This paragraph was not added. The Paper A Discussion contains no acknowledgement that the pre-R1 cover-letter and release-notes numbers (which are still publicly visible on the v3.0.0 release page) are wrong. Without this disclosure, a reviewer cross-checking the manuscript abstract ($P = 0.023$) against the public release page ($P = 0.0004$) will assume carelessness rather than transparency. This is a clinical-credibility issue, not just an editorial one: the framework's load-bearing claim is "pre-registered, auditable, reproducible"; failing to acknowledge a 0.48 $\to$ 0.39 / 0.71 $\to$ 0.41 in-house correction undermines all three claims.

### B5. The R2-sweep commit's diff is misleadingly small (9 tex lines + 4 cover-letter / metadata lines) vs the commit message ("sweep 14 stale numbers"). **MINOR but indicative.**

`git show dadf797 --stat`: 22 files changed, 674 insertions, 19 deletions. The 674 insertions are almost entirely from the three round-2 review files added to the repo (`clinical.md` 201 lines, `editor.md` 373 lines, `methods.md` 81 lines = 655). The actual fix delta is 9 paper_A.tex lines, ~6 cover-letter lines, ~6 medrxiv metadata lines, and the regenerated docx/pdf binaries. **The commit message overstates the scope of the fix by a factor of ~3.** R2's clinical ask list was 12 items; only items 1-3 were even partially attempted, and only the cover-letter / metadata items were fully done. A future reviewer or editor reading the commit log will assume "R2 integration" means "12 clinical asks were processed"; it does not.

---

## C. Per-node strict evidence-free audit vs paper claims

Quote of `data/results/v3_pooled_efdpr.json` `primary.strict.evidence_free_nodes`:

```
["G9", "G12", "G13", "G14", "G15", "G17", "G21", "G22", "G24", "G25",
 "N9", "N10", "N12", "N19", "N20", "N21", "N22", "N23", "N24"]
```

Count = 19. Pooled EFDPR = 19/49 = 0.388. (Matches abstract.)

NSCLC strict evidence-free subset = `[N9, N10, N12, N19, N20, N21, N22, N23, N24]` = 9 nodes. NSCLC-only EFDPR = 9/24 = 0.375. (Matches.)

NSCLC EGFR-only evidence-free = `[N9, N10, N12, N21, N22, N23, N24]` = 7. EFDPR 7/17 = 0.412. (Matches abstract.)

NSCLC ALK-only evidence-free = `[N19, N20]` = 2. EFDPR 2/7 = 0.286. (Matches.)

**Comparison to Paper A prose:**

- Discussion L136 says "**12** of 17 EGFR-mutant nodes evidence-free" — should be **7**. STALE.
- Discussion L139 says ALK "$P = 0.63$" — should be **0.56**. STALE.
- Discussion L142 says "**19** evidence-free decision nodes" — CORRECT.
- Results L118 cluster (i): "N7, N8, N9, N10, N21, N23, N24" — N7, N8 are NOT evidence-free. Honest post-osi cluster is N9, N10 (post-chemo placeholder), N21, N23, N24.
- Results L118 cluster (ii): "N5, N11, N12, N25" — N5, N11, N25 are NOT evidence-free. Honest ex20ins/special cluster is N12, plus N20/N22 brain-mets and N19 ALK-post-everything.
- Results L118 cluster (iii) mBC: "G9, G13, G14, G17, G22/G24, G25, G21" — should also include G12, G15 (per the strict evidence-free list). The mBC count in the prose is 9 nodes; the actual mBC evidence-free count is 10.

The cluster-prose is the load-bearing paragraph for "where is the gap"; it is materially wrong.

**Comparison to the cover-letter claim:** the JCO PO cover letter (correctly updated) says "the evidence gap is concentrated at NSCLC EGFR-mutant post-osimertinib decision nodes (HER3-ADC, TROP2-ADC, MET+osimertinib positions)" — HER3-ADC = N8 is supported. The cover-letter list is also subtly wrong on the same item the abstract and Discussion are wrong on. R2 fixed the cover-letter $P$-value but not the cluster phrasing.

---

## D. Concrete asks (8)

The R2 integration commit closed almost nothing on the clinical-review side. Rather than re-list the 12 unresolved R2 asks (which are documented above as still-open), I list the 8 highest-priority items for v3 round-3 integration:

### D1. **REGENERATE THE FIGURES FROM REAL DATA.** Rewrite `analysis/v3_09_figures.py` to read every number from `data/results/v3_pooled_efdpr.json` instead of hard-coding pre-R1 constants. At minimum: L44/46/48 row labels must use `EFDPR["primary"]["n_nodes"]`, etc.; L83 title must use the actual primary `exact_p_one_sided_vs_p25`; L121 must use the actual node total; L142-143 trajectory must read v1, v2, v3 from their respective result JSONs (or at minimum update the v3 hardcoded values to `[0.31, 0.40, 0.39]` and `[0.37, 0.071, 0.0231]`). Then re-run and commit the resulting PDFs. **This is the single most publication-blocking item** — the abstract says $P = 0.023$ and Figure 1 says $P = 0.0004$.

### D2. **REWRITE `release/RELEASE_NOTES_v3.0.0.md` END-TO-END.** Every headline number on the public release page is pre-R1 (0.48, 0.0004, 261 trials, 50 nodes, 210 edges, EGFR 0.71 P=0.0001, NSCLC-only 0.56 P=0.0009). This is the surface a journal editor lands on if they Google the GitHub repo. R2 did not touch it. Replace with the post-R1 numbers and add a one-line note: "v3.0.0 release was tagged before R1 bug-fix integration; current canonical numbers are EFDPR 0.39, P = 0.023, 259 trials, 49 nodes, 212 edges (R1 commit `4ff3cdd`, R2 commit `dadf797`). Pre-R1 numbers preserved in `release/RELEASE_NOTES_v3.0.0_pre_R1.md` for audit trail."

### D3. **FIX PAPER B (`paper_B_methods_v3.tex`).** R2 left this entirely unchanged. Specific lines:
- L124: "180 trials (145 in-scope)" $\to$ "178 trials (147 in-scope)".
- L130: "0.34 (24/50 $\to$ 17/50; $P = 0.10$)" $\to$ "0.35 (19/49 $\to$ 17/49; $P = 0.084$)".
- L147: "$n = 50$ nodes" $\to$ "$n = 49$ nodes".
- Re-render `paper_B_methods_v3.docx` and `release/submission_kit_paperB_medrxiv/paper_B_methods.docx` from the updated source.

### D4. **FIX THE THREE PAPER A STALE NUMBERS THAT R2 MISSED.**
- L73 (Intro): "$n = 50$" $\to$ "$n = 49$".
- L81 (Methods): "145 in-scope" $\to$ "147 in-scope".
- L90 (Methods): "50-node pooled denominator" $\to$ "49-node pooled denominator".
- L136 (Discussion): "Of 17 EGFR-mutant decision nodes, **12** are evidence-free" $\to$ "**7** are evidence-free" (and adjust the sentence's "post-osimertinib is the largest concentrated gap" framing to reflect 7/17 = 0.41 vs ALK 0.29, a 1.4x ratio not 3x).
- L139 (Discussion): "$P = 0.63$" $\to$ "$P = 0.56$".
- L145 (Three caveats): "$P = 0.10$" $\to$ "$P = 0.084$".

### D5. **FIX THE CLUSTER PROSE AT PAPER A L118.** Drop N7, N8, N11, N25 from the "evidence-free cluster" lists (all four are supported). Add G12, G15 to the mBC cluster (omitted from prose). Honest post-osi-EGFR cluster: N9 (TROP2-ADC), N10 (platinum salvage placeholder), N21 (MET+osi), N23 (post-amivantamab), N24 (post-osi+post-chemo). Honest 1L/special-EGFR cluster: N5 (anti-VEGF+TKI, conditional on B5/D8), N12 (ex20ins post-chemo), N20 (brain-mets ALK), N22 (brain-mets EGFR), N19 (post-everything ALK). The mBC cluster is approximately right but should match the strict `evidence_free_nodes` list exactly (G9, G12, G13, G14, G15, G17, G21, G22, G24, G25).

### D6. **DO ONE OF THE THREE FUNCTIONAL R2 FIXES THAT WERE PUNTED.** Choose one and execute end-to-end, not as a partial code-touch:
- **(a) TROPION-N9 (R2-A5/B2)**: set `prior_state.post_osimertinib=true` AND change subgroup token from `"EGFR-mut_subgroup"` to `"EGFR-mut"` (so liberal matcher resolves it). Then N9 should support under liberal at minimum. OR honestly remove TROPION-Lung01 from the Discussion L136 post-osi example list and state N9 is evidence-free.
- **(b) ALTA-1L-N13 (R2-A6/B3)**: move N13.year=2017 $\to$ 2020 (admits ALTA-1L; clinically defensible per the 2020 OS update) OR drop NCT02737501 from `cited_trials`. The current "citation but no support" is silently inconsistent.
- **(c) Brain-mets-N20/N22 (R2-A4/B1)**: add `"brain_mets_subgroup"` to FLAURA / ALEX / ALTA-1L / CROWN `subgroup_readouts` AND extend `_state_match` (liberal tolerance only) to strip `brain-mets` from the guideline state when any candidate trial has the brain-mets subgroup readout. OR drop N20 and N22 from the tree with a Methods footnote. OR explicitly disclose in Methods that N20/N22 are deliberately evidence-free because no NSCLC pivotal trial has a brain-mets-explicit registrational readout.

If none of the three is done in R3 integration, at minimum add a one-paragraph "known limitations of the current encoding" sub-section to Paper A Limitations or to the Supplement listing these three node-level encoding choices and their consequences for the per-node interpretation. **The pooled headline ($P = 0.023$) is robust to all three fixes** (any of them either keeps an evidence-free flag in place or reduces the count by one), so this is honesty work, not headline work.

### D7. **ADD THE R1-CORRECTION TRANSPARENCY PARAGRAPH** (R2-editor-A4, still unaddressed). One paragraph in Paper A Discussion §"Three caveats" (L145), e.g.:

> An internal round-1 adversarial review identified six encoding bugs that materially changed the result numbers between the v3.0.0 release tag and the current canonical analysis: pooled strict EFDPR moved from 0.48 to 0.39 ($P = 0.0004 \to 0.023$), and the NSCLC EGFR-only sensitivity from 0.71 to 0.41 ($P = 0.0001 \to 0.11$, no longer individually rejecting). Both corrections preserve the pre-registered pooled-denominator rejection; the strict-EGFR-vs-strict-ALK contrast becomes 1.4$\times$ rather than 3$\times$, and the "post-osimertinib is the largest concentrated gap" framing is preserved at the structural level (5 of 7 post-osimertinib EGFR sub-nodes remain strict-evidence-free) but the magnitude is honest. The pre-R1 numbers are preserved in the v3.0.0 release tag for audit-trail completeness. The fix-trajectory commits are `4ff3cdd` (R1 integration) and `dadf797` (R2 integration); reviewer logs are in `reviews/v3_round{1,2,3}/`.

Without this paragraph, the manuscript and the publicly-visible release page tell two different stories.

### D8. **SYNC THE TWO STALE SUBMISSION-PLAN DOCS** (`release/submission_plan_paperA_jcopo/AUDIT_REPORT.md`, `POLISH_PLAN_14_DAYS.md`, `release/submission_kit_paperB_medrxiv/AUDIT_REPORT.md`). The polish-plan currently instructs the editor to use $P = 0.0004$ and $n = 261$ "consistently throughout." An editor following the plan would re-introduce the bugs that R1 and R2 are supposedly fixing. Either delete these documents or update them to reflect the post-R1/R2 canonical numbers.

---

## E. What R2 did well (for completeness, brief)

- The two cover letters (`release/submission_kit_paperB_medrxiv/cover_letter_medrxiv.md` L14, `release/submission_plan_paperA_jcopo/cover_letter_jcopo_draft.md` L18) and the medRxiv metadata sheet (L19) are correctly updated to $P = 0.023$, EFDPR 0.39, 259 trials, 49-node tree. This was the right priority for a journal-submission desk-screen surface.
- Paper A.tex got 9 fixes: abstract was already correct from R1; R2 fixed the two figure captions ($P = 0.023$), three Methods numbers (`178 trials`, `24 nodes / 17 EGFR / 7 ALK`, `212 edges / 147 NSCLC / 48 source nodes`, `259-trial pooled corpus`), and the Discussion headline ($P = 0.023$, "19 evidence-free decision nodes"). Six tex lines flipped from pre-R1 to canonical; the other ~12 stale references in the same file were missed.
- The TROPION-Lung01 record got `biomarker.egfr_mut = true` set (one of the two-line fixes the R2 reviewer prescribed). This is real progress even though N9 still does not support — the other line (`prior_state.post_osimertinib = true`) is missing.

---

## VERDICT

**MAJOR REVISION.**

R2 was advertised as a "bulk sweep" of 14 stale numbers. In fact it was a narrow 9-line edit to Paper A.tex plus three cover-letter / metadata updates, plus one half-fix to the TROPION record (`egfr_mut=true` without `post_osimertinib=true`). It claimed to regenerate figures and sync Paper B; it did neither (the figure script is unchanged and still hard-codes $P = 0.0004$; Paper B.tex is unchanged; the regenerated Paper B.docx propagates the stale tex verbatim). **All six functional R2 asks (B1 brain-mets, B2 TROPION-N9, B3 ALTA-1L, B4 SAVANNAH, B5 FL-ALTER, B6 3rd-gen TKI rename) are unaddressed.** **Eight of the twelve R2 clinical asks are unaddressed or only partially addressed.** The public-facing release page `release/RELEASE_NOTES_v3.0.0.md` still reports the pre-R1 numbers (EFDPR 0.48, $P = 0.0004$, 261 trials, EGFR-only 0.71 $P = 0.0001$) — anyone who reads the release page before the abstract will conclude the submission is internally inconsistent.

**The single most publication-blocking item is the figure / figure-script disconnect.** The three v3 figures still display "$P = 0.0004$", "n=50", "ALK-only (n=8)", trajectory EFDPR `0.48`. The abstract says "$P = 0.023$", "n = 49", "ALK-only n=7", trajectory EFDPR `0.39`. A journal editor scanning Figure 1 will conclude the submission has not been QC'd; a reviewer cross-checking the abstract against Figure 3 will find a 24x discrepancy in $P$-value ($0.023 / 0.001 \approx 23$). The figure script `v3_09_figures.py` hard-codes all the wrong numbers; until the script is rewritten to read from the result JSON (D1), every figure regen will re-introduce the bug.

**The three functional items the R2 reviewer prescribed (TROPION-N9, ALTA-1L-N13, brain-mets-N20/N22) are pending.** None of them changes the pooled headline (which rejects regardless), but all three are clinician-facing per-node interpretation errors that the framework's own concordance algorithm produces. A thoracic oncologist reading Paper A Discussion L136 sees TROPION-Lung01 cited as a post-osimertinib example for a node (N9) that the framework reports as evidence-free; the framework and the prose contradict each other. Either fix at least one of the three (D6), or honestly disclose the per-node encoding limitation.

I would re-review a v3 round-3-integration revision that addresses **D1 (figure regen, blocking), D2 (release notes, blocking), D3 (Paper B sweep, blocking), D4 (six remaining Paper A stale numbers, blocking), and D5 (cluster prose, blocking)** at minimum. I would not block on D6 (functional R2 punts), D7 (R1-correction disclosure paragraph), or D8 (submission-plan docs), but they should be addressed before journal submission — D7 especially, because the public release page will continue to show pre-R1 numbers until D2 is done, and an editor cross-checking the release page against the abstract will notice the gap.

The framework is sound and the post-R1 numbers are honest. The manuscript and release infrastructure have not been re-pulled to match. The R2 integration commit was a step in the right direction but a small step; R3 needs to finish the sweep, regenerate the figures from real data, and address at least one of the three pending functional items.

— Reviewer (Thoracic + Breast MO, ESMO/ASCO panel)
