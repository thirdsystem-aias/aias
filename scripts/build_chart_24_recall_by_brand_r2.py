#!/usr/bin/env python3
"""
build_chart_24_recall_by_brand_r2.py
AIAS(TM) v0.24 - B2B SaaS - Protocol v1.6 - "Recall by brand", revision r2

r2 (Nov 20, 2026): layout and font fix only. Same numbers, same row order,
same colors and wording as the figure published May 27, 2026
(osf/v24/figures/chart_24_recall_by_brand.pdf, matplotlib 3.10.8).

Defects in the published figure, measured from its PDF:
  1. The indigo header rule cut through the subtitle (rule at 32.4 pt from
     the top, subtitle spans 27.2-36.2 pt). Cause: the rule was drawn at a
     fixed offset instead of below the subtitle's rendered box.
  2. The cell legend sat on the x-axis label (legend starts at 655.0 pt,
     label spans 656.6-665.1 pt). Cause: the legend was anchored at a fixed
     point that ignores the label.
  3. The brand font fell back to DejaVu Sans (pdffonts lists DejaVu only).
     Cause: the figure was not built on the Mac. Its PDF says matplotlib
     3.10.8; all 79 charts committed from the Mac say 3.10.9 and embed
     Akkurat Pro. Akkurat is not installed where it was built, and
     matplotlib substitutes DejaVu without stopping the build.

How r2 fixes them (checked against the matplotlib 3.10.8 docs):
  - Every piece of chrome is placed after measuring the piece before it
    (Figure.draw_without_rendering, then get_window_extent), and the build
    stops if any two chrome boxes overlap or sit closer than MIN_CLEAR_PT.
  - The build stops unless matplotlib resolves Akkurat, regular and bold,
    to an Akkurat file: findfont(fallback_to_default=False). Fonts are
    searched recursively in the report builder's folders, including
    ~/.cache/third_system_reports/fonts on the Third System Mac, and the
    family name is read from the font file itself.

Usage (Third System Mac):
  cd ~/aias && python3 scripts/build_chart_24_recall_by_brand_r2.py
  -> reports/figs/v24/chart_24_recall_by_brand_r2.pdf
  The published chart_24_recall_by_brand.pdf is never overwritten.

Options:
  --scores CSV      canonical scores, columns brand,r_cat,r_cult. The build
                    stops if any value differs from the published figure.
  --out PATH        output PDF (any name except the published one)
  --allow-fallback  preview with Inter when Akkurat is missing. Adds
                    "_PREVIEW-inter" to the file name. Never a deliverable.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import numpy as np

# ---------------------------------------------------------------------------
# Published content (unchanged in r2)
# ---------------------------------------------------------------------------
# Values read from the vector geometry of the May 27 PDF (bar width / tick
# spacing); every one lands on an integer. Row order is the published order.
# Note: the published order puts SAP (total 33) above Oracle (total 34), so
# it is not a strict "total recall, descending" sort. Kept as published.
ROWS = [
    # brand,        cell, r_cat, r_cult
    ("Slack",       "B", 33, 30),
    ("Salesforce",  "A", 36, 25),
    ("HubSpot",     "A", 33, 21),
    ("Workday",     "A", 34,  7),
    ("SAP",         "A", 25,  8),
    ("Oracle",      "A", 26,  8),
    ("Notion",      "B",  2, 27),
    ("ServiceNow",  "A", 17,  8),
    ("Figma",       "B",  1, 23),
    ("Snowflake",   "C", 10, 13),
    ("Zendesk",     "A", 18,  4),
    ("Datadog",     "C",  7,  8),
    ("Linear",      "B",  0, 12),
    ("Stripe",      "C",  4,  6),
    ("Airtable",    "B",  0, 10),
    ("Miro",        "B",  0,  8),
    ("MongoDB",     "C",  1,  4),
    ("Twilio",      "C",  2,  2),
    ("Cloudflare",  "C",  0,  3),
    ("Quip",        "D",  0,  0),
    ("Yammer",      "D",  0,  0),
    ("Wunderlist",  "D",  0,  0),
    ("HipChat",     "D",  0,  0),
    ("Stride",      "D",  0,  0),
]

TITLE    = "Recall by brand"
SUBTITLE = ("R_cat (category) and R_cult (cultural) mentions across "
            "36 outputs per channel")
XLABEL   = "Mentions (out of 36 per channel)"
SOURCE   = "AIAS™ Measurement Program v0.24 · B2B SaaS · Protocol v1.6"
CELL_LABELS = {
    "A": "Cell A: Enterprise Incumbents",
    "B": "Cell B: High-Identity Challengers",
    "C": "Cell C: Infrastructure / Dev Platform",
    "D": "Cell D: Phantom (defunct)",
}

# Colors and sizes as published (read from the PDF)
R_CAT, R_CULT = "#37237B", "#8B7BB5"
CELL_COLORS = {"A": "#37237B", "B": "#D4573B", "C": "#2B9E9E", "D": "#AAAAAA"}
BOLD_CELLS = {"A", "B"}
TITLE_COLOR, SUBTITLE_COLOR, SOURCE_COLOR = "#000000", "#666666", "#999999"
RULE_COLOR, RULE_LW = "#37237B", 1.5
GRID_COLOR = "#B0B0B0"
FS = {"title": 13.0, "subtitle": 9.0, "ytick": 8.5, "xtick": 10.0,
      "xlabel": 8.5, "bar_legend": 8.0, "cell_legend": 7.0, "source": 7.0}
FIGSIZE = (8, 10)
BAR_H = 0.35
SAVEFIG = {"bbox_inches": "tight", "pad_inches": 0.15, "dpi": 300}

# Spacing between chrome pieces, in points (independent of figure height)
GAP = {"top": 6, "title_sub": 4, "sub_rule": 6, "rule_axes": 10,
       "xlabel_legend": 9, "legend_source": 8, "bottom": 4,
       "left": 4, "right": 10}
MIN_CLEAR_PT = 2.0

PUBLISHED_NAME = "chart_24_recall_by_brand.pdf"
DEFAULT_OUT = Path.home() / "aias" / "reports" / "figs" / "v24" / "chart_24_recall_by_brand_r2.pdf"

# ---------------------------------------------------------------------------
# Fonts: same search folders as reports/build_report_v26.py, recursive
# ---------------------------------------------------------------------------
_HOME = Path.home()
FONT_DIRS = [
    _HOME / "Library" / "Fonts",
    Path("/Library/Fonts"),
    _HOME / "Library" / "Application Support" / "Adobe" / "CoreSync" / "plugins" / "livetype" / ".r",
    _HOME / "Library" / "Application Support" / "Adobe" / "CoreSync" / "plugins" / "livetype" / "r",
    _HOME / ".fonts",
    _HOME / ".local" / "share" / "fonts",
    _HOME / ".cache" / "third_system_reports" / "fonts",
]
FALLBACK_FAMILY = "Inter"   # the program's designated fallback (report builder)


def _akkurat_files() -> list[Path]:
    found = set()
    for d in FONT_DIRS:
        if not d.is_dir():
            continue
        for p in d.rglob("*"):
            if p.suffix.lower() in (".otf", ".ttf") and "akkurat" in p.name.lower():
                found.add(p)
    return sorted(found)


def _pick_family(families: set[str]) -> str | None:
    fams = sorted(f for f in families if "akkurat" in f.lower())
    if not fams:
        return None
    for f in fams:
        if f.lower() == "akkurat pro":
            return f
    plain = [f for f in fams if not any(k in f.lower() for k in ("light", "mono", "cond"))]
    return (plain or fams)[0]


def setup_font(allow_fallback: bool) -> tuple[str, bool]:
    """Register Akkurat and prove matplotlib resolves it. Returns (family, is_brand)."""
    files = _akkurat_files()
    families = set()
    for f in files:
        try:
            fm.fontManager.addfont(str(f))
            families.add(fm.FontProperties(fname=f).get_name())
        except Exception as exc:  # unreadable file: report it, keep going
            print(f"[fonts] skipped {f.name}: {type(exc).__name__}: {exc}")
    family = _pick_family(families)
    problem = None
    if family is None:
        problem = f"no Akkurat font files found in: {', '.join(str(d) for d in FONT_DIRS)}"
    else:
        try:
            reg = fm.findfont(fm.FontProperties(family=family), fallback_to_default=False)
            bold = fm.findfont(fm.FontProperties(family=family, weight="bold"),
                               fallback_to_default=False)
            if "akkurat" not in Path(reg).name.lower():
                problem = f"'{family}' resolved to {reg}, not an Akkurat file"
            elif Path(bold) == Path(reg):
                problem = f"no bold weight for '{family}' (bold resolves to {Path(reg).name})"
            else:
                print(f"[fonts] {family}: regular={Path(reg).name}, bold={Path(bold).name}")
        except ValueError as exc:
            problem = f"matplotlib cannot resolve '{family}': {exc}"

    if problem is None:
        plt.rcParams["font.family"] = [family, "DejaVu Sans"]  # DejaVu only for missing glyphs
        plt.rcParams["axes.unicode_minus"] = False
        return family, True

    if not allow_fallback:
        sys.exit(f"[fonts] STOP: {problem}. Not building a chart in a substitute font.")
    print(f"[fonts] PREVIEW ONLY: {problem}. Using {FALLBACK_FAMILY}.")
    fm.findfont(fm.FontProperties(family=FALLBACK_FAMILY), fallback_to_default=False)
    plt.rcParams["font.family"] = [FALLBACK_FAMILY, "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False
    return FALLBACK_FAMILY, False


# ---------------------------------------------------------------------------
# Data check against canonical scores
# ---------------------------------------------------------------------------
def check_scores(path: Path) -> None:
    with open(path, newline="", encoding="utf-8") as fh:
        canon = {r["brand"].strip(): (int(float(r["r_cat"])), int(float(r["r_cult"])))
                 for r in csv.DictReader(fh)}
    diffs = []
    for brand, _cell, rc, ru in ROWS:
        got = canon.get(brand)
        if got != (rc, ru):
            diffs.append(f"{brand}: figure ({rc}, {ru}) vs scores {got}")
    extra = sorted(set(canon) - {r[0] for r in ROWS})
    if diffs or extra:
        sys.exit("[data] STOP: published values do not match the scores file:\n  "
                 + "\n  ".join(diffs + [f"not in figure: {b}" for b in extra]))
    print(f"[data] all {len(ROWS)} brands match {path.name}")


# ---------------------------------------------------------------------------
# Chart
# ---------------------------------------------------------------------------
def build(out: Path) -> None:
    fig = plt.figure(figsize=FIGSIZE)
    W_PT, H_PT = FIGSIZE[0] * 72.0, FIGSIZE[1] * 72.0
    ax = fig.add_axes([0.2, 0.15, 0.75, 0.7])  # provisional; set after measuring

    n = len(ROWS)
    y = np.arange(n)
    ax.barh(y - BAR_H / 2, [r[2] for r in ROWS], height=BAR_H, color=R_CAT,
            label="R_cat (category)", zorder=3)
    ax.barh(y + BAR_H / 2, [r[3] for r in ROWS], height=BAR_H, color=R_CULT,
            label="R_cult (cultural)", zorder=3)
    ax.set_yticks(y, labels=[r[0] for r in ROWS])
    for tick, (_b, cell, _c, _u) in zip(ax.get_yticklabels(), ROWS):
        tick.set_color(CELL_COLORS[cell])
        tick.set_fontsize(FS["ytick"])
        tick.set_fontweight("bold" if cell in BOLD_CELLS else "normal")
    ax.tick_params(axis="y", length=0)
    ax.tick_params(axis="x", labelsize=FS["xtick"])
    ax.invert_yaxis()
    ax.set_xlabel(XLABEL, fontsize=FS["xlabel"])
    ax.grid(axis="x", color=GRID_COLOR, linewidth=0.8, alpha=0.3, zorder=0)
    ax.legend(loc="lower right", fontsize=FS["bar_legend"])

    title = fig.text(0, 0, TITLE, fontsize=FS["title"], fontweight="bold",
                     color=TITLE_COLOR, ha="left", va="top")
    subtitle = fig.text(0, 0, SUBTITLE, fontsize=FS["subtitle"],
                        color=SUBTITLE_COLOR, ha="left", va="top")
    rule = Line2D([0, 1], [0, 0], transform=fig.transFigure, color=RULE_COLOR,
                  linewidth=RULE_LW, solid_capstyle="butt")
    fig.add_artist(rule)
    source = fig.text(0, 0, SOURCE, fontsize=FS["source"], color=SOURCE_COLOR,
                      fontstyle="italic", ha="left", va="bottom")
    handles = [Patch(facecolor=CELL_COLORS[c], edgecolor="none") for c in CELL_LABELS]
    cell_legend = fig.legend(
        handles, list(CELL_LABELS.values()), loc="lower left", ncols=2,
        fontsize=FS["cell_legend"], frameon=False, borderpad=0, borderaxespad=0,
        handlelength=0.9, handleheight=0.9, handletextpad=0.5, columnspacing=1.6,
        labelspacing=0.5, labelcolor=[CELL_COLORS[c] for c in CELL_LABELS],
        bbox_to_anchor=(0, 0), bbox_transform=fig.transFigure)

    # --- measure (sizes in points; text needs one draw pass first) ---------
    fig.draw_without_rendering()
    px = fig.dpi / 72.0                       # display pixels per point
    def h_pt(a): return a.get_window_extent().height / px
    ax_box = ax.get_window_extent()
    tight = ax.get_tightbbox()
    xl_box = ax.xaxis.label.get_window_extent()
    left_need = (ax_box.x0 - tight.x0) / px   # widest brand label + pad
    below_axes = (ax_box.y0 - xl_box.y0) / px  # tick labels + x-label

    # --- place: top-down header, bottom-up footer, axes in between ---------
    left = (GAP["left"] + left_need) / W_PT
    right = 1 - GAP["right"] / W_PT
    t_top = H_PT - GAP["top"]
    s_top = t_top - h_pt(title) - GAP["title_sub"]
    r_y = s_top - h_pt(subtitle) - GAP["sub_rule"] - RULE_LW / 2
    ax_top = r_y - RULE_LW / 2 - GAP["rule_axes"]
    src_y = GAP["bottom"]
    leg_y = src_y + h_pt(source) + GAP["legend_source"]
    ax_bottom = leg_y + h_pt(cell_legend) + GAP["xlabel_legend"] + below_axes

    ax.set_position([left, ax_bottom / H_PT, right - left, (ax_top - ax_bottom) / H_PT])
    title.set_position((left, t_top / H_PT))
    subtitle.set_position((left, s_top / H_PT))
    rule.set_data([left, right], [r_y / H_PT] * 2)
    source.set_position((left, src_y / H_PT))
    cell_legend.set_bbox_to_anchor((left, leg_y / H_PT), transform=fig.transFigure)

    # --- verify: no chrome overlaps, minimum clearance ---------------------
    fig.draw_without_rendering()
    boxes = {
        "title": title.get_window_extent(),
        "subtitle": subtitle.get_window_extent(),
        "rule": rule.get_window_extent(),
        "plot": ax.get_tightbbox(),          # axes, brand labels, ticks, x-label
        "cell legend": cell_legend.get_window_extent(),
        "source": source.get_window_extent(),
    }
    order = list(boxes)                        # top to bottom
    for upper, lower in zip(order, order[1:]):
        gap = (boxes[upper].y0 - boxes[lower].y1) / px
        if gap < MIN_CLEAR_PT:
            sys.exit(f"[layout] STOP: {upper} and {lower} are {gap:.1f} pt apart "
                     f"(minimum {MIN_CLEAR_PT} pt)")
        print(f"[layout] {upper} -> {lower}: {gap:.1f} pt clear")

    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, metadata={
        "Title": "Recall by brand (r2)",
        "Subject": "AIAS v0.24 B2B SaaS. r2: layout and font fix only; "
                   "values unchanged from the May 27, 2026 figure.",
    }, **SAVEFIG)
    plt.close(fig)
    print(f"[out] {out}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--scores", type=Path)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--allow-fallback", action="store_true")
    args = ap.parse_args()

    out = args.out.expanduser()
    if out.name == PUBLISHED_NAME:
        sys.exit(f"[out] STOP: {out.name} is the published figure. "
                 "Replacing it is a separate decision; write r2 to its own file.")
    if args.scores:
        check_scores(args.scores.expanduser())
    family, is_brand = setup_font(args.allow_fallback)
    if not is_brand:
        out = out.with_name(out.stem + "_PREVIEW-inter" + out.suffix)
    build(out)


if __name__ == "__main__":
    main()
