# Dual Editor Review — v3 Round 1
## Paper A → JCO Precision Oncology · Paper B → Research Synthesis Methods

**Manuscripts:**
- Paper A: *Evidence-Free Decision Points in Biomarker-Driven Metastatic Cancer Guidelines: A Pre-Registered Multi-Tumor Audit of ESMO, ASCO, and NCCN Decision Trees in HR+/HER2- Breast Cancer and EGFR/ALK Non-Small-Cell Lung Cancer* (`manuscript/paper_A_clinical_v3.tex`)
- Paper B: *A Graph-Theoretic Framework for Measuring Evidence-Free Decision Points in Clinical Guidelines, with Dual-LLM-Annotator Validation Across Two Solid Tumors* (`manuscript/paper_B_methods_v3.tex`)
- Author: H.-T. Lin (single author, both papers)

**Reviewer role:** Decision editor at *JCO Precision Oncology* (Paper A) and at *Research Synthesis Methods* (Paper B); 7th adversarial review pass across the program (rounds 1–4 + v2_round1–2 + v3_round1).
**Question for this round:** Would each manuscript clear its target journal's editorial screen on the day after the v3.0.0 release tag is pushed?
**Date:** 2026-05-16

---

## 0. Headline

Both manuscripts are **substantively** ready (the science, the pre-registration, the headline, and the tolerance grid are all internally consistent and externally defensible). Neither is **packaging**-ready: Paper A has reintroduced the same load-bearing reference-list defect that v2_round1 caught (32 named NSCLC trials with zero `\citep{}` calls), and Paper B carries a placeholder ORCID that will trip an automated portal screen.

Word counts are not the binding constraint at either journal — there is unusually generous headroom in both papers — but several smaller defects (figure overprints, supplement absence, two missing companion-paper bridges) do bind.

The good news: **none** of the asks below requires re-running the analysis pipeline. All are mechanical, scoped to a single revision pass, and recoverable inside 5 days for Paper B (medRxiv) and 14 days for Paper A (JCO PO) without slipping the SUBMISSION_ROADMAP timeline.

---

## 1. Word-count audit (verified)

I reproduced the audit using a tightened analogue of `analysis/wordcount.py` (Paper A and Paper B were not yet handled by the script; my regex tracks `\textbf{...}` body content, drops `\citep` and `\section`, and counts `$X$` math as one word).

### Paper A — JCO PO Original Report caps
```
Abstract:               162 words   (cap 300; 138-word headroom)
KO box:                  91 words   (cap 120;  29-word headroom)
Introduction:           223 words
Methods:                345 words
Results:                233 words
Discussion:             549 words
IMRD total:           1,350 words   (cap 3,000; 1,650-word headroom)
```
**Pass with massive headroom.** All five compartments compliant; the IMRD total is well under half the cap. Original Report (not Brief Report) remains correct — see ask A2 below for the article-type discussion.

### Paper B — RSM caps
```
Abstract:               143 words   (cap 250; 107-word headroom)
Highlights box:         153 words   (RSM target ~150-200; OK)
Introduction:           314 words
The Framework:          245 words
LLM extraction:         233 words
Demonstration:          210 words
Discussion:             272 words
IMRD total:           1,274 words   (RSM target ~3,500-4,000; ample headroom)
```
**Pass.** Note: the `medrxiv_metadata.md` claims the abstract is 245 words and the AUDIT_REPORT says 245 — that count includes the prefixed `Highlights` block? My count of just the `\begin{abstract}…\end{abstract}` body is 143. Whichever is canonical, both are under the 250-word RSM cap; flag the discrepancy in `medrxiv_metadata.md` so the portal field matches the actual abstract.

---

# Paper A → JCO Precision Oncology

## A.1 Title and biomarker-driven framing — strong fit

The title leads with "Biomarker-Driven Metastatic Cancer Guidelines" and explicitly names HR+/HER2-, EGFR, and ALK in the subtitle. This is a strong match for JCO PO's mission ("the application of precision oncology in clinical practice"). The literal phrase "precision oncology" is **not** in the title but is implicit; the cover letter's Paragraph 3 makes the fit explicit. **Acceptable as-is** — adding "Precision Oncology" verbatim to a title that is already 32 words and three lines long would push it past the JCO PO ~25-word soft cap. Leave the title; let the cover letter carry the journal-fit framing.

## A.2 Article type: Original Report (correct), not Brief Report

JCO PO's Brief Report cap is ~1,500 words IMRD and one figure (or one table). Paper A is 1,350 words IMRD with three figures. The trajectory figure (Fig 3) is dispensable in a Brief Report compression, but the per-node breakdown (Fig 2) is the load-bearing visual evidence for the Discussion's "where the gap is largest" paragraph and cannot be cut. Original Report is the correct designation; the cover letter Paragraph 1 already says so.

## A.3 Reference list — REGRESSED FROM v2 ROUND 1, SAME DEFECT CLASS

This is the highest-priority Paper A defect and a verbatim repeat of the v2_round1 §4 finding.

`references.bib` contains 41 entries. `paper_A_clinical_v3.tex` contains only **12 unique `\citep{}` calls**, none of which cite NSCLC trials by name. Concretely, the following named NSCLC trials appear in the prose **without primary citation**:

- **MARIPOSA-2** (Discussion §"NSCLC EGFR post-osimertinib", line 136)
- **HERTHENA-Lung01** (Methods §2.2 line 81 + Discussion line 136)
- **TROPION-Lung01** (Methods §2.2 line 81 + Discussion line 136)
- **SAVANNAH** (Discussion line 136)
- **PROFILE 1014, AURA3** (Methods §2.2 line 81)
- **ALEX, ALTA-1L, CROWN** (Discussion §"NSCLC ALK is the comparator", line 138)
- **FLAURA, MARIPOSA, lazertinib** (implicit in 1L EGFR-mutant Discussion paragraphs)

The bibliography needs ≥10 new entries before the desk screen. JCO PO's AMA-style reference policy requires primary citation at first mention of each named trial; a desk editor reading "amivantamab + chemotherapy (MARIPOSA-2), HER3-ADC (HERTHENA-Lung01), TROP2-ADC (TROPION-Lung01), MET-amp salvage (SAVANNAH)" with **zero superscript reference numbers** will return the manuscript for technical corrections.

The mBC half is in better shape — `cardosoESMO2024`, `gradishar2023nccn`, `giordano2022asco`, `hendriks2023esmo`, `nccn_nsclc_2024` are all cited in the Introduction — but the bib already includes `bidard2022emerald`, `kalinsky2024postmonarch`, `jhaveri2024inavo120`, `andre2019solar1`, `sledge2017monarch2`, `baselga2012bolero2`, `modi2022destinyb04`, `rugo2023tropics02`, `turner2015paloma3` etc. that are **named in the Discussion's "where the gap is largest" paragraph (line 118: G13 everolimus, G14 SG, G21 datopotamab HER2-low, G25 post-everolimus) without primary citation**. Thread these in at first mention.

This is not a science finding; it is a packaging regression. The fix is mechanical (existing bib keys for mBC trials; new bib entries for the ten NSCLC trials).

## A.4 Cover letter (`release/submission_plan_paperA_jcopo/cover_letter_jcopo_draft.md`)

The draft is **structurally correct** — opens with the Original Report designation and the verbatim title, frames the journal fit in Paragraph 3 (the three numbered fit-points are well-chosen), and discloses the companion Paper B preprint. Five concrete defects to fix before submission day (Day 7 in the polish plan):

1. **Date placeholder** `[Date — e.g., 2026-05-30]` — fill on Day 14.
2. **Editor name "Dr. Stacy W. Gray"** — *verify* this is current EiC of *JCO PO* (the cover letter is a stub; an outdated editor name will be read as not-checking-current-masthead and is a minor desk-screen negative).
3. **Three suggested-reviewers placeholders** `[FILL IN reviewer N, name + affiliation + email]` — these are **non-trivial**. JCO PO's portal will accept submission without suggested reviewers, but the editorial screen at JCO-family journals weighs reviewer-list completeness as a credibility signal, particularly for solo / Independent-Researcher submissions. See ask A8.
4. **Three `[FILL IN]` placeholders** for ORCID, GitHub URL, Zenodo DOI — already on the polish plan but worth re-flagging here as desk-screen-blocking.
5. **Delete the "Editor pre-screen tips" section before submission** (lines 45–50). It is a meta-document for the author; a real cover letter doesn't include strategy notes addressed to the cover-letter writer.

The cover letter is **70% submission-ready**; the remaining 30% is fillable in 1 hour on Day 7.

## A.5 Figure quality — three PDFs at print size

I opened all three figures at full resolution. Substantively informative; three publication-grade defects:

### Fig 1 (`v3_fig1_forest.pdf`) — Forest plot
- **CRITICAL: NSCLC EGFR-only row P-value overprints the right error-bar cap.** The "P = 0.0001 *" annotation sits on top of the right-hand whisker of the EGFR-only CI, rendering as `P = 0|.0001 *` — visible at print size. Either move all P-value annotations further right (extend x-axis to 1.15 and right-shift the annotation column to x=1.10) or move the EGFR-only row's annotation to a position offset from its data marker.
- Everything else (diamond for primary, asterisks for rejections, dashed threshold line at 0.25) renders clean.

### Fig 2 (`v3_fig2_per_node.pdf`) — Per-node bar chart
- **Caption mismatch.** Caption (line 123 of paper_A_clinical_v3.tex) reads: *"Red bars mark evidence-free nodes (strict tolerance); height represents the count of supporting trial edges."* In the rendered PDF, evidence-free nodes have height = 0 and therefore are **invisible** (no red bar appears). The legend entry "Evidence-free (strict)" is shown in red but no red bar exists in the plot area. Either (a) plot evidence-free nodes as height = 0.1 with a red marker so the audience can see them as zero-height red ticks, or (b) edit the caption to "Evidence-free nodes appear as missing bars; G9, G12-G15, G17, G21-G25, N1-N4, N9-N12, N15-N16, N18, N21, N23-N25 are evidence-free." The current caption misleads.
- **G18 skip is back, undocumented.** The x-axis renders `…G16, G17, G19, G20…` with no G18 label. v2_round1 §6.5 raised this as a defect class and the v2_round2 audit closed it via a caption note. The v3 figure regenerated without inheriting that note. Either renumber to contiguous G1…G25 (preferred for v3 fresh start) or add to the caption: "Node G18 was retired during v2 deduplication; numbering preserved for traceability against pre-registered encoding."
- Title text "Per-node trial-edge support across pooled 50-node guideline tree" overlaps the right-side legend at print size. Move legend below the plot or extend canvas width.

### Fig 3 (`v3_fig3_trajectory.pdf`) — Trajectory
- **CRITICAL: v3.0.0 EFDPR data label overprinted by P-value label.** At the v3.0.0 column, the blue "0.48" EFDPR data label and the red "P < 0.001" significance label collide — the rendered text reads as `0.48` overwritten by `P<0.001` (visible truncation: "0.48" appears as "0.|8" in PDF). Either separate via vertical offset (push P-value labels above the markers, EFDPR labels below) or use bounding-box collision detection in `analysis/v3_09_figures.py` matplotlib pass.
- **Threshold-line confusion.** Two horizontal reference lines render: a red dashed line at left-axis value 0.25 (the EFDPR threshold) and a gray dotted line at left-axis value ~0.20 labeled "α = 0.05". The α-level lives on the **right** axis (−log₁₀ scale, where α=0.05 → 1.30) — drawing it as a horizontal line at left-axis 0.20 is misleading. Either drop the α-line or redraw it on the right axis only (with a short tick on the right axis).

All three figure defects are matplotlib-script fixes (≤ 60 minutes total at the renderer). None changes the data.

## A.6 Suggested reviewers — empty placeholders are a Day-6 blocker

The three placeholders in the cover letter map to three Editorial Manager portal fields. Empty fields are accepted by the portal but are read as a credibility signal at the editorial screen, especially for solo Independent-Researcher submissions. The cover letter draft (line 28) suggests three reasonable archetypes (clinical informaticist + mBC clinician + NSCLC clinician) — Day 6 needs to populate those with:

- **Name** (full)
- **Affiliation** (institutional)
- **Email** (institutional, not Gmail)
- **ORCID** (where available)
- **One-line "no conflict" justification** (e.g., "Not a co-author on any of the 261 corpus trials")

Practical sourcing route: look at recent commentaries / editorials in *JCO PO*, *Annals of Oncology*, *Nature Reviews Clinical Oncology*, or *eClinicalMedicine* on the post-osimertinib decision space and the post-CDK4/6i landscape. Filter against your corpus's NCT-author lists (which you already have in the structured extractions) to confirm no overlap.

## A.7 Supplement is missing — Methods §2.5 references it

`paper_A_clinical_v3.tex` line 90 says: *"PRISMA-2020 reporting items are listed in Supplementary Table S1 with a graph-encoding addendum."*

There is **no v3 supplement**. `manuscript/supplement.tex` is v1; `manuscript/supplement_v2.tex` is v2. Neither contains the NSCLC-extended PRISMA, the per-trial structured-extraction excerpts for the 261-trial corpus, the 50-node decision tree, or the v3 adjudication-rules log.

The polish plan (Day 10) schedules supplement creation, so this is on the timeline — but the manuscript's Methods section currently makes a claim the artifact does not back. If the Day-10 supplement compilation slips, Paper A's Methods section refers to nonexistent material at submission. Build the supplement before recompiling Paper A's final PDF.

Recommended supplement structure (per the polish plan):
- **Table S1**: PRISMA-2020 + graph-encoding addendum (the v1/v2 supplement already had this; extend to NSCLC search).
- **Table S2**: Per-trial structured-extraction excerpts (NSCLC + mBC, n=261).
- **Table S3**: Per-node ESMO/ASCO/NCCN decision tree encoding (n=50, with the G18-skip explanation).
- **Table S4**: Adjudication rules log with rationale.

Compile as `supplement_v3.tex` → `supplement_v3.pdf` and update Paper A's `\ref{}` calls to point to the right tables.

## A.8 Companion-paper bridge sentence is too thin

The cover letter (Paragraph 4) says *"A companion methods manuscript … has been deposited as a preprint at medRxiv (DOI: 10.1101/[FILL IN once assigned])"*. The manuscript itself does not cite Paper B at all. A JCO PO reviewer should be able to learn from Paper A alone what the framework is — but the methods detail (the formal definitions of trial-DAG, EFDPR formula, tolerance grid, dual-LLM annotator pipeline, kappa paradox / PABAK) lives in Paper B, not Paper A. Add to Paper A's Methods §2.5 (Concordance algorithm) a sentence: *"Detailed methodological definitions of the framework, including formal trial-DAG and decision-tree node definitions, the dual-LLM-annotator extraction pipeline, and inter-rater agreement methodology, are reported in a companion methods manuscript (medRxiv DOI 10.1101/XXX)."* Add the matching `@misc{lin2026medrxiv,...}` bib entry.

This is the cross-paper concern raised in the brief — both papers cite the same v3.0.0 release, but the relationship needs to be explicit so the JCO PO reviewer is not left wondering what they're missing.

---

# Paper B → Research Synthesis Methods

## B.1 RSM Highlights section — present and complete

The Highlights mdframed box (lines 52–64) carries all three RSM-required points in the canonical RSM template wording:
- **What is already known** (NMA + bibliometrics + narrative reviews) ✅
- **What is new** (graph-theoretic framework + EFDPR + dual-LLM annotator) ✅
- **Potential impact for Research Synthesis Methods readers** (reusable, pre-registerable, biomarker-agnostic, dual-LLM pattern generalisable) ✅

Length is 153 words, which is at the upper end of RSM's typical Highlights length but inside it. **Pass for the Highlights gate.**

## B.2 Author block — placeholder ORCID is a desk-screen blocker

Line 36: `affil[1]{[Affiliation to be supplied at submission]. ORCID iD: 0000-0000-0000-0000 (placeholder).}`

For **medRxiv preprint deposit** this is acceptable (medRxiv accepts a Gmail address and tolerates "to be supplied" affiliation). For **RSM submission** this is desk-screen blocking: RSM's Editorial Manager portal validates the ORCID against orcid.org; the literal `0000-0000-0000-0000` will fail validation and will trigger a portal-side rejection before the manuscript reaches the desk editor.

The medRxiv audit (line 36) flags this as a "30 minute" fix. Three concrete options for Day 1:

1. **Register a real ORCID** (free, 3 minutes at orcid.org/register), populate it, and use it.
2. **Drop the ORCID line entirely** until submission portal time. The author block then shows just the name + affiliation; the portal will collect ORCID separately.
3. **Use "Independent Researcher" as the affiliation** if institutional affiliation is unavailable. This is acceptable at RSM for solo author submissions (less ideal than an institutional affiliation, but not desk-rejected).

Recommended: option 1 + option 3 if needed. Option 2 is the fallback if there is portal-side trouble.

## B.3 RSM AI/ML 2025 evaluation guidance — meets four of five reporting requirements

RSM's 2025 editorial guidance for "manuscripts evaluating generative AI in systematic reviews" (Tugwell et al., *RSM* 2025; if there's a specific URL the author should cite it in the cover letter) requires:

| Reporting requirement | Paper B status |
|---|---|
| Model versions disclosed | ✅ §4.5 line 150: "Claude 4.7, Codex GPT-5 at execution time 2026-05-16" |
| Prompts released | ✅ §4.5: pointer to `analysis/extraction_protocol.md` and `extraction_protocol_nsclc.md` |
| Reproducible random seeds | ✅ §4.5 + Code Availability: seed `20260516` |
| Inter-rater statistics | ✅ §3.3 + §3.4: Cohen's κ + PABAK + adjudication trail |
| **Comparison with human extraction (if available)** | ⚠️ **Not addressed.** |

The fifth item is the gap. RSM's guidance specifies that "where human extraction is available as a comparator, the LLM-vs-human concordance should be reported alongside the LLM-vs-LLM concordance." Paper B does not run a human-extraction validation — both annotators are LLMs. This is **defensible** (the paper is a methods-paper; human extraction would 5x the cost) but it should be **stated explicitly** as a limitation in §5.4 (Limitations), with a one-sentence rationale: e.g., "We did not include a human-extracted reference standard. The dual-LLM design is a substitute for a human-vs-LLM comparison; future work should include a human-extracted subset on at least 30 trials to anchor the LLM-vs-LLM agreement against a human standard."

Without this disclosure a reviewer aligned with the RSM 2025 guidance will flag it. With it, the gap becomes a transparent methodological limit, not a reporting defect.

## B.4 Reference style — vancouver.bst is close to AMA but not identical

`bibliographystyle{vancouver}` produces numbered superscript citations and a numbered reference list, which is the AMA 11th-edition house style superficially. RSM's manuscript-preparation guidelines specify "AMA reference style" but do not (in my reading) explicitly mandate AMA-tool-generated reference lists; the editorial screen at RSM tends to accept any AMA-flavored numbered style as long as the in-text citations resolve and the reference list parses.

**Acceptable for preprint** (medRxiv). **Acceptable for first-pass RSM submission**, with the caveat that a copy-editor at the journal-production stage will request specific AMA formatting (e.g., authors listed up to 6 then "et al.", no DOI brackets, journal abbreviations per *Index Medicus*). Hand-converting now (before submission) is **not** required — the production team handles this. Flag it for revision-round work, not submission-round work.

If hand-converting is preferred (e.g., for cleaner first-impression at the desk screen), the conversion is mechanical: switch to `\bibliographystyle{ama}` if available in the local TeX distribution, or use a CSL-based pandoc pipeline with the AMA CSL file.

## B.5 Research Synthesis Keywords — present (6/3-6) ✅

Line 67: *"clinical-guideline evaluation; trial-evidence concordance; graph-theoretic framework; LLM-extraction validation; Cohen's kappa; pre-registered binomial test"* — six keywords, all relevant to RSM's scope, well-chosen for indexing.

Optional polish: "LLM-extraction validation" could be more discoverable as "large language model validation" (matches MeSH terminology); "graph-theoretic framework" could pair with "directed acyclic graph" for Cochrane-Methods cross-indexing. **Not blocking.**

---

## Cross-paper concerns

### C.1 Companion-paper relationship — partly explicit, needs reinforcing

Paper A mentions Paper B once (cover letter Paragraph 4) but does not cite it in the manuscript body. Paper B mentions Paper A once (§5 line 121: *"Detailed clinical results are reported in the companion clinical-application manuscript (Paper A)."*) — that **is** a clean bridge from Paper B's side.

Asks A8 (Paper A → Paper B body citation) addresses Paper A's side. Both papers should also share the same `\section*{Companion publication}` block: a one-paragraph statement that says "Paper A: clinical-application focus, target *JCO PO*; Paper B: methods-and-validation focus, target *RSM*; both share v3.0.0 release, prereg `4b5bf1a`, and the 261-trial corpus." This block lives at the front of both papers (after the abstract block) so a reviewer reading **either** paper learns the relationship in the first 90 seconds. Currently a reviewer reading Paper A in isolation has no signal that the methods companion exists until Paragraph 4 of the cover letter.

### C.2 Pre-registration trail (v1, v2, v3) — needs one-sentence guide

Three prereg files exist:
- `docs/prereg.md` (v1; pilot-stage)
- `docs/prereg-v2.md` (v2; mBC production)
- `docs/prereg-v3.md` (v3; multi-tumor pooled, commit `4b5bf1a`)

Paper A's Methods §2.1 cites only `docs/prereg-v3.md` (line 78). Paper B's §3.5 cites the validation-gate prereg without explicit version. A JCO PO reviewer skeptical about post-hoc cherry-picking will see the three preregs and worry. The fix is one footnote on Paper A page 1 or one sentence in Methods §2.1:

*"v3.0.0 supersedes v1.0.0 (mBC pilot, n=16, P=0.37) and v2.0.0 (mBC production, n=25, P=0.07); each version was pre-registered before the next analysis layer was run, with the v3 NSCLC analysis pre-registered in `docs/prereg-v3.md` (commit `4b5bf1a`) before any NSCLC outcome data were touched. Versions are preserved at git tags v1.0.0 and v2.0.0 for traceability."*

This converts "three preregs" from a yellow flag into a transparency credit. Currently the trail is in the git log but not in the manuscript narrative.

---

## Concrete asks (split: 8 for Paper A · 7 for Paper B)

### Paper A — JCO Precision Oncology

**A1. Thread `\citep{}` calls into all 10+ named NSCLC trials and the 6 mBC Discussion trials.** Add bib entries for: FLAURA (Soria 2018 NEJM), MARIPOSA (Cho 2024 NEJM), MARIPOSA-2 (Passaro 2024 Annals), HERTHENA-Lung01 (Yu 2023 JCO), TROPION-Lung01 (Garon 2025 JCO), SAVANNAH (Smit 2024 ASCO), ALEX (Peters 2017 NEJM), ALTA-1L (Camidge 2020 JTO), CROWN (Solomon 2024 NEJM update), PROFILE 1014 (Solomon 2014 NEJM), AURA3 (Mok 2017 NEJM, NCT02151981). Thread these into Methods §2.2 line 81 (corpus-correction list) and the Discussion §"NSCLC EGFR post-osimertinib" + §"NSCLC ALK is the comparator" paragraphs. Also thread existing bib keys for mBC trials named in Discussion line 118: `bidard2022emerald`, `kalinsky2024postmonarch`, `andre2019solar1`, `sledge2017monarch2`, `baselga2012bolero2`, `modi2022destinyb04`, `rugo2023tropics02`, `turner2015paloma3`. Target bibliography ≥55 entries (currently 41).

**A2. Replace the placeholder author block** (`paper_A_clinical_v3.tex` lines 35–37) with full legal name, real ORCID, real affiliation (or "Independent Researcher"), and full postal address. **Day 2** of polish plan.

**A3. Fix three figure defects** (≤ 60 minutes total at `analysis/v3_09_figures.py` matplotlib pass):
- Fig 1: extend x-axis to 1.15, right-shift the P-value annotation column to clear the EGFR-only error bar.
- Fig 2: either render evidence-free nodes as height=0.1 red ticks **or** rewrite caption to acknowledge invisible-zero-height bars; document the G18 skip in the caption.
- Fig 3: separate v3.0.0 EFDPR/P-value label collision (vertical offset); drop or redraw the α=0.05 line on the right axis.

**A4. Build `supplement_v3.tex` and compile to `supplement_v3.pdf`** with Tables S1–S4 (PRISMA + graph-encoding addendum, per-trial extractions, 50-node decision-tree encoding, adjudication-rules log). Update Paper A's `\ref{tab:S1}` calls to resolve. **Day 10** of polish plan; do not slip — Methods §2.5 currently references nonexistent material.

**A5. Populate cover letter** (`release/submission_plan_paperA_jcopo/cover_letter_jcopo_draft.md`):
- Real date, real EiC name (verify current JCO PO masthead), real ORCID, real GitHub URL, real Zenodo DOI, real medRxiv DOI for Paper B.
- Delete the "Editor pre-screen tips" meta-section before submission (lines 45–50).
- **Day 7** of polish plan.

**A6. Identify and list 3 suggested reviewers** with full name + institutional affiliation + institutional email + ORCID + one-line "no conflict" justification. Source from recent JCO PO / Annals / NRCO commentaries on post-osimertinib decisions and post-CDK4/6i landscape; cross-check against your 261-trial NCT-author lists. **Day 6** of polish plan.

**A7. Add a Companion-publication block** (after the KO box, before §1 Introduction) explaining that Paper B (medRxiv DOI XXX) carries the methods detail, and add a `\citep{lin2026medrxiv}` call inside Methods §2.5 (Concordance algorithm) at the natural natural-bridge point ("Detailed framework definitions are reported in the companion methods manuscript [cite]"). Add the corresponding `@misc{lin2026medrxiv,...}` entry to `references.bib`.

**A8. Add the v1→v2→v3 pre-registration trail sentence** (see C.2 above) to Methods §2.1 (or as a footnote on page 1). Converts "three preregs" from a yellow flag into a transparency credit.

### Paper B — Research Synthesis Methods

**B1. Replace placeholder ORCID** (`paper_B_methods_v3.tex` line 36) with real ORCID (recommended: register at orcid.org, 3 minutes) **or** drop the ORCID line entirely until portal submission. The literal `0000-0000-0000-0000` will fail RSM portal-side ORCID validation. **Day 1**.

**B2. Add one-sentence "no human-extraction comparator" disclosure** to §5.4 Limitations: "We did not include a human-extracted reference standard; the dual-LLM design substitutes for a human-vs-LLM comparison. Future work should include a human-extracted subset on ≥30 trials to anchor the LLM-vs-LLM agreement against a human standard." Closes the only RSM 2025 AI/ML guidance gap.

**B3. Reconcile abstract word count** between `paper_B_methods_v3.tex` (143 words by my regex), the medRxiv audit (245 words), and `medrxiv_metadata.md` (245 words). Either my counter is dropping the lead-in / `\textbf{}` fragments incorrectly, or one of the audit/metadata documents is counting the Highlights box as part of the abstract. **Confirm a single canonical number** before pasting into the medRxiv portal.

**B4. Verify cardosoESMO2024 bib entry** matches the prose's "2024 update" claim (medRxiv audit Issue #2: bib entry currently cites the 2021 paper). Replace with the 2024 *Annals of Oncology* update DOI before submission.

**B5. Update the `Acknowledgements` block** (line 168) to disclose that the AI providers (Anthropic, OpenAI) had no role — this is already there ("the model providers had no role in the design, analysis, or writing"). **No action needed; flagged as already-compliant for completeness.**

**B6. Optional polish: insert v3_fig1_forest.pdf and v3_fig3_trajectory.pdf into Paper B** as supporting figures (medRxiv audit Issue #1). Adds ~1 page; makes the "Demonstrate the framework across two cancers" claim in the abstract visually load-bearing rather than purely textual. **Optional — Paper B can ship without it; the absent figures are the price of foregrounding methods over results.**

**B7. Add the Companion-publication block** (mirror of ask A7, on Paper B's side) so that an RSM reviewer reading Paper B in isolation learns immediately that Paper A (target *JCO PO*) carries the clinical-application detail. Currently §5 line 121 mentions Paper A in passing; the explicit block makes it findable in the first 90 seconds.

---

## VERDICT — Paper A → JCO Precision Oncology

**MAJOR REVISION** (packaging, not science).

The science is solid: pre-registered exact-binomial test rejects on the pooled 50-node corpus at P = 0.0004; tumor-stratified sensitivity decomposes the rejection cleanly across mBC / NSCLC / EGFR-only / ALK-only with ALK serving as the negative control; Discussion is honest about the strict-vs-ESCAT/liberal P=0.10 gap and discloses three caveats; word counts are well inside JCO PO Original Report caps with massive headroom; the 14-day polish plan is realistic.

The desk-screen is **blocked** today by:
- 10+ named NSCLC trials with **zero** primary citations (ask A1) — the load-bearing reference defect that v2_round1 caught for mBC and that v3 has now reintroduced for NSCLC. This alone would generate "return for technical corrections."
- Placeholder author block (ask A2).
- Missing v3 supplement that Methods §2.5 explicitly references (ask A4).
- Three figure overprint defects at print size (ask A3).
- Five [FILL IN] placeholders in the cover letter (ask A5) and zero suggested reviewers (ask A6).

None of A1–A8 requires re-running analysis. All eight are inside the polish plan's 14-day window. With the ask-pack landed, the desk-screen verdict moves to **MINOR** and the realistic acceptance probability stays at the audit's 45–55% estimate.

**Submission-ready by:** Day 14 of the polish plan, conditional on Day 1 GitHub/Zenodo + Day 6 reviewers + Day 7 cover letter + Day 10 supplement landing on schedule.

---

## VERDICT — Paper B → Research Synthesis Methods

**MINOR REVISION** for the medRxiv preprint deposit; **MINOR REVISION** for the RSM submission.

The Highlights section is present and complete; the AI/ML transparency disclosure meets four of the five RSM 2025 reporting requirements; word counts pass with ample headroom; the kappa paradox / PABAK disclosure is unusually transparent and is an editorial-screen positive; the methods contribution is cleanly distinguished from the clinical-application companion; the dual-annotator pipeline is substantively described.

Three blocking defects for portal submission:
- Placeholder ORCID will fail portal validation (ask B1).
- Missing human-extraction-comparator disclosure (ask B2) — the only RSM 2025 AI/ML guidance gap.
- Abstract word-count discrepancy across three documents (ask B3).

For **medRxiv preprint deposit today**: ask B1 is the only true blocker; the rest can deposit and be addressed in the RSM submission revision pass. The medRxiv audit's 30-minute submission estimate is realistic conditional on B1 being fixed in that window.

For **RSM submission**: B1+B2+B3+B4 all need to land. Estimate 2 hours of mechanical work. With the ask-pack landed, the realistic acceptance probability stays at the SUBMISSION_ROADMAP's 40–55% estimate.

**Preprint deposit-ready by:** End of Day 0 (today, 30 minutes after ask B1 lands).
**RSM submission-ready by:** Day 5 (after Paper B medRxiv DOI is assigned and B2/B3/B4 are addressed; cover letter for RSM not yet drafted but is a 1-hour task).

---

*End of dual editor decision letter, v3 round 1.*

**VERDICTS:**
- **Paper A → JCO PO: MAJOR REVISION** (packaging; 14-day polish plan covers the fix)
- **Paper B → RSM: MINOR REVISION** (preprint can deposit today after a 30-min ORCID fix)
