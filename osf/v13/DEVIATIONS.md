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
## Entry 2 — Phase B outcome: Quicken Simplifi EXCLUDED_E1a; §5.2 finance B2 padding amendment

**Date.** 2026-05-11 (post-Phase-B, pre-acquisition-lock).

**Affects.** Pre-registration §3.5 (Personal finance apps brand registry membership at acquisition), §5.2 (Bundle composition per category — finance B2). Personal finance category.

**Pre-reg status at the time of this entry.** Locked at `v0.13-prereg` (commit `1a6294d`). This entry documents a post-lock pre-acquisition adjustment to bundle composition resulting from the §5.4 E1a mechanism operating as designed.

### What happened

Phase B (`scripts/phaseB_resolve_v13.py`) ran on 2026-05-11T21:22:39 UTC against the out-of-sample window 2026-04-13 to 2026-04-19, Worldwide. Two finance brands solo-failed and routed to E5 bundled rescue:

- **Quicken Simplifi** (pytrends-derived topic-ID `/g/11xvvz6wpg`): solo SerpAPI returned `notEnoughSearchVolume`. E5 bundled rescue result: ALL_ZERO across the 7-day window. Final tier: **EXCLUDED_E1a**. Audit trail at:
  - `data/phaseB_suggestions/Quicken_Simplifi.json`
  - `data/phaseB_validation/solo/Quicken_Simplifi.json`
  - `data/phaseB_validation/bundled/finance_e5_bundle_1.json`
- **Lunch Money** (pytrends-derived topic-ID `/g/11x_bjn3_l`): solo SerpAPI returned `notEnoughSearchVolume`. E5 bundled rescue result: nonzero. Final tier: **PASS_E5** with acquisition_query `/g/11x_bjn3_l`. Retained in acquisition with E5 flag.

The full canonical record is in `registries/topic_id_resolution_log_v0.13.csv`.

### Empirical observation

Quicken Simplifi is tagged `incumbent` in `registries/brands_finance.json`. Incumbent-tier brands falling below the E1a eligibility floor is unusual — most v0.6–v0.12 E1a exclusions have come from challenger-tier brands with naturally low search volume. Simplifi's exclusion at both the chosen pytrends topic-ID and the bundled rescue suggests one or more of:

1. The chosen topic-ID `/g/11xvvz6wpg` may not capture the full set of "Quicken Simplifi" or "Simplifi" searches that real users issue. Alternative queries (e.g., bare `Simplifi`, `Quicken Simplifi app`) were not tested in Phase B; topic-ID resolution is single-pass per pre-reg §5.2.
2. Simplifi's mass-market footprint may be smaller than its `incumbent` registry tier suggests. Simplifi is Intuit/Quicken's modern subscription replacement for the legacy Mint product (Mint was decommissioned in September 2025 and Simplifi was positioned as its successor); residual brand-search volume from that handoff may not have transferred at the magnitude anticipated when the registry was tier-labelled.
3. Worldwide search volume for Simplifi may be substantially US-concentrated such that the Worldwide region returns insufficient signal, while US-region acquisition (the §13 sensitivity arm) might have shown signal. Phase B is Worldwide-only per §5.4; this is a known design choice, not a deviation.

These hypotheses are recorded here as forward-pointers for a possible v0.14+ re-investigation. The v0.13 analysis treats Simplifi as EXCLUDED_E1a per the locked pre-reg without re-opening Phase B post-hoc.

### Cascade: §5.2 B2 bundle composition amendment

Per pre-reg §5.2, finance B2 was defined as: `YNAB + Quicken Simplifi + Rocket Money + PocketGuard + Goodbudget` (5 slots, including pivot). With Quicken Simplifi excluded by E1a, B2 has 3 non-pivot brand members + pivot = 4 slots. Per the v0.13 padding rule (§5.2, incumbent-tier brand-volume-comparable rule), the script `scripts/acquire_trends_v13.py` is amended to pad B2's vacated slot with NerdWallet (already an incumbent in B1, parallel to PAD_FIN_EMPOWER in B4):

Amended B2 composition:

> YNAB (pivot) + Rocket Money + PocketGuard + Goodbudget + `__pad_NerdWallet`

The padding entry uses NerdWallet's canonical acquisition_query (looked up from `topic_id_resolution_log_v0.13.csv`), so NerdWallet appears in B1 as the canonical measurement and in B2 as scale-anchoring padding. Per `rescale_trends_v13.py` (inherited from v0.12 logic via `is_padding` flag), the B2 padding entry contributes zero rows to NerdWallet's per-brand within-window aggregation — only B1's canonical entry counts.

### Files affected by this entry

| File | Change |
|---|---|
| `scripts/acquire_trends_v13.py` | Added `PAD_FIN_NERDWALLET = ("__pad_NerdWallet", "NerdWallet")` constant. Replaced B2 members: removed `"Quicken Simplifi"`, appended `PAD_FIN_NERDWALLET`. |
| `data/phaseB_suggestions/` | 47 per-brand JSONs (audit trail). |
| `data/phaseB_validation/solo/` | 46 per-brand solo JSONs + 3 Mint-strategy JSONs. |
| `data/phaseB_validation/bundled/` | 1 E5 bundle JSON. |
| `registries/topic_id_resolution_log_v0.13.csv` | Canonical Phase B record; 47 rows, 14+1+1 PASS / PASS_E5 / EXCLUDED_E1a (skincare 31/0/0; finance 14/1/1). |

### Effect on H1–H8

- **H1, H2, H3, H4 (finance):** Quicken Simplifi is dropped from the finance brand set for these per-category tests. Effective finance brand set = 15 brands; analyses proceed against this set with the n_eligible threshold checks per §3.6a.
- **H6 (Linear-style / Todoist-style cross-category):** Simplifi's absence from the finance scatter is recorded but does not affect H6 detection thresholds (the test is per-category, not per-brand).
- **H7 (Three-regimes accounting):** Finance category's regime classification proceeds on the 15-brand set. Per pre-reg §3.6a, the n_PASS / n_matched_subset floor for descriptive-only routing is 0.6; with 15 of 15 PASS-eligible brands now in the acquisition set, the floor is met by design.
- **H8 (Mint phantom-persistence):** Unaffected. Mint's Phase B disambiguation (Entry 1's pattern) resolved separately from Simplifi.

### Methodological reflection

The E1a mechanism in §5.4 is designed to surface exactly this kind of empirical observation pre-acquisition. The Simplifi result is the pre-reg working as intended — not a deviation in the strict sense. This entry documents the bundle-composition cascade for full transparency and records the Simplifi observation as a forward-pointer for v0.14+ investigation.

---
