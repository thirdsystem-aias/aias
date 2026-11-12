
# AIAS™ Presence Measurement Protocol — Pre-Registration v0.62 (revision r3, WORKING DRAFT — not locked, not final)

Pablo Ulpiano González Castro
School of Visual Arts, MPS Branding Program, New York, NY (primary academic affiliation)
Third System™ (research entity; data archive and methodology venue)
Correspondence: pablou@pablou.com · pablou.com
ORCID: 0009-0003-8968-9990 (linked: https://orcid.org/0009-0003-8968-9990)

**Study:** The non-English wave — do AI availability scores measured in Spanish, in Korean and in Chinese reproduce the English values of the t₄ wave?
**Languages (r2):** Spanish (neutral Latin American usage), Korean (South Korea, standard), Chinese (**Simplified script, Mainland usage**, zh-Hans-CN). They replace r0/r1's French and Japanese (pre-registrant's decision, 2026-11-10, 20:44 CT; §0).
**Design:** The t₄ panel (v0.42 r2): the five omnibus categories (v0.19 audiophile headphones, v0.20 skincare, v0.21 cosmetics, v0.22 automotive, v0.23 premium spirits; 112 brand units), asked of the same three models as t₄ (N3: Claude Fable 5.2, GPT-6 Astra, Gemini 4 Argon) without web search (S0). **Adopted core: the 30 category questions (Phase B) in all three languages, three runs: 3 × 3 × 30 × 3 = 810 calls.** **Decided 2026-11-12 (§9 item 7 (b)): the 88 yes/no brand questions (Phase A, v0.19–v0.22; block 4, one run; 792 calls) are collected last, after the three category runs, under the same $80 pause and $100 stop (`params_v0_62.BRAND_YES_NO = True`); the 24 open brand questions (v0.23; block 5) are not collected (`BRAND_EXTRAS = False`). Adopted design: 1,602 calls.** (r3 had put the 112 brand questions to the pre-registrant as an option, off by default.)
**Budget:** at most US$100 of paid model calls for the paper, hard cap; pause at $80; both from actual recorded usage (programme rule, 2026-11-10). **r3: re-based on t₄'s recorded usage** (v0.42, tag `v0.42-acquisition-locked`; §6). Core (810 calls): **central $33.44** if collected on 2026-11-29/30 as planned ($38.84 at December prices); **conservative high $121.80** (December prices for every call). Full design with extras (1,818 calls): central $69.23 / $76.79, conservative high $185.38. The conservative high of the core exceeds the cap; §6.3 states what the guard does (a projection pause after block 1) and what the pre-registrant decides. **Adopted design (r3 update, core + block 4, 1,602 calls): central $34.52 ($39.98 at December prices), conservative high $124.77; block 4 alone $1.09 / $1.15 central, $2.97 conservative high; at the conservative high the $100 stop falls in run 3, before block 4 (§6.3).** All figures: `python3 osf/v62/scripts/cost_estimate_r3_v0_62.py` (output `osf/v62/prereg/cost_estimate_v0_62_r3.txt`); r2's proxy-basis figures (core $55.50 / $142.06) are superseded.
**Protocol version:** recall Presence π̂ and recognition (v1.6, SSRN 6816340), Consistency φ (v1.8, SSRN 6963359), both as implemented for t₄ in `osf/v42/scripts/score_v0_42.py` (locked, tag `v0.42-prereg-r1` → `58d1891`); Ranking, only if v1.14 passes (§2.4), as v1.14 defines it (modal position R\*, tag `v1.14-prereg-r1`).
**Pre-registrant:** Pablo Ulpiano González Castro
**Status:** r3 working draft (2026-11-11, programme runner, lane v0.62-r3), built on r2; every change is listed in §11 "Changes from r2 (r3)" (r2's own change list is kept below it). **Updated 2026-11-12 (r3 update, §11): the pre-registrant's decisions on §9 items 3, 7 and 8 applied (item 7 (b) with its parameter and tests, as r3 described it), dated change-log lines, the cost of the adopted design, the re-run fake-SDK dry run and the list of files the lock manifest will cover; no hypothesis, test, threshold, unit set, model or analysis changed.** No study probe has been sent and none will be before the lock.
**Lock target:** git tag `v0.62-prereg-r1` on branch `v0.62`, pushed to `origin`; external anchor: deposit of the pre-registration, the English source probes, the Spanish, Korean and Chinese probe files with their back-translations and review record, the alias table, the cost estimate, DEVIATIONS.md, the scripts and tests and the lock manifest at OSF `ec6wh` → `v62/prereg/` and `v62/anchor/` before the first call. Locks 24 hours after the pre-registrant receives the final text, unless he objects (programme rule, Nov 9, 2026); the 24 hours of this r3 start when he receives it.
**Collection window:** 2026-11-29 00:00 to 2026-12-02 24:00 US Central, all calls within 72 hours of the first (default (2) of 2026-11-10, kept). Constraints: after the lock; one paid collection at a time on the collection machine; never 2026-11-17 to 2026-11-21; before the t₅ wave (target 2026-12-03).
**Paper:** one Non-English paper for the three languages, about 2027-01-15.

---

## §0 Programme position, phase number and the language change

- **Language change (r2).** The pre-registrant decided on 2026-11-10 (20:44 CT) that the non-English wave runs in Spanish, Korean and Chinese, replacing French and Japanese. Rationale (his): the languages of his current student cohort (SVA MPS Branding, Class of 2027) include Spanish, Korean and Chinese and no French or Japanese, so the study speaks to the users the programme teaches and native readers are within reach for the translation checks (§3.2). Chinese is **Simplified, Mainland usage**, the default the decision names; the pre-registrant may change it before the lock (§9).
- **Study inventory.** r0/r1 covered the roadmap's "French full panel" and "Japanese full panel" items (studies #52/#53). The study list entries are the pre-registrant's to relabel (§9 item 5); this draft changes no other study. The cross-cultural identity-load study (#55) remains separate: no identity-load variable, hypothesis or market contrast is defined here.
- **Phase number v0.62** unchanged (first number neither used by a branch nor reserved; r0 §0).
- **Industry breadth.** Not an aim: the five omnibus categories are kept because the question is a comparison with the English t₄ values on the same registries (programme rule: repeat waves keep the omnibus categories).

## §1 Context and question

Every AIAS™ measurement so far was taken in US English. A brand's AI availability describes what a model makes available to a person who asks; people ask in many languages, and a model's knowledge of brands need not be the same in each. If scores depend on the language of the question, an English-only measure describes English-speaking users only.

The t₄ wave (v0.42 r2; locked 2026-11-10, collecting from 2026-11-11) gives the English baseline. This study asks the same category questions, translated, of the same models with the same settings, and tests whether the brand orderings reproduce:

1. **Presence** (primary): does recall Presence order brands in Spanish, in Korean and in Chinese as it does in English?
2. **Consistency** (secondary): does φ order brands alike?
3. **Ranking** (secondary, conditional): if v1.14 passes, does Ranking order brands alike?
4. **Where they differ** (descriptive).

Three languages from three scripts (Latin, Hangul, Han) and three language families. Language is varied alone: no country, market or location is stated in any probe, and no system prompt is sent.

---

## §2 Pre-registered hypotheses

### §2.1 Definitions

- **Languages.** L ∈ {ES, KO, ZH}. EN = the English t₄ wave (v0.42).
- **Brand units.** The 112 units of the five omnibus registries, unchanged (16 + 24 + 24 + 24 + 24).
- **Comparator values (EN).** From v0.42's locked outputs (v0.42's scored brand table): π̂_{b,EN} = `pi_N3_S0`, φ_{b,EN} = `phi_N3_S0` with its partition, and, for Ranking, R\*_{b,EN} = v1.14's Stage 1 value at t₄, S0. If v0.42's drop rule excludes any N3 model in S0, the corresponding v0.62 test is UNDETERMINED.
- **k_{b,m,r,L}.** Number of the six Phase B questions of brand b's category whose answer by model m in run r in language L mentions b (§4, §7.1).
- **Recall Presence** π̂_{b,L} = Σ_m Σ_r k_{b,m,r,L} ÷ (answered Phase B calls of the category; 6 · 3 · 3 when complete); exactly v0.42's definition on N3, S0.
- **Consistency** φ_{b,L} = v0.42's definition (v1.8 per run on N3; mean over the runs whose partition is defined; undefined if fewer than 2 of 3 runs are defined). Higher φ = less consistent.
- **Ranking** R\*_{b,L} = v1.14's modal-position statistic, pooled over the 54 S0 answers of the brand's category in L, rated iff ≥ 6 rankable mentions.
- **ρ_c(x, y)**, **permutation p**, **bootstrap**: as r1 (centred pooled within-category Spearman; 10,000 within-category permutations, one-sided; 10,000 within-category bootstrap resamples, percentile 95%).
- **Seeds.** H_Lang_Presence 620101 (ES), 620102 (KO), 620103 (ZH); H_Lang_Phi 620111, 620112, 620113; H_Lang_Rank 620121, 620122, 620123; bootstrap 620131; descriptives 620141; gate P1 synthetic tables 620151–620153.
- **α.** 0.05 per test, no multiplicity correction (programme convention); verdicts rest on pre-set effect-size thresholds, and every test is reported.

### §2.2 PRIMARY: `H_Lang_Presence` (one test per language)

**Statement.** Asked in language L, the newest models order brands by recall Presence as they do in English.
**Operationalisation.** x = π̂_{b,EN}; y = π̂_{b,L}; all 112 brands; one test each for ES, KO, ZH.
**Verdict rule (per language).** CONFIRMED if ρ_c ≥ 0.70 and p < 0.05 · FALSIFIED if ρ_c < 0.50 · MARGINAL otherwise.
**Rationale.** 0.70 is the programme's stability bar (v0.34) and t₄'s generation test bar (v0.42 `H_Gen_Presence`); 0.50 its falsification line.
**Reported alongside.** Per-category ρ_c; the level shift Δ_L = mean(π̂_{b,L} − π̂_{b,EN}) with its bootstrap interval; per-model ρ_c; the uncentred value; sensitivities (§7.5).

### §2.3 SECONDARY: `H_Lang_Phi` (per language)

x = φ_{b,EN}; y = φ_{b,L}; brands with φ defined in both. UNDETERMINED if n < 40 · CONFIRMED if ρ_c ≥ 0.50 and p < 0.05 · FALSIFIED if ρ_c < 0.30 · MARGINAL otherwise. Reported alongside: partition counts; |ρ_c(φ_L, π̂_L)|, flagged if ≥ 0.50.

### §2.4 SECONDARY, CONDITIONAL: `H_Lang_Rank` (per language)

Tested only if v1.14 resolves PASS before v0.62 is scored (else NOT TESTED; deadline 2027-01-05). x = R\*_{b,EN}; y = R\*_{b,L}; units rated in both; categories with ≥ 5 such units. UNDETERMINED if n < 30 · CONFIRMED if ρ_c ≥ 0.50 and p < 0.05 · FALSIFIED if ρ_c < 0.30 or p ≥ 0.05 · MARGINAL otherwise. Degeneracy (> 80% of rated units sharing one R\*) → UNDETERMINED. Mention matching uses the pre-step of §4.3.

### §2.5 Where the languages differ (descriptive; no verdicts)

Per category and language: ρ_c, Δ_L with interval, share of units whose π̂ moves by more than 1/6. Labels fixed now: **language-stable** (ρ_c ≥ 0.70 and interval of Δ_L contains 0), **level-shifted** (ρ_c ≥ 0.70, interval excludes 0), **language-sensitive** (ρ_c < 0.50), otherwise **intermediate**. Also: ρ_c between each pair of languages (ES–KO, ES–ZH, KO–ZH); the 10 units with the largest |π̂_L − π̂_EN| per language, without commentary addressed to any brand.

### §2.6 Joint reading (fixed now)

**Language-robust** if `H_Lang_Presence` is CONFIRMED in all three languages; **language-dependent** if it is FALSIFIED in any (the paper names the languages); **partly robust** otherwise. `H_Lang_Phi` and `H_Lang_Rank` are reported beside this reading and do not change it.

### §2.7 Benchmark for time (no verdict)

As r1: if t₅ (English, target 2026-12-03) is scored before v0.62, ρ_c(π̂_{EN,t₄}, π̂_{EN,t₅}) is reported beside each `H_Lang_Presence` value (language gap = ρ_c(EN t₄, EN t₅) − ρ_c(EN t₄, L)), and ρ_c(π̂_{EN,t₅}, π̂_L). Otherwise reported as not available.

### §2.8 Manipulation checks

- **MC_Complete.** ≥ 98% of sent calls end with non-empty answer text after the retry policy; a model × language × phase below 90% triggers the drop rule (§7.4).
- **MC_Served.** Served model ID equals the requested ID (or a dated snapshot of it).
- **MC_Language (rule fixed now; implemented and unit-tested).** KO: Hangul syllables make up ≥ 50% of the answer's letters. ZH: Han characters make up ≥ 50% of the letters. ES: among the words of a fixed list of 20 Spanish and 20 English function words (listed in the coder), Spanish words outnumber English words. Below 95% for a model × language is flagged. Off-language answers are kept; sensitivity S-Language excludes them.
- **MC_Script (new, ZH).** Share of Chinese answers containing any of 24 fixed Traditional-only characters (listed in the coder, `ZH_TRAD`). Flagged above 5% per model; sensitivity S-Script excludes them. No character conversion is applied (§4.3).
- **MC_Alias.** Every match of a collision-prone alias (§4.3) is exported for audit; the audit is reported, never used to change a code.
- **MC_Truncation.** Share of calls ending at the output cap, per model × language; above 5% flagged.
- **MC_Window.** All calls within 72 hours. **MC_Parity.** Gates P1–P4 pass before any statistic. **MC_Budget.** Spend from recorded usage ≤ $100; every pause, approval and stop logged and reported with the calls not sent.

### §2.9 Pre-registered descriptives (no verdicts)

1. Run-to-run reliability of recall per model × language (rel1, rel3 as v0.42 §2.7) beside t₄'s English values.
2. Recognition (Phase A) per model × language beside English t₄, for the 88 yes/no brand questions of v0.19–v0.22 (block 4; §9 item 7 (b), decided 2026-11-12); v0.23's open brand questions are not collected, so the 24 spirits units have no recognition value.
3. Answer form per language: tokens (input, output, thinking) per call against English t₄ (the measured language factor that replaces §6's planning values), characters per answer, registry brands named per Phase B answer, finish reasons, refusals.
4. Script of brand mentions in KO and ZH answers: share of matched mentions written in Latin script vs Hangul / Han.
5. Home-language descriptive: Δ_L for units whose brand owner is headquartered where L is the main language; the country column is built from cited sources before the lock and used by no test.
6. Cost: tokens and spend per model × language from recorded usage.

---

## §3 Translation protocol

### §3.1 Source and items

The 142 English probes of t₄ (`osf/v62/inputs/probes_v0_42.jsonl`, byte copy of v0.42 commit `527899e`, SHA-256 `7aa246ee…6323aa`, checked by the build script). Translated: the 30 Phase B questions; the five Phase A templates (which, with the registry brand string inserted unchanged, give the 112 brand questions); the 15 v0.23 category labels. File: `osf/v62/translations/translations_v0_62_r2.json`; review table `translation_review_v0_62_r2.md`.

### §3.2 Steps

1. **Forward translation (model).** Claude (Anthropic; Claude Opus 5.5, runner session of 2026-11-10/11) — not a paid model call — into: **Spanish**, neutral Latin American usage, *usted*, no *voseo*, vocabulary common to Mexico and Argentina (*auto*, *auriculares*, *confiables*); **Korean**, standard South Korean, formal polite style (-습니다 / -십시오); **Chinese**, Simplified script, Mainland usage (e.g. 金酒 not 琴酒; 网红; 评测), polite 您 where a pronoun is needed.
2. **Back-translation.** Each item rendered back into English literally from the target text, in a separate pass by the same model in the same session: **not independent** (as r0). Each pair is coded *equivalent*, *minor drift* (wording differs, meaning and answer format the same) or *meaning change*. r2 record (30 Phase B items + 5 templates per language): **ES 22 equivalent, 13 minor drift; KO 23, 12; ZH 19, 16; meaning change 0 in every language.** Every drift is described in the item's note (e.g. "viral" → KO 입소문 'word of mouth', ZH 爆红; "storied" → legendaria / 이야깃거리가 풍부한 / 传奇色彩; the declared v0.21 scope rule).
3. **Native check (conditional, per language).**
   - **Spanish:** the pre-registrant reviews the 30 category questions, the five templates, the 15 labels and the notes (about an hour).
   - **Korean and Chinese:** student volunteers, if any accept the pre-registrant's invitation (optional, about an hour each; the runner contacts no one). The reviewer reads the items, the notes flagged "native check requested" and the alias table rows for the language.
   - Any change goes back through step 2. Reviewers are acknowledged only with their permission; no data about them is collected.
   - **Fallback, stated now:** if no native reader checks a language before the lock, that language's translations are checked by **back-translation only** — an independent back-translation made in a fresh session that is given only the target-language file — and the paper states, **for that language**, that its questions were model-translated and checked by back-translation only, without native review (§8, limitation 1). The fallback is decided per language; a checked language does not carry the limitation.
4. **Freeze.** Probe files rebuilt by `build_translated_probes_v0_62.py`, SHA-256 entered in the lock manifest; every sent prompt must equal its probe text byte for byte (gate P3).

### §3.3 Checklist (applied to every item)

1. **Category scope.** The category noun covers the same set of brands as the US English one. US "cosmetics" means colour cosmetics, while ES *cosméticos*, KO 화장품 and ZH 化妆品 include skincare and would merge v0.21 into v0.20: every v0.21 item uses ES *maquillaje*, KO 메이크업, ZH 彩妆 (the English cosmetics/makeup wording difference is not kept; declared). "Headphones": ES *auriculares*, KO 헤드폰, ZH 耳机 (the general word; 头戴式耳机 would narrow it to over-ear). "Audiophile": ES *audiófilos*, KO 오디오파일, ZH 发烧友. "Spirits": ES *destilados*, KO 증류주, ZH 烈酒; "premium": ES *premium*, KO 프리미엄, ZH 高端.
2. **Speech act and format.** "List several" and "Name several" kept distinct (ES *Enumere* / *Mencione*; KO 나열해 주십시오 / 이름을 들어 주십시오; ZH 列举 / 说出); "with descriptions" kept; "Answer yes or no" uses the language's own words (ES *sí* / *no*; KO 예 / 아니요; ZH "是" / "否").
3. **Nothing added or removed.** No country, market, currency, example or brand. KO EA-2 renders the em-dash apposition as a relative clause (대회인) without 등 ('etc.'), so the list stays closed.
4. **Names kept in Latin script.** Brands exactly as in the registry; publications and competitions as in English.
5. **No cultural substitution.** 6. **Superlatives and evaluative weight preserved.** 7. **Register** as §3.2 step 1; no system prompt.
8. **Typography.** Unicode NFC. ES: opening ¿ and ordinary spaces. KO: in Phase A the brand is followed by a space and 브랜드, so no particle attaches to a Latin-script name (Korean particles depend on the final sound). ZH: full-width punctuation; a half-width space between Latin-script runs and Han characters in Phase B (checked by the build script: 0 contacts); in Phase A the brand in Chinese double quotes “…”.
9. **Length** re-check for additions (as r1). 10. **Back-translation agreement** (§3.2 step 2).

### §3.4 Status in r2

All 30 + 5 + 15 items translated and back-translated in all three languages; 0 meaning changes. Build check PASS (`osf/v62/translations/build_check_v0_62_r2.txt`): 142 probes per language (30 + 112), 112 of 112 Phase A prompts carry the registry brand string verbatim, 0 unfilled placeholders, 0 no-break spaces. Probe files r2 SHA-256: ES `8484ae76…3dcf`, KO `ba24ca01…7bb8`, ZH `e897dc87…8753`. Native checks: not yet done (§3.2 step 3).

---

## §4 Brand names per language

### §4.1 In the questions

Brand names appear in Phase A only and are written in **Latin script** in all three languages, exactly as the registry has them (stimulus identical across languages; models' Korean and Chinese answers commonly carry Latin-script names). A Hangul or Han form in the question is not adopted (it would add one translation choice per brand).

### §4.2 In the answers (coding aliases)

`osf/v62/translations/brand_aliases_v0_62_r2.csv` (112 rows; built by `make_alias_table_r2_v0_62.py`):
- **Korean:** 120 Hangul aliases over 111 units (ZMF Headphones has none; r3: 119 → 120, MAC Cosmetics' 맥 코스메틱스 added), e.g. 젠하이저, 오디오테크니카 / 오디오 테크니카, 토요타 / 도요타, 현대자동차 / 현대차, 맥 코스메틱스 / 맥 코스메틱.
- **Chinese:** 80 Han aliases over 74 units (38 units have no established Chinese name the runner could state and are matched in Latin script only), e.g. 森海塞尔, 铁三角, 雅诗兰黛, 宝马, 尊尼获加.
- **Spanish:** no alias. Spanish keeps the registry names; the brands where Spanish usage differs in spelling were checked: *Bacardí*, *Patrón* / Patron, *L'Oréal París* (accents, removed by the certified matchers' accent stripping), *Rémy Martin*; *Fernet Branca* without hyphen (Argentine usage) is a parity check against the v0.23 matcher before the lock, no alias added.
- **Parity rule (as r1).** An alias may not be looser than the certified English matcher, which counts only the full registry string: bare 벤츠 / 奔驰 (Mercedes-Benz), 디올 / 迪奥 (Dior Beauty), 샤넬 / 香奈儿 (Chanel Beauty), 아르마니 / 阿玛尼, 톰 포드 / 汤姆福特, 로레알 / 欧莱雅 and 맥 (MAC Cosmetics) are not aliases. ZH 肌肤之钥 is the full Chinese name of Clé de Peau Beauté and is kept; ZH 魅可 (MAC) is kept pending the v0.21 matcher parity check.
- **Common words excluded:** bare 현대 / 现代 ('modern') for Hyundai; bare 大众 ('the public', 'mass market') for Volkswagen (大众汽车, 上汽大众, 一汽-大众 kept).
- **Check record (2026-11-11 UTC; source and date per row).** Each alias is CONFIRMED only if the runner opened the brand's own Korean/Chinese site or a dated authoritative page showing it; PARTLY if seen only on a secondary dated source or only one of several forms was seen; otherwise UNCONFIRMED (in force as a spelling transcription, flagged for the native check). **Korean: 23 confirmed (brand Korea site, or the Korean site of the brand's local subsidiary or owner; 19 on the brand's own Korean site, e.g. Porsche, Hyundai, Mercedes-Benz, Sony, Sennheiser), 4 partly (Toyota 토요타 seen on the brand's Korean site, 도요타 not seen; MAC: the site writes 맥 코스메틱스, added in r3, while the r2 transcription 맥 코스메틱 is not seen there and is kept; Audio-Technica 오디오테크니카, seen only on the Korean official importer's site; Denon, secondary source), 84 unconfirmed, 1 without alias. Chinese: 30 confirmed (brand China site or the Chinese site of the brand's owner or local subsidiary), 3 partly (Volkswagen, where 大众汽车 and 上汽大众 were seen but not 一汽-大众 / 一汽大众; HiFiMan and Beyerdynamic 拜雅, secondary sources), 41 unconfirmed, 38 without alias; for those 38 no Chinese name was found on a brand site, so no new Chinese alias is proposed.** Many brand sites refuse automated access (robots) or could not be read; those rows stay unconfirmed. Where a brand's own site writes a different form from the alias (BMW 비엠더블유 and Tesla 테슬라, which the Korean sites write in Latin script; Focal 劲浪 / 포칼, which both brand sites write as Latin 'Focal'; Dior Beauty and Chanel Beauty in Korean; Mercedes-Benz and Johnnie Walker without the optional space, which KO-1 covers), nothing was changed. **r3 applied the one proposed change:** Korean 맥 코스메틱스 added for MAC Cosmetics (the form on the brand's Korean site, https://www.maccosmetics.co.kr/, meta description "맥 코스메틱스의 아이코닉 메이크업 컬렉션", re-opened 2026-11-11 about 14:53 UTC); the r2 form 맥 코스메틱 alone would not match it under KO-2, so both forms are aliases and the row stays PARTLY (one of two forms seen); counts unchanged (KO 23 / 4 / 84 / 1). Built through the CHECKS record of `make_alias_table_r2_v0_62.py` (the table keeps its r2 file name; change log in the script) and unit-tested (`test_mac_korean_alias_r3`). Mercedes-Benz Chinese was moved from a Xinhua source to the brand China site. One check changed nothing but is recorded: Denon's Chinese site writes "Denon" in Latin script (its company name uses 电音, which is not adopted as an alias: it also means 'electronic music'); 天龙 stays unconfirmed.

### §4.3 Matching (implemented; fixed now)

The certified English matchers (v0.42 §5.1) stay unchanged. A language pre-step prepares answers before they reach them (`code_v0_62.py`):
1. **Normalisation.** NFC; full-width Latin letters, digits and signs, half-width katakana and half-width Hangul → ordinary forms (NFKC, run by run: ＢＭＷ → BMW, ＳＯＮＹ → SONY); ideographic and no-break spaces → space; typographic apostrophes → ' (applied to both sides of gate P2); URLs removed (byte copy of v0.42's `strip_urls`).
2. **Alias canonicalisation** (longest alias first): each occurrence is replaced by " <registry name> ". Rules:
   - **KO-1 / ZH-1 (spacing and joints).** Spaces, hyphens (- －) and middle dots (· ・ ･) at an alias's word joints are optional: 오디오테크니카 = 오디오 테크니카; 梅赛德斯-奔驰 = 梅赛德斯·奔驰 = 梅赛德斯奔驰.
   - **KO-2 (Hangul boundaries).** A Hangul alias matches only when not preceded by a Hangul syllable and when followed by a non-Hangul character, the end, or a run of particles / copula forms from a fixed list (은 는 이 가 을 를 의 에 에서 와 과 도 만 로 으로 처럼 보다 부터 까지 이나 나 랑 이랑 하고 께서 이다 입니다 이며 이고 예요 이에요 라는 이라는) that ends before a non-Hangul character. So 소니의, 현대자동차에서는 and 코스의 match; 코스 does not match inside 코스메틱 or 코스트코.
   - **ZH-2 (Han).** Han aliases match as written (Chinese does not separate words).
   - **Script variants.** Chinese aliases are Simplified only; Traditional forms are not mapped and no conversion is applied; answers with Traditional-only characters are counted (MC_Script) and excluded in S-Script.
   - **Collision-prone aliases** (counted, every match exported for audit, switched off in S-Alias): KO 코스 (Koss), 로드 (Rhode), 나스 (NARS), 재규어 (Jaguar), 머큐리 (Mercury), 새턴 (Saturn); ZH 歌德 (Grado; also Goethe), 高斯 (Koss; also Gauss), 日产 (Nissan), 普利茅斯 (Plymouth; also the city), 水星 (Mercury), 土星 (Saturn), 知更鸟 (Redbreast; also the bird).
3. **Script-boundary spacing:** a space at every transition between a Latin letter or digit and a kana, Han or Hangul character (Python's `\b` treats these as word characters).
4. The certified matcher runs on the result. The same pre-step feeds v1.14's rank extractor (§2.4). Gate P2 shows the pre-step changes nothing on English text; gate P4 shows every alias reaches its unit (§7.3).

### §4.4 Recognition answers (Phase A; block 4, v0.19–v0.22, collected under §9 item 7 (b))

v0.19–v0.22: a leading ES *sí* / *no* (unaccented *si* only before punctuation or the end, so *Si bien…* is not read as yes), KO 예 / 네 / 아니요 / 아니오 / 아니 (not followed by a Hangul syllable, so 네이버 is not read as yes), ZH 是的 / 是 / 否 / 不是 / 不 (是 and 不 only before punctuation, space or the end, so 是一个… and 不太… are not mapped) is replaced by Yes / No (in Chinese, which is written without spaces, the mapped word is set off by a space wherever it touches another character, so that the certified parser can read it: "否。" → "No 。"; pre-lock correction of 2026-11-12, §11) and the certified parser `parse_yes_no` reads the answer; unparsed answers are non-answers (v0.42 C6). v0.23 open answers (block 5, **not collected** under §9 item 7 (b), so no judge call is made; kept for the record): the t₁–t₄ recognition judge with its English instruction unchanged; Claude Sonnet 4.5 retires on 2026-11-30, so the judge calls (after the 2026-11-29..12-02 collection) use the successor judge that t₅ adopts, with t₅'s parity check, logged in DEVIATIONS.

---

## §5 Probes and collection

### §5.1 Probe files

`osf/v62/translations/probes_{es,ko,zh}_v0_62_r2.jsonl`: 142 lines each, t₄ probe IDs and order, each line carrying the English source beside the translated prompt.

### §5.2 Design and order

| Block (collection order) | Phase | Languages | Run | Calls per model | Calls (N3) | Status |
|---|---|---|---|---|---|---|
| 1 | B (30 category questions) | ES, KO, ZH | 1 | 90 | 270 | core |
| 2 | B | ES, KO, ZH | 2 | 90 | 270 | core |
| 3 | B | ES, KO, ZH | 3 | 90 | 270 | core |
| 4 | A, v0.19–v0.22 yes/no (88 per language) | ES, KO, ZH | 1 | 264 | 792 | **collected, last (§9 item 7 (b), 2026-11-12)** |
| 5 | A, v0.23 open (24 per language) | ES, KO, ZH | 1 | 72 | 216 | not collected |
| **Core / adopted (blocks 1–4) / with all extras** | | | | **270 / 534 / 606** | **810 / 1,602 / 1,818** | |

Within a block: one worker per model, the three in parallel, ES then KO then ZH, probes in file order. Every confirmatory test (Presence, Consistency, Ranking) uses blocks 1–3 only; blocks 4–5 feed descriptives (§2.9 item 2) only. **Extras rule (fixed now):** blocks 4–5 are collected only if `params_v0_62.BRAND_EXTRAS` is True at the lock, which the final pre-registration sets only if the high estimate of blocks 1–5 (re-based on t₄'s recorded English usage, §6.2) is at or below $100. At r3 (re-based) the conservative high of blocks 1–5 is $185.38, so by this rule it stays False; §9 item 7 sets out what a change of the rule would cost (the pre-registrant's decision). **r3 update (decided 2026-11-12, §9 item 7 (b)): block 4 is collected whenever `params_v0_62.BRAND_YES_NO` is True (set True by the decision), block 5 only if `BRAND_EXTRAS` is True (False). Block 4 starts only after blocks 1–3 have been sent, under the same $80 pause, $100 stop and projection pause; any pause or stop in blocks 1–3 halts the collection before block 4.** Phase B three runs per language: as t₄ (a one-run π̂ against a three-run English π̂ would attenuate ρ for a reason that is not language; φ needs two defined runs). Search on (S1) not collected (r1 §5.2).

### §5.3 Panel and §5.4 Call settings

As r1: N3 as verified for v0.42 r2 (Claude Fable 5.2 `claude-fable-5-2` through Anthropic's Message Batches API; GPT-6 Astra `gpt-6-astra` and Gemini 4 Argon `gemini-4-argon` synchronous), re-verified at the final pre-registration; t₄'s S0 settings exactly (no tools; no system prompt; sampling at provider defaults; maximum output 16,384 tokens; v0.42's retry policy and re-run pass); no language, locale or region parameter. Raw artefact `osf/v62/data/v62_raw.jsonl` with v0.42's fields plus `language`.

### §5.5 Window and guards

As r1: window 2026-11-29..12-02 US Central, 72 hours from the first call; refusal during 2026-11-17..21; one collection at a time; `--collect` refuses unless the tag is on `origin` and the OSF anchor names its commit; a slip needs a DEVIATIONS entry first.

---

## §6 Budget

### §6.1 Cap and prices

At most $100 of paid model calls for this paper, including re-sends and (if block 5 is collected) the v0.23 judge; pause at $80; both from actual recorded usage. **Prices re-read on 2026-11-11 at about 14:35 UTC (r3), unchanged from the programme list of 2026-11-10** (US$ per 1M tokens in / out): Claude Fable 5.2 Message Batches 4 / 20 (standard 8 / 40; "a 50 percent discount on both input and output tokens"; https://platform.claude.com/docs/about-claude/pricing); GPT-6 Astra standard 10 / 50 (batch 5 / 25, not used, as t₄; https://developers.openai.com/api/docs/pricing; reasoning tokens "billed as output tokens", https://developers.openai.com/api/docs/guides/reasoning); Gemini 4 Argon standard 2 / 10 through 2026-11-30 and 4 / 20 from 2026-12-01 ("$4.00 starting December 1, 2026"; output "including thinking tokens"; https://ai.google.dev/gemini-api/docs/latest-model, "Last updated 2026-10-27 UTC"; the general pricing page does not list the model). The guard prices each request at the UTC date it starts. Judge (block 5 only): t₅'s successor-judge candidates are Claude Sonnet 5.5 at 2 / 10 and Claude Sonnet 4.6 at 3 / 15 (same Anthropic page); the reserve uses 3 / 15. Re-read again at the final pre-registration.

### §6.2 Basis: t₄'s recorded usage (r3) and language factors

- **English basis (r3).** t₄'s recorded usage (v0.42, tag `v0.42-acquisition-locked` → `a790bb1`; `t4_raw.jsonl` SHA-256 `f3109091…96d4bf` and `t4_batches.jsonl` `d73b8e81…39298c`, read from the tag with `git show`; usage fields only, no answer text read). Reconciliation: recorded cost $67.4551 + the $0.50 judge reserve = $67.9551, the recorded spend; the S0 lines recomputed by `budget_v0_62` at t₄'s dates equal their recorded cost ($14.5460; largest line difference 0). The 606 answered S0 lines (202 per model: 90 category questions, 88 yes/no and 24 open brand questions) were one billed request each: no re-send, no transient failure (6 Gemini requests were refused with HTTP 402, not billed, and re-run); all 292 Claude Fable 5.2 answers came from the 7 recorded batches. Per model × question type: **central per call = mean recorded tokens × 1.02 (re-sends); conservative high per call = 90th percentile of each token field × 1.10** — v0.42 r2's rules, now on measured tokens of the same three models; r2's proxies (Fable as Claude Opus 5.5 × 2 / × 3; Gemini output × 1.5 for unrecorded thinking) are dropped, since t₄ recorded Fable itself and Gemini reported no thinking tokens at S0.

| Per English call (US$; central / conservative high) | Category question | Yes/no brand question | Open brand question |
|---|---|---|---|
| Claude Fable 5.2 (batch) | 0.0263 / 0.0772 | 0.0019 / 0.0037 | 0.0837 / 0.1029 |
| GPT-6 Astra | 0.0430 / 0.0995 | 0.0007 / 0.0014 | 0.1953 / 0.2381 |
| Gemini 4 Argon, November prices | 0.0133 / 0.0200 | 0.0002 / 0.0002 | 0.0195 / 0.0233 |
| Gemini 4 Argon, December prices | 0.0267 / 0.0399 | 0.0003 / 0.0004 | 0.0389 / 0.0466 |

(Output tokens per category question, mean / p90: Fable 1,279 / 3,489; GPT-6 Astra 838 / 1,798, reasoning included; Gemini 1,296 / 1,799. Open brand questions: 4,088 / 4,660; 3,820 / 4,318; 1,892 / 2,104. Full table: `cost_estimate_v0_62_r3.txt`.)
- **Language factors (declared assumptions, not measured; unchanged from r2), on the whole per-call cost: central ES 1.25, KO 1.75, ZH 1.50; conservative high ES 1.50, KO 2.50, ZH 2.25.** Korean and Chinese are set conservatively: Hangul and Han text usually costs more tokens per unit of meaning than English in byte-pair tokenizers, by vendor-specific amounts not published for these models; no Korean or Chinese answer from them is on record and no tokenizer is installed on the collection machine. During collection the projection pause uses actual usage, and the measured factor is reported (§2.9 item 3).
- **Judge reserve** (only with block 5): 216 × (1,500 × 2.50 input + 10 output tokens) at 3 / 15 = **$2.46** (v0.23's judge reads at most 3,000 characters of each answer).

### §6.3 Estimate per block (r3, US$)

| Block | Calls | Central, Nov prices | Central, Dec prices | Conservative high, Nov | Conservative high, Dec |
|---|---|---|---|---|---|
| 1. category questions, run 1 | 270 | 11.15 | 12.95 | 36.86 | 40.60 |
| 2. category questions, run 2 | 270 | 11.15 | 12.95 | 36.86 | 40.60 |
| 3. category questions, run 3 | 270 | 11.15 | 12.95 | 36.86 | 40.60 |
| **Core: blocks 1–3 (adopted)** | **810** | **33.44** | **38.84** | **110.58** | **121.80** |
| 4. yes/no brand questions (v0.19–v0.22) | 792 | 1.09 | 1.15 | 2.87 | 2.97 |
| 5. open brand questions (v0.23) + judge reserve | 216 | 34.70 | 36.81 | 57.10 | 60.60 |
| Full design: blocks 1–5 + judge reserve | 1,818 | 69.23 | 76.79 | 170.56 | 185.38 |
| **Adopted (r3 update, §9 item 7 (b)): blocks 1–4, block 4 last** | **1,602** | **34.52** | **39.98** | **113.45** | **124.77** |

(Cells rounded; totals from unrounded values. Headline: **central $33.44** — the window opens 2026-11-29 00:00 CT and December begins for the guard at 2026-11-30 18:00 CT, while t₄'s 876 calls took under 7 hours, so a core started on 2026-11-29 runs at November prices — and **conservative high $121.80**, December prices on every call.)

**Reading.** (a) The core fits easily at the central estimate, well below the $80 pause. (b) At the conservative high it does not fit ($121.80 > $100): every call at t₄'s 90th-percentile tokens and at the high Korean and Chinese factors. With the high factors on t₄'s mean tokens the core would cost $58.17 (December), so the token tail, not only the language factors, drives the conservative high. (c) The brand questions do not fit under the $80 pause at the conservative high (§9 item 7).

**What happens in the conservative-high case (core).** Block 1 costs about $40.60; the projection pause after block 1 (block-1 call spend × 3.0 > $80, i.e. block 1 above $26.67) stops collection for the pre-registrant's decision (§6.5, r3 fix): continue under the $80 pause and $100 stop (the $80 pause then falls at about 1.97 runs and the $100 stop at about 2.46 runs, before in-flight reservations), fallback F2 (drop run 3: φ then needs both remaining runs defined; declared asymmetry with the three-run English value), drop a language, or raise the budget for this paper. **The smallest budget that covers the conservative high of the core is $121.80** (r2: $142.06). At the central estimate no pause is reached (block 1 $11.15, projection $33.44; at December prices $12.95 and $38.84).

**Adopted design (r3 update, 2026-11-12; `cost_estimate_v0_62_r3.json` → `guard_core_plus_yn`).** Spend at the end of blocks 1–4: central (November) $11.15 / $22.29 / $33.44 / $34.52; central (December) $12.95 / $25.89 / $38.84 / $39.98; conservative high (December) $40.60 / $81.20 / $121.80 / $124.77. *Central:* the projection after block 1 is $11.15 × 3.0975 = $34.52 (December $12.95 × 3.0887 = $39.98), so no projection pause, and neither the $80 pause nor the $100 stop can bind (the whole design stays below $40). The $100 rule's worst-case reservations ($0.3357 per Claude Fable 5.2 batch request) let at most 198 of Fable's 264 block-4 requests into its first batch at the end of block 3 (192 while both synchronous workers hold their reservations; December 182 / 175); the rest go in later batches and no request is refused. *Conservative high:* the projection pause falls after block 1 ($40.60 × 3.0887 = $125.40 > $80); if the pre-registrant continues, the $80 pause falls in run 2 and the $100 stop in run 3, so block 4 is not reached unless the budget is raised to $124.77. Block 4 can therefore never take budget from the first pass of the category runs. One ordering detail: category calls that still fail after the main pass are re-sent in the re-run pass (a later `--collect`), which comes after block 4; block 4's own spend (central $1.09 November, $1.15 December) is then already counted.

### §6.4 Design trade-off (r3, US$)

| Design | Calls | Central (Nov) | Central (Dec) | Conservative high (Dec) |
|---|---|---|---|---|
| Core, Phase B S0 × 3, ES + KO + ZH (r3's adopted design until 2026-11-12) | 810 | 33.44 | 38.84 | 121.80 |
| **Adopted (2026-11-12, §9 item 7 (b)): core + yes/no brand questions (block 4, last)** | **1,602** | **34.52** | **39.98** | **124.77** |
| Core + open brand questions + judge reserve (block 5) | 1,026 | 68.14 | 75.64 | 182.41 |
| Core + both (full t₄ S0 panel) | 1,818 | 69.23 | 76.79 | 185.38 |

r2's other designs (fallback F2 with extras, one language, search on) are not recomputed in r3; none is a candidate. What the adopted design gives up: recognition of the 24 v0.23 (spirits) units (block 5, with its judge); search-on answers; within-provider replication.

### §6.5 Guard (from actual usage; conservative counting, r2; projection pause restored, r3)

v0.42's ledger arithmetic, with these rules (`budget_v0_62.py`, `acquire_v0_62.py`; each unit-tested):
1. **Spend** = judge reserve (only if block 5 is collected; else $0) + the cost of every raw line from its recorded usage, each request at the price of the UTC date it started.
2. **Failed attempts count at worst case.** Every attempt of a synchronous call that returned no usage (timeouts and other transient failures; the copied call function does not distinguish them) is costed at the request's worst case (16,384 output tokens, 2,000 input tokens): $0.84 for GPT-6 Astra and $0.34 for Gemini 4 Argon at December prices (t₄ had no such failure at S0). A final non-transient 4xx error is not billed (t₄'s six HTTP 402 refusals were of this kind). Errored or expired batch requests are costed at the batch worst case. Rule 2 over-counts rate-limit (429) failures, which vendors do not bill; this is accepted as conservative.
3. **Searches** (S1 only; S0 sends no tool): every OpenAI page-open or find-in-page action counts as a billed search; a Gemini part with searches but no reported tool-token count is charged 150,000 extra input tokens.
4. **Reservations.** Before each request its worst case is reserved; **two worst cases per synchronous call** (it may be re-sent: retry or empty re-send): GPT-6 Astra $1.6784, Gemini 4 Argon $0.6714 (December); Claude Fable 5.2 batch $0.3357 per request.
5. **Hard stop:** no request if spend + reservations + its reservation would exceed $100. **Pause at $80:** no new request until the pre-registrant's `--approve-past-80`. **Projection pause:** after block 1, projected total = block-1 call spend × 3.0 (core) or × the central ratio of the design with extras (`cost_estimate_v0_62_r3.json`: full design 6.2110 Nov / 5.9318 Dec; core + block 4: 3.0975 / 3.0887); above $80 → pause; options as §6.3. **r3 update: the adopted design uses the core + block 4 ratio (`projection_core_plus_yn`, read by `acquire_v0_62.projection_ratio`): a pause whenever block 1 costs more than $25.83 (November) or $25.90 (December).** **r3 fix:** r2's `collect()` recorded a `drop_phase_a` approval whenever the extras were off, and any recorded fallback approval switches the projection pause off, so in the adopted design the first halt would have been the $80 pause (the r2 fake-SDK dry run halted at the $80 pause inside block 3 with `approved_drop_phase_a: True`). r3 leaves blocks 4–5 out without recording an approval (`acquire_v0_62.collection_specs`), so the projection pause after block 1 works as written; regression tests: with a block-1 spend of $29.70 the core collection pauses after 270 calls (r2's behaviour: first halt at the $80 pause after 730 calls).

The fake-SDK dry run (§7.6) of r2 (`dry_run_fake_sdk_v0_62_r2.txt`) predates the r3 fix: with about 30% adversarial attempts the guard's spend ran $51 above an independent bill of the requests that returned usage (the effect of rule 2). **r3 update (2026-11-12): re-run with the fix and the adopted 1,602-call design (`osf/v62/prereg/dry_run_fake_sdk_v0_62_r3.txt`; script `_dry_run_fake_sdk_v0_62.py`; the fakes are now in the repository as `_fakesdk_v0_62.py`, byte-identical to r2's). Adversarial scenario, in `--collect` stages: (1) the projection pause after block 1 (call spend $35.80 × 3.0975 = $110.90 > $80; r2 had no such pause); (2) after `--approve-projection`, the $80 pause inside block 3 ($80.86); (3) after `--approve-past-80`, the $100 stop inside block 3 ($98.93); (4) a further `--collect` (re-run pass) sent nothing (the $100 rule); no yes/no question was sent at any stage; the guard's spend was $65.96 above the independent bill ($32.97; 147 worst-case parts). Mild scenario: all 1,602 calls answered, block 4 strictly after blocks 1–3, Claude Fable 5.2's block-4 requests in three batches (236, 49 and 3, the last two from the reservation limit and from re-sends), spend $36.01 (independent bill $22.41); after the pre-lock correction of the Chinese answer words, 11 of 11 plain "否。" answers are read as No (before it, 10 were non-answers). Stop mid-batch (pre-lock correction, record of batches in flight): the run stopped while Claude Fable 5.2's 90-request block-2 batch was in flight; the next `--collect` first recorded that batch from the journal (90 lines, its spend counted), sent no request twice, wrote no call twice, and finished all 1,602 calls at the same spend as the uninterrupted run ($36.01). Exact figures vary slightly between runs near the pause and stop (three parallel workers).**

---

## §7 Analysis plan

### §7.1 Coding

Phase B mentions: the pre-step of §4.3, then each category's certified matcher as v0.42's coder calls it (`code_t4_v0_42.py`, run unchanged as a separate process on prepared copies, one language at a time). Phase A: §4.4. Coder `osf/v62/scripts/code_v0_62.py`.

### §7.2 Computation

`osf/v62/scripts/score_v0_62.py`, tested on synthetic data and run once after the gates. Its π̂ and φ kernels are transcriptions of v0.42's (the v0.62 branch does not contain osf/v41–v42); gate P1 checks them against v0.42's locked kernels.

### §7.3 Gates (before any statistic)

- **P1 (kernel parity).** r2: run against v0.42's **locked** kernels, pinned to tag `v0.42-prereg-r1` (`58d1891`): `score_v0_42.pi_hat`, `phi_runs`, `phi_panel` and `score_v41.phi_m` read from the tag with `git show` and executed unchanged (`gate_p1_v0_62.py`). On three synthetic English-shaped tables (112 units; complete; with missing model-runs; seeds 620151–620153) the transcriptions reproduce π̂ and (φ, partition) exactly for all 112 units: **PASS, 0 mismatches** (`osf/v62/prereg/gate_P1_v0_62_r2.json`); unit tests show the gate fails on a perturbed kernel. v0.42's real answers were not read; the same comparison on t₄'s coded tables is run at the lock. **r3:** re-run against the same tag: PASS, 0 mismatches on the three tables, identical to r2's record (`osf/v62/prereg/gate_P1_v0_62_r3.json`); the r1 item "v0.42's kernels must pass P1 before the lock" is closed for the locked kernels. t₄'s coded tables now exist on branch `v0.42` (commit `c84f6fa`); the real-data half is proposed to run after v0.42's own single scoring run, so that v0.62 computes no t₄ statistic before v0.42 does.
- **P2 (pre-step inert on English; r1 open item closed in code, r3).** `gate_p2_v0_62.py`: side PRE = the full pre-step; side REF = the pre-step's step-1 normalisation only (apostrophe mapping included); both on t₄'s English answers and both coded by v0.42's coder unchanged; **PASS iff every coded cell (Phase B mentions; Phase A labels and codes) is equal and no row is missing.** Why both sides: the certified v0.20–v0.22 matchers do not map ’ to ' (they lower-case and strip accents only), so a "Paula’s Choice" or "L’Oréal Paris" written with a typographic apostrophe was not counted at t₄, and a comparison with v0.42's locked codes would fail on such cells for a reason that is not the pre-step (r1's fix, commit `4f3a226`, was a test with a fake matcher only). The mapping's own effect is reported beside P2 as the **apostrophe delta** (cells where REF differs from v0.42's locked codes); it can concern only Paula's Choice (v0.20) and L'Oréal Paris (v0.21), because v0.19 has no registry name with an apostrophe and v0.23's patterns make it optional. The English comparator of every test stays v0.42's locked values (§2.1); a non-zero delta is reported with its units and direction (those units' English π̂ would be slightly higher under the mapping), not corrected (§9 item 6). Unit tests (r3): with the real certified matchers (the same git blobs as at tag `v0.42-prereg-r1`) on synthetic English answers, PRE = REF on every answer, the apostrophe delta is exactly {Paula's Choice, L'Oréal Paris}, and the gate fails on a perturbed pre-step; cell comparison and file preparation are tested. Run at the lock on t₄'s English answers.
- **P3 (probe parity).** Probe files' SHA-256 equal the lock manifest; every sent prompt equals its probe text.
- **P4 (alias reach).** Every KO and ZH alias, inside particles, lists, Markdown bold and after a number, is coded as a mention of its unit and no other; fixed decoys yield no mention: 현대적인, 코스메틱, 로드바이크, 파이널, 엘프, 现代, 大众, 迪奥, 香奈儿, 欧莱雅, 阿玛尼, 奔驰, 벤츠, 디올, 맥. r2: PASS in the unit tests on the full r2 table (119 KO × 5 frames, 80 ZH × 4 frames); r3: PASS on the table with MAC's added form (120 KO × 5 frames, 80 ZH × 4 frames).

### §7.4 Drop rule and missing data

As r1, per language: a model × language × phase with < 90% of its calls answered is excluded for that language and phase; `H_Lang_*` in L need all three models in Phase B in L, otherwise UNDETERMINED for L. Calls not sent because of a budget stop count as unanswered. No imputation.

### §7.5 Sensitivities (reported; no verdict changes)

S-Denon (111 units); S-Headphones (96 units); **S-COI (r3, proposed; 106 units: the six units with a Samsung-group tie in DEVIATIONS Entry 0, Part F — Denon, Eucerin, BMW, Bentley, Chevrolet, Jack Daniel's — removed together; `params_v0_62.COI_FLAGGED`; computed under every headphones option)**; S-Language (off-language answers excluded); S-Script (ZH answers with Traditional-only characters excluded); S-Alias (collision-prone aliases off); S-Uncentred. If a primary verdict differs under S-Denon, S-Headphones or S-COI, the paper reports both in its abstract (default (3) of 2026-11-10: every result is also shown without Denon and without the headphones category; r3 extends the rule to S-COI, the check without every unit with a tie).

### §7.6 Reporting and dry run

Every test reported, including failures and undetermined results; raw answers, coded tables and verdicts deposited. Public-study rules apply: no focal brand, no lesson addressed to a brand, no brand contacted. Before the lock a fake-SDK dry run exercises the acquisition (r2: `osf/v62/prereg/dry_run_fake_sdk_v0_62_r2.txt`; 810 core specs; r3 update: `dry_run_fake_sdk_v0_62_r3.txt`, the adopted 1,602 specs, §6.5; adversarial cases per model: transient failures, timeouts, fatal 4xx, empty answers re-sent once, refusals, truncation at the cap, served-model mismatch, English-language and Traditional-script answers, expired and errored batch requests).

---

## §8 Limitations

1. **Translations are model-made.** The back-translations are by the same model and not independent. Native review is planned (Spanish: the pre-registrant; Korean and Chinese: student volunteers, if any). **For any language without a native check before the lock, the paper states that its questions were checked by back-translation only** (independent, fresh session), and that naturalness is unverified for that language.
2. The forward translator (Claude) belongs to the same provider as one of the three measured models.
3. Language is varied without a market: the registries are US-market selections; Spanish-, Korean- and Chinese-speaking users would also ask about brands absent here. The study tests whether the same brands are ordered alike. The Chinese results describe what these three models answer when asked in Simplified Chinese, not what users in any particular country receive from locally available assistants.
4. One variety per language: neutral Latin American Spanish (not Peninsular), standard South Korean, Simplified Mainland Chinese (not Traditional).
5. Time and language are confounded (t₄ mid-November; v0.62 late November / early December); §2.7's t₅ benchmark helps only if t₅ is scored in time.
6. Search off only.
7. Korean and Chinese coding rests on a new alias table, mostly unconfirmed at r2 and r3 (§4.2), and some aliases are also common words (MC_Alias, S-Alias). Brands without a Chinese alias are matched in Latin script only, which under-counts any Han-script mention the runner could not anticipate.
8. One model per provider and three runs, as t₄.
9. The English token basis is t₄'s recorded usage (r3), but the Korean and Chinese factors stay unmeasured until collection; at the conservative high the core exceeds the $100 cap (§6.3), so a budget stop could cut confirmatory runs unless the projection pause after block 1 and the pre-registrant's choice prevent it.
10. Recognition is collected for the 88 yes/no brand questions only (block 4, last; §9 item 7 (b)): none for the 24 spirits units, and in the conservative-high case the $100 stop falls before block 4, so recognition may be missing altogether (§6.3). Yes/no answers are read by a fixed plain-text rule (§4.4): an answer that puts a sentence before its answer word is a non-answer, or, in Spanish, can be read as No when that sentence contains the negation *no* (noted 2026-11-12, no change; §11).
11. **No buyer persona.** Every question is asked without a persona or any description of the asker (no system prompt; §5.4), as at t₄, so the scores describe answers to persona-free questions. Outside audits find that a stated buyer persona changes which brands are recommended: category leaders stayed about 80% the same across personas, while mid-market brands swapped up to 75% of the recommended set (Jack, Lehman, Maloney and Xu, arXiv 2605.30207, May 2026; 2,000 runs on one day; authors at Unusual); and U.S.-developed Gemini and GPT models favoured American entities, a pattern that persisted across personas (Rienecker et al., "Auditing Preferences for Brands and Cultures in LLMs" (ChoiceEval), arXiv 2603.18300, March 2026). Whether the language results hold for questions asked with a persona is not tested here; ChoiceEval is cited as context for any skew toward US brands in the descriptives (§2.5, §2.9 item 5); no test is added.

---

## §9 Decisions for the pre-registrant (before the lock)

1. **Chinese variety.** Default: Simplified, Mainland usage (as the decision names). Alternative: Traditional (Taiwan), which would need a new translation and alias pass.
2. **Spanish variety.** Runner's choice: neutral Latin American (*usted*, *auto*, *auriculares*). Alternative: Mexican or Rioplatense usage (e.g. *audífonos*), or Peninsular.
3. **Budget in the conservative-high scenario** (§6.3; r3, re-based on t₄'s recorded usage). **DECIDED 2026-11-12, 00:48 CT (pre-registrant: "as you suggest"): the default, keep the $100 cap; the projection pause after block 1 stops collection for his choice whenever block 1 costs more than the threshold (r3 update: $25.83 November / $25.90 December with block 4 in the design).** The core's central estimate is $33.44 ($38.84 at December prices); its conservative high is $121.80, above the $100 cap. Options: keep the core at $100 (recommended: the projection pause after block 1 stops collection whenever block 1 costs more than $26.67, before the second run, and you choose then); or authorise up to $121.80 for the core now (r2 asked for up to $142.06); or decide now to drop run 3 (F2) or a language if the projection pause triggers.
4. **Native checks.** Spanish: the pre-registrant. Korean and Chinese: whether any student volunteer accepts Friday's invitation; the fallback of §3.2 step 3 applies per language otherwise.
5. **Study-list labels** for the non-English wave (r0's #52/#53 were French and Japanese).
6. Settled by the runner (can be overruled): Latin script for brand names in the questions (§4.1); KO/ZH matching rules (§4.3); v0.21 scope rule in all three languages (§3.3). r3: MAC Cosmetics' Korean alias 맥 코스메틱스 added and 맥 코스메틱 kept (§4.2); P2 reports the apostrophe delta and does not correct the English comparator (§7.3; alternative: re-code the English comparator with the same normalisation); the projection-pause fix (§6.5); P1's real-data half after v0.42's own scoring run (§7.3).
7. **Brand questions (Phase A). DECIDED 2026-11-12, 00:48 CT (pre-registrant: "as you suggest"): option (b), the 88 yes/no brand questions only (block 4), run last, with the code change made and checked before the lock (`params_v0_62.BRAND_YES_NO = True`; `acquire_v0_62` `yes_no_on`, `open_on`, `design_key`, `projection_ratio`; 8 unit tests; dry run re-run; §11 r3 update).** r3's text of the option follows: **an option, not added (r3).** **In the conservative-high case none of the 112 brand questions fits under the $80 pause: the core alone is $121.80 there.** Smallest budgets that would include them at the conservative high: **core + the 88 yes/no brand questions (v0.19–v0.22; block 4; 792 calls): $124.77**; **core + all 112 (blocks 4–5; 1,008 calls; with the $2.46 judge reserve): $185.38**. Block 4 alone costs $2.97 at the conservative high and $1.09 central ($1.15 at December prices); block 5 with the reserve $60.60 and $34.70 ($36.81). At the central estimate both fit under $80 (core + block 4: $34.52 / $39.98; core + blocks 4–5: $69.23 / $76.79). They serve **no confirmatory test** (H_Lang_Presence, H_Lang_Phi and H_Lang_Rank use the category questions only); they serve the pre-registered **descriptive §2.9 item 2** (recognition per model × language beside English t₄: block 4 gives it for 88 of the 112 units; block 5, the 24 spirits units, also needs t₅'s successor judge and its parity check) and the Phase A rows of descriptive 3 (answer form per language). Choices: **(a) keep them off** (the §5.2 rule's result, default); **(b) add block 4 only**, as the last block: it starts only after the three category runs, under the same $80 pause and $100 stop, so it cannot take budget from the confirmatory tests; at the central estimate it adds about $1.10; in the conservative-high case the guard stops before reaching it unless the budget is raised to $124.77; this changes the §5.2 rule and needs a parameter that turns on block 4 alone (a one-line change with its test, made at the final pre-registration if chosen); **(c) add both blocks**, with a budget of $185.38 to be covered at the conservative high.
8. **Conflict of interest (r3 screen; DEVIATIONS Entry 0, Part F). DECIDED 2026-11-12, 00:48 CT: the default, S-COI as proposed (Denon and the five brands with Cheil Worldwide or Iris agency ties, 106 units; `COI_FLAGGED` unchanged), the programme's Cheil/Iris option (b) (DEVIATIONS Entry 0, Part G).** New ties found: Cheil Worldwide, a Samsung affiliate, or its Iris agency has done agency work for five registry brands — Chevrolet (Cheil for GM Korea, 2017), BMW (Iris, UK consumer PR, 2018), Bentley (Iris, Americas experiential agency of record from 2021), Jack Daniel's (Iris, UK digital, 2022; since replaced) and Eucerin (Iris with Cheil, search marketing for Beiersdorf, from 2024). Proposed handling, as for Denon: all stay in every primary test; a new sensitivity **S-COI** removes them and Denon together (106 units), reported beside every Presence test and in the abstract if a verdict differs (§7.5). Recorded and disclosed, not flagged: Samsung Electronics' chip contract with Tesla (2025–2033) and Samsung SDI's battery agreement with Hyundai (2023), supply relationships beyond v0.22's record (handled as v0.22's); Hotel Shilla's duty-free business (retail). Choices: accept S-COI as proposed; or flag a different set (for example add Tesla and Hyundai, or leave out the older agency ties, Chevrolet 2017 and BMW 2018); or treat agency work as general disclosure only (no S-COI). The set is one parameter (`COI_FLAGGED`).
Already decided (2026-11-10): languages ES, KO, ZH; window 2026-11-29..12-02 (`WINDOW`); headphones option A, Denon kept and disclosed (`HEADPHONES_OPTION = "A"`); category questions first, extras only if they fit (`BRAND_EXTRAS`). All are parameters in `osf/v62/scripts/params_v0_62.py`.

---

## §10 Declarations

## Conflict of interest {-}

The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. This study re-asks, in Spanish, Korean and Chinese, questions against brand registries fixed in earlier phases (v0.19–v0.23); it performs no new brand selection, and each registry carries its source-phase conflict-of-interest handling forward unchanged. Two items of record apply. In the automotive registry, Samsung subsidiaries hold tier-2/3 component supply relationships with several registry brands — Harman International (audio systems), Samsung SDI (battery cells), and Samsung Display (infotainment) — characterized in the source phase as non-competitive, with no brand-level overlap, and imposing no operational restriction on registry composition (v0.22 Declarations; screened in v0.22 DEVIATIONS Entry 0, Part B). In the audiophile-headphones registry, AKG was substituted with Denon before the v0.19 pre-registration lock because AKG's parent, Harman International, is a Samsung subsidiary. Correction (November 10, 2026): Denon, which replaced AKG in the v0.19 registry, has itself been owned by Harman International, a wholly owned subsidiary of Samsung Electronics, since September 23, 2025, when Harman completed its acquisition of Sound United from Masimo; the v0.19 headphones registry therefore includes one Samsung-group brand. The substitution did not achieve its purpose, and this was not noticed until November 10, 2026. The registries of this study are those of the English t₄ wave, with Denon included and disclosed as in the t₄ pre-registration; every result is also reported without the Denon unit and without the headphones category (DEVIATIONS Entry 0). One of the three languages is Korean, and South Korea is Samsung Electronics' home market: answers in Korean, as in any language, may name Samsung-group brands that are not registry units; such names are never coded or scored, because coding counts only the 112 registry units. The conflict-of-interest screen of this study (DEVIATIONS Entry 0, Part F) found further ties. Cheil Worldwide, a marketing company of the Samsung group in which Samsung Electronics holds 28.43%, or its agency Iris has done advertising, public-relations or search-marketing work for five registry brands: Chevrolet (for GM Korea, 2017), BMW (UK consumer public relations, 2018), Bentley (experiential agency of record in the Americas from 2021), Jack Daniel's (UK digital agency from 2022, since replaced) and Eucerin (search marketing for Beiersdorf from 2024). As the pre-registrant decided on November 12, 2026, these five brands are kept in every analysis, as Denon is, and every Presence result is also reported without them and Denon (sensitivity S-COI, 106 units). Samsung Electronics supplies semiconductors to Tesla under a contract running from 2025 to 2033, and Samsung SDI supplies batteries to Hyundai under an agreement of 2023; like the supply relationships of record, these are non-competitive and impose no restriction on the registries. Hotel Shilla, a Samsung affiliate, operates duty-free shops that sell brands of several registry categories among many others. Acquisition, coding and scoring are fully automated against the locked registries, and this pre-registration is locked and deposited before the first call. Samsung Electronics had no role in the design, conduct, analysis or reporting of this work.

## Funding {-}

Self-funded.

## Ethics {-}

Not applicable; no human subjects. Volunteer translation reviewers, if any, act as reviewers, not participants; no data about them is collected, and they are acknowledged only with their permission.

## Use of AI tools {-}

During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.

---

## §11 Lock procedure and change log

- **r0** (2026-11-10): French/Japanese design, translations, aliases, cost, DEVIATIONS Entry 0 (proposed).
- **r1** (2026-11-10): scripts and tests on fakes; parameters for the open choices; alias check record; gate P2 apostrophe fix.
- **r2** (2026-11-10/11): languages changed to Spanish, Korean and Chinese (below).
- **r3** (2026-11-11, this draft): cost re-based on t₄'s recorded usage; brand-question option; guard fix; MAC alias; r1 items closed; Samsung-group screen of all 112 units (below).
- **r3 update** (2026-11-12): the pre-registrant's decisions on §9 items 3, 7 (b) and 8 applied; dated change-log lines; adopted design's cost; dry run re-run; lock-manifest file list (below). Same revision, no new design element.
- **Before the lock:** the pre-registrant's choices (§9, notably items 3, 7 and 8; **made 2026-11-12, applied in the r3 update**); native checks or the per-language fallback; independent back-translations for unchecked languages; prices and model IDs re-read; P1 (after v0.42's scoring run) and P2 on t₄'s data; alias parity checks (MAC 魅可, Fernet Branca); the country column (§2.9 item 5); lock manifest. **Lock:** 24 hours after the pre-registrant receives the final text unless he objects; then manifest, commit, tag `v0.62-prereg-r1`, push, OSF deposit; only then `--collect`.

### r3 update (2026-11-12): the pre-registrant's decisions applied; dated change-log lines; files for the lock manifest

1. **Decisions** (pre-registrant, 2026-11-12, 00:48 CT, "as you suggest"): §9 item 7, option (b): the 88 yes/no brand questions only (block 4), run last, with the small code change made and checked before the lock; item 3, the default (the $100 cap, with the projection pause after block 1); item 8, the default (S-COI as proposed). The other §9 items stand as drafted.
2. **Code for item 7 (b)** (as r3 described it: a parameter that turns on block 4 alone, with its tests). `params_v0_62.BRAND_YES_NO = True` (new; `BRAND_EXTRAS` stays False). `acquire_v0_62.py`: `yes_no_on()`, `open_on()`, `design_key()`; `blocks_in_design`, `expected_total` and `build_specs` take `drop_open` (block 5 alone); `collection_specs` keeps block 4, last, and leaves block 5 out without recording any approval (as r3's fix requires); `projection_ratio` uses the central ratio of core + block 4 (3.0975 November, 3.0887 December, option A); no judge reserve without block 5; the dry run prints the design collected. `cost_estimate_r3_v0_62.py` adds `projection_core_plus_yn` (each headphones option) and `guard_core_plus_yn` to `cost_estimate_v0_62_r3.json/.txt`, re-run from the pinned t₄ record: every r3 number unchanged. Tests: 96 (r3's 88 + 7 acquisition + 1 cost), local fakes and pinned files only, all passing; r3's core-only tests now switch `BRAND_YES_NO` off and still pass. Nothing else in the code changed for item 7 (the pre-lock corrections are item 5).
3. **Dry run** re-run with the r3 guard fix on the adopted design (§6.5; `dry_run_fake_sdk_v0_62_r3.txt`).
4. **Change-log lines (2026-11-12).**
   - (i) **Buyer-persona limitation** added (§8 limitation 11; programme plan update agreed by the pre-registrant on 2026-11-11, 23:22 CT, "ok plan updates"). Cites only sources marked Verified in the programme's literature check of 2026-11-11: Jack, Lehman, Maloney and Xu, arXiv 2605.30207, and Rienecker et al., ChoiceEval, arXiv 2603.18300. arXiv 2605.27439 (same four authors) is only partly verified there (its abstract does not contain the persona figures) and is not cited. No test added.
   - (ii) **Conflict of interest, Cheil Worldwide / Iris** (programme option (b); §9 item 8 decided): the five brands with agency ties stay in every analysis and every Presence result is also reported without them and Denon (S-COI, 106 units; `COI_FLAGGED` unchanged; DEVIATIONS Entry 0, Parts F–G); §10 says so in one sentence. No design change.
   - (iii) **Gemini 4 Carbon became generally available on 2026-11-10** (Google Cloud documentation, "Gemini 4 Carbon": "Launch stage: GA", "Release date: November 10, 2026", page "Last updated 2026-11-11 UTC", https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/4-carbon; Google's announcement "Gemini 4 Carbon is now available", Nov 10, 2026, https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-carbon-now-available/; both opened 2026-11-12). v0.62 stays on Gemini 4 Argon (`gemini-4-argon`): its questions are compared with t₄'s answers from the same three models (§2.1, §5.3), so a model change would confound language with model. No design change.
   - (iv) **Noted, no change** (v1.15's finding of 2026-11-11: Claude Opus 5.5 put a sentence before a required JSON reply on 4.2% of first tries, and strict parsing then failed). v0.62 parses no JSON and, with block 5 not collected, calls no LLM judge. Block 4's yes/no answers are read as plain text (§4.4): a leading answer word is mapped to Yes / No, then the certified parsers read the answer (v0.20–v0.22 `parse_yes_no`: the first word, else the first sentence; v0.19 `parse_phase_a_response`: the earliest yes/no word anywhere). The analogous failure can occur: an answer that puts a sentence before its answer word is coded as a non-answer, or, in Spanish, read as No when that sentence contains the negation *no* (dry run: 16 of 16 Spanish, 33 of 33 Korean and 35 of 35 Chinese preamble answers were non-answers; 18 of 18 Spanish preambles containing *no* were read as No). Only the recognition descriptive (§2.9 item 2) is affected; no confirmatory test.
5. **Pre-lock corrections** (coordinator's decision, 2026-11-12, after this update's first commit `0074bc1`): two corrections that make the code match the written rules and the programme's guard practice; no hypothesis, test, threshold, unit set, model, prompt or analysis changes.
   - (a) **Chinese "No" answers (§4.4).** r3's `code_v0_62.map_answer_words` mapped 否 / 不是 / 不 to "No" but kept an ideographic full stop or unspaced text after it ("否。" → "No。"; "不是，这不是。" → "No,这不是。"), and v0.20–v0.22's certified `parse_yes_no` then returned "ambiguous" (a non-answer), while the same forms of 是 were read as Yes; v0.19's parser read both. Without the correction, Chinese recognition (§2.9 item 2) for the 72 v0.20–v0.22 units would have lost No answers and read high. Corrected: in Chinese the mapped word is set off by a space wherever it touches another character ("否。" → "No 。", "不是，这不是。" → "No ,这不是。", "“否”。" → "“ No ”。"), so the certified parsers read every 否 / 不是 / 不 form as No and every 是 / 是的 form as Yes, as §4.4 states. Spanish and Korean mappings are byte-identical to r3's, and v0.19's readings are unchanged. Answers with Markdown bold (\*\*否\*\*, \*\*是\*\*) are, as at r3, not mapped in either direction (§4.4's lookahead does not list \*), so they remain non-answers on both sides. Tests: 7 (`ZhAnswerWordsCertifiedParsers`, with the certified parsers of this tree, checked to be v0.42-prereg-r1's blobs); dry run: 11 of 11 plain "否。" answers now read as No (10 were non-answers before).
   - (b) **Record of Message Batches in flight.** Ported from v0.42's `acquire_v0_42.py` (C26 (ii); v0.44 C11 (d) does the same for its requests): every created Claude Fable 5.2 batch is journaled in `osf/v62/data/v62_batches.jsonl` before it is polled and marked recorded once its lines are written; at the start of every `--collect`, `recover_batches` fetches and records any batch left in flight by a stopped run (no line written twice, nothing re-sent, its spend counted) before any new request. `_journal`, `open_batches`, `written_batch_requests`, `recover_batches` and `_finish_batch` are v0.42's, with v0.62's batch lines unchanged (errored or expired requests costed at worst case). Tests: 3 (two ported from v0.42's tests); dry run: a stop mid-batch is recovered as above (§6.5).
   - (c) Noted, not changed (it only errs toward pausing): every `--collect` re-applies the projection check after block 1 to the total spend so far (v0.42 C26 (iv) applies it once), so a re-run pass after a main pass at central cost with any failed call pauses until `--approve-projection`.
   - Tests after the corrections: 106 (96 + 7 + 3), all passing.
6. **Files the lock manifest will cover** (SHA-256 of each, computed at the lock; not computed here): the final pre-registration `osf/v62/prereg/PRE_REGISTRATION_v0_62.md`; every other file in `osf/v62/prereg/` (drafts r0–r3; cost estimates r0–r3, .json and .txt; `coi_screen_v0_62_r0.txt`, `_r3.txt`; `gate_P1_v0_62_r2.json`, `_r3.json`; `dry_run_fake_sdk_v0_62_r2.txt`, `_r3.txt`); `osf/v62/DEVIATIONS.md`; `osf/v62/PLAIN_SUMMARY_v0_62_r0.md`, `_r3.md`; `osf/v62/inputs/` (`probes_v0_42.jsonl`, `cost_estimate_v0_42_r2.json`); `osf/v62/translations/` (`translations_v0_62_r0.json`, `_r2.json`; `translation_review_v0_62_r0.md`, `_r2.md`; `probes_{es,ko,zh}_v0_62_r2.jsonl`; `probes_{fr,ja}_v0_62_r0.jsonl`; `brand_aliases_v0_62_r0.csv`, `_r1.csv`, `_r2.csv`; `alias_check_v0_62_r1.csv`; `build_check_v0_62_r0.txt`, `_r2.txt`); every `osf/v62/scripts/*.py` (acquire, budget, params, code, score, gate_p1, gate_p2, cost_estimate and cost_estimate_r3, build_translated_probes, make_alias_table_r1 and _r2, check_aliases, coi_screen, and the helpers `_fork_v0_62.py`, `_make_r1_text.py`, `_patch_cost_v0_62.py`, `_dry_run_fake_sdk_v0_62.py`, `_fakesdk_v0_62.py`) and `_acquire_tail_v0_62.py.txt`; every `osf/v62/scripts/tests/*.py` (6 files). Earlier-phase files in this tree that v0.62 reads or imports unchanged (the same git blobs as at tag `v0.42-prereg-r1`): `scripts/score_v20.py`, `score_v21.py`, `score_v22.py`, `score_v0_23.py`; `scripts/run_acquisition_v20.py`, `_v21.py`, `_v22.py`; `osf/v19/acquire_v0_19.py`. Pinned by tag and recorded by git blob or SHA-256 (not in this branch): v0.42's coder `osf/v42/scripts/code_t4_v0_42.py` (blob `2d36735d…`), v0.42's kernels at tag `v0.42-prereg-r1` (`58d1891`), and `t4_raw.jsonl` / `t4_batches.jsonl` at tag `v0.42-acquisition-locked` (`a790bb1`; SHA-256 `f3109091…96d4bf`, `d73b8e81…39298c`). Not covered: `__pycache__`; `osf/v62/data/` and `osf/v62/anchor/` (written at and after the lock).
7. **The 24 hours** of r3 are not restarted: this update applies choices that r3 put to the pre-registrant (item 7 (b) exactly as r3 described it), adds a limitation and dated disclosures, records checks, and makes two pre-lock corrections that bring the code into line with §4.4's written rule and the programme's guard practice (item 5); no hypothesis, test, threshold, unit set, model, prompt or analysis changed.

### Changes from r2 (r3 working draft)

1. **Cost re-based on t₄'s recorded usage** (§6.2–§6.4; `cost_estimate_r3_v0_62.py` → `cost_estimate_v0_62_r3.json/.txt`): v0.42's t₄ record at tag `v0.42-acquisition-locked` (`a790bb1`), usage fields only, reconciled with the recorded spend ($67.4551 + $0.50 = $67.9551); central = t₄ mean tokens × 1.02, conservative high = t₄ p90 tokens × 1.10, both × r2's language factors; per block at November and December prices. Core: central $33.44 (Nov) / $38.84 (Dec), conservative high $121.80 (Dec) (r2: $55.50 / $142.06). The acquisition reads the r3 file (`COST_PATH`).
2. Prices re-read on 2026-11-11 (vendor pages cited in §6.1): unchanged.
3. **Brand questions:** still off under the §5.2 rule (conservative high of blocks 1–5: $185.38); none fits under the $80 pause at the conservative high; the option, its cost, the smallest budgets ($124.77 with the yes/no questions; $185.38 with all 112) and the descriptives they serve are put to the pre-registrant (§9 item 7). Nothing was added or dropped.
4. **Guard fix (§6.5):** `collect()` no longer records a `drop_phase_a` approval when the extras are off (that approval switched off the projection pause in the adopted design); `collection_specs()`; the dry run prints the core's cost; 4 regression tests.
5. **Alias (§4.2):** MAC Cosmetics' Korean alias 맥 코스메틱스 added (brand Korea site), 맥 코스메틱 kept; KO 120 aliases; unit test.
6. **r1 open items:** P2's both-sides rule implemented in code (`gate_p2_v0_62.py`, with the apostrophe delta reported) and tested with the real certified matchers (§7.3); P1 re-run against v0.42's locked kernels: PASS (`gate_P1_v0_62_r3.json`).
7. **Conflict of interest (DEVIATIONS Entry 0, Part F):** all 112 units screened for ownership, Korean distribution or licensing by a Samsung affiliate, Harman brands and Cheil Worldwide's agencies, with Korea in mind; source phases' handling carried verbatim (v0.19 with the Nov 10 correction; v0.22 supply relationships). Five new agency ties (Chevrolet, BMW, Bentley, Jack Daniel's, Eucerin: Cheil Worldwide or Iris) handled like Denon: kept, plus the new sensitivity S-COI (§7.5; `params_v0_62.COI_FLAGGED`; scorer and 2 tests). Supply relationships beyond v0.22's record (Tesla, Hyundai) and Samsung-affiliated retail (Hotel Shilla) disclosed (§10). String screen re-run with 70 terms (`coi_screen_v0_62_r3.txt`: Denon only).
8. **Tests:** 88 unit tests (65 at r2 + 23: acquisition 4, cost r3 8, gate P2 8, coder 1, scorer 2), local fakes and pinned files only, no network, no model, all passing.

### Changes from r1 (r2 working draft)

1. Languages: ES, KO, ZH (Simplified, Mainland usage) replace FR, JA (pre-registrant's decision, 2026-11-10 20:44 CT); rationale in §0.
2. Translations r2 (30 + 5 + 15 items × 3 languages) with back-translations and drift codes; probe files r2; build check r2 PASS.
3. Native-check plan conditional per language with the back-translation fallback stated as a per-language limitation (§3.2, §8).
4. Alias table r2 (KO 119, ZH 80, ES none) with check record and counts (§4.2); matching rules KO-1, KO-2, ZH-1, ZH-2, script variants, collision list (§4.3); answer words for ES/KO/ZH (§4.4); MC_Language rules for ES/KO/ZH; new MC_Script and S-Script.
5. Design: category questions first in all three languages (810 calls, core); brand-question extras only if the high estimate fits (`BRAND_EXTRAS`, off at r2) (§5.2).
6. Cost r2: language factors ES 1.25/1.50, KO 1.75/2.50, ZH 1.50/2.25; December prices for the whole run; judge reserve 216 answers ($2.46); the high core estimate ($142.06) exceeds the cap and is put to the pre-registrant (§6.3, §9).
7. Guard: conservative counting (failed attempts and errored/expired batch requests at worst case; OpenAI page opens as searches; Gemini tool tokens; two worst cases reserved per synchronous call) (§6.5).
8. Gate P1 run against v0.42's locked kernels (tag `v0.42-prereg-r1`): PASS on synthetic tables (§7.3).
9. Hypotheses per language ×3; seeds 6201x1–3; joint reading over three languages (§2).
10. Declarations: COI note for the Korean language (registries are t₄'s; Denon disclosed as in v0.42 with the canonical Denon/Harman wording copied from v0.42's locked pre-registration; brand names outside the registries never scored); Ethics note on volunteer reviewers; AI-use statement verbatim.
11. Tests: 65 unit tests (local fakes, no network, no model), all passing; fake-SDK dry run of the acquisition (§7.6).
