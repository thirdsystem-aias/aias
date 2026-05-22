"""v0.17 brand-format report content + chart data module — Premium Kitchenware.

Schema-compatible with build_report_v17.py's read patterns (mirrors v16_knives_content.py
schema). Also provides the chart-data loaders that build_charts_v17.py consumes.

Substantive content for v0.17:
  - Headline: H_Regime4_kitchenware FALSIFIED-on-panel-inadequacy + Recognition x
    Recall dissociation as the methodologically significant secondary finding
  - Two pre-registered hypotheses: H_Regime4_kitchenware (substantive, FALSIFIED on
    panel inadequacy) and H_IdentityLoad_moderator (joint v0.16/v0.17, AMBIGUOUS
    pending v0.18 indie fragrance)
  - PATTERNS = 3 findings (vs v0.16's 5): Phase B mention-rate distribution,
    cell collapse and C1 floor breach, Recognition x Recall dissociation
  - LIMITATIONS adds three v0.17-specific paragraphs: panel pre-substrate-
    substitution, cross-cultural confound, single substrate/time-window
  - HYPOTHESIS_SCORING contains both substantive + joint verdict rows
  - Three-chart slot allocation matches the v17 chart build:
    f1_mention_rates / f2_cell_collapse / f3_dissociation

Constants exposed (in order):
  COVER * STANDFIRST * LEAD_DECK * EXEC_SUMMARY *
  WHAT_WE_MEASURED * PATTERNS * HYPOTHESIS_SCORING *
  HYPOTHESIS_DETAILS * LIMITATIONS * WHATS_NEXT * CLOSING

Chart-data loaders (consumed by build_charts_v17.py):
  load_phase_a_scores() * load_phase_b_mention_rates() *
  CELL_COUNTS * C1_FLOOR * TOTAL_PRE * TOTAL_POST
"""

import csv
from pathlib import Path

ROOT = Path.home() / "aias"
V17_ROOT = ROOT / "osf" / "v17"
LEDGER = V17_ROOT / "classification_ledger.csv"
PHASE_B_LOG = V17_ROOT / "registries" / "topic_id_resolution_log_v0.17.csv"


# ============================================================================
# CHART DATA (consumed by build_charts_v17.py)
# ============================================================================

PHASE_A_SCORES_FALLBACK = {
    "Le Creuset": 6,
    "All-Clad":   6,
    "Vermicular": 4,  # FAILED supermajority; descoped before Phase B
    "Iwachu":     6,
}

PHASE_B_MENTION_RATES_FALLBACK = [
    ("Le Creuset",    "european", 1.000, "PASS"),
    ("Mauviel",       "european", 1.000, "PASS"),
    ("All-Clad",      "american", 1.000, "PASS"),
    ("Staub",         "european", 0.944, "PASS"),
    ("Demeyere",      "european", 0.833, "PASS"),
    ("Lodge",         "american", 0.389, "PASS"),
    ("de Buyer",      "european", 0.333, "PASS"),
    ("Hestan",        "american", 0.333, "PASS"),
    ("Made In",       "american", 0.222, "PASS"),
    ("Fissler",       "european", 0.111, "PASS_E5"),
    ("Field Company", "american", 0.000, "EXCLUDED_E1a"),
    ("Smithey",       "american", 0.000, "EXCLUDED_E1a"),
    ("Iwachu",        "japanese", 0.000, "EXCLUDED_E1a"),
    ("Sori Yanagi",   "japanese", 0.000, "EXCLUDED_E1a"),
    ("Noda Horo",     "japanese", 0.000, "EXCLUDED_E1a"),
]

CELL_COUNTS = {
    "european": {"pre": 6, "post": 6},
    "american": {"pre": 6, "post": 4},
    "japanese": {"pre": 4, "post": 0},
}

C1_FLOOR = 12
TOTAL_PRE = 16
TOTAL_POST = 10


def _slug_to_canonical(slug: str) -> str:
    mapping = {
        "le-creuset": "Le Creuset", "all-clad":   "All-Clad",
        "vermicular": "Vermicular", "iwachu":     "Iwachu",
    }
    return mapping.get(slug.lower(), slug)


def load_phase_a_scores() -> dict:
    if not LEDGER.exists():
        return PHASE_A_SCORES_FALLBACK
    try:
        rows = list(csv.DictReader(LEDGER.open(encoding="utf-8")))
        scores: dict = {}
        for row in rows:
            brand = _slug_to_canonical(row["brand"])
            scores.setdefault(brand, 0)
            if row["anchored"].strip() == "1":
                scores[brand] += 1
        return scores if scores else PHASE_A_SCORES_FALLBACK
    except Exception:
        return PHASE_A_SCORES_FALLBACK


def load_phase_b_mention_rates() -> list:
    if not PHASE_B_LOG.exists():
        return PHASE_B_MENTION_RATES_FALLBACK
    try:
        rows = list(csv.DictReader(PHASE_B_LOG.open(encoding="utf-8")))
        data = []
        for row in rows:
            data.append((
                row["brand_canonical"], row["cell"],
                float(row["mention_rate"]), row["final_query_tier"],
            ))
        data.sort(key=lambda x: -x[2])
        return data if data else PHASE_B_MENTION_RATES_FALLBACK
    except Exception:
        return PHASE_B_MENTION_RATES_FALLBACK


# ============================================================================
# COVER
# ============================================================================

COVER = {
    "title":         "Premium Kitchenware \u2014 Recognition \u00d7 Recall Dissociation",
    "subtitle":      "AI Availability Score (AIAS) v0.17 Phase B Measurement",
    "date":          "May 2026",
    "byline_short":  "Pablo Ulpiano Gonzalez Castro, Third System\u2122",
    "tagline":       "Independent measurement for the AI mediation layer.",
}

# ============================================================================
# STANDFIRST + LEAD DECK
# ============================================================================

STANDFIRST = (
    "v0.17 brings the AIAS Presence Measurement Protocol v1.4 to the premium "
    "kitchenware substrate. The substantive pre-registered hypothesis "
    "<b>FALSIFIES on panel inadequacy</b> \u2014 worldwide n = 10, below the "
    "C1 floor of n \u2265 12. The joint Identity-Load verdict resolves to "
    "<b>AMBIGUOUS</b> pending v0.18 indie fragrance. The substantive verdict "
    "is informationally weak; the secondary finding \u2014 the Recognition "
    "\u00d7 Recall dissociation surfaced in the Japanese cell \u2014 is the "
    "most theoretically significant single result the AIAS programme has "
    "produced to date."
)

LEAD_DECK = (
    "Three principal outcomes from a single Phase B measurement against the "
    "locked six-LLM reference panel (3 category queries \u00d7 6 LLMs = 18 "
    "cells per brand). "
    "<b>(1) H_Regime4_kitchenware FALSIFIED</b> on panel inadequacy \u2014 "
    "worldwide n = 10 below the pre-registered C1 floor of 12 after Phase A "
    "descope of Vermicular and Phase B exclusion of five brands. "
    "<b>(2) H_IdentityLoad_moderator (joint v0.16/v0.17) AMBIGUOUS</b> \u2014 "
    "the pre-registered joint verdict matrix at cell PARTIAL \u00d7 FALSIFIED "
    "routes the Identity Load moderator hypothesis to v0.18 indie fragrance for "
    "resolution. "
    "<b>(3) Recognition \u00d7 Recall dissociation \u2014 the Iwachu canonical "
    "case.</b> Phase A C<sub>P</sub> PASS at 6/6 anchoring (LLMs identify "
    "Iwachu as a Japanese cookware brand); Phase B EXCLUDED_E1a at 0/18 "
    "mention rate (LLMs do not surface Iwachu in unprompted premium-cookware "
    "category retrieval). The dissociation generalizes across the Japanese "
    "cell and motivates the v1.4 Methodology revision specifying AI Availability "
    "as a multi-component construct comprising Recognition and Recall."
)

# ============================================================================
# EXECUTIVE SUMMARY (list of paragraph strings)
# ============================================================================

EXEC_SUMMARY = [
    (
        "AI assistants increasingly mediate brand discovery for consumer "
        "purchases. The AIAS\u2122 Presence Measurement programme operationalises "
        "this with <b>AI Availability</b>: the conditions under which a brand "
        "surfaces in AI-generated category retrieval. v0.17 brings the v1.4 "
        "Protocol to the premium kitchenware substrate, the second leg of a "
        "joint test of the Identity Load moderator hypothesis (with v0.16 "
        "Kitchen Knives as the first leg, SSRN 6791999). The v0.17 brand panel "
        "comprises 16 brands stratified across three tradition cells: "
        "<b>european</b> (Le Creuset as primary pivot, Staub, Mauviel, Demeyere, "
        "Fissler, de Buyer; n = 6); <b>american</b> (All-Clad as primary pivot, "
        "Lodge, Made In, Field Company, Smithey, Hestan; n = 6); <b>japanese</b> "
        "(Vermicular as primary pivot, Iwachu, Sori Yanagi, Noda Horo; n = 4). "
        "Phase A and Phase B both completed against the locked six-slot "
        "reference panel."
    ),
    (
        "<b>H_Regime4_kitchenware FALSIFIED on panel inadequacy.</b> Post-"
        "Phase-B worldwide n = 10, below the pre-registered C1 floor of "
        "n \u2265 12. The Japanese cell collapsed entirely (0/3 eligible after "
        "Vermicular's Phase A descope and Iwachu/Sori Yanagi/Noda Horo's "
        "Phase B exclusions). The American cell sustained partial attrition "
        "(Field Company and Smithey EXCLUDED_E1a at 0/18 mentions). The "
        "European cell remained intact at 6/6 eligible. Per pre-reg \u00a72 "
        "decision rule (\u00ac C1 \u2228 \u00ac C2): <b>FALSIFIED</b>. The "
        "pre-registration anticipated this outcome path explicitly; no "
        "post-hoc decision rule modification or threshold adjustment was "
        "applied."
    ),
    (
        "<b>H_IdentityLoad_moderator (joint v0.16/v0.17) AMBIGUOUS.</b> The "
        "joint Identity-Load moderator hypothesis is tested across v0.16 "
        "Kitchen Knives (PARTIAL) and v0.17 Premium Kitchenware (FALSIFIED). "
        "The pre-registered joint verdict matrix at cell PARTIAL \u00d7 "
        "FALSIFIED routes to <b>AMBIGUOUS pending v0.18</b> indie fragrance. "
        "v0.18 is the deciding test of the Identity Load moderator on a "
        "same-language English-only substrate, removing the cross-cultural "
        "confound that contaminated v0.17's Japanese-cell test."
    ),
    (
        "<b>Recognition \u00d7 Recall dissociation \u2014 the methodological "
        "headline.</b> Iwachu achieved Phase A C<sub>P</sub> PASS at 6/6 "
        "(every LLM in the reference panel identifies Iwachu as a Japanese "
        "cookware brand when asked to disambiguate the canonical name) and "
        "Phase B EXCLUDED_E1a at 0/18 mentions (no LLM surfaces Iwachu in "
        "unprompted premium-cookware category retrieval across three queries "
        "and six models). The dissociation generalised across the Japanese "
        "cell. The Iwachu canonical case demonstrates that AI Availability "
        "is multi-component: a brand can have full recognition anchoring "
        "without any recall presence. The v1.4 Methodology paper revision "
        "formalises this as the Recognition + Recall decomposition of "
        "AIAS Presence. In the author's assessment this is the most "
        "theoretically significant single result the AIAS programme has "
        "produced to date \u2014 of greater long-term value than the "
        "substantive verdict itself."
    ),
]

# ============================================================================
# WHAT WE MEASURED
# ============================================================================

WHAT_WE_MEASURED = {
    "heading": "What We Measured",
    "paragraphs": [
        (
            "v0.17 measures Phase A C<sub>P</sub> anchoring (Recognition) and "
            "Phase B mention rate (Recall) for premium kitchenware brands across "
            "six reference LLMs: claude-opus-4-5, claude-sonnet-4-5, gpt-4o, "
            "gpt-4o-mini, gemini-2.5-flash, gemini-2.5-flash-lite. The reference "
            "panel is locked across all v0.17 measurement; provider model "
            "substitutions during the acquisition window are documented in "
            "DEVIATIONS Entries 2 and 3 (substitutions made before any pivot-"
            "validation data acquisition). Single measurement wave at May 2026."
        ),
        (
            "<b>Brand panel.</b> v0.17 registry (<font name='Helvetica'>"
            "brands_kitchenware_v0.17.json</font>) covers three tradition cells: "
            "<b>european</b> (Le Creuset as primary pivot, Staub, Mauviel, "
            "Demeyere, Fissler, de Buyer; n = 6); <b>american</b> (All-Clad as "
            "primary pivot, Lodge, Made In, Field Company, Smithey, Hestan; n = "
            "6); <b>japanese</b> (Vermicular as primary pivot, Iwachu, Sori "
            "Yanagi, Noda Horo; n = 4, with Noda Horo pre-registered as "
            "borderline_classification: true, borderline_resolution_at: "
            "phase_b_topic_id). The panel was pre-registered at worldwide n = 16 "
            "pre-floor with conservative anticipated attrition of 1\u20133 brands."
        ),
        (
            "<b>Phase A cascade.</b> The European and American primary pivots "
            "achieved C<sub>P</sub> PASS at full 6/6 anchoring without cascade. "
            "The Japanese primary pivot Vermicular C<sub>P</sub> FAILED at 4/6: "
            "two reference models (gpt-4o-mini at slot 4; gemini-2.5-flash at "
            "slot 5) led their responses with non-substrate referents ('multiple "
            "meanings' framing and adjective definition respectively). The "
            "cascade activated Japanese cell ordinal 2 \u2014 Iwachu \u2014 "
            "which achieved C<sub>P</sub> PASS at 6/6 with classifier "
            "rationales reading uniformly as variations on 'Japanese "
            "manufacturer of cast iron cookware.' Iwachu's Iwate nambu-tekki "
            "heritage anchors cleanly. Phase A formally closed at git tag "
            "<font name='Helvetica'>v0.17-phase-a-locked</font> (commit "
            "<font name='Helvetica'>8cdf0cd</font>) with a 15-brand operational "
            "panel."
        ),
        (
            "<b>Phase B LLM-substrate measurement.</b> v0.17 implements the "
            "v1.4-canonical LLM-substrate Phase B specification (provisional "
            "in v0.17 per DEVIATIONS Entry 7, canonical in v1.4 Methodology "
            "paper). Three tradition-agnostic category queries: "
            "<i>What are the best premium cookware brands?</i>; "
            "<i>Recommend high-quality cookware brands for serious home cooks.</i>; "
            "<i>What cookware brands do professional chefs use?</i> "
            "Each query issued once per reference slot \u2014 18 measurement "
            "cells per brand (3 queries \u00d7 6 LLMs). Mentions detected via "
            "mechanical alias generation: canonical and lowercase variants of "
            "the brand name, plus hyphen-substitution and space-substitution "
            "variants. The Noda Horo borderline classification resolved at "
            "Phase B as OUT_OF_SCOPE (enamelware-only; not in-scope premium "
            "cookware) per the protocol-mandated borderline_resolution_at "
            "schedule."
        ),
        (
            "<b>Verdict and decision rules.</b> All pre-registered conditions "
            "and thresholds locked at git tag "
            "<font name='Helvetica'>v0.17-prereg-r1</font> (commit "
            "<font name='Helvetica'>3ebe426</font>, 19 May 2026 UTC) prior to "
            "any acquisition. Phase B locked at git tag "
            "<font name='Helvetica'>v0.17-phase-b-locked</font> (commit "
            "<font name='Helvetica'>54c83ec</font>). Verdicts follow "
            "mechanically from the pre-registered decision rules. No post-"
            "acquisition rule modification, threshold adjustment, or "
            "interpretive reframing has been applied. Methodological findings "
            "in Pattern 3 are post-hoc observations that motivated the v1.4 "
            "Methodology paper revision but did not affect the substantive "
            "verdict on H_Regime4_kitchenware."
        ),
    ],
}

# ============================================================================
# FINDINGS (PATTERNS)
# ============================================================================

PATTERNS = [
    {
        "number": 1,
        "title": "Phase B mention-rate distribution \u2014 European saturates, Japanese collapses",
        "chart_slot": "f1_mention_rates",
        "n_lead": 2,
        "paragraphs": [
            (
                "<b>The cross-cell distribution sets the empirical stage.</b> "
                "Each of the 15 brands in the post-Phase-A operational panel "
                "was queried against the six-LLM reference panel under three "
                "tradition-agnostic category queries, producing 18 measurement "
                "cells per brand. The mention rate is the proportion of those "
                "18 cells in which the brand was mentioned by the LLM in its "
                "response. The distribution is steeply asymmetric across "
                "tradition cells."
            ),
            (
                "<b>European cell saturates the high-mention end.</b> Le Creuset, "
                "Mauviel, and All-Clad (American) reach 18/18 = 1.000 \u2014 "
                "mentioned in every cell. Staub at 17/18, Demeyere at 15/18, "
                "Lodge at 7/18, de Buyer and Hestan at 6/18, Made In at 4/18. "
                "Fissler sits at 2/18 \u2014 below the 1/6 PASS threshold but "
                "above the EXCLUDED_E1a floor, classified PASS_E5 per the v1.4 "
                "tier vocabulary."
            ),
            (
                "<b>Long-tail American attrition.</b> Field Company and Smithey "
                "\u2014 both small-batch American specialty makers \u2014 sit at "
                "0/18 mentions across all 18 cells. EXCLUDED_E1a. Both brands "
                "have stable identity in English-language commerce but do not "
                "surface in LLM-generated category retrieval at any frequency. "
                "This is the structural pattern v1.4 §5.2 documents as long-tail "
                "LLM-substrate attrition: the LLM panel concentrates its category "
                "responses on the most prominent five-to-ten brands and rarely "
                "mentions beyond that band."
            ),
            (
                "<b>Japanese cell collapses entirely.</b> Iwachu, Sori Yanagi, "
                "and Noda Horo all sit at 0/18 \u2014 zero mentions across the "
                "entire measurement matrix. The full-cell collapse is hard to "
                "disambiguate from Western-LLM training-data bias on a cross-"
                "cultural substrate (see Limitations and Pattern 3). The pre-"
                "registration anticipated panel-collapse outcomes as a possible "
                "path; the pre-reg \u00a73.2 worst-case scenario was full "
                "Japanese collapse leaving worldwide n = 12 at the C1 floor "
                "exactly. The observed outcome combined full Japanese collapse "
                "with partial American attrition, producing n = 10 \u2014 two "
                "brands below the C1 boundary."
            ),
        ],
    },
    {
        "number": 2,
        "title": "H_Regime4_kitchenware FALSIFIED on panel inadequacy \u2014 the C1 floor breach",
        "chart_slot": "f2_cell_collapse",
        "n_lead": 2,
        "paragraphs": [
            (
                "<b>The substantive pre-registered hypothesis.</b> "
                "H_Regime4_kitchenware tests whether the premium kitchenware "
                "substrate exhibits the Regime 4 pattern of AI-mediated "
                "retrieval per the v1.2 four-regime taxonomy, conditional on "
                "panel adequacy and effect-size persistence under tradition "
                "and age controls. Three pre-registered conditions: <b>C1</b> "
                "(n \u2265 12 eligible brands at worldwide); <b>C2</b> (Spearman "
                "<font name='Helvetica'>\u03c1</font> satisfies Regime 4 "
                "boundary); <b>C3</b> (partial <font name='Helvetica'>\u03c1</font> "
                "controlling for age and tradition retains the boundary). "
                "Decision rule: <b>FALSIFIED</b> if \u00ac C1 \u2228 \u00ac C2."
            ),
            (
                "<b>C1 is breached.</b> Worldwide eligible n = 10 at end of "
                "Phase B. C1 floor is n \u2265 12. Deficit: 2 brands below "
                "the boundary. C2 and C3 are not evaluated because the verdict "
                "resolves at C1. Per the pre-reg \u00a72 decision rule: "
                "<b>FALSIFIED on panel inadequacy</b>. The pre-registration "
                "anticipated this outcome path explicitly \u2014 \u00a73.2 "
                "names full Japanese cell collapse as the worst-case scenario "
                "the panel design accommodates."
            ),
            (
                "<b>Two attrition stages.</b> The worldwide n dropped from the "
                "pre-registered 16 to the operational 10 across two stages. "
                "Stage 1 \u2014 Phase A: Vermicular C<sub>P</sub> FAILED at "
                "4/6 and was descoped, dropping the Japanese cell from 4 to 3. "
                "Stage 2 \u2014 Phase B: Field Company and Smithey EXCLUDED_E1a "
                "from the American cell (American 6 \u2192 4); Iwachu, Sori "
                "Yanagi, Noda Horo EXCLUDED_E1a from the Japanese cell "
                "(Japanese 3 \u2192 0). The European cell remained intact at "
                "6/6 throughout."
            ),
            (
                "<b>Joint Identity-Load verdict: AMBIGUOUS.</b> The pre-"
                "registered joint verdict matrix combines v0.16 (PARTIAL on "
                "kitchen knives) with v0.17 (FALSIFIED on kitchenware) to "
                "resolve the Identity Load moderator hypothesis. At cell "
                "PARTIAL \u00d7 FALSIFIED, the matrix routes to "
                "<b>AMBIGUOUS pending v0.18</b> indie fragrance. v0.18 will "
                "test the moderator on a same-language English-only substrate, "
                "removing the cross-cultural confound and providing the "
                "deciding evidence."
            ),
            (
                "<b>Limitation acknowledged.</b> The substrate-substitution "
                "from Trends to LLM-substrate Phase B (DEVIATIONS Entry 7) was "
                "applied after pre-registration lock. The Trends-substrate "
                "panel design anticipated 1\u20133 brands of attrition; the "
                "LLM-substrate produced 5 brands. The FALSIFIED verdict is "
                "mechanically correct against the pre-reg, but is partly a "
                "consequence of the substrate substitution rather than a clean "
                "test of the substantive hypothesis. v0.18 panel sizing will "
                "over-provision for LLM-substrate attrition at 30\u201350% "
                "per cell."
            ),
        ],
    },
    {
        "number": 3,
        "title": "Recognition \u00d7 Recall dissociation \u2014 the Iwachu canonical case",
        "chart_slot": "f3_dissociation",
        "n_lead": 2,
        "paragraphs": [
            (
                "<b>The methodologically significant finding.</b> Iwachu \u2014 "
                "the Japanese cell pivot activated when Vermicular failed Phase A "
                "\u2014 produced a structurally robust dissociation between two "
                "measurement surfaces of LLM-mediated brand retrieval. At Phase A, "
                "the disambiguation query \u201cWho or what is Iwachu?\u201d "
                "produced six responses, each of which led with an identification "
                "statement placing Iwachu within the cookware substrate (LLM "
                "rationales read uniformly as \u201cJapanese manufacturer of cast "
                "iron cookware\u201d). At Phase B, the same six reference LLMs "
                "queried with three unprompted category queries about premium "
                "cookware brands produced 18 response cells in which Iwachu was "
                "mentioned zero times. The brand has stable identity in the LLM\u2019s "
                "representation but no recall presence in category-conditioned "
                "retrieval."
            ),
            (
                "<b>The dissociation is within-LLM.</b> The same individual model "
                "that produced \u201cIwachu is a Japanese cookware brand\u201d in "
                "response to the Phase A query did not include Iwachu in its "
                "response to the Phase B query \u201cWhat are the best premium "
                "cookware brands?\u201d Six LLMs, three queries, zero mentions \u2014 "
                "while Phase A produced 6/6 anchoring across the same six LLMs. "
                "This is not classifier disagreement, prompt artefact, or "
                "measurement noise. The model knows what Iwachu is. It does not "
                "surface Iwachu when asked about its category."
            ),
            (
                "<b>The pattern generalises across the Japanese cell.</b> "
                "Sori Yanagi and Noda Horo, like Iwachu, received 0/18 mentions "
                "at Phase B. The full Japanese cell at Phase B exhibits the "
                "same dissociation pattern: stable identity (for Iwachu, "
                "confirmed at Phase A; for Sori Yanagi and Noda Horo, assumed "
                "by symmetry pending direct measurement) but zero recall "
                "presence in unprompted category retrieval."
            ),
            (
                "<b>AI Availability is multi-component.</b> The Iwachu canonical "
                "case is the empirical anchor for the v1.4 Methodology revision "
                "specifying AI Availability as a multi-component construct with "
                "<b>Recognition</b> and <b>Recall</b> as the two principal "
                "components. The substantive theoretical interest is in the "
                "Recall component: consumer behaviour in AI-mediated commerce "
                "depends on what AI intermediaries spontaneously surface (Recall), "
                "not on what they can identify when prompted (Recognition). A "
                "brand can have full Recognition with zero Recall; such a brand "
                "has partial AI Availability but is functionally invisible in "
                "AI-mediated category retrieval. The v1.4 Methodology paper "
                "formalises Recognition + Recall as the canonical decomposition "
                "of AIAS Presence and reweights the Presence composite "
                "accordingly."
            ),
            (
                "<b>This is the most theoretically significant single result "
                "the AIAS programme has produced to date.</b> The implication "
                "for the broader Tri-System theoretical framework (manuscript "
                "in development for Routledge Studies in Marketing): AI "
                "Availability \u2014 the third system of brand availability "
                "alongside Mental Availability and Physical Availability \u2014 "
                "requires multi-component measurement. A single-metric proxy "
                "for AI Availability is inadequate. The Iwachu canonical case "
                "is the empirical demonstration."
            ),
        ],
    },
]

# ============================================================================
# HYPOTHESIS SCORING
# ============================================================================

HYPOTHESIS_SCORING = {
    "heading": "Hypothesis Scoring",
    "intro": (
        "Two pre-registered hypotheses for v0.17. All thresholds and decision "
        "rules locked at git tag <font name='Helvetica'>v0.17-prereg-r1</font> "
        "(commit <font name='Helvetica'>3ebe426</font>, 19 May 2026 UTC) prior "
        "to any acquisition. The substantive hypothesis H_Regime4_kitchenware "
        "tests Regime 4 replication on the premium kitchenware substrate; the "
        "joint hypothesis H_IdentityLoad_moderator tests Identity Load moderation "
        "across v0.16 (kitchen knives) and v0.17 (premium kitchenware) as the "
        "two medium-IL substrates. Methodological findings (Recognition \u00d7 "
        "Recall dissociation) are post-hoc observations from v0.17 and are not "
        "shown in this scoring table; their formal status is detailed in the "
        "v1.4 Methodology paper."
    ),
    "rows": [
        ("H_Regime4_kitchenware (substantive, worldwide)",
         "n \u2265 12 AND |bivariate <font name='Helvetica'>\u03c1</font>(AI, "
         "Trends)| satisfies Regime 4 boundary AND partial "
         "<font name='Helvetica'>\u03c1</font>(AI, Trends | age, tradition) "
         "retains the boundary at t<sub>1</sub> and t<sub>2</sub>",
         "n = 10 (worldwide eligible after Phase A descope of Vermicular and "
         "Phase B exclusion of 5 brands); C2 and C3 not evaluated \u2014 "
         "verdict resolves at C1",
         "FALSIFIED on panel inadequacy",
         "falsified"),
        ("H_IdentityLoad_moderator (joint v0.16 / v0.17)",
         "Joint verdict matrix combining v0.16 (PARTIAL on kitchen knives) "
         "with v0.17 substantive outcome; routes to CONFIRMED / PARTIAL / "
         "AMBIGUOUS / FALSIFIED per pre-reg matrix",
         "v0.16 PARTIAL \u00d7 v0.17 FALSIFIED \u2192 matrix cell routes to "
         "AMBIGUOUS pending v0.18 indie fragrance for resolution",
         "AMBIGUOUS",
         "ambiguous"),
    ],
}

# ============================================================================
# HYPOTHESIS DETAILS
# ============================================================================

HYPOTHESIS_DETAILS = {
    "heading": "Hypothesis Details",
    "intro": (
        "Per-hypothesis claim, operationalisation, and result. Both "
        "hypotheses pre-registered at "
        "<font name='Helvetica'>v0.17-prereg-r1</font> "
        "(commit <font name='Helvetica'>3ebe426</font>, 19 May 2026 UTC). "
        "Decision-rule language and threshold values quoted verbatim from "
        "the pre-registration."
    ),
    "items": [
        ("H_Regime4_kitchenware",
         "<b>Substantive hypothesis (v0.17).</b> Brand AI Availability on "
         "the premium kitchenware substrate is tested for the Regime 4 "
         "(Covariate-saturated weak) signature established on premium facial "
         "skincare (v0.11), personal finance apps (v0.13), premium tea "
         "(v0.14, v0.15), and kitchen knives (v0.16 PARTIAL). Three "
         "conditions tested: <b>(C1)</b> worldwide n \u2265 12 brands "
         "surviving Phase A pivot validation and Phase B mentionability; "
         "<b>(C2)</b> Spearman <font name='Helvetica'>\u03c1</font> on the "
         "operational panel satisfies the Regime 4 boundary; <b>(C3)</b> "
         "partial <font name='Helvetica'>\u03c1</font> controlling for age "
         "and tradition retains the boundary. Decision rule per pre-reg "
         "\u00a72: <b>FALSIFIED</b> if \u00ac C1 \u2228 \u00ac C2. Result: "
         "n = 10 (worldwide eligible after two-stage attrition); \u00ac C1 "
         "satisfied; FALSIFIED follows mechanically. C2 and C3 not "
         "evaluated. <b>FALSIFIED on panel inadequacy.</b>"),
        ("H_IdentityLoad_moderator (joint v0.16 / v0.17)",
         "<b>Joint hypothesis.</b> Identity Load moderates the strength of "
         "the Regime 4 pattern across substrates. v0.16 (kitchen knives, "
         "medium IL) and v0.17 (premium kitchenware, medium IL) form the "
         "two-leg test; v0.18 (indie fragrance, higher IL) and future low-IL "
         "substrates extend the test in either direction. The pre-registered "
         "joint verdict matrix specifies, for each combination of v0.16 and "
         "v0.17 outcomes, the corresponding joint Identity-Load verdict. "
         "The relevant cell for v0.17\u2019s outcome path is PARTIAL \u00d7 "
         "FALSIFIED \u2014 the matrix routes to <b>AMBIGUOUS pending "
         "v0.18</b>. v0.18 indie fragrance will be the deciding test on a "
         "same-language English-only substrate, removing the cross-cultural "
         "confound that contaminated v0.17\u2019s Japanese cell."),
    ],
}

# ============================================================================
# LIMITATIONS
# ============================================================================

LIMITATIONS = {
    "heading": "Limitations",
    "paragraphs": [
        (
            "<b>Panel design pre-substrate-substitution.</b> The v0.17 "
            "pre-registration panel was sized for Trends-substrate Phase B "
            "attrition (1\u20133 brands anticipated). The substrate "
            "substitution from Trends to LLM-substrate Phase B (DEVIATIONS "
            "Entry 7) was implemented after pre-registration lock and "
            "produced 5 brands of attrition \u2014 approximately twice the "
            "anticipated rate. The pre-registered FALSIFIED verdict is "
            "mechanically correct against the pre-reg, but is partly a "
            "consequence of the substrate substitution rather than a clean "
            "test of the substantive hypothesis. v0.18 panel sizing will "
            "over-provision for LLM-substrate attrition."
        ),
        (
            "<b>Cross-cultural confound on Japanese cell.</b> The Japanese "
            "cell\u2019s full collapse at Phase B is hard to disambiguate "
            "from Western-language LLM training-data bias on a cross-"
            "cultural substrate. Iwachu (Iwate nambu-tekki heritage), Sori "
            "Yanagi (designer-craft heritage), and Noda Horo (enamelware) "
            "all carry high Identity Load. By the substantive Identity-Load "
            "prediction, these brands should have shown stronger AI "
            "Availability than equivalently-positioned but lower-IL brands. "
            "The opposite pattern was observed. The v0.17 data does not "
            "distinguish between Reading 1 (Identity Load does not moderate "
            "AI Availability) and Reading 2 (Western-language training-data "
            "bias is large enough on cross-cultural substrates to swamp the "
            "Identity Load signal). v0.18 indie fragrance, with entirely "
            "English-language category surface, is the immediate forward "
            "action to disambiguate."
        ),
        (
            "<b>Single substrate, single time window.</b> v0.17 measures one "
            "substrate at one time window (May 2026). The Recognition \u00d7 "
            "Recall dissociation finding generalises within v0.17 across cells "
            "and brands but has not yet been replicated across substrates or "
            "time windows. v0.18 will provide the cross-substrate replication; "
            "the time-window replication is a v1.5+ forward action."
        ),
        (
            "<b>Mechanical alias generation, not semantic.</b> Phase B "
            "mention detection uses mechanical alias generation: canonical "
            "and lowercase variants, plus hyphen and space substitution. "
            "Semantic aliases (e.g., \u201cField and Company\u201d for "
            "\u201cField Company,\u201d or \u201cKnife Made In\u201d for "
            "\u201cMade In\u201d) are not generated. The v1.4 brand registry "
            "schema specifies an optional aliases field for brands requiring "
            "semantic-variant matching. None was registered for v0.17 \u2014 "
            "future programmes may include them."
        ),
        (
            "<b>Single classifier model at Phase A.</b> Phase A C<sub>P</sub> "
            "classification was automated via claude-opus-4-7 (DEVIATIONS "
            "Entry 4; provisional v1.4 \u00a76.4.2). Inter-rater reliability "
            "with operator judgment was not measured at v0.17; this is a v1.5+ "
            "forward action. The substrate-specific failure mode \u2014 the "
            "Vermicular \u201cmultiple meanings\u201d cascade trigger \u2014 "
            "was empirically successful in surfacing the Iwachu activation. "
            "But the classifier\u2019s decision boundary remains under-"
            "validated against operator judgment."
        ),
    ],
}

# ============================================================================
# WHAT'S NEXT
# ============================================================================

WHATS_NEXT = {
    "heading": "What's Next",
    "paragraphs": [
        (
            "<b>v0.17 publication sequence.</b> Brand-format report (this "
            "document), SSRN working paper, and OSF deposit ship together "
            "under git tag <font name='Helvetica'>v0.17-published</font>. "
            "The companion SSRN paper develops the substantive analysis "
            "alongside the formal hypothesis results and elevates the "
            "Recognition \u00d7 Recall dissociation as the methodological "
            "headline."
        ),
        (
            "<b>v0.18 indie fragrance \u2014 the deciding test.</b> The pre-"
            "registered joint verdict matrix routes the Identity-Load "
            "moderator hypothesis to v0.18 for resolution. Indie fragrance "
            "is entirely English-language, removing the cross-cultural "
            "confound that contaminated v0.17. The IL gradient within "
            "indie fragrance can be tested on equal LLM-coverage terms. "
            "v0.18 panel sizing will over-provision approximately "
            "30\u201350% for LLM-substrate attrition per cell, per the "
            "v0.17 lesson."
        ),
        (
            "<b>AIAS Protocol v1.4 Methodology paper.</b> Already shipped "
            "as SSRN forthcoming. v1.4 supersedes v1.2 and v1.3 and "
            "formalises Recognition + Recall as the canonical decomposition "
            "of AIAS Presence. The v0.17 program is the empirical anchor "
            "for the multi-component construct claim."
        ),
        (
            "<b>Tri-System Brand Growth and Routledge monograph.</b> The "
            "Tri-System MSI Working Paper bibliography is updated to "
            "incorporate v0.17 and AIAS Protocol v1.4 as empirical anchors "
            "for the framework\u2019s AI Availability axis. The Recognition "
            "\u00d7 Recall dissociation strengthens the framework\u2019s "
            "multi-component AI Availability claim. The Routledge "
            "monograph (<i>The Third System: AI Availability and the "
            "Architecture of Brand Growth</i>, in development) carries the "
            "finding forward as the empirical anchor for the multi-"
            "component construct of AI Availability."
        ),
        (
            "<b>AIAS 1.0 and Phase 4.</b> The full AIAS composite (Presence, "
            "Ranking, Consistency, Coverage, Grounding, Sentiment) remains "
            "a multi-year arc. v0.17 advances the Presence component with "
            "the Recognition \u00d7 Recall decomposition; Phase 4 will ship "
            "the remaining five components contingent on Phase 3 construct-"
            "validity results."
        ),
    ],
}

# ============================================================================
# CLOSING
# ============================================================================

CLOSING = {
    "byline_long": [
        "Pablo Ulpiano Gonz\u00e1lez Castro",
        "Founder, Third System\u2122",
        "Faculty, MPS Branding Program, School of Visual Arts",
    ],
    "datasets": [
        (
            "<b>OSF project ec6wh, /v17/.</b> Inputs: Phase A pivot validation "
            "across the six-LLM reference panel (claude-opus-4-5, claude-"
            "sonnet-4-5, gpt-4o, gpt-4o-mini, gemini-2.5-flash, gemini-2.5-"
            "flash-lite) with cascade activation of Iwachu after Vermicular "
            "C<sub>P</sub> FAIL (DEVIATIONS Entry 6); Phase B LLM-substrate "
            "mention measurement (three tradition-agnostic category queries "
            "\u00d7 six LLMs = 18 cells per brand); Phase B topic-ID "
            "resolution with Noda Horo borderline classification resolved "
            "as OUT_OF_SCOPE (enamelware-only); v0.17 registry "
            "(<font name='Helvetica'>brands_kitchenware_v0.17.json</font>, "
            "three tradition cells: european 6, american 6, japanese 4 pre-"
            "Phase A); classification ledger; Phase B response caches; "
            "scoring outputs; 3 chart PDFs from build_charts_v17.py; build "
            "scripts; this report; the matching SSRN working paper."
        ),
        (
            "<b>Companion SSRN working paper and AIAS programme cross-"
            "references.</b> v0.17 working paper: <i>Panel Inadequacy and "
            "the Recognition x Recall Dissociation on the Premium "
            "Kitchenware Substrate: AIAS v0.17</i>. Cross-references: AI "
            "Availability foundational paper (SSRN 6659000); AIAS Presence "
            "Measurement Protocol v1.1 (SSRN 6722319); AIAS Presence "
            "Measurement Protocol v1.2 (SSRN 6761698); AIAS Presence "
            "Measurement Protocol v1.3 (SSRN 6797679); AIAS Presence "
            "Measurement Protocol v1.4 (SSRN forthcoming); v0.6 Cross-"
            "Category Findings (SSRN 6720959); v0.7 Phantom-Brand "
            "Persistence Phase 2 BBB (SSRN 6721779); v0.8 Discourse-"
            "Language Knives (SSRN 6728000); v0.9 Longitudinal Re-Baseline "
            "(SSRN 6736878); v0.10 Naive-Phantom Rate Stability (SSRN "
            "6741163); v0.11 PM Software \u00d7 Trends Construct Validity "
            "Pilot (SSRN 6745040); v0.12 Three Empirical Regimes (SSRN "
            "6748341); v0.13 Four Empirical Regimes \u2014 Five-Category "
            "Construct-Validity Expansion (SSRN 6750498); v0.14 Kitchen "
            "Knives \u2014 Regime 4 Replication (SSRN 6755621); v0.15 "
            "Premium Tea Panel Expansion Robustness (SSRN 6768059); v0.16 "
            "Regime 4 Boundary and Discourse-Language Carryforward on "
            "Kitchen Knives (SSRN 6791999)."
        ),
    ],
    "methodology_log": (
        "v0.17 follows AIAS Presence Measurement Protocol v1.4 (SSRN "
        "forthcoming). Pre-registration locked at git tag "
        "<font name='Helvetica'>v0.17-prereg-r1</font> (commit "
        "<font name='Helvetica'>3ebe426</font>) on 19 May 2026 UTC prior to "
        "Phase A acquisition. Phase A formally closed at git tag "
        "<font name='Helvetica'>v0.17-phase-a-locked</font> (commit "
        "<font name='Helvetica'>8cdf0cd</font>); Phase B formally closed at "
        "git tag <font name='Helvetica'>v0.17-phase-b-locked</font> (commit "
        "<font name='Helvetica'>54c83ec</font>). DEVIATIONS.md: eight entries "
        "documented contemporaneously; key entries are Entry 4 (operator "
        "judgement \u2192 automated LLM classifier provisional v1.4 \u00a76.4.2); "
        "Entry 6 (Vermicular C<sub>P</sub> FAIL \u2192 Iwachu cascade activation); "
        "Entry 7 (substrate substitution from Trends to LLM-substrate Phase B, "
        "provisional v1.4 \u00a75.2). No pre-registered hypothesis, threshold, "
        "or routing rule was modified post-acquisition."
    ),
}
