# v1.13 Grounding Paper A: the commands after scoring

Built on branch `v1.13-paper` (from `origin/v1.13` at `232cf64`, the anchor commit after tag `v1.13-prereg-r1`) on 11 November 2026, before any $t_4$ search-on answer was read and before the Part II lock. Mirrors the Coverage pipeline (`papers/v1_12/` on branch `v1.12-paper`). Paper A is a methodology paper: no brand-format report (not a milestone) and no SSRN packet (Pablo's rule of 11 November 2026: v1.N papers no longer go to SSRN by default), so the outputs are `v1_13_paper*`. Every builder reads only the scorers' outputs; no number is typed by hand. Results and Discussion were written in advance as alternative sentences, one per pre-registered outcome, and the fill script picks one from the verdicts. Verdict words are printed exactly as `score_v1_13.py` writes them, and the fill refuses a file whose words, gate or Stage C2 re-issues the locked scorer's own functions do not reproduce.

## Inputs

| File | Written by | Required |
|---|---|---|
| `osf/methodology/v1_13/v1_13_verdicts.json` | `score_v1_13.py --stage C1`, then `--stage C2` (appends `stage_C2`) | yes; Stage C2 required unless `--interim` |
| `osf/methodology/v1_13/audit/v1_13_sdri.csv` | `audit_v1_13.py --sdri` (Part II, after pass 1 and the logged QID adjudications) | only if Part II was collected; the fill refuses it if Stage C2 recorded Part II as not collected, and refuses its absence if H7 was computed |
| `osf/methodology/v1_13/registries/brand_domains_v1_13.csv` | locked | brand names in the appendix |
| tag `v1.13-prereg-r1` and `anchor/git_anchor_v1_13.json` naming its commit | Part I lock | yes |
| tag `v1.13-audit-r1`, `anchor/audit_anchor_v1_13.json` (and `anchor/audit_receipt_v1_13.json`) | Part II lock | only if Part II locked; required if H7 was computed |
| `anchor/DEVIATIONS.md` | locked; dated entries added after the lock | yes (must still state the waiver of the 24-hour review; entries after the lock are counted) |

### What the fill reads from the verdict file (for checking)

- Stage C1 (`score_v1_13.stage_c1`): `phase`, `stage`, `primary_field`, `panel_models`, `dropped_models`; `gate` (`verdict`, `legs`, `active`, `gating`; `notes` only to detect a C1 downgrade, never printed); `verdicts`; `reasons` (H4/H6 PENDING); `legs.H1_Sep_Presence[0|1]` and `legs.H2_Sep_Consistency[0|1]` (S1 then S0: `n`, `rho_w`, `p`, `ci90.lo/hi`, `below_n_floor`); `legs.H4_Sep_Ranking[0]` / `legs.H6_Sep_Coverage[0]` if computed at C1; `H3` (`pairs[].pair/n/rho_w/qualifies`, `n_qualifying_pairs`, `rel1`, `rel3`, `p`); `MQ.MQ1_parsed_s1_records`; `MQ.MQ2.<model>` (`answers`, `with_source`, `share`, `flag_search_rarely_used`, `dropped_from_g_star`); `MQ.MQ3` (`share`, `flag`, `low_coverage`); `MQ.MQ4` (`via_title_share`, `unresolved_share`, `drop_gemini`); `MQ.MQ5` (`failed`, `zero_share`, `flat_substrates`, `n_rated`); `MQ.MQ6` (`rho_g_pi_s1`, `rho_gstar_g`, `flag`); `MQ.MQ8.<provider>`; `units.<sub|id>` (`m`, `g`, `o`, `G_star`, `rated`, `reason`, `house_portal_domain`); `descriptives.<sub|id>` (`mix.<class>`, `d`); `baseline.per_substrate_model.<sub|model>` (`share_with_source`, `domains_per_answer`, `share_any_brand_owned`, `mix`); `baseline.g_star_by_substrate.<sub>` (`units`, `rated`, `median`, `q1`, `q3`, `share_zero`); `baseline.top_domains`; `H4_ranking_source` / `H6_coverage_source` (`status`, `sha256`, `stage1_verdict`, `h4_gates`, `dry_run`, `v1_12_commit`); `sensitivities.<S>` (`rho.H1|H2[S1,S0]`, `rel3`, `gate`, `verdicts`); `sensitivities.S8_leave_one_substrate_out.<sub>`; `verdict_changes`.
- Stage C2 (`score_v1_13.main --stage C2`): `stage_C2.H7_Struct_Gap`, `.reason`, `.leg` (`n`, `rho_w`, `p`, `ci90`), `.rho_sdri_p_s0`, `.partial_rho_sdri_gstar_given_p_s0`; `stage_C2.ranking` (`H4_Sep_Ranking`, `leg`, `H4_ranking_source`, `h4_gates`, `gate_reissued.before/after`, `reason`, `note`); `stage_C2.coverage` (`H6_Sep_Coverage`, `leg`, `H6_coverage_source`, `gate_reissued`, `reason`); `stage_C2.appended_utc`.
- SDRI table (`audit_v1_13.SDRI_FIELDS`): `substrate`, `brand_id`, `phantom`, `p1_outcome`, `i1`–`i8`, `SDRI`.
- The final gate verdict is the last `gate_reissued.after` of Stage C2 (coverage after ranking, as `main` chains them), else the Stage C1 `gate.verdict`.

## Scoring (coordinator, in the `v1.13` worktree; not part of this pipeline)

`osf/methodology/v1_13/LOCK_STEPS.md` §9: Stage C1 after $t_4$ is complete and its raw file's SHA-256 is recorded; H4 waits for v1.14's Stage 1 output (`--h4-stage1`), H6 for v1.12's scored output (`--h6-cov`); Stage C2 with `--h4-unavailable REASON` / `--h6-unavailable REASON` if a score does not exist by then. The verdict file is written to `osf/methodology/v1_13/v1_13_verdicts.json` (C2 appends to it).

## 0. Bring the pipeline next to the scored data

`v1.13-paper` only adds files (`papers/v1_13/`, three scripts in `scripts/`). It changes nothing under `osf/methodology/v1_13/` and no file in the lock manifest.

```
git -C /Users/pablou/aias diff --stat v1.13...v1.13-paper
cd /Users/pablou/aias/_worktrees/v1.13 && git merge --no-ff v1.13-paper
```

`python3` is the system Python 3.14 (matplotlib, reportlab, pypdf); pandoc with xelatex, Carlito and `pdftoppm`.

## 1. Tests (23)

```
PYTHONDONTWRITEBYTECODE=1 python3 papers/v1_13/tests/test_fill_paper_v1_13.py
```

Expect `Ran 23 tests … OK`. They check: every switch value matches exactly one case; the AI-use statement, the Denon/Harman correction and the Samsung rule (Samsung, Harman and Cheil only in the COI paragraph); citations only from `papers/references.bib` or records the locked pre-registration names (no declined or unposted SSRN number, no ssrn.com link); the thresholds in the text equal the scorer's constants; no shipping language; every fixture is SYNTHETIC_ and reproduced by the scorer's verdict functions; the twelve scenarios cover every gate case and every H1, H3, H4, H6, H7 and Part II state; every scenario fills, every number in each filled paper is pre-registration text or a recorded value, and every value re-resolves from its path; every gate-leg verdict renders; the wording of Part II held / locked-not-run, dependencies unavailable, the interim draft and the C1 and C2 downgrades; the Cheil switch (off by default; on, only in the COI paragraph); and the refusals (inconsistent word, wrong re-issue, SDRI table against Part II state, synthetic in real mode, real-looking file in synthetic mode, synthetic output in the repository, charts and build without a watermark, scenario output under `osf/`).

## 2. Figures

```
PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_charts_v113.py
```

Writes `reports/figs/v113/chart_01_search_use.pdf` … `chart_08_sdri_gstar.pdf` (+ `_preview.png`): search use per category and model (RQ1/MQ2), source-type mix (RQ2), G\* by category (RQ2), H1 and H2 under every analysis, H3's run pairs, every leg against its bands (the gate), and SDRI against G\* (H7; only if Part II was collected). Titles describe the plot, never a finding or a section.

## 3. Fill the paper

```
PYTHONDONTWRITEBYTECODE=1 python3 papers/v1_13/fill_paper_v1_13.py            # add --interim for a Stage C1 draft
```

Writes `papers/v1_13/v1_13_paper_draft.md` and `…_draft_provenance.json` and prints the selected cases (`CASE_GATE`, `CASE_H1`–`CASE_H7`, `CASE_PART2`). `--coi-cheil` adds the optional Cheil Worldwide / Iris sentence to the COI paragraph (**pending decision; off by default**). Real-mode refusals: listed in the script's docstring.

## 4. Build the PDF

```
PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_paper_v1_13.py
```

Writes `papers/v1_13/v1_13_paper.pdf` (pandoc, xelatex, Carlito; tables via `tables_as_tabular.lua`, the per-brand appendix as a longtable). A missing Carlito glyph is printed as a warning; add it to `UNICODE_SUBS`.

## 5. Pre-flight (CLAUDE.md: before commit, tag or deposit)

```
rm -rf /tmp/v113_pf && mkdir /tmp/v113_pf && pdftoppm -r 80 -png papers/v1_13/v1_13_paper.pdf /tmp/v113_pf/paper
```

Look at every page; read the selected Results and Discussion sentences against `v1_13_verdicts.json`; confirm Samsung appears only in the COI paragraph. Then commit the figures, the draft and its provenance, and the PDF.

## Synthetic end-to-end test (no real data; every page and chart stamped "SYNTHETIC TEST — NOT RESULTS")

```
cd /Users/pablou/aias/_worktrees/v1.13-paper && zsh papers/v1_13/tests/run_synthetic_e2e_v1_13.sh /tmp/v113_pipeline_test/e2e
```

`tests/make_scenarios_v1_13.py` imports the locked scorers read-only and runs `stage_c1` on the synthetic inputs of their own unit tests (`test_score_v1_13.synthetic_t4`: 5 categories × 8 invented brands under `.test`), then the Stage C2 sequence of `main` (`stage_c2`, `stage_c2_ranking`, `stage_c2_coverage`) with an SDRI table written by `audit_v1_13.sdri_rows` from synthetic audit records and synthetic v1.14 / v1.12 comparator files (`test_clarification_v1_13.write_stage1` / `write_v112`). Derived scenarios change one gate leg's statistics and recompute every word with the scorer's `sep_verdict`, `reliability_verdict`, `struct_gap_verdict` and `gate`.

| Scenario | Gate (final) | H4 | H6 | H7 | Part II |
|---|---|---|---|---|---|
| scored | PASS | gating, CONFIRMED (C2) | CONFIRMED (C2) | CONFIRMED | collected |
| pass_reported | PASS | FALSIFIED, reported, not gating (Stage 1 FAIL) | CONFIRMED | FALSIFIED | collected |
| downgraded | MARGINAL (PASS re-issued at C2 by H4) | gating, FALSIFIED | CONFIRMED | MARGINAL | collected |
| downgraded_h6 | MARGINAL (PASS re-issued at C2 by H6) | gating, CONFIRMED | FALSIFIED | CONFIRMED | collected |
| c1_h4 | MARGINAL (downgraded at C1 by H4) | gating, FALSIFIED (C1) | CONFIRMED | CONFIRMED | collected |
| fail | FAIL (H1 FALSIFIED) | unavailable by C2 | unavailable by C2 | not collected | held (not locked) |
| marginal | MARGINAL (H2) | reported (Stage 1 MARGINAL) | unavailable by C2 | not collected | locked, not run |
| h3_undetermined | MARGINAL (H3 UNDETERMINED) | gating, below the floor | CONFIRMED | below the floor | collected |
| dropped | FAIL (H3 FALSIFIED); Gemini dropped (MQ4), MQ2/MQ3/MQ6 flagged, S10/S11 change a word | gating, CONFIRMED | FALSIFIED | CONFIRMED | collected |
| mq5 | UNDETERMINED (MQ5 failed) | unavailable | unavailable | not collected | held |
| floor | UNDETERMINED (H1 below the floor) | gating, CONFIRMED | CONFIRMED | FALSIFIED | collected |
| interim | PASS at Stage C1 only (`--interim`) | pending | pending | pending | locked, not run |

The committed fixtures (`tests/fixtures/SYNTHETIC_*`) are these twelve verdict files and the eight SDRI tables. Outputs go only under the given `/tmp` directory; the script refuses a path in the repository, and `make_scenarios_v1_13.py` refuses any path under `osf/`. Synthetic statistics are not meaningful (40 invented units; derived legs edited); only the wording and layout are under test.

## What selects the wording

| Switch | Values | Source in the verdict file |
|---|---|---|
| `CASE_GATE` | PASS, FAIL, MARGINAL, MARGINAL_DOWNGRADED, UNDETERMINED_MQ5, UNDETERMINED | final gate (C1 `gate.verdict`, then Stage C2 `gate_reissued.after`); C1 downgrade note or a C2 PASS→MARGINAL; `MQ.MQ5.failed` |
| `CASE_H1`, `CASE_H2` | CONFIRMED, MARGINAL, FALSIFIED, UNDETERMINED_FLOOR, UNDETERMINED_MQ5 | `verdicts`, `MQ.MQ5.failed` |
| `CASE_H3` | CONFIRMED, MARGINAL, FALSIFIED, UNDETERMINED_PAIRS | `verdicts.H3_Run_Reliability` |
| `CASE_H4` | INACTIVE, PENDING, UNAVAILABLE, GATING, REPORTED | `gate.active`, `H4_ranking_source.sha256` (C1) or `stage_C2.ranking.leg`, `h4_gates` |
| `CASE_H5` | INACTIVE, ACTIVE | `gate.active.H5_Sep_Sentiment` |
| `CASE_H6` | INACTIVE, PENDING, UNAVAILABLE, COMPUTED | `gate.active`, `H6_coverage_source.sha256` or `stage_C2.coverage.leg` |
| `CASE_H7` | CONFIRMED, MARGINAL, FALSIFIED, UNDETERMINED_FLOOR, NOT_COLLECTED, PENDING | `stage_C2.H7_Struct_Gap`, `stage_C2.leg` |
| `CASE_PART2` | COLLECTED, LOCKED_NOT_COLLECTED, NOT_LOCKED, PENDING | `stage_C2.leg`; tag `v1.13-audit-r1` (synthetic: `synthetic_fixture.part2`) |

## Files

`papers/v1_13/`: `v1_13_paper_template.md`; `fill_paper_v1_13.py` (engine forked unchanged from v1.12) with `v113_values.py`; `tables_as_tabular.lua` (v1.12's, plus longtable for tables over 32 rows); `PIPELINE.md`; `tests/` (`test_fill_paper_v1_13.py`, `make_scenarios_v1_13.py`, `run_synthetic_e2e_v1_13.sh`, `fixtures/SYNTHETIC_*`). `scripts/`: `build_charts_v113.py`, `build_paper_v1_13.py`, `watermark_v113.py`.

## Rules kept

- No analysis outside the pre-registration; the paper reads only the scorers' outputs (counts and medians over the SDRI table are named functions recorded in the provenance).
- Samsung (and Harman, Cheil) appear only in the COI paragraph of the Declarations, which carries the pre-registration's §11 text: the two items of record quoted, the Denon/Harman correction of 10 November 2026 and its handling (S11).
- The "Use of AI tools" statement is CLAUDE.md's, verbatim. ™ marks the first mention of AIAS and of Third System (title page).
- Background cites only `papers/references.bib` entries (as the bib gives them) and records the locked pre-registration names.
- A failed or undetermined gate is reported with the redesign path the pre-registration gives (§3, §8); there is no shipping language.

## Open (for the coordinator)

See the hand-off report of 11 November 2026: items the locked texts leave open (S6 and S7 not computed by the scorer's command line; §6's cited-set tables; SDRI_kg-only sensitivity; AQ3/AQ4; the C1 gate note when H4 is merely pending; the lock-time wording) and the pending Cheil decision.
