# AIAS 3.0 (Coverage) release: what it still needs, dated

Written Thu 2026-11-26 (US Central) on branch `aias-3.0-draft` (pre-build, nothing public). Dates are either fixed by a locked or dated record (cited) or derived from those with the step lengths of earlier releases; a date that depends on a decision not yet taken says so. Forecast on the control panel: AIAS 3.0 ~Fri 2027-01-08.

## What exists today (copied into the drafts as {{L:KEY}} tokens, 77 keys, each with file + commit)

- Coverage Paper A, v1.12: locked `v1.12-prereg-r1` (49efc47), scored once 949be61 (PASS), paper 86b929a (published, 20 pp).
- Coverage Paper B, v1.19: locked `v1.19-prereg-r1` (4bc4ce4), scored once 6e8f157, paper b9e0d20 (published, 16 pp).
- AIAS 2.0 (release precedent and comparison values): outline f97db70, data lock 94f6618, paper r3 a425191.
- Bridge from the AIAS 2.0 panel to the newest models: v0.42 scored 31c64c6; erratum of Nov 25 b3eb526; corrected values v0.45 S-Q 47f1748.
- Predictive validity: v0.43 locked 8c96d9c (§2.6: new components join Stage 2 by dated amendment), Stage 1 scored 3ed9e1d.

## What it still needs

| # | Item | Pre-registered? | Data it needs, and when that data exists | Earliest feasible | Depends on | Needs Pablo |
|---|---|---|---|---|---|---|
| 1 | **Scope decisions** (below, D1-D4) | n/a | none | his next answer | none | **yes** |
| 2 | **Typographic-apostrophe check for v1.12/v1.19.** v1.12 uses v0.42's coder unchanged (P1 pins blob 2d36735), so the miss the Nov 25 t4 erratum fixed also affects Coverage answers and the t4 comparators. Read-only count today (raw file at 86b929a, mentions file): 30 Coverage answers name Paula's Choice and 10 name L'Oréal Paris only with a typographic apostrophe, all coded "not mentioned" (GPT-6 Astra 12 + 4, Gemini 4 Argon 18 + 6). Effect on Cov*, the gate legs and v1.19 not computed. | no (sensitivity of locked studies, as v0.45's S-Q; DEVIATIONS note first) | v1.12 raw answers, v0.42 corrected tables (exist) | about one session after his decision; before the calibration reads v1.12 | none | **yes** (handling, as the Nov 24 t4 options A/B/C; a corrections-log row if a published value changes) |
| 3 | **Release pre-registration** (outline with outcome-contingent headline wording in the AIAS 2.0 form, the calibration and dissociation analyses with scorer and tests, the panel decision, the v0.43 Coverage amendment) | **no, not drafted** | none to write it | sent ~Mon 11/30 if D1-D4 come by Fri 11/27; locks 24 h after he receives it (~Tue 12/1); must lock before the Preview's scoring run (Fri 12/11) to read its Coverage tests blind; a lock in 2026 still deposits to OSF ec6wh | 1 | **yes** (new pre-registration) |
| 4 | **Two -> three-score calibration** (the N -> N+1 step; v1.9 did it for two scores) | no (in 3) | t4 P and C* on N3 (v0.42, exists), Cov* (v1.12, exists), AIAS 2.0 profiles (exist) | the day 3 locks (~12/1); re-analysis, no model call | 2, 3 | inside 3 |
| 5 | **Three-score dissociation** (P, C*, Cov* on the same brands and week) | no (in 3); the Preview (`aias-6-0-preview-prereg-r1`) already locks pairwise and all-earlier-parts tests that include Coverage on t4 | t4 + v1.12 (exist); the Preview's outputs from its data lock **Fri 12/11** (public Tue 12/15) | ~12/1 on t4 alone; **Fri 12/11** if it reads the Preview | 3 (and 6) | inside 3 |
| 6 | AIAS 6.0 Preview scorer outputs | yes (locked Nov 11) | t5 for v1.14 Stage 2 (t5 window opens Thu **12/3**, 72 h) | **Fri 12/11** (data lock), public **Tue 12/15** | t5, v1.14 Stage 2 | no |
| 7 | **Coverage over time** (OPTIONAL retest: v1.12's probes re-asked to N3). Nothing measures Cov* over time today: t5 carries "no Coverage block" (v0.45 §1), v1.19 did not include the re-ask, and t6 (target **2027-02-12**) repeats t4's design. | **no** | a new paid collection; one paid job at a time, never during t5 (12/3-12/6) or the v1.21 judge that follows it; v1.12 recorded $17.08 on four models at November prices (Argon's list price doubled Dec 1, so re-estimate) | collection ~12/8-12/10, scored the next day, if pre-registered (in 3 or separately) by ~12/5 | 3, t5 end, v1.21 judge end | **yes** (spend and scope) |
| 8 | **Predictive-validity update** (Cov* into v0.43 Stage 2 by the §2.6 amendment) | rule locked (v0.43 §2.6); the amendment **not drafted** | search interest to the four weeks ending **2027-03-06**; outcome pulls from **Wed 2027-03-10**, three at least 24 h apart | amendment: any day before 3/10 (with 3); **result not before Fri 2027-03-12** | 3 | **yes**: ship 3.0 with this leg registered and its result pending (then reported in AIAS 4.0/5.0), or hold 3.0 for it (it would then follow AIAS 4.0, ~2/19, against "releases stay in order") |
| 9 | Data lock (`aias-3-0-data-locked`, class computed mechanically from 4, 5 and 7) | in 3 | 4, 5 (+7) | **Sat 12/12** | 4-7 | no |
| 10 | Charts, paper (fill `--mode final`), report (after the paper; fork `build_report_aias6_preview.py`), page-by-page pre-flight | n/a | 9 | ~12/16-12/18 (v0.40's launch Mon 12/14 and the Preview Tue 12/15 come first) | 9 | cover: full-size "Curved slats" file; report code |
| 11 | Fable review of the full draft (milestone rule) | n/a | 10 | ~12/18-12/21 | 10 | no |
| 12 | Ship: OSF deposit, website (content/pending/aias-3-0.json wired in, Methodology/Home keep-up lines, Claims Register), GitHub | n/a | 11 | **Tue 12/22** | 11 | no (automatic), unless it slips into January: then data, paper and report go to Zenodo (deposit rule of Nov 25), which needs his Zenodo token and the December test deposit |
| - | Not required for the release (Pablo's call whether they belong in it): #32b parallel situation set with buyer weights, #33 question wording (each a paid collection and its own pre-registration); the identity-load question (v1.19: 26 eligible brands against a floor of 45) | no | new collections | after 3.0 unless he says otherwise | - | yes, if he wants them inside 3.0 |

## Decisions for Pablo (nothing below is done)

- **D1 Panel and score set.** Coverage exists only on the newest-models panel (N3). The legacy six-model panel that carries AIAS 2.0's published scores is retiring (Claude Opus 4.5 from Nov 24, Sonnet 4.5 Nov 30), so a three-score calibration on the AIAS 2.0 panel is not possible. The release would move the published score set to N3, with AIAS 2.0's scores bridged through v0.42 (Presence order held, 0.828; Consistency order held only partly, 0.310; corrected 0.827 and 0.304). AIAS 2.0's outline (D9) said Consistency must be recalibrated on the new reference panel before any post-legacy comparison, and the roadmap lists the new reference panel as his decision.
- **D2 Coverage retest (item 7):** yes/no, and if yes the panel (N3 only, or with Opus 5.5 as in v1.12) and the cap.
- **D3 Predictive leg (item 8):** registered-and-pending in 3.0, or wait to March.
- **D4 Apostrophe check (item 2):** handling, as for t4.
- Also his: report code, cover file, working titles (paper "Presence, Consistency and Coverage"; report "Named in Which Situations").

## Earliest realistic release

**Tue 2026-12-22** for the release as planned (calibration, dissociation with the Preview's locked Coverage tests, Coverage retest only if he approves it in time, predictive leg registered with its result due after 2027-03-12), about two and a half weeks before the ~1/8 forecast. Reasoning: every input of the calibration exists now; the last input with a fixed date is the Preview's outputs (Fri 12/11); the Preview's plan allows four days from its data lock (Fri 12/11) to publication (Tue 12/15) with its pipeline already built; this plan allows ten (12/12 to 12/22) for charts, paper, report and the Fable review, because v0.40 (12/14) and the Preview (12/15) come first. Conditions: D1-D4 answered by about Fri 11/27-Mon 11/30 so the pre-registration locks by ~12/1-12/5; the apostrophe check done before the calibration; no slip of the Preview's data lock. If the release slips past Dec 31, its deposit needs the Zenodo path. Jan 8 stays the safe date; holding for the predictive result would put AIAS 3.0 after mid-March 2027.

## Placeholders (every {{P:KEY}} and the input that fills it)

`python3 papers/aias_3_0/tokens_aias3.py` prints the table (39 keys, 9 future inputs); `--inputs` prints the inputs with their dates. A final build (`build_aias3.py --mode final`) refuses any key without a value and any token left in its output; `tests/test_tokens_aias3.py` checks both.
