# DRAFT (not committed to v1.20's records, not deposited on OSF): v1.20 note on merge 5da5ef8 (§5 item 5)

*Drafted 2026-11-22 by the Sentiment Paper A lane of the runner, for the coordinator. Suggested home: a dated Entry 2 in a post-lock continuation file `osf/methodology/v1_20/postlock/DEVIATIONS_continued_v1_20.md` (v1.20's `anchor/DEVIATIONS.md` is in its lock manifest). It records how §5 item 5 was carried out; it is not a change of rule. The checks below were run by code on 2026-11-22 in the worktree `_worktrees/sentiment-paper-a`.*

## Entry 2 — ex ante for the scoring run: the checkout v1.20 scored in (merge 5da5ef8, 2026-11-22)

**Type:** ex ante (before v1.20's Stage J and Stage C), recorded after the fact; procedural.

**What.** v1.20 §5 item 5 requires v1.20's stages to run in a checkout that holds both v1.11's frozen records at their v1.11 paths and v1.20's locked files, "e.g. branch v1.11 merged into the v1.20 branch after the v1.20 tag". On 2026-11-22 (04:15 CST) branch v1.11 at aca9266 (the acquisition record: judge raw records, batch log, plan, guard log, frozen outputs; v1.11 DEVIATIONS Entries 1–2; the Paper B sample replacement files) was merged into `sentiment-successor` as merge commit 5da5ef8 (parents 4bb32e1, v1.20's anchor commit, and aca9266). v1.20's Stage J and Stage C then ran once each in that checkout (Stage J 10:15 UTC, Stage C 10:19 UTC); their outputs were committed as d8efc4e.

**Checks (by code, 2026-11-22).** `git diff --quiet v1.20-prereg-r1 5da5ef8` is empty for every file of v1.20's lock manifest that the merge could reach: `prereg/PRE_REGISTRATION_v1_20.md`, `prereg/config_v1_20.json`, `scoping/`, `dryrun/`, `anchor/DEVIATIONS.md`, `scripts/score_v1_20.py`, `scripts/test_score_v1_20.py`, and the three pinned v1.11 files (`osf/methodology/v1_11/prereg/LOCK_MANIFEST_v1_11.sha256`, `scripts/score_v1_11.py`, `scripts/score_v1_10.py`). Between the tag and 4bb32e1 the only change is the anchor record `anchor/git_anchor_v1_20.json`. The merge adds only v1.11 files (12 files: `osf/methodology/v1_11/anchor/DEVIATIONS.md` Entry 1, `anchor/git_anchor_v1_11.json`, `data/` ×4, `outputs/judge_outputs_frozen_v1_11.json`, `paperB/` ×2, `postlock/DEVIATIONS_continued_v1_11.md`, `scripts/sva_sample_replace_v1_11.py` and its test). v1.20's scorer itself re-checks, before scoring, the imported v1.11 and v1.10 scorers against v1.11's lock manifest, v1.11's raw file against its frozen SHA-256, the tag and the anchor (§5 item 2; it ran and did not refuse).

**Why recorded.** The order and place of the run are part of the pre-registration (§5 items 2–5, §7); the merge is the step that made v1.11's frozen records readable at their paths, and it changed no v1.20 locked file.

**Effect on inference.** None.

**Also noted (for the coordinator, not a deviation of the merge):** v1.20 §5 item 3 lists a "P/C\* cross-check" among Stage C's steps, but `score_v1_20.run_stage_c` does not write the `P_Cstar_v1_9_cross_check` block that v1.11's Stage C writes (v1.11 §2: Stage C "reports any difference between the two tables' P and C\*"). v1_20_verdicts.json therefore has no such block, and Sentiment Paper A says so (§3.3). Whether to record this as a scorer omission (code fix only restoring a rule as written, with results before and after; v1.20 §12) is the coordinator's call.
