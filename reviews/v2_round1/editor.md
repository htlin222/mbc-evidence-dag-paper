# JCO Clinical Cancer Informatics — Editor Review, v2 Round 1

**Manuscript:** *A Computable Map of Treatment-Sequencing Evidence in HR+/HER2-
Metastatic Breast Cancer: A 64-Trial, Pre-Registered Graph-Theoretic Analysis
of ESMO, ASCO, and NCCN Decision-Tree Concordance*
**Author:** H.-T. Lin (single author)
**Reviewer role:** Decision Editor, editorial-screen simulation, JCO CCI
**Question for this round:** Does the v2 production manuscript clear the
editorial screen for **journal submission** (Original Report) at JCO CCI?
**Date:** 2026-05-16

---

## 0. Summary

This is a substantive upgrade from the v1 pilot (16 nodes, P=0.37, did not
reject) to a production analysis (25 nodes, 64-edge in-scope trial-DAG,
P=0.0002, rejects). The pre-registration trail (commits `085ae54` and `079b540`)
is cited correctly at two points in the manuscript (Methods §2.1 and the
Preregistration statement on line 190); the abstract, KO box, and Headline
paragraph in the Discussion are mutually consistent at the new effect size
(0.60, 95% CI 0.39–0.79); and the three pre-specified by-guideline-source
sensitivity analyses are reported faithfully, including the ASCO-citing
marginal P=0.057. Word counts are inside JCO CCI caps with comfortable
headroom.

The reason this is not yet acceptable at the editorial screen is **not** the
science — it is **manuscript hygiene that regressed during the v1→v2 rewrite**.
Three specific defects would, at a real JCO CCI desk pass, generate a "return
for technical corrections" rather than an out-for-review decision:

1. **Reference list collapsed.** v1 had 21 bibliography entries with each
   named trial carrying a `\citep{}` call at first mention. v2 has the same
   bib (`references.bib` unchanged) but **only three** `\citep{}` calls remain
   in `main_v2.tex` (lines 74 and 76) and **zero** in `discussion_v2.tex`. The
   load-bearing first-pass-screen fix from Round 3 of the v1 cycle is gone.
2. **Cover letter is still the v1 letter.** Title, article framing, P-value,
   and "16-trial pilot" language all describe the v1 result. The reviewer
   reading the cover letter will be confused about what manuscript they have.
3. **Three of the four figures have legibility defects** that print review at
   90% of `\linewidth`: legend-on-data overprints in Fig 1 and Fig 2, an
   axis-label typo in Fig 3, and an aspect-ratio / scale mismatch in Fig 4.

All three are mechanical fixes, all three need to land before the manuscript
goes to peer review, and none of them touches the analysis or its conclusions.

---

## 1. Word-count audit

Reproduced with the inline script in the editor brief:

```
Abstract:    268 words   (cap 300; 32-word headroom)
KO box:       79 words   (cap 120; 41-word headroom)
Introduction: 350 words
Methods:      707 words
Results:      403 words
Discussion:   672 words
Main total: 2,132 words  (cap 3,000; 868-word headroom)
```

**Pass.** All five compartments compliant with headroom. The Methods is the
single largest section (707) which is appropriate given the new dual-annotator
protocol, ODI, and concordance algorithm; if compression is ever needed in a
revision round, Methods §2.2 + §2.4 can collapse without losing
reproducibility.

## 2. Cover letter (`docs/cover_letter.md`) — OUT OF SYNC with v2

The cover letter is the v1 letter, verbatim. Concrete mismatches:

- **Title** (line 13–15) reads *"Graph-Theoretic Pilot Comparing Trial Chains
  with the ESMO Guideline Decision Tree"* — must read *"64-Trial,
  Pre-Registered Graph-Theoretic Analysis of ESMO, ASCO, and NCCN Decision-
  Tree Concordance"* (matches `main_v2.tex` lines 34–36).
- **Framing paragraph** (lines 26–33) says *"This 16-trial pilot is a
  pre-registered methodology submission ... the pre-registered exact-binomial
  test of EFDPR > 0.25 did not reject the null in this corpus (P = 0.37)"*.
  The v2 result is the opposite (n=25 unified nodes against 64 in-scope trials;
  P = 0.0002; primary null rejected). Leaving the v1 framing in place would
  be read by a desk editor as either a submission of the wrong manuscript or
  a serious mis-statement of findings.
- **Methodology framing** says "methodology submission" — v2 is no longer
  primarily a methods paper; it is a confirmatory study with a methods
  contribution. The cover letter should reposition accordingly (Original
  Report, hypothesis-driven, pre-registered).
- **Preprint statement** (line 38) says "A preprint copy will be posted to
  medRxiv concurrent with this submission" — fine, but the v2 cover letter
  should also cite the v1 preprint (if posted) and note v2 supersedes it.

This is the single highest-priority fix.

## 3. Pre-registration commit hashes

Both hashes are cited in the manuscript:

- `085ae54` — Preregistration statement at `main_v2.tex` line 190 (original
  v2 prereg).
- `079b540` — Methods §2.1 at line 85 ("amendment v2.1") and Preregistration
  statement at line 190.

**Pass.** Both first-prereg and amendment hashes are findable from the
manuscript, located in the two natural places (Methods top and end-of-paper
statement block). No fix needed.

## 4. Reference list — REGRESSED FROM v1

`references.bib` contains 21+ entries covering each named pivotal trial
(PALOMA-2 → `finn2016paloma2`, OlympiAD → `robson2017olympiad`, SOLAR-1 →
`andre2019solar1`, EMERALD → `bidard2022emerald`, INAVO120 → `jhaveri2024inavo120`,
postMONARCH → `kalinsky2024postmonarch`, MONARCH-2 → `sledge2017monarch2`,
TROPiCS-02 → `rugo2023tropics02`, DESTINY-Breast04 → `modi2022destinyb04`,
MONALEESA-2/3/7, MONARCH-3, BOLERO-2, PALOMA-3, ESCAT, TRIPOD, NetworkX,
PRISMA, GRADE, Cochrane, OpenAlex, ClinicalTrials.gov-API). The v1 round 4
editor closed the missing-citation defect on this basis.

In `main_v2.tex`, only **three** `\citep{}` calls remain:

```
Line 74: \citep{cardosoESMO2024,gradishar2023nccn,giordano2022asco}
Line 76: \citep{cardosoESMO2024,giordano2022asco,gradishar2023nccn}
Line 76: \citep{turner2023evidence,bardia2024hergap}
```

In `discussion_v2.tex`, **zero** `\citep{}` calls.

That means PALOMA-2, OlympiAD, SOLAR-1, EMERALD, INAVO120, postMONARCH (all
named at Methods §2.2 line 88 as the six v1-cited supplementary trials),
SERENA-6 (Results §3.6 line 171 evidence-free-node atlas), MONARCH-2 /
MONALEESA-3 / CAPItello-291 / DESTINY-Breast04 / DESTINY-Breast06 / TROPiCS-02 /
BOLERO-2 / MONALEESA-7 / MONARCH-3 are all named in the manuscript without
the first-mention primary citation that JCO CCI's AMA-style reference policy
requires.

At a real JCO CCI desk screen this is the single defect that most reliably
generates a "return for technical corrections": the bibliography is too short
relative to the named trial set. The fix is mechanical and low-risk because
the bib entries already exist; the author needs to thread `\citep{...}` calls
into Methods §2.2 (the six supplementary trials at line 88), Results §3.6
(SERENA-6, EMERALD), and Discussion paragraph "Where the gap is largest"
where the post-CDK4/6i trials are named.

The Vancouver / `unsrtnat` numbered-superscript style in the template is
correct for JCO CCI's AMA 11th-edition house style; no style change needed,
only the missing `\citep{}` calls.

## 5. Author block

```
\author[1,*]{H.-T.\ Lin}
\affil[1]{[Affiliation and full postal address to be supplied at submission].}
\affil[*]{Correspondence: \texttt{ppoiu87@gmail.com}. ORCID iD and full
   institutional address pending submission-time author block.}
```

Identical to v1. **Acceptable for preprint deposit only.** Blocking for the
journal submission portal: JCO CCI requires (a) ORCID iD for corresponding
author at submission, (b) institutional postal address, (c) institutional
email if the author has one. Gmail is permitted as a backup but not as the
primary corresponding-author address. Fix at the journal-submission
boundary, not the editorial-screen boundary; flagging here so that the v2
release artefact (PDF, DOCX, git tag) carries a non-placeholder block.

## 6. Figures — three of four have legibility defects

### Fig 1 (`v2_fig1_dag.pdf`) — DAG

Substantial improvement over v1 (proper state × biomarker grid, 19 source
nodes with n-counts, 25 guideline-node squares G1–G26 with G18 absent — see
defect 6.5 below). Two material defects:

- **Legend overprints data.** The legend ("Guideline decision node / Trial
  source node (size=enrolment)") sits in the upper-left of the plot area and
  overlaps the y-axis label at row `HR+/HER2-/PIK3CAmut/AKTpath` and the
  `n=1` callout for the post-CDK46i+post-endo source node. At 0.93\linewidth
  print width this is visible but messy; on a printed page it will be read as
  a sloppy figure.
- **Source-node count labels (`n=23`, `n=10`, `n=9` …) and guideline-node
  labels (`G1`, `G4+G15`, `G6` …) collide** at the two highest-degree columns
  (first-line and post-endo). Concretely: the `G4+G15` and `G3` labels at the
  post-endo column sit nearly on top of the `n=10` callout for the post-endo
  source node. This is the same class of defect Round 4 of the v1 cycle
  documented at §4 and partially mitigated; v2 reintroduces it because the
  guideline-node count went from 16 to 25.

### Fig 2 (`v2_fig2_forest.pdf`) — Forest plot

Clean primary signal (0.60 \*, P<0.001 at top row, threshold line at 0.25 in
red dashed). **One material defect:**

- The "Pre-registered H0 threshold (0.25)" legend label sits on the
  right-hand side of the bottom row and **overprints the NCCN-citing row's
  P=0.0197 annotation**. Either move the legend to a corner or extend the
  x-axis to 1.15.
- Minor: the `0.60 *` value annotation at the top row sits on top of the title
  ("EFDPR forest plot: primary + by-guideline sensitivity"). Nudge the title
  up by ~5% of the plot height or the annotation down by the marker radius.

### Fig 3 (`v2_fig3_odi.pdf`) — ODI bar chart

Substantive content is correct. **Two defects:**

- **Axis-label typo.** The top bar is labelled `prior CDK4 6i` (with a space
  where the slash should be). The Methods, Results, Discussion, Table 3
  caption, and abstract all spell this `prior-CDK4/6i`. The figure caption
  in `main_v2.tex` line 159 also says "prior-CDK4/6i". This is the kind of
  typo a reviewer screenshots into their review.
- **Value labels overprint error-bar caps** for the top three bars
  (`0.64 (n=80 trials, 3160 pairs)`, `0.38 (n=9 trials, 36 pairs)`, `0.27
  (n=5 trials, 10 pairs)`). Move labels above the bars or extend the x-axis
  to 1.15.

### Fig 4 (`v2_fig4_heatmap.pdf`) — Per-node support heatmap

Clean and informative. **One minor defect:**

- The figure is portrait-tall (25 rows × 3 columns) but is included at
  `\includegraphics[width=0.66\linewidth]` (line 175). On the printed page
  this gives a very narrow heatmap with lots of horizontal whitespace. Either
  rotate the figure (rows on x-axis, tolerance levels colour-coded as a
  3-series small-multiple) or reduce the include width to ~0.45\linewidth and
  let it sit flush left.
- Substantive: G18 is missing from the G1…G26 sequence (G17 → G19 visible on
  the y-axis). The manuscript text claims 25 unified nodes; the heatmap also
  shows 25 rows but with a G18 skip. Either the encoding renumbers around a
  deprecated node (in which case **document the skip in the figure caption
  and the table**) or there is an off-by-one that needs reconciling against
  `v2_tab_efdpr.tex`. Either way, the next round needs an explicit sentence
  in the methods or caption: "Node G18 was removed during deduplication; the
  numbering is preserved for traceability against the pre-registered
  encoding."

## 7. Article type

**Original Report remains correct.** v2 now meets every JCO CCI Original
Report criterion: hypothesis-driven, pre-registered primary outcome, primary
data (structured trial-eligibility extractions), structured abstract,
reproducible pipeline, key-objective / knowledge-generated / relevance
precis block. The earlier v1 ambivalence ("methods article or research
letter, at editor's discretion" — cover letter line 12) is no longer
warranted and should be dropped from the v2 cover letter.

---

## Concrete asks (10)

1. **Rewrite `docs/cover_letter.md` for v2.** New title verbatim from
   `main_v2.tex` line 34–36. New framing paragraph: 25-node unified
   ESMO+ASCO+NCCN tree against 64 in-scope trials of an 80-trial corpus,
   pre-registered exact binomial test rejects $H_0$ at P=0.0002, three
   pre-specified by-source sensitivities (ESMO P=0.027, NCCN P=0.020, ASCO
   P=0.057 marginal), ODI 0.64 for prior-CDK4/6i. Drop "pilot",
   "methodology submission", and the "did not reject" sentence. Commit to
   the Original Report article type.

2. **Thread `\citep{}` calls into `main_v2.tex` and `discussion_v2.tex`** at
   first mention of each named trial. Minimum set, with existing bib keys:
   - Methods §2.2 line 88 (PALOMA-2 → `finn2016paloma2`, OlympiAD →
     `robson2017olympiad`, SOLAR-1 → `andre2019solar1`, EMERALD →
     `bidard2022emerald`, INAVO120 → `jhaveri2024inavo120`, postMONARCH →
     `kalinsky2024postmonarch`).
   - Results §3.6 line 171 (EMERALD subgroup → `bidard2022emerald`; SERENA-6
     subgroup — note: no `serena6` bib entry exists yet, add one).
   - Discussion "Where the gap is largest" (post-CDK4/6i trials referenced
     by class need at least one representative citation each:
     `sledge2017monarch2` for fulvestrant post-endo, `turner2023evidence`
     for capivasertib, `andre2019solar1` for alpelisib).
   - Discussion "Operationalization discordance" (ESR1 mutation definitions —
     cite `bidard2022emerald` again here).
   Target the bibliography to land at ≥25 entries.

3. **Add a SERENA-6 bib entry** to `references.bib` if the trial is to remain
   named in Results §3.6 line 171. If the entry cannot be added (no primary
   publication yet), recast the sentence to "an ongoing ESR1mut early-switch
   trial" and drop the named callout.

4. **Fix Fig 1 legend placement.** Move the legend to outside the plot area
   (e.g., `bbox_to_anchor=(1.02, 1)` to the right margin, or below the x-axis
   with `loc='lower center', bbox_to_anchor=(0.5, -0.20), ncol=2`). Re-render
   at 300 dpi. Verify at 0.93\linewidth print size that no `n=k` callout or
   `G#` label is overprinted.

5. **Fix Fig 2 right-margin overlap.** Either move the "Pre-registered H0
   threshold (0.25)" legend label to a corner via `loc='upper right'` /
   `loc='lower right'` outside the data range, or extend the x-axis to
   `[0.0, 1.15]` so the legend and the NCCN-citing P-value annotation no
   longer collide. Also nudge the `0.60 *` top-row annotation off the title.

6. **Fix Fig 3 axis-label typo.** Change `prior CDK4 6i` to `prior-CDK4/6i`
   in `analysis/v2_*_fig3*.py` (or the corresponding plot script). Move the
   value+(n, pairs) annotations off the error-bar caps — either above each
   bar or to the right of the plotted error bar by extending the x-axis to
   1.15.

7. **Fix Fig 4 aspect and the G18 skip.** Either (a) include at
   `\includegraphics[width=0.45\linewidth]` flush-left with a paragraph of
   wrap text, or (b) rotate to 3 rows × 25 columns landscape. **Independently,
   document in the figure caption** why the y-axis sequence is G1…G17,
   G19…G26 (25 nodes, G18 absent) — either as a deprecated-during-
   deduplication node (preferred) or by renumbering to G1…G25 contiguous.
   Whichever path is chosen, `v2_tab_efdpr.tex`, the heatmap, and the atlas
   paragraph (Results §3.6 line 171) need to agree.

8. **Replace placeholder author block at submission boundary.** ORCID iD,
   institutional postal address, institutional email. Acceptable to defer to
   the journal-portal submission step but flag in the v2.0.0 release tag's
   README that the placeholder is intentional and what fields are missing.

9. **Confirm power-claim consistency.** Methods §2.8 line 106 says "23% at
   $p_1=0.35$, 42% at $p_1=0.40$, 82% at $p_1=0.50$"; Discussion paragraph
   "Three caveats" says "~42% at $p_1 = 0.40$, ~82% at $p_1 = 0.50$".
   Consistent — but add a one-line statement that the observed point
   estimate (0.60) sits above the 0.50 powered-for level, so the rejecting
   P=0.0002 is consistent with the pre-registered power table rather than a
   surprise.

10. **Add a one-sentence v1→v2 traceability note** to the Methods (or as a
    footnote on the first page). Concretely: "The v1.0.0 pilot (16 nodes,
    ESMO-only, 16-trial corpus; P=0.37, did not reject) is preserved at git
    tag `v1.0.0`; v2 supersedes v1 with a systematic search, ASCO+NCCN
    extension to 25 nodes, and an expanded 80-trial / 64-in-scope corpus."
    This is half-stated in the Limitations paragraph of `discussion_v2.tex`
    line 22 but a methods-section sentence makes the relationship explicit
    and prevents a reviewer from worrying about post-hoc corpus expansion.

---

## VERDICT: MINOR

The science is solid, the pre-registration trail is auditable, word counts
are compliant with headroom, and the three pre-specified sensitivity
analyses are reported faithfully including the marginal ASCO result. None
of the ten asks above requires re-analysis or re-running the pipeline.
Asks 1, 2, 4, 5, 6, 7 are the load-bearing technical corrections; asks 3,
8, 9, 10 are polish. The fix-pack should land in a single revision round
and clear the v2 round-2 editor screen for out-for-review.
