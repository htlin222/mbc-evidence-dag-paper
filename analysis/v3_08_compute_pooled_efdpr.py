"""v3_08_compute_pooled_efdpr.py
Pooled mBC + NSCLC EFDPR with pre-registered primary test (one-sided exact
binomial, H0: pooled EFDPR <= 0.25 at alpha=0.05), per prereg-v3 (commit 4b5bf1a).
"""
from __future__ import annotations

import json
import random
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EDGES = ROOT / "data" / "processed" / "v3_combined_dag_edges.json"
MBC_GL = ROOT / "data" / "processed" / "v2_decision_tree.json"
NSCLC_GL = ROOT / "data" / "processed" / "v3_nsclc_decision_tree.json"
OUT = ROOT / "data" / "results" / "v3_pooled_efdpr.json"
OUT.parent.mkdir(parents=True, exist_ok=True)


ESCAT_GROUPS = {
    "AKTpath": {"AKTpath", "PIK3CAmut"},
    "PIK3CAmut": {"PIK3CAmut"},
    "EGFR-T790M": {"EGFR-T790M", "EGFR-mut"},  # T790M is downstream of EGFR-mut
}


def _state_tokens(s): return set(s.split("+"))
def _bm_tokens(b):    return set(b.split("/"))


def _state_match(edge_state, gl_state):
    """State superset with special line-agnostic tokens. v3 R1 fix:
    'brain-mets' is NO LONGER stripped (was an inflation source — N20 reduced
    to N13+N15). 'brain-mets' guideline nodes are now matched only when the
    trial explicitly enrols/stratifies brain-mets cohorts (encoded via a
    subgroup_readouts entry checked by the liberal-tolerance matcher).
    """
    gl_t = _state_tokens(gl_state)
    for special in ("metastatic", "indolent", "visceral-crisis", "poor-prognosis"):
        gl_t = gl_t - {special}
    return gl_t.issubset(_state_tokens(edge_state))


def _bm_match_strict(e, g, _sub):
    """Strict: trial biomarker tokens must be a SUPERSET of guideline tokens.

    Rationale: a trial with more specific biomarker eligibility (e.g.
    EGFR-mut/EGFR-ex19del/EGFR-L858R/NSCLC) DOES support a guideline node
    with more general biomarker requirement (e.g. EGFR-mut/NSCLC). Set-
    equality was incorrect and caused 4+ NSCLC-EGFR nodes to be falsely
    evidence-free (v3 round-1 clinical reviewer ask #1-2). This is
    analogous to the state-superset rule already in place.
    """
    return _bm_tokens(g).issubset(_bm_tokens(e))


def _bm_match_escat(e, g, _sub):
    """ESCAT-aligned: strict (superset) plus ESCAT-equivalence groupings.
    Allows ESCAT-grouped tokens in the guideline to be matched by any member
    of the equivalence group present in the trial.
    """
    if _bm_match_strict(e, g, _sub): return True
    e_set, g_set = _bm_tokens(e), _bm_tokens(g)
    if "NSCLC" in g_set and "NSCLC" not in e_set: return False
    if "NSCLC" not in g_set and "NSCLC" in e_set: return False
    if {"HR+", "HER2-"} & g_set:
        if not ({"HR+", "HER2-"} & e_set): return False
    for tok in g_set - {"HR+", "HER2-", "NSCLC"}:
        if not (ESCAT_GROUPS.get(tok, {tok}) & e_set):
            return False
    return True


def _bm_match_liberal(e, g, sub):
    if _bm_match_escat(e, g, sub): return True
    e_set, g_set = _bm_tokens(e), _bm_tokens(g)
    sub_set = set(sub or [])
    if "NSCLC" in g_set and "NSCLC" not in e_set: return False
    if "NSCLC" not in g_set and "NSCLC" in e_set: return False
    core_mbc = {"HR+", "HER2-"} & g_set
    if core_mbc and not (core_mbc & e_set): return False
    for tok in g_set - {"HR+", "HER2-", "NSCLC"}:
        if tok in e_set or tok in sub_set: continue
        if ESCAT_GROUPS.get(tok, {tok}) & (e_set | sub_set): continue
        return False
    return True


MATCHERS = {"strict": _bm_match_strict, "escat": _bm_match_escat, "liberal": _bm_match_liberal}


DRUG_CLASS_EQUIVALENCE = {
    # mBC classes (from v2)
    "CDK4/6i + AI": {"CDK4/6i + AI"},
    "CDK4/6i + fulvestrant": {"CDK4/6i + fulvestrant"},
    "CDK4/6i + endocrine (pre-menopausal)": {"CDK4/6i + endocrine (pre-menopausal)"},
    "CDK4/6i + fulvestrant (post-CDK4/6i)": {"CDK4/6i + fulvestrant (post-CDK4/6i)"},
    "PI3Ki + fulvestrant": {"PI3Ki + fulvestrant"},
    "PI3Ki triplet (inavolisib + CDK4/6i + fulv)": {"PI3Ki triplet (inavolisib + CDK4/6i + fulv)"},
    "AKTi + fulvestrant": {"AKTi + fulvestrant"},
    "AKTi + chemotherapy": {"AKTi + chemotherapy"},
    "SERD oral": {"SERD oral"},
    "SERD oral + CDK4/6i": {"SERD oral + CDK4/6i"},
    "HER2-ADC (T-DXd)": {"HER2-ADC (T-DXd)"},
    "HER2-ADC (other)": {"HER2-ADC (other)", "HER2-ADC (T-DXd)"},
    "TROP2-ADC (sacituzumab govitecan)": {"TROP2-ADC (sacituzumab govitecan)"},
    "TROP2-ADC (datopotamab deruxtecan)": {"TROP2-ADC (datopotamab deruxtecan)"},
    "PARPi (olaparib)": {"PARPi (olaparib)", "PARPi (talazoparib)"},
    "PARPi (talazoparib)": {"PARPi (olaparib)", "PARPi (talazoparib)"},
    "everolimus + exemestane": {"everolimus + exemestane"},
    "chemotherapy": {"chemotherapy", "chemotherapy single agent"},
    "chemotherapy single agent": {"chemotherapy", "chemotherapy single agent"},
    "endocrine therapy alone": {"endocrine therapy alone"},
    # NSCLC classes
    "EGFR TKI 1st-gen (gefitinib/erlotinib)": {"EGFR TKI 1st-gen (gefitinib/erlotinib)"},
    "EGFR TKI 2nd-gen (afatinib/dacomitinib)": {"EGFR TKI 2nd-gen (afatinib/dacomitinib)"},
    "EGFR TKI 3rd-gen (osimertinib)": {"EGFR TKI 3rd-gen (osimertinib)"},
    "EGFR TKI 3rd-gen + chemotherapy": {"EGFR TKI 3rd-gen + chemotherapy"},
    "EGFR TKI 3rd-gen + bispecific (amivantamab + lazertinib)": {"EGFR TKI 3rd-gen + bispecific (amivantamab + lazertinib)"},
    "Amivantamab + chemotherapy": {"Amivantamab + chemotherapy"},
    "HER3-ADC (patritumab deruxtecan)": {"HER3-ADC (patritumab deruxtecan)"},
    "ALK TKI 1st-gen (crizotinib)": {"ALK TKI 1st-gen (crizotinib)"},
    "ALK TKI 2nd-gen (alectinib/brigatinib/ceritinib/ensartinib)": {"ALK TKI 2nd-gen (alectinib/brigatinib/ceritinib/ensartinib)"},
    "ALK TKI 3rd-gen (lorlatinib)": {"ALK TKI 3rd-gen (lorlatinib)"},
    "Platinum doublet chemotherapy": {"Platinum doublet chemotherapy"},
    "Platinum doublet + PD-1/PD-L1": {"Platinum doublet + PD-1/PD-L1"},
    "PD-1/PD-L1 monotherapy": {"PD-1/PD-L1 monotherapy"},
    "PD-1/PD-L1 + CTLA-4": {"PD-1/PD-L1 + CTLA-4"},
    "Anti-VEGF + chemotherapy": {"Anti-VEGF + chemotherapy"},
    "Bevacizumab + chemotherapy": {"Bevacizumab + chemotherapy"},
    "Ramucirumab + EGFR TKI": {"Ramucirumab + EGFR TKI"},
    "Bevacizumab + EGFR TKI": {"Bevacizumab + EGFR TKI"},
    # v3 R1 fix: add NSCLC drug classes flagged by clinical reviewer as
    # missing (SAVANNAH MET+osi, EGFR ex20ins TKIs, etc.)
    "MET-TKI + osimertinib": {"MET-TKI + osimertinib", "investigational (other)"},
    "EGFR TKI mutant-selective (ex20ins)": {"EGFR TKI mutant-selective (ex20ins)",
                                              "EGFR TKI 3rd-gen (osimertinib)",
                                              "investigational (other)"},
    "investigational (other)": {"investigational (other)"},
}


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
    return (len(ef)/len(gls) if gls else 0.0), len(ef), len(gls), ef, per


def exact_binomial_p(k, n, p0=0.25):
    return sum(comb(n, x) * (p0**x) * ((1-p0)**(n-x)) for x in range(k, n+1))


def clopper_pearson(k, n, alpha=0.05):
    from scipy.stats import beta
    lo = 0.0 if k == 0 else float(beta.ppf(alpha/2, k, n-k+1))
    hi = 1.0 if k == n else float(beta.ppf(1-alpha/2, k+1, n-k))
    return lo, hi


def bootstrap_ci_efdpr(edges, gls, tol, n_iter=1000, seed=20260516):
    """Percentile bootstrap CI by guideline-node resampling.
    v3 R1 fix: was promised in prereg-v3 but never computed."""
    rng = random.Random(seed)
    est = []
    for _ in range(n_iter):
        sample = [rng.choice(gls) for _ in range(len(gls))]
        p, *_ = efdpr(edges, sample, tol)
        est.append(p)
    est.sort()
    lo = est[max(0, int(0.025 * n_iter) - 1)]
    hi = est[min(n_iter - 1, int(0.975 * n_iter))]
    return lo, hi


def run_subset(edges, gls, label):
    out = {"label": label, "n_nodes": len(gls)}
    for tol in ("strict", "escat", "liberal"):
        p, k, n, ef, per = efdpr(edges, gls, tol)
        cp_lo, cp_hi = clopper_pearson(k, n)
        boot_lo, boot_hi = bootstrap_ci_efdpr(edges, gls, tol)
        pval = exact_binomial_p(k, n)
        out[tol] = {
            "point_estimate": round(p, 4),
            "evidence_free_count": k,
            "total_nodes": n,
            "clopper_pearson_ci95": [round(cp_lo, 4), round(cp_hi, 4)],
            "bootstrap_ci95":       [round(boot_lo, 4), round(boot_hi, 4)],
            "exact_p_one_sided_vs_p25": round(pval, 4),
            "rejects": bool(pval < 0.05),
            "evidence_free_nodes": ef,
            "per_node_support": per,
        }
        print(f"    {tol:<8s} EFDPR={p:.3f}  CP-CI=[{cp_lo:.3f},{cp_hi:.3f}]  Boot-CI=[{boot_lo:.3f},{boot_hi:.3f}]  P={pval:.4f}  {'REJECT' if pval<0.05 else 'fails'}")
    return out


def main() -> None:
    edges = json.loads(EDGES.read_text())
    mbc_gls = json.loads(MBC_GL.read_text())
    nsclc_gls = json.loads(NSCLC_GL.read_text())
    pooled_gls = mbc_gls + nsclc_gls
    print(f"Total edges: {len(edges)} ({sum(1 for e in edges if e['tumor']=='mBC')} mBC + {sum(1 for e in edges if e['tumor']=='NSCLC')} NSCLC)")
    print(f"Total pooled nodes: {len(pooled_gls)} ({len(mbc_gls)} mBC + {len(nsclc_gls)} NSCLC)")
    print()
    print("== PRIMARY: pooled mBC + NSCLC ==")
    primary = run_subset(edges, pooled_gls, "primary_pooled")
    print(f"\n== Sensitivity 1: mBC-only ==")
    s_mbc = run_subset(edges, mbc_gls, "mbc_only")
    print(f"\n== Sensitivity 2: NSCLC-only ==")
    s_nsclc = run_subset(edges, nsclc_gls, "nsclc_only")
    # NSCLC sub-stratification (EGFR vs ALK)
    egfr_gls = [g for g in nsclc_gls if "EGFR" in g["biomarker"]]
    alk_gls  = [g for g in nsclc_gls if "ALK" in g["biomarker"]]
    print(f"\n== Sensitivity 3: NSCLC EGFR-only ==")
    s_egfr = run_subset(edges, egfr_gls, "nsclc_egfr_only")
    print(f"\n== Sensitivity 4: NSCLC ALK-only ==")
    s_alk = run_subset(edges, alk_gls, "nsclc_alk_only")
    OUT.write_text(json.dumps({
        "primary": primary,
        "mbc_only": s_mbc,
        "nsclc_only": s_nsclc,
        "nsclc_egfr_only": s_egfr,
        "nsclc_alk_only": s_alk,
    }, indent=2))
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
