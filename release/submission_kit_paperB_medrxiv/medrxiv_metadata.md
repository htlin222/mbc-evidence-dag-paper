# medRxiv Metadata Sheet — Paper B

> Copy-paste into the medRxiv submission portal. Fields marked [FILL IN] need your data.

## Title (≤200 characters; current = 168 chars)
A Graph-Theoretic Framework for Measuring Evidence-Free Decision Points in Clinical Guidelines, with Dual-LLM-Annotator Validation Across Two Solid Tumors

## Short Title (≤80 characters)
A graph-theoretic framework for guideline–trial evidence concordance

## Authors

| Order | Full Name | ORCID | Affiliation | Email | Corresponding? |
|---|---|---|---|---|---|
| 1 | Hsieh-Ting Lin | 0009-0002-3974-4528 | Department of Hematology & Medical Oncology, Koo Foundation Sun Yat-Sen Cancer Center, 125 Lide Rd., Beitou Dist., Taipei 11259, Taiwan | htlin222@kfsyscc.org | Yes |

## Abstract (≤250 words; current = 260 words approximate)

Clinical practice guidelines compose treatment recommendations across non-overlapping pivotal trials, but no general computational method has been published for quantifying the structural concordance between a guideline decision tree and its underlying trial evidence. We introduce a graph-theoretic framework that places both objects (pivotal-trial corpus, guideline decision tree) on a shared (state, biomarker) node space, defines an evidence-free decision-point ratio (EFDPR), and tests it with a pre-registered one-sided exact binomial test. The framework is paired with a dual-LLM-annotator extraction pipeline (Claude as annotator A; Codex/GPT-5 as annotator B) validated by Cohen's kappa and the prevalence-adjusted bias-adjusted kappa (PABAK). We demonstrate the framework across two biomarker-driven metastatic cancers (HR+/HER2-negative breast and EGFR-mutant/ALK-rearranged non-small-cell lung), pooling 259 systematically-searched pivotal trials against a 49-node unified ESMO+ASCO+NCCN decision tree. The pre-registered exact binomial test of H_0: EFDPR <= 0.25 at alpha = 0.05 rejected the null with P = 0.023 (strict-tolerance EFDPR 0.39, Clopper-Pearson 95% CI 0.25-0.54; ESCAT/liberal 0.35, P = 0.084). Pre-adjudication mean Cohen's kappa on key fields was 0.67-0.78 across tumors, with documented adjudication trail. The framework, schema, decision-tree encoding, dual-annotator outputs, and adjudication log are released under MIT licence at the GitHub URL in the Data Availability statement.

## Author Keywords (6)
clinical-guideline evaluation; trial-evidence concordance; graph-theoretic framework; LLM-extraction validation; Cohen's kappa; pre-registered binomial test

## Lay Summary (optional, ≤200 words)

Clinical guidelines for cancer treatment combine recommendations from many different clinical trials, but the trials usually do not test every step of the treatment pathway directly. This can create gaps in the evidence chain that supports specific treatment recommendations. We developed a computer-based method that maps both clinical trials and treatment guidelines onto a shared "decision-point" structure and counts where the guideline-recommended treatment is not directly supported by a trial that enrolled exactly that kind of patient. We tested the method on two cancers — hormone-receptor-positive breast cancer and lung cancer with EGFR or ALK mutations — using 259 pivotal trials and 49 guideline decision points. We found that roughly four in ten decision points lacked directly-supporting trial evidence under strict criteria, especially in lung cancer after first-line targeted therapy. To make the analysis trustworthy, we used two different AI assistants (Claude and GPT-5) to read trial eligibility criteria independently, then compared their answers using inter-rater agreement statistics. The method, code, and data are released openly so other groups can apply it to their own tumor type.

## Subject Area
- **Primary:** Health Informatics
- **Secondary:** Oncology

## Type of Article
Methodological Research Article (preprint)

## Funding Statement
No specific funding was received for this work.

## Competing Interest Statement
The author declares no competing financial or non-financial interests relevant to this work.

## Ethics Approval Statement
Not applicable. This study analyses publicly-available trial-registry data and publicly-available clinical-guideline documents only; no human subjects, animal subjects, or identifiable patient data were involved.

## Data Availability Statement
All structured data (frozen JSON schema, decision-tree encodings, dual-annotator outputs, adjudication rules), analysis code, and LaTeX sources are released under MIT licence at the GitHub repository linked in the Code Availability section of the manuscript. A persistent Zenodo DOI is minted at the tagged release (`v3.0.0`).

## Code Availability Statement
Python 3.12 analysis pipeline released at the GitHub URL with bootstrap seed `20260516` for deterministic reproducibility. See manuscript Methods §2.8.

## Preprint License
**CC-BY 4.0** (recommended for maximum reuse; matches the journal-target reproducibility ethos).

## Conflicts/Disclosures (medRxiv field)
None.

## Acknowledgements (will appear in the published preprint)
The author acknowledges the open-data infrastructure of ClinicalTrials.gov and the publishing programmes of ESMO, ASCO, and NCCN. The dual-annotator extraction protocol was implemented using Anthropic's Claude (annotator A) and OpenAI's Codex / GPT-5 (annotator B) via shared protocol documents; the model providers had no role in the design, analysis, or writing of this manuscript.
