# JCO Clinical Cancer Informatics — Editor Review, Round 3

**Manuscript:** *A Computable Map of Treatment-Sequencing Evidence in HR+/HER2-
Metastatic Breast Cancer: Graph-Theoretic Discordance Between Trial Chains and
Guideline Pathways*
**Author:** H.-T. Lin (single author)
**Article type as submitted:** Original Report
**Reviewer role:** Bar-raising / editorial-screen simulation, JCO CCI
**Date:** 2026-05-16

---

## Framing for this round

The question I am answering this round is simple: **if this manuscript arrived
on the JCO CCI editor's desk tomorrow, would it pass the first-pass editorial
screen?** Not "is the science sound" (it is), and not "would peer reviewers
recommend acceptance" (they might). Editorial screen is a different gate: it
asks whether the packaging is complete, the metadata is submittable, and the
framing is honest. A paper that fails screen is returned without review.

Two Round 1 asks and three Round 2 asks remain open. Several are now resolved.
The verdict at the bottom is calibrated to "would this clear screen today?",
not "is this a good paper?" — those are different questions.

---

## 1. Word-count audit (verified by running `analysis/wordcount.py`)

```
$ uv run python analysis/wordcount.py
      Abstract:  230 words
        KO box:  106 words
  Introduction:  339 words
       Methods:  700 words
       Results:  597 words
    Discussion:  795 words
```

| Section | Target (JCO CCI) | Actual | Status |
|---|---|---|---|
| Abstract | ≤ 300 | **230** | Compliant (70-word headroom) |
| Key Objective + Knowledge Generated + Relevance | ≤ 120 | **106** | Compliant (14-word headroom) |
| Main text (Intro + Methods + Results + Discussion) | ≤ 3,000 | **2,431** | Compliant (569-word headroom) |
| &nbsp;&nbsp;Intro | — | 339 | — |
| &nbsp;&nbsp;Methods | — | 700 | — |
| &nbsp;&nbsp;Results | — | 597 | — |
| &nbsp;&nbsp;Discussion | — | 795 | — |

**Word count is in compliance and was the most-resolved Round 2 ask.** The
abstract was cut from 347 → 230 (−117 words, well past the −47 ask) and the
KO block from 129 → 106. Both have comfortable headroom for any reviewer-driven
additions in a future round. Pass.

---

## 2. Reference list

The references resolve to **6 unique entries in the printed bibliography**
(`main.bbl`):

1. Gennari 2024 (ESMO 2024)
2. Gradishar 2024 (NCCN v3.2024)
3. Giordano 2022 (ASCO mBC)
4. Turner 2023 (CAPItello-291)
5. Bardia 2024 (DESTINY-Breast06)
6. Niranjan 2020 (subgroup representation)

They appear in the order they are cited and are rendered in Vancouver / AMA-ish
style (`bibliographystyle{vancouver}`, line 204 of `main.tex`), which is
acceptable for JCO CCI with a copyedit pass at acceptance.

**The problem is not the bibliography — it is the citation density in the body
text.** Only **three `\citep{}` invocations exist in the entire manuscript**
(`main.tex` lines 77, 79, 175) and **zero in `discussion.tex`**. Twenty-one
trial-level primary publications are sitting in `references.bib` (PALOMA-2/3,
MONALEESA-2/3/7, MONARCH-2/3, postMONARCH, SOLAR-1, INAVO120, EMERALD,
TROPiCS-02, OlympiAD, DESTINY-Breast04, BOLERO-2, ESCAT, TRIPOD, PRISMA, GRADE,
Cochrane, NMA, ClinicalTrials.gov API, OpenAlex, NetworkX) and never cited.

In Results §3.3 the manuscript names ten trials by acronym (EMERALD,
postMONARCH, CAPItello-291, PALOMA-3, MONARCH-2, INAVO120, SOLAR-1,
DESTINY-Breast04, DESTINY-Breast06, plus the operational-token-vocabulary
trials in Methods); none of these acronyms carry a primary-publication
citation. A JCO CCI clinical reviewer reading "EMERALD, postMONARCH" will
expect `[12,13]` after each acronym and will mark "trial citations missing" on
the screening sheet. This is the single most likely first-pass screening flag
on the current draft.

**Action:** add primary-publication citations the first time each named trial
appears, in both Results §3.3 and Methods §2.3. The references already exist in
`references.bib`; this is a one-pass `\citep{}` insertion exercise, not new
literature work. Expected post-fix reference count: 18–22 unique entries,
still well under the 50 cap.

---

## 3. Author block — still a placeholder

Current state (`main.tex` lines 41–43):

```
\author[1,*]{H.-T.\ Lin}
\affil[1]{[Affiliation and full postal address to be supplied at submission].}
\affil[*]{Correspondence: \texttt{ppoiu87@gmail.com}. ORCID iD and full
   institutional address are placeholders pending the submission-time author
   block.}
```

**For a preprint (medRxiv / bioRxiv / arXiv) deposit:** this is acceptable.
medRxiv accepts "Independent Researcher" with a Gmail corresponding-author
address, and an ORCID iD is encouraged but not enforced at deposit. So the
manuscript as written is **preprint-ready** in this respect.

**For a JCO CCI submission portal:** this is **not acceptable**. The ASCO
submission system enforces (i) a full given name, (ii) an institutional
affiliation field that does not accept "[to be confirmed]" as a value,
(iii) ORCID iD for the corresponding author (policy, not soft requirement).
The author can declare *"Independent Researcher, [city, country]"* — that is
permitted by ASCO — but the literal string "[Affiliation and full postal
address to be supplied at submission]" will be rejected at intake screening.

**Action (preprint path):** leave as-is and deposit. Note in `JOURNAL.md` that
the journal submission requires the author block to be completed *before*
journal submission, with concrete language ("Independent Researcher, [city],
[country]") rather than a bracketed placeholder.

**Action (journal path):** complete the author block before submission. The
asks are unchanged from Round 1 (item 10) and Round 2 (§5).

---

## 4. Cover letter (`docs/cover_letter.md`)

A cover letter now exists (it did not in Round 2). It is structurally
correct: it identifies the article type, names the contribution, declares
non-overlap, declares conflicts, declares preprint intent, and offers three
reviewer slots. The novelty sentence and the article-fit sentence are both
present.

**The blocker is the placeholders.** The current letter contains:

- `[Date placeholder]`
- `Dr. [Editor name placeholder]` (×2)
- `[Reviewer 1], [Reviewer 2], [Reviewer 3]`
- `[Affiliation to be supplied]`
- "(or, at the editor's discretion, as a Methods Article or Research Letter)"
  — JCO CCI does not accept article-type optionality; one type must be
  chosen.

The letter is **not submission-ready**. It is, however, **70% of the way
there**, and the remaining 30% is data entry, not writing. Three concrete
fixes:

(a) Resolve all five bracketed placeholders (date, editor name, three
reviewers, affiliation).
(b) Drop the "or, at the editor's discretion" hedge — commit to either Original
Report or Methods Article (see §6 below).
(c) Add the ORCID iD line to the signature block; the cover letter is where the
editorial office expects it.

---

## 5. Title

Current title:
> *A Computable Map of Treatment-Sequencing Evidence in HR+/HER2- Metastatic
> Breast Cancer: Graph-Theoretic Discordance Between Trial Chains and
> Guideline Pathways*

The Round 2 review asked the author to weaken "Discordance" given the
P = 0.37 non-rejection. **The title is unchanged.** The word "Discordance"
still sits in the headline phrase position. For a non-rejecting pre-registered
test, a JCO CCI screening editor will read "Discordance" as
over-claiming.

The first clause (*A Computable Map of Treatment-Sequencing Evidence in
HR+/HER2- Metastatic Breast Cancer*) is clinical-finding-friendly and works.
The second clause is the methods-paper framing; drop or soften it.

**Suggested replacement (one of):**

1. *A Computable Map of Treatment-Sequencing Evidence in HR+/HER2- Metastatic
   Breast Cancer: A Pre-Registered 16-Trial Pilot of an Evidence-Free
   Decision-Point Ratio.*
2. *A Computable Map of Treatment-Sequencing Evidence in HR+/HER2- Metastatic
   Breast Cancer: A Graph-Theoretic Pilot of Trial-to-Guideline Concordance.*

Either replaces "Discordance" with framework language (a "ratio" or a
"pilot"); the manuscript's empirical claim is now appropriately humble and the
title should match.

---

## 6. Article-type recommendation

This is the most consequential open call. Round 2 strongly recommended
**Methods Article**, with **Research Letter** as a fallback. The manuscript
is still submitted as **Original Report** (`main.tex` line 1 comment;
`JOURNAL.md` line 11). The cover letter hedges between three types.

Three reasons the Methods Article re-pitch is now even more defensible than it
was in Round 2:

1. **The discussion now leads with the descriptive framing.** Round 2 asked
   for this; Round 2.x delivered it. The headline sentence of
   `discussion.tex` reads "the framework's primary contribution from this
   pilot is therefore a quantitative description …", which is the Methods
   Article frame, not the Original Report frame.
2. **The abstract Conclusion now reads "the result is best read as descriptive
   evidence … with confirmatory testing deferred to a systematic-review-scale
   extension."** This is, verbatim, the abstract Conclusion of a Methods
   Article, not of an Original Report.
3. **The Supplementary Table S1 is now a PRISMA-2020 reporting checklist with
   a graph-construction addendum.** PRISMA reporting is on-charter for a
   methods/evidence-synthesis paper. For an Original Report, the more usual
   companion checklist is CONSORT-style or STROBE-style; PRISMA is the methods
   tell.

Every artefact the paper actually delivers — pilot framing, humble Conclusion,
methods-style reporting checklist — points to Methods Article. The only
remaining attachment to Original Report is the type label on the cover letter
and `JOURNAL.md`. Two-line fix.

**Action:** change to **Methods Article** in the cover letter and in
`JOURNAL.md`. State the chosen type once in the cover letter without
optionality. This will reduce screening-editor friction.

---

## 7. Headline framing — Results §3.2

The Results §3.2 headline sentence now reads:

> *"Under strict concordance the EFDPR was 0.31 (5/16 decision nodes
> evidence-free; Clopper-Pearson 95\% CI 0.11--0.59) ... The point estimate
> exceeded the pre-registered 0.25 threshold under strict and ESCAT tolerance,
> but the pre-registered one-sided exact-binomial test of $H_0: \mathrm{EFDPR}
> \le 0.25$ did not reject under any tolerance level (strict $P = 0.37$;
> ESCAT $P = 0.37$; liberal $P = 0.60$ ... ). **The headline finding from
> this pilot is therefore a quantitative description of evidence sparsity at
> five clinically consequential decision points rather than a confirmatory
> rejection of the null.**"*

This is the right framing. The boldfaced sentence is what Round 2 §4 asked
for, and it is now the load-bearing sentence in §3.2. **Pass.**

The Discussion opener mirrors it. **Pass.**

The remaining miscalibration is at the title level (§5 above); fix that and
the framing is internally consistent end-to-end.

---

## 8. Figure 1 — still not publication-grade

I pulled `figures/fig1_dag.pdf` and inspected it. Of the six Round 2 defects:

| Defect | Round 2 | Round 3 |
|---|---|---|
| Trial count in title (N=14 vs body N=16) | "N = 14" | **Fixed: now "N=16 trials"** |
| Truncated edge labels | broken | **Still broken** (visible: "MONALEESA", "CAPItello", "DESTINY-B", "postMONAR", "TROPiCS-0") |
| Empty grey target nodes | unlabelled | **Still unlabelled** (every edge ends in a blank grey circle) |
| Layout (random/spring vs hierarchical) | spring layout, broken | **Still appears spring-layout-like** with disconnected components scattered across canvas with large empty whitespace |
| Node-colour legend | missing | **Still missing** (all source nodes appear single-colour blue) |
| Edge-width-by-enrolment legend | missing | **Still missing** (all edges appear uniform width) |

One of six defects is fixed (the N=14/16 inconsistency, which was the most
blocking single defect). Five remain. **Figure 1 is still not publication-grade
for JCO CCI's print column.** A reviewer who pulls the PDF on a laptop screen
at 100% zoom cannot read the right-edge edge labels and cannot identify what
node any of the trials transitions to.

This is the second most likely first-pass screening flag on the current draft,
after item §2 (missing trial citations).

**Action (minimum viable):** regenerate Figure 1 with (i) full trial labels
not truncated, (ii) labelled target nodes (the post-trial-state node), (iii)
a `dot`-layout (left-to-right by line-of-therapy), (iv) a visible
node-colour legend, (v) edge-width variation matched to enrolment. The caption
on line 123 of `main.tex` already claims (iv) and (v); the figure renderer needs
to match the caption.

---

## 9. Pre-registration — GitHub-only is still fragile

The Preregistration statement (`main.tex` lines 186–187) reads:

> *"Primary and secondary outcomes were pre-registered in
> \texttt{docs/prereg.md} prior to any outcome-touching analysis. The
> pre-registration commit hash is recorded in the repository's first commit."*

Round 1 (item 13) flagged this as fragile because Git history is technically
rewriteable, even though in practice the commit hash anchors the timestamp
robustly. **JCO CCI's editorial expectation is an external, citable,
timestamped artefact** — OSF, Zenodo, or AsPredicted, with a DOI in the
Methods statement.

Three concrete moves, in increasing strength:

1. **Weakest (acceptable for preprint, not for journal):** keep the GitHub
   commit-hash anchor, name the actual SHA-1 hash inline (not just "the
   repository's first commit"). The commit SHA is the audit trail; print it.
2. **Middle (acceptable for journal):** deposit `docs/prereg.md` as an OSF
   project. The OSF DOI takes about 15 minutes to mint, costs nothing, is
   immutable by design, and is precisely the artefact JCO CCI's screen
   expects. Cite the DOI in Methods §2.7 and again in the Preregistration
   statement.
3. **Strongest:** OSF deposit + Zenodo deposit of the entire repo at the
   v1.0.0-submission tag. The two complement each other (OSF for the
   protocol, Zenodo for the code+data). Round 2 §8 already asked for the
   Zenodo deposit; Round 1 already asked for the OSF deposit. Doing both is
   the lowest-friction permanent fix.

**For journal submission, option 2 is the minimum bar.** The current GitHub-
only language will be flagged by an experienced screening editor.

---

## 10. Reporting-transparency checklist (Supplementary Table S1)

Round 2 (item 9 of Round 1) asked specifically for **PRISMA-2020 + a
graph-construction reporting addendum**. The current Supplementary Table S1
delivers exactly this: items 1–29 are PRISMA-2020 items, items G1–G6 are the
graph-encoding addendum, and the header sentence acknowledges that "no
standard reporting guideline (TRIPOD, STROBE, PRISMA, CONSORT, STARD) is a
perfect fit. We adopt a custom transparency checklist that combines PRISMA-2020
reporting items (relevant to evidence synthesis) with a graph-encoding
addendum specific to the present method."

**Pass.** This is the Round 2 ask, delivered as requested. The "Reporting
Transparency" subsection of the main text (`main.tex` line 190) still says
"modelled on TRIPOD section structure", which is stale — the actual S1 is
PRISMA, not TRIPOD. **Minor tidy:** update line 190 to "PRISMA-2020 with a
graph-construction reporting addendum" to match the Supplement.

---

## Concrete asks for Round 4 (in priority order)

1. **Add `\citep{}` calls for the 10–12 named primary trials in Results §3.3
   and Methods §2.3.** The .bib entries already exist; this is one
   compilation pass, no new literature work. This single fix is the most
   load-bearing of all Round 3 asks (§2 above).
2. **Regenerate Figure 1.** Fix the five remaining Round 2 defects (truncated
   labels, blank target nodes, layout, two legends). Without this the figure
   is unusable in print (§8).
3. **Re-pitch as Methods Article.** Change the article-type declaration in
   the cover letter and in `JOURNAL.md`; the body framing, the abstract
   Conclusion, and the supplementary reporting checklist already match the
   Methods Article slot (§6).
4. **Soften the title.** Drop "Discordance Between Trial Chains and Guideline
   Pathways" and replace with one of the two suggested subtitles in §5; the
   word "Discordance" overpromises against a P = 0.37 result.
5. **Finish the cover letter** (`docs/cover_letter.md`): resolve five
   bracketed placeholders, commit to one article type, add ORCID iD to
   signature (§4). For preprint, this is optional; for journal submission it
   is blocking.
6. **Deposit `docs/prereg.md` on OSF** and replace the
   first-commit-hash language in Methods §2.7 and in the Preregistration
   statement with the OSF DOI (§9).
7. **Update the Reporting Transparency subsection (line 190 of `main.tex`)**
   from "modelled on TRIPOD section structure" to "PRISMA-2020 with a
   graph-construction reporting addendum" to match the Supplement (§10).
8. **Mint the Zenodo DOI before submission** and replace the placeholder in
   the Code Availability statement (`main.tex` line 184). This Round 2 ask
   remains open and will not pass screen as a placeholder.
9. **Complete the author block** *if and only if* the next deposit is to a
   journal portal. For a medRxiv preprint, leave as-is; for JCO CCI portal,
   resolve to "Independent Researcher, [city], [country]" with full given
   name and ORCID (§3).

---

## VERDICT

**MINOR REVISION** for the *preprint path* (medRxiv / bioRxiv deposit).

**MAJOR REVISION** for the *journal path* (JCO CCI submission).

The split is deliberate. The manuscript has converged: word counts pass,
reporting checklist passes, headline framing passes, discussion is honest,
figures 2 and 3 are publication-grade. **The science is screen-ready.** What
is not screen-ready is the *packaging* for an ASCO journal portal: Figure 1
will be flagged by reviewers, named trials are not citation-linked, the
article-type label still says Original Report against a Methods-Article body,
the cover letter has five bracketed placeholders, the Zenodo DOI is a
placeholder, the pre-registration is GitHub-only, and the author block is
literally `[to be supplied]`.

For a preprint, none of these are blocking — medRxiv routinely accepts
exactly this state, and the framing is already honest enough that the
preprint will land cleanly. **My recommendation is: deposit the preprint now
(after fixing asks 1 and 4, both ~1 hour of work each), and treat asks 2–9 as
the journal-submission to-do list for a separate cycle.**

If the author intends to skip the preprint step and submit directly to the
JCO CCI portal next week, the verdict is MAJOR REVISION — items 1, 2, 3, 5,
6, 8, 9 above are all blocking at the editorial screen.

---
*End of editorial decision letter, round 3.*
