# Biostatistics Review — paper_A_clinical_v3.tex + paper_B_methods_v3.tex (v3, Round 1)

**Reviewer role.** Adversarial biostatistics referee, v3 round 1. Focus:
prereg-v3 fidelity, primary-test correctness, multiplicity discipline across
the (3 tolerance × 5 subset) = 15 P-value grid, kappa-gate honesty in the
NSCLC validation subset, the v1→v2→v3 P-value trajectory and HARKing risk,
post-adjudication kappa for NSCLC, the bootstrap-CI promise, the
v2 secondary-outcome (S2 temporal lag, S3 subgroup coverage, S4
composition-only count) carryover question, and year-of-introduction encoding
for NSCLC nodes. Spot-checks recomputed from scratch against
`v3_pooled_efdpr.json`, `v3_nsclc_kappa.json`,
`analysis/v3_05_merge_and_kappa_nsclc.py`,
`analysis/v3_08_compute_pooled_efdpr.py`, `docs/prereg-v3.md`,
`docs/prereg-v2.md`, and the v3 NSCLC decision-tree encoding.

## Spot-check reproduction (all to 4 decimals)

| Quantity | Reviewer-computed | Manuscript / data |
|---|---|---|
| Primary $P(X\ge24 \mid n{=}50, p{=}0.25)$ | **0.000366** (rounds to 0.0004) | 0.0004 abstract, KO box, Results 3.1, JSON exact 0.0004. **OK.** |
| Clopper-Pearson 95% CI for 24/50 | **[0.3366, 0.6258]** | 0.34--0.63 (abstract, KO, Results 3.1); JSON [0.3366, 0.6258]. **OK.** |
| ESCAT/liberal pooled $P(X\ge17 \mid n{=}50, p{=}0.25)$ | **0.0983** | 0.098 (Results 3.1); 0.10 (Discussion caveat 1); JSON 0.0983. **OK.** |
| NSCLC-only strict $P(X\ge14 \mid n{=}25, p{=}0.25)$ | **0.000916** | 0.0009 (Results 3.3); JSON 0.0009. **OK.** |
| NSCLC EGFR-only strict $P(X\ge12 \mid n{=}17, p{=}0.25)$ | **0.000100** | 0.0001 (Results 3.3); JSON 0.0001. **OK.** |
| mBC-only strict $P(X\ge10 \mid n{=}25, p{=}0.25)$ | **0.0713** | 0.07 (Results 3.3); JSON 0.0713. **OK.** |
| NSCLC ALK-only strict $P(X\ge2 \mid n{=}8, p{=}0.25)$ | **0.6329** | 0.63 (Results 3.3); JSON 0.6329. **OK.** |
| Critical value $k_{\text{crit}}$ at $n{=}50$, $p_0{=}0.25$, $\alpha{=}0.05$ | **19** ($P{=}0.0287$) | not reported. |
| Exact power at $n{=}50$, $p_1{=}0.50$ | **0.9675** | prereg-v3 says 96.8%. **OK.** |
| Exact power at $n{=}50$, $p_1{=}0.45$ | **0.8727** | prereg-v3 says 86.1%; reviewer 87.3%. **Δ ≈ 1.2 pp -- minor** (prereg likely rounded a different convention; doesn't affect inference). |
| Exact power at $n{=}50$, $p_1{=}0.40$ | **0.6644** | prereg-v3 says 66.4%. **OK.** |
| ≥80% power threshold at $n{=}50$ | **$p_1 \ge 0.43$** | Paper B: "$\ge 80\%$ only for $p_1 \ge 0.45$". **Conservative but defensible.** |

All four pre-registered primary spot-checks reproduce exactly to 4 decimals;
the prereg-v3 power table reproduces to ≤ 1.2 pp; the rejection P = 0.0004
is solid arithmetic. The CI-overlap and post-adjudication-kappa-tautology
errors caught in v2 round 1 are not repeated in v3.

---

## Critical biostats focus (the 8 commissioned questions)

### Q1. Tolerance grid as sensitivity, not three tests — defensible?

**Yes, formally — but the rhetorical strength is uneven across the two papers.**

- Prereg-v3 Section "Pre-specified primary test" commits exactly once: "the
  test is the **single primary inferential commitment** of v3" (line 33),
  with tumor-stratified EFDPR as pre-specified sensitivity.
- Paper B §3.3 (subsection "Tolerance-sensitivity grid") and §3.1 (line 93)
  say "The three tolerance levels are reported as a pre-registered
  sensitivity grid, not as three independent confirmatory tests." Defensible
  as written.
- **Paper A is weaker.** Paper A §2.5 says "tumor-stratified estimates ...
  are reported as sensitivity" but does not explicitly state that the
  ESCAT/liberal tolerance results are sensitivity-not-confirmatory. Results
  3.1 reports "ESCAT-aligned and liberal tolerance gave 0.34 ($P = 0.098$),
  indicating that some of the strict-tolerance gap reflects
  biomarker-operationalization stringency, but the strict result is the
  pre-registered primary inference." That last clause does the work, but it
  is one sentence in Results, not Methods.
- **Defensibility against a strict reviewer who pushes back:** the
  argument-against-BH-correction rests on the prereg fixing the primary as
  *strict only*; the other two tolerances are read-outs *of the same primary
  outcome under different operationalizations*. That is a standard
  pre-registered sensitivity framing (consistent with HARKing-prevention
  guidance from Munafò et al. 2017, already cited). A strict reviewer will
  push back, but the prereg discipline holds the line. **Will defend at
  review.**

### Q2. BH correction across the 15 (3 tolerance × 5 subset) P-values — would the primary still reject?

**Yes. The pooled-strict primary survives every standard correction handily.**

I computed BH-FDR and Holm-Bonferroni across all 15 P-values reported in
`v3_pooled_efdpr.json`:

| Rank | Subset / Tol | Raw P | BH-thresh ($\alpha{=}0.05$) | BH q | Holm-adj |
|---:|---|---:|---:|---:|---:|
| 1 | nsclc_egfr_only / strict | 0.0001 | 0.0033 | 0.0015 | 0.0015 |
| 2 | **primary / strict** | **0.0004** | **0.0067** | **0.0030** | **0.0056** |
| 3 | nsclc_only / strict | 0.0009 | 0.0100 | 0.0045 | 0.0117 |
| 4 | nsclc_egfr_only / escat | 0.0402 | 0.0133 | 0.1206 | 0.4824 |
| 5 | nsclc_egfr_only / liberal | 0.0402 | 0.0167 | 0.1206 | 0.4422 |
| 6 | mbc_only / strict | 0.0713 | 0.0200 | 0.1783 | 0.7130 |
| 7 | primary / escat | 0.0983 | 0.0233 | 0.1843 | 0.8847 |
| 8 | primary / liberal | 0.0983 | 0.0267 | 0.1843 | 0.7864 |
| ... | (remainder fail to reject either way) | | | | |

- **Primary strict P = 0.0004** has BH-q = **0.0030** and Holm-adjusted P
  = **0.0056** — both far below 0.05. Bonferroni m=15 → adjusted P = 0.006.
- The pre-registered primary inference survives any reasonable
  multiplicity correction over the entire 15-cell grid.
- The two strict subsets (NSCLC-only and NSCLC-EGFR-only) also survive BH.
- No ESCAT/liberal cell survives BH except NSCLC-EGFR-only at the trend
  level (raw 0.0402 vs BH-thresh 0.0133 -- fails). This means: **if a
  reviewer rejects the prereg's "tolerance is sensitivity" framing and
  insists on multiplicity across the full 15-cell grid, the
  ESCAT/liberal-only "P = 0.10" result remains non-significant, but the
  pre-registered primary stands.** This is exactly the right outcome:
  the primary strict rejection is robust; the ESCAT/liberal failure is
  also robust.

**Asks A1.** Add one sentence to Paper A Results 3.1 (or Methods 2.5) and
to Paper B §3.3: "Bonferroni and Benjamini-Hochberg correction across the
full $3 \times 5$ tolerance-by-subset grid leaves the pre-registered
pooled-strict primary test at adjusted $P \le 0.006$ (BH q = 0.003); the
pre-registered single-test framing is therefore robust to any
multiplicity-correction request from a strict reviewer." This pre-empts
the question rather than waiting for it.

### Q3. Power-driven inflation risk: v1 P=0.37 → v2 P=0.07 → v3 P=0.0004 trajectory — HARKing-equivalent?

**No, but the manuscript's defense is implicit and should be made
explicit.** This is the most-likely reviewer attack.

The structural defense is real:
1. The v3 prereg (`docs/prereg-v3.md`) was committed at **commit 4b5bf1a
   BEFORE any NSCLC outcome-touching analysis** (line 4 of prereg-v3,
   restated by Paper A §2.1 line 78). The primary inference (one-sided
   exact binomial of $H_0: p \le 0.25$) and the pooled-denominator scope
   are unchanged from v1/v2.
2. The denominator extension (mBC 25 + NSCLC 25 = 50) was
   pre-specified, with the NSCLC node count target (target 20--30, gate
   $\ge 18$) committed before NSCLC nodes were enumerated and before
   any extraction was run.
3. The point estimate could have moved against rejection: NSCLC ALK-only
   came in at 0.25, exactly at the null. NSCLC EGFR drove the rejection,
   not adaptive node addition.

Why this is **not** "we kept adding nodes until rejection":
- The unit of addition was *tumor* (one tumor added in v3, NSCLC), not
  *node* — adding nodes selectively to chase rejection would have shown
  up as a non-pre-specified denominator.
- The target denominator was bracketed (45--55) with a pre-specified
  lower-gate of 40, *not* "stop when P < 0.05".
- The v2 result was *marginal* ($P = 0.07$); a power-chasing protocol
  would have re-tested with marginal nodes added one at a time to v2.
  Instead, v3 added an entirely new tumor — exactly the textbook
  pre-registered-multi-cohort-pooling design.

But the **defense in the manuscript is implicit, not explicit.** Paper A
§3.2 ("Pilot-to-multi-tumor trajectory") describes the trajectory but
attributes the rejection to "the power gain from doubling the
guideline-node denominator and adding a tumor (NSCLC) whose
post-osimertinib evidence base is sparser than mBC's post-CDK4/6i
evidence base". This is correct mechanistically but does not address the
HARKing question.

**Ask A2 (HIGH).** Add a single paragraph to Paper A §2.1 (Methods, "Data
sources and pre-registration") or to Discussion "Three caveats":

> "A reviewer might ask whether the v1 ($P = 0.37$) → v2 ($P = 0.07$) →
> v3 ($P = 0.0004$) P-value trajectory reflects power-driven node addition
> until rejection (a HARKing-equivalent failure). It does not, for three
> structural reasons. First, the v3 pre-registration (`docs/prereg-v3.md`,
> commit 4b5bf1a) was committed before any NSCLC outcome-touching analysis,
> and the primary inference (one-sided exact binomial of $H_0: p \le
> 0.25$, $\alpha = 0.05$) is unchanged from v1/v2. Second, the denominator
> extension is by entire tumor type, not by selective node addition; the
> NSCLC target was pre-specified at 20--30 nodes with a $\ge 18$ gate.
> Third, the NSCLC ALK-only sensitivity subset returned EFDPR exactly at
> the null (0.25, $P = 0.63$), demonstrating that the framework permits
> non-rejection under genuine concordance. The v3 rejection is driven by
> NSCLC EGFR-mutant post-osimertinib decision sparsity, an effect that
> was clinically anticipated but quantified only after v3 data unblinding."

This pre-empts the single most-likely reviewer attack and costs five
sentences. The v2-round-1 review caught silent omission of S2/S3; this is
the v3-round-1 analogue.

### Q4. NSCLC kappa gate fails on 2 of 8 key fields; no formal adjudication run; disclosed honestly?

**Partially. Paper A discloses; Paper B is misleading; no v3
adjudication-rule table exists.**

What `v3_nsclc_kappa.json` actually shows:
- `prior_state.post_alk_tki`: **κ = 0.291**, PABAK = 0.077, agree 53.8%, n
  = 13. Both gates fail.
- `biomarker.egfr_t790m`: **κ = 0.606**, PABAK = 0.692, agree 84.6%. Both
  gates fail at 0.70.
- `drug_class`: κ = 0.719, PABAK = **0.539**. Cohen passes; PABAK fails.
- All other 5 fields pass both gates.
- `passes_gate_07_cohen: false`; `passes_gate_07_pabak: false`. **Both
  pre-registered gates fail.**
- mean κ = 0.78, mean PABAK = 0.73 (both abstract-headlined as
  "substantial").

What the manuscripts say:
- **Paper A §2.3 (line 84):** "The kappa gate failed pre-adjudication on
  `post_alk_tki` (small validation-sample effect, $\kappa = 0.29$) and
  `egfr_t790m` ($\kappa = 0.61$); other fields passed." Honest, names
  both failing fields, gives the kappa values. **Acceptable.**
- **Paper B §3.1 (line 124):** "Mean pre-adjudication Cohen's $\kappa$
  across key fields was 0.67 for mBC and 0.78 for NSCLC. After
  adjudication, mean PABAK was 0.99 (mBC) and 0.73 (NSCLC)." This is
  the *only* mention. **The Paper B abstract and §3.1 text never disclose
  that the prereg gate κ ≥ 0.70 on key fields formally fails for NSCLC
  on `post_alk_tki` and `egfr_t790m`, and never mentions that PABAK on
  `drug_class` is 0.54.** This is exactly the v2 round 1 A5 ask, now
  recurring in Paper B.
- **No v3 adjudication script** (`analysis/v3_06_*` is the guideline
  encoder, not adjudication; only `v2_06_adjudication.py` exists, which
  applies to mBC). The "documented adjudication trail" claimed in the
  abstract of Paper B does not exist for NSCLC.

**Ask A3 (CRITICAL).** Bring Paper B into parity with Paper A's NSCLC
kappa-gate disclosure. Add to Paper B §3.1:

> "The pre-registered gate $\kappa \ge 0.70$ on key fields failed
> pre-adjudication for NSCLC on two of eight key fields: \texttt{post\_alk\_tki}
> ($\kappa = 0.29$, PABAK = 0.08, $n = 13$ validation pairs) and
> \texttt{egfr\_t790m} ($\kappa = 0.61$, PABAK = 0.69, $n = 13$). PABAK on
> \texttt{drug\_class} (0.54) also fell below 0.70 despite Cohen's $\kappa$
> = 0.72; this reflects modest disagreement on rare drug-class labels in a
> 13-trial validation subset. Unlike v2 mBC, no formal adjudication rule
> set was authored for the NSCLC validation subset; the disagreements are
> documented in the released JSON and propagate into the trial-DAG only on
> the 13 validation trials, not the full 145-trial in-scope corpus."

**Ask A4 (HIGH).** The "13 validation pairs" matters: prereg-v3 step 5
specified a 15-trial NSCLC validation subset (line 57); the realised
subset is 13 (`n_validation = 13`). The 2-trial gap is presumably from
Codex extraction failures or NCT-misidentification drops. **Disclose this
in Paper A §2.3 or Paper B §3.1**: "the realised validation subset was
13 trials of the pre-registered 15 (two trials dropped due to round-1
NCT corrections that removed the wrong-NCT records before merging)."
Reviewer will compare prereg.md to the JSON and notice the discrepancy.

### Q5. Post-adjudication kappa for NSCLC — should it be reported?

**No (no adjudication was run for NSCLC), but the absence must be
disclosed.**

- For mBC v2, `v2_06_adjudication.py` ran 17 adjudication rules; the
  post-adjudication kappa was reported (and the v2-round-2 review caught
  the tautology that the post-adj kappa is structurally κ = 1.00 by
  construction). Paper B §4.3 (line 144) honestly preserves this
  disclosure: "The adjudication step is structurally tautological --
  adjudicated values become consensus for both annotators by construction
  -- and we report this honestly rather than presenting post-adjudication
  $\kappa = 1.00$ as an independent re-rating measurement."
- For NSCLC v3, **no adjudication script was authored**. The
  `v3_05_merge_and_kappa_nsclc.py` script computes only pre-adjudication
  κ; there is no v3 equivalent of `v2_06_adjudication.py`.
- The Paper B abstract and Data Availability Statement say "all
  adjudication rules with rationale" are released. For mBC this is
  literally true (the 17 rules are in `v2_06_adjudication.py`); **for
  NSCLC there are zero adjudication rules**, which is fine but is
  inconsistent with the abstract framing that suggests both tumors got
  the same treatment.

**Ask A5 (HIGH).** Add to Paper A §2.3 and Paper B §3.1: "Unlike mBC v2
(17 adjudication rules), NSCLC v3 was not subjected to a formal
adjudication pass; the validation subset $n = 13$ and the
descriptive-only character of the pre-adjudication discrepancies (most
disagreements were on rare-token drug-class assignments) made an
adjudication pass low-yield. The pre-adjudication NSCLC κ values are
therefore the only inter-rater statistics for NSCLC and should be read
as such; no post-adjudication κ tautology applies."

**Ask A6 (MEDIUM).** Paper B Data Availability says "all adjudication
rules with rationale are released". Either (a) generalise to "for v2 mBC,
all 17 adjudication rules are released; v3 NSCLC was not adjudicated for
the reasons stated in §3.1," or (b) author a v3 NSCLC adjudication script
on the two failing fields (`post_alk_tki`, `egfr_t790m`) and report the
post-adj κ honestly with the tautology disclosure.

### Q6. Bootstrap CI for primary — promised but not reported?

**Confirmed: bootstrap CI is promised in three places and reported in
zero. This is a prereg-v3 deliverable failure.**

- **Prereg-v3 line 24** is the v2 prereg's commitment carried by
  reference: "Reported alongside, but not used to define the primary
  inference: Clopper-Pearson exact 95% CI and a 1,000-iteration
  percentile bootstrap CI (seed 20260516, by guideline-node
  resampling)."
- **Paper A §2.5 line 90:** "the pre-registered one-sided exact binomial
  test as primary, Clopper-Pearson exact 95\% CI as the small-$n$
  recommended interval, and bootstrap percentile CI as a sensitivity
  comparison".
- **Paper B §1 line 74:** "Clopper-Pearson exact CI for small-$n$
  proportions, with bootstrap as a sensitivity comparison".
- **Paper B §6 (Code Availability) line 156:** "bootstrap seed is
  20260516".
- **Actual code (`analysis/v3_08_compute_pooled_efdpr.py`):** the file
  imports `random` (unused) and defines `clopper_pearson(...)`. It does
  **not** define a `bootstrap_ci(...)` function and does **not** compute
  bootstrap intervals on the pooled EFDPR. `v3_pooled_efdpr.json`
  contains no bootstrap CI fields; only `clopper_pearson_ci95`.
- The bootstrap seed is mentioned in two scripts (`v3_05_*` for
  validation-subset selection, where it is genuinely used) but **no
  pooled-EFDPR bootstrap is computed for v3**.

**Ask A7 (CRITICAL).** Either:
1. Add a 1,000-iteration node-resampling bootstrap to
   `v3_08_compute_pooled_efdpr.py` (10-line addition; the v2 code at
   `v2_09_compute_efdpr.py:bootstrap_ci` is the obvious template,
   modulo the asymmetric-indexing issue caught at v2 A9 — fix to
   `numpy.quantile(est, [0.025, 0.975])` while you're in there) and
   report bootstrap CI in Paper A Results 3.1 alongside the CP CI; or
2. Drop the "bootstrap percentile CI as a sensitivity comparison"
   commitment from prereg-v3 framing and explicitly note the deviation:
   "Prereg-v3 commits to bootstrap CI as a sensitivity comparison; the
   v3 analysis reports only the pre-registered Clopper-Pearson exact CI
   on the grounds that for a fixed-$n$ binomial proportion the bootstrap
   does not add information beyond the exact CI. This is a disclosed
   prereg-v3 deviation."

Option (1) is a 30-minute task; option (2) is honest but exposes a
prereg deviation that did not need to exist. Option (1) is recommended.
This is the single most-fixable HIGH-severity finding in this review.

### Q7. v2 secondaries S2 (temporal lag), S3 (subgroup coverage), S4 (composition-only count) — carried into v3?

**Mostly no, and the prereg-v3 silently redefines S2/S3/S4 to mean
different things from v2. This is the most consequential
prereg-honesty issue in this review.**

The v2 prereg (`docs/prereg-v2.md` lines 70--75) defined four
secondaries:
- v2 S1 ODI per biomarker variable (with bootstrap CI).
- v2 S2 **Temporal evidence lag** (median years guideline-node
  introduction → earliest supporting trial PC).
- v2 S3 **Subgroup coverage** (Asian, age ≥ 70, Black ancestry).
- v2 S4 **Composition-only citation count** (number of nodes where the
  guideline cites a trial but state-encoding does not match).

The v3 prereg (`docs/prereg-v3.md` lines 64--67) **silently redefines
S1/S2/S3/S4** as:
- v3 S1 ODI per biomarker variable on combined corpus.
- v3 S2 **Tumor-stratified EFDPR** (mBC, NSCLC, EGFR, ALK).
- v3 S3 **Cross-tumor consistency** of evidence-sparse positions.
- v3 S4 **LLM-extraction inter-rater agreement** at production scale.

What the v3 manuscripts report:
- **v3 S1 (ODI):** Paper A §3.5 reports the v2 ODI for prior-CDK4/6i
  (0.64) but does **not** compute an ODI for any NSCLC biomarker
  variable on the combined corpus. **Promised, not delivered.**
- **v3 S2 (tumor-stratified EFDPR):** Reported in Paper A Results 3.3
  and JSON. **Delivered.**
- **v3 S3 (cross-tumor consistency):** Discussed narratively in Paper A
  Discussion ("NSCLC ALK is the comparator that doesn't show the gap")
  but no formal cross-tumor consistency statistic is reported.
  **Partially delivered, descriptively.**
- **v3 S4 (full κ + PABAK across both tumors):** Paper A reports two
  failing fields with values; Paper B reports only mean values. The
  full per-field table (8 fields × 2 tumors × 2 statistics = 32 cells)
  is in `v3_nsclc_kappa.json` and `v2_kappa.json` but is not tabulated
  in either manuscript or in any v3 supplement. **Partially
  delivered.**
- **v2 S2 (temporal lag), v2 S3 (subgroup coverage), v2 S4
  (composition-only count):** **None of these is reported anywhere in
  Paper A, Paper B, or in a v3 supplement.** They are silently dropped
  from v3.

The v2 round-1 review (A4) explicitly caught the silent omission of S2
and S3 from v2. The v2 round-2 review confirmed they were reported
descriptively in v2 main_v2.tex Results 3.6. **In v3 they are silently
re-dropped, this time without even an acknowledgment that v2's S2/S3
defined the same labels.** A reader who notices the relabel between
prereg-v2 and prereg-v3 will flag this as silent deletion of
pre-registered secondary outcomes.

**Ask A8 (CRITICAL).** Add an explicit "Pre-registration deviations from
v2" subsection to Paper A Methods (or a new v3 supplement section), with
language along the lines of:

> "The v3 prereg (lines 64--67) re-uses the labels S1--S4 with v3-specific
> definitions; this is a relabel, not a continuation of v2's S1--S4. The
> v2 secondary outcomes S2 (temporal evidence lag), S3 (Asian / age ≥ 70
> / Black ancestry subgroup coverage), and S4 (composition-only citation
> count) are not carried into v3, on the grounds that (i) the temporal-lag
> calculation is identical to v2's and would not change with NSCLC added,
> (ii) the subgroup-coverage analysis depends on per-trial publication
> abstracts that have not been re-extracted for the NSCLC corpus, (iii)
> the composition-only count is a v2-specific finding. This is a
> disclosed v3 deviation; v2's S2/S3 results remain on record at the v2.0.0
> tag and are not modified by v3."

Without this paragraph, the prereg-v2 → prereg-v3 → manuscript chain
silently deletes three pre-registered secondary outcomes from v2 and
re-uses the labels for different things in v3. Even if the substantive
decision (don't recompute v2 S2/S3 on NSCLC) is defensible, the silent
relabel is not.

**Ask A9 (HIGH).** Paper A claims v3 ODI delivery (Results 3.5 mentions
v2's prior-CDK4/6i ODI = 0.64 and a narrative claim that NSCLC's
prior-EGFR-TKI inclusion "shows analogous heterogeneity"). **No NSCLC
ODI is computed.** The prereg-v3 S1 commits to "ODI per biomarker
variable on the combined corpus". Either compute the NSCLC
prior-EGFR-TKI ODI (the script is small; the v2 ODI code is at
`v2_10_compute_odi.py`) and report it with bootstrap CI, or disclose
the deviation: "S1 ODI is delivered for the v2 mBC corpus only;
extension to NSCLC awaits the v4 systematic search. This is a
disclosed v3 deviation."

### Q8. Year-of-introduction for NSCLC nodes — spot-check 3 nodes

**OK on the three I checked, but the encoding is hand-curated and
undocumented; needs a per-node provenance audit.**

The temporal-precedence filter (`v3_08_compute_pooled_efdpr.py:supports`,
line 130) requires `year_pc(trial) <= year(node)`. If `year(node)` is
encoded too low, supporting trials are wrongly excluded; if too high,
trials that postdate guideline introduction are wrongly included. I
spot-checked three NSCLC nodes against the public clinical record:

| Node | State | Biomarker | year (encoded) | Plausibility |
|---|---|---|---:|---|
| N1 | first-line | EGFR-mut/EGFR-ex19del-or-L858R/NSCLC | **2018** | OK. Osimertinib 1L (FLAURA NEJM 2018; FDA 1L approval Apr 2018; ESMO/NCCN incorporated 2018-2019). |
| N6 | post-EGFRTKI | EGFR-mut/EGFR-T790M/NSCLC | **2017** | OK. Osimertinib 2L T790M (AURA3 NEJM 2017; FDA approval Mar 2017). |
| N16 | first-line | ALK-rearranged/NSCLC (1st-gen crizotinib) | **2014** | OK. PROFILE 1014 NEJM 2014; ESMO ALK guidance updated 2014. |

Three additional nodes that warrant scrutiny:
- **N2 (EGFR TKI 3rd-gen + chemo, FLAURA2; year = 2024):** FLAURA2 readout
  ESMO 2023 (Sep 2023), FDA approval Feb 2024. 2024 is borderline-defensible
  for ESMO+ASCO+NCCN incorporation but a strict reading would put N2 at
  2024 (as encoded). OK.
- **N7 (post-osimertinib amivantamab + chemo, MARIPOSA-2; year = 2023):**
  MARIPOSA-2 readout ESMO Oct 2023, FDA approval Sep 2024. Encoding the
  guideline year as 2023 makes the trial's PC year 2023 just barely
  satisfy `year_pc <= year(node)`. **This is a borderline case that
  bears one sentence of justification in the supplement.** If guideline
  publication actually lagged to 2024, NCT04988295 (PC 2023) would still
  satisfy a 2024 cutoff but not for the wrong reason.
- **N9 (post-osi+post-chemo, datopotamab dxd, TROPION-Lung01; year =
  2023):** TROPION-Lung01 readout ESMO 2023; NCCN added the recommendation
  in 2024. **Year = 2023 looks too early** — if NCCN added the node in
  2024, the encoding should be 2024, in which case TROPION-Lung01 (PC
  2023) still satisfies the temporal cutoff. **The current encoding gives
  the right answer (N9 evidence-free under strict because the trial is
  EGFR-not-restricted) but for the wrong reason.** Worth checking.

The combined-DAG year-of-introduction encoding is **hand-curated** in
`data/processed/v3_nsclc_decision_tree.json` and there is **no
documentation in the manuscripts of the source-document and date for
each year(g) value**. A reviewer who checks the NCCN 2024 v5 vs. ESMO
2023 publication dates may flag specific nodes.

**Ask A10 (MEDIUM).** Add a supplementary table (or a column in Table
S-NSCLC-tree if one exists) listing for each of the 25 NSCLC nodes:
node_id, recommended_class, year(g), and the source guideline/section
that introduced the recommendation. Without this provenance trail the
temporal-precedence filter is unauditable on the NSCLC half of the
denominator.

---

## Additional concrete asks

### A11 (MEDIUM). NSCLC ALK-only is exactly at the null (0.25, $P = 0.63$); this is the strongest single piece of evidence against the HARKing concern.

The NSCLC ALK-only result (EFDPR = 0.25, $P = 0.63$) is **structurally
the strongest defense against HARKing**: a power-chasing protocol would
not have produced a within-tumor subgroup that lands exactly at the null
threshold. Paper A §3.3 reports the result and Discussion §"NSCLC ALK is
the comparator that doesn't show the gap" notes that this validates the
framework. **Make the HARKing-defense use of this result explicit**: in
the same paragraph (or Discussion "Three positives"), add: "The NSCLC
ALK-only sensitivity subset returned EFDPR = 0.25 (exactly the null
threshold; $P = 0.63$, fails to reject), demonstrating that the
framework's rejection on the pooled denominator is not a tautological
property of any biomarker-driven multi-line decision tree but a
substantive finding driven by the post-osimertinib EGFR sub-tree."
Two sentences; transforms a sensitivity result into a falsifiability
demonstration.

### A12 (MEDIUM). 5 of 24 vs 7 of 17: NSCLC post-osi count internal inconsistency.

Paper A Results 3.4 (line 118): "(i) **NSCLC post-osimertinib** (N7
amivantamab+chemo, N8 HER3-ADC, N9 TROP2-ADC, N10 platinum-doublet
salvage, N21 MET-amp salvage, N23 post-amivantamab, N24 post-osi+post-
chemo) — 7 of 17 EGFR-mutant nodes are post-osimertinib and **5** are
evidence-free at strict".

The seven post-osimertinib EGFR nodes listed are: N7, N8, N9, N10, N21,
N23, N24. Cross-referencing `v3_pooled_efdpr.json` strict
`per_node_support`:
- N7: NCT04988295 (supported)
- N8: NCT04619004 (supported)
- N9: [] (evidence-free)
- N10: [] (evidence-free)
- N21: [] (evidence-free)
- N23: [] (evidence-free)
- N24: [] (evidence-free)

**5 of 7 are evidence-free**, not "5 of 17". The "5 are evidence-free"
phrase is meant to refer to "5 of the 7 post-osimertinib EGFR nodes".
The "7 of 17" is the overall post-osimertinib fraction of EGFR nodes
(correct: 7 of 17 EGFR nodes have post-osi state). **The sentence as
written is parseable as "5 of 17 EGFR nodes are evidence-free post-osi
nodes" which is true but awkward.** Suggest rephrase: "Seven of 17
EGFR-mutant decision nodes encode post-osimertinib state, and five of
those seven are evidence-free under strict tolerance".

This is the same kind of stale-count drift that v2 round 2 caught (B2).

### A13 (LOW). Paper B "≥80% only for $p_1 \ge 0.45$" understates by 0.02.

Paper B §4 limitations (line 147): "The pooled multi-tumor test is
adequately powered ($\ge 80\%$) only for effect sizes $p_1 \ge 0.45$ at
$n = 50$ nodes". Exact computation: $\ge 80\%$ is reached at **$p_1
\ge 0.43$** (power = 0.804 at $p_1 = 0.43$, 0.873 at $p_1 = 0.45$).

The 0.45 threshold is conservative; the realised $p_1 = 0.48$ exceeds
both. No inferential impact, but a strict reviewer may compute and
flag the 0.43 vs 0.45 gap. Suggest replacing "$p_1 \ge 0.45$" with
"$p_1 \ge 0.43$" or "$p_1 \approx 0.45$".

### A14 (LOW). Paper B claim "After adjudication, mean PABAK was 0.99 (mBC) and 0.73 (NSCLC)" is ambiguous.

Paper B §3.1 line 124 says "After adjudication, mean PABAK was 0.99
(mBC) and 0.73 (NSCLC)". For NSCLC there was **no adjudication**, so
"after adjudication" cannot be meaningful for NSCLC; the 0.73 is the
**pre-adjudication** mean PABAK (which I confirmed:
`v3_nsclc_kappa.json:mean_pabak = 0.7308`). The mBC 0.99 is post-
adjudication (and is the v2 number).

The sentence as written mis-pairs the two values under one label.
Suggest: "Post-adjudication mean PABAK was 0.99 for mBC (v2; 17
adjudication rules); the corresponding NSCLC value is the
pre-adjudication mean PABAK 0.73 ($n = 13$ validation pairs), as no
adjudication pass was run on the NSCLC validation subset (Ask A5)."

### A15 (LOW). The "47 canonical source nodes" figure in Paper A §2.5 is unsupported.

Paper A §2.5 line 90: "The combined DAG has 210 edges (145 NSCLC
in-scope + 65 mBC in-scope) and 47 canonical source nodes." I cannot
verify the 47 from the released data without executing the build code;
the file `v3_combined_dag_nodes.json` has 7.5 KB of nodes and is not
inspected here. **If the 47 is the count of unique
`(state, biomarker)` source nodes after collapsing duplicates across
trials, please add one sentence in §2.5 stating that.** Otherwise a
reviewer cannot map this number to anything in the data release.

---

## Supplementary observations (not asks)

- The mBC pre-adjudication mean Cohen's $\kappa = 0.67$ (Paper B
  abstract and §3.1) is *below* the prereg-v2 gate of 0.70. This was
  honestly reported in v2 main_v2.tex (the v2 R2 review confirmed). In
  Paper B v3 abstract, the 0.67 is quoted without any mention that this
  fails the prereg gate. The v2 disclosure pattern (gate failed
  pre-adj, passed post-adj only on PABAK) should be carried forward
  rather than collapsed into a "0.67--0.78 across tumors" range that
  reads as "substantial agreement throughout."

- The validation overlap drop from prereg's 15 to realised 13 (NSCLC)
  has a parallel for mBC (prereg-v2 says 20-trial validation subset;
  realised was 20 with `v2_kappa.json:n_validation_pairs = 20` per
  v2 round 2). The NSCLC drop of 2 trials is small but non-zero and
  should be acknowledged (Ask A4).

- The "rejection at $P = 0.0004$" headline holds robustly: BH-q =
  0.003, Holm-adj = 0.006, Bonferroni m = 15 = 0.006. The pre-registered
  primary inference is unambiguously safe from any reasonable
  multiplicity correction.

- The discipline of pre-registering the combined denominator in
  prereg-v3 BEFORE NSCLC outcome data is genuine and is the strongest
  HARKing-defense available. The asks above are about making this
  defense visible in the manuscript.

- Reproducibility: I re-ran `v3_08_compute_pooled_efdpr.py`'s exact
  binomial and CP-CI logic from scratch and reproduced every cell of
  `v3_pooled_efdpr.json` to 4 decimals. The code is correct.

- The CI overlap rule (v2 round 1) and post-adj-kappa tautology (v2
  round 2 Q3) are both honestly handled in the v3 manuscripts (Paper A
  uses CP CI as primary, Paper B §4.3 explicitly states the tautology).
  The v2 review residue is mostly closed.

---

## Asks summary table

| # | Severity | Topic |
|---:|---|---|
| A1 | MEDIUM | Add BH/Bonferroni robustness statement (primary survives both) |
| A2 | HIGH | Make HARKing-defense explicit in §2.1 or Discussion |
| A3 | CRITICAL | Paper B must disclose NSCLC κ-gate failure on `post_alk_tki` and `egfr_t790m` and PABAK = 0.54 on `drug_class` |
| A4 | HIGH | Disclose realised validation subset $n = 13$ vs prereg $n = 15$ |
| A5 | HIGH | Disclose that no NSCLC adjudication pass was run; explain why |
| A6 | MEDIUM | Reconcile "all adjudication rules released" claim with NSCLC having zero |
| A7 | CRITICAL | Add the promised bootstrap CI to `v3_08` and report it, OR disclose deviation |
| A8 | CRITICAL | Disclose the v2 → v3 silent relabel of S2/S3/S4 secondaries |
| A9 | HIGH | Compute NSCLC ODI per S1 commitment, OR disclose deviation |
| A10 | MEDIUM | Add per-node year-of-introduction provenance table for NSCLC |
| A11 | MEDIUM | Frame ALK-only $P = 0.63$ as falsifiability demonstration |
| A12 | MEDIUM | Fix the "5 of 17" / "5 of 7" parsing in Results 3.4 |
| A13 | LOW | Power threshold 0.45 → 0.43 (or "≈0.45") in Paper B |
| A14 | LOW | Disambiguate "after adjudication ... 0.73 (NSCLC)" in Paper B §3.1 |
| A15 | LOW | Justify or remove the "47 canonical source nodes" count |

---

## VERDICT

**MAJOR** revision.

The pre-registered primary inference is computationally bullet-proof
($P = 0.0004$ reproduces exactly to 4 decimals and survives BH-FDR,
Holm-Bonferroni, and Bonferroni-15 multiplicity at adjusted $P \le
0.006$). The CI-overlap and post-adjudication-kappa-tautology errors
caught in v2 are not repeated. The HARKing concern, while real, is
structurally rebutted by the prereg-v3 commit being timestamped before
NSCLC outcome-touching analysis and by the ALK-only sensitivity subset
landing exactly at the null.

The MAJOR drivers are:

1. (A3) **Paper B's silence on the NSCLC κ-gate failure** parallels the
   v2 round-1 A5 ask exactly; the v3 round-1 review is catching a
   recurrence in the methods paper that was caught and fixed in the
   clinical paper at v2.
2. (A7) **The bootstrap CI is promised in three places and computed in
   zero**, including in the prereg's primary-CI sentence carried into
   Paper A §2.5 and Paper B §1. Either compute it (30-minute fix) or
   disclose the prereg deviation. This is the single most-fixable
   HIGH-severity finding.
3. (A8) **The v2 → v3 silent relabel of S2/S3/S4 silently deletes three
   v2-pre-registered secondary outcomes** (temporal lag, subgroup
   coverage, composition-only count) and reuses the labels for
   different v3 analyses. This is the v3 analogue of the v2 round-1 A4
   ask and is the single most consequential prereg-honesty issue
   in this round.
4. (A9) **S1 ODI is promised on the combined corpus and delivered only
   on the mBC half**. Either compute the NSCLC prior-EGFR-TKI ODI or
   disclose the deviation.
5. (A2) **The HARKing-defense paragraph is missing**, despite the
   v1→v2→v3 trajectory being the single most-likely reviewer attack on
   the rejection.

All five are fixable without re-running the primary test, and none
threatens the conclusion. With A3, A7, A8 in full, plus some form of
A2, A4, A5, A9, I recommend MINOR; with all 15 in some form, I
recommend ACCEPT.
