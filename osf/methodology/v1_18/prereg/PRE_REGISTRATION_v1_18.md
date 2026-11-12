# AIAS v1.18 — Grounding under four competing definitions (exploratory re-analysis beside v1.13)

AIAS™ Measurement Program — Third System™. Pre-registration **r1, draft for the coordinator's check** (2026-11-12). Not locked: the lock is tag `v1.18-prereg-r1` pushed to origin and the OSF deposit of `prereg/` and `registries/`, both the coordinator's and Pablo's gates. Nothing that this study estimates has been computed on real data (§9). No model call, no web fetch, no spend.

## 0. Status, scope and lineage

| Field | Value |
|---|---|
| PHASE_ID | v1.18 |
| PHASE_TYPE | Exploratory re-analysis [RE-ANALYSIS: t4]. No confirmatory hypothesis, no verdict, no gate. |
| Branch | `v1.18`, from `v1.13` @ `1b58837` (v1.13 Stage C1 commit). |
| Origin | Literature check of Nov 11, 2026 (project doc claude/literature-check-2026-11-11.md), study (C), approved by Pablo ("ok plan updates", Nov 11, 11:22 pm): "Grounding under competing definitions … Exploratory beside v1.13, not a change to it." |
| Data | t4 = v0.42's stored search-on (S1) category answers, three runs per cell on N3 (Claude Fable 5.2, GPT-6 Astra, Gemini 4 Argon), the 270 answers v1.13 Stage C1 parsed (its MQ1). |
| Relation to v1.13 | v1.13's locked tests, verdicts and Stage C2 (due by Nov 25) are unchanged (§8). |

**Why this study.** Published shares of AI citations that "belong to brands" range from a few per cent to over 80 per cent, and the program's literature check found that the spread is largely one of definition. As recorded there (verified at source, Nov 11, 2026): Kumar (arXiv 2606.20065, Jun 2026; vendor study by a Ranqo co-founder) finds about 78% of 149,912 citations go to corporate websites but only 2.9% to the brand's own domain; Profound (Singh, Jul 30, 2026; via WARC, Sep 1, 2026) reports "roughly 57%" of AI citations to brand websites, where "brand" means "company-operated web properties of any company, not only the category owner's"; Yext (Oct 9, 2025) reports 86% "brand-managed" = websites 44% plus listings 42%; Muck Rack (Albasi, updated Oct 28, 2026) reports "More than 84% come from earned and third-party sources", which include other companies' pages, with owned media at 13.7% rising to 15.2%. This study applies the four definitions to one set of answers with one domain table, so that the definitional part of the spread can be read off directly for the program's brands.

## 1. Questions (exploratory)

- **Q1.** Per brand and for the program, what is the Grounding share under each of the four definitions?
- **Q2.** How far do the definitions agree: do brands keep their order, and how many brands' readings move by a material amount?
- **Q3.** How sensitive are Q1–Q2 to the domain table's open choices (unresolved domains, retailers, aliases), to the evidence field and to the panel?

## 2. Data

- **Records.** `osf/v42/data/t4_raw.jsonl` (v0.42 worktree), selected exactly as v1.13 Stage C1 selects them, by importing v1.13's code (`score_v1_13.py`: `dedupe_calls`, `select_calls(N3, S1, Phase B)`, `resolve_source` U1–U5). Loader check (pre-lock, §9): 990 lines, 876 calls after de-duplication, **270** answered S1 category answers on N3 (= v1.13 MQ1), and per provider the answers with ≥ 1 citation and the cited URLs (Google 16 and 122, OpenAI 86 and 516, Anthropic 75 and 557) equal v1.13's MQ8.
- **Who is named.** v0.42's certified coder rows (Phase B, `mentioned` = 1) through v1.13's `named_index` and the frozen D_b list (`brand_domains_v1_13.csv`), as in v1.13 §2.1. A unit is a (substrate, brand) row of that list (112 units). Not read before the lock.
- **Primary evidence field: `search.citations`** (the URLs the answer attributes). Argument: all four outside definitions are shares of *citations*, so the comparison is like for like; v1.13's primary field is `sources` (retrieved results, including results the answer did not use), which v1.13 chose because it is recorded for all providers, but v1.13's MQ2 and MQ8 show `citations` populated in as many answers as `sources` on every provider (16, 86 and 75 of 90 in both), and 98.6–100% of cited URLs are also in `sources`, so no provider is lost. `sources` is sensitivity S5, which links this study to v1.13's G\*.
- **Answer domains.** For each answer, the set of distinct registrable domains of its resolved cited URLs (U1–U6; Gemini redirects by title, U5). Each domain counts once per answer, whatever the number of URLs on it (as v1.13's mix_b).

## 3. The four definitions (exact rules)

Every cited domain x of an answer a is given one of five labels relative to a brand b named in a: **focal** if x ∈ D_b; otherwise its class in the domain table (§4): **company**, **listing**, **review_social**, **editorial_other** (a domain in another unit's D_b is company by rule T0). Domains whose table class is UNRESOLVED leave the denominator (primary; §7 S1 for the alternatives). With L(a, b) = the labels of a's classified domains and n = |L(a, b)|, the pair share under definition d is #{x ∈ L(a, b): label ∈ S_d} / n, with

| Definition | Source of the definition (as the literature check records it) | Classes counted, S_d |
|---|---|---|
| **K, own domain only** | Kumar: "only 2.9% the brand's own domain" | focal |
| **P, any company's site** | Profound: "company-operated web properties of any company" | focal + company |
| **Y, own site plus listings** | Yext: websites ("Full Control") + listings ("Controllable") | focal + listing |
| **M, everything the brand does not own** | Muck Rack: "earned and third-party", incl. other companies' pages | company + listing + review_social + editorial_other |

Choices argued. (i) *Focal through D_b only.* v1.13's frozen D_b is the program's one audited statement of each brand's own domains; re-deciding it here would change v1.13's own-domain rule by the back door. Alias candidates are a sensitivity (S3). (ii) *Domain, not URL.* A page count rewards sites that are cited many times in one answer; the domain set treats each answer's distinct sources equally, as v1.13 does. (iii) *A share per (answer, brand) pair, then averaged.* The same category answer is about several brands at once, and "focal" differs between them; Kumar's and the others' pooled shares are over citations, so the program-level share here is the pair-weighted mean (§5, E2), and the brand-weighted mean is reported beside it. (iv) *M is the complement of K.* With a common denominator, M = 100 − K for every pair and every brand, exactly. Muck Rack's definition therefore changes the headline level (a brand-controlled share near K becomes a third-party share near 100 − K) but not the order of brands; every K–M agreement statistic is −1 or 100% by construction and is reported as an identity, not as an estimate. Listing and review classes do not enter K or M, so M's headline matches Muck Rack's "earned and third-party" only as far as its owned/earned split matches focal/not focal; neither Muck Rack page defines "earned" (literature check, row 11). (v) *Retailers are listings* (Yext's "controllable" listings are pages a brand can manage on someone else's platform; a retailer's product page is the main such page for consumer brands); Profound's "any company" could include retailers, so S2 moves them to company.

## 4. The domain table

`registries/domain_rules_v1_18.md` (rules), `registries/domain_table_v1_18.csv` (one row per distinct domain), `registries/build_domain_table_v1_18.py` (builder with the hand classifications). Precedence: T0 registry D_b → company; T1 v1.13's frozen class lists mapped (retailer → listing; forum/UGC → review_social; news, review/editorial, reference → editorial_other) and the public-sector TLD rule; T2 hand classification under the written class definitions; T3 UNRESOLVED. Each distinct domain is classified once, for every answer and brand in which it appears.

**4.1 Blindness.** The coder classified from an alphabetical list of the cited domains outside D_b, with no count, model, substrate, answer, brand, field label or v1.13 class; the coded brand rows were never read by a v1.18 script; no per-brand Grounding share (v1.13's or this study's) was looked at. The order of writing is declared in the rules file (§"Order of writing"): rules fixed in the working plan and the builder's docstring, then the classification, then the rules written out in full.

**4.2 Counts (r1 draft).** 1,345 distinct domains in either field (339 cited, 1,344 retrieved); 33 are D_b domains (21 cited). Cited domains outside D_b, 318: editorial_other 172, company 54, listing 27, review_social 6, UNRESOLVED 59 (17.4% of the 339 distinct cited domains). With the 21 cited D_b domains (company by T0): company 75. Sources-only domains, 994: 67 by T1, 927 UNRESOLVED (not hand-classified in r1).

**4.3 Unresolved domains** are listed in the table and reported with every result (their share of each brand's cited domains, and S1); they are never guessed.

**4.4 Audit.** 60 rows, seed 118003: 50 hand-classified rows drawn proportional to class and 10 T1 rows (`draw_audit_sample_v1_18.py`; `audit_sheet_v1_18.csv` holds the domains only). The second coder (Pablo or a person he names) classifies them blind to the key and may also resolve any of the 59 cited UNRESOLVED domains with a stated reason. Reported: raw agreement and Cohen's κ. If raw agreement on the 50 hand rows is below 0.85, every hand row is re-coded before the lock and disagreements go to Pablo. The audit is completed **before** the lock; any change is logged in DEVIATIONS and re-pinned in the manifest.

## 5. Estimands and reporting rule

Rated brand: a unit with a D_b (status RESOLVED; NONE units are not rated, as in v1.13) and **g_b ≥ 6** grounded answers naming it (an answer is grounded for b if it has at least one classified cited domain); the floor is v1.13's G\* floor.

- **E1 (per brand).** S_d(b) = 100 × the mean over b's grounded answers of the pair share, for d ∈ {K, P, Y, M}; with g_b.
- **E2 (program).** The pair-weighted mean of the pair shares over all (answer, unit-with-D_b) pairs (primary; comparable to the outside pooled shares) and the brand-weighted mean over rated brands; and the five-class mix (pair-weighted mean of each label's share, plus the UNRESOLVED share before it is dropped).
- **E3 (order).** For each of the six pairs of definitions, ρ_w = pooled within-substrate Spearman of rated brands' shares, ranks centred on the substrate mean (v1.13 §3 convention; substrates with < 5 rated units dropped). K–M is −1 by identity.
- **E4 (readings that move).** For each pair, the share of rated brands whose share differs by **more than 25 percentage points** (primary threshold: a quarter of the scale, about the gap between Profound's 57% and Yext's 86% and well under the 3%-to-86% spread); 10 and 50 points reported beside it.
- **Reporting rule.** Exploratory: no hypothesis, no verdict, no p-value. Every estimand is reported with its 90% interval (§6), for all rated brands, under each sensitivity; nothing is selected after the data. The one-table summary is: per definition, the program share (E2) with its interval and the median and range of brand shares (E1); beside it E3 and E4 for each pair. Statements of the form "the headline share depends on the definition" are made only from E2's intervals (definitions whose intervals do not overlap are called different; otherwise "not distinguishable at this n").

## 6. Intervals

Cluster bootstrap over **cells** (substrate × model × question; the three runs of a cell stay together, because runs of one question share a prompt and often a search), resampled with replacement within substrate; 2,000 draws; seed 118001 (118002 reserved for sensitivities); every estimand recomputed per draw, including which brands are rated; 90% percentile intervals (v1.13's level). Brands rated in fewer than 50% of draws are flagged.

## 7. Sensitivities (each reported beside the primary; none replaces it)

S1 UNRESOLVED table domains kept in the denominator, counted outside every class (lower bound for K, P, Y) or inside P's and Y's classes (upper bound); they are never focal, so they always count for M. S2 retailers (`retailer` = 1) counted as company (Profound read widely). S3 `alias_of` candidates with class company counted as focal for their unit. S4 floors 3 and 10. S5 the retrieved set `search.sources` (v1.13's primary field) instead of `citations`, reported with its UNRESOLVED share (r1: most sources-only domains unclassified). S6 without the Denon unit; S6-COI without Denon and the five brands with Cheil Worldwide or Iris agency ties (§13). S7 without Gemini 4 Argon (v1.13 MQ2 flags it "search rarely used": 16 of 90 answers with a source).

## 8. v1.13 is unchanged

v1.13's pre-registration, frozen lists, D_b, scorer, Stage C1 verdicts (gate MARGINAL; H1 ρ 0.307 and 0.395; H3 undetermined, as recorded on Nov 11) and Stage C2 (due by Nov 25, 2026) are not changed, re-run or re-interpreted by this study. v1.18 imports v1.13's code read-only, writes only under `osf/methodology/v1_18/`, and adds no domain to v1.13's lists. Nothing here enters v1.13's gate or Paper B unless a later pre-registration says so.

## 9. Looks at real data before the lock (declared)

1. `extract_domains_v1_18.py` read t4 (SHA-256 `f3109091f51a…`, as v1.13's C1 input record) to count records and answers, reproduce v1.13's MQ1 (270) and MQ8 counts, and list distinct domains. It does not read the coded brand rows.
2. The coder read the alphabetical cited-domain list to build the table (§4.1).
3. Before writing the design, the lane read v1.13's published Stage C1 file `v1_13_verdicts.json` at its aggregate quality checks only (MQ1–MQ8: e.g. 42 rated units, share of G\* = 0 0.405, MQ2 and MQ8 per provider), not its per-brand values. No v1.18 estimand was computed on real data; the dry run uses a synthetic world only.

## 10. Limitations

One wave, three models, five categories, US English. Citations depend on each provider's search tool (Gemini cites in only 16 of 90 answers). Domain classes are a judgement; the audit measures it but does not remove it; "company" vs "editorial" is hardest for agencies, small blogs and research firms. D_b is v1.13's list and can miss regional or campaign domains (S3 shows how much that matters). The outside figures are pooled over millions of citations, other prompts and other models; this study compares definitions, not levels with theirs.

## 11. Deviations policy

`DEVIATIONS.md` (stub; Entry 0 ex ante). After the lock every change is an entry (id, date, ex ante or ex post, what, why, effect); the definitions, the table, the floors, the thresholds and the seeds do not change; a domain-table correction after the lock runs only as a labelled sensitivity.

## 12. Lock procedure

Audit (§4.4) → domain table final → `prereg/LOCK_MANIFEST_v1_18.sha256` regenerated (`write_manifest_v1_18.py`) → commit → tag `v1.18-prereg-r1` → push → OSF deposit of `prereg/` and `registries/` with SHA-256 verified → only then `analyse_v1_18.py --run` (it refuses unless the tag is on origin and every manifest hash matches).

## 13. Declarations

**Conflict of interest.** The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. This study re-analyses stored answers scored against brand registries fixed in earlier phases; it performs no new brand selection, and each registry carries its source-phase conflict-of-interest handling forward (v1.13 §11 and DEVIATIONS Entry 0). Three items of record apply, quoted verbatim from their source records as v1.13 §11 quotes them. *Audiophile headphones (v0.19)* — `osf/v19/PRE_REGISTRATION_v0_19.md` §2.3: "**AKG removed from Cell A short-list; Denon substituted.** AKG is Samsung-owned since 2016. The author's COI declaration names Samsung; including AKG would invite the kind of reviewer suspicion AIAS™ 1.0 does not need to absorb. Denon carries comparable heritage stature (founded 1910; AH-D7000 → D9200 audiophile line) and removes the question. Decision rationale recorded here for audit trail." (Also v0.19 DEVIATIONS Entry 1.) Correction (November 10, 2026): Denon, which replaced AKG in the v0.19 registry, has itself been owned by Harman International, a wholly owned subsidiary of Samsung Electronics, since September 23, 2025, when Harman completed its acquisition of Sound United from Masimo; the v0.19 headphones registry therefore includes one Samsung-group brand. The substitution did not achieve its purpose, and this was not noticed until November 10, 2026. Denon stays in every analysis (sensitivity S6). *Automotive (v0.22)* — `papers/v0_22/v0_22_ssrn_paper_draft.md`, Declarations §COI: "Samsung subsidiaries hold tier-2/3 component supply relationships with several brands in the v0.22 registry: Harman International (audio systems) supplies Mercedes-Benz, BMW, and other premium automotive OEMs; Samsung SDI (battery cells) supplies BMW (i-series), Volkswagen Group brands including Bentley and Porsche (Stellantis-adjacent platforms), and others; Samsung Display (infotainment) supplies Mercedes-Benz and BMW. Tesla and Polestar also have tangential Samsung-component exposure at the parts level. These are non-competitive supply relationships; Samsung Electronics America does not produce or market passenger car brands and has no brand-level competitive overlap with any v0.22 registry entry. The COI was screened and documented in DEVIATIONS Entry 0 (Part B) of the pre-registration module; no operational restriction on registry composition was imposed."

*Agency work (Cheil Worldwide and Iris).* Cheil Worldwide, a marketing company of the Samsung group in which Samsung Electronics holds 28.43%, or its agency Iris has done advertising, public-relations or search-marketing work for five registry brands: Chevrolet (for GM Korea, 2017), BMW (UK consumer public relations, 2018), Bentley (experiential agency of record in the Americas from 2021), Jack Daniel's (UK digital agency from 2022, since replaced) and Eucerin (search marketing for Beiersdorf from 2024). (Conflict-of-interest screen of v0.62, DEVIATIONS Entry 0, Part F.) As Denon, these five brands stay in every analysis, and every estimand is also reported without them and Denon (sensitivity S6-COI).

Samsung Electronics had no role in the design, conduct, analysis or reporting of this work.

**Funding.** Self-funded. **Ethics.** Not applicable; no human subjects.

**Use of AI tools.** During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.

## 14. Files

`prereg/`: this file; `LOCK_MANIFEST_v1_18.sha256` (draft); `write_manifest_v1_18.py`. `registries/`: `domain_rules_v1_18.md`, `domain_table_v1_18.csv`, `build_domain_table_v1_18.py`, `draw_audit_sample_v1_18.py`, `audit_sheet_v1_18.csv`, `audit_key_v1_18.csv`. `scripts/`: `common_v1_18.py`, `extract_domains_v1_18.py`, `analyse_v1_18.py`, `tests/test_v1_18.py`. `outputs/prelock/`: the blind domain lists and `prelock_counts_v1_18.json`. `outputs/dry_run/`: `dry_run_v1_18.txt`, `dry_run_results_v1_18.json`. `DEVIATIONS.md`, `README.md`.
