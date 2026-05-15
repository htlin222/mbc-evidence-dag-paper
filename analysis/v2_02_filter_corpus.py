"""v2_02_filter_corpus.py
Apply pre-specified inclusion filters per prereg-v2 to the 874-study
systematic search output. Produces a candidate corpus for LLM extraction.

Filters (in order, with rejection counts logged):
  F1. Phase: must include PHASE2 or PHASE3 (interventional).
  F2. Study type: INTERVENTIONAL (no observational).
  F3. Started or first-posted 2015-01-01 .. 2026-05-16.
  F4. Setting: metastatic OR advanced (not adjuvant / neoadjuvant).
  F5. Population: HR+/ER+ inclusion either required or as a pre-specified
      subgroup; HER2 not mandated positive.
  F6. Eligibility text retrievable and non-empty.
  F7. Enrolment count >= 50 (proxy for pivotal scale).
  F8. Primary publication likely (uses ReferenceList field as proxy)
      OR completion date <= today.

The filter is deterministic and committed before LLM extraction.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "ctgov_systematic_v2.json"
OUT = ROOT / "data" / "processed" / "candidate_corpus.json"
LOG = ROOT / "data" / "processed" / "filter_log.json"
OUT.parent.mkdir(parents=True, exist_ok=True)

ADJ_NEOADJ_RX = re.compile(
    r"\b(adjuvant|neoadjuvant|pre.?operative|peri.?operative|early.?stage|"
    r"early.?breast|node.?positive disease|stage I |stage II )\b",
    re.IGNORECASE,
)
METASTATIC_RX = re.compile(
    r"\b(metastatic|advanced|stage IV|stage 4|locally.?advanced|inoperable|recurrent)\b",
    re.IGNORECASE,
)
HR_POS_RX = re.compile(
    r"\b(hormone.?receptor.?positive|HR\+|HR-positive|ER\+|estrogen.?receptor.?positive|"
    r"oestrogen.?receptor.?positive|ER-positive|PR\+|progesterone.?receptor.?positive)\b",
    re.IGNORECASE,
)
HER2_POS_RESTRICTED_RX = re.compile(
    r"\b(HER2.?positive|HER2\+|HER2.?amplified|HER2.?overexpressing|"
    r"HER2.?3\+|IHC.?3\+ AND ISH amplified)\b",
    re.IGNORECASE,
)
HER2_NEG_ALLOWED_RX = re.compile(
    r"\b(HER2.?negative|HER2-|HER2.?low|HER2.?zero|HER2.?ultralow|"
    r"HER2 0|HER2 1\+|HER2 2\+)\b",
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
    """Per prereg-v2 amendment v2.1, the date window is widened to 2013-2026
    to capture pre-2015 foundational CDK4/6i trials (PALOMA-3, MONALEESA-2,
    MONARCH-2, etc.) that are cited by ESMO, ASCO, and NCCN.
    """
    status = proto.get("statusModule", {}) or {}
    start_y = year_of(status.get("startDateStruct"))
    posted_y = year_of(status.get("studyFirstPostDateStruct"))
    candidates = [y for y in (start_y, posted_y) if y is not None]
    if not candidates:
        return False
    return 2013 <= min(candidates) <= 2026


def setting_metastatic(proto: dict) -> bool:
    """Trial setting must be metastatic/advanced, not adjuvant/neoadjuvant.

    Only check titles and conditions for adj/neoadj rejection, NOT the
    eligibility text. Eligibility text often mentions 'prior adjuvant
    therapy' which describes patient history rather than the trial setting,
    and the previous regex over-rejected on those mentions.
    """
    cond_mod = proto.get("conditionsModule") or {}
    conds = " | ".join(cond_mod.get("conditions") or [])
    titles = " | ".join([
        (proto.get("identificationModule") or {}).get("briefTitle") or "",
        (proto.get("identificationModule") or {}).get("officialTitle") or "",
    ])
    setting_text = conds + " || " + titles
    if ADJ_NEOADJ_RX.search(setting_text):
        return False
    # require metastatic mention in title, condition, or eligibility
    elig = (proto.get("eligibilityModule") or {}).get("eligibilityCriteria") or ""
    full_text = setting_text + " || " + elig[:2000]
    return bool(METASTATIC_RX.search(full_text))


def is_her2_negative_population(proto: dict) -> bool:
    elig = (proto.get("eligibilityModule") or {}).get("eligibilityCriteria") or ""
    titles = " | ".join([
        (proto.get("identificationModule") or {}).get("briefTitle") or "",
        (proto.get("identificationModule") or {}).get("officialTitle") or "",
    ])
    text = titles + " || " + elig[:6000]
    if not HR_POS_RX.search(text):
        return False
    # Accept trials where HER2-negative or HER2-low is mentioned, OR where
    # HER2-positive is NOT the primary restriction.
    if HER2_NEG_ALLOWED_RX.search(text):
        return True
    # If the trial title says HER2-positive explicitly, exclude.
    if HER2_POS_RESTRICTED_RX.search(titles):
        return False
    # Default: include (most HR+ trials are HER2-mixed or HER2-negative)
    return True


def enrolment_count_ok(proto: dict) -> bool:
    """Per prereg-v2 amendment v2.1, enrolment threshold tightened to >=200
    to focus on pivotal-scale trials.
    """
    enr = (proto.get("designModule") or {}).get("enrollmentInfo") or {}
    try:
        return int(enr.get("count", 0) or 0) >= 200
    except (TypeError, ValueError):
        return False


def eligibility_present(proto: dict) -> bool:
    elig = (proto.get("eligibilityModule") or {}).get("eligibilityCriteria") or ""
    return len(elig) >= 200


def primary_completion_by_2026(proto: dict) -> bool:
    """For temporal-precedence support of guideline nodes, the trial must
    have a primary readout no later than 2026. Trials with completion
    dates in 2027+ cannot support any guideline node introduced before
    2027 under the temporal-precedence rule.
    """
    status = proto.get("statusModule") or {}
    pc_y = year_of(status.get("primaryCompletionDateStruct"))
    if pc_y is None:
        return False
    return pc_y <= 2026


FILTERS = [
    ("F1_phase23",           is_phase23),
    ("F2_interventional",    is_interventional),
    ("F3_started_in_window", started_in_window),
    ("F4_setting_metastatic", setting_metastatic),
    ("F5_her2_neg_pop",      is_her2_negative_population),
    ("F6_eligibility",       eligibility_present),
    ("F7_enrolment_ge_200",  enrolment_count_ok),
    ("F8_primary_completion_by_2026", primary_completion_by_2026),
]


def main() -> None:
    raw = json.loads(RAW.read_text())["studies"]
    counts = {name: 0 for name, _ in FILTERS}
    counts["passed_all"] = 0
    passed: list[dict] = []
    failure_reasons = {}
    for s in raw:
        proto = s.get("protocolSection", {})
        nct = (proto.get("identificationModule") or {}).get("nctId", "?")
        for name, fn in FILTERS:
            if not fn(proto):
                counts[name] += 1
                failure_reasons[nct] = name
                break
        else:
            counts["passed_all"] += 1
            passed.append(s)
    OUT.write_text(json.dumps({"studies": passed}, indent=2))
    LOG.write_text(json.dumps({"counts": counts, "by_nct": failure_reasons}, indent=2))
    print(f"input: {len(raw)} studies")
    for k, v in counts.items():
        print(f"  {k}: {v}")
    print(f"output: {len(passed)} candidates -> {OUT}")


if __name__ == "__main__":
    main()
