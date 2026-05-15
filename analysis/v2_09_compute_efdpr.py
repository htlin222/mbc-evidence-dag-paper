"""v2_09_compute_efdpr.py
Compute EFDPR on the v2 expanded corpus + ASCO/NCCN sensitivity.

Per prereg-v2:
  - Primary analysis: strict-tolerance EFDPR on the full 25-node decision
    tree (ESMO + ASCO + NCCN unique nodes), with one-sided exact binomial
    test of H0: EFDPR <= 0.25 at alpha = 0.05.
  - Sensitivity: ESMO-only nodes, ASCO-only nodes, NCCN-only nodes.
  - Tolerance grid: strict / ESCAT / liberal (sensitivity, not three tests).
"""
from __future__ import annotations

import json
import random
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EDGES = ROOT / "data" / "processed" / "v2_dag_edges.json"
GL    = ROOT / "data" / "processed" / "v2_decision_tree.json"
OUT   = ROOT / "data" / "results" / "v2_efdpr.json"
OUT.parent.mkdir(parents=True, exist_ok=True)


ESCAT_GROUPS = {
    "AKTpath":   {"AKTpath", "PIK3CAmut"},
    "PIK3CAmut": {"PIK3CAmut"},
}

DRUG_CLASS_EQUIVALENCE = {
    "CDK4/6i + AI":                                 {"CDK4/6i + AI"},
    "CDK4/6i + fulvestrant":                        {"CDK4/6i + fulvestrant"},
    "CDK4/6i + endocrine (pre-menopausal)":         {"CDK4/6i + endocrine (pre-menopausal)"},
    "CDK4/6i + fulvestrant (post-CDK4/6i)":         {"CDK4/6i + fulvestrant (post-CDK4/6i)"},
    "PI3Ki + fulvestrant":                          {"PI3Ki + fulvestrant"},
    "PI3Ki triplet (inavolisib + CDK4/6i + fulv)":  {"PI3Ki triplet (inavolisib + CDK4/6i + fulv)"},
    "AKTi + fulvestrant":                           {"AKTi + fulvestrant"},
    "AKTi + chemotherapy":                          {"AKTi + chemotherapy"},
    "SERD oral":                                    {"SERD oral"},
    "SERD oral + CDK4/6i":                          {"SERD oral + CDK4/6i"},
    "HER2-ADC (T-DXd)":                             {"HER2-ADC (T-DXd)"},
    "HER2-ADC (other)":                             {"HER2-ADC (other)", "HER2-ADC (T-DXd)"},
    "TROP2-ADC (sacituzumab govitecan)":            {"TROP2-ADC (sacituzumab govitecan)"},
    "TROP2-ADC (datopotamab deruxtecan)":           {"TROP2-ADC (datopotamab deruxtecan)"},
    "PARPi (olaparib)":                             {"PARPi (olaparib)", "PARPi (talazoparib)"},
    "PARPi (talazoparib)":                          {"PARPi (olaparib)", "PARPi (talazoparib)"},
    "everolimus + exemestane":                      {"everolimus + exemestane"},
    "chemotherapy":                                 {"chemotherapy", "chemotherapy single agent"},
    "chemotherapy single agent":                    {"chemotherapy", "chemotherapy single agent"},
    "endocrine therapy alone":                      {"endocrine therapy alone"},
}


def _state_tokens(s):  return set(s.split("+"))
def _bm_tokens(b):     return set(b.split("/"))


def _state_match(edge_state, gl_state):
    gl_tokens = _state_tokens(gl_state)
    # special line-agnostic tokens for gBRCAm and indolent/visceral-crisis nodes
    for special in ("metastatic", "indolent", "visceral-crisis"):
        if special in gl_tokens:
            gl_tokens = gl_tokens - {special}
    return gl_tokens.issubset(_state_tokens(edge_state))


def _bm_match_strict(e, g, _sub):
    return _bm_tokens(e) == _bm_tokens(g)


def _bm_match_escat(e, g, _sub):
    if _bm_match_strict(e, g, _sub):
        return True
    e_set, g_set = _bm_tokens(e), _bm_tokens(g)
    core_g = g_set & {"HR+", "HER2-"}
    core_e = e_set & {"HR+", "HER2-"}
    if core_g and core_g != core_e:
        return False
    non_core = g_set - {"HR+", "HER2-"}
    for tok in non_core:
        if not (ESCAT_GROUPS.get(tok, {tok}) & e_set):
            return False
    return True


def _bm_match_liberal(e, g, sub):
    if _bm_match_escat(e, g, sub):
        return True
    e_set, g_set = _bm_tokens(e), _bm_tokens(g)
    core_g = g_set & {"HR+", "HER2-"}
    core_e = e_set & {"HR+", "HER2-"}
    if core_g and core_g != core_e:
        return False
    non_core = g_set - {"HR+", "HER2-"}
    subset = set(sub or [])
    for tok in non_core:
        if tok in e_set or tok in subset: continue
        if ESCAT_GROUPS.get(tok, {tok}) & (e_set | subset): continue
        return False
    return True


MATCHERS = {"strict": _bm_match_strict, "escat": _bm_match_escat, "liberal": _bm_match_liberal}


def _drug_match(ec, rec_classes):
    if ec in rec_classes: return True
    return bool(DRUG_CLASS_EQUIVALENCE.get(ec, {ec}) & rec_classes)


def supports(edge, gl, tol):
    if not _state_match(edge["source_state"], gl["state"]): return False
    rec_classes = {r["class"] for r in gl["recommended_classes"]}
    if not _drug_match(edge["drug_class"], rec_classes): return False
    if not MATCHERS[tol](edge["biomarker"], gl["biomarker"], edge.get("subgroup_readouts") or []): return False
    if int(edge["year_pc"]) > int(gl["year"]): return False
    return True


def efdpr(edges, gls, tol):
    ef, per = [], {}
    for g in gls:
        sup = [e["nct_id"] for e in edges if supports(e, g, tol)]
        per[g["node_id"]] = sup
        if not sup: ef.append(g["node_id"])
    return (len(ef) / len(gls)) if gls else 0.0, len(ef), len(gls), ef, per


def exact_binomial_p(k, n, p0=0.25):
    return sum(comb(n, x) * (p0 ** x) * ((1 - p0) ** (n - x)) for x in range(k, n + 1))


def clopper_pearson(k, n, alpha=0.05):
    from scipy.stats import beta
    lo = 0.0 if k == 0 else float(beta.ppf(alpha/2, k, n - k + 1))
    hi = 1.0 if k == n else float(beta.ppf(1 - alpha/2, k + 1, n - k))
    return lo, hi


def bootstrap_ci(edges, gls, tol, n=1000, seed=20260516):
    rng = random.Random(seed)
    est = []
    for _ in range(n):
        sample = [rng.choice(gls) for _ in range(len(gls))]
        p, *_ = efdpr(edges, sample, tol)
        est.append(p)
    est.sort()
    lo = est[max(0, int(0.025*n) - 1)]
    hi = est[min(n-1, int(0.975*n))]
    return lo, hi


def run_one_subset(edges, gls, label):
    out = {"label": label, "n_nodes": len(gls)}
    for tol in ("strict", "escat", "liberal"):
        p, k, n, ef, per = efdpr(edges, gls, tol)
        lo, hi = bootstrap_ci(edges, gls, tol)
        cp_lo, cp_hi = clopper_pearson(k, n)
        pval = exact_binomial_p(k, n, 0.25)
        out[tol] = {
            "point_estimate": round(p, 4),
            "evidence_free_count": k,
            "total_nodes": n,
            "clopper_pearson_ci95": [round(cp_lo, 4), round(cp_hi, 4)],
            "bootstrap_ci95":       [round(lo, 4),    round(hi, 4)],
            "exact_binomial_pvalue_one_sided_vs_p25": round(pval, 4),
            "rejects_h0_at_alpha_05": bool(pval < 0.05),
            "evidence_free_nodes": ef,
            "per_node_support": per,
        }
        print(f"    {tol:<8s} EFDPR={p:.3f}  CP-CI=[{cp_lo:.3f},{cp_hi:.3f}]  P={pval:.4f}  {'REJECT' if pval<0.05 else 'fails to reject'}")
    return out


def main() -> None:
    edges = json.loads(EDGES.read_text())
    gls   = json.loads(GL.read_text())
    print(f"Trial-DAG edges (in-scope): {len(edges)}")
    print(f"Guideline decision nodes: {len(gls)}")
    print()
    print("== Primary: all 25 nodes (ESMO+ASCO+NCCN unified) ==")
    primary = run_one_subset(edges, gls, "primary_all")
    # Sensitivity subsets
    esmo_only = [g for g in gls if "ESMO" in g["source"]]
    asco_only = [g for g in gls if "ASCO" in g["source"]]
    nccn_only = [g for g in gls if "NCCN" in g["source"]]
    print(f"\n== Sensitivity 1: ESMO-only ({len(esmo_only)} nodes) ==")
    sens_esmo = run_one_subset(edges, esmo_only, "esmo_only")
    print(f"\n== Sensitivity 2: ASCO-citing ({len(asco_only)} nodes) ==")
    sens_asco = run_one_subset(edges, asco_only, "asco_only")
    print(f"\n== Sensitivity 3: NCCN-citing ({len(nccn_only)} nodes) ==")
    sens_nccn = run_one_subset(edges, nccn_only, "nccn_only")
    OUT.write_text(json.dumps({
        "primary": primary,
        "sensitivity_esmo": sens_esmo,
        "sensitivity_asco": sens_asco,
        "sensitivity_nccn": sens_nccn,
    }, indent=2))
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
