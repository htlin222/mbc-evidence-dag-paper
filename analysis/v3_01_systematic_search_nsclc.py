"""v3_01_systematic_search_nsclc.py
Systematic ClinicalTrials.gov v2 search for EGFR-mutant + ALK-rearranged
NSCLC pivotal trials, per prereg-v3 (commit 4b5bf1a).

Frozen at the prereg commit; no outcome data observed yet.
"""
from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "raw" / "ctgov_nsclc_systematic_v3.json"
OUT.parent.mkdir(parents=True, exist_ok=True)

API = "https://clinicaltrials.gov/api/v2/studies"

# Two-track query: EGFR-mutant and ALK-rearranged. The OR is encoded as a
# disjunction in query.term to keep a single pagination loop.
QUERY = {
    "query.cond":     "non-small cell lung cancer OR NSCLC OR non-small-cell lung carcinoma",
    "query.intr":     "(drug OR biological)",
    "query.term":     "((EGFR mutation OR EGFR-mutant OR EGFR mutant OR EGFR positive) "
                       "OR (ALK rearrangement OR ALK-rearranged OR ALK-positive OR ALK positive)) "
                       "AND (metastatic OR advanced) "
                       "AND NOT (adjuvant OR neoadjuvant)",
    "filter.advanced": "AREA[Phase](PHASE2 OR PHASE3)",
    "pageSize":       "100",
    "format":         "json",
}


def fetch_page(token: str | None) -> dict:
    params = dict(QUERY)
    if token:
        params["pageToken"] = token
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "mbc-evidence-dag-v3/0.1"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> None:
    all_studies: list[dict] = []
    token: str | None = None
    page = 0
    while True:
        page += 1
        data = fetch_page(token)
        studies = data.get("studies", [])
        all_studies.extend(studies)
        print(f"  page {page:3d}: +{len(studies):3d} studies (total {len(all_studies)})", flush=True)
        token = data.get("nextPageToken")
        if not token:
            break
        if page > 60:
            print("  hit page cap; stopping")
            break
        time.sleep(0.25)
    OUT.write_text(json.dumps({"studies": all_studies}, indent=2))
    print(f"wrote {len(all_studies)} NSCLC studies to {OUT}")


if __name__ == "__main__":
    main()
