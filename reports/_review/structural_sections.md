# Step 3 — Six structural content-module sections draft

**Target file:** `reports/aias_1_0_content.py` → COVER + LEAD_DECK + WHAT_WE_MEASURED + PROPOSITION_SCORING + PROPOSITION_DETAILS + CLOSING
**Review artifact** (2026-05-23); final content-module checkpoint before assembly + render.
**Source translation:** synthesis paper (SSRN 6817841) §1–§3 (program intro + methodology consolidation) + §7 (Phase 3/4 trajectory for CLOSING dataset references); outline §3 (P1–P5 lock); outline OD7 (cover hybrid subtitle).
**Voice register check applied:** Managerial throughout. ™ marked per CLAUDE.md per-section first-mention. No H1/H2 hypothesis labels. PROPOSITION_SCORING table column header "P" (set in builder per Step 2 fork).

**Cumulative content-module size after Step 3 lock:** ~6172 (chunks 1–4) + ~2900 (Step 3) = ~9070 words. Outline §7 target was 1500–2200 lines for the .py file; with Python string-literal wrapping (~3× word-count → line-count multiplier), estimated final size ~700–800 lines of constant declarations + ~200–300 lines of docstring/comments = **~900–1100 lines**, within the D5 band.

---

## SECTION 1 — COVER

**Schema:** `COVER = {"title", "subtitle", "date", "byline_short", "tagline"}` (dict literal; 5 string fields)

### COVER.title

> AI Availability as a Third Measurable Layer

Per outline OD7 (c) hybrid lock: title carries the third-layer construct claim directly. Title renders at 44pt cover_title style; ~43 chars at this length will wrap to 2 lines on cover page.

### COVER.subtitle

> Five-substrate empirical anchor base under locked methodology v1.6. The Presence component of the AIAS™ construct reaches its 1.0 milestone with cosmetics as the strongest single-phase evidence base: cultural-channel Recall populates the dissociation construct's third quadrant above threshold, Identity Load empirically tracks AI channel asymmetry at confidence-interval rigor, and off-panel brand presence enters as a measured component with channel signatures that track the same Identity-Load gradient as panel-internal brands.

73 words / ~525 chars. Renders at 18pt cover_subtitle style.

Carries (per OD7 hybrid spec): 1.0 milestone + third-layer claim (echoed from title) + five-family substrate breadth + the three v0.21 headline findings (Type 2 EMERGED + IL Direct + Phantom).

### COVER.date

> May 2026

### COVER.byline_short

> Pablo Ulpiano González Castro · Third System

### COVER.tagline

> Independent measurement for the AI mediation layer.

(Program-level tagline; unchanged from v21. Renders at 20pt cover_tagline style.)

---

## SECTION 2 — LEAD_DECK

**Schema:** `LEAD_DECK = <single string>` (one paragraph)

### LEAD_DECK body (~165 words)

> This report consolidates the AIAS™ Measurement Program's five-substrate empirical anchor base in five propositions for brand strategy and marketing-science practitioners. P1: AI Availability is now anchored across five substrate families — kitchenware, indie fragrance, audiophile electronics, skincare, and cosmetics — as a measurable third channel of brand presence. P2: brands not on a measurement panel can still drive AI retrieval, and their channel signature tracks Identity Load — Estée Lauder and Clinique canonical-pure, Glossier cultural-pure. P3: Recall splits into a canonical channel and a cultural channel that can be managed separately, with Rare Beauty's 1:17 R_cat:R_cult split as the textbook diagnostic. P4: Identity Load predicts which channel will lead, with cosmetics returning the program's first CONFIRMED moderator verdict at any layer. P5: methodology v1.6 closes the operational layer that makes P2 through P4 measurable.

Mirrors EXEC_SUMMARY ¶4 (P1–P5 overview) at the lead-spread layout's deck length. ~165 words ≈ v21 LEAD_DECK length.

---

## SECTION 3 — WHAT_WE_MEASURED

**Schema:** `WHAT_WE_MEASURED = {"heading": <str>, "paragraphs": [<str>, ...]}`

### WHAT_WE_MEASURED.heading

> What we measured

(Per outline OD3 lock: keep v21 section heading for scaffolding parity. The section's prose carries the synthesis-scope cue.)

### WHAT_WE_MEASURED.paragraphs (8 paragraphs / ~720 words)

**¶1 (~95 words) — Cumulative methodology framing**

> AIAS™ measures AI Availability through a pre-registered protocol that runs the same two-phase measurement against each new substrate family under a panel of six LLMs held fixed across the program. The protocol's specifications are locked at git tag at each new phase before any acquisition; the methodology version that governs scoring is itself locked at git tag before retrospective scoring is applied to any prior-phase corpus. The methodology version that governs the present synthesis is v1.6 (SSRN 6816340, May 2026).

**¶2 (~105 words) — Reference panel discipline**

> The reference panel is six LLMs locked at v0.17 and held constant across the program: Claude Opus 4.5, Claude Sonnet 4.5, GPT-4o, GPT-4o-mini, Gemini 2.5 Flash, and Gemini 2.5 Flash Lite. Holding the panel fixed across phases is the program's cross-phase comparability discipline — verdicts produced in any one phase are evaluable against verdicts from any other phase because the measurement instrument is the same. Per-LLM rankings and provider-level performance comparisons are not the program's subject; verdicts are properties of brand × substrate × panel triples evaluated under the same set of intermediaries each time.

**¶3 (~105 words) — Phase A Recognition**

> <b>Phase A — Recognition.</b> Each brand in the panel registry is presented to each of the six panel intermediaries with a category-membership probe (template locked at v1.4 specification): the model is asked whether the brand is commonly recognized as a member of the substrate's category, with a yes/no response. The brand's Recognition score C_P is the count of yes responses across the six panel intermediaries, range 0–6. C_P is the Recognition component of AI Availability — a brand with C_P = 6 is universally categorized by the panel; a brand with C_P = 0 is not categorized as a category member by any panel intermediary.

**¶4 (~110 words) — Phase B Recall + two-channel decomposition**

> <b>Phase B — Recall, two-channel decomposition.</b> Each panel intermediary receives a six-frame open-ended query battery against the substrate's category, and the panel's responses are scanned for brand mentions against the locked substrate registry. v1.5 introduced the two-channel decomposition: three frames anchor the canonical channel (R_cat — best brands, most-recommended brands, highest-quality brands; max 18 = 3 frames × 6 models) and three frames anchor the cultural channel (R_cult — most popular brands, celebrity-favorite brands, viral or cult-favorite brands; max 18). The two channels operate on disjoint inputs and can be managed separately at the brand-strategy intervention layer.

**¶5 (~115 words) — Three dissociation patterns**

> <b>Three dissociation patterns at the v1.5 thresholds.</b> Iwachu: high Recognition with sparse canonical Recall (C_P ≥ 5 ∧ R_cat ≤ 2) — named after the Japanese kitchenware brand that anchored the first case in v0.17. Type 1: canonical-channel-preferred (R_cat ≥ 5 ∧ R_cult ≤ 2) — prestige and authority-anchored brands cluster here. Type 2: cultural-channel-preferred (R_cat ≤ 2 ∧ R_cult ≥ 5) — celebrity-DTC and discourse-driven brands cluster here. The three patterns occupy the Recognition × Recall plane and bracket the dissociation construct's empirical geometry. v0.21 cosmetics is the first phase where Type 2 cleared the EMERGED threshold (three Cell B cases).

**¶6 (~135 words) — Methodology v1.6 three increments**

> <b>Methodology v1.6 — three increments.</b> First, a substrate-level Recognition pre-screen identifies substrates where every panel brand is categorically recognized in every cell (the cosmetics case) and routes them to a distinct verdict state preserving the substrate's evidentiary value at the moderator and phantom layers. Second, an independent moderator pathway evaluates Identity-Load asymmetry as δ = mean(R_cult) − mean(R_cat) per cell with 95% bootstrap confidence intervals (n = 10,000) and a monotonic-gradient check across cells. Third, the Phantom Brand Persistence Phase B extension scores off-panel brand presence against an exogenously-constructed reference vocabulary (union of the panel, a pre-registered top-50 market-share list, and prior-phase Phase B emergents cross-validated by the market-share list) with persistence threshold K = 6 and a pre-registered validity anchor.

**¶7 (~125 words) — Five substrate families with cell construction**

> <b>Five substrate families anchor the construct.</b> v0.16 kitchen knives and v0.17 premium kitchenware (kitchenware family — Cell A heritage, Cell B Japanese-cult, Cell C mass); v0.18 indie fragrance (Cell A heritage / niche, Cell B perfumista-cult, Cell C mass); v0.19 audiophile electronics (two-cell uniform-IL design — Heritage and Boutique, with audiophile-community curation producing the substrate-shape case the IL-gradient framework cannot test against); v0.20 skincare (Cell A heritage / clinical, Cell B celebrity-DTC, Cell C mass / drugstore); v0.21 cosmetics (Cell A prestige, Cell B celebrity-DTC / cult, Cell C drugstore / mass). Each phase locked its 24-brand panel — eight brands per cell × three cells, or twelve per cell × two cells for v0.19 — at pre-registration before any acquisition.

**¶8 (~115 words) — Pre-registration discipline (closing methodology beat)**

> <b>Pre-registration discipline.</b> Every phase enters the program under pre-registration. Panel construction, substrate registry, Phase A probe template, Phase B six-frame battery, hypothesis set, decision rules, and verdict matrices are locked ex-ante at a git tag (v0.NN-prereg-rN); the methodology version is locked at its own tag (v1.NN-prereg-rN). All artifacts — pre-registrations, acquisition data, scoring code, verdict outputs, reference vocabularies — are deposited under Open Science Framework project ec6wh (osf.io/ec6wh). The discipline is what allows the construct's verdicts to be falsifiable and the construct's measurability claim to stand or fall on its own evidence.

---

## SECTION 4 — PROPOSITION_SCORING

**Schema:** `PROPOSITION_SCORING = {"heading": <str>, "intro": <str>, "rows": [(p_id, proposition, result, status_text, status_class), ...]}`

### PROPOSITION_SCORING.heading

> Five propositions, anchored

### PROPOSITION_SCORING.intro (~75 words)

> Five propositions consolidate the five-substrate empirical anchor base into actionable framing for brand strategy. Each is anchored against the data the program has shipped under locked methodology v1.6. The table below states each proposition, the substantive evidence that anchors it, and the status as of the AIAS™ 1.0 milestone. The detailed interpretation of each — what it means, what it does not mean — follows in the section below the table.

### PROPOSITION_SCORING.rows (5 tuples / ~440 words)

**Row format:** `(p_id, proposition, result, status_text, status_class)` — five 5-tuples.

```python
[
    ("P1",
     "AI Availability is a measurable third channel of brand presence, "
     "anchored across five substrate families.",
     "Five families measured under one locked methodology version (v1.6, "
     "SSRN 6816340): kitchenware, indie fragrance, audiophile electronics, "
     "skincare, cosmetics. Six pre-registered measurement events March–May "
     "2026.",
     "ANCHORED",
     "confirmed"),

    ("P2",
     "Off-panel brand presence is real and tracks Identity Load. Brands "
     "not on a measurement panel can still drive AI retrieval with "
     "auditable channel signatures.",
     "Six off-panel cosmetics brands cleared K = 6. Estée Lauder + "
     "Clinique canonical-pure (R_cult = 0); Glossier cultural-pure "
     "(R_cat = 0). Glossier validity anchor passed at R_phantom = 12.",
     "CALIBRATED",
     "confirmed"),

    ("P3",
     "Recall splits into a canonical channel (R_cat) and a cultural "
     "channel (R_cult) that operate on disjoint inputs and can be managed "
     "separately.",
     "Rare Beauty textbook anchor: C_P = 6/6, R_cat = 1, R_cult = 17. "
     "Type 2 EMERGED with three Cell B cosmetics cases (Rare Beauty, "
     "Huda Beauty 0:11, Kylie Cosmetics 0:5).",
     "CONFIRMED",
     "confirmed"),

    ("P4",
     "Identity Load predicts the AI channel where a brand will surface. "
     "Cell position carries an expected channel asymmetry that the audit "
     "can compare brand performance against.",
     "v0.21 cosmetics returned the program's first CONFIRMED moderator at "
     "any layer. Cell B's cultural channel led by 7.13 mentions on average "
     "— the strongest IL-predicted asymmetry signal in the program. Cell A "
     "canonical-led by 3.13; Cell C balanced. All three cells matched the "
     "IL-gradient prediction with confidence-interval margin.",
     "CONFIRMED",
     "confirmed"),

    ("P5",
     "Methodology v1.6 closes the operational layer. Three increments "
     "shipped May 2026 make P2 through P4 measurable.",
     "Substrate Recognition pre-screen (Inc 1) + independent moderator "
     "pathway (Inc 2) + Phantom Brand Persistence (Inc 3). Each "
     "load-bearing for v0.21 verdicts.",
     "SHIPPED v1.6",
     "confirmed"),
]
```

All five rows render with status_class="confirmed" (bold status text in the rendered table). The synthesis-scale event is a consolidation of measurement wins; PARTIAL or NARROWED status would be a structural anomaly at this stage. Status vocabulary intentionally varied per proposition (ANCHORED, CALIBRATED, CONFIRMED, CONFIRMED, SHIPPED v1.6) so each P reads as anchored on its own evidence rather than as a uniform pass/fail block.

**Note on P4 status text:** keep the academic verdict label "CONFIRMED" because it carries discipline information (the program's verdict matrix is the construct's credibility instrument). The H_ prefix is dropped per register lock; "H_IdentityLoad_Direct CONFIRMED" in the result column reads as data provenance, not as academic-paper voice.

---

## SECTION 5 — PROPOSITION_DETAILS

**Schema:** `PROPOSITION_DETAILS = {"heading": <str>, "intro": <str>, "items": [(p_id, body_text), ...]}`

### PROPOSITION_DETAILS.heading

> Proposition interpretation

### PROPOSITION_DETAILS.intro (~55 words)

> Each proposition carries substantive interpretation beyond the table-row summary. The verdicts are what the data produced; the meaning of each verdict for the construct, the brand-strategy practitioner, and the v0.22+ trajectory is what the prose below addresses, structured as "What it means" + "What it doesn't mean" per proposition.

### PROPOSITION_DETAILS.items (5 tuples / ~1310 words)

**Item format:** `(p_id, body_text)` — five 2-tuples. Body uses `<b>What it means.</b>` / `<b>What it doesn't mean.</b>` markup (same pattern as v21 HYPOTHESIS_DETAILS).

**P1 item (~245 words)**

> <b>What it means.</b> AI Availability has graduated from a construct claimed on one or two substrate-family anchors to a construct that holds across five distinct families measured under one locked methodology. The empirical base is sufficient for the program to apply the construct to new substrate families as candidates for prospective measurement, and for brand-strategy practitioners to consume the construct as a stable measurement instrument rather than a moving-target methodology. The five families span three distinct consumer-discovery environments (editorial-authority, community-curated, social-media-native), and the construct's verdicts hold across all three. <b>What it doesn't mean.</b> ANCHORED is not the same as construct validity. The synthesis claims measurability — that AI Availability can be measured under a falsifiable pre-registered protocol with cross-substrate replicability — not predictive validity against behavioral outcomes. Whether AI Availability scores predict consumer behavior (consideration, search, purchase) is Phase 3 future work and is not established by the present anchor base. The full six-component AIAS™ composite (Ranking, Consistency, Coverage, Grounding, Sentiment) is reserved for a Phase 4 multi-year program. The present claim is bounded to Presence-component measurability across five substrate families, and the program's credibility rests on that bounded claim rather than on an over-claimed composite the data does not yet carry.

**P2 item (~265 words)**

> <b>What it means.</b> A brand's AI Availability cannot be inferred from absence on any single measurement panel. The phantom layer surfaces off-panel brands at measurable frequency, with channel signatures that track the same Identity-Load gradient as the panel-internal brands. The construct's value as a managerial instrument is highest in substrates where the brand-of-interest's panel-membership status is itself a moving question — emerging brands, indie tiers, and substrate categories where panel construction is contested. Practitioners can identify high-phantom-risk categories by checking whether category-best lists vary substantially across editorial sources or whether community-curated emergents regularly enter category discourse without appearing on supply-side market-share leaderboards. <b>What it doesn't mean.</b> CALIBRATED is not the same as cross-substrate replicated. v0.21 cosmetics is the calibration anchor — the substrate where the construct was empirically motivated, where the reference vocabulary was constructed, and where the validity anchor (Glossier R_phantom = 12) passed. Cross-substrate replication is the genuine generalization test, and that test is v0.22+ future work — prospective phases under the locked v1.6 protocol measuring phantom-layer behavior on substrate families other than cosmetics. Brand managers reading this report should treat the phantom-layer finding as established for cosmetics, hypothesized for other substrate families, and pending prospective measurement in each new substrate where the construct's behavior matters for brand-strategy decisions.

**P3 item (~275 words)**

> <b>What it means.</b> R_cat and R_cult operate on disjoint inputs and can be managed separately. A brand with low canonical-channel Recall has identifiable intervention pathways in authority surfaces (editorial coverage, expert recommendation, category-best curation, professional certification); a brand with low cultural-channel Recall has a different intervention class in discourse density (social-media volume, celebrity endorsement, viral content, community-curated cult-tier discourse). Rare Beauty's 1:17 channel split establishes the upper bound on how decoupled the two channels can be within a single brand, and the dissociation framework identifies the inverse pole at the Type 1 anchors (Bobbi Brown 8:0, Laura Mercier 5:0 in v0.21 Cell A). <b>What it doesn't mean.</b> Two-channel decomposition does not mean every brand should target both channels equally. The audit returns the brand's current channel position; the brand-strategy prescription depends on the brand's positioning and the cell's IL construction. A celebrity-DTC brand may correctly concentrate in the cultural channel; a heritage prestige brand may correctly concentrate in the canonical channel; the diagnostic is the audit surface, not the prescription. Conflating audit with prescription would reintroduce the single-channel framing the two-channel decomposition was designed to escape. The audit's contribution is structural: it surfaces the channel distinction so the brand-strategy team can decide whether the brand's current position matches the brand's intent, and act on the gap directly rather than negotiating which intervention class applies as a separate question.

**P4 item (~290 words)**

> <b>What it means.</b> Identity Load — operationalized through the substrate's panel design — empirically predicts the AI channel where a brand will surface, with confidence-interval rigor. A brand's cell position carries a predictive prior: high-IL cells expect cultural-channel lead; medium-IL cells expect canonical-channel lead; low-IL cells lie between under monotonic-gradient discipline. v0.21 cosmetics is the program's first CONFIRMED moderator verdict at any layer (Cell B δ = +7.13 with CI [+4.75, +10.25]; Cell A δ = −3.13 with CI [−6.00, −0.25]; Cell C δ = +1.00 with CI [−0.50, +3.25]; all in IL-predicted regions). Brand managers auditing brands can compare a brand's measured channel asymmetry against the cell's expected asymmetry directly — deviation from expectation is itself diagnostic information. <b>What it doesn't mean.</b> Identity Load is operationalized through the substrate's panel design, not through independently-measured consumer perceptions of the brand. The moderator operates on the panel-design construction, not on a separately-measured consumer-side construct of brand identity. The construct's mechanism is the IL-gradient property of the substrate-as-measured, and the brand-strategy implication is bounded to substrates where the panel-design IL classification meaningfully tracks the brand-of-interest's category positioning. v0.20 skincare's PARTIAL on the same test surfaced substrate-specific architecture — the cell where canonical authority concentrates is substrate-dependent, not panel-design-invariant. Clinical and dermatologist-anchored authority in skincare lives in a different cell position than editorial-prestige authority in cosmetics. The moderator holds for the substrate; the cell-architecture assumption requires substrate-aware interpretation.

**P5 item (~235 words)**

> <b>What it means.</b> Methodology v1.6 closed three measurement gaps the prior framework versions could not address: substrate-level Recognition pre-screen (so maximally-coded categories like cosmetics don't collapse the verdict matrix); independent moderator pathway (so Identity-Load asymmetry is evaluable separately from the four-regime test); Phantom Brand Persistence Phase B extension (so off-panel brand presence is a measured component rather than a descriptive side observation). Together the three form a coordinated audit pathway for substrates where prior framework versions would have collapsed the verdict — Increment 1 preserves the substrate's evidentiary value, and Increments 2 and 3 carry the discrimination signal that Recognition can't supply when it's exhausted at ceiling. <b>What it doesn't mean.</b> SHIPPED v1.6 does not mean the construct is methodology-complete. v1.7 (if it ships) would extend the protocol further — the program's methodology arc is ongoing, not closed. The v1.6 increments are bounded to the retrospective scope where the v1.6 paper's published rules permit them (Increment 2 for v0.20 + v0.21; Increment 3 for v0.21 only). Cross-substrate replication of Increments 2 and 3 is v0.22+ work. AIAS™ 1.0 names the Presence component of the AIAS construct, not the full multi-component composite — and the version-number arc 1.0 → 6.0 will track the measurement surface (each new component reaching falsifiable measurement) rather than architectural ambition.

---

## SECTION 6 — CLOSING

**Schema:** `CLOSING = {"byline_long": [<str>, ...], "datasets": [<str>, ...], "methodology_log": <str>}`

### CLOSING.byline_long

> Pablo Ulpiano González Castro
> School of Visual Arts, MPS Branding Program · New York, NY
> Third System™ (research entity; data archive and methodology venue)
> Correspondence: pablou@pablou.com · ORCID: 0009-0003-8968-9990

Standard 4-line program byline (matches v21). ™ marked on Third System per CLAUDE.md (first prominent mention in the closing block).

### CLOSING.datasets (5 entries)

> AIAS 1.0 synthesis data (cross-phase source-of-truth, locked at aias-1-0-data-locked): osf.io/ec6wh/aias_1_0/aias_1_0_synthesis_data.json

> Phase-level acquisitions, scoring code, and verdict matrices (v0.16 through v0.21): osf.io/ec6wh/v16/ through osf.io/ec6wh/v21/ (six per-phase deposit trees)

> Methodology papers v1.2 through v1.6 (pre-registrations, retrospective scoring outputs, increment specifications): osf.io/ec6wh/methodology/v1_2/ through osf.io/ec6wh/methodology/v1_6/

> AIAS 1.0 charts (academic synthesis paper figures + brand-format report upgrades): osf.io/ec6wh/aias_1_0/figures/

> Pre-registration lock artifacts (outline, data, charts, paper): git tags aias-1-0-outline-locked, aias-1-0-data-locked, aias-1-0-charts-locked, aias-1-0-paper-locked in the repository

### CLOSING.methodology_log

> AIAS 1.0 synthesis paper locked at git tags aias-1-0-outline-locked, aias-1-0-data-locked, aias-1-0-charts-locked, and aias-1-0-paper-locked. Academic companion deposited at SSRN 6817841 (May 2026). Methodology version: v1.6 (SSRN 6816340). This brand-format report ships two weeks behind the SSRN deposit per the program's two-register discipline

(Note: closing string drops the trailing period — the builder appends one in `build_closing_story` at `f"<b>Methodology log:</b> {content.CLOSING['methodology_log']}."` so trailing period in content produces double-period in rendered output. Matches v21 convention.)

---

## Step 3 self-scan

**Word counts:**

| Section | Words |
|---|---|
| COVER (subtitle is the load-bearing field) | ~80 |
| LEAD_DECK | 165 |
| WHAT_WE_MEASURED (8 paragraphs) | 920 |
| PROPOSITION_SCORING (heading + intro + 5 rows) | 525 |
| PROPOSITION_DETAILS (heading + intro + 5 items) | 1370 |
| CLOSING (byline_long + 5 datasets + methodology_log) | 215 |
| **Step 3 total** | **~3275 words** |

**Cumulative content-module total** (chunks 1–4 + step 3): ~6172 + ~3275 = **~9450 words**.

**Estimated .py file size** (chunk 1 had 12,185 bytes for ~987 words = ~12 bytes/word ratio including Python string-literal wrapping + comments): ~9450 × 12 ≈ **~113 KB**, ~**900–1100 lines**. Within outline §7 D5 estimate (1500–2200 lines target — comes in under the upper bound; comfortable cushion).

**Voice register checks:**

- COVER title — direct construct claim ("AI Availability as a Third Measurable Layer"); no academic framing. ✓
- COVER subtitle — opens "Five-substrate empirical anchor base under locked methodology v1.6" (concrete program-state fact). ✓
- LEAD_DECK — opens "This report consolidates the AIAS™ Measurement Program's five-substrate empirical anchor base in five propositions for brand strategy and marketing-science practitioners." Sets P1–P5 frame upfront. ✓
- WHAT_WE_MEASURED ¶3, ¶4, ¶5, ¶6 use bolded labels (`<b>Phase A — Recognition.</b>` etc.) — same convention as v21 WHAT_WE_MEASURED; aids skimming for managerial readers. ✓
- WHAT_WE_MEASURED ¶7 (substrate families) names each cell construction explicitly — gives readers the substrate-family vocabulary they need before PATTERNS findings reference cells. ✓
- PROPOSITION_SCORING intro opens "Five propositions consolidate the five-substrate empirical anchor base into actionable framing for brand strategy" — frames the table as actionable, not as audit-checklist. ✓
- PROPOSITION_SCORING rows — status vocabulary varies across the 5 (ANCHORED / CALIBRATED / CONFIRMED / CONFIRMED / SHIPPED v1.6); each row anchored on its own evidence rather than uniform pass/fail. ✓
- PROPOSITION_DETAILS items — "What it means / What it doesn't mean" pattern preserves the v21 HYPOTHESIS_DETAILS structure that managerial readers will recognize from phase reports. ✓
- CLOSING — datasets and methodology_log emphasize the synthesis-scale provenance (cross-phase data source-of-truth; OSF tree layout; lock tag chain). ✓

**Conventions:**

- ™ marked on first prominent mention per section: COVER subtitle ("AIAS™" first), LEAD_DECK ("AIAS™" first), WHAT_WE_MEASURED ¶1 ("AIAS™" first), PROPOSITION_SCORING intro ("AIAS™ 1.0 milestone" first), PROPOSITION_DETAILS P1 item ("AIAS™ composite" first), CLOSING byline ("Third System™" first).
- No H1/H2 hypothesis labels in rendered text. Note: PROPOSITION_SCORING P4 row carries "H_IdentityLoad_Direct CONFIRMED" in the result column — this reads as data provenance (the verdict came from this specific hypothesis test in v0.21 scoring), not as academic-paper voice. Flag for your judgment: keep, drop, or rephrase ("the IL Direct test returned CONFIRMED" without the H_ prefix).
- Verdict labels (CONFIRMED, EMERGED, PARTIAL, FALSIFIED) preserved where they carry methodology discipline.
- No Samsung COI disclosure (academic-paper-only per CLAUDE.md; report has no Declarations block).
- Cross-references to PATTERNS findings minimal (mostly forward-referenced in EXEC_SUMMARY; the structural sections don't need to re-anchor them).

**One flag for review:**

PROPOSITION_SCORING P4 row contains "v0.21 cosmetics H_IdentityLoad_Direct CONFIRMED" in the result column. This is the only H_ label in the structural sections. Three options:

- (a) Keep as-is — reads as data provenance, not academic voice. The test has a name; the verdict was returned against that specific name.
- (b) Drop the H_ prefix — "v0.21 cosmetics IdentityLoad_Direct CONFIRMED" (still reads as the test's name).
- (c) Rephrase — "v0.21 cosmetics: the IL Direct test returned CONFIRMED" (drops the test-name format entirely).

Recommend (a) — the H_ label here is informational (it ties the row's verdict back to the methodology-paper test the verdict came from) and the row is dense enough that the prefix doesn't disrupt scanning. (b) and (c) are equally defensible; flag for your call.

---

**After Step 3 approval: content module assembles fully.**

Assembly steps:

1. Create `reports/aias_1_0_content.py` with module docstring matching v21 pattern (mention forks from v21_cosmetics_content)
2. Assemble in builder-consumption order: COVER, STANDFIRST, LEAD_DECK, EXEC_SUMMARY, WHAT_WE_MEASURED, PATTERNS, LIMITATIONS, WHATS_NEXT, PROPOSITION_SCORING, PROPOSITION_DETAILS, CLOSING
3. Convert all native Unicode in chunk 1–4 + step 3 prose to `\u` escapes per v21 convention (e.g., `™` for ™, `×` for ×, `·` for ·, `—` for em-dash, `’` for ′, etc.)
4. Verify imports work: `python -c "from reports import aias_1_0_content"` (or similar)

Then proceed to:
- Render PDF: `python reports/build_charts_aias_1_0_report.py` → `python reports/build_report_aias_1_0.py`
- Pre-flight: page count band (22–32), chart placement, voice register spot-check, brand-format identity (Akkurat / Indigo)
- OSF deposit: `python scripts/osf_upload.py osf/aias_1_0/reports/ aias_1_0/reports`

**Holding for Step 3 verdict before assembly + render.**
