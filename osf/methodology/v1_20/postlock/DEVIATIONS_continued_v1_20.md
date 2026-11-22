# AIAS v1.20 — Sentiment Paper A, successor re-scoring: deviations log, continued after the lock (kept separately because `anchor/DEVIATIONS.md` is listed in `prereg/LOCK_MANIFEST_v1_20.sha256`)

This file continues `osf/methodology/v1_20/anchor/DEVIATIONS.md` (Entries 0 and 1, ex ante, written before the lock) under the deviations policy v1.20 takes from v1.11 (§13: id, date, ex ante or ex post, what, why, effect on inference). From Entry 2 on, entries are kept here, so no file listed in v1.20's lock manifest changes.

## Entry 2 — ex ante for the scoring run: the checkout v1.20 scored in (merge 5da5ef8, 2026-11-22)

**Type:** ex ante (before v1.20's Stage J and Stage C), recorded after the fact; procedural.

**What.** v1.20 §5 item 5 requires v1.20's stages to run in a checkout that holds both v1.11's frozen records at their v1.11 paths and v1.20's locked files, "e.g. branch v1.11 merged into the v1.20 branch after the v1.20 tag". On 2026-11-22 (04:15 CST) branch v1.11 at aca9266 (the acquisition record: judge raw records, batch log, plan, guard log, frozen outputs; v1.11 DEVIATIONS Entries 1–2; the Paper B sample replacement files) was merged into `sentiment-successor` as merge commit 5da5ef8 (parents 4bb32e1, v1.20's anchor commit, and aca9266). v1.20's Stage J and Stage C then ran once each in that checkout (Stage J 10:15 UTC, Stage C 10:19 UTC); their outputs were committed as d8efc4e.

**Checks (by code, 2026-11-22).** `git diff --quiet v1.20-prereg-r1 5da5ef8` is empty for every file of v1.20's lock manifest that the merge could reach: `prereg/PRE_REGISTRATION_v1_20.md`, `prereg/config_v1_20.json`, `scoping/`, `dryrun/`, `anchor/DEVIATIONS.md`, `scripts/score_v1_20.py`, `scripts/test_score_v1_20.py`, and the three pinned v1.11 files (`osf/methodology/v1_11/prereg/LOCK_MANIFEST_v1_11.sha256`, `scripts/score_v1_11.py`, `scripts/score_v1_10.py`). Between the tag and 4bb32e1 the only change is the anchor record `anchor/git_anchor_v1_20.json`. The merge adds only v1.11 files (12 files: `osf/methodology/v1_11/anchor/DEVIATIONS.md` Entry 1, `anchor/git_anchor_v1_11.json`, `data/` ×4, `outputs/judge_outputs_frozen_v1_11.json`, `paperB/` ×2, `postlock/DEVIATIONS_continued_v1_11.md`, `scripts/sva_sample_replace_v1_11.py` and its test). v1.20's scorer itself re-checks, before scoring, the imported v1.11 and v1.10 scorers against v1.11's lock manifest, v1.11's raw file against its frozen SHA-256, the tag and the anchor (§5 item 2; it ran and did not refuse).

**Why recorded.** The order and place of the run are part of the pre-registration (§5 items 2–5, §7); the merge is the step that made v1.11's frozen records readable at their paths, and it changed no v1.20 locked file.

**Effect on inference.** None.

## Entry 3 — ex post: the P/C\* cross-check against the v1.9 unit table, omitted by the scorer, completed post hoc (2026-11-22)

**Type:** ex post; a pre-registered check the scorer did not run, completed after the verdicts by separate code. No verdict, statistic, rule, threshold, seed or output file of v1.20 changed, and neither stage was re-run.

**What.** v1.20 §5 item 3 lists among Stage C's steps "P and C\* are opened (join check, P/C\* cross-check, window counts)", following v1.11 §2 (Stage C "reports any difference between the two tables' P and C\*"). `score_v1_20.run_stage_c` reads P and C\* with v1.11's code and writes the join check and the window counts, but not the `P_Cstar_v1_9_cross_check` block that `score_v1_11.run_stage_c` writes; `v1_20_verdicts.json` (commit d8efc4e) has no such block. On Sun 2026-11-22 `papers/v1_20/v1_9_cross_check_v1_20.py` (branch `sentiment-paper-a`) ran v1.11's comparison (the nested `_differs` of `score_v1_11.run_stage_c`, copied verbatim; tolerance 1e-9) on the two tables v1.11's input manifest pins, after checking both SHA-256 against `osf/methodology/v1_11/registries/INPUTS_MANIFEST_v1_11.json` (`osf/aias_2_0/aias_2_0_profiles.csv` 022ef56e…, `osf/methodology/v1_9/v1_9_unit_table.csv` 3a02f957…; both equal). Output: `papers/v1_20/v1_9_cross_check_v1_20.json`.

**Result.** 336 rows compared, all 336 keys in both tables. Under the 1e-9 tolerance 335 of 336 rows are flagged as differing. The v1.9 table prints P and C\* to 4 decimals and the profiles table to 6; compared at 4 decimals, 0 of 336 rows differ in P, in C\* or in which rows carry a C\* (163 rows rated in both); the largest absolute differences are 4.8e-05 (P) and 4.7e-05 (C\*), within the rounding of the 4th decimal. Sentiment Paper A (§3.3) reports this, labelled as a dated post-hoc completion.

**Why recorded.** The check is pre-registered and its absence from the scorer's output is an omission, not a rule change; completing it outside the scorer keeps v1.20's one-shot stages and outputs as they ran. The scorer itself is not changed (a code fix restoring the block would be a v1.20 §12 matter).

**Effect on inference.** None: the cross-check is never a verdict input (v1.11 input manifest: "never a verdict input"), and P and C\* agree with the v1.9 table to its printed precision.
