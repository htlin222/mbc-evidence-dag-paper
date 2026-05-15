"""01_fetch_trials.py
Fetch HR+/HER2- metastatic breast cancer pivotal trials from ClinicalTrials.gov v2.

Freeze date: 2026-05-16 (recorded in docs/prereg.md).
Output: data/raw/ctgov_trials.json (full registry payloads for documented pivotal trials).
"""
from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data" / "raw"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT = OUT_DIR / "ctgov_trials.json"

API = "https://clinicaltrials.gov/api/v2/studies/{nct}"

# 14 pivotal trials selected as the documented HR+/HER2- mBC corpus (2015-2024).
# This list extends the 6-trial pilot in docs/prereg.md with eight additional
# pivotal trials drawn from ESMO 2024 reference list and ASCO 2022 guideline
# update reference list. The freeze date of this list is 2026-05-16; later
# extensions go into v2 of the corpus, not retroactive edits.
NCT_IDS = [
    # NCT identifiers verified against ClinicalTrials.gov briefTitle and
    # conditionsModule. Round 2 review caught 4 NCT-misidentifications in
    # the previous list (PALOMA-2, MONARCH-3, MONALEESA-3, MONALEESA-7);
    # this is the corrected canonical list. PALLAS (NCT02513394, adjuvant)
    # and monarcHER (NCT02675231, HR+/HER2+) are EXCLUDED as out-of-scope.
    "NCT01942135",  # PALOMA-3       (palbociclib + fulvestrant, post-endocrine)
    "NCT01958021",  # MONALEESA-2    (ribociclib + letrozole, first-line)
    "NCT01740427",  # PALOMA-2       (palbociclib + letrozole, first-line)
    "NCT02000622",  # OlympiAD       (olaparib, gBRCA mBC)
    "NCT02107703",  # MONARCH-2      (abemaciclib + fulvestrant, post-endocrine)
    "NCT02246621",  # MONARCH-3      (abemaciclib + NSAI, first-line postmen)
    "NCT02278120",  # MONALEESA-7    (ribociclib in premenopausal, first-line)
    "NCT02422615",  # MONALEESA-3    (ribociclib + fulvestrant, 1L and 2L)
    "NCT02437318",  # SOLAR-1        (alpelisib + fulvestrant, PIK3CAmut, post-AI)
    "NCT03734029",  # DESTINY-Breast04 (T-DXd, HER2-low, post-chemo)
    "NCT03778931",  # EMERALD        (elacestrant vs SoC, post-CDK4/6i)
    "NCT03901339",  # TROPiCS-02     (sacituzumab govitecan, post-CDK4/6i + post-chemo)
    "NCT04191499",  # INAVO120       (inavolisib + palbo + fulv, PIK3CAmut, endo-resistant)
    "NCT04305496",  # CAPItello-291  (capivasertib + fulvestrant, mixed pre/post-CDK4/6i)
    "NCT04494425",  # DESTINY-Breast06 (T-DXd, HER2-low/ultralow, post-endocrine)
    "NCT05169567",  # postMONARCH    (abemaciclib + fulv after CDK4/6i progression)
]


def fetch_one(nct: str) -> dict:
    url = API.format(nct=urllib.parse.quote(nct))
    req = urllib.request.Request(url, headers={"User-Agent": "mbc-evidence-dag/0.1"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> None:
    out: dict[str, dict] = {}
    for nct in NCT_IDS:
        print(f"  fetching {nct}", flush=True)
        try:
            out[nct] = fetch_one(nct)
        except Exception as e:
            print(f"    FAIL {nct}: {e}")
            out[nct] = {"error": str(e)}
        time.sleep(0.25)
    OUT.write_text(json.dumps(out, indent=2))
    n_ok = sum(1 for v in out.values() if "error" not in v)
    print(f"saved {n_ok}/{len(NCT_IDS)} trials to {OUT}")


if __name__ == "__main__":
    main()
