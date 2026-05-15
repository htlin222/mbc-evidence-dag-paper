"""v2_11_figures.py
Publication-grade figures for v2.
  Figure 1: Trial-DAG with state on x-axis, biomarker on y-axis, edges as
            trial annotations. Color by drug class.
  Figure 2: Forest plot of EFDPR across guideline subsets (primary +
            sensitivity), with Clopper-Pearson 95% CIs and the 0.25 reference line.
  Figure 3: ODI per biomarker variable with bootstrap CI errorbars.
  Figure 4: Per-node support count (heatmap of guideline node x tolerance).
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
FIGS = ROOT / "figures"; FIGS.mkdir(parents=True, exist_ok=True)
MAN  = ROOT / "manuscript"

EDGES = json.loads((ROOT/"data/processed/v2_dag_edges.json").read_text())
GLS   = json.loads((ROOT/"data/processed/v2_decision_tree.json").read_text())
EFDPR = json.loads((ROOT/"data/results/v2_efdpr.json").read_text())
ODI   = json.loads((ROOT/"data/results/v2_odi.json").read_text())

# Publication-quality defaults
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "axes.titlesize": 10,
    "axes.labelsize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "pdf.fonttype": 42,  # editable text
    "ps.fonttype": 42,
})


# ===== Figure 1: Trial-DAG ===================================================

DRUG_COLORS = {
    "CDK4/6i + AI":                                 "#1f77b4",
    "CDK4/6i + fulvestrant":                        "#aec7e8",
    "CDK4/6i + endocrine (pre-menopausal)":         "#1f77b4",
    "CDK4/6i + fulvestrant (post-CDK4/6i)":         "#9edae5",
    "PI3Ki + fulvestrant":                          "#ff7f0e",
    "PI3Ki triplet (inavolisib + CDK4/6i + fulv)":  "#ffbb78",
    "AKTi + fulvestrant":                           "#d62728",
    "AKTi + chemotherapy":                          "#ff9896",
    "SERD oral":                                    "#2ca02c",
    "SERD oral + CDK4/6i":                          "#98df8a",
    "HER2-ADC (T-DXd)":                             "#9467bd",
    "HER2-ADC (other)":                             "#c5b0d5",
    "TROP2-ADC (sacituzumab govitecan)":            "#8c564b",
    "TROP2-ADC (datopotamab deruxtecan)":           "#c49c94",
    "PARPi (olaparib)":                             "#e377c2",
    "PARPi (talazoparib)":                          "#f7b6d2",
    "everolimus + exemestane":                      "#7f7f7f",
    "chemotherapy single agent":                    "#bcbd22",
    "AKTi + chemotherapy":                          "#dbdb8d",
    "endocrine therapy alone":                      "#17becf",
    "investigational (other)":                      "#cccccc",
}


def fig1_dag():
    state_order = [
        "first-line", "first-line+pre-menopausal", "first-line+visceral-crisis",
        "first-line+indolent", "first-line+indolent+post-menopausal",
        "post-endo", "post-endo+post-CDK46i", "post-CDK46i",
        "post-CDK46i+post-endo", "post-CDK46i+post-chemo",
        "post-CDK46i+post-endo+post-mTORi",
        "post-endo+post-CDK46i+post-chemo", "post-chemo", "metastatic",
    ]
    biomarker_order = ["HR+/HER2-", "HR+/HER2-/PIK3CAmut", "HR+/HER2-/ESR1mut",
                       "HR+/HER2-/AKTpath", "HR+/HER2-/HER2-low",
                       "HR+/HER2-/PIK3CAmut+endo-resistant",
                       "HR+/HER2-/no-actionable", "gBRCAmut/HER2-"]
    # de-dup biomarkers from data
    bm_from_data = sorted({e["biomarker"] for e in EDGES} | {g["biomarker"] for g in GLS},
                          key=lambda b: biomarker_order.index(b) if b in biomarker_order else 999)
    biomarker_order = bm_from_data
    fig, ax = plt.subplots(figsize=(10.5, 6.8))
    # Index nodes
    state_to_x = {s: i for i, s in enumerate(state_order)}
    bm_to_y    = {b: i for i, b in enumerate(biomarker_order)}
    # Group trials by (state, biomarker)
    by_loc = defaultdict(list)
    for e in EDGES:
        by_loc[(e["source_state"], e["biomarker"])].append(e)
    # Group guideline nodes by (state, biomarker)
    by_g = defaultdict(list)
    for g in GLS:
        by_g[(g["state"], g["biomarker"])].append(g)
    # Plot guideline nodes (background squares)
    for (s, b), gls in by_g.items():
        x, y = state_to_x.get(s), bm_to_y.get(b)
        if x is None or y is None: continue
        ax.scatter([x], [y], s=900, marker="s", facecolor="#ffe9b8",
                    edgecolors="#a06000", linewidths=1.2, zorder=1)
        ax.text(x, y - 0.32, "+".join(g["node_id"] for g in gls),
                 ha="center", va="top", fontsize=6, color="#603000", weight="bold")
    # Plot trial source nodes (circles)
    for (s, b), elist in by_loc.items():
        x, y = state_to_x.get(s), bm_to_y.get(b)
        if x is None or y is None: continue
        ax.scatter([x], [y], s=200, c="#1f4a7b", alpha=0.85,
                    edgecolors="white", linewidths=0.5, zorder=4)
        ax.text(x + 0.20, y, f"n={len(elist)}", ha="left", va="center",
                 fontsize=7, weight="bold")
    # Configure axes
    ax.set_xticks(range(len(state_order)))
    ax.set_xticklabels([s.replace("+", "\n+") for s in state_order],
                       rotation=45, ha="right", fontsize=7.5)
    ax.set_yticks(range(len(biomarker_order)))
    ax.set_yticklabels(biomarker_order, fontsize=7.5)
    ax.set_xlabel("Patient state at trial enrolment")
    ax.set_ylabel("Biomarker profile")
    ax.set_title(f"v2 trial-DAG (N={len(EDGES)} in-scope trials, {len(GLS)} guideline nodes)")
    ax.grid(True, alpha=0.20, linestyle=":")
    ax.set_axisbelow(True)
    ax.set_xlim(-0.5, len(state_order) - 0.5)
    ax.set_ylim(-0.7, len(biomarker_order) - 0.2)
    # Legend
    legend = [
        mpatches.Patch(facecolor="#ffe9b8", edgecolor="#a06000", label="Guideline decision node"),
        mpatches.Patch(facecolor="#1f4a7b", label="Trial source node (size=enrolment)"),
    ]
    ax.legend(handles=legend, loc="upper left", fontsize=7, frameon=False)
    plt.tight_layout()
    out = FIGS / "v2_fig1_dag.pdf"
    plt.savefig(out, bbox_inches="tight")
    plt.close()
    print(f"  {out}")


# ===== Figure 2: Forest plot of EFDPR =======================================

def fig2_forest():
    fig, ax = plt.subplots(figsize=(7, 4.2))
    rows = [
        ("Primary (ESMO+ASCO+NCCN, n=25)", EFDPR["primary"]["strict"]),
        ("Sensitivity: ESMO-only (n=16)", EFDPR["sensitivity_esmo"]["strict"]),
        ("Sensitivity: ASCO-citing (n=15)", EFDPR["sensitivity_asco"]["strict"]),
        ("Sensitivity: NCCN-citing (n=10)", EFDPR["sensitivity_nccn"]["strict"]),
    ]
    labels = [r[0] for r in rows]
    pts    = [r[1]["point_estimate"] for r in rows]
    los    = [r[1]["clopper_pearson_ci95"][0] for r in rows]
    his    = [r[1]["clopper_pearson_ci95"][1] for r in rows]
    pvals  = [r[1]["exact_binomial_pvalue_one_sided_vs_p25"] for r in rows]
    ys = np.arange(len(rows))[::-1]
    # CI bars
    ax.errorbar(pts, ys, xerr=[[p-lo for p,lo in zip(pts,los)],
                                [hi-p for p,hi in zip(pts,his)]],
                fmt="o", color="#1f4a7b", ecolor="#666", capsize=4, markersize=8, lw=1.2)
    ax.axvline(0.25, color="#c14a4a", linestyle="--", lw=1, label="Pre-registered H0 threshold (0.25)")
    for y, p, pv in zip(ys, pts, pvals):
        marker = "*" if pv < 0.05 else ""
        ax.text(p + 0.04, y + 0.18, f"{p:.2f} {marker}", fontsize=8, color="#1f4a7b")
        ax.text(1.03, y, f"P={pv:.4f}" if pv >= 0.001 else f"P<0.001",
                 fontsize=8, color="#444")
    ax.set_yticks(ys)
    ax.set_yticklabels(labels, fontsize=8)
    ax.set_xlabel("Evidence-Free Decision-Point Ratio (EFDPR), strict tolerance")
    ax.set_xlim(0, 1.18)
    ax.set_title("EFDPR forest plot: primary + by-guideline sensitivity")
    ax.legend(loc="lower right", fontsize=8, frameon=False)
    plt.tight_layout()
    out = FIGS / "v2_fig2_forest.pdf"
    plt.savefig(out, bbox_inches="tight")
    plt.close()
    print(f"  {out}")


# ===== Figure 3: ODI ========================================================

def fig3_odi():
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    items = sorted(ODI.items(), key=lambda x: -x[1]["odi"])
    labels = [k for k, _ in items]
    vals   = [v["odi"] for _, v in items]
    los    = [v["bootstrap_ci95_low"]  or 0.0 for _, v in items]
    his    = [v["bootstrap_ci95_high"] or 0.0 for _, v in items]
    n_t    = [v["n_trials"] for _, v in items]
    n_p    = [v["n_pairs"]  for _, v in items]
    ys = np.arange(len(labels))[::-1]
    ax.barh(ys, vals, color="#7fb069", edgecolor="#2d5016", height=0.6)
    ax.errorbar(vals, ys, xerr=[[v-lo for v,lo in zip(vals,los)],
                                 [hi-v for v,hi in zip(vals,his)]],
                fmt="none", ecolor="#222", capsize=4, lw=1.0)
    for y, v, n, p in zip(ys, vals, n_t, n_p):
        ax.text(v + 0.02, y, f"{v:.2f}  (n={n} trials, {p} pairs)",
                 va="center", fontsize=7.5)
    ax.set_yticks(ys); ax.set_yticklabels([l.replace("_", " ") for l in labels])
    ax.set_xlim(0, 1.0)
    ax.set_xlabel("Operationalization Discordance Index (mean pairwise Jaccard distance)")
    ax.set_title("Cross-trial inclusion-definition discordance by biomarker variable")
    plt.tight_layout()
    out = FIGS / "v2_fig3_odi.pdf"
    plt.savefig(out, bbox_inches="tight")
    plt.close()
    print(f"  {out}")


# ===== Figure 4: per-node support heatmap ==================================

def fig4_heatmap():
    primary = EFDPR["primary"]
    nodes = sorted(primary["strict"]["per_node_support"].keys(),
                    key=lambda n: int(n.replace("G","")))
    tolerances = ["strict", "escat", "liberal"]
    mat = np.zeros((len(nodes), len(tolerances)))
    for j, tol in enumerate(tolerances):
        per = primary[tol]["per_node_support"]
        for i, nid in enumerate(nodes):
            mat[i, j] = len(per.get(nid, []))
    fig, ax = plt.subplots(figsize=(5.0, 8.0))
    im = ax.imshow(mat, aspect="auto", cmap="YlGnBu", vmin=0, vmax=max(1, mat.max()))
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            v = int(mat[i, j])
            ax.text(j, i, str(v), ha="center", va="center",
                     fontsize=7, color="white" if v > mat.max()*0.6 else "#222")
    ax.set_xticks(range(len(tolerances))); ax.set_xticklabels([t.title() for t in tolerances], fontsize=8)
    ax.set_yticks(range(len(nodes))); ax.set_yticklabels(nodes, fontsize=7.5)
    ax.set_xlabel("Concordance tolerance")
    ax.set_ylabel("ESMO/ASCO/NCCN decision node")
    ax.set_title("Trial edges supporting each guideline node")
    plt.colorbar(im, ax=ax, fraction=0.04, pad=0.03)
    plt.tight_layout()
    out = FIGS / "v2_fig4_heatmap.pdf"
    plt.savefig(out, bbox_inches="tight")
    plt.close()
    print(f"  {out}")


# ===== Tables ===============================================================

def write_tables():
    # Table 1: cohort summary
    n_trials = len(EDGES)
    n_nodes = len(GLS)
    n_source_nodes = len({e["source_node"] for e in EDGES})
    body = (
        r"\begin{tabular}{lr}\toprule" "\n"
        r"Item & Count \\ \midrule" "\n"
        rf"Pivotal HR+/HER2- mBC trials (frozen 2026-05-16) & {n_trials} \\" "\n"
        rf"Distinct trial source nodes & {n_source_nodes} \\" "\n"
        rf"Guideline decision nodes (ESMO + ASCO + NCCN) & {n_nodes} \\" "\n"
        rf"ESMO-source nodes & {sum(1 for g in GLS if 'ESMO' in g['source'])} \\" "\n"
        rf"ASCO-citing nodes & {sum(1 for g in GLS if 'ASCO' in g['source'])} \\" "\n"
        rf"NCCN-citing nodes & {sum(1 for g in GLS if 'NCCN' in g['source'])} \\" "\n"
        r"\bottomrule\end{tabular}" "\n"
    )
    (MAN / "v2_tab_cohort.tex").write_text(body)

    # Table 2: EFDPR main + sensitivity
    lines = [
        r"\begin{tabular}{lcccc}\toprule",
        r"Analysis & EFDPR (strict) & 95\% CI (CP) & Exact $P$ vs $p_0=0.25$ & Reject H$_0$? \\ \midrule",
    ]
    for label, key in [
        ("Primary (ESMO+ASCO+NCCN, $n=25$)", "primary"),
        ("ESMO-only ($n=16$)", "sensitivity_esmo"),
        ("ASCO-citing ($n=15$)", "sensitivity_asco"),
        ("NCCN-citing ($n=10$)", "sensitivity_nccn"),
    ]:
        r = EFDPR[key]["strict"]
        rej = "yes" if r["rejects_h0_at_alpha_05"] else "no"
        p_str = f"{r['exact_binomial_pvalue_one_sided_vs_p25']:.4f}" if r['exact_binomial_pvalue_one_sided_vs_p25'] >= 0.0001 else "<0.0001"
        lines.append(
            rf"{label} & {r['point_estimate']:.3f} & "
            rf"[{r['clopper_pearson_ci95'][0]:.3f}, {r['clopper_pearson_ci95'][1]:.3f}] & "
            rf"{p_str} & {rej} \\"
        )
    lines.append(r"\bottomrule\end{tabular}")
    (MAN / "v2_tab_efdpr.tex").write_text("\n".join(lines) + "\n")

    # Table 3: ODI
    lines = [
        r"\begin{tabular}{lccc}\toprule",
        r"Biomarker variable & ODI & Bootstrap 95\% CI & Trials (pairs) \\ \midrule",
    ]
    for var, r in sorted(ODI.items(), key=lambda x: -x[1]["odi"]):
        safe = var.replace("_", r"\_")
        ci = (rf"[{r['bootstrap_ci95_low']:.3f}, {r['bootstrap_ci95_high']:.3f}]"
              if r['bootstrap_ci95_low'] is not None else "n/a")
        lines.append(rf"{safe} & {r['odi']:.3f} & {ci} & {r['n_trials']} ({r['n_pairs']}) \\")
    lines.append(r"\bottomrule\end{tabular}")
    (MAN / "v2_tab_odi.tex").write_text("\n".join(lines) + "\n")
    print("  wrote v2_tab_cohort.tex, v2_tab_efdpr.tex, v2_tab_odi.tex")


def main():
    fig1_dag()
    fig2_forest()
    fig3_odi()
    fig4_heatmap()
    write_tables()


if __name__ == "__main__":
    main()
