# Sentiment Paper A (v1.11 study, scored under its successor rule v1.20): build commands

Branch `sentiment-paper-a` = `origin/sentiment-successor` (d8efc4e: v1.20 outputs) + merge of `v1.11-paper` (the pre-data pipeline, 6400af8) + merge of `v1.11` (7635e86: v1.11's Stage J console record). Forked from `papers/v1_11/` (case A pipeline); this fork reads v1.20's outputs and reports case B: v1.11's own Stage J halted, and v1.20's verdicts are Sentiment Paper A's result (v1.20 §7, switch Q6). No number is typed by hand.

From the worktree root, system Python 3.14 (numpy, matplotlib, pypdf, PIL), pandoc + xelatex + Carlito, pdftoppm:

```
export PYTHONDONTWRITEBYTECODE=1
python3 papers/v1_20/make_run_values_v1_20.py   # call-record metadata -> papers/v1_20/run_values_v1_20.json (raw SHA-256 checked against the frozen record; reply text never read out)
python3 scripts/build_charts_v120.py            # reports/figs/v120/chart_01..06 (+ _preview.png)
python3 papers/v1_20/fill_paper_v1_20.py        # papers/v1_20/v1_20_paper_draft.md + _provenance.json
python3 scripts/build_paper_v1_20.py            # papers/v1_20/v1_20_paper.pdf
pdftoppm -r 80 -png papers/v1_20/v1_20_paper.pdf /tmp/v120_pf/p   # look at every page
```

Inputs: `osf/methodology/v1_20/outputs/` (`v1_20_verdicts.json`, `stage_j_v1_20.json`, `comparison_v1_11_v1_20.json`), `osf/methodology/v1_20/scoping/cut_units_v1_20.json`, `osf/methodology/v1_11/outputs/judge_outputs_frozen_v1_11.json` and `stage_j_run_v1_11.log`, `osf/methodology/v1_11/data/plan_v1_11.json` and `judge_raw_v1_11.jsonl` (metadata only), both tags and anchor records, the three DEVIATIONS files.

The fill refuses: synthetic files; wrong prereg tag; any SHA-256 link broken (Stage J ↔ verdicts, frozen ↔ Stage J, plan ↔ frozen, raw ↔ run values, cut list ↔ verdicts); case not B; v1.11's console halt list not equal to the recomputed one; verdict words not reproduced by `score_v1_11`'s own verdict functions; and any template sentence whose premise (sign, band, count, "no API error", "under the US$80 pause", ...) the data do not meet (`need(...)`).

Drafts for the coordinator (not committed to OSF or to v1.11/v1.20 records): `drafts/DRAFT_v1_11_DEVIATIONS_continued_Entry_3.md`, `drafts/DRAFT_v1_20_note_merge_5da5ef8.md`.

Not covered: synthetic scenarios and tests of this fork (the v1.11 pipeline's tests cover the engine and case A); the vendors' invoices (not a machine output).
