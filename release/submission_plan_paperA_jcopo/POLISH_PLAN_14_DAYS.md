# Paper A Polish Plan — 14 days to JCO Precision Oncology submission

**Target journal**: JCO Precision Oncology (IF ~5–6; fits biomarker-driven multi-tumor framing).
**Backup target**: JCO Clinical Cancer Informatics (IF ~6; same family, more methods-friendly).
**Day 0 = the day Paper B medRxiv preprint is submitted.**

---

## Week 1 — Foundation work (parallel with medRxiv processing)

### Day 1 — GitHub + Zenodo setup
- [ ] Push v3.0.0 to GitHub (per `submission_kit_paperB_medrxiv/ZENODO_INSTRUCTIONS.md`)
- [ ] Mint Zenodo DOI via webhook
- [ ] Submit Paper B to medRxiv (using `SUBMISSION_CHECKLIST.md`)
- [ ] Expect medRxiv staff queue 1–3 days; preprint DOI assigned at end of that window

### Day 2 — Author block + ORCID
- [ ] Register ORCID at orcid.org if not already (3 min)
- [ ] Update `manuscript/paper_A_clinical_v3.tex` author block:
  - Full legal name as preferred for indexing
  - Real ORCID iD (format `0000-0000-0000-XXXX`)
  - Real institutional affiliation OR "Independent Researcher"
  - Full postal address (JCO PO portal asks for this)
- [ ] Update same fields in references and signature lines

### Day 3 — Figure polish for Paper A
- [ ] Re-open `figures/v3_fig1_forest.pdf` and confirm legibility at print size
- [ ] Re-open `figures/v3_fig2_per_node.pdf` and confirm G/N label readability
- [ ] Re-open `figures/v3_fig3_trajectory.pdf` and confirm log-scale axis labels visible
- [ ] Generate Figure 4 if reviewer cycle suggests one (per-tumor concordance grid mBC×NSCLC side-by-side)
- [ ] Adjust figure widths in `paper_A_clinical_v3.tex` if any are too small/large

### Day 4 — Reference completeness audit
- [ ] Audit every `\citep{...}` in `paper_A_clinical_v3.tex` against `references.bib`
- [ ] Add canonical primary publications for any cited trial not yet in bib (esp. FLAURA, MARIPOSA, MARIPOSA-2, ALEX, ALTA-1L, CROWN, AURA3, HERTHENA-Lung01, TROPION-Lung01)
- [ ] Verify all DOIs resolve (use bibtex with `doi` field; spot-check 5–10)
- [ ] Convert bib style to AMA if JCO PO author instructions require (vancouver.bst is acceptable as close-equivalent)

### Day 5 — Update with medRxiv preprint DOI
- [ ] When Paper B's medRxiv DOI is assigned, add it to Paper A as a self-citation in Methods §2 ("[A companion methods manuscript describing the framework has been deposited as medRxiv 10.1101/XXX]")
- [ ] Add `@article{lin2026medrxiv, ...}` entry to `references.bib`
- [ ] Recompile `paper_A_clinical_v3.tex`

### Day 6 — Suggested reviewers research
- [ ] Identify 3 plausible reviewers with no conflict:
  - One clinical informaticist (e.g., someone who has published in JCO CCI on evidence synthesis / decision support)
  - One mBC clinician (e.g., a recent SOLAR-1 or CAPItello-291 commentator who is NOT a trial author of those)
  - One NSCLC clinician (e.g., a recent FLAURA / MARIPOSA commentator)
- [ ] Note for each: name, affiliation, email, ORCID, one-line "no conflict" rationale
- [ ] Avoid reviewers who are co-authors on any trial in our corpus

### Day 7 — Draft JCO PO cover letter
- [ ] Use `cover_letter_jcopo_draft.md` (already pre-staged in this kit) as starting point
- [ ] Update with:
  - Real date
  - Real editor name (look up current JCO PO Editor-in-Chief)
  - Real Paper B medRxiv DOI
  - Real ORCID
  - Real suggested reviewers
- [ ] Verify cover-letter title matches paper title exactly

---

## Week 2 — Submission readiness

### Day 8 — Internal soft review (one more reviewer pass)
- [ ] Re-read Paper A end-to-end as a fresh reader would
- [ ] Check: does the abstract conclusion match the Results conclusion?
- [ ] Check: does every figure caption stand alone (interpretable without re-reading main text)?
- [ ] Check: every claim in Discussion has a Result-section anchor

### Day 9 — Statistical reporting check
- [ ] Confirm all P-values to 4 decimal places consistent across abstract/KO box/results/discussion (P=0.023 throughout)
- [ ] Confirm Clopper-Pearson CI bounds match `v3_pooled_efdpr.json` exactly
- [ ] Confirm tumor-stratified sensitivity numbers match the JSON
- [ ] Add one sentence to Limitations about the ESCAT/liberal P=0.10 explicitly

### Day 10 — Supplementary preparation
- [ ] Create `supplement_paper_A.tex`:
  - Table S1: PRISMA-2020 style reporting checklist (with graph-encoding addendum)
  - Table S2: per-trial structured-extraction excerpts (NSCLC + mBC, n=261)
  - Table S3: per-node ESMO/ASCO/NCCN decision tree (n=49)
  - Table S4: adjudication rules log
- [ ] Compile as separate PDF
- [ ] DOCX version via pandoc

### Day 11 — JCO PO portal pre-flight
- [ ] Visit JCO PO submission portal (Editorial Manager) and create author account
- [ ] Pre-fill author info (name, ORCID, affiliation, full address, conflicts, funding)
- [ ] Confirm article type "Original Report" or "Brief Report" (under 1500 words alt format)
- [ ] Note any field that doesn't have a corresponding paper-A section; add to draft if needed

### Day 12 — File format finalization
- [ ] Recompile final `paper_A_clinical_v3.tex` → `paper_A_clinical_v3.0.1.pdf`
- [ ] Recompile final `supplement_paper_A.tex` → `supplement_paper_A_v3.0.1.pdf`
- [ ] Generate DOCX: `pandoc paper_A_clinical_v3.tex --bibliography=references.bib --citeproc -o paper_A_clinical.docx`
- [ ] Verify all figures embed correctly in DOCX
- [ ] Save figures as separate high-res files (PDF + 600 DPI PNG) for portal upload

### Day 13 — Final check + commit + tag
- [ ] Confirm all placeholders replaced (ORCID, affiliation, GitHub, Zenodo, medRxiv DOI)
- [ ] `git tag -fa v3.0.1` with submission-ready commit
- [ ] Update RELEASE_NOTES_v3.0.1.md with submission status
- [ ] One final read-through by a friend or colleague if available (24h turnaround)

### Day 14 — Submission
- [ ] Log in to JCO PO Editorial Manager
- [ ] Upload PDF + DOCX of main manuscript
- [ ] Upload PDF + DOCX of supplement
- [ ] Paste abstract into portal field
- [ ] Enter keywords
- [ ] Upload cover letter
- [ ] List 3 suggested reviewers
- [ ] List conflicts (none)
- [ ] Confirm pre-registration commit hash and Zenodo DOI in data-availability portal field
- [ ] Reference medRxiv preprint DOI in "Previously deposited" field
- [ ] **Click submit**

---

## After submission

Expected timeline:
- Editorial screen: 1–2 weeks (could be desk-reject if article-type mismatch or out-of-scope)
- Peer review: 4–8 weeks
- First decision: typically Major Revision (this is normal); plan for 1–2 revision rounds
- Acceptance: typically 4–6 months from initial submission for accepted papers at this tier

If desk-rejected:
- Reformat lightly for JCO Clinical Cancer Informatics (backup target) and resubmit same week
- Don't lose the preprint citation momentum

---

## Soft deadline tracking

| Day | Date (fill in) | Done? |
|---|---|---|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |
| 6 | | |
| 7 | | |
| 8 | | |
| 9 | | |
| 10 | | |
| 11 | | |
| 12 | | |
| 13 | | |
| 14 (submit) | | |

If any day slips by >2 calendar days, re-plan the rest. Don't let the plan become a rolling deadline that defeats itself.
