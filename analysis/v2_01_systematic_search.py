"""v2_01_systematic_search.py
Systematic ClinicalTrials.gov v2 search for HR+/HER2- mBC pivotal trials.

Per prereg-v2 (commit 085ae54), the search criteria are:
  - condition: breast cancer / breast neoplasm
  - intervention type: drug or biological
  - phase: phase 2 or phase 3 (interventional)
  - first-posted date: 2015-01-01 to 2026-05-16
  - eligibility text mentions HR+/ER+/estrogen receptor positive
    AND metastatic/advanced
  - excluded: adjuvant, neoadjuvant settings
  - excluded: HER2-positive primary populations
    (HER2-low and HER2-zero are included since they fall under HR+/HER2-)

The search yields a candidate list; downstream filtering happens in
v2_02_filter_corpus.py against the LLM-extracted schema.
"""
from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "raw" / "ctgov_systematic_v2.json"
OUT.parent.mkdir(parents=True, exist_ok=True)

API = "https://clinicaltrials.gov/api/v2/studies"

# Search query — encoded against CT.gov v2 API expr syntax.
QUERY = {
    "query.cond":     "breast cancer OR breast neoplasm",
    "query.intr":     "(drug OR biological)",
    "query.term":     "(hormone receptor positive OR estrogen receptor positive OR HR+ OR ER+) AND (metastatic OR advanced) AND NOT (adjuvant OR neoadjuvant)",
    "filter.advanced": "AREA[Phase](PHASE2 OR PHASE3)",
    "pageSize":       "100",
    "format":         "json",
}


def fetch_page(token: str | None) -> dict:
    params = dict(QUERY)
    if token:
        params["pageToken"] = token
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "mbc-evidence-dag-v2/0.2"})
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
        if page > 50:  # safety cap
            print("  hit page cap, stopping")
            break
        time.sleep(0.25)
    OUT.write_text(json.dumps({"studies": all_studies}, indent=2))
    print(f"wrote {len(all_studies)} studies to {OUT}")


if __name__ == "__main__":
    main()
