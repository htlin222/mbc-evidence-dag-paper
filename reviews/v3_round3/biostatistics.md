# Biostatistics Review — paper_A_clinical_v3.tex + paper_B_methods_v3.tex (v3, Round 3)

**Reviewer role.** Adversarial biostatistics referee, v3 round 3. Scope: verify that the R1 biostats MAJOR findings (bootstrap CI not computed; S2/S3/S4 silent relabel; NSCLC adjudication deferred; HARKing defense missing; multiplicity across the 3 × 5 tolerance-by-subset grid) and the R2 bulk stale-number sweep landed cleanly in the post-`dadf797` manuscripts and data artifacts. Spot-checks recomputed from scratch against the post-R2 `v3_pooled_efdpr.json`, `v3_nsclc_kappa.json`, `analysis/v3_08_compute_pooled_efdpr.py`, and the two `.tex` files. No R2 biostats record exists (crash mid-review), so this round re-runs the R1 grid against the corrected numbers.

---

## Spot-check reproduction (all 4-decimal verifications)

All eight requested cells reproduce **exactly** against the manuscript / JSON. Re-computed from scratch (scipy `binom`, `beta`):

| Quantity | Reviewer-computed | JSON / paper | Match |
|---|---|---|---|
| Primary $P(X\ge 19 \mid n{=}49, p{=}0.25)$ | **0.0231** | JSON 0.0231; Paper A abstract & §3.1 & box & Fig 1 caption & Discussion headline all $P = 0.023$; Paper B abstract & §5.2 & trajectory all $P = 0.023$. | OK |
| Clopper-Pearson 95% CI for 19/49 | **[0.2520, 0.5376]** | JSON `[0.252, 0.5376]`; both papers report "0.25--0.54". | OK (user's expected [0.2525, 0.5377] is off by one in the 4th decimal — the correct CP CI is [0.2520, 0.5376]; the JSON value is right.) |
| Bootstrap CI for primary strict (seed 20260516, 1000 iters) | **[0.2449, 0.5306]** | JSON `bootstrap_ci95: [0.2449, 0.5306]`. Papers A abstract / KO box and Paper B §5.2 round to "0.25--0.53". | OK numerically; **rounding issue: 0.2449 rounds to 0.24, not 0.25**. See ask A1. |
| ESCAT/liberal $P(X\ge 17 \mid n{=}49, p{=}0.25)$ | **0.0836** | JSON 0.0836; both papers report $P = 0.084$ in abstract; Paper A Discussion "Three caveats" still says $P = 0.10$; Paper B §5.3 still says $P = 0.10$ (with the stale "24/50 → 17/50" arithmetic). | Number OK; **disclosure stale in 2 prose locations** (asks A2, A3). |
| mBC-only 10/25 strict $P$ | **0.0713** | JSON 0.0713; Paper A reports $P = 0.07$. | OK |
| NSCLC-only 9/24 strict $P$ | **0.1213** | JSON 0.1213; Paper A reports $P = 0.12$. | OK |
| NSCLC EGFR-only 7/17 strict $P$ | **0.1071** | JSON 0.1071; Paper A reports $P = 0.11$. | OK |
| NSCLC ALK-only 2/7 strict $P$ | **0.5551** | JSON 0.5551; Paper A reports $P = 0.56$. | OK (note: this is the de-inflated `n=7` denominator post N13/N14 merge — the R1 number `P = 0.63` at `n=8` is no longer relevant). |

The pre-registered primary test is computationally bullet-proof at $P = 0.023$ on the 19/49 strict pooled denominator. Code (`analysis/v3_08_compute_pooled_efdpr.py:bootstrap_ci_efdpr`, lines 177–189) implements the percentile bootstrap with `seed=20260516`, `n_iter=1000`, by guideline-node resampling; the JSON has `bootstrap_ci95` populated for all **15** cells (3 tolerances × 5 subsets). The R1 CRITICAL ask A7 (bootstrap CI promised but not computed) is **fully closed**.

---

## R1 carry-over audit — what landed, what didn't

| R1 ask | Severity | Post-R2 status |
|---|---|---|
| **A1** Add BH/Bonferroni robustness statement | MEDIUM | **NOT ADDRESSED.** Neither paper mentions multiplicity correction across the tolerance-by-subset grid. With the post-R1 corrected numbers this is now substantively load-bearing (see Q1 below). |
| **A2** Make HARKing-defense explicit | HIGH | **PARTIAL.** Paper B §5.4 has one sentence ("commit `4b5bf1a`, before any NSCLC outcome data \ldots structural defence against the HARKing-equivalent concern"). Paper A still has zero HARKing paragraph. Paper A is the clinical paper and the more-read of the two; this is where the defense matters most. |
| **A3** Paper B disclose NSCLC κ-gate failure on `post_alk_tki`, `egfr_t790m`, `drug_class` PABAK | CRITICAL | **CLOSED.** Paper B §5.2 line 127 now names all three failing fields with values and explicitly says "A formal NSCLC adjudication pass is deferred to v3.0.1." Clean fix. |
| **A4** Disclose realised $n=13$ vs prereg $n=15$ validation subset | HIGH | **NOT ADDRESSED.** Neither paper mentions the 13-vs-15 gap. `v3_nsclc_kappa.json:n_validation = 13`, prereg-v3 step 5 says 15. |
| **A5** Disclose no NSCLC adjudication pass run | HIGH | **CLOSED.** Paper B §5.2 line 127 says explicitly: "the v3 NSCLC arm did not undergo a formal adjudication-rule pass analogous to v2 mBC (which had 17 adjudication rules) \ldots A formal NSCLC adjudication pass is deferred to v3.0.1." |
| **A6** Reconcile "all adjudication rules released" with NSCLC having zero | MEDIUM | **NOT ADDRESSED.** Paper B Data Availability still says "all adjudication rules with rationale are released". The §5.2 disclosure of the deferred NSCLC adjudication is honest but the DAS framing is unchanged. |
| **A7** Add the promised bootstrap CI | CRITICAL | **CLOSED.** Function added at `v3_08_compute_pooled_efdpr.py:177–189`; all 15 cells have `bootstrap_ci95` populated; both papers report bootstrap CI alongside CP CI in abstract and box. |
| **A8** Disclose v2 → v3 silent relabel of S2/S3/S4 secondaries | CRITICAL | **NOT ADDRESSED.** No "Pre-registration deviations from v2" subsection in either paper. v2 S2 (temporal lag), v2 S3 (subgroup coverage), v2 S4 (composition-only count) are still silently dropped from v3. |
| **A9** Compute NSCLC ODI per S1 commitment, OR disclose deviation | HIGH | **NOT ADDRESSED.** Paper A §3.5 still narratively describes "analogous heterogeneity" for NSCLC prior-EGFR-TKI inclusion without any computed ODI. No deviation disclosure. |
| A10 Per-node year-of-introduction provenance for NSCLC | MEDIUM | Not verified this round (out of scope per user's task brief). |
| A11 Frame ALK $P=0.56$ as falsifiability demonstration | MEDIUM | **CLOSED.** Paper A §3.3 final sentence now says "The ALK-rearranged subset's lower EFDPR (0.29) and high P (0.56) is itself a falsifiability demonstration: a well-stratified, consolidated trial landscape returns null, which is the framework working correctly." |
| A12 Fix "5 of 17" / "5 of 7" parsing in Results 3.4 | MEDIUM | Not directly applicable — Results 3.4 was rewritten to a cluster list; the "5 of 17" phrasing no longer appears. |
| A13 Power threshold 0.45 → 0.43 (or "≈0.45") | LOW | **NOT ADDRESSED.** Paper B §5 limitations still says "$\ge 80\%$ only for $p_1 \ge 0.45$". |
| A14 Disambiguate "after adjudication \ldots 0.73 (NSCLC)" | LOW | **CLOSED.** Paper B §5.1 wording is now "After adjudication, mean PABAK was 0.99 (mBC) and 0.73 (NSCLC)" but §5.2 explicitly says NSCLC was not adjudicated. The §5.1 phrasing is still mildly misleading in isolation but the §5.2 disclosure resolves the ambiguity. |
| A15 "47 canonical source nodes" justification | LOW | Paper A §2.5 now says "48 canonical source nodes" — number changed during R2 sweep but still unjustified. |

**Net R1 carry-over.** 4 of 5 CRITICAL/HIGH biostats asks delivered (A3, A5, A7, A11). **3 CRITICAL/HIGH not addressed** (A2 Paper A side; A4 validation $n$; A8 S2/S3/S4 silent relabel). **A1 (BH/Bonferroni) was MEDIUM at R1; with the corrected post-R1 P-values it is now CRITICAL** because the primary no longer survives BH across the 15-cell grid (see Q1 below).

---

## R2 bulk-sweep verification — leftover stale numbers in biostats prose

The R2 integration `dadf797` was a "sweep 14 stale numbers + regen figures" commit. Verify each biostats-relevant prose location against `v3_pooled_efdpr.json`:

| Location | Says | Correct | Status |
|---|---|---|---|
| Paper A abstract L50 | "0.39 (19/49); CP 0.25--0.54; bootstrap 0.25--0.53; $P = 0.023$"; "ESCAT-aligned and liberal tolerance gave 0.35 ($P = 0.084$)"; subsets 0.40/$P{=}0.07$, 0.38/$P{=}0.12$, 0.41/$P{=}0.11$, 0.29/$P{=}0.56$ | All correct against JSON | OK |
| Paper A boxed summary L61 | "0.39; CP 0.25--0.54; bootstrap 0.25--0.53; $P = 0.023$; ESCAT/liberal 0.35 ($P = 0.084$)" | OK | OK |
| Paper A §3.1 L95 | "0.39 (19/49 \ldots CP 0.25--0.54; bootstrap 0.25--0.53); \ldots $P = 0.023$"; "ESCAT \ldots gave 0.35 ($P = 0.084$, marginal non-rejection)" | OK | OK |
| **Paper A Discussion "Three caveats" L145** | "ESCAT-aligned and liberal tolerance gave **$P = 0.10$** on the pooled denominator" | Should be $P = 0.084$ | **STALE** (R2 missed this; R1 reviewer Q1 / R2 clinical C3 both flagged it). |
| **Paper A Discussion headline L133** | "At adequately-powered multi-tumor scale (**50 pooled guideline nodes**)" | Should be **49** | **STALE** (R2 missed; n=49 throughout the rest of the paper). |
| **Paper B §5.3 Tolerance-sensitivity grid L130** | "ESCAT-aligned and liberal tolerance gave **0.34 (24/50 → 17/50; $P = 0.10$)**, failing to reject" | Should be **0.35 (19/49 → 17/49; $P = 0.084$)** | **STALE** (R2 clinical C4 flagged; R2 integration apparently did not patch this paragraph; the abstract L48 and §5.2 L127 have the correct numbers, so the paper is internally inconsistent). |
| Paper B abstract L48 | "0.39; CP 0.25--0.54; bootstrap 0.25--0.53; $P = 0.023$; ESCAT and liberal 0.35 ($P = 0.084$)" | OK | OK |
| Paper B §5.2 L127 | "0.39 \ldots CP 0.25--0.54; bootstrap 0.25--0.53 \ldots $P = 0.023$"; "0.35 ($P = 0.084$)"; NSCLC κ disclosure | OK | OK |
| Paper B §5.4 trajectory L133 | v1 $P=0.37$ / v2 $P=0.07$ / v3 strict $P=0.023$, ESCAT/liberal $P=0.084$; HARKing-defense sentence | OK | OK |

Three R2 stale-number escapes (Paper A L133, L145; Paper B L130) are directly biostats-prose. None changes the inference, but Paper B's "0.34 (24/50 → 17/50; $P = 0.10$)" sentence has **two wrong cell counts plus the wrong denominator plus the wrong $P$** in a single sentence that sits inside a heading literally titled "Tolerance-sensitivity grid" — a copy-editor will flag it immediately.

---

## User's verification checklist — direct answers

### 1. Are all bootstrap CIs reported in both papers, not just CP?

**JSON: yes, every one of the 15 (3 tolerance × 5 subset) cells has a `bootstrap_ci95` field.** Papers: bootstrap CI is reported **only for the primary cell** in both papers' abstract / KO box / §3.1 (Paper A) / §5.2 (Paper B). The four sensitivity subsets and the two non-strict primary tolerances do **not** have bootstrap CI quoted in either paper; only CP CI appears for those. This is defensible (the primary is what was pre-registered to get a bootstrap CI), but the R1 ask A7 framed it as "alongside CP \ldots as a sensitivity comparison" — strictly, the sensitivity comparison should be available wherever CP CI is reported. Minor inconsistency; not blocking.

### 2. ESCAT/liberal $P = 0.084$ explicitly disclosed (not buried)?

**Mixed.** Abstract (both papers) and Paper A §3.1 / Paper B §5.2 (primary results paragraph) explicitly disclose $P = 0.084$ in the rejection sentence itself. **Paper A Discussion "Three caveats" L145 still says $P = 0.10$**; Paper B §5.3 "Tolerance-sensitivity grid" L130 still says $P = 0.10$ with the stale "24/50 → 17/50" arithmetic. The disclosure is honest in the high-visibility abstract / first-results paragraph, but the prose in the dedicated tolerance / caveat paragraphs is internally inconsistent with the abstract. **Critical inconsistency**: Paper B has a paragraph titled "Tolerance-sensitivity grid" that gives the wrong $P$, wrong denominator, and wrong cell counts for the tolerance-sensitivity grid.

### 3. Tolerance grid framed as sensitivity not 3 tests in BOTH papers?

**Yes, in both.** Paper A §3.1 line 95: "the tolerance grid is reported as pre-registered sensitivity, not three independent confirmatory tests." Paper B §2.3 line 93: "The three tolerance levels are reported as a pre-registered sensitivity grid, not as three independent confirmatory tests." Both papers carry the framing **once** in Methods/Results; neither repeats it in Discussion. Sufficient. The prereg backs both papers: prereg-v3 line 33 says "the test is the **single primary inferential commitment** of v3".

### 4. Multiplicity across 15 P-values — is BH/Bonferroni discussed in either paper?

**No, in neither paper.** This was R1 ask A1 (MEDIUM, "pre-empt the question rather than waiting for it"). With the corrected post-R1 numbers, **the silence is now substantively load-bearing**, not just rhetorical:

Re-computing BH-FDR, Holm, and Bonferroni across the 15 cells:

| Rank | Subset / Tol | Raw P | BH-q | Holm-adj | Bonferroni-15 |
|---:|---|---:|---:|---:|---:|
| 1 | **primary / strict** | **0.0231** | **0.3465** | **0.3465** | **0.3465** |
| 2 | mbc_only / strict | 0.0713 | 0.5348 | 0.9982 | 1.0000 |
| 3 | primary / escat | 0.0836 | 0.4180 | 1.0000 | 1.0000 |
| 4 | primary / liberal | 0.0836 | 0.3135 | 1.0000 | 1.0000 |
| 5 | nsclc_egfr_only / strict | 0.1071 | 0.3213 | 1.0000 | 1.0000 |
| 6–15 | (all fail to reject either way) | | | | |

**The pre-registered primary survives the prereg's "single test" framing (raw $P = 0.023$) but does NOT survive any standard multiplicity correction across the full 3 × 5 tolerance-by-subset grid.** At BH-q = 0.35 and Bonferroni-15 = 0.35, the primary is **far above** $\alpha = 0.05$ if a strict reviewer demands grid-wide multiplicity. Even on the more lenient partitions:

- **m=5 (strict across 5 subsets only):** primary BH-q = 0.12, Bonferroni-5 = 0.12 — still fails $\alpha = 0.05$.
- **m=3 (3 tolerances on primary only):** primary BH-q = 0.069, Bonferroni-3 = 0.069 — still fails $\alpha = 0.05$.
- **m=1 (prereg-honored single test):** $P = 0.023$ — passes.

**The R1-era statement "primary survives BH at adjusted $P \le 0.006$" is now obsolete** (the R1 number was based on the pre-R1 $P = 0.0004$). Under the corrected numbers, the rejection depends critically on the prereg's "single primary inferential commitment" framing being honored. This **strengthens** the prereg-discipline argument but also **strengthens** the need for the paper to explicitly defend that framing in the manuscript itself, not just by reference to the prereg.

### 5. HARKing defense paragraph present and adequate?

**Paper B: present but minimal (one sentence at §5.4 L133).** Paper A: **absent**. The R1 ask A2 specifically requested a paragraph for Paper A §2.1 or Discussion. Paper A is the clinical, higher-readership paper and is where reviewers will look for the trajectory-defense argument. With the corrected $P = 0.023$ (no longer $P = 0.0004$), the "v1 → v2 → v3 P-value trajectory looks like power-chasing" attack is now even more accessible to a hostile reviewer because the rejection is marginal — a reviewer can plausibly argue that the v3 rejection sits exactly at the boundary where any post-hoc data choice could flip it. The HARKing-defense paragraph is now **more important**, not less.

### 6. NSCLC adjudication: papers acknowledge it's deferred to v3.0.1?

**Paper B yes (§5.2 L127, explicit "A formal NSCLC adjudication pass is deferred to v3.0.1.").** **Paper A no** — §2.3 still reports pre-adjudication κ values without saying anything about a deferred adjudication pass. The R1 ask A5 was for both papers; only Paper B closed it. Paper A still leaves a careful reader to infer that NSCLC was adjudicated like mBC was; the parallel "documented adjudication trail" phrase in Paper A "Three caveats" L145 ("with documented adjudication trail" — applied jointly to NSCLC 0.78 and mBC 0.67) is the v2-A5-analogue misleading framing that R1 caught for Paper B and is now reproduced in Paper A.

### 7. mBC 17 adjudication rules vs NSCLC 0 — disclosed?

**Paper B yes (§5.2 L127 explicitly says "v2 mBC (which had 17 adjudication rules)" and contrasts NSCLC's lack of adjudication pass).** **Paper A no** — §2.3 L84 mentions only the NSCLC pre-adjudication κ, with no mention of v2's 17 rules or the v3 0-rules contrast. Same asymmetry as #6.

---

## R2-era new biostats issue surfaced this round

### Q1-new. The primary no longer survives BH if the 15-cell grid is taken as the relevant family.

This is the **single most consequential biostats finding of this round.** R1 wrote (Q2) that the primary survives BH at adjusted $P \le 0.006$ — true at the pre-R1 P = 0.0004 but **false at the post-R1 P = 0.023**. With the corrected numbers:

- **Prereg-protected single-test framing**: P = 0.023, rejects.
- **Any multiplicity correction across ≥ 3 cells**: fails.

The prereg-v3 line 33 explicitly says "single primary inferential commitment", and prereg-v3 line 99 says "the pooled primary test is run **once**. Tumor-stratified estimates are sensitivity". The prereg discipline holds the line — but only if the manuscripts make that framing **load-bearing-and-defensible** rather than buried in a single Results sentence. Without an explicit Methods-level argument that the 15-cell grid is sensitivity (not 15 independent tests), a strict reviewer can mechanically apply Bonferroni-15 and reject the rejection.

This is the R1 A1 ask, escalated from MEDIUM to CRITICAL by the post-R1 number correction.

### Q2-new. Bootstrap CI lower-bound rounding in primary.

JSON: `bootstrap_ci95: [0.2449, 0.5306]`. Papers (both) report "bootstrap 0.25--0.53" in abstract/box. 0.2449 rounds to 0.24, not 0.25 — the lower bound is off by one in the second decimal. CP CI in the same sentence is 0.25--0.54 (correctly rounded from [0.2520, 0.5376]); juxtaposing "CP 0.25--0.54" with "bootstrap 0.25--0.53" makes the bootstrap lower bound numerically identical to CP, which is what the paper wants to claim but isn't quite what the bootstrap actually returned. Either round honestly (bootstrap 0.24--0.53) or quote to 3 decimals (bootstrap 0.245--0.531).

### Q3-new. The 19 strict evidence-free nodes are not robust to a 1-node perturbation at the primary cell.

For a one-sided exact binomial of $H_0: p \le 0.25$ at $n = 49$, the critical value $k_{\text{crit}}$ is **18** ($P(X \ge 18 \mid 49, 0.25) = 0.0488$, rejects at 0.05; $P(X \ge 17 \mid 49, 0.25) = 0.0836$, fails). The realised $k = 19$ ($P = 0.0231$) is **one node above the critical value**. If a future reviewer adjudication moves any **one** of the 19 evidence-free nodes into supported, the test moves to $P = 0.0488$ — still rejects but margin shrinks to a hairline. If **two** nodes flip to supported (17/49), the test fails ($P = 0.0836$). **The rejection is one node deep**.

This is not a defect — the rejection is real at the realised data. But it makes the per-node adjudication audit much more important than at v2's $P = 0.07$ marginal-non-rejection where a single node didn't matter. A sensitivity row showing "if 1 of 19 evidence-free nodes flips: $P = 0.05$; if 2 flip: $P = 0.08$" would be honest and pre-empts the worry that a single TROPION-Lung01 re-adjudication or a single N20 brain-mets re-encoding could overturn the headline.

---

## Concrete asks (8)

### A1 (CRITICAL — escalates R1 A1). Add an explicit multiplicity-correction discussion in BOTH papers.

The R1-era "primary survives BH at $P \le 0.006$" claim is **no longer true** at the post-R1 $P = 0.023$. Under the corrected numbers, the primary survives only the prereg's "single primary inferential commitment" framing; BH-q across the 15-cell grid is 0.35, Bonferroni-15 = 0.35, Bonferroni-3 (across tolerances on primary) = 0.07. Add to **Paper A Methods §2.5 (or end of §3.1)** and **Paper B §3.3 (Tolerance-sensitivity grid)**:

> "Because prereg-v3 (commit \texttt{4b5bf1a}, line 33) commits the pooled-strict-tolerance test as the single primary inferential commitment, multiplicity correction across the tolerance-grid (sensitivity) cells is not applied. If a reviewer prefers a family-wise framing across all 15 (3 tolerance × 5 subset) cells reported in `v3_pooled_efdpr.json`, the pre-registered primary's raw $P = 0.023$ rises to BH-q $= 0.35$ and Bonferroni-15 $= 0.35$ — i.e., the rejection depends on the prereg's single-test framing. We hold the prereg framing on the grounds that (i) the tolerance grid is one outcome under three operationalizations, not three outcomes; (ii) the tumor-stratified subsets are sensitivity, not pre-specified independent tests; (iii) the prereg was committed before any NSCLC outcome-touching analysis."

Without this paragraph, a strict reviewer will mechanically apply Bonferroni-15 and unrebutted reject the rejection.

### A2 (CRITICAL — closes R1 A8). Disclose the v2 → v3 silent S2/S3/S4 relabel and the v2 secondary-outcome drop.

R1 ask A8 has not been actioned in either paper. Add to **Paper A Methods §2.1 (Data sources and pre-registration)** or to a new **"Pre-registration deviations from v2"** subsection:

> "The v3 prereg (\texttt{docs/prereg-v3.md}, commit \texttt{4b5bf1a}, lines 64--67) re-uses the labels S1--S4 with v3-specific definitions (S1 ODI on combined corpus; S2 tumor-stratified EFDPR; S3 cross-tumor consistency; S4 LLM-extraction inter-rater agreement at production scale). This is a relabel, not a continuation of v2's S1--S4. The v2 secondary outcomes — v2 S2 (temporal evidence lag from guideline-node introduction to earliest supporting trial PC), v2 S3 (Asian / age $\ge 70$ / Black ancestry subgroup coverage), v2 S4 (composition-only citation count) — are not recomputed in v3; v2's S2/S3/S4 results remain on record at the v2.0.0 tag and are not modified by v3. This is a disclosed v3 deviation."

The R1 reviewer flagged this as "the most consequential prereg-honesty issue in this round". It remains so post-R2.

### A3 (CRITICAL — fix Paper B §5.3 stale paragraph). Patch the "Tolerance-sensitivity grid" paragraph that the R2 sweep missed.

Paper B §5.3 line 130 currently says:

> "ESCAT-aligned and liberal tolerance gave 0.34 (24/50 → 17/50; $P = 0.10$), failing to reject."

Every number in that sentence is stale. Replace with:

> "ESCAT-aligned and liberal tolerance gave 0.35 (17/49; $P = 0.084$), failing to reject."

This paragraph sits inside a subsection literally titled "Tolerance-sensitivity grid" and is the only place in Paper B where the tolerance arithmetic is laid out. A copy-editor will flag immediately.

### A4 (HIGH — closes R1 A2 Paper A side). Add HARKing-defense paragraph to Paper A.

Paper B has a single-sentence defense at §5.4 L133. Paper A — the clinical, higher-readership paper — has zero defense. With the corrected $P = 0.023$ sitting one node above critical (Q3-new above), the v1 ($P{=}0.37$) → v2 ($P{=}0.07$) → v3 ($P{=}0.023$) trajectory is more accessible to a hostile reviewer, not less. Add a paragraph to **Paper A Discussion "Three positives"** or as a new "Why this isn't HARKing" paragraph:

> "A reviewer might ask whether the v1 ($P = 0.37$) $\to$ v2 ($P = 0.07$) $\to$ v3 ($P = 0.023$) trajectory reflects power-driven node addition until rejection. It does not, for three structural reasons. First, the v3 pre-registration (\texttt{docs/prereg-v3.md}, commit \texttt{4b5bf1a}) was committed before any NSCLC outcome-touching analysis, and the primary inference is unchanged from v1/v2. Second, the denominator extension is by entire tumor type (NSCLC EGFR + ALK), not by selective node addition; the NSCLC target was pre-specified at 20--30 nodes with a $\ge 18$ gate. Third, the NSCLC ALK-only sensitivity subset returned EFDPR = 0.29 ($P = 0.56$), demonstrating that the framework permits non-rejection under genuine concordance even within the v3 corpus that delivered the pooled rejection."

### A5 (HIGH — closes R1 A4). Disclose realised validation subset $n = 13$ vs prereg $n = 15$.

Neither paper acknowledges that `v3_nsclc_kappa.json:n_validation = 13` while prereg-v3 step 5 specified a 15-trial NSCLC validation subset. Add one sentence to **Paper A §2.3** and **Paper B §3.2**:

> "The realised NSCLC validation subset was 13 trials of the pre-registered 15; two trials were dropped due to round-1 NCT corrections that removed wrong-NCT records before merging. The 13-vs-15 gap is a disclosed minor deviation."

Reviewers comparing prereg.md to the released JSON will notice immediately.

### A6 (HIGH — closes R1 A5/A6 Paper A side). Bring Paper A NSCLC adjudication disclosure into parity with Paper B.

Paper B §5.2 L127 explicitly says NSCLC was not adjudicated and defers a formal pass to v3.0.1. **Paper A §2.3 L84** reports NSCLC κ values without any such disclosure, and **Paper A "Three caveats" L145** says "with documented adjudication trail" jointly for NSCLC 0.78 and mBC 0.67 — which is true for mBC (v2's 17 rules) and **not true for NSCLC** (zero rules). Either rewrite the "Three caveats" sentence to split mBC and NSCLC, or add the v3.0.1-deferral sentence from Paper B §5.2 to Paper A §2.3. Also reconcile Paper B Data Availability Statement (which still says "all adjudication rules with rationale" are released) with NSCLC having zero rules — R1 A6 still pending.

### A7 (MEDIUM — closes R1 A9). Compute NSCLC ODI per prereg-v3 S1 commitment, OR disclose the deviation.

Prereg-v3 S1 commits to "ODI per biomarker variable on the combined corpus". Paper A §3.5 narratively describes NSCLC prior-EGFR-TKI heterogeneity ("some trials require prior 1st/2nd-gen TKI, others require prior osimertinib") without any computed ODI. The v2 ODI code at `analysis/v2_10_compute_odi.py` is the obvious template — a 30-minute extension to NSCLC would deliver S1 honestly. Failing that, disclose: "S1 ODI is delivered for the v2 mBC corpus only (0.64, 95\% CI 0.62--0.66); extension to NSCLC awaits a v3.0.1 supplement. This is a disclosed v3 deviation."

### A8 (MEDIUM — new). Add a "single-node sensitivity" row to clarify the depth of the rejection.

The rejection is one node deep ($k_{\text{crit}} = 18$ at $n = 49$, $\alpha = 0.05$; realised $k = 19$, $P = 0.023$). A future re-adjudication that flips any one of the 19 evidence-free nodes drops the test to $P = 0.049$ (still rejects but marginally); flipping any two drops to $P = 0.084$ (fails). Add one sentence to **Paper A §3.1** (or end of §3.4 per-node breakdown):

> "The exact-binomial test's critical value at $n = 49$, $\alpha = 0.05$ is $k = 18$ ($P = 0.049$); the realised $k = 19$ ($P = 0.023$) is therefore one node above critical. If any single one of the 19 strict evidence-free nodes were re-adjudicated to supported, the test would move to $P = 0.049$ and still reject at the boundary; if two flipped, the test would fail to reject ($P = 0.084$). The headline rejection is robust to the prereg's pre-specified inference but is sensitive to per-node adjudication at one to two nodes' depth."

This is the honest characterisation of the inference, and it pre-empts the obvious "what if you'd adjudicated TROPION/N20/etc. the other way" reviewer attack.

---

## Asks summary table

| # | Severity | Topic |
|---:|---|---|
| A1 | CRITICAL | Explicit multiplicity-correction paragraph: primary survives prereg single-test framing only; BH-q grid-wide = 0.35 |
| A2 | CRITICAL | Disclose v2 → v3 S2/S3/S4 silent relabel and v2 secondary-outcome drop |
| A3 | CRITICAL | Patch Paper B §5.3 stale paragraph (24/50 → 17/49; $P=0.10$ → $0.084$) |
| A4 | HIGH | Add HARKing-defense paragraph to Paper A (Paper B has one sentence) |
| A5 | HIGH | Disclose realised validation subset $n = 13$ vs prereg $n = 15$ |
| A6 | HIGH | Paper A NSCLC adjudication-deferred disclosure to parity with Paper B; reconcile DAS |
| A7 | MEDIUM | Compute NSCLC ODI per S1 commitment, OR disclose deviation |
| A8 | MEDIUM | Add single-node sensitivity row ($k_{\text{crit}} = 18$; rejection one node deep) |

Minor housekeeping (not numbered):
- Paper A L133 "50 pooled guideline nodes" → 49.
- Paper A "Three caveats" L145 "$P = 0.10$" → $P = 0.084$.
- Bootstrap CI lower bound 0.2449 rounds to 0.24, not 0.25 (both papers).
- Paper B §5 limitations "$p_1 \ge 0.45$" → "$p_1 \ge 0.43$" (R1 A13 carryover).

---

## VERDICT

**MAJOR** revision.

The R1 CRITICAL biostats deliverables — bootstrap CI (A7), Paper B NSCLC κ-gate disclosure (A3), no-NSCLC-adjudication disclosure (A5) — landed cleanly in commit `4ff3cdd`. The spot-check arithmetic is exact: every one of the eight requested 4-decimal cells reproduces against the JSON, the bootstrap function exists and is called for all 15 cells, and the pre-registered primary holds at $P = 0.023$ under the prereg's "single primary inferential commitment" framing.

The MAJOR drivers this round are:

1. **(A1) The multiplicity-correction picture inverted between R1 and R2.** At the pre-R1 $P = 0.0004$ the primary survived BH at $P \le 0.006$; at the post-R1 $P = 0.023$ the primary's BH-q across the 15-cell grid is **0.35**, and even Bonferroni-3 across primary tolerances is 0.07. The rejection now hinges entirely on the prereg's "single primary inferential commitment" framing being explicitly defended in the manuscript. R1 ask A1 (MEDIUM at R1) is now CRITICAL.

2. **(A2) The v2 → v3 silent S2/S3/S4 relabel** (R1 A8 CRITICAL, unaddressed in both R1 integration and R2 integration) remains the largest prereg-honesty defect.

3. **(A3) The R2 stale-number sweep missed Paper B §5.3** — a paragraph titled "Tolerance-sensitivity grid" that gives wrong cell counts, wrong denominator, and wrong $P$ in a single sentence. Cleanly fixable in 1 edit.

4. **(A4) Paper A still has no HARKing-defense paragraph**, only Paper B does (one sentence). With the corrected $P = 0.023$ sitting one node above critical (single-node sensitivity, ask A8), the HARKing attack is more accessible to a hostile reviewer, not less.

5. **(A5, A6) Paper A still does not disclose** the realised validation subset $n = 13$ vs prereg $n = 15$, and does not bring its NSCLC adjudication disclosure to parity with Paper B. The "Three caveats" L145 sentence is the v2-A5-analogue misleading framing (joint mBC/NSCLC "with documented adjudication trail") that R1 caught for Paper B and is now reproduced in Paper A.

All five are fixable without re-running the primary test, and none threatens the conclusion. With A1, A2, A3 in full plus some form of A4, A5, A6, I recommend MINOR; with all 8 in some form, I recommend ACCEPT.

The pre-registered primary inference is still correct, reproduces exactly, and respects the prereg's single-test commitment. The asks above are about making the prereg discipline visible and load-bearing in the manuscript, so that the rejection stands against the multiplicity attack that the post-R1 number-correction has made the most likely critique.
