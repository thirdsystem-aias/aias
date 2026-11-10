# DEVIATIONS — v1.14 (Ranking, redesigned measure)

## Entry 0 — ex ante (2026-11-10, before the lock)

**Type:** ex ante (selection history, COI screen, pre-lock record, anchor preamble). No rank position has been computed on a t4 or t5 answer; no t4 answer exists.

**Selection history.** The declared statistic (MODE, modal position) is v1.10's sixth candidate. It was chosen after v1.10's sensitivity check S3 had run all six candidates through H1–H3 on the archived waves t1–t3 (v1.10 verdicts file, `sensitivities.S3_candidate_MODE`), on Pablo's decision of Tue Nov 10, 2026, 12:27 pm (pre-registration §0, §1). The archived waves are therefore calibration only; t4 (Stage 1) and t5 (Stage 2) are the confirmatory data.

**COI screen.** No new brand selection. Stage 1 and Stage 2 use the five omnibus registries (v0.19–v0.23) exactly as v1.10 loads them; the calibration also reads v1.10's early-panel rank tables (registries screened in v1.10 DEVIATIONS Entry 0, no match). Each substrate keeps the COI handling of its source phase, as recorded in v1.10 DEVIATIONS Entries 0 and 2: the v0.19 AKG → Denon substitution with the correction of November 10, 2026 (Denon owned by Harman International, a wholly owned subsidiary of Samsung Electronics, since September 23, 2025; source: HARMAN press release, Business Wire, September 23, 2025), and the v0.22 tier-2/3 supply relationships (Harman International audio systems, Samsung SDI battery cells, Samsung Display infotainment; non-competitive; no restriction on registry composition). Handling here: Denon stays in the registry and in the primary analysis; every gate statistic is also reported without the Denon unit (S7). No v0.22 brand is removed (supply, not ownership).

**Pre-lock record.** On 2026-11-10 the calibration (`scripts/score_v1_14.py --calibration`) read v1.10's 31 hashed rank tables and the locked profiles table and reproduced v1.10's S3 values for MODE exactly; it also computed, on the same archived waves, H4, H5, MQ7, S2, S7, S9, MQ9 and the precision note for MODE (pre-registration §4, §7). Stage 1 and Stage 2 were run only on synthetic t4-shaped data in the unit tests.

**Anchor preamble.** Content lock → `prereg/LOCK_MANIFEST_v1_14.sha256` → commit → tag `v1.14-prereg-r1` → push → `anchor/git_anchor_v1_14.json` (with the activation record of the component legs) → OSF deposit of `prereg/`, `calibration/`, `anchor/` with SHA-256 verified → Stage 1 only after tag `v0.42-acquisition-locked` exists (the scorer refuses otherwise).
