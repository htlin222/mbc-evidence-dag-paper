"""v3_05_merge_and_kappa_nsclc.py
Merge 4 Claude NSCLC batches + Codex validation, compute per-field Cohen's κ.
Also injects hand-curated records for 3 round-1-corrected supplementary trials
(AURA3, HERTHENA-Lung01, TROPION-Lung01) whose NCTs were misidentified in the
prereg-v3 round-0 supplementary list and were corrected in commit `<TBD>`.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"
RESULTS = ROOT / "data" / "results"
RESULTS.mkdir(parents=True, exist_ok=True)


HAND_CURATED_SUPPLEMENTARIES = [
    {
        "nct_id": "NCT02151981",
        "trial_name": "AURA3",
        "prior_state": {"post_egfr_tki": True, "post_osimertinib": False,
                        "post_chemo_metastatic_min": 0, "post_alk_tki": None,
                        "post_immunotherapy": None, "menopausal_status": None,
                        "post_endo": None, "post_cdk46i": None},
        "excluded": {"post_egfr_tki": None, "post_osimertinib": True,
                     "post_alk_tki": None, "post_chemo_metastatic_any": True,
                     "post_immunotherapy": None},
        "biomarker": {"hr_pos": False, "her2_neg": None, "her2_low": None,
                      "pik3ca_mut": None, "esr1_mut": None, "akt_path": None,
                      "brca_germline": None,
                      "egfr_mut": True, "egfr_t790m": True,
                      "egfr_ex19del": None, "egfr_l858r": None, "egfr_ex20ins": False,
                      "egfr_other_mut": None,
                      "alk_rearranged": False, "alk_resistance_mut": None,
                      "tumor_type": "NSCLC-EGFR"},
        "subgroup_readouts": [],
        "drug_class": "EGFR TKI 3rd-gen (osimertinib)",
        "year_pc": 2017,
        "guideline_target_node": "post-EGFRTKI|EGFR-T790M|NSCLC",
        "confidence": "high",
        "notes": "v3 round-1 corrected: original supplementary NCT02788279 was IMblaze370 (colorectal); real AURA3 is NCT02151981.",
        "provenance": "nsclc_v3_round1_corrected",
    },
    {
        "nct_id": "NCT04619004",
        "trial_name": "HERTHENA-Lung01",
        "prior_state": {"post_egfr_tki": True, "post_osimertinib": True,
                        "post_chemo_metastatic_min": 0, "post_alk_tki": None,
                        "post_immunotherapy": None, "menopausal_status": None,
                        "post_endo": None, "post_cdk46i": None},
        "excluded": {"post_egfr_tki": None, "post_osimertinib": None,
                     "post_alk_tki": None, "post_chemo_metastatic_any": False,
                     "post_immunotherapy": None},
        "biomarker": {"hr_pos": False, "her2_neg": None, "her2_low": None,
                      "pik3ca_mut": None, "esr1_mut": None, "akt_path": None,
                      "brca_germline": None,
                      "egfr_mut": True, "egfr_t790m": None,
                      "egfr_ex19del": None, "egfr_l858r": None, "egfr_ex20ins": False,
                      "egfr_other_mut": None,
                      "alk_rearranged": False, "alk_resistance_mut": None,
                      "tumor_type": "NSCLC-EGFR"},
        "subgroup_readouts": [],
        "drug_class": "HER3-ADC (patritumab deruxtecan)",
        "year_pc": 2023,
        "guideline_target_node": "post-osimertinib|EGFR-mut|NSCLC",
        "confidence": "high",
        "notes": "v3 round-1 corrected: original supplementary NCT05009836 was savolitinib+osimertinib MET trial; real HERTHENA-Lung01 is NCT04619004.",
        "provenance": "nsclc_v3_round1_corrected",
    },
    {
        "nct_id": "NCT04656652",
        "trial_name": "TROPION-Lung01",
        "prior_state": {"post_egfr_tki": None, "post_osimertinib": None,
                        "post_chemo_metastatic_min": 1, "post_alk_tki": None,
                        "post_immunotherapy": None, "menopausal_status": None,
                        "post_endo": None, "post_cdk46i": None},
        "excluded": {"post_egfr_tki": None, "post_osimertinib": None,
                     "post_alk_tki": None, "post_chemo_metastatic_any": False,
                     "post_immunotherapy": None},
        "biomarker": {"hr_pos": False, "her2_neg": None, "her2_low": None,
                      "pik3ca_mut": None, "esr1_mut": None, "akt_path": None,
                      "brca_germline": None,
                      "egfr_mut": None, "egfr_t790m": None,
                      "egfr_ex19del": None, "egfr_l858r": None, "egfr_ex20ins": None,
                      "egfr_other_mut": None,
                      "alk_rearranged": None, "alk_resistance_mut": None,
                      "tumor_type": "NSCLC-other"},
        "subgroup_readouts": ["actionable_genomic_alteration_subgroup", "non-actionable_subgroup"],
        "drug_class": "TROP2-ADC (datopotamab deruxtecan)",
        "year_pc": 2023,
        "guideline_target_node": "post-chemo|any-biomarker|NSCLC",
        "confidence": "medium",
        "notes": "v3 round-1 corrected: original supplementary NCT04644237 was DESTINY-Lung02 HER2-mutated; real TROPION-Lung01 is NCT04656652. Trial enrolled mixed biomarker NSCLC; partially in scope (EGFR-mut and AGA subgroups).",
        "provenance": "nsclc_v3_round1_corrected",
    },
]


def cohen_kappa(a, b):
    a = [str(x) for x in a]; b = [str(x) for x in b]
    n = len(a)
    if n == 0: return float("nan"), 0
    n_agree = sum(1 for x, y in zip(a, b) if x == y)
    obs = n_agree / n
    labels = set(a) | set(b)
    pa = {l: a.count(l)/n for l in labels}
    pb = {l: b.count(l)/n for l in labels}
    exp = sum(pa[l]*pb[l] for l in labels)
    if exp == 1.0:
        return (1.0 if obs == 1.0 else 0.0), n
    return (obs - exp) / (1.0 - exp), n


def main() -> None:
    claude_all = []
    for batch in ("A", "B", "C", "D"):
        d = json.loads((PROC / f"v3_nsclc_extraction_batch{batch}.json").read_text())
        claude_all.extend(d)
    # Drop misidentified NCTs (those in WRONG_TO_RIGHT)
    DROP = {"NCT02788279", "NCT05009836", "NCT04644237", "NCT04379635"}
    claude_all = [r for r in claude_all if r["nct_id"] not in DROP]
    # Append hand-curated round-1 corrections
    claude_all.extend(HAND_CURATED_SUPPLEMENTARIES)
    # Dedup by NCT (latest wins)
    seen = {}
    for r in claude_all:
        seen[r["nct_id"]] = r
    merged = sorted(seen.values(), key=lambda r: r["nct_id"])
    (PROC / "v3_nsclc_full.json").write_text(json.dumps(merged, indent=2))
    print(f"Merged Claude extraction (post round-1 fixes): {len(merged)} records")

    # Compute Cohen κ vs Codex validation
    codex = json.loads((PROC / "v3_nsclc_extraction_codex.json").read_text())
    codex_by_nct = {r["nct_id"]: r for r in codex}
    claude_by_nct = {r["nct_id"]: r for r in merged}
    val_subset = json.loads((PROC / "v3_nsclc_validation_subset.json").read_text())["validation_ncts"]
    val_ncts = [n for n in val_subset if n in claude_by_nct and n in codex_by_nct]
    print(f"Validation overlap: {len(val_ncts)} NCTs (out of {len(val_subset)} prereg-specified)")

    FIELDS = [
        "prior_state.post_egfr_tki",
        "prior_state.post_osimertinib",
        "prior_state.post_alk_tki",
        "biomarker.egfr_mut",
        "biomarker.egfr_t790m",
        "biomarker.alk_rearranged",
        "biomarker.tumor_type",
        "drug_class",
    ]
    def get_nested(d, path):
        for p in path.split("."):
            if d is None: return None
            d = d.get(p) if isinstance(d, dict) else None
        return d

    out = {"per_field": {}, "n_validation": len(val_ncts)}
    print(f"\n{'Field':<32s} {'κ':>8s} {'PABAK':>8s} {'agree%':>8s}")
    for f in FIELDS:
        a = [get_nested(claude_by_nct[n], f) for n in val_ncts]
        b = [get_nested(codex_by_nct[n], f)  for n in val_ncts]
        k, n = cohen_kappa(a, b)
        agree = sum(1 for x, y in zip(a, b) if str(x) == str(y)) / n if n else 0
        pabak = 2 * agree - 1
        out["per_field"][f] = {"kappa": round(k, 4), "pabak": round(pabak, 4),
                                "agreement_pct": round(agree, 4), "n_pairs": n}
        print(f"  {f:<32s} {k:8.3f} {pabak:8.3f} {agree*100:7.1f}%")
    kappas = [v["kappa"] for v in out["per_field"].values()]
    pabaks = [v["pabak"] for v in out["per_field"].values()]
    out["mean_kappa"] = round(sum(kappas)/len(kappas), 4)
    out["mean_pabak"] = round(sum(pabaks)/len(pabaks), 4)
    out["passes_gate_07_cohen"] = bool(all(k >= 0.70 for k in kappas))
    out["passes_gate_07_pabak"] = bool(all(p >= 0.70 for p in pabaks))
    print(f"\nMean Cohen κ: {out['mean_kappa']}")
    print(f"Mean PABAK:    {out['mean_pabak']}")
    print(f"Gate κ>=0.70 (Cohen): {'PASS' if out['passes_gate_07_cohen'] else 'FAIL'}")
    print(f"Gate κ>=0.70 (PABAK): {'PASS' if out['passes_gate_07_pabak'] else 'FAIL'}")
    (RESULTS / "v3_nsclc_kappa.json").write_text(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
