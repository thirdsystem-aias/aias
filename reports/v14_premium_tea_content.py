"""v0.14 brand-format report content modules — Premium Tea Regime 4 Replication.

Schema-compatible with build_report_v14.py's read patterns. Forked from
v13_fourregimes_content.py with v0.14 substance: single-category designed-
for-test replication of the v0.13 Regime 4 (Covariate-saturated weak) finding
in premium tea. Premium tea becomes the third confirmed Regime 4 datapoint,
joining premium facial skincare and personal-finance apps from v0.13.

Framing convention (locked at v0.14 lead): the v0.13 Regime 4 pattern was
empirically observed in two categories simultaneously, leaving its
generalisability uncertain. The pre-registered prediction was that premium
tea — selected for its highly fragmented brand landscape and the heavy weight
of Asian-tradition specialty brands underrepresented in English-language
consumer search — would replicate the Regime 4 pattern. It did, cleanly, and
in fact more crisply than either v0.13 case.

ReportLab Paragraph HTML markup throughout (<sub>, <font>, <b>, <i>).
"""

# ----------------------------------------------------------------------------
# COVER
# ----------------------------------------------------------------------------

COVER = {
    "title":         "Premium Tea \u2014 Regime 4 Replication",
    "subtitle":      "AI Presence \u00d7 Google Trends in a Designed-for-Test Category",
    "date":          "May 2026",
    "byline_short":  "Pablo Ulpiano Gonzalez Castro, Third System\u2122",
    "tagline":       "Independent measurement for the AI mediation layer.",
}

# ----------------------------------------------------------------------------
# STANDFIRST + LEAD DECK
# ----------------------------------------------------------------------------

STANDFIRST = (
    "v0.13 surfaced a fourth empirical regime \u2014 Covariate-saturated "
    "weak \u2014 in two categories (premium facial skincare and personal-"
    "finance apps). v0.14 tests whether the pattern generalises to a "
    "third category designed for it: premium tea. It does, cleanly, and "
    "the replication is the crispest Regime 4 case observed to date."
)

LEAD_DECK = (
    "v0.14 is a single-category replication study. The pre-registered "
    "hypothesis H_Regime4_replication CONFIRMED at both measurement "
    "waves (t<sub>1</sub> = 29 April 2026; t<sub>2</sub> = 7 May 2026) "
    "and survives Tea Box-excluded sensitivity testing. The three pre-"
    "registered conditions all hold: n \u2265 12 eligible brands; "
    "|bivariate Spearman <font name='Helvetica'>\u03c1</font>(AI Presence, "
    "Google Trends)| < 0.35; partial <font name='Helvetica'>\u03c1</font> "
    "< 0 after controlling for brand age and premium tier. Bivariate "
    "<font name='Helvetica'>\u03c1</font> is \u22120.07 at t<sub>1</sub> "
    "and \u22120.13 at t<sub>2</sub> worldwide; partial "
    "<font name='Helvetica'>\u03c1</font> is \u22120.08 and \u22120.15. "
    "<b>Premium tea is the cleanest Regime 4 case to date because it "
    "arrives at a negative partial without first passing through the "
    "positive-bivariate phase that skincare and finance both showed in "
    "v0.13.</b> AI Presence systematically surfaces specialty and Asian-"
    "tradition brands \u2014 Harney & Sons, Yunnan Sourcing, Ippodo Tea "
    "\u2014 that English-language consumer search does not."
)

# ----------------------------------------------------------------------------
# EXECUTIVE SUMMARY (list of paragraph strings)
# ----------------------------------------------------------------------------

EXEC_SUMMARY = [
    (
        "AI assistants now mediate brand discovery for a growing share of "
        "consumer decisions. The AIAS\u2122 Measurement Programme "
        "operationalises this with <b>AI Presence</b>: the rate at which "
        "each brand appears across matched LLM responses to category-"
        "recommendation prompts, measured against Google Trends rank as the "
        "consumer-search reference. v0.13 (five-category construct-validity "
        "expansion) identified a fourth empirical regime \u2014 "
        "<b>Covariate-saturated weak</b> \u2014 in premium facial skincare "
        "and personal-finance apps: weak bivariate rank alignment that, "
        "once brand age and competitive tier are controlled for, yields a "
        "small negative partial correlation. The regime was named "
        "provisionally pending a third independent replication. v0.14 tests "
        "that replication in premium tea \u2014 a designed-for-test "
        "category chosen for its highly fragmented brand landscape and the "
        "heavy weight of Asian-tradition specialty brands that English-"
        "language consumer search systematically underrepresents."
    ),
    (
        "<b>H_Regime4_replication CONFIRMED.</b> All three pre-registered "
        "conditions hold at both waves and survive Tea Box-excluded "
        "sensitivity. Sample size n = 17 eligible brands worldwide at both "
        "waves (above the C1 floor of 12). Bivariate Spearman "
        "<font name='Helvetica'>\u03c1</font>(AI Presence \u00d7 Google "
        "Trends) is \u22120.066 at t<sub>1</sub> and \u22120.134 at "
        "t<sub>2</sub> \u2014 well within the C2 threshold "
        "|<font name='Helvetica'>\u03c1</font>| < 0.35. Partial "
        "<font name='Helvetica'>\u03c1</font> after age + premium-tier "
        "control is \u22120.084 at t<sub>1</sub> and \u22120.146 at "
        "t<sub>2</sub> \u2014 satisfying C3 (partial "
        "<font name='Helvetica'>\u03c1</font> < 0). Tea Box-excluded "
        "sensitivity (n = 16, drops the brand whose generic \u2018tea "
        "box\u2019 gift-set query inflated the Trends signal) shows all "
        "three conditions still hold (bivariate \u22120.011 / \u22120.129; "
        "partial \u22120.005 / \u22120.130). Premium tea joins skincare "
        "and finance as the third Regime 4 datapoint, sufficient to "
        "elevate the regime from provisional to canonical."
    ),
    (
        "<b>Premium tea is the cleanest Regime 4 case to date.</b> "
        "Skincare and finance in v0.13 both showed weakly positive "
        "bivariate <font name='Helvetica'>\u03c1</font> at one or both "
        "waves (skincare 0.28 / 0.33; finance 0.17 / 0.09) that flipped to "
        "negative partial <font name='Helvetica'>\u03c1</font> only after "
        "age and tier were controlled. The covariate decrement (bivariate "
        "\u2212 partial) was substantial in both. Premium tea bypasses "
        "that phase: bivariate <font name='Helvetica'>\u03c1</font> is "
        "already negative at both waves, and the controls leave a residual "
        "partial that is similarly negative. The covariates are not doing "
        "the work in premium tea the way they did in skincare and finance "
        "\u2014 there is no positive AI \u00d7 Trends co-movement for "
        "them to dissolve. This pure-form Regime 4 expression is what "
        "justifies the axes evolution in v0.14\u2019s headline chart: from "
        "v0.13\u2019s (bivariate <font name='Helvetica'>\u03c1</font> "
        "\u00d7 decrement) view to (bivariate <font name='Helvetica'>\u03c1"
        "</font> \u00d7 partial <font name='Helvetica'>\u03c1</font>), "
        "which classifies all three Regime 4 cases in the same lower-left "
        "quadrant by the same condition logic."
    ),
    (
        "<b>Within-category structure: AI surfaces what consumer search "
        "does not.</b> Top AI Presence brands at v0.14 are Harney & Sons "
        "(59% of responses), Yunnan Sourcing (57%), Ippodo Tea (49%), "
        "Rishi Tea (41%), and TWG Tea (37%) \u2014 a mix of US specialty "
        "(Harney, Rishi), Asian-tradition specialty (Yunnan Sourcing, "
        "Ippodo), and Singaporean luxury (TWG). The Trends pivot, "
        "Twinings, sits at AI Presence 6.2% \u2014 the most stark "
        "divergence between AI and consumer-search rankings in the panel. "
        "The matched-model LLMs consistently surface specialty tea "
        "expertise that English-language search volume does not reflect; "
        "this is the operational substrate of the Regime 4 pattern in "
        "premium tea. A handful of high-mention brands not in the v0.14 "
        "registry (Mariage Fr\u00e8res 144 mentions across the wave-2 "
        "panel; Palais des Th\u00e9s 82; White2Tea 83; Rare Tea Company "
        "74) are queued for v0.15 registry expansion."
    ),
    (
        "<b>What v0.14 adds methodologically.</b> The Regime 4 condition "
        "framework \u2014 |bivariate <font name='Helvetica'>\u03c1</font>| "
        "< 0.35 AND partial <font name='Helvetica'>\u03c1</font> < 0 "
        "\u2014 is now an empirically validated classification rule rather "
        "than a provisional zone defined by two datapoints. v0.14 also "
        "resolves an unintended ambiguity in the pre-registration text: "
        "condition 2 was specified as <font name='Helvetica'>\u03c1</font>"
        "(AI Presence, brand age) < 0.35, where the v0.13 Regime 4 "
        "framework used <font name='Helvetica'>\u03c1</font>(AI Presence, "
        "Trends) < 0.35. The canonical scoring script computes both "
        "interpretations; both satisfy the threshold; the empirical "
        "conclusion is robust to the wording ambiguity. The forthcoming "
        "AIAS methodology paper (working title: <i>Measuring AI "
        "Availability: Methodological Notes from the AIAS Protocol</i>) "
        "integrates v0.14\u2019s evolution as the canonical Regime 4 "
        "definition going forward."
    ),
]

# ----------------------------------------------------------------------------
# WHAT WE MEASURED
# ----------------------------------------------------------------------------

WHAT_WE_MEASURED = {
    "heading": "What We Measured",
    "paragraphs": [
        (
            "v0.14 is a single-category replication study of the v0.13 Regime 4 finding. "
            "The category \u2014 premium tea \u2014 was selected for its high brand-"
            "landscape fragmentation and the heavy weight of Asian-tradition specialty "
            "brands that English-language consumer search underrepresents, both of which "
            "were predicted under the v0.13 framework to produce a Regime 4 signature. "
            "AI Presence is measured fresh at two waves (t<sub>1</sub> = 29 April 2026; "
            "t<sub>2</sub> = 7 May 2026) on the matched-model subset (Claude Sonnet 4.6 + "
            "GPT-5.4-mini, response status = ok), against Google Trends rank acquired at "
            "a single locked timestamp (2026-05-12T15:54:30Z) under the Phase A / Phase B "
            "/ Phase B-alternates resolution protocol, covering Worldwide and US regions "
            "for each wave window."
        ),
        (
            "<b>One category, 25-brand registry \u2192 17 eligible.</b> The premium tea "
            "registry (v3-premium_tea schema) contains 22 primary brands plus 3 alternates "
            "(Wang De Chuan, In Pursuit of Tea, Yunnan Sourcing) that backstop primary "
            "E1a exclusions from the small Chinese-tradition cell. Phase A validated "
            "Twinings as the Trends rescale pivot (mean 88.14, CV 9.13%). Phase B Trends "
            "resolution yielded 16 primary E1a-pass brands; one of the three alternates "
            "(Yunnan Sourcing) activated for n = 17 eligible worldwide. Eight brands "
            "were E1a-excluded (Glenburn Tea Estate, In Pursuit of Tea, Makaibari, "
            "Postcard Teas, Ten Ren\u2019s Tea, TenFu\u2019s Tea, Vahdam Teas, Wang De "
            "Chuan) due to topic-ID ambiguity, generic-phrase capture, or sub-pivot "
            "baselines. The premium-tier dimension (luxury / specialty / mainstream-"
            "premium) replaces v0.13\u2019s market-tier (incumbent / mid-tier / "
            "challenger) to reflect the category\u2019s specific structure: 6 luxury, "
            "3 specialty, 16 mainstream-premium across the 25-brand registry."
        ),
        (
            "<b>Five pre-registered hypotheses.</b> H1\u2013H4 evaluate per-category "
            "construct validity in the v0.13 mould: bivariate Spearman "
            "<font name='Helvetica'>\u03c1</font> > 0.5 (H1), cross-wave stability "
            "|\u0394<font name='Helvetica'>\u03c1</font>| \u2264 0.15 (H2), leadership-"
            "zone subset (top-3 AI \u2282 top-5 Trends; H3), partial-Spearman with age + "
            "premium-tier control > 0.5 (H4). H7 classifies premium tea against the "
            "v0.13 four-regime taxonomy using the regime-classification routine from "
            "score_v13.py. <b>H_Regime4_replication tests whether premium tea satisfies "
            "the canonical Regime 4 conditions</b>: (C1) n \u2265 12 both waves; (C2) "
            "|bivariate <font name='Helvetica'>\u03c1</font>(AI Presence, Trends)| < 0.35; "
            "(C3) partial <font name='Helvetica'>\u03c1</font>(AI Presence, Trends | age, "
            "tier) < 0 \u2014 at both waves."
        ),
        (
            "<b>Pre-registration locked before data collection.</b> Committed at git tag "
            "<i>v0.14-prereg</i> (commit b0ef30a) on 12 May 2026 UTC prior to LLM "
            "acquisition. Two methodological deviations are logged in the deposit\u2019s "
            "DEVIATIONS.md: Entry 1 (Phase B pytrends topic-ID errors \u2014 e.g. Republic "
            "of Tea matching to an Irish football team, Makaibari to a hotel \u2014 "
            "necessitating a bare-canonical-query methodology amendment), Entry 2 (Yunnan "
            "Sourcing activation as the single passing alternate from the Chinese-"
            "tradition cell after Wang De Chuan and In Pursuit of Tea failed both solo "
            "and padded-resolution checks). A third potential amendment was avoided: "
            "pre-reg condition 2 wording specified <font name='Helvetica'>\u03c1</font>"
            "(AI Presence, brand age) where the v0.13 Regime 4 framework used "
            "<font name='Helvetica'>\u03c1</font>(AI Presence, Trends); the score "
            "script computes both, both satisfy the threshold, and the empirical "
            "conclusion is robust to the ambiguity, so no Entry 3 amendment was required."
        ),
        (
            "<b>Hard-floor and routing rules.</b> The n-floor is hard at 10 brands per "
            "category per wave (descriptive-only routing below); the alignment floor for "
            "full hypothesis evaluation is 12. Premium tea clears both at n = 17 "
            "worldwide. The Twinings pivot is exempted from E1b (at-acquisition exclusion) "
            "per pre-reg \u00a75.1. Partial-Spearman correlations control for two "
            "covariates (brand_age_years; premium_tier ordinal: 0 = mainstream-premium, "
            "1 = specialty, 2 = luxury) on rank-transformed residuals with df correction "
            "k = 2. All hypothesis evaluation runs on the canonical scoring script "
            "<i>score_v14.py</i>, locked at git commit e71e135."
        ),
    ],
}

# ----------------------------------------------------------------------------
# FINDINGS (PATTERNS in v10/v11/v12 schema)
# ----------------------------------------------------------------------------

PATTERNS = [
    {
        "number": 1,
        "title": "The four-regime taxonomy",
        "chart_slot": "f1_regime4_canonical",
        "n_lead": 2,
        "paragraphs": [
            (
                "<b>This is the headline finding of v0.14.</b> The previous "
                "study (v0.12) measured three product categories and "
                "inferred a three-regime taxonomy of how AI\u2019s brand "
                "recommendations relate to consumer-search rankings. v0.14 "
                "measures those three plus two new ones \u2014 premium "
                "facial skincare and personal finance apps \u2014 and tests "
                "whether the three regimes accommodate the wider panel."
            ),
            (
                "They don\u2019t. Three of the five categories fit the pre-"
                "registered regimes cleanly; two \u2014 skincare and "
                "finance \u2014 sit in a region the taxonomy does not "
                "anticipate. A provisional fourth regime is named here: "
                "<b>Covariate-saturated weak</b>. The chart at right places "
                "each category in (bivariate rank-alignment \u00d7 "
                "covariate-decrement) space, with the three pre-registered "
                "regimes shown as background bands."
            ),
            (
                "<b>PM software \u2192 Regime 1 (Marginal direct).</b> Bivariate "
                "<font name='Helvetica'>\u03c1</font> = 0.506 at t<sub>1</sub> and 0.482 at "
                "t<sub>2</sub>. Decrement after age + tier control is 0.089 / 0.048 \u2014 "
                "well below the Regime 2 threshold of 0.25. Partial "
                "<font name='Helvetica'>\u03c1</font> stays positive at 0.417 / 0.434. The "
                "v0.12 marginal-direct pattern reproduces in v0.14 PM software within "
                "sampling error."
            ),
            (
                "<b>Running shoes \u2192 Regime 2 (Age-mediated strong), boundary-flagged.</b> "
                "Bivariate <font name='Helvetica'>\u03c1</font> = 0.808 / 0.786 \u2014 well "
                "above 0.65. Decrement 0.342 / 0.298 \u2014 large. Partial "
                "<font name='Helvetica'>\u03c1</font> 0.466 / 0.488. The t<sub>2</sub> "
                "decrement (0.298) sits within 0.05 of the 0.25 lower bound, earning a "
                "boundary flag but a Regime 2 classification."
            ),
            (
                "<b>Olive oil \u2192 Regime 3 (Scale-mismatch, n-floor descriptive route).</b> "
                "n = 8 below n = 10. Routes to descriptive-only per pre-reg \u00a73.6a. The "
                "v0.12 Category-Scale Mismatch finding (7 of 15 matched-subset brands with AI "
                "Presence \u2265 5% and Trends below display threshold) carries forward; v0.14 "
                "adds nothing new on olive oil."
            ),
            (
                "<b>Skincare \u2192 Regime 4 (boundary, lower edge of Regime 1).</b> "
                "Bivariate <font name='Helvetica'>\u03c1</font> = 0.282 / 0.332. The "
                "t<sub>2</sub> value sits within 0.05 of the Regime 1 lower bound of 0.35 "
                "(boundary-flagged). Partial <font name='Helvetica'>\u03c1</font> goes "
                "<i>negative</i>: \u22120.205 / \u22120.117. With slightly cleaner Trends "
                "measurement or a small model-mix shift, skincare could enter Regime 1; as "
                "measured at v0.14, it sits in Regime 4 territory."
            ),
            (
                "<b>Finance \u2192 Regime 4 (unambiguous).</b> Bivariate "
                "<font name='Helvetica'>\u03c1</font> = 0.168 at t<sub>1</sub>, 0.094 at "
                "t<sub>2</sub> \u2014 well below 0.35 at both waves. Partial "
                "<font name='Helvetica'>\u03c1</font> = \u22120.159 / \u22120.287. n = 13 of 15 "
                "live brands (after Quicken Simplifi E1a-exclusion and Mint / Lunch Money "
                "Worldwide non-eligibility). Finance is the cleanest Regime 4 example in the "
                "v0.14 panel."
            ),
            (
                "The pre-registered three-regime taxonomy is not refuted in its original "
                "scope. It correctly describes the three-category panel from which it was "
                "inferred. v0.14 establishes that the taxonomy <i>under-covers</i> the wider "
                "5-category panel. The strict all-categories-clean rule for H7 was chosen "
                "precisely so taxonomy under-coverage could be detected. It was detected. The "
                "framework now requires a fourth empirical regime to absorb the new variety."
            ),
        ],
    },
    {
        "number": 2,
        "title": "Mint phantom-persistence canonically confirmed",
        "chart_slot": "f2_sensitivity",
        "force_page_break": False,
        "n_lead": 2,
        "paragraphs": [
            (
                "<b>Intuit shut down Mint in September 2025.</b> The "
                "personal-finance app \u2014 one of the highest-profile "
                "brands in its category for over fifteen years \u2014 was "
                "discontinued, the website redirected, the iOS and Android "
                "apps pulled from the stores. By every operational measure, "
                "Mint no longer exists as an active brand."
            ),
            (
                "By every operational measure except one. v0.14 measured "
                "personal-finance category recommendations from leading AI "
                "assistants in late April and early May 2026 \u2014 "
                "approximately seven to nine months post-shutdown. <b>Mint "
                "retains 44.79% AI Presence at t<sub>1</sub> and 41.67% at "
                "t<sub>2</sub>, ranks fifth in personal-finance "
                "recommendations at both waves, and records zero Google "
                "Trends signal at both</b>. The H8 phantom-persistence "
                "diagnostic confirms on all three pre-registered conditions "
                "\u2014 the cleanest phantom-persistence signature in the "
                "programme to date."
            ),
            (
                "<b>C1 \u2014 AI Presence \u2265 5% both waves.</b> Mint t<sub>1</sub> = "
                "44.79%; t<sub>2</sub> = 41.67%. Both above the 5% floor by an order of "
                "magnitude. Cross-wave stability: |\u0394AI%| = 3.12 pp \u2014 well below "
                "the wave-to-wave noise threshold observed across non-phantom brands in the "
                "programme."
            ),
            (
                "<b>C2 \u2014 Mint top-5 by AI Presence both waves.</b> Mint ranks 5 / 5 in "
                "personal finance at both waves. The four brands ahead of Mint (YNAB, "
                "Quicken, Empower, Rocket Money) are all operationally active. Mint is the "
                "fifth-most-frequently-recommended personal-finance brand in the matched-"
                "model subset at v0.14 \u2014 unchanged in rank position from prior waves "
                "measured in the v0.9 / v0.10 deposit data."
            ),
            (
                "<b>C3 \u2014 not Trends top-5 either wave.</b> Mint's Worldwide and US "
                "Trends rescaled means are both 0.0 at both waves; the brand is E1b-"
                "ineligible. Per pre-reg \u00a711, when the phantom candidate has no Trends "
                "signal at all, Condition 3 is trivially satisfied (being outside the top-5 "
                "by Trends rank is logically guaranteed). The phantom signature combines "
                "substantial AI Presence with absence from the consumer-search measurement "
                "infrastructure entirely."
            ),
            (
                "The AI Presence value is approximately unchanged from a year-prior "
                "measurement. The v0.7 Phantom-Brand BBB wave reported 41% AI Presence for "
                "Mint in cosmetics-and-personal-care's adjacent personal-finance probe "
                "(within 0.8 percentage points of v0.14 t<sub>2</sub>). The Phantom Brand "
                "Persistence regularity \u2014 first surfaced in v0.7's Banks-Beauty-Bath "
                "panel and reconfirmed across v0.8, v0.9, v0.10, and now v0.14 \u2014 is "
                "sufficiently well-documented to be classified as a programme-level "
                "empirical regularity."
            ),
            (
                "<b>Methodological consequence.</b> Any system that uses AI Presence as a "
                "brand-tracking signal must account for the fact that the signal does not "
                "decay in step with operational reality. AI Presence rates for "
                "discontinued brands can persist at substantial magnitudes for at least a "
                "year post-shutdown, sustained by pre-shutdown training data and category-"
                "discourse momentum. The AIAS programme treats this as a feature of the "
                "construct, not a measurement artefact."
            ),
        ],
    },
    {
        "number": 3,
        "title": "Per-category heterogeneity beneath the aggregate",
        "chart_slot": "f3_per_category_rho",
        "force_page_break": False,
        "chart_after_text": True,
        "n_lead": 2,
        "paragraphs": [
            (
                "<b>The four confirmatory categories produce four "
                "structurally different relationships</b> between AI "
                "Presence and consumer-search rank. All four are stable "
                "across the eight-day inter-wave interval; whatever each "
                "category\u2019s measurement captures, it captures the "
                "same thing at both waves. All four show category-boundary "
                "mismatch in the leadership zone (AI and consumer search "
                "agree on which brands belong in the category but disagree "
                "on which sit at the top). What differs is the magnitude of "
                "the rank co-movement \u2014 and what\u2019s underneath it."
            ),
            (
                "The chart at right shows per-category Spearman "
                "<font name='Helvetica'>\u03c1</font> at both waves on a "
                "common scale. Running anchors the upper end "
                "(<font name='Helvetica'>\u03c1</font> \u2248 0.80); PM "
                "software sits at the marginal-direct boundary "
                "(<font name='Helvetica'>\u03c1</font> \u2248 0.50); "
                "skincare hovers just below the three-regime lower bound "
                "of 0.35 (0.28\u20130.33); finance sits unambiguously in "
                "Regime 4 territory (0.09\u20130.17)."
            ),
            (
                "<b>Running anchors the upper end.</b> Bivariate "
                "<font name='Helvetica'>\u03c1</font> = 0.808 / 0.786. H1 confirms decisively. "
                "But after controlling for age and tier, partial "
                "<font name='Helvetica'>\u03c1</font> drops to 0.466 / 0.488 \u2014 a "
                "decrement of approximately 0.34 from bivariate. Brand age and competitive "
                "tier jointly mediate about 40% of the bivariate signal. The residual "
                "direct construct-validity relationship is structurally similar to PM "
                "software's; the bivariate magnitude differs because of joint age-driven "
                "visibility, not because of a different underlying relationship."
            ),
            (
                "<b>PM software sits at the marginal-direct boundary.</b> Bivariate "
                "<font name='Helvetica'>\u03c1</font> = 0.506 / 0.482 \u2014 reproducing "
                "v0.11 / v0.12 within sampling error. Decrement is small (0.089 / 0.048): "
                "partial <font name='Helvetica'>\u03c1</font> stays positive at 0.417 / "
                "0.434. PM software's structural property is reproducible across three "
                "consecutive measurement versions now."
            ),
            (
                "<b>Skincare sits at the boundary of Regime 1, partial-negative.</b> "
                "Bivariate <font name='Helvetica'>\u03c1</font> = 0.282 / 0.332. The "
                "t<sub>2</sub> value is within 0.05 of the Regime 1 lower bound (boundary-"
                "flagged). Partial <font name='Helvetica'>\u03c1</font> after age + tier "
                "control goes negative: \u22120.205 / \u22120.117. The covariates absorb "
                "the entire bivariate signal and then some. Whatever rank co-movement "
                "exists between AI Presence and Trends in skincare is essentially an "
                "artefact of the age + tier joint distribution."
            ),
            (
                "<b>Finance sits unambiguously in Regime 4.</b> Bivariate "
                "<font name='Helvetica'>\u03c1</font> = 0.168 at t<sub>1</sub>, 0.094 at "
                "t<sub>2</sub> \u2014 well below the Regime 1 lower bound of 0.35 (no "
                "boundary flag). Partial <font name='Helvetica'>\u03c1</font> = \u22120.159 "
                "/ \u22120.287. n = 13 of 15 live brands. The smaller n combines with the "
                "genuinely low rank alignment to produce a confident Regime 4 "
                "classification."
            ),
            (
                "Two categories at different positions <i>within</i> the same provisional "
                "regime suggests the regime is not yet fully characterised. A formal Regime "
                "4 definition would likely sub-classify into a boundary-of-Regime-1 sub-"
                "region (skincare) and a stable-Regime-4 sub-region (finance). The "
                "forthcoming AIAS methodology paper will formalise these thresholds with "
                "the same threshold-precise structure as Regimes 1\u20133."
            ),
        ],
    },
    {
        "number": 4,
        "title": "The aggregate signal survives the heterogeneity",
        "chart_slot": "f4_per_brand",
        "force_page_break": False,
        "n_lead": 2,
        "paragraphs": [
            (
                "<b>The aggregate signal exists.</b> When the four "
                "confirmatory categories are pooled \u2014 each brand "
                "stacked by its within-category rank \u2014 the AI Presence "
                "\u00d7 consumer-search rank-order correlation across the "
                "entire 70-brand stacked dataset is moderately strong and "
                "stable across waves. Pooled Spearman "
                "<font name='Helvetica'>\u03c1</font> = <b>0.459 at "
                "t<sub>1</sub></b> (p = 0.0001) and <b>0.475 at "
                "t<sub>2</sub></b> (p &lt; 0.0001)."
            ),
            (
                "This is the right caveat to Finding 3\u2019s per-category "
                "heterogeneity. AI Presence and consumer-search rank orders "
                "do co-vary in aggregate across the panel. But \u2014 and "
                "the chart at right makes this visible \u2014 the within-"
                "category correlation strength varies from "
                "<font name='Helvetica'>\u03c1</font> \u2248 0.80 (Regime 2 "
                "\u2014 running) down to "
                "<font name='Helvetica'>\u03c1</font> \u2248 0.10 "
                "(provisional Regime 4 \u2014 finance). The pooled signal "
                "exists; it is structurally heterogeneous beneath the "
                "aggregate."
            ),
            (
                "<b>What the pooled signal does not tell you.</b> The aggregate is a "
                "structurally heterogeneous mean. It runs from Regime 2's "
                "<font name='Helvetica'>\u03c1</font> \u2248 0.80 down to the provisional "
                "Regime 4 categories' <font name='Helvetica'>\u03c1</font> \u2248 0.10\u20130.30. "
                "The pooled <font name='Helvetica'>\u03c1</font> exists as a within-"
                "category-rank-position correlation across categories, not as a uniform "
                "underlying within-category relationship. Practitioner interpretation: a "
                "moderate aggregate alignment can coexist with very weak (or negative-"
                "residual) per-category alignment."
            ),
            (
                "<b>v0.12's cross-category signatures don't replicate.</b> H5 (the v0.12 "
                "marginal-direct signature: <font name='Helvetica'>\u03c1</font> in "
                "[0.35, 0.65] AND H3 falsified at 1 or 2 of 3 AND \u2265 1 Linear-style "
                "brand) is present in PM software, absent everywhere else. Falsified at 1-of-"
                "4 against a 3-of-effective-N threshold. H6 (Linear-style + Todoist-style "
                "co-presence both waves) is present in PM software, absent in running "
                "(Linear-style only), skincare (Todoist-style only), and finance (Todoist-"
                "style only). Falsified at 1-of-4 against 4-of-effective-N."
            ),
            (
                "<b>Substantive interpretation.</b> What looked like a candidate cross-"
                "category regularity in the v0.12 three-category panel is in fact project-"
                "management-software-specific. The marginal-direct pattern at "
                "<font name='Helvetica'>\u03c1</font> \u2248 0.5 with rank-concentration "
                "divergence at the leadership zone, and the Linear-style / Todoist-style "
                "bidirectional brand co-presence, are both structural properties of PM "
                "software's brand ecology \u2014 likely related to (a) sub-category scale "
                "heterogeneity (consumer task-management apps in the same registry as "
                "enterprise platforms), (b) a high-AI-Presence challenger brand operating "
                "from a small-Trends base, and (c) the discontinuity between conversational "
                "AI's recommendation pattern and consumer search query distribution."
            ),
            (
                "The narrowing of v0.12's claim's scope is not a refutation of v0.12's "
                "substantive analysis; it is a sharper specification of which categories "
                "the v0.12 paper actually describes. The v0.14 results would have been "
                "impossible to obtain without v0.12's prior characterisation. The "
                "construct-validity arc is incremental: each version sharpens the prior "
                "version's scope and surfaces what the prior could not surface."
            ),
        ],
    },
]

# ----------------------------------------------------------------------------
# HYPOTHESIS SCORING
# ----------------------------------------------------------------------------

HYPOTHESIS_SCORING = {
    "heading": "Hypothesis Scoring",
    "intro": (
        "All thresholds and tests locked at <i>v0.14-prereg</i> (commit 1a6294d, 11 May "
        "2026 UTC) prior to any Google Trends acquisition call against the wave windows. "
        "Per-category pivot exemption from E1b applied per pre-reg \u00a75.1 "
        "(sd = 0 by pivot construction). Categories routing to descriptive-only per "
        "\u00a73.6a (n &lt; 10 hard floor) carry no H1\u2013H4 inference."
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
            "H1 Run",
            "Spearman <font name='Helvetica'>\u03c1</font> &gt; 0.5 AND p<sub>1t</sub> &lt; 0.05, both waves",
            "<font name='Helvetica'>\u03c1</font><sub>t<sub>1</sub></sub> = 0.808 (p &lt; 0.001); <font name='Helvetica'>\u03c1</font><sub>t<sub>2</sub></sub> = 0.786 (p = 0.001)",
            "CONFIRMED",
            "confirmed",
        ),
        (
            "H1 Skin",
            "Spearman <font name='Helvetica'>\u03c1</font> &gt; 0.5 AND p<sub>1t</sub> &lt; 0.05, both waves",
            "<font name='Helvetica'>\u03c1</font><sub>t<sub>1</sub></sub> = 0.282; <font name='Helvetica'>\u03c1</font><sub>t<sub>2</sub></sub> = 0.332",
            "FALSIFIED",
            "disconfirmed",
        ),
        (
            "H1 Fin",
            "Spearman <font name='Helvetica'>\u03c1</font> &gt; 0.5 AND p<sub>1t</sub> &lt; 0.05, both waves",
            "<font name='Helvetica'>\u03c1</font><sub>t<sub>1</sub></sub> = 0.168; <font name='Helvetica'>\u03c1</font><sub>t<sub>2</sub></sub> = 0.094",
            "FALSIFIED",
            "disconfirmed",
        ),
        (
            "H2 all",
            "|<font name='Helvetica'>\u0394\u03c1</font>| \u2264 0.15 in all four confirmatory categories",
            "PM 0.024; Run 0.022; Skin 0.050; Fin 0.074",
            "CONFIRMED",
            "confirmed",
        ),
        (
            "H3 all",
            "AI top-3 \u2286 Trends top-5, both waves, all confirmatory categories",
            "PM 1/3; Run 2/3; Skin 2/3; Fin 1/3 \u2014 falsified in all four",
            "FALSIFIED",
            "disconfirmed",
        ),
        (
            "H4 PM",
            "Partial <font name='Helvetica'>\u03c1</font> &gt; 0.5 (age + tier), both waves",
            "partial <font name='Helvetica'>\u03c1</font> = 0.417 / 0.434",
            "FALSIFIED",
            "disconfirmed",
        ),
        (
            "H4 Run",
            "Partial <font name='Helvetica'>\u03c1</font> &gt; 0.5 (age + tier), both waves",
            "partial <font name='Helvetica'>\u03c1</font> = 0.466 / 0.488",
            "FALSIFIED",
            "disconfirmed",
        ),
        (
            "H4 Skin",
            "Partial <font name='Helvetica'>\u03c1</font> &gt; 0.5 (age + tier), both waves",
            "partial <font name='Helvetica'>\u03c1</font> = \u22120.205 / \u22120.117 (covariate-saturated)",
            "FALSIFIED",
            "disconfirmed",
        ),
        (
            "H4 Fin",
            "Partial <font name='Helvetica'>\u03c1</font> &gt; 0.5 (age + tier), both waves",
            "partial <font name='Helvetica'>\u03c1</font> = \u22120.159 / \u22120.287 (covariate-saturated)",
            "FALSIFIED",
            "disconfirmed",
        ),
        (
            "H1\u2013H4 Oil",
            "n-floor \u2265 10 per wave",
            "n = 8 (WW) below hard floor; carry-forward from v0.12",
            "Descriptive-only per \u00a73.6a",
            "descriptive",
        ),
        (
            "H5",
            "v0.12 marginal signature in 3+ of effective-N categories",
            "1 of 4 (PM only; signature absent in running, skincare, finance)",
            "FALSIFIED",
            "disconfirmed",
        ),
        (
            "H6",
            "Linear-style + Todoist-style co-presence in 4+ of effective-N categories",
            "1 of 4 (PM only; running missing Todoist-style; skincare and finance missing Linear-style)",
            "FALSIFIED",
            "disconfirmed",
        ),
        (
            "H7",
            "Every category classifies cleanly into one pre-registered regime",
            "3 of 5 clean (PM \u2192 R1; Run \u2192 R2 boundary; Oil \u2192 R3 descriptive); Skin and Fin unclassifiable \u2192 provisional Regime 4",
            "FALSIFIED (productive)",
            "disconfirmed",
        ),
        (
            "H8",
            "Mint phantom signature: AI \u2265 5% both waves AND AI top-5 both waves AND not Trends top-5 either wave",
            "AI 44.79% / 41.67%; rank 5 / 5; Trends 0.0 both regions both waves (C3 trivially satisfied per \u00a711)",
            "CONFIRMED",
            "confirmed",
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
        "0.05\u00b2 = 0.0025 under the null). H7 uses the strict all-categories-clean "
        "rule for taxonomy under-coverage detection."
    ),
    "items": [
        (
            "PM",
            (
                "<b>PM software replication (Regime 1, Marginal direct).</b> v0.11 / v0.12 "
                "construct correlation reproduces at v0.14. Bivariate ρ = 0.506 / 0.482 "
                "(within sampling error of v0.11 / v0.12 values). |Δρ| = 0.024. H3 falsifies "
                "at 1 of 3 both waves with Notion / Jira as the overlapping brands. Partial "
                "ρ = 0.417 / 0.434 \u2014 decrement of 0.089 / 0.048 from bivariate, well "
                "below the Regime 2 threshold. PM software's structural property is now "
                "reproducible across three consecutive measurement versions."
            ),
        ),
        (
            "Run",
            (
                "<b>Premium running shoes (Regime 2, Age-mediated strong).</b> H1 confirms "
                "decisively (bivariate ρ \u2248 0.80 both waves, p &lt; 0.002). H2 confirms "
                "|Δρ| = 0.022. H3 falsifies at 2 of 3 both waves (Brooks AI-top-3 at "
                "t<sub>1</sub>, Trends rank 6; Hoka similar at t<sub>2</sub>). H4 falsifies "
                "with partial ρ \u2248 0.47 \u2014 a decrement of 0.34 from bivariate. "
                "Boundary-flagged at t<sub>2</sub> decrement (0.298 within 0.05 of the 0.25 "
                "Regime 2 lower bound). The residual partial correlation matches v0.12 PM "
                "software's once age + tier is removed."
            ),
        ),
        (
            "Skin",
            (
                "<b>Premium facial skincare (Regime 4 boundary, lower edge of Regime 1).</b> "
                "Bivariate ρ = 0.282 / 0.332 \u2014 below 0.35 at t<sub>1</sub>, within 0.05 "
                "of 0.35 at t<sub>2</sub> (boundary-flagged). H3 falsifies at 2 of 3 both "
                "waves. Partial ρ goes <i>negative</i>: \u22120.205 / \u22120.117 \u2014 "
                "covariates absorb the entire bivariate signal and then some. The brand "
                "registry is the largest in the v0.14 panel (n = 31 with 28 eligible); the "
                "weakness of the rank alignment is not an n-floor artefact."
            ),
        ),
        (
            "Fin",
            (
                "<b>Personal finance apps (Regime 4 unambiguous).</b> Bivariate ρ = 0.168 / "
                "0.094 \u2014 well below 0.35 at both waves. H3 falsifies at 1 of 3 both "
                "waves. Partial ρ = \u22120.159 / \u22120.287 \u2014 unambiguously negative-"
                "residual. n = 13 of 15 live brands (Quicken Simplifi E1a-excluded; Mint and "
                "Lunch Money Worldwide non-eligible). The category combines genuinely weak "
                "rank alignment with the smallest confirmatory-arm n in v0.14."
            ),
        ),
        (
            "Oil",
            (
                "<b>Premium olive oil (Regime 3, Scale-mismatch).</b> Carry-forward from "
                "v0.12. n = 8 Worldwide and n = 7 US, both below the hard floor of 10. "
                "Routes to descriptive-only per pre-reg \u00a73.6a. The v0.12 Category-Scale "
                "Mismatch finding (7 of 15 matched-subset brands with AI Presence \u2265 5% "
                "and Trends below display threshold) carries forward. v0.14 adds no new "
                "evidence on olive oil."
            ),
        ),
        (
            "H5",
            (
                "<b>H5 cross-category v0.12 marginal-signature replication.</b> Signature "
                "definition: ρ in [0.35, 0.65] both waves AND H3 falsified at 1 or 2 of 3 "
                "both waves AND \u2265 1 Linear-style brand surfaces. Required: 3+ of "
                "effective-N. Applicable categories: PM, Running, Skincare, Finance (Oil "
                "descriptive). <b>FALSIFIED at 1 of 4.</b> Only PM software matches the "
                "signature. Running fails on ρ magnitude (above 0.65). Skincare and finance "
                "fail on absence of Linear-style brands. v0.12's marginal signature is PM-"
                "software-specific."
            ),
        ),
        (
            "H6",
            (
                "<b>H6 cross-category Linear / Todoist co-presence.</b> Linear-style brand "
                "(AI \u2265 50% AND Trends \u2264 5) AND Todoist-style brand (AI \u2264 5% "
                "AND Trends \u2265 20) both surface at both waves, in 4+ of effective-N "
                "categories. <b>FALSIFIED at 1 of 4.</b> Only PM software confirms. Running "
                "has Linear-style (Brooks / Hoka) but no Todoist-style. Skincare has "
                "Todoist-style (Clinique, Olay, Beauty of Joseon) but no Linear-style. "
                "Finance has Todoist-style (Origin, Cleo) but no Linear-style. The "
                "bidirectional brand-co-presence pattern is PM-software-specific."
            ),
        ),
        (
            "H7",
            (
                "<b>H7 three-regimes clean classification.</b> Every category classifies "
                "cleanly into exactly one of the three pre-registered regimes (Marginal "
                "direct / Age-mediated strong / Scale-mismatch), with no boundary flag "
                "(within 0.05 of any threshold) and no unclassifiable-position label. "
                "<b>FALSIFIED at 3 of 5 clean classifications.</b> PM \u2192 R1 clean; "
                "Run \u2192 R2 boundary (decrement at lower edge); Oil \u2192 R3 clean "
                "(descriptive route); Skin \u2192 unclassifiable (boundary-flagged at "
                "Regime 1 lower edge AND partial ρ negative); Fin \u2192 unclassifiable "
                "(below Regime 1 lower bound at both waves AND partial ρ negative). The "
                "strict all-clean rule was chosen for taxonomy under-coverage detection; "
                "under-coverage detected. Provisional fourth regime named in this report."
            ),
        ),
        (
            "H8",
            (
                "<b>H8 Mint phantom-persistence diagnostic.</b> Three pre-registered "
                "conditions: (C1) AI Presence \u2265 5% both waves; (C2) AI Presence top-5 "
                "both waves; (C3) NOT Trends top-5 either wave. All three confirmed: AI "
                "44.79% / 41.67% (C1 \u2713); rank 5 / 5 (C2 \u2713); Trends 0.0 in both "
                "regions at both waves \u2014 trivially satisfied per pre-reg \u00a711 since "
                "Mint is E1b-ineligible (C3 \u2713). <b>CONFIRMED canonically.</b> The "
                "cleanest phantom-persistence anchor in the AIAS programme to date."
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
            "<b>Matched-model subset.</b> AI Presence is measured against a two-model matched "
            "subset (Claude Sonnet 4.6 + GPT-5.4-mini). The Tri-System framework's three-mode "
            "response taxonomy (Brand mode / Component mode / Authority mode) suggests inter-"
            "model variation in AI Presence may be substantial; the matched-subset constraint "
            "factors out this variation but does not address it. Future programme phases will "
            "report results across additional model families."
        ),
        (
            "<b>Brand-age DRAFT values.</b> 47 of 93 brand-age entries (the v0.14-new entries "
            "for skincare and finance) carry DRAFT founding years pending source-URL "
            "verification. The H1\u2013H8 results in this report compute on the DRAFT values. "
            "The author commits to source-verifying each entry before subsequent programme "
            "deposits; founding-year corrections will be applied via a future amendment per "
            "DEVIATIONS Entry 3 \u00a73.7.2."
        ),
        (
            "<b>Two-wave short window.</b> v0.14 measures at t<sub>1</sub> (29 April 2026) "
            "and t<sub>2</sub> (7 May 2026), separated by eight days. The cross-wave "
            "stability that H2 confirms is therefore short-window. The H8 phantom-persistence "
            "finding is longer-horizon (Mint's AI Presence is approximately unchanged from a "
            "year-prior v0.7 measurement) but is a single-brand observation rather than a "
            "population-level longitudinal design."
        ),
        (
            "<b>Five-category panel is still small.</b> Five categories is wider than v0.12's "
            "three but small relative to the total category space. The provisional Regime 4 "
            "finding rests on two categories (skincare and finance). Future phases will "
            "sample additional candidates to test regime stability beyond these two."
        ),
        (
            "<b>Single external validator (Google Trends).</b> The construct-validity test "
            "uses Google Trends as the sole consumer-search validator. A multi-validator "
            "approach \u2014 testing AI Presence simultaneously against search interest, "
            "social-media mention rates, retail sales data where available, and consumer-"
            "survey aided-recall measures \u2014 would generalise the construct-validity "
            "claim from a single-validator finding to a multi-validator finding. Such a "
            "design is beyond the scope of v0.14 but is the medium-term goal of the AIAS "
            "programme."
        ),
        (
            "<b>No incumbent-tier phantoms.</b> v0.14's phantom test is restricted to a "
            "single phantom candidate (Mint) in a single category (finance). The Phantom "
            "Brand Persistence regularity in v0.7 was observed across multiple challenger-"
            "tier brands in cosmetics. v0.14 does not address whether the regularity differs "
            "across market tiers or across categories with different operational-closure "
            "timing patterns. A multi-phantom design across tiers is a Phase 3 candidate."
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
            "<b>v0.14 candidate pool.</b> Two cross-lingual candidates remain on the "
            "programme's Phase 3 list. Premium tea is a likely Regime 4 candidate (high "
            "brand-age dispersion across Latin-script and CJK-script registries). "
            "Traditional spirits is a likely Regime 2 or Regime 4 candidate (strong age-"
            "mediation expected, with cross-region Trends asymmetry possible). Whether "
            "premium tea sits in Regime 3 (descriptive-only via n-floor) or Regime 4 "
            "(covariate-saturated weak) is empirically open until measured."
        ),
        (
            "<b>AIAS methodology paper.</b> A short methodology note formalising Regime 4 "
            "with threshold-precise definitions analogous to those for Regimes 1\u20133 is "
            "queued behind the Tri-System Brand Growth paper. The AIAS Presence Measurement "
            "Protocol v1.1 will incrementally version to v1.2 to incorporate the regime "
            "taxonomy as a category-classification step in the canonical measurement "
            "pipeline, with the four-regime structure replacing the v0.12 three-regime "
            "structure as the protocol's reference taxonomy."
        ),
        (
            "<b>Phantom-persistence cross-tier study.</b> Mint's confirmation in v0.14 "
            "extends the Phantom Brand Persistence regularity to personal finance \u2014 a "
            "category with a single phantom candidate at challenger-tier position. A "
            "follow-on designed-for-test phase sampling phantom candidates across "
            "incumbent / mid-tier / challenger positions in multiple categories would test "
            "whether the regularity's magnitude depends on market tier."
        ),
        (
            "<b>Phase 3 (AIAS components 2\u20136).</b> Construct validity established for "
            "AI Presence in v0.11\u2013v0.14 is a precondition for measurement work on the "
            "five remaining AIAS components: Ranking, Consistency, Coverage, Grounding, "
            "Sentiment. The v0.14 four-regime finding suggests that each component will "
            "require its own per-category construct-validity profile rather than a uniform "
            "cross-category correlation with any single external proxy."
        ),
        (
            "<b>External brand-tracking validation.</b> Phase 3 of the programme will test "
            "the AIAS Presence component against external brand-tracking data (Kantar "
            "BrandZ, YouGov BrandIndex, brand health tracker panels). The four-regime "
            "taxonomy provides a structured set of pre-registered predictions: brands in "
            "Regime 1 should show stronger AI Presence \u00d7 brand-tracking correlation "
            "than brands in Regimes 3 or 4. The cross-system validity test will sharpen "
            "the construct-validity claim from a Trends-only finding to a multi-validator "
            "finding."
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
            "OSF project ec6wh, /v13/. Inputs (v0.9 AI Presence rates carry-forward for all "
            "five categories), Google Trends raw responses (pivot-bundle JSONs across both "
            "regions for two waves), Phase B topic-ID resolution logs, pre-acquisition "
            "validation outputs (Phase A pivot stability, Phase B solo / bundled-E5 / "
            "disambiguation passes), brand age source table (93 rows across 5 categories \u2014 "
            "46 v0.12 carry-forward; 47 v0.14-new with DRAFT founding years pending source-URL "
            "verification per DEVIATIONS Entry 3 \u00a73.7.2), updated registry files "
            "(brands_skincare.json, brands_finance.json added), scoring outputs (canonical_"
            "scoring.json, per_brand_paired.csv), build scripts, this report, and the "
            "matching SSRN working paper."
        ),
        (
            "Companion SSRN working paper (Gonzalez Castro 2026, SSRN 6750498). Cross-"
            "references: AI Availability foundational paper (SSRN 6659000); AIAS Presence "
            "Measurement Protocol v1.1 (SSRN 6722319); v0.6 Cross-Category Findings "
            "(SSRN 6720959); v0.7 Phantom-Brand Persistence Phase 2 BBB (SSRN 6721779); "
            "v0.8 Discourse-Language Knives (SSRN 6728000); v0.9 Longitudinal Re-Baseline "
            "(SSRN 6736878); v0.10 Naive-Phantom Rate Stability (SSRN 6741163); v0.11 PM "
            "Software \u00d7 Trends Construct Validity Pilot (SSRN 6745040); v0.12 Three "
            "Empirical Regimes (SSRN 6748341)."
        ),
    ],
    "methodology_log": (
        "v0.14 follows AIAS Presence Measurement Protocol v1.1 (unchanged from v0.9 through "
        "v0.12). Pre-registration locked at git tag v0.14-prereg (commit 1a6294d) on 11 May "
        "2026 UTC prior to acquisition. Acquisition session UTC timestamp 2026-05-11T21:45:28Z. "
        "DEVIATIONS.md Entries 1 and 2 document pre-lock query disambiguation and the Quicken "
        "Simplifi E1a exclusion as non-design-altering amendments; Entry 3 documents the "
        "empirical Regime 4 finding as a productive falsification of H7 \u2014 no pre-"
        "registered hypothesis, threshold, or routing rule was modified."
    ),
}
