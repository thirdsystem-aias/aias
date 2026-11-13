# AIAS™ Presence Measurement Protocol — Pre-Registration v0.65 (study #55, cross-cultural identity load; revision r0, DRAFT — not locked, not final)

Pablo Ulpiano González Castro
School of Visual Arts, MPS Branding Program, New York, NY (primary academic affiliation)
Third System™ (research entity; data archive and methodology venue)
Correspondence: pablou@pablou.com · pablou.com
ORCID: 0009-0003-8968-9990 (linked: https://orcid.org/0009-0003-8968-9990)

---

## For Pablo: plain-language summary (not part of the locked text; removed or kept as an appendix at the lock)

**What this study asks.** The programme measures a brand's *identity load* as how much more often AI models name it when asked culture questions ("which brands are popular right now", "which do celebrities use", "which have the most iconic identity") than when asked category questions ("which are the best", "which do experts recommend"). v1.6 introduced the measure and confirmed the pattern in cosmetics (v0.21; partly in skincare, v0.20); v0.37 defined it per brand. All of this is in English. Study #55 asks whether that pattern travels: when the same questions are asked in Spanish, Korean and Chinese (v0.62's wave), do the same brands lead on the culture questions as in English, does the cultural lead shrink or grow, and do culture-led brands lose more of their visibility outside English?

**What it uses.** Only answers that v0.62 will collect (Nov 29–Dec 2) plus t4's English answers already collected (v0.42). No model calls, no spend. The draft fixes every test, threshold, seed, exclusion and sensitivity now, and locks before any v0.62 answer exists.

**Three tests, per language (Spanish, Korean, Chinese).**
1. *Same brands lead?* (primary) Brands' identity load in the language orders them as in English: confirmed at a rank correlation of 0.50 or more, failed below 0.30.
2. *Do culture-led brands travel worse?* Brands with higher English identity load lose more visibility in the language, holding their English visibility fixed: confirmed at −0.30 or below, failed above −0.15.
3. *Does the cultural lead move as a whole?* The average identity load shifts by at least 2 mentions in 27 answers, in either direction: confirmed if it does, failed if it stays within that band.

**What it cannot say.** v0.62 changes the language of the question, not the country: no market is named and the models are the same US-built ones. So #55 tests language-of-question, not collectivist versus individualist markets as the roadmap line puts it; the paper says so. Translations of the culture questions drift more than the category ones (Chinese cosmetics has no culture question coded "equivalent"); a sensitivity check keeps only the questions coded equivalent.

**Where it goes.** One cross-cutting paper with #54 (v0.63, panel-construction sensitivity), about late January (per the coordinator's brief; the Full study list on the control panel was not re-read for this draft).

## Decisions for Pablo (each has a default; the draft is written on the defaults)

| # | Decision | Default (in this draft) | Alternative |
|---|---|---|---|
| Q1 | Study number | **v0.65** (next free number in Phase P that no draft has proposed; §0) | v0.64, if #76 takes another number |
| Q2 | Scope of the confirmatory tests | **The two-channel trio v0.20–v0.22, 72 units** (where the programme defines identity load, v0.37); v0.19 and v0.23 exploratory only (E1) | All five categories, using v0.19's and v0.23's own channel labels |
| Q3 | H1 bars | **0.50 / 0.30**, n ≥ 45 (v0.62's secondary bars; v0.37's floor) | 0.70 / 0.50 (v0.62's Presence bars) |
| Q4 | H2 direction | **One-sided, negative** (culture-led brands lose more outside English) | Two-sided |
| Q5 | H3 equivalence bound | **2/27** per unit (about 0.074) | 1/27; the dry run shows 1/27 almost never yields FALSIFIED at n ≈ 72 (§6) |
| Q6 | Cultural framing | **No external culture index**; the contrast is English against each language | Attach a published individualism index (source and values cited before the lock) as a descriptive |
| Q7 | Lock | **24 hours after you receive the final text**, before v0.62's first call | Waive the 24 hours, as for v0.42 |

---

**Study:** Cross-cultural identity load (roadmap Phase P, "Cross-cultural Identity Load study (collectivist vs. individualist markets)"; study list #55). Does a brand's identity load, the cultural-channel lead in how AI models surface it, carry over when the questions are asked in Spanish, Korean and Chinese instead of English?
**Design:** Pre-registered re-analysis, no new collection. Data: the category-question answers (Phase B, 30 questions, three runs, three models N3, search off S0) that v0.62 collects in Spanish, Korean and Chinese (locked design, `osf/v62/prereg/PRE_REGISTRATION_v0_62.md`), against the same questions in English from the t₄ wave (v0.42, collected; coded tables at tag `v0.42-scoring-locked`). Confirmatory scope: the trio v0.20 skincare, v0.21 cosmetics, v0.22 automotive (72 units).
**Budget:** none. No model call, no paid service; the programme's $100 cap is not touched.
**Protocol version:** identity load as IL-Direct (v0.37 MODERATOR_DEFINITION; construct anchor v1.6, SSRN 6816340, Increment 2, H_IdentityLoad_Direct); recall Presence π̂ as v0.42 / v0.62; statistics as v0.62 (`osf/v62/scripts/score_v0_62.py`, imported unchanged).
**Pre-registrant:** Pablo Ulpiano González Castro
**Status:** r0 draft (2026-11-12, programme runner, lane F). Not reviewed; nothing locked.
**Lock target:** git tag `v0.65-prereg-r1` on branch `v0.65`, pushed to `origin`; external anchor: OSF `ec6wh` → `v65/prereg/` and `v65/anchor/`. Locks 24 hours after the pre-registrant receives the final text, unless he objects (programme rule, Nov 9, 2026); must lock before the first v0.62 call (window opens 2026-11-29 00:00 US Central).
**Scoring:** once, after v0.62's own single scoring run (§5.2).
**Paper:** one cross-cutting paper with #54 (v0.63), about late January 2027 (coordinator's brief).

---

## §0 Programme position, number and branch

- **Study.** Roadmap Phase P lists "Cross-cultural Identity Load study (collectivist vs. individualist markets)" (`aias_roadmap_ssot.md`, Phase P) and CLAUDE.md's plan names "cross-cultural identity load" among the cross-cutting studies; the study list numbers it #55. v0.62's pre-registration keeps it separate: "The cross-cultural identity-load study (#55) remains separate: no identity-load variable, hypothesis or market contrast is defined here" (v0.62 §0). This pre-registration supplies that variable, hypotheses and contrast, on v0.62's data, without changing v0.62.
- **Number v0.65 (proposed; decision Q1).** Phase P slots into v0.62–v0.68. On 2026-11-12 (06:06 CT) `git tag -l` and `git branch -a` show, at v0.45 and above, only `v0.45`, `v0.62`, `v0.63` (branches, local and origin) and `v0.63-prereg-r1` (tag); `git ls-remote --heads --tags origin` shows nothing from v0.46–v0.59 or v0.64–v0.69. v0.46–v0.61 are reserved by the roadmap for the Ranking and Sentiment arcs (v0.46: "RS × prompt-phrasing stability"). v0.64 is the next free number in Phase P, but the draft for #76 (the agent-choice Registered Report candidate) proposes v0.46 or v0.64; to avoid two drafts claiming one number, this draft takes **v0.65**. If #76 is numbered elsewhere, v0.64 is equally valid (a rename of the folder, branch and tag before the lock; nothing else depends on the number). The OSF folder list was not re-read for this draft (open item, §11).
- **Branch and base.** `v0.65`, from `v0.62` @ `e449b6c` (v0.62's lock-preparation commit, "final PRE_REGISTRATION_v0_62.md (byte copy of r3)"), the way v0.63 was branched from the tip of the study whose code and data it re-uses (v0.63 from `v1.14` @ `ceb706d`; v0.63 DEVIATIONS Entry 0 item 1). The base carries v0.62's scorer, parameters, probe file with t₄'s channel labels, translations with drift codes, and the v1.7 per-brand channel table. It does not carry `osf/v42`; t₄'s coded tables are read from git at a pinned tag (§4.1), as v0.62 does for v0.42's kernels. If v0.62's lock adds commits after `e449b6c` that change any file this study reads, v0.65 is rebased onto `v0.62-prereg-r1` before its own lock and the manifest is rebuilt (§11).
- **Relation to #54 (v0.63).** Same paper, separate pre-registrations. v0.63 tested whether Recognition × Recall verdicts survive changes in how the brand panel is built (locked and scored on 2026-11-10, US Central: tag `v0.63-prereg-r1` on commit `f90a5b8`, 20:21; scoring commit `1bce3fc`, 20:36; H1 CONFIRMED, H2 MARGINAL, H3 CONFIRMED, H4 MARGINAL; `osf/v63/outputs/v0_63_verdicts.json` on branch `v0.63`). #55 holds the panel fixed (the trio's registries as v0.62 uses them) and varies the language of the question; no v0.63 rule is crossed with a language here.
- **Industry breadth.** Not an aim: the trio's categories are fixed by the construct (identity load is defined on them) and by v0.62's design (repeat waves keep the omnibus categories).

## §1 Context and question

Identity load is the programme's name for how much a brand's AI surfacing rests on cultural rather than category questions. v1.6 (SSRN 6816340, Increment 2) measured it per cell as δ = mean(R_cult) − mean(R_cat) and returned H_IdentityLoad_Direct CONFIRMED for v0.21 cosmetics and PARTIAL for v0.20 skincare. v0.37 turned it into a per-brand moderator, IL-Direct(b) = R_cult(b) − R_cat(b), "a CONTINUOUS per-brand covariate ... Higher IL-Direct = more cultural-channel-led surfacing = higher Identity Load", valid on the two-channel trio v0.20–v0.22 (`osf/v37/prereg/v0_37_cpc_identity_load_moderator_content.py`, MODERATOR_DEFINITION); its primary test against Consistency φ was a clean null (H_IL_Consistency FALSIFIED → CLEAN-NULL, ρ = −0.008, n = 53; `osf/v37/v37_verdicts.json`). Every one of these measurements was taken in US English.

The cultural channel is where language should matter most: "popular right now", "celebrities and influencers", "viral or cult-favorite" and "iconic or storied identity in popular culture" are questions about a culture, and a model asked them in Spanish, Korean or Chinese may draw on a different one. v0.62 asks the trio's six questions per category (three category, three cultural; the `channel` field of t₄'s probe file) in the three languages, of the same three models as t₄, with no country named. This study asks, per language:

1. **Order** (primary): does identity load order brands as in English?
2. **Moderation**: do brands with higher English identity load lose more Presence in the language than their English Presence predicts?
3. **Level**: does the cultural-channel lead shift as a whole?

The roadmap frames the study as "collectivist vs. individualist markets". v0.62 varies language alone ("no country, market or location is stated in any probe, and no system prompt is sent", v0.62 §1), so this design can test the language of the question, not markets or national cultures; §8 states the limit and decision Q6 sets whether any external culture index is attached.

---

## §2 Pre-registered hypotheses

### §2.1 Definitions

- **Languages.** L ∈ {ES, KO, ZH}, v0.62's Spanish (neutral Latin American), Korean (standard South Korean) and Chinese (Simplified, Mainland usage). EN = the English t₄ wave (v0.42).
- **Units.** Confirmatory: the 72 units of the trio v0.20 (24), v0.21 (24), v0.22 (24), unchanged from the registries v0.62 uses. Under v0.62's headphones option A (adopted) no trio unit is removed. Exploratory E1 (§2.7): the 16 v0.19 and 24 v0.23 units.
- **Channels.** Each Phase B question's channel is its `channel` field in `osf/v62/inputs/probes_v0_42.jsonl` (byte copy of t₄'s probe file; v0.62 §3.1): for each trio category, q1–q3 are `R_cat` (category) and q4–q6 `R_cult` (cultural). E1 uses v0.19's `category_anchored` / `cultural_footprint` and v0.23's `editorial-authority` / `cultural-cult` labels the same way. The translated questions keep t₄'s probe IDs (v0.62 §5.1), so the channel of each translated question is that of its English source.
- **Calls and mentions.** For unit b of category c in language X ∈ {EN, ES, KO, ZH}: n_{c,ch,X} = number of answered Phase B calls of category c in channel ch (N3: Claude Fable 5.2, GPT-6 Astra, Gemini 4 Argon; condition S0; runs 1–3; complete = 3 · 3 · 3 = 27); k_{b,ch,X} = number of those calls whose answer mentions b, as coded by v0.42's coder (EN) and v0.62's coder (ES, KO, ZH; v0.62 §4.3, §7.1).
- **Identity load (IL-Direct), per language.** IL_{b,X} = k_{b,cult,X} / n_{c,cult,X} − k_{b,cat,X} / n_{c,cat,X}. This is v0.37's IL-Direct(b) = R_cult(b) − R_cat(b) (MODERATOR_DEFINITION, cited in §1) on t₄'s and v0.62's panel and runs, divided by the channel's answered calls so that a missing call does not count as a non-mention; with complete data it equals (R_cult − R_cat) / 27, and the within-category ranks are identical to v0.37's count form (sensitivity S-Count uses the count form). Range −1 to +1; higher = more cultural-channel-led surfacing = higher identity load.
- **Recall Presence over the six questions.** π̂_{b,X} = (k_{b,cat,X} + k_{b,cult,X}) / (n_{c,cat,X} + n_{c,cult,X}), equal to v0.62's π̂ (v0.62 §2.1) for the trio.
- **Eligibility (H1, H3).** b enters the test for L iff 0 < π̂_{b,EN} < 1 and 0 < π̂_{b,L} < 1: v0.37's true-zero floor and saturation ceiling (v0.37 ELIGIBILITY_ATTRITION), applied to π̂, because a unit never named, or named in every answer, has an identity load of 0 by construction. **H2** needs only 0 < π̂_{b,EN} < 1 (a unit that falls to π̂_{b,L} = 0 is the outcome H2 is about).
- **ρ_c, permutation p, bootstrap.** As v0.62 §2.1, by import of `score_v0_62.rho_c`, `perm_p` and `bootstrap_ci` unchanged: the centred pooled within-category Spearman; 10,000 within-category permutations of y, one-sided; 10,000 within-category bootstrap resamples, percentile 95%. **Partial ρ_c(x, y | z):** the partial correlation of the centred within-category ranks of x and y given those of z; its p from 10,000 within-category permutations of x (lower and upper tails reported).
- **Seeds.** H1 650101 (ES), 650102 (KO), 650103 (ZH); H2 650111, 650112, 650113; H3 650121, 650122, 650123; bootstrap of ρ_c 650131; descriptives and E1 650141; dry-run synthetic worlds 650151–650155.
- **α.** 0.05 per test, no multiplicity correction (programme convention); verdicts rest on the pre-set effect-size bars, and every test is reported.
- **n floor.** 45 eligible units, v0.37's power floor ("critical Spearman rho at p=.05 crosses 0.30 near n~=44", `osf/v37/scripts/score_v0_37.py`); below it the test is UNDETERMINED.

### §2.2 PRIMARY: `H1_IL_Order` (one test per language)

**Statement.** Asked in language L, the models order brands by identity load as they do in English.
**Operationalisation.** x = IL_{b,EN}; y = IL_{b,L}; eligible trio units; one test each for ES, KO, ZH.
**Verdict rule (per language).** UNDETERMINED if n < 45 or the drop rule applies (§5.3) · CONFIRMED if ρ_c ≥ 0.50 and p < 0.05 · FALSIFIED if ρ_c < 0.30 · MARGINAL otherwise.
**Rationale.** 0.50 / 0.30 are v0.62's bars for its second instrument (H_Lang_Phi), used here because IL is a difference of two channel rates and carries more sampling noise than π̂; the stricter Presence bars (0.70 / 0.50) are decision Q3.
**Reported alongside.** Bootstrap 95% interval of ρ_c; per-category ρ_c; the uncentred value; the sensitivities (§5.4).

### §2.3 SECONDARY: `H2_IL_Moderates_Language` (per language)

**Statement.** Brands whose English surfacing leans more on cultural questions lose more Presence when asked in L, given their English Presence.
**Operationalisation.** ρ_partial = partial ρ_c(IL_{b,EN}, π̂_{b,L} | π̂_{b,EN}) over trio units with 0 < π̂_{b,EN} < 1. Predicted sign negative (decision Q4).
**Verdict rule.** UNDETERMINED if n < 45 or the drop rule applies · CONFIRMED if ρ_partial ≤ −0.30 and lower-tail p < 0.05 · FALSIFIED if ρ_partial > −0.15 (labelled REVERSED when ρ_partial ≥ +0.30 and upper-tail p < 0.05) · MARGINAL otherwise. Bars: v0.37's (|ρ| ≥ 0.30 confirm, < 0.15 falsify).
**Rationale.** The cultural questions ask what is popular, worn by celebrities or iconic; if the models' answers to them draw on an English-language culture, a brand that English answers surface mainly through those questions has less to carry it into another language. This is the study's hypothesis, not a finding cited from elsewhere.
**Reported alongside.** ρ_c(IL_{b,EN}, π̂_{b,L} − π̂_{b,EN}) (no verdict). Note: H2 and H3 are not independent: a shift toward the cultural channel in L (H3) raises π̂_{b,L} most for high-IL brands, which pushes ρ_partial up; the dry run shows it (§6, scenario C, ZH: ρ_partial = +0.239 under a pure cultural shift, FALSIFIED). The paper reads H2 beside H3.

### §2.4 SECONDARY: `H3_IL_Shift` (per language; two-sided)

**Statement.** Asked in L, the models' balance between the cultural and the category channel shifts.
**Operationalisation.** Δ_L = mean over H1's eligible units of (IL_{b,L} − IL_{b,EN}); 95% interval from 10,000 within-category bootstrap resamples (seed per language). Equivalence bound ε = 2/27 ≈ 0.074 (two mentions in the 27 answered calls of a channel, per unit on average; decision Q5).
**Verdict rule.** UNDETERMINED if n < 45 or the drop rule applies · FALSIFIED (no shift) if the interval lies inside (−ε, +ε) · CONFIRMED (shift; direction "toward cultural" if Δ_L > 0, "toward category" if Δ_L < 0) if the interval excludes 0 and |Δ_L| ≥ ε · MARGINAL otherwise.
**Rationale.** The programme has no prior result on the direction, so the test is two-sided. ε is the smallest change this design counts as more than one call's worth; r0 first drafted ε = 1/27, which the synthetic dry run showed could almost never return FALSIFIED (§6).
**Reported alongside.** The mean channel rates (k/n) in EN and L for each channel, so that a shift can be read as a cultural-channel rise or a category-channel fall.

### §2.5 Pre-registered descriptives (no verdicts)

1. **D1** per-category ρ_c of H1 (in H1's record).
2. **D2** ρ_c of IL between each pair of languages (ES–KO, ES–ZH, KO–ZH), units eligible in both.
3. **D3 Benchmark across time and panel.** ρ_c(IL-Direct at t₁, IL_{b,EN} at t₄) on trio units eligible at t₄, where IL-Direct at t₁ = R_cult_total − R_cat_total from `osf/methodology/v1_7/data/v1_7_cpc.csv`, read exactly as `score_v0_37.load_il_direct` reads it, with v0.37's hash of the consumed columns checked against `osf/v37/.v37_il_direct_baseline.sha256`. It shows how stable English identity load is across the six-model legacy panel (t₁) and N3 (t₄); H1's values are read beside it, as v0.62 §2.7 reads its language gap beside time.
4. **D4 Home language.** Δ of IL for trio units whose brand owner is headquartered where L is the main language, from v0.62's country column (v0.62 §2.9 item 5), when it exists; never a test.
5. **D5** Counts: eligible units per language and category; units excluded at the floor and at the ceiling, per language.

### §2.6 Joint reading (fixed now)

**IL-portable** if `H1_IL_Order` is CONFIRMED in all three languages; **IL-language-bound** if it is FALSIFIED in any (the paper names the languages); **partly portable** otherwise. H2 and H3 are reported beside this reading and do not change it.

### §2.7 Exploratory E1 (declared; no verdict)

H1's statistic on the v0.19 and v0.23 units with their own channel labels. v0.37 put v0.19 out of the construct ("single-channel") and v0.23 outside the trio ("walled"); E1 is reported as exploratory and never enters the joint reading.

### §2.8 Manipulation checks

v0.62's checks are inherited unchanged and read from v0.62's outputs (MC_Complete, MC_Served, MC_Language, MC_Script, MC_Alias, MC_Truncation, MC_Window, MC_Parity, MC_Budget; v0.62 §2.8). Added here: **MC_Channel**, the answered calls per category × channel × language (27 when complete), reported; **MC_Pin**, t₄'s coded tables equal the pinned git blobs (§4.1), else HALT.

---

## §3 Data, and what is known before the lock

1. **v0.62 (ES, KO, ZH).** Nothing collected. v0.62 locks on 2026-11-12 unchanged from `e449b6c` (its design is final: Spanish, Korean and Chinese; the 30 category questions per language in three runs, 810 calls; the 88 yes/no brand questions last, 792 calls; window 2026-11-29 to 2026-12-02 US Central; v0.62 §5). **This pre-registration locks before any v0.62 answer exists.** It uses blocks 1–3 only (the category questions); block 4 (yes/no brand questions) serves no test here.
2. **t₄ (EN).** Collected (tag `v0.42-acquisition-locked`, 876 of 876 calls answered), coded (commit `c84f6fa`) and scored once (tag `v0.42-scoring-locked`, `31c64c6`: `v42_verdicts.json`, `v42_brand_table.csv`). v0.42's verdicts and brand table hold π̂ and φ per brand, not channel-split values: a search of `v42_verdicts.json` and `PRE_REGISTRATION_v0_42.md` for "cult", "identity" and "channel" on 2026-11-12 found no channel or identity-load statistic (the one hit is a domain name). To the drafting lane's knowledge no one has computed t₄'s identity load. The lane read the headers of t₄'s coded tables and the blob ids of the files at the tag (metadata), not their values. It did not read v0.42's per-brand π̂ values.
3. **t₁–t₃ (EN, legacy six-model panel).** Identity load at t₁ is published: v1.6 (cell level) and v0.37 (per brand, `osf/v37/v37_il_phi_analysis_set.csv`; source `v1_7_cpc.csv`). The lane read v0.37's README, verdict summary and the first lines of its analysis set while drafting; it did not compute anything from them. D3 uses the t₁ values as a benchmark only.
4. **Translations.** v0.62's drift codes are known (design file `osf/v62/translations/translations_v0_62_r2.json`, read for the S-Drift rule). On the trio's 18 questions, those coded *equivalent* are: ES 7 of 9 category and 5 of 9 cultural; KO 7 and 4; ZH 7 and 2. v0.21's three category and three cultural questions in Chinese are all coded *minor drift* except one category question (q2), because of the declared v0.21 scope rule (cosmetics → 彩妆; v0.62 §3.3); S-Drift therefore has no v0.21 cultural question in Chinese and drops that category for ZH (§5.4).
5. **No synthetic result is a finding.** The dry run (§6) uses invented worlds to check the code and the operating characteristics of the rules.

## §4 Inputs (pinned)

### §4.1 English comparator

t₄'s coded Phase B tables, read with `git show v0.42-scoring-locked:osf/v42/data/coded/{v19..v23}_phase_b.csv`; before reading, the scorer checks each file's blob id against the pinned value (MC_Pin; HALT on mismatch): v19 `7fb571b5…`, v20 `5f765d98…`, v21 `feb9d5f6…`, v22 `8dc39b9d…`, v23 `7f379235…` (full ids in `score_v0_65.EN_BLOBS`). Rows used: condition S0, models N3, runs 1–3.

### §4.2 Language data

v0.62's coded Phase B tables `osf/v62/data/coded/{es,ko,zh}/v2{0,1,2}_phase_b.csv` (and v19, v23 for E1), as written by v0.62's coder (`code_v0_62.py`, v0.62 §7.1) and read by v0.62's own reader (`score_v0_62.read_coded_b`, imported unchanged). If v0.62 writes its S-Language, S-Script and S-Alias exclusions or alternative tables, they feed v0.65's sensitivities of the same names; otherwise those sensitivities are reported NOT AVAILABLE (§5.4).

### §4.3 Design files (from v0.62's lock, read only)

`osf/v62/inputs/probes_v0_42.jsonl` (channels), `osf/v62/translations/translations_v0_62_r2.json` (drift codes), `osf/v62/scripts/score_v0_62.py` and `params_v0_62.py` (statistics, drop share, `COI_FLAGGED`), `osf/v62/prereg/PRE_REGISTRATION_v0_62.md`; `osf/methodology/v1_7/data/v1_7_cpc.csv` (D3). All are in the lock manifest (§11).

## §5 Analysis plan

### §5.1 Computation

`osf/v65/scripts/score_v0_65.py --run` (skeleton at r0; tests on synthetic data, §6). It computes IL and π̂ for EN and each language from the coded tables (§2.1), then H1, H2, H3, the sensitivities, E1 and the descriptives, and writes `osf/v65/outputs/v65_verdicts.json`.

### §5.2 Order and guard

v0.65 is scored **once, after v0.62's own single scoring run**, so that v0.65 computes no statistic on v0.62's answers before v0.62 does (as v0.62 runs gate P1's real-data half after v0.42's scoring). `--run` refuses unless: tag `v0.65-prereg-r1` is on `origin`; `osf/v62/v62_verdicts.json` exists; the lock manifest verifies; no v0.65 output exists.

### §5.3 Drop rule and missing data

v0.62's rule, per language (v0.62 §7.4): a model with < 90% of its expected Phase B calls answered in L makes every v0.65 test in L UNDETERMINED (and every sensitivity in L); the same rule on t₄'s S0 calls makes every test UNDETERMINED. Calls not sent because of v0.62's budget stop count as unanswered. Within a language that passes, a missing call reduces n_{c,ch,L} (rate form); no imputation. If v0.62 stops before block 3 (its projection pause or $100 stop), the rule decides; no v0.65 test is run on fewer runs.

### §5.4 Sensitivities (reported; no verdict changes)

- **S-COI.** The trio units in v0.62's `COI_FLAGGED` removed together (Eucerin, BMW, Bentley, Chevrolet; 68 units; the Declarations give the ties), for H1, H2 and H3. If a primary verdict differs under S-COI, the paper reports both in its abstract (v0.62 §7.5's rule).
- **S-Drift.** Only questions coded *equivalent* in L, in both EN and L; a category with no equivalent question in a channel drops out (ZH v0.21; §3 item 4). H1 and H3.
- **S-Language, S-Script, S-Alias.** v0.62's exclusions (off-language answers; Chinese answers with Traditional-only characters; collision-prone aliases off), when v0.62 provides them (§4.2). H1 and H3.
- **S-Count.** v0.37's count form R_cult − R_cat instead of rates. H1.
- **S-Uncentred.** The uncentred pooled statistic (in H1's record).
S-Denon and S-Headphones do not apply (no trio unit is a headphones unit).

### §5.5 Reporting

Every test is reported, including failures and undetermined results, with n, the statistic, p and interval; outputs deposited. Public-study rules apply: no focal brand, no lesson addressed to a brand, no brand contacted. The 10 units with the largest |IL_{b,L} − IL_{b,EN}| per language may be listed without commentary addressed to any brand (as v0.62 §2.5).

## §6 Dry run and operating characteristics (synthetic only)

`python3 osf/v65/scripts/score_v0_65.py --dry-run` → `osf/v65/prereg/dry_run_v0_65_r0.txt`. Five invented worlds in v0.62's coded-table shape (112 units in five categories of 16/24/24/24/24, including units named like the six flagged units so that S-COI is exercised; 3 models × 3 runs × 30 questions per language; a mention is drawn with probability logistic(a_b ± 0.8 · d_b), + for cultural and − for category questions, where d_b is a latent identity load; in language L, d_{b,L} = r · d_b + √(1 − r²) · noise). 2,000 permutations and resamples per statistic in the dry run (10,000 in the real run). Results (seeds 650151–650155):

| World | What is built in | H1 (ES / KO / ZH) | H2 | H3 |
|---|---|---|---|---|
| A portable | r = 0.95 everywhere | CONFIRMED ×3 (ρ_c 0.722 / 0.789 / 0.661) | FALSIFIED ×3 | FALSIFIED ×3 (no shift) |
| B language-bound | r = 0 in KO | KO FALSIFIED (ρ_c −0.101); ES, ZH CONFIRMED | FALSIFIED ×3 | KO MARGINAL; ES, ZH FALSIFIED |
| C cultural shift | +1 logit on ZH cultural questions | CONFIRMED ×3 | ZH ρ_partial +0.239, FALSIFIED | ZH CONFIRMED, toward cultural (Δ +0.194, interval +0.158 to +0.232); ES, KO FALSIFIED |
| D moderation | ES presence lowered by 1 logit per unit of d_b | CONFIRMED ×3 | ES CONFIRMED (ρ_partial −0.822); KO, ZH FALSIFIED | ES MARGINAL; KO, ZH FALSIFIED |
| E drop rule | 20% of one model's ES calls removed | ES UNDETERMINED (and its sensitivities); KO, ZH CONFIRMED | ES UNDETERMINED | ES UNDETERMINED |

What the dry run shows about the rules: (1) with a near-perfect latent correlation (r = 0.95), sampling noise from 27 calls per channel brings the observed ρ_c down to 0.66–0.85, so the Presence bars (0.70 / 0.50; decision Q3) would have returned MARGINAL for ZH in world A; (2) under r0's first bound ε = 1/27, H3 returned MARGINAL in 12 of 13 language cases without a built-in shift (the 95% interval of Δ_L is about ±0.04 wide at n ≈ 72), so it could almost never return FALSIFIED; under ε = 2/27 it returns FALSIFIED in 11 of those 13 (MARGINAL in B-KO and D-ES) and still CONFIRMED for the built-in shift (decision Q5); (3) a pure cultural shift pushes H2's ρ_partial upward (world C), as §2.3 notes. These are properties of the invented worlds, not predictions for v0.62's data.

**Operating characteristics over 500 worlds per condition** (`--power` → `osf/v65/prereg/power_v0_65_r0.json`; seed 650161; same invented generative model; Spanish only; H1 read from ρ_c and n, since at n ≈ 70 a ρ_c of 0.50 is far inside p < 0.05; H3 with 1,000 bootstrap resamples):

| Latent IL correlation r | 0.30 | 0.50 | 0.70 | 0.80 | 0.90 | 0.95 |
|---|---|---|---|---|---|---|
| Mean observed ρ_c | 0.236 | 0.385 | 0.544 | 0.636 | 0.732 | 0.771 |
| P(H1 CONFIRMED) | 0.008 | 0.146 | 0.700 | 0.946 | 1.000 | 1.000 |
| P(H1 FALSIFIED) | 0.686 | 0.198 | 0.022 | 0 | 0 | 0 |

| Cultural shift (logit), r = 0.9 | 0 | 0.25 | 0.5 | 1.0 |
|---|---|---|---|---|
| P(H3 FALSIFIED, no shift) | 0.756 | 0.300 | 0.010 | 0 |
| P(H3 MARGINAL) | 0.242 | 0.604 | 0.286 | 0 |
| P(H3 CONFIRMED, shift) | 0.002 | 0.096 | 0.704 | 1.000 |

In these worlds every test had n ≥ 45 (no UNDETERMINED); real Korean and Chinese answers may name fewer trio brands. Sampling noise from 27 calls per channel attenuates the observed ρ_c well below the latent correlation (0.771 at r = 0.95), which is the reason for H1's bars (decision Q3). H2's operating characteristics were not simulated beyond the five worlds above (§11).

## §7 Budget

None: no model call, no paid service, no judge. The programme's $100 cap per paper is not touched by this study; v0.62's own collection is costed and guarded in v0.62 §6.

## §8 Limitations

1. **Language, not market or culture.** v0.62 names no country, sends no system prompt and uses the same three US-developed models in every language (v0.62 §1, §8 limitation 3). A difference between languages is a difference in how these models answer in that language, not in what users in any country receive, and not a measured difference between collectivist and individualist cultures. No culture index is attached (decision Q6).
2. **The cultural questions translate less cleanly than the category questions** (§3 item 4), so a cultural-channel difference can come from wording. S-Drift checks it where equivalent questions remain; for ZH v0.21 none does.
3. **Coding differs by language.** Korean and Chinese mentions rest on v0.62's alias table, mostly unconfirmed (v0.62 §4.2, §8 limitation 7); a brand under-counted in one channel and not the other would move its IL. S-Alias and MC_Alias (v0.62) bound this.
4. **Time and language are confounded** (t₄ mid-November; v0.62 late November / early December; v0.62 §8 limitation 5). D3 shows English identity load's own stability across time and panel.
5. **Small trio, one panel.** 72 units, three models, three runs; eligibility can lower n below the floor of 45 in a language where many units are never named (UNDETERMINED). v0.37 had 53 of 72 analysable units at t₁ under its own (φ-defined) rule.
6. **Identity load is defined on the trio.** v0.19 and v0.23 enter only as exploratory E1 (v0.37's scope).
7. **H2 is not independent of H3** (§2.3); its sign prediction is this study's hypothesis, not a cited result.
8. **No buyer persona**, as v0.62 (§8 limitation 11 there).

---

## §9 Decisions for the pre-registrant (before the lock)

Q1–Q7 as in the table at the top, with their reasons:

1. **Q1 Number.** v0.65 (default) because #76's draft proposes v0.46 or v0.64 and v0.46 is reserved by the roadmap; v0.64 if #76 is numbered elsewhere.
2. **Q2 Scope.** Trio only (default; v0.37's construct scope, 72 units). Alternative: all 112 units with v0.19's and v0.23's own channel labels (more units; outside the construct as v0.37 defined it).
3. **Q3 H1 bars.** 0.50 / 0.30 (default; v0.62's secondary bars; the dry run shows the attenuation that 27 calls per channel cause). Alternative 0.70 / 0.50.
4. **Q4 H2 direction.** One-sided negative (default). Alternative: two-sided with the same bars on |ρ_partial|.
5. **Q5 H3 bound.** 2/27 (default). Alternative 1/27 (stricter on "no shift", rarely decisive at n ≈ 72) or a bound on another scale.
6. **Q6 Culture index.** None (default). Alternative: a published individualism index attached as a descriptive, with its source and the values for the US and for the countries chosen to stand for each language cited before the lock; the draft names no index values because none was checked for it.
7. **Q7 Lock timing.** 24 hours after receipt (default); alternatively waived, as the pre-registrant did for v0.42 (control panel, "LOCK NOW", 2026-11-10). Either way before 2026-11-29 00:00 US Central.
8. **Settled by the runner (can be overruled):** eligibility rule (0 < π̂ < 1 in both, §2.1); rate form with S-Count; S-Drift on *equivalent* questions only; E1 exploratory; scoring after v0.62's own run (§5.2); seeds (§2.1).

---

## §10 Declarations

## Conflict of interest {-}

The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. This study re-analyses the answers that v0.62 collects in Spanish, Korean and Chinese, beside the English answers of the t₄ wave, against brand registries fixed in earlier phases (v0.19–v0.23; its confirmatory tests use v0.20–v0.22); it performs no new brand selection, and each registry carries its source-phase conflict-of-interest handling forward unchanged. Two items of record apply. In the automotive registry, Samsung subsidiaries hold tier-2/3 component supply relationships with several registry brands — Harman International (audio systems), Samsung SDI (battery cells), and Samsung Display (infotainment) — characterized in the source phase as non-competitive, with no brand-level overlap, and imposing no operational restriction on registry composition (v0.22 Declarations; screened in v0.22 DEVIATIONS Entry 0, Part B). In the audiophile-headphones registry, used here only in an exploratory analysis, AKG was substituted with Denon before the v0.19 pre-registration lock because AKG's parent, Harman International, is a Samsung subsidiary. Correction (November 10, 2026): Denon, which replaced AKG in the v0.19 registry, has itself been owned by Harman International, a wholly owned subsidiary of Samsung Electronics, since September 23, 2025, when Harman completed its acquisition of Sound United from Masimo; the v0.19 headphones registry therefore includes one Samsung-group brand. The substitution did not achieve its purpose, and this was not noticed until November 10, 2026. One of the three languages is Korean, and South Korea is Samsung Electronics' home market: answers in Korean, as in any language, may name Samsung-group brands that are not registry units; such names are never coded or scored, because coding counts only the registry units. The conflict-of-interest screen of v0.62 (v0.62 DEVIATIONS Entry 0, Part F) found further ties. Cheil Worldwide, a marketing company of the Samsung group in which Samsung Electronics holds 28.43%, or its agency Iris has done advertising, public-relations or search-marketing work for five registry brands: Chevrolet (for GM Korea, 2017), BMW (UK consumer public relations, 2018), Bentley (experiential agency of record in the Americas from 2021), Jack Daniel's (UK digital agency from 2022, since replaced) and Eucerin (search marketing for Beiersdorf from 2024). Four of them (Chevrolet, BMW, Bentley and Eucerin) are units of this study's confirmatory tests and Jack Daniel's of its exploratory analysis; as in v0.62, all five are kept in every analysis, and every confirmatory result is also reported without the four trio brands (sensitivity S-COI, 68 units). Samsung Electronics supplies semiconductors to Tesla under a contract running from 2025 to 2033, and Samsung SDI supplies batteries to Hyundai under an agreement of 2023; like the supply relationships of record, these are non-competitive and impose no restriction on the registries. Hotel Shilla, a Samsung affiliate, operates duty-free shops that sell brands of several registry categories among many others. The analysis is fully automated against the locked registries and v0.62's locked coding, and this pre-registration is locked and deposited before the first v0.62 call. Samsung Electronics had no role in the design, conduct, analysis or reporting of this work.

(Wording carried from v0.62's pre-registration §10, `osf/v62/prereg/PRE_REGISTRATION_v0_62.md` at `e449b6c`, which locks unchanged; the canonical v0.19 and v0.22 records and the Denon/Harman correction are kept as v0.62 states them. Adapted to this study: the description of the study in the second sentence, "used here only in an exploratory analysis" in the v0.19 item, the sentence on which flagged brands enter which analysis, and "before the first v0.62 call". The Cheil Worldwide / Iris sentence follows the pattern of v1.18 §13. v0.62's sentence on reporting every result without Denon and without the headphones category is not carried, because no confirmatory unit is a headphones unit.)

## Funding {-}

Self-funded.

## Ethics {-}

Not applicable; no human subjects.

## Use of AI tools {-}

During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.

---

## §11 Lock procedure and change log

- **r0** (2026-11-12, this draft; lane F of the programme runner): design, hypotheses, verdict rules, seeds, exclusions, sensitivities, scorer skeleton with synthetic tests, dry run and operating characteristics (H1, H3), draft lock manifest (`LOCK_MANIFEST_v0_65_DRAFT_r0.sha256`), DEVIATIONS Entry 0.
- **Before the lock:** the pre-registrant's answers to Q1–Q7; if v0.62's lock adds commits after `e449b6c` that change any file in the manifest, rebase onto `v0.62-prereg-r1` and rebuild the manifest; wire v0.62's S-Language / S-Script / S-Alias outputs into `--run` once v0.62 fixes their file names (skeleton: NOT AVAILABLE); re-read the OSF folder list to confirm `v65` is free; optional simulation of H2 over many synthetic worlds (H1 and H3 done, §6); final text `PRE_REGISTRATION_v0_65.md` (byte copy of the final draft), the plain-language summary and the decision table removed or moved to an appendix.
- **Lock:** 24 hours after the pre-registrant receives the final text unless he objects (decision Q7) and before 2026-11-29 00:00 US Central → `--lock-manifest osf/v65/prereg/LOCK_MANIFEST_v0_65.sha256` → `--verify-lock` → commit → tag `v0.65-prereg-r1` → push branch and tag (gate: Pablo) → OSF deposit of `osf/v65/prereg`, `osf/v65/scripts`, `osf/v65/anchor` (gate: Pablo) → anchor note in DEVIATIONS → after v0.62's own scoring run, `--run` once.
