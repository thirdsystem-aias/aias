# AIAS™ v0.43: dated amendment under §2.6, the Coverage component in Stage 2

Deposited 2026-11-27 with the lock of the AIAS 3.0 release pre-registration (tag `aias-3-0-prereg-r1`, `osf/aias_3_0/prereg/PRE_REGISTRATION_aias_3_0.md`, Appendix A). The text below is Appendix A as locked, with only "[date of deposit]" filled in. OSF `ec6wh`, `v43/prereg/` (and `aias_3_0/prereg/`).

**Amendment, dated 2026-11-27: Coverage (v1.12) added to Stage 2.** Under §2.6 ("Each component's predictive hypothesis is added to Stage 2 by a dated amendment … with this section's outcome, windows, statistic and verdict rule unchanged and Z = {L, P_new}. A component that failed its Paper A separability gate is not added."), Coverage is added: its Paper A (Methodology v1.12, tag `v1.12-prereg-r1`) returned GATE PASS on 2026-11-14 (`osf/methodology/v1_12/v112_verdicts.json`, commit `949be61`).

- **`H_Pred_Coverage_Confirm` (SECONDARY).** X = Cov\* at the t4 week (N3, search off; v1.12 §2.4; column `cov_star` of `osf/methodology/v1_12/v112_unit_table.csv` at `949be61`; rated units only); Y = the change from W(2026-11-07) to W(2027-03-06) (§2.4); Z = {L at W(2026-11-07), P_new at t4} (§2.1); ρ_pw|Z (§2.1); one-sided permutation p, 10,000 draws, seed 430051; bootstrap intervals as §2.1; verdict rule of §2.1 unchanged, including the REVERSED label; minimum n 30 units with a defined outcome (the floor §2.1 sets for the rated-only Consistency tests).
- **Reported beside it (no verdict):** per substrate (§2.8 item 1); without the five defunct automotive brands (§2.8 item 2; Cov\* rates none of them unless named); the same test with Cov\* and P_new from the quotes-normalised coding (AIAS 3.0 pre-registration §10.2; v0.45 DEVIATIONS Entry 2).
- **Data.** Stage 2's three outcome pulls as §4.5 fixes them; no request is added. No sales-rank outcome is added (§4.6 unchanged).
- **Effect on the locked text.** None: no other hypothesis, window, statistic, threshold, seed or check changes.
