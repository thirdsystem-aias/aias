# AIAS™ methodology v1.17 — How many runs are enough

**Pre-registration, revision r1 (draft for the lock).** Exploratory re-analysis of archived answers. Prepared Thu Nov 12, 2026 (US Central) in worktree `_worktrees/v1.17`, branch `v1.17`, based on branch `v0.42` at commit `31c64c6` (the t4 scoring commit, tag `v0.42-scoring-locked`; the coded answers were committed at `a790bb1`, tag `v0.42-acquisition-locked`, Nov 11, 2026). To be locked at git tag `v1.17-prereg-r1`, pushed and deposited on OSF (`methodology/v1_17/`) before any estimand below is computed on real data.

**Status: declared exploratory.** There are no confirmatory hypotheses and no verdicts. What is fixed here, before the data are analysed, is the exact estimands, the code, the outputs and the reporting rule. Approved as Study B of the Nov 11 literature check (Pablo, "ok plan updates", Wed Nov 11, 2026, 11:22 pm). Cost: $0 (no API calls).

---

## §1 Question and why now

**Question.** How much does a brand's Presence move from one run to the next on the newest models, and how many runs per cell does a study need for a brand's Presence to have a standard error below 0.10 and below 0.05?

**The literature check's definition, word for word.** "(B) How many runs are enough — Keep. Re-analysis: per-brand standard error of Presence against the number of runs, by category size (registry brand count). Use t4's three runs per cell for run-to-run noise; keep the omnibus waves (May 20–26, Jun 10, Nov 9) separate, since they mix time drift with run noise; project the runs needed for a standard error below 0.10 and 0.05 (Schulte's benchmarks), stating that projection beyond three runs assumes independent runs. Declared exploratory. If done before v0.40's lock, v0.40 can check its runs per cell; it never holds that lock." (project doc `claude/literature-check-2026-11-11.md`, plan-placement table.)

**Outside evidence (as verified at source on Nov 11, 2026, same doc).**
- Schulte, Bleeker and Kaufmann, "Don't Measure Once: Measuring Visibility in AI Search (GEO)", arXiv 2604.07585 (submitted Apr 8, 2026): brand visibility needs at least 7 runs per prompt per day (bootstrap standard error 0.081 at 7); per-brand standard error below 0.10 at 10 days and below 0.05 at 24 days; 2–4 week rolling windows recommended. German-language prompts; ChatGPT, Gemini, Google AI Mode, Perplexity.
- SparkToro with Gumshoe (Rand Fishkin, Jan 27, 2026; not peer-reviewed): advises asking "usually at least 60-100X"; smaller markets steadier than broad ones.

**Why now.** v0.40's pre-registration is due Fri Nov 13, 7 pm, and v0.40 locks Mon Nov 16. If this study's result is in hand first, v0.40 can check its runs per cell against it (§6). v1.17 never holds v0.40's lock.

**Not like for like with Schulte et al.** Their standard errors are for one prompt's visibility on an engine; the program's per-run Presence of a brand on one model averages six questions (frames) per run. A brand's per-run Presence therefore moves less than a single question's answer. The frame-level estimand (§4, A-frame) puts the t4 noise on the per-question scale for comparison; the benchmarks 0.10 and 0.05 are applied to the program's own Presence scale (0 to 1), as the literature check asked.

---

## §2 Data

### §2.1 t4 (study v0.42): run-to-run noise

- **What.** The newest models (panel N3: Claude Fable 5.2 `claude-fable-5-2`, GPT-6 Astra `gpt-6-astra`, Gemini 4 Argon `gemini-4-argon`), search off (S0) and on (S1), three runs per cell, the five omnibus categories; 876 calls, all answered (v0.42 MC_Complete 876/876; no served-ID exclusion; no model × condition dropped). Collected and committed Nov 11, 2026 (commit `a790bb1`).
- **Coded answers used.** Phase B only (the recall questions): `osf/v42/data/coded/v19_phase_b.csv` … `v23_phase_b.csv`, one row per (call, registry brand), column `mentioned` (1 = the answer named the brand), coded by v0.42's locked coder. Phase A (recognition) is not used: it has one run (S0, run 1), so it has no run-to-run noise to measure.
- **Counts per cell (loader check, §7).** 12,096 rows; 672 units = 112 brands × 3 models × 2 conditions; every unit has 3 runs × 6 frames, none missing or duplicated. 30 answer cells (category × model × condition): in v0.19 (16 brands) 6 cells of 16 units; in v0.20–v0.23 (24 brands each) 24 cells of 24 units.
- **Categories and size (registry brand count).** v0.19 audiophile headphones 16; v0.20 skincare 24; v0.21 cosmetics 24; v0.22 automotive 24; v0.23 premium spirits 24 (brands coded S01–S24 in the t4 tables).

### §2.2 Omnibus waves: time drift plus run noise (reported separately)

- **What.** The same five categories and six frames, legacy six models (Claude Opus 4.5, Claude Sonnet 4.5, GPT-4o, GPT-4o mini, Gemini 2.5 Flash, Gemini 2.5 Flash Lite), one run per wave: t1 May 20–26, t2 Jun 10, t3 Nov 9, 2026 (`Try system book/archive_inventory_nov10.md`; t3's date also in v0.42's pre-registration §2.2).
- **Input.** `osf/v41/v41_three_wave_table.csv` (v0.41's locked three-wave table), column `k_per_model` (mentions over the six frames, one count per legacy model, in the order of `score_v0_31.PANEL`). 336 rows = 112 brands × 3 waves; 672 units = 112 brands × 6 models. The table's `pi_hat` equals sum(k) ÷ 36 on every row (loader check).
- **Why separate.** A change between waves is run noise plus real change over three weeks (t1→t2) or five months (t2→t3), on different models from t4. It cannot be split into the two with one run per wave, so it is never pooled with t4's run-to-run noise and no runs projection is made from it.

---

## §3 Design choices, argued

1. **Unit: brand × model × search condition.** This is the cell a study runs repeatedly. Providers differ systematically (v0.33, H_Provider_Asymmetry CONFIRMED), and search on and off are separate cells in every current design; computing the variance within the unit keeps those differences out of "run noise". Presence is computed per category's six-frame question set, so the question set is fixed within a unit and is not a further factor. The N3 panel mean (the brand table's `pi_N3_<cond>`) is reported alongside (A-panel), because that is the published figure.
2. **Per-run Presence** p_{u,r} = mentions ÷ 6 (every t4 Phase B call was answered, so the answered-call denominator of v0.42 equals 6).
3. **Run-to-run variance per unit** s²_u = the sample variance (n − 1 denominator) of p_{u,1}, p_{u,2}, p_{u,3}. With three runs each unit's own value has only 2 degrees of freedom, so the projection uses the **pooled** variance of a stratum, σ̂²_g = mean of s²_u over its units (every unit has the same degrees of freedom). Per-unit standard errors are reported only as counts (E4), never projected one by one.
4. **Standard error from R runs** SE_g(R) = σ̂_g ÷ √R. For R = 1, 2, 3 this is what t4 observed (Presence from 1, 2 or 3 runs); beyond three it is a projection.
5. **Runs needed** R*_g(τ) = the smallest whole R with σ̂_g ÷ √R < τ, for τ = 0.10 and 0.05 (strictly below, as "below 0.10"). **Assumption, stated wherever a projection appears: runs are independent and have the same variance as t4's three runs.** Runs collected on one day by one account may be more alike than runs spread over days; then the projection is too optimistic for day-to-day use, and the omnibus figures (§2.2) bound the other side.
6. **By category size and by Presence level.** Size (registry brand count) is the literature check's moderator; t4 has two sizes only, 16 (one category, v0.19) and 24 (four categories), so a size difference cannot be told apart from a category difference; every category is also reported (alongside). A proportion-like score varies most near the middle, so units are also grouped by Presence level, from their total mentions K over the 18 answers: zero (K = 0), low (1–5), middle (6–12), high (13–17), full (18). Zero and full units have no run-to-run variance by construction; they stay in the primary estimate (they are measured, stably) and a "named, not saturated" stratum (1 ≤ K ≤ 17) is reported alongside. Grouping on the observed level is descriptive (a unit's level is itself measured with noise).
7. **Intervals.** Units in the same answer cell (category × model × condition) are coded from the same answers, so they are not independent. Primary interval: a percentile cluster bootstrap that resamples whole answer cells within the stratum (10,000 draws, seed 117017), mapped to R* by the rule in point 5. Alongside: a χ² interval with 2 degrees of freedom per unit, which assumes independent, normal units and is known to be too narrow (dry run, §8). A stratum with fewer than 10 clusters is flagged (`few_clusters_flag`): size 16 has 6 clusters, and in the dry run its interval covered the true value in 84–88% of replicates, not 95%.
8. **Once instead of three times.** Two published uses of a brand's Presence are checked: its place among the brands of its category, and the recall floor of v0.42 descriptive 3 (6 · π̂ < 1 on N3; 49 of 112 brands below it in S0 with three runs). For each run, the one-run value is compared with the three-run value.
9. **Omnibus waves:** reported beside t4, never pooled, no projection (§2.2).
10. **Conflict-of-interest sensitivity (S-COI).** As in v0.62 (pre-registrant's decision of Nov 12, 2026), the primary results keep every brand, and the main estimates are also reported without Denon and the five brands with Cheil Worldwide or Iris agency ties (Chevrolet, BMW, Bentley, Jack Daniel's, Eucerin): 106 brands, 636 t4 units. Jack Daniel's is v0.23's `S03` (v0.42 probe file).

---

## §4 Estimands (exact; code `scripts/analyze_v1_17.py` and `scripts/v1_17_lib.py`)

Notation: u = unit (category, brand, model, condition); r = run 1–3; f = frame 1–6; x_{u,r,f} ∈ {0, 1}; p_{u,r} = Σ_f x_{u,r,f} ÷ 6; s²_u = Var_r(p_{u,r}) with n − 1; for a stratum g of n_g units, σ̂²_g = mean_{u∈g} s²_u, σ̂_g = √σ̂²_g.

**E1 (primary). Runs needed, by category size.** For g ∈ {all 672 units; size 16 (96 units, 6 clusters); size 24 (576 units, 24 clusters)}: σ̂²_g; σ̂_g (the standard error of one run); SE_g(R) for R = 1, 2, 3, 5, 7, 10, 24; R*_g(0.10) and R*_g(0.05) with their cluster-bootstrap 95% intervals (and χ² intervals alongside). Every projection beyond R = 3 is printed with the independence assumption.

**E2 (alongside). The same block for:** each condition (S0, S1) and size × condition; each model; each category; each Presence level (zero, low, middle, high, full) overall and by size; "named, not saturated" (1 ≤ K ≤ 17) overall and by size; S-COI overall and by size.

**E3 (alongside). Two other scales.**
- A-frame (per question): s² of x_{u,r,f} over runs for each (u, f), pooled over 4,032 (unit, frame) pairs; overall and by size; same block (the scale of Schulte et al.'s per-prompt figures).
- A-panel (N3 panel mean, the published `pi_N3_<cond>`): P_{b,c,r} = mean over the three models of p_{u,r}; s² over runs for each of 224 (brand, condition) pairs, clusters = category × condition (10); overall and by size (size 16 has 2 clusters: flagged).

**E4 (descriptive). Per-unit standard errors.** Counts of units (of 672) with s_u ÷ √3 below 0.10 and below 0.05, and with s_u below 0.10 and below 0.05; units with zero variance; units per Presence level. Each s_u rests on three runs; these are counts, not projections.

**E5 (descriptive). Once instead of three times** (integer mention counts throughout, so ties are exact).
- *Changing places, per model* (30 answer cells): for each run r, a brand "changes place" if at least one other brand of its category is strictly above it by that run's count and strictly below it by the three-run total (a move between a tie and a strict order is not counted). Reported: brands changing place out of 2,016 brand-runs (672 × 3), and reversed pairs out of all within-cell pairs.
- *Changing places, N3 panel* (10 category × condition cells, 224 brands × 3 runs): the same, on the panel's summed counts.
- *Alongside:* the one run against the total of the other two runs (no shared run), for both.
- *Crossing the published floor (N3):* for S0 and S1 separately, the brands below 6 · π̂ < 1 with three runs (54 answers) and with each single run (18 answers: fewer than 3 mentions); per run, the brands whose status differs, in each direction; their mean over the three runs. In S0 the three-run count is the published 49.
- *Named at all, per unit:* units named in at least one of the 18 answers, and for each run, how many of them that run alone would show as never named.

**E6 (descriptive, separate). Omnibus waves.** Unit = (category, brand, legacy model), w_{u,t} = k ÷ 6 for t1, t2, t3; s²_u over waves; pooled σ̂²_g and its cluster-bootstrap interval (clusters = category × model, 30) for all, size 16, size 24, each Presence level (K over the 18 answers of three waves) and S-COI; and the half mean squared change between waves, mean (w_{t′} − w_t)² ÷ 2, for t1→t2, t2→t3 and t1→t3, overall and by size. No runs projection and no pooling with E1–E5. Read as time drift plus run noise, on the legacy models.

**Seeds.** 117017 (every bootstrap), 117001 and 117002 (dry run only).

---

## §5 Outputs and reporting rule

**Run once.** `python3 osf/methodology/v1_17/scripts/analyze_v1_17.py --run` after the lock is anchored. It refuses unless tag `v1.17-prereg-r1` is on origin and every file in `LOCK_MANIFEST_v1_17.sha256` matches. Outputs:
- `outputs/v1_17_results.json`: the loader check, E1–E6 in full.
- `outputs/RESULTS_NOTE_v1_17.md`, filled from the JSON by `scripts/write_note_v1_17.py` (wording around the numbers may be edited; numbers only from the JSON): a short plain-words note: E1 first (by size, with the independence assumption in the same sentence as every projection), then the Presence-level pattern, then E5, then E6, then what v0.40 should check (§6). Every number with its n.
- One chart per finding, drawn by `scripts/build_charts_v1_17.py` (matplotlib, program chart conventions: bold title top-left, grey subtitle, thin indigo #37237B rule, italic grey source line citing v0.42's tags and `v1.17-prereg-r1`). Chart titles never repeat a finding's title. Planned: (1) standard error against runs by category size, with lines at 0.10 and 0.05 and the projected part drawn differently from the observed part (R ≤ 3); (2) one-run standard deviation by Presence level; (3) brands that change place or cross the floor if measured once; (4) the omnibus waves' wave-to-wave figures beside t4's run-to-run figures, in separate panels, labelled as different quantities on different models.

**Reporting rule.** Exploratory: no verdicts, no "significant". Every projection names its assumption. Primary rows are reported whatever their size; alongside rows are all reported in the JSON, and the note reports those named in §6 plus any alongside row whose point R*(0.10) or R*(0.05) lies outside the 95% cluster-bootstrap interval of the primary row of its size (or of "all" when it spans both sizes). A flagged interval (`few_clusters_flag`) is reported with the flag and the dry run's coverage. Numbers: variances and standard errors to 3 decimals, R* as whole runs, counts with their base. The S-COI rows are reported beside E1 in the note; if any R* differs from the primary, the note says so in the first paragraph.

---

## §6 What v0.40 should check (recommendation only)

v0.40 (current arm on the newest models, search off and on; models and runs per cell set in its own pre-registration; its draft brief gives "for example 3 runs per cell") is a different study with different categories (airlines, banks) and question sets. The recommendation is computed by a fixed rule and never holds v0.40's lock:

1. For v0.40's runs per cell R₄₀ in its current arm: the expected standard error of a brand's per-model Presence, σ̂_all ÷ √R₄₀, with its interval; whether R₄₀ ≥ R*_all(0.10) and ≥ R*_all(0.05). If v0.40's registry brand count per category lies between 16 and 24, the nearer t4 size stratum is reported alongside; otherwise the note says no t4 stratum matches.
2. If v0.40 asks Q recall questions per category instead of 6, an alongside figure σ̂²_frame ÷ Q (E3), which assumes the questions of one run vary independently.
3. v0.40's legacy arm (one call per probe and model): t4 has no legacy runs; the note gives E1 at R = 1 for N3 and E6 for the legacy models, and says neither is a run-to-run estimate for the legacy arm.
4. Phrasing: "v1.17 suggests …"; v0.40's runs per cell are decided in v0.40's pre-registration.

---

## §7 Looks at the data before the lock (declared)

Before this lock the preparer (Claude, Nov 12, 2026) did only the following on real data:
- **Loader check** (`outputs/prelock/loader_check_v1_17.json`): row, unit and cell counts (§2.1, §2.2), category sizes, the six S-COI brands present, the omnibus table's internal check (`pi_hat` = Σk ÷ 36, largest difference 0.0), and one published number reproduced: 49 brands below the recall floor on N3, S0, three runs (v0.42 descriptive 3; reproduced 49).
- While checking file formats: the first rows of `v42_brand_table.csv` (published three-run per-model and N3 Presence of five v0.19 brands), v0.42's published descriptive 1 (run-to-run reliability rel1 per model × condition, 0.845–0.915) and descriptive 3 (floor persistence), and the column total of `mentioned` in `v19_phase_b.csv` (576 of 1,728 rows). No variance, standard error, rank comparison or floor crossing was computed on real data.
- The test suite's real-data tests check the same counts and the same published number only.
Everything else (the estimators, intervals, the once-versus-three comparisons and the omnibus block) was run on synthetic data only (§8).

---

## §8 Dry run on synthetic data with known standard error

`python3 scripts/analyze_v1_17.py --synthetic outputs/dry_run` (seed 117001; outputs `outputs/dry_run/dry_run_v1_17.json`, the two full synthetic outputs `synthetic_results_A.json` and `_B.json`, and, for scenario A, the four charts and the filled note, all marked SYNTHETIC). The omnibus block was run on synthetic omnibus-shaped data (one run per wave, with drift). The generator copies t4's shape (5 categories of 16/24/24/24/24 brands, 3 models, 2 conditions, 3 runs, 6 frames; 25% of brands never named) with a known mention chance for every unit and frame and independent runs, so each unit's true run-to-run variance is Σ_f π_f(1 − π_f) ÷ 36. Scenario A: every answer independent. Scenario B: a shared "short answer" shock within each answer (chance 0.3, halves every brand's chance), so brands named in one answer are dependent, as in real answers.

| Scenario, stratum | true SD of one run | estimated | R*(0.10) true / est. [95% interval] | R*(0.05) true / est. [95% interval] |
|---|---|---|---|---|
| A, all (672) | 0.146 | 0.148 | 3 / 3 [2, 3] | 9 / 9 [8, 10] |
| A, size 16 (96) | 0.137 | 0.139 | 2 / 2 [2, 3] | 8 / 8 [7, 10] |
| A, size 24 (576) | 0.148 | 0.150 | 3 / 3 [2, 3] | 9 / 9 [8, 10] |
| B, all (672) | 0.151 | 0.157 | 3 / 3 [3, 3] | 10 / 10 [9, 12] |
| B, size 16 (96) | 0.141 | 0.157 | 2 / 3 [2, 4] | 8 / 10 [8, 13] |
| B, size 24 (576) | 0.153 | 0.157 | 3 / 3 [3, 3] | 10 / 10 [9, 12] |

Coverage over 300 replicates per scenario (1,000 bootstrap draws each): cluster bootstrap 0.96 (A, all), 0.95 (A, size 24), 0.88 (A, size 16); 0.97, 0.96, 0.84 in B. χ² alongside 0.89–0.90 throughout. Mean relative bias of the pooled variance within ±0.5% in every stratum. The point R* equalled the true R* in 75–93% of replicates for 0.10 and 33–67% for 0.05 (it is often one run off; the interval carries this). Conclusion for the design: the estimator is unbiased; the cluster interval is adequate with 24–30 clusters and too narrow with 6 (hence the flag); the χ² interval is too narrow and stays alongside only.

---

## §9 Deviations

Any change after the lock goes in `DEVIATIONS.md`, dated, before the outputs it affects, with the reason. The stub opens with Entry 0 (conflict-of-interest handling carried from v0.42 and v0.62).

---

## §10 Limitations (stated up front)

- Three runs per unit, collected on one day (Nov 11, 2026) through the providers' APIs: day-to-day variation is not in t4's run-to-run figure, and the projection assumes independent runs with constant variance.
- Category size has two values, and size 16 is one category: size and category cannot be separated.
- Six frames per category: a study with more or other questions has a different per-run variance (E3 gives the per-question scale under an independence assumption).
- Presence levels are grouped on observed values.
- Models: t4 is N3 only; the omnibus waves are the legacy six, one run per wave, so the two blocks differ in models as well as in what they measure.
- Phase A (recognition) has one run on t4; its run-to-run noise is not measured.
- Answers come through APIs, not consumer apps (the SparkToro volunteers used the apps; not compared there either).

---

## §11 Declarations

**Conflict of interest.** The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. This study re-analyses answers collected against brand registries fixed in earlier phases (v0.19–v0.23); it performs no new brand selection and no new collection, and each registry carries its source-phase conflict-of-interest handling forward unchanged. Two items of record apply. In the automotive registry, Samsung subsidiaries hold tier-2/3 component supply relationships with several registry brands — Harman International (audio systems), Samsung SDI (battery cells), and Samsung Display (infotainment) — characterized in the source phase as non-competitive, with no brand-level overlap, and imposing no operational restriction on registry composition (v0.22 Declarations; screened in v0.22 DEVIATIONS Entry 0, Part B). In the audiophile-headphones registry, AKG was substituted with Denon before the v0.19 pre-registration lock because AKG's parent, Harman International, is a Samsung subsidiary. Correction (November 10, 2026): Denon, which replaced AKG in the v0.19 registry, has itself been owned by Harman International, a wholly owned subsidiary of Samsung Electronics, since September 23, 2025, when Harman completed its acquisition of Sound United from Masimo; the v0.19 headphones registry therefore includes one Samsung-group brand. The substitution did not achieve its purpose, and this was not noticed until November 10, 2026. Cheil Worldwide, a marketing company of the Samsung group in which Samsung Electronics holds 28.43%, or its agency Iris has done advertising, public-relations or search-marketing work for five registry brands: Chevrolet (for GM Korea, 2017), BMW (UK consumer public relations, 2018), Bentley (experiential agency of record in the Americas from 2021), Jack Daniel's (UK digital agency from 2022, since replaced) and Eucerin (search marketing for Beiersdorf from 2024). As in v0.62 (the pre-registrant's decision of November 12, 2026), these five brands are kept in every analysis, as Denon is, and the main results are also reported without them and Denon (sensitivity S-COI, 106 brands). Coding and scoring were fully automated against the locked registries, and this pre-registration is locked and deposited before any estimand is computed on real data. Samsung Electronics had no role in the design, conduct, analysis or reporting of this work.

**Funding.** Self-funded.

**Ethics.** Not applicable; no human subjects.

**Use of AI tools.** During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.

---

## §12 Lock procedure and change log

- **r1 draft** prepared Nov 12, 2026 by the runner's lane B (local commit on branch `v1.17`; not pushed).
- Lock: the coordinator checks the numbers, regenerates `LOCK_MANIFEST_v1_17.sha256` (`scripts/make_manifest_v1_17.py`), commits, tags `v1.17-prereg-r1`, pushes the tag and deposits this folder on OSF (`methodology/v1_17/`). Only then may `--run` be used, once.
