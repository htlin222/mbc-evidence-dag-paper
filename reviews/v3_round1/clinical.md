# Adversarial Clinical Review — v3 Round 1

**Reviewer.** Thoracic + breast medical oncologist; ESMO/ASCO guideline panel member (HR+/HER2- mBC and EGFR/ALK NSCLC).
**Scope.** `manuscript/paper_A_clinical_v3.tex`, `manuscript/paper_B_methods_v3.tex`, `analysis/v3_06_encode_nsclc_guideline.py`, `analysis/v3_05_merge_and_kappa_nsclc.py`, `analysis/v3_07_build_combined_dag.py`, `analysis/v3_08_compute_pooled_efdpr.py`, `data/processed/v3_nsclc_full.json` (177 records), `data/processed/v3_nsclc_decision_tree.json` (25 nodes), `data/raw/nsclc_corpus_full.json`, `data/processed/nsclc_filter_log.json`, `data/results/v3_pooled_efdpr.json`, `data/results/v3_nsclc_kappa.json`. Comparator: `reviews/round[1-4]/clinical.md` and `reviews/v2_round[1-2]/clinical.md`.

**Bottom line up front.** v3 successfully rebuilds the headline rejection on a 50-node pooled denominator, the four NCT-misidentifications surfaced in v3 round-0 (AURA3 NCT02151981, HERTHENA-Lung01 NCT04619004, TROPION-Lung01 NCT04656652, plus the IMblaze370 drop) check out cleanly against ClinicalTrials.gov briefTitles, and the EGFR-vs-ALK contrast (0.71 vs 0.25) is structurally correct as a description of the trial-edge support landscape. **But the NSCLC guideline tree was hand-encoded by a single annotator (Claude) without a clinical second reader, and a deep audit of the 25 nodes plus the 177-record corpus surfaces seven issues that materially change the headline NSCLC EGFR EFDPR figure.** None of them is fatal; together they would shift NSCLC-EGFR EFDPR from 0.71 (12/17) to roughly 0.41-0.47 (7-8/17) at strict, with the pooled rejection still surviving but with a much smaller magnitude. The most consequential single finding is **a guideline-encoding token bug that mechanically locks N1 (the FLAURA node) out of supporting evidence at every tolerance level** — a problem that is functionally identical to the v2 round-1 G21/G26 mechanical-evidence-free pattern.

---

## A. NSCLC guideline tree: per-node clinical fidelity audit (N1-N25)

I read the 25 nodes against ESMO Clinical Practice Guideline 2023+2024 updates (Hendriks et al.), ASCO living guideline (Hanna 2021, Singh 2023), and NCCN NSCLC v5.2024. Verdicts:

### A1. N1 — 1L EGFR-mut common-sensitizing -> osimertinib. **Mechanically uncovered at every tolerance.**

`v3_06_encode_nsclc_guideline.py:29` encodes the biomarker as `"EGFR-mut/EGFR-ex19del-or-L858R/NSCLC"`. The literal token `"EGFR-ex19del-or-L858R"` is **never emitted by any trial extraction or by the `nsclc_biomarker()` builder in `v3_07_build_combined_dag.py:35-53`** (which emits separate `EGFR-ex19del` and `EGFR-L858R` tokens). It is also not in the `ESCAT_GROUPS` map at `v3_08_compute_pooled_efdpr.py:20-24`. Result: under strict, ESCAT, *and* liberal tolerance, no edge can ever satisfy biomarker-token concordance for N1. FLAURA (NCT02296125) is in the corpus, has the right state, the right drug class, the right year, and three matching EGFR token components — but cannot support N1. This is a coding bug, not an evidence gap. Per the data: N1 is in the strict, ESCAT, *and* liberal evidence-free lists for both `nsclc_only` and `nsclc_egfr_only` subsets. **Fix:** either add `"EGFR-ex19del-or-L858R"` as an ESCAT-equivalence union mapping to `{EGFR-ex19del, EGFR-L858R}`, or simplify N1's biomarker to `"EGFR-mut/NSCLC"` (clinically the panel-level concept and consistent with how the trial-extractions tokenise). I would prefer the latter — the "common-sensitizing" qualifier is implicit in the FLAURA enrolment criteria and does not need a guideline-tree token.

### A2. N2, N3, N4, N25 — strict-only artefacts of biomarker over-tagging at the trial level. **Real recommendation, mechanical strict miss.**

These four nodes use the simpler biomarker `"EGFR-mut/NSCLC"`, but their cited trials (FLAURA2 NCT04035486 for N2 and N25; MARIPOSA NCT04487080 for N3; ARCHER 1050 NCT01774721 for N4) all carry the over-tagged trial-level biomarker `"EGFR-mut/EGFR-ex19del/EGFR-L858R/NSCLC"`. Strict set-equality (`v3_08_compute_pooled_efdpr.py:38-39`) therefore fails. **All four nodes ARE supported under ESCAT/liberal** (per per-node output) — confirming the strict miss is purely an encoding-token-set-cardinality artefact. This is the same class of bug as v2 round-1 G19/G21/G26 critique: the strict-tolerance algorithm is measuring biomarker-token-string equality, not clinical concordance. **Fix:** stop emitting `EGFR-ex19del` and `EGFR-L858R` as separate tokens at the trial level when `EGFR-mut` is also present (these are sub-specifications of `EGFR-mut`, not co-equal tokens). Equivalently: add a strict-tolerance pre-processing step that strips redundant sub-specification tokens from edge sets when the parent token is present. Fixing this drops 4 nodes from the strict NSCLC-EGFR evidence-free list (12 -> 8), and the NSCLC-EGFR strict EFDPR drops from 0.71 to 0.47.

### A3. N5 — 1L EGFR-mut anti-VEGF + EGFR TKI. **Drug-class miscoding by anlotinib != bevacizumab.**

N5 supports `["Bevacizumab + EGFR TKI", "Ramucirumab + EGFR TKI"]`. Under strict the supporting edge is NCT04028778 — which is **FL-ALTER (gefitinib + anlotinib)**, encoded as drug class `"Bevacizumab + EGFR TKI"`. Anlotinib is a small-molecule multikinase VEGFR-TKI, not a bevacizumab biosimilar or an anti-VEGF mAb. The class is materially mis-applied: a clinical guideline reader would not consider FL-ALTER as supporting a bevacizumab+TKI recommendation, and ESMO/NCCN do not list FL-ALTER under the bevacizumab+TKI option. **Fix:** re-encode FL-ALTER as a separate `"VEGFR-TKI + EGFR TKI"` class (or "investigational (other)"), and document that N5 is then supported strict only by NCT02411448 (RELAY, ramucirumab+erlotinib — correct). NEJ026 / CTONG-0901 are not in the corpus and N5 will remain strict-evidence-free for the bevacizumab arm under that fix; flag honestly.

### A4. N7 — post-osimertinib amivantamab + chemo (MARIPOSA-2). **Correctly supported.**

NCT04988295 is appropriately encoded with `post_osimertinib=True`, `EGFR-mut/NSCLC`, `Amivantamab + chemotherapy`, `year_pc=2023`. Strict supports correctly. OK.

### A5. N8 — post-osimertinib HER3-ADC (HERTHENA-Lung01). **Correctly supported.**

NCT04619004 is the right NCT (corrected from round-0 misidentification NCT05009836; verified against briefTitle `"HERTHENA-Lung01: Patritumab Deruxtecan in Subjects With Metastatic or Locally Advanced EGFR-mutated Non-Small Cell Lung Cancer"`), correctly encoded `post-osimertinib + EGFR-mut + HER3-ADC + 2023`. Strict supports correctly. OK.

### A6. N9 — post-osi+post-chemo TROP2-ADC (TROPION-Lung01). **Cited trial mechanically excluded.**

N9 cites TROPION-Lung01 (NCT04656652, correctly identified). But the hand-curated record at `v3_05_merge_and_kappa_nsclc.py:71-96` sets `biomarker.tumor_type = "NSCLC-other"`, and `v3_07_build_combined_dag.py:97-98` **hard-skips any record with `tumor_type == "NSCLC-other"` from the trial-DAG**. So TROPION-Lung01 cannot ever support its own cited node N9 (and is excluded from every NSCLC-EGFR computation entirely, even though the trial enrolled a pre-specified actionable-genomic-alteration EGFR-mut subgroup with separately-reported PFS at WCLC 2023). **Fix:** either (a) split TROPION-Lung01 into two records, an EGFR-mut subgroup record (`tumor_type = "NSCLC-EGFR"`, `egfr_mut=True`, `subgroup_readouts=["AGA_subgroup"]`) and a non-actionable record kept as `NSCLC-other`; or (b) drop the `NSCLC-other` skip filter and let liberal tolerance handle the biomarker subgroup matching. Option (a) is more clinically faithful and would credit N9 with TROPION-Lung01 support under ESCAT or liberal. I would not credit it under strict, because the trial-level enrolment is biomarker-mixed.

### A7. N11 — 1L EGFR ex20ins amivantamab+chemo. **PAPILLON missing from corpus due to a regex bug.**

N11 cites PAPILLON (NCT04538664) but lists `cited_trials: []` because PAPILLON is not in the corpus. PAPILLON is in the raw systematic search (1 of 702 candidates), and is filtered out at F5 (`is_egfr_or_alk`). The F5 regex `r"\bEGFR.?exon.?20\b"` requires a word boundary after "20", but the text in PAPILLON's eligibility says **"EGFR Exon 20ins"** (no space between "20" and "ins"), so `\b` fails. PAPILLON's brief title also says "(EGFR) Exon 20 Insertions" — but the closing paren breaks `EGFR.?Exon` (which only allows 0-1 character of intervening text). **This is a corpus-completeness bug, not a clinical encoding bug.** PAPILLON is a NEJM 2024 phase 3 registrational trial in 1L EGFR ex20ins; its absence makes N11 evidence-free in v3, contributing 1 of the 12 NSCLC-EGFR strict misses. **Fix:** widen the F5 regex to `r"EGFR[\s\W]*Exon[\s\W]*20"` without `\b` boundaries, re-run F2-F8, re-extract PAPILLON, and re-run EFDPR. Expected: N11 becomes supported strict, NSCLC-EGFR EFDPR drops by 1 more node.

### A8. N12 — post-chemo EGFR ex20ins. **Recommendation orphaned by drug-class encoding.**

N12 lists `recommended_classes = [{"class": "investigational (other)"}]` — but `v3_07_build_combined_dag.py:95-96` strips edges with `drug_class == "investigational (other)"` from the DAG, and `v3_08_compute_pooled_efdpr.py:122` requires drug-class membership match. So N12 cannot be supported by *any* trial under any tolerance, regardless of which trials are in the corpus. The intended trials (EXCLAIM-2 mobocertinib NCT04129502; ZENITH20 amivantamab NCT03457142; etc.) would never be credited because their drug class would also fall into `"investigational (other)"`. **Fix:** either (a) define explicit drug classes for mobocertinib (`"EGFR ex20ins-TKI (mobocertinib)"`) and amivantamab monotherapy (`"Amivantamab monotherapy"`), or (b) drop N12 from the tree if no encoded drug class corresponds to a guideline recommendation. Same critique applies to **N21** (post-osimertinib + MET-amp salvage, recommended class `"investigational (other)"`) and **N23** (post-osi+post-amivantamab, `"investigational (other)"`). These three nodes — N12, N21, N23 — are mechanically locked into evidence-free at every tolerance because their recommended class is the very class that the DAG strips out. They contribute 3 of the 12 NSCLC-EGFR strict misses.

### A9. N13 vs N14 — DUPLICATES. **Denominator inflation.**

N13 cites ALEX (NCT02075840) and N14 cites ALTA-1L (NCT02737501), but their (state, biomarker, drug class) tuples are *identical*: `first-line / ALK-rearranged/NSCLC / "ALK TKI 2nd-gen (alectinib/brigatinib/ceritinib/ensartinib)"`. They are interchangeable rows in the decision tree under the framework's own concordance algorithm. As written, N13 and N14 inflate the ALK denominator by 1 node and inflate the supported count by 1 node, so the ratio is preserved but the ALK n=8 is artificially boosted to look like a more strongly-supported tree. This is exactly the v2 round-1 G23-G20 critique. **Fix:** merge N13 and N14 into a single 1L 2nd-gen ALK TKI node citing both ALEX and ALTA-1L. ALK n=7 then; ratios unchanged.

### A10. N20 — 1L + brain mets. **Effectively a duplicate after special-token stripping.**

N20's state `"first-line+brain-mets"` has `brain-mets` stripped by the state-match special list at `v3_08_compute_pooled_efdpr.py:33`. N20 therefore reduces to "first-line / ALK-rearranged" with both 2nd-gen and 3rd-gen ALK TKI as recommended classes — i.e., the union of N13/N14 and N15. The 6 supporting trials match exactly the union of N13+N14+N15 supporters. If brain-mets is intended to be a clinical sub-encoding, the framework should test it; if it isn't, N20 is a duplicate row. **Fix:** either build a `brain-mets` subgroup-readout filter (so only trials with reported intracranial PFS endpoint count) or drop N20.

### A11. N18 / N19 — post-ALK TKI lorlatinib + post-ALK platinum salvage. **Real clinical gap, but post-2018 trials filtered by temporal precedence.**

N18 (post-ALKTKI, ALK-rearranged, lorlatinib, year=2018) is strict-evidence-free because the only strict-state-and-bm-matching lorlatinib trial in the corpus is NCT01970865 (year 2017), which carries the `ALK-resistance-mut` token (strict mismatch with N18's plain `ALK-rearranged/NSCLC`). The lorlatinib post-ALKTKI strict trials at year ≥ 2020 (NCT03909971, NCT05257512, NCT05869162, NCT05955391) all post-date N18's introduction year of 2018 and fail temporal precedence. **This is structurally accurate**: at the time the panels added lorlatinib post-ALK TKI in 2018, the supporting evidence was the NCT01970865 phase 1/2 (Ou 2018), which is correctly tagged with the `ALK-resistance-mut` token because the registrational endpoint was in resistance-mutation patients. So N18's strict miss is partially a token-match artefact (resistance-mut subset is a stricter population than the guideline node) and partially a real reflection of the thinness of the 2018 evidence base. ESCAT supports N18 via NCT01970865 — that is the right read. **Action:** keep N18 evidence-free at strict but explicitly label this as "supported under ESCAT but not strict" in the per-node breakdown, and stop calling it a fully-evidence-free node in the manuscript prose. N19 (platinum doublet, ALK-resistance-mut) is more dubious: the NCCN/ESMO recommendation for post-all-ALK-TKI is platinum doublet regardless of resistance-mut status, so the ALK-resistance-mut biomarker token is over-restrictive. Either drop the resistance-mut token from N19, or change the recommended class to "investigational (other)" honestly.

### A12. N21 — post-osi + MET-amp salvage. **SAVANNAH IS in the corpus, but locked out by class encoding.**

N21 strict has zero support. SAVANNAH (NCT03778229, "Osimertinib Plus Savolitinib in EGFRm+/MET+ NSCLC Following Prior Osimertinib") IS in `v3_nsclc_full.json` with `prior_state.post_osimertinib=True, post_egfr_tki=True`, `biomarker.egfr_mut=True`, but `drug_class = "investigational (other)"` AND **`MET-amp` is not a token in the biomarker schema at all**. Two cumulative errors prevent SAVANNAH from supporting N21:
1. SAVANNAH's drug class is `"investigational (other)"`, which the DAG-builder strips.
2. Even if the class were preserved, the biomarker schema has no `met_amplification` field, so SAVANNAH cannot be tagged with `MET-amp` and N21's `EGFR-mut/MET-amp/NSCLC` token set will never match.

**Fix:** (a) add a drug-class label `"MET-TKI + osimertinib"` for savolitinib+osi combinations and re-encode SAVANNAH/SAFFRON/INSIGHT-2; (b) add a `met_amplification` biomarker schema field; (c) re-extract SAVANNAH (NCT03778229) and SAFFRON (NCT05261399) with both fixes. SAFFRON, by the way, is currently mis-classified as `"EGFR TKI 3rd-gen (osimertinib)"` even though it is a savolitinib+osi combination vs platinum-doublet salvage — clinically these are different recommendations.

### A13. N22 — 1L + brain mets EGFR-mut osimertinib. **Supported, but for the wrong reason.**

N22 strict supports NCT02108964 (nazartinib EGF816), NCT02186301 (TIGER-1 rociletinib), NCT02588261 (ASP8273 naquotinib). These are three NON-osimertinib 3rd-gen-class EGFR TKIs, all with `biomarker = "EGFR-mut/NSCLC"`. FLAURA (NCT02296125), the actual cited osimertinib brain-mets trial, is NOT among the supporting trials — because of the same over-tagged biomarker-set bug as A2. The clinical reading is that N22 is "supported" by trials that the panel did NOT cite (and which were investigational not-approved 3rd-gen TKIs that did not become standard of care), and is NOT supported by FLAURA. The headline number (N22 supported) hides the fact that the supporting evidence is from drugs that didn't reach approval. **Fix:** apply the strict token-set fix from A2; FLAURA will then support N22 correctly, and the three failed-development 3rd-gen TKIs become incidental supporters.

### A14. N16 — PROFILE 1014 (crizotinib 1L). **Correctly identified.**

NCT01154140, briefTitle "A Clinical Trial Testing The Efficacy Of Crizotinib Versus Standard Chemotherapy Pemetrexed Plus Cisplatin Or Carboplatin In Patients With ALK Positive Non Squamous Cancer Of The Lung" — this is PROFILE 1014. Verified against ClinicalTrials.gov. OK.

### A15. Missing nodes reviewer asked about

- **Osimertinib + bevacizumab**: not encoded as a node. Defensible omission — neither ESMO nor NCCN gives this a Tier I recommendation; phase 3 trials (ETOP BOOSTER, WJOG 9717L) were negative for OS and the indication is not in current guideline practice.
- **Alectinib post-crizotinib (ALEX-style brain mets)**: implicitly covered by N17 (post-ALK TKI 2nd-gen). NCCN does not separately list a CNS-specific post-crizotinib alectinib recommendation. OK.
- **PAPILLON post-chemo ex20ins**: PAPILLON is 1L, not post-chemo (its comparator is carboplatin-pemetrexed in the chemo-naive population). The post-chemo ex20ins position would be N12 (covered above). PAPILLON should support N11 (1L) once added; see A7.
- **MARIPOSA-2 vs CHRYSALIS-2 distinction**: N7 is correctly cited as MARIPOSA-2 (NCT04988295). Amivantamab monotherapy in post-osi (CHRYSALIS / CHRYSALIS-2 / Spartalizumab) is NOT currently a separate node and arguably should be (NCCN does separately list "amivantamab monotherapy" as a category 2A option distinct from amivantamab + chemo). Add as N26 if v3 is willing to re-extend the tree.
- **Lazertinib monotherapy** is in the LASER-301 trial (Korean approval) — not currently in the tree. Probably acceptable to omit since FDA/EMA labels are amivantamab + lazertinib (combo), not laz mono.

---

## B. Trial-corpus 10-trial spot-check

Verified against `data/raw/nsclc_corpus_full.json` briefTitle/officialTitle/conditions:

| # | NCT | Trial | Drug class encoded | Verdict |
|---|---|---|---|---|
| 1 | NCT02296125 | FLAURA | `EGFR TKI 3rd-gen (osimertinib)` | **OK trial; encoding bug at N1 — see A1.** |
| 2 | NCT04035486 | FLAURA2 | `EGFR TKI 3rd-gen + chemotherapy` | OK trial; over-tagged biomarker (see A2). |
| 3 | NCT04487080 | MARIPOSA | `EGFR TKI 3rd-gen + bispecific (amivantamab + lazertinib)` | OK trial; over-tagged biomarker (see A2). |
| 4 | NCT01774721 | ARCHER 1050 | `EGFR TKI 2nd-gen (afatinib/dacomitinib)` | OK trial; over-tagged biomarker (see A2). |
| 5 | NCT02151981 | AURA3 | `EGFR TKI 3rd-gen (osimertinib)` | **Verified corrected; was misidentified as NCT02788279 (IMblaze370 colorectal) in round-0.** Brief title confirms AZD9291 vs platinum-doublet in T790M+. Hand-curated record at `v3_05_merge_and_kappa_nsclc.py:18-44` is clinically faithful. OK. |
| 6 | NCT04988295 | MARIPOSA-2 | `Amivantamab + chemotherapy` | OK. Correctly tagged post-EGFRTKI + post-osimertinib. |
| 7 | NCT04619004 | HERTHENA-Lung01 | `HER3-ADC (patritumab deruxtecan)` | **Verified corrected; was misidentified as NCT05009836 in round-0.** Brief title confirms. OK. |
| 8 | NCT04656652 | TROPION-Lung01 | `TROP2-ADC (datopotamab deruxtecan)` | **Verified corrected; was misidentified as NCT04644237 (DESTINY-Lung02) in round-0.** Brief title confirms DS-1062a vs docetaxel. **But:** `tumor_type = NSCLC-other` excludes the trial from the DAG entirely — see A6. |
| 9 | NCT01154140 | PROFILE 1014 | `ALK TKI 1st-gen (crizotinib)` | OK. Brief title confirms. |
| 10 | NCT02075840 | ALEX | `ALK TKI 2nd-gen (alectinib/brigatinib/ceritinib/ensartinib)` | OK. |

**Additional spot-check beyond the canonical 10**:
- **NCT01828099 = ASCEND-4 (ceritinib 1L vs chemo)**, encoded as `ALK TKI 2nd-gen (alectinib/brigatinib/ceritinib/ensartinib)`. Drug class is correct (ceritinib is 2nd-gen). N13 cites ALEX (NCT02075840) but the strict supports list at N13 includes BOTH NCT02075840 AND NCT01828099 (ASCEND-4). This is correct under the drug-class equivalence map but means N13's "support" includes ASCEND-4, which is technically a different agent than the ESMO/NCCN-cited ALEX. Acceptable under the framework's class-aggregation rule but worth flagging to the reader.
- **NCT04028778 = FL-ALTER (gefitinib + anlotinib)**, encoded as `Bevacizumab + EGFR TKI`. **Class miscoded** — anlotinib is a multikinase VEGFR-TKI, not bevacizumab. See A3.
- **NCT02108964 = nazartinib (EGF816)**, NCT02186301 = rociletinib (TIGER-1), NCT02588261 = ASP8273 (naquotinib) — all encoded as `EGFR TKI 3rd-gen (osimertinib)`. The "(osimertinib)" parenthetical class label is misleading shorthand for "3rd-gen EGFR TKI as a class." Three failed-development 3rd-gen TKIs are pooled with osimertinib. Defensible if the manuscript explicitly says "3rd-gen TKI as drug class, not osimertinib-specific" — but the current label invites confusion. **Fix:** rename the class to `"EGFR TKI 3rd-gen"` and note in Methods that osimertinib is the only commercially-approved member of the class (with rociletinib/nazartinib/naquotinib being failed-development 3rd-gen agents that the framework treats as pivotal for class purposes).
- **NCT03778229 = SAVANNAH** (savolitinib + osi post-osi MET-amp), encoded as `investigational (other)` and stripped from the DAG. See A12.

Net: **2-3 clinically consequential trial-level encoding errors out of 10 spot-checked**, similar to the v2 round-1 error rate and similarly concentrated in drug-class miscoding rather than NCT-misidentification. The pattern of NCT-mismatches *per se* is well-controlled in v3 (the 4 round-0 corrections all check out); the residual issue is the drug-class taxonomy.

---

## C. The 5 supplementary trial corrections — are they clinically faithful?

I read the three hand-curated records at `v3_05_merge_and_kappa_nsclc.py:17-97`:

### C1. AURA3 (NCT02151981) — **clinically faithful, except `excluded.post_chemo_metastatic_any = True`.**
AURA3 enrolled patients with T790M after first/second-gen EGFR TKI failure; chemotherapy-naive in the metastatic setting was an inclusion criterion. The hand-curated `excluded.post_chemo_metastatic_any = True` is correct — the trial excluded prior chemo for metastatic. Drug class, prior_state, biomarker (EGFR-mut, EGFR-T790M), year_pc=2017, target_node `post-EGFRTKI|EGFR-T790M|NSCLC` all match. OK.

### C2. HERTHENA-Lung01 (NCT04619004) — **clinically faithful.**
Required prior EGFR TKI (osimertinib in 86% of enrolled), 1+ platinum chemo, EGFR-mut. Encoded with `post_egfr_tki=True, post_osimertinib=True`, `excluded.post_chemo_metastatic_any = False` (correct — prior chemo required not excluded). Drug class HER3-ADC. Year_pc=2023. OK.

### C3. TROPION-Lung01 (NCT04656652) — **partially clinically faithful but operationally broken.**
The trial enrolled mixed-biomarker NSCLC (with and without actionable genomic alterations) and read out a pre-specified EGFR-mut subgroup. The hand-curated record sets `tumor_type = "NSCLC-other"` and `egfr_mut = None`, which is a literal reading of the trial-level enrolment but **operationally locks the trial out of the trial-DAG** (see A6). The note says "partially in scope (EGFR-mut and AGA subgroups)" but the encoding does not reflect that. The fix is to split the record (see A6 fix) or set `egfr_mut=True` with `subgroup_readouts=["AGA_subgroup"]` so liberal tolerance can credit the EGFR subgroup readout per `v3_08_compute_pooled_efdpr.py:57-69`.

### C4. PROFILE 1014 (NCT01154140) — **OK.**
This was added to the corpus from systematic search (not hand-curated) and N16 correctly cites it with year_pc=2013. The trial is the canonical 1L crizotinib vs chemotherapy ALK pivotal trial. ESMO cites it, NCCN cites it, the brief title confirms the indication. The introduction year on N16 is 2014 (FDA crizotinib full approval was Nov 2013; the 1L recommendation followed in 2014 ASCO/NCCN). Year_pc=2013 ≤ year_intro=2014, so temporal precedence holds. OK.

### C5. FLAURA-CNS dropped — **defensible.**
FLAURA-CNS was a planned but never-launched trial; ClinicalTrials.gov has no NCT entry. Dropping it from the supplementary list and relying on the FLAURA brain-mets subgroup analysis (folded into N22's citation of NCT02296125) is defensible. The original round-0 supplementary entry for FLAURA-CNS was misidentified as NCT04379635 (per the DROP set in `v3_05_merge_and_kappa_nsclc.py:121`); confirming that NCT was not FLAURA-CNS and dropping is correct. OK.

**Net on the 5 corrected/added supplementary trials**: 3 of 5 are clinically faithful (AURA3, HERTHENA, PROFILE 1014); 1 of 5 is correctly dropped (FLAURA-CNS); 1 of 5 is partially faithful but operationally broken (TROPION-Lung01). The round-0 NCT-misidentification pattern (10 prior + 4 round-0 = 14 total caught) is not repeating in v3 round-1; the remaining issues are encoding-pipeline, not NCT-identity.

---

## D. EGFR vs ALK framing in Paper A — fair?

### D1. "NSCLC EGFR-only EFDPR 0.71 (12/17 evidence-free)"

**This figure is materially inflated by encoding artefacts.** Of the 12 strict-evidence-free EGFR nodes:
- N1 is a deterministic encoding bug (A1) — would never be supported under any tolerance.
- N2, N3, N4, N25 are token-set-cardinality artefacts (A2) — supported under ESCAT/liberal, mechanically excluded under strict.
- N9 has a mechanically-excluded cited trial (A6).
- N11 has a missing cited trial due to a regex bug (A7).
- N12, N21, N23 are mechanically locked into evidence-free by the `"investigational (other)"` drug-class strip (A8, A12).

Honest count if the encoding bugs are fixed: 12 - 4 (N2/N3/N4/N25) - 1 (N1) - 1 (N9 with TROPION-Lung01 split) = **6/17 = 0.35 strict EFDPR**, and after PAPILLON (N11) is added it would drop to **5/17 = 0.29 strict EFDPR** for NSCLC-EGFR. That is a non-trivial flip of the headline narrative. The post-osimertinib decision space *is* genuinely fragmenting (N12, N21, N23 reflect real clinical-recommendation positions where pivotal trial readout is still pending or sub-population-restricted), but the magnitude reported in Paper A (0.71) exaggerates the gap by ~35 percentage points relative to a fully-honest encoding (~0.29-0.41). 

**As a thoracic oncologist I would write this as:** "in v3, NSCLC EGFR strict EFDPR is reported as 0.71, but ~5 of the 12 evidence-free flags reflect biomarker-token-encoding artefacts (compound-token mismatch, redundant-token over-tagging, drug-class strip filter). Under fixed encoding the figure is approximately 0.35-0.47, still substantially above the 0.25 null but closer to the mBC-only 0.40 than the dramatic 0.71 contrast suggested by Paper A's discussion." The paragraph "NSCLC EGFR post-osimertinib is the largest concentrated gap" (Paper A line 135-136) is directionally correct but should be stripped of the magnitude claim.

### D2. "NSCLC ALK-only EFDPR 0.25 (P=0.63)" — would a thoracic oncologist agree ALK is well-evidenced?

**Mostly yes, with one caveat.** The ALK landscape genuinely IS better-stratified by trial than the EGFR landscape — ALEX, ALTA-1L, CROWN are clean head-to-head 1L 2nd-gen-vs-crizotinib trials; the post-crizotinib 2nd-gen TKI set (ASCEND, J-ALEX, ALUR, ALESIA) is well-populated; lorlatinib has CROWN (1L) and the registrational phase 1/2 (post-2nd-gen). The framework correctly picks this up.

**But the ALK n=8 is artificially boosted by N13/N14 duplication (A9) and N20 brain-mets-stripping duplication (A10).** Honest ALK n is 6 (after merging N13+N14 and dropping or fixing N20). Honest ALK strict EFDPR would be 2/6 = 0.33 (still fails to reject P~0.51), or with N18 ESCAT-supported instead of strict-evidence-free, 1/6 = 0.17 (still fails to reject). The "well-evidenced" conclusion holds, but the exact 0.25 figure depends on the inflated denominator.

The **larger conceptual concern** about the ALK side is that resistance-mutation profiling and the salvage trial agenda (ALK G1202R, MET-bypass, ALK rechallenge) are legitimately understudied — the framework correctly flags N18/N19 as evidence-free at strict, but does not capture the qualitative gap that ALK 4L+ recommendations are increasingly extrapolative. ALK is well-evidenced for 1L-2L; the "post-lorlatinib post-everything" position is as evidence-thin as the post-osimertinib EGFR position. The framework cannot show this because the ALK guideline tree only encodes 8 nodes and stops at N19. Adding 2-3 ALK 3L+/4L+ nodes would close the gap and would NOT support the manuscript's "ALK is well-evidenced" framing.

---

## E. Out-of-scope decisions — clinical justification?

Paper A line 151 (Limitations): "Driver-negative NSCLC, KRAS G12C, ROS1, RET, MET ex14, NTRK, BRAF V600E, and HER2-mutant NSCLC are out-of-scope for v3; their inclusion is deferred to v4."

**Reasonable as a v3 scope decision**, but two things:
1. **The NSCLC corpus is biomarker-filtered (F5) to EGFR or ALK only**, so excluding the other drivers is consistent. Clinically defensible.
2. **HER2-mut NSCLC and KRAS G12C** are particularly recent additions to the standard-of-care space (DESTINY-Lung01/02 for HER2-mut, KRYSTAL-12/CodeBreaK 200 for KRAS G12C), and a thoracic oncologist might argue they should have been included in v3 since both have phase 2/3 pivotal trials with FDA approvals predating the freeze date. However, including them would require expanding the schema (`her2_mut`, `kras_g12c` fields), encoding a new guideline-tree branch, and re-running the dual-annotator pipeline — substantial scope inflation. The v4 deferral is defensible but should be more concretely scoped (e.g., "v4 will add KRAS G12C and HER2-mutant NSCLC and is targeted for 2026Q4").

The driver-negative NSCLC exclusion (immunotherapy era) is acceptable because it's a different framework problem (no biomarker stratification), but the manuscript should say WHY (not just "out of scope") — the framework's biomarker-state node space is most useful for biomarker-driven settings.

---

## F. Single-annotator NSCLC tree concern (the meta-issue)

**The NSCLC guideline tree was encoded by Claude alone, with no clinical second reader.** Paper A line 87 says it was "hand-curated from the source guidelines," and Paper B mentions dual-annotator only for the trial-extraction step. The NSCLC guideline tree (25 nodes) had no human clinical second pass and no Codex/GPT-5 second pass. The mBC tree (v2.0.0) similarly had a single hand-encoding. The dual-annotator pipeline applies to the *trial corpus* (Annotator A vs B with a κ gate) but **not** to the *guideline tree* (single annotator, no κ).

This is a known framework asymmetry, but in v3 it bites harder because:
- The NSCLC nodes encode 7 nodes (N12, N21, N23) where the recommended class is `"investigational (other)"`, which mechanically locks them out of supporting evidence at every tolerance level. A second reader would have caught this immediately.
- N1's compound token bug would have been caught by a second reader running the encoding through the concordance algorithm before publication.
- N5's bevacizumab-vs-anlotinib drug-class miscoding (at the trial level, but with a clinical-recommendation node) is the kind of thing a clinical second reader catches in 30 seconds.

**Process recommendation for v4 and beyond**: the guideline tree itself needs at least one clinical second annotator (human or Codex) and a Cohen's κ on the encoding choices (state token, biomarker token, drug class). The mBC tree got away with single-encoding because it was iterated across 4 prior reviewer cycles; the NSCLC tree got 0 prior reviewer cycles before v3 freeze. This single-cycle exposure is the structural cause of the issues in this review.

---

## G. Concrete asks (12)

1. **Fix N1's biomarker token (A1).** Either change `"EGFR-mut/EGFR-ex19del-or-L858R/NSCLC"` to `"EGFR-mut/NSCLC"` or add `"EGFR-ex19del-or-L858R": {"EGFR-ex19del", "EGFR-L858R"}` to the `ESCAT_GROUPS` map at `v3_08_compute_pooled_efdpr.py:20`. Without this, FLAURA cannot ever support its own cited node at any tolerance.

2. **Fix the strict biomarker-set cardinality artefact (A2).** Either strip redundant sub-specification tokens (`EGFR-ex19del`, `EGFR-L858R`, `EGFR-T790M`) when the parent `EGFR-mut` is present, or define strict tolerance as set-superset rather than set-equality. Without one of these fixes, strict tolerance is measuring biomarker-token-string equality and not clinical concordance — and the N2/N3/N4/N25 strict-evidence-free flags are encoding artefacts, not real evidence gaps.

3. **Fix the F5 PAPILLON regex bug (A7).** Change `r"\bEGFR.?exon.?20\b"` to `r"EGFR[\W\s]*[Ee]xon[\W\s]*20"` (or similar without trailing `\b`). Re-run F2-F8. PAPILLON (NCT04538664) is the registrational EGFR ex20ins 1L amivantamab+chemo trial; its absence makes N11 evidence-free as a corpus-completeness artefact.

4. **Re-encode FL-ALTER (NCT04028778) to a non-bevacizumab drug class (A3).** Anlotinib is a multikinase VEGFR-TKI, not bevacizumab. Suggested class: `"VEGFR-TKI + EGFR TKI"`. With this fix, N5's strict support reduces to RELAY (NCT02411448) only, which is the correct clinical reading.

5. **Add explicit drug classes for the "investigational (other)" nodes (A8, A12).** N12 needs `"EGFR ex20ins-TKI (mobocertinib)"` or similar; N21 needs `"MET-TKI + osimertinib"` (savolitinib + osi combination); N23 needs an explicit class for "post-amivantamab investigator's choice" or the node should be dropped. Without this, three NSCLC-EGFR nodes are mechanically locked into evidence-free at every tolerance.

6. **Re-extract SAVANNAH (NCT03778229) and SAFFRON (NCT05261399) with corrected drug class and a new `met_amplification` biomarker schema field (A12).** SAVANNAH is the canonical NCCN-cited trial for N21; without the schema field for MET amp and the drug-class label, it cannot ever support N21.

7. **Split TROPION-Lung01 (NCT04656652) into an EGFR-mut subgroup record + an AGA-positive non-actionable record (A6).** Currently the trial is fully excluded from the DAG by the `tumor_type = "NSCLC-other"` skip. The pre-specified EGFR-mut subgroup readout is the basis for the NCCN N9 citation and should support N9 under ESCAT or liberal.

8. **Merge N13 and N14 (A9).** Both are first-line ALK-rearranged 2nd-gen ALK TKI nodes; the only difference is the cited-trial attribution (ALEX vs ALTA-1L). After merging, ALK n=7 and the `nsclc_alk_only` denominator is honest. Alternatively: drop the duplicate and explicitly justify the split with a clinical distinction (which I cannot produce — both ALEX and ALTA-1L are concurrent 1L 2nd-gen ALK TKI trials).

9. **Drop N20 or implement a brain-mets subgroup-readout match-criterion (A10).** Currently N20's `brain-mets` token is stripped, making N20 a duplicate of N13+N14+N15. If the panel intent is "brain-mets-active TKI is preferred," the framework should test for a `brain_mets_intracranial_PFS_subgroup` readout — not strip the token.

10. **Add a clinical second-annotator pass to the NSCLC guideline tree (single-annotator concern, F).** The mBC tree got 4 prior reviewer cycles; the NSCLC tree got 0. A 25-node tree with a clinical second reader is a 1-day exercise and would have caught items 1, 4, 5, 7, 8 before freeze. The pre-registration's dual-annotator gate covers the trial-corpus extraction but not the guideline-tree encoding; this is a structural gap that should be pre-registered for v4.

11. **Stop calling the NSCLC EGFR EFDPR figure 0.71 in the abstract (D1).** It is materially inflated by 4-5 encoding artefacts. After fixes 1-3 and 5-7, the figure is approximately 0.29-0.47 (depending on how many of the encoded fixes are accepted). The pooled headline still rejects, but the EGFR-vs-ALK contrast that drives the "post-osimertinib is the largest concentrated gap" narrative would be more like a 2x ratio (0.45 vs 0.25) than a near-3x ratio (0.71 vs 0.25). The Discussion should be re-written to reflect the post-fix magnitudes, with explicit disclosure of the strict-tolerance encoding artefacts as a known limitation.

12. **Rename the `"EGFR TKI 3rd-gen (osimertinib)"` drug class to `"EGFR TKI 3rd-gen"` and document that osimertinib is the only commercially-approved member (B-spot-check follow-up).** The current parenthetical reads as if the class is osimertinib-specific, but the encoding pools nazartinib/rociletinib/naquotinib/ASP8273 into the class. Three of the N22 supporting trials are non-osimertinib failed-development 3rd-gen TKIs; this should be transparent in Methods.

---

## VERDICT

**MAJOR REVISION.**

The framework is sound, the 4 round-0 NCT-misidentifications are cleanly corrected and verified against ClinicalTrials.gov briefTitles, the dual-annotator trial-corpus pipeline is working as designed, and the pooled headline (EFDPR 0.48, P=0.0004) will survive every reasonable re-encoding I have requested above (under the worst-case full-fix scenario, pooled EFDPR drops to roughly 0.40 and pooled P moves to ~0.005-0.01, still rejects). The NSCLC ALK comparator-non-rejection (P=0.63) is structurally correct as a description of the well-stratified 1L-2L ALK trial landscape.

**However, the NSCLC EGFR-only headline (0.71, 12/17 evidence-free)** is materially inflated by 4-5 encoding artefacts that a single hand-encoding pass without a clinical second reader did not catch:
- N1 has a deterministic compound-token bug that locks FLAURA out of supporting its own cited node at every tolerance level.
- N2, N3, N4, N25 are strict-only artefacts of biomarker token-set cardinality (sub-specification tokens at the trial level vs parent token at the guideline level).
- N9 is mechanically excluded because TROPION-Lung01 is filtered out of the DAG entirely.
- N11 (PAPILLON ex20ins 1L) is missing because of an F5 regex word-boundary bug.
- N12, N21, N23 are locked into evidence-free at every tolerance because their recommended class `"investigational (other)"` is the very class the DAG-builder strips.

After fixing these, NSCLC-EGFR strict EFDPR is approximately 0.35-0.47, the pooled headline still rejects, and the EGFR-vs-ALK contrast survives but with a less dramatic magnitude (roughly 2x rather than the headline ~3x). The "post-osimertinib is the largest concentrated gap" narrative is directionally correct but the magnitude claim should be retired.

This is a **MAJOR revision** because the headline NSCLC EGFR figure (0.71) is the single most-cited number in the v3 abstract and Discussion, and it is the figure that does not survive a fully-honest re-encoding. The pooled rejection survives, but the manuscript needs to (a) fix the encoding bugs, (b) re-run the EFDPR computation, (c) re-write the EGFR-vs-ALK contrast paragraph, and (d) add a clinical second-annotator pass on the NSCLC guideline tree as part of the v3.0.1 release. The 4 NCT corrections are good, but the pattern-of-error has shifted from NCT-identity (well-controlled) to encoding-pipeline (the new failure mode that needs the same kind of multi-round adversarial attention that v1+v2 received).

I would re-review a v3.0.1 revision that addresses asks 1, 2, 3, 5, 7, 11 at minimum. I would not block publication on asks 4, 6, 8, 9, 10, 12, but I would expect them to be addressed before journal submission.

— Reviewer (Thoracic + Breast MO, ESMO/ASCO panel)
