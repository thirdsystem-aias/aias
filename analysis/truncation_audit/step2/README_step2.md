# Sensitivity analysis — not a replacement of any locked or published result

Truncation audit, step 2 (Nov 12, 2026). Branch `truncation-audit` (local only). Question: do the
verdicts of v0.41, v1.9 (Stage 2), AIAS 2.0, v0.34 and v1.8 change when Gemini 2.5 Flash's answers
are taken out, given that its headphones (v0.19) answers were cut at the output-token limit before
naming any brand and its premium-spirits (v0.23) answers partly so (step 1, `../README.md`)?

- **Variant (a):** Gemini 2.5 Flash removed from v0.19 and v0.23 only, in every wave (t1, t2, t3).
- **Variant (b):** Gemini 2.5 Flash removed everywhere (all five substrates, all waves).

Every locked file is untouched: nothing under `osf/`, `data/`, `prereg/` changed in any worktree; no
model or API was called; nothing was pushed or deposited. Data copies and run outputs live in the
scratch folder `/Users/pablou/aias/_worktrees/_runner_tmp/truncation_s2/` (not committed); the files
below in `results/` are copies of those outputs. Every Python run used `PYTHONDONTWRITEBYTECODE=1`.

## Answer

| Study | Verdicts that change | Under | How |
|---|---|---|---|
| v0.41 | none (all 6 verdict lines of the 5 hypotheses) | (a), (b) | statistics move; see `results/verdict_table.csv` |
| v1.9 Stage 2 | none (3 primary + 1 descriptive) | (a), (b) | H_Consistency_Reliability p_frame 0.0081 → 0.0168 (a), 0.0352 (b); still < .05 |
| AIAS 2.0 | none: class A in all three | (a), (b) | rho(C*,P) at t3 0.1895 → 0.2417 (a), 0.1802 (b); all within the locked lines |
| v0.34 | **H_CPC_Temporal_Stability CONFIRMED → MARGINAL** | (b) only | v0.21 CV-CPC rho 0.8901 → 0.6953: 3 of 5 substrates ≥ 0.70, the rule needs 4. Not under (a). |
| v1.8 | **H_LowRecallDefined CONFIRMED → PARTIAL-STRUCTURAL** | (a) and (b) | without Flash, Sennheiser (t1) is named by all five other models in all six frames: pi_hat = 1, the by-design ceiling where phi is undefined and CV-CPC_raw is defined, which the locked matrix routes to PARTIAL-STRUCTURAL. |

The v0.34 instrument (CV-CPC) is the one v1.7 retired; AIAS 2.0 cites it as lineage only.

## What the website shows (AIAS 2.0 profiles: P and C*)

`results/brand_profiles_6_vs_5.csv`: every brand, every wave, P and C* on six models and on the five
other models, with ranks within the category; the six-model values reproduce all 336 rows of the
published `osf/aias_2_0/aias_2_0_profiles.csv` (aias-2.0) to the printed 6 decimals (the script stops
otherwise). For v0.19 and v0.23 the five-model values are what (a) and (b) both give; for v0.20–v0.22
they are (b) only. `results/brand_movers.csv`: Sennheiser, plus every headphones or spirits brand whose
C* moves by 10 points or more (0.10 on a 0–1 scale), or whose rank by P or by C* changes, or whose rated
status changes (the column `dC_ge_0.10_points` flags moves of 0.10 points on the 0–100 scale).

- Sennheiser, all three waves: k = [6, 6, 6, 6, 0, 6] (Flash 0). C* 0.0 → 100.0 (rank 8 of 8 rated → 1);
  P 88.89 → 100.00 (t1, t3), 83.33 → 100.00 (t2); P rank 1 in both.
- Headphones: 7 of 8 rated brands move by ≥ 10 C* points in every wave (all move up; the smallest
  move is Grado's, +3.6 to +4.9, so Grado drops from C* rank 1–3 to 5–6). Mean C* of rated
  headphones brands (AIAS 2.0 summaries): t1 59.22 → 87.70, t2 63.92 → 92.14, t3 64.78 → 92.21.
- Premium spirits: no rated brand moves by 10 points (largest +8.2, Del Maguey t2; smallest −2.7,
  Fortaleza t1/t2); ranks by P change for 10 (t1), 12 (t2), 7 (t3) of 24 brands, each by one or
  two places except Fortaleza t1 (4 → 7); no rated-status change.

## Every test re-checked

`results/verdict_table.csv` (written by `summarize_step2.py`) has one row per test: locked verdict and
statistics, (a), (b), and the three files each number is read from (with the key paths in the script).
Locked = the published file (v0.41: `osf/v41/v41_verdicts.json`; v1.9: aias-2.0
`osf/methodology/v1_9/v1_9_verdicts.json`; v0.34: `osf/v34/v34_verdicts.json`; v1.8: the frozen copy
`osf/v41/registries/v1_8_verdicts.json`). For AIAS 2.0 the locked column is `aias20_variant_baseline.json`,
whose class and statistics are identical to the published `aias_2_0_synthesis_data.json` (below).

| Study · test | Locked | (a) | (b) |
|---|---|---|---|
| v0.41 H_Phi_LongHorizon | CONFIRMED rho .6807, p_frame 1.0e-4, n 80 | CONFIRMED .6304, 0.0022, 79 | CONFIRMED .6703, 8.0e-4, 79 |
| v0.41 H_Presence_LongHorizon | CONFIRMED 5/5 ≥ .70 | CONFIRMED 5/5 | CONFIRMED 5/5 |
| v0.41 H_Horizon_Decay phi | MARGINAL D .0185 [−.1323, .1681] | MARGINAL .0052 [−.1731, .1816] | MARGINAL −.0058 [−.1751, .1566] |
| v0.41 H_Horizon_Decay pi_hat | MARGINAL D .0023 [−.0254, .0324] | MARGINAL .00046 [−.0323, .0315] | MARGINAL .00024 [−.0342, .0324] |
| v0.41 H_Drift_Dissociation | CONFIRMED rho .0324 | CONFIRMED .0646 | CONFIRMED −.0537 |
| v0.41 H_Phantom (descriptive) | 56/58 | 55/57 | 52/55 |
| v1.9 H_Presence_Score_Reliability | CONFIRMED .9543 | CONFIRMED .9565 | CONFIRMED .9566 |
| v1.9 H_Dissociation_t3 | CONFIRMED .1895 (n 54) | CONFIRMED .2417 (54) | CONFIRMED .1802 (50) |
| v1.9 H_Consistency_Reliability | CONFIRMED .6473, p_frame .0081 | CONFIRMED .6429, .0168 | CONFIRMED .6546, .0352 |
| v1.9 H_NoComposite_t3 (descr.) | rho(A,P) .9693 | .9767 | .9815 |
| AIAS 2.0 section-5 class | A | A | A |
| v0.34 H_CPC_Temporal_Stability | CONFIRMED 4/5 ≥ .70 | CONFIRMED 4/5 | **MARGINAL 3/5** |
| v0.34 H_CPC_Drift_Beyond_Presence | MARGINAL (v0.19 resid .6108) | MARGINAL (.5150) | MARGINAL (.5150) |
| v0.34 H_Presence_Temporal_Stability | MARGINAL 3/5 ≥ .80 | MARGINAL 2/5 | MARGINAL 2/5 |
| v0.34 H_Phantom (descriptive) | v0.19 8/8, v0.23 15/15 | 7/7, 14/14 | 7/7, 14/14 |
| v1.8 H_CV_Reproduces | CONFIRMED −.6823 (n 55) | CONFIRMED −.7682 (57) | CONFIRMED −.7502 (57) |
| v1.8 H_MeanIndependent | CONFIRMED pooled .0907 | CONFIRMED −.0287 | CONFIRMED .0309 |
| v1.8 H_LowRecallDefined | CONFIRMED (gain 29, ceiling 0) | **PARTIAL-STRUCTURAL** (27, 1) | **PARTIAL-STRUCTURAL** (27, 1) |
| v1.8 H_GradedRecognition | FORWARD-SPEC | not computable | not computable |
| v1.8 H_PositionalDissociation | CONFIRMED −.4025, 9 discordant | CONFIRMED −.4097, 9 | CONFIRMED −.3926, 10 |
| v1.8 H_PhantomSignature | NULL | NULL | NULL |
| v1.8 two-wave phi t1–t2 (descr.) | .6454 (n 83) | .5910 (82) | .5514 (82) |

AIAS 2.0 descriptive lines (`aias20_variant_*.json`, keys `summaries/t*/rho_Cstar_P`,
`descriptive_retest_t2_t3`): rho(C*,P) t1/t2/t3 .0729/.0815/.1895 → (a) .1152/.1380/.2417 → (b)
.1056/.1422/.1802; retest C* t2→t3 .6473 → .6429 → .6546; share not rated at t3 .5179 → .5179 → .5536.
With the stock builder flags (t1/t2 full panel, t3 without Flash; `aias20_stockflags_b_*`): class A;
with the edited copy of the published v1.9 file the builder's own check `rho_Cstar_P_t3_matches_v19`
is False (expected: the copied verdicts are the six-model ones); with the variant (b) v1.9 file it is True.

## Baselines: each locked result reproduced first, by the same code path as its variants

`results/baseline_checks.txt` (written by `baseline_checks.sh`) holds every comparison.

- **v0.41.** Stock `--synthetic` on a byte copy of `osf/v41/data`: the whole `v41_verdicts.json` and the
  three-wave table are identical to the published files. The per-substrate wrapper in mode `baseline`:
  `verdicts` identical, table byte-identical. Wrapper mode `b` = stock `--synthetic` on the Flash-free
  copy: `verdicts` identical, table byte-identical (so the wrapper and the stock path agree both ways).
- **v1.9 Stage 2.** Stock `--stage2-synthetic` on the byte copy: whole file identical. Wrapper `baseline`:
  `verdicts` and `constraints_t3` identical; wrapper `b` = stock on the Flash-free copy, identical.
- **AIAS 2.0.** Builder with the test flags and the published v0.41 and v1.9 files: `aias_2_0_profiles.csv`
  byte-identical; in `aias_2_0_synthesis_data.json` the class, every rho, n, share, retest, the parity
  checks A1–A5, the v0.41 gates, the lineage and the spec are identical. Differences: the build time,
  the anchor field (test mode skips the remote check), the input-path keys (the published build ran
  under `/sessions/...`), and 18 per-substrate mean values (`mean_P`, `mean_C_rated`) that differ in the
  last (16th or 17th) significant digit (e.g. 46.99074074074075 vs 46.99074074074074). They do not depend on the
  hash seed (three seeds give identical summaries here), so they come from floating-point arithmetic on
  a different machine; no verdict, statistic or profile value depends on them. The wrapper
  `aias20_variants.py` in mode `baseline` equals this builder run exactly (summaries, retest, class).
- **v0.34.** Stock `score_v34.py` with HOME at a scratch mirror: the whole file is identical once the
  mirror's copy of `osf/v34/data/v19/phase_a_responses.jsonl` carries its modification date 2026-06-10
  (the v0.19 t2 date in `delta_t` falls back to that file's date; before setting it, `delta_t[0]` was
  the only difference: t2 2026-11-12, 176 days, against 2026-06-10, 21). Wrapper `baseline`: every key identical.
- **v1.8.** Kernel instrument table vs the frozen `v1_8_instrument_table.csv`: 112 rows, all fields equal,
  max abs difference 0.0. Verdicts and two-wave block identical to the frozen record with
  `PYTHONHASHSEED=1`; with seeds 2 and 3 (and an unset seed) only H_MeanIndependent's pooled rho moves,
  in its last (16th) significant digit (…117, …118, …115, …121), because the locked v1.8 code
  iterates a Python set. The
  committed v1.8 outputs were all run with `PYTHONHASHSEED=1`.

## How each variant was run (code paths)

- **Flash-free t3 copy** (`make_t3_copies.py`): every record whose model field is exactly
  `gemini-2.5-flash` (after the `models/` prefix) removed from every file of `osf/v41/data` that has a
  model field, including the provenance sidecar (164 rows) and the interrupted v0.23 run; counts in
  `results/t3_noflash_filter_log.json`. Flash-Lite is kept.
- **v0.41** (b): stock `score_v41.py --synthetic <Flash-free copy> --out <scratch>`; the scorer's
  MODEL_DROP_RULE drops Flash from all three waves (panel_used = five models; MC_Completeness is
  INCOMPLETE by construction). (a): `v41_per_substrate.py --mode a`, which calls score_v41's own
  `run_gates`, `load_wave`, `wave_metrics` (once per keep list, each substrate from its own list) and the
  five hypothesis functions unchanged; only the frame-structure null is transcribed, with the kept models
  looked up per substrate (it reproduces the stock null exactly when the list is the same everywhere).
- **v1.9 Stage 2** (b): stock `score_v1_9.py --stage2-synthetic <Flash-free copy>` (aias-2.0; writes
  `<copy>/_score_v1_9/`). (a): `v1_9_per_substrate.py --mode a`, score_v1_9's `stage2` line for line with
  per-substrate wave metrics and the C* frame null transcribed the same way. Stage 1 (full panel) untouched.
- **AIAS 2.0**: stock builder with the test flags (`--t3 --v41 --v19 --skip-origin --out`), once with an
  edited copy of the published v1.9 file whose `panel_used` drops Flash and once with the variant (b)
  v0.41 and v1.9 files (t3 and t2-on-t3-panel profiles without Flash; t1/t2 full panel, as the builder
  locks them). `aias20_variants.py` applies the variant's keep list to t1, t2 and t3 alike (builder's own
  `wave_rows`, `summarize`, `classify`; parity A1–A5 not re-checked for (a)/(b), Stage 1 being full
  panel) and classifies with that variant's own v0.41 and v1.9 files.
- **Per-brand P and C*** (`brand_profiles.py`): score_v1_9.unit_table on score_v41.wave_metrics with six
  and with five models, all waves.
- **v0.34** (`v34_per_substrate.py`): run with HOME at the scratch mirror `home34/aias` (copies of
  scripts, prereg, osf/v19–v23, osf/v34/data, the v1.7 reference CSV), so the stock scorer's fixed output
  path lands in scratch. Imports the locked score_v34 from the mirror and replaces `wave_t1`/`wave_t2`
  (locked extractors, then Flash's entry dropped from the recall and recognition vectors of the chosen
  substrates) and `saturated` (its literal `range(6)` read from the vector length; identical for six models).
- **v1.8** (`v1_8_kernel.py`): k, pi_hat and phi from score_v41's kernel with the keep list; J from
  v1.8's own `stage0_frame_surfacing` + `jaccard_of` restricted to the kept models (the kernel's J is
  equal to 1e-16 but in a different model order, which moves ties in the phi–J Spearman: with the
  kernel's J the baseline gave −.4019 instead of −.4025, so v1.8's own was used); CPC_raw/CPC_corr from
  v1.8's `cvcpc_of`; then v1.8's `framing_membership` (the v0.35 roster stays the published one) and
  `verdicts`, imported unchanged from `git show v1.8:scripts/score_v1_8.py` (scratch copy, with its
  prereg module). Two-wave phi agreement as in v1.8's `two_wave_reproducibility`, on kernel phi.

## Commands run (scratch S = /Users/pablou/aias/_worktrees/_runner_tmp/truncation_s2; T = this worktree;
## A = /Users/pablou/aias/_worktrees/aias-2.0; PY = /Users/pablou/aias/venv/bin/python3; all with PYTHONDONTWRITEBYTECODE=1)

```
cd $T; $PY analysis/truncation_audit/step2/make_t3_copies.py osf/v41/data $S/t3; diff -rq osf/v41/data $S/t3/full
# v0.41 (AIAS_ROOT=$T)
$PY -u osf/v41/scripts/score_v41.py --synthetic $S/t3/full    --out $S/out/v41_full
$PY -u osf/v41/scripts/score_v41.py --synthetic $S/t3/noflash --out $S/out/v41_noflash
$PY -u analysis/truncation_audit/step2/v41_per_substrate.py --mode {baseline,a,b} --t3 $S/t3/full --out $S/out/v41ps_{mode}
# v1.9 Stage 2 (AIAS_ROOT=$A, cwd $A or $S)
$PY -u $A/osf/methodology/v1_9/scripts/score_v1_9.py --stage2-synthetic $S/t3/full
$PY -u $A/osf/methodology/v1_9/scripts/score_v1_9.py --stage2-synthetic $S/t3/noflash
$PY -u $T/analysis/truncation_audit/step2/v1_9_per_substrate.py --mode {baseline,a,b} --t3 $S/t3/full --out $S/out/v19ps_{mode}
# AIAS 2.0 (AIAS_ROOT=$A, cwd $S); edited copy: published v1_9_verdicts.json with panel_used minus gemini-2.5-flash
$PY -u $A/scripts/aias_2_0_synthesis_data.py --t3 $S/t3/full --v41 $A/osf/v41/v41_verdicts.json --v19 $A/osf/methodology/v1_9/v1_9_verdicts.json --skip-origin --out $S/out/a20_baseline
#   same with PYTHONHASHSEED=0,1,2 --out $S/out/a20_baseline_hash{0,1,2}
$PY -u $A/scripts/aias_2_0_synthesis_data.py --t3 $S/t3/full --v41 $A/osf/v41/v41_verdicts.json --v19 $S/a20_inputs/v1_9_verdicts_published_panel_used_noflash.json --skip-origin --out $S/out/a20_b_edited_published
$PY -u $A/scripts/aias_2_0_synthesis_data.py --t3 $S/t3/full --v41 $S/out/v41_noflash/v41_verdicts.json --v19 $S/t3/noflash/_score_v1_9/v1_9_verdicts.json --skip-origin --out $S/out/a20_b_variant_verdicts
$PY -u $T/analysis/truncation_audit/step2/aias20_variants.py --mode {baseline|a|b} --t3 $S/t3/full --v41 <locked|v41ps_a|v41_noflash> --v19 <locked|v19ps_a|noflash/_score_v1_9> --out $S/out/a20ps_{mode}.json
$PY $T/analysis/truncation_audit/step2/brand_profiles.py --t3 $S/t3/full --published $A/osf/aias_2_0/aias_2_0_profiles.csv --out $T/analysis/truncation_audit/step2/results/brand_profiles_6_vs_5.csv
# v0.34: mirror (cp -Rp of scripts, prereg, osf/v19..v23, osf/v34/data, osf/methodology/v1_7/data/v1_7_cpc.csv into $S/home34/aias)
cd $S/home34/aias; HOME=$S/home34 $PY -u scripts/score_v34.py            # before and after: touch -t 202606101200 osf/v34/data/v19/phase_a_responses.jsonl
HOME=$S/home34 $PY -u $T/analysis/truncation_audit/step2/v34_per_substrate.py --mode {baseline,a,b} --out $S/out/v34ps_{mode}.json
# v1.8 (AIAS_ROOT=$T): git show v1.8:scripts/score_v1_8.py > $S/v18mod/score_v1_8.py; git show v1.8:prereg/v1_8_consistency_instrument_content.py > $S/v18mod/prereg/...
PYTHONHASHSEED=1 $PY -u $T/analysis/truncation_audit/step2/v1_8_kernel.py --mode {baseline,a,b} --v18mod $S/v18mod --out $S/out/v18k_{mode}.json --table $S/out/v18k_{mode}_table.csv
#   baseline also with PYTHONHASHSEED=2,3 and unset (hash-order check)
# results
cp <outputs> analysis/truncation_audit/step2/results/   (names as listed above)
$PY analysis/truncation_audit/step2/summarize_step2.py; $PY analysis/truncation_audit/step2/brand_summary.py
zsh analysis/truncation_audit/step2/baseline_checks.sh > analysis/truncation_audit/step2/results/baseline_checks.txt
```

## Not done

- AIAS 2.0 paper text and figures were not re-built; the class, the summaries and the profiles are.
- v1.8 H_GradedRecognition is FORWARD-SPEC (not computable from the frozen data) in every variant.
- v1.8's per-channel secondary diagnostic (non-gating, v0.20–v0.22 only) was not re-run.
- v0.41's manipulation checks are descriptive and were not re-stated for (a); (b) carries them in its file.
