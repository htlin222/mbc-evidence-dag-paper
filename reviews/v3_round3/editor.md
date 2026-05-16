# Dual Editor Review — v3 Round 3
## Paper A → JCO Precision Oncology · Paper B → Research Synthesis Methods

**Manuscripts:**
- Paper A: *Evidence-Free Decision Points in Biomarker-Driven Metastatic Cancer Guidelines: A Pre-Registered Multi-Tumor Audit of ESMO, ASCO, and NCCN Decision Trees in HR+/HER2- Breast Cancer and EGFR/ALK Non-Small-Cell Lung Cancer* (`manuscript/paper_A_clinical_v3.tex`)
- Paper B: *A Graph-Theoretic Framework for Measuring Evidence-Free Decision Points in Clinical Guidelines, with Dual-LLM-Annotator Validation Across Two Solid Tumors* (`manuscript/paper_B_methods_v3.tex`)
- Author: H.-T. Lin (single author, both papers)

**Reviewer role:** Decision editor at *JCO Precision Oncology* (Paper A) and at *Research Synthesis Methods* (Paper B); 9th adversarial pass across the program (rounds 1–4 + v2_round1–2 + v3_round1–3).
**Question for this round:** After R2-integration commit `dadf797` ("v3 R2 integration: sweep 14 stale numbers + regen figures + sync cover letters + sync medRxiv kit"), would either manuscript clear its target journal's editorial screen today?
**Date:** 2026-05-16
**Inputs read:** R1 + R2 editor reviews; current `paper_A_clinical_v3.tex` and `paper_B_methods_v3.tex`; `references.bib`; `data/results/v3_pooled_efdpr.json` as canonical ground truth; the three v3 figure PDFs opened at print size (text-stream extracted); `cover_letter_jcopo_draft.md`, `cover_letter_medrxiv.md`, `medrxiv_metadata.md`; `manuscript/` directory listing to verify supplement status; git log + `git show --stat dadf797`.

---

## 0. Headline — the third integration claim is the second one the figures did not believe

R2's verdict was MAJOR for Paper A and MAJOR-for-RSM / MINOR-for-medRxiv for Paper B. The R2-integration commit `dadf797` advertised three deliverables: (a) "sweep 14 stale numbers", (b) "regen figures", (c) "sync cover letters + sync medRxiv kit." The body-prose sweep landed cleanly for **most** of the R2 catalogue: Paper A abstract, KO box, Results §3.1/§3.2/§3.3/§3.4, Figure 1 caption, Figure 2 caption, Discussion §"Headline", Discussion §"NSCLC ALK is the comparator", Discussion §"What this means", Limitations, and Paper B abstract / §5.2 / §5.4 all now report the canonical post-R1 numbers (EFDPR 0.39 strict, 19/49, P = 0.023; mBC-only n=25 P = 0.07; NSCLC-only n=24 P = 0.12; EGFR-only n=17 P = 0.11; ALK-only n=7 P = 0.56; 259 trials). The cover letter (Paper A side) and the medRxiv cover letter (Paper B side) are now also numerically sync'd.

Three of the deliverables, however, **did not actually happen**:

1. **The figures were not regenerated.** `git show --stat dadf797` shows `figures/v3_fig1_forest.pdf | Bin 30662 -> 30662 bytes` and `figures/v3_fig2_per_node.pdf | Bin 21618 -> 21618 bytes` and `figures/v3_fig3_trajectory.pdf | Bin 21311 -> 21311 bytes` — **byte-for-byte identical**. The commit message says "regen figures + force-deleted-and-rebuilt"; the binary contents say otherwise. Opening the PDFs at print size confirms: Fig 1 title still reads "**P = 0.0004**" and the primary row label still reads "**(n=50)**"; the NSCLC-only row reads "(n=25)" and the ALK-only row reads "(n=8)"; Fig 2 title still reads "**50-node guideline tree**" and the "Evidence-free (strict)" red legend swatch still has **zero red bars** in the plot area; Fig 3 v3.0.0 EFDPR data label still reads "**0.48**" with P-value annotation "**P < 0.001**" — these are the pre-R1 buggy numbers. R2 ask R2-A1 (figure regeneration) **did not land**. This is the same defect class R2 caught and the integrator claimed to have closed.

2. **The Paper A body did not get a clean sweep.** Five stale spots remain in Paper A:
   - Line 73 (Introduction): "pools the two-tumor decision-tree denominator to $n = 50$" — stale (canonical 49).
   - Line 90 (Methods §2.5): "computed on the 50-node pooled denominator" — stale.
   - Line 110 (Fig 3 caption): "The pooled 50-node test rejects at $P = 0.023$ ($-\log_{10} P = 3.4$)" — `50-node` stale, AND the $-\log_{10}$ value is arithmetically wrong ($-\log_{10}(0.023) = 1.64$, not 3.4 — the "3.4" is the **pre-R1 $-\log_{10}(0.0004) = 3.4$** value, frozen in place).
   - Line 133 (Discussion §"Headline"): "**50 pooled guideline nodes**" — stale.
   - Line 136 (Discussion §"NSCLC EGFR post-osimertinib"): "**12 are evidence-free at strict tolerance**" — stale; canonical JSON says EGFR-only is 7/17 evidence-free (0.4118), not 12/17. This is the pre-R1 0.71 buggy number not corrected.

3. **The cover letter still has every placeholder R1 flagged plus the meta-section R1 flagged for deletion.** `[Date]`, `Dr. Stacy W. Gray` (still unverified as current JCO PO EiC), three `[FILL IN reviewer N...]` lines, four `[FILL IN]` placeholders for full name / affiliation / postal address / ORCID, the `https://github.com/[FILL IN]/...` URL, the `[FILL IN Zenodo DOI]`, and the `10.1101/[FILL IN once assigned]` medRxiv DOI. The "Editor pre-screen tips (delete this section before submission)" meta-section (lines 45–50) is still in place. The cover letter is **numerically sync'd** but **not submission-ready** by the simplest possible criterion — eleven `[FILL IN]` markers remain.

In addition, three R1/R2 asks remain entirely untouched: **v3 supplement** (still missing — `manuscript/` has `supplement.tex` v1 and `supplement_v2.tex` v2 only; Methods §2.5 line 90 still claims "Supplementary Table S1" exists); **placeholder author block** on Paper A (line 36 still `\affil[1]{[Affiliation to be supplied at submission].}`); **placeholder ORCID** on Paper B (line 36 still `0000-0000-0000-0000 (placeholder)`).

R2 had 6 Paper A asks and 4 Paper B asks plus 1 cross-paper. After dadf797 landed, my audit of those 11 items: **5 closed cleanly** (R2-A2 body-prose sweep partially landed; R2-A3 cover letter numerics sync; R2-A4 honest-correction disclosure partly landed; R2-B1 §5.3 numbers partly fixed; R2-B3 medRxiv abstract numbers landed). **6 not closed**: R2-A1 (figures), R2-A2 partial (5 spots remain), R2-A4 partial (no honest 0.71→0.41 paragraph), R2-A5 (supplement), R2-A6 (author block + prereg trail), R2-B2 (human-comparator disclosure), R2-B4 (placeholder ORCID), R2-C1 (canonical-numbers cheat sheet not added to `release/`). The same regression-pattern R2 caught is now in its **second** unaddressed copy.

This is not a science finding. It is a quality-control finding about the integration step itself: the integrator is shipping commit messages that overstate what the diff actually contains. R3's central ask is therefore to (i) actually regenerate the figures and verify by `sha256sum` that the file content changed, (ii) finish the five body-prose stale spots that the dadf797 sweep missed, (iii) close the cover letter, supplement, ORCID, and human-comparator asks that have now been on the table for two rounds.

None of R3-A1 through R3-A6 or R3-B1 through R3-B3 requires re-running the analysis. All are mechanical and recoverable inside the polish-plan 14-day window.

---

## 1. Word-count audit (verified)

I ran a tightened regex over both `.tex` files (drops `\citep`, `\section`, `\textbf{...}` keeps body content, `$X$` counts as 1).

### Paper A — JCO PO Original Report caps
```
Abstract:               227 words   (cap 300; 73-word headroom)
KO box:                  90 words   (cap 120; 30-word headroom)
Introduction:           258 words
Methods:                324 words
Results:                154 words
Discussion:             304 words
IMRD total:           1,040 words   (cap 3,000; 1,960-word headroom)
```
**Pass with massive headroom.** All compartments compliant.

### Paper B — RSM caps
```
Abstract:               101 words (in tex body, post-cleanup of \citep+section noise)
                        ~196 words by raw `wc -w` of the abstract paragraph
Highlights:             144 words (RSM target ~150-200; lower bound)
Introduction:           275 words
Framework:              ~51 words (math-heavy; sectional content not extractive-counted by my regex)
LLM pipeline:           127 words
Demonstration:          151 words
Discussion:             210 words
IMRD total:             ~814 words by regex (closer to ~1,400 by raw count)
```
**Pass.** Whichever way it's counted, Paper B abstract is well under the 250-word RSM cap. The `medrxiv_metadata.md` line 17 still says **"(≤250 words; current = 260 words approximate)"** — by raw `wc -w` the metadata-sheet abstract paragraph is 196 words; by the canonical RSM-portal counting rules (which collapse hyphenated tokens to single words and ignore in-text reference markers) it's closer to ~190. The metadata sheet's "260 words approximate" header is **stale by two integration rounds** (R1 said 245; R2 said 245; the actual count never exceeded ~196 after the post-R1 abstract rewrite). The number is now both wrong **and** misleading — it claims 260 against a 250 cap, suggesting the abstract is over-cap when in fact it is well under.

---

# Paper A → JCO Precision Oncology

## A.1 Figures: PDF bytes did not change (CRITICAL)

`git show --stat dadf797` reports `Bin 30662 -> 30662 bytes` for `v3_fig1_forest.pdf`, `Bin 21618 -> 21618 bytes` for `v3_fig2_per_node.pdf`, `Bin 21311 -> 21311 bytes` for `v3_fig3_trajectory.pdf`. These are no-op binary deltas. The commit message claims "regen figures + force-deleted-and-rebuilt"; the file system says the rebuilt PDFs are identical to the pre-R2 PDFs at byte level. The most likely explanation: `analysis/v3_09_figures.py` was rerun but the matplotlib output is deterministic to the byte under the same input data — so unless the data inputs changed (which they did at the JSON layer, but the figure script may be reading from a stale intermediate cache), the output is bit-identical to the previous render. Less likely: `make` short-circuited because the source file mtime did not update.

I confirmed the stale content by reading the PDFs directly. Fig 1 text stream contains:
- Title: "Pooled mBC + NSCLC EFDPR — pre-registered primary test rejects H₀ (**P = 0.0004**)"
- Primary row label: "Primary: pooled mBC + NSCLC (**n=50**)"
- NSCLC-only row label: "Sensitivity: NSCLC-only (**n=25**)"
- NSCLC ALK-only row label: "Sensitivity: NSCLC ALK-only (**n=8**)"
- Primary annotation: "P = 0.0231 *" (this row is correct — the annotation took the new P but the title and primary-row label still report n=50 and P = 0.0004 from the pre-R1 buggy render).

Fig 2 text stream contains:
- Title: "Per-node trial-edge support across pooled **50-node** guideline tree"
- Legend entries: mBC node (supported) [blue], NSCLC node (supported) [green], **Evidence-free (strict) [red — but no red bars exist in the plot area]**
- x-axis labels: G1...G26 (with G18 missing) AND N1...N25 (with N14 missing). Both the G18 skip and the G26 addition and the N14 skip are **undocumented in the caption**.

Fig 3 text stream contains:
- Title: "Pilot → production → multi-tumor: directional + significance trajectory" (this title is data-narrative not arithmetic, so isn't itself stale)
- Three EFDPR data labels: 0.31, 0.40, **0.48** — the last is pre-R1; canonical is 0.39.
- Three P-value labels: P = 0.3700, P = 0.0710, **P < 0.001** — last is pre-R1; canonical is P = 0.023.
- α = 0.05 reference line drawn on the **left** axis at y ≈ 0.20 (this is R1 ask A3 sub-bullet 3 — the α-level should be on the right axis at $-\log_{10}(0.05) = 1.30$, not on the left axis at 0.20).

The fix is: (i) rerun `python analysis/v3_09_figures.py` after `rm figures/v3_fig{1,2,3}*.pdf` (force regen, not cached), (ii) verify by `sha256sum figures/v3_fig{1,2,3}*.pdf` that the digests have changed, (iii) open the regenerated PDFs and confirm the text streams show **P = 0.023**, **n = 49**, **n = 24** (not 25), **n = 7** (not 8), **EFDPR 0.39** (not 0.48), **49-node** (not 50-node), and red bars for evidence-free nodes in Fig 2. **This is the R3 #1 ask.**

## A.2 Five body-prose stale spots that the dadf797 sweep missed (HIGH)

The R2-integration commit landed most of R2-A2's 8-item sed pass but missed these five:

| Line | Current text | Should read |
|---|---|---|
| 73 | "pools the two-tumor decision-tree denominator to $n = 50$" | "$n = 49$" |
| 90 | "computed on the **50-node** pooled denominator" | "**49-node**" |
| 110 | "The pooled **50-node** test rejects at $P = 0.023$ ($-\log_{10} P = **3.4**$)" | "**49-node** … ($-\log_{10} P = **1.64**$)" |
| 133 | "At adequately-powered multi-tumor scale (**50** pooled guideline nodes …)" | "**49** pooled guideline nodes" |
| 136 | "Of 17 EGFR-mutant decision nodes, **12** are evidence-free at strict tolerance" | "**7** are evidence-free" (canonical JSON: `nsclc_egfr_only.strict.evidence_free_count = 7`; 7/17 = 0.4118 matches Results §3.3's "0.41") |

The line-110 $-\log_{10} = 3.4$ error is the most diagnostic: it's the pre-R1 $-\log_{10}(0.0004) = 3.4$ value mechanically un-updated when the surrounding P-value sed-replaced from 0.0004 to 0.023. A diligent sed pass would have caught this; the dadf797 sweep used a non-contextual find-and-replace that updated the P-value but not the derived $-\log_{10}$ value (which a reviewer will compute mentally in 5 seconds: $-\log_{10}(0.023) \approx 1.64$, not 3.4).

Line 136's "12 EGFR-mutant evidence-free" is the most damaging substantively: it asserts a 0.71 EGFR-only sub-rate that has been corrected to 0.41 in Results §3.3 and the abstract. Discussion line 136 narratively contradicts Results §3.3 by ratio 12 vs 7.

## A.3 mBC corpus and NSCLC corpus counts — INTERNAL INCONSISTENCY remains (HIGH)

R2 §A.2 row "178 vs 180" flagged Paper A's internal disagreement on the NSCLC corpus count. **Status after dadf797**: not closed.
- Abstract line 49: "702 candidates filtered to **178** pivotal trials"
- Methods §2.2 line 81: "five reviewer-flagged supplementary pivotal trials … brought the final NSCLC corpus to **178** trials, of which 145 entered the in-scope trial-DAG"
- Paper B §5.1 (Demonstration §6.1) line 124: "702 candidates were filtered to **180** trials (145 in-scope)"

Paper A is now internally consistent at 178; Paper B is at 180. **Cross-paper, the same corpus is described with two different numbers.** A reviewer comparing the two manuscripts (which they will, given the explicit companion-paper cross-reference) sees 178 in one and 180 in the other. The pooled corpus total (259 = 81 + 178) is reported in both papers as 259, which implies 178 is canonical. Paper B's "180" is the stale value and needs to come down to 178.

## A.4 Cover letter — numerically sync'd, structurally incomplete (HIGH)

The cover letter `cover_letter_jcopo_draft.md` has had the post-R1 numbers swept into Paragraph 2 cleanly (n = 49, 259-trial, P = 0.023, EFDPR 0.39, CI 0.25-0.54, ESCAT 0.35 P = 0.084) — **R2 ask R2-A3 numerics: closed**. The 71% EGFR claim is removed; the substitute "evidence gap concentrated at NSCLC EGFR-mutant post-osimertinib decision nodes and at mBC post-CDK4/6i salvage positions" is honest and well-phrased.

However the eleven placeholders R1 flagged in October are still in place:
- Line 7: `[Date — e.g., 2026-05-30]`
- Line 9: `Dr. Stacy W. Gray` — still unverified as current JCO PO Editor-in-Chief; the JCO PO masthead as of 2026-05 should be checked against the journal website before submission (a stale EiC name reads as not-checking-current-masthead at the desk-screen).
- Lines 29-31: `[FILL IN reviewer 1, name + affiliation + email]` × 3 — R2 ask R2-A3 second clause was to populate these; not done.
- Line 24: `https://github.com/[FILL IN]/mbc-evidence-dag-paper`
- Line 24: `[FILL IN Zenodo DOI]`
- Line 22: `10.1101/[FILL IN once assigned]`
- Lines 37-41: `[FILL IN full name]`, `[FILL IN affiliation]`, `[FILL IN postal address]`, `ORCID iD: [FILL IN]`
- Lines 45-50: "**## Editor pre-screen tips (delete this section before submission)**" with three meta-strategy bullets to the cover-letter author. This section explicitly says delete-before-submission, and it has now survived three review cycles.

A JCO PO desk editor opening this cover letter sees eleven `[FILL IN]` markers, a `Dr.` salutation that may or may not be the current EiC, and a self-addressed strategy section. **Not submission-ready by the simplest criterion.** R2 ask R2-A3's second-half ("close the R1 A5/A6 asks") has not been touched.

## A.5 v3 supplement: STILL MISSING (HIGH)

`manuscript/` directory listing shows `supplement.tex` (v1), `supplement_v2.tex` (v2). No `supplement_v3.tex` exists. Paper A line 90 still asserts: *"PRISMA-2020 reporting items are listed in Supplementary Table S1 with a graph-encoding addendum."* This artefact does not exist. R1 ask A4 → R2 ask R2-A5 → R3: open. This has now been on the asks list for three rounds. The fix is either: build `supplement_v3.tex` with Tables S1-S4 as R1 specified, or delete the Methods §2.5 sentence. The 30-second fix is the deletion; the right answer is the supplement. As of dadf797 commit, neither has been done.

## A.6 Honest 0.71 → 0.41 R1-correction disclosure: still NOT a Discussion paragraph (MEDIUM)

R2 ask R2-A4 asked for an explicit Discussion paragraph disclosing the R1 bug-fix trajectory (pre-R1 EFDPR 0.48, P = 0.0004; post-R1 0.39, P = 0.023; pre-R1 EGFR-only 0.71, P = 0.0001; post-R1 0.41, P = 0.11). Status after dadf797:
- Results §3.4 line 118 still has only the parenthetical "(post critical-bug fixes; v3 round-1 internal review log in repository)". This is a passing mention.
- Discussion §"Three caveats" line 145 has three caveats — tolerance grid, LLM κ, BOLERO-2 — but does **not** mention the 0.71 → 0.41 EGFR-only correction.
- Discussion §"Three positives" line 148 sub-bullet 2 reads: "the multi-round internal adversarial review process surfaced and corrected 6 NCT-identification errors across v1/v2/v3 with full git-log transparency". This is closer to the spirit of R2-A4 but is framed as a process credit, not a numeric-disclosure of the EFDPR delta.

Combined with Discussion line 136 still saying "12 are evidence-free" (which is the pre-R1 0.71 number), the manuscript reads inconsistent: line 118 implies the corrections were absorbed, line 136 reports a pre-R1 corrected-away number, and the honest pre-vs-post EFDPR comparison is not made anywhere. **R2-A4 partly landed; needs a one-paragraph honest disclosure.**

## A.7 Author block placeholder + Methods §2.1 prereg-trail sentence: STILL NOT DONE (MEDIUM)

R2 ask R2-A6 bundled two ~2-line edits:
- Line 36: `\affil[1]{[Affiliation to be supplied at submission].}` — **untouched**.
- Methods §2.1 line 78: should append v1→v2→v3 prereg-versioning sentence. Currently reads only "(\texttt{docs/prereg-v3.md}, commit \texttt{4b5bf1a}) was committed before any NSCLC outcome-touching analysis". Does not mention v1/v2 preregs are also in `docs/` and at git tags. **Untouched.**

---

# Paper B → Research Synthesis Methods

## B.1 §5.3 tolerance-grid stale numbers (HIGH — still present)

R2 ask R2-B1 flagged Paper B §5.3 line 130: *"ESCAT-aligned and liberal tolerance gave 0.34 (24/50 → 17/50; P = 0.10), failing to reject."* The dadf797 commit **did not** update this line. Three stale numbers:
- "0.34" — canonical is **0.35** (= 17/49 = 0.3469, rounds to 0.35).
- "24/50" — meaningless artifact (24 was a pre-R1 evidence-free count under a different tolerance; the canonical post-R1 strict count is 19 and the ESCAT/liberal count is 17 — neither is "24/50").
- "17/50" — should be **17/49**.
- "P = 0.10" — should be **P = 0.084**.

This is the same defect class as Paper A line 110: the surrounding abstract (line 48) and §5.2 (line 127) have the correct numbers (0.35, P = 0.084), but §5.3 was not swept. A reviewer reading §5.2 → §5.3 sees "0.084 in §5.2, 0.10 in §5.3" and a denominator switching from 49 to 50. Either delete §5.3 (redundant with §5.2) or rewrite to match. **R2-B1: not closed.**

## B.2 "No human-extraction comparator" disclosure: NOT ADDED (MEDIUM)

R1 ask B2 → R2 ask R2-B2 → R3: still not in §5.4 Limitations. The RSM 2025 AI/ML guidance fifth reporting requirement is still uncovered. One-sentence fix: "We did not include a human-extracted reference standard; the dual-LLM design substitutes for a human-vs-LLM comparison. Future work should include a human-extracted subset on ≥30 trials to anchor the LLM-vs-LLM agreement against a human standard." **Three rounds open. Closes the only RSM 2025 AI/ML gap.**

## B.3 Placeholder ORCID `0000-0000-0000-0000`: STILL THERE (HIGH for RSM portal; tolerable for medRxiv)

Line 36: `\affil[1]{[Affiliation to be supplied at submission]. ORCID iD: 0000-0000-0000-0000 (placeholder).}`

For medRxiv: deferrable to portal time (medRxiv tolerates placeholder ORCIDs).
For RSM: the literal `0000-0000-0000-0000` will fail orcid.org validation at the Editorial Manager portal and bounce before the desk editor sees it. This has been open since R1.

Three options remain valid (verbatim from R1 §B.2): register at orcid.org (3 minutes), drop the ORCID line until portal time, or use "Independent Researcher" as the affiliation. None has been chosen.

## B.4 Paper B §6.1 "180 trials" still inconsistent with Paper A's 178 (LOW; cross-paper)

See §A.3 above. Paper B line 124 has "180 trials"; Paper A has settled on "178". Either both should be 180 (in which case Paper A's "178" everywhere — including 259-trial total = 81 + 178 vs the 81 + 180 = 261 that would result) needs to recompute, **or** Paper B comes down to 178. Canonical 259 = 81 + 178 implies Paper A is right and Paper B is stale. The 5-trial supplementary-addition narrative in Paper A line 81 (176 systematic + 5 supplementary − 1 removed = 180, but then "one trial removed for misidentification" implies 179 — actually Paper A's arithmetic doesn't quite add either: 176 + 5 − 1 = 180, not 178. So Paper A line 81's "178" is itself reachable only if 176 + 5 − 3 = 178 or some other counting. **Paper A's own arithmetic in line 81 is wrong** — 176 + 5 − 1 = 180; "one trial removed for misidentification" should be three trials to get to 178, or the "178" number is itself the typo. This needs to be reconciled with Paper B and with the canonical 259 = 81 + ?? total.

## B.5 medRxiv metadata sheet abstract word-count claim: STALE (LOW)

`medrxiv_metadata.md` line 17 still header reads "**Abstract (≤250 words; current = 260 words approximate)**". The current abstract paragraph in line 19 (which is the post-R1 sync'd version with 259 trials, 49 nodes, EFDPR 0.39, P = 0.023) is ~196 words by raw `wc -w`. The "260 words approximate" claim is **stale by two rounds** and is **misleading in the wrong direction** — it claims over-cap when the abstract is comfortably under. medRxiv staff cross-check metadata against manuscript; an internally-contradicting metadata sheet is a portal-side bounce risk. **30-second fix: change "260 words approximate" to "~196 words" or run the canonical RSM word-count rule and use that number.**

## B.6 medRxiv lay-summary numbers: NOW CORRECT (CLOSED)

The lay summary in `medrxiv_metadata.md` line 26 reads "259 pivotal trials and 49 guideline decision points" — correct. R2 §C.1 flagged this as stale at 261/50; the dadf797 sweep closed this one cleanly. **R2 §C.1 lay summary: closed.**

## B.7 medRxiv cover letter: numerically sync'd (CLOSED)

`cover_letter_medrxiv.md` line 14 now reads "rejection of H₀: EFDPR ≤ 0.25 at P = 0.023 on a pooled 49-node decision tree" — correct. R2 §C.2: closed.

---

## Cross-paper concerns

### C.1 The "regen figures" claim in dadf797 (CRITICAL — meta-concern)

The integrator's commit message asserts "regen figures + force-deleted-and-rebuilt"; the file bytes show no change; the PDF text streams show pre-R1 numbers. This is the third round in a row in which the integration step has overstated what landed (R1 integration claimed "fix 6 critical bugs" — they fixed in the JSON and code but not in the figures or cover letter; R2 integration claimed "regen figures" — they did not regenerate). The R3 ask is not just to actually do the work but to **add a regression test** that compares figure-PDF SHA256 against the canonical-results JSON SHA256 and fails the build if the figure is older than the data it visualises. This prevents R4 from being the fourth round of "the commit message says X, the bytes say not-X". A 10-line `make verify-figures` target is sufficient.

### C.2 ORCID placeholder format `0000-0000-0000-0000` will fail RSM/JCO PO portal validation (HIGH — cross-portal)

Both ScholarOne (JCO PO) and Editorial Manager (RSM) validate ORCID against orcid.org's REST API at submission time. The literal `0000-0000-0000-0000` is the documented "test ORCID" reserved by ORCID and the portals reject it with "ORCID validation failed; please provide a valid registered ORCID". For Paper A this is in the cover letter `[FILL IN]` placeholder; for Paper B this is in the manuscript body line 36 plus the `medrxiv_metadata.md` line 15. Three options (R1 §B.2 verbatim): register one, drop the line, or use "Independent Researcher" affiliation. Closing this before next submission requires picking one and propagating across (a) `paper_B_methods_v3.tex` line 36, (b) `medrxiv_metadata.md` line 15, (c) `cover_letter_jcopo_draft.md` line 41, (d) `cover_letter_medrxiv.md` line 29, (e) `paper_A_clinical_v3.tex` line 36-37 author block.

### C.3 Canonical-numbers cheat sheet: NOT ADDED to `release/` (LOW)

R2 ask R2-C1 recommended adding a `release/canonical_numbers.md` (or similar) one-page cheat sheet so that all surfaces (Paper A abstract, KO box, figures, captions, Discussion, Paper B abstract, medRxiv metadata, cover letters) are derived from a single source of truth. The dadf797 commit did not add this. The defence-against-regression value is high relative to cost (≈15-minute one-time write of a markdown file with 12 numbers in it).

---

## Concrete asks for R3 (4 for Paper A · 3 for Paper B · 1 cross-paper = 8)

### Paper A — JCO Precision Oncology

**R3-A1. ACTUALLY regenerate the three v3 figures.** This means: `rm figures/v3_fig{1,2,3}*.pdf`, then `python analysis/v3_09_figures.py` (verify the script reads `data/results/v3_pooled_efdpr.json` and not a stale intermediate cache), then `sha256sum figures/v3_fig{1,2,3}*.pdf` and confirm the digests differ from the pre-R2 ones, then open the PDFs and visually confirm text streams show: Fig 1 title "P = 0.023" and primary row "(n=49)" and NSCLC-only "(n=24)" and ALK-only "(n=7)"; Fig 2 title "49-node guideline tree" and red bars actually present for the 19 evidence-free nodes; Fig 3 v3.0.0 EFDPR "0.39" and "P = 0.023". Add a `make verify-figures` target (or shell script in `analysis/`) that asserts figure SHA256 ≠ previously-cached pre-R2 SHA256 to defend against R4 repeating R3.

**R3-A2. Sweep the five remaining body-prose stale spots** in Paper A (verbatim from §A.2 above):
- Line 73: "$n = 50$" → "$n = 49$".
- Line 90: "50-node pooled denominator" → "49-node".
- Line 110 (Fig 3 caption): "50-node" → "49-node" AND "$-\log_{10} P = 3.4$" → "$-\log_{10} P = 1.64$".
- Line 133: "50 pooled guideline nodes" → "49 pooled guideline nodes".
- Line 136: "12 are evidence-free" → "7 are evidence-free" (canonical EGFR-only = 7/17 = 0.4118 from `v3_pooled_efdpr.json`).
- Also: reconcile line 81 arithmetic ("176 systematic + 5 supplementary − 1 removed" = 180, not 178); either change the math or the final corpus count, and propagate the chosen value to Paper B §6.1 line 124 (which currently says 180).

**R3-A3. Close the cover letter.** Fill all eleven `[FILL IN]` markers (date, EiC name verified against current JCO PO masthead, three suggested reviewers with full institutional details, full name, affiliation, postal address, ORCID, GitHub URL, Zenodo DOI, medRxiv DOI). Delete lines 45-50 "**## Editor pre-screen tips (delete this section before submission)**" meta-section. Replace the placeholder author block in `paper_A_clinical_v3.tex` line 36 with real (or "Independent Researcher") affiliation + a real or removed ORCID. This is R1-A2/A5/A6 → R2-A3 → R3, three rounds.

**R3-A4. Build `manuscript/supplement_v3.tex` and compile** with Tables S1-S4 (PRISMA-2020 + graph-encoding addendum, per-trial structured extractions, 49-node decision-tree encoding with G18-skip / G26-add / N14-skip documented, adjudication-rules log). OR delete the Paper A Methods §2.5 line 90 sentence about Supplementary Table S1. Three rounds open. **Also**: add the honest 0.71→0.41 / 0.48→0.39 R1-correction disclosure paragraph to Discussion §"Three caveats" (R2-A4 second-half open) and add the v1→v2→v3 prereg-trail sentence to Methods §2.1 (R2-A6 second-half open).

### Paper B — Research Synthesis Methods

**R3-B1. Sweep §5.3 tolerance-grid stale numbers** (R2-B1 unchanged). Line 130 needs: "0.34" → "0.35", "24/50 → 17/50" → "(canonical: 17/49)" or rewrite to "ESCAT-aligned and liberal tolerance gave EFDPR 0.35 (17/49; P = 0.084), failing to reject" matching the abstract and §5.2. Easier: delete §5.3 as redundant with §5.2.

**R3-B2. Add the one-sentence human-extraction-comparator disclosure** to §5.4 Limitations (R1-B2 → R2-B2 → R3; three rounds open). Verbatim suggested wording in §B.2 above. Closes the only RSM 2025 AI/ML guidance gap.

**R3-B3. Resolve ORCID + medRxiv metadata word-count + Paper B 180-vs-178** (three small fixes bundled):
- ORCID placeholder `0000-0000-0000-0000` → register, drop, or replace across all 5 surfaces (C.2 above).
- `medrxiv_metadata.md` line 17 header "(≤250 words; current = 260 words approximate)" → recount and update to actual (~196 words).
- Paper B line 124 "180 trials" → reconcile with Paper A's 178 (after R3-A2 reconciles Paper A's own arithmetic).

### Cross-paper

**R3-C1. Add `release/canonical_numbers.md`** with the 12 canonical numbers (n=49, n=25 mBC, n=24 NSCLC, n=17 EGFR, n=7 ALK, EFDPR 0.39 strict, EFDPR 0.35 ESCAT/liberal, P = 0.023, P = 0.084, 19 evidence-free strict, 17 evidence-free ESCAT/liberal, 259 pooled trials, 212 trial-DAG edges, $-\log_{10}(0.023) = 1.64$) and a one-line audit-checklist that every regenerated artefact (figures, cover letters, metadata sheets, abstracts) should match. Add a `make audit-numbers` target that greps for the pre-R1 buggy numbers (0.48, 0.0004, 50-node, 261, 12/17, 0.71, 24/50, 3.4 as $-\log_{10}$) across all release-kit files and fails if any are found. This is the regression-defence that prevents R4 from being R3 redux.

---

## VERDICT — Paper A → JCO Precision Oncology

**MAJOR REVISION** (packaging, with the central R2 critical — figure staleness — un-addressed despite the R2-integration commit message claiming it was).

The science remains solid (pre-registered rejection on the pooled 49-node denominator at P = 0.023; four sensitivity subsets cleanly decompose; ALK-rearranged remains the negative-control; ESCAT/liberal tolerance is honestly reported as marginal non-rejection at P = 0.084). The R1 reference-list defect is closed cleanly. The R2 body-prose sweep landed for **most** of the 14 R2-identified stale spots — but five more remain (§A.2), the figures still report pre-R1 numbers despite the commit message saying otherwise (§A.1), the cover letter still has eleven `[FILL IN]` placeholders plus a self-addressed meta-section (§A.4), the v3 supplement still doesn't exist despite Methods §2.5 still referencing it (§A.5), the honest 0.71→0.41 R1-correction is still not in the Discussion (§A.6), and the author block + prereg-trail sentence are still un-edited (§A.7).

The desk-screen is **blocked** today by:
- Three figures whose displayed numbers contradict the manuscript body (R3-A1).
- Five stale body-prose spots including a Discussion line that reports 12/17 EGFR evidence-free when Results §3.3 and the JSON say 7/17 (R3-A2).
- Eleven `[FILL IN]` cover-letter placeholders plus a delete-before-submission meta-section (R3-A3).
- A Methods reference to a non-existent supplement (R3-A4).
- A 178 vs 180 NSCLC-corpus number disagreement between Paper A and Paper B (R3-A2 + R3-B3).

This is the third round in which the integration step has materially overstated what landed. None of R3-A1 through R3-A4 requires re-running the analysis pipeline; all are mechanical, scoped to a single revision pass, and recoverable inside 5 days **conditional** on R3-A1 actually changing the figure PDF bytes this time and R3-C1's `make audit-numbers` regression target landing alongside to prevent R4 from being R3 redux.

**Submission-ready by:** Day 14 of the original polish plan, **conditional** on R3-A1 (real figure regeneration, verified by SHA256 delta) landing in the next 48 hours.

---

## VERDICT — Paper B → Research Synthesis Methods

**MINOR REVISION** for medRxiv preprint deposit; **MAJOR REVISION** for RSM submission.

For **medRxiv preprint deposit today**: numerics are sync'd (lay summary correct, cover letter correct, abstract numbers correct). Three issues block deposit-as-is:
- §5.3 tolerance-grid stale numbers (R3-B1) — visible-in-PDF.
- medRxiv metadata "260 words approximate" header is stale and misleading (R3-B3 part 2) — visible-in-portal-paste.
- Paper B §6.1 "180 trials" disagrees with Paper A's "178" (R3-B3 part 3) — would be caught by any reviewer cross-checking the two papers.

For **RSM submission**:
- All of R3-B1, R3-B2, R3-B3 must land.
- The placeholder ORCID (C.2) must land before portal-side validation.
- The R2-B2 human-extraction-comparator disclosure (one sentence) is the only RSM 2025 AI/ML guidance gap and has now been open for three rounds.

**Preprint deposit-ready by:** End of today, conditional on R3-B1 (§5.3 fix) + R3-B3 (metadata word-count + 180→178 reconcile) landing in the next 90 minutes.

**RSM submission-ready by:** Day 5 (after preprint DOI is assigned and R3-B1/B2/B3 + C.2 ORCID land; RSM cover letter not yet drafted but is a 1-hour task).

---

*End of dual editor decision letter, v3 round 3.*

**VERDICTS:**
- **Paper A → JCO PO: MAJOR REVISION** (figures still pre-R1 despite dadf797 commit message; 5 stale body-prose spots remain; cover letter has 11 `[FILL IN]` markers + 1 meta-section to delete; supplement still missing; 4 R3 asks + 1 cross-paper ask; the R3 regression-defence (R3-C1) is the structural fix that prevents R4 from being R3 redux)
- **Paper B → RSM: MINOR REVISION** for medRxiv deposit (90-min fix conditional on R3-B1 + R3-B3); **MAJOR REVISION** for RSM submission (3 R3 asks + cross-paper ORCID)
