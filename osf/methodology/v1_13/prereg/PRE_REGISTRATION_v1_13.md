# AIAS v1.13 — Grounding, Paper A: instrument, cross-category baseline, separability gate

AIAS™ Measurement Program — Third System™. Pre-registration **DRAFT r1** (2026-11-10). **Not locked, not sent, not tagged.**

## 0. Status, scope and lineage

| Field | Value |
|---|---|
| PHASE_ID | v1.13 |
| PHASE_TYPE | Two parts with different lock rules. **Part I [RE-ANALYSIS: t4]** = citation instrument on the stored S1 (search-on) answers of the t4 wave (v0.42): no model calls, no spend; locks on Pablo's OK, before any t4 S1 search record is read for Grounding. **Part II [NEW WEB DATA: audit]** = structured-data audit of brand websites and public knowledge-graph records: no paid models, no spend; locked, tagged and OSF-anchored, then **not run until 24 hours after Pablo receives the locked text** (programme rule, Nov 9, 2026). Every section below carries one of the two tags. |
| Status | DRAFT r1 by the runner's sub-agent on branch `v1.13` (from `aias-2.0`, commit `894ccee`). Not reviewed by Pablo. |
| Locks on | Part I: content lock → commit → tag `v1.13-prereg-r1` → OSF deposit of `osf/methodology/v1_13/prereg/` + `anchor/git_anchor_v1_13.json` (tag object, commit, tree, SHA-256 of every locked file, including `source_classes_v1_13.md` and `registries/brand_domains_v1_13.csv`) → anchors verified → only then `score_v1_13.py --stage C1`. Part II: the same sequence under tag `v1.13-audit-r1`, then the 24-hour wait, then `audit_v1_13.py --collect`. |
| Locked inputs | Presence: protocol v1.6 (P = 100·(C_P/6 + 2·π̂)/3). Consistency: v1.8 φ, scaled by v1.9 to C_φ = 100(1 − φ/7.2), rated only with ≥ 6 total mentions (C\*). At t4 both are computed with v0.42's certified coder and definitions (§2.2), not re-weighted. v0.42 raw file `osf/v42/data/t4_raw.jsonl` (SHA-256 recorded in the anchor before the first read). |
| Pilot (declared, no verdict) | v0.39 coffee roasters, search-on arm: 90 answers, 67 with sources (held study: OSF yes, website never). Used only to dry-run the parser, check the Google redirect-title rule (U5 in `source_classes_v1_13.md`) and measure the share of domains the frozen class list leaves as `other`. Pilot numbers are reported as pilot. |
| Feeds forward | Grounding Paper B (only after PASS, or MARGINAL with Pablo's recorded decision); the component calibration after Ranking (v1.10), Sentiment (v1.11), Coverage (v1.12). |

**Lineage.** AIAS 2.0 (published 2026-11-10; tag `aias-2-0-paper-locked`) showed Consistency separable from Presence: within-category |ρ(C\*, P)| = 0.073 (t1), 0.082 (t2), 0.189 (t3). Ranking (v1.10), Sentiment (v1.11) and Coverage (v1.12) Paper A pre-registrations apply the same gate. The archive inventory (Nov 10) found only 90 archived search-on answers (v0.39), too thin for a cross-category baseline, so Grounding rests on t4's S1 arm (v0.42, collected Nov 11–13), v0.40's S1 arm (Nov 17–21, Paper B) and the structured-data audit. Plan of record: Pablo, 2026-11-09.

**Construct.** Grounding = what an AI answer about a category rests on: which sources it cites when search is on (**cited grounding**, Part I), and whether the brand's own structured data is in place for those systems to find (**structured grounding**, Part II). Whether a brand is named is Presence; how evenly models name it is Consistency; where it sits in a list is Ranking. Grounding must add information none of them carries, or it is not a component.

## 1. Research questions

- **RQ1 (instrument) [RE-ANALYSIS: t4].** Can a fixed, pre-declared rule turn each S1 answer's stored citation record into classified sources (brand-owned, retailer, review/editorial, news, Wikipedia/reference, forum/UGC, other) at coverage high enough to score brands in all five omnibus categories?
- **RQ2 (baseline) [RE-ANALYSIS: t4].** What do category answers on the newest models rest on, per category and per model?
- **RQ3 (gate: separability) [RE-ANALYSIS: t4].** Within category, is the Grounding score separable from P and C\* by the programme's bands (|ρ| ≤ 0.30 CONFIRMED, ≥ 0.50 FALSIFIED, between MARGINAL)?
- **RQ4 (gate: reliability) [RE-ANALYSIS: t4].** Does the Grounding score hold across t4's three S1 runs? A score that is separable only because it is noise does not pass.
- **RQ5 (structured-data gap) [NEW WEB DATA: audit + t4].** Do brands with richer structured data have higher own-domain citation shares?

## 2. Data and definitions

### 2.1 Answers [RE-ANALYSIS: t4]

- **Source file.** `osf/v42/data/t4_raw.jsonl` (v0.42 §4.4), one JSON line per call. Fields used (confirmed in `osf/v42/scripts/acquire_v0_42.py`, `send_call`, branch `v0.42` @ `4e86dd9`): `call_id`, `substrate` (`v19`…`v23`), `phase` (`A`/`B`), `probe_id`, `brand_id`, `frame_id`, `model_requested`, `provider`, `served_model`, `condition` (`S0`/`S1`), `run` (1–3), `text`, `status`, `finish_reason`, `search`. For S1, `search` = `{n_searches, queries, sources, citations, errors}`; `citations` and `sources` are lists of `{url, title}` (Anthropic sources add `page_age`; OpenAI pages opened by a non-search action add `action`). S0 records have `search = null`.
- **What the fields hold, per provider (from the acquisition code).** Anthropic: `citations` = URLs attached to text blocks, `sources` = every result of every `web_search_tool_result`. OpenAI: `citations` = `url_citation` annotations of the message, `sources` = `web_search_call.action.sources` (plus opened pages). Google: `sources` = `grounding_metadata.grounding_chunks[].web` (`uri`, `title`), `citations` = the chunks referenced by `grounding_supports` (**one entry per support, so duplicates are expected**; de-duplicated by rule U6).
- **Answered S1 answer.** `condition == "S1"`, `status == "ok"`, non-empty `text`, accepted served ID (v0.42 C9).
- **Category answers** = Phase B (6 questions per substrate). **Brand answers** = Phase A (one question per brand; v0.19–v0.22 yes/no, v0.23 open).
- **Panels.** Primary **N3** = Claude Fable 5.2, GPT-6 Astra, Gemini 4 Argon (one model per provider, v0.42's primary panel; avoids double-weighting one provider's search tool). Sensitivities: **A4** (all four models) and **C3** (Claude Opus 5.5, GPT-6 Astra, Gemini 4 Argon). Per substrate on N3: 6 × 3 × 3 = 54 category answers; 270 in all.
- **Names the brand.** v0.42's certified coder (`osf/v42/scripts/code_t4_v0_42.py`), visible text with URLs removed (v0.42 §5.1). A brand cited only through a URL is not "named".

### 2.2 Presence and Consistency at t4 [RE-ANALYSIS: t4]

- π̂_{b,N3,c} and φ_{b,N3,c} for condition c ∈ {S0, S1}: v0.42 §2.1 definitions, computed by `score_v0_42.py` (its outputs are read, not recomputed).
- **P at t4.** v1.6 formula with C_P/6 read as the recognition share: C_P/6 := share of N3 model-runs whose Phase A answer codes b as recognized (v0.42 coder). P_c = 100·(C_P,c/6 + 2·π̂_c)/3.
- **C\* at t4.** C_φ = 100(1 − φ_{b,N3,c}/7.2), rated iff b has ≥ 6 total Phase B mentions on N3 in condition c (v1.9 floor).
- The AIAS 2.0 locked P and C\* at t3 (`osf/aias_2_0/aias_2_0_profiles.csv`, legacy panel) enter only sensitivity S7.

### 2.3 Source classification [RE-ANALYSIS: t4]

The full rule is `source_classes_v1_13.md` (frozen at lock, SHA-256 in the anchor). In brief: URL → normalised host → registrable domain (U1–U6; Google redirect URLs take the domain from `title`, never by following the redirect) → class by fixed precedence: **brand-owned** (domain ∈ D_b of any registry brand of the substrate; for a given brand, *own* = D_b) → Wikipedia/reference → forum/UGC → news → review/editorial → retailer → host-pattern rules → `other`; unparseable → `unresolved`. The domain lists were written before any t4 answer exists (t4 collects Nov 11–13) and before v0.42's own S1 descriptive (its §2.7 item 5, top domains per model) is computed. They are not extended after any t4 S1 record is read; additions are exploratory and labelled.

**Brand domains D_b.** `osf/methodology/v1_13/registries/brand_domains_v1_13.csv` (TODO before lock): one row per brand unit (112) with the canonical official domain and any declared aliases (US-market domain, e.g. a `…usa.com` variant), each with a source note. Built by the declared rule in `website_audit_protocol_v1_13.md` §2 **without** fetching study pages; frozen before the first t4 S1 read. Part II later verifies D_b (sensitivity S6); the primary G\* always uses the frozen D_b, so Part I verdicts never wait for Part II.

### 2.4 Per-brand statistics [RE-ANALYSIS: t4]

Over N3 category answers of b's substrate (all three runs pooled):

| Symbol | Definition |
|---|---|
| m_b | answered S1 category answers naming b |
| g_b | of those, answers with ≥ 1 citation that resolves to a class other than `unresolved` ("grounded answers naming b") |
| o_b | of those, answers whose citation domains include a domain in D_b |
| **G_b** | o_b / g_b, the **own-domain citation share** |
| **G\*** | 100·G_b, **rated iff g_b ≥ 6** (the C\* floor); otherwise NOT RATED |
| mix_b | for each class k, the mean over b's grounded answers of the share of the answer's distinct cited domains in class k (each answer weighs 1) |
| d_b | mean number of distinct cited registrable domains per grounded answer naming b |
| G_A | own-domain share over grounded Phase A answers about b on A4 (max 12), rated iff ≥ 6 grounded answers (secondary, descriptive) |

Primary Grounding score = **G\***. mix_b, d_b and G_A are reported for every rated brand; no verdict rests on them.

### 2.5 Structured-data richness [NEW WEB DATA: audit]

Defined in `website_audit_protocol_v1_13.md` §5, fixed now: **SDRI** = 100 × (sum of 8 binary indicators)/8: (1) schema.org Organization or a subtype on the home page; (2) Brand on any audited page; (3) Product or a subtype on any audited page; (4) ≥ 1 `sameAs` on an Organization/Brand node; (5) a `sameAs` to Wikidata or Wikipedia; (6) a Wikidata item exists (adjudicated QID); (7) that item's official website (P856) has its registrable domain in D_b; (8) an English Wikipedia article is linked from that item. Sub-indices SDRI_site = (1)–(5), SDRI_kg = (6)–(8). Equal weights; no re-weighting after data.

## 3. Hypotheses, tests and verdict rules

Conventions (as v1.10). ρ_w = pooled within-category Spearman: Pearson correlation of within-substrate average ranks; only substrates with ≥ 5 units in the comparison enter. Values compared unrounded. Permutation: the first variable permuted within substrate, 10,000 draws, p = (hits + 1)/(N + 1); a draw is a hit if |ρ_perm| ≥ |ρ_obs| − 10⁻¹² (two-sided) or ρ_perm ≥ ρ_obs − 10⁻¹² (one-sided). Bootstrap: units resampled within substrate, 2,000 draws, 90% percentile CI (reported, not a verdict input). Seeds 113001–113010 as listed.

| ID | Tag | Role | Statistic | CONFIRMED | FALSIFIED | MARGINAL | UNDETERMINED |
|---|---|---|---|---|---|---|---|
| **H1_Sep_Presence** | t4 | PRIMARY (gate) | ρ_w(G\*, P_S1) and ρ_w(G\*, P_S0), units with G\* rated; seed 113001, two-sided p reported | both \|ρ\| ≤ 0.30 | either \|ρ\| ≥ 0.50 | otherwise | < 30 rated units, or MQ5 fails |
| **H2_Sep_Consistency** | t4 | PRIMARY (gate) | ρ_w(G\*, C\*_S1) and ρ_w(G\*, C\*_S0), units with both rated; seed 113002 | both \|ρ\| ≤ 0.30 | either \|ρ\| ≥ 0.50 | otherwise | < 30 units, or MQ5 fails |
| **H3_Run_Reliability** | t4 | PRIMARY (gate: reliability leg) | G\*_r per run r (rated iff g_{b,r} ≥ 3); rel1 = mean of ρ_w over the 3 run pairs (units rated in both runs of the pair); rel3 = 3·rel1/(1 + 2·rel1); one-sided permutation (second run of each pair permuted within substrate), seed 113003 | rel3 ≥ 0.50 AND p < 0.05 | rel3 < 0.30 | otherwise | < 30 units in 2 or more of the 3 pairs |
| H4_Sep_Ranking | t4 | SECONDARY (conditional) | ρ_w(G\*, R\*) with R\* from locked v1.10 on the same t4 N3 S1 answers; seed 113004 | \|ρ\| ≤ 0.30 | \|ρ\| ≥ 0.50 | otherwise | NOT RUN if v1.10 is not locked with a t4 R\* by Stage C1; < 30 units |
| H5_Sep_Sentiment | t4 | SECONDARY (conditional) | as H4 with the locked v1.11 score; seed 113005 | as H4 | as H4 | as H4 | as H4 (v1.11) |
| H6_Sep_Coverage | t4 | SECONDARY (conditional) | as H4 with the locked v1.12 score on the same brands; seed 113006 | as H4 | as H4 | as H4 | as H4 (v1.12; its new question set may not exist for t4 brands) |
| H7_Struct_Gap | audit + t4 | SECONDARY (or hand-off) | ρ_w(SDRI, G\*), units with both; one-sided; seed 113007. Reported beside it: ρ_w(SDRI, P_S0) and the partial ρ_w(SDRI, G\* \| P_S0) (within-substrate rank residuals) | ρ ≥ 0.30 AND p < 0.05 | ρ ≤ 0.10 | otherwise | < 30 units; or Part II not collected before Stage C2 (then handed to Paper B, §8) |

Seeds 113008 (bootstrap), 113009 (S-sensitivities), 113010 (reserved) are recorded now.

**Gate rule.** **PASS** iff H1, H2 and H3 are all CONFIRMED — downgraded to MARGINAL if any run secondary separability leg (H4–H6) is FALSIFIED. **FAIL** if H1, H2 or H3 is FALSIFIED. **UNDETERMINED** if H1 or H2 is UNDETERMINED (published as such; the instrument goes back to design). Otherwise **MARGINAL**: Pablo decides (recorded) whether Paper B proceeds. H7 never changes the gate.

**Rationale.** G\* is a share conditional on being named and on the answer citing anything, so it is not mechanically tied to how often a brand is named; g_b is (MQ6 checks this). Separability is required against P in both conditions because G\* is computed from S1 answers whose own Presence (P_S1) is the most direct rival, while P_S0 is Presence as the programme measures it at t4. A score that is mostly zeros could pass the separability bands by having no variance; MQ5 makes that UNDETERMINED instead of CONFIRMED.

## 4. Manipulation and quality checks [RE-ANALYSIS: t4]

| ID | Check | Rule |
|---|---|---|
| MQ1 | Parse | the parser completes on 100% of answered S1 records (an exception halts) |
| MQ2 | Search use | share of N3 category answers with ≥ 1 citation, per model; < 0.25 flags the model "search rarely used" in every result (v0.42 MC_Search bar); a model below 0.10 is dropped from G\* (reported both ways) |
| MQ3 | Class coverage | share of distinct (answer, domain) citation pairs classed `other` or `unresolved`: > 0.40 flagged; > 0.60 labels the source-mix descriptives "low coverage" (no verdict uses the mix) |
| MQ4 | Google redirects | share of Gemini citations whose domain is taken from `title` (U5) and share left `unresolved`; > 0.20 unresolved → Gemini dropped from G\* for the primary (N3 becomes two models; sensitivity S5 keeps it) |
| MQ5 | Degeneracy | gate UNDETERMINED if > 0.80 of rated brands have G\* = 0, or within-substrate SD of G\* is 0 in ≥ 3 of the 5 substrates |
| MQ6 | Mechanical coupling | ρ_w(g_b, π̂_S1) and ρ_w(G\*, g_b) reported; \|ρ_w(G\*, g_b)\| ≥ 0.50 flagged (the share is tracking the count) |
| MQ7 | Frozen lists | SHA-256 of `source_classes_v1_13.md` and `brand_domains_v1_13.csv` at Stage C1 equal the anchored values; a mismatch halts |
| MQ8 | Citations vs sources | share of cited URLs that also appear in `sources` (per provider); reported only |

## 5. Stages

1. **Stage P (pilot, before lock, declared).** Run the parser and classifier on v0.39's 90 search-on answers; report MQ1, MQ3, MQ4 and the top 20 domains as pilot numbers. Pilot results may change a parsing rule before the lock (logged); they may not change a threshold.
2. **Stage C1 (after Part I lock; t4 data).** Verify anchors and MQ7 → parse t4 S1 → classify → per-brand statistics → MQ1–MQ6, MQ8 → H1–H6 → baseline → sensitivities. Verdicts to `v1_13_verdicts.json`.
3. **Stage A (after Part II lock + 24 h).** Audit per `website_audit_protocol_v1_13.md`; writes `audit/v1_13_audit_records.jsonl` and `v1_13_sdri.csv`.
4. **Stage C2.** H7 and the SDRI descriptives; appended to the verdict file with their own timestamp.

## 6. Baseline descriptives (no verdicts) [RE-ANALYSIS: t4]

Per substrate and per model (N3 and A4): share of category answers with ≥ 1 citation; citations and distinct domains per answer; source-type mix; share of answers citing any registry brand's own domain; share citing Wikipedia/reference; the 20 most-cited domains; the distribution of G\* (median, IQR, share zero); g_b and rating coverage; the same for brand answers (Phase A) with G_A; Phase A v0.19–v0.22 (yes/no) reported apart from v0.23 (open).

## 7. Sensitivities (verdict changes listed next to the verdict)

S1 denominator m_b instead of g_b. S2 retrieved set (`search.sources`) instead of `citations`. S3 panels A4 and C3. S4 rating floors 3 and 10. S5 Gemini kept/dropped against the MQ4 decision. S6 D_b as verified by Part II (aliases from the audit's final redirect domains added). S7 P and C\* from AIAS 2.0 t3 (legacy panel; cross-panel, descriptive). S8 leave-one-substrate-out ranges for H1–H3. S9 citation set extended with URLs written in the answer text (Markdown links and bare `https?://` addresses).

## 8. What Paper B inherits (not pre-registered here)

Pre-registered separately, only after PASS (or MARGINAL with Pablo's recorded decision): the locked parser, `source_classes_v1_13.md`, D_b, `score_v1_13.py` and tests; per-answer source tables (SHA-256 pinned); **source-coverage stability over waves** (t4 → v0.40 S1 arm, Nov 17–21, US airlines and retail banks → t5 → t6, each re-classified with the frozen lists); **phantom-brand grounding** (what answers cite when they name a registry phantom brand; registry phantom flags); **identity load** (OMNI cultural vs category frames); **typology** (G\* × P × C\* × R\* profiles); H7 if Part II was not collected in time; re-audits of structured data at t5/t6; v0.40's brands added to the audit if v0.40's pre-registration declares its citation record.

## 9. Limitations

S1 answers depend on the web on the day and on each provider's search back-end; they are reproducible only as recorded. Citation records differ by provider (Google's are redirect URLs with a domain title), so model differences mix model and tool. Own-domain citation needs the brand's site to be indexed and open to crawlers; a low G\* can reflect robots policies as much as model behaviour. D_b is a declared list and can miss regional or campaign domains (S6). Five categories, one market and language (US English). Static HTML only in the audit: structured data injected by JavaScript is missed (protocol §7).

## 10. Deviations policy

`osf/methodology/v1_13/anchor/DEVIATIONS.md` opens with **Entry 0 (ex ante)**: COI carry-forward (§11) and the anchor sequence of §0. After the lock: every change gets an entry (id, date, ex ante/ex post, what, why, effect on inference); a frozen-input hash mismatch halts the run; a parser fix is allowed only to restore a rule as written; thresholds, floors, seeds, class lists and the gate rule do not change; a failed gate is published with the same prominence as a pass.

## 11. Declarations

**Conflict of interest.** The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. This study performs no new brand selection: it re-uses the five omnibus registries (v0.19–v0.23) and carries forward each registry's source-phase COI handling unchanged. Part II fetches public pages of the registry brands' own websites; it contacts no brand and buys nothing. Two items of record apply, quoted verbatim from their source records:

- *v0.19 audiophile headphones* — `osf/v19/PRE_REGISTRATION_v0_19.md` §2.3: "**AKG removed from Cell A short-list; Denon substituted.** AKG is Samsung-owned since 2016. The author's COI declaration names Samsung; including AKG would invite the kind of reviewer suspicion AIAS™ 1.0 does not need to absorb. Denon carries comparable heritage stature (founded 1910; AH-D7000 → D9200 audiophile line) and removes the question. Decision rationale recorded here for audit trail." Declaration of the same file: "Note: AKG (Samsung-owned since 2016) was considered for Cell A inclusion on substantive heritage-audiophile grounds and substituted with Denon to avoid any appearance of conflict; substitution rationale recorded in §2.3 above." (Also recorded in v0.19 DEVIATIONS Entry 1.)
- *v0.22 automotive* — `papers/v0_22/v0_22_ssrn_paper_draft.md`, Declarations §COI: "Samsung subsidiaries hold tier-2/3 component supply relationships with several brands in the v0.22 registry: Harman International (audio systems) supplies Mercedes-Benz, BMW, and other premium automotive OEMs; Samsung SDI (battery cells) supplies BMW (i-series), Volkswagen Group brands including Bentley and Porsche (Stellantis-adjacent platforms), and others; Samsung Display (infotainment) supplies Mercedes-Benz and BMW. Tesla and Polestar also have tangential Samsung-component exposure at the parts level. These are non-competitive supply relationships; Samsung Electronics America does not produce or market passenger car brands and has no brand-level competitive overlap with any v0.22 registry entry. The COI was screened and documented in DEVIATIONS Entry 0 (Part B) of the pre-registration module; no operational restriction on registry composition was imposed."

Samsung Electronics had no role in the design, conduct, analysis or reporting of this work. **TODO before lock (runner):** confirm the current ownership of every v0.19 registry brand (in particular Denon) against a dated public source and record the result in DEVIATIONS Entry 0; the quoted records above stay verbatim either way.

**Funding.** Self-funded. **Ethics.** No human subjects; Part II reads public web pages under the protocol's robots and rate rules. **Use of AI tools.** The author used Anthropic's Claude to assist with analysis code, drafting and editing of text, and figure production. The study design, pre-registered hypotheses and decision rules, and all interpretations are the author's; the author reviewed all content and takes full responsibility for it.

## 12. Open questions to settle before the lock

1. D_b build: offline declared list now (this draft) vs Wikidata P856 lookups, which are web data under the 24-hour rule?
2. Primary citation field `citations` (what the text cites) vs `sources` (what was retrieved)?
3. Primary panel N3 vs A4; Gemini redirect titles (MQ4) to be checked on the v0.39 pilot.
4. Floors: G\* rated at g_b ≥ 6, per-run 3, unit floor 30 — feasible with 54 category answers per substrate? If not, lower to 5 / 2 / 25 now, not later.
5. H4–H6 need Ranking/Sentiment/Coverage scores on the t4 answers; v1.10–v1.12 define them on other sets. Run cross-panel or leave NOT RUN?
6. v0.42 §2.7 item 5 (top domains per model) must not be viewed before the class lists freeze.
