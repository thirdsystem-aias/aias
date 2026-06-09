#!/usr/bin/env python3
"""
v0.33 Provider-Asymmetric CPC — figure builder (one per finding).
  chart_01_eta2_null      permutation-null of mean eta^2; observed modestly past q95 (H_Provider_Asymmetry)
  chart_02_gate_arms      recall-arm vs recognition-arm eta^2 + nulls; the saturation collapse (H_Provider_Beyond_Presence)
  chart_03_provider_ranks within-pair-consistency provider ranks by substrate + Kendall's W (H_Provider_Ordinal)

Reads osf/v33/data/v33_eta2.csv + osf/v33/v33_provider_asymmetry_verdicts.json.
Regenerates the MC null deterministically (seed 280400) to match the locked verdicts.
House style via chart_style.py. Outputs PDFs to reports/figs/v33/.

NOTE: paper (academic) register only. The managerial P1-P5 report-register footers are
swapped in at the step-6 report pass, not authored here (no findings-to-propositions
mapping is locked yet).
"""
import sys, csv, json, itertools
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path.home() / "aias"
sys.path.insert(0, str(ROOT / "scripts"))
import chart_style as cs
cs.setup()

OUT = ROOT / "reports" / "figs" / "v33"
SOURCE_PHASE = "v0.33 (Provider-Asymmetric CPC)"
PROTOCOL = "v0.33-prereg-r1"
SEED = 280400
N_MC = 10_000
PROVS = ["Anthropic", "OpenAI", "Google"]
OMNI = ["v0.19", "v0.20", "v0.21", "v0.22", "v0.23"]
CAT = {"v0.19": "headphones", "v0.20": "skincare", "v0.21": "cosmetics",
       "v0.22": "automotive", "v0.23": "spirits"}

# academic-register footers (P1-P5 report register swapped at the report pass)
FOOTERS = {
    "eta2null": "H_Provider_Asymmetry CONFIRMED — mean eta^2 = 0.360 > null (p = 7e-4), robust across all five LOSO; modest excess over a high chance floor.",
    "gatearms": "H_Provider_Beyond_Presence — numerical criterion met (delta eta^2 = 0.505, p = 1e-4) but saturation-collapsed; NOT a dissociation.",
    "ranks":    "H_Provider_Ordinal UNINFORMATIVE — Kendall's W = 0.31, exact p = 0.18; underpowered at N = 5, not disconfirming.",
}

# ---- load committed confirmatory outputs -----------------------------------
rows = list(csv.DictReader(open(ROOT / "osf/v33/data/v33_eta2.csv")))
V = json.load(open(ROOT / "osf/v33/v33_provider_asymmetry_verdicts.json"))


# ---- eta^2 over the 90-assignment labeled-pair space (matches score_v33) ----
def gen90():
    pos = list(range(6)); out = []
    for a in itertools.combinations(pos, 2):
        rem = [p for p in pos if p not in a]
        for b in itertools.combinations(rem, 2):
            out.append((a, b, tuple(p for p in rem if p not in b)))
    return out
ASSIGN90 = gen90()
OBS_IDX = ASSIGN90.index(((0, 1), (2, 3), (4, 5)))


def eta2_for(x, asg):
    x = np.asarray(x, float); g = x.mean(); st = float(((x - g) ** 2).sum())
    if st <= 0.0:
        return 0.0
    return sum(2.0 * ((x[i] + x[j]) / 2 - g) ** 2 for i, j in asg) / st


def eta2_matrix(vectors):
    return np.array([[eta2_for(v, a) for a in ASSIGN90] for v in vectors])


# =============================================================================
def chart_01_eta2_null():
    recall = [json.loads(r["recall_per_model"]) for r in rows]
    Ec = eta2_matrix(recall)                          # 112 x 90
    rng = np.random.default_rng(SEED)
    n = Ec.shape[0]
    idx = rng.integers(0, 90, size=(N_MC, n))
    null_means = Ec[np.arange(n)[None, :], idx].mean(axis=1)

    a = V["H_Provider_Asymmetry"]
    obs, nmean, q95, p = (a["mean_eta2_observed"], a["null_mean"], a["null_q95"], a["mc_p_onesided"])
    loso = [V["loso"]["per_leftout"][k]["mean_eta2"] for k in OMNI]

    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    ax.hist(null_means, bins=60, color=cs.PALETTE["gray_light"], edgecolor="white", linewidth=0.3, zorder=2)
    ax.axvline(nmean, color=cs.GRAY, lw=1.0, ls="--", zorder=3, label=f"null mean ({nmean:.3f})")
    ax.axvline(q95, color=cs.GRAY, lw=1.0, ls=":", zorder=3, label=f"null 95th pct ({q95:.3f})")
    ax.axvline(obs, color=cs.INDIGO, lw=2.0, zorder=5, label=f"observed ({obs:.3f})")
    # LOSO refit means — robustness, just above the axis
    ymax = ax.get_ylim()[1]
    ax.scatter(loso, [ymax * 0.045] * len(loso), marker="v", s=34, color=cs.WARM,
               edgecolor="white", linewidth=0.5, zorder=6, label="LOSO refit means (5)")
    ax.annotate(f"observed {obs:.3f}\np = {p:.1e}\nexcess over null floor "
                + r"$\approx$" + f" {obs - nmean:.2f}",
                xy=(obs, ymax * 0.62), xytext=(obs + 0.012, ymax * 0.62),
                ha="left", va="center", fontsize=cs.FONT_SIZES["annotation"],
                bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=cs.PALETTE["gray_light"], lw=0.6))
    ax.set_xlabel(r"mean between-provider variance share  $\eta^2$  (per MC draw)")
    ax.set_ylabel("MC draws")
    ax.legend(loc="upper right", fontsize=cs.FONT_SIZES["legend"])
    fig.subplots_adjust(**cs.MARGINS["single"])
    cs.add_header(fig, "Provider organization of recall is significant but modest",
                  r"Permutation-null of mean $\eta^2$ across 112 brands ($\geq$10,000 draws); observed vs the null",
                  "The observed share sits just past the 95th percentile of a high chance floor — a reliable but small provider signal.")
    cs.add_footer(fig, verdict=FOOTERS["eta2null"], phase=SOURCE_PHASE, protocol=PROTOCOL)
    p_ = OUT / "chart_01_eta2_null.pdf"; fig.savefig(p_, **cs.SAVEFIG_PARAMS); plt.close(fig); return p_


# =============================================================================
def chart_02_gate_arms():
    af = [r for r in rows if r["defined"] == "True"]
    recall_af = [json.loads(r["recall_per_model"]) for r in af]
    recog_af = [json.loads(r["recog_per_model"]) for r in af]
    Ec, Ep = eta2_matrix(recall_af), eta2_matrix(recog_af)
    rng = np.random.default_rng(SEED)
    n = Ec.shape[0]; idx = rng.integers(0, 90, size=(N_MC, n)); cols = np.arange(n)[None, :]
    recall_null, recog_null = Ec[cols, idx].mean(1), Ep[cols, idx].mean(1)
    bands = {  # observed, null mean, null q95
        "recall": (Ec[:, OBS_IDX].mean(), recall_null.mean(), np.quantile(recall_null, 0.95)),
        "recog":  (Ep[:, OBS_IDX].mean(), recog_null.mean(), np.quantile(recog_null, 0.95)),
    }

    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    xs = [0, 1]
    labels = [r"recall arm  $\eta^2_{CV\text{-}CPC}$", r"recognition arm  $\eta^2_{C_P}$"]
    colors = [cs.INDIGO, cs.TEAL]
    for x, key, col in zip(xs, ("recall", "recog"), colors):
        obs, nmean, q95 = bands[key]
        ax.bar(x, obs, width=0.5, color=col, alpha=0.85, zorder=3)
        # null band: shaded [null mean, q95] across the bar; dashed line at null mean
        ax.add_patch(plt.Rectangle((x - 0.3, nmean), 0.6, q95 - nmean, facecolor=cs.GRAY,
                                   alpha=0.18, zorder=2, edgecolor="none"))
        ax.plot([x - 0.3, x + 0.3], [nmean, nmean], color=cs.GRAY, lw=1.1, ls="--", zorder=4)
        ax.text(x, obs + 0.015, f"{obs:.3f}", ha="center", va="bottom", fontweight="bold",
                fontsize=cs.FONT_SIZES["annotation"], color=cs.BLACK)
        label_y = nmean if nmean > 0.06 else 0.055   # keep the saturated-arm null label off the axis
        ax.text(x + 0.33, label_y, f"null {nmean:.3f}\n(q95 {q95:.3f})", ha="left", va="center",
                fontsize=cs.FONT_SIZES["data_label"], color=cs.GRAY)
    ax.set_xticks(xs); ax.set_xticklabels(labels)
    ax.set_ylabel(r"between-provider variance share  $\eta^2$  (above-floor brands)")
    ax.set_ylim(0, 0.72); ax.set_xlim(-0.6, 1.9)
    ax.annotate(r"paired gate  $\delta\eta^2 = +0.505$,  paired null 0.378,  $p = 1\times10^{-4}$"
                + "\n54 of 55 above-floor brands: zero recognition variance"
                + "\npremium spirits saturated at source  "
                + r"$\Rightarrow$ gate collapses onto the recall arm",
                xy=(0.5, 0.655), ha="center", va="center", fontsize=cs.FONT_SIZES["annotation"],
                bbox=dict(boxstyle="round,pad=0.45", fc="white", ec=cs.PALETTE["gray_light"], lw=0.6))
    fig.subplots_adjust(**cs.MARGINS["single"])
    cs.add_header(fig, "The Beyond-Presence gate collapses under recognition saturation",
                  r"Recall-arm vs recognition-arm $\eta^2$ among above-floor brands, each with its permutation null",
                  r"Recognition carries almost no provider variance ($\eta^2_{C_P}\approx 0$), so the paired gate measures recall asymmetry, not a contrast.")
    cs.add_footer(fig, verdict=FOOTERS["gatearms"], phase=SOURCE_PHASE, protocol=PROTOCOL)
    p_ = OUT / "chart_02_gate_arms.pdf"; fig.savefig(p_, **cs.SAVEFIG_PARAMS); plt.close(fig); return p_


# =============================================================================
def chart_03_provider_ranks():
    from scipy import stats
    cons = V["H_Provider_Ordinal"]["within_pair_consistency"]
    W = V["H_Provider_Ordinal"]["kendalls_w"]; Wp = V["H_Provider_Ordinal"]["exact_p"]
    # rank within each substrate (1 = most consistent); average ranks for ties (skincare)
    rankmat = np.array([stats.rankdata([-cons[k][p] for p in PROVS], method="average") for k in OMNI])

    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero"])
    # heatmap: rank 1 (best) -> indigo, rank 3 (worst) -> light
    ax.imshow(rankmat, cmap="Purples_r", vmin=1, vmax=3, aspect="auto")
    for i, k in enumerate(OMNI):
        for j, prov in enumerate(PROVS):
            r = rankmat[i, j]
            txt = f"{r:g}"
            ax.text(j, i, txt, ha="center", va="center", fontweight="bold",
                    fontsize=cs.FONT_SIZES["annotation"],
                    color="white" if r <= 1.5 else cs.BLACK)
            ax.text(j, i + 0.30, f"{cons[k][prov]:.2f}", ha="center", va="center",
                    fontsize=6.2, color="white" if r <= 1.5 else cs.GRAY)
    ax.set_xticks(range(len(PROVS))); ax.set_xticklabels(PROVS)
    ax.set_yticks(range(len(OMNI))); ax.set_yticklabels([f"{k} {CAT[k]}" for k in OMNI])
    ax.set_xticks(np.arange(-.5, len(PROVS), 1), minor=True)
    ax.set_yticks(np.arange(-.5, len(OMNI), 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=1.4); ax.tick_params(which="minor", length=0)
    fig.subplots_adjust(**cs.MARGINS["single"])
    cs.add_header(fig, "Provider consistency ranks are not stably ordered",
                  "Within-pair-consistency provider rank by substrate (1 = most consistent; cell sub-value = consistency)",
                  f"Kendall's W = {W:.2f} against the exact null (p = {Wp:.2f}) — underpowered at five substrates, uninformative about concordance.")
    cs.add_footer(fig, verdict=FOOTERS["ranks"], phase=SOURCE_PHASE, protocol=PROTOCOL)
    p_ = OUT / "chart_03_provider_ranks.pdf"; fig.savefig(p_, **cs.SAVEFIG_PARAMS); plt.close(fig); return p_


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for fn in (chart_01_eta2_null, chart_02_gate_arms, chart_03_provider_ranks):
        print("wrote:", fn())
