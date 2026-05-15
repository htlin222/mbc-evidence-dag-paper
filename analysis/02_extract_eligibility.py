"""02_extract_eligibility.py
Structure each pivotal trial's eligibility into the frozen v1.0 schema.

For this pilot, eligibility coding is performed by hand-curated assignment
based on the canonical published primary-publication of each trial. The
mapping below is auditable and the source files (raw ClinicalTrials.gov
JSON + cited primary publication) are kept in data/raw. A future production
version will replace this hand-curated mapping with the LLM-extraction
pipeline plus a hold-out validation set; for the present manuscript the
hand-curated mapping IS the data, and is published as Supplementary
Table S2.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "ctgov_trials.json"
OUT = ROOT / "data" / "processed" / "trials_structured.json"
OUT.parent.mkdir(parents=True, exist_ok=True)

# Schema v1.0 fields (frozen). For each trial:
#   prior_state: which lines/classes are required to have been received
#   excluded:    which lines/classes are excluded (must NOT have been received)
#   biomarker:   inclusion biomarker requirements (boolean flags)
#   drug_class:  primary investigational arm drug class
#   year_pc:     primary-completion year (used for temporal-precedence checks)
#   guideline_target_node: the canonical (state, biomarker) node this trial is
#                          designed to support (analyst-coded)

STRUCTURED: dict[str, dict] = {
    "NCT01942135": {  # PALOMA-3
        "trial_name": "PALOMA-3",
        "prior_state": {"post_endo": True, "post_cdk46i": False, "post_chemo_metastatic_min": 0},
        "excluded":    {"post_cdk46i": True},
        "biomarker":   {"hr_pos": True, "her2_neg": True, "pik3ca_mut": None, "esr1_mut": None, "her2_low": None},
        "drug_class":  "CDK4/6i + fulvestrant",
        "year_pc":     2015,
        "guideline_target_node": "post-endo|HR+/HER2-",
    },
    "NCT02107703": {  # MONARCH-2
        "trial_name": "MONARCH-2",
        "prior_state": {"post_endo": True, "post_cdk46i": False},
        "excluded":    {"post_cdk46i": True, "post_chemo_metastatic_any": True},
        "biomarker":   {"hr_pos": True, "her2_neg": True},
        "drug_class":  "CDK4/6i + fulvestrant",
        "year_pc":     2017,
        "guideline_target_node": "post-endo|HR+/HER2-",
    },
    "NCT02437318": {  # SOLAR-1
        "trial_name": "SOLAR-1",
        "prior_state": {"post_endo": True, "post_cdk46i": False},
        "excluded":    {"post_chemo_metastatic_any": True},
        "biomarker":   {"hr_pos": True, "her2_neg": True, "pik3ca_mut": True},
        "drug_class":  "PI3Ki + fulvestrant",
        "year_pc":     2018,
        "guideline_target_node": "post-endo|PIK3CAmut|HR+/HER2-",
    },
    "NCT03778931": {  # EMERALD
        "trial_name": "EMERALD",
        "prior_state": {"post_endo": True, "post_cdk46i": True},
        "excluded":    {},
        "biomarker":   {"hr_pos": True, "her2_neg": True},  # all-comers
        "subgroup_readouts": ["ESR1mut"],  # registrational ESR1mut subgroup
        "drug_class":  "SERD oral",
        "year_pc":     2021,
        "guideline_target_node": "post-CDK46i|ESR1mut|HR+/HER2-",
    },
    "NCT04305496": {  # CAPItello-291
        "trial_name": "CAPItello-291",
        "prior_state": {"post_endo": True, "post_cdk46i": False},  # all-comers, CDK4/6i not required
        "excluded":    {},
        "biomarker":   {"hr_pos": True, "her2_neg": True},  # all-comers
        "subgroup_readouts": ["AKTpath"],  # registrational AKT-pathway subgroup
        "drug_class":  "AKTi + fulvestrant",
        "year_pc":     2022,
        "guideline_target_node": "post-CDK46i|AKTpath|HR+/HER2-",
    },
    "NCT04494425": {  # DESTINY-Breast06
        "trial_name": "DESTINY-Breast06",
        "prior_state": {"post_endo": True, "post_cdk46i": True, "post_chemo_metastatic_min": 0},
        "excluded":    {"post_chemo_metastatic_any": True},
        "biomarker":   {"hr_pos": True, "her2_neg": True, "her2_low": True},
        "drug_class":  "HER2-ADC (T-DXd)",
        "year_pc":     2024,
        "guideline_target_node": "post-CDK46i|HER2-low|HR+/HER2-",
    },
    "NCT01958021": {  # MONALEESA-2
        "trial_name": "MONALEESA-2",
        "prior_state": {"post_endo": False},
        "excluded":    {"post_endo_metastatic_any": True, "post_chemo_metastatic_any": True},
        "biomarker":   {"hr_pos": True, "her2_neg": True},
        "drug_class":  "CDK4/6i + AI",
        "year_pc":     2016,
        "guideline_target_node": "first-line|HR+/HER2-",
    },
    "NCT02246621": {  # MONALEESA-3
        "trial_name": "MONALEESA-3",
        "prior_state": {"post_endo": None, "post_cdk46i": False},  # mixed: 1L and 2L
        "excluded":    {"post_cdk46i": True},
        "biomarker":   {"hr_pos": True, "her2_neg": True},
        "drug_class":  "CDK4/6i + fulvestrant",
        "year_pc":     2018,
        "guideline_target_node": "post-endo|HR+/HER2-",
    },
    "NCT02513394": {  # PALOMA-2
        "trial_name": "PALOMA-2",
        "prior_state": {"post_endo": False},
        "excluded":    {"post_endo_metastatic_any": True},
        "biomarker":   {"hr_pos": True, "her2_neg": True},
        "drug_class":  "CDK4/6i + AI",
        "year_pc":     2016,
        "guideline_target_node": "first-line|HR+/HER2-",
    },
    "NCT02675231": {  # MONARCH-3
        "trial_name": "MONARCH-3",
        "prior_state": {"post_endo": False},
        "excluded":    {"post_endo_metastatic_any": True},
        "biomarker":   {"hr_pos": True, "her2_neg": True},
        "drug_class":  "CDK4/6i + AI",
        "year_pc":     2017,
        "guideline_target_node": "first-line|HR+/HER2-",
    },
    "NCT02763566": {  # MONALEESA-7
        "trial_name": "MONALEESA-7",
        "prior_state": {"post_endo": False, "menopausal_status": "pre"},
        "excluded":    {"post_endo_metastatic_any": True},
        "biomarker":   {"hr_pos": True, "her2_neg": True},
        "drug_class":  "CDK4/6i + endocrine (pre-menopausal)",
        "year_pc":     2018,
        "guideline_target_node": "first-line|pre-menopausal|HR+/HER2-",
    },
    "NCT03734029": {  # DESTINY-Breast04
        "trial_name": "DESTINY-Breast04",
        "prior_state": {"post_chemo_metastatic_min": 1},
        "excluded":    {},
        "biomarker":   {"hr_pos": True, "her2_neg": True, "her2_low": True},  # HR+ subgroup
        "subgroup_readouts": ["HR+_subgroup"],
        "drug_class":  "HER2-ADC (T-DXd)",
        "year_pc":     2022,
        "guideline_target_node": "post-chemo|HER2-low|HR+/HER2-",
    },
    "NCT03997123": {  # postMONARCH
        "trial_name": "postMONARCH",
        "prior_state": {"post_endo": True, "post_cdk46i": True},
        "excluded":    {"post_chemo_metastatic_any": True},
        "biomarker":   {"hr_pos": True, "her2_neg": True},
        "drug_class":  "CDK4/6i + fulvestrant (post-CDK4/6i)",
        "year_pc":     2024,
        "guideline_target_node": "post-CDK46i|HR+/HER2-",
    },
    "NCT04032080": {  # INAVO120
        "trial_name": "INAVO120",
        "prior_state": {"post_endo": True, "post_cdk46i": None, "endo_resistance_window_months": 12},
        "excluded":    {"post_cdk46i_metastatic": True},
        "biomarker":   {"hr_pos": True, "her2_neg": True, "pik3ca_mut": True},
        "drug_class":  "PI3Ki + CDK4/6i + fulvestrant",
        "year_pc":     2023,
        "guideline_target_node": "post-endo|PIK3CAmut|HR+/HER2-",
    },
}


def _augment_with_ctgov(structured: dict, raw: dict) -> dict:
    """Augment each trial record with key fields from the raw API payload."""
    for nct, rec in structured.items():
        payload = raw.get(nct, {})
        proto = payload.get("protocolSection", {}) if isinstance(payload, dict) else {}
        ident = proto.get("identificationModule", {})
        status = proto.get("statusModule", {})
        rec["nct_id"] = nct
        rec["brief_title"] = ident.get("briefTitle")
        rec["start_year"] = (status.get("startDateStruct", {}) or {}).get("date", "")[:4]
        rec["primary_completion_year_api"] = (
            (status.get("primaryCompletionDateStruct", {}) or {}).get("date", "")[:4]
        )
        elig = proto.get("eligibilityModule", {})
        rec["eligibility_text_len"] = len((elig.get("eligibilityCriteria") or ""))
    return structured


def main() -> None:
    raw = json.loads(RAW.read_text())
    out = _augment_with_ctgov(STRUCTURED, raw)
    OUT.write_text(json.dumps(out, indent=2))
    print(f"wrote {len(out)} structured trial records to {OUT}")


if __name__ == "__main__":
    main()
