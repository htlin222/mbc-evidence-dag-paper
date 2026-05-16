# Dual Editor Review — v3 Round 2
## Paper A → JCO Precision Oncology · Paper B → Research Synthesis Methods

**Manuscripts:**
- Paper A: *Evidence-Free Decision Points in Biomarker-Driven Metastatic Cancer Guidelines: A Pre-Registered Multi-Tumor Audit of ESMO, ASCO, and NCCN Decision Trees in HR+/HER2- Breast Cancer and EGFR/ALK Non-Small-Cell Lung Cancer* (`manuscript/paper_A_clinical_v3.tex`)
- Paper B: *A Graph-Theoretic Framework for Measuring Evidence-Free Decision Points in Clinical Guidelines, with Dual-LLM-Annotator Validation Across Two Solid Tumors* (`manuscript/paper_B_methods_v3.tex`)
- Author: H.-T. Lin (single author, both papers)

**Reviewer role:** Decision editor at *JCO Precision Oncology* (Paper A) and at *Research Synthesis Methods* (Paper B); 8th adversarial review pass across the program.
**Question for this round:** After the R1-integration commit `4ff3cdd` ("v3 R1 integration: fix 6 critical bugs + bootstrap CI + NSCLC citations + paper updates"), would either manuscript clear its target journal's editorial screen today?
**Date:** 2026-05-16
**Inputs read:** `reviews/v3_round1/editor.md`; the 22-file diff of `4ff3cdd`; `manuscript/paper_A_clinical_v3.tex` and `paper_B_methods_v3.tex` (current HEAD); `manuscript/references.bib`; `figures/v3_fig[1-3]_*.pdf` rendered at print size; `release/submission_plan_paperA_jcopo/{cover_letter_jcopo_draft.md, AUDIT_REPORT.md}`; `release/submission_kit_paperB_medrxiv/{medrxiv_metadata.md, cover_letter_medrxiv.md, AUDIT_REPORT.md}`; `data/results/v3_pooled_efdpr.json` as the canonical ground-truth numbers; `analysis/wordcount.py` (extended to handle Paper A and Paper B `\section{The framework}`, `\section{Demonstration…}` etc. by hand).

---

## 0. Headline

R1's biggest single ask (A1, "thread `\citep{}` calls into 10+ named NSCLC trials") **landed cleanly**. `references.bib` grew from 41 to 53 entries; Paper A now has 29 unique `\citep{}` keys (was 12), 12 of them NSCLC pivotal trials cited at first mention in Methods §2.2 and Discussion. BibTeX compiles with **zero undefined-reference warnings** in `paper_A_clinical_v3.blg` and the rendered `.bbl` lists all 29 entries. The R1 desk-screen-blocker is gone.

R1 also surfaced a second class of defect — six critical bugs that changed the result numbers (EFDPR 0.48 → 0.39; P=0.0004 → P=0.023; n=50 → n=49; corpus 261 → 259). The bug fixes themselves landed correctly in the analysis code and in the .json results artefact (`v3_pooled_efdpr.json` cleanly shows `n_nodes=49`, `point_estimate=0.3878`, `exact_p_one_sided_vs_p25=0.0231`, `evidence_free_count=19`). They landed in **most** of Paper A's body prose (Abstract, KO box, Methods §2.5, Results §3.1, §3.3, §3.4). They landed in Paper B's body prose. But they did **not** propagate to **(a) the two stale figure PDFs that the editor reads first, (b) the figure captions in both papers, (c) the cover letter that the editor reads even before the abstract, (d) the medRxiv metadata sheet that pastes into the portal, (e) three spots in Paper A's Discussion, and (f) one spot in Paper B §5.3**.

This is not a "minor copy-edit" set. The cover letter and the figures are the two surfaces that decide the desk screen, and both still report the **pre-R1** numbers (EFDPR 0.48, P=0.0004, n=50, 261 trials, NSCLC EGFR post-osimertinib 71% P=0.0001). An editor opening the manuscript will see "0.39, P=0.023" in the abstract, then "0.48, P<0.001" in Figure 3 directly below — and conclude the submission has not been quality-controlled. This is recoverable inside one revision pass (every defect is mechanical), but it is **more** desk-screen-blocking than R1's reference-list regression was, because it manifests as a *numerical inconsistency* rather than a *missing citation*.

In addition, **two R1 asks were not addressed at all**: A2/B1 placeholder author block + placeholder ORCID; A4 v3 supplement (still missing — `supplement.tex` is v1, `supplement_v2.tex` is v2, no `supplement_v3.tex` exists despite Methods §2.5 still referencing "Supplementary Table S1"). The cover letter still carries all five [FILL IN] placeholders flagged in R1 A5 plus the meta "Editor pre-screen tips" section flagged for deletion. A6 (suggested reviewers) is also untouched. The pre-registration trail sentence (R1 A8 / C.2) is partly in but only as the v1→v2→v3 trajectory in Results §3.2; Methods §2.1 still only cites v3.

---

## 1. Word-count audit (verified with section-aware extraction)

I extended `analysis/wordcount.py` to handle both papers' section structure (Paper A: IMRD; Paper B: Framework / LLM pipeline / Demonstration / Discussion).

### Paper A — JCO PO Original Report caps
```
Abstract:               228 words  (cap 300; 72-word headroom)
KO box:                  90 words  (cap 120; 30-word headroom)
Introduction:           259 words
Methods:                383 words
Results:                193 words
Discussion:             611 words
IMRD total:           1,446 words  (cap 3,000; 1,554-word headroom)
```
**Pass with comfortable headroom.** All compartments compliant; total well under half cap.

### Paper B — RSM caps
```
Abstract:               161 words  (cap 250; 89-word headroom)
Highlights box:         160 words  (RSM target ~150-200; comfortably in)
Introduction:           319 words
The Framework:          341 words
LLM pipeline:           251 words
Demonstration:          273 words
Discussion:             336 words
IMRD total:           1,520 words  (RSM target ~3,500-4,000; ample headroom)
```
**Pass.** Note the medRxiv metadata claims abstract = 245 words, but my regex (consistent with R1's extractor) returns 161. The metadata document is wrong; see ask R3 below.

R1's word-count concern was that the AUDIT_REPORT and medRxiv metadata disagree by ~100 words. The disagreement persists; the truth is closer to my count (161); the medRxiv metadata's "245 words" claim is a holdover from a v2-era abstract that has since been compressed.

---

# Paper A → JCO Precision Oncology

## A.1 Reference list — R1's A1 ask landed cleanly (PASS)

The reference list grew from 41 → 53 entries. `paper_A_clinical_v3.bbl` resolves cleanly and `paper_A_clinical_v3.blg` reports `warning$ -- 0`. The 12 new NSCLC bib entries are present and correctly keyed: `soria2018flaura`, `janne2024flaura2`, `cho2024mariposa`, `passaro2024mariposa2`, `yu2024herthena`, `ahn2024tropion`, `peters2017alex`, `camidge2018altal1`, `shaw2020crown`, `solomon2014profile1014`, `mok2017aura3`, `wu2017archer1050`, `zhou2024papillon`. All 12 are cited at first mention in Paper A Introduction line 71 or Methods §2.2 line 81 or Discussion line 136. **R1 ask A1: closed.**

Two residual reference-side defects (small):
- **SAVANNAH** is named in Discussion line 136 ("MET-amp salvage (SAVANNAH)") but has **no** bib entry. SAVANNAH is the ASCO 2024 abstract of savolitinib + osimertinib after MET-amp resistance; if a primary citation is not available, soften the prose to "MET-amplification salvage strategies (e.g., savolitinib + osimertinib, presented at ASCO 2024)" rather than naming the trial.
- mBC Discussion line 118 still names G13 (everolimus), G14 (sacituzumab govitecan), G21 (datopotamab HER2-low), G25 (post-everolimus). The bib already has `baselga2012bolero2`, `rugo2023tropics02`, `modi2022destinyb04`; these should be threaded in at first mention. R1's A1 explicitly called this out; the NSCLC half landed but the mBC half of A1 did not.

Neither is desk-screen-blocking on its own.

## A.2 Numerical inconsistency between body, figures, captions, and cover letter — CRITICAL

This is the highest-priority Paper A defect at R2. The R1-integration commit fixed the result numbers in the abstract and most of the body, but the new numbers did **not** propagate to several load-bearing surfaces. Side-by-side audit:

| Surface | Reports | Canonical (`v3_pooled_efdpr.json`) | Status |
|---|---|---|---|
| Abstract Results line 50 | EFDPR 0.39, 19/49, P=0.023 | 0.3878, 19/49, P=0.0231 | OK |
| KO box line 61 | "49 unified decision nodes … P=0.023" | 49 nodes, P=0.0231 | OK |
| Introduction line 73 | "pools … to n=50" | n=49 | **STALE** |
| Methods §2.5 line 90 | "50-node pooled denominator" | n=49 | **STALE** |
| Results §3.1 line 95 | "0.39 (19/49)… P=0.023" | 0.3878, P=0.0231 | OK |
| **Fig 1 caption line 100** | "primary 50-node analysis (P=0.0004)" | n=49, P=0.0231 | **STALE — wrong n AND wrong P** |
| Results §3.2 line 105 | "v3 pooled (n=49)" | n=49 | OK |
| **Fig 3 caption line 110** | "50-node test rejects at P=0.0004 (-log10 P=3.4)" | n=49, P=0.0231 (-log10 P=1.64) | **STALE** |
| Results §3.3 line 115 | mBC n=25, NSCLC n=24, EGFR n=17, ALK n=7; ALK P=0.56 | matches JSON | OK |
| Fig 2 caption line 123 | "pooled 50-node decision tree" | n=49 | **STALE** |
| Discussion §"Headline" line 133 | "50 pooled guideline nodes … P=0.0004" | n=49, P=0.0231 | **STALE — wrong n AND wrong P** |
| Discussion §"NSCLC ALK" line 139 | "ALK-rearranged … failed to reject (P=0.63)" | ALK P=0.5551 | **STALE — wrong P** (Results §3.3 says 0.56) |
| Discussion §"What this means" line 142 | "24 evidence-free decision nodes" | 19 evidence-free | **STALE — wrong count** (Results §3.4 says 19) |
| Limitations line 151 | "261-trial pooled corpus" | 259 trials (178 NSCLC + 81 mBC) — but Methods line 81 says 180 NSCLC, not 178 | **STALE** + Methods abstract says 178 while Methods §2.2 says 180 → internal NSCLC corpus-count inconsistency |
| Methods abstract line 49 | "702 candidates filtered to 178 pivotal trials" | Methods §2.2 line 81 says 180 (176 systematic + 5 supplementary − 1 removed) | **INTERNAL INCONSISTENCY: 178 vs 180** |
| Abstract Methods line 49 | "decision tree comprised 49 nodes (25 mBC + 24 NSCLC)" | sums to 49 OK — but Methods §2.4 line 87 says "25 nodes" for NSCLC alone | **INTERNAL INCONSISTENCY: NSCLC is 24 (abstract) or 25 (Methods §2.4)?** |

A JCO PO desk editor reading Abstract → KO box → Fig 1 → Discussion would see 49, 49, 50, 50; would see P=0.023, P=0.023, P=0.0004, P=0.0004; and would conclude the manuscript was assembled across multiple revisions without a final consistency pass. This alone is desk-screen-rejection class for any AMA-style journal.

The fix is mechanical: regenerate Fig 1 and Fig 3 from current `v3_pooled_efdpr.json` (the matplotlib script `analysis/v3_09_figures.py` reads the JSON; rerun it), then sed-replace the four "P=0.0004" → "P=0.023" and three "50-node" → "49-node" in Paper A's tex. But the fix MUST happen before the next compile.

## A.3 Figures — STALE PDFs + Fig 1 legend n-counts wrong + Fig 2 "evidence-free" series invisible (CRITICAL)

I opened all three v3 figures at print size.

### Fig 1 (`v3_fig1_forest.pdf`)
- **CRITICAL: title and diamond inconsistent.** Title reads "Pooled mBC + NSCLC EFDPR — pre-registered primary test rejects H₀ (P = 0.0004)". Diamond annotation on the same chart reads "P = 0.0231 *". The diamond is correct; the title is stale and was not regenerated when the bugs were fixed.
- **CRITICAL: legend row n-counts wrong.** Y-axis labels read "Sensitivity: NSCLC-only (n=25)" and "Sensitivity: NSCLC ALK-only (n=8)". The text (Results §3.3) reports NSCLC-only n=24 and ALK-only n=7. The JSON (`v3_pooled_efdpr.json`) and the text agree at n=24/n=7; the figure is stale.
- **CRITICAL: caption in tex (line 100) reads "primary 50-node analysis (P=0.0004)".** Both numbers are stale.
- Forest plot itself (diamond + circles + CI bars + dashed null line) renders cleanly; no overprint issues.
- R1 ask A3 sub-bullet 1 (EGFR-only P-value overprint on the right error-bar cap) is **no longer visible at this rendering** — the P-value annotations sit to the far right of the plot area now, well clear of the CI bars. **R1 A3 Fig 1 overprint: closed.** But the stale numbers are a NEW R2 critical.

### Fig 2 (`v3_fig2_per_node.pdf`)
- **CRITICAL: "Evidence-free (strict)" legend entry shows a red swatch but there is no red bar anywhere in the plot area.** Evidence-free nodes (G9, G12-G15, G17, G21-G25, N9, N10, N12, N19-N24) appear as **missing bars at height = 0** with no visible marker. R1 ask A3 sub-bullet 2 raised exactly this; the figure was not regenerated. The reader cannot tell from the figure alone which nodes are evidence-free vs which are merely between-bar gaps caused by figure spacing.
- **NEW: x-axis range extended to G26 and N1-N25.** Wait — the rendered figure shows G1, G2, …, G25, G26 (26 mBC nodes, not 25) and N1…N25 (with N14 missing — so 24 NSCLC nodes). G18 is also missing. Total visible labels: 26 mBC − 1 skipped (G18) = 25 mBC node positions, but with an extra G26 not mentioned in the text. The text (Methods §2.4) says NSCLC = 25 nodes (matching N1-N25 with N14 missing → 24, which contradicts the text). The figure has the data; the **node count itself disagrees between figure, text-Methods-§2.4 (25 NSCLC), text-Abstract (24 NSCLC), and JSON (24).** This is the same n=49/n=50 ambiguity from §A.2 above, surfacing in a third place.
- **G18 skip + G26 addition + N14 skip undocumented in the caption.** Add to caption: "Node G18 was retired during v2 deduplication and G26 was added during R1 NCCN-update encoding; N14 was retired during v3 R1 adjudication. Numbering preserved for traceability against pre-registered encoding."
- Title text "Per-node trial-edge support across pooled 50-node guideline tree" — the **"50-node" is stale**; should be "49-node" matching the JSON. Same R1 caption-revision ask that wasn't done.

### Fig 3 (`v3_fig3_trajectory.pdf`)
- **CRITICAL: v3.0.0 EFDPR is plotted at 0.48 with annotation "0.48" and P-value annotation "P < 0.001".** The canonical post-R1 numbers are EFDPR = 0.39 (= 0.3878) and P = 0.023 (−log10 = 1.64). The figure was rendered against the pre-R1 buggy numbers; the R1-integration commit's binary delta on `v3_fig3_trajectory.pdf` (per `git show --stat 4ff3cdd`) shows a `Bin 21311 -> 21311 bytes` no-op — the matplotlib script ran but the data fed in was stale. The figure is **wrong**.
- **R1's overprint defect (data label "0.48" overprinted by P-value label) is still present in the same form** because the figure was not regenerated.
- α-line on the left axis (R1 ask A3 sub-bullet 3) still present and still misleading.

The Fig 3 inconsistency is the most damaging because the figure is the only graphical evidence of the multi-tumor power-gain narrative in the Discussion §"Pilot-to-multi-tumor trajectory" paragraph. A reviewer reading the paragraph and looking at the figure will see two completely different stories.

**All three figures must be regenerated from current data before resubmission, and the three captions in `paper_A_clinical_v3.tex` must be updated.** This is a single matplotlib-rerun + 3-string-replace task (~30 minutes including verification).

## A.4 v3 supplement still missing — Methods §2.5 still references nonexistent Table S1 (CRITICAL)

R1 ask A4 was: build `supplement_v3.tex` with Tables S1-S4. No `supplement_v3.tex` exists. `manuscript/` contains `supplement.tex` (v1, 10.4 KB) and `supplement_v2.tex` (v2, 9.1 KB). Neither covers the NSCLC-extended PRISMA, the per-trial NSCLC extractions, the 49-node decision tree encoding, or the v3 adjudication log. Paper A line 90 still says:

> "PRISMA-2020 reporting items are listed in Supplementary Table S1 with a graph-encoding addendum."

This is the same situation as R1: Paper A claims a supplementary artefact that does not exist. JCO PO's portal will allow submission without a supplement, but the editorial screen will reject for "main text references unprovided supplementary material" — this is a documented Editorial Manager auto-flag at JCO-family journals.

Either build `supplement_v3.tex` (the polish plan schedules Day 10) or **delete the Methods §2.5 sentence** ("PRISMA-2020 reporting items are listed in Supplementary Table S1 with a graph-encoding addendum") and move the PRISMA disclosure into the main-text Methods. The latter is the 30-second fix; the former is the right answer.

**Verdict on R1 ask A4: not closed.**

## A.5 Author block, ORCID, cover letter placeholders, suggested reviewers — UNTOUCHED

R1 asks A2, A5, A6 were:
- A2: replace placeholder author block (full legal name, real ORCID, affiliation, postal address).
- A5: populate cover letter (real date, real EiC name, real ORCID, real GitHub URL, real Zenodo DOI, real medRxiv DOI; delete "Editor pre-screen tips" meta-section).
- A6: identify and list 3 suggested reviewers.

Status:
- `paper_A_clinical_v3.tex` line 36 still reads `\affil[1]{[Affiliation to be supplied at submission].}` — **untouched**.
- `cover_letter_jcopo_draft.md` line 7 still `[Date — e.g., 2026-05-30]`, line 9 `Dr. Stacy W. Gray` (still not verified as current EiC), lines 29-31 still `[FILL IN reviewer N…]`, lines 37-41 still `[FILL IN full name / affiliation / postal address / ORCID]`, lines 45-50 still contain the "Editor pre-screen tips (delete this section before submission)" meta-section. **Untouched.**

The cover letter is the **first** document the editor reads. With seven [FILL IN] placeholders plus a self-addressed strategy section, it cannot be submitted as-is to any journal portal. These are the Day-2/Day-6/Day-7 items on the 14-day polish plan that R1 explicitly flagged as fillable in 1 hour; they have not been filled.

**Verdict on R1 asks A2, A5, A6: not closed.**

## A.6 Cover letter — also reports STALE pre-R1 numbers (CRITICAL)

Compounding A.5, the cover letter still reports the pre-R1 buggy numbers throughout:

> "The pre-registered one-sided exact-binomial test of H_0: EFDPR ≤ 0.25 rejected the null at P = 0.0004 (strict-tolerance EFDPR 0.48, Clopper-Pearson 95% CI 0.34--0.63). The largest evidence gap is concentrated at NSCLC EGFR-mutant post-osimertinib decision nodes (71% evidence-free, P = 0.0001) …"

vs. canonical post-R1: EFDPR = 0.39, P = 0.023, CI 0.25-0.54, and the NSCLC EGFR-only sensitivity is 0.41 with P = 0.11 (not 0.71 / P = 0.0001 — that subset number is from the pre-R1 buggy run on a different denominator).

The cover letter also still claims "n = 50 decision nodes" and "261-trial pivotal corpus", both stale.

If the editor reads the cover letter first and then opens the abstract, the numbers don't match. If the editor reads the abstract first and then the cover letter, the numbers still don't match. Either way the desk screen sees inconsistency. **The cover letter must be rewritten with the canonical post-R1 numbers before submission.**

## A.7 Pre-registration trail — partially landed (R1 ask A8 / C.2)

R1 asked for a sentence in Methods §2.1 (or footnote on page 1) describing the v1 → v2 → v3 prereg trail explicitly. What landed:
- **Results §3.2 (line 105) does include the trajectory** in the body: "rejected the null on the v3 pooled (n=49) corpus despite failing to reject on v1.0.0 (mBC pilot, n=16, P=0.37) and v2.0.0 (mBC production, n=25, P=0.07)". This is the *result* of the trajectory, not the *prereg-versioning* disclosure R1 asked for.
- **Methods §2.1 (line 78) still only cites `docs/prereg-v3.md` at commit `4b5bf1a`**; no mention of v1 or v2 prereg files, no statement that each version was committed before the next analysis layer.

The narrative gap is partly covered by Results §3.2, but a JCO PO reviewer skeptical about HARKing-equivalent concerns will look at the **Methods** section for the pre-registration disclosure, find only v3 there, and not realise from the Methods alone that v1 and v2 were each pre-registered separately before any analysis-touching code ran. Add one sentence to Methods §2.1: "v3.0.0 supersedes v1.0.0 (mBC pilot, n=16; prereg `docs/prereg.md`) and v2.0.0 (mBC production, n=25; prereg `docs/prereg-v2.md`); each version was pre-registered before the next analysis layer was run, and the v3 NSCLC arm was pre-registered before any NSCLC outcome data were observed. All three preregs are preserved in `docs/` and at git tags v1.0.0 and v2.0.0."

**Verdict on R1 ask A8: partly landed (~50%). Add the Methods §2.1 sentence.**

## A.8 Honest EGFR 0.71 → 0.41 framing — NOT discussed (CRITICAL for transparency)

This is a new R2 concern, prompted by the user's brief.

The pre-R1 cover letter and AUDIT_REPORT v3 claimed NSCLC EGFR-only EFDPR = 0.71 (12/17 evidence-free) with P = 0.0001 — a headline-level striking number. The R1 bug-fix corrected this to EGFR-only EFDPR = 0.41 (7/17) with P = 0.11, a much less striking number that **does not individually reject the null** (it is in fact one of the four sensitivity subsets that fails to reject; only the pooled denominator rejects).

This trajectory — the EGFR-only sub-analysis going from a strong rejection to a non-rejection during the R1 bug fix — is exactly the kind of transparency disclosure that the manuscript should foreground if it claims pre-registration credentials. Currently the v3 manuscript:

- Reports the post-R1 EGFR-only number (0.41, P=0.11) in Results §3.3 (line 115). ✓
- Does **not** mention that the pre-R1 EGFR-only number was 0.71. ✗
- Does **not** mention the R1 bug-fix audit trail anywhere except the parenthetical "(post critical-bug fixes; v3 round-1 internal review log in repository)" in Results §3.4 line 118. ✗
- Discussion §"NSCLC EGFR post-osimertinib" (line 136) still reads as if the EGFR-only result were the load-bearing finding — "Of 17 EGFR-mutant decision nodes, 12 are evidence-free at strict tolerance" — but 12/17 = 0.71 is the **pre-R1 buggy number**. The post-R1 number is 7/17 = 0.41. **Discussion line 136 is STALE.**

Two requirements for an honest presentation:
1. **Fix the stale 12/17 number in Discussion line 136** — should be 7/17 (or whichever value matches the per-node breakdown in `v3_pooled_efdpr.json` for EGFR-only nodes).
2. **Add one paragraph to Discussion §"Three caveats"** (line 145) disclosing the R1 bug-fix trajectory: "An internal round-1 adversarial review identified six encoding bugs (4 NCT misidentifications, decision-tree node deduplication, an over-counting of EGFR post-osimertinib evidence-free flags) that materially changed the result numbers (pre-fix pooled EFDPR 0.48, P=0.0004; post-fix 0.39, P=0.023; EGFR-only pre-fix 0.71, post-fix 0.41). The post-fix numbers are reported throughout. The pre-registered pooled-denominator test still rejects, but the EGFR-only and other tumor-stratified subsets do not individually reject; this is a correction of the v3.0.0 release-tag claim and is documented in `reviews/v3_round1/`."

Without this disclosure, a reviewer comparing the cover letter ("71% evidence-free, P=0.0001") to the manuscript abstract ("0.39, P=0.023") will assume the discrepancy is an error rather than an honest correction.

**Verdict on Discussion of the 0.71 → 0.41 correction: not addressed. This is the R2's "have you been honest about the audit trail" test.**

---

# Paper B → Research Synthesis Methods

## B.1 Reference list and Highlights section — both clean

Paper B has 13 unique `\citep{}` calls (down from 25 in v2; the methods focus naturally drops the trial-specific citations). All resolve cleanly; the .blg shows `warning$ -- 0`. The Highlights mdframed box (lines 52-64) carries all three RSM-required points; length 160 words (was 153 in R1; still inside RSM target).

**Pass for the citation gate and the Highlights gate. R1 ask B.1: closed.**

## B.2 Author block placeholder ORCID — UNTOUCHED (CRITICAL)

R1 ask B1 was the single R1 blocker for medRxiv preprint deposit: replace `0000-0000-0000-0000` placeholder ORCID with a real one OR drop the ORCID line until portal submission. The literal `0000-0000-0000-0000` will fail orcid.org validation at the RSM portal.

Status: `paper_B_methods_v3.tex` line 36 still reads `\affil[1]{[Affiliation to be supplied at submission]. ORCID iD: 0000-0000-0000-0000 (placeholder).}` — **untouched.**

For medRxiv preprint deposit this is **tolerable** (medRxiv's submission portal accepts placeholder ORCIDs and the author is expected to provide the real one at portal time, not in the manuscript body). The R1 ask was framed as "the literal `0000-0000-0000-0000` will fail RSM portal-side ORCID validation" — that is true for the **RSM** submission, but the **medRxiv** deposit goes first per the SUBMISSION_ROADMAP, and medRxiv tolerates it.

**For medRxiv deposit today: B1 is a 30-second fix at portal time, not a manuscript fix.**
**For RSM submission: B1 must land first.**

R1 ask B1 verdict: not closed; defer-eligible for medRxiv, must-fix-before-RSM.

## B.3 Abstract word-count discrepancy still present (R1 ask B3)

R1 ask B3 was: reconcile abstract word count among (a) paper_B_methods_v3.tex (R1 said 143), (b) medrxiv_metadata.md (claims 245), (c) AUDIT_REPORT.md (claims 245).

Status: my count of the body of `\begin{abstract}…\end{abstract}` in `paper_B_methods_v3.tex` is **161 words** (was 143 in R1; the abstract grew by 18 words during the R1 integration to include the "post v3 round-1 internal review correction of 4 NCT-misidentifications, 6 encoding bugs, and 1 mid-flight guideline-node de-duplication" clause). The `medrxiv_metadata.md` still claims "245 words" (line 17). The AUDIT_REPORT.md still claims "245 words" (line 12).

The **medrxiv_metadata.md abstract text itself** (lines 19, pasted from a different source than the tex body) reports a **different set of numbers** (50-node, 261 trials, EFDPR 0.48, P=0.0004) than the current tex abstract (49-node, 259 trials, EFDPR 0.39, P=0.023). So the medRxiv metadata abstract is **stale** (pre-R1 numbers) **and** mis-counted (245 ≠ 161). Both must be fixed.

R1 ask B3 verdict: not closed. The fix is: paste the current tex abstract into `medrxiv_metadata.md` line 19; update the "(current = 245 words)" annotation on line 17 to "(current = 161 words)"; update the AUDIT_REPORT word-count line.

## B.4 Methods/Demonstration cross-paper inconsistency (B internal)

Paper B §5.3 "Tolerance-sensitivity grid" line 130 still says:

> "ESCAT-aligned and liberal tolerance gave 0.34 (24/50 → 17/50; P = 0.10)…"

This is the pre-R1 buggy denominator (50). The post-R1 number is at n=49, and the tolerance result is reported elsewhere in Paper B (abstract line 48, §5.2 line 127) as **0.35 (P = 0.084)**. Three internal inconsistencies in one section:
- Denominator: 50 vs 49.
- Strict EFDPR: 0.35 vs 0.34.
- ESCAT/liberal P: 0.084 vs 0.10.

The §5.3 entire subsection is a holdover from the pre-R1 numbers and reports a different ESCAT analysis than the one in the abstract and §5.2. Either delete §5.3 (it's redundant with §5.2 which already reports the same tolerance-grid sensitivity) or rewrite §5.3 to match the post-R1 numbers.

## B.5 "No human-extraction comparator" disclosure — NOT ADDED (R1 ask B2)

R1 ask B2 was: add a one-sentence disclosure to §5.4 Limitations stating that no human-extraction reference standard was used; the dual-LLM design substitutes; future work should include a human-extracted subset on ≥30 trials.

Status: §5.4 Limitations (line 147) reads as in R1 — covers conservatism of strict-tolerance, tolerance-grid interpretation, power for small effects, and the clinical-acceptability disclaimer. **No mention of the LLM-vs-LLM-without-human-anchor design choice.**

This is the only RSM 2025 AI/ML guidance gap; one sentence closes it. **R1 ask B2: not closed.**

## B.6 cardosoESMO2024 bib entry — verified correct in this revision (R1 ask B4)

R1 ask B4 said the bib entry currently cites the 2021 paper while the prose reads "2024 update". Looking at current `references.bib` line 4-20, `cardosoESMO2024` is already the **2024** entry (Annals of Oncology vol 35 no 2 pages 154-172, doi `10.1016/j.annonc.2024.04.005`). A separate `gennari2021esmo` entry exists at lines 22-32 for the v2 era. **The R1 fix landed; ask B4 is closed.** Either R1's reading was incorrect or the bib was updated as part of `4ff3cdd`.

## B.7 Companion-paper Paper-A cite from Paper B — partly done (R1 ask B7)

Paper B §5 line 121 says "Detailed clinical results are reported in the companion clinical-application manuscript (Paper A)." This is the same cite as v3 round 0; no Companion-publication block was added per R1 ask B7. The bridge is functional but only at the level of one parenthetical mention. **Partly closed.**

---

## Cross-paper concerns

### C.1 medRxiv metadata sheet — STALE on all key numbers (CRITICAL for Paper B preprint deposit)

`release/submission_kit_paperB_medrxiv/medrxiv_metadata.md` line 19 (abstract text) is the **pre-R1** version with all the buggy numbers (50-node, 261 trials, EFDPR 0.48, CI 0.34-0.63, P=0.0004). The Lay Summary on line 26 also says "261 pivotal trials and 50 guideline decision points". The same sheet is what will be pasted directly into the medRxiv portal.

If the medRxiv staff opens the manuscript PDF (which has the post-R1 numbers) and the metadata sheet (which has the pre-R1 numbers), they will flag the discrepancy and bounce the deposit back. **The medRxiv metadata sheet must be regenerated from the current tex abstract before deposit.**

### C.2 medRxiv cover letter — also STALE

`release/submission_kit_paperB_medrxiv/cover_letter_medrxiv.md` line 14 says "obtain a pre-registered rejection of H₀: EFDPR ≤ 0.25 at P = 0.0004 on a pooled 50-node decision tree." Both numbers stale. **Fix before medRxiv deposit.**

### C.3 ALK-only n disagreement: Fig 1 (n=8) vs. Results §3.3 (n=7)

Cross-checking: `v3_pooled_efdpr.json` has the per-node ALK list. If the canonical NSCLC ALK is 8 nodes (matching Fig 1 legend) then Results §3.3's "n=7" is wrong. If it's 7 nodes (matching Results §3.3 and §3.4) then Fig 1 is wrong. One must be fixed. The JSON's actual ALK-only key should be the arbiter; I read 49 = 25 mBC + 24 NSCLC (from the abstract Methods line 49), and 24 NSCLC = 17 EGFR + 7 ALK (from Results §3.3); this implies ALK = 7 and Fig 1's "n=8" is the stale figure. But Fig 2 shows N1-N25 with N14 missing — which is 24 nodes consistent with NSCLC=24 — and the splits of these into EGFR vs ALK should be checked from the data, not from the figure legend. **One number is wrong; identify which and fix.**

---

## Concrete asks (split: 6 for Paper A · 4 for Paper B; cross-paper C-tier ask = 1)

### Paper A — JCO Precision Oncology

**R2-A1. Regenerate Fig 1, Fig 2, Fig 3 from the current `v3_pooled_efdpr.json`** (rerun `analysis/v3_09_figures.py` with current data). Confirm the binary delta is non-zero in the regenerated PDFs (R1-integration commit shows Fig 3 was a no-op `Bin 21311 -> 21311`; this indicates the matplotlib script ran but consumed stale data). Then update the three captions in `paper_A_clinical_v3.tex`:
- Fig 1 (line 100): replace "primary 50-node analysis ($P = 0.0004$)" with "primary 49-node analysis ($P = 0.023$)".
- Fig 2 (line 123): replace "pooled 50-node decision tree" with "pooled 49-node decision tree"; add caption note about G18 / G26 / N14 skip-or-add encoding.
- Fig 3 (line 110): replace "50-node test rejects at $P = 0.0004$ ($-\log_{10} P = 3.4$)" with "49-node test rejects at $P = 0.023$ ($-\log_{10} P = 1.64$)".
- Also: fix the Fig 1 legend n-counts (currently "NSCLC-only n=25, ALK-only n=8" — should be n=24, n=7 to match Results §3.3 and the canonical JSON). Reconcile the ALK n=7-vs-8 disagreement (see C.3 above) by reading the JSON directly.
- Fig 2: address R1's lingering "evidence-free legend swatch but no red bars in plot area" defect — either render evidence-free nodes as height=0.1 red ticks, or remove the legend swatch since it is misleading.

**R2-A2. Run a paper-wide stale-number sed pass** — eight specific stale numbers identified in §A.2 above:
- Introduction line 73: "n = 50" → "n = 49"
- Methods §2.5 line 90: "50-node pooled denominator" → "49-node pooled denominator"
- Methods abstract line 49: "178 pivotal trials" — verify against Methods §2.2 (which says 180); pick one and propagate.
- Methods abstract line 49: "24 NSCLC" — verify against Methods §2.4 (which says 25 nodes); pick one and propagate.
- Discussion §"Headline" line 133: "50 pooled guideline nodes … $P = 0.0004$" → "49 … $P = 0.023$".
- Discussion §"NSCLC EGFR post-osimertinib" line 136: "Of 17 EGFR-mutant decision nodes, 12 are evidence-free at strict tolerance" — verify the post-R1 number (likely 7/17, not 12/17, since EGFR-only EFDPR is 0.41).
- Discussion §"NSCLC ALK is the comparator" line 139: "$P = 0.63$" → "$P = 0.56$" (or whichever matches Results §3.3's "$P = 0.56$" and JSON's 0.5551).
- Discussion §"What this means" line 142: "24 evidence-free decision nodes" → "19 evidence-free decision nodes" (matching Results §3.4 and JSON).
- Limitations line 151: "261-trial" → "259-trial".

**R2-A3. Rewrite the cover letter** (`cover_letter_jcopo_draft.md`) with the canonical post-R1 numbers:
- Paragraph 2: "n = 50" → "n = 49"; "261-trial" → "259-trial"; "P = 0.0004" → "P = 0.023"; "EFDPR 0.48" → "EFDPR 0.39"; "CI 0.34--0.63" → "CI 0.25--0.54"; remove or soften the "71% evidence-free, P = 0.0001" sub-claim (the post-R1 EGFR-only is 0.41, P = 0.11 — does not individually reject; rewrite as "the largest evidence-free clusters are at NSCLC EGFR-mutant post-osimertinib and mBC post-CDK4/6i salvage positions, where individual sub-analyses do not reject but contribute most heavily to the pooled rejection.").
- Then close the R1 A5 / A6 asks: fill [Date], verify EiC name (Stacy W. Gray vs. current JCO PO masthead), fill [ORCID], [GitHub URL], [Zenodo DOI], [medRxiv DOI]; identify and list 3 suggested reviewers with name + affiliation + institutional email + ORCID; delete the "Editor pre-screen tips (delete this section before submission)" meta-section lines 45-50.

**R2-A4. Add the honest 0.71 → 0.41 (and 0.48 → 0.39) R1-correction disclosure paragraph** to Paper A Discussion §"Three caveats" (line 145), per §A.8 above. Without this paragraph, the manuscript reads as if the post-R1 numbers were always the numbers, when in fact the cover letter and the figures still tell the pre-R1 story. The disclosure converts the discrepancy from "carelessness" into "transparency credit."

**R2-A5. Build `supplement_v3.tex` and compile to `supplement_v3.pdf`** OR delete the Methods §2.5 sentence referencing Supplementary Table S1. R1 ask A4 deadline (Day 10 of the polish plan) has slipped; the Methods section currently references a nonexistent artefact. The 30-second fix is deleting the sentence; the right answer is building the supplement.

**R2-A6. Replace the author block placeholder and add the Methods §2.1 prereg-trail sentence.** Two unrelated fixes bundled because each is ~2 lines:
- Line 36 affiliation → real or "Independent Researcher" + real (or removed) ORCID + postal address.
- Methods §2.1 line 78 → append the v1 → v2 → v3 prereg-versioning sentence (see §A.7 above).

### Paper B — Research Synthesis Methods

**R2-B1. Fix Paper B §5.3 "Tolerance-sensitivity grid" stale numbers** (line 130): "0.34 (24/50 → 17/50; P = 0.10)" — three numbers (denominator, point estimate, P) are stale relative to the abstract and §5.2. Either delete §5.3 (redundant) or rewrite to match: "0.35 (17/49; P = 0.084), failing to reject."

**R2-B2. Add the one-sentence "no human-extraction comparator" disclosure** to §5.4 Limitations (R1 ask B2 unchanged; the only RSM 2025 AI/ML guidance gap).

**R2-B3. Regenerate the medRxiv metadata sheet abstract** from the current tex body (`paper_B_methods_v3.tex` lines 48). Update `medrxiv_metadata.md` line 19 with the post-R1 numbers; correct the "(current = 245 words)" annotation to the actual current count (~161 words). Same fix on `cover_letter_medrxiv.md` line 14 ("P = 0.0004 on a pooled 50-node decision tree" → "P = 0.023 on a pooled 49-node decision tree"). Same fix on the medRxiv AUDIT_REPORT.md word-count claim.

**R2-B4. Replace or drop the placeholder ORCID** (R1 ask B1 unchanged). For **medRxiv deposit** this can wait until portal time. For **RSM submission** this must land first.

### Cross-paper

**R2-C1. After R2-A1/A2/A3 and R2-B1/B3 land, re-run a numerical-consistency audit across the seven surfaces** (Paper A abstract, Paper A figures, Paper A captions, Paper A Discussion, Paper B abstract, medRxiv metadata, JCO PO cover letter). Recommend a single one-page "canonical-numbers cheat sheet" be added to `release/` and that all seven surfaces be derived from it (this is a lightweight defence against the R1-integration regression repeating itself in v4).

---

## VERDICT — Paper A → JCO Precision Oncology

**MAJOR REVISION** (packaging, with NEW critical numerical-inconsistency class on top of the R1 packaging defects).

The science remains solid (pre-registered rejection on the pooled 49-node denominator at P = 0.023; the four sensitivity subsets cleanly decompose to the cross-tumor signal; ALK-rearranged still serves as the negative-control demonstrating the framework distinguishes consolidated from fragmented evidence landscapes; tolerance-grid sensitivity is honestly reported). R1 ask A1 (NSCLC trial citations) landed cleanly and the desk-screen blocker from R1 is gone.

But R1 introduced a **new** desk-screen blocker that is arguably worse: the bug fixes propagated to the abstract and most of the body but did **not** propagate to:
- Two of three figures (Fig 1 title and Fig 3 entire data series), plus all three figure captions in the tex.
- Four spots in Paper A body (Introduction, Methods §2.5, Discussion §"Headline", Discussion §"NSCLC ALK", Discussion §"What this means", Limitations).
- The cover letter (still all pre-R1 numbers, plus all seven R1-flagged placeholders untouched).
- The medRxiv metadata sheet (Paper B's portal-paste material; cross-paper concern).

R1 asks A2 (author block), A4 (supplement), A5 (cover letter), A6 (suggested reviewers), and A8 (prereg trail) are **not closed**. The honest 0.71 → 0.41 / 0.48 → 0.39 R1-correction trajectory is **not disclosed** in the Discussion.

None of R2-A1 through R2-A6 requires re-running the analysis pipeline. All six are inside the original 14-day polish plan's scope. With the asks landed and one consistency-audit pass run across the seven surfaces, the desk-screen verdict moves to **MINOR** and the realistic acceptance probability stays at the AUDIT_REPORT's 45-55% estimate.

**Submission-ready by:** Day 14 of the polish plan **conditional** on R2-A1 (figure regeneration) and R2-A2 (stale-number sed pass) landing in the next 48 hours, plus R2-A3 (cover letter) and R2-A5 (supplement) landing on their existing polish-plan days.

---

## VERDICT — Paper B → Research Synthesis Methods

**MINOR REVISION** for medRxiv preprint deposit; **MAJOR REVISION** for the RSM submission.

For the **medRxiv preprint deposit today**:
- The placeholder ORCID (R1 B1) is **deferrable to portal time**.
- The §5.3 stale numbers (R2-B1) and the missing human-extraction-comparator disclosure (R2-B2) are visible-in-PDF and should be fixed before deposit.
- The medRxiv metadata sheet abstract and cover letter (R2-B3) are the **portal-paste material** and are **stale on all key numbers**. Fixing these is the only true blocker for medRxiv deposit (because medRxiv staff cross-check the metadata against the manuscript).

For the **RSM submission**:
- All R2-B1 through R2-B4 must land.
- The placeholder ORCID must land (RSM portal will fail validation).
- The §5.3 redundant/stale subsection must be rewritten or removed.
- The human-extraction-comparator disclosure must land.

**Preprint deposit-ready by:** End of today, conditional on R2-B1 (§5.3 fix) and R2-B3 (metadata regeneration) landing in the next 2 hours. R2-B2 (human-comparator disclosure) is RSM-2025-gap closing and can wait one revision cycle.

**RSM submission-ready by:** Day 5 (after preprint DOI is assigned and B1/B2/B3/B4 all land; cover letter for RSM not yet drafted but is a 1-hour task).

---

*End of dual editor decision letter, v3 round 2.*

**VERDICTS:**
- **Paper A → JCO PO: MAJOR REVISION** (numerical inconsistency across figures/cover letter/Discussion; 6 R2 asks; recoverable inside the 14-day polish plan with the figures and cover letter regenerated in the next 48 hours)
- **Paper B → RSM: MINOR REVISION** for medRxiv deposit (2-hour fix); **MAJOR REVISION** for RSM submission (4 R2 asks)
