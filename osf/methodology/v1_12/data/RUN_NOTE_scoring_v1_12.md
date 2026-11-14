# v1.12 Coverage Paper A: coding and scoring run note (2026-11-14, runner lane A)

Worktree `/Users/pablou/aias/_worktrees/v1.12`, branch `v1.12` at `b89ff1f` (collection commit). `PYTHONDONTWRITEBYTECODE=1` for every step. No model call, no spend.

## Checks before coding
- Tag `v1.12-prereg-r1` on origin: tag object `e0b5e31c`, commit `49efc473`; `anchor/osf_anchor_v1_12.json` names both.
- `shasum -a 256 -c prereg/LOCK_MANIFEST_v1_12.sha256` (38 files): 37 OK; `anchor/DEVIATIONS.md` differs only because Entry 1 (2026-11-13) was appended after the lock; its content at the tag (SHA-256 `782e071e…`, as manifested) is unchanged above the new lines (`git diff v1.12-prereg-r1 HEAD` = 4 added lines). Re-checked after scoring: same result.
- Raw record `data/v112_raw.jsonl` SHA-256 `e23b6652…6c11` (900 lines); log `data/collect_v1_12.log` `933def22…b94`. Deposited at OSF `methodology/v1_12/data/` on 2026-11-14 12:17 UTC (osf_deposit.py, 2 of 2 verified by SHA-256).
- Coder pin (§2.3): `git rev-parse v0.42-prereg-r1:osf/v42/scripts/code_t4_v0_42.py` = `2d36735d…` = vendored copy (SHA-256 `d0e4e685…`). No difference, so no DEVIATIONS entry.
- MC_BrandFree re-run to a scratch file (`--brandfree --out <lane folder>`): PASS, 0 hits, identical to `anchor/mc_brandfree_v1_12.json` (the locked record was not rewritten).

## Steps (UTC)
| Step | Command | Start | End | Exit |
|---|---|---|---|---|
| P1 | `score_v1_12.py --parity-p1` | 12:20:19 | 12:20:24 | 0 (PASS: 4,032 mention cells, 0 mismatches; recognition 672 cells, 0 mismatches, reported) |
| Coding | `score_v1_12.py --code` | 12:21:17 | 12:21:21 | 0 (900 calls, 900 answered, 20,160 mention rows) |
| Scoring (once) | `score_v1_12.py --run --raw osf/methodology/v1_12/data/v112_raw.jsonl --coded osf/methodology/v1_12/data/coded --t4-raw …/v0.42/osf/v42/data/t4_raw.jsonl --t4-coded …/v0.42/osf/v42/data/coded --t4-brand-table …/v0.42/osf/v42/v42_brand_table.csv --t4-verdicts …/v0.42/osf/v42/v42_verdicts.json --h5-stage1 …/v1.14/osf/methodology/v1_14/outputs/stage1/stage1_v1_14.json` (no `--h6`; draws as locked, 10,000/10,000) | 12:21:56 | 12:23:21 | 0 |

Full command lines and output: `code_v1_12.log`, `parity_p1_v1_12.log`, `score_v1_12.log` (this folder).

Inputs read by the scoring run: t4 = v0.42 at tag `v0.42-scoring-locked` (`31c64c6`; no diff to the worktree for these files): `t4_raw.jsonl` `f3109091…d4bf` (= `anchor/t4_complete_v1_12.json`), `v42_brand_table.csv` `792e14ad…`, `v42_verdicts.json` `b5094ced…`; H5 = v1.14 Stage 1 (commit `3129674`, on origin): `stage1_v1_14.json` `4de97fea…`, `rank_table_t4_v1_14.csv` `5e628658…`, STAGE1_VERDICT MARGINAL; H6 INACTIVE (as the anchor recorded); scorer `f7689898…` (as manifested).

## Outputs (SHA-256)
- `data/coded/v112_mentions.csv` `f40dfd27ff9a192d382b893e2bd67a7c8bef262bbfe90ea655c70a7bc211f006`
- `data/coded/registry_v1_12.json` `5cb33c898a57a8655ff8f858a0baa6ff981eba835fb7aed7bb6eeb2bce032843`
- `data/coded/coding_record_v1_12.json` `aefeef0aeeb4a564807502cd778a47bed5b66e592e80917f372d9af48f57041f`
- `anchor/parity_P1_v1_12.json` `257a203d2370b85af8f2b4ce3cd08c6874f9301970a40d0ecb25694839fdbfd1`
- `v112_verdicts.json` `0c70bde10c7cbd79209f791e1447e8508d7bae66d911dae3bb12808ffa87c992`
- `v112_unit_table.csv` `06b7875042ee5f5c17676cab604a9d58ffd1a15102f1edc5d5f075bfd16e97b0`

## Result (from `v112_verdicts.json`; verdict words as the scorer wrote them)
Paper A: **PASS** (H1–H4 CONFIRMED; H5 CONFIRMED, reported, not gating because v1.14's Stage 1 is MARGINAL, N35; H6 INACTIVE; H7 CONFIRMED, no downgrade; H8 CONFIRMED). Parity P1, P2 (112 units, 0 mismatches), P3 (900 records) passed; comparators from t4 (not cross-panel); no model dropped. Gate repeated on C3 and A4: PASS on both. Verdict changes under sensitivities (reported, never change a verdict): S1 raw Cov flips H1 and H3 to FALSIFIED (expected, §7.4); S2 floor 28 leaves H1–H3 UNDETERMINED (below the n floor); S4 moves H4 to MARGINAL. δ fits: 418 ok, 30 not converged and set to 0 (§2.4).
