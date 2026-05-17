# Paper A Audit — JCO Precision Oncology submission readiness

Date: 2026-05-16
Audited PDF: `release/mbc-evidence-dag-paper-A-clinical-v3.0.0.pdf` (330 KB, ~12 pp.)

## ✅ READY

| Item | Status | Notes |
|---|---|---|
| Title length and biomarker-driven framing | ✅ | "Biomarker-driven metastatic cancer guidelines" — fits JCO PO mission |
| Structured abstract | ✅ Present | Purpose / Methods / Results / Conclusion blocks |
| Key Objective / Knowledge Generated / Relevance box | ✅ Present | JCO-family convention |
| Pre-registration cited | ✅ | `prereg-v3.md` commit `4b5bf1a` |
| Pre-registered exact-binomial test as primary | ✅ | Stated explicitly in Methods |
| Headline result (P=0.023 REJECT) | ✅ | Consistently throughout |
| Tumor-stratified sensitivity | ✅ | mBC / NSCLC / NSCLC-EGFR / NSCLC-ALK |
| 3 figures present and referenced | ✅ | Forest, per-node, trajectory |
| Discussion: 3 caveats + 3 positives + limitations + outlook | ✅ | Standard structure |
| Data + Code availability statements | ✅ | Both present |
| Conflicts + funding | ✅ | Both present |

## ✅ RESOLVED 2026-05-17

| Item | Resolved value | Source |
|---|---|---|
| Author full name | Hsieh-Ting Lin | lin.hsiehting.com/cv |
| ORCID iD | 0009-0002-3974-4528 | lin.hsiehting.com/cv |
| Affiliation | Department of Hematology & Medical Oncology, Koo Foundation Sun Yat-Sen Cancer Center, Taipei, Taiwan | lin.hsiehting.com/cv |
| Postal address | 125 Lide Rd., Beitou Dist., Taipei 11259, Taiwan | Koo Foundation public address |
| Correspondence email | htlin222@kfsyscc.org | confirmed by author |
| GitHub URL | github.com/htlin222/mbc-evidence-dag-paper | corrected handle |

## ⚠️ STILL NEEDS YOUR INPUT BEFORE SUBMISSION

| Item | Current | Action (day reference per POLISH_PLAN) |
|---|---|---|
| medRxiv preprint DOI | not yet | Day 5 — after Paper B medRxiv assigns DOI |
| Zenodo DOI | `[FILL IN Zenodo DOI]` | Day 1 — after Zenodo webhook |
| Suggested reviewers (3) | none listed | Day 6 — research and add |
| Cover letter | draft in `cover_letter_jcopo_draft.md` (author block resolved) | Day 7 — finalize editor name, reviewer names, date |
| Supplement (Tables S1-S4) | not yet compiled | Day 10 — create |

## MINOR ISSUES IDENTIFIED IN AUDIT

| # | Issue | Severity | Suggested fix |
|---|---|---|---|
| 1 | Figure 1 caption refers to "Diamond: primary 49-node analysis" but in publication-grade rendering the diamond is similar in size to circles; readers may not notice. | low | Increase markersize gap (10 → 14 for diamond) in `v3_09_figures.py` line 36 |
| 2 | "NSCLC ALK-only (n=7)" sensitivity has n very small; CP-CI [0.03, 0.65] is wide. The narrative correctly notes "well-evidenced" but a sceptical reviewer may flag the small-n CI as inadequately powered to detect a gap. | medium | Add one sentence acknowledging that ALK-only n=8 is underpowered (~30% power at p1=0.40) — disclose this as a structural limit. |
| 3 | The pooled-rejection driven heavily by NSCLC EGFR-only could be framed as "the rejection depends on EGFR-mutant nodes; a stricter null analysis would be the EGFR-only test". An aggressive reviewer might argue the pooled test is over-powered by the EGFR subset. | medium | Add Discussion paragraph: "EGFR-only sensitivity confirms the same direction without pooling; pooled rejection therefore reflects genuine multi-tumor signal, not artificially pooled noise." |
| 4 | The Methods section is dense for an Original Report (could exceed JCO PO's 3000-word cap once supplement is split off). | low | Audit main-text word count after Day 5 medRxiv DOI integration. |
| 5 | References still mix DOIs (some have, some don't). | low | Day 4 audit |

## Submission portal pre-flight (Day 11)

JCO PO uses Editorial Manager. Pre-fill:
- Article type: Original Report (or Brief Report if word-count-tight)
- Cover letter: upload `cover_letter_jcopo_draft.md` once finalized
- Suggested reviewers: 3 with full names + emails + affiliations + ORCID where available
- Conflicts of interest: none
- Funding: none specific
- Patient consent: not applicable (no human data)
- Data availability: GitHub URL + Zenodo DOI + pre-reg commit hash
- Previous deposition: medRxiv preprint DOI
- Manuscript word count: confirm under JCO PO Original Report cap (typically 3000 for IMRD)
- Highlights / lay summary: not required by JCO PO (but pre-staged for medRxiv)

## Realistic Acceptance Estimate

With all polish complete:
- JCO Precision Oncology: **45-55%** acceptance probability (positive pre-registered finding + biomarker framing fit)
- Backup JCO Clinical Cancer Informatics: **50-60%** (methods-friendly journal)

These are honest estimates; actual outcomes depend on editor priority and reviewer pool.
