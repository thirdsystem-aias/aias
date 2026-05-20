"""
v0.18 Indie Fragrance — Brand-format report content.

Consumed by reports/build_report_v18.py (ReportLab + pypdf two-pass overlay).
All [TBD-*] markers from the pre-acquisition draft are now resolved against
the actual v0.18 verdict (data/verdicts/v0_18_verdict.{json,md}).

Brand tokens (Third System Indigo #37237B primary) are sourced from
brand/third_system_brand.json by the build script. Akkurat Pro auto-detection
from ~/.fonts/Akkurat and ~/Library/Fonts is also handled by the build script.

Section IDs follow the same convention as v15/v16/v17 content modules so the
build script can iterate sections uniformly.

Citation chain:
  - AIAS Protocol v1.4 (SSRN 6799479) — methodology base
  - v0.16 (SSRN 6791999), v0.17 (SSRN 6802261) — predecessor legs
  - Pre-reg tag v0.18-prereg-r1 at commit 183386c, r4 at commit 1195cb8
"""

# ---------------------------------------------------------------------------
# COVER
# ---------------------------------------------------------------------------

COVER = {
    "phase_id": "v0.18",
    "substrate_label": "Indie Fragrance",
    "report_kind": "Phase Findings Report",
    "title": "When Recognition Meets Recall",
    "interpretive_subtitle": (
        "The Recognition \u00d7 Recall dissociation generalizes to a "
        "same-language substrate. The Identity-Load moderator operates, "
        "but bounded. Three PARTIAL verdicts that say more together than apart."
    ),
    "author_block": [
        "Pablo Ulpiano Gonz\u00e1lez Castro",
        "School of Visual Arts, MPS Branding Program (primary academic affiliation)",
        "Third System\u2122 \u2014 research entity",
    ],
    "date_label": "May 2026",
    "phase_tag": "v0.18-prereg-r1 \u00b7 commit 183386c \u00b7 refined through r4 at 1195cb8",
    "methodology_citation": "AIAS\u2122 Presence Measurement Protocol v1.4 (SSRN 6799479)",
    "deposit_uri": "osf.io/ec6wh/v18/",
}


# ---------------------------------------------------------------------------
# EXECUTIVE SUMMARY
# ---------------------------------------------------------------------------

EXECUTIVE_SUMMARY = {
    "what_we_found": (
        "Nine cases of Recognition without Recall, on a same-language fragrance "
        "substrate. The Iwachu pattern \u2014 brands that AI systems recognize as "
        "category members but do not surface when asked to enumerate the category "
        "\u2014 is not specific to the cross-cultural anchor that first identified it. "
        "It generalizes. And it concentrates where it should: 6 of the 9 cases "
        "fall in the highest-Identity-Load cell (indie/artisan, 75% of cell brands)."
    ),
    "what_this_means": (
        "The AIAS\u2122 Presence Measurement Protocol's multi-component construct "
        "(Recognition + Recall) gains its first generalization anchor. Before "
        "v0.18, the construct rested on one case from a Japanese-cell substrate; "
        "now it rests on ten cases across two substrate families. The Identity-Load "
        "moderator is real but bounded \u2014 it operates through layer-specific "
        "channels (Recognition-floor at one boundary, dissociation pattern at "
        "another) that older single-dimensional frameworks could not surface. "
        "For senior brand leaders: the gap between what an AI knows about your "
        "brand and what it will say about your brand is a measurable, "
        "category-level quantity. v0.18 puts a number on the gap."
    ),
    "three_verdicts": [
        {
            "hypothesis": "H_Regime4_indie_fragrance",
            "verdict": "PARTIAL",
            "shortform": (
                "C1 panel adequacy + C2 within-cell + C2 IL-gradient all clear. "
                "C3 ranking coherence fails on cells with degenerate variance "
                "(only Cell C clears the 0.50 rho threshold)."
            ),
        },
        {
            "hypothesis": "H_IdentityLoad_moderator (three-leg joint)",
            "verdict": "PARTIAL",
            "shortform": (
                "v0.16 PARTIAL x v0.17 FALSIFIED x v0.18 PARTIAL. Moderator "
                "operates with substrate-specific qualifications; layer-specific "
                "channels (Recognition vs. Recall) act differently."
            ),
        },
        {
            "hypothesis": "H_Recognition_Recall_dissociation_generalization",
            "verdict": "DISSOCIATION_PARTIAL",
            "shortform": (
                "9 Iwachu-pattern cases in 2 of 3 cells. v1.4 multi-component "
                "construct generalizes from cross-cultural to same-language "
                "substrate. Cell C contributes zero by Recognition-floor design."
            ),
        },
    ],
}


# ---------------------------------------------------------------------------
# Section 01 - Purpose and substrate
# ---------------------------------------------------------------------------

SECTION_01_PURPOSE_AND_SUBSTRATE = {
    "id": "01_purpose_and_substrate",
    "heading": "Purpose and substrate",
    "lede": (
        "v0.18 tests two pre-registered hypotheses on a single substrate: "
        "(a) whether the Identity-Load moderator hypothesis from v0.16/v0.17 "
        "operates on a third leg, and (b) whether the Recognition \u00d7 Recall "
        "dissociation pattern from v0.17 generalizes beyond its original "
        "cross-cultural anchor."
    ),
    "body_paragraphs": [
        "The AIAS\u2122 Presence Measurement Protocol operationalizes AI Availability \u2014 "
        "the brand-level probability of retrieval, recommendation, or selection "
        "by an AI intermediary \u2014 as the third measurable layer alongside the "
        "Ehrenberg-Bass tradition's Mental and Physical Availability.",

        "Protocol v1.4 (SSRN 6799479) refined the AI Availability construct from "
        "a single-dimensional measure into a multi-component decomposition: "
        "Recognition (does the AI recognize the brand as a category member?) "
        "and Recall (does the AI surface the brand when asked to enumerate the "
        "category?). Until v0.18, the multi-component construct rested on one "
        "empirical anchor \u2014 the Iwachu dissociation observed on the v0.17 "
        "Japanese-cell substrate (Recognition = 6/6, Recall = 0/18).",

        "The substrate for v0.18 is indie fragrance: a culturally and personally "
        "identity-bearing category, English-language-anchored throughout, "
        "admitting a clean three-tier Identity-Load stratification. Three cells "
        "of 8 brands each. The locked six-slot reference panel from v0.17 is "
        "carried forward (claude-opus-4-5, claude-sonnet-4-5, gpt-4o, gpt-4o-mini, "
        "gemini-2.5-flash, gemini-2.5-flash-lite). Phase B uses a three-frame "
        "query battery: niche, independent, and perfumistas anchors.",
    ],
    "panel_table": {
        "caption": "v0.18 brand panel by Identity-Load cell (n = 24 worldwide pre-floor).",
        "columns": ["IL tier", "Cell", "Brands"],
        "rows": [
            ["Medium IL", "Cell C \u2014 Mass-prestige (comparison anchor)",
             "Chanel \u00b7 Dior \u00b7 YSL \u00b7 Tom Ford \u00b7 Givenchy \u00b7 Versace \u00b7 Marc Jacobs \u00b7 Calvin Klein"],
            ["Medium-high IL", "Cell A \u2014 Designer-niche",
             "Maison Francis Kurkdjian \u00b7 Le Labo \u00b7 Diptyque \u00b7 Frederic Malle \u00b7 "
             "Byredo \u00b7 Comme des Gar\u00e7ons Parfums \u00b7 Memo Paris \u00b7 Etat Libre d'Orange"],
            ["High IL", "Cell B \u2014 Indie / Artisan",
             "D.S. & Durga \u00b7 Boy Smells \u00b7 Heretic Parfum \u00b7 Ellis Brooklyn \u00b7 "
             "Vyrao \u00b7 Henry Rose \u00b7 Phlur \u00b7 Snif"],
        ],
    },
}


# ---------------------------------------------------------------------------
# Section 02 - Design
# ---------------------------------------------------------------------------

SECTION_02_DESIGN = {
    "id": "02_design",
    "heading": "Design",
    "lede": (
        "Two phases. Phase A measures Recognition. Phase B measures Recall. "
        "Phase D computes within-cell rank correlation. The three verdicts "
        "are scored from these phases by pre-registered decision rules."
    ),
    "body_paragraphs": [
        "Phase A asks each of the six reference panel models a single question "
        "per brand: 'Is this brand commonly recognized as a niche fragrance?' "
        "The brand's Recognition score (C_P, range 0..6) is the count of "
        "recognition-positive responses across the panel.",

        "Phase B asks each of the six reference panel models three queries about "
        "the category \u2014 'What are the best niche fragrances?', 'Recommend "
        "high-quality independent fragrance brands.', 'What fragrances do "
        "industry insiders and perfumistas recommend?' \u2014 and scans each response "
        "for brand mentions across the 24-brand registry. Each brand has at most "
        "18 observation slots (3 queries x 6 models).",

        "The Recognition \u00d7 Recall dissociation threshold (the Iwachu-pattern "
        "case) requires C_P \u2265 5/6 and mention rate \u2264 2/18 \u2014 the brand is "
        "recognized in 5+ of 6 single-brand probes, but surfaces in 2 or fewer "
        "of 18 enumeration responses.",
    ],
    "verdict_logic_summary": (
        "H_Regime4_indie_fragrance verdict cascade per pre-reg r4 \u00a74.0: "
        "C1 (panel adequacy, worldwide n \u2265 12) \u2192 C2 within-cell "
        "(per-cell top-2 mention share \u2265 0.50) \u2192 C2 IL-gradient "
        "(Cell B share \u2212 Cell C share \u2265 0.10) \u2192 C3 ranking coherence "
        "(per-cell Spearman rho \u2265 0.50 in at least 2 of 3 cells)."
    ),
}


# ---------------------------------------------------------------------------
# Section 03 - Findings: Recognition
# ---------------------------------------------------------------------------

SECTION_03_FINDINGS_RECOGNITION = {
    "id": "03_findings_recognition",
    "heading": "Findings \u2014 Recognition",
    "lede": (
        "Recognition shows a strong, threshold-shaped Identity-Load gradient. "
        "Cell C is below the category-recognition floor entirely. Cells A and B "
        "are near-saturated, with Cell A slightly higher than Cell B against "
        "strict monotonicity \u2014 itself a substantive finding about how 'niche' "
        "as a lexical anchor maps onto the consumer-discovery surface."
    ),
    "recognition_table": {
        "caption": (
            "Phase A Recognition (C_P score, 0\u20136) per cell. Mean and range "
            "across the 8 cell brands."
        ),
        "columns": ["Cell", "Mean C_P", "Range", "Pivot"],
        "rows": [
            ["Cell C \u2014 Mass-prestige", "0.25 / 6", "0 \u2013 2 (Tom Ford alone at 2)",
             "Cascade exhausted (DEVIATIONS Entry 1)"],
            ["Cell A \u2014 Designer-niche", "5.88 / 6", "5 \u2013 6 (7 of 8 at 6/6)",
             "Maison Francis Kurkdjian (anchored at first step)"],
            ["Cell B \u2014 Indie / Artisan", "5.00 / 6", "3 \u2013 6 (varied)",
             "D.S. & Durga (anchored at first step)"],
        ],
    },
    "interpretation_paragraphs": [
        "The Cell C \u2192 Cell A transition is a step function, not a smooth "
        "gradient. The 'niche fragrance' Recognition probe maps cleanly onto "
        "designer-niche and indie/artisan houses (Cells A and B) but cleanly "
        "off mass-prestige designer fragrance (Cell C). The asymmetry isn't a "
        "panel construction error; it's the IL-gradient operating on Recognition "
        "itself. Mass-prestige fragrance is, by definition, not niche.",

        "The Cell A > Cell B inversion (5.88 vs. 5.00) is also substantive: "
        "the lexical anchor 'niche fragrance' maps most tightly to canonically-"
        "labeled designer-niche houses (Le Labo, Frederic Malle, Diptyque) than "
        "to the newer American-DTC indie houses (Henry Rose, Phlur, Ellis Brooklyn) "
        "that occupy an adjacent vocabulary space \u2014 'indie', 'clean', or 'artisan' "
        "rather than 'niche' specifically. The Recognition gradient is real "
        "but operates at the threshold-and-vocabulary level, not as a smooth "
        "monotone function of Identity Load.",
    ],
    "chart_slot": "chart_01_mention_rate_distribution",
}


# ---------------------------------------------------------------------------
# Section 04 - Findings: Recall
# ---------------------------------------------------------------------------

SECTION_04_FINDINGS_RECALL = {
    "id": "04_findings_recall",
    "heading": "Findings \u2014 Recall",
    "lede": (
        "Recall shows a second Identity-Load gradient, but operating as "
        "near-total Recall attrition in Cell B (the highest-IL tier) rather "
        "than as Pareto concentration. Cell A is broadly distributed; Cell C "
        "surfaces sporadically through general fragrance-discourse channels "
        "despite failing the niche-fragrance Recognition probe."
    ),
    "recall_table": {
        "caption": (
            "Phase B Recall outcomes per cell. Mentions are out of 18 "
            "(3 query frames x 6 reference panel models)."
        ),
        "columns": ["Cell", "Zero-mention brands", "Top-2 share", "Notes"],
        "rows": [
            ["Cell A", "1 of 8 (Memo Paris)", "0.446",
             "Le Labo 17, MFK 16, Diptyque 15 lead; below C2 within-cell threshold of 0.50 because Recall is distributed across many recognized houses"],
            ["Cell B", "7 of 8", "1.000",
             "Only D.S. & Durga with non-zero mentions (2/18); top-2 share is degenerate \u2014 concentration arises from sparseness, not Pareto"],
            ["Cell C", "4 of 8", "0.688",
             "Tom Ford 4, Chanel 3, Versace 1, Dior 1 surface through general discourse channels despite zero Recognition for 'niche fragrance'"],
        ],
    },
    "interpretation_paragraphs": [
        "Cell A's distributed Recall is the healthy pattern: many brands "
        "recognized AND surfaced, with no single brand dominating. The C2 "
        "within-cell concentration threshold of 0.50 isn't cleared here, but "
        "for a substantive reason \u2014 Cell A is too rich, not too sparse.",

        "Cell B's pattern is the opposite. Recognition is strong (mean C_P = 5.00) "
        "but Recall is near-zero across the cell. Seven of eight brands receive "
        "zero mentions in 18 observations; only D.S. & Durga surfaces, and only "
        "at 2/18. This is the Recognition \u00d7 Recall dissociation pattern at cell "
        "scale: the AI knows these brands belong to the category, but does not "
        "retrieve them when asked to enumerate the category. The behavior is "
        "more pronounced for newer indie houses (Heretic, Vyrao, Phlur, Snif) "
        "than for the cell's pivot (D.S. & Durga), suggesting that brand age "
        "or accumulated discourse-volume mediates the Recall channel independently "
        "of Recognition status.",

        "Cell C's surprising surface coverage \u2014 Tom Ford, Chanel, Versace, Dior "
        "all surface in niche-anchored queries despite failing the niche "
        "Recognition probe \u2014 points to a parallel Recall channel that operates "
        "on cultural-footprint terms rather than category-anchored Recognition. "
        "AI systems can include Chanel in a niche-fragrance list while not "
        "actually classifying Chanel as niche. This sub-threshold channel is "
        "registered for follow-up in v0.19+ but does not change the v0.18 "
        "verdicts.",
    ],
    "chart_slot": "chart_02_cell_attrition",
}


# ---------------------------------------------------------------------------
# Section 05 - Findings: Dissociation
# ---------------------------------------------------------------------------

SECTION_05_FINDINGS_DISSOCIATION = {
    "id": "05_findings_dissociation",
    "heading": "Findings \u2014 Recognition \u00d7 Recall dissociation",
    "lede": (
        "Nine Iwachu-pattern cases on a same-language substrate. The v1.4 "
        "multi-component construct generalizes: the dissociation is not a "
        "Western-language LLM training-data bias artifact, and not specific "
        "to the original cross-cultural anchor. It is a real, measurable "
        "property of AI-mediated retrieval \u2014 and it concentrates in the "
        "highest-Identity-Load cell."
    ),
    "dissociation_table": {
        "caption": (
            "9 Iwachu-pattern cases (Phase A C_P \u2265 5/6 AND Phase B mentions \u2264 2/18) "
            "from the v0.18 panel."
        ),
        "columns": ["Cell", "Brand", "C_P", "Mentions"],
        "rows": [
            ["Cell A", "Comme des Gar\u00e7ons Parfums", "5/6", "2/18"],
            ["Cell A", "Memo Paris", "6/6", "0/18"],
            ["Cell A", "Etat Libre d'Orange", "6/6", "1/18"],
            ["Cell B", "D.S. & Durga", "6/6", "2/18"],
            ["Cell B", "Boy Smells", "5/6", "0/18"],
            ["Cell B", "Heretic Parfum", "6/6", "0/18"],
            ["Cell B", "Vyrao", "6/6", "0/18"],
            ["Cell B", "Phlur", "5/6", "0/18"],
            ["Cell B", "Snif", "5/6", "0/18"],
        ],
    },
    "interpretation_paragraphs": [
        "Cell A contributes three cases: brands that AI systems recognize cleanly "
        "as niche fragrance (5 or 6 of 6 recognition-positive responses) but "
        "do not surface when prompted to list category members. Memo Paris and "
        "Etat Libre d'Orange are at the upper end of canonical designer-niche "
        "Recognition (6/6) but in the lower end of Recall in their cell. The "
        "pattern is real but minority within Cell A.",

        "Cell B contributes six cases: 75% of the cell's brands exhibit the "
        "Iwachu pattern. The cell-level concentration is the methodological "
        "headline. If the construct were noise-driven or artifact-driven, the "
        "dissociation cases would distribute roughly uniformly across cells. "
        "Instead they concentrate where category Identity Load is highest \u2014 "
        "consistent with the moderator hypothesis and with the substantive "
        "theory that AI mediation amplifies retrieval inequality in identity-"
        "bearing categories.",

        "Cell C contributes zero cases by design. The Iwachu-pattern threshold "
        "requires C_P \u2265 5/6, which no Cell C brand achieves (maximum is Tom "
        "Ford at 2/6). The construct is asymmetric: it captures "
        "Recognition-without-Recall, not Non-Recognition-with-Non-Recall. Cell C's "
        "zero contribution is therefore a feature of the design, not a failure "
        "of generalization.",
    ],
    "chart_slot": "chart_03_dissociation_scatter",
}


# ---------------------------------------------------------------------------
# Section 06 - Verdict
# ---------------------------------------------------------------------------

SECTION_06_VERDICT = {
    "id": "06_verdict",
    "heading": "Verdict",
    "lede": (
        "Three orthogonal pre-registered hypotheses; three PARTIAL verdicts. "
        "Read together, they describe a moderator that operates through "
        "layer-specific channels and a multi-component construct that "
        "generalizes with cell-level concentration in the highest-IL tier."
    ),
    "verdict_blocks": [
        {
            "hypothesis": "H_Regime4_indie_fragrance",
            "verdict": "PARTIAL",
            "resolved_at": "C3 (ranking coherence)",
            "rationale": (
                "C1 panel adequacy clears (worldwide n = 24, well above the "
                "floor of 12). C2 within-cell clears (Cells B and C meet the "
                "top-2 share \u2265 0.50 threshold). C2 IL-gradient separation clears "
                "(Cell B 1.000 \u2212 Cell C 0.688 = 0.3125, above the 0.10 floor). "
                "C3 ranking coherence fails: only Cell C meets the per-cell "
                "rho \u2265 0.50 threshold (Cell C rho = 0.615; Cell A rho = 0.247; "
                "Cell B rho = 0.434). 1 of 3 cells clearing < 2 of 3 required."
            ),
        },
        {
            "hypothesis": "H_IdentityLoad_moderator (three-leg joint)",
            "verdict": "PARTIAL",
            "resolved_at": "joint matrix routing",
            "rationale": (
                "v0.16 PARTIAL (SSRN 6791999, kitchen knives) x v0.17 FALSIFIED "
                "(SSRN 6802261, premium kitchenware, falsification on panel "
                "inadequacy) x v0.18 PARTIAL (this report). The joint matrix "
                "routes to PARTIAL: the moderator operates with substrate-"
                "specific qualifications. Across three legs, the moderator is "
                "neither uniformly confirmed nor cleanly falsified."
            ),
        },
        {
            "hypothesis": "H_Recognition_Recall_dissociation_generalization",
            "verdict": "DISSOCIATION_PARTIAL",
            "resolved_at": "case enumeration and cell distribution",
            "rationale": (
                "9 Iwachu-pattern cases identified across 2 of 3 cells "
                "(Cells A and B). The \u00a75.2 matrix routes 'cases present but "
                "cell-clustered (2 of 3)' to DISSOCIATION_PARTIAL. The v1.4 "
                "multi-component construct generalizes from the cross-cultural "
                "Japanese-cell anchor (v0.17 Iwachu) to a same-language "
                "IL-gradient substrate. Cell C contributes zero by Recognition-"
                "floor design \u2014 expected, not a failure."
            ),
        },
    ],
    "per_cell_diagnostics_table": {
        "caption": "Phase B per-cell diagnostics fed to the verdict cascade.",
        "columns": ["Cell", "n", "Top-2 share (C2)", "Spearman rho (C3)"],
        "rows": [
            ["Cell A \u2014 Designer-niche", "8", "0.446", "0.247"],
            ["Cell B \u2014 Indie / Artisan", "8", "1.000", "0.434"],
            ["Cell C \u2014 Mass-prestige", "8", "0.688", "0.615"],
        ],
    },
}


# ---------------------------------------------------------------------------
# Section 07 - Implications
# ---------------------------------------------------------------------------

SECTION_07_IMPLICATIONS = {
    "id": "07_implications",
    "heading": "Implications",
    "lede": (
        "Three readings: for the AIAS\u2122 canonical methodology layer, for "
        "Identity-Load as a brand-strategy moderator, and for the next "
        "phase of the program."
    ),
    "implication_blocks": [
        {
            "label": "For AIAS\u2122 1.0 canonical methodology",
            "body": (
                "v0.18 strengthens Protocol v1.4 from one empirical anchor to "
                "ten cases across two substrate families. The multi-component "
                "construct (Recognition \u00d7 Recall) survives its first "
                "generalization test on a same-language substrate. The "
                "dissociation pattern is not a cross-cultural artifact. "
                "v1.4 is closer to canonical-methodology readiness \u2014 though "
                "AIAS\u2122 1.0's full six-component composite remains 2\u20133 years "
                "out per v1.2 \u00a77.4. What ships with v0.18 is the strengthened "
                "Recognition \u00d7 Recall axis; the remaining composite "
                "components (Ranking, Coverage, Grounding, Sentiment) are on "
                "the post-v1.4 implementation roadmap."
            ),
        },
        {
            "label": "For Identity-Load as a brand-strategy moderator",
            "body": (
                "Senior brand leaders managing identity-bearing categories now "
                "have a measurable mechanism: in high-IL categories, AI "
                "mediation produces Recognition-without-Recall dissociation "
                "as a measurable consequence \u2014 not as a hypothetical risk. "
                "For brands in these categories, optimizing for Recognition "
                "(does the AI know us?) is necessary but not sufficient. "
                "Recall (does the AI surface us?) is a distinct, separable "
                "channel. The two channels can \u2014 and on v0.18 evidence, "
                "frequently do \u2014 diverge."
            ),
        },
        {
            "label": "For v0.19 and beyond",
            "body": (
                "Three pre-registerable directions emerge cleanly from the "
                "v0.18 verdicts. First, substrates with greater within-cell "
                "Recognition variance would address the C3 failure mode "
                "(Cell A's near-saturation, Cell B's near-zero Recall both "
                "degenerate the within-cell rank correlation). Second, finer "
                "Identity-Load stratification within high-IL tiers would test "
                "whether the dissociation cell-clustering in Cell B (75%) "
                "replicates and refines. Third, finer stratification within "
                "Cell C \u2014 separating icon-tier (Chanel, Dior) from mainstream-"
                "tier (Marc Jacobs, Calvin Klein) \u2014 would clarify the "
                "cultural-footprint Recall channel surfaced as a v0.18 "
                "sensitivity finding. Each direction is independently "
                "preregisterable and leaves v0.18's verdicts unchanged."
            ),
        },
    ],
}


# ---------------------------------------------------------------------------
# Section 08 - Methodology notes (DEVIATIONS, limits)
# ---------------------------------------------------------------------------

SECTION_08_METHODOLOGY_NOTES = {
    "id": "08_methodology_notes",
    "heading": "Methodology notes",
    "lede": (
        "DEVIATIONS log entries from the v0.18 acquisition, plus four limits "
        "that qualify the verdicts. Pre-registration discipline (commit "
        "183386c \u2192 1195cb8) locks the verdict logic ex-ante; deviations are "
        "documented openly rather than retroactively reconciled."
    ),
    "deviations_summary": (
        "One DEVIATIONS entry opened during v0.18 acquisition. "
        "Entry 1 (2026-05-20): Cell C pivot cascade exhausted at the 'niche "
        "fragrance' Recognition probe. No Cell C brand achieved C_P = 6/6; "
        "the cascade exhausted without anchoring a pivot. Treated as a "
        "substantive empirical finding rather than a panel-construction error. "
        "Cell C alternates (Hugo Boss, Lanc\u00f4me, etc., also mass-prestige) "
        "NOT invoked \u2014 they would hit the same Recognition-anchor mismatch by "
        "construction. The pre-registered panel of 24 brands is unchanged. "
        "Full entry deposited at osf.io/ec6wh/v18/DEVIATIONS.md."
    ),
    "limits": [
        {
            "label": "Single-substrate constraint on the generalization claim",
            "body": (
                "v0.18 generalizes the multi-component construct from one "
                "substrate to two. Multi-substrate generalization across the "
                "consumer-category spectrum remains future work. v0.19+ should "
                "probe substrates with shifted IL profiles and category-vocabulary "
                "structures."
            ),
        },
        {
            "label": "LLM panel temporal validity",
            "body": (
                "The six-slot reference panel reflects model versions in market "
                "as of mid-2026. Provider model substitutions over time are "
                "expected and documented in the DEVIATIONS protocol. v0.18 "
                "cases should be read as the pattern observed against the "
                "locked panel at acquisition, not as permanent substrate "
                "properties."
            ),
        },
        {
            "label": "C2 IL-gradient guard's degenerate case",
            "body": (
                "Cell B's top-2 share = 1.000 emerges from Recall sparseness "
                "(D.S. & Durga alone, with 2 of 18 mentions) rather than from "
                "a healthy Pareto distribution. The IL-gradient separation "
                "guard clears against a near-empty Cell B baseline. The "
                "substantive interpretation rests on the \u00a705 dissociation "
                "pattern, not on the C2 mention concentration metric alone."
            ),
        },
        {
            "label": "C3 ranking coherence as a within-cell variance test",
            "body": (
                "Phase D rho requires within-cell variance in both Recognition "
                "and Recall. Cell A's flat Recognition (7 of 8 brands at C_P = "
                "6/6) and Cell B's flat Recall (7 of 8 brands at zero mentions) "
                "both degenerate the rank-correlation signal. Future operationalization "
                "may benefit from supplementary measures that do not require "
                "simultaneous variance in both dimensions."
            ),
        },
    ],
}


# ---------------------------------------------------------------------------
# Section 09 - References and attribution
# ---------------------------------------------------------------------------

SECTION_09_REFERENCES_AND_ATTRIBUTION = {
    "id": "09_references_and_attribution",
    "heading": "References and attribution",
    "references": [
        "Gonz\u00e1lez Castro, P. U. (2026). AI Availability \u2014 A Third System in Brand Availability Theory. SSRN 6659000.",
        "Gonz\u00e1lez Castro, P. U. (2026). The AIAS Presence Measurement Protocol: Methodological Notes (v1.2). SSRN 6761698.",
        "Gonz\u00e1lez Castro, P. U. (2026). AIAS Protocol v1.3 Phase A Pivot-Validation Specification. SSRN 6797679.",
        "Gonz\u00e1lez Castro, P. U. (2026). AIAS Protocol v1.4: Recognition \u00d7 Recall Decomposition. SSRN 6799479.",
        "Gonz\u00e1lez Castro, P. U. (2026). v0.16 \u2014 Regime 4 Boundary and Discourse-Language Carryforward (Kitchen Knives). SSRN 6791999.",
        "Gonz\u00e1lez Castro, P. U. (2026). v0.17 \u2014 Panel Inadequacy and Recognition \u00d7 Recall Dissociation (Premium Kitchenware). SSRN 6802261.",
        "Romaniuk, J. (2018). Building Distinctive Brand Assets. Oxford University Press.",
        "Sharp, B. (2010). How Brands Grow. Oxford University Press.",
        "Sharp, B., & Romaniuk, J. (2021). How Brands Grow Part 2 (revised). Oxford University Press.",
    ],
    "data_and_code_availability": (
        "Pre-registration, acquisition data, scoring code, figures, and verdict "
        "outputs deposited at osf.io/ec6wh/v18/. Pre-reg tag v0.18-prereg-r1 "
        "(commit 183386c), refined through r4 at commit 1195cb8."
    ),
    "trademark_notice": "AIAS\u2122 and Third System\u2122 are trademarks of the research program.",
    "correspondence": {
        "name": "Pablo Ulpiano Gonz\u00e1lez Castro",
        "email": "pablou@pablou.com",
        "web": "pablou.com \u00b7 thirdsystem.ai",
        "orcid": "0009-0003-8968-9990",
    },
}


# ---------------------------------------------------------------------------
# Ordered section manifest (for build_report_v18.py iteration)
# ---------------------------------------------------------------------------

SECTIONS_ORDERED = [
    SECTION_01_PURPOSE_AND_SUBSTRATE,
    SECTION_02_DESIGN,
    SECTION_03_FINDINGS_RECOGNITION,
    SECTION_04_FINDINGS_RECALL,
    SECTION_05_FINDINGS_DISSOCIATION,
    SECTION_06_VERDICT,
    SECTION_07_IMPLICATIONS,
    SECTION_08_METHODOLOGY_NOTES,
    SECTION_09_REFERENCES_AND_ATTRIBUTION,
]


# ---------------------------------------------------------------------------
# Build metadata (consumed by build_report_v18.py for footer / colophon)
# ---------------------------------------------------------------------------

BUILD_META = {
    "phase": "v0.18",
    "pre_reg_tag": "v0.18-prereg-r1",
    "pre_reg_r4_commit": "1195cb8",
    "protocol_version": "v1.4",
    "protocol_citation": "AIAS Presence Measurement Protocol v1.4 (SSRN 6799479)",
    "predecessor_phase_ids": ["v0.16", "v0.17"],
    "predecessor_ssrn_ids": ["6791999", "6802261"],
    "data_deposit": "osf.io/ec6wh/v18/",
    "chart_dir_relative": "reports/figs/v18/",
    "brand_tokens_path": "brand/third_system_brand.json",
    "footer_line": (
        "AIAS Presence Measurement Protocol v0.18 \u00b7 "
        "Pre-reg tag v0.18-prereg-r1 \u00b7 osf.io/ec6wh/v18/"
    ),
}
