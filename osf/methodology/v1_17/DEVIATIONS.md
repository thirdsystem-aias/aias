# v1.17 — Deviations

Entries are dated, written before the outputs they affect, and give the reason. No deviation so far; Entry 0 records an ex-ante handling, not a deviation.

## Entry 0 — Conflict-of-interest handling (ex ante, Nov 12, 2026)

No new brand selection and no new collection: v1.17 re-analyses v0.42's t4 answers and v0.41's three-wave table on the registries of v0.19–v0.23. Each registry's conflict-of-interest handling is carried forward from its source record unchanged (v0.19 with the November 10, 2026 Denon correction; v0.22's supply relationships). The agency ties found by v0.62's screen (DEVIATIONS Entry 0, Parts F–G of v0.62) are handled as v0.62 decided on Nov 12, 2026: the five brands stay in every analysis, as Denon does, and the main estimates are also reported without them and Denon (S-COI, 106 brands; `COI_FLAGGED_NAMES` in `scripts/v1_17_lib.py`, the same set as v0.62's `COI_FLAGGED`). The disclosure is in the pre-registration's Declarations (§11).

## Run record (Nov 12, 2026)

`analyze_v1_17.py --run` was run once, at 2026-11-12T08:52:35Z (after tag `v1.17-prereg-r1` reached origin at 08:48:26Z). It did not crash and was not re-run. Its code was unchanged from the lock.

## Entry 1 — Chart 1 layout (Nov 12, 2026, after the run; no number affected)

On the real data the standard errors sit far below the dry run's, so in chart 1 the legend and the "observed | projected" label overlapped the 0.10 line. In `scripts/build_charts_v1_17.py` (`chart_se_runs`) the y-axis now starts at 0 and reaches at least 0.115, the legend sits at centre right, and the label sits at 70% of the axis height. Layout only: no data, estimate or other chart changed. The script's hash therefore differs from `LOCK_MANIFEST_v1_17.sha256`.

## Entry 2 — v0.40's legacy arm has three runs (Nov 12, 2026)

§6 item 3 of the pre-registration assumed v0.40's legacy arm makes one call per probe and model (from v0.40's early brief). v0.40's frozen probe set (`_worktrees/v0.40`, commit 1c2bc9f, `osf/v40/scripts/build_probes_v0_40.py` line 148) has `"runs_per_cell": 3` in the legacy arm as well. The results note says so and replaces the template's legacy-arm line by hand; the rule's substance holds (v1.17 has no legacy run-to-run estimate; the omnibus figures are not one). As §5 allows, the note's wording around the numbers was edited by hand. Every number in it comes from `outputs/v1_17_results.json`, or is computed directly from it (for example √(σ̂²_frame ÷ 16)), or comes from the cited v0.40 files.
