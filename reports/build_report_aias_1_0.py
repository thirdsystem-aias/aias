#!/usr/bin/env python3
"""
AIAS 1.0 — Third System brand-format synthesis report typesetting pipeline.

Synthesis-scale managerial deliverable for the AIAS 1.0 SSRN paper
(SSRN 6817841, May 2026). Consolidates five-substrate empirical anchor
base (v0.16 kitchenware → v0.21 cosmetics) under locked methodology v1.6
in P1–P5 propositional register for brand strategists and marketing-
science practitioners.

Forked from build_report_v21.py with surgical changes per outline §6 D6:
  - Imports aias_1_0_content instead of v21_cosmetics_content
  - CHART_FIGSIZE_IN extended with 4 aias_1_0_* figsize keys (matches
    native figsizes of the 3 re-used synthesis charts + the P2 brand-
    format upgrade)
  - _slot_lookup returns RELATIVE PATHS from reports/ root (charts live
    in two subdirs: figs/aias_1_0/ for the 3 re-used synthesis charts;
    figs/aias_1_0_report/ for the P2 brand-format upgrade)
  - HERO_FIGURE_CAPTIONS rebuilt for synthesis chart slots in managerial
    register (4 captions; P5 is text-only with no chart_slot)
  - PATTERNS loop handles 5 findings vs. v21's 3 (loop is count-agnostic;
    no scaffolding change)
  - HYPOTHESIS_SCORING/HYPOTHESIS_DETAILS renamed PROPOSITION_SCORING/
    PROPOSITION_DETAILS in content module; corresponding builder function
    renamed build_proposition_scoring_story; column header "H" → "P" so
    no academic-register leakage into rendered text
  - Header right text: "AIAS 1.0 · Five-Substrate Synthesis · May 2026"
  - Citation text: synthesis paper SSRN 6817841
  - Output filename: aias_1_0_brand_format_report.pdf
  - Page count target band: 22–32 pages (vs. v21's 8–14 for single phase)

Inputs:
  - brand/third_system_brand.json
  - brand/design_tokens_template.json
  - reports/figs/aias_1_0/chart_02_anchor_base_lineage.pdf   (re-used)
  - reports/figs/aias_1_0/chart_04_type2_emergence.pdf       (re-used)
  - reports/figs/aias_1_0/chart_05_il_direct_forest.pdf      (re-used)
  - reports/figs/aias_1_0_report/chart_p2_phantom_channel_brand_format.pdf
    (built by reports/build_charts_aias_1_0_report.py)

Output:
  - osf/aias_1_0/reports/aias_1_0_brand_format_report.pdf

Run order:
    python scripts/build_charts_aias_1_0.py              # synthesis paper charts
    python reports/build_charts_aias_1_0_report.py        # P2 brand-format upgrade
    python reports/build_report_aias_1_0.py               # the report

Locked rules followed (same as v0.6 → v0.21):
  - Image-placeholder rectangles in master spreads stay BLANK.
  - Template's #FF001A red is overridden to brand primary (Indigo).
  - Akkurat Pro registered when available; Inter fallback; HARD WARNING
    if neither found.
  - Charts embedded at native figsize from CHART_FIGSIZE_IN; no rescaling.
"""

from __future__ import annotations

import json
import os
import sys
import warnings
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import (
    BalancedColumns,
    BaseDocTemplate,
    CondPageBreak,
    Flowable,
    Frame,
    FrameBreak,
    ImageAndFlowables,
    KeepTogether,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

import pypdf
from pypdf import PdfReader, PdfWriter, Transformation

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
AIAS_ROOT = SCRIPT_DIR.parent
BRAND_DIR = AIAS_ROOT / "brand"
OUTPUT_DIR = SCRIPT_DIR / "output"
REPORTS_DIR = SCRIPT_DIR  # ~/aias/reports/ — base for chart subdirs

BRAND_JSON = BRAND_DIR / "third_system_brand.json"
TOKENS_JSON = BRAND_DIR / "design_tokens_template.json"
SPECS_JSON = BRAND_DIR / "report_specs.json"
SOURCE_TEXT = BRAND_DIR / "v06_source_text.md"
WORDMARK_SVG = BRAND_DIR / "THIRDSYSTEM_Logo.svg"
LOCKUP_SVG = BRAND_DIR / "THIRDSYSTEM_AIPT_Logo.svg"

# Make `import aias_1_0_content` work regardless of working directory.
sys.path.insert(0, str(SCRIPT_DIR))
import aias_1_0_content as content  # noqa: E402
import tsboilerplate as boilerplate  # noqa: E402

# ---------------------------------------------------------------------------
# Page geometry — locked by template content_area (same as v21)
# ---------------------------------------------------------------------------

PAGE_W, PAGE_H = LETTER
MARGIN = 36.0
CONTENT_W = PAGE_W - 2 * MARGIN
CONTENT_H = PAGE_H - 2 * MARGIN
COL_COUNT = 6
GUTTER = 10.0008
COL_W = (CONTENT_W - (COL_COUNT - 1) * GUTTER) / COL_COUNT

COL_X = [MARGIN + i * (COL_W + GUTTER) for i in range(COL_COUNT)]

def span_pts(n: int) -> float:
    return n * COL_W + (n - 1) * GUTTER

SPANS_PT = {n: span_pts(n) for n in range(1, COL_COUNT + 1)}

# Synthesis-scale charts (11 × 7.5 / 11 × 8) exceed v21's hardcoded 500pt
# clamp; lifted to 600pt here so native chart heights render without slot
# under-fill. v21 used 500.0 for phase-scale charts (max ~5.5" / 396pt).
CHART_RESERVATION_HEIGHT_CLAMP_PT = 600.0

# Width clamp mirrors the height clamp pattern. Synthesis charts render at
# 11" native width (792pt) which exceeds the page content area (540pt at
# the 0.5" MARGIN config). Without this clamp, ChartReservation stores the
# raw 792pt in manifest.w_pt, and overlay_charts positions charts based on
# that 792pt reservation — extending charts past the page right margin.
# Clamping to CONTENT_W keeps charts inside the page margins; the chart-
# overlay's proportional min(sx, sy) scaling then preserves chart aspect.
CHART_RESERVATION_WIDTH_CLAMP_PT = CONTENT_W

# Chart figsize spec (inches). AIAS 1.0 keys match native figsizes from
# the synthesis paper chart builder + the P2 brand-format upgrade.
CHART_FIGSIZE_IN = {
    # AIAS 1.0 synthesis report keys — 4 chart slots; P5 is text-only.
    # Native figsizes match scripts/build_charts_aias_1_0.py for the 3 re-
    # used synthesis charts; P2 brand-format upgrade matches chart_06
    # native (11 × 8) for layout consistency.
    "aias_1_0_anchor_base":      (11.0, 6.5),   # P1 — chart_02 (native)
    "aias_1_0_phantom_channel":  (11.0, 8.0),   # P2 — brand-format upgrade
                                                # (native; signature chart kept
                                                # at full size; P2 heading orphan
                                                # on page 9 accepted per r2 triage)
    "aias_1_0_type2_emergence":  (11.0, 6.5),   # P3 — chart_04 reduced from 7.5
                                                # to fit heading + chart + caption
                                                # on one page (no orphan)
    "aias_1_0_il_direct_forest": (11.0, 6.5),   # P4 — chart_05 reduced from 7.5
                                                # to fit heading + chart + caption
                                                # on one page (no orphan)
}

BODY_LEFT_X = COL_X[0]
BODY_LEFT_W = span_pts(3)
BODY_RIGHT_X = COL_X[3]
BODY_RIGHT_W = span_pts(3)


# ---------------------------------------------------------------------------
# Brand colors (verbatim from v21)
# ---------------------------------------------------------------------------

@dataclass
class BrandPalette:
    indigo: str
    soft_black: str
    paper: str
    petro: str
    lavender_grey: str
    template_red_override: str

    @classmethod
    def from_json(cls, brand: dict) -> "BrandPalette":
        p = brand["palette"]
        indigo = p["primary_brand"]["indigo"]["hex"]
        soft_black = p["anchor_black"]["hex"]
        paper = p["paper_off_white"]["hex"]
        petro = p["brand_supporting"]["petro"]["hex"]
        lavender = p["brand_supporting"]["lavender_grey"]["hex"]
        return cls(
            indigo=indigo,
            soft_black=soft_black,
            paper=paper,
            petro=petro,
            lavender_grey=lavender,
            template_red_override=indigo,
        )


# ---------------------------------------------------------------------------
# Font registration (verbatim from v21)
# ---------------------------------------------------------------------------

@dataclass
class FontFamily:
    name: str
    light: str
    regular: str
    bold: str
    italic: str
    bold_italic: str
    is_brand_primary: bool


def _convert_otf_to_ttf(otf_path: Path, cache_dir: Path) -> Path | None:
    try:
        from fontTools.ttLib import TTFont as _FTFont
        from fontTools.pens.ttGlyphPen import TTGlyphPen
        from fontTools.pens.cu2quPen import Cu2QuPen
        from fontTools.ttLib.tables import _l_o_c_a
        from fontTools.ttLib.tables._g_l_y_f import table__g_l_y_f
    except ImportError:
        print(f"  [convert-fail] fontTools not installed; cannot convert {otf_path.name}")
        return None

    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cache_dir / (otf_path.stem + ".ttf")

    try:
        if cache_path.exists() and cache_path.stat().st_mtime >= otf_path.stat().st_mtime:
            return cache_path
    except OSError:
        pass

    try:
        font = _FTFont(str(otf_path))
        if "glyf" in font:
            font.save(str(cache_path))
            return cache_path
        if "CFF " not in font:
            return None

        glyph_set = font.getGlyphSet()
        glyf_table = table__g_l_y_f()
        glyf_table.glyphs = {}
        for name in font.getGlyphOrder():
            glyph = glyph_set[name]
            ttpen = TTGlyphPen(glyph_set)
            cu2qupen = Cu2QuPen(ttpen, max_err=1.0, reverse_direction=True)
            glyph.draw(cu2qupen)
            glyf_table.glyphs[name] = ttpen.glyph()

        font["glyf"] = glyf_table
        font["loca"] = _l_o_c_a.table__l_o_c_a()
        font["head"].indexToLocFormat = 0
        if font["maxp"].tableVersion != 0x00010000:
            font["maxp"].tableVersion = 0x00010000
            for attr, default in [
                ("maxPoints", 0), ("maxContours", 0), ("maxCompositePoints", 0),
                ("maxCompositeContours", 0), ("maxZones", 1), ("maxTwilightPoints", 0),
                ("maxStorage", 0), ("maxFunctionDefs", 0), ("maxInstructionDefs", 0),
                ("maxStackElements", 0), ("maxSizeOfInstructions", 0),
                ("maxComponentElements", 0), ("maxComponentDepth", 0),
            ]:
                if not hasattr(font["maxp"], attr):
                    setattr(font["maxp"], attr, default)
        del font["CFF "]
        if "VORG" in font:
            del font["VORG"]
        font.sfntVersion = "\x00\x01\x00\x00"
        font.save(str(cache_path))
        return cache_path
    except Exception as exc:
        print(f"  [convert-fail] {otf_path.name}: {type(exc).__name__}: {exc}")
        return None


_FONT_CACHE_DIR = Path.home() / ".cache" / "third_system_reports" / "fonts"


def _try_register_font(label: str, path: Path) -> bool:
    if not path.exists():
        return False
    try:
        pdfmetrics.registerFont(TTFont(label, str(path)))
        return True
    except Exception as exc:
        msg = str(exc).lower()
        if path.suffix.lower() == ".otf" and (
            "postscript" in msg or "cff" in msg or "outlines are not supported" in msg
        ):
            converted = _convert_otf_to_ttf(path, _FONT_CACHE_DIR)
            if converted and converted.exists():
                try:
                    pdfmetrics.registerFont(TTFont(label, str(converted)))
                    return True
                except Exception:
                    return False
            return False
        return False


def _font_search_dirs() -> list[Path]:
    home = Path.home()
    return [
        home / "Library" / "Fonts",
        Path("/Library/Fonts"),
        Path("/System/Library/Fonts"),
        Path("/System/Library/Fonts/Supplemental"),
        home / "Library" / "Application Support" / "Adobe" / "CoreSync" / "plugins" / "livetype" / ".r",
        home / "Library" / "Application Support" / "Adobe" / "CoreSync" / "plugins" / "livetype" / "r",
        home / ".fonts",
        home / ".fonts" / "Akkurat",
        home / ".fonts" / "Inter",
        home / ".local" / "share" / "fonts",
        Path("/usr/share/fonts"),
        Path("/usr/local/share/fonts"),
    ]


def _enumerate_font_files(dirs: list[Path]) -> list[Path]:
    found = []
    for d in dirs:
        if not d.exists():
            continue
        try:
            for ext in ("*.otf", "*.ttf", "*.OTF", "*.TTF"):
                found.extend(d.rglob(ext))
        except Exception:
            continue
    return found


def _classify_font_filename(filename: str) -> str | None:
    n = filename.lower().replace(" ", "").replace("_", "").replace("-", "")
    if "bolditalic" in n:
        return "bolditalic"
    if "lightpro" in n and "italic" in n:
        return "italic"
    if "lightitalic" in n:
        return "italic"
    if "light" in n and "italic" in n:
        return "italic"
    if "italic" in n and "bold" not in n:
        return "italic"
    if "bold" in n:
        return "bold"
    if "light" in n:
        return "light"
    if "regular" in n:
        return "regular"
    return "regular"


def _classify_files_into_slots(files: list[Path]) -> dict[str, Path | None]:
    buckets: dict[str, list[Path]] = {
        "light": [], "regular": [], "bold": [],
        "italic": [], "bolditalic": [],
    }
    for f in files:
        cls = _classify_font_filename(f.name)
        if cls in buckets:
            buckets[cls].append(f)

    def _is_light_family(p: Path) -> bool:
        n = p.name.lower().replace(" ", "").replace("_", "").replace("-", "")
        return "lightpro" in n

    picked: dict[str, Path | None] = {}
    for cls, candidates in buckets.items():
        if cls in ("bold", "italic", "bolditalic"):
            non_light = [p for p in candidates if not _is_light_family(p)]
            if non_light:
                picked[cls] = non_light[0]
            elif candidates:
                picked[cls] = candidates[0]
            else:
                picked[cls] = None
        elif cls == "light":
            light_in_pro_family = [
                p for p in candidates
                if "-light." in p.name.lower() or "prolight." in p.name.lower().replace("-", "").replace("_", "")
            ]
            if light_in_pro_family:
                picked[cls] = light_in_pro_family[0]
            elif candidates:
                picked[cls] = candidates[0]
            else:
                picked[cls] = None
        else:
            picked[cls] = candidates[0] if candidates else None
    return picked


def register_typography() -> FontFamily:
    dirs = _font_search_dirs()
    all_files = _enumerate_font_files(dirs)
    print(f"[fonts] scanned {len(all_files)} font files across {len(dirs)} dirs")

    akkurat_files = [p for p in all_files if "akkurat" in p.name.lower()]
    akkurat_picked = _classify_files_into_slots(akkurat_files)

    slot_to_class = {
        "Akkurat-Light":      "light",
        "Akkurat-Regular":    "regular",
        "Akkurat-Bold":       "bold",
        "Akkurat-Italic":     "italic",
        "Akkurat-BoldItalic": "bolditalic",
    }
    found_akkurat: dict[str, Path | None] = {}
    for slot_label, cls in slot_to_class.items():
        path = akkurat_picked.get(cls)
        if path and _try_register_font(slot_label, path):
            found_akkurat[slot_label] = path
        else:
            found_akkurat[slot_label] = None

    must_have = ("Akkurat-Light", "Akkurat-Regular", "Akkurat-Bold")
    if all(found_akkurat.get(k) for k in must_have):
        regular = "Akkurat-Regular"
        bold = "Akkurat-Bold"
        italic = "Akkurat-Italic" if found_akkurat.get("Akkurat-Italic") else regular
        bold_italic = "Akkurat-BoldItalic" if found_akkurat.get("Akkurat-BoldItalic") else bold
        for base in (regular, "Akkurat-Light"):
            pdfmetrics.registerFontFamily(
                base, normal=base, bold=bold, italic=italic, boldItalic=bold_italic)
        print(f"[fonts] using Akkurat Pro (brand-compliant)")
        return FontFamily(
            name="Akkurat Pro",
            light="Akkurat-Light",
            regular=regular,
            bold=bold,
            italic=italic,
            bold_italic=bold_italic,
            is_brand_primary=True,
        )

    warnings.warn("Akkurat Pro not found; attempting Inter fallback.")
    inter_files = [p for p in all_files if "inter" in p.name.lower()
                    and "interstate" not in p.name.lower()]
    inter_picked = _classify_files_into_slots(inter_files)
    inter_slot_to_class = {
        "Inter-Light": "light", "Inter-Regular": "regular", "Inter-Bold": "bold",
        "Inter-Italic": "italic", "Inter-BoldItalic": "bolditalic",
    }
    found_inter: dict[str, Path | None] = {}
    for slot_label, cls in inter_slot_to_class.items():
        path = inter_picked.get(cls)
        if path and _try_register_font(slot_label, path):
            found_inter[slot_label] = slot_label
        else:
            found_inter[slot_label] = None

    if all(found_inter.get(k) for k in ("Inter-Light", "Inter-Regular", "Inter-Bold")):
        regular = "Inter-Regular"
        bold = "Inter-Bold"
        italic = "Inter-Italic" if found_inter.get("Inter-Italic") else regular
        bold_italic = "Inter-BoldItalic" if found_inter.get("Inter-BoldItalic") else bold
        for base in (regular, "Inter-Light"):
            pdfmetrics.registerFontFamily(
                base, normal=base, bold=bold, italic=italic, boldItalic=bold_italic)
        print(f"[fonts] using Inter (fallback)")
        return FontFamily(
            name="Inter", light="Inter-Light", regular=regular, bold=bold,
            italic=italic, bold_italic=bold_italic, is_brand_primary=False,
        )

    warnings.warn("HARD FALLBACK to Helvetica; install Akkurat Pro at ~/Library/Fonts/")
    return FontFamily(
        name="Helvetica", light="Helvetica", regular="Helvetica",
        bold="Helvetica-Bold", italic="Helvetica-Oblique",
        bold_italic="Helvetica-BoldOblique", is_brand_primary=False,
    )


# ---------------------------------------------------------------------------
# Paragraph styles (verbatim from v21)
# ---------------------------------------------------------------------------

def build_paragraph_styles(font: FontFamily, palette: BrandPalette,
                           tokens: dict) -> dict[str, ParagraphStyle]:
    by_name = {ps["name"]: ps for ps in tokens.get("paragraph_styles", [])}

    def fill_to_hex(fill_color: str) -> str:
        if fill_color in ("Color/Black", "Color/C=25 M=25 Y=25 K=100"):
            return palette.soft_black
        if fill_color == "Color/C=0 M=100 Y=90 K=0":
            return palette.template_red_override
        if fill_color == "Color/Paper":
            return palette.paper
        return palette.soft_black

    def font_for_style(style_name: str, font_style: str) -> str:
        s = font_style.lower()
        if "bold" in s and "italic" in s:
            return font.bold_italic
        if "italic" in s:
            return font.italic
        if "bold" in s:
            return font.bold
        if "light" in s:
            return font.light
        return font.regular

    def make(alias: str, src_name: str, **overrides) -> ParagraphStyle:
        src = by_name.get(src_name, {})
        kwargs = dict(
            name=alias,
            fontName=overrides.get("fontName") or font_for_style(
                src_name, src.get("FontStyle", "Regular")),
            fontSize=overrides.get("fontSize", src.get("PointSize", 10)),
            leading=overrides.get("leading", src.get("Leading", 12)),
            textColor=HexColor(overrides.get("textColor")
                              or fill_to_hex(src.get("FillColor", "Color/Black"))),
            spaceAfter=overrides.get("spaceAfter", src.get("SpaceAfter", 0)),
            spaceBefore=overrides.get("spaceBefore", src.get("SpaceBefore", 0)),
            alignment=overrides.get("alignment", 0),
            firstLineIndent=overrides.get("firstLineIndent", 0),
            allowWidows=1,
            allowOrphans=0,
        )
        if "wordWrap" in overrides and overrides["wordWrap"] is not None:
            kwargs["wordWrap"] = overrides["wordWrap"]
        return ParagraphStyle(**kwargs)

    P = "Marketing Literature Styles:"

    return {
        "cover_title": make("cover_title", P + "A_Brochure Title 40/40",
                            textColor=palette.indigo,
                            fontName=font.bold,
                            fontSize=44, leading=44, spaceAfter=10),
        "cover_subtitle": make("cover_subtitle", P + "A_Brochure Subtile 18/20",
                                textColor=palette.indigo,
                                fontName=font.bold,
                                fontSize=18, leading=22, spaceAfter=6),
        "cover_meta": make("cover_meta", P + "C_Intro Copy 1 12/15",
                           fontName=font.regular,
                           fontSize=11, leading=14, spaceAfter=4),
        "cover_byline": make("cover_byline", P + "C_Intro Copy 1 12/15",
                              fontName=font.regular,
                              fontSize=10, leading=13, spaceAfter=2),
        "cover_tagline": make("cover_tagline", P + "H_Callout 1 20/22",
                               textColor=palette.indigo,
                               fontName=font.bold,
                               fontSize=20, leading=24),
        "standfirst": make("standfirst", P + "H_Callout 1 20/22",
                           textColor=palette.indigo,
                           fontName=font.bold,
                           fontSize=24, leading=28, spaceAfter=14),
        "lead_deck": make("lead_deck", P + "A_Bruchure Summary 11/14",
                          fontSize=14, leading=18, spaceAfter=14,
                          fontName=font.light),
        "h1": make("h1", P + "B_Heading Level 1 33/33",
                   textColor=palette.indigo,
                   fontName=font.bold,
                   fontSize=22, leading=24, spaceAfter=10, spaceBefore=4),
        "h2": make("h2", P + "B_Heading Level 2 14/17",
                   fontName=font.bold,
                   fontSize=14, leading=17, spaceAfter=8, spaceBefore=14),
        "subhead": make("subhead", P + "D_Subheading Level 1 16/18",
                         textColor=palette.indigo,
                         fontName=font.bold,
                         fontSize=14, leading=17, spaceAfter=6, spaceBefore=10),
        "intro": make("intro", P + "C_Intro Copy 1 12/15",
                      fontName=font.regular,
                      fontSize=11, leading=14, spaceAfter=8),
        "body": make("body", P + "E_Body Copy 1 9/12",
                     fontName=font.light,
                     fontSize=9.4, leading=13.2, spaceAfter=6.5),
        "body_lead": make("body_lead", P + "C_Intro Copy 1 12/15",
                           fontName=font.regular,
                           fontSize=10, leading=13.5, spaceAfter=6),
        "pattern_number": make("pattern_number", P + "D_Subheading Level 1 16/18",
                                textColor=palette.indigo,
                                fontName=font.bold,
                                fontSize=10, leading=12,
                                spaceAfter=2),
        "pattern_title": make("pattern_title", P + "B_Heading Level 1 33/33",
                               textColor=palette.indigo,
                               fontName=font.bold,
                               fontSize=20, leading=22, spaceAfter=12),
        "caption": make("caption", P + "G_Charts Copy 2 9/12",
                        fontName=font.regular,
                        fontSize=8, leading=10, spaceAfter=4),
        "hero_caption": make("hero_caption", P + "G_Charts Copy 2 9/12",
                              fontName=font.regular,
                              fontSize=9.5, leading=13, spaceAfter=4),
        "footer": make("footer", P + "I_Disclaimer/Footnotes 7.5/9.5",
                       fontName=font.light,
                       fontSize=7, leading=9.5),
        "disclaimer": make("disclaimer", P + "I_Disclaimer/Footnotes 7.5/9.5",
                            fontName=font.light,
                            fontSize=7.5, leading=10, spaceAfter=4),
    }


# ---------------------------------------------------------------------------
# Chart slot tracker + reservation Flowable (verbatim from v21)
# ---------------------------------------------------------------------------

@dataclass
class ChartSlot:
    slot_key: str
    chart_path: Path
    page_index: int
    x_pt: float
    y_pt: float
    w_pt: float
    h_pt: float


@dataclass
class ChartManifest:
    slots: list[ChartSlot] = field(default_factory=list)

    def add(self, key: str, chart_path: Path, page_index: int,
            x_pt: float, y_pt: float, w_pt: float, h_pt: float) -> None:
        self.slots.append(ChartSlot(
            slot_key=key, chart_path=chart_path,
            page_index=page_index,
            x_pt=x_pt, y_pt=y_pt, w_pt=w_pt, h_pt=h_pt,
        ))


class ChartReservation(Flowable):
    def __init__(self, slot_key: str, chart_path: Path,
                 width_in: float, height_in: float,
                 manifest: ChartManifest, debug: bool = False,
                 caption: str | None = None,
                 caption_style: ParagraphStyle | None = None,
                 hAlign: str = 'LEFT'):
        Flowable.__init__(self)
        self.slot_key = slot_key
        self.chart_path = chart_path

        # Compute requested slot dimensions with page-content clamps applied.
        requested_w_pt = min(width_in * 72.0, CHART_RESERVATION_WIDTH_CLAMP_PT)
        raw_h_pt = height_in * 72.0
        requested_h_pt = 400.0 if raw_h_pt > CHART_RESERVATION_HEIGHT_CLAMP_PT else raw_h_pt

        # Pre-compute the chart's actual rendered footprint at proportional
        # fit-to-clamps. Sizing the reservation to match the rendered chart
        # eliminates the chart-caption vertical gap that arose when the
        # reserved slot exceeded the chart's actual size after fit-scaling.
        # Without this pre-compute, slot reservation = figsize but actual
        # chart = figsize × min(sx, sy) × overlay_padding — leaving white
        # space inside slot, BETWEEN chart bottom and caption.
        try:
            reader = PdfReader(str(chart_path))
            cb = reader.pages[0].mediabox
            chart_w_native = float(cb.width)
            chart_h_native = float(cb.height)
            fit_scale = min(requested_w_pt / chart_w_native,
                            requested_h_pt / chart_h_native)
            self.chart_w_pt = chart_w_native * fit_scale
            self.chart_h_pt = chart_h_native * fit_scale
        except Exception:
            # Fallback to requested dimensions if PDF read fails.
            self.chart_w_pt = requested_w_pt
            self.chart_h_pt = requested_h_pt
        self.manifest = manifest
        self.debug = debug
        self.caption_p = (Paragraph(caption, caption_style)
                          if caption and caption_style else None)
        self.hAlign = hAlign
        self._caption_h = 0.0
        self._caption_w = 0.0
        self.drawWidth = self.chart_w_pt
        self.drawHeight = self.chart_h_pt
        self.imageWidth = self.drawWidth
        self.imageHeight = self.drawHeight

    def _restrictSize(self, aW, aH):
        return self.drawWidth, self.drawHeight

    def _unRestrictSize(self):
        pass

    def wrap(self, available_w, available_h):
        reported_w = min(self.chart_w_pt, available_w)
        if self.caption_p is not None:
            cw, ch = self.caption_p.wrap(reported_w, available_h)
            self._caption_w, self._caption_h = cw, ch
            total_h = self.chart_h_pt + ch + 4
            self.drawWidth = reported_w
            self.drawHeight = total_h
            self.imageWidth = reported_w
            self.imageHeight = total_h
            return reported_w, total_h
        self.drawWidth = reported_w
        self.drawHeight = self.chart_h_pt
        self.imageWidth = reported_w
        self.imageHeight = self.chart_h_pt
        return reported_w, self.chart_h_pt

    def draw(self):
        c = self.canv
        x_page, y_page = c.absolutePosition(0, 0)
        chart_y_local = self._caption_h + 4 if self.caption_p else 0
        chart_y_page = y_page + chart_y_local
        chart_x_page = x_page
        page_index = c.getPageNumber() - 1

        self.manifest.add(
            key=self.slot_key,
            chart_path=self.chart_path,
            page_index=page_index,
            x_pt=chart_x_page,
            y_pt=chart_y_page,
            w_pt=self.chart_w_pt,
            h_pt=self.chart_h_pt,
        )

        if self.debug:
            c.saveState()
            c.setStrokeColorRGB(0.7, 0.7, 0.85)
            c.setLineWidth(0.3)
            c.setDash(2, 2)
            c.rect(0, chart_y_local, self.chart_w_pt, self.chart_h_pt, stroke=1, fill=0)
            c.restoreState()

        if self.caption_p is not None:
            self.caption_p.drawOn(c, 0, 0)


# ---------------------------------------------------------------------------
# DocTemplate (functionally verbatim from v21; only header right text + title
# changed)
# ---------------------------------------------------------------------------

class V15DocTemplate(BaseDocTemplate):

    def __init__(self, filename: str, *,
                 palette: BrandPalette, font: FontFamily,
                 styles: dict[str, ParagraphStyle],
                 manifest: ChartManifest, debug_layout: bool = False, **kw):
        super().__init__(filename, pagesize=LETTER,
                         leftMargin=MARGIN, rightMargin=MARGIN,
                         topMargin=MARGIN, bottomMargin=MARGIN,
                         showBoundary=0, **kw)
        self.palette = palette
        self.font = font
        self.styles = styles
        self.manifest = manifest
        self.debug_layout = debug_layout

        cover_frame = Frame(MARGIN, MARGIN, CONTENT_W, CONTENT_H,
                             leftPadding=0, rightPadding=0,
                             topPadding=0, bottomPadding=0,
                             showBoundary=0, id="cover")

        FOOTER_BAND_H = 30
        HEADER_BAND_H = 24
        body_top_y = MARGIN + FOOTER_BAND_H
        body_h = CONTENT_H - FOOTER_BAND_H - HEADER_BAND_H
        body_left_frame = Frame(BODY_LEFT_X, body_top_y, BODY_LEFT_W, body_h,
                                 leftPadding=0, rightPadding=0,
                                 topPadding=0, bottomPadding=0,
                                 showBoundary=0, id="body_left")
        body_right_frame = Frame(BODY_RIGHT_X, body_top_y, BODY_RIGHT_W, body_h,
                                  leftPadding=0, rightPadding=0,
                                  topPadding=0, bottomPadding=0,
                                  showBoundary=0, id="body_right")
        spread_frame = Frame(MARGIN, body_top_y, CONTENT_W, body_h,
                              leftPadding=0, rightPadding=0,
                              topPadding=0, bottomPadding=0,
                              showBoundary=0, id="spread")

        LEAD_TOP_H = 396.0
        lead_top_frame = Frame(MARGIN, body_top_y + (body_h - LEAD_TOP_H),
                               CONTENT_W, LEAD_TOP_H,
                               leftPadding=0, rightPadding=0,
                               topPadding=0, bottomPadding=0,
                               showBoundary=0, id="lead_top")
        lead_bottom_h = body_h - LEAD_TOP_H
        lead_bottom_left_frame = Frame(BODY_LEFT_X, body_top_y,
                                       BODY_LEFT_W, lead_bottom_h,
                                       leftPadding=0, rightPadding=0,
                                       topPadding=0, bottomPadding=0,
                                       showBoundary=0, id="lead_bottom_left")
        lead_bottom_right_frame = Frame(BODY_RIGHT_X, body_top_y,
                                        BODY_RIGHT_W, lead_bottom_h,
                                        leftPadding=0, rightPadding=0,
                                        topPadding=0, bottomPadding=0,
                                        showBoundary=0, id="lead_bottom_right")

        self.addPageTemplates([
            PageTemplate(id="cover", frames=[cover_frame],
                         onPage=self._cover_decoration),
            PageTemplate(id="body", frames=[body_left_frame, body_right_frame],
                         onPage=self._body_chrome),
            PageTemplate(id="lead",
                         frames=[lead_top_frame,
                                 lead_bottom_left_frame,
                                 lead_bottom_right_frame],
                         onPage=self._body_chrome),
            PageTemplate(id="spread", frames=[spread_frame],
                         onPage=self._body_chrome),
            PageTemplate(id="closing", frames=[
                Frame(MARGIN, MARGIN, CONTENT_W, CONTENT_H,
                      leftPadding=0, rightPadding=0,
                      topPadding=0, bottomPadding=0,
                      showBoundary=0, id="closing")],
                         onPage=self._body_chrome),
        ])

    def _cover_decoration(self, canvas: Canvas, doc):
        c = canvas
        c.saveState()
        c.setFillColor(HexColor(self.palette.paper))
        c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
        if LOCKUP_SVG.exists():
            self._draw_lockup_top(c, LOCKUP_SVG, x=MARGIN, y=PAGE_H - MARGIN - 36, height=36)
        else:
            self._draw_lockup_text_fallback(c, x=MARGIN, y=PAGE_H - MARGIN - 36)
        c.setFillColor(HexColor(self.palette.soft_black))
        c.setFont(self.font.regular, 8)
        c.drawString(MARGIN, MARGIN + 8, content_meta_line(self))
        c.restoreState()

    def _body_chrome(self, canvas: Canvas, doc):
        c = canvas
        c.saveState()
        header_y = PAGE_H - MARGIN + 14
        if WORDMARK_SVG.exists():
            self._draw_wordmark_top(c, WORDMARK_SVG, x=MARGIN, y=header_y - 10, height=10)
        else:
            c.setFont(self.font.bold, 9)
            c.setFillColor(HexColor(self.palette.indigo))
            c.drawString(MARGIN, header_y - 8, "Third System")

        c.setFont(self.font.regular, 7.5)
        c.setFillColor(HexColor(self.palette.soft_black))
        # AIAS 1.0 header right text — synthesis report identifier
        c.drawRightString(PAGE_W - MARGIN, header_y - 8,
                           "AIAS 1.0 · Five-Substrate Synthesis · May 2026")

        footer_y = MARGIN - 18
        c.setFont(self.font.light, 7)
        c.setFillColor(HexColor(self.palette.soft_black))
        footer_text = (
            "© 2026 Third System.  "
            "Methodology and underlying datasets: thirdsystem.ai/methodology.  "
            "Inquiries: hello@thirdsystem.ai.  "
            "Findings may be cited with attribution."
        )
        c.drawString(MARGIN, footer_y, footer_text)
        c.drawRightString(PAGE_W - MARGIN, footer_y, f"{doc.page}")
        c.restoreState()

    def _draw_wordmark_top(self, c, svg_path, x, y, height):
        c.saveState()
        c.setFillColor(HexColor(self.palette.indigo))
        c.setFont(self.font.bold, height)
        c.drawString(x, y, "Third System")
        c.restoreState()

    def _draw_lockup_top(self, c, svg_path, x, y, height):
        c.saveState()
        line_h = height / 2.6
        c.setFillColor(HexColor(self.palette.indigo))
        c.setFont(self.font.bold, line_h * 1.4)
        c.drawString(x, y + line_h * 0.9, "Third System")
        c.setFillColor(HexColor(self.palette.soft_black))
        c.setFont(self.font.regular, line_h * 1.1)
        c.drawString(x, y - line_h * 0.4, "AI Presence Index")
        c.restoreState()

    def _draw_lockup_text_fallback(self, c, x, y):
        c.saveState()
        c.setFillColor(HexColor(self.palette.indigo))
        c.setFont(self.font.bold, 14)
        c.drawString(x, y + 14, "Third System")
        c.setFillColor(HexColor(self.palette.soft_black))
        c.setFont(self.font.regular, 11)
        c.drawString(x, y, "AI Presence Index")
        c.restoreState()


def content_meta_line(doc: V15DocTemplate) -> str:
    return "thirdsystem.ai · hello@thirdsystem.ai · " + content.COVER["date"]


# ---------------------------------------------------------------------------
# Story builders (forked from v21; PATTERNS loop unchanged, slot resolver
# extended to handle multi-subdir chart layout)
# ---------------------------------------------------------------------------

def build_cover_story(styles: dict[str, ParagraphStyle]) -> list:
    s = []
    s.append(Spacer(1, CONTENT_H * 0.30))
    s.append(Paragraph(content.COVER["title"], styles["cover_title"]))
    s.append(Paragraph(content.COVER["subtitle"], styles["cover_subtitle"]))
    s.append(Spacer(1, 18))
    s.append(Paragraph(
        f"{content.COVER['date']} &nbsp;&nbsp;·&nbsp;&nbsp; "
        f"{content.COVER['byline_short']}",
        styles["cover_byline"]))
    s.append(Spacer(1, CONTENT_H * 0.10))
    s.append(Paragraph(content.COVER["tagline"], styles["cover_tagline"]))
    return s


def build_lead_story(styles: dict[str, ParagraphStyle]) -> list:
    s = []
    s.append(Paragraph(content.STANDFIRST, styles["standfirst"]))
    s.append(FrameBreak())
    s.append(Paragraph(content.LEAD_DECK, styles["lead_deck"]))
    s.append(Spacer(1, 4))
    s.append(NextPageTemplate("body"))
    for p in content.EXEC_SUMMARY:
        s.append(Paragraph(p, styles["body"]))
    return s


def build_what_we_measured_story(styles: dict[str, ParagraphStyle]) -> list:
    s = []
    s.append(Paragraph(content.WHAT_WE_MEASURED["heading"], styles["h2"]))
    for p in content.WHAT_WE_MEASURED["paragraphs"]:
        s.append(Paragraph(p, styles["body"]))
    return s


# AIAS 1.0 brand-format report figure captions for the 4 chart slots.
# P5 is text-only and has no caption entry. Captions translate the
# academic chart content to managerial register for non-academic readers.
HERO_FIGURE_CAPTIONS = {
    "f1_anchor_base": (
        "Figure 1 · Cumulative substrate-family anchor base, "
        "v0.16 → v0.21. Six pre-registered measurement events "
        "between March and May 2026 anchor the AIAS™ Presence "
        "Measurement Protocol across five substrate families: "
        "kitchenware (v0.16 + v0.17), indie fragrance (v0.18), "
        "audiophile electronics (v0.19), skincare (v0.20), and "
        "cosmetics (v0.21). All five families measured under one "
        "locked methodology version (v1.6, SSRN 6816340). The "
        "anchor-base completion changes the construct's standing "
        "from one-or-two-substrate-anchored to cross-category "
        "measurable under pre-registration discipline."
    ),
    "f2_phantom_channel": (
        "Figure 2 · Off-panel channel signature on v0.21 "
        "cosmetics. Six off-panel brands cleared the K = 6 "
        "persistence threshold; three of six are channel-pure. "
        "Estée Lauder (R_cat = 13) and Clinique (R_cat = 6) "
        "appear exclusively in canonical-channel frames — the "
        "authority pathway: prestige and heritage cosmetics. "
        "Glossier (R_cult = 12) appears exclusively in cultural-"
        "channel frames — the discourse pathway: celebrity, "
        "DTC, and cult brands. The channel signature tracks the "
        "brands' Identity Load, with the same gradient operating on "
        "off-panel brands as on the panel-internal brands (Finding "
        "04). Glossier was pre-registered as the validity anchor and "
        "passed at R_phantom = 12, well clear of the K = 6 threshold."
    ),
    "f3_type2_emergence": (
        "Figure 3 · Type 2 quadrant cross-phase emergence: "
        "v0.20 PARTIAL → v0.21 EMERGED. The Type 2 cultural-"
        "channel-preferred quadrant (R_cat ≤ 2 ∧ R_cult "
        "≥ 5) cleared the EMERGED threshold for the first time "
        "at v0.21 cosmetics with three Cell B cases: Rare Beauty "
        "(R_cat = 1, R_cult = 17 — the program's textbook "
        "Recognition × Recall dissociation case), Huda Beauty "
        "(0:11), and Kylie Cosmetics (0:5). v0.20 skincare returned "
        "PARTIAL on the same test with two Cell B cases below the "
        "EMERGED threshold of 3. Two cross-phase out-of-cell Type 2 "
        "anchors — La Mer (v0.20 Cell A) and e.l.f. Cosmetics "
        "(v0.21 Cell C) — establish out-of-cell Type 2 as a "
        "recurrent feature of the dissociation pattern across "
        "substrate families."
    ),
    "f4_il_direct_forest": (
        "Figure 4 · Identity-Load moderator δ values "
        "across v0.20 + v0.21 with 95% bootstrap confidence "
        "intervals. δ = mean(R_cult) − mean(R_cat) per "
        "cell; positive values indicate cultural-channel lead, "
        "negative values indicate canonical-channel lead. v0.21 "
        "cosmetics returned the program's first CONFIRMED moderator "
        "verdict at any layer: Cell B δ = +7.13 (CI [+4.75, "
        "+10.25]) excludes zero in IL-predicted direction; Cell A "
        "δ = −3.13 (CI [−6.00, −0.25]) excludes "
        "zero in opposite direction as IL gradient predicts; Cell C "
        "δ = +1.00 (CI [−0.50, +3.25]) between Cell A and "
        "Cell B, satisfying monotonic-gradient check. v0.20 skincare "
        "PARTIAL on the same test with substrate-specific Cell A "
        "architecture (clinical authority lives in mass tier, not "
        "prestige)."
    ),
}


def _slot_lookup(slot_key: str) -> tuple[str | None, str | None]:
    """Map an AIAS 1.0 brand-format slot_key to (relative_path, figsize_key).

    Relative path is relative to ~/aias/reports/. Charts live in two
    subdirs: figs/aias_1_0/ for the 3 re-used synthesis paper charts;
    figs/aias_1_0_report/ for the P2 brand-format upgrade.

    P5 has chart_slot=None and is not in this table (text-only finding).
    """
    table = {
        "f1_anchor_base": (
            "figs/aias_1_0/chart_02_anchor_base_lineage.pdf",
            "aias_1_0_anchor_base",
        ),
        "f2_phantom_channel": (
            "figs/aias_1_0_report/chart_p2_phantom_channel_brand_format.pdf",
            "aias_1_0_phantom_channel",
        ),
        "f3_type2_emergence": (
            "figs/aias_1_0/chart_04_type2_emergence.pdf",
            "aias_1_0_type2_emergence",
        ),
        "f4_il_direct_forest": (
            "figs/aias_1_0/chart_05_il_direct_forest.pdf",
            "aias_1_0_il_direct_forest",
        ),
    }
    return table.get(slot_key, (None, None))


def build_pattern_unified(pattern: dict, styles: dict,
                            manifest: ChartManifest,
                            reports_dir: Path, debug: bool) -> list:
    """v0.14+ vertical-flow pattern: heading -> text (2-col balanced) -> chart below.

    P5 (Finding 05) is text-only: chart_slot=None, no chart_block built.
    """
    slot = pattern.get("chart_slot")

    chart_path = None
    figsize_key = None
    if slot:
        relpath, figsize_key = _slot_lookup(slot)
        if relpath:
            chart_path = reports_dir / relpath
            if not chart_path.exists():
                warnings.warn(
                    f"Pattern {pattern['number']} chart missing "
                    f"({relpath}); rendering body without chart."
                )
                chart_path = None

    s: list = []
    s.append(PageBreak())

    # Build chart_block before assembling the heading so we can wrap
    # heading + chart in a single KeepTogether (prevents orphan heading
    # pages where chart breaks to next page leaving heading isolated).
    chart_block: list = []
    if chart_path is not None and figsize_key is not None:
        w_in, h_in = CHART_FIGSIZE_IN[figsize_key]
        # AIAS 1.0 brand-format report hero slot names — 4 chart slots;
        # P5 (no chart) is not in this set.
        is_hero = slot in (
            "f1_anchor_base",
            "f2_phantom_channel",
            "f3_type2_emergence",
            "f4_il_direct_forest",
        )
        caption_style = styles["hero_caption"] if is_hero else styles["caption"]
        caption_text = HERO_FIGURE_CAPTIONS.get(slot, f"Figure {pattern['number']}.")
        chart_res = ChartReservation(
            slot, chart_path, w_in, h_in, manifest,
            debug=debug, caption=caption_text, caption_style=caption_style,
        )
        chart_block = [chart_res]

    paragraphs = [Paragraph(p, styles["body"]) for p in pattern["paragraphs"]]
    text_block: list = []
    if paragraphs:
        text_block = [BalancedColumns(
            paragraphs, nCols=2, innerPadding=GUTTER,
            spaceBefore=4, spaceAfter=10, needed=30,
        )]

    _flag = pattern.get("chart_after_text", False)
    print(f"[pattern {pattern['number']}] chart_after_text={_flag} "
          f"order={'text-then-chart' if _flag else 'chart-then-text'}")

    heading_items = [
        Spacer(1, 4),
        Paragraph(f"FINDING {pattern['number']:02d}", styles["pattern_number"]),
        Paragraph(pattern["title"], styles["pattern_title"]),
    ]

    if _flag:
        # text-then-chart mode: heading-only KeepTogether (chart isn't
        # adjacent to heading; orphan heading is fine because text follows).
        s.append(KeepTogether(heading_items))
        s.extend(text_block)
        s.extend(chart_block)
    else:
        # chart-then-text mode (default for AIAS 1.0): heading + chart wrapped
        # in single KeepTogether so they break together to next page if needed.
        # Prevents the orphan-heading-page failure where chart pushes to next
        # page leaving heading alone (visible in r1 on pages 9/12/15).
        s.append(KeepTogether(heading_items + chart_block))
        s.extend(text_block)

    return s


def build_proposition_scoring_story(styles: dict) -> list:
    """Renames v21's build_hypothesis_scoring_story. Column header H -> P;
    pulls content.PROPOSITION_SCORING + content.PROPOSITION_DETAILS instead
    of content.HYPOTHESIS_SCORING + content.HYPOTHESIS_DETAILS. Preserves
    v21's row-format and table styling."""
    s = []
    s.append(Spacer(1, 4))
    s.append(Paragraph(content.PROPOSITION_SCORING["heading"], styles["h1"]))
    s.append(Spacer(1, 4))
    s.append(Paragraph(content.PROPOSITION_SCORING["intro"], styles["body_lead"]))
    s.append(Spacer(1, 10))

    header_style = ParagraphStyle(
        "scoring_header", parent=styles["body"],
        fontName=styles["body"].fontName.replace("Regular", "Bold")
                 if "Regular" in styles["body"].fontName else styles["body"].fontName,
        fontSize=8.5, textColor=HexColor("#37237B"), leading=11,
    )
    cell_style = ParagraphStyle(
        "scoring_cell", parent=styles["body"], fontSize=7.5, leading=10,
    )
    h_cell_style = ParagraphStyle(
        "scoring_h", parent=cell_style, fontName=header_style.fontName,
    )
    status_styles = {
        "confirmed": ParagraphStyle(
            "status_confirmed", parent=cell_style, fontName=header_style.fontName),
        "partial": cell_style,
        "disconfirmed": cell_style,
        "descriptive": ParagraphStyle(
            "status_descriptive", parent=cell_style, fontName=cell_style.fontName),
    }

    # P (propositions) column header — was "H" in v21
    table_data = [[
        Paragraph("<b>P</b>", header_style),
        Paragraph("<b>Proposition</b>", header_style),
        Paragraph("<b>What the data shows</b>", header_style),
        Paragraph("<b>Status</b>", header_style),
    ]]
    for p_id, proposition, result, status_text, status_class in content.PROPOSITION_SCORING["rows"]:
        st_style = status_styles.get(status_class, cell_style)
        if status_class == "confirmed":
            status_para = Paragraph(f"<b>{status_text}</b>", st_style)
        elif status_class == "descriptive":
            status_para = Paragraph(f"<i>{status_text}</i>", st_style)
        else:
            status_para = Paragraph(status_text, st_style)
        table_data.append([
            Paragraph(f"<b>{p_id}</b>", h_cell_style),
            Paragraph(proposition, cell_style),
            Paragraph(result, cell_style),
            status_para,
        ])

    indigo = HexColor("#37237B")
    lavender = HexColor("#BBB9DD")
    tbl = Table(
        table_data,
        colWidths=[44, 165, 195, 136],
        style=TableStyle([
            ("LINEABOVE",  (0, 0), (-1, 0), 1.2, indigo),
            ("LINEBELOW",  (0, 0), (-1, 0), 0.5, indigo),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 5),
            ("TOPPADDING",    (0, 0), (-1, 0), 5),
            ("LINEBELOW",  (0, 1), (-1, -2), 0.3, lavender),
            ("BOTTOMPADDING", (0, 1), (-1, -1), 4),
            ("TOPPADDING",    (0, 1), (-1, -1), 4),
            ("LINEBELOW",  (0, -1), (-1, -1), 1.2, indigo),
            ("VALIGN",     (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING",  (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ]),
    )
    s.append(tbl)

    if hasattr(content, "PROPOSITION_DETAILS"):
        details = content.PROPOSITION_DETAILS
        s.append(Spacer(1, 14))
        s.append(KeepTogether([
            Paragraph(details["heading"], styles["h2"]),
            Spacer(1, 4),
            Paragraph(details["intro"], styles["body_lead"]),
        ]))
        s.append(Spacer(1, 8))

        p_paragraphs = [Paragraph(body, styles["body"])
                         for p_id, body in details["items"]]
        s.append(BalancedColumns(
            p_paragraphs, nCols=2, innerPadding=GUTTER,
            spaceBefore=4, spaceAfter=8,
        ))

    return s


def build_limitations_story(styles: dict) -> list:
    s = []
    s.append(Spacer(1, 4))
    s.append(Paragraph(content.LIMITATIONS["heading"], styles["h1"]))
    for p in content.LIMITATIONS["paragraphs"]:
        s.append(Paragraph(p, styles["body"]))
    return s


def build_whats_next_story(styles: dict) -> list:
    s = []
    s.append(Spacer(1, 4))
    s.append(Paragraph(content.WHATS_NEXT["heading"], styles["h1"]))
    for p in content.WHATS_NEXT["paragraphs"]:
        s.append(Paragraph(p, styles["body"]))
    return s


def build_closing_story(styles: dict, brand: dict) -> list:
    s = []
    s.append(Spacer(1, CONTENT_H * 0.04))

    s.append(Paragraph("About the Third System", styles["h1"]))
    s.append(Spacer(1, 4))
    s.append(Paragraph(boilerplate.SYSTEM_OVERVIEW["medium"], styles["body_lead"]))
    s.append(Spacer(1, 16))

    s.append(Paragraph("<b>Authored by</b>", styles["body_lead"]))
    for line in content.CLOSING["byline_long"]:
        s.append(Paragraph(line, styles["body"]))
    s.append(Spacer(1, 10))

    # AIAS 1.0 protocol version — synthesis under v1.6 lock
    REPORT_PROTOCOL_VERSION = "v1.6"
    methodology_text = brand["disclaimers"]["methodology_standard"].replace(
        "(current: v0.3)",
        f"(current: {REPORT_PROTOCOL_VERSION})",
    )
    s.append(Paragraph("<b>Methodology</b>", styles["body_lead"]))
    s.append(Paragraph(methodology_text, styles["disclaimer"]))
    s.append(Spacer(1, 10))

    s.append(Paragraph("<b>Citation</b>", styles["body_lead"]))
    # AIAS 1.0 synthesis citation — references SSRN 6817841
    citation_text = (
        "Gonzalez Castro, P. U. (2026). "
        "<i>AI Availability as a Third Measurable Layer of Brand "
        "Availability: Five-Substrate Empirical Anchoring of the "
        "AIAS™ Presence Measurement Protocol</i> (AIAS 1.0). "
        "Third System. thirdsystem.ai/aias-1-0 "
        "(academic companion: SSRN 6817841)"
    )
    s.append(Paragraph(citation_text, styles["disclaimer"]))
    s.append(Spacer(1, 10))

    s.append(Paragraph("<b>Underlying datasets</b>", styles["body_lead"]))
    for ds in content.CLOSING["datasets"]:
        s.append(Paragraph(ds, styles["disclaimer"]))
    s.append(Spacer(1, 10))

    s.append(Paragraph(
        f"<b>Methodology log:</b> {content.CLOSING['methodology_log']}.",
        styles["disclaimer"]))
    s.append(Paragraph("<b>Inquiries:</b> hello@thirdsystem.ai", styles["disclaimer"]))
    return s


# ---------------------------------------------------------------------------
# Pass 2 overlay (verbatim from v21)
# ---------------------------------------------------------------------------

def overlay_charts(base_pdf_path: Path, manifest: ChartManifest,
                    out_pdf_path: Path) -> None:
    reader = PdfReader(str(base_pdf_path))
    writer = PdfWriter(clone_from=reader)

    for slot in manifest.slots:
        if not slot.chart_path.exists():
            warnings.warn(f"Skipping merge for missing {slot.chart_path.name}; "
                          f"the page reservation remains blank.")
            continue
        chart_reader = PdfReader(str(slot.chart_path))
        chart_page = chart_reader.pages[0]

        cb = chart_page.mediabox
        chart_w = float(cb.width)
        chart_h = float(cb.height)
        target_w = slot.w_pt
        target_h = slot.h_pt
        sx = target_w / chart_w
        sy = target_h / chart_h
        if abs(sx - sy) / max(sx, sy) > 0.02:
            warnings.warn(
                f"Chart {slot.chart_path.name} aspect mismatch: "
                f"chart {chart_w:.1f}x{chart_h:.1f}pt, reservation "
                f"{target_w:.1f}x{target_h:.1f}pt. Stretching to fit."
            )
        # Scale chart to fill slot exactly (slot is pre-sized to chart's
        # actual rendered footprint in ChartReservation.__init__).
        # Removed the historical 0.92 padding factor; with slot now matching
        # the chart's fit-to-clamps dimensions, the padding produced visible
        # chart-caption gaps that were not acceptable for the synthesis
        # report. Chart now sits flush within slot; caption is immediately
        # below the chart with only the 4pt internal flowable padding.
        scale = min(sx, sy)
        offset_x = slot.x_pt + (target_w - chart_w * scale) / 2
        if slot.h_pt > 350.0:
            offset_y = slot.y_pt + (target_h - chart_h * scale)
        else:
            offset_y = slot.y_pt + (target_h - chart_h * scale) / 2
        op = Transformation().scale(scale, scale).translate(offset_x, offset_y)
        writer.pages[slot.page_index].merge_transformed_page(chart_page, op)

    with open(out_pdf_path, "wb") as f:
        writer.write(f)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def build(*, debug_layout: bool = False,
          output_path: Path | None = None) -> Path:
    with open(BRAND_JSON) as f:
        brand = json.load(f)
    with open(TOKENS_JSON) as f:
        tokens = json.load(f)

    palette = BrandPalette.from_json(brand)
    font = register_typography()
    styles = build_paragraph_styles(font, palette, tokens)

    print(f"[build_report_aias_1_0] palette: indigo={palette.indigo}, "
          f"soft_black={palette.soft_black}, paper={palette.paper}")
    print(f"[build_report_aias_1_0] typography: {font.name} "
          f"(brand_primary={font.is_brand_primary})")

    AIAS_DEPOSIT_ROOT = AIAS_ROOT / "osf" / "aias_1_0"
    output_path = output_path or (
        AIAS_DEPOSIT_ROOT / "reports" / "aias_1_0_brand_format_report.pdf"
    )
    base_pdf = output_path.parent / "_aias_1_0_base.pdf"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"[build_report_aias_1_0] chart pre-flight (reports/-rooted relative paths)")
    expected_slots = [
        "f1_anchor_base", "f2_phantom_channel",
        "f3_type2_emergence", "f4_il_direct_forest",
        # P5 is text-only (no chart slot)
    ]
    for sk in expected_slots:
        relpath, _ = _slot_lookup(sk)
        chart_path = REPORTS_DIR / relpath
        present = chart_path.exists()
        status = "FOUND  " if present else "MISSING"
        print(f"  [{status}] {sk:25s} -> {relpath}")

    manifest = ChartManifest()
    doc = V15DocTemplate(
        str(base_pdf),
        palette=palette, font=font, styles=styles,
        manifest=manifest, debug_layout=debug_layout,
        title="AIAS™ 1.0 — Five-Substrate Synthesis",
        author=", ".join(content.CLOSING["byline_long"][:1]),
        subject="Independent measurement for the AI mediation layer.",
    )

    story: list = []

    # --- Cover ---
    story.append(NextPageTemplate("lead"))
    for f_ in build_cover_story(styles):
        story.append(f_)
    story.append(PageBreak())

    # --- Lead spread + exec summary ---
    for f_ in build_lead_story(styles):
        story.append(f_)

    # --- What we measured (methodology) ---
    story.append(NextPageTemplate("body"))
    story.append(PageBreak())
    for f_ in build_what_we_measured_story(styles):
        story.append(f_)

    # --- Findings 1–5 (P1 through P5) ---
    story.append(NextPageTemplate("spread"))
    for pattern in content.PATTERNS:
        story.extend(build_pattern_unified(
            pattern, styles, manifest, REPORTS_DIR, debug_layout))

    # --- Limitations ---
    story.append(NextPageTemplate("body"))
    story.append(PageBreak())
    for f_ in build_limitations_story(styles):
        story.append(f_)

    # --- What's next ---
    story.append(PageBreak())
    for f_ in build_whats_next_story(styles):
        story.append(f_)

    # --- Proposition scoring + details ---
    if hasattr(content, "PROPOSITION_SCORING"):
        story.append(NextPageTemplate("spread"))
        story.append(PageBreak())
        story.extend(build_proposition_scoring_story(styles))

    # --- Closing ---
    story.append(NextPageTemplate("closing"))
    story.append(PageBreak())
    for f_ in build_closing_story(styles, brand):
        story.append(f_)

    doc.build(story)
    print(f"[build_report_aias_1_0] base PDF written: {base_pdf} "
          f"({len(manifest.slots)} chart reservations)")
    for slot in manifest.slots:
        ok = "OK" if slot.chart_path.exists() else "MISSING"
        print(f"  [{ok}] {slot.slot_key:25s} -> page {slot.page_index + 1:>2} "
              f"@({slot.x_pt:6.1f},{slot.y_pt:6.1f}) "
              f"{slot.w_pt:6.1f}x{slot.h_pt:6.1f}pt  ({slot.chart_path.name})")

    overlay_charts(base_pdf, manifest, output_path)
    print(f"[build_report_aias_1_0] FINAL PDF written: {output_path}")

    final_pages = len(PdfReader(str(output_path)).pages)
    print(f"[build_report_aias_1_0] page count: {final_pages}")
    if final_pages < 22 or final_pages > 32:
        warnings.warn(
            f"Page count {final_pages} is outside the 22-32 target band."
        )

    return output_path


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--debug-layout", action="store_true",
                     help="Draw faint borders around chart reservations.")
    ap.add_argument("--output", type=Path, default=None,
                     help="Output PDF path. Defaults to "
                          "~/aias/osf/aias_1_0/reports/aias_1_0_brand_format_report.pdf")
    args = ap.parse_args()
    build(
        debug_layout=args.debug_layout,
        output_path=args.output,
    )
