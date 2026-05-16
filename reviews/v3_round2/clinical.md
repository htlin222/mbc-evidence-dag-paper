# Adversarial Clinical Review — v3 Round 2

**Reviewer.** Thoracic + breast medical oncologist; ESMO/ASCO guideline panel member (HR+/HER2- mBC and EGFR/ALK NSCLC).
**Scope.** Verification of v3 Round-1 integration (commit `4ff3cdd`) against the 12 clinical concerns in `reviews/v3_round1/clinical.md`. Files audited: `manuscript/paper_A_clinical_v3.tex`, `manuscript/paper_B_methods_v3.tex`, `data/processed/v3_nsclc_decision_tree.json`, `data/processed/v3_nsclc_full.json`, `data/processed/v3_combined_dag_edges.json`, `data/results/v3_pooled_efdpr.json`, `analysis/v3_07_build_combined_dag.py`, `analysis/v3_08_compute_pooled_efdpr.py`.

**Bottom line.** R1 commit `4ff3cdd` cleanly fixed three structural items (strict→superset, PAPILLON corpus addition, N13/N14 merge) and three encoding items (N1 token, NSCLC trial \citep'ing, strict matcher rewrite), and the headline numbers (pooled EFDPR 0.39 strict, $P=0.023$ REJECT; NSCLC-EGFR 0.41 vs ALK 0.29) are now derivable from the artifacts. **But six R1 asks were not addressed (4, 5, 6, 9, 10, 12)**, two R1 fixes introduced new clinical issues (TROPION-Lung01 still cannot support N9; brain-mets de-stripping silently dropped FLAURA and ALEX from their own brain-mets nodes), and **multiple paragraphs of Paper A still carry pre-R1 stale numbers ($P=0.0004$ in two figure captions and the Discussion headline; "12 of 17 EGFR evidence-free" in Discussion; "24 evidence-free decision nodes" in the committee-implications paragraph; "180 trials / 145 in-scope" in Methods; "210 edges (145 NSCLC + 65 mBC)" in Methods; "12 nodes cover EGFR-mutant" in Methods; "261-trial pooled corpus" in Limitations)**. The R1 fixes are real and the numbers run end-to-end; the manuscript prose was not fully re-written to match.

---

## A. R1-ask verification (8 asks the user listed for explicit verification)

### A1. Strict matching is SUPERSET — does FLAURA support N1? **YES, verified.**

`v3_08_compute_pooled_efdpr.py:44-54` defines `_bm_match_strict` as `_bm_tokens(g).issubset(_bm_tokens(e))` (trial-side superset of guideline). N1's `cited_trials = ["NCT02296125"]` (FLAURA) and the `v3_pooled_efdpr.json` strict per-node block reports `"N1": ["NCT02108964", "NCT02186301", "NCT02296125", "NCT02588261"]` — FLAURA is now supporting N1 at every tolerance. **Verified.** The corollary that R1 ask #12 asked about (the three other supporters are nazartinib/rociletinib/naquotinib, three failed-development 3rd-gen TKIs co-classed as `"EGFR TKI 3rd-gen (osimertinib)"`) is unchanged — see B5 below.

### A2. PAPILLON added — does it support N11? **YES, verified.**

`data/processed/v3_nsclc_full.json` now contains NCT04538664 PAPILLON with `egfr_mut=true, egfr_ex20ins=true, drug_class="Amivantamab + chemotherapy", year_pc=2023, guideline_target_node="first-line|EGFR-ex20ins|NSCLC", provenance="nsclc_v3_round1_added"`. The DAG edge resolves to `source_state="first-line", biomarker="EGFR-mut/EGFR-ex20ins/NSCLC"`. N11 (`first-line / EGFR-ex20ins/NSCLC / Amivantamab + chemotherapy / year 2024`) supports via PAPILLON under strict superset (g={EGFR-ex20ins, NSCLC} ⊆ e={EGFR-mut, EGFR-ex20ins, NSCLC}) and temporal precedence (2023 ≤ 2024). The result JSON confirms `"N11": ["NCT04538664"]` under all three tolerances. **Verified.** The F5 regex fix in `analysis/v3_02_filter_nsclc.py` accomplished the corpus-completeness goal.

### A3. TROPION-Lung01 now NSCLC-EGFR — does it support N9? **NO. The re-routing changed `tumor_type` but did not encode the EGFR-mut subgroup; N9 remains evidence-free, and the R1-integration commit message overstates the fix.**

The hand-curated record at `data/processed/v3_nsclc_full.json` (NCT04656652) now sets `biomarker.tumor_type = "NSCLC-EGFR"` (was `"NSCLC-other"`) and adds `subgroup_readouts = ["non-actionable_subgroup", "actionable_genomic_alteration_subgroup", "EGFR-mut_subgroup"]`. **But `biomarker.egfr_mut` is still `null` (not `true`)**, and `prior_state.post_osimertinib` is `null`. Because `v3_07_build_combined_dag.py:38-39` only emits the `EGFR-mut` token when `egfr_mut is True` (and only emits the `post-osimertinib` state token when `post_osimertinib is True`), TROPION-Lung01's DAG edge is `source_state="post-chemo", biomarker="NSCLC"` — a bare `NSCLC` biomarker with no EGFR token.

Consequences:
1. **Strict superset fails**: N9 wants `g={EGFR-mut, NSCLC}` but trial e={NSCLC}. g ⊄ e.
2. **State superset fails**: N9 wants `{post-osimertinib, post-chemo}` but trial = `{post-chemo}`.
3. **Liberal does not save it**: `_bm_match_liberal` looks for token `EGFR-mut` in `e_set | sub_set`. The subgroup set is `{"non-actionable_subgroup", "actionable_genomic_alteration_subgroup", "EGFR-mut_subgroup"}` — the literal token `EGFR-mut_subgroup` does not equal `EGFR-mut`, so liberal also fails on biomarker (and would still fail on state regardless).

The result JSON confirms N9 is empty `[]` under all three tolerances. **R1 ask #3 is not delivered as advertised.** The R1-integration commit's claim of "TROPION mis-routed → fixed" is honest about the tumor-type re-tag but does not produce N9 support, and Paper A's Discussion paragraph at line 136 still names "TROP2-ADC (TROPION-Lung01)" as a post-osimertinib evidence example — which is still factually wrong inside the framework's own concordance algorithm.

**Fix:** either (a) set `biomarker.egfr_mut=true` on the TROPION record AND change the subgroup-readout token from `"EGFR-mut_subgroup"` to literal `"EGFR-mut"` (so the liberal matcher resolves it) AND add `prior_state.post_osimertinib=true` (justified because the registrational EGFR-mut subgroup readout was in post-osi patients per WCLC 2023); or (b) split the record into an EGFR-mut subgroup row (`egfr_mut=true`, `post_osimertinib=true`, `subgroup_readouts=["AGA_subgroup"]`, `tumor_type="NSCLC-EGFR"`) and a non-actionable row (`tumor_type="NSCLC-other"`, dropped from DAG); or (c) honestly disclose in the Discussion that N9 remains evidence-free in v3 and re-cite a different example.

### A4. N13/N14 merged — does the merged node cite both ALEX and ALTA-1L? **YES on citation. NO on support — ALTA-1L is silently dropped from the support set by temporal precedence.**

The merged N13 in `v3_nsclc_decision_tree.json` lists `cited_trials = ["NCT02075840", "NCT02737501"]` (ALEX + ALTA-1L). But `year=2017` was inherited from the original N13 (the ALEX node); ALTA-1L has `year_pc=2020`, and `_drug_match` / `supports()` enforces `year_pc ≤ year`. So ALTA-1L fails temporal precedence and is **not** in N13's support set. The result JSON confirms: `"N13": ["NCT01828099", "NCT02075840"]` — ALEX + ASCEND-4 (ceritinib, year_pc=2017). **ALTA-1L is named in the citation list but contributes zero evidence.**

This is a new issue introduced by the R1 merge: pre-R1, ALTA-1L supported its own dedicated N14 because N14 (presumably) carried `year=2020` matching ALTA-1L's primary completion. The merge collapsed both nodes to N13's year-2017 introduction, silently expelling ALTA-1L. The framework treats the merged N13 as a 2017-introduced node whose evidence base is ALEX + ASCEND-4, which is correct as a *2017 evidence statement* but is mis-cited as ALEX + ALTA-1L. A clinical reader who looked at the citation list and expected the support set to match would be misled.

**Fix:** either (a) move N13's `year` to 2020 to admit ALTA-1L into the support set (clinically defensible: the 1L 2nd-gen-ALK-TKI recommendation took its current "alectinib OR brigatinib OR ceritinib OR ensartinib" form by 2020 with the ALTA-1L OS update, not 2017), or (b) drop ALTA-1L from `cited_trials` (citation honesty) and keep year=2017, or (c) split into two year-stratified nodes (2017: ALEX/ASCEND-4; 2020: ALTA-1L+CROWN style update). Option (a) is the cleanest and would also pull NCT02075840 (ALEX, year_pc=2017) and NCT02737501 (ALTA-1L, year_pc=2020) into a single coherent support set.

### A5. NSCLC trial citations in Paper A — are FLAURA, MARIPOSA, etc. now \citep'd? **YES, verified.**

`manuscript/paper_A_clinical_v3.tex:71` now \citep's `soria2018flaura`, `janne2024flaura2`, `cho2024mariposa`, `yu2024herthena`, `ahn2024tropion`, `zhou2024papillon`, `mok2017aura3`, `wu2017archer1050`, `passaro2024mariposa2`, `peters2017alex`, `camidge2018altal1`, `shaw2020crown`, `solomon2014profile1014`, and the two guideline cites `hendriks2023esmo`, `nccn_nsclc_2024`. All resolve to entries added in `references.bib` lines 422-563. **Verified.** All 12 promised NSCLC primary-trial publications and the two NSCLC guideline references are present. (This is the cleanest R1 fix of the lot.)

### A6. New corpus arithmetic — 178 NSCLC trials, 49 unified nodes — are paper numbers consistent? **PARTIALLY. Abstract and boxed summary are correct (178 trials, 49 nodes, 259 pooled, 212 edges). Methods section is stale (180 trials, 145 in-scope, 210 edges, "12 EGFR nodes"). Limitations is stale ("261-trial pooled corpus"). Discussion headline still cites $P=0.0004$. Two figure captions still cite $P=0.0004$.**

Concrete inconsistencies (line numbers in `manuscript/paper_A_clinical_v3.tex`):

| Location | Says | Should say |
|---|---|---|
| L49 abstract | "178 pivotal trials ... 49 nodes (25 mBC + 24 NSCLC)" | ✓ matches `jq length` of corpus (178) and tree (24 NSCLC) |
| L50 abstract | "0.39 (19/49) ... $P=0.023$ ... NSCLC EGFR-only 0.41 ($P=0.11$); NSCLC ALK-only 0.29 ($P=0.56$)" | ✓ matches `v3_pooled_efdpr.json` |
| L61 box | "49 nodes ... 212-edge trial-DAG ... 259 trials ... 0.39 ... $P=0.023$" | ✓ matches |
| **L81 Methods** | "filtered to 176 systematic candidates ... brought the final NSCLC corpus to **180 trials**, of which **145** entered the in-scope trial-DAG" | Should be **178 trials, 147 in-scope** (per `jq length` of `v3_nsclc_full.json` and `jq '[.[]\|select(.tumor=="NSCLC")]\|length'` of `v3_combined_dag_edges.json`) |
| **L87 Methods** | "**12 nodes cover EGFR-mutant** decisions (including 4 post-osimertinib sub-positions), **8 cover ALK-rearranged**" | Should be **17 EGFR / 7 ALK** (per the abstract's own NSCLC EGFR-only $n=17$ and ALK-only $n=7$). This is internally contradictory with line 115. |
| **L90 Methods** | "The combined DAG has **210 edges (145 NSCLC in-scope + 65 mBC in-scope)** and 47 canonical source nodes" | Should be **212 edges (147 NSCLC + 65 mBC)**. The +2 is PAPILLON (now in corpus) and TROPION-Lung01 (re-routed from `NSCLC-other` to `NSCLC-EGFR`); both new edges fit, and the boxed-summary count (212) is right. |
| **L100 figure caption** | "Diamond: primary 50-node analysis (**$P=0.0004$**)" | Should be **$P=0.023$** (and "49-node" not 50). This is the pre-R1 stale number. |
| **L110 figure caption** | "The pooled 50-node test rejects at **$P=0.0004$** ($-\log_{10} P=3.4$)" | Should be **$P=0.023$ ($-\log_{10} P=1.64$)** (and 49-node). The trajectory figure's right-axis label is therefore wrong, not just the caption. |
| **L133 Discussion headline** | "the pre-registered exact-binomial test rejected $H_0: \mathrm{EFDPR} \le 0.25$ at **$P=0.0004$**" | Should be **$P=0.023$**. The Headline paragraph is the most-cited sentence; this stale number flatly contradicts the abstract. |
| **L136 Discussion** | "Of 17 EGFR-mutant decision nodes, **12 are evidence-free** at strict tolerance" | Should be **7 evidence-free** (per `nsclc_egfr_only.strict.evidence_free_count=7`). The 12 was the pre-R1 NSCLC-EGFR figure. |
| **L139 Discussion** | "ALK-rearranged decisions ... failed to reject (**$P=0.63$**)" | Should be **$P=0.56$** (`nsclc_alk_only.strict.exact_p_one_sided_vs_p25=0.5551`). |
| **L142 Discussion** | "The **24 evidence-free decision nodes** are not all equally problematic" | Should be **19 evidence-free** (per `primary.strict.evidence_free_count=19`). |
| **L151 Limitations** | "The **261-trial pooled corpus**" | Should be **259** (178 NSCLC + 81 mBC). |

**Severity:** the figure-caption $P=0.0004$ and the Discussion-headline $P=0.0004$ are publication-blocking — a reader scanning Figure 1 alone will conclude $P=0.0004$ when the abstract says $P=0.023$, and a reader scanning the Discussion alone will see "12 of 17 EGFR-mutant nodes evidence-free" when the abstract says "EGFR-only 0.41 (7/17)". The journal copy-editor will catch this; you should catch it first.

### A7. EGFR-only honest number (was 0.71 inflated, now 0.41) — is paper narrative updated? **PARTIALLY. The abstract narrative is updated. The Discussion paragraph at line 136 is not.**

Abstract line 50 correctly cites "NSCLC EGFR-only 0.41 ($P=0.11$)". The Discussion paragraph at line 135-136 still says "Of 17 EGFR-mutant decision nodes, 12 are evidence-free at strict tolerance" — which is the pre-R1 0.71 figure. The headline EGFR-vs-ALK contrast is now 0.41 vs 0.29 (P=0.11 vs P=0.56) — a 1.4x ratio, not the pre-R1 ~3x ratio (0.71 vs 0.25). The Discussion's "post-osimertinib is the largest concentrated gap" framing is still defensible at the structural level (the 5 post-osi EGFR nodes N9, N21, N22, N23, N24 are all evidence-free, plus N10), but the magnitude claim and the "12 of 17" arithmetic are stale. Paper A's "Three caveats" paragraph (line 145) also needs updating: "ESCAT-aligned and liberal tolerance gave $P=0.10$ on the pooled denominator" — actual is $P=0.084$.

### A8. ALK-only n=7 (was n=8) — disclosed? **YES on the n=7 number (abstract, results, R1 narrative); inferentially on the merge rationale.**

`nsclc_alk_only.n_nodes=7`, abstract and results both cite n=7 with P=0.56. Paper A line 87 still says "8 cover ALK-rearranged" (stale, contradicts abstract). Paper B line 124 says "(25 mBC + 24 NSCLC after de-duplication)" — implicitly acknowledges the merge. Neither paper explicitly says "N13 and N14 were merged in R1 because they were duplicates"; the only documentation is the commit message and the R1 review itself. The R1 reviewer flagged that "ALK n=8 is artificially boosted by N13/N14 duplication" (A9) — the framework now reports the un-inflated n=7, which is honest, but the merge rationale should be in the manuscript Methods or Supplement so a future reader can understand why ALK has 7 nodes when the round-0 tree had 8.

---

## B. New clinical issues introduced or surfaced by R1 fixes

### B1. Brain-mets de-stripping silently dropped FLAURA and ALEX from N22 and N20 without compensating subgroup-readout logic. **NEW REGRESSION.**

R1 changed `_state_match` (lines 31-41 of `v3_08_compute_pooled_efdpr.py`) to no longer strip `brain-mets` from the guideline state (R1 ask #9 was: "Drop N20 or implement a brain-mets subgroup-readout match-criterion"). The fix did half: it removed `brain-mets` from the strip list and added a docstring saying "brain-mets guideline nodes are now matched only when the trial explicitly enrols/stratifies brain-mets cohorts (encoded via a subgroup_readouts entry checked by the liberal-tolerance matcher)." **But the liberal matcher does not actually implement that check.** No `brain-mets` or `brain_mets` token is ever added to any trial's `subgroup_readouts` in `v3_nsclc_full.json` (verified by `jq '[.[]|.subgroup_readouts|.[]] | unique'` — no brain-mets token present), and `_bm_match_liberal` only consumes the subgroup tokens for biomarker matching, not state matching.

Consequences:
- **N20 (1L+brain-mets, ALK-rearranged):** pre-R1 strict supports were the union of N13+N15 (ALEX, ALTA-1L, CROWN). Now N20 is strict-evidence-free and stays evidence-free at every tolerance. The result JSON confirms `"N20": []` strict/escat/liberal.
- **N22 (1L+brain-mets, EGFR-mut):** pre-R1 strict supported FLAURA + the three failed-development 3rd-gen TKIs via brain-mets stripping. Now N22 is evidence-free at every tolerance. The result JSON confirms `"N22": []` strict/escat/liberal.

This is exactly the R1 reviewer's documented preference *only if you also add the subgroup-readout match*. As implemented, the fix drops two formerly-supported nodes into the evidence-free pool, contributing 2 of the 19 strict evidence-free flags. **It moved the result in the right direction (less ALK n-inflation) but for the wrong reason (silent loss of formerly-credited support).** This is a non-trivial methodological story that the manuscript does not currently disclose.

**Fix:** either (a) implement the promised subgroup-readout brain-mets match in `_bm_match_liberal` (would require adding `brain_mets_subgroup` to FLAURA/ALEX/CROWN/etc. trials' `subgroup_readouts` and matching it against `brain-mets` in the guideline state), or (b) drop N20 and N22 from the tree entirely (with rationale documented in Methods), or (c) keep the current behaviour and disclose explicitly in the Methods that N20 and N22 are now evidence-free as a deliberate framework choice to require brain-mets-explicit trial readouts.

### B2. TROPION-Lung01 N9 fix is incomplete — see A3. **Re-stated here for the "new issues" tally.**

The R1 change re-routed TROPION from `NSCLC-other` to `NSCLC-EGFR` but did not update `egfr_mut`, `post_osimertinib`, or the subgroup token format. N9 stays evidence-free. The Discussion paragraph at L136 names TROPION-Lung01 as if it supported N9 — which is now factually wrong inside the framework.

### B3. N13 merged-node ALTA-1L citation honesty — see A4.

Cited but does not support due to temporal precedence (year_pc=2020 > year=2017).

### B4. SAVANNAH still excluded from N21 despite R1 adding `"MET-TKI + osimertinib"` to `DRUG_CLASS_EQUIVALENCE`. **R1 ask #6 not closed.**

`v3_08_compute_pooled_efdpr.py:135-138` adds two new drug-class equivalence keys (`"MET-TKI + osimertinib"` and `"EGFR TKI mutant-selective (ex20ins)"`). But:
1. **No trial in the corpus is encoded with either of these classes.** `jq '.[]|select(.drug_class=="MET-TKI + osimertinib" or .drug_class=="EGFR TKI mutant-selective (ex20ins)") | length'` returns 0.
2. SAVANNAH (NCT03778229) still has `drug_class="investigational (other)"` (and `egfr_mut=true, post_osimertinib=true`, but no `met_amplification` schema field — the field was not added per R1 ask #6).
3. `v3_07_build_combined_dag.py:95-96` strips all `"investigational (other)"` records from the DAG before edge construction, so SAVANNAH never reaches the EFDPR computation.

The new equivalence-map entries are dead code. N21 remains evidence-free for the same two cumulative reasons R1 documented: drug-class strip + missing MET-amp biomarker token. EXCLAIM-2 (mobocertinib), ZENITH20 (amivantamab monotherapy), SPARTA, ORCHARD, WU-KONG1, REZILIENT1 are similarly all `"investigational (other)"` and stripped.

**Fix:** (a) add `met_amplification` field to the biomarker schema; (b) re-encode SAVANNAH/SAFFRON/INSIGHT-2 with `drug_class="MET-TKI + osimertinib"`; (c) re-encode EXCLAIM-2/ZENITH20/REZILIENT1 with `drug_class="EGFR TKI mutant-selective (ex20ins)"` or `"Amivantamab monotherapy"`. Without these, N12/N21/N23 are deterministic evidence-free flags (3 of 7 NSCLC-EGFR evidence-free) and contribute mechanically to the headline.

### B5. FL-ALTER (NCT04028778) still encoded as `"Bevacizumab + EGFR TKI"`. **R1 ask #4 not addressed.**

`v3_nsclc_full.json` for NCT04028778 still shows `drug_class="Bevacizumab + EGFR TKI"`, with note "Closest canonical class is Bevacizumab + EGFR TKI (anti-angiogenic + EGFR TKI category)." Anlotinib is a multikinase VEGFR-TKI, not bevacizumab. N5's strict-support set is `["NCT02411448", "NCT04028778"]` = RELAY + FL-ALTER. The clinical reading (NCCN/ESMO would not credit FL-ALTER as supporting a bevacizumab+TKI recommendation) is still wrong. N5 looks supported at strict, but for one valid (RELAY) and one mis-classified (FL-ALTER) trial. The "supported at strict" status of N5 therefore overstates the case for the bevacizumab+TKI guideline recommendation.

### B6. N1's drug class label still `"EGFR TKI 3rd-gen (osimertinib)"` while the support set includes three failed-development 3rd-gen TKIs. **R1 ask #12 not addressed.**

N1's support list under strict is `["NCT02108964" (nazartinib EGF816), "NCT02186301" (rociletinib TIGER-1), "NCT02296125" (FLAURA — the right answer), "NCT02588261" (naquotinib ASP8273)]`. Three of four "supporters" are failed-development 3rd-gen TKIs that did not reach approval and are not osimertinib. The parenthetical class label `"(osimertinib)"` therefore mis-represents the support set. A clinical reader who sees "N1 is supported by 4 trials including FLAURA" and assumes those are osimertinib-family trials will be misled. The R1 reviewer asked for the class rename to `"EGFR TKI 3rd-gen"` with a Methods note that osimertinib is the only commercially-approved class member; this is not done. Same issue affects N22 (also lists the three failed 3rd-gen TKIs as part of its support set when implemented per A3 below, though N22 is currently evidence-free for the separate brain-mets reason — B1).

---

## C. Manuscript narrative issues that survived R1

### C1. Paper A line 118 evidence-free cluster list is internally inconsistent with the result JSON.

The paragraph asserts cluster (i) "NSCLC post-osimertinib (N7 amivantamab+chemo, N8 HER3-ADC, N9 TROP2-ADC, N10 platinum-doublet salvage, N21 MET-amp salvage, N23 post-amivantamab, N24 post-osi+post-chemo)". But N7 and N8 are **supported**, not evidence-free (`"N7": ["NCT04988295"]`, `"N8": ["NCT04619004"]` — MARIPOSA-2 and HERTHENA-Lung01 both support their cited nodes under strict). Cluster (ii) includes N11 — also supported (`"N11": ["NCT04538664"]` PAPILLON). So the listed cluster includes 3 nodes that are NOT evidence-free, and the prose is therefore inflated. The actual evidence-free NSCLC nodes (N9, N10, N12, N19, N20, N21, N22, N23, N24) cluster as: post-osi/post-chemo (N9, N24), post-osi salvage (N21, N23), 1L brain-mets (N20, N22), ALK post-everything (N19), 1L platinum-doublet salvage placeholder (N10), 2L ex20ins (N12). The cluster prose needs to be rewritten against the actual `evidence_free_nodes` list.

### C2. Paper A abstract "post-osimertinib EGFR-mutant decision nodes (HER3-ADC, TROP2-ADC, MET+osimertinib positions)" — HER3-ADC (N8) is supported.

This phrasing mirrors C1: HER3-ADC is N8, which is supported (HERTHENA-Lung01). The honest list of post-osi-EGFR evidence-free nodes is TROP2-ADC (N9), MET+osi (N21), post-amivantamab (N23), post-osi+post-chemo (N24), 1L+brain-mets (N22 — but brain-mets, not post-osi). The abstract should drop "HER3-ADC".

### C3. Paper A line 145 cites "$P=0.10$ on the pooled denominator" for ESCAT/liberal; actual is $P=0.084$.

The result JSON: `primary.escat.exact_p_one_sided_vs_p25 = 0.0836`. The Discussion rounds to 0.10, which conventionally would be 0.08 (one significant digit) or 0.084 (two). The abstract correctly uses 0.084. The Discussion paragraph is therefore inconsistent with the abstract on a number that the same paragraph is highlighting.

### C4. Paper B line 130 has a number-set arithmetic error.

"ESCAT-aligned and liberal tolerance gave 0.34 (**24/50** $\to$ **17/50**; $P = 0.10$), failing to reject." The actual primary denominator is 49 (not 50); the actual evidence-free count at ESCAT/liberal is 17; the strict evidence-free count is 19. The "24/50 → 17/50" phrasing implies a strict-to-ESCAT transition that was 24 → 17, but actually it is 19 → 17. The denominator is 49 throughout, not 50. Paper B also has a "before/after" framing that maps to a pre-R1 strict count of 24 — i.e., this sentence is a stale draft from a pre-R1 version.

### C5. Paper A line 87 NSCLC node-count breakdown contradicts the abstract.

"12 nodes cover EGFR-mutant decisions, 8 cover ALK-rearranged, and 5 cover combined or special-population scenarios." Sum 25. But (a) tree now has 24 nodes after merge; (b) abstract counts EGFR=17 and ALK=7 (sum 24). The breakdown in Methods is from the pre-R1 25-node tree with the wrong EGFR/ALK split; it has not been updated.

---

## D. Concrete asks (12)

1. **Fix Paper A figure captions for Figs 1 and 3 ($P=0.0004$ → $P=0.023$; "50-node" → "49-node").** Lines 100 and 110 of `paper_A_clinical_v3.tex`. The trajectory figure's $-\log_{10} P$ axis label also needs to change from 3.4 to ~1.64. Re-render Fig 1 and Fig 3 from the actual `v3_pooled_efdpr.json`.

2. **Fix Paper A Discussion headline $P=0.0004$ → $P=0.023$ (line 133)**, AND "12 of 17 EGFR evidence-free" → "7 of 17" (line 136), AND "$P=0.63$" → "$P=0.56$" (line 139), AND "24 evidence-free decision nodes" → "19" (line 142). All are direct re-statements of the abstract's already-corrected numbers; the Discussion was not re-pulled.

3. **Fix Paper A Methods stale counts (line 81, 87, 90, 151).** "180 trials, 145 in-scope" → "178 trials, 147 in-scope"; "12 nodes cover EGFR-mutant ... 8 cover ALK" → "17 EGFR, 7 ALK"; "210 edges (145 NSCLC + 65 mBC)" → "212 edges (147 NSCLC + 65 mBC)"; "261-trial pooled corpus" → "259-trial pooled corpus".

4. **Re-implement or honestly disclose the brain-mets handling (B1).** Choose one: (a) add `brain_mets_subgroup` to `subgroup_readouts` of FLAURA, ALEX, ALTA-1L, CROWN, lorlatinib-CROWN, etc., and add a `brain-mets` state-match rule to `_state_match` under the liberal tolerance only; or (b) drop N20 and N22 from the tree with rationale; or (c) explicitly document in Methods that N20 and N22 are intentionally evidence-free under the current framework because no NSCLC trial has a brain-mets-explicit registrational readout in `subgroup_readouts`. The current implementation is a half-fix that silently expelled FLAURA and ALEX from their own cited nodes.

5. **Fix TROPION-Lung01 N9 support (B2/A3).** Set `biomarker.egfr_mut=true` and `prior_state.post_osimertinib=true` on the TROPION record, and either change the subgroup token from `"EGFR-mut_subgroup"` to `"EGFR-mut"` (so the liberal matcher resolves it) or change the liberal matcher to strip the `_subgroup` suffix when comparing. Document in the trial note that TROPION's registrational EGFR-mut subgroup readout (WCLC 2023) is the basis for crediting N9. If you choose not to do this, rewrite the Discussion paragraph at line 136 to remove TROPION-Lung01 from the post-osi example list and to honestly state that N9 is evidence-free in v3.

6. **Fix N13 merged-node temporal-precedence issue with ALTA-1L (B3/A4).** Either move `year=2017` → `year=2020` (admits ALTA-1L into the support set; clinically defensible because the "ALK 2nd-gen alectinib/brigatinib/ceritinib/ensartinib" 1L recommendation took its current form by 2020 with the ALTA-1L OS update) or drop NCT02737501 from `cited_trials` and keep year=2017 (citation honesty). Currently the merged node cites ALTA-1L but expels it via the temporal-precedence rule, which is silently inconsistent.

7. **Either deliver R1 ask #6 (SAVANNAH/MET-amp) or remove the dead-code drug-class equivalence entries (B4).** `DRUG_CLASS_EQUIVALENCE` at lines 135-138 adds `"MET-TKI + osimertinib"` and `"EGFR TKI mutant-selective (ex20ins)"` but no trial in the corpus uses either class. Either (a) add `met_amplification` to the biomarker schema, re-encode SAVANNAH/SAFFRON/INSIGHT-2 with `drug_class="MET-TKI + osimertinib"`, and re-encode EXCLAIM-2/ZENITH20/REZILIENT1 with the ex20ins class (would credit N21 and N12 and reduce NSCLC-EGFR evidence-free count from 7 → 4 or 5), or (b) delete the unused equivalence entries to avoid implying that the fix was done.

8. **Fix Paper A line 118 cluster prose (C1) and abstract line 50 cluster phrasing (C2).** Remove N7 (MARIPOSA-2 / amivantamab+chemo), N8 (HERTHENA-Lung01 / HER3-ADC), and N11 (PAPILLON / 1L ex20ins) from the "evidence-free cluster" list; they are all supported. The honest cluster (i) is post-osi/post-chemo (N9, N24) + post-osi salvage (N21, N23). Cluster (ii) is brain-mets (N20, N22) + 2L ex20ins (N12) + 1L anti-VEGF (N5 if FL-ALTER is re-classed per B5) + N10. The abstract "HER3-ADC, TROP2-ADC, MET+osimertinib" should become "TROP2-ADC (N9), MET+osimertinib (N21), post-amivantamab (N23)".

9. **Fix Paper B line 130 stale arithmetic (C4).** "24/50 → 17/50; $P=0.10$" → "19/49 → 17/49; $P=0.084$". The 50-denominator and the strict count of 24 are both pre-R1 stale.

10. **Either re-class FL-ALTER (NCT04028778) away from `"Bevacizumab + EGFR TKI"` (B5/R1 ask #4) or honestly disclose in N5's cluster narrative.** Anlotinib is a multikinase VEGFR-TKI, not bevacizumab. Suggested class: `"VEGFR-TKI + EGFR TKI"` (new) or `"investigational (other)"`. With this fix, N5 strict-supports only RELAY (NCT02411448) and moves toward evidence-free for the bevacizumab arm — which is the honest clinical reading. If you keep FL-ALTER under the bevacizumab class, add a Methods footnote saying that "Bevacizumab + EGFR TKI" is the framework's umbrella for anti-angiogenic + EGFR TKI combinations including anti-VEGF mAbs and multikinase VEGFR-TKIs.

11. **Rename drug class `"EGFR TKI 3rd-gen (osimertinib)"` to `"EGFR TKI 3rd-gen"` (B6 / R1 ask #12).** Add Methods footnote that the class pools osimertinib (sole approved member) with nazartinib (NCT02108964), rociletinib (NCT02186301), and naquotinib (NCT02588261), which were failed-development 3rd-gen TKIs that the framework treats as pivotal for class-aggregation purposes. Without this rename, N1's "4 supporting trials" claim implies 4 osimertinib-class trials, which is false.

12. **Document the N13/N14 merge in Methods, not just the commit log (A8 follow-up).** Add one sentence to Methods or Supplement: "The original v3-round-0 NSCLC tree contained N13 (1L ALK 2nd-gen, citing ALEX) and N14 (1L ALK 2nd-gen, citing ALTA-1L) as distinct nodes. After v3 round-1 clinical review (B-ALK reviewer flagged identical (state, biomarker, drug class) tuples), these were merged into a single N13 citing both ALEX and ALTA-1L. The ALK-only denominator is therefore $n=7$, not $n=8$." Without this, a v4 reviewer who inherits the tree will not know why N14 is missing.

---

## E. What R1 did well (for completeness)

- The strict-superset matcher change (`_bm_match_strict` rewritten at lines 44-54 of `v3_08_compute_pooled_efdpr.py`) is the right call clinically and operationally. It cleanly resolves the v3-round-0 G-19/G-21/G-26 class of issues that v2 had to band-aid around.
- PAPILLON addition (NCT04538664, F5 regex fix at `v3_02_filter_nsclc.py`) is fully delivered: in corpus, in DAG, supports N11 under all three tolerances. Cleanest single fix in the R1 commit.
- N1 token simplification (`"EGFR-mut/EGFR-ex19del-or-L858R/NSCLC"` → `"EGFR-mut/NSCLC"`) plus the superset matcher together let FLAURA support its own cited node. R1 ask #1 fully delivered.
- NSCLC trial \citep coverage in Paper A line 71 (12 trial citations + 2 guideline citations added to `references.bib`). R1 ask asked for; delivered cleanly.
- Bootstrap CI computation now in `v3_08_compute_pooled_efdpr.py:177-189` (was promised in prereg-v3 but never computed pre-R1). The percentile bootstrap CIs in `v3_pooled_efdpr.json` are concordant with Clopper-Pearson — good evidence that the small-$n$ inference is internally consistent.
- N13/N14 merge (denominator de-inflation): ALK now $n=7$, EGFR $n=17$, pooled $n=49$. The R1 reviewer asked for this; delivered (with caveat A4 above).
- The drug-class equivalence map gained `"MET-TKI + osimertinib"` and `"EGFR TKI mutant-selective (ex20ins)"` — dead code as currently implemented (B4), but the *intent* is there and a v4 pass that completes the trial-side encoding will benefit.

---

## VERDICT

**MAJOR REVISION (manuscript-level).**

The R1 integration is a solid code-side delivery — the strict matcher is rewritten correctly, PAPILLON is added cleanly, the N13/N14 merge is structurally sound, and the headline numbers (pooled EFDPR 0.39, $P=0.023$ REJECT; NSCLC EGFR 0.41; NSCLC ALK 0.29) are derivable end-to-end from the artifacts. The pre-registered rejection survives every R2-flagged manuscript fix below.

But the **manuscript prose was not fully re-pulled to match the post-R1 numbers**. Two figure captions and the Discussion headline still carry the pre-R1 $P=0.0004$ (which a journal copy-editor will catch immediately and which a careful reader will surface as an inconsistency with the abstract). The Discussion paragraph at L135-136 still uses "12 of 17 EGFR evidence-free" (the pre-R1 0.71 figure). The Methods section has four stale numbers (180 trials, 145 in-scope, 210 edges, 12-EGFR/8-ALK node breakdown) that contradict the abstract's own arithmetic. The Limitations paragraph cites the wrong corpus count (261 vs 259). The cluster-prose lists supported nodes (N7, N8, N11) as if evidence-free.

**Three of the R1 fixes also have functional issues that need resolving:**
1. TROPION-Lung01 N9 fix is incomplete (re-routed `tumor_type` but did not set `egfr_mut=true` or `post_osimertinib=true`; N9 remains evidence-free at every tolerance) — A3, B2.
2. N13 merge silently expelled ALTA-1L from its own cited support set via temporal precedence (cited but contributes zero evidence) — A4, B3.
3. Brain-mets de-stripping silently expelled FLAURA and ALEX from N22 and N20 (two formerly-supported nodes now evidence-free without compensating subgroup-readout logic) — B1.

**Six R1 asks remain not addressed** (4, 5, 6, 9, 10, 12 from R1's concrete-asks list): FL-ALTER drug-class miscoding, investigational-other re-classing, SAVANNAH/MET-amp schema, brain-mets subgroup logic, NSCLC clinical second-annotator pass, 3rd-gen TKI class rename. Of these, #5 (investigational-other) and #6 (SAVANNAH/MET-amp) are the most consequential — together they account for 3 of 7 NSCLC-EGFR evidence-free flags (N12, N21, N23) and would shift NSCLC-EGFR EFDPR from 0.41 → ~0.24 if fully addressed.

This is a **manuscript-level MAJOR revision**, not a code-level one. The code is now mostly right; the prose is mostly stale. I would re-review a v3.0.2 revision that addresses asks 1-3 (prose stale numbers, blocking), 4-6 (functional R1 regressions, blocking), and 8 (cluster-prose, blocking) at minimum. I would not block on 7, 9, 10, 11, 12 but they should be addressed before journal submission.

— Reviewer (Thoracic + Breast MO, ESMO/ASCO panel)
