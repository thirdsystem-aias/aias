#!/usr/bin/env python3
"""
build_charts_v21.py — Third System brand-format charts for AIAS v0.21 (v2).

v2 layout discipline:
  - Single-chart layouts (no subplot grids that cramp annotations)
  - Side panels for case lists instead of overlaid labels on scatters
  - Quadrant labels in corner zones empty of data
  - Generous figure dimensions and bottom margins for summary text

Produces three PDFs at ~/aias/reports/figs/v21/:
  - chart_01_cp_distribution.pdf       All 24 brands stacked vertically by cell
  - chart_02_dissociation_scatter.pdf  C_P × R_cat with right-side Iwachu list
  - chart_03_channel_asymmetry.pdf     R_cat × R_cult with Type 2 foregrounded

Editorial convention:
  - Title bold top-left
  - Gray subtitle below title
  - Thin indigo separator rule (#37237B)
  - Italic gray source line at bottom citing upstream SSRN IDs
  - Akkurat Pro font (auto-detected from ~/.fonts/Akkurat and ~/Library/Fonts)

Usage:
    python build_charts_v21.py
    python build_charts_v21.py --verdicts <path>
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import Rectangle

# --- Paths -------------------------------------------------------------------

DEFAULT_VERDICTS = Path.home() / "aias" / "osf" / "v21" / "v21_verdicts.json"
DEFAULT_OUTPUT_DIR = Path.home() / "aias" / "reports" / "figs" / "v21"

# --- Brand colors and style --------------------------------------------------

INDIGO = "#37237B"
GRAY_TITLE = "#1A1A1A"
GRAY_SUB = "#666666"
GRAY_SOURCE = "#999999"
GRAY_LIGHT = "#CCCCCC"
PASS_GREEN = "#2D7D4A"
FAIL_RED = "#B83A3A"

CELL_COLORS = {
    "A": "#37237B",
    "B": "#A560E8",
    "C": "#3E8EC9",
}
CELL_LABELS_SHORT = {
    "A": "Prestige",
    "B": "Celebrity DTC",
    "C": "Drugstore",
}

# --- Font registration -------------------------------------------------------

def register_akkurat() -> bool:
    dirs = [Path.home() / ".fonts" / "Akkurat", Path.home() / "Library" / "Fonts"]
    count = 0
    for d in dirs:
        if not d.exists():
            continue
        for ext in ("*.otf", "*.ttf"):
            for fontfile in d.glob(ext):
                if "akkurat" in fontfile.name.lower():
                    try:
                        fm.fontManager.addfont(str(fontfile))
                        count += 1
                    except Exception:
                        pass
    if count > 0:
        plt.rcParams["font.family"] = ["Akkurat Pro", "sans-serif"]
        return True
    plt.rcParams["font.family"] = ["sans-serif"]
    return False


# --- Editorial layout --------------------------------------------------------

def apply_editorial_layout(fig, title: str, subtitle: str, source: str,
                           title_y: float = 0.965,
                           subtitle_y: float = 0.935,
                           rule_y: float = 0.910,
                           source_y: float = 0.025) -> None:
    """Standardized editorial header + footer. All other content must sit
    within rule_y and source_y. Single-line subtitle assumed."""
    fig.text(0.06, title_y, title, fontsize=14, fontweight="bold",
             color=GRAY_TITLE, ha="left", va="top")
    fig.text(0.06, subtitle_y, subtitle, fontsize=9.5,
             color=GRAY_SUB, ha="left", va="top")
    fig.add_artist(plt.Line2D([0.06, 0.94], [rule_y, rule_y],
                              color=INDIGO, linewidth=0.6,
                              transform=fig.transFigure))
    fig.text(0.06, source_y, source, fontsize=7.5, style="italic",
             color=GRAY_SOURCE, ha="left", va="bottom")


def load_verdicts(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


# --- Chart 1: C_P distribution (single chart, all 24 brands) ----------------

def build_chart_01(verdicts: dict, output_path: Path) -> None:
    cells = verdicts["phase_a"]["per_cell"]
    c2 = verdicts["v1_5_c2_per_cell"]

    fig = plt.figure(figsize=(11, 9.5))
    apply_editorial_layout(
        fig,
        title="Phase A Recognition (C_P) per brand, grouped by IL-tier cell",
        subtitle="v1.5 C2 acceptance: distinct C_P values ≥ 3  ∧  modal share ≤ 0.625 (per cell)",
        source=("Source: AIAS™ Presence Measurement Protocol v0.21 acquisition (May 2026). "
                "v1.5 methodology per SSRN 6810758. Pre-registration v0.21-prereg-r1."),
    )

    # Single tall axis for all brands, side panel for stats
    # Bottom = 0.12 (not 0.07) so x-axis label clears the source line at 0.025
    ax = fig.add_axes([0.27, 0.12, 0.55, 0.76])

    # Build flat list of (brand, cell, cp, cascade_order) in cell order A, B, C
    flat = []
    for cell_id in ["A", "B", "C"]:
        for b in sorted(cells[cell_id]["brands"], key=lambda x: x["cascade_order"]):
            flat.append({
                "name": b["name"],
                "cell": cell_id,
                "cp": b["cp"],
                "cascade_order": b["cascade_order"],
            })

    y_positions = list(range(len(flat)))
    bar_colors = [CELL_COLORS[b["cell"]] for b in flat]
    cps = [b["cp"] for b in flat]
    labels = [f"{b['cell']}.{b['cascade_order']}  {b['name']}" for b in flat]

    ax.barh(y_positions, cps, color=bar_colors, alpha=0.85,
            edgecolor="white", height=0.7, zorder=3)

    # Numeric value annotation at end of each bar
    for y, cp in zip(y_positions, cps):
        ax.text(cp + 0.12, y, str(cp), fontsize=8, color=GRAY_TITLE,
                va="center", ha="left", zorder=4)

    # Cell group dividers (horizontal lines between cells)
    cell_a_n = len(cells["A"]["brands"])
    cell_b_n = len(cells["B"]["brands"])
    for divider_y in [cell_a_n - 0.5, cell_a_n + cell_b_n - 0.5]:
        ax.axhline(divider_y, color=GRAY_LIGHT, linewidth=0.8, zorder=2)

    ax.set_yticks(y_positions)
    ax.set_yticklabels(labels, fontsize=8.5)
    ax.invert_yaxis()
    ax.set_xlim(0, 7)
    ax.set_xticks(range(0, 7))
    ax.tick_params(axis="x", labelsize=9)
    ax.set_xlabel("C_P  (Recognition score: yes-count across 6 panel models, 0–6)",
                  fontsize=9.5, color=GRAY_TITLE, labelpad=8)

    # Reference lines: Iwachu threshold (C_P=5) and saturation (C_P=6)
    ax.axvline(5, color=INDIGO, linewidth=0.5, linestyle=":", alpha=0.5, zorder=1)
    ax.axvline(6, color=GRAY_LIGHT, linewidth=0.5, linestyle="--", alpha=0.7, zorder=1)

    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color(GRAY_LIGHT)
    ax.spines["bottom"].set_color(GRAY_LIGHT)
    ax.set_axisbelow(True)
    ax.grid(axis="x", color=GRAY_LIGHT, alpha=0.3, linewidth=0.4, zorder=0)

    # Side panel — per-cell stats stacked vertically on the right
    side_x = 0.84
    panel_y_top = 0.86
    panel_y_bot = 0.16
    cell_panel_height = (panel_y_top - panel_y_bot) / 3.0

    for i, cell_id in enumerate(["A", "B", "C"]):
        cell = cells[cell_id]
        c2_status = c2[cell_id]
        y_top = panel_y_top - i * cell_panel_height
        y_text_start = y_top - 0.02

        fig.text(side_x, y_text_start,
                 f"Cell {cell_id} · {CELL_LABELS_SHORT[cell_id]}",
                 fontsize=10, fontweight="bold", color=CELL_COLORS[cell_id],
                 ha="left", va="top")
        fig.text(side_x, y_text_start - 0.030,
                 f"mean C_P  = {cell['mean_cp']:.2f}",
                 fontsize=8.5, color=GRAY_TITLE, ha="left", va="top")
        fig.text(side_x, y_text_start - 0.055,
                 f"distinct  = {cell['distinct_cp_count']}",
                 fontsize=8.5, color=GRAY_TITLE, ha="left", va="top")
        fig.text(side_x, y_text_start - 0.080,
                 f"modal     = {cell['modal_cp_share']:.3f}",
                 fontsize=8.5, color=GRAY_TITLE, ha="left", va="top")

        status_color = PASS_GREEN if c2_status["passes"] else FAIL_RED
        status_text = "v1.5 C2: PASS" if c2_status["passes"] else "v1.5 C2: FAIL"
        fig.text(side_x, y_text_start - 0.115, status_text,
                 fontsize=9, fontweight="bold", color=status_color,
                 ha="left", va="top")

        pivot = cell.get("pivot_brand") or "cascade exhausted"
        fig.text(side_x, y_text_start - 0.143,
                 f"pivot: {pivot}",
                 fontsize=7.5, color=GRAY_SUB, style="italic",
                 ha="left", va="top")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, format="pdf", dpi=300)
    plt.close(fig)
    print(f"  ✓ {output_path.name}")


# --- Chart 2: Dissociation scatter (C_P × R_cat) ----------------------------

def build_chart_02(verdicts: dict, output_path: Path) -> None:
    cp_data = verdicts["phase_a"]["per_brand"]
    recall_data = verdicts["phase_b"]["per_brand"]
    dissoc = verdicts["dissociation"]

    fig = plt.figure(figsize=(12, 8))
    apply_editorial_layout(
        fig,
        title="Recognition × Recall — Iwachu dissociation on the v0.21 cosmetics panel",
        subtitle="Iwachu pattern: C_P ≥ 5  ∧  R_cat ≤ 2  (high Recognition, sparse canonical Recall)",
        source=("Source: AIAS™ Presence Measurement Protocol v0.21 (May 2026). "
                "Upstream phases: v0.17 SSRN 6802261, v0.18 SSRN 6806558, v0.19 SSRN 6809182, v0.20 SSRN 6811441, v1.5 SSRN 6810758."),
    )

    # Scatter on left, Iwachu case list on right
    ax = fig.add_axes([0.08, 0.13, 0.55, 0.72])

    # Iwachu quadrant shading
    iwachu_rect = Rectangle((5, -0.4), 1.6, 2.7, facecolor=INDIGO, alpha=0.08,
                            edgecolor=INDIGO, linewidth=0.6, linestyle="--", zorder=1)
    ax.add_patch(iwachu_rect)
    # Quadrant label in lower-left of the chart (below where Cell A points concentrate)
    ax.text(0.1, 6.5, "IWACHU QUADRANT  (C_P ≥ 5  ∧  R_cat ≤ 2)",
            fontsize=8.5, color=INDIGO, style="italic", fontweight="bold",
            ha="left", va="top")

    # Per-cell scatter with slight jitter to reduce overlap of identical points
    import random
    random.seed(42)
    for cell_id in ["A", "B", "C"]:
        cell_brands = [b for b, info in cp_data.items() if info["cell"] == cell_id]
        xs, ys = [], []
        for brand_name in cell_brands:
            x = cp_data[brand_name]["cp"] + random.uniform(-0.08, 0.08)
            y = recall_data[brand_name]["r_cat"] + random.uniform(-0.15, 0.15)
            xs.append(x)
            ys.append(y)
        ax.scatter(xs, ys, s=85, color=CELL_COLORS[cell_id], alpha=0.80,
                   edgecolors="white", linewidth=1.0, zorder=3,
                   label=f"Cell {cell_id} — {CELL_LABELS_SHORT[cell_id]}")

    ax.set_xlim(-0.4, 6.8)
    ax.set_ylim(-1, 19)
    ax.set_xticks(range(0, 7))
    ax.set_yticks(range(0, 19, 3))
    ax.set_xlabel("Recognition — Phase A C_P (0–6)",
                  fontsize=10, color=GRAY_TITLE, labelpad=8)
    ax.set_ylabel("Recall (canonical) — Phase B R_cat (0–18)",
                  fontsize=10, color=GRAY_TITLE, labelpad=8)

    # Threshold lines
    ax.axvline(5, color=INDIGO, linewidth=0.4, linestyle=":", alpha=0.5, zorder=2)
    ax.axhline(2, color=INDIGO, linewidth=0.4, linestyle=":", alpha=0.5, zorder=2)

    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color(GRAY_LIGHT)
    ax.spines["bottom"].set_color(GRAY_LIGHT)
    ax.tick_params(labelsize=9)
    ax.set_axisbelow(True)
    ax.grid(True, color=GRAY_LIGHT, alpha=0.25, linewidth=0.4, zorder=0)

    ax.legend(loc="upper left", bbox_to_anchor=(0.02, 0.85),
              frameon=False, fontsize=9,
              labelcolor=GRAY_TITLE, handletextpad=0.5)

    # Side panel — list of all Iwachu cases by cell
    panel_x = 0.67
    panel_y_top = 0.83

    fig.text(panel_x, panel_y_top, "Iwachu cases (v0.21)",
             fontsize=11, fontweight="bold", color=INDIGO,
             ha="left", va="top")
    fig.text(panel_x, panel_y_top - 0.030,
             f"{dissoc['iwachu_count']} total · {len(dissoc['iwachu_cells'])} of 3 cells",
             fontsize=8.5, color=GRAY_SUB, ha="left", va="top")

    y_offset = panel_y_top - 0.068
    line_h = 0.024
    for cell_id in ["A", "B", "C"]:
        cell_iwachu = [c for c in dissoc["iwachu"] if c["cell"] == cell_id]
        if not cell_iwachu:
            continue
        fig.text(panel_x, y_offset,
                 f"Cell {cell_id} — {CELL_LABELS_SHORT[cell_id]}",
                 fontsize=9, fontweight="bold", color=CELL_COLORS[cell_id],
                 ha="left", va="top")
        y_offset -= 0.022
        for case in cell_iwachu:
            label = f"  {case['brand']}  (C_P={case['cp']}, R_cat={case['r_cat']})"
            fig.text(panel_x, y_offset, label,
                     fontsize=7.5, color=GRAY_TITLE, ha="left", va="top")
            y_offset -= line_h * 0.85
        y_offset -= 0.012  # group spacing

    # Bottom-of-chart summary headline
    fig.text(0.08, 0.067,
             f"H_Dissociation_substrate_generalization → GENERALIZED  "
             f"(Iwachu cases in all 3 cells; cumulative anchor base now spans 5 substrate families).",
             fontsize=9, color=INDIGO, fontweight="bold",
             ha="left", va="top")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, format="pdf", dpi=300)
    plt.close(fig)
    print(f"  ✓ {output_path.name}")


# --- Chart 3: Channel asymmetry (R_cat × R_cult) ----------------------------

def build_chart_03(verdicts: dict, output_path: Path) -> None:
    recall_data = verdicts["phase_b"]["per_brand"]
    dissoc = verdicts["dissociation"]

    fig = plt.figure(figsize=(12, 8.5))
    apply_editorial_layout(
        fig,
        title="Two-channel Recall — R_cat × R_cult on the v0.21 cosmetics panel",
        subtitle="Three v1.5 dissociation quadrants. Type 2 (cultural-preferred) is the primary v0.21 hypothesis.",
        source=("Source: AIAS™ Presence Measurement Protocol v0.21 (May 2026). "
                "v1.5 two-channel Recall per SSRN 6810758. Upstream: v0.20 SSRN 6811441."),
    )

    ax = fig.add_axes([0.08, 0.13, 0.60, 0.72])

    # Type 1 quadrant: R_cat ≥ 5, R_cult ≤ 2 (canonical-preferred, lower-right)
    type1_rect = Rectangle((5, -0.4), 14.4, 2.7, facecolor="#3E8EC9", alpha=0.08,
                           edgecolor="#3E8EC9", linewidth=0.5, linestyle="--", zorder=1)
    ax.add_patch(type1_rect)

    # Type 2 quadrant: R_cat ≤ 2, R_cult ≥ 5 (cultural-preferred, upper-left) ← PRIMARY
    type2_rect = Rectangle((-0.4, 5), 2.7, 14.4, facecolor="#A560E8", alpha=0.14,
                           edgecolor="#A560E8", linewidth=1.0, linestyle="-", zorder=1)
    ax.add_patch(type2_rect)

    # Iwachu band on left edge (small visual cue, since Iwachu is on C_P axis)
    # We omit the Iwachu rectangle in this chart — it's a C_P-axis pattern, not R_cat/R_cult.

    # Quadrant labels in EMPTY zones (corners)
    # Type 2 label — upper-left, just inside the shaded band, at the top
    ax.text(0.15, 18.5, "TYPE 2", fontsize=11, fontweight="bold",
            color="#7B2DB3", ha="left", va="top")
    ax.text(0.15, 17.7, "cultural-preferred",
            fontsize=8, color="#7B2DB3", style="italic", ha="left", va="top")
    ax.text(0.15, 17.1, "(R_cat ≤ 2  ∧  R_cult ≥ 5)",
            fontsize=7.5, color="#7B2DB3", style="italic", ha="left", va="top")

    # Type 1 label — lower-right corner
    ax.text(18.7, 0.4, "TYPE 1", fontsize=11, fontweight="bold",
            color="#1F6A9C", ha="right", va="bottom")
    ax.text(18.7, 1.1, "canonical-preferred",
            fontsize=8, color="#1F6A9C", style="italic", ha="right", va="bottom")

    # Per-cell scatter with jitter
    import random
    random.seed(7)
    for cell_id in ["A", "B", "C"]:
        cell_brands = [b for b in recall_data if recall_data[b]["cell"] == cell_id]
        xs, ys = [], []
        for b in cell_brands:
            x = recall_data[b]["r_cat"] + random.uniform(-0.12, 0.12)
            y = recall_data[b]["r_cult"] + random.uniform(-0.12, 0.12)
            xs.append(x)
            ys.append(y)
        ax.scatter(xs, ys, s=90, color=CELL_COLORS[cell_id], alpha=0.80,
                   edgecolors="white", linewidth=1.0, zorder=3,
                   label=f"Cell {cell_id} — {CELL_LABELS_SHORT[cell_id]}")

    # Annotate Type 2 cases by name — manual offsets to avoid overlap
    # Use raw (non-jittered) positions for arrow endpoints
    # v0.21 has 4 Type 2 cases (3 Cell B + 1 Cell C); extended to 5 entries for headroom
    type2_cases = sorted(dissoc["type_2"], key=lambda c: (c["r_cat"], c["r_cult"]))
    offsets = [(2.8, 0.0), (3.0, 1.2), (3.0, -1.2), (3.0, 2.4), (3.0, -2.4)]
    for case, (dx, dy) in zip(type2_cases, offsets):
        x, y = case["r_cat"], case["r_cult"]
        ax.annotate(f"{case['brand']}\n(R_cat={case['r_cat']}, R_cult={case['r_cult']})",
                    xy=(x, y), xytext=(x + dx, y + dy),
                    fontsize=8, color="#7B2DB3", fontweight="bold",
                    ha="left", va="center", zorder=5,
                    arrowprops=dict(arrowstyle="-", color="#7B2DB3",
                                    lw=0.7, alpha=0.7,
                                    connectionstyle="arc3,rad=0.15"))

    ax.set_xlim(-1, 19.5)
    ax.set_ylim(-1, 19.5)
    ax.set_xticks(range(0, 19, 3))
    ax.set_yticks(range(0, 19, 3))
    ax.set_xlabel("R_cat — canonical Recall (mentions across q1–q3 × 6 models, 0–18)",
                  fontsize=10, color=GRAY_TITLE, labelpad=8)
    ax.set_ylabel("R_cult — cultural-footprint Recall (mentions across q4–q6 × 6 models, 0–18)",
                  fontsize=10, color=GRAY_TITLE, labelpad=8)

    # Quadrant threshold lines
    for v in [2, 5]:
        ax.axvline(v, color=GRAY_SUB, linewidth=0.4, linestyle=":", alpha=0.5, zorder=2)
        ax.axhline(v, color=GRAY_SUB, linewidth=0.4, linestyle=":", alpha=0.5, zorder=2)

    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color(GRAY_LIGHT)
    ax.spines["bottom"].set_color(GRAY_LIGHT)
    ax.tick_params(labelsize=9)
    ax.set_axisbelow(True)
    ax.grid(True, color=GRAY_LIGHT, alpha=0.25, linewidth=0.4, zorder=0)

    ax.legend(loc="upper right", frameon=False, fontsize=9,
              labelcolor=GRAY_TITLE, handletextpad=0.5)

    # Side panel — Type 2 case list
    panel_x = 0.72
    panel_y_top = 0.83

    fig.text(panel_x, panel_y_top, "Type 2 cases — PRIMARY",
             fontsize=11, fontweight="bold", color="#7B2DB3",
             ha="left", va="top")
    fig.text(panel_x, panel_y_top - 0.030,
             f"{dissoc['type_2_count']} total · {len(dissoc['type_2_cells'])} of 3 cells",
             fontsize=8.5, color=GRAY_SUB, ha="left", va="top")

    y_off = panel_y_top - 0.075
    for case in sorted(dissoc["type_2"], key=lambda c: -c["r_cult"]):
        fig.text(panel_x, y_off,
                 f"Cell {case['cell']} · {case['brand']}",
                 fontsize=9, fontweight="bold",
                 color=CELL_COLORS[case["cell"]], ha="left", va="top")
        fig.text(panel_x, y_off - 0.025,
                 f"  R_cat = {case['r_cat']},  R_cult = {case['r_cult']}",
                 fontsize=8, color=GRAY_TITLE, ha="left", va="top")
        y_off -= 0.062

    # Type 1 cases (descriptive)
    fig.text(panel_x, y_off, "Type 1 cases (descriptive)",
             fontsize=10, fontweight="bold", color="#1F6A9C",
             ha="left", va="top")
    fig.text(panel_x, y_off - 0.025,
             f"{dissoc['type_1_count']} total · {len(dissoc['type_1_cells'])} of 3 cells",
             fontsize=8, color=GRAY_SUB, ha="left", va="top")
    y_off -= 0.060
    for case in dissoc["type_1"][:4]:  # cap at 4 to keep panel clean
        fig.text(panel_x, y_off,
                 f"Cell {case['cell']} · {case['brand']}",
                 fontsize=8, color=CELL_COLORS[case["cell"]], ha="left", va="top")
        y_off -= 0.022

    # Bottom headline
    fig.text(0.08, 0.067,
             f"H_Type2_emergence → EMERGED  "
             f"({sum(1 for c in dissoc['type_2'] if c['cell']=='B')} cases in Cell B). "
             f"Cultural-channel Recall pathway transitions PARTIAL (v0.20) → EMERGED (v0.21).",
             fontsize=9, color="#7B2DB3", fontweight="bold",
             ha="left", va="top")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, format="pdf", dpi=300)
    plt.close(fig)
    print(f"  ✓ {output_path.name}")


# --- Main --------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="Build v0.21 charts (v2 — single-chart layouts, side panels)")
    parser.add_argument("--verdicts", default=str(DEFAULT_VERDICTS))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    args = parser.parse_args()

    verdicts_path = Path(args.verdicts).expanduser()
    output_dir = Path(args.output_dir).expanduser()

    if not verdicts_path.exists():
        print(f"ERROR: verdicts not found at {verdicts_path}", file=sys.stderr)
        return 2

    print("Building v0.21 charts (v2 layout)")
    print(f"  Verdicts source: {verdicts_path}")
    print(f"  Output directory: {output_dir}")
    print(f"  Font: {'Akkurat Pro' if register_akkurat() else 'sans-serif fallback'}")

    verdicts = load_verdicts(verdicts_path)
    print()

    build_chart_01(verdicts, output_dir / "chart_01_cp_distribution.pdf")
    build_chart_02(verdicts, output_dir / "chart_02_dissociation_scatter.pdf")
    build_chart_03(verdicts, output_dir / "chart_03_channel_asymmetry.pdf")

    print(f"\n✓ All charts written to {output_dir}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
