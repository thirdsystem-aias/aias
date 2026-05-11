"""v0.11 brand-format report content modules.

Schema-compatible with build_report_v10.py's read patterns. Forked from
v10_naivephantom_content.py with v0.11 substance: PM software x Google
Trends construct validity pilot.

Framing convention (locked at v0.11 lead): AI applies a tighter and partly-
different category boundary than consumer search does. The H1 just-miss is
reframed as evidence FOR the AI Availability framework's distinctness claim.

ReportLab Paragraph HTML markup throughout (<sub>, <font>, <b>, <i>).
"""

# ----------------------------------------------------------------------------
# COVER
# ----------------------------------------------------------------------------

COVER = {
    "title":         "PM Software \u00d7 Google Trends",
    "subtitle":      "Construct Validity, t<sub size='10'>1</sub> \u2192 t<sub size='10'>2</sub>",
    "date":          "May 2026",
    "byline_short":  "Pablo Ulpiano Gonzalez Castro, Third System",
    "tagline":       "Independent measurement for the AI mediation layer.",
}

# ----------------------------------------------------------------------------
# STANDFIRST + LEAD DECK
# ----------------------------------------------------------------------------

STANDFIRST = (
    "Does AI Presence correspond to consumer search interest? "
    "v0.11 tests this on 18 project management software brands across both, "
    "at two longitudinal waves seven days apart."
)

LEAD_DECK = (
    "The correlation is positive, statistically significant, and reproducibly "
    "stable across both waves (Spearman <font name='Helvetica'>\u03c1</font> = 0.50 at t<sub>1</sub>, "
    "0.48 at t<sub>2</sub>; p &lt; 0.05 one-tailed at both; "
    "|<font name='Helvetica'>\u0394\u03c1</font>| = 0.02 \u2014 H2 confirmed). "
    "It narrowly misses the pre-registered moderate-to-strong threshold "
    "(<font name='Helvetica'>\u03c1</font> &gt; 0.5) by 0.004 at t<sub>1</sub> and weakens "
    "further under covariate control (partial <font name='Helvetica'>\u03c1</font> \u2248 0.41 after age + "
    "tier control). The construct's divergence from consumer search is "
    "concentrated and identifiable: only one of three AI-top-three brands "
    "appears in the Trends top-five, at both waves. The leadership zone is "
    "where AI applies a tighter category boundary than consumers do."
)

# ----------------------------------------------------------------------------
# EXECUTIVE SUMMARY (list of paragraph strings)
# ----------------------------------------------------------------------------

EXEC_SUMMARY = [
    (
        "The AI Availability Score (AIAS) research programme has, through v0.6\u2013v0.10, "
        "established a methodologically rigorous LLM-side measurement of brand presence in "
        "AI-mediated decision contexts. What it has not yet established \u2014 and what the "
        "framework's external validity ultimately rests on \u2014 is that this LLM-side measurement "
        "corresponds to what consumers actually do. v0.11 is the first construct-validity test "
        "in the programme: a single-category pilot against an external behavioural validator "
        "(Google Trends search interest)."
    ),
    (
        "The result is informative in a way that a clean confirmation or a hard rejection "
        "would not be. AI Presence and Google Trends search interest are positively correlated "
        "(<b>Spearman <font name='Helvetica'>\u03c1</font> = 0.50 at t<sub>1</sub>, 0.48 at t<sub>2</sub>; "
        "p &lt; 0.05 one-tailed at both waves</b>) and stably so across the seven-day "
        "longitudinal interval (<b>|<font name='Helvetica'>\u0394\u03c1</font>| = 0.02</b>). The two waves "
        "measure essentially the same relationship. But the correlation narrowly misses the "
        "pre-registered moderate-to-strong threshold (<font name='Helvetica'>\u03c1</font> &gt; 0.5) at "
        "t<sub>1</sub> by 0.004, and weakens further under covariate control "
        "(<b>partial <font name='Helvetica'>\u03c1</font> \u2248 0.41 after age + tier control</b>)."
    ),
    (
        "The leaderboard test (H3) localises where the construct fails. At both waves, only "
        "<b>one of three AI-top-three brands appears in the Trends top-five</b>. The construct's "
        "divergence is concentrated at the top of the AI Presence distribution \u2014 exactly the "
        "zone where AI mediation carries the most predictive weight for purchase decisions. "
        "<b>Linear</b> is AI's #1 recommendation in the category (86.5% AI Presence) with "
        "negligible consumer search interest (Trends value 1.88, Asana indexed to 100). "
        "<b>Todoist</b> is the inverse: 1.04% AI Presence with Trends value 28 \u2014 "
        "comparable to GitHub Projects, which receives 40\u00d7 more AI Presence. Different "
        "brands, same diagnostic: AI Presence is not interchangeable with consumer search."
    ),
    (
        "The substantive interpretation is that AI applies a tighter and partly-different "
        "category boundary than consumer search does. Linear, framed by AI as developer-focused "
        "PM, falls inside the AI category; Todoist, treated by AI as a personal task manager, "
        "falls outside it. Both are real PM tools by ordinary consumer reasoning. The construct "
        "of AI Availability is <i>correlated but not equivalent</i> to Mental Availability \u2014 "
        "which is the position the Tri-System Brand Growth framework articulates theoretically "
        "and which v0.11 now supports empirically in a single category."
    ),
    (
        "Phase 3 expansion (v0.12, three categories) will test whether this divergence pattern "
        "is specific to project management software or generalises. Categories where the "
        "leadership zone is stable across both AI and consumer search (premium olive oil is a "
        "candidate) may yield <font name='Helvetica'>\u03c1</font> &gt; 0.5. Categories where AI applies "
        "idiosyncratic boundaries (personal finance with its phantom-brand effects) may yield "
        "<font name='Helvetica'>\u03c1</font> further below."
    ),
]

# ----------------------------------------------------------------------------
# WHAT WE MEASURED
# ----------------------------------------------------------------------------

WHAT_WE_MEASURED = {
    "heading": "What We Measured",
    "paragraphs": [
        (
            "v0.11 measures the cross-sectional correlation between two independent brand-level "
            "signals: per-brand AI Presence rate (drawn from v0.9's deposited matched-subset "
            "LLM measurements) and per-brand Google Trends search interest (acquired fresh at "
            "v0.11 under a pre-registered protocol)."
        ),
        (
            "<b>AI Presence input.</b> Per-brand AI Presence rates for 18 PM software brands at "
            "two waves: t<sub>1</sub> = v0.6 collection window (29\u201330 April 2026); "
            "t<sub>2</sub> = v0.9 re-baseline window (7 May 2026). Both waves use the matched-"
            "model subset (Claude Sonnet 4.6 + GPT-5.4-mini) restricted to PM software per the "
            "v0.9 deposit's H2 leaderboard. n = 96 responses per wave."
        ),
        (
            "<b>Google Trends validator.</b> Daily search-interest indices for the same 18 "
            "brands acquired in a single locked session on 10 May 2026 via SerpAPI's Google "
            "Trends engine. Five pivot bundles (Asana as anchor; topic IDs where available, "
            "distinctive strings or '&lt;brand&gt; project management' compound queries where "
            "not) across two regions (Worldwide primary; US sensitivity). Pivot-rescaling "
            "converts the bundle-local 0\u2013100 indices into a single cross-brand-comparable "
            "scale where Asana \u2261 100."
        ),
        (
            "<b>Two waves.</b> t<sub>1</sub> Trends window: 27 April \u2013 3 May 2026 (centred "
            "on the v0.6 collection window). t<sub>2</sub> Trends window: 4 May \u2013 10 May "
            "2026 (centred on the v0.9 collection window). Windows are fully disjoint at the "
            "3/4 May boundary with identical Monday\u2013Sunday composition."
        ),
        (
            "<b>Pre-registration.</b> The protocol was locked at git tag "
            "<i>v0.11-prereg</i> (commit f20ade8) prior to any acquisition call against the "
            "wave windows. Four hypotheses with numerical thresholds: H1 cross-sectional "
            "construct validity (<font name='Helvetica'>\u03c1</font> &gt; 0.5 at both waves, primary); "
            "H2 stability (|<font name='Helvetica'>\u0394\u03c1</font>| \u2264 0.15); H3 leaderboard "
            "top-3 \u2286 top-5 at both waves; H4 covariate-controlled (partial "
            "<font name='Helvetica'>\u03c1</font> &gt; 0.5 after age + tier control). One brand (Shortcut) "
            "was excluded pre-acquisition under rule E1a; one brand (Height) was retained as a "
            "phantom brand following the rebrand-period convention from v0.7 / v0.10."
        ),
    ],
}

# ----------------------------------------------------------------------------
# FINDINGS (PATTERNS in v10 schema)
# ----------------------------------------------------------------------------

PATTERNS = [
    {
        "number": 1,
        "title": "The construct is positive, significant, and just-misses",
        "chart_slot": "f1_scatter_t1",
        "paragraphs": [
            (
                "Spearman <font name='Helvetica'>\u03c1</font> = 0.496 at t<sub>1</sub> with "
                "one-tailed p = 0.021. Positive and significant \u2014 but 0.004 below the "
                "pre-registered moderate-to-strong threshold."
            ),
            (
                "Per-brand AI Presence rates correlate positively with per-brand Google Trends "
                "rescaled means at t<sub>1</sub>: Spearman <font name='Helvetica'>\u03c1</font> = 0.496 "
                "(n = 17 brands clearing the at-acquisition eligibility rule). One-tailed "
                "p = 0.021 against the null of zero correlation. The directional claim of the "
                "construct \u2014 AI Presence and consumer search interest co-vary at the brand "
                "level \u2014 is statistically supported."
            ),
            (
                "The pre-registered threshold was <font name='Helvetica'>\u03c1</font> &gt; 0.5, calibrated "
                "against the conventional moderate-to-strong correlation benchmark in "
                "behavioural research. v0.11 misses this bar by 0.004. The pre-registration "
                "discipline gives this near-miss its weight: a post-hoc adjustment to "
                "<font name='Helvetica'>\u03c1</font> \u2265 0.49 would convert the result, but the bar is "
                "what it is. <b>H1 is falsified at the locked threshold.</b>"
            ),
            (
                "The Pearson sensitivity, in contrast, clears the same bar (r = 0.544 at "
                "t<sub>1</sub>; r = 0.533 at t<sub>2</sub>). This Pearson-vs-Spearman "
                "disagreement is not a methodological glitch. Pearson weights large absolute "
                "differences; Notion's Trends value of 591.95 (\u2248 6\u00d7 Asana) anchors the "
                "linear fit and pulls Pearson up. Spearman treats Notion as a single high rank "
                "and is in turn pulled down by the rank-1-AI / rank-low-Trends inversions at "
                "the top of the AI distribution (Linear; see Finding 3). The two statistics "
                "tell different parts of the same story."
            ),
        ],
    },
    {
        "number": 2,
        "title": "The just-miss is stable, not noise",
        "chart_slot": "f2_scatter_t2",
        "paragraphs": [
            (
                "<font name='Helvetica'>\u03c1</font><sub>t<sub>2</sub></sub> = 0.476 against "
                "<font name='Helvetica'>\u03c1</font><sub>t<sub>1</sub></sub> = 0.496. "
                "|<font name='Helvetica'>\u0394\u03c1</font>| = 0.020 \u2014 far below the 0.15 stability "
                "tolerance. H2 confirms: whatever H1 measured, it measured reproducibly."
            ),
            (
                "The H1 correlation magnitude is essentially identical at t<sub>2</sub>: "
                "Spearman <font name='Helvetica'>\u03c1</font> = 0.476, "
                "|<font name='Helvetica'>\u0394\u03c1</font>| = 0.020 against the t<sub>1</sub> value. The "
                "pre-registered tolerance was |<font name='Helvetica'>\u0394\u03c1</font>| \u2264 0.15, "
                "calibrated to absorb sampling variance at small n while detecting meaningful "
                "instability. <b>H2 is confirmed</b> with almost an order of magnitude of margin."
            ),
            (
                "The H2 confirmation is the load-bearing positive finding in v0.11. It rules "
                "out the interpretation that the H1 near-miss is wave-specific noise: the two "
                "waves' correlations sit on top of each other. The Pearson sensitivity tells "
                "the same story (r<sub>t<sub>1</sub></sub> = 0.544; "
                "r<sub>t<sub>2</sub></sub> = 0.533; |\u0394r| = 0.011)."
            ),
            (
                "The US-only sensitivity replicates the Worldwide pattern "
                "(<font name='Helvetica'>\u03c1</font><sub>t<sub>1</sub></sub> = 0.489; "
                "<font name='Helvetica'>\u03c1</font><sub>t<sub>2</sub></sub> = 0.455; "
                "|<font name='Helvetica'>\u0394\u03c1</font>| = 0.034). Nothing region-specific is "
                "driving the result, and the within-wave US-vs-Worldwide difference is itself "
                "smaller than the H2 tolerance."
            ),
        ],
    },
    {
        "number": 3,
        "title": "Where the construct diverges: AI's category boundary",
        "chart_slot": "f3_rank_shift_t1",
        "paragraphs": [
            (
                "1 of 3 AI-top-three brands appear in the Trends top-five \u2014 at both waves. "
                "Linear (AI rank 1, Trends rank 14) and Todoist (AI rank 17, Trends rank 9) "
                "bracket the same diagnostic from opposite ends."
            ),
            (
                "<b>H3 is falsified.</b> At t<sub>1</sub>, the AI-top-three is Linear, Asana, "
                "Notion. The Trends-top-five is Notion, Jira, Trello, ClickUp, Confluence. "
                "Only Notion appears in both. At t<sub>2</sub>, the AI-top-three is Linear, "
                "Asana, Jira; the Trends-top-five is unchanged from t<sub>1</sub>. Only Jira "
                "appears in both. The divergence concentrates at the top of the AI Presence "
                "distribution \u2014 the zone where AI Presence carries the most predictive "
                "weight for purchase decisions."
            ),
            (
                "<b>The Linear paradox.</b> Linear has the highest AI Presence in the registry "
                "(86.5% at t<sub>1</sub>, 89.6% at t<sub>2</sub>) and the second-lowest Trends "
                "value (rescaled mean 1.88 at t<sub>1</sub>; Asana indexed to 100 by "
                "construction). AI systems strongly recommend Linear despite the brand's "
                "negligible consumer search interest. The bare query 'Linear' returns Google "
                "Trends results dominated by linear-algebra textbooks; the brand-disambiguated "
                "query <i>'linear project management'</i> returns the residual signal reported "
                "here."
            ),
            (
                "<b>The Todoist inverse.</b> Todoist has the second-lowest AI Presence at "
                "t<sub>1</sub> (1.04%; effectively zero at t<sub>2</sub>) and Trends value "
                "28.38 \u2014 comparable to GitHub Projects (28.01), which receives 42.7% "
                "AI Presence. At similar consumer search interest, AI grants GitHub Projects "
                "40\u00d7 more recommendation share. The mechanism is plausibly category-boundary: "
                "AI frames Todoist as a personal task manager rather than a project management "
                "tool, and excludes it from PM recommendations."
            ),
            (
                "Both diagnostics support the same substantive finding: <b>AI applies a "
                "tighter and partly-different category boundary than consumers do.</b> Linear "
                "is inside AI's PM category but barely inside consumers' search-revealed one; "
                "Todoist is outside AI's PM category but well inside consumers' search-revealed "
                "one. The construct of AI Availability is empirically distinct from Mental "
                "Availability \u2014 and the distinction is structural, not noise."
            ),
        ],
    },
    {
        "number": 4,
        "title": "Brand age and tier absorb part of the H1 signal",
        "chart_slot": "f4_partial_residual_t1",
        "paragraphs": [
            (
                "Partial Spearman <font name='Helvetica'>\u03c1</font> after controlling for brand age and "
                "competitive density: 0.41 at t<sub>1</sub>, 0.43 at t<sub>2</sub>. H4 "
                "falsified at the magnitude bar; t<sub>1</sub> also misses statistical "
                "significance."
            ),
            (
                "H4 controls for two pre-registered covariates: brand age (years since product "
                "launch) and competitive density (market tier from the v0.6 registry, treated "
                "as ordinal). The control removes the most obvious confounds: older brands "
                "tend to have more consumer search interest and may have accumulated more AI "
                "training-data presence; incumbents differ structurally from challengers on "
                "both axes."
            ),
            (
                "After this control, the H1 correlation falls from 0.50 to 0.41 (t<sub>1</sub>) "
                "and from 0.48 to 0.43 (t<sub>2</sub>). <b>H4 is falsified at the magnitude "
                "bar</b> (partial <font name='Helvetica'>\u03c1</font> &gt; 0.5 required). t<sub>1</sub> "
                "also fails the significance bar (one-tailed p = 0.066); t<sub>2</sub> clears "
                "it (p = 0.049). The pattern points to real confound absorption: a meaningful "
                "component of H1's signal was age-and-tier covariation between AI Presence and "
                "search interest."
            ),
            (
                "Per-row inspection confirms this. Workfront (24 years, mid-tier) has AI "
                "Presence 1.04% and Trends 6.67. Wrike (20 years, mid-tier) has AI 8.33 and "
                "Trends 12. Linear and Motion (both 7 years, challenger) over-perform their "
                "search-implied AI Presence; older mid-tier brands under-perform. The covariate "
                "control removes this systematic drift, exposing the partial relationship "
                "below it."
            ),
        ],
    },
]

# ----------------------------------------------------------------------------
# HYPOTHESIS SCORING TABLE
# Each row is a 5-tuple: (h_id, prediction, result, status_text, status_class).
# status_class is one of: "confirmed", "partial", "disconfirmed", "descriptive".
# ----------------------------------------------------------------------------

HYPOTHESIS_SCORING = {
    "heading": "Hypothesis Scoring",
    "intro": (
        "All thresholds and tests locked at <i>v0.11-prereg</i> (commit f20ade8, "
        "10 May 2026 UTC) prior to any Google Trends acquisition call against the "
        "wave windows. Pivot brand (Asana) exempted from at-acquisition E1b rule per "
        "pre-reg \u00a75.1 (sd = 0 by pivot construction). Height (defunct September "
        "2025) retained as phantom brand per registry-frozen-ness convention. "
        "n-floor evaluation: t<sub>1</sub> n = 17, t<sub>2</sub> n = 18 against the "
        "16-of-19 floor."
    ),
    "rows": [
        (
            "H1",
            "Spearman <font name='Helvetica'>\u03c1</font> &gt; 0.5 AND p<sub>1t</sub> &lt; 0.05, both waves",
            "<font name='Helvetica'>\u03c1</font><sub>t<sub>1</sub></sub> = 0.496 (p = 0.021); "
            "<font name='Helvetica'>\u03c1</font><sub>t<sub>2</sub></sub> = 0.476 (p = 0.023)",
            "FALSIFIED",
            "disconfirmed",
        ),
        (
            "H2",
            "|<font name='Helvetica'>\u0394\u03c1</font>| \u2264 0.15",
            "|<font name='Helvetica'>\u0394\u03c1</font>| = 0.020",
            "CONFIRMED",
            "confirmed",
        ),
        (
            "H3",
            "AI top-3 \u2286 Trends top-5, both waves",
            "1 / 3 at both waves",
            "FALSIFIED",
            "disconfirmed",
        ),
        (
            "H4",
            "Partial <font name='Helvetica'>\u03c1</font> &gt; 0.5 AND p<sub>1t</sub> &lt; 0.05, both waves",
            "partial <font name='Helvetica'>\u03c1</font><sub>t<sub>1</sub></sub> = 0.41 (p = 0.066); "
            "partial <font name='Helvetica'>\u03c1</font><sub>t<sub>2</sub></sub> = 0.43 (p = 0.049)",
            "FALSIFIED",
            "disconfirmed",
        ),
        (
            "H1<sub>r</sub>",
            "Pearson r &gt; 0.5 AND p &lt; 0.05, both waves (sensitivity)",
            "r<sub>t<sub>1</sub></sub> = 0.544; r<sub>t<sub>2</sub></sub> = 0.533",
            "CONFIRMED (sensitivity)",
            "descriptive",
        ),
        (
            "H1<sub>US</sub>",
            "Spearman <font name='Helvetica'>\u03c1</font> &gt; 0.5 AND p &lt; 0.05, both waves (US sensitivity)",
            "<font name='Helvetica'>\u03c1</font><sub>t<sub>1</sub></sub> = 0.489; "
            "<font name='Helvetica'>\u03c1</font><sub>t<sub>2</sub></sub> = 0.455",
            "FALSIFIED (sensitivity)",
            "descriptive",
        ),
    ],
}

# ----------------------------------------------------------------------------
# HYPOTHESIS DETAILS (per-hypothesis expansion below the scoring table)
# items is a list of (h_id, body_html) tuples.
# ----------------------------------------------------------------------------

HYPOTHESIS_DETAILS = {
    "heading": "Hypothesis Details",
    "intro": (
        "Per-hypothesis claim, operationalisation, and result. All confirm/falsify decisions "
        "use the pre-registered thresholds; the both-waves conjunction provides FWER control "
        "for H1 and H4 by construction (joint p \u2248 0.05\u00b2 = 0.0025 under the null)."
    ),
    "items": [
        (
            "H1",
            (
                "<b>H1 \u2014 Cross-Sectional Construct Validity.</b> "
                "Per-brand AI Presence rate co-varies with per-brand Google Trends search-"
                "interest index at sufficient strength to support the construct. "
                "Spearman <font name='Helvetica'>\u03c1</font> across the eligible brand set per wave; "
                "confirmed if <font name='Helvetica'>\u03c1</font> &gt; 0.5 AND p<sub>1t</sub> &lt; 0.05 at "
                "both waves. <b>Status: FALSIFIED.</b> "
                "<font name='Helvetica'>\u03c1</font><sub>t<sub>1</sub></sub> = 0.496 (p = 0.021); "
                "<font name='Helvetica'>\u03c1</font><sub>t<sub>2</sub></sub> = 0.476 (p = 0.023). "
                "Significance bar cleared both waves; magnitude bar missed at t<sub>1</sub> by "
                "0.004 and at t<sub>2</sub> by 0.024. Direction supported; strength is not."
            ),
        ),
        (
            "H2",
            (
                "<b>H2 \u2014 Correlation Stability.</b> "
                "The H1 correlation strength is stable across t<sub>1</sub> \u2192 t<sub>2</sub>. "
                "|<font name='Helvetica'>\u03c1</font><sub>t<sub>2</sub></sub> \u2212 "
                "<font name='Helvetica'>\u03c1</font><sub>t<sub>1</sub></sub>|; confirmed if \u2264 0.15. "
                "<b>Status: CONFIRMED.</b> |<font name='Helvetica'>\u0394\u03c1</font>| = 0.020 \u2014 "
                "almost an order of magnitude below tolerance. The construct's measurement "
                "reproduces near-identically across waves. Whatever H1 captured at t<sub>1</sub> "
                "was captured again at t<sub>2</sub>; the just-miss is not a sampling artefact."
            ),
        ),
        (
            "H3",
            (
                "<b>H3 \u2014 Leaderboard Directional Consistency.</b> "
                "Brands ranked top-3 by AI Presence are also among the top-5 by Trends, at "
                "each wave. Confirmed if all 3 of the AI-top-3 appear in the Trends top-5, at "
                "both waves. <b>Status: FALSIFIED at both waves.</b> 1/3 at each wave. "
                "t<sub>1</sub> overlap: Notion. t<sub>2</sub> overlap: Jira. Linear and Asana "
                "\u2014 the top two by AI Presence at both waves \u2014 fall outside the Trends "
                "top-5 at both waves. The construct divergence is concentrated at the leadership "
                "zone of the AI Presence distribution. See Finding 3 for the Linear paradox and "
                "Todoist inverse diagnostic."
            ),
        ),
        (
            "H4",
            (
                "<b>H4 \u2014 Covariate-Controlled.</b> "
                "The H1 correlation survives partialling out brand age and within-category "
                "competitive density. Pearson correlation on rank residuals after OLS on rank-"
                "transformed covariates (brand age years; tier ordinal incumbent=1 / mid=2 / "
                "challenger=3); df corrected for k = 2. Confirmed if partial "
                "<font name='Helvetica'>\u03c1</font> &gt; 0.5 AND p &lt; 0.05 at both waves. "
                "<b>Status: FALSIFIED.</b> Partial "
                "<font name='Helvetica'>\u03c1</font><sub>t<sub>1</sub></sub> = 0.407 (p = 0.066); "
                "partial <font name='Helvetica'>\u03c1</font><sub>t<sub>2</sub></sub> = 0.428 (p = 0.049). "
                "The H1 correlation loses meaningful strength under covariate control, "
                "indicating that age-and-tier covariation accounts for a non-trivial portion "
                "of the H1 signal."
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
            "<b>Single category.</b> v0.11 tests one of the five v0.6 baseline categories. "
            "The H1 just-miss, H3 falsification, and H4 covariate-controlled weakening are "
            "PM-software findings; their generalisation to running shoes, premium olive oil, "
            "premium facial skincare, and personal finance is the v0.12 hypothesis space, not "
            "a v0.11 claim."
        ),
        (
            "<b>Single validator.</b> Google Trends search interest is one behavioural proxy "
            "for brand mindshare. Other validators \u2014 purchase data, brand-tracker survey "
            "measures, social-media share-of-voice \u2014 were not measured. A construct that "
            "doesn't correlate with one external proxy may correlate with another; v0.11's "
            "result is specifically about the AI-Presence-vs-search-interest relationship."
        ),
        (
            "<b>Small n.</b> 17\u201318 brands per wave. The pre-registered floor was 16-of-19; "
            "v0.11 cleared it with margin, but the small-n constraint is real. The "
            "<font name='Helvetica'>\u03c1</font>-statistic's standard error is roughly 0.20 at n = 17, "
            "which is why H2's 0.02-magnitude stability is striking evidence of reproducibility "
            "rather than expected variance."
        ),
        (
            "<b>Trends index, not raw volume.</b> Google Trends exposes only the bundle-"
            "normalised 0\u2013100 search-interest index, not raw query counts. The pivot-"
            "rescaling protocol in v0.11 makes the indices cross-brand comparable, but the "
            "absolute query volume per brand cannot be recovered. The 'Asana = 100' baseline "
            "is structural, not substantive."
        ),
        (
            "<b>Two waves seven days apart.</b> H2's stability claim is about the same "
            "construct measured twice across one week; it is not a claim about long-horizon "
            "stability. The v0.12 timing decision (next acquisition windows) will partly "
            "determine how far the H2 finding can be extrapolated."
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
            "<b>v0.12 \u2014 Three-category Phase 3 expansion.</b> Add running shoes and "
            "premium olive oil to the PM-software protocol. The sharpened question: does the "
            "H1 just-miss + H3 leadership-zone divergence pattern generalise, or is it specific "
            "to PM-software's category-boundary structure? Premium olive oil's leadership zone "
            "is stable across both AI and consumer search (Brightland, Graza, Castillo de "
            "Canena) and is the cleanest replication candidate; running shoes will test the "
            "pattern under high-brand-density competitive conditions."
        ),
        (
            "<b>v0.13 \u2014 Full-category construct validity panel.</b> Extend to the "
            "remaining two v0.6 baseline categories (premium facial skincare, personal "
            "finance). Personal finance carries the Mint phantom-brand effect documented in "
            "v0.7 and v0.10 and is expected to show the largest construct divergence."
        ),
        (
            "<b>Tri-System Brand Growth manuscript</b> (Gonzalez Castro, 2026, in preparation). "
            "The v0.11 findings sharpen the framework's empirical content. The Linear paradox "
            "and Todoist inverse are candidate empirical anchors for the framework's "
            "distinctness claim \u2014 AI Availability as a third system distinct from Mental "
            "and Physical Availability."
        ),
        (
            "<b>Phase 4 (AIAS components 2\u20136).</b> Construct validity established for AI "
            "Presence in v0.11\u2013v0.13 is a precondition for measurement work on Ranking, "
            "Consistency, Coverage, Grounding, and Sentiment."
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
            "OSF project ec6wh, /v11/. Inputs (v0.9 AI Presence rates), Google Trends raw "
            "responses (10 pivot-bundle JSONs across 2 regions), topic-ID suggestion logs, "
            "pre-acquisition validation outputs, brand age source table, registry files, "
            "scoring outputs, build scripts, this report, and the matching SSRN working "
            "paper."
        ),
        (
            "Cross-references: AI Availability foundational paper (SSRN 6659000); AIAS "
            "Presence Measurement Protocol v1.1 (SSRN 6722319); v0.6 Cross-Category "
            "Findings (SSRN 6720959); v0.7 Phantom-Brand Persistence Phase 2 BBB "
            "(SSRN 6721779); v0.8 Discourse-Language Knives (SSRN 6728000); v0.9 "
            "Longitudinal Re-Baseline (SSRN 6736878); v0.10 Naive-Phantom Rate Stability "
            "(SSRN 6741163)."
        ),
    ],
    "methodology_log": (
        "v0.11 follows AIAS Presence Measurement Protocol v1.1 (unchanged from v0.9). "
        "Pre-registration locked at git tag v0.11-prereg (commit f20ade8) on 10 May 2026 "
        "UTC prior to acquisition. Acquisition session UTC timestamp captured in "
        "trends_acquisition_log.csv. No deviations from the pre-reg recorded as of "
        "publication."
    ),
}
