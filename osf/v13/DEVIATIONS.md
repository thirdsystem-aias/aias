# DEVIATIONS — AIAS v0.13

This file records all methodology decisions made during v0.13 execution that differ from, clarify, or extend the locked pre-registration. Each entry is dated and references the affected pre-registration section. Entries are appended chronologically and not edited post-commit, except for filling in placeholders that are explicitly marked `[FILL]` at the time of writing.

---

## Entry 1 — Phase A pivot validation: §4.2 query-string amendment for YNAB

**Date.** 2026-05-11 (pre-lock).

**Affects.** Pre-registration §4.1 (Per-category pivots table), §4.2 (Pivot validation protocol — Query bullet). Personal finance category.

**Pre-reg status at the time of this entry.** Draft. No `v0.13-prereg` git tag yet. The pre-reg's Acquisition lock and Git commit fields remain `[FILLED AT LOCK]`. This entry documents a pre-lock correction to a drafting flaw surfaced by the Phase A validation step, which is itself part of the pre-lock drafting process per the pre-reg's design.

### What was originally specified

§4.2's Query bullet read:

> Pivot brand canonical name + standard category disambiguation if needed (e.g., `CeraVe`; `YNAB personal finance`).

The example treated `YNAB personal finance` as the disambiguated query string for the YNAB primary pivot.

### What was empirically observed

The initial Phase A validation run on 2026-05-11 was executed with the §4.2 example query string `YNAB personal finance` for the finance primary pivot. The SerpAPI Google Trends engine returned the response *"hasn't returned any results for this query"* across all three retry attempts. This is the same signal class as the E1a `notEnoughSearchVolume` flag defined in §5.4. The result is logged at:

- `data/phaseA_test/finance_primary_YNAB_2026-05-11T20-44-42.418271+00-00.json`
  (`phase_a_status: FAIL_API`, error: SerpAPI no-results)

Under Phase A's fallback logic, Quicken was tested as fallback and PASSed (mean 87.0, CV 11.0%):

- `data/phaseA_test/finance_fallback_Quicken_2026-05-11T20-45-00.989880+00-00.json`
  (`phase_a_status: PASS`)

CeraVe (skincare primary) PASSed in the same run:

- `data/phaseA_test/skincare_primary_CeraVe_2026-05-11T20-44-37.845133+00-00.json`
  (`phase_a_status: PASS`, mean 89.43, CV 7.77%)

A subsequent diagnostic check — executed outside the canonical Phase A validator script as a one-off Python invocation — issued the bare query `YNAB` against the same out-of-sample window (2026-04-13 to 2026-04-19, Worldwide). Result: 7 daily values `[89, 86, 79, 82, 100, 69, 69]`; mean 82.0; sd 11.08; CV 13.5%. PASS by both §4.2 criteria with comfortable margin on each. This diagnostic result is recorded here for transparency; it is not stored as a `phaseA_test/` JSON because it was not produced by the canonical validator.

### Methodology decision

§4.2's "if needed" clause is conditional: the disambiguation suffix is added only when bare-query disambiguation is empirically insufficient. The evidence demonstrates the opposite for YNAB — the disambiguated query suppressed the signal entirely, while the bare query produced PASS-quality signal with substantial margin on both criteria. Under §4.2 as written and properly interpreted, `YNAB` (bare) is the correct application of the rule; `YNAB personal finance` was a drafting flaw embedded in the §4.2 illustrative example, not a binding query specification.

The corrective action is:

1. Re-run the official Phase A validator with the corrected query string `YNAB` for the finance primary pivot, producing the canonical JSON record in `data/phaseA_test/`. CeraVe is re-validated in the same run (idempotent PASS expected).

2. Tighten the §4.2 Query bullet wording to remove the misleading example and make the "if needed" rule operationally explicit. New wording locked at this entry's commit:

   > **Query.** Pivot brand canonical name. Default is the bare brand name; category-disambiguation suffix added only if Phase A demonstrates the bare query returns insufficient signal AND a disambiguated query produces PASS-quality signal. The chosen query string per pivot is recorded in `data/phaseA_test/` JSONs and in §4.1.

3. Update §4.1 to record the canonical Phase A outcomes per category, including the YNAB result and a cross-reference to this entry.

4. Designate YNAB as the validated finance primary pivot at the v0.13-prereg lock.

5. Preserve the original failed-disambiguation JSON and the Quicken-fallback JSON in `data/phaseA_test/` as full audit trail. They are not deleted on re-run because the JSONs are timestamped and do not collide.

### Status of the corrective re-run

Re-run executed 2026-05-11T20:51 UTC. Both pivots PASS:

- Canonical CeraVe JSON: `data/phaseA_test/skincare_primary_CeraVe_2026-05-11T20-51-17.073555+00-00.json` — `phase_a_status: PASS`, mean 89.43, CV 7.77%. Replicates the original 2026-05-11T20:44:37 run within Trends sampling variance.
- Canonical YNAB JSON: `data/phaseA_test/finance_primary_YNAB_2026-05-11T20-51-22.483836+00-00.json` — `phase_a_status: PASS`, mean 82.00, CV 13.51%. Replicates the diagnostic bare-YNAB result within Trends sampling variance.
- `data/phaseA_summary.csv` overwritten with the canonical run; the original-run CSV is superseded but the per-pivot JSONs preserve the full audit trail.

### Files affected by this entry

| File | Change |
|---|---|
| `PRE_REGISTRATION_v0_13.md` §4.1 | Table updated with Phase A outcomes for Skincare and Personal finance. |
| `PRE_REGISTRATION_v0_13.md` §4.2 | Query bullet wording tightened (see Methodology decision §2). |
| `data/phaseA_test/` | 5 JSONs total — full audit trail: CeraVe primary × 2 runs, YNAB-disambiguated FAIL, YNAB-bare PASS, Quicken-fallback PASS. |
| `data/phaseA_summary.csv` | Overwritten with canonical Phase A run results. |
| `scripts/phaseA_validate_v13.py` | PIVOTS list line for finance primary changed from `"YNAB personal finance"` to `"YNAB"`. |

### Methodological reflection

Pre-registration discipline distinguishes pre-lock drafting corrections from post-lock deviations. This is a pre-lock drafting correction surfaced by the empirical validation step that the pre-reg itself prescribes. The full audit trail is preserved so any reviewer can verify the failed query, the diagnostic that identified the cause, the corrective re-run, and the wording change. Future AIAS pre-registrations should default to bare brand names for pivot queries unless prior evidence demonstrates need for disambiguation.

### Forward note for Phase B (YNAB-as-brand acquisition)

The Phase B disambiguation strategy for YNAB-as-brand (i.e., as a measured brand rather than as the pivot) is informed by this Phase A result: the bare query `YNAB` produces healthy signal at Worldwide region against the v0.13 wave windows, so Phase B should default to bare `YNAB` for YNAB's topic-ID resolution. Disambiguation only revisited if Phase B pytrends.suggestions() returns ambiguous results for bare `YNAB`. The decision is logged in `registries/topic_id_resolution_log_v0.13.csv` prior to acquisition lock.

---
