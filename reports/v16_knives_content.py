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
# V16_CONTENT_REWRITE_PATTERNS_SCORING_DETAILS — rewrite applied 2026-05-18
# V16_BACK_MATTER_REWRITE — rewrite applied 2026-05-18
# V16_WHAT_WE_MEASURED_STUB — rewrite applied 2026-05-18
# V16_FRONT_MATTER_REWRITE — rewrite applied 2026-05-18
# V16_PATTERNS_STUB_CHART_FIRST — patterns 3-5 use chart-then-text layout

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
    "v0.16 brings AIAS Protocol v1.2 to the kitchen-knives substrate, "
    "completing the v0.8 Discourse-Language Knives lineage (SSRN "
    "6728000). Two pre-registered hypotheses, two verdicts: "
    "<b>H_Regime4_replication_knives PARTIAL</b> on the worldwide primary "
    "panel; <b>H_Discourse_Language_carryforward CARRY-FORWARD CONFIRMED</b> "
    "on the Japanese tradition cell. The US/worldwide divergence surfaces "
    "the same brand-asymmetry through a second aperture."
)

LEAD_DECK = (
    "Two pre-registered hypotheses tested at a single measurement wave "
    "(t<sub>1</sub>: 2026-04-27 to 2026-05-03; t<sub>2</sub>: 2026-05-04 "
    "to 2026-05-10). "
    "<b>H_Regime4_replication_knives PARTIAL</b> on the worldwide primary "
    "panel \u2014 n = 13 eligible brands; bivariate Spearman "
    "<font name='Helvetica'>\u03c1</font>(AI Presence, Google Trends) = "
    "+0.022 at t<sub>1</sub> and +0.003 at t<sub>2</sub> (both well within "
    "C2 threshold |<font name='Helvetica'>\u03c1</font>| < 0.35); partial "
    "<font name='Helvetica'>\u03c1</font> after brand_age + tradition_cell "
    "control (k = 5 dummies per pre-reg \u00a73) = +0.101 at t<sub>1</sub> "
    "and +0.080 at t<sub>2</sub> (both fail C3 partial "
    "<font name='Helvetica'>\u03c1</font> < 0). Per pre-reg \u00a72: PARTIAL "
    "is 'conditions (1) and (2) hold but (3) fails \u2014 non-saturated "
    "weak signature; productive boundary finding.' "
    "<b>H_Discourse_Language_carryforward CARRY-FORWARD CONFIRMED</b> on the "
    "Japanese tradition cell (Shun, Global, Miyabi, Mac, Tojiro, "
    "Yoshihiro; n = 6): Spearman "
    "<font name='Helvetica'>\u03c1</font>(English-prompt AI Presence, "
    "Japanese-prompt AI Presence) = +0.197 at t<sub>1</sub> and "
    "\u22120.149 at t<sub>2</sub> \u2014 both far below the 0.85 "
    "CARRY-FORWARD CONFIRMED threshold. The v0.8 finding survives "
    "v1.2 protocol with corrected eligibility filtering. The pre-registered "
    "US-region cell sits below the inferential n = 12 floor (n = 10 at "
    "both waves; three brands \u2014 G\u00fcde, Sunlong, Au Nain \u2014 "
    "drop out because their US-region Trends signal is at the 14-day-zero "
    "floor) and reads strongly negative as descriptive sensitivity: "
    "bivariate <font name='Helvetica'>\u03c1</font> = \u22120.881 / "
    "\u22120.812; partial <font name='Helvetica'>\u03c1</font> = "
    "\u22120.940 / \u22120.708. The US/worldwide divergence is the same "
    "underlying brand-asymmetry surfacing via registry coverage rather "
    "than via prompt language."
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
        "recommendation prompts, measured against Google Trends rank as "
        "the consumer-search reference. v0.16 brings the v1.2-formalized "
        "construct-validity panel to the kitchen-knives substrate, "
        "completing a programme arc that began in v0.8 Discourse-Language "
        "Knives (SSRN 6728000). The v0.16 brand panel comprises 22 non-"
        "pivot brands stratified across five tradition cells: japanese, "
        "german, french, american-specialty, and chinese, with Victorinox "
        "as panel pivot (replaced by W\u00fcsthof in Phase A pivot "
        "fallback per pre-reg \u00a76; DEVIATIONS Entry 3). Two pre-"
        "registered hypotheses tested at a single measurement wave."
    ),
    (
        "<b>H_Regime4_replication_knives PARTIAL.</b> The pre-registered "
        "primary panel (worldwide region, n = 13 eligible brands) satisfies "
        "two of three Regime 4 conditions and fails the third. C1 (n "
        "\u2265 12): satisfied, n = 13 at both waves. C2 (|bivariate "
        "<font name='Helvetica'>\u03c1</font>(AI Presence, Trends)| < "
        "0.35): satisfied with substantial margin, "
        "<font name='Helvetica'>\u03c1</font> = +0.022 at t<sub>1</sub> "
        "and +0.003 at t<sub>2</sub>. C3 (partial "
        "<font name='Helvetica'>\u03c1</font>(AI, Trends | age, tradition) "
        "< 0): fails, partial <font name='Helvetica'>\u03c1</font> = "
        "+0.101 at t<sub>1</sub> and +0.080 at t<sub>2</sub>. Per pre-reg "
        "\u00a72, PARTIAL is the verdict tier for this combination: "
        "'conditions (1) and (2) hold but (3) fails \u2014 non-saturated "
        "weak signature; productive boundary finding. v0.16 refinement of "
        "v0.15's binary structure; strict sub-classification of "
        "v0.15-canonical FALSIFIED, not a contradiction.' The Regime 4 "
        "cluster remains at three confirmed substrates (premium facial "
        "skincare v0.11, personal finance apps v0.13, premium tea v0.14/"
        "v0.15); kitchen knives at v0.16 lands as a productive boundary "
        "finding for the regime's identity-load and discourse-language "
        "boundaries."
    ),
    (
        "<b>H_Discourse_Language_carryforward CARRY-FORWARD CONFIRMED.</b> "
        "v0.8 (SSRN 6728000) surfaced the Discourse-Language Bias on "
        "knives before the v1.2 construct-validity eligibility panel "
        "existed. v0.16 tests whether the original finding survives v1.2 "
        "protocol with corrected eligibility filtering, computed on the "
        "Japanese tradition cell as anchor cell. Per-brand AI Presence "
        "under an English-language prompt is rank-correlated with "
        "per-brand AI Presence under the equivalent Japanese-language "
        "prompt across the six Japanese-cell brands (Shun, Global, "
        "Miyabi, Mac, Tojiro, Yoshihiro). Pre-registered conditions: "
        "n_japanese \u2265 5 AND Spearman "
        "<font name='Helvetica'>\u03c1</font>(English, native-language) "
        "< 0.85 at both waves. Result: n = 6; Spearman "
        "<font name='Helvetica'>\u03c1</font><sub>t<sub>1</sub></sub> = "
        "+0.197; <font name='Helvetica'>\u03c1</font><sub>t<sub>2</sub>"
        "</sub> = \u22120.149. Both correlations sit far below the 0.85 "
        "CARRY-FORWARD CONFIRMED threshold, with t<sub>2</sub> actually "
        "slightly negative. The brands the LLM panel surfaces when "
        "prompted in English are not the same brands it surfaces when "
        "prompted in Japanese, even within the same six-brand Japanese "
        "tradition cell. The v0.8 finding survives v1.2 protocol \u2014 "
        "now documented under canonical eligibility filtering with full "
        "pre-registration and OSF transparency."
    ),
    (
        "<b>US/worldwide divergence \u2014 the same asymmetry, a second "
        "aperture.</b> Pre-reg \u00a72 specifies the worldwide-region "
        "panel as primary and the US-region panel as descriptive "
        "sensitivity when n < 12. v0.16's US panel sits below that floor "
        "(n = 10 at both waves) because three brands \u2014 G\u00fcde "
        "(German tradition), Sunlong (Chinese tradition), and Au Nain "
        "(French tradition) \u2014 fall out of US-region Trends "
        "eligibility: their US-region Google Trends signal sits at or "
        "near the 14-day-zero floor, while their worldwide signal "
        "supports eligibility. Descriptive correlations on the US panel "
        "read strongly negative: bivariate "
        "<font name='Helvetica'>\u03c1</font> = \u22120.881 at t<sub>1"
        "</sub> and \u22120.812 at t<sub>2</sub>; partial "
        "<font name='Helvetica'>\u03c1</font> = \u22120.940 and "
        "\u22120.708 after the same covariate control. The worldwide "
        "panel reads near-zero bivariate correlation; the US panel reads "
        "strongly negative. This divergence is not a methodological "
        "artifact \u2014 it is the same brand-asymmetry that "
        "H_Discourse_Language_carryforward surfaces via prompt language, "
        "appearing here via registry coverage. Foreign-tradition brands "
        "generate worldwide AI Presence but produce US-region Trends "
        "signal at or near floor; the panel composition shifts when the "
        "Trends aperture narrows from worldwide to US."
    ),
    (
        "<b>What v0.16 adds to the AIAS programme.</b> v0.16 completes "
        "the v0.8 discourse-language lineage under canonical v1.2 "
        "protocol \u2014 the finding is no longer a one-paper "
        "observation; it is documented with construct-validity "
        "eligibility, pre-registration discipline (tag v0.16-prereg at "
        "commit 511e339), and full OSF data transparency. The Regime 4 "
        "verdict for kitchen knives lands at PARTIAL rather than "
        "CONFIRMED \u2014 a productive boundary finding for the regime's "
        "identity-load and discourse-language boundaries rather than a "
        "fourth-substrate canonical confirmation. The AIAS Presence "
        "Measurement Protocol v1.2 (SSRN 6761698) carries the methodology; "
        "Phase 4 will extend measurement to the remaining five Presence "
        "components (Ranking, Consistency, Coverage, Grounding, "
        "Sentiment), at which point the v0.16 kitchen-knives baseline "
        "becomes useful for cross-component comparison. The Tri-System "
        "Brand Growth framework (MSI Working Paper) will cite v0.16 as "
        "empirical evidence of Regime 4 identity-load boundary behaviour."
    ),
]

# ----------------------------------------------------------------------------
# WHAT WE MEASURED
# ----------------------------------------------------------------------------

WHAT_WE_MEASURED = {
    "heading": "What We Measured",
    "paragraphs": [
        (
            "v0.16 measures AI Presence for kitchen-knife brands across "
            "six LLM slots (Anthropic Sonnet 4.6, Anthropic Opus 4.7, "
            "OpenAI gpt-5.4-mini, OpenAI gpt-5.5, Google gemini-2.5-flash, "
            "xAI grok-4-1-fast-reasoning) on category-recommendation prompts, "
            "and compares it against Google Trends rank as the consumer-"
            "search reference. Two waves at the canonical 14-day inter-wave "
            "spacing (t<sub>1</sub>: April 27 \u2013 May 3, 2026; "
            "t<sub>2</sub>: May 4 \u2013 May 10, 2026). The full "
            "acquisition produced 960 cells (20 prompts \u00d7 6 model "
            "slots \u00d7 8 runs); all enriched at function-calling "
            "extraction with no errors."
        ),
        (
            "<b>Brand panel.</b> v0.16 registry (<font name=\'Helvetica\'>"
            "brands_kitchen_knives_v0.16.json</font>) covers five tradition "
            "cells: <b>japanese</b> (Shun, Global, Miyabi, Mac, Tojiro, "
            "Yoshihiro; n = 6); <b>german</b> (W\u00fcsthof as pivot after "
            "Victorinox fallback, Zwilling J.A. Henckels, Messermeister, "
            "G\u00fcde, Friedr. Dick; n = 5 primaries); <b>french</b> "
            "(Sabatier, Opinel, Laguiole, Nogent + Au Nain activated from "
            "alternates; n = 4 after activation); <b>american</b> (Cutco, "
            "Dalstrong, Misen, New West KnifeWorks, Made In; n = 5); "
            "<b>chinese</b> (Sunlong, ZHEN + Hengtai activated from "
            "alternates; n = 3 after primary-brand topic-ID failures and "
            "alternate-pool exhaustion). Phase B excluded brands documented "
            "in OSF deposit phase_b_resolution.csv."
        ),
        (
            "<b>Pivot, Phase A fallback.</b> Victorinox was the pre-"
            "registered Phase A pivot but EXCLUDED_E1a at validation "
            "(kitchen-knife brand presence below Trends-eligibility floor "
            "on bare canonical query). W\u00fcsthof activated as pivot per "
            "pre-reg \u00a76 contingency; DEVIATIONS Entry 3 documents the "
            "operational handling. The pivot supplies the per-region Trends "
            "rescale baseline against which all other brands\u2019 Trends "
            "signals are normalized."
        ),
        (
            "<b>Eligibility resolution.</b> n = 13 eligible brands at the "
            "worldwide-region cell at both waves (Tojiro, Yoshihiro, "
            "Zwilling J.A. Henckels, Messermeister, G\u00fcde, Sabatier, "
            "Opinel, Laguiole, Cutco, Dalstrong, Sunlong, ZHEN, Au Nain). "
            "The pre-registered US-region cell sits at n = 10 (G\u00fcde, "
            "Sunlong, Au Nain fall to 14-day-zero Trends floor; see Pattern "
            "1 closing paragraph). The Japanese tradition cell at n = 6 "
            "supports the H_Discourse_Language_carryforward hypothesis on "
            "the original v0.8 anchor cell."
        ),
        (
            "<b>Hypothesis evaluation.</b> All pre-registered conditions and "
            "thresholds locked at git tag <font name=\'Helvetica\'>"
            "v0.16-prereg</font> (commit <font name=\'Helvetica\'>511e339"
            "</font>, 16 May 2026 UTC). Worldwide-region cell is the "
            "inferential primary; US-region is descriptive sensitivity per "
            "pre-reg \u00a72 (n falls below the n = 12 inferential floor). "
            "All Spearman correlations are computed on per-brand rank data; "
            "partial correlations control for brand_age (continuous, rank-"
            "transformed) and tradition_cell (categorical dummies, k_adj = 5 "
            "for the five-cell panel). Full per-brand inputs are deposited in "
            "the OSF project at /v16/analysis/per_brand_paired.csv; full "
            "scoring outputs at /v16/analysis/canonical_scoring.json. "
            "Substantive measurement notes \u2014 acquisition error "
            "handling, network-cascade recovery sequence, enrichment "
            "function-calling provider \u2014 are developed in the companion "
            "SSRN working paper."
        ),
    ],
}

# ----------------------------------------------------------------------------
# FINDINGS (PATTERNS)
# ----------------------------------------------------------------------------

PATTERNS = [
    {
        "number": 1,
        "title": "H_Regime4_replication_knives PARTIAL \u2014 bivariate decoupling holds; conservative test fails",
        "chart_slot": "f1_regime4_canonical",
        "n_lead": 2,
        "paragraphs": [
            (
                "<b>This is the v0.16 primary pre-registered hypothesis.</b> "
                "Premium facial skincare (v0.11), personal finance apps (v0.13), "
                "and premium tea (v0.14, v0.15) constitute the current three-"
                "substrate Regime 4 (Covariate-saturated weak) empirical "
                "foundation. v0.16 tests Regime 4 replication on a fourth "
                "substrate \u2014 kitchen knives \u2014 a substrate that "
                "previously surfaced a related finding under v0.8\u2019s "
                "Discourse-Language Bias measurement (SSRN 6728000), before "
                "the construct-validity panel and four-regime taxonomy were "
                "formalized. The pre-registered conditions evaluate at "
                "<b>PARTIAL</b> at the worldwide primary panel, with the US "
                "descriptive sensitivity reading divergent in direction \u2014 "
                "a substantive result discussed in the closing paragraph."
            ),
            (
                "<b>The three pre-registered conditions: two satisfied, one "
                "failed.</b> <b>C1 (n \u2265 12):</b> n = 13 eligible brands "
                "at both waves \u2014 above the floor by one brand. <b>C2 "
                "(|bivariate <font name='Helvetica'>\u03c1</font>(AI Presence, "
                "Trends)| &lt; 0.35):</b> <font name='Helvetica'>\u03c1</font> "
                "= +0.022 at t<sub>1</sub> and +0.003 at t<sub>2</sub> "
                "\u2014 both well within the threshold, with substantial "
                "margin. <b>C3 (partial <font name='Helvetica'>\u03c1</font>"
                "(AI, Trends | brand_age, tradition_cell) &lt; 0):</b> partial "
                "<font name='Helvetica'>\u03c1</font> = +0.101 at t<sub>1</sub> "
                "and +0.080 at t<sub>2</sub> \u2014 both fail the C3 condition "
                "(positive rather than negative). Per pre-reg \u00a72 decision "
                "rules: <b>PARTIAL</b>."
            ),
            (
                "<b>What PARTIAL means.</b> v0.16 pre-registration introduces "
                "PARTIAL as a verdict tier distinct from FALSIFIED, refining "
                "v0.15\u2019s binary structure (the v0.15 pre-reg would have "
                "collapsed this outcome to FALSIFIED). The PARTIAL verdict "
                "names a specific substantive pattern: the central Regime 4 "
                "diagnostic \u2014 bivariate decoupling between AI Presence and "
                "Trends \u2014 holds (Condition 2 satisfied), but the residual "
                "association after controlling for brand age and tradition-cell "
                "membership does not deepen into the negative-partial signature "
                "Regime 4 produces in skincare, finance, and tea. Per pre-reg: "
                "a <i>non-saturated weak signature</i>; a productive boundary "
                "finding rather than a confirmation or a falsification."
            ),
            (
                "<b>The US descriptive sensitivity reads divergently \u2014 "
                "and strongly negative.</b> The pre-registered US-region panel "
                "falls below the inferential n = 12 floor (n = 10 at both "
                "waves; per pre-reg \u00a72 this is descriptive sensitivity, "
                "not a parallel verdict). But the correlation magnitudes are "
                "striking: bivariate <font name='Helvetica'>\u03c1</font> = "
                "\u22120.881 at t<sub>1</sub> and \u22120.812 at t<sub>2</sub>; "
                "partial <font name='Helvetica'>\u03c1</font> = \u22120.940 "
                "and \u22120.708 after the same covariate control. The "
                "worldwide panel reads near-zero bivariate correlation; the US "
                "panel reads strongly negative. The brand composition "
                "explains the divergence: three brands drop from the US-"
                "eligible panel relative to worldwide \u2014 G\u00fcde "
                "(German), Sunlong (Chinese), and Au Nain (French) \u2014 "
                "because their US-region Google Trends signal sits at the "
                "14-day-zero floor, while their worldwide signal supports "
                "eligibility."
            ),
            (
                "<b>The US/worldwide divergence is the v0.8 finding "
                "replicating via a different measurement aperture.</b> v0.8 "
                "(SSRN 6728000) surfaced a Discourse-Language Bias on knives: "
                "non-English-anchored brands underperform in English-prompt "
                "conditions relative to discourse-language-matched conditions. "
                "v0.16\u2019s US/worldwide divergence is the same structural "
                "asymmetry surfacing via <i>registry coverage</i> rather than "
                "via prompt language: foreign-tradition brands (Japanese, "
                "German, French, Chinese) generate worldwide AI Presence but "
                "produce US-region Trends signal at or near floor. v0.16\u2019s "
                "discourse-language carryforward (Pattern 2) confirms the v0.8 "
                "finding under the original prompt-language operationalization "
                "with full v1.2 protocol discipline; the US/worldwide "
                "divergence here is the same underlying asymmetry surfacing "
                "through a second, independent measurement aperture."
            ),
        ],
    },
    {
        "number": 2,
        "title": "H_Discourse_Language_carryforward CONFIRMED \u2014 v0.8 finding survives v1.2 protocol",
        "chart_slot": "f3_discourse_language",
        "n_lead": 2,
        "paragraphs": [
            (
                "<b>This is v0.16\u2019s second pre-registered hypothesis and "
                "the direct extension of the v0.8 programme lineage.</b> "
                "v0.8 (SSRN 6728000) surfaced the Discourse-Language Bias on "
                "kitchen knives before the construct-validity eligibility "
                "panel and four-regime taxonomy of v1.2 were formalized. "
                "v0.16 tests whether the original finding survives v1.2 "
                "protocol with corrected eligibility filtering. The pre-"
                "registered verdict: <b>CARRY-FORWARD CONFIRMED</b>."
            ),
            (
                "<b>Computed on the Japanese tradition cell \u2014 the anchor "
                "cell for the v0.8 finding.</b> Six brands enter the analysis: "
                "<b>Shun, Global, Miyabi, Mac, Tojiro, Yoshihiro</b>. The "
                "test compares per-brand AI Presence ranks under an English-"
                "language prompt versus the equivalent Japanese-language "
                "prompt on the same six brands. Pre-registered conditions: "
                "n_japanese \u2265 5 AND Spearman <font name='Helvetica'>"
                "\u03c1</font>(English-prompt AI Presence, native-language-"
                "prompt AI Presence) &lt; 0.85 at both waves."
            ),
            (
                "<b>Both pre-registered conditions met with substantial margin."
                "</b> n_japanese = 6 (above the floor of 5). Spearman "
                "<font name='Helvetica'>\u03c1</font><sub>t<sub>1</sub></sub> "
                "= 0.197; <font name='Helvetica'>\u03c1</font><sub>t<sub>2"
                "</sub></sub> = \u22120.149. Both correlations sit far below "
                "the CONFIRMED threshold of 0.85, with t<sub>2</sub> actually "
                "going slightly negative. The brands the LLM panel surfaces "
                "when prompted in English are not the same brands (in the "
                "same relative ranking) it surfaces when prompted in Japanese, "
                "even within the same six-brand Japanese tradition cell."
            ),
            (
                "<b>What CONFIRMED means.</b> Pre-registration framed three "
                "verdict tiers around the 0.85 threshold and a 0.95 ceiling. "
                "CONFIRMED (&lt; 0.85): the v0.8 finding survives unchanged "
                "\u2014 prompt language materially changes which Japanese-"
                "cell brands surface, even under v1.2\u2019s stricter "
                "eligibility filtering. WEAKENED ([0.85, 0.95)): the finding "
                "would have survived at attenuated magnitude. FALSIFIED-"
                "favorable (\u2265 0.95): the v0.8 finding would have been a "
                "pre-v1.2 protocol artifact, productively retired by "
                "v1.2\u2019s eligibility correction. The v0.16 result lands "
                "in the CONFIRMED tier by substantial margin \u2014 "
                "<font name='Helvetica'>\u03c1</font><sub>t<sub>1</sub></sub> "
                "at 0.197 is less than a quarter of the 0.85 threshold."
            ),
            (
                "<b>Same underlying asymmetry, two measurement apertures.</b> "
                "Pattern 1\u2019s US/worldwide divergence and Pattern 2\u2019s "
                "discourse-language CONFIRMED are two views of the same "
                "structural property. Pattern 1 measures the asymmetry as a "
                "region-induced registry-coverage effect: US sparsity drops "
                "foreign-tradition brands from the eligible panel because "
                "their US-region Trends signal is at floor. Pattern 2 measures "
                "the asymmetry as a prompt-language-induced ranking effect: "
                "English-prompt vs Japanese-prompt rankings on the same six "
                "Japanese-cell brands diverge sharply. Both surface a "
                "structural property of AI Availability that classical brand-"
                "equity measures (Google Trends search interest) do not "
                "symmetrically capture: AI mediation for foreign-tradition "
                "brands has language and region dependencies absent from "
                "search-interest measures."
            ),
            (
                "<b>The v0.8 lineage is now methodologically closed.</b> "
                "v0.8 surfaced the discourse-language finding before v1.2 "
                "protocol existed. v0.16 reproduces the finding under "
                "v1.2\u2019s construct-validity panel, with canonical "
                "eligibility filtering, canonical pre-registration discipline "
                "(tag v0.16-prereg at commit 511e339), and full data "
                "transparency via OSF deposit. The Discourse-Language "
                "Carryforward is no longer a one-paper observation; it is "
                "documented under canonical protocol, available for future "
                "AIAS programme work that implicates AI Availability\u2019s "
                "language and region dependencies."
            ),
        ],
    },
    {
        "number": 3,
        "title": "Phase A pivot fallback \u2014 Victorinox EXCLUDED_E1a; Wüsthof activated",
        "chart_slot": "f5_per_tradition",
        "chart_after_text": False,
        "n_lead": 1,
        "paragraphs": [
            (
                "<b>Substantive analysis deferred.</b> v0.16 Phase A pivot "
                "validation surfaced Victorinox EXCLUDED_E1a; Wüsthof "
                "activated as pivot per pre-reg \u00a76 contingency. "
                "DEVIATIONS Entry 3 documents the operational handling. The "
                "substantive analysis of the pivot fallback \u2014 including "
                "Victorinox\u2019s prominence as the most-mentioned brand in "
                "LLM responses (n = 417 unknown mentions across 960 panel "
                "responses) and the methodological implications for Phase A "
                "pivot-validation criteria in future categories \u2014 will "
                "be developed in the v0.16 SSRN working paper and a v1.3 "
                "Protocol methodology increment. Brand-format report content "
                "deferred to that work."
            ),
        ],
    },
    {
        "number": 4,
        "title": "Alternate activation \u2014 Au Nain (French), Hengtai (Chinese)",
        "chart_slot": "f5_per_tradition",
        "chart_after_text": False,
        "n_lead": 1,
        "paragraphs": [
            (
                "<b>Substantive analysis deferred.</b> v0.16 Phase B surfaced "
                "primary-brand topic-ID failures in the French cell (Au Nain "
                "activated from alternates) and the Chinese cell (Hu Si Chao "
                "and Dengjia both EXCLUDED_E1a; Hengtai activated). The "
                "Chinese cell collapses to n = 3 (Sunlong, ZHEN, Hengtai) "
                "after alternate-pool exhaustion \u2014 retained for "
                "descriptive reporting per pre-reg \u00a76 cell-collapse "
                "contingency. DEVIATIONS Entry 4 documents the full "
                "operational sequence. The substantive analysis of why "
                "Chinese-cell brands fail Phase B at higher rates than other "
                "cells, and the implications for AI Availability measurement "
                "in tradition cells with under-represented English-language "
                "search interest, will be developed in the SSRN paper."
            ),
        ],
    },
    {
        "number": 5,
        "title": "Cross-version comparability \u2014 v0.16 as v0.8 carryforward",
        "chart_slot": "f2_per_category",
        "chart_after_text": False,
        "n_lead": 1,
        "paragraphs": [
            (
                "<b>Substantive analysis deferred.</b> v0.16 is the v1.2-"
                "protocol carryforward of v0.8 (SSRN 6728000), not an "
                "independent fourth-substrate Regime 4 confirmation. The "
                "Regime 4 cluster remains at three confirmed substrates "
                "(premium facial skincare, personal finance apps, premium "
                "tea); kitchen knives v0.16 lands at PARTIAL, a productive "
                "boundary finding for the regime\u2019s identity-load and "
                "discourse-language boundaries. The chart at right places "
                "kitchen knives v0.16 on the canonical four-regime "
                "classification axes alongside the v0.13 cohort. Full "
                "cross-version comparison \u2014 v0.8 (pre-v1.2) vs v0.16 "
                "(v1.2-canonical) on the kitchen-knives substrate, including "
                "construct-validity panel differences and eligibility-"
                "filtering effects \u2014 will be developed in the SSRN paper."
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
        "Two pre-registered hypotheses; all thresholds and decision rules "
        "locked at v0.16-prereg (tag <font name='Helvetica'>v0.16-prereg</font>, "
        "commit <font name='Helvetica'>511e339</font>, 16 May 2026) prior to any "
        "LLM acquisition or Google Trends acquisition call against the wave "
        "windows. Per pre-reg \u00a72, the primary panel is the worldwide-"
        "region cell at both waves; the US-region cell is descriptive "
        "sensitivity (falls below the n = 12 inferential floor at v0.16). "
        "Construct-validity diagnostics from earlier-version programme "
        "convention (H1\u2013H7 carry-forward at v0.13\u2013v0.15) are not "
        "shown in this scoring table because they are not pre-registered for "
        "v0.16; descriptive content where relevant appears in Patterns 1\u20135."
    ),
    "rows": [
        ("H_Regime4_replication_knives (primary, worldwide)",
         "n \u2265 12 AND |bivariate <font name='Helvetica'>\u03c1</font>(AI, "
         "Trends)| &lt; 0.35 AND partial <font name='Helvetica'>\u03c1</font>"
         "(AI, Trends | age, tradition) &lt; 0; both waves",
         "n = 13 (both waves); bivariate <font name='Helvetica'>\u03c1</font> "
         "= +0.022 / +0.003; partial <font name='Helvetica'>\u03c1</font> "
         "= +0.101 / +0.080 \u2014 C1 and C2 satisfied; C3 fails (positive "
         "rather than negative)",
         "PARTIAL", "partial"),
        ("H_Regime4_replication_knives (descriptive, US)",
         "Same three conditions on US-region cell; descriptive sensitivity "
         "only (n falls below inferential floor)",
         "n = 10 (both waves; below C1 floor); bivariate <font name='Helvetica'>"
         "\u03c1</font> = \u22120.881 / \u22120.812; partial <font name='Helvetica'>"
         "\u03c1</font> = \u22120.940 / \u22120.708 \u2014 descriptive only per "
         "pre-reg \u00a72",
         "DESCRIPTIVE", "descriptive"),
        ("H_Discourse_Language_carryforward",
         "n_japanese \u2265 5 AND <font name='Helvetica'>\u03c1</font>(English-"
         "prompt AI Presence, native-language-prompt AI Presence) &lt; 0.85; "
         "both waves; Japanese tradition cell",
         "n = 6; <font name='Helvetica'>\u03c1</font><sub>t<sub>1</sub></sub> "
         "= +0.197; <font name='Helvetica'>\u03c1</font><sub>t<sub>2</sub></sub> "
         "= \u22120.149 \u2014 both far below 0.85 threshold",
         "CARRY-FORWARD CONFIRMED", "confirmed"),
    ],
}

# ----------------------------------------------------------------------------
# HYPOTHESIS DETAILS (per-hypothesis expansion below the scoring table)
# ----------------------------------------------------------------------------

HYPOTHESIS_DETAILS = {
    "heading": "Hypothesis Details",
    "intro": (
        "Per-hypothesis claim, operationalisation, and result. Both "
        "hypotheses pre-registered at <font name='Helvetica'>v0.16-prereg</font> "
        "(commit <font name='Helvetica'>511e339</font>, 16 May 2026). "
        "Decision-rule language and threshold values quoted verbatim from "
        "the pre-registration."
    ),
    "items": [
        ("H_Regime4_replication_knives",
         "<b>Primary hypothesis (v0.16).</b> Brand AI Presence on the kitchen-"
         "knives substrate is tested for the canonical Regime 4 (Covariate-"
         "saturated weak) signature established on premium facial skincare "
         "(v0.11), personal finance apps (v0.13), and premium tea (v0.14, "
         "v0.15). Three conditions tested at both worldwide waves: <b>(C1)"
         "</b> n \u2265 12 eligible brands; <b>(C2)</b> |bivariate "
         "<font name='Helvetica'>\u03c1</font>(AI Presence, Trends)| &lt; "
         "0.35; <b>(C3)</b> partial <font name='Helvetica'>\u03c1</font>(AI "
         "Presence, Trends | brand_age, tradition_cell) &lt; 0. Controls in "
         "C3 partial correlation: brand_age (continuous, rank-transformed) "
         "+ tradition_cell (categorical dummies, k_adj = 5). Result: n = 13; "
         "bivariate <font name='Helvetica'>\u03c1</font> = +0.022 / +0.003 "
         "(within C2 threshold); partial <font name='Helvetica'>\u03c1</font> "
         "= +0.101 / +0.080 (positive, fails C3). <b>PARTIAL</b>. Per pre-"
         "reg \u00a72 decision rules: 'Conditions (1) and (2) hold but (3) "
         "fails (positive partial after controls) \u2014 non-saturated weak "
         "signature; productive boundary finding.'"),
        ("H_Regime4_replication_knives \u2014 US descriptive sensitivity",
         "<b>Pre-registered US-region cell, descriptive only.</b> The US-"
         "region subset of the panel sits below the C1 inferential floor "
         "(n = 10 at both waves; three brands \u2014 G\u00fcde, Sunlong, "
         "Au Nain \u2014 drop from US eligibility because their US-region "
         "Trends signal is at 14-day-zero floor). Per pre-reg \u00a72, US "
         "below n = 12 is a descriptive sensitivity panel, not a parallel "
         "verdict. Magnitudes reported here as descriptive observation: "
         "bivariate <font name='Helvetica'>\u03c1</font> = \u22120.881 / "
         "\u22120.812; partial <font name='Helvetica'>\u03c1</font> = "
         "\u22120.940 / \u22120.708. The worldwide-vs-US correlation "
         "magnitude divergence is itself a substantive finding (see Pattern "
         "1 closing paragraph) \u2014 the same brand-asymmetry that "
         "Pattern 2\u2019s prompt-language test surfaces, replicating via "
         "registry coverage rather than via prompt language."),
        ("H_Discourse_Language_carryforward",
         "<b>Exploratory hypothesis (v0.16), v0.8 lineage carryforward.</b> "
         "Tests whether the v0.8 Discourse-Language Bias finding on knives "
         "(SSRN 6728000) survives v1.2 protocol with corrected eligibility "
         "filtering. Computed on the Japanese tradition cell (anchor cell "
         "for the v0.8 finding): per-brand AI Presence under English-"
         "language prompt vs equivalent Japanese-language prompt, rank-"
         "correlated across the six Japanese-cell brands (Shun, Global, "
         "Miyabi, Mac, Tojiro, Yoshihiro). Pre-registered conditions: "
         "n_japanese \u2265 5 AND Spearman <font name='Helvetica'>\u03c1"
         "</font>(English, native-language) &lt; 0.85, both waves. Result: "
         "n = 6; <font name='Helvetica'>\u03c1</font><sub>t<sub>1</sub></sub> "
         "= +0.197; <font name='Helvetica'>\u03c1</font><sub>t<sub>2</sub>"
         "</sub> = \u22120.149. Both far below the 0.85 threshold. "
         "<b>CARRY-FORWARD CONFIRMED</b>. Per pre-reg \u00a72: 'the v0.8 "
         "finding survives v1.2 protocol with corrected eligibility "
         "filtering.'"),
    ],
}

# ----------------------------------------------------------------------------
# LIMITATIONS
# ----------------------------------------------------------------------------

LIMITATIONS = {
    "heading": "Limitations",
    "paragraphs": [
        (
            "<b>Single substrate at v0.16.</b> v0.16 tests kitchen knives as "
            "the fourth-substrate Regime 4 test and the v0.8 discourse-"
            "language carryforward. The Regime 4 cluster\u2019s cross-"
            "substrate confirmations (premium facial skincare v0.11, "
            "personal finance apps v0.13, premium tea v0.14/v0.15) supply "
            "the cross-substrate triangulation; v0.16\u2019s PARTIAL verdict "
            "documents the regime\u2019s identity-load boundary at the "
            "kitchen-knives substrate rather than extending the canonical "
            "cluster."
        ),
        (
            "<b>Two-wave short window.</b> Both waves are within 14 days "
            "(t<sub>1</sub>: April 27 \u2013 May 3, 2026; t<sub>2</sub>: "
            "May 4 \u2013 May 10, 2026). Cross-wave stability of the "
            "Regime 4 signature at month-to-month or quarter-to-quarter "
            "horizons is not tested at v0.16."
        ),
        (
            "<b>Six-LLM panel at status = ok.</b> AI Presence is computed "
            "across six LLM slots (Anthropic Sonnet 4.6, Anthropic Opus 4.7, "
            "OpenAI gpt-5.4-mini, OpenAI gpt-5.5, Google gemini-2.5-flash, "
            "xAI grok-4-1-fast-reasoning) at status = ok. The six-slot "
            "panel factors variation across providers but does not "
            "decompose it. Per-model AI Presence breakdowns are available "
            "in the OSF deposit\u2019s analysis directory."
        ),
        (
            "<b>Single external validator (Google Trends).</b> Construct "
            "validity is tested against Google Trends as sole external "
            "consumer-search reference. A multi-validator design "
            "(simultaneous search interest, social-media mentions, retail "
            "sales data, consumer-survey aided recall) is the medium-term "
            "goal of the AIAS programme Phase 3."
        ),
        (
            "<b>US-region panel below inferential floor.</b> The pre-"
            "registered US-region cell sits at n = 10 at both waves \u2014 "
            "below the inferential n = 12 floor. Three brands (G\u00fcde, "
            "Sunlong, Au Nain) fall out of US eligibility at the 14-day-"
            "zero Trends floor. The strongly-negative US correlations "
            "(bivariate \u22120.881 / \u22120.812; partial \u22120.940 / "
            "\u22120.708) are reported as descriptive sensitivity per pre-"
            "reg \u00a72, not as a parallel verdict. The US/worldwide "
            "divergence is itself a substantive finding (Pattern 1 closing "
            "paragraph), but cannot be inferentially generalised at v0.16 "
            "without panel expansion adding US-eligible foreign-tradition "
            "brands."
        ),
        (
            "<b>Chinese cell collapsed to n = 3 after alternate "
            "exhaustion.</b> Following pre-reg \u00a76 cell-collapse "
            "contingency, the chinese cell is retained for descriptive "
            "reporting but is the smallest cell in the panel. The cell\u2019s "
            "structural smallness reflects under-representation of Chinese-"
            "tradition kitchen-knife brands in English-language Google "
            "Trends signal at v0.16\u2019s acquisition timestamp \u2014 a "
            "substrate-specific Trends-coverage observation worth flagging "
            "for downstream interpretation. DEVIATIONS Entry 4 documents "
            "the operational sequence."
        ),
        (
            "<b>Phase A pivot fallback.</b> Phase A pivot validation "
            "surfaced Victorinox EXCLUDED_E1a (kitchen-knife brand presence "
            "below Trends-eligibility floor on bare canonical query); "
            "W\u00fcsthof activated as pivot per pre-reg \u00a76 contingency. "
            "DEVIATIONS Entry 3 documents the handling. The substrate "
            "specificity of the pivot-validation criterion \u2014 v1.2 "
            "Protocol does not centrally specify a pivot-quality threshold "
            "below which fallback activates \u2014 is a methodology-paper "
            "v1.3 increment surfaced by v0.16 and queued for the AIAS "
            "Protocol Methodology v1.3 update."
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
            "<b>v0.16 publication sequence.</b> Brand-format report (this "
            "document), SSRN working paper, and OSF deposit ship together "
            "under git tag <font name='Helvetica'>v0.16-published</font>. "
            "Companion SSRN paper develops the substantive analysis "
            "deferred from Patterns 3\u20135 of this report \u2014 Phase A "
            "pivot fallback, alternate activation, cross-version "
            "comparability with v0.8 \u2014 alongside the formal hypothesis "
            "results."
        ),
        (
            "<b>Tri-System Brand Growth framework cross-citation.</b> The "
            "MSI Working Paper bibliography is updated to incorporate "
            "v0.13, v0.14, v0.15, v0.16, and AIAS Protocol v1.2 (SSRN "
            "6761698) as empirical anchors for the framework\u2019s AI "
            "Availability axis. v0.16 specifically supports the framework\u2019s "
            "identity-load boundary claim with the kitchen-knives PARTIAL "
            "verdict."
        ),
        (
            "<b>AIAS Protocol v1.3 methodology increment.</b> v0.16 Phase A "
            "pivot validation surfaced an unspecified contingency: Protocol "
            "v1.2 does not centrally specify a pivot-quality threshold "
            "below which fallback activates. DEVIATIONS Entry 3 documents "
            "the operational handling. The forward action is a methodology-"
            "paper v1.3 increment specifying the pivot-validation criterion "
            "centrally."
        ),
        (
            "<b>Phase 4 \u2014 AIAS components 2\u20136.</b> Construct "
            "validity established for AI Presence across v0.11\u2013v0.16 "
            "is the precondition for measurement work on the remaining "
            "five AIAS components: Ranking, Consistency, Coverage, "
            "Grounding, Sentiment. The four-substrate Regime 4 baseline "
            "(skincare, finance, tea, kitchen-knives PARTIAL) provides "
            "the construct-validity anchor against which cross-component "
            "correlation will be measured."
        ),
        (
            "<b>Routledge monograph.</b> Single-authored research monograph "
            "<i>The Third System: AI Availability and the Architecture of "
            "Brand Growth</i> (Routledge Studies in Marketing, in "
            "development). v0.16 contributes to the empirical archive "
            "supporting the monograph\u2019s extension of the Ehrenberg-"
            "Bass tradition to the AI-mediated commerce environment."
        ),
    ],
}

# ----------------------------------------------------------------------------
# CLOSING
# ----------------------------------------------------------------------------

CLOSING = {
    "byline_long": [
        "Pablo Ulpiano Gonz\u00e1lez Castro",
        "Founder, Third System\u2122",
        "Faculty, MPS Branding Program, School of Visual Arts",
    ],
    "datasets": [
        (
            "<b>OSF project ec6wh, /v16/.</b> Inputs: fresh LLM acquisition "
            "(960 cells across two waves on six-LLM panel \u2014 Anthropic "
            "Sonnet 4.6, Anthropic Opus 4.7, OpenAI gpt-5.4-mini, OpenAI "
            "gpt-5.5, Google gemini-2.5-flash, xAI grok-4-1-fast-reasoning, "
            "status = ok); Google Trends raw responses (6 bundles \u00d7 2 "
            "regions \u00d7 14-day combined window covering t<sub>1</sub> "
            "and t<sub>2</sub>); Phase A pivot validation with W\u00fcsthof "
            "fallback after Victorinox EXCLUDED_E1a (DEVIATIONS Entry 3); "
            "Phase B topic-ID resolution with Au Nain (French) and Hengtai "
            "(Chinese) activated from alternates (DEVIATIONS Entry 4); v0.16 "
            "registry (<font name='Helvetica'>brands_kitchen_knives_v0.16."
            "json</font>, five tradition cells: japanese 6, german 5, "
            "french 4, american 5, chinese 3 after alternate exhaustion); "
            "scoring outputs (canonical_scoring.json, per_brand_paired.csv, "
            "h_regime4_replication_knives.csv, h_discourse_language_"
            "carryforward.csv); 5 chart PDFs; build scripts; this report; "
            "and the matching SSRN working paper."
        ),
        (
            "<b>Companion SSRN working paper and AIAS programme cross-"
            "references.</b> v0.16 working paper: <i>Regime 4 Boundary and "
            "Discourse-Language Carryforward on the Kitchen-Knives Substrate: "
            "AIAS Presence Measurement Programme v0.16</i>. Cross-references: "
            "AI Availability foundational paper (SSRN 6659000); AIAS Presence "
            "Measurement Protocol v1.1 (SSRN 6722319); AIAS Presence "
            "Measurement Protocol v1.2 (SSRN 6761698); v0.6 Cross-Category "
            "Findings (SSRN 6720959); v0.7 Phantom-Brand Persistence "
            "Phase 2 BBB (SSRN 6721779); v0.8 Discourse-Language Knives "
            "(SSRN 6728000); v0.9 Longitudinal Re-Baseline (SSRN 6736878); "
            "v0.10 Naive-Phantom Rate Stability (SSRN 6741163); v0.11 PM "
            "Software \u00d7 Trends Construct Validity Pilot (SSRN 6745040); "
            "v0.12 Three Empirical Regimes (SSRN 6748341); v0.13 Four "
            "Empirical Regimes \u2014 Five-Category Construct-Validity "
            "Expansion (SSRN 6750498); v0.14 Kitchen Knives \u2014 Regime 4 "
            "Replication (SSRN 6755621); v0.15 Premium Tea Panel Expansion "
            "Robustness (SSRN 6768059)."
        ),
    ],
    "methodology_log": (
        "v0.16 follows AIAS Presence Measurement Protocol v1.2 (SSRN "
        "6761698). Pre-registration locked at git tag <font name='Helvetica'>"
        "v0.16-prereg</font> (commit <font name='Helvetica'>511e339</font>) "
        "on 16 May 2026 UTC prior to LLM acquisition. Acquisition windows: "
        "t<sub>1</sub> April 27 \u2013 May 3, 2026; t<sub>2</sub> May 4 "
        "\u2013 May 10, 2026. DEVIATIONS.md: Entry 3 documents Phase A "
        "pivot fallback (Victorinox EXCLUDED_E1a \u2192 W\u00fcsthof "
        "activated per pre-reg \u00a76); Entry 4 documents alternate "
        "activation for primary-brand topic-ID failures (Au Nain activated "
        "in French cell; Hengtai activated in Chinese cell after Hu Si Chao "
        "and Dengjia both EXCLUDED_E1a; Chinese cell stops at n = 3 after "
        "alternate-pool exhaustion). No pre-registered hypothesis, "
        "threshold, or routing rule was modified. The canonical scoring "
        "script (<font name='Helvetica'>score_v16.py</font>) is locked at "
        "git commit <font name='Helvetica'>511e339</font> (same as pre-reg "
        "tag)."
    ),
}