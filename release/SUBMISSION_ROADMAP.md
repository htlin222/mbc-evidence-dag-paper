# Submission Roadmap (single-page)

Two papers, two journals, two-stage timeline.

## TODAY (start)

### 30 minutes: Paper B medRxiv preprint submission

1. Read `release/submission_kit_paperB_medrxiv/SUBMISSION_CHECKLIST.md`
2. Push v3.0.0 to GitHub (see `ZENODO_INSTRUCTIONS.md`)
3. Wait for Zenodo to mint DOI (~5 min)
4. Replace 3 placeholders in `paper_B_methods_v3.tex` and recompile
5. Submit at https://www.medrxiv.org/submit-a-manuscript
6. Expect 1–3 day medRxiv staff queue

## DAYS 1–14: Paper A polish

Detailed day-by-day in `release/submission_plan_paperA_jcopo/POLISH_PLAN_14_DAYS.md`.

Key milestones:
- Day 1: GitHub push + Zenodo + medRxiv submission of B
- Day 5: Paper B medRxiv DOI arrives; add to Paper A
- Day 7: Finalize JCO PO cover letter (`cover_letter_jcopo_draft.md`)
- Day 10: Compile Paper A supplement
- Day 14: Submit Paper A to JCO Precision Oncology

## TIMELINE CHART

```
Day  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15... 28 29...
Pap.B[●  ▒ ▒ ▒ ▒ ●  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─]
                     │              (medRxiv preprint live)
                     │
Pap.A[ ] [author block][figures][refs][medRxiv DOI add][reviewers][cover][.... internal review .... supplement .... submit▼]
                                                                                                                       │
                                                                                                            JCO PO submission

Legend:
● = action day
▒ = waiting day (medRxiv queue)
─ = preprint live and citable
▼ = formal journal submission
```

## RISK MITIGATION

| Risk | Mitigation |
|---|---|
| Paper B medRxiv endorsement delays | Submit Paper B Day 1; if endorsement needed, queue for endorser early |
| Zenodo webhook fails | Manual upload to zenodo.org as fallback (~15 min, same result) |
| Paper A JCO PO desk-reject | Reformat for JCO CCI within 1 week, resubmit with preprint citation maintained |
| Day-slipping | If any day slips >2 days, re-plan; don't let plan rot |

## SUCCESS METRICS (mid-term)

| Metric | Target by Day 14 |
|---|---|
| Paper B medRxiv preprint live with DOI | ✓ |
| Paper A submitted to JCO PO | ✓ |
| GitHub repo public with v3.0.0 tag | ✓ |
| Zenodo DOI minted | ✓ |
| Author block complete with real ORCID and affiliation | ✓ |
| 3 suggested reviewers identified | ✓ |
| Supplement (Tables S1–S4) compiled | ✓ |

## SUCCESS METRICS (long-term, 6 months)

| Metric | Target |
|---|---|
| Paper B accepted at Research Synthesis Methods | 40-55% probability |
| Paper A accepted at JCO PO (or JCO CCI as backup) | 45-60% probability |
| At least one paper accepted | 70-80% probability |
| Both papers accepted | 25-35% probability |

If both get rejected: re-target to **eClinicalMedicine** (Paper A) and **BMC Medical Research Methodology** (Paper B) within 1 month.

---

## File index

| File | Purpose |
|---|---|
| `submission_kit_paperB_medrxiv/SUBMISSION_CHECKLIST.md` | Step-by-step medRxiv |
| `submission_kit_paperB_medrxiv/medrxiv_metadata.md` | Copy-paste fields for portal |
| `submission_kit_paperB_medrxiv/cover_letter_medrxiv.md` | Optional cover letter |
| `submission_kit_paperB_medrxiv/AUDIT_REPORT.md` | Paper B readiness audit |
| `submission_kit_paperB_medrxiv/ZENODO_INSTRUCTIONS.md` | GitHub→Zenodo setup |
| `submission_kit_paperB_medrxiv/paper_B_methods.pdf` | The PDF to upload |
| `submission_kit_paperB_medrxiv/paper_B_methods.docx` | The DOCX to upload |
| `submission_plan_paperA_jcopo/POLISH_PLAN_14_DAYS.md` | Day-by-day Paper A work plan |
| `submission_plan_paperA_jcopo/cover_letter_jcopo_draft.md` | JCO PO cover-letter draft |
| `submission_plan_paperA_jcopo/AUDIT_REPORT.md` | Paper A readiness audit |
| `SUBMISSION_ROADMAP.md` | THIS file |

Open `SUBMISSION_ROADMAP.md` first; everything else linked from there.
