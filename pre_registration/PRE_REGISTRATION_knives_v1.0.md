# AIAS Phase 2 v0.8 — Pre-registration

**Category:** Premium kitchen knives
**Designed-for-test pattern:** Pattern 4 — Discourse-language bias
**Pre-registration version:** knives_v1.0
**Lock date:** 2026-05-06
**Status:** Locked before data collection per AIAS Presence Measurement Protocol v1.1 §6.4
**Previous designed-for-test:** v0.7 BBB (Pattern 6 — phantom-brand persistence)

---

## 1. Purpose and design

This document pre-registers hypotheses for the v0.8 designed-for-test measurement of Pattern 4 (discourse-language bias) per protocol §6.4 and §6.6. The v0.6 cross-category report surfaced Pattern 4 as a preliminary signal (Spanish olive oil under-surfacing despite ~45% global production share; K-beauty brands at 0% Presence despite extensive English-language editorial coverage), but no v0.6 category was designed-for-test. v0.8 closes that gap.

The category — premium kitchen knives — was selected because (a) Japan dominates premium production in a way comparable to Spain's position in olive oil, (b) English-language coverage exists but is mediated through US/UK food media rather than direct Japanese marketing, (c) German knives (Wüsthof, Henckels) and American knives (Cutco, Misen) provide structurally analogous English-discourse comparators on the same product, and (d) the Korean small-electronics alternative was ruled out due to Samsung's dominance in English discourse and the author's institutional Samsung affiliation creating an independence question.

The lineage structure (Japanese subject + German + American comparators + shared-context noise floor) was committed in `registries/brands_knives.json` v1.0, dated 2026-05-06. Twenty-one brands across three lineage aggregates plus three shared-context brands. Three Japanese brands (Masamoto, Sakai Takayuki, Yoshihiro) carry `boundary_condition: "discourse_language_test"` flags as the primary boundary-condition tests.

The prompt set was committed in `prompts/prompts_knives.json` v1.0 on the same date. Six CEPs per protocol §3.1. p3 (CONSTRAINT_WITH — "I cook a lot of fish and vegetables and want a really sharp, precise knife") carries deliberate structural bias toward Japanese-style blade characteristics. The bias is documented in the prompts.json design_note and is operationalized in H4 below.

## 2. Hypotheses

All eight hypotheses are evaluated on the full v0.8 dataset (target 288 successful measurements: 6 prompts × 6 models × 8 runs). "Aggregate Presence" for a lineage means the **mean Presence across the brands in that lineage** — not the sum, to control for unequal registry sizes (8 Japanese, 5 German, 5 American).

### H1 — Headline: Japanese aggregate Presence < German aggregate Presence

The headline test of Pattern 4 in v0.8.

- **CONFIRMED:** Japanese aggregate < German aggregate by ≥ 15 percentage points.
- **PARTIALLY CONFIRMED:** Japanese < German by 5–15 points.
- **DISCONFIRMED:** Japanese ≥ German, OR Japanese < German by less than 5 points.

Rationale: The 15pp threshold is calibrated against v0.6 cross-category gaps (Spanish olive oil mean ~9% vs Italian/American leaders > 50%). For knives, the gap is expected to be smaller because Japanese brands have more English presence than Spanish olive oil brands have. A 15-point gap on means is large enough to constitute a finding while small enough to be plausible given the comparator structure.

### H2 — Robustness: Japanese aggregate Presence < American aggregate Presence

Controls for the "Wüsthof effect" reviewer objection — namely, that German brands are unusually iconic in English-language cooking media and any Japanese-vs-German gap might just be Wüsthof and Henckels saturation, not a lineage-of-origin pattern.

- **CONFIRMED:** Japanese aggregate < American aggregate by ≥ 10 percentage points.
- **PARTIALLY CONFIRMED:** Japanese < American by 0–10 points.
- **DISCONFIRMED:** Japanese ≥ American.

Rationale: The threshold is smaller than H1 because American brands are less universally English-marketed than German brands (Cutco direct-sales channel, Misen is recent DTC, Lamson and Warther are heritage but niche). Even a directional gap (Japanese < American) controls for the German-specific objection; a 10pp gap establishes the finding robustly.

### H3 — Within-Japanese: Mass-market Japanese >> Traditional Japanese

Tests whether Pattern 4 operates within the Japanese lineage itself — specifically, whether English-marketing exposure within Japanese brands predicts Presence.

- **Mass-market Japanese:** mean Presence of Shun + Global (the incumbent-tier Japanese brands).
- **Traditional Japanese:** mean Presence of Masamoto + Sakai Takayuki + Yoshihiro (the three boundary-condition Japanese brands).
- **CONFIRMED:** Mass-market mean > Traditional mean by ≥ 30 percentage points.
- **PARTIALLY CONFIRMED:** by 15–30 points.
- **DISCONFIRMED:** by less than 15 points.

Rationale: The 30pp threshold is aggressive because the within-Japanese contrast is the cleanest controlled comparison — same lineage, same product category, differing only on English-marketing exposure. If H3 confirms at 30+ points, the report can claim that English-marketing exposure (not lineage per se) is the operative variable for AI Presence within a single lineage.

### H4 — Within-prompt: Japanese aggregate peaks in p3

Tests whether AI recognizes Japanese knife specialization at all. p3 (CONSTRAINT_WITH) is structurally biased toward Japanese-style blade characteristics; if Japanese brands fail to peak in p3 versus the lineage-neutral prompts, the AI does not recognize the specialization.

- **Lineage-neutral baseline:** mean of Japanese aggregate Presence across p1, p4, p6 (FUNCTIONAL_WHY, IDENTITY_HOW_FEELING, COMPARISON).
- **CONFIRMED:** Japanese aggregate Presence in p3 ≥ 1.5× the lineage-neutral baseline.
- **PARTIALLY CONFIRMED:** 1.2–1.5×.
- **DISCONFIRMED:** Japanese p3 ≤ baseline (the AI does not recognize Japanese specialization), OR Japanese p3 between 1.0× and 1.2× baseline.

Rationale: A 1.5× peak captures meaningful within-Japanese variance without requiring extreme effect size. Disconfirmation at p3 ≤ baseline would itself be a strong finding — a stronger-edged version of Pattern 4 than the headline H1 contrast.

### H5 — German parallel: Güde under-surfaces relative to Wüsthof + Henckels

Tests whether Pattern 4 is fundamentally about marketing-language coverage (which would predict any limited-English-marketing brand under-surfaces, regardless of lineage) or specifically about Japanese (which would predict Güde surfaces normally despite limited English presence).

- **CONFIRMED:** Güde Presence < one-third of (Wüsthof + Henckels mean Presence).
- **PARTIALLY CONFIRMED:** Güde Presence between 1/3 and 1/2 of (Wüsthof + Henckels mean).
- **DISCONFIRMED:** Güde Presence ≥ 1/2 of (Wüsthof + Henckels mean).

Rationale: This is the methodological-depth hypothesis. If H5 confirms (Güde under-surfaces), the v0.8 finding generalizes to "limited-English-marketing brands under-surface regardless of national lineage." If H5 disconfirms (Güde surfaces normally), the finding is specifically about Japanese, which is interesting but narrower. Either outcome is publishable and the methodology paper should report both possible framings.

### H6 — Within-lab freshness: descriptive

Mirrors v0.7 H4 (within-OpenAI descriptive). The within-Anthropic and within-OpenAI generational pairs (Sonnet 4.6 vs Opus 4.7; gpt-5.4-mini vs gpt-5.5) are reported as descriptive comparisons of how lineage-aggregate gaps differ across model generations within the same lab.

- **No pre-registered threshold.** Result is reported in direction and magnitude, with explicit acknowledgment that it is descriptive rather than confirmatory.

Rationale: The v0.7 finding (newer models phantom-mention "better, not less") was strongly counter-intuitive and emerged from the descriptive H4 analysis. Holding H6 descriptive in v0.8 preserves the same epistemic posture — letting the data tell us about generational behavior rather than committing to a pre-registered direction. If the v0.8 within-lab pattern points strongly in a direction, that's a finding; if it doesn't, the descriptive treatment is honest about that.

### H7 — Authority mode: English-language publications dominate

DISCOVERY (p5) and IDENTITY (p4) prompts often activate authority-mode responses (per protocol §3.4) where the AI names publications, communities, retailers, or competitions instead of brands. The v0.6 finding (every authority named was English-language) should replicate.

- **CONFIRMED:** ≥ 90% of named authority sources (publications, websites, online communities, retailers) in p4 + p5 responses are English-language.
- **PARTIALLY CONFIRMED:** 70–90%.
- **DISCONFIRMED:** < 70%.

Rationale: 90% is calibrated against v0.6's near-100% English-only authority observation. The threshold leaves room for a few non-English sources without being so stringent that any minor non-English mention disconfirms.

### H8 — Boundary punchline: Traditional Japanese collectively register < 5% aggregate Presence

The strongest-edged test. If the three boutique Japanese masters collectively get less than 5% mean Presence in AI knife recommendations — despite being among the most respected makers in Japanese knife traditions and being recognized by professional chefs — that's the v0.8 hero finding.

- **Aggregate:** mean Presence of Masamoto + Sakai Takayuki + Yoshihiro across all 288 measurements.
- **CONFIRMED:** aggregate mean Presence < 5%.
- **PARTIALLY CONFIRMED:** 5–15%.
- **DISCONFIRMED:** ≥ 15%.

Rationale: The 5% threshold is aggressive. v0.6 K-beauty Beauty of Joseon was 0%; if traditional Japanese knife makers cluster near zero or low single-digits, the parallel to skincare K-beauty is direct and the methodology paper has a clean finding chain across categories.

## 3. Methodological risks

Per protocol §6.4 ("Risks that materialize as predicted are recorded; risks that don't are recorded too").

### Risk 1 — Wüsthof / Henckels ceiling compression

Parallel to v0.7's Walmart / Amazon ceiling-compression risk. The two German incumbents are likely to saturate p1 (FUNCTIONAL_WHY) and p6 (COMPARISON) at near-100% each, structurally constraining how much of those prompts' brand-mention budget remains for Japanese or American brands. If this materializes, the lineage gaps in p1 and p6 will be inflated by ceiling effects rather than purely by Pattern 4. Mitigation: report per-prompt aggregates separately so the ceiling-compressed prompts are visible, and use p3 and p4 as the prompts where lineage gaps are most diagnostic.

### Risk 2 — DISCOVERY (p5) component-mode or authority-mode response

Per protocol §3.4 (the three modes of AI response). v0.6 skincare's DISCOVERY prompt produced no clear emerging-brand tier — interpreted as a structural finding (the editorial discourse has worked through "emerging" so the cognitive slot is empty), not a prompt failure. v0.8 p5 may behave the same way. If DISCOVERY produces zero or near-zero brand-mode Presence across all lineages, the prompt contributes nothing to the headline contrast but contributes to H7 (authority-mode dominance). This is documented as expected, not as a measurement failure.

### Risk 3 — p3 component-mode response

p3 (CONSTRAINT_WITH) may activate component mode — naming "VG-10 steel," "single bevel," "thin profile," "high-carbon steel" instead of brands. Similar to v0.6 olive oil FUNCTIONAL producing "extra virgin," "PDO/PGI" instead of brand names. If p3 goes component-mode, H4 becomes uninterpretable because there are no Japanese brand mentions to peak. Mitigation: manual review of p3 responses to classify mode (brand vs component) before computing H4. If a substantial fraction of p3 responses are component-mode, report H4 conditional on brand-mode responses only and flag the conditional.

### Risk 4 — "Made In" false-positive risk

The American challenger brand "Made In" overlaps with the common preposition phrase ("made in USA," "made in Japan"). Aliases narrowed to "made in cookware," "made in knives," "madein" to mitigate, but residual risk remains. Mitigation: manual spot-check of Made In mentions if its Presence appears anomalously high relative to other DTC American challengers.

### Risk 5 — Extractor category-prompt artifact

Per protocol §5.1 known artifact: the extractor system prompt is hardcoded for project management software ("You extract brand mentions from text about project management software"). The structured-output extraction handles domain context via the brand registry's canonical/alias list, but the system prompt is mismatched. Phase 2 plans to parameterize by category. For v0.8 the extractor still performs correctly because the brand registry provides the disambiguation context, but the residual risk is documented here.

## 4. Scoring rubric

Each hypothesis is scored against three bands: CONFIRMED, PARTIALLY CONFIRMED, DISCONFIRMED. Bands are defined per-hypothesis above with explicit numerical thresholds.

For descriptive hypotheses (H6), no band applies — the result is reported in direction and magnitude with the descriptive label attached.

If manual review or post-hoc analysis surfaces a finding the pre-registration did not anticipate (e.g., the v0.7 recommendation-slot reframe), the v0.8 report explicitly acknowledges that finding as exploratory rather than confirmatory and labels it accordingly. Specific reframe candidates already anticipated:

- A within-Japanese variance pattern not captured by the H3 binary (mass-market vs traditional). For example, if Tojiro / Mac / Misono cluster differently from both Shun/Global and Masamoto/Sakai Takayuki/Yoshihiro, the within-lineage structure may need a third tier in the report.
- Component-mode findings for p3 producing structurally informative results (e.g., AI naming Japanese-style steel terms — "shun steel," "VG-10," "Aogami," "Damascus" — without naming Japanese brands). This would be a Pattern 4 sub-finding distinct from the headline measurement.
- Authority-mode findings beyond H7's English-language test (e.g., specific publications dominate the authority slot).

These are flagged in advance to maintain methodological honesty per the v0.7 reframe-during-analysis precedent.

## 5. Lock statement

This pre-registration document is locked as of **2026-05-06** and committed to git before any v0.8 measurement data collection. The associated registry (`registries/brands_knives.json` v1.0) and prompt set (`prompts/prompts_knives.json` v1.0) were locked on the same date. No data has been collected against these hypotheses prior to lock; the wiring smoke test on 2026-05-06 (3 successful API calls before user interrupt) was discarded without writing to disk.

The v0.8 measurement run is authorized to proceed after this document is committed.

---

## Appendix A — Threshold rationale summary

| H | Threshold | Rationale |
|---|---|---|
| H1 | ≥ 15pp Japanese < German | Calibrated against v0.6 cross-category gaps; large enough to constitute a finding, small enough to be plausible |
| H2 | ≥ 10pp Japanese < American | Smaller because American brands less universally English-marketed; controls for "Wüsthof effect" objection |
| H3 | ≥ 30pp mass-market > traditional Japanese | Aggressive because within-lineage contrast is cleanest controlled comparison |
| H4 | ≥ 1.5× Japanese p3 vs lineage-neutral baseline | Captures within-prompt variance without requiring extreme effect |
| H5 | Güde < 1/3 of Wüsthof+Henckels mean | Tests language-coverage broadly vs Japanese-specifically |
| H6 | (descriptive) | Mirrors v0.7 H4; lets data tell us about generational behavior |
| H7 | ≥ 90% English authorities | Calibrated against v0.6 near-100% English-only observation |
| H8 | < 5% traditional Japanese aggregate | Aggressive; if confirmed, parallels v0.6 K-beauty 0% directly |

## Appendix B — Cross-references

- AIAS Presence Measurement Protocol v1.1 (canonical methodology)
- Tri-System Brand Growth (Gonzalez Castro 2026, JBM forthcoming) — defines AIAS as third availability layer; v0.8 data feeds §9.5a Corporate Portfolio Layer
- v0.6 cross-category report — Pattern 4 preliminary observations (olive oil Spanish under-surfacing; skincare K-beauty under-surfacing)
- v0.7 BBB designed-for-test — Pattern 6 closure; methodological template for designed-for-test category structure
