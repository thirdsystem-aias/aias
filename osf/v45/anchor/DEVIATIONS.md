# v0.45 (t₅ wave) — DEVIATIONS

Every change after the lock gets an entry: id, date, ex ante or ex post, what, why, effect on inference. Hypotheses, thresholds, tests and seeds do not change after the lock; anything added later is exploratory.

## Entry 0 (ex ante, written with pre-registration r0, 2026-11-10)

**Conflict-of-interest handling carried forward.** v0.45 re-asks t₄'s questions against the registries fixed in v0.19–v0.23 and performs no new brand selection. The handling of record is carried forward unchanged from v0.42 §8, including the correction of November 10, 2026 on the v0.19 registry's Denon unit, quoted verbatim in the pre-registration's §8. No registry, probe or rule changes.

**Contingencies declared before any t₅ call** (pre-registration §4.3, §4.5, §4.6, §5.1): the replacement rule for a t₄ model retired or no longer served under its ID; the successor v0.23 recognition judge and its parity check J1; the projection pause and the $80 and $100 rules; the move of the window if t₄ is delayed. Using any of them is logged here as an entry before its effect, with the record that triggered it.

## Entry 1 (2026-11-21; ex post for J1, ex ante for t₅ coding: written before any t₅ answer exists or is coded)

**Pre-registered contingency used: successor v0.23 recognition judge = Claude Sonnet 5.5 (`claude-sonnet-5-5`), J1 PASS** (pre-registration §5.1; LOCK_STEPS step 8). Run once, on 2026-11-21 from 17:11 UTC (11:11 am CT), with the locked script unchanged: `code_t5_v0_45.py --parity claude-sonnet-5-5 --t4-raw <t4_raw.jsonl from tag v0.42-acquisition-locked, SHA-256 f3109091…> --t4-coded <coded tables at c84f6fa; v23_phase_a.csv SHA-256 52a1c9d7…>`, from worktree branch `v0.45-j1` at `46896a7` (lock manifest: 34 of 34 OK; no other paid collection running; model served per the free models lookup). Lock-test note: `test_judge_and_parity_refuse_before_lock` now fails (68 tests, 1 failure) because the tag is on origin, so the guard it tests no longer refuses; expected after the lock, no code change.

**Result.** 216 requests, 216 labels, 0 R_ERR. Binary agreement with Claude Sonnet 4.5: 216 of 216 (1.000; threshold ≥ 206), t₃ 144 of 144, t₄ 72 of 72 (1.000; threshold ≥ 65). Exact R-level agreement: t₃ 136 of 144 (0.944), t₄ 72 of 72. Verdict PASS; the fallback (Claude Sonnet 4.6) was not run. Recorded usage: 308,511 input and 864 output tokens, $0.625662 at the standard price in `budget_v0_45.py` ($2 / $10 per million), within J1's $0.67 bound and the $2.50 judge reserve. Record: `osf/v45/data/judge_parity_J1_v0_45.json` (with the winner's 72 t₄ codes) and its log `judge_parity_J1_v0_45.log`.

**Effect on inference.** As pre-registered: Claude Sonnet 5.5 codes t₅'s v0.23 Phase A answers, and its t₄ codes (recorded in the J1 file) are the t₄ v0.23 recognition codes in every t₄ → t₅ comparison of P and recognition (§5.1, "Judge held constant"); v0.42's locked Sonnet 4.5 values are reported beside them. No hypothesis, threshold, test or seed changes.
