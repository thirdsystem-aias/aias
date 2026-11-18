# AIAS v0.40 — DEVIATIONS log

Entries are added in order and never edited after the lock (tag `v0.40-prereg-r1`); a correction is a new entry.

## Entry 0 (ex ante, before the lock): conflict-of-interest screen, Cheil Worldwide and Iris

**Date:** 2026-11-12 (runner). **Status:** ex ante; written before the lock and before any study probe.

**What was screened.** Every brand of the frozen v0.40 registry (2026-11-12): the 11 airline brands of `registries/out/airlines_current.csv`, the 25 bank holders of `registries/out/banks_current.csv` (with their brand and alias fields) and the 27 rows of `registries/out/exits_and_controls.csv` (24 ghosts and 3 living-brand controls, with aliases and successors), 63 rows in all; as a context check, the scan inputs `bank_scan_class.csv`, `airline_scan_class.csv`, `aliases_current.csv`, `exit_events.csv` and `out/bank_exit_scan.csv`, `out/airline_exit_scan.csv` (whole text).

**Against what.** The five brands with a recorded Cheil Worldwide or Iris agency tie in the programme's conflict-of-interest note of 2026-11-12 (record: v0.62 DEVIATIONS Entry 0, Part F): Chevrolet (for GM Korea, 2017), BMW (UK consumer public relations, 2018), Bentley (experiential agency of record in the Americas from 2021), Jack Daniel's (UK digital agency from 2022, since replaced) and Eucerin (search marketing for Beiersdorf from 2024). Patterns, case-insensitive: `chevrolet|chevy|gm korea`, `\bbmw\b`, `bentley`, `jack daniel`, `eucerin|beiersdorf`.

**Result.** No match: none of the 63 registry rows names or aliases any of the five brands, and none of the five patterns occurs anywhere in the six scan files. No v0.40 registry brand has a recorded Cheil Worldwide or Iris tie, so the conflict-of-interest section adds no agency-work sentence and no COI sensitivity is declared.

**Scope.** The screen compares the registry with the programme's record of ties; it is not a new search of agency work for each airline and bank brand. A tie found later is a DEVIATIONS entry, with every result reported with and without the brand concerned.

**Script.** Screen run by the runner with a one-off script (pattern match over the CSVs above); no data, probe, threshold or script of the study was changed.

## Lock record (2026-11-16, 7:00 pm CT / 2026-11-17 01:00 UTC): pre-registration locked as tag v0.40-prereg-r1

**What.** The pre-registration, probe set, frozen registries and scripts were locked at the time set when the pre-registration reached Pablo (Mon 11/16, 7 pm CT); no hold was typed. No study probe has been sent; collection starts only after this tag is pushed and the OSF deposit is made.

**Changes at the lock (not deviations; no hypothesis, threshold, probe, registry row, model, setting or decision rule changed).** (1) §9's test count corrected to what the deposited test record shows: `test_acquire_v0_40.py` 29 of 29 (the text still said 21 of 21 after the guard carry-over tests were added in commit 36770bd). (2) `LOCK_MANIFEST_v0_40.sha256` refreshed: four files had changed since the manifest was written (the pre-registration text above, `acquire_v0_40.py`, its test file and its test record, from the technical-check carry-over), and the Fable 5.2 technical-check record `prereg/feasibility_check_v0_40.json` was added (46 files; every checksum verified). Test suites re-run at the lock: acquire 29/29, pre-lock 54/54, score 44/44, all mock (no model call).

## Collection start (2026-11-17, ~7:10 pm CT / 2026-11-18 01:10 UTC): anchor record written before the first `--collect`

**What.** The first `acquire_v0_40.py --collect` refused: `osf/v40/anchor/osf_anchor_v0_40.json` did not exist. The anchor itself happened at the lock (tag v0.40-prereg-r1 on origin, commit a53d2b7; OSF ec6wh v40/prereg 17 files and v40/registries 18 files, every file verified by SHA-256 at 01:07–01:08 UTC on 2026-11-17), but the lock step did not write the record file the guard reads. The runner wrote it from the lock-time OSF receipts and the tag on origin (it names the commit, the tag object, both deposits and the receipts' SHA-256). **Not a deviation from the pre-registration:** no hypothesis, threshold, probe, registry row, model, setting, script or decision rule changed; no study probe had been sent before this record existed. The record is committed with the collection data.
