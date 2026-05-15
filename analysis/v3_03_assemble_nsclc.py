"""v3_03_assemble_nsclc.py
Assemble final NSCLC corpus: systematic search + supplementary v3 round-0
trials missed by the systematic pull. Disclosed before extraction.
"""
from __future__ import annotations

import json
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAND = ROOT / "data" / "processed" / "nsclc_candidate_corpus.json"
OUT = ROOT / "data" / "processed" / "nsclc_corpus_ncts.json"
FULL = ROOT / "data" / "raw" / "nsclc_corpus_full.json"

# Key pivotal NSCLC trials missing from systematic search; verified by spot-check.
SUPPLEMENTARY = [
    ("NCT02788279", "AURA3"),               # osimertinib 2L post-T790M
    ("NCT05009836", "HERTHENA-Lung01"),     # HER3-DXd post-osimertinib
    ("NCT04644237", "TROPION-Lung01"),      # datopotamab deruxtecan
    ("NCT01154140", "PROFILE 1014"),        # crizotinib 1L ALK+
    ("NCT04379635", "FLAURA-CNS"),          # osimertinib CNS-focused
]


def fetch_one(nct: str) -> dict:
    url = f"https://clinicaltrials.gov/api/v2/studies/{nct}"
    req = urllib.request.Request(url, headers={"User-Agent": "mbc-evidence-dag-v3/0.3"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> None:
    sys_studies = json.loads(CAND.read_text())["studies"]
    sys_ncts = {s["protocolSection"]["identificationModule"]["nctId"] for s in sys_studies}
    corpus: list[dict] = []
    for s in sys_studies:
        nct = s["protocolSection"]["identificationModule"]["nctId"]
        corpus.append({"nct_id": nct, "provenance": "nsclc_systematic", "payload": s})
    for nct, name in SUPPLEMENTARY:
        if nct in sys_ncts:
            continue
        print(f"  fetching supplementary {nct} ({name})", flush=True)
        try:
            payload = fetch_one(nct)
            corpus.append({"nct_id": nct, "provenance": "nsclc_supplementary",
                           "trial_name_hint": name, "payload": payload})
        except Exception as e:
            print(f"    FAIL: {e}")
        time.sleep(0.25)
    OUT.write_text(json.dumps({
        "n_systematic": sum(1 for c in corpus if c["provenance"] == "nsclc_systematic"),
        "n_supplementary": sum(1 for c in corpus if c["provenance"] == "nsclc_supplementary"),
        "n_total": len(corpus),
        "trials": [{"nct_id": c["nct_id"], "provenance": c["provenance"],
                    "trial_name_hint": c.get("trial_name_hint")} for c in corpus],
    }, indent=2))
    FULL.write_text(json.dumps(corpus, indent=2))
    print(f"systematic: {sum(1 for c in corpus if c['provenance'] == 'nsclc_systematic')}")
    print(f"supplementary: {sum(1 for c in corpus if c['provenance'] == 'nsclc_supplementary')}")
    print(f"total: {len(corpus)}")


if __name__ == "__main__":
    main()
