"""07_figures.py
Render the three main figures (PDFs) plus the three LaTeX table inputs.

Outputs:
  figures/fig1_dag.pdf
  figures/fig2_efdpr.pdf
  figures/fig3_odi.pdf
  manuscript/tab_cohort.tex
  manuscript/tab_efdpr.tex
  manuscript/tab_odi.tex
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
FIGS = ROOT / "figures"
MAN  = ROOT / "manuscript"
FIGS.mkdir(parents=True, exist_ok=True)

EDGES = json.loads((ROOT / "data" / "processed" / "dag_edges.json").read_text())
NODES = json.loads((ROOT / "data" / "processed" / "dag_nodes.json").read_text())
TRIALS = json.loads((ROOT / "data" / "processed" / "trials_structured.json").read_text())
GLS = json.loads((ROOT / "data" / "processed" / "esmo_decision_tree.json").read_text())
EFDPR = json.loads((ROOT / "data" / "results" / "efdpr.json").read_text())
ODI = json.loads((ROOT / "data" / "results" / "odi.json").read_text())


def fig1_dag() -> None:
    g = nx.DiGraph()
    for n in NODES:
        g.add_node(n["node_id"], state=n["state"], biomarker=n["biomarker"])
    for e in EDGES:
        g.add_edge(e["source_node"], e["target_node"], trial=e["trial_name"], year=e["year_pc"])
    # Layout: order nodes by treatment-line distance
    order = ["first-line", "first-line+pre-menopausal", "post-endo", "post-endo+post-CDK46i",
             "post-endo+post-CDK46i+post-chemo", "post-CDK46i", "post-chemo"]

    def state_rank(state: str) -> int:
        for i, prefix in enumerate(order):
            if state == prefix:
                return i
        # fallback: by token count
        return len(state.split("+"))
    pos = {}
    # group nodes by state on horizontal axis
    states = sorted({n["state"] for n in NODES}, key=state_rank)
    biomarkers = sorted({n["biomarker"] for n in NODES})
    for n in NODES:
        x = state_rank(n["state"])
        y = biomarkers.index(n["biomarker"])
        pos[n["node_id"]] = (x, y)
    # add target nodes (not in NODES list) with synthetic positions
    for e in EDGES:
        if e["target_node"] not in pos:
            sx, sy = pos[e["source_node"]]
            pos[e["target_node"]] = (sx + 0.45, sy + 0.18)
    plt.figure(figsize=(11, 5.6))
    nx.draw_networkx_edges(g, pos, alpha=0.35, arrows=True, arrowsize=10,
                           edge_color="#1f77b4", connectionstyle="arc3,rad=0.12")
    nx.draw_networkx_nodes(g, pos, nodelist=[n["node_id"] for n in NODES],
                            node_size=520, node_color="#cce5ff",
                            edgecolors="#1f77b4", linewidths=1.2)
    target_only = [n for n in g.nodes() if n not in {x["node_id"] for x in NODES}]
    nx.draw_networkx_nodes(g, pos, nodelist=target_only,
                            node_size=160, node_color="#eeeeee",
                            edgecolors="#999999", linewidths=0.6)
    # short labels
    short = {n["node_id"]: n["state"].replace("+post-", "+").replace("post-", "")
             + "\n" + n["biomarker"].replace("HR+/HER2-", "HR+H2-")
             for n in NODES}
    nx.draw_networkx_labels(g, pos, labels=short, font_size=6)
    edge_labels = {(e["source_node"], e["target_node"]): e["trial_name"][:9]
                   for e in EDGES}
    nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels, font_size=5,
                                  bbox=dict(facecolor="white", edgecolor="none",
                                            alpha=0.75, pad=0.3))
    plt.title("HR+/HER2- mBC pivotal-trial DAG (N=14 trials)", fontsize=10)
    plt.axis("off")
    plt.tight_layout()
    out = FIGS / "fig1_dag.pdf"
    plt.savefig(out, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"  wrote {out}")


def fig2_efdpr() -> None:
    plt.figure(figsize=(6.2, 4.2))
    labels = ["strict", "ESCAT-aligned", "liberal"]
    keys   = ["strict", "escat", "liberal"]
    points = [EFDPR[k]["point_estimate"] for k in keys]
    los    = [EFDPR[k]["ci95_low"] for k in keys]
    his    = [EFDPR[k]["ci95_high"] for k in keys]
    errs   = [[p - lo for p, lo in zip(points, los)],
              [hi - p for p, hi in zip(points, his)]]
    xs = np.arange(len(keys))
    plt.bar(xs, points, color="#5e93c4", edgecolor="#1f4a7b", width=0.55)
    plt.errorbar(xs, points, yerr=errs, fmt="none", ecolor="#222", capsize=4, linewidth=1.1)
    plt.axhline(0.25, color="#c14a4a", linestyle="--", linewidth=1.2,
                label="Pre-registered threshold (0.25)")
    plt.xticks(xs, labels)
    plt.ylabel("Evidence-Free Decision-Point Ratio")
    plt.ylim(0, 1.0)
    plt.title("EFDPR across biomarker-definition tolerance", fontsize=10)
    plt.legend(loc="upper right", fontsize=8, frameon=False)
    for i, p in enumerate(points):
        plt.text(i, p + 0.03, f"{p:.2f}", ha="center", fontsize=9)
    plt.tight_layout()
    out = FIGS / "fig2_efdpr.pdf"
    plt.savefig(out, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"  wrote {out}")


def fig3_odi() -> None:
    items = sorted(ODI.items(), key=lambda x: -x[1]["odi"])
    labels = [k for k, _ in items]
    vals   = [v["odi"] for _, v in items]
    n_trials = [v["n_trials"] for _, v in items]
    plt.figure(figsize=(6.2, 4.2))
    ys = np.arange(len(labels))
    plt.barh(ys, vals, color="#7fb069", edgecolor="#2d5016")
    plt.yticks(ys, [f"{l}\n(n={n})" for l, n in zip(labels, n_trials)], fontsize=8)
    plt.xlabel("Operationalization Discordance Index")
    plt.xlim(0, 1.0)
    plt.title("Pairwise discordance in trial-level biomarker definitions", fontsize=10)
    for i, v in enumerate(vals):
        plt.text(v + 0.015, i, f"{v:.2f}", va="center", fontsize=8)
    plt.gca().invert_yaxis()
    plt.tight_layout()
    out = FIGS / "fig3_odi.pdf"
    plt.savefig(out, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"  wrote {out}")


def write_tab_cohort() -> None:
    n_trials = len(TRIALS)
    states = sorted({_state(t) for t in TRIALS.values()})
    biomarkers = sorted({_biomarker(t) for t in TRIALS.values()})
    n_edges = len(EDGES)
    n_gls = len(GLS)
    body = (
        r"\begin{tabular}{lr}\toprule" "\n"
        r"Item & Count \\ \midrule" "\n"
        rf"Pivotal HR+/HER2- mBC trials (frozen 2026-05-16) & {n_trials} \\" "\n"
        rf"Distinct prior-state classes & {len(states)} \\" "\n"
        rf"Distinct biomarker classes & {len(biomarkers)} \\" "\n"
        rf"Trial-DAG edges & {n_edges} \\" "\n"
        rf"ESMO 2024 decision nodes (HR+/HER2- subset) & {n_gls} \\" "\n"
        r"\bottomrule\end{tabular}" "\n"
    )
    (MAN / "tab_cohort.tex").write_text(body)
    print(f"  wrote {MAN / 'tab_cohort.tex'}")


def _state(rec: dict) -> str:
    prior = rec.get("prior_state", {})
    parts = []
    if prior.get("post_endo") is True: parts.append("post-endo")
    if prior.get("post_cdk46i") is True: parts.append("post-CDK46i")
    if (prior.get("post_chemo_metastatic_min") or 0) >= 1: parts.append("post-chemo")
    if not parts: parts.append("first-line")
    if prior.get("menopausal_status") == "pre": parts.append("pre-menopausal")
    return "+".join(parts)


def _biomarker(rec: dict) -> str:
    bm = rec.get("biomarker", {})
    parts = []
    if bm.get("hr_pos"): parts.append("HR+")
    if bm.get("her2_neg"): parts.append("HER2-")
    if bm.get("her2_low"): parts.append("HER2-low")
    if bm.get("pik3ca_mut"): parts.append("PIK3CAmut")
    if bm.get("esr1_mut"): parts.append("ESR1mut")
    if bm.get("akt_path"): parts.append("AKTpath")
    return "/".join(parts) or "ANY"


def write_tab_efdpr() -> None:
    lines = [
        r"\begin{tabular}{lcccc}\toprule",
        r"Tolerance & EFDPR & 95\% CI & Evidence-free nodes / total & Threshold rejected? \\ \midrule",
    ]
    for tol_key, tol_label in [("strict", "Strict"), ("escat", "ESCAT-aligned"), ("liberal", "Liberal")]:
        r = EFDPR[tol_key]
        rej = "yes" if r["ci95_low"] > 0.25 else ("no" if r["ci95_high"] < 0.25 else "marginal")
        lines.append(
            rf"{tol_label} & {r['point_estimate']:.3f} & "
            rf"[{r['ci95_low']:.3f}, {r['ci95_high']:.3f}] & "
            rf"{r['evidence_free_count']}/{r['total_decision_nodes']} & {rej} \\"
        )
    lines.append(r"\bottomrule\end{tabular}")
    (MAN / "tab_efdpr.tex").write_text("\n".join(lines) + "\n")
    print(f"  wrote {MAN / 'tab_efdpr.tex'}")


def write_tab_odi() -> None:
    lines = [
        r"\begin{tabular}{lccc}\toprule",
        r"Biomarker variable & ODI & Trials compared & Pairs \\ \midrule",
    ]
    for var, r in sorted(ODI.items(), key=lambda x: -x[1]["odi"]):
        safe_var = var.replace("_", r"\_")
        lines.append(
            rf"{safe_var} & {r['odi']:.3f} & {r['n_trials']} & {r['n_pairs']} \\"
        )
    lines.append(r"\bottomrule\end{tabular}")
    (MAN / "tab_odi.tex").write_text("\n".join(lines) + "\n")
    print(f"  wrote {MAN / 'tab_odi.tex'}")


def main() -> None:
    fig1_dag()
    fig2_efdpr()
    fig3_odi()
    write_tab_cohort()
    write_tab_efdpr()
    write_tab_odi()


if __name__ == "__main__":
    main()
