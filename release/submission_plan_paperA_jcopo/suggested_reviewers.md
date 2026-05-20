# Suggested Reviewers — Paper A (JCO Precision Oncology)

> Candidates below are reasonable fits based on PubMed/Google Scholar
> footprint and JCO PO editorial-board membership. **You must perform a
> final conflict-of-interest screen** before entering at the portal,
> especially:
> 1. Cross-check against the 259-trial corpus (`data/processed/v3_combined_dag_edges.json`).
>    No suggested reviewer should be a named investigator on any corpus trial.
> 2. No co-authorship history with the corresponding author.
> 3. No recent grant collaboration.

> If you have stronger candidates from your network or the Taiwan/Asia
> oncology community, prefer those.

---

## Reviewer 1 — Clinical informatics / evidence synthesis perspective

**Name:** Travis J. Zack, MD, PhD (or alternative: any JCO CCI Associate Editor with computational-meta-research background)
**Affiliation:** Division of Hematology/Oncology, UCSF
**ORCID:** [look up]
**Email:** [look up at ucsf.edu]
**Why this reviewer:** Published on LLM-assisted clinical evidence synthesis and computational meta-research in oncology; would evaluate the dual-LLM-annotator + Cohen-kappa validation as a clinical-informatics reviewer rather than purely as a methodologist.
**Conflict screen:** Verify (a) not on any corpus trial; (b) no prior co-authorship.

## Reviewer 2 — HR+/HER2- mBC clinician

**Name:** Aditya Bardia, MD, MPH (or alternative: Erica L. Mayer at Dana-Farber, or Sara Tolaney as second choice — but Tolaney is on multiple corpus trials, double-check)
**Affiliation:** UCLA / Mass General previously
**ORCID:** [look up]
**Email:** [look up]
**Why this reviewer:** Known for HR+/HER2- post-CDK4/6i sequencing commentary including HER2-low and TROP2-ADC; would evaluate the clinical-actionability framing of the mBC findings.
**⚠️ Conflict screen:** Bardia is likely a co-investigator on TROPiCS-02 and possibly DESTINY-Breast trials in the corpus — VERIFY against `data/processed/v3_combined_dag_edges.json` before submitting. If conflicted, replace with:
- **Erica L. Mayer, MD, MPH** (Dana-Farber) — known for CDK4/6i sequencing commentary, less heavy on the pivotal-trial author list.
- Or **Lajos Pusztai, MD, DPhil** (Yale) — known for trial-design critique in mBC.

## Reviewer 3 — EGFR/ALK NSCLC clinician

**Name:** Charu Aggarwal, MD, MPH (or alternative: Jorge E. Gomez at Mount Sinai; or Hossein Borghaei at Fox Chase)
**Affiliation:** Abramson Cancer Center, University of Pennsylvania
**ORCID:** [look up]
**Email:** [look up]
**Why this reviewer:** Active in NSCLC EGFR-mutant clinical practice including post-osimertinib decision-making; would evaluate the clinical realism of the "evidence-free post-osimertinib" framing without being a primary trial PI on MARIPOSA-2 or HERTHENA-Lung01.
**⚠️ Conflict screen:** Verify she is NOT a named investigator on any of the v3 NSCLC pivotal corpus trials (FLAURA, MARIPOSA, MARIPOSA-2, HERTHENA-Lung01, TROPION-Lung01, AURA3, PROFILE 1014, ALEX, ALTA-1L, CROWN). Cross-check `data/processed/v3_combined_dag_edges.json` author lists.

---

## Alternates (use if any above declines or has conflict)

- **Mark G. Kris, MD** (MSK) — NSCLC senior commentator, would have broad-view perspective.
- **Hatim Husain, MD** (UCSD) — EGFR-mutant NSCLC; mostly commentary, less primary-trial-PI footprint.
- **Hope S. Rugo, MD** (UCSF, breast) — but heavily on PALOMA-3 / CAPItello-291 / TROPiCS-02 — likely conflicted.
- **Stephen V. Liu, MD** (Georgetown) — NSCLC; broad reviewer footprint.
- **William Gradishar, MD** (Northwestern) — NCCN Breast Guidelines panel chair — extremely relevant but may have institutional COI as a guideline-author.

## Reviewers we should ask the editor NOT to assign

- Anyone listed as PI / co-PI on a corpus trial. Specifically avoid:
  - PALOMA / MONALEESA / MONARCH series investigators
  - SOLAR-1, CAPItello-291, BYLieve, SERENA-6, EMBER-3 investigators
  - DESTINY-Breast04 / -06, TROPiCS-02 investigators
  - FLAURA / FLAURA2, MARIPOSA / MARIPOSA-2, HERTHENA-Lung01, TROPION-Lung01, PAPILLON, AURA3, ARCHER 1050 investigators
  - PROFILE 1014, ALEX, ALTA-1L, CROWN investigators

## How to verify a reviewer

```bash
# From the repo root:
python3 -c "
import json
edges = json.load(open('data/processed/v3_combined_dag_edges.json'))
name_query = 'Bardia'  # replace
for e in edges:
    # The trial_name field gives the corpus trial; cross-check on ClinicalTrials.gov NCT page
    if name_query.lower() in e.get('trial_name','').lower():
        print(f\"{e['nct_id']}  {e['trial_name']}\")
"
```

For author lists per trial, visit `https://clinicaltrials.gov/study/<NCT_ID>` and check the "Sponsors and Collaborators" + investigator-list fields.
