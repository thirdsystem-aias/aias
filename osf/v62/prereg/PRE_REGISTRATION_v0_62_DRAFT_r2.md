
# AIAS™ Presence Measurement Protocol — Pre-Registration v0.62 (revision r2, WORKING DRAFT — not locked, not final)

Pablo Ulpiano González Castro
School of Visual Arts, MPS Branding Program, New York, NY (primary academic affiliation)
Third System™ (research entity; data archive and methodology venue)
Correspondence: pablou@pablou.com · pablou.com
ORCID: 0009-0003-8968-9990 (linked: https://orcid.org/0009-0003-8968-9990)

**Study:** The non-English wave — do AI availability scores measured in Spanish, in Korean and in Chinese reproduce the English values of the t₄ wave?
**Languages (r2):** Spanish (neutral Latin American usage), Korean (South Korea, standard), Chinese (**Simplified script, Mainland usage**, zh-Hans-CN). They replace r0/r1's French and Japanese (pre-registrant's decision, 2026-11-10, 20:44 CT; §0).
**Design:** The t₄ panel (v0.42 r2): the five omnibus categories (v0.19 audiophile headphones, v0.20 skincare, v0.21 cosmetics, v0.22 automotive, v0.23 premium spirits; 112 brand units), asked of the same three models as t₄ (N3: Claude Fable 5.2, GPT-6 Astra, Gemini 4 Argon) without web search (S0). **Adopted core: the 30 category questions (Phase B) in all three languages, three runs: 3 × 3 × 30 × 3 = 810 calls.** The 112 brand questions (Phase A, one run; 1,008 more calls) are **extras, collected only if they fit** (§5.2, §6.4): at r2 their high estimate does not fit, so they are off (`BRAND_EXTRAS = False`).
**Budget:** at most US$100 of paid model calls for the paper, hard cap; pause at $80; both from actual recorded usage (programme rule, 2026-11-10). **December prices are used for the whole run** (the window straddles Gemini 4 Argon's price change on 2026-12-01; conservative). Core (810 calls): **expected $55.50, high $142.06**. Full design with extras (1,818 calls): expected $98.59, high $260.68. The high figures exceed the cap; §6 states what the guard does and what the pre-registrant decides. All figures: `python3 osf/v62/scripts/cost_estimate_v0_62.py` (r2 output `osf/v62/prereg/cost_estimate_v0_62_r2.txt`).
**Protocol version:** recall Presence π̂ and recognition (v1.6, SSRN 6816340), Consistency φ (v1.8, SSRN 6963359), both as implemented for t₄ in `osf/v42/scripts/score_v0_42.py` (locked, tag `v0.42-prereg-r1` → `58d1891`); Ranking, only if v1.14 passes (§2.4), as v1.14 defines it (modal position R\*, tag `v1.14-prereg-r1`).
**Pre-registrant:** Pablo Ulpiano González Castro
**Status:** r2 working draft (2026-11-10/11, programme runner, lane v0.62-r2), built on r1; every change is listed in §11 "Changes from r1". No study probe has been sent and none will be before the lock.
**Lock target:** git tag `v0.62-prereg-r1` on branch `v0.62`, pushed to `origin`; external anchor: deposit of the pre-registration, the English source probes, the Spanish, Korean and Chinese probe files with their back-translations and review record, the alias table, the cost estimate, DEVIATIONS.md, the scripts and tests and the lock manifest at OSF `ec6wh` → `v62/prereg/` and `v62/anchor/` before the first call. Locks 24 hours after the pre-registrant receives the final text, unless he objects (programme rule, Nov 9, 2026); the 24 hours of this r2 start when he receives it.
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
2. Recognition (Phase A) per model × language beside English t₄ — only if the extras are collected.
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
- **Korean:** 119 Hangul aliases over 111 units (ZMF Headphones has none), e.g. 젠하이저, 오디오테크니카 / 오디오 테크니카, 토요타 / 도요타, 현대자동차 / 현대차.
- **Chinese:** 80 Han aliases over 74 units (38 units have no established Chinese name the runner could state and are matched in Latin script only), e.g. 森海塞尔, 铁三角, 雅诗兰黛, 宝马, 尊尼获加.
- **Spanish:** no alias. Spanish keeps the registry names; the brands where Spanish usage differs in spelling were checked: *Bacardí*, *Patrón* / Patron, *L'Oréal París* (accents, removed by the certified matchers' accent stripping), *Rémy Martin*; *Fernet Branca* without hyphen (Argentine usage) is a parity check against the v0.23 matcher before the lock, no alias added.
- **Parity rule (as r1).** An alias may not be looser than the certified English matcher, which counts only the full registry string: bare 벤츠 / 奔驰 (Mercedes-Benz), 디올 / 迪奥 (Dior Beauty), 샤넬 / 香奈儿 (Chanel Beauty), 아르마니 / 阿玛尼, 톰 포드 / 汤姆福特, 로레알 / 欧莱雅 and 맥 (MAC Cosmetics) are not aliases. ZH 肌肤之钥 is the full Chinese name of Clé de Peau Beauté and is kept; ZH 魅可 (MAC) is kept pending the v0.21 matcher parity check.
- **Common words excluded:** bare 현대 / 现代 ('modern') for Hyundai; bare 大众 ('the public', 'mass market') for Volkswagen (大众汽车, 上汽大众, 一汽-大众 kept).
- **Check record (2026-11-11 UTC; source and date per row).** Each alias is CONFIRMED only if the runner opened the brand's own Korean/Chinese site or a dated authoritative page showing it; PARTLY if seen only on a secondary dated source or only one of several forms was seen; otherwise UNCONFIRMED (in force as a spelling transcription, flagged for the native check). **Korean: 0 confirmed, 3 partly (Sennheiser, Denon, Sony), 108 unconfirmed, 1 without alias. Chinese: 2 confirmed (Sennheiser, brand press release dated 2025-04-10; Audio-Technica, brand China site), 2 partly (HiFiMan, Beyerdynamic 拜雅), 70 unconfirmed, 38 without alias.** One check changed nothing but is recorded: Denon's Chinese site writes "Denon" in Latin script (its company name uses 电音, which is not adopted as an alias: it also means 'electronic music'); 天龙 stays unconfirmed.

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

### §4.4 Recognition answers (Phase A; only if the extras are collected)

v0.19–v0.22: a leading ES *sí* / *no* (unaccented *si* only before punctuation or the end, so *Si bien…* is not read as yes), KO 예 / 네 / 아니요 / 아니오 / 아니 (not followed by a Hangul syllable, so 네이버 is not read as yes), ZH 是的 / 是 / 否 / 不是 / 不 (是 and 不 only before punctuation, space or the end, so 是一个… and 不太… are not mapped) is replaced by Yes / No and the certified parser `parse_yes_no` reads the answer; unparsed answers are non-answers (v0.42 C6). v0.23 open answers: the t₁–t₄ recognition judge with its English instruction unchanged; Claude Sonnet 4.5 retires on 2026-11-30, so the judge calls (after the 2026-11-29..12-02 collection) use the successor judge that t₅ adopts, with t₅'s parity check, logged in DEVIATIONS.

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
| 4 | A, v0.19–v0.22 yes/no (88 per language) | ES, KO, ZH | 1 | 264 | 792 | extra (off at r2) |
| 5 | A, v0.23 open (24 per language) | ES, KO, ZH | 1 | 72 | 216 | extra (off at r2) |
| **Core / with extras** | | | | **270 / 606** | **810 / 1,818** | |

Within a block: one worker per model, the three in parallel, ES then KO then ZH, probes in file order. Every confirmatory test (Presence, Consistency, Ranking) uses blocks 1–3 only; blocks 4–5 feed descriptives (§2.9 item 2) only. **Extras rule (fixed now):** blocks 4–5 are collected only if `params_v0_62.BRAND_EXTRAS` is True at the lock, which the final pre-registration sets only if the high estimate of blocks 1–5 (re-based on t₄'s recorded English usage, §6.2) is at or below $100. At r2 it is False. Phase B three runs per language: as t₄ (a one-run π̂ against a three-run English π̂ would attenuate ρ for a reason that is not language; φ needs two defined runs). Search on (S1) not collected (r1 §5.2).

### §5.3 Panel and §5.4 Call settings

As r1: N3 as verified for v0.42 r2 (Claude Fable 5.2 `claude-fable-5-2` through Anthropic's Message Batches API; GPT-6 Astra `gpt-6-astra` and Gemini 4 Argon `gemini-4-argon` synchronous), re-verified at the final pre-registration; t₄'s S0 settings exactly (no tools; no system prompt; sampling at provider defaults; maximum output 16,384 tokens; v0.42's retry policy and re-run pass); no language, locale or region parameter. Raw artefact `osf/v62/data/v62_raw.jsonl` with v0.42's fields plus `language`.

### §5.5 Window and guards

As r1: window 2026-11-29..12-02 US Central, 72 hours from the first call; refusal during 2026-11-17..21; one collection at a time; `--collect` refuses unless the tag is on `origin` and the OSF anchor names its commit; a slip needs a DEVIATIONS entry first.

---

## §6 Budget

### §6.1 Cap and prices

At most $100 of paid model calls for this paper, including re-sends and (if Phase A is collected) the v0.23 judge; pause at $80; both from actual recorded usage. Prices (programme list read 2026-11-10, US$ per 1M tokens in/out; vendor sources in v0.42 r2 §4.5): Claude Fable 5.2 batch 4 / 20 (used); GPT-6 Astra standard 10 / 50 (used; batch not used, as t₄); Gemini 4 Argon standard 2 / 10 through 2026-11-30 and **4 / 20 from 2026-12-01 — the December price is used for the whole run**, since the window straddles the change; judge 3 / 15. Re-read at the final pre-registration.

### §6.2 Per-call basis and language factors

- **English basis.** v0.42 r2's measured-basis per-call figures (`osf/v62/inputs/cost_estimate_v0_42_r2.json`, SHA-256 checked), central / high with re-sends (the high basis assumes Claude Fable 5.2 at three times Claude Opus 5.5's v0.39 token use).
- **Language factors (declared assumptions, not measured), on the whole per-call cost: central ES 1.25, KO 1.75, ZH 1.50; high ES 1.50, KO 2.50, ZH 2.25.** Korean and Chinese are set conservatively: Hangul and Han text usually costs more tokens per unit of meaning than English in byte-pair tokenizers, by vendor-specific amounts not published for these models; no Korean or Chinese answer from them is on record and no tokenizer is installed on the collection machine. At the final pre-registration the English basis is replaced by t₄'s recorded usage (S0, per model and question type) times these factors; during collection the projection pause uses actual usage, and the measured factor is reported (§2.9 item 3).
- **Judge reserve** (only with block 5): 216 open answers × (1,500 input tokens × 2.50 + 10 output) at 3 / 15 = **$2.46**.

### §6.3 Estimate (December prices, US$, expected / high)

| Language × model | Calls (core / with extras) | Core: blocks 1–3 | With extras: blocks 1–5 |
|---|---|---|---|
| ES, Claude Fable 5.2 (batch) | 90 / 202 | 8.44 / 20.12 | 14.48 / 35.90 |
| ES, GPT-6 Astra | 90 / 202 | 3.93 / 6.90 | 7.10 / 12.48 |
| ES, Gemini 4 Argon | 90 / 202 | 3.05 / 7.08 | 5.13 / 13.59 |
| KO, Claude Fable 5.2 (batch) | 90 / 202 | 11.82 / 33.53 | 20.27 / 59.83 |
| KO, GPT-6 Astra | 90 / 202 | 5.50 / 11.50 | 9.94 / 20.80 |
| KO, Gemini 4 Argon | 90 / 202 | 4.27 / 11.80 | 7.18 / 22.65 |
| ZH, Claude Fable 5.2 (batch) | 90 / 202 | 10.13 / 30.18 | 17.37 / 53.85 |
| ZH, GPT-6 Astra | 90 / 202 | 4.71 / 10.35 | 8.52 / 18.72 |
| ZH, Gemini 4 Argon | 90 / 202 | 3.66 / 10.62 | 6.15 / 20.39 |
| Judge reserve | (216) | — | 2.46 / 2.46 |
| **All** | **810 / 1,818** | **55.50 / 142.06** | **98.59 / 260.68** |

(Cells rounded; totals from unrounded values. Block 1 alone: 270 calls, 18.50 / 47.35.)

By phase (with extras): Phase B 55.50 / 142.06; Phase A yes/no 25.82 / 78.28; Phase A open 14.80 / 37.88; judge 2.46; sum 98.59 / 260.68 (sum check in the script output). Further lines (`cost_estimate_v0_62_r2.txt`): core + yes/no extras 1,602 calls 81.32 / 220.34; core + open extras 1,026 calls 72.77 / 182.40; per language (with extras) ES 27.52 / 62.79, KO 38.20 / 104.11, ZH 32.86 / 93.78; at English token counts (factor 1.0) the design with extras would cost 66.55 / 126.41; November prices (reference only) with extras 89.36 / 232.37, core 50.02 / 127.31.

**Reading.** (a) The **core fits at the expected cost** ($55.50, under the $80 pause). (b) **At the high estimate the core does not fit** ($142.06 > $100): the high scenario combines the high Fable basis with the high Korean and Chinese factors. (c) **The extras do not fit at the high estimate under any combination** (the core alone is above the cap), so by the pre-registrant's rule they are off at r2. (d) Break-even on the high basis (with extras, December): the design reaches $80 at a uniform language factor of 0.63 and $100 at 0.79 — the high basis exceeds the cap even at English token counts ($126.41).

**What happens in the high scenario (core only).** Block 1 would cost about $47.35; the projection pause (§6.5) multiplies the block-1 call spend by 3.0 (the three Phase B runs cost alike) and pauses after block 1 whenever the projection passes $80 (block-1 spend above $26.67). The pre-registrant then chooses: continue under the $80 pause and $100 stop (in this scenario blocks 1–2 cost $94.71: the $80 pause falls inside block 2 and the $100 stop early in block 3, leaving about two runs), fallback F2 (drop run 3: φ then needs both remaining runs defined; declared asymmetry with the three-run English value), drop a language, or raise the budget for this paper. **The smallest budget that covers the high scenario of the core is $142.06**; for the core with extras, $260.68. Per the programme's budget rule, this is put to the pre-registrant now (§9 item 3); the r2 recommendation is to keep the core at $100 and re-base the estimate on t₄'s recorded usage before the lock (t₄ is collecting now), which replaces the assumed high Fable basis with measured tokens.

### §6.4 Design trade-off (December prices, expected / high)

| Design | Calls | Expected | High |
|---|---|---|---|
| **Adopted at r2: core, Phase B S0 × 3, ES + KO + ZH** | **810** | **55.50** | **142.06** |
| Core + Phase A yes/no (v0.19–v0.22) | 1,602 | 81.32 | 220.34 |
| Core + Phase A open (v0.23) | 1,026 | 72.77 | 182.40 |
| Core + both extras (full t₄ S0 panel) | 1,818 | 98.59 | 260.68 |
| Phase B S0 × 2 + Phase A (fallback F2 with extras) | 1,548 | 80.09 | 213.33 |
| Phase B S0 × 1 + Phase A (not adopted: no φ, no run noise) | 1,278 | 61.59 | 165.98 |
| Full + Phase B S1 × 1 (not adopted) | 2,088 | 167.45 | 471.69 |
| One language only, with extras: ES / KO / ZH | 606 each | 27.52 / 38.20 / 32.86 | 62.79 / 104.11 / 93.78 |

What the design gives up: recognition (Phase A) in the three languages unless re-based estimates allow it; search-on answers; within-provider replication.

### §6.5 Guard (from actual usage; conservative counting, r2)

v0.42's ledger arithmetic, with these r2 rules (`budget_v0_62.py`, `acquire_v0_62.py`; each unit-tested):
1. **Spend** = judge reserve (only if block 5 is collected; else $0) + the cost of every raw line from its recorded usage, each request at the price of the UTC date it started.
2. **Failed attempts count at worst case.** Every attempt of a synchronous call that returned no usage (timeouts and other transient failures; the copied call function does not distinguish them) is costed at the request's worst case (16,384 output tokens, 2,000 input tokens); a final non-transient 4xx error is not billed. Errored or expired batch requests are costed at the batch worst case.
3. **Searches** (S1 only; S0 sends no tool): every OpenAI page-open or find-in-page action counts as a billed search; a Gemini part with searches but no reported tool-token count is charged 150,000 extra input tokens.
4. **Reservations.** Before each request its worst case is reserved; **two worst cases per synchronous call** (it may be re-sent: retry or empty re-send): GPT-6 Astra $1.6784, Gemini 4 Argon $0.6714 (December); Claude Fable 5.2 batch $0.3357 per request.
5. **Hard stop:** no request if spend + reservations + its reservation would exceed $100. **Pause at $80:** no new request until the pre-registrant's `--approve-past-80`. **Projection pause:** after block 1, projected total = block-1 call spend × 3.0 (core) or × 5.3288 (with extras, December; adopted ÷ block 1, central); above $80 → pause; options as §6.3.
Fake-SDK dry run (§7.6) shows the effect of rule 2: with about 30% adversarial attempts the guard's spend ran $51 above an independent bill of the requests that returned usage, and the $80 pause fell inside block 3. Rule 2 over-counts rate-limit (429) failures, which vendors do not bill; this is accepted as conservative.

---

## §7 Analysis plan

### §7.1 Coding

Phase B mentions: the pre-step of §4.3, then each category's certified matcher as v0.42's coder calls it (`code_t4_v0_42.py`, run unchanged as a separate process on prepared copies, one language at a time). Phase A: §4.4. Coder `osf/v62/scripts/code_v0_62.py`.

### §7.2 Computation

`osf/v62/scripts/score_v0_62.py`, tested on synthetic data and run once after the gates. Its π̂ and φ kernels are transcriptions of v0.42's (the v0.62 branch does not contain osf/v41–v42); gate P1 checks them against v0.42's locked kernels.

### §7.3 Gates (before any statistic)

- **P1 (kernel parity).** r2: run against v0.42's **locked** kernels, pinned to tag `v0.42-prereg-r1` (`58d1891`): `score_v0_42.pi_hat`, `phi_runs`, `phi_panel` and `score_v41.phi_m` read from the tag with `git show` and executed unchanged (`gate_p1_v0_62.py`). On three synthetic English-shaped tables (112 units; complete; with missing model-runs; seeds 620151–620153) the transcriptions reproduce π̂ and (φ, partition) exactly for all 112 units: **PASS, 0 mismatches** (`osf/v62/prereg/gate_P1_v0_62_r2.json`); unit tests show the gate fails on a perturbed kernel. v0.42's real answers were not read; the same comparison on t₄'s coded tables is run at the lock.
- **P2 (pre-step inert on English).** The pre-step + certified matchers on English t₄ answers reproduce v0.42's mention and recognition codes exactly, with the apostrophe mapping applied to both sides (r1 fix). Unit-tested now; run on t₄'s coded answers at the lock.
- **P3 (probe parity).** Probe files' SHA-256 equal the lock manifest; every sent prompt equals its probe text.
- **P4 (alias reach).** Every KO and ZH alias, inside particles, lists, Markdown bold and after a number, is coded as a mention of its unit and no other; fixed decoys yield no mention: 현대적인, 코스메틱, 로드바이크, 파이널, 엘프, 现代, 大众, 迪奥, 香奈儿, 欧莱雅, 阿玛尼, 奔驰, 벤츠, 디올, 맥. r2: PASS in the unit tests on the full r2 table (119 KO × 5 frames, 80 ZH × 4 frames).

### §7.4 Drop rule and missing data

As r1, per language: a model × language × phase with < 90% of its calls answered is excluded for that language and phase; `H_Lang_*` in L need all three models in Phase B in L, otherwise UNDETERMINED for L. Calls not sent because of a budget stop count as unanswered. No imputation.

### §7.5 Sensitivities (reported; no verdict changes)

S-Denon (111 units); S-Headphones (96 units); S-Language (off-language answers excluded); S-Script (ZH answers with Traditional-only characters excluded); S-Alias (collision-prone aliases off); S-Uncentred. If a primary verdict differs under S-Denon or S-Headphones, the paper reports both in its abstract (default (3) of 2026-11-10: every result is also shown without Denon and without the headphones category).

### §7.6 Reporting and dry run

Every test reported, including failures and undetermined results; raw answers, coded tables and verdicts deposited. Public-study rules apply: no focal brand, no lesson addressed to a brand, no brand contacted. Before the lock a fake-SDK dry run exercises the acquisition (r2: `osf/v62/prereg/dry_run_fake_sdk_v0_62_r2.txt`; 810 core specs; adversarial cases per model: transient failures, timeouts, fatal 4xx, empty answers re-sent once, refusals, truncation at the cap, served-model mismatch, English-language and Traditional-script answers, expired and errored batch requests).

---

## §8 Limitations

1. **Translations are model-made.** The back-translations are by the same model and not independent. Native review is planned (Spanish: the pre-registrant; Korean and Chinese: student volunteers, if any). **For any language without a native check before the lock, the paper states that its questions were checked by back-translation only** (independent, fresh session), and that naturalness is unverified for that language.
2. The forward translator (Claude) belongs to the same provider as one of the three measured models.
3. Language is varied without a market: the registries are US-market selections; Spanish-, Korean- and Chinese-speaking users would also ask about brands absent here. The study tests whether the same brands are ordered alike. The Chinese results describe what these three models answer when asked in Simplified Chinese, not what users in any particular country receive from locally available assistants.
4. One variety per language: neutral Latin American Spanish (not Peninsular), standard South Korean, Simplified Mainland Chinese (not Traditional).
5. Time and language are confounded (t₄ mid-November; v0.62 late November / early December); §2.7's t₅ benchmark helps only if t₅ is scored in time.
6. Search off only.
7. Korean and Chinese coding rests on a new alias table, mostly unconfirmed at r2 (§4.2), and some aliases are also common words (MC_Alias, S-Alias). Brands without a Chinese alias are matched in Latin script only, which under-counts any Han-script mention the runner could not anticipate.
8. One model per provider and three runs, as t₄.
9. Cost assumptions for Korean and Chinese token use are unmeasured until collection; at the high estimate the core exceeds the $100 cap (§6.3), so a budget stop could cut confirmatory runs unless re-based estimates or the pre-registrant's choice prevent it.
10. Recognition (Phase A) is not collected unless the extras fit (§5.2).

---

## §9 Decisions for the pre-registrant (before the lock)

1. **Chinese variety.** Default: Simplified, Mainland usage (as the decision names). Alternative: Traditional (Taiwan), which would need a new translation and alias pass.
2. **Spanish variety.** Runner's choice: neutral Latin American (*usted*, *auto*, *auriculares*). Alternative: Mexican or Rioplatense usage (e.g. *audífonos*), or Peninsular.
3. **Budget in the high scenario** (§6.3): keep the core at $100 and re-base on t₄'s recorded usage before the lock (recommended); or authorise up to $142.06 for the core; or drop a run or a language if the projection pause triggers.
4. **Native checks.** Spanish: the pre-registrant. Korean and Chinese: whether any student volunteer accepts Friday's invitation; the fallback of §3.2 step 3 applies per language otherwise.
5. **Study-list labels** for the non-English wave (r0's #52/#53 were French and Japanese).
6. Settled by the runner (can be overruled): Latin script for brand names in the questions (§4.1); KO/ZH matching rules (§4.3); v0.21 scope rule in all three languages (§3.3).
Already decided (2026-11-10): languages ES, KO, ZH; window 2026-11-29..12-02 (`WINDOW`); headphones option A, Denon kept and disclosed (`HEADPHONES_OPTION = "A"`); category questions first, extras only if they fit (`BRAND_EXTRAS`). All are parameters in `osf/v62/scripts/params_v0_62.py`.

---

## §10 Declarations

## Conflict of interest {-}

The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. This study re-asks, in Spanish, Korean and Chinese, questions against brand registries fixed in earlier phases (v0.19–v0.23); it performs no new brand selection, and each registry carries its source-phase conflict-of-interest handling forward unchanged. Two items of record apply. In the automotive registry, Samsung subsidiaries hold tier-2/3 component supply relationships with several registry brands — Harman International (audio systems), Samsung SDI (battery cells), and Samsung Display (infotainment) — characterized in the source phase as non-competitive, with no brand-level overlap, and imposing no operational restriction on registry composition (v0.22 Declarations; screened in v0.22 DEVIATIONS Entry 0, Part B). In the audiophile-headphones registry, AKG was substituted with Denon before the v0.19 pre-registration lock because AKG's parent, Harman International, is a Samsung subsidiary. Correction (November 10, 2026): Denon, which replaced AKG in the v0.19 registry, has itself been owned by Harman International, a wholly owned subsidiary of Samsung Electronics, since September 23, 2025, when Harman completed its acquisition of Sound United from Masimo; the v0.19 headphones registry therefore includes one Samsung-group brand. The substitution did not achieve its purpose, and this was not noticed until November 10, 2026. The registries of this study are those of the English t₄ wave, with Denon included and disclosed as in the t₄ pre-registration; every result is also reported without the Denon unit and without the headphones category (DEVIATIONS Entry 0). One of the three languages is Korean, and South Korea is Samsung Electronics' home market: answers in Korean, as in any language, may name Samsung-group brands that are not registry units; such names are never coded or scored, because coding counts only the 112 registry units. Acquisition, coding and scoring are fully automated against the locked registries, and this pre-registration is locked and deposited before the first call. Samsung Electronics had no role in the design, conduct, analysis or reporting of this work.

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
- **r2** (2026-11-10/11, this draft): languages changed to Spanish, Korean and Chinese (below).
- **Before the lock:** native checks or the per-language fallback; independent back-translations for unchecked languages; prices and model IDs re-read; cost re-based on t₄'s recorded usage and `BRAND_EXTRAS` set by the §5.2 rule; P1 and P2 on t₄'s coded tables; alias parity checks (MAC 魅可, Fernet Branca); the country column (§2.9 item 5); lock manifest. **Lock:** 24 hours after the pre-registrant receives the final text unless he objects; then manifest, commit, tag `v0.62-prereg-r1`, push, OSF deposit; only then `--collect`.

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
