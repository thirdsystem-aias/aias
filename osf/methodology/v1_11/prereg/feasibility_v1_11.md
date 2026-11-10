# v1.11 feasibility count (parsing only, development sample)

r0, Nov 10, 2026. Script: `osf/methodology/v1_11/scoping/feasibility_v1_11.py` (output `feasibility_v1_11.json` beside it), using the unit code of `scripts/score_v1_11.py`. Re-run on Nov 10 with the r1 scorer (brand matches located on the whole answer, PRE_REGISTRATION §4.1): the output file is byte-identical. The planning rates below served draft r0's cost estimate only; r1's §7 uses the exact counts of the unit build U0 on the frozen inputs.

**Declaration.** Parsing only, on a development sample that every v1.11 confirmatory analysis excludes. No model call, no valence, and nothing computed on Presence, Consistency, Ranking, separability or stability. No confirmatory input (v0.23 recognition, omnibus frames, early category sets) was parsed; the manifest builder read their bytes for hashes and their CSV headers only.

| Dev set | Answers | Registry brands | Answers naming ≥ 1 | Windows | Windows / answer (mean, median) | Window chars (median, p90) | ≈ tokens / window | At 1,500 cap | Bare windows |
|---|---|---|---|---|---|---|---|---|---|
| D2 v0.17 Phase B frames (legacy six) | 18 | 16 | 18 | 111 | 6.17, 6 | 190, 554 | 68 | 0 | 10 (9%) |
| D3 v0.18 Phase B frames (legacy six) | 18 | 24 | 15 | 72 | 4.00, 4 | 158.5, 359 | 50 | 0 | 2 (3%) |
| D4 v0.5 archive, early design (3 providers) | 67 | 14 (from `brands_found`) | 67 | 374 | 5.58, 5 | 271, 671 | 84 | 1 | 7 (2%) |
| D1 v0.17 Phase A recognition-type | 24 | — | — | whole answers | — | median 905, max 2,707 characters | ≈ 296 / answer | 0 over 16,000 | — |

"Bare" = the brand's segments carry fewer than 4 words besides the brand name (list-only mentions; expected to judge neutral).

**What changed because of this count (before the lock, declared).** The first window rule (only segments that name the brand) failed on list formats: D4 stores newlines as double spaces and puts the descriptors in sub-bullets under a heading that names the brand (`### Best overall: **ClickUp** - Very flexible - …`). The locked rule (PRE_REGISTRATION §4.1) splits on newlines or 2+ spaces and on inline headings, bullets and numbered items, and carries up to 4 continuation segments after each naming segment, stopping at a heading or a segment naming another registry brand. With it, the median window is 159–271 characters and only 1 of 557 windows reaches the cap.

**Planning rates used in §7.** Frames 6.2 windows per answer (the higher frame rate, conservative); early design 5.6 per answer; ≈ 1,000 input tokens per window call (762-token fixed prompt by the 4-characters-per-token estimate, plus question, category and window); recognition ≈ 2,100 input tokens per call, from the inventory's v0.23 median of 4,765 characters (the development recognition answers are shorter, median 905, and are not used for this rate).

**Limits.** 127 answers; the legacy-panel frames and a pre-protocol early run stand in for the confirmatory sets; registry matching in D4 uses the run's own `brands_found` names, not a registry with aliases. Exact unit counts are fixed at lock step U0 on the frozen inputs (deterministic, no calls).
