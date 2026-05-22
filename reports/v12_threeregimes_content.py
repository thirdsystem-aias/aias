"""v0.12 brand-format report content modules — Three Empirical Regimes.

Schema-compatible with build_report_v11.py's read patterns. Forked from
v11_pmtrends_content.py with v0.12 substance: three-category construct-
validity expansion revealing three distinct empirical regimes of the
AI Availability / Mental Availability relationship.

Framing convention (locked at v0.12 lead): The pre-registered prediction
was that v0.11's signature would generalise. It didn't — and the falsification
reveals three distinct empirical regimes, each supporting the Tri-System
framework's separability claim in a different way.

ReportLab Paragraph HTML markup throughout (<sub>, <font>, <b>, <i>).
"""

# ----------------------------------------------------------------------------
# COVER
# ----------------------------------------------------------------------------

COVER = {
    "title":         "Three Empirical Regimes",
    "subtitle":      "AI Presence \u00d7 Google Trends Across Three Categories",
    "date":          "May 2026",
    "byline_short":  "Pablo Ulpiano Gonzalez Castro, Third System",
    "tagline":       "Independent measurement for the AI mediation layer.",
}

# ----------------------------------------------------------------------------
# STANDFIRST + LEAD DECK
# ----------------------------------------------------------------------------

STANDFIRST = (
    "The pre-registered prediction was that v0.11's PM software finding "
    "would generalise across categories. It didn't \u2014 and the "
    "falsification reveals something sharper."
)

LEAD_DECK = (
    "PM software replicates v0.11 within 0.010 ρ at both waves. Premium "
    "running shoes shows a structurally different regime: bivariate "
    "Spearman <font name='Helvetica'>\u03c1</font> = 0.81, but age and tier mediate "
    "40% of the correlation; partial <font name='Helvetica'>\u03c1</font> \u2248 0.47. "
    "Premium olive oil routes to descriptive-only \u2014 47% of the matched "
    "subset cannot be placed on the same scale: AI-present at 5-22%, but "
    "Trends below display threshold. <b>AI Availability is empirically "
    "separable from Mental Availability in three distinct ways.</b>"
)

# ----------------------------------------------------------------------------
# EXECUTIVE SUMMARY (list of paragraph strings)
# ----------------------------------------------------------------------------

EXEC_SUMMARY = [
    (
        "v0.11 established the AIAS construct-validity methodology in one category "
        "(project management software) and pre-announced a three-category expansion. "
        "v0.12 delivers that expansion: PM software is retained as the replication "
        "test, premium running shoes is added as a structurally different B2C category, "
        "and premium olive oil is added as a premium consumer packaged goods category "
        "with non-English production origins. The pre-registered prediction was that "
        "v0.11's boundary-mismatch signature would generalise across the three categories \u2014 "
        "the v0.11 marginal correlation magnitude, the leadership-zone divergence, and the "
        "Linear-style + Todoist-style diagnostic cases reproducing in 2 of 3 categories."
    ),
    (
        "The prediction is falsified at both the H5 magnitude bar and the H6 diagnostic-case "
        "bar. The falsifications, however, organise into a sharper substantive finding: the "
        "empirical relationship between AI Availability and Mental Availability is "
        "<b>category-dependent</b>, with three distinct empirical regimes observable in the "
        "v0.12 sample. What unifies them is the persistence of category-boundary mismatch "
        "(H3 falsified in both confirmatory-eligible categories). What differentiates them is "
        "magnitude and structure."
    ),
    (
        "<b>Regime 1 \u2014 PM software replicates v0.11 with eerie precision.</b> "
        "Spearman <font name='Helvetica'>\u03c1</font> = 0.506 at t<sub>1</sub>, 0.482 at t<sub>2</sub> \u2014 "
        "within 0.010 of v0.11's 0.496 and 0.476 at both waves. H3 falsifies identically at "
        "1 of 3 both waves. H6 confirms with Linear and Todoist surfacing as the same "
        "diagnostic cases. The v0.11 measurement is not a single-collection artefact \u2014 "
        "the construct correlation in PM software is structurally near 0.50 with concentrated "
        "boundary mismatch, reproducibly so across versions."
    ),
    (
        "<b>Regime 2 \u2014 Premium running shoes is a different empirical regime.</b> "
        "Spearman <font name='Helvetica'>\u03c1</font> = 0.808 at t<sub>1</sub>, 0.786 at t<sub>2</sub> \u2014 "
        "well above the moderate-to-strong threshold. H1 confirms decisively. But the partial "
        "<font name='Helvetica'>\u03c1</font> after age + tier control drops to 0.466 and 0.488 (a decrement "
        "of 0.34, against PM software's decrement of 0.07). Brand age and competitive tier "
        "mediate approximately 40% of the bivariate correlation. The strongest signal is "
        "driven by older incumbents (Asics, Nike, Adidas, Brooks, New Balance) showing "
        "jointly high AI Presence and high Trends. H3 still falsifies (2 of 3 both waves); "
        "H6 falsifies asymmetrically \u2014 Linear-style brands surface (Brooks at t<sub>1</sub>, "
        "Hoka at t<sub>2</sub>), but no Todoist-style brand surfaces in either wave."
    ),
    (
        "<b>Regime 3 \u2014 Premium olive oil reveals Category-Scale Mismatch.</b> "
        "Routes to descriptive-only per pre-reg \u00a73.4a (n = 8 at Worldwide, n = 7 at US, "
        "below the hard floor of 10). The substantive finding is sharper than the routing "
        "suggests: <b>7 of 15 matched-subset olive oil brands (46.7%)</b> have AI Presence "
        "rates of at least 5% at either wave, but Trends signal below the platform's "
        "display threshold. The two constructs cannot be placed on the same scale at all "
        "for nearly half the matched subset. The seven scale-mismatch brands include "
        "Frescobaldi Laudemio, Olio Verde, Lucini, McEvoy Ranch, Manni, Colonna, and "
        "Núñez de Prado \u2014 all returning the platform message 'Google Trends hasn't "
        "returned any results for this query' against the out-of-sample window."
    ),
    (
        "The substantive contribution of v0.12 is the identification of these three regimes "
        "as distinct empirical manifestations of the same theoretical separability claim. "
        "The Tri-System Brand Growth framework's central claim is that AI Availability is "
        "empirically separable from Mental Availability \u2014 not equivalent at the level of "
        "practical inference. v0.11 supported this claim through a single-category boundary-"
        "mismatch finding. v0.12 supports the same claim more broadly: AI Availability is "
        "separable from Mental Availability in three distinct empirical ways across three "
        "structurally different categories. The framework's separability claim does not "
        "require a uniform mechanism of separation across categories; it requires that "
        "separability obtain. v0.12 demonstrates that it does, with the structural form of "
        "the separation varying with category characteristics."
    ),
]

# ----------------------------------------------------------------------------
# WHAT WE MEASURED
# ----------------------------------------------------------------------------

WHAT_WE_MEASURED = {
    "heading": "What We Measured",
    "paragraphs": [
        (
            "v0.12 tests the cross-sectional correlation between two independent brand-level "
            "signals across three categories: per-brand AI Presence rate (drawn from v0.9's "
            "deposited matched-subset LLM measurements) and per-brand Google Trends search "
            "interest (acquired fresh under a pre-registered protocol). The design adds two "
            "cross-category hypotheses (H5 cross-category generalisation; H6 cross-category "
            "diagnostic-case detection) and a descriptive-only route for categories where "
            "the n-floor is breached, formalised in pre-reg \u00a73.4a."
        ),
        (
            "<b>Three categories.</b> Project management software (18 brands, retained from "
            "v0.11 as the replication test); premium running shoes (13 brands, new \u2014 a "
            "high-volume B2C category with well-known incumbents and DTC challengers); "
            "premium olive oil (15 brands in matched subset, new \u2014 a premium CPG category "
            "with non-English production origins). The three-category selection deliberately "
            "samples three positions on the cross-cutting dimensions of category volume, "
            "B2B vs B2C, and English vs multi-lingual production."
        ),
        (
            "<b>Per-category pivot rescaling.</b> Each category has its own pivot brand "
            "(Asana for PM software, California Olive Ranch for olive oil, Asics for running "
            "shoes). Each pivot was validated for stability against the out-of-sample window "
            "prior to lock per pre-reg \u00a76.A (California Olive Ranch mean 83.5, CV 12.4%; "
            "Asics mean 84.5, CV 7.9%). Pivot-rescaling converts each bundle-relative 0\u2013100 "
            "daily value to a pivot-normalised daily value where the pivot is fixed at 100 "
            "by construction."
        ),
        (
            "<b>Two waves seven days apart.</b> t<sub>1</sub> Trends window: 27 April \u2013 "
            "3 May 2026. t<sub>2</sub> Trends window: 4 May \u2013 10 May 2026. Both regions "
            "(Worldwide primary; US sensitivity). Single locked acquisition session at "
            "2026-05-11T10:33:22Z covering 20 bundles \u00d7 2 regions = 280 (brand, day) "
            "cells."
        ),
        (
            "<b>Pre-registration.</b> Locked at git commit ae4bd3a (tag <i>v0.12-prereg</i>) "
            "prior to any Google Trends acquisition call against the wave windows. Six per-"
            "category hypotheses (H1\u2013H4 plus sensitivities), two cross-category hypotheses "
            "(H5, H6), and the Category-Scale Mismatch reporting rule (\u00a710.2). Routing "
            "rule \u00a73.4a: categories with fewer than 10 brands clearing E1b at either "
            "wave route to descriptive-only. The cross-category hypotheses become "
            "2-of-2 effective if one category routes descriptive."
        ),
    ],
}

# ----------------------------------------------------------------------------
# FINDINGS (PATTERNS in v10/v11 schema)
# ----------------------------------------------------------------------------

PATTERNS = [
    {
        "number": 1,
        "title": "PM software replicates v0.11 with high precision",
        "chart_slot": "f1_pm_rank_shift",
        "paragraphs": [
            (
                "v0.11's PM software finding reproduces under independent Trends acquisition "
                "seven days later. Spearman <font name='Helvetica'>\u03c1</font> = 0.506 at t<sub>1</sub> and "
                "0.482 at t<sub>2</sub> \u2014 within 0.010 of v0.11's 0.496 and 0.476 at both "
                "waves. H3 falsifies identically at 1 of 3 both waves. The Linear paradox and "
                "Todoist inverse surface as the same diagnostic cases."
            ),
            (
                "Spearman <font name='Helvetica'>\u03c1</font> at t<sub>1</sub> = 0.506 (n = 17; p<sub>1t</sub> = "
                "0.019); at t<sub>2</sub> = 0.482 (n = 18; p<sub>1t</sub> = 0.022). The wave-to-"
                "wave direction of the just-miss flips: v0.11 missed at t<sub>1</sub> by 0.004, "
                "v0.12 misses at t<sub>2</sub> by 0.018. But the overall pattern reproduces "
                "within sampling error: ρ near 0.5 with the both-waves conjunction failing at "
                "the magnitude threshold."
            ),
            (
                "<b>H2 confirms with |\u0394<font name='Helvetica'>\u03c1</font>| = 0.024</b> (v0.11 reported "
                "0.020 \u2014 almost identical reproducibility across versions). The cross-wave "
                "stability of PM software's construct-validity correlation is itself "
                "reproducible. Whatever H1 measured at v0.11, it measured the same thing at v0.12."
            ),
            (
                "<b>H3 falsifies identically.</b> At t<sub>1</sub>, the AI-top-three is Linear, "
                "Asana, Notion; the Trends-top-five is Notion, Jira, Trello, ClickUp, Confluence. "
                "Only Notion overlaps. At t<sub>2</sub>, the AI-top-three is Linear, Asana, Jira; "
                "the Trends-top-five is unchanged. Only Jira overlaps. Identical to v0.11 \u2014 "
                "1 of 3 at both waves, same divergence concentration at the leadership zone."
            ),
            (
                "<b>H4 partial <font name='Helvetica'>\u03c1</font> = 0.417 at t<sub>1</sub>, 0.434 at t<sub>2</sub></b>, "
                "after age + tier control. Below the 0.5 magnitude bar at both waves \u2014 a "
                "decrement of 0.09 from bivariate. The covariate absorption is real but small. "
                "v0.11 reported 0.407 and 0.428; v0.12 is within 0.01 at both waves. Identical "
                "structural finding."
            ),
            (
                "<b>H6 diagnostic-case detection confirms.</b> Linear is the unique Linear-"
                "style brand at both waves (AI Presence 86.5% at t<sub>1</sub>, Trends rescaled "
                "1.88). Todoist is the unique Todoist-style brand at t<sub>1</sub>; Basecamp "
                "joins Todoist in the Todoist-style category at t<sub>2</sub>. The v0.11 "
                "diagnostic cases are still the diagnostic cases at v0.12. PM software's "
                "construct-validity finding has direct test-retest validity at the category "
                "level."
            ),
        ],
    },
    {
        "number": 2,
        "title": "Running shoes is a structurally different regime",
        "chart_slot": "f2_running_partial",
        "force_page_break": True,
        "paragraphs": [
            (
                "Bivariate Spearman <font name='Helvetica'>\u03c1</font> = 0.808 at t<sub>1</sub>, "
                "0.786 at t<sub>2</sub> \u2014 well above the moderate-to-strong threshold "
                "and significant at p<sub>1t</sub> &lt; 0.002 at both waves. H1 confirms "
                "decisively. The partial <font name='Helvetica'>\u03c1</font> tells a different story: "
                "0.466 and 0.488. Age and tier mediate 40% of the bivariate correlation."
            ),
            (
                "<b>H1 confirms; H4 falsifies; the decrement quantifies the regime.</b> "
                "Bivariate <font name='Helvetica'>\u03c1</font> = 0.81 drops to partial <font name='Helvetica'>\u03c1</font> "
                "\u2248 0.47 after controlling for brand age and competitive tier \u2014 a "
                "decrement of 0.34. The corresponding decrement in v0.11 PM software was 0.09. "
                "Running shoes' strong bivariate signal is substantially confounded by joint "
                "variation in age-of-brand: older incumbents (Asics, Nike, Adidas, Brooks, "
                "New Balance) show jointly high AI Presence and high Trends, and that joint "
                "variation drives the correlation."
            ),
            (
                "<b>The residual partial correlation matches v0.11.</b> Once age + tier is "
                "controlled, running shoes' direct AI-to-Trends construct correlation is "
                "approximately 0.47 \u2014 statistically indistinguishable from v0.11 PM "
                "software's partial ρ of 0.42 (and from v0.12 PM software's 0.43). The "
                "categories are not actually different in the underlying relationship; they "
                "are different in how much of that relationship is explained by age-driven "
                "joint visibility versus direct construct correlation."
            ),
            (
                "<b>H3 falsifies at 2 of 3 both waves.</b> At t<sub>1</sub>, the AI-top-three "
                "is Asics, Brooks, New Balance; Brooks ranks sixth in Trends despite being "
                "top-three in AI Presence. At t<sub>2</sub>, the AI-top-three is Asics, Brooks, "
                "Hoka; Brooks again falls outside the Trends top-five. The leadership-zone "
                "boundary mismatch is present, just less concentrated than PM software's."
            ),
            (
                "<b>H6 falsifies asymmetrically.</b> Linear-style brands surface in running "
                "shoes (Brooks at t<sub>1</sub>, AI Presence 56% with Trends rescaled 4.69; "
                "Hoka at t<sub>2</sub>, AI Presence 51% with Trends rescaled 3.23). Both are "
                "performance-running incumbents with strong narratives in athletic discourse "
                "that LLM training data captures with high salience. But no Todoist-style "
                "brand surfaces in either wave \u2014 no running brand combines AI Presence "
                "below 5% with Trends rescaled above 20. The boundary mismatch is "
                "<b>unidirectional</b>: AI over-recommends certain incumbents, but does not "
                "under-recommend brands well-known to consumer search."
            ),
            (
                "The substantive reading is that running shoes occupies a different empirical "
                "regime from v0.11 PM software despite sharing the boundary-mismatch mechanism. "
                "The bivariate correlation is strong; the magnitude is well above the v0.11 "
                "signature. But the direct construct-validity relationship after age and tier "
                "control is comparable to PM software's. The category's mechanism is not 'no "
                "boundary mismatch' but 'asymmetric boundary mismatch with age-driven bivariate "
                "covariance.'"
            ),
        ],
    },
    {
        "number": 3,
        "title": "Olive oil reveals Category-Scale Mismatch",
        "chart_slot": "f3_olive_scale_mismatch",
        "force_page_break": True,
        "paragraphs": [
            (
                "Premium olive oil routes to descriptive-only per pre-reg \u00a73.4a "
                "(n = 8 at Worldwide; n = 7 at US; both below the hard floor of 10). "
                "The substantive finding is sharper than the routing suggests: <b>7 of 15 "
                "matched-subset olive oil brands (46.7%)</b> have AI Presence rates of at "
                "least 5% at either wave, but Trends signal below the platform's display "
                "threshold. The two constructs cannot be placed on the same scale at all."
            ),
            (
                "Spearman <font name='Helvetica'>\u03c1</font> across the 8 PASS brands at Worldwide is 0.168 "
                "at t<sub>1</sub> and \u22120.095 at t<sub>2</sub> \u2014 essentially zero, "
                "with the wave-to-wave drift across the small PASS subset uninformative on its "
                "own. The PASS subset is too small for confirmatory inference; the substantive "
                "olive oil finding lives in the descriptive-only arm, not in the PASS subset "
                "correlation."
            ),
            (
                "<b>The seven scale-mismatch brands.</b> Frescobaldi Laudemio (AI Presence "
                "22\u201323% at both waves; Trends below threshold). Olio Verde (17\u201323%; "
                "below threshold). Lucini (18\u201320%; below threshold). McEvoy Ranch (5\u20139%; "
                "below threshold). Manni (3\u20135%; below threshold). Colonna (4\u20135%; "
                "below threshold). Núñez de Prado (4\u20135%; below threshold). All seven brands "
                "return the platform message 'Google Trends hasn't returned any results for "
                "this query' against the out-of-sample window at solo Phase B validation. The "
                "non-trivial AI Presence rates are not measurement noise \u2014 they are stable "
                "across waves and consistent across the two models in the matched subset."
            ),
            (
                "<b>The mechanism candidate is asymmetric specialist-vs-mass surface area.</b> "
                "Premium artisanal olive oil brands have strong presence in food-publication "
                "discourse, restaurant recommendations, gift-guide listings, sommelier-style "
                "curation, and direct-to-consumer marketing channels that LLM training data "
                "captures. They have limited mass-market consumer-search interest under brand-"
                "name queries because the typical consumer of premium olive oil discovers "
                "brands through curation rather than direct search. The asymmetry is "
                "structurally different from the boundary mismatches in PM software (about "
                "category framing) and running shoes (about age-driven joint visibility); it "
                "is about the relative size of the specialist-recommendation surface versus "
                "the mass-search surface for the same brand."
            ),
            (
                "<b>Why this is the strongest separability evidence.</b> In PM software and "
                "running shoes, AI Availability and Mental Availability are correlated but "
                "distinct (the v0.11 / v0.12 finding) or strongly correlated with shared age "
                "confound (the running shoes regime). In premium olive oil, the constructs are "
                "operating on different scales entirely: AI systems treat seven matched-subset "
                "brands as having meaningful category presence, while Google's consumer-search "
                "measurement infrastructure returns no signal at all for the same brand names "
                "at the same wave windows. The category-scale mismatch is the strongest "
                "empirical evidence in the v0.12 dataset that AI Availability is a separable "
                "construct \u2014 not just a tighter or differently-bounded version of Mental "
                "Availability, but a fundamentally different operational layer."
            ),
        ],
    },
    {
        "number": 4,
        "title": "Three regimes, one shared mechanism",
        "chart_slot": "f4_h6_zones_three_cats",
        "force_page_break": True,
        "paragraphs": [
            (
                "Across the three v0.12 categories, the shared mechanism is category-boundary "
                "mismatch (H3 falsified in both confirmatory-eligible categories). The "
                "differentiating dimensions are <b>magnitude of correlation</b> and "
                "<b>structural source of correlation</b>. Three distinct empirical "
                "manifestations of the same theoretical separability claim."
            ),
            (
                "<b>The shared mechanism.</b> In PM software (1 of 3 top brands overlap), "
                "running shoes (2 of 3), and olive oil (constructs not on same scale entirely), "
                "AI's category boundary differs structurally from consumer search's. The "
                "specific brands surfaced inside AI's category are not the same brands "
                "surfaced inside consumer search's category. That boundary divergence is the "
                "shared mechanism."
            ),
            (
                "<b>Two differentiating dimensions.</b> Magnitude: bivariate "
                "<font name='Helvetica'>\u03c1</font> ranges from near-zero in olive oil's PASS subset to "
                "marginal in PM software (\u22480.50) to strong in running shoes (\u22480.80). "
                "Structural source: direct construct relation (PM software, where partial "
                "<font name='Helvetica'>\u03c1</font> \u22480.42 is comparable in magnitude to bivariate "
                "<font name='Helvetica'>\u03c1</font>); age-mediated joint variation (running shoes, where "
                "bivariate <font name='Helvetica'>\u03c1</font> \u22480.80 drops to partial "
                "<font name='Helvetica'>\u03c1</font> \u22480.47); scale incommensurability (olive oil, where "
                "Trends signal is absent for nearly half the matched subset)."
            ),
            (
                "<b>Why H5 / H6 falsifications are theoretically constructive.</b> "
                "H5 (v0.11 signature generalises in 2 of 2 applicable categories) falsified "
                "for asymmetric reasons: PM software's t<sub>1</sub> <font name='Helvetica'>\u03c1</font> = 0.506 "
                "just clears the 0.5 threshold (within sampling error of v0.11's signature); "
                "running shoes is substantially above 0.5. The two falsifications carry "
                "different content. H6 falsified at 1 of 2 \u2014 PM software confirms with "
                "Linear and Todoist; running shoes lacks any Todoist-style brand. The "
                "asymmetric H6 falsification in running shoes is itself a substantive finding "
                "about that category's boundary structure."
            ),
            (
                "<b>The pooled rank-within-category sensitivity confirms the cross-category "
                "structure.</b> Stacking rank-within-category data across PM and running "
                "(olive oil excluded for descriptive routing) yields Spearman "
                "<font name='Helvetica'>\u03c1</font> = 0.624 at t<sub>1</sub> (n = 29; p &lt; 0.001) and "
                "0.580 at t<sub>2</sub> (n = 30; p &lt; 0.001). Within-category brand-ranking "
                "by AI Presence is positively associated with within-category brand-ranking "
                "by Trends, robustly across both confirmatory categories. The pooled "
                "correlation is stronger than v0.11's per-category <font name='Helvetica'>\u03c1</font> \u2014 "
                "driven largely by running shoes' strong bivariate signal."
            ),
            (
                "The substantive contribution of v0.12 is the identification of these three "
                "regimes as distinct empirical manifestations of the same theoretical "
                "separability claim. The Tri-System Brand Growth framework's central claim "
                "\u2014 that AI Availability is empirically separable from Mental Availability "
                "\u2014 does not require a uniform mechanism of separation across categories. "
                "It requires that separability obtain. v0.12 demonstrates that it does, with "
                "the structural form of the separation varying with category characteristics."
            ),
        ],
    },
]

# ----------------------------------------------------------------------------
# HYPOTHESIS SCORING TABLE
# ----------------------------------------------------------------------------

HYPOTHESIS_SCORING = {
    "heading": "Hypothesis Scoring",
    "intro": (
        "All thresholds and tests locked at <i>v0.12-prereg</i> (commit ae4bd3a, 11 May "
        "2026 UTC) prior to any Google Trends acquisition call against the wave windows. "
        "Per-category pivot exemption from E1b applied per pre-reg \u00a75.1 "
        "(sd = 0 by pivot construction). Categories routing to descriptive-only per "
        "\u00a73.4a (n &lt; 10 hard floor) carry no H1\u2013H4 inference."
    ),
    "rows": [
        (
            "H1 PM",
            "Spearman <font name='Helvetica'>\u03c1</font> &gt; 0.5 AND p<sub>1t</sub> &lt; 0.05, both waves",
            "<font name='Helvetica'>\u03c1</font><sub>t<sub>1</sub></sub> = 0.506; <font name='Helvetica'>\u03c1</font><sub>t<sub>2</sub></sub> = 0.482",
            "FALSIFIED",
            "disconfirmed",
        ),
        (
            "H2 PM",
            "|<font name='Helvetica'>\u0394\u03c1</font>| \u2264 0.15",
            "|<font name='Helvetica'>\u0394\u03c1</font>| = 0.024",
            "CONFIRMED",
            "confirmed",
        ),
        (
            "H3 PM",
            "AI top-3 \u2286 Trends top-5, both waves",
            "1 / 3 at both waves",
            "FALSIFIED",
            "disconfirmed",
        ),
        (
            "H4 PM",
            "Partial <font name='Helvetica'>\u03c1</font> &gt; 0.5, both waves",
            "partial <font name='Helvetica'>\u03c1</font><sub>t<sub>1</sub></sub> = 0.417; partial <font name='Helvetica'>\u03c1</font><sub>t<sub>2</sub></sub> = 0.434",
            "FALSIFIED",
            "disconfirmed",
        ),
        (
            "H1 Run",
            "Spearman <font name='Helvetica'>\u03c1</font> &gt; 0.5 AND p<sub>1t</sub> &lt; 0.05, both waves",
            "<font name='Helvetica'>\u03c1</font><sub>t<sub>1</sub></sub> = 0.808 (p &lt; 0.001); <font name='Helvetica'>\u03c1</font><sub>t<sub>2</sub></sub> = 0.786 (p = 0.001)",
            "CONFIRMED",
            "confirmed",
        ),
        (
            "H2 Run",
            "|<font name='Helvetica'>\u0394\u03c1</font>| \u2264 0.15",
            "|<font name='Helvetica'>\u0394\u03c1</font>| = 0.022",
            "CONFIRMED",
            "confirmed",
        ),
        (
            "H3 Run",
            "AI top-3 \u2286 Trends top-5, both waves",
            "2 / 3 at both waves",
            "FALSIFIED",
            "disconfirmed",
        ),
        (
            "H4 Run",
            "Partial <font name='Helvetica'>\u03c1</font> &gt; 0.5, both waves",
            "partial <font name='Helvetica'>\u03c1</font><sub>t<sub>1</sub></sub> = 0.466; partial <font name='Helvetica'>\u03c1</font><sub>t<sub>2</sub></sub> = 0.488",
            "FALSIFIED",
            "disconfirmed",
        ),
        (
            "H1\u2013H4 Oil",
            "n-floor \u2265 10 per wave",
            "n = 8 (WW), n = 7 (US); below hard floor",
            "Descriptive-only per \u00a73.4a",
            "descriptive",
        ),
        (
            "\u00a710.2 Oil",
            "Category-Scale Mismatch index",
            "7 / 15 = 46.7% of matched subset (AI \u2265 5% AND Trends below display threshold)",
            "Descriptive finding",
            "descriptive",
        ),
        (
            "H5",
            "v0.11 signature in 2 of 2 applicable categories",
            "0 of 2 (PM <font name='Helvetica'>\u03c1</font> just clears 0.5 at t<sub>1</sub>; Running <font name='Helvetica'>\u03c1</font> above 0.5)",
            "FALSIFIED",
            "disconfirmed",
        ),
        (
            "H6",
            "Linear-style + Todoist-style in 2 of 2 applicable categories",
            "1 of 2 (PM confirms; Running missing Todoist-style)",
            "FALSIFIED",
            "disconfirmed",
        ),
    ],
}

# ----------------------------------------------------------------------------
# HYPOTHESIS DETAILS (per-hypothesis expansion below the scoring table)
# ----------------------------------------------------------------------------

HYPOTHESIS_DETAILS = {
    "heading": "Hypothesis Details",
    "intro": (
        "Per-hypothesis claim, operationalisation, and result. The both-waves conjunction "
        "for H1 / H4 provides built-in family-wise error rate control (joint p \u2248 "
        "0.05\u00b2 = 0.0025 under the null). Cross-category H5 / H6 evaluate against the "
        "effective 2-of-2 rule because olive oil routes to descriptive-only."
    ),
    "items": [
        (
            "PM",
            (
                "<b>PM software replication.</b> v0.11's PM finding reproduces under "
                "independent Trends acquisition seven days later. H1 falsifies at the magnitude "
                "bar at one wave (t<sub>1</sub> ρ = 0.506 just clears 0.5; t<sub>2</sub> ρ = 0.482 "
                "below). H2 confirms with |\u0394ρ| = 0.024. H3 falsifies identically at 1/3 both "
                "waves with Notion / Jira as the overlapping brands. H4 partial ρ = 0.42 (t<sub>1</sub>) "
                "and 0.43 (t<sub>2</sub>) \u2014 covariate absorption is real but small "
                "(decrement of 0.09 from bivariate). The construct in PM software is reproducibly "
                "near the marginal threshold with concentrated boundary mismatch."
            ),
        ),
        (
            "Run",
            (
                "<b>Premium running shoes.</b> H1 confirms decisively (bivariate ρ \u2248 0.80 "
                "both waves, p &lt; 0.002). H2 confirms |\u0394ρ| = 0.022. H3 falsifies at "
                "2/3 both waves (Brooks AI-top-3 but Trends rank 6). H4 falsifies with partial "
                "ρ \u2248 0.47 \u2014 a decrement of 0.34 from bivariate, indicating that age + "
                "tier mediate approximately 40% of the bivariate correlation. The residual "
                "partial correlation matches v0.11 PM software's partial ρ \u2248 0.42, suggesting "
                "the direct AI-to-Trends construct relationship is comparable across categories "
                "once the age-of-brand confound is removed."
            ),
        ),
        (
            "Oil",
            (
                "<b>Premium olive oil.</b> Routes to descriptive-only per \u00a73.4a (n = 8 "
                "Worldwide, n = 7 US; both below the hard floor of 10). The Category-Scale "
                "Mismatch finding (\u00a710.2): 7 of 15 matched-subset brands have AI Presence "
                "\u2265 5% at either wave but Trends signal below the platform's display "
                "threshold. The seven scale-mismatch brands (Frescobaldi Laudemio, Olio Verde, "
                "Lucini, McEvoy Ranch, Manni, Colonna, Núñez de Prado) constitute the strongest "
                "separability evidence in the v0.12 dataset: the two constructs cannot be placed "
                "on the same scale at all for nearly half the matched subset."
            ),
        ),
        (
            "H5",
            (
                "<b>H5 cross-category generalisation.</b> v0.11 signature defined as ρ &lt; 0.5 "
                "AND p &lt; 0.05 AND H3 falsified, at both waves. Applicable categories: PM "
                "software and running shoes (olive oil descriptive). Required: 2 of 2 effective. "
                "<b>FALSIFIED.</b> PM software fails because t<sub>1</sub> ρ = 0.506 just clears "
                "the 0.5 threshold (within sampling error of v0.11's signature; the wave-to-wave "
                "direction of the just-miss flipped). Running shoes fails because ρ is in a "
                "different magnitude regime entirely (\u22480.80 \u2014 well above the v0.11 "
                "signature). The two falsifications carry different substantive content."
            ),
        ),
        (
            "H6",
            (
                "<b>H6 cross-category diagnostic-case detection.</b> Linear-style brand "
                "(AI \u2265 50% AND Trends \u2264 5) AND Todoist-style brand (AI \u2264 5% AND "
                "Trends \u2265 20) surface at both waves in 2 of 2 applicable categories. "
                "<b>FALSIFIED at 1 of 2.</b> PM software confirms: Linear-style = Linear at both "
                "waves; Todoist-style = Todoist (and Basecamp at t<sub>2</sub>). Running shoes "
                "confirms Linear-style (Brooks at t<sub>1</sub>, Hoka at t<sub>2</sub>) but no "
                "Todoist-style brand surfaces. The asymmetric H6 falsification in running shoes "
                "is itself a substantive finding about that category's unidirectional boundary "
                "mismatch."
            ),
        ),
    ],
}

# ----------------------------------------------------------------------------
# LIMITATIONS
# ----------------------------------------------------------------------------

LIMITATIONS = {
    "heading": "Limitations",
    "paragraphs": [
        (
            "<b>Single-acquisition design.</b> The v0.12 Trends acquisition was executed at a "
            "single locked timestamp covering both waves. The replication evidence for v0.11 PM "
            "software is therefore between-version (v0.11 collection 10 May 2026; v0.12 "
            "collection 11 May 2026, one day apart) rather than within-version. A future v0.13 "
            "design with multiple independent acquisitions within the same pre-registered "
            "category would strengthen the test-retest validity claim at the methodology level."
        ),
        (
            "<b>Small olive oil n.</b> The olive oil descriptive-only route is methodologically "
            "defensible per pre-reg \u00a73.4a, but the n = 8 PASS subset is below the threshold "
            "for any meaningful correlation inference. The substantive olive oil interpretation "
            "rests on the absolute fact of scale mismatch \u2014 that 7 brands have AI Presence "
            "\u2265 5% with Trends below display threshold \u2014 rather than on any precise "
            "quantitative claim about the magnitude of the mismatch. A larger olive oil registry "
            "(50+ brands spanning the full premium-to-mass spectrum) would clarify whether the "
            "scale-mismatch index converges to a stable population value."
        ),
        (
            "<b>Bundle-padding methodology lesson.</b> The olive oil Bundle 2 padding term "
            "(\u201cextra virgin olive oil\u201d) is a generic category-level search query with "
            "absolute search volume orders of magnitude higher than any individual brand in the "
            "bundle. This swamped the bundle's 0\u2013100 relative-scaling reference at "
            "acquisition and produced quantization noise in the pivot-rescaled values for "
            "Brightland, Graza, and Kosterina. Documented in DEVIATIONS.md as a v0.13 design "
            "lesson: bundle padding must be brand-volume-comparable, not category-generic. The "
            "lesson does not modify any pre-registered hypothesis or routing rule and does not "
            "affect the categorical conclusion that olive oil routes to descriptive-only."
        ),
        (
            "<b>Single external validator.</b> v0.12 tests construct validity against one "
            "external behavioural validator (Google Trends search interest). A multi-validator "
            "approach \u2014 testing AI Presence simultaneously against search interest, social-"
            "media mention rates, retail sales data where available, and consumer-survey aided-"
            "recall measures \u2014 would generalise the construct-validity claim from a single-"
            "validator finding to a multi-validator finding. Such a design is beyond the scope "
            "of v0.12 but is the medium-term goal of the AIAS programme."
        ),
        (
            "<b>Open question of practical predictive validity for purchase behaviour.</b> "
            "v0.12 establishes construct validity at the category level for AI Presence against "
            "Google Trends search interest. The relationship between AI Presence and actual "
            "purchase behaviour at the brand level \u2014 the question that ultimately matters "
            "for the Tri-System Brand Growth framework's practical claims \u2014 remains the "
            "object of future Phase 3 work. The category-dependent nature of the AI-Presence-"
            "to-Trends relationship documented in this report suggests that the AI-Presence-to-"
            "purchase relationship is likely to be category-dependent as well."
        ),
    ],
}

# ----------------------------------------------------------------------------
# WHAT'S NEXT
# ----------------------------------------------------------------------------

WHATS_NEXT = {
    "heading": "What's Next",
    "paragraphs": [
        (
            "<b>v0.13 \u2014 Full-category construct validity panel.</b> Extends to five "
            "categories by adding premium facial skincare and personal finance to the v0.12 "
            "three-category set. Personal finance carries the Mint phantom-brand effect "
            "documented in v0.7 and v0.10 and is expected on theoretical grounds to show a "
            "<b>fourth empirical regime</b> distinct from the three documented here \u2014 "
            "phantom brands with non-zero AI Presence and exactly zero Trends signal sit at "
            "one tail of the construct-validity distribution. Premium facial skincare is "
            "structurally similar to premium olive oil (B2C consumer packaged goods with "
            "specialist-vs-mass surface asymmetry) and is expected to test whether the "
            "Category-Scale Mismatch regime reproduces in a structurally adjacent category."
        ),
        (
            "<b>Cross-lingual replication.</b> v0.8's discourse-language bias finding "
            "documented that AI category boundaries depend on the language of the AI query. "
            "The construct-validity question in cross-lingual categories is whether the "
            "AI-Presence-to-Trends correlation depends on the language of the AI query, the "
            "language of the Trends acquisition, or both. Premium tea and traditional spirits "
            "are pre-identified candidate categories for the cross-lingual construct-validity "
            "test."
        ),
        (
            "<b>Tri-System Brand Growth manuscript</b> (Gonzalez Castro, 2026, in preparation). "
            "The v0.12 three-regimes finding sharpens the framework's empirical content. The "
            "category-dependent nature of the AI Availability / Mental Availability relationship "
            "is a candidate empirical anchor for the framework's separability claim \u2014 "
            "AI Availability as a third system whose relationship to Mental Availability varies "
            "systematically with category structure."
        ),
        (
            "<b>Causal-mechanism studies.</b> v0.12 establishes covariation across three regimes; "
            "the next-step question is what specifically about each category produces its regime. "
            "Brand age, category-discourse surface asymmetry, and category-framing tightness "
            "are candidate mechanisms in the three regimes documented here. Mechanism studies "
            "operationalising those candidates are the medium-term research path."
        ),
        (
            "<b>Phase 4 (AIAS components 2\u20136).</b> Construct validity established for AI "
            "Presence in v0.11\u2013v0.13 is a precondition for measurement work on Ranking, "
            "Consistency, Coverage, Grounding, and Sentiment. The v0.12 three-regimes finding "
            "suggests that the construct-validity bar for each AIAS component is unlikely to "
            "be a clean uniform correlation with any single external proxy across all categories."
        ),
    ],
}

# ----------------------------------------------------------------------------
# CLOSING
# ----------------------------------------------------------------------------

CLOSING = {
    "byline_long": [
        "Pablo Ulpiano Gonzalez Castro",
        "Principal Researcher, Third System",
        "Faculty, MPS Branding Program, School of Visual Arts",
    ],
    "datasets": [
        (
            "OSF project ec6wh, /v12/. Inputs (v0.9 AI Presence rates), Google Trends raw "
            "responses (20 pivot-bundle JSONs across 2 regions \u2014 PM software 5 bundles, "
            "olive oil 2 bundles, running shoes 3 bundles), topic-ID suggestion logs, pre-"
            "acquisition validation outputs (solo and bundled E1a checks), brand age source "
            "table (46 rows across 3 categories), registry files frozen at v0.6's final state, "
            "scoring outputs, build scripts, this report, and the matching SSRN working paper."
        ),
        (
            "Companion SSRN working paper (Gonzalez Castro 2026, SSRN 6748341). "
            "Cross-references: AI Availability foundational paper (SSRN 6659000); AIAS "
            "Presence Measurement Protocol v1.1 (SSRN 6722319); v0.6 Cross-Category Findings "
            "(SSRN 6720959); v0.7 Phantom-Brand Persistence Phase 2 BBB (SSRN 6721779); "
            "v0.8 Discourse-Language Knives (SSRN 6728000); v0.9 Longitudinal Re-Baseline "
            "(SSRN 6736878); v0.10 Naive-Phantom Rate Stability (SSRN 6741163); v0.11 PM "
            "Software \u00d7 Trends Construct Validity Pilot (SSRN 6745040)."
        ),
    ],
    "methodology_log": (
        "v0.12 follows AIAS Presence Measurement Protocol v1.1 (unchanged from v0.9). "
        "Pre-registration locked at git tag v0.12-prereg (commit ae4bd3a) on 11 May 2026 UTC "
        "prior to acquisition. Acquisition session UTC timestamp 2026-05-11T10:33:22Z. "
        "DEVIATIONS.md Entry 1 documents the olive oil Bundle 2 padding methodology lesson "
        "as a non-design-altering observation; no pre-registered hypothesis, threshold, or "
        "routing rule was modified."
    ),
}
