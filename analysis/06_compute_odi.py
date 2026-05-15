"""06_compute_odi.py
Operationalization Discordance Index (ODI) per biomarker variable.

For each biomarker variable b, the ODI is the mean pairwise Jaccard distance
between trial-level inclusion definitions, treating each definition as a set
of operational tokens.

Token assignments below are derived from the canonical primary publication of
each trial; this hand-curated mapping is published as Supplementary Table S4
of the manuscript.
"""
from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "results" / "odi.json"
OUT.parent.mkdir(parents=True, exist_ok=True)

# Biomarker operational tokens per trial.
# Token vocabulary:
#   IHC1+, IHC2+_ISH_negative, central_read, local_read, ISH_threshold_2,
#   tissue_NGS, plasma_ctDNA, single_variant, multi_variant, VAF_threshold_low,
#   exon_9, exon_20, helical_domain, kinase_domain, AKT1_E17K, PTEN_loss,
#   prior_CDK4_6i_required, prior_CDK4_6i_allowed, post_AI_required,
#   post_AI_post_progression, post_endo_2plus_lines.
DEFINITIONS = {
    "HER2-low": {
        "DESTINY-Breast04": {"IHC1+", "IHC2+_ISH_negative", "central_read", "ISH_threshold_2"},
        "DESTINY-Breast06": {"IHC1+", "IHC2+_ISH_negative", "central_read", "ISH_threshold_2", "HER2_ultralow_eligible"},
    },
    "ESR1mut": {
        "EMERALD":         {"tissue_NGS", "plasma_ctDNA", "multi_variant"},
        "CAPItello-291":   {"plasma_ctDNA", "multi_variant"},          # subgroup analysis
    },
    "PIK3CAmut": {
        "SOLAR-1":         {"tissue_NGS", "exon_9", "exon_20", "kinase_domain", "helical_domain"},
        "INAVO120":        {"tissue_NGS", "plasma_ctDNA", "exon_9", "exon_20", "kinase_domain"},
        "CAPItello-291":   {"plasma_ctDNA", "exon_9", "exon_20", "helical_domain", "kinase_domain"},
    },
    "AKTpath": {
        "CAPItello-291":   {"PIK3CAmut", "AKT1_E17K", "PTEN_loss"},
        # SOLAR-1 narrower (PIK3CA only), included only as PIK3CAmut comparator
        "SOLAR-1":         {"PIK3CAmut"},
    },
    "prior_CDK4_6i": {
        "EMERALD":         {"prior_CDK4_6i_required"},
        "CAPItello-291":   {"prior_CDK4_6i_allowed"},
        "PALOMA-3":        {"prior_endo_progression"},   # NO CDK4/6i allowed
        "MONARCH-2":       {"prior_endo_progression"},
        "DESTINY-Breast06": {"prior_endo_required", "no_chemo_metastatic"},
        "postMONARCH":     {"prior_CDK4_6i_required"},
        "INAVO120":        {"endo_resistance_window_12mo"},
    },
}


def _jaccard_distance(a: set, b: set) -> float:
    if not a and not b:
        return 0.0
    return 1.0 - len(a & b) / len(a | b)


def main() -> None:
    out = {}
    for variable, trials_defs in DEFINITIONS.items():
        names = list(trials_defs.keys())
        pairs = list(combinations(names, 2))
        if not pairs:
            odi = 0.0
        else:
            d = [_jaccard_distance(trials_defs[a], trials_defs[b]) for a, b in pairs]
            odi = sum(d) / len(d)
        out[variable] = {
            "trials": names,
            "n_trials": len(names),
            "n_pairs": len(pairs),
            "odi": round(odi, 4),
            "pairwise": [
                {"trial_a": a, "trial_b": b, "jaccard_distance": round(_jaccard_distance(trials_defs[a], trials_defs[b]), 4)}
                for a, b in pairs
            ],
        }
        print(f"  {variable:<20s} ODI = {odi:.3f} ({len(names)} trials)")
    OUT.write_text(json.dumps(out, indent=2))
    print(f"wrote ODI results to {OUT}")


if __name__ == "__main__":
    main()
