# Release v1.0.0 — A Computable Map of Treatment-Sequencing Evidence in HR+/HER2- mBC

**Date:** 2026-05-16
**Target journal:** JCO Clinical Cancer Informatics (Original Report or Methods Article)

## Artifacts

| File | Format | Size | Purpose |
|---|---|---|---|
| `mbc-evidence-dag-paper-v1.0.0.pdf` | PDF | 330 KB | Main manuscript (10 pp.) |
| `mbc-evidence-dag-paper-v1.0.0.docx` | DOCX | 68 KB | Main manuscript, editable Word |
| `mbc-evidence-dag-paper-supplement-v1.0.0.pdf` | PDF | 205 KB | Supplementary material (3 pp.) |
| `mbc-evidence-dag-paper-supplement-v1.0.0.docx` | DOCX | 16 KB | Supplement, editable Word |

The full LaTeX source, references, figures, analysis code, structured data,
and pre-registration commit are at the tagged commit in this repository.

## Headline finding

In this pre-registered 16-trial pilot:

| Tolerance | EFDPR | Clopper-Pearson 95% CI | Exact one-sided P vs 0.25 |
|---|---|---|---|
| Strict       | 0.31 (5/16) | [0.11, 0.59] | 0.37 |
| ESCAT-aligned | 0.31 (5/16) | [0.11, 0.59] | 0.37 |
| Liberal      | 0.19 (3/16) | [0.04, 0.46] | 0.80 |

The pre-registered one-sided exact-binomial test of H₀: EFDPR ≤ 0.25 does
**not** reject under any tolerance level. The point estimate exceeds the
threshold under strict and ESCAT tolerance but the pilot corpus (n=16) is
under-powered for confirmatory inference.

Evidence-free decision points under strict concordance:

- G5 — post-CDK4/6i ESR1mut (SERD oral)
- G6 — post-endo AKT-pathway (AKTi + fulvestrant)
- G7 — post-CDK4/6i PIK3CAmut (PI3Ki + fulvestrant)
- G9 — post-CDK4/6i no-actionable mutation (everolimus + exemestane)
- G13 — post-CDK4/6i+post-endo (everolimus + exemestane)

A 15-node sensitivity excluding G16 (the gBRCAm node, a disclosed scope
deviation) preserves the result: strict EFDPR 0.33 (P = 0.31), liberal 0.20.

## Reviewer-cycle history

This release reflects four rounds of structured internal review by four
parallel reviewer personas (methods, clinical, biostatistics, JCO CCI
editor). The review files are in `reviews/round[1-4]/`.

Key corrections during review:

- **Round 1:** Two wrong NCT IDs corrected (NCT03997123 → NCT05169567 postMONARCH;
  NCT04032080 → NCT04191499 INAVO120). Pre-registered one-sided exact-binomial
  test added. LLM-extraction claim replaced with honest hand-curation description.
- **Round 2:** Four more wrong NCT IDs corrected (NCT02513394 was PALLAS adjuvant
  → real PALOMA-2 NCT01740427; NCT02675231 was monarcHER HER2+ → removed; MONARCH-3
  relabeled at NCT02246621; NCT02763566 was MONARCH plus → real MONALEESA-7 NCT02278120;
  MONALEESA-3 added at NCT02422615). Drug-class prefix matcher replaced with explicit
  equivalence table. Abstract trimmed under 300 words.
- **Round 3:** All 16 trial primary publications now cited in Methods. Title
  softened. G6 recoded to post-endo per ESMO 2024 actual placement of capivasertib.
  Figure 1 redesigned as tabular layout.
- **Round 4:** Final polish — discussion G6 wording, abstract trial-count phrasing,
  pinned Python deps, supplement provenance log, cover-letter title sync.

Final Round 4 verdicts:
- Clinical reviewer: MINOR (preprint-ready)
- Biostatistics reviewer: MINOR (preprint-ready; numerics verified to four decimals)
- JCO CCI editor reviewer: MINOR (preprint-ready)
- Methods reviewer: MAJOR (cited unaddressed polish items; not blockers for preprint)

## How to reproduce

```bash
cd mbc-evidence-dag-paper
uv sync
uv run python analysis/01_fetch_trials.py
uv run python analysis/02_extract_eligibility.py
uv run python analysis/03_encode_guideline.py
uv run python analysis/04_build_dag.py
uv run python analysis/05_compute_efdpr.py
uv run python analysis/06_compute_odi.py
uv run python analysis/07_figures.py
uv run python analysis/08_sensitivity_no_g16.py
cd manuscript && latexmk -pdf main.tex && latexmk -pdf supplement.tex
```

The bootstrap random seed is `20260516`; two consecutive runs of step 5 are
byte-identical.

## License

Code and manuscript text: MIT License. See `LICENSE`.

## Citation

Pre-publication citation (preprint pending):

> Lin H.-T. *A Computable Map of Treatment-Sequencing Evidence in HR+/HER2-
> Metastatic Breast Cancer: A Graph-Theoretic Pilot Comparing Trial Chains
> with the ESMO Guideline Decision Tree.* mbc-evidence-dag-paper, v1.0.0,
> 2026-05-16. GitHub: https://github.com/htlin222/mbc-evidence-dag-paper

## Known limitations explicitly disclosed in the manuscript

- 16-trial pilot is not a systematic-review-scale census.
- Trial selection seeded from ESMO/ASCO reference lists (selection bias).
- Eligibility coding is hand-curated, not LLM-extracted (LLM pipeline is
  the subject of a planned companion methods paper).
- ASCO and NCCN sensitivity analyses deferred to production extension.
- ORCID and full institutional address are placeholders pending submission.
