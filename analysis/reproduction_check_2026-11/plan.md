# Reproduction check from the public files, November 2026

AIAS™ measurement program · Third System™ · OSF project ec6wh · November 13, 2026 · plan deposited before the check is run

Pablo Ulpiano González Castro
School of Visual Arts, MPS Branding Program, New York, NY (primary academic affiliation)
Third System (research entity; data archive and methodology venue)
Correspondence: pablou@pablou.com · pablou.com
ORCID: 0009-0003-8968-9990 (linked: https://orcid.org/0009-0003-8968-9990)

**What this is.** A test of whether a published result can be recomputed from the files deposited on OSF alone. It is a reproduction from the public files by the program itself, not an independent replication: no new data are collected, and the same program runs the check.

**Study.** AIAS 2.0, "Presence and Consistency: A Two-Component Measurement of AI Availability" (paper r2, `aias_2_0/paper/aias_2_0_synthesis_paper.pdf`, SHA-256 `17490189…527e7e`). It is the program's headline result, and its numbers come from a deterministic chain: the per-answer files of three waves (May, June and November 2026; five categories, 112 brands, six models) are scored by `aias_2_0_synthesis_data.py` with the v1.9 and v0.41 scorers, which give each brand a Presence score P and a Consistency score C*.

**Inputs.** The 64 files listed in `inputs.md` (OSF path, size, SHA-256, link); each file already on OSF was downloaded without a login and matched its SHA-256 on November 13. Four were not on OSF when the chain was traced: the brand-mention matchers for skincare, cosmetics and automotive answers (`score_v20.py`, `score_v21.py`, `score_v22.py`) and the automotive acquisition script, whose checksum one of the scorer's integrity gates verifies (`run_acquisition_v22.py`; it is not run). They are deposited with this plan in `inputs/`, byte-identical to the repository files last changed in May 2026. Four locked records among the inputs hold values the builder checks its own output against (the May per-brand dispersion and the summary correlations of all three waves). The results file and the paper are not given to the reproducer.

**Numbers to reproduce.** `expected_values.csv`, 1,063 values. 1,008 are per-brand values (P, C* or "not rated", and total mentions; 112 brands in each of three waves) from the results file the paper reports from, `aias_2_0/aias_2_0_profiles.csv`, because the paper shows per-brand values only in a chart (Figure 3). 55 are counts and statistics printed in the paper, for example `ps-rhoCP-t3`, the November correlation of C* with P, 0.189 (n = 54, printed p. 9).

**Tolerance.** Counts exact. Scores equal to the published value at the digits reported: six decimals for per-brand P and C* (as the results file prints them), three for correlations, whole percentages for shares. A brand published as not rated must come out not rated.

**What counts as a pass.** PASS if all 1,063 values match. Otherwise FAIL, with each difference listed and explained. The result is published beside this plan either way.

**Procedure.** A fresh agent (Claude, in Anthropic's cloud session) that has not worked on AIAS 2.0 gets only the links in `inputs.md` and the list of quantities to compute, without their values: no program notes, git repository, access to the author's computer or model API. It may install public packages. It reports every number it computes and every file it used. The program's coordinating agent compares the numbers with `expected_values.csv` and publishes the comparison here. Not redone: the model calls and the coding done at collection (spirits recognition was coded by a model); the check starts from the per-answer files as deposited.

**Stated in advance.** (1) Three pairs of C* values are equal in exact arithmetic but differ in the last bits of floating point (May: Augustinus Bader and CeraVe, Fenty Beauty and Huda Beauty; June: Focal and Audio-Technica). The published correlations rank each pair as distinct, as the deposited code does; ranking them as ties gives 0.072, 0.740 and 0.648 instead of the published 0.073, 0.736 and 0.647. (2) Some Gemini 2.5 Flash answers were cut off before naming a brand in headphones (v0.19) and partly in spirits (v0.23). This is under review; it bears on validity, not on computational reproducibility.

**Use of AI tools.** During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.
