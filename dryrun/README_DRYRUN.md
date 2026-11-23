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
