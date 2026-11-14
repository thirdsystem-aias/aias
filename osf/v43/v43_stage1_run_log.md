# v0.43 Stage 1 — scoring run log

Pre-registration: `osf/v43/prereg/PRE_REGISTRATION_v0_43.md`, locked as tag `v0.43-prereg-r1` (tag object 9955529f, commit 8c96d9cf, 2026-11-11 00:31 CT), anchor `osf/v43/anchor/osf_anchor_v0_43.json`, post-lock record `osf/v43/anchor/DEVIATIONS.md` (Entry 1 only). Stage 1 per §2.2, §2.3, §2.7, §2.8 and §5.3: one run on the three complete main pulls.

## Checks before the run (2026-11-14, 06:16 to 06:18 CT)

- Tag on origin: `git ls-remote origin refs/tags/v0.43-prereg-r1` → 9955529f7c26407df2b24f8eb8523ba5b91d8380 (= anchor `tag_object`); tag commit 8c96d9cf is an ancestor of the scored head 38e5711.
- Lock manifest: `shasum -a 256 -c osf/v43/prereg/LOCK_MANIFEST_v0_43.sha256` from the repository root → 12 of 12 OK.
- Data (read-only check with the locked `trends_common_v0_43` functions): main1, main2 and main3 each hold 28 of 28 records, status ok, 1 attempt each (no re-sends, none missing); every record's units, terms and `q` match `bundles_v0_43.json` and `terms_v0_43.json`; parameters TIMESERIES, geo US, tz 0, range 2025-05-04 to 2026-11-07; MC_Weekly re-run on every stored response with windows ending 2026-06-06, 2026-11-07, 2026-02-07, 2025-06-07 and 2025-11-08: 84 of 84 pass; every record fetched after the lock.
- Spacing (§4.3, read as last request of one pull to first request of the next): main1 06:50:07Z to 06:51:39Z on 11-12; main2 06:55:04Z to 06:56:40Z on 11-13 (gap 24.06 h); main3 07:00:07Z to 07:01:49Z on 11-14 (gap 24.06 h).
- Raw data are the files committed at 38e5711 (git status clean under `osf/v43/data`). `bundles_v0_43.json` SHA-256 7d6b08ca28e203c8953f8b6d84c7473d7a496110cae902db52d6c27f48b315c7; `terms_v0_43.json` 2e83420f2c693f394aa4cea5003c6b3a29545a7a732fcf6c12e482e27952bb56.
- Locked unit tests `osf/v43/scripts/tests/run_all_v0_43.py` (synthetic data, temporary folders): 16 of 16 pass.
- No timing rule in the pre-registration sets an earliest analysis time for Stage 1 other than complete pulls (§5.3).

## Run (once)

    cd /Users/pablou/aias/_worktrees/v0.43
    PYTHONDONTWRITEBYTECODE=1 caffeinate -is python3 -u osf/v43/scripts/score_v0_43.py --stage 1

Python 3.14.4, numpy 2.4.4, scipy 1.17.1. Start 2026-11-14T12:18:14Z, end 2026-11-14T12:18:21Z (`created_utc` in the output 12:18:15.858899Z). Default B_perm = B_boot = 10,000; seeds as §2.1. Output `osf/v43/v43_stage1_verdicts.json`, 50,409 bytes, SHA-256 437d0ea327f3c0b0177dc9e9b3ce9fbb9d9b670171c7c74493c84bfc614e43dc. Console:

    H_Pred_Presence FALSIFIED [] -0.1859935412130373 0.9664033596640336 105
    H_Pred_Presence_SA FALSIFIED [] -0.14691153767974902 0.9192080791920808 101
    H_Pred_Presence_Momentum FALSIFIED ['REVERSED'] -0.21859000139715726 0.9851014898510149 103
    H_Pred_Consistency UNDETERMINED [] 0.063783011053971 0.34206579342065796 52
    flags: []

## Results (from `v43_stage1_verdicts.json`)

| Test | x \| controls | n | ρ_pw\|Z | 90% CI | 95% CI | p one-sided | p two-sided | Verdict |
|---|---|---|---|---|---|---|---|---|
| H_Pred_Presence (primary) | P \| L | 105 | −0.186 | −0.326 to −0.023 | −0.355 to 0.008 | 0.966 | 0.070 | FALSIFIED |
| H_Pred_Presence_SA | P \| L, y = Y^SA | 101 | −0.147 | −0.298 to 0.015 | −0.327 to 0.048 | 0.919 | 0.160 | FALSIFIED |
| H_Pred_Presence_Momentum | P \| L, M | 103 | −0.219 | −0.380 to −0.038 | −0.411 to −0.001 | 0.985 | 0.031 | FALSIFIED, REVERSED |
| H_Pred_Consistency | C* \| L, P | 52 | 0.064 | −0.266 to 0.380 | −0.327 to 0.433 | 0.342 | 0.693 | UNDETERMINED |

Manipulation checks: MC_Concurrent ρ = 0.416 (n 112, one-sided p 0.0002), pass; MC_PullReliability mean 0.949 (pairs 0.933, 0.978, 0.935), pass; MC_Weekly 84 of 84 ok, 0 missing, 0 re-sent; MC_Terms share by topic 0.554, pass; MC_Chain links held: main1 3/3, 4/5, 5/5, 5/5, 5/5; main2 3/3, 4/5, 5/5, 5/5, 5/5; main3 3/3, 5/5, 5/5, 5/5, 5/5 (v0.19 to v0.23; the failed link is in v0.20). No flags.

## Exclusions (§5.2, §5.5; no imputation)

- Y undefined (S(W_base) + S(W_end) < 4 in every bundle in all three pulls), 7 units, out of every test: v0.19 Audeze (0+0), Beyerdynamic (0+1), Spirit Torino (0+0), ZMF Headphones (0+0); v0.20 Bioderma (0 in b4; 0+1 or 0+2 in b5), Dior Beauty (0+0); v0.21 Chantecaille (0+0). Outcome defined: v0.19 12/16, v0.20 22/24, v0.21 23/24, v0.22 24/24, v0.23 24/24.
- Y′ (one year earlier) defined in fewer than two pulls (H_Pred_Presence_SA), 4 more: v0.19 Dan Clark Audio (defined in main2 only); v0.23 S21 (no pull), S23 (no pull), S24 (main2 only).
- M undefined (H_Pred_Presence_Momentum), 2 more: v0.19 Dan Clark Audio (main3 only); v0.23 S21 (main2 only).
- H_Pred_Consistency: only units rated for C* at t₂ (54 of 112); 2 of them lack Y (v0.19), leaving 52 (v0.19 6, v0.20 9, v0.21 14, v0.22 14, v0.23 9).

## Independent re-check (not part of the locked pipeline)

The four point estimates, their n and MC_Concurrent's ρ were recomputed from the output's unit table with pandas and numpy least squares (not the locked code): all equal to the stored values to 1e-9. The verdict rule of §2.1 applied by hand to the stored statistics gives the stored verdicts and labels.

Lane B, AIAS runner, 2026-11-14.
