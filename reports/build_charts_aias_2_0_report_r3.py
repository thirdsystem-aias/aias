#!/usr/bin/env python3
"""
build_charts_aias_2_0_report_r3.py - AIAS(TM) 2.0 report r3: the charts that change (approved Nov 12, 2026).

Report-only copies, written to reports/figs/aias_2_0/report_r3/. r2's chart builder, its content
module and its chart files (reports/figs/aias_2_0/report/) are imported or read, never changed, and
the paper's figures (reports/figs/aias_2_0/chart_0*.pdf, scripts/build_charts_aias_2_0.py) are not
involved: no report chart file is shared with the paper. Data, checks, sizes, positions and every
text line come from r2's builder; only the items below differ.

1. Source lines (citations of papers SSRN has not made public):
   - chart 1 (P1): Methodology v1.9 cited as SSRN 7685126, which SSRN declined (Nov 11). CLAUDE.md's
     SSRN rule (Nov 11) moves the AIAS 2.0 report to the thirdsystem.ai/OSF citation at this revision.
   - chart 2 (P2): v0.41 cited as SSRN 7685100. CLAUDE.md's registry lists 7685100 as submitted
     (Nov 9), not posted, so v0.41 is cited by its thirdsystem.ai/OSF copy, as the v0.43 paper
     (084ad11) does (thirdsystem.ai/studies/v0-41/, OSF ec6wh/v41). Pablo, Nov 11, 11:32 pm (c).
2. Data-viz colour roles (Pablo, Nov 11, 11:32 pm and Nov 12, 12:48 am; approved Nov 12, 6:57 am with
   Consistency in Rust, so Copper Plate keeps its challenger meaning): Presence = Indigo; Consistency =
   Rust #BD4718; time/waves = light-to-dark tints of the Indigo ramp (as chart 4, p.9);
   failed/old/reference = grey. Hex values are read from the brand tokens
   (brand/third_system_brand.json palette.measure_color_semantics) and asserted; no colour is invented.
   - chart 2 (P2, p.7): Presence dot Indigo, Consistency dot Rust (5.15:1 on white, 4.82:1 on Paper);
     both value labels stay in the chart's ink (r3b); the shuffled-answer band (a reference range)
     Black 20 grey, was Lavender Grey.
   - chart 3 (P3, p.8): the current measure (phi) Rust (line, dot and value label), the failed first
     measure grey as in r2. r2 had the current measure in Indigo.
   - chart 5 (P5, p.10): May Lavender Grey (edged in Iris so the light dot holds its outline on white
     and on the grey zone), June Indigo, November unchanged (hollow Indigo diamond). r2 had May Iris
     and June Indigo, which read too close at this dot size.

Run on the Mac (Akkurat Pro), from the worktree:
  AIAS_ROOT=<worktree> ~/aias/venv/bin/python reports/build_charts_aias_2_0_report_r3.py
"""
import json
import os
import sys
from pathlib import Path

import matplotlib.transforms
import numpy as np
from matplotlib.patches import Patch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_charts_aias_2_0_report as r2c  # noqa: E402  (r2's builder, unchanged)

# ---------------------------------------------------------------- source lines
R3_SOURCES = {
    "P1": ("AIAS 2.0 synthesis data; Methodology v1.9 (SSRN 7685126)",
           "AIAS 2.0 synthesis data; Methodology v1.9 (thirdsystem.ai; OSF)"),
    "P2": ("AIAS 2.0 synthesis data; v0.41 (SSRN 7685100); v1.9",
           "AIAS 2.0 synthesis data; v0.41 (thirdsystem.ai; OSF); v1.9"),
}
OUT_R3 = r2c.ROOT / "reports/figs/aias_2_0/report_r3"

# ---------------------------------------------------------------- colour roles (brand tokens)
# Pablo, Nov 12, 6:57 am: the roles are approved, with Consistency in Rust (Copper Plate keeps its
# challenger meaning). They are read from the committed tokens, brand/third_system_brand.json
# palette.measure_color_semantics, and their hex values asserted; no colour is invented.
BRAND_JSON = r2c.ROOT / "brand" / "third_system_brand.json"
EXPECTED_HEX = {"presence": "#37237B", "consistency": "#BD4718", "reference": "#CCCCCC",
                "failed_or_old": "#6E6E6E", "label_ink": "#1A1A1A",
                "waves_light_to_dark": ["#BBB9DD", "#908EC5", "#37237B"]}


def role_tokens(path: Path = BRAND_JSON) -> dict:
    sem = json.loads(Path(path).read_text(encoding="utf-8"))["palette"]["measure_color_semantics"]
    out = {k: sem[k]["hex"] for k in EXPECTED_HEX}
    for k, want in EXPECTED_HEX.items():
        if out[k] != want:
            raise SystemExit(f"measure colour role {k} is {out[k]}, expected {want}")
    return out


_R = role_tokens()
ROLE = {
    "presence": _R["presence"],                        # Indigo
    "consistency": _R["consistency"],                  # Rust
    "reference": _R["reference"],                      # Black 20 (reference band)
    "failed_old": _R["failed_or_old"],                 # grey (retired measure)
    "wave_early": _R["waves_light_to_dark"][0],        # Lavender Grey
    "wave_early_edge": _R["waves_light_to_dark"][1],   # Iris (outline of the light dot)
    "wave_late": _R["waves_light_to_dark"][2],         # Indigo
}
assert _R["label_ink"] == r2c.BLACK
INK = r2c.BLACK  # the chart's existing ink (#1A1A1A); p.7 labels stay in ink (r3b)


# ============================================================ P2, report-only copy (roles)
def chart_p2_roles():
    """r2's chart_p2 line for line; colours from the roles."""
    print("P2 (roles)")
    VER = r2c.VER
    pr, cr = VER["H_Presence_Score_Reliability"], VER["H_Consistency_Reliability"]
    nul = cr["frame_structure_null"]
    r2c.check("Presence retest rho", pr["rho"], 0.954, 3)
    r2c.checkn("Presence n", pr["n"], 112)
    r2c.check("Consistency retest rho", cr["rho"], 0.647, 3)
    r2c.checkn("Consistency n", cr["n"], 52)
    r2c.check("shuffled-answer null mean", nul["null_mean"], 0.438, 3)
    r2c.check("shuffled-answer null 95th pct", nul["null_p95"], 0.585, 3)
    marks = (0.80, 0.50)
    h = 3.2
    fig = r2c.frame("P2", h)
    ax = r2c.place(fig, h, 0.25, 0.96, 0.62, 0.12)
    rows = [("Presence", pr["rho"], pr["n"], marks[0], None, ROLE["presence"]),
            ("Consistency", cr["rho"], cr["n"], marks[1], nul, ROLE["consistency"])]
    ys = [1, 0]
    for y, (lab, v, n, mk, null, col) in zip(ys, rows):
        ax.plot([0, 1], [y, y], color=r2c.LIGHT, lw=0.8, zorder=0)
        if null:
            ax.plot([null["null_mean"], null["null_p95"]], [y, y], color=ROLE["reference"], lw=9,
                    solid_capstyle="butt", zorder=1)
            ax.text((null["null_mean"] + null["null_p95"]) / 2, y - 0.2,
                    f"shuffled answers: mean {null['null_mean']:.3f}, 95th percentile {null['null_p95']:.3f}",
                    ha="center", va="top", fontsize=7.4, color=r2c.GRAY)
        ax.plot([mk, mk], [y - 0.14, y + 0.14], color=r2c.LIMIT, lw=1.4, zorder=2)
        ax.text(mk, y + 0.18, f"pass mark {mk:.2f}", ha="center", va="bottom", fontsize=7.4, color=r2c.LIMIT)
        ax.scatter([v], [y], s=78, color=col, zorder=3, edgecolor="white", lw=0.7)
        ax.text(v + 0.025 if null else v, y if null else y - 0.2, f"{v:.3f}  (n = {n})",
                ha="left" if null else "center", va="center" if null else "top", fontsize=9,
                color=INK, fontweight="bold")
    ax.set_yticks(ys)
    ax.set_yticklabels([r[0] for r in rows], fontsize=9, fontweight="bold")
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.6, 1.55)
    ax.set_xlabel("rank correlation between the June and November waves", fontsize=8.4)
    r2c.clean(ax, left=False)
    ax.tick_params(axis="y", length=0)
    r2c.save(fig, "report_fig_02_brand_order_kept")


# ============================================================ P3, report-only copy (roles)
def chart_p3_roles():
    """r2's chart_p3 line for line; the current Consistency measure takes Rust (Pablo, Nov 12,
    6:57 am), the failed first measure stays grey. Rust passes as text (5.15:1 on white), so the
    value label keeps r2's colour-coding."""
    print("P3 (roles)")
    V18 = r2c.V18
    first = V18["H_CV_Reproduces"]["stat"]
    cur = V18["H_MeanIndependent"]["stat"]["pooled"]
    r2c.check("first measure (CV) |rho| with mean recall", first["abs_rho"], 0.682, 3)
    r2c.checkn("first measure n", first["n"], 55)
    r2c.check("current measure (phi) |rho| with mean recall", cur["abs_rho"], 0.091, 3)
    r2c.checkn("current measure n", cur["n"], 197)
    h = 2.8
    fig = r2c.frame("P3", h)
    ax = r2c.place(fig, h, 0.30, 0.96, 0.62, 0.12)
    rows = [("First measure\n(coefficient of variation)", first["abs_rho"], first["n"], False),
            ("Current measure\n(phi)", cur["abs_rho"], cur["n"], True)]
    ys = [1, 0]
    for y, (lab, v, n, cur_) in zip(ys, rows):
        col = ROLE["consistency"] if cur_ else ROLE["failed_old"]
        ax.plot([0, v], [y, y], color=col, lw=1.6, alpha=0.5, zorder=1)
        ax.scatter([v], [y], s=70, color=col, zorder=3, edgecolor="white", lw=0.7)
        ax.text(v + 0.016, y, f"{v:.3f}  (n = {n})", va="center", ha="left", fontsize=9,
                color=col, fontweight="bold")
    ax.axvline(0.50, color=r2c.LIMIT, lw=1.0, ls="--", zorder=0)
    ax.text(0.505, 1.5, "0.50 independence ceiling", fontsize=7.4, color=r2c.LIMIT, ha="left", va="bottom")
    ax.set_yticks(ys)
    ax.set_yticklabels([r[0] for r in rows], fontsize=8.6, linespacing=1.35)
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.6, 1.7)
    ax.set_xlabel("rank correlation with mean recall (absolute value)", fontsize=8.4)
    r2c.clean(ax)
    ax.tick_params(axis="y", length=0)
    r2c.save(fig, "report_fig_03_agreement_vs_naming")


# ============================================================ P5, report-only copy (wave tints)
def chart_p5_roles():
    """r2's chart_p5 line for line; May and June take the light and dark ends of the ramp."""
    print("P5 (roles)")
    CAL, VER = r2c.CAL, r2c.VER
    cands = CAL["candidates"]
    assert len(cands) == 8
    limit = CAL["constants"]["K2"]
    r2c.check("limit rho(A,P)", limit, 0.95, 2)
    sel = next(i for i, c in enumerate(cands) if c["spec"] == "C_phi+FLOOR+ADD")
    nov = VER["H_NoComposite_t3"]["rho_A_P"]
    r2c.check("November floored average rho(A,P)", nov, 0.969, 3)
    floored = [c for c in cands if c["low_count"] == "FLOOR"]
    fvals = [abs(c[t]["K2"]["rho"]) for c in floored for t in ("t1", "t2")]
    r2c.check("floored min", min(fvals), 0.971, 3)
    r2c.check("floored max", max(fvals), 0.997, 3)
    h = 4.8
    fig = r2c.frame("P5", h)
    ax = r2c.place(fig, h, 0.255, 0.67, 1.05, 0.30)
    y = np.arange(len(cands))[::-1]
    names, fails = [], []
    for i, c in enumerate(cands):
        m, j = abs(c["t1"]["K2"]["rho"]), abs(c["t2"]["K2"]["rho"])
        ax.plot([m, j], [y[i], y[i]], color=r2c.LIGHT, lw=1.2, zorder=1)
        ax.scatter([m], [y[i]], s=34, color=ROLE["wave_early"], edgecolor=ROLE["wave_early_edge"], lw=0.9,
                   zorder=3, label="May" if i == 0 else None)
        ax.scatter([j], [y[i]], s=34, color=ROLE["wave_late"], zorder=3, label="June" if i == 0 else None)
        names.append(f"{r2c.LAB[c['consistency']]} · {r2c.LAB[c['low_count']]} · {r2c.LAB[c['form']]}")
        failed = [k for k in ("K1", "K2", "K3") if not (c["t1"][k]["pass"] and c["t2"][k]["pass"])]
        assert failed, "every candidate fails at least one condition"
        fails.append(" · ".join(r2c.CONDITION[k] for k in failed))
    ax.scatter([nov], [y[sel]], s=50, marker="D", facecolor="white", edgecolor=r2c.INDIGO, lw=1.3, zorder=4,
               label="November, floored average")
    ax.axvline(limit, color=r2c.LIMIT, lw=1.0, ls="--", zorder=2)
    ax.axvspan(limit, 1.0, color="#E4E4E4", alpha=0.55, lw=0, zorder=0)
    ax.set_xlim(0.92, 1.0)
    ax.set_ylim(-0.6, len(cands) - 0.4)
    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=8)
    ax.set_xticks([0.92, 0.94, 0.96, 0.98, 1.0])
    ax.set_xlabel("rank correlation of the combined score with Presence", fontsize=8.4)
    ax.text(limit - 0.0015, y[0] + 0.62, "limit 0.95", ha="right", va="bottom", fontsize=7.4, color=r2c.LIMIT)
    r2c.clean(ax)
    ax.tick_params(axis="y", length=0)
    blend = matplotlib.transforms.blended_transform_factory(ax.transAxes, ax.transData)
    ax.text(1.03, len(cands) - 0.4, "Conditions failed", transform=blend, fontsize=8, fontweight="bold",
            color=r2c.BLACK, ha="left", va="bottom", clip_on=False)
    for i, f in enumerate(fails):
        ax.text(1.03, y[i], f, transform=blend, fontsize=7.4, color=r2c.BLACK, ha="left", va="center", clip_on=False)
    hs, ls = ax.get_legend_handles_labels()
    hs.append(Patch(facecolor="#E4E4E4", edgecolor="none")); ls.append("fails the 0.95 limit")
    ax.legend(hs, ls, loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=4, fontsize=7.6, frameon=False,
              columnspacing=1.2, handletextpad=0.4)
    r2c.save(fig, "report_fig_05_combined_scores")


CHARTS = {"P1": r2c.chart_p1, "P2": chart_p2_roles, "P3": chart_p3_roles, "P5": chart_p5_roles}


def main() -> None:
    for key, (old, new) in R3_SOURCES.items():
        if r2c.SPECS[key]["source"] != old:
            raise SystemExit(f"{key}: r2 source is {r2c.SPECS[key]['source']!r}, expected {old!r}")
    for key, spec in r2c.SPECS.items():
        if ("SSRN 7685126" in spec["source"] or "SSRN 7685100" in spec["source"]) and key not in R3_SOURCES:
            raise SystemExit(f"{key} cites an unposted SSRN paper and is not replaced")
    OUT_R3.mkdir(parents=True, exist_ok=True)
    r2c.OUT = OUT_R3  # save() writes here; r2's folder is left alone
    print("roles:", ROLE, "| tokens", BRAND_JSON)
    for key, (old, new) in R3_SOURCES.items():
        print(f"{key}: source '{old}' -> '{new}'")
        r2c.SPECS[key] = dict(r2c.SPECS[key], source=new)  # in memory only
    for key in ("P1", "P2", "P3", "P5"):
        CHARTS[key]()
    print(f"done -> {OUT_R3}")


if __name__ == "__main__":
    main()
