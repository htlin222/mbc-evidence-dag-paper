"""03_encode_guideline.py
Encode the ESMO 2021/2024 HR+/HER2- mBC decision tree as a directed graph
of decision nodes with recommended drug classes and cited pivotal trials.

Source: ESMO Clinical Practice Guideline for metastatic breast cancer
(Gennari et al., Ann Oncol 2021) and the 2024 update incorporating
trastuzumab deruxtecan for HER2-low and capivasertib for AKT-pathway
alterations. The encoding here is a hand-curated structuring of the
HR+/HER2- subset of the decision tree; the JSON file is published
as Supplementary Table S3 of this manuscript.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "processed" / "esmo_decision_tree.json"
OUT.parent.mkdir(parents=True, exist_ok=True)

# Each decision node:
#   node_id:    canonical (state, biomarker) tuple
#   state:      patient sub-state at the decision point
#   biomarker:  required biomarker profile
#   recommended_classes: list of recommended drug classes (with grade)
#   cited_trials: NCT IDs that the guideline cites in support
#   year:       year of decision-tree introduction

DECISION_NODES = [
    {
        "node_id": "G1",
        "state":   "first-line",
        "biomarker": "HR+/HER2-",
        "recommended_classes": [
            {"class": "CDK4/6i + AI", "grade": "I-A"},
        ],
        "cited_trials": ["NCT01958021", "NCT02513394", "NCT02675231", "NCT02763566"],
        "year": 2018,
    },
    {
        "node_id": "G2",
        "state":   "first-line+pre-menopausal",
        "biomarker": "HR+/HER2-",
        "recommended_classes": [
            {"class": "CDK4/6i + endocrine (pre-menopausal)", "grade": "I-A"},
        ],
        "cited_trials": ["NCT02763566"],
        "year": 2019,
    },
    {
        "node_id": "G3",
        "state":   "post-endo",
        "biomarker": "HR+/HER2-",
        "recommended_classes": [
            {"class": "CDK4/6i + fulvestrant", "grade": "I-A"},
        ],
        "cited_trials": ["NCT01942135", "NCT02107703", "NCT02246621"],
        "year": 2016,
    },
    {
        "node_id": "G4",
        "state":   "post-endo",
        "biomarker": "HR+/HER2-/PIK3CAmut",
        "recommended_classes": [
            {"class": "PI3Ki + fulvestrant", "grade": "I-A"},
        ],
        "cited_trials": ["NCT02437318"],
        "year": 2020,
    },
    {
        "node_id": "G5",
        "state":   "post-CDK46i",
        "biomarker": "HR+/HER2-/ESR1mut",
        "recommended_classes": [
            {"class": "SERD oral", "grade": "I-B"},
        ],
        "cited_trials": ["NCT03778931"],
        "year": 2023,
    },
    {
        "node_id": "G6",
        "state":   "post-CDK46i",
        "biomarker": "HR+/HER2-/AKTpath",
        "recommended_classes": [
            {"class": "AKTi + fulvestrant", "grade": "I-B"},
        ],
        "cited_trials": ["NCT04305496"],
        "year": 2024,
    },
    {
        "node_id": "G7",
        "state":   "post-CDK46i",
        "biomarker": "HR+/HER2-/PIK3CAmut",
        "recommended_classes": [
            {"class": "PI3Ki + fulvestrant", "grade": "II-B"},
        ],
        # Guideline cites SOLAR-1 by extrapolation, despite the trial pop being
        # mostly post-AI (not post-CDK4/6i): this is the canonical example of
        # composition across non-overlapping pivotal trials.
        "cited_trials": ["NCT02437318"],
        "year": 2022,
    },
    {
        "node_id": "G8",
        "state":   "post-CDK46i",
        "biomarker": "HR+/HER2-/HER2-low",
        "recommended_classes": [
            {"class": "HER2-ADC (T-DXd)", "grade": "I-A"},
        ],
        "cited_trials": ["NCT04494425", "NCT03734029"],
        "year": 2024,
    },
    {
        "node_id": "G9",
        "state":   "post-CDK46i",
        "biomarker": "HR+/HER2-/no-actionable",
        "recommended_classes": [
            {"class": "everolimus + exemestane", "grade": "II-B"},
            {"class": "chemotherapy", "grade": "II-B"},
        ],
        "cited_trials": [],  # no trial directly tests this post-CDK46i node
        "year": 2022,
    },
    {
        "node_id": "G10",
        "state":   "post-CDK46i",
        "biomarker": "HR+/HER2-",
        "recommended_classes": [
            {"class": "CDK4/6i + fulvestrant (post-CDK4/6i)", "grade": "II-C"},
        ],
        "cited_trials": ["NCT03997123"],
        "year": 2024,
    },
    {
        "node_id": "G11",
        "state":   "post-endo",
        "biomarker": "HR+/HER2-/HER2-low",
        "recommended_classes": [
            {"class": "HER2-ADC (T-DXd)", "grade": "I-A"},
        ],
        "cited_trials": ["NCT04494425"],
        "year": 2024,
    },
    {
        "node_id": "G12",
        "state":   "post-chemo",
        "biomarker": "HR+/HER2-/HER2-low",
        "recommended_classes": [
            {"class": "HER2-ADC (T-DXd)", "grade": "I-A"},
        ],
        "cited_trials": ["NCT03734029"],
        "year": 2022,
    },
    {
        "node_id": "G13",
        "state":   "post-CDK46i+post-endo",
        "biomarker": "HR+/HER2-",
        "recommended_classes": [
            {"class": "everolimus + exemestane", "grade": "II-B"},
        ],
        # BOLERO-2 tested everolimus + exemestane post-AI, NOT post-CDK4/6i;
        # therefore this guideline node is composition-only.
        "cited_trials": [],
        "year": 2018,
    },
    {
        "node_id": "G14",
        "state":   "post-CDK46i+post-chemo",
        "biomarker": "HR+/HER2-",
        "recommended_classes": [
            {"class": "Sacituzumab govitecan", "grade": "I-A"},
        ],
        "cited_trials": ["NCT03901339"],  # TROPiCS-02
        "year": 2023,
    },
    {
        "node_id": "G15",
        "state":   "post-endo",
        "biomarker": "HR+/HER2-/PIK3CAmut",
        "recommended_classes": [
            {"class": "PI3Ki triplet (inavolisib + CDK4/6i + fulv)", "grade": "I-A"},
        ],
        "cited_trials": ["NCT04191499"],  # INAVO120 (corrected)
        "year": 2024,
    },
    {
        "node_id": "G16",
        "state":   "metastatic",  # gBRCAm setting, line-agnostic
        "biomarker": "gBRCAmut/HER2-",
        "recommended_classes": [
            {"class": "PARPi (olaparib)", "grade": "I-A"},
            {"class": "PARPi (talazoparib)", "grade": "I-A"},
        ],
        "cited_trials": ["NCT02000622"],  # OlympiAD; EMBRACA omitted from this pilot
        "year": 2018,
    },
]


def main() -> None:
    OUT.write_text(json.dumps(DECISION_NODES, indent=2))
    print(f"wrote {len(DECISION_NODES)} guideline decision nodes to {OUT}")


if __name__ == "__main__":
    main()
