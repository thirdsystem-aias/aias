# v1.11 Sentiment Paper A: the commands after scoring

Built on branch `v1.11-paper` (from `v1.11` at `95c3fa1`, DEVIATIONS Entry 1, after tag `v1.11-prereg-r1`) on 11 November 2026, before any judge call: the paid judge run cannot start before 22 November 2026 06:00 UTC (pre-registration §8). Mirrors the v1.12 Coverage and v1.13 Grounding pipelines. Paper A is a methodology paper: no Third System report and no SSRN packet (methodology papers no longer go to SSRN by default, CLAUDE.md, 11 November 2026). Every builder reads only the scorer's and judge runner's outputs; no number is typed by hand. Results and Discussion were written in advance as alternative sentences, one for each pre-registered outcome, and the fill script picks one from the verdicts. Verdict words are printed exactly as `score_v1_11.py` writes them, and the fill refuses a verdict file whose words the locked scorer's own functions do not reproduce from its statistics.

## Inputs

| File | Written by | Folder |
|---|---|---|
| `v1_11_verdicts.json` | `score_v1_11.py --stage C` | `osf/methodology/v1_11/outputs/` |
| `stage_j_v1_11.json` | `score_v1_11.py --stage J` | `osf/methodology/v1_11/outputs/` |
| `judge_outputs_frozen_v1_11.json` | `judge_v1_11.py --freeze` | `osf/methodology/v1_11/outputs/` |
| `plan_v1_11.json` | `judge_v1_11.py` (binding projection, §7) | `osf/methodology/v1_11/data/` (looked up there when it is not beside the others) |
| tag `v1.11-prereg-r1` and `osf/methodology/v1_11/anchor/git_anchor_v1_11.json` | lock | the fill refuses unless the anchor names the tag's commit and a non-empty `osf_deposit` |
| `osf/methodology/v1_11/anchor/DEVIATIONS.md` | locked; dated entries added after the lock | entries after Entry 0 are counted in Method §2.10 |

## Scoring (coordinator, in the `v1.11` worktree; from 22 November 2026)

Not part of this branch. The order is the pre-registration's (§8): judge run (calibration, plan, phases A, A2, B, B2; `--no-other-collection "<who, when>"`; the pause at US$80 needs `--approve-past-pause`), `judge_v1_11.py --freeze`, then

```
cd /Users/pablou/aias/_worktrees/v1.11
python3 scripts/score_v1_11.py --stage J
python3 scripts/score_v1_11.py --stage C
```

Stage C computes H5 only when v1.10's own Stage C verdict file is on branch `v1.10`; otherwise H5 is PENDING (the paper has the sentence for it) and Stage C is re-run when v1.10 reports, under the same pre-registration.

## 0. Bring the pipeline next to the scored data

`v1.11-paper` only adds files (`papers/v1_11/`, three scripts in `scripts/`); it changes nothing under `osf/methodology/v1_11/` and no file in the lock manifest.

```
git -C /Users/pablou/aias diff --stat v1.11...v1.11-paper
cd /Users/pablou/aias/_worktrees/v1.11 && git merge --no-ff v1.11-paper
```

Run steps 1 to 5 from that worktree. `python3` is the system Python 3.14 (numpy, matplotlib, reportlab, pypdf); pandoc with xelatex, Carlito, `pdftoppm`.

## 1. Tests (26)

```
PYTHONDONTWRITEBYTECODE=1 python3 papers/v1_11/tests/test_fill_paper_v1_11.py
```

Expect `Ran 26 tests … OK`. They generate the synthetic scenarios into a temporary folder and check: every switch value matches exactly one case and the cases are exactly the pre-registered outcomes; the AI-use statement verbatim, the COI paragraph (v0.22 tier-2/3 disclosure, the Denon/Harman correction with "a Samsung subsidiary since March 2017" and 23 September 2025) and Samsung only in that paragraph; the citations (v1.9 by its thirdsystem.ai and OSF copies, never SSRN 7685126; the methodology chain v1.2–v1.9, AIAS 1.0/2.0, the MSI report; every reference cited); the thresholds in the text are the scorer's constants; the base fixtures are the scorer's dry-run outputs (SHA-256) and every scenario keeps the scorer's schema, is marked synthetic and is reproduced by the scorer's verdict functions; the scenarios cover CONFIRMED, MARGINAL, FALSIFIED and UNDETERMINED for every hypothesis (and PENDING, INACTIVE for H5) and every Discussion opening; every scenario fills; every printed value re-resolves from its JSON path (over 1,000 values and table cells); every number in the Abstract and Results is either fixed text or a recorded value; every pre-registered test appears exactly once (the verdict table) with its verdict; the verdict words in the text match the file; every case and flag renders; the real-mode checks pass on a relabelled fixture; and the refusals (synthetic in real mode, real-looking in synthetic mode, an edited verdict word or statistic, a Stage J or plan file that is not the one recorded, synthetic output inside the repository, charts or PDF of synthetic data without the watermark, scenarios under `osf/`).

## 2. Figures

```
PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_charts_v111.py
```

Writes `reports/figs/v111/chart_01_judge_confusion.pdf` … `chart_05_baseline.pdf` (+ `_preview.png`), one per finding: H1 (J1 × J2 valence counts), H2/H3/H5/H8 (per-wave $\rho_w$ with intervals against the bands), H4/H6 (between-wave $\rho_w$), H9 (judge difference by answer provider), and the baseline (§6.1). Titles describe the plot, never the finding.

## 3. Fill the paper

```
PYTHONDONTWRITEBYTECODE=1 python3 papers/v1_11/fill_paper_v1_11.py
```

Writes `papers/v1_11/v1_11_paper_draft.md` and `…_draft_provenance.json` (JSON path, raw value and format of every number) and prints the selected cases. It refuses when any of the four files is synthetic (`dry_run` true or a `synthetic_fixture` key), `prereg_tag` is not `v1.11-prereg-r1`, the verdicts' `stage_j_sha256` is not the Stage J file's, the frozen outputs' `plan_sha256` is not the plan file's, the unit-table hashes differ, the four files name different judges, the tag is missing or the anchor does not name its commit with an OSF deposit, or a verdict word is not what the scorer's functions give for its statistics.

## 4. Build the PDF

```
PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_paper_v1_11.py
```

Writes `papers/v1_11/v1_11_paper.pdf` (pandoc, xelatex, Carlito; tables via `tables_as_tabular.lua`; the Carlito glyph-gap substitutions of the v1.12 builder). A missing glyph is printed as a warning; add it to `UNICODE_SUBS`.

## 5. Pre-flight (CLAUDE.md: before commit, tag or deposit)

```
rm -rf /tmp/v111_pf && mkdir /tmp/v111_pf && pdftoppm -r 100 -png papers/v1_11/v1_11_paper.pdf /tmp/v111_pf/paper
```

Look at every page. Then check by hand, against the files:

- the selected Results and Discussion sentences against `VERDICTS` and `verdicts_before_noise_guard` in `v1_11_verdicts.json` (the noise guard sentence, and the H1 MARGINAL flag sentence when H1 is MARGINAL);
- H5: ACTIVE with rank tables matching v1.10 (§3.1 sentence), or PENDING — then the paper is not final until Stage C is re-run;
- §3.1: reductions applied (plan), a judge replaced by the alternate (frozen `replacements`), the served-model sentence;
- recorded spend against the vendors' invoices (§7 says the difference is reported; the invoices are not in the scorer's outputs, so add a sentence by hand if they differ);
- Samsung only in the COI paragraph; the deviation count in §2.10 against `DEVIATIONS.md`.

Then commit the figures, the draft and its provenance and the PDF.

## Synthetic end-to-end test (no real data; every page and chart stamped "SYNTHETIC TEST — NOT RESULTS")

```
cd /Users/pablou/aias/_worktrees/v1.11-paper && zsh papers/v1_11/tests/run_synthetic_e2e_v1_11.sh /tmp/v111_pipeline_test/e2e
```

`tests/make_scenarios_v1_11.py` starts from the scorer's own Stage J and Stage C outputs of its end-to-end dry run on synthetic replicas (v1.11 worktree, `osf/methodology/v1_11/dryrun/outputs/`, 10 November 2026: `build_dryrun_v1_11.py` replicas, a fake judge and a fake batch service; no real answer, judge call, P, C\* or Ranking value), committed as `tests/fixtures/SYNTHETIC_base_*` with their SHA-256 in the script. The other scenarios change statistics and recompute every verdict word with the scorer's functions (`judge_agreement_verdict`, `separability_verdict`, `stability_verdict`, `band_verdict`, `self_pref_verdict`, `verdict_row`, `apply_noise_guard`) and the sensitivity verdict changes as `run_stage_c` does:

| Scenario | H1 | H2 | H3 | H4 | H5 | H6 | H7 | H8 | H9 | Discussion |
|---|---|---|---|---|---|---|---|---|---|---|
| scored | MARGINAL | CONFIRMED | CONFIRMED | CONFIRMED | CONFIRMED | CONFIRMED | CONFIRMED | CONFIRMED | CONFIRMED | SEPARABLE_FLAGGED |
| confirmed | CONFIRMED | CONFIRMED | CONFIRMED | CONFIRMED | CONFIRMED | CONFIRMED | CONFIRMED | CONFIRMED | CONFIRMED | SEPARABLE |
| h1_falsified | FALSIFIED | UNDET. (guard) | UNDET. (guard) | CONFIRMED | UNDET. (guard) | CONFIRMED | UNDET. (guard) | UNDET. (guard) | FALSIFIED | INSTRUMENT_FAILED |
| unstable | CONFIRMED | UNDET. (guard) | UNDET. (guard) | FALSIFIED (ρ) | UNDET. (guard) | CONFIRMED | UNDET. (guard) | UNDET. (guard) | CONFIRMED | UNSTABLE |
| marginal | MARGINAL | MARGINAL | FALSIFIED | MARGINAL | MARGINAL | FALSIFIED (p) | MARGINAL | FALSIFIED | MARGINAL | NOT_SEPARABLE |
| mixed | CONFIRMED | MARGINAL | MARGINAL | MARGINAL | CONFIRMED | MARGINAL | FALSIFIED | MARGINAL | CONFIRMED | MIXED |
| presence | MARGINAL | FALSIFIED | CONFIRMED | CONFIRMED | FALSIFIED | FALSIFIED (ρ) | CONFIRMED | CONFIRMED | CONFIRMED | NOT_SEPARABLE |
| undetermined | UNDETERMINED | UNDET. (waves) | UNDET. (waves) | UNDETERMINED | PENDING | UNDETERMINED | UNDET. (floor) | UNDET. (waves) | UNDETERMINED | INSTRUMENT_UNDETERMINED |
| inactive | MARGINAL | CONFIRMED | CONFIRMED | CONFIRMED | INACTIVE | CONFIRMED | CONFIRMED | CONFIRMED | CONFIRMED | SEPARABLE_FLAGGED |

In `marginal`, sensitivity SD changes H2 (MARGINAL → CONFIRMED); in `h1_falsified`, H9 FALSIFIED adds the "S without J1-provider answers" sensitivity. Outputs go only under the given `/tmp` directory; the script refuses a path in the repository and `make_scenarios_v1_11.py` refuses any path under `osf/`. The synthetic build has 19 pages in every scenario.

## What selects the wording

| Switch | Values | Source |
|---|---|---|
| `CASE_H1`, `CASE_H9` | CONFIRMED, MARGINAL, FALSIFIED, UNDETERMINED | `VERDICTS` |
| `CASE_H2`, `CASE_H3`, `CASE_H8` | CONFIRMED, MARGINAL, FALSIFIED, UNDETERMINED_GUARD (noise guard), UNDETERMINED_WAVES (fewer than two determined waves) | `VERDICTS`, `verdicts_before_noise_guard` |
| `CASE_H5` | as H2, plus PENDING, INACTIVE | `VERDICTS.H5`, `ranking.status` |
| `CASE_H4`, `CASE_H6` | CONFIRMED, MARGINAL, FALSIFIED_RHO (ρ < 0.30), FALSIFIED_P (p ≥ .05), UNDETERMINED | `VERDICTS`, `H4_/H6_….rho` |
| `CASE_H7` | CONFIRMED, MARGINAL, FALSIFIED, UNDETERMINED_GUARD, UNDETERMINED_FLOOR | `VERDICTS` |
| `CASE_OVERALL` (Abstract, Discussion) | INSTRUMENT_FAILED (H1 F), UNSTABLE (H4 F), INSTRUMENT_UNDETERMINED (H1 U), NOT_SEPARABLE (H2, H3 or active H5 F), SEPARABLE (H1, H2, H3, active H5, H4 C), SEPARABLE_FLAGGED (the same with H1 M), MIXED | `VERDICTS` (a reading of the scorer's words, never a new verdict) |

## Files

`papers/v1_11/`: `v1_11_paper_template.md`; `fill_paper_v1_11.py` (template engine forked unchanged from v1.12) with `v111_values.py`; `tables_as_tabular.lua` (copied); `tests/` (`test_fill_paper_v1_11.py`, `make_scenarios_v1_11.py`, `run_synthetic_e2e_v1_11.sh`, `fixtures/SYNTHETIC_base_*`). `scripts/`: `build_charts_v111.py`, `build_paper_v1_11.py`, `watermark_v111.py`.

## Rules kept

- No analysis outside the pre-registration; the paper reads only the scorer's and runner's outputs, the locked anchor and the deviations record.
- Samsung appears only in the COI paragraph of the Declarations: the pre-registration's §14 text, with the Denon/Harman sentence of CLAUDE.md (Harman a Samsung subsidiary since March 2017; Sound United, Denon included, acquired 23 September 2025).
- The "Use of AI tools" statement is CLAUDE.md's, verbatim.
- ™ marks the first mention of AIAS and of Third System.
- v1.9 is cited by its thirdsystem.ai and OSF copies, never as SSRN 7685126.

## Open (for the coordinator)

- Pre-registered descriptives not in the scorer's outputs: §6.5 lists served-model **and finish-reason counts and reasoning tokens per judge**. Stage J/C do not write the last two; they are in `data/judge_raw_v1_11.jsonl`. The paper reports the served-model count (from the frozen file) only. Adding the others needs a small reader of the raw file (descriptive; no verdict depends on it).
- §6.1 asks for the baseline "per panel" as well as per category; the scorer writes per category (block × wave) and the mean unit score per panel, which is what the paper prints. The per-category shares of JUDGE_FAIL, UNJUDGED and bare windows are in `descriptives.baseline` but not printed (table width); add a column if wanted.
- §7: "the vendors' invoices are reconciled with the recorded spend after the run and any difference is reported". The invoices are not a machine output; add the sentence by hand at step 5.
- If Stage C runs before v1.10's Stage C verdicts exist, H5 is PENDING and the paper is provisional on H5 until Stage C is re-run.
