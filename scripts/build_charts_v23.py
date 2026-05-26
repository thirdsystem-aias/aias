#!/usr/bin/env python3
"""
AIAS v0.23 — Premium Spirits Chart Builder
Reads osf/v23/v23_verdicts.json, outputs 4 chart PDFs to reports/figs/v23/

Charts:
  chart_23_composite_bar.pdf    — AI Presence composite by brand (horizontal bar)
  chart_23_channel_heatmap.pdf  — EA vs CC recall mentions (heatmap)
  chart_23_conglomerate_box.pdf — Composite by ownership structure (box plot)
  chart_23_recall_scatter.pdf   — Recall frequency vs mean slot position (scatter)

Usage:
  cd /Users/pablou/aias
  python3 scripts/build_charts_v23.py
"""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.patches as mpatches
import numpy as np

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PIPELINE_ROOT = Path("/Users/pablou/aias")
VERDICTS_PATH = PIPELINE_ROOT / "osf" / "v23" / "v23_verdicts.json"
FIGS_DIR = PIPELINE_ROOT / "reports" / "figs" / "v23"

# ---------------------------------------------------------------------------
# Font registration — Akkurat Pro
# ---------------------------------------------------------------------------
FONT_DIRS = [
    Path.home() / ".fonts" / "Akkurat",
    Path.home() / "Library" / "Fonts",
]
for d in FONT_DIRS:
    if d.exists():
        for f in d.glob("*.otf"):
            fm.fontManager.addfont(str(f))
        for f in d.glob("*.ttf"):
            fm.fontManager.addfont(str(f))

plt.rcParams["font.family"] = ["Akkurat Pro", "sans-serif"]
plt.rcParams["axes.unicode_minus"] = False

# ---------------------------------------------------------------------------
# Brand palette — Third System indigo system
# ---------------------------------------------------------------------------
INDIGO_PRIMARY = "#37237B"
INDIGO_MED = "#6B5CA5"
INDIGO_LIGHT = "#A89BCF"
INDIGO_FADED = "#D4CDE5"
BLACK = "#1A1A1A"
GRAY = "#888888"
WHITE = "#FFFFFF"

REGIME_COLORS = {
    "Dominant": INDIGO_PRIMARY,
    "Established": INDIGO_MED,
    "Emerging": INDIGO_LIGHT,
    "Absent": INDIGO_FADED,
}

SOURCE_LINE = "AIAS\u2122 v0.23 | Protocol v1.6 | Third System\u2122"

# ---------------------------------------------------------------------------
# Shared layout: title block at top, source at bottom — all left-aligned
# ---------------------------------------------------------------------------
LEFT_X = 0.04

def add_header(fig, title, subtitle, description):
    """Left-aligned title + subtitle + description at top of figure."""
    fig.text(LEFT_X, 0.97, title,
             fontsize=13, fontweight="bold", color=BLACK,
             ha="left", va="top")
    fig.text(LEFT_X, 0.945, subtitle,
             fontsize=9, color=GRAY,
             ha="left", va="top")
    fig.text(LEFT_X, 0.915, description,
             fontsize=7.5, color=GRAY, fontstyle="italic",
             ha="left", va="top", wrap=True)

def add_source(fig):
    """Left-aligned source line at bottom."""
    fig.text(LEFT_X, 0.01, SOURCE_LINE,
             fontsize=6, color=GRAY, ha="left", va="bottom")


def load_verdicts():
    with open(VERDICTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# =========================================================================
# Chart 1: Composite Bar
# =========================================================================
def chart_composite_bar(verdicts):
    brands = sorted(verdicts["brand_details"],
                    key=lambda b: b["composite_presence"])
    names = [b["brand_name"] for b in brands]
    scores = [b["composite_presence"] for b in brands]
    colors = [REGIME_COLORS[b["regime"]] for b in brands]

    thresholds = verdicts["regime_thresholds"]
    q25, q50, q75 = thresholds["q25"], thresholds["q50"], thresholds["q75"]

    fig, ax = plt.subplots(figsize=(10, 9.5))
    fig.subplots_adjust(top=0.87, bottom=0.06, left=0.22, right=0.88)

    y_pos = np.arange(len(names))
    ax.barh(y_pos, scores, color=colors, edgecolor="none", height=0.7)

    # Quartile lines
    for val, label in [(q25, "Q25"), (q50, "Q50"), (q75, "Q75")]:
        ax.axvline(x=val, color=GRAY, linestyle="--", linewidth=0.8, alpha=0.6)
        ax.text(val + 0.3, len(names) - 0.3, label,
                fontsize=7, color=GRAY, va="bottom")

    # Regime labels on right
    for i, b in enumerate(brands):
        ax.text(scores[i] + 0.5, i, b["regime"],
                fontsize=7, color=REGIME_COLORS[b["regime"]],
                va="center", fontweight="bold")

    ax.set_yticks(y_pos)
    ax.set_yticklabels(names, fontsize=8)
    ax.set_xlabel("Composite Presence Score (0\u2013100)", fontsize=9,
                  color=BLACK, labelpad=10)
    ax.set_xlim(35, 78)

    handles = [mpatches.Patch(color=c, label=r)
               for r, c in REGIME_COLORS.items()]
    ax.legend(handles=handles, loc="lower right", fontsize=7,
              frameon=True, framealpha=0.9)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(axis="both", which="both", length=0)

    add_header(fig,
               "AI Presence Composite Score by Brand",
               "Protocol v1.6 \u2014 Premium Spirits (v0.23)",
               "All four regimes populated (6/6/6/6). Recognition at ceiling; "
               "recall drives the distribution.")
    add_source(fig)

    out = FIGS_DIR / "chart_23_composite_bar.pdf"
    fig.savefig(out, bbox_inches="tight", dpi=300)
    plt.close(fig)
    print(f"  \u2713 {out.name}")
    return out


# =========================================================================
# Chart 2: Channel Heatmap
# =========================================================================
def chart_channel_heatmap(verdicts):
    brands = sorted(verdicts["brand_details"],
                    key=lambda b: b["recall_ea"] + b["recall_cc"],
                    reverse=True)
    names = [b["brand_name"] for b in brands]
    ea = [b["recall_ea"] for b in brands]
    cc = [b["recall_cc"] for b in brands]

    data = np.array([ea, cc]).T
    max_val = max(max(ea), max(cc)) if max(max(ea), max(cc)) > 0 else 1

    fig, ax = plt.subplots(figsize=(7, 11.5))
    fig.subplots_adjust(top=0.88, bottom=0.05, left=0.30, right=0.92)

    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list("indigo", [WHITE, INDIGO_PRIMARY])

    ax.imshow(data, cmap=cmap, aspect="auto", vmin=0, vmax=max_val)

    for i in range(len(names)):
        for j in range(2):
            val = data[i, j]
            text_color = WHITE if val > max_val * 0.5 else BLACK
            ax.text(j, i, str(int(val)),
                    ha="center", va="center", fontsize=9,
                    color=text_color, fontweight="bold")

    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Editorial-Authority", "Cultural-Cult"], fontsize=9)
    ax.set_yticks(np.arange(len(names)))
    ax.set_yticklabels(names, fontsize=8)
    ax.xaxis.tick_top()

    for i, b in enumerate(brands):
        if b["brand_name"] in ("R\u00e9my Martin", "Jack Daniel's"):
            ax.add_patch(plt.Rectangle((-0.5, i - 0.5), 2, 1,
                         linewidth=2, edgecolor="#E74C3C", facecolor="none"))

    add_header(fig,
               "Recall Mentions by Channel and Brand",
               "Editorial-Authority vs Cultural-Cult",
               "Overlap = 0.80. Channels converge in high-familiarity substrates; "
               "channel-exclusive brands (red outlines) are exceptions.")
    add_source(fig)

    out = FIGS_DIR / "chart_23_channel_heatmap.pdf"
    fig.savefig(out, bbox_inches="tight", dpi=300)
    plt.close(fig)
    print(f"  \u2713 {out.name}")
    return out


# =========================================================================
# Chart 3: Conglomerate Box Plot
# =========================================================================
def chart_conglomerate_box(verdicts):
    conglom_brands = [(b["brand_name"], b["composite_presence"])
                      for b in verdicts["brand_details"] if b["conglomerate"] == 1]
    indep_brands = [(b["brand_name"], b["composite_presence"])
                    for b in verdicts["brand_details"] if b["conglomerate"] == 0]

    conglom = [v for _, v in conglom_brands]
    indep = [v for _, v in indep_brands]

    fig, ax = plt.subplots(figsize=(9, 7.5))
    fig.subplots_adjust(top=0.87, bottom=0.10, left=0.06, right=0.94)

    bp = ax.boxplot([conglom, indep], positions=[1, 2], widths=0.45,
                    patch_artist=True, showmeans=True,
                    meanprops=dict(marker="D", markerfacecolor="white",
                                   markeredgecolor=BLACK, markersize=6),
                    medianprops=dict(color=BLACK, linewidth=1.5),
                    whiskerprops=dict(color=GRAY),
                    capprops=dict(color=GRAY),
                    flierprops=dict(marker="", linewidth=0))

    bp["boxes"][0].set_facecolor(INDIGO_PRIMARY)
    bp["boxes"][0].set_alpha(0.7)
    bp["boxes"][1].set_facecolor(INDIGO_LIGHT)
    bp["boxes"][1].set_alpha(0.7)

    # Key brands to label
    label_brands_conglom = {"Patr\u00f3n", "Hennessy", "Bombay Sapphire", "Casamigos", "Del Maguey"}
    label_brands_indep = {"Fortaleza", "Hendrick's", "R\u00e9my Martin",
                          "The Balvenie", "Compass Box", "Fernet-Branca"}

    # Overlay points — stagger x to avoid dot overlap
    # Record actual (x, y) positions for annotation targeting
    dot_positions = {}  # {brand_name: (actual_x, actual_y)}

    for pos, brand_list, color in [
        (1, conglom_brands, INDIGO_PRIMARY),
        (2, indep_brands, INDIGO_LIGHT),
    ]:
        sorted_b = sorted(brand_list, key=lambda x: x[1])
        n = len(sorted_b)
        offsets = np.linspace(-0.13, 0.13, n)
        for (name, val), off in zip(sorted_b, offsets):
            actual_x = pos + off
            ax.scatter(actual_x, val,
                       color=color, edgecolors=BLACK, linewidth=0.5,
                       s=30, zorder=5, alpha=0.8)
            dot_positions[name] = (actual_x, val)

    # Label shelf: evenly space label y-positions to prevent overlap
    # Uses recorded dot positions so arrows point to actual dots
    y_min, y_max = 38, 73

    for pos, brand_list, label_set in [
        (1, conglom_brands, label_brands_conglom),
        (2, indep_brands, label_brands_indep),
    ]:
        to_label = sorted([(n, v) for n, v in brand_list if n in label_set],
                          key=lambda x: x[1])
        n_labels = len(to_label)
        if n_labels == 0:
            continue
        label_ys = np.linspace(y_min, y_max, n_labels)

        ha = "right" if pos == 1 else "left"
        label_x = 0.55 if pos == 1 else 2.45

        for (name, val), label_y in zip(to_label, label_ys):
            dot_x, dot_y = dot_positions[name]
            ax.annotate(name, (dot_x, dot_y),
                        xytext=(label_x, label_y),
                        fontsize=6.5, color=BLACK, ha=ha, va="center",
                        arrowprops=dict(arrowstyle="-", color=GRAY,
                                       linewidth=0.4, shrinkA=2, shrinkB=1))

    # p-value bracket
    bracket_y = max(max(conglom), max(indep)) + 3.5
    ax.plot([1, 1, 2, 2], [bracket_y - 0.5, bracket_y, bracket_y, bracket_y - 0.5],
            color=GRAY, linewidth=0.8)
    ax.text(1.5, bracket_y + 0.5, "t = 0.59, p = 0.28 (ns)",
            ha="center", fontsize=8, color=GRAY)

    ax.set_xticks([1, 2])
    ax.set_xticklabels(["Conglomerate\n(n=14)", "Independent\n(n=10)"],
                       fontsize=9)
    ax.set_ylabel("Composite Presence Score", fontsize=9, color=BLACK)
    ax.set_ylim(35, bracket_y + 4)
    ax.set_xlim(0.15, 2.85)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    add_header(fig,
               "Composite Presence by Ownership Structure",
               "Conglomerate (n=14) vs Independent (n=10)",
               "H_ConglomeratePortfolio falsified. 4.6% lift, not significant "
               "(p = 0.28).")
    add_source(fig)

    out = FIGS_DIR / "chart_23_conglomerate_box.pdf"
    fig.savefig(out, bbox_inches="tight", dpi=300)
    plt.close(fig)
    print(f"  \u2713 {out.name}")
    return out


# =========================================================================
# Chart 4: Recall vs Slot Scatter
# =========================================================================
def chart_recall_scatter(verdicts):
    active = [b for b in verdicts["brand_details"] if b["recall_total"] > 0]
    active = sorted(active, key=lambda b: b["composite_presence"], reverse=True)

    fig, ax = plt.subplots(figsize=(9, 7.5))
    fig.subplots_adjust(top=0.87, bottom=0.10, left=0.12, right=0.92)

    xs, ys = [], []
    for b in active:
        x = b["recall_rate"]
        y = b["mean_slot_position"]
        s = max(b["elaboration_count"] * 15, 20)
        color = REGIME_COLORS[b["regime"]]
        ax.scatter(x, y, s=s, color=color, edgecolors=BLACK,
                   linewidth=0.5, alpha=0.8, zorder=5)
        xs.append(x)
        ys.append(y)

    ax.invert_yaxis()

    # Manual label placements — explicit offsets to prevent collisions
    # Offsets are (dx, dy) in points from the data point
    LABEL_OFFSETS = {
        "Patr\u00f3n":          (8, -8),
        "Hennessy":             (8, 6),
        "R\u00e9my Martin":     (8, -8),
        "Fortaleza":            (8, 6),
        "Grey Goose":           (-70, -4),
        "Hendrick's":           (8, 6),
        "Del Maguey":           (8, -8),
        "Nikka":                (8, 6),
        "Monkey 47":            (-70, -8),
        "Jack Daniel's":        (8, -8),
        "Clase Azul":           (8, 8),
        "Lagavulin":            (8, 6),
        "Redbreast":            (-65, 6),
        "Mezcal Vago":          (8, -8),
        "St. George Spirits":   (8, 6),     # to the right
        "Bacardi":              (8, -8),
        "Johnnie Walker":       (8, 6),
        "Jameson":              (8, 6),
    }

    for b in active:
        x = b["recall_rate"]
        y = b["mean_slot_position"]
        name = b["brand_name"]
        dx, dy = LABEL_OFFSETS.get(name, (8, 0))
        ax.annotate(name, (x, y),
                    xytext=(dx, dy), textcoords="offset points",
                    fontsize=7, color=BLACK,
                    arrowprops=dict(arrowstyle="-", color=GRAY,
                                   linewidth=0.3, shrinkA=3, shrinkB=1))

    ax.set_xlabel("Recall Rate (proportion of probes mentioning brand)",
                  fontsize=9, color=BLACK, labelpad=10)
    ax.set_ylabel("Mean Slot Position (1 = first mentioned)",
                  fontsize=9, color=BLACK, labelpad=10)

    # Padding
    x_pad = 0.025
    y_pad = 0.4
    ax.set_xlim(min(xs) - x_pad, max(xs) + 0.06)
    ax.set_ylim(max(ys) + y_pad, min(ys) - y_pad)  # inverted

    handles = [mpatches.Patch(color=c, label=r)
               for r, c in REGIME_COLORS.items() if r != "Absent"]
    ax.legend(handles=handles, loc="lower right", fontsize=7,
              frameon=True, framealpha=0.9)

    ax.text(0.02, 0.02, "Bubble size = elaboration count",
            transform=ax.transAxes, fontsize=7, color=GRAY)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    add_header(fig,
               "Recall Frequency vs Mean Slot Position",
               "Brands with zero recall excluded (n=%d plotted)" % len(active),
               "Patr\u00f3n leads on recall frequency; Lagavulin and Redbreast "
               "lead on slot position (always first when mentioned).")
    add_source(fig)

    out = FIGS_DIR / "chart_23_recall_scatter.pdf"
    fig.savefig(out, bbox_inches="tight", dpi=300)
    plt.close(fig)
    print(f"  \u2713 {out.name}")
    return out


# =========================================================================
# Main
# =========================================================================
def main():
    FIGS_DIR.mkdir(parents=True, exist_ok=True)
    verdicts = load_verdicts()

    print("=" * 60)
    print("AIAS v0.23 \u2014 Chart Builder (Premium Spirits)")
    print("=" * 60)

    chart_composite_bar(verdicts)
    chart_channel_heatmap(verdicts)
    chart_conglomerate_box(verdicts)
    chart_recall_scatter(verdicts)

    print(f"\n\u2713 All charts written to {FIGS_DIR}")


if __name__ == "__main__":
    main()
