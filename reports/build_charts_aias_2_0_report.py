#!/usr/bin/env python3
"""
build_charts_aias_2_0_report.py - AIAS(TM) 2.0 synthesis, brand-format report figures (P1-P5).

One chart per finding, placed with its finding in build_report_aias_2_0.py:

  report_fig_01_link_between_scores    P1  |rho(C*, P)| by wave
  report_fig_02_brand_order_kept       P2  June-to-November retest, with the shuffled-answer range
  report_fig_03_agreement_vs_naming    P3  first vs current agreement measure, rho with mean recall
  report_fig_04_rated_share            P4  share of brands rated, by category and wave
  report_fig_05_combined_scores        P5  eight candidate composites, rho(A, P), May and June (+ November)

Title and subtitle are CHART_SPECS[Pn]["title"/"subtitle"] from reports/aias_2_0_content.py,
verbatim. Every plotted value is READ from the locked records and printed; each is asserted
against the figure stated in CHART_SPECS[Pn]["data"].

Inputs (locked):
  osf/aias_2_0/aias_2_0_synthesis_data.json, aias_2_0_profiles.csv   (P1, P2, P4)
  osf/methodology/v1_9/v1_9_verdicts.json, prereg/v1_9_calibration.json   (P2, P5)
  osf/v41/registries/v1_8_verdicts.json   (frozen v1.8 verdicts; P3)

Run on the Mac (Akkurat Pro), from the worktree:
  AIAS_ROOT=<worktree> ~/aias/venv/bin/python reports/build_charts_aias_2_0_report.py
"""
import csv
import json
import os
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.transforms
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

# --- Akkurat Pro (registered at module top) -------------------------------
for _d in (Path.home() / ".fonts" / "Akkurat", Path.home() / "Library" / "Fonts"):
    if _d.exists():
        for _f in list(_d.glob("*.otf")) + list(_d.glob("*.ttf")):
            fm.fontManager.addfont(str(_f))
plt.rcParams.update({
    "font.family": ["Akkurat Pro", "sans-serif"],
    "axes.unicode_minus": False,
    "font.size": 9,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.linewidth": 0.6,
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
    "xtick.major.size": 0,
    "ytick.major.size": 0,
})

HERE = Path(__file__).resolve().parent
ROOT = Path(os.environ.get("AIAS_ROOT", str(HERE.parent))).resolve()
sys.path.insert(0, str(HERE))
import aias_2_0_content as content  # noqa: E402

SPECS = content.CHART_SPECS
OUT = ROOT / "reports/figs/aias_2_0/report"
OUT.mkdir(parents=True, exist_ok=True)

INDIGO, INDIGO_2, INDIGO_3 = "#37237B", "#908EC5", "#BBB9DD"
BLACK, GRAY, LIGHT, LIMIT = "#1A1A1A", "#6E6E6E", "#CCCCCC", "#4A4A4A"
WIDTH = 7.5
SOURCE_TAIL = "AIAS 2.0 synthesis, Third System"

# ---------------------------------------------------------------- data (read, never typed)
A2 = ROOT / "osf/aias_2_0"
D = json.load(open(A2 / "aias_2_0_synthesis_data.json"))
assert D["status"] == "complete", "build figures only from the data lock"
PROF = list(csv.DictReader(open(A2 / "aias_2_0_profiles.csv", newline="")))
SUM = D["summaries"]
M19 = ROOT / "osf/methodology/v1_9"
VER = json.load(open(M19 / "v1_9_verdicts.json"))["verdicts"]
CAL = json.load(open(M19 / "prereg/v1_9_calibration.json"))
V18 = json.load(open(ROOT / "osf/v41/registries/v1_8_verdicts.json"))["verdicts"]

# the paper's own loaders (lineage inside the data lock) must agree with the standalone files
assert D["stage2"]["v19_verdicts"]["H_Consistency_Reliability"]["rho"] == VER["H_Consistency_Reliability"]["rho"]
assert D["lineage"]["v1.9-stage1"]["record"]["candidates"] == CAL["candidates"]
assert D["lineage"]["v1.8"]["record"]["verdicts"]["H_CV_Reproduces"]["stat"] == V18["H_CV_Reproduces"]["stat"]


def check(label, got, want, dec):
    """Print a plotted value and require it to equal the stated figure to `dec` decimals."""
    ok = round(got, dec) == round(want, dec)
    print(f"    {label:48s} {got:.6f}  -> {round(got, dec):.{dec}f}   spec {want:.{dec}f}   {'OK' if ok else 'MISMATCH'}")
    if not ok:
        raise SystemExit(f"MISMATCH: {label}: {got} vs {want}")


def checkn(label, got, want):
    ok = got == want
    print(f"    {label:48s} n = {got}   spec {want}   {'OK' if ok else 'MISMATCH'}")
    if not ok:
        raise SystemExit(f"MISMATCH: {label}: {got} vs {want}")


# ---------------------------------------------------------------- frame
def frame(key, h):
    """Figure with bold title, gray subtitle, thin Indigo rule and italic gray source line."""
    spec = SPECS[key]
    fig = plt.figure(figsize=(WIDTH, h))
    x0 = 0.035
    fig.text(x0, 1 - 0.13 / h, spec["title"], fontsize=13, fontweight="bold", color=BLACK, ha="left", va="top")
    fig.text(x0, 1 - 0.43 / h, spec["subtitle"], fontsize=8.8, color=GRAY, ha="left", va="top")
    ry = 1 - 0.66 / h
    fig.add_artist(Line2D([x0, 1 - 0.025], [ry, ry], color=INDIGO, lw=0.8, transform=fig.transFigure))
    fig.text(x0, 0.12 / h, f"Source: {spec['source']} | {SOURCE_TAIL}", fontsize=7, color=GRAY,
             fontstyle="italic", ha="left", va="bottom")
    return fig


def place(fig, h, left, right, bottom_in, top_in):
    """Axes box in inches from the bottom / below the rule."""
    top = 1 - (0.66 + top_in) / h
    bottom = bottom_in / h
    return fig.add_axes([left, bottom, right - left, top - bottom])


def save(fig, name):
    fig.savefig(OUT / f"{name}.pdf")
    plt.close(fig)
    print(f"  wrote {name}.pdf")


def clean(ax, left=True):
    for s in ("top", "right") + (() if left else ("left",)):
        ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=8)


# ============================================================ P1
def chart_p1():
    print("P1")
    t3 = VER["H_Dissociation_t3"]
    rows = [("May", abs(SUM["t1"]["rho_Cstar_P"]), SUM["t1"]["rho_Cstar_P_n"]),
            ("June", abs(SUM["t2"]["rho_Cstar_P"]), SUM["t2"]["rho_Cstar_P_n"]),
            ("November", abs(t3["rho"]), t3["n"])]
    for (lab, v, n), want, wn in zip(rows, (0.073, 0.082, 0.189), (55, 54, 54)):
        check(f"|rho(C*,P)| {lab}", v, want, 3)
        checkn(f"n {lab}", n, wn)
    h = 3.0
    fig = frame("P1", h)
    ax = place(fig, h, 0.17, 0.96, 0.62, 0.12)
    ys = [2, 1, 0]
    for y, (lab, v, n) in zip(ys, rows):
        ax.plot([0, v], [y, y], color=INDIGO, lw=1.6, alpha=0.5, zorder=1)
        ax.scatter([v], [y], s=64, color=INDIGO, zorder=3, edgecolor="white", lw=0.7)
        ax.text(v + 0.014, y, f"{v:.3f}", va="center", ha="left", fontsize=9, color=INDIGO, fontweight="bold")
    ax.axvline(0.30, color=LIMIT, lw=1.0, ls=":", zorder=0)
    ax.axvline(0.50, color=LIMIT, lw=1.0, ls="--", zorder=0)
    ax.text(0.30, 2.62, "0.30 pass mark", fontsize=7.4, color=LIMIT, ha="center", va="bottom")
    ax.text(0.50, 2.62, "0.50 too close", fontsize=7.4, color=LIMIT, ha="center", va="bottom")
    ax.set_yticks(ys)
    ax.set_yticklabels([f"{lab}\nn = {n} brands" for lab, _, n in rows], fontsize=8.4, linespacing=1.35)
    ax.set_xlim(0, 0.6)
    ax.set_ylim(-0.6, 2.6)
    ax.set_xlabel("rank correlation of Consistency with Presence (absolute value)", fontsize=8.4)
    clean(ax)
    ax.tick_params(axis="y", length=0)
    save(fig, "report_fig_01_link_between_scores")


# ============================================================ P2
def chart_p2():
    print("P2")
    pr, cr = VER["H_Presence_Score_Reliability"], VER["H_Consistency_Reliability"]
    nul = cr["frame_structure_null"]
    check("Presence retest rho", pr["rho"], 0.954, 3)
    checkn("Presence n", pr["n"], 112)
    check("Consistency retest rho", cr["rho"], 0.647, 3)
    checkn("Consistency n", cr["n"], 52)
    check("shuffled-answer null mean", nul["null_mean"], 0.438, 3)
    check("shuffled-answer null 95th pct", nul["null_p95"], 0.585, 3)
    # pass marks: the registered constants in the data lock (0.80 Presence, 0.50 Consistency)
    marks = (0.80, 0.50)
    h = 3.2
    fig = frame("P2", h)
    ax = place(fig, h, 0.25, 0.96, 0.62, 0.12)
    rows = [("Presence", pr["rho"], pr["n"], marks[0], None),
            ("Consistency", cr["rho"], cr["n"], marks[1], nul)]
    ys = [1, 0]
    for y, (lab, v, n, mk, null) in zip(ys, rows):
        ax.plot([0, 1], [y, y], color=LIGHT, lw=0.8, zorder=0)
        if null:
            ax.plot([null["null_mean"], null["null_p95"]], [y, y], color=INDIGO_3, lw=9,
                    solid_capstyle="butt", zorder=1)
            ax.text((null["null_mean"] + null["null_p95"]) / 2, y - 0.2,
                    f"shuffled answers: mean {null['null_mean']:.3f}, 95th percentile {null['null_p95']:.3f}",
                    ha="center", va="top", fontsize=7.4, color=GRAY)
        ax.plot([mk, mk], [y - 0.14, y + 0.14], color=LIMIT, lw=1.4, zorder=2)
        ax.text(mk, y + 0.18, f"pass mark {mk:.2f}", ha="center", va="bottom", fontsize=7.4, color=LIMIT)
        ax.scatter([v], [y], s=78, color=INDIGO, zorder=3, edgecolor="white", lw=0.7)
        ax.text(v + 0.025 if null else v, y if null else y - 0.2, f"{v:.3f}  (n = {n})",
                ha="left" if null else "center", va="center" if null else "top", fontsize=9,
                color=INDIGO, fontweight="bold")
    ax.set_yticks(ys)
    ax.set_yticklabels([r[0] for r in rows], fontsize=9, fontweight="bold")
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.6, 1.55)
    ax.set_xlabel("rank correlation between the June and November waves", fontsize=8.4)
    clean(ax, left=False)
    ax.tick_params(axis="y", length=0)
    save(fig, "report_fig_02_brand_order_kept")


# ============================================================ P3
def chart_p3():
    print("P3")
    first = V18["H_CV_Reproduces"]["stat"]
    cur = V18["H_MeanIndependent"]["stat"]["pooled"]
    check("first measure (CV) |rho| with mean recall", first["abs_rho"], 0.682, 3)
    checkn("first measure n", first["n"], 55)
    check("current measure (phi) |rho| with mean recall", cur["abs_rho"], 0.091, 3)
    checkn("current measure n", cur["n"], 197)
    h = 2.8
    fig = frame("P3", h)
    ax = place(fig, h, 0.30, 0.96, 0.62, 0.12)
    rows = [("First measure\n(coefficient of variation)", first["abs_rho"], first["n"], False),
            ("Current measure\n(phi)", cur["abs_rho"], cur["n"], True)]
    ys = [1, 0]
    for y, (lab, v, n, cur_) in zip(ys, rows):
        ax.plot([0, v], [y, y], color=INDIGO if cur_ else GRAY, lw=1.6, alpha=0.5, zorder=1)
        ax.scatter([v], [y], s=70, color=INDIGO if cur_ else GRAY, zorder=3, edgecolor="white", lw=0.7)
        ax.text(v + 0.016, y, f"{v:.3f}  (n = {n})", va="center", ha="left", fontsize=9,
                color=INDIGO if cur_ else GRAY, fontweight="bold")
    ax.axvline(0.50, color=LIMIT, lw=1.0, ls="--", zorder=0)
    ax.text(0.505, 1.5, "0.50 independence ceiling", fontsize=7.4, color=LIMIT, ha="left", va="bottom")
    ax.set_yticks(ys)
    ax.set_yticklabels([r[0] for r in rows], fontsize=8.6, linespacing=1.35)
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.6, 1.7)
    ax.set_xlabel("rank correlation with mean recall (absolute value)", fontsize=8.4)
    clean(ax)
    ax.tick_params(axis="y", length=0)
    save(fig, "report_fig_03_agreement_vs_naming")


# ============================================================ P4
def chart_p4():
    print("P4")
    cats = ["v0.19", "v0.20", "v0.21", "v0.22", "v0.23"]
    names = {"v0.19": "Audiophile\nheadphones", "v0.20": "Skincare", "v0.21": "Cosmetics",
             "v0.22": "Automotive", "v0.23": "Premium\nspirits"}
    waves = (("t1", "May"), ("t2", "June"), ("t3", "November"))
    shares, lo, hi = {}, 1.0, 0.0
    tot = {}
    for w, _ in waves:
        ps = SUM[w]["per_substrate"]
        for s in cats:
            # cross-check the summary against the profiles table
            rows = [r for r in PROF if r["wave"] == w and r["substrate"] == s]
            assert sum(r["rated"] == "1" for r in rows) == ps[s]["n_rated"] and len(rows) == ps[s]["n_units"]
            sh = ps[s]["n_rated"] / ps[s]["n_units"]
            shares[(w, s)] = sh
            lo, hi = min(lo, sh), max(hi, sh)
            print(f"    {dict(waves)[w]:9s} {s} {ps[s]['n_rated']:>2}/{ps[s]['n_units']:<2}  {sh * 100:5.1f}%")
        tot[w] = (SUM[w]["n_rated"], SUM[w]["n_units"])
        shares[(w, "all")] = SUM[w]["n_rated"] / SUM[w]["n_units"]
    for (w, lab), want in zip(waves, (55, 54, 54)):
        checkn(f"rated total {lab} (of 112)", tot[w][0], want)
        checkn(f"units {lab}", tot[w][1], 112)
    print(f"    per-category share range: {lo * 100:.1f}% to {hi * 100:.1f}%")
    assert round(lo * 100) == 38 and round(hi * 100) == 58, "per-category shares must lie within 38-58%"
    groups = cats + ["all"]
    h = 3.7
    fig = frame("P4", h)
    ax = place(fig, h, 0.075, 0.975, 1.05, 0.12)
    w_ = 0.26
    cols = {"t1": INDIGO_3, "t2": INDIGO_2, "t3": INDIGO}
    for j, (w, lab) in enumerate(waves):
        vals = [shares[(w, g)] for g in groups]
        xs = np.arange(len(groups)) + (j - 1) * w_
        ax.bar(xs, vals, width=w_ * 0.92, color=cols[w], zorder=2,
               label=f"{lab} ({tot[w][0]} of {tot[w][1]} brands)")
        for x, v in zip(xs, vals):
            ax.text(x, v + 0.014, f"{v * 100:.0f}", ha="center", va="bottom", fontsize=7, color=BLACK)
    ax.axvline(len(cats) - 0.5, color=LIGHT, lw=0.8, zorder=0)
    ax.set_xticks(np.arange(len(groups)))
    ax.set_xticklabels([names[g] for g in cats] + ["All five\n(112 brands)"], fontsize=8, linespacing=1.25)
    ax.set_ylim(0, 0.80)
    ax.set_yticks([0, 0.25, 0.5, 0.75])
    ax.set_yticklabels(["0%", "25%", "50%", "75%"])
    ax.set_ylabel("share of brands rated", fontsize=8.4)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=3, fontsize=7.8, frameon=False)
    clean(ax)
    ax.tick_params(axis="x", length=0)
    save(fig, "report_fig_04_rated_share")


# ============================================================ P5
CONDITION = {"K1": "not separate", "K2": "like Presence", "K3": "early credit"}
LAB = {"C_phi": "phi", "C_phiJ": "phi + J", "FLOOR": "floor", "SHRINK": "shrink", "ADD": "average", "MOD": "multiply"}


def chart_p5():
    print("P5")
    cands = CAL["candidates"]
    assert len(cands) == 8
    limit = CAL["constants"]["K2"]
    check("limit rho(A,P)", limit, 0.95, 2)
    sel = next(i for i, c in enumerate(cands) if c["spec"] == "C_phi+FLOOR+ADD")
    nov = VER["H_NoComposite_t3"]["rho_A_P"]
    check("November floored average rho(A,P)", nov, 0.969, 3)
    floored = [c for c in cands if c["low_count"] == "FLOOR"]
    fvals = [abs(c[t]["K2"]["rho"]) for c in floored for t in ("t1", "t2")]
    print(f"    floored candidates ({len(floored)}): rho(A,P) range {min(fvals):.3f} to {max(fvals):.3f}")
    check("floored min", min(fvals), 0.971, 3)
    check("floored max", max(fvals), 0.997, 3)
    h = 4.8
    fig = frame("P5", h)
    ax = place(fig, h, 0.255, 0.67, 1.05, 0.30)
    y = np.arange(len(cands))[::-1]
    names, fails = [], []
    for i, c in enumerate(cands):
        m, j = abs(c["t1"]["K2"]["rho"]), abs(c["t2"]["K2"]["rho"])
        print(f"    {c['spec']:22s} May {m:.3f}  June {j:.3f}  pass K1/K2/K3 May {[c['t1'][k]['pass'] for k in ('K1','K2','K3')]} "
              f"June {[c['t2'][k]['pass'] for k in ('K1','K2','K3')]}")
        ax.plot([m, j], [y[i], y[i]], color=LIGHT, lw=1.2, zorder=1)
        ax.scatter([m], [y[i]], s=34, color=INDIGO_2, zorder=3, label="May" if i == 0 else None)
        ax.scatter([j], [y[i]], s=34, color=INDIGO, zorder=3, label="June" if i == 0 else None)
        names.append(f"{LAB[c['consistency']]} · {LAB[c['low_count']]} · {LAB[c['form']]}")
        failed = [k for k in ("K1", "K2", "K3") if not (c["t1"][k]["pass"] and c["t2"][k]["pass"])]
        assert failed, "every candidate fails at least one condition"
        fails.append(" · ".join(CONDITION[k] for k in failed))
    ax.scatter([nov], [y[sel]], s=50, marker="D", facecolor="white", edgecolor=INDIGO, lw=1.3, zorder=4,
               label="November, floored average")
    ax.axvline(limit, color=LIMIT, lw=1.0, ls="--", zorder=2)
    ax.axvspan(limit, 1.0, color="#E4E4E4", alpha=0.55, lw=0, zorder=0)
    ax.set_xlim(0.92, 1.0)
    ax.set_ylim(-0.6, len(cands) - 0.4)
    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=8)
    ax.set_xticks([0.92, 0.94, 0.96, 0.98, 1.0])
    ax.set_xlabel("rank correlation of the combined score with Presence", fontsize=8.4)
    ax.text(limit - 0.0015, y[0] + 0.62, "limit 0.95", ha="right", va="bottom", fontsize=7.4, color=LIMIT)
    clean(ax)
    ax.tick_params(axis="y", length=0)
    # failed-condition column to the right of the plot
    blend = matplotlib.transforms.blended_transform_factory(ax.transAxes, ax.transData)
    ax.text(1.03, len(cands) - 0.4, "Conditions failed", transform=blend, fontsize=8, fontweight="bold",
            color=BLACK, ha="left", va="bottom", clip_on=False)
    for i, f in enumerate(fails):
        ax.text(1.03, y[i], f, transform=blend, fontsize=7.4, color=BLACK, ha="left", va="center", clip_on=False)
    from matplotlib.patches import Patch
    hs, ls = ax.get_legend_handles_labels()
    hs.append(Patch(facecolor="#E4E4E4", edgecolor="none")); ls.append("fails the 0.95 limit")
    ax.legend(hs, ls, loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=4, fontsize=7.6, frameon=False,
              columnspacing=1.2, handletextpad=0.4)
    print("    failed conditions:", fails)
    save(fig, "report_fig_05_combined_scores")


if __name__ == "__main__":
    print(f"building AIAS 2.0 report figures -> {OUT}")
    chart_p1(); chart_p2(); chart_p3(); chart_p4(); chart_p5()
    print("done")
