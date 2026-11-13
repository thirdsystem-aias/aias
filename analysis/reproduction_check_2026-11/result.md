# Reproduction check from the public files, November 2026: result

AIAS™ measurement program · Third System™ · OSF project ec6wh · November 13, 2026 · the plan (`plan.md`, `inputs.md`, `expected_values.csv`, `inputs/`) was deposited in this folder at 18:50 UTC, before the run

Pablo Ulpiano González Castro
School of Visual Arts, MPS Branding Program, New York, NY (primary academic affiliation)
Third System (research entity; data archive and methodology venue)
Correspondence: pablou@pablou.com · pablou.com
ORCID: 0009-0003-8968-9990 (linked: https://orcid.org/0009-0003-8968-9990)

**Result: PASS.** All 1,063 published values named in the plan came out the same when AIAS 2.0 was recomputed from the public files: the 1,008 per-brand values (Presence P, Consistency C* or "not rated", and total mentions; 112 brands in each of three waves) and the 55 counts and statistics printed in the paper, each at the digits the paper or the results file reports. The results file the builder wrote, `aias_2_0_profiles.csv`, is byte-identical to the published one (SHA-256 `022ef56ecad9ddb60ad9ce0a2129698fd84ee9656630500e30b05f1e4b7e8c6e`).

**How it was run.** A fresh Claude agent in Anthropic's cloud session, which had not worked on AIAS 2.0, got only the 64 links in `inputs.md` and the list of quantities, without their values. It ran on November 13, 2026, 18:52 to 19:08 UTC, with Python 3.13.18, numpy 2.5.3 and scipy 1.18.1, made no model or API calls, and changed no code. Its results and its log are in `reproducer/`. The program's coordinating agent then compared its numbers with `expected_values.csv`: `comparison.csv` has one row per value (published, reproduced, reproduced at the published digits, match). This is a reproduction from the public files by the program itself, not an independent replication.

**What it took.**
1. Four files the scorers need were not on OSF before this check: the brand-mention matchers for skincare, cosmetics and automotive answers, and one acquisition script that an integrity gate checksums but does not run. They were deposited with the plan, before the run. Without them the result could not have been recomputed from OSF alone.
2. The builder's last stage proves that the pre-registrations were locked before the November data, by checking their git tags against the code host, or against OSF anchor files together with a local git tag. Without the git repository that check cannot run, so the November values were computed with the builder's documented test option `--skip-origin`, which then only checks that the two verdict files exist. The May and June values are identical with and without the option. The lock record itself (tags and OSF anchors) was not part of this check.

**Differences.** None among the 1,063 published values. The builder's summary file, `aias_2_0_synthesis_data.json`, differs from the published one in 26 places, none of them a published number: the build time; the folder paths of the inputs (their SHA-256 values are the same); the stage-2 record (published: both tags anchored at origin; here: skipped, test mode); and 18 per-category means that differ in the last digits of floating point (largest difference 1.4 × 10⁻¹⁴, for example 88.72561615590907 published and 88.72561615590908 here). All 26 are listed in `json_differences.txt`.

**Stated in advance, and what happened.** (1) Three pairs of C* values that are equal in exact arithmetic were ranked as the deposited code ranks them; the reproduced correlations 0.07293925573105668, 0.7357486264955685 and 0.6473238536507431 give the published 0.073, 0.736 and 0.647. (2) The Gemini 2.5 Flash answers cut off before naming a brand, under review, bear on validity and were not part of this check.

**What this does not show.** That the data measure what they are meant to, or that another team writing its own code would reach the same numbers. It shows that the published numbers follow from the public answers and the public code.

**Files in this folder.** Before the run: `plan.md`, `inputs.md`, `expected_values.csv`, `inputs/`. After the run: `result.md` (this page), `comparison.csv` (made by `compare.py`), `json_differences.txt`, and `reproducer/` (`results.csv`, `log.md`). The builder's two output files are not deposited again: its `aias_2_0_profiles.csv` is byte-identical to the published file, and its `aias_2_0_synthesis_data.json` equals the published file except for the 26 differences listed.

**Use of AI tools.** During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.
