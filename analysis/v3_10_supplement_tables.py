"""Generate LaTeX tables S2 + S3 for Paper A supplement.

S2: Representative per-trial structured extractions (10 sampled trials).
S3: Complete 49-node ESMO/ASCO/NCCN decision tree with concordance status.

Outputs are written to manuscript/ as supplement_table_S2.tex and S3.tex.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "manuscript"


def latex_escape(s: str) -> str:
    if s is None:
        return ""
    s = str(s)
    return (s.replace("&", r"\&")
             .replace("%", r"\%")
             .replace("#", r"\#")
             .replace("_", r"\_")
             .replace("$", r"\$"))


def truncate(s: str, n: int) -> str:
    s = str(s) if s else ""
    return s if len(s) <= n else s[: n - 1] + "…"


# ---------- Table S2: representative per-trial extractions ----------
edges = json.loads((DATA / "processed/v3_combined_dag_edges.json").read_text())
# pick 5 mBC + 5 NSCLC representative pivotal trials, ordered by year_pc
mbc_edges = sorted([e for e in edges if e["tumor"] == "mBC"], key=lambda x: x.get("year_pc", 9999))
nsclc_edges = sorted([e for e in edges if e["tumor"] == "NSCLC"], key=lambda x: x.get("year_pc", 9999))

sample = []
# 5 representative mBC pivotal trials spanning the timeline
for nct in ["NCT01958021", "NCT02278120", "NCT01942135", "NCT03778931", "NCT04494425"]:
    e = next((x for x in mbc_edges if x["nct_id"] == nct), None)
    if e:
        sample.append(e)
# 5 representative NSCLC
for nct in ["NCT01154140", "NCT02296125", "NCT04487080", "NCT02151981", "NCT03521154"]:
    e = next((x for x in nsclc_edges if x["nct_id"] == nct), None)
    if e:
        sample.append(e)

lines = []
lines.append("% Supplementary Table S2 — representative per-trial structured extractions")
lines.append(r"\begin{table}[H]")
lines.append(r"\centering")
lines.append(r"\caption{\textbf{Representative per-trial structured extractions} (10 of the 259 pivotal trials in the v3.0.0 corpus). Full dual-annotator outputs released at \texttt{data/processed/v2\_extraction\_final.json} and \texttt{nsclc\_full.json}.}")
lines.append(r"\label{tab:S2}")
lines.append(r"\footnotesize")
lines.append(r"\begin{tabular}{@{}p{0.13\textwidth}p{0.12\textwidth}p{0.18\textwidth}p{0.22\textwidth}p{0.18\textwidth}@{}}")
lines.append(r"\toprule")
lines.append(r"NCT ID & Trial name & Pre-treatment state & Biomarker / subgroup & Drug class \\")
lines.append(r"\midrule")
for e in sample:
    row = " & ".join([
        latex_escape(e["nct_id"]),
        latex_escape(truncate(e.get("trial_name", ""), 18)),
        latex_escape(truncate(e.get("source_state", ""), 22)),
        latex_escape(truncate(e.get("biomarker", ""), 28)),
        latex_escape(truncate(e.get("drug_class", ""), 28)),
    ])
    lines.append(row + r" \\")
lines.append(r"\bottomrule")
lines.append(r"\end{tabular}")
lines.append(r"\end{table}")
(OUT / "supplement_table_S2.tex").write_text("\n".join(lines) + "\n")
print(f"Wrote {OUT}/supplement_table_S2.tex ({len(sample)} rows)")


# ---------- Table S3: full 49-node guideline tree with concordance ----------
mbc_tree = json.loads((DATA / "processed/v2_decision_tree.json").read_text())
nsclc_tree = json.loads((DATA / "processed/v3_nsclc_decision_tree.json").read_text())
efdpr = json.loads((DATA / "results/v3_pooled_efdpr.json").read_text())
ef_nodes = set(efdpr["primary"]["strict"]["evidence_free_nodes"])
per_node_support = efdpr["primary"]["strict"]["per_node_support"]

lines = []
lines.append("% Supplementary Table S3 — full 49-node ESMO/ASCO/NCCN decision tree")
lines.append(r"\begin{table}[H]")
lines.append(r"\centering")
lines.append(r"\caption{\textbf{Full 49-node ESMO/ASCO/NCCN unified decision tree} with strict-tolerance concordance status. ``Concordant'' = at least one trial edge satisfies state-superset, biomarker-superset, drug-class, and temporal-precedence criteria. ``Evidence-free'' = no such trial edge. Concordant trial counts in last column are derived from \texttt{data/results/v3\_pooled\_efdpr.json}.}")
lines.append(r"\label{tab:S3}")
lines.append(r"\footnotesize")
lines.append(r"\begin{tabular}{@{}p{0.05\textwidth}p{0.10\textwidth}p{0.13\textwidth}p{0.18\textwidth}p{0.22\textwidth}p{0.06\textwidth}p{0.10\textwidth}@{}}")
lines.append(r"\toprule")
lines.append(r"Node & Tumor & State & Biomarker & Recommended class(es) & Year & Concordance \\")
lines.append(r"\midrule")
combined = [("mBC", n) for n in mbc_tree] + [("NSCLC", n) for n in nsclc_tree]
for tumor, n in combined:
    classes = n.get("recommended_classes", [])
    class_str = "; ".join([c.get("class", "") for c in classes]) if isinstance(classes, list) else str(classes)
    nid = n["node_id"]
    nsupport = len(per_node_support.get(nid, []))
    concord = r"\textbf{evidence-free}" if nid in ef_nodes else f"concordant (n={nsupport})"
    row = " & ".join([
        latex_escape(nid),
        latex_escape(tumor),
        latex_escape(truncate(n.get("state", ""), 18)),
        latex_escape(truncate(n.get("biomarker", ""), 25)),
        latex_escape(truncate(class_str, 35)),
        latex_escape(str(n.get("year", "-"))),
        concord,
    ])
    lines.append(row + r" \\")
lines.append(r"\bottomrule")
lines.append(r"\end{tabular}")
lines.append(r"\end{table}")
(OUT / "supplement_table_S3.tex").write_text("\n".join(lines) + "\n")
print(f"Wrote {OUT}/supplement_table_S3.tex ({len(combined)} rows; "
      f"{sum(1 for _,n in combined if n['node_id'] in ef_nodes)} evidence-free)")
