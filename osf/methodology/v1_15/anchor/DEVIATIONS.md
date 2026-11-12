# v1.15 DEVIATIONS

## Entry 0 (ex ante, draft r0, 2026-11-10 evening CT)

**Type:** ex ante. No judge call has been made; no t4 answer, window, valence, P, C\* or R value has been read or computed by this study.

**What was read before the lock.** v1.11's locked files at tag `v1.11-prereg-r1` (pre-registration, judge prompt, `u0_v1_11.json`, `token_counts_v1_11.json`, scripts); the AIAS 6.0 Preview pre-registration (branch `aias-6.0-preview` @ f59d4d4, read only); v0.42's scripts and probe file (branch `v0.42` @ 73daada and tag `v0.42-prereg-r1` → 58d1891; the four copied functions are identical at both); v1.14's Stage 1 output schema (`scripts/score_v1_14.py`, branch `v1.14` @ ceb706d); the five omnibus registries (loader of v1.10).

**What was computed before the lock.** The planning cost table (`prereg/cost_estimate_v1_15.json`; locked inputs only) and the COI string screen of the five registries (`prereg/coi_screen_v1_15.json`; registry names and aliases only). Tests run on synthetic data only.

**COI.** No new brand selection; each registry keeps its source phase's handling (v1.11 DEVIATIONS Entry 0, quoted there verbatim). String screen with the 22 terms of v1.11 Entry 0: one match, Denon (v0.19). Denon stays in the primary analysis; every statistic is also reported without it (SD).

**Anchor sequence.** As `LOCK_STEPS.md`: lock manifest → commit → tag `v1.15-prereg-r1` → push → `lock/write_anchor_v1_15.py --osf-deposit` → commit → OSF deposit, SHA-256 verified → only then U0 on t4 (if not already run) and the judge run.
