#!/usr/bin/env python3
"""
v0.11 PM Software × Google Trends Construct Validity — typesetting pipeline.

Forked from build_report_v10.py with surgical changes:
  - Imports v10_naivephantom_content instead of v09_rebaseline_content
  - Section label remains "FINDING"
  - Hero check matches v10 hero slot keys (valence / h2_split / decoupling)
  - HERO_FIGURE_CAPTIONS extended for v10 figures
  - _slot_lookup table updated for chart_v10_*.pdf filenames
  - CHART_FIGSIZE_IN extended with v10 figsize keys (3 charts at 6-col width:
    valence 4.50", h2 4.00", h3 4.40")
  - build_leaderboards_spread returns [] (v10 has no front-of-report hero
    spread; the three findings carry the narrative directly after exec summary)
  - Header right text, citation, output filename, doc metadata updated
  - REPORT_PROTOCOL_VERSION stays at v1.1 (same protocol as v0.9)

Inputs:
  - brand/third_system_brand.json        (v1.4)
  - brand/design_tokens_template.json    (IDML extract)
  - brand/report_specs.json              (priority-1 spec for cross_category_report)
  - reports/output/chart_v10_*.pdf       (3 charts from build_charts_v10_naivephantom.py)

Output:
  - reports/output/v10_naivephantom_stability.pdf

The v0.6, v0.7, v0.8, and v0.9 build_report scripts are left untouched. Run
this for v0.10 naive-phantom rate longitudinal stability:

    python3 build_charts_v10_naivephantom.py
    python3 build_report_v10.py

Locked rules followed (same as v0.6/v0.7/v0.8/v0.9):
  - Image-placeholder rectangles in master spreads stay BLANK (no fill colors).
  - Template's #FF001A red is overridden to brand primary (Indigo #37237B per
    third_system_brand.json v1.4).
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
AIAS_ROOT = SCRIPT_DIR.parent              # /Users/pablou/aias on Pablo's Mac
BRAND_DIR = AIAS_ROOT / "brand"
OUTPUT_DIR = SCRIPT_DIR / "output"

BRAND_JSON = BRAND_DIR / "third_system_brand.json"
TOKENS_JSON = BRAND_DIR / "design_tokens_template.json"
SPECS_JSON = BRAND_DIR / "report_specs.json"
SOURCE_TEXT = BRAND_DIR / "v06_source_text.md"     # extracted body text (informational only)
WORDMARK_SVG = BRAND_DIR / "THIRDSYSTEM_Logo.svg"
LOCKUP_SVG = BRAND_DIR / "THIRDSYSTEM_AIPT_Logo.svg"

# Make `import v06_content` work regardless of working directory.
sys.path.insert(0, str(SCRIPT_DIR))
import v11_pmtrends_content as content  # noqa: E402
import tsboilerplate as boilerplate  # noqa: E402

# ---------------------------------------------------------------------------
# Page geometry — locked by template content_area
# ---------------------------------------------------------------------------

PAGE_W, PAGE_H = LETTER                    # 612 x 792 pt
MARGIN = 36.0                              # 36 pt
CONTENT_W = PAGE_W - 2 * MARGIN            # 540
CONTENT_H = PAGE_H - 2 * MARGIN            # 720
COL_COUNT = 6
GUTTER = 10.0008
COL_W = (CONTENT_W - (COL_COUNT - 1) * GUTTER) / COL_COUNT  # ~81.667

# Column x positions (left edge of each column), in points
COL_X = [MARGIN + i * (COL_W + GUTTER) for i in range(COL_COUNT)]

# Span widths in points (column_count * COL_W + (column_count-1)*GUTTER)
def span_pts(n: int) -> float:
    return n * COL_W + (n - 1) * GUTTER

SPANS_PT = {n: span_pts(n) for n in range(1, COL_COUNT + 1)}

# Locked figsize spec (inches) from chart_sizing_specifications.figsize_by_column_span.
# Used for chart slot reservation only — chart PDFs are already rendered at these sizes.
CHART_FIGSIZE_IN = {
    "1_col": (1.13, 1.13),
    "2_col": (2.41, 2.10),
    "3_col_inline": (3.68, 2.85),
    "4_col": (4.95, 3.71),
    "6_col_hero": (7.50, 5.00),
    "6_col_hero_tall": (7.50, 6.50),
    "6_col_hero_xl": (7.50, 7.50),    # used for leaderboards: 5 stacked panels
    "6_col_hero_xl_95": (7.125, 7.125),  # v0.8: 5% smaller leaderboard variant
    "spread": (7.50, 4.50),           # used for v0.6 Pattern 4 country panel
    # v0.7 additions: shorter heights for charts whose content doesn't need 5".
    "6_col_short": (7.50, 3.50),      # F1, F5 — two/three-row compact comparisons
    "6_col_hero_short": (7.50, 3.75), # F2 — multi-row stacked bars, tightened
    "6_col_compact": (7.50, 3.00),    # F4 — extra-compact for body-heavy findings
    # v0.9 additions: charts have varied heights at the 6-col width (4.00 to
    # 4.75 inches) plus a square 4.5-inch chart for the H4 Mint two-point
    # plot. Each key reserves a slot whose height matches the chart's actual
    # figsize so the pypdf overlay aligns at native resolution.
    "6_col_v09_drift":      (7.50, 4.75),  # H1 drift scatter
    "6_col_v09_leaderboard": (7.50, 6.50), # H2 leaderboard (5 stacked panels, fits printable area)
    "6_col_v09_variance":   (7.50, 4.10),  # H3 within-category variance
    "4_col_v09_mint":       (3.55, 3.20),  # H4 Mint persistence (1-column inline, fits in BC col 1)
    "6_col_v09_pattern4":   (7.50, 4.40),  # H5 Pattern 4 sensitivity
    "6_col_v09_h6":         (7.50, 4.00),  # H6 cross-model spread
    "6_col_v09_pattern1":   (7.50, 4.20),  # post-hoc Pattern 1
    "6_col_v09_modes":      (7.50, 4.50),  # mode distribution
    "6_col_v09_matrix":     (7.50, 4.75),  # pattern replication matrix
    # v0.10 additions: three charts at 6-col width with varied heights matching
    # the matplotlib figsize used in build_charts_v10_naivephantom.py.
    "6_col_v10_h2":         (7.50, 4.00),  # F2 H2 binary breakdown (naive vs caveated)
    "6_col_v10_valence":    (7.50, 4.50),  # F1 v0.7 5-class valence distribution
    "6_col_v10_h3":         (7.50, 4.40),  # F3 H3 decoupling line plot
    # v0.11 additions: three figsize variants matching the matplotlib
    # figsize used in build_charts_v11_pmtrends.py.
    "6_col_v11_scatter":    (7.50, 5.00),  # F1 / F2 scatter plots
    "6_col_v11_rankshift":  (7.50, 6.50),  # F3 rank-shift slope chart (tall)
    "6_col_v11_partial":    (7.50, 5.30),  # F4 partial-residual scatter (taller for 2-line subtitle)
}

# Body two-column flow uses 3+3: text spans columns 1-3, then 4-6, with the
# template's 10pt gutter between them.
BODY_LEFT_X = COL_X[0]
BODY_LEFT_W = span_pts(3)
BODY_RIGHT_X = COL_X[3]
BODY_RIGHT_W = span_pts(3)


# ---------------------------------------------------------------------------
# Brand colors — INDIGO #37237B is the v1.4 primary. The handoff doc references
# the legacy #25408F from v1.0; brand JSON's version_history confirms the swap
# at v1.1. Brand spec wins as documented "source of truth."
# ---------------------------------------------------------------------------

@dataclass
class BrandPalette:
    indigo: str
    soft_black: str
    paper: str
    petro: str
    lavender_grey: str
    template_red_override: str   # what the template's red maps to

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
            template_red_override=indigo,   # the explicit override
        )


# ---------------------------------------------------------------------------
# Font registration with graceful fallback
# ---------------------------------------------------------------------------

@dataclass
class FontFamily:
    name: str
    light: str
    regular: str
    bold: str
    italic: str
    bold_italic: str
    is_brand_primary: bool   # True = Akkurat Pro; False = Inter or system fallback


def _convert_otf_to_ttf(otf_path: Path, cache_dir: Path) -> Path | None:
    """Convert a CFF-flavored OTF to a glyf-flavored TTF using fontTools.

    ReportLab's TTFont class accepts TrueType (.ttf) and TrueType-flavored OTF
    files but does NOT support OpenType OTFs with PostScript (CFF) outlines —
    which is exactly what most professional typefaces (including Akkurat Pro)
    are distributed as. This converter rewrites the font with quadratic glyf
    outlines so ReportLab can load it.

    Cache: converted files live in cache_dir, keyed by filename. Re-converts
    if the source file's mtime is newer than the cache.

    Returns the path to the converted TTF, or None if conversion failed
    (e.g., fontTools isn't installed or the font is already a glyf-based TTF).
    """
    try:
        from fontTools.ttLib import TTFont as _FTFont
        from fontTools.pens.ttGlyphPen import TTGlyphPen
        from fontTools.pens.cu2quPen import Cu2QuPen
        from fontTools.ttLib.tables import _l_o_c_a
        from fontTools.ttLib.tables._g_l_y_f import table__g_l_y_f
    except ImportError:
        print(f"  [convert-fail] fontTools not installed; cannot convert {otf_path.name} "
              f"from CFF to TTF. Run: pip install fonttools")
        return None

    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cache_dir / (otf_path.stem + ".ttf")

    # Skip conversion if cache is fresh
    try:
        if cache_path.exists() and cache_path.stat().st_mtime >= otf_path.stat().st_mtime:
            return cache_path
    except OSError:
        pass

    try:
        font = _FTFont(str(otf_path))

        if "glyf" in font:
            # Already TT outlines — just rewrite to drop any CFF baggage.
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
        font.sfntVersion = "\x00\x01\x00\x00"  # TrueType signature
        font.save(str(cache_path))
        return cache_path
    except Exception as exc:
        print(f"  [convert-fail] {otf_path.name}: {type(exc).__name__}: {exc}")
        return None


# Cache directory for converted fonts (one-time conversion per OTF)
_FONT_CACHE_DIR = Path.home() / ".cache" / "third_system_reports" / "fonts"


def _try_register_font(label: str, path: Path) -> bool:
    if not path.exists():
        print(f"  [register-fail] {label}: file does not exist at {path}")
        return False
    try:
        pdfmetrics.registerFont(TTFont(label, str(path)))
        return True
    except Exception as exc:
        # Most likely cause for OTF files: ReportLab's TTFont does not support
        # CFF (PostScript) outlines. Convert OTF to TTF and retry.
        msg = str(exc).lower()
        if path.suffix.lower() == ".otf" and (
            "postscript" in msg or "cff" in msg or "outlines are not supported" in msg
        ):
            print(f"  [register-info] {path.name} has CFF outlines; converting to TTF…")
            converted = _convert_otf_to_ttf(path, _FONT_CACHE_DIR)
            if converted and converted.exists():
                try:
                    pdfmetrics.registerFont(TTFont(label, str(converted)))
                    print(f"  [register-info] {label} loaded from converted TTF "
                          f"at {converted}")
                    return True
                except Exception as exc2:
                    print(f"  [register-fail] {label} <- {converted.name}: "
                          f"{type(exc2).__name__}: {exc2}")
                    return False
            return False
        print(f"  [register-fail] {label} <- {path.name}: {type(exc).__name__}: {exc}")
        return False


# Search paths in descending priority. macOS-friendly first, then Linux.
def _font_search_dirs() -> list[Path]:
    home = Path.home()
    return [
        home / "Library" / "Fonts",                # macOS user
        Path("/Library/Fonts"),                    # macOS system-wide
        Path("/System/Library/Fonts"),             # macOS system (read)
        Path("/System/Library/Fonts/Supplemental"),# macOS supplemental
        # Adobe Fonts (Creative Cloud) sync location — fonts appear here as
        # files with hash-based names AND also as recognizable .otf/.ttf files
        # that we can pick up by their filename content.
        home / "Library" / "Application Support" / "Adobe" / "CoreSync" / "plugins" / "livetype" / ".r",
        home / "Library" / "Application Support" / "Adobe" / "CoreSync" / "plugins" / "livetype" / "r",
        home / ".fonts",                           # Linux user (legacy)
        home / ".fonts" / "Akkurat",
        home / ".fonts" / "Inter",
        home / ".local" / "share" / "fonts",
        Path("/usr/share/fonts"),
        Path("/usr/local/share/fonts"),
    ]


def _enumerate_font_files(dirs: list[Path]) -> list[Path]:
    """Recursively find every .otf and .ttf file in the given directories.
    Recursive because macOS Font Book sometimes puts fonts in subfolders, and
    so do font foundry installers."""
    found = []
    for d in dirs:
        if not d.exists():
            continue
        try:
            for ext in ("*.otf", "*.ttf", "*.OTF", "*.TTF"):
                found.extend(d.rglob(ext))
        except Exception:
            # permissions on some macOS system dirs — skip silently
            continue
    return found


def _classify_font_filename(filename: str) -> str | None:
    """Classify a font filename into one of: light, regular, bold, italic,
    bolditalic. Returns None if no clear classification.

    Order matters: more specific patterns checked first. 'BoldItalic' must be
    checked before 'Bold' or 'Italic' alone, because the filename contains
    both substrings.
    """
    n = filename.lower().replace(" ", "").replace("_", "").replace("-", "")
    # n is now e.g. "akkuratprobolditalic.otf" or "akkuratlightproregular.otf"

    # Order matters — most specific first.
    if "bolditalic" in n:
        return "bolditalic"
    # Light Italic — treat as italic of the light face if no separate bold-italic
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
    # Default — anything else with 'akkurat' or 'inter' in it is the regular face.
    # (Fonts named just 'AkkuratPro-Regular.otf' or 'AkkuratPro.otf' fall here.)
    if "regular" in n:
        return "regular"
    # Bare family name like "AkkuratPro.otf" — assume regular
    return "regular"


def _classify_files_into_slots(files: list[Path]) -> dict[str, Path | None]:
    """For each font file, classify it and assign to the matching slot. If
    multiple files map to the same classification, prefer non-Light variants
    for the regular weight family (Bold, Italic, BoldItalic).

    Light slot prefers files explicitly named with 'Light' in their family
    portion (e.g. AkkuratLightPro-Regular.otf — that's Light Pro family at
    regular weight).
    """
    buckets: dict[str, list[Path]] = {
        "light": [], "regular": [], "bold": [],
        "italic": [], "bolditalic": [],
    }
    for f in files:
        cls = _classify_font_filename(f.name)
        if cls in buckets:
            buckets[cls].append(f)

    # Disambiguation: bold/italic/bolditalic should NOT come from a Light Pro
    # family file. Light Pro is a distinct family (different weight) — its
    # italic is meant to pair with Light Pro Regular, not with Akkurat Pro
    # Regular. So filter out Light Pro variants for those slots.
    def _is_light_family(p: Path) -> bool:
        n = p.name.lower().replace(" ", "").replace("_", "").replace("-", "")
        # 'lightpro' substring marks the Light Pro family
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
            # Prefer "AkkuratPro-Light" (the Akkurat Pro family at light
            # weight) over "AkkuratLightPro-Regular" (the Akkurat Light Pro
            # family at regular weight). Brand spec calls for Akkurat Pro
            # Light specifically.
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
    """
    Register Akkurat Pro from any sensible macOS/Linux font location, with
    Inter as documented fallback. Filenames are classified by examining
    substrings in priority order so any reasonable Akkurat naming convention
    works.

    Prints a loud diagnostic showing which directories were scanned, which
    Akkurat files were found, and how each was classified.
    """
    dirs = _font_search_dirs()
    all_files = _enumerate_font_files(dirs)
    print(f"[fonts] scanned {len(all_files)} font files across {len(dirs)} dirs:")
    for d in dirs:
        marker = "ok" if d.exists() else "--"
        print(f"  [{marker}] {d}")

    # Akkurat
    akkurat_files = [p for p in all_files if "akkurat" in p.name.lower()]
    if akkurat_files:
        print(f"[fonts] {len(akkurat_files)} Akkurat file(s) found:")
        for p in akkurat_files:
            cls = _classify_font_filename(p.name)
            print(f"  - {p.name} -> classified as: {cls}")
    else:
        print(f"[fonts] no Akkurat files matched (looked for 'akkurat' in filename)")

    akkurat_picked = _classify_files_into_slots(akkurat_files)

    # Map classifications to slot labels and try to register
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
            print(f"  [register] {slot_label:22s} <- {path.name}")
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

    warnings.warn(
        "Akkurat Pro not found in any searched font directory. "
        "See the [fonts] log lines above for which paths were checked. "
        "Attempting Inter fallback. Brand typography is not at full fidelity."
    )

    # Inter fallback — same classifier
    inter_files = [p for p in all_files if "inter" in p.name.lower()
                    and "interstate" not in p.name.lower()]
    inter_picked = _classify_files_into_slots(inter_files)

    inter_slot_to_class = {
        "Inter-Light":      "light",
        "Inter-Regular":    "regular",
        "Inter-Bold":       "bold",
        "Inter-Italic":     "italic",
        "Inter-BoldItalic": "bolditalic",
    }
    found_inter: dict[str, Path | None] = {}
    for slot_label, cls in inter_slot_to_class.items():
        path = inter_picked.get(cls)
        if path and _try_register_font(slot_label, path):
            found_inter[slot_label] = slot_label
            print(f"  [register] {slot_label:22s} <- {path.name}")
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
        print(f"[fonts] using Inter (documented fallback — not Akkurat)")
        return FontFamily(
            name="Inter", light="Inter-Light", regular=regular, bold=bold,
            italic=italic, bold_italic=bold_italic,
            is_brand_primary=False,
        )

    warnings.warn(
        "*** HARD FALLBACK: neither Akkurat Pro nor Inter could be registered. "
        "Falling back to Helvetica. The PDF will render but is NOT brand-compliant. "
        "Install Akkurat Pro at ~/Library/Fonts/ to restore brand typography. ***"
    )
    print(f"[fonts] using Helvetica (HARD FALLBACK — not brand-compliant)")
    return FontFamily(
        name="Helvetica",
        light="Helvetica",
        regular="Helvetica",
        bold="Helvetica-Bold",
        italic="Helvetica-Oblique",
        bold_italic="Helvetica-BoldOblique",
        is_brand_primary=False,
    )


# ---------------------------------------------------------------------------
# IDML paragraph_styles → ReportLab ParagraphStyle mapping
# ---------------------------------------------------------------------------

def build_paragraph_styles(font: FontFamily, palette: BrandPalette,
                           tokens: dict) -> dict[str, ParagraphStyle]:
    """
    Convert the template's IDML paragraph styles to ReportLab ParagraphStyles,
    overriding template colors with brand palette per the locked rules.

    Returns dict keyed by short alias (e.g. 'title40', 'body9', 'h1', 'callout1').
    """

    by_name = {ps["name"]: ps for ps in tokens.get("paragraph_styles", [])}

    def fill_to_hex(fill_color: str) -> str:
        # Color/Black, Color/C=0 M=100 Y=90 K=0, Color/C=25 M=25 Y=25 K=100
        if fill_color in ("Color/Black", "Color/C=25 M=25 Y=25 K=100"):
            return palette.soft_black
        if fill_color == "Color/C=0 M=100 Y=90 K=0":   # template red → brand override
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
        # ReportLab 4.x ParagraphStyle does NOT carry a tracking field — char-spacing
        # is a canvas-level setCharSpace, not a paragraph attribute. We simply omit
        # it; if Pablo wants tighter or looser tracking on a specific style we can
        # subclass Paragraph to call setCharSpace before drawing.
        if "wordWrap" in overrides and overrides["wordWrap"] is not None:
            kwargs["wordWrap"] = overrides["wordWrap"]
        return ParagraphStyle(**kwargs)

    P = "Marketing Literature Styles:"

    styles = {
        # ---- Cover ----
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

        # ---- Lead spread ----
        "standfirst": make("standfirst", P + "H_Callout 1 20/22",
                           textColor=palette.indigo,
                           fontName=font.bold,
                           fontSize=24, leading=28, spaceAfter=14),
        "lead_deck": make("lead_deck", P + "A_Bruchure Summary 11/14",
                          fontSize=14, leading=18, spaceAfter=14,
                          fontName=font.light),

        # ---- Body ----
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

        # ---- Charts / captions ----
        "caption": make("caption", P + "G_Charts Copy 2 9/12",
                        fontName=font.regular,
                        fontSize=8, leading=10, spaceAfter=4),
        "hero_caption": make("hero_caption", P + "G_Charts Copy 2 9/12",
                              fontName=font.regular,
                              fontSize=9.5, leading=13, spaceAfter=4),

        # ---- Footer / disclaimers ----
        "footer": make("footer", P + "I_Disclaimer/Footnotes 7.5/9.5",
                       fontName=font.light,
                       fontSize=7, leading=9.5),
        "disclaimer": make("disclaimer", P + "I_Disclaimer/Footnotes 7.5/9.5",
                            fontName=font.light,
                            fontSize=7.5, leading=10, spaceAfter=4),
    }

    # Reportlab will silently choke on unknown kwargs; clean up the phantom one
    # I sketched in body above (defensive — make() accepts overrides only).
    return styles


# ---------------------------------------------------------------------------
# Chart slot reservation — manifest tracker + Flowable
# ---------------------------------------------------------------------------

@dataclass
class ChartSlot:
    """One reserved rectangle on a page where a chart PDF will be merged."""
    slot_key: str
    chart_path: Path
    page_index: int             # 0-indexed
    x_pt: float                 # lower-left x in PDF coords (origin = bottom-left)
    y_pt: float
    w_pt: float
    h_pt: float


@dataclass
class ChartManifest:
    """Collects all chart placements during pass 1, used during pass 2 overlay."""
    slots: list[ChartSlot] = field(default_factory=list)

    def add(self, key: str, chart_path: Path, page_index: int,
            x_pt: float, y_pt: float, w_pt: float, h_pt: float) -> None:
        self.slots.append(ChartSlot(
            slot_key=key, chart_path=chart_path,
            page_index=page_index,
            x_pt=x_pt, y_pt=y_pt, w_pt=w_pt, h_pt=h_pt,
        ))


class ChartReservation(Flowable):
    """
    Reserves a rectangle in the platypus flow at the chart's native figsize.
    Records its actual position on the page into the manifest so the overlay
    pass can place the chart PDF there.

    The reservation draws nothing visible (no placeholder fill — locked rule).
    A faint debug border can be enabled for layout checking.
    """

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
        self.hAlign = hAlign  # 'LEFT' (default), 'CENTER', or 'RIGHT'
        # caption height computed lazily during wrap
        self._caption_h = 0.0
        self._caption_w = 0.0

        # Image-like attrs so ChartReservation can be used as the image
        # argument in ImageAndFlowables. IAF queries drawWidth/drawHeight
        # and _restrictSize() to position the image and reserve its column
        # space. Caption height is included so text wraps around the
        # chart+caption block as a unit.
        self.drawWidth = self.chart_w_pt
        # drawHeight is set during wrap once caption_h is known. Pre-fill
        # with chart height alone in case wrap isn't called first.
        self.drawHeight = self.chart_h_pt
        self.imageWidth = self.drawWidth
        self.imageHeight = self.drawHeight

    def _restrictSize(self, aW, aH):
        """ImageAndFlowables compatibility — IAF calls this to constrain
        the image to available space. We don't actually scale; the chart's
        figsize is locked. Just return current dimensions."""
        return self.drawWidth, self.drawHeight

    def _unRestrictSize(self):
        """ImageAndFlowables compatibility — IAF calls this after layout
        to undo any size restriction. We don't restrict, so this is a
        no-op."""
        pass

    def wrap(self, available_w, available_h):
        # Report a width that fits within the available space — this makes the
        # reservation play nicely inside BalancedColumns, where each column may
        # be narrower than the chart's intrinsic figsize. The chart still
        # draws at its native pixel size; this only affects layout decisions.
        reported_w = min(self.chart_w_pt, available_w)
        if self.caption_p is not None:
            cw, ch = self.caption_p.wrap(reported_w, available_h)
            self._caption_w, self._caption_h = cw, ch
            total_h = self.chart_h_pt + ch + 4
            # Update Image-like attrs for IAF
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
        # The Flowable's local coord system has origin at lower-left of its box.
        # We need page-coordinates for the manifest.
        # Translate local origin to page coords:
        x_page, y_page = c.absolutePosition(0, 0)

        # Caption sits below the chart
        chart_y_local = self._caption_h + 4 if self.caption_p else 0
        chart_y_page = y_page + chart_y_local
        chart_x_page = x_page

        # canvas.getPageNumber() is 1-indexed; pypdf wants 0-indexed.
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

        # Caption
        if self.caption_p is not None:
            self.caption_p.drawOn(c, 0, 0)


# ---------------------------------------------------------------------------
# Custom DocTemplate — page templates for cover, body, closing
# ---------------------------------------------------------------------------

class V06DocTemplate(BaseDocTemplate):

    def __init__(self, filename: str, *,
                 palette: BrandPalette,
                 font: FontFamily,
                 styles: dict[str, ParagraphStyle],
                 manifest: ChartManifest,
                 debug_layout: bool = False,
                 **kw):
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

        # Body uses two visual columns (3+3 of the 6-col grid), with a footer
        # band reserved at the bottom.
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

        # Spread template: a single full-width frame for hero charts and lead spreads
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

    # -- chrome painters ----------------------------------------------------

    def _cover_decoration(self, canvas: Canvas, doc):
        """Cover chrome: draw the AIPT lockup at the top of the cover.
        Image-placeholder rectangles in the master are intentionally blank."""
        c = canvas
        c.saveState()

        # Page background: paper #FAF7F2 for screen, white for print.
        # Choose paper for screen-first viewing.
        c.setFillColor(HexColor(self.palette.paper))
        c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

        # AIPT lockup — top-left of cover area, drawn from SVG
        if LOCKUP_SVG.exists():
            self._draw_lockup_top(c, LOCKUP_SVG, x=MARGIN, y=PAGE_H - MARGIN - 36, height=36)
        else:
            self._draw_lockup_text_fallback(c, x=MARGIN, y=PAGE_H - MARGIN - 36)

        # (No rule under the lockup — cover stays clean.)

        # Tagline — bottom of cover, small
        c.setFillColor(HexColor(self.palette.soft_black))
        c.setFont(self.font.regular, 8)
        c.drawString(MARGIN, MARGIN + 8, content_meta_line(self))

        c.restoreState()

    def _body_chrome(self, canvas: Canvas, doc):
        """Running header (wordmark) + footer (public_report verbatim).
        No indigo rule under the wordmark — header stays clean."""
        c = canvas
        c.saveState()

        # Header — wordmark left, page meta right, no rule
        header_y = PAGE_H - MARGIN + 14   # in the top margin band
        if WORDMARK_SVG.exists():
            self._draw_wordmark_top(c, WORDMARK_SVG, x=MARGIN, y=header_y - 10, height=10)
        else:
            c.setFont(self.font.bold, 9)
            c.setFillColor(HexColor(self.palette.indigo))
            c.drawString(MARGIN, header_y - 8, "Third System")

        c.setFont(self.font.regular, 7.5)
        c.setFillColor(HexColor(self.palette.soft_black))
        c.drawRightString(PAGE_W - MARGIN, header_y - 8,
                           "PM Software \u00d7 Trends Construct Validity \u00b7 v0.11 \u00b7 10 May 2026")

        # Footer — public_report verbatim from third_system_brand.json
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
        # Page number on the right
        c.drawRightString(PAGE_W - MARGIN, footer_y, f"{doc.page}")

        c.restoreState()

    def _draw_wordmark_top(self, c: Canvas, svg_path: Path, x: float, y: float, height: float):
        """Draw the THIRDSYSTEM wordmark at given height, preserving aspect ratio.
        We render text directly using Akkurat Bold Indigo since the SVG is itself
        a typeset 'Third System' wordmark — bypassing SVG parsing keeps things vector
        without an extra dep. If the SVG embedded glyphs were truly custom we'd use
        svglib; for the brand wordmark, the typeface is the wordmark."""
        # Use wordmark text styled per spec: Akkurat Bold #37237B, no stretching.
        c.saveState()
        c.setFillColor(HexColor(self.palette.indigo))
        c.setFont(self.font.bold, height)
        c.drawString(x, y, "Third System")
        c.restoreState()

    def _draw_lockup_top(self, c: Canvas, svg_path: Path, x: float, y: float, height: float):
        """Two-line product lockup: 'Third System' bold indigo over 'AI Presence Index' regular black."""
        c.saveState()
        line_h = height / 2.6
        c.setFillColor(HexColor(self.palette.indigo))
        c.setFont(self.font.bold, line_h * 1.4)
        c.drawString(x, y + line_h * 0.9, "Third System")
        c.setFillColor(HexColor(self.palette.soft_black))
        c.setFont(self.font.regular, line_h * 1.1)
        c.drawString(x, y - line_h * 0.4, "AI Presence Index")
        c.restoreState()

    def _draw_lockup_text_fallback(self, c: Canvas, x: float, y: float):
        c.saveState()
        c.setFillColor(HexColor(self.palette.indigo))
        c.setFont(self.font.bold, 14)
        c.drawString(x, y + 14, "Third System")
        c.setFillColor(HexColor(self.palette.soft_black))
        c.setFont(self.font.regular, 11)
        c.drawString(x, y, "AI Presence Index")
        c.restoreState()


def content_meta_line(doc: V06DocTemplate) -> str:
    return "thirdsystem.ai · hello@thirdsystem.ai · " + content.COVER["date"]


# ---------------------------------------------------------------------------
# Story builders — produce platypus flowables for each section
# ---------------------------------------------------------------------------

def make_chart_reservation(slot_key: str, manifest: ChartManifest,
                            chart_dir: Path, styles: dict,
                            caption: str | None = None,
                            debug: bool = False) -> ChartReservation | None:
    """
    Look up the slot's filename + figsize and return a reservation.

    Returns None (with a warning) if the slot key is unknown, or with a warning
    if the chart file is missing (the reservation still gets returned so the
    page geometry is reserved correctly).
    """
    fname, figsize_key = _slot_lookup(slot_key)
    if fname is None:
        warnings.warn(f"Unknown chart slot: {slot_key}")
        return None
    chart_path = chart_dir / fname
    if not chart_path.exists():
        warnings.warn(
            f"Chart file missing: {chart_path}. Reservation will be left blank."
        )
    w_in, h_in = CHART_FIGSIZE_IN[figsize_key]
    return ChartReservation(slot_key, chart_path, w_in, h_in, manifest,
                             debug=debug,
                             caption=caption,
                             caption_style=styles.get("caption"))


def build_cover_story(styles: dict[str, ParagraphStyle]) -> list:
    """Cover story: minimal — title, subtitle, byline, tagline. No placeholder fills."""
    s = []
    # Push the title down to roughly the upper third of the cover
    s.append(Spacer(1, CONTENT_H * 0.30))
    s.append(Paragraph(content.COVER["title"], styles["cover_title"]))
    s.append(Paragraph(content.COVER["subtitle"], styles["cover_subtitle"]))
    s.append(Spacer(1, 18))
    s.append(Paragraph(
        f"{content.COVER['date']} &nbsp;&nbsp;·&nbsp;&nbsp; "
        f"{content.COVER['byline_short']}",
        styles["cover_byline"]))
    s.append(Spacer(1, CONTENT_H * 0.18))
    s.append(Paragraph(content.COVER["tagline"], styles["cover_tagline"]))
    return s


def build_lead_story(styles: dict[str, ParagraphStyle]) -> list:
    """Lead spread + executive summary. Ends with the closing paragraph
    of the exec summary, so the next section break lands cleanly."""
    s = []
    s.append(Paragraph(content.STANDFIRST, styles["standfirst"]))
    s.append(Paragraph(content.LEAD_DECK, styles["lead_deck"]))
    s.append(Spacer(1, 4))
    for p in content.EXEC_SUMMARY:
        s.append(Paragraph(p, styles["body"]))
    return s


def build_what_we_measured_story(styles: dict[str, ParagraphStyle]) -> list:
    """The methodology section that introduces the measurement approach."""
    s = []
    s.append(Paragraph(content.WHAT_WE_MEASURED["heading"], styles["h2"]))
    for p in content.WHAT_WE_MEASURED["paragraphs"]:
        s.append(Paragraph(p, styles["body"]))
    return s


def build_leaderboards_spread(styles: dict, manifest: ChartManifest,
                               chart_dir: Path, debug: bool) -> list:
    """v0.10: skipped. The three findings (F1 valence, F2 H2 split,
    F3 decoupling) follow the executive summary directly. There is no
    front-of-report hero spread — at v0.10's narrower scope (single brand,
    three hypotheses), the exec summary already carries the at-a-glance
    framing the leaderboards spread provided in v0.6–v0.9.

    Returning [] makes the caller skip the spread template switch and the
    PageBreak entirely (the calling code already checks `if leaderboards_flow`)."""
    return []


def build_three_modes_story(styles: dict) -> list:
    s = []
    s.append(Spacer(1, 4))
    s.append(Paragraph(content.THREE_MODES["heading"], styles["h1"]))
    for p in content.THREE_MODES["paragraphs"]:
        s.append(Paragraph(p, styles["body"]))
    return s


def build_pattern_unified(pattern: dict, styles: dict,
                            manifest: ChartManifest,
                            chart_dir: Path, debug: bool) -> list:
    """Single unified builder for all patterns on the SPREAD template.

    All patterns use the SANDWICH layout:
    1. Section title (full width, KeepTogether with PATTERN N tag).
    2. BalancedColumns(2) with the LEAD body paragraphs (first 2). This
       block fills any leftover space on the previous pattern's last page,
       so the section visually starts there with real text flow rather
       than just a title plus empty space.
    3. Chart + caption (full width). For hero patterns the chart is wide
       6-col size; for non-hero it's 4-col. The chart appears inline in
       the section's text flow — wherever it lands by the natural reflow.
    4. BalancedColumns(2) with the REST of the body. Continues the
       2-column flow after the chart, naturally page-breaking as needed.

    This sandwich layout solves three problems at once:
    - Pattern starts on the previous pattern's last page (lead BC fills
      leftover space cleanly).
    - Chart embeds in the section's text flow, never on its own page.
    - Small BC blocks (2 paragraphs each) lay out reliably in any
      remaining space — no shrink-to-fit failures.
    """
    slot = pattern["chart_slot"]
    is_hero = slot in (
        # v0.6/v0.7/v0.8 slot names (kept so old reports still build)
        "hero_f1_lineage_aggregates", "hero_f2_authorities",
        "hero_f3_within_lineage", "hero_f4_per_cep",
        # v0.9 slot names — Findings 1, 2, 3, 5, 6, 7 render full-width hero;
        # Finding 4 (Mint) renders inline in column 1 because the chart is
        # a small two-point comparison that reads better at column width.
        "hero_f1_drift_scatter", "hero_f2_leaderboard",
        "hero_f3_variance",
        "hero_f5_pattern4",       "hero_f6_spread",
        "hero_f7_pattern1",
        # v0.10 slot names — all three findings render full-width hero
        # (the charts are wide-format and benefit from the spread frame).
        "hero_f1_valence", "hero_f2_h2_split", "hero_f3_decoupling",
        # v0.11 slot names — all four findings render full-width hero.
        "f1_scatter_t1", "f2_scatter_t2", "f3_rank_shift_t1", "f4_partial_residual_t1",
    )

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

    # v0.8.2: cond_threshold = 50 (was 100) for the tightest packing the
    # title block tolerates. Title KeepTogether is ~80pt — at threshold
    # below that, KT will defer cleanly when there isn't enough room rather
    # than placing an orphaned title. So setting threshold to 50 means:
    # findings start in any leftover space \u226550pt; if the title block
    # itself can't fit in that space, KT handles deferral. Eliminates dead
    # space \u2265 50pt at end of previous findings.
    #
    # v0.9 addition: per-pattern force_page_break=True overrides CondPageBreak
    # with an unconditional PageBreak. Used by Finding 4 (Mint), whose smaller
    # inline chart wants to stay on a single page with its body text rather
    # than starting in leftover space from Finding 3.
    if pattern.get("force_page_break"):
        s.append(PageBreak())
    else:
        cond_threshold = 50
        s.append(CondPageBreak(cond_threshold))

    # Section title spans full width
    s.append(KeepTogether([
        Spacer(1, 4),
        Paragraph(f"FINDING {pattern['number']:02d}", styles["pattern_number"]),
        Paragraph(pattern["title"], styles["pattern_title"]),
    ]))

    paragraphs = [Paragraph(p, styles["body"]) for p in pattern["paragraphs"]]

    if chart_path is not None and paragraphs:
        n_lead = min(6, max(1, len(paragraphs) - 1))
        lead = paragraphs[:n_lead]
        rest = paragraphs[n_lead:]

        w_in, h_in = CHART_FIGSIZE_IN[figsize_key]
        caption_style = styles["hero_caption"] if is_hero else styles["caption"]
        # Rich captions from HERO_FIGURE_CAPTIONS are used regardless of
        # is_hero — what differs is just the style (hero_caption is larger;
        # caption is the smaller inline-chart variant). Falls back to a
        # generic "Figure N." string when no entry exists for the slot.
        caption_text = HERO_FIGURE_CAPTIONS.get(slot, f"Figure {pattern['number']}.")
        chart_res = ChartReservation(
            slot, chart_path, w_in, h_in, manifest,
            debug=debug,
            caption=caption_text,
            caption_style=caption_style,
        )

        if is_hero:
            # Hero: title \u2192 chart \u2192 body by default. Per-finding override
            # via pattern["n_lead"] in the content module \u2014 some findings
            # need lead body BEFORE the chart to fill leftover space on
            # the current page (e.g., F3 wants 3 paragraphs before its
            # chart so page 8 dead space gets filled by body before chart
            # defers to page 9). Default 0 is "chart immediately after
            # title," which pulls charts as early as possible.
            n_paragraphs = len(paragraphs)
            n_lead = pattern.get("n_lead", 0)
            n_lead = max(0, min(n_lead, n_paragraphs))   # clamp to valid range
            lead = paragraphs[:n_lead]
            tail = paragraphs[n_lead:]

            if lead:
                s.append(BalancedColumns(
                    lead, nCols=2, innerPadding=GUTTER,
                    spaceBefore=4, spaceAfter=10,
                    needed=30,
                ))
                s.append(Spacer(1, 8))
            s.append(chart_res)
            if tail:
                s.append(Spacer(1, 8))
                s.append(BalancedColumns(
                    tail, nCols=2, innerPadding=GUTTER,
                    spaceBefore=4, spaceAfter=10,
                    needed=30,
                ))
        else:
            # NON-HERO: chart embedded in column 1 of BalancedColumns(2).
            # Text flows top-to-bottom in column 1 (with chart at top of
            # col 1), then jumps to top of column 2. Standard newspaper-
            # style 2-column layout where the chart is just an element
            # within column 1's flow.
            #
            # All body paragraphs (lead + rest) go in this single BC after
            # the chart. The BC's internal balancing handles everything:
            # chart in col 1 top, body fills col 1 below chart, and col 2
            # fills top-to-bottom. When leftover space on the previous
            # pattern's last page is small, BC defers to the next page;
            # when it's large, BC starts there and overflows naturally.
            # NON-HERO sandwich layout:
            # - Lead BC with 1-2 lead paragraphs fills the leftover space on
            #   the previous pattern's last page.
            # - Main BC has the chart at the top of col 1 + remaining body
            #   paragraphs flowing in col 1 below chart and col 2 from top.
            #
            # n_lead_inner kept small (2) so most of the body stays in the
            # main BC alongside the chart. Without this, a long lead BC
            # claims most of the available column space on the page where
            # the finding starts, and the main BC (chart + rest) defers to
            # the next page even when the chart could have fit on the
            # current page.
            n_lead_inner = min(2, max(1, len(paragraphs) - 1))
            lead = paragraphs[:n_lead_inner]
            rest = paragraphs[n_lead_inner:]

            if lead:
                # Lead BC: needed=30 (well below default 72) so the lead
                # body starts laying out even when there's only ~30pt of
                # space left after the title in the previous frame. This
                # keeps the body directly under the title (no orphan)
                # instead of deferring the lead BC to a fresh page.
                s.append(BalancedColumns(
                    lead, nCols=2, innerPadding=GUTTER,
                    spaceBefore=4, spaceAfter=8,
                    needed=30,
                ))

            # Main BC: chart at col 1 top, body wraps. needed=270 restored
            # to prevent BC from collapsing to single-column when there
            # isn't enough vertical space to balance content across two
            # columns. v0.8.1 attempt to drop this to 30 caused F5 to
            # render as one column \u2014 reverting to 270 (the v0.7 value).
            main_content: list = [chart_res, Spacer(1, 8)] + rest
            s.append(BalancedColumns(
                main_content, nCols=2, innerPadding=GUTTER,
                spaceBefore=4, spaceAfter=10,
                needed=270,
            ))
    else:
        # No chart available — just body in BC
        s.append(BalancedColumns(
            paragraphs, nCols=2, innerPadding=GUTTER,
            spaceBefore=4, spaceAfter=10,
        ))

    return s


# Per-pattern figure descriptors used on hero spreads. Brief, factual,
# distinct from the section title (which already appeared on the body page).
HERO_FIGURE_CAPTIONS = {
    "hero_f1_drift_scatter": (
        "Figure 1 \u00b7 Per-brand t<sub size='6'>1</sub>\u2192t<sub size='6'>2</sub> drift across 5 "
        "categories on the matched subset (n=103 brand-level deltas). "
        "88.3% within \u00b15pp; 99.0% within \u00b110pp; no brand "
        "exceeds \u00b120pp. The empirical noise floor of one-week AI "
        "Presence measurement on the matched subset is approximately "
        "\u00b15pp for the modal brand."
    ),
    "hero_f2_leaderboard": (
        "Figure 2 \u00b7 Top-3 brands at t<sub size='6'>1</sub> remain in top-5 at "
        "t<sub size='6'>2</sub> across all 5 categories. Each panel is one category; "
        "asterisk and copper coloring mark t<sub size='6'>1</sub> top-three brands. "
        "Leaderboard composition preserved with no exceptions."
    ),
    "hero_f3_variance": (
        "Figure 3 \u00b7 Within-category brand-presence stdev at "
        "t<sub size='6'>1</sub> vs t<sub size='6'>2</sub>; categories sorted by t<sub size='6'>2</sub> variance. "
        "Personal finance highest dispersion at both waves; running "
        "shoes lowest. Spearman <font name='Helvetica'>\u03c1</font> = 0.8 across the 5 categories, "
        "above the 0.7 H3 threshold."
    ),
    "hero_f4_mint": (
        "Figure 4 \u00b7 Mint phantom-brand persistence at gross "
        "Presence in personal finance. The \u00b15pp stability band "
        "around t<sub size='6'>1</sub>'s 44.8% is shaded; t<sub size='6'>2</sub> lands at 41.7% "
        "(\u22123.1pp). Predicted-stability outcome confirmed."
    ),
    "hero_f5_pattern4": (
        "Figure 5 \u00b7 H5 Pattern 4 sensitivity. Strict Spanish "
        "(Castillo de Canena, N\u00fa\u00f1ez de Prado) at 11.5pp "
        "passes the 12.5pp threshold; +Graza pushes the cohort to "
        "14.2pp and breaches. K-beauty at 1.0pp passes the 5pp "
        "threshold. The 2.7-point swing between strict and inclusive "
        "is entirely Graza \u2014 the diagnostic case isolating brand-"
        "marketing-language from country-of-origin."
    ),
    "hero_f6_spread": (
        "Figure 6 \u00b7 Per-brand cross-model spread (Sonnet vs gpt-"
        "5.4-mini) Pearson correlation between t<sub size='6'>1</sub> and t<sub size='6'>2</sub> by "
        "category. Dashed line marks the 0.7 H6 threshold; all 5 "
        "categories clear it. Cross-model relative behavior is "
        "preserved across the wave interval."
    ),
    "hero_f7_pattern1": (
        "Figure 7 \u00b7 Post-hoc Pattern 1 cross-model spread by "
        "category at t<sub size='6'>1</sub> and t<sub size='6'>2</sub>. Spearman <font name='Helvetica'>\u03c1</font> = 0.800 "
        "(t<sub size='6'>1</sub>/t<sub size='6'>2</sub>); <font name='Helvetica'>\u03c1</font> = 0.900 (t<sub size='6'>2</sub> vs v0.6 narrative "
        "ordering). Personal finance widens at t<sub size='6'>2</sub>; project "
        "management narrows; both shifts within H1's empirical noise "
        "floor but in directions that strengthen v0.6's stated "
        "ordering."
    ),
    "hero_mode_distribution": (
        "Figure 8 \u00b7 Exploratory mode-distribution shifts on the "
        "matched subset. t<sub size='6'>1</sub> left, t<sub size='6'>2</sub> right per category. "
        "Largest shifts in PM software (+7.3pp brand mode), olive oil "
        "(\u22128.3pp brand mode), skincare (\u22126.2pp component "
        "mode). Reported as a calibration baseline for a v0.10 pre-"
        "registered mode-stability hypothesis."
    ),
    "hero_pattern_matrix": (
        "Figure 9 \u00b7 v0.6 framework pattern replication summary "
        "at v0.9. Pattern 1 cross-model spread replicates across all "
        "5 categories; Pattern 4 discourse-language bias replicates "
        "strict in the 2 cross-lingual categories where tested; "
        "Pattern 6 phantom-brand replicates in personal finance "
        "(Mint). Bottom row shows brand-mode share at t<sub size='6'>2</sub>."
    ),
    # v0.10 figure captions
    "hero_f1_valence": (
        "Figure 1 \u00b7 Distribution of the v0.7 5-class valence output "
        "across both waves before mapping to the v0.10 binary. "
        "<i>status_correction</i> (the strongest caveat type \u2014 explicit "
        "\u201cMint is decommissioned/closed/sunset\u201d framing) dominates "
        "both waves. <i>historical_reference</i> and <i>live_with_caveat</i> "
        "make up the remainder of caveated cases. Zero <i>ambiguous</i> "
        "classifications were produced; the E3 sensitivity mapping is "
        "therefore identical to the primary mapping."
    ),
    "hero_f2_h2_split": (
        "Figure 2 \u00b7 Per-wave naive vs caveated phantom-presence "
        "breakdown for the matched two-model subset. At t<sub size='6'>1</sub>, "
        "all 43 Mint mentions carried some form of caveat; zero were naive. "
        "At t<sub size='6'>2</sub>, 39 of 40 carried caveats and one was naive. "
        "The single naive case is a Sonnet 4.6 response listing Mint at the "
        "top of \u201cFree Options\u201d with present-tense feature description "
        "and explicit recommendation as \u201cthe most common starting point "
        "for beginners.\u201d No caveat anywhere in the response."
    ),
    "hero_f3_decoupling": (
        "Figure 3 \u00b7 Directional decoupling of gross Presence and "
        "naive-phantom rate across t<sub size='6'>1</sub> \u2192 t<sub size='6'>2</sub>. "
        "Gross Presence falls from 44.79% to 41.67% (\u0394 = \u22123.12pp) "
        "while the naive rate rises from 0.00% to 2.50% (\u0394 = +2.50pp). "
        "The directions are opposite; the magnitudes are comparable in "
        "absolute terms. At the matched-subset n observed (43 and 40), the "
        "pattern is noise-dominated and reported as diagnostic only per "
        "pre-reg \u00a72 H3."
    ),
    # v0.11 figure captions
    "f1_scatter_t1": (
        "Figure 1 \u00b7 Per-brand AI Presence (matched subset, Sonnet 4.6 + "
        "GPT-5.4-mini, PM software) against Google Trends rescaled mean at "
        "t<sub size='6'>1</sub>. Worldwide region. Log-y axis. Pivot brand Asana indexed "
        "to 100 by construction. Spearman <font name='Helvetica'>\u03c1</font> = 0.496 "
        "(p<sub size='6'>1t</sub> = 0.021); Pearson r = 0.544. n = 17."
    ),
    "f2_scatter_t2": (
        "Figure 2 \u00b7 Same shape at t<sub size='6'>2</sub>. The cross-wave visual "
        "stability is the H2 finding: Spearman <font name='Helvetica'>\u03c1</font> = 0.476; "
        "|\u0394<font name='Helvetica'>\u03c1</font>| from t<sub size='6'>1</sub> = 0.020. "
        "Whatever the construct is, it reproduces."
    ),
    "f3_rank_shift_t1": (
        "Figure 3 \u00b7 Slope chart: each brand's rank by AI Presence (left) "
        "connected to its rank by Trends (right) at t<sub size='6'>1</sub>. Steep slopes "
        "indicate construct divergence. Extreme cases (|\u0394rank| \u2265 8) "
        "highlighted in copper. Linear (top-left) and Todoist (mid-right) anchor "
        "the divergence diagnostic discussed in Finding 3."
    ),
    "f4_partial_residual_t1": (
        "Figure 4 \u00b7 H4 partial correlation visualisation. Rank residuals on "
        "both axes after OLS on rank-transformed brand age and tier ordinal. "
        "Partial Spearman <font name='Helvetica'>\u03c1</font> = 0.407 (p<sub size='6'>1t</sub> = 0.066), "
        "missing both the moderate-to-strong threshold and (at t<sub size='6'>1</sub>) "
        "the significance bar."
    ),
}


def _slot_lookup(slot_key: str) -> tuple[str | None, str | None]:
    """Map a slot_key to (filename, figsize_key). Centralized so the hero spread
    builder can reuse the table without duplicating it."""
    table = {
        # v0.9 Longitudinal Re-Baseline findings (kept for cross-version reuse)
        "hero_f1_drift_scatter":      ("chart_v09_h1_drift_scatter_6col.pdf",        "6_col_v09_drift"),
        "hero_f2_leaderboard":        ("chart_v09_h2_leaderboard_6col.pdf",          "6_col_v09_leaderboard"),
        "hero_f3_variance":           ("chart_v09_h3_within_cat_variance_6col.pdf",  "6_col_v09_variance"),
        "hero_f4_mint":               ("chart_v09_h4_mint_persistence_4col.pdf",     "4_col_v09_mint"),
        "hero_f5_pattern4":           ("chart_v09_h5_pattern4_sensitivity_6col.pdf", "6_col_v09_pattern4"),
        "hero_f6_spread":             ("chart_v09_h6_cross_model_spread_6col.pdf",   "6_col_v09_h6"),
        "hero_f7_pattern1":           ("chart_v09_pattern1_spread_6col.pdf",         "6_col_v09_pattern1"),
        "hero_mode_distribution":     ("chart_v09_mode_distribution_6col.pdf",       "6_col_v09_modes"),
        "hero_pattern_matrix":        ("chart_v09_pattern_matrix_6col.pdf",          "6_col_v09_matrix"),
        # v0.10 Naive-Phantom Rate Stability findings
        "hero_f1_valence":            ("chart_v10_valence_distribution.pdf",         "6_col_v10_valence"),
        "hero_f2_h2_split":           ("chart_v10_h2_naive_caveated.pdf",            "6_col_v10_h2"),
        "hero_f3_decoupling":         ("chart_v10_h3_decoupling.pdf",                "6_col_v10_h3"),
        # v0.11 PM Software x Google Trends Construct Validity findings
        "f1_scatter_t1":              ("chart_v11_h1_scatter_t1_6col.pdf",           "6_col_v11_scatter"),
        "f2_scatter_t2":              ("chart_v11_h1_scatter_t2_6col.pdf",           "6_col_v11_scatter"),
        "f3_rank_shift_t1":           ("chart_v11_h3_rank_shift_t1_6col.pdf",        "6_col_v11_rankshift"),
        "f4_partial_residual_t1":     ("chart_v11_h4_partial_residual_t1_6col.pdf",  "6_col_v11_partial"),
    }
    return table.get(slot_key, (None, None))


def build_hypothesis_scoring_story(styles: dict) -> list:
    """Render the HYPOTHESIS_SCORING section as a paragraph + table.

    Mirrors the closing-data-summary role the v0.6 aggregate matrix played,
    but in tabular form because the v0.7 data is inherently row-structured
    (one hypothesis per row) rather than matrix-structured."""
    s = []
    s.append(Spacer(1, 4))
    s.append(Paragraph(content.HYPOTHESIS_SCORING["heading"], styles["h1"]))
    s.append(Spacer(1, 4))
    s.append(Paragraph(content.HYPOTHESIS_SCORING["intro"], styles["body_lead"]))
    s.append(Spacer(1, 10))

    # Build table data: header row + body rows.
    # Body width is CONTENT_W = 540pt. Column widths chosen to fit:
    # H: 28pt (just "H1"-"H8"), Prediction: 175pt, Result: 200pt, Status: 137pt.
    header_style = ParagraphStyle(
        "scoring_header",
        parent=styles["body"],
        fontName=styles["body"].fontName.replace("Regular", "Bold")
                 if "Regular" in styles["body"].fontName else styles["body"].fontName,
        fontSize=8.5,
        textColor=HexColor("#37237B"),
        leading=11,
    )
    cell_style = ParagraphStyle(
        "scoring_cell",
        parent=styles["body"],
        fontSize=8,
        leading=10.5,
    )
    h_cell_style = ParagraphStyle(
        "scoring_h",
        parent=cell_style,
        fontName=header_style.fontName,
    )
    status_styles = {
        "confirmed": ParagraphStyle(
            "status_confirmed", parent=cell_style,
            fontName=header_style.fontName,
        ),
        "partial": cell_style,
        "disconfirmed": cell_style,
        "descriptive": ParagraphStyle(
            "status_descriptive", parent=cell_style,
            fontName=cell_style.fontName,
        ),
    }

    # Header row
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
    tbl = Table(
        table_data,
        colWidths=[28, 175, 200, 137],
        style=TableStyle([
            # Header row: thick rule above, thin rule below
            ("LINEABOVE",  (0, 0), (-1, 0), 1.2, indigo),
            ("LINEBELOW",  (0, 0), (-1, 0), 0.5, indigo),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
            ("TOPPADDING",    (0, 0), (-1, 0), 6),
            # Body rows: thin rule between rows
            ("LINEBELOW",  (0, 1), (-1, -2), 0.3, lavender),
            ("BOTTOMPADDING", (0, 1), (-1, -1), 5),
            ("TOPPADDING",    (0, 1), (-1, -1), 5),
            # Final row: thick rule below
            ("LINEBELOW",  (0, -1), (-1, -1), 1.2, indigo),
            # Cell vertical alignment
            ("VALIGN",     (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING",  (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ]),
    )
    s.append(tbl)

    # ----------------------------------------------------------------------
    # Hypothesis details — fuller reasoning per H. Renders after the table on
    # the same spread page if it fits, else flows to the next page naturally.
    # ----------------------------------------------------------------------
    if hasattr(content, "HYPOTHESIS_DETAILS"):
        details = content.HYPOTHESIS_DETAILS
        s.append(Spacer(1, 16))

        # Sub-heading bound to the intro paragraph so they don't separate
        s.append(KeepTogether([
            Paragraph(details["heading"], styles["h2"]),
            Spacer(1, 4),
            Paragraph(details["intro"], styles["body_lead"]),
        ]))
        s.append(Spacer(1, 8))

        # Per-hypothesis paragraphs. Render in a 2-column BalancedColumns so
        # 8 short paragraphs fit compactly on the rest of the page rather
        # than stretching down a single column.
        h_paragraphs = []
        for h_id, body in details["items"]:
            h_paragraphs.append(Paragraph(body, styles["body"]))

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


def build_aggregate_spread(styles: dict, manifest: ChartManifest,
                            chart_dir: Path, debug: bool) -> list:
    """Aggregate matrix hero spread. Returns an empty list if the chart is
    missing so the caller can skip the page break entirely."""
    fname, figsize_key = _slot_lookup("hero_aggregate")
    chart_path = chart_dir / fname
    if not chart_path.exists():
        warnings.warn(
            f"Aggregate matrix chart missing ({chart_path.name}); "
            f"skipping the aggregate spread page entirely."
        )
        return []
    s = []
    s.append(Spacer(1, 4))
    s.append(Paragraph("Aggregate matrix", styles["h1"]))
    s.append(Paragraph(
        "The full pattern \u00d7 category map. Each cell summarizes how strongly the "
        "pattern shows up in that category. The bottom row tracks the three response "
        "modes by category.",
        styles["body_lead"]))
    s.append(Spacer(1, 6))
    w_in, h_in = CHART_FIGSIZE_IN[figsize_key]
    s.append(ChartReservation(
        "hero_aggregate", chart_path, w_in, h_in, manifest,
        debug=debug,
        caption=("Figure B \u00b7 Aggregate matrix: six patterns \u00d7 five categories. "
                 "Cell intensity is qualitative \u2014 strong / moderate / weak / not observed. "
                 "Bottom row records mode-activation across categories."),
        caption_style=styles["hero_caption"],
    ))
    return s


def build_closing_story(styles: dict, brand: dict) -> list:
    s = []
    s.append(Spacer(1, CONTENT_H * 0.04))

    # About Third System — system overview, medium length, leads the closing
    # page so the reader leaves with a framing of what the framework is.
    s.append(Paragraph("About the Third System", styles["h1"]))
    s.append(Spacer(1, 4))
    s.append(Paragraph(boilerplate.SYSTEM_OVERVIEW["medium"], styles["body_lead"]))
    s.append(Spacer(1, 16))

    # Authored by
    s.append(Paragraph("<b>Authored by</b>", styles["body_lead"]))
    for line in content.CLOSING["byline_long"]:
        s.append(Paragraph(line, styles["body"]))
    s.append(Spacer(1, 10))

    # Methodology disclaimer.
    #
    # TEMPLATE-LEVEL FIXES (applied here, future reports inherit by copying
    # this block):
    #
    # 1. Brand JSON's methodology_standard hardcodes "(current: v0.3)" \u2014 the
    #    methodology version of the v0.6 cross-category report. Each report
    #    follows a different protocol version; v0.7 Phase 2 BBB uses the AIAS
    #    Presence Measurement Protocol v1.0 (locked 2026-05-04). We override
    #    the version reference here per-report. Future reports update the
    #    REPORT_PROTOCOL_VERSION constant below.
    REPORT_PROTOCOL_VERSION = "v1.1"
    methodology_text = brand["disclaimers"]["methodology_standard"].replace(
        "(current: v0.3)",
        f"(current: {REPORT_PROTOCOL_VERSION})",
    )
    s.append(Paragraph("<b>Methodology</b>", styles["body_lead"]))
    s.append(Paragraph(methodology_text, styles["disclaimer"]))
    s.append(Spacer(1, 10))

    # Citation
    #
    # TEMPLATE-LEVEL FIX: surname-first byline order per Spanish-name
    # convention. "Gonzalez Castro" is the surname pair, "Pablo Ulpiano" is
    # the given-name pair. Citation form is "Gonzalez Castro, P. U. (year)."
    # Brand JSON's citation.format field has the inverted order; this
    # hardcoded version is the corrected template that future reports copy.
    s.append(Paragraph("<b>Citation</b>", styles["body_lead"]))
    citation_text = (
        "Gonzalez Castro, P. U. (2026). "
        "<i>PM Software \u00d7 Google Trends Construct Validity: AI Presence Index "
        "v0.11 \u2014 Phase 3 pilot</i>. "
        "Third System. thirdsystem.ai/v11-pm-trends-construct-validity"
    )
    s.append(Paragraph(citation_text, styles["disclaimer"]))
    s.append(Spacer(1, 10))

    # Datasets
    s.append(Paragraph("<b>Underlying datasets</b>", styles["body_lead"]))
    for ds in content.CLOSING["datasets"]:
        s.append(Paragraph(ds, styles["disclaimer"]))
    s.append(Spacer(1, 10))

    # Methodology log + contact
    s.append(Paragraph(
        f"<b>Methodology log:</b> {content.CLOSING['methodology_log']}.",
        styles["disclaimer"]))
    s.append(Paragraph("<b>Inquiries:</b> hello@thirdsystem.ai", styles["disclaimer"]))

    return s


# ---------------------------------------------------------------------------
# Pass 2 — overlay chart PDFs onto the base PDF using pypdf
# ---------------------------------------------------------------------------

def overlay_charts(base_pdf_path: Path, manifest: ChartManifest,
                    out_pdf_path: Path) -> None:
    """
    For each chart slot, merge the chart PDF onto the recorded position on the
    recorded page of the base PDF. Vector-preserving.
    """
    reader = PdfReader(str(base_pdf_path))
    writer = PdfWriter(clone_from=reader)

    for slot in manifest.slots:
        if not slot.chart_path.exists():
            warnings.warn(f"Skipping merge for missing {slot.chart_path.name}; "
                          f"the page reservation remains blank.")
            continue
        chart_reader = PdfReader(str(slot.chart_path))
        chart_page = chart_reader.pages[0]

        # chart's MediaBox in points — should match figsize * 72
        cb = chart_page.mediabox
        chart_w = float(cb.width)
        chart_h = float(cb.height)

        # Reservation box dimensions in points
        target_w = slot.w_pt
        target_h = slot.h_pt

        sx = target_w / chart_w
        sy = target_h / chart_h
        # If sx and sy diverge by more than a hair, the chart wasn't rendered
        # at the locked figsize — flag but DO scale to the reservation rather
        # than letting the chart overflow.
        if abs(sx - sy) / max(sx, sy) > 0.02:
            warnings.warn(
                f"Chart {slot.chart_path.name} aspect mismatch: "
                f"chart {chart_w:.1f}x{chart_h:.1f}pt, reservation "
                f"{target_w:.1f}x{target_h:.1f}pt. Stretching to fit; "
                f"verify the chart was rendered at locked figsize."
            )
        # Use uniform scale = min to avoid distortion; small letterbox is OK.
        s = min(sx, sy)
        # Center within the reservation if scale is uniform
        offset_x = slot.x_pt + (target_w - chart_w * s) / 2
        offset_y = slot.y_pt + (target_h - chart_h * s) / 2

        # Apply scale, then translate by the page-space offset. With pypdf's
        # Transformation (PDF-standard 3x3 matrix in [a b 0; c d 0; e f 1]
        # form, points are row vectors multiplied on the LEFT), scale-then-
        # translate produces matrix entries (s, 0, 0, s, tx, ty) where tx and
        # ty are in PAGE coordinates (NOT pre-scaled chart coordinates).
        # Verified: chart point (0,0) -> page (offset_x, offset_y);
        #           chart point (cw, 0) -> page (offset_x + cw*s, offset_y).
        op = Transformation().scale(s, s).translate(offset_x, offset_y)
        writer.pages[slot.page_index].merge_transformed_page(chart_page, op)

    with open(out_pdf_path, "wb") as f:
        writer.write(f)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def build(*, debug_layout: bool = False,
          chart_dir: Path | None = None,
          output_path: Path | None = None) -> Path:
    """
    Build the v0.11 PM Software x Google Trends Construct Validity report.

    debug_layout=True draws thin dashed borders around chart reservations to
    make geometry visible during review. Use False for production output.
    """
    # Load assets
    with open(BRAND_JSON) as f:
        brand = json.load(f)
    with open(TOKENS_JSON) as f:
        tokens = json.load(f)

    palette = BrandPalette.from_json(brand)
    font = register_typography()
    styles = build_paragraph_styles(font, palette, tokens)

    print(f"[build_report_v11] palette: indigo={palette.indigo}, "
          f"soft_black={palette.soft_black}, paper={palette.paper}")
    print(f"[build_report_v11] typography: {font.name} "
          f"(brand_primary={font.is_brand_primary})")

    # Preconditions — v0.11 deposits live under /v11/, not in reports/output.
    # Default chart and report paths point at the deposit so the report sits
    # with the data.
    V11_DEPOSIT_ROOT = AIAS_ROOT / "osf" / "v11"
    chart_dir = chart_dir or (V11_DEPOSIT_ROOT / "figures")
    output_path = output_path or (V11_DEPOSIT_ROOT / "reports" / "v11_pmtrends_construct_validity.pdf")
    base_pdf = output_path.parent / "_v11_base.pdf"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Pre-flight: report which charts are present and which are missing.
    print(f"[build_report_v11] chart pre-flight (looking in {chart_dir})")
    expected_slots = [
        "f1_scatter_t1", "f2_scatter_t2",
        "f3_rank_shift_t1", "f4_partial_residual_t1",
    ]
    expected_files = set()
    for sk in expected_slots:
        fname, _ = _slot_lookup(sk)
        expected_files.add(fname)
        present = (chart_dir / fname).exists()
        status = "FOUND  " if present else "MISSING"
        print(f"  [{status}] {sk:34s} -> {fname}")

    # Also list every PDF actually present in chart_dir whose name starts with
    # 'chart_' — this surfaces filename mismatches at a glance.
    if chart_dir.exists():
        actual_charts = sorted(p.name for p in chart_dir.iterdir()
                                if p.is_file() and p.suffix.lower() == ".pdf"
                                and p.name.startswith("chart_v11"))
        if actual_charts:
            unexpected = [n for n in actual_charts if n not in expected_files]
            if unexpected:
                print(f"[build_report_v11] chart files in dir not matched by any v11 slot:")
                for n in unexpected:
                    print(f"  [UNUSED ] {n}")

    manifest = ChartManifest()
    doc = V06DocTemplate(
        str(base_pdf),
        palette=palette, font=font, styles=styles,
        manifest=manifest,
        debug_layout=debug_layout,
        title="PM Software \u00d7 Google Trends Construct Validity \u2014 AI Presence Index v0.11",
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

    # --- Cross-category leaderboards hero (placement Q3 default).
    # Switch to spread template + force a PageBreak. Template switches in
    # ReportLab happen at page boundaries, not mid-page — the leaderboards
    # chart needs the full-width spread frame (540pt), so we have to break
    # to a fresh page even if the previous one isn't full.
    leaderboards_flow = build_leaderboards_spread(styles, manifest, chart_dir, debug_layout)
    if leaderboards_flow:
        story.append(NextPageTemplate("spread"))
        story.append(PageBreak())
        story.extend(leaderboards_flow)

    # --- What we measured (methodology) — body template ---
    story.append(NextPageTemplate("body"))
    story.append(PageBreak())
    for f_ in build_what_we_measured_story(styles):
        story.append(f_)

    # --- Three modes (skipped for v0.7 Phase 2 — BBB content has no THREE_MODES) ---
    if hasattr(content, "THREE_MODES"):
        story.append(Spacer(1, 8))
        for f_ in build_three_modes_story(styles):
            story.append(f_)

    # --- Findings 1-5 ---
    # ALL findings render on the SPREAD template (single wide frame with
    # BalancedColumns(2) providing the column split). Same architecture as
    # v0.6 patterns; section label is rendered as "FINDING" (see
    # build_pattern_unified).
    story.append(NextPageTemplate("spread"))
    story.append(PageBreak())
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

    # --- Hypothesis scoring (replaces v0.6 aggregate matrix as the closing
    # data summary). Uses HYPOTHESIS_SCORING from v09_rebaseline_content. Renders
    # on the SPREAD template because the scoring table needs the full 540pt
    # content width \u2014 it does not fit in the body template's 3-col frames.
    if hasattr(content, "HYPOTHESIS_SCORING"):
        story.append(NextPageTemplate("spread"))
        story.append(PageBreak())
        story.extend(build_hypothesis_scoring_story(styles))
    # --- Closing page ---
    story.append(NextPageTemplate("closing"))
    story.append(PageBreak())
    for f_ in build_closing_story(styles, brand):
        story.append(f_)

    # Build base PDF
    doc.build(story)
    print(f"[build_report_v11] base PDF written: {base_pdf} "
          f"({len(manifest.slots)} chart reservations)")
    for slot in manifest.slots:
        ok = "OK" if slot.chart_path.exists() else "MISSING"
        print(f"  [{ok}] {slot.slot_key:34s} -> page {slot.page_index + 1:>2} "
              f"@({slot.x_pt:6.1f},{slot.y_pt:6.1f}) "
              f"{slot.w_pt:6.1f}x{slot.h_pt:6.1f}pt  ({slot.chart_path.name})")

    # Pass 2 — overlay charts
    overlay_charts(base_pdf, manifest, output_path)
    print(f"[build_report_v11] FINAL PDF written: {output_path}")

    # Page count check — v0.11 is single-category with 4 findings, similar
    # to v0.10's scope plus one extra finding.
    final_pages = len(PdfReader(str(output_path)).pages)
    print(f"[build_report_v11] page count: {final_pages}")
    if final_pages < 9 or final_pages > 20:
        warnings.warn(
            f"Page count {final_pages} is outside the 8-18 target band. "
            "Adjust body sizing or section length if final PDF reads long/short."
        )

    return output_path


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--debug-layout", action="store_true",
                     help="Draw faint borders around chart reservations.")
    ap.add_argument("--chart-dir", type=Path, default=None,
                     help="Directory containing chart_*.pdf files. "
                          "Defaults to ./output relative to this script.")
    ap.add_argument("--output", type=Path, default=None,
                     help="Output PDF path. Defaults to ~/aias/osf/v11/reports/v11_pmtrends_construct_validity.pdf")
    args = ap.parse_args()
    build(
        debug_layout=args.debug_layout,
        chart_dir=args.chart_dir,
        output_path=args.output,
    )
