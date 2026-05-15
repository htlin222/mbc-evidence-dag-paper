"""v2_04_prepare_extraction.py
Prepare per-trial extraction inputs (briefTitle, conditions, eligibility text,
interventions, phase, dates) as compact JSONL for LLM annotators. Also
pre-pick a 20-trial validation subset using seed 20260516.
"""
from __future__ import annotations

import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data" / "raw" / "v2_corpus_full.json"
OUT_DIR = ROOT / "data" / "processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)
ALL_OUT = OUT_DIR / "v2_extraction_inputs.jsonl"
VAL_OUT = OUT_DIR / "v2_validation_subset.json"


def extract_fields(payload: dict) -> dict:
    proto = payload.get("protocolSection", {})
    ident = proto.get("identificationModule", {})
    elig = proto.get("eligibilityModule", {}) or {}
    interv = proto.get("armsInterventionsModule", {}) or {}
    design = proto.get("designModule", {}) or {}
    status = proto.get("statusModule", {}) or {}
    cond_mod = proto.get("conditionsModule", {}) or {}
    return {
        "nct_id": ident.get("nctId"),
        "brief_title": ident.get("briefTitle"),
        "official_title": ident.get("officialTitle"),
        "acronym": ident.get("acronym"),
        "conditions": cond_mod.get("conditions", []),
        "phase": design.get("phases", []),
        "enrollment_count": (design.get("enrollmentInfo") or {}).get("count"),
        "start_year": (status.get("startDateStruct") or {}).get("date", "")[:4],
        "primary_completion_year": (status.get("primaryCompletionDateStruct") or {}).get("date", "")[:4],
        "eligibility_text": elig.get("eligibilityCriteria", ""),
        "interventions": [
            {"name": iv.get("name"), "type": iv.get("type"),
             "description": (iv.get("description") or "")[:200]}
            for iv in (interv.get("interventions") or [])
        ],
        "arm_groups": [
            {"label": ag.get("label"), "type": ag.get("type"),
             "interventions": ag.get("interventionNames", [])}
            for ag in (interv.get("armGroups") or [])
        ],
    }


def main() -> None:
    corpus = json.loads(SRC.read_text())
    inputs = []
    for entry in corpus:
        row = extract_fields(entry["payload"])
        row["provenance"] = entry["provenance"]
        row["trial_name_hint"] = entry.get("trial_name_hint")
        inputs.append(row)
    # Sort by NCT for stable ordering
    inputs.sort(key=lambda r: r["nct_id"])
    # Pre-pick validation subset (seed 20260516)
    rng = random.Random(20260516)
    val_ncts = sorted(rng.sample([r["nct_id"] for r in inputs], 20))
    with ALL_OUT.open("w") as f:
        for row in inputs:
            f.write(json.dumps(row) + "\n")
    VAL_OUT.write_text(json.dumps({"validation_ncts": val_ncts}, indent=2))
    print(f"wrote {len(inputs)} extraction inputs to {ALL_OUT}")
    print(f"validation subset (n={len(val_ncts)}): {VAL_OUT}")
    print(f"  validation NCTs: {val_ncts}")


if __name__ == "__main__":
    main()
