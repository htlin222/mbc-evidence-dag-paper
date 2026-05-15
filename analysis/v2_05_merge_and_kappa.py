"""v2_05_merge_and_kappa.py
Merge 4 Claude extraction batches; compute per-field Cohen's κ between Claude
and Codex on the 20-trial validation subset.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"
RESULTS = ROOT / "data" / "results"
RESULTS.mkdir(parents=True, exist_ok=True)


def cohen_kappa(a_vals: list, b_vals: list) -> tuple[float, int]:
    """Compute Cohen's kappa for paired categorical labels. None == None counts
    as agreement; None vs non-None counts as disagreement.
    Returns (kappa, n_pairs)."""
    assert len(a_vals) == len(b_vals)
    n = len(a_vals)
    if n == 0:
        return float("nan"), 0
    # use simple categorical labels (cast booleans / nulls to strings)
    a = [str(x) for x in a_vals]
    b = [str(x) for x in b_vals]
    n_agree = sum(1 for x, y in zip(a, b) if x == y)
    obs = n_agree / n
    # marginal prob per label
    labels = set(a) | set(b)
    pa = {l: a.count(l) / n for l in labels}
    pb = {l: b.count(l) / n for l in labels}
    exp = sum(pa[l] * pb[l] for l in labels)
    if exp == 1.0:
        return 1.0 if obs == 1.0 else 0.0, n
    return (obs - exp) / (1.0 - exp), n


def main() -> None:
    claude_all = []
    for batch in ("A", "B", "C", "D"):
        d = json.loads((PROC / f"v2_extraction_claude_batch{batch}.json").read_text())
        claude_all.extend(d)
    # dedupe by NCT, keep first
    seen, merged = set(), []
    for r in claude_all:
        if r["nct_id"] in seen: continue
        seen.add(r["nct_id"]); merged.append(r)
    merged.sort(key=lambda r: r["nct_id"])
    (PROC / "v2_claude_full.json").write_text(json.dumps(merged, indent=2))
    print(f"merged Claude extractions: {len(merged)}")

    # Build per-NCT lookup
    claude_by_nct = {r["nct_id"]: r for r in merged}
    codex = json.loads((PROC / "v2_extraction_codex.json").read_text())
    codex_by_nct = {r["nct_id"]: r for r in codex}
    val_ncts = sorted(set(claude_by_nct) & set(codex_by_nct))
    print(f"validation NCT overlap: {len(val_ncts)}")

    # Per-field kappa on validation subset
    FIELDS = [
        ("prior_state.post_endo",          lambda r: r.get("prior_state",{}).get("post_endo")),
        ("prior_state.post_cdk46i",        lambda r: r.get("prior_state",{}).get("post_cdk46i")),
        ("prior_state.menopausal_status",  lambda r: r.get("prior_state",{}).get("menopausal_status")),
        ("biomarker.hr_pos",               lambda r: r.get("biomarker",{}).get("hr_pos")),
        ("biomarker.her2_neg",             lambda r: r.get("biomarker",{}).get("her2_neg")),
        ("biomarker.her2_low",             lambda r: r.get("biomarker",{}).get("her2_low")),
        ("biomarker.pik3ca_mut",           lambda r: r.get("biomarker",{}).get("pik3ca_mut")),
        ("biomarker.esr1_mut",             lambda r: r.get("biomarker",{}).get("esr1_mut")),
        ("biomarker.akt_path",             lambda r: r.get("biomarker",{}).get("akt_path")),
        ("biomarker.brca_germline",        lambda r: r.get("biomarker",{}).get("brca_germline")),
        ("drug_class",                     lambda r: r.get("drug_class")),
        ("excluded.post_cdk46i",           lambda r: r.get("excluded",{}).get("post_cdk46i")),
    ]
    KEY_FIELDS = {"prior_state.post_endo", "prior_state.post_cdk46i",
                  "biomarker.hr_pos", "biomarker.her2_neg",
                  "biomarker.pik3ca_mut", "biomarker.esr1_mut",
                  "biomarker.akt_path", "biomarker.her2_low"}
    out = {"per_field": {}, "n_validation": len(val_ncts)}
    print(f"\n{'Field':<32s} {'κ':>8s} {'agreement%':>11s} {'n':>4s}")
    for name, getter in FIELDS:
        a = [getter(claude_by_nct[n]) for n in val_ncts]
        b = [getter(codex_by_nct[n])  for n in val_ncts]
        k, n = cohen_kappa(a, b)
        agree = sum(1 for x, y in zip(a, b) if str(x) == str(y)) / n
        out["per_field"][name] = {"kappa": round(k, 4), "agreement_pct": round(agree, 4),
                                   "n_pairs": n, "is_key_field": name in KEY_FIELDS}
        flag = "★" if name in KEY_FIELDS else " "
        print(f"  {flag}{name:<32s} {k:8.3f} {agree*100:10.1f}% {n:4d}")
    # Summary gates
    key_kappas = [v["kappa"] for k, v in out["per_field"].items() if v["is_key_field"]]
    key_kappas_valid = [k for k in key_kappas if not (k != k)]  # filter NaN
    out["mean_key_field_kappa"] = round(sum(key_kappas_valid) / len(key_kappas_valid), 4) if key_kappas_valid else None
    out["min_key_field_kappa"]  = round(min(key_kappas_valid), 4) if key_kappas_valid else None
    out["passes_kappa_gate_07"] = bool(all(k >= 0.70 for k in key_kappas_valid))
    print(f"\nMean κ (key fields): {out['mean_key_field_kappa']}")
    print(f"Min  κ (key fields): {out['min_key_field_kappa']}")
    print(f"Pre-registered κ >= 0.70 gate (all key fields): {'PASS' if out['passes_kappa_gate_07'] else 'FAIL'}")
    (RESULTS / "v2_kappa.json").write_text(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
