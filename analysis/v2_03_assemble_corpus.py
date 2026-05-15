"""v2_03_assemble_corpus.py
Assemble the final v2 corpus: systematic-search candidates + supplementary
v1.0.0 guideline-cited trials missed by the systematic search.

Per prereg-v2 (commit 085ae54) and amendment v2.1 (commit 079b540), the v2
corpus is the union of:
  (a) studies passing the systematic-search filter (74 trials), and
  (b) v1.0.0 corpus trials that failed the systematic filter but are
      ESMO/ASCO/NCCN-cited pivotal trials (6 trials):
        NCT01740427 PALOMA-2     (failed F3 — started 2013)
        NCT02000622 OlympiAD     (not in raw API search; gBRCAm scope)
        NCT02437318 SOLAR-1      (not in raw API search; query.term miss)
        NCT03778931 EMERALD      (failed F5 — query keyword miss)
        NCT04191499 INAVO120     (not in raw API search)
        NCT05169567 postMONARCH  (failed F5 — query keyword miss)

The supplementary 6 are tagged `provenance: "v1_supplementary"` and
disclosed in the prereg-v2 deviation log. Output: data/processed/v2_corpus_ncts.json
"""
from __future__ import annotations

import json
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAND = ROOT / "data" / "processed" / "candidate_corpus.json"
RAW = ROOT / "data" / "raw" / "ctgov_systematic_v2.json"
OUT = ROOT / "data" / "processed" / "v2_corpus_ncts.json"

V1_SUPPLEMENTARY = [
    ("NCT01740427", "PALOMA-2"),
    ("NCT02000622", "OlympiAD"),
    ("NCT02437318", "SOLAR-1"),
    ("NCT03778931", "EMERALD"),
    ("NCT04191499", "INAVO120"),
    ("NCT05169567", "postMONARCH"),
]


def fetch_supplementary(nct: str) -> dict:
    url = f"https://clinicaltrials.gov/api/v2/studies/{nct}"
    req = urllib.request.Request(url, headers={"User-Agent": "mbc-evidence-dag-v2/0.3"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> None:
    sys_studies = json.loads(CAND.read_text())["studies"]
    sys_ncts = {s["protocolSection"]["identificationModule"]["nctId"] for s in sys_studies}
    corpus: list[dict] = []
    for s in sys_studies:
        nct = s["protocolSection"]["identificationModule"]["nctId"]
        corpus.append({"nct_id": nct, "provenance": "systematic_search", "payload": s})
    # supplementary
    for nct, name in V1_SUPPLEMENTARY:
        if nct in sys_ncts:
            continue
        print(f"  fetching supplementary {nct} ({name})", flush=True)
        try:
            payload = fetch_supplementary(nct)
            corpus.append({"nct_id": nct, "provenance": "v1_supplementary",
                           "trial_name_hint": name, "payload": payload})
        except Exception as e:
            print(f"    FAIL: {e}")
        time.sleep(0.25)
    OUT.write_text(json.dumps({
        "n_systematic": sum(1 for c in corpus if c["provenance"] == "systematic_search"),
        "n_supplementary": sum(1 for c in corpus if c["provenance"] == "v1_supplementary"),
        "n_total": len(corpus),
        "trials": [{"nct_id": c["nct_id"], "provenance": c["provenance"],
                    "trial_name_hint": c.get("trial_name_hint")} for c in corpus],
    }, indent=2))
    # Also save the full payloads to a separate file
    full = ROOT / "data" / "raw" / "v2_corpus_full.json"
    full.write_text(json.dumps(corpus, indent=2))
    print(f"systematic: {sum(1 for c in corpus if c['provenance'] == 'systematic_search')}")
    print(f"supplementary: {sum(1 for c in corpus if c['provenance'] == 'v1_supplementary')}")
    print(f"total: {len(corpus)} -> {OUT}")


if __name__ == "__main__":
    main()
