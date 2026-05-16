# Adversarial Clinical Review — v3 Round 4 (FINAL)

**Reviewer.** Thoracic + breast medical oncologist; ESMO/ASCO guideline panel member (HR+/HER2- mBC and EGFR/ALK NSCLC).
**Scope.** Final clinical sign-off on the v3 round-3 integration commit `123a461` ("v3 R3 integration: programmatic stale-literal sweep + figure script de-hardcoding + canonical numbers") against the four outstanding R3 functional items (TROPION-Lung01 N9, ALTA-1L N13, brain-mets N20/N22, SAVANNAH N21) and the cluster-prose / discussion stale numbers that R3 explicitly punted on. Files audited: `manuscript/paper_A_clinical_v3.tex`, `manuscript/paper_B_methods_v3.tex`, `data/processed/v3_nsclc_decision_tree.json`, `data/processed/v3_nsclc_full.json`, `data/results/v3_pooled_efdpr.json`, `release/canonical_numbers.md`, `release/RELEASE_NOTES_v3.0.0.md`, `release/audit_numbers.sh`. Git range `dadf797..HEAD` (single commit, `123a461`).

**Bottom line.** R3 (commit `123a461`) is a real, substantive integration that closes the most publication-blocking item from R3-review (the figure-script hard-coded constants), installs a canonical-numbers single-source-of-truth (`release/canonical_numbers.md`) with a literal-grep audit script (`release/audit_numbers.sh`), and brings the bulk-arithmetic stale literals into compliance: `n=49` everywhere except two prose locations, `178 trials / 147 in-scope` everywhere, `P=0.084` (no more `P=0.10`), `ALK P=0.56` (no more `P=0.63`), `17/49` ESCAT/liberal (no more `24/50`), and the figures now read numbers from the JSON. **This is genuine progress.**

**But four R3 outstanding clinical items remain, and the manuscript continues to make claims at the prose level that the framework's own concordance algorithm contradicts.** Specifically:

1. **TROPION-Lung01 N9** is still evidence-free at every tolerance (`prior_state.post_osimertinib = null`; subgroup token `EGFR-mut_subgroup` ≠ liberal-matcher token `EGFR-mut`). Paper A L136 still names "TROP2-ADC (TROPION-Lung01)" inside the post-osimertinib evidence-base paragraph — implicitly claiming TROPION supports the post-osi decision space when the framework says N9 = `[]`.
2. **ALTA-1L N13** is still cited in `cited_trials` but expelled from the support set (`year_pc=2020 > N13.year=2017`). Per-node support is `[NCT01828099 (ASCEND-4), NCT02075840 (ALEX)]`. The manuscript at L139 still names "ALEX, ALTA-1L, CROWN, PROFILE 1014 all in 1L" — implicitly claiming ALTA-1L is one of N13's 1L supporters.
3. **N20 / N22 (brain-mets)** are still evidence-free at every tolerance because the brain-mets de-stripping change from R1 was never paired with a subgroup-readout match. The manuscript does not disclose this design choice anywhere.
4. **SAVANNAH** is still `drug_class="investigational (other)"` (stripped from the DAG) and the biomarker schema still has no `met_amplification` field. N21 = `[]` at every tolerance. Paper A L136 still names "MET-amp salvage (SAVANNAH)" inside the same post-osimertinib evidence-base sentence — implicitly claiming SAVANNAH supports N21 when the framework expelled it.

**Plus three prose-level honesty failures that R3 punted on:**

5. **Discussion headline at L132-133 still says "50 pooled guideline nodes"** (should be 49). The audit script `release/audit_numbers.sh` line 16 explicitly searches for `"50-node\|n = 50\|n=50"` as a forbidden literal but it scans `release/*.md`, `release/submission_*/*.md`, and `release/submission_*/cover_letter*.md` only — it does NOT scan `manuscript/paper_A_clinical_v3.tex` or `manuscript/paper_B_methods_v3.tex`. The same is true of the other forbidden literals. The audit script gives a false sense of completeness: it lints the release surface but not the manuscript surface where the same stale numbers persist.
6. **Discussion L136 still says "Of 17 EGFR-mutant decision nodes, 12 are evidence-free at strict tolerance"** — should be **7** (the post-R1 honest figure). This is the pre-R1 buggy 0.71 figure × 17 = 12. The abstract at L50 correctly says "NSCLC EGFR-only 0.41" (= 7/17) so the Discussion at L136 flatly contradicts the abstract on the most-cited number in the manuscript. R3-clinical asked for this fix (D4); not done.
7. **Cluster prose at L118 still lists supported nodes as evidence-free**: N7 (MARIPOSA-2, supported), N8 (HERTHENA-Lung01, supported), N11 (PAPILLON, supported), N25 (FLAURA2, supported) are all named in cluster (i)/(ii) but they have non-empty `per_node_support`. R3-clinical D5 asked for this; not done.

The pooled headline ($P = 0.023$) is robust to all four functional fixes (any of them either keeps an evidence-free flag in place or reduces the count by one; the one-node-deep rejection margin survives ±1 node), so this is **honesty work, not headline work**. But until the prose is reconciled with the framework's actual output, a clinician cross-checking Paper A L136 against `v3_pooled_efdpr.json` `primary.strict.per_node_support` will find that TROPION-Lung01 and SAVANNAH are named in the post-osimertinib evidence-base sentence but contribute zero edges; that ALTA-1L is named in the 1L ALK list but does not support N13; and that "12 of 17 EGFR evidence-free" contradicts the abstract's own "0.41 (7/17)" arithmetic.

---

## A. R3 outstanding items — honest-disclosure audit

The user-provided question for R4 is: **for each of the four R3 outstanding functional items, is the manuscript's disclosure honest, or is it implicitly claiming these are supported?** Verdicts below.

### A1. TROPION-Lung01 N9 — manuscript implicitly claims support; framework disagrees. **DISHONEST AS WRITTEN.**

The TROPION record at `data/processed/v3_nsclc_full.json` (NCT04656652) now has `biomarker.egfr_mut = true` (R2 fix), but `prior_state.post_osimertinib = null` and the subgroup-readout token is still `"EGFR-mut_subgroup"` (not the literal `"EGFR-mut"` that `_bm_match_liberal` looks for). Consequences per `data/results/v3_pooled_efdpr.json`:

```
primary.strict.per_node_support.N9   = []
primary.escat.per_node_support.N9    = []
primary.liberal.per_node_support.N9  = []
```

Paper A L136 reads (current text):

> Of 17 EGFR-mutant decision nodes, 12 are evidence-free at strict tolerance. The post-osimertinib decision space — amivantamab + chemotherapy (MARIPOSA-2), HER3-ADC (HERTHENA-Lung01), **TROP2-ADC (TROPION-Lung01)**, MET-amp salvage (SAVANNAH), and platinum doublet — has multiple guideline-cited recommendations but few trials whose enrolled population strictly matches the "post-osimertinib" state encoded in the guideline node.

A thoracic oncologist reading this paragraph would naturally infer: "the framework is showing me which trials support which post-osimertinib guideline nodes, and TROPION-Lung01 is one of them." But the framework's `N9 = []` says TROPION-Lung01 does not support its own cited node at any tolerance. **The prose names TROPION-Lung01 as evidence and the framework's concordance algorithm rejects it.** Either fix the record (R3-clinical D6a: set `post_osimertinib=true`, normalise the subgroup token), or rewrite the sentence to honestly state "of 7 EGFR-mutant nodes that are evidence-free, the post-osimertinib decision positions (N9 TROP2-ADC, N21 MET-amp, N23 post-amivantamab, N24 post-osi+post-chemo) are evidence-free at every tolerance level in the current framework; TROPION-Lung01 and SAVANNAH are guideline-cited but do not satisfy concordance — see Methods / Supplement for the encoding rationale."

### A2. ALTA-1L N13 — manuscript implicitly claims support; framework disagrees. **DISHONEST AS WRITTEN.**

The merged N13 cites both ALEX (NCT02075840) and ALTA-1L (NCT02737501). Temporal precedence: ALTA-1L's `year_pc = 2020`, N13's `year = 2017`, so the supports function rejects ALTA-1L. Per-node support:

```
primary.strict.per_node_support.N13 = ["NCT01828099", "NCT02075840"]
                                       (ASCEND-4 + ALEX, no ALTA-1L)
```

Paper A L139 reads:

> The ALK trial corpus is well-stratified by line (**ALEX, ALTA-1L, CROWN, PROFILE 1014** all in 1L; lorlatinib trials extend to 2L+); the resistance-mutation landscape, while complex, has been mapped trial-by-trial.

The sentence lists ALTA-1L as one of the 1L ALK trial supporters. The framework treats it as cited-but-not-supporting. This is a milder issue than A1 because ALTA-1L genuinely IS a 1L ALK trial and the temporal-precedence rule is what expels it from N13's support set (not a clinical mis-coding). But: the per-node figure (Fig 2) does not distinguish between "cited and supports" and "cited but expelled by year_pc"; a reader looking at N13's bar and at L139's prose will conclude that ALTA-1L is among N13's supporters. This is a transparency issue, not a falsehood, but it should be disclosed in Methods that N13's year=2017 represents the 2017 introduction of the 2nd-gen ALK TKI 1L recommendation and that ALTA-1L (year_pc=2020) is registered as a confirmatory data point for the same recommendation rather than a primary support. Alternatively, move N13's year to 2020 (R3-clinical D6b option a) and ALTA-1L will support; or drop ALTA-1L from `cited_trials` (option b).

### A3. N20 / N22 brain-mets — manuscript does not disclose the design choice. **HONEST OMISSION, BUT REQUIRES METHODS DISCLOSURE.**

`primary.strict.per_node_support.N20 = []` and `primary.strict.per_node_support.N22 = []` at every tolerance. N20 (1L+brain-mets, ALK-rearranged) and N22 (1L+brain-mets, EGFR-mut) contribute 2 of the 19 strict evidence-free flags. The R1 fix removed `brain-mets` from the state-strip list but did not implement a compensating subgroup-readout match for brain-mets-explicit registrational trials (FLAURA, ALEX, ALTA-1L, CROWN). The manuscript does NOT name N20 or N22 in any cluster-prose at L118; it does NOT cite FLAURA or ALEX as brain-mets evidence supporters anywhere. So at the prose level the manuscript is not making a false claim — it is silent on N20 and N22.

**But the manuscript is also silent on WHY N20 and N22 are evidence-free.** A clinician reading Fig 2 sees two flagged-red bars (N20, N22) and a reader who knows the trial landscape will ask "but the FLAURA CNS subgroup and ALEX CNS subgroup both reported intracranial PFS — why don't they count?" The honest answer is: the framework's current encoding requires a brain-mets-explicit token in `subgroup_readouts` and none of FLAURA/ALEX/ALTA-1L/CROWN have it; this is a deliberate design choice for v3 to require explicit brain-mets-stratified registrational endpoints, deferred to v4 to widen. **This sentence belongs in Paper A Methods §"NSCLC guideline decision-tree encoding" (L87) or in Paper B §"Concordance algorithm" (L84).** The current manuscript does not make this disclosure; a reviewer or guideline committee member will misread N20/N22 as "no brain-mets evidence in NSCLC" when in fact the brain-mets evidence exists at the subgroup level and is excluded by an encoding choice.

R3-clinical D6c offered this as one of three options (the other two being to implement the subgroup-readout match, or to drop N20 and N22 from the tree). None was executed. The manuscript should disclose the choice in Methods even if the encoding is not changed.

### A4. SAVANNAH / N21 MET-amp — manuscript implicitly claims support; framework disagrees. **DISHONEST AS WRITTEN.**

SAVANNAH (NCT03778229) is in the corpus with `egfr_mut=true, post_osimertinib=true` but `drug_class="investigational (other)"` (stripped from DAG by `v3_07_build_combined_dag.py:95-96`). The biomarker schema has no `met_amplification` field. N21 (post-osimertinib, EGFR-mut/MET-amp/NSCLC, `cited_trials=[]`, recommended class "investigational (other)") cannot be supported by any trial under any tolerance: `primary.strict.per_node_support.N21 = []`.

Paper A L136 names "MET-amp salvage (SAVANNAH)" in the post-osimertinib evidence-base sentence (same sentence as TROPION-Lung01, see A1 quote above). The prose implies SAVANNAH is part of the post-osimertinib trial evidence; the framework expelled it via the drug-class strip. **Same dishonesty as A1 but with an additional structural issue:** N21 has `cited_trials = []` (no NCCN-cited registrational trial), so even without the drug-class strip the node would be evidence-free for a stricter reason than the framework's algorithm. The fix is to either (a) re-encode SAVANNAH with `drug_class="MET-TKI + osimertinib"` and add a `met_amplification` biomarker field, or (b) drop N21 from the tree as "investigational, no Tier I/II evidence" with a Methods disclosure, or (c) rewrite L136 to honestly state that SAVANNAH is guideline-cited as an investigational option but does not satisfy the framework's drug-class concordance criterion (because "investigational (other)" is excluded from the DAG by construction).

R3-clinical D6 listed SAVANNAH as a possible R3-functional fix (it was not the recommended one); R3 did not execute any of the three. The R4-blocking item here is **either fix the encoding or rewrite the Discussion sentence** — not both. The current state (encoding unchanged, prose unchanged) is the dishonest combination.

---

## B. Stale prose carryover from R3-clinical D4 and D5

R3-clinical D4 asked for six Paper A stale-number fixes. R3 (commit `123a461`) closed three of the six:

- L73 (Intro): `n = 50` → `n = 49` ✓ (fixed)
- L90 (Methods): "50-node pooled denominator" → "49-node" ✓ (fixed)
- L139 (Discussion): "$P = 0.63$" → "$P = 0.56$" ✓ (fixed)
- L145 (Three caveats): "$P = 0.10$" → "$P = 0.084$" ✓ (fixed)
- L81 (Methods): "145 in-scope" — **NOT FIXED**, still says "145" (canonical is 147; R3 only swept release files, not paper_A.tex L81)
- L133 (Discussion Headline): "50 pooled guideline nodes" — **NOT FIXED**, still says "50" (the audit script does NOT lint manuscript/*.tex)
- L136 (Discussion): "12 of 17 EGFR evidence-free" — **NOT FIXED**, still says "12" (post-R1 honest is 7)

R3-clinical D5 asked for cluster prose cleanup at L118. **NOT FIXED.** The cluster prose still lists N7, N8, N11, N25 as evidence-free (all four are supported per `primary.strict.per_node_support`).

R3-clinical D7 asked for a one-paragraph R1-correction transparency disclosure in §"Three caveats". **NOT ADDED.** The Discussion still does not acknowledge that the v3.0.0 release tag (still publicly visible) reports pre-R1 numbers (EFDPR 0.48, P=0.0004, EGFR 0.71). A reader who lands on the GitHub release page sees one set of numbers; a reader who downloads the PDF sees another set; no bridge.

**Summary of stale-prose items still open after R3 integration:**

| Location | Current text | Canonical | R3 round of fix |
|---|---|---|---|
| paper_A L81 | "145 in-scope" | 147 | should have been D4 |
| paper_A L118 | N7/N8/N11/N25 listed as evidence-free | All four supported | D5 |
| paper_A L132-133 | "50 pooled guideline nodes" | 49 | D4 |
| paper_A L136 | "12 of 17 EGFR evidence-free" | 7 of 17 | D4 (most-cited number) |
| paper_A L136 | "TROP2-ADC (TROPION-Lung01)" cited as evidence | Framework: N9 = [] | D6a |
| paper_A L136 | "MET-amp salvage (SAVANNAH)" cited as evidence | Framework: N21 = [] | D6 (any option) |
| paper_A L139 | "ALEX, ALTA-1L, CROWN, PROFILE 1014 all in 1L" | ALTA-1L not in N13 supports | D6b |
| paper_A Methods | No disclosure of brain-mets encoding choice | — | D6c |
| paper_A §"Three caveats" | No R1-correction acknowledgement | — | D7 |
| paper_B L130 prose | "17/49 → 17/50" (typo: should be "17/49") | 17/49 ESCAT/liberal | R3 swept but introduced new arithmetic typo |

Note the last row: R3's sweep of `paper_B_methods_v3.tex` L130 changed `"0.34 (24/50 → 17/50; $P = 0.10$)"` to `"0.347 (17/49 → 17/50; $P = 0.084$)"`. The new text reads "17/49 → 17/50" which is meaningless — neither side is the "before" and the destination is still wrong (`17/50` should be `17/49`). This appears to be a partial-sed artifact. The sentence is supposed to read "ESCAT-aligned and liberal tolerance gave 0.347 (**17/49 evidence-free vs 19/49 strict**; $P = 0.084$)". The R3 sweep was mechanically right on `0.34→0.347` and `0.10→0.084` and `24/50→17/49` but left the second `17/50` in place, which is now numerically wrong by a different mechanism.

---

## C. Net manuscript credibility audit

### C1. Per-node support consistency (strict, primary)

Quoting `data/results/v3_pooled_efdpr.json` `primary.strict.evidence_free_nodes`:

```
["G9", "G12", "G13", "G14", "G15", "G17", "G21", "G22", "G24", "G25",
 "N9", "N10", "N12", "N19", "N20", "N21", "N22", "N23", "N24"]
```

Count = 19. NSCLC evidence-free subset = `[N9, N10, N12, N19, N20, N21, N22, N23, N24]` = 9 nodes. NSCLC EGFR-only evidence-free = `[N9, N10, N12, N21, N22, N23, N24]` = 7 nodes. NSCLC ALK-only evidence-free = `[N19, N20]` = 2 nodes. All match the abstract.

### C2. Manuscript prose vs framework output

| Paper A section | Prose claim | Framework output | Status |
|---|---|---|---|
| Abstract L50 | "0.39 (19/49)", "NSCLC EGFR-only 0.41 (P=0.11)", "NSCLC ALK-only 0.29 (P=0.56)" | ✓ matches | OK |
| Box L61 | "0.39", "P=0.023" | ✓ matches | OK |
| Methods L81 | "145 in-scope" | 147 | STALE |
| Methods L87 | "17 EGFR / 7 ALK" | ✓ 17 + 7 = 24 | OK (R2 fix) |
| Methods L90 | "49-node" | ✓ 49 | OK (R3 fix) |
| Fig 1 caption L100 | "P = 0.023, 49-node" | ✓ matches | OK (R2 fix) |
| Fig 2 caption L123 | "pooled 49-node" | ✓ matches | OK (R3 fix) |
| Fig 3 caption L110 | "P = 0.023, 49-node, $-\log_{10}P = 3.4$" | "3.4" is wrong; $-\log_{10}(0.023) \approx 1.64$ | STALE (R2/R3 missed) |
| Results L118 cluster | N7, N8, N11, N25 listed as evidence-free | All supported (MARIPOSA-2, HERTHENA, PAPILLON, FLAURA2) | STALE |
| Disc Headline L133 | "50 pooled guideline nodes" | 49 | STALE |
| Disc L136 | "12 of 17 EGFR evidence-free" | 7 of 17 | STALE (most-cited number) |
| Disc L136 | TROP2-ADC TROPION + MET-amp SAVANNAH listed as post-osi evidence | N9 = [], N21 = [] | DISHONEST |
| Disc L139 | ALTA-1L listed as 1L ALK support | ALTA-1L expelled from N13 | DISHONEST (mild) |
| Disc L142 | "19 evidence-free decision nodes" | ✓ 19 | OK (R2 fix) |
| Three caveats L145 | "P = 0.084" | ✓ matches | OK (R3 fix) |
| Limitations L151 | "259-trial pooled corpus" | ✓ 178 + 81 = 259 | OK (R2 fix) |

### C3. Fig 3 trajectory caption arithmetic still wrong

L110: "The pooled 49-node test rejects at $P = 0.023$ ($-\log_{10} P = 3.4$)." For $P = 0.023$, $-\log_{10}(0.023) = 1.64$, not $3.4$. The "3.4" was the correct $-\log_{10}$ for the pre-R1 $P = 0.0004$ figure. R2 fixed $P = 0.0004 \to 0.023$ in the caption; neither R2 nor R3 fixed the $-\log_{10}$. This is a self-contradicting sentence: the $P$-value and the $-\log_{10}$ now do not match each other. A journal copy-editor will catch this; a careful reviewer will lose confidence in the QC pipeline.

This is a small but completely-mechanical fix and the fact that two integration rounds missed it is indicative of the same pattern that drove the R3 review: the manuscript is being edited number-by-number rather than re-read end-to-end.

### C4. Audit script scope is narrower than advertised

`release/audit_numbers.sh` lints `release/*.md`, `release/submission_*/*.md`, `release/submission_*/cover_letter*.md` for forbidden literals. It does NOT lint `manuscript/paper_A_clinical_v3.tex`, `manuscript/paper_B_methods_v3.tex`, or any of the `release/submission_*/POLISH_PLAN*.md` documents. This is why "50 pooled guideline nodes" survives at Paper A L133, "12 of 17 EGFR" survives at L136, "$-\log_{10} P = 3.4$" survives at L110, and "145 in-scope" survives at L81 — none of these is in the audit script's path glob.

**Suggested fix (one-line):** extend the script's globs to include `manuscript/*.tex`. Then re-run; the script will flag all four remaining issues automatically.

---

## D. Concrete asks for v3 round-4 integration (6 items)

These are the minimum honest-disclosure asks for v3 release. None of them changes the pooled headline ($P = 0.023$).

### D1. **Fix Paper A L133 and L136 stale numbers (BLOCKING).**

- L133 (Discussion headline): "**50 pooled guideline nodes**" → "**49 pooled guideline nodes**".
- L136 (Discussion): "Of 17 EGFR-mutant decision nodes, **12** are evidence-free at strict tolerance" → "**7** are evidence-free at strict tolerance" (cite `primary.strict.per_node_support` directly, 7/17 = 0.41 matches the abstract).
- L81 (Methods): "**145** in-scope" → "**147** in-scope".
- L110 (Fig 3 caption): "$-\log_{10} P = 3.4$" → "$-\log_{10} P = 1.64$" (or simply remove the parenthetical and let the figure axis label carry the value).

These are pure-arithmetic fixes; no clinical content involved.

### D2. **Honest rewrite of Paper A L136 post-osimertinib paragraph (BLOCKING).**

Current text names TROP2-ADC (TROPION-Lung01) and MET-amp salvage (SAVANNAH) inside the post-osimertinib evidence-base sentence, implicitly claiming both as supporters when the framework reports N9 = `[]` and N21 = `[]`. Rewrite to one of:

- **(option a, encoding fix)**: set `prior_state.post_osimertinib=true` on TROPION-Lung01 (NCT04656652); change subgroup-readout token `"EGFR-mut_subgroup"` → `"EGFR-mut"`; re-encode SAVANNAH with `drug_class="MET-TKI + osimertinib"` (a class already in `DRUG_CLASS_EQUIVALENCE`) and add `met_amplification` to the biomarker schema. Then both N9 and N21 should support under liberal at minimum. Re-run EFDPR. The pooled headline either stays at $P = 0.023$ (if the new supports are under liberal only) or shifts to $P = 0.049$ (if 1 evidence-free flips; still rejects). Either way the headline survives.
- **(option b, prose fix)**: rewrite L136 to "Of 17 EGFR-mutant decision nodes, 7 are evidence-free at strict tolerance, concentrated at post-osimertinib salvage positions (N9 TROP2-ADC, N21 MET-amp, N23 post-amivantamab, N24 post-osi+post-chemo). TROPION-Lung01 and SAVANNAH are guideline-cited at these positions but do not satisfy the framework's strict drug-class / state concordance criterion — the encoding rationale is documented in Methods §[brain-mets / subgroup-readout disclosure, per D5]."

Option (a) is more honest scientifically but is the bigger code change; option (b) is the smaller, low-risk path and is acceptable as a v3 release if D5 is also added.

### D3. **Cluster-prose cleanup at Paper A L118 (BLOCKING).**

Drop N7 (MARIPOSA-2 supports under strict), N8 (HERTHENA-Lung01 supports under strict), N11 (PAPILLON supports under strict), N25 (FLAURA2 supports under strict) from the "evidence-free cluster" list at L118. Add N19 (post-everything ALK, evidence-free) to the cluster (i) or (ii) per clinical judgement. The honest NSCLC evidence-free cluster is:
- post-osi salvage: N9, N21, N23, N24
- post-chemo: N10 (placeholder)
- 2L ex20ins: N12
- brain-mets: N20, N22
- post-everything ALK: N19

The mBC cluster (iii) is approximately right but should also include G12 and G15 (per `primary.strict.evidence_free_nodes`), and the prose count should match `evidence_free_count = 19` exactly. R3-clinical D5 prescribed this; not done.

### D4. **Fix Paper B L130 arithmetic typo (MINOR but copy-editor-blocking).**

R3 swept the sentence but left a partial-edit artifact: "ESCAT-aligned and liberal tolerance gave 0.347 (**17/49 → 17/50**; $P = 0.084$), failing to reject." The "17/50" denominator is still pre-R3 stale. Rewrite to: "ESCAT-aligned and liberal tolerance gave 0.347 (17/49 evidence-free, vs strict 19/49; $P = 0.084$), failing to reject." Or simpler: "ESCAT-aligned and liberal tolerance gave 0.347 (17/49; $P = 0.084$), failing to reject."

### D5. **Add a one-paragraph Methods disclosure of the four encoding limitations (BLOCKING for transparency).**

Add to Paper A §"NSCLC guideline decision-tree encoding" (L87) or to a new Methods sub-section titled "Known encoding limitations for v3 release":

> Four guideline-node encoding choices in v3 produce deterministic evidence-free flags that a clinically-aware reader may find counter-intuitive: (i) **N20 and N22 (brain-mets)** are evidence-free at every tolerance because the framework requires a brain-mets-explicit token in the trial's `subgroup_readouts`; the CNS subgroup analyses of FLAURA, ALEX, ALTA-1L, and CROWN are not encoded with such a token in v3 and are scheduled for v3.0.1 / v4. (ii) **N9 (TROPION-Lung01)** is evidence-free at every tolerance because the trial enrolled a biomarker-mixed population with a pre-specified EGFR-mut subgroup readout (WCLC 2023) that the framework's strict and liberal matchers do not currently resolve; the trial is hand-curated in the corpus with `tumor_type=NSCLC-EGFR` but the post-osimertinib state token and the subgroup-readout matcher were not updated in v3. (iii) **N13 (1L 2nd-gen ALK TKI)** cites both ALEX (year_pc=2017) and ALTA-1L (year_pc=2020); the merged node carries `year=2017` and ALTA-1L is therefore excluded from the support set by the temporal-precedence criterion. The 2017 introduction date reflects the original ALEX-based 2nd-gen 1L recommendation, not the 2020 ALTA-1L OS update. (iv) **N21 (post-osimertinib MET-amp)** has no NCCN-cited registrational trial in `cited_trials` and its recommended class is "investigational (other)" which the framework strips from the trial-DAG by construction; SAVANNAH (NCT03778229), the canonical NCCN-cited candidate, is in the corpus but excluded by the drug-class strip and by the absence of a `met_amplification` field in the biomarker schema. All four choices are deliberately conservative for v3; v4 will widen the brain-mets matcher, normalise the subgroup-readout token, add the MET-amp biomarker field, and reconsider the merged-node year convention.

This paragraph is honest, audit-trail-complete, and does not change the headline. It is the single most-important disclosure missing from v3.

### D6. **Extend `release/audit_numbers.sh` to lint `manuscript/*.tex` (MINOR but high-leverage).**

Two-line change: add `manuscript/paper_A_clinical_v3.tex` and `manuscript/paper_B_methods_v3.tex` to the script's globbed file list. Re-run; the script will automatically flag "50 pooled guideline nodes" at L133 and "12 of 17 EGFR" at L136. This closes the gap between "release surface is linted" and "manuscript surface is linted" and prevents a recurrence of the same stale-literal issue at v3.0.1 / v3.1 / v4.

(Optional: also add a check for the $-\log_{10}P = 3.4$ literal specifically; this is the kind of one-off arithmetic error that survives sed-style sweeps.)

---

## E. What R3 did well (for completeness)

- **`release/canonical_numbers.md`** is the single most-valuable artifact added in R3. It is a complete numerical bill-of-materials with the canonical-vs-stale split, the multiplicity caveat (one-node-deep rejection), and the FORBIDDEN STALE LITERALS list. **This is the right way to manage a multi-version manuscript with a sed-and-grep editing pattern.** If extended to lint manuscript/*.tex (D6), it would have caught the four remaining items above before they reached this review.
- **`release/audit_numbers.sh`** mechanically searches for the forbidden literals across the release surface and is a real CI-grade tool. Its scope is narrower than its name suggests (D6) but the bones are right.
- **`analysis/v3_09_figures.py` de-hardcoding** (35-line diff) is the most consequential code-side fix in R3. The three figure PDFs are now data-driven and re-running the script reproduces the committed figures from the result JSON. R3-clinical D1 closed.
- **`release/RELEASE_NOTES_v3.0.0.md` rewrite** (25-line diff) closes R3-clinical D2: the public-facing release page now shows post-R1 canonical numbers.
- **`paper_B_methods_v3.tex` sweep** (6-line diff) closes R3-clinical D3: the methods paper now reports 178 trials, 147 in-scope, 49-node, $P = 0.084$ — modulo the residual "17/50" typo at L130 (D4 above).
- **Paper A discussion ALK P-value** ($0.63 \to 0.56$ at L139) — closed in R3.
- **Paper A "Three caveats" P-value** ($0.10 \to 0.084$ at L145) — closed in R3.
- **`submission_plan_paperA_jcopo/AUDIT_REPORT.md` and `POLISH_PLAN_14_DAYS.md`** swept (R3-clinical D8 closed).

R3 is the most productive integration round of v3. The remaining open items are concentrated in the Discussion (L118, L133, L136), in the Fig 3 caption ($-\log_{10}$ arithmetic), and in the four functional encoding choices that the manuscript continues to not disclose.

---

## VERDICT

**MINOR REVISION.**

The R3 integration is genuine progress. The figure script is data-driven, the canonical-numbers single-source-of-truth is in place, the audit script catches the bulk-arithmetic literals across the release surface, the public-facing release page is rewritten, Paper B and the submission-plan documents are swept, and 4 of 6 R3-clinical D4 stale-number fixes were closed. **The framework's headline ($P = 0.023$) is honest, derivable from the artifacts, and survives the remaining encoding choices.**

But the manuscript still contains **two dishonest prose claims** (Paper A L136 names TROPION-Lung01 and SAVANNAH in the post-osimertinib evidence-base sentence; the framework reports both as evidence-free) and **two stale prose carryovers from R2-R3** (L133 "50 pooled guideline nodes"; L136 "12 of 17 EGFR evidence-free"). The cluster prose at L118 still lists supported nodes (N7, N8, N11, N25) as evidence-free. The brain-mets design choice (N20, N22 evidence-free as a deliberate v3 conservatism) is undisclosed in the manuscript. The Fig 3 caption $-\log_{10}P$ arithmetic ($P = 0.023$ does not give $-\log_{10}P = 3.4$) is self-contradicting.

**None of the six R4 asks (D1-D6) changes the pooled rejection.** D1-D4 are arithmetic and prose fixes (1-2 hours of work). D5 is one Methods paragraph (the single most-important disclosure missing from v3). D6 is a two-line glob extension to the audit script. The full R4 integration is approximately one half-day of focused editing plus a `make` re-render.

**I would sign off on a v3.0.1 release that addresses D1, D2 (option b: prose rewrite, not encoding fix), D3, D4, D5, and D6.** Option (a) of D2 (encoding fix for TROPION and SAVANNAH) is preferable scientifically and should be considered for v3.1 / v4 but is not blocking for the v3.0.1 release. The four functional R3 punts (TROPION-N9, ALTA-1L-N13, brain-mets-N20/N22, SAVANNAH-N21) are then disclosed as known v3 encoding limitations with explicit v4 scheduling rather than silently inconsistent claims.

**The framework is sound, the numbers are honest, and the remaining work is one Discussion-paragraph rewrite plus one Methods-paragraph disclosure.** I would not block the JCO PO submission on D1-D6 if the editor decides to ship v3.0.0 now and follow up with v3.0.1 within 30 days; but the manuscript-vs-framework prose inconsistency at L136 (TROPION + SAVANNAH cited as evidence; framework says no) is the kind of thing a JCO PO reviewer will flag during peer review, and pre-submission resolution is the cheaper path.

— Reviewer (Thoracic + Breast MO, ESMO/ASCO panel)
