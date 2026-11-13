"""
ts_layout.py - Third System(TM) report design system v2 (approved by Pablo, Nov 11, 2026).

One shared layout module for Third System brand-format reports (managerial register).
Phase builders (build_report_vNN.py) import it, so the design lives in one place:
one unified pipeline, no toggles.

Every colour, size and position comes from the brand files:
  brand/third_system_brand.json  (v1.6+): typography.number_scale, cover_system,
                                   photography, pictograms, palette, footers, grid
  brand/report_specs.json        (v1.2+): section_template.page_templates, word_budget,
                                   running_header
Nothing the brand files hold is hard-coded here (tests/test_ts_layout.py checks that the
module contains no colour literals).

Pages are drawn on a ReportLab canvas, one function per page type:
  cover_c2(), cover_c3()                      covers (Tier 1, Tier 2)
  at_a_glance(), contents_page()              front matter
  finding_page(), finding_evidence_page()     findings (Tier 1 adds the evidence page)
  section_opener()                            full-Indigo opener (Tier 1 only)
  text_page()                                 intro, limitations, closing
  closing_page()                              Tier 1 closing page: statement, colophon, Indigo band
Shared pieces: lockup(), wordmark(), number_row(), icon(), running_chrome().

Report code (decision 14, Pablo, Nov 13, 2026; reports/report_code.py): the Tier 1 closing band
carries the code after the website; on Tiers 2 and 3 the last page passes code= to its page
function and the footer line reads "thirdsystem.ai · TS-CS-v0.22-r1". The website is always
printed in lower case, caps lines included (report_code.upper_keep_website()).

Charts keep the program's two-pass pattern. A page reserves each chart's exact footprint
from the chart PDF's mediabox before any text is placed (the ChartReservation pre-compute)
and records a ChartSlot; overlay_charts() then merges the unchanged chart PDFs onto the
base PDF (pass 2).

Icons: the pictogram set is a draft that Pablo has not marked up. icon() draws nothing
for an icon that is not listed in pictograms.approved (currently empty).

Word budgets: word_budget() and check_page_budget() apply report_specs.word_budget
(600 words per full text page minus each element's deduction).
"""

from __future__ import annotations

import io
import json
import os
import re
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterable, Sequence

from reportlab.lib.colors import Color, HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Frame, Paragraph, Table, TableStyle

if __package__:
    from . import report_code as RC
else:
    import report_code as RC

__all__ = [
    "Tokens", "LayoutOverflow", "ChartSlot",
    "register_fonts", "font_name",
    "lockup", "wordmark", "icon", "number_row", "running_chrome", "last_page_footer",
    "cover_c2", "cover_c3", "at_a_glance", "contents_page", "finding_page",
    "finding_evidence_page", "section_opener", "text_page", "closing_page", "colophon_paragraphs",
    "table_flowable", "reserve_chart", "overlay_charts", "treated_photo",
    "count_words", "word_budget", "check_page_budget",
]


class LayoutOverflow(Exception):
    """Raised when copy does not fit its template slot. The fix is to cut copy or move it,
    never to let it spill or shrink silently."""


# ---------------------------------------------------------------------------
# Tokens: everything read from the brand files
# ---------------------------------------------------------------------------

def _default_root() -> Path:
    env = os.environ.get("AIAS_ROOT")
    return Path(env).resolve() if env else Path(__file__).resolve().parent.parent


class Tokens:
    """Design tokens from brand/third_system_brand.json and brand/report_specs.json."""

    def __init__(self, root: Path | str | None = None):
        self.root = Path(root).resolve() if root else _default_root()
        with open(self.root / "brand" / "third_system_brand.json", encoding="utf-8") as f:
            self.brand = json.load(f)
        with open(self.root / "brand" / "report_specs.json", encoding="utf-8") as f:
            self.specs = json.load(f)
        bv = float(self.brand["_meta"]["schema_version"])
        sv = float(self.specs["_meta"]["schema_version"])
        if bv < 1.6 or sv < 1.2:
            raise RuntimeError(f"ts_layout needs brand >= 1.6 and report_specs >= 1.2 (got {bv}, {sv})")
        geo = self.brand["chart_construction_rules"]["chart_sizing_specifications"]["page_geometry_reference"]
        self.margin = float(geo["margins_pt"])
        self.content_w = float(geo["content_width_pt"])
        self.content_h = float(geo["content_height_pt"])
        self.page_w = self.content_w + 2 * self.margin
        self.page_h = self.content_h + 2 * self.margin
        self.columns = int(geo["columns"])
        self.gutter = float(geo["gutter_pt"])
        self.col_w = (self.content_w - (self.columns - 1) * self.gutter) / self.columns
        self.scale = self.brand["typography"]["number_scale"]
        self.covers = self.brand["cover_system"]
        self.photography = self.brand["photography"]
        self.pictograms = self.brand["pictograms"]
        self.tiers = self.brand["publication_tiers"]
        self.pages = self.specs["section_template"]["page_templates"]
        self.budget = self.specs["word_budget"]
        # the website, always printed in lower case (decision 14, Nov 13, 2026)
        self.website = self.brand["company"]["contact"]["web"].lower()
        self.footer_text = RC.website_lower(self.brand["footers"]["public_report"], self.website)
        self.catalogue = RC.catalogue(self.specs)

    # -- colours -------------------------------------------------------------
    def colour(self, name: str) -> Color:
        """Resolve a colour name (typography.number_scale.colour_refs) or a hex token."""
        if name.startswith("#"):
            return HexColor(name)
        ref = self.scale["colour_refs"][name]
        if ref.startswith("#"):
            return HexColor(ref)
        node = self.brand
        for part in ref.split("."):
            node = node[part]
        return HexColor(node)

    # -- grid ----------------------------------------------------------------
    def col_left(self, i: int) -> float:
        """Left edge of column i (1-based)."""
        return self.margin + (i - 1) * (self.col_w + self.gutter)

    def col_right(self, i: int) -> float:
        """Right edge of column i (1-based)."""
        return self.col_left(i) + self.col_w

    def span(self, a: int, b: int) -> float:
        """Width from the left edge of column a to the right edge of column b."""
        return self.col_right(b) - self.col_left(a)

    def y(self, from_top: float) -> float:
        """ReportLab y for a distance measured from the top edge."""
        return self.page_h - from_top

    # -- type ----------------------------------------------------------------
    def style(self, key: str, variant: str | None = None) -> dict:
        """A type spec from typography.number_scale, merged with a cover variant (C2/C3)."""
        spec = dict(self.scale[key])
        if variant:
            spec.update(spec.pop(variant))
        for k in [k for k, v in spec.items() if isinstance(v, dict)]:
            spec.pop(k)
        return spec


# ---------------------------------------------------------------------------
# Fonts: Akkurat Pro only
# ---------------------------------------------------------------------------

_FONT_FILES = {
    "Light": "AkkuratPro-Light.ttf",
    "Regular": "AkkuratPro-Regular.ttf",
    "Bold": "AkkuratPro-Bold.ttf",
    "Italic": "AkkuratPro-Italic.ttf",
    "BoldItalic": "AkkuratPro-BoldItalic.ttf",
}
_FONT_DIRS = [
    Path.home() / "Library" / "Fonts",
    Path.home() / ".fonts" / "Akkurat",
    Path.home() / ".cache" / "third_system_reports" / "fonts",
]
_REGISTERED: dict[str, str] = {}


def font_name(weight: str) -> str:
    return f"TSAkkuratPro-{weight}"


def register_fonts() -> dict[str, str]:
    """Register Akkurat Pro (Light, Regular, Bold, Italic, Bold Italic). No fallback face."""
    if _REGISTERED:
        return _REGISTERED
    for weight, fname in _FONT_FILES.items():
        path = next((d / fname for d in _FONT_DIRS if (d / fname).is_file()), None)
        if path is None:
            raise FileNotFoundError(f"Akkurat Pro {weight} ({fname}) not found in {_FONT_DIRS}")
        pdfmetrics.registerFont(TTFont(font_name(weight), str(path)))
        _REGISTERED[weight] = str(path)
    for base in ("Light", "Regular"):
        pdfmetrics.registerFontFamily(font_name(base), normal=font_name(base), bold=font_name("Bold"),
                                      italic=font_name("Italic"), boldItalic=font_name("BoldItalic"))
    pdfmetrics.registerFontFamily(font_name("Bold"), normal=font_name("Bold"), bold=font_name("Bold"),
                                  italic=font_name("BoldItalic"), boldItalic=font_name("BoldItalic"))
    return _REGISTERED


def _pstyle(t: Tokens, spec: dict, name: str = "ts", **kw) -> ParagraphStyle:
    size = float(spec["size_pt"])
    return ParagraphStyle(
        name,
        fontName=font_name(spec.get("weight", "Regular")),
        fontSize=size,
        leading=float(spec.get("leading_pt", size * 1.2)),
        textColor=t.colour(spec.get("color", "soft_black")),
        allowWidows=0,
        allowOrphans=0,
        splitLongWords=0,
        **kw,
    )


def _para(t: Tokens, text: str, spec: dict, **kw) -> Paragraph:
    if spec.get("case") == "upper":
        text = RC.upper_keep_website(text, t.website)
    return Paragraph(text, _pstyle(t, spec, **kw))


def _caps(c: Canvas, t: Tokens, x: float, y: float, text: str, spec: dict,
          align: str = "left", colour: str | None = None, case: str | None = None) -> float:
    """Draw one line of tracked caps; returns its width. The website stays lower case.
    case='as_is' keeps the text as given (a report code prints exactly as registered)."""
    size = float(spec["size_pt"])
    fnt = font_name(spec.get("weight", "Regular"))
    if (case or spec.get("case", "upper")) == "upper":
        text = RC.upper_keep_website(text, t.website)
    cs = size * float(spec.get("tracking_em", 0))
    w = pdfmetrics.stringWidth(text, fnt, size) + cs * max(len(text) - 1, 0)
    if align == "right":
        x -= w
    # Character spacing (Tc) is graphics state in PDF and would leak into every later
    # string on the page; save and restore around the tracked line.
    c.saveState()
    obj = c.beginText(x, y)
    obj.setFont(fnt, size)
    obj.setCharSpace(cs)
    obj.setFillColor(t.colour(colour or spec.get("color", "soft_black")))
    obj.textLine(text)
    c.drawText(obj)
    c.restoreState()
    return w


# ---------------------------------------------------------------------------
# Flowing text into frames (manual split, widows and orphans controlled)
# ---------------------------------------------------------------------------

def _scratch() -> Canvas:
    return Canvas(io.BytesIO())


def _flow(c: Canvas, flowables: list, frames: Sequence[tuple[float, float, float, float]]) -> tuple[list, list[float]]:
    """Lay flowables into frames (x, y_bottom, w, h) in order, splitting paragraphs at frame
    ends. Returns (leftover flowables, used height per frame)."""
    queue = list(flowables)
    used = []
    for (x, yb, w, h) in frames:
        fr = Frame(x, yb, w, h, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        while queue:
            fl = queue[0]
            if fr.add(fl, c, trySplit=1):
                queue.pop(0)
                continue
            parts = fr.split(fl, c)
            if parts and len(parts) > 1 and fr.add(parts[0], c, trySplit=1):
                queue[0:1] = list(parts[1:])
            break
        used.append((yb + h) - fr._y)
    return queue, used


def _height(make: Callable[[], list], w: float) -> float:
    """Height of a flowable list at width w (single column, unbounded)."""
    left, used = _flow(_scratch(), make(), [(0, 0, w, 100000)])
    assert not left
    return used[0]


def _columns(c: Canvas, make: Callable[[], list], top: float, bottom: float,
             xs: Sequence[float], w: float, what: str) -> dict:
    """Balanced columns of equal width from y=top down to at most y=bottom."""
    avail = top - bottom
    n = len(xs)

    def fits(h: float) -> bool:
        left, _ = _flow(_scratch(), make(), [(x, top - h, w, h) for x in xs])
        return not left

    if not fits(avail):
        total = _height(make, w)
        raise LayoutOverflow(f"{what}: text needs about {total / n:.0f} pt per column, {avail:.0f} pt available")
    lo, hi = 0.0, avail
    for _ in range(18):
        mid = (lo + hi) / 2
        if fits(mid):
            hi = mid
        else:
            lo = mid
    h = hi + 0.5
    left, used = _flow(c, make(), [(x, top - h, w, h) for x in xs])
    assert not left
    return {"top": top, "bottom": top - max(used), "height": max(used), "columns": [(x, w) for x in xs]}


def _last_line_words(p: Paragraph, w: float) -> tuple[int, int]:
    """(lines, words on the last line) of a paragraph wrapped at width w."""
    p.wrap(w, 100000)
    bl = p.blPara
    if not bl.lines:
        return 0, 0
    ln = bl.lines[-1]
    if bl.kind == 0:
        return len(bl.lines), len(ln[1])
    text = "".join(getattr(f, "text", "") for f in getattr(ln, "words", []))
    return len(bl.lines), len(text.split())


def _runt_free_width(make: Callable[[], list], w: float, min_ratio: float = 0.7) -> float:
    """Large type never ends on a one-word line: narrow the measure (never widen it) until
    the last line carries at least two words, keeping the line count where possible."""
    fl = make()
    if len(fl) != 1 or not isinstance(fl[0], Paragraph):
        return w
    lines, last = _last_line_words(fl[0], w)
    if lines < 2 or last >= 2:
        return w
    best = None
    k = w
    while k >= w * min_ratio:
        k -= 2
        n, lw = _last_line_words(make()[0], k)
        if lw >= 2:
            if n == lines:
                return k
            best = best or k
    return best or w


def _block(c: Canvas, make: Callable[[], list], x: float, top: float, w: float,
           bottom_limit: float, what: str, runt: bool = False) -> float:
    """One column of flowables from y=top; returns the y of its bottom edge.
    runt=True applies the no-one-word-last-line rule for large type."""
    if runt:
        w = _runt_free_width(make, w)
    h = _height(make, w)
    if top - h < bottom_limit - 0.01:
        raise LayoutOverflow(f"{what}: needs {h:.0f} pt, {top - bottom_limit:.0f} pt available")
    left, _ = _flow(c, make(), [(x, top - h - 1, w, h + 1)])
    assert not left
    return top - h


# ---------------------------------------------------------------------------
# Photographs: greyscale, contrast 1.08, no tint, cropped to the frame
# ---------------------------------------------------------------------------

def pool_photo(t: Tokens, photo_id: str, cover: str | None = None) -> Path:
    """Path of a pool photo's original, by pool id (A01, A02 ...), for a print cover. Refuses ids
    not in the print pool (web-only photos included) and photos restricted to other covers."""
    entry = next((p for p in t.photography["pool"] if p["id"] == photo_id), None)
    if entry is None:
        if any(p["id"] == photo_id for p in t.photography.get("web_only", [])):
            raise ValueError(f"{photo_id} is web only (too small to print)")
        raise ValueError(f"{photo_id} is not in the licensed photo pool")
    if cover and entry.get("covers") and cover not in entry["covers"]:
        raise ValueError(f"{photo_id} is for {', '.join(entry['covers'])} covers only, not {cover}")
    rel = t.photography["originals_dir"]
    bases = [Path(os.environ["TS_PHOTO_DIR"])] if os.environ.get("TS_PHOTO_DIR") else []
    bases += [t.root / rel, Path.home() / "aias" / rel]
    for base in bases:
        if (base / entry["file"]).is_file():
            return base / entry["file"]
    raise FileNotFoundError(f"{entry['file']} not found in {[str(b) for b in bases]}")


def photo_in_use(t: Tokens, photo_id: str, exclude_report: str | None = None) -> list[dict]:
    """Usage-record entries for a photo (other than `exclude_report`)."""
    return [u for u in t.photography.get("usage_record", [])
            if u["photo"] == photo_id and u["report"] != exclude_report]


def treated_photo(t: Tokens, path: Path | str, w_pt: float, h_pt: float, dpi: int = 300) -> str:
    """Apply the photography treatment and crop to the frame's aspect ratio (centred).
    Returns the path of a temporary JPEG sized for `dpi` at the frame size."""
    from PIL import Image, ImageEnhance, ImageOps
    tr = t.photography["treatment"]
    if tr.get("tint"):
        raise ValueError("photo tints are not allowed")
    with Image.open(path) as src:
        im = ImageOps.exif_transpose(src)
        im.load()
    if tr.get("greyscale", True):
        im = ImageOps.grayscale(im)
    ar = w_pt / h_pt
    iw, ih = im.size
    if iw / ih > ar:
        nw = int(round(ih * ar))
        x0 = (iw - nw) // 2
        im = im.crop((x0, 0, x0 + nw, ih))
    else:
        nh = int(round(iw / ar))
        y0 = (ih - nh) // 2
        im = im.crop((0, y0, iw, y0 + nh))
    im = ImageEnhance.Contrast(im).enhance(float(tr["contrast"]))
    target = (int(round(w_pt / 72 * dpi)), int(round(h_pt / 72 * dpi)))
    if im.size[0] > target[0]:
        im = im.resize(target, Image.LANCZOS)
    fd, out = tempfile.mkstemp(suffix=".jpg", prefix="ts_photo_")
    os.close(fd)
    im.save(out, "JPEG", quality=90)
    return out


# ---------------------------------------------------------------------------
# Lockup, wordmark, icons
# ---------------------------------------------------------------------------

def lockup(c: Canvas, t: Tokens, x: float | None = None, baseline_from_top: float | None = None,
           dark: bool = False, scale: float = 1.0) -> dict:
    """Product lockup: 'Third System' (Akkurat Bold) over 'AI Presence Index' (Akkurat Regular).
    Indigo over Soft Black on paper; white over Lavender Grey on dark grounds."""
    lk = t.covers["lockup"]
    l1, l2 = lk["line1"], lk["line2"]
    cols = lk["on_dark" if dark else "on_light"]
    x = lk["x_pt"] if x is None else x
    b1 = t.y(l1["baseline_from_top_pt"] if baseline_from_top is None else baseline_from_top)
    s1, s2 = l1["size_pt"] * scale, l2["size_pt"] * scale
    b2 = b1 - l2["baseline_gap_pt"] * scale
    c.setFillColor(t.colour(cols["line1"]))
    c.setFont(font_name(l1["weight"]), s1)
    c.drawString(x, b1, l1["text"])
    c.setFillColor(t.colour(cols["line2"]))
    c.setFont(font_name(l2["weight"]), s2)
    c.drawString(x, b2, l2["text"])
    w = max(pdfmetrics.stringWidth(l1["text"], font_name(l1["weight"]), s1),
            pdfmetrics.stringWidth(l2["text"], font_name(l2["weight"]), s2))
    asc = pdfmetrics.getAscent(font_name(l1["weight"]), s1)
    desc = -pdfmetrics.getDescent(font_name(l2["weight"]), s2)
    return {"x": x, "top": b1 + asc, "bottom": b2 - desc, "width": w,
            "line1": {"text": l1["text"], "font": font_name(l1["weight"]), "colour": cols["line1"]},
            "line2": {"text": l2["text"], "font": font_name(l2["weight"]), "colour": cols["line2"]}}


def wordmark(c: Canvas, t: Tokens, x: float, baseline: float, size: float, dark: bool = False) -> float:
    """'Third System' wordmark, Akkurat Bold, Indigo (white on dark grounds). Returns its width."""
    l1 = t.covers["lockup"]["line1"]
    c.setFillColor(t.colour(t.covers["lockup"]["on_dark" if dark else "on_light"]["line1"]))
    c.setFont(font_name(l1["weight"]), size)
    c.drawString(x, baseline, l1["text"])
    return pdfmetrics.stringWidth(l1["text"], font_name(l1["weight"]), size)


def _icon_paths(c: Canvas, name: str, colour: Color, accent: Color):
    """Draft drawings on the 64-unit grid (y down), from the Nov 11 draft set."""
    def L(*pts, close=False):
        p = c.beginPath()
        p.moveTo(*pts[0])
        for q in pts[1:]:
            p.lineTo(*q)
        if close:
            p.close()
        c.drawPath(p, stroke=1, fill=0)

    def R(x0, y0, w, h, fill=False):
        if fill:
            c.setFillColor(accent)
        c.rect(x0, y0, w, h, stroke=0 if fill else 1, fill=1 if fill else 0)

    if name == "question":
        L((8, 10), (56, 10), (56, 44), (30, 44), (18, 56), (18, 44), (8, 44), close=True)
        c.saveState(); c.scale(1, -1); c.setFillColor(colour); c.setFont(font_name("Bold"), 26)
        c.drawCentredString(32, -35, "?"); c.restoreState()
    elif name == "ai_model":
        L((8, 8), (56, 8), (56, 42), (30, 42), (18, 54), (18, 42), (8, 42), close=True)
        L((18, 20), (46, 20)); L((18, 30), (38, 30))
    elif name == "web_search":
        c.circle(26, 26, 15, stroke=1, fill=0); L((37, 37), (56, 56))
    elif name == "answer":
        L((14, 6), (40, 6), (50, 16), (50, 58), (14, 58), close=True); L((40, 6), (40, 16), (50, 16))
        L((22, 28), (42, 28)); L((22, 38), (42, 38)); L((22, 48), (34, 48))
    elif name == "coding":
        for yy in (14, 30, 46):
            L((28, yy), (56, yy))
        L((8, 14), (13, 19), (21, 9)); L((8, 30), (13, 35), (21, 25)); R(9, 41, 10, 10)
    elif name == "score":
        L((8, 56), (56, 56)); R(12, 36, 8, 20, True); R(28, 24, 8, 32, True); R(44, 12, 8, 44, True)
    elif name == "presence":
        for i in range(3):
            for j in range(3):
                if i == 1 and j == 1:
                    R(25, 25, 14, 14, True)
                else:
                    R(9 + i * 18, 9 + j * 18, 10, 10)
    elif name == "consistency":
        for yy in (16, 32, 48):
            L((8, yy), (56, yy)); R(32, yy - 6, 12, 12, True)
    elif name == "category":
        R(8, 8, 48, 48); L((8, 24), (56, 24)); L((8, 40), (56, 40))
        for (a, b) in ((14, 13), (26, 13), (14, 29), (26, 29), (38, 29), (14, 45)):
            R(a, b, 8, 8)
    elif name == "brand":
        L((8, 8), (34, 8), (56, 30), (30, 56), (8, 34), close=True); c.circle(20, 20, 4, stroke=1, fill=0)
    elif name == "pre_registered":
        R(12, 28, 40, 28)
        p = c.beginPath(); p.moveTo(20, 28); p.lineTo(20, 20); p.arcTo(20, 4, 44, 36, 180, 180)
        p.lineTo(44, 28); c.drawPath(p, stroke=1, fill=0); L((32, 38), (32, 46))
    elif name == "waves":
        L((8, 32), (56, 32))
        c.setFillColor(colour); c.rect(8, 27, 10, 10, stroke=0, fill=1); c.rect(27, 27, 10, 10, stroke=0, fill=1)
        c.setFillColor(accent); c.rect(46, 27, 10, 10, stroke=0, fill=1)
    else:
        raise KeyError(name)


def icon(c: Canvas, t: Tokens, name: str, x: float, y: float, size: float | None = None) -> bool:
    """Draw pictogram `name` with its lower-left corner at (x, y). Draws nothing and returns
    False unless Pablo has approved the icon (pictograms.approved)."""
    pg = t.pictograms
    if name not in pg["set"]:
        raise KeyError(f"unknown pictogram {name!r}")
    if name not in pg.get("approved", []):
        return False
    grid = pg["grid"]
    size = size or float(pg["size_pt"][0])
    k = size / float(grid["units"])
    c.saveState()
    c.translate(x, y + size)
    c.scale(k, -k)
    c.setStrokeColor(t.colour(pg["colour"]["stroke"]))
    c.setFillColor(t.colour(pg["colour"]["stroke"]))
    c.setLineWidth(float(grid["stroke_units"]))
    c.setLineJoin(0 if grid["join"] == "miter" else 1)
    c.setLineCap(0 if grid["cap"] == "butt" else 1)
    _icon_paths(c, name, t.colour(pg["colour"]["stroke"]), t.colour(pg["colour"]["accent"]))
    c.restoreState()
    return True


def any_icon_approved(t: Tokens, names: Iterable[str | None]) -> bool:
    return any(n and n in t.pictograms.get("approved", []) for n in names)


# ---------------------------------------------------------------------------
# Page chrome: running header and footer
# ---------------------------------------------------------------------------

def _paper(c: Canvas, t: Tokens, ground: str | None = None) -> None:
    c.setFillColor(t.colour(ground or t.pages["inside_page"]["ground"]))
    c.rect(0, 0, t.page_w, t.page_h, stroke=0, fill=1)


def last_page_footer(t: Tokens, code: str) -> str:
    """Tier 2/3 last-page footer line (decision 14): 'thirdsystem.ai · TS-CS-v0.22-r1'."""
    RC.parse_code(code)
    return t.pages["footer"]["last_page_text"].format(website=t.website, code=code)


def running_chrome(c: Canvas, t: Tokens, label: str, page_no: int | None, code: str | None = None) -> dict:
    """Page ground, running header (wordmark left, label right in caps) and the locked footer.
    code= marks a Tier 2/3 report's last page: the footer line then reads
    'thirdsystem.ai · CODE' (decision 14) in place of the standard footer text."""
    _paper(c, t)
    rh = t.pages["running_header"]
    st = t.scale["running_header"]
    base = t.y(rh["baseline_from_top_pt"])
    wordmark(c, t, rh["x_pt"], base, st["wordmark"]["size_pt"])
    _caps(c, t, t.page_w - t.margin, base, label, st["label"], align="right")
    ft = t.pages["footer"]
    c.setStrokeColor(t.colour(ft["rule_color"]))
    c.setLineWidth(ft["rule_stroke_pt"])
    c.line(t.margin, ft["rule_from_bottom_pt"], t.page_w - t.margin, ft["rule_from_bottom_pt"])
    text = t.footer_text if code is None else last_page_footer(t, code)
    fnt = font_name("Regular")
    c.setFont(fnt, ft["size_pt"])
    c.setFillColor(t.colour(ft["color"]))
    c.drawString(t.margin, ft["baseline_from_bottom_pt"], text)
    if page_no is not None:
        c.drawRightString(t.page_w - t.margin, ft["baseline_from_bottom_pt"], str(page_no))
    fw = pdfmetrics.stringWidth(text, fnt, ft["size_pt"])
    if fw > t.content_w - 24:
        raise LayoutOverflow("footer text is wider than the content width")
    return {"header_baseline": base, "footer_rule": ft["rule_from_bottom_pt"],
            "content_bottom": ft["rule_from_bottom_pt"] + 12}


# ---------------------------------------------------------------------------
# Covers
# ---------------------------------------------------------------------------

def cover_c2(c: Canvas, t: Tokens, *, photo_path: Path | str, kicker: str, title: str,
             deck: str, byline: str) -> dict:
    """Tier 1 cover: lockup on paper, full-width photo, Indigo title block on columns 1-5
    crossing the photo's bottom edge, deck on paper, byline in caps at the foot."""
    cv = t.covers["C2"]
    _paper(c, t, cv["ground"])
    ph = cv["photo"]
    photo_top = t.y(ph["top_from_top_pt"])
    photo_bottom = t.y(t.page_h * float(ph["bottom_from_top_ratio"]))
    photo_w = t.page_w
    img = treated_photo(t, photo_path, photo_w, photo_top - photo_bottom)
    c.drawImage(img, ph["x_pt"], photo_bottom, photo_w, photo_top - photo_bottom)
    os.unlink(img)
    lk = lockup(c, t)
    tb = cv["title_block"]
    bx0 = float(tb["x_pt"])
    bx1 = t.col_right(tb["columns"][1])
    bh = float(tb["height_pt"])
    bbot = photo_bottom - float(tb["hang_below_photo_pt"])
    btop = bbot + bh
    c.setFillColor(t.colour(tb["fill"]))
    c.rect(bx0, bbot, bx1 - bx0, bh, stroke=0, fill=1)
    kspec = t.style("cover_kicker", "C2")
    kbase = btop - float(tb["kicker_baseline_below_block_top_pt"])
    _caps(c, t, tb["text_x_pt"], kbase, kicker, kspec)
    tspec = t.style("cover_title", "C2")
    tw = bx1 - tb["text_x_pt"] - tb["text_right_padding_pt"]
    ttop = kbase - 2 * kspec["size_pt"]
    tbottom_limit = bbot + tb["title_bottom_padding_pt"]
    tbot = _block(c, lambda: [_para(t, title, tspec)], tb["text_x_pt"], ttop, tw, tbottom_limit, "C2 title", runt=True)
    dk = cv["deck"]
    dspec = t.style("cover_deck")
    by = cv["byline"]
    bspec = t.style("cover_byline")
    dtop = bbot - dk["top_gap_below_block_pt"]
    dx = t.col_left(dk["columns"][0])
    dw = t.span(*dk["columns"])
    dbot = _block(c, lambda: [_para(t, deck, dspec)], dx, dtop, dw,
                  by["baseline_from_bottom_pt"] + 3 * bspec["size_pt"], "C2 deck")
    _caps(c, t, t.margin, by["baseline_from_bottom_pt"], byline, bspec)
    return {
        "page": (t.page_w, t.page_h),
        "photo": {"x": ph["x_pt"], "w": photo_w, "top_from_top": t.page_h - photo_top,
                  "bottom_from_top": t.page_h - photo_bottom, "h": photo_top - photo_bottom},
        "block": {"x0": bx0, "x1": bx1, "h": bh, "top_from_top": t.page_h - btop,
                  "bottom_from_top": t.page_h - bbot,
                  "over_photo": min(btop, photo_top) - max(bbot, photo_bottom),
                  "below_photo": photo_bottom - bbot},
        "lockup": lk,
        "title": {"top": ttop, "bottom": tbot, "x": tb["text_x_pt"], "w": tw},
        "deck": {"top": dtop, "bottom": dbot, "x": dx, "w": dw},
        "byline_baseline": by["baseline_from_bottom_pt"],
    }


def cover_c3(c: Canvas, t: Tokens, *, photo_path: Path | str, kicker: str, title: str,
             deck: str, byline: str) -> dict:
    """Tier 2 cover: lockup, photo framed inside the margins (540 x 330 pt), then kicker,
    title, a 60 pt Indigo rule, the deck and the byline."""
    cv = t.covers["C3"]
    _paper(c, t, cv["ground"])
    lk = lockup(c, t)
    ph = cv["photo"]
    ptop = t.y(ph["top_from_top_pt"])
    pw, phh = float(ph["width_pt"]), float(ph["height_pt"])
    pbot = ptop - phh
    img = treated_photo(t, photo_path, pw, phh)
    c.drawImage(img, ph["x_pt"], pbot, pw, phh)
    os.unlink(img)
    kspec = t.style("cover_kicker", "C3")
    kbase = pbot - cv["kicker"]["baseline_below_photo_pt"]
    _caps(c, t, t.margin, kbase, kicker, kspec)
    tspec = t.style("cover_title", "C3")
    ttop = pbot - cv["title"]["top_below_photo_pt"]
    by = cv["byline"]
    bspec = t.style("cover_byline")
    tbot = _block(c, lambda: [_para(t, title, tspec)], t.margin, ttop, cv["title"]["width_pt"],
                  by["baseline_from_bottom_pt"] + 120, "C3 title", runt=True)
    rl = cv["rule"]
    ry = tbot - rl["gap_below_title_pt"]
    c.setStrokeColor(t.colour(rl["color"]))
    c.setLineWidth(rl["stroke_pt"])
    c.line(t.margin, ry, t.margin + rl["width_pt"], ry)
    dk = cv["deck"]
    dspec = t.style("cover_deck")
    dtop = ry - dk["top_gap_below_rule_pt"]
    dx = t.col_left(dk["columns"][0])
    dw = t.span(*dk["columns"])
    dbot = _block(c, lambda: [_para(t, deck, dspec)], dx, dtop, dw,
                  by["baseline_from_bottom_pt"] + 3 * bspec["size_pt"], "C3 deck")
    _caps(c, t, t.margin, by["baseline_from_bottom_pt"], byline, bspec)
    return {
        "page": (t.page_w, t.page_h),
        "photo": {"x": ph["x_pt"], "w": pw, "h": phh, "top_from_top": t.page_h - ptop,
                  "bottom_from_top": t.page_h - pbot},
        "lockup": lk,
        "kicker_baseline": kbase,
        "title": {"top": ttop, "bottom": tbot},
        "rule": {"y": ry, "w": rl["width_pt"]},
        "deck": {"top": dtop, "bottom": dbot, "x": dx, "w": dw},
        "byline_baseline": by["baseline_from_bottom_pt"],
    }


# ---------------------------------------------------------------------------
# Charts: ChartReservation pre-compute (pass 1) and overlay (pass 2)
# ---------------------------------------------------------------------------

@dataclass
class ChartSlot:
    page_index: int
    chart_path: Path
    x: float
    y: float
    w: float
    h: float
    scale: float


def reserve_chart(chart_path: Path | str, max_w: float) -> tuple[float, float, float]:
    """Pre-compute a chart's real footprint from its PDF mediabox: (w, h, scale).
    Charts are never enlarged; wider charts are scaled down to max_w, aspect kept."""
    from pypdf import PdfReader
    mb = PdfReader(str(chart_path)).pages[0].mediabox
    cw, ch = float(mb.width), float(mb.height)
    s = min(1.0, max_w / cw)
    return cw * s, ch * s, s


def overlay_charts(base_pdf: Path | str, slots: Sequence[ChartSlot], out_pdf: Path | str) -> None:
    """Pass 2: merge each unchanged chart PDF onto its reserved slot."""
    from pypdf import PdfReader, PdfWriter, Transformation
    writer = PdfWriter(clone_from=PdfReader(str(base_pdf)))
    for s in slots:
        page = PdfReader(str(s.chart_path)).pages[0]
        op = Transformation().scale(s.scale, s.scale).translate(s.x, s.y)
        writer.pages[s.page_index].merge_transformed_page(page, op)
    with open(out_pdf, "wb") as f:
        writer.write(f)


# ---------------------------------------------------------------------------
# Shared piece: a row of three big numbers
# ---------------------------------------------------------------------------

def number_row(c: Canvas, t: Tokens, x: float, rule_y: float, width: float, numbers: Sequence[dict]) -> dict:
    """Three big numbers, each with a top rule, an icon (only if approved), the number
    (Light 56, unit at 43%), a label (caps, two lines at most) and a source line.
    numbers: [{"value", "unit", "label", "source", "icon"}]."""
    nr = t.pages["at_a_glance"]["number_row"]
    n = int(nr["columns"])
    if len(numbers) != n:
        raise ValueError(f"number_row takes {n} numbers")
    gap = float(nr["column_gap_pt"])
    cw = (width - (n - 1) * gap) / n
    big = t.style("big_number")
    lab = t.style("number_label")
    src = t.style("number_source")
    out = []
    for i, num in enumerate(numbers):
        cx = x + i * (cw + gap)
        drew_icon = False
        if num.get("icon"):
            drew_icon = icon(c, t, num["icon"], cx, rule_y + nr["icon_gap_above_rule_pt"], nr["icon_size_pt"])
        c.setStrokeColor(t.colour(nr["rule_color"]))
        c.setLineWidth(nr["rule_stroke_pt"])
        c.line(cx, rule_y, cx + cw, rule_y)
        nb = rule_y - nr["number_baseline_below_rule_pt"]
        fnt = font_name(big["weight"])
        c.setFillColor(t.colour(big["color"]))
        c.setFont(fnt, big["size_pt"])
        c.drawString(cx, nb, num["value"])
        vw = pdfmetrics.stringWidth(num["value"], fnt, big["size_pt"])
        unit = num.get("unit") or ""
        us = big["size_pt"] * float(big["unit_size_ratio"])
        if unit:
            ux = cx + vw + (us * 0.1 if unit[0] in "%" else us * 0.25)
            c.setFont(fnt, us)
            c.drawString(ux, nb, unit)
            vw = ux + pdfmetrics.stringWidth(unit, fnt, us) - cx
        if vw > cw:
            raise LayoutOverflow(f"big number {num['value']} {unit} is wider than its column")
        ltop = rule_y - nr["label_top_below_rule_pt"]
        lh = _height(lambda: [_para(t, num["label"], lab)], cw - 6)
        if lh > nr["label_height_pt"] + 0.5:
            raise LayoutOverflow(f"number label too long: {num['label']!r}")
        _flow(c, [_para(t, num["label"], lab)], [(cx, ltop - nr["label_height_pt"], cw - 6, nr["label_height_pt"])])
        sb = rule_y - nr["source_baseline_below_rule_pt"]
        sf = font_name(src["weight"])
        if pdfmetrics.stringWidth(num["source"], sf, src["size_pt"]) > cw:
            raise LayoutOverflow(f"number source too long: {num['source']!r}")
        c.setFont(sf, src["size_pt"])
        c.setFillColor(t.colour(src["color"]))
        c.drawString(cx, sb, num["source"])
        out.append({"x": cx, "w": cw, "icon": drew_icon})
    return {"rule_y": rule_y, "bottom": rule_y - nr["source_baseline_below_rule_pt"] - 3, "columns": out}


# ---------------------------------------------------------------------------
# Inside pages
# ---------------------------------------------------------------------------

def _body_style(t: Tokens, space_after: float | None = None) -> dict:
    spec = t.style("body")
    if space_after is not None:
        spec["space_after"] = space_after
    return spec


def _body_paras(t: Tokens, paras: Sequence[str], space_after: float = 6.5) -> list:
    spec = t.style("body")
    return [Paragraph(p, _pstyle(t, spec, spaceAfter=space_after)) for p in paras]


def paragraph(t: Tokens, text: str, kind: str = "body", space_after: float = 0, space_before: float = 0) -> Paragraph:
    """A Paragraph in one of the system's text styles: body, small, subheading, standfirst,
    cover_deck, finding_headline."""
    tp = t.pages["text_page"]
    if kind == "small":
        spec = {"weight": "Regular", "size_pt": tp["small_size_pt"], "leading_pt": tp["small_leading_pt"], "color": "soft_black"}
        space_after = space_after or tp["small_space_after_pt"]
    elif kind == "subheading":
        spec = {"weight": "Bold", "size_pt": tp["subheading_size_pt"], "leading_pt": tp["subheading_leading_pt"], "color": "indigo"}
    else:
        spec = t.style(kind)
    return Paragraph(text, _pstyle(t, spec, spaceAfter=space_after, spaceBefore=space_before))


def at_a_glance(c: Canvas, t: Tokens, *, label: str, page_no: int, standfirst: str,
                numbers: Sequence[dict], measured: str, summary: Sequence[str],
                kicker: str = "AT A GLANCE", measured_heading: str | None = None,
                icons: bool = True, code: str | None = None) -> dict:
    """Page 2 of Tiers 1-2: kicker, standfirst, a row of three big numbers, a 'What we
    measured' box (left) and the summary in body type (right). Nothing spills to another page.
    icons=False keeps a page free of icons even once some are approved. code= on a Tier 2/3
    report's last page (see running_chrome)."""
    pt = t.pages["at_a_glance"]
    if not icons:
        numbers = [dict(n, icon=None) for n in numbers]
    running_chrome(c, t, label, page_no, code)
    _caps(c, t, t.margin, t.y(pt["kicker_baseline_from_top_pt"]), kicker, t.style("kicker"))
    sf = t.style("standfirst")
    stop = t.y(pt["standfirst_top_from_top_pt"])
    sbot = _block(c, lambda: [_para(t, standfirst, sf)], t.margin, stop, pt["standfirst_width_pt"],
                  t.page_h / 2, "At a glance standfirst", runt=True)
    nr = pt["number_row"]
    rule_y = sbot - pt["number_row_gap_below_standfirst_pt"]
    if any_icon_approved(t, [n.get("icon") for n in numbers]):
        rule_y -= nr["icon_size_pt"] + nr["icon_gap_above_rule_pt"]
    row = number_row(c, t, t.margin, rule_y, t.content_w, numbers)
    bx = pt["box"]
    btop = row["rule_y"] - nr["source_baseline_below_rule_pt"] - bx["gap_below_number_row_pt"]
    bmin = bx["bottom_from_bottom_pt"]
    pad = bx["padding_pt"]
    # The box hugs its content (and the summary beside it) so the page stays balanced when
    # the method icons are absent; it never runs below bottom_from_bottom_pt.
    sm = pt["summary"]
    s_h = _height(lambda: _body_paras(t, summary, sm["space_after_pt"]), sm["width_pt"])
    if btop + 2 - s_h < bmin - 0.01:
        raise LayoutOverflow("At a glance summary overflows the page: cut copy, never spill")
    method = bx.get("method_icons", []) if icons else []
    show_icons = bool(method) and all(n in t.pictograms.get("approved", []) for n in method)
    mspec = {"weight": "Regular", "size_pt": bx["text_size_pt"], "leading_pt": bx["text_leading_pt"], "color": "soft_black"}
    m_h = _height(lambda: [_para(t, measured, mspec)], bx["width_pt"] - 2 * pad)
    inner = pad + bx["heading_size_pt"] + pad + ((bx["icon_size_pt"] + pad) if show_icons else 0) + m_h + pad
    bbot = max(bmin, min(btop - inner, btop + 2 - s_h))
    c.setFillColor(t.colour(bx["fill"]))
    c.rect(bx["x_pt"], bbot, bx["width_pt"], btop - bbot, stroke=0, fill=1)
    kspec = dict(t.style("kicker"), size_pt=bx["heading_size_pt"])
    hb = btop - pad - bx["heading_size_pt"]
    _caps(c, t, bx["x_pt"] + pad, hb, measured_heading or bx["heading"], kspec)
    ttop = hb - pad
    if show_icons:
        for k, nm in enumerate(method):
            icon(c, t, nm, bx["x_pt"] + pad + k * bx["icon_pitch_pt"], ttop - bx["icon_size_pt"], bx["icon_size_pt"])
        ttop -= bx["icon_size_pt"] + pad
    mbot = _block(c, lambda: [_para(t, measured, mspec)], bx["x_pt"] + pad, ttop, bx["width_pt"] - 2 * pad,
                  bbot + pad - 0.5, "At a glance: What we measured")
    scol = _columns(c, lambda: _body_paras(t, summary, sm["space_after_pt"]), btop + 2, bmin,
                    [sm["x_pt"]], sm["width_pt"], "At a glance summary (cut copy; never spill)")
    return {"standfirst_bottom": sbot, "number_row": row, "box": {"top": btop, "bottom": bbot, "text_bottom": mbot},
            "summary": scol,
            "words": {"kicker": count_words(kicker), "standfirst": count_words(standfirst),
                      "numbers": sum(count_words(" ".join([n["value"], n.get("unit", ""), n["label"], n["source"]])) for n in numbers),
                      "measured": count_words(measured) + count_words(measured_heading or bx["heading"]),
                      "summary": sum(count_words(p) for p in summary)}}


def contents_page(c: Canvas, t: Tokens, *, label: str, page_no: int, rows: Sequence[dict],
                  kicker: str = "CONTENTS", code: str | None = None) -> dict:
    """Contents. rows: [{"kind": "part"|"entry", "label": str, "title": str, "page": int}]."""
    pt = t.pages["contents"]
    running_chrome(c, t, label, page_no, code)
    _caps(c, t, t.margin, t.y(pt["kicker_baseline_from_top_pt"]), kicker, t.style("kicker"))
    y = t.y(pt["first_row_top_from_top_pt"])
    size = float(pt["entry_size_pt"])
    light, regular = font_name("Light"), font_name("Regular")
    num_x = t.col_left(1)
    title_x = t.col_left(2)
    for r in rows:
        if r["kind"] == "part":
            y -= pt["part_gap_pt"]
            _caps(c, t, num_x, y - size * 0.8, r["label"], t.style("kicker"))
            c.setFont(light, size)
            c.setFillColor(t.colour("soft_black"))
            c.drawString(title_x, y - size * 0.8, r["title"])
        else:
            c.setFont(light, size)
            c.setFillColor(t.colour("indigo"))
            c.drawString(num_x, y - size * 0.8, r.get("label", ""))
            c.setFillColor(t.colour("soft_black"))
            c.drawString(title_x, y - size * 0.8, r["title"])
        if r.get("page") is not None:
            c.setFont(regular, size * 0.7)
            c.setFillColor(t.colour("indigo"))
            c.drawRightString(t.page_w - t.margin, y - size * 0.8, str(r["page"]))
        tw = pdfmetrics.stringWidth(r["title"], light, size)
        if title_x + tw > t.page_w - t.margin - 30:
            raise LayoutOverflow(f"contents title too long: {r['title']!r}")
        c.setStrokeColor(t.colour("grid"))
        c.setLineWidth(pt["rule_stroke_pt"])
        c.line(t.margin, y - pt["row_pitch_pt"] + 8, t.page_w - t.margin, y - pt["row_pitch_pt"] + 8)
        y -= pt["row_pitch_pt"]
        if y < t.pages["footer"]["rule_from_bottom_pt"] + 20:
            raise LayoutOverflow("contents run past the page")
    return {"bottom": y}


def finding_page(c: Canvas, t: Tokens, *, label: str, page_no: int, page_index: int, number: int,
                 kicker: str, headline: str, chart_path: Path | str, caption: str,
                 body: Sequence[str], slots: list, code: str | None = None) -> dict:
    """Finding page: number left, kicker and headline right, an Indigo rule, the chart at
    full content width (reserved from its mediabox), its caption, two columns of body.
    code= on a Tier 2/3 report's last page (see running_chrome)."""
    fp = t.pages["finding_page"]
    running_chrome(c, t, label, page_no, code)
    nspec = t.style("finding_number")
    c.setFillColor(t.colour(nspec["color"]))
    c.setFont(font_name(nspec["weight"]), nspec["size_pt"])
    numtxt = f"{number:02d}"
    c.drawString(fp["number_x_pt"], t.y(fp["number_baseline_from_top_pt"]), numtxt)
    nw = pdfmetrics.stringWidth(numtxt, font_name(nspec["weight"]), nspec["size_pt"])
    if fp["number_x_pt"] + nw > fp["text_x_pt"] - 12:
        raise LayoutOverflow("finding number collides with the headline column")
    _caps(c, t, fp["text_x_pt"], t.y(fp["kicker_baseline_from_top_pt"]), kicker, t.style("kicker"))
    hspec = t.style("finding_headline")
    htop = t.y(fp["headline_top_from_top_pt"])
    hbot = _block(c, lambda: [_para(t, headline, hspec)], fp["text_x_pt"], htop, fp["headline_width_pt"],
                  htop - fp["headline_max_height_pt"], "finding headline", runt=True)
    ry = t.y(fp["rule_from_top_pt"])
    if hbot < ry + 4:
        raise LayoutOverflow("finding headline reaches the rule")
    c.setStrokeColor(t.colour("indigo"))
    c.setLineWidth(fp["rule_stroke_pt"])
    c.line(t.margin, ry, t.page_w - t.margin, ry)
    cw, ch, sc = reserve_chart(chart_path, t.content_w)
    ctop = t.y(fp["chart_top_from_top_pt"])
    cx = t.margin + (t.content_w - cw) / 2
    slots.append(ChartSlot(page_index, Path(chart_path), cx, ctop - ch, cw, ch, sc))
    cap = fp["caption"]
    cspec = {"weight": cap["weight"], "size_pt": cap["size_pt"], "leading_pt": cap["leading_pt"], "color": cap["color"]}
    capt = ctop - ch - cap["gap_below_chart_pt"]
    bd = fp["body"]
    content_bottom = bd["bottom_from_bottom_pt"]
    capb = _block(c, lambda: [_para(t, caption, cspec)], t.margin, capt, t.content_w, content_bottom, "chart caption")
    btop = capb - bd["gap_below_caption_pt"]
    xs = [t.margin + k * (bd["column_width_pt"] + bd["gutter_pt"]) for k in range(bd["columns"])]
    cols = _columns(c, lambda: _body_paras(t, body), btop, content_bottom, xs, bd["column_width_pt"],
                    f"finding {number:02d} body")
    return {"chart": {"x": cx, "top": ctop, "bottom": ctop - ch, "w": cw, "h": ch},
            "caption": {"top": capt, "bottom": capb}, "body": cols, "headline_bottom": hbot, "rule_y": ry,
            "words": {"head": count_words(kicker) + count_words(headline), "caption": count_words(caption),
                      "body": sum(count_words(p) for p in body)},
            "chart_h_pt": ch}


def finding_evidence_page(c: Canvas, t: Tokens, *, label: str, page_no: int, page_index: int,
                          kicker: str, charts: Sequence[tuple[Path | str, str]], body: Sequence[str],
                          slots: list, code: str | None = None) -> dict:
    """Tier 1 evidence page: up to two 3-column charts side by side with their captions,
    then two columns of body."""
    ep = t.pages["finding_evidence_page"]
    if not 1 <= len(charts) <= ep["charts_max"]:
        raise ValueError(f"an evidence page carries 1 to {ep['charts_max']} charts")
    running_chrome(c, t, label, page_no, code)
    _caps(c, t, t.margin, t.y(ep["kicker_baseline_from_top_pt"]), kicker, t.style("kicker"))
    span = int(ep["chart_columns"])
    top = t.y(ep["charts_top_from_top_pt"])
    cap = t.pages["finding_page"]["caption"]
    cspec = {"weight": cap["weight"], "size_pt": cap["size_pt"], "leading_pt": cap["leading_pt"], "color": cap["color"]}
    lowest = top
    placed = []
    for k, (path, caption) in enumerate(charts):
        x0 = t.col_left(1 + k * span)
        wmax = t.span(1 + k * span, (k + 1) * span)
        cw, ch, sc = reserve_chart(path, wmax)
        slots.append(ChartSlot(page_index, Path(path), x0, top - ch, cw, ch, sc))
        cb = _block(c, lambda: [_para(t, caption, cspec)], x0, top - ch - ep["caption_gap_below_chart_pt"], wmax,
                    t.pages["finding_page"]["body"]["bottom_from_bottom_pt"], "evidence caption")
        placed.append({"x": x0, "w": cw, "h": ch, "caption_bottom": cb})
        lowest = min(lowest, cb)
    bd = t.pages["finding_page"]["body"]
    xs = [t.margin + k * (bd["column_width_pt"] + bd["gutter_pt"]) for k in range(bd["columns"])]
    cols = _columns(c, lambda: _body_paras(t, body), lowest - ep["body_gap_below_charts_pt"],
                    bd["bottom_from_bottom_pt"], xs, bd["column_width_pt"], "evidence body") if body else None
    return {"charts": placed, "body": cols}


def section_opener(c: Canvas, t: Tokens, *, part: int, title: str, part_label: str | None = None) -> dict:
    """Tier 1 section opener: full Indigo page, the wordmark, 'PART N' in caps (Lavender Grey),
    the title in Light 44/47 white, and a large part number (Light 200, Lavender Grey)."""
    so = t.pages["section_opener"]
    c.setFillColor(t.colour(so["ground"]))
    c.rect(0, 0, t.page_w, t.page_h, stroke=0, fill=1)
    wordmark(c, t, t.margin, t.y(so["wordmark_baseline_from_top_pt"]), so["wordmark_size_pt"], dark=True)
    pspec = t.style("section_opener_part")
    pb = t.page_h * float(so["part_baseline_from_bottom_ratio"])
    _caps(c, t, t.margin, pb, part_label or f"PART {part}", pspec)
    tspec = t.style("section_opener_title")
    ttop = t.page_h * float(so["title_top_from_bottom_ratio"])
    nspec = t.style("section_opener_numeral")
    nb = so["numeral_baseline_from_bottom_pt"]
    num_top = nb + pdfmetrics.getAscent(font_name(nspec["weight"]), nspec["size_pt"]) * 0.72
    tbot = _block(c, lambda: [_para(t, title, tspec)], t.margin, ttop, so["title_width_pt"], num_top + 12,
                  "section opener title", runt=True)
    c.setFillColor(t.colour(nspec["color"]))
    c.setFont(font_name(nspec["weight"]), nspec["size_pt"])
    c.drawRightString(so["numeral_right_x_pt"], nb, f"{part:02d}")
    return {"part_baseline": pb, "title": {"top": ttop, "bottom": tbot}}


def text_page(c: Canvas, t: Tokens, *, label: str, page_no: int, sections: Sequence[dict],
              kicker: str | None = None, lead: str | None = None, bottom_note: Sequence[dict] | None = None,
              code: str | None = None) -> dict:
    """Running text page. Optional kicker and lead (standfirst style), then sections stacked
    down the page: {"heading": str|None, "heading_style": "finding_headline"|"subheading",
    "paras": [...], "columns": 1|2, "size": "body"|"small", "flowables": [...]}.
    code= on a Tier 2/3 report's last page (see running_chrome)."""
    tp = t.pages["text_page"]
    running_chrome(c, t, label, page_no, code)
    y = t.y(tp["heading_top_from_top_pt"])
    bottom = t.pages["finding_page"]["body"]["bottom_from_bottom_pt"]
    if kicker:
        _caps(c, t, t.margin, t.y(tp["kicker_baseline_from_top_pt"]), kicker, t.style("kicker"))
    words = 0
    if lead:
        y = _block(c, lambda: [_para(t, lead, t.style("standfirst"))], t.margin, y, t.content_w, bottom, "lead", runt=True) - 22
        words += count_words(lead)
    gw = tp["gutter_pt"]
    for sec in sections:
        if sec.get("stacks"):
            colw = (t.content_w - gw) / 2
            bottoms = []
            for k, make in enumerate(sec["stacks"]):
                bottoms.append(_block(c, make, t.margin + k * (colw + gw), y, colw, bottom, f"stack {k + 1}"))
            y = min(bottoms) - sec.get("gap_after", 12)
            words += sec.get("words", 0)
            continue
        if sec.get("rule"):
            c.setStrokeColor(t.colour("indigo"))
            c.setLineWidth(t.pages["finding_page"]["rule_stroke_pt"])
            c.line(t.margin, y + 6, t.page_w - t.margin, y + 6)
            y -= 8
        if sec.get("heading"):
            hs = sec.get("heading_style", "finding_headline")
            if hs == "subheading":
                spec = {"weight": "Bold", "size_pt": tp["subheading_size_pt"], "leading_pt": tp["subheading_leading_pt"], "color": "indigo"}
            else:
                spec = t.style(hs)
            y = _block(c, lambda h=sec["heading"], s=spec: [_para(t, h, s)], t.margin, y, t.content_w, bottom,
                       "section heading", runt=True) - (4 if hs == "subheading" else 12)
            words += count_words(sec["heading"])
        if sec.get("size") == "small":
            spec = {"weight": "Regular", "size_pt": tp["small_size_pt"], "leading_pt": tp["small_leading_pt"], "color": "soft_black"}
            make = (lambda ps=sec["paras"], s=spec: [Paragraph(p, _pstyle(t, s, spaceAfter=tp["small_space_after_pt"])) for p in ps])
        elif sec.get("flowables"):
            make = sec["flowables"]
        else:
            make = (lambda ps=sec["paras"]: _body_paras(t, ps))
        ncol = sec.get("columns", 2)
        if ncol == 2:
            colw = (t.content_w - gw) / 2
            res = _columns(c, make, y, bottom, [t.margin, t.margin + colw + gw], colw, sec.get("heading") or "text")
            y = res["bottom"] - sec.get("gap_after", 18)
        else:
            y = _block(c, make, t.margin, y, sec.get("width", t.content_w), bottom, sec.get("heading") or "text") - sec.get("gap_after", 12)
        words += sum(count_words(p) for p in sec.get("paras", []))
    return {"bottom": y, "words": words}


def colophon_paragraphs(t: Tokens) -> Callable[..., Paragraph]:
    """Paragraph maker for the closing page's colophon (report_specs closing_page: 7.2/9.9 pt,
    headings Bold Indigo): p(text, kind='body'|'head', before=0, after=None). The website
    in colophon text is always lower case."""
    cp = t.pages["closing_page"]
    body = {"weight": "Regular", "size_pt": cp["colophon_size_pt"], "leading_pt": cp["colophon_leading_pt"],
            "color": "soft_black"}
    head = dict(body, weight="Bold", color="indigo")

    def p(text: str, kind: str = "body", before: float = 0.0, after: float | None = None) -> Paragraph:
        return _para(t, RC.website_lower(text, t.website), head if kind == "head" else body, spaceBefore=before,
                     spaceAfter=cp["colophon_space_after_pt"] if after is None else after)
    return p


def closing_page(c: Canvas, t: Tokens, *, label: str, page_no: int, statement: str,
                 left: Callable[[], list], right: Callable[[], list], code: str) -> dict:
    """Tier 1 closing page (decision 13, Pablo, Nov 12, 2026; updated Nov 13 with decision 14):
    the running header; the closing statement large (standfirst style); the admin blocks as a
    quiet two-column colophon low on the page under a thin footer-style rule (left/right return
    each column's flowables, made with colophon_paragraphs()); then a full-width Indigo band
    (the C2 title block's fill), in place of the footer line, with one line: the wordmark in
    white at the cover lockup's size, the website in lower case (Lavender Grey, Regular), the
    report code (Lavender Grey caps style, printed exactly as registered) and the page number.
    Geometry: report_specs.json section_template.page_templates.closing_page."""
    RC.parse_code(code)
    cp = t.pages["closing_page"]
    tp = t.pages["text_page"]
    _paper(c, t)
    rh = t.pages["running_header"]
    st = t.scale["running_header"]
    hb = t.y(rh["baseline_from_top_pt"])
    wordmark(c, t, rh["x_pt"], hb, st["wordmark"]["size_pt"])
    _caps(c, t, t.page_w - t.margin, hb, label, st["label"], align="right")
    band_top = float(cp["band_height_pt"])
    stop = t.y(tp["heading_top_from_top_pt"])
    sbot = _block(c, lambda: [_para(t, statement, t.style("standfirst"))], t.margin, stop, t.content_w,
                  band_top, "closing statement", runt=True)
    # colophon: two columns, top-aligned, its lowest line colophon_gap_above_band_pt above the band
    gw = tp["gutter_pt"]
    colw = (t.content_w - gw) / 2
    hl, hr = _height(left, colw), _height(right, colw)
    ctop = band_top + cp["colophon_gap_above_band_pt"] + max(hl, hr)
    rule_y = ctop + cp["colophon_rule_gap_pt"]
    if rule_y > sbot - cp["min_gap_below_statement_pt"]:
        raise LayoutOverflow(f"closing colophon reaches the statement ({sbot - rule_y:.0f} pt apart)")
    ft = t.pages["footer"]
    c.setStrokeColor(t.colour(ft["rule_color"]))
    c.setLineWidth(ft["rule_stroke_pt"])
    c.line(t.margin, rule_y, t.page_w - t.margin, rule_y)
    bl = _block(c, left, t.margin, ctop, colw, band_top, "colophon left")
    br = _block(c, right, t.margin + colw + gw, ctop, colw, band_top, "colophon right")
    # the Indigo band and its one line
    c.setFillColor(t.colour(t.covers["C2"]["title_block"]["fill"]))
    c.rect(0, 0, t.page_w, band_top, stroke=0, fill=1)
    base = float(cp["band_baseline_from_bottom_pt"])
    wm = t.covers["lockup"]["line1"]["size_pt"]
    ww = wordmark(c, t, t.margin, base, wm, dark=True)
    kspec = t.style(cp["band_text_style"], "C2")
    web = dict(kspec, tracking_em=cp["band_website_tracking_em"])
    x_web = t.margin + ww + float(cp["band_gap_after_wordmark_em"]) * wm
    w_web = _caps(c, t, x_web, base, t.website, web, case="as_is")
    w_sep = _caps(c, t, x_web + w_web, base, cp["band_separator"], web, case="as_is")
    x_code = x_web + w_web + w_sep
    w_code = _caps(c, t, x_code, base, code, kspec, case=cp["band_code_case"])
    w_page = _caps(c, t, t.page_w - t.margin, base, str(page_no), kspec, align="right")
    if x_code + w_code > t.page_w - t.margin - w_page - 12:
        raise LayoutOverflow("closing band: the report code runs into the page number")
    return {"statement_bottom": sbot, "colophon": {"rule_y": rule_y, "top": ctop, "bottom": min(bl, br)},
            "band": {"top": band_top, "baseline": base, "wordmark_size": wm, "wordmark_right": t.margin + ww,
                     "website": {"x": x_web, "w": w_web, "text": t.website},
                     "code": {"x": x_code, "w": w_code, "text": code}, "page_number_w": w_page}}


def table_flowable(t: Tokens, header: Sequence[str], rows: Sequence[Sequence[str]], col_widths: Sequence[float],
                   bold_first_col: bool = True) -> Table:
    """A ruled table in the system's type: Indigo rules top and bottom, Lavender Grey row rules."""
    tb = t.pages["table"]
    hs = {"weight": "Bold", "size_pt": tb["header_size_pt"], "leading_pt": tb["header_leading_pt"], "color": tb["rule_color"]}
    cs = {"weight": "Regular", "size_pt": tb["cell_size_pt"], "leading_pt": tb["cell_leading_pt"], "color": "soft_black"}
    data = [[Paragraph(h, _pstyle(t, hs)) for h in header]]
    for r in rows:
        data.append([Paragraph((f"<b>{v}</b>" if (bold_first_col and i == 0) else v), _pstyle(t, cs)) for i, v in enumerate(r)])
    ind, lav = t.colour(tb["rule_color"]), t.colour(tb["row_rule_color"])
    pad = tb["padding_pt"]
    return Table(data, colWidths=list(col_widths), style=TableStyle([
        ("LINEABOVE", (0, 0), (-1, 0), tb["outer_rule_pt"], ind), ("LINEBELOW", (0, 0), (-1, 0), tb["header_rule_pt"], ind),
        ("LINEBELOW", (0, 1), (-1, -2), tb["row_rule_pt"], lav), ("LINEBELOW", (0, -1), (-1, -1), tb["outer_rule_pt"], ind),
        ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), pad),
        ("BOTTOMPADDING", (0, 0), (-1, -1), pad), ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2 * pad)]))


# ---------------------------------------------------------------------------
# Word budgets
# ---------------------------------------------------------------------------

_TAG = re.compile(r"<[^>]+>")


def count_words(text: str) -> int:
    """Words in a string (markup stripped; a token counts if it holds a letter or digit)."""
    text = _TAG.sub(" ", text or "").replace("&nbsp;", " ").replace(" ", " ")
    return sum(1 for tok in text.split() if any(ch.isalnum() for ch in tok))


def word_budget(t: Tokens, elements: Iterable[str] = ()) -> int:
    """600 words per full text page minus the deduction of each element on the page."""
    wb = t.budget
    total = int(wb["full_text_page_words"])
    for e in elements:
        total -= int(wb["deductions_words"][e])
    return total


def check_page_budget(t: Tokens, words: int, elements: Iterable[str] = ()) -> dict:
    elements = list(elements)
    b = word_budget(t, elements)
    return {"elements": elements, "budget": b, "words": int(words), "ok": words <= b, "over_by": max(0, words - b)}


def chart_element(t: Tokens, w_pt: float, h_pt: float) -> str:
    """Word-budget element for a chart of this footprint (column span from its width;
    6-column charts up to 7.5 x 3.75 in count as the short hero)."""
    cols_needed = next(n for n in range(1, t.columns + 1) if t.span(1, n) >= w_pt - 0.5)
    if cols_needed >= 6:
        return "hero_6col_short" if h_pt <= 3.75 * 72 + 0.5 else "hero_6col"
    if cols_needed >= 4:
        return "chart_4col"
    return "chart_3col"
