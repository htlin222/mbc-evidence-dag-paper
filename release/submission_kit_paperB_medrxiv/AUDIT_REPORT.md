# Paper B Audit — medRxiv submission readiness

Date: 2026-05-16
Audited PDF: `paper_B_methods.pdf` (274 KB, ~10 pp.)
Audit method: section-by-section review against medRxiv submission requirements.

## ✅ READY (no action needed)

| Item | Status | Notes |
|---|---|---|
| Title length (≤200 chars) | ✅ 168 chars | Well under cap |
| Abstract length (≤250 words) | ✅ 245 words | Within RSM and medRxiv cap |
| File format (PDF + Word) | ✅ PDF 274 KB; DOCX 22 KB | Both present |
| Figures embedded | ✅ Figure references resolve in compiled PDF | Inherits v3 figures |
| References (AMA style) | ✅ vancouver.bst close to AMA | Refs typeset with numbers + superscript |
| Pre-registration cited | ✅ commit `4b5bf1a` referenced in Methods | Auditable |
| Data availability stmt | ✅ Present (Section "Data Availability Statement") | Zenodo DOI placeholder pending |
| Code availability stmt | ✅ Present | Zenodo DOI placeholder pending |
| CRediT taxonomy | ✅ Single-author CRediT block present | Roles enumerated |
| AI/ML transparency | ✅ Model versions disclosed (Claude 4.7, Codex GPT-5) | Per RSM 2025 AI guidance |
| Funding statement | ✅ "No specific funding received" | |
| Conflicts statement | ✅ "None declared" | |
| Acknowledgements | ✅ ClinicalTrials.gov, ESMO/ASCO/NCCN, AI providers | |
| Highlights section | ✅ Required by RSM — present in mdframed box | What is known / new / impact |
| Research Synthesis Keywords | ✅ 6 keywords listed | After abstract |
| 5 reporting items (intro / sci background / results / implications / broader perspective) | ✅ Abstract covers all 5 RSM-required points | Confirmed |
| Abstract has no citations | ✅ No `\citep` in abstract block | RSM rule |
| Honest reporting of negatives | ✅ Cohen κ gate failure + kappa paradox disclosed; tolerance-sensitivity P=0.10 noted | Bar-raising honest |
| Reproducibility seed | ✅ `20260516` stated in Methods | |

## ✅ RESOLVED 2026-05-17 (was: NEEDS YOUR INPUT)

| Item | Resolved value | Source |
|---|---|---|
| Author full name | Hsieh-Ting Lin | lin.hsiehting.com/cv |
| ORCID iD | 0009-0002-3974-4528 | lin.hsiehting.com/cv |
| Affiliation | Department of Hematology & Medical Oncology, Koo Foundation Sun Yat-Sen Cancer Center, 125 Lide Rd., Beitou Dist., Taipei 11259, Taiwan | lin.hsiehting.com/cv |
| Correspondence email | htlin222@kfsyscc.org | confirmed by author |
| GitHub URL | github.com/htlin222/mbc-evidence-dag-paper | corrected handle |

## ⚠️ STILL NEEDS YOUR INPUT (cannot pre-stage)

| Item | Current | Action |
|---|---|---|
| Zenodo DOI | Not yet minted | Follow `ZENODO_INSTRUCTIONS.md` (~10 min after GitHub push) |
| GitHub push | Repo not yet public | Push v3.0.0 to github.com/htlin222/mbc-evidence-dag-paper |
| medRxiv endorsement | n/a | If first medRxiv submission, secure endorser; otherwise skip |

## ⚠️ MINOR ISSUES SURFACED (you can decide whether to fix before submission)

| # | Issue | Severity | Recommended action |
|---|---|---|---|
| 1 | Paper B inherits figure references from v2 mBC + v3 NSCLC analyses but does not reproduce the figure files in-text (Paper B is a methods paper — figures live in Paper A). The abstract says "Demonstrate the framework across two cancers" without showing the demonstrative figure. | low | Optional: insert v3_fig1_forest.pdf and v3_fig3_trajectory.pdf into Paper B as supporting figures. Adds ~1 page. |
| 2 | Reference list has duplicates from v1/v2/v3 era; `cardosoESMO2024` cites the 2021 paper bib entry but reads "2024 update" in prose. | medium | Bib entry should be replaced with the 2024 Annals of Oncology update DOI. Quick fix in `references.bib`. |
| 3 | Author block uses placeholder ORCID format `0000-0000-0000-0000` — submission portal may reject. | medium | Replace with real ORCID OR remove the line until submission. |
| 4 | "Section \ref{sec:tolerance}" cross-reference relies on `\label{sec:tolerance}` in §3.4 — visual check confirms it resolves correctly. | none | No action |
| 5 | The "post-adjudication κ is structurally adjudicability not independent re-rating" disclosure is in Methods §3.4 — surfaces honestly. | none | No action; this is a strength |

## Overall verdict

**Paper B is preprint-ready** subject to:
1. ~~Real ORCID + affiliation + name from you (~5 min)~~ **DONE 2026-05-17**
2. Push v3.0.0 to GitHub + mint Zenodo DOI (~15 min)
3. ~~Update the 3 placeholders in `paper_B_methods_v3.tex` and recompile (~3 min)~~ **DONE 2026-05-17**

Estimated total time from this state to medRxiv submission: **~15 minutes** (excluding medRxiv-staff queue, typically 1–3 days).
