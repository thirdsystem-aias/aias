#!/usr/bin/env python3
"""
build_charts_aias_1_0.py — Third System brand-format charts for the AIAS 1.0
synthesis paper.

Six charts per outline §8 inventory (JAR target length):
  chart_01_three_layers.pdf            — conceptual: Mental + Physical + AI Availability
  chart_02_anchor_base_lineage.pdf     — v0.16 → v0.21 substrate-family anchor base
  chart_03_iwachu_cross_phase.pdf      — Iwachu count by phase × cell
  chart_04_type2_emergence.pdf         — Type 2 v0.20 PARTIAL → v0.21 EMERGED
  chart_05_il_direct_forest.pdf        — H_IdentityLoad_Direct δ forest plot (v0.20, v0.21)
  chart_06_phantom_channel.pdf         — v0.21 Phantom R_cat_phantom × R_cult_phantom scatter

Editorial convention (matches v0.21 phase report):
  - Title bold top-left
  - Gray subtitle below title
  - Thin Indigo (#37237B) horizontal separator rule
  - Italic gray source line at bottom citing upstream SSRN IDs + lock tag
  - Akkurat Pro font registered at module top

Data source: osf/aias_1_0/aias_1_0_synthesis_data.json (locked at
aias-1-0-data-locked). No per-phase JSON imports — synthesis_data.json is
the single source of truth.

Usage:
    python scripts/build_charts_aias_1_0.py
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

REPO = Path(__file__).resolve().parent.parent
DATA_PATH = REPO / "osf" / "aias_1_0" / "aias_1_0_synthesis_data.json"
OUTPUT_DIR = REPO / "reports" / "figs" / "aias_1_0"

# Brand tokens (Third System; primary Indigo).
INDIGO       = "#37237B"
INDIGO_LIGHT = "#7B5FB8"
VIOLET       = "#A560E8"   # Cell B
CYAN         = "#3E8EC9"   # Cell C
GRAY_TITLE   = "#1A1A1A"
GRAY_SUB     = "#666666"
GRAY_SOURCE  = "#999999"
GRAY_LIGHT   = "#CCCCCC"
GRAY_RULE    = "#E5E5E5"
PASS_GREEN   = "#2D7D4A"

CELL_COLORS = {"A": INDIGO, "B": VIOLET, "C": CYAN}
CELL_LABELS = {"A": "Cell A (Prestige / medium IL)",
               "B": "Cell B (Celebrity-DTC / high IL)",
               "C": "Cell C (Mass / low IL)"}

CANONICAL_SOURCE = (
    "Source: AIAS™ 1.0 synthesis paper data — osf/aias_1_0/aias_1_0_synthesis_data.json "
    "(lock tag aias-1-0-data-locked). Upstream: SSRN 6791999 (v0.16), 6802261 (v0.17), "
    "6806558 (v0.18), 6809182 (v0.19), 6811441 (v0.20), 6815378 (v0.21); methodology "
    "v1.6 SSRN 6816340. Five methodology papers v1.2–v1.6 in citation chain."
)


def register_akkurat() -> bool:
    dirs = [Path.home() / ".fonts" / "Akkurat", Path.home() / "Library" / "Fonts"]
    n = 0
    for d in dirs:
        if not d.exists():
            continue
        for pattern in ("*.otf", "*.ttf"):
            for f in d.glob(pattern):
                if "akkurat" in f.name.lower():
                    try:
                        fm.fontManager.addfont(str(f)); n += 1
                    except Exception:
                        pass
    if n > 0:
        plt.rcParams["font.family"] = ["Akkurat Pro", "sans-serif"]
        return True
    plt.rcParams["font.family"] = ["sans-serif"]
    return False


def apply_editorial_layout(fig, title: str, subtitle: str, source: str = CANONICAL_SOURCE,
                            title_y: float = 0.965, subtitle_y: float = 0.930,
                            rule_y: float = 0.905, source_y: float = 0.025) -> None:
    fig.text(0.06, title_y, title, fontsize=14, fontweight="bold",
             color=GRAY_TITLE, ha="left", va="top")
    fig.text(0.06, subtitle_y, subtitle, fontsize=9.5,
             color=GRAY_SUB, ha="left", va="top")
    fig.add_artist(plt.Line2D([0.06, 0.94], [rule_y, rule_y],
                              color=INDIGO, linewidth=0.6,
                              transform=fig.transFigure))
    fig.text(0.06, source_y, source, fontsize=7, style="italic",
             color=GRAY_SOURCE, ha="left", va="bottom", wrap=True)


def load_data() -> dict:
    with DATA_PATH.open() as f:
        return json.load(f)


# ---------------------------------------------------------------- Chart 1 ----

def build_chart_01_three_layers(data: dict, output_path: Path) -> None:
    """Conceptual: Mental + Physical + AI Availability as three measurable layers."""
    fig = plt.figure(figsize=(11, 7.5))
    apply_editorial_layout(
        fig,
        title="Three measurable layers of brand availability",
        subtitle="AI Availability as a third measurable layer alongside Ehrenberg-Bass Mental and Physical Availability",
    )

    ax = fig.add_axes([0.06, 0.12, 0.88, 0.78])
    ax.set_xlim(0, 12); ax.set_ylim(0, 8); ax.axis("off")

    layers = [
        ("Mental Availability",  "Memory-anchored\nbrand retrieval",  "Sharp 2010; Sharp & Romaniuk 2021", 1.5, INDIGO_LIGHT),
        ("Physical Availability", "Distribution-anchored\nbrand access", "Sharp & Romaniuk 2021",            5.5, INDIGO_LIGHT),
        ("AI Availability",       "Intermediary-anchored\nbrand retrieval", "AIAS™ 1.0 (present paper)\nmeasured component: Presence", 9.5, INDIGO),
    ]
    for label, sub, cite, cx, color in layers:
        box = FancyBboxPatch((cx - 1.55, 3.0), 3.1, 3.3,
                              boxstyle="round,pad=0.08,rounding_size=0.15",
                              facecolor=color, edgecolor="white", linewidth=1.5,
                              alpha=0.92 if color == INDIGO else 0.75)
        ax.add_patch(box)
        ax.text(cx, 5.5, label, ha="center", va="center", fontsize=12.5,
                fontweight="bold", color="white")
        ax.text(cx, 4.55, sub, ha="center", va="center", fontsize=9.5, color="white")
        ax.text(cx, 2.5, cite, ha="center", va="top", fontsize=7.5,
                style="italic", color=GRAY_SUB)

    # Connector arc/line at top: "Three measurable layers of brand availability"
    ax.plot([1.5, 9.5], [6.7, 6.7], color=GRAY_LIGHT, linewidth=0.7)
    for cx in (1.5, 5.5, 9.5):
        ax.plot([cx, cx], [6.3, 6.7], color=GRAY_LIGHT, linewidth=0.7)
    ax.text(5.5, 7.05, "Three measurable layers of brand availability",
            ha="center", va="bottom", fontsize=10, color=GRAY_SUB, style="italic")

    # Footer caveat: Presence only, full composite roadmap
    ax.text(6.0, 1.6,
            "AIAS™ 1.0 operationalizes the Presence component of the multi-component AIAS construct.\n"
            "Full six-component composite (Phase 4) is a multi-year research roadmap; not claimed here.",
            ha="center", va="top", fontsize=8.5, color=GRAY_SUB)

    fig.savefig(output_path, format="pdf", bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------- Chart 2 ----

def build_chart_02_anchor_base_lineage(data: dict, output_path: Path) -> None:
    """v0.16 → v0.21 substrate-family anchor base timeline."""
    fig = plt.figure(figsize=(11, 6.5))
    apply_editorial_layout(
        fig,
        title="Cumulative substrate-family anchor base (v0.16 → v0.21)",
        subtitle="Five substrate families anchored under locked v1.6 methodology",
    )

    ax = fig.add_axes([0.06, 0.18, 0.88, 0.66])

    # Group phases by substrate family for cumulative-count display.
    families = [
        ("Kitchenware",          ["v0.16", "v0.17"]),
        ("Indie fragrance",      ["v0.18"]),
        ("Audiophile headphones", ["v0.19"]),
        ("Skincare",             ["v0.20"]),
        ("Cosmetics",            ["v0.21"]),
    ]

    phases = data["phases"]
    by_phase = {p["phase"]: p for p in phases}
    phase_order = [p["phase"] for p in phases]
    x_pos = list(range(len(phase_order)))

    cumulative = []
    seen = set()
    for p in phase_order:
        family = next(f for f, ps in families if p in ps)
        seen.add(family)
        cumulative.append(len(seen))

    # Lineage line
    ax.plot(x_pos, [1] * len(x_pos), color=GRAY_LIGHT, linewidth=1.2, zorder=1)
    # Phase markers
    for i, p in enumerate(phase_order):
        ax.scatter([i], [1], s=180, color=INDIGO, edgecolor="white",
                   linewidth=1.8, zorder=3)
        ax.text(i, 1.0, f"{cumulative[i]}", ha="center", va="center",
                fontsize=9, color="white", fontweight="bold", zorder=4)
        # Phase label below
        ax.text(i, 0.55, p, ha="center", va="top", fontsize=9.5,
                color=GRAY_TITLE, fontweight="bold")
        ax.text(i, 0.30, by_phase[p]["substrate"], ha="center", va="top",
                fontsize=8.5, color=GRAY_SUB)
        ax.text(i, 0.10, f"SSRN {by_phase[p]['ssrn_id']}", ha="center", va="top",
                fontsize=7.5, color=GRAY_SOURCE, style="italic")

    # Family-bracket annotations above the lineage
    for family, phs in families:
        idxs = [phase_order.index(p) for p in phs if p in phase_order]
        if not idxs:
            continue
        x0, x1 = min(idxs), max(idxs)
        mid = (x0 + x1) / 2.0
        ax.plot([x0 - 0.25, x1 + 0.25], [1.55, 1.55], color=INDIGO, linewidth=1.0)
        ax.plot([x0 - 0.25, x0 - 0.25], [1.45, 1.55], color=INDIGO, linewidth=1.0)
        ax.plot([x1 + 0.25, x1 + 0.25], [1.45, 1.55], color=INDIGO, linewidth=1.0)
        ax.text(mid, 1.65, family, ha="center", va="bottom", fontsize=9,
                color=INDIGO, fontweight="bold")

    # Annotation: cumulative count label
    ax.text(len(phase_order) - 0.5, 2.05,
            "Cumulative substrate-family count (in circle)",
            ha="right", va="top", fontsize=8, color=GRAY_SUB, style="italic")

    ax.set_xlim(-0.6, len(phase_order) - 0.4)
    ax.set_ylim(0, 2.3)
    ax.axis("off")

    fig.savefig(output_path, format="pdf", bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------- Chart 3 ----

def build_chart_03_iwachu_cross_phase(data: dict, output_path: Path) -> None:
    """Iwachu dissociation count by phase, with v0.20 / v0.21 broken down by cell."""
    fig = plt.figure(figsize=(11, 7))
    apply_editorial_layout(
        fig,
        title="Iwachu dissociation cases across the five-substrate anchor base",
        subtitle="High Recognition (C_P ≥ 5) with sparse canonical Recall (R_cat ≤ 2) — multi-cell distribution in three of five families",
    )

    ax = fig.add_axes([0.10, 0.18, 0.82, 0.66])

    phases = data["phases"]
    by_phase = {p["phase"]: p for p in phases}
    phase_order = [p["phase"] for p in phases]
    x = list(range(len(phase_order)))

    # For v0.20 / v0.21, break Iwachu by cell. For v0.16-v0.19, present a single
    # narrative bar.
    for i, p in enumerate(phase_order):
        rec = by_phase[p]
        count = rec.get("dissociation_counts", {}).get("iwachu")
        brands = rec.get("dissociation_brands", {}).get("iwachu", [])
        if isinstance(count, int) and brands:
            # Cell breakdown
            cells = {"A": 0, "B": 0, "C": 0}
            for b in brands:
                cells[b["cell"]] = cells.get(b["cell"], 0) + 1
            bottom = 0
            for cell_id in ("A", "B", "C"):
                v = cells[cell_id]
                if v == 0:
                    continue
                ax.bar(i, v, bottom=bottom, color=CELL_COLORS[cell_id],
                       width=0.62, edgecolor="white", linewidth=1.2, zorder=3)
                ax.text(i, bottom + v / 2.0, str(v), ha="center", va="center",
                        fontsize=10, fontweight="bold", color="white", zorder=4)
                bottom += v
            ax.text(i, bottom + 0.35, f"total {count}", ha="center", va="bottom",
                    fontsize=9, color=GRAY_TITLE, fontweight="bold")
        elif isinstance(count, str):
            # Narrative: show a light placeholder bar with annotation
            ax.bar(i, 1.0, color=GRAY_LIGHT, width=0.62, edgecolor="white",
                   linewidth=1.2, alpha=0.6, zorder=3)
            ax.text(i, 0.5, "narrative\n(single-channel\nframework)",
                    ha="center", va="center", fontsize=7.5, color=GRAY_SUB,
                    style="italic", zorder=4)
        else:
            # None — explicit N/A note
            ax.text(i, 0.7, "N/A", ha="center", va="center", fontsize=9.5,
                    color=GRAY_SOURCE, style="italic")
            ax.text(i, 0.3, "(2-cell design)" if p == "v0.19" else "(pre-v1.4 framework)",
                    ha="center", va="center", fontsize=7.5, color=GRAY_SOURCE,
                    style="italic")

    ax.set_xticks(x)
    ax.set_xticklabels([f"{p}\n{by_phase[p]['substrate']}" for p in phase_order],
                       fontsize=9, color=GRAY_TITLE)
    ax.set_ylabel("Iwachu dissociation cases (all cells, scored phases)",
                  fontsize=9.5, color=GRAY_TITLE, labelpad=8)
    ax.set_ylim(0, 16)
    ax.tick_params(axis="y", labelsize=9)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color(GRAY_LIGHT)
    ax.spines["bottom"].set_color(GRAY_LIGHT)
    ax.set_axisbelow(True)
    ax.grid(axis="y", color=GRAY_LIGHT, alpha=0.3, linewidth=0.4, zorder=0)

    # Cell-color legend (bottom margin, horizontal, between x-axis labels and source line)
    legend_y = 0.085
    legend_block_widths = [0.20, 0.30, 0.20]  # approximate text widths in fig coords
    legend_start_x = 0.12
    cx = legend_start_x
    for cell_id, w in zip(("A", "B", "C"), legend_block_widths):
        fig.add_artist(Rectangle((cx, legend_y - 0.008), 0.016, 0.016,
                                  facecolor=CELL_COLORS[cell_id], edgecolor="white",
                                  transform=fig.transFigure))
        fig.text(cx + 0.022, legend_y, CELL_LABELS[cell_id], fontsize=8.5,
                 color=GRAY_TITLE, ha="left", va="center")
        cx += w

    fig.savefig(output_path, format="pdf", bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------- Chart 4 ----

def build_chart_04_type2_emergence(data: dict, output_path: Path) -> None:
    """v0.20 PARTIAL → v0.21 EMERGED. Cell B count vs all-cell algorithmic."""
    fig = plt.figure(figsize=(11, 7.5))
    apply_editorial_layout(
        fig,
        title="Type 2 quadrant emergence — v0.20 PARTIAL → v0.21 EMERGED",
        subtitle="Cell B count drives the H_Type2_emergence verdict (≥3 → EMERGED); cross-phase all-cell count surfaces out-of-cell cases",
    )

    ax = fig.add_axes([0.10, 0.18, 0.55, 0.66])

    by_phase = {p["phase"]: p for p in data["phases"]}
    phases_shown = ["v0.20", "v0.21"]
    x = list(range(len(phases_shown)))

    bar_w = 0.34
    cell_b_counts = []
    out_of_cell_counts = []
    for p in phases_shown:
        h = by_phase[p]["v1_4_v1_5_verdicts"]["H_Type2_emergence"]
        cell_b = h["cell_b_type2_count"]
        ooc = by_phase[p]["dissociation_counts"]["type_2"] - cell_b
        cell_b_counts.append(cell_b)
        out_of_cell_counts.append(ooc)

    bars1 = ax.bar([i - bar_w / 2 for i in x], cell_b_counts, bar_w,
                   color=VIOLET, edgecolor="white", linewidth=1.2, label="Cell B count (verdict-driving)",
                   zorder=3)
    bars2 = ax.bar([i + bar_w / 2 for i in x], out_of_cell_counts, bar_w,
                   color=GRAY_LIGHT, edgecolor="white", linewidth=1.2,
                   label="Out-of-cell (algorithmic; surfaced by synthesis)", zorder=3)

    for i, (cb, oc) in enumerate(zip(cell_b_counts, out_of_cell_counts)):
        ax.text(i - bar_w / 2, cb + 0.07, str(cb), ha="center", va="bottom",
                fontsize=10, fontweight="bold", color=GRAY_TITLE)
        ax.text(i + bar_w / 2, oc + 0.07, str(oc), ha="center", va="bottom",
                fontsize=10, fontweight="bold", color=GRAY_TITLE)

    # EMERGED threshold line
    ax.axhline(3, color=PASS_GREEN, linewidth=0.8, linestyle="--", alpha=0.7, zorder=2)
    ax.text(len(x) - 0.5, 3.08, "EMERGED threshold = 3 (Cell B)", ha="right", va="bottom",
            fontsize=8, color=PASS_GREEN, style="italic")

    # Verdict labels under each phase
    for i, p in enumerate(phases_shown):
        verdict = by_phase[p]["v1_4_v1_5_verdicts"]["H_Type2_emergence"]["verdict"]
        ax.text(i, -0.55, f"{p}\nverdict: {verdict}", ha="center", va="top",
                fontsize=9.5, color=GRAY_TITLE, fontweight="bold")

    ax.set_xticks(x); ax.set_xticklabels([])
    ax.set_ylabel("Type 2 cases (R_cat ≤ 2 ∧ R_cult ≥ 5)",
                  fontsize=9.5, color=GRAY_TITLE, labelpad=8)
    ax.set_ylim(0, 5.5)
    ax.tick_params(axis="y", labelsize=9)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color(GRAY_LIGHT); ax.spines["bottom"].set_color(GRAY_LIGHT)
    ax.set_axisbelow(True)
    ax.grid(axis="y", color=GRAY_LIGHT, alpha=0.3, linewidth=0.4, zorder=0)

    ax.legend(loc="upper left", fontsize=8.5, frameon=False, bbox_to_anchor=(0.0, 1.0))

    # Side panel — Cell B case anchors + out-of-cell anchors
    panel_x = 0.70
    fig.text(panel_x, 0.78, "Cell B case anchors", fontsize=10, fontweight="bold",
             color=GRAY_TITLE, ha="left", va="top")

    y = 0.745
    for p in phases_shown:
        fig.text(panel_x, y, p, fontsize=9, fontweight="bold",
                 color=INDIGO, ha="left", va="top")
        for b in by_phase[p]["dissociation_brands"]["type_2"]:
            if b["cell"] != "B":
                continue
            fig.text(panel_x + 0.028, y,
                     f"· {b['brand']:<22} R_cat={b['r_cat']:<2}  R_cult={b['r_cult']}",
                     fontsize=8, color=GRAY_TITLE, family="monospace",
                     ha="left", va="top")
            y -= 0.028
        y -= 0.020

    fig.text(panel_x, y, "Out-of-cell cases (synthesis layer)", fontsize=10,
             fontweight="bold", color=GRAY_TITLE, ha="left", va="top")
    y -= 0.030
    for p, cases in data["cross_phase_summary"]["type_2_out_of_cell_cases_by_phase"].items():
        for c in cases:
            fig.text(panel_x, y,
                     f"{p}  {c['brand']:<18} cell={c['cell']}  R_cat={c['r_cat']}  R_cult={c['r_cult']}",
                     fontsize=8, color=GRAY_TITLE, family="monospace",
                     ha="left", va="top")
            y -= 0.026

    fig.savefig(output_path, format="pdf", bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------- Chart 5 ----

def build_chart_05_il_direct_forest(data: dict, output_path: Path) -> None:
    """H_IdentityLoad_Direct δ forest plot — v0.20 PARTIAL + v0.21 CONFIRMED."""
    fig = plt.figure(figsize=(11, 7.5))
    apply_editorial_layout(
        fig,
        title="H_IdentityLoad_Direct — per-cell δ = mean(R_cult) − mean(R_cat) with 95% bootstrap CIs",
        subtitle="v0.20 PARTIAL (skincare; Cell B vs. Cell C signal) → v0.21 CONFIRMED (cosmetics; monotonic A < C < B)",
    )

    ax = fig.add_axes([0.20, 0.18, 0.72, 0.66])

    deltas = data["cross_phase_summary"]["il_direct_deltas_by_phase_cell"]
    rows = []
    for phase in ("v0.20", "v0.21"):
        for cell in ("A", "B", "C"):
            d = deltas[phase][cell]
            rows.append({
                "phase": phase, "cell": cell,
                "delta": d["delta"], "lo": d["ci_lo"], "hi": d["ci_hi"],
                "excl": d["ci_excludes_zero"],
            })

    rows = list(reversed(rows))   # top of plot = first listed
    y_pos = list(range(len(rows)))
    labels = [f"{r['phase']} · Cell {r['cell']}" for r in rows]

    # Zero reference line
    ax.axvline(0, color=GRAY_LIGHT, linewidth=0.8, linestyle="-", zorder=1)

    for i, r in enumerate(rows):
        color = CELL_COLORS[r["cell"]]
        # Bootstrap CI bar
        ax.plot([r["lo"], r["hi"]], [i, i], color=color, linewidth=2.2, alpha=0.7,
                zorder=2, solid_capstyle="round")
        # CI tick marks
        for x_tick in (r["lo"], r["hi"]):
            ax.plot([x_tick, x_tick], [i - 0.18, i + 0.18], color=color,
                    linewidth=1.6, zorder=2)
        # Point estimate
        ax.scatter([r["delta"]], [i], s=70, color=color,
                   edgecolor="white", linewidth=1.5, zorder=3)
        # Delta annotation
        ax.text(r["hi"] + 0.3, i, f"δ = {r['delta']:+.2f}  [{r['lo']:+.2f}, {r['hi']:+.2f}]"
                + ("  ✓" if r["excl"] else ""),
                fontsize=8.5, color=color, va="center", ha="left",
                fontweight="bold" if r["excl"] else "normal")

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=9.5, color=GRAY_TITLE)
    ax.set_xlabel("δ = mean(R_cult) − mean(R_cat), per cell",
                  fontsize=9.5, color=GRAY_TITLE, labelpad=8)
    ax.set_xlim(-8, 14)
    ax.tick_params(axis="x", labelsize=9)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color(GRAY_LIGHT); ax.spines["bottom"].set_color(GRAY_LIGHT)
    ax.set_axisbelow(True)
    ax.grid(axis="x", color=GRAY_LIGHT, alpha=0.3, linewidth=0.4, zorder=0)

    # Phase verdict annotations need to fit in the strip between the chart's
    # bottom (axes bottom = 0.18, xlabel ~ y=0.155) and the source line top
    # (source at y=0.025 may wrap to multiple lines, extending up to ~y=0.07).
    # Park them above the chart instead, in the strip between the rule
    # (y=0.905) and the axes top (y=0.84) — clear of all other content.
    # Two-line stacked: bold verdict line above, italic detail line below.
    fig.text(0.22, 0.892, "v0.20 verdict: PARTIAL", fontsize=9.5, fontweight="bold",
             color=INDIGO, ha="left", va="top")
    fig.text(0.22, 0.868,
             "Cell B CI excludes 0; Cell A against IL (skincare-specific).",
             fontsize=8, color=GRAY_SUB, ha="left", va="top", style="italic")

    fig.text(0.62, 0.892, "v0.21 verdict: CONFIRMED", fontsize=9.5, fontweight="bold",
             color=PASS_GREEN, ha="left", va="top")
    fig.text(0.62, 0.868,
             "Monotonic A < C < B; focal CIs exclude 0.",
             fontsize=8, color=GRAY_SUB, ha="left", va="top", style="italic")

    fig.savefig(output_path, format="pdf", bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------- Chart 6 ----

def build_chart_06_phantom_channel(data: dict, output_path: Path) -> None:
    """v0.21 Phantom Brand Persistence — R_cat_phantom × R_cult_phantom scatter."""
    fig = plt.figure(figsize=(11, 8))
    apply_editorial_layout(
        fig,
        title="v0.21 Phantom Brand Persistence — off-panel channel signature (R_cat_phantom × R_cult_phantom)",
        subtitle="Six off-panel brands clear K = 6; channel signatures track Identity Load (validity anchor Glossier passes with margin)",
    )

    ax = fig.add_axes([0.10, 0.16, 0.62, 0.70])

    sigs = data["cross_phase_summary"]["phantom_channel_signatures_v021"]

    # Validity-anchor threshold lines at K = 6 on both axes
    ax.axhline(6, color=PASS_GREEN, linewidth=0.7, linestyle="--", alpha=0.6, zorder=1)
    ax.axvline(6, color=PASS_GREEN, linewidth=0.7, linestyle="--", alpha=0.6, zorder=1)
    ax.text(0.3, 6.4, "K = 6 (validity threshold)", fontsize=7.5, color=PASS_GREEN,
            style="italic", ha="left", va="bottom")

    # Channel signature classification
    def channel_color(rcat, rcult):
        if rcat == 0 and rcult > 0:  return VIOLET     # pure cultural
        if rcult == 0 and rcat > 0:  return INDIGO     # pure canonical
        return CYAN                                      # mixed

    for s in sigs:
        rcat, rcult = s["r_cat_phantom"], s["r_cult_phantom"]
        color = channel_color(rcat, rcult)
        ax.scatter([rcat], [rcult], s=140, color=color, edgecolor="white",
                   linewidth=1.6, alpha=0.92, zorder=3)
        # Label position: nudge to avoid the marker
        dx, dy = (0.6, 0.3)
        if s["brand"] == "Glossier":         dx, dy = (0.6, -0.6)
        if s["brand"] == "Estée Lauder":     dx, dy = (-0.5, 0.7)
        if s["brand"] == "Clinique":         dx, dy = (-0.5, 0.7)
        if s["brand"] == "Make Up For Ever": dx, dy = (0.6, -0.5)
        ax.text(rcat + dx, rcult + dy, s["brand"], fontsize=9,
                color=GRAY_TITLE, va="center",
                ha="left" if dx > 0 else "right", zorder=4)

    ax.set_xlim(-0.5, 16); ax.set_ylim(-0.5, 16)
    ax.set_xlabel("R_cat_phantom (canonical-channel mentions, max 18)",
                  fontsize=9.5, color=GRAY_TITLE, labelpad=8)
    ax.set_ylabel("R_cult_phantom (cultural-channel mentions, max 18)",
                  fontsize=9.5, color=GRAY_TITLE, labelpad=8)
    ax.tick_params(axis="both", labelsize=9)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color(GRAY_LIGHT); ax.spines["bottom"].set_color(GRAY_LIGHT)
    ax.set_axisbelow(True)
    ax.grid(True, color=GRAY_LIGHT, alpha=0.3, linewidth=0.4, zorder=0)

    # Right-side panel — per-brand table
    panel_x = 0.74
    fig.text(panel_x, 0.82, "Off-panel passing brands (v0.21)", fontsize=10,
             fontweight="bold", color=GRAY_TITLE, ha="left", va="top")
    fig.text(panel_x, 0.795, "R_phantom ≥ K = 6", fontsize=8, style="italic",
             color=GRAY_SUB, ha="left", va="top")
    headers = f"{'brand':<18} {'R_cat':>5} {'R_cult':>6} {'total':>6}"
    fig.text(panel_x, 0.760, headers, fontsize=8, color=GRAY_SUB,
             family="monospace", ha="left", va="top")
    y = 0.735
    for s in sigs:
        line = f"{s['brand'][:18]:<18} {s['r_cat_phantom']:>5} {s['r_cult_phantom']:>6} {s['r_phantom']:>6}"
        fig.text(panel_x, y, line, fontsize=8, color=GRAY_TITLE,
                 family="monospace", ha="left", va="top")
        y -= 0.030

    # Channel signature legend
    fig.text(panel_x, y - 0.020, "Channel signatures", fontsize=10, fontweight="bold",
             color=GRAY_TITLE, ha="left", va="top")
    y -= 0.050
    legend_items = [(INDIGO, "Pure canonical (R_cult = 0)"),
                    (VIOLET, "Pure cultural (R_cat = 0)"),
                    (CYAN,   "Mixed channel")]
    for color, label in legend_items:
        fig.add_artist(Rectangle((panel_x, y - 0.005), 0.017, 0.017,
                                  facecolor=color, edgecolor="white",
                                  transform=fig.transFigure))
        fig.text(panel_x + 0.024, y + 0.004, label, fontsize=8.5,
                 color=GRAY_TITLE, ha="left", va="center")
        y -= 0.030

    # Validity anchor note
    inc3 = next(p for p in data["phases"] if p["phase"] == "v0.21")["v1_6_retrospective"]["inc3"]
    vc = inc3["validity_check"]
    fig.text(panel_x, y - 0.020,
             f"Validity anchor: {vc['anchor']} "
             f"R_phantom = {vc['anchor_observed']} ≥ {vc['anchor_min_required']}  "
             + ("✓" if vc["passes"] else "✗"),
             fontsize=8.5, color=PASS_GREEN if vc["passes"] else "#B83A3A",
             fontweight="bold", ha="left", va="top")

    fig.savefig(output_path, format="pdf", bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------- Main ------

def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    register_akkurat()
    data = load_data()

    charts = [
        ("chart_01_three_layers.pdf",         build_chart_01_three_layers),
        ("chart_02_anchor_base_lineage.pdf",  build_chart_02_anchor_base_lineage),
        ("chart_03_iwachu_cross_phase.pdf",   build_chart_03_iwachu_cross_phase),
        ("chart_04_type2_emergence.pdf",      build_chart_04_type2_emergence),
        ("chart_05_il_direct_forest.pdf",     build_chart_05_il_direct_forest),
        ("chart_06_phantom_channel.pdf",      build_chart_06_phantom_channel),
    ]

    for filename, builder in charts:
        path = OUTPUT_DIR / filename
        builder(data, path)
        print(f"  wrote {path.relative_to(REPO)}")

    print(f"\nAll {len(charts)} charts written to {OUTPUT_DIR.relative_to(REPO)}/")


if __name__ == "__main__":
    main()
