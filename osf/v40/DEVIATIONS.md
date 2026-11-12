# AIAS v0.40 — DEVIATIONS log

Entries are added in order and never edited after the lock (tag `v0.40-prereg-r1`); a correction is a new entry.

## Entry 0 (ex ante, before the lock): conflict-of-interest screen, Cheil Worldwide and Iris

**Date:** 2026-11-12 (runner). **Status:** ex ante; written before the lock and before any study probe.

**What was screened.** Every brand of the frozen v0.40 registry (2026-11-12): the 11 airline brands of `registries/out/airlines_current.csv`, the 25 bank holders of `registries/out/banks_current.csv` (with their brand and alias fields) and the 27 rows of `registries/out/exits_and_controls.csv` (24 ghosts and 3 living-brand controls, with aliases and successors), 63 rows in all; as a context check, the scan inputs `bank_scan_class.csv`, `airline_scan_class.csv`, `aliases_current.csv`, `exit_events.csv` and `out/bank_exit_scan.csv`, `out/airline_exit_scan.csv` (whole text).

**Against what.** The five brands with a recorded Cheil Worldwide or Iris agency tie in the programme's conflict-of-interest note of 2026-11-12 (record: v0.62 DEVIATIONS Entry 0, Part F): Chevrolet (for GM Korea, 2017), BMW (UK consumer public relations, 2018), Bentley (experiential agency of record in the Americas from 2021), Jack Daniel's (UK digital agency from 2022, since replaced) and Eucerin (search marketing for Beiersdorf from 2024). Patterns, case-insensitive: `chevrolet|chevy|gm korea`, `\bbmw\b`, `bentley`, `jack daniel`, `eucerin|beiersdorf`.

**Result.** No match: none of the 63 registry rows names or aliases any of the five brands, and none of the five patterns occurs anywhere in the six scan files. No v0.40 registry brand has a recorded Cheil Worldwide or Iris tie, so the conflict-of-interest section adds no agency-work sentence and no COI sensitivity is declared.

**Scope.** The screen compares the registry with the programme's record of ties; it is not a new search of agency work for each airline and bank brand. A tie found later is a DEVIATIONS entry, with every result reported with and without the brand concerned.

**Script.** Screen run by the runner with a one-off script (pattern match over the CSVs above); no data, probe, threshold or script of the study was changed.
