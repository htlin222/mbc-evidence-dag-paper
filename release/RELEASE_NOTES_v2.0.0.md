# Release v2.0.0 — Production-scale ESMO+ASCO+NCCN analysis

**Date:** 2026-05-16
**Target journal:** JCO Clinical Cancer Informatics (Original Report)
**Tag:** `v2.0.0`
**Supersedes:** `v1.0.0` (16-trial pilot; preserved at tag `v1.0.0`)

## Artifacts

| File | Format | Size | Purpose |
|---|---|---|---|
| `mbc-evidence-dag-paper-v2.0.0.pdf` | PDF | 353 KB | Main manuscript |
| `mbc-evidence-dag-paper-v2.0.0.docx` | DOCX | 92 KB | Word version |
| `mbc-evidence-dag-paper-supplement-v2.0.0.pdf` | PDF | 239 KB | Supplement |
| `mbc-evidence-dag-paper-supplement-v2.0.0.docx` | DOCX | 16 KB | Supplement (Word) |

## Headline (honest)

**81-trial systematic corpus, 25-node unified ESMO+ASCO+NCCN HR+/HER2- mBC decision tree:**

| Analysis | EFDPR | Clopper-Pearson 95% CI | Exact one-sided P | Reject H₀? |
|---|---|---|---|---|
| Primary (n=25)           | 0.40 (10/25) | [0.21, 0.61] | 0.071 | **no** (marginal) |
| Sensitivity: ESMO-only (n=16)   | 0.31 (5/16) | [0.11, 0.59] | 0.370 | no |
| Sensitivity: ASCO-citing (n=15) | 0.20 (3/15) | [0.04, 0.48] | 0.764 | no |
| Sensitivity: NCCN-citing (n=10) | 0.40 (4/10) | [0.12, 0.74] | 0.224 | no |

**The pre-registered one-sided exact-binomial test of H₀: EFDPR ≤ 0.25 marginally failed to reject at α = 0.05 (P = 0.071).** The point estimate (0.40) modestly exceeds the threshold (0.25), and the pilot-to-production scaling produced a clear directional shift (v1.0.0 16-node pilot: 0.31, P = 0.37 → v2.0.0 25-node production: 0.40, P = 0.071), but confirmatory inference at single-tumour scale was not achieved.

## Pre-registration trail (auditable)

| Commit | Description |
|---|---|
| `085ae54` | prereg-v2: committed BEFORE any v2 outcome data |
| `079b540` | prereg-v2 amendment v2.1: widened date filter to 2013-2026, enrolment ≥200 |
| `93f0b9a` | systematic search + corpus assembly |
| `4233d46` | dual-annotator extraction + adjudication |
| `6d25902` | initial pipeline (round-0): EFDPR 0.60, P=0.0002 |
| `9a12001` | round-0 manuscript |
| `218cd2c` | round-1 integration: 4 R1 fixes, BYLieve + SERENA-6 added → 0.48, P=0.011 |
| `2d91aef` | round-2 integration: post-adjudication CAPItello-291 + DB-06 → 0.40, P=0.071 |

The result trajectory (0.60 → 0.48 → 0.40) and P-trajectory (0.0002 → 0.011 → 0.071) is **fully disclosed in the manuscript Discussion** as part of the pre-registered transparency commitment.

## What's new vs v1.0.0

| Item | v1.0.0 | v2.0.0 |
|---|---|---|
| Trial corpus | 16 hand-curated guideline-cited | 81 systematic CT.gov search + adjudicated |
| Guideline nodes | 16 ESMO | 25 ESMO+ASCO+NCCN unified |
| LLM extraction | Hand-curated (claimed) | Dual-annotator validated (Claude + Codex/GPT-5) |
| Kappa | n/a | Pre-adj κ=0.40 (post_endo); post-adj PABAK 0.99 |
| Primary EFDPR | 0.31 strict | 0.40 strict |
| Primary P | 0.37 | 0.071 (marginal) |
| Sensitivity grid | strict + ESCAT + liberal | + 3 guideline-source subsets |
| ODI | n=6 trials, prior-CDK4/6i 0.91 | n=81 trials, prior-CDK4/6i 0.64 [0.62, 0.66] |
| Reviewer cycle | 4 rounds × 4 reviewers (v1) | + 2 rounds × 4 reviewers (v2) |

## Reviewer cycle history

- **v1**: 4 rounds × 4 adversarial reviewers (methods, clinical, biostatistics, JCO CCI editor). Caught 6 wrong NCT IDs across rounds; final verdict 3 MINOR + 1 polish.
- **v2**: 2 rounds × 4 adversarial reviewers. Round 1 surfaced 2 missing pivotal trials (BYLieve, SERENA-6) and 3 extraction errors; Round 2 surfaced the post-CDK4/6i subgroup-readout adjudication and the stale-paragraph issues.

Both cycles are in `reviews/`.

## Reproduce

```bash
cd mbc-evidence-dag-paper
git checkout v2.0.0
uv sync
uv run python analysis/v2_01_systematic_search.py
uv run python analysis/v2_02_filter_corpus.py
uv run python analysis/v2_03_assemble_corpus.py
uv run python analysis/v2_04_prepare_extraction.py
# extraction step: dispatched as parallel Claude + Codex agents per protocol
uv run python analysis/v2_05_merge_and_kappa.py
uv run python analysis/v2_06_adjudication.py
uv run python analysis/v2_07_build_dag.py
uv run python analysis/v2_08_extend_guideline.py
uv run python analysis/v2_09_compute_efdpr.py
uv run python analysis/v2_10_compute_odi.py
uv run python analysis/v2_11_figures.py
cd manuscript && latexmk -pdf main_v2.tex && latexmk -pdf supplement_v2.tex
```

Bootstrap seed: `20260516`. Numerical outputs are deterministic.

## License

MIT. See `LICENSE`.

## Citation (preprint pending)

> Lin H.-T. *A Computable Map of Treatment-Sequencing Evidence in HR+/HER2- Metastatic
> Breast Cancer: A Pre-Registered, Systematic Graph-Theoretic Analysis of ESMO, ASCO,
> and NCCN Decision-Tree Concordance.* mbc-evidence-dag-paper, v2.0.0, 2026-05-16.

## Honest limitations (disclosed in manuscript)

- 81-trial corpus is a snapshot; trials primarily-completed after 2026 excluded
- BOLERO-2 excluded by amendment v2.1 start-year filter; G9/G13 evidence-free status partially reflects that
- Cohen's κ paradox on akt_path explicitly disclosed; PABAK reported as the alternative measure
- Post-adjudication κ measures adjudicability, not independent re-rating
- Single-tumour scale; multi-tumour pooling needed for fully-powered confirmatory test
- Author block, ORCID, and full affiliation are placeholders for submission-time fill
