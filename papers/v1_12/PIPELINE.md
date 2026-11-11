# v1.12 Coverage Paper A: the commands after scoring

Built on branch `v1.12-paper` (from `v1.12` at `f19fb73`, the anchor commit after tag `v1.12-prereg-r1`) on 10–11 November 2026, before any v1.12 answer existed. Mirrors the t4 pipeline (`papers/v0_42/` on branch `t4-paper`). Paper A is a paper only: no Third System report, so no report builder. Every builder reads only the scorer's outputs; no number is typed by hand. Results and Discussion were written in advance as alternative sentences, one for each pre-registered outcome, and the fill script picks one from the verdicts. Verdict words are printed exactly as `score_v1_12.py` writes them.

## Inputs

| File | Written by | Required |
|---|---|---|
| `osf/methodology/v1_12/v112_verdicts.json` | `score_v1_12.py --run --h5-stage1 <v1.14 Stage 1 output>` (or `--h5-unavailable REASON`), never `--h6`; after `--code` and `--parity-p1` (Scoring, below) | yes |
| `osf/methodology/v1_12/v112_unit_table.csv` | the same run | yes |
| `osf/methodology/v1_12/prereg/calibration_N1_v1_12.json` | locked at `v1.12-prereg-r1` (N1 numbers in §2.4) | yes |
| tag `v1.12-prereg-r1` in the repository, and `osf/methodology/v1_12/anchor/osf_anchor_v1_12.json` naming its commit | lock | yes: the fill refuses without both |
| `osf/methodology/v1_12/anchor/DEVIATIONS.md` | locked; the coordinator adds dated entries | yes (its dated entries are counted in §2.9) |

## Scoring (coordinator, in the `v1.12` worktree, after the collection; before step 0)

Decided before data (runner's log, Nov 10, 2026, 9:59 pm): the real run passes H5's score with `--h5-stage1` (or `--h5-unavailable`) and never `--h6`. The anchor recorded H5 ACTIVE (tag `v1.14-prereg-r2` pushed before the lock) and H6 INACTIVE (no Sentiment score on the t4 answers was tagged before the lock; pre-registration §12 (h), N36). The coder's re-check against tag `v0.42-prereg-r1` and P1 come first (`LOCK_STEPS.md` §7).

```
cd /Users/pablou/aias/_worktrees/v1.12
PYTHONDONTWRITEBYTECODE=1 python3 osf/methodology/v1_12/scripts/score_v1_12.py --code
PYTHONDONTWRITEBYTECODE=1 python3 osf/methodology/v1_12/scripts/score_v1_12.py --parity-p1
PYTHONDONTWRITEBYTECODE=1 python3 osf/methodology/v1_12/scripts/score_v1_12.py --run \
    --h5-stage1 /Users/pablou/aias/_worktrees/v1.14/osf/methodology/v1_14/outputs/stage1/stage1_v1_14.json
```

- `--h5-stage1`: v1.14's Stage 1 output (`stage1_v1_14.json`, with `rank_table_t4_v1_14.csv` beside it), where `score_v1_14.py --stage 1` wrote it (the path above is its place in the `v1.14` worktree; check it first). The scorer records its SHA-256; H5 gates only if its `STAGE1_VERDICT` is `SEPARABLE (Stage 2 pending)` (N35). Without the file the run refuses (blindness guard, N34).
- `--h5-unavailable "REASON"` replaces `--h5-stage1` only if v1.14's Stage 1 halted and its output cannot exist: H5 is then UNDETERMINED and neither gates nor downgrades (N30). Log the reason.
- Never `--h6` (and `--h6-cross-panel` is refused by the scorer). Step 3 refuses a verdict file with H6 active or H5 inactive.
- The t4 inputs default to `osf/v42/…` in this worktree. If v0.42's outputs are elsewhere, pass `--t4-raw`, `--t4-coded`, `--t4-brand-table` and `--t4-verdicts`: if any of the four is missing, the scorer falls back to the published AIAS 2.0 t3 values for H1 and H2 (cross-panel, N19) and reports `MC_Window`'s t4 overlap as not checked.

## 0. Bring the pipeline next to the scored data (coordinator)

`v1.12-paper` only adds files (`papers/v1_12/`, three scripts in `scripts/`). It changes nothing under `osf/methodology/v1_12/` and no file in the lock manifest. Three dots compare with the fork point: `v1.12` has commits after `f19fb73` (from `a57f590`, `anchor/t4_complete_v1_12.json`), which a two-dot diff shows as deletions on `v1.12-paper`; the merge keeps them.

```
git -C /Users/pablou/aias diff --stat v1.12...v1.12-paper
cd /Users/pablou/aias/_worktrees/v1.12 && git merge --no-ff v1.12-paper
```

Run steps 1 to 5 from that worktree after scoring. `python3` is the system Python 3.14 (numpy, scipy, matplotlib, reportlab, pypdf); pandoc 3.9 with xelatex, Carlito and `pdftoppm`.

## 1. Tests (20)

```
PYTHONDONTWRITEBYTECODE=1 python3 papers/v1_12/tests/test_fill_paper_v1_12.py
```

Expect `Ran 20 tests … OK`. They check that every switch value matches exactly one case; that all eight synthetic scenarios fill and that every number in each filled paper is either fixed pre-registration text or a recorded value; that every JSON, derived and table value re-resolves from its path; that every leg renders under CONFIRMED, MARGINAL, FALSIFIED and UNDETERMINED (floor and reason); the AI-use statement, the Denon/Harman correction and the Samsung rule (Samsung only in the COI paragraph) in every render; the citations (no SSRN number or ssrn.com link for a paper SSRN declined or has not posted; v1.9 by title with its thirdsystem.ai and OSF copies; Romaniuk & Sharp 2016 as the locked CEP file); that Method §2.2 names the primary panel by the drop rule (N3, or C3 when Claude Fable 5.2 left) and refuses a record against it; that the scenarios' gate equals the scorer's `gate()`; the real-mode checks (tag, its date, anchor, MC_BrandFree, the deviations record and its lock entry, H5/H6 as the anchor recorded them) on a relabelled fixture in memory; and the refusals.

## 2. Figures

```
PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_charts_v112.py
```

Writes `reports/figs/v112/chart_01_situation_overlap.pdf` … `chart_08_baseline.pdf` (+ `_preview.png`), one per finding: MC_Situation, the legs against their bands (Paper A verdict), H1, H2, H3 (with raw Cov, MC_Positive), H4, H8, and the baseline. Titles describe the plot, never the finding.

## 3. Fill the paper

```
PYTHONDONTWRITEBYTECODE=1 python3 papers/v1_12/fill_paper_v1_12.py
```

Writes `papers/v1_12/v1_12_ssrn_paper_draft.md` and `…_draft_provenance.json` (JSON path, raw value and format of every number). It prints the selected cases (`CASE_GATE`, `CASE_MSIT`, `CASE_H1`–`CASE_H4`, `CASE_H5`, `CASE_H6`, `CASE_H7`, `CASE_H8`, `CASE_PARITY`). It refuses when the verdicts are synthetic (P1 not passed, or a `synthetic_fixture` key), P1 or P3 failed, P2 failed outside the declared fallback, `prereg_tag` is not `v1.12-prereg-r1`, the tag is missing, the anchor does not name the tag's commit, the tag is not dated 2026-11-11 02:45 UTC or `anchor/DEVIATIONS.md` no longer records that lock time and the waiver (Method §2.9 states both), H6 is active or H5 inactive (the anchor recorded H6 INACTIVE and H5 ACTIVE), or the primary panel does not follow the drop rule.

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

## Settled before data (for the coordinator)

Decided before any v1.12 answer existed (runner's log, "Decided by Claude", 10 November 2026, 9:59 pm) and applied on 11 November:

1. **Lock time.** Method §2.9 states in words that the pre-registration was locked on 11 November 2026 at 02:45 UTC, before the earliest lock time its text states (11 November, about 3 pm CT), because the pre-registrant waived the 24-hour review (10 November, 20:26 CT), as `anchor/DEVIATIONS.md` records in its entry made before the tag. Checked against tag `v1.12-prereg-r1` (tagger date 2026-11-10T20:45:38-06:00, as in `osf_anchor_v1_12.json`), `DEVIATIONS.md` at the tag, and the pre-registration's header and §12 (f). The real fill re-checks the tag's date and the entry.
2. **Romaniuk & Sharp.** Cited as the locked `cep_sets_v1_12.md` cites them: Romaniuk & Sharp (2016), *How Brands Grow: Part 2*, Oxford University Press (three citations in the text and the reference; other programme papers cite the 2022 revised edition). A test keeps it so.
3. **H5 and H6 in the real run.** Scoring passes `--h5-stage1` with v1.14's Stage 1 output (or `--h5-unavailable REASON`) and never `--h6` (Scoring, above). The scorer makes H5 active when tag `v1.14-prereg-r2` exists locally (it does).
4. **Fable drop.** Method §2.2 names the primary panel by the drop rule (pre-registration §7.3): N3, or C3 when Claude Fable 5.2 left the panel (flag `PRIMARY_C3` from `primary_panel`, checked against `models_dropped_section_7_3`). The same flag words the repetition of the gate in §2.7 and §3.6; §2.3 and §2.7 say "the primary panel" where they said N3, and §2.7 states the whole drop rule.

Also settled: **descriptives** (pre-registration §5) are printed in the appendix (per category and model; per-W coverage; run reliability with tokens and spend). **Citations** (11 November 2026): SSRN declined v1.9 (abstract 7685126), so the paper cites it by title with its thirdsystem.ai and OSF copies; no other paper cited here is on the list of papers SSRN declined, and v0.37 and v0.41 (submitted, not yet posted) are not cited.

## Open (for the coordinator)

- Step 5 (SSRN packet) and the file names `v1_12_ssrn_paper*` predate the decision of 11 November 2026 that methodology papers (v1.N) no longer go to SSRN by default; the paper's own text does not call it an SSRN paper. Left as they are.
