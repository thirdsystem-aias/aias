# AIAS™ Presence Measurement Protocol — Pre-Registration v0.40 (revision r1, DRAFT for the pre-registrant's review — not locked)

**Substrate:** US airlines (share: revenue passenger miles, BTS T-100) and US retail banks (share: deposits, FDIC Summary of Deposits), with every brand retired by merger, failure or rename from 2008-01-01 to 2026-11-12.
**Working title:** Leaders, challengers and ghosts. Two US categories reshaped by mergers and failures.
**Design:** Category registry built mechanically from official data (no focal brand), two-arm panel: the legacy fixed panel (v0.17–v0.39) and the current assistants without and with each provider's own web search.
**Programme position:** First public flagship study under the independence rule (no focal brand, no lessons addressed to a brand, no brand contacted). Tests the MSI framework's proposition P1 (does AI's share of recommendations track, amplify or flatten real market share; MSI Working Paper *Tri-System Brand Growth: The AI Mediation Layer*, Report No. 26-132) and, for the first time with dated exits, whether brands that no longer exist keep a place in AI answers and how that place decays with the time between the exit and each model's training cutoff.
**Protocol version:** Presence definitions per Methodology v1.2 (SSRN 6761698); legacy-arm panel and decoding per v0.17–v0.39 (temperature 0.0; max output 2,048 tokens), except Gemini 2.5 Flash (§4.4).
**Lock target:** git tag `v0.40-prereg-r1` on branch `v0.40` (pushed from the runner branch `v0.40-runner`). **External anchor (pre-declared):** this pre-registration, the probe set, the frozen registry, the scripts and the lock manifest deposited at OSF `ec6wh` → `v40/prereg/` and `v40/registries/` before any study probe is sent. `acquire_v0_40.py --collect` refuses to run unless the tag is on `origin` and `osf/v40/anchor/osf_anchor_v0_40.json` names its commit.
**Pre-registrant:** Pablo Ulpiano González Castro
**Status:** DRAFT r1, written 2026-11-12 by the runner; r1 working revision of 2026-11-12 adds the sensitivities, descriptive definitions, conflict-of-interest screen, vendor re-check and v1.17 category-size reading (§9, "Done by the runner"). Locks 24 hours after the pre-registrant receives it unless he objects. Open items are marked **PENDING PABLO** (§9).
**Change log, 2026-11-13 (runner; under the pre-registrant's approval of 2026-11-12, 11:36 pm CT):** added the length-limit stop rule inside the collection (§4.7), the pre-lock check on an already-published category's questions (§4.8; 258 paid calls, $5.91 central, counted toward the $100 cap; the lock waits for its PASS) and the declared handling of answers at the length limit or with thinking at half the limit or more (§5.9, sensitivity S-Length); the guard counts the check's spend (§6.5); the Discover switch is set to (a), as the pre-registrant decided on 2026-11-12, 6:57 am CT (§3.2, §8 item 7, §9 item 1). No other rule changed.

**Change log, 2026-11-13, later (runner, before the lock; no rule changed):** the pre-lock check was run and passed (§4.8). Its first pass found two faults, both fixed before its resumed calls: Claude Sonnet 4.5 is not served to the new Anthropic organization (24 calls answered 404, unbilled), so M2 is now sent with the old organization's key by `call_anthropic_legacy_org`, a copy of the verbatim `call_anthropic` whose request is unchanged (§4.3; each record names its key in `api_key_env`; `test_acquire_v0_40.py` checks the routing and that the request matches); and one GPT-6 Astra call was lost to a Python import deadlock between worker threads, so `require_keys()` now also imports the SDK modules once before any thread starts (`warm_imports`). `cost_estimate_v0_40.py`'s default t4 path now follows the OSF layout (`v42/data/t4_raw.jsonl`); run with `--t4` pointing at the collection computer's copy it reproduces `cost_estimate_v0_40.txt` exactly.
**Pre-lock check (declared non-acquisition step, §4.8):** **PASS, run 2026-11-13 by the runner** (258 of 258 answers; recorded spend $4.73; its paid calls approved by the pre-registrant on 2026-11-12).
**Technical check (declared non-acquisition step):** on 2026-11-09 (00:22 UTC) `feasibility_v0_40.py` sent each legacy model, Gemini 2.5 Flash in both settings and the then current arm (Claude Opus 5.5, GPT-6 Astra, Gemini 4 Argon) one neutral, non-category prompt ("Reply with the single word: ready"), and each current model two neutral search prompts (today's date; the current BBC headline); 16 of 16 calls returned ok (`prereg/feasibility_v0_40.json`, `.csv`). No study probe was sent and no brand was named. Because the current arm now uses Claude Fable 5.2 through the Message Batches API (§4.3), the same check is repeated for Fable 5.2 before the lock with `acquire_v0_40.py --feasibility` (neutral prompts only; output `prereg/feasibility_check_v0_40.json`). **PENDING (runner, before the lock).** *2026-11-12, not run:* as written, `--feasibility` sends the whole panel (10 neutral calls and 6 search calls), not Fable 5.2 alone, and sends Fable 5.2 synchronously at $8 / $40; the two search prompts used about 13,300 and 61,600 input tokens on Claude Opus 5.5 on 2026-11-09 (`feasibility_v0_40.csv`), which at Fable 5.2's prices is about $0.12 and $0.52 before search fees, above the runner's $0.50 ceiling for this step. A Fable-only check, or one without the BBC-headline prompt, needs the coordinator's approval.
**Acquisition window:** 2026-11-17 00:00 CT to 2026-11-21 23:59 CT. The legacy arm must be complete before 2026-11-24, the earliest possible retirement of Claude Opus 4.5 (Claude Sonnet 4.5 retires 2026-11-30; registry `model_cutoffs.csv`).

---

## §1 Context and questions

The MSI framework paper (Report No. 26-132) proposes that the AI layer reweights brands relative to their market position (P1). Two earlier phases bracket the question this study asks about brands that have left the market: Mint was named in 44.8% of answers 25 months after it closed (v0.10), while five car brands closed in 2001–2010 were named in 0 of 18 answers (v0.22). Neither phase had dated exits matched to each model's training cutoff.

- **RQ1.** Does AI's share of recommendations track real market share, amplify the category leader (Double Jeopardy) or flatten it?
- **RQ2.** Do brands that disappeared through a merger, failure or rename still appear in AI answers; does that presence decay with the time between the exit and each model's training cutoff; do answers say the brand is gone; and does web search change that?

US airlines and US retail banks were chosen because both have official share data (BTS, FDIC), many dated exits since 2008, and no product category in which the pre-registrant's employer competes (Declarations). The study is independent: there is no focal brand, no finding is addressed to a brand, and no brand was contacted.

---

## §2 Pre-registered hypotheses

Verdict words: CONFIRMED, PARTIAL, UNDETERMINED, FALSIFIED. Every test is one-sided as stated, at α = 0.05, without multiplicity correction (six tests, each reported in full, including failures). Permutation tests use 10,000 permutations with seed 4040; p = (hits + 1)/(permutations + 1). All thresholds below are fixed in `score_v0_40.py` (`T`) and tested on synthetic data (§5.8).

### §2.1 Definitions (used by every test)

- **Answer:** the text of one completed call (status ok, non-empty). **Recommendation answers** are the answers to the 16 recommendation probes of the brand's category (6 generic, 6 by need, 4 by Census region).
- **Mention:** a whole-word, case-sensitive match of a registry alias (§5.2) in an answer; the longest alias wins and overlapping shorter matches are dropped. A mention through a bare collision alias (D11) is **ambiguous** and is excluded from every primary test (reported with it as a sensitivity).
- **Current unit:** one of the 10 airline share units (11 brands; Hawaiian inside Alaska, R8) or 25 bank holders of the frozen registry. A retained brand's mentions count toward its share unit (D2, D12: Discover toward Capital One).
- **AI share** of a current unit, per model: the number of the model's recommendation answers that name the unit, divided by the sum of that count over all current units of the category; the study's AI share is the mean over the nine tested models (six legacy, three current, search off).
- **Market share:** airlines, allocated brand share of RPM (registry `airlines_current.csv`, `brand_share_pct`; D1); banks, share of deposits (`banks_current.csv`, `share_pct`).
- **Ghost:** one of the 24 registry exits (7 airlines, 17 banks). **Gap:** months from the ghost's brand-retirement date to the model's primary cutoff (registry `exit_cutoff_gaps.csv`, `gap_brand_m`; R11). A **pre-cutoff exit** has gap > 0 for that model. Claude Fable 5.2 has the same training-data cutoff month as Claude Opus 5.5 (Jun 2026; §4.3), so the frozen Opus 5.5 rows are used for it unchanged.
- **Gone-flag:** a mention is gone-flagged when the locked lexicon (§5.3) occurs within 150 characters before or after it. An answer to a status (S) probe is flagged when any mention of its subject is gone-flagged, or, if the subject is not matched, when the lexicon occurs in its first 300 characters.
- **Tested models:** M1–M6 (legacy, search off) and C1–C3 (current, search off) for H_Reinforce to H_Flag; C1–C3 with search off and on for H_Search. The extra Gemini 2.5 Flash pass at the v0.39 setting (M5X) is reported, never tested.

### §2.2 `H_Reinforce` (RQ1): AI share tracks market share

**Claim.** Within each category, current units with a larger market share receive a larger AI share.
**Test.** Spearman ρ between market share and AI share across the category's current units; one-sided permutation test (ρ > 0).
**Rule (per category).** Passes when at least 5 units have AI share > 0, ρ ≥ 0.50 and p < 0.05.
**Verdict.** CONFIRMED: both categories pass. PARTIAL: one passes. FALSIFIED: both evaluable and p ≥ 0.05 in both. UNDETERMINED: otherwise (including fewer than 5 units with AI share > 0 in a category).

### §2.3 `H_Amplify` (RQ1): AI amplifies the category leader

**Claim.** The leader's AI share exceeds its market share (Double Jeopardy amplification) rather than flattening it. Leaders: American Airlines (allocated share, D1; Delta in the operating-share sensitivity) and the JPMorgan Chase holder.
**Test.** Pooled over the nine tested models: k = recommendation answers naming the leader, n = the sum over current units of recommendation answers naming each unit, p₀ = the leader's market share divided by the category's total over current units. Ratio = (k/n)/p₀. Exact binomial test, one-sided both ways (amplified: X ≥ k; flattened: X ≤ k). The log-log slope of AI share on market share (units with AI share > 0) is reported, with and without the three brokerage and wealth holders (D4), and carries no verdict.
**Rule (per category).** Amplified: ratio ≥ 1.25 and p(X ≥ k) < 0.05. Flattened: ratio < 1 and p(X ≤ k) < 0.05.
**Verdict.** CONFIRMED: amplified in both. PARTIAL: amplified in one. FALSIFIED: flattened in both. UNDETERMINED: otherwise.

### §2.4 `H_Afterlife` (RQ2): ghosts keep a place in recommendations

**Claim.** Brands that exited before a model's cutoff are still recommended as if current.
**Unit.** Ghost × tested model pairs with a pre-cutoff exit (197 of the 216 pairs: 24 ghosts × 9 models, less the 19 post-cutoff pairs of the registry, Spirit and SVB and First Republic; with Fable 5.2 on the Opus 5.5 rows). A pair is an **afterlife pair** when at least one of the model's search-off recommendation answers (any run) names the ghost without a gone-flag.
**Test.** Per category, the afterlife rate k/n; exact binomial test against 0.05, one-sided (greater).
**Rule (per category).** Passes when the rate ≥ 0.20 and p < 0.05. Low when the rate < 0.05.
**Verdict.** CONFIRMED: both pass. PARTIAL: one passes. FALSIFIED: both low. UNDETERMINED: otherwise.

### §2.5 `H_Decay` (RQ2): presence decays with the exit-to-cutoff gap

**Claim.** The longer before a model's cutoff a brand was retired, the less often the model names it.
**Unit.** The same pre-cutoff ghost × model pairs; ghost Presence = share of the model's search-off recommendation answers in the ghost's category that name it (any run; ambiguous mentions excluded).
**Test.** Spearman ρ between gap (months) and ghost Presence over all pairs; one-sided permutation test (ρ < 0), gaps permuted within model.
**Floor.** Evaluable only when at least 10 pairs have Presence > 0; otherwise UNDETERMINED.
**Verdict.** CONFIRMED: ρ ≤ −0.30 and p < 0.05. PARTIAL: ρ < 0 and p < 0.05 with ρ > −0.30. FALSIFIED: ρ ≥ 0. UNDETERMINED: otherwise.

### §2.6 `H_Flag` (RQ2): answers say the brand is gone

**Claim.** Asked whether one can still book with or open an account at a ghost, models say it is gone, and they do not say so about living brands.
**Unit.** Search-off answers of the nine tested models to the status (S) probes, all runs. Ghost answers: pre-cutoff exits only. Control answers: the living-brand controls (Hawaiian, Sun Country, and the bank control set by the Discover switch, §3.2) and the four incumbents (American, Delta, Chase, Bank of America).
**Test.** Ghost flag rate; one-sided Fisher exact test that the ghost flag rate exceeds the control flag rate.
**Verdict.** CONFIRMED: ghost flag rate ≥ 0.80 and Fisher p < 0.05. PARTIAL: one of the two. FALSIFIED: ghost flag rate < 0.50 and Fisher p ≥ 0.05. UNDETERMINED: otherwise.

### §2.7 `H_Search` (RQ2): web search corrects the status of ghosts

**Claim.** With its own web search on, a current model flags ghosts it did not flag without search, including exits after its cutoff.
**Unit.** Current models C1–C3; ghost S probes. Search-off flag per (ghost, model) = flagged in a majority of its three runs; search-on flag = its single run (§4.2).
**Test.** Exact McNemar test (binomial on the discordant pairs, one-sided toward search-on flagging); the search-on flag rate on post-cutoff cells (ghost × current model with gap < 0: SVB for all three, Spirit for GPT-6 Astra and Gemini 4 Argon) is reported with it.
**Rule.** McNemar part: at least 10 discordant pairs and p < 0.05. Post-cutoff part: search-on flag rate ≥ 0.80.
**Verdict.** CONFIRMED: both parts. PARTIAL: one part. FALSIFIED: no more search-only flags than search-off-only flags, and post-cutoff search-on flag rate < 0.50. UNDETERMINED: otherwise (including a search-on block cut short by the budget guard, §6.5).

### §2.8 Manipulation checks (computed before any verdict is read)

- **MC1 Completeness.** At least 95% of each arm's planned calls end ok (legacy 1,786; current 1,035). Below that, every verdict that uses the arm is reported as computed and marked "incomplete arm".
- **MC2 Search used.** In S1, each current model searched (at least one recorded search) in at least 80% of its answers. Not searching is part of the condition and is kept (§7); below 80%, H_Search is reported with that caveat.
- **MC3 Recognition of incumbents.** The recognition (K) answers for American, Delta, Chase and Bank of America name the brand in at least 95% of answers. A failure means the coder or the probe is broken; scoring stops and the cause is logged before any verdict.
- **MC4 Output caps.** Truncated answers (finish reason at the token cap) are at most 5% in the legacy arm (2,048) and 2% in the current arm (16,384).

### §2.9 Pre-registered descriptives (no verdicts)

1. AI share against market share per unit and model, both arms, search off and on; the log-log slope with and without the brokerage and wealth holders (D4).
2. Ghost Presence and the afterlife rate per ghost, model and arm; post-cutoff exits (Spirit, SVB, First Republic) shown apart.
3. **Old versus new name:** of the ghost mentions (all answers, ambiguous mentions excluded), the share with the successor's name within 150 characters (registry `successor` column), per arm and condition (legacy search off; current search off; current search on).
4. Recognition (K) answers per ghost, model and condition, coded as: **flagged as gone** when a mention of the ghost is gone-flagged, or, when the ghost is not matched, when the gone-flag lexicon occurs in the first 300 characters and no non-recognition phrase occurs; **described as current** when the ghost is named and no mention is gone-flagged; **not recognised** otherwise (the ghost not named and no gone-flag, or a non-recognition phrase such as "not familiar", "not aware of", "can't find / identify / verify", "no information about"; locked list `NOT_RECOGNISED` in `score_v0_40.py`). *(Definition added in the working revision of 2026-11-12; the first r1 draft named the three codes without a rule.)*
5. The extra Gemini 2.5 Flash pass at the v0.39 setting against the thinking-off runs: calls, completed answers, truncation and ghost mentions, M5 against M5X.
6. Run-to-run standard error of per-model Presence at search off, from v0.40's own three runs, per arm: per model × current unit, the standard deviation of the three per-run Presence values divided by √3, averaged over units; reported for all units and for units named in some of the model's answers but not all, beside v1.17's 0.040 and 0.050 (§2.10).
7. Search traces (queries, number of sources and citations) per S1 answer, and the domains cited or retrieved in S1 answers to ghost status probes that were flagged.
8. Mentions of the near-floor holders coded "other" (D16: USAA, RBC, Synchrony, Western Alliance, Santander, Zions; aliases in `NEAR_FLOOR`, `score_v0_40.py`): bank recommendation answers naming each, per arm and condition. USAA is expected often. *(Alias list added 2026-11-12.)*
9. First-mention share per current unit, per model, condition and category: among the recommendation answers that name at least one current unit of the category (ambiguous mentions excluded), the share in which that unit is the first current unit named. *(Denominator added 2026-11-12.)*

### §2.10 Runs per cell and expected precision

Three runs per cell with search off in both arms; one run with search on (§6.4). Method v1.17 (locked 2026-11-12; OSF `methodology/v1_17`, tag `v1.17-prereg-r1`; results in `osf/methodology/v1_17/outputs/`) estimated, from v0.42's t4 answers on the three current models, that at 3 runs per cell a brand's per-model Presence has a standard error of about 0.040 (95% interval 0.037–0.043, n = 672 units), 0.050 for brands named in some answers but not all (n = 433), and that one question's reading is noisier (0.176 per run); one run's standard error is 0.069 (n = 672). These figures assume independent runs with the same variance as t4's three runs, which were collected on one day. They apply to the current arm with search off; for the search-on run the one-run figure (0.069) applies. By category size (v1.17 results note, "Runs needed, by category size"): the all-brand figure is much the same in t4's 16-brand and 24-brand categories (one run 0.069, three runs 0.040; below 0.05 needs 2 runs), but for brands named in some answers but not all, one run's standard error is 0.086 and staying below 0.05 needs 3 runs in the 16-brand category and 4 runs in the 24-brand categories.

**What this means for v0.40's category sizes.** Airlines (18 brands: 11 current, 7 ghosts) lie between t4's 16 and 24 brands, so at three runs the all-brand figure (about 0.040) is expected to hold, while brands named in some answers but not all are expected at about 0.050, on the 0.05 line rather than below it (four runs would be needed by the 24-brand figure). Banks (42 brands: 25 holders, 17 ghosts) are outside t4's range, so v1.17 gives no estimate for them; no figure is assumed. v0.40 keeps the three runs of design D7 (a fourth search-off run would be a design change for the pre-registrant, §9 item 6) and reports its own run-to-run standard error per arm, for all units and for units named in some answers but not all (§2.9 item 6), beside v1.17's figures. v1.17 has no legacy-arm run-to-run estimate, so v0.40's own figure is the only one for the legacy arm.

---

## §3 Brand registry

### §3.1 Construction and freeze

The registry was built mechanically by `osf/v40/scripts/build_registry_v0_40.py` from BTS T-100, the BTS On-Time marketing-carrier file and the FDIC Summary of Deposits and BankFind, under rules R1–R12, and frozen on 2026-11-12 (`registries/out/v0_40_registry_draft.md`, r3; decisions D1–D19 adopted by the pre-registrant on 2026-11-08 and D4 on 2026-11-09). Current units: airlines, 11 brands in 10 share units; banks, 25 holders. Ghosts: 7 airlines, 17 banks. Living-brand controls: Hawaiian and Sun Country (airlines), Discover (banks; see §3.2). Incumbent controls: American and Delta; Chase and Bank of America. The freeze re-check found no brand status change between 2026-11-08 and 2026-11-12. Every share, floor, window and gap is in `registries/out/` with sources; this pre-registration adds none.

### §3.2 The bank living-brand control: Discover switch — **DECIDED (a): Discover kept** (the pre-registrant, 2026-11-12, 6:57 am CT)

The freeze check found, dated before 2026-11-08, that Discover's deposit accounts are moving to Capital One: Capital One says "Your Discover checking account is becoming a Capital One checking account" (https://www.capitalone.com/updates/discover/checking/), and secondary reports place a migration date of 2026-08-23 for some savings accounts (registry draft r3, §5 item 5). The registry row's source still says the Discover brand is not going away. Because SVB moved to the ghosts (D6), Discover is the only bank living-brand control. One switch decides its role in both the probe build and the scorer: `DISCOVER_OPTION` in `build_probes_v0_40.py` (`--final` refuses to freeze the probe set while it is unset; the draft build stays byte-identical). **Decision:** version (a), by the pre-registrant on 2026-11-12, 6:57 am CT; `DISCOVER_OPTION = "a"` since 2026-11-13 (checked by `test_prelock_v0_40.py`). Version (b) and the candidate check below are kept as the record of the choice.

**Version (a), keep Discover (registered):** "The bank living-brand control is Discover, whose deposit accounts were being moved to Capital One during the study (§8, limitation 7). Discover is kept as a control in H_Flag, which is also reported without it (sensitivity S-Discover); the status answers about Discover are shown in full in the descriptives, because an answer that says its deposits now sit with Capital One may be correct."

**Version (b), replace Discover (not chosen):** "The bank living-brand control is [REPLACEMENT], chosen from the frozen registry's own material because Discover's deposit accounts were being moved to Capital One during the study. Discover's mentions still count toward the Capital One holder's share (D12); it is no longer a control."

Candidates for (b), all from the frozen registry's own material; the runner does not pick:
- **Merrill** (`bank_scan_class.csv`, CERT 27374, class "brand persists", D10): Merrill Lynch Bank USA merged into Bank of America on 2009-07-01 and the Merrill brand continues. Fits R10 (a living brand after a legal change); but it is a brokerage and wealth brand rather than a deposit-account brand, and its change predates every model cutoff by years.
- **Webster Bank** (registry draft r3, §5 item 5, D16): Santander completed its acquisition of Webster on 2026-08-20 and merged Webster Bank into Santander Bank, N.A.; both brands continue "for now" (SHUSA 8-K, Exhibit 99.1). Closest to Discover's role (recent legal change, retail deposit brand in use); but below the 0.5% floor (0.371% at SOD 2026), its change postdates every cutoff, and it may be retired as Discover is.
- **Fifth Third Bank** (`bank_scan_class.csv`, CERT 993, class "not an exit"): a charter consolidation in 2009 that kept the stem. A living retail brand with an internal legal change only; weakest fit, and the scan row itself says "verify FDIC record".

**Candidate check for (b), 2026-11-12 (runner; for the pre-registrant's decision; the switch is not set).** Test: no merger, acquisition or account migration under way or completed in 2025–26, and in Discover's size band by the registry's own measure (share of deposits; Discover 0.6439%, SOD 2024, `exits_and_controls.csv`; the registry defines no band, so shares are given as they stand).
- *Fifth Third Bank:* fails the merger test. Fifth Third completed its merger with Comerica on 2026-02-02 ("Fifth Third Completes Merger with Comerica to Become 9th Largest U.S. Bank", press release, 2026-02-02, https://www.nasdaq.com/press-release/fifth-third-completes-merger-comerica-become-9th-largest-us-bank-2026-02-02), with "full system and brand conversions … expected in the third quarter" (the release gives no year; whether the conversion has happened was not checked). Size: the Fifth Third holder is 1.2620% in `banks_current.csv`, about twice Discover's share.
- *Webster Bank:* fails the merger test. Santander completed its acquisition on 2026-08-20; Webster Bank is now "a division of Santander Bank, N.A.", and "Any future changes will be communicated well in advance" (Webster Bank newsroom, 2026-08-20, https://websterbank.com/about/newsroom/santander-expands-u-s-presence-with-completion-of-webster-acquisition; SHUSA 8-K as cited in the registry draft). Size: 0.371% at SOD 2026, below the 0.5% floor.
- *Merrill:* no merger, acquisition or account migration in 2025–26 was found (searched 2026-11-12; Financial Planning, 2026-01-14, https://www.financial-planning.com/news/merrill-trumpets-low-advisor-attrition-in-2025, reports team departures only); its legal change is Merrill Lynch Bank USA's merger into Bank of America in 2009. Size: the registry's only measure is Merrill Lynch Bank USA's 0.7645% at its 2009 exit (`bank_scan_class.csv`), close to Discover's 0.6439% but measured 15 years apart; today its deposits sit inside the Bank of America holder. It is a brokerage and wealth brand, not a deposit-account brand, and its change predates every model cutoff.
- *Runner's reading:* only Merrill passes the merger test, and it fits the role of a deposit-account brand changing status poorly. The runner recommends (a), keeping Discover with limitation 7 and S-Discover; if the pre-registrant prefers (b), Merrill is the only candidate of the three that passes the test.

Either version keeps 94 probes and the call count unchanged.

---

## §4 Probes and acquisition

### §4.1 Probe set (94 probes; verbatim in `prereg/probes_v0_40.md`)

Built by `osf/v40/scripts/build_probes_v0_40.py` from the frozen registry, unchanged since the draft (step 1, Pablo, 2026-11-09: no feedback, draft kept): per category 6 generic, 6 need-based and 4 Census-region recommendation probes (32), and one recognition (K) and one status (S) probe for each of the 24 ghosts, 3 living-brand controls and 4 incumbents (62). One user turn, no system prompt; recommendation probes name no brand; collision names carry the FDIC disambiguator (D11). `prereg/probes_v0_40.json` sha256 `93aee03f655cb8c4c6b04211e941b854bd921c3dbd31a9f5ffbaa91249be38ca`; `probes_v0_40.md` sha256 `45f1f3871f6fb60cd39840253cc6834fb918aadb160fd489c260ba50876bc92f`. The final build (`--final`, after the Discover switch, §3.2) rewrites the file's status and call-count fields (and, under (b), the two Discover probes); the lock manifest then carries its new checksum and `acquire_v0_40.py` the same value.

### §4.2 Design (registered: D7 of §6.3)

| Arm | Models | Condition | Runs | Probes | Calls |
|---|---|---|---|---|---|
| Legacy | M1–M6 | search off | 3 | 94 | 1,692 |
| Legacy, extra pass | M5X (Gemini 2.5 Flash, v0.39 setting) | search off | 1 | 94 | 94 |
| Current | C1–C3 | search off (S0) | 3 | 94 | 846 |
| Current | C1–C3 | search on (S1) | 1 | 63 (32 recommendation + 31 status) | 189 |
| **Total** | | | | | **2,821** |

The probe set as frozen counted 37 calls per probe (3,478 calls: search on with 3 runs on all 94 probes). At the recorded costs that design is estimated at $191.14 central, above the $100 cap, so search on is reduced to one run on the probes that carry its hypothesis (§6.4). Under D7 every probe gets 28 calls (legacy 6 models × 3 runs + 1 M5X pass = 19; current 3 models × 3 runs search off = 9) and the 63 recommendation and status probes 3 more (current 3 models × 1 run search on): 28 × 94 + 3 × 63 = 2,632 + 189 = 2,821, i.e. 31 calls per recommendation or status probe and 28 per recognition probe. The final build writes this count into the probe-set header (`build_probes_v0_40.py --final`).

### §4.3 Panel

**Legacy arm** (fixed since v0.17): Claude Opus 4.5 (M1), Claude Sonnet 4.5 (M2), GPT-4o (M3), GPT-4o mini (M4), Gemini 2.5 Flash (M5), Gemini 2.5 Flash-Lite (M6); lifecycle and cutoffs in `registries/out/model_cutoffs.csv` (vendor pages, 2026-11-08). Gemini runs on the Developer API with the v0.39 project (D18). Each call logs the snapshot it returns. Claude Sonnet 4.5 is called with the old Anthropic organization's API key (`ANTHROPIC_API_KEY_LEGACY`, the organization that served v0.42's Sonnet 4.5 coding judge): the new organization does not serve this model (all 24 of its calls in the pre-lock check's first run, 2026-11-13, returned 404 "model: claude-sonnet-4-5", with no charge); the request is unchanged, and each record names the key it used (`api_key_env`).

**Current arm: each provider's newest generally available flagship, checked on the vendors' pages on 2026-11-12.** Restricted and pre-release models are excluded.
- **C1 Claude Fable 5.2** (`claude-fable-5-2`). Anthropic, *Models overview* (https://platform.claude.com/docs/en/about-claude/models/overview.md, opened 2026-11-12): the latest-models table lists Claude Fable 5.2 "For demanding reasoning and long-horizon agentic work", $8 / $40 per MTok, reliable-knowledge and training-data cutoff Jun 2026, retirement "Not sooner than November 9, 2027", and says "Batch API requests are 50% off". Claude Mythos 5.2 is marked "limited availability" and is excluded. *Re-check 2026-11-12 (11:10–11:20 UTC), same URL:* unchanged; the latest-models table still lists Claude Fable 5.2, Claude Opus 5.5, Claude Sonnet 5.5 and Claude Haiku 5.5, no model newer than Fable 5.2 is listed, and Claude Mythos 5.2 is still marked "limited availability" ("Available only to organizations verified through Anthropic's verification programs"). **Claude Fable 5.2 stays.** The same page says to "start with Claude Opus 5.5 for most workloads" and to use Fable 5.2 for demanding reasoning; v0.42 (t4) used Fable 5.2 as Anthropic's flagship under the one-flagship-per-provider rule, and v0.40 follows it (alternative: Opus 5.5, §6.3 D5/D6; **PENDING PABLO**). Sent through the Message Batches API (same request parameters as a synchronous call).
- **C2 GPT-6 Astra** (`gpt-6-astra`). OpenAI, model page (https://developers.openai.com/docs/models/gpt-6-astra, opened 2026-11-12): "Our most capable model for the most demanding work"; knowledge cutoff April 30, 2026; $10.00 / $50.00 per 1M tokens; the page gives no preview or restricted status for the API model (its Google Cloud listing is "Private preview"). OpenAI's pricing page (https://developers.openai.com/api/docs/pricing) also lists `gpt-6.1-sol` and `gpt-6.1-terra` without ranking them; OpenAI's GPT-6.1 Terra announcement page (https://openai.com/index/introducing-gpt-6-1-terra/) could not be fetched (client error), so whether Terra is positioned above Astra was not verified from the vendor. Synchronous.
  *Re-check 2026-11-12 (11:10–11:20 UTC).* The Terra announcement page again could not be fetched (client error). OpenAI's GPT-6.1 Terra model page (https://developers.openai.com/docs/models/gpt-6.1-terra, opened 2026-11-12) was read: "A fast, efficient model for visual reasoning, precise computer use, and clear, natural writing"; knowledge cutoff Jun 01, 2026; $1.00 / $5.00 per 1M tokens; no preview or restricted label for the API (its Google Cloud listing is "Private preview"); it makes no comparison with Astra. The pricing page (same URL, opened 2026-11-12) lists gpt-6-astra ($10.00 / $50.00), gpt-6.1-sol ($2.00 / $10.00), gpt-6.1-terra ($1.00 / $5.00) and gpt-6-luna ($0.10 / $0.50) together under the heading "Flagship models", without ranking them. The GPT-6 Astra page (opened 2026-11-12) still reads "Our most capable model for the most demanding work" and names no successor. Terra is therefore generally available in the API by its own page, but nothing on OpenAI's pages places it above Astra, and Astra's page calls Astra OpenAI's most capable model: **GPT-6 Astra stays** as OpenAI's flagship; design, cost estimate and budget unchanged. (A trade-press report, not a vendor source, describes Terra as the mid-tier of OpenAI's Luna, Terra, Sol and Astra tiers: Silicon Report, 2026-10-26, https://www.siliconreport.com/openai-releases-gpt-6-1-terra-at-half-the-api-price-of-predecessor.)
- **C3 Gemini 4 Argon** (`gemini-4-argon`). Google, *Latest model* (https://ai.google.dev/gemini-api/docs/latest-model, opened 2026-11-12): "our latest, most capable model", available through the Gemini API and Google AI Studio; $2 / $10 per 1M tokens through November 30, 2026, then $4 / $20; Gemini 4 Carbon is not listed there. **Gemini 4 Carbon is excluded:** its Google Cloud page (https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/4-carbon, opened 2026-11-12) gives "Launch stage: GA" and "Release date: November 10, 2026", but also "Gemini 4 Carbon is available to verified enterprise customers in select regions", i.e. restricted access. Synchronous.
  *Re-check 2026-11-12 (11:10–11:20 UTC).* (i) The *Latest model* URL above now redirects (HTTP 302) to https://aistudio.google.com/docs/latest-model, whose readable text names no model; the earlier quotation could not be re-read. (ii) Google's Gemini API changelog (https://ai.google.dev/gemini-api/docs/changelog, opened 2026-11-12): "Gemini 4 Argon (`gemini-4-argon`) generally available (GA)", 2026-10-13, "our most capable model built for complex coding, agentic, math, and science tasks"; no entry mentions Gemini 4 Carbon and there is no November 2026 entry. (iii) The Gemini 4 Carbon Google Cloud page (same URL, opened 2026-11-12, "Last updated 2026-11-11 UTC") still reads "Launch stage: GA", "Release date: November 10, 2026" and "available to verified enterprise customers in select regions". (iv) **Changed since the r1 check:** Google's Gemini API pricing page (https://aistudio.google.com/docs/pricing, opened 2026-11-12) now lists `gemini-4-carbon`, "Our most capable reasoning model, built for complex software engineering", at the same Standard, Batch and Priority prices as Gemini 4 Argon (not on the Free tier), and describes Argon as "Our efficient Gemini 4 frontier reasoning model". A price listing is not a statement of general availability, and Google's own availability statements (Cloud page, changelog) still restrict Carbon, so **Gemini 4 Argon stays** under the standing rule; design, cost estimate and budget unchanged. **Flagged for the coordinator:** if Google states that Gemini 4 Carbon is generally available in the Gemini API before the lock, Carbon would replace Argon under the same rule (same listed prices; the cost basis would need Carbon's recorded token usage).

### §4.4 Decoding and call policy

- **Legacy arm:** temperature 0.0, max output 2,048 tokens, single user turn, no system prompt; call functions copied verbatim from `acquire_v0_39.py` (checked by test). **Gemini 2.5 Flash (M5):** thinking budget 0 for its three runs (under the v0.39 setting, answers ending at the 2,048-token cap were expected; v0.39 pre-registration §6.6); plus one pass per probe at the v0.39 setting (M5X: provider-default thinking), reported, never tested.
- **Current arm:** provider defaults for temperature, top_p, top_k and reasoning effort (none is sent; checked at dry run); **max output 16,384 tokens**; no system prompt. S1 tools as v0.39 (Anthropic `web_search_20250305`, max 5 uses, US location; OpenAI `web_search`, medium context, US location; Google Search grounding). An Anthropic `pause_turn` is continued once with identical tools.
- Transient errors are retried up to 3 attempts; an empty answer is re-sent once; every attempt is one raw line with its usage and cost.

### §4.5 Order and windows

Blocks in order, models in parallel within a block: legacy runs 1, 2, 3; the M5X pass; current S0 runs 1, 2, 3; current S1. **All search-on calls are sent in the last block, inside one window:** no new S1 request later than 24 hours after the first S1 request. No request after 2026-11-21 23:59:59 CT. One paid collection at a time on the machine (guard copied from v0.42).

### §4.6 Acquisition artefact

`osf/v40/data/v40_raw.jsonl` (append-only, one line per attempt: prompt, answer, served snapshot, finish reason, tokens, searches, sources, citations, cost), `v40_budget_state.json`, `v40_batches.jsonl` (Message Batches journal).

### §4.7 Length-limit stop rule inside the collection (added 2026-11-13)

Programme rule of 2026-11-12 (the pre-registrant, 11:36 pm CT): no answer may stop at the output-token limit before naming a brand. Background: in v0.38 and v0.39 the legacy arm's Gemini 2.5 Flash, at the 2,048-token limit with the provider's default thinking, ended 19 of 22 and 26 of 30 answers at the limit, 5 and 15 of them before naming any registry brand; the current arm at 16,384 tokens had no answer at the limit in v0.39 (180 answers) or in v0.42's t4 (876 answers) (truncation audit of 2026-11-12, branch `truncation-audit`, `analysis/truncation_audit/results/newer_collections.csv`). v0.40 already sets Gemini 2.5 Flash's thinking budget to 0 for its three runs (§4.4); this rule checks every answer as it arrives.

- **What is checked, and when.** Every answer, as soon as its raw line is written: for the synchronous models before that model's next request; for Claude Fable 5.2 when each Message Batch's results are written, so the rule acts from its next batch. Per answer: *at the limit* means the provider's finish reason is its length stop (Anthropic `max_tokens`; OpenAI `length` or `incomplete:max_output_tokens`; Google `MAX_TOKENS`) or, when no finish reason is recorded, output tokens (Google: plus thinking tokens) reach the limit (2,048 legacy, 16,384 current); *names a brand* means the coder's own matcher (§5.2) finds at least one registry brand in the answer as the primary coding counts it (a bare ambiguous alias, D11, does not count: "United" in "United States" names no brand); *cut before the first brand* means at the limit with no brand. An empty first answer that stopped at the limit and was re-sent (§4.4) also counts as cut before the first brand; its finish reason is kept in the raw line.
- **Trigger.** One answer cut before the first brand, in any block or condition, from any model slot except M5X (below).
- **Action.** That model's slot is paused at once: no further request for it, in any block or condition; the other models go on. The trigger is written to `data/v40_stoprule.jsonl` and reported to the pre-registrant the same day with the answer's call ID, finish reason and token counts; the run ends with exit code 7. The pause holds across restarts until the pre-registrant decides; his decision is journaled (`acquire_v0_40.py --resume-model SLOT NOTE`) and is a DEVIATIONS entry.
- **Handling, declared now.** (i) The triggering answer, and any other answer cut before the first brand, stays in the raw file and is treated as missing in every test and descriptive (§5.7, §5.9), never as an answer that names no brand. (ii) The pre-registrant either resumes the model unchanged (the rule stays active, and a new trigger pauses it again) or leaves it paused; a model left paused is treated as unavailable for its unsent calls (§7.1): the tests run on the other models, denominators shrink, and each test is also reported without that model. (iii) No call setting is changed during the collection (no higher limit, no new thinking setting); answers under a changed setting would form a separate arm, reported apart and never pooled with the registered cells.
- **M5X.** The extra Gemini 2.5 Flash pass at the v0.39 setting is reported, never tested, and its answers at the 2,048-token limit are expected (§7.6). Its answers are assessed and journaled but do not pause it (**PENDING PABLO**, §9 item 7).
- **Implementation.** `scripts/stoprule_v0_40.py`, called by the writer of `acquire_v0_40.py`; tested with fake providers in `scripts/test_prelock_v0_40.py` (no call sent).

### §4.8 Pre-lock check (declared non-acquisition step before the lock; added 2026-11-13)

- **Rule.** The study is not locked while any model, under the study's own call settings, returns an answer that stops at the length limit before naming a brand (programme rule of 2026-11-12).
- **Questions, and why.** v0.39's published probes (commercial coffee roasters; its pre-registration, probe set, registry and answers are public on OSF `ec6wh` → `v39`): the 24 probes that ask for or name a brand (six café-roaster recommendations G1–G6, six under an infrastructure constraint C1–C6, six production-roastery recommendations R1–R6, and six questions naming one roaster K1–K6), verbatim from `osf/v39/prereg/probes_v0_39.json`; its six frame probes ask for no brand and are not used. No v0.40 probe is sent, so no study data is collected early. v0.39 is also where the problem was observed (Gemini 2.5 Flash at its v0.39 setting: 26 of 30 answers at the limit, 15 before the first brand, §4.7), so the check tests the study's settings on questions that have produced cut answers before. A brand is a v0.39 registry brand found by v0.39's own matcher (`score_v0_39.Coder.brand_matches`).
- **Calls per model.** Through `acquire_v0_40.py`'s own call functions (same limits, thinking settings, temperature, tools and SDK calls; Claude Fable 5.2 through the Message Batches API), one answer per probe: search off, the 24 probes for each of M1–M6, M5X and C1–C3 (24 calls per model setting, 240); search on, the six G probes for each of C1–C3 (6 calls per model, 18). 258 calls.
- **Cost.** From the study's own per-call basis (§6.2, `prereg/cost_estimate_v0_40.txt`, at the prices of §6.1): $5.91 central and $14.93 high (sum of 90th percentiles): legacy arm $0.54 / $2.76, current arm search off $1.85 / $4.96, search on $3.53 / $7.21. The check's own guard reserves each request's worst case and stops before its spend could pass $20 (the high estimate plus one worst-case search-on request). Its recorded spend counts toward the $100 cap and the $80 pause of this study (§6.5); with D7 (§6.3) the central total is $62.40 + $5.91 = $68.31.
- **Verdict and consequence.** BLOCKED if any answer of M1–M6 or C1–C3 is cut before the first brand, or records neither a finish reason nor output tokens: the study is not locked, and the remedy (for example a thinking budget, as M5 has, or a higher limit) is the pre-registrant's decision, a new revision of the settings followed by a repeated check. INCOMPLETE while any planned call has no answer (the check resumes). PASS otherwise. Answers cut after a brand, and answers whose thinking reaches half the limit, do not block; they are listed in the record and handled as §5.9. M5X's answers are assessed and reported but cannot block (§4.7; §9 item 7). `acquire_v0_40.py --collect` refuses to start unless the record says PASS.
- **Record and script.** `prereg/prelock_check_v0_40.jsonl` (the answers, in the study's raw format) and `prereg/prelock_check_v0_40.json` (verdict, counts per model setting, spend), deposited with this pre-registration. `scripts/prelock_check_v0_40.py`: `--dry-run` prints the 258 planned calls and their cost without any network call; `--run` sends them (paid); `--evaluate` assesses the record. Tested with fake providers in `scripts/test_prelock_v0_40.py`. **Run 2026-11-13 by the runner: PASS.** 258 of 258 planned calls answered (sent 08:39–08:53 UTC; Claude Sonnet 4.5's 24 calls and one GPT-6 Astra call, which had failed without an answer, re-sent 08:53–08:58 UTC after the key routing of §4.3 and the import fix in the change log). No answer of M1–M6 or C1–C3 stopped at its limit before naming a brand. Gemini 2.5 Flash (M5, thinking budget 0) stopped at the 2,048-token limit in 6 of 24 answers, each after naming a brand (kept and flagged, §5.9). M5X (v0.39 setting; exempt, §9 item 7) stopped at the limit in 19 of 24 answers, 8 of them before any brand, and spent half the limit or more on thinking in 21. No other model setting reached its limit; the largest thinking was Claude Fable 5.2's, 2,252 tokens search off and 4,355 search on, of 16,384. Recorded spend $4.73, counted toward the $100 cap (§6.5).

---

## §5 Coding and analysis plan

### §5.1 Coder

Coding is automated and rule-based (`score_v0_40.py`); no LLM is used as coder or judge. If a later revision adds an LLM coder or judge, its reply rule is fixed before the lock and tested on recorded replies: exactly one complete JSON object with the required keys counts, and any text around it is ignored (programme rule of 2026-11-12, after v1.15, where Claude Opus 5.5 put a sentence before its JSON object on 4.2% of first tries).

### §5.2 Aliases and collisions

Aliases are those of the frozen registry: `registries/out/exits_and_controls.csv` (ghosts and controls; old and new names) and the `aliases` columns of `airlines_current.csv` and `banks_current.csv` (current units; D12: Marcus counts for Goldman Sachs, Discover for Capital One, "TD" alone does not count). Matching is whole-word and case-sensitive; the longest alias wins. These bare aliases are coded **ambiguous** (D11) and are excluded from the primary tests: American, United, Delta, Frontier, Spirit, Continental, Northwest, Breeze, Southwest, Alaska, Commerce Bank, Union Bank, Signature Bank, Discover, Sovereign, Compass Bank, ATA, Harris Bank, National City. Every Presence result is also reported with ambiguous mentions included (sensitivity S-Ambig). Brands below the floor (D16) are not registry units and are counted as "other" in the descriptives only.

### §5.3 Gone-flag (±150 characters)

A mention is gone-flagged when the locked, case-insensitive lexicon in `score_v0_40.py` (`GONE`; for example "no longer", "defunct", "ceased operations", "merged into/with", "acquired by", "now part of", "rebranded", "formerly", "failed", "shut down", "bankrupt") occurs within 150 characters before or after the mention. The lexicon is not changed after the lock; a change found necessary is a DEVIATIONS entry, with verdicts reported both ways.

### §5.4 Old versus new name

For each ghost mention the coder records whether the successor's name (registry `successor` column, e.g. "Truist" for SunTrust and BB&T) occurs within the same ±150-character window (descriptive 3).

### §5.5 Declared audit sample

Drawn after collection with seed 4040, before any verdict is read: 100 recommendation answers that contain at least one ghost or control mention (all of them if fewer), stratified by arm and condition, and 100 status (S) answers, stratified by arm, condition and role (ghost, control, incumbent). The analyst is the pre-registrant (**PENDING PABLO**: or a delegate he names); he codes each sampled mention for subject, ambiguity, gone-flag and successor name, blind to the coder's codes. Agreement is reported per field (percent agreement and Cohen's κ). Threshold: κ ≥ 0.80 on the gone-flag. Below it the coder is not changed: H_Flag, H_Afterlife and H_Search are reported as computed and marked "coder reliability below threshold", with the analyst-coded rates of the sample beside them.

### §5.6 Sensitivities (reported beside each verdict; no verdict changes)

S-Ambig (all six tests with ambiguous mentions included in Presence and unit counts; the status-answer flag rule of §2.1 already reads every mention of the probe's subject, ambiguous or not, so H_Flag and H_Search are identical under S-Ambig by construction); S-Legal (legal-date gaps, `gap_legal_m`, for H_Afterlife and H_Decay; a pair without a legal gap drops out; North Fork drops out, SVB changes sign, D3, D6); S-Operating (airline part of H_Reinforce and H_Amplify on the airline operating share, `operating_share_pct`, with Delta as leader, D1); S-SunCountry (airline part of H_Reinforce and H_Amplify with Sun Country inside Allegiant at the registry's `holder_share_alt_pct`, 2.6673%, D2); S-D4 (banks without Morgan Stanley, Charles Schwab and UBS, D4); S-Discover (H_Flag without the bank living-brand control, §3.2); S-Arm (each test's statistic per arm: H_Reinforce to H_Flag on the legacy models M1–M6 alone and on the current models C1–C3 alone; H_Search has the current arm only). *(Scope of each sensitivity written out 2026-11-12.)*

### §5.7 Missing data

A call that fails after its attempts is missing; denominators shrink. A test whose evaluable units fall below its floor is UNDETERMINED.

### §5.8 Scoring artefact and tests

`python3 osf/v40/scripts/score_v0_40.py` writes `osf/v40/data/v40_mentions.csv` and `osf/v40/v40_verdicts.json` and is run once. `test_score_v0_40.py` checks the coder and the exact tests and scores two synthetic worlds built from the frozen registry and probe set: one where every effect is present by construction (all six CONFIRMED) and one where none is (H_Reinforce, H_Amplify, H_Afterlife, H_Flag and H_Search FALSIFIED; H_Decay UNDETERMINED at its floor). The same file tests every sensitivity of §5.6 and descriptives 3–9 of §2.9 on synthetic data (41 checks, all pass, 2026-11-12), and since 2026-11-13 the handling of §5.9 (S-Length, missing answers cut before the first brand, descriptive 10: 44 checks, all pass). Record: `prereg/test_score_v0_40.txt`. The stop rule, the pre-lock check and the Discover switch are tested in `test_prelock_v0_40.py` (54 checks, all pass, 2026-11-13; record `prereg/test_prelock_v0_40.txt`).

### §5.9 Answers at the length limit or with heavy thinking (declared handling; added 2026-11-13)

Every answer carries the flags of §4.7, computed by `stoprule_v0_40.assess` from its raw line:
1. **Cut before the first brand** (at the limit, no registry brand counted by the primary coding): triggers the stop rule (§4.7) and is treated as missing (§5.7), never as an answer that names no brand. An empty first answer cut at the limit also triggers the rule; the answer re-sent under §4.4 is coded as recorded.
2. **Cut after a brand** (at the limit, at least one registry brand): kept and coded as recorded; the brands named before the limit count.
3. **Thinking at half the limit or more** (at least 1,024 of 2,048 tokens in the legacy arm; at least 8,192 of 16,384 in the current arm). Thinking tokens are the provider's own count (Google `thoughts_token_count`, OpenAI `reasoning_tokens`). Claude Fable 5.2 is called with Anthropic's defaults and its usage gives no separate thinking count (thinking is billed inside output tokens), so its total output tokens are used as an upper bound and the flag errs toward flagging. Calls that send no thinking setting to models without default thinking (Claude Opus 4.5, Claude Sonnet 4.5, GPT-4o, GPT-4o mini) count zero. A flagged answer that ended normally is a complete answer: kept and coded as recorded, never re-sent or replaced.
4. **Sensitivity S-Length:** every test is also reported without the answers of items 2 and 3, beside its verdict; no verdict changes (as §5.6).
5. The counts of items 1–3 per model, arm and condition are reported with the descriptives; M5X's are reported as its expected behaviour (§7.6).

---

## §6 Budget

### §6.1 Cap and prices

At most $100 of paid model calls for this paper, hard cap (programme rule of 2026-11-10), with a pause at $80. Prices from the vendors' pages opened 2026-11-12 (US$ per 1M tokens, input / output): Claude Fable 5.2 $8 / $40 (Batch API 50% off), Claude Opus 5.5 $4 / $20, Claude Opus 4.5 $5 / $25, Claude Sonnet 4.5 $3 / $15 (Anthropic models overview); GPT-6 Astra $10 / $50 (model page), GPT-4o $2.50 / $10.00, GPT-4o mini $0.15 / $0.60 (model pages), web search $10.00 per 1,000 calls (OpenAI pricing page); Gemini 4 Argon $2 / $10 through 2026-11-30, Gemini 2.5 Flash $0.30 / $2.50, Gemini 2.5 Flash-Lite $0.10 / $0.40, output including thinking, grounding $14 per 1,000 for Gemini 3 and newer (Google pricing page, https://aistudio.google.com/docs/pricing; the free allowances are not assumed). Anthropic web search: $10 per 1,000 searches (Anthropic pricing page as quoted in v0.42's budget module, opened 2026-11-10; not re-opened for this draft).

### §6.2 Basis (recorded usage, not guesses)

Current arm: the recorded cost of every t4 call of v0.42 (collected 2026-11-11, the same three models and settings; `cost_usd` per raw line, failed attempts included), per model, phase and condition. Recommendation probes use t4's category questions; K and S probes use t4's brand questions with search off and t4's category questions with search on (t4 asked no brand question with search on; conservative). Claude Opus 5.5 (alternative only): v0.39's recorded tokens. Legacy arm: v0.39's recorded tokens per model at today's prices; the "high" case puts every legacy answer at the 2,048-token cap. Central = mean cost per completed call; high = 90th percentile for every call. Script: `scripts/cost_estimate_v0_40.py`; output `prereg/cost_estimate_v0_40.txt`.

### §6.3 Designs (US$, central / high)

| Design | Calls | Central | High |
|---|---|---|---|
| D1 frozen probe set: S0 ×3 and S1 ×3 on all 94 probes, Fable 5.2 (Batch API) | 3,478 | 191.14 | 420.75 |
| D2 = D1 with S1 ×1 run | 2,914 | 80.62 | 194.75 |
| D3 = D1 with S1 ×3 on the 32 recommendation probes only | 2,920 | 81.80 | 197.16 |
| D4 = D1 with S1 ×1 on the 32 recommendation probes only | 2,728 | 44.17 | 120.22 |
| D5 = D1 with Claude Opus 5.5 (synchronous) instead of Fable 5.2 | 3,478 | 173.68 | 359.14 |
| D6 = D5 with S1 ×1 run | 2,914 | 76.97 | 169.46 |
| **D7 (registered) = D1 with S1 ×1 on the 32 recommendation + 31 status probes** | **2,821** | **62.40** | **157.49** |

D7 by cell (central): legacy arm $5.53 (of which Claude Opus 4.5 $2.03); Fable 5.2 S0 $6.01, S1 $11.01; GPT-6 Astra S0 $11.78, S1 $24.77; Gemini 4 Argon S0 $2.04, S1 $1.26. GPT-6 Astra with search on costs $0.39 per call at t4 (central), the largest single cost. The pre-registrant's estimate of about $51 on 2026-11-10 predates t4's recorded usage and the choice of Fable 5.2.

### §6.4 Design trade-off

Search on with three runs on all probes (D1) cannot be afforded. D7 keeps every confirmatory search-off test at three runs (v1.17: about 0.040 per model-brand Presence) and gives the search-on condition one run on the 63 probes that carry H_Search and the search-on descriptives (recommendations and status); the 31 recognition probes are asked without search only. The cost is precision at S1 (one run: about 0.069, §2.10) and no search-on recognition answers. The high case ($157.49) sums each call's 90th percentile and is not a forecast; the guard (§6.5) bounds actual spend. Order protects the tests: the legacy arm and every search-off run come first (central about $25.4), so a budget stop can only shorten the search-on block. Cheaper alternatives if the pre-registrant prefers them: D4 ($44.17; H_Search would lose its status probes and become UNDETERMINED by construction) or D6 with Opus 5.5 ($76.97).

### §6.5 Guard (from actual usage)

`budget_v0_40.py` (fork of v0.42's guard): spend is computed from the recorded usage of every billed request; each request's worst case is reserved before it is sent; no new request once spend reaches $80 until the pre-registrant approves (`--approve-past-80`); no request that could take spend past $100. Spend includes the recorded spend of the pre-lock check (§4.8), which `acquire_v0_40.py --collect` carries into the guard (added 2026-11-13). If the guard stops collection inside the search-on block, H_Search is UNDETERMINED unless its parts can be evaluated on the complete cells, and the shortfall is a DEVIATIONS entry.

---

## §7 Contingencies

- **§7.1 Model unavailable.** Logged; analyses run on the remaining models and denominators shrink. If Claude Opus 4.5 or Claude Sonnet 4.5 is retired before the legacy arm is complete, the arm is reported without it; it is not replaced.
- **§7.2 Search behaviour in S1.** An S1 answer in which the model chose not to search is kept as recorded; not searching is part of the condition. Tool errors are retried as transient errors; a persistent failure is a missing cell.
- **§7.3 Manipulation check fails.** As §2.8.
- **§7.4 Budget.** As §6.5. A pause at $80 waits for the pre-registrant; nothing is sent past $100.
- **§7.5 Changes.** Any change to probes, registry, coding or thresholds before acquisition is a new revision (`v0.40-prereg-r2`); after acquisition, a DEVIATIONS entry. Tags are additive-only.
- **§7.6 Known truncation.** Answers of the M5X pass that end at the 2,048-token cap are expected and are not a deviation. (2026-11-13: they are assessed by the stop rule but do not pause M5X, **PENDING PABLO**, §9 item 7; they are counted as §5.9.)

---

## §8 Limitations

1. **One market, one language, two categories.** US airlines and US retail banks, asked in English; the findings describe these models' answers to these questions in November 2026.
2. **One collection window.** Answers drift between model versions and days; v1.17's precision figures rest on runs collected on one day (§2.10).
3. **Search on is thin.** One run on 63 probes (§6.4); each provider decides whether and what to search, and the search trace is recorded but not controlled.
4. **Rule-based coding.** The gone-flag lexicon can miss paraphrases ("now flies as part of Alaska") and can flag living brands whose answers mention a merger they survived (Hawaiian, Sun Country, Discover). The declared audit (§5.5) measures this; the coder is not tuned after the lock.
5. **Cutoffs are vendor-published and month-level** (R11). Claude Fable 5.2 is assigned Claude Opus 5.5's gap rows because Anthropic gives both a Jun 2026 training-data cutoff; any difference within that month is not resolved.
6. **Pairs are not independent.** Ghost × model pairs share ghosts, and answers share probes and runs; the exact tests treat them as independent units, and per-ghost and per-model results are reported beside each test.
7. **The bank living-brand control** (version (a), decided by the pre-registrant on 2026-11-12, §3.2). Discover's deposit accounts were being moved to Capital One during the study (Capital One: "Your Discover checking account is becoming a Capital One checking account"), so the only bank living-brand control was itself changing status; H_Flag is reported with and without it.
8. **Share measures.** AI share counts answers that name a unit, not rank or prominence. Brokerage-sweep holders enter by the deposit rule (D4); near-floor brands such as USAA are not units (D16) and will be named often.
9. **Legacy decoding.** The legacy panel runs at temperature 0; three runs per cell may be near-identical, so its run-to-run variation is measured, not assumed.
10. **No buyer persona.** Every question is asked without a persona or any description of the asker (no system prompt; §4.4), so the scores describe answers to persona-free questions. Outside audits find that a stated buyer persona changes which brands are recommended: category leaders stayed about 80% the same across personas, while mid-market brands swapped up to 75% of the recommended set (Jack, Lehman, Maloney and Xu, arXiv 2605.30207, May 2026; 2,000 runs on one day; authors at Unusual); and U.S.-developed Gemini and GPT models favoured American entities, a pattern that persisted across personas (Rienecker et al., "Auditing Preferences for Brands and Cultures in LLMs" (ChoiceEval), arXiv 2603.18300, March 2026). Whether the results hold for questions asked with a persona is not tested here; no test is added.

---

## §9 Decisions for the pre-registrant (before the lock)

1. **Discover switch (§3.2, §8 item 7): DECIDED (a)**, keep Discover with the limitation (the pre-registrant, 2026-11-12, 6:57 am CT; applied 2026-11-13: `DISCOVER_OPTION = "a"` in `build_probes_v0_40.py`, §3.2 and §8 item 7 worded for (a), checked by `test_prelock_v0_40.py`). The options were (a), or (b) replacing it with one of Merrill, Webster Bank or Fifth Third Bank; the runner's check of 2026-11-12 (§3.2) had found that Fifth Third and Webster fail the no-merger test and recommended (a).
2. **Search-on design (§6.3–6.4).** Default D7 (search on, one run, recommendation and status probes; $62.40 central). Alternatives: D4 ($44.17) or D6 with Opus 5.5 ($76.97).
3. **Anthropic's current model (§4.3).** Default Claude Fable 5.2 through the Message Batches API, as v0.42. Alternative: Claude Opus 5.5, the model Anthropic recommends "for most workloads" and the current arm of v0.38–v0.39.
4. **OpenAI's current model (§4.3).** Default GPT-6 Astra ("Our most capable model" on its own page). Re-checked 2026-11-12: Terra's model page is readable and shows it generally available in the API, but no OpenAI page ranks it above Astra, and Astra's page still calls Astra "Our most capable model"; Astra stays under the standing rule (announcement page still unreadable). No decision needed unless OpenAI ranks Terra above Astra before the lock.
5. **Audit analyst (§5.5).** Default the pre-registrant; or a delegate he names.
6. **Runs per cell (§2.10), optional.** Default three search-off runs (D7). v1.17 puts brands named in some answers but not all at about 0.050 at three runs, and 4 runs are needed below 0.05 in 24-brand categories; a fourth search-off run would be a design change with its own cost estimate (not computed).
7. **M5X and the length rule (§4.7, §4.8), PENDING PABLO.** Default: the extra Gemini 2.5 Flash pass at the v0.39 setting (reported, never tested; its answers at the 2,048-token limit are expected, §7.6) is assessed and reported but neither pauses the collection nor blocks the lock. Alternatives: apply the rule to M5X as to every other model (in v0.39 its setting cut 15 of 30 answers before the first brand, so the pre-lock check would be expected to block the lock), or drop the M5X pass (94 calls, $0.45 central). *Pre-lock check, 2026-11-13:* M5X stopped before any brand in 8 of its 24 answers, so applying the rule to M5X would block the lock; under the default the check passes.
8. **Fable 5.2 technical check (header), optional.** The pre-lock check (§4.8) sends Claude Fable 5.2 the study's own batch requests, with search off and on; the pre-registrant may let it stand in for the separate Fable 5.2 technical check (default: both are run).

Done by the runner on 2026-11-13: the length-limit stop rule (§4.7); the pre-lock check (§4.8; its dry run gave 258 calls, $5.91 central, $14.93 high, `prereg/prelock_check_dry_run_v0_40.txt`; run later on 2026-11-13: PASS, $4.73, `prereg/prelock_check_v0_40.json`); the declared handling of §5.9 in `score_v0_40.py` (answers cut before the first brand are missing; S-Length; descriptive 10); the guard's carry-over of the check's spend (§6.5); the Discover switch set to (a) (item 1). Tests are mock only: `test_prelock_v0_40.py` 54 of 54, `test_score_v0_40.py` 44 of 44, `test_acquire_v0_40.py` 21 of 21 (18 before the key routing).

Done by the runner on 2026-11-12: a scorer fix, the airline current units are now the 10 share units of §2.1 (Hawaiian inside Alaska at the summed brand share 8.5110%, R8), where the first r1 scorer had kept Hawaiian as an eleventh unit on its partial-window brand share; the sensitivities of §5.6 and descriptives 3–9 of §2.9 in `score_v0_40.py`, with synthetic tests (§5.8); the conflict-of-interest screen of the registry (DEVIATIONS Entry 0); the vendor re-check of the current arm (§4.3: no change; Gemini 4 Carbon flagged); the D7 call count in the final-build header (§4.2); v1.17's result by category size (§2.10). Before the lock, by the runner: the Fable 5.2 technical check (header; not run, needs the coordinator's approval at its cost); the final probe build after item 1, with its checksum in the manifest and in `acquire_v0_40.py`; the refreshed lock manifest (scripts changed on 2026-11-12); the anchor file; and the personal-details fix of the older commits before the first push.

---

## §10 Declarations

## Conflict of interest {-}

The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. Samsung does not compete in US airlines or US retail banking; banking has an adjacency through Samsung Wallet, which is disclosed here. The programme's record from the v0.62 pre-registration reads: "Cheil Worldwide, a marketing company of the Samsung group in which Samsung Electronics holds 28.43%, or its agency Iris has done advertising, public-relations or search-marketing work for five registry brands: Chevrolet (for GM Korea, 2017), BMW (UK consumer public relations, 2018), Bentley (experiential agency of record in the Americas from 2021), Jack Daniel's (UK digital agency from 2022, since replaced) and Eucerin (search marketing for Beiersdorf from 2024)." None of those five brands is in the v0.40 registry: every brand of the frozen registry (11 airline brands, 25 bank holders, 24 ghosts and 3 living-brand controls, with their aliases) was screened against them on 2026-11-12 and none matched (DEVIATIONS Entry 0, ex ante), so no v0.40 brand has a recorded Cheil Worldwide or Iris tie. No brand was contacted. Acquisition, coding and scoring are fully automated against the frozen registry, and this pre-registration is locked and deposited before the first call. Samsung Electronics had no role in the design, conduct, analysis or reporting of this work.

## Funding {-}

Self-funded.

## Ethics {-}

Not applicable; no human subjects. Public model APIs, including the providers' own web search tools, and public official data (BTS, FDIC, SEC filings).

## Use of AI tools {-}

During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.

---

## §11 Deliverables, lock and sources

**Deliverables.** Raw answers with search traces (JSONL); coded mention table (CSV); verdicts (JSON); figures; the Third System report (managerial register) and the SSRN-format paper (academic register); data on OSF (`ec6wh` → `v40`). Every test is reported, including failures.

**Lock.** `prereg/LOCK_MANIFEST_v0_40.sha256` lists the SHA-256 of this file, the probe set, the cost estimate, the dry-run and test records, the technical check, the pre-lock check record (§4.8), every script under `osf/v40/scripts/` and the frozen registry inputs and outputs. It is refreshed at the lock (step 4), committed, tagged `v0.40-prereg-r1`, pushed, and deposited with `osf/v40/prereg` and `osf/v40/registries`. No lock before the pre-lock check records PASS (§4.8); no study probe before tag and deposit.

### Sources cited in this pre-registration
- Anthropic, Models overview (opened 2026-11-12): https://platform.claude.com/docs/en/about-claude/models/overview.md
- OpenAI, GPT-6 Astra model page (opened 2026-11-12): https://developers.openai.com/docs/models/gpt-6-astra ; pricing: https://developers.openai.com/api/docs/pricing ; GPT-4o: https://developers.openai.com/api/docs/models/gpt-4o.md ; GPT-4o mini: https://developers.openai.com/api/docs/models/gpt-4o-mini.md ; GPT-6.1 Terra announcement (not fetched, client error): https://openai.com/index/introducing-gpt-6-1-terra/
- Google, Gemini API latest model (opened 2026-11-12): https://ai.google.dev/gemini-api/docs/latest-model ; pricing: https://aistudio.google.com/docs/pricing ; Gemini 4 Carbon (Google Cloud): https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/4-carbon
- Capital One, Discover checking update: https://www.capitalone.com/updates/discover/checking/ (as cited in registry draft r3, §5 item 5)
- Registry sources: `osf/v40/registries/out/v0_40_registry_draft.md` (r3, frozen 2026-11-12) and its CSV source columns
- Method v1.17 results note: `osf/methodology/v1_17/outputs/RESULTS_NOTE_v1_17.md` (tag `v1.17-prereg-r1`)
- Jack, Lehman, Maloney and Xu, arXiv 2605.30207 (May 2026); Rienecker et al., "Auditing Preferences for Brands and Cultures in LLMs" (ChoiceEval), arXiv 2603.18300 (March 2026)
- MSI Working Paper *Tri-System Brand Growth: The AI Mediation Layer*, Report No. 26-132
