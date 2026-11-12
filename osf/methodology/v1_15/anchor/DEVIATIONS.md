# v1.15 DEVIATIONS

## Entry 0 (ex ante, draft r0, 2026-11-10 evening CT)

**Type:** ex ante. No judge call has been made; no t4 answer, window, valence, P, C\* or R value has been read or computed by this study.

**What was read before the lock.** v1.11's locked files at tag `v1.11-prereg-r1` (pre-registration, judge prompt, `u0_v1_11.json`, `token_counts_v1_11.json`, scripts); the AIAS 6.0 Preview pre-registration (branch `aias-6.0-preview` @ f59d4d4, read only); v0.42's scripts and probe file (branch `v0.42` @ 73daada and tag `v0.42-prereg-r1` → 58d1891; the four copied functions are identical at both); v1.14's Stage 1 output schema (`scripts/score_v1_14.py`, branch `v1.14` @ ceb706d); the five omnibus registries (loader of v1.10).

**What was computed before the lock.** The planning cost table (`prereg/cost_estimate_v1_15.json`; locked inputs only) and the COI string screen of the five registries (`prereg/coi_screen_v1_15.json`; registry names and aliases only). Tests run on synthetic data only.

**COI.** No new brand selection; each registry keeps its source phase's handling (v1.11 DEVIATIONS Entry 0, quoted there verbatim). String screen with the 22 terms of v1.11 Entry 0: one match, Denon (v0.19). Denon stays in the primary analysis; every statistic is also reported without it (SD).

**Anchor sequence.** As `LOCK_STEPS.md`: lock manifest → commit → tag `v1.15-prereg-r1` → push → `lock/write_anchor_v1_15.py --osf-deposit` → commit → OSF deposit, SHA-256 verified → only then U0 on t4 (if not already run) and the judge run.

## Entry 1 (ex ante, 2026-11-12 03:35 UTC = Wed 2026-11-11 9:35 pm CT, after the lock and before any judge call): U0 on t4 run after the lock

**Type:** ex ante (runner). No judge call has been made; no valence, P, C\* or R value exists for this study.

**What.** U0 was run after tag `v1.15-prereg-r1` (tag object `4f7e1d85196489c9c26ea00a77536cd9bcbce056` → commit `1d9e912848c9357e3703b522e7061da61f5549b8`, pushed 2026-11-12 ~03:33 UTC), the anchor commit `5ea75ca` and the OSF deposit of `prereg/` and `anchor/` (SHA-256 verified: 4 of 4, 2 of 2): `score_v1_15.py --build-units --raw-ref v0.42-acquisition-locked --coded-ref 31c64c64656b7b0393eca49e5d10384744475dd9`. The coded ref is the commit of tag `v0.42-scoring-locked` (tag object `a4c20832…`); v0.42's coded Phase B tables were committed at `c84f6fa` (2026-11-11) and are unchanged at `31c64c6`. Raw answers: `osf/v42/data/t4_raw.jsonl` at `v0.42-acquisition-locked` (→ `a790bb1`), SHA-256 `f3109091f51af789…` (the value in that tag's message). Every input is logged with its git blob and SHA-256 in `prereg/u0_v1_15.json` (`inputs_read`, `refs`). Result: drop rule, no model dropped (202 of 202 answered S0 calls for each N3 model); 270 judged answers (54 per category); 1,644 mention windows, 0 extraction misses; 1,547 judged after the window cap (97 capped out); self-consistency sample 77; calls planned 1,624 per judge; 0 judged Denon windows. Unit table `prereg/units_v1_15.csv` (1,644 rows), SHA-256 `2fb080fb982256265657244938a0c9c3e2eda09115f20ea3394b1b03bfa6e1ce`. Then `judge_v1_15.py --dry-run` (no network, no SDK import): 3,248 jobs, 0 requests with a sampling parameter, planning projection $15.84 with overhead (`prereg/dry_run_judge_v1_15.txt`).

**Why.** §3: U0 runs after t4's acquisition lock and before any judge call, and "if it is run after the lock it is logged in DEVIATIONS as an ex ante step". `LOCK_STEPS.md` §4 places U0 after the lock.

**Effect on inference.** None: U0 applies §3's rules unchanged (v1.11's F rules, seeds 111001 and 111003), and no judge output existed when it ran.
