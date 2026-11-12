# AIAS 6.0 Preview (provisional): the paper pipeline after scoring

Built on branch `aias-6.0-preview-paper` (from `aias-6.0-preview` at `d67d23d`, the anchor commit after tag `aias-6-0-preview-prereg-r1` on `598990b`) on 11 November 2026, before the data lock (Dec 11, 2026). Mirrors the v1.11, v1.12 and v1.13 paper pipelines. **Paper only**: the Third System brand-format report waits for the new report design. Every builder reads only the locked scorer's outputs; no number is typed by hand. Results and Discussion are written in advance as alternative sentences, one for each outcome the plan defines, and the headline follows the wording fixed in §6.6 (classes A, A_k, B, C, U) with rules W1–W3. State and verdict words are printed exactly as `score_aias_6_0_preview.py` writes them, and the fill refuses outputs whose words the scorer's own functions do not reproduce.

## Inputs

| File | Written by |
|---|---|
| `osf/aias_6_0_preview/outputs/results_aias_6_0_preview.json` | `score_aias_6_0_preview.py --run --ref …` (once, after the data lock, §11.4) |
| `osf/aias_6_0_preview/outputs/gates_aias_6_0_preview.json` | same run (MQ_Gate, written before any statistic) |
| `osf/aias_6_0_preview/outputs/inputs_read_aias_6_0_preview.json` | same run (git ref, blob and SHA-256 of every input) |
| `osf/aias_6_0_preview/outputs/profile_aias_6_0_preview.csv` | same run (D4) |
| `osf/aias_6_0_preview/outputs/components/` | **you**, step 0: the component files the paper reads to name a MARGINAL leg (§4.2) |
| tag `aias-6-0-preview-prereg-r1` and `anchor/git_anchor_aias_6_0_preview.json` | lock (the fill refuses unless the anchor names the tag's commit) |
| `anchor/DEVIATIONS.md` | Entry 0 and C1–C6 before the lock; entries after it are counted in Method §2.8 |

## 0. After the scorer's run: extract the component files

The paper names the marginal leg of a MARGINAL part from the part's own record. Extract them from the refs the scorer used (`results.refs`), so that their SHA-256 equals the one in `inputs_read` (the fill checks it):

```
cd <worktree that ran the scorer>; O=osf/aias_6_0_preview/outputs; mkdir -p $O/components
git show <v1.14 ref>:osf/methodology/v1_14/outputs/stage1/stage1_v1_14.json > $O/components/stage1_v1_14.json
git show <v1.12 ref>:osf/methodology/v1_12/v112_verdicts.json > $O/components/v112_verdicts.json
git show <v1.13 ref>:osf/methodology/v1_13/v1_13_verdicts.json > $O/components/v1_13_verdicts.json
```

Then merge this branch next to the outputs: `git -C /Users/pablou/aias diff --stat aias-6.0-preview...aias-6.0-preview-paper` (it only adds `papers/aias_6_0_preview/` and three scripts), and `git merge --no-ff aias-6.0-preview-paper` in the worktree that holds the outputs.

## 1. Tests (22)

```
PYTHONDONTWRITEBYTECODE=1 python3 papers/aias_6_0_preview/tests/test_fill_paper_aias6.py
```

Expect `Ran 22 tests … OK`. They check: every switch value matches exactly one case and the cases are exactly the scorer's states and the plan's outcomes; the AI-use statement verbatim; the COI paragraph (v0.19 record, the Harman/Denon sentence with March 2017 and 23 September 2025, v0.22 tier-2/3 with Harman, Samsung SDI and Samsung Display) and Samsung only there; citations (v1.9 by its thirdsystem.ai and OSF copies, never SSRN 7685126; the chain v1.2–v1.9, AIAS 1.0/2.0, MSI; every reference cited); the §6.6 wordings and W1 phrases; the fixtures are marked synthetic, their component files match the input log, and the scorer's functions reproduce every state and verdict; the fixtures cover classes A, A_k, B, C, U, H_Structure CONFIRMED/PARTIAL/FALSIFIED/UNDETERMINED, H_PC_N3 in every band and untested, every component status, and Ranking PASS, PASS retest pending, MARGINAL, FAIL, NOT RUN; every scenario fills; every printed value re-resolves from its source (over 800); every number in the Abstract and Results is fixed text or a recorded value; H_Structure and H_PC_N3 are stated once with their verdicts and every S-test and I-test has one row with its verdict; **Ranking MARGINAL as §4.2 and W3 define it** (below the profile, under review, the marginal leg named with its ρ and n, outside K, pairs descriptive only, excluded from the composite check, "retest pending" while v1.14 has no final gate); class C refused without `--class-c-draft`; every case and flag renders; and the refusals (synthetic in real mode, real-looking in synthetic mode, a state or verdict word not the scorer's, a tampered component file, synthetic output inside the repository, charts or PDF of synthetic data without the watermark, the generator under `osf/`).

## 2. Figures

```
PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_charts_aias6.py
```

`reports/figs/aias6/chart_01_pairwise.pdf` (S-tests of K with intervals and bands; parts under review in a separate lower band, descriptive) and `chart_02_profile_coverage.pdf` (included parts rated per unit by category, D9). Every title carries "provisional".

## 3. Fill

```
PYTHONDONTWRITEBYTECODE=1 python3 papers/aias_6_0_preview/fill_paper_aias6.py
```

Writes `papers/aias_6_0_preview/aias_6_0_preview_paper_draft.md` and its provenance. **Class C** (H_Structure FALSIFIED): the fill refuses; under §6.6 drafting pauses and Claude writes a one-page options memo for Pablo. `--class-c-draft` builds an internal draft, marked as such on the title page, for that memo only.

## 4. Build

```
PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_paper_aias6.py
```

pandoc + xelatex + Carlito with the Carlito glyph-gap substitutions of the v1.11/v1.12 builder; tables via `tables_as_tabular.lua`.

## 5. Pre-flight

`pdftoppm -r 100 -png papers/aias_6_0_preview/aias_6_0_preview_paper.pdf /tmp/aias6_pf/p` and look at every page. Check by hand: the headline against §6.6 (class, k, d, the parts named); W1 for H_PC_N3; W2 when Sentiment is NOT RUN; W3 ("retest pending" in every Ranking sentence while v1.14 Stage 2 does not exist); a MARGINAL part's leg named from its own file; MQ_Blind (late inputs make the Preview's own tests exploratory); addenda (§4.4) are not automated: a gate that changes before the paper lock means re-running the scorer under the addendum rule and re-filling.

## Synthetic end-to-end test

```
zsh papers/aias_6_0_preview/tests/run_synthetic_e2e_aias6.sh /tmp/aias6_pipeline_test/e2e [--regenerate]
```

The fixtures (`tests/fixtures/<scenario>/`) are made by `tests/make_scenarios_aias6.py`: the locked scorer's own `run()` (require_lock=False, the mode of its own tests) on the scratch repository its own test fixture builds (`Synth`, imported read-only; invented brand names), with an overlay commit that sets the component gate words a scenario needs (and the hash records that chain them), and derived scenarios whose S-test / I-test statistics are changed and whose every word is recomputed with the scorer's functions (permutation draws 200, bootstrap 200, parallel analysis 100 for speed; the real run uses 10,000 / 2,000 / 1,000).

| Scenario | R | S | Cov | G | K | H_Structure | H_PC_N3 | Class |
|---|---|---|---|---|---|---|---|---|
| ranking_marginal (inputs as of Nov 11: v1.14 Stage 1 MARGINAL) | MARGINAL | NOT RUN | PASS | PASS | P, C, Cov, G | CONFIRMED | CONFIRMED | A_k |
| ranking_marginal_confirmed | MARGINAL | NOT RUN | PASS | PASS | P, C, Cov, G | CONFIRMED | CONFIRMED | A_k |
| ranking_marginal_partial | MARGINAL | NOT RUN | PASS | PASS | P, C, Cov, G | PARTIAL | CONFIRMED | B |
| retest_pending | PASS, retest pending | NOT RUN | PASS | PASS | P, C, R, Cov, G | CONFIRMED | CONFIRMED | A_k |
| six_parts / six_confirmed | PASS (Stage 2) | PASS, AI-judged | PASS | PASS | all six | CONFIRMED | CONFIRMED | A |
| six_partial | PASS | PASS, AI-judged | PASS | PASS | all six | PARTIAL | MARGINAL | B |
| six_falsified | PASS | PASS, AI-judged | PASS | PASS | all six | FALSIFIED | FALSIFIED | C |
| six_undetermined | PASS | PASS, AI-judged | PASS | PASS | all six | UNDETERMINED | UNDETERMINED | U |
| reduced_panel | PASS, retest pending | NOT RUN | PASS | PASS | (no structure, §4.3) | UNDETERMINED | not tested | U |
| parts_failed | FAIL | FAIL | MARGINAL | UNDETERMINED | P, C | UNDETERMINED | CONFIRMED | U |
| not_run | NOT RUN | NOT RUN | NOT RUN | NOT RUN | P, C | UNDETERMINED | CONFIRMED | U |

Synthetic builds: 13–16 pages (watermarked on every page).

## Ranking MARGINAL (the state of the inputs on Nov 11)

v1.14's Stage 1 on t4 (commit 3129674 on origin/v1.14) is MARGINAL. Under §4.1 the Preview reads it as Ranking MARGINAL; under §4.2 Ranking is then shown in a separate band below the profile, labelled "under review" with the marginal leg named (the paper reads every leg of `stage1_v1_14.json` whose verdict is MARGINAL, with its ρ and n), is not in K, enters no verdict (its pairs with K are printed as descriptive, §3.6), and is excluded from the composite check; under W3 every Ranking sentence says "retest pending" until v1.14's final gate (Stage 2) exists, which then enters by dated addendum (§4.4). Since Stage 1 is not SEPARABLE, v1.12's H5 does not gate and the R × Cov pair is not carried (§6.2). The scenario `ranking_marginal` and its two derived scenarios test exactly this text.

## Files

`papers/aias_6_0_preview/`: `aias_6_0_preview_paper_template.md`; `fill_paper_aias6.py` (engine forked unchanged from v1.11/v1.12) with `aias6_values.py`; `tables_as_tabular.lua`; `tests/` (`test_fill_paper_aias6.py`, `make_scenarios_aias6.py`, `run_synthetic_e2e_aias6.sh`, `fixtures/`). `scripts/`: `build_charts_aias6.py`, `build_paper_aias6.py`, `watermark_aias6.py`.

## Open (for the coordinator)

- §4.2 says a FAIL part's correlations are "printed in an appendix table, descriptive"; the scorer writes descriptive pairs only for MARGINAL parts (`descriptive_marginal_pairs`), so the paper prints none for a FAIL part (computing them here would be a new analysis).
- Addenda (§4.4) need a new scorer run and fill; the template has no addendum section yet.
- Sentiment Paper B's verdict enters only through the scorer's `sentiment_paper_b` input; the paper's Sentiment sentences cover PASS (qualifier removed) and FAIL, not "any other Paper B verdict printed beside the qualifier".
- The class C options memo is not drafted by this pipeline.
