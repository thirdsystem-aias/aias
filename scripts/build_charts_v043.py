#!/usr/bin/env python3
"""
v0.43 Stage 1 (predictive validity on past data) -- figure builder (paper register only: no brand-format report).
House style of build_charts_v112.py (scripts/chart_style.py: bold title top-left, gray subtitle, thin Indigo rule,
italic gray source line citing the pre-registration tag). Every number comes from the scorer's output.

One chart per pre-registered finding (PRE_REGISTRATION_v0_43.md sections 2.2, 2.3, 2.7, 2.8):
  chart_01_checks                      MC_Concurrent and MC_PullReliability
  chart_02_presence_change             H_Pred_Presence (primary)
  chart_03_tests_intervals             the four Stage 1 tests against the verdict thresholds
  chart_04_presence_change_sa          H_Pred_Presence_SA
  chart_05_presence_change_momentum    H_Pred_Presence_Momentum
  chart_06_consistency_change          H_Pred_Consistency
  chart_07_per_category                descriptive 1 (every test per category)
  chart_08_descriptives                descriptives 2-6

Input: --verdicts (osf/v43/v43_stage1_verdicts.json, written by `score_v0_43.py --stage 1`). Nothing is re-scored:
the residual-rank scatters use the scorer's own rho_pw on the scorer's unit table, and the builder refuses unless
papers/v0_43/v043_values.check_consistency() passes (which includes: each test's rho recomputed from the unit table
equals the verdicts' rho). Statistics printed on charts are verdicts-JSON leaves formatted by v043_values. Chart titles
describe what is plotted and never repeat a finding's or a section's title (CLAUDE.md). --watermark TEXT stamps every
chart (synthetic runs only; required for them, refused for real ones).

Usage (real run):  python3 scripts/build_charts_v043.py
Synthetic test:    python3 scripts/build_charts_v043.py --verdicts F.json --out /tmp/x/figs \
                       --watermark "SYNTHETIC TEST — NOT RESULTS"
"""
import argparse
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "papers/v0_43"))
import chart_style as cs  # noqa: E402
import v043_values as VV  # noqa: E402
cs.setup()

SUBCOL = {"v0.19": cs.PALETTE["indigo"], "v0.20": cs.PALETTE["warm"], "v0.21": cs.PALETTE["teal_t2"],
          "v0.22": cs.PALETTE["blue"], "v0.23": cs.PALETTE["magenta"]}
SOURCE = ("Source: AIAS™ v0.43, Stage 1 | pre-registration {tag} | search interest: Google Trends via SerpAPI | "
          "scores: Methodology v1.9, t₂ | Third System™")
WATERMARK = None
TITLES = {
    1: "Presence against search level, and agreement between pulls",
    2: "Residual ranks: Presence score against change in search interest",
    3: "Partial rank correlations of the four tests, with bootstrap intervals",
    4: "Residual ranks: Presence score against year-on-year-adjusted change",
    5: "Residual ranks: Presence score against change, after level and earlier trend",
    6: "Residual ranks: Consistency C* against change, after level and Presence",
    7: "Single-category partial rank correlations, by test",
    8: "Variants of the Presence test and a cross-lagged comparison",
}
NAMES = {1: "chart_01_checks", 2: "chart_02_presence_change", 3: "chart_03_tests_intervals",
         4: "chart_04_presence_change_sa", 5: "chart_05_presence_change_momentum", 6: "chart_06_consistency_change",
         7: "chart_07_per_category", 8: "chart_08_descriptives"}
TEST_LABEL = {"H_Pred_Presence": "Presence → change (primary)", "H_Pred_Presence_SA": "Presence → adjusted change",
              "H_Pred_Presence_Momentum": "Presence → change, trend controlled",
              "H_Pred_Consistency": "Consistency → change, Presence controlled"}


def _header(fig, key, subtitle, desc=""):
    cs.add_header(fig, TITLES[key], subtitle, desc)
    y = 1.0 - (0.74 / fig.get_figheight())
    fig.add_artist(Line2D([cs.LEFT_X, 0.985], [y, y], transform=fig.transFigure, color=cs.INDIGO, lw=0.6))


def _save(fig, key, verdict, out):
    _, _, _, vy, sy = cs._compute_positions(fig)
    if verdict:
        fig.text(cs.LEFT_X, vy, verdict, fontsize=cs.FONT_SIZES["verdict"], color=cs.INDIGO, fontstyle="italic",
                 ha="left", va="bottom")
    fig.text(cs.LEFT_X, sy, SOURCE.format(tag=VV.EXPECTED_PREREG_TAG), fontsize=cs.FONT_SIZES["source"], color=cs.GRAY,
             fontstyle="italic", ha="left", va="bottom")
    if WATERMARK:
        fig.text(0.5, 0.5, WATERMARK, rotation=28, fontsize=30, color=cs.WARM, alpha=0.22, ha="center",
                 va="center", fontweight="bold", zorder=100)
    out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out / f"{NAMES[key]}.pdf", **cs.SAVEFIG_PARAMS)
    fig.savefig(out / f"{NAMES[key]}_preview.png", dpi=110, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    print(f"  wrote {out / (NAMES[key] + '.pdf')}")


def _box(ax, text, x=0.03, y=0.97, ha="left", va="top", fs=7.4):
    ax.text(x, y, text, transform=ax.transAxes, ha=ha, va=va, fontsize=fs, color=cs.INDIGO,
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=cs.INDIGO, lw=0.6), zorder=5)


def _word(T):
    return T["verdict"] + (" (REVERSED)" if "REVERSED" in (T.get("labels") or []) else "")


def _stat_text(T):
    if not VV.finite(T.get("rho")):
        return f"n = {T.get('n')}: statistic not computed\n{_word(T)}"
    s = f"ρ = {VV.r3(T['rho'])}   n = {T['n']}"
    if VV.has(T, ["ci90", 1]):
        s += f"\n90% interval [{VV.r3(T['ci90'][0])}, {VV.r3(T['ci90'][1])}]"
    if VV.finite(T.get("p_one")):
        s += f"\none-sided p = {VV.p4(T['p_one'])}"
        if "REVERSED" in (T.get("labels") or []):
            s += f"   two-sided p = {VV.p4(T['p_two'])}"
    return s


def resid_scatter(V, key, name, xlabel, ylabel, subtitle, desc, out):
    T = V["tests"][name]
    spec = (T["spec"]["x"], T["spec"]["y"], T["spec"]["controls"])
    rho, n, res = VV.recompute_rho(V, spec)
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    allx, ally = [], []
    for s, ry, rx in res:
        ax.scatter(rx, ry, s=26, color=SUBCOL[s], alpha=0.85, edgecolor="white", linewidth=0.4, zorder=3,
                   label=f"{VV.CAT[s]} (n = {len(rx)})")
        allx += list(rx)
        ally += list(ry)
    ax.axhline(0, color=cs.PALETTE["gray_light"], lw=0.8, zorder=1)
    ax.axvline(0, color=cs.PALETTE["gray_light"], lw=0.8, zorder=1)
    if VV.finite(rho) and len(allx) > 2 and np.std(allx) > 0:
        xs = np.array(allx)
        slope = np.dot(xs - xs.mean(), np.array(ally) - np.mean(ally)) / np.dot(xs - xs.mean(), xs - xs.mean())
        lim = np.array([xs.min(), xs.max()])
        ax.plot(lim, np.mean(ally) + slope * (lim - xs.mean()), color=cs.INDIGO, lw=1.0, ls="--", zorder=2)
    else:
        ax.text(0.5, 0.5, "statistic not computed on these data", transform=ax.transAxes, ha="center", fontsize=9,
                color=cs.GRAY)
    ax.set_xlabel(xlabel, fontsize=9)
    ax.set_ylabel(ylabel, fontsize=9)
    ax.tick_params(labelsize=8.5)
    if res:
        ax.legend(loc="center left", bbox_to_anchor=(1.01, 0.5), fontsize=7.2, frameon=False)
    _box(ax, _stat_text(T))
    fig.subplots_adjust(top=0.80, bottom=0.17, left=0.10, right=0.74)
    _header(fig, key, subtitle, desc)
    _save(fig, key, f"{name}: {_word(T)}", out)


def chart_01(V, out):
    mc = V["manipulation_checks"]
    c, rel = mc["MC_Concurrent"], mc["MC_PullReliability"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=cs.FIGSIZE["hero"], gridspec_kw={"width_ratios": [1.5, 1]})
    _, _, res = VV.recompute_rho(V, ("P", "Lc", []), [dict(r, Lc=r["L"]) for r in V["unit_table"]])
    for s, ry, rx in res:
        a1.scatter(rx, ry, s=18, color=SUBCOL[s], alpha=0.85, edgecolor="white", linewidth=0.3, zorder=3,
                   label=VV.CAT_SHORT[s])
    a1.axhline(0, color=cs.PALETTE["gray_light"], lw=0.8)
    a1.axvline(0, color=cs.PALETTE["gray_light"], lw=0.8)
    a1.set_xlabel("June Presence P (rank, centred in category)", fontsize=8.5)
    a1.set_ylabel("search level, May–June (rank, centred)", fontsize=8.5)
    a1.tick_params(labelsize=8)
    a1.legend(loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=5, fontsize=6.4, frameon=False,
              handletextpad=0.2, columnspacing=0.8)
    if VV.finite(c.get("rho")):
        _box(a1, f"ρ = {VV.r3(c['rho'])}   n = {c['n']}\none-sided p = {VV.p4(c['p_one'])}\n"
                 f"{'passed' if c['pass_'] else 'failed'} (at least 0.30 required)", fs=7)
    pairs = rel.get("pairs") or []
    lab = ["pulls 1–2", "pulls 1–3", "pulls 2–3"][:len(pairs)]
    a2.bar(range(len(pairs)), pairs, color=cs.PALETTE["indigo_t2"], width=0.6, zorder=2)
    for i, p in enumerate(pairs):
        a2.text(i, p + 0.02, VV.r3(p), ha="center", va="bottom", fontsize=7.5, color=cs.INDIGO)
    a2.axhline(0.70, color=cs.WARM, lw=0.9, ls=":", zorder=3)
    a2.text(1.01, 0.70, "0.70", color=cs.WARM, fontsize=7.5, ha="left", va="center",
            transform=a2.get_yaxis_transform())
    a2.set_xticks(range(len(pairs)))
    a2.set_xticklabels(lab, fontsize=8)
    a2.set_ylim(min(0.0, min(pairs) - 0.05) if pairs else 0, 1.08)
    a2.set_ylabel("pooled within-category Spearman of per-pull change", fontsize=8)
    a2.tick_params(labelsize=8)
    m = rel.get("mean_pairwise_pooled_spearman")
    a2.set_title(f"mean {VV.r3(m) if VV.finite(m) else 'not computable'}: "
                 f"{'passed' if rel['pass_'] else 'failed'}", fontsize=8, color=cs.INDIGO, loc="left")
    fig.subplots_adjust(top=0.78, bottom=0.24, left=0.08, right=0.95, wspace=0.34)
    _header(fig, 1, "Left: one point per brand (MC_Concurrent). Right: the three pairs of pulls (MC_PullReliability).",
            "Pre-registration §2.7; seed 430049.")
    _save(fig, 1, f"flags: {', '.join(V['flags']) if V['flags'] else 'none'}", out)


def chart_03(V, out):
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero_short"])
    ax.axvline(0, color=cs.PALETTE["gray_light"], lw=0.8, zorder=1)
    ax.axvline(0.15, color=cs.PALETTE["teal_t2"], lw=0.9, ls="--", zorder=1)
    ax.axvline(0.10, color=cs.WARM, lw=0.9, ls=":", zorder=1)
    ys = list(range(len(VV.TESTS), 0, -1))
    for y, name in zip(ys, VV.TESTS):
        T = V["tests"][name]
        col = cs.INDIGO if name == "H_Pred_Presence" else cs.PALETTE["indigo_t1"]
        if VV.has(T, ["ci95", 1]):
            ax.plot(T["ci95"], [y, y], color=col, lw=1.0, zorder=2)
        if VV.has(T, ["ci90", 1]):
            ax.plot(T["ci90"], [y, y], color=col, lw=3.2, zorder=2, solid_capstyle="butt")
        if VV.finite(T.get("rho")):
            ax.scatter([T["rho"]], [y], s=42, color="white", edgecolor=col, linewidth=1.4, zorder=3)
        ax.text(1.02, y, f"{_word(T)}  (n = {T['n']})", transform=ax.get_yaxis_transform(), fontsize=7.4,
                va="center", ha="left", color=col)
    ax.set_yticks(ys)
    ax.set_yticklabels([TEST_LABEL[n] for n in VV.TESTS], fontsize=8)
    ax.set_ylim(0.4, len(VV.TESTS) + 0.6)
    ax.set_xlim(-0.8, 0.8)
    ax.set_xlabel("ρ, pooled within-category partial Spearman (thick: 90% interval; thin: 95%)", fontsize=8.5)
    ax.tick_params(labelsize=8)
    fig.subplots_adjust(top=0.72, bottom=0.22, left=0.33, right=0.75)
    _header(fig, 3, "Dashed: confirmation needs ρ of at least 0.15 (with p < 0.05). Dotted: falsified if the 90% "
                    "interval ends below 0.10.", "")
    _save(fig, 3, "Verdict rule: pre-registration §2.1", out)


def chart_07(V, out):
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero_tall"])
    ax.axvline(0, color=cs.PALETTE["gray_light"], lw=0.8, zorder=1)
    ys = list(range(len(VV.TESTS), 0, -1))
    off = {s: (2 - i) * 0.16 for i, s in enumerate(VV.SUBS)}
    for y, name in zip(ys, VV.TESTS):
        for s in VV.SUBS:
            d = V["descriptives"]["per_substrate"][name].get(s) or {}
            if VV.finite(d.get("rho")):
                ax.scatter([d["rho"]], [y + off[s]], s=26, color=SUBCOL[s], zorder=3,
                           label=VV.CAT[s] if y == ys[0] else None)
                ax.text(d["rho"] + 0.035, y + off[s], f"n = {d.get('n')}", fontsize=6.0, va="center",
                        color=SUBCOL[s])
    ax.set_yticks(ys)
    ax.set_yticklabels([TEST_LABEL[n] for n in VV.TESTS], fontsize=8)
    ax.set_xlim(-1, 1)
    ax.set_ylim(0.4, len(VV.TESTS) + 0.6)
    ax.set_xlabel("ρ within one category (no bootstrap; descriptive)", fontsize=8.5)
    ax.tick_params(labelsize=8)
    ax.legend(loc="center left", bbox_to_anchor=(1.01, 0.5), fontsize=7.2, frameon=False)
    fig.subplots_adjust(top=0.84, bottom=0.12, left=0.30, right=0.76)
    _header(fig, 7, "One point per category and test; 16 to 24 brands per category.",
            "Pre-registration §2.8, item 1; seed 430050.")
    _save(fig, 7, "Descriptive: no verdicts", out)


def chart_08(V, out):
    D = V["descriptives"]
    rows = [("Primary test (reference)", V["tests"]["H_Pred_Presence"], cs.GRAY)]
    for label, path, item in VV.DESC_ROWS:
        lab = label.replace("$\\hat\\pi$", "recall rate").replace("$P$", "P").replace("$t_1$", "t₁")
        lab = lab.replace("No defunct automotive brands: ", "no defunct automotive: ")
        try:
            rows.append((f"{item}. {lab}", VV.jget(D, path), cs.INDIGO))
        except VV.Missing:
            rows.append((f"{item}. {lab}", {}, cs.INDIGO))
    xl = D.get("cross_lagged") or {}
    rows.append(("6. AI → search (P at t₂ → November level)", {"rho": xl.get("rho_AI_to_search"), "n": xl.get("n")},
                 cs.PALETTE["teal_t1"]))
    rows.append(("6. search → AI (June level → P at t₃)", {"rho": xl.get("rho_search_to_AI"), "n": xl.get("n")},
                 cs.PALETTE["teal_t1"]))
    rows.append(("6. difference (AI → search minus search → AI)",
                 {"rho": xl.get("difference"), "ci90": xl.get("difference_ci90"), "n": xl.get("n")},
                 cs.PALETTE["teal_t1"]))
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero_tall"])
    ax.axvline(0, color=cs.PALETTE["gray_light"], lw=0.8, zorder=1)
    ys = list(range(len(rows), 0, -1))
    for y, (lab, d, col) in zip(ys, rows):
        if VV.has(d, ["ci90", 1]):
            ax.plot(d["ci90"], [y, y], color=col, lw=2.6, zorder=2, solid_capstyle="butt")
        if VV.finite(d.get("rho")):
            ax.scatter([d["rho"]], [y], s=36, color="white", edgecolor=col, linewidth=1.3, zorder=3)
            ax.text(1.02, y, f"{VV.r3(d['rho'])}  (n = {d.get('n')})", transform=ax.get_yaxis_transform(),
                    fontsize=7.2, va="center", ha="left", color=col)
        else:
            ax.text(1.02, y, "not computed", transform=ax.get_yaxis_transform(), fontsize=7.2, va="center",
                    ha="left", color=cs.GRAY)
    ax.set_yticks(ys)
    ax.set_yticklabels([r[0] for r in rows], fontsize=7.6)
    ax.set_xlim(-1, 1)
    ax.set_ylim(0.4, len(rows) + 0.6)
    ax.set_xlabel("ρ, pooled within-category partial Spearman (bar: 90% bootstrap interval)", fontsize=8.5)
    ax.tick_params(labelsize=8)
    fig.subplots_adjust(top=0.84, bottom=0.12, left=0.42, right=0.82)
    _header(fig, 8, "Pre-registered descriptives 2 to 6; no verdicts. The cross-lagged comparison is exploratory.",
            "Seed 430050.")
    _save(fig, 8, "Descriptive: no verdicts", out)


def main(argv=None):
    global WATERMARK
    ap = argparse.ArgumentParser(description="v0.43 Stage 1 figures")
    ap.add_argument("--verdicts", type=Path, default=ROOT / "osf/v43/v43_stage1_verdicts.json")
    ap.add_argument("--out", type=Path, default=ROOT / "reports/figs/v043")
    ap.add_argument("--watermark", default=None)
    a = ap.parse_args(argv)
    V = json.loads(a.verdicts.read_text(encoding="utf-8"))
    syn = VV.is_synthetic(V)
    if syn and not a.watermark:
        sys.exit("[v0.43 charts] REFUSED: synthetic verdicts need --watermark")
    if not syn and a.watermark:
        sys.exit("[v0.43 charts] REFUSED: --watermark is for synthetic runs only")
    if syn and str(a.out.resolve()).startswith(str(ROOT.resolve()) + "/"):
        sys.exit("[v0.43 charts] REFUSED: synthetic figures must be written outside the repository")
    try:
        VV.check_consistency(V, real=not syn)
    except VV.Inconsistent as e:
        sys.exit(f"[v0.43 charts] REFUSED: inconsistent verdicts: {e}")
    WATERMARK = a.watermark
    print(f"building v0.43 Stage 1 figures -> {a.out}")
    chart_01(V, a.out)
    lev = "after the June search level"
    resid_scatter(V, 2, "H_Pred_Presence", f"June Presence P (residual rank, {lev})",
                  "change to November (residual rank)",
                  "One point per brand with a defined change; ranks within category, pooled.",
                  "Dashed: least-squares line through the pooled residuals; its correlation is ρ.", a.out)
    chart_03(V, a.out)
    resid_scatter(V, 4, "H_Pred_Presence_SA", f"June Presence P (residual rank, {lev})",
                  "adjusted change (residual rank)",
                  "Brands with both years defined (W(7 Jun) → W(8 Nov 2025) as the year-earlier change).",
                  "Dashed: least-squares line through the pooled residuals.", a.out)
    resid_scatter(V, 5, "H_Pred_Presence_Momentum", "June Presence P (residual rank, after level and trend)",
                  "change to November (residual rank)",
                  "Controls: June search level and the February-to-June change.",
                  "Dashed: least-squares line through the pooled residuals.", a.out)
    resid_scatter(V, 6, "H_Pred_Consistency", "June Consistency C* (residual rank, after level and P)",
                  "change to November (residual rank)",
                  "Brands with a rated C* (at least six mentions); controls: June search level and June Presence.",
                  "Dashed: least-squares line through the pooled residuals.", a.out)
    chart_07(V, a.out)
    chart_08(V, a.out)
    print("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
