#!/usr/bin/env python3
"""
v0.26 Automotive — typesetting pipeline.

Phantom Brand Persistence stress-test on a heritage-saturated automotive
substrate (n=24, four cells: Heritage / Disruptor / Mass-Legacy / Defunct).
First prospective phase under v1.6 methodology lock. The lead hypothesis
H_Phantom_Defunct tests whether discontinued corporate brands (Pontiac,
Oldsmobile, Plymouth, Mercury, Saturn — all closed 2001–2010) surface in
unprompted current-tense Recall as if currently active. Cell D provides
the pure-phantom upper-bound test that no prior substrate could support.
Substrate anchor base extends 5 → 6 families.
Brand-format report companion to the v0.26 SSRN paper (SSRN TBD).

Forked from build_report_v21.py with surgical changes:
  - Imports v26_automotive_content instead of v21_cosmetics_content
  - HERO_FIGURE_CAPTIONS rewritten as v0.26 templates (4 entries; the
    fourth — f4_phantom_defunct — is net new for v0.26)
  - _slot_lookup table updated for the 4 v0.26 brand-format chart filenames
    (all produced by build_charts_v26.py at reports/figs/v26/):
      f1_cp_distribution      -> chart_01_cp_distribution.pdf
      f2_dissociation_scatter -> chart_02_dissociation_scatter.pdf
      f3_channel_asymmetry    -> chart_03_channel_asymmetry.pdf
      f4_phantom_defunct      -> chart_04_phantom_defunct.pdf   (NEW)
  - CHART_FIGSIZE_IN extended with v0.26 figsize keys (4 entries; v0.21
    entries preserved for cross-version reuse)
  - Header right text updated: "Phantom Brand Persistence · v0.26 · May 2026"
  - Citation updated: v0.26 automotive, SSRN TBD
  - Output filename: v26_amazon_bsr_predictive_validity_report.pdf
  - REPORT_PROTOCOL_VERSION: v1.5 → v1.6 (first prospective v1.6 phase)
  - Chart directory: reports/figs/v26/
  - Deposit root: osf/v26/
  - Page count target band: 8-14 pages (v0.26 has 4 findings vs v0.21's 3;
    band kept at 8-14 — the fourth finding may push toward the upper end)

Inputs:
  - brand/third_system_brand.json        (v1.5+)
  - brand/design_tokens_template.json    (IDML extract)
  - reports/figs/v26/chart_01_*.pdf      (4 brand-format charts; all from
                                          build_charts_v26.py)

Output:
  - osf/v26/reports/v26_amazon_bsr_predictive_validity_report.pdf

Run for v0.26:
    python3 ~/aias/scripts/build_charts_v26.py
    python3 ~/aias/reports/build_report_v26.py

Locked rules followed (same as v0.6 - v0.21):
  - Image-placeholder rectangles in master spreads stay BLANK (no fill colors).
  - Template's #FF001A red is overridden to brand primary (Indigo #37237B per
    third_system_brand.json v1.5+).
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

BRAND_JSON = BRAND_DIR / "third_system_brand.json"
TOKENS_JSON = BRAND_DIR / "design_tokens_template.json"
SPECS_JSON = BRAND_DIR / "report_specs.json"
SOURCE_TEXT = BRAND_DIR / "v06_source_text.md"
WORDMARK_SVG = BRAND_DIR / "THIRDSYSTEM_Logo.svg"
LOCKUP_SVG = BRAND_DIR / "THIRDSYSTEM_AIPT_Logo.svg"

# Make `import v26_amazon_bsr_predictive_validity_content` work regardless of working directory.
sys.path.insert(0, str(SCRIPT_DIR))
import v26_amazon_bsr_predictive_validity_content as content  # noqa: E402
import tsboilerplate as boilerplate  # noqa: E402

# ---------------------------------------------------------------------------
# Content adapter — reshape flat v0.26 content module into builder structures
# ---------------------------------------------------------------------------

# COVER: add missing keys the cover story builder expects
if "byline_short" not in content.COVER:
    content.COVER["byline_short"] = "Pablo Ulpiano González Castro"
if "tagline" not in content.COVER:
    content.COVER["tagline"] = "AIAS™ Measurement Program · Discriminant Validity"

# EXEC_SUMMARY: string → list of paragraphs
if isinstance(content.EXEC_SUMMARY, str):
    content.EXEC_SUMMARY = [p.strip() for p in content.EXEC_SUMMARY.split("\n\n") if p.strip()]

# LEAD_DECK: list of stat dicts → single string (stat block rendered separately)
_LEAD_DECK_STATS = content.LEAD_DECK if isinstance(content.LEAD_DECK, list) else []
if isinstance(content.LEAD_DECK, list):
    content.LEAD_DECK = " · ".join(
        f"<b>{d['metric']}</b> {d['label']}" for d in content.LEAD_DECK
        if isinstance(d, dict))

# WHAT_WE_MEASURED: string → dict {heading, paragraphs}
if isinstance(content.WHAT_WE_MEASURED, str):
    _paras = [p.strip() for p in content.WHAT_WE_MEASURED.split("\n\n") if p.strip()]
    content.WHAT_WE_MEASURED = {"heading": "What we measured", "paragraphs": _paras}

# PATTERNS: {id, title, body} → {number, title, paragraphs, chart_slot}
_PATTERN_CHART_MAP = {
    1: "f1_cp_vs_bsr_scatter",
    2: None,
    3: None,
    4: None,
    5: None,
}
if content.PATTERNS and isinstance(content.PATTERNS[0], dict):
    _new_patterns = []
    for i, p in enumerate(content.PATTERNS):
        if "id" in p:
            _title = p["title"]
            _body = p["body"]
        else:
            _title = p.get("label", f"Pattern {i+1}")
            _body = p.get("text", "")
        _paras = [para.strip() for para in _body.split("\n\n") if para.strip()]
        _new_patterns.append({
            "number": i + 1,
            "title": _title,
            "paragraphs": _paras,
            "chart_slot": _PATTERN_CHART_MAP.get(i + 1),
            "chart_after_text": False,
        })
    content.PATTERNS = _new_patterns

# HYPOTHESIS_SCORING: list of dicts → dict {heading, intro, rows}
if isinstance(content.HYPOTHESIS_SCORING, list) and content.HYPOTHESIS_SCORING and isinstance(content.HYPOTHESIS_SCORING[0], dict):
    _rows = []
    for h in content.HYPOTHESIS_SCORING:
        _status_class = "confirmed" if h["verdict"] == "CONFIRMED" else (
            "partial" if h["verdict"] == "PARTIAL" else "disconfirmed")
        _rows.append((h["id"], h["label"], h["detail"], h["verdict"], _status_class))
    content.HYPOTHESIS_SCORING = {
        "heading": "Hypothesis scoring",
        "intro": "Four pre-registered propositions tested across the v0.26 cross-substrate panel (kitchen knives, audiophile headphones, skincare, cosmetics).",
        "rows": _rows,
    }

# HYPOTHESIS_DETAILS: string → dict {heading, intro, items}
if isinstance(content.HYPOTHESIS_DETAILS, str):
    _detail_paras = [p.strip() for p in content.HYPOTHESIS_DETAILS.split("\n\n") if p.strip()]
    content.HYPOTHESIS_DETAILS = {
        "heading": "Detailed hypothesis results",
        "intro": "",
        "items": [(f"P{i+1}", p) for i, p in enumerate(_detail_paras)],
    }

# LIMITATIONS: string → dict {heading, paragraphs}
if isinstance(content.LIMITATIONS, str):
    _paras = [p.strip() for p in content.LIMITATIONS.split("\n\n") if p.strip()]
    content.LIMITATIONS = {"heading": "Limitations", "paragraphs": _paras}

# WHATS_NEXT: string → dict {heading, paragraphs}
if isinstance(content.WHATS_NEXT, str):
    _paras = [p.strip() for p in content.WHATS_NEXT.split("\n\n") if p.strip()]
    content.WHATS_NEXT = {"heading": "What’s next", "paragraphs": _paras}

# CLOSING: string → dict {byline_long, datasets, methodology_log}
if isinstance(content.CLOSING, str):
    content.CLOSING = {
        "byline_long": [
            "Pablo Ulpiano González Castro",
            "School of Visual Arts, MPS Branding Program, New York, NY",
            "Third System™ (research entity)",
        ],
        "datasets": [
            "BSR data: osf.io/ec6wh/v26/data/v26_bsr_master.csv",
            "C_P retrofit: osf.io/ec6wh/v26/data/v16_cp_retrofit_aggregated.csv",
            "Scoring verdicts: osf.io/ec6wh/v26/v26_verdicts.json",
        ],
        "methodology_log": "v1.6 (SSRN 6816340)",
        "closing_text": content.CLOSING,
    }

# --- Akkurat Pro glyph-coverage fallback substitutions ----------------------
# Akkurat lacks several Unicode symbols. Substitute before any Paragraph parse.
# Same coverage-gap pattern as the subscript and arrow rules already in memory.
# Add new entries here as additional missing glyphs are discovered.
_AKKURAT_SUBS = {
    "\u2227": "&amp;",   # logical-and ∧ → ampersand entity (renders as &)
}

def _sanitize_akkurat(obj):
    """Recursively replace Akkurat-missing glyphs in any string content."""
    if isinstance(obj, str):
        for src, dst in _AKKURAT_SUBS.items():
            obj = obj.replace(src, dst)
        return obj
    if isinstance(obj, list):
        return [_sanitize_akkurat(x) for x in obj]
    if isinstance(obj, tuple):
        return tuple(_sanitize_akkurat(x) for x in obj)
    if isinstance(obj, dict):
        return {k: _sanitize_akkurat(v) for k, v in obj.items()}
    return obj

# Apply to every top-level content module attribute so all string fields get
# sanitized before Paragraph instantiation. HERO_FIGURE_CAPTIONS (in this file)
# gets the same treatment after definition below.
for _attr in dir(content):
    if _attr.startswith("_"):
        continue
    setattr(content, _attr, _sanitize_akkurat(getattr(content, _attr)))

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

# Chart figsize spec (inches).
CHART_FIGSIZE_IN = {
    # v0.11–v0.17 keys preserved for cross-version reuse (not used by v0.19 report)
    "6_col_v11_scatter":    (7.50, 5.00),
    "6_col_v11_rankshift":  (7.50, 6.50),
    "6_col_v11_partial":    (7.50, 5.30),
    "6_col_v12_pm_rankshift":     (7.50, 6.50),
    "6_col_v12_running_partial":  (7.50, 5.80),
    "6_col_v12_scale_mismatch":   (7.50, 6.00),
    "6_col_v12_h6_zones":         (7.50, 4.70),
    "6_col_v16_regime4":            (7.50, 6.50),
    "6_col_v16_per_category":       (7.50, 7.20),
    "6_col_v16_discourse_language": (7.50, 4.70),
    "6_col_v16_per_brand":          (7.50, 4.20),
    "6_col_v16_per_tradition":      (7.50, 7.20),
    "6_col_v17_mention_rates":  (7.50, 9.00),
    "6_col_v17_cell_collapse":  (7.50, 5.40),
    "6_col_v17_dissociation":   (7.50, 7.50),
    # v0.18 brand-format report keys preserved for cross-version reuse
    "6_col_v18_mention_rate_distribution": (7.50, 5.50),
    "6_col_v18_cell_attrition":            (7.50, 5.50),
    "6_col_v18_dissociation_scatter":      (7.50, 5.50),
    # v0.19 brand-format report keys — 3 charts at native figsize 7.5 × 5.5.
    # Matches build_charts_v19.py CHART_FIGSIZE = (7.5, 5.5).
    "6_col_v19_cp_distribution":      (7.50, 5.50),
    "6_col_v19_dissociation_scatter": (7.50, 5.50),
    "6_col_v19_channel_asymmetry":    (7.50, 5.50),
    # v0.20 brand-format report keys — 3 charts at native figsize 7.5 × 5.5.
    # Matches build_charts_v20.py CHART_FIGSIZE = (7.5, 5.5).
    "6_col_v20_cp_distribution":      (7.50, 5.50),
    "6_col_v20_dissociation_scatter": (7.50, 5.50),
    "6_col_v20_channel_asymmetry":    (7.50, 5.50),
    # v0.21 brand-format report keys — 3 charts at native figsize 7.5 × 5.5.
    # Matches build_charts_v21.py CHART_FIGSIZE = (7.5, 5.5).
    "6_col_v21_cp_distribution":      (7.50, 5.50),
    "6_col_v21_dissociation_scatter": (7.50, 5.50),
    "6_col_v21_channel_asymmetry":    (7.50, 5.50),
    # v0.26 B2B SaaS brand-format report keys — 4 charts.
    "6_col_v26_recall_by_brand":  (7.50, 9.00),
    "6_col_v26_mlt_frequency":    (7.50, 5.50),
    "6_col_v26_identity_load":    (7.50, 5.50),
    "6_col_v26_mlc_by_model":     (7.50, 5.50),
    "6_col_v26_phantom_gap":      (7.50, 5.00),
    "hero":                       (7.50, 5.00),
    "hero_short":                 (7.50, 3.50),
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
# Font registration (verbatim from build_report_v18.py)
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
# Paragraph styles (verbatim from build_report_v18.py)
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
                           fontSize=20, leading=24, spaceAfter=10),
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
                               fontSize=20, leading=22, spaceAfter=8),
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
# Chart slot tracker, reservation Flowable (verbatim from v0.18)
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
        raw_h_pt = height_in * 72.0
        nominal_h_pt = 400.0 if raw_h_pt > 500.0 else raw_h_pt

        # v0.26: auto-size reservation height to match the actual chart PDF's
        # aspect ratio. bbox_inches='tight' in build_charts_v26 produces
        # variable mediabox dimensions depending on side-panel content length,
        # so the stored CHART_FIGSIZE_IN aspect is no longer reliable. If the
        # chart PDF exists, read its mediabox and compute the height that
        # makes the chart fill the reservation width exactly at scale=sx.
        # This eliminates the dead-space-below-chart that was producing the
        # ~40-80pt figure-to-caption gap on charts 2-4.
        adjusted_h = nominal_h_pt
        if chart_path.exists():
            try:
                _r = PdfReader(str(chart_path))
                _mb = _r.pages[0].mediabox
                _cw, _ch = float(_mb.width), float(_mb.height)
                # Height to match chart aspect at reservation width:
                _h_at_reservation_w = self.chart_w_pt * (_ch / _cw)
                # Cap at nominal so a very-tall chart doesn't break page flow;
                # honor nominal as the MAX, use actual aspect when it's shorter.
                adjusted_h = min(_h_at_reservation_w, nominal_h_pt)
            except Exception:
                pass
        self.chart_h_pt = adjusted_h

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
            total_h = self.chart_h_pt + ch + 2   # was + 4 (v0.26 tightening)
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
        chart_y_local = self._caption_h + 2 if self.caption_p else 0   # was + 4
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
# DocTemplate (functionally verbatim from v0.18; only header right text changed)
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

        # v0.26 lead-page layout — REVERTED to v0.21 / aias_1_0 working pattern:
        # ONE full-width lead_top frame (STANDFIRST renders as single-column,
        # full content-width block — NOT BalancedColumns) + 2 lead_bottom frames
        # at 3-col widths each (LEAD_DECK and EXEC_SUMMARY render as 2-column
        # body-style flow). This is the pattern in aias_1_0 page 2.
        LEAD_TOP_H = 340.0
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
        c.drawRightString(PAGE_W - MARGIN, header_y - 8,
                           "Discriminant Validity \u00b7 v0.26 \u00b7 May 2026")

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
# Story builders (verbatim from v0.18)
# ---------------------------------------------------------------------------

def build_cover_story(styles: dict[str, ParagraphStyle]) -> list:
    s = []
    # Cover sizing tuned to match working aias_1_0 layout:
    #   - top spacer ~22% of CONTENT_H pushes title into upper-middle
    #   - byline → tagline gap: fixed 50pt so tagline sits predictably
    #     near the bottom regardless of subtitle length variance.
    # Previous CONTENT_H * 0.18 = 130pt bottom spacer was too large; for
    # a 67-word subtitle (~12 lines × 22pt leading = 264pt) it pushed total
    # cover stack past the 720pt content height and orphaned the tagline.
    s.append(Spacer(1, CONTENT_H * 0.22))
    s.append(Paragraph(content.COVER["title"], styles["cover_title"]))
    s.append(Paragraph(content.COVER["subtitle"], styles["cover_subtitle"]))
    s.append(Spacer(1, 18))
    s.append(Paragraph(
        f"{content.COVER['date']} &nbsp;&nbsp;\u00b7&nbsp;&nbsp; "
        f"{content.COVER['byline_short']}",
        styles["cover_byline"]))
    s.append(Spacer(1, 50))
    s.append(Paragraph(content.COVER["tagline"], styles["cover_tagline"]))
    return s


def build_lead_story(styles: dict[str, ParagraphStyle]) -> list:
    s = []
    # STANDFIRST: single-column, full content-width block in lead_top frame.
    # This is the working aias_1_0 pattern — NOT BalancedColumns.
    s.append(Paragraph(content.STANDFIRST, styles["standfirst"]))
    s.append(FrameBreak())
    # LEAD_DECK and EXEC_SUMMARY flow naturally through:
    #   lead_bottom_left (3-col width) → lead_bottom_right (3-col width)
    # → body template (2-col). NextPageTemplate hint set BEFORE EXEC_SUMMARY
    # so overflow goes to body, not another lead page.
    s.append(Paragraph(content.LEAD_DECK, styles["lead_deck"]))
    s.append(Spacer(1, 8))
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


def build_leaderboards_spread(styles, manifest, chart_dir, debug):
    return []


HERO_FIGURE_CAPTIONS = {
    "f1_cp_vs_bsr_scatter": (
        "Figure 1 \u00b7 AI Presence does not predict Amazon BSR. "
        "C_P (0\u20136) vs. Amazon Best Sellers Rank by substrate. "
        "Each panel shows listed brands with Spearman rho annotated. "
        "Kitchen knives, audiophile headphones, and skincare show "
        "indistinguishable-from-zero correlations; cosmetics shows "
        "the ceiling effect (all C_P\u2009=\u20096)."
    ),
    "f2_correlation_matrix": (
        "Figure 2 \u00b7 Component-level correlations. "
        "Spearman \u03C1 across AIAS components and Google Trends. "
        "C_P excluded (constant at 6/6 across all 24 brands, ceiling effect). "
        "Asterisks denote p\u2009<\u20090.05. "
        "Presence\u2013Trends \u03C1\u2009=\u20090.74; "
        "Identity Load\u2013Trends \u03C1\u2009=\u2009\u22120.18 (n.s.), "
        "confirming discriminant validity."
    ),
    "f3_cell_comparison": (
        "Figure 3 \u00b7 Cell-level convergence. "
        "Mean AIAS Presence and Google Trends by cell assignment. "
        "Cell A and Cell D anchor extremes on both measures. "
        "Kendall \u03C4\u2009=\u20090.67 (partial: B\u2013C swap on Trends)."
    ),
    "f4_identity_load": (
        "Figure 4 \u00b7 Identity Load by cell. "
        "Diverging bars show mean R_cat (category-anchored, left) and "
        "R_cult (cultural-footprint, right) per cell. "
        "Cell B (High-Identity Challengers) leads on cultural recall; "
        "Cell A (Enterprise Incumbents) dominates category recall. "
        "Cell D phantom brands show zero on both channels."
    ),
    "f5_residual": (
        "Figure 5 \u00b7 Presence\u2013Trends residual. "
        "Brands sorted by the gap between AI Presence and search interest. "
        "SAP is the sharpest outlier: near-maximum LLM recall, near-zero "
        "Google Trends signal \u2014 consistent with procurement-embedded "
        "AI Presence without consumer search behaviour."
    ),
}



def _slot_lookup(slot_key: str) -> tuple[str | None, str | None]:
    """Map a v0.26 brand-format slot_key to (filename, figsize_key)."""
    table = {
        "f1_cp_vs_bsr_scatter": (
            "chart_26_cp_vs_bsr_scatter.pdf",
            "hero",
        ),
    }
    return table.get(slot_key, (None, None))

def build_pattern_unified(pattern: dict, styles: dict,
                            manifest: ChartManifest,
                            chart_dir: Path, debug: bool) -> list:
    """v0.14+ vertical-flow pattern: heading -> text (2-col balanced) -> chart below."""
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
    s.append(PageBreak())

    s.append(KeepTogether([
        Spacer(1, 4),
        Paragraph(f"FINDING {pattern['number']:02d}", styles["pattern_number"]),
        Paragraph(pattern["title"], styles["pattern_title"]),
    ]))

    chart_block: list = []
    if chart_path is not None and figsize_key is not None:
        w_in, h_in = CHART_FIGSIZE_IN[figsize_key]
        # v0.26 hero slot names — 4 findings pattern (one more than v0.18-v0.21)
        is_hero = slot in (
            "f1_recall_by_brand",
            "f2_mlc_by_model",
            "f3_mlt_frequency",
            "f4_identity_load",
            "f5_phantom_gap",
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
            spaceBefore=2, spaceAfter=10, needed=30,
        )]

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

    # v0.26 protocol version — v1.6 (Phantom Brand Persistence increment Inc3)
    REPORT_PROTOCOL_VERSION = "v1.6"
    methodology_text = brand["disclaimers"]["methodology_standard"].replace(
        "(current: v0.3)",
        f"(current: {REPORT_PROTOCOL_VERSION})",
    )
    s.append(Paragraph("<b>Methodology</b>", styles["body_lead"]))
    s.append(Paragraph(methodology_text, styles["disclaimer"]))
    s.append(Spacer(1, 10))

    s.append(Paragraph("<b>Citation</b>", styles["body_lead"]))
    citation_text = (
        "González Castro, P. U. (2026). "
        "<i>What AI Presence Does Not Predict: Amazon Best Sellers Rank as "
        "Discriminant Validity Evidence for the AIAS Construct (v0.26)</i>. "
        "Third System. thirdsystem.ai/v26 (SSRN 6847678)"
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
# Pass 2 overlay (verbatim from v0.18)
# ---------------------------------------------------------------------------

def _measure_chart_bottom_whitespace_pt(chart_path: Path,
                                        chart_h_pt: float) -> float:
    """Detect the bottom blank margin of a chart PDF in points.
    Rasterizes the page, finds the last row containing non-paper pixels, and
    returns the height of pure-paper rows below that as pt. Returns 0 on any
    failure so the caller's behavior is unchanged.
    """
    try:
        from pdf2image import convert_from_path
        import numpy as np
    except ImportError:
        return 0.0
    try:
        # Render at modest DPI — we only need to find a horizontal threshold.
        pages = convert_from_path(str(chart_path), dpi=72)
        if not pages:
            return 0.0
        arr = np.array(pages[0].convert("L"))
        # "Paper" = brightness >= 250 (Akkurat source line at fontsize 7.5 italic
        # gray is well below this threshold).
        non_paper_rows = np.where((arr < 250).any(axis=1))[0]
        if non_paper_rows.size == 0:
            return 0.0
        last_content_row = int(non_paper_rows[-1])
        total_rows = arr.shape[0]
        blank_rows_below = total_rows - 1 - last_content_row
        # Convert image rows to points using the chart's known pt height.
        return (blank_rows_below / total_rows) * chart_h_pt
    except Exception:
        return 0.0


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
        # v0.26: scale = min(sx, sy) — was * 0.92 (8% safety margin). The
        # safety margin produced ~32pt of trapped whitespace at the bottom
        # of every chart reservation (since charts > 350pt are top-aligned),
        # widening the visual figure-to-caption gap. With CHART_FIGSIZE_IN
        # matched to build_charts_v26.py figsize, the margin is unnecessary.
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
          chart_dir: Path | None = None,
          output_path: Path | None = None) -> Path:
    with open(BRAND_JSON) as f:
        brand = json.load(f)
    with open(TOKENS_JSON) as f:
        tokens = json.load(f)

    palette = BrandPalette.from_json(brand)
    font = register_typography()
    styles = build_paragraph_styles(font, palette, tokens)

    print(f"[build_report_v26] palette: indigo={palette.indigo}, "
          f"soft_black={palette.soft_black}, paper={palette.paper}")
    print(f"[build_report_v26] typography: {font.name} "
          f"(brand_primary={font.is_brand_primary})")

    V22_DEPOSIT_ROOT = AIAS_ROOT / "osf" / "v26"
    # Charts live in reports/figs/v26/ (matches build_charts_v26.py default).
    chart_dir = chart_dir or (AIAS_ROOT / "reports" / "figs" / "v26")
    output_path = output_path or (V22_DEPOSIT_ROOT / "reports" / "v26_amazon_bsr_predictive_validity_report.pdf")
    base_pdf = output_path.parent / "_v26_base.pdf"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"[build_report_v26] chart pre-flight (looking in {chart_dir})")
    expected_slots = [
        "f1_scatter_presence_trends",
        "f2_correlation_matrix",
        "f3_cell_comparison",
        "f4_identity_load",
        "f5_residual",
    ]
    expected_files = set()
    for sk in expected_slots:
        fname, _ = _slot_lookup(sk)
        if fname is None:
            continue
        expected_files.add(fname)
        present = (chart_dir / fname).exists()
        status = "FOUND  " if present else "MISSING"
        print(f"  [{status}] {sk:35s} -> {fname}")

    if chart_dir.exists():
        actual_charts = sorted(p.name for p in chart_dir.iterdir()
                                if p.is_file() and p.suffix.lower() == ".pdf"
                                and p.name.startswith("chart_"))
        unexpected = [n for n in actual_charts if n not in expected_files]
        if unexpected:
            print(f"[build_report_v26] chart files in dir not used by brand-format report:")
            for n in unexpected:
                print(f"  [UNUSED ] {n}")

    manifest = ChartManifest()
    doc = V15DocTemplate(
        str(base_pdf),
        palette=palette, font=font, styles=styles,
        manifest=manifest, debug_layout=debug_layout,
        title="What AI Presence Does Not Predict \u2014 AIAS v0.26",
        author=content.CLOSING["byline_long"][0],
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

    # --- Findings 1–3 ---
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
    print(f"[build_report_v26] base PDF written: {base_pdf} "
          f"({len(manifest.slots)} chart reservations)")
    for slot in manifest.slots:
        ok = "OK" if slot.chart_path.exists() else "MISSING"
        print(f"  [{ok}] {slot.slot_key:35s} -> page {slot.page_index + 1:>2} "
              f"@({slot.x_pt:6.1f},{slot.y_pt:6.1f}) "
              f"{slot.w_pt:6.1f}x{slot.h_pt:6.1f}pt  ({slot.chart_path.name})")

    overlay_charts(base_pdf, manifest, output_path)
    print(f"[build_report_v26] FINAL PDF written: {output_path}")

    final_pages = len(PdfReader(str(output_path)).pages)
    print(f"[build_report_v26] page count: {final_pages}")
    if final_pages < 8 or final_pages > 14:
        warnings.warn(
            f"Page count {final_pages} is outside the 8-14 target band."
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
                     help="Output PDF path. Defaults to ~/aias/osf/v26/reports/v26_amazon_bsr_predictive_validity_report.pdf")
    args = ap.parse_args()
    build(
        debug_layout=args.debug_layout,
        chart_dir=args.chart_dir,
        output_path=args.output,
    )
