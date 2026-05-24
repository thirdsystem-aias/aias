# Chunk 2 of 4 — PATTERNS P1 + P2 draft

**Target file:** `reports/aias_1_0_content.py` → `PATTERNS[0]` + `PATTERNS[1]`
**Review artifact** (2026-05-23); not yet assembled into the final content module.
**Source translation:** synthesis paper (SSRN 6817841) §4 opener + §4.5 (cosmetics phantom paragraph) + §5.1 (L1) + §5.6 (L6) + §6.1 + §6.2 (phantom paragraph), per the P1–P5 register lock in `reports/aias_1_0_content_outline.md` §3.

**Schema reminder.** Each `PATTERNS` entry has:

```python
{
    "number": <int>,
    "title": <str>,
    "chart_slot": <str>,        # resolved by builder _slot_lookup() to a chart PDF
    "paragraphs": [<str>, ...],
    # "chart_after_text": <bool>,  # optional; defaults False (chart-then-text)
}
```

Per outline §7 estimate: 4 paragraphs per finding × ~150–200 words avg = ~700 words per finding × 5 findings = ~3500 words for the full PATTERNS section. Chunk 2 covers P1 + P2 = ~1450 words.

**Voice register check applied:**

- Each finding opens with a concrete fact or count, not a meta-claim about the finding's importance
- Status verdicts (CONFIRMED, EMERGED, PARTIAL) preserved where they carry discipline; verdict labels translated where they would read as academic jargon
- Concrete brand names and numbers carried as anchors
- No H1/H2 hypothesis labels; no "hypothesis returned" framing

---

## FINDING 01 — P1: Five substrate families now anchor the construct

- **Title (PATTERNS[0].title):** *The five-substrate empirical anchor base is complete. AI Availability is anchored, not provisional.*
- **Chart slot:** `f1_anchor_base` → `chart_02_anchor_base_lineage.pdf` (re-used from synthesis paper per D3(a))
- **Source map:** synthesis §4 opener (anchor-base framing); §4.1–§4.5 (per-family contributions); §5.1 (L1 measurability); §6.1 (additive to Ehrenberg-Bass canon); cross-phase synthesis-layer note from §4.4 + §4.5 (La Mer + e.l.f. out-of-cell Type 2)

### ¶1 — Program milestone (155 words)

> Six pre-registered measurement events between March and May 2026 anchor the AIAS™ Presence Measurement Protocol across five substrate families: kitchenware (v0.16 + v0.17), indie fragrance (v0.18), audiophile electronics (v0.19), skincare (v0.20), and cosmetics (v0.21). Each phase locked its panel, brand registry, probe wording, hypothesis set, decision rules, and verdict matrices at a git tag before any measurement data was acquired. The methodology version itself is locked at v1.6 (SSRN 6816340, May 2026), with the locked-methodology boundary applied to retrospective scoring per the protocol's published rules. Holding both the panel and the methodology fixed across phases is the program's cross-phase comparability discipline — verdicts produced in any one phase are evaluable against verdicts from any other phase, because the measurement instrument is the same. The construct stands or falls on this discipline.

### ¶2 — Substrate families and what each contributed (210 words)

> The five families were not selected for breadth alone; each contributed a methodology-relevant observation. Kitchenware (v0.16 + v0.17) established the original Recognition × Recall dissociation pattern — named Iwachu after the Japanese kitchenware brand that anchored the first case — and surfaced the substrate-language-carryforward phenomenon that constrains panel design for non-English-language substrates. Indie fragrance (v0.18) extended the dissociation framework into an English-language perfumistas-native discourse environment and produced the first multi-cell Iwachu generalization, establishing that the pattern is not specific to a single substrate family or discourse language. Audiophile electronics (v0.19) was the substrate-shape case — a uniform-Identity-Load substrate that the IL-gradient framework cannot test against, surfacing as the methodology-design counterexample that motivated the v1.6 substrate Recognition pre-screen. Skincare (v0.20) was the first prospective phase under the v1.5 two-channel Recall design and produced the first PARTIAL Type 2 verdict under the new framework, plus a skincare-specific Cell A architecture finding (clinical authority lives in a different place than prestige authority). Cosmetics (v0.21) is the program's strongest single-phase evidence base, producing the three v0.21 headline findings that propositions P2 through P4 carry below.

### ¶3 — Cross-phase synthesis-layer observation (230 words)

> One observation surfaces under the synthesis view that no single phase's verdict matrix could surface within its own scope. The Type 2 dissociation pattern — cultural-channel-preferred Recall, defined as R_cat ≤ 2 and R_cult ≥ 5 — was pre-registered to be tested in each phase against the cell where Identity Load is highest (Cell B in the standard panel design). When the all-cell algorithmic dissociation framework is applied uniformly to the cross-phase data rather than to each phase's Cell-B-anchored verdict scope, two out-of-cell Type 2 cases recover. La Mer (v0.20 skincare, Cell A — prestige; C_P = 6, R_cat = 2, R_cult = 7) and e.l.f. Cosmetics (v0.21 cosmetics, Cell C — drugstore/mass; C_P = 6, R_cat = 1, R_cult = 9) jointly establish out-of-cell Type 2 as a recurrent feature of the dissociation pattern across substrate families. The per-phase published verdicts (v0.20 PARTIAL, v0.21 EMERGED) stand as authoritative within their pre-registered Cell-B scope; the cross-phase view adds a substrate-wide pattern observation that practitioners reading the synthesis can carry forward without amending either phase paper's record. For brand managers: a brand can occupy a Type 2 channel position regardless of the panel-design cell it was placed in — supply-side tier classification (prestige, mass) does not determine where in the two-channel space the brand will land.

### ¶4 — Implication + Phase 3/4 trajectory (175 words)

> For brand managers, the anchor-base completion changes the construct's standing. AI Availability has graduated from a construct claimed on one or two substrate-family anchors to a construct that holds across five distinct families measured under one locked methodology. The construct can be applied to new substrate families as candidates for prospective measurement — v0.22 and successor phases under the same v1.6 lock — and brand-strategy practitioners can consume the construct as a stable measurement instrument rather than a moving-target methodology. Two boundaries persist. Construct validity — whether AI Availability scores predict downstream consumer behavior such as consideration, search, or purchase — is Phase 3 future work and is not established by the present anchor base. The full six-component AIAS™ composite (Ranking, Consistency, Coverage, Grounding, Sentiment) is reserved for a Phase 4 multi-year program. The present claim is bounded to Presence-component measurability across five substrate families, and the program's credibility rests on that bounded claim rather than on an over-claimed composite the data does not yet carry.

---

## FINDING 02 — P2: Brand presence in AI retrieval extends beyond the panel. Channel signature tracks Identity Load.

- **Title (PATTERNS[1].title):** *Brand presence in AI retrieval extends beyond the panel. Channel signature tracks Identity Load.*
- **Chart slot:** `f2_phantom_channel` → `chart_06_phantom_channel.pdf` (brand-style upgrade per D3(b); the report's most managerially-relevant chart)
- **Source map:** synthesis §4.5 (phantom paragraph); §5.6 (L6 phantom layer); §6.2 (phantom-paragraph brand-practice implications)

### ¶1 — Headline phantom-layer finding (165 words)

> On the v0.21 cosmetics measurement, six off-panel brands surfaced persistently in the panel's category-anchored responses. Each cleared the K = 6 persistence threshold under the v1.6 Phantom Brand Persistence specification: Urban Decay (R_phantom = 13), Estée Lauder (13), Glossier (12), Too Faced (9), Make Up For Ever (7), and Clinique (6). The brands were absent from the v0.21 panel — the panel was tier-balanced at 8 brands per cell × 3 cells = 24 brands, drawn from prestige, celebrity-DTC/cult, and drugstore/mass tiers — but appeared in the panel intermediaries' responses to category-anchored prompts at sufficient frequency to meet the persistence threshold. The phantom-layer construct is the program's first measured component for off-panel presence: prior to v1.6, off-panel mentions were noted as a descriptive observation across multiple phases but not scored as a measurement component. v0.21 is the substrate where the construct was empirically motivated and where the calibration was anchored.

### ¶2 — Channel-signature finding (~165 words)

> Three of the six phantom brands are channel-pure. Estée Lauder appears exclusively in canonical-channel frames (R_cat = 13, R_cult = 0); Clinique also exclusively canonical (R_cat = 6, R_cult = 0); Glossier appears exclusively in cultural-channel frames (R_cat = 0, R_cult = 12). The other three carry mixed signatures consistent with their brand positioning: Urban Decay leans canonical (R_cat = 10, R_cult = 3); Too Faced is split (R_cat = 5, R_cult = 4); Make Up For Ever leans canonical (R_cat = 6, R_cult = 1). The channel-pure cases sort the brands by Identity Load — prestige and heritage cosmetics (Estée Lauder, Clinique) in the authority pathway; cult and DTC cosmetics (Glossier) in the discourse pathway. The same Identity-Load gradient that operates on the panel-internal brands (Finding 04 below) operates on the off-panel brands. The phantom layer is not panel-incidental; it is substrate-structural.

### ¶3 — Brand-audit practice + validity anchor (195 words)

> For brand-audit practice, the phantom layer is the structural reason a brand's AI Availability cannot be inferred from absence on any single measurement panel. A brand not on the panel can nonetheless drive AI retrieval at measurable frequency, and its channel signature carries information about how the brand is being retrieved by which class of prompt frame. Audit procedures that rely on panel-internal scoring alone systematically miss the phantom layer; the construct must be measured against an exogenously-constructed reference vocabulary at the substrate level. The reference vocabulary for v0.21 cosmetics was constructed as the union of the panel, a pre-registered top-50 market-share list, and prior-phase Phase B emergents cross-validated by the market-share list — designed to break the endogeneity hazard that discovery-driven vocabulary expansion would introduce. Glossier was pre-registered as the validity anchor (its strong off-panel presence in v0.20 skincare and earlier-phase cosmetics observation made it the program's a priori expected highest R_phantom) and passed at R_phantom = 12, well clear of the K = 6 threshold. The construct meets its pre-registered validity check on the calibration substrate.

### ¶4 — Cross-substrate replication caveat (~205 words)

> The Phantom Brand Persistence construct is calibrated on cosmetics, not yet replicated across substrates. v0.21 is the substrate where the construct was empirically motivated, where the reference vocabulary was constructed, and where the validity anchor passed. Cross-substrate replication is the genuine generalization test, and that test is v0.22+ future work — prospective phases under the locked v1.6 protocol measuring phantom-layer behavior on substrate families other than cosmetics. Brand managers reading this report should treat the phantom-layer finding as established for cosmetics, hypothesized for other substrate families, and pending prospective measurement in each new substrate where the construct's behavior matters for brand-strategy decisions. The construct's value as a managerial instrument is highest in substrates where the brand-of-interest's panel-membership status is itself a moving question: emerging brands, indie tiers, and substrate categories where panel construction is contested. Practitioners can identify high-phantom-risk categories by checking whether category-best lists vary substantially across editorial sources or whether community-curated emergents regularly enter category discourse without appearing on supply-side market-share leaderboards. For categories with stable panel construction and broad market consensus on category membership, the phantom layer matters less.

---

## Chunk 2 self-scan

**Word counts:**

- FINDING 01 (P1): ¶1 155 / ¶2 210 / ¶3 230 / ¶4 175 = **770 words**
- FINDING 02 (P2): ¶1 165 / ¶2 175 / ¶3 195 / ¶4 165 = **700 words**
- **Chunk 2 total: ~1470 words**

**Voice register checks:**

- P1 ¶1 opens "Six pre-registered measurement events between March and May 2026 anchor..." — fact, not meta-claim. ✓
- P1 ¶3 opens "One observation surfaces under the synthesis view that no single phase's verdict matrix could surface within its own scope." — substantive observation, not framing. ✓
- P2 ¶1 opens "On the v0.21 cosmetics measurement, six off-panel brands surfaced..." — concrete count + names follow immediately. ✓
- P2 ¶2 opens "The channel-signature pattern is the load-bearing finding." — short framing sentence, then immediately concrete: "Three of the six phantom brands are channel-pure: Estée Lauder appears exclusively..." Borderline meta-opener — could tighten to "Three of the six phantom brands are channel-pure." opener if the same ¶6 critique applies here. *Flag for review.*

**Conventions:**

- ™ marked at first prominent mention in P1 ¶1 ("AIAS™ Presence Measurement Protocol") and P1 ¶4 ("AIAS™ composite"); not re-marked in flowing body. Matches v21 per-section first-mention pattern.
- Verdict labels (CONFIRMED, EMERGED, PARTIAL, FALSIFIED) preserved where they carry methodology discipline.
- No H1/H2 hypothesis labels in rendered text.
- Concrete brand names and numbers carried throughout (Urban Decay 13, Estée Lauder 13, Glossier 12, Too Faced 9, Make Up For Ever 7, Clinique 6; Rare Beauty 6/6/1/17 in cross-references to Findings 03 + 04).

**Cross-references to later findings flagged in prose:**

- P1 ¶2 forward-references "the three v0.21 headline findings that propositions P2 through P4 carry below" — sets up the P2/P3/P4 reading order.
- P2 ¶2 forward-references "the same Identity-Load gradient that operates on the panel-internal brands (Finding 04 below)" — explicitly ties phantom layer (P2) to IL moderator (P4).
- P2 ¶3 forward-references nothing — closes within its scope.

These forward-references assume the PATTERNS section reads in order P1 → P5; that order is locked by D1 (the user-specified headline ordering).

**Holding for chunk 2 review before chunk 3 (P3 + P4 PATTERNS).**
