# v1.12 Coverage Paper A: the commands after scoring

Built on branch `v1.12-paper` (from `v1.12` at `f19fb73`, the anchor commit after tag `v1.12-prereg-r1`) on 10–11 November 2026, before any v1.12 answer existed. Mirrors the t4 pipeline (`papers/v0_42/` on branch `t4-paper`). Paper A is a paper only: no Third System report, so no report builder. Every builder reads only the scorer's outputs; no number is typed by hand. Results and Discussion were written in advance as alternative sentences, one for each pre-registered outcome, and the fill script picks one from the verdicts. Verdict words are printed exactly as `score_v1_12.py` writes them.

## Inputs

| File | Written by | Required |
|---|---|---|
| `osf/methodology/v1_12/v112_verdicts.json` | `score_v1_12.py --run` (after `--code`, `--parity-p1`, and v1.14's Stage 1 or `--h5-unavailable`) | yes |
| `osf/methodology/v1_12/v112_unit_table.csv` | the same run | yes |
| `osf/methodology/v1_12/prereg/calibration_N1_v1_12.json` | locked at `v1.12-prereg-r1` (N1 numbers in §2.4) | yes |
| tag `v1.12-prereg-r1` in the repository, and `osf/methodology/v1_12/anchor/osf_anchor_v1_12.json` naming its commit | lock | yes: the fill refuses without both |
| `osf/methodology/v1_12/anchor/DEVIATIONS.md` | locked; the coordinator adds dated entries | yes (its dated entries are counted in §2.9) |

## 0. Bring the pipeline next to the scored data (coordinator)

`v1.12-paper` only adds files (`papers/v1_12/`, three scripts in `scripts/`). It changes nothing under `osf/methodology/v1_12/` and no file in the lock manifest:

```
git -C /Users/pablou/aias diff --stat v1.12 v1.12-paper
cd /Users/pablou/aias/_worktrees/v1.12 && git merge --no-ff v1.12-paper
```

Run steps 1 to 5 from that worktree after scoring. `python3` is the system Python 3.14 (numpy, scipy, matplotlib, reportlab, pypdf); pandoc 3.9 with xelatex, Carlito and `pdftoppm`.

## 1. Tests (16)

```
PYTHONDONTWRITEBYTECODE=1 python3 papers/v1_12/tests/test_fill_paper_v1_12.py
```

Expect `Ran 16 tests … OK`. They check that every switch value matches exactly one case; that all eight synthetic scenarios fill and that every number in each filled paper is either fixed pre-registration text or a recorded value; that every JSON, derived and table value re-resolves from its path; that every leg renders under CONFIRMED, MARGINAL, FALSIFIED and UNDETERMINED (floor and reason); the AI-use statement, the Denon/Harman correction and the Samsung rule (Samsung only in the COI paragraph) in every render; that the scenarios' gate equals the scorer's `gate()`; the real-mode checks (tag, anchor, MC_BrandFree, deviations record) on a relabelled fixture in memory; and the refusals.

## 2. Figures

```
PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_charts_v112.py
```

Writes `reports/figs/v112/chart_01_situation_overlap.pdf` … `chart_08_baseline.pdf` (+ `_preview.png`), one per finding: MC_Situation, the legs against their bands (Paper A verdict), H1, H2, H3 (with raw Cov, MC_Positive), H4, H8, and the baseline. Titles describe the plot, never the finding.

## 3. Fill the paper

```
PYTHONDONTWRITEBYTECODE=1 python3 papers/v1_12/fill_paper_v1_12.py
```

Writes `papers/v1_12/v1_12_ssrn_paper_draft.md` and `…_draft_provenance.json` (JSON path, raw value and format of every number). It prints the selected cases (`CASE_GATE`, `CASE_MSIT`, `CASE_H1`–`CASE_H4`, `CASE_H5`, `CASE_H6`, `CASE_H7`, `CASE_H8`, `CASE_PARITY`). It refuses when the verdicts are synthetic (P1 not passed, or a `synthetic_fixture` key), P1 or P3 failed, P2 failed outside the declared fallback, `prereg_tag` is not `v1.12-prereg-r1`, the tag is missing, or the anchor does not name the tag's commit.

## 4. Build the PDF

```
PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_paper_v1_12.py
```

Writes `papers/v1_12/v1_12_ssrn_paper.pdf` (pandoc, xelatex, Carlito; tables via `tables_as_tabular.lua`). "Cov*" in running text is escaped so pandoc never reads the asterisk as emphasis. A missing Carlito glyph is printed as a warning; add it to `UNICODE_SUBS`.

## 5. SSRN packet

```
PYTHONDONTWRITEBYTECODE=1 python3 papers/v1_12/ssrn_packet_hook_v1_12.py
```

Runs `scripts/generate_ssrn_packet.py` unchanged; writes `papers/v1_12/ssrn_submission_packet_v1_12.md`; must print `all checks passed` (title and abstract equal the paper's, no LaTeX/template residue or underscores in the abstract, standing keywords, JEL codes, COI paragraph).

## 6. Pre-flight (CLAUDE.md: before commit, tag or deposit)

```
rm -rf /tmp/v112_pf && mkdir /tmp/v112_pf && pdftoppm -r 80 -png papers/v1_12/v1_12_ssrn_paper.pdf /tmp/v112_pf/paper
```

Look at every page; read the selected Results and Discussion sentences against `v112_verdicts.json`; check the abstract length in the packet; confirm Samsung appears only in the COI paragraph. Then commit the figures, the draft and its provenance, the PDF and the packet.

## Synthetic end-to-end test (no real data; every page and chart stamped "SYNTHETIC TEST — NOT RESULTS")

```
cd /Users/pablou/aias/_worktrees/v1.12-paper && zsh papers/v1_12/tests/run_synthetic_e2e_v1_12.sh /tmp/v112_pipeline_test/e2e
```

`tests/make_scenarios_v1_12.py` runs the locked scorer's `score_coverage()` (imported read-only) on the synthetic inputs of its own unit tests (`scripts/tests/test_pipeline_v1_12.inputs`, invented brand names) with 10,000 draws and writes its output with the scorer's `write_outputs()` (scenario `scored`). The other scenarios copy that output and give the primary legs other statistics; each verdict word is recomputed by the scorer's verdict functions and the Paper A verdict by its `gate()`:

| Scenario | Paper A | H5 |
|---|---|---|
| scored | the scorer's own result on the synthetic data (FAIL: H3 FALSIFIED) | INACTIVE |
| pass | PASS | active, gating, CONFIRMED |
| fail | FAIL (H1 FALSIFIED) | reported, not gating |
| marginal | MARGINAL (H1) | INACTIVE |
| downgraded | MARGINAL (PASS downgraded: H7 FALSIFIED) | INACTIVE |
| undetermined | UNDETERMINED (H4 below the n floor) | active, Stage 1 unavailable |
| instrument | INSTRUMENT FAIL (MC_Situation) | INACTIVE |
| fallback | MARGINAL (two-model, H1/H2 cross-panel) | active, gating |

The committed fixtures (`tests/fixtures/SYNTHETIC_*`) are the same eight files. Outputs go only under the given `/tmp` directory; the script refuses a path in the repository, and `make_scenarios_v1_12.py` refuses any path under `osf/`. In derived scenarios the sensitivity "verdict changes" still compare with the `scored` verdicts (synthetic only; the real file is self-consistent).

## What selects the wording

| Switch | Values | Source in the verdicts |
|---|---|---|
| `CASE_GATE` | PASS, FAIL, MARGINAL, MARGINAL_H7 (downgrade), MARGINAL_TWO_MODEL (§7.3 cap), UNDETERMINED, INSTRUMENT_FAIL | `paper_A_verdict.verdict` / `.notes` |
| `CASE_MSIT` | PASSED, FAILED | `MC.MC_Situation.passed` |
| `CASE_H1`…`H4`, `H7`, `H8` | CONFIRMED, MARGINAL, FALSIFIED, UNDETERMINED_FLOOR, UNDETERMINED_REASON, UNDETERMINED_DEGENERATE | `legs.<H>.verdict` / `.below_n_floor` / `.reason` |
| `CASE_H5` | INACTIVE, GATING, REPORTED (N35), UNAVAILABLE (N30) | `legs.H5_Sep_Ranking`, `H5_ranking_source.h5_gates` |
| `CASE_H6` | INACTIVE, ACTIVE | `legs.H6_Sep_Sentiment.verdict` |
| `CASE_PARITY` | PASSED, SYNTHETIC | real vs synthetic mode |

## Files

`papers/v1_12/`: `v1_12_ssrn_paper_template.md`; `fill_paper_v1_12.py` (engine forked unchanged from v0.42) with `v112_values.py`; `tables_as_tabular.lua` (copied); `ssrn_packet_hook_v1_12.py`; `tests/` (`test_fill_paper_v1_12.py`, `make_scenarios_v1_12.py`, `run_synthetic_e2e_v1_12.sh`, `fixtures/SYNTHETIC_*`). `scripts/`: `build_charts_v112.py`, `build_paper_v1_12.py`, `watermark_v112.py`.

## Rules kept

- No analysis outside the pre-registration; the paper reads only the scorer's outputs and the locked N1 record.
- Samsung appears only in the COI paragraph of the Declarations, which carries the pre-registration's §8 text with the Denon/Harman correction of 10 November 2026 and the v0.22 tier-2/3 disclosure.
- The "Use of AI tools" statement is CLAUDE.md's, verbatim.
- ™ marks the first mention of AIAS and of Third System.

## Open before data arrives (for the coordinator)

1. **Lock time.** The pre-registration text says it locks no earlier than 11 November, about 3 pm CT; `anchor/DEVIATIONS.md` records that the pre-registrant waived the 24-hour review (10 November, 20:26 CT) and the lock at 02:45 UTC on 11 November. §2.9 only counts the dated entries; decide whether the paper states the waiver in words.
2. **Romaniuk & Sharp.** The locked `cep_sets_v1_12.md` cites Romaniuk & Sharp (2016), *How Brands Grow: Part 2*; other programme papers cite the 2022 revised edition. The template follows the locked file (2016).
3. **Descriptives not yet printed.** §5 of the pre-registration also lists per-W coverage, words per answer, C0 agreement and tokens per model; the verdict file has them (`descriptives.per_W_coverage_primary_panel`, `per_category_model`, `tokens_and_spend`), but the paper prints only the per-category table, run reliability, brands per answer and total spend. Add an appendix table if wanted.
4. **H5 and H6 in the real run.** The scorer makes H5 active when tag `v1.14-prereg-r2` exists locally (it does), so the real run needs `--h5-stage1` (v1.14's Stage 1 output) or `--h5-unavailable REASON`. H6 is INACTIVE unless `--h6` is passed; no t4 Sentiment score was tagged before the lock, so `--h6` must not be passed.
5. **Fable drop.** If Claude Fable 5.2 leaves the panel, C3 becomes primary; Results print the primary panel's name, but Method §2.2 is fixed text that calls N3 primary.
