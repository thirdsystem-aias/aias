# AIAS™ Presence Measurement Protocol — Pre-Registration v0.38 (revision r1)

**Substrate:** Home coffee roasters — consumer and prosumer machines for residential use (batch ≤ ~1.2 kg)
**Design:** Focal-brand designed-for-test inside a full category registry (v0.7 lineage). Focal brand: Aillio (Bullet).
**Programme position:** Moves the phantom line (v0.6 → v0.7 → v0.23 → v0.35) from the brand level to the product-generation level; first focal-brand test of H1 Conditional Reweighting and H2 Default Reinforcement; first Grounding pilot.
**Protocol version:** Presence definitions per Methodology v1.2 (SSRN 6761698); panel and decoding conventions per v0.17–v0.23 (six-model panel; temperature 0.0; max output 2,048 tokens; one call per probe × model).
**Lock target:** git tag `v0.38-prereg-r1` on branch `v0.38`; the tag is pushed to `origin` and this pre-registration is deposited at OSF `ec6wh` → `v38/prereg/` before any study probe is sent.
**Pre-registrant:** Pablo Ulpiano González Castro
**Pre-lock feasibility check (non-acquisition):** on 2026-11-07 each panel model received one neutral, non-category prompt ("Reply with the single word: ready") to confirm it is still served. Served snapshots are recorded in §4.3. No study probe was sent before lock.

---

## §1 Strategic context

The programme's phantom line has so far been tested at the brand level. v0.6 found Mint at 44% Presence 25 months after decommissioning. v0.7 (designed-for-test) found Bed Bath & Beyond at 38.2% against Pier 1 at 0.0%; manual valence review showed 88% of BBB mentions carried evidence that the model knew the entity had changed and surfaced it anyway — the phantom is a recommendation slot, not a knowledge gap. v0.23 (SSRN 6834298) located a boundary: defunct corporate automotive brands surfaced zero times across unprompted recall opportunities while living heritage brands surfaced at elevated rates — phantom persistence has a living-brand boundary. v0.35 (SSRN 6921758) carried the naive-phantom question into the Consistency component.

All of these tests ask whether a brand's slot outlives the brand. v0.38 asks the next question inside the living-brand boundary: **does a recommendation slot attach to a superseded product generation of a brand that is alive and selling its successor?**

The Aillio Bullet is an unusually clean case:

1. **Living brand, active successor.** Aillio introduced the Bullet R2 and R2 Pro in July 2024; its CEO described the R2 as a completely new machine relative to the original induction-heated 1 kg Bullet that debuted in 2015 (Daily Coffee News, 2024-07-03).
2. **Codable identifiers.** Generations carry explicit model names (R1, R1 V2, R2, R2 Pro) that can be coded from free text without semantic judgement.
3. **A staggered, not total, transition.** Sweet Maria's (US) lists the R2 and R2 Pro as its two Bullet versions; some non-US retailers still list the R1 V2 (Green Coffee Collective, UK; Di Pacci, AU); and Sweet Maria's own R2 Pro page still recommends the R1 for less experienced roasters. The R1 is therefore a **legacy generation**, not a phantom, and is coded and reported as such.
4. **The panel straddles the change.** GPT-4o and GPT-4o-mini carry an October 2023 knowledge cutoff, before the R2 announcement. Claude Sonnet 4.5 (reliable knowledge cutoff January 2025), Claude Opus 4.5 (May 2025) and Gemini 2.5 Flash / Flash-Lite (January 2025) postdate it. The two pre-boundary models are a built-in no-knowledge control.

The substrate also supports a focal test of the governing hypotheses. Home roasting has two discourse worlds: commission-supported "best home coffee roaster" listicles built around entry machines (Fresh Roast, Behmor, Amazon-native brands), and enthusiast forums where the Bullet is commonly described as the home standard. H1 (Conditional Reweighting) predicts that expertise and scale cues in the prompt reweight retrieval toward the enthusiast default; H2 (Default Reinforcement) predicts that, inside the enthusiast frame, the default is surfaced first and most.

Finally, the focal design makes a first Grounding pilot cheap: the Bullet's heating method (induction) and batch capacity (1 kg; 1.2 kg for the R2 Pro) are hard, checkable facts.

---

## §2 Pre-registered hypotheses

### §2.1 Lead: `H_LegacySlot`

**Statement.** Among panel models that demonstrably know the R2 exists, unprompted recommendations that name a specific Aillio generation name only the superseded R1 at least half the time.

**Operationalisation.**
- *R2-aware model:* a model whose response to K1 or K2 (§4.2) names the R2 family (R2 or R2 Pro) under the attribution rule of §3.3.
- *Analysis set:* responses to the 18 recommendation probes (§4.1) from R2-aware models in which Aillio is mentioned and at least one generation token is attributed to Aillio.
- *LegacyShare* = R1-only ÷ (R1-only + R2-only + Both) in the analysis set. A response naming both generations counts against legacy (conservative).

**Verdict rule.** CONFIRMED if LegacyShare ≥ 0.50 · PARTIAL if 0.20 ≤ LegacyShare < 0.50 · FALSIFIED if LegacyShare < 0.20 · UNDETERMINED if the analysis set has n < 10 or no panel model is R2-aware.

**Reported alongside.** Per-model LegacyShare; Wilson 95% interval for the pooled share; the same statistic for the pre-boundary pair (control).

### §2.2 Supporting: `H_Tier` (H1 Conditional Reweighting, focal)

**Statement.** Aillio Presence is higher under enthusiast and prosumer framing than under beginner framing.

**Operationalisation.** Presence = share of recommendation responses that mention Aillio. Δ = Presence(E ∪ P) − Presence(B), pooled over the six models (each model contributes 6 B and 12 E ∪ P responses, so pooling weights models equally).

**Test.** One-sided stratified permutation test; tier labels permuted within model (preserving each model's 6/12 split); 10,000 permutations; seed 38; p = (1 + #{Δ_perm ≥ Δ_obs}) ÷ 10,001.

**Verdict rule.** CONFIRMED if Δ ≥ 0.20 and p < 0.05 · PARTIAL if 0 < Δ < 0.20 and p < 0.05 · UNDETERMINED if Δ > 0 and p ≥ 0.05 · FALSIFIED if Δ ≤ 0.

**Reported alongside.** Presence in B, E and P separately; model-level Δ and the count of models with Δ > 0.

### §2.3 Supporting: `H_Default` (H2 Default Reinforcement, focal)

**Statement.** Under enthusiast and prosumer framing, Aillio is the most-surfaced brand in the registry.

**Operationalisation.** Presence(E ∪ P) for every registry brand, pooled over models (n = 72 responses).

**Verdict rule.** CONFIRMED if Aillio ranks 1 and its margin over rank 2 ≥ 0.10 · PARTIAL if Aillio ranks 1 (or ties for 1) with margin < 0.10 · FALSIFIED if Aillio does not rank 1.

**Reported alongside.** First-mention share (share of E ∪ P responses in which Aillio is the first registry brand named) and Aillio's mean first-mention position.

### §2.4 Manipulation check: `MC_Boundary`

**Statement.** The two pre-boundary models (GPT-4o, GPT-4o-mini) do not name the R2 family.

**Operationalisation.** Across all 22 probes, the share of their Aillio-mentioning, generation-specified responses that name the R2 family (R2-only or Both). Pass if the share ≤ 0.10, or if no R2-family token is attributed at all. Neither pre-boundary model is expected to be R2-aware.

**If failed.** The pre/post contrast is withdrawn from interpretation (§6.3); `H_LegacySlot` is still computed as specified.

### §2.5 Pre-registered descriptives (no verdicts)

- **D1 Brand-cued choice (K3):** the generation each model recommends once the buyer has chosen Aillio (automated generation code plus analyst audit of the recommended model).
- **D2 Discontinuation knowledge (K4):** whether each model states that the R1 has been superseded or discontinued ("Superseded"), states it is current ("Current"), or neither ("Unclear").
- **D3 Knowledge–recommendation gap:** per model and per boundary group, the R2-naming rate in K1/K2 minus the R2-naming rate among generation-specified recommendation responses.
- **D4 Grounding pilot:** accuracy of heating-method and maximum-batch claims attached to Aillio in recommendation responses, against the fact sheet in §3.3. Automated extraction proposes candidates; the report uses the audited classification (§5.6).
- **D5 Price caveat:** share of Aillio-mentioning recommendation responses with a price or expense caveat within ±200 characters of an Aillio mention.
- **D6 Category structure:** Presence for every registry brand by tier and by model; first-mention position.
- **D7 Brand-level phantom comparators:** Presence of the two discontinued registry brands (Hearthware i-Roast; Nesco) in recommendation responses, and whether each mention flags discontinuation within ±150 characters.

### §2.6 Regime classification

Home coffee roasters is classified **a priori as Regime 3** (scale-mismatch; descriptive only) under the v1.2 taxonomy, and no Trends-based regime test is run. Fewer than ten registry brands have keyword-unambiguous Google Trends proxies: several names are ordinary words or collide with unrelated entities (Fresh Roast; Roest, Dutch for rust; Stronghold; Quest; Nucleus; Kaldi, the coffee-origin legend; Skywalker; Nesco, a small-appliance brand). This is a design decision, not a deviation.

---

## §3 Brand registry

### §3.1 Construction logic

32 brands in five descriptive segments: home-entry, enthusiast, prosumer, commercial spillover, discontinued. Segments are labels for reporting only and enter no test. Alias patterns, case sensitivity and context exclusions are locked in the registry artefact (§3.4); post-acquisition alias amendments are not permitted for confirmatory tests. Unregistered roaster brands found during the coder audit are logged descriptively (§5.6) and enter no test.

### §3.2 Registry

| ID | Brand | Segment | Status |
|---|---|---|---|
| R01 | **Aillio** (focal) | prosumer | active |
| R02 | Hottop | enthusiast | active |
| R03 | Kaffelogic | enthusiast | active |
| R04 | Behmor | home-entry | active |
| R05 | Fresh Roast | home-entry | active |
| R06 | Gene Cafe | enthusiast | active |
| R07 | Ikawa | prosumer | active |
| R08 | Roest | prosumer | active |
| R09 | Stronghold | prosumer | active |
| R10 | Nucleus (Link) | enthusiast | active |
| R11 | Kaleido | prosumer | active |
| R12 | Huky | enthusiast | active |
| R13 | Quest (M3s) | enthusiast | active |
| R14 | Sandbox Smart | enthusiast | active |
| R15 | Kaldi | enthusiast | active |
| R16 | Nuvo Eco | home-entry | active |
| R17 | Santoker | prosumer | active |
| R18 | Skywalker | enthusiast | active |
| R19 | Coffee-Tech Engineering | prosumer | active |
| R20 | Sweet Maria's Popper | home-entry | active |
| R21 | Diedrich | commercial spillover | active |
| R22 | Mill City Roasters | commercial spillover | active |
| R23 | San Franciscan | commercial spillover | active |
| R24 | Probat | commercial spillover | active |
| R25 | Giesen | commercial spillover | active |
| R26 | Loring | commercial spillover | active |
| R27 | Bellwether | commercial spillover | active |
| R28 | US Roaster Corp | commercial spillover | active |
| R29 | Hearthware (i-Roast) | discontinued | discontinued |
| R30 | Nesco | discontinued | discontinued (CR-1010 in 2014; CR-04-13 recalled 2021) |
| R31 | Jiawanshun | home-entry | active (Amazon-native) |
| R32 | DYVEE | home-entry | active (Amazon-native) |

### §3.3 Aillio generation coding and Grounding fact sheet

- **Anchors:** "Aillio" (and the misspellings Ailio, Aillo, Allio), and capitalised "Bullet".
- **R1-family tokens:** R1, V1, V2, Classic (case-sensitive). **R2-family tokens:** R2, R2 Pro (case-sensitive).
- **Attribution rule:** a token is attributed to Aillio if an anchor ends within the 60 characters preceding it and no other registry brand alias occurs between that anchor and the token. (This prevents, for example, Sandbox Smart R2 from being read as an Aillio R2.)
- **Response codes:** R1-only, R2-only, Both, Unspecified (Aillio mentioned, no attributed token), Absent.
- **Fact sheet (D4):** heating = induction (all generations); maximum batch = 1 kg / 2.2 lb (R1, R1 V2, R2) and 1.2 kg / 2.65 lb (R2 Pro). Sources: Daily Coffee News (2024-07-03); Sweet Maria's Aillio Bullet product page and Coffee Library (accessed 2026-11-07).

### §3.4 Registry artefact

`osf/v38/registries/brands_home_roasters_v0.38.json` — checksum in `osf/v38/prereg/LOCK_MANIFEST_v0_38.sha256`.

---

## §4 Probe battery and acquisition

### §4.1 Recommendation battery (18 probes; verbatim)

| ID | Tier | Prompt |
|---|---|---|
| B1 | Beginner | What's the best home coffee roaster? |
| B2 | Beginner | I want to start roasting my own coffee beans at home. Which roaster should I buy? |
| B3 | Beginner | Can you recommend a good coffee roaster for home use? |
| B4 | Beginner | What are the best coffee roasters for beginners? |
| B5 | Beginner | I'm new to home roasting. What roaster would you suggest I start with? |
| B6 | Beginner | I'm thinking about buying a coffee roaster for my kitchen. What are my best options? |
| E1 | Enthusiast | I'm an experienced home roaster looking to upgrade. Which roaster should I get? |
| E2 | Enthusiast | What's the best home coffee roaster for someone who wants full control over roast profiles? |
| E3 | Enthusiast | Which home coffee roasters do serious hobbyists recommend? |
| E4 | Enthusiast | I'm an espresso enthusiast and want to roast my own beans. Which roaster is best? |
| E5 | Enthusiast | Money isn't the main concern. What's the best home coffee roaster I can buy? |
| E6 | Enthusiast | What do advanced home roasters consider the best roaster on the market? |
| P1 | Prosumer | What's the best roaster for starting a small coffee roasting business from home? |
| P2 | Prosumer | Can you recommend a small-batch roaster for a home-based micro-roastery? |
| P3 | Prosumer | Which compact roaster should I buy to start selling my coffee at farmers markets? |
| P4 | Prosumer | What roaster would you recommend for sample roasting at a small café? |
| P5 | Prosumer | I roast about 5 kg a week for friends and family and want something more professional. Which roaster should I buy? |
| P6 | Prosumer | What roaster should I buy to scale up from home roasting to supplying a small café? |

No probe names a brand, a heating method or a batch size that singles out the focal brand.

### §4.2 Aillio probes (4 probes; verbatim)

| ID | Purpose | Prompt |
|---|---|---|
| K1 | Knowledge | What is the newest Aillio Bullet roaster model? |
| K2 | Knowledge | Which coffee roaster models does Aillio currently sell? |
| K3 | Brand-cued choice | I've decided to buy an Aillio Bullet. Which model should I get? |
| K4 | Discontinuation knowledge | Is the Aillio Bullet R1 still in production? |

### §4.3 Panel

| Slot | Model | API id | Served snapshot (2026-11-07) | Documented knowledge cutoff | Boundary |
|---|---|---|---|---|---|
| M1 | Claude Opus 4.5 | claude-opus-4-5 | claude-opus-4-5-20251101 | May 2025 (reliable knowledge) | post |
| M2 | Claude Sonnet 4.5 | claude-sonnet-4-5 | claude-sonnet-4-5-20250929 | Jan 2025 (reliable knowledge) | post |
| M3 | GPT-4o | gpt-4o | gpt-4o-2024-08-06 | Oct 2023 | pre |
| M4 | GPT-4o-mini | gpt-4o-mini | gpt-4o-mini-2024-07-18 | Oct 2023 | pre |
| M5 | Gemini 2.5 Flash | gemini-2.5-flash | gemini-2.5-flash | Jan 2025 | post |
| M6 | Gemini 2.5 Flash-Lite | gemini-2.5-flash-lite | gemini-2.5-flash-lite | Jan 2025 | post |

Boundary = position of the documented cutoff relative to the R2 announcement (2024-07-03). Anthropic lists Claude Opus 4.5 as active (legacy) with retirement not sooner than 2026-11-24; exact replication on M1 may become impossible after that date.

### §4.4 Decoding and call policy

Temperature 0.0; max output 2,048 tokens; a single user turn with no system prompt; one call per probe × model; 22 × 6 = **132 calls**. Order: probes in battery order (B1 … P6, K1 … K4), models M1 … M6 within each probe; every call is independent (no conversation state). Transient errors (rate limit, 5xx, connection, timeout) retry up to 3 times with exponential backoff. An empty reply is retried once with identical configuration; if still empty the cell is recorded as missing, excluded from denominators and logged in DEVIATIONS. Each record stores the served model id, finish reason, token usage, attempt count, UTC timestamps and the prompt's sha256.

### §4.5 Acquisition artefact

`scripts/acquire_v0_38.py` (forked from `osf/v23/scripts/acquire_v0_23.py`; decoding unchanged); probes in `osf/v38/prereg/probes_v0_38.json` with per-prompt sha256, verified at run time. Raw output: `osf/v38/data/v38_raw.json`.

---

## §5 Analysis plan

### §5.1 Mention detection
Registry aliases are matched as regular expressions with the case sensitivity stated per alias; a match is discarded if one of the brand's context exclusions occurs within the stated window. Presence is binary per response × brand.

### §5.2 Presence, ranking and first mention
Presence(brand, tier) = share of ok recommendation responses in the tier that mention the brand, pooled over models and also reported per model. First-mention position is the rank of a brand's earliest match among the registry brands mentioned in the response.

### §5.3 Generation coding
Per §3.3, applied to every ok response (recommendation and Aillio probes). R2-awareness, LegacyShare, the control statistic and D3 are computed exactly as defined in §2.

### §5.4 Tests
`H_Tier`: stratified permutation test as in §2.2. `H_Default` and `H_LegacySlot`: threshold rules on point estimates as in §2.3 and §2.1; intervals are descriptive.

### §5.5 Descriptives
D1–D7 as in §2.5. D4 heating: "induction" within ±200 characters of an Aillio anchor = correct; another heating term without "induction" = incorrect candidate. D4 batch: the largest quantity stated within ±200 characters of an Aillio anchor, converted to kg; 0.9–1.3 kg = correct, otherwise incorrect candidate. D5 and D7 windows as stated in §2.5.

### §5.6 Coder audit
After scoring and before the report is drafted, the analyst reads (a) all 24 Aillio-probe responses and (b) every recommendation response that mentions Aillio, and records agreement with the automated generation code. Confirmatory verdicts use the locked automated coding. If disagreement exceeds 10% of audited responses it is reported in DEVIATIONS with a sensitivity re-computation; verdicts are not changed. D1 and D4 are reported from the audited classification. Unregistered roaster brands noticed during the audit are logged descriptively.

### §5.7 Scoring artefact
`scripts/score_v0_38.py` and `scripts/test_score_v0_38.py` (synthetic fixtures only; no study data) are locked at the pre-registration tag; checksums in `osf/v38/prereg/LOCK_MANIFEST_v0_38.sha256`. Scoring runs once on the acquired data; any later change to scoring code is a DEVIATIONS entry with both results reported.

---

## §6 Contingencies

- **§6.1 Model unavailable during acquisition.** Logged; analyses run on the remaining models and denominators shrink accordingly.
- **§6.2 No R2-aware model.** `H_LegacySlot` = UNDETERMINED; D3 is reported as the finding (recommendations of the R1 would then be knowledge-bounded, not slot persistence).
- **§6.3 `MC_Boundary` fails.** The pre/post contrast is withdrawn from interpretation and noted in the report.
- **§6.4 Changes.** Any change to probes, registry, coding or thresholds before acquisition requires a new revision tag (`v0.38-prereg-r2`); after acquisition it is a DEVIATIONS entry. Tags are additive-only.

---

## §7 Declarations

- **Conflict of interest.** The pre-registrant is employed by Samsung Electronics America (unrelated to this substrate; standing declaration). The pre-registrant owns an Aillio Bullet R1 (first generation) and has no commercial relationship with Aillio or any registry brand. Aillio did not commission, fund or review this study.
- **Funding.** Self-funded.
- **Ethics.** Not applicable; no human subjects; public model APIs.

---

## §8 Deliverables

Raw responses (JSON); coded response and mention tables (CSV); verdicts (JSON); figures; brand-format report (PDF). The SSRN paper and the post-acquisition OSF deposit follow the programme workflow and require the pre-registrant's go.

---

## §9 Sign-off

Approved for lock by the pre-registrant, 2026-11-07.

### Sources cited in this pre-registration
- Daily Coffee News, "Aillio fires off two new Bullet roasters: the R2 and R2 Pro" (2024-07-03): https://dailycoffeenews.com/2024/07/03/aillio-fires-off-two-new-bullet-roasters-the-r2-and-r2-pro
- Sweet Maria's, Aillio Bullet: https://www.sweetmarias.com/roasting/drum-roasters/aillio-bullet.html ; R2 Pro: https://www.sweetmarias.com/aillio-bullet-r2-pro-roaster.html
- Green Coffee Collective (UK), Aillio Bullet R1 V2: https://greencoffeecollective.com/products/aillio-bullet-r1
- Di Pacci (AU), coffee roasters: https://dipacci.com.au/collections/coffee-roasters
- Anthropic platform documentation, Claude Opus 4.5 model overview (knowledge cutoffs and retirement date; accessed 2026-11-07)
- Google Cloud, Gemini 2.5 Flash / Flash-Lite model pages (knowledge cutoff January 2025)
- OpenRouter, GPT-4o (2024-08-06): https://openrouter.ai/openai/gpt-4o-2024-08-06
- Sweet Maria's Coffee Library, Hearthware glossary entry; Daily Coffee News (2021-04-22), Nesco recall
