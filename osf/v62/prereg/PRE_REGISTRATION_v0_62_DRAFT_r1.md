# AIAS™ Presence Measurement Protocol — Pre-Registration v0.62 (revision r1, WORKING DRAFT — not locked, not final)

Pablo Ulpiano González Castro
School of Visual Arts, MPS Branding Program, New York, NY (primary academic affiliation)
Third System™ (research entity; data archive and methodology venue)
Correspondence: pablou@pablou.com · pablou.com
ORCID: 0009-0003-8968-9990 (linked: https://orcid.org/0009-0003-8968-9990)

**Study:** The non-English wave — do AI availability scores measured in French and in Japanese reproduce the English values of the t₄ wave?
**Design:** The full t₄ panel (v0.42 r2): the five omnibus categories (v0.19 audiophile headphones, v0.20 skincare, v0.21 cosmetics, v0.22 automotive, v0.23 premium spirits; 112 brand units), its 30 category questions (Phase B) and 112 brand questions (Phase A), translated into French and into Japanese (§3) and asked of the same three models as t₄ (N3: Claude Fable 5.2, GPT-6 Astra, Gemini 4 Argon) without web search (S0): Phase B three runs, Phase A one run. Per language 3 × (30 × 3 + 112) = 606 calls; **1,212 calls** in all.
**Budget:** at most US$100 of paid model calls for the paper (both languages together), hard cap; pause at $80; both computed from actual recorded usage (programme rule, 2026-11-10). **Expected $54.42 at November prices, $60.06 at December prices** (Gemini 4 Argon doubles from 2026-12-01); the high scenario ($130.06 / $145.92) exceeds the cap and is handled by the collection order and the guard, which protect every confirmatory test (§6). All figures: `python3 osf/v62/scripts/cost_estimate_v0_62.py` (r1 output `osf/v62/prereg/cost_estimate_v0_62_r1.txt`).
**Protocol version:** recall Presence π̂ and recognition (v1.6, SSRN 6816340), Consistency φ (v1.8, SSRN 6963359), both as implemented for t₄ in `osf/v42/scripts/score_v0_42.py`; Ranking, only if v1.14 passes (§2.4), as v1.14 defines it (modal position R\*, tag `v1.14-prereg-r1`).
**Pre-registrant:** Pablo Ulpiano González Castro
**Status:** r1 working draft (2026-11-10, programme runner lane 9), built on r0 (lane 6, same day); every change is listed in §11 "Changes from r0". Scripts and tests now exist (§5, §7); the pre-registrant's three choices are still open and are each one parameter in `osf/v62/scripts/params_v0_62.py` (§9). r0 status text follows: It fixes the question, the design, the translation protocol, the brand-name rules, the COI handling and the budget. Not yet written: the acquisition, coding and scoring scripts and their tests, the parity records, the lock manifest (r1). No study probe has been sent and none will be before the lock.
**Lock target:** git tag `v0.62-prereg-r1` on branch `v0.62`, pushed to `origin`; external anchor: deposit of the pre-registration, the English source probes, the French and Japanese probe files with their back-translations and review record, the alias table, the cost estimate, DEVIATIONS.md, the scripts and tests and the lock manifest at OSF `ec6wh` → `v62/prereg/` and `v62/anchor/` before the first call. Locks 24 hours after the pre-registrant receives the final text, unless he objects (programme rule, Nov 9, 2026).
**Collection window (proposed):** 2026-11-29 00:00 to 2026-12-02 24:00 US Central, all calls within 72 hours of the first; first call planned on 2026-11-29 so that Gemini 4 Argon bills at its November price. Constraints: after the lock; one paid collection at a time on the collection machine (booked by v0.42 from 2026-11-11, v0.40 from 2026-11-17 to 2026-11-21, v0.44 from 2026-11-24 to 2026-11-28); never 2026-11-17 to 2026-11-21; before the t₅ wave (target 2026-12-03). The alternative, after t₅, is costed at December prices (§6, §9 question 2).
**Paper:** one Non-English paper for both languages, about 2027-01-15.

---

## §0 Programme position and phase number

- **Study inventory.** This pre-registration covers study #52 (French full panel) and study #53 (Japanese full panel) of the programme's study list, bundled into one Non-English paper (Plan for speed, Pablo, Nov 9, 2026: every analysis kept and individually pre-registered; the packaging changes). The cross-cultural identity-load study (#55) is a separate cross-cutting paper and is not part of v0.62: no identity-load variable, hypothesis or market contrast is defined here, and the v0.62 answers enter #55 only under #55's own pre-registration.
- **Phase number v0.62.** Branches in use on 2026-11-10 run to v0.44 (`git -C ~/aias branch -a`); the roadmap (`Try system book/aias_roadmap_ssot.md`, PHASE N and O) reserves v0.45–v0.61 for the Ranking and Sentiment arcs (v0.45/v0.46: Ranking Paper B), and places the cross-cutting studies (PHASE P, "Non-English substrate: French full panel", "… Japanese full panel") in "the v0.62–v0.68 range". v0.62 is the first number neither used by a branch nor reserved for another study.
- **Industry breadth.** Not an aim of this study: the five omnibus categories are kept because the question is a comparison with the English t₄ values on the same registries (programme rule: repeat waves keep the omnibus categories for comparability).

## §1 Context and question

Every AIAS™ measurement so far was taken in US English. A brand's AI availability is meant to describe what a model makes available to a person who asks; people ask in many languages, and a model's knowledge of brands is not guaranteed to be the same in each. If the scores depend on the language of the question, an English-only measure describes English-speaking users only, and the programme's components cannot be claimed beyond them.

The t₄ wave (v0.42 r2, collection planned for 2026-11-11 to 2026-11-13 on the newest models; not yet collected when r0 was written) gives an English baseline on the full omnibus panel. This study asks the same questions, translated, of the same models with the same settings, and tests whether the brand orderings reproduce:

1. **Presence** (primary): does recall Presence order brands in French and in Japanese as it does in English?
2. **Consistency** (secondary): does φ order brands alike?
3. **Ranking** (secondary, conditional): if the redesigned Ranking measure passes its gates (v1.14), does it order brands alike?
4. **Where they differ** (descriptive): in which categories, and by how much, do the languages part?

The study is deliberately small and confirmatory: two languages, one condition (search off), the t₄ thresholds, no new brands. Language is varied alone: no country, market or location is stated in any probe (none is stated in the English ones either), and no system prompt is sent.

---

## §2 Pre-registered hypotheses

### §2.1 Definitions

- **Languages.** L ∈ {FR, JA}. EN = the English t₄ wave (v0.42).
- **Brand units.** The 112 units of the five omnibus registries, unchanged (16 + 24 + 24 + 24 + 24).
- **Comparator values (EN).** From v0.42's locked outputs (tag `v0.42-acquisition-locked` for the raw answers; v0.42's scored brand table `osf/v42/v42_brand_table.csv`): π̂_{b,EN} = `pi_N3_S0` (three-run mean), φ_{b,EN} = `phi_N3_S0` with its partition, and, for Ranking, R\*_{b,EN} = v1.14's Stage 1 value at t₄, S0. If v0.42's drop rule excludes any N3 model in S0, the corresponding v0.62 test is UNDETERMINED.
- **k_{b,m,r,L}.** Number of the six Phase B questions of brand b's category whose answer by model m in run r in language L mentions b (§4, §7.1).
- **Recall Presence** π̂_{b,L} = Σ_m Σ_r k_{b,m,r,L} ÷ (6 · 3 · 3), answered calls as the denominator (§7.4); exactly v0.42's definition on N3, S0.
- **Consistency** φ_{b,L} = v0.42's definition (v1.8 formula per run on N3 with its partitions; the mean over the runs whose partition is defined; undefined if fewer than 2 of the 3 runs are defined). Higher φ = less consistent.
- **Ranking** R\*_{b,L} = v1.14's modal-position statistic (§3.1 of v1.14), pooled over the 54 S0 answers of the brand's category in language L, rated iff ≥ 6 rankable mentions.
- **ρ_c(x, y).** Centred pooled within-category Spearman: values rounded to 10 decimals and ranked within category (average ranks for ties), each category's ranks centred on their category mean, Pearson's r of the centred ranks pooled over categories (v0.44 r1 §2.1, C2; v1.10/v1.14's ρ_w convention). With categories of unequal size (16 and 24 units) the uncentred statistic of v0.41/v0.42 carries a between-category term; the uncentred value is reported beside each test as a non-gating comparability figure.
- **Permutation p.** One-sided; y permuted within category; ρ_c recomputed on each draw; 10,000 draws; p = (1 + #{ρ_perm ≥ ρ_obs − 10⁻¹²}) ÷ 10,001.
- **Bootstrap.** Brands resampled with replacement within category; 10,000 resamples; percentile 95% interval.
- **Seeds.** 620101 (H_Lang_Presence FR), 620102 (JA); 620111, 620112 (H_Lang_Phi FR, JA); 620121, 620122 (H_Lang_Rank FR, JA); 620131 (bootstrap); 620141 (descriptives).
- **α.** 0.05 per test, no multiplicity correction (programme convention); verdicts rest on pre-set effect-size thresholds, and every test is reported.

### §2.2 PRIMARY: `H_Lang_Presence` (one test per language) — Presence reproduces across languages

**Statement.** Asked in language L, the newest models order brands by recall Presence as they do when asked in English.

**Operationalisation.** x = π̂_{b,EN} (t₄); y = π̂_{b,L}; all 112 brands. One test for FR and one for JA.

**Verdict rule (per language).** CONFIRMED if ρ_c ≥ 0.70 and p < 0.05 · FALSIFIED if ρ_c < 0.50 · MARGINAL otherwise.

**Rationale.** 0.70 is the programme's stability bar (v0.34) and the bar of t₄'s own generation test (v0.42 `H_Gen_Presence`); 0.50 is its falsification line. Language is held to the same standard as time and model generation: if a translated question orders brands less alike than that, the English scores cannot stand for the other language.

**Reported alongside.** Per-category ρ_c; the level shift Δ_L = mean(π̂_{b,L} − π̂_{b,EN}) with its bootstrap interval, overall and per category; per-model ρ_c (each model's three-run recall, EN against L); the uncentred value; sensitivities S-Denon and S-Headphones (§7.5).

### §2.3 SECONDARY: `H_Lang_Phi` (per language) — Consistency reproduces across languages

**Operationalisation.** x = φ_{b,EN}; y = φ_{b,L}; brands with φ defined on both.

**Verdict rule.** UNDETERMINED if n < 40 · CONFIRMED if ρ_c ≥ 0.50 and p < 0.05 · FALSIFIED if ρ_c < 0.30 · MARGINAL otherwise (the thresholds and n floor of v0.42 `H_Gen_Phi` and v0.41 `H_Phi_LongHorizon`).

**Reported alongside.** Partition counts (zero, saturated, defined) per language; mean-independence |ρ_c(φ_L, π̂_L)|, flagged if ≥ 0.50 (the v1.7 ceiling).

### §2.4 SECONDARY, CONDITIONAL: `H_Lang_Rank` (per language) — Ranking reproduces across languages

**Condition.** Tested only if v1.14 resolves **PASS** (its §8: Stage 1 separability at t₄ and Stage 2 reliability t₄ → t₅) before v0.62 is scored. If v1.14 fails, or has not resolved by 2027-01-05, the test is NOT TESTED and reported as such; no Ranking value is computed on the v0.62 answers for this paper.

**Operationalisation.** x = R\*_{b,EN}; y = R\*_{b,L}; units rated in both; ρ_c over categories with ≥ 5 such units (v1.10/v1.14 convention).

**Verdict rule.** UNDETERMINED if n < 30 units · CONFIRMED if ρ_c ≥ 0.50 and p < 0.05 · FALSIFIED if ρ_c < 0.30 or p ≥ 0.05 · MARGINAL otherwise (v1.10's reliability band, which v1.14 keeps).

**Declared.** The lead-item and list rules of v1.10 (E5–E7) read Markdown list structure, which is language-independent; mention matching uses the alias step of §4. A degeneracy check as v1.14's MQ9 applies: more than 80% of rated units sharing one R\* value → UNDETERMINED.

### §2.5 Where the languages differ (pre-declared descriptive readings; no verdicts)

For each category and language: ρ_c (EN against L), Δ_L with its bootstrap interval, and the share of the category's units whose π̂ moves by more than 1/6 (one question's worth of recall per model-run average). Labels, fixed now: a category is **language-stable** in L if its ρ_c ≥ 0.70 and the interval of Δ_L contains 0; **level-shifted** if ρ_c ≥ 0.70 and the interval excludes 0; **language-sensitive** if ρ_c < 0.50; otherwise **intermediate**. With 16 to 24 units per category these readings are imprecise and are reported as descriptions, not findings. Also reported: ρ_c(π̂_FR, π̂_JA); the 10 units with the largest |π̂_L − π̂_EN| per language, without commentary addressed to any brand (independence rule).

### §2.6 Joint reading (fixed now)

- **Language-robust** if `H_Lang_Presence` is CONFIRMED in both languages.
- **Language-dependent** if it is FALSIFIED in either language (the paper names the language).
- **Partly robust** otherwise.
`H_Lang_Phi` and `H_Lang_Rank` are reported beside this reading and do not change it.

### §2.7 Benchmark for time (reported alongside; no verdict)

The English t₅ wave (target 2026-12-03, its own pre-registration) re-asks t₄'s questions about three weeks later. If its N3 S0 values are scored before v0.62 is scored, the paper reports ρ_c(π̂_{EN,t₄}, π̂_{EN,t₅}) beside each `H_Lang_Presence` value: the agreement that time alone produces over a comparable interval, so that a language gap can be read against it (language gap = ρ_c(EN t₄, EN t₅) − ρ_c(EN t₄, L)). It also reports ρ_c(π̂_{EN,t₅}, π̂_L), the English wave nearest in time to the v0.62 collection. If t₅ is not scored in time, these are reported as not available.

### §2.8 Manipulation checks

- **MC_Complete.** At least 98% of the 1,212 calls end with non-empty answer text after the retry policy. A model × language × phase below 90% triggers the drop rule (§7.4).
- **MC_Served.** Every served model ID equals the requested ID (a dated snapshot of it is accepted); any other ID: excluded, re-run in the re-run pass, logged.
- **MC_Language (new).** Share of answers written in the language asked, per model × language. Rule (fixed now; implemented and unit-tested in r1): a JA answer is in Japanese if hiragana, katakana and CJK ideographs make up at least 50% of its letters; a FR answer is in French if, among the words of a fixed list of 20 French and 20 English function words (listed in the coder), French words outnumber English words. Below 95% for a model × language is flagged. Off-language answers are kept (they are what a user receives) and a sensitivity excluding them is reported.
- **MC_Alias (new).** Every match of a collision-prone alias (§4.3) is exported for audit; the audit is reported, never used to change a code.
- **MC_Truncation.** Share of calls ending at the output cap, per model × language; above 5% flagged.
- **MC_Window.** First and last call times; all calls within 72 hours.
- **MC_Parity.** Gates P1–P4 (§7.3) pass before any statistic is computed.
- **MC_Budget.** Spend from recorded usage stays at or below $100 including the judge reserve; every pause, approval and stop is logged and reported with the calls not sent.

### §2.9 Pre-registered descriptives (no verdicts)

1. Run-to-run reliability of recall per model × language (rel1, rel3 as v0.42 §2.7), beside t₄'s English values: the noise floor against which cross-language agreement is read.
2. Recognition (Phase A) share per model × language beside English t₄; brand-level agreement of recognition codes EN against L.
3. Answer form per language: tokens (input, output, thinking) per call against English t₄ — the measured language factor that replaces the planning assumption of §6 —, words or characters per answer, registry brands named per Phase B answer, finish reasons, refusals and non-answers.
4. Script of brand mentions in JA answers: share of matched mentions written in Latin script, in katakana, in kanji.
5. Home-language descriptive: Δ_L for units whose brand owner is headquartered in France (FR) or Japan (JA). The country column is built from cited sources before the lock (r1) and is not used by any test.
6. Cost: tokens and spend per model × language from recorded usage.

---

## §3 Translation protocol

### §3.1 Source

The 142 English probes of t₄, `osf/v62/inputs/probes_v0_42.jsonl`, a byte copy of `osf/v42/prereg/probes_v0_42.jsonl` at v0.42 commit `527899e` (SHA-256 `7aa246ee…6323aa`, checked by the build script). Translated: the 30 Phase B questions; the five Phase A templates (one per category); the 15 v0.23 category labels that the open brand question inserts. Brand names are not translated (§4.1); they are cut out of each English prompt by the build script and inserted unchanged, never retyped.

### §3.2 Steps

1. **Forward translation (model).** Claude (Anthropic) translates each item into France French (vous form) and standard Japanese (polite form), following the checklist (§3.3). r0: Claude Opus 5.5 in the programme runner session, 2026-11-10. This is not a paid model call.
2. **Back-translation (independent).** A separate translator renders the French and Japanese texts back into English **without access to the English source**, literally rather than idiomatically. r0: the back-translations in `translations_v0_62_r0.json` were written by the same model in the same session in a separate pass; they are **not independent** and serve only as a first check. r1 replaces them with back-translations made in a fresh session that is given only the target-language file.
3. **Comparison.** Each back-translation is compared with the English source and coded *equivalent*, *minor drift* (wording differs, meaning and answer format the same) or *meaning change*. Any meaning change is fixed in the forward translation, which is then back-translated again. The record (item, code, change) is part of the lock.
4. **Native-speaker review (proposed; the pre-registrant's decision, §9 question 1).** One fluent reader per language reviews the 30 category questions, the five templates, the 15 category labels and the alias table (§4) for naturalness and scope, about an hour each. Any change goes back through steps 2–3. Without this review the paper states that the translations were model-made and checked by back-translation only (§8).
5. **Freeze.** The probe files are rebuilt by `build_translated_probes_v0_62.py`, their SHA-256 entered in the lock manifest; every sent prompt must equal its probe text byte for byte (gate P3).

### §3.3 Checklist (applied to every item)

1. **Category scope.** The category noun covers the same set of brands as the US English one. FR "casque" alone also means helmet, so "casques audio". US "cosmetics" means colour cosmetics, while FR "cosmétiques" and JA 化粧品/コスメ include skincare, which would merge v0.21 into v0.20: every v0.21 item uses FR "maquillage" and JA メイクアップ (so the English distinction between "cosmetics" and "makeup" items is not kept; recorded as a translation note).
2. **Speech act and answer format.** Question form kept; "List several" and "Name several" kept distinct (FR Énumérez / Citez; JA 挙げてください / 名前を挙げてください); "with descriptions" kept; "Answer yes or no" uses the language's own answer words (oui/non; はい/いいえ).
3. **Nothing added or removed.** No country, market, currency, example or brand not in the source; no hedges or politeness formulas beyond the target language's neutral register. Exception declared: FR v0.23 template "la marque {BRAND}" (avoids elision variants such as d'Hennessy; the English already says "as a premium spirits brand").
4. **Names kept in Latin script.** Brands (exactly as in the registry), publications (Whisky Advocate, Wine Enthusiast, The Spirits Business) and competitions (San Francisco World Spirits Competition, IWSC, International Spirits Challenge).
5. **No cultural substitution.** No French or Japanese publication, competition or category is swapped in for an American one.
6. **Superlatives and evaluative weight preserved** ("best", "most", "highest quality", "cult-favorite"), without strengthening or softening.
7. **Register.** FR vous; JA です/ます. No system prompt.
8. **Typography.** Unicode NFC; FR ordinary spaces before ? ! : ; (no no-break spaces, checked by the build script); JA full-width question mark, brand in corner brackets in Phase A so that Latin script and kana do not run together.
9. **Length.** A translation more than twice the source length in characters (JA counted at two characters per Latin letter-equivalent) is re-checked for additions.
10. **Back-translation agreement** (§3.2 step 3).

### §3.4 Status in r0

All 30 + 5 + 15 items are translated and back-translated (`osf/v62/translations/translation_review_v0_62_r0.md`); six items carry a note asking for a native check (v19 q1, v20 q6, v21 q1 with the v0.21 scope rule, v22 q4, v23 EA-1 and CC-1); the FR v0.23 template carries a declared change (§3.3 item 3). Build check: PASS (`osf/v62/translations/build_check_v0_62_r0.txt`: 142 probes per language, 30 + 112, 112 of 112 Phase A prompts carry the registry brand string verbatim, 0 unfilled placeholders, 0 no-break spaces).

---

## §4 Brand names per language

### §4.1 In the questions

Brand names appear in Phase A only. Both languages use the registry string in **Latin script**, exactly as the English probe has it (e.g. "Sennheiser", "L'Oréal Paris", "Clé de Peau Beauté"). Reason: the stimulus stays identical across the three languages; a katakana form would add a translation choice per brand, and the models' Japanese answers commonly carry Latin-script brand names. The alternative (katakana in the Japanese question, Latin in parentheses) is not adopted; it would change the stimulus for 112 items.

### §4.2 In the answers (coding aliases)

Answers name brands in whatever script the model chooses. `osf/v62/translations/brand_aliases_v0_62_r0.csv` (112 rows, one per unit) gives:
- **Japanese aliases:** katakana (and, where standard, kanji) forms, 129 aliases over 111 units (ZMF Headphones has none; the build check counts them), e.g. ゼンハイザー (Sennheiser), トヨタ (Toyota), 日産 and ニッサン (Nissan), ヒョンデ, ヒュンダイ and 現代自動車 (Hyundai), ドゥ・ラ・メール (La Mer, its Japanese market name). Words that are only a part of a brand name and common on their own are not aliases (ファイナル for Final Audio, ポーラ for Paula's Choice, マック for MAC Cosmetics, エルフ for e.l.f. Cosmetics, 本田 for Honda).
- **French forms:** unaccented spellings for accented names (Lancome, L'Oreal Paris, Estee Lauder, Cle de Peau Beaute, Patron, Remy Martin). No French-specific brand name was identified.
Every alias was a draft from the runner's knowledge in r0. **r1:** `brand_aliases_v0_62_r1.csv` carries, per unit, the check status, the source opened (the brand's Japanese site and/or the Japanese Wikipedia article linked from the English one) and the access date (`check_aliases_v0_62.py` → `alias_check_v0_62_r1.csv`, 2026-11-10): 51 units confirmed, 4 partly confirmed, 55 unconfirmed (no reachable source showed the form), 1 without alias, 1 changed from a source (Lucid: ルシード added). Unconfirmed aliases stay in force (they are spelling transcriptions) and are flagged for the native review. Four more rows changed for **parity with the certified English matchers**, which count only the full registry string (v0.20–v0.22 `detect_mention`; e.g. "Mercedes-Benz", "Milani Cosmetics"): an alias may not be looser than the English rule, so bare ベンツ and bare クレ・ド・ポー are dropped, ミラニ becomes ミラニ・コスメティックス, and the company forms ニッカウヰスキー / ニッカウイスキー are added for Nikka (v0.23's English rule counts "Nikka Whisky"). The same parity reason settles r0's open note on bare ディオール / シャネル / ロレアル: not aliases, because the English rule does not count bare "Dior", "Chanel" or "L'Oréal". The French unaccented forms are redundant with the certified matchers (which strip accents) and harmless.

### §4.3 Matching (implemented in r1; fixed now)

The certified English matchers of each category (v0.42 §5.1) stay unchanged. A new, language-specific **pre-step** prepares French and Japanese answers before they reach them:
1. Unicode NFC; full-width Latin letters, digits and signs and half-width katakana → their ordinary forms (NFKC, r1: ＢＭＷ → BMW, ﾄﾖﾀ → トヨタ); ideographic space → space; typographic apostrophes → '; no-break and narrow no-break spaces → space; URLs removed (`strip_urls`, byte copy of v0.42's).
2. **Alias canonicalisation:** each occurrence of a Japanese alias or a French spelling variant is replaced by " <registry name> ". A Japanese alias matches with optional separators (・, ･, half- or full-width space) at its word joints and only when not preceded or followed by another katakana character (U+30A1–U+30FA, ー), so that ソニー matches in ソニーの but コス does not match inside コスメ or コスプレ. Kanji aliases match as written. r1: the two loan words of registry names match in both common spellings, ビューティ / ビューティー and コスメティクス / コスメティックス, and the middle dot · is a separator.
3. **Script-boundary spacing:** a space is inserted at every transition between a Latin letter or digit and a kana or CJK character. Python's word boundary treats kana as word characters, so without this step "Sennheiserの" would not match a whole-word English pattern.
4. The certified matcher runs on the result.
The same pre-step feeds v1.14's rank extractor (§2.4). **Collision-prone aliases** (Koss コス, Rhode ロード, Jaguar ジャガー, Mercury マーキュリー, Saturn サターン) are counted like any alias and every match is exported for audit (MC_Alias). Gate P2 (§7.3) proves that the pre-step changes nothing on English text.

### §4.4 Recognition answers (Phase A)

v0.19–v0.22 (yes/no): a leading oui/non (FR) or はい/いいえ (JA), after the pre-step's normalisation and ignoring punctuation and case, is mapped to "Yes"/"No" and the answer passed to the certified parser `parse_yes_no` unchanged; answers in English are passed as they are. Unparsed answers are counted as non-answers (v0.42 C6). v0.23 (open answers): the t₁–t₄ recognition judge (`score_v0_23.score_phase_a`, Claude Sonnet 4.5), its English instruction unchanged, reading the French or Japanese answer; coding, not acquisition. Claude Sonnet 4.5 retires on 2026-11-30: if the v0.62 judge calls cannot finish by then, the successor judge that t₅ adopts is used with t₅'s parity check, and the change is logged in DEVIATIONS.

---

## §5 Probes and collection

### §5.1 Probe files

`osf/v62/translations/probes_fr_v0_62_r0.jsonl` and `probes_ja_v0_62_r0.jsonl`: 142 lines each, the t₄ probe IDs and order, each line carrying the English source prompt beside the translated one; built by `python3 osf/v62/scripts/build_translated_probes_v0_62.py` (r0 SHA-256: FR `aef89ae4…5b587a`, JA `60720f7e…cfae744`; they change with any translation fix before the lock).

### §5.2 Design and order

| Block (collection order) | Phase | Languages | Run | Calls per model | Calls (N3) |
|---|---|---|---|---|---|
| 1 | B (30 category questions) | FR, JA | 1 | 60 | 180 |
| 2 | B | FR, JA | 2 | 60 | 180 |
| 3 | B | FR, JA | 3 | 60 | 180 |
| 4 | A, v0.19–v0.22 yes/no (88 per language) | FR, JA | 1 | 176 | 528 |
| 5 | A, v0.23 open (24 per language) | FR, JA | 1 | 48 | 144 |
| **Total** | | | | **404** | **1,212** |

Within a block, one worker per model, the three in parallel, FR before JA, probes in file order. The order puts every answer that a confirmatory test needs (blocks 1–3: Presence, Consistency, Ranking) before the brand questions, which feed descriptives only, so that a budget stop can only cut descriptives.

**Why this design is the fewest calls that keep the tests valid.** Phase B three runs per language is what t₄ used for its English values: a one-run French or Japanese π̂ compared with a three-run English π̂ would attenuate ρ toward FALSIFIED for a reason that is not language; φ needs at least two defined runs; the run-to-run noise floor (§2.9, item 1) needs run pairs. Phase A one run as in t₄. Search on (S1) is not collected: it is the most expensive condition (§6.4) and its answers depend on the web on the day, so a language contrast in S1 would mix language with the search results each language retrieves; the English S1 answers of t₄ remain for the component papers.

### §5.3 Panel

N3 as verified for v0.42 r2 on 2026-11-10 from each vendor's own documentation (`osf/v42/prereg/PRE_REGISTRATION_v0_42.md` §4.3): Claude Fable 5.2 (`claude-fable-5-2`), GPT-6 Astra (`gpt-6-astra`), Gemini 4 Argon (`gemini-4-argon`), one flagship per provider (budget rule). The IDs are re-verified at the final pre-registration. The comparison requires the models of the English values, so a newer flagship released before the collection is not substituted; it is reported. Cheaper tiers are not used for the same reason.

### §5.4 Call settings

Exactly t₄'s S0 settings (v0.42 r2 §4.4): no tools; no system prompt; temperature, top-p and reasoning effort at provider defaults (Claude Fable 5.2 accepts none; its adaptive thinking is on); maximum output 16,384 tokens; Claude Fable 5.2 through Anthropic's Message Batches API with the synchronous call's parameters, GPT-6 Astra and Gemini 4 Argon synchronous; v0.42's retry policy and re-run pass. No language, locale or region parameter is set on any call. The call functions are byte copies of v0.42's (test in r1). Raw artefact `osf/v62/data/v62_raw.jsonl` with v0.42's fields plus `language`.

### §5.5 Window and guards

- **Window.** 2026-11-29 00:00 to 2026-12-02 24:00 US Central; no request after the earlier of the window's end and 72 hours after the first recorded call. First call planned on 2026-11-29 (November prices for Gemini 4 Argon). The script refuses to collect during 2026-11-17 to 2026-11-21.
- **One collection at a time.** `--collect` refuses while another acquisition process is running on the machine.
- **Anchor.** `--collect` refuses unless the tag is on `origin` and the OSF anchor file names the tag's commit.
- **Slip.** A DEVIATIONS entry naming the new dates and the reason, committed before the first call; the budget guard and 72-hour rule unchanged. A collection after t₅ bills Gemini 4 Argon at December prices (§6).

---

## §6 Budget

### §6.1 Cap and prices

At most $100 of paid model calls for this paper, both languages together, including re-sends and the v0.23 judge; pause at $80; both from actual recorded usage (programme rule, 2026-11-10; it overrides any larger figure). Prices (programme list read 2026-11-10, US$ per 1M tokens in / out; vendor sources in v0.42 r2 §4.5): Claude Fable 5.2 8 / 40 standard, **4 / 20 batch (used)**; GPT-6 Astra **10 / 50 standard (used)**; batch 5 / 25 is listed by OpenAI but not used, as in t₄, so that call mode matches the English values; Gemini 4 Argon **2 / 10 through 2026-11-30, 4 / 20 from 2026-12-01** (standard; no batch price listed); judge Claude Sonnet 4.5 3 / 15. Re-read at the final pre-registration.

### §6.2 Per-call basis and the language factor

- **English basis.** v0.42 r2's measured-basis figures per call (`osf/v62/inputs/cost_estimate_v0_42_r2.json`, design "r2 (adopted)", SHA-256 checked), central / high with re-sends: Claude Fable 5.2 (batch) category 0.0750 / 0.1490, yes/no 0.0344 / 0.0789, open 0.0750 / 0.1490; GPT-6 Astra 0.0349 / 0.0511, 0.0193 / 0.0284, 0.0349 / 0.0511; Gemini 4 Argon at November prices 0.0135 / 0.0262, 0.0058 / 0.0175, 0.0135 / 0.0262 (December rows of the same file at 4 / 20). The high basis already assumes Claude Fable 5.2 at three times Claude Opus 5.5's v0.39 token use.
- **Language factor (assumption, not measured).** French and Japanese prompts and answers are assumed to cost more tokens than English ones: central FR 1.25, JA 1.50; high FR 1.50, JA 2.00, applied to the whole per-call cost. No French or Japanese answer from these models is on record and no tokenizer is installed on the collection machine, so these are declared planning values. At the final pre-registration the English basis is replaced by t₄'s recorded usage (S0, per model and question type); during collection the projection pause (§6.5) uses actual usage, and the measured factor is reported (§2.9, item 3).
- **Judge reserve.** 144 open answers × (1,500 input tokens × 2.00 + 10 output tokens) on Claude Sonnet 4.5 = **$1.32** (v0.42 r2's per-answer bound, times the high JA factor).

### §6.3 Estimate of the adopted design (US$, expected / high)

| Language × model | Calls | November prices | December prices |
|---|---|---|---|
| FR, Claude Fable 5.2 (batch) | 202 | 14.48 / 35.90 | 14.48 / 35.90 |
| FR, GPT-6 Astra | 202 | 7.10 / 12.48 | 7.10 / 12.48 |
| FR, Gemini 4 Argon | 202 | 2.56 / 6.80 | 5.13 / 13.59 |
| JA, Claude Fable 5.2 (batch) | 202 | 17.37 / 47.87 | 17.37 / 47.87 |
| JA, GPT-6 Astra | 202 | 8.52 / 16.64 | 8.52 / 16.64 |
| JA, Gemini 4 Argon | 202 | 3.08 / 9.06 | 6.15 / 18.12 |
| Judge reserve | (144) | 1.32 / 1.32 | 1.32 / 1.32 |
| **All** | **1,212** | **54.42 / 130.06** | **60.06 / 145.92** |
| of which blocks 1–3 (Phase B, every confirmatory test) | 540 | 30.57 / 71.29 | 33.92 / 79.55 |

(Cells rounded; totals from unrounded values; `cost_estimate_v0_62_r1.txt`. The by-phase lines of that file now list the judge reserve as a line of its own: Phase B + Phase A yes/no + Phase A open = $33.92 + $15.78 + $9.04 = $58.74 at December prices, plus the $1.32 reserve = $60.06; high $79.55 + $43.84 + $21.21 = $144.60 + $1.32 = $145.92. r0's printout omitted the reserve line, which made the phase lines look $1.32 short.) At English token counts (factor 1.0) the design would cost $39.94 / $74.89 at November prices.

**Reading.** The expected cost is below the $80 pause at either price. The high scenario is above the cap, as t₄'s was ($135.62 high); it combines the high Fable basis with the high language factor. Under it the guard ends the collection inside Phase A, after blocks 1–3 are complete: no confirmatory test is lost, only recognition descriptives. **Correction (r1):** the guard counts the $1.32 judge reserve in the spend from the first call (§6.5), so at the end of blocks 1–3 the guard's spend is $72.61 at November prices but **$80.87 at December prices** (high scenario): at December prices the $80 pause is reached inside block 3, and the last Phase B calls wait for the pre-registrant's `--approve-past-80`. They are paused, not lost; the hard stop ($100) is not near. At the expected cost the figure is $31.88 / $35.24. Break-even: on the high basis the full design reaches $80 at a uniform language factor of 1.07 (November) and $100 at 1.34; at December prices 0.95 and 1.19.

### §6.4 Design trade-off (November prices, expected / high)

| Design | Calls | Expected | High |
|---|---|---|---|
| **Adopted: FR + JA, Phase B S0 × 3, Phase A S0 × 1** | **1,212** | **54.42** | **130.06** |
| French only | 606 | 24.80 | 55.84 |
| Japanese only | 606 | 29.62 | 74.23 |
| Fallback F1: Phase B S0 × 3 only (no Phase A) | 540 | 30.57 | 71.29 |
| Fallback F2: Phase B S0 × 2 + Phase A | 1,032 | 44.23 | 106.30 |
| Phase B S0 × 1 + Phase A (no φ, no noise floor; not adopted) | 852 | 34.04 | 82.53 |
| Phase B S0 × 3 + Phase A × 3 (not adopted) | 2,556 | 99.50 | 244.97 |
| Adopted + Phase B S1 × 1 (not adopted) | 1,392 | 95.36 | 245.37 |
| Adopted + Phase B S1 × 3 (t₄'s full design; not adopted) | 1,752 | 177.23 | 475.99 |

What the design gives up: search-on answers in French and Japanese; Phase A runs 2–3; within-provider replication (one model per provider, as t₄). What it keeps: every t₄ S0 question in both languages, on the same models, with the run structure of the English values.

### §6.5 Guard (from actual usage)

v0.42's ledger, forked unchanged in its arithmetic: spend = judge reserve + the cost of every raw line written, from its recorded usage at the listed prices (each request priced at the price of the UTC date it started); before each request its worst case is reserved (16,384 output tokens, 2,000 input tokens: $0.3357 Claude Fable 5.2 batch, $0.8392 GPT-6 Astra, $0.1678 / $0.3357 Gemini 4 Argon in November / December; v0.44 r1 §4.5).
1. **Hard stop:** no request if spend + reservations + its worst case would exceed $100.
2. **Pause at $80:** no new request until the pre-registrant's OK is recorded (`--approve-past-80`).
3. **Projection pause:** after block 1, projected total = actual call spend (r1: without the judge reserve, which the ratio's numerator already contains) × 5.3413 (November; 5.3122 if block 1 starts on or after 2026-12-01; adopted ÷ block 1, central, from `cost_estimate_v0_62_r0.json`). If it exceeds $80 (block-1 spend above $14.98 November, $15.06 December), collection pauses and the pre-registrant chooses: continue (`--approve-projection`), F1 (drop Phase A), or F2 (drop Phase B run 3; `H_Lang_Phi` then needs φ defined in both remaining runs, and the English comparator stays the three-run t₄ value, a declared asymmetry).
At the expected cost none of these is reached (block 1 ≈ $10.19); at the high scenario block 1 ≈ $23.76 triggers the projection pause.

---

## §7 Analysis plan

### §7.1 Coding

Phase B mentions: the pre-step of §4.3, then each category's certified matcher as v0.42's coder calls it (`code_t4_v0_42.py`: v0.20–v0.22 `detect_mention`; v0.19 `acquire_v0_19` brand patterns; v0.23 `score_v0_23.score_phase_b` with `dry_run=True`). Phase A: §4.4. Coder `osf/v62/scripts/code_v0_62.py` (r1), which adds only the pre-step and the answer-word mapping and writes prepared copies of the raw answers per language; v0.42's coder (`code_t4_v0_42.py`) then runs unchanged on each prepared copy (r1: as a separate process, because the v0.62 branch does not contain osf/v41–v42 and v0.42's coder re-executes itself with its own ROOT shim).

### §7.2 Computation

`osf/v62/scripts/score_v0_62.py` (r1), written and tested on synthetic data before the lock and run once after the gates. r1 draft: it carries transcriptions of the π̂ and φ kernels (`score_v41.phi_m`, `score_v0_42.pi_hat` / `phi_panel`) and of v0.44's centred ρ and permutation, because the v0.62 branch does not contain osf/v41–v42; gate P1 must show that the transcriptions reproduce v0.42's English t₄ values exactly before the lock, or the v0.42 scripts are merged and imported instead. R\* values (§2.4) are an input from v1.14's own scorer. The English comparator values are read from v0.42's and v1.14's committed outputs, each read logged with its git blob and SHA-256.

### §7.3 Gates (before any statistic)

- **P1 (kernel parity).** The imported kernels reproduce v0.42's English t₄ k, π̂ and φ for all 112 brands exactly from t₄'s coded tables.
- **P2 (pre-step is inert on English).** The pre-step + certified matchers applied to all English t₄ answers reproduce v0.42's locked t₄ mention and recognition codes exactly (0 changed cells). Any changed cell stops scoring until explained in DEVIATIONS.
- **P3 (probe parity).** The probe files' SHA-256 equal the lock manifest; every sent prompt equals its probe text byte for byte.
- **P4 (alias reach).** For every alias, a synthetic French or Japanese sentence containing it (inside particles, lists, Markdown bold and after a number) is coded as a mention of its unit and of no other unit, by the full pipeline; and a fixed list of decoy strings (コスメ, コスプレ, ロードバイク, ファイナル, マック, エルフ, ポーラ) yields no mention.

### §7.4 Drop rule and missing data

As v0.42 §5.4 per language: a model × language × phase with fewer than 90% of its calls answered after the re-run pass is excluded from that language's statistics for that phase. `H_Lang_Presence`, `H_Lang_Phi` and `H_Lang_Rank` in language L need all three models in Phase B in L; otherwise they are UNDETERMINED for L and reported on the remaining models as descriptives. Calls not sent because of a budget stop count as unanswered. No imputation.

### §7.5 Sensitivities (reported; no verdict changes)

- **S-Denon.** Every test without the v0.19 unit flagged in DEVIATIONS Entry 0 (Denon): 111 units.
- **S-Headphones.** Every test without the v0.19 category: 96 units (r1 correction: r0 said 88; 112 − 16 = 96) (DEVIATIONS Entry 0).
- **S-Language.** Every test without off-language answers (MC_Language).
- **S-Alias.** Every test with the collision-prone aliases (§4.3) switched off.
- **S-Uncentred.** The uncentred ρ (v0.41/v0.42 convention).
If a primary verdict differs under S-Denon or S-Headphones, the paper reports both in its abstract.

### §7.6 Reporting

Every test, including failures and undetermined results, with per-category breakdowns; the raw answers, coded tables and verdicts in the OSF deposit. Public-study rules apply: no focal brand, no lessons addressed to a brand, no brand contacted.

---

## §8 Limitations

1. Translations are model-made; the back-translation check is weaker than a full committee translation, and without native review (§3.2 step 4) naturalness is unverified.
2. The forward translator (Claude) belongs to the same provider as one of the three measured models.
3. Language is varied without a market: the brand registries are US-market selections, and a French or Japanese user would also ask about brands that are absent here. The study tests whether the same brands are ordered alike, not which brands matter in France or Japan.
4. The English values (t₄, mid-November) and the French and Japanese collection (late November or early December) are some two to three weeks apart; time and language are confounded, which §2.7's t₅ benchmark addresses only if t₅ is scored in time.
5. Search off only: the results describe the models' own knowledge in each language, not what a search-enabled assistant would retrieve.
6. Japanese coding rests on a new alias table and pre-step; aliases are drafts until checked (§4.2), and some katakana names are also common words (MC_Alias).
7. One model per provider and three runs: within-provider replication is absent and run noise is estimated coarsely, as at t₄.
8. Two languages chosen by the roadmap; they do not stand for all non-English languages.
9. Cost assumptions for French and Japanese token use are unmeasured until collection (§6.2).

---

## §9 Decisions for the pre-registrant (before r1)

1. **Native-speaker review.** Proposed: one fluent reader each for French and Japanese, about an hour each (contacting anyone is the pre-registrant's decision). Without it, §8 limitation 1 stands and the paper says so.
2. **Window.** Proposed: 2026-11-29 to 2026-12-02, first call 2026-11-29 (before t₅; November price for Gemini 4 Argon). Alternative: after t₅ (expected $60.06, December prices).
3. **COI handling for the headphones category** (DEVIATIONS Entry 0): proposed option A (registry unchanged, Denon included, disclosed, with the S-Denon and S-Headphones sensitivities); alternatives B (Phase A without the Denon question) and C (headphones category not collected).
4. **v0.21 scope rule.** FR "maquillage" / JA メイクアップ for every cosmetics item (§3.3 item 1), accepting the loss of the English cosmetics/makeup wording difference.
**Each of questions 1–3 is one parameter (r1):** `HEADPHONES_OPTION = "A"` and `WINDOW = ("2026-11-29", "2026-12-02")` in `osf/v62/scripts/params_v0_62.py` (read by the acquisition, cost, coding and scoring scripts; a window touching 2026-11-17..21 is refused), and the native review changes only the translation files. The pre-registrant's answer becomes a one-line edit plus a change-log line.
Settled in r0 by the runner (can be overruled): Latin script for brand names in the questions (§4.1); search off only (§5.2); Ranking conditional on v1.14 (§2.4); centred ρ (§2.1).

---

## §10 Declarations

## Conflict of interest {-}

The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. This study re-asks, in French and in Japanese, questions against brand registries fixed in earlier phases (v0.19–v0.23); it performs no new brand selection, and each registry carries its source-phase conflict-of-interest handling forward. In the automotive registry, Samsung subsidiaries hold tier-2/3 component supply relationships with several registry brands — Harman International (audio systems), Samsung SDI (battery cells), and Samsung Display (infotainment) — characterized in the source phase as non-competitive, with no brand-level overlap, and imposing no operational restriction on registry composition (v0.22 Declarations; screened in v0.22 DEVIATIONS Entry 0, Part B). In the audiophile-headphones registry, AKG was substituted with Denon before the v0.19 pre-registration lock because AKG's parent, Harman International, is a Samsung subsidiary. Correction (November 10, 2026): Denon, which replaced AKG in the v0.19 registry, has itself been owned by Harman International, a wholly owned subsidiary of Samsung Electronics, since September 23, 2025, when Harman completed its acquisition of Sound United from Masimo; the v0.19 headphones registry therefore includes one Samsung-group brand. The substitution did not achieve its purpose, and this was not noticed until November 10, 2026. Because this study is a new collection that includes the headphones category, in which Samsung Electronics and Harman International (whose brands include JBL, AKG and Harman Kardon) sell products, a pre-acquisition screen (DEVIATIONS Entry 0) kept the v0.19 registry unchanged, Denon included, so that the French and Japanese values remain comparable with the English ones, and pre-registered two sensitivity analyses, one without the Denon unit and one without the headphones category, reported beside every test. A string screen of the 112 registry names against the Samsung-group names of record found no other Samsung-group brand among the registry units (DEVIATIONS Entry 0); brands named in answers outside the registries are not coded. Acquisition, coding and scoring are fully automated against the locked registries, and this pre-registration is locked and deposited before the first call. Samsung Electronics had no role in the design, conduct, analysis or reporting of this work.

## Funding {-}

Self-funded.

## Ethics {-}

Not applicable; no human subjects.

## Use of AI tools {-}

During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.

---

## §11 Lock procedure and change log

- **r0** (2026-11-10, this draft): design, translations and back-translations (non-independent), alias table, cost estimate, DEVIATIONS Entry 0 (proposed), for the pre-registrant's first look. Not for deposit as a lockable text.
- **r1** (planned): the pre-registrant's answers to §9; independent back-translations and the comparison record; native review if approved; checked aliases with sources; the country column for §2.9 item 5; acquisition, coding and scoring scripts with tests (local fakes only); gates P1, P2 and P4 run on t₄ data once v0.42's acquisition is locked; the cost basis re-based on t₄'s recorded usage; prices and model IDs re-read; lock manifest.
- **Lock:** 24 hours after the pre-registrant receives the final text unless he objects; then manifest, commit, tag `v0.62-prereg-r1`, push, OSF deposit of `osf/v62/prereg/` and `osf/v62/anchor/` with SHA-256 verified; only then `--collect`.

**Change log**

- 2026-11-10, r0 written (no earlier revision).
- 2026-11-10, r1 working draft (lane 9): see "Changes from r0".

### Changes from r0 (r1 working draft, 2026-11-10)

1. Scripts written, with unittest tests on local fakes (no network, no model): `acquire_v0_62.py` (dry run by default; fork of v0.44's, call functions byte-copied from v0.42), `budget_v0_62.py`, `params_v0_62.py`, `code_v0_62.py`, `score_v0_62.py`, `check_aliases_v0_62.py`, `make_alias_table_r1_v0_62.py`; tests `osf/v62/scripts/tests/` (48 tests).
2. The three open choices are parameters: headphones option and window in `params_v0_62.py`; option B removes the Denon Phase A probe (1,206 calls), option C the v0.19 category (1,008 calls); costs per option in `cost_estimate_v0_62_r1.txt`.
3. Collection blocks: Phase A is split into block 4 (yes/no) and block 5 (open), as r0's table already listed; fallback F1 is `--drop-phase-a`, F2 `--drop-run-3`.
4. Cost script reconciled (§6.3): the by-phase lines omitted the $1.32 judge reserve; it is now printed as its own line with a sum check. No total changes.
5. Correction (§6.3): with the judge reserve counted from the first call, the December high scenario reaches the $80 pause inside block 3 ($80.87 at the end of blocks 1–3); r0 said blocks 1–3 stay under $80 at December prices. November: $72.61.
6. Projection pause (§6.5): computed on the call spend without the judge reserve (the ratio's numerator already contains it); thresholds unchanged ($14.98 / $15.06).
7. Correction (§7.5, DEVIATIONS Entry 0): without the headphones category 96 units remain, not 88.
8. Alias table r1 (§4.2): check record with sources and dates; Lucid gains ルシード; parity changes for Mercedes-Benz, Clé de Peau Beauté, Milani Cosmetics; Nikka gains ニッカウヰスキー / ニッカウイスキー.
9. Pre-step (§4.3): full-width and half-width normalisation; ビューティ(ー) and コスメティ(ッ)クス spelling variants; · as a separator.
10. Coding and scoring architecture (§7.1, §7.2): v0.42's coder runs as a separate process on prepared copies; the scorer carries transcribed kernels pending gate P1 (or a merge of the v0.42 scripts).
11. Open issue for the lock (not changed): the pre-step maps typographic apostrophes to ', which the certified English matchers do not; gate P2 (pre-step inert on English) will fail on any English t₄ answer that writes a registry name with ’ (e.g. Paula’s Choice, L’Oréal Paris). Either P2 is read on the mention cells after the same mapping is applied to English, or the mapping is dropped (French answers, which commonly write L’Oréal, would then under-match).

