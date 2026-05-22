"""
v09 Longitudinal Re-Baseline — structured content.

Mirrors v08_knives_content.py top-level structure so build_report_v09.py can
fork build_report_v08.py with minimal changes.

Differences from v08:
  - Subject is methodological/longitudinal validity (not a designed-for-test
    on a single category). Five categories, six pre-registered hypotheses
    plus a post-hoc Pattern 1 replication test.
  - Story arc is "AI Presence behaves like a real measurable construct";
    headline is the joint replication of multiple stability and structural-
    variance patterns across a seven-day interval.
  - Pattern under test is the framework as a whole, not a single mechanism.
  - Seven findings (H1, H2, H3, H4, H5, H6, post-hoc Pattern 1) instead of
    v0.8's five.
  - Hypothesis scoring includes both H5 strict and H5 inclusive readings
    plus the post-hoc Pattern 1 row.
"""

# ---- Cover ----
COVER = {
    "title": "AI Presence Drift",
    "subtitle": "AI Presence Index v0.9 \u2014 Five categories, two waves, longitudinal re-baseline",
    "date": "8 May 2026",
    "byline_short": "Pablo Ulpiano Gonzalez Castro \u00b7 Third System",
    "tagline": "Independent measurement for the AI mediation layer.",
}

# ---- Standfirst (lead spread) ----
STANDFIRST = "AI Presence is stable. Patterns replicate. The instrument works."
LEAD_DECK = (
    "Seven days after the v0.6 cross-category baseline, we re-measured the "
    "same five categories on the same matched two-model subset. Per-brand "
    "drift is small. Top-of-leaderboard composition is preserved. Within-"
    "category brand variance and cross-model spread structures both "
    "replicate. The Mint phantom-brand persists at gross Presence. The "
    "v0.6 discourse-language bias hypothesis replicates strict at threshold "
    "and surfaces Graza as a sharper diagnostic. Five formal hypotheses "
    "confirmed; the sixth landed at the predicted stability band; v0.6's "
    "Pattern 1 cross-model spread replicates in a post-hoc test. AI "
    "Presence behaves like a real underlying construct."
)

# ---- Executive summary ----
EXEC_SUMMARY = [
    (
        "Third System re-measured the five categories first measured in the "
        "v0.6 cross-category baseline \u2014 project management software, "
        "premium running shoes, premium olive oil, premium facial skincare, "
        "and personal finance applications \u2014 at a second time point "
        "approximately seven days after t<sub size='6'>1</sub>. Six hypotheses with "
        "explicit numerical thresholds were committed to a pre-registration "
        "document locked at git commit f8cebbd prior to any t<sub size='6'>2</sub> data "
        "collection. The matched two-model subset (Anthropic Claude Sonnet "
        "4.6 and OpenAI gpt-5.4-mini, the original v0.6 lineup) carries the "
        "longitudinal claim; four parallel-baseline models added at "
        "t<sub size='6'>2</sub> contribute new baselines but cannot contribute to drift "
        "deltas. Total measurement volume: 1,440 successful runs across 5 "
        "categories \u00d7 6 prompts \u00d7 6 models \u00d7 8 runs."
    ),
    (
        "<b>The headline result is decisive.</b> Five of six formal "
        "hypotheses confirmed at the strongest level the protocol allows; "
        "the sixth landed at the predicted stability band. Per-brand drift "
        "across all 5 categories on the matched subset (n = 103 brand-"
        "level deltas) is small: <b>88.3 percent of brands within "
        "\u00b15pp</b>; <b>99.0 percent within \u00b110pp</b>. Top-three "
        "brands at t<sub size='6'>1</sub> remained in the top-five at t<sub size='6'>2</sub> in every "
        "category (5 of 5). Within-category brand-presence variance "
        "ordering across the five categories at t<sub size='6'>2</sub> correlated with "
        "t<sub size='6'>1</sub> at <b>Spearman <font name='Helvetica'>\u03c1</font> = 0.8</b>."
    ),
    (
        "<b>Mechanisms hold.</b> The Mint phantom-brand stayed at "
        "<b>41.7 percent</b> matched-subset gross Presence at t<sub size='6'>2</sub> "
        "versus <b>44.8 percent</b> at t<sub size='6'>1</sub> \u2014 a \u22123.1 "
        "percentage-point delta within the predicted stability band, "
        "confirming that recommendation-slot persistence does not decay "
        "measurably across a seven-day interval. Pattern 4 discourse-"
        "language bias replicated under the strict reading: Spanish olive "
        "oil aggregate Presence at <b>11.5pp</b> below the 12.5pp threshold "
        "derived from the International Olive Council production share, "
        "and K-beauty aggregate Presence in skincare at <b>1.0pp</b> well "
        "below the 5pp threshold. Per-brand cross-model spread between "
        "the matched-subset models correlated between t<sub size='6'>1</sub> and t<sub size='6'>2</sub> "
        "at Pearson r \u2265 0.7 in every category."
    ),
    (
        "<b>The H5 sensitivity surfaces a cleaner instance of v0.6 "
        "\u00a74.4's refined hypothesis.</b> When Graza \u2014 a US-"
        "headquartered, Spanish-sourced, English-marketed olive oil brand "
        "\u2014 is added to the Spanish cohort, aggregate Presence rises "
        "to 14.2pp and breaches the threshold. The 2.7-point swing is "
        "entirely Graza. Including Graza breaches the threshold; "
        "excluding Graza confirms it. The brand-marketing-language tier "
        "is the binding variable, not country of origin. The v0.9 "
        "contribution is operationalizing the v0.6 \u00a74.4 framing at "
        "numerical threshold and surfacing Graza as the diagnostic case."
    ),
    (
        "<b>A post-hoc Pattern 1 test replicates v0.6's qualitative "
        "ordering.</b> Per-category mean cross-model spread between Sonnet "
        "and gpt-5.4-mini ranks at <b>Spearman <font name='Helvetica'>\u03c1</font> = 0.800</b> between "
        "t<sub size='6'>1</sub> and t<sub size='6'>2</sub>, and at <b><font name='Helvetica'>\u03c1</font> = 0.900</b> between "
        "t<sub size='6'>2</sub> and v0.6's narrative ordering (personal finance > olive "
        "oil > project management > skincare > running). The t<sub size='6'>2</sub> "
        "ranking matches v0.6's narrative <i>better</i> than t<sub size='6'>1</sub> does "
        "(0.900 vs 0.600), with finance cross-model spread widening "
        "(+3.9pp) and project management narrowing (\u22121.4pp) between "
        "waves \u2014 both within H1's empirical noise floor but in "
        "directions that strengthen v0.6's qualitative ordering at t<sub size='6'>2</sub>."
    ),
    (
        "<b>The combined result set is interpreted as a longitudinal "
        "validity argument for AI Presence as a construct.</b> AI "
        "Presence behaves like a real, structured property of the LLM "
        "tier rather than measurement noise. Drift is small. Leaderboards "
        "are stable. Structural variance patterns replicate at two scales "
        "(within-category brand variance and between-model spread). "
        "Established mechanisms hold across waves \u2014 phantom-brand "
        "persistence, discourse-language bias in the brand-marketing-"
        "language form, cross-model relative behavior. The four legs "
        "together motivate interpretation of AI Presence as a measurable "
        "underlying construct rather than an instrument-and-occasion "
        "artifact. This unblocks Phase 3 construct-validity work, which "
        "requires three categories at two time points and now has data "
        "for five."
    ),
]

# ---- What we measured ----
WHAT_WE_MEASURED = {
    "heading": "What we measured",
    "paragraphs": [
        (
            "v0.9 is the longitudinal re-baseline that closes Phase 2 of "
            "the AIAS measurement program and provides the data spine for "
            "Phase 3 construct-validity work. The five categories first "
            "measured in the v0.6 cross-category baseline \u2014 project "
            "management software, premium running shoes, premium olive "
            "oil, premium facial skincare, and personal finance "
            "applications \u2014 were re-measured at a second time point "
            "approximately seven days after t<sub size='6'>1</sub>, on the same matched "
            "two-model subset that v0.6 used. Six hypotheses with explicit "
            "numerical thresholds were committed to a pre-registration "
            "document locked at git commit f8cebbd (tag v0.9-prereg-"
            "locked) prior to any t<sub size='6'>2</sub> data collection."
        ),
        (
            "<b>Two waves.</b> t<sub size='6'>1</sub> = 29\u201330 April 2026 (the v0.6 "
            "cross-category baseline). t<sub size='6'>2</sub> = 7 May 2026 (this "
            "measurement). Inter-wave interval approximately seven days "
            "\u2014 short enough that no major model release or training-"
            "cutoff change is expected to fall within it, supporting the "
            "assumption that drift observed across the interval is "
            "incidental rather than structural. Longer intervals (one "
            "month, three months, twelve months) are required to "
            "characterize drift across model-pipeline transitions and "
            "are listed as v0.10+ candidates."
        ),
        (
            "<b>Matched two-model subset carries the longitudinal claim.</b> "
            "Anthropic Claude Sonnet 4.6 and OpenAI gpt-5.4-mini, the "
            "original v0.6 lineup, are the only models present at both "
            "waves. Drift deltas are computed exclusively against this "
            "subset. Four parallel-baseline models added at t<sub size='6'>2</sub> "
            "(Anthropic Claude Opus 4.7, OpenAI gpt-5.4, Google Gemini "
            "2.5 Pro, xAI Grok 4) provide new t<sub size='6'>2</sub> baselines for "
            "downstream cross-vendor work but cannot contribute to the "
            "longitudinal claim itself."
        ),
        (
            "<b>Same six prompts as v0.6, frozen.</b> One prompt class "
            "per Category Entry Point per Protocol \u00a73.1: DISCOVERY, "
            "COMPARISON, CONSTRAINT, IDENTITY, AUTHORITY, and "
            "RECOMMENDATION. The prompt set was frozen at v0.6 to "
            "preserve longitudinal comparability. The brand registries "
            "were similarly frozen at v0.6 final state."
        ),
        (
            "<b>1,440 successful measurements.</b> 5 categories \u00d7 6 "
            "prompts \u00d7 6 models \u00d7 8 runs at temperature 0.7 "
            "where supported, with a single round of failed-call "
            "recovery restoring the initial sweep to 100 percent. The "
            "matched-subset volume that carries the longitudinal claim "
            "is 480 measurements per wave (2 models \u00d7 5 categories "
            "\u00d7 6 prompts \u00d7 8 runs)."
        ),
        (
            "<b>Brand mention extraction</b> used gpt-5.4-mini at "
            "temperature 0 with structured-output classification, "
            "producing canonical brand mentions per response. A second-"
            "stage mode classifier labeled each response along the five-"
            "mode taxonomy (brand / mixed / component / authority / "
            "refusal) per Protocol \u00a73.4. The v0.6 mode classifications "
            "were derived retroactively against the same classifier "
            "(per the Decision Note locked at git commit e6428a4 prior "
            "to the pre-registration), so v0.9 mode-distribution shifts "
            "are computed against a consistent classifier across waves."
        ),
        (
            "<b>Six pre-registered hypotheses</b> plus the H5 strict-"
            "vs-inclusive sensitivity check plus an exploratory mode-"
            "distribution observation. H1: per-brand drift small and "
            "tightly bounded. H2: top-3 at t<sub size='6'>1</sub> remain in top-5 at "
            "t<sub size='6'>2</sub>, in 5 of 5 categories. H3: within-category brand-"
            "presence variance ordering preserves at Spearman <font name='Helvetica'>\u03c1</font> "
            "\u2265 0.7. H4: Mint phantom-brand stable within \u00b15pp "
            "of t<sub size='6'>1</sub> gross Presence (stability predicted, not "
            "decay). H5: Spanish olive oil and K-beauty skincare "
            "aggregate Presence below pre-registered thresholds. H6: "
            "per-brand cross-model spread Pearson r \u2265 0.7 between "
            "t<sub size='6'>1</sub> and t<sub size='6'>2</sub>, in \u22654 of 5 categories. A post-"
            "hoc test of v0.6's Pattern 1 (cross-model spread by "
            "category) was added against the same matched-subset data."
        ),
    ],
}

# ---- Patterns / Findings ----
PATTERNS = [
    # ------------------------------------------------------------------
    # FINDING 1 — Drift is small and tightly bounded.
    # ------------------------------------------------------------------
    {
        "number": 1,
        "title": "Drift across categories is small and tightly\u00a0bounded.",
        "chart_slot": "hero_f1_drift_scatter",
        "n_lead": 0,
        "paragraphs": [
            (
                "Across all <b>103 brand-level deltas</b> computed on the "
                "matched subset (the union of registered brands across the "
                "five categories at the v0.6 final-state registry), "
                "<b>88.3 percent of brands surfaced at t<sub size='6'>2</sub> within "
                "\u00b15 percentage points</b> of their t<sub size='6'>1</sub> Presence, "
                "and <b>99.0 percent surfaced within \u00b110 percentage "
                "points</b>. The H1 confirmation thresholds were "
                "\u226570 percent within \u00b15pp and \u226590 percent "
                "within \u00b110pp \u2014 both cleared with margin."
            ),
            (
                "<b>The empirical noise floor of one-week AI Presence "
                "measurement on the matched subset is approximately "
                "\u00b15 percentage points</b> for the modal brand and "
                "approximately \u00b110 percentage points for ninety-"
                "nine of every hundred. Among the largest movers, no "
                "single brand exceeded \u00b120 percentage points; the "
                "distribution is concentrated near zero."
            ),
            (
                "The drift result establishes the longitudinal noise floor "
                "against which all subsequent findings are interpreted. "
                "A measurement infrastructure where 88 percent of brand-"
                "level deltas are within \u00b15pp across a seven-day "
                "interval has the resolution to detect substantively "
                "interesting brand-level movement when it occurs. The "
                "absence of large-magnitude drift across the wave "
                "interval is the empirical signature of a stable "
                "underlying quantity that the AIAS measurement is "
                "recovering with bounded noise."
            ),
        ],
    },

    # ------------------------------------------------------------------
    # FINDING 2 — Leaderboards are stable.
    # ------------------------------------------------------------------
    {
        "number": 2,
        "title": "Top-of-leaderboard composition is stable across "
                 "categories.",
        "chart_slot": "hero_f2_leaderboard",
        "n_lead": 0,
        "paragraphs": [
            (
                "In each of the five categories, <b>the top-three brands "
                "by matched-subset Presence at t<sub size='6'>1</sub> remained in the "
                "top-five at t<sub size='6'>2</sub></b>. The result confirmed at <b>5 of "
                "5 categories with no exceptions</b>, well above the "
                "5-of-5 threshold for the headline confirmation band."
            ),
            (
                "The leaderboard stability is the most directly category-"
                "management-relevant of the v0.9 findings. Brand managers "
                "and category buyers tracking AI Presence as a leading "
                "indicator can rely on the top-of-leaderboard composition "
                "across at least the seven-day measurement interval. "
                "Specifically, the headline brands that lead an AI-mediated "
                "category at any given measurement point are the same "
                "headline brands the same measurement will identify a "
                "week later."
            ),
            (
                "The finding is consistent with the construct-validity "
                "interpretation in the discussion. A noise-dominated "
                "measurement process would, with non-trivial probability, "
                "reorder leaderboards across an interval; the observed "
                "across-the-board stability indicates that the position "
                "of dominant brands within a category is not artefactual."
            ),
        ],
    },

    # ------------------------------------------------------------------
    # FINDING 3 — Within-category variance ordering preserves.
    # ------------------------------------------------------------------
    {
        "number": 3,
        "title": "Within-category brand-presence variance ordering "
                 "preserves.",
        "chart_slot": "hero_f3_variance",
        "n_lead": 0,
        "paragraphs": [
            (
                "The pre-registered H3 measures whether the within-"
                "category dispersion of brand-presence rates \u2014 how "
                "spread out brands are within each category, computed as "
                "the standard deviation of per-brand Presence values "
                "\u2014 preserves its rank-ordering across categories "
                "between t<sub size='6'>1</sub> and t<sub size='6'>2</sub>."
            ),
            (
                "<b>The Spearman rank correlation of within-category "
                "variance between t<sub size='6'>1</sub> and t<sub size='6'>2</sub> across the five "
                "categories is <font name='Helvetica'>\u03c1</font> = 0.8</b>, above the 0.7 threshold "
                "for confirmation and well above the 0.4 threshold for "
                "partial confirmation. The within-category variance "
                "ordering is therefore stable across waves."
            ),
            (
                "Personal finance is the highest-dispersion category at "
                "both waves; running shoes is the lowest. The structural "
                "shape of how concentrated or fragmented brand-presence "
                "is within a category persists across the longitudinal "
                "interval. Categories that have widely-divergent brands "
                "at t<sub size='6'>1</sub> still have widely-divergent brands at "
                "t<sub size='6'>2</sub>; categories with tightly-clustered brands "
                "remain tightly-clustered."
            ),
            (
                "<b>A clarification on what H3 tests and what it does "
                "not.</b> H3's statistic is <i>within-category brand "
                "variance</i> \u2014 how much the registered brands "
                "within a single category differ from each other on "
                "Presence. This is related to but distinct from v0.6's "
                "Pattern 1 (Cross-Model Variance and Discourse "
                "Coherence), which is <i>between-model spread per brand</i> "
                "\u2014 a different statistic computed at the brand "
                "\u00d7 model level. The cross-model spread test is "
                "reported separately in Finding 7 as a post-hoc "
                "replication."
            ),
        ],
    },

    # ------------------------------------------------------------------
    # FINDING 4 — Mint persists at gross Presence.
    # ------------------------------------------------------------------
    {
        "number": 4,
        "title": "Mint persists at gross Presence \u2014 phantom-brand "
                 "stability across the wave interval.",
        "chart_slot": "hero_f4_mint",
        "n_lead": 0,
        "paragraphs": [
            (
                "The Mint phantom-brand observation from v0.6 \u00a74.6 "
                "(the brand was Intuit's leading personal finance "
                "application until its decommissioning in March 2024) "
                "holds at t<sub size='6'>2</sub>. <b>Mint's matched-subset gross "
                "Presence in personal finance was 44.8 percent at "
                "t<sub size='6'>1</sub> and 41.7 percent at t<sub size='6'>2</sub></b> \u2014 a delta "
                "of \u22123.1 percentage points within the predicted "
                "\u00b15-percentage-point stability band."
            ),
            (
                "The pre-registration explicitly named <i>stability</i> "
                "rather than decay as the predicted outcome under the "
                "corpus-aging mechanism articulated in v0.6 \u00a74.6: "
                "one additional time point seven days later is not "
                "enough for a defunct brand to be displaced from the LLM "
                "corpus, particularly when the brand's prior dominance "
                "generated extensive English-language discourse that "
                "persists in both training data and continuing "
                "inferential context. The H4 finding is therefore a "
                "confirmation of the predicted-stability outcome."
            ),
            (
                "<b>What H4 measures versus what v0.7 unpacked.</b> H4 "
                "measures <i>gross Presence</i> \u2014 the rate at "
                "which Mint surfaces in the model's output regardless "
                "of how the model contextualizes it (with or without "
                "caveat about the brand's decommissioning, with or "
                "without correction). This is the variable v0.6 \u00a74.6 "
                "reported. The v0.7 designed-for-test follow-up "
                "(Phantom-Brand Persistence Phase 2 BBB) reframed the "
                "phantom mechanism from knowledge-freshness lag to "
                "<i>recommendation-slot persistence</i>, distinguishing "
                "the <i>naive-phantom rate</i> (model presents the "
                "brand as fully live with no caveat \u2014 1.7 percent "
                "for BBB in v0.7) from gross Presence (38.2 percent for "
                "BBB)."
            ),
            (
                "The v0.9 H4 measurement does not unpack this distinction; "
                "the pre-registration tested the gross-Presence variable "
                "common to v0.6, on which the longitudinal stability "
                "claim is supported. A v0.10 measurement could pre-"
                "register a naive-phantom-rate stability hypothesis on "
                "Mint specifically and would extend the v0.7 reframe "
                "into the longitudinal frame. The v0.9 raw responses "
                "are deposited; only the classifier needs to be applied."
            ),
        ],
    },

    # ------------------------------------------------------------------
    # FINDING 5 — Pattern 4 replicates with refined hypothesis
    # ------------------------------------------------------------------
    {
        "number": 5,
        "title": "Pattern 4 replicates at v0.9, with the v0.6 \u00a74.4 "
                 "refined hypothesis operationalized.",
        "chart_slot": "hero_f5_pattern4",
        "n_lead": 0,
        "paragraphs": [
            (
                "The v0.6 \u00a74.4 baseline observed in two cross-"
                "lingual categories (premium olive oil and premium "
                "facial skincare) that brand-presence rates appeared to "
                "track marketing-discourse language rather than country "
                "of origin or cultural reference. The v0.6 paper's "
                "diagnostic case for the refinement was the contrast "
                "between Tatcha (Japanese-aesthetic skincare brand "
                "founded in San Francisco with American-English "
                "marketing \u2014 18 percent Presence) and Beauty of "
                "Joseon (Korean brand with Korean-language primary "
                "marketing \u2014 zero percent Presence): the cultural "
                "reference does not constrain Presence; the marketing-"
                "discourse language does."
            ),
            (
                "The v0.6 refined hypothesis stated <i>\u201cLLMs under-"
                "surface brands whose primary marketing discourse is "
                "conducted in a language under-represented in AI "
                "training data, even when the cultural reference is "
                "well-known in English.\u201d</i> The v0.8 designed-for-"
                "test on premium kitchen knives confirmed the mechanism "
                "on a third category. <b>The v0.9 H5 contribution is "
                "the operationalization of the refined hypothesis with "
                "explicit pre-registered numerical thresholds applied "
                "to the original two cross-lingual categories at "
                "t<sub size='6'>2</sub>.</b>"
            ),
            (
                "<b>The strict-reading H5 outcome confirms the pattern.</b> "
                "Spanish olive oil aggregate Presence, restricted to "
                "the two registered brands that present themselves to "
                "consumers as Spanish-discourse-coverage (Castillo de "
                "Canena and N\u00fa\u00f1ez de Prado), measured "
                "<b>11.5 percentage points</b> \u2014 below the 12.5-"
                "percent threshold derived from Spain's approximately "
                "50-percent share of global olive oil production "
                "(International Olive Council). K-beauty aggregate "
                "Presence in skincare, comprising the single registered "
                "K-beauty brand (Beauty of Joseon), measured <b>1.0 "
                "percentage point</b> \u2014 well below the 5-percent "
                "threshold."
            ),
            (
                "<b>A sensitivity check produces a sharper instance of "
                "the v0.6 refined hypothesis.</b> When Graza \u2014 a "
                "US-headquartered, Spanish-sourced, English-marketed "
                "D2C olive oil brand that surfaces at approximately 14 "
                "percent matched-subset Presence \u2014 is added to the "
                "Spanish cohort, the aggregate rises to 14.2 percentage "
                "points and breaches the 12.5-percent threshold. The "
                "2.7-point swing is entirely Graza."
            ),
            (
                "Graza is the cleanest available diagnostic for the "
                "brand-marketing-language tier: a brand that sources "
                "its olives from Spain but markets to American "
                "consumers in English, indexes in English-language "
                "retail feeds, and is discussed in English-language "
                "food media. <b>Including Graza in the Spanish cohort "
                "breaches the H5 threshold; excluding Graza confirms "
                "it.</b> The brand-marketing-language tier \u2014 "
                "which v0.6 \u00a74.4 identified \u2014 is the binding "
                "variable. The v0.9 contribution is making the v0.6 "
                "refinement testable at threshold and surfacing Graza "
                "as the diagnostic case that isolates it cleanly from "
                "country-of-origin."
            ),
            (
                "<b>The K-beauty registry coverage is itself a finding.</b> "
                "The v0.6 skincare registry contains thirty-one brands, "
                "of which exactly one (Beauty of Joseon) is a Korean-"
                "headquartered K-beauty brand discoursed primarily in "
                "Korean-language category media. The under-representation "
                "in the registry construction parallels the discourse-"
                "language bias the test is designed to detect. The "
                "implication is that the registry-construction process "
                "inherits, at the analyst tier, the same Anglo-discourse "
                "coverage gap that produces the LLM-tier discourse-"
                "language bias. The reflexivity is internally consistent "
                "with the discourse-language bias hypothesis itself "
                "\u2014 it would be more surprising if registry "
                "construction were free of the bias the registry is "
                "designed to detect."
            ),
        ],
    },

    # ------------------------------------------------------------------
    # FINDING 6 — Cross-model relative behavior is stable.
    # ------------------------------------------------------------------
    {
        "number": 6,
        "title": "Cross-model relative behavior is preserved across the "
                 "wave interval.",
        "chart_slot": "hero_f6_spread",
        "n_lead": 0,
        "paragraphs": [
            (
                "For each of the five categories, the per-brand spread "
                "between Anthropic Claude Sonnet 4.6 and OpenAI gpt-5.4-"
                "mini at t<sub size='6'>2</sub> correlated with the same-pair spread "
                "at t<sub size='6'>1</sub> at <b>Pearson r \u2265 0.7</b>. The result "
                "confirmed at <b>5 of 5 categories</b>, above the 4-of-"
                "5 threshold for headline confirmation."
            ),
            (
                "The finding indicates that the cross-model differential "
                "\u2014 what each model emphasizes versus what its "
                "companion emphasizes within a category \u2014 is "
                "preserved across the seven-day interval. Divergent "
                "brand-level shifts between the two models would suggest "
                "model-specific behavior change; the observed stability "
                "instead suggests that whatever AI behavior changed "
                "between t<sub size='6'>1</sub> and t<sub size='6'>2</sub> affected both models in "
                "approximately parallel ways, or affected neither."
            ),
            (
                "Combined with H3 (within-category brand variance "
                "preservation), H6 establishes that AI Presence has "
                "two independent variance structures that both replicate "
                "across the wave interval: the within-category "
                "dispersion of brands and the between-model dispersion "
                "of attention. Both are predicted by v0.6's discourse-"
                "coherence framing, both are stable, and both are "
                "structural rather than artefactual."
            ),
        ],
    },

    # ------------------------------------------------------------------
    # FINDING 7 — Pattern 1 cross-model spread replicates (post-hoc)
    # ------------------------------------------------------------------
    {
        "number": 7,
        "title": "Pattern 1 cross-model spread replicates v0.6's "
                 "ordering (post-hoc).",
        "chart_slot": "hero_f7_pattern1",
        "n_lead": 0,
        "paragraphs": [
            (
                "<b>A post-hoc test of v0.6's Pattern 1</b> (Cross-Model "
                "Variance and Discourse Coherence) at the category level "
                "was performed against the same matched-subset data as "
                "H1 through H6. The test is post-hoc rather than pre-"
                "registered because the H3 statistic is within-category "
                "brand-presence variance, while Pattern 1's statistic "
                "is between-model spread per brand averaged within a "
                "category \u2014 a different aggregation."
            ),
            (
                "The post-hoc test computes, for each category, the "
                "mean absolute |Sonnet \u2212 gpt-5.4-mini| Presence "
                "across registered brands, and ranks categories by this "
                "mean cross-model spread at each wave. <b>The Spearman "
                "rank correlation between t<sub size='6'>1</sub> and t<sub size='6'>2</sub> rankings "
                "is <font name='Helvetica'>\u03c1</font> = 0.800.</b> The rank correlation between "
                "v0.9's t<sub size='6'>2</sub> ranking and v0.6's narrative ordering "
                "(personal finance > olive oil > project management > "
                "skincare > running) is <b><font name='Helvetica'>\u03c1</font> = 0.900</b>."
            ),
            (
                "<b>Pattern 1 as v0.6 stated it replicates at v0.9.</b> "
                "The t<sub size='6'>2</sub> ranking matches v0.6's narrative ordering "
                "more closely than t<sub size='6'>1</sub> does (<font name='Helvetica'>\u03c1</font> 0.900 versus "
                "0.600), with finance cross-model spread increasing "
                "(+3.9pp) and project management spread decreasing "
                "(\u22121.4pp) between waves \u2014 both within H1's "
                "empirical noise floor (Finding 1) but in directions "
                "that strengthen v0.6's qualitative ordering at "
                "t<sub size='6'>2</sub>."
            ),
            (
                "The post-hoc Pattern 1 result is reported as exploratory "
                "and is not part of the formal H1 through H6 score. It "
                "is included here because v0.6 stated Pattern 1 in "
                "qualitative terms (which categories have wider cross-"
                "model spreads) and v0.9 has the data to test that "
                "specific qualitative claim quantitatively at the "
                "longitudinal interval, even though Pattern 1 was not "
                "the variable the v0.9 pre-registration committed to. "
                "A v0.10 pre-registration could lock the Pattern 1 "
                "ordering as a formal hypothesis given the v0.9 "
                "calibration."
            ),
        ],
    },
]

# ---- Hypothesis scoring ----
HYPOTHESIS_SCORING = {
    "heading": "Pre-registration outcomes",
    "intro": (
        "Six pre-registered hypotheses plus the H5 strict-vs-inclusive "
        "sensitivity check, plus an exploratory mode-distribution "
        "observation, plus a post-hoc Pattern 1 replication test. "
        "<b>Headline: five formal hypotheses confirmed; the sixth landed "
        "at the predicted stability band.</b>"
    ),
    "rows": [
        (
            "H1",
            "Per-brand drift small and tightly bounded "
            "(\u226570% within \u00b15pp; \u226590% within \u00b110pp).",
            "88.3% within \u00b15pp; 99.0% within \u00b110pp.",
            "CONFIRMED",
            "confirmed",
        ),
        (
            "H2",
            "Top-3 at t<sub size='6'>1</sub> remain in top-5 at t<sub size='6'>2</sub>, in 5 of 5 "
            "categories.",
            "5 of 5; no exceptions.",
            "CONFIRMED",
            "confirmed",
        ),
        (
            "H3",
            "Within-category brand-presence variance ordering preserves "
            "(Spearman <font name='Helvetica'>\u03c1</font> \u2265 0.7).",
            "<font name='Helvetica'>\u03c1</font> = 0.8.",
            "CONFIRMED",
            "confirmed",
        ),
        (
            "H4",
            "Mint matched-subset gross Presence stable within \u00b15pp "
            "(stability predicted, not decay).",
            "\u22123.1pp (44.8% \u2192 41.7%); within band.",
            "STABILITY (predicted)",
            "confirmed",
        ),
        (
            "H5 strict",
            "Spanish olive oil aggregate \u226412.5pp AND K-beauty "
            "aggregate \u22645pp.",
            "11.5pp; 1.0pp \u2014 both pass.",
            "CONFIRMED",
            "confirmed",
        ),
        (
            "H5 inclusive",
            "As H5 strict, with Graza included in the Spanish cohort.",
            "14.2pp (breach); 1.0pp.",
            "PARTIALLY CONFIRMED",
            "partial",
        ),
        (
            "H6",
            "Per-brand cross-model spread Pearson r \u2265 0.7 between "
            "t<sub size='6'>1</sub> and t<sub size='6'>2</sub>, in \u22654 of 5 categories.",
            "5 of 5.",
            "CONFIRMED",
            "confirmed",
        ),
        (
            "Mode dist.",
            "Exploratory; no pre-registered threshold. Reported as a "
            "calibration baseline for v0.10.",
            "Largest shifts: PM software +7.3pp brand mode; olive oil "
            "\u22128.3pp brand mode; skincare \u22126.2pp component "
            "mode.",
            "EXPLORATORY",
            "descriptive",
        ),
        (
            "Pattern 1 (post-hoc)",
            "Spearman <font name='Helvetica'>\u03c1</font> on cross-model spread ranking, t<sub size='6'>1</sub> vs "
            "t<sub size='6'>2</sub>; and t<sub size='6'>2</sub> vs v0.6 narrative ordering.",
            "<font name='Helvetica'>\u03c1</font> = 0.800 (t<sub size='6'>1</sub>/t<sub size='6'>2</sub>); <font name='Helvetica'>\u03c1</font> = 0.900 (t<sub size='6'>2</sub>/v0.6).",
            "POST-HOC REPLICATED",
            "descriptive",
        ),
    ],
}

# ---- Hypothesis details (per-hypothesis explainers) ----
HYPOTHESIS_DETAILS = {
    "heading": "Per-hypothesis breakdown",
    "intro": (
        "Each pre-registered hypothesis with what the test measured, "
        "what the data delivered, and how to read the outcome against "
        "the construct-validity argument."
    ),
    "items": [
        (
            "H1",
            "<b>H1 \u2014 Drift.</b> Per-brand magnitude of "
            "t<sub size='6'>1</sub>\u2192t<sub size='6'>2</sub> Presence delta on the matched subset. "
            "Establishes the empirical noise floor for one-week "
            "measurement intervals: <b>\u00b15pp for the modal brand</b>, "
            "<b>\u00b110pp for ninety-nine of every hundred</b>. The "
            "absence of large-magnitude drift is the empirical signature "
            "of a stable underlying quantity."
        ),
        (
            "H2",
            "<b>H2 \u2014 Leaderboards.</b> Whether top-of-category "
            "brands at t<sub size='6'>1</sub> remain top-of-category at t<sub size='6'>2</sub>. <b>5 "
            "of 5 categories; every t<sub size='6'>1</sub> top-three brand in the "
            "t<sub size='6'>2</sub> top-five.</b> The most directly category-management-"
            "relevant of the v0.9 findings: top-of-leaderboard composition "
            "behaves as a stable leading indicator across at least the "
            "seven-day interval."
        ),
        (
            "H3",
            "<b>H3 \u2014 Within-category variance.</b> Whether "
            "categories preserve their within-category brand-presence "
            "dispersion ordering across the wave. <b>Spearman <font name='Helvetica'>\u03c1</font> = "
            "0.8</b> across the 5 categories \u2014 above the 0.7 "
            "threshold for confirmation. Personal finance is the "
            "highest-dispersion category at both waves; running shoes "
            "the lowest. The structural shape of within-category "
            "fragmentation is preserved across the longitudinal "
            "interval."
        ),
        (
            "H4",
            "<b>H4 \u2014 Mint persistence.</b> Whether the v0.6 "
            "phantom-brand observation (Mint at 44 percent gross "
            "Presence despite operational decommissioning in March "
            "2024) is stable at t<sub size='6'>2</sub>. <b>44.8% \u2192 41.7% "
            "(\u22123.1pp)</b>; within the predicted \u00b15pp "
            "stability band. The v0.7 reframe distinguishing naive-"
            "phantom rate from gross Presence is not unpacked at v0.9; "
            "the variable v0.6 \u00a74.6 reported is what H4 confirms "
            "longitudinal stability for."
        ),
        (
            "H5",
            "<b>H5 \u2014 Pattern 4.</b> Whether the v0.6 \u00a74.4 "
            "discourse-language bias hypothesis replicates with explicit "
            "numerical thresholds. <b>Strict reading: 11.5pp Spanish "
            "(below 12.5pp threshold); 1.0pp K-beauty (below 5pp "
            "threshold).</b> Inclusive reading with Graza added: 14.2pp "
            "Spanish (breach). The v0.9 contribution is operationalizing "
            "the v0.6 brand-marketing-language framing at threshold and "
            "surfacing Graza as the diagnostic case isolating marketing-"
            "language from country-of-origin."
        ),
        (
            "H6",
            "<b>H6 \u2014 Cross-model spread.</b> Whether per-brand "
            "Sonnet-vs-mini spread structure preserves across waves. "
            "<b>Pearson r \u2265 0.7 in 5 of 5 categories.</b> "
            "Independent variance-replication test at the brand "
            "\u00d7 model aggregation level, separate from H3's "
            "category-aggregation test. Together H3 and H6 establish "
            "two independent variance structures that both replicate."
        ),
        (
            "P1",
            "<b>Pattern 1 (post-hoc).</b> Whether v0.6's qualitative "
            "cross-model spread ordering by category replicates at v0.9. "
            "<b>Spearman <font name='Helvetica'>\u03c1</font> = 0.800 (t<sub size='6'>1</sub>/t<sub size='6'>2</sub>); <font name='Helvetica'>\u03c1</font> = "
            "0.900 (t<sub size='6'>2</sub> vs v0.6 narrative ordering).</b> The "
            "t<sub size='6'>2</sub> ranking matches v0.6's stated qualitative "
            "ordering more closely than t<sub size='6'>1</sub> does, with finance "
            "widening (+3.9pp) and project management narrowing "
            "(\u22121.4pp) \u2014 both within H1's empirical noise "
            "floor but in directions that strengthen v0.6's "
            "narrative."
        ),
    ],
}

# ---- Limitations ----
LIMITATIONS = {
    "heading": "Limitations",
    "paragraphs": [
        (
            "Seven caveats apply to the v0.9 findings. Each is disclosed "
            "for transparency; none individually invalidates the "
            "longitudinal validity argument, but each constrains how "
            "the results generalize."
        ),
        (
            "<b>Single-pair longitudinal subset.</b> The longitudinal "
            "claim is computed on the matched two-model subset (Anthropic "
            "Claude Sonnet 4.6 and OpenAI gpt-5.4-mini) \u2014 the only "
            "models present at both t<sub size='6'>1</sub> and t<sub size='6'>2</sub>. The four "
            "parallel-baseline models added at t<sub size='6'>2</sub> contribute "
            "parallel new baselines but cannot contribute to the "
            "longitudinal claim. The validity argument generalizes most "
            "directly to the matched-subset model behavior."
        ),
        (
            "<b>Seven-day inter-measurement interval.</b> The interval "
            "is short enough that no major model release or training-"
            "cutoff change is expected to fall within it. Longer "
            "intervals (one month, three months, twelve months) are "
            "required to characterize drift across model-pipeline "
            "transitions \u2014 a v0.10+ candidate."
        ),
        (
            "<b>Gross-Presence-vs-naive-phantom-rate distinction not "
            "measured at v0.9.</b> The H4 finding is stability of "
            "<i>gross Presence</i> \u2014 the variable v0.6 \u00a74.6 "
            "reported and the variable on which the pre-registration "
            "tested. The v0.7 reframe distinguished naive-phantom rate "
            "(no caveat) from caveated phantom (model presents brand "
            "alongside knowledge of its decommissioning). Whether the "
            "naive-phantom rate alone is similarly stable is a separable "
            "question that a v0.10 pre-registration could address."
        ),
        (
            "<b>Registry-construction reflexivity.</b> The K-beauty "
            "observation in Finding 5 establishes that the registry-"
            "construction process inherits Anglo-discourse coverage "
            "bias. The reflexivity does not invalidate the H1 through "
            "H6 results \u2014 which are computed on the registered "
            "brand population whatever its construction \u2014 but "
            "constrains their generalization."
        ),
        (
            "<b>Construct validity remains open.</b> The longitudinal "
            "validity argument establishes that AI Presence behaves "
            "like a real LLM-tier construct. Whether AI Presence "
            "correlates with consumer awareness, purchase intent, or "
            "category share at the consumer-facing tier is the separate "
            "question the AIAS Phase 3 program will address. The v0.9 "
            "result unblocks Phase 3 (which requires three categories "
            "at two time points and now has data for five) but does not "
            "itself constitute construct-validity evidence at the "
            "consumer tier."
        ),
        (
            "<b>Personal finance metadata anomaly.</b> The v0.6 personal "
            "finance measurement carries the <i>brand_registry_version</i> "
            "stamp \u201cv2-skincare\u201d, inherited from the prior "
            "session's module-level constant. The metadata is cosmetic; "
            "raw-response inspection confirms that the prompts and "
            "registry that fired at v0.6 were the personal finance "
            "prompts and registry. The anomaly is disclosed for "
            "transparency."
        ),
        (
            "<b>Mode-classification audits deferred.</b> Manual inter-"
            "rater agreement audits on the v0.9 mode-classified data "
            "have not been completed at the time of this report's "
            "posting. The v0.8 audit established 96 percent strict "
            "agreement on the brand-surfacing macro unit (the unit at "
            "which H1 through H6 score) and 68 percent strict agreement "
            "on the underlying five-mode taxonomy. The v0.9 H1 through "
            "H6 results score against the macro unit and are therefore "
            "not dependent on the strict-mode-taxonomy agreement budget. "
            "Manual audits are scheduled prior to v0.10."
        ),
    ],
}

# ---- What's next ----
WHATS_NEXT = {
    "heading": "What\u2019s next",
    "paragraphs": [
        (
            "The Phase 3 program will address five priorities surfaced "
            "by the v0.9 findings. Each is enumerated as a candidate "
            "v0.10 or later study with the relevant data already in "
            "place."
        ),
        (
            "<b>Construct-validity correlation.</b> The v0.9 result "
            "unblocks the Phase 3 construct-validity study by "
            "providing five categories at two time points. Candidate "
            "consumer-tier validators include search-volume data "
            "(Google Trends), retail-tracking data (Amazon Best Seller "
            "ranks; category-share trackers where available), DTC "
            "brand-tracking instruments, and survey-based brand-"
            "awareness measurements. The construct-validity work is "
            "the program's gate to v1.0 release."
        ),
        (
            "<b>Longer-interval longitudinal measurements.</b> Drift "
            "across one-month, three-month, and twelve-month intervals "
            "\u2014 particularly across model-pipeline transitions or "
            "training-cutoff changes \u2014 would characterize the "
            "temporal stability of AI Presence at scales that bracket "
            "model retraining, brand-discourse evolution, and "
            "consumer-behavior cycles. The v0.9 seven-day interval "
            "establishes a noise floor; longer intervals would add "
            "structural drift on top of the noise floor."
        ),
        (
            "<b>Cross-lingual category expansion.</b> Premium tea and "
            "traditional spirits remain candidate categories for "
            "designed-for-test measurements of Pattern 4. The v0.9 H5 "
            "sensitivity \u2014 which surfaces the brand-marketing-"
            "language tier as the binding variable via the Graza "
            "diagnostic \u2014 informs the design of future cross-"
            "lingual studies: the discourse-language coverage of each "
            "registered brand becomes a primary variable, with country "
            "of origin as a secondary controlled covariate."
        ),
        (
            "<b>Naive-phantom-rate longitudinal stability.</b> "
            "Extending the v0.7 reframe into the longitudinal frame "
            "\u2014 measuring whether Mint's naive-phantom rate is as "
            "stable as its gross Presence \u2014 would distinguish the "
            "recommendation-slot persistence component of phantom-"
            "brand surfacing from the cumulative-discourse-mass "
            "component. A v0.10 pre-registration on this variable "
            "specifically is feasible against the v0.9 dataset (raw "
            "responses are deposited; only the classifier needs to be "
            "applied)."
        ),
        (
            "<b>Registry-construction protocols for cross-lingual "
            "categories.</b> The K-beauty observation suggests a "
            "structural improvement to the AIAS registry-construction "
            "methodology. A formal protocol that explicitly probes for "
            "non-English-discourse coverage gaps (for example, through "
            "the requirement that any registry intended to measure "
            "Pattern 4 in a category include a stated population-share "
            "survey of non-English-discourse producers) would mitigate "
            "the reflexivity caveat. The protocol revision is planned "
            "as part of AIAS Presence Measurement Protocol v1.2."
        ),
    ],
}

# ---- Closing matter ----
CLOSING = {
    "byline_long": [
        "<b>Pablo Ulpiano Gonzalez Castro</b>",
        "School of Visual Arts, MPS Branding Program, New York, NY "
        "(primary academic affiliation)",
        "Third System\u2122 (research entity; data archive and "
        "methodology venue)",
        "Correspondence: pablou@pablou.com \u00b7 pablou.com",
    ],
    "datasets": [
        "v0.9 raw responses, mode-classified responses, per-brand "
        "Presence rates per category per wave, and pre-registration "
        "outcome score \u2014 deposited as the v0.9 OSF release "
        "alongside the v0.6 Cross-Category Findings dataset.",
        "v0.6 baseline data and v0.7/v0.8 designed-for-test datasets "
        "remain available in their respective OSF deposits "
        "(unchanged).",
        "Build pipeline (chart generator, brand-format report builder, "
        "scoring scripts) deposited as v0.9 source archive.",
    ],
    "methodology_log": (
        "Pre-registration locked at git commit f8cebbd "
        "(tag v0.9-prereg-locked) prior to any t<sub size='6'>2</sub> data "
        "collection. Methodology decisions \u2014 matched two-model "
        "subset, retroactive mode classification of v0.6 data, "
        "registry freeze at v0.6 final state \u2014 locked at git "
        "commit e6428a4 prior to the pre-registration. AIAS Presence "
        "Measurement Protocol v1.1"
    ),
}
