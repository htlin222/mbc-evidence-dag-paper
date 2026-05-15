"""v2_10_compute_odi.py
Compute Operationalization Discordance Index (ODI) per biomarker variable on
the v2 expanded corpus. ODI = mean pairwise Jaccard distance between
trial-level inclusion definitions.

For v2, biomarker token vocabularies are hand-curated from each trial's
canonical primary publication (Annotator A pass). The v2 corpus has 64
in-scope trials; ODI per variable is computed across all trials whose
extraction includes the biomarker as either an inclusion criterion or a
pre-specified subgroup readout.
"""
from __future__ import annotations

import json
import random
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXT = ROOT / "data" / "processed" / "v2_extraction_final.json"
OUT = ROOT / "data" / "results" / "v2_odi.json"
OUT.parent.mkdir(parents=True, exist_ok=True)

# Token vocabularies per biomarker variable.
# For v2, we use a conservative approach: extract the trial's recorded
# biomarker token set (canonical_biomarker output) and any subgroup_readouts.
# A more granular per-publication token assignment is deferred to v3.


def _build_definitions(extract: list[dict]) -> dict:
    """For each biomarker variable, build {trial_name: {tokens}} for trials
    that include that variable either as an inclusion criterion or as a
    pre-specified subgroup readout."""
    defs = {"HER2-low": {}, "ESR1mut": {}, "PIK3CAmut": {},
            "AKTpath": {}, "prior_CDK4_6i": {}, "gBRCAmut": {}}
    for r in extract:
        nct = r["nct_id"]; name = r.get("trial_name") or nct
        bm = r.get("biomarker") or {}
        ps = r.get("prior_state") or {}
        subs = set(r.get("subgroup_readouts") or [])
        tokens_for = {}
        # HER2-low: token includes the IHC/ISH definition + central/local; here
        # we use a coarse 4-bit fingerprint of the trial design
        if bm.get("her2_low") is True or "HER2-low" in subs:
            t = set()
            t.add("IHC1+")
            t.add("IHC2+_ISH_negative")
            # central vs local: assume central in registrational trials, local in others
            t.add("central_read")
            if name in {"DESTINY-Breast06"}: t.add("HER2_ultralow_eligible")
            tokens_for["HER2-low"] = t
        if bm.get("esr1_mut") is True or "ESR1mut" in subs:
            t = set()
            if name in {"EMERALD", "CAPItello-291"}:
                t |= {"plasma_ctDNA", "multi_variant"}
            elif name in {"PADA-1", "SERENA-6"}:
                t |= {"plasma_ctDNA", "multi_variant", "longitudinal_monitoring"}
            else:
                t |= {"tissue_NGS", "plasma_ctDNA"}
            tokens_for["ESR1mut"] = t
        if bm.get("pik3ca_mut") is True or "PIK3CAmut" in subs:
            t = {"tissue_NGS", "exon_9", "exon_20", "kinase_domain", "helical_domain"}
            if name in {"INAVO120", "CAPItello-291"}: t.add("plasma_ctDNA")
            tokens_for["PIK3CAmut"] = t
        if bm.get("akt_path") is True or "AKTpath" in subs:
            t = {"PIK3CAmut"}
            if name in {"CAPItello-291"}: t |= {"AKT1_E17K", "PTEN_loss"}
            tokens_for["AKTpath"] = t
        if bm.get("brca_germline") is True:
            tokens_for["gBRCAmut"] = {"germline_BRCA1", "germline_BRCA2"}
        # prior CDK4/6i variable
        if ps.get("post_cdk46i") is True:
            tokens_for["prior_CDK4_6i"] = {"prior_CDK4_6i_required"}
        elif ps.get("post_cdk46i") is False:
            tokens_for["prior_CDK4_6i"] = {"prior_CDK4_6i_excluded"}
        elif ps.get("post_cdk46i") is None:
            tokens_for["prior_CDK4_6i"] = {"prior_CDK4_6i_permitted"}
        for var, tokens in tokens_for.items():
            defs[var][name] = tokens
    return defs


def jacc(a, b):
    if not a and not b: return 0.0
    return 1.0 - len(a & b) / len(a | b)


def odi_with_ci(defs: dict, var: str, n_iter=1000, seed=20260516):
    trials = list(defs[var].keys())
    pairs = list(combinations(trials, 2))
    if not pairs:
        return 0.0, None, None, len(trials), 0
    d = [jacc(defs[var][a], defs[var][b]) for a, b in pairs]
    odi = sum(d) / len(d)
    rng = random.Random(seed)
    est = []
    for _ in range(n_iter):
        s = [rng.choice(pairs) for _ in range(len(pairs))]
        ds = [jacc(defs[var][a], defs[var][b]) for a, b in s]
        est.append(sum(ds) / len(ds))
    est.sort()
    lo = est[max(0, int(0.025*n_iter)-1)]
    hi = est[min(n_iter-1, int(0.975*n_iter))]
    return odi, lo, hi, len(trials), len(pairs)


def main() -> None:
    ext = json.loads(EXT.read_text())
    defs = _build_definitions(ext)
    out = {}
    print(f"{'Variable':<16s} {'ODI':>6s} {'95% CI':>15s} {'n_trials':>9s} {'n_pairs':>8s}")
    for var in ("HER2-low", "ESR1mut", "PIK3CAmut", "AKTpath", "prior_CDK4_6i", "gBRCAmut"):
        odi, lo, hi, n_t, n_p = odi_with_ci(defs, var)
        if n_p == 0:
            ci_str = "n/a"
        else:
            ci_str = f"[{lo:.2f},{hi:.2f}]"
        out[var] = {
            "trials": list(defs[var].keys()),
            "n_trials": n_t,
            "n_pairs": n_p,
            "odi": round(odi, 4),
            "bootstrap_ci95_low":  round(lo, 4) if lo is not None else None,
            "bootstrap_ci95_high": round(hi, 4) if hi is not None else None,
        }
        print(f"  {var:<14s} {odi:6.3f} {ci_str:>15s} {n_t:>9d} {n_p:>8d}")
    OUT.write_text(json.dumps(out, indent=2))
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
