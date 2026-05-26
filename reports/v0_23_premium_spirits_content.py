"""
AIAS v0.23 — Premium Spirits
Brand-format report content module (Third System™)
Protocol v1.6 | Scored 2026-05-26

11 content attributes for build_report_v23.py
"""

# ---------------------------------------------------------------------------
# COVER
# ---------------------------------------------------------------------------
COVER = {
    "title": "AI Availability Score",
    "subtitle": "Premium Spirits",
    "version": "v0.23",
    "descriptor": "AIAS\u2122 Presence Component \u2014 Substrate 7 of N",
    "date": "May 2026",
    "protocol": "Protocol v1.6",
    "author": "Pablo Ulpiano Gonz\u00e1lez Castro",
    "entity": "Third System\u2122",
    "confidentiality": "Public Release",
}

# ---------------------------------------------------------------------------
# STANDFIRST
# ---------------------------------------------------------------------------
STANDFIRST = (
    "Premium spirits is the first AIAS substrate where every brand in the "
    "24-brand registry achieves rich recognition (R3) across all six LLMs. "
    "AI knows these brands perfectly. The question that remains is which "
    "brands AI recommends\u2009\u2014\u2009and there, the field splits wide open."
)

# ---------------------------------------------------------------------------
# LEAD_DECK (3\u20134 bullet-weight propositions)
# ---------------------------------------------------------------------------
LEAD_DECK = [
    "All 24 brands scored R3 (rich recognition) across all six models\u2009"
    "\u2014\u2009a universal ceiling never observed in the prior six substrates.",

    "Recall, not recognition, drives the entire Presence distribution: "
    "composite scores range from 40.0 (zero recall) to 71.2, with six brands "
    "perfectly known yet never recommended.",

    "Fortaleza, an independent craft tequila brand, lands in the Dominant "
    "regime alongside Hennessy, Patr\u00f3n, and Grey Goose\u2009\u2014\u2009"
    "conglomerate ownership confers no statistically significant AI Presence "
    "advantage (p\u2009=\u20090.28).",

    "The editorial-authority and cultural-cult recall channels converge more "
    "than in any prior substrate (overlap\u2009=\u20090.80), suggesting that "
    "in high-familiarity categories the two channels surface largely the same "
    "brand set.",
]

# ---------------------------------------------------------------------------
# EXEC_SUMMARY
# ---------------------------------------------------------------------------
EXEC_SUMMARY = (
    "AIAS v0.23 measures AI Presence for 24 premium spirits brands across "
    "six large language models under Protocol v1.6. The substrate introduces "
    "the seventh product family to the AIAS measurement program and the first "
    "where editorial-authority and cultural-cult recall channels were expected "
    "to populate with comparable density.\n\n"

    "The recognition ceiling is the defining structural feature of this "
    "substrate. With all 144 Phase A probes returning R3, the Recognition "
    "axis contributes zero discriminating variance to the Presence composite. "
    "This directly falsifies H_ILDirect (r\u2009=\u2009NaN; zero variance "
    "precludes correlation) and shifts analytical attention entirely to the "
    "Recall axis.\n\n"

    "On recall, the 24 brands distribute across all four regimes in a "
    "perfectly balanced 6/6/6/6 split. Six brands\u2009\u2014\u2009Bombay "
    "Sapphire, The Balvenie, Casamigos, Compass Box, and Fernet-Branca, plus "
    "Jameson at the margin\u2009\u2014\u2009register zero or near-zero recall "
    "despite flawless recognition. These are brands that AI systems can "
    "describe in expert detail but never surface in recommendation contexts. "
    "The recognition\u2013recall gap is the actionable finding for brand "
    "strategists operating in this category.\n\n"

    "The substrate-specific hypothesis H_ConglomeratePortfolio is falsified: "
    "conglomerate-owned brands (n\u2009=\u200914) average 60.75 on the "
    "Presence composite versus 58.05 for independents (n\u2009=\u200910), "
    "a 4.6% lift that does not reach statistical significance "
    "(t\u2009=\u20090.59, p\u2009=\u20090.28; Mann-Whitney "
    "U\u2009=\u200972.0, p\u2009=\u20090.46). Training-corpus density from "
    "conglomerate media coverage does not translate mechanically into higher "
    "AI Presence."
)

# ---------------------------------------------------------------------------
# WHAT_WE_MEASURED
# ---------------------------------------------------------------------------
WHAT_WE_MEASURED = (
    "Phase A (Recognition): 24 brands \u00d7 6 LLMs = 144 single-shot "
    "probes at temperature 0.0. Each response scored R0\u2013R3 by an "
    "LLM judge (Claude Sonnet 4.5). Substrate Recognition pre-screen "
    "(Protocol v1.6) applied; zero brands excluded.\n\n"

    "Phase B (Two-channel Recall): 6 category-level probes (3 editorial-"
    "authority, 3 cultural-cult) \u00d7 6 LLMs = 36 queries. Each response "
    "scored for brand mention (binary), slot position (ordinal rank of first "
    "mention), and elaboration (LLM judge). 110 total brand mentions "
    "detected across 36 responses.\n\n"

    "Composite Presence score: 0.4 \u00d7 Recognition (normalized) + "
    "0.4 \u00d7 Recall rate + 0.2 \u00d7 inverse mean slot position. "
    "Regime classification by quartile thresholds: Q25\u2009=\u200958.28, "
    "Q50\u2009=\u200964.22, Q75\u2009=\u200967.50.\n\n"

    "Model panel (fixed from v0.17): Claude Opus 4.5, Claude Sonnet 4.5, "
    "GPT-4o, GPT-4o-mini, Gemini 2.5 Flash, Gemini 2.5 Flash Lite.\n\n"

    "Registry: 24 brands spanning 12 spirit types, structured in three "
    "tiers (Global-dominant, Premium-enthusiast, Craft-cult-emerging) with "
    "conglomerate ownership coded binary (top-5 global spirits groups = 1; "
    "all others = 0). 14 conglomerate, 10 independent."
)

# ---------------------------------------------------------------------------
# PATTERNS (the analytical meat)
# ---------------------------------------------------------------------------
PATTERNS = (
    "P1. The recognition ceiling.\n"
    "All 24 brands scored R3 across all six models\u2009\u2014\u2009144/144 "
    "probes at the maximum recognition level. This is structurally distinct "
    "from every prior AIAS substrate, where recognition variance contributed "
    "meaningfully to the composite. In premium spirits, LLMs can identify "
    "distillery locations, flagship expressions, ownership lineage, and "
    "tasting profiles for every brand in the registry, from Johnnie Walker "
    "to Mezcal Vago. The result: the entire Presence distribution is driven "
    "by who gets recommended, not who gets recognized.\n\n"

    "P2. Known but never recommended: the recognition\u2013recall gap.\n"
    "Six brands score a composite of 40.0, the floor value representing "
    "perfect recognition with zero recall: Bombay Sapphire, The Balvenie, "
    "Casamigos, Compass Box, and Fernet-Branca (plus Jameson at 57.63 with "
    "a single mention). These brands exist fully in AI\u2019s knowledge base "
    "but are invisible in its recommendation behavior. For brand managers, "
    "this gap is the most directly actionable finding: recognition alone is "
    "a necessary but insufficient condition for AI Presence.\n\n"

    "P3. Craft disrupts the hierarchy.\n"
    "The Dominant regime (composite \u226567.50) contains two independent "
    "brands: Fortaleza (68.84, craft tequila) and Hendrick\u2019s (69.23). "
    "Fortaleza outranks every Bacardi Ltd. brand in the registry despite "
    "being a fraction of the size. R\u00e9my Martin (68.76), coded "
    "independent under the top-5 rule, also lands Dominant. The finding is "
    "consistent with H_ConglomeratePortfolio\u2019s falsification: scale and "
    "media spend do not mechanically translate into AI recommendation "
    "behavior.\n\n"

    "P4. Channel convergence at high familiarity.\n"
    "The editorial-authority channel surfaced 15 brands; cultural-cult "
    "surfaced 16; 12 appear in both (overlap\u2009=\u20090.80). This is "
    "the highest overlap observed across seven substrates and sits at the "
    "exact boundary of H_C2\u2019s support range. The finding suggests that "
    "in categories where LLMs have dense training data, the two channels "
    "converge: the same brands surface whether the query frames authority "
    "through critics or through community enthusiasm. Channel-specific "
    "brands do exist\u2009\u2014\u2009R\u00e9my Martin is pure editorial "
    "(10 EA / 0 CC), Jack Daniel\u2019s pure cultural (0 EA / 5 CC)"
    "\u2009\u2014\u2009but they are exceptions.\n\n"

    "P5. Conglomerate ownership is not a Presence driver.\n"
    "The 14 conglomerate-owned brands average 60.75 on the composite versus "
    "58.05 for the 10 independents\u2009\u2014\u2009a directionally positive "
    "but non-significant 4.6% lift (t\u2009=\u20090.59, p\u2009=\u20090.28). "
    "Diageo, Pernod Ricard, Bacardi Ltd., LVMH, and Brown-Forman collectively "
    "own 14 of 24 registry brands but capture no systematic AI Presence "
    "advantage. The mechanism hypothesized\u2009\u2014\u2009training-corpus "
    "density from conglomerate-level media coverage\u2009\u2014\u2009either "
    "does not operate as theorized or is offset by the editorial and "
    "enthusiast attention that craft and independent brands attract."
)

# ---------------------------------------------------------------------------
# LIMITATIONS
# ---------------------------------------------------------------------------
LIMITATIONS = (
    "The universal R3 ceiling collapses the Recognition axis and renders "
    "H_ILDirect structurally untestable (zero-variance correlation returns "
    "NaN). This is a property of the substrate, not a protocol deficiency, "
    "but it limits the composite\u2019s discriminating power to a single "
    "component.\n\n"

    "H_C2_TwoChannel\u2019s overlap coefficient lands at exactly 0.80, the "
    "upper boundary of the pre-registered support range. A stricter threshold "
    "(e.g., 0.75) would flip the verdict. The result should be interpreted "
    "as borderline rather than robust.\n\n"

    "Conglomerate coding uses a binary top-5 rule. William Grant & Sons, "
    "R\u00e9my Cointreau, and Asahi Group are coded independent despite being "
    "multinational producers. Alternative coding schemes (e.g., any publicly "
    "traded parent) could shift H_ConglomeratePortfolio\u2019s direction or "
    "significance.\n\n"

    "The 24-brand registry is a purposive sample. Pan-spirits breadth comes "
    "at the cost of within-type depth: some spirit categories have only 1\u20132 "
    "representatives, limiting subcategory-level inference.\n\n"

    "Recall probes name specific publications and competitions (Whisky "
    "Advocate, SFWSC). This anchoring may favor brands prominent in those "
    "specific circuits over brands prominent in others."
)

# ---------------------------------------------------------------------------
# WHATS_NEXT
# ---------------------------------------------------------------------------
WHATS_NEXT = (
    "The recognition ceiling finding motivates a cross-substrate comparison: "
    "which product families exhibit ceiling effects and which show recognition "
    "variance? This pattern becomes testable at scale as the substrate count "
    "grows.\n\n"

    "The recognition\u2013recall gap invites intervention-design work. If a "
    "brand like The Balvenie is perfectly known but never recommended, what "
    "content or signal changes would shift its recall behavior? This is the "
    "bridge from measurement to strategy.\n\n"

    "Channel convergence at 0.80 overlap raises the question of whether a "
    "third channel\u2009\u2014\u2009perhaps a commerce or availability-framed "
    "prompt\u2009\u2014\u2009would introduce additional discriminating variance "
    "in high-familiarity substrates."
)

# ---------------------------------------------------------------------------
# HYPOTHESIS_SCORING (summary table data)
# ---------------------------------------------------------------------------
HYPOTHESIS_SCORING = [
    {
        "id": "H_Regime4",
        "label": "Four-regime classification",
        "verdict": "Supported",
        "detail": "6/6/6/6 split across Dominant, Established, Emerging, Absent",
    },
    {
        "id": "H_RecognitionPrescreen",
        "label": "Recognition pre-screen gate",
        "verdict": "Supported",
        "detail": "0 brands excluded (threshold: \u22643)",
    },
    {
        "id": "H_Phantom",
        "label": "Phantom brand persistence",
        "verdict": "Not testable",
        "detail": "No defunct brands in registry",
    },
    {
        "id": "H_ILDirect",
        "label": "Recognition\u2013recall correlation",
        "verdict": "Falsified",
        "detail": "r = NaN (zero recognition variance; all R3 ceiling)",
    },
    {
        "id": "H_C2_TwoChannel",
        "label": "Two-channel recall divergence",
        "verdict": "Supported (borderline)",
        "detail": "Overlap = 0.80 (EA: 15 brands, CC: 16, intersection: 12)",
    },
    {
        "id": "H_ConglomeratePortfolio",
        "label": "Conglomerate ownership advantage",
        "verdict": "Falsified",
        "detail": "Conglomerate mean 60.75 vs independent 58.05; lift 4.6%, p = 0.28",
    },
]

# ---------------------------------------------------------------------------
# HYPOTHESIS_DETAILS (per-hypothesis narrative blocks)
# ---------------------------------------------------------------------------
HYPOTHESIS_DETAILS = {
    "H_Regime4": (
        "The four-regime taxonomy distributes evenly across the 24-brand "
        "registry: Dominant (Hennessy, Patr\u00f3n, Grey Goose, Hendrick\u2019s, "
        "R\u00e9my Martin, Fortaleza), Established (Jack Daniel\u2019s, "
        "Lagavulin, Monkey 47, Nikka, Del Maguey, Redbreast), Emerging "
        "(Johnnie Walker, Bacardi, Clase Azul, Woodford Reserve, St. George "
        "Spirits, Mezcal Vago), Absent (Bombay Sapphire, Jameson, The Balvenie, "
        "Casamigos, Compass Box, Fernet-Branca). The 6/6/6/6 split is the most "
        "balanced distribution observed across seven substrates. Note that "
        "\u2018Absent\u2019 in this context means absent from recall, not from "
        "knowledge\u2009\u2014\u2009every Absent-regime brand scored R3 on "
        "recognition."
    ),

    "H_RecognitionPrescreen": (
        "Zero brands triggered the pre-screen exclusion gate (R0 across "
        "\u22655 of 6 models). This confirms the prediction that premium spirits "
        "has high baseline LLM familiarity. The substrate is the cleanest pass "
        "through the pre-screen observed to date."
    ),

    "H_ILDirect": (
        "Falsified by structural ceiling. All 24 brands scored recognition "
        "mean = 3.0 (R3 across all six models). With zero variance on the "
        "Recognition axis, the Pearson correlation between Recognition and "
        "Recall is undefined (NaN). This is not a measurement failure but a "
        "substantive finding: in categories where AI training data is "
        "sufficiently dense, recognition saturates and ceases to discriminate. "
        "The implication for AIAS methodology is that high-familiarity "
        "substrates may require recall-only composite scoring."
    ),

    "H_C2_TwoChannel": (
        "Supported at the boundary. The editorial-authority channel surfaced "
        "15 unique brands; cultural-cult surfaced 16; 12 brands appear in "
        "both, yielding an overlap coefficient of 0.80 (the upper limit of "
        "the pre-registered [0.30, 0.80] support range). Channel-exclusive "
        "brands exist: R\u00e9my Martin (10 EA / 0 CC), Del Maguey (8 EA / "
        "1 CC) skew editorial; Jack Daniel\u2019s (0 EA / 5 CC), St. George "
        "Spirits (0 EA / 2 CC) skew cultural. But the dominant pattern is "
        "convergence\u2009\u2014\u2009in high-familiarity substrates, both "
        "channels largely surface the same brand set."
    ),

    "H_ConglomeratePortfolio": (
        "Falsified. The 14 conglomerate-owned brands (Diageo 3, Bacardi Ltd. "
        "4, Pernod Ricard 4, Brown-Forman 2, LVMH 1) averaged 60.75 on the "
        "Presence composite versus 58.05 for the 10 independent brands. The "
        "4.6% lift is directionally consistent with the prediction but far "
        "from significant (t = 0.59, p = 0.28; Mann-Whitney U = 72.0, "
        "p = 0.46). The independent brands Fortaleza (68.84) and "
        "Hendrick\u2019s (69.23) both outperform the conglomerate mean. "
        "Conglomerate media density\u2009\u2014\u2009press releases, annual "
        "reports, cross-brand coverage\u2009\u2014\u2009does not translate "
        "mechanically into AI recommendation behavior."
    ),
}

# ---------------------------------------------------------------------------
# CLOSING
# ---------------------------------------------------------------------------
CLOSING = (
    "Premium spirits reveals what happens when AI recognition saturates: "
    "the competitive frontier shifts entirely to recall. A brand that AI can "
    "describe in expert detail but never recommends occupies a new kind of "
    "strategic gap\u2009\u2014\u2009one invisible to traditional brand-tracking "
    "methods that measure awareness without distinguishing recognition from "
    "recommendation. The AIAS framework surfaces this gap by design."
)


# =========================================================================
# CHART SPECIFICATIONS
# =========================================================================

CHART_SPECS = {
    "chart_01_composite_bar": {
        "type": "horizontal_bar",
        "title": "AI Presence Composite Score by Brand",
        "subtitle": "Protocol v1.6 \u2014 Premium Spirits (v0.23)",
        "data_source": "v23_verdicts.json \u2192 brand_details",
        "sort": "descending by composite_presence",
        "color_by": "regime",
        "regime_colors": {
            "Dominant": "#37237B",    # Third System indigo
            "Established": "#6B5CA5",  # medium indigo
            "Emerging": "#A89BCF",     # light indigo
            "Absent": "#D4CDE5",       # faded indigo
        },
        "annotations": [
            "Vertical dashed lines at Q25 (58.28), Q50 (64.22), Q75 (67.50)",
            "Regime labels in right margin",
        ],
        "x_label": "Composite Presence Score (0\u2013100)",
        "y_label": "",  # brand names on y-axis
        "source_line": "AIAS\u2122 v0.23 | Protocol v1.6 | Third System\u2122",
        "figsize": [10, 8],
        "verdict_text": "All four regimes populated (6/6/6/6). Recognition at ceiling; recall drives the distribution.",
    },

    "chart_02_channel_heatmap": {
        "type": "heatmap",
        "title": "Recall Mentions by Channel and Brand",
        "subtitle": "Editorial-Authority vs Cultural-Cult",
        "data_source": "v23_verdicts.json \u2192 brand_details (recall_ea, recall_cc)",
        "rows": "brands (sorted by total recall descending)",
        "columns": ["Editorial-Authority (EA)", "Cultural-Cult (CC)"],
        "color_scale": "sequential indigo (0 = white, max = #37237B)",
        "annotations": [
            "Cell values as integers",
            "Highlight R\u00e9my Martin (10 EA / 0 CC) and Jack Daniel\u2019s (0 EA / 5 CC) as channel-exclusive exemplars",
        ],
        "source_line": "AIAS\u2122 v0.23 | Protocol v1.6 | Third System\u2122",
        "figsize": [7, 10],
        "verdict_text": "Overlap = 0.80. Channels converge in high-familiarity substrates; channel-exclusive brands are exceptions.",
    },

    "chart_03_conglomerate_box": {
        "type": "box_plot",
        "title": "Composite Presence by Ownership Structure",
        "subtitle": "Conglomerate (n=14) vs Independent (n=10)",
        "data_source": "v23_verdicts.json \u2192 brand_details (conglomerate, composite_presence)",
        "groups": ["Conglomerate", "Independent"],
        "colors": ["#37237B", "#A89BCF"],
        "overlay_points": True,
        "annotations": [
            "Mean markers",
            "p-value annotation: t = 0.59, p = 0.28 (ns)",
        ],
        "source_line": "AIAS\u2122 v0.23 | Protocol v1.6 | Third System\u2122",
        "figsize": [6, 6],
        "verdict_text": "H_ConglomeratePortfolio falsified. 4.6% lift, not significant (p = 0.28).",
    },

    "chart_04_recall_vs_slot": {
        "type": "scatter",
        "title": "Recall Frequency vs Mean Slot Position",
        "subtitle": "Brands with zero recall excluded (n=18 plotted)",
        "data_source": "v23_verdicts.json \u2192 brand_details",
        "x": "recall_rate",
        "y": "mean_slot_position (inverted axis: 1 at top)",
        "size": "elaboration_count",
        "color_by": "regime",
        "label_points": True,
        "annotations": [
            "Quadrant labels: high recall + early slot = strong; high recall + late slot = mentioned but buried",
        ],
        "source_line": "AIAS\u2122 v0.23 | Protocol v1.6 | Third System\u2122",
        "figsize": [8, 6],
        "verdict_text": "Patr\u00f3n leads on recall frequency; Lagavulin and Redbreast lead on slot position (always first when mentioned).",
    },
}
