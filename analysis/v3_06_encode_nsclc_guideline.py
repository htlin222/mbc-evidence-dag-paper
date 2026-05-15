"""v3_06_encode_nsclc_guideline.py
Encode the ESMO + ASCO + NCCN HR+/HER2- EGFR-mutant and ALK-rearranged
metastatic NSCLC decision tree.

Source: ESMO Clinical Practice Guideline for metastatic NSCLC (Hendriks et al.
Ann Oncol 2023 + 2024 updates); ASCO living guideline for NSCLC stage IV
non-driver and driver-positive (Hanna et al. 2021 update, Singh et al. 2023);
NCCN NSCLC v5.2024.

Each node:
  node_id, state, biomarker, recommended_classes (with grade),
  cited_trials (NCT), year, source
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "processed" / "v3_nsclc_decision_tree.json"
OUT.parent.mkdir(parents=True, exist_ok=True)

NODES = [
    # ===== EGFR-mutant section ============================================
    # N1: 1L common-sensitizing EGFR mutation (ex19del or L858R) -> osimertinib
    {
        "node_id": "N1",
        "state": "first-line",
        "biomarker": "EGFR-mut/EGFR-ex19del-or-L858R/NSCLC",
        "recommended_classes": [{"class": "EGFR TKI 3rd-gen (osimertinib)", "grade": "I-A"}],
        "cited_trials": ["NCT02296125"],  # FLAURA
        "year": 2018,
        "source": "ESMO+ASCO+NCCN",
    },
    # N2: 1L EGFR-mut -> 3rd-gen TKI + chemotherapy (FLAURA2)
    {
        "node_id": "N2",
        "state": "first-line",
        "biomarker": "EGFR-mut/NSCLC",
        "recommended_classes": [{"class": "EGFR TKI 3rd-gen + chemotherapy", "grade": "I-B"}],
        "cited_trials": ["NCT04035486"],  # FLAURA2
        "year": 2024,
        "source": "ESMO+ASCO+NCCN",
    },
    # N3: 1L EGFR-mut -> amivantamab + lazertinib (MARIPOSA)
    {
        "node_id": "N3",
        "state": "first-line",
        "biomarker": "EGFR-mut/NSCLC",
        "recommended_classes": [{"class": "EGFR TKI 3rd-gen + bispecific (amivantamab + lazertinib)", "grade": "I-B"}],
        "cited_trials": ["NCT04487080"],  # MARIPOSA
        "year": 2024,
        "source": "ASCO+NCCN",
    },
    # N4: 1L EGFR-mut -> 2nd-gen TKI (dacomitinib)
    {
        "node_id": "N4",
        "state": "first-line",
        "biomarker": "EGFR-mut/NSCLC",
        "recommended_classes": [{"class": "EGFR TKI 2nd-gen (afatinib/dacomitinib)", "grade": "II-B"}],
        "cited_trials": ["NCT01774721"],  # ARCHER 1050
        "year": 2017,
        "source": "ESMO+ASCO+NCCN",
    },
    # N5: 1L EGFR-mut -> 1st-gen TKI + chemo or anti-VEGF (NEJ026, etc.)
    {
        "node_id": "N5",
        "state": "first-line",
        "biomarker": "EGFR-mut/NSCLC",
        "recommended_classes": [{"class": "Bevacizumab + EGFR TKI", "grade": "II-B"},
                                 {"class": "Ramucirumab + EGFR TKI", "grade": "II-B"}],
        "cited_trials": [],  # NEJ026 not in our corpus by default
        "year": 2020,
        "source": "ESMO",
    },
    # N6: post-1st/2nd-gen EGFR TKI + T790M+ -> osimertinib (AURA3)
    {
        "node_id": "N6",
        "state": "post-EGFRTKI",
        "biomarker": "EGFR-mut/EGFR-T790M/NSCLC",
        "recommended_classes": [{"class": "EGFR TKI 3rd-gen (osimertinib)", "grade": "I-A"}],
        "cited_trials": ["NCT02151981"],  # AURA3 (corrected)
        "year": 2017,
        "source": "ESMO+ASCO+NCCN",
    },
    # N7: post-osimertinib (T790M-, MET-, MET amp-, etc.) -> amivantamab + chemo (MARIPOSA-2)
    {
        "node_id": "N7",
        "state": "post-osimertinib",
        "biomarker": "EGFR-mut/NSCLC",
        "recommended_classes": [{"class": "Amivantamab + chemotherapy", "grade": "I-B"}],
        "cited_trials": ["NCT04988295"],  # MARIPOSA-2
        "year": 2023,
        "source": "ESMO+NCCN",
    },
    # N8: post-osimertinib -> HER3-ADC (HERTHENA-Lung01)
    {
        "node_id": "N8",
        "state": "post-osimertinib",
        "biomarker": "EGFR-mut/NSCLC",
        "recommended_classes": [{"class": "HER3-ADC (patritumab deruxtecan)", "grade": "II-B"}],
        "cited_trials": ["NCT04619004"],  # HERTHENA-Lung01 (corrected)
        "year": 2023,
        "source": "NCCN",
    },
    # N9: post-osimertinib -> TROP2-ADC (TROPION-Lung01 mixed pop)
    {
        "node_id": "N9",
        "state": "post-osimertinib+post-chemo",
        "biomarker": "EGFR-mut/NSCLC",
        "recommended_classes": [{"class": "TROP2-ADC (datopotamab deruxtecan)", "grade": "II-C"}],
        "cited_trials": ["NCT04656652"],  # TROPION-Lung01 (corrected)
        "year": 2023,
        "source": "NCCN",
    },
    # N10: post-osimertinib + post-chemo -> platinum doublet chemo
    {
        "node_id": "N10",
        "state": "post-osimertinib",
        "biomarker": "EGFR-mut/NSCLC",
        "recommended_classes": [{"class": "Platinum doublet chemotherapy", "grade": "I-A"}],
        "cited_trials": [],  # standard of care; not a single pivotal trial
        "year": 2020,
        "source": "ESMO+ASCO+NCCN",
    },
    # N11: 1L EGFR ex20ins -> amivantamab (PAPILLON) - distinct from common-sens
    {
        "node_id": "N11",
        "state": "first-line",
        "biomarker": "EGFR-ex20ins/NSCLC",
        "recommended_classes": [{"class": "Amivantamab + chemotherapy", "grade": "I-B"}],
        "cited_trials": [],  # PAPILLON (NCT04538664) - may not be in corpus
        "year": 2024,
        "source": "ESMO+NCCN",
    },
    # N12: post-chemo EGFR ex20ins -> mobocertinib or amivantamab
    {
        "node_id": "N12",
        "state": "post-chemo",
        "biomarker": "EGFR-ex20ins/NSCLC",
        "recommended_classes": [{"class": "investigational (other)", "grade": "II-B"}],
        "cited_trials": [],
        "year": 2022,
        "source": "NCCN",
    },

    # ===== ALK-rearranged section ==========================================
    # N13: 1L ALK+ -> alectinib (ALEX)
    {
        "node_id": "N13",
        "state": "first-line",
        "biomarker": "ALK-rearranged/NSCLC",
        "recommended_classes": [{"class": "ALK TKI 2nd-gen (alectinib/brigatinib/ceritinib/ensartinib)", "grade": "I-A"}],
        "cited_trials": ["NCT02075840"],  # ALEX
        "year": 2017,
        "source": "ESMO+ASCO+NCCN",
    },
    # N14: 1L ALK+ -> brigatinib (ALTA-1L)
    {
        "node_id": "N14",
        "state": "first-line",
        "biomarker": "ALK-rearranged/NSCLC",
        "recommended_classes": [{"class": "ALK TKI 2nd-gen (alectinib/brigatinib/ceritinib/ensartinib)", "grade": "I-A"}],
        "cited_trials": ["NCT02737501"],  # ALTA-1L
        "year": 2020,
        "source": "ESMO+ASCO+NCCN",
    },
    # N15: 1L ALK+ -> lorlatinib (CROWN)
    {
        "node_id": "N15",
        "state": "first-line",
        "biomarker": "ALK-rearranged/NSCLC",
        "recommended_classes": [{"class": "ALK TKI 3rd-gen (lorlatinib)", "grade": "I-A"}],
        "cited_trials": ["NCT03052608"],  # CROWN
        "year": 2020,
        "source": "ESMO+ASCO+NCCN",
    },
    # N16: 1L ALK+ -> crizotinib (PROFILE 1014) - older
    {
        "node_id": "N16",
        "state": "first-line",
        "biomarker": "ALK-rearranged/NSCLC",
        "recommended_classes": [{"class": "ALK TKI 1st-gen (crizotinib)", "grade": "II-B"}],
        "cited_trials": ["NCT01154140"],  # PROFILE 1014
        "year": 2014,
        "source": "ESMO+ASCO+NCCN",
    },
    # N17: post-crizotinib -> 2nd-gen ALK TKI (ascertain salvage)
    {
        "node_id": "N17",
        "state": "post-ALKTKI",
        "biomarker": "ALK-rearranged/NSCLC",
        "recommended_classes": [{"class": "ALK TKI 2nd-gen (alectinib/brigatinib/ceritinib/ensartinib)", "grade": "I-A"}],
        "cited_trials": [],
        "year": 2017,
        "source": "ESMO+ASCO+NCCN",
    },
    # N18: post-2nd-gen ALK TKI -> lorlatinib
    {
        "node_id": "N18",
        "state": "post-ALKTKI",
        "biomarker": "ALK-rearranged/NSCLC",
        "recommended_classes": [{"class": "ALK TKI 3rd-gen (lorlatinib)", "grade": "I-A"}],
        "cited_trials": [],
        "year": 2018,
        "source": "ESMO+ASCO+NCCN",
    },
    # N19: post-lorlatinib + ALK G1202R / resistance mutations -> rechallenge or chemo
    {
        "node_id": "N19",
        "state": "post-ALKTKI",
        "biomarker": "ALK-rearranged/ALK-resistance-mut/NSCLC",
        "recommended_classes": [{"class": "Platinum doublet chemotherapy", "grade": "II-C"}],
        "cited_trials": [],
        "year": 2022,
        "source": "NCCN",
    },
    # N20: ALK+ + brain mets -> alectinib or lorlatinib (CNS-active)
    {
        "node_id": "N20",
        "state": "first-line+brain-mets",
        "biomarker": "ALK-rearranged/NSCLC",
        "recommended_classes": [{"class": "ALK TKI 3rd-gen (lorlatinib)", "grade": "I-A"},
                                 {"class": "ALK TKI 2nd-gen (alectinib/brigatinib/ceritinib/ensartinib)", "grade": "I-A"}],
        "cited_trials": ["NCT03052608", "NCT02075840"],
        "year": 2020,
        "source": "ESMO+ASCO+NCCN",
    },
    # N21: post-osimertinib + MET amp -> savolitinib + osimertinib (SAVANNAH)
    {
        "node_id": "N21",
        "state": "post-osimertinib",
        "biomarker": "EGFR-mut/MET-amp/NSCLC",
        "recommended_classes": [{"class": "investigational (other)", "grade": "II-C"}],
        "cited_trials": [],  # SAVANNAH may be in corpus
        "year": 2024,
        "source": "NCCN",
    },
    # N22: EGFR-mut + brain mets 1L -> osimertinib (FLAURA brain subgroup)
    {
        "node_id": "N22",
        "state": "first-line+brain-mets",
        "biomarker": "EGFR-mut/NSCLC",
        "recommended_classes": [{"class": "EGFR TKI 3rd-gen (osimertinib)", "grade": "I-A"}],
        "cited_trials": ["NCT02296125"],  # FLAURA brain subgroup
        "year": 2018,
        "source": "ESMO+ASCO+NCCN",
    },
    # N23: post-osimertinib + post-amivantamab -> investigator's choice
    {
        "node_id": "N23",
        "state": "post-osimertinib+post-amivantamab",
        "biomarker": "EGFR-mut/NSCLC",
        "recommended_classes": [{"class": "investigational (other)", "grade": "II-C"}],
        "cited_trials": [],
        "year": 2024,
        "source": "ASCO",
    },
    # N24: EGFR-mut + post-chemo + post-osimertinib -> docetaxel-based salvage
    {
        "node_id": "N24",
        "state": "post-osimertinib+post-chemo",
        "biomarker": "EGFR-mut/NSCLC",
        "recommended_classes": [{"class": "Platinum doublet chemotherapy", "grade": "II-B"}],
        "cited_trials": [],
        "year": 2020,
        "source": "ASCO+NCCN",
    },
    # N25: 1L EGFR-mut + smoking history (TP53 co-mutation) -> osimertinib + chemo (FLAURA2 subgroup)
    {
        "node_id": "N25",
        "state": "first-line+poor-prognosis",
        "biomarker": "EGFR-mut/NSCLC",
        "recommended_classes": [{"class": "EGFR TKI 3rd-gen + chemotherapy", "grade": "I-B"}],
        "cited_trials": ["NCT04035486"],  # FLAURA2 high-risk subgroup
        "year": 2024,
        "source": "NCCN",
    },
]


def main() -> None:
    OUT.write_text(json.dumps(NODES, indent=2))
    from collections import Counter
    src_counts = Counter(n["source"] for n in NODES)
    print(f"Wrote {len(NODES)} NSCLC guideline decision nodes")
    print("By source:")
    for s, n in src_counts.most_common():
        print(f"  {s}: {n}")


if __name__ == "__main__":
    main()
