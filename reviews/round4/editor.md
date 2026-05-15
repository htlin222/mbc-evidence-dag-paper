# JCO Clinical Cancer Informatics — Editor Review, Round 4 (final)

**Manuscript:** *A Computable Map of Treatment-Sequencing Evidence in HR+/HER2-
Metastatic Breast Cancer: A Graph-Theoretic Pilot Comparing Trial Chains with
the ESMO Guideline Decision Tree*
**Author:** H.-T. Lin (single author)
**Reviewer role:** Decision Editor, editorial-screen simulation, JCO CCI
**Question for this round:** Would the manuscript, as it stands today, clear
the editorial screen for a **medRxiv / bioRxiv preprint deposit**?
**Date:** 2026-05-16

---

## What converged since Round 3

| Round 3 ask | Status |
|---|---|
| Trial citations in Results §3.1 / Methods §2.3 | **Resolved.** All 16 named trials now carry `\citep{}` calls at first mention (`main.tex` line 118); bibliography expanded from 6 → 21 entries. This was the load-bearing fix and it landed cleanly. |
| Title softening — drop "Discordance" | **Resolved.** New subtitle reads "A Graph-Theoretic Pilot Comparing Trial Chains with the ESMO Guideline Decision Tree" (line 39). Calibrated to the P = 0.37 result. |
| Reporting Transparency line 190 ("TRIPOD" stale reference) | **Resolved.** Now reads "PRISMA 2020, augmented with a six-item graph-encoding addendum" (line 190). Matches Supplement §S1. |
| Headline framing leads with descriptive map | **Resolved end-to-end.** Abstract Conclusion, KO box, Results §3.2 bold sentence, and Discussion opener are now mutually consistent. |
| Word counts | **Compliant with headroom.** Abstract 230 / KO 91 / main text 2,509 (Intro 339, Methods 700, Results 649, Discussion 821). KO trimmed by another 15 words this round; 29-word headroom under the 120-word cap. |

---

## 1. Word-count audit (verified)

```
$ uv run python analysis/wordcount.py
      Abstract:  230 words   (cap 300; 70-word headroom)
        KO box:   91 words   (cap 120; 29-word headroom)
  Introduction:  339 words
       Methods:  700 words
       Results:  649 words
    Discussion:  821 words
   Main total:  2,509 words  (cap 3,000; 491-word headroom)
```

Pass for both preprint and journal slot.

## 2. References — all named trials cited

The bibliography (`main.bbl`) now resolves to **21 unique entries**: ESMO 2024,
NCCN, ASCO, the 16 corpus trials (PALOMA-2/3, MONARCH-2/3, MONALEESA-2/3/7,
SOLAR-1, EMERALD, CAPItello-291, DESTINY-Breast04/06, postMONARCH, INAVO120,
TROPiCS-02, OlympiAD), and the subgroup-representation reference
(`niranjan2020`). Each corpus trial is cited at first mention in Results §3.1
via `\citep{}`. The previously-flagged Round 3 first-pass-screen risk
(missing primary citations) is closed. Under the 50-reference cap with
29-entry headroom.

## 3. Author block

```
\author[1,*]{H.-T.\ Lin}
\affil[1]{[Affiliation and full postal address to be supplied at submission].}
\affil[*]{Correspondence: \texttt{ppoiu87@gmail.com}. ORCID iD and full
   institutional address are placeholders pending the submission-time
   author block.}
```

medRxiv / bioRxiv will accept this. The Gmail corresponding-author address is
permitted, the literal placeholder string is a yellow flag that screening
moderators routinely accept on preprint servers, and ORCID is encouraged but
not enforced at preprint deposit. **Pass for preprint.** For the journal
portal this remains blocking (asks 9 of Round 3 unchanged); fix at the
journal-submission boundary, not at the preprint boundary.

## 4. Figure 1 — improved, still not publication-grade

Substantial progress since Round 3. The new figure (`figures/fig1_dag.pdf`)
has a proper hierarchical layout with `x = patient state at trial enrolment`
and `y = biomarker profile`, all 16 trials are present, source nodes carry
both state and biomarker tuple labels, and the N = 16 / N = 14 inconsistency
is fully resolved. Three Round 2 defects (trial count, layout, source-node
labels) are closed.

Three defects remain, all material for print legibility:

- **Label collisions at the two highest-degree nodes.** The
  `post-endo [HR+/HER2-]` node (degree 4) and the
  `post-endo+post-CDK46i [HR+/HER2-]` node (degree 2) both render their trial
  annotations on top of each other. Concretely: PALOMA-3, MONARCH-2,
  MONALEESA-3 and CAPItello-291 callouts overprint at the post-endo node, and
  postMONARCH and EMERALD overprint at the post-CDK46i node. At 0.85\linewidth
  print width this is illegible. The two HER2-low callouts (DESTINY-Breast06
  vs DESTINY-Breast04, attached to two different nodes) also collide visually
  because their target nodes sit at nearly the same y-coordinate.
- **No node-colour legend.** The figure caption (`main.tex` line 123) claims
  "Node colour: distance from first-line treatment-naive state", but every
  source node in the PDF renders in a single shade of light blue. Either the
  colour mapping is not being applied or all nodes are at the same distance;
  either way the claim in the caption is not supported by the figure.
- **No edge-thickness legend.** Caption claims "Edge thickness: enrolment
  count"; the figure shows uniform-width annotation arrows only (no actual
  edges between source and target nodes in the strict DAG sense, just
  trial-to-source-node callouts). The enrolment-count encoding is invisible.

These are the same three defects flagged in Round 3 §8 minus the three that
were fixed. For a preprint, **none of them is a screen blocker** — medRxiv /
bioRxiv accept figures of this quality routinely, and the figure is now
substantively informative even with the collisions. For the journal-portal
boundary it remains blocking; flag for that boundary, not this one.

## 5. Cover letter

`docs/cover_letter.md` still contains five bracketed placeholders ([Date],
[Editor name] ×2, [Reviewer 1/2/3], [Affiliation to be supplied]) and still
hedges between three article types ("Original Report (or, at the editor's
discretion, as a Methods Article or Research Letter)"). The article-type
recommendation in Round 3 §6 (re-pitch as Methods Article) was not adopted,
and the title still cites the old "Discordance" subtitle (line 14 of the
cover letter) — that subtitle no longer matches `main.tex` line 39 since
the Round 3 title fix landed.

**For the preprint header** (which is what this round is gating): a cover
letter is not required by medRxiv / bioRxiv. The placeholders are journal-
boundary blockers, not preprint-boundary blockers. The internal title
mismatch (cover-letter title vs main-text title) is, however, a one-minute
fix that should land before deposit so that the preprint description on
medRxiv does not need to be re-edited later.

## 6. Zenodo DOI and pre-registration

`main.tex` line 184 still reads "Persistent code DOI via Zenodo to be minted
at release." Round 1 (item 6) and Round 2 (§8) asked for the DOI before
submission. For a preprint deposit this is **acceptable but suboptimal** —
medRxiv accepts a GitHub URL as the code pointer, and the Zenodo deposit can
be minted concurrent with preprint posting. For the journal portal it is
blocking. **Recommendation:** mint the Zenodo DOI in the same 30-minute
window as the preprint deposit; the GitHub–Zenodo webhook will mint it
automatically on tag push.

Pre-registration is still anchored to the repository's first commit hash
(`main.tex` line 187). For preprint deposit this is acceptable; the OSF DOI
deposit (Round 3 §9) is the journal-boundary fix.

## 7. Internal consistency check

I ran an end-to-end consistency check across the main text, the discussion,
the supplement, and Figure 1:

- N = 16 trials is consistent across abstract, Results §3.1, Figure 1 title,
  KO box, Table 1, and Supplement §S2.
- EFDPR strict = 0.31 (5/16) is consistent across abstract, Results §3.2, KO
  box, Discussion headline, and Table 2.
- Clopper-Pearson CI = [0.11, 0.59] is consistent across abstract, Results
  §3.2, and Table 2.
- ODI prior-CDK4/6i = 0.91 (n = 7 trials) is consistent across abstract,
  Results §3.3, Figure 3, and Table 3.
- Decision-node labels (G3, G5, G6, G7, G9, G13, G16) are consistent across
  Results §3.2, §3.4, §3.5, and Discussion.

**Pass.** The Round 1–Round 3 NCT-identification errors and trial-count
inconsistencies are fully resolved.

## 8. Reporting and supplement

- Supplement §S1: PRISMA-2020 + graph-encoding addendum (G1–G6). **Pass.**
- Supplement §S2 / §S3 / §S4: hand-curated schema, ESMO decision-tree
  encoding, ODI biomarker-token vocabulary released as JSON in the repo.
  **Pass.**
- Supplement §Text 1: nine pre-registration deviations disclosed
  (corpus seeding, six NCT corrections, scope deviations, descriptive
  S2/S3, Clopper-Pearson addition, exact-binomial primary test, drug-class
  equivalence table, NCCN deferral, selection-bias disclosure). This is
  unusually transparent and is an editorial-screen positive, not a flag.

---

## Concrete asks for Round 4 (final, in priority order)

The asks below are scoped to **preprint deposit only**. Journal-portal asks
from Round 3 (§3 author block, §6 cover letter, §9 OSF/Zenodo) remain open
and should be tracked separately for the journal-submission cycle.

1. **Sync the cover-letter title.** `docs/cover_letter.md` line 14 still
   reads "Graph-Theoretic Discordance Between Trial Chains and Guideline
   Pathways." Update to match `main.tex` line 39 ("A Graph-Theoretic Pilot
   Comparing Trial Chains with the ESMO Guideline Decision Tree") so the
   preprint description does not mismatch the manuscript title.
2. **Fix Figure 1 label collisions.** Offset the trial annotations at the
   `post-endo [HR+/HER2-]` and `post-endo+post-CDK46i [HR+/HER2-]` nodes
   (e.g. stagger callout y-positions, or add a per-node mini-legend) so that
   PALOMA-3 / MONARCH-2 / MONALEESA-3 / CAPItello-291 and
   postMONARCH / EMERALD do not overprint each other. This is a one-pass
   renderer fix and the only Figure 1 defect that materially harms preprint
   readability.
3. **Either implement node-colour and edge-thickness encodings or update
   the caption.** Caption claims a node-distance colour map and an
   enrolment-count edge-thickness map, neither of which appears in the
   rendered PDF. Pick one of (a) implement both encodings in the renderer
   and add a visible legend, or (b) cut both claims from the caption. The
   current state (caption claims encodings that the figure does not show)
   is the largest figure-caption mismatch in the draft.
4. **Mint the Zenodo DOI concurrent with preprint deposit.** Tag
   `v1.0.0-preprint`, push, and replace the placeholder on `main.tex`
   line 184 with the resolved DOI before the preprint posts. The
   GitHub–Zenodo webhook makes this a 5-minute operation and removes the
   only remaining "to be minted" placeholder in the main text.
5. **Spell out the pre-registration commit SHA.** `main.tex` line 187 says
   "The pre-registration commit hash is recorded in the repository's first
   commit"; print the actual SHA-1 inline (e.g. "first commit
   `abcdef1`") so the audit trail is in the manuscript, not behind a
   `git log` invocation. This is the Round 3 §9 option-1 (weakest, but
   preprint-sufficient) fix.
6. **Add medRxiv subject categories to `JOURNAL.md`.** The current
   `JOURNAL.md` documents JCO CCI conventions but not the preprint deposit
   parameters (medRxiv subject categories — Oncology + Health Informatics —
   licence selection CC-BY 4.0, and the funder field). Add a short
   "Preprint deposit" section so the deposit is repeatable.
7. **Cross-link the preprint DOI back into the manuscript at deposit.**
   Once the medRxiv DOI resolves, add a one-line "This manuscript has been
   deposited as a preprint at medRxiv (DOI: …)" sentence either to
   `JOURNAL.md` or as a footnote on `main.tex` page 1. Optional but
   conventional for the journal-submission boundary downstream.

(Asks 1, 5, 6 are five-minute fixes. Asks 2, 3 are 30–60 minutes each at the
renderer. Ask 4 is the only one that requires an external service. Ask 7 is
post-deposit.)

---

## VERDICT

**MINOR** — preprint deposit can proceed.

The manuscript has converged across four rounds. Word counts pass with
headroom. Headline framing is honest and consistent end-to-end (abstract,
KO box, Results §3.2, Discussion). All 16 named trials carry primary
publication citations. The title no longer over-claims. The PRISMA-2020 +
graph-encoding reporting checklist is in place. The pre-registration
deviation log is unusually transparent and is a screening-editor positive.
Internal trial-count, EFDPR, CI, ODI, and decision-node-label consistency
checks all pass.

The seven asks above are polish — none of them is a screen blocker for
medRxiv / bioRxiv. The largest remaining defect (Figure 1 label collisions
and caption-vs-figure encoding mismatch, asks 2–3) is a print-readability
issue, not a science or framing issue, and is recoverable by a renderer pass
without manuscript edits.

For the **journal-portal boundary** (next cycle, not this one): Round 3
asks 3, 5, 6, 8, 9 remain open (article-type re-pitch to Methods Article,
cover-letter placeholders, OSF deposit of `prereg.md`, Zenodo DOI in the
Code Availability statement, full author block with ORCID and institutional
affiliation). The journal verdict, applied today, would still be **MAJOR
REVISION** on packaging grounds — but that is the wrong gate for this round.

For the **preprint boundary** (this round): **ACCEPT WITH MINOR REVISION —
deposit can proceed once asks 1 and (ideally) 2–4 land.**

---
*End of editorial decision letter, round 4 (final).*

**VERDICT: MINOR**
