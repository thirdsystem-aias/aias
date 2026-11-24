"""
small_print.py - Third System(TM) small-print notes and disclosure callouts (Pablo, Nov 15, 2026, 8:33 am).

The rule (CLAUDE.md): reports and briefs keep the main text light. Source and method notes,
definitions, caveats, sample sizes and model lists move to numbered notes or margin callouts on the
same page; a short Disclosures block (conflicts of interest, held-out brands, AI use, independence)
closes the report in small print, with a one-line pointer in the main text. Scope: new reports only;
published locked reports are unchanged and papers are untouched.

Type scale (brand/report_specs.json section_template.page_templates.small_print; nothing is
hard-coded here):

    note, source_line, note_marker   6.5 - 7 pt    numbered notes and source lines
    margin_callout (+ label)         7.5 pt        callout beside the text
    disclosures (+ head)             7.5 pt        closing Disclosures block
    floor                            6.5 pt        nothing in a report is smaller

Material disclosures stay legible: every style takes the body text colour (soft_black) or a token
whose contrast on the page ground is at least 4.5:1 (WCAG); preflight_styles() computes it.

Pieces
    NoteSeq                numbered notes for ONE page: cite(text) returns the marker to put in the
                           text and records the note, so a note can only land on its own page
    foot_blocks()          draws the page's Disclosures block (last page) and numbered notes at the
                           foot, above the footer rule; returns the lowest y the body may reach
    notes_block(), disclosures_block(), margin_callout()   the single blocks
    disclosure_pointer()   the one-line pointer for the main text
    preflight_styles()     fails on a style under the 6.5 pt floor, outside its band, or under 4.5:1
    check_pdf_min_size()   fails on any text in a rendered PDF under the floor
    check_notes_same_page()  each note's text is on the page of its reference
    check_disclosures()    the Disclosures block is on the last page, with every required item
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Mapping, Sequence

from reportlab.lib.colors import Color
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph

if __package__:
    from . import ts_layout as L
else:
    import ts_layout as L

__all__ = [
    "SmallPrintError", "spec", "style", "contrast_ratio", "NoteSeq", "marker", "notes_block",
    "notes_height", "disclosures_block", "disclosures_height", "foot_blocks", "margin_callout",
    "margin_callout_height", "disclosure_pointer", "preflight_styles", "check_pdf_min_size",
    "check_notes_same_page", "check_disclosures",
]


class SmallPrintError(ValueError):
    """A small-print style, page or PDF that breaks the type scale, the floor or the contrast rule."""


# ---------------------------------------------------------------------------
# Tokens
# ---------------------------------------------------------------------------

def spec(t: L.Tokens) -> dict:
    """report_specs.json section_template.page_templates.small_print."""
    return t.pages["small_print"]


def style(t: L.Tokens, name: str, **kw):
    """The ReportLab paragraph style of one small-print role (note, source_line, margin_callout, ...)."""
    return L._pstyle(t, spec(t)["styles"][name], name=f"sp_{name}", **kw)


def _lum(c: Color) -> float:
    def ch(v: float) -> float:
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * ch(c.red) + 0.7152 * ch(c.green) + 0.0722 * ch(c.blue)


def contrast_ratio(fg: Color, bg: Color) -> float:
    """WCAG 2 contrast ratio of two colours, from 1 to 21."""
    a, b = sorted((_lum(fg), _lum(bg)), reverse=True)
    return (a + 0.05) / (b + 0.05)


def ground(t: L.Tokens) -> Color:
    return t.colour(t.pages["inside_page"]["ground"])


def style_report(t: L.Tokens) -> dict[str, dict]:
    """Per role: size, band, colour name, contrast on the page ground."""
    sp = spec(t)
    bg = ground(t)
    return {n: {"size_pt": float(s["size_pt"]), "band_pt": tuple(s["band_pt"]), "color": s.get("color", "soft_black"),
                "contrast": contrast_ratio(t.colour(s.get("color", "soft_black")), bg)}
            for n, s in sp["styles"].items()}


def preflight_styles(t: L.Tokens) -> dict:
    """Pre-flight: every small-print style is at or above the floor (6.5 pt), inside its band of the
    type scale, and has contrast of at least min_contrast on the page ground. Raises SmallPrintError
    naming each failure; returns the per-style report when all is well."""
    sp = spec(t)
    floor, need = float(sp["floor_pt"]), float(sp["min_contrast"])
    problems = []
    rep = style_report(t)
    for n, r in rep.items():
        lo, hi = r["band_pt"]
        if r["size_pt"] < floor:
            problems.append(f"{n}: {r['size_pt']} pt is under the {floor} pt floor")
        if not lo <= r["size_pt"] <= hi:
            problems.append(f"{n}: {r['size_pt']} pt is outside its band {lo}-{hi} pt")
        if lo < floor:
            problems.append(f"{n}: band starts at {lo} pt, under the {floor} pt floor")
        if r["contrast"] < need:
            problems.append(f"{n}: contrast {r['contrast']:.2f}:1 is under {need}:1 ({r['color']} on the page ground)")
    if problems:
        raise SmallPrintError("; ".join(problems))
    return rep


# ---------------------------------------------------------------------------
# Notes
# ---------------------------------------------------------------------------

def marker(t: L.Tokens, n: int) -> str:
    """Reference mark for the text: a raised numeral at the note-marker size (6.5 pt)."""
    s = spec(t)["styles"]["note_marker"]
    return f'<super rise="3" size="{s["size_pt"]}">{n}</super>'


class NoteSeq:
    """Numbered notes of ONE page. Numbers restart at 1 on every page, so a reference and its note
    are always on the same page: build a NoteSeq per page, put cite(...) in that page's text and
    hand notes to foot_blocks()/notes_block() on the same page.

        ns = NoteSeq(t)
        text = f"Share of answers naming the brand{ns.cite('Source: SAMPLE. n = 000 prompts.')} rose."
    """

    def __init__(self, t: L.Tokens):
        self.t = t
        self.notes: list[str] = []

    def cite(self, text: str) -> str:
        self.notes.append(text)
        return marker(self.t, len(self.notes))


def _note_paras(t: L.Tokens, notes: Sequence[str], source_line: str | None = None) -> list:
    lay = spec(t)["layout"]
    st = style(t, "note", leftIndent=lay["notes_number_width_pt"], bulletIndent=0,
               bulletFontName=L.font_name("Regular"), bulletFontSize=float(spec(t)["styles"]["note"]["size_pt"]),
               spaceAfter=float(spec(t)["styles"]["note"]["space_after_pt"]))
    out = [Paragraph(n, st, bulletText=str(i)) for i, n in enumerate(notes, 1)]
    if source_line:
        out.append(Paragraph(source_line, style(t, "source_line", spaceBefore=2)))
    return out


def _two_col(t: L.Tokens) -> tuple[float, float]:
    gw = float(spec(t)["layout"]["disclosures_gutter_pt"])
    return (t.content_w - gw) / 2, gw


def _cols_height(t: L.Tokens, make, ncol: int) -> float:
    if ncol == 1:
        return L._height(make, t.content_w)
    colw, gw = _two_col(t)
    xs = [t.margin + k * (colw + gw) for k in range(ncol)]
    return L._columns(L._scratch(), make, 100000.0, 0.0, xs, colw, "small print")["height"]


def notes_height(t: L.Tokens, notes: Sequence[str], source_line: str | None = None) -> float:
    """Height of the notes block (rule, gap and two balanced columns of notes)."""
    if not notes and not source_line:
        return 0.0
    lay = spec(t)["layout"]
    return lay["notes_rule_gap_pt"] + _cols_height(t, lambda: _note_paras(t, notes, source_line), 2) + 1


def notes_block(c: Canvas, t: L.Tokens, notes: Sequence[str], bottom: float, source_line: str | None = None) -> dict:
    """Numbered notes (and an optional source line) in two balanced columns, a hairline above, the
    block's lower edge at y=bottom. Returns {'top', 'bottom'} (top is the hairline's y)."""
    if not notes and not source_line:
        return {"top": bottom, "bottom": bottom}
    lay = spec(t)["layout"]
    make = lambda: _note_paras(t, notes, source_line)
    h = _cols_height(t, make, 2)
    colw, gw = _two_col(t)
    top = bottom + h + lay["notes_rule_gap_pt"]
    c.setStrokeColor(t.colour(lay["notes_rule_color"]))
    c.setLineWidth(lay["notes_rule_pt"])
    c.line(t.margin, top, t.page_w - t.margin, top)
    L._columns(c, make, top - lay["notes_rule_gap_pt"], bottom - 1, [t.margin, t.margin + colw + gw], colw, "notes")
    return {"top": top, "bottom": bottom}


# ---------------------------------------------------------------------------
# Disclosures
# ---------------------------------------------------------------------------

def _disc_paras(t: L.Tokens, items: Mapping[str, str], labels: Mapping[str, str] | None) -> list:
    keys = spec(t)["disclosure_items"]
    labels = labels or DEFAULT_LABELS
    st = style(t, "disclosures", spaceAfter=float(spec(t)["styles"]["disclosures"]["space_after_pt"]))
    return [Paragraph(f"<b>{labels[k]}.</b> {items[k]}", st) for k in keys]


DEFAULT_LABELS = {"conflicts_of_interest": "Conflicts of interest", "held_out_brands": "Held-out brands",
                  "ai_use": "Use of AI", "independence": "Independence"}


def _check_items(t: L.Tokens, items: Mapping[str, str]) -> None:
    missing = [k for k in spec(t)["disclosure_items"] if not str(items.get(k) or "").strip()]
    if missing:
        raise SmallPrintError(f"Disclosures block is missing: {', '.join(missing)}")


def disclosures_height(t: L.Tokens, items: Mapping[str, str], labels: Mapping[str, str] | None = None) -> float:
    _check_items(t, items)
    lay = spec(t)["layout"]
    head = float(spec(t)["styles"]["disclosures_head"]["leading_pt"])
    return (lay["notes_rule_gap_pt"] + head + lay["disclosures_head_gap_pt"]
            + _cols_height(t, lambda: _disc_paras(t, items, labels), int(lay["disclosures_columns"])) + 1)


def disclosures_block(c: Canvas, t: L.Tokens, items: Mapping[str, str], bottom: float,
                      labels: Mapping[str, str] | None = None, heading: str = "Disclosures") -> dict:
    """The Disclosures block in small print (7.5 pt): a hairline, the heading, then the four items
    (conflicts of interest, held-out brands, AI use, independence) in two balanced columns, the
    block's lower edge at y=bottom. Raises SmallPrintError if an item is missing."""
    _check_items(t, items)
    lay = spec(t)["layout"]
    ncol = int(lay["disclosures_columns"])
    make = lambda: _disc_paras(t, items, labels)
    h = _cols_height(t, make, ncol)
    headh = float(spec(t)["styles"]["disclosures_head"]["leading_pt"])
    top = bottom + h + lay["disclosures_head_gap_pt"] + headh + lay["notes_rule_gap_pt"]
    c.setStrokeColor(t.colour(lay["notes_rule_color"]))
    c.setLineWidth(lay["notes_rule_pt"])
    c.line(t.margin, top, t.page_w - t.margin, top)
    y = top - lay["notes_rule_gap_pt"]
    L._block(c, lambda: [Paragraph(heading, style(t, "disclosures_head"))], t.margin, y, t.content_w, y - headh - 1,
             "Disclosures heading")
    y -= headh + lay["disclosures_head_gap_pt"]
    colw, gw = _two_col(t)
    L._columns(c, make, y, bottom - 1, [t.margin + k * (colw + gw) for k in range(ncol)], colw, "Disclosures")
    return {"top": top, "bottom": bottom}


def disclosure_pointer(page_no: int | str | None = None) -> str:
    """The one-line pointer in the main text."""
    return "Disclosures, including conflicts of interest, held-out brands, use of AI and independence, are set out on " + (
        f"page {page_no}." if page_no is not None else "the last page.")


def foot_blocks(c: Canvas, t: L.Tokens, *, notes: Sequence[str] = (), source_line: str | None = None,
                disclosures: Mapping[str, str] | None = None, labels: Mapping[str, str] | None = None) -> dict:
    """Foot of the page, above the footer rule: the Disclosures block lowest (last page only), the
    numbered notes above it. Returns {'body_bottom': y, ...}: the body must stop above body_bottom
    (the block gap above the top block is already included)."""
    lay = spec(t)["layout"]
    floor_y = t.pages["footer"]["rule_from_bottom_pt"] + lay["foot_gap_above_footer_pt"]
    y = floor_y
    out = {"notes": None, "disclosures": None}
    if disclosures is not None:
        out["disclosures"] = disclosures_block(c, t, disclosures, y, labels)
        y = out["disclosures"]["top"] + lay["block_gap_pt"]
    if notes or source_line:
        out["notes"] = notes_block(c, t, notes, y, source_line)
        y = out["notes"]["top"] + lay["block_gap_pt"]
    out["body_bottom"] = y
    return out


# ---------------------------------------------------------------------------
# Margin callout
# ---------------------------------------------------------------------------

def _callout_paras(t: L.Tokens, text: str, label: str | None) -> list:
    out = []
    if label:
        out.append(Paragraph(label, style(t, "margin_callout_label",
                                          spaceAfter=float(spec(t)["styles"]["margin_callout_label"]["space_after_pt"]))))
    out.append(Paragraph(text, style(t, "margin_callout")))
    return out


def margin_callout_height(t: L.Tokens, text: str, width: float, label: str | None = None) -> float:
    pad = spec(t)["layout"]["callout_pad_left_pt"]
    return L._height(lambda: _callout_paras(t, text, label), width - pad)


def margin_callout(c: Canvas, t: L.Tokens, text: str, *, top: float, col_from: int, col_to: int,
                   label: str | None = None, bottom_limit: float | None = None) -> dict:
    """A callout beside the main text, in the grid columns col_from..col_to: an Indigo rule on its
    left, an optional bold label and the text at 7.5 pt. Returns {'top','bottom','x','w'}."""
    lay = spec(t)["layout"]
    x, w = t.col_left(col_from), t.span(col_from, col_to)
    pad = lay["callout_pad_left_pt"]
    limit = t.pages["footer"]["rule_from_bottom_pt"] + lay["foot_gap_above_footer_pt"] if bottom_limit is None else bottom_limit
    bottom = L._block(c, lambda: _callout_paras(t, text, label), x + pad, top, w - pad, limit, "margin callout")
    c.setStrokeColor(t.colour(lay["callout_rule_color"]))
    c.setLineWidth(lay["callout_rule_pt"])
    c.line(x, top, x, bottom)
    return {"top": top, "bottom": bottom, "x": x, "w": w}


# ---------------------------------------------------------------------------
# Checks on a rendered PDF
# ---------------------------------------------------------------------------

def _flat(s: str) -> str:
    return re.sub(r"\s+", " ", s or "")


def pdf_text_sizes(pdf_path: Path | str) -> list[list[tuple[str, float]]]:
    """Per page, (text, effective font size in pt) of every text run."""
    from pypdf import PdfReader
    pages = []
    for page in PdfReader(str(pdf_path)).pages:
        runs = []

        def visit(text, cm, tm, font_dict, font_size, runs=runs):
            if not text or not text.strip():
                return
            sx = (tm[0] ** 2 + tm[1] ** 2) ** 0.5 * (cm[0] ** 2 + cm[1] ** 2) ** 0.5
            runs.append((text.strip(), round(font_size * sx, 2)))

        page.extract_text(visitor_text=visit)
        pages.append(runs)
    return pages


def check_pdf_min_size(pdf_path: Path | str, floor: float = 6.5, tol: float = 0.05) -> dict:
    """Pre-flight on a rendered PDF: no text run under the floor (6.5 pt). Raises SmallPrintError
    listing page, size and text of each offender; returns {'smallest': pt, 'runs': n}."""
    pages = pdf_text_sizes(pdf_path)
    bad = [(i, sz, tx) for i, runs in enumerate(pages, 1) for tx, sz in runs if sz < floor - tol]
    if bad:
        raise SmallPrintError("text under the %s pt floor: " % floor + "; ".join(
            f"p{i} {sz} pt {tx[:40]!r}" for i, sz, tx in bad[:10]))
    sizes = [sz for runs in pages for _, sz in runs]
    return {"smallest": min(sizes) if sizes else None, "runs": len(sizes)}


def check_notes_same_page(pdf_path: Path | str, pairs: Sequence[tuple[str, str]]) -> list[int]:
    """pairs = (text of the reference sentence, text of its note). Each pair must be found on ONE
    page together; returns that page (1-based) per pair, raises SmallPrintError otherwise."""
    from pypdf import PdfReader
    texts = [_flat(p.extract_text()) for p in PdfReader(str(pdf_path)).pages]
    found, bad = [], []
    for ref, note in pairs:
        ref_pages = [i for i, tx in enumerate(texts, 1) if _flat(ref) in tx]
        note_pages = [i for i, tx in enumerate(texts, 1) if _flat(note) in tx]
        if not ref_pages or not note_pages or ref_pages[0] != note_pages[0]:
            bad.append(f"{ref[:40]!r}: reference on {ref_pages}, note on {note_pages}")
        else:
            found.append(ref_pages[0])
    if bad:
        raise SmallPrintError("note not on its reference's page: " + "; ".join(bad))
    return found


def check_disclosures(pdf_path: Path | str, t: L.Tokens, heading: str = "Disclosures") -> dict:
    """The Disclosures block is on the LAST page, after the main text, with every item label."""
    from pypdf import PdfReader
    texts = [_flat(p.extract_text()) for p in PdfReader(str(pdf_path)).pages]
    last = texts[-1]
    problems = []
    if heading not in last:
        problems.append("no Disclosures heading on the last page")
    for k in spec(t)["disclosure_items"]:
        if DEFAULT_LABELS[k] not in last:
            problems.append(f"last page lacks {DEFAULT_LABELS[k]!r}")
    if any(heading + " " in tx and DEFAULT_LABELS["ai_use"] in tx for tx in texts[:-1]):
        problems.append("a Disclosures block sits on a page before the last")
    if problems:
        raise SmallPrintError("; ".join(problems))
    return {"page": len(texts)}
