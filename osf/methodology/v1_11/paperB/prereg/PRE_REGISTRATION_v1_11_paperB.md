# AIAS v1.11 — Sentiment, Paper B: human-label validation of the AI sentiment judge

AIAS™ Measurement Program — Third System™. **Status: r1, lock-ready, not locked (2026-11-11).** Branch `v1.11-paperB` (from `v1.11` @ `95c3fa1`). Conformed from DRAFT r1 (2026-11-10, `_runner_tmp/sva_labels/PREREG_PaperB_human_labels_DRAFT_r1.md`) to the author's decision of 2026-11-10, 5:12 pm (variant b: the 48 long brand-description answers are not labelled). Lock target: tag `v1.11-paperB-prereg-r1`, pushed, with `../anchor/git_anchor_v1_11_paperB.json` and the OSF deposit, **before the first invitation (Fri 2026-11-13)**; the steps are in `../LOCK_STEPS.md`. The lock waits for the author's "guide final".

| Field | Value |
|---|---|
| Study | Sentiment Paper B, human-label arm: students of the SVA MPS Branding program label the tone of AI answers toward a named brand; their labels are compared with the v1.11 AI judge |
| Parent | v1.11 Sentiment Paper A: tag `v1.11-prereg-r1` → commit `62e2d38`, anchor commit `97c26be`, branch `v1.11`; PRE_REGISTRATION_v1_11.md §9 (hand-off), §4.2–4.3 (judge, prompt, scale); DEVIATIONS Entries 1 (commit `95c3fa1`) and 2 (this branch) |
| Sample | `paperB/human_sample_v1_11_paperB_r1.csv` (566 units, SHA-256 `94d120f4a752d72f4fe96f90523fb3be663b3feba92fc3ff0dcdd2a11da0295e`): the v1.11 §9 draw (`human_sample_v1_11.csv`, SHA-256 `b80bd109…`, seed 111022) with its 2 Denon units replaced (v1.11 DEVIATIONS Entry 1, seed 111025). **Labelled: its 518 mention windows** (blocks F and E); the 48 recognition answers (block R) are not labelled (DEVIATIONS Entry 2) |
| Labellers | Volunteers from the SVA MPS Branding Class of 2027 (19 students); voluntary, not graded |
| Approval | Emily Weiland, chair of the program, approved on 2026-11-10 on condition that students are told clearly how their labels are used (statement in §3, word for word) |
| Timeline | Invitations Fri 2026-11-13; sign-up closes Fri 11-20; personal forms out Mon 11-23; labels due Fri 12-04; withdrawal possible until Fri 12-18; day-1 discussion 2027-04-21 |
| Lock | Before the first invitation (2026-11-13), so that the guide, the statement, the packets rule and the thresholds are fixed before any student is contacted; in any case before any label is read and before the v1.11 judge run starts (first allowed submission 2026-11-22 06:00 UTC) |

## 1. Question

Does the v1.11 AI judge (J1, Claude Opus 5.5, `claude-opus-5-5`, low effort, Message Batches API; `judge_prompt_v1_11.md`) rate the tone of AI answers toward a named brand the way people do? v1.11 Sentiment is labelled "provisional" until this paper confirms it (v1.11 §0, LABEL).

## 2. Hypotheses and decision rules (fixed here, before any label is read)

**Scale and scores.** Valence v ∈ {−2, −1, 0, +1, +2}, the judge's scale; unit score u = 25 × (v + 2), as in v1.11 §4.3. A student's tone answer "+2 · Strongly favorable" … "−2 · Strongly unfavorable" is v = +2 … −2; "Not about this brand" is `refers_to_brand` = false and carries no valence. A J1 output with `refers_to_brand` = false likewise carries no valence in V0–V2 (its scored valence of 0 under rule 7 is not used), so that the two sides are treated alike; agreement on `refers_to_brand` itself is reported (§11).

**Statistics.** Krippendorff's α, ordinal metric unless stated, computed on all pairable values (units with at least two valences); students are coders in a sparse design. 95% intervals: percentile bootstrap over units (all labels of a resampled unit move together), 2,000 resamples, seed 111024. The α implementation is written and tested on synthetic data and on a published worked example before the label file is read; it is deposited with the analysis.

- **V0 — the human labels are reliable enough to validate against (gate).** α_HH = α among students over the labelled units. **Pass:** α_HH ≥ 0.667. If α_HH < 0.667, V1–V3 are reported descriptively and Paper B's verdict is **INCONCLUSIVE** (a failure of the human benchmark, not of the judge). If fewer than 200 units carry two student valences after §10, V0 is not evaluable and the verdict is **INCONCLUSIVE**.
- **V1 — primary: the judge agrees with the students about as well as the students agree with each other.** α_JH = α on the pairs (J1 valence, one student's valence), one pair per student label with both valences present. Δ = α_JH − α_HH, both on the units that enter α_HH. **CONFIRMED** if α_JH ≥ 0.667 **and** the lower 95% bound of Δ ≥ −0.10 (non-inferiority margin). **MARGINAL** if exactly one holds. **FAILED** if neither holds. The 0.667 bound is the one v1.11 uses for its two-judge gate H1.
- **V2 — no systematic bias.** B = mean over units of (u_J1 − ū_human), ū_human = mean of the unit's student scores. **No bias** if the 95% interval of B lies within ±5 points. Reported overall (decision) and by category (descriptive).
- **V3 — secondary: the evaluative flag.** α (nominal) between J1's `evaluative` and the student's question-3 answer (any answer other than "No judgment" = evaluative), pairs as in V1. Threshold 0.667, reported as met or not met; it does not change the V1 verdict.

**Consequence for v1.11.** Only V1 CONFIRMED with V0 passed confirms v1.11 Sentiment, and only for mention windows (blocks F and E): the scores built on F and E windows lose the "provisional" label. MARGINAL, FAILED or INCONCLUSIVE leaves v1.11 Sentiment "provisional", with the reason stated. **The recognition check stays provisional in every case:** block R (the 48 v0.23 recognition answers) is not labelled, so S_rec and the v1.11 checks that use it (H8's floor-free separability check, the convergence check) get no human check from this paper.

**Predictions.** None recorded.

## 3. Labellers, consent and the statement students receive

Voluntary, unpaid, not graded; students who do not take part join the day-1 discussion the same way. Signing up is the consent: the sign-up form carries the statement below and a required tick box ("I've read this and agree to take part"); the form responses are the record. An optional second tick box asks to be thanked by name. The statement appears word for word in the invitation email, at the top of the sign-up form (`forms/Code.gs`, `buildSignupForm`), in each labelling form, and here. Source: the exercise doc (https://claude.ai/artifact/QHkHLwkqZHAaHs7pTrFTH2, section "How your labels will be used (statement for students)"), saved as `statement/statement_exercise_doc.md` (provenance in `statement/statement_source.json`); `lock/paperB_lock_v1_11.py --check` verifies that this section, the file and `Code.gs` carry the same words, and that the statement agrees with guide page 1 on the number of answers, the time, the due date and the withdrawal date.

<!-- BEGIN STATEMENT -->
> **What this is.** An optional exercise for the Class of 2027, before our course starts. It is not graded and has no effect on your course or standing. If you skip it, you still join the discussion on April 21.
>
> **What you do.** You watch a 10-minute video, then read about 50 short AI answers about brands. For each one, you mark the tone toward one named brand in a Google Form. It takes about an hour, on your own time, by January 22.
>
> **What your labels are for.** They are part of my independent research program, Third System. The research checks whether an AI can judge the tone toward a brand the way people do. Your labels are the human benchmark.
>
> **Who sees them.** I see your responses. Before any analysis, your name is replaced with a code (for example R07), and only I keep the key. I use AI tools (Claude) to help with the analysis, using the coded data only.
>
> **What gets published.** The coded labels, with no names or emails, go into a public research archive (OSF). Summary results appear in a research paper and on thirdsystem.ai, and may appear in Third System reports and talks. You are never named, unless you tick the box asking to be thanked by name in the paper's acknowledgments.
>
> **Your choice.** Taking part is voluntary. You can stop at any time. You can withdraw your labels until February 1 by emailing me at pablou@pablou.com, with no questions asked. After that date, the coded data may already be published.
>
> **Questions.** Email me, or ask Emily Weiland in the program office.
<!-- END STATEMENT -->

## 4. What students label

The 518 mention windows of the Paper B sample (header). Every unit is a judged unit of the frozen v1.11 unit table; J1 judges every one (v1.11 §9; the two Entry 1 replacements are F units, which v1.11 never reduces).

| Block | What it is | Categories | Units |
|---|---|---|---|
| F | mention windows, omnibus panel, waves t1/t2/t3 | audiophile headphones 38, automotive, cosmetics, premium spirits, skincare (40 each) | 198 |
| E | mention windows, eight early categories | household goods retail, personal finance apps, premium facial skincare, premium kitchen knives, premium olive oil, premium tea, project management software, running shoes (40 each) | 320 |

Windows (518): median 33 words; longest 254; 1 over 250 words, 50 over 100 (whitespace split over the sample file, runner, 2026-11-10). Eleven answering models; 37 bare windows.

**What a student sees per unit:** the judge's own input fields, in the judge's order and wording: TARGET BRAND, CATEGORY, QUESTION THE ASSISTANT WAS ANSWERING, TEXT TYPE, TEXT (verbatim). **Never shown:** unit_id, answering model, wave, study, block, frame label, any judge output or AIAS score. Students see a random five-character item code.

## 5. The guide and the label fields

**The guide is locked word for word.** Two pages (https://claude.ai/artifact/4sCt6DcfA4RD6h4TdvUdZZ, version `1794364205-6bca`, read 2026-11-11). Both pages are saved byte for byte in `guide/source/` (`Main.dc.html` SHA-256 `fc577e17cc7664dad1e6d85fe6c6b00e5e9762f62c56ae98d3cdd62dee4c1744`; `Rules.dc.html` SHA-256 `5179a1d13619c9898ba5be3f33fc6efc3de31d96790800d9fc6ea093b08e2ffb`); their text is in `guide/STUDENT_GUIDE_v1_11_paperB.md` and in Appendix A. A guide that differs from these files is not the pre-registered guide.

**v1.11 §9 is met.** §9 requires "the judge's instructions and scale verbatim (`judge_prompt_v1_11.md`, rules 1–7)". Page 2 carries them: a line-by-line exact comparison of the judge prompt (from "Rules:" to the last scale line) with page 2 finds 14 of 14 lines identical — the "Rules:" heading, rules 1–7, the "Valence scale:" heading and the five scale lines — and no difference (`guide/guide_vs_judge_v1_11_paperB.json`). No deviation is recorded for the guide. Around the judge's text the guide adds page 1 (the four questions, invented examples about a fictional brand, the timeline, how labels are used) and, on page 2, six "Rules for hard cases" and a note on how the form's answers map to the judge's fields.

**Form questions** (`forms/Code.gs`; wording = guide page 1, checked by `--check`): 1. "What's the tone toward the brand?" (+2 · Strongly favorable, +1 · Favorable, 0 · Neutral or balanced, −1 · Unfavorable, −2 · Strongly unfavorable, Not about this brand) → `valence`, `refers_to_brand`; 2. "Praise and criticism?" (Yes, No) → `mixed`; 3. "Where does the judgment come from?" (No judgment, The AI's own voice, Quoted sources, Both) → `evaluative` (any answer but "No judgment"; the split between own voice and quoted sources is exploratory, the judge does not record it); 4. "How sure?" (Sure, Not sure) → exploratory; a one-line optional comment. Questions 1–4 are required. Answers that break the judge's consistency rules (for example "No judgment" with a non-zero tone) are kept as given, counted and reported; valence is the primary variable.

## 6. Packets and overlap (rule fixed in `packets/make_packets_v1_11_paperB.py`, seed 111023)

- **Load cap:** at most 60 items per student.
- **Full double coding when 60 × N ≥ 2 × 518** (N ≥ 18). Otherwise every unit gets one label and a seeded, category-stratified subset of 60N − 518 units gets a second; below 200 double-coded units (N ≤ 11) the script stops and the author decides.
- **Assignment:** units in a seeded order; each unit goes to the pair of students that keeps packets most even (fewest items overall, then the pair that has shared the fewest units, then a seeded tie-break). Each packet is shuffled into its own seeded order.
- **At N = 19** (`packets/packet_design_N19_b.json`; rebuilt byte-identical by `--check`): 518 units × 2 = 1,036 labels; 10 students × 55 items + 9 × 54; every unit with two different students; all 171 student pairs share units (2 pairs share 2, 162 share 3, 7 share 4).
- Packets are regenerated with the real N, the same seed and variant b after sign-up closes (Fri 11-20); codes R01…RN are assigned by the author; the runner never sees names. Each student's form states the number of items.

## 7. No third label

v1.11 §9 planned a third student on valence disagreement. This study has none (DEVIATIONS Entry 2): the students consent to one packet, and V0–V3 never used a third label. Units whose two valences differ in sign or by 2 or more points are listed and counted (descriptive, and for the day-1 discussion).

## 8. Procedure

1. The author records the 10-minute intro once.
2. Invitations Fri 11-13 with the statement; sign-up form open until Fri 11-20.
3. The author assigns codes and gives the runner N only; the runner re-runs `make_packets_v1_11_paperB.py --n N --variant b`; the author imports `packets_all.csv` into one Google Sheet and runs the Apps Script (one form per student, a tracker).
4. Personal forms out Mon 11-23; reminders to non-submitters; due Fri 12-04; then `closeLabelForms()`.
5. Students work alone, blind to other students' labels, the judge, the answering model, wave and any AIAS score.
6. J1 outputs for these units come from the v1.11 run (no earlier than 2026-11-22) and are set aside: no one compares them with any student label before the label file is frozen (§9) and §10's exclusions are applied.

## 9. Data handling, missing data and withdrawal

- Names and emails exist only in the sign-up responses and the author's name-to-code key; labelling forms collect no email; every file the runner reads carries codes only.
- **Withdrawal** until Fri 2026-12-18 by email to the author. A withdrawn student's labels are deleted before any analysis. After 12-18 the author exports the `labels` tab once (`collectLabels()`), removes withdrawn students, and records the file's SHA-256 (**label file frozen**); analysis starts only then. Nothing is deposited on OSF before 12-18 has passed.
- **Missing data.** All four questions are required and a form is sent only on Submit, so a submitted packet is complete. A student who submits nothing, or withdraws, contributes no label; the units of that packet keep their other label. Units left with one student valence enter α_JH and B but not α_HH or Δ; their number is reported. No imputation.
- OSF deposit after scoring: coded labels, item key, packets, scripts, guide, this pre-registration, with SHA-256. Free-text comments are deposited only after the author removes anything identifying.

## 10. Exclusions (fixed before any label is read)

- **Student level:** (a) nothing submitted by the cut-off: the end of Fri 2026-12-04, New York time, or a later cut-off announced to every student before 12-04 (recorded); (b) withdrawal; (c) straight-lining: the same tone answer on ≥ 95% of the student's items. A student's first submitted response counts.
- **Unit level:** units that both students mark "Not about this brand" leave V0–V2 and are counted; units J1 failed (JUDGE_FAIL or UNJUDGED) leave V1–V3 and are counted.
- No other exclusion; none based on agreement with other students or with the judge.

## 11. Further analyses (no verdict changes)

- **Secondary:** V1–V3 for J2 (GPT-6.1 Sol) on the units J2 judged; α_HH and α_JH by category and by block (F, E); interval-metric α next to ordinal; nominal α on `refers_to_brand` (students vs J1) and on `mixed` (question 2 vs J1).
- **Sensitivity:** every statistic without the 3 units whose text names a brand listed in the conflict-of-interest section (Declarations).
- **Exploratory:** sources of judgments (question 3); agreement on items both students marked "Sure"; comments; units where students split, for the day-1 discussion.

## 12. Differences from the plan documents

| Source says | This pre-registration | Why |
|---|---|---|
| v1.11 §9: the 566-unit draw (`b80bd109…`) | the same draw with 2 Denon units replaced (`94d120f4…`) | v1.11 DEVIATIONS Entry 1 |
| v1.11 §9: at most 3 units per brand per category | Sony and Beyerdynamic have 4 in audiophile headphones | Entry 1 (least relaxation of the cap) |
| v1.11 §9: 48 v0.23 recognition answers labelled | not labelled; 518 mention windows | author's decision 2026-11-10; DEVIATIONS Entry 2 |
| v1.11 §9: a third student on valence disagreement | none | DEVIATIONS Entry 2 |
| v1.11 §9: labels due about Jan 22, 2027 | due Dec 4, 2026 | timeline set by the author; DEVIATIONS Entry 2 |
| v1.11 §9: judge's instructions and scale verbatim | met: guide page 2, 14 of 14 lines identical | §5 (no deviation) |
| DRAFT r1: variants (a) and (b) | variant b | author's decision |

## 13. Settled in drafting (runner, 2026-11-11; DRAFT r1's open items)

1. Variant b (author, 2026-11-10, 5:12 pm). 2. The guide is the two-page guide, locked word for word (§5) when the author says it is final. 3. The cap relaxation of Entry 1 stands (already recorded in v1.11). 4. The 3 units whose text names AKG or JBL stay (author); the sensitivity of §11 is kept. 5. Lock before the first invitation. 6. No third-label round (§7). 7. Cut-off as in §10 (a). 8. Thresholds (α 0.667, margin 0.10, ±5 points, 95% straight-lining) and seeds 111023 (packets) and 111024 (bootstrap) as in DRAFT r1. 9. A J1 output with `refers_to_brand` false carries no valence in V0–V2, as a student's "Not about this brand" (§2). 10. V0 not evaluable below 200 units with two student valences (§2). 11. Study version v1.11 Paper B, tag `v1.11-paperB-prereg-r1`, OSF `methodology/v1_11/paperB/`.

## 14. Declarations

### Conflict of interest {-}

The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. This study has students label archived answers drawn from the v1.11 unit table, whose brand registries were fixed in earlier phases; it performs no new brand selection, and each registry carries its source-phase conflict-of-interest handling forward (v1.11 DEVIATIONS Entry 0). Two items of record apply to the registries in the labelled sample. (Wording copied from the latest locked pre-registration, `osf/v63/prereg/PRE_REGISTRATION_v0_63.md`, Declarations, lines 182–190, tag `v0.63-prereg-r1`. The two quoted records, the Denon/Harman correction with its source, and the closing sentence are verbatim; adapted to this study's design: the description of the study in this paragraph, the last sentence of the v0.19 item, the last sentence of the v0.22 item, and the sentence before the closing sentence.)

*Audiophile headphones (v0.19).* The v0.19 record states: “The panel substitution of AKG → Denon documented in §5 was made out of an abundance of caution given that Samsung's subsidiary Harman International owns AKG; the substitution occurred prior to pre-registration lock.” (v0.19 paper, Declaration of interest; see also v0.19 pre-registration §2.3 and v0.19 DEVIATIONS Entry 1.) Correction (November 10, 2026): Denon, which replaced AKG in the v0.19 registry, has itself been owned by Harman International, a wholly owned subsidiary of Samsung Electronics, since September 23, 2025, when Harman completed its acquisition of Sound United from Masimo; the v0.19 headphones registry therefore includes one Samsung-group brand. The substitution did not achieve its purpose, and this was not noticed until November 10, 2026. Source: HARMAN, “HARMAN Completes Sound United Acquisition to Expand Premium Audio Leadership”, press release, Business Wire, September 23, 2025. In this study no unit has Denon, or any other Samsung-group brand, as its target brand: the 2 Denon units of v1.11's Paper B draw were replaced by a fixed rule before any label or judge output existed (v1.11 DEVIATIONS Entry 1, which lists the screen terms and the membership sources), and a screen of the 518 labelled units' target brands on November 11, 2026, with the terms of Entry 1, found none (`lock/paperB_lock_v1_11.py --check`). Three labelled units whose target brand is not a Samsung-group brand name one in their text (AKG in two, JBL in one); they stay in the sample (author's decision), and every statistic is also reported without them (§11).

*Automotive (v0.22).* The v0.22 record states: “Samsung subsidiaries hold tier-2/3 component supply relationships with several brands in the v0.22 registry: Harman International (audio systems) supplies Mercedes-Benz, BMW, and other premium automotive OEMs; Samsung SDI (battery cells) supplies BMW (i-series), Volkswagen Group brands including Bentley and Porsche (Stellantis-adjacent platforms), and others; Samsung Display (infotainment) supplies Mercedes-Benz and BMW. Tesla and Polestar also have tangential Samsung-component exposure at the parts level. These are non-competitive supply relationships; Samsung Electronics America does not produce or market passenger car brands and has no brand-level competitive overlap with any v0.22 registry entry. The COI was screened and documented in DEVIATIONS Entry 0 (Part B) of the pre-registration module; no operational restriction on registry composition was imposed.” (v0.22 paper, Conflict of interest.) These are supply relationships, not ownership; no v0.22 unit is removed for them in this study.

Students label blind to the judge's outputs, and the judge's outputs come from the locked v1.11 run. Samsung Electronics had no role in the design, conduct, analysis or reporting of this work.

### Funding {-}

Self-funded. No external funding supported this research. Students are not paid.

### Ethics {-}

Human labels are provided by students of the SVA MPS Branding program, Class of 2027, before the author's course begins. Taking part is voluntary, unpaid and not graded, and has no effect on a student's course or standing; students who do not take part join the day-1 discussion (April 21, 2027) the same way. Emily Weiland, chair of the program, approved the exercise on November 10, 2026 on the condition that students are told clearly how their labels are used. The plain-language statement of §3 is how that condition is met: it goes word for word into the invitation and the sign-up form, and each student consents by ticking a box on the sign-up form, whose responses are the record. Labels are used as the statement says: names are replaced by codes before any analysis and only the author keeps the key; AI tools (Claude) help analyse the coded data only; the coded labels, with no names or emails, are deposited on OSF; summary results appear in a research paper and on thirdsystem.ai and may appear in Third System reports and talks; a student is named only on request, in the acknowledgments. A student can stop at any time and can withdraw their labels until December 18, 2026 by email to the author; withdrawn labels are deleted before analysis (§9). The labelled texts are archived AI answers about brands. No institutional review-board review is recorded for this exercise.

## Use of AI tools {-}

During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.

## 15. Files

Under `osf/methodology/v1_11/paperB/`: `prereg/PRE_REGISTRATION_v1_11_paperB.md` (this file); `prereg/LOCK_MANIFEST_v1_11_paperB.sha256`; `guide/source/Main.dc.html`, `guide/source/Rules.dc.html`, `guide/STUDENT_GUIDE_v1_11_paperB.md`, `guide/guide_vs_judge_v1_11_paperB.json`; `statement/statement_exercise_doc.md`, `statement/statement_source.json`; `forms/Code.gs` with its offline mock (`mock_test.js`, `mock_driver.js`, `mock_run.sh`); `packets/make_packets_v1_11_paperB.py`, `packets/coi_screen_v1_11_paperB.py`, `packets/packet_design_N19_b.json`; `lock/paperB_lock_v1_11.py`, `lock/test_paperB_lock_v1_11.py`; `LOCK_STEPS.md`. Pinned, unchanged: `human_sample_v1_11_paperB_r1.csv`, `../prereg/judge_prompt_v1_11.md`; `../anchor/DEVIATIONS.md` (Entries 0–2) as it stands at the lock.

## Appendix A. The student guide, word for word

Text of the two pages as read (§5; generated from `guide/source/` by `lock/paperB_lock_v1_11.py --guide-md`).

<!-- BEGIN GUIDE -->
#### Page 1

```text
SVA MPS BRANDING · CLASS OF 2027 Third System™ research · page 1 of 2
OPTIONAL · ABOUT 45 MINUTES · NOT GRADED
Labeling AI answers about brands
You'll read about 55 short AI answers and mark the tone toward one brand in each. Your labels show whether an AI judges tone the way people do.
SIGN UP BY
Nov 20
FORM ARRIVES
Nov 23
LABELS DUE
Dec 4
RESULTS TOGETHER
Apr 21
Four questions for each answer
About the named brand only. Examples use a made-up brand, “Halvor”.
1
What's the tone toward the brand?
+2 · Strongly favorable
“The best knife you can buy.”
+1 · Favorable
“Well regarded and good value.”
0 · Neutral or balanced
“Makes knives from $80 to $150.”
−1 · Unfavorable
“A bit overpriced.”
−2 · Strongly unfavorable
“Skip it; the handles crack.”
Not about this brand
“I don't know this brand.”
2
Praise and criticism?
Yes or No
If Yes, your tone is the overall balance: 0 when both sides weigh about the same.
3
Where does the judgment come from?
No judgment · facts only
The AI's own voice · “Halvor is overpriced.”
Quoted sources · “Reviewers rate it highly.”
Both · “Testers love it, and I agree.”
4
How sure?
Sure or Not sure
Use “Not sure” freely; it helps.
Only the text counts, not your opinion of the brand. Work alone and don't look anything up. Rules for hard cases, and the exact instructions the AI judge gets, are on page 2.
How your labels will be used
Your name is replaced by a code before analysis; only I keep the key.
I use AI tools (Claude) to help analyze the coded data.
Coded labels, with no names, go on OSF, a public research archive. Results appear in a paper, on thirdsystem.ai and in Third System talks.
You're named only if you ask to be thanked in the paper.
You can stop at any time, and withdraw your labels until December 18 by emailing pablou@pablou.com.
Signing up means you've read this and agree to take part.Questions: pablou@pablou.com or Emily Weiland
```

#### Page 2

```text
LABELING AI ANSWERS ABOUT BRANDS Third System™ research · page 2 of 2
Rules for hard cases
Judge the target brand only. Ignore what the text says about other brands, unless it compares them with the target brand.
Being listed is not tone. Being named, included in a list of picks, or listed first is not an evaluation. Rate the words that describe the brand. Just named, with nothing said about it: tone 0, No judgment.
Facts are not praise. “Has a 10-year warranty” is 0; “stands out for its generous 10-year warranty” is +1.
Reported opinions count. Awards, ratings, complaints and recalls that the text reports are evaluations. “Some owners mention quality issues” is −1, from Quoted sources.
Go by the overall impression. One small caveat inside strong praise is still favorable. Use 0 for mixed texts only when neither side wins.
Work alone. Don't look anything up, don't compare with classmates before April 21, and don't go back to change an answer after you have moved on.
The exact instructions the AI judge receives
You and the AI judge follow the same rules and scale. Here they are word for word. The judge answers in a fixed format, so some lines name its answer fields: your tone answer is its “valence”, “Not about this brand” is “refers_to_brand” false, question 2 is “mixed”, and any answer to question 3 other than “No judgment” is “evaluative”. Question 3's split between the AI's own voice and quoted sources is ours; the judge does not record it.
Rules:
1. Rate only statements about the target brand: its products, quality, performance, value, reputation, people and conduct, and comparisons that involve it. Ignore statements about other brands unless they compare the target brand with them.
2. Being named, listed or recommended by inclusion is not an evaluation in itself. List labels and phrases that only repeat the question (for example "Top picks:" or "Brands for beginners:") are not evaluations of the target brand. Rate the words that describe the target brand itself.
3. Plain facts are neutral: history, founding date, ownership, location, product range, ingredients, price level or market position stated without judgement.
4. Evaluations count: praise or criticism by the assistant, and judgements by others that the text reports (awards, ratings, critical acclaim, complaints, recalls, controversies, lawsuits).
5. "evaluative" is true if the text contains at least one evaluation of the target brand under rule 4, and false if it contains only facts or description.
6. If favourable and unfavourable evaluations are both present, set "mixed" to true and choose the valence that reflects their overall balance (0 if they are of similar weight).
7. If the text does not refer to the target brand (the name is used as an ordinary word or for a different company, or the assistant says it does not know the brand and describes nothing), set "refers_to_brand" to false, "evaluative" to false, "mixed" to false and "valence" to 0.
Valence scale:
2 = strongly favourable: emphatic praise or endorsement of the brand ("outstanding", "the best", "exceptional quality") with no substantive reservation.
1 = favourable: a positive evaluation ("well regarded", "reliable", "good value", "award-winning"), possibly with minor reservations.
0 = neutral: no evaluation of the brand (facts or description only), or favourable and unfavourable evaluations of similar weight.
-1 = unfavourable: a negative evaluation ("overpriced", "inconsistent quality", "mixed reviews", "less refined than"), possibly with some positives.
-2 = strongly unfavourable: emphatic criticism or warning ("avoid", "poor quality", a scandal or recall presented as defining) with no substantive positive.
All examples are invented, about a fictional brand (“Halvor”). None comes from the texts you will label.Questions: pablou@pablou.com
```
<!-- END GUIDE -->
