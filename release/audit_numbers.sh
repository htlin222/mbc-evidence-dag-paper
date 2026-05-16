#!/bin/bash
# audit_numbers.sh — fail if any stale v3 literal appears in release files.
# Source of truth: release/canonical_numbers.md
set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# Forbidden stale literals (v3.0.0 pre-R1 numbers + v3 R1/R2 stale)
FORBIDDEN=(
    "P = 0.0004"
    "P=0.0004"
    "P = 0.0009"
    "P = 0.0001"
    "EFDPR 0.48"
    "EFDPR = 0.48"
    "50-node"
    "n = 50"
    "261 trials"
    "261-trial"
    "210 edges"
    "180 NSCLC trials"
    "180 trials"
    "12 of 17 EGFR"
    "12 EGFR-mutant"
    "0.71.*evidence-free"
    "P = 0.10"
    "EFDPR 0.71"
)

# Files to audit
FILES=(
    manuscript/paper_A_clinical_v3.tex
    manuscript/paper_B_methods_v3.tex
    release/RELEASE_NOTES_v3.0.0.md
    release/SUBMISSION_ROADMAP.md
    release/submission_kit_paperB_medrxiv/SUBMISSION_CHECKLIST.md
    release/submission_kit_paperB_medrxiv/medrxiv_metadata.md
    release/submission_kit_paperB_medrxiv/cover_letter_medrxiv.md
    release/submission_kit_paperB_medrxiv/AUDIT_REPORT.md
    release/submission_plan_paperA_jcopo/POLISH_PLAN_14_DAYS.md
    release/submission_plan_paperA_jcopo/cover_letter_jcopo_draft.md
    release/submission_plan_paperA_jcopo/AUDIT_REPORT.md
)

found=0
for forbidden in "${FORBIDDEN[@]}"; do
    for f in "${FILES[@]}"; do
        [ -f "$f" ] || continue
        if matches=$(grep -nE "$forbidden" "$f" 2>/dev/null); then
            echo "STALE: $f"
            echo "$matches" | sed 's/^/    /'
            found=1
        fi
    done
done

if [ $found -eq 1 ]; then
    echo
    echo "FAIL: stale literals found above. See release/canonical_numbers.md for ground truth."
    exit 1
fi
echo "PASS: no stale literals found across $(echo "${FILES[@]}" | wc -w) files."
