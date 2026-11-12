#!/usr/bin/env python3
"""
AIAS 6.0 Preview (provisional) -- figure builder (paper register; the brand-format report waits for the new report
design). House style of build_charts_v112.py / build_charts_v111.py (scripts/chart_style.py: bold title top-left, gray
subtitle, thin Indigo rule, italic gray source line citing the pre-registration tag). Every number is a leaf of the
scorer's outputs read through papers/aias_6_0_preview/aias6_values.py; nothing is re-scored.

One chart per finding (pre-registration sections 6 and 10):
  chart_01_pairwise           S-tests among the included parts (H_Structure, H_PC_N3), with the parts under review
                              (MARGINAL row) in a separate lower band, descriptive
  chart_02_profile_coverage   included parts rated per unit, by category (D9)
Titles describe what is plotted and never repeat a finding's headline. Every chart carries "provisional".

  python3 scripts/build_charts_aias6.py [--outputs DIR] [--out DIR] [--watermark TEXT]
--watermark is required for synthetic outputs and refused for real ones.
"""
import argparse
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "papers/aias_6_0_preview"))
import chart_style as cs  # noqa: E402
import aias6_values as VV  # noqa: E402
cs.setup()

SOURCE = "Source: AIAS™ 6.0 Preview (provisional) | pre-registration {tag} | N3, t₄ week | Third System™"
WATERMARK = None
TITLES = {1: "Within-category rank correlation of each pair of parts (provisional)",
          2: "Included parts rated per brand unit, by category (provisional)"}
NAMES = {1: "chart_01_pairwise", 2: "chart_02_profile_coverage"}
VCOL = {"CONFIRMED": cs.INDIGO, "MARGINAL": cs.PALETTE["warm_t1"], "FALSIFIED": cs.PALETTE["warm"],
        "UNDETERMINED": cs.PALETTE["gray"]}


def M(s):
    for a, b in (("ρ_w", r"$\rho_w$"), ("ρ", r"$\rho$"), ("≤", r"$\leq$"), ("≥", r"$\geq$")):
        s = s.replace(a, b)
    return s


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


def chart_01(V, out):
    st = V["structure"]
    rows = []
    for t in (st.get("S_tests") or {}).values():
        rows.append((t, False))
    for t in (st.get("descriptive_marginal_pairs") or {}).values():
        rows.append((t, True))
    h = max(3.6, 1.4 + 0.32 * len(rows))
    fig, ax = plt.subplots(figsize=(7.5, h))
    for x0, c in ((-0.5, cs.WARM), (-0.3, cs.PALETTE["gray_light"]), (0.3, cs.PALETTE["gray_light"]), (0.5, cs.WARM)):
        ax.axvline(x0, color=c, lw=0.8, ls=":", zorder=1)
    ax.axvline(0, color=cs.PALETTE["gray_light"], lw=0.6, zorder=1)
    labels = []
    n = len(rows)
    for i, (t, desc) in enumerate(rows):
        y = n - 1 - i
        a, b = t["pair"]
        labels.append(f"{VV.NAME[a]} × {VV.NAME[b]}" + ("  (under review)" if desc else ""))
        if t.get("rho") is None:
            ax.text(0, y, "not computed", fontsize=7, color=cs.GRAY, ha="center", va="center")
            continue
        ci = t.get("ci90") or [None, None]
        col = cs.PALETTE["gray"] if desc else VCOL.get(t["verdict"], cs.INDIGO)
        if ci[0] is not None and ci[1] is not None:
            ax.plot(ci, [y, y], color=col, lw=1.4, zorder=2)
        ax.scatter([t["rho"]], [y], s=30, color=col, zorder=3, edgecolor="white", linewidth=0.4,
                   marker="D" if desc else "o")
        ax.text(0.98, y, ("descriptive" if desc else t["verdict"]), fontsize=6.8, color=col, va="center", ha="right")
    nk = sum(1 for _, d in rows if not d)
    if nk < n:
        ax.axhline(n - nk - 0.5, color=cs.INDIGO, lw=0.5)
    ax.set_yticks(range(n - 1, -1, -1), labels, fontsize=7.6)
    ax.set_xlim(-1, 1)
    ax.set_ylim(-0.7, n - 0.3)
    ax.set_xlabel(M("ρ_w (centred within-category ranks; pairwise-complete units)"), fontsize=9)
    ax.tick_params(axis="x", labelsize=8.5)
    fig.subplots_adjust(top=1 - 1.05 / h, bottom=0.55 / h + 0.08, left=0.3, right=0.97)
    _header(fig, 1, "Point = ρ_w; bar = 90% bootstrap interval; diamonds below the line: parts under review (no verdict).",
            "Dotted gray: |ρ| = 0.30; dotted orange: |ρ| = 0.50.")
    hs = st["H_Structure"]
    _save(fig, 1, f"H_Structure: {hs['verdict']} (k = {hs['k']}); H_PC_N3: {st.get('H_PC_N3')}", V["prereg_tag"], out)


def chart_02(V, out):
    rpu = V["descriptives"]["D9_coverage"]["rated_parts_per_unit"]["K"]
    k = len(V["K"])
    cats = [c for c in VV.SUBS if c in rpu]
    fig, ax = plt.subplots(figsize=cs.FIGSIZE["hero_short"])
    left = [0.0] * len(cats)
    shades = [cs.PALETTE[c] for c in ("gray_light", "indigo_t3", "indigo_t2", "indigo_t1", "indigo_sec", "indigo",
                                      "black")]
    for j in range(k + 1):
        vals = [float(rpu[c].get(str(j), rpu[c].get(j, 0))) for c in cats]
        ax.barh(range(len(cats)), vals, left=left, color=shades[min(j, len(shades) - 1)], height=0.6,
                label=f"{j} of {k}", edgecolor="white", linewidth=0.4)
        left = [a + b for a, b in zip(left, vals)]
    ax.set_yticks(range(len(cats)), [VV.CAT[c] for c in cats], fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel("Brand units", fontsize=9)
    ax.tick_params(axis="x", labelsize=8.5)
    ax.legend(loc="center left", bbox_to_anchor=(1.01, 0.5), fontsize=7.2, frameon=False, title="parts rated",
              title_fontsize=7.2)
    fig.subplots_adjust(top=0.72, bottom=0.2, left=0.16, right=0.82)
    _header(fig, 2, "Units by the number of the included parts on which they are rated.",
            "Every rating floor requires the brand to be named, so full profiles lean to well-named brands.")
    _save(fig, 2, f"Complete-profile set: {V['structure'].get('U_K', {}).get('n', 'n/a')} units", V["prereg_tag"], out)


def main(argv=None):
    global WATERMARK
    ap = argparse.ArgumentParser(description="AIAS 6.0 Preview figures")
    ap.add_argument("--outputs", type=Path, default=VV.OUTDIR)
    ap.add_argument("--out", type=Path, default=ROOT / "reports/figs/aias6")
    ap.add_argument("--watermark", default=None)
    a = ap.parse_args(argv)
    src = VV.load_sources(a.outputs)
    V = src["results"]
    if VV.is_synthetic(src) and not a.watermark:
        print("[aias6 charts] REFUSED: synthetic outputs need --watermark", file=sys.stderr)
        return 2
    if not VV.is_synthetic(src) and a.watermark:
        print("[aias6 charts] REFUSED: --watermark is for synthetic runs only", file=sys.stderr)
        return 2
    WATERMARK = a.watermark
    print(f"building AIAS 6.0 Preview figures -> {a.out}")
    if "S_tests" in V["structure"]:
        chart_01(V, a.out)
    chart_02(V, a.out)
    print("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
