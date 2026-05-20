# RSM Portal Metadata Sheet — Paper B

> Copy-paste into ScholarOne Manuscripts portal fields.

## Article Type
Research Article

## Title (≤300 characters; current = 154 chars)
A Graph-Theoretic Framework for Measuring Evidence-Free Decision Points in Clinical Guidelines, with Dual-LLM-Annotator Validation Across Two Solid Tumors

## Running Title (≤80 characters; current = 70 chars)
Graph-theoretic guideline-trial evidence concordance with dual-LLM extraction

## Authors (single)

| Order | Full Name | ORCID | Affiliation | Email | Corresponding? |
|---|---|---|---|---|---|
| 1 | Hsieh-Ting Lin | 0009-0002-3974-4528 | Department of Hematology & Medical Oncology, Koo Foundation Sun Yat-Sen Cancer Center, 125 Lide Rd., Beitou Dist., Taipei 11259, Taiwan | htlin222@kfsyscc.org | Yes |

## Abstract (≤250 words; current = 244 words; plain text below — no LaTeX markup)

Clinical practice guidelines compose treatment recommendations across non-overlapping pivotal trials, but no general computational method has been published for quantifying the structural concordance between a guideline decision tree and its underlying trial evidence. We introduce a graph-theoretic framework that places both objects (pivotal-trial corpus, guideline decision tree) on a shared (state, biomarker) node space, defines an evidence-free decision-point ratio (EFDPR), and tests it with a pre-registered one-sided exact binomial test. The framework is paired with a dual-LLM-annotator extraction pipeline (Claude as annotator A; Codex/GPT-5 as annotator B) validated by Cohen's kappa and the prevalence-adjusted bias-adjusted kappa (PABAK). We demonstrate the framework across two biomarker-driven metastatic cancers (HR+/HER2-negative breast and EGFR-mutant/ALK-rearranged non-small-cell lung), pooling 259 systematically-searched pivotal trials against a 49-node unified ESMO+ASCO+NCCN decision tree (post v3 round-1 internal review correction of 4 NCT-misidentifications, 6 encoding bugs, and 1 mid-flight guideline-node de-duplication). The pre-registered exact binomial test of H_0: EFDPR <= 0.25 at alpha = 0.05 rejected the null with P = 0.023 (strict-tolerance EFDPR 0.39, Clopper-Pearson 95% CI 0.25-0.54; bootstrap CI 0.25-0.53); ESCAT and liberal tolerance gave 0.35 (P = 0.084). Pre-adjudication mean Cohen's kappa on key fields was 0.67-0.78 across tumors, with documented adjudication trail. The framework, schema, decision-tree encoding, dual-annotator outputs, and adjudication log are released under MIT licence at github.com/htlin222/mbc-evidence-dag-paper (v3.0.0) and archived at Zenodo (10.5281/zenodo.20250848).

## Author Keywords (6)
clinical-guideline evaluation; trial-evidence concordance; graph-theoretic framework; LLM-extraction validation; Cohen's kappa; pre-registered binomial test

## Subject Area
- Primary: Evidence Synthesis Methods
- Secondary: Health Informatics

## Funding Statement
No specific funding was received for this work.

## Competing Interest Statement
The author declares no competing financial or non-financial interests relevant to this work.

## Ethics Approval Statement
Not applicable. This study analyses publicly-available clinical-trial-registry data and publicly-available clinical-guideline documents only; no human subjects, animal subjects, or identifiable patient data were involved.

## Data Availability Statement
All structured data (frozen JSON schema, decision-tree encodings, dual-annotator outputs, adjudication rules), analysis code, and LaTeX sources are released under MIT licence at https://github.com/htlin222/mbc-evidence-dag-paper at the tagged release v3.0.0. The release is permanently archived at Zenodo: 10.5281/zenodo.20250848 (https://doi.org/10.5281/zenodo.20250848).

## Code Availability Statement
Python 3.12 analysis pipeline released at the GitHub URL and Zenodo DOI with bootstrap seed 20260516 for deterministic reproducibility. See manuscript Methods §2.8.

## AI/ML Transparency Statement (per RSM 2025 author guidance)
Trial-eligibility extraction used Anthropic's Claude (model version 4.7, execution timestamp 2026-05-16) as annotator A and OpenAI's Codex / GPT-5 (model version GPT-5, execution timestamp 2026-05-16) as annotator B, with extraction prompts released in the GitHub repository (`analysis/extraction_protocol.md` and `extraction_protocol_nsclc.md`). Inter-rater agreement was validated with Cohen's kappa and PABAK, and pre-adjudication gate failures were disclosed in Methods. The model providers had no role in the design, analysis, or writing of this manuscript.

## CRediT Author Statement
**Hsieh-Ting Lin**: Conceptualization, Methodology, Software, Formal analysis, Investigation, Data curation, Validation, Visualization, Writing — original draft, Writing — review & editing, Project administration.

## Concurrent Submission Declaration
A companion clinical-application manuscript demonstrating the framework on HR+/HER2- breast and EGFR/ALK NSCLC clinical findings has been submitted in parallel to JCO Precision Oncology on the same date. The two manuscripts share the same underlying analysis and pre-registration but address different audiences and emphases; the present submission foregrounds the methodology and dual-LLM-annotator validation.

## Preprint Status
None. This manuscript has not been deposited as a preprint.
