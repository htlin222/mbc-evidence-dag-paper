# Cover Letter — JCO Clinical Cancer Informatics (v2.0.0)

[Date placeholder]

Dr. [Editor name placeholder]
Editor-in-Chief
JCO Clinical Cancer Informatics

Dear Dr. [Editor name placeholder],

We submit for consideration as an **Original Report** the manuscript "A Computable
Map of Treatment-Sequencing Evidence in HR+/HER2- Metastatic Breast Cancer: A 64-Trial,
Pre-Registered Graph-Theoretic Analysis of ESMO, ASCO, and NCCN Decision-Tree
Concordance."

The manuscript introduces a reproducible computational framework that places a
systematic pivotal-trial corpus and the unified ESMO+ASCO+NCCN HR+/HER2- mBC
guideline decision tree on a shared (state, biomarker) node space and computes an
evidence-free decision-point ratio (EFDPR) plus an operationalization discordance
index (ODI). On 25 unified decision nodes against 66 in-scope trial edges, the
pre-registered one-sided exact binomial test of $H_0: \mathrm{EFDPR} \le 0.25$
rejected the null at $\alpha = 0.05$ with $P = 0.011$ (EFDPR 0.48, Clopper-Pearson
95\% CI 0.28--0.69); operationalization discordance for the prior-CDK4/6i variable
across 3,240 trial pairs was substantial (ODI 0.64, CI 0.62--0.66).

The analysis is fully pre-registered (\texttt{docs/prereg-v2.md} commit \texttt{085ae54},
amendment v2.1 \texttt{079b540}, both committed before any v2 outcome data). The
LLM-extraction pipeline is dual-annotator validated (Claude + Codex/GPT-5; post-
adjudication mean PABAK 0.99 on key fields; Cohen's $\kappa$ paradox for
\texttt{akt\_path} explicitly disclosed). The framework, frozen schema, decision-tree
encoding, dual-annotator outputs, adjudication log, and 4-round v1 reviewer cycle
are released openly at \texttt{github.com/htlin222/mbc-evidence-dag-paper} under MIT
licence, permanently archived at Zenodo: \texttt{10.5281/zenodo.20250848}.

The manuscript has not been previously published and is not under consideration
elsewhere.

We suggest three potential reviewers with no apparent conflict of interest:
[Reviewer 1], [Reviewer 2], [Reviewer 3] (full names, affiliations, and emails to
be added at submission).

Sincerely,

Hsieh-Ting Lin, MD
Hematology \& Medical Oncology Fellow
Department of Hematology \& Medical Oncology
Koo Foundation Sun Yat-Sen Cancer Center
125 Lide Rd., Beitou Dist., Taipei 11259, Taiwan
\texttt{htlin222@kfsyscc.org}
ORCID iD: 0009-0002-3974-4528
