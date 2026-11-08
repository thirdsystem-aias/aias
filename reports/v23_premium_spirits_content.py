"""
AIAS v0.23 — Premium Spirits
Brand-format report content in the schema build_report_v23.py reads.

Rebuilt 2026-11-08. The file previously at this path was a copy of the
v0.22 automotive content (kept as
_superseded_v23_premium_spirits_content_automotive.py), so the May 2026
report carried automotive findings under the spirits file name.

Every finding, number and interpretation below is imported from
v0_23_premium_spirits_content.py (the scored spirits content, 2026-05-26),
not retyped. This module adds only what the brand-format layout needs:
section headings, the cover headline, the hypothesis table's prediction
column (condensed from prereg/v0_23_mega_prompt.md at tag v0.23-prereg-r1),
the dataset list and the methodology log.
"""

import re as _re

import v0_23_premium_spirits_content as _src


def _esc(text):
    """Escape the characters ReportLab's paragraph markup reads as markup."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _paras(text):
    return [_esc(p.strip()) for p in text.split("\n\n") if p.strip()]


def _label_bold(paragraph):
    """Bold a short leading 'Label:' (the What we measured paragraphs)."""
    head, sep, rest = paragraph.partition(": ")
    if sep and len(head) <= 40:
        return f"<b>{head}:</b> {rest}"
    return paragraph


# ---------------------------------------------------------------------------
# COVER
# The headline is the one line written for this module: it states the
# substrate's defining finding (P1, "The recognition ceiling") in the
# sentence form the series' covers use. The deck is the content module's
# own standfirst.
# ---------------------------------------------------------------------------
COVER = {
    "title": "The Recognition Ceiling on the Premium Spirits Substrate",
    "subtitle": _esc(_src.STANDFIRST),
    "date": _src.COVER["date"],
    "byline_short": "Pablo Ulpiano González Castro · Third System",
    "tagline": "Independent measurement for the AI mediation layer.",
}

# ---------------------------------------------------------------------------
# LEAD SPREAD: standfirst = first executive-summary paragraph; lead deck =
# the four lead-deck propositions in the series' "First, ... Second, ..." form.
# ---------------------------------------------------------------------------
_exec = _paras(_src.EXEC_SUMMARY)
STANDFIRST = _exec[0]

_ORDINALS = ("First", "Second", "Third", "Fourth")
_KEEP_CAPITAL = {"Fortaleza"}  # proper nouns that open a proposition


def _lower_first(sentence):
    first_word = sentence.split(" ", 1)[0].rstrip(",")
    if first_word in _KEEP_CAPITAL:
        return sentence
    return sentence[0].lower() + sentence[1:]


assert len(_src.LEAD_DECK) == len(_ORDINALS)
LEAD_DECK = "Four findings shape the v0.23 phase. " + " ".join(
    f"{o}, {_lower_first(_esc(b))}" for o, b in zip(_ORDINALS, _src.LEAD_DECK)
)

EXEC_SUMMARY = _exec[1:]

WHAT_WE_MEASURED = {
    "heading": "What we measured",
    "paragraphs": [_label_bold(p) for p in _paras(_src.WHAT_WE_MEASURED)],
}

# ---------------------------------------------------------------------------
# FINDINGS (P1-P5). Chart slots refer to _slot_lookup in build_report_v23.py:
# f1 composite bar, f2 recall vs slot scatter, f3 channel heatmap,
# f4 ownership box plot. Finding 2 has no chart of its own (its brands are
# the floor of Figure 1).
# ---------------------------------------------------------------------------
_PATTERN_CHART = {
    1: "f1_cp_distribution",
    2: "",
    3: "f2_dissociation_scatter",
    4: "f3_channel_asymmetry",
    5: "f4_phantom_defunct",
}

PATTERNS = []
for _block in _src.PATTERNS.split("\n\n"):
    _head, _body = _block.strip().split("\n", 1)
    _m = _re.match(r"P(\d+)\.\s+(.+)$", _head)
    _n = int(_m.group(1))
    PATTERNS.append({
        "number": _n,
        "title": _esc(_m.group(2)),
        "chart_slot": _PATTERN_CHART[_n],
        "paragraphs": [_esc(" ".join(_body.split("\n")))],
    })
assert [p["number"] for p in PATTERNS] == [1, 2, 3, 4, 5]

LIMITATIONS = {
    "heading": "Limitations",
    "paragraphs": _paras(_src.LIMITATIONS),
}

# The content module's closing paragraph ends the What's next section.
WHATS_NEXT = {
    "heading": "What’s next",
    "paragraphs": _paras(_src.WHATS_NEXT) + _paras(_src.CLOSING),
}

# ---------------------------------------------------------------------------
# HYPOTHESIS SCORING. Prediction column condensed from sections 5
# (hypotheses) and 6 (falsification criteria) of prereg/v0_23_mega_prompt.md
# at tag v0.23-prereg-r1. Result and verdict columns are the content
# module's own.
# ---------------------------------------------------------------------------
_PREDICTION = {
    "H_Regime4": (
        "<b>Standard set.</b> Each of the 24 brands classifies into one of "
        "four Presence regimes (Dominant, Established, Emerging, Absent) on "
        "the composite score. Falsified if any regime is empty."
    ),
    "H_RecognitionPrescreen": (
        "<b>Standard set.</b> The R0 pre-screen gate excludes at most three "
        "brands from the composite denominator. Falsified if more than three "
        "are excluded."
    ),
    "H_Phantom": (
        "<b>Standard set.</b> No phantom brands surface. The registry holds "
        "no defunct brands, so the hypothesis is carried for protocol "
        "completeness, not tested."
    ),
    "H_ILDirect": (
        "<b>Standard set.</b> Information Landscape Direct scores (from "
        "Phase A Recognition richness) correlate positively with Phase B "
        "Recall frequency (r ≥ 0.40, p &lt; .05). Falsified if "
        "r &lt; 0.40 or p ≥ .05."
    ),
    "H_C2_TwoChannel": (
        "<b>Standard set.</b> The editorial-authority and cultural-cult "
        "channels surface partly overlapping, non-identical brand sets: an "
        "overlap coefficient between 0.30 and 0.80. Falsified below 0.30 or "
        "above 0.80."
    ),
    "H_ConglomeratePortfolio": (
        "<b>Substrate-specific.</b> Brands owned by the top-5 global spirits "
        "groups (n = 14) score higher on the composite than independents "
        "(n = 10), by t-test or Mann-Whitney U at the .05 level. Falsified if "
        "p ≥ .05 or the direction reverses."
    ),
}

_STATUS_CLASS = {
    "supported": "confirmed",
    "supported (borderline)": "confirmed",
    "falsified": "disconfirmed",
    "not testable": "descriptive",
}

HYPOTHESIS_SCORING = {
    "heading": "Pre-registered hypothesis scoring",
    "intro": (
        "Six hypotheses were pre-registered at tag v0.23-prereg-r1, before "
        "any acquisition. Falsification criteria were locked in the "
        "pre-registration. The verdicts below are what the data produced "
        "against those criteria."
    ),
    "rows": [
        [h["id"], _PREDICTION[h["id"]], _esc(h["detail"]) + ".",
         h["verdict"].upper(), _STATUS_CLASS[h["verdict"].lower()]]
        for h in _src.HYPOTHESIS_SCORING
    ],
}

HYPOTHESIS_DETAILS = {
    "heading": "Hypothesis interpretation",
    "intro": (
        "Each verdict carries interpretation beyond the pass/fail routing. "
        "The verdicts are what the data produced; what each one means for "
        "the construct is what the prose below addresses."
    ),
    "items": [
        [_hid, f"<b>{_hid}.</b> {_esc(_text)}"]
        for _hid, _text in _src.HYPOTHESIS_DETAILS.items()
    ],
}

# ---------------------------------------------------------------------------
# CLOSING. Byline as on the working paper's title page; datasets as listed in
# osf/v23/README.md (deposit osf.io/ec6wh/v23/); git tags and commits from
# the repository.
# ---------------------------------------------------------------------------
CLOSING = {
    "byline_long": [
        "Pablo Ulpiano González Castro",
        "School of Visual Arts, MPS Branding Program · New York, NY",
        "Third System™ (research entity; data archive and methodology venue)",
        "Correspondence: pablou@pablou.com · ORCID: 0009-0003-8968-9990",
    ],
    "datasets": [
        "v0.23 Phase A acquisition (Recognition, n = 144 probes), raw and "
        "scored: osf.io/ec6wh/v23/data/v23_phase_a_raw.json, "
        "v23_phase_a_scored.json",
        "v0.23 Phase B acquisition (two-channel Recall, n = 36 queries), raw "
        "and scored: osf.io/ec6wh/v23/data/v23_phase_b_raw.json, "
        "v23_phase_b_scored.json",
        "v0.23 scoring verdicts (six hypotheses, 24 brand records): "
        "osf.io/ec6wh/v23/v23_verdicts.json",
        "v0.23 pre-registration (registry, hypotheses, falsification "
        "criteria): osf.io/ec6wh/v23/prereg/",
    ],
    "methodology_log": (
        "v0.23 pre-registration locked at git tag v0.23-prereg-r1 (commit "
        "6b6b047) before acquisition began. Runs under Protocol v1.6 (SSRN "
        "6816340), with v1.5 two-channel Recall (SSRN 6810758) and the v1.2 "
        "four-regime taxonomy (SSRN 6761698). Scoring locked at git tag "
        "v0.23-scoring-locked (commit 28879cd). Academic companion: working "
        "paper, May 2026 (SSRN posting to be confirmed). Corrected 8 November "
        "2026: five brands, not six, received no recall mentions (Jameson "
        "received one); no data, scores, hypotheses or verdicts changed"
    ),
}
