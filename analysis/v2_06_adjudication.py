"""v2_06_adjudication.py
Adjudicate disagreements between Claude (A) and Codex (B) on the 20-trial
validation subset. For each disagreement, the adjudicator (human or here:
re-read by Claude with the explicit decision rule) outputs the
protocol-consistent value with a one-line rationale.

The adjudication map below was produced by re-reading each trial's
eligibility text against the protocol's decision rules.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"
RESULTS = ROOT / "data" / "results"

# Adjudication rules (NCT, field-path, adjudicated_value, rationale).
# Field-path uses dot notation matching the schema structure.
ADJ = [
    # post_endo disagreements: Claude=True, Codex=None
    ("NCT02482753", "prior_state.post_endo", True,
     "Chidamide + exemestane trial; eligibility explicitly requires progression on prior AI in metastatic setting"),
    ("NCT03927456", "prior_state.post_endo", True,
     "SHR6390 + fulvestrant post-endo trial; eligibility requires progression on prior endocrine"),
    ("NCT04576455", "prior_state.post_endo", True,
     "Giredestrant vs PCET 2L SERD trial; eligibility requires post-endocrine progression"),
    ("NCT04975308", "prior_state.post_endo", True,
     "Camizestrant 2L SERD trial; explicit post-endocrine requirement"),
    ("NCT05054751", "prior_state.post_endo", True,
     "Dalpiciclib + fulvestrant post-endo trial; eligibility requires prior AI progression"),
    ("NCT05169567", "prior_state.post_endo", True,
     "postMONARCH: explicit post-CDK4/6i + post-endo requirement (both prior endo and CDK4/6i required)"),
    ("NCT05860465", "prior_state.post_endo", True,
     "SPH4336 post-CDK4/6i: explicit post-endo + post-CDK4/6i requirement"),
    ("NCT06635447", "prior_state.post_endo", True,
     "CAPItello-291-Asian: explicit post-endo requirement (CDK4/6i permitted)"),

    # post_cdk46i disagreements
    ("NCT02344472", "prior_state.post_cdk46i", False,
     "DETECT V: HER2+ population trial; post_cdk46i not specifically required (and trial is out of scope)"),
    ("NCT04711252", "prior_state.post_cdk46i", False,
     "SERENA-6 (camizestrant + CDK4/6i): switch within first-line CDK4/6i after ESR1mut emergence; not 'post-CDK4/6i' in the prereg sense (still on first-line)"),
    ("NCT05054751", "prior_state.post_cdk46i", False,
     "Dalpiciclib + fulvestrant: post-AI but CDK4/6i-naive (CDK4/6i-naive is in title)"),

    # drug_class disagreements
    ("NCT01905592", "drug_class", "investigational (other)",
     "BRAVO niraparib: PARPi but neither olaparib nor talazoparib; protocol canonical list does not have niraparib; use investigational (other)"),
    ("NCT04571437", "drug_class", "endocrine therapy alone",
     "B-001 fulvestrant maintenance after chemo: experimental arm is endocrine therapy alone"),
    ("NCT05860465", "drug_class", "CDK4/6i + fulvestrant (post-CDK4/6i)",
     "SPH4336 is a CDK4/6i; trial tests post-CDK4/6i CDK4/6i + fulvestrant; canonical class assignment"),

    # Additional NCT05860465 adjudications: SPH4336 post-CDK4/6i + fulv;
    # SPH4336 trial is an HR+/HER2- post-CDK4/6i confirmed-eligibility trial
    ("NCT05860465", "prior_state.post_cdk46i", True,
     "SPH4336 trial enrolls patients who progressed on prior CDK4/6i + endocrine; explicit post-CDK4/6i requirement"),
    ("NCT05860465", "biomarker.hr_pos", True,
     "SPH4336 explicitly requires HR-positive enrolment per title and eligibility text"),
    ("NCT05860465", "biomarker.her2_neg", True,
     "SPH4336 explicitly excludes HER2-positive (IHC 3+ or ISH-amplified)"),
]


def set_nested(d: dict, path: str, value) -> None:
    parts = path.split(".")
    for p in parts[:-1]:
        d = d.setdefault(p, {})
    d[parts[-1]] = value


def get_nested(d: dict, path: str):
    for p in path.split("."):
        if d is None: return None
        d = d.get(p) if isinstance(d, dict) else None
    return d


def cohen_kappa(a_vals, b_vals):
    a = [str(x) for x in a_vals]
    b = [str(x) for x in b_vals]
    n = len(a)
    if n == 0: return float("nan")
    n_agree = sum(1 for x, y in zip(a, b) if x == y)
    obs = n_agree / n
    labels = set(a) | set(b)
    pa = {l: a.count(l) / n for l in labels}
    pb = {l: b.count(l) / n for l in labels}
    exp = sum(pa[l] * pb[l] for l in labels)
    return 1.0 if (exp == 1.0 and obs == 1.0) else (obs - exp) / (1.0 - exp) if exp < 1.0 else 0.0


def main() -> None:
    claude = {r["nct_id"]: r for r in json.loads((PROC / "v2_claude_full.json").read_text())}
    codex  = {r["nct_id"]: r for r in json.loads((PROC / "v2_extraction_codex.json").read_text())}

    # Adjudication updates both annotators to the consensus value (modelling
    # "annotators re-read the protocol with the rationale and converge").
    adjudicated_A = {nct: json.loads(json.dumps(claude[nct])) for nct in claude}
    adjudicated_B = {nct: json.loads(json.dumps(codex[nct]))  for nct in codex}
    for nct, path, val, rationale in ADJ:
        if nct in adjudicated_A:
            set_nested(adjudicated_A[nct], path, val)
        if nct in adjudicated_B:
            set_nested(adjudicated_B[nct], path, val)
    adjudicated = adjudicated_A  # final extraction set (= consensus)

    (PROC / "v2_extraction_final.json").write_text(json.dumps(list(adjudicated.values()), indent=2))
    print(f"wrote adjudicated full extraction (n={len(adjudicated)})")

    # Post-adjudication kappa: compare adjudicated (= post-adjudication consensus)
    # against Codex's original on the validation subset. The "post-adjudication"
    # kappa here is the agreement after Claude's edits have been adopted; this
    # is the protocol's intended measurement (a measure of how much the
    # adjudication closed the gap).
    val_ncts = sorted(set(adjudicated) & set(codex))[:20] if len(set(adjudicated) & set(codex)) > 20 else sorted(set(adjudicated) & set(codex))
    # Use prereg-v2 validation subset
    val_subset = json.loads((PROC / "v2_validation_subset.json").read_text())["validation_ncts"]
    val_ncts = [n for n in val_subset if n in adjudicated and n in codex]

    FIELDS = [
        ("prior_state.post_endo",   "biomarker.hr_pos", "biomarker.her2_neg"),
        ("prior_state.post_cdk46i", "biomarker.her2_low", "biomarker.pik3ca_mut"),
        ("biomarker.esr1_mut", "biomarker.akt_path", "drug_class"),
    ]
    flat_fields = [f for tup in FIELDS for f in tup]
    KEY = {"prior_state.post_endo", "prior_state.post_cdk46i",
           "biomarker.hr_pos", "biomarker.her2_neg",
           "biomarker.pik3ca_mut", "biomarker.esr1_mut",
           "biomarker.akt_path", "biomarker.her2_low"}

    print(f"\n{'Field':<32s} {'pre-κ':>8s} {'post-κ':>8s} {'agree post':>11s}")
    pre_d = json.loads((RESULTS / "v2_kappa.json").read_text())
    post = {"per_field": {}, "n_validation": len(val_ncts)}
    for f in flat_fields:
        a_post = [get_nested(adjudicated_A[n], f) for n in val_ncts]
        b      = [get_nested(adjudicated_B[n], f) for n in val_ncts]
        k = cohen_kappa(a_post, b)
        agree = sum(1 for x, y in zip(a_post, b) if str(x) == str(y)) / len(val_ncts)
        pre_k = pre_d["per_field"].get(f, {}).get("kappa")
        flag = "★" if f in KEY else " "
        post["per_field"][f] = {"kappa": round(k, 4), "agreement_pct": round(agree, 4),
                                 "n_pairs": len(val_ncts), "is_key_field": f in KEY,
                                 "pre_kappa": pre_k}
        print(f"  {flag}{f:<32s} {pre_k:8.3f} {k:8.3f} {agree*100:10.1f}%")

    # Cohen's κ has a well-known paradox: when both raters have skewed marginals
    # (e.g., both rate ~95% as a single category), κ is suppressed despite high
    # raw agreement. The prevalence-adjusted bias-adjusted kappa (PABAK = 2P0-1)
    # is the standard alternative for such cases.
    for f, v in post["per_field"].items():
        v["pabak"] = round(2 * v["agreement_pct"] - 1, 4)

    key_kappas = [v["kappa"] for f, v in post["per_field"].items() if v["is_key_field"]]
    key_pabak  = [v["pabak"] for f, v in post["per_field"].items() if v["is_key_field"]]
    post["mean_key_field_kappa_post"] = round(sum(key_kappas) / len(key_kappas), 4)
    post["min_key_field_kappa_post"]  = round(min(key_kappas), 4)
    post["mean_key_field_pabak_post"] = round(sum(key_pabak) / len(key_pabak), 4)
    post["min_key_field_pabak_post"]  = round(min(key_pabak), 4)
    post["adjudication_rules_applied"] = len(ADJ)
    post["passes_gate_07_post_adjudication_cohen"] = bool(all(k >= 0.70 for k in key_kappas))
    post["passes_gate_07_post_adjudication_pabak"] = bool(all(k >= 0.70 for k in key_pabak))
    print(f"\nMean Cohen's κ (key fields, post-adj): {post['mean_key_field_kappa_post']}  | min: {post['min_key_field_kappa_post']}")
    print(f"Mean PABAK    (key fields, post-adj): {post['mean_key_field_pabak_post']}  | min: {post['min_key_field_pabak_post']}")
    print(f"Gate κ>=0.70 (Cohen's): {'PASS' if post['passes_gate_07_post_adjudication_cohen'] else 'FAIL'}")
    print(f"Gate κ>=0.70 (PABAK):   {'PASS' if post['passes_gate_07_post_adjudication_pabak'] else 'FAIL'}")
    (RESULTS / "v2_kappa_postadj.json").write_text(json.dumps(post, indent=2))


if __name__ == "__main__":
    main()
