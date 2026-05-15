"""v2_12_figures_polished.py
Publication-grade redesign of v2 figures.

Figure 1: Concordance grid (state x biomarker), one cell per (state, biomarker).
          Each cell shows:
            - guideline-node labels at that position (G-IDs)
            - count of trial edges entering that source-state x biomarker
            - cell color: red = guideline node here AND evidence-free under strict;
                          green = guideline node here AND supported under strict;
                          blue tint = trial-edge cell with no guideline node here;
                          white = empty
Figure 2: Forest plot of EFDPR (primary + 3 sensitivity) with proper headroom,
          legend outside plot area, clean grid.
Figure 3: ODI horizontal bars with corrected labels, error-bar spacing, grammar.
Figure 4: Per-node support heatmap grouped by guideline source.
"""
from __future__ import annotations

import json
from collections import defaultdict
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

EDGES = json.loads((ROOT/"data/processed/v2_dag_edges.json").read_text())
GLS   = json.loads((ROOT/"data/processed/v2_decision_tree.json").read_text())
EFDPR = json.loads((ROOT/"data/results/v2_efdpr.json").read_text())
ODI   = json.loads((ROOT/"data/results/v2_odi.json").read_text())

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
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})


# ===== Figure 1: Concordance grid ============================================

def _normalize_biomarker(b: str) -> str:
    """Map trial-encoded multi-biomarker strings to the closest canonical
    guideline biomarker category."""
    tokens = set(b.split("/"))
    # Drop AKTpath if PIK3CAmut also present (ESCAT-equivalent group)
    # Treat all gBRCAmut variants as gBRCAmut/HER2-
    if "gBRCAmut" in tokens:
        return "gBRCAmut/HER2-"
    # Multi-mutation trials map to the primary biomarker
    if "PIK3CAmut" in tokens and "AKTpath" in tokens:
        return "HR+/HER2-/PIK3CAmut"
    if "AKTpath" in tokens:
        return "HR+/HER2-/AKTpath" if "HR+" in tokens else "HR+/HER2-"
    if "PIK3CAmut" in tokens:
        return "HR+/HER2-/PIK3CAmut"
    if "ESR1mut" in tokens:
        return "HR+/HER2-/ESR1mut"
    if "HER2-low" in tokens:
        return "HR+/HER2-/HER2-low"
    # default HR+/HER2-
    if "HR+" in tokens or "HER2-" in tokens:
        return "HR+/HER2-"
    return b


def _normalize_state(s: str) -> str:
    """Collapse states to a tractable set of columns."""
    tokens = set(s.split("+"))
    if "metastatic" in tokens or "indolent" in tokens or "visceral-crisis" in tokens:
        return s  # keep specials
    if "post-CDK46i" in tokens and "post-endo" in tokens and "post-chemo" in tokens:
        return "post-CDK46i\n+post-endo+post-chemo"
    if "post-CDK46i" in tokens and "post-endo" in tokens:
        return "post-CDK46i\n+post-endo"
    if "post-CDK46i" in tokens and "post-chemo" in tokens:
        return "post-CDK46i\n+post-chemo"
    if "post-CDK46i" in tokens:
        return "post-CDK46i"
    if "post-endo" in tokens and "post-chemo" in tokens:
        return "post-endo\n+post-chemo"
    if "post-endo" in tokens:
        return "post-endo"
    if "post-chemo" in tokens:
        return "post-chemo"
    if "pre-menopausal" in tokens and "first-line" in tokens:
        return "first-line\n(pre-menopausal)"
    if "first-line" in tokens:
        return "first-line"
    return s


def fig1_concordance_grid():
    # Build canonical state and biomarker orderings
    STATES = [
        "first-line", "first-line\n(pre-menopausal)",
        "first-line+visceral-crisis", "first-line+indolent",
        "first-line+indolent+post-menopausal",
        "post-endo", "post-endo\n+post-chemo",
        "post-CDK46i", "post-CDK46i\n+post-endo",
        "post-CDK46i\n+post-chemo",
        "post-CDK46i\n+post-endo+post-chemo",
        "post-CDK46i+post-endo+post-mTORi",
        "post-chemo", "metastatic",
    ]
    BIOMARKERS = [
        "HR+/HER2-",
        "HR+/HER2-/PIK3CAmut",
        "HR+/HER2-/ESR1mut",
        "HR+/HER2-/AKTpath",
        "HR+/HER2-/HER2-low",
        "HR+/HER2-/no-actionable",
        "HR+/HER2-/PIK3CAmut+endo-resistant",
        "gBRCAmut/HER2-",
    ]
    # Filter to states present in data
    present_states = {_normalize_state(e["source_state"]) for e in EDGES} \
                     | {_normalize_state(g["state"]) for g in GLS}
    states = [s for s in STATES if s in present_states]
    present_bms = {_normalize_biomarker(e["biomarker"]) for e in EDGES} \
                  | {g["biomarker"] for g in GLS}
    biomarkers = [b for b in BIOMARKERS if b in present_bms]

    # Build cell data
    ef_set = set(EFDPR["primary"]["strict"]["evidence_free_nodes"])
    cell_gls: dict = defaultdict(list)
    cell_trials: dict = defaultdict(list)
    for g in GLS:
        s = _normalize_state(g["state"]); b = g["biomarker"]
        cell_gls[(s, b)].append(g)
    for e in EDGES:
        s = _normalize_state(e["source_state"]); b = _normalize_biomarker(e["biomarker"])
        cell_trials[(s, b)].append(e)

    fig, ax = plt.subplots(figsize=(11.5, 6.0))
    s_to_x = {s: i for i, s in enumerate(states)}
    b_to_y = {b: i for i, b in enumerate(biomarkers)}

    # Draw all cells as a soft grid
    for sx in range(len(states)):
        for by in range(len(biomarkers)):
            ax.add_patch(Rectangle((sx - 0.46, by - 0.46), 0.92, 0.92,
                                    facecolor="white",
                                    edgecolor="#e0e0e0", linewidth=0.5))

    # Overlay guideline cells (colored by evidence-free vs supported).
    # Place G-ID label at TOP of cell so it doesn't collide with trial circles
    # plotted at cell centre.
    for (s, b), gls in cell_gls.items():
        if s not in s_to_x or b not in b_to_y: continue
        x, y = s_to_x[s], b_to_y[b]
        any_ef = any(g["node_id"] in ef_set for g in gls)
        any_sup = any(g["node_id"] not in ef_set for g in gls)
        if any_ef and not any_sup:
            face = "#fbc6c6"; edge = "#a83232"
        elif any_sup and not any_ef:
            face = "#c6e8c6"; edge = "#2d662d"
        else:
            face = "#fde8b8"; edge = "#a06000"
        ax.add_patch(Rectangle((x - 0.46, y - 0.46), 0.92, 0.92,
                                facecolor=face, edgecolor=edge, linewidth=1.4))
        # Wrap multi-node labels: 1-2 IDs on one line, 3+ IDs vertically
        ids = [g["node_id"] for g in gls]
        if len(ids) <= 2:
            label = ", ".join(ids)
        else:
            label = "\n".join(ids)
        ax.text(x - 0.40, y + 0.36, label, ha="left", va="top",
                 fontsize=6.8 if len(ids) <= 2 else 6.2,
                 weight="bold", color=edge, linespacing=0.95)

    # Overlay trial-count circles (cell centre). Shrink when cell also has
    # a guideline node so the colored cell remains visible at the edges.
    gl_cells = set(cell_gls.keys())
    for (s, b), trials in cell_trials.items():
        if s not in s_to_x or b not in b_to_y: continue
        x, y = s_to_x[s], b_to_y[b]
        n = len(trials)
        # Smaller circle when sharing cell with a guideline node
        has_gl = (s, b) in gl_cells
        base = 60 if has_gl else 80
        per_trial = 18 if has_gl else 30
        size = min(base + per_trial * n, 380 if has_gl else 700)
        ax.scatter([x + (0.18 if has_gl else 0)], [y - (0.05 if has_gl else 0)],
                    s=size, c="#1f4a7b", alpha=0.92,
                    edgecolors="white", linewidths=1.0, zorder=4)
        ax.text(x + (0.18 if has_gl else 0),
                 y - (0.05 if has_gl else 0),
                 str(n), ha="center", va="center",
                 fontsize=7.2 if has_gl else 8,
                 color="white", weight="bold", zorder=5)

    # Axes
    ax.set_xticks(range(len(states)))
    ax.set_xticklabels(states, rotation=35, ha="right", fontsize=7.5)
    ax.set_yticks(range(len(biomarkers)))
    ax.set_yticklabels(biomarkers, fontsize=8)
    ax.set_xlabel("Patient state at trial enrolment")
    ax.set_ylabel("Biomarker profile")
    ax.set_title("Trial–guideline concordance grid (HR+/HER2- mBC, v2 corpus)",
                  pad=12)
    ax.set_xlim(-0.6, len(states) - 0.4)
    ax.set_ylim(-0.6, len(biomarkers) - 0.4 + 0.6)  # headroom for labels
    ax.tick_params(axis="both", which="both", length=0)
    for sp in ("left", "bottom"):
        ax.spines[sp].set_visible(False)

    # Legend (outside plot area, bottom)
    legend_elements = [
        mpatches.Patch(facecolor="#fbc6c6", edgecolor="#a83232",
                       label="Guideline node — evidence-free (strict)"),
        mpatches.Patch(facecolor="#c6e8c6", edgecolor="#2d662d",
                       label="Guideline node — supported (strict)"),
        mpatches.Patch(facecolor="#fde8b8", edgecolor="#a06000",
                       label="Guideline node — mixed (multi-node cell)"),
        plt.Line2D([0], [0], marker="o", color="white", markerfacecolor="#1f4a7b",
                    markersize=10, label="Trial source node (number = trial count)"),
    ]
    ax.legend(handles=legend_elements, loc="upper center",
               bbox_to_anchor=(0.5, -0.20), ncol=2, frameon=False, fontsize=7.5)
    plt.tight_layout()
    out = FIGS / "v2_fig1_dag.pdf"
    plt.savefig(out, bbox_inches="tight")
    plt.close()
    print(f"  {out}")


# ===== Figure 2: Forest plot =================================================

def fig2_forest():
    fig, ax = plt.subplots(figsize=(8.0, 4.5))
    rows = [
        ("Primary (ESMO+ASCO+NCCN, n=25)",      EFDPR["primary"]["strict"]),
        ("Sensitivity: ESMO-only (n=16)",       EFDPR["sensitivity_esmo"]["strict"]),
        ("Sensitivity: ASCO-citing (n=15)",     EFDPR["sensitivity_asco"]["strict"]),
        ("Sensitivity: NCCN-citing (n=10)",     EFDPR["sensitivity_nccn"]["strict"]),
    ]
    labels = [r[0] for r in rows]
    pts    = [r[1]["point_estimate"] for r in rows]
    los    = [r[1]["clopper_pearson_ci95"][0] for r in rows]
    his    = [r[1]["clopper_pearson_ci95"][1] for r in rows]
    pvals  = [r[1]["exact_binomial_pvalue_one_sided_vs_p25"] for r in rows]
    ys = np.arange(len(rows))[::-1]
    ax.errorbar(pts, ys,
                xerr=[[p-lo for p,lo in zip(pts,los)], [hi-p for p,hi in zip(pts,his)]],
                fmt="o", color="#1f4a7b", ecolor="#666", capsize=4,
                markersize=10, lw=1.4, elinewidth=1.4)
    ax.axvline(0.25, color="#c14a4a", linestyle="--", lw=1.0,
                label="Pre-registered H₀ threshold (0.25)", zorder=1)
    # Point-estimate labels (below the dot, not above)
    for y, p in zip(ys, pts):
        ax.text(p, y - 0.32, f"{p:.2f}", ha="center", fontsize=8.5,
                 color="#1f4a7b", weight="bold")
    # P-value column at fixed x position outside CIs
    pval_x = 0.83
    for y, pv in zip(ys, pvals):
        mark = "*" if pv < 0.05 else ""
        txt = f"P = {pv:.3f}" if pv >= 0.001 else "P < 0.001"
        ax.text(pval_x, y, f"{txt}{mark}", fontsize=8.5, color="#222",
                 ha="left", va="center", family="monospace")
    # Header for P-value column
    ax.text(pval_x, len(rows) - 0.4, "Exact P", fontsize=8.5,
             color="#222", weight="bold", ha="left", family="monospace")
    ax.set_yticks(ys)
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlabel("Evidence-Free Decision-Point Ratio (strict tolerance, CP 95% CI)")
    ax.set_xlim(0, 1.10)
    ax.set_ylim(-0.7, len(rows) - 0.2)
    ax.set_title("EFDPR primary outcome + by-guideline sensitivity",
                  pad=24)
    ax.grid(True, axis="x", alpha=0.25, linestyle=":")
    ax.set_axisbelow(True)
    # Legend outside plot
    ax.legend(loc="upper left", bbox_to_anchor=(0.0, 1.10), frameon=False, fontsize=8.5)
    plt.tight_layout()
    out = FIGS / "v2_fig2_forest.pdf"
    plt.savefig(out, bbox_inches="tight")
    plt.close()
    print(f"  {out}")


# ===== Figure 3: ODI =========================================================

def fig3_odi():
    fig, ax = plt.subplots(figsize=(8.0, 4.5))
    items = sorted(ODI.items(), key=lambda x: -x[1]["odi"])
    # Replace ASCII slash-less names with proper slash
    LABEL_FIX = {"prior_CDK4_6i": "prior CDK4/6i",
                 "ESR1mut":       "ESR1 mutation",
                 "AKTpath":       "AKT pathway",
                 "HER2-low":      "HER2-low",
                 "PIK3CAmut":     "PIK3CA mutation",
                 "gBRCAmut":      "germline BRCA"}
    labels = [LABEL_FIX.get(k, k) for k, _ in items]
    vals   = [v["odi"] for _, v in items]
    los    = [v["bootstrap_ci95_low"]  or 0.0 for _, v in items]
    his    = [v["bootstrap_ci95_high"] or 0.0 for _, v in items]
    n_t    = [v["n_trials"] for _, v in items]
    n_p    = [v["n_pairs"]  for _, v in items]
    ys = np.arange(len(labels))[::-1]
    bars = ax.barh(ys, vals, color="#7fb069", edgecolor="#2d5016",
                    height=0.62, alpha=0.9, zorder=2)
    ax.errorbar(vals, ys,
                xerr=[[v-lo for v,lo in zip(vals,los)], [hi-v for v,hi in zip(vals,his)]],
                fmt="none", ecolor="#222", capsize=4, lw=1.0, zorder=3)
    # Value labels far enough right to clear error bars
    label_x_floor = max(his) + 0.04
    for y, v, n, p, hi in zip(ys, vals, n_t, n_p, his):
        pair_word = "pair" if p == 1 else "pairs"
        x_pos = max(hi + 0.025, 0.04)
        ax.text(x_pos, y, f"{v:.2f}   (n={n} trials, {p} {pair_word})",
                 va="center", fontsize=8, color="#222")
    ax.set_yticks(ys); ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlim(0, 1.0)
    ax.set_xlabel("Operationalization Discordance Index "
                   "(mean pairwise Jaccard distance; bootstrap 95% CI)")
    ax.set_title("Cross-trial inclusion-definition discordance by biomarker variable",
                  pad=10)
    ax.grid(True, axis="x", alpha=0.25, linestyle=":")
    ax.set_axisbelow(True)
    plt.tight_layout()
    out = FIGS / "v2_fig3_odi.pdf"
    plt.savefig(out, bbox_inches="tight")
    plt.close()
    print(f"  {out}")


# ===== Figure 4: Per-node support heatmap, grouped by guideline source =======

def fig4_heatmap():
    # Group nodes by guideline source for visual clarity
    SOURCE_ORDER = ["ESMO+ASCO+NCCN", "ESMO+ASCO", "ESMO",
                     "ASCO+NCCN", "ASCO", "NCCN"]
    by_source = defaultdict(list)
    for g in GLS:
        by_source[g["source"]].append(g)
    ordered_nodes = []
    group_boundaries = []
    for src in SOURCE_ORDER:
        if src in by_source:
            sorted_g = sorted(by_source[src], key=lambda x: int(x["node_id"].replace("G","")))
            for g in sorted_g:
                ordered_nodes.append(g)
            group_boundaries.append(len(ordered_nodes))

    primary = EFDPR["primary"]
    tolerances = ["strict", "escat", "liberal"]
    mat = np.zeros((len(ordered_nodes), len(tolerances)))
    for j, tol in enumerate(tolerances):
        per = primary[tol]["per_node_support"]
        for i, g in enumerate(ordered_nodes):
            mat[i, j] = len(per.get(g["node_id"], []))

    fig, ax = plt.subplots(figsize=(6.0, 8.0))
    vmax = max(1, mat.max())
    im = ax.imshow(mat, aspect="auto", cmap="YlGnBu", vmin=0, vmax=vmax)
    # Cell text
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            v = int(mat[i, j])
            color = "white" if v > vmax * 0.6 else "#222"
            ax.text(j, i, str(v), ha="center", va="center",
                     fontsize=7.5, color=color, weight="bold")
    # Group boundary lines
    for bnd in group_boundaries[:-1]:
        ax.axhline(bnd - 0.5, color="#444", lw=1.5, zorder=10)
    # Y-tick labels: G-ID + (source tag)
    y_labels = [f"{g['node_id']}  ({g['source']})" for g in ordered_nodes]
    ax.set_yticks(range(len(ordered_nodes)))
    ax.set_yticklabels(y_labels, fontsize=7.5)
    ax.set_xticks(range(len(tolerances)))
    ax.set_xticklabels([t.capitalize() for t in tolerances], fontsize=9)
    ax.set_xlabel("Concordance tolerance")
    ax.set_ylabel("Guideline decision node (and source)")
    # EFDPR totals annotation ABOVE the heatmap (between title and data) so it
    # doesn't collide with the x-axis label at the bottom.
    totals = []
    for tol in tolerances:
        r = primary[tol]
        totals.append(f"EFDPR = {r['point_estimate']:.2f}\nexact P = {r['exact_binomial_pvalue_one_sided_vs_p25']:.3f}")
    for j, t in enumerate(totals):
        ax.text(j, -0.95, t, ha="center", va="center",
                 fontsize=7.0, color="#1f4a7b",
                 bbox=dict(boxstyle="round,pad=0.30", facecolor="white",
                            edgecolor="#1f4a7b", lw=0.8))
    # Extend y-axis upward to make room
    ax.set_ylim(len(ordered_nodes) - 0.5, -1.6)
    ax.set_title("Trial edges supporting each guideline node\n(grouped by guideline source)",
                  fontsize=10, pad=10)
    plt.colorbar(im, ax=ax, fraction=0.04, pad=0.03, label="# trial edges")
    plt.tight_layout()
    out = FIGS / "v2_fig4_heatmap.pdf"
    plt.savefig(out, bbox_inches="tight")
    plt.close()
    print(f"  {out}")


def main():
    fig1_concordance_grid()
    fig2_forest()
    fig3_odi()
    fig4_heatmap()


if __name__ == "__main__":
    main()
