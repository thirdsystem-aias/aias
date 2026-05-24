"""
aias_1_0_content.py — Content module for the AIAS 1.0 Third System
brand-format synthesis report.

Forked schema from v21_cosmetics_content.py with surgical changes per
outline §4:
  - HYPOTHESIS_SCORING / HYPOTHESIS_DETAILS renamed to PROPOSITION_SCORING /
    PROPOSITION_DETAILS to prevent H_ label leakage into the rendered table
  - PATTERNS expanded to 5 findings (P1-P5) vs v21's 3
  - WHAT_WE_MEASURED scaled from single-phase methodology to cumulative
    v1.2 → v1.6 chain + 5-family scope (8 paragraphs vs v21's 5)
  - LIMITATIONS scaled from single-phase to cross-family (5 paragraphs vs 4)
  - WHATS_NEXT scaled from single-phase to Phase 3 + Phase 4 + 3 expansion
    axes (5 paragraphs vs 3)

Schema (in builder-consumption order, consumed by build_report_aias_1_0.py):
  COVER, STANDFIRST, LEAD_DECK, EXEC_SUMMARY, WHAT_WE_MEASURED,
  PATTERNS, LIMITATIONS, WHATS_NEXT, PROPOSITION_SCORING,
  PROPOSITION_DETAILS, CLOSING

PATTERNS items expose: number, title, chart_slot, chart_after_text (opt),
paragraphs. The chart_slot string is one of:
  f1_anchor_base, f2_phantom_channel, f3_type2_emergence, f4_il_direct_forest
or None (P5 is text-only). Resolved in build_report_aias_1_0.py via
_slot_lookup() to the chart PDF at one of:
  reports/figs/aias_1_0/        (3 re-used synthesis paper charts)
  reports/figs/aias_1_0_report/ (P2 phantom brand-format upgrade)

Voice register lock (non-negotiable):
  - Managerial / P1-P5 propositional throughout
  - NO H1/H2 hypothesis labels in rendered text
  - Each proposition reads as what brands can do or know
  - Verdict labels (CONFIRMED, EMERGED, PARTIAL, FALSIFIED,
    REGIME-4-UNAVAILABLE-AT-RECOGNITION) preserved where they carry
    discipline; verdict labels translated where they would read as
    academic jargon

Convention note: This module uses native Unicode (UTF-8 source file)
rather than v21's \\uXXXX escape convention. Technically equivalent
under Python 3 and ReportLab; the convention departure is for prose
readability during ongoing voice-test review. Convert with
unicodedata.normalize / repr() pass at any time if v21 convention
re-enforcement is required.

Source: Translated from synthesis paper SSRN 6817841 (§1, §2, §3, §4,
§5, §6.2, §7) per the P1-P5 register lock in
reports/aias_1_0_content_outline.md §3. Drafted in 4 chunks + 1
structural-sections pass to ~/aias/reports/_review/ (chunks 2-4) and
/tmp/aias_1_0_report_review/ (chunk 1); checkpoint-approved by Pablo
between 2026-05-23 chunks.
"""


# ---------------------------------------------------------------------------
# COVER
# ---------------------------------------------------------------------------

COVER = {
    "title": "AI Availability as a Third Measurable Layer",
    "subtitle": (
        "Five-substrate empirical anchor base under locked methodology "
        "v1.6. The Presence component of the AIAS™ construct reaches its "
        "1.0 milestone with cosmetics as the strongest single-phase "
        "evidence base: cultural-channel Recall populates the dissociation "
        "construct’s third quadrant above threshold, Identity Load "
        "empirically tracks AI channel asymmetry at confidence-interval "
        "rigor, and off-panel brand presence enters as a measured "
        "component with channel signatures that track the same "
        "Identity-Load gradient as panel-internal brands."
    ),
    "date": "May 2026",
    "byline_short": "Pablo Ulpiano González Castro · Third System",
    "tagline": "Independent measurement for the AI mediation layer.",
}


# ---------------------------------------------------------------------------
# STANDFIRST — single Paragraph (rendered in cover_subtitle style on lead spread)
# Per D4 lock: ~790 chars / 105 words.
# ---------------------------------------------------------------------------

STANDFIRST = (
    "AIAS™ measures AI Availability — the probability that an AI "
    "intermediary retrieves, recommends, or selects a brand in a "
    "category-anchored decision context — as a third measurable channel "
    "of brand presence alongside the Ehrenberg-Bass framework’s Mental "
    "Availability and Physical Availability. With the v0.21 cosmetics "
    "phase, the protocol’s empirical anchor base spans five substrate "
    "families (kitchenware, indie fragrance, audiophile electronics, "
    "skincare, cosmetics) under one locked methodology version. AIAS™ "
    "1.0 anchors the Presence component across five substrate families."
)


# ---------------------------------------------------------------------------
# LEAD_DECK — single Paragraph (rendered in lead_deck style)
# ~165 words; frames P1-P5 upfront so PATTERNS sections read in context.
# ---------------------------------------------------------------------------

LEAD_DECK = (
    "This report consolidates the AIAS™ Measurement Program’s "
    "five-substrate empirical anchor base in five propositions for "
    "brand strategy and marketing-science practitioners. P1: AI "
    "Availability is now anchored across five substrate families — "
    "kitchenware, indie fragrance, audiophile electronics, skincare, "
    "and cosmetics — as a measurable third channel of brand presence. "
    "P2: brands not on a measurement panel can still drive AI "
    "retrieval, and their channel signature tracks Identity Load — "
    "Estée Lauder and Clinique canonical-pure, Glossier cultural-pure. "
    "P3: Recall splits into a canonical channel and a cultural channel "
    "that can be managed separately, with Rare Beauty’s 1:17 "
    "R_cat:R_cult split as the textbook diagnostic. P4: Identity Load "
    "predicts which channel will lead, with cosmetics returning the "
    "program’s first CONFIRMED moderator verdict at any layer. P5: "
    "methodology v1.6 closes the operational layer that makes P2 "
    "through P4 measurable."
)


# ---------------------------------------------------------------------------
# EXEC_SUMMARY — list of paragraph strings (renders in body style)
# 9 paragraphs / ~880 words.
# ---------------------------------------------------------------------------

EXEC_SUMMARY = [
    (
        "AIAS™ measures AI Availability — the probability that an AI "
        "intermediary retrieves, recommends, or selects a brand in a "
        "category-anchored decision context — as a third measurable "
        "channel of brand presence alongside the Ehrenberg-Bass "
        "framework’s Mental Availability and Physical Availability. "
        "The construct is operationalized through a pre-registered "
        "measurement protocol that runs against a fixed reference "
        "panel of six LLMs and is evaluated under locked verdict "
        "matrices each phase. AIAS™ 1.0 names the Presence component "
        "of a multi-component AIAS construct; the remaining five "
        "components (Ranking, Consistency, Coverage, Grounding, "
        "Sentiment) are reserved for a Phase 4 multi-year program "
        "and are not claimed by the present synthesis."
    ),
    (
        "With the v0.21 cosmetics phase shipped in May 2026, the "
        "protocol’s empirical anchor base spans five substrate "
        "families: kitchenware (v0.16 kitchen knives, v0.17 premium "
        "kitchenware), indie fragrance (v0.18), audiophile "
        "electronics (v0.19), skincare (v0.20), and cosmetics (v0.21). "
        "Six pre-registered measurement events between March and May "
        "2026. The five families span three distinct consumer-"
        "discovery environments: editorial-authority categories where "
        "canonical recommendation drives retrieval (skincare, "
        "kitchenware), community-curated categories where forum and "
        "review-channel discourse drives retrieval (audiophile, indie "
        "fragrance), and social-media-native categories where "
        "celebrity and viral discourse drives retrieval (cosmetics). "
        "The construct’s verdicts hold across all three environments."
    ),
    (
        "The reference panel is six LLMs held fixed across the "
        "program: Claude Opus 4.5, Claude Sonnet 4.5, GPT-4o, "
        "GPT-4o-mini, Gemini 2.5 Flash, and Gemini 2.5 Flash Lite. "
        "Holding the panel fixed across phases is the program’s "
        "cross-phase comparability discipline — verdicts are "
        "properties of brand × substrate × panel triples measured "
        "under the same set of intermediaries each time. Per-LLM "
        "rankings and provider-level performance comparisons are not "
        "the report’s subject; the construct is a property of the "
        "brand × substrate × panel system as a whole."
    ),
    (
        "This report consolidates the five-family anchor base under "
        "five propositions. P1: AI Availability is now a measurable "
        "third channel of brand presence, anchored across five "
        "substrate families. P2: off-panel brand presence is real "
        "and its channel signature tracks Identity Load — Estée "
        "Lauder and Clinique surface canonical-pure, Glossier "
        "surfaces cultural-pure. P3: Recall splits into a canonical "
        "channel and a cultural channel that can be managed "
        "separately — Rare Beauty’s 1:17 R_cat:R_cult split is the "
        "textbook diagnostic. P4: Identity Load predicts which "
        "channel will lead, at confidence-interval rigor. P5: "
        "methodology v1.6 closes the operational layer that makes "
        "P2 through P4 measurable."
    ),
    (
        "The v0.21 cosmetics phase produced the program’s strongest "
        "single-phase evidence base. Three primary findings stack: "
        "cultural-channel Recall populated the Type 2 dissociation "
        "quadrant above the EMERGED threshold for the first time "
        "(three Cell B cases — Rare Beauty, Huda Beauty, Kylie "
        "Cosmetics); the Identity-Load moderator returned CONFIRMED "
        "with the program’s first CONFIRMED moderator verdict at any "
        "layer (95% bootstrap confidence intervals satisfying the "
        "monotonic-gradient check across cells); and Phantom Brand "
        "Persistence returned CONFIRMED with margin (six off-panel "
        "brands clearing the persistence threshold; the Glossier "
        "validity anchor passing at R_phantom = 12)."
    ),
    (
        "Three of the six phantom brands in cosmetics are channel-"
        "pure. Estée Lauder appears exclusively in canonical-channel "
        "frames (R_cat = 13, R_cult = 0); Clinique also exclusively "
        "canonical; Glossier exclusively in cultural-channel frames "
        "(R_cat = 0, R_cult = 12). The channel signature tracks "
        "Identity Load — prestige and heritage cosmetics in the "
        "authority pathway; celebrity, DTC, and cult brands in the "
        "discourse pathway. A brand’s AI Availability cannot be "
        "inferred from absence on any single measurement panel; the "
        "phantom layer must be measured against an exogenously-"
        "constructed reference vocabulary at the substrate level."
    ),
    (
        "Rare Beauty is the textbook diagnostic case. With "
        "Recognition saturated at C_P = 6/6 (universally categorized "
        "as a cosmetics brand by every panel intermediary), the "
        "brand’s canonical-channel Recall is 1/18 while its cultural-"
        "channel Recall is 17/18 — a 1:17 split that establishes the "
        "upper bound on how decoupled the two channels can be within "
        "a single brand. The diagnostic is load-bearing for brand-"
        "strategy practice: a brand with this profile has "
        "identifiably different brand-strategy options than a brand "
        "with the inverse profile, and the protocol’s measurement "
        "procedure surfaces the distinction at the audit layer rather "
        "than leaving it to interpretation."
    ),
    (
        "For brand practice, the report’s most actionable finding is "
        "the two-channel decomposition. R_cat (canonical Recall) and "
        "R_cult (cultural Recall) respond to disjoint inputs and can "
        "be managed separately. Canonical Recall responds to "
        "authority surfaces — editorial coverage, expert "
        "recommendation, category-best curation, professional "
        "certification. Cultural Recall responds to discourse "
        "density — social-media volume, celebrity endorsement, viral "
        "content, community-curated cult-tier discourse. "
        "Practitioners can audit a brand’s current channel position "
        "with the protocol’s measurement procedure and target the "
        "underperforming channel with the appropriate intervention "
        "class without conflating the two pathways into a single "
        "Recall budget."
    ),
    (
        "The report’s claims are scoped by design. AIAS™ 1.0 names "
        "the Presence component of the AIAS construct, not the full "
        "six-component composite. Construct validity (predictive "
        "validity against behavioral outcomes; convergent and "
        "discriminant validity against Mental and Physical "
        "Availability) is Phase 3 future work. The consumer-behavior "
        "correlate of AI Availability — whether AI Availability "
        "scores predict consideration, search, or purchase behavior — "
        "is plausible on theoretical grounds but has not been "
        "measured by the present program. The report establishes "
        "measurability under pre-registration discipline across five "
        "substrate families; validation against behavioral outcomes "
        "and integration of the remaining five composite components "
        "is the work the next decade of measurement-program research "
        "will do."
    ),
]


# ---------------------------------------------------------------------------
# WHAT_WE_MEASURED — heading + paragraphs
# 8 paragraphs / ~920 words (vs v21's 5 paragraphs single-phase scope).
# ---------------------------------------------------------------------------

WHAT_WE_MEASURED = {
    "heading": "What we measured",
    "paragraphs": [
        (
            "AIAS™ measures AI Availability through a pre-registered "
            "protocol that runs the same two-phase measurement against "
            "each new substrate family under a panel of six LLMs held "
            "fixed across the program. The protocol’s specifications "
            "are locked at git tag at each new phase before any "
            "acquisition; the methodology version that governs scoring "
            "is itself locked at git tag before retrospective scoring "
            "is applied to any prior-phase corpus. The methodology "
            "version that governs the present synthesis is v1.6 "
            "(SSRN 6816340, May 2026)."
        ),
        (
            "The reference panel is six LLMs locked at v0.17 and held "
            "constant across the program: Claude Opus 4.5, Claude "
            "Sonnet 4.5, GPT-4o, GPT-4o-mini, Gemini 2.5 Flash, and "
            "Gemini 2.5 Flash Lite. Holding the panel fixed across "
            "phases is the program’s cross-phase comparability "
            "discipline — verdicts produced in any one phase are "
            "evaluable against verdicts from any other phase because "
            "the measurement instrument is the same. Per-LLM rankings "
            "and provider-level performance comparisons are not the "
            "program’s subject; verdicts are properties of brand "
            "× substrate × panel triples evaluated under the same "
            "set of intermediaries each time."
        ),
        (
            "<b>Phase A — Recognition.</b> Each brand in the panel "
            "registry is presented to each of the six panel "
            "intermediaries with a category-membership probe (template "
            "locked at v1.4 specification): the model is asked whether "
            "the brand is commonly recognized as a member of the "
            "substrate’s category, with a yes/no response. The brand’s "
            "Recognition score C_P is the count of yes responses "
            "across the six panel intermediaries, range 0–6. C_P is "
            "the Recognition component of AI Availability — a brand "
            "with C_P = 6 is universally categorized by the panel; "
            "a brand with C_P = 0 is not categorized as a category "
            "member by any panel intermediary."
        ),
        (
            "<b>Phase B — Recall, two-channel decomposition.</b> Each "
            "panel intermediary receives a six-frame open-ended query "
            "battery against the substrate’s category, and the panel’s "
            "responses are scanned for brand mentions against the "
            "locked substrate registry. v1.5 introduced the two-channel "
            "decomposition: three frames anchor the canonical channel "
            "(R_cat — best brands, most-recommended brands, "
            "highest-quality brands; max 18 = 3 frames × 6 models) and "
            "three frames anchor the cultural channel (R_cult — most "
            "popular brands, celebrity-favorite brands, viral or "
            "cult-favorite brands; max 18). The two channels operate "
            "on disjoint inputs and can be managed separately at the "
            "brand-strategy intervention layer."
        ),
        (
            "<b>Three dissociation patterns at the v1.5 thresholds.</b> "
            "Iwachu: high Recognition with sparse canonical Recall "
            "(C_P ≥ 5 ∧ R_cat ≤ 2) — named after the Japanese "
            "kitchenware brand that anchored the first case in v0.17. "
            "Type 1: canonical-channel-preferred (R_cat ≥ 5 ∧ "
            "R_cult ≤ 2) — prestige and authority-anchored brands "
            "cluster here. Type 2: cultural-channel-preferred "
            "(R_cat ≤ 2 ∧ R_cult ≥ 5) — celebrity-DTC and "
            "discourse-driven brands cluster here. The three patterns "
            "occupy the Recognition × Recall plane and bracket the "
            "dissociation construct’s empirical geometry. v0.21 "
            "cosmetics is the first phase where Type 2 cleared the "
            "EMERGED threshold (three Cell B cases)."
        ),
        (
            "<b>Methodology v1.6 — three increments.</b> First, a "
            "substrate-level Recognition pre-screen identifies "
            "substrates where every panel brand is categorically "
            "recognized in every cell (the cosmetics case) and routes "
            "them to a distinct verdict state preserving the "
            "substrate’s evidentiary value at the moderator and "
            "phantom layers. Second, an independent moderator pathway "
            "evaluates Identity-Load asymmetry as δ = mean(R_cult) "
            "− mean(R_cat) per cell with 95% bootstrap confidence "
            "intervals (n = 10,000) and a monotonic-gradient check "
            "across cells. Third, the Phantom Brand Persistence Phase "
            "B extension scores off-panel brand presence against an "
            "exogenously-constructed reference vocabulary (union of "
            "the panel, a pre-registered top-50 market-share list, "
            "and prior-phase Phase B emergents cross-validated by the "
            "market-share list) with persistence threshold K = 6 and "
            "a pre-registered validity anchor."
        ),
        (
            "<b>Five substrate families anchor the construct.</b> "
            "v0.16 kitchen knives and v0.17 premium kitchenware "
            "(kitchenware family — Cell A heritage, Cell B Japanese-"
            "cult, Cell C mass); v0.18 indie fragrance (Cell A "
            "heritage / niche, Cell B perfumista-cult, Cell C mass); "
            "v0.19 audiophile electronics (two-cell uniform-IL design "
            "— Heritage and Boutique, with audiophile-community "
            "curation producing the substrate-shape case the IL-"
            "gradient framework cannot test against); v0.20 skincare "
            "(Cell A heritage / clinical, Cell B celebrity-DTC, Cell "
            "C mass / drugstore); v0.21 cosmetics (Cell A prestige, "
            "Cell B celebrity-DTC / cult, Cell C drugstore / mass). "
            "Each phase locked its 24-brand panel — eight brands per "
            "cell × three cells, or twelve per cell × two cells "
            "for v0.19 — at pre-registration before any acquisition."
        ),
        (
            "<b>Pre-registration discipline.</b> Every phase enters "
            "the program under pre-registration. Panel construction, "
            "substrate registry, Phase A probe template, Phase B "
            "six-frame battery, hypothesis set, decision rules, and "
            "verdict matrices are locked ex-ante at a git tag "
            "(v0.NN-prereg-rN); the methodology version is locked at "
            "its own tag (v1.NN-prereg-rN). All artifacts — "
            "pre-registrations, acquisition data, scoring code, "
            "verdict outputs, reference vocabularies — are deposited "
            "under Open Science Framework project ec6wh "
            "(osf.io/ec6wh). The discipline is what allows the "
            "construct’s verdicts to be falsifiable and the "
            "construct’s measurability claim to stand or fall on its "
            "own evidence."
        ),
    ],
}


# ---------------------------------------------------------------------------
# PATTERNS — 5 findings (P1-P5), each with chart_slot (P5 text-only)
# ~3765 words total across PATTERNS section.
# ---------------------------------------------------------------------------

PATTERNS = [
    {
        "number": 1,
        "title": (
            "The five-substrate empirical anchor base is complete. "
            "AI Availability is anchored, not provisional."
        ),
        "chart_slot": "f1_anchor_base",
        "paragraphs": [
            (
                "Six pre-registered measurement events between March "
                "and May 2026 anchor the AIAS™ Presence Measurement "
                "Protocol across five substrate families: kitchenware "
                "(v0.16 + v0.17), indie fragrance (v0.18), audiophile "
                "electronics (v0.19), skincare (v0.20), and cosmetics "
                "(v0.21). Each phase locked its panel, brand registry, "
                "probe wording, hypothesis set, decision rules, and "
                "verdict matrices at a git tag before any measurement "
                "data was acquired. The methodology version itself is "
                "locked at v1.6 (SSRN 6816340, May 2026), with the "
                "locked-methodology boundary applied to retrospective "
                "scoring per the protocol’s published rules. Holding "
                "both the panel and the methodology fixed across "
                "phases is the program’s cross-phase comparability "
                "discipline — verdicts produced in any one phase are "
                "evaluable against verdicts from any other phase, "
                "because the measurement instrument is the same. The "
                "construct stands or falls on this discipline."
            ),
            (
                "The five families were not selected for breadth "
                "alone; each contributed a methodology-relevant "
                "observation. Kitchenware (v0.16 + v0.17) established "
                "the original Recognition × Recall dissociation "
                "pattern — named Iwachu after the Japanese kitchenware "
                "brand that anchored the first case — and surfaced "
                "the substrate-language-carryforward phenomenon that "
                "constrains panel design for non-English-language "
                "substrates. Indie fragrance (v0.18) extended the "
                "dissociation framework into an English-language "
                "perfumistas-native discourse environment and produced "
                "the first multi-cell Iwachu generalization, "
                "establishing that the pattern is not specific to a "
                "single substrate family or discourse language. "
                "Audiophile electronics (v0.19) was the substrate-"
                "shape case — a uniform-Identity-Load substrate that "
                "the IL-gradient framework cannot test against, "
                "surfacing as the methodology-design counterexample "
                "that motivated the v1.6 substrate Recognition "
                "pre-screen. Skincare (v0.20) was the first "
                "prospective phase under the v1.5 two-channel Recall "
                "design and produced the first PARTIAL Type 2 verdict "
                "under the new framework, plus a skincare-specific "
                "Cell A architecture finding (clinical authority "
                "lives in a different place than prestige authority). "
                "Cosmetics (v0.21) is the program’s strongest "
                "single-phase evidence base, producing the three "
                "v0.21 headline findings that propositions P2 through "
                "P4 carry below."
            ),
            (
                "One observation surfaces under the synthesis view "
                "that no single phase’s verdict matrix could surface "
                "within its own scope. The Type 2 dissociation "
                "pattern — cultural-channel-preferred Recall, defined "
                "as R_cat ≤ 2 and R_cult ≥ 5 — was pre-registered "
                "to be tested in each phase against the cell where "
                "Identity Load is highest (Cell B in the standard "
                "panel design). When the all-cell algorithmic "
                "dissociation framework is applied uniformly to the "
                "cross-phase data rather than to each phase’s "
                "Cell-B-anchored verdict scope, two out-of-cell Type 2 "
                "cases recover. La Mer (v0.20 skincare, Cell A — "
                "prestige; C_P = 6, R_cat = 2, R_cult = 7) and e.l.f. "
                "Cosmetics (v0.21 cosmetics, Cell C — drugstore/mass; "
                "C_P = 6, R_cat = 1, R_cult = 9) jointly establish "
                "out-of-cell Type 2 as a recurrent feature of the "
                "dissociation pattern across substrate families. The "
                "per-phase published verdicts (v0.20 PARTIAL, v0.21 "
                "EMERGED) stand as authoritative within their "
                "pre-registered Cell-B scope; the cross-phase view "
                "adds a substrate-wide pattern observation that "
                "practitioners reading the synthesis can carry forward "
                "without amending either phase paper’s record. For "
                "brand managers: a brand can occupy a Type 2 channel "
                "position regardless of the panel-design cell it was "
                "placed in — supply-side tier classification "
                "(prestige, mass) does not determine where in the "
                "two-channel space the brand will land."
            ),
            (
                "For brand managers, the anchor-base completion "
                "changes the construct’s standing. AI Availability "
                "has graduated from a construct claimed on one or two "
                "substrate-family anchors to a construct that holds "
                "across five distinct families measured under one "
                "locked methodology. The construct can be applied to "
                "new substrate families as candidates for prospective "
                "measurement — v0.22 and successor phases under the "
                "same v1.6 lock — and brand-strategy practitioners "
                "can consume the construct as a stable measurement "
                "instrument rather than a moving-target methodology. "
                "Two boundaries persist. Construct validity — whether "
                "AI Availability scores predict downstream consumer "
                "behavior such as consideration, search, or purchase "
                "— is Phase 3 future work and is not established by "
                "the present anchor base. The full six-component "
                "AIAS™ composite (Ranking, Consistency, Coverage, "
                "Grounding, Sentiment) is reserved for a Phase 4 "
                "multi-year program. The present claim is bounded to "
                "Presence-component measurability across five "
                "substrate families, and the program’s credibility "
                "rests on that bounded claim rather than on an "
                "over-claimed composite the data does not yet carry."
            ),
        ],
    },
    {
        "number": 2,
        "title": (
            "Brand presence in AI retrieval extends beyond the panel. "
            "Channel signature tracks Identity Load."
        ),
        "chart_slot": "f2_phantom_channel",
        "paragraphs": [
            (
                "On the v0.21 cosmetics measurement, six off-panel "
                "brands surfaced persistently in the panel’s "
                "category-anchored responses. Each cleared the K = 6 "
                "persistence threshold under the v1.6 Phantom Brand "
                "Persistence specification: Urban Decay "
                "(R_phantom = 13), Estée Lauder (13), Glossier (12), "
                "Too Faced (9), Make Up For Ever (7), and Clinique "
                "(6). The brands were absent from the v0.21 panel — "
                "the panel was tier-balanced at 8 brands per cell × "
                "3 cells = 24 brands, drawn from prestige, celebrity-"
                "DTC/cult, and drugstore/mass tiers — but appeared in "
                "the panel intermediaries’ responses to category-"
                "anchored prompts at sufficient frequency to meet the "
                "persistence threshold. The phantom-layer construct "
                "is the program’s first measured component for "
                "off-panel presence: prior to v1.6, off-panel "
                "mentions were noted as a descriptive observation "
                "across multiple phases but not scored as a "
                "measurement component. v0.21 is the substrate where "
                "the construct was empirically motivated and where "
                "the calibration was anchored."
            ),
            (
                "Three of the six phantom brands are channel-pure. "
                "Estée Lauder appears exclusively in canonical-"
                "channel frames (R_cat = 13, R_cult = 0); Clinique "
                "also exclusively canonical (R_cat = 6, R_cult = 0); "
                "Glossier appears exclusively in cultural-channel "
                "frames (R_cat = 0, R_cult = 12). The other three "
                "carry mixed signatures consistent with their brand "
                "positioning: Urban Decay leans canonical "
                "(R_cat = 10, R_cult = 3); Too Faced is split "
                "(R_cat = 5, R_cult = 4); Make Up For Ever leans "
                "canonical (R_cat = 6, R_cult = 1). The channel-pure "
                "cases sort the brands by Identity Load — prestige "
                "and heritage cosmetics (Estée Lauder, Clinique) in "
                "the authority pathway; cult and DTC cosmetics "
                "(Glossier) in the discourse pathway. The same "
                "Identity-Load gradient that operates on the panel-"
                "internal brands (Finding 04 below) operates on the "
                "off-panel brands. The phantom layer is not panel-"
                "incidental; it is substrate-structural."
            ),
            (
                "For brand-audit practice, the phantom layer is the "
                "structural reason a brand’s AI Availability cannot "
                "be inferred from absence on any single measurement "
                "panel. A brand not on the panel can nonetheless "
                "drive AI retrieval at measurable frequency, and its "
                "channel signature carries information about how the "
                "brand is being retrieved by which class of prompt "
                "frame. Audit procedures that rely on panel-internal "
                "scoring alone systematically miss the phantom "
                "layer; the construct must be measured against an "
                "exogenously-constructed reference vocabulary at the "
                "substrate level. The reference vocabulary for v0.21 "
                "cosmetics was constructed as the union of the "
                "panel, a pre-registered top-50 market-share list, "
                "and prior-phase Phase B emergents cross-validated "
                "by the market-share list — designed to break the "
                "endogeneity hazard that discovery-driven vocabulary "
                "expansion would introduce. Glossier was "
                "pre-registered as the validity anchor (its strong "
                "off-panel presence in v0.20 skincare and earlier-"
                "phase cosmetics observation made it the program’s a "
                "priori expected highest R_phantom) and passed at "
                "R_phantom = 12, well clear of the K = 6 threshold. "
                "The construct meets its pre-registered validity "
                "check on the calibration substrate."
            ),
            (
                "The Phantom Brand Persistence construct is "
                "calibrated on cosmetics, not yet replicated across "
                "substrates. v0.21 is the substrate where the "
                "construct was empirically motivated, where the "
                "reference vocabulary was constructed, and where the "
                "validity anchor passed. Cross-substrate replication "
                "is the genuine generalization test, and that test "
                "is v0.22+ future work — prospective phases under "
                "the locked v1.6 protocol measuring phantom-layer "
                "behavior on substrate families other than cosmetics. "
                "Brand managers reading this report should treat the "
                "phantom-layer finding as established for cosmetics, "
                "hypothesized for other substrate families, and "
                "pending prospective measurement in each new "
                "substrate where the construct’s behavior matters "
                "for brand-strategy decisions. The construct’s value "
                "as a managerial instrument is highest in substrates "
                "where the brand-of-interest’s panel-membership "
                "status is itself a moving question: emerging brands, "
                "indie tiers, and substrate categories where panel "
                "construction is contested. Practitioners can "
                "identify high-phantom-risk categories by checking "
                "whether category-best lists vary substantially "
                "across editorial sources or whether community-"
                "curated emergents regularly enter category discourse "
                "without appearing on supply-side market-share "
                "leaderboards. For categories with stable panel "
                "construction and broad market consensus on category "
                "membership, the phantom layer matters less."
            ),
        ],
    },
    {
        "number": 3,
        "title": (
            "Recall splits into two channels that can be managed "
            "separately. Rare Beauty 1:17 is the textbook diagnostic."
        ),
        "chart_slot": "f3_type2_emergence",
        "paragraphs": [
            (
                "The Recall layer of the protocol splits into two "
                "channels at the v1.5 specification. The canonical "
                "channel (R_cat) is anchored by three prompt frames: "
                "best brands in the category, most-recommended brands "
                "in the category, highest-quality brands in the "
                "category. The cultural channel (R_cult) is anchored "
                "by three prompt frames: most popular brands in the "
                "category, celebrity-favorite or influencer-driven "
                "brands in the category, viral or cult-favorite "
                "brands in the category. Each frame is sent to each "
                "of the six panel intermediaries; per-brand R_cat and "
                "R_cult are mention counts ranging 0–18 (3 frames "
                "× 6 models). The two channels operate on disjoint "
                "inputs: R_cat responds to authority surfaces — "
                "editorial coverage, expert recommendation, "
                "category-best curation, professional certification, "
                "dermatologist endorsement, makeup-artist "
                "recommendation. R_cult responds to discourse "
                "density — social-media volume, celebrity "
                "endorsement, viral content, community-curated "
                "cult-tier discourse, founder-identity association. "
                "Conflating them under a single Recall metric loses "
                "the actionable diagnosis: a brand strong on one "
                "channel and weak on the other reads as average "
                "under single-channel scoring but reads as channel-"
                "asymmetric under the two-channel decomposition, and "
                "the asymmetry is the audit signal."
            ),
            (
                "Rare Beauty is the textbook diagnostic case in v0.21 "
                "cosmetics. With Recognition saturated at C_P = 6/6 "
                "— universally categorized as a cosmetics brand by "
                "every panel intermediary — the brand’s canonical-"
                "channel Recall is 1/18 while its cultural-channel "
                "Recall is 17/18. The 1:17 split establishes the "
                "upper bound on how decoupled the two channels can be "
                "within a single brand: nearly every cultural-frame "
                "mention available, almost none of the canonical-"
                "frame mentions. Two Cell B companions joined Rare "
                "Beauty in clearing the EMERGED threshold for the "
                "Type 2 cultural-channel-preferred quadrant "
                "(R_cat ≤ 2 and R_cult ≥ 5): Huda Beauty "
                "(R_cat = 0, R_cult = 11) and Kylie Cosmetics "
                "(R_cat = 0, R_cult = 5). The three Cell B cases "
                "share a brand-positioning profile — celebrity-DTC "
                "cosmetics with founder-identity association at the "
                "substrate’s high-Identity-Load tier — and the Type "
                "2 emergence is the empirical signature of that "
                "positioning class translating to AI retrieval."
            ),
            (
                "For brand strategy, the two-channel decomposition "
                "makes interventions targetable rather than budget-"
                "consuming. A brand whose AI Availability audit "
                "returns low canonical-channel Recall has "
                "identifiable intervention pathways: build editorial-"
                "coverage relationships in the category’s authority "
                "press; pursue makeup-artist and dermatologist "
                "recommendations where the category supports them; "
                "secure category-best list inclusion at curated "
                "review surfaces; target professional-certification "
                "visibility. A brand whose audit returns low "
                "cultural-channel Recall has a different intervention "
                "class: invest in social-media volume; secure "
                "celebrity or influencer endorsement; build "
                "community-curated cult-tier discourse through "
                "founder identity and brand storytelling. A brand "
                "strong on one channel and weak on the other can "
                "target the weaker channel without trading off "
                "against the stronger; the two channels do not share "
                "input budgets and they do not compete for the same "
                "brand-strategy resources. The audit is the "
                "diagnostic, not the prescription — but the audit "
                "surfaces a structural distinction (canonical vs. "
                "cultural channel position) that the prescription "
                "can then act on without the brand-strategy team "
                "having to negotiate the intervention class as a "
                "separate question."
            ),
            (
                "Rare Beauty’s 1:17 channel split is the upper bound; "
                "the dissociation framework also identifies the "
                "inverse pole. The Type 1 pattern — canonical-"
                "channel-preferred Recall, R_cat ≥ 5 and "
                "R_cult ≤ 2 — surfaces in the v0.21 cosmetics "
                "Cell A (prestige) with Bobbi Brown (R_cat = 8, "
                "R_cult = 0) and Laura Mercier (R_cat = 5, "
                "R_cult = 0) as the channel-pure canonical anchors. "
                "The Type 1 and Type 2 poles bracket the two-channel "
                "space within a single substrate. Brand managers "
                "auditing a candidate brand can locate its position "
                "in the R_cat × R_cult plane and read its position "
                "against the substrate’s Type 1 and Type 2 anchors: "
                "a brand near a pole has identifiable intervention "
                "options matched to the dominant channel’s input "
                "class; a brand near the Iwachu region — high "
                "Recognition with low Recall in both channels — has "
                "a different question — why the categorical "
                "Recognition isn’t converting to either channel of "
                "Recall; a brand in the middle reads as positioned-"
                "but-undifferentiated and may warrant a positioning "
                "decision before an AI Availability intervention. "
                "The two-channel decomposition turns AI Availability "
                "from a single metric into an audit surface with "
                "structural geometry."
            ),
        ],
    },
    {
        "number": 4,
        "title": (
            "Identity Load predicts the AI channel where a brand "
            "will surface. Cosmetics returned the program’s first "
            "CONFIRMED moderator verdict."
        ),
        "chart_slot": "f4_il_direct_forest",
        "paragraphs": [
            (
                "Identity Load is the substrate-design property that "
                "distinguishes the panel’s cells: prestige (Cell A, "
                "medium IL — established editorial recognition and "
                "category-best curation as primary brand identity); "
                "celebrity-DTC / cult (Cell B, high IL — strong "
                "founder-identity association and community-curated "
                "discourse as primary brand identity); drugstore / "
                "mass (Cell C, low IL — distribution-led brand "
                "identity, less identity-anchored discourse). The "
                "v1.6 Increment 2 specification (SSRN 6816340) "
                "introduced the IL Direct test: per "
                "cell, δ = mean(R_cult) − mean(R_cat) is computed "
                "with a 95% percentile bootstrap confidence interval "
                "(n = 10,000), and the verdict matrix requires the "
                "CI to exclude zero in the IL-predicted direction in "
                "Cell B (the high-IL anchor, cultural-channel-"
                "leading expected); the IL-predicted opposite "
                "direction in Cell A (the medium-IL anchor, "
                "canonical-channel-leading expected); and the "
                "monotonic-gradient check Cell A δ < Cell C δ < "
                "Cell B δ across cells. The test is evaluable "
                "independently of the protocol’s Regime 4 conditions "
                "— a separation that the v1.5 framework did not "
                "permit and that v1.6 introduced specifically to "
                "surface the moderator signal where prior framework "
                "versions could not."
            ),
            (
                "The v0.21 cosmetics measurement returned CONFIRMED "
                "on the IL Direct test, with each cell’s "
                "δ falling in its predicted region and the "
                "monotonic-gradient check satisfied. Cell B δ = "
                "+7.13 with 95% bootstrap CI [+4.75, +10.25] — the "
                "program’s strongest cultural-channel-lead signal, "
                "with cultural-frame mentions outpacing canonical-"
                "frame mentions by 7.13 average across Cell B brands. "
                "(Rare Beauty’s 1:17 split from Finding 03 is the "
                "Cell B exemplar.) Cell A δ = −3.13 with CI "
                "[−6.00, −0.25] — the canonical channel leads in "
                "the medium-IL prestige cell, as the IL gradient "
                "predicts. Cell C δ = +1.00 with CI [−0.50, +3.25] "
                "— between Cell A and Cell B, satisfying the "
                "monotonic-gradient check. v0.21 is the program’s "
                "first CONFIRMED moderator verdict at any layer. The "
                "IL-gradient construct moves from a hypothesized "
                "pattern visible in earlier-phase single-channel "
                "data to a measured moderator with confidence-"
                "interval rigor."
            ),
            (
                "The skincare measurement (v0.20) returned PARTIAL "
                "on the same test, with the substrate’s IL signal "
                "carrying directionally with prediction but with "
                "substrate-specific architecture. Cell B δ = +3.75 "
                "with CI [+2.25, +5.25] cleared the IL-predicted "
                "direction. Cell A δ = +0.75 with CI [−0.25, +2.12] "
                "carried against prediction with CI overlapping "
                "zero — clinical and heritage skincare brands such "
                "as CeraVe, La Roche-Posay, and Eucerin do not "
                "concentrate in canonical-channel Recall the way "
                "prestige cosmetics brands do, because skincare’s "
                "canonical authority lives in dermatologist-"
                "recommended and clinical-result-anchored discourse "
                "rather than in editorial-prestige curation. Cell C "
                "δ = −2.50 with CI [−5.25, +0.38] broke the "
                "monotonic-gradient check with Cell A. The skincare "
                "finding is substrate-specific rather than "
                "methodology-disqualifying: the IL-gradient model "
                "holds for the substrate, but the cell where "
                "canonical authority concentrates is not the cell "
                "that the standard panel-design heuristic predicts. "
                "Indie fragrance (v0.18) carried an IL-gradient "
                "signature visible in the v1.4 single-channel data "
                "and articulated the moderator hypothesis as a "
                "coherent cross-phase question — the v1.5 two-"
                "channel decomposition was designed in response, and "
                "the v1.6 IL Direct test was specified "
                "to surface the signal more cleanly than the v1.5 "
                "framework could."
            ),
            (
                "For brand strategy, the IL-gradient moderator gives "
                "the audit a predictive prior. A brand’s cell "
                "position (and the IL construction of that cell) "
                "carries an expected channel asymmetry: high-IL "
                "cells expect cultural-channel lead; medium-IL cells "
                "expect canonical-channel lead; low-IL cells lie "
                "between under monotonic-gradient discipline. A "
                "brand whose measured channel asymmetry matches the "
                "cell’s expected asymmetry reads as cell-typical; "
                "deviation from the expected asymmetry is itself "
                "diagnostic information — the brand is operating "
                "against the cell’s IL grain, and the diagnostic "
                "surfaces the deviation as a question worth "
                "investigating (a high-IL cell brand with "
                "unexpectedly strong canonical Recall may be "
                "punching above its cell’s editorial weight; a "
                "low-IL cell brand with unexpectedly strong cultural "
                "Recall may be operating with social-media leverage "
                "uncharacteristic of its tier). One boundary is "
                "essential: Identity Load is operationalized through "
                "the substrate’s panel design, not through "
                "independently-measured consumer perceptions of the "
                "brand. The moderator operates on the panel-design "
                "construction, not on a separately-measured "
                "consumer-side construct of brand identity. The "
                "construct’s mechanism is the IL-gradient property "
                "of the substrate-as-measured, and the brand-"
                "strategy implication is bounded to substrates where "
                "the panel-design IL classification meaningfully "
                "tracks the brand-of-interest’s category positioning."
            ),
        ],
    },
    {
        "number": 5,
        "title": (
            "Methodology v1.6 closes the operational layer. Three "
            "increments shipped May 2026."
        ),
        "chart_slot": None,
        "paragraphs": [
            (
                "Protocol v1.6 (SSRN 6816340, May 2026) shipped "
                "three increments that closed three measurement gaps "
                "the prior framework versions could not address. The "
                "first increment is a substrate-level Recognition "
                "pre-screen: a substrate whose Phase A Recognition "
                "distribution is uniformly saturated — every brand "
                "recognized as a category member by every panel "
                "intermediary, in every cell — is routed to a "
                "distinct verdict state rather than collapsed into "
                "the prior framework’s FALSIFIED bucket. The second "
                "increment is an independent moderator pathway: the "
                "Identity-Load test is evaluable per-cell with "
                "bootstrap confidence intervals, separately from the "
                "protocol’s four-regime test that the prior "
                "framework coupled it to. The third increment is the "
                "Phantom Brand Persistence Phase B extension: "
                "off-panel brand presence is scored against an "
                "exogenously-constructed reference vocabulary with a "
                "persistence threshold and a validity anchor, "
                "lifting the construct from a descriptive side "
                "observation to a measured component. Each increment "
                "was specified in v1.6’s methodology paper and "
                "pre-registered at git tag v1.6-prereg-r1 before "
                "retrospective scoring was applied to the v0.16–"
                "v0.21 corpus."
            ),
            (
                "Each increment found its first measured anchor in "
                "v0.21 cosmetics. Increment 1 returned its first "
                "uniform-saturation trigger: every panel brand in "
                "every cell scored C_P = 6/6, producing distinct "
                "C_P count = 1 and modal share = 1.000 in Cell A, "
                "Cell B, and Cell C — a substrate where the prior "
                "framework’s four-regime test was not applicable, "
                "and where v1.6’s REGIME-4-UNAVAILABLE-AT-"
                "RECOGNITION verdict preserved the substrate’s "
                "evidentiary value at the moderator and phantom "
                "layers (the substrate would have read as a "
                "FALSIFIED bucket under prior framework versions, "
                "losing the discrimination signal v1.6’s pre-screen "
                "surfaces). Increment 2 returned the program’s first "
                "CONFIRMED moderator verdict at any layer, with "
                "Cell B δ = +7.13 (CI [+4.75, +10.25]), Cell A δ = −3.13 (CI "
                "[−6.00, −0.25]), Cell C δ = +1.00 (CI [−0.50, "
                "+3.25]), monotonic-gradient check satisfied. "
                "Increment 3 returned CONFIRMED with margin: six "
                "off-panel brands cleared the K = 6 persistence "
                "threshold, and the pre-registered Glossier validity "
                "anchor passed at R_phantom = 12. Together they form "
                "a coordinated audit pathway for substrates where "
                "prior framework versions would have collapsed the "
                "verdict — Increment 1 preserves the substrate’s "
                "evidentiary value, and Increments 2 and 3 carry the "
                "discrimination signal that Recognition can’t supply "
                "when it’s exhausted at ceiling."
            ),
            (
                "For the brand-strategy practitioner, v1.6’s "
                "increments translate to vocabulary the prior "
                "framework versions could not provide. A substrate "
                "where every brand is categorically recognized is "
                "now identifiable as a category where the "
                "discrimination signal lives entirely in Recall — a "
                "vocabulary distinction that lets brand managers "
                "diagnose maximally-coded categories (cosmetics is "
                "the first measured example; other consumer-facing "
                "categories with broad media coverage and stable "
                "category-membership consensus are candidates for "
                "similar shape) without conflating them with "
                "categories where Recognition itself carries the "
                "diagnostic signal. The moderator pathway makes "
                "Identity-Load asymmetry an audit input, not an "
                "inferred property — the audit returns δ values with "
                "bootstrap CIs, and brand managers can compare a "
                "brand’s cell-relative position against the cell’s "
                "measured asymmetry directly. The phantom layer "
                "measures off-panel presence, which means brand "
                "audits for emerging brands not yet on standard "
                "category-tracking panels can include AI Availability "
                "as a measurable construct rather than treating "
                "panel-absence as missing data. v0.22 and successor "
                "phases apply v1.6 prospectively to new substrate "
                "families under the same locked protocol; the "
                "operational layer is what each new prospective "
                "phase consumes, not what each new phase has to "
                "first redefine."
            ),
            (
                "AIAS™ 1.0 names the Presence component of the AIAS "
                "construct, not the full multi-component composite. "
                "The Tri-System framework names the composite as a "
                "0–100 score across six measurable dimensions — "
                "Presence, Ranking, Consistency, Coverage, Grounding, "
                "Sentiment — and positions the composite as a "
                "multi-year research arc. AIAS™ 1.0 operationalizes "
                "the first of those six dimensions; the remaining "
                "five ship under a Phase 4 successor program with "
                "specifications, verdict matrices, and "
                "pre-registration discipline reserved for that "
                "program’s pre-registration round. The version-"
                "number arc is load-bearing: 1.0 names the moment "
                "when the construct’s first component reaches "
                "falsifiable measurement against a cross-substrate "
                "anchor base, and the version increments that follow "
                "will track the measurement surface rather than the "
                "architectural ambition. The construct does not "
                "jump to 2.0 by claiming additional components "
                "without measuring them. For brand managers "
                "consuming the report’s findings, the boundary is "
                "the program’s credibility asset — what AIAS 1.0 "
                "measures is what it claims to measure, and the "
                "multi-year roadmap is signposted, not over-claimed."
            ),
        ],
    },
]


# ---------------------------------------------------------------------------
# LIMITATIONS — heading + paragraphs
# 5 paragraphs / ~715 words (vs v21's 4 paragraphs single-phase scope).
# ---------------------------------------------------------------------------

LIMITATIONS = {
    "heading": "Limitations",
    "paragraphs": [
        (
            "The reference panel is held fixed at the v0.17 six-slot "
            "specification across all phases of the synthesis: Claude "
            "Opus 4.5, Claude Sonnet 4.5, GPT-4o, GPT-4o-mini, Gemini "
            "2.5 Flash, and Gemini 2.5 Flash Lite. Holding the panel "
            "fixed across phases is the program’s cross-phase "
            "comparability discipline. It is also a measurement-"
            "window constraint: the v0.21 verdicts and all earlier-"
            "phase verdicts are properties of brand × substrate × "
            "panel triples evaluated at acquisition time, not "
            "permanent properties of the substrate. Provider model "
            "substitutions over future-phase horizons are expected, "
            "and the construct’s stability across model generations "
            "is itself future-work to demonstrate. Brand managers "
            "reading verdicts should treat them as measurements "
            "anchored in a specific panel state, with the panel’s "
            "evolution itself a subject for the program’s continued "
            "discipline."
        ),
        (
            "Four of the five substrate families operated in "
            "English-language consumer-discovery environments. The "
            "kitchenware family’s substrate-language carryforward at "
            "v0.16 — where Japanese-language category-bound discourse "
            "surfaced different brand mention patterns than English-"
            "language responses for the same substrate — is the "
            "program’s only cross-language acquisition. Cross-"
            "language replication is future work. The construct may "
            "behave structurally differently in substrates where "
            "consumer discovery operates in non-English discourse "
            "environments, and the panel intermediaries’ English-"
            "language training bias is a known structural feature of "
            "the measurement system. Brand managers in markets where "
            "the brand-of-interest’s consumer-discovery surface is "
            "non-English should treat the report’s findings as "
            "suggestive rather than directly transferable, pending "
            "prospective cross-language replication phases."
        ),
        (
            "Cell-classification limits surfaced through the e.l.f. "
            "Cosmetics out-of-cell Type 2 case noted in Finding 01 "
            "¶3 and Finding 03 ¶4. The IL-gradient cell structure "
            "assumes brands behave per their supply-side tier "
            "classification — a drugstore/mass brand should sit in "
            "Cell C, a celebrity-DTC brand in Cell B, a prestige "
            "brand in Cell A — and a brand whose observable channel "
            "behavior crosses the supply-side / discourse-side "
            "boundary exposes friction in the classification scheme. "
            "e.l.f. Cosmetics has drugstore/mass price points (Cell "
            "C by panel design) but a social-media-native cultural "
            "footprint that produces Type 2 dissociation more "
            "characteristic of Cell B brands. The classification "
            "scheme remains useful at the aggregate level — the IL "
            "gradient holds for cell-typical brands — but brand "
            "managers auditing brands at the supply-side / "
            "discourse-side boundary should expect classification "
            "friction."
        ),
        (
            "The synthesis honors the v1.6-locked retrospective-"
            "scoring boundary without extension. Increment 1 "
            "(substrate Recognition pre-screen) classifies all six "
            "phases by narrative or by scoring, depending on the "
            "phase’s data shape. Increment 2 (IL Direct) "
            "is bounded to v0.20 and v0.21 — the only phases that "
            "acquired R_cult data under the v1.5 two-channel design. "
            "Increment 3 (Phantom Brand Persistence) is bounded to "
            "v0.21, the substrate where the construct was "
            "empirically motivated and where the validity anchor was "
            "anchored. The boundary is methodology discipline, not "
            "data — extending Increments 2 and 3 retrospectively "
            "beyond their stated scope would require either "
            "retrospective channel re-mapping (which the program has "
            "explicitly disallowed) or post-hoc reference-vocabulary "
            "construction (which would compromise the validity "
            "anchor’s pre-registration). Brand managers should read "
            "v0.16–v0.19 verdicts as v1.4-era authoritative within-"
            "phase results, with v1.6 framing added only where the "
            "retrospective scope supports it."
        ),
        (
            "The synthesis claims measurability of the Presence "
            "component across five substrate families. It does not "
            "claim construct validity. Predictive validity against "
            "behavioral outcomes (whether AI Availability scores "
            "predict consideration, search, or purchase behavior), "
            "convergent validity across alternative panel "
            "constructions (whether other panel compositions yield "
            "the same brand-rank ordering), and discriminant validity "
            "against Mental and Physical Availability (whether AI "
            "Availability captures variance the existing constructs "
            "do not) are Phase 3 future work and are not established "
            "here. The consumer-behavior correlate of AI Availability "
            "is plausible on theoretical grounds — the Ehrenberg-"
            "Bass canon’s logic implies that availability constructs "
            "should be load-bearing for category buying — but the "
            "present program has not measured the correlation. Brand "
            "managers should treat AI Availability as a measurement-"
            "program construct with anchored measurability and "
            "bounded scope, not as a predictor of downstream consumer "
            "behavior pending Phase 3 evidence."
        ),
    ],
}


# ---------------------------------------------------------------------------
# WHATS_NEXT — heading + paragraphs
# 5 paragraphs / ~700 words (vs v21's 3-paragraph single-phase scope).
# ---------------------------------------------------------------------------

WHATS_NEXT = {
    "heading": "What’s next",
    "paragraphs": [
        (
            "The immediate next deliverable is v0.22, the program’s "
            "first prospective phase under the locked v1.6 protocol. "
            "Substrate selection is open: candidates include "
            "automotive (a substrate with a different IL-gradient "
            "shape — brand identity carries strong individual-"
            "purchase identity but the discovery surface is "
            "dominated by review-channel discourse), consumer "
            "electronics outside audio (where heritage, cult, and "
            "mass tiers may map cleanly to the standard panel "
            "design), or premium spirits (where editorial authority "
            "and cultural-cult dimensions both run strong). Each "
            "candidate would test v1.6’s three increments "
            "prospectively against a substrate not in the present "
            "retrospective scope. Pre-registration locks the panel "
            "and verdict matrices before acquisition, as the "
            "program’s standing discipline requires."
        ),
        (
            "Phase 3 is construct validation. Predictive validity "
            "against behavioral outcomes — whether AI Availability "
            "scores predict consumer behavior such as consideration, "
            "search, or purchase — is the discipline’s primary "
            "validation criterion and the program’s Phase 3 anchor. "
            "The Phase 3 design requires a behavioral-outcome "
            "dataset paired with AI Availability scores measured at "
            "the same brand × substrate boundary, against panel "
            "constructions held fixed for measurement comparability "
            "and varied for convergent-validity testing. Discriminant "
            "validity against Mental Availability and Physical "
            "Availability requires paired measurements of all three "
            "constructs against a common brand × substrate cohort. "
            "Both validation arcs sit in the Phase 3 pre-registration "
            "roadmap; neither is in the present synthesis’s claim "
            "scope."
        ),
        (
            "Phase 4 is the full six-component AIAS™ composite. The "
            "Tri-System framework names the composite as a 0–100 "
            "score across Presence (operationalized by the present "
            "synthesis), Ranking (which brand surfaces first), "
            "Consistency (how stable the ranking is across panel "
            "intermediaries), Coverage (how completely the panel "
            "surfaces the category’s relevant brand set), Grounding "
            "(whether brand mentions are accompanied by category-"
            "relevant context), and Sentiment (how favorable the "
            "mention’s affective framing is). The remaining five "
            "components ship under a Phase 4 successor program at "
            "the level of intent only; component-level "
            "prioritization, panel-design implications, and "
            "methodology successors will follow the same pre-"
            "registration discipline that v1.2 through v1.6 "
            "established for the Presence layer. The composite "
            "reaches a fully-measured 6.0 state only when all six "
            "components have been operationalized to the standard "
            "the Presence component reaches in the present synthesis."
        ),
        (
            "Cross-language replication is the construct’s second "
            "expansion axis. Non-English-language substrate phases "
            "— Japanese, Spanish, Mandarin, and others selected on "
            "substrate-availability grounds — will test whether the "
            "construct’s measurement procedure transfers across "
            "discourse-language boundaries with the panel-internal "
            "scoring discipline held fixed. Panel-construction "
            "sensitivity is the third axis: studies that hold "
            "substrate and methodology version fixed while varying "
            "the panel — substituting providers, varying panel "
            "size, testing single-provider panels against multi-"
            "provider panels — will supply the convergent-validity "
            "evidence base that Phase 3 construct validation "
            "requires. The three expansion axes (substrate, "
            "language, panel-construction) together carry the "
            "construct’s empirical anchor base from the present "
            "five families into a sustained replication program "
            "under the program’s standing pre-registration "
            "discipline."
        ),
        (
            "For brand managers planning against the construct’s "
            "evolution, three timelines matter. AIAS 1.0’s Presence "
            "component is anchored on cosmetics and four other "
            "families as of May 2026; new substrate families ship "
            "at the program’s pace under v1.6 lock. Phase 3 "
            "construct validation is multi-year work that "
            "establishes whether AI Availability scores predict "
            "downstream consumer behavior — until that work ships, "
            "brand managers should treat AI Availability as a "
            "measurable property of brand × substrate × panel "
            "triples without inferring behavioral consequences. "
            "Phase 4 composite expansion is the longest-horizon "
            "arc; the version-number arc 1.0 → 6.0 will track the "
            "measurement surface rather than architectural "
            "ambition. Brand managers consuming the report should "
            "plan against the present anchored claim and against "
            "the future-work claims as separate planning tracks, "
            "with the construct’s evolution timeline as the "
            "resource-allocation input."
        ),
    ],
}


# ---------------------------------------------------------------------------
# PROPOSITION_SCORING — heading + intro + rows (5-tuples)
# Row format: (p_id, proposition, result, status_text, status_class)
# status_class ∈ {"confirmed", "partial", "disconfirmed", "descriptive"}
# ---------------------------------------------------------------------------

PROPOSITION_SCORING = {
    "heading": "Five propositions, anchored",
    "intro": (
        "Five propositions consolidate the five-substrate empirical "
        "anchor base into actionable framing for brand strategy. Each "
        "is anchored against the data the program has shipped under "
        "locked methodology v1.6. The table below states each "
        "proposition, the substantive evidence that anchors it, and "
        "the status as of the AIAS™ 1.0 milestone. The detailed "
        "interpretation of each — what it means, what it does not "
        "mean — follows in the section below the table."
    ),
    "rows": [
        (
            "P1",
            "AI Availability is a measurable third channel of brand "
            "presence, anchored across five substrate families.",
            "Five families measured under one locked methodology "
            "version (v1.6, SSRN 6816340): kitchenware, indie "
            "fragrance, audiophile electronics, skincare, cosmetics. "
            "Six pre-registered measurement events March–May 2026.",
            "ANCHORED",
            "confirmed",
        ),
        (
            "P2",
            "Off-panel brand presence is real and tracks Identity "
            "Load. Brands not on a measurement panel can still drive "
            "AI retrieval with auditable channel signatures.",
            "Six off-panel cosmetics brands cleared K = 6. Estée "
            "Lauder + Clinique canonical-pure (R_cult = 0); Glossier "
            "cultural-pure (R_cat = 0). Glossier validity anchor "
            "passed at R_phantom = 12.",
            "CALIBRATED",
            "confirmed",
        ),
        (
            "P3",
            "Recall splits into a canonical channel (R_cat) and a "
            "cultural channel (R_cult) that operate on disjoint "
            "inputs and can be managed separately.",
            "Rare Beauty textbook anchor: C_P = 6/6, R_cat = 1, "
            "R_cult = 17. Type 2 EMERGED with three Cell B cosmetics "
            "cases (Rare Beauty, Huda Beauty 0:11, Kylie Cosmetics "
            "0:5).",
            "CONFIRMED",
            "confirmed",
        ),
        (
            "P4",
            "Identity Load predicts the AI channel where a brand "
            "will surface. Cell position carries an expected channel "
            "asymmetry that the audit can compare brand performance "
            "against.",
            "v0.21 cosmetics returned the program’s first CONFIRMED "
            "moderator at any layer. Cell B’s cultural channel led by "
            "7.13 mentions on average — the strongest IL-predicted "
            "asymmetry signal in the program. Cell A canonical-led by "
            "3.13; Cell C balanced. All three cells matched the "
            "IL-gradient prediction with confidence-interval margin.",
            "CONFIRMED",
            "confirmed",
        ),
        (
            "P5",
            "Methodology v1.6 closes the operational layer. Three "
            "increments shipped May 2026 make P2 through P4 "
            "measurable.",
            "Substrate Recognition pre-screen (Inc 1) + independent "
            "moderator pathway (Inc 2) + Phantom Brand Persistence "
            "(Inc 3). Each load-bearing for v0.21 verdicts.",
            "SHIPPED v1.6",
            "confirmed",
        ),
    ],
}


# ---------------------------------------------------------------------------
# PROPOSITION_DETAILS — heading + intro + items (2-tuples)
# Item format: (p_id, body_text)
# ---------------------------------------------------------------------------

PROPOSITION_DETAILS = {
    "heading": "Proposition interpretation",
    "intro": (
        "Each proposition carries substantive interpretation beyond "
        "the table-row summary. The verdicts are what the data "
        "produced; the meaning of each verdict for the construct, the "
        "brand-strategy practitioner, and the v0.22+ trajectory is "
        "what the prose below addresses, structured as “What it "
        "means” + “What it doesn’t mean” per proposition."
    ),
    "items": [
        (
            "P1",
            "<b>What it means.</b> AI Availability has graduated from "
            "a construct claimed on one or two substrate-family "
            "anchors to a construct that holds across five distinct "
            "families measured under one locked methodology. The "
            "empirical base is sufficient for the program to apply "
            "the construct to new substrate families as candidates "
            "for prospective measurement, and for brand-strategy "
            "practitioners to consume the construct as a stable "
            "measurement instrument rather than a moving-target "
            "methodology. The five families span three distinct "
            "consumer-discovery environments (editorial-authority, "
            "community-curated, social-media-native), and the "
            "construct’s verdicts hold across all three. <b>What it "
            "doesn’t mean.</b> ANCHORED is not the same as construct "
            "validity. The synthesis claims measurability — that AI "
            "Availability can be measured under a falsifiable "
            "pre-registered protocol with cross-substrate "
            "replicability — not predictive validity against "
            "behavioral outcomes. Whether AI Availability scores "
            "predict consumer behavior (consideration, search, "
            "purchase) is Phase 3 future work and is not established "
            "by the present anchor base. The full six-component "
            "AIAS™ composite (Ranking, Consistency, Coverage, "
            "Grounding, Sentiment) is reserved for a Phase 4 "
            "multi-year program. The present claim is bounded to "
            "Presence-component measurability across five substrate "
            "families, and the program’s credibility rests on that "
            "bounded claim rather than on an over-claimed composite "
            "the data does not yet carry."
        ),
        (
            "P2",
            "<b>What it means.</b> A brand’s AI Availability cannot "
            "be inferred from absence on any single measurement "
            "panel. The phantom layer surfaces off-panel brands at "
            "measurable frequency, with channel signatures that "
            "track the same Identity-Load gradient as the panel-"
            "internal brands. The construct’s value as a managerial "
            "instrument is highest in substrates where the brand-of-"
            "interest’s panel-membership status is itself a moving "
            "question — emerging brands, indie tiers, and substrate "
            "categories where panel construction is contested. "
            "Practitioners can identify high-phantom-risk categories "
            "by checking whether category-best lists vary "
            "substantially across editorial sources or whether "
            "community-curated emergents regularly enter category "
            "discourse without appearing on supply-side market-share "
            "leaderboards. <b>What it doesn’t mean.</b> CALIBRATED "
            "is not the same as cross-substrate replicated. v0.21 "
            "cosmetics is the calibration anchor — the substrate "
            "where the construct was empirically motivated, where "
            "the reference vocabulary was constructed, and where the "
            "validity anchor (Glossier R_phantom = 12) passed. "
            "Cross-substrate replication is the genuine "
            "generalization test, and that test is v0.22+ future "
            "work — prospective phases under the locked v1.6 "
            "protocol measuring phantom-layer behavior on substrate "
            "families other than cosmetics. Brand managers reading "
            "this report should treat the phantom-layer finding as "
            "established for cosmetics, hypothesized for other "
            "substrate families, and pending prospective measurement "
            "in each new substrate where the construct’s behavior "
            "matters for brand-strategy decisions."
        ),
        (
            "P3",
            "<b>What it means.</b> R_cat and R_cult operate on "
            "disjoint inputs and can be managed separately. A brand "
            "with low canonical-channel Recall has identifiable "
            "intervention pathways in authority surfaces (editorial "
            "coverage, expert recommendation, category-best "
            "curation, professional certification); a brand with low "
            "cultural-channel Recall has a different intervention "
            "class in discourse density (social-media volume, "
            "celebrity endorsement, viral content, community-curated "
            "cult-tier discourse). Rare Beauty’s 1:17 channel split "
            "establishes the upper bound on how decoupled the two "
            "channels can be within a single brand, and the "
            "dissociation framework identifies the inverse pole at "
            "the Type 1 anchors (Bobbi Brown 8:0, Laura Mercier 5:0 "
            "in v0.21 Cell A). <b>What it doesn’t mean.</b> Two-"
            "channel decomposition does not mean every brand should "
            "target both channels equally. The audit returns the "
            "brand’s current channel position; the brand-strategy "
            "prescription depends on the brand’s positioning and the "
            "cell’s IL construction. A celebrity-DTC brand may "
            "correctly concentrate in the cultural channel; a "
            "heritage prestige brand may correctly concentrate in "
            "the canonical channel; the diagnostic is the audit "
            "surface, not the prescription. Conflating audit with "
            "prescription would reintroduce the single-channel "
            "framing the two-channel decomposition was designed to "
            "escape. The audit’s contribution is structural: it "
            "surfaces the channel distinction so the brand-strategy "
            "team can decide whether the brand’s current position "
            "matches the brand’s intent, and act on the gap "
            "directly rather than negotiating which intervention "
            "class applies as a separate question."
        ),
        (
            "P4",
            "<b>What it means.</b> Identity Load — operationalized "
            "through the substrate’s panel design — empirically "
            "predicts the AI channel where a brand will surface, "
            "with confidence-interval rigor. A brand’s cell position "
            "carries a predictive prior: high-IL cells expect "
            "cultural-channel lead; medium-IL cells expect "
            "canonical-channel lead; low-IL cells lie between under "
            "monotonic-gradient discipline. v0.21 cosmetics is the "
            "program’s first CONFIRMED moderator verdict at any "
            "layer (Cell B δ = +7.13 with CI [+4.75, +10.25]; Cell A "
            "δ = −3.13 with CI [−6.00, −0.25]; Cell C δ = +1.00 "
            "with CI [−0.50, +3.25]; all in IL-predicted regions). "
            "Brand managers auditing brands can compare a brand’s "
            "measured channel asymmetry against the cell’s expected "
            "asymmetry directly — deviation from expectation is "
            "itself diagnostic information. <b>What it doesn’t "
            "mean.</b> Identity Load is operationalized through the "
            "substrate’s panel design, not through independently-"
            "measured consumer perceptions of the brand. The "
            "moderator operates on the panel-design construction, "
            "not on a separately-measured consumer-side construct "
            "of brand identity. The construct’s mechanism is the "
            "IL-gradient property of the substrate-as-measured, and "
            "the brand-strategy implication is bounded to substrates "
            "where the panel-design IL classification meaningfully "
            "tracks the brand-of-interest’s category positioning. "
            "v0.20 skincare’s PARTIAL on the same test surfaced "
            "substrate-specific architecture — the cell where "
            "canonical authority concentrates is substrate-"
            "dependent, not panel-design-invariant. Clinical and "
            "dermatologist-anchored authority in skincare lives in "
            "a different cell position than editorial-prestige "
            "authority in cosmetics. The moderator holds for the "
            "substrate; the cell-architecture assumption requires "
            "substrate-aware interpretation."
        ),
        (
            "P5",
            "<b>What it means.</b> Methodology v1.6 closed three "
            "measurement gaps the prior framework versions could "
            "not address: substrate-level Recognition pre-screen "
            "(so maximally-coded categories like cosmetics don’t "
            "collapse the verdict matrix); independent moderator "
            "pathway (so Identity-Load asymmetry is evaluable "
            "separately from the four-regime test); Phantom Brand "
            "Persistence Phase B extension (so off-panel brand "
            "presence is a measured component rather than a "
            "descriptive side observation). Together the three form "
            "a coordinated audit pathway for substrates where prior "
            "framework versions would have collapsed the verdict — "
            "Increment 1 preserves the substrate’s evidentiary "
            "value, and Increments 2 and 3 carry the discrimination "
            "signal that Recognition can’t supply when it’s "
            "exhausted at ceiling. <b>What it doesn’t mean.</b> "
            "SHIPPED v1.6 does not mean the construct is "
            "methodology-complete. v1.7 (if it ships) would extend "
            "the protocol further — the program’s methodology arc "
            "is ongoing, not closed. The v1.6 increments are "
            "bounded to the retrospective scope where the v1.6 "
            "paper’s published rules permit them (Increment 2 for "
            "v0.20 + v0.21; Increment 3 for v0.21 only). Cross-"
            "substrate replication of Increments 2 and 3 is v0.22+ "
            "work. AIAS™ 1.0 names the Presence component of the "
            "AIAS construct, not the full multi-component composite "
            "— and the version-number arc 1.0 → 6.0 will track "
            "the measurement surface (each new component reaching "
            "falsifiable measurement) rather than architectural "
            "ambition."
        ),
    ],
}


# ---------------------------------------------------------------------------
# CLOSING — byline_long + datasets + methodology_log
# ---------------------------------------------------------------------------

CLOSING = {
    "byline_long": [
        "Pablo Ulpiano González Castro",
        "School of Visual Arts, MPS Branding Program · New York, NY",
        "Third System™ (research entity; data archive and methodology venue)",
        "Correspondence: pablou@pablou.com · ORCID: 0009-0003-8968-9990",
    ],
    "datasets": [
        "AIAS 1.0 synthesis data (cross-phase source-of-truth, locked "
        "at aias-1-0-data-locked): "
        "osf.io/ec6wh/aias_1_0/aias_1_0_synthesis_data.json",
        "Phase-level acquisitions, scoring code, and verdict matrices "
        "(v0.16 through v0.21): osf.io/ec6wh/v16/ through "
        "osf.io/ec6wh/v21/ (six per-phase deposit trees)",
        "Methodology papers v1.2 through v1.6 (pre-registrations, "
        "retrospective scoring outputs, increment specifications): "
        "osf.io/ec6wh/methodology/v1_2/ through "
        "osf.io/ec6wh/methodology/v1_6/",
        "AIAS 1.0 charts (academic synthesis paper figures + brand-"
        "format report upgrades): osf.io/ec6wh/aias_1_0/figures/",
        "Pre-registration lock artifacts (outline, data, charts, "
        "paper): git tags aias-1-0-outline-locked, "
        "aias-1-0-data-locked, aias-1-0-charts-locked, "
        "aias-1-0-paper-locked in the repository",
    ],
    "methodology_log": (
        "AIAS 1.0 synthesis paper locked at git tags "
        "aias-1-0-outline-locked, aias-1-0-data-locked, "
        "aias-1-0-charts-locked, and aias-1-0-paper-locked. Academic "
        "companion deposited at SSRN 6817841 (May 2026). Methodology "
        "version: v1.6 (SSRN 6816340). This brand-format report "
        "ships two weeks behind the SSRN deposit per the program’s "
        "two-register discipline"
    ),
}
