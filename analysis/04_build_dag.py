"""04_build_dag.py
Construct the trial-DAG from structured trial records. Each trial becomes a
directed edge from the (prior-state, biomarker) source node to the
(prior-state plus drug-class, biomarker) target node.

Output:
  data/processed/dag_edges.json    list of edges
  data/processed/dag_nodes.json    list of distinct nodes (state, biomarker)
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRIALS = ROOT / "data" / "processed" / "trials_structured.json"
NODES_OUT = ROOT / "data" / "processed" / "dag_nodes.json"
EDGES_OUT = ROOT / "data" / "processed" / "dag_edges.json"


def _canonical_state(rec: dict) -> str:
    prior = rec.get("prior_state", {})
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


def _canonical_biomarker(rec: dict) -> str:
    bm = rec.get("biomarker", {})
    parts = []
    if bm.get("hr_pos") is True:
        parts.append("HR+")
    if bm.get("her2_neg") is True:
        parts.append("HER2-")
    if bm.get("her2_low") is True:
        parts.append("HER2-low")
    if bm.get("pik3ca_mut") is True:
        parts.append("PIK3CAmut")
    if bm.get("esr1_mut") is True:
        parts.append("ESR1mut")
    if bm.get("akt_path") is True:
        parts.append("AKTpath")
    if bm.get("brca_germline") is True:
        parts.append("gBRCAmut")
    return "/".join(parts) if parts else "ANY"


def _target_state(source_state: str, drug_class: str) -> str:
    """Approximate target state: append the drug class as a 'post-X' token."""
    return f"{source_state}|after:{drug_class}"


def main() -> None:
    trials = json.loads(TRIALS.read_text())
    nodes_set: set[tuple[str, str]] = set()
    edges: list[dict] = []
    for nct, rec in trials.items():
        source_state = _canonical_state(rec)
        biomarker = _canonical_biomarker(rec)
        source_node = f"{source_state}|{biomarker}"
        target_node = f"{_target_state(source_state, rec['drug_class'])}|{biomarker}"
        nodes_set.add((source_state, biomarker))
        edges.append({
            "nct_id":          nct,
            "trial_name":      rec.get("trial_name"),
            "source_node":     source_node,
            "target_node":     target_node,
            "source_state":    source_state,
            "biomarker":       biomarker,
            "subgroup_readouts": rec.get("subgroup_readouts", []),
            "drug_class":      rec["drug_class"],
            "year_pc":         rec["year_pc"],
            "guideline_target_node": rec.get("guideline_target_node"),
        })
    nodes = sorted(
        [{"node_id": f"{s}|{b}", "state": s, "biomarker": b} for s, b in nodes_set],
        key=lambda x: x["node_id"],
    )
    NODES_OUT.write_text(json.dumps(nodes, indent=2))
    EDGES_OUT.write_text(json.dumps(edges, indent=2))
    print(f"wrote {len(nodes)} nodes and {len(edges)} edges")


if __name__ == "__main__":
    main()
