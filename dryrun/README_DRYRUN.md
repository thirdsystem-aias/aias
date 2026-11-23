# v1.21 dry run (pre-registration section 13, step 1)

Run Mon 2026-11-23, 02:07-02:31 CT on the Mac by the AIAS runner, before the lock. No data, no model call.
Code: score_v1_21.py at 8d3c95f (prereg r2, SHA-256 303cb6b5...2375). Draws: perm, shuffle, bootstrap 10,000 each (the pre-registered counts), CI 0.95.
Command per world: score_v1_21.py --fixture osf/methodology/v1_21/tests/fixtures/WORLD --out dryrun/WORLD (both stages).

| World | Known answer | Result | GATE |
|---|---|---|---|
| confirmed | H1-H5 CONFIRMED, PASS | H1-H7 CONFIRMED (H2 rho 0.048) | PASS |
| falsified | H2 FALSIFIED, FAIL | H2 FALSIFIED (rho 0.989), H5 FALSIFIED, H6 FALSIFIED | FAIL |
| marginal | H2 MARGINAL, MARGINAL | H2 MARGINAL (rho 0.369), H5 MARGINAL, H6 MARGINAL | MARGINAL |
| retest_fail | H4 FALSIFIED, noise guard on, FAIL | H4 FALSIFIED; H2, H3, H5 UNDETERMINED by the guard | FAIL |
| judge_noise | H1 FALSIFIED, noise guard on, FAIL | H1 FALSIFIED; H2 UNDETERMINED by the guard | FAIL |
| two_cats | all gate rows UNDETERMINED | all gate rows UNDETERMINED (H7 CONFIRMED, not a gate row) | UNDETERMINED |

All six worlds recover their known answer (6 of 6), each exit 0, about 4.4 min per world (two_cats 1.9 min).
Sensitivity verdict changes: one, in judge_noise: TONE_J2 moves H4 CONFIRMED to FALSIFIED (the world makes J2 noisy by construction); primary verdicts and GATE unchanged, as section 10 requires.
Log: _worktrees/_runner_tmp/v121_dryrun.log. If r3 replaces r2 before the lock, re-run this dry run on the r3 code and regenerate the lock manifest.

## Re-run on the r3 code (Mon 2026-11-23, 17:28-17:54 CT)

Code: score_v1_21.py pointed at prereg r3 (PRE_REGISTRATION_v1_21_DRAFT_r3.md, SHA-256 7ea1e8ac02d137be5b815a0646b01324ac244781b6fa6690b71f2d46db28d293; r3 is wording only, no rule changed). Same command per world, same draws (10,000 each, CI 0.95). The files in this folder are now the r3 run's.

| World | Result | GATE | Exit |
|---|---|---|---|
| confirmed | H1-H7 CONFIRMED (H2 rho 0.048) | PASS | 0 |
| falsified | H2 FALSIFIED (rho 0.989), H5 FALSIFIED, H6 FALSIFIED | FAIL | 0 |
| marginal | H2 MARGINAL (rho 0.369), H5 MARGINAL, H6 MARGINAL | MARGINAL | 0 |
| retest_fail | H4 FALSIFIED; H2, H3, H5 UNDETERMINED by the guard | FAIL | 0 |
| judge_noise | H1 FALSIFIED; H2, H3, H5 UNDETERMINED by the guard | FAIL | 0 |
| two_cats | all gate rows UNDETERMINED (H7 CONFIRMED, not a gate row) | UNDETERMINED | 0 |

Each verdicts file meets the expected answers of tests/test_score_v1_21.py (TestWorlds). Sensitivity verdict changes: one, as before (judge_noise, TONE_J2 moves H4 CONFIRMED to FALSIFIED). Every verdicts, values and Stage J file is identical to the r2-code run except the fields created_utc and prereg; the unit-outcome CSVs are byte-identical. About 4.4-5.4 min per world (two_cats 1.9 min). Log: _worktrees/_runner_tmp/v121_r3_dryrun.log; comparison: _worktrees/_runner_tmp/v121_r3_check.log.
