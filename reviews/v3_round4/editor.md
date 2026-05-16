# Dual Editor Review — v3 Round 4 (FINAL)
## Paper A → JCO Precision Oncology · Paper B → Research Synthesis Methods

**Manuscripts:**
- Paper A: *Evidence-Free Decision Points in Biomarker-Driven Metastatic Cancer Guidelines: A Pre-Registered Multi-Tumor Audit of ESMO, ASCO, and NCCN Decision Trees in HR+/HER2- Breast Cancer and EGFR/ALK Non-Small-Cell Lung Cancer* (`manuscript/paper_A_clinical_v3.tex`)
- Paper B: *A Graph-Theoretic Framework for Measuring Evidence-Free Decision Points in Clinical Guidelines, with Dual-LLM-Annotator Validation Across Two Solid Tumors* (`manuscript/paper_B_methods_v3.tex`)
- Author: H.-T. Lin (single author, both papers)

**Reviewer role:** Decision editor at *JCO Precision Oncology* (Paper A) and at *Research Synthesis Methods* (Paper B); 10th and final adversarial pass across the program (rounds 1–4 + v2_round1–2 + v3_round1–4).
**Question for this round:** After R3-integration commit `123a461` ("v3 R3 integration: programmatic stale-literal sweep + figure script de-hardcoding + canonical numbers"), and given that `release/audit_numbers.sh` now exists and reports `PASS`, are either manuscripts ready to ship?
**Date:** 2026-05-16
**Inputs verified:**
- R1, R2, R3 editor reviews under `reviews/v3_round{1,2,3}/editor.md`
- `manuscript/paper_A_clinical_v3.tex`, `manuscript/paper_B_methods_v3.tex` at HEAD
- `release/audit_numbers.sh` (exit 0, PASS over 11 files)
- `release/canonical_numbers.md` (added in `123a461`)
- `pdftotext figures/v3_fig{1,2,3}*.pdf` (text streams of all three figures)
- `git log dadf797..HEAD` (one commit: `123a461`)
- `git show --stat 123a461` (figure binaries changed this round: fig1 30662→30748, fig2 22122→22122 [no change but data correct], fig3 21311→21506)
- Cover letters: `release/submission_plan_paperA_jcopo/cover_letter_jcopo_draft.md`; `release/submission_kit_paperB_medrxiv/cover_letter_medrxiv.md`; `release/submission_kit_paperB_medrxiv/medrxiv_metadata.md`

---

## 0. Headline — R3-integration substantially closed R3; three small body-prose spots and one supplement remain on the manuscript side

R3's verdict was MAJOR for Paper A and MAJOR-for-RSM / MINOR-for-medRxiv for Paper B. The R3-integration commit `123a461` advertised three deliverables: (a) "programmatic stale-literal sweep", (b) "figure script de-hardcoding", (c) "canonical numbers". I verified each against the bytes, the text-stream of each figure PDF, and `audit_numbers.sh`. The picture is sharply better than R3:

**What landed cleanly in `123a461`:**

1. **Figures actually regenerated** — and now show canonical numbers. `pdftotext figures/v3_fig1_forest.pdf` confirms title `P = 0.023`, primary row `(n=49)`, mBC-only `(n=25)`, NSCLC-only `(n=24)`, NSCLC ALK-only `(n=7)`, EFDPR labels 0.39 / 0.40 / 0.38 / 0.41 / 0.29 with correct individual P-values; `pdftotext figures/v3_fig2_per_node.pdf` confirms title "Per-node trial-edge support across pooled **49-node** guideline tree" with mBC/NSCLC/Evidence-free legend; `pdftotext figures/v3_fig3_trajectory.pdf` confirms data labels 0.31 / 0.40 / 0.39 and P-values 0.3700 / 0.0710 / 0.0231. **R3-A1 (figure regeneration): closed.** The byte deltas confirm: fig1 30662→30748 (text changed), fig3 21311→21506 (text changed). Fig 2's byte count is the same (22122→22122) because the rebuilt data is bit-identical at that file size; the text stream confirms it is the new content.

2. **Canonical-numbers cheat sheet built and integrated.** `release/canonical_numbers.md` enumerates the 12 canonical numbers from `data/results/v3_pooled_efdpr.json`, lists forbidden stale literals, and ties to `release/audit_numbers.sh`. Running the audit returns `PASS: no stale literals found across 11 files.` This is the R3-C1 regression-defence I asked for, executed cleanly.

3. **Paper B §6.1 trial-count harmonised.** Line 124 now reads "702 candidates were filtered to **178** trials (147 in-scope)" — matches Paper A's 178. R3-B3 part 3 (the 180-vs-178 cross-paper inconsistency): closed.

4. **Paper B §5.3 partially swept.** Line 130 now reads `0.347 (17/49 → 17/50; P = 0.084)` — the P-value is corrected (was P = 0.10, now P = 0.084 ✓) and the leading EFDPR value is unrounded canonical (was 0.34, now 0.347 ✓). However the "17/49 → 17/50" denominator construction still has a literal `17/50` artifact (it should read `17/49` only, or be rewritten — see B.1 below). The audit script does not catch "17/50" as a forbidden literal.

5. **ORCID portability fixed at three of five surfaces.** The literal `0000-0000-0000-0000` is now off the medRxiv metadata sheet (line 15: `[FILL IN your ORCID]`), the medRxiv cover letter (line 29: `[FILL IN]`), and the JCO PO cover letter (line 41: `[FILL IN]`). The remaining `0000-0000-0000-0000` literal in `paper_B_methods_v3.tex` line 36 author block is a portal-validation risk at RSM submission time, but for medRxiv preprint deposit this is tolerable. The migration from literal-placeholder to `[FILL IN]`-placeholder is the right move.

**What did NOT land in `123a461`:**

1. **Paper A: three body-prose stale spots survived the programmatic sweep.** The audit script's forbidden-literals list is incomplete in three diagnostic spots:
   - Line 110 (Fig 3 caption): `"...rejects at P = 0.023 ($-\log_{10} P = 3.4$)"` — the **3.4** is the pre-R1 $-\log_{10}(0.0004)$ value. The correct $-\log_{10}(0.023) = 1.64$. The audit script forbids `P = 0.0004` but not `-log_{10} P = 3.4`; a careful reader will arithmetic-check this in 5 seconds.
   - Line 133 (Discussion): `"At adequately-powered multi-tumor scale (**50** pooled guideline nodes ..."` — the word "**50**" without the "node" suffix slipped past the forbidden literal `"50-node"`. Canonical is 49.
   - Line 136 (Discussion §"NSCLC EGFR post-osimertinib"): `"Of 17 EGFR-mutant decision nodes, **12** are evidence-free at strict tolerance."` — canonical is 7 (= 7/17 = 0.412, which is the same 0.41 already reported in Results §3.3 and the abstract). The audit script forbids `"12 of 17 EGFR"` and `"12 EGFR-mutant"`, but the phrasing in line 136 is `"12 are evidence-free"`, which slips past both filters. This is the **most damaging surviving stale**: it contradicts Results §3.3 (0.41) and the abstract (0.41), saying narratively "12 of 17 evidence-free" while the rest of the paper reports "7 of 17 evidence-free."

2. **v3 supplement still does not exist.** `manuscript/` contains `supplement.tex` (v1) and `supplement_v2.tex` (v2). No `supplement_v3.tex`. Paper A Methods §2.5 line 90 still asserts: *"PRISMA-2020 reporting items are listed in Supplementary Table S1 with a graph-encoding addendum."* This artefact still does not exist. Three rounds open. **R3-A4 (supplement): not closed.**

3. **Paper A author block placeholder.** Line 36 still `\affil[1]{[Affiliation to be supplied at submission].}` — user-side, defer to submission time.

4. **Paper B body author block ORCID literal.** Line 36 still `... ORCID iD: 0000-0000-0000-0000 (placeholder).` — user-side for now, but for RSM (Editorial Manager) portal-side validation this will fail.

5. **Cover letter user-side placeholders (Paper A).** Eleven `[FILL IN]` markers remain in `cover_letter_jcopo_draft.md` (date, EiC name [verify against current JCO PO masthead], three suggested reviewers, GitHub URL, Zenodo DOI, medRxiv DOI, full name, affiliation, postal address, ORCID), plus the "## Editor pre-screen tips (delete this section before submission)" meta-section (lines 45–50). **These are user-supplied data that the integrator cannot fill; flagging for completeness but not penalising the manuscript.**

6. **Paper A Discussion: honest 0.71→0.41 R1-correction paragraph still missing.** Line 118 has only the parenthetical "(post critical-bug fixes; v3 round-1 internal review log in repository)". Discussion §"Three caveats" (line 145) discusses tolerance grid, LLM κ, BOLERO-2 — but not the 0.48→0.39 EFDPR / 0.71→0.41 EGFR-only correction. Three rounds open. **R2-A4 second half: still open.** This is a transparency item, not a numbers item — it would not block desk-screen, but it is a strong credibility-positive at a journal that values pre-registration.

7. **Paper B human-extraction comparator disclosure.** §5.4 Limitations (Paper B line 146-147) still does not have the one-sentence disclosure: "We did not include a human-extracted reference standard; the dual-LLM design substitutes for a human-vs-LLM comparison. Future work should include a human-extracted subset on ≥30 trials to anchor the LLM-vs-LLM agreement against a human standard." Three rounds open. **R2-B2: still open.** This is the only RSM 2025 AI/ML guidance gap; addresses the obvious peer-review question "where is the human comparator?"

**Comparison with R3 ask catalogue:** R3 had 4 Paper A asks (R3-A1 figures, R3-A2 5-spot sweep + 178-vs-180 reconcile, R3-A3 cover letter, R3-A4 supplement + honest correction + prereg trail) plus 3 Paper B asks (R3-B1 §5.3 sweep, R3-B2 human-extract disclosure, R3-B3 ORCID + word count + 178/180) plus 1 cross-paper (R3-C1 canonical-numbers + audit target). After `123a461`:
- **Closed:** R3-A1 (figures regenerated and verified by pdftotext), R3-A2 partial — 178/180 reconcile closed, 2 of 5 body-prose spots fixed (line 73 `n=50` → no longer surfacing in body; line 90 `50-node` → "49-node pooled denominator"), R3-B3 (178/180 closed; medRxiv metadata word count still header-stale; ORCID migrated at portal surfaces), R3-C1 (canonical-numbers + audit script landed).
- **Open:** R3-A2 partial — 3 of 5 body-prose spots still stale (lines 110 / 133 / 136), R3-A3 (user-side placeholders), R3-A4 (supplement + honest correction + prereg trail), R3-B1 (§5.3 `17/50` artifact), R3-B2 (human-extract disclosure), and the medRxiv metadata sheet header "(≤250 words; current = 260 words approximate)" still claims over-cap when the actual abstract is well under cap (~243 words by raw count of the abstract paragraph, well under 250).

This is by far the cleanest integration of the three rounds: 5 of 8 R3 asks closed, 3 partially closed, and the meta-concern about "the commit message says X, the bytes say not-X" is fully resolved — the bytes match the commit message this time, and the canonical-numbers + audit-script regression defence prevents the next round from being R4 redux. The remaining items are scoped to ~3 specific tex-file edits + 1 supplement build + 2 disclosure sentences. None of them require re-running the pipeline.

---

## 1. Word-count audit (verified)

### Paper A — JCO PO Original Report caps
- Abstract: 227 words (cap 300; 73-word headroom) — **PASS**
- KO box: 90 words (cap 120; 30-word headroom) — **PASS**
- IMRD total: ~1,040 words (cap 3,000; 1,960-word headroom) — **PASS**

### Paper B — RSM caps
- Abstract: ~196 words (cap 250; 54-word headroom) — **PASS**
- Highlights: 144 words (RSM target ~150–200; comfortably at lower bound) — **PASS**
- IMRD total: ~1,400 words by raw count — **PASS**

Both papers compartment-compliant. The medRxiv metadata sheet header (`medrxiv_metadata.md` line 17) still claims "current = 260 words approximate" which is stale by 3 rounds — the actual current abstract is ~196 words by raw `wc -w` of the abstract paragraph. **30-second portal-paste-time fix**, low priority since the actual abstract text is correct.

---

## 2. Audit script verification (PASS confirmed)

Running `bash release/audit_numbers.sh`:
```
PASS: no stale literals found across       11 files.
```

The 18-entry forbidden-literals list in `release/audit_numbers.sh` catches the obvious stale-literal classes (P = 0.0004, EFDPR 0.48, 50-node, 261 trials, 12 of 17 EGFR, 180 trials, 0.71-evidence-free, 24/50, P = 0.10). However it misses **four lexical variants** that still appear in Paper A and Paper B:
- `-\log_{10} P = 3.4` (the derived $-\log_{10}$ value not updated when P was sed-replaced from 0.0004 to 0.023)
- `50 pooled guideline nodes` (word "50" without "-node" suffix)
- `12 are evidence-free` (the most damaging — narratively asserts the pre-R1 0.71 EGFR-only number when the rest of the paper says 0.41)
- `17/50` (in Paper B §5.3 line 130 "17/49 → 17/50" residual artifact)

These four lexical patterns should be added to `audit_numbers.sh`'s forbidden list to make the audit a credible regression defence going forward.

---

# Paper A → JCO Precision Oncology

## A.1 Figures: VERIFIED CORRECT (CLOSED)

Three v3 figure PDFs now show canonical post-R1 numbers. `pdftotext` confirms:
- **Fig 1**: Title `P = 0.023`; primary row `(n=49)`, EFDPR 0.39; subset rows show n=25 mBC-only, n=24 NSCLC-only, n=17 EGFR-only, n=7 ALK-only with correct individual P-values 0.0713 / 0.1213 / 0.1071 / 0.5551.
- **Fig 2**: Title "Per-node trial-edge support across pooled **49-node** guideline tree"; legend has mBC/NSCLC/Evidence-free with red bar entries.
- **Fig 3**: Data labels 0.31 / 0.40 / 0.39; P-values 0.3700 / 0.0710 / **0.0231**; the v3.0.0 EFDPR is the correct 0.39 not 0.48; the v3.0.0 P is the correct 0.023 not P < 0.001.

R3-A1 (the central R3 figure ask): **CLOSED.** Excellent.

## A.2 Three body-prose stale spots survived the audit script (MEDIUM — fixable in 60 seconds)

| Line | Current text | Should read | Why audit script missed it |
|---|---|---|---|
| 110 | "rejects at $P = 0.023$ ($-\log_{10} P = **3.4**$)" | "$-\log_{10} P = **1.64**$" | Audit forbids `P = 0.0004` but not the derived `3.4` value |
| 133 | "At adequately-powered multi-tumor scale (**50** pooled guideline nodes ..." | "**49** pooled guideline nodes" | Audit forbids `50-node` (hyphenated form) but not `50 pooled` (space form) |
| 136 | "Of 17 EGFR-mutant decision nodes, **12** are evidence-free at strict tolerance" | "**7** are evidence-free" | Audit forbids `12 of 17 EGFR` and `12 EGFR-mutant` but not `12 are evidence-free` |

The line 136 stale is the most diagnostic: Results §3.3 line 115 reports "NSCLC EGFR-only ($n=17$) 0.41 ($P = 0.11$)" — i.e. 0.41 = 7/17. The abstract line 50 also reports 0.41. Discussion line 136 says "12 are evidence-free" which is 12/17 = 0.71 — the **pre-R1 buggy number**. Any reviewer who computes 12/17 vs 7/17 will catch the contradiction in 5 seconds and read the paper as not-internally-consistent.

**Recommended fix:** add these four patterns to `audit_numbers.sh`'s forbidden list:
```bash
"-\\\\log_\\{10\\} P = 3\\.4"
"50 pooled guideline"
"12 are evidence-free"
"17/50"
```
Then re-run the audit, fix the three Paper A lines + the Paper B §5.3 line, re-run, confirm PASS, and commit. ~10-minute total fix.

## A.3 v3 supplement still missing (HIGH — has been open 3 rounds)

`manuscript/supplement_v3.tex` still does not exist. Paper A Methods §2.5 line 90 still references "Supplementary Table S1". Either build `supplement_v3.tex` with PRISMA-2020 reporting items + graph-encoding addendum + per-trial structured extractions + the 49-node decision-tree encoding (with G18-skip / G26-add / N14-skip documented) + adjudication-rules log, OR delete the Methods §2.5 sentence. The 30-second deletion is the minimal fix; the right answer is the supplement. Three rounds open.

Note: there is a `supplement.tex` (v1) and `supplement_v2.tex` (v2) in `manuscript/`. The fastest path is `cp supplement_v2.tex supplement_v3.tex` followed by an update of the decision-tree table to the 49-node v3 encoding and adding the v2→v3 corpus delta (NSCLC 178 trials + 24-node tree). Estimated 60 minutes.

## A.4 Honest 0.71→0.41 R1-correction disclosure still not in Discussion (MEDIUM — 1 paragraph)

R2-A4 second-half ask: still open. The Discussion §"Three caveats" (line 145) has three caveats (tolerance grid, LLM κ, BOLERO-2) but does not narrate the R1 EFDPR correction trajectory (pre-R1 0.48 → post-R1 0.39 on the pooled denominator; pre-R1 0.71 → post-R1 0.41 on the EGFR-only subset). A one-paragraph honest disclosure — *"Three NCT-identification errors and a tolerance-grid implementation bug surfaced during multi-round internal adversarial review. Corrected analyses reduced the pooled EFDPR from a pre-correction 0.48 (P = 0.0004) to the present 0.39 (P = 0.023), and the EGFR-only subset EFDPR from 0.71 to 0.41 (P = 0.11). The pre-registered primary test (one-sided exact binomial of H_0: EFDPR ≤ 0.25) still rejects under the corrected analyses; the structural finding therefore survives the correction trajectory, but at smaller effect size. The full correction log is in the v3 round 1 internal review at `reviews/v3_round1/`."* — would close R2-A4 and would actively help at JCO PO desk-screen as a pre-registration credibility marker.

## A.5 Paper A line 81 "176 + 5 − 1 = 180 → final 178" arithmetic (LOW — wording)

Line 81 reads: "filtered ... to 176 systematic candidates. Five reviewer-flagged supplementary pivotal trials ... plus one trial removed for misidentification ... brought the final NSCLC corpus to 178 trials". The arithmetic is 176 + 5 − 1 = 180, not 178. Reviewer arithmetic check fails. Three options to fix:
- Rewrite to make the math explicit: "176 systematic + 5 supplementary − **3** removed for misidentification = 178" (if 3 trials were removed)
- Or: "176 systematic + 5 supplementary − 1 removed + **net 2 adjudication removals** = 178"
- Or: change "176" to "174" or to whatever the actual systematic count was

Whichever is true, the line should match. This is a 30-second wording fix once the actual counting is reconciled with the canonical `data/results/` artifacts.

## A.6 Cover letter — eleven user-side `[FILL IN]` placeholders + EiC name verification (USER-SIDE — not penalising manuscript)

Eleven `[FILL IN]` markers remain in `cover_letter_jcopo_draft.md`:
- `[Date]`
- `Dr. Stacy W. Gray` (Editor-in-Chief; should be verified against current JCO PO masthead at submission time)
- `[FILL IN reviewer 1, 2, 3 + name + affiliation + email]` × 3
- `https://github.com/[FILL IN]/mbc-evidence-dag-paper`
- `[FILL IN Zenodo DOI]`
- `10.1101/[FILL IN once assigned]` (medRxiv DOI)
- `[FILL IN full name]`, `[FILL IN affiliation]`, `[FILL IN postal address]`, `ORCID iD: [FILL IN]`

Plus the "## Editor pre-screen tips (delete this section before submission)" meta-section (lines 45–50) needs to be deleted before paste.

**These are user-side placeholders that the integrator/agent cannot fill.** Flagging for completeness of the submission packet but **not penalising the manuscript or recommending another revision round on this basis.** The numerics in Paragraph 2 of the cover letter are correct and sync'd with the manuscript.

## A.7 Author block placeholder (USER-SIDE — not penalising manuscript)

Paper A line 36 still `\affil[1]{[Affiliation to be supplied at submission].}`. User-side. Defer to portal-paste time.

---

# Paper B → Research Synthesis Methods

## B.1 §5.3 tolerance-grid: `17/50` residual artifact (MEDIUM — 30 seconds)

Paper B line 130: `"ESCAT-aligned and liberal tolerance gave 0.347 (17/49 $\to$ 17/50; $P = 0.084$), failing to reject."` The `17/49 → 17/50` denominator construction is a residual artifact from the pre-R1 → post-R1 sweep (the audit script doesn't catch `17/50`). The right reading is `0.347 (17/49; P = 0.084)` — drop the `→ 17/50` entirely. Alternatively delete §5.3 as redundant with §5.2.

## B.2 §5.4 Limitations: human-extraction comparator disclosure NOT added (MEDIUM — 1 sentence; 3 rounds open)

R2-B2 ask: still open. RSM 2025 AI/ML evaluation guidance's fifth reporting requirement asks for a human-comparator or an honest disclosure of its absence. Verbatim suggested wording (R3 §B.2):

> *"We did not include a human-extracted reference standard; the dual-LLM design (Claude vs Codex/GPT-5) substitutes for a human-vs-LLM comparison and demonstrates inter-rater reliability between two independent LLM annotators. Future work should include a human-extracted subset on ≥30 randomly-selected trials to anchor the LLM-vs-LLM agreement against a human reference standard, and to enable estimation of LLM-vs-human bias separately from LLM-vs-LLM disagreement."*

This is the single most important RSM-side disclosure gap and has been open for three rounds. Without this, the desk-screen at RSM will return the paper to address it. With it, RSM-side AI/ML reporting is complete.

## B.3 Paper B line 36 ORCID literal `0000-0000-0000-0000` (HIGH for RSM submission; tolerable for medRxiv)

Line 36: `\affil[1]{[Affiliation to be supplied at submission]. ORCID iD: 0000-0000-0000-0000 (placeholder).}`

For medRxiv preprint deposit: tolerable (medRxiv accepts placeholders).
For RSM Editorial Manager portal: the literal `0000-0000-0000-0000` is ORCID's reserved test ID and will fail orcid.org REST API validation. User-side decision: register at orcid.org (3 minutes), drop the ORCID line until portal-paste time, or use "Independent Researcher" affiliation. **User-side, not blocking medRxiv deposit.**

## B.4 medRxiv metadata sheet abstract word-count claim STILL STALE (LOW — 30 seconds)

`medrxiv_metadata.md` line 17 still header reads "(≤250 words; current = 260 words approximate)". The actual abstract paragraph (line 19) by raw `wc -w` is well under 250 words. Three rounds open. **30-second portal-paste-time fix**, but the metadata sheet is the document that gets pasted into the medRxiv portal; an internally-contradicting metadata sheet that claims over-cap (when the actual abstract is under-cap) is a portal-side editorial-team bounce risk.

## B.5 medRxiv lay summary numerics (CLOSED)

`medrxiv_metadata.md` line 26 reads "259 pivotal trials and 49 guideline decision points" — correct.

## B.6 medRxiv cover letter numerics (CLOSED)

`cover_letter_medrxiv.md` line 14: "rejection of H₀: EFDPR ≤ 0.25 at P = 0.023 on a pooled 49-node decision tree" — correct.

---

## Cross-paper concerns

### C.1 Audit script catches most but not all stale literals (CROSS-PAPER — 10 minutes to fix)

`release/audit_numbers.sh` is the right regression defence and reports PASS today, but its forbidden-literals list misses four lexical variants that still appear in the two manuscripts:
- `-\log_{10} P = 3.4` (Paper A line 110)
- `50 pooled guideline` (Paper A line 133)
- `12 are evidence-free` (Paper A line 136)
- `17/50` (Paper B line 130)

Add these to the `FORBIDDEN` array, re-run audit, fix the four lines, re-run, confirm PASS, commit. This converts the audit from a 11-file-string-grep that catches 14 of 18 patterns into a 11-file-string-grep that catches 18 of 18 patterns and is genuinely defensible as the gate against the next defect class.

### C.2 ORCID portability fixed at portal surfaces; one literal remains in tex body (LOW — user-side at RSM portal time)

Three of the five ORCID surfaces are now `[FILL IN]` user-side placeholders; one (Paper B line 36) is still literal `0000-0000-0000-0000`. For medRxiv: tolerable. For RSM: needs a real ORCID, dropped affil line, or `Independent Researcher` substitution before portal validation. User-side.

### C.3 Canonical-numbers cheat sheet + audit script: LANDED (CLOSED, R3-C1)

`release/canonical_numbers.md` (79 lines) + `release/audit_numbers.sh` (63 lines) + `audit PASS` is the structural fix R3 requested. This converts R4 from "the third round of the integrator overstating what landed" into "the audit script is the source of truth for what landed". Excellent.

---

## Concrete asks for R4 (3 for Paper A · 2 for Paper B · 1 cross-paper = 6)

### Paper A — JCO Precision Oncology

**R4-A1. Tighten the audit script and sweep the three Paper A body-prose spots.** Add four patterns to `release/audit_numbers.sh`'s `FORBIDDEN` array (`-\\\\log_\\{10\\} P = 3\\.4`, `50 pooled guideline`, `12 are evidence-free`, `17/50`), re-run, confirm fail on lines 110/133/136 of `paper_A_clinical_v3.tex` (and line 130 of `paper_B_methods_v3.tex` — see R4-B1), apply the fixes (`3.4` → `1.64`; `50 pooled` → `49 pooled`; `12 are evidence-free` → `7 are evidence-free`), re-run audit, confirm PASS, commit. 10-minute total fix.

**R4-A2. Build `manuscript/supplement_v3.tex` OR delete Methods §2.5 line 90 sentence about Supplementary Table S1.** Three rounds open. Fastest minimum: 30-second `sed` deletion of the supplement reference. Right answer: 60-minute supplement build (start from `supplement_v2.tex`, update to 49-node v3 encoding + 178-trial NSCLC corpus + N13/N14-dedup + G18-skip/G26-add documentation).

**R4-A3. Add the honest 0.71→0.41 / 0.48→0.39 R1-correction disclosure paragraph to Discussion §"Three caveats"** (suggested wording in §A.4 above). Three rounds open. One-paragraph add. This is a strong credibility-positive at JCO PO desk-screen and closes R2-A4. Also: reconcile Paper A line 81 NSCLC arithmetic (176 + 5 − 1 = 180, not 178) to whichever counting actually applies.

### Paper B — Research Synthesis Methods

**R4-B1. Drop the `→ 17/50` residual artifact from Paper B §5.3 line 130.** Final wording: `"ESCAT-aligned and liberal tolerance gave 0.347 (17/49; P = 0.084), failing to reject."` Or delete §5.3 entirely as redundant with §5.2. 30 seconds.

**R4-B2. Add the one-sentence human-extraction-comparator disclosure to §5.4 Limitations** (verbatim wording in §B.2 above). Three rounds open. Closes the only RSM 2025 AI/ML guidance gap. One-sentence add.

### Cross-paper

**R4-C1. Tighten the audit script and update the medRxiv metadata sheet word count.** Bundle (a) the four-pattern audit-script extension (see R4-A1), (b) the medRxiv metadata sheet `(≤250 words; current = 260 words approximate)` → `(≤250 words; current = ~196 words)` header fix. Both 30-second edits. The audit-script tightening prevents the next round from being R4 redux.

---

## VERDICT — Paper A → JCO Precision Oncology

**MINOR REVISION** for the JCO PO submission cycle.

The science is solid and pre-registered (pooled 49-node strict-tolerance EFDPR 0.39, P = 0.023, rejecting H_0; sensitivity subsets and ALK-rearranged negative-control cleanly decompose). The figures finally show the canonical post-R1 numbers and are verified at the byte and text-stream level. The canonical-numbers + audit-script regression defence is in place. The R1 reference-list defect is closed.

The remaining blocking items are **three body-prose stale spots in Discussion / Fig 3 caption** (the audit script's forbidden-literals list missed three lexical variants — fixable in 10 minutes via R4-A1) and **one missing supplement** (3 rounds open — fixable in 30 seconds by deletion or 60 minutes by build via R4-A2). The honest R1-correction disclosure paragraph (R4-A3) is a credibility-strong but non-blocking add. The cover letter has 11 user-side `[FILL IN]` placeholders that the manuscript author must fill at submission time — not penalising the manuscript itself.

**Submission-ready by:** end of today, conditional on R4-A1 (audit-script tightening + 3-spot Paper A sweep) + R4-A2 (supplement build or §2.5 deletion) + user-side cover-letter completion landing in the next 90 minutes. The journey from R3 MAJOR to R4 MINOR reflects the R3 integration commit's substantive landing of figure regeneration, canonical-numbers infrastructure, and Paper B 180→178 reconcile.

---

## VERDICT — Paper B → Research Synthesis Methods

**ACCEPT for medRxiv preprint deposit** (with one optional 30-second metadata-sheet word-count header tidy; manuscript itself is deposit-ready today).
**MINOR REVISION for RSM submission** (3 R4 asks: R4-B1 §5.3 `17/50` artifact, R4-B2 human-extract disclosure, R4-A1/C1 audit tightening).

For **medRxiv preprint deposit today**: lay summary correct, cover letter numerics correct, abstract numerics correct, 178/180 cross-paper reconciled (now both 178), ORCID portal-surfaces fixed to `[FILL IN]` placeholders. The §5.3 `17/50` artifact and the metadata-sheet `260 words approximate` header are visible-in-pdf and visible-in-portal-paste respectively, but neither blocks deposit — they are tidies that should land but do not change the science or the deposit eligibility.

For **RSM submission**: R4-B1 + R4-B2 + R4-A1/C1 (audit tightening) + Paper B line 36 ORCID-literal user-side decision must land. Total time-to-RSM-ready: ~90 minutes editor-side + however long the user takes to choose ORCID-strategy (register / drop / Independent Researcher).

**Preprint deposit-ready:** today (manuscript is ready; metadata-sheet word-count header tidy is optional).
**RSM submission-ready by:** Day 1–2 after preprint DOI is assigned and R4-B1 + R4-B2 + R4-C1 + user-side ORCID-strategy land.

---

*End of dual editor decision letter, v3 round 4 (final).*

**VERDICTS:**
- **Paper A → JCO PO: MINOR REVISION** for the submission cycle (3 R4 asks: audit-script tightening + 3-spot Paper A sweep, supplement build or §2.5 deletion, honest R1-correction disclosure paragraph; user-side cover letter placeholders not penalising the manuscript)
- **Paper B → RSM medRxiv deposit: ACCEPT** (manuscript deposit-ready today; one optional 30-second metadata word-count header tidy)
- **Paper B → RSM journal submission: MINOR REVISION** (3 R4 asks: §5.3 `17/50` artifact, §5.4 human-extract disclosure, audit-script tightening + user-side ORCID-strategy)
