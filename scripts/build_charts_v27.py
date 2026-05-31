#!/usr/bin/env python3
"""
build_charts_v27.py — figures for AIAS v0.27 (B2B SaaS convergent validity).

Outputs two vector PDFs for the SSRN paper (and later the brand-format report):
  Fig 1  v0_27_scatter_recall_sov.pdf  — recall-SOM x I1 Share-of-Voice (the primary null)
  Fig 2  v0_27_component_rho.pdf       — recall-SOM x each I1 dimension (exploratory)

Data-driven: reads the canonical CSVs and recomputes the same Spearman rhos the
paper reports, so the figures cannot drift from Table 2 / Table 3.

CC — VERIFY BEFORE FIRST RUN:
  * chart_style calls (setup, add_header, add_footer, FIGSIZE, PALETTE,
    SAVEFIG_PARAMS) assume build_charts_v0_26.py signatures. If any differ,
    reconcile against chart_style.py — the matplotlib plotting itself is
    self-contained and won't need changes.
  * CELL map below is a literal; reconcile against the registry SSOT (it should
    match, but the registry is the source of truth, not this file).
  * FIGDIRS = papers/v0_27/figs (SSRN paper) + reports/figs/v27 (brand-format
    report). The .md figure includes use a path relative to the paper source.
"""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import spearmanr, rankdata
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

import chart_style as cs   # ~/aias/scripts/chart_style.py

# --- paths --------------------------------------------------------------------
ROOT   = Path("/Users/pablou/aias")
DATA   = ROOT / "osf" / "v27" / "data"
# Two outputs: papers/ for the SSRN paper, reports/figs/v27/ for the Third System
# brand-format report (CLAUDE.md per-phase chart convention).
FIGDIRS = [
    ROOT / "papers" / "v0_27" / "figs",
    ROOT / "reports" / "figs" / "v27",
]
for _d in FIGDIRS:
    _d.mkdir(parents=True, exist_ok=True)


def savefig_all(fig, name):
    """Write the figure to every output dir at the locked savefig params."""
    for _d in FIGDIRS:
        fig.savefig(_d / name, **cs.SAVEFIG_PARAMS)

# --- brand tokens (cs.PALETTE; restated for readability) ----------------------
INDIGO = "#37237B"   # incumbent / live competitive
PETRO  = "#6A6AB1"   # mid / exploratory dimensions
COPPER = "#F36C35"   # challenger / the pre-registered metric + type-2 flag
GREY   = "#999999"
ANNOT  = 9           # match cs.FONT_SIZES if you prefer the house size

# --- brand metadata (CC: reconcile cells against the registry SSOT) -----------
CELL = {
    "Salesforce": "A", "HubSpot": "A", "ServiceNow": "A", "Workday": "A",
    "SAP": "A", "Oracle": "A", "Zendesk": "A",
    "Notion": "B", "Figma": "B", "Linear": "B", "Airtable": "B", "Slack": "B", "Miro": "B",
    "Datadog": "C", "Snowflake": "C", "Stripe": "C", "Twilio": "C", "Cloudflare": "C", "MongoDB": "C",
    "Quip": "D", "Yammer": "D", "Wunderlist": "D", "HipChat": "D", "Stride": "D",
}
TYPE2  = {"Linear", "Airtable", "Miro", "Cloudflare"}   # R_cat=0, R_cult>0
STRIDE = "Stride"                                       # name-collision confound (D5)

# --- load + merge -------------------------------------------------------------
aias = pd.read_csv(DATA / "v0.27_aias_side.csv")
i1   = pd.read_csv(DATA / "v0.27_I1_normalized.csv")
df = aias.merge(i1, on="brand_id", how="inner")
assert len(df) == 24, f"expected 24 covered brands, got {len(df)} (check the I1 remap)"
df["cell"] = df["brand_name"].str.strip().map(CELL)
assert df["cell"].notna().all(), "unmapped brand -> cell; reconcile CELL with registry"

x = df["recall_channel_som"].to_numpy(float)

# --- component rhos (reproduce Table 3) ---------------------------------------
DIMS = [
    ("I1_presence_quality",   "Presence Quality"),
    ("I1_brand_recognition",  "Brand Recognition"),
    ("I1_composite_100",      "Composite (/100)"),
    ("I1_market_competition", "Market Competition"),
    ("I1_sov",                "Share of Voice"),
    ("I1_sentiment",          "Sentiment"),
]
rows = [(label, spearmanr(x, df[col].to_numpy(float))[0]) for col, label in DIMS]
rows.sort(key=lambda r: r[1], reverse=True)   # descending rho

# ============================================================================
# Figure 2 — component-rho bar (exploratory; SoV is the pre-registered metric)
# ============================================================================
cs.setup()
fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])

labels = [r[0] for r in rows]
vals   = [r[1] for r in rows]
colors = [COPPER if lab == "Share of Voice" else PETRO for lab in labels]
ypos   = np.arange(len(rows))[::-1]           # top row = highest rho

ax.barh(ypos, vals, color=colors, height=0.62, zorder=3)
ax.set_yticks(ypos)
ax.set_yticklabels([f"{lab}  (pre-reg)" if lab == "Share of Voice" else lab for lab in labels])
for yp, v in zip(ypos, vals):
    ax.text(v + 0.012, yp, f"{v:+.2f}", va="center", ha="left", fontsize=ANNOT)

for xt, txt in [(0.60, "confirm 0.60"), (0.74, "strong 0.74")]:
    ax.axvline(xt, color=GREY, lw=1, ls="--", zorder=1)
    ax.text(xt + 0.006, 1.7, txt, rotation=90, va="bottom", ha="left", fontsize=ANNOT - 1, color="#888888")

ax.set_xlim(0, 0.9)
ax.set_ylim(-0.6, len(rows) - 0.4)
ax.set_xlabel("Spearman \u03c1 with AIAS recall-SOM")
ax.legend(handles=[
        Patch(facecolor=COPPER, label="Pre-registered convergent metric (falsified)"),
        Patch(facecolor=PETRO,  label="Exploratory dimensions"),
    ], loc="lower right", frameon=False, fontsize=ANNOT)

cs.add_header(
    fig,
    "Where AIAS recall-SOM meets the HubSpot Grader's dimensions",
    r"Spearman $\rho$ of recall-SOM with each Grader dimension (n = 24)",
    "Exploratory; the pre-registered metric is Share of Voice.",
)
cs.add_footer(
    fig,
    verdict="Presence-quality and brand-recognition exceed the 0.74 strong benchmark; SoV does not.",
    phase="v0.27",
)
fig.subplots_adjust(left=0.13, right=0.97, top=0.80, bottom=0.18)
savefig_all(fig, "v0_27_component_rho.pdf")
plt.close(fig)

# ============================================================================
# Figure 1 — recall-SOM x I1 Share-of-Voice scatter (the primary null)
# ============================================================================
cs.setup()
fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])

def style(row):
    nm = row.brand_name.strip()
    if nm == STRIDE:
        return "Stride (name confound)", dict(c=GREY, marker="X", s=95, edgecolors="#444444", linewidths=1.2)
    if nm in TYPE2:
        return "Type-2 (R_cat=0, salient)", dict(c=COPPER, marker="o", s=85, edgecolors="#7a3415", linewidths=1.2)
    if row.cell == "D":
        return "Phantom (defunct)", dict(c="#FFFFFF", marker="o", s=72, edgecolors=GREY, linewidths=1.2)
    return "Live competitive", dict(c=INDIGO, marker="o", s=62, edgecolors="white", linewidths=0.8)

# Jitter the coincident recall=0 cluster horizontally so its markers/labels
# separate; non-zero recall values are left exact.
np.random.seed(27)
df["x_plot"] = df["recall_channel_som"].astype(float)
_z = df["recall_channel_som"] == 0
df.loc[_z, "x_plot"] = np.random.uniform(-2.4, 2.4, int(_z.sum()))

seen = set()
for _, r in df.iterrows():
    lab, st = style(r)
    ax.scatter(r.x_plot, r.I1_sov, zorder=3,
               label=(lab if lab not in seen else None), **st)
    seen.add(lab)

SCATTER_LABELS = {"Salesforce": (-6, 6, "right"), "Figma": (5, 5, "left"),
                  "Linear": (7, 0, "left"), "Stride": (9, -1, "left")}
for _, r in df.iterrows():
    nm = r.brand_name.strip()
    if nm in SCATTER_LABELS:
        dx, dy, ha = SCATTER_LABELS[nm]
        ax.annotate(nm, (r.x_plot, r.I1_sov), xytext=(dx, dy),
                    textcoords="offset points", fontsize=ANNOT, ha=ha, color="#333333")

ax.set_xlim(-4, 104)
ax.set_ylim(-0.4, 9)
ax.set_xlabel("AIAS recall-SOM (category-leadership recall, 0\u2013100)")
ax.set_ylabel("HubSpot Grader Share-of-Voice (mean of 3 engines, 0\u201310)")
ax.legend(loc="center right", frameon=True, framealpha=0.92, edgecolor="none", fontsize=ANNOT)

cs.add_header(
    fig,
    "AIAS recall-SOM vs. brand-absolute AI Share-of-Voice",
    r"HubSpot AEO Grader Share-of-Voice, mean of 3 engines (n = 24)",
    r"Spearman $\rho$ = 0.29 (n.s.); much rank agreement is the live/defunct split.",
)
cs.add_footer(
    fig,
    verdict="Primary convergent test falsified \u2014 recall-SOM does not converge with brand-absolute Share-of-Voice.",
    phase="v0.27",
)
fig.subplots_adjust(left=0.13, right=0.97, top=0.80, bottom=0.18)
savefig_all(fig, "v0_27_scatter_recall_sov.pdf")
plt.close(fig)

# ============================================================================
# Figure 2 (Finding 2) — recognition ceiling vs recall-SOM spread
# ============================================================================
cs.setup()
fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])

cp_scaled = (df["C_P"].astype(float) / 6.0) * 100.0    # all 24 brands -> 100
som_vals  = df["recall_channel_som"].astype(float).to_numpy()
_rng = np.random.default_rng(27)
ax.scatter(cp_scaled, np.full(len(df), 1.0) + _rng.uniform(-0.15, 0.15, len(df)),
           s=62, c=GREY, edgecolors="white", linewidths=0.6, zorder=3)
ax.scatter(som_vals, np.full(len(df), 0.0) + _rng.uniform(-0.15, 0.15, len(df)),
           s=62, c=INDIGO, edgecolors="white", linewidths=0.6, zorder=3)

ax.set_yticks([0, 1])
ax.set_yticklabels(["Recall-SOM", "Recognition ($C_P$)"])
ax.set_ylim(-0.75, 1.75)
ax.set_xlim(-4, 104)
ax.set_xlabel("Score (0–100; recognition scaled from 0–6)")
ax.annotate("all 24 brands at the ceiling · sd = 0", (100, 1.20),
            ha="right", va="bottom", fontsize=ANNOT, color="#666666")
ax.annotate("spread 0–100 — the variance-bearing measure", (0, -0.45),
            ha="left", va="top", fontsize=ANNOT, color="#666666")

cs.add_header(
    fig,
    "Recognition is at the ceiling; recall carries the variance",
    r"AIAS recognition ($C_P$) vs. recall-SOM across 24 B2B SaaS brands",
    "Recognition is saturated at 6/6 for every brand; only recall-SOM separates them.",
)
cs.add_footer(
    fig,
    verdict="Recognition enters as a null control; recall-SOM is the variance-bearing convergent variable.",
    phase="v0.27",
)
fig.subplots_adjust(left=0.20, right=0.97, top=0.80, bottom=0.18)
savefig_all(fig, "v0_27_recognition_ceiling.pdf")
plt.close(fig)

# ============================================================================
# Figure 4 (Finding 4) — rank-alignment: whose ranking follows recall's
# Honest mechanism for the SoV null: it is rank-misaligned with recall (and
# tie-heavy), NOT range-restricted. Rank-rank plots make Spearman legible —
# presence quality hugs the agreement diagonal; Share of Voice scatters off it.
# ============================================================================
cs.setup()
fig, (axL, axR) = plt.subplots(1, 2, figsize=cs.FIGSIZE["spread"],
                               sharex=True, sharey=True)

xr = df["recall_channel_som"].astype(float).to_numpy()
pq = (df["I1_presence_quality"].astype(float).to_numpy() / 20.0) * 100.0
sv = (df["I1_sov"].astype(float).to_numpy() / 10.0) * 100.0
rx = rankdata(xr)
n  = len(df)

for ax_, yv, title, col in ((axL, pq, "Presence Quality", INDIGO),
                            (axR, sv, "Share of Voice", COPPER)):
    ry = rankdata(yv)
    rho = spearmanr(xr, yv)[0]
    ax_.plot([1, n], [1, n], color=GREY, lw=1.0, ls="--", zorder=1)   # perfect agreement
    ax_.scatter(rx, ry, s=42, c=col, edgecolors="white", linewidths=0.5, zorder=3)
    ax_.set_xlim(0, n + 1)
    ax_.set_ylim(0, n + 1)
    ax_.set_xlabel("AIAS recall-SOM rank")
    ax_.text(0.05, 0.95, f"{title}\n$\\rho$ = {rho:.2f}", transform=ax_.transAxes,
             ha="left", va="top", fontsize=ANNOT, color=col, fontweight="bold")
axL.set_ylabel("HubSpot dimension rank")

cs.add_header(
    fig,
    "Presence quality’s ranking follows recall’s; Share of Voice’s doesn’t",
    r"Rank–rank plots: AIAS recall-SOM rank vs. HubSpot dimension rank (n = 24)",
    "Dashed line = perfect rank agreement. Presence quality hugs it; Share of Voice "
    "scatters — its variation is real but rank-misaligned with recall.",
)
cs.add_footer(
    fig,
    verdict="The convergence gap is rank-alignment, not spread: Share of Voice varies as much, but its order does not match recall’s.",
    phase="v0.27",
)
fig.subplots_adjust(left=0.10, right=0.97, top=0.78, bottom=0.16, wspace=0.16)
savefig_all(fig, "v0_27_recall_tracking.pdf")
plt.close(fig)

print("wrote to", len(FIGDIRS), "dirs:")
for _d in FIGDIRS:
    for _f in ("v0_27_scatter_recall_sov.pdf", "v0_27_recognition_ceiling.pdf",
               "v0_27_component_rho.pdf", "v0_27_recall_tracking.pdf"):
        print("  ", _d / _f)
print("component rhos:", [(lab, round(v, 3)) for lab, v in rows])
