#!/usr/bin/env python3
"""
v1.7 CPC — figure builder (one per finding).
Honest depiction of the r3-recorded outcomes:
  fig_01_cpc_defined      H_CPC_Defined      FALSIFIED (pooled defined-rate 57%)
  fig_02_cpc_dissociation H_CPC_Dissociates  FALSIFIED (|rho|=0.77 > 0.50)
  fig_03_phantom_null     H_CPC_PhantomNull   CONFIRMED (all 5 Cell-D -> N/A)
  fig_04_cv_mean_coupling Finding 2 mechanism CV ~ 1/sqrt(mean) at low counts

Reads osf/methodology/v1_7/data/v1_7_cpc.csv. House style via chart_style.py.
Outputs PDFs to reports/figs/v1_7/.
"""
import sys, csv, json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path.home() / "aias"
sys.path.insert(0, str(ROOT / "scripts"))
import chart_style as cs
cs.setup()

OUT = ROOT / "reports" / "figs" / "v1_7"; OUT.mkdir(parents=True, exist_ok=True)
SUB_NAME = {"v0.20": "skincare", "v0.21": "cosmetics", "v0.22": "automotive"}
SUB_COLOR = {"v0.20": cs.INDIGO, "v0.21": cs.WARM, "v0.22": cs.TEAL}
SOURCE_PHASE = "v1.7 (CPC.r3)"

rows = list(csv.DictReader(open(ROOT / "osf/methodology/v1_7/data/v1_7_cpc.csv")))
for r in rows:
    r["mean_r"] = float(r["mean_r"])
    r["in_market"] = (r["in_market"] == "True")
    r["is_phantom"] = (r["is_phantom"] == "True")
    r["cpc_score"] = float(r["cpc_score"]) if r["cpc_score"] not in ("", "None") else None
    r["cpc_raw"] = float(r["cpc_raw"]) if r["cpc_raw"] not in ("", "None") else None
    r["presence_composite"] = float(r["presence_composite"])


def fig_01_cpc_defined():
    """Stacked defined / N-A counts per substrate + pooled."""
    subs = ["v0.20", "v0.21", "v0.22"]
    defined = [sum(1 for r in rows if r["substrate"] == s and r["in_market"] and r["cpc_score"] is not None) for s in subs]
    na = [sum(1 for r in rows if r["substrate"] == s and r["in_market"] and r["cpc_score"] is None) for s in subs]
    labels = [SUB_NAME[s] for s in subs] + ["pooled"]
    defined.append(sum(defined)); na.append(sum(na))
    rates = [d / (d + n) * 100 if (d + n) else 0 for d, n in zip(defined, na)]

    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    x = np.arange(len(labels))
    ax.bar(x, defined, color=cs.INDIGO, label="CPC defined", width=0.62)
    ax.bar(x, na, bottom=defined, color=cs.PALETTE["gray_light"], label="N/A (mean r < 1.0)", width=0.62)
    for i, (d, n, rt) in enumerate(zip(defined, na, rates)):
        ax.text(i, d + n + 0.6, f"{rt:.0f}%", ha="center", va="bottom",
                fontsize=cs.FONT_SIZES["data_label"], fontweight="bold", color=cs.BLACK)
        ax.text(i, d / 2, f"{d}", ha="center", va="center", color="white",
                fontsize=cs.FONT_SIZES["data_label"])
        if n:
            ax.text(i, d + n / 2, f"{n}", ha="center", va="center", color=cs.GRAY,
                    fontsize=cs.FONT_SIZES["data_label"])
    ax.axvline(2.5, color=cs.GRAY, lw=0.5, ls=":")
    ax.set_xticks(x); ax.set_xticklabels(labels)
    ax.set_ylabel("in-market brands")
    ax.set_ylim(0, max(d + n for d, n in zip(defined, na)) + 5)
    ax.legend(loc="upper left", fontsize=cs.FONT_SIZES["legend"])
    fig.subplots_adjust(**cs.MARGINS["single"])
    cs.add_header(fig, "Many in-market brands have no defined CPC",
                  "Defined vs N/A under the locked floor (mean combined recall r >= 1.0)",
                  "The N/A brands are recognized but rarely recalled (e.g. Lancôme, Chanel, Dior at C_P=6, ~0 recall).")
    cs.add_footer(fig, verdict="H_CPC_Defined FALSIFIED — pooled defined-rate 57% (43% of in-market brands N/A).",
                  phase=SOURCE_PHASE, protocol="v1.7-prereg-r2")
    p = OUT / "fig_01_cpc_defined.pdf"; fig.savefig(p, **cs.SAVEFIG_PARAMS); plt.close(fig)
    return p


def fig_02_cpc_dissociation():
    """CPC x Presence scatter; median-split quadrants; rho annotated."""
    pts = [r for r in rows if r["in_market"] and r["cpc_score"] is not None]
    xs = np.array([r["presence_composite"] for r in pts])
    ys = np.array([r["cpc_score"] for r in pts])
    xmed, ymed = float(np.median(xs)), float(np.median(ys))

    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    for s in ["v0.20", "v0.21", "v0.22"]:
        sx = [r["presence_composite"] for r in pts if r["substrate"] == s]
        sy = [r["cpc_score"] for r in pts if r["substrate"] == s]
        ax.scatter(sx, sy, s=42, color=SUB_COLOR[s], alpha=0.85, edgecolor="white",
                   linewidth=0.6, label=SUB_NAME[s], zorder=3)
    ax.axvline(xmed, color=cs.GRAY, lw=0.6, ls="--", zorder=1)
    ax.axhline(ymed, color=cs.GRAY, lw=0.6, ls="--", zorder=1)
    # trend (visualizes the non-dissociation)
    xs_sorted = np.linspace(xs.min(), xs.max(), 50)
    b, a = np.polyfit(xs, ys, 1)
    ax.plot(xs_sorted, a + b * xs_sorted, color=cs.BLACK, lw=1.0, ls="-", alpha=0.5, zorder=2)
    ax.text(0.97, 0.06,
            "pooled $\\rho$ = 0.766  (95% BCa [0.60, 0.89], n=38)\n"
            "skincare +0.94 · cosmetics +0.85 · automotive +0.64\n"
            "ceiling for dissociation: |$\\rho$| < 0.50",
            transform=ax.transAxes, ha="right", va="bottom",
            fontsize=cs.FONT_SIZES["annotation"],
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=cs.PALETTE["gray_light"], lw=0.6))
    ax.set_xlabel("Presence (composite: C_P, R_cat, R_cult)")
    ax.set_ylabel("CPC = 1 / (1 + CV)")
    ax.legend(loc="upper left", fontsize=cs.FONT_SIZES["legend"])
    fig.subplots_adjust(**cs.MARGINS["single"])
    cs.add_header(fig, "CPC tracks Presence — it does not dissociate",
                  "Consistency rises monotonically with presence level across all three substrates",
                  "At recall counts r ∈ 0–6, CV ≈ 1/√mean, so CV-based consistency reparametrizes level.")
    cs.add_footer(fig, verdict="H_CPC_Dissociates FALSIFIED — |ρ| = 0.77 >= 0.50 ceiling; redefinition escalated to v1.8.",
                  phase=SOURCE_PHASE, protocol="v1.7-prereg-r2")
    p = OUT / "fig_02_cpc_dissociation.pdf"; fig.savefig(p, **cs.SAVEFIG_PARAMS); plt.close(fig)
    return p


def fig_03_phantom_null():
    """Cell-D defunct brands: recall = 0 -> N/A, vs in-market reference band."""
    ph = [r for r in rows if r["is_phantom"]]
    inm = [r for r in rows if r["in_market"] and r["substrate"] == "v0.22"]
    inm_means = [r["mean_r"] for r in inm]
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    names = [r["brand"] for r in ph]
    vals = [r["mean_r"] for r in ph]
    REF_Y = len(names) + 0.4          # dedicated reference row below the phantoms
    y = np.arange(len(names))
    ax.barh(y, vals, color=cs.PALETTE["gray_light"], height=0.6, zorder=3)
    # floor marker + label at the TOP, clear of the reference row
    ax.axvline(1.0, color=cs.WARM, lw=1.2, ls="--", zorder=2)
    ax.text(1.06, -0.7, "floor: mean r = 1.0", color=cs.WARM,
            fontsize=cs.FONT_SIZES["annotation"], va="center", ha="left")
    for i, v in enumerate(vals):
        ax.text(0.05, i, "N/A  (mean r = 0)", va="center", ha="left", color=cs.BLACK,
                fontsize=cs.FONT_SIZES["data_label"], fontweight="bold")
    # reference band: in-market (v0.22) mean recall, on its own labelled row
    ax.scatter(inm_means, np.full(len(inm_means), REF_Y), s=20,
               color=cs.INDIGO, alpha=0.55, zorder=3)
    ax.text(max(inm_means) + 0.2, REF_Y, "in-market recall spread", va="center", ha="left",
            color=cs.INDIGO, fontsize=cs.FONT_SIZES["annotation"])
    ax.set_yticks(list(y) + [REF_Y]); ax.set_yticklabels(names + ["in-market\n(v0.22)"])
    ax.set_xlabel("mean combined recall  r  (across the six-model panel)")
    ax.set_xlim(0, max(max(inm_means), 1.2) + 0.8)
    ax.set_ylim(REF_Y + 0.6, -1.1)    # inverted (Pontiac top), reference row at bottom
    fig.subplots_adjust(**cs.MARGINS["single"])
    cs.add_header(fig, "Phantom brands return undefined CPC, as predicted",
                  "Cell-D defunct automotive brands: zero recall → below floor → N/A",
                  "Consistency is undefined for brands with no AI presence to be consistent about.")
    cs.add_footer(fig, verdict="H_CPC_PhantomNull CONFIRMED — all 5 Cell-D defunct brands → N/A.",
                  phase=SOURCE_PHASE, protocol="v1.7-prereg-r2")
    p = OUT / "fig_03_phantom_null.pdf"; fig.savefig(p, **cs.SAVEFIG_PARAMS); plt.close(fig)
    return p


def fig_04_cv_mean_coupling():
    """Finding 2 mechanism: CV vs mean recall with the Poisson 1/sqrt(mean) curve."""
    pts = [r for r in rows if r["in_market"] and r["cpc_raw"] is not None]
    xs = np.array([r["mean_r"] for r in pts])
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    for s in ["v0.20", "v0.21", "v0.22"]:
        sx = [r["mean_r"] for r in pts if r["substrate"] == s]
        sy = [r["cpc_raw"] for r in pts if r["substrate"] == s]
        ax.scatter(sx, sy, s=42, color=SUB_COLOR[s], alpha=0.85, edgecolor="white",
                   linewidth=0.6, label=SUB_NAME[s], zorder=3)
    # Poisson prediction: CV = 1/sqrt(mean) — the mechanical coupling the data hug
    xc = np.linspace(max(xs.min(), 0.6), xs.max(), 120)
    ax.plot(xc, 1.0 / np.sqrt(xc), color=cs.BLACK, lw=1.5, ls="--", zorder=2,
            label="Poisson: CV = 1/$\\sqrt{\\mathrm{mean}}$")
    ax.text(0.97, 0.95,
            "rank correlation (CV, mean) = -0.77\n"
            "spread is set by the average, so a\nCV score restates the average",
            transform=ax.transAxes, ha="right", va="top",
            fontsize=cs.FONT_SIZES["annotation"],
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=cs.PALETTE["gray_light"], lw=0.6))
    ax.set_xlabel("mean combined recall  r  (across the six-model panel)")
    ax.set_ylabel("CV  =  SD / mean   (the raw dispersion)")
    ax.legend(loc="lower left", fontsize=cs.FONT_SIZES["legend"])
    fig.subplots_adjust(**cs.MARGINS["single"])
    cs.add_header(fig, "Spread is governed by the mean",
                  "Coefficient of variation against mean recall, with the Poisson prediction",
                  "At the counts models produce, CV approaches 1/√mean — so a CV-based score reparametrizes level.")
    cs.add_footer(fig, verdict="The presence–consistency coupling is arithmetic, not incidental — it recurs for any low-count CV score.",
                  phase=SOURCE_PHASE, protocol="v1.7-prereg-r2")
    p = OUT / "fig_04_cv_mean_coupling.pdf"; fig.savefig(p, **cs.SAVEFIG_PARAMS); plt.close(fig)
    return p


if __name__ == "__main__":
    for fn in (fig_01_cpc_defined, fig_02_cpc_dissociation, fig_03_phantom_null,
               fig_04_cv_mean_coupling):
        print("wrote:", fn())
