# AIAS™ Presence Measurement Protocol — Pre-Registration v0.39 (revision r1)

**Substrate:** Commercial coffee roasters for cafés, retailers and specialty roasteries (US market) — sample, shop and production machines
**Design:** Focal-brand designed-for-test inside a full category registry (v0.7 → v0.38 lineage), with a two-arm panel (legacy fixed panel; current assistants with and without web search). Focal brand: Bellwether Coffee (Shop Roaster).
**Programme position:** First focal test of a brand whose proposition is the removal of a category barrier. Tests H1 Conditional Reweighting at the level of the brand's defining category entry point (the infrastructure constraint) and H2 Default Reinforcement at the level of the category frame (what a café is told it needs before any brand is named). First pre-registered retrieval arm. First Physical-vs-AI Availability contrast that uses a trade-show floor as the physical-availability set. Carries the v0.38 product-generation contrast to a second brand as a descriptive.
**Protocol version:** Presence definitions per Methodology v1.2 (SSRN 6761698); legacy-arm panel and decoding per v0.17–v0.38 (six-model panel; temperature 0.0; max output 2,048 tokens; one call per probe × model).
**Lock target:** git tag `v0.39-prereg-r1` on branch `v0.39`. **External anchor (pre-declared):** deposit of this pre-registration, the probe battery, the registry, the scripts and the lock manifest at OSF `ec6wh` → `v39/prereg/` before any study probe is sent. The tag is pushed to `origin` once the GitHub credential is restored (see v0.38 DEVIATIONS entry 1); because the OSF deposit is the declared anchor, an unpushed tag at acquisition is not a deviation.
**Pre-registrant:** Pablo Ulpiano González Castro
**Status:** Locked at tag `v0.39-prereg-r1` on 2026-11-08 with the pre-registrant's approval. No study probe was sent before lock.
**Pre-lock feasibility check (non-acquisition):** on 2026-11-08 (06:06 UTC) each of the nine panel models received one neutral, non-category prompt ("Reply with the single word: ready"), and each current-arm model received two neutral search-enabled prompts (today's date; the current BBC headline). All 15 calls returned ok; served snapshots are recorded in §4.3. Claude Opus 5.5 and GPT-6 Astra searched on both S1 prompts; Gemini 4 Argon answered the date prompt without searching and searched on the second (3 queries, 5 sources). Record: `osf/v39/prereg/feasibility_v0_39.json`. No study probe was sent.
**Acquisition deadline:** acquisition must finish before 2026-11-24, the earliest possible retirement of Claude Opus 4.5 (M1). Claude Sonnet 4.5 (M2) is deprecated, with retirement scheduled (tentatively) for 2026-11-30.

---

## §1 Strategic context

v0.38 (Aillio-focal home roasters) confirmed both governing hypotheses at the focal-brand level — `H_Tier` CONFIRMED, `H_Default` CONFIRMED — while its lead test, `H_LegacySlot`, was UNDETERMINED because no panel model knew the successor generation; `MC_Boundary` passed. v0.38 asked whether a recommendation slot attaches to a superseded product. v0.39 asks a question v0.38 could not: **what does AI retrieval do to a brand whose whole proposition is that a category barrier no longer applies?**

Bellwether Coffee sells an all-electric shop roaster that, per its own specifications, needs no external exhaust, ductwork or gas line (an internal afterburner treats smoke and VOCs). In-café roasting has traditionally required exactly those three things. Two outcomes follow from the governing hypotheses:

1. **H2 at the frame level.** If AI answers to "should my café roast in-house?" present venting and gas as part of the job and never raise a ventless option, the category frame itself works against the brand before any brand is named.
2. **H1 at the CEP level.** If AI names Bellwether only when the buyer already states the constraint (no gas line, no venting, smoke, air-quality rules), the brand is retrievable only through its defining category entry point, by buyers who already know to ask.

The case has four further features:

1. **A dated generation ladder.** Original roaster (US launch 2018; "Series 1"; Bellwether ended technical and software support on 2026-01-01) → Series 2 (February 2022; 2.7 kg / 6 lb) → Shop Roaster (announced 2024-03-07; 1.5 kg / 3.3 lb) → the new Shop Roaster (announced 2026-10-15; public debut at Coffee Fest Dallas-Fort Worth, 2026-10-17/18; first deliveries Q1 2027).
2. **Codable generation tokens.** "Series 1" / "Series 2" against "Shop Roaster" (§3.4).
3. **The legacy panel straddles the Shop Roaster.** GPT-4o and GPT-4o-mini (October 2023 cutoff) predate its announcement; the other four legacy models postdate it. All three current-arm models postdate the Shop Roaster and predate the 2026 model in their documented cutoffs, so the 2026 model can reach an answer only through retrieval (S1).
4. **A physical-availability anchor.** Bellwether debuted the new Shop Roaster at Coffee Fest Dallas-Fort Worth 2026 (booth DE 210), one of six roasting-machine makers on that floor. The show floor gives an externally defined physical-availability set against which AI availability can be compared (D5).

**Exploratory motivation (declared).** A re-read of v0.38's 132 panel answers, outside v0.38's pre-registered analyses and using this registry and lexicons, found: Bellwether (v0.38 registry R27) named in 0 of 132 answers, including 0 of the 36 prosumer / micro-roastery answers; the venting lexicon (§5.5) matched in 22 of those 36; the ventless lexicon matched in 0 of 132. These counts motivated `H_Frame` and informed its thresholds (§2.3). v0.39 collects new data with a new battery; no v0.38 response enters any v0.39 statistic.

---

## §2 Pre-registered hypotheses

### §2.1 Lead: `H_CEP` (H1 Conditional Reweighting, focal)

**Statement.** Bellwether Presence is higher when the café buyer states the infrastructure constraint (tier C) than when the buyer does not (tier G).

**Operationalisation.** Legacy arm (L). Presence = share of ok responses that mention Bellwether under the audited coding of §3.3. Δ = Presence(C) − Presence(G), pooled over the six models (each contributes 6 G and 6 C responses, so pooling weights models equally).

**Test.** One-sided stratified permutation test; tier labels permuted within model (preserving each model's 6/6 split); 10,000 permutations; seed 39; p = (1 + #{Δ_perm ≥ Δ_obs}) ÷ 10,001.

**Verdict rule.** CONFIRMED if Δ ≥ 0.20 and p < 0.05 · PARTIAL if 0 < Δ < 0.20 and p < 0.05 · UNDETERMINED if Δ > 0 and p ≥ 0.05 · FALSIFIED if Δ ≤ 0.

**Reported alongside.** Presence in G and C separately; model-level Δ and the count of models with Δ > 0; the same contrast in the current arm, S0 and S1 (descriptive).

### §2.2 Supporting: `H_CEPDefault` (H2 Default Reinforcement inside the CEP)

**Statement.** Under constraint framing, Bellwether is the most-surfaced brand in the registry.

**Operationalisation.** Presence(C) for every registry brand, legacy arm, pooled over models (n = 36 responses).

**Verdict rule.** CONFIRMED if Bellwether ranks 1 and its margin over rank 2 ≥ 0.10 · PARTIAL if Bellwether ranks 1 (or ties for 1) with margin < 0.10 · FALSIFIED if Bellwether does not rank 1. A Presence of zero cannot rank 1, even if every brand is at zero.

**Reported alongside.** First-mention share and mean first-mention position in C; the same ranking in the current arm, S0 and S1.

### §2.3 Supporting: `H_Frame` (H2 Default Reinforcement at the frame level)

**Statement.** When a café owner asks whether and how to roast in-house, answers present venting as part of the job and do not raise a ventless option.

**Operationalisation.** Tier F, legacy arm (n = 36 responses). VentShare = share of responses with at least one venting-lexicon match (§5.5). VentlessShare = share with at least one ventless-lexicon match.

**Verdict rule.** CONFIRMED if VentShare ≥ 0.50 and VentlessShare ≤ 0.10 · PARTIAL if exactly one of the two conditions holds · FALSIFIED if neither holds.

**Declared.** Both thresholds were set after the exploratory re-read in §1 (0.61 and 0.00 on a different battery).

**Reported alongside.** The audited classification of every F response (§5.7): venting presented as required; venting presented as machine-dependent; ventless option named (with brand); infrastructure not discussed. The same statistics for the current arm, S0 and S1.

### §2.4 Supporting: `H_Search` (retrieval arm)

**Statement.** Web search raises Bellwether Presence in café recommendation answers from current assistants.

**Operationalisation.** Current arm; G ∪ C probes; 3 models × 12 probes = 36 cells, each observed in S0 and S1. Δ = Presence(S1) − Presence(S0).

**Test.** One-sided exact McNemar test: with b = cells where Bellwether appears in S1 only and c = cells where it appears in S0 only, p = P(X ≥ b), X ~ Binomial(b + c, 0.5). If b + c = 0, p = 1.

**Verdict rule.** CONFIRMED if Δ ≥ 0.20 and p < 0.05 · PARTIAL if 0 < Δ < 0.20 and p < 0.05 · UNDETERMINED if Δ > 0 and p ≥ 0.05 · FALSIFIED if Δ ≤ 0.

**Reported alongside.** Per-model Δ; the same contrast for G and C separately.

### §2.5 Manipulation checks

- **`MC_Constraint`.** The constraint prompts shift the frame: VentlessShare(C) − VentlessShare(G) ≥ 0.20, legacy arm, pooled (n = 36 each). If failed, `H_CEP` and `H_CEPDefault` are computed as specified and reported with a note that the constraint did not move the frame.
- **`MC_Boundary`.** The two pre-boundary models (GPT-4o, GPT-4o-mini) do not name the Shop Roaster: across all 30 probes, the share of their Bellwether-mentioning, generation-specified responses coded Shop-only or Both is ≤ 0.10, or no Shop token is attributed at all. If failed, the pre/post contrasts in D1 are withdrawn from interpretation.

### §2.6 Pre-registered descriptives (no verdicts)

- **D1 Generation knowledge.** Generation codes (§3.4) for K1, K2 and K4 and for every recommendation response that mentions Bellwether, per model, boundary group and condition. Shop-aware model: a model whose K1 or K2 response is coded Shop-only or Both. LegacyShare = PreShop-only ÷ generation-specified responses from Shop-aware models (the v0.38 `H_LegacySlot` statistic, carried as a descriptive). Share of responses that name Series 1, which has been unsupported since 2026-01-01.
- **D2 Grounding.** Audited accuracy of Bellwether facts against §3.5: K3 ventilation answer (correct = no external venting, ductwork or gas line; incorrect = venting or a hood required; hedged); K5 batch capacity against the generation named; power-requirement claims wherever stated.
- **D3 Claim reproduction.** Whether responses that name Bellwether reproduce its uniqueness claim (the only ventless or smokeless commercial roaster), qualify it, or contradict it.
- **D4 Ventless attribution.** Brands other than Bellwether described as ventless, smokeless or needing no venting; audited against the manufacturer's published specification where one exists (§3.5), otherwise labelled unverifiable.
- **D5 Show floor vs. AI shelf.** In G ∪ C ∪ R responses, by arm and condition: share of responses naming at least one show-floor (S) brand; share of all registry-brand mentions going to S brands; Presence of each S brand against the most-surfaced non-S brands.
- **D6 Category structure.** Presence for every registry brand by tier, arm, condition and model; first-mention position.
- **D7 Retrieval traces (S1).** Searches per response; cited domains; share of S1 responses citing bellwethercoffee.com; share citing coverage of the 2026-10-15 launch; 2026-model markers (§3.4) in K1 and K2.
- **D8 Legacy brands.** Presence of the historic registry brands (Jabez Burns, Royal, Sivetz) and whether each mention flags that the machines are vintage or no longer made (±150 characters).
- **D9 Price caveat.** Share of Bellwether-mentioning recommendation responses with a price or cost statement within ±200 characters of a Bellwether mention.
- **D10 Five-model sensitivity (declared limitation).** Gemini 2.5 Flash (M5) spends internal thinking tokens against the same 2,048-token cap as its visible answer; in v0.38, 19 of its 22 answers ended at the cap (v0.38 DEVIATIONS, Note 1), so M5 Presence is a lower bound. `H_CEP` (Δ and p), `H_CEPDefault` (rank and margin) and `H_Frame` (both shares) are also reported for the legacy arm without M5, with the share of M5 answers that end at the cap. Verdicts stay on the six-model panel.

### §2.7 Regime classification

Commercial coffee roasters is classified **a priori as Regime 3** (scale-mismatch; descriptive only) under the v1.2 taxonomy, and no Trends-based regime test is run. Several registry names are ordinary words or collide with unrelated entities (Bellwether, Stronghold, North, Primo, Royal, ARC, Lilla), and business-to-business search volume for most registry brands is too thin for keyword-unambiguous Google Trends proxies. This is a design decision, not a deviation.

---

## §3 Brand registry

### §3.1 Construction rule

36 brands in four strata, built mechanically from four external routes (snapshot 2026-11-08). A brand's stratum is its first qualifying route in the order S, A, M, D.

- **S — Show floor.** Every roasting-machine maker, or its exclusive distributor, on the Coffee Fest Dallas-Fort Worth 2026 exhibitor list (139 exhibitors).
- **A — AI shelf.** v0.38 registry brands in the prosumer and commercial-spillover segments, plus unregistered commercial roaster brands named in v0.38's 132 panel answers.
- **M — Market.** Manufacturers with a brand collection page in the Coffee Equipment Pros "Roasters by Manufacturer" index — the marketplace of the distributor that exhibited Air-Motion on the show floor. One-off product listings are excluded.
- **D — Claim holders.** Makers whose own materials market in-store or on-site retail roasting, found in the pre-lock fact check.

Strata enter only D5. Segments (shop, production, sample, micro, in-store retail, legacy) are labels for reporting only and enter no test. Unregistered roaster brands found during the coder audit are logged descriptively (§5.7) and enter no test.

**Resolved at lock (2026-11-08).** The pre-registrant kept the show-floor stratum as listed (six brands): Toper (Coffee Equipment Pros also demos Toper drums) stays in A, Sonofresco (owned by Coffee Holding, booth DE 420) stays in D, and Wiltronic Corporation is not added. Brands marked "to verify" keep that status label; segment and status labels enter no test.

### §3.2 Registry

| ID | Brand | Stratum | Segment | Status |
|---|---|---|---|---|
| B01 | **Bellwether** (focal) | S | shop | active |
| B02 | Aillio | S | micro | active |
| B03 | Air-Motion Roasters | S | production | active |
| B04 | Loring | S | production | active |
| B05 | Mill City Roasters | S | production | active |
| B06 | Stronghold | S | shop | active |
| B07 | Diedrich | A | production | active |
| B08 | San Franciscan | A | production | active |
| B09 | Probat | A | production | active |
| B10 | Giesen | A | production | active |
| B11 | US Roaster Corp | A | production | active |
| B12 | Ikawa | A | sample | active |
| B13 | Roest | A | sample | active |
| B14 | Coffee-Tech Engineering | A | shop | active |
| B15 | Kaleido | A | micro | active |
| B16 | Santoker | A | micro | active |
| B17 | Toper | A | production | active |
| B18 | Has Garanti | A | production | active |
| B19 | BC Roasters | A | micro | to verify |
| B20 | Buckeye | A | production | to verify |
| B21 | North | A | micro | to verify |
| B22 | Ambex | M | production | active |
| B23 | ARC | M | sample | to verify |
| B24 | Joper | M | production | active |
| B25 | Lilla | M | production | active |
| B26 | Öztürkbay | M | production | active |
| B27 | Petroncini | M | production | active |
| B28 | Primo | M | production | to verify |
| B29 | Proaster | M | production | to verify |
| B30 | Trabattoni | M | production | to verify |
| B31 | Vittoria | M | production | to verify |
| B32 | Jabez Burns | M | legacy | historic |
| B33 | Royal | M | legacy | historic |
| B34 | Sivetz | M | legacy | to verify |
| B35 | Sonofresco | D | in-store retail | active |
| B36 | Java Master | D | in-store retail | active |

Show-floor notes: Bellwether DE 210; Aillio DE 225; Air-Motion DE 332 (exhibited by its exclusive North American distributor, Coffee Equipment Pros); Stronghold via RoasTronix, its US distributor.

### §3.3 Collision policy

Alias patterns, case sensitivity and context exclusions are locked in the registry artefact (§3.6). Two exceptions to the v0.38 rule that confirmatory tests use the locked automated coding unaltered:

- **Bellwether (B01) and Stronghold (B06)** are matched case-sensitively, and **every match for these two brands is audited** before scoring. A match is removed if and only if it is a common-noun use ("an industry bellwether", "a stronghold of specialty coffee"). Confirmatory statistics use the audited coding for these two brands and the locked automated coding for all others. No other audit change enters a verdict. The audit is recorded in `osf/v39/data/v39_audit_commonnoun.json`, which lists every response containing a B01 or B06 match and the match offsets judged common-noun uses; until that file covers every such response, the scoring script writes all verdicts as PROVISIONAL.
- Collision-prone names elsewhere (North, Primo, Royal, ARC, Vittoria, Burns) match only with a model number or a "roaster" context, so that Royal Coffee (green-coffee importer) and Vittoria Coffee (coffee brand) are not read as roaster makers.

Test bed (declared, not a study analysis): run over v0.38's 132 answers, the registry aliases produced no false positives on manual inspection of the collision-prone brands, and no prompt in §4 matches any brand alias except K1–K6, which match Bellwether only (`scripts/check_registry_v0_39.py`).

### §3.4 Bellwether generation coding

- **Anchor:** "Bellwether" (case-sensitive).
- **Pre-Shop tokens:** Series 1, Series 2, Series One, Series Two (case-insensitive); "original Bellwether (roaster)".
- **Shop tokens:** "Shop Roaster" (case-sensitive, so the generic phrase "shop roaster" is not read as the product name).
- **2026-model markers (D7 only):** "new Shop Roaster", "deep bronze", "Q1 2027", "Coffee Fest Dallas/DFW", "Bellwether app".
- **Attribution rule:** a token is attributed to Bellwether if an anchor ends within the 60 characters preceding it and no other registry brand alias occurs between that anchor and the token (v0.38 rule).
- **Response codes:** PreShop-only, Shop-only, Both, Unspecified (Bellwether mentioned, no attributed token), Absent.

### §3.5 Grounding fact sheet

- **Shop Roaster:** 1.5 kg (3.3 lb) per batch; 3–4 roasts per hour; 200–240 VAC single phase, 30 A circuit, 5 kW, NEMA L6-30P plug; no external exhaust, ductwork or gas line (internal afterburner); UL 197, UL 710, NSF 4, CE.
- **Series 2:** 2.7 kg (6 lb) per batch; 240 V single phase or 208 V three phase, 50 A circuit.
- **Series 1:** original roaster, US launch 2018; Bellwether technical and software support ended 2026-01-01.
- **New Shop Roaster (2026):** announced 2026-10-15; public debut at Coffee Fest Dallas-Fort Worth, booth 210; first deliveries Q1 2027; no specifications in the launch release.
- **Competitor specification used in D4:** Air-Motion's AMR12 specification lists an exhaust exit pipe (247 mm), so it is a vented machine.

### §3.6 Registry artefact

`osf/v39/registries/brands_commercial_roasters_v0.39.json`, built from the v0.38 registry by `scripts/build_registry_v0_39.py`; checksum in `osf/v39/prereg/LOCK_MANIFEST_v0_39.sha256`.

---

## §4 Probe battery and acquisition

### §4.1 Frame and recommendation battery (24 probes; verbatim)

| ID | Tier | Prompt |
|---|---|---|
| F1 | Frame | I own a coffee shop. Should we start roasting our own coffee in-house? |
| F2 | Frame | What do I need to start roasting coffee inside my café? |
| F3 | Frame | What are the requirements for installing a coffee roaster in a café? |
| F4 | Frame | Is it realistic for a small café to roast its own beans? |
| F5 | Frame | How much does it cost to start roasting coffee in a café? |
| F6 | Frame | We want to roast coffee in our retail store where customers can watch. What's involved? |
| G1 | Café | What's the best coffee roaster for a café? |
| G2 | Café | I run a coffee shop and want to roast our own beans. Which roaster should I buy? |
| G3 | Café | Can you recommend a commercial coffee roaster for a small café? |
| G4 | Café | Which roaster should a café buy to roast about 50 pounds of coffee a week? |
| G5 | Café | What shop roasters do café owners recommend? |
| G6 | Café | We have two cafés and want to roast for both locations. What roaster should we get? |
| C1 | Constraint | What's the best coffee roaster for a café that doesn't have a gas line? |
| C2 | Constraint | Can you recommend a coffee roaster we can use in our café without installing ventilation or ductwork? |
| C3 | Constraint | We lease our café space and can't vent through the roof. What roaster options do we have? |
| C4 | Constraint | Which commercial coffee roaster produces the least smoke for roasting indoors in a café? |
| C5 | Constraint | Our city has strict air-quality rules. Which roaster can we use to roast in our shop? |
| C6 | Constraint | What's the best electric coffee roaster for a coffee shop? |
| R1 | Roastery | What's the best production coffee roaster for a growing specialty roastery? |
| R2 | Roastery | We roast about 500 pounds of coffee a week and need a bigger roaster. What should we buy? |
| R3 | Roastery | Which commercial coffee roasters are the most reliable for a wholesale roastery? |
| R4 | Roastery | What's the most energy-efficient, lowest-emission production coffee roaster? |
| R5 | Roastery | Which roaster should a new roasting company buy to supply local cafés and grocery stores? |
| R6 | Roastery | What do professional roasters consider the best commercial coffee roaster on the market? |

No F, G or R probe names a brand, a heating method, a venting arrangement or a batch size that singles out the focal brand. C probes state a buyer's constraint in buyer language and never use the words "ventless" or "smokeless". R is a contrast tier in which Bellwether is not expected to lead.

### §4.2 Bellwether probes (6 probes; verbatim)

| ID | Purpose | Prompt |
|---|---|---|
| K1 | Knowledge | What is Bellwether Coffee's newest roaster? |
| K2 | Knowledge | Which coffee roasters does Bellwether Coffee currently sell? |
| K3 | Grounding | Does the Bellwether coffee roaster need ventilation? |
| K4 | Brand-cued choice | I've decided to buy a Bellwether roaster for my café. Which model should I get? |
| K5 | Grounding | How much coffee can a Bellwether roaster roast per batch? |
| K6 | Claim reproduction | How is Bellwether's coffee roaster different from other commercial roasters? |

### §4.3 Panel

**Legacy arm (L)** — unchanged from v0.38.

| Slot | Model | API id | Served snapshot (2026-11-08) | Documented knowledge cutoff | Shop Roaster boundary (2024-03-07) |
|---|---|---|---|---|---|
| M1 | Claude Opus 4.5 | claude-opus-4-5 | claude-opus-4-5-20251101 | May 2025 (reliable knowledge) | post |
| M2 | Claude Sonnet 4.5 | claude-sonnet-4-5 | claude-sonnet-4-5-20250929 | Jan 2025 (reliable knowledge) | post |
| M3 | GPT-4o | gpt-4o | gpt-4o-2024-08-06 | Oct 2023 | pre |
| M4 | GPT-4o-mini | gpt-4o-mini | gpt-4o-mini-2024-07-18 | Oct 2023 | pre |
| M5 | Gemini 2.5 Flash | gemini-2.5-flash | gemini-2.5-flash | Jan 2025 | post |
| M6 | Gemini 2.5 Flash-Lite | gemini-2.5-flash-lite | gemini-2.5-flash-lite | Jan 2025 | post |

**Current arm (C)** — each provider's flagship model, each observed in two conditions.

| Slot | Model | API id | Served snapshot (2026-11-08) | Documented knowledge cutoff |
|---|---|---|---|---|
| C1 | Claude Opus 5.5 | claude-opus-5-5 | claude-opus-5-5 | Jun 2026 (reliable knowledge) |
| C2 | GPT-6 Astra | gpt-6-astra | gpt-6-astra | 2026-04-30 |
| C3 | Gemini 4 Argon | gemini-4-argon | gemini-4-argon | not documented |

The three current-arm ids are served without a dated snapshot suffix, so exact replication of C1–C3 depends on the providers keeping these versions in service.

All current-arm models postdate the Shop Roaster; all documented cutoffs predate the 2026 model (2026-10-15).

**Conditions.** S0: no tools. S1: the provider's own web search —
- Anthropic Messages API: `{"type": "web_search_20250305", "name": "web_search", "max_uses": 5, "user_location": {"type": "approximate", "country": "US"}}` (basic version, without dynamic filtering);
- OpenAI Responses API: `{"type": "web_search", "search_context_size": "medium", "user_location": {"type": "approximate", "country": "US"}}`, with `include: ["web_search_call.action.sources"]`;
- Google Gemini API: the `google_search` grounding tool at provider defaults.

### §4.4 Decoding and call policy

- **Legacy arm:** temperature 0.0; max output 2,048 tokens; a single user turn with no system prompt; one call per probe × model; 30 × 6 = **180 calls**.
- **Current arm:** temperature and reasoning effort left at provider defaults (not set); max output 16,384 tokens, because reasoning tokens count against the output limit on some providers; no system prompt; one call per probe × model × condition; 30 × 3 × 2 = **180 calls**. S1 records every tool call, search query, consulted source and citation.
- **HTTP timeout:** 600 s per current-arm call. A grounded Gemini 4 Argon answer took 57 s in the recorded feasibility check and 224 s in an earlier, superseded run of the same check, so the full acquisition is expected to take one to three hours.
- **Total: 360 calls.** Order: probes in battery order (F1 … R6, K1 … K6); within each probe, M1 … M6, then C1 … C3 in S0, then C1 … C3 in S1. Every call is independent (no conversation state). Transient errors (rate limit, 5xx, connection, timeout) retry up to 3 times with exponential backoff. An empty reply is retried once; if still empty the cell is missing, excluded from denominators and logged in DEVIATIONS. An Anthropic `pause_turn` stop is continued once with identical tools and logged. Each record stores the served model id, finish reason, token usage (including reasoning tokens), attempt count, UTC timestamps and the prompt's sha256.

### §4.5 Acquisition artefact

`scripts/acquire_v0_39.py`, forked from `scripts/acquire_v0_38.py`. The three legacy-arm call functions are identical to v0.38 (checked by source comparison); current-arm and S1 adapters are added, and `--feasibility` sends only the neutral prompts of the pre-lock check. The probe file's per-prompt sha256 values and call count are verified at run time. Raw output: `osf/v39/data/v39_raw.json`.

---

## §5 Analysis plan

### §5.1 Mention detection
As v0.38: registry aliases matched as regular expressions with the case sensitivity stated per alias; a match is discarded if one of the brand's context exclusions occurs within the stated window; Presence is binary per response × brand. Bellwether and Stronghold matches then pass through the audit of §3.3.

### §5.2 Presence, ranking and first mention
Presence(brand, tier, arm, condition) = share of ok responses in the cell that mention the brand, pooled over models and also reported per model. First-mention position is the rank of a brand's earliest match among the registry brands mentioned in the response.

### §5.3 Generation coding
Per §3.4, applied to every ok response. Shop-awareness, LegacyShare, the boundary statistic and D1 are computed exactly as defined in §2.

### §5.4 Tests
`H_CEP`: stratified permutation test (§2.1). `H_Search`: exact one-sided McNemar test (§2.4). `H_CEPDefault`, `H_Frame`, `MC_Constraint` and `MC_Boundary`: threshold rules on point estimates; Wilson 95% intervals reported as descriptives.

### §5.5 Frame lexicons (case-insensitive; locked in the registry artefact)
- **Venting:** vent / vents / vented / venting / ventilation / ventilate(d); exhaust(s); duct / ducts / ducting / ductwork; chimney(s); flue(s); afterburner(s); catalytic; hood(s).
- **Ventless:** ventless; vent-free; smokeless; smoke-free; zero emission(s); "no / without (any) / without the need for (external / outside) venting, ventilation, vent(s), ducting, ductwork, ducts, exhaust, chimney or hood"; "does not / doesn't / do not / don't / won't / will not / never need(s) or require(s) (any / an) (external / outside) venting, ventilation, vent(s), ducting, ductwork, exhaust, chimney or hood"; "no need for / to (a) vent, venting, ventilation, ducting, ductwork or exhaust".
- Lexicon matches are mention-level. Whether a response affirms or denies that a ventless option exists is reported from the audit (§5.7), not from the lexicon.

### §5.6 Descriptives
D1–D10 as in §2.6. D2: the K3 code is audited; K5 capacity is the largest quantity stated within ±200 characters of a Bellwether anchor, converted to kg and compared with the generation named (1.4–1.6 kg = Shop Roaster; 2.5–2.9 kg = Series 2). D7 domains are taken from provider citation and source fields, not from response text. Gemini grounding links are Google redirect URLs whose title carries the source domain, so the title is used for those; OpenAI real-time feeds (for example `oai-time`) are recorded by name and carry no domain.

### §5.7 Coder audit
After scoring and before the report is drafted, the analyst reads (a) every response that mentions Bellwether or Stronghold (binding for those two brands, §3.3); (b) all K responses, 6 probes × 12 model-conditions = 72, for D1–D3; (c) all F responses (36 legacy, 18 current S0, 18 current S1) for the frame classification of §2.3. For everything except (a), confirmatory verdicts use the locked automated coding; if disagreement exceeds 10% of audited responses it is reported in DEVIATIONS with a sensitivity re-computation, and verdicts are not changed. Unregistered roaster brands noticed during the audit are logged descriptively.

### §5.8 Scoring artefact
`scripts/score_v0_39.py` and `scripts/test_score_v0_39.py` (synthetic fixtures only; no study data; the tests exercise the collision rules, generation coding, lexicons, both tests, the audit gate and missing-cell handling), locked at the pre-registration tag with checksums in `osf/v39/prereg/LOCK_MANIFEST_v0_39.sha256`. Scoring runs once on the acquired data; any later change to scoring code is a DEVIATIONS entry with both results reported.

---

## §6 Contingencies

- **§6.1 Model unavailable during acquisition** (including the retirement of M1 or M2). Logged; analyses run on the remaining models and denominators shrink. If M1 and M2 are both unavailable, `H_CEP` is computed on the four remaining legacy models, and the report says so.
- **§6.2 Search behaviour in S1.** An S1 response in which the model chose not to search is kept as recorded; not searching is part of the condition. Tool errors are retried as transient errors; a persistent failure is a missing cell.
- **§6.3 Manipulation check fails.** As §2.5.
- **§6.4 Changes.** Any change to probes, registry, coding or thresholds before acquisition requires a new revision tag (`v0.39-prereg-r2`); after acquisition it is a DEVIATIONS entry. Tags are additive-only.
- **§6.5 Second wave.** The identical battery is re-run once, on both arms, in April–May 2027, after Bellwether's first Q1 2027 deliveries, as `v0.39-w2`. Its contrasts are pre-registered in an addendum deposited at OSF before that acquisition. A legacy model retired by then is reported as missing, not replaced.
- **§6.6 Known truncation.** Gemini 2.5 Flash answers that end at the 2,048-token cap are expected (D10) and are not a deviation; decoding stays as locked.

---

## §7 Declarations

- **Conflict of interest.** The pre-registrant is employed by Samsung Electronics America (unrelated to this substrate; standing declaration). The pre-registrant owns an Aillio Bullet R1; Aillio is a registry brand (show-floor stratum). The pre-registrant met Bellwether staff at Coffee Fest Dallas-Fort Worth 2026 and receives Bellwether marketing email; he has no commercial relationship with Bellwether or any registry brand. Bellwether did not commission, fund or review this study. Any later sharing of results with registry brands does not alter this pre-registration.
- **Funding.** Self-funded.
- **Ethics.** Not applicable; no human subjects; public model APIs, including the providers' own web search tools.

---

## §8 Deliverables

Raw responses including search traces (JSON); coded response and mention tables (CSV); verdicts (JSON); figures; brand-format report (PDF, Bellwether-focal). The SSRN paper and the post-acquisition OSF deposit follow the programme workflow and require the pre-registrant's go.

---

## §9 Sign-off

Approved for lock by the pre-registrant, 2026-11-08.

### Sources cited in this pre-registration
- Bellwether Coffee, "Bellwether Roaster Specifications" (published 2026-02-13, modified 2026-06-19): https://bellwethercoffee.com/blog/bellwether-shop-roaster-specifications ; Shop Roaster technical specifications (PDF): https://bellwethercoffee.com/s/Bellwether-Shop-Roaster-Technical-Specifications.pdf
- Bellwether Coffee, FAQ (Series 1 end of support; Series 2 power): https://bellwethercoffee.com/faq ; Series 2: https://bellwethercoffee.com/series-2 (accessed 2026-11-08)
- Sprudge, "Bellwether Announces New Smaller Footprint Shop Roaster" (2024-03-07): https://sprudge.com/bellwether-announces-new-smaller-footprint-shop-roaster-233800.html
- Sprudge, "Bellwether Debuts New Shop Roaster As Data Shows Cafés Can Cut Coffee Costs In Half By Roasting In-House" (2026-10-15): https://sprudge.com/bellwether-debuts-new-shop-roaster-as-data-shows-cafes-can-cut-coffee-costs-in-half-by-roasting-in-house-1457452.html
- Daily Coffee News, Bellwether Series 2 (2022-02-15): https://dailycoffeenews.com/2022/02/15/bellwether-coffee-launches-second-generation-of-its-innovative-roasting-system ; Global Coffee Report / BeanScene, Bellwether funding and US launch (2019-09-05)
- Kokoquest, Coffee Fest Dallas Fort Worth 2026 exhibitor list (accessed 2026-11-08): https://www.kokoquest.com/tradeshows/coffee-fest-dallas-fort-worth-2026
- Coffee Equipment Pros, Roasters by Manufacturer index (accessed 2026-11-08): https://coffeeequipmentpros.com
- Daily Coffee News, "From South Africa, Air-Motion Roasters Makes Its Move in the US" (2025-05-29); Air-Motion AMR12 specification page
- Perfect Daily Grind, co-roasting spaces / RoasTronix (2023-09-11): https://perfectdailygrind.com/2023/09/co-roasting-spaces-specialty-coffee/
- Coffee-Tech Engineering, https://www.coffee-tech.com/llms.txt ; Java Master (BusinessWire; CSNews); Sonofresco (Benzinga; Daily Coffee News 2014-01-22 and 2020-01-17)
- Anthropic, model deprecations and models overview; web search tool documentation (accessed 2026-11-08)
- OpenAI, models catalogue (GPT-6 Astra; knowledge cutoff 2026-04-30) and web search tool guide (accessed 2026-11-08)
- Google, Gemini models (Gemini 4 Argon) and Grounding with Google Search documentation (accessed 2026-11-08)
