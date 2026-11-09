#!/usr/bin/env python3
"""
v0.41 Long-Horizon Stability t1->t2->t3 — figure builder (paper + report registers).
Forked from build_charts_v34.py; house style via scripts/chart_style.py.

  chart_01_phi_t2_t3           H_Phi_LongHorizon        (PRIMARY, CONFIRMED)
  chart_02_presence_t2_t3      H_Presence_LongHorizon   (PRIMARY, CONFIRMED)
  chart_03_horizon             H_Horizon_Decay          (SECONDARY, MARGINAL / MARGINAL)
  chart_04_drift_dissociation  H_Drift_Dissociation     (SECONDARY, CONFIRMED)

Inputs (locked at tag v0.41-scoring-locked): osf/v41/v41_verdicts.json (every verdict,
rho, p and n shown) and osf/v41/v41_three_wave_table.csv (per-brand points). Nothing is
re-scored here. The only new numbers are DESCRIPTIVE 95% bootstrap intervals for the
per-horizon rho in chart 3 (brand units resampled within substrate, 2,000 resamples,
seed 410046), labelled as such; the hypothesis CIs on D come from the verdicts.

Outputs: reports/figs/v41/chart_0N_<topic>.pdf (+ _preview.png) and
reports/figs/v41/report/report_fig_0N.pdf.
"""
import csv
import json
import os
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(os.environ.get("AIAS_ROOT", str(Path.home() / "aias")))
sys.path.insert(0, str(ROOT / "scripts"))
import chart_style as cs  # noqa: E402
cs.setup()

SOURCE_PHASE = "v0.41 (Long-Horizon Stability t1→t2→t3)"
PROTOCOL = "v0.41-prereg-r1"
OUT = {"paper": ROOT / "reports/figs/v41", "report": ROOT / "reports/figs/v41/report"}
for _d in OUT.values():
    _d.mkdir(parents=True, exist_ok=True)
MODE = "paper"

OMNI = ["v0.19", "v0.20", "v0.21", "v0.22", "v0.23"]
CAT = {"v0.19": "headphones", "v0.20": "skincare", "v0.21": "cosmetics",
       "v0.22": "automotive", "v0.23": "spirits"}
SUBCOL = {"v0.19": cs.PALETTE["indigo"], "v0.20": cs.PALETTE["warm"], "v0.21": cs.PALETTE["teal_t2"],
          "v0.22": cs.PALETTE["blue"], "v0.23": cs.PALETTE["magenta"]}

V = json.load(open(ROOT / "osf/v41/v41_verdicts.json"))
H = V["verdicts"]


def _num(x):
    return None if x in ("", None) else float(x)


ROWS = list(csv.DictReader(open(ROOT / "osf/v41/v41_three_wave_table.csv", newline="")))
W = {}
for r in ROWS:
    W.setdefault(r["wave"], {}).setdefault(r["substrate"], {})[r["brand"]] = {
        "phi": _num(r["phi"]), "pi_hat": _num(r["pi_hat"]), "J": _num(r["J"]), "C_P": _num(r["C_P"])}

META = {
    1: {"paper": "chart_01_phi_t2_t3", "report": "report_fig_01",
        "paper_v": "H_Phi_LongHorizon: CONFIRMED — ρ = {rho:.2f} (n = {n}), p_perm = {p:.4f}, p_frame = {pf:.4f}",
        "report_v": "P1 SUPPORTED — which brands the AI models agree on stayed the same over five months, beyond what the questions alone explain."},
    2: {"paper": "chart_02_presence_t2_t3", "report": "report_fig_02",
        "paper_v": "H_Presence_LongHorizon: CONFIRMED — ρ of at least 0.70 in 5/5 substrates (range {lo:.2f}–{hi:.2f})",
        "report_v": "P2 SUPPORTED — how often each brand is named kept its order in every category over five months."},
    3: {"paper": "chart_03_horizon", "report": "report_fig_03",
        "paper_v": "H_Horizon_Decay: MARGINAL (φ, D = {dphi:+.3f}) / MARGINAL (π̂, D = {dpi:+.3f}) — no detectable decay",
        "report_v": "P3 NO FADING DETECTED — five months was as stable as three weeks, for both scores."},
    4: {"paper": "chart_04_drift_dissociation", "report": "report_fig_04",
        "paper_v": "H_Drift_Dissociation: CONFIRMED — ρ(change in φ rank, change in π̂ rank) = {rho:+.3f} (n = {n}, p = {p:.3f})",
        "report_v": "P4 SUPPORTED — when a brand's consistency changes, its presence does not change with it: two separate signals."},
    5: {"paper": None, "report": "report_fig_05", "paper_v": "",
        "report_v": "P5 OBSERVED — almost every brand AI rarely named in June was still rarely named in November (descriptive)."},
}


REPORT_TITLE = {   # report register: describe the chart; never restate the finding's headline
    "Consistency keeps its brand order over five months": "Consistency score, June against November",
    "Presence keeps its brand order in every category": "Presence, June against November, by category",
    "Five months is as stable as three weeks": "Rank stability over three time spans",
    "Consistency and Presence change independently": "Change in Consistency against change in Presence",
}


def _header(fig, title, subtitle, desc=""):
    cs.add_header(fig, REPORT_TITLE.get(title, title) if MODE == "report" else title, subtitle, desc)


def _save(fig, key, **fmt):
    m = META[key]
    verdict = (m["paper_v"] if MODE == "paper" else m["report_v"]).format(**fmt)
    cs.add_footer(fig, verdict=verdict, phase=SOURCE_PHASE, protocol=PROTOCOL)
    fig.savefig(OUT[MODE] / f"{m[MODE]}.pdf", **cs.SAVEFIG_PARAMS)
    if MODE == "paper":
        fig.savefig(OUT[MODE] / f"{m[MODE]}_preview.png", dpi=120, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    print(f"  [{MODE}] wrote {m[MODE]}.pdf")


def _ranks(a):
    a = np.asarray(a, float)
    order = a.argsort(kind="mergesort")
    r = np.empty(len(a))
    r[order] = np.arange(1, len(a) + 1)
    for v in np.unique(a):                      # average ties
        m = a == v
        if m.sum() > 1:
            r[m] = r[m].mean()
    return r


def _pearson(x, y):
    x = x - x.mean(); y = y - y.mean()
    d = np.sqrt((x * x).sum() * (y * y).sum())
    return float((x * y).sum() / d) if d > 0 else float("nan")


def _within(v, g):
    v = np.asarray(v, float); g = np.asarray(g)
    out = np.empty(len(v))
    for s in dict.fromkeys(g):
        i = np.where(g == s)[0]
        out[i] = _ranks(v[i])
    return out


def _pairs(metric, a, b):
    xs, ys, gs = [], [], []
    for s in OMNI:
        for br, m in W[a][s].items():
            n = W[b][s].get(br)
            if n and m[metric] is not None and n[metric] is not None:
                xs.append(m[metric]); ys.append(n[metric]); gs.append(s)
    return np.array(xs), np.array(ys), np.array(gs)


def _stat(metric, x, y, g):
    if metric in ("phi", "J"):
        return _pearson(_ranks(x), _ranks(y))
    return _pearson(_within(x, g), _within(y, g))


# ============================================================ fig1
def chart_01():
    h = H["H_Phi_LongHorizon"]; fn = h["frame_structure_null"]
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    for s in OMNI:
        x, y, _ = _pairs("phi", "t2", "t3")
        x, y, g = _pairs("phi", "t2", "t3")
        m = g == s
        ax.scatter(x[m], y[m], s=30, color=SUBCOL[s], alpha=0.85, edgecolor="white", linewidth=0.4,
                   zorder=3, label=f"{s} {CAT[s]} (n = {int(m.sum())})")
    lim = 4.2                                    # one brand sits at phi_max = 7.2 in both waves
    off = (x > lim) | (y > lim)
    ax.plot([0, lim], [0, lim], color=cs.PALETTE["gray_light"], lw=0.8, ls="--", zorder=1)
    ax.set_xlim(0, lim); ax.set_ylim(0, lim)
    if off.any():
        ax.text(0.97, 0.66, f"{int(off.sum())} brand off scale:\nφ = {x[off][0]:.1f} in both waves",
                transform=ax.transAxes, ha="right", va="top", fontsize=7.2, color=cs.GRAY, fontstyle="italic")
    ax.set_xlabel("φ at t₂ (June 2026)   ← more consistent across models", fontsize=9)
    ax.set_ylabel("φ at t₃ (November 2026)", fontsize=9)
    ax.tick_params(labelsize=8.5)
    ax.legend(loc="lower right", fontsize=7.6, frameon=False)
    ax.text(0.03, 0.97,
            f"ρ = {h['rho']:.2f}   (n = {h['n']})\n"
            f"criterion: at least 0.50\n"
            f"frame-structure null: mean {fn['null_mean']:.2f}, 95th pct {fn['null_p95']:.2f}\n"
            f"p_perm = {h['p_perm']:.4f}   p_frame = {fn['p_frame']:.4f}",
            transform=ax.transAxes, ha="left", va="top", fontsize=8, color=cs.INDIGO,
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=cs.INDIGO, lw=0.6))
    fig.subplots_adjust(top=0.80, bottom=0.17, left=0.10, right=0.97)
    _header(fig, "Consistency keeps its brand order over five months",
                  "Per-brand φ (between-model dispersion; lower = more consistent), June vs November 2026, φ defined in both waves.",
                  "The order beats both nulls: shuffled brands and models scrambled within each question. Dashed: no change.")
    _save(fig, 1, rho=h["rho"], n=h["n"], p=h["p_perm"], pf=fn["p_frame"])


# ============================================================ fig2
def chart_02():
    h = H["H_Presence_LongHorizon"]; ps = h["per_substrate"]
    if MODE == "report":
        fig, grid = plt.subplots(2, 3, figsize=(7.5, 5.6))
        axes = list(grid.flat)
        axes[5].axis("off")
    else:
        fig, axes = plt.subplots(1, 5, figsize=(8.6, 3.3))
    for ax, s in zip(axes, OMNI):
        xs, ys = [], []
        for br, m in W["t2"][s].items():
            n = W["t3"][s].get(br)
            if n:
                xs.append(m["pi_hat"]); ys.append(n["pi_hat"])
        rho = ps[s]["rho"]
        ax.plot([0, 1], [0, 1], color=cs.PALETTE["gray_light"], lw=0.8, ls="--", zorder=1)
        ax.scatter(xs, ys, s=24, color=cs.INDIGO, alpha=0.8, edgecolor="white", linewidth=0.4, zorder=3)
        ax.set_xlim(-0.02, 1.02); ax.set_ylim(-0.02, 1.02)
        ax.set_xticks([0, 0.5, 1.0]); ax.set_yticks([0, 0.5, 1.0]); ax.tick_params(labelsize=6.5)
        ax.set_title(f"{s} {CAT[s]}", fontsize=7.6, fontweight="bold", color=cs.INDIGO, pad=4)
        ax.text(0.04, 0.96, f"ρ={rho:.2f}\nn={ps[s]['n']}", transform=ax.transAxes, ha="left", va="top",
                fontsize=6.8, color=cs.INDIGO, bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=cs.INDIGO, lw=0.6))
        if MODE == "report":
            if s in ("v0.19", "v0.22"):
                ax.set_ylabel("November", fontsize=8)
            ax.set_xlabel("June", fontsize=7.5)
            ax.tick_params(labelsize=7.5)
        else:
            if s == "v0.19":
                ax.set_ylabel("recall share π̂, t₃", fontsize=8)
            ax.set_xlabel("t₂", fontsize=7.5)
    if MODE == "report":
        axes[5].text(0.05, 0.55, "Each dot is one brand.\nOn the dashed line, its share\nwas the same in both months.",
                     transform=axes[5].transAxes, fontsize=8, color=cs.GRAY, va="center")
        fig.subplots_adjust(top=0.78, bottom=0.14, left=0.08, right=0.985, wspace=0.32, hspace=0.42)
    else:
        fig.subplots_adjust(top=0.60, bottom=0.26, left=0.06, right=0.985, wspace=0.32)
    _header(fig, "Presence keeps its brand order in every category",
                  "Per-brand recall share π̂ (share of the 36 model × question answers that name the brand), June vs November.",
                  "Criterion: ρ of at least 0.70 in at least four of five categories; all five pass.")
    vals = [ps[s]["rho"] for s in OMNI]
    _save(fig, 2, lo=min(vals), hi=max(vals))


# ============================================================ fig3
def chart_03():
    hd = H["H_Horizon_Decay"]
    metrics = [("phi", "φ (consistency)"), ("J", "J (positional overlap)"),
               ("pi_hat", "π̂ (recall presence)"), ("C_P", "C_P (recognition)")]
    horizons = [("t1", "t2", "t₁→t₂  (15–21 days)", cs.PALETTE["indigo_t2"]),
                ("t2", "t3", "t₂→t₃  (152 days)", cs.INDIGO),
                ("t1", "t3", "t₁→t₃  (167–173 days)", cs.WARM)]
    rng = np.random.default_rng(410046)
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    for i, (mk, ml) in enumerate(metrics):
        for j, (a, b, hl, col) in enumerate(horizons):
            x, y, g = _pairs(mk, a, b)
            rho = _stat(mk, x, y, g)
            gi = [np.where(g == s)[0] for s in OMNI if (g == s).any()]
            boots = []
            for _ in range(2000):
                idx = np.concatenate([rng.choice(k, len(k), replace=True) for k in gi])
                v = _stat(mk, x[idx], y[idx], g[idx])
                if np.isfinite(v):
                    boots.append(v)
            lo, hi = np.percentile(boots, [2.5, 97.5])
            xpos = i + (j - 1) * 0.22
            ax.errorbar(xpos, rho, yerr=[[rho - lo], [hi - rho]], fmt="o", color=col, ms=6,
                        capsize=2.5, lw=1.1, zorder=3, label=hl if i == 0 else None)
            ax.text(xpos, hi + 0.015, f"{rho:.2f}", ha="center", va="bottom", fontsize=6.6, color=col)
    ax.set_xticks(range(len(metrics))); ax.set_xticklabels([m for _, m in metrics], fontsize=8.5)
    ax.set_ylim(0.3, 1.08); ax.set_ylabel("rank stability ρ", fontsize=9); ax.tick_params(axis="y", labelsize=8.5)
    ax.axhline(0.50, color=cs.GRAY, lw=0.8, ls=":", zorder=1)
    ax.legend(loc="lower left", fontsize=7.6, frameon=False)
    ax.text(0.99, 0.03,
            f"D = ρ(t₁,t₂) − ρ(t₁,t₃), three-wave sets:\n"
            f"φ  {hd['phi']['D']:+.3f}  [{hd['phi']['ci95'][0]:+.2f}, {hd['phi']['ci95'][1]:+.2f}]   n = {hd['phi']['n']}\n"
            f"π̂  {hd['pi_hat']['D']:+.3f}  [{hd['pi_hat']['ci95'][0]:+.2f}, {hd['pi_hat']['ci95'][1]:+.2f}]   n = {hd['pi_hat']['n']}",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=7.6, color=cs.INDIGO,
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=cs.INDIGO, lw=0.6))
    fig.subplots_adjust(top=0.80, bottom=0.14, left=0.09, right=0.97)
    _header(fig, "Five months is as stable as three weeks",
                  "Rank stability by horizon for four instruments; whiskers = descriptive 95% bootstrap intervals (2,000 resamples).",
                  "φ and J: pooled Spearman; π̂ and C_P: pooled within-category ranks. Pairwise definedness per horizon.")
    _save(fig, 3, dphi=hd["phi"]["D"], dpi=hd["pi_hat"]["D"])


# ============================================================ fig4
def chart_04():
    h = H["H_Drift_Dissociation"]
    x2, x3, g = _pairs("phi", "t2", "t3")
    keys = [(s, br) for s in OMNI for br, m in W["t2"][s].items()
            if br in W["t3"][s] and m["phi"] is not None and W["t3"][s][br]["phi"] is not None]
    p2 = np.array([W["t2"][s][br]["pi_hat"] for s, br in keys]); p3 = np.array([W["t3"][s][br]["pi_hat"] for s, br in keys])
    gg = np.array([s for s, _ in keys])
    n_s = np.array([np.sum(gg == s) for s in gg], float)
    dphi = _within(x3, gg) / n_s - _within(x2, gg) / n_s
    dpi = _within(p3, gg) / n_s - _within(p2, gg) / n_s
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    for s in OMNI:
        m = gg == s
        ax.scatter(dpi[m], dphi[m], s=30, color=SUBCOL[s], alpha=0.85, edgecolor="white", linewidth=0.4,
                   zorder=3, label=f"{s} {CAT[s]}")
    ax.axhline(0, color=cs.PALETTE["gray_light"], lw=0.8, zorder=1)
    ax.axvline(0, color=cs.PALETTE["gray_light"], lw=0.8, zorder=1)
    ax.set_xlabel("change in Presence rank (within category, t₂→t₃)", fontsize=9)
    ax.set_ylabel("change in φ rank (within category, t₂→t₃)", fontsize=9)
    ax.tick_params(labelsize=8.5)
    ax.legend(loc="lower right", fontsize=7.6, frameon=False)
    ax.text(0.03, 0.97,
            f"ρ = {h['rho']:+.3f}   (n = {h['n']}, p = {h['p_perm_two_sided']:.3f})\n"
            f"confirmed band: |ρ| at most 0.30\n"
            f"t₂ baseline coupling ρ(φ, π̂) = {h['baseline_coupling_t2_rho']:+.2f} (descriptive)",
            transform=ax.transAxes, ha="left", va="top", fontsize=8, color=cs.INDIGO,
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=cs.INDIGO, lw=0.6))
    fig.subplots_adjust(top=0.80, bottom=0.18, left=0.10, right=0.97)
    _header(fig, "Consistency and Presence change independently",
                  "Per-brand change in within-category percentile rank, June to November, brands with φ defined in both waves.",
                  "No relationship: a brand gaining or losing presence does not gain or lose consistency with it.")
    _save(fig, 4, rho=h["rho"], n=h["n"], p=h["p_perm_two_sided"])


# ============================================================ fig5 (report register only)
def chart_05():
    h = H["H_Phantom_LongPersistence"]; ps = h["per_substrate"]; po = h["pooled"]
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    ys = np.arange(len(OMNI))[::-1]
    for y, s in zip(ys, OMNI):
        n, k = ps[s]["t2_phantom"], ps[s]["retained_t3"]
        ax.barh(y, k, color=cs.INDIGO, height=0.55, zorder=2)
        if n > k:
            ax.barh(y, n - k, left=k, color=cs.WARM, height=0.55, zorder=2)
        ax.text(n + 0.3, y, f"{k} of {n}", va="center", fontsize=8.5, color=cs.INDIGO)
    ax.set_yticks(ys); ax.set_yticklabels([f"{s} {CAT[s]}" for s in OMNI], fontsize=8.5)
    ax.set_xlim(0, 23); ax.set_xlabel("brands below the recall floor in June", fontsize=8.5)
    ax.tick_params(axis="x", labelsize=8)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=cs.INDIGO, label="still below it in November"),
                       Patch(color=cs.WARM, label="above it in November")], loc="upper center", bbox_to_anchor=(0.45, -0.2), ncol=2, fontsize=7.8, frameon=False)
    ax.text(0.99, 0.42, f"pooled: {po['retained_t3']} of {po['t2_phantom']} ({100 * po['proportion']:.0f}%)\n"
            f"May to June, three weeks: {h['v0_34_reference_t1_t2'].replace('/', ' of ')}", transform=ax.transAxes, ha="right", va="center",
            fontsize=8, color=cs.INDIGO, bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=cs.INDIGO, lw=0.6))
    fig.subplots_adjust(top=0.76, bottom=0.27, left=0.21, right=0.97)
    cs.add_header(fig, "Brands below the recall floor, June and November",
                  "Brands averaging under one mention per model in June, and whether they were still below that in November.",
                  "Descriptive: no pass mark was set.")
    _save(fig, 5)


if __name__ == "__main__":
    print("building v0.41 figures (dual register) -> reports/figs/v41/{,report/}")
    for _m in ("paper", "report"):
        MODE = _m
        chart_01(); chart_02(); chart_03(); chart_04()
        if MODE == "report":
            chart_05()
    print("done")
