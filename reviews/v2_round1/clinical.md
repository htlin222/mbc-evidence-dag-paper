# Adversarial Clinical Review — v2 Round 1

**Reviewer.** Breast medical oncologist; ESMO HR+/HER2- mBC guideline panel member.
**Scope of review.** `manuscript/main_v2.tex`, `manuscript/discussion_v2.tex`, `analysis/v2_07_build_dag.py`, `analysis/v2_08_extend_guideline.py`, `data/processed/v2_extraction_final.json`, `data/processed/v2_decision_tree.json`, `data/results/v2_efdpr.json`.

**Bottom line up front.** The pilot-to-production scaling is real, the systematic search is reproducible, the dual-annotator pipeline is a respectable defence against "LLM-hallucination" critique, and the headline result (strict EFDPR 0.60, P=0.0002) is statistically valid. **But the 9 new ASCO/NCCN-unique nodes (G17, G19–G26) are where the manuscript is most fragile.** Several are duplicates of existing nodes, several are encoded in a way that mechanically forces "evidence-free," and at least two pivotal trials that *do* directly support new nodes are sitting unprocessed in the raw systematic corpus. I can sign on to the framework and the headline conclusion, but not without surgical fixes to the G17–G26 set and a few clinically-loaded encoding choices in G5/G6/G7/G13/G26.

---

## A. Audit of the 9 ASCO/NCCN-unique nodes (G17, G19–G26)

A clinical reviewer reads `v2_08_extend_guideline.py` as a "what did the authors add, and are these real guideline-tree positions?" question. My verdict on each:

### A1. G17 — first-line + visceral-crisis → single-agent chemotherapy. **Defensible but mis-cited.**
ASCO 2022 and NCCN both carve out a visceral-crisis exception in HR+/HER2- 1L (ESMO 2024 §5.3 also does). The recommendation itself is real. **Problem:** the manuscript counts G17 as evidence-free, but RIGHT Choice (NCT03839823, primary completion 2022) is in the corpus, randomised ribociclib+ET vs combination chemotherapy specifically in symptomatic visceral disease / impending visceral crisis, and demonstrated CDK4/6i+ET was non-inferior. The reasonable guideline reading post-RIGHT Choice is that **chemotherapy is no longer the unique 1L visceral-crisis recommendation** — CDK4/6i+ET is now equipoise. If the panel intent is "rapid response required," RIGHT Choice supports the displaced recommendation (CDK4/6i+ET), not the chemotherapy node. G17 as currently encoded therefore measures the gap between an outdated 2022 recommendation and a 2022 trial. Either (a) re-encode G17 to allow CDK4/6i+ET (with RIGHT Choice as supporting edge → no longer evidence-free), or (b) keep the chemotherapy encoding and **explicitly note** in the heatmap that G17 is evidence-free because the supporting trial pushed against the recommendation.

### A2. G19 — post-endo + ESR1mut → SERD oral + CDK4/6i. **Duplicate of G5 plus questionable encoding.**
The intent is the SERENA-6 indication (1L emergent ESR1mut on AI+CDK4/6i, ctDNA-guided switch to camizestrant+CDK4/6i). But:
- The state is encoded as `post-endo`. SERENA-6 patients are **on** AI+CDK4/6i in 1L for the metastatic setting, ctDNA flags ESR1 emergence, and they switch *before* RECIST progression. They are not "post-endo" in the classical sense — they are intra-1L with biomarker-detected resistance.
- SERENA-6 (NCT04964934) is in the corpus with `post_endo=True, post_cdk46i=True, ESR1mut=True, drug_class="SERD oral + CDK4/6i"`. So the *trial extraction* matches the biomarker but its prior-state token set is `post-endo+post-CDK46i`, which under strict state-superset *should* cover G19's `post-endo`. It does not, because the strict tolerance also requires the drug-class match — which it does — so the trial would in fact support G19 if the encoding were consistent. **Action:** verify why G19 reports zero support when SERENA-6 satisfies all four concordance predicates under strict (G19 cited_trials list is empty in `v2_decision_tree.json` line 286, yet `v2_efdpr.json` line 75 confirms G19 is evidence-free — this is either a bug in the concordance algorithm or a deliberate exclusion that needs to be disclosed).
- Biologically G19 is essentially the *same* clinical decision as G5 (post-endo, ESR1mut → oral SERD-containing regimen). G5 is monotherapy elacestrant; G19 is camizestrant+CDK4/6i. The two-node split is defensible *if* the manuscript explicitly says "post-progression vs early-switch" — but the current G5 vs G19 encoding doesn't distinguish those. Recommend either merging or re-stating G19 as `first-line + on-CDK46i + ESR1mut-emergent`.

### A3. G20 — post-endo + post-CDK4/6i → SG. **Real, defensible, supported.**
This is the TROPiCS-02 indication, and the corpus supports it (NCT03901339). Fine.

### A4. G21 — post-chemo + HER2-low → Dato-DXd or T-DXd. **Real, but encoded incompletely.**
TROPION-Breast01 (NCT05104866) enrolled HR+/HER2- patients independent of HER2-low status; the extraction correctly does **not** mark `her2_low=True`. So G21's biomarker requirement of `HER2-low` is not satisfied by TROPION-Breast01 even though TROPION-Breast01 is the cited trial. Two paths: (a) drop `HER2-low` from G21's biomarker (Dato-DXd does not require HER2-low) — this is what NCCN actually says, **HER2-low is required for T-DXd, not for Dato-DXd**; (b) split into G21a (Dato-DXd, no HER2-low requirement, supported by TROPION-Breast01) and G21b (T-DXd, HER2-low required, supported by DESTINY-Breast06/04 which are already in the corpus). The current encoding mechanically forces evidence-free because it imposes the T-DXd biomarker requirement on a Dato-DXd recommendation. This is a real clinical error.

### A5. G22 — bone-only indolent, single-agent endocrine. **Real but anachronistic.**
Single-agent endocrine for indolent HR+/HER2- mBC is real ESMO/ASCO/NCCN low-disease-burden guidance, but the registrational trials supporting it (TARGET, FACT, FIRST, FALCON, P024, ATAC, BIG 1-98) all predate 2013 and were filtered out by the v2.1 amendment's start-year filter. So G22 is **structurally evidence-free as an artefact of the start-year filter, not as a real evidence gap.** This must be disclosed in the Results section as part of the EFDPR=0.60 narrative. The manuscript's Discussion §3 hand-waves it as "populations rarely enrolled in modern phase 3 trials" — that is a euphemism for "we filtered out the trials that support this." Pre-2013-completion FALCON (NCT01602380) directly supports G22 (fulvestrant > anastrozole 1L in HR+/HER2- mBC, primary completion 2017 — actually within the start-year window). I'd ask the authors to re-check why FALCON is not in the corpus.

### A6. G23 — post-endo + post-CDK4/6i + post-chemo → SG. **Duplicate of G20+G14 stack.**
TROPiCS-02 supports both G20 (`post-endo+post-CDK46i`) and G23 (`post-endo+post-CDK46i+post-chemo`). TROPiCS-02 patients had 2–4 prior chemo regimens, so they are *strictly* in G23's state. G23 is therefore a tighter sub-population of G20 with the same recommendation. **Either merge (the guideline tree shouldn't distinguish them — both ASCO and NCCN cite SG once) or justify the split.** As written, G23 is double-counting in the EFDPR denominator.

### A7. G24 — first-line + indolent + post-menopausal → endocrine monotherapy. **Pure duplicate of G22.**
G22 already encodes "first-line + indolent → endocrine alone, HR+/HER2-." G24 adds `+post-menopausal` and the same recommendation. Why are these two nodes? This looks like padding to inflate the denominator. If the panel actually distinguishes pre- vs post-menopausal indolent disease (which they do — pre-menopausal requires OFS), then G22 should be re-encoded as pre-menopausal and G24 kept as post-menopausal, but the current G22 has no menopausal token. **Recommend dropping G24 and re-tagging G22 as the canonical indolent-disease post-menopausal endocrine-alone node.** This shaves 1 node and 1 evidence-free node off the EFDPR; new EFDPR would be 14/24 = 0.583, still rejects (P≈0.0006), so the headline survives.

### A8. G25 — post-CDK4/6i + post-endo + post-mTORi → chemotherapy salvage. **Real evidence gap, encoded correctly.**
Genuinely undefined territory; ASCO 2022 living guideline does acknowledge this is a clinical option without trial backing. Honest evidence-free. Keep.

### A9. G26 — post-CDK4/6i + AKTpath → AKTi + fulvestrant. **Encoded to force evidence-free.**
This is the most problematic of the new nodes. CAPItello-291 (NCT04305496) **was specifically designed in the post-CDK4/6i era and enrolled ~69% post-CDK4/6i patients** (Turner et al. NEJM 2023; pre-specified subgroup analysis showed PFS benefit retained in post-CDK4/6i subgroup, HR 0.55). Encoding the trial as `post_endo=True, post_cdk46i=None` in v2_extraction_final.json (and downstream as `post-endo` only, not `post-endo+post-CDK46i`) makes CAPItello-291 fail the state-superset check against G26's required `post-CDK46i` token. **This is a direct extraction error.** The fix is to mark CAPItello-291 as `post_cdk46i=True` (it was strongly enriched, registrationally subgrouped, and the FDA label specifically permits prior CDK4/6i). Then G26 would have ≥1 supporting edge under strict tolerance, dropping the EFDPR by one node. The same critique applies to the encoding of G6 vs G26 (see §C below).

### Summary of A1–A9:
**Defensible:** G20, G25.
**Real but mis-encoded (fixable):** G17, G21, G22, G26.
**Duplicate / padding:** G23 (sub-population of G20), G24 (duplicate of G22).
**Same-decision-different-trial-arm:** G19 (sub-encoding of G5 ESR1mut decision).

If the authors fix the duplicates and the four encoding errors, the EFDPR will drop from 0.60 to roughly **0.48 (12/25 if you keep all 25, or 11/22 if you de-duplicate G19/G23/G24).** Even at 0.48 (or 0.50 on 22 nodes) the test rejects at α=0.05 (P≈0.013), so the **headline conclusion survives a fully honest re-encoding** — but the 0.60 number is inflated by ~7 percentage points by avoidable encoding choices. *That is the central clinical concern of this review.*

---

## B. Trial-extraction spot-check (8 trials)

I checked 8 trials against their canonical primary publication:

| # | NCT | Trial | Drug class | Prior state | Biomarker | Verdict |
|---|---|---|---|---|---|---|
| 1 | NCT01740427 | PALOMA-2 | CDK4/6i+AI | first-line (DFI>12mo from adjuvant AI) | HR+, HER2- | **OK** |
| 2 | NCT02000622 | OlympiAD | PARPi (olaparib) | post-endo; HR+ subgroup required prior ET; TNBC also enrolled | HER2-, gBRCAmut, HR=mixed | **OK** (note: hr_pos=null because the trial is HER2-/gBRCAmut, not HR+-specific — correct) |
| 3 | NCT02437318 | SOLAR-1 | PI3Ki+fulv | post-AI/post-endo, PIK3CAmut cohort | HR+/HER2-/PIK3CAmut | **OK** |
| 4 | NCT03734029 | DESTINY-Breast04 | T-DXd | post-chemo (1–2 prior in mBC), post-endo if HR+ | HER2-low, mixed HR+/HR- | **OK**; but `hr_pos=null` is technically right (because TNBC HR-low were also eligible) — strict tolerance against G12 requires HR+, which is why G12 fails. *Recommendation:* add the HR+ subgroup readout as a separate supporting edge (currently `subgroup_readouts=['HR+_subgroup','HR-_subgroup']` exists in the extraction but the concordance algorithm doesn't appear to use it for supporting G12). This may be the single largest unforced error in the concordance algorithm. **Verify behaviour.** |
| 5 | NCT04494425 | DESTINY-Breast06 | T-DXd | post-endo+CDK4/6i (no prior chemo for mBC) | HR+/HER2-/HER2-low (and ultralow) | **OK**; but missing `post_cdk46i=True` flag despite the trial requiring "progression within 6 mo of 1L ET+CDK4/6i" for one arm. This is a clear extraction omission. Patients with ≥2 prior endocrine lines are eligible *without* prior CDK4/6i, so the trial population is mixed — but the post-CDK4/6i arm is the registrational one. *Either set the flag or document the choice.* |
| 6 | NCT04305496 | CAPItello-291 | AKTi+fulv | "post-endo (AI), endocrine-resistance window 12mo, post-CDK4/6i permitted and accounted for in stratification" | HR+/HER2-/AKTpath | **WRONG.** `post_cdk46i=None` understates the trial. ~69% of enrolled patients had prior CDK4/6i; the trial design explicitly stratifies on prior CDK4/6i use; the primary biomarker-subgroup PFS readout is reported separately for the post-CDK4/6i subset. Should be `post_cdk46i=True`. *This is the single most consequential mis-coding because it directly produces the G26 zero.* |
| 7 | NCT03778931 | EMERALD | SERD oral | post-endo, post-CDK4/6i, ESR1mut subgroup | HR+/HER2-/ESR1mut | **OK** |
| 8 | NCT05169567 | postMONARCH | CDK4/6i+fulv (post-CDK4/6i) | post-endo, post-CDK4/6i, no prior mBC chemo | HR+/HER2- | **OK** |

**Additional cross-check (TROPION-Breast01, NCT05104866).** Extraction lists `her2_low=null`. Correct (TROPION-Breast01 did not stratify on HER2-low). The encoding error is on G21's biomarker, not on the trial extraction.

**Bottom line on extraction quality.** The 80-trial corpus is broadly accurate. The error rate on my 8-trial sample is 2/8 with clinically consequential mis-coding (DESTINY-Breast06 missing `post_cdk46i`; CAPItello-291 missing `post_cdk46i`), with the latter directly producing one of the headline evidence-free nodes (G26). The mean post-adjudication κ of 0.875 is plausible at the schema-field level, but it does not capture this class of "field present and well-defined but missed because eligibility text is ambiguous on CDK4/6i" error. *Recommend a 5-trial focused re-extraction of CAPItello-291, DESTINY-Breast06, RIGHT Choice, EMBER-3, TROPiCS-02 against the published primary papers (not just the eligibility text).*

---

## C. Missing pivotal trials

I checked for trials that should support otherwise-evidence-free nodes:

### C1. BYLieve (NCT03056755). **Missing — the systematic search found it, but it's not in the final 80.**
BYLieve is the explicit post-CDK4/6i PIK3CAmut PI3Ki trial. The systematic v2 search captured it (it appears in `data/raw/ctgov_systematic_v2.json` with full citation). It would directly support **G7** (post-CDK4/6i + PIK3CAmut → PI3Ki) — currently the largest evidence-free claim in the post-CDK4/6i biomarker cluster. Why was it excluded from the final 80? Phase 2 non-comparative (n=349 across cohorts) likely tripped the n≥200 threshold (cohort A alone was 127; total study enrolled 349). If the filter is per-cohort, this needs review; if per-study, BYLieve is in. **Action:** add BYLieve and re-run concordance. This single addition would shift G7 from evidence-free to supported and would drop the headline EFDPR by 1 node.

### C2. BOLERO-2 (NCT00863655). **Filtered out by start year (2009 start, completion 2014).**
BOLERO-2 is *the* registrational everolimus+exemestane trial post-NSAI, and it directly supports **G9** (post-CDK4/6i + no-actionable → everolimus+exemestane) and **G13** (post-CDK4/6i+post-endo → everolimus+exemestane). The v2.1 amendment's "start year ≥ 2013" filter excludes it. **This is the same artefact as with FALCON (§A5)**: the filter is hostile to historical pivotal trials. The honest framing is that those two nodes are evidence-free *under the v2.1 start-year filter*, not in absolute terms. Disclose explicitly, or add a sensitivity analysis that drops the start-year filter. (Either way, the manuscript's claim that post-CDK4/6i everolimus is unsupported is misleading — BOLERO-2 enrolled NSAI-failed patients, which is the closest historical analog to post-CDK4/6i, even though it predates the modern era.)

### C3. DESTINY-Breast09 (NCT04784715). **Out of scope (HER2-positive 1L).**
This is the T-DXd 1L HER2+ trial. Out of scope for HR+/HER2- mBC. Not missing; correct to exclude.

### C4. HER2CLIMB-04 (NCT04539306). **Out of scope (HER2-positive).**
Same. Correctly excluded.

### C5. SERENA-6 (NCT04964934). **In corpus but not credited to G19.** See §A2.

### C6. INAVO121 (NCT05646862). **In corpus.** Supports G7 directly when it reads out (primary completion 2026). Currently future-dated relative to G7's 2022 introduction year, so correctly excluded under temporal precedence. Fine.

### C7. VIKTORIA-1 (NCT05501886). **In corpus, primary completion 2026.** Same temporal-precedence reasoning as INAVO121. Fine.

### C8. EMBER-3 (NCT04975308). **In corpus.** Imlunestrant ± abemaciclib post-AI±CDK4/6i, ESR1mut subgroup co-primary. Should support G5 under liberal (it does — confirmed). Could also support G19 under a reasonable post-endo+ESR1mut+SERD reading. Verify.

**Net effect of C1+C2 alone:** add BYLieve to support G7, add BOLERO-2 to support G9 and G13 (or document the start-year filter rationale). Even with both additions, the strict EFDPR would be ~11/25 = 0.44, P≈0.027, rejects.

---

## D. Fairness of framing toward guideline panels

The headline "P=0.0002, REJECTS H0" sounds damning. As a panel member, my honest reaction is mixed:

**What I would not protest:**
- The framework's central insight is correct. Guidelines *do* compose across non-overlapping pivotal trials, and that composition is rarely audited at production scale.
- The pre-registered exact-binomial test is appropriate, and a 0.25 threshold is not unreasonable. (I would have argued for 0.20 to be more conservative against the panel; the authors chose 0.25, which is panel-friendly.)
- The discussion paragraph on "composition-across-non-overlap is routine and often unavoidable" is the right tone. It does not accuse the panel of malpractice.

**What I would protest:**
- The headline narrative "the pre-registered hypothesis that more than one quarter of HR+/HER2- mBC guideline decision nodes lack a directly-supporting trial chain is confirmed" elides that the panel has *never* claimed those nodes have direct-trial-chain support. ESMO grading explicitly distinguishes Level I-A (direct phase 3) from Level II-B (extrapolation), and panels assign II-B precisely when composition is required. The manuscript should acknowledge that **EFDPR captures the I-A/II-A vs II-B/II-C split, not a quality failure of the panel.** A pre-specified breakdown of evidence-free nodes by their assigned grade would defuse most of the panel objection. (Right now `recommended_classes[].grade` is in the data but never reported in the manuscript.) **Action:** add a 1-row table or a stacked bar showing EFDPR stratified by the panel's own evidence grade. Predict that I-A nodes have low EFDPR and II-B/II-C nodes have high EFDPR — that would *confirm the panel's self-assessment rather than contradict it.*
- The Discussion paragraph "Three caveats" mentions "a finer-grained encoding would yield more nodes and would likely shift the EFDPR up." This is mathematically true but is a one-way escape hatch — the more honest framing is that the *interpretive degree of freedom in encoding granularity is large enough to swing the EFDPR by ±15 percentage points*. The G24-G22, G23-G20, G19-G5 duplicate issues (§A) are direct examples.
- The 16→25 node expansion is presented as adding ASCO/NCCN coverage, but 4 of the 9 new nodes are evidence-free by construction of how the new node was encoded (G17, G21, G24, G26 per §A). That is a quiet form of denominator inflation. **The pre-registration should specify the node-encoding rules before the encoding is done.** The current `v2_08_extend_guideline.py` is committed after the pre-reg (commit 079b540 was the amendment), but the *node-by-node encoding decisions* are not pre-specified — they are author-discretionary. A reviewer should ask: were these encoding choices made before or after seeing which trials would support which nodes? Disclose.

**Net.** A fair reading is "EFDPR=0.60 measures the gap between guideline-recommended decisions and direct-trial-chain support, under strict state-superset matching and the authors' encoding choices; under fully honest encoding the EFDPR is ~0.44–0.48, still significantly above 0.25." The headline survives. The "REJECTS H0" framing should be softened in the abstract from "the pre-registered hypothesis is confirmed" to "the pre-registered test rejects under the registered encoding."

---

## E. Honest characterization of post-CDK4/6i nodes (G5, G6, G7, G9, G13)

This is where the clinical reviewer reads most carefully.

- **G5 (post-CDK4/6i + ESR1mut → SERD oral):** EMERALD is the correct supporting trial. Encoding is honest. Fine.

- **G6 (post-endo + AKTpath → AKTi+fulv):** The v1-round-3 decision to move G6 from "post-CDK4/6i" to "post-endo" is **defensible only because CAPItello-291's official eligibility criterion is post-AI (not post-CDK4/6i)**. The trial *enrolled* heavily post-CDK4/6i but did not *require* it. So the strict reading is that the panel-level recommendation is post-endo (i.e., after any prior endocrine), and CAPItello-291's required state is post-AI ⊆ post-endo. G6's "post-endo" encoding is correct. **But G26 then duplicates G6 with a `post-CDK46i` state.** That duplication is the problem (§A9), not G6 itself.

- **G7 (post-CDK4/6i + PIK3CAmut → PI3Ki):** Encoded honestly *as a strict state requirement*. SOLAR-1 is post-AI without required prior CDK4/6i, so it doesn't support G7 strictly. BYLieve is the trial that does, and it is missing from the corpus (§C1). **Fix the corpus, not the encoding.**

- **G9 (post-CDK4/6i + no-actionable → everolimus+exemestane or chemotherapy):** "no-actionable" is a synthetic biomarker token meaning "PIK3CAwt + ESR1wt + AKTpath-negative + HER2-zero." There is no trial that explicitly enrolled this combinatorial population. BOLERO-2 and BOLERO-6 (and EVEREXES) are the closest analogues — all enrolled "post-NSAI without biomarker selection," which is biologically equivalent to "post-endo without actionable mutations" but not formally identical. The current strict-tolerance algorithm correctly fails. *This is one of the few nodes where "evidence-free" is genuinely accurate even after corpus fixes.* Keep.

- **G13 (post-CDK4/6i + post-endo → everolimus+exemestane):** BOLERO-2/BOLERO-6 again. Same critique as G9 — pre-CDK4/6i era trials are not in the corpus due to the start-year filter. *Disclose, do not silently mark evidence-free.*

**Composite verdict on post-CDK4/6i nodes:** the encoding is mostly honest, but the corpus is incomplete (BYLieve, BOLERO-2 missing) and the CAPItello-291 extraction is wrong on the post-CDK4/6i flag. Fix those three issues and the post-CDK4/6i cluster goes from 5 evidence-free nodes (G5✓ supported, G6✓ supported, G7 ✗, G9 ✗, G13 ✗) under strict — actually 3 unsupported (G7, G9, G13) — to 2 unsupported (G9, G13 under start-year filter; G13 arguably supported by BOLERO-2 if added). Honest count for the cluster is ~2, not 3.

---

## F. Concrete asks (12)

1. **Re-extract CAPItello-291 (NCT04305496) with `post_cdk46i=True`.** The trial stratified on it; the registrational subgroup is post-CDK4/6i. This is a clinical-fidelity error that mechanically generates G26's evidence-free status.

2. **Re-extract DESTINY-Breast06 (NCT04494425) with `post_cdk46i=True`** for the cohort progressing after 1L ET+CDK4/6i. Currently `None` despite the eligibility text explicitly requiring it for that arm.

3. **Verify the concordance algorithm's handling of subgroup_readouts.** DESTINY-Breast04 has `subgroup_readouts=['HR+_subgroup','HR-_subgroup']` but `hr_pos=null`, and G12 requires HR+. Under strict tolerance, should the registrational pre-specified HR+ subgroup count as direct evidence? The current code appears to say no. Document the choice in Methods. If subgroup readouts count under ESCAT-aligned, this should rescue G12 — currently it does not.

4. **Add BYLieve (NCT03056755) to the corpus** or document why it failed the n≥200 filter (cohort size vs total enrolment). BYLieve is *the* post-CDK4/6i PIK3CAmut PI3Ki trial and directly bears on G7.

5. **Add a "historical pivotal" disclosure for BOLERO-2 (NCT00863655) and FALCON (NCT01602380),** explicitly noting they were excluded by the v2.1 amendment's start-year filter. Either include them with documented provenance ("v1-cited foundational, like PALOMA-2/OlympiAD/SOLAR-1") or run a pre-specified sensitivity analysis without the start-year filter. The Discussion's silence on this is the largest single fairness issue with the EFDPR=0.60 claim.

6. **Merge or justify G19, G23, and G24 as duplicates of G5, G20, and G22 respectively.** As written they inflate the denominator by 3 and the numerator by 3 (all three are evidence-free), preserving the ratio but reducing the credibility of the count. If kept separate, justify with a clinical-distinction rationale (e.g., G19 vs G5: monotherapy SERD post-progression vs early-switch SERD+CDK4/6i on emergent ESR1mut). I would recommend collapsing them, which would tighten the analysis to 22 nodes and EFDPR≈0.55, P≈0.001, still rejects.

7. **Fix G21's biomarker encoding.** Either drop `HER2-low` from G21 (NCCN does not require it for Dato-DXd) or split G21 into G21a (Dato-DXd, no HER2-low) and G21b (T-DXd, HER2-low required, redundant with G12). Currently the encoding makes TROPION-Breast01 mechanically unable to support its own cited node.

8. **Re-encode G17 to allow CDK4/6i+ET as the modern visceral-crisis recommendation,** with RIGHT Choice (NCT03839823) as supporting edge. If kept as chemotherapy-only, explicitly note that the supporting trial (RIGHT Choice) demonstrated CDK4/6i+ET was non-inferior — i.e., the evidence pushes against the recommendation.

9. **Report EFDPR stratified by ESMO MCBS / level-of-evidence grade.** The data is in `recommended_classes[].grade` and is currently unused in the manuscript. A breakdown showing EFDPR ≈ 0.05–0.10 for I-A nodes and EFDPR ≈ 0.70+ for II-B/II-C nodes would defuse the "panel malpractice" misreading and is the single most useful supplementary table to add.

10. **Pre-specify node-encoding rules.** Document — ideally in a supplement amending the pre-reg — how the 9 new nodes were defined (drug-class granularity, state-token aggregation, menopausal-status splitting, indolent-disease tokenisation). Without this, the encoding choices are author-discretionary and are not protected from researcher degrees of freedom. The current pre-reg covers the test, but not the node set.

11. **Soften the abstract framing.** Replace "the pre-registered hypothesis...is confirmed (P=0.0002)" with "under the pre-registered encoding the test rejects (P=0.0002); under sensitivity analyses that re-encode the four debatable new nodes the EFDPR ranges 0.44–0.60 and the test continues to reject in all variants." This is more defensible and pre-empts the obvious panel rebuttal.

12. **Add a "what would convert each evidence-free node to supported?" column to Table tab:efdpr.** For each of the 15 evidence-free nodes, a one-line statement: "G7: a phase 2/3 trial with post-CDK4/6i + PIK3CAmut enrolment and PI3Ki vs control (BYLieve cohort A is candidate)." This converts the EFDPR overlay into actionable target-population guidance for trial sponsors — which the Discussion claims as a contribution but does not actually deliver in the current tables.

---

## VERDICT

**MAJOR REVISION.**

The framework is publishable. The systematic search, dual-annotator extraction, and pre-registered test are credible methodological contributions. The headline result (EFDPR significantly above 0.25) will likely survive every reasonable re-encoding I have requested.

However, the manuscript currently overstates the magnitude (0.60 is inflated by duplicate nodes G19/G23/G24 and by extraction errors on CAPItello-291 and DESTINY-Breast06), under-discloses the start-year filter's exclusion of BOLERO-2/FALCON, and presents the 9 new ASCO/NCCN nodes as if they were independently derived when at least 3 are duplicates of ESMO nodes. The fairness-to-panels framing is salvageable but requires stratification by evidence grade and softening of the "confirmed" language. None of these are fatal; all are fixable in a revision cycle.

I would re-review a revision that addresses asks 1, 2, 4, 5, 6, 9, and 11 at minimum. I would not block publication on asks 3, 7, 8, 10, and 12, but I would expect them to be addressed before final acceptance.

— Reviewer (BMO, ESMO panel)
