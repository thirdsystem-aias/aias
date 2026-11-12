# Truncation audit (read-only), Nov 12, 2026

Question: did any model's answers end on the output-token limit before naming a brand, and which
Presence and Consistency values rest on those answers? Branch `truncation-audit`, cut from `v0.41`
(the branch that holds `osf/v41`). Nothing under `osf/`, `data/` or `prereg/` is changed; no model API
is called; nothing is pushed.

Run: `~/aias/venv/bin/python3 analysis/truncation_audit/truncation_audit.py` (about 30 s). It re-executes
itself through score_v41's HOME shim so every scorer import resolves to this worktree, and writes no
`__pycache__`. Every number below is in `results/`.

## What it does

- **Archive** = the Consistency panel's inputs (AIAS 2.0): substrates v0.19 to v0.23; waves t1
  (`osf/v19`..`osf/v23`), t2 (`osf/v34/data`), t3 (`osf/v41/data`); six models; the six Phase B (open
  category) answers per model, 540 answers.
- **Brand matching is the scorer's own**: v0.19 `acquire_v0_19.detect_mentions_in_response`; v0.20 to
  v0.22 `score_v33.RECON_CFG` `detect_mention`; v0.23 `brand_mentions` (= `score_v0_23.find_brand_mentions`).
  Per-answer counts reconcile exactly to `score_v41.load_wave` and to `osf/v41/v41_three_wave_table.csv`
  (2,016 brand × model cells, 0 mismatches); the script stops on any mismatch.
- **Ended on the cap** (in this order of evidence): `finish_reason` (t3 only; the v41 sidecar matched
  call by call; score_v41's `TRUNC_REASONS`); `tokens_at_cap` (output tokens ≥ cap, models without hidden
  thinking tokens; agrees with the finish reason on 30 of 30 t3 v0.19 answers); `identical_to_t3`
  (byte-identical text to the t3 answer, same model and question, no thinking tokens); else
  `not_recorded`. t1 and t2 recorded no finish reasons and, except v0.19, no token counts.
- **Cut before the first brand** = ended on the cap and the scorer's matcher finds no registry brand.
- **Caps** are read from the runners (identical blobs at t2, t3 and HEAD): v0.19 1,024 (all models);
  v0.20 to v0.22 2,048 for Claude and GPT, no limit sent for Gemini; v0.23 2,048 (all).

## Files (`results/`)

| File | Content |
|---|---|
| `omnibus_table.csv` | substrate × wave × model: answers, ended on cap, evidence, cut before first brand, not recorded, zero-brand answers, brands named (= column total of k_per_model), tokens, characters |
| `omnibus_answers.csv` | the 540 answers, one row each, with the brands named and the last 60 characters |
| `touched_brands.csv`, `touched_summary.csv` | brands whose P and C* inputs rest on cut-off answers, with k_per_model and the published AIAS 2.0 P, C*, rated, n_mentions (`aias-2-0-data-locked:osf/aias_2_0/aias_2_0_profiles.csv`) |
| `phase_a_t3.csv` | t3 recognition answers ending on the cap, and each model's recognized count (C_P input) per wave |
| `newer_collections.csv` | v0.38, v0.39 (legacy and current arm, search off/on), v0.42 = t4 (current arm, search off/on) |
| `coding_calls.csv`, `not_collected.csv` | judge and coding calls; studies with no answers collected yet |
| `truncation_audit_results.json` | all of the above plus the checks (runner caps, sidecar matching, reconciliation, claims) |

## Headline results

- Headphones (v0.19): Gemini 2.5 Flash names 0 of 16 brands in t1, t2 and t3 (other models 29–38,
  29–35, 28–36). t3: 6 of 6 answers `MAX_TOKENS`, all before the first brand (38–41 visible tokens,
  196–227 characters). t1/t2: finish reason not recorded; 6 of 6 answers name no brand (38–54 visible
  tokens, 189–315 characters; same runner and cap). Flash k = 0 for all 16 brands in all waves.
- Premium spirits (v0.23): affected, partly. t3: 6 of 6 Flash answers `MAX_TOKENS` after 1,585–1,965
  thinking tokens of 2,048; 5 cut before the first registry brand; Flash names 2 (others 16–25). t1/t2:
  not recorded; Flash names 4 and 5 (others 17–26, 16–23); 4 and 3 answers name no registry brand.
- v0.20 to v0.22: no answer ended on a cap at t3; t1/t2 not recorded; no zero-brand answers except one
  Flash-Lite answer (v0.21 t2).
- Paper §3.6 "Gemini 2.5 Flash 35%" = 58 of 164 calls (all sidecar calls, incl. the interrupted
  spirits run): reproduced with `score_v41.mc_truncation`. Of the 852 final t3 answers, Flash ended 36 of
  142 on the cap; of its 30 Phase B answers, 12 (all 6 headphones, all 6 spirits).
- Newer collections: Flash at the 2,048 cap ended 19 of 22 (v0.38) and 26 of 30 (v0.39 legacy arm)
  answers there, 5 and 15 before the first brand. Current arm (16,384; v0.39 and t4, search off and on):
  0 answers at the cap.

## Draft pre-lock check (text only; not in any pre-registration)

**Rule.** A study is not locked while any panel model, in a live dry run of the study's own questions,
returns an answer that ends on the output-token limit before naming a brand of the study's registry.

1. Dry run: every scored question once per model and condition (search off/on), through the locked
   call functions (same cap, thinking or reasoning setting, temperature, tools, SDK). A neutral prompt
   ("Reply with the single word: ready", as in the v0.40 and v0.41 feasibility checks) does not count.
2. Record per call: finish reason, visible output tokens, thinking tokens, text. Missing fields fail the
   check for that model.
3. Per answer: `at_cap` = finish reason in {length, max_tokens, MAX_TOKENS} (also after an enum prefix),
   or visible + thinking tokens ≥ cap when no finish reason is returned; `named` = registry brands found
   by the study's own scorer matcher; `cut_before_first_brand` = `at_cap` and `named` = 0.
4. **Blocks the lock:** any model with 1 or more `cut_before_first_brand` answers (zero tolerance), or
   missing finish reasons/tokens. **Also blocks unless the pre-registration states the handling before
   the lock** (higher cap and a repeated dry run; a thinking budget, as v0.40 sets for Gemini 2.5 Flash;
   or the model's cells pre-specified as excluded, with a with/without sensitivity run): any other answer
   at the cap, or any answer whose thinking tokens reach half the cap. In this archive the half-cap line
   separates the cases: Gemini 2.5 Flash reached it in 19 of 22 (v0.38) and 26 of 30 (v0.39) answers,
   exactly its cap hits, and spent 1,585–1,965 of 2,048 in v0.23 t3; the current models' largest share
   was 0.17 of 16,384 (GPT-6 Astra, t4, search on).
5. A re-wave bound to a verbatim runner (t2, t3, t5) runs the same check; if it fails, the runner stays
   verbatim and the handling is pre-registered instead.

## Step 2 inventory (not run): re-scoring without given model × substrate cells

| Study | Scorer (branch) and output | Inputs | Without cells? |
|---|---|---|---|
| AIAS 2.0 | `scripts/aias_2_0_synthesis_data.py` (aias-2.0) → `osf/aias_2_0/aias_2_0_synthesis_data.json`, `aias_2_0_profiles.csv` (the site's P and C*) | t1/t2/t3 via score_v41.load_wave; `v1_9_calibration.json` (parity A1–A5); `v41_verdicts.json`, `v1_9_verdicts.json`; lineage verdict files | Test flags `--t3 DIR --v41 FILE --v19 FILE --skip-origin --out DIR`. t3 profiles use `panel_used` of the v1.9 verdicts file, so an edited copy without gemini-2.5-flash drops it from t3 (and t2-on-t3-panel) profiles, panel-wide. t1/t2 profiles are full panel and parity-locked: no flag. |
| v0.41 | `osf/v41/scripts/score_v41.py` (v0.41) → `osf/v41/v41_verdicts.json`, `v41_three_wave_table.csv` | t1 `osf/v19..v23`, t2 `osf/v34/data`, t3 `osf/v41/data` (+ sidecar), `osf/v41/registries` (P1/P2), `osf/v34/v34_verdicts.json` (P3) | `--synthetic DIR --out OUT` scores a t3 folder with the same code as `--run` (never `--run`: it writes `osf/v41`). A model with no t3 answers is dropped from all three waves (MODEL_DROP_RULE; `phi_m` handles 5 models); a model missing in only some substrates halts ("partially failed"). So: a filtered copy of `osf/v41/data` without every gemini-2.5-flash row removes Flash everywhere; per-substrate cells need a wrapper with a per-substrate keep list. |
| v1.9 | `osf/methodology/v1_9/scripts/score_v1_9.py` (v1.9): Stage 1 → `prereg/v1_9_calibration.json`, Stage 2 → `v1_9_verdicts.json` | as v0.41 (imports score_v41) | Stage 2: `--stage2-synthetic DIR` (writes `DIR/_score_v1_9`; `--stage2 --t3 DIR` writes into `osf/methodology/v1_9`) on the same filtered t3 copy drops Flash from t2 and t3 metrics, panel-wide. Stage 1 is full panel (`full = range(M)`): no flag. |
| v0.34 | `scripts/score_v34.py` (v0.34) → `~/aias/osf/v34/v34_verdicts.json`, fixed path, no flags | t1 `osf/v19..v23` (score_v33, score_v0_31), t2 `osf/v34/data` | No flag; fixed six-model PANEL; a filtered input can only zero a model's counts, not remove it. Needs a wrapper that drops the model from the per-brand recall/recognition vectors of chosen substrates before `score()` (cv_cpc and c_p take any length), run under a HOME shim to a scratch tree. |
| v1.8 | `scripts/score_v1_8.py` (v1.8; `--run` only) → `osf/methodology/v1_8/v1_8_verdicts.json`, instrument table, fixed path | t1 omnibus via score_v33 + v1.7 reconciliation; t2; `v33_eta2.csv`, `v35_phantom_roster.csv`, v0.36 stratum (materialized per `v1_8_materialization_manifest.json`) | No flag; M = 6 is asserted from the locked module. A reduced panel needs code: score_v41's kernel (`wave_metrics` with a keep list; P1 reproduces v1.8's 112 rows on the full panel) is the existing implementation. |
