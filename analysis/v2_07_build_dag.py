"""v2_07_build_dag.py
Build the v2 trial DAG from the 80-trial adjudicated extraction. Out-of-scope
and investigational-other trials are recorded but excluded from concordance.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data" / "processed" / "v2_extraction_final.json"
NODES_OUT = ROOT / "data" / "processed" / "v2_dag_nodes.json"
EDGES_OUT = ROOT / "data" / "processed" / "v2_dag_edges.json"


def canonical_state(rec: dict) -> str:
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


def canonical_biomarker(rec: dict) -> str:
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
    extract = json.loads(SRC.read_text())
    in_scope = [r for r in extract
                if "out of scope" not in (r.get("notes") or "").lower()
                and r.get("drug_class") != "investigational (other)"]
    nodes_set: set[tuple[str, str]] = set()
    edges: list[dict] = []
    skipped: list[dict] = []
    for r in extract:
        if r not in in_scope:
            skipped.append({"nct_id": r["nct_id"], "trial_name": r.get("trial_name"),
                            "reason": r.get("notes") or "investigational"})
            continue
        s = canonical_state(r)
        b = canonical_biomarker(r)
        nodes_set.add((s, b))
        edges.append({
            "nct_id":      r["nct_id"],
            "trial_name":  r.get("trial_name"),
            "source_node": f"{s}|{b}",
            "source_state": s,
            "biomarker":    b,
            "subgroup_readouts": r.get("subgroup_readouts") or [],
            "drug_class":   r["drug_class"],
            "year_pc":      int(r.get("year_pc") or 0),
            "guideline_target_node": r.get("guideline_target_node"),
            "provenance":   r.get("provenance"),
        })
    nodes = sorted([{"node_id": f"{s}|{b}", "state": s, "biomarker": b}
                     for s, b in nodes_set], key=lambda x: x["node_id"])
    NODES_OUT.write_text(json.dumps(nodes, indent=2))
    EDGES_OUT.write_text(json.dumps(edges, indent=2))
    print(f"in-scope edges: {len(edges)}")
    print(f"canonical source nodes: {len(nodes)}")
    print(f"skipped (out-of-scope / investigational): {len(skipped)}")
    # Edge year distribution
    from collections import Counter
    yc = Counter(e["year_pc"] for e in edges)
    print(f"primary-completion year distribution: {sorted(yc.items())}")


if __name__ == "__main__":
    main()
