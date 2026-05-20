# Cover Letter — Research Synthesis Methods Submission (Paper B)

> Replace [TBD] placeholders before submission. Reviewer suggestions in a
> separate file (`suggested_reviewers.md`).

---

2026-05-20

Professor Terri D. Pigott & Professor Dimitris Mavridis
Co-Editors-in-Chief
*Research Synthesis Methods*
Cambridge University Press

Dear Professors Pigott and Mavridis,

We submit for consideration as a **Research Article** the manuscript "**A Graph-Theoretic Framework for Measuring Evidence-Free Decision Points in Clinical Guidelines, with Dual-LLM-Annotator Validation Across Two Solid Tumors**" (Paper B in our two-paper programme; see also "concurrent submission" note below).

**The contribution.** Network meta-analysis pools trials at a single decision point and GRADE rates per-recommendation certainty, but no general method exists for measuring the structural concordance between an entire clinical-guideline decision tree and its underlying pivotal-trial evidence base. We introduce a graph-theoretic framework that places both objects --- a systematically-searched pivotal-trial corpus and a unified guideline decision tree --- on a shared (state, biomarker) node space, defines an evidence-free decision-point ratio (EFDPR), and tests it pre-registered with a one-sided exact binomial test against a fixed-effect null. The method is paired with a dual-LLM-annotator extraction pipeline (Claude 4.7 + Codex/GPT-5) validated by Cohen's kappa and the prevalence-adjusted bias-adjusted kappa (PABAK), with documented adjudication trail and full disclosure of pre-adjudication gate failures. We demonstrate the framework across two biomarker-driven metastatic cancers (HR+/HER2- breast, EGFR-mutant + ALK-rearranged NSCLC) on a pooled 49-node ESMO+ASCO+NCCN decision tree against a 212-edge trial-DAG drawn from 259 systematically-searched pivotal trials; the pre-registered exact binomial test of $H_0: \mathrm{EFDPR} \le 0.25$ at $\alpha = 0.05$ rejected the null with P = 0.023 (strict tolerance EFDPR 0.39, Clopper-Pearson 95% CI 0.25--0.54).

**Why Research Synthesis Methods.** The framework is biomarker-agnostic and tumour-agnostic. It is built on standard graph-data-structure tooling and on the ESCAT biomarker-actionability classification as the basis of a pre-registered tolerance grid; the inferential machinery is the Clopper-Pearson exact CI with bootstrap as sensitivity. The dual-LLM-annotator pattern with Cohen's kappa / PABAK validation and transparent adjudication generalises beyond oncology to any evidence-synthesis task that extracts structured data from trial registry records. The manuscript follows the journal's Research Synthesis Keywords convention, provides the required Highlights block (What is known / What is new / Impact), discloses AI model versions and prompts per the journal's 2025 AI/ML evaluation guidance, and pre-registers the analysis plan in advance of any outcome-touching analysis (commits `085ae54`, `079b540`, `4b5bf1a`).

**Reproducibility.** All artefacts --- frozen JSON schema, decision-tree encodings, dual-annotator per-trial outputs, adjudication rules with rationale, analysis code (Python 3.12 with deterministic seeds), LaTeX sources --- are released under MIT licence at https://github.com/htlin222/mbc-evidence-dag-paper (tag `v3.0.0`). The tagged release is permanently archived at Zenodo: **10.5281/zenodo.20250848** (https://doi.org/10.5281/zenodo.20250848). Bootstrap seed `20260516` yields byte-identical figure and table outputs across runs.

**Concurrent submission.** A companion clinical-application manuscript demonstrating the framework on the JCO Precision Oncology audience (HR+/HER2- mBC and EGFR/ALK NSCLC clinical findings) has been submitted in parallel to *JCO Precision Oncology* on the same date. The two manuscripts share the same underlying analysis and the same pre-registration; the present submission to *Research Synthesis Methods* foregrounds the framework, statistic, dual-LLM-annotator methodology, and inter-rater validation rather than the tumour-specific clinical findings.

**Declarations.** The manuscript has not been previously published and is not under consideration elsewhere except as stated above. We declare no competing financial or non-financial interests relevant to this work. No specific funding was received. No human subjects, animal subjects, or identifiable patient data are involved; all analysis is based on publicly-available clinical-trial registry data and publicly-available clinical-guideline documents, so ethics approval was not required.

**Suggested reviewers.** Three potential reviewers with no apparent conflict of interest are listed in the portal submission form (see `suggested_reviewers.md` in the submission kit for full details and conflict-screening notes).

We thank you for considering this submission.

Sincerely,

Hsieh-Ting Lin, MD
Hematology & Medical Oncology Fellow
Department of Hematology & Medical Oncology
Koo Foundation Sun Yat-Sen Cancer Center
125 Lide Rd., Beitou Dist., Taipei 11259, Taiwan
htlin222@kfsyscc.org
ORCID iD: 0009-0002-3974-4528
