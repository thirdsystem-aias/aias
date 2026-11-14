# v0.43 Stage 1 paper: the commands after scoring

Built on branch `v0.43-paper` (from `origin/v0.43` at `4f8abfa`, the day-1 run-time records after tag `v0.43-prereg-r1`) on 11 November 2026, before any Stage 1 search-interest data existed. Programme queue row 8: predictive validity on past data (June scores → search-interest change to November). Mirrors the Coverage pipeline (`papers/v1_12/` on branch `v1.12-paper`). A paper only: no Third System brand-format report (not a milestone study) and no SSRN packet (validity papers no longer go to SSRN by default; Pablo, 11 November 2026). Every builder reads only the scorer's output and the stored request records; no number is typed by hand. Results and Discussion were written in advance as alternative sentences, one for each outcome the pre-registration allows, and the fill picks one from the verdicts. Verdict words, labels and flags are printed exactly as `score_v0_43.py` writes them.

Title (true whatever the result): *AI Availability Scores and Later Change in Brand Search Interest: A Pre-Registered Test of Predictive Validity on Past Data, June to November 2026 (AIAS™ v0.43, Stage 1)*.

## Inputs

| File | Written by | Read by |
|---|---|---|
| `osf/v43/v43_stage1_verdicts.json` | `score_v0_43.py --stage 1` (the only file Stage 1 writes) | fill, charts |
| `osf/v43/data/trends_raw/main{1,2,3}/<substrate>_b<j>.json` | `acquire_trends_v0_43.py pull --n 1/2/3` | fill (`fetched_utc`, `status`, `n_attempts` only) |
| tag `v0.43-prereg-r1` → commit `8c96d9cf`, tagger date 2026-11-11 06:31 UTC; `osf/v43/anchor/osf_anchor_v0_43.json`; `osf/v43/anchor/DEVIATIONS.md`; `osf/v43/prereg/LOCK_MANIFEST_v0_43.sha256` | the lock | fill (refuses unless all agree and every locked file still has its SHA-256) |

### Fields of the verdicts file the fill and charts read

- top level: `stage` (= 1), `prereg` (= `PRE_REGISTRATION_v0_43.md (tag v0.43-prereg-r1)`), `pulls_used` (= `main1`–`main3`), `B_perm`, `B_boot` (= 10,000 each), `flags`, and the absence of `synthetic_fixture`;
- `manipulation_checks`: `MC_Concurrent.{rho, p_one, n, pass_}`; `MC_PullReliability.{mean_pairwise_pooled_spearman, pairs, pass_}`; `MC_Weekly.{requests, ok, missing, resent}`; `MC_Terms.{share_topic, pass_}`; `MC_Chain.<pull>.<substrate>.{links_held, links}`;
- `outcome_defined_per_substrate.<substrate>.{units, Y_defined}`;
- `tests.<H_Pred_Presence | _SA | _Momentum | H_Pred_Consistency>.{n, n_per_substrate, seed, min_n, spec.{x, y, controls}, rho, p_one, p_two, ci90, ci95, boot_valid, verdict, labels, reason, flags}`;
- `descriptives.per_substrate.<test>.<substrate>.{rho, n, p_one}`; `descriptives.presence_without_defunct_automotive.<3 Presence tests>`, `recall_alone`, `topic_only_primary`, `longer_lead_P_t1` (each `{n, rho, ci90, p_one}`); `descriptives.cross_lagged.{n, rho_AI_to_search, rho_search_to_AI, difference, difference_ci90, difference_ci95}`;
- `unit_table[*].{sub, kind, Y, Y_SA, M, L, P, Cs}` (counts of topic units and defined outcomes; each test's rho and `MC_Concurrent`'s rho recomputed with the scorer's own `rho_pw`; the residual-rank scatters).

Not read: `created_utc`, the descriptives' `ci95` and `p_two`, `unit_table` columns `Yp`, `L_end`, `pi`, `P_t1`, `P_new`, and `MC_Concurrent.n_per_substrate`.

## Scoring (coordinator, in the `v0.43` worktree, after the third pull; before step 0)

```
cd /Users/pablou/aias/_worktrees/v0.43
PYTHONDONTWRITEBYTECODE=1 python3 osf/v43/scripts/score_v0_43.py --stage 1
```

Defaults: 10,000 permutations and bootstrap resamples, raw records from `osf/v43/data/trends_raw/`, output `osf/v43/v43_stage1_verdicts.json`. It refuses if any of the 84 main records is absent (never pass `--allow-incomplete` or other `--B-*` values for the real run: the fill refuses both).

## 0. Bring the pipeline next to the scored data (coordinator)

`v0.43-paper` only adds files (`papers/v0_43/`, three scripts in `scripts/`); it changes nothing under `osf/v43/` and no locked file. Three dots compare with the fork point:

```
git -C /Users/pablou/aias diff --stat v0.43...v0.43-paper
cd /Users/pablou/aias/_worktrees/v0.43 && git merge --no-ff v0.43-paper
```

Run steps 1 to 5 from that worktree. `python3` is the system Python 3.14 (numpy, scipy, matplotlib, reportlab, pypdf); pandoc with xelatex, Carlito and `pdftoppm`.

## 1. Tests (22)

```
PYTHONDONTWRITEBYTECODE=1 python3 papers/v0_43/tests/test_fill_paper_v0_43.py
```

Expect `Ran 22 tests … OK`. They check: every switch value matches exactly one case; the COI paragraph equals the pre-registration's §7 text word for word (one change of tense, "the pre-registration was locked") plus only the optional Cheil sentence; the AI-use statement verbatim; Samsung only in the COI paragraph; the hypotheses quoted verbatim from the pre-registration with section numbers; no SSRN number or ssrn.com link for a declined or unposted paper, v1.9 by title with its thirdsystem.ai and OSF copies, the foundational paper as `papers/references.bib` has it; the five fixtures are synthetic, are the locked scorer's own output (every verdict, label, reason and flag re-derived; each rho recomputed from the unit table) and together cover CONFIRMED, MARGINAL, FALSIFIED, UNDETERMINED (thresholds) and UNDETERMINED (minimum n) for the primary test, REVERSED, all three flags, each check passing and failing, a missing request and failed chain links; every fixture fills, and every number in each filled paper is fixed pre-registration text or a recorded value; provenance re-resolves; every outcome renders for every test (the six cases, REVERSED with FALSIFIED and with UNDETERMINED, below-minimum with and without a statistic, rho undefined), with the words from the scorer's `verdict()`; all eight flag combinations render; the Cheil switch is off by default; 19 kinds of tampering are refused (rho, word, label, flags, seed, minimum n, spec, n per category, unit table, intervals, a check's pass, records against `MC_Weekly`, draws, pulls, stage, a missing test, a missing interval, outcome counts); the real-mode path on a relabelled fixture in memory, including the 24-hour spacing and a missing pull; the lock records and their tamper check; the refusals to write synthetic output inside the repository; the chart and build watermark rules; and that `osf/v43` is untouched.

The locked kit's own tests still pass: `python3 osf/v43/scripts/tests/run_all_v0_43.py` → `16/16 pass`.

## 2. Figures

```
PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_charts_v043.py
```

Writes `reports/figs/v043/chart_01_checks.pdf` … `chart_08_descriptives.pdf` (+ `_preview.png`), one per finding: the two checks (`MC_Concurrent`, `MC_PullReliability`), the primary test, the four tests against the thresholds, each secondary test, the per-category descriptive, and descriptives 2–6. Titles describe the plot and never repeat a finding's or section's title. Refuses unless the verdicts pass the consistency check.

## 3. Fill the paper

```
PYTHONDONTWRITEBYTECODE=1 python3 papers/v0_43/fill_paper_v0_43.py
```

Writes `papers/v0_43/v0_43_paper_draft.md` and `…_draft_provenance.json` (path, raw value and format of every number). Prints the selected cases (`CASE_PRES`, `CASE_SA`, `CASE_MOM`, `CASE_CONS`) and flags. It refuses when the verdicts are synthetic; the tag, its commit or date, the anchor, the deviations record or a locked file's SHA-256 disagree; any verdict, label, reason or flag differs from the locked scorer's rule on the recorded statistics; a test's rho differs from the one recomputed from the unit table; the draws are not 10,000, the pulls not `main1`–`main3`, the units not 112; the stored records are not 28 per pull, disagree with `MC_Weekly`, or a pull started less than 24 hours after the previous one was stored; or a value a selected sentence needs is missing.

**Pending decision (do not switch on without Pablo):** `--coi-cheil` adds one COI sentence: Samsung's agency Cheil Worldwide, or its Iris unit, has worked for Chevrolet, BMW, Bentley (v0.22), Jack Daniel's (v0.23, S03) and Eucerin (v0.20), all five in this study's units (source: v0.62 DEVIATIONS Entry 0, Part F). Off by default. The release paper (14 November 2026) was filled with `--coi-cheil`: all five brands are units of this study, and CLAUDE.md's COI rule asks for disclosed relationships rather than a clean claim; the analysis keeps them as locked.

## 4. Build the PDF

```
PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_paper_v0_43.py
```

Writes `papers/v0_43/v0_43_paper.pdf` (pandoc, xelatex, Carlito; tables via `tables_as_tabular.lua`). The curly-quote substitutions of the v1.12 list are dropped (Carlito has the glyphs; the old substitution turned quoted words into code spans). A missing Carlito glyph is printed as a warning; add it to `UNICODE_SUBS`.

## 5. Pre-flight (CLAUDE.md: before commit, tag or deposit)

```
rm -rf /tmp/v043_pf && mkdir /tmp/v043_pf && pdftoppm -r 80 -png papers/v0_43/v0_43_paper.pdf /tmp/v043_pf/paper
```

Look at every page; read the selected Results and Discussion sentences against `v43_stage1_verdicts.json`; confirm Samsung appears only in the COI paragraph. Then commit the figures, the draft, its provenance and the PDF.

## Synthetic end-to-end test (no real data; every page and chart stamped "SYNTHETIC TEST — NOT RESULTS")

```
cd /Users/pablou/aias/_worktrees/v0.43-paper && zsh papers/v0_43/tests/run_synthetic_e2e_v0_43.sh /tmp/v043_pipeline_test/e2e
```

`tests/make_scenarios_v0_43.py` builds, for each scenario, a scratch repository root outside this repository with 112 invented units (`SYN-H01` … `SYN-S24`, the real category sizes, five automotive units in cell D), synthetic P, C* and π̂, synthetic term kinds, main bundles formed by the locked rule, and 84 synthetic request records per scenario in the acquisition script's stored format (Trends-style 0–100 integers relative to each bundle's largest value). The locked scorer's `score()` (imported read-only) scores each root with 10,000 draws; its output is written with the scorer's `dump_json`, with one added key, `synthetic_fixture`. Nothing is written under `osf/v43/`.

| Scenario | Planted | Primary verdict (the scorer's) | Checks |
|---|---|---|---|
| lead | Presence → later gain | CONFIRMED (all four CONFIRMED) | all pass |
| lag | Presence → later loss | FALSIFIED, REVERSED (secondaries FALSIFIED, three REVERSED) | all pass |
| null | none | UNDETERMINED (thresholds not met) | all pass |
| marginal | weak gain; seed searched until the scorer returned MARGINAL | MARGINAL (SA UNDETERMINED, Consistency FALSIFIED REVERSED) | all pass |
| sparse | half the units without volume, one request missing, noisy pulls, Presence unrelated to level, 33% topics | UNDETERMINED (59 < 60); Consistency FALSIFIED | all three flags; failed chain links |

The committed fixtures (`tests/fixtures/SYNTHETIC_*`) are these five verdict files with their pull summaries. Each synthetic paper has 18 pages.

## What selects the wording

| Switch / flag | Values | Source in the verdicts |
|---|---|---|
| `CASE_PRES`, `CASE_SA`, `CASE_MOM`, `CASE_CONS` | CONFIRMED, MARGINAL, FALSIFIED, UNDETERMINED (thresholds), UNDETERMINED_N (`reason` "n=… < …"), UNDETERMINED_RHO (`reason` "rho undefined") | `tests.<name>.verdict`, `.reason` |
| `<K>_REVERSED` | true / false | `tests.<name>.labels` |
| `ANY_FLAG`, `FLAG_LIST` | the scorer's flag words | `flags` |
| `CONC_PASS`, `REL_PASS` | true / false | `MC_Concurrent.pass_`, `MC_PullReliability.pass_` |
| `XL_HAS` | cross-lagged computed | `descriptives.cross_lagged` |
| `COI_CHEIL` | false unless `--coi-cheil` | argument (pending decision) |

## Files

`papers/v0_43/`: `PIPELINE.md`; `v0_43_paper_template.md`; `fill_paper_v0_43.py` (template engine forked unchanged from v1.12) with `v043_values.py`; `tables_as_tabular.lua` (copied); `tests/` (`test_fill_paper_v0_43.py`, `make_scenarios_v0_43.py`, `run_synthetic_e2e_v0_43.sh`, `fixtures/SYNTHETIC_*`). `scripts/`: `build_charts_v043.py`, `build_paper_v0_43.py`, `watermark_v043.py`.

## Rules kept

- No analysis outside the pre-registration: the paper reads only the scorer's output and the stored request records; the residual ranks in the charts and the consistency check use the scorer's own `rho_pw`.
- Samsung appears only in the COI paragraph, which is the pre-registration's §7 text (with the Denon/Harman correction of 10 November 2026 and the v0.22 tier-2/3 disclosure).
- The "Use of AI tools" statement is CLAUDE.md's, verbatim. ™ marks the first mention of AIAS and of Third System.
- The limits are stated plainly: search interest is not sales; Stage 1 is a test on past data; the confirmatory test is Stage 2 (pulls from 10 March 2027).
