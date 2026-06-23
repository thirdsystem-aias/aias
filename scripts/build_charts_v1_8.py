#!/usr/bin/env python3
"""
v1.8 CPC instrument redesign — figure builder (one per finding).
Visualizes the SEALED results (read-only) from the locked artifacts:
  chart_01_mean_independence  headline: phi-vs-mu (mean-independent) vs CV-CPC_raw-vs-mu (coupled)
  chart_02_defined_coverage   phi-defined 84 superset CV_raw 55; the 29 sub-floor gain units
  chart_03_phi_j_dissociation phi-vs-J, rho=-0.403, the 9 discordant units flagged
  chart_04_two_wave           phi(t1) vs phi(t2), rho=0.645 (recomputed read-only; asserted vs locked)

Reads osf/methodology/v1_8/v1_8_instrument_table.csv (sealed at v1.8-results-r1).
Fig 4 recomputes the t1/t2 pairs from the materialized frozen inputs (deterministic;
asserts the recomputed rho == the locked verdicts value). House style via chart_style.py.
Outputs PDFs to reports/figs/v1_8/. Does NOT modify any locked artifact.
"""
import sys, csv
from pathlib import Path
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

ROOT = Path.home() / "aias"
sys.path.insert(0, str(ROOT / "scripts"))
import chart_style as cs
cs.setup()

OUT = ROOT / "reports" / "figs" / "v1_8"; OUT.mkdir(parents=True, exist_ok=True)
SOURCE_PHASE = "v1.8 (CPC redesign)"
PROTOCOL = "v1.8-prereg-r4"
CEIL_MI, CEIL_PD = 0.50, 0.70
PI_FLOOR = 1.0 / 6.0          # CV-CPC_raw floor: mu_count >= 1.0  <=>  pi_hat >= 1/6

SUB_NAME = {"v0.19": "headphones", "v0.20": "skincare", "v0.21": "cosmetics",
            "v0.22": "automotive", "v0.23": "premium spirits"}
SUB_COLOR = {"v0.19": cs.INDIGO, "v0.20": cs.WARM, "v0.21": cs.TEAL,
             "v0.22": cs.PALETTE["blue"], "v0.23": cs.PALETTE["green"]}
SUBS = ["v0.19", "v0.20", "v0.21", "v0.22", "v0.23"]


def _f(v):
    return float(v) if v not in ("", "None") else None

rows = list(csv.DictReader(open(ROOT / "osf/methodology/v1_8/v1_8_instrument_table.csv")))
for r in rows:
    r["pi_hat"] = _f(r["pi_hat"]); r["mu"] = _f(r["mu"]); r["phi"] = _f(r["phi"])
    r["J"] = _f(r["J"]); r["cpc_raw"] = _f(r["cpc_raw"])
    r["phi_defined"] = r["phi_defined"] == "True"
    r["J_defined"] = r["J_defined"] == "True"
    r["cpc_raw_defined"] = r["cpc_raw_defined"] == "True"


def _scatter_by_substrate(ax, pts, xk, yk):
    for s in SUBS:
        sx = [p[xk] for p in pts if p["substrate"] == s]
        sy = [p[yk] for p in pts if p["substrate"] == s]
        if sx:
            ax.scatter(sx, sy, s=34, color=SUB_COLOR[s], alpha=0.85, edgecolor="white",
                       linewidth=0.5, label=SUB_NAME[s], zorder=3)


def _box(ax, text, loc=("right", "top")):
    ha, va = loc
    x = 0.97 if ha == "right" else 0.03
    y = 0.95 if va == "top" else 0.06
    ax.text(x, y, text, transform=ax.transAxes, ha=ha, va=va,
            fontsize=cs.FONT_SIZES["annotation"],
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=cs.PALETTE["gray_light"], lw=0.6))


# ---------------------------------------------------------------------------
def fig_01_mean_independence():
    """Two-panel headline: phi vs mu (flat) | CV-CPC_raw vs mu (sloped)."""
    phi_pts = [r for r in rows if r["phi_defined"]]                 # 84
    cv_pts  = [r for r in rows if r["cpc_raw_defined"]]             # 55
    rho_phi = stats.spearmanr([p["mu"] for p in phi_pts], [p["phi"] for p in phi_pts])[0]
    rho_cv  = stats.spearmanr([p["mu"] for p in cv_pts], [p["cpc_raw"] for p in cv_pts])[0]
    # integrity: match the locked per-framing (phi,84) and baseline (CV,55) values
    assert abs(rho_phi - (-0.08232812314127262)) < 1e-9, rho_phi
    assert abs(rho_cv - (-0.6822887846481871)) < 1e-9, rho_cv

    fig, (axL, axR) = plt.subplots(1, 2, figsize=cs.FIGSIZE["spread"])
    _scatter_by_substrate(axL, phi_pts, "mu", "phi")
    axL.axhline(1.0, color=cs.GRAY, lw=0.6, ls=":", zorder=1)        # phi null E[phi]=1
    axL.set_xlabel("recall level  $\\hat{\\pi}$  (mean surfacing rate)")
    axL.set_ylabel("$\\varphi$  (between-model dispersion)")
    _box(axL, f"$\\rho(\\varphi,\\hat\\pi)$ = {rho_phi:+.2f}  (n={len(phi_pts)})\n"
              f"pooled make-or-break |$\\rho$| = 0.09\nceiling |$\\rho$| $\\leq$ 0.50", ("right", "top"))
    axL.set_title("$\\varphi$ — mean-independent", fontsize=cs.FONT_SIZES["subtitle"])

    _scatter_by_substrate(axR, cv_pts, "mu", "cpc_raw")
    xs = np.array([p["mu"] for p in cv_pts]); ys = np.array([p["cpc_raw"] for p in cv_pts])
    b, a = np.polyfit(xs, ys, 1)
    xl = np.linspace(xs.min(), xs.max(), 50)
    axR.plot(xl, a + b * xl, color=cs.BLACK, lw=1.0, alpha=0.5, zorder=2)
    axR.set_xlabel("recall level  $\\hat{\\pi}$  (mean surfacing rate)")
    axR.set_ylabel("CV-CPC$_{raw}$  =  SD / mean")
    _box(axR, f"$\\rho$(CV,$\\hat\\pi$) = {rho_cv:+.2f}  (n={len(cv_pts)})\n"
              "reproduces v1.7 coupling\n|$\\rho$| = 0.68 $\\geq$ 0.50", ("right", "top"))
    axR.set_title("CV-CPC — mean-coupled", fontsize=cs.FONT_SIZES["subtitle"])
    # legend on the LEFT panel's empty upper-left (phi>4.5 region) — clear of both annotation boxes
    axL.legend(loc="upper left", fontsize=cs.FONT_SIZES["legend"], framealpha=0.9)

    fig.subplots_adjust(**cs.MARGINS["two_panel"])
    cs.add_header(fig, "Dispersion that does not restate the mean",
                  "φ is independent of recall level; the CV-based measure it replaces is not",
                  "Same six-model panel, same brands — the contrast is the instrument, not the data.")
    cs.add_footer(fig, verdict="H_MeanIndependent CONFIRMED — pooled |ρ(φ,μ)| = 0.091, below the 0.50 ceiling; CV-CPC baseline 0.682.",
                  phase=SOURCE_PHASE, protocol=PROTOCOL)
    p = OUT / "chart_01_mean_independence.pdf"; fig.savefig(p, **cs.SAVEFIG_PARAMS); plt.close(fig)
    return p


# ---------------------------------------------------------------------------
def fig_02_defined_coverage():
    """pi_hat strip: phi-defined (84) vs CV-defined (55); the 29 sub-floor gain units."""
    defined = [r for r in rows if r["phi_defined"]]                 # 84
    gain    = [r for r in defined if not r["cpc_raw_defined"]]      # 29  (0 < pi_hat < 1/6)
    cvdef   = [r for r in defined if r["cpc_raw_defined"]]          # 55
    assert len(defined) == 84 and len(gain) == 29 and len(cvdef) == 55

    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    rng = np.random.RandomState(0)
    def strip(pts, y, color, lab):
        xs = [p["pi_hat"] for p in pts]
        ax.scatter(xs, y + (rng.rand(len(xs)) - 0.5) * 0.5, s=30, color=color,
                   alpha=0.8, edgecolor="white", linewidth=0.4, zorder=3, label=lab)
    strip(cvdef, 2.0, cs.INDIGO, f"CV-CPC$_{{raw}}$-defined ($\\hat\\pi \\geq$ 1/6)  ·  n={len(cvdef)}")
    strip(gain, 0.5, cs.WARM, f"$\\varphi$-defined gain ($\\hat\\pi <$ 1/6)  ·  n={len(gain)}")
    ax.axvline(PI_FLOOR, color=cs.WARM, lw=1.2, ls="--", zorder=2)
    ax.text(PI_FLOOR + 0.006, 2.9, "CV floor  $\\hat\\pi$ = 1/6\n(mean recall = 1.0)",
            color=cs.WARM, fontsize=cs.FONT_SIZES["annotation"], va="top", ha="left")
    ax.set_yticks([0.5, 2.0]); ax.set_yticklabels(["low-recall\ngain (29)", "CV-defined\n(55)"])
    ax.set_ylim(-0.4, 3.2)
    ax.set_xlabel("recall level  $\\hat{\\pi}$  (mean surfacing rate across the six-model panel)")
    _box(ax, "$\\varphi$-defined (84)  $\\supsetneq$  CV-CPC$_{raw}$-defined (55)\n"
             "gain = 29 sub-floor units, all genuinely low-recall\n"
             "no $\\hat\\pi$=1 ceiling unit (containment intact)", ("right", "top"))
    fig.subplots_adjust(**cs.MARGINS["single"])
    cs.add_header(fig, "φ extends defined coverage into the low-recall floor",
                  "The 29 brands CV cannot score — recalled too rarely — still yield a finite φ",
                  "φ is undefined only at true-zero and full saturation; CV is undefined below mean recall 1.0.")
    cs.add_footer(fig, verdict="H_LowRecallDefined CONFIRMED [0] — φ-defined strictly contains CV-defined; non-empty gain; 0 ceiling units.",
                  phase=SOURCE_PHASE, protocol=PROTOCOL)
    p = OUT / "chart_02_defined_coverage.pdf"; fig.savefig(p, **cs.SAVEFIG_PARAMS); plt.close(fig)
    return p


# ---------------------------------------------------------------------------
def _discordant_keys(pts):
    """Percentile rule (locked): |cons_pct(phi) - cons_pct(J)| >= 0.50."""
    n = len(pts)
    def pct(vals):
        rk = stats.rankdata(np.asarray(vals, float), method="average")
        return (rk - 1.0) / (n - 1.0)
    cphi = 1.0 - pct([p["phi"] for p in pts]); cJ = pct([p["J"] for p in pts])
    return {id(p) for i, p in enumerate(pts) if abs(cphi[i] - cJ[i]) >= 0.50}


def fig_03_phi_j_dissociation():
    """phi-vs-J scatter; rho annotated; the 9 discordant units flagged."""
    pts = [r for r in rows if r["phi_defined"] and r["J_defined"]]  # 74
    rho = stats.spearmanr([p["phi"] for p in pts], [p["J"] for p in pts])[0]
    assert abs(rho - (-0.4025454211840846)) < 1e-9, rho
    disc = _discordant_keys(pts)
    assert len(disc) == 9, len(disc)

    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    _scatter_by_substrate(ax, pts, "phi", "J")
    # ring the discordant units
    dx = [p["phi"] for p in pts if id(p) in disc]; dy = [p["J"] for p in pts if id(p) in disc]
    ax.scatter(dx, dy, s=120, facecolors="none", edgecolors=cs.BLACK, linewidths=1.1,
               zorder=4, label="discordant (9)")
    ax.axhline(np.median([p["J"] for p in pts]), color=cs.GRAY, lw=0.5, ls="--", zorder=1)
    ax.axvline(np.median([p["phi"] for p in pts]), color=cs.GRAY, lw=0.5, ls="--", zorder=1)
    ax.set_xlabel("$\\varphi$  (magnitude facet — between-model dispersion)")
    ax.set_ylabel("J  (positional facet — mean pairwise Jaccard)")
    _box(ax, f"$\\rho(\\varphi, J)$ = {rho:+.2f}  (n={len(pts)})\n"
             "ceiling |$\\rho$| $\\leq$ 0.70  (non-redundant)\n"
             "9 brands: magnitude- vs position-consistent split", ("right", "bottom"))
    ax.legend(loc="upper right", fontsize=cs.FONT_SIZES["legend"])
    fig.subplots_adjust(**cs.MARGINS["single"])
    cs.add_header(fig, "φ and J measure distinct facets of consistency",
                  "How much a brand surfaces (φ) and where it surfaces (J) come apart",
                  "Below the 0.70 redundancy ceiling, with discordant brands present in every framing.")
    cs.add_footer(fig, verdict="H_PositionalDissociation CONFIRMED — |ρ(φ,J)| = 0.403, below the 0.70 ceiling; 9 discordant.",
                  phase=SOURCE_PHASE, protocol=PROTOCOL)
    p = OUT / "chart_03_phi_j_dissociation.pdf"; fig.savefig(p, **cs.SAVEFIG_PARAMS); plt.close(fig)
    return p


# ---------------------------------------------------------------------------
def _two_wave_pairs():
    """Recompute phi(t1) vs phi(t2) pairs read-only from the materialized frozen inputs."""
    import score_v0_31 as S31, score_v33 as V33, score_v1_8 as SC
    V = ROOT / "osf"
    def counts_for(base, v23_rel):
        out = {}
        for sub in ("v0.20", "v0.21", "v0.22"):
            rk, rp, mod, _ = V33.RECON_CFG[sub]
            out[sub], _ = S31.counts_raw_text(rk, rp, mod, base / f"{sub.replace('v0.', 'v')}/phase_b_results.csv")
        out["v0.19"], _ = S31.counts_v19(base / "v19/phase_b_results.csv")
        out["v0.23"], _ = S31.counts_v23(base / v23_rel)
        return out
    t1 = counts_for(V, "v23/data/v23_phase_b_scored.json")
    t2 = counts_for(V / "v34/data", "v23/v23_phase_b_scored.json")
    out = []
    for sub in SUBS:
        for b in (set(t1.get(sub, {})) & set(t2.get(sub, {}))):
            p1, _, s1 = SC.phi_of(t1[sub][b]); p2, _, s2 = SC.phi_of(t2[sub][b])
            if s1 == "defined" and s2 == "defined":
                out.append({"phi1": p1, "phi2": p2, "substrate": sub})
    return out


def fig_04_two_wave():
    """phi(t1) vs phi(t2) reproducibility; rho asserted == locked 0.645."""
    pts = _two_wave_pairs()
    rho = stats.spearmanr([p["phi1"] for p in pts], [p["phi2"] for p in pts])[0]
    assert abs(rho - 0.6453869683902722) < 1e-9, (rho, len(pts))   # locked verdicts value
    assert len(pts) == 83, len(pts)

    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    _scatter_by_substrate(ax, pts, "phi1", "phi2")
    lim = max(max(p["phi1"] for p in pts), max(p["phi2"] for p in pts)) * 1.05
    ax.plot([0, lim], [0, lim], color=cs.GRAY, lw=0.8, ls="--", zorder=1, label="$t_1 = t_2$")
    ax.set_xlim(0, lim); ax.set_ylim(0, lim)
    ax.set_xlabel("$\\varphi$  at wave  $t_1$  (original deposit)")
    ax.set_ylabel("$\\varphi$  at wave  $t_2$  (re-acquisition)")
    _box(ax, f"Spearman $\\rho$ = {rho:.2f}  (n={len(pts)}, p < 1e-10)\n"
             "moderate temporal reproducibility", ("right", "bottom"))
    ax.legend(loc="upper left", fontsize=cs.FONT_SIZES["legend"])
    fig.subplots_adjust(**cs.MARGINS["single"])
    cs.add_header(fig, "φ rank order is moderately stable across waves",
                  "Per-brand φ at two acquisition waves of the same panel",
                  "Reported as moderate (ρ = 0.65), not overstated — a single re-acquisition, not a stability claim.")
    cs.add_footer(fig, verdict="Two-wave reproducibility: ρ(φ) = 0.645 across waves t1 to t2 (n = 83); supplementary, non-gating.",
                  phase=SOURCE_PHASE, protocol=PROTOCOL)
    p = OUT / "chart_04_two_wave.pdf"; fig.savefig(p, **cs.SAVEFIG_PARAMS); plt.close(fig)
    return p


if __name__ == "__main__":
    for fn in (fig_01_mean_independence, fig_02_defined_coverage,
               fig_03_phi_j_dissociation, fig_04_two_wave):
        print("wrote:", fn())
