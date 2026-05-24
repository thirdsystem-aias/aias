#!/usr/bin/env python3
"""
build_charts_aias_1_0_report.py — Brand-format chart upgrades for the
AIAS 1.0 Third System brand-format report.

Per outline D3 lock: re-use 3 SSRN paper charts directly (chart_02
anchor-base lineage, chart_04 Type 2 emergence, chart_05 IL Direct forest)
and build ONE brand-format upgrade — the P2 phantom channel signature.
This is the report's most managerially-relevant chart and earns a
brand-format upgrade with clearer quadrant labels, explicit brand-name
callouts for the three channel-pure anchors, and managerial-register
title/axis text.

Brand-format upgrade spec (vs. scripts/build_charts_aias_1_0.py chart_06):
  - Managerial-register title (drops "R_cat_phantom × R_cult_phantom"
    academic notation)
  - Subtitle names the three channel-pure brands explicitly (Estée Lauder,
    Clinique, Glossier)
  - CANONICAL-PURE / CULTURAL-PURE quadrant shading + overlay labels
  - Larger, bolder markers and labels for the three channel-pure anchors;
    deemphasized for mixed-signature brands
  - Brand-format axis labels (drops R_cat_phantom notation; uses
    "Canonical-channel mentions (out of 18)" form)
  - Right-side panel: channel-signature legend with managerial glosses
    (authority pathway / discourse pathway); off-panel passing brands
    sorted by R_phantom descending; explicit validity-anchor verdict

Output:
  reports/figs/aias_1_0_report/chart_p2_phantom_channel_brand_format.pdf

Native figsize: 11 × 8 inches (matches scripts/build_charts_aias_1_0.py
chart_06 for consistency with the other three re-used synthesis charts
under the same height range 11 × 6.5 / 7.5 / 8).

Data source:
  osf/aias_1_0/aias_1_0_synthesis_data.json (locked at
  aias-1-0-data-locked) — same source-of-truth as the synthesis paper's
  chart builder. Re-reads the locked JSON to avoid drift.

Usage:
  python reports/build_charts_aias_1_0_report.py
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

REPO = Path(__file__).resolve().parent.parent
DATA_PATH = REPO / "osf" / "aias_1_0" / "aias_1_0_synthesis_data.json"
OUTPUT_DIR = REPO / "reports" / "figs" / "aias_1_0_report"

# Brand tokens (Third System; primary Indigo).
INDIGO       = "#37237B"
VIOLET       = "#A560E8"   # Cell B / cultural-pure
CYAN         = "#3E8EC9"   # Cell C / mixed
GRAY_TITLE   = "#1A1A1A"
GRAY_SUB     = "#666666"
GRAY_SOURCE  = "#999999"
GRAY_LIGHT   = "#CCCCCC"
PASS_GREEN   = "#2D7D4A"
FAIL_RED     = "#B83A3A"


def register_akkurat() -> bool:
    """Register Akkurat Pro fonts from standard locations.
    Matches scripts/build_charts_aias_1_0.py convention."""
    dirs = [Path.home() / ".fonts" / "Akkurat", Path.home() / "Library" / "Fonts"]
    n = 0
    for d in dirs:
        if not d.exists():
            continue
        for pattern in ("*.otf", "*.ttf"):
            for f in d.glob(pattern):
                if "akkurat" in f.name.lower():
                    try:
                        fm.fontManager.addfont(str(f))
                        n += 1
                    except Exception:
                        pass
    if n > 0:
        plt.rcParams["font.family"] = ["Akkurat Pro", "sans-serif"]
        return True
    plt.rcParams["font.family"] = ["sans-serif"]
    return False


def load_data() -> dict:
    with open(DATA_PATH) as f:
        return json.load(f)


def build_chart_p2_phantom_channel_brand_format(data: dict, output_path: Path) -> None:
    """Brand-format upgrade of chart_06 phantom channel signature.

    Renders the v0.21 cosmetics off-panel channel signature as a
    managerial-register chart for the AIAS 1.0 Third System brand-format
    report (Finding 02 / Proposition P2).
    """
    fig = plt.figure(figsize=(11, 8))

    # ---- Brand-format title + subtitle (managerial register) ----
    fig.text(0.06, 0.965,
             "Off-panel cosmetics brands — channel signature",
             fontsize=16, fontweight="bold", color=GRAY_TITLE,
             ha="left", va="top")
    fig.text(0.06, 0.928,
             "Three of six phantom brands channel-pure. "
             "Estée Lauder and Clinique canonical-pure; "
             "Glossier cultural-pure.",
             fontsize=10.5, color=GRAY_SUB, ha="left", va="top")

    # Thin Indigo separator rule
    fig.add_artist(plt.Line2D([0.06, 0.94], [0.900, 0.900],
                              color=INDIGO, linewidth=0.7,
                              transform=fig.transFigure))

    # Source line at bottom
    source = (
        "Source: v0.21 cosmetics measurement — "
        "osf/aias_1_0/aias_1_0_synthesis_data.json (lock tag "
        "aias-1-0-data-locked). v1.6 Phantom Brand Persistence "
        "specification, SSRN 6816340."
    )
    fig.text(0.06, 0.025, source, fontsize=7.5, style="italic",
             color=GRAY_SOURCE, ha="left", va="bottom", wrap=True)

    # ---- Main scatter axes ----
    ax = fig.add_axes([0.08, 0.14, 0.58, 0.71])

    sigs = data["cross_phase_summary"]["phantom_channel_signatures_v021"]

    # ---- Quadrant shading: CANONICAL-PURE strip + CULTURAL-PURE strip ----
    # CANONICAL-PURE: R_cult = 0 strip (bottom of plot)
    ax.axhspan(-0.5, 0.5, color=INDIGO, alpha=0.08, zorder=0)
    # CULTURAL-PURE: R_cat = 0 strip (left of plot)
    ax.axvspan(-0.5, 0.5, color=VIOLET, alpha=0.08, zorder=0)

    # Quadrant overlay labels (placed inside the shaded strips, on the
    # opposite axis from the markers so they don't overlap brand labels)
    ax.text(11.0, -0.05, "CANONICAL-PURE", fontsize=10, fontweight="bold",
            color=INDIGO, ha="center", va="center", zorder=2,
            bbox=dict(facecolor="white", edgecolor="none", pad=2))
    ax.text(-0.05, 11.0, "CULTURAL-PURE", fontsize=10, fontweight="bold",
            color=VIOLET, ha="center", va="center", rotation=90, zorder=2,
            bbox=dict(facecolor="white", edgecolor="none", pad=2))

    # ---- K = 6 validity-anchor threshold lines ----
    ax.axhline(6, color=PASS_GREEN, linewidth=0.7, linestyle="--",
               alpha=0.55, zorder=1)
    ax.axvline(6, color=PASS_GREEN, linewidth=0.7, linestyle="--",
               alpha=0.55, zorder=1)
    ax.text(0.5, 6.35, "K = 6 persistence threshold", fontsize=8,
            color=PASS_GREEN, style="italic", ha="left", va="bottom")

    # ---- Per-brand markers + labels ----
    def channel_color(rcat, rcult):
        if rcat == 0 and rcult > 0:
            return VIOLET     # pure cultural
        if rcult == 0 and rcat > 0:
            return INDIGO     # pure canonical
        return CYAN           # mixed

    # Label-position offsets keyed to each brand to avoid overlaps
    label_offsets = {
        "Glossier":         (0.7, -0.7),
        "Estée Lauder":(-0.5, 0.85),
        "Clinique":         (-0.5, 0.85),
        "Make Up For Ever": (0.7, -0.55),
        "Too Faced":        (0.7, 0.5),
        "Urban Decay":      (-0.5, -0.8),
    }

    for s in sigs:
        rcat, rcult = s["r_cat_phantom"], s["r_cult_phantom"]
        color = channel_color(rcat, rcult)

        # Channel-pure brands get larger markers + bolder labels
        is_pure = (rcat == 0 and rcult > 0) or (rcult == 0 and rcat > 0)
        marker_size = 240 if is_pure else 140
        label_fontsize = 11 if is_pure else 9
        label_weight = "bold" if is_pure else "normal"
        marker_edge_w = 2.0 if is_pure else 1.5

        ax.scatter([rcat], [rcult], s=marker_size, color=color,
                   edgecolor="white", linewidth=marker_edge_w,
                   alpha=0.95, zorder=3)

        dx, dy = label_offsets.get(s["brand"], (0.7, 0.4))
        ax.text(rcat + dx, rcult + dy, s["brand"],
                fontsize=label_fontsize, fontweight=label_weight,
                color=GRAY_TITLE, va="center",
                ha="left" if dx > 0 else "right", zorder=4)

    # ---- Axes spec ----
    ax.set_xlim(-0.5, 16)
    ax.set_ylim(-0.5, 16)
    ax.set_xlabel("Canonical-channel mentions (out of 18)",
                  fontsize=10.5, color=GRAY_TITLE, labelpad=8)
    ax.set_ylabel("Cultural-channel mentions (out of 18)",
                  fontsize=10.5, color=GRAY_TITLE, labelpad=8)
    ax.tick_params(axis="both", labelsize=9.5)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color(GRAY_LIGHT)
    ax.spines["bottom"].set_color(GRAY_LIGHT)
    ax.set_axisbelow(True)
    ax.grid(True, color=GRAY_LIGHT, alpha=0.25, linewidth=0.4, zorder=0)

    # ---- Right-side managerial panel ----
    panel_x = 0.69

    # Channel-signature legend
    fig.text(panel_x, 0.83, "Channel signature classification",
             fontsize=11, fontweight="bold", color=GRAY_TITLE,
             ha="left", va="top")

    y = 0.792
    legend_items = [
        (INDIGO, "Canonical-pure",
         "R_cult = 0 · authority pathway"),
        (VIOLET, "Cultural-pure",
         "R_cat = 0 · discourse pathway"),
        (CYAN,   "Mixed channel",
         "both channels present"),
    ]
    for color, label, gloss in legend_items:
        fig.add_artist(Rectangle((panel_x, y - 0.010), 0.022, 0.022,
                                 facecolor=color, edgecolor="white",
                                 transform=fig.transFigure))
        fig.text(panel_x + 0.030, y + 0.006, label, fontsize=9.5,
                 fontweight="bold", color=GRAY_TITLE,
                 ha="left", va="center")
        fig.text(panel_x + 0.030, y - 0.012, gloss, fontsize=8,
                 color=GRAY_SUB, ha="left", va="center")
        y -= 0.058

    # Off-panel passing brands list (sorted by R_phantom descending)
    fig.text(panel_x, y - 0.010,
             "Off-panel passing (R_phantom ≥ 6)",
             fontsize=11, fontweight="bold", color=GRAY_TITLE,
             ha="left", va="top")
    y -= 0.040

    sorted_sigs = sorted(sigs, key=lambda s: -s["r_phantom"])
    for s in sorted_sigs:
        line = f"{s['brand']}: {s['r_phantom']}"
        sub = (f"  ({s['r_cat_phantom']} canonical, "
               f"{s['r_cult_phantom']} cultural)")
        fig.text(panel_x, y, line, fontsize=9, color=GRAY_TITLE,
                 ha="left", va="top")
        fig.text(panel_x, y - 0.019, sub, fontsize=7.5, color=GRAY_SUB,
                 ha="left", va="top")
        y -= 0.044

    # Validity anchor note (pulled from locked synthesis data)
    inc3 = next(p for p in data["phases"] if p["phase"] == "v0.21"
                )["v1_6_retrospective"]["inc3"]
    vc = inc3["validity_check"]
    fig.text(panel_x, y - 0.022,
             f"Validity anchor: {vc['anchor']}",
             fontsize=9.5, fontweight="bold", color=GRAY_TITLE,
             ha="left", va="top")
    fig.text(panel_x, y - 0.040,
             f"R_phantom = {vc['anchor_observed']} "
             f"(≥ {vc['anchor_min_required']} required) "
             + ("✓ passes" if vc["passes"] else "✗ fails"),
             fontsize=8.5,
             color=PASS_GREEN if vc["passes"] else FAIL_RED,
             ha="left", va="top")

    fig.savefig(output_path, format="pdf", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    registered = register_akkurat()
    print(f"[build_charts_aias_1_0_report] Akkurat Pro registered: {registered}")

    data = load_data()

    output_path = OUTPUT_DIR / "chart_p2_phantom_channel_brand_format.pdf"
    build_chart_p2_phantom_channel_brand_format(data, output_path)
    print(f"[build_charts_aias_1_0_report] wrote: {output_path}")


if __name__ == "__main__":
    main()
