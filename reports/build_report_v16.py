#!/usr/bin/env python3
"""
v0.16 Panel Expansion Robustness — typesetting pipeline.

Kitchen knives registry-expansion robustness study (panel grew from 16 to 28
brands across six tradition cells; french cell added). Brand-format report
companion to the v0.16 SSRN paper (SSRN forthcoming).

Forked from build_report_v14.py with surgical changes:
  - Imports v16_kitchen_knives_content instead of v14_kitchen_knives_content
  - Section label remains "FINDING"
  - HERO_FIGURE_CAPTIONS replaced with v0.16 brand-format figure captions (5)
  - _slot_lookup table updated for the 5 v0.16 brand-format chart filenames
    (all produced by build_charts_v16.py — single chart-build script for v0.16
    ships both SSRN paper figures and brand-format report figures; adds
    per-tradition small-multiples chart)
  - Slot name reshuffle to match v16 content pattern slots:
      f3_primary_vs_sensitivity -> f3_discourse_language (v0.16 substrate change)
      f3_per_category_rho -> f2_per_category
      f5_per_tradition (NEW)
  - CHART_FIGSIZE_IN extended with v0.16 figsize keys (5 entries)
  - Header right text, citation, output filename, doc metadata updated
  - REPORT_PROTOCOL_VERSION stays at v1.1
  - build_leaderboards_spread returns [] (v0.16, like v0.10–v0.14, has no
    front-of-report hero spread; the five findings carry the narrative directly
    after the exec summary)

Inputs:
  - brand/third_system_brand.json        (v1.5)
  - brand/design_tokens_template.json    (IDML extract)
  - osf/v16/figures/chart_v16_*.pdf      (5 brand-format charts; all from
                                          build_charts_v16.py)

Output:
  - osf/v16/reports/v16_kitchen_knives.pdf

Run for v0.16:
    python3 ~/aias/scripts/build_charts_v16.py
    python3 ~/aias/reports/build_report_v16.py

Locked rules followed (same as v0.6–v0.14):
  - Image-placeholder rectangles in master spreads stay BLANK (no fill colors).
  - Template’s #FF001A red is overridden to brand primary (Indigo #37237B per
    third_system_brand.json v1.5).
  - Akkurat Pro registered when available; Inter as fallback; HARD WARNING
    emitted before any further fallback.
  - Charts embedded at NATIVE figsize from chart_construction_rules; no rescaling.
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

BRAND_JSON = BRAND_DIR / "third_system_brand.json"
TOKENS_JSON = BRAND_DIR / "design_tokens_template.json"
SPECS_JSON = BRAND_DIR / "report_specs.json"
SOURCE_TEXT = BRAND_DIR / "v06_source_text.md"
WORDMARK_SVG = BRAND_DIR / "THIRDSYSTEM_Logo.svg"
LOCKUP_SVG = BRAND_DIR / "THIRDSYSTEM_AIPT_Logo.svg"

# Make `import v14_kitchen_knives_content` work regardless of working directory.
sys.path.insert(0, str(SCRIPT_DIR))
import v16_kitchen_knives_content as content  # noqa: E402
import tsboilerplate as boilerplate  # noqa: E402

# ---------------------------------------------------------------------------
# Page geometry — locked by template content_area
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

# Chart figsize spec (inches). v0.16 brand-format report uses 5 charts at 6-col
# width, with varied heights matching the figsize used in build_charts_v16.py
# (single chart-build script for v0.16 ships both SSRN paper and report figures).
CHART_FIGSIZE_IN = {
    # v0.11 keys kept for cross-version reuse
    "6_col_v11_scatter":    (7.50, 5.00),
    "6_col_v11_rankshift":  (7.50, 6.50),
    "6_col_v11_partial":    (7.50, 5.30),
    # v0.12 keys retained for cross-version cross-reference (not used by v0.16 report)
    "6_col_v12_pm_rankshift":     (7.50, 6.50),
    "6_col_v12_running_partial":  (7.50, 5.80),
    "6_col_v12_scale_mismatch":   (7.50, 6.00),
    "6_col_v12_h6_zones":         (7.50, 4.70),
    # v0.16 brand-format report keys — 5 charts at 6-col width.
    # All produced by build_charts_v16.py (same script ships SSRN paper + report charts).
    "6_col_v16_regime4":            (7.50, 6.50),  # chart_v16_regime4_canonical.pdf (matches render)
    "6_col_v16_per_category":       (7.50, 7.20),  # chart_v16_per_category_rho_comparison.pdf (less stretch; render still 8.0)
    "6_col_v16_discourse_language": (7.50, 4.70),  # chart_v16_discourse_language_pair.pdf (2-panel scatter)
    "6_col_v16_per_brand":          (7.50, 4.20),  # chart_v16_kitchen_knives_per_brand.pdf
    "6_col_v16_per_tradition":      (7.50, 7.20),  # chart_v16_kitchen_knives_per_tradition.pdf (reduced from 8.40 to fit spread frame)
}

BODY_LEFT_X = COL_X[0]
BODY_LEFT_W = span_pts(3)
BODY_RIGHT_X = COL_X[3]
BODY_RIGHT_W = span_pts(3)


# ---------------------------------------------------------------------------
# Brand colors
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
# Font registration (verbatim from build_report_v11.py)
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
# Paragraph styles (verbatim from build_report_v11.py)
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
# Chart slot tracker, reservation Flowable (verbatim from v0.11)
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
        self.chart_w_pt = width_in * 72.0
        self.chart_h_pt = height_in * 72.0
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
# DocTemplate
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

        self.addPageTemplates([
            PageTemplate(id="cover", frames=[cover_frame],
                         onPage=self._cover_decoration),
            PageTemplate(id="body", frames=[body_left_frame, body_right_frame],
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
        c.drawRightString(PAGE_W - MARGIN, header_y - 8,
                           "Panel Expansion Robustness \u00b7 v0.16 \u00b7 14 May 2026")

        footer_y = MARGIN - 18
        c.setFont(self.font.light, 7)
        c.setFillColor(HexColor(self.palette.soft_black))
        footer_text = (
            "\u00a9 2026 Third System.  "
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
    return "thirdsystem.ai \u00b7 hello@thirdsystem.ai \u00b7 " + content.COVER["date"]


# ---------------------------------------------------------------------------
# Story builders (functionally identical to v11; section labels unchanged)
# ---------------------------------------------------------------------------

def build_cover_story(styles: dict[str, ParagraphStyle]) -> list:
    s = []
    s.append(Spacer(1, CONTENT_H * 0.30))
    s.append(Paragraph(content.COVER["title"], styles["cover_title"]))
    s.append(Paragraph(content.COVER["subtitle"], styles["cover_subtitle"]))
    s.append(Spacer(1, 18))
    s.append(Paragraph(
        f"{content.COVER['date']} &nbsp;&nbsp;\u00b7&nbsp;&nbsp; "
        f"{content.COVER['byline_short']}",
        styles["cover_byline"]))
    s.append(Spacer(1, CONTENT_H * 0.18))
    s.append(Paragraph(content.COVER["tagline"], styles["cover_tagline"]))
    return s


def build_lead_story(styles: dict[str, ParagraphStyle]) -> list:
    s = []
    s.append(Paragraph(content.STANDFIRST, styles["standfirst"]))
    s.append(Paragraph(content.LEAD_DECK, styles["lead_deck"]))
    s.append(Spacer(1, 4))
    for p in content.EXEC_SUMMARY:
        s.append(Paragraph(p, styles["body"]))
    return s


def build_what_we_measured_story(styles: dict[str, ParagraphStyle]) -> list:
    s = []
    s.append(Paragraph(content.WHAT_WE_MEASURED["heading"], styles["h2"]))
    for p in content.WHAT_WE_MEASURED["paragraphs"]:
        s.append(Paragraph(p, styles["body"]))
    return s


def build_leaderboards_spread(styles, manifest, chart_dir, debug):
    return []


# Brand-format report figure captions for v0.16 charts.
HERO_FIGURE_CAPTIONS = {
    "f1_regime4_canonical": (
        "Figure 1 \u00b7 H_Regime4_replication_knives CONFIRMED \u2014 Regime 4 holds on the registry-expanded panel. "
        "Each v0.13 + v0.14 + v0.16 category at (bivariate Spearman <font name='Helvetica'>\u03c1</font> "
        "\u00d7 partial <font name='Helvetica'>\u03c1</font>), worldwide, with t<sub size='6'>1</sub>"
        "\u2192t<sub size='6'>2</sub> connectors. The Regime 4 zone is the AIAS Protocol v1.2 \u00a73.4 "
        "canonical definition: |bivariate <font name='Helvetica'>\u03c1</font>| < 0.35 AND partial "
        "<font name='Helvetica'>\u03c1</font> < 0. Kitchen knives (\u2605) sits in Regime 4 at v0.14 "
        "(n = 17) and v0.16 (n = 23); the v0.16 reading deepens the AI \u00d7 Trends decoupling "
        "(bivariate \u22120.150 / \u22120.200 vs v0.14's \u22120.066 / \u22120.134) rather than "
        "regressing it."
    ),
    "f2_per_category": (
        "Figure 2 \u00b7 Per-category construct validity, v0.13 + v0.14 + v0.16. Six categories with "
        "bivariate WW <font name='Helvetica'>\u03c1</font> (indigo), partial WW "
        "<font name='Helvetica'>\u03c1</font> (petro), and bivariate US "
        "<font name='Helvetica'>\u03c1</font> (grey) at t<sub size='6'>1</sub> (open) and "
        "t<sub size='6'>2</sub> (filled). Running anchors the upper end (\u2248 0.80); PM software "
        "at the marginal-direct boundary (\u2248 0.50); skincare and finance show the canonical "
        "Regime 4 pattern; kitchen knives v0.16 (highlighted row) reads the panel-expansion robustness "
        "verdict \u2014 Regime 4 holds with bivariate intensified relative to v0.14."
    ),
    "f3_discourse_language": (
        "Figure 3 \u00b7 H_Discourse_Language_carryforward \u2014 Japanese "
        "tradition cell discourse-language pair scatter. Per-brand AI Presence "
        "under English-anchored prompt (x-axis, knives_b3_en_jp) vs Japanese-"
        "language prompt (y-axis, knives_b4_ja_01). Two panels: t<sub size=\'6\'>1"
        "</sub> (left), t<sub size=\'6\'>2</sub> (right). Spearman "
        "<font name=\'Helvetica\'>\u03c1</font> annotated per panel; identity "
        "line y = x for reference. Verdict zones per pre-reg \u00a72: "
        "<font name=\'Helvetica\'>\u03c1</font> < 0.85 = CARRY-FORWARD "
        "CONFIRMED (v0.8 finding survives v1.2 protocol); "
        "<font name=\'Helvetica\'>\u03c1</font> in [0.85, 0.95) = WEAKENED; "
        "<font name=\'Helvetica\'>\u03c1</font> \u2265 0.95 = FALSIFIED-"
        "favorable (pre-v1.2 protocol artefact corrected). [Caption to be "
        "refined post-acquisition with verdict-conditional language.]"
    ),
    "f4_per_brand": (
        "Figure 4 \u00b7 Kitchen knives v0.16, per-brand AI Presence \u00d7 Trends rescaled at "
        "t<sub size='6'>1</sub> and t<sub size='6'>2</sub>. Each point is an eligible (E1a + E1b) "
        "brand; coloured by tradition cell (chinese, japanese, british, indian, us_specialty, "
        "french). Mariage Fr\u00e8res, Yunnan Sourcing, and Ippodo Tea anchor the high-AI cluster; "
        "Victorinox \u2014 the Trends pivot \u2014 sits in the low-AI cluster. The new french cell "
        "members (Mariage Fr\u00e8res, Palais des Th\u00e9s, Kusmi Tea, all PASS_E5) cluster in the "
        "high-AI / low-Trends quadrant that drives the Regime 4 signature."
    ),
    "f5_per_tradition": (
        "Figure 5 \u00b7 Kitchen knives v0.16, per-tradition small-multiples. Each panel shows the "
        "eligible brands in one tradition cell at (AI Presence \u00d7 Trends rescaled), with "
        "per-panel axes (magnitudes vary substantially across cells). The chinese cell at n = 3 "
        "(after alternate exhaustion) is structurally smaller than other cells; the new french "
        "cell (PASS_E5 only, lower-confidence Trends signal) and the indian cell (with Tea Box's "
        "anomalously high Trends) show the most internal heterogeneity. Brand labels are auto-"
        "positioned with thin connector lines back to the dots they label."
    ),
}


def _slot_lookup(slot_key: str) -> tuple[str | None, str | None]:
    """Map a v0.16 brand-format slot_key to (filename, figsize_key)."""
    table = {
        # All 5 charts from build_charts_v16.py output (single script ships SSRN + report charts):
        "f1_regime4_canonical":       ("chart_v16_regime4_canonical.pdf",         "6_col_v16_regime4"),
        "f2_per_category":            ("chart_v16_per_category_rho_comparison.pdf", "6_col_v16_per_category"),
        "f3_discourse_language":  ("chart_v16_discourse_language_pair.pdf", "6_col_v16_discourse_language"),
        "f4_per_brand":               ("chart_v16_kitchen_knives_per_brand.pdf",     "6_col_v16_per_brand"),
        "f5_per_tradition":           ("chart_v16_kitchen_knives_per_tradition.pdf", "6_col_v16_per_tradition"),
    }
    return table.get(slot_key, (None, None))


def build_pattern_unified(pattern: dict, styles: dict,
                            manifest: ChartManifest,
                            chart_dir: Path, debug: bool) -> list:
    """v0.14 vertical-flow pattern: heading -> text (2-col balanced) -> chart below.

    Eliminates the lead/chart/tail interleaving from earlier versions. All text
    flows in a single 2-column BalancedColumns block; the chart appears as a
    separate full-width flowable below the text. Avoids the chart-page-conflict
    that produced blank pages when v0.14 source charts are taller than v0.13's.

    Layout budget on Letter (10" content height):
      - Heading block: ~1"
      - Text in 2-col balanced (4-7 paragraphs): ~2-3"
      - Chart with caption: ~5-7"
      Total: 8-11"; tallest patterns may push chart to next page naturally
      (no blank-page artefact).
    """
    slot = pattern["chart_slot"]

    chart_path = None
    figsize_key = None
    if slot:
        fname, figsize_key = _slot_lookup(slot)
        if fname:
            chart_path = chart_dir / fname
            if not chart_path.exists():
                warnings.warn(
                    f"Pattern {pattern['number']} chart missing "
                    f"({fname}); rendering body without chart."
                )
                chart_path = None

    s: list = []

    # Each finding starts on a fresh page (Pablo, 13 May).
    # Note: prior CondPageBreak(80) + PageBreak() combo removed because
    # it could produce empty pages when the previous content ended
    # within 80pt of the frame bottom (CondPageBreak fires → page N+1,
    # PageBreak fires → page N+2, page N+1 blank). The single
    # unconditional PageBreak() suffices to start each finding on a
    # fresh page.
    s.append(PageBreak())

    # Heading: FINDING NN + pattern title (kept together)
    s.append(KeepTogether([
        Spacer(1, 4),
        Paragraph(f"FINDING {pattern['number']:02d}", styles["pattern_number"]),
        Paragraph(pattern["title"], styles["pattern_title"]),
    ]))

    # Build chart flowable (used in either order)
    chart_block: list = []
    if chart_path is not None and figsize_key is not None:
        w_in, h_in = CHART_FIGSIZE_IN[figsize_key]
        is_hero = slot in (
            "f1_regime4_canonical", "f2_per_category",
            "f3_discourse_language", "f4_per_brand",
            "f5_per_tradition",
        )
        caption_style = styles["hero_caption"] if is_hero else styles["caption"]
        caption_text = HERO_FIGURE_CAPTIONS.get(slot, f"Figure {pattern['number']}.")
        chart_res = ChartReservation(
            slot, chart_path, w_in, h_in, manifest,
            debug=debug, caption=caption_text, caption_style=caption_style,
        )
        chart_block = [Spacer(1, 8), chart_res, Spacer(1, 10)]

    # Body text in 2-column balanced block
    paragraphs = [Paragraph(p, styles["body"]) for p in pattern["paragraphs"]]
    text_block: list = []
    if paragraphs:
        text_block = [BalancedColumns(
            paragraphs, nCols=2, innerPadding=GUTTER,
            spaceBefore=4, spaceAfter=10, needed=30,
        )]

    # Per-pattern chart placement (default: chart after title; flag flips to
    # chart after text). Future extensions can add mid-text placement.
    _flag = pattern.get("chart_after_text", False)
    print(f"[pattern {pattern['number']}] chart_after_text={_flag} "
          f"order={'text-then-chart' if _flag else 'chart-then-text'}")
    if _flag:
        s.extend(text_block)
        s.extend(chart_block)
    else:
        s.extend(chart_block)
        s.extend(text_block)

    return s


def build_hypothesis_scoring_story(styles: dict) -> list:
    s = []
    s.append(Spacer(1, 4))
    s.append(Paragraph(content.HYPOTHESIS_SCORING["heading"], styles["h1"]))
    s.append(Spacer(1, 4))
    s.append(Paragraph(content.HYPOTHESIS_SCORING["intro"], styles["body_lead"]))
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

    table_data = [[
        Paragraph("<b>H</b>", header_style),
        Paragraph("<b>Pre-registered prediction</b>", header_style),
        Paragraph("<b>Result</b>", header_style),
        Paragraph("<b>Status</b>", header_style),
    ]]
    for h_id, prediction, result, status_text, status_class in content.HYPOTHESIS_SCORING["rows"]:
        st_style = status_styles.get(status_class, cell_style)
        if status_class == "confirmed":
            status_para = Paragraph(f"<b>{status_text}</b>", st_style)
        elif status_class == "descriptive":
            status_para = Paragraph(f"<i>{status_text}</i>", st_style)
        else:
            status_para = Paragraph(status_text, st_style)
        table_data.append([
            Paragraph(f"<b>{h_id}</b>", h_cell_style),
            Paragraph(prediction, cell_style),
            Paragraph(result, cell_style),
            status_para,
        ])

    indigo = HexColor("#37237B")
    lavender = HexColor("#BBB9DD")
    # v0.14 has 12 rows (more than v0.11's 6). Slightly tighter cell padding
    # and narrower H column to fit on a single page.
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

    if hasattr(content, "HYPOTHESIS_DETAILS"):
        details = content.HYPOTHESIS_DETAILS
        s.append(Spacer(1, 14))
        s.append(KeepTogether([
            Paragraph(details["heading"], styles["h2"]),
            Spacer(1, 4),
            Paragraph(details["intro"], styles["body_lead"]),
        ]))
        s.append(Spacer(1, 8))

        h_paragraphs = [Paragraph(body, styles["body"])
                         for h_id, body in details["items"]]
        s.append(BalancedColumns(
            h_paragraphs, nCols=2, innerPadding=GUTTER,
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

    REPORT_PROTOCOL_VERSION = "v1.1"
    methodology_text = brand["disclaimers"]["methodology_standard"].replace(
        "(current: v0.3)",
        f"(current: {REPORT_PROTOCOL_VERSION})",
    )
    s.append(Paragraph("<b>Methodology</b>", styles["body_lead"]))
    s.append(Paragraph(methodology_text, styles["disclaimer"]))
    s.append(Spacer(1, 10))

    s.append(Paragraph("<b>Citation</b>", styles["body_lead"]))
    citation_text = (
        "Gonzalez Castro, P. U. (2026). "
        "<i>Four Empirical Regimes in AI-Mediated Brand Visibility: A Five-Category "
        "Replication of the v0.13 Regime 4 (Covariate-saturated Weak) Finding "
        "in a Designed-for-Test Category \u2014 Kitchen Knives \u2014 "
        "AI Presence Index v0.16</i>. "
        "Third System. thirdsystem.ai/v16-premium-tea-panel-expansion-robustness (SSRN 6768059)"
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
# Pass 2 overlay (verbatim from v0.11)
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
        scale = min(sx, sy)
        offset_x = slot.x_pt + (target_w - chart_w * scale) / 2
        offset_y = slot.y_pt + (target_h - chart_h * scale) / 2
        op = Transformation().scale(scale, scale).translate(offset_x, offset_y)
        writer.pages[slot.page_index].merge_transformed_page(chart_page, op)

    with open(out_pdf_path, "wb") as f:
        writer.write(f)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def build(*, debug_layout: bool = False,
          chart_dir: Path | None = None,
          output_path: Path | None = None) -> Path:
    with open(BRAND_JSON) as f:
        brand = json.load(f)
    with open(TOKENS_JSON) as f:
        tokens = json.load(f)

    palette = BrandPalette.from_json(brand)
    font = register_typography()
    styles = build_paragraph_styles(font, palette, tokens)

    print(f"[build_report_v16] palette: indigo={palette.indigo}, "
          f"soft_black={palette.soft_black}, paper={palette.paper}")
    print(f"[build_report_v16] typography: {font.name} "
          f"(brand_primary={font.is_brand_primary})")

    V15_DEPOSIT_ROOT = AIAS_ROOT / "osf" / "v16"
    chart_dir = chart_dir or (V15_DEPOSIT_ROOT / "figures")
    output_path = output_path or (V15_DEPOSIT_ROOT / "reports" / "v16_kitchen_knives.pdf")
    base_pdf = output_path.parent / "_v16_base.pdf"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"[build_report_v16] chart pre-flight (looking in {chart_dir})")
    expected_slots = [
        "f1_regime4_canonical", "f2_per_category",
        "f3_discourse_language", "f4_per_brand",
        "f5_per_tradition",
    ]
    expected_files = set()
    for sk in expected_slots:
        fname, _ = _slot_lookup(sk)
        expected_files.add(fname)
        present = (chart_dir / fname).exists()
        status = "FOUND  " if present else "MISSING"
        print(f"  [{status}] {sk:30s} -> {fname}")

    if chart_dir.exists():
        actual_charts = sorted(p.name for p in chart_dir.iterdir()
                                if p.is_file() and p.suffix.lower() == ".pdf"
                                and p.name.startswith("chart_v16"))
        unexpected = [n for n in actual_charts if n not in expected_files]
        if unexpected:
            print(f"[build_report_v16] chart files in dir not used by brand-format report:")
            for n in unexpected:
                print(f"  [UNUSED ] {n}")

    manifest = ChartManifest()
    doc = V15DocTemplate(
        str(base_pdf),
        palette=palette, font=font, styles=styles,
        manifest=manifest, debug_layout=debug_layout,
        title="Panel Expansion Robustness \u2014 AI Presence Index v0.16",
        author=", ".join(content.CLOSING["byline_long"][:1]),
        subject="Independent measurement for the AI mediation layer.",
    )

    story: list = []

    # --- Cover ---
    story.append(NextPageTemplate("body"))
    for f_ in build_cover_story(styles):
        story.append(f_)
    story.append(PageBreak())

    # --- Lead spread + exec summary ---
    for f_ in build_lead_story(styles):
        story.append(f_)

    # --- (No leaderboards spread for v0.14, like v0.10/v0.11.) ---

    # --- What we measured (methodology) ---
    story.append(NextPageTemplate("body"))
    story.append(PageBreak())
    for f_ in build_what_we_measured_story(styles):
        story.append(f_)

    # --- Findings 1-4 ---
    # No story-level PageBreak: build_pattern_unified does its own
    # PageBreak at the start of each finding. The NextPageTemplate
    # change takes effect when that PageBreak fires.
    story.append(NextPageTemplate("spread"))
    for pattern in content.PATTERNS:
        story.extend(build_pattern_unified(
            pattern, styles, manifest, chart_dir, debug_layout))

    # --- Limitations ---
    story.append(NextPageTemplate("body"))
    story.append(PageBreak())
    for f_ in build_limitations_story(styles):
        story.append(f_)

    # --- What's next ---
    story.append(PageBreak())
    for f_ in build_whats_next_story(styles):
        story.append(f_)

    # --- Hypothesis scoring + details ---
    if hasattr(content, "HYPOTHESIS_SCORING"):
        story.append(NextPageTemplate("spread"))
        story.append(PageBreak())
        story.extend(build_hypothesis_scoring_story(styles))

    # --- Closing ---
    story.append(NextPageTemplate("closing"))
    story.append(PageBreak())
    for f_ in build_closing_story(styles, brand):
        story.append(f_)

    doc.build(story)
    print(f"[build_report_v16] base PDF written: {base_pdf} "
          f"({len(manifest.slots)} chart reservations)")
    for slot in manifest.slots:
        ok = "OK" if slot.chart_path.exists() else "MISSING"
        print(f"  [{ok}] {slot.slot_key:30s} -> page {slot.page_index + 1:>2} "
              f"@({slot.x_pt:6.1f},{slot.y_pt:6.1f}) "
              f"{slot.w_pt:6.1f}x{slot.h_pt:6.1f}pt  ({slot.chart_path.name})")

    overlay_charts(base_pdf, manifest, output_path)
    print(f"[build_report_v16] FINAL PDF written: {output_path}")

    final_pages = len(PdfReader(str(output_path)).pages)
    print(f"[build_report_v16] page count: {final_pages}")
    if final_pages < 9 or final_pages > 20:
        warnings.warn(
            f"Page count {final_pages} is outside the 9-20 target band."
        )

    return output_path


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--debug-layout", action="store_true",
                     help="Draw faint borders around chart reservations.")
    ap.add_argument("--chart-dir", type=Path, default=None,
                     help="Directory containing chart_*.pdf files.")
    ap.add_argument("--output", type=Path, default=None,
                     help="Output PDF path. Defaults to ~/aias/osf/v16/reports/v16_kitchen_knives.pdf")
    args = ap.parse_args()
    build(
        debug_layout=args.debug_layout,
        chart_dir=args.chart_dir,
        output_path=args.output,
    )
