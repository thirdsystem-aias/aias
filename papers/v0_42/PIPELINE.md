# v0.42 (t₄) paper and report: the commands after scoring

Built on branch `t4-paper` (from `61515b4`, the tip of `v0.42` before the lock) on 10 November 2026, before any t₄ answer existed. Every builder reads only the scorer's outputs; no number is typed by hand. Results and Discussion were written in advance as alternative sentences, one for each pre-registered outcome, and the fill script picks one from the verdicts.

## Inputs

| File | Written by | Required |
|---|---|---|
| `osf/v42/v42_verdicts.json` | `score_v0_42.py --run` (LOCK_STEPS §11 step 2) | yes |
| `osf/v42/v42_brand_table.csv` | the same run | yes |
| tag `v0.42-prereg-r1` in the repository, and `osf/v42/anchor/osf_anchor_v0_42.json` naming its commit | lock (LOCK_STEPS steps 3–4) | yes: the fill refuses without both |
| `osf/v42/DEVIATIONS.md` | the coordinator, if a deviation was logged | if it is absent, the fill needs `--no-deviations` |
| `osf/v42/data/t4_budget_state.json` | `acquire_v0_42.py` (only when a pause was approved) | read if present; absent means no approval was recorded |
| `osf/v41/v41_verdicts.json` | v0.41, tag `v0.41-scoring-locked` | yes (background numbers in §1) |

## 0. Bring the pipeline next to the scored data (coordinator)

`t4-paper` only adds files. It changes nothing under `osf/v42/` and no file in the lock manifest:

```
git -C /Users/pablou/aias diff --stat 61515b4 t4-paper
cd /Users/pablou/aias/_worktrees/v0.42 && git fetch origin --tags && git merge --no-ff t4-paper
```

Run steps 1 to 7 from that worktree, after `v0.42-scoring-locked`. On the Mac, `python3` is the system Python 3.14, which has numpy, matplotlib, reportlab and pypdf; it also needs pandoc 3.9 with xelatex, Carlito, Akkurat Pro and `pdftoppm`. The steps take about 2 minutes in all.

## 1. Tests (12)

```
cd /Users/pablou/aias/_worktrees/v0.42 && PYTHONDONTWRITEBYTECODE=1 python3 papers/v0_42/tests/test_fill_paper_v0_42.py
```

Expect `Ran 12 tests … OK`. The tests check that every switch in the template covers every outcome. They fill 15 verdict variants and trace every printed number to a JSON path or to a declared pre-registration constant. They also check the refusals and that the report content builds for every variant.

## 2. Figures (paper and report registers)

```
PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_charts_v42.py
```

Writes `reports/figs/v42/chart_01_presence_t3_t4.pdf`, `chart_02_phi_t3_t4.pdf`, `chart_03_search_s0_s1.pdf`, `chart_04_run_reliability.pdf` and `chart_05_floor.pdf`, each with a `_preview.png`. It also writes `reports/figs/v42/report/report_fig_01.pdf` to `report_fig_05.pdf`, one per pre-registered finding: H_Gen_Presence, H_Gen_Phi, H_Search_Presence, descriptive 1 and descriptive 3.

## 3. Fill the paper

```
PYTHONDONTWRITEBYTECODE=1 python3 papers/v0_42/fill_paper_v0_42.py            # add --no-deviations only if osf/v42/DEVIATIONS.md does not exist
```

Then, on the real data, always run `PYTHONDONTWRITEBYTECODE=1 python3 papers/v0_42/post_fill_real_v0_42.py`: the Discussion and the sentences written for the observed results live only in that script, so a fill without it loses them (it refuses unless `v42_verdicts.json` has the SHA-256 it was written for).

The fill writes `papers/v0_42/v0_42_ssrn_paper_draft.md` and `papers/v0_42/v0_42_ssrn_paper_draft_provenance.json`, which records the JSON path, raw value and format of every number. The script prints the cases it selected (`CASE_GEN`, `CASE_PHI`, `CASE_SEARCH`, `GEN_DELTA_DIR`, `CASE_PARITY`).

It refuses in five cases:
- the verdicts come from the synthetic mode;
- a parity gate failed;
- `prereg_tag` is not `v0.42-prereg-r1`;
- the tag is missing from the repository;
- the anchor does not name the tag's commit.

## 4. Build the paper PDF

```
PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_paper_v0_42.py
```

Writes `papers/v0_42/v0_42_ssrn_paper.pdf` (pandoc, xelatex and Carlito). Tables are set as unbreakable tabulars by `papers/v0_42/tables_as_tabular.lua`. A glyph that Carlito lacks is printed as a warning; add it to `UNICODE_SUBS`.

## 5. SSRN packet

```
PYTHONDONTWRITEBYTECODE=1 python3 papers/v0_42/ssrn_packet_hook_v0_42.py
```

Runs `scripts/generate_ssrn_packet.py` unchanged and writes `papers/v0_42/ssrn_submission_packet_v0_42.md`. It must print `all checks passed` (exit 0). The checks:
- title and abstract equal the paper's;
- no LaTeX or template residue in the abstract;
- the standing keywords are present;
- JEL codes are found (label `**JEL codes:**`);
- the Declaration of Interest is the paper's COI paragraph.

## 6. Report

```
PYTHONDONTWRITEBYTECODE=1 python3 reports/build_report_v42.py
```

Writes `osf/v42/reports/v42_t4_generation_report.pdf`. It is in the managerial register, with P1 to P5, one chart per finding and no hypothesis labels. Its content module is `reports/v42_t4_generation_content.py`, and its wording follows the same verdict cases as the paper.

## 7. Pre-flight (CLAUDE.md: required before commit, tag or deposit)

```
rm -rf /tmp/v42_pf && mkdir /tmp/v42_pf && pdftoppm -r 80 -png papers/v0_42/v0_42_ssrn_paper.pdf /tmp/v42_pf/paper && pdftoppm -r 80 -png osf/v42/reports/v42_t4_generation_report.pdf /tmp/v42_pf/report
```

Then:
- Look at every page: overflow, orphan lines, chart–caption gaps, tables.
- Read the selected Results and Discussion sentences against `v42_verdicts.json`.
- Check the abstract length in the packet against SSRN's field.
- Confirm that Samsung appears only under Declarations (the tests check this on synthetic variants).

Then commit the figures, the draft and its provenance, the PDFs and the packet. OSF, website and SSRN follow the programme's steps 6 to 8 (gates).

## Synthetic end-to-end test (no real data; every page stamped "SYNTHETIC TEST — NOT RESULTS")

```
cd /Users/pablou/aias/_worktrees/t4-paper && zsh papers/v0_42/tests/run_synthetic_e2e_v0_42.sh /tmp/t4_pipeline_test/e2e noisy
```

The script makes synthetic t₄ raw and coded files in the real formats (`papers/v0_42/tests/make_scenarios_v0_42.py`, which uses `osf/v42/scripts/tests/make_synthetic_t4.build`). It then runs the real scorer in `--synthetic` mode with full draws, followed by steps 2 to 6 with `--watermark`, page PNGs and the tests. Everything is written under the given `/tmp` directory, which must be outside the repository. Use the scenario `copy` to get the all-CONFIRMED path.

## What selects the wording

| Switch | Values | Source in the verdicts |
|---|---|---|
| `CASE_GEN` | CONFIRMED, MARGINAL, FALSIFIED, UNDETERMINED_EXCLUDED (drop rule, §5.4), UNDETERMINED_DEGENERATE (scorer note N14) | `verdicts.H_Gen_Presence.verdict` / `.reason` |
| `CASE_PHI` | the same five, plus UNDETERMINED_FLOOR (n < 40) | `verdicts.H_Gen_Phi` |
| `CASE_SEARCH` | ROBUST, SENSITIVE, DOMINATED (pre-declared labels), UNDETERMINED, NOT_COMPUTED | `verdicts.H_Search_Presence.label` / `.status` |
| `GEN_DELTA_DIR` | ABOVE, BELOW, SPANS (the level-shift interval against 0) | `verdicts.H_Gen_Presence.ci95_delta` |
| `CASE_PARITY` | PASSED, SYNTHETIC | `manipulation_checks.MC_Parity` |

The pre-registration's verdict words are CONFIRMED, MARGINAL, FALSIFIED and UNDETERMINED; r2 has no "PARTIAL". The report renders MARGINAL as "PARTLY SUPPORTED".

## Files

`papers/v0_42/`:
- `v0_42_ssrn_paper_template.md`: the paper. Introduction and Method are fixed text from the pre-registration (r2 with C1–C28); Results and Discussion are variants.
- `fill_paper_v0_42.py`, with `v42_values.py` (reading, formats, provenance, cases).
- `tables_as_tabular.lua`.
- `ssrn_packet_hook_v0_42.py`.
- `tests/`: `test_fill_paper_v0_42.py`, `make_scenarios_v0_42.py`, `run_synthetic_e2e_v0_42.sh`, and `fixtures/SYNTHETIC_noisy_*`, the scorer's synthetic output.

`scripts/`:
- `build_charts_v42.py`
- `build_paper_v0_42.py`
- `watermark_v42.py`

`reports/`:
- `build_report_v42.py` (forked from v0.41)
- `v42_t4_generation_content.py`

## Rules kept

- No analysis outside the v0.42 pre-registration. No Ranking-component statistic (rank position, MNP, MODE) is computed on t₄ answers; LOCK_STEPS §11 gates those on v1.14's Stage 1.
- Samsung appears only in the paper's Declarations, in the COI paragraph, which is the pre-registration's §8 text including the Denon/Harman correction of 10 November 2026.
- The "Use of AI tools" statement is CLAUDE.md's, verbatim.
- ™ marks the first mention of AIAS and of Third System.
- Background numbers in §1 are read from `osf/v41/v41_verdicts.json` (tag `v0.41-scoring-locked`).
