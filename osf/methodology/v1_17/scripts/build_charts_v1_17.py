"""
build_charts_v1_17.py -- the four pre-registered charts of v1.17 (PRE_REGISTRATION_v1_17.md section 5), one per
finding, from a results JSON ({"t4": ..., "omnibus": ...}). Program chart conventions: bold title top-left, grey
subtitle, thin indigo rule, italic grey source line; Akkurat Pro when installed.

usage: python3 build_charts_v1_17.py RESULTS_JSON OUT_DIR [--synthetic]
"""
import json
import math
import sys
import textwrap
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                 # noqa: E402
from matplotlib import font_manager              # noqa: E402

INDIGO, GREY, LIGHT = "#37237B", "#6B6B6B", "#B9B2D6"
CYAN = "#3FA7C9"
for f in Path.home().joinpath("Library/Fonts").glob("AkkuratPro-*.otf"):
    font_manager.fontManager.addfont(str(f))
if any("Akkurat Pro" == f.name for f in font_manager.fontManager.ttflist):
    plt.rcParams["font.family"] = "Akkurat Pro"
SOURCE = ("Source: AIAS v0.42 t4 coded answers (tags v0.42-acquisition-locked, v0.42-scoring-locked); "
          "v0.41 three-wave table; analysis pre-registered at v1.17-prereg-r1. Exploratory.")


def frame(fig, title, subtitle, source):
    fig.text(0.04, 0.955, title, fontsize=13, fontweight="bold", ha="left", va="top")
    fig.text(0.04, 0.905, "\n".join(textwrap.wrap(subtitle, 115)), fontsize=8.5, color=GREY, ha="left", va="top")
    fig.add_artist(plt.Line2D([0.04, 0.96], [0.845, 0.845], color=INDIGO, linewidth=0.8))
    fig.text(0.04, 0.025, source, fontsize=7, color=GREY, style="italic", ha="left", va="bottom", wrap=True)


def _style(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=8.5)


def chart_se_runs(t4, out, tag):
    fig = plt.figure(figsize=(8, 5))
    ax = fig.add_axes([0.09, 0.15, 0.86, 0.66])
    Rs = list(range(1, 31))
    for key, col, lab in (("size_24", INDIGO, "24-brand categories"), ("size_16", CYAN, "16-brand category")):
        row = t4["primary"][key]
        sd = row["sd_one_run"]
        lo, hi = (math.sqrt(v) for v in row["var_ci95_cluster_bootstrap"])
        se = [sd / math.sqrt(R) for R in Rs]
        ax.fill_between(Rs, [lo / math.sqrt(R) for R in Rs], [hi / math.sqrt(R) for R in Rs], color=col, alpha=0.12,
                        linewidth=0)
        ax.plot(Rs[:3], se[:3], color=col, linewidth=2, label=f"{lab} (n = {row['n_units']} units)")
        ax.plot(Rs[2:], se[2:], color=col, linewidth=1.2, linestyle="--")
    for tau in (0.10, 0.05):
        ax.axhline(tau, color=GREY, linewidth=0.7, linestyle=":")
        ax.text(30.3, tau, f"{tau:.2f}", fontsize=8, color=GREY, va="bottom")
    ax.axvline(3, color=GREY, linewidth=0.5)
    ax.text(3.2, ax.get_ylim()[1] * 0.97, "observed | projected", fontsize=7.5, color=GREY, va="top")
    ax.set_xlabel("Runs per cell", fontsize=9)
    ax.set_ylabel("Standard error of Presence (0–1 scale)", fontsize=9)
    ax.legend(frameon=False, fontsize=8.5)
    _style(ax)
    frame(fig, "Standard error of a brand's Presence, by number of runs",
          "Per model and search condition. Solid: runs 1–3 observed. Dashed: projection that assumes independent "
          "runs. Shading: 95% interval.", SOURCE + tag)
    fig.savefig(out / "chart_01_se_by_runs.png", dpi=200)
    fig.savefig(out / "chart_01_se_by_runs.pdf")
    plt.close(fig)


def chart_level(t4, out, tag):
    fig = plt.figure(figsize=(8, 5))
    ax = fig.add_axes([0.09, 0.15, 0.86, 0.66])
    bands = ["low", "middle", "high"]
    names = {"low": "Low\n(1–5 of 18)", "middle": "Middle\n(6–12 of 18)", "high": "High\n(13–17 of 18)"}
    vals, errs_lo, errs_hi, ns = [], [], [], []
    for b in bands:
        row = t4["alongside"][f"band_{b}"]
        if not row["n_units"]:
            vals.append(0); errs_lo.append(0); errs_hi.append(0); ns.append(0)
            continue
        sd = row["sd_one_run"]
        lo, hi = (math.sqrt(v) for v in row["var_ci95_cluster_bootstrap"])
        vals.append(sd); errs_lo.append(sd - lo); errs_hi.append(hi - sd); ns.append(row["n_units"])
    ax.bar(range(len(bands)), vals, color=INDIGO, width=0.55, yerr=[errs_lo, errs_hi], ecolor=GREY, capsize=3)
    for i, (v, n) in enumerate(zip(vals, ns)):
        ax.text(i, v / 2, f"n = {n}", color="white", ha="center", fontsize=8)
    z, f = t4["alongside"]["band_zero"]["n_units"], t4["alongside"]["band_full"]["n_units"]
    ax.set_xticks(range(len(bands)), [names[b] for b in bands], fontsize=8.5)
    ax.set_ylabel("Standard deviation of one run", fontsize=9)
    _style(ax)
    frame(fig, "Run-to-run movement by how often a brand is named",
          f"Units grouped by mentions over 18 answers. Not shown: never named ({z} units) and named every time "
          f"({f} units), which do not move by construction. Bars: 95% interval.", SOURCE + tag)
    fig.savefig(out / "chart_02_sd_by_level.png", dpi=200)
    fig.savefig(out / "chart_02_sd_by_level.pdf")
    plt.close(fig)


def chart_once(t4, out, tag):
    o = t4["once_vs_three"]
    fig = plt.figure(figsize=(8, 5))
    ax = fig.add_axes([0.36, 0.15, 0.56, 0.64])
    rows = [("Change place, per model", o["unit_level_vs_three_run_mean"]["share_brands_changing_place"]),
            ("Change place, three-model panel", o["panel_N3_vs_three_run_mean"]["share_brands_changing_place"]),
            ("Cross the recall floor, search off",
             o["published_floor_N3"]["S0"]["mean_brands_crossing"] / o["published_floor_N3"]["S0"]["n_brands"]),
            ("Cross the recall floor, search on",
             o["published_floor_N3"]["S1"]["mean_brands_crossing"] / o["published_floor_N3"]["S1"]["n_brands"])]
    ys = list(range(len(rows)))[::-1]
    ax.barh(ys, [r[1] for r in rows], color=INDIGO, height=0.5)
    for y, (lab, v) in zip(ys, rows):
        ax.text(v + 0.005, y, f"{v:.1%}", va="center", fontsize=8.5)
    ax.set_yticks(ys, [r[0] for r in rows], fontsize=8.5)
    ax.set_xlabel("Share of brands (mean over the three single runs)", fontsize=9)
    _style(ax)
    frame(fig, "One run against three: places and the floor",
          "Each single run compared with the three-run result. A place change needs a strict reversal against at "
          "least one brand of the same category.", SOURCE + tag)
    fig.savefig(out / "chart_03_once_vs_three.png", dpi=200)
    fig.savefig(out / "chart_03_once_vs_three.pdf")
    plt.close(fig)


def chart_omni(t4, om, out, tag):
    fig = plt.figure(figsize=(8, 5))
    axl = fig.add_axes([0.09, 0.15, 0.38, 0.56])
    axr = fig.add_axes([0.58, 0.15, 0.38, 0.56])
    keys = [("size_16", "16 brands"), ("size_24", "24 brands")]
    axl.bar(range(2), [t4["primary"][k]["sd_one_run"] for k, _ in keys], color=INDIGO, width=0.5)
    axl.set_xticks(range(2), [lab for _, lab in keys], fontsize=8.5)
    axl.set_title("t4: run to run, same day\n(newest models, 3 runs)", fontsize=9, loc="left")
    axr.bar(range(2), [om["strata"][k]["sd_one_run"] for k, _ in keys], color=LIGHT, width=0.5)
    axr.set_xticks(range(2), [lab for _, lab in keys], fontsize=8.5)
    axr.set_title("Omnibus: wave to wave, May–Nov\n(legacy six models, 1 run per wave)", fontsize=9, loc="left")
    top = max(axl.get_ylim()[1], axr.get_ylim()[1])
    for ax in (axl, axr):
        ax.set_ylim(0, top)
        ax.set_ylabel("Standard deviation of one measurement", fontsize=8.5)
        _style(ax)
    frame(fig, "Same-day noise and change across waves, kept apart",
          "Different quantities on different models: the right panel mixes real change with run noise. "
          "Never pooled.", SOURCE + tag)
    fig.savefig(out / "chart_04_omnibus_separate.png", dpi=200)
    fig.savefig(out / "chart_04_omnibus_separate.pdf")
    plt.close(fig)


def main(argv):
    src, out = Path(argv[0]), Path(argv[1])
    tag = " SYNTHETIC DATA (dry run)." if "--synthetic" in argv else ""
    out.mkdir(parents=True, exist_ok=True)
    d = json.loads(Path(src).read_text(encoding="utf-8"))
    chart_se_runs(d["t4"], out, tag)
    chart_level(d["t4"], out, tag)
    chart_once(d["t4"], out, tag)
    chart_omni(d["t4"], d["omnibus"], out, tag)
    print(f"wrote 4 charts to {out}")


if __name__ == "__main__":
    main(sys.argv[1:])
