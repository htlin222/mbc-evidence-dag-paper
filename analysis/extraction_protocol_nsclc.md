# LLM Extraction Protocol — NSCLC extension (schema v1.0 additive)

Used by both annotator A (Claude) and annotator B (Codex / GPT-5) for the NSCLC
v3 corpus. Same frozen schema v1.0 as mBC, with NSCLC-specific biomarker
vocabulary additions. The mBC fields remain valid even if `null` for NSCLC.

## Output schema (frozen v1.0; NSCLC biomarker vocabulary added)

```json
{
  "nct_id": "NCT0xxxxxxx",
  "trial_name": "TRIAL-ACRONYM or canonical trial name (string)",
  "prior_state": {
    "post_endo":            null,      // not applicable to NSCLC; always null
    "post_cdk46i":          null,      // not applicable to NSCLC
    "post_egfr_tki":        true | false | null,   // prior EGFR TKI required/excluded/silent
    "post_osimertinib":     true | false | null,
    "post_alk_tki":         true | false | null,   // prior ALK TKI required/excluded/silent
    "post_chemo_metastatic_min": int | null,
    "post_immunotherapy":   true | false | null,
    "menopausal_status":    null
  },
  "excluded": {
    "post_egfr_tki":        true | false | null,
    "post_osimertinib":     true | false | null,
    "post_alk_tki":         true | false | null,
    "post_chemo_metastatic_any": true | false | null,
    "post_immunotherapy":   true | false | null
  },
  "biomarker": {
    "hr_pos":          false,    // mBC field; always false for NSCLC
    "her2_neg":        null,
    "her2_low":        null,
    "pik3ca_mut":      null,
    "esr1_mut":        null,
    "akt_path":        null,
    "brca_germline":   null,
    "egfr_mut":              true | false | null,   // any EGFR mutation
    "egfr_ex19del":          true | false | null,
    "egfr_l858r":            true | false | null,
    "egfr_t790m":            true | false | null,
    "egfr_ex20ins":          true | false | null,
    "egfr_other_mut":        true | false | null,   // L861Q, G719X, etc.
    "alk_rearranged":        true | false | null,
    "alk_resistance_mut":    true | false | null,
    "tumor_type":            "NSCLC-EGFR" | "NSCLC-ALK" | "NSCLC-both" | "NSCLC-other"
  },
  "subgroup_readouts": [ "egfr_ex19del", "egfr_l858r", "t790m_subgroup", "alk_resistance_subgroup", ... ],
  "drug_class": "Canonical NSCLC drug-class string (see CLASS LIST)",
  "year_pc": int,
  "guideline_target_node": "string-or-null",
  "confidence": "high" | "medium" | "low",
  "notes": "Free-text notes on ambiguity, scope, or special considerations"
}
```

## Canonical NSCLC drug-class strings

- `"EGFR TKI 1st-gen (gefitinib/erlotinib)"`
- `"EGFR TKI 2nd-gen (afatinib/dacomitinib)"`
- `"EGFR TKI 3rd-gen (osimertinib)"`
- `"EGFR TKI 3rd-gen + chemotherapy"`
- `"EGFR TKI 3rd-gen + bispecific (amivantamab + lazertinib)"`
- `"Amivantamab + chemotherapy"`
- `"HER3-ADC (patritumab deruxtecan)"`
- `"TROP2-ADC (datopotamab deruxtecan)"`
- `"ALK TKI 1st-gen (crizotinib)"`
- `"ALK TKI 2nd-gen (alectinib/brigatinib/ceritinib/ensartinib)"`
- `"ALK TKI 3rd-gen (lorlatinib)"`
- `"Platinum doublet chemotherapy"`
- `"Platinum doublet + PD-1/PD-L1"`
- `"PD-1/PD-L1 monotherapy"`
- `"PD-1/PD-L1 + CTLA-4"`
- `"Anti-VEGF + chemotherapy"`
- `"Bevacizumab + chemotherapy"`
- `"Ramucirumab + EGFR TKI"`
- `"Bevacizumab + EGFR TKI"`
- `"investigational (other)"`

## Decision rules

1. **`tumor_type`**: required field for NSCLC trials. Use "NSCLC-EGFR" if biomarker requires EGFR mutation; "NSCLC-ALK" if ALK rearrangement; "NSCLC-both" if multi-cohort; "NSCLC-other" if neither (e.g., trial in driver-negative or HER2-mutant NSCLC — likely out of scope for this paper).

2. **mBC-specific fields** (hr_pos, her2_neg, post_endo, post_cdk46i, etc.): all `null` or `false` for NSCLC trials. Don't infer.

3. **`post_egfr_tki`** vs **`post_osimertinib`**:
   - If trial requires post-1st/2nd-gen EGFR TKI progression: `post_egfr_tki: true`
   - If trial requires post-osimertinib (3rd-gen) progression: BOTH `post_egfr_tki: true` AND `post_osimertinib: true`
   - If silent: `null`

4. **`alk_resistance_mut`**: if trial enrolls patients with specific ALK resistance mutations (e.g., G1202R, ROS1 L1196M), set `true`; else `null`.

5. **`drug_class`**: prefer the most specific canonical string. For combination arms, use the experimental-arm class.

6. **Out-of-scope**: HER2-mutant NSCLC, KRAS G12C, ROS1, RET, MET, NTRK, BRAF V600E trials are OUT-OF-SCOPE for v3 (deferred to v4). Driver-negative NSCLC is OUT-OF-SCOPE. Flag with `confidence: "low"` and `notes: "Out of scope: <reason>"`. Don't drop — keep in extraction for transparency.

7. **`guideline_target_node`**: best-guess in format `"<state>|<biomarker>|NSCLC"`, e.g. `"post-osimertinib|EGFR-mut|NSCLC"`.

## Confidence labelling

- **high**: every required field is unambiguous from the eligibility text.
- **medium**: at least one field inferred from context (trial design, intervention names, official title).
- **low**: trial is out-of-scope, or eligibility text is too sparse.
