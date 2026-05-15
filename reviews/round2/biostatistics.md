# Round 2 Review — Biostatistics

**Reviewer role:** Biostatistics
**Manuscript:** A Computable Map of Treatment-Sequencing Evidence in HR+/HER2- mBC
**Files reviewed:**
- `manuscript/main.tex`, `manuscript/discussion.tex`, `manuscript/supplement.tex`
- `analysis/05_compute_efdpr.py`, `analysis/06_compute_odi.py`
- `data/results/efdpr.json`, `data/results/odi.json`
- `docs/prereg.md`

---

## Round 1 carry-over: what is now resolved

| R1 ask | Status |
|---|---|
| Pre-registered exact-binomial test missing | **Resolved.** Test now reported; strict P=0.3698, ESCAT P=0.3698, liberal P=0.5950. Numbers re-verified by reviewer (scipy beta-ppf and direct binomial tail). |
| Bootstrap CI alongside Clopper-Pearson | **Resolved.** Both reported in Table 2 and Results 3.2. |
| Asymmetric percentile indexing | **Resolved.** Symmetric indexing in `bootstrap_efdpr` (line 175) with comment. |
| Multiple-testing across S1/S2/S3 | **Partial.** Deviation disclosed in Supplementary Text 1, but the framing in main text (Methods 2.7) is incomplete — see Ask 5. |

---

## Spot-check: Clopper-Pearson and exact-binomial recomputation

Reproduced independently with `scipy.stats.beta.ppf` and `math.comb`:

| Tolerance | k/n | EFDPR | CP CI (reviewer) | CP CI (paper) | Exact P (reviewer) | Exact P (paper) |
|---|---|---|---|---|---|---|
| strict | 5/16 | 0.3125 | [0.1102, 0.5866] | [0.1102, 0.5866] | 0.3698 | 0.37 |
| ESCAT | 5/16 | 0.3125 | [0.1102, 0.5866] | [0.1102, 0.5866] | 0.3698 | 0.37 |
| liberal | 4/16 | 0.2500 | [0.0727, 0.5238] | [0.0727, 0.5238] | 0.5950 | 0.60 |

**Verdict on numerical correctness:** Clopper-Pearson and exact binomial P-values are correct. The implementation in `clopper_pearson_ci` (lines 193–198) uses the textbook beta formulation correctly, with appropriate edge-case handling for k=0 and k=n.

The abstract reports the strict CP CI as **0.11–0.59** but reports the CP CI for *liberal* as the bootstrap-only **0.07–0.52** with the words "CI 0.07--0.52" — this is the CP CI, but readers cannot tell which CI is being shown for which tolerance without consulting Table 2. **Ask 1a** below.

---

## Concrete asks

### Ask 1. The "honesty about non-rejection" check — sentence-level audit

I checked each location for whether the failure to reject is stated unambiguously.

(a) **Abstract — PASS with one nit.** The abstract says, verbatim:
> "the pre-registered one-sided exact binomial test of $H_0: \mathrm{EFDPR} \le 0.25$ failed to reject under all three tolerance levels (strict $P=0.37$; ESCAT $P=0.37$; liberal $P=0.60$)."
> "the result is therefore best interpreted as descriptive evidence of substantial composition-across-non-overlapping-trials..."

This is honest. **Nit (1a):** In the Results sentence of the abstract, the abstract lists "Clopper-Pearson 0.11--0.59" for strict but "CI 0.07--0.52" for liberal without naming the CI type. Make this consistent: say "Clopper-Pearson 0.07--0.52" for liberal too (lines 56 of main.tex).

(b) **Key Objective box — PASS.** Reads:
> "the pre-registered one-sided exact-binomial test of $H_0: \mathrm{EFDPR} \le 0.25$ did not reject ($P=0.37$)."

Strong and unambiguous. No revision needed.

(c) **Results 3.2 — PASS.** Reads:
> "the pre-registered one-sided exact-binomial test of $H_0: \mathrm{EFDPR} \le 0.25$ did not reject under any tolerance level (strict $P = 0.37$; ESCAT $P = 0.37$; liberal $P = 0.60$ ...). The headline finding from this pilot is therefore a quantitative description of evidence sparsity at five clinically consequential decision points rather than a confirmatory rejection of the null."

Unambiguous. No revision needed.

(d) **Discussion — PASS.** discussion.tex line 5 reads:
> "the pre-registered one-sided exact-binomial test did not reject the null at $\alpha = 0.05$ ($P = 0.37$)"

and the "Pilot scale and the gap between estimate and inference" paragraph quantifies that k≥8 would be needed. Good.

**Ask 1, summary:** four out of four locations are honest about non-rejection; only the abstract-results sentence needs the CI-type fix in 1a.

### Ask 2. Clopper-Pearson verification

Spot-checked above. **No revision required.**

### Ask 3. The `metastatic` line-agnostic state token — undisclosed post-hoc deviation

`analysis/05_compute_efdpr.py:_state_match` (lines 51–59) contains a special-case escape hatch:

```python
if "metastatic" in gl_tokens:
    gl_tokens = gl_tokens - {"metastatic"}
return gl_tokens.issubset(_state_tokens(edge_state))
```

This token is used for the gBRCAm node (G16, supported by OlympiAD/NCT02000622). The behaviour materially affects the EFDPR numerator: without it, G16 would be evidence-free under strict tolerance because OlympiAD's source state does not match "metastatic" by superset.

**The prereg (`docs/prereg.md`) does not mention `metastatic` as a special state-match token.** Methods 2.5 in `main.tex` line 100 *does* mention it in passing:

> "(a) state superset --- every guideline-required prior-treatment token of $g$ is a member of the trial's source-state token set, with the special line-agnostic token `metastatic` (used for gBRCAm) satisfied by any state"

So it is **disclosed in Methods** but **not flagged as a post-hoc deviation in Supplementary Text 1.** This is a borderline case: the gBRCAm guideline recommendation is genuinely line-agnostic in ESMO 2024, and OlympiAD was always going to be the supporting trial for that node. But the prereg did not anticipate a "satisfied by any state" exception, and the rule changes the numerator of the primary outcome.

**Ask 3:** Add a bullet to Supplementary Text 1 explicitly disclosing the `metastatic` token as a post-hoc clarification to the state-superset rule, and run a sensitivity analysis reporting EFDPR with this exception removed (i.e., G16 treated by exact state superset against OlympiAD's source state). I expect EFDPR to rise from 0.3125 to 0.3750 under strict and from 0.25 to 0.3125 under liberal — neither shifts the inferential conclusion, but transparency about this is required.

### Ask 4. ODI confidence intervals are still missing

`data/results/odi.json` reports point ODI values (HER2-low 0.20, ESR1mut 0.33, PIK3CAmut 0.33, AKTpath 0.67, prior_CDK4_6i 0.90) with no uncertainty quantification. ODI is the secondary outcome S1, and the manuscript flags it as the most clinically important secondary signal ("prior-CDK4/6i inclusion variable was the most discordant (ODI 0.905 across 7 trials)").

For pairs-based metrics with small trial counts (n=2 for HER2-low, ESR1mut, AKTpath; n=3 for PIK3CAmut; n=7 for prior_CDK4_6i), point estimates without intervals are not informative. With n=2 trials there is exactly one pair and the ODI equals the single Jaccard distance — the "estimate" is essentially the observation itself.

**Ask 4:** Add a **bootstrap-by-trial CI for ODI per biomarker variable.** Resample trials with replacement (`B=1000`, same seed `20260516`), recompute mean pairwise Jaccard distance per resample, report 2.5/97.5 percentile bounds. Note that the variables with n=2 trials will have degenerate CIs (point estimate or zero from a both-same resample); report them anyway with a note. Add a column to Table 4 (`tab_odi.tex`) and a note in Results 3.3.

### Ask 5. S2/S3 descriptive reporting — framing is acceptable but partly buried

The prereg commits (line 45) to "Benjamini-Hochberg q < 0.05 across three tests" for S1, S2, S3. The Round 2 main text Methods 2.7 says:

> "in the present pilot, S2 and S3 are reported descriptively because the small corpus precludes a meaningful Benjamini-Hochberg correction across three independent tests, a deviation that is disclosed here."

and Supplementary Text 1 says:

> "S2 (temporal lag) and S3 (subgroup coverage) are reported descriptively because the small corpus precludes a meaningful formal test."

Framing is **mostly honest**, but I want one tightening:

**Ask 5:** S1 itself is also reported descriptively (as a per-biomarker mean pairwise Jaccard distance) without a p-value, so the BH-correction was never applied to *any* of S1/S2/S3. Make this explicit in Methods 2.7 and Supplementary Text 1: not just "S2 and S3 descriptive" but **"the entire S1/S2/S3 family is reported descriptively; no BH correction was applied because no formal tests were run."** The current wording leaves the reader to infer that S1 has a test and S2/S3 don't.

### Ask 6. Bootstrap resampling unit — node clustering ignored

Round 1 flagged that resampling guideline nodes by simple random sampling assumes node independence, which is questionable because (i) several ESMO decision nodes share patient sub-states (G5/G6/G7 are all post-CDK4/6i biomarker-stratified branches and consequently share the prior-CDK4/6i-and-endo state), and (ii) evidence-free status at one node is mechanically correlated with evidence-free status at a sibling node (the same upstream trial vacuum).

The current paper has **not addressed this.** `bootstrap_efdpr` (line 165) still does `[rng.choice(gls) for _ in range(len(gls))]` with no clustering or stratification. This is also why the bootstrap CI ([0.125, 0.5625]) is narrower than the Clopper-Pearson CI ([0.110, 0.587]) — the bootstrap underestimates variance under positive dependence.

**Ask 6:** Either (a) acknowledge in Methods 2.7 that the bootstrap assumes node-level independence and that the Clopper-Pearson CI (which is exchangeable-Bernoulli-based and not independence-requiring in the same way) is the recommended primary CI for inference (the supplement already calls CP the "recommended primary CI"); or (b) implement a cluster-bootstrap where the resampling unit is the upstream patient-state cluster (e.g., {G5, G6, G7} as one cluster, {G13, G14} as another). Option (a) is sufficient; option (b) is preferred for a methods-flavored paper. The current silence is not.

### Ask 7. Independence assumption for the exact-binomial test

The one-sided exact binomial test of H0: p ≤ 0.25 with k=5, n=16 assumes the 16 indicator variables (1 if node g is evidence-free, 0 otherwise) are iid Bernoulli(p). The same node-clustering objection in Ask 6 applies: nodes sharing patient sub-states have correlated evidence-free indicators because they share the upstream trial pool.

The manuscript does **not state this assumption** anywhere. Methods 2.7 says only "the one-sided exact binomial test of $H_0: \mathrm{EFDPR} \le 0.25$ given $k$ evidence-free nodes out of $n = |\mathcal{G}|$ guideline nodes" with no reference to independence.

**Ask 7:** Add one sentence to Methods 2.7 stating the iid-Bernoulli assumption and acknowledging that ESMO decision nodes are not fully independent (sibling nodes share upstream trial pools, so positive dependence is expected). The practical consequence: the nominal Type I error under positive dependence is approximately preserved or conservative for the one-sided test (because positive dependence reduces effective sample size, widening the true null distribution), so the failure to reject is robust to this assumption. Make this argument explicitly — do not leave the reader to construct it.

### Ask 8. Seed and reproducibility statement — present and correct

Methods 2.7 line 110 mentions "A bootstrap random seed (`20260516`) ensures reproducibility." Code uses the same seed in `bootstrap_efdpr` (line 165). Supplementary Table S1 row G6 records "Seed 20260516; v1.0.0 commit." **No revision required.**

### Ask 9. Bootstrap CI vs Clopper-Pearson divergence — explain it

The bootstrap CI for strict is [0.125, 0.5625] (width 0.4375) while the Clopper-Pearson CI is [0.1102, 0.5866] (width 0.4764). The CP interval is wider, which is the expected ordering for finite-sample percentile bootstrap of a binomial proportion. **Ask 9:** One line in Results 3.2 explaining that CP is wider as expected for small-n (because the bootstrap is biased toward the empirical proportion and undercovers in the tails) would close the loop with statistically-literate readers.

### Ask 10. Liberal-tolerance result lands exactly at the pre-registered threshold

Under liberal tolerance EFDPR = 4/16 = 0.25, **exactly** at the pre-registered rejection threshold. With one-sided H0: p ≤ 0.25, the exact-binomial P-value is 0.595, which is the probability of observing k ≥ 4 successes under p=0.25. This is correct (a point estimate equal to the null mean cannot reject), but the manuscript says (Sensitivity Analyses, line 172):

> "Liberal tolerance rescued EMERALD's support of the post-CDK4/6i ESR1mut node (G5), reducing EFDPR to 0.25, exactly at the pre-registered threshold."

without flagging that this means the liberal-tolerance result is the *least informative* of the three for inference about H0. **Ask 10:** Add a one-sentence note that liberal-tolerance EFDPR sitting exactly at the null mean is the worst case for power; reframe the strict result (which is the pre-registered primary, anyway) as the headline.

### Ask 11. Stop rule and prereg consistency

The prereg defines two stop rules (line 41): "Primary hypothesis refuted if 95% CI upper bound of EFDPR < 0.25" and "Clean null: EFDPR point estimate < 0.10 with CI upper bound < 0.15." Neither stop rule is triggered (CP upper bound 0.5866 ≥ 0.25, point estimate 0.3125 ≥ 0.10). **Ask 11:** Add one sentence to Methods 2.7 or Results 3.2 saying that the two pre-registered stop rules were also not triggered, so the conclusion is "neither rejected nor refuted; inconclusive at pilot scale." This closes the prereg loop fully.

### Ask 12. Pre-registration commit hash

Methods 2.7 says the prereg was committed before any outcome-touching analysis but does not give the commit hash inline. Supplementary Table S1 row 26 points to `docs/prereg.md`. **Ask 12:** Quote the actual prereg commit short-hash in the Preregistration statement (currently line 187 says "The pre-registration commit hash is recorded in the repository's first commit" — give the hash, not a pointer).

### Ask 13. Effect size and post-hoc power

Methods 2.5/2.7 do not report a power analysis. The prereg (line 18) expected EFDPR in [0.30, 0.55]. Under p=0.40 (midpoint), the exact-binomial power for n=16 against H0: p≤0.25 is about 0.34 (computable). **Ask 13:** Add a one-sentence post-hoc statement: under the prereg-expected alternative p=0.40, the n=16 pilot has ~34% power at α=0.05 one-sided — this is the quantitative basis for the "underpowered pilot" framing in the Discussion. Without this number, "small sample" is hand-waving.

---

## Verdict

**MINOR REVISION.**

Round 2 has substantively addressed the largest Round 1 biostatistics asks: the pre-registered exact-binomial test is now reported (and the manuscript is honest about non-rejection in all four required locations); Clopper-Pearson CIs are reported and verify numerically; asymmetric percentile indexing was fixed; the multiple-testing deviation is disclosed. The remaining items (Asks 3, 4, 6, 7, 11) are real but address-able with text edits and a small additional ODI bootstrap. None of them threaten the paper's conclusions — they tighten the rigor of how those conclusions are framed.

The single most important outstanding item is **Ask 4 (ODI CIs)**: point estimates of ODI without uncertainty are not defensible for a biostatistics audience and the bootstrap is a 20-line change to `06_compute_odi.py`.
