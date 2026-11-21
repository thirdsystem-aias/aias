# Brief 3 report: consistency across documents. AIAS v0.40 SSRN paper, 21 Nov 2026

**What I checked:** definitions, model names, dates, counts and figures in the paper against the pre-registration (PR), DEVIATIONS (DEV), the values file (VAL), the verdict file through VAL, and the audit record (AUD). I also checked the names and status words that Brief 3 step 2 lists.

**What agrees with the record:**
- **Counts:** 2,821 calls (1,786 / 846 / 189), 27,647 mentions and 24 ghosts (7 airline, 17 bank) all match. So do the 3 living-brand controls and the 4 incumbents, and 10 airline and 25 bank units. Pre-cutoff pairs match too: 197 = 55 + 142, and 208 under S-Legal. Answer counts check: 591 = 197×3 and 189 = 7×27. MC counts match, and S-Length's 43 matches.
- **Spend:** $36.74 + $6.40 = $43.14, plus the $6.12 audit gives $49.26.
- **Dates:** registry freeze 12 Nov, lock 16 Nov (CT), collection 17–19 Nov, DEV Entry 1 dated 21 Nov.
- **Audit:** the three coders, 12 tie-breaks, κ 0.883 / 0.914 / 0.487, and 895 of 932 all match.
- **Scorer re-run:** the mentions file's SHA-256 equals the coding manifest's (0a83…).
- **Names and status words:**
  - "System 3" cites Shaw & Nave (SSRN 6097646) and MSI Report No. 26-132.
  - The AI-use statement is verbatim.
  - The employer appears only in Declarations.
  - The independence wording matches PR §1.
  - Third System™ and AIAS™ carry the mark on first prominent mention.
  - No combined score appears.
  - v0.38 and v0.39 are not named.

## Findings

| ID | Location | What is wrong | Evidence: this paper says / other document says (primary) | Severity |
|---|---|---|---|---|
| C1 | §2.2 ("newest generally available flagship on the vendors' pages **at the lock**"); Abstract ("the newest flagship of each of three providers") | The date of the model check is wrong, and the record suggests Argon and Astra may not have been the newest flagships. | **Paper:** checked "at the lock" (16 Nov). **PR §4.3:** "checked on the vendors' pages on **2026-11-12**". On the re-check of 12 Nov, PR found the Gemini API changelog had "no entry mentions Gemini 4 Carbon and there is no November 2026 entry". It also flagged that "if Google states that Gemini 4 Carbon is generally available in the Gemini API before the lock, Carbon would replace Argon". **DEV Entry 1** (read 21 Nov) quotes "The Gemini API changelog of **2026-11-10** reads 'Gemini 4 Carbon … generally available (GA) … our most capable reasoning model'". It also says GPT-6.2 Astra "is newer than GPT-6 Astra, which this study's current arm uses". The paper names gpt-6.2-astra and gemini-4-carbon as audit coders without saying this. **Primary:** PR for the check date. PR and DEV contradict each other on when Carbon became GA, so this **needs Pablo**. | **blocker** (a reader would believe C2 and C3 were the newest GA flagships when the study ran) |
| C2 | §2.7 ("The file was not edited at or after the lock") | Contradicts the lock record. | **DEV lock record:** "Changes at the lock … (1) §9's test count corrected … (2) LOCK_MANIFEST refreshed: four files had changed … (the pre-registration text above, …)". The edit was not substantive ("no hypothesis, threshold … changed"), but it was made at the lock. **Primary:** DEV. Suggested wording: "edited only at the lock, for §9's test count (DEVIATIONS lock record), and not after". | fix |
| C3 | §3.10 "Not in the scored record"; Limitation 9 ("Two pre-registered descriptives are missing"); Limitation 6 | More pre-registered reporting promises go unmet than the paper declares. | **PR §8.6:** "per-ghost and per-model results are reported beside each test". The paper's Limitation 6 drops this clause. **PR §3.2 (a):** "the status answers about Discover are shown in full in the descriptives". They are not shown. **PR §2.9.8** lists six near-floor holders and VAL carries all six (Synchrony 11/4/1, Santander 9/3/0, Zions 9/4/1, …). The paper reports USAA only. Descriptive 5 (M5 against M5X: calls, ghost mentions) is only partly reported. **Primary:** PR. | fix |
| C4 | §1, §2.3, §3.6, §3.10, Table 1 | "Presence" and "ghost Presence" are used as the study's measure but never defined. | **PR §2.5:** "ghost Presence = share of the model's search-off recommendation answers in the ghost's category that name it (any run; ambiguous mentions excluded)". The paper's §2.3 defines mention, AI share and gone-flag, but not Presence. This breaks rubric principle 3 and the "Presence as a measure" check. | fix |
| C5 | Fig. 1 and Fig. 4 subtitles | The registered rule cannot be read because a glyph is missing. | **PNG renders:** "Filled: rule met (ρ ⍻ 0.50 …)" and "Filled: ρ ⍻ −0.30 …". The extracted text shows the symbol as blank ("Filled: rule met ( 0.50"; "Filled: 0.30"). PR §2.2 / §2.5 require "≥ 0.50" and "≤ −0.30". | fix |
| C6 | §2.2 ("the two declared pre-lock checks ($6.40)") | The paper merges two differently named steps under one label. | **PR header and §6.5:** a "Pre-lock check" ($4.73, §4.8) and a separate "Technical check" ($1.67). VAL `cost.prelock_check_usd` and `cost.technical_check_usd` keep them apart. **Primary:** PR. | note |
| C7 | Declarations, COI ("the correction of 10 November 2026 to the v0.19 disclosure … Harman … Denon") | Not in any v0.40 source. | This text is absent from PR §10 Declarations and from DEV. **Unverified** from the sources given. | note |
| C8 | §4 ("This supports the MSI framework's P1 (default reinforcement)") | The wording could imply the framework is MSI's, and the gloss "default reinforcement" has no source in the record. | **Rubric 9:** no implied endorsement by MSI. **PR §header and §1:** P1 asks whether AI "track[s], amplify or flatten[s]" share; the "default reinforcement" label is not in PR. Suggest "the Tri-System framework's P1 (MSI Working Paper 26-132)". | note |
| C9 | Throughout ("AIAS v0.40", "AIAS measurement programme") | Possible conflict with the naming rule. | **Rubric 8:** "AIAS always as Score". The paper never writes "AIAS Score" and uses AIAS as the programme name. Brief 3 itself asks only for TM on first mention, which holds (title). The registry was not provided, so this is **unverified**. | note |
| C10 | §2.2 and §2.7 (record of steps) | A logged step has no recorded outcome, and the paper is silent on it. | **DEV step 6:** "The old-panel check (step 7, Sat 11/21) still follows". No later DEV entry records it. | note |
| C11 | Table 1 "Rule" column | The table summarises the registered verdict rules but leaves some out. | **PR §2.2:** H_Reinforce FALSIFIED is "both evaluable and p ≥ 0.05 in both". Table 1 omits it, and also omits PARTIAL for H_Amplify, H_Afterlife and H_Flag. There is no contradiction, but a reader cannot rebuild every verdict word from the table. | note |

**Verdict: blocked.** C1 needs a wording fix in the paper. Pablo also needs to settle whether the record shows Gemini 4 Carbon was GA in the Gemini API before the lock, because PR §4.3 and DEV Entry 1 disagree.
