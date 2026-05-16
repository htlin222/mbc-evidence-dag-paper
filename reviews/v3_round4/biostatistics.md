# Biostatistics Review — paper_A_clinical_v3.tex + paper_B_methods_v3.tex (v3, Round 4 — FINAL)

**Reviewer role.** Adversarial biostatistics referee, v3 round 4 (final). Scope: verify (a) that the six R3 outstanding biostatistics items have landed in the manuscripts after the R3 integration commit `123a461`, and (b) that all numerical claims in both papers match `release/canonical_numbers.md` and `data/results/v3_pooled_efdpr.json`.

---

## Spot-check verification (canonical_numbers.md)

All four user-specified primary cells reproduce **exactly** against `v3_pooled_efdpr.json` and `release/canonical_numbers.md`:

| Cell | Expected | JSON | canonical_numbers.md | Match |
|---|---|---|---|---|
| Primary $P(X\ge 19\mid 49, 0.25)$ | 0.0231 | `exact_p_one_sided_vs_p25: 0.0231` | "0.0231 (write as 0.023)" | OK |
| ESCAT/liberal $P(X\ge 17\mid 49, 0.25)$ | 0.0836 | `exact_p_one_sided_vs_p25: 0.0836` (escat + liberal) | "0.0836" | OK |
| mBC-only $P(X\ge 10\mid 25, 0.25)$ | 0.0713 | `mbc_only.strict.exact_p_one_sided_vs_p25: 0.0713` | "0.0713" | OK |
| Bootstrap CIs in JSON for all 15 cells (3 tolerance × 5 subset)? | yes | every `*.{strict,escat,liberal}` block carries `bootstrap_ci95: [lo, hi]` | n/a | OK |

Bootstrap CI inventory (all 15 cells populated, seed `20260516`, `n_iter=1000`):
- primary/{strict,escat,liberal} → `[0.2449, 0.5306] / [0.2245, 0.4898] / [0.2245, 0.4898]`
- mbc_only/{strict,escat,liberal} → `[0.20, 0.60] / [0.16, 0.52] / [0.16, 0.52]`
- nsclc_only/{strict,escat,liberal} → `[0.2083, 0.5833] / [0.2083, 0.5833] / [0.2083, 0.5833]`
- nsclc_egfr_only/{strict,escat,liberal} → `[0.1765, 0.6471] / [0.1765, 0.6471] / [0.1765, 0.6471]`
- nsclc_alk_only/{strict,escat,liberal} → `[0.00, 0.5714] / [0.00, 0.5714] / [0.00, 0.5714]`

R1 ask A7 (bootstrap CI computed for all sensitivity cells) remains fully closed at the data layer. Papers still only quote the primary bootstrap CI in prose, which is acceptable.

---

## R3 outstanding biostats items — post-`123a461` status

The R3 integration commit `123a461` (sole post-`dadf797` commit) had scope *"programmatic stale-literal sweep + figure script de-hardcoding + canonical numbers"*. The diff against the two TeX files is **5 lines in Paper A and 3 lines in Paper B**, all of them stale-literal fixes (`50` → `49`, `P = 0.10` → `P = 0.084`, `180/145` → `178/147`, `P = 0.63` → `P = 0.56`, `24/50 → 17/50` → `17/49 → 17/50`). **No new biostats prose was added.** Status of each R3 outstanding item:

| R3 item | Severity | Post-R3 status in manuscripts |
|---|---|---|
| **1. Multiplicity discussion across 15-cell tolerance × subset grid** | CRITICAL (R3 A1) | **NOT ADDRESSED.** `grep -E "multiplicity\|BH\|Bonferroni\|Benjamini\|family-wise"` returns zero hits in both papers. The single most consequential R3 finding — that the primary survives only under the prereg's single-test framing (BH-q = 0.35 across the 15-cell grid; Bonferroni-3 across primary tolerances = 0.07) — has zero defense in the manuscripts. |
| **2. S2/S3/S4 silent relabel from v2 prereg** | CRITICAL (R3 A2 = R1 A8) | **NOT ADDRESSED.** No "Pre-registration deviations from v2" subsection in either paper. v2 S2 (temporal evidence lag), v2 S3 (Asian/age≥70/Black ancestry subgroup coverage), v2 S4 (composition-only citation count) remain silently dropped. v3 S1–S4 still re-use the same labels with NSCLC-specific re-definitions without disclosure. |
| **3. One-node-deep rejection disclosure** | MEDIUM (R3 A8) | **NOT ADDRESSED.** No mention of $k_{\text{crit}} = 18$, "one node above critical", or sensitivity to single-node re-adjudication. The R3 honest characterisation ("if any single one of the 19 flips: $P = 0.049$; if two flip: $P = 0.084$") is absent. |
| **4. HARKing defense paragraph (Paper A)** | HIGH (R3 A4 = R1 A2 Paper A side) | **NOT ADDRESSED in Paper A.** Paper B still has the single sentence at §5.4 L133 ("structural defence against the HARKing-equivalent concern"); Paper A has zero defense. With the corrected $P = 0.023$ sitting one node above critical, the v1 → v2 → v3 trajectory attack is more accessible, not less. |
| **5. Realised $n = 13$ vs prereg $n = 15$ validation subset** | HIGH (R3 A5 = R1 A4) | **NOT ADDRESSED.** Paper A §2.3 L84 still says "Annotator B (Codex / GPT-5) on a 15-trial validation subset". Neither paper acknowledges `v3_nsclc_kappa.json:n_validation = 13`. |
| **6. NSCLC ODI per S1 commitment** | MEDIUM (R3 A7 = R1 A9) | **NOT ADDRESSED.** Paper A §3.5 L128 still narratively describes "analogous heterogeneity" for NSCLC prior-EGFR-TKI inclusion ("some trials require prior 1st/2nd-gen TKI, others require prior osimertinib, others permit either") without any computed ODI and no S1-deviation disclosure. |

**Net R3 → R4 delta: 0 of 6 outstanding biostats items addressed.** R3 integration was strictly a number-correction sweep; the entire R3 substantive biostats agenda is unmoved.

---

## Two new stale-number escapes from the R3 sweep

The R3 sweep was programmatic (per the commit message), and three literal-pattern escapes remain in the manuscripts:

### Escape 1. Paper A Discussion "Headline" L133

> "At adequately-powered multi-tumor scale (**50 pooled guideline nodes** across mBC HR+/HER2- and NSCLC EGFR + ALK), ..."

Should be **49 pooled guideline nodes**. The audit script (`release/audit_numbers.sh`) catches `"n = 50"`, `"50-node"`, `"261 trials"`, etc., but does not catch the prose phrase "50 pooled guideline nodes" (no hyphen, no `n =`). One of three R3 "50-node" escapes flagged by R3 review still present (R3 ask: housekeeping bullet, unfixed).

### Escape 2. Paper B §5.3 "Tolerance-sensitivity grid" L130

Current text:

> "ESCAT-aligned and liberal tolerance gave 0.347 (17/49 $\to$ **17/50**; $P = 0.084$), failing to reject."

The numerator was corrected (24 → 17) and the $P$ was corrected (0.10 → 0.084), but the **denominator on the right-hand side of the arrow is still 50, not 49**. The arrow `17/49 → 17/50` is semantically nonsensical (a 17/49 outcome at strict tolerance cannot "go to" 17/50 at ESCAT/liberal because the denominator is the same 49 nodes; the right-hand side is a leftover stale literal). Replace with `(17/49; $P = 0.084$)` per R3 ask A3.

### Escape 3. Paper A Discussion "NSCLC EGFR post-osimertinib" L136

> "Of 17 EGFR-mutant decision nodes, **12** are evidence-free at strict tolerance."

JSON: `nsclc_egfr_only.strict.evidence_free_count = 7`. The correct figure is **7 of 17**, not 12. This is the same stale literal that the audit script does flag as `"12 of 17 EGFR"` and `"12 EGFR-mutant"`, but the manuscript phrasing inverts the word order ("Of 17 ... 12 are evidence-free") so the grep escapes it. This is a **number-shifting stale literal** that contradicts both the JSON and the immediately-preceding Results §3.3 ("NSCLC EGFR-only ($n = 17$) 0.41 ($P = 0.11$)") — 0.41 × 17 = 7, not 12.

This is the most consequential of the three escapes because it (i) contradicts the JSON, (ii) contradicts Results §3.3, and (iii) sits in the Discussion's headline NSCLC paragraph that a hostile reviewer will read first.

---

## Net status

| Category | R1 | R2 | R3 | R4 |
|---|---|---|---|---|
| Bootstrap CI computed (15 cells) | not done | done | done | done |
| Bulk stale-number sweep | partial | partial | mostly done | 3 escapes remain |
| Multiplicity defense | flagged MEDIUM | escalated CRITICAL | flagged CRITICAL | **not addressed** |
| S2/S3/S4 silent relabel disclosure | flagged CRITICAL | unmoved | flagged CRITICAL | **not addressed** |
| Paper A HARKing defense | flagged HIGH | unmoved | flagged HIGH | **not addressed** |
| n=13 vs prereg-15 disclosure | flagged HIGH | unmoved | flagged HIGH | **not addressed** |
| Paper A NSCLC adjudication parity | flagged HIGH | unmoved | flagged HIGH | **not addressed** |
| NSCLC ODI per S1 | flagged HIGH | unmoved | flagged MEDIUM | **not addressed** |
| One-node-deep sensitivity row | flagged MEDIUM (new R3) | n/a | flagged MEDIUM | **not addressed** |

The pre-registered primary inference is computationally correct at $P = 0.023$ on 19/49 strict, and the data layer is clean. The defects are all in the **disclosure and defense layer**: the manuscripts do not pre-empt the multiplicity attack that the post-R1 number correction made the most likely critique, do not disclose the v2 → v3 prereg-label re-use, do not bring Paper A's NSCLC disclosure to parity with Paper B, do not acknowledge the realised-vs-prereg validation $n$ mismatch, and do not characterise the depth of the rejection (one node above critical).

---

## Concrete asks (6) — final

### A1 (CRITICAL — R3 A1 carry-over). Add explicit multiplicity-correction paragraph to BOTH papers.

Required in **Paper A end of §3.1** and **Paper B §3.3** (Tolerance-sensitivity grid). Suggested text (adapt as needed):

> "Because prereg-v3 (commit \texttt{4b5bf1a}) commits the pooled strict-tolerance test as the single primary inferential commitment, multiplicity correction across the tolerance-grid (sensitivity) cells is not applied. If a reviewer prefers a family-wise framing across all 15 (3 tolerance × 5 subset) cells reported in `v3_pooled_efdpr.json`, the pre-registered primary's raw $P = 0.023$ rises to BH-q $= 0.35$ and Bonferroni-15 $= 0.35$ — i.e., the rejection depends on the prereg's single-test framing. We hold the prereg framing on three grounds: (i) the tolerance grid is one outcome under three operationalizations, not three outcomes; (ii) the tumor-stratified subsets are sensitivity, not pre-specified independent tests; (iii) the prereg was committed before any NSCLC outcome-touching analysis."

Without this paragraph a strict reviewer will mechanically apply Bonferroni-15 and reject the rejection unrebutted. Already cleanly fixable; one paragraph in each paper.

### A2 (CRITICAL — R3 A2 = R1 A8 carry-over). Disclose v2 → v3 S2/S3/S4 silent relabel.

Add a "Pre-registration deviations from v2" subsection to **Paper A Methods §2.1** (and a parallel sentence to Paper B §5.1). Suggested text:

> "The v3 prereg (\texttt{docs/prereg-v3.md}, commit \texttt{4b5bf1a}, lines 64--67) re-uses the labels S1--S4 with v3-specific definitions (S1 ODI on combined corpus; S2 tumor-stratified EFDPR; S3 cross-tumor consistency; S4 LLM-extraction inter-rater agreement at production scale). This is a relabel, not a continuation of v2's S1--S4. The v2 secondary outcomes — v2 S2 (temporal evidence lag from guideline-node introduction to earliest supporting trial PC), v2 S3 (Asian / age $\ge 70$ / Black ancestry subgroup coverage), v2 S4 (composition-only citation count) — are not recomputed in v3; v2's S2/S3/S4 results remain on record at the v2.0.0 tag and are not modified by v3. This is a disclosed v3 deviation."

This is the largest prereg-honesty defect that has carried unaddressed from R1 → R2 → R3 → R4.

### A3 (HIGH — fix 3 R3-sweep stale-number escapes).

Three single-line edits, all numerical:

- **Paper A L133.** `50 pooled guideline nodes` → `49 pooled guideline nodes`.
- **Paper A L136.** `Of 17 EGFR-mutant decision nodes, 12 are evidence-free at strict tolerance` → `Of 17 EGFR-mutant decision nodes, 7 are evidence-free at strict tolerance` (matches JSON `nsclc_egfr_only.strict.evidence_free_count = 7` and Results §3.3 "0.41 × 17 = 7").
- **Paper B L130.** `0.347 (17/49 $\to$ 17/50; $P = 0.084$)` → `0.347 (17/49; $P = 0.084$)` (the right-hand side of the arrow is a leftover stale literal; the denominator is 49 throughout the pooled analysis).

After these three edits, also extend `release/audit_numbers.sh` with the patterns `"50 pooled guideline"`, `"17/50"`, `"12 are evidence-free"`, and `"Of 17 EGFR-mutant decision nodes, 12"` so the next sweep catches the inverted word order.

### A4 (HIGH — R3 A4 = R1 A2 Paper A carry-over). Add HARKing-defense paragraph to Paper A.

Paper B has one sentence (§5.4 L133). Paper A — the clinical, higher-readership paper, and the one where reviewers will look for the trajectory-defense argument — has zero. Add to Paper A Discussion (as a new paragraph after "Three positives" or as a new "Why this isn't HARKing" paragraph). With the corrected $P = 0.023$ one node above critical, this defense is more important, not less. Suggested text already in R3 review ask A4 (lines 178–180); reproduce verbatim.

### A5 (HIGH — R3 A5/A6 carry-over). Disclose realised $n = 13$ validation subset AND bring Paper A NSCLC adjudication disclosure to Paper B parity.

Two related sentences in Paper A:

- **Paper A §2.3** (after L84): "The realised NSCLC validation subset was 13 of the pre-registered 15 trials; two trials were dropped due to round-1 NCT corrections. This is a disclosed minor deviation. A formal NSCLC adjudication pass analogous to v2 mBC (which had 17 adjudication rules) was not run for the v3 NSCLC arm; the pre-adjudication kappa gate failed on \texttt{post\_alk\_tki}, \texttt{egfr\_t790m}, and \texttt{drug\_class}. A formal NSCLC adjudication pass is deferred to v3.0.1."

- **Paper A "Three caveats" L145**: split the joint mBC/NSCLC "with documented adjudication trail" phrasing — true for mBC (v2's 17 rules) and not true for NSCLC (zero rules). Either rewrite or cross-reference the §2.3 disclosure.

Paper B §5.2 L127 already says this; Paper A needs to match.

### A6 (MEDIUM — R3 A8 + R3 A7 carry-overs combined). Add a one-paragraph "depth of rejection" + "S1 deviation" disclosure to Paper A.

Two related items in one paragraph:

- **One-node-deep sensitivity.** "The exact-binomial test's critical value at $n = 49$, $\alpha = 0.05$ is $k = 18$ ($P = 0.049$); the realised $k = 19$ ($P = 0.023$) is therefore one node above critical. If any single one of the 19 strict evidence-free nodes were re-adjudicated to supported, the test would move to $P = 0.049$ and still reject at the boundary; if two flipped, the test would fail to reject ($P = 0.084$). The headline rejection is robust to the prereg's pre-specified inference but is sensitive to per-node adjudication at one to two nodes' depth."

- **S1 ODI deviation.** "S1 ODI is delivered for the v2 mBC corpus only (0.64, 95\% CI 0.62--0.66); extension to NSCLC awaits a v3.0.1 supplement. This is a disclosed v3 deviation."

Both can be folded into a single Methods/Discussion paragraph.

---

## Asks summary

| # | Severity | Topic |
|---:|---|---|
| A1 | CRITICAL | Multiplicity-correction paragraph in both papers (BH-q = 0.35 grid-wide, primary survives only under prereg single-test framing) |
| A2 | CRITICAL | "Pre-registration deviations from v2" subsection: S2/S3/S4 relabel + v2 secondary-outcome drop |
| A3 | HIGH | Fix 3 R3-sweep stale-number escapes (Paper A L133 "50 pooled"; Paper A L136 "12 are evidence-free" → 7; Paper B L130 "17/50") |
| A4 | HIGH | Paper A HARKing-defense paragraph (Paper B has one sentence) |
| A5 | HIGH | Paper A: disclose n=13 vs prereg-15 + NSCLC adjudication-deferred parity with Paper B |
| A6 | MEDIUM | One-node-deep sensitivity row + S1 NSCLC ODI deviation disclosure |

---

## VERDICT

**MAJOR** revision.

The R3 integration `123a461` delivered a clean programmatic stale-literal sweep (matching the commit-message scope) and the data layer is correct: every spot-check P-value matches the JSON to 4 decimals, all 15 tolerance×subset cells carry bootstrap CIs, the canonical_numbers.md table is the single source of truth, and the audit script passes on 11 release files.

But the R3 integration **did not advance any of the six R3 outstanding biostats items** (multiplicity, S2/S3/S4 relabel, one-node-deep rejection, Paper A HARKing defense, n=13 validation disclosure, NSCLC ODI). All six were flagged at R3 as CRITICAL or HIGH (A1 + A2 CRITICAL; A4, A5, A6 HIGH; A3, A7, A8 MEDIUM), and all six remain literally unchanged. Additionally, three stale-number patterns escaped the R3 programmatic sweep because of word-order inversion or right-hand-side-of-arrow context (Paper A L133 "50 pooled guideline nodes"; Paper A L136 "12 are evidence-free"; Paper B L130 "17/50") — one of which (Paper A L136) is a number-shifting contradiction with the immediately-preceding Results §3.3.

The pre-registered primary inference at $P = 0.023$ is real and reproduces, but it is one node above critical and survives only under the prereg's "single primary inferential commitment" framing. The rejection therefore stands or falls on whether the manuscript makes that framing load-bearing and defensible — and at present, neither paper does so. A strict adversarial reviewer will mechanically apply Bonferroni-15 (q = 0.35) and unrebutted reject the rejection.

**Path to ACCEPT:** A1 + A2 + A3 in full, plus some form of A4 + A5 → MINOR. A1–A6 in full → ACCEPT. Two of these (A3, A6) are one-paragraph or three-line edits. A1, A2, A4, A5 are each one paragraph. Total estimated additional manuscript text: ≈ 600 words across both papers.

The biostatistics inference is sound and the data layer is releasable. The disclosure/defense layer is incomplete in a way that the multiplicity-correction picture (post the R1 number correction) has made structurally load-bearing.

**MAJOR.**
