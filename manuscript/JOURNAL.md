# Target journal: JCO Clinical Cancer Informatics (JCO CCI)

> **Source caveat.** The ASCO publications site (`ascopubs.org`) returned HTTP 403
> to automated fetches on 2026-05-16. The numbers below are the **standard,
> publicly documented JCO-family conventions**. Any author MUST verify each
> number against the current JCO CCI "Information for Authors" PDF (download
> from ascopubs.org/jcci) before submission. Discrepancies are revision-cycle
> work, not blockers for first draft.

## Article type (chosen)
**Original Report** — appropriate for a hypothesis-driven, primary-data,
fully reproducible computational study with structured abstract.

## Manuscript structure
| Element | Cap | Format |
|---|---|---|
| Main text word count (Intro + Methods + Results + Discussion) | **3,000** | excludes abstract, refs, tables, figures |
| Abstract | **300 words**, structured | Purpose / Methods / Results / Conclusion |
| Key Objective + Knowledge Generated + Relevance | **120 words total** | required precis block |
| References | **50** | full author list up to 6, then "et al." |
| Tables + Figures combined | **7** | counted together |
| Supplementary material | unlimited | online-only PDF |

## Reference style
- **AMA 11th ed.**, numbered citations in order of appearance.
- Superscript citations in text (e.g. `...prior reports.\textsuperscript{3,7-9}`).
- BibTeX style: `vancouver` or `unsrtnat` with `\bibpunct{[}{]}{,}{n}{,}{,}` mimicry; for JCO CCI submission use a custom `ama` style or post-process to AMA. **LaTeX choice for this project:** `unsrtnat` + numbered superscript via `[numbers,super,sort&compress]` (already in template), with manual AMA refinement at submission stage.
- Journal abbreviations follow the NLM Title Abbreviations.

## Required statements (in this order at end of main text)
1. **Data availability** — public-source URLs + DOIs (this study uses public APIs, so list ClinicalTrials.gov / OpenAlex / ESMO source identifiers).
2. **Code availability** — GitHub URL + Zenodo DOI tag.
3. **Author contributions** — CRediT taxonomy.
4. **Conflict of interest** — required even if "none declared".
5. **Funding** — declare or state "no specific funding".
6. **Acknowledgements**.

## Reporting checklist
- **Not a clinical-prediction model**, so TRIPOD is not the primary checklist.
- **Reasonable choice:** TRIPOD-Cluster or PRISMA-NMA-adjacent are partial fits, but the cleanest match is **a self-declared "Methods and Reporting Transparency" checklist** in supplementary, modeled on TRIPOD section structure (data, participants, predictors, outcomes, analysis, validation, ethics). Attach as Supplementary Table S1.

## Other policies
- **Preprint policy** — bioRxiv / medRxiv allowed and encouraged. Cite the preprint in cover letter.
- **ORCID** — required for corresponding author at submission.
- **Open access** — JCO CCI is hybrid; OA fee ~USD 3,300 (verify at submission).
- **Suggested reviewers** — 3 recommended, none with conflict.

## Cover letter pointers (filed in `docs/cover_letter.md` later)
- One paragraph on the novelty: "first computational, graph-theoretic quantification of evidence-free decision points in mBC guideline trees".
- One paragraph on fit to JCO CCI: computational, reproducible, clinically actionable.
- Explicit statement that no overlapping submission exists.

## Style touches characteristic of JCO CCI accepted papers
- Clinical-actionability framing in Introduction first paragraph.
- Methods written so a re-implementation is feasible (figures used to be light-on-text; lean on tables for parameters).
- Results subsection titles describe the *finding*, not the *analysis* (e.g. "Four post-CDK4/6i decision nodes lacked any concordant trial-DAG edge" not "Concordance analysis").
- Discussion opens with a single-sentence headline restatement, then three caveats, then three positives, then limitations + outlook.
