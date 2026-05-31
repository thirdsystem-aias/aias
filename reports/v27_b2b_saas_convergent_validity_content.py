"""
v0.27 — What AI Share-of-Voice Doesn't Capture
Convergent validity of AIAS Presence against a third-party AI-visibility instrument

Brand-format report content module (Third System)
P1-P5 propositional register for managerial readers.
"""

VERSION = "v0.27"
SUBSTRATE = "B2B SaaS — Convergent Validity"
SUBTITLE = "Third-Party AI-Visibility Instruments"

# ---------------------------------------------------------------------------
# COVER
# ---------------------------------------------------------------------------

COVER = {
    "title": "What AI Share-of-Voice\nDoesn’t Capture",
    "subtitle": (
        "A pre-registered convergent-validity test of AIAS Presence "
        "against a third-party AI-visibility instrument"
    ),
    "version": "v0.27",
    "category": "Construct Validity — Convergent",
    "substrate": "B2B SaaS · 24 brands · HubSpot AEO Grader",
    "date": "May 2026",
    "byline_short": "Pablo Ulpiano González Castro",
    "tagline": "AIAS™ Measurement Program · Convergent Validity",
}

# ---------------------------------------------------------------------------
# STANDFIRST
# ---------------------------------------------------------------------------

STANDFIRST = (
    "AIAS Presence does not agree with the “Share of Voice” score that "
    "commercial AI-visibility tools put at the top of the dashboard. Across "
    "24 B2B SaaS brands, the correlation was weak and not significant — a "
    "pre-registered null. But the same measure converges strongly with the "
    "tool’s presence-quality and brand-recognition signals. The headline "
    "number is the weakest dial on the board; the signals beneath it move with "
    "AI presence."
)

# ---------------------------------------------------------------------------
# LEAD_DECK
# ---------------------------------------------------------------------------

LEAD_DECK = [
    {
        "metric": "rho = 0.29",
        "label": "Primary convergence",
        "detail": "recall-SOM × HubSpot Share-of-Voice (n = 24, n.s.; 95% CI [-0.17, 0.64])",
    },
    {
        "metric": "FALSIFIED",
        "label": "Pre-registered hypothesis",
        "detail": "Below the 0.60 confirm threshold and not significant",
    },
    {
        "metric": "0.80 / 0.75",
        "label": "Where it does converge",
        "detail": "Presence-quality and brand-recognition subscores (exploratory)",
    },
    {
        "metric": "6 / 6",
        "label": "Recognition at ceiling",
        "detail": "All 24 brands fully recognized — recognition enters only as a null control",
    },
]

# ---------------------------------------------------------------------------
# EXEC_SUMMARY
# ---------------------------------------------------------------------------

EXEC_SUMMARY = (
    "This study tested whether AIAS Presence agrees with the score that "
    "commercial “AI visibility” tools sell as a measure of how present a "
    "brand is inside ChatGPT, Perplexity, and Gemini. It does not. Across 24 "
    "B2B SaaS brands, the rank correlation between AIAS recall-SOM and the "
    "HubSpot AEO Grader’s Share-of-Voice was rho = 0.29 — not significant, "
    "with a confidence interval that straddles zero. Share-of-Voice was the "
    "metric named in advance as the convergent variable, and the test failed.\n\n"

    "The null is not the whole story. An exploratory scan of the instrument’s "
    "other dimensions found that AIAS recall-SOM converges <b>strongly</b> with "
    "two of them — presence quality (rho = 0.80) and brand recognition "
    "(rho = 0.75), both above the program’s 0.74 “strong” benchmark — while "
    "the headline Share-of-Voice it was tested against carried almost no rank "
    "information. These correlations are exploratory; the pre-registered metric "
    "failed, and re-nominating a better-correlating dimension after the fact is "
    "not available. But the pattern is informative.\n\n"

    "The failure is in the metric, not the construct. It is tempting to read the "
    "Share-of-Voice null as proof that AIAS Presence measures something "
    "category-competitive that brand-absolute tools cannot see. The data refute "
    "that: presence quality and brand recognition are also brand-absolute "
    "scores, and recall-SOM converges with them. The likely cause is range "
    "restriction — Share-of-Voice compresses almost every live brand into a "
    "narrow 4.7-to-8.3 band, leaving little to rank against. The dimensions that "
    "do spread — presence quality, brand recognition — track AIAS recall, "
    "consistent with its earlier convergence with Google Trends search interest "
    "(v0.25, rho = 0.74).\n\n"

    "For brand leaders, the consequence is sharper than a clean convergence "
    "would have delivered: the “Share of Voice” headline these tools sell as "
    "AI visibility is, on this evidence, the weakest available proxy for "
    "category-competitive AI presence. A brand managing to that number may be "
    "watching the least informative dial on the dashboard."
)

# ---------------------------------------------------------------------------
# WHAT_WE_MEASURED
# ---------------------------------------------------------------------------

WHAT_WE_MEASURED = (
    "We correlated AIAS Presence against a commercial AI-visibility instrument "
    "across 24 B2B SaaS brands, pre-registered before any instrument data was "
    "pulled.\n\n"

    "<b>AIAS-side (recall-SOM):</b> A brand’s share of category-leadership "
    "recall across a six-model panel — how often each brand is named when a "
    "model is asked, generically, for the leading platforms in its category "
    "(0–100). The measure is inherited verbatim from the v0.25 scorer, so it "
    "is identical to the one that converged with Google Trends at rho = 0.74. "
    "Brand recognition (C<sub>P</sub>) sat at the ceiling — every brand "
    "scored 6/6 — so it carries no variance and enters only as a null "
    "control.\n\n"

    "<b>Instrument (HubSpot AEO Grader, free tier):</b> For each brand, the "
    "Grader returns a perception profile across three engines on five "
    "dimensions — Share of Voice, Presence Quality, Brand Recognition, "
    "Market Competition, and Brand Sentiment — plus an overall composite. "
    "<b>Share of Voice</b> was pre-registered as the convergent variable.\n\n"

    "<b>Test:</b> Spearman rank correlation (10,000-sample bootstrap, Holm "
    "correction), with two pre-specified sensitivity analyses. The "
    "construct-matched instrument (Profound’s category-scoped share-of-model) "
    "was deferred on access; a discriminant instrument (Brandwatch) was not "
    "run. The convergent claim here rests on the HubSpot Grader alone."
)

# ---------------------------------------------------------------------------
# PATTERNS
# ---------------------------------------------------------------------------

PATTERNS = [
    {
        "id": "p1",
        "title": "The headline metric doesn’t converge",
        "body": (
            "AIAS recall-SOM and the HubSpot Grader’s Share-of-Voice do not "
            "co-rank: rho = 0.29 across 24 brands (not significant; 95% CI "
            "[-0.17, 0.64]). The correlation sits below the 0.60 confirm "
            "threshold and is statistically indistinguishable from zero. The "
            "pre-registered primary test is falsified.\n\n"

            "Much of the rank agreement that does exist is carried by the "
            "live-versus-defunct split — both measures rank the dead products "
            "(Wunderlist, HipChat, Yammer) at the bottom. Above that floor, the "
            "Grader’s live-brand scores barely move: Salesforce, Figma, "
            "Stripe, and Cloudflare all land within a point of each other on "
            "Share of Voice while their category-leadership recall spans the "
            "full range. A brand can post a strong Share-of-Voice score and be "
            "absent from the category-leadership answers its buyers actually "
            "receive — and the reverse.\n\n"

            "The clearest cases are the four “type-2” brands (Linear, "
            "Airtable, Miro, Cloudflare): specialist-salient, visible when the "
            "Grader scores them in isolation, but absent from generic "
            "category-leadership recall. A pre-specified sensitivity that drops "
            "them lifts the correlation only to rho = 0.36 — still below "
            "threshold. The non-convergence is broader than those four cases."
        ),
    },
    {
        "id": "p2",
        "title": "Recognition is already maxed out",
        "body": (
            "Every one of the 24 brands scored full recognition (C<sub>P</sub> "
            "= 6/6) across the model panel. With zero variance, recognition "
            "carries no convergent signal by construction — it cannot rank "
            "brands because it does not separate them.\n\n"

            "This is why AIAS Presence is operationalized as recall-SOM rather "
            "than recognition on this substrate: in a category where models "
            "recognize every established brand, the question that discriminates "
            "is not “does the model know this brand?” but “does the model "
            "surface it when asked for the category leaders?” The ceiling is a "
            "property of B2B SaaS, recorded here so recognition is not mistaken "
            "for a live convergent dimension."
        ),
    },
    {
        "id": "p3",
        "title": "Where AIAS Presence does converge",
        "body": (
            "The pre-registered metric failed, but the instrument has five "
            "other dimensions, and AIAS recall-SOM tracks two of them closely. "
            "Against <b>Presence Quality</b> the correlation is rho = 0.80; "
            "against <b>Brand Recognition</b> it is rho = 0.75 — both above "
            "the program’s 0.74 “strong” benchmark. The overall composite "
            "reaches rho = 0.44. Share of Voice, the dimension it was tested "
            "against, is the weakest match at rho = 0.29.\n\n"

            "These correlations are <b>exploratory</b>. Share of Voice was the "
            "pre-registered convergent variable; it failed, and re-nominating "
            "presence quality or brand recognition as the “real” convergent "
            "measure after seeing which one worked is exactly the move "
            "pre-registration exists to prevent. They are reported to generate "
            "the next hypothesis, not to rescue this one — and they are "
            "pre-specified for confirmatory test on a fresh substrate.\n\n"

            "What they show is that AIAS recall-SOM is not failing to converge "
            "with this instrument in general. It converges with most of the "
            "instrument’s facets and fails on the one the vendor puts in the "
            "headline."
        ),
    },
    {
        "id": "p4",
        "title": "It’s the metric, not the construct",
        "body": (
            "The obvious reading — that AIAS Presence measures "
            "category-competitive presence and therefore diverges from "
            "brand-absolute AI visibility — does not survive the data. "
            "Presence quality and brand recognition are computed on a single "
            "named brand in isolation, exactly like Share of Voice, and "
            "recall-SOM converges with them. The category-versus-brand-absolute "
            "story does not explain the pattern.\n\n"

            "Range restriction does. Among live brands, Share of Voice "
            "compresses into a 4.7-to-8.3 band with most brands tied near 7.3, "
            "so nearly all its rank information is the live-versus-defunct "
            "split — there is little left to track standing among salient "
            "brands. Presence quality and brand recognition spread across the "
            "live brands and move with recall. One detail sharpens this: the "
            "Grader’s own brand-recognition subscore carries real variance and "
            "tracks recall-SOM, even though AIAS’s recognition measure is at "
            "the ceiling — the Grader’s graded version behaves like a "
            "prominence measure, which is what recall-SOM is.\n\n"

            "Read against the program’s prior results, the pattern is "
            "coherent. The same AIAS measure converged with Google Trends "
            "search-interest prominence (rho = 0.74) and stood independent of "
            "Amazon sales rank. The dimensions it converges with here — "
            "prominence and knowledge facets — are of a piece with the Trends "
            "result; the compressed competitive-share score it fails on is the "
            "exception the construct predicts. The practitioner takeaway is "
            "direct: the “Share of Voice” number sold as AI visibility carries "
            "real signal, but read as AI availability it is the wrong place to "
            "read it."
        ),
    },
]

# ---------------------------------------------------------------------------
# LIMITATIONS
# ---------------------------------------------------------------------------

LIMITATIONS = (
    "The convergent claim rests on a single instrument, pre-registered as a "
    "<i>loose</i> construct match. The strongest available test — convergence "
    "against a category-scoped, construct-matched instrument (share-of-model) "
    "— was never run: Profound is enterprise-only and access was declined as "
    "disproportionate to one phase. A single-instrument null on one dimension "
    "cannot, on its own, separate a genuine convergence failure from a metric "
    "artifact — which is what the exploratory scan suggests is in play.\n\n"

    "The Grader is brand-absolute and cannot be category-scoped on the free "
    "tier. One brand, Stride, carries a name-collision confound: “Stride” is "
    "ambiguous (Stride gum, Stride Inc., Stride Bank), so its score may reflect "
    "non-target entities rather than the defunct Atlassian product. A "
    "pre-specified sensitivity excludes it; the estimate is <i>sensitive</i> to "
    "that exclusion, which is reported rather than smoothed.\n\n"

    "n = 24 is modest, though pre-registered and adequate for the planned "
    "correlation. Recognition is at the ceiling on this substrate, so "
    "recognition convergence cannot be tested here. The AIAS-side measure is "
    "inherited from the v0.24 corpus, collected the same month as the "
    "instrument pull; residual brand-level drift over the gap is mitigated, not "
    "removed, by rank-based correlation."
)

# ---------------------------------------------------------------------------
# WHATS_NEXT
# ---------------------------------------------------------------------------

WHATS_NEXT = (
    "The deferred test is the decisive next step: convergence of AIAS recall-SOM "
    "against a category-scoped share-of-model instrument (Profound, or a "
    "self-serve tool with equivalent scoping). If recall-SOM converges with a "
    "construct-matched instrument, the present null becomes evidence of "
    "construct specificity rather than a threat to it.\n\n"

    "Separately, the strong exploratory convergence surfaced here — presence "
    "quality and brand recognition — is pre-specified for a confirmatory "
    "pre-registration on a fresh substrate, with those dimensions fixed in "
    "advance, to test whether the pattern replicates. Completing the "
    "discriminant arm (a web-mention instrument) would round out the "
    "Campbell–Fiske matrix paired with the v0.26 sales-rank result."
)

# ---------------------------------------------------------------------------
# HYPOTHESIS_SCORING
# ---------------------------------------------------------------------------

HYPOTHESIS_SCORING = [
    {
        "id": "P1",
        "label": "Primary convergence — recall-SOM × Share-of-Voice",
        "prediction": (
            "AIAS recall-SOM correlates with the HubSpot Grader’s Share-of-Voice "
            "at rho ≥ 0.60."
        ),
        "verdict": "FALSIFIED",
        "detail": "rho = 0.29, n = 24, n.s. (95% CI [-0.17, 0.64]). Below threshold.",
    },
    {
        "id": "P2",
        "label": "Recognition null control",
        "prediction": (
            "Recognition (C<sub>P</sub>), at ceiling, carries no convergent "
            "signal."
        ),
        "verdict": "CONFIRMED",
        "detail": "C<sub>P</sub> = 6/6 for all 24 brands (sd = 0). No variance, as predicted.",
    },
    {
        "id": "P3",
        "label": "Component scan — where AIAS Presence converges",
        "prediction": (
            "Exploratory: cross-correlate recall-SOM with each Grader dimension."
        ),
        "verdict": "EXPLORATORY",
        "detail": (
            "Presence Quality rho = 0.80, Brand Recognition rho = 0.75 "
            "(both > 0.74); Composite 0.44; Share of Voice 0.29 (weakest)."
        ),
    },
    {
        "id": "P4",
        "label": "Construct-matched instrument (share-of-model)",
        "prediction": (
            "recall-SOM converges with a category-scoped share-of-model "
            "instrument (Profound)."
        ),
        "verdict": "NOT RUN",
        "detail": "Profound access declined as disproportionate (enterprise-only). Deferred.",
    },
]

# ---------------------------------------------------------------------------
# HYPOTHESIS_DETAILS
# ---------------------------------------------------------------------------

HYPOTHESIS_DETAILS = (
    "<b>P1 — Primary convergence: FALSIFIED</b>\n"
    "recall-SOM × HubSpot Share-of-Voice: rho = 0.294, n = 24, "
    "p_adj = 0.164 (Holm), 95% CI [-0.171, 0.638]. Below the 0.60 confirm "
    "threshold and not significant. Type-2 sensitivity (drop Linear, Airtable, "
    "Miro, Cloudflare): rho = 0.359 (n = 20). Stride-confound sensitivity (drop "
    "Stride): rho = 0.223 (n = 23) — the estimate is sensitive to the "
    "exclusion.\n\n"

    "<b>P2 — Recognition null control: CONFIRMED</b>\n"
    "Brand recognition C<sub>P</sub> = 6/6 for all 24 brands (sd = 0). Zero "
    "variance; recognition enters only as a control, not a convergent "
    "dimension.\n\n"

    "<b>P3 — Component scan: EXPLORATORY</b>\n"
    "recall-SOM × Grader dimensions: Presence Quality rho = 0.798 "
    "(p < 0.001), Brand Recognition rho = 0.748 (p < 0.001), Composite "
    "rho = 0.443 (p = 0.030), Market Competition rho = 0.297, Share of Voice "
    "rho = 0.294 (n.s.), Sentiment rho = 0.133. Exploratory; does not bear on "
    "the falsified primary.\n\n"

    "<b>P4 — Construct-matched instrument: NOT RUN</b>\n"
    "Profound (category-scoped share-of-model) deferred on access at "
    "pre-registration amendment r4; the discriminant instrument (Brandwatch) "
    "was not run."
)

# ---------------------------------------------------------------------------
# CLOSING
# ---------------------------------------------------------------------------

CLOSING = (
    "AIAS Presence does not converge with the AI “Share of Voice” score that "
    "commercial visibility tools sell. That is the pre-registered result, and "
    "it stands. But it is not evidence that AIAS Presence measures something "
    "those tools cannot — it converges strongly with their presence-quality "
    "and brand-recognition signals, and fails only on the compressed, "
    "range-restricted headline metric.\n\n"

    "For brand leaders, the strategic implication is direct. The “AI "
    "visibility” scores now entering the market carry real signal, but the "
    "Share-of-Voice headline is the wrong place to read AI availability. The "
    "recognition and presence-quality signals beneath it track category "
    "presence far better. Managing to the headline number may mean managing "
    "the least informative dial on the dashboard — and the decisive test, "
    "against a construct-matched instrument, remains open and pre-registered."
)
