"""
AIAS v0.26 — B2B SaaS Chart Builder
Uses chart_style.py for all layout, color, and positioning decisions.

Usage:
    cd /Users/pablou/aias
    python3 scripts/build_charts_v26.py
"""
import sys
from pathlib import Path

# Allow import of chart_style from scripts/
sys.path.insert(0, str(Path(__file__).resolve().parent))
import chart_style as cs

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

cs.setup()

PIPELINE_ROOT = Path(__file__).resolve().parent.parent
FIGS_DIR = PIPELINE_ROOT / "reports" / "figs" / "v26"
FIGS_DIR.mkdir(parents=True, exist_ok=True)

PHASE = "v0.26 \u2014 B2B SaaS"
COLORS = cs.cell_colors()
INDIGO, WARM = cs.diverging_pair()

CELL_LABELS = {
    "A": "Cell A: Enterprise Incumbents",
    "B": "Cell B: High-Identity Challengers",
    "C": "Cell C: Infrastructure / Dev Platform",
    "D": "Cell D: Phantom (defunct)",
}

RECALL_DATA = [
    ("Slack","B",33,30), ("Salesforce","A",36,25), ("HubSpot","A",33,21),
    ("Workday","A",34,7), ("SAP","A",25,8), ("Oracle","A",26,8),
    ("Notion","B",2,27), ("ServiceNow","A",17,8), ("Figma","B",1,23),
    ("Snowflake","C",10,13), ("Zendesk","A",18,4), ("Datadog","C",7,8),
    ("Linear","B",0,12), ("Stripe","C",4,6), ("Airtable","B",0,10),
    ("Miro","B",0,8), ("MongoDB","C",1,4), ("Twilio","C",2,2),
    ("Cloudflare","C",0,3), ("Quip","D",0,0), ("Yammer","D",0,0),
    ("Wunderlist","D",0,0), ("HipChat","D",0,0), ("Stride","D",0,0),
]


# ── Chart 1: Recall by Brand ──────────────────────────────────────────

def build_chart_recall():
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero_tall"])
    fig.subplots_adjust(top=0.82, bottom=0.10, left=0.17, right=0.92)

    n = len(RECALL_DATA)
    brands = [d[0] for d in RECALL_DATA][::-1]
    cells  = [d[1] for d in RECALL_DATA][::-1]
    r_cats = [d[2] for d in RECALL_DATA][::-1]
    r_cults= [d[3] for d in RECALL_DATA][::-1]
    y_pos  = np.arange(n)
    bh = 0.35

    ax.barh(y_pos + bh/2, r_cats, bh, color=INDIGO,
            label="R_cat (category)", edgecolor="none", zorder=3)
    ax.barh(y_pos - bh/2, r_cults, bh, color=cs.PALETTE["indigo_t3"],
            label="R_cult (cultural)", edgecolor="none", zorder=3)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(brands, fontsize=cs.FONT_SIZES["axis_tick"])
    for i, (lbl, cell) in enumerate(zip(ax.get_yticklabels(), cells)):
        lbl.set_color(COLORS.get(cell, cs.BLACK))

    ax.set_xlim(0, 38)
    ax.set_xlabel("Mentions (out of 36 per channel)",
                  fontsize=cs.FONT_SIZES["axis_label"], color=cs.BLACK, labelpad=8)
    ax.legend(loc="lower right", fontsize=cs.FONT_SIZES["legend"])

    # Cell legend — inside axes, bottom-left
    handles = [mpatches.Patch(color=COLORS[c], label=CELL_LABELS[c])
               for c in ["A","B","C","D"]]
    ax.legend(handles=handles, loc="lower left", fontsize=7,
              frameon=True, framealpha=0.9, ncol=1)

    cs.add_header(fig,
        "Recall by Brand",
        "R_cat (category) and R_cult (cultural) mentions across 36 outputs per channel",
        "Sorted by total recall descending. Slack and Salesforce dominate; "
        "Cell D phantom brands show zero recall.")
    cs.add_footer(fig, phase=PHASE)

    # Bar legend (R_cat vs R_cult) — upper right
    cat_patch = mpatches.Patch(color=INDIGO, label="R_cat (category)")
    cult_patch = mpatches.Patch(color=cs.PALETTE["indigo_t3"], label="R_cult (cultural)")
    fig.legend(handles=[cat_patch, cult_patch], loc="upper right",
               bbox_to_anchor=(0.92, 0.82), fontsize=7, frameon=True, framealpha=0.9)

    out = FIGS_DIR / "chart_24_recall_by_brand.pdf"
    fig.savefig(out, **cs.SAVEFIG_PARAMS)
    plt.close(fig)
    print(f"  \u2713 {out.name}")


# ── Chart 2: MLT Frequency ────────────────────────────────────────────

def build_chart_mlt():
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    fig.subplots_adjust(top=0.82, bottom=0.18, left=0.38, right=0.92)

    tokens = [
        ("HubSpot: inbound marketing", 21), ("ServiceNow: workflow automation", 15),
        ("Airtable: no-code", 10), ("Salesforce: Trailblazer", 9),
        ("Notion: all-in-one workspace", 8), ("Salesforce: Einstein", 5),
        ("Snowflake: Data Cloud", 4), ("Salesforce: Customer 360", 1),
        ("Salesforce: Ohana", 1), ("ServiceNow: Now Platform", 1),
    ]
    labels = [t[0] for t in tokens][::-1]
    counts = [t[1] for t in tokens][::-1]
    y_pos = np.arange(len(labels))

    ax.barh(y_pos, counts, color=INDIGO, height=0.6, edgecolor="none", zorder=3)

    for y, c in zip(y_pos, counts):
        ax.text(c + 0.4, y, str(c), va="center",
                fontsize=cs.FONT_SIZES["data_label"], color=INDIGO)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=cs.FONT_SIZES["axis_tick"])
    ax.set_xlim(0, 25)
    ax.set_xlabel("Appearances in Phase B outputs",
                  fontsize=cs.FONT_SIZES["axis_label"], color=cs.BLACK, labelpad=8)

    cs.add_header(fig,
        "Marketing-Language Tokens in AI Recall Outputs",
        "Frequency of pre-registered vendor-coined terms across 72 Phase B outputs",
        '"Inbound marketing" fully category-absorbed; '
        '"Trailblazer" retains Salesforce brand linkage.')
    cs.add_footer(fig,
        verdict="MLC = 55.6% \u2014 PARTIAL: strong absolute signal; "
                "cross-substrate baseline pending.",
        phase=PHASE)

    out = FIGS_DIR / "chart_24_mlt_frequency.pdf"
    fig.savefig(out, **cs.SAVEFIG_PARAMS)
    plt.close(fig)
    print(f"  \u2713 {out.name}")


# ── Chart 3: Identity Load ────────────────────────────────────────────

def build_chart_identity_load():
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    fig.subplots_adjust(top=0.82, bottom=0.18, left=0.22, right=0.82)

    cells_data = [
        ("Cell C  (Infrastructure)", 4.0, 6.0),
        ("Cell B  (Challengers)",    6.0, 18.3),
        ("Cell A  (Enterprise)",     27.0, 11.6),
    ]
    y_pos = np.arange(len(cells_data))
    bh = 0.45

    for i, (label, r_cat, r_cult) in enumerate(cells_data):
        ax.barh(i, -r_cat, bh, color=INDIGO, edgecolor="none", zorder=3)
        ax.barh(i, r_cult, bh, color=WARM, edgecolor="none", zorder=3)
        ax.text(-r_cat - 0.8, i, f"{r_cat:.0f}", va="center", ha="right",
                fontsize=cs.FONT_SIZES["data_label"], color=INDIGO, fontweight="bold")
        ax.text(r_cult + 0.8, i, f"{r_cult:.0f}", va="center", ha="left",
                fontsize=cs.FONT_SIZES["data_label"], color=WARM, fontweight="bold")
        cult_lead = r_cult - r_cat
        sign = "+" if cult_lead >= 0 else ""
        ax.text(26, i, f"cult-lead: {sign}{cult_lead:.1f}",
                va="center", fontsize=cs.FONT_SIZES["annotation"], color=cs.BLACK)

    ax.set_yticks(y_pos)
    ax.set_yticklabels([d[0] for d in cells_data],
                       fontsize=cs.FONT_SIZES["axis_tick"])
    ax.axvline(0, color=cs.BLACK, linewidth=0.6, zorder=2)
    ax.set_xlim(-32, 32)
    ax.set_xlabel("Mean mentions per cell (out of 36 per channel)",
                  fontsize=cs.FONT_SIZES["axis_label"], color=cs.BLACK, labelpad=8)

    # Channel direction labels — figure-level, between description and axes
    fig.text(0.35, 0.795, "\u2190 R_cat (category)", ha="center",
             fontsize=cs.FONT_SIZES["annotation"], color=INDIGO, fontweight="bold")
    fig.text(0.65, 0.795, "R_cult (cultural) \u2192", ha="center",
             fontsize=cs.FONT_SIZES["annotation"], color=WARM, fontweight="bold")

    cs.add_header(fig,
        "Identity Load: Category vs Cultural Recall by Cell",
        "Mean R_cat and R_cult per cell (main cells only)",
        "27.7-point separation between Cell A and Cell B \u2014 "
        "strongest Identity Load signal in the program.")
    cs.add_footer(fig,
        verdict="H_IL_direct CONFIRMED \u2014 Cell B cult-lead (+12.3) "
                "vs Cell A (\u221215.4).",
        phase=PHASE)

    out = FIGS_DIR / "chart_24_identity_load.pdf"
    fig.savefig(out, **cs.SAVEFIG_PARAMS)
    plt.close(fig)
    print(f"  \u2713 {out.name}")


# ── Chart 4: MLC by Model ─────────────────────────────────────────────

def build_chart_mlc_by_model():
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    fig.subplots_adjust(top=0.82, bottom=0.18, left=0.26, right=0.92)

    models_data = [
        ("Claude Sonnet 4.6", 3, 12), ("GPT-4o", 4, 12),
        ("Claude Opus 4.7", 5, 12), ("GPT-4o-mini", 8, 12),
        ("Gemini 2.5 Flash Lite", 10, 12), ("Gemini 2.5 Flash", 10, 12),
    ]
    y_pos = np.arange(len(models_data))
    rates = [d[1]/d[2] for d in models_data]

    ax.barh(y_pos, rates, color=INDIGO, height=0.55, edgecolor="none", zorder=3)
    ax.axvline(0.556, color=WARM, linewidth=1.2, linestyle="--",
               zorder=4, label="Overall MLC (55.6%)")

    for i, (name, hits, total) in enumerate(models_data):
        rate = hits/total
        ax.text(rate + 0.015, i, f"{rate:.0%}  ({hits}/{total})",
                va="center", fontsize=cs.FONT_SIZES["data_label"], color=INDIGO)

    ax.set_yticks(y_pos)
    ax.set_yticklabels([d[0] for d in models_data],
                       fontsize=cs.FONT_SIZES["axis_tick"])
    ax.set_xlim(0, 1.05)
    ax.set_xlabel("MLC rate", fontsize=cs.FONT_SIZES["axis_label"],
                  color=cs.BLACK, labelpad=8)
    ax.legend(loc="lower right", fontsize=cs.FONT_SIZES["legend"])

    cs.add_header(fig,
        "Marketing-Language Coverage by Model",
        "Proportion of 12 outputs per model containing \u22651 MLT",
        "Gemini models carry the most vendor-coined language; "
        "Claude Sonnet carries the least.")
    cs.add_footer(fig,
        verdict="Permeability varies 3.3\u00d7 across models.",
        phase=PHASE)

    out = FIGS_DIR / "chart_24_mlc_by_model.pdf"
    fig.savefig(out, **cs.SAVEFIG_PARAMS)
    plt.close(fig)
    print(f"  \u2713 {out.name}")


# ── Chart 5: Phantom Recognition–Recall Gap ──────────────────────────

def build_chart_phantom():
    phantoms = [d for d in RECALL_DATA if d[1] == "D"]
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    fig.subplots_adjust(top=0.82, bottom=0.18, left=0.22, right=0.92)

    brands = [d[0] for d in phantoms]
    n = len(brands)
    y_pos = np.arange(n)
    bh = 0.35

    recognition = [6] * n
    recall_total = [d[2] + d[3] for d in phantoms]

    ax.barh(y_pos + bh/2, recognition, bh, color=INDIGO,
            label="Recognition (C_P out of 6)", edgecolor="none", zorder=3)
    ax.barh(y_pos - bh/2, recall_total, bh, color=cs.PALETTE["gray_light"],
            label="Total recall mentions (out of 72)", edgecolor="none", zorder=3)

    for i in range(n):
        ax.text(recognition[i] + 0.3, y_pos[i] + bh/2, "6/6",
                va="center", fontsize=cs.FONT_SIZES["data_label"],
                color=INDIGO, fontweight="bold")
        ax.text(0.3, y_pos[i] - bh/2, "0",
                va="center", fontsize=cs.FONT_SIZES["data_label"],
                color=cs.PALETTE["gray"])

    ax.set_yticks(y_pos)
    ax.set_yticklabels(brands, fontsize=cs.FONT_SIZES["axis_tick"])
    ax.set_xlim(0, 10)
    ax.set_xlabel("Score", fontsize=cs.FONT_SIZES["axis_label"],
                  color=cs.BLACK, labelpad=8)
    ax.legend(loc="lower right", fontsize=cs.FONT_SIZES["legend"])

    cs.add_header(fig,
        "Phantom Brand Recognition–Recall Gap",
        "All 5 defunct brands are recognized at 6/6 but never recalled",
        "Models know these brands existed, describe their features and "
        "discontinuation dates, yet never recommend them.")
    cs.add_footer(fig,
        verdict="Recognition–recommendation gap: 100% known, 0% recommended.",
        phase=PHASE)

    out = FIGS_DIR / "chart_24_phantom_gap.pdf"
    fig.savefig(out, **cs.SAVEFIG_PARAMS)
    plt.close(fig)
    print(f"  ✓ {out.name}")


# ── Main ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("AIAS v0.26 \u2014 Chart Builder (B2B SaaS)")
    print("=" * 60)
    build_chart_recall()
    build_chart_mlt()
    build_chart_identity_load()
    build_chart_mlc_by_model()
    build_chart_phantom()
    print(f"\n\u2713 All charts \u2192 {FIGS_DIR}")
