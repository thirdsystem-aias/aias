# AIAS v1.13 — Grounding, Paper A: instrument, cross-category baseline, separability gate

AIAS™ Measurement Program — Third System™. Pre-registration **DRAFT r1, sent to Pablo for the 24-hour review (2026-11-10).** Not locked, not tagged. Nothing collected, no website fetched, nothing spent.

Files: this document; `source_classes_v1_13.md` (source-classification rule; its fenced lists are the machine copy); `website_audit_protocol_v1_13.md` (Part II); `dry_run_audit_v1_13.txt` (Part II dry run on synthetic fixtures). In `osf/methodology/v1_13/registries/`: `brand_domains_v1_13.csv` (D_b, pinned in §2.3) and `wikidata_types_v1_13.csv` (words of the Part II QID rule). In `osf/methodology/v1_13/scripts/`: `score_v1_13.py` (Part I scorer core) with `tests/test_score_v1_13.py`; `audit_v1_13.py` (Part II audit) with `tests/test_audit_v1_13.py` and the synthetic fixtures `fixtures/audit/`.

## 0. Status, scope and lineage

| Field | Value |
|---|---|
| PHASE_ID | v1.13 |
| PHASE_TYPE | Two parts with different lock rules. **Part I [RE-ANALYSIS: t4]** = source instrument on the stored S1 (search-on) answers of the t4 wave (v0.42): no model calls, no spend; locks on Pablo's OK, before any t4 S1 search record is read for Grounding. **Part II [NEW WEB DATA: audit]** = structured-data audit of the registry brands' own websites and public Wikidata records: no paid model, no spend; locked, tagged and OSF-anchored, then **not run until 24 hours after Pablo receives the locked text** (programme rule, Nov 9, 2026). Every section below carries one of the two tags. |
| Status | DRAFT r1 on branch `v1.13` (from `aias-2.0` @ `894ccee`): written by the runner's sub-agent (commit `062b94a`), completed for sending with the runner's decisions of 2026-11-10 (§13) and sent to Pablo for the 24-hour review on 2026-11-10. |
| Locks on | Part I: content lock → `prereg/LOCK_MANIFEST_v1_13.sha256` → commit → tag `v1.13-prereg-r1` → push → `anchor/git_anchor_v1_13.json` (tag object, commit, tree, SHA-256 of every locked file, including `source_classes_v1_13.md` and `registries/brand_domains_v1_13.csv`, and the activation record of H4–H6, §3) → OSF deposit of `prereg/`, `registries/` and `anchor/`, SHA-256 verified there → only then `score_v1_13.py --stage C1` (it refuses without the tag, the anchor, matching list hashes and a D_b list with no UNRESOLVED row). Part II: the same sequence under tag `v1.13-audit-r1` with `anchor/audit_anchor_v1_13.json`, then the 24-hour wait recorded in `anchor/audit_receipt_v1_13.json`, then `audit_v1_13.py --collect` (it refuses otherwise; protocol §8). |
| Locked inputs | Presence: protocol v1.6 (P = 100·(C_P/6 + 2·π̂)/3). Consistency: v1.8 φ, scaled by v1.9 to C_φ = 100(1 − φ/7.2), rated only with ≥ 6 total mentions (C\*). At t4 both come from v0.42's certified coder and scorer (§2.2), not re-weighted: `code_t4_v0_42.py` (git blob `2d36735d512cf9e13b74010ba5a7f655fc7de0bc`, SHA-256 `d0e4e685b5e3e1d983190726b5e88ef2b841b4589d5802ba67b86e31e4148220`) and `score_v0_42.py` (git blob `884b02cd64438ec031f3967c6b2120c25bc286a3`, SHA-256 `3a54037b109e84d801e38073f36b175e97717c73d88a9fd381e6956103df2f7b`), branch `v0.42` @ `4e86dd9`; both are re-checked against tag `v0.42-prereg-r1` at the v1.13 lock and any difference is logged before it. v0.42 raw file `osf/v42/data/t4_raw.jsonl` (SHA-256 recorded in the anchor before the first read). |
| Pilot | **None.** The instrument was specified without looking at any search-on answer: t4 has none yet, and v0.39's search-on answers (a held study; 90 answers, 67 with sources, by the archive inventory of Nov 10) are not used for anything. The only search-on facts used are the field definitions in v0.42's acquisition code and the per-call counts in v0.42's feasibility record (neutral prompts, no study probe) (§2.1). |
| Feeds forward | Grounding Paper B (only after PASS, or MARGINAL with Pablo's recorded decision); the component calibration after Ranking (v1.10), Sentiment (v1.11), Coverage (v1.12). |

**Lineage.** AIAS 2.0 (published 2026-11-10; tag `aias-2-0-paper-locked`) showed Consistency separable from Presence: within-category |ρ(C\*, P)| = 0.073 (t1), 0.082 (t2), 0.189 (t3) (as published, under the uncentred pooled-rank convention that §3 replaces). Ranking (v1.10, locked), Sentiment (v1.11) and Coverage (v1.12) Paper A pre-registrations apply the same gate. The archive inventory (Nov 10) found only 90 archived search-on answers (v0.39, a held study), too thin for a cross-category baseline, so Grounding rests on t4's S1 arm (v0.42, collecting Nov 11–13), v0.40's S1 arm (Nov 17–21, Paper B) and the structured-data audit. Plan of record: Pablo, 2026-11-09.

**Construct.** Grounding = what an AI answer about a category rests on when search is on: which sources its search brings back (**retrieved grounding**, Part I: the search record's `sources`; the subset the answer cites, `citations`, is sensitivity S2), and whether the brand's own structured data is in place for those systems to find (**structured grounding**, Part II). Whether a brand is named is Presence; how evenly models name it is Consistency; where it sits in a list is Ranking. Grounding must add information none of them carries, or it is not a component.

## 1. Research questions

- **RQ1 (instrument) [RE-ANALYSIS: t4].** Can a fixed, pre-declared rule turn each S1 answer's stored search record into classified sources (brand-owned, retailer, review/editorial, news, Wikipedia/reference, forum/UGC, other) at coverage high enough to score brands in all five omnibus categories?
- **RQ2 (baseline) [RE-ANALYSIS: t4].** What do category answers on the newest models rest on, per category and per model?
- **RQ3 (gate: separability) [RE-ANALYSIS: t4].** Within category, is the Grounding score separable from P and C\* by the programme's bands (|ρ| ≤ 0.30 CONFIRMED, ≥ 0.50 FALSIFIED, between MARGINAL)?
- **RQ4 (gate: reliability) [RE-ANALYSIS: t4].** Does the Grounding score hold across t4's three S1 runs? A score that is separable only because it is noise does not pass.
- **RQ5 (structured-data gap) [NEW WEB DATA: audit + t4].** Do brands with richer structured data have higher own-domain source shares?

## 2. Data and definitions

### 2.1 Answers [RE-ANALYSIS: t4]

- **Source file.** `osf/v42/data/t4_raw.jsonl` (v0.42 §4.4), one JSON line per call. Fields used (confirmed in `osf/v42/scripts/acquire_v0_42.py`, `send_call`, branch `v0.42` @ `4e86dd9`): `call_id`, `substrate` (`v19`…`v23`), `phase` (`A`/`B`), `probe_id`, `brand_id`, `frame_id`, `model_requested`, `provider`, `served_model`, `condition` (`S0`/`S1`), `run` (1–3), `text`, `status`, `error`, `finish_reason`, `search`. For S1, `search` = `{n_searches, queries, sources, citations, errors}`; `sources` and `citations` are lists of `{url, title}` (Anthropic sources add `page_age`; OpenAI pages opened by a non-search action add `action`). S0 records have `search = null`.
- **What the fields hold, per provider (from the acquisition code).** Anthropic: `sources` = every result of every `web_search_tool_result`, `citations` = URLs attached to text blocks. OpenAI: `sources` = `web_search_call.action.sources` plus pages opened by the search tool, `citations` = `url_citation` annotations of the message. Google: `sources` = `grounding_metadata.grounding_chunks[].web` (`uri`, `title`), `citations` = the chunks referenced by `grounding_supports` (one entry per support, so duplicates are expected; de-duplicated by U6).
- **Primary evidence field: `search.sources`, for every provider (runner decision 2).** The rule is the field that t4 records for all three N3 providers. v0.42's feasibility record (`osf/v42/prereg/feasibility_v0_42.json`, run 2026-11-10 05:13 UTC, neutral prompts only) counts sources for each S1 call: Claude Fable 5.2 28 and 9, GPT-6 Astra 1 and 13, Gemini 4 Argon 0 and 6, so `sources` was populated for each N3 model in at least one call; the record holds no citation count, so it does not show `citations` populated for every provider. `citations` is therefore sensitivity S2. One rule for all providers; Gemini's redirect URLs are resolved by their title domain (U5) in both fields.
- **Answered S1 answer.** `condition == "S1"`, `status == "ok"`, non-empty `text`, no error, accepted served ID (v0.42 C9); one record per `call_id` (the last answered attempt, else the last attempt).
- **Category answers** = Phase B (6 questions per substrate). **Brand answers** = Phase A (one question per brand; v0.19–v0.22 yes/no, v0.23 open).
- **Panels.** Primary **N3** = Claude Fable 5.2, GPT-6 Astra, Gemini 4 Argon (one model per provider, v0.42's primary panel; avoids double-weighting one provider's search tool). Sensitivities: **A4** (all four models) and **C3** (Claude Opus 5.5, GPT-6 Astra, Gemini 4 Argon). Per substrate on N3: 6 × 3 × 3 = 54 category answers; 270 in all.
- **Names the brand.** v0.42's certified coder (`code_t4_v0_42.py`, pinned above), applied to the visible text with URLs removed (v0.42 §5.1); its Phase B table row (`mentioned` = 1) is matched to the unit through the `coder_key` column of `brand_domains_v1_13.csv`. A brand reached only through a URL is not "named".

### 2.2 Presence and Consistency at t4 [RE-ANALYSIS: t4]

- π̂_{b,N3,c} and φ_{b,N3,c} for condition c ∈ {S0, S1}: v0.42 §2.1 definitions, computed by `score_v0_42.py` (its brand-table columns `pi_N3_<c>` and `phi_N3_<c>` are read, not recomputed).
- **P at t4.** v1.6 formula with C_P/6 read as the recognition share: C_P/6 := share of answered N3 model-runs whose Phase A answer codes b as recognized (v0.42 coder). P_c = 100·(C_P,c/6 + 2·π̂_c)/3.
- **C\* at t4.** C_φ = 100(1 − φ_{b,N3,c}/7.2), rated iff φ is defined and b has ≥ 6 total Phase B mentions on N3 in condition c (v1.9 floor). ρ_w is invariant to the divisor.
- The AIAS 2.0 locked P and C\* at t3 (`osf/aias_2_0/aias_2_0_profiles.csv`, legacy panel) enter only sensitivity S7.

### 2.3 Source classification [RE-ANALYSIS: t4]

The full rule is `source_classes_v1_13.md` (frozen at lock, SHA-256 in the anchor). In brief: URL → normalised host → registrable domain (U1–U6; Google redirect URLs take the domain from `title`, never by following the redirect) → class by fixed precedence: **brand-owned** (domain ∈ D_b of any registry brand of the substrate; for a given brand, *own* = D_b) → Wikipedia/reference → forum/UGC → news → review/editorial → retailer → host-pattern rules → `other`; unparseable → `unresolved`. The domain lists were written before any t4 answer exists (t4 collects Nov 11–13) and before v0.42's own S1 descriptive (its §2.7 item 5, top domains per model) is computed; that descriptive stays unseen until the lists freeze at the Part I lock (runner decision 6). The lists are not extended after any t4 S1 record is read; additions are exploratory and labelled.

**Brand domains D_b (runner decision 1).** `osf/methodology/v1_13/registries/brand_domains_v1_13.csv` is a frozen offline list: one row per brand unit (112), keyed by t4's `substrate` and `brand_id`, with the registry name and the v0.42 coder's key. Each domain is the registrable domain (U2/U4) of an official-site URL recorded in a committed repository file, given with its source (path, line, git blob, URL); nothing is looked up at analysis time and no brand page was fetched to build it. A unit with no such record is UNRESOLVED; ambiguous units are listed with the reason, not guessed. The runner decides every UNRESOLVED row before sending (a domain with its source, or NONE = no own domain), and each decision is logged in §12.

- **Status as built (2026-11-10):** 2 RESOLVED, 110 UNRESOLVED. RESOLVED: Cetaphil (v20 C.6) `cetaphil.com` and Augustinus Bader (v20 B.7) `augustinusbader.com`, both from `osf/v13/registries/brand_age_sources_v0.13.csv` (lines 49 and 64, git blob `f0e6787a1f6a9949815615be0dd6210aac99c7b9`), whose source URLs for those two brands are on the brands' own sites. For the other 110 units the repository holds no official-site record (git grep of all local branches, 2026-11-10; URLs that occur only inside model answers are not records and were not used).
- **Ambiguities listed (18 rows):** one brand in two units (Rare Beauty, v20 B.1 and v21 B.1); sister lines of one brand family (Fenty Skin, Fenty Beauty); beauty lines of fashion houses (Dior Beauty, Chanel Beauty, Tom Ford Beauty, Giorgio Armani Beauty); brand vs parent-company domain (Estée Lauder, L'Oréal Paris, The Ordinary); a former brand name (Dan Clark Audio, "Formerly MrSpeakers"); company status (Fisker); the five v0.22 cell D "Defunct" brands (Pontiac, Oldsmobile, Plymouth, Mercury, Saturn), for which no own site is expected. Denon's row carries the COI note of §11.
- **Pin.** SHA-256 of the file as built: `e45aa22c82879d234b33fe06220f9b8de8ea571c5e6bc1d1a54c3c9d72b9f98e`. Any change (the runner's decisions included) changes the pin; the Part I lock pins the final file in the anchor, and Stage C1 refuses while any row is UNRESOLVED (MQ7).
- A unit with status NONE has no own domain: its G\* is NOT RATED (it cannot be retrieved from a site it does not have), it adds no domain to the brand-owned class and it is reported apart. Part II later verifies D_b (sensitivity S6); the primary G\* always uses the frozen D_b, so Part I verdicts never wait for Part II.

### 2.4 Per-brand statistics [RE-ANALYSIS: t4]

Over N3 category answers of b's substrate (all three runs pooled), with the primary field `sources`:

| Symbol | Definition |
|---|---|
| m_b | answered S1 category answers naming b |
| g_b | of those, answers with ≥ 1 source that resolves to a class other than `unresolved` ("grounded answers naming b") |
| o_b | of those, answers whose resolved source domains include a domain in D_b |
| **G_b** | o_b / g_b, the **own-domain source share** |
| **G\*** | 100·G_b, **rated iff g_b ≥ 6** (the C\* floor) and b has a D_b; otherwise NOT RATED |
| mix_b | for each class k, the mean over b's grounded answers of the share of the answer's distinct resolved source domains in class k (each answer weighs 1) |
| d_b | mean number of distinct resolved source domains per grounded answer naming b |
| G_A | own-domain share over grounded Phase A answers about b on A4 (max 12), rated iff ≥ 6 grounded answers (secondary, descriptive) |

Primary Grounding score = **G\***. mix_b, d_b and G_A are reported for every rated brand; no verdict rests on them.

### 2.5 Structured-data richness [NEW WEB DATA: audit]

Defined in `website_audit_protocol_v1_13.md` §5, fixed now: **SDRI** = 100 × (sum of 8 binary indicators)/8: (1) schema.org Organization or a subtype on the home page; (2) Brand on any audited page; (3) Product or a subtype on any audited page; (4) ≥ 1 `sameAs` on an Organization/Brand node; (5) a `sameAs` to Wikidata or Wikipedia; (6) a Wikidata item exists (adjudicated QID); (7) that item's official website (P856) has its registrable domain in D_b; (8) an English Wikipedia article is linked from that item. Sub-indices SDRI_site = (1)–(5), SDRI_kg = (6)–(8). Equal weights; no re-weighting after data. Extraction and indicators: `audit_v1_13.py` (each indicator tested, §13 item 12).

## 3. Hypotheses, tests and verdict rules

**Conventions (as v1.10 §7).** ρ_w = pooled within-category Spearman: average ranks are computed within each substrate and **centred on the substrate's mean rank (m_c + 1)/2** (runner decision 5); ρ_w is the Pearson correlation of the pooled centred ranks. Uncentred pooling adds a between-category component when substrates contribute different numbers of units (found in the v1.10 work); the uncentred v0.37–v0.41 convention is reported as sensitivity S10. Only substrates with ≥ 5 units in the comparison enter; the n floor is 30 units (runner decision 3). Values are compared unrounded. Permutation: the first variable permuted within substrate, 10,000 draws, p = (hits + 1)/(N + 1); a draw is a hit if |ρ_perm| ≥ |ρ_obs| − 10⁻¹² (two-sided) or ρ_perm ≥ ρ_obs − 10⁻¹² (one-sided). Bootstrap: units resampled within substrate, 2,000 draws, 90% percentile CI (reported, not a verdict input). Seeds 113001–113010 as listed. **Verdict order of a two-leg hypothesis (H1, H2):** MQ5 failed → UNDETERMINED; a leg with ≥ 30 units and |ρ| ≥ 0.50 → FALSIFIED; a leg below 30 units → UNDETERMINED; both |ρ| ≤ 0.30 → CONFIRMED; otherwise MARGINAL.

| ID | Tag | Role | Statistic | CONFIRMED | FALSIFIED | MARGINAL | UNDETERMINED |
|---|---|---|---|---|---|---|---|
| **H1_Sep_Presence** | t4 | PRIMARY (gate) | ρ_w(G\*, P_S1) and ρ_w(G\*, P_S0), units with G\* rated; seed 113001, two-sided p reported | both \|ρ\| ≤ 0.30 | either \|ρ\| ≥ 0.50 | otherwise | < 30 rated units, or MQ5 fails |
| **H2_Sep_Consistency** | t4 | PRIMARY (gate) | ρ_w(G\*, C\*_S1) and ρ_w(G\*, C\*_S0), units with both rated; seed 113002 | both \|ρ\| ≤ 0.30 | either \|ρ\| ≥ 0.50 | otherwise | < 30 units, or MQ5 fails |
| **H3_Run_Reliability** | t4 | PRIMARY (gate: reliability leg) | G\*_r per run r (rated iff g_{b,r} ≥ 3); for each run pair, ρ_w on the units rated in both runs; rel1 = mean of ρ_w over the pairs with ≥ 30 such units; rel3 = 3·rel1/(1 + 2·rel1); one-sided permutation (second run of each pair permuted within substrate, rel1 recomputed), seed 113003 | rel3 ≥ 0.50 AND p < 0.05 | rel3 < 0.30 | otherwise | < 30 units in 2 or more of the 3 pairs |
| H4_Sep_Ranking | t4 | SECONDARY (conditional) | ρ_w(G\*, R\*), R\* = v1.10's locked statistic (MNP, selected at its Stage S), extractor and floor, applied to the same t4 N3 S1 category answers; seed 113004 | \|ρ\| ≤ 0.30 | \|ρ\| ≥ 0.50 | otherwise | < 30 units; INACTIVE unless activated |
| H5_Sep_Sentiment | t4 | SECONDARY (conditional) | ρ_w(G\*, S), S = v1.11's locked score on the same t4 answers if a locked score on them exists by Stage C2 (v1.13 makes no judge call); otherwise v1.11's locked omnibus score at t3, labelled cross-panel; seed 113005 | as H4 | as H4 | as H4 | as H4 |
| H6_Sep_Coverage | t4 | SECONDARY (conditional) | ρ_w(G\*, Cov\*), Cov\* = v1.12's locked score on its own collection (same 112 units, N3, S0); seed 113006 | as H4 | as H4 | as H4 | as H4 |
| H7_Struct_Gap | audit + t4 | SECONDARY (or hand-off) | ρ_w(SDRI, G\*), units with both; one-sided; seed 113007. Reported beside it: ρ_w(SDRI, P_S0) and the partial ρ_w(SDRI, G\* \| P_S0) (within-substrate rank residuals) | ρ ≥ 0.30 AND p < 0.05 | ρ ≤ 0.10 | otherwise | < 30 units; or Part II not collected before Stage C2 (then handed to Paper B, §8) |

Seeds 113008 (bootstrap), 113009 (S-sensitivities), 113010 (reserved) are recorded now.

**Activation rule (H4–H6; runner decision 4, as v1.12's).** A leg is active only if tag `v1.10-prereg-r2` (H4), `v1.11-prereg-r1` (H5) or `v1.12-prereg-r1` (H6), or a later revision, is pushed **before** the v1.13 lock commit; the v1.13 lock then records that tag, its commit and the file defining the score, which is used exactly as locked (its own unit, floor and rated set). Otherwise the leg is INACTIVE (no verdict) and may be tested only under a later pre-registration. An active leg is computed at Stage C1 if its score exists then, otherwise at Stage C2; if the score does not exist by Stage C2 the leg is UNDETERMINED (score not available) and handed to Paper B. At this draft: `v1.10-prereg-r2` is pushed (tag object `841f7307747cd32e618abda974767e8879b91b37`, commit `db938197b0caf83df790ed92c1d283b18d62ad9b`; checked with `git ls-remote` on 2026-11-10); v1.11 and v1.12 have no tag.

**Gate rule.** **PASS** iff H1, H2 and H3 are all CONFIRMED — downgraded to MARGINAL if any active secondary separability leg (H4–H6) is FALSIFIED (a leg computed at Stage C2 re-issues the gate verdict with its own timestamp, downgrade only). **FAIL** if H1, H2 or H3 is FALSIFIED. **UNDETERMINED** if H1 or H2 is UNDETERMINED (published as such; the instrument goes back to design). Otherwise **MARGINAL**: Pablo decides (recorded) whether Paper B proceeds. H7 never changes the gate.

**Rationale.** G\* is a share conditional on being named and on the answer's search returning anything, so it is not mechanically tied to how often a brand is named; g_b is (MQ6 checks this). Separability is required against P in both conditions because G\* is computed from S1 answers whose own Presence (P_S1) is the most direct rival, while P_S0 is Presence as the programme measures it at t4. A score that is mostly zeros could pass the separability bands by having no variance; MQ5 makes that UNDETERMINED instead of CONFIRMED.

## 4. Manipulation and quality checks [RE-ANALYSIS: t4]

| ID | Check | Rule |
|---|---|---|
| MQ1 | Parse | the parser completes on 100% of answered S1 records, in both fields (an exception halts) |
| MQ2 | Search use | share of a model's category answers with ≥ 1 entry in `sources`, per model; < 0.25 flags the model "search rarely used" in every result (v0.42 MC_Search bar); a model below 0.10 is dropped from G\* (reported both ways) |
| MQ3 | Class coverage | share of distinct (answer, domain) source pairs classed `other` or `unresolved`: > 0.40 flagged; > 0.60 labels the source-mix descriptives "low coverage" (no verdict uses the mix) |
| MQ4 | Google redirects | share of Gemini sources whose domain is taken from `title` (U5) and share left `unresolved`; > 0.20 unresolved → Gemini dropped from G\* for the primary (N3 becomes two models; sensitivity S5 keeps it) |
| MQ5 | Degeneracy | gate UNDETERMINED if > 0.80 of rated brands have G\* = 0, or within-substrate SD of G\* is 0 in ≥ 3 of the 5 substrates (runner decision 7) |
| MQ6 | Mechanical coupling | ρ_w(g_b, π̂_S1) and ρ_w(G\*, g_b) reported (rated units); \|ρ_w(G\*, g_b)\| ≥ 0.50 flagged (the share is tracking the count) |
| MQ7 | Frozen inputs | SHA-256 of `source_classes_v1_13.md` and `brand_domains_v1_13.csv` at Stage C1 equal the anchored values, and no D_b row is UNRESOLVED; v0.42's coder and scorer equal their pins (§0); a mismatch halts |
| MQ8 | Citations vs sources | per provider: share of answered S1 answers with ≥ 1 entry in `citations`, and share of cited URLs that also appear in `sources`; reported only |

## 5. Stages

1. **Stage C1 (after the Part I lock; t4 data).** Verify anchors and MQ7 → parse t4 S1 → classify → per-brand statistics → MQ1–MQ6, MQ8 → H1–H3 and the active H4–H6 whose scores exist → baseline → sensitivities. Verdicts to `v1_13_verdicts.json`.
2. **Stage A (after the Part II lock + 24 h).** Audit per `website_audit_protocol_v1_13.md`; writes `audit/v1_13_audit_records.jsonl` and, after the logged QID adjudications, `audit/v1_13_sdri.csv`.
3. **Stage C2.** H7, the SDRI descriptives, S6 and any active H4–H6 not computed at C1; appended to the verdict file with their own timestamp.

There is no pilot stage (§0).

## 6. Baseline descriptives (no verdicts) [RE-ANALYSIS: t4]

Per substrate and per model (N3 and A4): share of category answers with ≥ 1 source; sources and distinct domains per answer; source-type mix; share of answers retrieving any registry brand's own domain; share retrieving Wikipedia/reference; the 20 most-retrieved domains; the distribution of G\* (median, IQR, share zero); g_b and rating coverage; the same for brand answers (Phase A) with G_A; Phase A v0.19–v0.22 (yes/no) reported apart from v0.23 (open). The same tables for the cited set (`citations`) are reported beside them.

## 7. Sensitivities (verdict changes listed next to the verdict)

S1 denominator m_b instead of g_b (the rating rule stays g_b ≥ 6). S2 cited set (`search.citations`) instead of `sources`, de-duplicated by U6. S3 panels A4 and C3. S4 rating floors 3 and 10. S5 Gemini kept/dropped against the MQ4 decision. S6 D_b as verified by Part II (aliases from the audit's final redirect domains and Wikidata P856 added). S7 P and C\* from AIAS 2.0 t3 (legacy panel; cross-panel, descriptive). S8 leave-one-substrate-out ranges for H1–H3. S9 source set extended with URLs written in the answer text (Markdown links and bare `https?://` addresses). **S10** every pooled statistic under the uncentred v0.37–v0.41 convention (§3). **S11** every gate statistic (H1–H3 and any active H4–H6) without the Denon unit (v0.19; COI correction, §11).

## 8. What Paper B inherits (not pre-registered here)

Pre-registered separately, only after PASS (or MARGINAL with Pablo's recorded decision): the locked parser, `source_classes_v1_13.md`, D_b, `score_v1_13.py` and tests; per-answer source tables (SHA-256 pinned); **source-coverage stability over waves** (t4 → v0.40 S1 arm, Nov 17–21, US airlines and retail banks → t5 → t6, each re-classified with the frozen lists); **phantom-brand grounding** (what answers retrieve when they name a registry phantom brand; registry phantom flags); **identity load** (OMNI cultural vs category frames); **typology** (G\* × P × C\* × R\* profiles); H7 if Part II was not collected in time; any active H4–H6 whose score did not exist by Stage C2; re-audits of structured data at t5/t6; v0.40's brands added to the audit if v0.40's pre-registration declares its search record.

## 9. Limitations

S1 answers depend on the web on the day and on each provider's search back-end; they are reproducible only as recorded. The retrieved set (`sources`) includes results an answer did not use, and what it holds differs by provider (all results of every search for Anthropic, the search action's sources for OpenAI, the grounding chunks for Google, whose URLs are redirects with a domain title), so model differences mix model and tool; the cited set (S2) is what the answer attributes. Own-domain retrieval needs the brand's site to be indexed and open to crawlers; a low G\* can reflect robots policies as much as model behaviour. D_b is a declared list built from repository records and the runner's logged decisions, and can miss regional or campaign domains (S6). Five categories, one market and language (US English). Static HTML only in the audit: structured data injected by JavaScript is missed (protocol §7).

## 10. Deviations policy

`osf/methodology/v1_13/anchor/DEVIATIONS.md` opens with **Entry 0 (ex ante)**: COI carry-forward and the Denon correction (§11), the runner's D_b decisions (§2.3), and the anchor sequence of §0. After the lock: every change gets an entry (id, date, ex ante/ex post, what, why, effect on inference); a frozen-input hash mismatch halts the run; a parser fix is allowed only to restore a rule as written; thresholds, floors, seeds, class lists, D_b and the gate rule do not change; a failed gate is published with the same prominence as a pass.

## 11. Declarations

**Conflict of interest.** The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. This study performs no new brand selection: it re-uses the five omnibus registries (v0.19–v0.23) and carries forward each registry's source-phase COI handling unchanged. Part II fetches public pages of the registry brands' own websites; it contacts no brand and buys nothing. Two items of record apply, quoted verbatim from their source records:

- *v0.19 audiophile headphones* — `osf/v19/PRE_REGISTRATION_v0_19.md` §2.3: "**AKG removed from Cell A short-list; Denon substituted.** AKG is Samsung-owned since 2016. The author's COI declaration names Samsung; including AKG would invite the kind of reviewer suspicion AIAS™ 1.0 does not need to absorb. Denon carries comparable heritage stature (founded 1910; AH-D7000 → D9200 audiophile line) and removes the question. Decision rationale recorded here for audit trail." Declaration of the same file: "Note: AKG (Samsung-owned since 2016) was considered for Cell A inclusion on substantive heritage-audiophile grounds and substituted with Denon to avoid any appearance of conflict; substitution rationale recorded in §2.3 above." (Also recorded as Entry 1 of the DEVIATIONS section of the v0.19 paper, `papers/v0_19/v0_19_ssrn_paper_draft.md` §5.)
- *v0.22 automotive* — `papers/v0_22/v0_22_ssrn_paper_draft.md`, Declarations §COI: "Samsung subsidiaries hold tier-2/3 component supply relationships with several brands in the v0.22 registry: Harman International (audio systems) supplies Mercedes-Benz, BMW, and other premium automotive OEMs; Samsung SDI (battery cells) supplies BMW (i-series), Volkswagen Group brands including Bentley and Porsche (Stellantis-adjacent platforms), and others; Samsung Display (infotainment) supplies Mercedes-Benz and BMW. Tesla and Polestar also have tangential Samsung-component exposure at the parts level. These are non-competitive supply relationships; Samsung Electronics America does not produce or market passenger car brands and has no brand-level competitive overlap with any v0.22 registry entry. The COI was screened and documented in DEVIATIONS Entry 0 (Part B) of the pre-registration module; no operational restriction on registry composition was imposed."

Correction (November 10, 2026): Denon, which replaced AKG in the v0.19 registry, has itself been owned by Harman International, a wholly owned subsidiary of Samsung Electronics, since September 23, 2025, when Harman completed its acquisition of Sound United from Masimo (HARMAN press release, Business Wire, September 23, 2025: https://www.businesswire.com/news/home/20250923135384/en/HARMAN-Completes-Sound-United-Acquisition-to-Expand-Premium-Audio-Leadership); the v0.19 headphones registry therefore includes one Samsung-group brand. The substitution did not achieve its purpose, and this was not noticed until November 10, 2026.

Handling in v1.13: Denon stays in the registry (no new brand selection); every gate statistic is also reported without the Denon unit (sensitivity S11), with any verdict change listed next to the verdict. Part II fetches Denon's own website like any other brand's, under the same rules (public pages only, robots.txt respected, no contact, no form, nothing bought). The correction and its handling open DEVIATIONS Entry 0.

Samsung Electronics had no role in the design, conduct, analysis or reporting of this work.

**Funding.** Self-funded. **Ethics.** No human subjects; Part II reads public web pages under the protocol's robots and rate rules.

**Use of AI tools.** During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.

## 12. Lock procedure and change log

Between sending and lock, clarifications that change no hypothesis, threshold, panel, data source or decision rule are logged here; any other change goes back to Pablo (Part I) and restarts the 24 hours (Part II). Part I lock: refresh `prereg/LOCK_MANIFEST_v1_13.sha256` (this file, `source_classes_v1_13.md`, `registries/brand_domains_v1_13.csv`, `scripts/score_v1_13.py` and its tests); commit; tag `v1.13-prereg-r1`; push; write the anchor with the activation record of H4–H6; deposit `prereg/`, `registries/` and `anchor/` at OSF and verify their SHA-256 there; only then Stage C1. Part II lock: the same for `website_audit_protocol_v1_13.md`, `registries/wikidata_types_v1_13.csv`, `dry_run_audit_v1_13.txt`, `scripts/audit_v1_13.py`, its tests and fixtures, under tag `v1.13-audit-r1`; then the receipt time and the 24 hours.

**Change log.**
- 2026-11-10: DRAFT r1 written by the runner's sub-agent (commit `062b94a`); not sent.
- 2026-11-10, r1 completed for sending (this text): the runner's decisions 1–11 applied (§13); the declared v0.39 pilot dropped before it was run; primary evidence field `sources` (`citations` → S2); ρ_w centred (S10 uncentred); activation rule for H4–H6; S11 (without Denon); written out as clarifications: the verdict order of H1/H2 and H3's rel1 over the qualifying run pairs; D_b built from repository records (2 RESOLVED, 110 UNRESOLVED, 18 ambiguities listed; SHA-256 `e45aa22c…` as built); COI correction for Denon; AI-use statement; Part II: User-Agent, run window, Mac load plan, page-selection details, QID-rule words, phantom units = v0.22 cell D; `score_v1_13.py` core and `audit_v1_13.py` with their tests and the dry run (§13, item 12). No threshold, floor, seed or class list changed. Sent to Pablo for the 24-hour review.
- 2026-11-10, **runner, before sending:** decisions on the 110 UNRESOLVED D_b rows (each a domain with its source, or NONE) and the resulting SHA-256 of `brand_domains_v1_13.csv` are entered here and in §2.3.

## 13. Settled before sending (runner, 2026-11-10)

1. **Brand domains (D_b):** a frozen offline list built now from the registries and each brand's official site as recorded in the repository; no lookups at analysis time; every domain with its source; ambiguous brands listed, not guessed; pinned by SHA-256 (§2.3). Repository records establish 2 of the 112 domains; the 110 others are UNRESOLVED and decided by the runner before sending (§12).
2. **Primary evidence field:** `search.sources` for all providers, the field the feasibility record shows for all three N3 models; `citations` is sensitivity S2; Gemini redirect URLs are resolved by their title domain (U5). One rule for all providers (§2.1).
3. **Floors:** G\* rated at g_b ≥ 6 (per run 3); n floor 30 units; ≥ 5 units per substrate (§2.4, §3).
4. **H4–H6:** conditional legs against Ranking (v1.10, tag `v1.10-prereg-r2`: its locked statistic, MNP per `osf/methodology/v1_10/outputs/selection_v1_10.json` on branch `v1.10` @ `0399a0b`, applied to the same t4 answers), Sentiment (v1.11) and Coverage (v1.12); active only if that pre-registration's tag is pushed before the v1.13 lock commit, as v1.12's activation rule; otherwise INACTIVE (§3).
5. **ρ_w** with within-category ranks centred on the category mean rank; the uncentred v0.37–v0.41 convention is reported as S10 (§3, §7).
6. **v0.42's top-domains descriptive** stays unseen until the class lists freeze (§2.3).
7. **MQ5** (> 80% zeros, or flat in ≥ 3 substrates) as drafted (§4).
8. **Website audit:** robots.txt respected; ≥ 10 s between requests to one host; User-Agent `AIAS research crawler; https://thirdsystem.ai` (no personal email); public pages only, no login, no forms; at most 3 pages per site; run window and Mac load plan declared (protocol §4): never during Nov 17–21; it may run while a paid collection runs because it makes no paid call.
9. **COI:** source records carried verbatim; the draft's TODO on the ownership of the v0.19 registry brands is resolved by the dated correction for Denon (§11); every gate statistic is also reported without Denon (S11); Part II fetches Denon's own website like any other brand's.
10. **AI-use statement:** Pablo's text of Nov 10, verbatim (§11).
11. **Held studies (v0.38, v0.39):** the pilot on v0.39's search-on answers is **dropped**. The draft had declared it (Stage P) but never run it, and no rule depended on its results; the instrument was specified without looking at search-on answers (§0). No held-study material enters any output of v1.13.
12. **Completed for sending:** t4 loaders, P/C\* readers, permutation and bootstrap drivers, the gate with conditional legs, sensitivities and the verdict-file writer in `score_v1_13.py` (39 tests on synthetic data, all pass); `audit_v1_13.py` with `--dry-run` (synthetic fixtures under `.test`, socket and DNS access refused: 7 fixture units, every indicator as the fixtures expect, 0 network attempts; record `dry_run_audit_v1_13.txt`) and 28 tests covering each of the 8 indicators, SDRI, page selection, robots, rate, redirects, the QID rule, the no-network guard and the `--collect` refusal (all pass); `registries/wikidata_types_v1_13.csv` (words, not QIDs, because no lookup was made); `source_classes_v1_13.md` header and pilot reference updated (lists unchanged).

**For Pablo (24-hour review).**
- **Denon.** Since September 23, 2025 Denon has been a Harman (Samsung) brand. The correction in §11 is written in your name; please confirm the wording. Handling: Denon stays, every gate statistic is also reported without it (S11), and its website is audited like any other.
- **Grounding rests on what search returns.** The feasibility record shows `sources` for all three newest models but no citation counts, so G\* is the share of grounded answers whose retrieved sources include the brand's own site; what the answer cites is sensitivity S2 (§2.1).
- **Brand domains.** The repository recorded official sites for only 2 of the 112 brands; how the other 110 were settled is logged in §12 (§2.3).
- **Two differences from the v1.12 draft.** P at t4 here uses the share of recognized N3 model-runs (C_P/6); v1.12 uses the number of N3 models recognizing the brand in a majority of runs (C_P/3). C\* here divides φ by 7.2 (v1.9); v1.12 divides by 9 (the three-model maximum). The divisor changes no verdict (verdicts are rank-based); the P definition can. Say which to use in both.
- **Timeline.** Part I locks on your OK; Part II locks after this review and runs no sooner than 24 hours after you receive its locked text, never during Nov 17–21.
