# DEVIATIONS — v1.16 (Ranking, the last measure: co-mention precedence)

## Entry 0 — ex ante (2026-11-12, before the lock)

**Type:** ex ante (decision of record, pre-lock record, COI screen, anchor preamble). No precedence (PREC) value, no pairwise win record and no H1–H5 statistic has been computed on a real answer.

**Decision of record.** Pablo, Wed Nov 11, 2026, 11:22 pm: “RANKING: (c), with one condition: this is the last redesign. Report v1.14 as MARGINAL, let the next part that passes its gate make the next release, and pre-register one new Ranking measure, justified in advance from the method and the literature (SparkToro/Gumshoe; Boffa et al.), stating in that pre-registration that if it does not PASS, Ranking is reported as part of Presence and not as a separate AIAS component; no further redesigns.” The pre-registration carries the consequence clause in §8 and the scorer prints it with the gate (`score_v1_16.consequence`).

**Branch.** `v1.16` was created from `v1.14` at `3129674` (v1.14 Stage 1), which holds v1.14's Stage 1 outputs used here as inputs. Nothing of v1.10 or v1.14 is changed.

**Pre-lock record (2026-11-12).**

1. Input parity (`python3 scripts/score_v1_16.py --parity` → `prereg/input_parity_v1_16.json`): pins verified; counts of answers, rankable answers, rankable rows and co-mentioned pairs per wave; units at the rating floor and their joins with P and C\*. All checks pass: v1.10's 31 rank tables match its verdicts file (hashes and row counts); t1–t3 n's 55 / 54 / 54 equal v1.10's published n's for P and C\*; t4 reproduces v1.14 Stage 1 (540 answers; 1,641 S0 and 1,375 S1 rankable rows; 71 units at the floor; 71 with P; 70 with C\*). No PREC, correlation or first-position concentration on real data.
2. Precision note (`scripts/precision_note_v1_16.py`): analytic, no data.
3. Dry run (`--dry-run` → `dryrun/`): the full pipeline on synthetic data in the real file formats, three worlds with known answers, 10,000 permutation and 10,000 shuffle draws; all three worlds give the expected verdicts (pre-registration §11). Two earlier versions of synthetic world A (with 100 shuffle and 200 permutation draws) returned H1 FALSIFIED because the drawn precedence happened to correlate with popularity among the rated brands; this was checked with `dryrun/check_world_A_versions.py` (synthetic only) and world A was rebuilt. No scorer rule, statistic or threshold changed (§11).
4. Unit tests: `python3 -m unittest scripts/test_score_v1_16.py`, 23 tests, all pass; v1.14's 34 tests also pass in this worktree (the imported code is unchanged).

Seen before v1.16 existed, and declared in pre-registration §4.3: every statistic v1.10 and v1.14 published on the same waves (MNP and all six v1.10 candidates at t1–t3; MODE at t4 with its sensitivities; v1.14's per-unit MODE values).

**COI screen.** No new brand selection: the five omnibus registries (v0.19–v0.23, 112 units) as v1.10 and v1.14 use them. Each substrate keeps its source-phase handling: the v0.19 AKG → Denon substitution with the correction of November 10, 2026 (Denon owned by Harman International, a wholly owned subsidiary of Samsung Electronics, since September 23, 2025); the v0.22 tier-2/3 supply relationships (Harman International, Samsung SDI, Samsung Display; supply, not ownership). Carried from the conflict-of-interest screen of v0.62 (DEVIATIONS Entry 0, Part F): Cheil Worldwide (a Samsung-group marketing company in which Samsung Electronics holds 28.43%) or its agency Iris has done agency work for Chevrolet, BMW, Bentley, Jack Daniel's (registry key S03 in v1.10's v0.23 registry) and Eucerin. Handling: all units stay in every primary analysis; separability is also reported without Denon (S7) and without Denon and the five agency-tie brands (S-COI, 106 units). Wording: pre-registration §15.

**Anchor preamble.** Content lock → `prereg/LOCK_MANIFEST_v1_16.sha256` → commit → tag `v1.16-prereg-r1` → push branch and tag → OSF deposit of `osf/methodology/v1_16/` (`prereg/`, `anchor/`, `dryrun/`, `scripts/`, `README.md`) with SHA-256 verified → `python3 scripts/score_v1_16.py --write-anchor --osf-note "<OSF location>"` → commit the anchor → `--run` once (refuses without the tag, the anchor file and an unchanged lock manifest, and if results exist).
