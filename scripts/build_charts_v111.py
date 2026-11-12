#!/usr/bin/env python3
"""
v1.11 Sentiment Paper A -- figure builder (paper register; Paper A has no Third System report).
House style of build_charts_v112.py (scripts/chart_style.py: bold title top-left, gray subtitle, thin Indigo rule,
italic gray source line citing the pre-registration tag). Every number is a leaf of the scorer's outputs, read and
formatted through papers/v1_11/v111_values.py; nothing is re-scored.

One chart per pre-registered finding (PRE_REGISTRATION_v1_11.md sections 5-6):
  chart_01_judge_confusion   H1_Judge_Agreement (J1 x J2 valence counts)
  chart_02_separability      H2, H3, H5, H8 (per-wave rho_w with 95% intervals against the bands)
  chart_03_stability         H4, H6 (rho_w between waves with 95% intervals against the thresholds)
  chart_04_self_preference   H9 (mean u_J1 - u_J2, own-provider answers vs others)
  chart_05_baseline          cross-category baseline (section 6.1, descriptive)
Chart titles describe what is plotted and never repeat a finding's headline (CLAUDE.md).

Inputs: --outputs, the folder with v1_11_verdicts.json, stage_j_v1_11.json, judge_outputs_frozen_v1_11.json and
plan_v1_11.json (default osf/methodology/v1_11/outputs). --watermark TEXT stamps every chart (synthetic runs only;
required for them).

Usage (real run):  python3 scripts/build_charts_v111.py
Synthetic test:    python3 scripts/build_charts_v111.py --outputs /tmp/x/synth/scored --out /tmp/x/figs \
                       --watermark "SYNTHETIC TEST — NOT RESULTS"
"""
import argparse
import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "papers/v1_11"))
import chart_style as cs  # noqa: E402
import v111_values as VV  # noqa: E402
cs.setup()

SOURCE = "Source: AIAS™ Methodology v1.11, Sentiment Paper A | pre-registration {tag} | Third System™"
WATERMARK = None
TITLES = {
    1: "Valence assigned by the two judges to the same units",
    2: "Rank correlation of the Sentiment score with each comparator, per wave",
    3: "Rank correlation of each brand's Sentiment score between waves",
    4: "Primary minus second judge's unit score, by who wrote the answer",
    5: "Sentiment score of the rated brands by category, wave and block",
}
NAMES = {1: "chart_01_judge_confusion", 2: "chart_02_separability", 3: "chart_03_stability",
         4: "chart_04_self_preference", 5: "chart_05_baseline"}
PROVIDER = {"anthropic": "Anthropic", "openai": "OpenAI", "google": "Google", "xai": "xAI"}


def M(s):
    """Greek letters and relations through mathtext (the house font lacks them in italic)."""
    for a, b in (("ρ_w", r"$\rho_w$"), ("ρ", r"$\rho$"), ("α", r"$\alpha$"), ("Δ", r"$\Delta$"),
                 ("≤", r"$\leq$"), ("≥", r"$\geq$"), ("S_rec", r"$S_{rec}$")):
        s = s.replace(a, b)
    return s


WAVE_COL = {"t1": cs.PALETTE["indigo"], "t2": cs.PALETTE["blue"], "t3": cs.PALETTE["warm"]}


def _header(fig, key, subtitle, desc=""):
    cs.add_header(fig, TITLES[key], M(subtitle), M(desc))
    y = 1.0 - (0.74 / fig.get_figheight())
    fig.add_artist(Line2D([cs.LEFT_X, 0.985], [y, y], transform=fig.transFigure, color=cs.INDIGO, lw=0.6))


def _save(fig, key, verdict, tag, out):
    _, _, _, vy, sy = cs._compute_positions(fig)
    if verdict:
        fig.text(cs.LEFT_X, vy, M(verdict), fontsize=cs.FONT_SIZES["verdict"], color=cs.INDIGO, fontstyle="italic",
                 ha="left", va="bottom")
    fig.text(cs.LEFT_X, sy, SOURCE.format(tag=tag), fontsize=cs.FONT_SIZES["source"], color=cs.GRAY,
             fontstyle="italic", ha="left", va="bottom")
    if WATERMARK:
        fig.text(0.5, 0.5, WATERMARK, rotation=28, fontsize=30, color=cs.WARM, alpha=0.22, ha="center",
                 va="center", fontweight="bold", zorder=100)
    out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out / f"{NAMES[key]}.pdf", **cs.SAVEFIG_PARAMS)
    fig.savefig(out / f"{NAMES[key]}_preview.png", dpi=110, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    print(f"  wrote {out / (NAMES[key] + '.pdf')}")


def _f(x, fmt=VV.r3):
    return "n/a" if x is None or (isinstance(x, float) and not math.isfinite(x)) else fmt(x)


def _box(ax, text, x=0.03, y=0.97, ha="left", va="top", fs=7.6):
    ax.text(x, y, M(text), transform=ax.transAxes, ha=ha, va=va, fontsize=fs, color=cs.INDIGO,
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=cs.INDIGO, lw=0.6), zorder=5)


def chart_01(V, out):
    h1 = V["H1_Judge_Agreement"]
    conf = h1.get("confusion_J1_rows_J2_cols") or {}
    vals = [-2, -1, 0, 1, 2]
    M = [[float(conf.get(f"{a}|{b}", 0)) for b in vals] for a in vals]
    tot = sum(map(sum, M)) or 1.0
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    ax.imshow([[m / tot for m in r] for r in M], cmap="Purples", vmin=0, aspect="auto")
    for i, r in enumerate(M):
        for j, m in enumerate(r):
            ax.text(j, i, VV.i0(m), ha="center", va="center", fontsize=8.5,
                    color="white" if m / tot > 0.12 else cs.BLACK)
    lab = ["−2", "−1", "0", "+1", "+2"]
    ax.set_xticks(range(5), lab); ax.set_yticks(range(5), lab)
    ax.set_xlabel(f"J2 valence ({VV.J2_NAME})", fontsize=9)
    ax.set_ylabel(f"J1 valence ({VV.J1_NAME})", fontsize=9)
    ax.tick_params(labelsize=8.5)
    _box(ax, f"ordinal α = {_f(h1.get('alpha_ordinal'))}\nbrand ρ_w = {_f(h1['brand_rho'].get('rho'))} "
             f"(n = {h1['brand_rho'].get('n')})\nunit pairs = {VV.i0(h1['units_judged_by_both'])}",
         x=1.03, y=0.98, fs=7.6)
    fig.subplots_adjust(top=0.80, bottom=0.14, left=0.12, right=0.72)
    _header(fig, 1, "Counts of units with valid outputs from both judges; diagonal = same valence.",
            "Recognition, omnibus and the early sample; shading = share of all pairs.")
    _save(fig, 1, f"H1: {V['VERDICTS']['H1']} (thresholds: α ≥ 0.667 and ρ ≥ 0.80; falsified if α < 0.50 or ρ < 0.60)",
          V["prereg_tag"], out)


def chart_02(V, out):
    rows = [("H2_Sep_Presence", "S vs Presence P"), ("H3_Sep_Consistency", "S vs Consistency C*"),
            ("H5_Sep_Ranking", "S vs Ranking R*"), ("H8_Recognition_Sep", "S_rec vs Presence P")]
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    for x0 in (-0.5, -0.3, 0.3, 0.5):
        ax.axvline(x0, color=cs.WARM if abs(x0) == 0.5 else cs.PALETTE["gray_light"], lw=0.8, ls=":", zorder=1)
    ax.axvline(0, color=cs.PALETTE["gray_light"], lw=0.6, zorder=1)
    ylabels = []
    for i, (h, lab) in enumerate(rows):
        y0 = len(rows) - 1 - i
        word = V["VERDICTS"][VV.SHORT[h]]
        ylabels.append((y0, f"{VV.SHORT[h]}  {lab}\n{word}"))
        if h not in V:
            ax.text(0, y0, f"not computed ({word})", ha="center", va="center", fontsize=8, color=cs.GRAY)
            continue
        for k, w in enumerate(VV.WAVES):
            pw = V[h]["per_wave"][w]
            y = y0 + 0.22 - 0.22 * k
            if not pw.get("determinable") or pw.get("rho") is None:
                ax.text(-0.95, y, f"{w}: below floor (n = {pw.get('n')})", fontsize=7, color=cs.GRAY, va="center")
                continue
            lo, hi = (pw.get("ci95") or [pw["rho"], pw["rho"]])
            ax.plot([lo, hi], [y, y], color=WAVE_COL[w], lw=1.4, zorder=2)
            ax.scatter([pw["rho"]], [y], s=30, color=WAVE_COL[w], zorder=3, edgecolor="white", linewidth=0.4)
    ax.set_yticks([y for y, _ in ylabels], [M(t) for _, t in ylabels], fontsize=8)
    ax.set_xlim(-1, 1); ax.set_ylim(-0.6, len(rows) - 0.4)
    ax.set_xlabel(M("ρ_w (within-category ranks, centred per category; H8: plain Spearman)"), fontsize=9)
    ax.tick_params(axis="x", labelsize=8.5)
    handles = [Line2D([], [], color=WAVE_COL[w], marker="o", lw=1.4, label=w) for w in VV.WAVES]
    ax.legend(handles=handles, loc="center left", bbox_to_anchor=(1.01, 0.5), fontsize=7.6, frameon=False)
    fig.subplots_adjust(top=0.80, bottom=0.14, left=0.27, right=0.88)
    _header(fig, 2, "Point = ρ_w per wave; bar = 95% bootstrap interval; rated brand units.",
            "Dotted gray: |ρ| = 0.30 (separable); dotted orange: |ρ| = 0.50 (falsified at any determined wave).")
    _save(fig, 2, "Verdicts as the scorer wrote them (three-wave rule; noise guard applied where marked in the paper).",
          V["prereg_tag"], out)


def chart_03(V, out):
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero_short"])
    for x0, c in ((0.30, cs.PALETTE["gray_light"]), (0.50, cs.WARM)):
        ax.axvline(x0, color=c, lw=0.8, ls=":", zorder=1)
    labels = []
    for i, (h, lab) in enumerate((("H4_Stability_Short", "H4  t1 → t2 (3 weeks)"),
                                  ("H6_Stability_Long", "H6  t2 → t3 (5 months)"))):
        r = V[h]
        y = 1 - i
        labels.append((y, f"{lab}\n{V['VERDICTS'][VV.SHORT[h]]}"))
        if r.get("rho") is None:
            continue
        lo, hi = r.get("ci95") or [r["rho"], r["rho"]]
        col = cs.INDIGO if r.get("determinable") else cs.PALETTE["gray_light"]
        ax.plot([lo, hi], [y, y], color=col, lw=1.6, zorder=2)
        ax.scatter([r["rho"]], [y], s=36, color=col, zorder=3, edgecolor="white", linewidth=0.4)
        ax.text(min(hi + 0.03, 0.98), y + 0.18, M(f"ρ_w = {_f(r['rho'])}, p = {_f(r.get('p_perm'), VV.p4)}, "
                f"n = {r.get('n')}"), fontsize=7.4, color=cs.INDIGO, ha="right" if hi > 0.6 else "left")
    ax.set_yticks([y for y, _ in labels], [M(t) for _, t in labels], fontsize=8)
    ax.set_xlim(-1, 1); ax.set_ylim(-0.6, 1.6)
    ax.set_xlabel(M("ρ_w between waves (omnibus brand units rated at both)"), fontsize=9)
    ax.tick_params(axis="x", labelsize=8.5)
    fig.subplots_adjust(top=0.72, bottom=0.2, left=0.27, right=0.97)
    _header(fig, 3, "Point = ρ_w; bar = 95% bootstrap interval; one-sided permutation p.",
            "Dotted gray: 0.30; dotted orange: 0.50 (confirmed needs ρ ≥ 0.50 and p < .05).")
    _save(fig, 3, "", V["prereg_tag"], out)


def chart_04(V, out):
    h9 = V["H9_Self_Preference"]
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero_short"])
    vals = [(f"Answers by {PROVIDER.get(h9['j1_provider'], h9['j1_provider'])} models\n(n = {VV.i0(h9['n_own_provider'])})", h9.get("mean_diff_own")),
            (f"Answers by other models\n(n = {VV.i0(h9['n_other'])})", h9.get("mean_diff_other"))]
    for i, (lab, v) in enumerate(vals):
        if v is None:
            continue
        ax.barh(1 - i, v, color=cs.INDIGO if i == 0 else cs.PALETTE["indigo_t2"], height=0.5, zorder=2)
        ax.text(v + (0.3 if v >= 0 else -0.3), 1 - i, VV.sf1(v), va="center", ha="left" if v >= 0 else "right",
                fontsize=8, color=cs.BLACK)
    ax.axvline(0, color=cs.PALETTE["gray"], lw=0.6)
    ax.set_yticks([1, 0], [v[0] for v in vals], fontsize=8)
    m = max([abs(v[1]) for v in vals if v[1] is not None] + [12])
    ax.set_xlim(-m - 3, m + 3); ax.set_ylim(-0.6, 1.6)
    ax.set_xlabel("Mean u(J1) − u(J2), points on the 0–100 unit scale", fontsize=9)
    ax.tick_params(axis="x", labelsize=8.5)
    fig.subplots_adjust(top=0.72, bottom=0.2, left=0.30, right=0.97)
    _header(fig, 4, "Recognition and omnibus units judged validly by both judges, both saying the text refers to the brand.",
            "Δ = own minus other; confirmed if |Δ| ≤ 5 points, falsified if |Δ| ≥ 10.")
    _save(fig, 4, f"H9: {V['VERDICTS']['H9']} — Δ = {_f(h9.get('delta_points'), VV.sf1)} points", V["prereg_tag"], out)


def chart_05(V, out):
    base = V["descriptives"]["baseline"]
    order = sorted(base, key=lambda b: ({"R": 0, "F": 1, "E": 2}[b["block"]], b["category"], b["wave"]), reverse=True)
    fig, ax = plt.subplots(figsize=(7.5, 7.6))
    col = {"R": cs.PALETTE["warm"], "F": cs.INDIGO, "E": cs.PALETTE["teal_t1"]}
    labels = []
    for y, b in enumerate(order):
        name = VV.CAT_SHORT.get(b["category"], b["category"]) if b["block"] != "E" else VV.EARLY_SHORT.get(
            b["category"], b["category"])
        blk = {"R": "Recognition", "F": "Omnibus", "E": "Early"}[b["block"]]
        labels.append(f"{blk} · {name} · {b['wave']}")
        s = b.get("S")
        if not s:
            ax.text(50, y, "no rated brand", fontsize=7, color=cs.GRAY, va="center", ha="center")
            continue
        ax.plot([s["q25"], s["q75"]], [y, y], color=col[b["block"]], lw=4, alpha=0.55, solid_capstyle="butt")
        ax.plot([s["min"], s["max"]], [y, y], color=col[b["block"]], lw=0.7, alpha=0.8)
        ax.scatter([s["median"]], [y], s=22, color=col[b["block"]], zorder=3, edgecolor="white", linewidth=0.4)
        ax.text(101, y, f"{b['brands_rated']}/{b['brands']}", fontsize=6.6, va="center", color=cs.GRAY)
    ax.axvline(50, color=cs.PALETTE["gray_light"], lw=0.8, ls=":", zorder=1)
    ax.set_yticks(range(len(order)), labels, fontsize=7.2)
    ax.set_xlim(0, 108)
    ax.set_xlabel("S (0–100; 50 = neutral)", fontsize=9)
    ax.tick_params(axis="x", labelsize=8.5)
    fig.subplots_adjust(top=0.88, bottom=0.08, left=0.33, right=0.97)
    _header(fig, 5, "Dot = median; thick bar = interquartile range; thin line = range; right: rated / brands.",
            "J1 scores; brands with at least six valid units. Dotted: S = 50.")
    _save(fig, 5, "", V["prereg_tag"], out)


def main(argv=None):
    global WATERMARK
    ap = argparse.ArgumentParser(description="v1.11 Sentiment Paper A figures")
    ap.add_argument("--outputs", type=Path, default=VV.OUTDIR)
    ap.add_argument("--out", type=Path, default=ROOT / "reports/figs/v111")
    ap.add_argument("--watermark", default=None)
    a = ap.parse_args(argv)
    src = VV.load_sources(a.outputs)
    V = src["verdicts"]
    if VV.is_synthetic(src) and not a.watermark:
        print("[v1.11 charts] REFUSED: synthetic outputs need --watermark", file=sys.stderr)
        return 2
    if not VV.is_synthetic(src) and a.watermark:
        print("[v1.11 charts] REFUSED: --watermark is for synthetic runs only", file=sys.stderr)
        return 2
    WATERMARK = a.watermark
    print(f"building v1.11 figures -> {a.out}")
    for fn in (chart_01, chart_02, chart_03, chart_04, chart_05):
        fn(V, a.out)
    print("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
