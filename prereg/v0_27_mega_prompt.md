# v0.27 - CV.03 Convergent Validity - Measurement Execution Prompt

**Project:** CV.03 - Convergent validity of AIAS Presence against third-party AI brand-visibility instruments
**Methodology lock:** Protocol v1.6 (SSRN 6816340)
**Substrate:** B2B SaaS (registry inherited verbatim from v0.24/v0.25)
**Pre-reg tag at acquisition:** `v0.27-prereg-r1` (or `-r2` if the Profound-access amendment fires)

> Run only AFTER the pre-reg is committed/tagged AND the cloned v27 scorer/builders have had `BSR_PROTOCOL` -> `INSTRUMENT_PROTOCOL` renamed (grep-scoped). Canonical scoring is sourced directly from the locked registry and the locked verdict matrix - no mid-session threshold edits.

---

## 0. Registry (locked, do not modify)

Load the 24-brand B2B SaaS list verbatim from `osf/v27/registries/v27_registry.json` (copied verbatim from `osf/v24/registries/v24_registry.json`). Do not re-derive or re-rank. Carry forward the **Stride name-collision** disambiguation (SaaS brand vs. gum) exactly as resolved in v0.24.

## 1. AIAS-side acquisition (fixed panel)

Panel held fixed from v0.17: Claude Opus 4.5 / Claude Sonnet 4.5 / GPT-4o / GPT-4o-mini / Gemini 2.5 Flash / Gemini 2.5 Flash Lite.

- **Phase A - Recognition:** 24 x 6 = 144 probes -> C_P per brand. *Expected at ceiling (6/6); retained only for H_CV3_Recognition_Null.*
- **Phase B - two-channel Recall:** 6 category probes x 6 LLMs = 36 queries -> per-brand **recall-channel SOM** and **AIAS composite** (variance-bearing AIAS-side variables for every convergent test).

Output: `data/v0.27_phaseA_recognition.csv`, `data/v0.27_phaseB_recall.csv`.

## 2. Instrument-side pulls (+/-7 days of Phase B; log timestamps)

| Tag | Instrument | Role | Variables | Access |
|---|---|---|---|---|
| I1 | HubSpot AEO Grader | convergent (primary floor) | visibility composite + 5 sub-dimensions | free, no account |
| I2 | Profound | convergent (co-primary) + same-metric SOM | visibility score + Share-of-Model | API/CSV **if obtained**, else NOT_RUN |
| I3 | Brandwatch | discriminant contrast | web/social mention volume | export |

Write one row per (brand, instrument, variable, pull_timestamp) to `data/v0.27_instrument_pulls.csv`. Record nulls explicitly; do not impute.

## 3. Coverage pre-screen (v1.6 Inc1-style gate)

A brand enters an instrument's correlation only if that instrument returned a non-null score. Correlations run **pairwise** per covered subset. Covered n < 12 -> that instrument's hypotheses UNDETERMINED (not FALSIFIED). Log covered-n per instrument in the verdicts file.

## 4. Scoring (locked v1.6 scorer)

Spearman rho, brand-level, per instrument. Bootstrap 95% CI (10,000). Holm correction across the I1/I2/I3 primary family. Emit `osf/v27/v0.27_verdicts.json` with per-hypothesis status against the locked matrix in `v0_27_b2b_saas_convergent_validity_content.py`.

## 5. Deviation handling

If Profound access is not secured before acquisition: stop, amend at `v0.27-prereg-r2`, DEVIATIONS Entry 0 -> 'fired' (I2 + H_CV3_SOM -> NOT_RUN), then proceed on I1 + I3. HubSpot AEO is the pre-committed floor for exactly this reason.
