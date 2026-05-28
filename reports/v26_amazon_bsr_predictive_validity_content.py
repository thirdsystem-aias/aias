# NOTE: cloned from v25_b2b_saas_construct_validity_content.py on phase scaffold.
# All COVER, STANDFIRST, LEAD_DECK, EXEC_SUMMARY, PATTERNS,
# LIMITATIONS, WHATS_NEXT, HYPOTHESIS_DETAILS, CLOSING text
# must be re-written for the v0.26 Amazon BSR Predictive Validity
# substrate. Do not ship this file as-is.

# NOTE: cloned from v24_b2b_saas_content.py on phase scaffold.
# All COVER, STANDFIRST, LEAD_DECK, EXEC_SUMMARY, PATTERNS,
# LIMITATIONS, WHATS_NEXT, HYPOTHESIS_DETAILS, CLOSING text
# must be re-written for the v0.26 B2B SaaS Construct Validity
# substrate. Do not ship this file as-is.

"""
AIAS v0.26 — B2B SaaS
Brand-Format Report Content Module
Third System™ · AIAS Measurement Program

Register: managerial / editorial (P1–P5 propositional framing)
Do NOT use H_* hypothesis framing in this file.
"""

# ── COVER ───────────────────────────────────────────────────────────────

COVER = {
    "title": "Your Marketing Language\nIs Now the Machine\u2019s Language",
    "subtitle": (
        "AI Presence in B2B SaaS: the eighth substrate in the "
        "AIAS\u2122 Measurement Program measures how enterprise software "
        "brands surface in large-language-model recommendations \u2014 "
        "and finds that vendor-coined positioning has crossed into "
        "the discourse AI uses to describe entire categories."
    ),
    "version": "v0.26",
    "substrate": "B2B SaaS",
    "date": "June 2026",
}

# ── STANDFIRST ──────────────────────────────────────────────────────────

STANDFIRST = (
    "Every major B2B SaaS brand in our 24-brand panel is perfectly "
    "recognized by every model tested. But recognition is table stakes. "
    "The real question is which brands get recommended \u2014 and in whose "
    "language. More than half of all AI recall outputs now contain "
    "vendor-coined marketing terms like \u201Cinbound marketing,\u201D "
    "\u201Cworkflow automation,\u201D and \u201Cno-code.\u201D The positioning "
    "language that brands invented to differentiate themselves has become "
    "the vocabulary AI systems use to describe their categories."
)

# ── LEAD_DECK ───────────────────────────────────────────────────────────

LEAD_DECK = [
    {
        "number": "24/24",
        "label": "brands recognized at 6/6",
        "detail": (
            "Perfect uniform saturation across the entire panel. Every "
            "model knows every brand \u2014 enterprise incumbents, challengers, "
            "infrastructure platforms, even defunct products."
        ),
    },
    {
        "number": "55.6%",
        "label": "Marketing-Language Coverage",
        "detail": (
            "More than half of all recall outputs contain at least one "
            "vendor-coined term. This is the first quantified measure of "
            "marketing-language absorption by AI systems in the program."
        ),
    },
    {
        "number": "27.7pt",
        "label": "Identity Load cell separation",
        "detail": (
            "The gap between challenger brands\u2019 cultural-recall lead "
            "and enterprise incumbents\u2019 category-recall lead \u2014 the "
            "strongest Identity Load separation measured in the program."
        ),
    },
    {
        "number": "0/5",
        "label": "phantom brands recalled",
        "detail": (
            "Quip, Yammer, Wunderlist, HipChat, and Stride are all "
            "recognized \u2014 models know what they were \u2014 but none appear "
            "in a single recommendation. Knowledge without influence."
        ),
    },
]

# ── EXEC_SUMMARY ────────────────────────────────────────────────────────

EXEC_SUMMARY = (
    "This study measures AI Presence for 24 B2B SaaS brands across six "
    "large language models. It is the eighth substrate family in the "
    "AIAS\u2122 Measurement Program and the first to quantify Marketing-Language "
    "Coverage (MLC) \u2014 the rate at which vendor-coined positioning terms "
    "appear in AI-generated recommendations.\n\n"

    "Five findings define the B2B SaaS substrate.\n\n"

    "First, recognition is completely undifferentiated. Every brand in the "
    "panel \u2014 from Salesforce to Linear to Cloudflare \u2014 scores 6/6 on "
    "recognition. AI models trained on the internet\u2019s vast corpus of "
    "technical content know every B2B SaaS brand. This makes recognition "
    "a non-competitive dimension; all competitive differentiation occurs "
    "in the recall layer.\n\n"

    "Second, recall is sharply concentrated. Salesforce and Slack together "
    "account for a disproportionate share of all recommendation mentions. "
    "Twilio, Cloudflare, and MongoDB are nearly invisible in recommendation "
    "space despite universal recognition. This is a clean demonstration "
    "of the AI-native analogue of Double Jeopardy: brands that are known "
    "but not mentioned get neither the awareness benefit nor the "
    "recommendation benefit.\n\n"

    "Third, marketing language has crossed into machine discourse. "
    "55.6% of all recall outputs contain at least one vendor-coined term. "
    "\u201CInbound marketing\u201D (HubSpot) appears 21 times, \u201Cworkflow "
    "automation\u201D (ServiceNow) 15, and \u201Cno-code\u201D (Airtable) 10. "
    "Some of these terms have fully detached from brand attribution "
    "\u2014 models use \u201Cinbound marketing\u201D as a category descriptor, "
    "not a HubSpot brand marker \u2014 while others (\u201CTrailblazer,\u201D "
    "\u201CEinstein\u201D) retain explicit brand linkage. The distinction "
    "matters: category-absorbed language lifts the category; "
    "brand-retained language lifts the brand.\n\n"

    "Fourth, Identity Load determines where brands appear. Enterprise "
    "incumbents dominate category-recall probes (\u201CWhat SaaS tools do "
    "enterprises use?\u201D) but are weak on cultural probes (\u201CWhat SaaS "
    "brands have cult-like followings?\u201D). Challengers show the inverse "
    "pattern. The 27.7-point cell separation is the strongest Identity "
    "Load signal in the program. Slack is the crossover anomaly \u2014 high "
    "on both channels \u2014 reflecting its dual identity as enterprise "
    "infrastructure and beloved brand.\n\n"

    "Fifth, defunct B2B SaaS brands vanish from recommendations even when "
    "models know exactly what they were. All five phantom candidates "
    "(Quip, Yammer, Wunderlist, HipChat, Stride) are perfectly recognized "
    "\u2014 models describe their features, note their discontinuation, "
    "identify their acquirers \u2014 yet none appears in a single recommendation "
    "output. The recognition\u2013recommendation gap is now confirmed across "
    "three substrate families."
)

# ── WHAT_WE_MEASURED ────────────────────────────────────────────────────

WHAT_WE_MEASURED = (
    "We measured AI Presence for 24 B2B SaaS brands across six large "
    "language models: Claude Opus 4.7, Claude Sonnet 4.6, GPT-4o, "
    "GPT-4o-mini, Gemini 2.5 Flash, and Gemini 2.5 Flash Lite.\n\n"

    "Phase A tested recognition: does the model know this brand? "
    "144 probes (24 brands \u00d7 6 models). Phase B tested recall: "
    "when asked to recommend B2B SaaS products, which brands surface? "
    "72 queries across two channels \u2014 category recall (\u201CWhat are "
    "the leading B2B SaaS platforms?\u201D) and cultural recall (\u201CWhat "
    "SaaS brands have cult-like followings?\u201D).\n\n"

    "New for this phase: we coded all Phase B outputs for "
    "Marketing-Language Coverage (MLC) \u2014 the proportion of responses "
    "containing vendor-coined positioning terms from a pre-registered "
    "dictionary of 19 tokens across 8 brands. This is the first "
    "quantified operationalization of Discourse-Language carryforward "
    "in the program.\n\n"

    "The panel spans four cells: enterprise incumbents (Salesforce, "
    "HubSpot, ServiceNow, Workday, SAP, Oracle, Zendesk), high-identity "
    "challengers (Notion, Figma, Linear, Airtable, Slack, Miro), "
    "infrastructure and developer platforms (Datadog, Snowflake, Stripe, "
    "Twilio, Cloudflare, MongoDB), and phantom candidates \u2014 defunct or "
    "absorbed brands (Quip, Yammer, Wunderlist, HipChat, Stride).\n\n"

    "All measurement follows the AIAS\u2122 Protocol v1.6."
)

# ── PATTERNS ────────────────────────────────────────────────────────────

PATTERNS = [
    {
        "id": "P1",
        "title": "Recognition is table stakes",
        "body": (
            "Every brand in the 24-brand panel achieves perfect recognition "
            "(C\u209a = 6/6) across all six models. This is uniform saturation "
            "\u2014 the strongest form of the pattern observed in cosmetics "
            "(v0.21) and automotive (v0.22). On B2B SaaS, the internet\u2019s "
            "density of technical documentation, product comparisons, and "
            "developer content means every brand is known. Recognition is "
            "not a differentiator; it is a baseline condition."
        ),
    },
    {
        "id": "P2",
        "title": "Recall concentration creates a two-tier recommendation market",
        "body": (
            "Salesforce (61/72 mentions) and Slack (63/72) sit in the "
            "first tier. HubSpot (54/72) and Workday (41/72) occupy the "
            "second. Below them, recall drops steeply: Twilio (4/72), "
            "Cloudflare (3/72), MongoDB (5/72). The gap between universal "
            "recognition and selective recall is the competitive surface "
            "in AI-mediated discovery. Being known is free; being "
            "recommended is scarce."
        ),
    },
    {
        "id": "P3",
        "title": "Marketing language has been absorbed into AI discourse",
        "body": (
            "55.6% of all recall outputs contain at least one vendor-coined "
            "marketing term. The absorption is not uniform. \u201CInbound "
            "marketing\u201D (21 appearances) has fully detached from HubSpot "
            "\u2014 models use it as a category descriptor without brand "
            "attribution. \u201CNo-code\u201D (10 appearances) shows the same "
            "pattern with Airtable. But \u201CTrailblazer\u201D (9 appearances) "
            "retains its Salesforce linkage \u2014 models say \u201CSalesforce "
            "Trailblazers.\u201D This creates two classes of marketing-language "
            "carryforward: terms that lift the category (category-absorbed) "
            "and terms that lift the brand (brand-retained). The strategic "
            "implication is asymmetric: HubSpot created a vocabulary that "
            "now benefits all inbound-marketing platforms; Salesforce created "
            "one that still accrues to Salesforce."
        ),
    },
    {
        "id": "P4",
        "title": "Identity Load determines the channel, not the volume",
        "body": (
            "Enterprise incumbents (Cell A) dominate category recall: "
            "mean R\u2091\u2090\u209c = 27.0/36. But they are weak on cultural "
            "recall: mean R\u2091\u1d64\u2097\u209c = 11.6/36. Challengers (Cell B) "
            "show the exact inverse: R\u2091\u2090\u209c = 6.0, R\u2091\u1d64\u2097\u209c = 18.3. "
            "The 27.7-point separation between cell cult-leads is the "
            "strongest Identity Load signal in the program. What this "
            "means for brand strategy: enterprise incumbents are recalled "
            "when users ask \u201Cwhat tools do companies use?\u201D but not "
            "when they ask \u201Cwhat tools do teams love?\u201D Challengers "
            "get the love question but miss the enterprise question. "
            "Slack is the sole brand that bridges both channels (R\u2091\u2090\u209c = 33, "
            "R\u2091\u1d64\u2097\u209c = 30) \u2014 a dual-identity advantage that no other "
            "brand in the panel replicates."
        ),
    },
    {
        "id": "P5",
        "title": "Defunct brands persist in knowledge but vanish from recommendations",
        "body": (
            "All five phantom candidates \u2014 Quip, Yammer, Wunderlist, "
            "HipChat, Stride \u2014 are recognized with detailed accuracy. "
            "Models describe their features, identify their acquirers, "
            "note their discontinuation dates. Yet none appears in a single "
            "recommendation output. The recognition\u2013recommendation gap "
            "replicates across three substrate families (automotive, B2B "
            "SaaS, and the broader AIAS program). Recommendation slots "
            "are reserved for active brands; historical knowledge does not "
            "convert to recommendation-slot persistence."
        ),
    },
]

# ── LIMITATIONS ─────────────────────────────────────────────────────────

LIMITATIONS = (
    "Four limitations qualify these findings.\n\n"

    "First, the Marketing-Language Coverage rate (55.6%) establishes a "
    "benchmark but lacks a cross-substrate baseline. Prior phases did not "
    "code recall outputs for MLTs. Retroactive baseline coding across "
    "v0.16\u2013v0.22 would be required to confirm whether the B2B SaaS "
    "rate is genuinely elevated or merely the first measurement of a "
    "substrate-invariant pattern.\n\n"

    "Second, the MLT dictionary was hand-curated at pre-registration. "
    "Terms that brands coined but that have become so generic they are "
    "no longer recognizable as marketing language (e.g., \u201CCRM,\u201D "
    "\u201Ccloud computing\u201D) were excluded. The dictionary captures "
    "mid-diffusion terms \u2014 still traceable to a brand but potentially "
    "on the path to full genericization. A broader or narrower dictionary "
    "would shift the MLC rate.\n\n"

    "Third, Stride (D5) presents a name-collision confound. All six "
    "models associated \u201CStride\u201D with the chewing-gum brand "
    "(Mondelez), not with Atlassian\u2019s defunct messaging product. "
    "Brand-name uniqueness is a precondition for clean recognition "
    "measurement. Future phantom-candidate selection should screen for "
    "name collisions.\n\n"

    "Fourth, the cross-vertical design (CRM + collaboration + "
    "infrastructure + developer tools under a single \u201CB2B SaaS\u201D "
    "umbrella) trades category coherence for breadth. Recall probes "
    "may favor brands in the CRM/productivity sub-vertical over "
    "infrastructure brands (Datadog, Cloudflare, MongoDB) that "
    "enterprises use but do not think of as \u201CSaaS platforms.\u201D A "
    "narrower single-vertical study would produce tighter recall "
    "distributions at the cost of generalizability."
)

# ── WHATS_NEXT ──────────────────────────────────────────────────────────

WHATS_NEXT = (
    "Three research directions follow from v0.26.\n\n"

    "First, retroactive MLC baseline coding across prior substrates "
    "(v0.16\u2013v0.22) to establish whether marketing-language absorption "
    "is substrate-specific or universal. If \u201Cinbound marketing\u201D and "
    "\u201Cno-code\u201D are B2B SaaS phenomena while kitchen knives and "
    "fragrances show near-zero MLC, the Discourse-Language hypothesis "
    "gains a comparative anchor.\n\n"

    "Second, the category-absorbed vs. brand-retained distinction in "
    "marketing-language carryforward warrants formal coding. A taxonomy "
    "of MLT types (fully detached, partially attributed, brand-retained) "
    "would sharpen the strategic implications for brand managers investing "
    "in category-creation language.\n\n"

    "Third, Slack\u2019s dual-channel dominance invites a dedicated "
    "subsidiary-identity study. Do acquired brands that maintain distinct "
    "identities (Slack within Salesforce, Instagram within Meta, YouTube "
    "within Alphabet) show systematically different recall patterns than "
    "absorbed brands (Quip within Salesforce, Yammer within Microsoft)? "
    "The v0.26 data provides the first data point; a designed comparison "
    "would test the mechanism."
)

# ── HYPOTHESIS_SCORING ──────────────────────────────────────────────────

HYPOTHESIS_SCORING = [
    {
        "id": "P1",
        "label": "Uniform Recognition Saturation",
        "verdict": "CONFIRMED",
        "detail": (
            "All 24 brands at C\u209a = 6/6. Strongest uniform-saturation "
            "finding in the program. Recognition is non-competitive on "
            "this substrate."
        ),
    },
    {
        "id": "P2",
        "label": "Regime Classification",
        "verdict": "REGIME 1 (UNIFORM SATURATION)",
        "detail": (
            "C1 passes (19/19 responding brands). C2 fails: distinct "
            "C\u209a = 1, modal share = 100%. Consistent with v0.20, v0.21, "
            "v0.22 pattern."
        ),
    },
    {
        "id": "P3",
        "label": "Marketing-Language Coverage",
        "verdict": "PARTIAL",
        "detail": (
            "MLC = 55.6% (40/72 outputs). Strong absolute signal. "
            "R\u2091\u1d64\u2097\u209c channel (63.9%) higher than R\u2091\u2090\u209c (47.2%). "
            "Comparative leg undetermined: no cross-substrate baseline yet."
        ),
    },
    {
        "id": "P4",
        "label": "Identity Load Moderator",
        "verdict": "CONFIRMED",
        "detail": (
            "Cell B cult-lead (+12.3) exceeds Cell A (\u221215.4). "
            "27.7-point separation. Strongest IL signal in the program."
        ),
    },
    {
        "id": "P5",
        "label": "Recognition \u00d7 Recall Dissociation",
        "verdict": "CONFIRMED (qualified)",
        "detail": (
            "16 Iwachu cases, all HIGH_REC_LOW_RECALL. Methodologically "
            "qualified: uniform C\u209a = 6/6 inflates count. The real "
            "finding is extreme recall variance (3\u201363/72) under "
            "uniform recognition."
        ),
    },
    {
        "id": "P6",
        "label": "Phantom Brand Persistence",
        "verdict": "FALSIFIED",
        "detail": (
            "All 5 Cell D brands: R\u209a\u2095\u2090\u2099\u209c\u2092\u2098 = 0. "
            "Replicates v0.22 automotive null. Recognition without "
            "recommendation confirmed across three substrate families."
        ),
    },
]

# ── HYPOTHESIS_DETAILS ──────────────────────────────────────────────────

HYPOTHESIS_DETAILS = (
    "P1 (Uniform Recognition Saturation): All 24 brands achieve perfect "
    "recognition across all six models. This is the third consecutive "
    "substrate (after cosmetics v0.21 and automotive v0.22) to show "
    "complete uniform saturation. The B2B SaaS substrate is particularly "
    "unsurprising \u2014 every brand in the panel appears extensively in "
    "technical documentation, product comparisons, and developer content "
    "that forms a significant portion of LLM training corpora.\n\n"

    "P2 (Regime Classification): With all main-cell brands at C\u209a = 6/6, "
    "the substrate classifies as Regime 1 (uniform saturation). C2 fails "
    "because there is exactly one distinct C\u209a value (6) with 100% modal "
    "share. This is the expected result for a substrate with dense "
    "training-data representation and extends the program\u2019s cumulative "
    "finding that Regime 4 has not been observed on any substrate with "
    "strong digital presence.\n\n"

    "P3 (Marketing-Language Coverage): The headline finding of this phase. "
    "55.6% of all Phase B outputs contain at least one pre-registered "
    "marketing-language token. The token-level analysis reveals a "
    "meaningful structural distinction. \u201CInbound marketing\u201D "
    "(HubSpot-originated, 21 hits) has become category-level vocabulary "
    "\u2014 models use the term without attributing it to HubSpot. In "
    "contrast, \u201CTrailblazer\u201D (Salesforce, 9 hits) and \u201CEinstein\u201D "
    "(Salesforce AI branding, 5 hits) retain explicit brand linkage. "
    "Gemini models show the highest MLC (83.3%); Claude Sonnet the "
    "lowest (25.0%). The cross-model variation suggests that "
    "marketing-language permeability is not uniform across architectures "
    "or training pipelines.\n\n"

    "P4 (Identity Load Moderator): The cell-level recall pattern is the "
    "cleanest in the program. Cell A brands (enterprise incumbents) show "
    "a mean R\u2091\u2090\u209c of 27.0/36 but mean R\u2091\u1d64\u2097\u209c of only 11.6/36 "
    "\u2014 they are functional-category brands. Cell B brands (challengers) "
    "invert: R\u2091\u2090\u209c = 6.0, R\u2091\u1d64\u2097\u209c = 18.3 \u2014 they are "
    "identity-cultural brands. The outlier is Slack (B5): R\u2091\u2090\u209c = 33, "
    "R\u2091\u1d64\u2097\u209c = 30, demonstrating dual-channel dominance that no other "
    "brand in the panel achieves. This may reflect Slack\u2019s unique "
    "position as both enterprise infrastructure (post-Salesforce acquisition) "
    "and cultural icon (pre-acquisition brand identity).\n\n"

    "P5 (Recognition \u00d7 Recall Dissociation): Sixteen Iwachu cases are "
    "detected, all in the HIGH_REC_LOW_RECALL direction. This is "
    "methodologically expected: when every brand achieves C\u209a = 6/6, "
    "any brand with below-maximum recall will show a recognition\u2013recall "
    "gap. The analytically meaningful finding is not the count of "
    "dissociation cases but the extreme range of recall under uniform "
    "recognition \u2014 from Cloudflare (3/72) to Slack (63/72), a 21:1 "
    "ratio. Dissociation is structural on this substrate, not "
    "brand-specific.\n\n"

    "P6 (Phantom Brand Persistence): The prediction that B2B SaaS "
    "phantom brands would show higher persistence than automotive "
    "phantoms (due to long-tail tech content) was falsified. All five "
    "Cell D brands show zero recall despite perfect recognition. This "
    "is the strongest evidence yet that Phantom Brand Persistence \u2014 "
    "as a recommendation-space phenomenon \u2014 does not generalize: "
    "models retain knowledge of defunct brands but do not surface them "
    "in recommendation contexts. The Stride name-collision (models "
    "recognized the gum brand, not the Atlassian product) adds a "
    "methodological note: phantom-candidate selection should verify "
    "brand-name uniqueness."
)

# ── CLOSING ─────────────────────────────────────────────────────────────

CLOSING = (
    "B2B SaaS is the eighth substrate in the AIAS\u2122 Measurement "
    "Program and the first to quantify Marketing-Language Coverage. "
    "The finding that 55.6% of AI recall outputs contain vendor-coined "
    "positioning terms reframes a familiar brand-strategy question: "
    "when you invest in category-creation language, you may be building "
    "vocabulary that AI systems will use to describe your competitors. "
    "Or you may be building vocabulary that keeps your name attached. "
    "The difference between \u201Cinbound marketing\u201D (category gift) and "
    "\u201CTrailblazer\u201D (brand asset) is the difference between creating "
    "a market and owning one."
)
