# LLM Extraction Protocol — frozen schema v1.0

Used by both annotator A (Claude) and annotator B (Codex / GPT-5). Both
annotators receive the **same** trial inputs (from
`data/processed/v2_extraction_inputs.jsonl`) and produce the **same** JSON
schema.

## Output schema (frozen v1.0)

For each trial, output a JSON object with these fields. Use `null` when the
trial's eligibility text is silent on the field; use `true`/`false` when the
eligibility text gives a clear yes/no answer.

```json
{
  "nct_id": "NCT0xxxxxxx",
  "trial_name": "TRIAL-ACRONYM or canonical trial name (string)",
  "prior_state": {
    "post_endo":            true | false | null,   // requires PRIOR endocrine therapy in metastatic
    "post_cdk46i":          true | false | null,   // requires PRIOR CDK4/6i in metastatic
    "post_chemo_metastatic_min": int | null,        // minimum prior chemo lines required in metastatic
    "endo_resistance_window_months": int | null,    // months from last adjuvant endo to disease event
    "menopausal_status":    "pre" | "post" | "any" | null
  },
  "excluded": {
    "post_cdk46i":          true | false | null,   // explicit exclusion of prior CDK4/6i
    "post_chemo_metastatic_any": true | false | null,
    "post_endo_metastatic_any":  true | false | null,
    "post_cdk46i_metastatic":    true | false | null
  },
  "biomarker": {
    "hr_pos":         true | false | null,
    "her2_neg":       true | false | null,
    "her2_low":       true | false | null,    // HER2 IHC 1+ or IHC 2+/ISH-
    "pik3ca_mut":     true | false | null,
    "esr1_mut":       true | false | null,
    "akt_path":       true | false | null,    // AKT-pathway alteration (PIK3CA, AKT1, PTEN)
    "brca_germline":  true | false | null,
    "hrd_status":     "HRD-positive" | "HRD-negative" | "any" | null
  },
  "subgroup_readouts": [ "ESR1mut", "AKTpath", "HR+_subgroup", ... ],  // pre-specified subgroup analyses
  "drug_class": "Canonical drug-class string (see CLASS LIST below)",
  "year_pc": int,                                 // primary completion year
  "guideline_target_node": "string-or-null",      // your best guess at which ESMO node this trial supports
  "confidence": "high" | "medium" | "low",        // overall extraction confidence
  "notes": "Free-text notes on ambiguity, scope, or special considerations"
}
```

## Canonical drug-class strings

Use EXACTLY one of these strings for `drug_class`. If a trial tests something
new, use the closest match plus a note. The downstream concordance algorithm
checks for exact match in this string set.

- `"CDK4/6i + AI"`
- `"CDK4/6i + fulvestrant"`
- `"CDK4/6i + endocrine (pre-menopausal)"`
- `"CDK4/6i + fulvestrant (post-CDK4/6i)"`
- `"PI3Ki + fulvestrant"`
- `"PI3Ki triplet (inavolisib + CDK4/6i + fulv)"`
- `"AKTi + fulvestrant"`
- `"AKTi + chemotherapy"`
- `"SERD oral"`
- `"SERD oral + CDK4/6i"`
- `"HER2-ADC (T-DXd)"`
- `"HER2-ADC (other)"`
- `"TROP2-ADC (sacituzumab govitecan)"`
- `"TROP2-ADC (datopotamab deruxtecan)"`
- `"PARPi (olaparib)"`
- `"PARPi (talazoparib)"`
- `"everolimus + exemestane"`
- `"chemotherapy single agent"`
- `"endocrine therapy alone"`
- `"investigational (other)"` — for novel/experimental classes

## Decision rules

1. **`post_endo` vs `excluded.post_endo_metastatic_any`**:
   - If eligibility text says "patients must have progressed on prior endocrine therapy in the metastatic setting" → `post_endo: true`.
   - If eligibility text says "no prior systemic therapy in the metastatic setting" → `excluded.post_endo_metastatic_any: true`.
   - If silent → both `null`.

2. **`post_cdk46i`**:
   - If eligibility text says "must have received prior CDK4/6i" → `true`.
   - If eligibility text says "prior CDK4/6i is permitted" → `null` (allowed, not required).
   - If eligibility text says "no prior CDK4/6i" or "CDK4/6i-naive" → `false`, AND `excluded.post_cdk46i: true`.

3. **`biomarker.hr_pos`**:
   - If eligibility requires HR+ or ER+ → `true`.
   - If eligibility enrolls all comers (e.g., TROP2-ADC trial in mixed HR status) → `null` if HR+ is a stratification; `false` if explicitly HR-.

4. **`biomarker.her2_neg`** vs **`her2_low`**:
   - If eligibility says "HER2-negative" (IHC 0, 1+, or 2+/ISH-) → `her2_neg: true`, `her2_low: null`.
   - If eligibility specifically requires HER2-low (IHC 1+ or 2+/ISH-) → both `her2_neg: true` AND `her2_low: true`.
   - If eligibility requires HER2-positive (IHC 3+ or ISH-amplified) → `her2_neg: false`. The trial is OUT-OF-SCOPE for HR+/HER2- mBC; flag with `notes: "HER2-positive trial — out of scope"`.

5. **`subgroup_readouts`**: list any pre-specified biomarker subgroup that the
   trial powered or reported separately, e.g.: ESR1mut subgroup in EMERALD;
   AKT-pathway subgroup in CAPItello-291; HR+ subgroup in DESTINY-Breast04.

6. **`drug_class`**: use the canonical string. If the trial tests two arms,
   use the experimental-arm class. If trial is dose-finding/multi-arm phase II,
   use the lead arm or note in `notes`.

7. **`guideline_target_node`**: your best-guess of the (state, biomarker) tuple
   the trial is designed to support, in the format
   `"<state>|<biomarker>|HR+/HER2-"`, e.g. `"post-CDK46i|ESR1mut|HR+/HER2-"`.
   If trial is out-of-scope, set to `null`.

## Out-of-scope handling

A trial is **out-of-scope** for this paper (HR+/HER2- mBC) and should be
flagged with `confidence: "low"` and `notes: "Out of scope: <reason>"` if:
- Population is HER2-positive only (HER2-amplified)
- Population is TNBC only (HR- AND HER2-)
- Population is early-stage / adjuvant / neoadjuvant
- Trial is investigational/dose-finding with no canonical drug-class assignment

Still produce a record for these trials (don't drop them); the downstream
filter will exclude based on the `notes` field.

## Tie-breaking when sources disagree

Eligibility text is authoritative. Trial title is secondary. Conditions field
is tertiary. Drug-name string in interventions field is decisive for
`drug_class`.

## Confidence labelling

- **high**: every required field is unambiguous from the eligibility text.
- **medium**: at least one required field is ambiguous; the annotator inferred from context.
- **low**: trial is out-of-scope, or eligibility text is too sparse to extract.
