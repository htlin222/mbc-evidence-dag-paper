# Round-4 Clinical Review (Final)

**Reviewer role.** Breast medical oncologist, ESMO mBC guideline panellist. Final-round adversarial check on whether the Round-3 G6 recoding (post-CDK46i → post-endo) is honestly reflected across the manuscript, whether the 16-NCT / 16-node corpus remains clinically defensible, and whether the residual framing meets the bar for preprint deposit.

**Scope.** `manuscript/main.tex`, `manuscript/discussion.tex`, `manuscript/supplement.tex`, `analysis/02_extract_eligibility.py`, `analysis/03_encode_guideline.py`, `data/processed/trials_structured.json`, `data/processed/esmo_decision_tree.json`, `data/results/efdpr.json`, `data/results/efdpr_sensitivity_no_g16.json`.

---

## A. Verification: G6 recoding is honest, but one prose paragraph is now stale

The Round-3 recoding (G6 `state: "post-CDK46i"` → `"post-endo"`) is reflected correctly in:
- `esmo_decision_tree.json` G6 (`state: "post-endo"`, `biomarker: "HR+/HER2-/AKTpath"`);
- `analysis/03_encode_guideline.py` lines 80–94 (with an explicit comment naming the Round-3 reviewer);
- `data/results/efdpr.json`: under strict tolerance G6 remains evidence-free (CAPItello-291's biomarker is `HR+/HER2-` only; AKTpath enters as a subgroup readout, which strict rejects), under liberal tolerance G6 is supported by CAPItello-291 via the AKT-pathway subgroup readout. Liberal evidence-free set is now {G7, G9, G13} → 3/16 = 0.1875 (= 0.19). Strict set remains {G5, G6, G7, G9, G13} → 5/16 = 0.3125 (= 0.31). The headline numbers in the Abstract (`main.tex:56`) and Results §3.2 (`main.tex:135`) match.
- Results §3.4 (`main.tex:169`) correctly labels G6 "the post-endo AKT-pathway node" and frames it as composition-only because CAPItello-291's AKT-pathway evidence is a registrational subgroup, not the ITT.
- Discussion §"Algorithm transparency" (`discussion.tex:14`) correctly names G6 "post-endo AKT-pathway".

**The recoding is therefore honestly reflected in the headline numbers, the encoding source files, the Results section, and one of the two Discussion paragraphs.**

**Ask 1 (BLOCKING for honest framing).** `discussion.tex:11` still reads *"…and of CAPItello-291 for **the post-CDK4/6i AKT-pathway node** (when CAPItello-291 enrolled a mixed pre/post-CDK4/6i population with only a subgroup readout)…"*. This is now factually inconsistent with the Round-3 recoding: G6 is encoded as `post-endo`, and the manuscript's own Results §3.4 (`main.tex:169`) explicitly calls G6 "the post-endo AKT-pathway node". A reader who reads only the Discussion will conclude that the framework codes ESMO's AKTi recommendation at post-CDK4/6i — which is precisely the over-narrow encoding the Round-3 reviewer asked to be removed. Edit `discussion.tex:11` to "the post-endo AKT-pathway node" so the Discussion matches the encoding and the Results. This is a one-token fix and should not be deferred to the post-preprint revision.

## B. Headline numbers and statistical claims are accurate

The Abstract Results sentence (`main.tex:56`) reports strict EFDPR 0.31 (CI 0.11–0.59), ESCAT 0.31, liberal 0.19 (CI 0.04–0.46), with $P=0.37/0.37/0.80$. These match `efdpr.json` exactly (Clopper-Pearson 0.1102–0.5866 → 0.11–0.59; 0.0405–0.4565 → 0.04–0.46; exact-binomial $P$ 0.3698/0.3698/0.8029). The 15-node sensitivity (`main.tex:172`) reports strict 0.33 (CI 0.12–0.62, $P=0.31$) and liberal 0.20 (CI 0.04–0.48, $P=0.76$); these match `efdpr_sensitivity_no_g16.json` (5/15 = 0.3333, Clopper-Pearson 0.1182–0.6162, $P=0.3135$; 3/15 = 0.2000, 0.0433–0.4809, $P=0.7639$). **No numerical errors detected.**

The Abstract clustering sentence (`main.tex:56`) now reads "post-CDK4/6i and adjacent biomarker-stratified positions (ESR1mut, AKT-pathway, post-CDK4/6i PIK3CAmut, post-CDK4/6i no-actionable-mutation, and the post-CDK4/6i+post-endo everolimus node)". The asymmetric labelling (only some entries carry the "post-CDK4/6i" prefix) is now honest: G6 (AKT-pathway) is the only one without the prefix, which is the correct consequence of the recoding. Round-3 ask #9 is partly resolved by the "and adjacent" hedge; an even tighter rephrase ("four post-CDK4/6i positions plus the post-endo AKT-pathway node") would be cleaner but is not blocking.

## C. Residual Round-3 asks the authors chose to defer (acceptable, but worth noting)

The following Round-3 asks remain unaddressed in Round 4. Each is documented or rhetorically softened rather than fixed, which is acceptable for a preprint:

- Round-3 ask #1 (`primary_endocrine_resistance` boolean on INAVO120) — deferred to v1.1 schema; acceptable.
- Round-3 ask #3 (BYLieve scope clause in Methods §2.1) — not added; the supplement only mentions EMBRACA, not BYLieve. **Ask 2 (MINOR):** add a half-sentence to Methods §2.1 or Discussion §"Limitations" explicitly excluding single-arm phase-2 expansion cohorts (BYLieve named) so the G7 "evidence-free" framing is not read as oversight.
- Round-3 ask #4 (G9 vs G13 operational distinction in Supplementary Table S3) — not added. The schema records `state: "post-CDK46i"` for G9 and `state: "post-CDK46i+post-endo"` for G13 but no `notes` field explains why a patient reaching G9 is not, by construction, also reaching G13. **Ask 3 (MINOR):** add one sentence to Supplementary Table S3 (or to a `notes` field in `esmo_decision_tree.json` on G9 and G13) clarifying the operational distinction; otherwise an ESMO panel reviewer will read the strict-EFDPR numerator as inflated by 1/16.
- Round-3 ask #5 (EMBRACA absence mentioned in Discussion limitations) — `discussion.tex:25–26` mentions only the six NCT corrections, not the EMBRACA scope choice. The supplement (`supplement.tex:126–129`) does name EMBRACA. **Ask 4 (MINOR):** add EMBRACA by name to `discussion.tex:25–26` so a main-text-only reader encounters the disclosure.
- Round-3 ask #6 (G3 temporal-precedence transparency) — partly addressed by `main.tex:135` ("G3 in this pilot is supported only by PALOMA-3 because MONARCH-2 (2017) and MONALEESA-3 (2018) post-date G3's encoded decision-tree year (2016)"). This is in the Results, not the Discussion as the Round-3 ask requested, but the disclosure is now somewhere a reader will encounter it. Resolved.
- Round-3 asks #7–#8 ("evidence-free" → "non-directly-state-matched" rephrase in Abstract Results and Key Objective; composition naming extended to EMERALD/G5) — not addressed. The phrase "evidence-free" still appears in the Abstract, Key Objective, Methods, Results, and Discussion. An ESMO panel reviewer will object to this label on the five flagged nodes, particularly G5/G6/G7 where ESMO does cite a pivotal trial that fails strict state-match only on the prior-line definition. **Ask 5 (MINOR but cumulatively load-bearing):** in the Abstract Results sentence (`main.tex:56`) and the Key Objective Knowledge-Generated box (`main.tex:67`), replace "evidence-free nodes" with "non-directly-state-matched nodes" or "nodes supported only by composition across non-overlapping pivotal trials". Retain the EFDPR acronym (the supplement defines it precisely). This is the same ask Round 1, 2, and 3 raised; I escalate it one final time because the manuscript is otherwise preprint-ready and this is the one phrase the panel will not let pass without comment.
- Round-3 ask #10 (15-node sensitivity raises EFDPR slightly, not lowers it) — not added to `main.tex:172`. The sensitivity is reported as preserving the primary finding, but the asymmetry (G16 is the only supported node whose removal raises EFDPR, which strengthens the headline) is not flagged. **Ask 6 (MINOR):** add to `main.tex:172` a half-sentence noting that G16 removal raises strict EFDPR from 0.31 to 0.33 — i.e. the sensitivity strengthens rather than weakens the primary finding.

## D. Residual clinically-substantive ask the authors should fix in print

**Ask 7 (MINOR).** The Abstract Results sentence (`main.tex:56`) names "AKT-pathway (ODI 0.67)" as a headline ODI finding. Round-2 ask #14 noted that this ODI is computed by comparing CAPItello-291 (AKT-pathway-altered tokens) with SOLAR-1 (PIK3CAmut-only tokens) — an apples-to-oranges comparison rather than a within-variable heterogeneity statistic, because SOLAR-1 did not enrol an AKT-pathway cohort. The number is technically defensible as "pairwise Jaccard between operational-token sets that any reader could compute from Table S4", but it is misleading as "AKT-pathway operational discordance". A one-line footnote on `tab_odi` (the table input file) noting that the AKT-pathway ODI is computed against SOLAR-1's PIK3CAmut tokens as the only available comparator would defuse this; alternatively, drop the AKT-pathway entry from the headline Abstract and keep it in Table S4 only. Either fix is acceptable; the current presentation is the only place in the manuscript where a panel reader will compute the number themselves and conclude it is not what it appears to be.

**Ask 8 (MINOR, preprint-compatible).** `analysis/02_extract_eligibility.py` has not added the `primary_endocrine_resistance` boolean (Round-2 ask #25, Round-3 ask #1). Acceptable for preprint; the schema deferral is disclosed in the supplement. No action required for v1.0; flag for v1.1.

---

## E. What I checked and accept as clean

- All 16 NCT identities verified clean against `data/raw/ctgov_trials.json` in Round 3; no further checks needed.
- All 16 trial encodings (prior_state, biomarker, drug_class, year_pc) clinically faithful (Round 3 verification stands).
- G6 recoding mechanically correct: strict EFDPR unchanged at 5/16 (biomarker fails without subgroup readout), liberal EFDPR moved from 4/16 = 0.25 to 3/16 = 0.1875 (CAPItello-291's AKT-pathway subgroup readout rescues G6 under liberal tolerance). The headline shift is honest.
- Six NCT corrections logged in `supplement.tex:108–121` and disclosed in Discussion §"Limitations". Adequate.
- Drug-class equivalence is now an explicit table, not a prefix rule (Round-2 ask #8 resolved); G15 correctly lists only INAVO120 as supporting.
- Three-tolerance grid is reported as a sensitivity, not as three confirmatory tests; Discussion §"Algorithm transparency" framing is appropriate.

---

## Summary

The Round-3 G6 recoding is honestly reflected in the encoding source files, the Results section, and one of the two Discussion paragraphs that name G6 — but `discussion.tex:11` still calls G6 "the post-CDK4/6i AKT-pathway node", which contradicts the encoding and the Results. That single inconsistency (Ask 1) is the only blocker for preprint deposit, and it is a one-line edit.

Residual asks 2–8 are minor polish items that any of the three preceding clinical reviews would have flagged and that an ESMO panel reviewer will probably re-raise; none of them blocks preprint deposit. The eight residual asks are bounded by the ≤8 limit.

**VERDICT: MINOR**
