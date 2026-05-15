# Biostatistics Review — main_v2.tex (Round 2)

**Reviewer role.** Adversarial biostatistics referee, final round. Focus:
integration honesty against round-1 asks (A1--A15), primary-test correctness
on the post-fix numerics, kappa-paradox disclosure, secondary-outcome
reporting, internal numerical consistency across abstract / KO box / Results
/ Discussion / Tables S1--S6. Spot-checks recomputed from scratch against
`v2_efdpr.json`, `v2_kappa.json`, `v2_kappa_postadj.json`,
`v2_odi.json`, and the analysis scripts.

## Spot-check reproduction (4 decimals)

| Quantity | Reviewer-computed | Manuscript |
|---|---|---|
| $P(X \ge 12 \mid n=25, p=0.25)$ | 0.0107 | 0.011 (abstract, KO, Results, Discussion, Table S-EFDPR 0.0107). OK |
| Clopper-Pearson 95% CI for 12/25 | [0.2780, 0.6869] | [0.28, 0.69] / [0.278, 0.687]. OK |
| ESMO-only $P(X \ge 6 \mid n=16, p=0.25)$ | 0.1897 | 0.19 abstract / 0.1897 table. OK |
| NCCN-citing $P(X \ge 6 \mid n=10, p=0.25)$ | 0.0197 | 0.020 abstract / 0.0197 table. OK |
| Exact power at $p_1=0.50$, $n=25$, $k_{\mathrm{crit}}=11$ | 0.7878 | 79% (Methods 2.7) and "$\sim 79\%$" (Discussion). OK -- the round-1 A1 82% error is fixed. |
| ASCO-citing $P(X \ge 5 \mid n=15)$ | 0.3135 | 0.31 abstract / 0.3135 table. OK |
| PABAK for akt\_path ($P_0 = 0.95$) | 0.90 | 0.90 abstract, Results, S2. OK |
| Mean key-field PABAK post-adj | 0.9875 -> rounds to 0.99 | 0.99 abstract, Results, Discussion. OK |

All primary and sensitivity numerics reproduce exactly to 4 decimals; the
A1 power-analysis numerical error is corrected; no internal inconsistency in
P-values across the manuscript.

## Round-1 ask integration check

| Ask | Status | Note |
|---|---|---|
| A1 power 82% -> 79% | **Fixed**. Methods 2.7 and Discussion both 79%. |
| A2 $n=25$ as realised gate | **Partially**. Methods 2.7 reports 25-node analysis with sensitivity by source; the "realised minimum" framing is implicit, not explicit. Minor. |
| A3 14 vs 17 rules | **Fixed**. Abstract, Methods, Results, supplement, S-T1 all say 17 (Sup. Text 1 explicitly flags the deviation). |
| A4 S2 / S3 | **Reported descriptively** (Results 3.6). Supplement Text 1 lists this as a disclosed deviation. Acceptable. |
| A5/A6 kappa-paradox honesty | **Partially fixed** -- see Specific Q2 + Q3 below. The Cohen's $\kappa$ gate failure on `akt_path` is now disclosed in the abstract, the Results, the Discussion, and S2. PABAK is now defined ($2P_0 - 1$) in Results 3.1 and S2. Byrt 1993 still uncited (round-1 A6 sub-point 2 unaddressed). |
| A7 supplement_v2.tex | **Fixed**. New `supplement_v2.tex` exists with S1 transparency checklist, S2 kappa table, Sup. Text 1 deviation log, S3-S6 stubs. The S3 trial corpus is by-reference to JSON rather than tabulated -- defensible but worth flagging. |
| A8 PRISMA funnel + F7 amendment + supplementary-six overlap | **Not addressed in this round's deliverables I can see**. No PRISMA figure in `main_v2.tex` or `supplement_v2.tex`. The 874 -> 74 -> 80 -> 82 funnel is described in prose only; the F7 retroactive tightening is not flagged in the manuscript proper (it lives in Sup. Text 1 as a prereg-v2.1 commit ref but not as a methodology-section disclosure). |
| A9 bootstrap indexing asymmetry | **Not fixed**. `v2_09_compute_efdpr.py:148-149` and `v2_10_compute_odi.py:102-103` still use `lo = est[max(0, int(0.025*n) - 1)]` and `hi = est[min(n-1, int(0.975*n))]` -- asymmetric (`-1` on the low side, none on the high side). Numeric impact is negligible at $n=1{,}000$; methodology is still non-standard. |
| A10 tolerance grid is sensitivity, not three tests | **Fixed**. Methods 2.7: "treating the three tolerance levels as a pre-registered sensitivity grid rather than three independent confirmatory tests". |
| A11 ASCO marginal P framing | **Fixed**. Results 3.4 now frames the by-guideline subsets as "pre-specified ... sensitivity", and Conclusion of abstract specifies "ESMO- and ASCO-only sensitivity subsets do not individually reject the null". |
| A12 G18 missing | **Not addressed**. Figure caption still "G1--G26" with G18 absent; no footnote. Low priority. |
| A13 liberal rescues 1 not 2 | **Drift remains**. Results 3.7 still says "Liberal tolerance rescues two ESR1mut nodes via registrational subgroup readouts (G5 by EMERALD; G19 by SERENA-6)". JSON shows G5 is strict-supported (by NCT03778931) and G19 is unsupported under every tolerance; the actual strict$\to$ESCAT/liberal rescue is G4 (PIK3CAmut), not two ESR1mut nodes. This is a factual error against the JSON, not just a narrative imprecision. |
| A14 CP vs bootstrap primary CI | **Implicitly fixed**: CP is reported in abstract / Results / Table; bootstrap is mentioned only for ODI. Acceptable. |
| A15 abstract PABAK precision | **Fixed**: abstract reports both mean (0.99) and min (akt\_path 0.90). |

## Specific questions from the editor

**Q1. Are the new P-values across abstract, KO box, Results, Discussion, Tables CONSISTENT?**

Yes. $P = 0.011$ appears identically in abstract, KO box, Results 3.3, Discussion paragraph 1 + caveat 2. Sensitivity P-values 0.020 / 0.19 / 0.31 are consistent abstract / Results 3.4 / Table. The EFDPR table reports four-decimal $P$ (0.0107, 0.1897, 0.3135, 0.0197); the main text consistently rounds to two-decimal. No collisions.

**Q2. Is the Cohen's kappa gate FAIL honestly reported (akt_path paradox)?**

Yes, by round-1 standards. The abstract Results paragraph states "gate $\kappa \ge 0.70$ fails on post\_endo and the akt\_path kappa paradox case" pre-adjudication and "akt\_path remained at $\kappa = 0$" post-adjudication. Results 3.1 is explicit: "under Cohen's $\kappa$ the pre-registered gate fails on akt\_path; under PABAK the gate passes on every key field." S2 row for akt\_path is labelled "Fail Cohen, Pass PABAK". Discussion caveat 2 repeats the disclosure. This is the most consequential round-1 ask and it is now properly disclosed.

**Q3. Is the adjudication methodology now honestly described (adjudicated values become consensus for BOTH annotators, so post-kappa is tautological)?**

**No.** `v2_06_adjudication.py:103-107` writes the adjudicated value into **both** `adjudicated_A` and `adjudicated_B`, then `v2_06_adjudication.py:138-141` computes post-adjudication $\kappa$ between `adjudicated_A` and `adjudicated_B`. By construction, every field with $\ge 1$ adjudication rule attains 100% agreement and $\kappa = 1.00$ post-adjudication. The post-adjudication $\kappa = 1.00$ values in S2 for seven of eight key fields are therefore **definitional, not empirical**.

The manuscript currently states (Results 3.1): "Seventeen adjudication rules ... resolved all disagreements to consensus; post-adjudication Cohen's $\kappa$ on key fields was 1.00 for seven of eight fields". The phrase "resolved all disagreements to consensus" gestures at the mechanism but does not state the methodological consequence: the post-adjudication $\kappa$ is not a measurement of independent inter-rater agreement on adjudicated trials -- it is the agreement of `adjudicated_A` with `adjudicated_A` modulo adjudication-target trials in `adjudicated_B`, which after substitution is the same record.

This is the round-1 A5 sub-point 2 ask, and it remains undisclosed. The fix is one sentence in Methods 2.3 and/or S2: "Because the adjudication rule writes the consensus value back into both annotators' records, post-adjudication Cohen's $\kappa$ on adjudicated fields is 1.00 by construction; the post-adjudication $\kappa$ should be read as a measure of how thoroughly the adjudication closed disagreements, not as an independent re-validation of the two annotators."

**Q4. Are S2 and S3 now reported (descriptively)?**

Yes. Results 3.6 reports S2 (median lag 0 yr, IQR $-$2 to 2; two ESR1mut nodes within one update cycle) and S3 (28/66 = 42% Asian-ancestry, 13/66 = 20% age $\ge 70$, 3/66 = 5% Black-ancestry). Both are flagged in S2 line (Sup. Text 1) as a pre-registered deviation from formal test to descriptive. Acceptable per round-1 A4 option 1.

**Q5. Are bootstrap and CP CIs both reported with correct indexing?**

Both are reported (CP for the EFDPR primary; bootstrap for the ODI). However the **bootstrap indexing remains asymmetric** in both `v2_09_compute_efdpr.py:148-149` and `v2_10_compute_odi.py:102-103`: lower bound uses `int(0.025*n) - 1` (= index 24 at $n=1000$), upper uses `int(0.975*n)` (= index 975). The conventional choice is symmetric (`int(0.025*n)` and `int(0.975*n) - 1`, or simply `numpy.quantile`). The numeric impact is one ordinal position out of 1,000 -- invisible at the reported 2-3 decimal precision -- but the round-1 A9 ask was to *either fix the indexing or document the convention*, and neither has been done. This is a tiny but recurring methodology hygiene issue.

## Residual internal inconsistencies (new in round-2)

- **Title says "64-Trial" but corpus is 66 in-scope** (after BYLieve + SERENA-6 round-1 additions). Both `main_v2.tex` and `supplement_v2.tex` titles still say "64-Trial, Pre-Registered Graph-Theoretic Analysis". The cohort table says "66" and the abstract / Methods say "82 trials (66 in-scope)". The title needs to be 66-trial (in-scope) or 82-trial (corpus), not 64.
- **Methods 2.5 ASCO/NCCN node arithmetic**: says "16 ESMO-sourced (10 shared with ASCO and/or NCCN), 6 are ASCO-citing additions, and 9 are NCCN-citing additions" (total 16+6+9 = 31, not 25); and immediately above says "extended with 9 nodes unique to ASCO ... and NCCN". The numbers as written do not partition the 25 nodes. The EFDPR table additionally reports ASCO-citing $n = 15$ (so ASCO touches 15 of 25, including shared). One consistent partition needed.
- **Results 3.7 evidence-free count: "15 evidence-free nodes"**. The JSON `primary.strict.evidence_free_count` = **12**, the discussion paragraph "Where the gap is largest" says "**12 evidence-free nodes under strict concordance**", the abstract says 12/25, the EFDPR table row 1 says 12. Results 3.7 ("The 15 evidence-free nodes ...") is the only place that says 15, and it then lists 11 specific node IDs across three structural clusters. This is the same kind of stale-count error A3 caught for the adjudication count; please fix to 12.
- **Results 3.7 / A13 liberal-rescue narrative**: "Liberal tolerance rescues two ESR1mut nodes via registrational subgroup readouts (G5 by EMERALD; G19 by SERENA-6); the remainder are robust to tolerance." Against `v2_efdpr.json` the only strict$\to$ESCAT/liberal change is G4 gaining NCT02437318; G5 is already strict-supported by NCT03778931; G19 is unsupported under every tolerance. The "two ESR1mut node rescues" claim is unsupported by the JSON.

## Concrete asks (round-2)

**B1 (HIGH).** Disclose the post-adjudication kappa methodology limitation. Add to Methods 2.3 (or S2 note): "Adjudication writes the resolved value back into both annotators' records, so post-adjudication Cohen's $\kappa$ on any adjudicated field is 1.00 by construction. The post-adjudication $\kappa$ should be read as a closure measure for the adjudication pass, not as an independent re-measurement of inter-rater agreement." Without this, the abstract's "Post-adjudication, 7 of 8 key fields achieved Cohen's $\kappa = 1.00$" claim is technically true but rhetorically misleading.

**B2 (HIGH).** Fix two manuscript-vs-data errors:
(a) Results 3.7 "15 evidence-free nodes" -> "12 evidence-free nodes" (matches abstract, KO box, JSON, Discussion).
(b) Results 3.7 "Liberal tolerance rescues two ESR1mut nodes (G5 by EMERALD; G19 by SERENA-6)" -> "Liberal/ESCAT tolerance rescues G4 (PIK3CAmut, by NCT02437318); no ESR1mut nodes are rescued under any tolerance relaxation in this corpus." Or audit the matcher if the round-1 narrative intent was that G5/G19 should rescue.

**B3 (HIGH).** Update the title from "64-Trial" to "66-Trial" (in-scope, matches cohort table and figure DAG node count) or "82-Trial" (whole corpus). Update both `main_v2.tex` and `supplement_v2.tex` titles. The 64 is a stale number from a pre-round-1 draft.

**B4 (MEDIUM).** Reconcile Methods 2.5 ASCO/NCCN node arithmetic: state the 25-node partition as ESMO-only vs ESMO$\cap$(ASCO or NCCN) vs ASCO-only vs NCCN-only, with the four counts summing to 25, and align with the per-source EFDPR sensitivity denominators (ESMO-only 16, ASCO-citing 15, NCCN-citing 10).

**B5 (MEDIUM).** Either fix the bootstrap CI indexing asymmetry (round-1 A9: switch to `numpy.quantile(est, [0.025, 0.975])` or symmetric ordinal indexing) **or** add one sentence to Methods 2.7 documenting the convention as written. Numeric impact is negligible; methodological clarity is not.

**B6 (MEDIUM, optional).** Address the unfilled round-1 asks that did not make this revision: A2 (single-sentence "realised gate" disclosure in Methods 2.7), A8 (PRISMA-style funnel figure or table, and explicit F7 amendment disclosure in the main text rather than only in Sup. Text 1), A12 (one-line footnote for G1--G17/G19--G26 non-contiguous numbering). These are individually minor; collectively they are the residue of a thorough round-1 pass and would clean the paper for submission.

## VERDICT

**MINOR** revision. The pre-registered primary test reproduces exactly
($P = 0.0107$, CP CI [0.278, 0.687]); the A1 power error is fixed; the
A3 / A4 / A5-headline / A7 / A10 / A11 / A14 / A15 round-1 asks are all
satisfactorily integrated; the akt\_path Cohen's $\kappa$ failure is now
honestly reported in abstract, Results, Discussion, and S2. The two HIGH
asks (B1 post-adj-kappa tautology disclosure, B2 the 15-vs-12 and
G4-vs-G5/G19 stale numerics) and the title fix (B3) are quick edits with
no re-computation. The remaining round-1 residue (A8 PRISMA, A9 bootstrap
indexing) is methodology hygiene that does not threaten the conclusion.
With B1, B2, B3 in full and B4-B6 in some form, I recommend ACCEPT.
