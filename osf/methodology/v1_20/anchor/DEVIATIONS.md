# DEVIATIONS — v1.20 (proposed id; Sentiment Paper A, successor re-scoring of v1.11's judge replies)

## Entry 0 — ex ante (2026-11-13, draft r0, before the lock)

**Type:** ex ante (COI carry-forward, pre-lock record). No v1.11 judge reply exists; v1.20 makes no model call; no valence, S, P, C\* or Ranking value has been computed by or for v1.20.

**COI.** v1.20 makes no brand selection and adds no registry, unit or judge call: it re-scores v1.11's stored judge replies on v1.11's frozen units. The conflict-of-interest handling of v1.11 applies unchanged, as recorded in v1.11 DEVIATIONS Entry 0 (source records quoted verbatim there, the November 10, 2026 correction, the registry string screen and its stated scope) and in v1.11 PRE_REGISTRATION §14, which v1.20 §14 quotes verbatim. Sensitivity SD (without Denon's v0.19 units) is kept.

**Pre-lock record (what was read, computed and printed for this draft; lane C, 2026-11-13, about 1:20–2:45 am CT).**
1. Read: v1.11's pre-registration, judge prompt and output schema, DEVIATIONS (Entries 0 and 1), and the code of `score_v1_11.py` (parser, outcomes, JUDGE_FAIL check, Stage J) and `judge_v1_11.py` (reply extraction, call records). No v1.11 judge output exists to read.
2. v1.15 (`_worktrees/v1.15`, read-only): DEVIATIONS Entries 1–2 (`postlock/DEVIATIONS_continued_v1_15.md`), the frozen-outputs record, and by code only the raw judge records (`data/judge_raw_v1_15.jsonl`, SHA-256 checked) and the unit table's `unit_id` and `set` columns. Printed and saved: format and parse-outcome counts only (`scoping/format_counts_v1_15.json`). No reply text, valence, evidence quote or score was printed, saved or computed.
3. Truncation audit (`_worktrees/truncation-audit` at `ea2b787`, read-only): README and the result tables `phase_a_t3.csv`, `omnibus_table.csv` (columns of counts), `touched_summary.csv`, `not_collected.csv`, `coding_calls.csv`, and the header of `omnibus_answers.csv`. Its `last_60_chars` column was not read.
4. v1.11's E answer files (eight CSVs at tag `v1.11-prereg-r1`): column names, `call_status` values, and per answering model the number of answers and the median, 90th percentile and maximum character length and the counts at ≥ 3,000 and ≥ 4,000 characters, computed by code. No answer text was printed. `run_aias_v2.py` read for its output-token settings.
5. Header row of v1.11's unit table (column names only).
6. Repository refs, tags, recent commit subjects and the master documents searched for study ids (§0 of the pre-registration); the claude.ai project documents searched for "v1.20" and the release plan.
