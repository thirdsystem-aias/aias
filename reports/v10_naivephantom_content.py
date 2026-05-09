"""
v0.10 Naive-Phantom Rate Longitudinal Stability — structured content.

Mirrors v09_rebaseline_content.py top-level structure so build_report_v10.py
can fork build_report_v09.py with minimal changes.

Differences from v09:
  - Subject is a single-brand designed-for-test extension, not a five-category
    longitudinal study. One brand (Mint), two waves (t1, t2), three
    pre-registered hypotheses (H1, H2, H3).
  - Story arc: "the floor breached; descriptive disclosure honors pre-reg
    discipline; H2 falsifies cleanly; one Sonnet 4.6 case is existence proof."
  - Three findings instead of v0.9's seven.
  - HYPOTHESIS_SCORING table has three rows.
  - No THREE_MODES, no HYPOTHESIS_DETAILS (the patterns themselves carry the
    per-hypothesis reasoning at greater depth than v0.9's small details table).
"""

# ---- Cover ---------------------------------------------------------------

COVER = {
    "title": "Naive-Phantom Rate Stability",
    "subtitle": ("AI Presence Index v0.10 \u2014 Mint, designed-for-test "
                 "extension, t<sub size='10'>1</sub>"
                 "\u00a0\u2192\u00a0"
                 "t<sub size='10'>2</sub>"),
    "date": "9 May 2026",
    "byline_short": "Pablo Ulpiano Gonz\u00e1lez Castro \u00b7 Third System\u2122",
    "tagline": "Independent measurement for the AI mediation layer.",
}

# ---- Lead spread ---------------------------------------------------------

STANDFIRST = "The phantom is mostly extinguished. Mostly."

LEAD_DECK = (
    "v0.7 measured a small but non-zero naive-phantom rate for Mint at the "
    "v0.6 baseline (1.7 percent). v0.9 confirmed gross Presence stability at "
    "matched-subset n. v0.10 tests the question v0.9 H4 left open: is the "
    "naive-phantom subset \u2014 recommendation slots delivered without "
    "caveat \u2014 as durable as gross Presence? The matched-subset n "
    "breached the pre-registered floor and routed H1 to descriptive "
    "disclosure. Within that path: zero naive at t<sub size='6'>1</sub> (43 of 43 caveated), "
    "one naive at t<sub size='6'>2</sub> (1 of 40). H2 falsified. H3 decoupled. The single "
    "t<sub size='6'>2</sub> case stands as existence proof that naive-phantom presence has "
    "not yet been fully extinguished from frontier-model substrates."
)

# ---- Executive summary ---------------------------------------------------

EXEC_SUMMARY = [
    (
        "Third System applied the v0.7 caveat-classifier to v0.9's deposited "
        "raw responses, restricted to Mint within the matched two-model "
        "subset (Anthropic Claude Sonnet 4.6 and OpenAI gpt-5.4-mini). Three "
        "hypotheses were pre-registered: <b>H1 stability</b> (\u00b12pp band, "
        "n\u2265100 floor), <b>H2 persistence</b> (r<sub size='6'>naive</sub> &gt; 0 at "
        "both waves), and <b>H3 co-movement</b> (diagnostic). "
        "Pre-registration locked at git commit <font name='Helvetica'>8767f44</font>, "
        "tag <font name='Helvetica'>v0.10-prereg</font>, on 2026-05-09, prior to any "
        "application of the classifier to the Mint subset."
    ),
    (
        "<b>The floor breached.</b> Matched-subset n at t<sub size='6'>1</sub> = 43; at "
        "t<sub size='6'>2</sub> = 40. Both below the pre-registered n\u2265100 required for "
        "H1 confirmatory inference. Pre-reg \u00a73.4 routed H1 to the "
        "descriptive disclosure path \u2014 exactly the case the floor was "
        "specified to handle. The pre-registered band is not invoked; the "
        "small-n descriptive picture is reported in its place."
    ),
    (
        "<b>H2 falsified.</b> r<sub size='6'>naive</sub>,t<sub size='6'>1</sub> = 0.00 percent (0/43); "
        "r<sub size='6'>naive</sub>,t<sub size='6'>2</sub> = 2.50 percent (1/40). Every Mint mention "
        "at t<sub size='6'>1</sub> in the matched subset carried some form of caveat \u2014 "
        "100 percent classifier-detectable correction at the v0.6 baseline "
        "measurement window. The single naive case at t<sub size='6'>2</sub> is in "
        "claude-sonnet-4-6, prompt <font name='Helvetica'>p1_functional</font>, run 3: "
        "Mint listed at the top of \u201cFree Options\u201d, described in "
        "present tense with feature details, and explicitly recommended as "
        "\u201cthe most common starting point for beginners.\u201d No caveat. "
        "Adjudication confirmed the classifier without override."
    ),
    (
        "<b>H3 decoupled.</b> Gross Presence falls (\u22123.12pp from 44.79 "
        "to 41.67 percent) while the naive rate rises (+2.50pp from 0 to 2.5 "
        "percent). The directional change is opposite. At small n the "
        "pattern is noise-dominated and reported as diagnostic only. If "
        "substantively replicated at higher n, the asymmetry would suggest "
        "the naive subset and the gross subset are governed by partly "
        "different mechanisms."
    ),
    (
        "<b>The result is honest, narrow, and methodologically clean.</b> "
        "The pre-registered floor caught a real small-n problem before it "
        "could be rationalized away. Four deviations from the "
        "pre-registration's descriptive language \u2014 the v0.7 classifier "
        "is LLM-only, not the rule-list-plus-judge protocol pre-reg \u00a75 "
        "described \u2014 are documented in DEVIATIONS.md and summarized in "
        "the SSRN paper. The substantive instruction (\u201cinherit v0.7 "
        "unchanged\u201d) is preserved. v0.10 ships as descriptive "
        "disclosure plus existence proof rather than confirmatory "
        "measurement."
    ),
]

# ---- What we measured ----------------------------------------------------

WHAT_WE_MEASURED = {
    "heading": "What we measured",
    "paragraphs": [
        (
            "v0.7 (Phantom-Brand BBB) introduced a designed-for-test reframe "
            "distinguishing two phantom-brand presence types: "
            "<i>naive-phantom presence</i> (recommendation as live, no "
            "caveat anywhere in the response) and <i>caveated-phantom "
            "presence</i> (mention with explicit acknowledgment of "
            "decommissioning, sunset, or migration). At the v0.7 BBB "
            "measurement against the v0.6 baseline data, the naive-phantom "
            "rate for Mint was 1.7 percent, against a gross Presence rate "
            "of 38.2 percent."
        ),
        (
            "v0.9 (Longitudinal Re-Baseline) confirmed gross Presence "
            "stability for Mint across the v0.6\u2192v0.9 measurement "
            "interval within the pre-registered \u00b15pp band (44.8 "
            "percent \u2192 41.7 percent, |\u0394|=3.1pp). What v0.9 H4 did "
            "<i>not</i> test is whether the naive-phantom subset exhibits "
            "comparable stability \u2014 whether AI systems\u2019 tendency "
            "to recommend Mint as if fully live persists at the same rate "
            "over the longitudinal interval, separately from the "
            "gross-mention rate."
        ),
        (
            "v0.10 tests this question. The v0.7 caveat-classifier is "
            "applied to the Mint-restricted subset of v0.9's deposited raw "
            "responses across the matched two-model subset (Sonnet 4.6, "
            "gpt-5.4-mini). No new measurement; no new model calls; no new "
            "data collection. The pre-registration locks three hypotheses "
            "with explicit numerical thresholds and an effective-n floor of "
            "100 per wave. Floor breach routes H1 to descriptive disclosure "
            "as pre-specified."
        ),
        (
            "All raw responses, classifier outputs, scoring scripts, "
            "adjudication log, and four deviations from pre-reg "
            "descriptive language are deposited at OSF project "
            "<font name='Helvetica'>ec6wh</font>, path <font name='Helvetica'>/v10/</font>. The pre-registration "
            "document is locked at git commit <font name='Helvetica'>8767f44</font>, tag "
            "<font name='Helvetica'>v0.10-prereg</font>, 2026-05-09."
        ),
    ],
}

# ---- Patterns / Findings -------------------------------------------------

PATTERNS = [
    {
        "number": 1,
        "title": "The floor breached. Descriptive disclosure engages.",
        "chart_slot": "hero_f1_valence",
        "paragraphs": [
            (
                "Exact-token match of <i>Mint</i> in the v0.9 raw responses\u2019 "
                "<font name='Helvetica'>brands_canonical</font> field, restricted to the matched "
                "two-model subset (Sonnet 4.6 + gpt-5.4-mini), yielded "
                "<b>43 Mint-bearing rows at t<sub size='6'>1</sub></b> and <b>40 at t<sub size='6'>2</sub></b>. "
                "Both well below the pre-registered n\u2265100 floor for H1 "
                "confirmatory inference."
            ),
            (
                "Pre-reg \u00a73.4 specified the floor as a single-flip "
                "resolution constraint: at n=100, a single response "
                "classification change moves r<sub size='6'>naive</sub> by 1.0pp \u2014 "
                "half the \u00b12pp stability band. Below that floor, the "
                "test cannot distinguish meaningful drift from sampling "
                "noise. The specified response is to route H1 to "
                "descriptive disclosure, not to relax the threshold or "
                "promote the descriptive observation to a confirmatory "
                "claim."
            ),
            (
                "The classifier output \u2014 v0.7\u2019s 5-class valence "
                "(<i>live_recommendation</i>, <i>live_with_caveat</i>, "
                "<i>status_correction</i>, <i>historical_reference</i>, "
                "<i>ambiguous</i>) \u2014 is dominated by "
                "<b>status_correction</b> at both waves: 21 of 43 at "
                "t<sub size='6'>1</sub> (48.8 percent) and 20 of 40 at t<sub size='6'>2</sub> (50.0 "
                "percent). This is the strongest caveat type, an explicit "
                "\u201cMint is decommissioned/sunset/closed\u201d framing, "
                "distinct from a hedged recommendation."
            ),
            (
                "<i>historical_reference</i> and <i>live_with_caveat</i> "
                "make up the remainder of the caveated cases. Zero "
                "<i>ambiguous</i> classifications were produced; the E3 "
                "sensitivity mapping (which would re-route ambiguous cases "
                "to the caveated bin) is therefore identical to the "
                "primary mapping."
            ),
            (
                "The descriptive picture is clean even under the floor "
                "breach. Within the data we have, classifier-detectable "
                "correction covers virtually every Mint surfacing in the "
                "matched-subset frontier-model substrate \u2014 and at "
                "t<sub size='6'>1</sub> specifically, every single one. The proper read "
                "is not \u201cmeasurement failed\u201d; it is "
                "\u201cmeasurement honestly disclosed below confirmatory "
                "threshold,\u201d with three pre-registered observations "
                "to follow."
            ),
        ],
    },
    {
        "number": 2,
        "title": "H2 falsified. One Sonnet 4.6 case is existence proof.",
        "chart_slot": "hero_f2_h2_split",
        "paragraphs": [
            (
                "H2 (persistence): r<sub size='6'>naive</sub> &gt; 0 at both waves. "
                "<b>Falsified.</b> n<sub size='6'>naive</sub>,t<sub size='6'>1</sub> = 0; "
                "n<sub size='6'>naive</sub>,t<sub size='6'>2</sub> = 1. Every Mint mention at t<sub size='6'>1</sub> in "
                "the matched subset carries some form of caveat \u2014 100 "
                "percent classifier-detectable correction at the v0.6 "
                "baseline measurement window."
            ),
            (
                "This is a stronger correction baseline than v0.7 BBB "
                "recorded for Mint at the same v0.6 measurement (which "
                "found 1.7 percent naive). Three non-mutually-exclusive "
                "explanations: v0.7\u2019s classifier was applied to a "
                "broader response set including models beyond the matched "
                "two; substrate evolution between v0.7\u2019s measurement "
                "window (4 May 2026) and v0.10\u2019s (9 May 2026, applied "
                "to v0.9\u2019s t<sub size='6'>1</sub> collection); and small-n sampling "
                "noise within the matched-subset restriction. The data do "
                "not adjudicate among them."
            ),
            (
                "<b>The single t<sub size='6'>2</sub> naive case</b> is "
                "claude-sonnet-4-6, prompt <font name='Helvetica'>p1_functional</font>, run 3. "
                "The response lists Mint at the top of a \u201cFree "
                "Options\u201d list. It describes the product\u2019s "
                "features in present tense \u2014 \u201cComprehensive, "
                "links to bank accounts, automatic categorization\u201d "
                "\u2014 and explicitly recommends it as \u201cthe most "
                "common starting point for beginners.\u201d No caveat "
                "about decommissioning, shutdown, or migration to Credit "
                "Karma anywhere in the response. The classifier valence "
                "(<i>live_recommendation</i>) and binary mapping (naive) "
                "were both confirmed without author override."
            ),
            (
                "The case constitutes existence proof at the substrate "
                "level. A frontier model (Sonnet 4.6) recommends a "
                "decommissioned product \u2014 Mint, two years past "
                "decommissioning at the t<sub size='6'>2</sub> collection date \u2014 as "
                "a top current option in its category, with present-tense "
                "feature description and explicit endorsement as a "
                "beginner\u2019s first choice. The phenomenon is not yet "
                "fully extinguished from frontier-model retrieval and "
                "response-generation pipelines."
            ),
            (
                "What the case is <i>not</i>: representative. One naive "
                "instance in 40 is consistent with rates anywhere from "
                "essentially zero to a few percent at population scale. "
                "What v0.10 has shown is that the rate is non-zero in this "
                "wave and zero in the previous wave \u2014 enough to "
                "falsify H2\u2019s formal prediction (r<sub size='6'>naive</sub> &gt; 0 at "
                "<i>both</i> waves) without resolving the question of "
                "whether naive-phantom presence is structurally drifting "
                "in either direction."
            ),
        ],
    },
    {
        "number": 3,
        "title": "H3 decoupled. Gross down, naive up.",
        "chart_slot": "hero_f3_decoupling",
        "paragraphs": [
            (
                "H3 (co-movement, diagnostic): the directional change in "
                "naive-phantom rate is consistent with the directional "
                "change in gross Presence. <b>Decoupled.</b> "
                "\u0394gross = \u22123.12pp; \u0394naive = +2.50pp. The "
                "directions are opposite; the magnitude ratio "
                "|\u0394r<sub size='6'>naive</sub>| / |\u0394r<sub size='6'>gross</sub>| = 0.80."
            ),
            (
                "At the matched-subset n observed (43 and 40), the pattern "
                "is noise-dominated. A single classification flip in "
                "either wave moves r<sub size='6'>naive</sub> by 2.3 to 2.5pp. The H3 "
                "result is reported as diagnostic only per pre-reg "
                "\u00a72; no falsification status is assigned, regardless "
                "of how striking the visual impression of decoupling "
                "looks."
            ),
            (
                "If substantively replicated at higher n, the asymmetry "
                "would be informative. Two readings, not mutually "
                "exclusive: <b>(a)</b> as caveat coverage matures across "
                "the model substrate, the residual naive cases become "
                "structurally harder to correct \u2014 perhaps because "
                "they arise from prompt formulations or response paths "
                "that bypass the typical correction pipeline. <b>(b)</b> "
                "the naive subset and the gross subset are governed by "
                "partly different mechanisms: gross presence by "
                "training-data prevalence and retrieval propensity, naive "
                "subset by the response-time decision to caveat or not."
            ),
            (
                "Either reading would have implications for measurement "
                "strategy. The first suggests naive-phantom rates may "
                "stabilize near a positive floor rather than tend to zero. "
                "The second suggests gross Presence and naive-phantom rate "
                "should be tracked as separate metrics with separate "
                "stability bands rather than treated as proportional or "
                "co-moving."
            ),
            (
                "A higher-volume study at n\u2265100 per wave would "
                "distinguish noise from signal. The same dataset cannot. "
                "v0.10 records the diagnostic for the program log; "
                "confirmatory inference about co-movement waits."
            ),
        ],
    },
]

# ---- Hypothesis scoring --------------------------------------------------

# Status classes (controls table-cell styling in build_hypothesis_scoring_story):
#   "confirmed"    bold
#   "partial"      default
#   "disconfirmed" default
#   "descriptive"  italic
HYPOTHESIS_SCORING = {
    "heading": "Pre-registration outcome",
    "intro": (
        "Three hypotheses were pre-registered. H1 was routed to descriptive "
        "disclosure under the n\u2265100 floor breach. H2 was evaluated as "
        "confirmatory and falsified. H3 was reported as diagnostic without "
        "falsification status. Detailed evaluation, per-wave metrics, and "
        "the single naive case quote in full are in the v0.10 SSRN paper "
        "(deposited at OSF project ec6wh, /v10/papers/)."
    ),
    "rows": [
        (
            "H1",
            "|\u0394r<sub size='6'>naive</sub>| \u2264 2.0pp; n\u2265100 floor required "
            "at both waves",
            "Floor breached: n,t<sub size='6'>1</sub> = 43; n,t<sub size='6'>2</sub> = 40. Routed to "
            "descriptive disclosure path per pre-reg \u00a73.4. Descriptive "
            "|\u0394r<sub size='6'>naive</sub>| = 2.50pp.",
            "INDETERMINATE",
            "descriptive",
        ),
        (
            "H2",
            "r<sub size='6'>naive</sub> &gt; 0 at both waves",
            "n<sub size='6'>naive</sub>,t<sub size='6'>1</sub> = 0; n<sub size='6'>naive</sub>,t<sub size='6'>2</sub> = 1. The single naive "
            "case is sonnet-4-6, p1_functional, run 3.",
            "FALSIFIED",
            "disconfirmed",
        ),
        (
            "H3",
            "Diagnostic; co-movement direction reported without "
            "falsification status",
            "\u0394gross = \u22123.12pp; \u0394naive = +2.50pp. Decoupled "
            "directional change. Magnitude ratio 0.80.",
            "DIAGNOSTIC",
            "descriptive",
        ),
    ],
}

# ---- Limitations ---------------------------------------------------------

LIMITATIONS = {
    "heading": "Limitations",
    "paragraphs": [
        (
            "<b>Sample size.</b> The matched-subset n at both waves is "
            "below the pre-registered floor of 100 per wave. Descriptive "
            "observations only; no inference about the population-level "
            "naive-phantom rate beyond the v0.6\u2192v0.9 longitudinal "
            "window measured here."
        ),
        (
            "<b>Single-brand scope.</b> v0.10 measures Mint only. "
            "Generalization to other phantom brands requires additional "
            "study. The v0.7 BBB result (1.7 percent naive at v0.6) and "
            "v0.10 Mint result (0 percent at t<sub size='6'>1</sub>, 2.5 percent at "
            "t<sub size='6'>2</sub>), taken together, suggest naive rates in the "
            "low-single-digit percentage range \u2014 consistent across "
            "two brands, but a sample of two."
        ),
        (
            "<b>Classifier validation.</b> The v0.7 classifier is a single "
            "<font name='Helvetica'>gpt-5.4-mini</font> call at temperature 0 with the v0.7 "
            "system prompt and tool schema applied. It has not been "
            "independently calibrated for inter-rater agreement at the "
            "v0.10 measurement window. The single naive case was "
            "author-adjudicated and confirmed; no override was applied. "
            "Author agreement with the classifier on the high-information "
            "case (the single naive instance) is not equivalent to "
            "calibration on the broader caveated set."
        ),
        (
            "<b>Substrate evolution.</b> AI training and retrieval "
            "substrates evolve continuously. The present result is a "
            "snapshot within v0.9\u2019s measurement windows (April-May "
            "2026); it does not characterize the phenomenon\u2019s "
            "trajectory across longer time scales or across documented "
            "model-pipeline transitions."
        ),
        (
            "<b>Pre-reg description vs v0.7 reality.</b> Four deviations "
            "from the pre-registration\u2019s descriptive language are "
            "documented in DEVIATIONS.md. The substantive pre-reg "
            "instruction (\u201cinherit v0.7 unchanged\u201d) is "
            "preserved. Deviations stem from a single root cause: "
            "pre-reg \u00a75 described the v0.7 classifier as a "
            "\u201ckeyword/phrase rule list and judge-LLM verification "
            "protocol\u201d; the actual v0.7 classifier is LLM-only with "
            "no rule list and no separate judge step. The classifier "
            "configuration applied at v0.10 is the actual v0.7, "
            "documented at registries/v07_caveat_classifier.json."
        ),
    ],
}

# ---- What's next ---------------------------------------------------------

WHATS_NEXT = {
    "heading": "What\u2019s next",
    "paragraphs": [
        (
            "<b>Higher-volume replication.</b> A v0.10b collection at a "
            "third time point t<sub size='6'>3</sub> specifically scaled to clear the "
            "n\u2265100 floor would enable confirmatory inference on H1. "
            "The most direct design is higher prompt-count per wave on "
            "the same matched subset, or careful expansion of the matched "
            "subset to include additional models where methodologically "
            "defensible (the matched-subset constraint exists to control "
            "for cross-model heterogeneity; relaxing it for n requires "
            "explicit accounting)."
        ),
        (
            "<b>Multi-brand replication.</b> Extending the v0.7/v0.10 "
            "protocol to additional phantom brands \u2014 Toys "
            "\u201cR\u201d Us, Circuit City, RadioShack, Pier 1, "
            "JCPenney post-bankruptcy, or comparable domain-specific "
            "phantoms \u2014 would establish whether the "
            "low-single-digit naive rate is a category-general property "
            "of the phenomenon or specific to particular brands. A "
            "designed-for-test multi-brand naive-phantom study is the "
            "natural v0.11 candidate."
        ),
        (
            "<b>Longer-interval longitudinal characterization.</b> The "
            "present seven-day t<sub size='6'>1</sub>\u2192t<sub size='6'>2</sub> interval is short "
            "relative to typical model retraining cycles. Repeating the "
            "v0.10 protocol at one-month, three-month, and twelve-month "
            "intervals \u2014 particularly across documented "
            "model-pipeline transitions or training-cutoff updates "
            "\u2014 would characterize the phenomenon\u2019s trajectory "
            "at scales relevant to substrate evolution rather than "
            "within-window noise."
        ),
        (
            "<b>Mechanism-level decomposition.</b> If the H3 decoupling "
            "diagnostic replicates at higher n, the naive subset and "
            "gross subset may be governed by partly different mechanisms. "
            "Designed-for-test studies isolating the response-time "
            "decision to caveat (as opposed to the retrieval-time "
            "decision to surface) would clarify the mechanism. "
            "Candidates: prompt-level cues that force or suppress "
            "temporal context; ablation of specific portions of the "
            "response generation context; comparison of decoder-time "
            "behavior at matched retrieval states."
        ),
        (
            "<b>Methodology paper.</b> A v1.x AIAS Presence Measurement "
            "Protocol paper, building on v1.1 and the v0.7\u2192v0.10 "
            "designed-for-test thread, will document the "
            "naive-vs-caveated distinction as a first-class dimension of "
            "the measurement program rather than a v0.7-specific "
            "extension. v0.10\u2019s descriptive disclosure path \u2014 "
            "and the four deviations between pre-reg description and v0.7 "
            "classifier reality \u2014 are useful inputs."
        ),
    ],
}

# ---- Closing matter ------------------------------------------------------

CLOSING = {
    "byline_long": [
        "<b>Pablo Ulpiano Gonz\u00e1lez Castro</b>",
        "School of Visual Arts, MPS Branding Program, New York, NY",
        "(primary academic affiliation)",
        "Third System\u2122 (research entity; data archive and methodology venue)",
        "Correspondence: pablou@pablou.com \u00b7 pablou.com",
        "ORCID: 0009-0003-8968-9990",
    ],
    "datasets": [
        (
            "<b>v0.10 deposit.</b> OSF project ec6wh, path /v10/. Inherits "
            "v0.9 raw responses without modification (filter only). Adds: "
            "filtered Mint subset (responses_mint.csv), classification "
            "outputs (classifications.csv), canonical scoring "
            "(canonical_scoring.{csv,json}), E3 sensitivity scoring, "
            "DEVIATIONS.md, adjudication log, build scripts (filter_v10.py, "
            "classify_v10.py, score_v10.py, build_charts_v10_naivephantom.py, "
            "build_report_v10.py), and inherited classifier configuration "
            "(registries/v07_caveat_classifier.json)."
        ),
        (
            "<b>Cross-cited deposits.</b> v0.9 raw responses, v0.7 "
            "caveat-classifier specification, and v0.6 baseline data "
            "remain available in their respective OSF deposits, unchanged. "
            "v0.10 makes no modifications to upstream data; the "
            "naive-phantom rate is recovered from v0.9\u2019s deposited "
            "data by applying the v0.7 classifier. AIAS Presence "
            "Measurement Protocol v1.1 governs the program."
        ),
        (
            "<b>Source archive.</b> The v0.10 build pipeline (chart "
            "generator, brand-format report builder, scoring scripts, "
            "classifier wrapper, content modules) is included in the "
            "deposit. The full pipeline is reproducible from raw v0.9 "
            "responses with a Python 3.14 environment, the brand JSON, "
            "and Akkurat Pro registered."
        ),
    ],
    "methodology_log": (
        "Pre-registration locked at git commit "
        "<font name='Helvetica'>8767f44</font> (tag <font name='Helvetica'>v0.10-prereg</font>) on "
        "2026-05-09, prior to any application of the v0.7 caveat-"
        "classifier to the v0.9 Mint response subset. Four deviations "
        "from pre-reg descriptive language documented post-lock in "
        "DEVIATIONS.md. AIAS Presence Measurement Protocol v1.1"
    ),
}
