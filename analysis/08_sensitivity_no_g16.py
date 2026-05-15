"""08_sensitivity_no_g16.py
Sensitivity analysis: re-compute EFDPR after excluding G16 (gBRCAm node), which
is a pre-registration scope deviation (OlympiAD enrolled regardless of HR status,
while the prereg restricted to HR+/HER2-). G16 is held as a disclosed deviation
in the supplement; the primary analysis is the 16-node ESMO HR+/HER2- subset,
while this sensitivity confirms the result is robust to G16 removal.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

from importlib import util
spec = util.spec_from_file_location("efdpr_mod", ROOT / "analysis" / "05_compute_efdpr.py")
mod = util.module_from_spec(spec); spec.loader.exec_module(mod)

edges = json.loads((ROOT / "data" / "processed" / "dag_edges.json").read_text())
gls   = json.loads((ROOT / "data" / "processed" / "esmo_decision_tree.json").read_text())
gls_15 = [g for g in gls if g["node_id"] != "G16"]

OUT = ROOT / "data" / "results" / "efdpr_sensitivity_no_g16.json"

results = {}
for tol in ("strict", "escat", "liberal"):
    p, k, n, ef, per = mod.efdpr(edges, gls_15, tol)
    lo, hi, _ = mod.bootstrap_efdpr(edges, gls_15, tol)
    cp_lo, cp_hi = mod.clopper_pearson_ci(k, n)
    pval = mod.exact_binomial_pvalue_one_sided(k, n, 0.25)
    results[tol] = {
        "point_estimate": round(p, 4),
        "evidence_free_count": k,
        "total_decision_nodes": n,
        "bootstrap_ci95":   [round(lo, 4), round(hi, 4)],
        "clopper_pearson_ci95": [round(cp_lo, 4), round(cp_hi, 4)],
        "exact_binomial_pvalue_one_sided_vs_p25": round(pval, 4),
        "preregistered_test_rejected_at_alpha_05": bool(pval < 0.05),
    }
    print(f"  {tol:<8s} (n=15)  EFDPR={p:.3f}  CP-CI={cp_lo:.3f}-{cp_hi:.3f}  exact P={pval:.4f}")
OUT.write_text(json.dumps(results, indent=2))
print(f"wrote {OUT}")
