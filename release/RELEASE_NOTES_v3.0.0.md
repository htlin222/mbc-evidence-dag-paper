# Release v3.0.0 — Multi-tumor extension (mBC + NSCLC) with two-paper split

**Date:** 2026-05-16
**Tag:** `v3.0.0`
**Supersedes scope of:** `v1.0.0` (mBC pilot) and `v2.0.0` (mBC production); both preserved at their tags.

## Headline finding (publishable)

On a pooled 49-node ESMO+ASCO+NCCN decision tree (25 mBC HR+/HER2- + 25 NSCLC EGFR/ALK) against a 210-edge trial-DAG from 259 systematically-searched pivotal trials:

**Strict-tolerance pooled EFDPR = 0.39 (Clopper-Pearson 95% CI 0.25–0.54; bootstrap CI 0.25–0.53);
pre-registered one-sided exact-binomial test of H₀: EFDPR ≤ 0.25 REJECTS at α = 0.05 (P = 0.023).**

ESCAT-aligned and liberal tolerance: EFDPR 0.35 (P = 0.084, marginal non-rejection).

Tumor-stratified sensitivity (strict; individually under-powered for confirmatory inference):
- mBC-only (n=25): EFDPR 0.40, P = 0.07 (marginal, consistent with v2.0.0)
- NSCLC-only (n=24): EFDPR 0.38, P = 0.12 (fails)
- NSCLC EGFR-only (n=17): EFDPR 0.41, P = 0.11 (fails)
- NSCLC ALK-only (n=7): EFDPR 0.29, P = 0.56 (well-evidenced; fails to reject — falsifiability demonstration)

## Trajectory across the program

| Version | Scope | EFDPR (strict) | Exact P | Reject? |
|---|---|---|---|---|
| v1.0.0 | mBC pilot (n=16 nodes) | 0.31 | 0.37 | fails |
| v2.0.0 | mBC production (n=25 nodes) | 0.40 | 0.07 | marginal |
| **v3.0.0** | **mBC + NSCLC pooled (n=49)** | **0.39** | **0.023** | **rejects** |

## Two-paper deliverables

| File | Pages | Target |
|---|---|---|
| `mbc-evidence-dag-paper-A-clinical-v3.0.0.pdf` (330 KB) | ~12 | JCO Precision Oncology / JCO Clinical Cancer Informatics |
| `mbc-evidence-dag-paper-A-clinical-v3.0.0.docx` (88 KB) | — | Word for submission portal |
| `mbc-evidence-dag-paper-B-methods-v3.0.0.pdf` (274 KB) | ~10 | Research Synthesis Methods |
| `mbc-evidence-dag-paper-B-methods-v3.0.0.docx` (22 KB) | — | Word for submission portal |

Both papers share the same underlying analysis and pre-registration commit (`4b5bf1a`). Paper A foregrounds the tumor-specific clinical findings; Paper B foregrounds the framework, dual-LLM-annotator validation, and reproducibility methodology.

## Pre-registration trail (auditable)

| Commit | Description |
|---|---|
| `085ae54` | prereg-v2 (mBC production) committed BEFORE any v2 outcome data |
| `079b540` | prereg-v2 amendment v2.1 (date range, enrolment threshold) BEFORE extraction |
| `4b5bf1a` | **prereg-v3** (NSCLC extension + multi-tumor pooled test) committed BEFORE any NSCLC outcome data |
| `11abc41` | v3 NSCLC corpus + dual-annotator extraction (post-prereg) |
| `0bcf6fa` | v3 pooled analysis: REJECT H₀ at P=0.023 |

Result trajectory disclosed in both manuscripts as part of pre-registration transparency.

## Reviewer-cycle history (across all versions)

- **v1.0.0**: 4 rounds × 4 reviewers = 16 adversarial reviews. Caught 6 NCT-misidentifications.
- **v2.0.0**: 2 rounds × 4 reviewers = 8 reviews. Caught extraction errors + missing pivotal trials.
- **v3.0.0**: 1 round of self-audit during execution. Caught 4 supplementary NCT-misidentifications (AURA3, HERTHENA-Lung01, TROPION-Lung01, FLAURA-CNS) before final analysis; corrected with hand-curated records.

**Total adversarial review passes across the program: 24+.**

## Honest caveats (disclosed in manuscripts)

- Strict-tolerance test rejects (P=0.023) but ESCAT-aligned and liberal tolerance give P=0.084 — tolerance-grid sensitivity matters and is reported as pre-registered
- Rejection is one node deep (k_crit=18, observed k=19 at n=49); BH correction across 15 cells would give q≈0.35. Defense: prereg-v3 commits the pooled strict-tolerance test as the single primary inferential commitment
- Pre-adjudication mean Cohen's κ on key fields: 0.67 (mBC) / 0.78 (NSCLC); failed gate on `akt_path` and `post_alk_tki` due to kappa paradox / small-n; PABAK pass on most fields
- Post-adjudication κ is structurally adjudicability, not independent re-rating
- Out-of-scope for v3: driver-negative NSCLC, KRAS G12C, ROS1, RET, MET ex14, NTRK, BRAF V600E, HER2-mutant NSCLC (deferred to v4)
- ORCID + institutional affiliation are placeholders pending submission

## Reproduce

```bash
git checkout v3.0.0
uv sync
# v3 NSCLC pipeline
uv run python analysis/v3_01_systematic_search_nsclc.py
uv run python analysis/v3_02_filter_nsclc.py
uv run python analysis/v3_03_assemble_nsclc.py
uv run python analysis/v3_04_prepare_extraction_nsclc.py
# Dual-annotator step: dispatched as parallel Claude + Codex agents per protocol
uv run python analysis/v3_05_merge_and_kappa_nsclc.py
uv run python analysis/v3_06_encode_nsclc_guideline.py
uv run python analysis/v3_07_build_combined_dag.py
uv run python analysis/v3_08_compute_pooled_efdpr.py
uv run python analysis/v3_09_figures.py
cd manuscript && latexmk -pdf paper_A_clinical_v3.tex && latexmk -pdf paper_B_methods_v3.tex
```

Bootstrap seed: `20260516`. Numerical outputs are deterministic.

## License
MIT. See `LICENSE`.

## Citation (preprint pending)

> Lin H.-T. *Evidence-Free Decision Points in Biomarker-Driven Metastatic Cancer Guidelines: A Pre-Registered Multi-Tumor Audit.* mbc-evidence-dag-paper, v3.0.0, 2026-05-16.

> Lin H.-T. *A Graph-Theoretic Framework for Measuring Evidence-Free Decision Points in Clinical Guidelines.* mbc-evidence-dag-paper, v3.0.0, 2026-05-16.
