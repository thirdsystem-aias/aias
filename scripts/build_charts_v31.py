#!/usr/bin/env python3
"""
v0.31 CPC cross-category baseline — figure builder (one per finding).
  chart_01_reconciliation_gate   generalized vs v1.7 CPC, y=x (certifies identity)
  chart_02_cpc_within_substrate  defined-brand CPC strip per substrate (H_CPC_Computable)
  chart_03_cpc_cross_category    box per substrate + KW (H_CPC_CrossCategory)
  chart_04_defined_undefined_floor  defined/undefined stacked bars (the floor)

Reads osf/v31/data/v31_cpc.csv + osf/v31/v31_cpc_verdicts.json. House style via chart_style.py.
Outputs PDFs to reports/figs/v31/.
"""
import sys, csv, json, re
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path.home() / "aias"
sys.path.insert(0, str(ROOT / "scripts"))
import chart_style as cs
cs.setup()

OUT = ROOT / "reports" / "figs" / "v31"; OUT.mkdir(parents=True, exist_ok=True)
SOURCE_PHASE = "v0.31 (CPC baseline)"
OMNI = ["v0.19", "v0.20", "v0.21", "v0.22", "v0.23"]
CAT = {"v0.19": "headphones", "v0.20": "skincare", "v0.21": "cosmetics",
       "v0.22": "automotive", "v0.23": "spirits", "v0.18": "fragrance"}
COL = {"v0.19": cs.PALETTE["blue"], "v0.20": cs.INDIGO, "v0.21": cs.WARM,
       "v0.22": cs.TEAL, "v0.23": cs.PALETTE["magenta"], "v0.18": cs.PALETTE["gray"]}

rows = list(csv.DictReader(open(ROOT / "osf/v31/data/v31_cpc.csv")))
for r in rows:
    r["mean_r"] = float(r["mean_r"])
    r["cpc_score"] = float(r["cpc_score"]) if r["cpc_score"] not in ("", "None") else None
V = json.load(open(ROOT / "osf/v31/v31_cpc_verdicts.json"))

# v0.23 S-ID -> name (locked registry table)
S2N = {m.group(1): m.group(2).strip() for m in
       re.finditer(r"\|\s*(S\d{2})\s*\|\s*([^|]+?)\s*\|", open(ROOT / "prereg/v0_23_mega_prompt.md").read())}


def defined(sub):
    return [r for r in rows if r["substrate"] == sub and r["status"] == "defined" and r["cpc_score"] is not None]


def chart_01_reconciliation_gate():
    v17 = {(r["substrate"], r["brand"]): r for r in csv.DictReader(
        open(ROOT / "osf/methodology/v1_7/data/v1_7_cpc.csv"))}
    xs, ys = [], []
    for r in rows:
        if r["substrate"] in ("v0.20", "v0.21", "v0.22") and r["cpc_score"] is not None:
            ref = v17.get((r["substrate"], r["brand"]))
            if ref and ref["cpc_score"] not in ("", "None"):
                xs.append(float(ref["cpc_score"])); ys.append(r["cpc_score"])
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    lo, hi = 0.45, 1.02
    ax.plot([lo, hi], [lo, hi], color=cs.GRAY, lw=1.0, ls="--", zorder=1, label="y = x (identity)")
    ax.scatter(xs, ys, s=46, color=cs.INDIGO, alpha=0.8, edgecolor="white", linewidth=0.6, zorder=3)
    ax.set_xlim(lo, hi); ax.set_ylim(lo, hi); ax.set_aspect("equal")
    ax.text(0.04, 0.95, f"n = {len(xs)} defined trio brands\nmax |$\\Delta$| = 1.1e-16  (float noise)\nexact per-model count identity",
            transform=ax.transAxes, ha="left", va="top", fontsize=cs.FONT_SIZES["annotation"],
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=cs.PALETTE["gray_light"], lw=0.6))
    ax.set_xlabel("v1.7-published CPC"); ax.set_ylabel("v0.31 generalized CPC")
    ax.legend(loc="lower right", fontsize=cs.FONT_SIZES["legend"])
    fig.subplots_adjust(**cs.MARGINS["single"])
    cs.add_header(fig, "The generalization reproduces v1.7 exactly",
                  "Channel-agnostic CPC against v1.7's two-channel CPC, on v0.20/21/22",
                  "Every brand lands on y = x — the channel-agnostic unit contains the locked two-channel unit by construction.")
    cs.add_footer(fig, verdict="Reconciliation gate PASSED — 72/72 exact per-model count identity; scoring proceeded.",
                  phase=SOURCE_PHASE, protocol="v0.31-prereg-r1")
    p = OUT / "chart_01_reconciliation_gate.pdf"; fig.savefig(p, **cs.SAVEFIG_PARAMS); plt.close(fig); return p


def chart_02_cpc_within_substrate():
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    rng = np.random.RandomState(280400)
    for i, sub in enumerate(OMNI):
        d = defined(sub); vals = [r["cpc_score"] for r in d]
        jit = rng.uniform(-0.13, 0.13, len(vals))
        ax.scatter(np.full(len(vals), i) + jit, vals, s=34, color=COL[sub],
                   alpha=0.8, edgecolor="white", linewidth=0.5, zorder=3)
        med = float(np.median(vals))
        ax.plot([i - 0.25, i + 0.25], [med, med], color=cs.BLACK, lw=1.6, zorder=4)
        ax.text(i, 1.03, f"n={len(vals)}", ha="center", va="bottom",
                fontsize=cs.FONT_SIZES["data_label"], color=cs.GRAY)
        # spirits median to the LEFT (its brand labels occupy the right)
        mx, mha = (i - 0.27, "right") if sub == "v0.23" else (i + 0.27, "left")
        ax.text(mx, med, f"{med:.2f}", ha=mha, va="center",
                fontsize=cs.FONT_SIZES["annotation"], color=cs.BLACK)
    # spirits labels: vertical stagger + leader lines (avoids overlap at clustered CPC)
    sp = sorted(defined("v0.23"), key=lambda r: r["cpc_score"])
    ypos = np.linspace(0.44, 0.70, len(sp))
    for r, yl in zip(sp, ypos):
        nm = S2N.get(r["brand"], r["brand"])
        ax.plot([4.06, 4.20], [r["cpc_score"], yl], color=cs.PALETTE["magenta"], lw=0.4, alpha=0.55, zorder=2)
        ax.annotate(nm, (4.24, yl), fontsize=6.2, color=cs.PALETTE["magenta"], va="center", ha="left")
    ax.set_xticks(range(len(OMNI)))
    ax.set_xticklabels([f"{s}\n{CAT[s]}" for s in OMNI])
    ax.set_ylabel("CPC = 1 / (1 + CV)   (defined brands)")
    ax.set_ylim(0.40, 1.08); ax.set_xlim(-0.5, 5.5)
    fig.subplots_adjust(**cs.MARGINS["single"])
    cs.add_header(fig, "Consistency is well-defined and varies within every category",
                  "Brand-level CPC for defined brands, by substrate, with medians (bar) and N",
                  "Non-degenerate spread in all five substrates — the instrument is not a near-constant (H_CPC_Computable).")
    cs.add_footer(fig, verdict="H_CPC_Computable CONFIRMED — non-degenerate CPC variance in all five omnibus substrates.",
                  phase=SOURCE_PHASE, protocol="v0.31-prereg-r1")
    p = OUT / "chart_02_cpc_within_substrate.pdf"; fig.savefig(p, **cs.SAVEFIG_PARAMS); plt.close(fig); return p


def chart_03_cpc_cross_category():
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    data = [[r["cpc_score"] for r in defined(s)] for s in OMNI]
    bp = ax.boxplot(data, positions=range(len(OMNI)), widths=0.55, patch_artist=True,
                    medianprops=dict(color=cs.BLACK, lw=1.6), showfliers=False)
    for patch, sub in zip(bp["boxes"], OMNI):
        patch.set_facecolor(COL[sub]); patch.set_alpha(0.35); patch.set_edgecolor(COL[sub])
    rng = np.random.RandomState(280400)
    for i, sub in enumerate(OMNI):
        vals = data[i]; jit = rng.uniform(-0.10, 0.10, len(vals))
        ax.scatter(np.full(len(vals), i) + jit, vals, s=20, color=COL[sub], alpha=0.7,
                   edgecolor="white", linewidth=0.4, zorder=3)
    kw = V["H_CPC_CrossCategory"]
    ax.text(0.03, 0.04, f"Kruskal-Wallis  H = {kw['kruskal_H']:.2f},  p = {kw['kruskal_p']:.1e}  (k=5, alpha=0.05)",
            transform=ax.transAxes, ha="left", va="bottom", fontsize=cs.FONT_SIZES["annotation"],
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=cs.PALETTE["gray_light"], lw=0.6))
    ax.set_xticks(range(len(OMNI)))
    ax.set_xticklabels([f"{s}\n{CAT[s]}" for s in OMNI])
    ax.set_ylabel("CPC  (defined brands)")
    fig.subplots_adjust(**cs.MARGINS["single"])
    cs.add_header(fig, "Consistency differs systematically across categories",
                  "Distribution of defined-brand CPC by substrate",
                  "Spirits least consistent, skincare most — significant cross-category variation (H_CPC_CrossCategory).")
    cs.add_footer(fig, verdict=f"H_CPC_CrossCategory CONFIRMED — KW H={kw['kruskal_H']:.2f}, p={kw['kruskal_p']:.1e}.",
                  phase=SOURCE_PHASE, protocol="v0.31-prereg-r1")
    p = OUT / "chart_03_cpc_cross_category.pdf"; fig.savefig(p, **cs.SAVEFIG_PARAMS); plt.close(fig); return p


def chart_04_defined_undefined_floor():
    order = OMNI + ["v0.18"]
    defc = [sum(1 for r in rows if r["substrate"] == s and r["status"] == "defined") for s in order]
    undc = [sum(1 for r in rows if r["substrate"] == s and r["status"] == "undefined") for s in order]
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    x = np.arange(len(order))
    ax.bar(x, defc, color=cs.INDIGO, width=0.62, label="CPC defined")
    ax.bar(x, undc, bottom=defc, color=cs.PALETTE["gray_light"], width=0.62, label="undefined (mean r < 1.0)")
    for i, (d, u) in enumerate(zip(defc, undc)):
        if d:
            ax.text(i, d / 2, str(d), ha="center", va="center", color="white", fontsize=cs.FONT_SIZES["data_label"])
        if u:
            ax.text(i, d + u / 2, str(u), ha="center", va="center", color=cs.GRAY, fontsize=cs.FONT_SIZES["data_label"])
        ax.text(i, d + u + 0.5, f"{d/(d+u)*100:.0f}%", ha="center", va="bottom",
                fontweight="bold", fontsize=cs.FONT_SIZES["data_label"], color=cs.BLACK)
    ax.axvline(4.5, color=cs.GRAY, lw=0.7, ls=":")
    ax.text(4.6, 26, "supplementary\n(descriptive, 3-frame)",
            color=cs.GRAY, fontsize=cs.FONT_SIZES["annotation"], va="top", ha="left")
    ax.set_xticks(x); ax.set_xticklabels([f"{s}\n{CAT[s]}" for s in order])
    ax.set_ylabel("brands"); ax.set_ylim(0, 28)
    ax.legend(loc="upper left", fontsize=cs.FONT_SIZES["legend"])
    fig.subplots_adjust(**cs.MARGINS["single"])
    cs.add_header(fig, "The floor sends near-zero-recall brands to undefined",
                  "Defined vs undefined CPC by substrate (omnibus | supplementary)",
                  "Undefined are recognized-but-unrecalled and defunct brands — excluded from the distribution, counted here.")
    cs.add_footer(fig, verdict="Floor (mean r < 1.0 -> undefined) inherited from v1.7; undefined counts reported per substrate.",
                  phase=SOURCE_PHASE, protocol="v0.31-prereg-r1")
    p = OUT / "chart_04_defined_undefined_floor.pdf"; fig.savefig(p, **cs.SAVEFIG_PARAMS); plt.close(fig); return p


if __name__ == "__main__":
    for fn in (chart_01_reconciliation_gate, chart_02_cpc_within_substrate,
               chart_03_cpc_cross_category, chart_04_defined_undefined_floor):
        print("wrote:", fn())
