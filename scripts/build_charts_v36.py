#!/usr/bin/env python3
"""
AIAS(TM) v0.36 -- CPC Regime Emergence -- figure builder.

Five figures. SSOT for every numeric value: osf/v36/v36_verdicts.json and
reports/figs/v36/data/*.csv (emitted by the locked scorer scripts/score_v0_36.py,
tag v0.36-prereg-r2). The silhouette permutation-null histogram (chart_01) and
per-substrate dispersion (chart_03) are recomputed deterministically (seed from
the prereg module) by importing the locked scorer functions; the recomputed
observed silhouette is asserted equal to the SSOT value.

Chart conventions: chart_style.py (Akkurat Pro registered at module top; Third
System brand tokens, Indigo primary; left-aligned title/subtitle/italic-
description at the top via fig.text x=0.04; source line left-aligned at bottom).
This builder adds a footer that keeps the verdict line clear of the xlabel and
>= 20pt above the source line.

  chart_01_omnibus_structure   weak omnibus structure; autonomy miss
  chart_02_inheritance_floor   inheritance unevaluable at power (24 -> 9; k=1)
  chart_03_saturation_reversal direction reversal (saturated dispersion higher)
  chart_04_residual_divergence primary (v0.23) vs sensitivity-only (omnibus)
  chart_05_verdict_matrix      predicted Cell A -> landed Cell D

Outputs reports/figs/v36/chart_0N_*.pdf
Usage: cd /Users/pablou/aias && python3 scripts/build_charts_v36.py
"""
import sys
import csv
import json
import importlib.util
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
from scipy.spatial.distance import pdist, squareform

ROOT = Path.home() / "aias"
sys.path.insert(0, str(ROOT / "scripts"))
import chart_style as cs
cs.setup()

# import the locked scorer (functions only; no main() runs on import)
_spec = importlib.util.spec_from_file_location("score_v0_36", ROOT / "scripts" / "score_v0_36.py")
sc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sc)
SPEC = sc.load_spec()
SEED = SPEC.SEED
PERM_N = SPEC.CLUSTERING["permutation_null_n"]

PHASE = "v0.36 (CPC Regime Emergence)"
PROTO = "v0.36-prereg-r2"
FIG_DIR = ROOT / "reports" / "figs" / "v36"
DATA_DIR = FIG_DIR / "data"
FIG_DIR.mkdir(parents=True, exist_ok=True)

SUBS = ["v0.19", "v0.20", "v0.21", "v0.22", "v0.23"]
CAT = {"v0.19": "headphones", "v0.20": "skincare", "v0.21": "cosmetics",
       "v0.22": "automotive", "v0.23": "spirits"}
INDIGO, WARM, TEAL, GRAY = cs.INDIGO, cs.WARM, cs.TEAL, cs.GRAY
GRAYL = cs.PALETTE["gray_light"]

# ---- SSOT ----------------------------------------------------------------- #
V = json.load(open(ROOT / "osf" / "v36" / "v36_verdicts.json"))
HYP = V["hypotheses"]
SAT = HYP["H_SaturationDegeneracy"]
NDEF = V["metadata"]["n_defined_per_substrate"]


def load_gap_curves():
    out = {}
    for r in csv.DictReader(open(DATA_DIR / "gap_curves.csv")):
        a = r["analysis"]
        out.setdefault(a, {"k": [], "gap": [], "s": []})
        out[a]["k"].append(int(r["k"]))
        out[a]["gap"].append(float(r["gap"]))
        out[a]["s"].append(float(r["gap_s"]))
    return out


GAP = load_gap_curves()


# ---- footer with guaranteed verdict clearance (>=20pt above source) ------- #
def footer(fig, verdict):
    h = fig.get_figheight()
    pt = 1.0 / (72.0 * h)            # one vertical point in figure fraction
    source_y = 9 * pt
    verdict_y = source_y + 26 * pt   # 26pt gap (>= 20pt requirement)
    src = f"Source: AIAS™ {PHASE} | Protocol {PROTO} | Third System™"
    if verdict:
        fig.text(cs.LEFT_X, verdict_y, verdict, fontsize=cs.FONT_SIZES["verdict"],
                 color=INDIGO, fontstyle="italic", ha="left", va="bottom")
    fig.text(cs.LEFT_X, source_y, src, fontsize=cs.FONT_SIZES["source"],
             color=GRAY, ha="left", va="bottom")


def save(fig, name):
    fig.savefig(FIG_DIR / f"{name}.pdf", **cs.SAVEFIG_PARAMS)
    plt.close(fig)
    print(f"  wrote {name}.pdf")


def gap_plot(ax, key, sel_k, color, title):
    g = GAP[key]
    ax.errorbar(g["k"], g["gap"], yerr=g["s"], fmt="o-", color=color,
                ecolor=GRAYL, elinewidth=1.0, capsize=2.5, ms=4, lw=1.3, zorder=3)
    ax.axvline(sel_k, color=color, ls="--", lw=1.0, alpha=0.7, zorder=1)
    yi = g["gap"][g["k"].index(sel_k)]
    ax.scatter([sel_k], [yi], s=90, facecolor="none", edgecolor=color,
               linewidth=1.8, zorder=4)
    ax.annotate(f"selected k={sel_k}", (sel_k, yi),
                textcoords="offset points", xytext=(8, 10),
                fontsize=cs.FONT_SIZES["annotation"], color=color, fontweight="bold")
    ax.set_xlabel("k (clusters)", fontsize=cs.FONT_SIZES["axis_label"])
    ax.set_ylabel("gap statistic", fontsize=cs.FONT_SIZES["axis_label"])
    ax.set_xticks(range(1, 9))
    ax.tick_params(labelsize=cs.FONT_SIZES["axis_tick"])
    ax.set_title(title, fontsize=cs.FONT_SIZES["axis_label"], fontweight="bold",
                 loc="left", color=cs.BLACK, pad=6)


# ============================================================ chart_01
def chart_01():
    # recompute silhouette null (deterministic) for the histogram; verify obs
    units = sc.load_units()
    X, meta = sc.build_feature_matrix(units)
    D = squareform(pdist(X, metric="euclidean"))
    labels = sc.ward_labels(X, 3)
    obs = sc.silhouette_from_dist(D, labels)
    assert abs(obs - V["omnibus_internal_structure_descriptor"]["silhouette"]) < 1e-3, obs
    subs = np.array([m["substrate"] for m in meta])
    idxs = {s: np.where(subs == s)[0] for s in np.unique(subs)}
    rng = np.random.default_rng(SEED)
    null = np.empty(PERM_N)
    for i in range(PERM_N):
        perm = labels.copy()
        for s, idx in idxs.items():
            perm[idx] = rng.permutation(perm[idx])
        null[i] = sc.silhouette_from_dist(D, perm)
    p95 = np.percentile(null, 95)
    THRESH = SPEC.HYPOTHESES["H_RegimeAutonomy"]["criteria"]["silhouette_min"]

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.5, 4.7))
    fig.subplots_adjust(top=0.80, bottom=0.26, left=0.08, right=0.97, wspace=0.26)

    gap_plot(axL, "omnibus_raw", 3, INDIGO, "Gap statistic (omnibus, 112 -> 55 defined)")

    axR.hist(null, bins=40, color=GRAYL, edgecolor="white", linewidth=0.3, zorder=2)
    axR.axvline(p95, color=GRAY, ls=":", lw=1.2, zorder=3)
    axR.axvline(THRESH, color=WARM, ls="--", lw=1.4, zorder=4)
    axR.axvline(obs, color=INDIGO, lw=1.8, zorder=5)
    axR.set_xlim(-0.13, 0.33)
    block = [(f"permutation null (95th pct = {p95:.3f})", GRAY, "normal"),
             ("locked threshold = 0.25", WARM, "bold"),
             (f"observed = {obs:.4f}  (null pct 100)", INDIGO, "bold")]
    yb = 0.96
    for txt, c, w in block:
        axR.text(0.40, yb, txt, transform=axR.transAxes, color=c,
                 fontsize=cs.FONT_SIZES["annotation"], fontweight=w, va="top", ha="left")
        yb -= 0.075
    axR.set_xlabel("mean silhouette", fontsize=cs.FONT_SIZES["axis_label"])
    axR.set_ylabel("permutation null (count)", fontsize=cs.FONT_SIZES["axis_label"])
    axR.tick_params(labelsize=cs.FONT_SIZES["axis_tick"])
    axR.set_title("Observed silhouette vs 0.25 threshold & null",
                  fontsize=cs.FONT_SIZES["axis_label"], fontweight="bold",
                  loc="left", color=cs.BLACK, pad=6)

    cs.add_header(fig,
                  "Omnibus CPC structure is weak — above null, below the locked bar",
                  "Ward/Euclidean clustering of the 6-dim per-model CPC signal; gap selects k=3.",
                  "Silhouette 0.2422 exceeds the 95th-percentile null but falls under the 0.25 autonomy threshold — a near miss.")
    footer(fig, "H_RegimeAutonomy NOT SUPPORTED — silhouette below locked 0.25 threshold (though above the permutation null).")
    save(fig, "chart_01_omnibus_structure")


# ============================================================ chart_02
def chart_02():
    n_total, n_def = 24, NDEF["v0.23"]
    n_exc = n_total - n_def
    inh = HYP["H_RegimeInheritance"]

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.5, 4.7),
                                   gridspec_kw={"width_ratios": [1.0, 1.15]})
    fig.subplots_adjust(top=0.80, bottom=0.26, left=0.09, right=0.97, wspace=0.30)

    # left: coverage waterfall 24 -> 9 (block bars)
    axL.bar([0], [n_total], width=0.6, color=INDIGO, zorder=3, label="v0.23 brands")
    axL.bar([1], [n_def], width=0.6, color=TEAL, zorder=3, label="defined (CV-CPC computable)")
    axL.bar([1], [n_exc], width=0.6, bottom=[n_def], color=GRAYL, zorder=3,
            label="excluded (mean recall < 1.0)")
    for x, v in [(0, n_total), (1, n_def)]:
        axL.annotate(str(v), (x, v), textcoords="offset points", xytext=(0, 4),
                     ha="center", fontsize=cs.FONT_SIZES["data_label"], fontweight="bold")
    axL.annotate(f"-{n_exc} undefined", (1, n_def + n_exc / 2), color=GRAY,
                 ha="center", va="center", fontsize=cs.FONT_SIZES["annotation"])
    axL.set_xticks([0, 1]); axL.set_xticklabels(["registry", "analysis set"])
    axL.set_ylabel("brand units", fontsize=cs.FONT_SIZES["axis_label"])
    axL.set_ylim(0, 27)
    axL.tick_params(labelsize=cs.FONT_SIZES["axis_tick"])
    axL.legend(fontsize=cs.FONT_SIZES["legend"] - 0.5, loc="upper right", framealpha=0.9)
    axL.set_title("v0.23 coverage under the CV-CPC floor",
                  fontsize=cs.FONT_SIZES["axis_label"], fontweight="bold",
                  loc="left", color=cs.BLACK, pad=6)

    # right: v0.23 n=9 gap curve selecting k=1
    gap_plot(axR, "v23_raw", 1, WARM, "v0.23 gap (n=9) — selects k=1")
    axR.annotate(f"k=1 → single cluster\nARI = {inh['ari']:.2f} (null pct {inh['ari_null_pct']:.0f}, p={inh['ari_p']:.2f})",
                 (0.97, 0.05), xycoords="axes fraction", ha="right", va="bottom",
                 fontsize=cs.FONT_SIZES["annotation"], color=WARM, fontweight="bold")

    cs.add_header(fig,
                  "Inheritance is unevaluable at power — the floor leaves n=9",
                  "The CV-CPC computability floor reduces v0.23 from 24 brands to 9; gap then selects k=1.",
                  "With one cluster the Adjusted Rand Index against the Presence-quartile regime is 0 by construction.")
    footer(fig, "H_RegimeInheritance NOT SUPPORTED — computability floor; test underpowered (n=9), recorded as-scored.")
    save(fig, "chart_02_inheritance_floor")


# ============================================================ chart_03
def chart_03():
    units = sc.load_units()
    def devmean(s):
        v = np.array([u["cvcpc"] for u in units if u["substrate"] == s and u["defined"]])
        return float(np.mean(np.abs(v - np.median(v)))) if len(v) else np.nan
    dev = {s: devmean(s) for s in SUBS}
    sat_set = set(SPEC.ANALYSIS_SET_SPEC["saturated_substrate_list"]["operative"]["saturated"])
    sat_mean = SAT["dev_mean_saturated"]
    uns_mean = SAT["dev_mean_unsaturated"]
    pk = SAT["per_substrate_gap_k"]

    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    fig.subplots_adjust(top=0.80, bottom=0.28, left=0.10, right=0.96)

    xs = range(len(SUBS))
    for i, s in enumerate(SUBS):
        c = INDIGO if s in sat_set else WARM
        ax.scatter([i], [dev[s]], s=130, color=c, zorder=4,
                   edgecolor="white", linewidth=0.8)
        ax.annotate(f"{dev[s]:.3f}\n(k={pk[s]})", (i, dev[s]),
                    textcoords="offset points", xytext=(0, 10), ha="center",
                    fontsize=cs.FONT_SIZES["annotation"], color=c, fontweight="bold")

    ax.axhline(sat_mean, color=INDIGO, ls="--", lw=1.2, zorder=2)
    ax.axhline(uns_mean, color=WARM, ls="--", lw=1.2, zorder=2)
    _wb = dict(facecolor="white", edgecolor="none", pad=1.0)
    ax.annotate(f"saturated mean {sat_mean:.3f}", (4.5, sat_mean),
                color=INDIGO, fontsize=cs.FONT_SIZES["annotation"], va="bottom",
                ha="left", bbox=_wb)
    ax.annotate(f"unsaturated mean {uns_mean:.3f}", (4.5, uns_mean),
                color=WARM, fontsize=cs.FONT_SIZES["annotation"], va="bottom",
                ha="left", bbox=_wb)

    # predicted-vs-observed direction arrow (in the open right margin)
    arr = FancyArrowPatch((5.25, uns_mean), (5.25, sat_mean), arrowstyle="-|>",
                          mutation_scale=13, color=GRAY, lw=1.6, zorder=3)
    ax.add_patch(arr)
    ax.annotate("observed:\nsaturated HIGHER\n(predicted: lower)",
                (5.05, (sat_mean + uns_mean) / 2), ha="right", va="center",
                fontsize=cs.FONT_SIZES["annotation"], color=GRAY, fontstyle="italic")

    ax.set_xticks(list(xs))
    ax.set_xticklabels([f"{s}\n{CAT[s]}" for s in SUBS])
    ax.set_xlim(-0.6, 5.7)
    ax.set_ylabel("within-substrate CPC dispersion\n(mean |CV-CPC − median|)",
                  fontsize=cs.FONT_SIZES["axis_label"])
    ax.tick_params(labelsize=cs.FONT_SIZES["axis_tick"])
    ax.set_ylim(0, max(dev.values()) * 1.35)
    # stats inside the axes (upper-left, open space) — clears the footer verdict
    stats = (f"Levene p={SAT['bf_levene_p_two_sided']:.3f} (opposite sign)  ·  "
             f"BF directional p={SAT['bf_directional_p']:.4f}\n"
             f"criterion (b) fail — per-substrate k: "
             + "/".join(str(pk[s]) for s in SUBS))
    ax.text(0.015, 0.98, stats, transform=ax.transAxes, ha="left", va="top",
            fontsize=cs.FONT_SIZES["annotation"], color=cs.BLACK, linespacing=1.4)

    cs.add_header(fig,
                  "Saturation reversal — saturated substrates carry MORE CPC dispersion",
                  "Within-substrate CPC dispersion by substrate; indigo = saturated (v0.34), copper = unsaturated.",
                  "The pre-registered prediction (saturated collapse, lower dispersion) is reversed; criterion (b) also fails.")
    footer(fig, "H_SaturationDegeneracy NOT SUPPORTED — direction reversed; variance higher where recognition saturates.")
    save(fig, "chart_03_saturation_reversal")


# ============================================================ chart_04
def chart_04():
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.5, 4.7), sharey=False)
    fig.subplots_adjust(top=0.80, bottom=0.26, left=0.08, right=0.97, wspace=0.26)

    gap_plot(axL, "v23_residual", 1, INDIGO,
             "PRIMARY — v0.23 residual on composite_presence")
    axL.annotate("k=1 — no residual structure", (0.97, 0.05),
                 xycoords="axes fraction", ha="right", va="bottom",
                 fontsize=cs.FONT_SIZES["annotation"], color=INDIGO, fontweight="bold")

    gap_plot(axR, "omnibus_mean_recall_residual", 2, TEAL,
             "SENSITIVITY-ONLY — omnibus mean-recall residual")
    axR.annotate("k=2 — criteria met,\nbut never verdict-determining", (0.97, 0.05),
                 xycoords="axes fraction", ha="right", va="bottom",
                 fontsize=cs.FONT_SIZES["annotation"], color=TEAL, fontweight="bold")

    cs.add_header(fig,
                  "Residual structure: primary says no, sensitivity arm diverges",
                  "Left: locked primary (v0.23, residualized on composite_presence). Right: omnibus mean-recall residual arm.",
                  "The verdict rests on the primary (k=1, no structure); the sensitivity arm (k=2) is reported but not verdict-determining.")
    footer(fig, "H_ResidualStructure NOT SUPPORTED — primary arm (v0.23), as predicted.")
    save(fig, "chart_04_residual_divergence")


# ============================================================ chart_05
def chart_05():
    fig = plt.figure(figsize=(7.5, 4.8))
    fig.subplots_adjust(top=0.78, bottom=0.20, left=0.05, right=0.97)
    gs = fig.add_gridspec(1, 2, width_ratios=[1.35, 1.0], wspace=0.18)
    axm = fig.add_subplot(gs[0, 0]); axm.axis("off")
    axr = fig.add_subplot(gs[0, 1]); axr.axis("off")

    cells = {
        (0, 1): ("Cell A", "borrowed structure", "inheritance + no residual"),
        (1, 1): ("Cell B", "layered structure", "inheritance + residual"),
        (0, 0): ("Cell C", "autonomous structure", "autonomy + residual"),
        (1, 0): ("Cell D", "unstructured", "unstructured + no residual"),
    }
    landed = "Cell D"
    predicted = "Cell A"
    for (cx, cy), (cell, verdict, cond) in cells.items():
        x, y, w, h = cx, cy, 0.96, 0.96
        is_land = cell == landed
        face = INDIGO if is_land else cs.PALETTE["white"]
        rect = Rectangle((x, y), w, h, facecolor=face, edgecolor=GRAYL,
                         linewidth=1.0, zorder=2)
        axm.add_patch(rect)
        if cell == predicted:
            axm.add_patch(Rectangle((x + 0.02, y + 0.02), w - 0.04, h - 0.04,
                                    facecolor="none", edgecolor=WARM, linewidth=2.2,
                                    linestyle=(0, (4, 2)), zorder=4))
        tc = cs.PALETTE["white"] if is_land else cs.BLACK
        axm.text(x + w / 2, y + h - 0.16, cell, ha="center", va="top",
                 fontsize=10.5, fontweight="bold", color=tc)
        axm.text(x + w / 2, y + h / 2 + 0.02, verdict, ha="center", va="center",
                 fontsize=7.5, color=tc)
        axm.text(x + w / 2, y + 0.12, cond, ha="center", va="bottom",
                 fontsize=6.4,
                 color=(cs.PALETTE["indigo_t3"] if is_land else GRAY), fontstyle="italic")
    # legend chips
    axm.add_patch(Rectangle((0.0, -0.42), 0.14, 0.16, facecolor=INDIGO, edgecolor="none"))
    axm.text(0.18, -0.34, "landed (observed)", fontsize=cs.FONT_SIZES["annotation"], va="center")
    axm.add_patch(Rectangle((1.05, -0.42), 0.14, 0.16, facecolor="none",
                            edgecolor=WARM, linewidth=2.0, linestyle=(0, (4, 2))))
    axm.text(1.23, -0.34, "predicted (pre-registered)", fontsize=cs.FONT_SIZES["annotation"], va="center")
    axm.set_xlim(-0.05, 2.05); axm.set_ylim(-0.5, 2.0)
    axm.set_aspect("equal")

    # right ribbon: hypotheses + verdicts + scopes
    order = [("H_RegimeInheritance", "v0.23 (n=9)"),
             ("H_RegimeAutonomy", "omnibus + v0.23 ARI"),
             ("H_ResidualStructure", "v0.23 primary"),
             ("H_SaturationDegeneracy", "omnibus (112)")]
    axr.text(0.0, 1.0, "Hypothesis verdicts", fontsize=cs.FONT_SIZES["subtitle"],
             fontweight="bold", va="top", color=cs.BLACK)
    yy = 0.88
    for h, scope in order:
        v = HYP[h]["verdict"]
        axr.text(0.0, yy, h, fontsize=8.6, fontweight="bold", va="top", color=cs.BLACK)
        axr.text(0.0, yy - 0.055, f"{v}", fontsize=8.2, va="top", color=WARM)
        axr.text(0.0, yy - 0.105, f"scope: {scope}", fontsize=7.2, va="top",
                 color=GRAY, fontstyle="italic")
        yy -= 0.20
    axr.set_xlim(0, 1); axr.set_ylim(0, 1)

    cs.add_header(fig,
                  "Verdict matrix — predicted Cell A, landed Cell D",
                  "pre-registered prediction falsified; reported as-scored.",
                  "Inheritance and saturation both fail (saturation reverses); residual-structure null as predicted.")
    footer(fig, "Net: Cell D (unstructured). Predicted Cell A (borrowed structure) — falsified.")
    save(fig, "chart_05_verdict_matrix")


if __name__ == "__main__":
    print("Building v0.36 figures...")
    chart_01(); chart_02(); chart_03(); chart_04(); chart_05()
    print(f"Done -> {FIG_DIR}")
