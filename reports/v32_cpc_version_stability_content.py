# NOTE: cloned from v31_cpc_baseline_content.py on phase scaffold.
# All COVER, STANDFIRST, LEAD_DECK, EXEC_SUMMARY, PATTERNS,
# LIMITATIONS, WHATS_NEXT, HYPOTHESIS_DETAILS, CLOSING text
# must be re-written for the v0.32 cpc version stability
# substrate. Do not ship this file as-is.

"""
v0.32 — CPC Cross-Category Baseline
Third System™ brand-format report content module.

Pure-data module. Managerial register (P1–P5 propositional framing; NOT the
paper's H_* framing). Consumed by reports/build_report_v32.py (forked from v30);
the builder maps the four v32 chart PDFs into the proposition slots:

    chart_01_reconciliation_gate      -> P4 (reproducible)
    chart_02_cpc_within_substrate     -> P1 (measurable)
    chart_03_cpc_cross_category       -> P2 (category-specific)
    chart_04_defined_undefined_floor  -> P3 (recognition is not recall)

Same underlying findings as the SSRN paper, intentionally divergent register.
"""

# ----------------------------------------------------------------------------
COVER = {
    "eyebrow": "Third System™ · AIAS™ Measurement Program · v0.32",
    "title": "Consistency, Category by Category",
    "subtitle": "A cross-category baseline for AI Availability's Consistency reading (CPC)",
    "deck": "How stably AI recalls a brand can be measured — and where market dominance stops predicting it.",
}

# ----------------------------------------------------------------------------
STANDFIRST = (
    "Generative systems now sit between buyers and brands. The AI Availability "
    "program measures where a brand stands inside those systems. This report "
    "establishes the first cross-category reading of the program's second "
    "component, Consistency: how stably a brand is recalled across AI models, "
    "measured across five categories on a single instrument fixed in advance."
)

# ----------------------------------------------------------------------------
LEAD_DECK = (
    "A brand can be present in AI answers without being present reliably. One "
    "model names it, another does not; one phrasing surfaces it, the next omits "
    "it. Consistency captures that reliability as a single reading on a zero-to-one "
    "scale, where a brand recalled uniformly across the model panel approaches one "
    "and a brand recalled erratically approaches zero. Before the reading can "
    "guide anything, two questions have to be answered: does it actually separate "
    "brands, and does it behave differently across categories? Across five anchored "
    "categories the answer to both is yes, and the categories order themselves in a "
    "way that says more about how a category is discussed than about who leads it."
)

# ----------------------------------------------------------------------------
EXEC_SUMMARY = (
    "Five propositions carry this baseline. Consistency is measurable: the reading "
    "separates brands within every category examined rather than flattening to a "
    "single value (P1). It is category-specific: spirits is the least consistent "
    "category and skincare the most, with categories shaped by editorial and "
    "cultural discourse scoring lower than utilitarian ones (P2). Recognition is "
    "not recall: several of the most dominant brands in spirits, Johnnie Walker "
    "among them, are known to the models yet barely recalled in the channels that "
    "matter, and so carry no consistency reading at all (P3). The reading is "
    "reproducible: it reproduces the program's prior instrument exactly where the "
    "two overlap, so categories are comparable rather than re-defined study by "
    "study (P4). And it is a floor rather than a forecast: the reading is taken "
    "across models at a single point in time, and it covers the five categories "
    "where the measurement is uniform (P5)."
)

# ----------------------------------------------------------------------------
WHAT_WE_MEASURED = (
    "Consistency (CPC) is the stability of a brand's recall across a fixed panel of "
    "six AI models. For each brand the analysis counts how often each model recalls "
    "it across a set of category prompts, then scores the evenness of those counts: "
    "uniform recall scores near one, lopsided recall near zero. The reading uses "
    "recall only, not recognition, and was computed by rescoring recall data already "
    "collected in earlier phases. No new model queries were issued. A floor handles "
    "near-absent brands: any brand a model panel almost never recalls is marked "
    "undefined rather than scored as zero, since the stability of an almost-empty "
    "signal is not meaningful. Five categories met a common measurement standard and "
    "form the comparable set: audiophile headphones, skincare, cosmetics, automotive, "
    "and premium spirits."
)

# ----------------------------------------------------------------------------
PATTERNS = (
    "Three patterns stand out. First, consistency is real and uneven within every "
    "category; the reading discriminates among brands rather than assigning everyone "
    "the same score. Second, categories differ systematically. Ordered by median, "
    "consistency runs from premium spirits at 0.60, through headphones at 0.67, "
    "cosmetics at 0.74, and automotive at 0.76, to skincare at 0.80. The categories "
    "organized around critics and enthusiasts are the least consistent; the "
    "utilitarian categories are the most. Third, and most consequential for brand "
    "owners, recall does not follow market share. In spirits the global volume "
    "leaders are largely absent from the recalled set: Johnnie Walker, the leading "
    "Scotch by volume, is recalled so rarely that it has no consistency reading, and "
    "Jack Daniel's, Bacardi, and Jameson sit in the same position. The brands that do "
    "carry a reading mix large premium houses with smaller critical favorites. Being "
    "known and being named are different things, and consistency measures the second."
)

# ----------------------------------------------------------------------------
LIMITATIONS = (
    "This is a baseline, and its claims are bounded. The reading is taken across "
    "models within a panel, not across the different AI platforms a buyer actually "
    "uses, and it reflects a single point in time rather than a trend. Because "
    "consistency is defined only for brands with enough recall to measure, each "
    "category's reading describes its recalled brands, not its full roster. And the "
    "comparable set is five categories; two more were observed on a coarser grid and "
    "two were measured off-standard, so they are not part of the cross-category "
    "comparison."
)

# ----------------------------------------------------------------------------
WHATS_NEXT = (
    "Three extensions follow. A second measurement wave would turn this static "
    "reading into a test of whether consistency holds over time and across model "
    "version changes. A cross-platform reading would separate stability inside one "
    "model family from stability across the systems buyers encounter. And the "
    "recognition–recall gap, now seen in spirits and earlier in prestige skincare, "
    "is worth treating as a diagnostic in its own right: a way to find brands that "
    "are widely known yet quietly missing from the answers buyers receive."
)

# ----------------------------------------------------------------------------
# Proposition scoring (managerial analogue of the paper's hypothesis table)
HYPOTHESIS_SCORING = [
    {"id": "P1", "proposition": "Consistency is measurable.",
     "verdict": "Established",
     "basis": "Non-degenerate CPC variance in all five categories; the reading separates brands rather than flattening."},
    {"id": "P2", "proposition": "Consistency is category-specific.",
     "verdict": "Established",
     "basis": "Cross-category difference is significant (Kruskal–Wallis H = 21.51, p < 0.001); spirits lowest, skincare highest."},
    {"id": "P3", "proposition": "Recognition is not recall.",
     "verdict": "Documented",
     "basis": "Dominant spirits brands fall below the recall floor (Johnnie Walker mean recall 0.17); a gap also seen in prestige skincare."},
    {"id": "P4", "proposition": "The reading is reproducible.",
     "verdict": "Confirmed",
     "basis": "Reproduces the prior locked instrument exactly across 72 overlapping brands; categories are comparable, not redefined."},
    {"id": "P5", "proposition": "This is a floor, not a forecast.",
     "verdict": "By design",
     "basis": "Cross-model and single-wave; covers the five categories with uniform measurement geometry."},
]

# ----------------------------------------------------------------------------
HYPOTHESIS_DETAILS = {
    "P1": (
        "Within every category, the consistency reading spreads brands across a "
        "real range rather than clustering at one value. Skincare runs from 0.52 to "
        "0.94 and automotive from 0.64 to 1.00; even the tightest category, "
        "headphones, spans 0.57 to 0.69. The instrument distinguishes brands, which "
        "is the first thing any measure has to do."
    ),
    "P2": (
        "Median consistency differs across the five categories from 0.60 in spirits "
        "to 0.80 in skincare, and the difference is statistically reliable "
        "(Kruskal–Wallis H = 21.51, p < 0.001). The ordering tracks how a category "
        "is talked about: categories driven by editorial authority and cultural "
        "enthusiasm are recalled less consistently than utilitarian categories."
    ),
    "P3": (
        "Consistency is built on recall, and recall does not follow sales. In "
        "spirits, several volume leaders are recalled so rarely by the panel that "
        "they have no defined reading: Johnnie Walker sits at a mean recall of 0.17, "
        "alongside Jack Daniel's, Bacardi, and Jameson. The same recognition–recall "
        "gap appeared earlier in prestige skincare. For a brand owner this is the "
        "actionable signal: a brand can be universally recognized and still be "
        "missing from the answers buyers actually receive."
    ),
    "P4": (
        "The reading is anchored to the program's prior instrument. Recomputed on "
        "the categories the two share, it reproduces the earlier values exactly "
        "across all 72 brands. The generalization that lets the reading extend to "
        "categories with different channel structures contains the prior definition "
        "as a special case, so the cross-category numbers are comparable rather than "
        "a fresh definition introduced for this study."
    ),
    "P5": (
        "The baseline reads consistency across models at one moment, for the five "
        "categories where the measurement is uniform. It describes where brands "
        "stand now, not whether they will hold, and it describes recalled brands "
        "rather than full category rosters. Those are the boundaries the later "
        "components and the longitudinal work are built to extend."
    ),
}

# ----------------------------------------------------------------------------
CLOSING = (
    "Consistency joins Presence as a measurable coordinate of a brand's standing in "
    "AI. The cross-category baseline shows the reading works, that it varies with "
    "the character of a category, and that it surfaces a gap dominance alone hides: "
    "being known is not being named. That gap is where the next questions, and the "
    "next opportunities for brand owners, begin."
)
