**Brief 4 (editor screen) report: AIAS v0.40 SSRN paper, 2026-11-21**

I judged the paper against the research-note standard of a general marketing or consumer-research journal. I used only the paper text, the figures (I viewed fig_02), the values file, the pre-registration and DEVIATIONS.

**1. Desk-reject screen**

- **Fit:** good. The topic (brand share in AI answers, Double Jeopardy, brand exits) suits a research note.
- **Contribution up front:** weak. Neither the abstract nor §1 says what is new against prior work. The abstract (about 300 words) is a list of hypothesis labels and verdicts.
- **Length and format:** 16 pages is fine. But the paper reads like a programme technical report: file paths, commit hashes, value keys in captions and S-codes.
- **Literature:** thin and mostly the author's own work. 12 of 16 references are the author's. There is no engagement with outside work on LLMs in marketing, LLM recommendation bias or knowledge cutoffs.

**2. Three hardest reviewer objections**

1. **H_Amplify could not reach "amplified", and banks could not even reach parity (§3.4, Fig. 2, Discussion "did not concentrate on the leader").**
   - The registered n is the total number of brand namings across answers, not the number of answers (pre-reg §2.3).
   - There are 432 search-off recommendation answers per category (16 probes × 9 models × 3 runs; the values file gives legacy 288).
   - So k can be at most 432. With every answer naming the leader:
     - Airlines: the highest possible ratio is about 432/1,884/0.216 ≈ 1.06, below the 1.25 threshold.
     - Banks: it is about 432/2,495/0.181 ≈ 0.96, below parity.
   - Chase was named in 395 of 432 bank answers (91%), yet the paper calls it "flattened".
   - The binomial test also treats each naming as an independent draw, although k cannot exceed the answer count.
   - **Current answer:** only the "counts answers, not rank or prominence" caveat (§4, limitation 8). The ceiling is not mentioned.

2. **The ghost measures may not be valid (§3.2, §3.5, §3.7).**
   - On recommendation answers, which H_Afterlife rests on, the gone-flag coder's κ is 0.487.
   - The audit is AI-only, and one of its coders, Claude Fable 5.2, is also a tested model.
   - The status question ("can one still book with / open an account at X") invites a "gone" answer.
   - Living-brand controls were flagged 16.9% of the time, and 34.9% for the current models.
   - **Current answer:** this is disclosed openly (§3.2, §3.7, limitations 3, 4 and 7), and §3.5 calls the afterlife rates upper bounds. Nothing shows H_Flag measures more than the question's wording.

3. **The share results rest on few units and a coding choice, and have no rival explanation (§3.3, §2.3, §3.6).**
   - Airlines have 10 units, and moving one (Sun Country) flips the result (ρ 0.483, p 0.099).
   - The ambiguity rule drops the bare names "American", "United" and "Delta", which are the largest airlines.
   - Nothing separates market share from web salience or brand age as the driver.
   - The exact tests treat pairs as independent although they share ghosts, probes and runs (limitation 6). So H_Decay's "p < 0.001" rests on 16 named pairs.
   - **Current answer:** the sensitivities are reported (S-Ambig, S-SunCountry, S-Arm), and §4 says airline reinforcement "should be read with its sensitivity". Nothing addresses rival predictors or clustering.

**Findings**

| ID | Location | What is wrong | Evidence (source) | Severity |
|---|---|---|---|---|
| E1 | §3.4, Fig. 2, abstract, §4 | The "flattened" verdict comes from the registered ratio's ceiling, and the paper does not say so. It is one of the two findings §4 calls "clear". | k ≤ 432 answers. Airline maximum ratio ≈ 1.06 (< 1.25). Bank maximum ≈ 0.96 (< 1). Chase 395/432 = 91% (values `H_Amplify.*`; pre-reg §2.3 and line 42). The verdict stands as registered, but its framing needs the ceiling stated. The design issue in the locked pre-reg is **needs Pablo**. | blocker |
| E2 | §1, References | Positioning is the most likely desk-reject reason. There is no contribution statement, and outside literature is missing. Works to consider (named from my memory; check before citing): Aggarwal et al. 2024, "GEO: Generative Engine Optimization" (KDD); Brand, Israeli & Ngwe 2023, "Using GPT for Market Research"; Li, Castelo, Katona & Sarvary 2024, Marketing Science (LLM perceptual analysis); Dhingra et al. 2022, "Time-Aware Language Models as Temporal Knowledge Bases" (TACL); Cheng et al. 2024, "Dated Data" (knowledge cutoffs); Varadarajan, DeFanti & Busch 2006 (brand deletion, JAMS); Jaju, Joiner & Reddy 2006 (brand redeployment after mergers, JAMS); popularity-bias work in LLM recommenders. | 12 of 16 references are by González Castro. The only outside works are Ehrenberg et al. 1990, Sharp 2010, Romaniuk & Sharp 2016 and Shaw & Nave 2026. | blocker |
| E3 | Abstract | Too long and too dense in internal labels for a research note. | About 300 words, with six H_ labels and four verdict words in capitals. | fix |
| E4 | Title | "Challengers" is in the title, but challengers are never defined or analysed. | "Challengers" appears only in the title. | fix |
| E5 | §2.3 | "Presence" (ghost Presence, the H_Decay measure) is used but never defined in the paper. | The definition exists only in the pre-reg: "share of the model's search-off recommendation answers … that name it". | fix |
| E6 | Fig. 2 subtitle | The label calls n "answers naming any current unit", but n is the total of brand namings. | 1,668 airline namings vs 432 airline answers; §3.4 itself says "unit-namings". | fix |
| E7 | References | Uncited entries (format breach). | v1.3–v1.8 (SSRN 6797679, 6799479, 6810758, 6816340, 6878818, 6963359), AIAS 1.0 (6817841) and the phase-paper list are cited nowhere in the text. | fix |
| E8 | Throughout | Internal pipeline detail in reader-facing text. | "score_v0_40.py", "osf/v40/DEVIATIONS.md", "commit a53d2b7", "Values: H_Reinforce.*, sensitivity.*…" in every caption. | fix |
| E9 | Declarations, COI | The quote is attributed to the "v0.62 pre-registration", but the source record is "v0.62 DEVIATIONS Entry 0, Part F". The Denon/v0.19 correction is unrelated to v0.40 and makes the section longer. | DEVIATIONS.md line 11. | fix |
| E10 | §2.7, limitation 10 | A pre-reg whose first line reads "DRAFT … not locked" will alarm a reviewer. The disclosure is honest. | Pre-reg line 1. The file is locked, so this is **needs Pablo**, with no change to the file. | note |
| E11 | Figs 1–6 | No uncertainty intervals are shown. Only point values, p and n are given (rubric principle 10). | Fig. 2 render. | note |
| E12 | Keywords / JEL | JEL codes use mixed separators. | "M31; L86, L15, D83, M37" | note |

**3. Recommendation:** send after fixes:
- E1: state the ceiling of the H_Amplify ratio beside the verdict and in §4, and soften "flattened" to what the measure allows. Pablo needs to decide how to handle the design issue in the locked pre-reg.
- E2: add a contribution paragraph and outside literature.
- E3–E9: shorten the abstract, fix the title, define Presence, correct the Fig. 2 label, prune uncited references, cut pipeline detail from the text and captions, and correct the COI record.

**Verdict: blocked (2 blockers: E1, needing Pablo for the pre-registration issue, and E2).**
