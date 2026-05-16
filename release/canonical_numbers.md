# Canonical Numbers — single source of truth for v3.0.0

> All numbers in any manuscript / release file MUST match this table.
> Source: `data/results/v3_pooled_efdpr.json` (computed by `analysis/v3_08_compute_pooled_efdpr.py`).
> Run `bash release/audit_numbers.sh` to grep for forbidden stale literals.

## Corpus

| Item | Value |
|---|---|
| NSCLC trials (post v3 R1 corrections) | 178 |
| mBC trials (from v2.0.0) | 81 |
| Total pooled corpus | 259 |
| NSCLC in-scope DAG edges | 147 |
| mBC in-scope DAG edges | 65 |
| Total DAG edges | 212 |
| Canonical source nodes | 48 |
| mBC guideline nodes | 25 |
| NSCLC guideline nodes (post N13/N14 dedup) | 24 |
| Total pooled guideline nodes (n) | 49 |

## Primary outcome (strict tolerance)

| Quantity | Value |
|---|---|
| Evidence-free count (k) | 19 |
| EFDPR point estimate | 0.388 (round to 0.39 in prose) |
| Clopper-Pearson 95% CI | [0.252, 0.538] (write as 0.25–0.54) |
| Bootstrap percentile 95% CI | [0.245, 0.531] (write as 0.25–0.53) |
| Exact one-sided P vs p₀=0.25 | 0.0231 (write as 0.023) |
| Reject H₀ at α=0.05? | **YES** |
| Critical k for rejection | 18 (one-node-deep rejection) |

## Sensitivity (strict tolerance)

| Subset | k/n | EFDPR | CP-CI | Boot-CI | Exact P | Reject? |
|---|---|---|---|---|---|---|
| ESCAT-aligned | 17/49 | 0.347 | [0.217, 0.496] | [0.224, 0.490] | 0.0836 | no |
| Liberal | 17/49 | 0.347 | [0.217, 0.496] | [0.224, 0.490] | 0.0836 | no |
| mBC-only | 10/25 | 0.400 | [0.211, 0.613] | [0.200, 0.600] | 0.0713 | no |
| NSCLC-only | 9/24 | 0.375 | [0.188, 0.594] | [0.208, 0.583] | 0.1213 | no |
| NSCLC EGFR-only | 7/17 | 0.412 | [0.184, 0.671] | [0.176, 0.647] | 0.1071 | no |
| NSCLC ALK-only | 2/7 | 0.286 | [0.037, 0.710] | [0.000, 0.571] | 0.5551 | no |

## Trajectory across versions

| Version | Scope | EFDPR | P | Reject? |
|---|---|---|---|---|
| v1.0.0 | mBC pilot (n=16) | 0.31 | 0.37 | fails |
| v2.0.0 | mBC production (n=25) | 0.40 | 0.07 | marginal |
| **v3.0.0** | **mBC + NSCLC pooled (n=49)** | **0.39** | **0.023** | **rejects** |

## Pre-registration trail

| Commit | What |
|---|---|
| `085ae54` | prereg-v2 (mBC production) BEFORE outcome data |
| `079b540` | prereg-v2 amendment v2.1 BEFORE extraction |
| `4b5bf1a` | prereg-v3 (NSCLC + multi-tumor pooled) BEFORE NSCLC outcome data |

## Multiplicity caveat

Rejection is **one-node-deep**: k_crit=18, observed k=19. If 1 evidence-free node flips to supported, P=0.049 (still marginally rejects). If 2 flip, P=0.084 (fails). BH-q across the 15-cell tolerance×subset grid = 0.35 (Bonferroni-15 same magnitude). The defense for primary rejection is that prereg-v3 commits the **single primary inferential commitment** as the pooled strict-tolerance test; tolerance-grid and tumor-stratified results are sensitivity, not independent confirmatory tests.

## FORBIDDEN STALE LITERALS

The following are stale and must NEVER appear in v3.0.0 release files:
- "P = 0.0004" / "P=0.0004"
- "EFDPR 0.48" / "EFDPR = 0.48"
- "50-node" / "n = 50" / "n=50"
- "261 trials" / "261-trial"
- "210 edges (145 NSCLC"
- "180 NSCLC trials" / "180 trials"
- "12 of 17 EGFR" / "12 EGFR-mutant"
- "0.71" as EGFR-only EFDPR
- "P = 0.0009" / "P = 0.0001" / "P = 0.63" (as NSCLC subset Ps)
- "P = 0.10" (as ESCAT/liberal P; correct is 0.084)

Run `bash release/audit_numbers.sh` to grep for these across all release files. CI should fail if any are found.
