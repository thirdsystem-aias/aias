"""v0.17 chart generation for the brand-format report and SSRN paper.

Produces three PDF charts visualising the v0.17 Premium Kitchenware program
outcomes: FALSIFIED-on-panel-inadequacy substantive verdict and the
Recognition-Recall dissociation methodological finding.

Carries v0.16 chart conventions forward (Third System brand spec 1.5):
  - Akkurat Pro + STIX mathtext, pdf.fonttype=42
  - Cell-coloring for brand-level points (european / american / japanese)
    drawn from palette.data_viz.schemes.qualitative_standard
  - 7.5" wide hero figsizes (6-column page grid)
  - Title 13pt bold + subtitle 9.5pt muted + source 7.5pt italic muted
  - 300 DPI vector PDF output
  - INDIGO reserved for chrome (title, headlines, post-state emphasis);
    series colors drawn from qualitative palette

Charts produced:
  chart_v17_phase_b_mention_rates.pdf      (15-brand cross-cell distribution)
  chart_v17_dissociation.pdf               (HEADLINE — Recognition x Recall)
  chart_v17_cell_collapse.pdf              (Pre-vs-post per cell + C1 breach)

Run:
    python3 ~/aias/scripts/build_charts_v17.py
"""
import sys
import textwrap
from pathlib import Path

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from matplotlib.patches import Patch

ROOT = Path.home() / "aias"
sys.path.insert(0, str(ROOT / "reports"))

from v17_kitchenware_content import (  # noqa: E402
    load_phase_a_scores,
    load_phase_b_mention_rates,
    CELL_COUNTS,
    C1_FLOOR,
    TOTAL_PRE,
    TOTAL_POST,
)

# ============================================================================
# Brand constants (per third_system_brand.json v1.5 python_constant_mapping)
# ============================================================================

# Indigo family (chrome — title, headlines, post-state emphasis)
INDIGO         = "#37237B"
AMETHYST       = "#534F9E"
PETRO          = "#6A6AB1"
IRIS           = "#908EC5"
LAVENDER_GREY  = "#BBB9DD"

# Qualitative palette (qualitative_standard, position-stable across reports)
NAVY           = "#002B5F"   # qualitative_standard position 2
HONEY          = "#FFAC17"   # position 3
MAROON         = "#6A035C"   # position 6

# Editorial chrome
TEXT           = "#231F20"
MUTED          = "#6B6967"
GRID           = "#CCCCCC"
GRID_SUBTLE    = "#E5E5E5"

# Cell color assignment (cookware tradition cells in pre-reg sec. 2 order)
CELL_COLOR = {
    "european": NAVY,
    "american": HONEY,
    "japanese": MAROON,
}

CELL_LABEL = {
    "european": "European",
    "american": "American",
    "japanese": "Japanese",
}


# ============================================================================
# Font setup (Third System brand spec)
# ============================================================================

def setup_font():
    """Register Akkurat / Akkurat Pro / Inter from user font dirs and resolve
    the canonical font NAME (not file path) that matplotlib's font manager
    knows about. Returns the resolved font name or 'DejaVu Sans' fallback."""
    for path in [Path.home() / ".fonts", Path.home() / "Library" / "Fonts"]:
        if path.exists():
            patterns = (
                list(path.glob("Akkurat*.[ot]tf"))
                + list(path.glob("Akkurat*/*.[ot]tf"))
                + list(path.glob("Inter*.[ot]tf"))
            )
            for fp in patterns:
                try:
                    fm.fontManager.addfont(str(fp))
                except Exception:
                    pass
    available = {f.name for f in fm.fontManager.ttflist}
    for c in ("Akkurat Pro", "Akkurat Pro Regular", "Akkurat", "Inter"):
        if c in available:
            return c
    return "DejaVu Sans"


FONT = setup_font()
print(f"# Font in use: {FONT}")

rcParams["font.family"]       = [FONT, "sans-serif"]
rcParams["mathtext.fontset"]  = "stix"
rcParams["axes.linewidth"]    = 0.6
rcParams["axes.edgecolor"]    = MUTED
rcParams["axes.labelcolor"]   = TEXT
rcParams["xtick.color"]       = MUTED
rcParams["ytick.color"]       = MUTED
rcParams["xtick.labelsize"]   = 8.5
rcParams["ytick.labelsize"]   = 8.5
rcParams["axes.labelsize"]    = 9
rcParams["axes.titlesize"]    = 10
rcParams["axes.spines.top"]   = False
rcParams["axes.spines.right"] = False
rcParams["pdf.fonttype"]      = 42


# ============================================================================
# Paths and source line
# ============================================================================

V17_ROOT = ROOT / "osf" / "v17"
OUT_DIR  = ROOT / "papers" / "v0_17" / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

SOURCE_LINE = ("Source: Third System AI Availability Score (AIAS) v0.17 \u00b7 "
               "Phase B LLM-substrate measurement (May 2026)\n"
               "Pre-reg locked at v0.17-prereg-r1 (commit 3ebe426); "
               "Phase B locked at v0.17-phase-b-locked (commit 54c83ec).")


# ============================================================================
# Shared chart chrome (matches v16 draw_title_and_subtitle + add_source)
# ============================================================================

def draw_title_and_subtitle(fig, title, subtitle, x=0.06, title_y=0.96,
                            subtitle_y=0.91, wrap_width=130):
    fig.text(x, title_y, title, ha="left", va="top",
             fontsize=13, color=TEXT, weight="bold")
    wrapped_subtitle = textwrap.fill(subtitle, width=wrap_width,
                                     break_long_words=False,
                                     break_on_hyphens=False)
    fig.text(x, subtitle_y, wrapped_subtitle, ha="left", va="top",
             fontsize=9.5, color=MUTED)


def add_source(fig, x=0.06, y=0.025):
    fig.text(x, y, SOURCE_LINE, ha="left", va="top",
             fontsize=7.5, color=MUTED, style="italic")


# ============================================================================
# CHART 1: Phase B mention rates across 15-brand panel
# ============================================================================

def chart_phase_b_mention_rates():
    """Horizontal bar chart of Phase B mention rates for the 15-brand
    operational panel. Sorted descending. Colored by tradition cell. PASS
    threshold (1/6) shown as a vertical reference."""
    data = load_phase_b_mention_rates()
    brands = [d[0] for d in data]
    rates  = [d[2] for d in data]
    tiers  = [d[3] for d in data]
    colors = [CELL_COLOR[d[1]] for d in data]

    fig, ax = plt.subplots(figsize=(7.5, 9.0))
    y_pos = np.arange(len(brands))
    ax.barh(y_pos, rates, color=colors, edgecolor="white",
            linewidth=0.8, zorder=3)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(brands, color=TEXT)
    ax.invert_yaxis()
    ax.set_xlabel("Phase B mention rate (mentions / 18 cells)", color=TEXT)
    ax.set_xlim(0, 1.05)
    ax.grid(True, axis="x", color=GRID_SUBTLE, linewidth=0.4, zorder=0)

    # PASS threshold (1/6)
    ax.axvline(1/6, color=MUTED, linestyle="--", linewidth=0.7, alpha=0.8)
    ax.text(1/6 + 0.012, len(brands) - 0.5, "PASS threshold (1/6)",
            fontsize=7.5, color=MUTED, va="bottom", style="italic")

    # Tier annotations
    for i, (brand, cell, rate, tier) in enumerate(data):
        if tier == "PASS_E5":
            ax.text(rate + 0.015, i, "PASS_E5",
                    fontsize=7.5, color=TEXT, va="center", style="italic")
        elif tier == "EXCLUDED_E1a":
            ax.text(0.012, i, "EXCLUDED",
                    fontsize=7.5, color="white", va="center",
                    bbox=dict(facecolor=TEXT, edgecolor="none", pad=1.5))

    # Cell legend (matches v16 pattern: bottom, no frame, equal columns)
    legend_handles = [
        Patch(facecolor=CELL_COLOR[c], label=CELL_LABEL[c] + " cell")
        for c in ("european", "american", "japanese")
    ]
    ax.legend(handles=legend_handles, loc="lower right",
              ncol=3, frameon=False, fontsize=8.5,
              handletextpad=0.4, columnspacing=2.0)

    # Title chrome
    title = "Premium kitchenware — Phase B mention rates across the 15-brand panel"
    subtitle = ("Cross-cell mention rate distribution under v0.17 LLM-substrate "
                "Phase B (three category queries x six reference LLMs = 18 cells "
                "per brand). European cell saturates the high-mention end; "
                "American cell occupies mid-range with two long-tail exclusions; "
                "Japanese cell concentrated entirely at zero — the full-cell "
                "collapse motivating the AMBIGUOUS Identity-Load verdict.")
    draw_title_and_subtitle(fig, title, subtitle, x=0.06,
                            title_y=0.965, subtitle_y=0.920, wrap_width=100)
    add_source(fig, x=0.06, y=0.035)

    fig.subplots_adjust(top=0.82, bottom=0.08, left=0.16, right=0.97)
    out = OUT_DIR / "chart_v17_phase_b_mention_rates.pdf"
    fig.savefig(out, dpi=300)
    plt.close(fig)
    print(f"  Wrote: {out.relative_to(ROOT)}")
    return out


# ============================================================================
# CHART 2: Recognition x Recall dissociation (HEADLINE)
# ============================================================================

def chart_dissociation():
    """Scatter of Phase A C_P anchoring score vs Phase B mention rate for the
    four pivots that received Phase A measurement. Iwachu highlighted as the
    canonical dissociation case. Le Creuset and All-Clad sit at the same
    underlying coordinate (6, 1.0); we jitter them slightly along x so both
    are visible and individually labelable."""
    scores = load_phase_a_scores()
    rates  = {b: r for (b, c, r, t) in load_phase_b_mention_rates()}

    # Visual positions (jittered for the (6, 1.0) overlap)
    PLACEMENT = {
        "Le Creuset": (5.82, 1.00, "european"),
        "All-Clad":   (6.18, 1.00, "american"),
        "Iwachu":     (6.00, 0.00, "japanese"),
        "Vermicular": (4.00, -0.06, "japanese"),  # Phase B descope marker
    }

    fig, ax = plt.subplots(figsize=(7.5, 7.5))

    # ---- Plot data points + their per-point labels --------------------------
    for brand, (x, y, cell) in PLACEMENT.items():
        color = CELL_COLOR[cell]

        if brand == "Vermicular":
            # Descoped marker — not a point on the Phase B axis
            ax.scatter([x], [y], marker="x", s=140,
                       color=MUTED, linewidths=2.0, zorder=4)
            ax.annotate(f"{brand}\n(C$_P$ FAIL — descoped)",
                        xy=(x, y), xytext=(x + 0.25, 0.10),
                        fontsize=8.5, color=MUTED, ha="left",
                        arrowprops=dict(arrowstyle="-", color=GRID,
                                        lw=0.5, shrinkA=0, shrinkB=4))
            continue

        ax.scatter([x], [y], s=180, color=color, edgecolor="white",
                   linewidth=1.2, zorder=4)

        if brand == "Le Creuset":
            # Above-left of the point
            ax.annotate(brand, xy=(x, y), xytext=(-8, 14),
                        textcoords="offset points",
                        fontsize=10, color=color, fontweight="bold",
                        ha="right", va="bottom")
        elif brand == "All-Clad":
            # Above-right of the point
            ax.annotate(brand, xy=(x, y), xytext=(8, 14),
                        textcoords="offset points",
                        fontsize=10, color=color, fontweight="bold",
                        ha="left", va="bottom")
        elif brand == "Iwachu":
            # Direct label below-right of the point
            ax.annotate(brand, xy=(x, y), xytext=(10, -3),
                        textcoords="offset points",
                        fontsize=11, color=color, fontweight="bold",
                        ha="left", va="top")

    # ---- Dissociation callout (upper-middle empty area) ---------------------
    # Positioned to be clear of all four data points and both threshold lines.
    ax.annotate("Recognition $\\times$ Recall dissociation:\n"
                "full recognition (6/6), zero recall (0/18)",
                xy=(6.0, 0.04), xytext=(2.7, 0.55),
                fontsize=9, color=MAROON, ha="left", va="center",
                style="italic",
                arrowprops=dict(arrowstyle="->", color=MAROON,
                                lw=1.0, shrinkA=2, shrinkB=8,
                                connectionstyle="arc3,rad=-0.15"))

    # ---- Threshold reference lines ------------------------------------------
    # Phase A supermajority (5/6): vertical dashed line. Label placed at
    # mid-axis-height where there are no data points.
    ax.axvline(5, color=MUTED, linestyle="--", linewidth=0.7, alpha=0.8)
    ax.text(4.92, 0.50, "Phase A supermajority (5/6)",
            fontsize=7.5, color=MUTED, va="center", ha="right",
            rotation=90, style="italic")
    # Phase B PASS (1/6): horizontal dashed line. Label placed in upper-left.
    ax.axhline(1/6, color=MUTED, linestyle="--", linewidth=0.7, alpha=0.8)
    ax.text(0.2, 1/6 + 0.018, "Phase B PASS threshold (1/6)",
            fontsize=7.5, color=MUTED, ha="left", style="italic")

    # ---- Axes ---------------------------------------------------------------
    ax.set_xlabel("Phase A C$_P$ anchoring score (out of 6 reference LLMs)",
                  color=TEXT)
    ax.set_ylabel("Phase B mention rate (mentions / 18 cells)", color=TEXT)
    ax.set_xlim(-0.5, 6.8)
    ax.set_ylim(-0.18, 1.18)
    ax.set_xticks(range(7))
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.grid(True, color=GRID_SUBTLE, linewidth=0.4, zorder=0)

    # ---- Quadrant labels (outside data area, in the axis-extension margins) -
    ax.text(-0.3, 1.13, "Low recognition + high recall (empty quadrant)",
            fontsize=7.5, color=MUTED, ha="left", style="italic", alpha=0.7)
    ax.text(6.7, 1.13, "Full Presence",
            fontsize=7.5, color=MUTED, ha="right", style="italic", alpha=0.7)
    ax.text(6.7, -0.15, "Recognition-only (dissociation)",
            fontsize=7.5, color=MUTED, ha="right", style="italic", alpha=0.7)

    # ---- Cell legend --------------------------------------------------------
    legend_handles = [
        Patch(facecolor=CELL_COLOR[c], label=CELL_LABEL[c] + " cell pivot")
        for c in ("european", "american", "japanese")
    ]
    ax.legend(handles=legend_handles, loc="lower left",
              bbox_to_anchor=(0.01, 0.08),
              frameon=False, fontsize=8.5)

    # ---- Title chrome -------------------------------------------------------
    title = "Recognition $\\times$ Recall dissociation — the Iwachu canonical case"
    subtitle = ("The four pivot brands that received Phase A C$_P$ measurement, "
                "plotted against Phase B mention rate. Le Creuset and All-Clad "
                "occupy the full-Presence quadrant; Vermicular failed Phase A "
                "(C$_P$ at 4/6) and was descoped before Phase B; Iwachu sits "
                "alone in the recognition-only quadrant. The dissociation "
                "motivates the v1.4 Methodology revision specifying AI "
                "Availability as a multi-component construct.")
    draw_title_and_subtitle(fig, title, subtitle, x=0.06,
                            title_y=0.965, subtitle_y=0.930, wrap_width=100)
    add_source(fig, x=0.06, y=0.045)

    fig.subplots_adjust(top=0.81, bottom=0.10, left=0.10, right=0.97)
    out = OUT_DIR / "chart_v17_dissociation.pdf"
    fig.savefig(out, dpi=300)
    plt.close(fig)
    print(f"  Wrote: {out.relative_to(ROOT)}")
    return out


# ============================================================================
# CHART 3: Per-cell collapse — pre vs post Phase B
# ============================================================================

def chart_cell_collapse():
    """Paired bar chart of pre-Phase-A vs post-Phase-B brand counts per
    tradition cell, with worldwide-n + C1 breach subtitle. Pre bars are
    neutral grey; post bars are INDIGO (operational-outcome emphasis)."""
    cells = ["european", "american", "japanese"]
    pre   = [CELL_COUNTS[c]["pre"]  for c in cells]
    post  = [CELL_COUNTS[c]["post"] for c in cells]

    x = np.arange(len(cells))
    width = 0.36

    fig, ax = plt.subplots(figsize=(7.5, 5.4))
    bars_pre  = ax.bar(x - width/2, pre, width,
                       label="Pre-Phase A (registered)",
                       color=GRID, edgecolor="white", linewidth=0.8, zorder=3)
    bars_post = ax.bar(x + width/2, post, width,
                       label="Post-Phase B (operational)",
                       color=INDIGO, edgecolor="white", linewidth=0.8, zorder=3)

    # Value labels above bars
    for bars in (bars_pre, bars_post):
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, h + 0.12,
                    str(int(h)), ha="center", fontsize=9, color=TEXT)

    ax.set_xticks(x)
    ax.set_xticklabels([CELL_LABEL[c] for c in cells], color=TEXT)
    ax.set_ylabel("Brand count", color=TEXT)
    ax.set_ylim(0, 7.5)
    ax.grid(True, axis="y", color=GRID_SUBTLE, linewidth=0.4, zorder=0)

    ax.legend(loc="upper right", frameon=False, fontsize=8.5)

    # Worldwide-n + C1 breach annotation (top-left of plot area)
    deficit = C1_FLOOR - TOTAL_POST
    breach_text = (f"Worldwide n: {TOTAL_PRE} \u2192 {TOTAL_POST}    "
                   f"C1 floor: {C1_FLOOR}    "
                   f"Breach deficit: {deficit}")
    ax.text(0.03, 0.95, breach_text,
            transform=ax.transAxes, fontsize=8.5, color=TEXT,
            ha="left", va="top", weight="bold",
            bbox=dict(facecolor="white", edgecolor=GRID,
                      boxstyle="round,pad=0.5", linewidth=0.5))

    # Title chrome
    title = "Panel attrition by tradition cell — pre-Phase-A versus post-Phase-B"
    subtitle = ("Worldwide n dropped from 16 to 10 across two attrition stages, "
                "breaching the C1 adequacy floor of 12 by a deficit of 2. The "
                "European cell remained intact; the American cell lost two "
                "long-tail brands; the Japanese cell collapsed entirely "
                "(Vermicular at Phase A; Iwachu, Sori Yanagi, Noda Horo at "
                "Phase B). This pattern produces the FALSIFIED-on-panel-"
                "inadequacy verdict for H$_\\mathrm{Regime4\\_kitchenware}$.")
    draw_title_and_subtitle(fig, title, subtitle, x=0.06,
                            title_y=0.965, subtitle_y=0.930, wrap_width=100)
    add_source(fig, x=0.06, y=0.080)

    fig.subplots_adjust(top=0.74, bottom=0.13, left=0.09, right=0.97)
    out = OUT_DIR / "chart_v17_cell_collapse.pdf"
    fig.savefig(out, dpi=300)
    plt.close(fig)
    print(f"  Wrote: {out.relative_to(ROOT)}")
    return out


# ============================================================================
# Main
# ============================================================================

def main():
    print("v0.17 chart build")
    print("=" * 60)
    print(f"  Font:        {FONT}")
    print(f"  Output dir:  {OUT_DIR.relative_to(ROOT)}")
    print(f"  Brand spec:  Third System v1.5 (Indigo {INDIGO})")
    print()

    chart_phase_b_mention_rates()
    chart_dissociation()
    chart_cell_collapse()

    print()
    print("=" * 60)
    print(f"Done. 3 figures in {OUT_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
