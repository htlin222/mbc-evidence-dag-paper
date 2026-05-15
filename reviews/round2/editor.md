# JCO Clinical Cancer Informatics — Editor Review, Round 2

**Manuscript:** *A Computable Map of Treatment-Sequencing Evidence in HR+/HER2-
Metastatic Breast Cancer: Graph-Theoretic Discordance Between Trial Chains and
Guideline Pathways*
**Author:** H.-T. Lin (single author)
**Article type as submitted:** Original Report
**Reviewer role:** Decision Editor, JCO CCI
**Date:** 2026-05-16

---

## Summary of Round 1 follow-through

| Round 1 ask | Status in Round 2 |
|---|---|
| Abstract over the 300-word cap | **Not fixed** — abstract is still 347 words |
| Reference deduplication | Done (taking author's word; not re-audited this round) |
| ESMO 2024 BibTeX year correction | Done |
| Author block incomplete | **Not fixed** — still "Affiliation to be confirmed by author"; no ORCID; no postal address |
| Supplementary Table S1 (reporting checklist) | Materialised (Supplement §S1) |
| LLM extraction honestly described | Done (Methods 2.2 now says pilot is hand-curated; LLM is a companion paper) |
| Cover letter | **Not written** |

Two Round 1 asks (abstract length, author block) are still open. A new
high-severity issue (Figure 1 quality and a figure-vs-text trial-count
inconsistency) is identified below.

---

## 1. Word-count audit

Tokens were counted on the LaTeX sources with citations, math, figures, and
tables stripped (script reproducible from `manuscript/main.tex` and
`manuscript/discussion.tex`).

| Section | Target (JCO CCI) | Actual | Status |
|---|---|---|---|
| Abstract | ≤ 300 | **347** | **Over by 47 words (16%)** |
| Key Objective + Knowledge Generated + Relevance | ≤ 120 | **129** | **Over by 9 words** |
| Main text (Intro + Methods + Results + Discussion) | ≤ 3,000 | **2,455** | Under by 545 (compliant) |
| &nbsp;&nbsp;Intro | — | 331 | — |
| &nbsp;&nbsp;Methods | — | 656 | — |
| &nbsp;&nbsp;Results | — | 597 | — |
| &nbsp;&nbsp;Discussion | — | 871 | — |

**Where to trim the abstract (target: −47 words, ideally −55 to leave headroom):**

- **Results paragraph** is the worst offender. Currently it states the strict
  CI twice (Clopper-Pearson *and* bootstrap), names every evidence-free node
  inline, *and* gives both ODI numbers. Drop the bootstrap CI from the abstract
  (keep Clopper-Pearson as primary, as already chosen in Methods 2.7), move the
  per-node list to the body, and keep one ODI value (prior-CDK4/6i 0.91). This
  saves ~30 words.
- **Methods paragraph**: "and one PARP-inhibitor trial for the gBRCAm node"
  and "spanning primary-completion years 2014--2024" can be cut; the schema
  version detail (v1.0) belongs in the body. Saves ~15 words.
- **Conclusion paragraph** is the second-worst offender. The sentence
  "substantial composition-across-non-overlapping-trials in post-CDK4/6i
  biomarker-stratified positions" is dense and can be tightened. Saves ~15 words.

**Where to trim the KO/KG/R block (target: −9 to −12 words):**

- "with a reproducible computational pipeline" in KO is redundant with the
  Knowledge Generated paragraph that follows. Cut it.
- Knowledge Generated currently re-states both the CI and the p-value; pick
  one (the p-value is the headline) and drop the parenthetical.

---

## 2. Title

The current title is two clauses joined by a colon, 23 words long, and is
**acceptable but not optimal** for JCO CCI. Concerns:

- "Graph-Theoretic Discordance Between Trial Chains and Guideline Pathways"
  is methods-forward and may read as a methods paper to the screening editor.
- The result the paper actually delivers is *descriptive* (a non-rejecting
  pilot), so the title's strong "Discordance" framing overpromises against a
  P = 0.37 finding (see §4 below).
- JCO CCI house style favours titles that name the clinical artefact and the
  computational contribution in one phrase.

**Recommended title (one of):**
1. *A Computable Map of Treatment-Sequencing Evidence in HR+/HER2- Metastatic
   Breast Cancer: A Pre-Registered 16-Trial Pilot of an Evidence-Free
   Decision-Point Ratio.*
2. *Locating Evidence-Free Decision Points in the HR+/HER2- Metastatic Breast
   Cancer Guideline Tree: A Reproducible Graph-Theoretic Pilot.*

Either de-emphasises "discordance" (a claim the test did not support) and
foregrounds the framework + pilot scope (a claim the data do support).

---

## 3. Article type

**Recommendation: re-pitch as a Research Letter (≤ ~1,500 words) or as a
Methods Article.** Original Report is the wrong slot for this manuscript as
currently written.

Rationale:

- The pre-registered primary test failed to reject (P = 0.37, all tolerances).
  Original Report at JCO CCI is the slot for confirmatory, hypothesis-driven
  primary-data work. A pilot with a non-rejecting primary endpoint, framed
  honestly, is a poor fit for that slot — and the abstract's "Conclusion" already
  concedes the result is "best interpreted as descriptive evidence".
- The contributions are (i) a framework, (ii) a frozen schema and decision-tree
  encoding, (iii) a pilot estimate. (i) and (ii) are methods deliverables.
- Two viable paths:
  - **Research Letter** (≤ ~1,500 main-text words, ≤ 2 display items): emphasise
    the descriptive finding ("five post-CDK4/6i biomarker nodes are supported
    only by composition across non-overlapping trials") and release the
    framework as supplementary. This will require cutting Methods by ~70% and
    Results by ~40%.
  - **Methods Article**: keep the current methods depth, frame the contribution
    as the EFDPR/ODI framework with the 16-trial corpus as a worked example;
    the failed test becomes a feature ("the pilot's sample size is the
    bottleneck"), not a bug.

My preference: **Methods Article**. It absorbs the entire pre-registration
honestly, keeps Supplementary Table S1 useful (a methods checklist is on-charter
for a methods paper), and frees the author from having to justify a
non-rejecting confirmatory test.

If the author insists on Original Report, the abstract Conclusion and the
Discussion headline must be rewritten so that the descriptive framing is the
*primary* finding (see §4) and the EFDPR point estimate is the secondary
descriptor; submitting as currently framed will not pass the editorial screen.

---

## 4. Result framing — recasting the headline

A non-rejecting pre-registered test is hard to sell. The good news is that the
*locations* of the five evidence-free nodes are clinically interesting in their
own right (every post-CDK4/6i biomarker branch except gBRCAm). Re-cast the
headline around the *map*, not the test.

**Two alternative headline sentences for the abstract Conclusion and the
Discussion opener:**

1. *"In this pre-registered 16-trial pilot, five of the six post-CDK4/6i
   biomarker-stratified decision nodes in the ESMO HR+/HER2- mBC tree
   (ESR1mut, AKT-pathway, PIK3CAmut, no-actionable-mutation, and the
   post-CDK4/6i+post-endo everolimus node) were supported only by trials whose
   enrolment state did not match the guideline-recommended state; the pilot
   was under-powered for a confirmatory test, and the framework, schema, and
   decision-tree encoding are released for a systematic-review-scale extension."*

2. *"A graph-theoretic audit of the ESMO HR+/HER2- mBC guideline tree
   identifies the post-CDK4/6i biomarker branch as the highest-yield target
   for new pivotal-trial enrolment: five of six decision nodes in that branch
   are supported only by composition across non-overlapping trials, and the
   prior-CDK4/6i inclusion definition is the most operationally heterogeneous
   variable across the corpus (ODI 0.91, n = 7 trials)."*

Both lead with the actionable map; both report the underpowered test honestly
in the second clause; both keep the ODI finding (which *is* a measurement, not
a hypothesis test) in view.

---

## 5. Author block — still incomplete

The current block reads:

> H.-T. Lin¹·\*
> ¹Affiliation to be confirmed by author.
> \*Correspondence: ppoiu87@gmail.com.

**This will not pass the JCO CCI submission portal.** Required before
submission:

- [ ] **Full given name** as it should appear in PubMed (e.g. *Hsing-Ting Lin*,
  not *H.-T. Lin*). PubMed indexing depends on this.
- [ ] **ORCID iD** for the corresponding author (JCO CCI policy: required, not
  optional). If the author does not have one, register at orcid.org before
  submission.
- [ ] **Institutional affiliation** at the time the work was performed. If the
  work was conducted without an institutional affiliation, declare
  "Independent Researcher, *city, country*" — this is acceptable to ASCO but
  must be stated explicitly; "to be confirmed" is not.
- [ ] **Corresponding-author full address**: street, city, postcode,
  country, telephone, and an institutional email if one exists (a
  Gmail address as the sole corresponding email is permitted but is a
  yellow flag for the editorial office; supply both if available).
- [ ] **CRediT statement** is already correct.
- [ ] **Conflict-of-interest disclosure** is already declared as "none" — keep,
  and ensure the ASCO conflict-of-interest form is uploaded at submission.

---

## 6. Cover letter — 3-sentence draft

For `docs/cover_letter.md`. Editorial-screen-passable:

> Dear Editors,
>
> We submit *A Computable Map of Treatment-Sequencing Evidence in HR+/HER2-
> Metastatic Breast Cancer* as a Methods Article for JCO Clinical Cancer
> Informatics: the paper introduces an open-source graph-theoretic framework
> (EFDPR + ODI) that places pivotal-trial corpora and guideline decision trees
> on a single canonical node space, and applies it in a pre-registered 16-trial
> pilot that localises five evidence-free decision points in the ESMO 2024
> HR+/HER2- mBC tree — all of them in the post-CDK4/6i biomarker branch. The
> framework, frozen JSON schema, decision-tree encoding, and analysis code
> are released under MIT licence with a tagged-release Zenodo DOI, and the
> work is not under consideration elsewhere and has not been previously
> published. We believe the manuscript fits JCO CCI's mandate for reproducible,
> clinically-actionable computational oncology, and we suggest the reviewers
> listed below; none has a conflict of interest with the author.
>
> Sincerely,
> Hsing-Ting Lin (corresponding author)

(If the article-type recommendation in §3 is rejected and the author retains
"Original Report", change "Methods Article" to "Original Report" in sentence
one — but see §3 for why this is dispreferred.)

---

## 7. Suggested reviewers (3)

The author must verify current affiliations and emails at submission; the
names below are real, active investigators in evidence-synthesis / clinical
guidelines / mBC trial methodology and are not co-authors or recent
collaborators of any institution declared in §5 (because no institution is
declared).

1. **Dr. Fabrice André** (Gustave Roussy, Villejuif, FR) — senior author on
   SOLAR-1 and the ESMO Precision Medicine Working Group; the natural
   methodologist for biomarker-trial-to-guideline mapping in HR+/HER2- mBC.
   *Conflict-of-interest disclosure:* none known with the author; Dr. André
   is a SOLAR-1 author, and SOLAR-1 is one of the 16 trials in the corpus, so
   the editor should treat his review as substantive on framework but recused
   on the SOLAR-1 / G7 specific finding.

2. **Dr. Nicola Latino** or **Dr. Giuseppe Curigliano** (ESMO Guidelines
   Committee, mBC chapter): direct conflict on the *target* of the audit
   (ESMO 2024) but precisely the right expertise on whether the decision-tree
   encoding is faithful.
   *Conflict-of-interest disclosure:* both are co-authors of the ESMO 2024 mBC
   update that the paper audits; flag this to the EIC and let the EIC decide
   whether to include one as a "methodology-on-encoding-only" reviewer or to
   substitute.

3. **Dr. Lisa Bero** (University of Colorado Anschutz; formerly Cochrane
   Methods Innovation Fund Chair) — methodologist on evidence synthesis,
   guideline trustworthiness, and computational meta-research; *not* an mBC
   clinician, which is desirable for a reviewer who must judge the
   graph-theoretic framework on its merits.
   *Conflict-of-interest disclosure:* none known with the author; no
   institutional or trial-corpus conflict.

The author should also list **one non-preferred reviewer** if any (the JCO CCI
portal accepts up to two); none is mandated.

---

## 8. Reproducibility deliverable — Zenodo DOI

> "Persistent code DOI via Zenodo to be minted at release."
> (`main.tex` line 184)

**Not acceptable for submission.** JCO CCI's reproducibility expectation is a
*resolvable* persistent identifier at the time the reviewers see the paper, not
at acceptance. The required workflow:

1. Tag `v1.0.0-submission` (or equivalent) **before submission**.
2. Push the tag to GitHub with the Zenodo–GitHub webhook enabled so Zenodo
   mints a DOI automatically.
3. Replace the line above with the resolved DOI (e.g. `10.5281/zenodo.XXXXXXX`)
   and include the matching DOI badge in the README.
4. If the author plans a post-review `v1.0.0` (final) tag, mint a *second*
   DOI at that point and note in the Code Availability statement that the
   submission-time DOI is the snapshot reviewers saw.

This is a hard ask: an unresolved DOI placeholder will fail the editorial
screen at JCO CCI.

---

## 9. Figure quality

Figures 2 and 3 are publication-quality: clean bar geometry, error bars
labelled, axes legible, the pre-registered threshold marked. Approve as-is.

**Figure 1 is not publication-ready. It is the most serious new issue in
Round 2 and must be remade before submission.** Concrete defects visible in
`figures/fig1_dag.pdf`:

- **Title-vs-text inconsistency.** The figure title reads "HR+/HER2- mBC
  pivotal-trial DAG (**N = 14 trials**)" but Results §3.1 and the abstract
  say **N = 16** (15 HR+/HER2- + 1 OlympiAD). MONALEESA-7, MONARCH-2, or
  PALOMA-3 are silently dropped in the figure renderer. This single
  discrepancy is enough to block acceptance — a reviewer will spot it
  immediately.
- **Truncated edge labels.** "MONALEESA", "CAPItello", "DESTINY-B",
  "postMONAR", "TROPiCS-0" are all cut off. Either rotate edge labels, use a
  trial-ID legend, or widen the canvas.
- **Empty grey target nodes.** Every trial edge terminates in an unlabelled
  grey circle. The caption says nodes encode (prior-state, biomarker) tuples,
  but the *target* nodes (post-trial state) carry no labels at all — the
  reader cannot tell what state each trial transitions to.
- **Layout is broken.** The graph appears to be rendered with a random/spring
  layout that scatters disconnected components across the canvas with large
  empty whitespace bands; this is not the topology-revealing layout the
  Results text leads the reader to expect.
- **No legend** for "Node colour: distance from first-line treatment-naive
  state" (the caption claims one) — nodes appear in a single shade of blue.
- **No edge-thickness legend** for enrolment count (the caption claims one) —
  edges are uniform width.

**Required fix:** regenerate Figure 1 with (i) all 16 trial edges, (ii)
labelled source *and* target nodes, (iii) a fixed hierarchical layout
(left-to-right by line-of-therapy, top-to-bottom by biomarker), (iv) a
visible node-colour legend that matches the caption, (v) an edge-width legend
that matches the caption, and (vi) the correct trial count in the title.
Graphviz `dot` or `networkx` + `pygraphviz` with a `dot` layout engine will
produce this; the current matplotlib spring layout will not.

---

## Concrete asks for the next round

1. Cut the abstract to ≤ 300 words (current: 347). Suggested cuts in §1.
2. Cut the Key Objective / Knowledge Generated / Relevance block to ≤ 120
   words (current: 129).
3. Complete the author block: full name, ORCID iD, declared affiliation
   (or "Independent Researcher, *city, country*"), full postal address (§5).
4. Switch article type to **Methods Article** (preferred) or rewrite the
   abstract Conclusion and Discussion headline to lead with the descriptive
   framing under "Original Report" (§3).
5. Adopt one of the two recasted headlines in §4 for both the abstract
   Conclusion and the first sentence of the Discussion. The current "the
   point estimate modestly exceeded ... but the test did not reject" framing
   is honest but soft; lead with the map, not the failed test.
6. Consider re-titling per §2; at minimum, weaken "Discordance" given the
   P = 0.37 result.
7. Write the cover letter (§6 draft above) and commit to
   `docs/cover_letter.md`.
8. List three suggested reviewers in the submission portal; verify the
   conflict-of-interest disclosures in §7.
9. Mint the Zenodo DOI *before* submission and replace the placeholder in
   the Code Availability statement (§8).
10. Regenerate Figure 1 with the six defects in §9 fixed. The N = 14 / N = 16
    inconsistency alone is blocking.
11. Once Figure 1 is regenerated, re-verify that the abstract's "16 pivotal
    phase 2/3 trials ... and one PARP-inhibitor trial" wording and Table 1
    counts match the figure.
12. Add an ORCID iD to the cover-letter signature (§6) once registered.

---

## Verdict

**MAJOR REVISION.**

Two Round 1 asks are still open (abstract length, author block), and Round 2
introduces three new blocking issues that cannot be hand-waved past an
editorial screen:

- **Figure 1** is unusable in its current state, and contradicts the main-text
  trial count.
- **Zenodo DOI** is unminted; the placeholder will not pass the editorial
  reproducibility screen.
- **Article-type framing** is misaligned with a P = 0.37 primary test.

None of these is fatal — all are addressable in one revision cycle — but the
manuscript as it stands today would be returned at first-pass screening by
the JCO CCI editorial office, before it reached external review. The science
and the reproducibility infrastructure are strong; the submission packaging is
not yet ready.

I would re-review a revised version that addresses asks 1–12 above.
