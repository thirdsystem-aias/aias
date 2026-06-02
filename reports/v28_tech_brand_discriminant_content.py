"""
v28_tech_brand_discriminant_content.py

AIAS™ v0.28 / CV.04 --- managerial brand-format report content.
Discriminant validity of AIAS Presence against human brand norms (Technology, n = 24).

Authored from the LOCKED verdicts (osf/v28/v28_verdicts.json, tag v0.28-results-locked);
results-aware. Replaces the v0.26 Amazon-BSR carryover wholesale.

Consumed by reports/build_report_v28.py. Attribute contract:
  VERSION, SUBSTRATE, SUBTITLE        -> str
  COVER                               -> dict{title, subtitle, version, category, substrate, date}
  STANDFIRST                          -> str (one paragraph)
  LEAD_DECK                           -> list[{metric, label, detail}]
  EXEC_SUMMARY                        -> str (\\n\\n -> paragraphs)
  WHAT_WE_MEASURED                    -> str (\\n\\n -> paragraphs)
  PATTERNS                            -> list[{id, title, body}]  (4; index -> chart via _PATTERN_CHART_MAP)
  LIMITATIONS                         -> str (\\n\\n -> paragraphs)
  WHATS_NEXT                          -> str (\\n\\n -> paragraphs)
  HYPOTHESIS_SCORING                  -> list[{id, label, prediction, verdict, detail}]
  HYPOTHESIS_DETAILS                  -> str (\\n\\n -> items)
  CLOSING                             -> dict{byline_long, datasets, methodology_log}
"""

VERSION = "Version 1 · CV.04 (v0.28)"

SUBSTRATE = "Technology — 24 brands"

SUBTITLE = (
    "A pre-registered discriminant test of AIAS™ Presence against human brand "
    "familiarity and recognition sensitivity."
)

COVER = {
    "title": "AI Availability Is Not Recognition Memory",
    "subtitle": (
        "And at n = 24 the familiarity question is still open. A pre-registered "
        "discriminant test of AIAS™ Presence against human brand norms, on 24 "
        "technology brands."
    ),
    "version": "Version 1 · CV.04 (v0.28)",
    "category": "Designed-for-Test: Technology",
    "substrate": "24 technology brands",
    "date": "June 2026",
}

STANDFIRST = (
    "AI Availability — whether language models surface, recognize, and recall a "
    "brand — only earns its place as a measurable layer of brand growth if it is "
    "distinct from the human memory measures it resembles. This study put AIAS™ "
    "Presence against two of them, on the hardest substrate for the test to pass: "
    "technology, where AI fame and human fame should align most tightly. Presence is "
    "distinct from recognition memory. Against familiarity, the evidence at this "
    "sample size is genuinely inconclusive — and the pre-registered rule says so "
    "rather than pretend otherwise."
)

LEAD_DECK = [
    {"metric": "rho = 0.38", "label": "Presence vs recognition (d')",
     "detail": "Distinct — confirmed, interval excludes redundancy"},
    {"metric": "rho = 0.59", "label": "Presence vs familiarity",
     "detail": "Unresolved at n = 24 — interval spans every band"},
    {"metric": "11 / 24", "label": "brands dissociate",
     "detail": "AI presence diverges from human familiarity, both directions"},
    {"metric": "n = 24", "label": "technology brands",
     "detail": "Pre-registered, blind-acquired, scored once"},
]

EXEC_SUMMARY = """For a new brand metric to be worth the name, it has to measure something the cheaper, older measures do not. This study tested whether AIAS™ Presence — the degree to which a six-model panel recognizes and recalls a brand — is just a re-reading of how well people already know that brand. The validator was the published BRAND database: human familiarity ratings and a signal-detection measure of recognition. The category was chosen to make the test hard. Technology is where model training is densest and where AI fame and human fame should track most closely, so if Presence were going to collapse into a familiarity proxy anywhere, it should collapse here.

Against recognition sensitivity — how reliably people tell a real brand from a decoy — Presence is distinct (rho = 0.38), and its confidence interval rules out the level of correlation that would mark it as redundant. Whether a model classes a brand as "technology" is not a restatement of human recognition. The interval is wide, so this is a confirmed result, not a tight one, and it is reported as such.

Against familiarity — a direct fame rating — the evidence is inconclusive. The central estimate (rho = 0.59) leans toward partial distinctness, exactly as predicted, but across 24 brands the interval is wide enough to span everything from clearly distinct to fully reducible. The pre-registered decision rule returned UNDETERMINED rather than read a finding into a number it cannot support. The fame question is open, not answered — and a larger panel is what would close it.

Where Presence and familiarity diverge, they diverge in a pattern. Eleven of 24 brands pull apart by more than a standard deviation, in both directions: the model layer amplifies core-technology identity — Apple, Microsoft, and the enterprise infrastructure names — and suppresses brands that are culturally famous without being category-canonical technology, such as Netflix, Instagram, Uber, and Airbnb. AI presence and human fame are not the same map of a category. The difference is legible, not noise, and it is the part of this result with the most immediate use for anyone managing a brand's standing inside the models."""

WHAT_WE_MEASURED = """Presence was composed from a fixed six-model panel in two phases. The recognition phase asked each model, for each brand, whether it is commonly recognized as a technology brand — a yes/no count from zero to six. The recall phase posed six category-level prompts and counted how often each brand surfaced, split into a quality channel (best, expert-chosen, highest-quality) and a cultural channel (most talked-about, biggest footprint, most iconic). Presence is the equal-weight mean of those three components on a 0–100 scale — the same composition behind the program's convergent benchmark.

The 24-brand panel was drawn from the technology category of the BRAND database, stratified across the full familiarity range so the test would not be confined to famous brands or obscure ones. It spans Apple, Google, and Microsoft at one end through Corning, VMware, NetApp, Jabil, and Pitney Bowes at the other. One Samsung-owned brand was removed before sampling to keep the panel clean of any conflict.

The whole measurement was run blind to the human validator. Presence was composed first; only at a single, pre-registered scoring step was it joined to familiarity and recognition and the verdicts read. Nothing about the human norms could shape how Presence was built."""

PATTERNS = [
    {
        "id": "verdict",
        "title": "The recognition question is settled; the fame question is open",
        "body": (
            "Two relationships were tested against a fixed reducibility threshold of 0.74 — the "
            "level at which a discriminant correlation would be as strong as the metric's own "
            "convergent benchmark, and therefore redundant. Presence versus recognition sits well "
            "inside the distinct range and its interval stops short of that line: confirmed. "
            "Presence versus familiarity has its central estimate in the partial range, but an "
            "interval so wide it reaches from clearly-distinct to fully-reducible. The locked rule "
            "reads that as unresolved, not as a partial finding. The figure shows why: one interval "
            "clears the threshold, the other straddles the whole field."
        ),
    },
    {
        "id": "scatters",
        "title": "Presence and human memory track each other loosely",
        "body": (
            "Plotted against both human norms, Presence rises with them but scatters widely around "
            "the trend. The leaders cluster high on every measure; the rest of the panel spreads out, "
            "and the brands that sit far off the line are the same ones that dissociate. The loose fit "
            "is the point — a tight fit would have meant Presence was simply re-indexing fame."
        ),
    },
    {
        "id": "dissociation",
        "title": "The model layer keeps its own map of the category",
        "body": (
            "Eleven brands diverge by more than a standard deviation between AI presence and human "
            "familiarity. The amplified set — Apple, Microsoft, HPE, NetApp — reads larger in the "
            "models than in human fame: core-technology identity the panel surfaces readily. The "
            "suppressed set splits in two: culturally famous brands the models do not treat as "
            "category-canonical technology (Netflix, Instagram, Uber, Airbnb), and human-familiar "
            "brands with thin model presence (Whirlpool, 3M, QVC). Knowing which side a brand falls "
            "on is the actionable read here."
        ),
    },
    {
        "id": "composition",
        "title": "For enterprise brands, AI recall goes quiet",
        "body": (
            "Presence has three parts: recognition, quality-recall, and cultural-recall. For most of "
            "this enterprise-heavy panel the two recall channels contribute almost nothing — the "
            "models recognize the brand as technology but do not volunteer it under 'best' or 'most "
            "iconic' consumer prompts. Presence reduces toward its recognition component, which is "
            "the main reason the familiarity test came in underpowered: for these brands, the recall "
            "signal that would most sharply distinguish Presence from fame simply did not fire."
        ),
    },
]

LIMITATIONS = """The binding limitation is sample size. At 24 brands the confidence intervals are wide enough that the primary, familiarity question cannot be resolved either way. The panel size was fixed by the need to stratify a single category by familiarity while holding the model panel and prompt battery constant; resolving the fame question requires a larger panel, which is the next study, not a reinterpretation of this one.

The substrate amplified that constraint. An enterprise-heavy technology panel under consumer-framed recall prompts floored the recall channels, so for most brands Presence reduced toward recognition. The discriminant tests therefore largely evaluated AI recognition against the human norms, not the full three-part Presence construct. A consumer category, where recall does not floor, would test the whole construct against familiarity more cleanly.

The reducibility threshold is borrowed from the program's convergent benchmark, which used a wider prompt set than the battery here, so the comparison is approximate on prompt breadth. It is used as a fixed, pre-registered decision line, not as a precise like-for-like quantity."""

WHATS_NEXT = """The immediate next step is a higher-powered replication of the familiarity test on a consumer category where recall does not floor, so that the full Presence composite — not its recognition component alone — is what confronts fame. That is what would convert this open question into a verdict.

Two further tests would complete the picture: a direct comparison against mental availability using category-entry-point measures, and a recognition replication on a substrate where AI and human recognition are expected to diverge more sharply. Consolidating these is the gate to expanding AIAS beyond Presence to the full multi-component score.

This study is one cell of a larger validation. It sits alongside the convergent evidence (Presence tracks an external interest signal) and the discriminant evidence against retail-sales rank, together forming a convergent-and-discriminant pairing across methods. Read as a set, the program is building the case that AI Availability measures something the existing brand measures do not."""

HYPOTHESIS_SCORING = [
    {
        "id": "H_Disc_Familiarity",
        "label": "Presence vs familiarity (primary)",
        "prediction": "rho in 0.30–0.60 (partial, modal)",
        "verdict": "UNDETERMINED",
        "detail": (
            "rho = 0.593, central estimate in the partial band; BCa 95% CI [0.179, 0.832] spans "
            "all three bands, so the locked override returns UNDETERMINED rather than the point "
            "verdict. Unresolved at n = 24."
        ),
    },
    {
        "id": "H_Disc_Recognition",
        "label": "Presence vs recognition d' (secondary)",
        "prediction": "discriminant (|rho| < 0.50)",
        "verdict": "CONFIRMED",
        "detail": (
            "rho = 0.379, inside the distinct band; BCa 95% CI [-0.076, 0.714], upper bound below "
            "the 0.74 reducibility threshold, so redundancy is excluded. Confirmed, though the "
            "interval is wide."
        ),
    },
    {
        "id": "H_Dissociation",
        "label": "Presence–familiarity dissociation (descriptive)",
        "prediction": "—  (non-gating, illustrative)",
        "verdict": "FULL",
        "detail": (
            "11 of 24 brands cross ±1 SD in both directions (4 amplified, 7 suppressed). Mechanically "
            "coupled to the primary correlation; reported as corroborating texture, excluded from the "
            "headline."
        ),
    },
]

HYPOTHESIS_DETAILS = """H_Disc_Familiarity — UNDETERMINED. The point estimate landed where the registered prediction said it would, in the partial band. What the prediction could not anticipate was how wide the interval would be at this sample size: from 0.18, which would mean a clearly distinct measure, to 0.83, which would mean one effectively reducible to fame. An honest reading cannot pick a side, and the pre-registered rule was written precisely to stop a tempting central number from being reported as a result. The verdict is "unresolved," and it is the most defensible thing the data support.

H_Disc_Recognition — CONFIRMED. Presence correlates with human recognition sensitivity only moderately, and the interval's upper bound stops short of the redundancy threshold. The model's judgement that a brand is "technology" is not a restatement of how reliably a person recognizes it. The interval reaches into the partial band, so the discriminance is confirmed but not robust — stated plainly rather than rounded up.

H_Dissociation — FULL. The amplified brands are the category's core-technology names; the suppressed brands are either culturally famous but not category-canonical, or human-familiar with thin model presence. The pattern is systematic and reconciles with the recall evidence — the brands the models recall culturally but not for quality, and the reverse. It is descriptive and mechanically tied to the familiarity correlation, so it corroborates rather than proves, but it is the clearest picture of how AI presence and human fame part ways."""

CLOSING = {
    "byline_long": (
        "Pablo Ulpiano González Castro — Principal Researcher, Third System™ / "
        "Faculty, MPS Branding Program, School of Visual Arts."
    ),
    "datasets": (
        "Human norms: the BRAND database (familiarity and recognition d', Brand Finance "
        "US 500). AI Presence: a six-model panel, 144 recognition probes and 36 recall "
        "queries over 24 technology brands. Pre-registration, data, scoring, and verdicts "
        "deposited at OSF (osf.io/ec6wh, v28)."
    ),
    "methodology_log": (
        "Pre-registered at git tags v0.28-prereg-r1 / r2 before any model was queried. "
        "Presence composed blind to the validator; joined to the human norms only at a "
        "single, one-shot scoring step (seed 280400, BCa 95% CI, 10,000 resamples). "
        "Verdicts locked at v0.28-results-locked and deposited unchanged."
    ),
}
