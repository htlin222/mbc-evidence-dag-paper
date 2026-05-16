"""v3_09_figures.py
Publication-grade figures for v3 (mBC + NSCLC pooled).
  Figure 1: Pooled concordance grid (mBC + NSCLC), two-tumor side-by-side
  Figure 2: Pooled forest plot (primary + 4 sensitivity)
  Figure 3: Per-tumor evidence-free decision-point breakdown
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
FIGS = ROOT / "figures"; FIGS.mkdir(parents=True, exist_ok=True)
MAN  = ROOT / "manuscript"

EFDPR = json.loads((ROOT/"data/results/v3_pooled_efdpr.json").read_text())

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "axes.titlesize": 11,
    "axes.labelsize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})


def fig_forest():
    """Forest plot of pooled + 4 sensitivity analyses.
    v3 R3 fix: read n_nodes from JSON, not hard-coded literals."""
    fig, ax = plt.subplots(figsize=(8.5, 5.0))
    def nn(key):
        return EFDPR[key]["strict"]["total_nodes"]
    rows = [
        (f"Primary: pooled mBC + NSCLC (n={nn('primary')})",      EFDPR["primary"]["strict"]),
        (f"Sensitivity: mBC-only (n={nn('mbc_only')})",            EFDPR["mbc_only"]["strict"]),
        (f"Sensitivity: NSCLC-only (n={nn('nsclc_only')})",        EFDPR["nsclc_only"]["strict"]),
        (f"Sensitivity: NSCLC EGFR-only (n={nn('nsclc_egfr_only')})", EFDPR["nsclc_egfr_only"]["strict"]),
        (f"Sensitivity: NSCLC ALK-only (n={nn('nsclc_alk_only')})",   EFDPR["nsclc_alk_only"]["strict"]),
    ]
    labels = [r[0] for r in rows]
    pts    = [r[1]["point_estimate"] for r in rows]
    los    = [r[1]["clopper_pearson_ci95"][0] for r in rows]
    his    = [r[1]["clopper_pearson_ci95"][1] for r in rows]
    pvals  = [r[1]["exact_p_one_sided_vs_p25"] for r in rows]
    ys = np.arange(len(rows))[::-1]
    # Bold the primary row
    ax.errorbar(pts[0], ys[0],
                xerr=[[pts[0]-los[0]], [his[0]-pts[0]]],
                fmt="D", color="#a83232", ecolor="#a83232", capsize=5,
                markersize=12, lw=1.8, elinewidth=1.8)
    ax.errorbar(pts[1:], ys[1:],
                xerr=[[p-lo for p,lo in zip(pts[1:],los[1:])],
                      [hi-p for p,hi in zip(pts[1:],his[1:])]],
                fmt="o", color="#1f4a7b", ecolor="#666", capsize=4,
                markersize=9, lw=1.3, elinewidth=1.3)
    ax.axvline(0.25, color="#c14a4a", linestyle="--", lw=1.0,
                label="Pre-registered H₀ threshold (0.25)")
    for y, p in zip(ys, pts):
        ax.text(p, y - 0.34, f"{p:.2f}", ha="center", fontsize=8.5,
                 color="#1f4a7b", weight="bold")
    pval_x = 0.83
    for y, pv in zip(ys, pvals):
        mark = " *" if pv < 0.05 else ""
        txt = f"P = {pv:.4f}" if pv >= 0.0001 else "P < 0.0001"
        ax.text(pval_x, y, f"{txt}{mark}", fontsize=8.5, color="#222",
                 ha="left", va="center", family="monospace",
                 weight="bold" if pv < 0.05 else "normal")
    ax.text(pval_x, len(rows) - 0.4, "Exact P", fontsize=9,
             color="#222", weight="bold", ha="left", family="monospace")
    ax.set_yticks(ys); ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlabel("Evidence-Free Decision-Point Ratio (strict tolerance, CP 95% CI)")
    ax.set_xlim(0, 1.10); ax.set_ylim(-0.7, len(rows) - 0.2)
    primary_p = EFDPR["primary"]["strict"]["exact_p_one_sided_vs_p25"]
    verdict = "rejects H₀" if primary_p < 0.05 else "marginal non-rejection"
    ax.set_title(f"Pooled mBC + NSCLC EFDPR — pre-registered primary test {verdict} (P = {primary_p:.3f})",
                  pad=20)
    ax.grid(True, axis="x", alpha=0.25, linestyle=":")
    ax.set_axisbelow(True)
    ax.legend(loc="upper left", bbox_to_anchor=(0.0, 1.08), frameon=False, fontsize=8.5)
    plt.tight_layout()
    out = FIGS / "v3_fig1_forest.pdf"
    plt.savefig(out, bbox_inches="tight"); plt.close()
    print(f"  {out}")


def fig_per_tumor_breakdown():
    """Per-tumor evidence-free decision-point bar plot."""
    primary = EFDPR["primary"]["strict"]
    per_node = primary["per_node_support"]
    # Load decision trees
    mbc_gl = json.loads((ROOT/"data/processed/v2_decision_tree.json").read_text())
    nsclc_gl = json.loads((ROOT/"data/processed/v3_nsclc_decision_tree.json").read_text())
    # Order nodes by id (G* mBC then N* NSCLC)
    nodes = mbc_gl + nsclc_gl
    n_supports = [len(per_node.get(g["node_id"], [])) for g in nodes]
    labels = [g["node_id"] for g in nodes]
    tumors = ["mBC" if g["node_id"].startswith("G") else "NSCLC" for g in nodes]
    colors = ["#a83232" if n == 0 else ("#1f4a7b" if t == "mBC" else "#7fb069")
              for n, t in zip(n_supports, tumors)]
    fig, ax = plt.subplots(figsize=(11, 5.0))
    xs = np.arange(len(labels))
    bars = ax.bar(xs, n_supports, color=colors, edgecolor="#222", lw=0.5)
    # Mark separating line between mBC and NSCLC
    n_mbc = sum(1 for t in tumors if t == "mBC")
    ax.axvline(n_mbc - 0.5, color="#444", lw=1.2, ls="--", alpha=0.6)
    ax.text(n_mbc/2 - 0.5, max(n_supports) * 0.95, "mBC HR+/HER2-",
             ha="center", fontsize=10, weight="bold", color="#1f4a7b")
    ax.text(n_mbc + (len(nodes) - n_mbc)/2 - 0.5, max(n_supports) * 0.95,
             "NSCLC EGFR + ALK",
             ha="center", fontsize=10, weight="bold", color="#2d5016")
    ax.set_xticks(xs); ax.set_xticklabels(labels, rotation=90, fontsize=7)
    ax.set_ylabel("# trial edges supporting node (strict)")
    n_pool = EFDPR["primary"]["strict"]["total_nodes"]
    ax.set_title(f"Per-node trial-edge support across pooled {n_pool}-node guideline tree", pad=8)
    legend_elements = [
        mpatches.Patch(facecolor="#1f4a7b", label="mBC node (supported)"),
        mpatches.Patch(facecolor="#7fb069", label="NSCLC node (supported)"),
        mpatches.Patch(facecolor="#a83232", label="Evidence-free (strict)"),
    ]
    ax.legend(handles=legend_elements, loc="upper right", frameon=False, fontsize=8)
    ax.grid(True, axis="y", alpha=0.25, linestyle=":")
    ax.set_axisbelow(True)
    plt.tight_layout()
    out = FIGS / "v3_fig2_per_node.pdf"
    plt.savefig(out, bbox_inches="tight"); plt.close()
    print(f"  {out}")


def fig_trajectory():
    """Pilot -> production -> multi-tumor trajectory of EFDPR + P-value.
    v3 R3 fix: read v3 numbers from JSON, not hard-coded literals."""
    fig, ax1 = plt.subplots(figsize=(8.0, 4.5))
    v3 = EFDPR["primary"]["strict"]
    v3_n = v3["total_nodes"]
    v3_ef = v3["point_estimate"]
    v3_p  = v3["exact_p_one_sided_vs_p25"]
    stages = ["v1.0.0\nmBC pilot\n(n=16)",
               "v2.0.0\nmBC production\n(n=25)",
               f"v3.0.0\nmBC+NSCLC pooled\n(n={v3_n})"]
    efdprs = [0.31, 0.40, v3_ef]
    pvals  = [0.37, 0.071, v3_p]
    xs = np.arange(len(stages))
    ax1.plot(xs, efdprs, "-D", color="#1f4a7b", markersize=12, lw=2,
              label="EFDPR (strict)")
    ax1.axhline(0.25, color="#c14a4a", linestyle="--", lw=1.0, alpha=0.7,
                 label="Pre-registered H₀ threshold (0.25)")
    for x, e in zip(xs, efdprs):
        ax1.text(x, e + 0.03, f"{e:.2f}", ha="center", fontsize=10,
                 weight="bold", color="#1f4a7b")
    ax1.set_xticks(xs); ax1.set_xticklabels(stages, fontsize=8.5)
    ax1.set_ylabel("EFDPR (strict tolerance)", color="#1f4a7b")
    ax1.tick_params(axis="y", labelcolor="#1f4a7b")
    ax1.set_ylim(0, 0.7)
    ax1.grid(True, axis="y", alpha=0.25, linestyle=":")

    ax2 = ax1.twinx()
    ax2.spines["top"].set_visible(False)
    ax2.plot(xs, [-np.log10(p) for p in pvals], "-s", color="#a83232",
              markersize=10, lw=1.8, alpha=0.85, label="−log₁₀(P)")
    for x, p in zip(xs, pvals):
        label = f"P = {p:.4f}" if p >= 0.001 else f"P < 0.001"
        ax2.text(x, -np.log10(p) + 0.15, label, ha="center",
                 fontsize=9, color="#a83232", weight="bold")
    ax2.axhline(-np.log10(0.05), color="#666", linestyle=":", lw=1.0)
    ax2.text(0.05, -np.log10(0.05) + 0.05, "α = 0.05", fontsize=8, color="#666")
    ax2.set_ylabel("−log₁₀(exact one-sided P)", color="#a83232")
    ax2.tick_params(axis="y", labelcolor="#a83232")
    ax2.set_ylim(0, 4.5)

    fig.suptitle("Pilot → production → multi-tumor: directional + significance trajectory",
                  fontsize=11)
    fig.tight_layout()
    out = FIGS / "v3_fig3_trajectory.pdf"
    plt.savefig(out, bbox_inches="tight"); plt.close()
    print(f"  {out}")


def main():
    fig_forest()
    fig_per_tumor_breakdown()
    fig_trajectory()


if __name__ == "__main__":
    main()
