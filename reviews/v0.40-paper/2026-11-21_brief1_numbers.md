# Brief 1 report: numbers and citations. AIAS v0.40 SSRN paper, review date 2026-11-21

**Scope.** I read the paper text, the six figure PNGs, the template, the values file, the verdict file (spot-checked), the pre-registration, DEVIATIONS and the audit record. I used only Read, Grep and Glob, and changed nothing.

## Claims ledger (compact)

| Claims (where) | Source | Result |
|---|---|---|
| Every `{{v:…}}` value in the abstract, §2.2–§2.6, §3.1–§3.10, Tables 1–3, Discussion and Limitations (about 200 values) | `v40_values.md`. I checked each key's Display value against the PDF text. | **match**, all of them |
| Values file against verdict file: H_Amplify airline ratio 0.599, H_Decay ρ −0.286, H_Flag ghost rate 98.0%, McNemar p 0.969, S-SunCountry ρ 0.483 | `v40_verdicts.json` lines 44, 87, 95, 106, 284 | match |
| Audit figures: κ 0.883, 932 entities, 96.0%, ties broken by `gemini-4-carbon`, $6.12 of $25.00 | `v40_audit_agreement.md` lines 5, 7, 13 | match |
| Figures 1–6: every point label, n, p and threshold line | values keys `H_*`, `sensitivity.*` | match (Fig 4 legacy −0.327, 11 of 130; current −0.200, p 0.043, 5 of 67; Fig 3 S-Legal 9 of 153, and so on) |
| 2,821 calls = 1,786 + 846 + 189; MC1 current 1,035 = 846 + 189 | prereg §4.2 table; DEVIATIONS Step 6 | match |
| Spend $36.74 + $6.40 = $43.14; + $6.12 = $49.26; cap $100.00, pause $80.00 | values `cost.*`; prereg §6.5 | match (recomputed from unrounded values: 49.2567) |
| 10 airline units (Hawaiian inside Alaska), 25 bank holders, 24 ghosts (7 + 17), 3 living-brand controls, 4 incumbents | prereg §2.1, §3.1; DEVIATIONS Entry 0 | match |
| Registry frozen 12 Nov; locked 16 Nov (7 pm CT); commit a53d2b7; collection 17–19 Nov; Entry 1 dated 21 Nov; OSF ec6wh v40/prereg and v40/registries | DEVIATIONS lock record, collection start, Step 6, Entry 1 | match |
| "since 2008", panel "fixed since v0.17", 150 characters, 10,000 permutations, seed 4040, MC limits 5% / 2% / 80% | prereg header, §2, §2.8 | match |
| "the three brokerage and wealth holders" (S-D4) | prereg §5.6: Morgan Stanley, Schwab, UBS | match |
| Claude Fable 5.2 uses Claude Opus 5.5's cutoff rows | prereg §2.1, §8 item 5 | match |
| Audit sample 200 (100 + 100); coders `claude-fable-5-2`, `gpt-6.2-astra`, `gemini-4-carbon` | DEVIATIONS Entry 1 items 2 and 4 | match |
| Section pointers §2.2–§2.10, §3, §4.1–§4.4, §5.5, §5.6, §5.9, §6.3–§6.4 | prereg headings | match |
| Pre-registered descriptives numbered 1, 2, 4, 7, 9 | prereg §2.9 | match |
| Wording of the locked file's first line (§2.7) | prereg line 1 | match |
| COI quote, including "28.43%" and the five brands | prereg §10, verbatim | match against the prereg; the original v0.62 record was not supplied (see F4) |
| Harman / Denon correction: 10 Nov 2026, March 2017, Nov 2016, 23 Sep 2025 (Declarations) | not in any source supplied | **untraceable / unverified** |
| AI-use statement | rubric text, verbatim | match |
| SSRN 6761698 (Protocol v1.2); MSI Report No. 26-132; Shaw & Nave, SSRN 6097646 | prereg header and §11; rubric | match |
| Other SSRN IDs: 6659000, 6797679, 6799479, 6810758, 6816340, 6878818, 6963359, 6817841, the 15 phase-paper IDs, 7685199 | no source supplied | **unverified** |
| Ehrenberg et al. 1990, *JM* 54(3) 82–91; Sharp 2010; Romaniuk & Sharp 2016 | no source supplied | unverified (not checked from memory) |
| ORCID, correspondence address, JEL codes | no source supplied | unverified (not result numbers) |

## Recomputed derived figures (all match)

- **Leader ratios**, (k/n)/p₀:
  - 216/1,668 ÷ 0.21612 = 0.599
  - 395/2,458 ÷ 0.18122 = 0.887
  - 251/1,668 ÷ 0.19943 = 0.755
  - 216/1,655 ÷ 0.21612 = 0.604
  - 172/1,223 → 0.651; 44/445 → 0.457; 265/1,699 → 0.861; 130/759 → 0.945; 349/2,403 → 0.672
- **Rates:**
  - Afterlife, main: 3/55 = 5.5%; 9/142 = 6.3%
  - Afterlife, by arm and S-Ambig: 1/36 = 2.8%; 7/94 = 7.4%; 2/19 = 10.5%; 2/48 = 4.2%; 7/55 = 12.7%; 12/142 = 8.5%
  - Afterlife, S-Legal: 9/153 = 5.9%
  - Flag: 579/591 = 98.0%; 32/189 = 16.9%; 22/162 = 13.6%; 10/126 = 7.9%; 22/63 = 34.9%; 378/390 = 96.9%
  - Old versus new name: 1,942/3,468 = 56.0%; 1,115/2,108 = 52.9%; 165/246 = 67.1%
  - Audit: 895/932 = 96.0%
- **Structural counts:**
  - 197 pre-cutoff pairs = 24 × 9 − 19
  - 55 airline pairs = 63 − 8 (Spirit); 142 bank pairs = 153 − 11
  - 591 ghost status answers = 197 × 3
  - 189 control answers = 7 controls × 9 models × 3 runs; 162 without Discover = 6 × 27
  - 72 paired cells = 24 × 3; 5 post-cutoff cells = SVB × 3 + Spirit × 2
  - MC3: 108 = 4 × 9 × 3; MC2: 63 = 32 + 31
  - MC4 legacy truncations: 29 = 27 + 2
  - Audit tables sum: 183 + 6 + 31 + 712 = 932; 17 + 5 + 28 + 687 = 737
  - Audit sample rates: 25/30 = 83.3%; 19/30 = 63.3%
- **Tests and text claims:**
  - One-sided exact McNemar with 1 vs 4 discordant cells: P(X ≥ 1 | 5, 0.5) = 31/32 = 0.969
  - "Did not search in about a third": 22/63 = 34.9%
  - Run-to-run standard errors 0.008 / 0.010 / 0.017 / 0.022 are below v1.17's 0.040 / 0.050 (prereg §2.10)

## Findings

| ID | Location | What is wrong | Evidence | Severity |
|---|---|---|---|---|
| F1 | Fig 2 subtitle | It defines the denominator as "answers naming any current unit". n is actually the sum of unit-namings: an answer naming three units counts three times. The numbers are right but the label misdescribes them, and it contradicts §3.4. | Fig 2: "Labels: ratio (answers naming the leader of answers naming any current unit)". §3.4: "216 of the 1,668 airline unit-namings". Prereg §2.3: "n = the sum over current units of recommendation answers naming each unit". | fix |
| F2 | Fig 1 and Fig 4 subtitles | The threshold symbol (≥ in Fig 1, ≤ in Fig 4) renders as a broken glyph, so the rule a filled marker stands for cannot be read. The text extraction loses it too. | fig_01.png: "Filled: rule met (ρ ◌ 0.50 …"; fig_04.png: "Filled: ρ ◌ −0.30 and p < 0.05"; paper.txt lines 279 and 418. | fix |
| F3 | Declarations, conflict of interest | The Harman / Denon correction has dates that no supplied source contains: 10 Nov 2026, March 2017, Nov 2016 and 23 Sep 2025. It is not a result number, but it is a dated factual claim. | Absent from the prereg §10, DEVIATIONS, the values file and the verdict file. | fix (unverified) |
| F4 | Declarations, COI quote | The paper attributes the quote to "the v0.62 pre-registration". DEVIATIONS Entry 0 cites the same record as "v0.62 DEVIATIONS Entry 0, Part F". The quote matches the locked v0.40 prereg §10 verbatim, but the original record (and its 28.43% figure) was not supplied. | DEVIATIONS line 11; prereg line 343 | note (attribution inconsistent; 28.43% unverified at origin) |
| F5 | References, phase-paper list | Most SSRN IDs cannot be traced to a supplied source. The last ID, 7685199 (v0.37), is far out of sequence with the other 14 (6791999–6915458), which could be a typo. | Reference list on p. 16 | note (unverified; check 7685199) |
| F6 | Fig 1 group headers | "Airlines (10 share units)" and "Banks (25 holders)" also head the S-SunCountry row (9 units) and the S-D4 row (22 holders). | `sensitivity.S-SunCountry.H_Reinforce_airline.n_units` = 9; prereg §5.6 drops 3 holders | note |
| F7 | §3.10, run-to-run precision | "below the method v1.17 planning estimate" gives no number. The estimate (0.040; 0.050 for units named in some answers but not all) is not stated near the claim (rubric principle 1). The claim itself is true. | prereg §2.10 | note |
| F8 | Title page, abstract block | ORCID, correspondence address and JEL codes ("M31; L86, L15, D83, M37": mixed separators) cannot be traced to a supplied source. | n/a | note (unverified) |

No result number in the text, the tables or the figure labels is a mismatch or untraceable. All the result values come from `v40_values.json`, which agrees with the verdict and audit files.

**Verdict:** no blockers. There are 3 fixes (F1, F2 and F3, which is unverified) and 5 notes.
