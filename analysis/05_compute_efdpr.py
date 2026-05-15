"""05_compute_efdpr.py
Compute the Evidence-Free Decision-Point Ratio (EFDPR) under three
biomarker-definition tolerance levels.

Concordance criteria (all four must hold):
  (1) STATE-MATCH:   trial-required prior states are a SUPERSET of the
                     guideline-node state. Rationale: a trial that requires
                     patients to be post-CDK4/6i AND post-endo can support
                     a guideline node requiring only post-CDK4/6i.
  (2) BIOMARKER-MATCH (tolerance-dependent):
        STRICT:      trial biomarker set equals guideline biomarker set.
        ESCAT:       STRICT, plus accept ESCAT-equivalence groupings (e.g.
                     AKT-pathway-alteration <-> PIK3CAmut at ESCAT tier I/II).
        LIBERAL:     ESCAT, plus accept registrational SUBGROUP readouts
                     (trial enrolled all-comers and the registrational subgroup
                     readout matches the guideline biomarker).
  (3) DRUG-MATCH:    trial drug class is among guideline-recommended classes
                     (with class-family equivalence: CDK4/6i partners, HER2-ADCs).
  (4) TEMPORAL:      trial primary-completion year <= guideline-version year.

Output: data/results/efdpr.json
"""
from __future__ import annotations

import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EDGES = ROOT / "data" / "processed" / "dag_edges.json"
GL    = ROOT / "data" / "processed" / "esmo_decision_tree.json"
OUT   = ROOT / "data" / "results" / "efdpr.json"
OUT.parent.mkdir(parents=True, exist_ok=True)

ESCAT_GROUPS = {
    # ESCAT-grouped variables for HR+/HER2- mBC.
    # Each token maps to the set of equivalent tokens accepted under ESCAT.
    "AKTpath":   {"AKTpath", "PIK3CAmut"},
    "PIK3CAmut": {"PIK3CAmut"},
}


def _state_tokens(s: str) -> set:
    return set(s.split("+"))


def _bm_tokens(b: str) -> set:
    return set(b.split("/"))


def _state_match(edge_state: str, gl_state: str) -> bool:
    """Trial state must include all guideline-required prior states.

    Special token 'metastatic' marks a line-agnostic guideline node (e.g.
    gBRCAm PARPi recommendation) and is satisfied by any edge state."""
    gl_tokens = _state_tokens(gl_state)
    if "metastatic" in gl_tokens:
        gl_tokens = gl_tokens - {"metastatic"}
    return gl_tokens.issubset(_state_tokens(edge_state))


def _biomarker_match_strict(edge_bm: str, gl_bm: str, edge_subgroups: list) -> bool:
    return _bm_tokens(edge_bm) == _bm_tokens(gl_bm)


def _biomarker_match_escat(edge_bm: str, gl_bm: str, edge_subgroups: list) -> bool:
    if _biomarker_match_strict(edge_bm, gl_bm, edge_subgroups):
        return True
    # ESCAT: allow guideline biomarker tokens to be replaced by their ESCAT group
    e = _bm_tokens(edge_bm)
    g = _bm_tokens(gl_bm)
    expanded_g = set()
    for tok in g:
        expanded_g |= ESCAT_GROUPS.get(tok, {tok})
    # require the guideline core (HR+/HER2-) is matched
    core_g = g & {"HR+", "HER2-"}
    core_e = e & {"HR+", "HER2-"}
    if core_g and core_g != core_e:
        return False
    # require every non-core guideline token has an equivalent in the edge
    non_core_g = g - {"HR+", "HER2-"}
    for tok in non_core_g:
        if not (ESCAT_GROUPS.get(tok, {tok}) & e):
            return False
    return True


def _biomarker_match_liberal(edge_bm: str, gl_bm: str, edge_subgroups: list) -> bool:
    if _biomarker_match_escat(edge_bm, gl_bm, edge_subgroups):
        return True
    # LIBERAL: accept registrational subgroup readouts.
    # Trial must satisfy guideline core (HR+/HER2-) and the guideline biomarker
    # token must be either in the trial biomarker set OR in the trial's
    # explicitly declared subgroup_readouts.
    e = _bm_tokens(edge_bm)
    g = _bm_tokens(gl_bm)
    core_g = g & {"HR+", "HER2-"}
    core_e = e & {"HR+", "HER2-"}
    if core_g and core_g != core_e:
        return False
    non_core_g = g - {"HR+", "HER2-"}
    sub = set(edge_subgroups or [])
    for tok in non_core_g:
        if tok not in e and tok not in sub:
            # also accept ESCAT-grouped subgroup readouts
            if not (ESCAT_GROUPS.get(tok, {tok}) & (e | sub)):
                return False
    return True


BIO_MATCHERS = {
    "strict":  _biomarker_match_strict,
    "escat":   _biomarker_match_escat,
    "liberal": _biomarker_match_liberal,
}


def _drug_match(edge_class: str, recommended: list) -> bool:
    rec_classes = {r["class"] for r in recommended}
    if edge_class in rec_classes:
        return True
    for rc in rec_classes:
        if edge_class.startswith("CDK4/6i") and rc.startswith("CDK4/6i"):
            return True
        if edge_class.startswith("HER2-ADC") and rc.startswith("HER2-ADC"):
            return True
        if edge_class.startswith("SERD") and rc.startswith("SERD"):
            return True
        if edge_class.startswith("AKTi") and rc.startswith("AKTi"):
            return True
        if edge_class.startswith("PI3Ki") and rc.startswith("PI3Ki"):
            return True
    return False


def _temporal_ok(edge_year: int, gl_year: int) -> bool:
    return int(edge_year) <= int(gl_year)


def supports(edge: dict, gl: dict, tolerance: str) -> bool:
    if not _state_match(edge["source_state"], gl["state"]):
        return False
    if not BIO_MATCHERS[tolerance](edge["biomarker"], gl["biomarker"], edge.get("subgroup_readouts") or []):
        return False
    if not _drug_match(edge["drug_class"], gl["recommended_classes"]):
        return False
    if not _temporal_ok(edge["year_pc"], gl["year"]):
        return False
    return True


def efdpr(edges: list, gls: list, tolerance: str) -> tuple[float, int, int, list[str], dict]:
    evidence_free = []
    per_node_support = {}
    for g in gls:
        supp = [e["nct_id"] for e in edges if supports(e, g, tolerance)]
        per_node_support[g["node_id"]] = supp
        if not supp:
            evidence_free.append(g["node_id"])
    return (len(evidence_free) / len(gls),
            len(evidence_free), len(gls),
            evidence_free, per_node_support)


def bootstrap_efdpr(edges: list, gls: list, tolerance: str, n: int = 1000, seed: int = 20260516):
    """Standard percentile-bootstrap. Resampling unit: guideline nodes."""
    rng = random.Random(seed)
    estimates = []
    for _ in range(n):
        sample = [rng.choice(gls) for _ in range(len(gls))]
        p, _, _, _, _ = efdpr(edges, sample, tolerance)
        estimates.append(p)
    estimates.sort()
    # symmetric percentile indexing (textbook formula): ceil(alpha*n) - 1 for lower,
    # floor((1-alpha)*n) for upper, with alpha=0.025.
    lo_idx = max(0, int(0.025 * n) - 1)
    hi_idx = min(n - 1, int(0.975 * n))
    return estimates[lo_idx], estimates[hi_idx], estimates


def exact_binomial_pvalue_one_sided(k: int, n: int, p0: float) -> float:
    """One-sided exact binomial p-value for H0: p <= p0 vs H1: p > p0.

    Returns P(X >= k | n, p0).
    """
    from math import comb
    pval = 0.0
    for x in range(k, n + 1):
        pval += comb(n, x) * (p0 ** x) * ((1 - p0) ** (n - x))
    return pval


def clopper_pearson_ci(k: int, n: int, alpha: float = 0.05) -> tuple[float, float]:
    """Clopper-Pearson exact CI using scipy beta-distribution."""
    from scipy.stats import beta
    lo = 0.0 if k == 0 else float(beta.ppf(alpha / 2, k, n - k + 1))
    hi = 1.0 if k == n else float(beta.ppf(1 - alpha / 2, k + 1, n - k))
    return lo, hi


def main() -> None:
    edges = json.loads(EDGES.read_text())
    gls   = json.loads(GL.read_text())
    results = {}
    for tol in ("strict", "escat", "liberal"):
        p, k, n, ef, per = efdpr(edges, gls, tol)
        lo, hi, _ = bootstrap_efdpr(edges, gls, tol)
        cp_lo, cp_hi = clopper_pearson_ci(k, n)
        pval = exact_binomial_pvalue_one_sided(k, n, 0.25)
        results[tol] = {
            "point_estimate": round(p, 4),
            "evidence_free_count": k,
            "total_decision_nodes": n,
            "bootstrap_ci95_low":  round(lo, 4),
            "bootstrap_ci95_high": round(hi, 4),
            "clopper_pearson_ci95_low":  round(cp_lo, 4),
            "clopper_pearson_ci95_high": round(cp_hi, 4),
            "exact_binomial_pvalue_one_sided_vs_p25": round(pval, 4),
            "preregistered_test_rejected_at_alpha_05": bool(pval < 0.05),
            "evidence_free_nodes": ef,
            "per_node_support": per,
        }
        print(f"  {tol:<8s}  EFDPR={p:.3f}  bootstrapCI=[{lo:.3f},{hi:.3f}]  "
              f"CP-CI=[{cp_lo:.3f},{cp_hi:.3f}]  exact P={pval:.4f}  {'rejects' if pval<0.05 else 'fails to reject'} H0:p<=0.25")
    OUT.write_text(json.dumps(results, indent=2))
    print(f"wrote results to {OUT}")


if __name__ == "__main__":
    main()
