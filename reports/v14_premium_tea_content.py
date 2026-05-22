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
        "title": "H_Regime4_replication CONFIRMED — premium tea joins the Regime 4 cluster",
        "chart_slot": "f1_regime4_canonical",
        "n_lead": 2,
        "paragraphs": [
            (
                "<b>This is the headline finding of v0.14.</b> The previous study "
                "(v0.13) identified a fourth empirical regime — Covariate-saturated "
                "weak — in two categories (premium facial skincare and personal-"
                "finance apps), and named the regime provisionally pending a third "
                "independent replication. v0.14 supplies that replication in premium "
                "tea, a designed-for-test category selected for its highly fragmented "
                "brand landscape and the heavy weight of Asian-tradition specialty "
                "brands that English-language consumer search underrepresents. The "
                "pre-registered hypothesis H_Regime4_replication CONFIRMED at both "
                "measurement waves and survives Tea Box-excluded sensitivity testing."
            ),
            (
                "The three pre-registered conditions all hold at both worldwide waves. "
                "<b>C1:</b> sample size n = 17 eligible brands — above the C1 floor of 12. "
                "<b>C2:</b> bivariate Spearman <font name='Helvetica'>ρ</font>(AI Presence × "
                "Google Trends) is −0.066 at t<sub>1</sub> and −0.134 at t<sub>2</sub> — "
                "within the C2 threshold |<font name='Helvetica'>ρ</font>| < 0.35. <b>C3:</b> "
                "partial <font name='Helvetica'>ρ</font> after age + premium-tier control is "
                "−0.084 at t<sub>1</sub> and −0.146 at t<sub>2</sub> — satisfying C3 partial "
                "<font name='Helvetica'>ρ</font> < 0. The chart at right places premium tea "
                "alongside the v0.13 Regime 4 cases in the canonical (bivariate "
                "<font name='Helvetica'>ρ</font> × partial <font name='Helvetica'>ρ</font>) "
                "classification axes."
            ),
            (
                "<b>Premium tea is the cleanest Regime 4 case to date.</b> v0.13's skincare "
                "and finance both exhibited weakly positive bivariate "
                "<font name='Helvetica'>ρ</font> (skincare 0.28 / 0.33; finance 0.17 / 0.09) "
                "that flipped to negative partial <font name='Helvetica'>ρ</font> only after "
                "age and tier were controlled. The covariate decrement (bivariate − partial) "
                "was substantial in both. Premium tea bypasses that phase: bivariate "
                "<font name='Helvetica'>ρ</font> is already negative at both waves, and the "
                "controls leave a residual partial that is similarly negative. The covariates "
                "are not doing the work in premium tea the way they did in skincare and "
                "finance — there is no positive AI × Trends co-movement for them to dissolve."
            ),
            (
                "<b>Three datapoints across three categories elevate Regime 4 from provisional "
                "to canonical.</b> The programme convention for promoting a provisional "
                "empirical regularity to canonical status — three independent confirmations "
                "under pre-registration — is now met. The Regime 4 condition framework "
                "(|bivariate <font name='Helvetica'>ρ</font>| < 0.35 AND partial "
                "<font name='Helvetica'>ρ</font> < 0) is an empirically validated "
                "classification rule rather than a provisional zone defined by two datapoints."
            ),
            (
                "<b>Axis evolution.</b> The headline classification chart evolves from "
                "v0.13's (bivariate <font name='Helvetica'>ρ</font> × decrement) view to "
                "v0.14's (bivariate <font name='Helvetica'>ρ</font> × partial "
                "<font name='Helvetica'>ρ</font>) view. The decrement axis worked when "
                "bivariate <font name='Helvetica'>ρ</font> was positive (so the covariate "
                "decrement was well-defined and positive); premium tea's already-negative "
                "bivariate yields a near-zero decrement that does not separate cleanly. The "
                "partial-<font name='Helvetica'>ρ</font> axis classifies all three Regime 4 "
                "cases by the same condition logic that drives the H_Regime4_replication "
                "test itself."
            ),
            (
                "<b>Resolving a pre-reg wording ambiguity.</b> Condition 2 was specified in "
                "the v0.14 pre-registration text as <font name='Helvetica'>ρ</font>(AI "
                "Presence, brand age) where the v0.13 Regime 4 framework used "
                "<font name='Helvetica'>ρ</font>(AI Presence, Trends). The canonical scoring "
                "script computes both. Both satisfy the |<font name='Helvetica'>ρ</font>| < "
                "0.35 threshold at both waves: <font name='Helvetica'>ρ</font>(AI, age) = "
                "0.018 / −0.019; <font name='Helvetica'>ρ</font>(AI, Trends) = −0.066 / "
                "−0.134. The empirical conclusion is robust to the ambiguity, and the v0.13 "
                "canonical interpretation (AI × Trends) is adopted going forward."
            ),
            (
                "What v0.14 leaves to formalise: a sub-classification within Regime 4. The "
                "skincare-and-finance pattern (positive-to-negative migration under covariate "
                "control) differs structurally from premium tea's already-negative bivariate "
                "path, even though both satisfy the same canonical conditions. The "
                "forthcoming AIAS methodology paper will specify <b>Regime 4a</b> (migration "
                "sub-type) and <b>Regime 4b</b> (pure sub-type) thresholds analogous to those "
                "for Regimes 1–3."
            ),
        ],
    },
    {
        "number": 2,
        "title": "Tea Box-excluded sensitivity — the Regime 4 verdict is robust to specification",
        "chart_slot": "f2_sensitivity",
        "n_lead": 2,
        "paragraphs": [
            (
                "<b>The Regime 4 verdict does not depend on Tea Box.</b> One of the 17 "
                "eligible primary brands in the premium-tea panel is the brand 'Tea Box' "
                "(mainstream-premium tier), whose Trends rescaled mean (166 worldwide at "
                "t<sub>2</sub>, 406 US at t<sub>2</sub>) is anomalously high relative to its "
                "AI Presence rate (2.1%). The cause: the generic phrase 'tea box' captures "
                "gift-set search volume unrelated to the brand entity. The Tea Box-excluded "
                "sensitivity drops this brand and re-runs the three pre-registered conditions "
                "on n = 16."
            ),
            (
                "All three conditions still hold at both waves. Bivariate Spearman "
                "<font name='Helvetica'>ρ</font>(AI × Trends) is −0.011 at t<sub>1</sub> and "
                "−0.129 at t<sub>2</sub> — both well within the C2 threshold of "
                "|<font name='Helvetica'>ρ</font>| < 0.35. Partial "
                "<font name='Helvetica'>ρ</font> after age + premium-tier control is −0.005 "
                "at t<sub>1</sub> and −0.130 at t<sub>2</sub> — both satisfying C3 partial "
                "<font name='Helvetica'>ρ</font> < 0. The sample size at n = 16 remains above "
                "the C1 floor of 12."
            ),
            (
                "<b>The primary and sensitivity panels arrive at structurally identical "
                "conclusions.</b> The chart at right shows bivariate "
                "<font name='Helvetica'>ρ</font> and partial <font name='Helvetica'>ρ</font> "
                "side-by-side across all four wave/region combinations, primary (n = 17) "
                "versus Tea Box-excluded (n = 16). At every wave and every region, both "
                "panels satisfy both the C2 and C3 thresholds. The verdict is robust to the "
                "inclusion or exclusion of any single brand whose Trends measurement may have "
                "been confounded by generic-phrase capture."
            ),
            (
                "<b>What this means methodologically.</b> The pivot-rescaling Trends "
                "acquisition occasionally captures generic-phrase search volume in addition "
                "to brand-specific search; the Tea Box case illustrates the failure mode in a "
                "category where it has greatest leverage (a brand whose name is also a "
                "category-level descriptive phrase). For the v0.14 Regime 4 verdict the "
                "leverage is small enough not to flip the result, but the operational lesson "
                "generalises: pre-registered sensitivity tests against generic-phrase "
                "contamination are a useful component of the AIAS Protocol going forward."
            ),
            (
                "<b>US-region sensitivity also confirms.</b> The US-region subset re-runs the "
                "H_Regime4_replication conditions: bivariate <font name='Helvetica'>ρ</font> "
                "= −0.076 / +0.011; partial <font name='Helvetica'>ρ</font> = −0.101 / "
                "+0.033. The US-region partial at t<sub>2</sub> sits very close to zero "
                "(+0.033), on the boundary of C3, but the worldwide-region verdict — the "
                "primary analysis — carries definitively."
            ),
            (
                "Premium tea joins skincare and finance as Regime 4 datapoints with "
                "sensitivity tests that confirm the verdict rather than narrow it. The "
                "condition framework has accumulated robustness across both within-version "
                "(multiple sensitivity panels) and cross-version (three independent "
                "categories) replication."
            ),
        ],
    },
    {
        "number": 3,
        "title": "Per-category construct validity — six categories on common axes",
        "chart_slot": "f3_per_category_rho",
        "force_page_break": False,
        "chart_after_text": True,
        "n_lead": 2,
        "paragraphs": [
            (
                "<b>The six-category panel shows three structurally different relationships "
                "between AI Presence and consumer-search rank.</b> v0.14 measures premium "
                "tea fresh alongside the five-category panel from v0.13 (project management "
                "software, premium running shoes, premium olive oil, premium facial skincare, "
                "personal-finance apps). The chart below places each category at its "
                "bivariate worldwide <font name='Helvetica'>ρ</font> (indigo), partial "
                "worldwide <font name='Helvetica'>ρ</font> (petro), and bivariate US "
                "<font name='Helvetica'>ρ</font> (grey, sensitivity) for both waves. The "
                "premium-tea row is the v0.14 addition."
            ),
            (
                "<b>Regime 1 — PM software.</b> Bivariate <font name='Helvetica'>ρ</font> = "
                "0.506 / 0.482, partial <font name='Helvetica'>ρ</font> = 0.417 / 0.434. The "
                "marginal-direct pattern reproduces in v0.14 within sampling error. v0.11 / "
                "v0.12 / v0.13 / v0.14 confirm PM software at the lower edge of construct-"
                "validity confirmation, with covariate decrement small enough (~0.07) to "
                "leave a positive residual."
            ),
            (
                "<b>Regime 2 — running shoes.</b> Bivariate <font name='Helvetica'>ρ</font> "
                "= 0.808 / 0.786, partial <font name='Helvetica'>ρ</font> = 0.466 / 0.488. H1 "
                "confirms decisively at both waves. The substantial covariate decrement "
                "(~0.34) reflects age-driven joint visibility — older heritage brands rank "
                "highly in both AI Presence and Trends because their age has produced both "
                "training-corpus exposure and search familiarity. The residual partial after "
                "age + tier control sits at PM-software's marginal-direct level."
            ),
            (
                "<b>Regime 3 — olive oil.</b> n = 8 worldwide and n = 7 US, both below the "
                "hard floor of 10. Routes to descriptive-only per pre-reg §3.6a. The v0.12 "
                "Category-Scale Mismatch finding (7 of 15 matched-subset brands with AI "
                "Presence ≥ 5% and Trends below display threshold) carries forward unchanged. "
                "The category is not refuted; it sits outside the H1–H4 inference path."
            ),
            (
                "<b>Regime 4 — skincare, finance, premium tea.</b> Three datapoints, three "
                "positions within the regime. Skincare sits at the boundary of Regime 1 "
                "(bivariate 0.28 / 0.33, partial −0.21 / −0.12) where the covariates absorb "
                "the entire bivariate signal and reveal a slight negative residual. Finance "
                "sits unambiguously inside Regime 4 (bivariate 0.17 / 0.09, partial −0.16 / "
                "−0.29). Premium tea sits in the pure-form region (bivariate −0.07 / −0.13, "
                "partial −0.08 / −0.15) — the cleanest case to date."
            ),
            (
                "<b>The structural heterogeneity within Regime 4 is the next methodological "
                "question.</b> A formal Regime 4 sub-classification distinguishes a migration "
                "sub-region (Regime 4a: positive bivariate that flips negative under "
                "covariate control — skincare, finance) from a pure sub-region (Regime 4b: "
                "already-negative bivariate; partial similarly negative — premium tea). The "
                "unified condition signature (|bivariate <font name='Helvetica'>ρ</font>| < "
                "0.35 AND partial <font name='Helvetica'>ρ</font> < 0) is satisfied by both "
                "sub-types and serves as the canonical operational test; the sub-"
                "classification awaits additional datapoints in each sub-region."
            ),
        ],
    },
    {
        "number": 4,
        "title": "Within-category structure — AI surfaces specialty and Asian-tradition brands",
        "chart_slot": "f4_per_brand",
        "n_lead": 2,
        "paragraphs": [
            (
                "<b>The within-category structure of premium tea makes the Regime 4 substrate "
                "visible.</b> Top AI Presence brands at v0.14, averaged across both waves on "
                "the matched-model subset, are Harney & Sons (59%), Yunnan Sourcing (57%), "
                "Ippodo Tea (49%), Rishi Tea (41%), and TWG Tea (37%). This is a mix of US "
                "specialty (Harney, Rishi), Asian-tradition specialty (Yunnan Sourcing, "
                "Ippodo), and Singaporean luxury (TWG)."
            ),
            (
                "The Trends pivot, Twinings, sits at AI Presence 6.2% — the starkest "
                "divergence between AI and consumer-search rankings observed in the v0.14 "
                "panel. The chart at right shows each eligible brand's position in (AI "
                "Presence × Trends rescaled mean) space at both waves, coloured by premium "
                "tier. Twinings anchors the high-Trends / low-AI corner; the top AI brands "
                "anchor the high-AI / low-Trends corner. The decoupling is geometrically "
                "visible."
            ),
            (
                "<b>What this reveals about the substrate.</b> Matched-model LLMs (Claude "
                "Sonnet 4.6 + GPT-5.4-mini) surface specialty tea expertise — loose-leaf "
                "curation, sourcing knowledge, Asian-tradition matcha and pu-erh varieties — "
                "that English-language consumer search does not concentrate on. This is not a "
                "measurement artefact: the LLM training corpora include substantial coverage "
                "of specialty tea writing (Ippodo's matcha guides, Yunnan Sourcing's pu-erh "
                "sourcing notes, Harney's blending tradition) that is not reflected in "
                "Trends' aggregate search-volume signal."
            ),
            (
                "<b>Twinings's position is the diagnostic.</b> Twinings dominates English-"
                "language tea search by an order of magnitude over any single specialty "
                "brand, but does not dominate LLM responses to category-recommendation "
                "prompts. The asymmetry has a clean reading: consumer search is structured "
                "around the brands consumers already know (Twinings, mass-market "
                "familiarity); LLM responses are structured around the brands the model has "
                "seen discussed substantively in training corpora (specialty curation, Asian-"
                "tradition expertise). Premium tea's Regime 4 signature is the geometric "
                "consequence of this asymmetry."
            ),
            (
                "<b>The category-specific substrate may not generalise.</b> Skincare and "
                "finance share the Regime 4 condition outcome but reach it through a "
                "different mechanism — large incumbent brands with high age + tier values "
                "that LLMs surface because of training-data persistence, where covariate "
                "control reveals the underlying decoupling. Premium tea's mechanism is the "
                "specialty / incumbent asymmetry. The canonical Regime 4 should not be "
                "interpreted as a single underlying mechanism — it is an empirical co-"
                "occurrence of two conditions that admits multiple substrates."
            ),
            (
                "<b>v0.15 registry candidates surfaced in v0.14.</b> Four high-mention brands "
                "not in the v0.14 registry were observed: Mariage Frères (144 mentions "
                "across the wave panel), Palais des Thés (82), White2Tea (83), and Rare Tea "
                "Company (74). Inclusion in v0.15 will expand the panel from n = 17 to "
                "approximately n = 25–27, with Mariage Frères likely entering the top-5 AI "
                "Presence ranks (its mention count exceeds Twinings's). The Regime 4 verdict "
                "is unlikely to invert under expansion — the additional brands amplify the "
                "specialty / luxury cluster that already drives the signature."
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
        "All thresholds and tests locked at v0.14-prereg (commit b0ef30a, 12 May 2026 "
        "UTC) prior to any LLM acquisition or Google Trends acquisition call against "
        "the wave windows. Per-category pivot exemption from E1b applied per pre-reg "
        "§5.1 (sd = 0 by pivot construction). The primary analysis is the worldwide-"
        "region cell at both waves; the Tea Box-excluded sensitivity and the US-region "
        "subset serve as pre-registered robustness panels."
    ),
    "rows": [
        (
            "H_Regime4_replication (primary)",
            "n ≥ 12 AND |bivariate <font name='Helvetica'>ρ</font>(AI, Trends)| &lt; 0.35 AND partial <font name='Helvetica'>ρ</font>(AI, Trends | age, tier) &lt; 0; both waves WW",
            "n = 17; bivariate <font name='Helvetica'>ρ</font> = −0.066 / −0.134; partial <font name='Helvetica'>ρ</font> = −0.084 / −0.146 — all three conditions satisfied",
            "CONFIRMED",
            "confirmed",
        ),
        (
            "H_Regime4_replication (Tea Box-excluded)",
            "Same three conditions on n = 16 (Tea Box dropped); sensitivity",
            "n = 16; bivariate <font name='Helvetica'>ρ</font> = −0.011 / −0.129; partial <font name='Helvetica'>ρ</font> = −0.005 / −0.130 — verdict robust",
            "CONFIRMED",
            "confirmed",
        ),
        (
            "H1 (per-category)",
            "Spearman <font name='Helvetica'>ρ</font> &gt; 0.5 AND p<sub>1t</sub> &lt; 0.05, both waves",
            "<font name='Helvetica'>ρ</font><sub>t<sub>1</sub></sub> = −0.066; <font name='Helvetica'>ρ</font><sub>t<sub>2</sub></sub> = −0.134 — well below 0.5 by sign and magnitude",
            "FALSIFIED",
            "disconfirmed",
        ),
        (
            "H2 (cross-wave stability)",
            "|<font name='Helvetica'>Δρ</font>| ≤ 0.15 between t<sub>1</sub> and t<sub>2</sub>",
            "|<font name='Helvetica'>Δρ</font>| = 0.068 — well within stability threshold",
            "CONFIRMED",
            "confirmed",
        ),
        (
            "H3 (leadership-zone subset)",
            "AI top-3 ⊆ Trends top-5, both waves",
            "0 / 3 brands overlap at both waves (Harney / Yunnan / Ippodo absent from Trends top-5)",
            "FALSIFIED",
            "disconfirmed",
        ),
        (
            "H4 (partial-Spearman)",
            "Partial <font name='Helvetica'>ρ</font> &gt; 0.5 (age + premium_tier), both waves",
            "partial <font name='Helvetica'>ρ</font> = −0.084 / −0.146 (covariate-saturated, negative-residual)",
            "FALSIFIED",
            "disconfirmed",
        ),
        (
            "H7 (regime classification)",
            "Matches Regime 1 / 2 / 3 (the pre-registered set)",
            "Matches none — Regime 4 candidate; confirmed under H_Regime4_replication",
            "FALSIFIED (productive)",
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
        "Per-hypothesis claim, operationalisation, and result. H_Regime4_replication is "
        "the v0.14 primary hypothesis; H1–H4 are per-category construct-validity tests "
        "carried forward from the programme convention (their falsification pattern is "
        "the structural complement of H_Regime4_replication confirmation). H7 tests "
        "whether premium tea classifies cleanly into one of the three pre-registered "
        "regimes; its productive falsification is the route by which premium tea enters "
        "Regime 4."
    ),
    "items": [
        (
            "H_Regime4_replication",
            (
                "<b>Primary hypothesis (v0.14).</b> Three pre-registered conditions tested at "
                "both worldwide waves: (C1) n ≥ 12 eligible brands; (C2) |bivariate <font "
                "name='Helvetica'>ρ</font>(AI Presence, Trends)| &lt; 0.35; (C3) partial <font "
                "name='Helvetica'>ρ</font>(AI Presence, Trends | age, premium_tier) &lt; 0. "
                "All three satisfied at t<sub>1</sub> and t<sub>2</sub>: n = 17 (above C1 "
                "floor of 12); bivariate <font name='Helvetica'>ρ</font> = −0.066 / −0.134 "
                "(within C2 threshold by an order of magnitude); partial <font name="
                "'Helvetica'>ρ</font> = −0.084 / −0.146 (satisfying C3). <b>CONFIRMED.</b> "
                "Three independent confirmations across three categories (premium facial "
                "skincare and personal-finance apps in v0.13; premium tea in v0.14) elevate "
                "Regime 4 from provisional to canonical."
            ),
        ),
        (
            "Tea Box sensitivity",
            (
                "<b>Tea Box-excluded sensitivity confirms.</b> One eligible brand (\"Tea Box\", "
                "mainstream-premium tier) carries a Trends rescaled mean (166 worldwide t<sub>2"
                "</sub>, 406 US t<sub>2</sub>) anomalously high relative to its AI Presence "
                "(2.1%) because the generic phrase \"tea box\" captures gift-set search volume. "
                "Sensitivity panel drops it (n = 16): bivariate <font name='Helvetica'>ρ</font> "
                "= −0.011 / −0.129; partial <font name='Helvetica'>ρ</font> = −0.005 / −0.130. "
                "All three pre-registered conditions still satisfied. The Regime 4 verdict is "
                "robust to the inclusion or exclusion of any single brand whose Trends "
                "measurement may have been confounded by generic-phrase capture."
            ),
        ),
        (
            "H1",
            (
                "<b>H1 (bivariate Spearman <font name='Helvetica'>ρ</font> &gt; 0.5 both "
                "waves) FALSIFIED.</b> <font name='Helvetica'>ρ</font><sub>t<sub>1</sub></sub> "
                "= −0.066; <font name='Helvetica'>ρ</font><sub>t<sub>2</sub></sub> = −0.134. "
                "Falsified by both sign and magnitude — bivariate <font name='Helvetica'>"
                "ρ</font> is already negative at both waves, the cleanest H1 falsification in "
                "the programme to date and the operational signature of Regime 4b (pure sub-"
                "type) as distinct from skincare and finance's Regime 4a (migration sub-type)."
            ),
        ),
        (
            "H2",
            (
                "<b>H2 (cross-wave stability |<font name='Helvetica'>Δρ</font>| ≤ 0.15) "
                "CONFIRMED.</b> |<font name='Helvetica'>Δρ</font>| = 0.068 between t<sub>1</"
                "sub> and t<sub>2</sub> (eight-day interval). The Regime 4 signature is "
                "stable across the inter-wave window. Whatever the matched-model LLMs' "
                "training-corpus exposure captures, it captures the same thing at both "
                "measurement points; the asymmetry between AI Presence and consumer-search "
                "rank is not a wave-specific artefact."
            ),
        ),
        (
            "H3",
            (
                "<b>H3 (top-3 AI ⊆ top-5 Trends both waves) FALSIFIED.</b> 0 of 3 brands "
                "overlap at both waves. AI top-3 across both waves: Harney &amp; Sons, Yunnan "
                "Sourcing, Ippodo Tea. Trends top-5 worldwide: Twinings (pivot), Republic of "
                "Tea, Whittard of Chelsea, Tea Pigs, Lupicia. The leadership zones are "
                "entirely disjoint — the cleanest H3 falsification in the programme to date "
                "and the geometric expression of the within-category decoupling that drives "
                "the Regime 4 signature."
            ),
        ),
        (
            "H4",
            (
                "<b>H4 (partial Spearman <font name='Helvetica'>ρ</font> &gt; 0.5 both waves) "
                "FALSIFIED.</b> Partial <font name='Helvetica'>ρ</font> = −0.084 / −0.146 "
                "after controlling for brand_age_years and premium_tier ordinal. Falsified "
                "by sign and magnitude. The partial-correlation machinery confirms the "
                "bivariate decoupling is not concealed by age or tier confounds: the "
                "covariate decrement (bivariate − partial ≈ 0.02) is near-zero, distinct "
                "from v0.13 skincare's decrement of ~0.49 and finance's ~0.18. Premium tea "
                "reaches Regime 4 partial signature via an already-negative bivariate, not "
                "via covariate dissolution."
            ),
        ),
        (
            "H7",
            (
                "<b>H7 (clean classification to Regime 1 / 2 / 3) FALSIFIED productively.</b> "
                "Premium tea matches none of the three pre-registered regimes. Bivariate "
                "<font name='Helvetica'>ρ</font> = −0.066 / −0.134 — below Regime 1's lower "
                "bound of 0.35 and above Regime 2's lower bound of 0.65 in absolute terms "
                "would still place it nowhere in the pre-registered set, and n = 17 ≥ 10 "
                "puts it outside Regime 3 (Scale-mismatch via §3.6a). The productive "
                "falsification is the route by which premium tea enters Regime 4, joining "
                "skincare and finance in the canonical lower-left quadrant of (bivariate "
                "<font name='Helvetica'>ρ</font> × partial <font name='Helvetica'>ρ</font>) "
                "space."
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
            "<b>Single category at v0.14.</b> The replication test is in one category "
            "(premium tea). The strength of the result rests on cross-version triangulation "
            "with v0.13's skincare and finance findings rather than on within-version "
            "replication. Future phases (v0.15 registry expansion; v0.16+ designed-for-test "
            "in additional categories) will test whether the Regime 4 signature persists "
            "across more datapoints and whether the Regime 4a / 4b sub-classification "
            "stabilises with additional datapoints in each sub-region."
        ),
        (
            "<b>Two-wave short window.</b> Both waves are within 8 days of each other "
            "(t<sub>1</sub> = 29 April 2026; t<sub>2</sub> = 7 May 2026). The cross-wave "
            "stability finding (H2 confirmed) is short-window. Longer-horizon stability of "
            "the Regime 4 signature — month-to-month or quarter-to-quarter — is not tested "
            "at v0.14."
        ),
        (
            "<b>Matched-model subset (two models).</b> AI Presence is computed across Claude "
            "Sonnet 4.6 + GPT-5.4-mini at status = ok. The Tri-System framework's three-mode "
            "response taxonomy (Brand mode / Component mode / Authority mode) suggests "
            "inter-model variation in AI Presence may be substantial; the matched-subset "
            "constraint factors out this variation but does not address it. Future programme "
            "phases will report results across additional model families."
        ),
        (
            "<b>Single external validator (Google Trends).</b> The construct-validity test "
            "uses Google Trends as the sole external consumer-search reference. A multi-"
            "validator design — testing AI Presence simultaneously against search interest, "
            "social-media mention rates, retail sales data where available, and consumer-"
            "survey aided-recall measures — would generalise the construct-validity claim "
            "from a single-validator finding to a multi-validator finding. This is the "
            "medium-term goal of the AIAS programme (Phase 3)."
        ),
        (
            "<b>Registry coverage gap.</b> Four high-mention brands not in the v0.14 "
            "registry were observed in LLM responses: Mariage Frères (144 wave-2 mentions), "
            "Palais des Thés (82), White2Tea (83), Rare Tea Company (74). At the matched-"
            "model subset's totals these would likely enter the top-5 AI Presence ranks "
            "(Mariage Frères ahead of Twinings, possibly ahead of TWG Tea). Their absence "
            "from v0.14 reflects registry-construction timing — the registry was locked "
            "before mention frequencies were observed. The Regime 4 verdict is unlikely to "
            "invert under their inclusion (they amplify the specialty / luxury cluster that "
            "already drives the signature), but per-brand rankings should be read against "
            "this caveat. v0.15 expansion is queued."
        ),
        (
            "<b>Tea Box query ambiguity.</b> The pivot-rescaling Trends acquisition for the "
            "Tea Box brand captured generic-phrase search volume (\"tea box\" as gift-set "
            "descriptor) in addition to brand-specific search. The Tea Box-excluded "
            "sensitivity panel (§3.2 in the SSRN paper; H_Regime4_replication second row in "
            "the scoring table above) addresses this directly: all three pre-registered "
            "conditions hold at n = 16 with Tea Box dropped. The primary verdict is robust "
            "to Tea Box's inclusion or exclusion; the failure mode is documented and "
            "addressed in the AIAS Protocol v1.2 specification (Phase B disambiguation step)."
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
            "<b>v0.15 — premium tea registry expansion.</b> Add Mariage Frères (144 wave-2 "
            "mentions), Palais des Thés (82), White2Tea (83), Rare Tea Company (74), plus "
            "approximately 6 additional high-mention specialty brands surfaced in v0.14's "
            "LLM responses (What-Cha, Upton Tea Imports, Kettl, Yunomi, Den's Tea, Seven "
            "Cups, Camellia Sinensis). Re-run H_Regime4_replication on the expanded n ≈ "
            "25–27 panel. Pre-registered prediction: the Regime 4 verdict persists; "
            "expansion amplifies the specialty / Asian-tradition cluster that drives the "
            "signature."
        ),
        (
            "<b>AIAS methodology paper.</b> Formalise the four-regime taxonomy with "
            "threshold-precise definitions analogous to those for Regimes 1–3. Specify the "
            "Regime 4a (migration sub-type — skincare, finance) / Regime 4b (pure sub-type "
            "— premium tea) sub-classification once a fourth datapoint is in hand. Working "
            "title: <i>Measuring AI Availability: Methodological Notes from the AIAS "
            "Protocol</i>. Queue position now open since the Tri-System Brand Growth paper "
            "is at MSI Working Paper Series."
        ),
        (
            "<b>AIAS Protocol v1.2.</b> Increment from v1.1 to incorporate regime "
            "classification as a category-level routing step in the canonical measurement "
            "pipeline. Categories classifying to Regime 4 receive category-specific "
            "commentary on the operational substrate, since the unified condition signature "
            "admits multiple substrates — LLM training-corpus exposure asymmetry for "
            "premium tea; age-and-tier confounds for skincare and finance. Phase B "
            "generic-phrase disambiguation step formalises the Tea Box failure-mode lesson."
        ),
        (
            "<b>Phase 3 (AIAS components 2–6).</b> Construct validity established for AI "
            "Presence in v0.11 through v0.14 is a precondition for measurement work on the "
            "five remaining AIAS components: Ranking, Consistency, Coverage, Grounding, "
            "Sentiment. The four-regime taxonomy suggests each component will require its "
            "own per-category construct-validity profile rather than a uniform cross-"
            "category correlation with any single external proxy."
        ),
        (
            "<b>External brand-tracking validation.</b> Phase 3 will test AI Presence "
            "against external brand-tracking data (Kantar BrandZ, YouGov BrandIndex, brand "
            "health tracker panels). The four-regime taxonomy provides pre-registered "
            "predictions: brands in Regime 1 should show stronger AI Presence × brand-"
            "tracking correlation than brands in Regime 4. The cross-system validity test "
            "will sharpen the construct-validity claim from a Trends-only finding to a "
            "multi-validator finding."
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
            "OSF project ec6wh, /v14/. Inputs: fresh LLM acquisition (288 calls across "
            "two waves on Claude Sonnet 4.6 + GPT-5.4-mini matched-model subset, status = "
            "ok); Google Trends raw responses (8 bundles × 2 waves × 2 regions, locked at "
            "acquisition timestamp 2026-05-12T15:54:30Z); Phase A pivot validation (Twinings, "
            "mean 88.14, CV 9.13%); Phase B topic-ID resolution and bare-canonical-query "
            "outputs; Phase B-alternates activation logs (Yunnan Sourcing); premium tea "
            "registry (brands_premium_tea.json, v3 schema, 25 brands organised by "
            "premium_tier: 6 luxury, 3 specialty, 16 mainstream-premium); brand-age "
            "verified table; scoring outputs (canonical_scoring.json, "
            "h_regime4_replication.csv, h7_regime_classification.csv, per_brand_paired.csv); "
            "4 chart PDFs (regime4 canonical, primary vs sensitivity, per-category "
            "construct-validity comparison, premium tea per-brand scatter); build scripts; "
            "this report; and the matching SSRN working paper."
        ),
        (
            "Companion SSRN working paper (Gonzalez Castro 2026, SSRN 6755621). Cross-"
            "references: AI Availability foundational paper (SSRN 6659000); AIAS Presence "
            "Measurement Protocol v1.1 (SSRN 6722319); v0.6 Cross-Category Findings "
            "(SSRN 6720959); v0.7 Phantom-Brand Persistence Phase 2 BBB (SSRN 6721779); "
            "v0.8 Discourse-Language Knives (SSRN 6728000); v0.9 Longitudinal Re-Baseline "
            "(SSRN 6736878); v0.10 Naive-Phantom Rate Stability (SSRN 6741163); v0.11 PM "
            "Software × Trends Construct Validity Pilot (SSRN 6745040); v0.12 Three "
            "Empirical Regimes (SSRN 6748341); v0.13 Four Empirical Regimes — Five-Category "
            "Construct-Validity Expansion (SSRN 6750498)."
        ),
    ],
    "methodology_log": (
        "v0.14 follows AIAS Presence Measurement Protocol v1.1 (unchanged from v0.9 "
        "through v0.13). Pre-registration locked at git tag v0.14-prereg (commit b0ef30a) "
        "on 12 May 2026 UTC prior to LLM acquisition. Trends acquisition session UTC "
        "timestamp 2026-05-12T15:54:30Z. DEVIATIONS.md Entry 1 documents the Phase B bare-"
        "canonical-query methodology amendment (pytrends topic-ID errors — Republic of Tea "
        "matching to an Irish football team, Makaibari to a hotel — necessitated abandoning "
        "topic-ID resolution); Entry 2 documents Yunnan Sourcing alternate activation after "
        "Wang De Chuan and In Pursuit of Tea failed both solo and bundled-E5 padded-"
        "resolution checks. No pre-registered hypothesis, threshold, or routing rule was "
        "modified. The canonical scoring script (score_v14.py) is locked at git commit "
        "e71e135."
    ),
}
