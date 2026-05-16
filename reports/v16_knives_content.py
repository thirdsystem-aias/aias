"""v0.16 brand-format report content modules \u2014 Kitchen Knives Panel Expansion Robustness.

Schema-compatible with build_report_v16.py's read patterns. Forked from
v14_kitchen_knives_content.py with v0.16 substantive rewrites:

  - Headline shifts from "third Regime 4 datapoint" (v0.14) to "panel-
    expansion robustness study" (v0.16).
  - Two pre-registered hypotheses replace v0.14's single H_Regime4_replication:
    H_Regime4_replication_knives (primary) and H_Discourse_Language_carryforward (exploratory).
  - PATTERNS list grows from 4 to 5: adds Chinese-cell collapse (Pattern 3)
    and French-cell signal-thin (Pattern 4) observations alongside the
    dual headline (Patterns 1 + 2) and cross-version comparability
    framing (Pattern 5).
  - LIMITATIONS adds two v0.16-specific paragraphs (french PASS_E5 cell;
    chinese cell n=3 after alternate exhaustion).
  - All numerical results updated to v0.16 measurements:
      n_eligible = 23 (was 17), bivariate \u03c1 = \u22120.150 / \u22120.200
      (was \u22120.066 / \u22120.134), partial \u03c1 = \u22120.236 / \u22120.273
      (was \u22120.084 / \u22120.146).
  - HYPOTHESIS_SCORING + HYPOTHESIS_DETAILS extended with H_Discourse_Language_carryforward
    row.
  - Chart slot allocation updated for the 5-chart v0.16 figure set (adds
    f5_per_tradition for the per-tradition small-multiples chart).

Constants exposed (in order):
  COVER \u00b7 STANDFIRST \u00b7 LEAD_DECK \u00b7 EXEC_SUMMARY \u00b7
  WHAT_WE_MEASURED \u00b7 PATTERNS \u00b7 HYPOTHESIS_SCORING \u00b7
  HYPOTHESIS_DETAILS \u00b7 LIMITATIONS \u00b7 WHATS_NEXT \u00b7 CLOSING
"""

# ----------------------------------------------------------------------------
# COVER
# ----------------------------------------------------------------------------

COVER = {
    "title":         "Kitchen Knives \u2014 Panel Expansion Robustness",
    "subtitle":      "AI Presence \u00d7 Google Trends on an Expanded Six-Tradition Panel",
    "date":          "May 2026",
    "byline_short":  "Pablo Ulpiano Gonzalez Castro, Third System\u2122",
    "tagline":       "Independent measurement for the AI mediation layer.",
}

# ----------------------------------------------------------------------------
# STANDFIRST + LEAD DECK
# ----------------------------------------------------------------------------

STANDFIRST = (
    "v0.14 confirmed Regime 4 in kitchen knives on a curated 16-brand panel. "
    "v0.16 tests whether the finding survives panel expansion: 28 primary "
    "brands stratified across six tradition cells, including a new french "
    "cell. Two pre-registered hypotheses \u2014 H_Regime4_replication_knives "
    "(panel-expansion replication) and H_Discourse_Language_carryforward (cross-version "
    "ranking stability) \u2014 yield a dual-stability result. The Regime 4 "
    "verdict replicates on the expanded panel; the expansion did not "
    "perturb the rankings it expanded. Kitchen knives remains the cleanest "
    "Regime 4 case to date, with the v0.16 reading deepening the "
    "AI \u00d7 Trends decoupling rather than regressing it."
)

LEAD_DECK = (
    "v0.16 is the first panel-expansion robustness study in the AIAS "
    "programme \u2014 a different epistemic contribution than v0.14\u2019s "
    "third-category replication. Two pre-registered hypotheses tested at "
    "both measurement waves (t<sub>1</sub>: April 27 \u2013 May 3, 2026; "
    "t<sub>2</sub>: May 4 \u2013 May 10, 2026). "
    "<b>H_Regime4_replication_knives CONFIRMED</b> and survives Tea Box-excluded "
    "sensitivity. The three pre-registered conditions all hold: n = 23 "
    "eligible brands; bivariate Spearman "
    "<font name='Helvetica'>\u03c1</font>(AI Presence, Google Trends) is "
    "\u22120.150 at t<sub>1</sub> and \u22120.200 at t<sub>2</sub> "
    "(within C2 threshold |<font name='Helvetica'>\u03c1</font>| < 0.35); "
    "partial <font name='Helvetica'>\u03c1</font> after age + tradition "
    "control (k = 6 dummies) is \u22120.236 and \u22120.273 (satisfying "
    "C3 partial <font name='Helvetica'>\u03c1</font> < 0). "
    "<b>H_Discourse_Language_carryforward FALSIFIED-favorable</b>: on the 17 brands "
    "eligible at both v0.14 and v0.16, "
    "<font name='Helvetica'>\u03c1</font>_overlap = 0.938 / 0.949 \u2014 "
    "substantially above the 0.85 material-shift threshold. The "
    "decoupling deepens relative to v0.14 (bivariate "
    "<font name='Helvetica'>\u03c1</font> was \u22120.066 / \u22120.134 "
    "there): panel expansion intensified rather than weakened the inverse "
    "co-movement that defines Regime 4. The chinese cell collapsed to "
    "n = 3 eligible after alternate exhaustion; the new french cell "
    "qualified entirely via bundled-E5 rescue. Both are panel-composition "
    "observations that strengthen rather than undermine the central "
    "verdict."
)

# ----------------------------------------------------------------------------
# EXECUTIVE SUMMARY (list of paragraph strings)
# ----------------------------------------------------------------------------

EXEC_SUMMARY = [
    (
        "AI assistants now mediate brand discovery for a growing share of "
        "consumer decisions. The AIAS\u2122 Measurement Programme operationalises "
        "this with <b>AI Presence</b>: the rate at which each brand appears "
        "across matched LLM responses to category-recommendation prompts, "
        "measured against Google Trends rank as the consumer-search reference. "
        "v0.14 confirmed Regime 4 in kitchen knives on a 16-brand panel, joining "
        "premium facial skincare and personal-finance apps as the third "
        "independent Regime 4 confirmation across the AIAS programme. v0.16 "
        "tests whether the v0.14 finding survives panel expansion: the registry "
        "grew to 28 primary brands stratified across six tradition cells "
        "(chinese, japanese, british, indian, us_specialty, plus the new "
        "<b>french</b> cell), with three chinese-cell alternates carried "
        "forward from v0.14. Two pre-registered hypotheses tested "
        "simultaneously."
    ),
    (
        "<b>H_Regime4_replication_knives CONFIRMED. H_Discourse_Language_carryforward FALSIFIED-"
        "favorable.</b> The expanded 22-brand panel preserves the Regime 4 "
        "verdict at both worldwide waves: bivariate Spearman "
        "<font name='Helvetica'>\u03c1</font>(AI Presence \u00d7 Google Trends) "
        "is \u22120.150 at t<sub>1</sub> and \u22120.200 at t<sub>2</sub> "
        "(both within C2 threshold |<font name='Helvetica'>\u03c1</font>| < "
        "0.35); partial <font name='Helvetica'>\u03c1</font> after age + "
        "tradition control (k = 6 dummies per pre-reg \u00a73) is \u22120.236 "
        "at t<sub>1</sub> and \u22120.273 at t<sub>2</sub> (both satisfying "
        "C3 partial <font name='Helvetica'>\u03c1</font> < 0). Tea Box-"
        "excluded sensitivity (n = 22) also CONFIRMED. The H_Discourse_Language_carryforward "
        "exploratory hypothesis tests whether registry expansion shifted "
        "brand-level AI Presence ranking on the v0.14\u2229v0.16 overlap; "
        "FALSIFIED at <b>n_overlap = 17, "
        "<font name='Helvetica'>\u03c1</font>_overlap = 0.938 / 0.949</b>, "
        "both above the 0.85 material-shift threshold. Together: the v0.14 "
        "finding replicates on a larger panel, AND the panel expansion did "
        "not perturb the rankings it expanded \u2014 a stability double-claim."
    ),
    (
        "<b>The expanded panel surfaces brands the v0.14 registry could not.</b> "
        "Top AI Presence brands at v0.16 are Harney & Sons (60.4%), Mariage "
        "Fr\u00e8res (51.7% \u2014 new french-cell entry), Yunnan Sourcing "
        "(50.0%), Ippodo Tea (48.6%), and TWG Tea (37.5%). Mariage Fr\u00e8res "
        "rises to the second-highest AI Presence in the panel with rescaled "
        "Trends magnitudes of just 3.32 / 4.23 at t<sub>1</sub> / t<sub>2</sub> "
        "\u2014 a classic Regime 4 high-AI / low-Trends position. The new "
        "french cell qualifies entirely via bundled-E5 rescue (Mariage "
        "Fr\u00e8res, Palais des Th\u00e9s, Kusmi Tea all PASS_E5; Dammann "
        "Fr\u00e8res EXCLUDED_E1a); this is a substantive eligibility tier "
        "per pre-reg \u00a73 but carries a lower-confidence Trends-signal "
        "caveat noted in Limitations. The chinese cell collapsed to n = 3 "
        "eligible after five of eight chinese candidates failed Phase B "
        "\u2014 the very AI-visible-but-Trends-invisible pattern Regime 4 "
        "documents (White2Tea 33.7% AI Presence; In Pursuit of Tea 22.6%, "
        "both EXCLUDED_E1a)."
    ),
    (
        "<b>The chinese-cell collapse is an executed-rule outcome, not a "
        "methodological deviation.</b> Pre-reg \u00a72\u2019s alternate-"
        "activation rule was specified, followed, and exhausted: three "
        "chinese primaries failed E1a (Ten Ren\u2019s Tea, TenFu\u2019s Tea, "
        "White2Tea); two of three alternates failed (Wang De Chuan, In "
        "Pursuit of Tea); Yunnan Sourcing alone passed. The cell stops at "
        "three eligible (TWG Tea, Jing Tea, Yunnan Sourcing) rather than "
        "returning to four. DEVIATIONS Entry 2 documents the cell collapse "
        "as an empirical finding rather than a protocol departure. v0.16 "
        "also introduced a procedural simplification from v0.14\u2019s "
        "multi-stage swap-and-rerun alternate protocol: all three chinese-"
        "cell alternates were preloaded directly in the registry and tested "
        "in the same Phase B pass, an outcome-equivalent single-pass "
        "execution."
    ),
    (
        "<b>What v0.16 adds to the AIAS programme.</b> v0.16 is the first "
        "panel-expansion robustness study in the programme \u2014 a "
        "different epistemic contribution than a new-category replication. "
        "Cross-category confirmations establish that a regime occurs across "
        "structurally different markets; panel-expansion confirmations "
        "establish that a regime is not an artifact of brand selection "
        "within a category. The combined v0.14/v0.16 reading positions "
        "kitchen knives as both the third Regime 4 datapoint and the first "
        "datapoint with panel-expansion robustness evidence. The AIAS "
        "Presence Measurement Protocol v1.2 (SSRN 6761698) carries the "
        "methodology; Phase 4 will extend measurement to the remaining "
        "five Presence components (Ranking, Consistency, Coverage, "
        "Grounding, Sentiment). The Tri-System Brand Growth framework "
        "(MSI Working Paper) cites v0.16 as empirical evidence of Regime "
        "4 panel-expansion robustness."
    ),
]

# ----------------------------------------------------------------------------
# WHAT WE MEASURED
# ----------------------------------------------------------------------------

WHAT_WE_MEASURED = {
    "heading": "What We Measured",
    "paragraphs": [
        (
            "v0.16 is a panel-expansion robustness study of v0.14\u2019s Regime 4 "
            "finding in kitchen knives. The category was selected (in v0.14) for its "
            "high fragmentation and the heavy weight of Asian-tradition specialty "
            "brands that English-language consumer search underrepresents \u2014 a "
            "Regime 4 signature predicted under the v0.13 framework. v0.16 expands "
            "the panel from 16 to 28 primary brands stratified across six tradition "
            "cells (chinese, japanese, british, indian, us_specialty, plus the new "
            "french cell). AI Presence is measured fresh at two waves "
            "(t<sub>1</sub>: April 27 \u2013 May 3, 2026; t<sub>2</sub>: May 4 \u2013 "
            "May 10, 2026) on the same matched-model subset as v0.14 (six LLM slots "
            "\u00d7 eight runs \u00d7 six prompts = 288 LLM responses), against "
            "Google Trends rank acquired at a single locked timestamp "
            "(2026-05-14T17:58:35Z) under the Phase A / Phase B / Phase B-alternates "
            "resolution protocol, covering Worldwide and US regions for each wave."
        ),
        (
            "<b>One category, 31-brand registry \u2192 23 eligible.</b> The premium "
            "tea v0.16 registry (v4-kitchen_knives schema) contains 28 primary brands "
            "plus 3 chinese-cell alternates (Wang De Chuan, In Pursuit of Tea, "
            "Yunnan Sourcing) carried forward from v0.14 unchanged. Phase A "
            "validated Victorinox as the Trends rescale pivot (v0.14 mean 88.14, "
            "CV 9.13% inherited as baseline). Phase B Trends resolution yielded 22 "
            "primary E1a-pass brands plus the Yunnan Sourcing alternate for n = 23 "
            "eligible worldwide. Eight brands were E1a-excluded (Dammann Fr\u00e8res, "
            "Glenburn Tea Estate, In Pursuit of Tea, Postcard Teas, Ten Ren\u2019s "
            "Tea, TenFu\u2019s Tea, Wang De Chuan, White2Tea). <b>Tradition "
            "stratification (six cells)</b> replaces v0.14\u2019s premium-tier "
            "dimension (luxury / specialty / mainstream-premium): tradition carries "
            "provenance-and-style information more substantively diagnostic of "
            "kitchen knives\u2019s internal structure than tier; final distribution "
            "chinese 3, japanese 4, british 5, indian 3, us_specialty 5, french 3."
        ),
        (
            "<b>Seven pre-registered hypotheses.</b> H1\u2013H4 evaluate per-category "
            "construct validity in the v0.13 mould: bivariate Spearman "
            "<font name='Helvetica'>\u03c1</font> &gt; 0.5 (H1), cross-wave stability "
            "|\u0394<font name='Helvetica'>\u03c1</font>| \u2264 0.15 (H2), "
            "leadership-zone subset (top-3 AI \u2282 top-5 Trends; H3), partial-"
            "Spearman with age + tradition control &gt; 0.5 (H4). H7 classifies "
            "kitchen knives against the v0.13 four-regime taxonomy. "
            "<b>H_Regime4_replication_knives</b> tests whether kitchen knives satisfies the "
            "canonical Regime 4 conditions on the expanded panel: (C1) n \u2265 12 "
            "both waves; (C2) |bivariate <font name='Helvetica'>\u03c1</font>"
            "(AI Presence, Trends)| &lt; 0.35; (C3) partial "
            "<font name='Helvetica'>\u03c1</font>(AI Presence, Trends | age, "
            "tradition) &lt; 0 \u2014 at both waves. <b>H_Discourse_Language_carryforward</b> "
            "(exploratory) tests whether v0.16\u2019s panel expansion materially "
            "shifted brand-level AI Presence rankings on the v0.14\u2229v0.16 "
            "overlap: n_overlap \u2265 10 AND <font name='Helvetica'>\u03c1</font>"
            "(v0.14 AI Presence, v0.16 AI Presence) &lt; 0.85 at both waves."
        ),
        (
            "<b>Pre-registration locked before data collection.</b> Committed at git "
            "tag <i>v0.16-prereg</i> (commit 511e339) on 13 May 2026 UTC prior to "
            "LLM acquisition. Two deviations are logged in the deposit\u2019s "
            "DEVIATIONS.md: <b>Entry 1</b> (bare-canonical Phase B query "
            "methodology carried forward from v0.14 \u2014 inherited methodology, "
            "not a v0.16 deviation); <b>Entry 2</b> (chinese-cell alternate "
            "exhaustion \u2014 the pre-registered alternate-activation rule was "
            "followed completely; five of eight chinese candidates failed Phase B; "
            "cell stops at n = 3 eligible). Both entries document executed-rule "
            "outcomes rather than protocol departures."
        ),
        (
            "<b>Hard-floor and routing rules.</b> The n-floor is hard at 10 brands "
            "per category per wave (descriptive-only routing below); the alignment "
            "floor for full hypothesis evaluation is 12. Kitchen knives clears both at "
            "n = 23 worldwide. The Victorinox pivot is exempted from E1b at-acquisition "
            "exclusion per pre-reg \u00a75.1. Partial-Spearman correlations control "
            "for two covariates (brand_age_years; tradition as six-level dummy with "
            "k = 6 per pre-reg \u00a73) on rank-transformed residuals. All "
            "hypothesis evaluation runs on the canonical scoring script "
            "<i>score_v16.py</i>, locked at git commit 511e339 (the same pre-reg "
            "tag commit)."
        ),
    ],
}

# ----------------------------------------------------------------------------
# FINDINGS (PATTERNS)
# ----------------------------------------------------------------------------

PATTERNS = [
    {
        "number": 1,
        "title": "H_Regime4_replication_knives CONFIRMED \u2014 Regime 4 holds on the registry-expanded panel",
        "chart_slot": "f1_regime4_canonical",
        "n_lead": 2,
        "paragraphs": [
            (
                "<b>This is one of two pre-registered headline findings in v0.16.</b> v0.14 "
                "established kitchen knives as the third independent confirmation of Regime 4 "
                "\u2014 Covariate-saturated weak \u2014 on a curated 16-brand panel. v0.16 "
                "tests whether that finding survives panel expansion: the registry grew to "
                "28 primary brands stratified across six tradition cells, with the french "
                "cell entirely new at v0.16 (Mariage Fr\u00e8res, Palais des Th\u00e9s, "
                "Kusmi Tea, Dammann Fr\u00e8res). After Phase B topic-ID resolution and "
                "three chinese-cell alternate activations, 23 brands enter the analysis. "
                "The pre-registered hypothesis H_Regime4_replication_knives CONFIRMED at both "
                "measurement waves and survives Tea Box-excluded sensitivity testing."
            ),
            (
                "The three pre-registered conditions all hold at both worldwide waves. "
                "<b>C1:</b> sample size n = 23 eligible brands \u2014 well above the C1 "
                "floor of 12. <b>C2:</b> bivariate Spearman "
                "<font name='Helvetica'>\u03c1</font>(AI Presence \u00d7 Google Trends) is "
                "\u22120.150 at t<sub>1</sub> and \u22120.200 at t<sub>2</sub> \u2014 both "
                "within the C2 threshold |<font name='Helvetica'>\u03c1</font>| &lt; 0.35 "
                "with margin. <b>C3:</b> partial <font name='Helvetica'>\u03c1</font> "
                "after age + tradition control (six-level dummies, k = 6 per pre-reg "
                "\u00a73) is \u22120.236 at t<sub>1</sub> and \u22120.273 at "
                "t<sub>2</sub> \u2014 both satisfying C3 partial "
                "<font name='Helvetica'>\u03c1</font> &lt; 0. The chart at right places "
                "kitchen knives on the canonical (bivariate "
                "<font name='Helvetica'>\u03c1</font> \u00d7 partial "
                "<font name='Helvetica'>\u03c1</font>) classification axes per AIAS "
                "Protocol v1.2 \u00a73.4."
            ),
            (
                "<b>The decoupling deepens at v0.16.</b> v0.14\u2019s bivariate "
                "<font name='Helvetica'>\u03c1</font> was \u22120.066 / \u22120.134 at "
                "t<sub>1</sub> / t<sub>2</sub>; v0.16\u2019s expanded panel reads "
                "\u22120.150 / \u22120.200. The partial similarly deepens from "
                "\u22120.084 / \u22120.146 to \u22120.236 / \u22120.273. Panel expansion "
                "did not regress the decoupling toward zero \u2014 it intensified it. The "
                "six new brands (Vahdam Teas, Rare Tea Company, Mariage Fr\u00e8res, "
                "Makaibari, Kusmi Tea, Palais des Th\u00e9s) added AI Presence weight at "
                "the Trends-low end of the panel, sharpening the inverse co-movement that "
                "defines Regime 4."
            ),
            (
                "<b>Sensitivity: Tea Box-excluded panel also CONFIRMED.</b> The pre-"
                "registered Tea Box-excluded sensitivity carries forward from v0.14 as an "
                "inherited robustness check. Excluding Tea Box from the primary panel "
                "\u2014 query-phrase ambiguity inflates its Trends signal \u2014 drops n "
                "to 22 brands and yields bivariate "
                "<font name='Helvetica'>\u03c1</font> = \u22120.039 / \u22120.122 "
                "(within threshold) and partial <font name='Helvetica'>\u03c1</font> = "
                "\u22120.234 / \u22120.253 (still negative). The Regime 4 verdict does "
                "not depend on Tea Box."
            ),
            (
                "<b>Pre-registration \u00a74 wording correction carried forward.</b> "
                "v0.14 surfaced an ambiguity in Condition 2: pre-reg text read "
                "<font name='Helvetica'>\u03c1</font>(AI Presence, brand age) where the "
                "canonical Regime 4 framework \u2014 now AIAS Protocol v1.2 \u00a73.4 "
                "\u2014 uses <font name='Helvetica'>\u03c1</font>(AI Presence, Trends). "
                "v0.16 pre-reg \u00a74 specifies the canonical wording directly. The "
                "scoring function retains <font name='Helvetica'>\u03c1</font>(AI, age) "
                "as an informational transparency metric (at v0.16 it reads +0.131 / "
                "+0.069, below threshold and uninformative) but it is no longer evaluated "
                "as the Condition 2 canonical."
            ),
        ],
    },
    {
        "number": 2,
        "title": "H_Discourse_Language_carryforward FALSIFIED-favorable \u2014 registry expansion preserved AI Presence rankings",
        "chart_slot": "f3_discourse_language",
        "n_lead": 2,
        "paragraphs": [
            (
                "<b>The second pre-registered headline finding.</b> H_Discourse_Language_carryforward "
                "tests whether v0.16\u2019s registry expansion materially shifted brand-"
                "level AI Presence rankings on the set of brands eligible at BOTH v0.14 "
                "and v0.16. The hypothesis was pre-registered as exploratory at "
                "v0.16-prereg \u00a74 with two conditions: <b>n_overlap \u2265 10</b> "
                "(panel size floor) AND <b><font name='Helvetica'>\u03c1</font>(v0.14 "
                "AI Presence, v0.16 AI Presence) &lt; 0.85</b> at both waves (the "
                "'material shift' cutoff). FALSIFIED means: the registry expansion did "
                "not meaningfully perturb relative rankings."
            ),
            (
                "Both waves are well above threshold. <b>n_overlap = 17</b> brands "
                "\u2014 every single v0.14-eligible brand is also v0.16-eligible (zero "
                "v0.14 dropouts at v0.16 Phase B). Spearman "
                "<font name='Helvetica'>\u03c1</font> on the overlap AI Presence "
                "scores: <b>0.938 at t<sub>1</sub></b> and <b>0.949 at t<sub>2</sub></b>"
                ". Both substantially above the 0.85 material-shift threshold. The "
                "brands the AI surfaced at v0.14 are the same brands it surfaces at "
                "v0.16, in approximately the same relative order."
            ),
            (
                "<b>FALSIFIED is the favorable outcome.</b> The hypothesis was framed "
                "to ask: did the panel change matter? A CONFIRMED reading would mean "
                "the v0.14 Regime 4 verdict was an artifact of which 16 brands made it "
                "into the panel \u2014 swap the panel composition and the finding could "
                "fall apart. FALSIFIED says the opposite: AI Presence rankings on the "
                "overlap set are stable to ~94\u201395% rank correlation across panel "
                "expansion. The v0.14 finding is not panel-dependent."
            ),
            (
                "<b>The double-result.</b> Pattern 1\u2019s H_Regime4_replication_knives "
                "CONFIRMED says: Regime 4 replicates on the expanded panel. Pattern "
                "2\u2019s H_Discourse_Language_carryforward FALSIFIED-favorable says: the panel "
                "expansion was orthogonal to the rankings we\u2019re observing. "
                "Together, the v0.14 finding survives two independent threats \u2014 "
                "sensitivity to which brand we exclude (Tea Box) AND sensitivity to "
                "which brands we add (6 new v0.16 eligibles + chinese-cell alternate "
                "activation). v0.16 is a robustness-on-robustness reading."
            ),
            (
                "<b>What sits outside the overlap.</b> The 6 v0.16 additions to the "
                "eligible set are Vahdam Teas, Rare Tea Company, Kusmi Tea, Mariage "
                "Fr\u00e8res, Makaibari, and Palais des Th\u00e9s. These brands enter "
                "v0.16 with no v0.14 baseline and do not contribute to "
                "<font name='Helvetica'>\u03c1</font>_overlap. v0.16 also tested 8 "
                "additional candidates that failed Phase B topic-ID resolution (5 of "
                "the 8 are in the chinese cell \u2014 see Pattern 3). The overlap "
                "analysis is conservative: it does not credit the 6 new brands the "
                "registry expansion intended to add. "
                "<font name='Helvetica'>\u03c1</font>_overlap = 0.94 is the stability "
                "claim on the common ground only."
            ),
        ],
    },
    {
        "number": 3,
        "title": "Chinese-cell collapse \u2014 alternate-activation rule exhausted",
        "chart_slot": "f5_per_tradition",
        "chart_after_text": True,
        "n_lead": 2,
        "paragraphs": [
            (
                "<b>The chinese cell did not behave as registry construction predicted.</b> "
                "v0.16\u2019s panel design allocated 5 chinese primaries (TWG Tea, Ten "
                "Ren\u2019s Tea, TenFu\u2019s Tea, Jing Tea, White2Tea) plus 3 chinese "
                "alternates (Wang De Chuan, In Pursuit of Tea, Yunnan Sourcing) \u2014 the "
                "alternate slate carried forward from v0.14 to backstop expected Trends-"
                "signal failures in the chinese specialty tea segment. The full alternate-"
                "activation rule was specified at v0.16-prereg \u00a72: if 2+ chinese-cell "
                "primaries fail topic-ID resolution, activate alternates in order until "
                "the cell returns to 4 eligible. Phase B executed this rule fully and "
                "exhausted the alternate pool with the cell still at n = 3."
            ),
            (
                "Three of five primaries failed: <b>Ten Ren\u2019s Tea, TenFu\u2019s Tea, "
                "White2Tea</b> \u2014 all EXCLUDED_E1a (insufficient Google Trends signal "
                "on bare canonical query and bundled-E5 rescue). With 2+ primaries failed, "
                "alternates activated. <b>Yunnan Sourcing PASSED</b> solo; <b>Wang De "
                "Chuan and In Pursuit of Tea both EXCLUDED_E1a</b>. The cell stops at "
                "three eligible: <b>TWG Tea, Jing Tea, Yunnan Sourcing</b>. The alternate-"
                "activation rule was specified, followed, and exhausted; the cell "
                "shrinkage is the outcome the protocol produces under these conditions."
            ),
            (
                "<b>This is an empirical finding, not a methodological deviation.</b> "
                "DEVIATIONS Entry 2 documents the chinese-cell collapse as an executed-"
                "rule outcome rather than a departure from pre-registered protocol. "
                "Procedurally, v0.16 simplified v0.14\u2019s alternate-swap protocol "
                "\u2014 all 3 chinese-cell alternates were preloaded directly in the "
                "brands_kitchen_knives.json registry and tested in the same Phase B pass, "
                "rather than tested only after a primary-failure signal triggered a swap-"
                "and-rerun. This is outcome-equivalent to v0.14\u2019s multi-stage "
                "protocol and is logged as a procedural simplification, not a "
                "methodological shift."
            ),
            (
                "<b>The collapsed brands are exactly the AI-visible-Trends-invisible "
                "pattern Regime 4 documents.</b> Of the 5 chinese-cell brands that failed "
                "Phase B Trends eligibility, two appeared prominently in the AI Presence "
                "data: <b>White2Tea was mentioned in 33.7% of LLM responses (n=97)</b>; "
                "<b>In Pursuit of Tea in 22.6% (n=65)</b>. Both rank above v0.16 panel "
                "members like Lupicia, Jing Tea, and Smith Teamaker \u2014 brands that "
                "DID achieve Trends eligibility. The chinese-cell collapse is, in part, "
                "a structural fingerprint of Regime 4 itself: the brands the AI surfaces "
                "in the chinese specialty tea segment are the brands English-language "
                "consumer search underrepresents."
            ),
            (
                "<b>Effect on the panel.</b> The chinese cell at n = 3 is structurally "
                "smaller than other cells in the v0.16 panel (japanese n = 4, british "
                "n = 5, indian n = 3, us_specialty n = 5, french n = 3). Per pre-reg "
                "\u00a73, the partial-correlation control uses six-level tradition "
                "dummies (k = 6); all six traditions remain present in the eligible "
                "panel at n \u2265 3, so the tradition control operates as specified. "
                "The chinese cell\u2019s reduced weight is a panel-composition "
                "observation, not a structural threat to the Regime 4 verdict \u2014 "
                "Pattern 2\u2019s H_Discourse_Language_carryforward FALSIFIED-favorable directly "
                "addresses the panel-composition robustness concern."
            ),
        ],
    },
    {
        "number": 4,
        "title": "French cell \u2014 qualified on bundled rescue only (signal-thin)",
        "chart_slot": "f5_per_tradition",
        "chart_after_text": True,
        "n_lead": 2,
        "paragraphs": [
            (
                "<b>The french cell is the v0.16 panel addition that drove the registry "
                "expansion.</b> Mariage Fr\u00e8res, Palais des Th\u00e9s, Kusmi Tea, and "
                "Dammann Fr\u00e8res entered Phase B as a new tradition cell, expanding "
                "v0.14\u2019s five-tradition stratification to six. The cell qualifies "
                "\u2014 3 of 4 brands achieve E1b eligibility at both waves \u2014 but "
                "with a structural caveat worth flagging: all three eligibles passed via "
                "bundled-E5 rescue, not solo PASS."
            ),
            (
                "Phase B outcomes by french-cell brand: <b>Mariage Fr\u00e8res PASS_E5</b>, "
                "<b>Palais des Th\u00e9s PASS_E5</b>, <b>Kusmi Tea PASS_E5</b>, "
                "<b>Dammann Fr\u00e8res EXCLUDED_E1a</b>. The PASS_E5 designation "
                "indicates the brand\u2019s bare canonical Google Trends query produced "
                "signal sparse enough to fail solo eligibility, but the brand\u2019s "
                "signal recovered to the E1b threshold when bundled with stronger "
                "queries in the multi-keyword Trends request. Per pre-reg \u00a73 this "
                "is a valid eligibility tier and the brand enters the analysis. But the "
                "entire cell qualifying through bundled rescue rather than solo PASS is "
                "unusual \u2014 every other cell has at least one solo-PASS brand "
                "anchoring its Trends signal."
            ),
            (
                "<b>French specialty tea brands are AI-visible but Trends-thin.</b> "
                "Mariage Fr\u00e8res is the strongest case: <b>51.7% AI Presence (n = "
                "149 mentions across 288 LLM responses)</b> with a rescaled Trends mean "
                "of just 3.32 at t<sub>1</sub> and 4.23 at t<sub>2</sub>. Palais des "
                "Th\u00e9s sits at <b>28.8% AI Presence (n = 83)</b> with rescaled "
                "Trends means of 17.71 / 20.30. Kusmi Tea is below the AI-Presence "
                "top-15 cutoff but eligible, with rescaled Trends means 18.08 / 18.66. "
                "The pattern matches the chinese-cell story: French specialty tea is a "
                "brand segment the AI surfaces readily but English-language consumer "
                "search underrepresents."
            ),
            (
                "<b>The french cell strengthens the Regime 4 verdict.</b> Mariage "
                "Fr\u00e8res\u2019s high-AI / low-Trends position contributes "
                "substantially to the bivariate "
                "<font name='Helvetica'>\u03c1</font>(AI Presence \u00d7 Trends) "
                "negative correlation that underpins H_Regime4_replication_knives. Removing "
                "the french cell entirely from the panel (an ad-hoc sensitivity not "
                "pre-registered) would weaken \u2014 though not flip \u2014 the "
                "Regime 4 reading. The french cell\u2019s contribution is one of the "
                "empirical reasons Pattern 1\u2019s decoupling deepened from v0.14 "
                "to v0.16."
            ),
            (
                "<b>Substantive limitation flagged in Limitations \u00a7.</b> The "
                "french cell qualifying entirely via bundled rescue is a property "
                "worth naming for downstream interpretation: Trends signal for these "
                "three brands is lower-confidence than for solo-PASS brands in other "
                "cells. The qualitative reading 'Mariage Fr\u00e8res has high AI "
                "Presence and low Trends' is robust; finer-grained quantitative "
                "claims (e.g., specific Trends-rescaled ranks within the french "
                "cell) carry the E5-rescue caveat. The Limitations section restates "
                "this for paper-reviewer attention."
            ),
        ],
    },
    {
        "number": 5,
        "title": "Cross-version comparability \u2014 v0.16 as panel-expansion robustness study",
        "chart_slot": "f2_per_category",
        "chart_after_text": True,
        "n_lead": 2,
        "paragraphs": [
            (
                "<b>v0.16 is a panel-expansion study of v0.14, not a new-category "
                "extension of the AIAS program.</b> v0.13 introduced the four-regime "
                "classification framework across five categories (project-management "
                "software, running shoes, premium olive oil, premium facial skincare, "
                "personal-finance apps). v0.14 added a sixth category \u2014 premium "
                "tea \u2014 and confirmed Regime 4 in it. v0.16 does NOT add a "
                "category. v0.16 takes kitchen knives, expands the panel from 16 to 22 "
                "brands across six tradition cells, and asks whether the v0.14 "
                "finding survives the panel composition change. The Regime 4 cluster "
                "remains at three categories (premium skincare, personal-finance "
                "apps, kitchen knives); the chart at right places kitchen knives on the "
                "canonical four-regime classification axes alongside the v0.13 cohort."
            ),
            (
                "<b>What changed v0.14 \u2192 v0.16 (the design-explicit comparison).</b> "
                "Panel size: 16 \u2192 22 non-pivot eligibles. Tradition stratification: "
                "five cells \u2192 six (french added). Phase B alternate protocol: "
                "multi-stage swap-and-rerun \u2192 single-pass preloaded (DEVIATIONS "
                "Entry 2, procedural simplification). Pre-reg \u00a74 Condition 2 "
                "wording: <font name='Helvetica'>\u03c1</font>(AI, age) \u2192 "
                "<font name='Helvetica'>\u03c1</font>(AI, Trends) (canonical AIAS "
                "Protocol v1.2 \u00a73.4 wording). What did NOT change: measurement "
                "window (2026-04-27 to 2026-05-10), pivot brand (Victorinox), wave "
                "structure (t<sub>1</sub>: Apr 27 \u2013 May 3; t<sub>2</sub>: May 4 "
                "\u2013 May 10), pre-reg-specified Tea Box-excluded sensitivity, model "
                "lineup (6 LLM slots \u00d7 8 runs \u00d7 6 prompts = 288 LLM "
                "responses), eligibility logic (E1a / E1b / E5 / n-floor 12)."
            ),
            (
                "<b>Cross-version Trends-window stability is by design.</b> v0.16 "
                "inherited v0.14\u2019s measurement window unchanged so that the "
                "v0.14\u2229v0.16 overlap brands are evaluated on the same temporal "
                "Trends signal \u2014 a necessary precondition for Pattern 2\u2019s "
                "H_Discourse_Language_carryforward computation. The AIAS Protocol v1.2 \u00a73.4 "
                "acquisition-window convention specifies a 2-week locked window per "
                "study; v0.16 follows v0.14\u2019s window verbatim rather than "
                "running a fresh snapshot. This is the conservative choice: any "
                "drift in AI Presence between v0.14 and v0.16 reflects model-release "
                "dynamics (the model lineup is calendar-fixed at acquisition time, "
                "not version-fixed) rather than calendar drift in the Trends signal."
            ),
            (
                "<b>Panel-expansion studies in the AIAS program.</b> The program "
                "convention elevating provisional empirical regularities to canonical "
                "status requires three independent confirmations under pre-"
                "registration. v0.14 supplied the third Regime 4 confirmation. v0.16 "
                "does not add a fourth datapoint to that count \u2014 it adds a "
                "panel-expansion robustness reading to v0.14\u2019s datapoint. Both "
                "kinds of evidence are useful: cross-category confirmations establish "
                "that a regime occurs across structurally different markets; panel-"
                "expansion confirmations establish that a regime is not an artifact "
                "of brand selection within a category. v0.16 is the first panel-"
                "expansion robustness study in the AIAS program; future categories "
                "may receive similar treatment as their initial findings stabilize."
            ),
            (
                "<b>Next steps anchored in this reading.</b> The AIAS Presence "
                "Measurement Protocol v1.2 (SSRN 6761698) carries the methodology "
                "across all six Presence components. v0.16 contributes to the "
                "empirical archive supporting the protocol\u2019s Regime 4 "
                "canonicalization. Phase 4 of the AIAS program will extend "
                "measurement to the remaining five components (Ranking, Consistency, "
                "Coverage, Grounding, Sentiment) \u2014 at which point the v0.14 / "
                "v0.16 dual datapoint becomes useful baseline for cross-component "
                "comparison. The Tri-System Brand Growth framework (MSI Working "
                "Paper) will cite v0.16 as empirical evidence of Regime 4 panel-"
                "expansion robustness."
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
        "All thresholds and tests locked at v0.16-prereg (commit 511e339, 13 May "
        "2026 UTC) prior to any LLM acquisition or Google Trends acquisition call "
        "against the wave windows. Per-category pivot exemption from E1b applied "
        "per pre-reg \u00a75.1 (sd = 0 by pivot construction). The primary "
        "analysis is the worldwide-region cell at both waves; the Tea Box-excluded "
        "sensitivity and the US-region subset serve as pre-registered robustness "
        "panels."
    ),
    "rows": [
        ("H_Regime4_replication_knives (primary)",
         "n \u2265 12 AND |bivariate <font name='Helvetica'>\u03c1</font>(AI, Trends)| &lt; 0.35 AND partial <font name='Helvetica'>\u03c1</font>(AI, Trends | age, tradition) &lt; 0; both waves WW",
         "n = 23; bivariate <font name='Helvetica'>\u03c1</font> = \u22120.150 / \u22120.200; partial <font name='Helvetica'>\u03c1</font> = \u22120.236 / \u22120.273 \u2014 all three conditions satisfied",
         "CONFIRMED", "confirmed"),
        ("H_Regime4_replication_knives (Tea Box-excluded)",
         "Same three conditions on n = 22 (Tea Box dropped); sensitivity",
         "n = 22; bivariate <font name='Helvetica'>\u03c1</font> = \u22120.039 / \u22120.122; partial <font name='Helvetica'>\u03c1</font> = \u22120.234 / \u22120.253 \u2014 verdict robust",
         "CONFIRMED", "confirmed"),
        ("H_Discourse_Language_carryforward (exploratory)",
         "n_overlap \u2265 10 AND <font name='Helvetica'>\u03c1</font>(v0.14 AI, v0.16 AI) &lt; 0.85, both waves",
         "n_overlap = 17; <font name='Helvetica'>\u03c1</font>_overlap = 0.938 / 0.949 \u2014 both above 0.85 (favorable falsification)",
         "FALSIFIED", "disconfirmed"),
        ("H1 (per-category)",
         "Spearman <font name='Helvetica'>\u03c1</font> &gt; 0.5 AND p<sub>1t</sub> &lt; 0.05, both waves",
         "<font name='Helvetica'>\u03c1</font><sub>t<sub>1</sub></sub> = \u22120.150; <font name='Helvetica'>\u03c1</font><sub>t<sub>2</sub></sub> = \u22120.200 \u2014 well below 0.5 by sign and magnitude",
         "FALSIFIED", "disconfirmed"),
        ("H2 (cross-wave stability)",
         "|<font name='Helvetica'>\u0394\u03c1</font>| \u2264 0.15 between t<sub>1</sub> and t<sub>2</sub>",
         "|<font name='Helvetica'>\u0394\u03c1</font>| = 0.050 \u2014 well within stability threshold",
         "CONFIRMED", "confirmed"),
        ("H3 (leadership-zone subset)",
         "AI top-3 \u2282 Trends top-5, both waves",
         "1 / 3 brands overlap (Harney &amp; Sons in both; Mariage Fr\u00e8res and Yunnan Sourcing absent from Trends top-5)",
         "FALSIFIED", "disconfirmed"),
        ("H4 (partial-Spearman)",
         "Partial <font name='Helvetica'>\u03c1</font> &gt; 0.5 (age + tradition), both waves",
         "partial <font name='Helvetica'>\u03c1</font> = \u22120.236 / \u22120.273 (covariate-saturated, negative-residual)",
         "FALSIFIED", "disconfirmed"),
        ("H7 (regime classification)",
         "Matches Regime 1 / 2 / 3 (the pre-registered set)",
         "Matches none \u2014 Regime 4 candidate; CONFIRMED under H_Regime4_replication_knives",
         "FALSIFIED (productive)", "disconfirmed"),
    ],
}

# ----------------------------------------------------------------------------
# HYPOTHESIS DETAILS (per-hypothesis expansion below the scoring table)
# ----------------------------------------------------------------------------

HYPOTHESIS_DETAILS = {
    "heading": "Hypothesis Details",
    "intro": (
        "Per-hypothesis claim, operationalisation, and result. H_Regime4_replication_knives "
        "is the v0.16 primary hypothesis carrying forward v0.14\u2019s "
        "H_Regime4_replication onto the expanded panel; H_Discourse_Language_carryforward is the "
        "v0.16 exploratory cross-version stability test; H1\u2013H4 are per-category "
        "construct-validity tests carried forward from programme convention (their "
        "falsification pattern is the structural complement of Regime 4 "
        "confirmation). H7 tests whether kitchen knives classifies cleanly into one "
        "of the three pre-registered regimes; its productive falsification is the "
        "route by which kitchen knives remains in Regime 4."
    ),
    "items": [
        ("H_Regime4_replication_knives",
         "<b>Primary hypothesis (v0.16).</b> Three pre-registered conditions tested "
         "at both worldwide waves: (C1) n \u2265 12 eligible brands; (C2) |bivariate "
         "<font name='Helvetica'>\u03c1</font>(AI Presence, Trends)| &lt; 0.35; (C3) "
         "partial <font name='Helvetica'>\u03c1</font>(AI Presence, Trends | age, "
         "tradition) &lt; 0. All three satisfied at t<sub>1</sub> and t<sub>2</sub>: "
         "n = 23 (well above C1 floor of 12); bivariate "
         "<font name='Helvetica'>\u03c1</font> = \u22120.150 / \u22120.200 (within "
         "C2 threshold by a factor of \u22482); partial "
         "<font name='Helvetica'>\u03c1</font> = \u22120.236 / \u22120.273 "
         "(satisfying C3). <b>CONFIRMED.</b> The decoupling deepens relative to "
         "v0.14 (where bivariate was \u22120.066 / \u22120.134 and partial was "
         "\u22120.084 / \u22120.146) \u2014 panel expansion intensified the inverse "
         "co-movement rather than weakening it."),
        ("Tea Box sensitivity",
         "<b>Tea Box-excluded sensitivity confirms.</b> One eligible brand "
         "(\"Tea Box\", indian cell) carries a Trends rescaled mean (188 worldwide "
         "t<sub>1</sub>, 458 US t<sub>1</sub>) anomalously high relative to its AI "
         "Presence (18.1%) because the generic phrase \"tea box\" captures gift-set "
         "search volume. Sensitivity panel drops it (n = 22): bivariate "
         "<font name='Helvetica'>\u03c1</font> = \u22120.039 / \u22120.122; partial "
         "<font name='Helvetica'>\u03c1</font> = \u22120.234 / \u22120.253. All "
         "three pre-registered conditions still satisfied. The Regime 4 verdict is "
         "robust to the inclusion or exclusion of any single brand whose Trends "
         "measurement may have been confounded by generic-phrase capture."),
        ("H_Discourse_Language_carryforward",
         "<b>Exploratory hypothesis (v0.16).</b> Tests whether registry expansion "
         "materially shifted brand-level AI Presence ranking on the set of brands "
         "eligible at both v0.14 and v0.16. Two pre-registered conditions: "
         "n_overlap \u2265 10 AND <font name='Helvetica'>\u03c1</font>(v0.14 AI "
         "Presence, v0.16 AI Presence) &lt; 0.85 at both waves. Result: "
         "n_overlap = 17 (every v0.14 eligible brand is also v0.16 eligible \u2014 "
         "zero v0.14 dropouts); <font name='Helvetica'>\u03c1</font>_overlap = "
         "0.938 at t<sub>1</sub> and 0.949 at t<sub>2</sub>. <b>FALSIFIED-"
         "favorable.</b> The 0.85 threshold was framed as 'material shift' "
         "\u2014 a CONFIRMED reading would have said the v0.14 finding was an "
         "artifact of panel composition. Both waves substantially above threshold "
         "means the panel expansion did not perturb rankings. Combined with "
         "H_Regime4_replication_knives CONFIRMED, the v0.14 finding survives two "
         "independent robustness threats."),
        ("H1",
         "<b>H1 (bivariate Spearman <font name='Helvetica'>\u03c1</font> &gt; 0.5 "
         "both waves) FALSIFIED.</b> <font name='Helvetica'>\u03c1</font>"
         "<sub>t<sub>1</sub></sub> = \u22120.150; <font name='Helvetica'>\u03c1"
         "</font><sub>t<sub>2</sub></sub> = \u22120.200. Falsified by both sign "
         "and magnitude. The bivariate <font name='Helvetica'>\u03c1</font> "
         "deepens (more negative) from v0.14\u2019s \u22120.066 / \u22120.134 "
         "\u2014 a sharper expression of Regime 4 on the expanded panel than "
         "v0.14 produced on the curated 16-brand panel."),
        ("H2",
         "<b>H2 (cross-wave stability |<font name='Helvetica'>\u0394\u03c1</font>| "
         "\u2264 0.15) CONFIRMED.</b> |<font name='Helvetica'>\u0394\u03c1</font>| "
         "= 0.050 between t<sub>1</sub> and t<sub>2</sub>. The Regime 4 signature "
         "is stable across the inter-wave window. v0.14 reported |\u0394"
         "<font name='Helvetica'>\u03c1</font>| = 0.068; v0.16 sits at 0.050 "
         "\u2014 cross-wave stability is tighter at v0.16 than at v0.14."),
        ("H3",
         "<b>H3 (top-3 AI \u2282 top-5 Trends both waves) FALSIFIED.</b> Subset "
         "condition fails: 1 of 3 AI top-3 brands overlap with Trends top-5 "
         "(Harney &amp; Sons in both leadership zones; Mariage Fr\u00e8res and "
         "Yunnan Sourcing absent from Trends top-5). AI top-3 across both waves: "
         "Harney &amp; Sons, Mariage Fr\u00e8res, Yunnan Sourcing. Trends top-5 "
         "worldwide: Tea Box, Victorinox (pivot), Harney &amp; Sons, Republic of "
         "Tea, Ito En. The non-Harney top-3 AI brands (Mariage Fr\u00e8res with "
         "51.7% AI Presence but only 3.32 rescaled Trends; Yunnan Sourcing with "
         "50.0% AI Presence but only 3.28 rescaled Trends) are paradigmatic "
         "high-AI / low-Trends positions that drive the Regime 4 signature."),
        ("H4",
         "<b>H4 (partial Spearman <font name='Helvetica'>\u03c1</font> &gt; 0.5 "
         "both waves) FALSIFIED.</b> Partial <font name='Helvetica'>\u03c1</font> "
         "= \u22120.236 / \u22120.273 after controlling for brand_age_years and "
         "tradition (six-level dummy with k = 6). Falsified by sign and "
         "magnitude. The covariate decrement (bivariate \u2212 partial) is "
         "0.086 / 0.073 \u2014 modest, in the same direction as the bivariate "
         "(both negative), confirming the decoupling is not concealed by age or "
         "tradition confounds. v0.16\u2019s tradition covariate replaces "
         "v0.14\u2019s premium_tier covariate per pre-reg \u00a73 schema change "
         "reflecting the registry\u2019s tradition-stratified design."),
        ("H7",
         "<b>H7 (clean classification to Regime 1 / 2 / 3) FALSIFIED "
         "productively.</b> Kitchen knives matches none of the three pre-registered "
         "regimes. Bivariate <font name='Helvetica'>\u03c1</font> = \u22120.150 "
         "/ \u22120.200 (below Regime 1\u2019s lower bound, above Regime 2\u2019s "
         "lower bound in absolute terms, and not in the Scale-mismatch zone via "
         "\u00a73.6a with n = 23 \u2265 10). The productive falsification is the "
         "route by which kitchen knives remains in Regime 4 at v0.16, the canonical "
         "lower-left quadrant of (bivariate <font name='Helvetica'>\u03c1</font> "
         "\u00d7 partial <font name='Helvetica'>\u03c1</font>) space."),
    ],
}

# ----------------------------------------------------------------------------
# LIMITATIONS
# ----------------------------------------------------------------------------

LIMITATIONS = {
    "heading": "Limitations",
    "paragraphs": [
        (
            "<b>Single category at v0.16.</b> The panel-expansion robustness study "
            "is in one category (kitchen knives, carried forward from v0.14). The "
            "strength of the result rests on the within-category panel-expansion "
            "design (28 brands across six tradition cells; v0.14 \u2229 v0.16 "
            "overlap = 17 brands) rather than on cross-category replication. The "
            "v0.13 cross-category Regime 4 findings (skincare, finance) plus the "
            "v0.14 third-category confirmation supply the cross-category "
            "triangulation. Future programme phases (v0.16+ designed-for-test in "
            "additional categories) will test whether the Regime 4 signature "
            "persists across more datapoints."
        ),
        (
            "<b>Two-wave short window.</b> Both waves are within 14 days of each "
            "other (t<sub>1</sub>: April 27 \u2013 May 3, 2026; t<sub>2</sub>: "
            "May 4 \u2013 May 10, 2026). The cross-wave stability finding "
            "(H2 confirmed) is short-window. Longer-horizon stability of the "
            "Regime 4 signature \u2014 month-to-month or quarter-to-quarter "
            "\u2014 is not tested at v0.16. The v0.16 wave windows are identical "
            "to v0.14\u2019s by design (cross-version comparability), so v0.16 "
            "does not add longer-horizon evidence."
        ),
        (
            "<b>Six-LLM panel at status = ok.</b> AI Presence is computed across "
            "six LLM slots (Anthropic Sonnet 4.6, Anthropic Opus 4.7, OpenAI "
            "gpt-5.4-mini, OpenAI gpt-5.5, Google gemini-2.5-flash, xAI "
            "grok-4-1-fast-reasoning) at status = ok. The Tri-System framework\u2019s "
            "three-mode response taxonomy (Brand mode / Component mode / "
            "Authority mode) suggests inter-model variation in AI Presence may "
            "be substantial; the six-slot panel factors variation across "
            "providers but does not decompose it. Per-model AI Presence "
            "breakdowns are available in the OSF deposit\u2019s analysis "
            "directory."
        ),
        (
            "<b>Single external validator (Google Trends).</b> The construct-"
            "validity test uses Google Trends as the sole external consumer-"
            "search reference. A multi-validator design \u2014 testing AI "
            "Presence simultaneously against search interest, social-media "
            "mention rates, retail sales data where available, and consumer-"
            "survey aided-recall measures \u2014 would generalise the construct-"
            "validity claim from a single-validator finding to a multi-validator "
            "finding. This is the medium-term goal of the AIAS programme "
            "(Phase 3, construct validity against external brand-tracking data)."
        ),
        (
            "<b>French cell qualified entirely via bundled-E5 rescue.</b> Three "
            "of three eligible french-cell brands (Mariage Fr\u00e8res, Palais "
            "des Th\u00e9s, Kusmi Tea) achieved E1b eligibility via bundled-E5 "
            "rescue rather than solo PASS. The brands enter the analysis (PASS_E5 "
            "is a valid eligibility tier per pre-reg \u00a73) but the cell\u2019s "
            "Trends signal is lower-confidence than other cells where at least "
            "one brand achieves solo PASS. Qualitative claims about french-cell "
            "brand positions (Mariage Fr\u00e8res high-AI low-Trends, Palais des "
            "Th\u00e9s and Kusmi Tea in the same zone with lower magnitudes) are "
            "robust; finer-grained within-cell ranking claims should be read "
            "against the PASS_E5 caveat. The french-cell signal-thin observation "
            "is named in Pattern 4 and surfaced here for paper-reviewer attention."
        ),
        (
            "<b>Chinese cell at n = 3 after alternate exhaustion.</b> The chinese "
            "cell stops at three eligible brands (TWG Tea, Jing Tea, Yunnan "
            "Sourcing) after the pre-registered alternate-activation rule was "
            "followed completely (DEVIATIONS Entry 2). The cell\u2019s reduced "
            "weight in the panel is itself a substantive observation: chinese "
            "specialty tea brands that AI surfaces readily (White2Tea, In Pursuit "
            "of Tea) are systematically Trends-thin, the very Regime 4 pattern "
            "the study tests. The chinese cell\u2019s n = 3 status does not "
            "invalidate the Regime 4 verdict (n = 23 overall well above the "
            "alignment floor; tradition control with k = 6 dummies operates per "
            "pre-reg \u00a73), but a cell-balanced sub-analysis (downsampling "
            "all cells to n = 3) is not pre-registered and can be reported as "
            "ad-hoc sensitivity if reviewer concerns warrant."
        ),
        (
            "<b>Registry coverage gap (revised).</b> v0.16 delivered on v0.14\u2019s "
            "queued registry-expansion candidates (Mariage Fr\u00e8res, Palais des "
            "Th\u00e9s, Rare Tea Company; plus Vahdam Teas, Makaibari, Kusmi Tea). "
            "New high-mention brands surfaced at v0.16 but not in the registry: "
            "What-Cha (60 mentions across 288 LLM responses), Kettl (55), Seven "
            "Cups (48), Upton Tea Imports (45), Yunomi (44), Art of Tea (38), "
            "Camellia Sinensis (36), Hibiki-an (34), Song Tea &amp; Ceramics (30). "
            "At the matched-model subset\u2019s totals these would likely enter the "
            "top-15 AI Presence ranks. They are queued for v0.16 registry-revision "
            "review per AIAS Protocol v1.2 \u00a72.4. The Regime 4 verdict is "
            "unlikely to invert under their inclusion (they amplify the specialty / "
            "Asian-tradition cluster that already drives the signature)."
        ),
        (
            "<b>Tea Box query ambiguity.</b> Carried forward from v0.14 unchanged. "
            "The pivot-rescaling Trends acquisition for the Tea Box brand captured "
            "generic-phrase search volume (\"tea box\" as gift-set descriptor) in "
            "addition to brand-specific search. The Tea Box-excluded sensitivity "
            "panel (H_Regime4_replication_knives second row in the scoring table above) "
            "addresses this directly: all three pre-registered conditions hold at "
            "n = 22 with Tea Box dropped. The primary verdict is robust; the "
            "failure mode is documented and addressed in the AIAS Protocol v1.2 "
            "specification (Phase B disambiguation step)."
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
            "<b>v0.16 \u2014 next designed-for-test category.</b> Kitchen knives now "
            "has both first-replication (v0.14) and panel-expansion-robustness "
            "(v0.16) evidence; the category is sufficiently anchored for the "
            "programme to move to its next designed-for-test category. Candidate "
            "categories under consideration: specialty coffee (high fragmentation, "
            "regional-cooperative structure, Discovery vs Comparison-mode "
            "asymmetry), kitchen knives (the v0.8 Discourse-Language Knives "
            "extension; testable cross-mode), and personal-care categories where "
            "premium-tier is structurally meaningful (men\u2019s grooming, indie "
            "fragrance). Each candidate carries a different Regime-4 prediction "
            "based on Trends-coverage structure."
        ),
        (
            "<b>AIAS Presence Measurement Protocol v1.2 published.</b> The "
            "methodological notes paper (SSRN 6761698) formalises the Phase A / "
            "Phase B / Phase B-alternates resolution protocol with the four-"
            "regime taxonomy as canonical category-classification step. v0.16 "
            "is the first study to follow Protocol v1.2 end-to-end; the pre-"
            "registration locks Condition 2 canonical wording "
            "(<font name='Helvetica'>\u03c1</font>(AI Presence, Trends), not "
            "<font name='Helvetica'>\u03c1</font>(AI Presence, age)) per "
            "Protocol \u00a73.4. Subsequent AIAS studies inherit the protocol "
            "directly."
        ),
        (
            "<b>Cross-version panel-expansion robustness as a programme "
            "convention.</b> v0.16 is the first panel-expansion robustness study "
            "in the AIAS programme. The two-claim structure \u2014 H_Regime4_"
            "robustness + H_Discourse_Language_carryforward together \u2014 generalises to any "
            "category where an initial finding (vN) is being tested under "
            "registry expansion (vN+1): does the regime verdict survive AND do "
            "the rankings remain stable on the overlap. Future programme phases "
            "may adopt this two-claim structure as a standard robustness check."
        ),
        (
            "<b>Phase 4 (AIAS components 2\u20136).</b> Construct validity "
            "established for AI Presence across v0.11\u2013v0.16 is the "
            "precondition for measurement work on the five remaining AIAS "
            "components: Ranking, Consistency, Coverage, Grounding, Sentiment. "
            "The four-regime taxonomy now anchored across three categories "
            "(skincare, finance, kitchen knives) plus one panel-expansion-robustness "
            "datapoint (kitchen knives v0.16) suggests each component will require "
            "its own per-category construct-validity profile rather than a "
            "uniform cross-category correlation with any single external proxy."
        ),
        (
            "<b>External brand-tracking validation (Phase 3).</b> The construct-"
            "validity claim against external brand-tracking data (Kantar BrandZ, "
            "YouGov BrandIndex, brand health tracker panels) will sharpen the "
            "single-validator finding into a multi-validator finding. The four-"
            "regime taxonomy provides pre-registered predictions: brands in "
            "Regime 1 should show stronger AI Presence \u00d7 brand-tracking "
            "correlation than brands in Regime 4. Kitchen knives v0.14 + v0.16 "
            "establish the Regime 4 baseline against which the cross-validator "
            "test will be calibrated."
        ),
        (
            "<b>Tri-System Brand Growth framework cross-citation.</b> The Tri-"
            "System framework (Marketing Science Institute Working Paper) will "
            "cite v0.16 as empirical evidence of Regime 4 panel-expansion "
            "robustness. The MSI WP bibliography will incorporate v0.13, v0.14, "
            "v0.16, and AIAS Protocol v1.2 (SSRN 6761698) as the empirical "
            "anchors for the framework\u2019s AI Availability axis."
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
            "OSF project ec6wh, /v16/. Inputs: fresh LLM acquisition (288 calls "
            "across two waves on six-LLM panel \u2014 Anthropic Sonnet 4.6, "
            "Anthropic Opus 4.7, OpenAI gpt-5.4-mini, OpenAI gpt-5.5, Google "
            "gemini-2.5-flash, xAI grok-4-1-fast-reasoning, status = ok); Google "
            "Trends raw responses (6 bundles \u00d7 2 regions \u00d7 14-day "
            "combined window, locked at acquisition timestamp "
            "2026-05-14T17:58:35Z); Phase A pivot validation inherited from "
            "v0.14 (Victorinox, mean 88.14, CV 9.13%); Phase B topic-ID resolution "
            "with three chinese-cell alternates tested in a single pass; premium "
            "tea v0.16 registry (brands_kitchen_knives.json, v4 schema, 28 primaries "
            "+ 3 alternates organised by tradition: chinese 8, japanese 4, "
            "british 6, indian 4, us_specialty 5, french 4); brand-age verified "
            "table; scoring outputs (canonical_scoring.json, per_brand_"
            "paired.csv, h_regime4_robustness.csv, h_coverage_closure.csv, "
            "h7_regime_classification.csv); 5 chart PDFs (regime4 canonical, "
            "per-category rho comparison, primary vs sensitivity, per-brand "
            "scatter, per-tradition small-multiples); build scripts; this report; "
            "and the matching SSRN working paper."
        ),
        (
            "Companion SSRN working paper (Gonzalez Castro 2026, SSRN 6768059, "
            "https://ssrn.com/abstract=6768059). Cross-references: AI Availability foundational "
            "paper (SSRN 6659000); AIAS Presence Measurement Protocol v1.1 "
            "(SSRN 6722319); AIAS Presence Measurement Protocol v1.2 (SSRN "
            "6761698); v0.6 Cross-Category Findings (SSRN 6720959); v0.7 "
            "Phantom-Brand Persistence Phase 2 BBB (SSRN 6721779); v0.8 "
            "Discourse-Language Knives (SSRN 6728000); v0.9 Longitudinal "
            "Re-Baseline (SSRN 6736878); v0.10 Naive-Phantom Rate Stability "
            "(SSRN 6741163); v0.11 PM Software \u00d7 Trends Construct Validity "
            "Pilot (SSRN 6745040); v0.12 Three Empirical Regimes (SSRN 6748341); "
            "v0.13 Four Empirical Regimes \u2014 Five-Category Construct-"
            "Validity Expansion (SSRN 6750498); v0.14 Kitchen Knives \u2014 "
            "Regime 4 Replication (SSRN 6755621)."
        ),
    ],
    "methodology_log": (
        "v0.16 follows AIAS Presence Measurement Protocol v1.2 (SSRN 6761698). "
        "Pre-registration locked at git tag v0.16-prereg (commit 511e339) on "
        "13 May 2026 UTC prior to LLM acquisition. Trends acquisition session "
        "UTC timestamp 2026-05-14T17:58:35Z, single combined 14-day window "
        "covering both wave windows (t<sub>1</sub>: April 27 \u2013 May 3, "
        "2026; t<sub>2</sub>: May 4 \u2013 May 10, 2026). DEVIATIONS.md "
        "Entry 1 documents bare-canonical Phase B query methodology carried "
        "forward from v0.14 (inherited methodology, not a v0.16 deviation); "
        "Entry 2 documents the chinese-cell alternate exhaustion (pre-"
        "registered alternate-activation rule was followed completely; five of "
        "eight chinese candidates failed Phase B; cell stops at n = 3 eligible). "
        "No pre-registered hypothesis, threshold, or routing rule was modified. "
        "The canonical scoring script (score_v16.py) is locked at git commit "
        "511e339 (same as pre-reg tag)."
    ),
}
