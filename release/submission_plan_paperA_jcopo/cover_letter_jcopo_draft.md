# Cover Letter — JCO Precision Oncology Submission (Paper A)

> Replace [FILL IN] placeholders before submission. Edit any boilerplate to match your voice.

---

[Date — e.g., 2026-05-30]

Dr. Stacy W. Gray
Editor-in-Chief
*JCO Precision Oncology*
American Society of Clinical Oncology

Dear Dr. Gray,

We submit for consideration as an **Original Report** the manuscript "**Evidence-Free Decision Points in Biomarker-Driven Metastatic Cancer Guidelines: A Pre-Registered Multi-Tumor Audit of ESMO, ASCO, and NCCN Decision Trees in HR+/HER2- Breast Cancer and EGFR/ALK Non-Small-Cell Lung Cancer**."

The manuscript applies a pre-registered graph-theoretic framework to two biomarker-driven metastatic cancer settings. We placed the unified ESMO+ASCO+NCCN HR+/HER2- mBC and EGFR/ALK NSCLC decision tree (n = 49 decision nodes) onto a shared (state, biomarker) node space with a systematically-searched 259-trial pivotal corpus and asked how many decision nodes lack any trial edge directly traversing the recommended (state, biomarker) pair. The pre-registered one-sided exact-binomial test of H_0: EFDPR ≤ 0.25 rejected the null at P = 0.023 (strict-tolerance EFDPR 0.39, Clopper-Pearson 95\% CI 0.25--0.54; bootstrap CI 0.25--0.53). ESCAT-aligned and liberal tolerance gave 0.35 (P = 0.084), reported as pre-registered tolerance-grid sensitivity. The evidence gap is concentrated at NSCLC EGFR-mutant post-osimertinib decision nodes and at mBC post-CDK4/6i salvage positions (full per-node breakdown in Figure 2), where multiple guideline-endorsed second-line strategies (amivantamab+chemotherapy, HER3-ADC, TROP2-ADC, platinum doublet, everolimus+exemestane) do not have a trial that strictly enrolled the (state, biomarker) population the guideline describes.

This work fits JCO Precision Oncology because: (i) the analysis is restricted to biomarker-driven settings (HR+/HER2-, EGFR-mutant, ALK-rearranged), where precision oncology has produced the densest trial-evidence base and the most consequential treatment-sequencing decisions; (ii) the EFDPR overlay provides a directly actionable artefact for guideline committees and trial sponsors to prioritise the next generation of pivotal trials toward the specific (state, biomarker) target populations currently lacking direct evidence; (iii) the framework is biomarker-agnostic and tumour-agnostic, making it natural to extend to mCRC, melanoma, RCC, prostate, and other precision-oncology settings in subsequent applications.

A companion methods manuscript describing the framework in greater depth, together with the dual-LLM-annotator extraction protocol and inter-rater validation, is in concurrent submission to *Research Synthesis Methods*. The two manuscripts share the same underlying analysis and the same pre-registration (`docs/prereg-v3.md` at commit `4b5bf1a`, committed before any NSCLC outcome-touching analysis); the present submission foregrounds the precision-oncology clinical findings.

All artefacts (frozen JSON schema, decision-tree encodings, dual-annotator outputs, adjudication rules with rationale, analysis code, LaTeX sources, figures) are released under MIT licence at https://github.com/htlin222/mbc-evidence-dag-paper at the tagged release `v3.0.0`. The persistent Zenodo DOI is `10.5281/zenodo.20250848` (https://doi.org/10.5281/zenodo.20250848). Bootstrap seed `20260516` ensures deterministic reproducibility of every figure and table.

We declare no competing financial or non-financial interests relevant to this work. No specific funding was received. All data sources are publicly available; no human-subjects approval was required.

We suggest three potential reviewers with no apparent conflict of interest:
- [FILL IN reviewer 1, name + affiliation + email] (clinical informatics / evidence synthesis)
- [FILL IN reviewer 2, name + affiliation + email] (HR+/HER2- mBC clinician, not a co-author on any corpus trial)
- [FILL IN reviewer 3, name + affiliation + email] (EGFR/ALK NSCLC clinician, not a co-author on any corpus trial)

The manuscript has not been previously published and is not under consideration elsewhere. We have read and approved the manuscript and agree to its submission.

Sincerely,

Hsieh-Ting Lin, MD
Hematology & Medical Oncology Fellow
Department of Hematology & Medical Oncology
Koo Foundation Sun Yat-Sen Cancer Center
125 Lide Rd., Beitou Dist., Taipei 11259, Taiwan
htlin222@kfsyscc.org
ORCID iD: 0009-0002-3974-4528

---

## Editor pre-screen tips (delete this section before submission)

- JCO Precision Oncology's editorial screen tends to reject papers that don't have a clear biomarker-driven precision-oncology framing. Our title and Paragraph 3 hit this explicitly.
- The journal prefers manuscripts with at least one institutional senior author; if you can find a senior co-author with mBC or NSCLC expertise, it materially helps. If submitting solo as Independent Researcher, expect editorial scepticism — the cover letter should highlight the pre-registration and reproducibility as compensating credentials.
- Avoid the word "audit" if it might be misread as criticism of the panels; we use it deliberately but neutrally.
