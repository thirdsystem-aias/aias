# AIAS™ v0.23 — Premium Spirits Mega-Prompt
# Protocol: v1.6 | Substrate family: 7 of N | Phase: Presence
# Pre-reg tag: v0.23-prereg-r1

---

## 1. Registry (24 brands)

| ID | Brand | Spirit type | Tier | Parent | Conglomerate flag |
|----|-------|------------|------|--------|-------------------|
| S01 | Johnnie Walker | Scotch blend | Global-dominant | Diageo | 1 |
| S02 | Hennessy | Cognac | Global-dominant | LVMH | 1 |
| S03 | Jack Daniel's | Tennessee whiskey | Global-dominant | Brown-Forman | 1 |
| S04 | Patrón | Tequila | Global-dominant | Bacardi Ltd. | 1 |
| S05 | Grey Goose | Vodka | Global-dominant | Bacardi Ltd. | 1 |
| S06 | Bacardi | Rum | Global-dominant | Bacardi Ltd. | 1 |
| S07 | Bombay Sapphire | Gin | Global-dominant | Bacardi Ltd. | 1 |
| S08 | Jameson | Irish whiskey | Global-dominant | Pernod Ricard | 1 |
| S09 | Lagavulin | Scotch single malt | Premium-enthusiast | Diageo | 1 |
| S10 | Clase Azul | Tequila | Premium-enthusiast | Independent | 0 |
| S11 | Hendrick's | Gin | Premium-enthusiast | William Grant & Sons | 0 |
| S12 | Woodford Reserve | Bourbon | Premium-enthusiast | Brown-Forman | 1 |
| S13 | Monkey 47 | Gin | Premium-enthusiast | Pernod Ricard | 1 |
| S14 | The Balvenie | Scotch single malt | Premium-enthusiast | William Grant & Sons | 0 |
| S15 | Rémy Martin | Cognac | Premium-enthusiast | Rémy Cointreau | 0 |
| S16 | Casamigos | Tequila | Premium-enthusiast | Diageo | 1 |
| S17 | Fortaleza | Tequila | Craft-cult-emerging | Independent | 0 |
| S18 | Compass Box | Scotch blend (craft) | Craft-cult-emerging | Independent | 0 |
| S19 | Nikka | Japanese whisky | Craft-cult-emerging | Asahi Group | 0 |
| S20 | Del Maguey | Mezcal | Craft-cult-emerging | Pernod Ricard | 1 |
| S21 | Fernet-Branca | Amaro | Craft-cult-emerging | Branca family | 0 |
| S22 | Redbreast | Irish whiskey | Craft-cult-emerging | Pernod Ricard | 1 |
| S23 | St. George Spirits | Multi-spirit craft | Craft-cult-emerging | Independent | 0 |
| S24 | Mezcal Vago | Mezcal | Craft-cult-emerging | Independent | 0 |

**Conglomerate coding rule:** Top-5 global spirits groups (Diageo, Pernod Ricard, Bacardi Ltd., LVMH/Moët Hennessy, Brown-Forman) = 1. All others = 0. Yields 14 conglomerate, 10 independent.

---

## 2. Model panel (fixed from v0.17)

| Slot | Model | Provider |
|------|-------|----------|
| M1 | Claude Opus 4.5 | Anthropic |
| M2 | Claude Sonnet 4.5 | Anthropic |
| M3 | GPT-4o | OpenAI |
| M4 | GPT-4o-mini | OpenAI |
| M5 | Gemini 2.5 Flash | Google |
| M6 | Gemini 2.5 Flash Lite | Google |

Temperature = 0.0 for all probes. Single-shot (no conversation history carried).

---

## 3. Phase A — Recognition (24 brands × 6 LLMs = 144 probes)

### Probe template

```
What do you know about {BRAND_NAME}? Specifically, I'm interested in it
as a premium spirits brand — its positioning, reputation, product range,
and how it fits within the broader {SPIRIT_TYPE} category. Please be
detailed and specific.
```

### Substitution

For each of the 24 registry entries, substitute `{BRAND_NAME}` and `{SPIRIT_TYPE}` from the registry. Send to each of the 6 models. Record full response text.

### Scoring (per Protocol v1.6 — substrate Recognition pre-screen)

Each response scored on a 4-level Recognition scale:

| Level | Label | Criterion |
|-------|-------|-----------|
| R3 | Rich recognition | Model produces ≥3 accurate, specific claims (e.g., distillery location, flagship expression, ownership history, tasting profile) |
| R2 | Basic recognition | Model produces 1–2 accurate specific claims; remainder is generic or hedged |
| R1 | Shallow recognition | Model acknowledges the brand exists but offers no specific claims or generates hedged/uncertain filler |
| R0 | Non-recognition | Model fails to identify the brand, confuses it with another entity, or declines to answer |

**Pre-screen gate (v1.6):** Brands scoring R0 across ≥5 of 6 models are flagged as below-threshold. They remain in the dataset for completeness but are excluded from the Presence composite score denominator to avoid floor-effect dilution.

---

## 4. Phase B — Two-channel Recall (6 probes × 6 LLMs = 36 queries)

Each query response scored against all 24 registry brands for mention/non-mention + slot position.

### Channel 1: Editorial-authority (3 probes)

**EA-1 — Critical consensus**
```
Which premium spirits brands are most highly regarded by leading spirits
critics and publications such as Whisky Advocate, Wine Enthusiast, or
The Spirits Business? I'm looking for brands that consistently receive
top ratings and critical acclaim across spirit categories. List specific
brands and explain why each is well-regarded.
```

**EA-2 — Awards authority**
```
What spirits brands have the strongest track record at major
international competitions — San Francisco World Spirits Competition,
International Wine & Spirit Competition (IWSC), International Spirits
Challenge? Name specific brands and describe their competitive record.
```

**EA-3 — Professional authority**
```
If I asked a professional bartender or spirits sommelier to recommend
premium spirits across categories — whisky, gin, tequila, vodka, rum,
cognac, mezcal — which brands would they most likely name? Give me
specific brand recommendations with reasoning.
```

### Channel 2: Cultural-cult (3 probes)

**CC-1 — Enthusiast community**
```
Which premium spirits brands have the most passionate and dedicated
enthusiast communities? I'm thinking of brands that inspire collector
behavior, bottle hunting, online forums, tasting groups, or cult-like
followings. Name specific brands and describe their community appeal.
```

**CC-2 — Cultural resonance**
```
Which spirits brands have transcended their product category to become
cultural phenomena — appearing in cocktail culture, media, lifestyle
contexts, or achieving iconic status? Name specific brands and explain
what makes them culturally significant beyond just being a good product.
```

**CC-3 — Insider discovery**
```
What premium spirits brands are considered hidden gems or insider picks
among serious spirits enthusiasts — the brands that knowledgeable
drinkers seek out but that aren't yet mainstream? Name specific brands
and explain what makes them special to those in the know.
```

### Recall scoring

For each of the 36 query responses, record:

1. **Mention binary** (0/1) — did brand appear by name in the response?
2. **Slot position** — ordinal rank of first mention within the response (1 = first brand named, 2 = second, etc.; 0 if not mentioned)
3. **Channel tag** — EA or CC per probe source
4. **Elaboration flag** (0/1) — did the model provide ≥1 specific claim about the brand beyond bare mention?

---

## 5. Hypotheses

### Standard set (carried from Protocol v1.6)

**H_Regime4** — Each of the 24 brands can be classified into one of four AI Presence regimes (Dominant, Established, Emerging, Absent) based on composite Recognition + Recall scoring. No regime is empty.

**H_RecognitionPrescreen** — The R0 pre-screen gate excludes ≤3 brands from the composite denominator (expectation: premium spirits has high baseline LLM familiarity; floor-effect exclusions should be rare).

**H_Phantom** — No phantom brands surface in this substrate (premium spirits registry contains no defunct brands). Phantom Brand Persistence is not directly testable in v0.23; hypothesis carried for protocol completeness.

**H_ILDirect** — Information Landscape Direct scores (derived from Phase A Recognition richness) correlate positively with Phase B Recall frequency (r ≥ 0.40, p < .05). Brands the models know more about are recommended more often.

**H_C2_TwoChannel** — The two recall channels (editorial-authority, cultural-cult) produce partially overlapping but non-identical brand sets. Measured via C2 statistic: overlap coefficient between EA-recalled and CC-recalled brand sets falls in range 0.30–0.80 (neither perfect overlap nor complete separation).

### Substrate-specific

**H_ConglomeratePortfolio** — Brands owned by top-5 global spirits conglomerates (conglomerate flag = 1, n = 14) show higher mean AI Presence composite scores than independent brands (flag = 0, n = 10). Tested via independent-samples t-test or Mann-Whitney U, α = .05. Directional prediction: conglomerate > independent, driven by training-corpus density from conglomerate-level media coverage and cross-brand portfolio mentions.

---

## 6. Falsification criteria

| Hypothesis | Falsified if |
|-----------|-------------|
| H_Regime4 | Any of the four regimes contains zero brands |
| H_RecognitionPrescreen | >3 brands excluded at R0 gate (would indicate substrate is too obscure for the model panel) |
| H_ILDirect | Correlation r < 0.40 or p ≥ .05 |
| H_C2_TwoChannel | Overlap coefficient < 0.30 (channels fully separate) or > 0.80 (channels redundant) |
| H_ConglomeratePortfolio | p ≥ .05 on group comparison, or direction reverses (independent > conglomerate) |

---

## 7. Predictions (directional, pre-registered)

P1. **High baseline recognition.** ≥20 of 24 brands score R2+ across majority of models. Premium spirits is a well-documented category; LLM training corpora are dense with spirits content.

P2. **Tier-aligned regime placement.** Global-dominant tier brands (S01–S08) cluster in Dominant/Established regimes. Craft-cult-emerging tier (S17–S24) shows wider regime dispersion (some Emerging, possibly one Absent).

P3. **Channel divergence on tier.** Editorial-authority channel favors Global-dominant and Premium-enthusiast tiers (award-winning, critically reviewed brands). Cultural-cult channel surfaces Craft-cult-emerging tier brands at higher relative frequency than EA channel does.

P4. **Mezcal/amaro as emergent edge.** Mezcal (S20 Del Maguey, S24 Mezcal Vago) and amaro (S21 Fernet-Branca) are the most likely candidates for Emerging regime or R0 pre-screen flag — subcategories with thinner training-corpus representation relative to whisky/gin/tequila.

P5. **Conglomerate lift.** Conglomerate-owned brands show 10–25% higher mean Presence composite than independents, consistent with corpus-density advantage.

---

## 8. Deviations log

| Entry | Date | Description |
|-------|------|-------------|
| — | — | No deviations at r1 |

If methodology defects are identified pre-acquisition, amend at r2 with Entry 0 documenting the change.
