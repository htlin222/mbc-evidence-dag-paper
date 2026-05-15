# Biostatistics Review — main_v2.tex (Round 1)

**Reviewer role.** Adversarial biostatistics referee. Focus: prereg fidelity,
test/estimator correctness, kappa-paradox handling, bootstrap and exact-CI
indexing, sensitivity-grid framing, secondary-outcome reporting honesty, search
funnel transparency. Reproduced all reported numerics from scratch on the raw
results JSON; cross-checked against `analysis/v2_09_compute_efdpr.py`,
`v2_10_compute_odi.py`, `v2_06_adjudication.py`, `v2_05_merge_and_kappa.py`, and
`docs/prereg-v2.md`.

## Headline assessment

The primary test is executed exactly as pre-registered (one-sided exact
binomial, $H_0: p \le 0.25$, $\alpha = 0.05$, single tolerance grid). The
primary numerics are correct to 4 decimals:

- P(X $\ge$ 15 | n = 25, p = 0.25) = **0.000215** (manuscript: 0.0002). OK.
- Clopper-Pearson 95% CI for 15/25 = **[0.3867, 0.7887]** (manuscript: 0.39-0.79
  / [0.387, 0.789]). OK.
- ESCAT/liberal P(X $\ge$ 14 | n = 25, p = 0.25) = **0.000916** (manuscript:
  0.0009). OK.
- ESMO-only P(X $\ge$ 8 | n = 16, p = 0.25) = **0.0271** (manuscript: 0.027). OK.
- ASCO-citing P(X $\ge$ 7 | n = 15, p = 0.25) = **0.0566** (manuscript: 0.057,
  reported as "marginal fail"). OK.
- NCCN-citing P(X $\ge$ 6 | n = 10, p = 0.25) = **0.0197** (manuscript: 0.020).
  OK.
- ODI bootstrap pair counts: C(80, 2) = 3,160 for `prior_CDK4_6i`. OK.
- PABAK = $2P_0 - 1$: for `akt_path` with $P_0 = 0.95$, PABAK = 0.90 (matches
  `v2_kappa_postadj.json`). OK.

The denominator $n = 25$ honours amendment v2.1's "$\ge 25$" gate. The
exact-binomial test, the rejection rule, and the tolerance-grid framing are
faithful to the prereg. The Cohen's $\kappa$ / PABAK pair is the right
diagnostic for the paradox observed on `akt_path`.

**However**, the manuscript contains (i) a power-analysis numerical error, (ii)
internal inconsistencies in the adjudication-rule count, (iii) silently dropped
pre-registered secondary outcomes S2 (temporal lag) and S3 (subgroup coverage),
(iv) an unconventional asymmetric bootstrap CI indexing, (v) honesty gaps in
the inter-rater agreement reporting, and (vi) a misleading funnel figure.
These are all addressable without re-running the primary test, but they need
to be fixed before MAJOR/MINOR can be downgraded.

---

## Concrete asks

### A1. (CRITICAL) Power-analysis numerical error in Methods.

Methods 2.7 (paragraph "Power analysis ... at $n = 25$ guideline nodes, the
test achieves ... 82% at $p_1 = 0.50$") is wrong. With $k_{\mathrm{crit}} = 11$
at $\alpha = 0.05$ (one-sided, exact-binomial, $p_0 = 0.25$) and $n = 25$, the
true exact power is:

| $p_1$ | reported (MS) | actual (recomputed) |
|---:|---:|---:|
| 0.30 | -- | 0.0978 |
| 0.35 | 23% | 0.2288 |
| 0.40 | 42% | 0.4142 |
| 0.45 | -- | 0.6157 |
| 0.50 | **82%** | **0.7878** |
| 0.60 | -- | 0.9656 |

The discussion (`discussion_v2.tex`, "Three caveats") repeats the 82% figure
verbatim. Both should read **79%** (or 78.8%). The error is small (3 percentage
points) but it is in Methods, it overstates power for the realistic effect
size, and it is trivial to fix. Please correct both occurrences and re-emit
the power table.

### A2. (HIGH) Pre-registered $n = 25$ denominator: honour the gate but note the conditioning.

The prereg-v2 amendment v2.1 sets a minimum $n \ge 25$ guideline-node gate and
commits to "whatever the deduplicated ESMO + ASCO + NCCN HR+/HER2- decision
tree yields". The realised value $n = 25$ is the minimum of the gate, not an
externally fixed denominator. Please add one sentence in Methods 2.7 stating
that the $n = 25$ denominator was the *realised* deduplicated count (gate
passed at its lower bound), not a power-target choice, and that node addition
was not adaptive on EFDPR support.

### A3. (HIGH) Adjudication-rule count: manuscript says 14, code/results say 17.

`v2_06_adjudication.py` `ADJ` list has 17 entries (verified by row count, and
`v2_kappa_postadj.json` reports `"adjudication_rules_applied": 17`). The
abstract, Methods 2.3, and the Knowledge Generated box all say "14
adjudication rules". This is either a stale number from an earlier draft or
a re-count of *unique field-paths* (8 unique field paths in `ADJ`). Pick one
definition (rules-as-decisions vs rules-as-field-paths) and use it
consistently across abstract, Methods, Results, and supplement; or report
both with explicit labelling.

### A4. (HIGH) S2 (temporal lag) and S3 (subgroup coverage) are silently dropped from v2.

`docs/prereg-v2.md` Secondary outcomes section commits to:
- **S2.** Temporal evidence lag with bootstrap CI.
- **S3.** Subgroup coverage (Asian ancestry, age $\ge 70$, Black ancestry) as
  proportions.

Neither is reported in `main_v2.tex`, `discussion_v2.tex`, or `supplement.tex`
(which is itself still the v1 16-trial document, see A7). The v1 supplement
acknowledged this as a deviation; the v2 manuscript is silent. Either:

1. Report S2 and S3 in a Supplementary Results section with descriptive
   results and (for S2, where there is a formal $H_0: \mathrm{lag} = 0$
   commitment) the BH-corrected $q$-value alongside S1, or
2. Add an explicit "Pre-registration deviations — v2" subsection to the
   manuscript main text (not just the supplement) that states S2/S3 are
   deferred, with the reason and the planned reporting venue.

Silent omission of pre-registered secondary outcomes is the single most
common cause of subsequent retraction in pre-registered work. Fix.

### A5. (HIGH) Pre-adjudication Cohen's $\kappa = 0.40$ on `post_endo` is the headline kappa story; bury it less.

`v2_kappa.json` reports `post_endo` $\kappa = 0.3985$, agreement 60%, on 20
trials. The text correctly identifies this as a literal-vs-design coding
disagreement, and adjudication brings it to $\kappa = 1.00$. The Results
section reports this honestly. Two refinements requested:

1. **Add the pre-adjudication mean key-field $\kappa$ (= 0.670) and min ($=
   0.00$) explicitly to the Results 3.1 text and to a supplementary table.**
   Currently `v2_kappa.json:passes_kappa_gate_07 = false` — the prereg gate at
   $\kappa \ge 0.70$ on key fields **fails pre-adjudication**. The manuscript
   says "Inter-annotator agreement was substantial after adjudication" but
   does not state explicitly that the prereg gate failed pre-adjudication and
   was passed only after the 17-rule adjudication pass. Per the prereg ("If
   gates fail, run a disagreement-adjudication pass and report the
   post-adjudication $\kappa$ as well") this is permitted, but it must be
   *disclosed* not glossed.

2. **Distinguish between rater drift (Annotator B's literal silent$\to$null
   policy) and protocol ambiguity (the protocol did not specify how to handle
   silent-on-endo eligibility text).** If the protocol was ambiguous, this is
   an extraction-protocol limitation, not a rater error; the manuscript should
   say so. If Annotator B mis-applied a clearly-specified rule, the
   manuscript should disclose that the adjudication essentially substituted
   Annotator A's coding for both raters. The current narrative leaves
   this ambiguous and risks a "double-counting" appearance.

### A6. (MEDIUM) Kappa-paradox + PABAK framing is statistically defensible but the manuscript should add the formal definition and one citation.

The PABAK = $2P_0 - 1$ formula is correct, the AKT-pathway case (Cohen's
$\kappa = 0.00$ at 95% raw agreement, prevalence 19/20 = 0.95 for the
"not-AKT-path" cell) is a textbook kappa-paradox, and reporting both
diagnostics is the right move. **However**, the Methods section uses "PABAK"
twice without defining it. Please:

1. Add one sentence in Methods 2.3: "We report Cohen's $\kappa$ alongside the
   prevalence-adjusted bias-adjusted kappa (PABAK = $2P_0 - 1$, Byrt 1993) to
   diagnose the well-known kappa paradox in which highly skewed marginals
   suppress $\kappa$ despite high raw agreement."
2. Cite Byrt 1993 (J Clin Epidemiol 46:423-429) or an equivalent reference;
   the current ref list does not contain a PABAK citation.
3. State the prereg-v2 gate explicitly: "$\kappa \ge 0.70$ on key fields"
   formally fails pre-adjudication (mean 0.670, AKT $\kappa = 0$), passes
   post-adjudication under PABAK (min PABAK 0.90), and *fails*
   post-adjudication under Cohen's $\kappa$ (because AKT remains at $\kappa =
   0$ post-adjudication). The current Results paragraph implies all gates
   pass; the JSON shows `"passes_gate_07_post_adjudication_cohen": false`.
   This is the single most consequential subtlety in the inter-rater
   reporting and the current draft soft-pedals it.

### A7. (MEDIUM) Supplement.tex is still the v1.0.0 document.

`manuscript/supplement.tex` describes the 16-trial pilot, the v1 prereg
deviations, and the 16-node ESMO encoding. The v2 main text cites
"Supplementary Table S1" (transparency checklist) but the supplement still
describes the v1 study. Either:

1. Rename to `supplement_v1.tex` and create a fresh `supplement_v2.tex` with:
   - v2 reporting transparency checklist (PRISMA-2020 + graph addendum
     extended to ASCO/NCCN);
   - S2/S3 deviation paragraph (per A4);
   - per-NCT filter-log table (the 874 $\to$ 74 $\to$ 80 funnel, see A8);
   - the 14/17 adjudication-rule table with rationales (per A3);
   - the full pre- and post-adjudication kappa table including the AKT
     paradox (per A5/A6).
2. Or, retitle the existing supplement to make clear it accompanies v1.0.0
   only and add a v2-only supplement.

The current state is incoherent: the main text says v2, the supplement says
v1.

### A8. (MEDIUM) Search funnel: 874 -> 74 -> 80 needs a PRISMA-style figure.

The text says "874 candidate studies; eight pre-specified filters ... yielded
74 systematic candidates" then "Six additional v1-cited foundational pivotal
trials ... were added as a disclosed supplementary set, yielding 80 trials."
`filter_log.json` gives the per-filter rejection counts:

| Filter | Reject count |
|---|---:|
| F1 phase 2/3 | 0 |
| F2 interventional | 0 |
| F3 started 2013--2026 | 210 |
| F4 metastatic setting | 20 |
| F5 HR+/HER2- population | 274 |
| F6 eligibility text retrievable | 0 |
| F7 enrolment $\ge 200$ | 259 |
| F8 primary completion $\le 2026$ | 37 |
| **Passed all** | **74** |

874 - 210 - 20 - 274 - 0 - 0 - 259 - 37 = 74. OK, arithmetic clean.

**Asks.**

1. Add a PRISMA 2020-style flow figure (or a supplement table) with these
   per-filter rejection counts. The current paragraph hides the very large
   F5 (n = 274) and F7 (n = 259) rejections behind a single "eight filters".
2. Disclose explicitly that amendment v2.1 retroactively tightened F7 from
   $\ge 50$ to $\ge 200$. The amendment text in the prereg says this; the
   manuscript does not. A reader who diffs the prereg against the code
   should see the change in both places.
3. The "six v1-cited foundational supplementary trials" addition is a
   convenience supplement and should be flagged as such. Specifically: did
   the v1-cited supplement *re-introduce* trials that the systematic search
   *would have* recovered if F3 had been wider? The amendment v2.1 already
   widened F3 to 2013; the six supplementary trials all started 2013--2014
   per the prereg text. **If the widened F3 already recovers PALOMA-2,
   OlympiAD, SOLAR-1, EMERALD, INAVO120, postMONARCH, why are they added
   *outside* the systematic pipeline?** This double-counting risk needs to
   be either (a) ruled out by listing which of the six were and were not in
   the systematic-74, or (b) acknowledged as a deviation. Per `v2_efdpr.json`
   the supporting NCTs include NCT01740427 (PALOMA-2), NCT02000622
   (OlympiAD), NCT03778931 (likely SOLAR-1 or EMERALD), etc., so this is a
   real overlap question, not a hypothetical.

### A9. (MEDIUM) Bootstrap CI indexing is asymmetric.

`v2_09_compute_efdpr.py:bootstrap_ci` uses:

```
lo = est[max(0, int(0.025*n) - 1)]
hi = est[min(n-1, int(0.975*n))]
```

For $n = 1000$: lo_idx = 24, hi_idx = 975. The lower bound subtracts 1, the
upper bound does not. The conventional 95% percentile bootstrap CI uses the
2.5th and 97.5th percentiles, which at $n = 1000$ are indices 24 and 974
(0-indexed) under the lower-of-two definition, or 25 and 975 under the
upper-of-two. Either is defensible; mixing them is not.

`v2_10_compute_odi.py:odi_with_ci` uses the same asymmetric indexing. The
manuscript's bootstrap CIs are off by one index on the high side relative to
the low side, which inflates the upper CI by ~1 ordinal position in 1,000.
The effect on the reported numbers is tiny (the strict bootstrap CI is
[0.40, 0.80] and the CP CI is [0.39, 0.79]; either rounding choice gives the
same display) but the **method**, as written, is non-standard.

**Ask.** Either:

1. Switch to `numpy.quantile(est, [0.025, 0.975])` (linear interpolation,
   industry-standard), or
2. Use symmetric ordinal indexing: `lo = est[int(0.025*n)]; hi =
   est[int(0.975*n) - 1]` (or `int((n-1)*0.025)` and `int((n-1)*0.975)`
   for the inclusive convention), and document the convention in Methods.

Either fix is one line; the inconsistency reflects badly in a paper that
asks reviewers to audit the code.

### A10. (MEDIUM) "Three tolerance levels = sensitivity grid, not three tests": say so explicitly.

Prereg-v2 step 9 of the confirmatory plan says: "The test is run **exactly
once** on the full $n$ guideline-node count, not iteratively across tolerance
levels (the three tolerance levels are a pre-registered sensitivity grid, not
three independent confirmatory tests)." The manuscript reports $P = 0.0002$
(strict) and $P = 0.0009$ (ESCAT, liberal) side-by-side in the abstract and
Results without explicitly stating that only the strict test is
confirmatory and the others are sensitivity readouts that do not require
multiple-testing correction.

**Ask.** Add one sentence in Methods 2.7 and one in Results 3.3:

> "Per the pre-registration (`prereg-v2.md` step 9), the confirmatory test
> is the strict-tolerance one-sided exact binomial test only; the ESCAT and
> liberal tolerance EFDPRs are reported as a pre-specified sensitivity grid
> on the same node set and do not enter a multiple-testing family."

Without this, a reader (or a meta-reviewer) may apply a Bonferroni/Holm
correction across the three tolerance reports and reach a different
conclusion.

### A11. (MEDIUM) ASCO-citing $P = 0.057$ marginal: report the prereg-honest interpretation.

The ASCO-citing-only by-guideline sensitivity yields $P = 0.057$ and the
manuscript says it "marginally fails to reject". Per the prereg-v2 step 9
("The test is run exactly once") the by-guideline-source sensitivity
results are *sensitivity analyses on the primary test's denominator*, not
independent confirmatory tests. They cannot, by construction, "fail to
reject" a primary hypothesis that was tested on $n = 25$. Please reframe:

> "ESMO-only and NCCN-citing subset EFDPRs remain significantly above 0.25
> at the unadjusted $\alpha = 0.05$ threshold (exact-binomial $P = 0.027$
> and 0.020 respectively); the ASCO-citing subset is at the threshold ($P
> = 0.057$). These are guideline-source sensitivity readouts, not
> independent confirmatory tests; the primary inference is on the unified
> $n = 25$ tree."

### A12. (LOW) Per-node support counts: G18 is missing from the node set; flag for the figure caption.

`v2_decision_tree.json` has node IDs G1--G17, G19--G26 (25 nodes, no G18).
The Figure 1 caption says "labelled G1--G26" which is true but visually
suggests 26 nodes. The Methods text says "25 nodes". The figure caption is
fine; the asymmetric numbering may confuse readers. Either:

1. Renumber G19--G26 to G18--G25 (clean, requires regenerating figures), or
2. Add a footnote to the figure caption: "Node identifiers G1--G17 and
   G19--G26 give a contiguous set of 25 unique decision nodes; G18 was
   removed during deduplication and is not reused."

### A13. (LOW) Liberal-tolerance $k$ is identical to ESCAT $k$: state why explicitly.

Both ESCAT and liberal tolerance yield EFDPR = 0.56 (14/25), same evidence-free
set, identical CP CI, identical $P$. The Results say "Liberal tolerance
rescues two ESR1mut nodes via registrational subgroup readouts (G5 by
EMERALD; G19 by SERENA-6); the remainder are robust to tolerance." But the
JSON shows liberal rescues only one node (G4 is rescued from strict to
ESCAT/liberal; G5 is supported in strict already by NCT03778931 and stays
supported). The narrative claims two rescues; the data show ESCAT and liberal
are identical on the strict-set. Please reconcile: either the liberal-tolerance
matcher is failing to rescue nodes the protocol intended it to rescue (a
**bug**), or the narrative is imprecise.

Concretely: G5 (strict) already has NCT03778931. G19 (strict) has no support
under any tolerance. G4 is rescued strict $\to$ ESCAT. So the actual rescue
count strict $\to$ liberal is **1**, not 2, and it's G4 (PIK3CAmut-related),
not G5 or G19. Fix the narrative or audit the matcher.

### A14. (LOW) Bootstrap by-node-resampling vs Clopper-Pearson: harmonise the primary CI.

Methods 2.7 says: "Clopper-Pearson exact CIs (recommended primary CI for
small-$n$ proportions) and 1,000-iteration percentile bootstrap CIs are
reported." The two CIs answer different questions (CP: exact for a fixed-$n$
binomial; bootstrap-by-node: resampling uncertainty about the guideline-node
*sample*). For the primary inference on a fixed decision-tree denominator,
the CP CI is the right primary; the bootstrap is a robustness check.
**Ask.** Designate one as the primary CI in Methods, the other as a
robustness CI. Currently the abstract and Results report only the CP CI for
the primary (which is the right move); the JSON `bootstrap_ci95: [0.40,
0.80]` is published but uncited in the main text. Either cite it in Results
with the framing "robustness CI" or drop it from the abstract-facing
results.

### A15. (LOW) PABAK = 0.99 is the mean PABAK *post-adjudication*; one-decimal precision in the abstract risks overclaim.

The abstract says "mean PABAK 0.99" and Results says "mean PABAK 0.99". The
JSON gives `mean_key_field_pabak_post = 0.9875`. With AKT at PABAK = 0.90
and the other seven at PABAK = 1.00, the mean is exactly 0.9875. Rounding to
0.99 is conventional but the abstract should also report the min (0.90,
AKT-pathway) so the kappa-paradox case is not invisible at the abstract
level. Suggest: "mean PABAK 0.99, min 0.90 (AKT-pathway, kappa-paradox
case)".

---

## Supplementary observations (not asks)

- The 80-trial corpus includes 64 in-scope, 12 out-of-scope, and 4
  investigational-only. The cohort table says "Pivotal HR+/HER2- mBC trials
  (frozen 2026-05-16): 64" but the abstract says "80 trials (74 systematic
  plus six v1-cited supplementary, including 64 with canonical drug-class
  assignments)". Consider one consistent number with a clear bracketed
  qualifier.

- The drug-class equivalence table (`DRUG_CLASS_EQUIVALENCE` in
  `v2_09_compute_efdpr.py`) is an explicit table per the v1 deviation log;
  good. The supplement should publish it (per A7).

- The bootstrap seed (20260516) is the same across `v2_09` and `v2_10`; the
  PRISMA filter is deterministic. Reproducibility is genuinely good.

- The pre-registration is well-written and the amendment v2.1 is genuinely
  *before* the LLM extraction. The pre-registration discipline is a
  strength.

---

## VERDICT

**MAJOR** revision required. The pre-registered confirmatory inference is
solid and the primary numerics reproduce exactly. The MAJOR drivers are:

1. (A1) Power-analysis numerical error (82% should be 79%).
2. (A4) Silently dropped pre-registered secondary outcomes S2 and S3.
3. (A5/A6) Inter-rater agreement reporting elides the fact that the
   pre-registered $\kappa \ge 0.70$ gate **fails** pre-adjudication and
   passes only under PABAK post-adjudication (Cohen's $\kappa$
   post-adjudication still fails because AKT remains at 0).
4. (A7) v2 supplement is missing — the existing supplement is still the v1
   document.
5. (A8) Funnel description hides the actual 874 -> 74 -> 80 attrition and
   does not address the systematic-vs-supplementary overlap on the six
   v1-cited additions.

All five are fixable without re-running the primary test, and none threatens
the conclusion (EFDPR $> 0.25$ at $\alpha = 0.05$ is firmly supported by
$P = 0.000215$ on a correctly executed pre-registered test). On a clean
MINOR-revision pass these would all be straightforward to fix; the volume
and the
fact that several touch pre-registration honesty pushes this into MAJOR.

If the round-2 submission addresses A1, A3, A4, A5, A6, A7, A8, and A10 in
full and the others in some form, I will recommend ACCEPT.
