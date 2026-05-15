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
    """Tabular DAG view: state on x-axis (treatment-line distance), biomarker
    on y-axis. Trials shown as labelled edges from source state to drug class."""
    import matplotlib.patches as mpatches
    state_order = [
        "first-line",
        "first-line+pre-menopausal",
        "post-endo",
        "post-endo+post-CDK46i",
        "post-chemo",
        "post-endo+post-CDK46i+post-chemo",
    ]
    biomarker_order = sorted({n["biomarker"] for n in NODES})
    fig, ax = plt.subplots(figsize=(11, 6.0))
    # Lay out each unique (state, biomarker) source node on the grid.
    state_to_x = {s: i for i, s in enumerate(state_order)}
    bm_to_y = {b: i for i, b in enumerate(biomarker_order)}
    # Group edges by source node so we can stack trial labels.
    by_source: dict[tuple[str, str], list[dict]] = {}
    for e in EDGES:
        by_source.setdefault((e["source_state"], e["biomarker"]), []).append(e)
    # Draw nodes (filled circles) for each source location and a tag inline.
    for (s, b), elist in by_source.items():
        x = state_to_x.get(s, len(state_order))
        y = bm_to_y.get(b, len(biomarker_order))
        ax.scatter([x], [y], s=420, c="#cce5ff", edgecolors="#1f4a7b",
                    linewidths=1.2, zorder=3)
        # node label
        ax.text(x, y - 0.30, f"{s}\n[{b}]", ha="center", va="top", fontsize=6.5)
        # trial labels stacked above node
        for i, e in enumerate(sorted(elist, key=lambda x: x["year_pc"])):
            label = f"{e['trial_name']} ({e['year_pc']}) → {e['drug_class']}"
            ax.annotate(label, xy=(x, y), xytext=(x + 0.18, y + 0.22 + i * 0.20),
                        fontsize=5.5,
                        arrowprops=dict(arrowstyle="->", color="#888",
                                         alpha=0.6, lw=0.7))
    ax.set_xticks(range(len(state_order)))
    ax.set_xticklabels([s.replace("+", "\n+") for s in state_order],
                       fontsize=7.5, rotation=0)
    ax.set_yticks(range(len(biomarker_order)))
    ax.set_yticklabels(biomarker_order, fontsize=7.5)
    ax.set_xlabel("Patient state at trial enrolment", fontsize=9)
    ax.set_ylabel("Biomarker profile", fontsize=9)
    ax.set_title(f"HR+/HER2- mBC pivotal-trial DAG (N={len(EDGES)} trials)",
                  fontsize=10)
    ax.grid(True, alpha=0.25, linestyle=":")
    ax.set_axisbelow(True)
    ax.set_xlim(-0.5, len(state_order) - 0.5)
    ax.set_ylim(-0.7, len(biomarker_order) - 0.2)
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
    los    = [EFDPR[k]["bootstrap_ci95_low"] for k in keys]
    his    = [EFDPR[k]["bootstrap_ci95_high"] for k in keys]
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
        r"\begin{tabular}{lccccc}\toprule",
        r"Tolerance & EFDPR & Bootstrap 95\% CI & Clopper-Pearson 95\% CI & Exact $P$ vs $p_0=0.25$ & Reject H$_0$? \\ \midrule",
    ]
    for tol_key, tol_label in [("strict", "Strict"), ("escat", "ESCAT-aligned"), ("liberal", "Liberal")]:
        r = EFDPR[tol_key]
        rej = "yes" if r["preregistered_test_rejected_at_alpha_05"] else "no"
        lines.append(
            rf"{tol_label} & {r['point_estimate']:.3f} & "
            rf"[{r['bootstrap_ci95_low']:.3f}, {r['bootstrap_ci95_high']:.3f}] & "
            rf"[{r['clopper_pearson_ci95_low']:.3f}, {r['clopper_pearson_ci95_high']:.3f}] & "
            rf"{r['exact_binomial_pvalue_one_sided_vs_p25']:.3f} & {rej} \\"
        )
    lines.append(r"\bottomrule\end{tabular}")
    (MAN / "tab_efdpr.tex").write_text("\n".join(lines) + "\n")
    print(f"  wrote {MAN / 'tab_efdpr.tex'}")


def write_tab_odi() -> None:
    lines = [
        r"\begin{tabular}{lcccc}\toprule",
        r"Biomarker variable & ODI & Bootstrap 95\% CI & Trials & Pairs \\ \midrule",
    ]
    for var, r in sorted(ODI.items(), key=lambda x: -x[1]["odi"]):
        safe_var = var.replace("_", r"\_")
        ci_str = (rf"[{r['bootstrap_ci95_low']:.3f}, {r['bootstrap_ci95_high']:.3f}]"
                  if r['bootstrap_ci95_low'] is not None else "n/a")
        lines.append(
            rf"{safe_var} & {r['odi']:.3f} & {ci_str} & {r['n_trials']} & {r['n_pairs']} \\"
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
