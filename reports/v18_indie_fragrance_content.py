"""
v0.18 Indie Fragrance — Brand-format report content.

Schema matches v17_kitchenware_content.py exactly so build_report_v18.py can
copy forward from build_report_v17.py with minimal surgical changes.

All TBD-VERDICT markers from the pre-acquisition draft are resolved against
the actual v0.18 verdict (data/verdicts/v0_18_verdict.{json,md}).

Citation chain:
  - AIAS Protocol v1.4 (SSRN 6799479) — methodology base
  - v0.16 (SSRN 6791999), v0.17 (SSRN 6802261) — predecessor legs
  - Pre-reg tag v0.18-prereg-r1 at commit 183386c, refined through r4 at 1195cb8
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# Paths (parallel to v0.17 content module)
# ---------------------------------------------------------------------------

ROOT = Path.home() / "aias"
V18_ROOT = ROOT / "osf" / "v18"
PHASE_A_RESULTS = ROOT / "data" / "phase_a" / "v0.18" / "phase_a_results.json"
PHASE_B_RESULTS = ROOT / "data" / "phase_b" / "v0.18" / "phase_b_results.json"
VERDICTS_JSON = ROOT / "data" / "verdicts" / "v0_18_verdict.json"

# Panel totals (used by build script for page-count target and cell summaries)
TOTAL_PRE = 24       # worldwide pre-floor
TOTAL_POST = 24      # post-attrition (no panel substitution; Cell C cascade exhaustion
                     # treated as substantive finding per DEVIATIONS Entry 1)

CELL_COUNTS = {
    "Cell A — Designer-niche":   {"pre": 8, "post": 8},
    "Cell B — Indie / Artisan":  {"pre": 8, "post": 8},
    "Cell C — Mass-prestige":    {"pre": 8, "post": 8},
}


# ---------------------------------------------------------------------------
# COVER
# ---------------------------------------------------------------------------

COVER = {
    "title": "When Recognition Meets Recall",
    "subtitle": "AIAS v0.18 — Indie Fragrance",
    "date": "May 2026",
    "byline_short": "Pablo Ulpiano González Castro",
    "tagline": (
        "The dissociation construct generalizes. "
        "The Identity-Load moderator is real — but bounded."
    ),
}


# ---------------------------------------------------------------------------
# STANDFIRST — full-width callout on the lead spread (24pt bold indigo)
# Sized to fill the 396pt lead_top frame (~13 lines at 28pt leading) so the
# transition into the LEAD_DECK + EXEC_SUMMARY columns reads continuous,
# not gapped. Earlier 2-sentence version left ~280pt of empty space between
# the bottom of the callout and where the columns begin in lead_bottom.
# ---------------------------------------------------------------------------

STANDFIRST = (
    "Nine cases of Recognition without Recall, on a same-language indie-"
    "fragrance substrate. The Iwachu pattern generalizes — it is not a "
    "cross-cultural artifact but a measurable mechanism of AI-mediated "
    "retrieval. Six of the nine cases concentrate in the highest-"
    "Identity-Load cell, where 75% of brands exhibit the pattern. The "
    "Identity-Load moderator operates across the three-leg v0.16 / v0.17 / "
    "v0.18 history, bounded by substrate-specific qualifications. Three "
    "pre-registered hypotheses; three PARTIAL verdicts that say more "
    "together than apart."
)


# ---------------------------------------------------------------------------
# LEAD_DECK — intro paragraph below the standfirst (14pt light)
# ---------------------------------------------------------------------------

LEAD_DECK = (
    "The AIAS™ Presence Measurement Protocol v1.4 multi-component construct "
    "(Recognition × Recall) survives its first generalization test. Nine "
    "Iwachu-pattern cases on a same-language indie-fragrance substrate, "
    "concentrated in the highest-Identity-Load cell (6 of 8 brands, 75%). "
    "Three pre-registered hypotheses; three PARTIAL verdicts. Read together, "
    "they describe a moderator that operates through layer-specific channels "
    "and a methodology layer measurably closer to canonical."
)


# ---------------------------------------------------------------------------
# EXEC_SUMMARY — list of paragraphs, body text (9.4pt light)
# ---------------------------------------------------------------------------

EXEC_SUMMARY = [
    "v0.18 was designed to resolve two questions on a single substrate: "
    "the Identity-Load moderator left at AMBIGUOUS by the v0.16/v0.17 panel "
    "(v0.16 PARTIAL, v0.17 FALSIFIED on panel inadequacy), and the "
    "generalization of the Recognition × Recall dissociation pattern first "
    "identified on the v0.17 Japanese-cell substrate.",

    "The substrate is indie fragrance, sampled across three cells stratified "
    "by Identity Load: mass-prestige (medium IL), designer-niche (medium-high IL), "
    "and indie/artisan (high IL). 24 brands worldwide pre-floor, 8 per cell, "
    "English-language anchored throughout. Phase B uses three category-anchored "
    "query frames: niche, independent, and perfumistas. The locked six-slot "
    "reference panel from v0.17 is carried forward.",

    "All three pre-registered hypotheses returned PARTIAL verdicts. The "
    "Recognition × Recall dissociation generalizes across cells (9 cases "
    "in 2 of 3 cells) but with cell-clustering in the highest-IL cell "
    "(75% of Cell B brands exhibit the pattern). The Identity-Load moderator "
    "operates across the three-leg history with substrate-specific qualifications. "
    "The H_Regime4_indie_fragrance verdict resolves at C3 ranking coherence: "
    "C1 panel adequacy and both C2 conditions clear, but only one of three "
    "cells satisfies the per-cell ρ ≥ 0.50 floor.",

    "For senior brand leaders managing identity-bearing categories: the gap "
    "between what an AI knows about your brand (Recognition) and what it "
    "will say about your brand (Recall) is a measurable, category-level "
    "quantity. v0.18 puts a number on the gap — and identifies the substrate "
    "conditions under which it widens.",
]


# ---------------------------------------------------------------------------
# WHAT_WE_MEASURED — methodology section
# ---------------------------------------------------------------------------

WHAT_WE_MEASURED = {
    "heading": "What we measured",
    "paragraphs": [
        "Two acquisition phases scored by pre-registered decision rules. "
        "Phase A measures <b>Recognition</b> — whether the AI panel recognizes "
        "a brand as belonging to the category. Phase B measures <b>Recall</b> — "
        "whether the AI panel surfaces the brand when asked to enumerate "
        "category members. Phase D computes within-cell rank correlation "
        "between the two.",

        "Phase A asks each of the six reference panel models a single question "
        "per brand: <i>'Is this brand commonly recognized as a niche fragrance?'</i> "
        "The brand's Recognition score (C_P, range 0..6) is the count of "
        "recognition-positive responses across the panel. Per-cell pivot "
        "anchoring follows a cascade: the first brand achieving C_P = 6/6 "
        "becomes the cell pivot; remaining cell brands are probed for the "
        "dissociation analysis.",

        "Phase B asks the same six models three category-anchored queries — "
        "<i>'What are the best niche fragrances?'</i>, <i>'Recommend high-quality "
        "independent fragrance brands.'</i>, and <i>'What fragrances do industry "
        "insiders and perfumistas recommend?'</i> — and scans each response for "
        "brand mentions across the 24-brand registry. Each brand has at most "
        "18 observation slots (3 queries × 6 models).",

        "The Recognition × Recall dissociation threshold (the Iwachu-pattern "
        "case, novel for v0.18 testing) requires C_P ≥ 5/6 AND mention rate "
        "≤ 2/18 — the brand is recognized in 5+ of 6 single-brand probes, "
        "but surfaces in 2 or fewer of 18 enumeration responses. The verdict "
        "cascade for H_Regime4_indie_fragrance runs C1 (panel adequacy) → "
        "C2 within-cell → C2 IL-gradient → C3 ranking coherence per pre-reg "
        "r4 §4.0. The pre-registration is locked at commit 183386c with "
        "C2/C3 numerical thresholds locked at commit 1195cb8.",
    ],
}


# ---------------------------------------------------------------------------
# PATTERNS — three findings, each anchored by one chart
# ---------------------------------------------------------------------------

PATTERNS = [
    {
        "number": 1,
        "title": "Recognition meets Recall: the IL-gradient at first glance",
        "chart_slot": "f1_mention_rate_distribution",
        "paragraphs": [
            "Phase A Recognition shows a sharp Identity-Load gradient. "
            "Cell A (designer-niche) anchored Maison Francis Kurkdjian at "
            "C_P = 6/6 on the first cascade step; 7 of 8 cell brands "
            "scored 6/6 (mean C_P ≈ 5.88/6, near-saturation). Cell B "
            "(indie/artisan) anchored D.S. & Durga also at first cascade "
            "step, with mean C_P ≈ 5.00/6 across the cell (range 3 to 6). "
            "Cell C (mass-prestige) exhausted its full cascade without "
            "anchoring a pivot — no Cell C brand achieved C_P = 6/6 (mean "
            "C_P ≈ 0.25/6; 7 of 8 brands at 0/6, Tom Ford alone at 2/6).",

            "The Cell C → Cell A transition is a step function, not a "
            "smooth gradient. The 'niche fragrance' Recognition probe maps "
            "cleanly onto designer-niche and indie/artisan houses (Cells A "
            "and B) but cleanly off mass-prestige designer fragrance (Cell "
            "C). The asymmetry isn't a panel-construction error; it's the "
            "IL-gradient operating on Recognition itself. Mass-prestige "
            "fragrance is, by definition, not niche.",

            "The Cell A > Cell B inversion (5.88 vs. 5.00) is also "
            "substantive. The lexical anchor 'niche fragrance' maps most "
            "tightly to canonically-labeled designer-niche houses (Le Labo, "
            "Frederic Malle, Diptyque) than to the newer American-DTC indie "
            "houses (Henry Rose, Phlur, Ellis Brooklyn) that occupy an "
            "adjacent vocabulary space — 'indie', 'clean', or 'artisan' "
            "rather than 'niche' specifically. The Recognition gradient is "
            "real but operates at the threshold-and-vocabulary level, not "
            "as a smooth monotone function of Identity Load.",

            "Phase B Recall shows a parallel but differently-shaped gradient. "
            "Cell A's mentions distribute across many recognized houses "
            "(Le Labo 17/18, MFK 16/18, Diptyque 15/18, Frederic Malle 12/18, "
            "Byredo 10/18 — broad coverage, top-2 share 0.446 below the C2 "
            "within-cell threshold of 0.50 because Recall is too rich, not "
            "too sparse). Cell B shows near-total Recall attrition — 7 of 8 "
            "cell brands receive zero mentions across 18 observations; only "
            "D.S. & Durga surfaces, and only at 2/18. Cell C surfaces "
            "sporadically through general fragrance-discourse channels "
            "(Tom Ford 4, Chanel 3, Versace 1, Dior 1) despite failing the "
            "niche Recognition probe.",
        ],
    },
    {
        "number": 2,
        "title": "Cell attrition: panel registered to Phase B Recall-positive",
        "chart_slot": "f2_cell_attrition",
        "paragraphs": [
            "Brand survival from the pre-registered Phase A panel (24 brands; "
            "8 per cell) to the Phase B mention-positive set (12 brands; "
            "1 + 4 + 7 per cell) traces the IL-gradient at the operational "
            "layer. Cell A retains 7 of 8 brands (only Memo Paris is "
            "mention-zero); Cell C retains 4 of 8 (the four with cultural-"
            "footprint discourse: Tom Ford, Chanel, Versace, Dior); Cell B "
            "retains 1 of 8 (D.S. & Durga alone surfaces, at 2 mentions of "
            "18). The cell-attrition pattern is the IL-gradient at the "
            "Recall layer — and it is non-monotonic across cells.",

            "Cell B's near-total attrition is the methodologically significant "
            "outcome. The cell's brands have strong Recognition (mean C_P = "
            "5.00, range 3-6, with five brands at C_P ≥ 5/6) but the panel "
            "of LLMs does not surface them when asked to enumerate the "
            "category. This isn't 'the AI doesn't know these brands' — it's "
            "'the AI knows these brands and does not retrieve them.' The "
            "dissociation operates at scale: most of Cell B exhibits the "
            "pattern, not just a single anchor brand.",

            "Cell C's surprising 4 of 8 retention — despite zero Recognition "
            "for 'niche fragrance' — points to a parallel Recall channel "
            "that operates on cultural-footprint terms independent of "
            "category-anchored Recognition. AI systems will include Chanel "
            "in a niche-fragrance list while not actually classifying Chanel "
            "as niche. This sub-threshold channel is registered for follow-up "
            "in v0.19+ as a sensitivity finding; it does not change the "
            "v0.18 verdicts but it does suggest the multi-component construct "
            "may benefit from a third Recall mode (cultural-footprint vs. "
            "category-anchored).",

            "The cell-attrition pattern fed directly into the C3 ranking-"
            "coherence verdict. Phase D ρ measures within-cell rank "
            "correlation between Recognition (C_P) and Recall (mention "
            "count); when one dimension has minimal variance, ρ degenerates. "
            "Cell A's flat Recognition (7 of 8 at C_P = 6/6) collapses the "
            "rank distinction on the x-axis; Cell B's flat Recall "
            "(7 of 8 at zero mentions) collapses it on the y-axis. Only "
            "Cell C exhibits sufficient variance in both dimensions to "
            "produce a meaningful ρ (= 0.615; the only cell clearing the "
            "0.50 floor).",
        ],
    },
    {
        "number": 3,
        "title": "Nine cases of dissociation, concentrated in the highest-IL cell",
        "chart_slot": "f3_dissociation_scatter",
        "paragraphs": [
            "Nine Iwachu-pattern cases (Phase A C_P ≥ 5/6 AND Phase B "
            "mentions ≤ 2/18) on a same-language indie-fragrance substrate. "
            "Before v0.18, the v1.4 multi-component construct rested on a "
            "single empirical anchor — the Iwachu dissociation observed on "
            "the v0.17 Japanese-cell substrate. A single case is insufficient "
            "ground for a canonical construct claim, and the cross-cultural "
            "framing left open the possibility that the dissociation was a "
            "Western-language LLM training-data bias artifact rather than a "
            "substantive mechanism. v0.18 closes that question.",

            "Cell A contributes three cases: Comme des Garçons Parfums "
            "(C_P = 5/6, mentions = 2/18), Memo Paris (6/6, 0/18), and "
            "Etat Libre d'Orange (6/6, 1/18). Cell B contributes six cases: "
            "D.S. & Durga (6/6, 2/18), Boy Smells (5/6, 0/18), Heretic "
            "Parfum (6/6, 0/18), Vyrao (6/6, 0/18), Phlur (5/6, 0/18), and "
            "Snif (5/6, 0/18). Cell C contributes zero cases by design — "
            "the threshold requires C_P ≥ 5/6, which no Cell C brand "
            "achieves (maximum is Tom Ford at 2/6).",

            "The cell-concentration pattern is the methodological headline. "
            "If the dissociation construct were noise-driven or artifact-"
            "driven, the cases would distribute roughly uniformly across "
            "cells. Instead they concentrate where category Identity Load "
            "is highest — 75% of Cell B brands exhibit the pattern. This "
            "is consistent with the moderator hypothesis and with the "
            "substantive theory that AI mediation amplifies retrieval "
            "inequality in identity-bearing categories. The v1.4 construct "
            "moves from 'anchored by one cross-cultural case' to 'anchored "
            "by ten cases across two substrate families, with a substantive "
            "IL-pattern in the second substrate.'",

            "The verdict routes to <b>DISSOCIATION_PARTIAL</b> rather than "
            "DISSOCIATION_GENERALIZED because Cell C contributes zero cases. "
            "This is the asymmetric design of the construct — it captures "
            "Recognition-without-Recall, not Non-Recognition-with-Non-Recall — "
            "and the Cell C zero is therefore a feature of the design, not "
            "a failure of generalization. For AIAS™ 1.0's canonical "
            "methodology layer, v0.18 supplies the empirical anchor v1.4 "
            "requires before the multi-component Recognition × Recall axis "
            "can ship as canonical.",
        ],
    },
]


# ---------------------------------------------------------------------------
# HYPOTHESIS_SCORING — the three orthogonal verdict rows
# ---------------------------------------------------------------------------

HYPOTHESIS_SCORING = {
    "heading": "The three verdicts",
    "intro": (
        "Three orthogonal pre-registered hypotheses; three PARTIAL verdicts. "
        "Read together, they describe a moderator that operates through "
        "layer-specific channels and a multi-component construct that "
        "generalizes with cell-level concentration in the highest-IL tier."
    ),
    "rows": [
        # (h_id, prediction, result, status_text, status_class)
        (
            "H_Regime4",
            "C1 (n ≥ 12) → C2 within-cell (top-2 ≥ 0.50) → C2 IL-gradient "
            "(B − C ≥ 0.10) → C3 (per-cell ρ ≥ 0.50 in ≥ 2 of 3 cells)",
            "C1 ✓ (n = 24); C2 within-cell ✓ (Cells B, C); C2 IL-gradient ✓ "
            "(0.3125); C3 ✗ (only Cell C clears, ρ = 0.615)",
            "PARTIAL",
            "partial",
        ),
        (
            "H_IL_mod",
            "Joint moderator confirmation across v0.16, v0.17, v0.18 legs",
            "v0.16 PARTIAL × v0.17 FALSIFIED × v0.18 PARTIAL → joint PARTIAL "
            "(moderator operates with substrate-specific qualifications)",
            "PARTIAL",
            "partial",
        ),
        (
            "H_dissoc",
            "Iwachu pattern generalizes to same-language substrate "
            "(≥ 1 case per cell ⇒ GENERALIZED; cell-clustered ⇒ PARTIAL)",
            "9 cases in 2 of 3 cells (Cell A: 3; Cell B: 6; Cell C: 0 by "
            "Recognition-floor design)",
            "DISSOCIATION_PARTIAL",
            "partial",
        ),
    ],
}


# ---------------------------------------------------------------------------
# HYPOTHESIS_DETAILS — expanded rationale for each verdict
# ---------------------------------------------------------------------------

HYPOTHESIS_DETAILS = {
    "heading": "Hypothesis details",
    "intro": (
        "The three verdicts in more detail, with the resolution path each "
        "took through the pre-registered decision cascade."
    ),
    "items": [
        (
            "H_Regime4_indie_fragrance",
            "Resolved at C3 (ranking coherence). C1 panel adequacy clears "
            "cleanly (worldwide n = 24, well above the floor of 12). C2 "
            "within-cell clears: Cell B (top-2 = 1.000) and Cell C (top-2 = "
            "0.688) both meet the 0.50 threshold. C2 IL-gradient separation "
            "clears: Cell B 1.000 − Cell C 0.688 = 0.3125, above the 0.10 "
            "floor. C3 ranking coherence fails: only Cell C clears the per-"
            "cell ρ ≥ 0.50 threshold (ρ = 0.615); Cells A and B fail "
            "(ρ = 0.247 and 0.434 respectively). 1 of 3 cells clearing is "
            "below the 2-of-3 requirement. The failure mode is informative — "
            "Cell A's flat Recognition and Cell B's flat Recall both "
            "degenerate the within-cell rank correlation.",
        ),
        (
            "H_IdentityLoad_moderator",
            "Three-leg joint verdict over v0.16 (PARTIAL on kitchen knives, "
            "SSRN 6791999), v0.17 (FALSIFIED on premium kitchenware, SSRN "
            "6802261, with the falsification grounded in panel inadequacy "
            "rather than substantive moderator failure), and v0.18 PARTIAL "
            "(this report). The joint matrix routes to PARTIAL: the moderator "
            "operates with substrate-specific qualifications. The v0.18 leg "
            "exposes that the moderator acts through layer-specific channels — "
            "as a Recognition-floor effect at the medium-IL / medium-high-IL "
            "boundary, and as a dissociation pattern at the high-IL tier. "
            "The moderator is not a single-mechanism construct.",
        ),
        (
            "H_Recognition_Recall_dissociation_generalization",
            "Nine Iwachu-pattern cases identified across 2 of 3 cells "
            "(Cells A and B). The §5.2 verdict matrix routes 'cases present "
            "but cell-clustered (2 of 3)' to DISSOCIATION_PARTIAL. The v1.4 "
            "multi-component construct generalizes from the cross-cultural "
            "Japanese-cell anchor (v0.17 Iwachu) to a same-language "
            "IL-gradient substrate. Cell C contributes zero cases by "
            "construction — the Iwachu-pattern threshold requires "
            "C_P ≥ 5/6, which no Cell C brand achieves. This is the "
            "asymmetric design of the construct (Recognition-without-Recall, "
            "not Non-Recognition-with-Non-Recall), and the Cell C zero is a "
            "feature, not a failure.",
        ),
    ],
}


# ---------------------------------------------------------------------------
# LIMITATIONS
# ---------------------------------------------------------------------------

LIMITATIONS = {
    "heading": "Limitations",
    "paragraphs": [
        "<b>Single-substrate constraint on the generalization claim.</b> "
        "v0.18 generalizes the multi-component construct from one substrate "
        "(v0.17 cross-cultural anchor) to two (v0.17 + v0.18 same-language). "
        "Multi-substrate generalization across the consumer-category spectrum "
        "remains future work. v0.19+ should probe substrates with shifted IL "
        "profiles and category-vocabulary structures.",

        "<b>LLM panel temporal validity.</b> The six-slot reference panel "
        "(claude-opus-4-5, claude-sonnet-4-5, gpt-4o, gpt-4o-mini, "
        "gemini-2.5-flash, gemini-2.5-flash-lite) reflects model versions in "
        "market as of mid-2026. Provider model substitutions over future-"
        "phase horizons are expected and documented in the DEVIATIONS "
        "protocol. v0.18 dissociation cases should be read as the pattern "
        "observed against the locked panel at acquisition, not as permanent "
        "substrate properties.",

        "<b>C2 IL-gradient guard's degenerate case for Cell B.</b> Cell B's "
        "top-2 share = 1.000 emerges from Recall sparseness (D.S. & Durga "
        "alone, with 2 mentions of 18) rather than from a healthy Pareto "
        "distribution. The IL-gradient separation guard clears against a "
        "near-empty Cell B baseline. The substantive interpretation rests "
        "on the §05 dissociation pattern, not on the C2 mention concentration "
        "metric alone.",

        "<b>C3 ranking coherence as a within-cell variance test.</b> Phase D "
        "ρ requires within-cell variance in both Recognition and Recall. "
        "Cell A's flat Recognition (7 of 8 brands at C_P = 6/6) and Cell B's "
        "flat Recall (7 of 8 brands at zero mentions) both degenerate the "
        "rank-correlation signal. Future operationalization may benefit from "
        "supplementary measures that do not require simultaneous variance "
        "in both dimensions.",
    ],
}


# ---------------------------------------------------------------------------
# WHATS_NEXT
# ---------------------------------------------------------------------------

WHATS_NEXT = {
    "heading": "What's next",
    "paragraphs": [
        "Three pre-registerable directions emerge cleanly from the v0.18 "
        "verdicts. None requires retracting v0.18; each addresses a specific "
        "v0.18 finding.",

        "<b>Substrates with greater within-cell Recognition variance.</b> "
        "The C3 failure mode in v0.18 — Cell A's near-saturation and Cell B's "
        "near-zero Recall — both degenerate the within-cell rank correlation. "
        "A substrate where Recognition and Recall both vary meaningfully "
        "within each cell would test C3 cleanly without confounding by "
        "variance collapse.",

        "<b>Finer Identity-Load stratification within the high-IL tier.</b> "
        "v0.18's high-IL cell (indie/artisan) carries 75% of dissociation "
        "cases. A substrate with finer IL stratification within the high-IL "
        "tier would test whether the dissociation × IL relationship operates "
        "monotonically within the tier, or whether it is bounded by an "
        "additional threshold structure.",

        "<b>Cell C internal variance — icon-tier vs. mainstream-tier.</b> "
        "Tom Ford's marginal Recognition (C_P = 2/6 vs. 0 for the rest of "
        "Cell C) and elevated Recall (4 mentions) suggest a sub-threshold "
        "Recognition variance operating within the mass-prestige tier. "
        "v0.19+ could profitably stratify mass-prestige into icon-tier "
        "(Chanel, Dior, Hermès) and mainstream-tier (Marc Jacobs, Calvin "
        "Klein) sub-cells to test whether the cultural-footprint Recall "
        "channel operates uniformly or stratifies further.",

        "Each direction is independently preregisterable and leaves v0.18's "
        "verdicts unchanged. The pre-registration discipline across r1–r4 "
        "of v0.18 — locking panel, hypotheses, thresholds, and verdict "
        "matrices ex-ante before any acquisition; documenting Cell C's "
        "cascade exhaustion as a substantive finding rather than retroactively "
        "substituting alternates — is itself the protocol-level commitment "
        "that distinguishes the AIAS™ program. v0.19 will inherit the same "
        "discipline.",
    ],
}


# ---------------------------------------------------------------------------
# CLOSING
# ---------------------------------------------------------------------------

CLOSING = {
    "byline_long": [
        "Pablo Ulpiano González Castro",
        "School of Visual Arts, MPS Branding Program (primary academic affiliation)",
        "Third System™ — research entity",
        "pablou@pablou.com · pablou.com · ORCID 0009-0003-8968-9990",
    ],
    "datasets": [
        "Pre-registration and DEVIATIONS log: osf.io/ec6wh/v18/PRE_REGISTRATION_v0_18.md "
        "and osf.io/ec6wh/v18/DEVIATIONS.md",
        "Phase A and Phase B acquisition data: osf.io/ec6wh/v18/data/",
        "Scoring code, figures, and verdict outputs: "
        "osf.io/ec6wh/v18/scripts/ and osf.io/ec6wh/v18/data/verdicts/",
    ],
    "methodology_log": "thirdsystem.ai/methodology and osf.io/ec6wh",
}
