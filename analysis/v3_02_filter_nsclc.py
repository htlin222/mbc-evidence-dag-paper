"""v3_02_filter_nsclc.py
Apply pre-specified inclusion filters per prereg-v3 to the NSCLC candidate
corpus. Eight filters, including NSCLC-specific biomarker filter (EGFR OR ALK).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "ctgov_nsclc_systematic_v3.json"
OUT = ROOT / "data" / "processed" / "nsclc_candidate_corpus.json"
LOG = ROOT / "data" / "processed" / "nsclc_filter_log.json"
OUT.parent.mkdir(parents=True, exist_ok=True)

ADJ_NEOADJ_RX = re.compile(
    r"\b(adjuvant|neoadjuvant|pre.?operative|peri.?operative|early.?stage|"
    r"resectable|stage I |stage II )\b",
    re.IGNORECASE,
)
METASTATIC_RX = re.compile(
    r"\b(metastatic|advanced|stage IV|stage 4|locally.?advanced|inoperable|recurrent)\b",
    re.IGNORECASE,
)
EGFR_OR_ALK_RX = re.compile(
    r"(EGFR.?mutation|EGFR.?mutant|EGFR.?positive|EGFR.?T790M|EGFR.?ex19|EGFR.?L858R|"
    r"EGFR.?exon.?19|EGFR.?exon.?20|EGFR.?ex20|"
    r"\bex20ins\b|\bexon.?20.?insertion|\bEGFR.?ex20|"  # v3 round-1 fix: capture PAPILLON-style 'Exon 20ins'
    r"ALK.?rearrang|ALK.?translocat|"
    r"ALK.?positive|ALK.?mutat|ALK.?fusion|crizotinib|alectinib|brigatinib|lorlatinib|"
    r"osimertinib|gefitinib|erlotinib|afatinib|dacomitinib|amivantamab|lazertinib)",
    re.IGNORECASE,
)
NSCLC_RX = re.compile(
    r"\b(NSCLC|non.?small.?cell|adenocarcinoma|squamous.cell.lung)\b",
    re.IGNORECASE,
)


def is_phase23(proto: dict) -> bool:
    phases = (proto.get("designModule") or {}).get("phases") or []
    return any(p in {"PHASE2", "PHASE3"} for p in phases)


def is_interventional(proto: dict) -> bool:
    return (proto.get("designModule") or {}).get("studyType") == "INTERVENTIONAL"


def year_of(date_field: dict | None) -> int | None:
    if not date_field:
        return None
    d = date_field.get("date", "")
    if len(d) >= 4 and d[:4].isdigit():
        return int(d[:4])
    return None


def started_in_window(proto: dict) -> bool:
    """Per prereg-v3: 2013-2026 (same as v2 amendment v2.1)."""
    status = proto.get("statusModule", {}) or {}
    start_y = year_of(status.get("startDateStruct"))
    posted_y = year_of(status.get("studyFirstPostDateStruct"))
    candidates = [y for y in (start_y, posted_y) if y is not None]
    if not candidates:
        return False
    return 2013 <= min(candidates) <= 2026


def is_nsclc_metastatic(proto: dict) -> bool:
    cond_mod = proto.get("conditionsModule") or {}
    conds = " | ".join(cond_mod.get("conditions") or [])
    titles = " | ".join([
        (proto.get("identificationModule") or {}).get("briefTitle") or "",
        (proto.get("identificationModule") or {}).get("officialTitle") or "",
    ])
    setting_text = conds + " || " + titles
    if ADJ_NEOADJ_RX.search(setting_text):
        return False
    if not NSCLC_RX.search(setting_text):
        return False
    elig = (proto.get("eligibilityModule") or {}).get("eligibilityCriteria") or ""
    full = setting_text + " || " + elig[:2000]
    return bool(METASTATIC_RX.search(full))


def is_egfr_or_alk(proto: dict) -> bool:
    elig = (proto.get("eligibilityModule") or {}).get("eligibilityCriteria") or ""
    titles = " | ".join([
        (proto.get("identificationModule") or {}).get("briefTitle") or "",
        (proto.get("identificationModule") or {}).get("officialTitle") or "",
    ])
    text = titles + " || " + elig[:6000]
    return bool(EGFR_OR_ALK_RX.search(text))


def eligibility_present(proto: dict) -> bool:
    elig = (proto.get("eligibilityModule") or {}).get("eligibilityCriteria") or ""
    return len(elig) >= 200


def enrolment_count_ok(proto: dict) -> bool:
    """Per prereg-v3: >=100 (lower than v2 mBC's 200 because NSCLC biomarker-
    enriched trials are commonly smaller)."""
    enr = (proto.get("designModule") or {}).get("enrollmentInfo") or {}
    try:
        return int(enr.get("count", 0) or 0) >= 100
    except (TypeError, ValueError):
        return False


def primary_completion_by_2026(proto: dict) -> bool:
    status = proto.get("statusModule") or {}
    pc_y = year_of(status.get("primaryCompletionDateStruct"))
    if pc_y is None:
        return False
    return pc_y <= 2026


FILTERS = [
    ("F1_phase23",           is_phase23),
    ("F2_interventional",    is_interventional),
    ("F3_started_in_window", started_in_window),
    ("F4_nsclc_metastatic",  is_nsclc_metastatic),
    ("F5_egfr_or_alk",       is_egfr_or_alk),
    ("F6_eligibility",       eligibility_present),
    ("F7_enrolment_ge_100",  enrolment_count_ok),
    ("F8_completion_by_2026", primary_completion_by_2026),
]


def main() -> None:
    raw = json.loads(RAW.read_text())["studies"]
    counts = {name: 0 for name, _ in FILTERS}
    counts["passed_all"] = 0
    passed: list[dict] = []
    by_nct: dict = {}
    for s in raw:
        proto = s.get("protocolSection", {})
        nct = (proto.get("identificationModule") or {}).get("nctId", "?")
        for name, fn in FILTERS:
            if not fn(proto):
                counts[name] += 1
                by_nct[nct] = name
                break
        else:
            counts["passed_all"] += 1
            passed.append(s)
    OUT.write_text(json.dumps({"studies": passed}, indent=2))
    LOG.write_text(json.dumps({"counts": counts, "by_nct": by_nct}, indent=2))
    print(f"input: {len(raw)} studies")
    for k, v in counts.items():
        print(f"  {k}: {v}")
    print(f"output: {len(passed)} candidates -> {OUT}")


if __name__ == "__main__":
    main()
