"""v2_08_extend_guideline.py
Extend the 16-node ESMO HR+/HER2- mBC decision-tree encoding with ASCO and
NCCN nodes that are not duplicates of the ESMO subset. Produces a unified
decision-tree file for the v2 primary analysis (per prereg-v2).

Pre-existing 16 nodes (ESMO, v1.0.0) are imported unchanged; 6 additional
nodes are added from ASCO and NCCN guidelines.

Provenance per node:
  source: "ESMO" | "ASCO" | "NCCN" | "ESMO+ASCO" | "ASCO+NCCN" | ...
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ESMO_SRC = ROOT / "data" / "processed" / "esmo_decision_tree.json"
OUT      = ROOT / "data" / "processed" / "v2_decision_tree.json"

# Tag existing ESMO nodes with source = "ESMO" (or ESMO+ASCO where applicable)
def tag_esmo(node: dict) -> dict:
    n = dict(node)
    n["source"] = "ESMO"
    # G1-G3 and G4 are shared with ASCO; G8-G12 (T-DXd nodes) and G16 are
    # shared across all three; tag accordingly
    if n["node_id"] in ("G1", "G2", "G3", "G4", "G5", "G6"):
        n["source"] = "ESMO+ASCO"
    if n["node_id"] in ("G8", "G11", "G12", "G16"):
        n["source"] = "ESMO+ASCO+NCCN"
    return n


ADDITIONAL_NODES = [
    # G17: visceral crisis / rapid progression -> 1L chemotherapy
    # ASCO 2022 recommendation; not in our existing tree
    {
        "node_id": "G17",
        "state":   "first-line+visceral-crisis",
        "biomarker": "HR+/HER2-",
        "recommended_classes": [
            {"class": "chemotherapy single agent", "grade": "II-B"},
        ],
        "cited_trials": [],
        "year": 2022,
        "source": "ASCO",
    },
    # G18: post-CDK4/6i + post-chemo (no biomarker) -> SG (TROPiCS-02 broader use)
    # Distinct from G14 (HR+/HER2-) which is the same indication; G18 is the
    # NCCN-specific framing where SG is endorsed for HR+/HER2- without HER2-low
    # requirement. We include only if it represents a unique node beyond G14.
    # Skipping — duplicate of G14.

    # G19: post-endo + ESR1-emergence (ctDNA monitoring) -> early SERD switch
    # SERENA-6 / PADA-1 indication; ASCO 2024 update
    {
        "node_id": "G19",
        "state":   "post-endo",
        "biomarker": "HR+/HER2-/ESR1mut",
        "recommended_classes": [
            {"class": "SERD oral + CDK4/6i", "grade": "II-B"},
        ],
        "cited_trials": [],  # SERENA-6 NCT04711252 should support
        "year": 2024,
        "source": "ASCO",
    },
    # G20: HR+/HER2- post-endo -> Sacituzumab govitecan (TROPiCS-02 broader)
    # NCCN 2024 update
    {
        "node_id": "G20",
        "state":   "post-endo+post-CDK46i",
        "biomarker": "HR+/HER2-",
        "recommended_classes": [
            {"class": "TROP2-ADC (sacituzumab govitecan)", "grade": "I-A"},
        ],
        "cited_trials": ["NCT03901339"],  # TROPiCS-02
        "year": 2023,
        "source": "NCCN",
    },
    # G21: HER2-low post-chemo -> datopotamab deruxtecan (TROPION-Breast01)
    # NCCN 2025 update
    {
        "node_id": "G21",
        "state":   "post-chemo",
        "biomarker": "HR+/HER2-/HER2-low",
        "recommended_classes": [
            {"class": "TROP2-ADC (datopotamab deruxtecan)", "grade": "I-A"},
            {"class": "HER2-ADC (T-DXd)", "grade": "I-A"},
        ],
        "cited_trials": ["NCT05104866"],  # TROPION-Breast01
        "year": 2025,
        "source": "NCCN",
    },
    # G22: bone-only indolent HR+/HER2- -> single-agent endocrine (NCCN)
    {
        "node_id": "G22",
        "state":   "first-line+indolent",
        "biomarker": "HR+/HER2-",
        "recommended_classes": [
            {"class": "endocrine therapy alone", "grade": "II-B"},
        ],
        "cited_trials": [],
        "year": 2020,
        "source": "NCCN",
    },
    # G23: TROP2-ADC for HR+/HER2- after multiple lines (ASCO/NCCN)
    {
        "node_id": "G23",
        "state":   "post-endo+post-CDK46i+post-chemo",
        "biomarker": "HR+/HER2-",
        "recommended_classes": [
            {"class": "TROP2-ADC (sacituzumab govitecan)", "grade": "I-A"},
        ],
        "cited_trials": ["NCT03901339"],  # TROPiCS-02
        "year": 2023,
        "source": "ASCO+NCCN",
    },
    # G24: aromatase inhibitor monotherapy 1L (NCCN low-disease-burden option)
    {
        "node_id": "G24",
        "state":   "first-line+indolent+post-menopausal",
        "biomarker": "HR+/HER2-",
        "recommended_classes": [
            {"class": "endocrine therapy alone", "grade": "II-B"},
        ],
        "cited_trials": [],
        "year": 2018,
        "source": "NCCN",
    },
    # G25: post-everolimus salvage (ASCO recognizes this is largely undefined)
    {
        "node_id": "G25",
        "state":   "post-CDK46i+post-endo+post-mTORi",
        "biomarker": "HR+/HER2-",
        "recommended_classes": [
            {"class": "chemotherapy single agent", "grade": "II-C"},
        ],
        "cited_trials": [],
        "year": 2022,
        "source": "ASCO",
    },
    # G26: post-CDK4/6i AKT-pathway re-introduction (ASCO 2024)
    # AKTi-fulvestrant after CDK4/6i (distinct from G6 which is post-endo only)
    {
        "node_id": "G26",
        "state":   "post-CDK46i",
        "biomarker": "HR+/HER2-/AKTpath",
        "recommended_classes": [
            {"class": "AKTi + fulvestrant", "grade": "I-B"},
        ],
        "cited_trials": ["NCT04305496"],  # CAPItello-291
        "year": 2024,
        "source": "ASCO+NCCN",
    },
]


def main() -> None:
    esmo = json.loads(ESMO_SRC.read_text())
    esmo_tagged = [tag_esmo(n) for n in esmo]
    full = esmo_tagged + ADDITIONAL_NODES
    # Dedupe by node_id (keep first)
    seen = set()
    out = []
    for n in full:
        if n["node_id"] in seen: continue
        seen.add(n["node_id"]); out.append(n)
    OUT.write_text(json.dumps(out, indent=2))
    from collections import Counter
    src_counts = Counter(n["source"] for n in out)
    print(f"wrote {len(out)} unified decision nodes")
    print("by source:")
    for s, n in src_counts.most_common():
        print(f"  {s}: {n}")


if __name__ == "__main__":
    main()
