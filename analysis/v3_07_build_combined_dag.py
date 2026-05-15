"""v3_07_build_combined_dag.py
Build combined mBC + NSCLC trial-DAG using the shared (state, biomarker)
node space (extended with NSCLC tokens).
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NSCLC_SRC = ROOT / "data" / "processed" / "v3_nsclc_full.json"
MBC_SRC   = ROOT / "data" / "processed" / "v2_extraction_final.json"

NODES_OUT = ROOT / "data" / "processed" / "v3_combined_dag_nodes.json"
EDGES_OUT = ROOT / "data" / "processed" / "v3_combined_dag_edges.json"


def nsclc_state(rec: dict) -> str:
    """Canonical NSCLC state."""
    prior = rec.get("prior_state") or {}
    parts = []
    if prior.get("post_egfr_tki") is True and prior.get("post_osimertinib") is True:
        parts.append("post-osimertinib")
    elif prior.get("post_egfr_tki") is True:
        parts.append("post-EGFRTKI")
    if prior.get("post_alk_tki") is True:
        parts.append("post-ALKTKI")
    if (prior.get("post_chemo_metastatic_min") or 0) >= 1:
        parts.append("post-chemo")
    if not parts:
        parts.append("first-line")
    return "+".join(parts)


def nsclc_biomarker(rec: dict) -> str:
    bm = rec.get("biomarker") or {}
    parts = []
    if bm.get("egfr_mut") is True:
        parts.append("EGFR-mut")
    if bm.get("egfr_t790m") is True:
        parts.append("EGFR-T790M")
    if bm.get("egfr_ex19del") is True:
        parts.append("EGFR-ex19del")
    if bm.get("egfr_l858r") is True:
        parts.append("EGFR-L858R")
    if bm.get("egfr_ex20ins") is True:
        parts.append("EGFR-ex20ins")
    if bm.get("alk_rearranged") is True:
        parts.append("ALK-rearranged")
    if bm.get("alk_resistance_mut") is True:
        parts.append("ALK-resistance-mut")
    parts.append("NSCLC")
    return "/".join(parts)


def mbc_state(rec: dict) -> str:
    prior = rec.get("prior_state") or {}
    parts = []
    if prior.get("post_endo") is True:
        parts.append("post-endo")
    if prior.get("post_cdk46i") is True:
        parts.append("post-CDK46i")
    if (prior.get("post_chemo_metastatic_min") or 0) >= 1:
        parts.append("post-chemo")
    if not parts:
        parts.append("first-line")
    if prior.get("menopausal_status") == "pre":
        parts.append("pre-menopausal")
    return "+".join(parts)


def mbc_biomarker(rec: dict) -> str:
    bm = rec.get("biomarker") or {}
    parts = []
    if bm.get("hr_pos") is True:        parts.append("HR+")
    if bm.get("her2_neg") is True:      parts.append("HER2-")
    if bm.get("her2_low") is True:      parts.append("HER2-low")
    if bm.get("pik3ca_mut") is True:    parts.append("PIK3CAmut")
    if bm.get("esr1_mut") is True:      parts.append("ESR1mut")
    if bm.get("akt_path") is True:      parts.append("AKTpath")
    if bm.get("brca_germline") is True: parts.append("gBRCAmut")
    return "/".join(parts) if parts else "ANY"


def main() -> None:
    nsclc = json.loads(NSCLC_SRC.read_text())
    mbc   = json.loads(MBC_SRC.read_text())

    edges: list[dict] = []
    nodes_set = set()
    # NSCLC edges
    for r in nsclc:
        if (r.get("notes") or "").lower().startswith("out of scope"):
            continue
        if r.get("drug_class") == "investigational (other)":
            continue
        if r.get("biomarker", {}).get("tumor_type") == "NSCLC-other":
            continue
        s = nsclc_state(r); b = nsclc_biomarker(r)
        nodes_set.add((s, b, "NSCLC"))
        edges.append({
            "nct_id": r["nct_id"], "trial_name": r.get("trial_name"),
            "source_node": f"{s}|{b}",
            "source_state": s, "biomarker": b,
            "subgroup_readouts": r.get("subgroup_readouts") or [],
            "drug_class": r["drug_class"],
            "year_pc": int(r.get("year_pc") or 0),
            "tumor": "NSCLC",
            "guideline_target_node": r.get("guideline_target_node"),
            "provenance": r.get("provenance"),
        })
    # mBC edges
    for r in mbc:
        if "out of scope" in (r.get("notes") or "").lower():
            continue
        if r.get("drug_class") == "investigational (other)":
            continue
        s = mbc_state(r); b = mbc_biomarker(r)
        nodes_set.add((s, b, "mBC"))
        edges.append({
            "nct_id": r["nct_id"], "trial_name": r.get("trial_name"),
            "source_node": f"{s}|{b}",
            "source_state": s, "biomarker": b,
            "subgroup_readouts": r.get("subgroup_readouts") or [],
            "drug_class": r["drug_class"],
            "year_pc": int(r.get("year_pc") or 0),
            "tumor": "mBC",
            "guideline_target_node": r.get("guideline_target_node"),
            "provenance": r.get("provenance"),
        })

    nodes = sorted([{"node_id": f"{s}|{b}", "state": s, "biomarker": b, "tumor": t}
                     for s, b, t in nodes_set], key=lambda x: (x["tumor"], x["node_id"]))
    NODES_OUT.write_text(json.dumps(nodes, indent=2))
    EDGES_OUT.write_text(json.dumps(edges, indent=2))
    print(f"Combined DAG:")
    print(f"  NSCLC edges: {sum(1 for e in edges if e['tumor']=='NSCLC')}")
    print(f"  mBC edges: {sum(1 for e in edges if e['tumor']=='mBC')}")
    print(f"  Total edges: {len(edges)}")
    print(f"  Total nodes: {len(nodes)}")


if __name__ == "__main__":
    main()
