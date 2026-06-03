#!/usr/bin/env python3
"""
build_charts_v30.py — AIAS v0.30 (CV.04) figure builder.

Builds the four CV.04 discriminant-validity figures from the LOCKED artifacts:
  - osf/v30/data/v0.30_presence.csv   (v0.30-acquisition-locked)
  - prereg/v0_30_brand_validator.csv  (v0.30-prereg-r1)
  - osf/v30/v30_verdicts.json         (v0.30-results-locked)

Figures (saved to --fig-dir, default reports/figs/):
  chart_28_verdict_bands.pdf          |rho| + BCa CI against the three |rho| bands
  chart_28_discriminant_scatters.pdf  Presence vs familiarity AND vs recognition d'
  chart_28_dissociation.pdf           within-panel z(Presence) - z(familiarity), all 24
  chart_28_presence_composition.pdf   C_P / R_cat / R_cult contributions to Presence

SELF-CHECK (the integrity guard): figure 3 recomputes the within-panel z-difference
for all 24 brands and ASSERTS it reconciles with the 11 threshold-crossers recorded
in v30_verdicts.json. If the standardization (ddof) differs from score_v30.py, the
build aborts with a message telling you to flip Z_DDOF — it will NOT ship a figure
inconsistent with the locked verdict.

================ RECONCILE BEFORE RUNNING (assumptions I can't verify from here) ===
 1. chart_style API. Assumed: setup(); add_header(fig, title, subtitle);
    add_footer(fig); PALETTE (dict or obj); FIGSIZE['hero'|'tall'|'short'];
    FONT_SIZES; SAVEFIG_PARAMS (dict); diverging_pair() -> (indigo_hex, warm_hex).
    Header/footer are called defensively (warn + continue on signature mismatch);
    the rest fall back to the literal brand tokens below if import fields differ.
 2. CSV columns. Assumed presence.csv -> brand, C_P, R_cat, R_cult, presence ;
    validator.csv -> brand, familiarity, dprime. Edit COL_* below if named otherwise.
    (If the bridge wrote only brand,presence, fig 4 will report the missing columns
    and skip — point COMPONENTS_FROM at a file that has C_P/R_cat/R_cult, or tell me.)
 3. Z_DDOF. score_v30.py's within-panel z standardization: 0 = population, 1 = sample.
    Default 0; the self-check fails loudly and names the fix if it's wrong.
 4. verdicts.json shape. Read flexibly via _dig() with candidate key names; if a field
    isn't found the script prints the actual keys it saw so you can map them.
====================================================================================

Build tooling — NOT a pre-reg artifact. Commit normally; no tags move.
"""

import argparse
import csv
import json
import math
import os
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# ----------------------------------------------------------------------------- #
# chart_style import (with literal-token fallback so the script still runs if a
# field name differs — reconcile per the header if you see a fallback warning).
# ----------------------------------------------------------------------------- #
try:
    import chart_style as cs
except Exception:                                            # noqa: BLE001
    sys.path.insert(0, str(Path("~/aias/scripts").expanduser()))
    import chart_style as cs                                 # type: ignore

# Brand tokens (literal fallbacks; prefer chart_style if it exposes them)
INDIGO = getattr(cs, "INDIGO", "#37237B")   # incumbent / discriminant / amplified
PETRO  = getattr(cs, "PETRO",  "#6A6AB1")   # mid-tier / PARTIAL band
COPPER = getattr(cs, "COPPER", "#F36C35")   # challenger / reducible / suppressed
INK    = getattr(cs, "INK",    "#1A1A1A")
GRID   = getattr(cs, "GRID",   "#D8D8DE")

# Verdict-logic constants — these are the LOCKED pre-reg bands; do not edit.
BAND_CONFIRMED = 0.50    # |rho| < 0.50            -> CONFIRMED (discriminant)
BAND_FALSIFIED = 0.74    # |rho| >= 0.74           -> FALSIFIED (reducible)
BENCHMARK      = 0.74    # convergent benchmark (v0.25 Presence x Google Trends)

# Within-panel z standardization. RECONCILE with score_v30.py (see header item 3).
Z_DDOF = 0
Z_TOL  = 0.02            # match tolerance vs verdicts' 2-dp stored z values

# CSV column names (edit if your headers differ — header item 2)
COL_BRAND = "brand"
COL_CP, COL_RCAT, COL_RCULT, COL_PRESENCE = "C_P", "R_cat", "R_cult", "presence"
COL_FAM, COL_DPRIME = "familiarity_1_7", "dprime"

# Display-name fixups for labels only (NOT used for joining)
DISPLAY = {"Netapp": "NetApp", "netapp": "NetApp"}

# Component fraction-of-max denominators (Protocol v1.6, r2-pinned)
CP_MAX, RCAT_MAX, RCULT_MAX = 6, 18, 18


# ----------------------------------------------------------------------------- #
# Loading helpers
# ----------------------------------------------------------------------------- #
def _read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _disp(name):
    return DISPLAY.get(name, name)


def _dig(d, *candidates, required=True):
    """Pull the first present key from a dict, trying several plausible names."""
    for c in candidates:
        if isinstance(d, dict) and c in d:
            return d[c]
    if required:
        raise KeyError(
            f"none of {candidates} found. Keys present: {list(d.keys()) if isinstance(d, dict) else type(d)}"
        )
    return None


def load_inputs(presence_csv, validator_csv, verdicts_json):
    pres = {r[COL_BRAND]: r for r in _read_csv(presence_csv)}
    vald = {r[COL_BRAND]: r for r in _read_csv(validator_csv)}

    brands = [b for b in pres if b in vald]
    dropped = (set(pres) | set(vald)) - set(brands)
    if dropped:
        print(f"[warn] {len(dropped)} brand(s) not joined 1:1: {sorted(dropped)}")
    if len(brands) != 24:
        print(f"[warn] n_joined = {len(brands)} (expected 24) — check brand-name match")

    rows = []
    have_components = all(
        c in next(iter(pres.values())) for c in (COL_CP, COL_RCAT, COL_RCULT)
    )
    for b in brands:
        p, v = pres[b], vald[b]
        row = {
            "brand": b,
            "presence": float(p[COL_PRESENCE]),
            "familiarity": float(v[COL_FAM]),
            "dprime": float(v[COL_DPRIME]),
        }
        if have_components:
            row["C_P"] = float(p[COL_CP])
            row["R_cat"] = float(p[COL_RCAT])
            row["R_cult"] = float(p[COL_RCULT])
        rows.append(row)

    with open(verdicts_json, encoding="utf-8") as f:
        verdicts = json.load(f)

    return rows, verdicts, have_components


def hyp(verdicts, *name_candidates):
    """Locate one hypothesis dict in verdicts.json under any of several names."""
    # verdicts may be {hyp: {...}} or {"hypotheses": {hyp: {...}}} etc.
    for container in (verdicts.get("verdicts", {}), verdicts, verdicts.get("hypotheses", {})):
        for n in name_candidates:
            if isinstance(container, dict) and n in container:
                return container[n]
    raise KeyError(f"hypothesis {name_candidates} not found; top keys: {list(verdicts.keys())}")


def abs_ci(h):
    """Return (|rho|, (abs_ci_lo, abs_ci_hi), verdict_str)."""
    rho_abs = abs(float(_dig(h, "abs_rho", "rho_abs", "spearman_rho", "rho")))
    flags = _dig(h, "flags", required=False) or {}
    ci = _dig(flags, "ci_abs_interval", required=False) or _dig(h, "rho_abs_ci", "abs_ci", required=False)
    if ci is None:
        signed = _dig(h, "bca_ci_95", "bca_ci", "ci", "ci95")
        lo, hi = float(signed[0]), float(signed[1])
        a_lo = 0.0 if lo <= 0 <= hi else min(abs(lo), abs(hi))
        a_hi = max(abs(lo), abs(hi))
        ci = [a_lo, a_hi]
    verdict = str(_dig(h, "status", "verdict", "result", required=False) or "")
    return rho_abs, (float(ci[0]), float(ci[1])), verdict.upper()


# ----------------------------------------------------------------------------- #
# chrome + save
# ----------------------------------------------------------------------------- #
def _chrome(fig, title, subtitle=""):
    if hasattr(cs, "setup"):
        try:
            cs.setup()
        except Exception:                                    # noqa: BLE001
            pass
    for fn, args, kwargs in (
        ("add_header", (fig, title, subtitle), {}),
        ("add_footer", (fig,), {"phase": "v0.30"}),   # else chart_style defaults to v0.24
    ):
        f = getattr(cs, fn, None)
        if f is None:
            continue
        try:
            f(*args, **kwargs)
        except TypeError:
            # older chart_style.add_footer without a phase kwarg — fall back
            try:
                f(*args)
            except Exception as e:                           # noqa: BLE001
                print(f"[warn] chart_style.{fn} signature mismatch ({e}); skipping — reconcile API")
        except Exception as e:                               # noqa: BLE001
            print(f"[warn] chart_style.{fn} signature mismatch ({e}); skipping — reconcile API")


def _figsize(name, fallback):
    fs = getattr(cs, "FIGSIZE", {})
    try:
        return fs[name]
    except Exception:                                        # noqa: BLE001
        return fallback


def _save(fig, fig_dir, stem, bottom=None, top=None):
    adj = {}
    if bottom is not None:
        adj["bottom"] = bottom   # lift content clear of the footer/source line
    if top is not None:
        adj["top"] = top         # reserve headroom for the header/subtitle
    if adj:
        fig.subplots_adjust(**adj)
    params = getattr(cs, "SAVEFIG_PARAMS", {"dpi": 300, "bbox_inches": "tight"})
    out = Path(fig_dir) / f"{stem}.pdf"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, **params)
    plt.close(fig)
    print(f"  -> {out}")


# ----------------------------------------------------------------------------- #
# Figure 1 — verdict bands
# ----------------------------------------------------------------------------- #
def fig_verdict_bands(verdicts, fig_dir):
    fam = abs_ci(hyp(verdicts, "H_Disc_Familiarity"))
    rec = abs_ci(hyp(verdicts, "H_Disc_Recognition"))

    fig, ax = plt.subplots(figsize=_figsize("short", (9, 3.4)))

    # band shading
    ax.axvspan(0.0, BAND_CONFIRMED, color=INDIGO, alpha=0.12, lw=0)
    ax.axvspan(BAND_CONFIRMED, BAND_FALSIFIED, color=PETRO, alpha=0.14, lw=0)
    ax.axvspan(BAND_FALSIFIED, 1.0, color=COPPER, alpha=0.14, lw=0)
    for x in (BAND_CONFIRMED, BAND_FALSIFIED):
        ax.axvline(x, color=GRID, lw=1.0, zorder=1)
    ax.axvline(BENCHMARK, color=INK, lw=1.0, ls="--", alpha=0.55, zorder=1)

    rows = [("H_Disc_Recognition (secondary)", rec, 0), ("H_Disc_Familiarity (primary)", fam, 1)]
    for label, (rho_abs, (lo, hi), verdict), y in rows:
        ax.hlines(y, lo, hi, color=INK, lw=2.4, zorder=3)
        for xb in (lo, hi):
            ax.vlines(xb, y - 0.06, y + 0.06, color=INK, lw=2.0, zorder=3)
        ax.plot(rho_abs, y, "o", ms=11, color=INDIGO, mec="white", mew=1.4, zorder=4)
        ax.text(rho_abs, y + 0.17, f"|ρ| = {rho_abs:.3f}", ha="center", va="bottom",
                fontsize=10, color=INK)
        ax.text(1.02, y, verdict, ha="left", va="center", fontsize=10,
                fontweight="bold", color=INK)

    ax.set_yticks([0, 1])
    ax.set_yticklabels(["Recognition d′", "Familiarity"], fontsize=11)
    ax.set_ylim(-0.5, 1.6)
    ax.set_xlim(0, 1.18)
    ax.set_xlabel("|ρ|  (Spearman, Presence vs validator)", fontsize=11)
    ax.set_xticks([0, BAND_CONFIRMED, BAND_FALSIFIED, 1.0])

    # band captions
    ax.text(0.25, 1.42, "CONFIRMED\n(discriminant)", ha="center", va="center",
            fontsize=8.5, color=INDIGO)
    ax.text(0.62, 1.42, "PARTIAL", ha="center", va="center", fontsize=8.5, color=PETRO)
    ax.text(0.87, 1.42, "FALSIFIED\n(reducible)", ha="center", va="center",
            fontsize=8.5, color=COPPER)
    ax.text(BENCHMARK, -0.26, "0.74 benchmark", ha="center", va="top",
            fontsize=8, color=INK, alpha=0.7)

    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(left=False)

    _chrome(fig, "Discriminant verdicts against the |ρ| bands",
            "Point |ρ| with BCa 95% CI · n = 24 · seed 280400")
    _save(fig, fig_dir, "chart_28_verdict_bands", bottom=0.24, top=0.80)


# ----------------------------------------------------------------------------- #
# Figure 2 — discriminant scatters
# ----------------------------------------------------------------------------- #
def fig_scatters(rows, verdicts, fig_dir):
    labels = _crosser_names(verdicts)
    fam_rho = abs_ci(hyp(verdicts, "H_Disc_Familiarity"))
    rec_rho = abs_ci(hyp(verdicts, "H_Disc_Recognition"))

    fig, axes = plt.subplots(1, 2, figsize=_figsize("hero", (12, 5.2)))
    panels = [
        (axes[0], "familiarity", "Human familiarity (1–7)", fam_rho),
        (axes[1], "dprime", "Recognition sensitivity d′", rec_rho),
    ]
    for ax, xkey, xlab, (rho_abs, (lo, hi), verdict) in panels:
        xs = [r[xkey] for r in rows]
        ys = [r["presence"] for r in rows]
        ax.scatter(xs, ys, s=46, color=INDIGO, alpha=0.85, edgecolor="white", lw=0.8, zorder=3)
        for r in rows:
            if r["brand"] in labels:
                ax.annotate(_disp(r["brand"]), (r[xkey], r["presence"]),
                            xytext=(4, 4), textcoords="offset points",
                            fontsize=7.5, color=INK, alpha=0.85)
        ax.set_xlabel(xlab, fontsize=11)
        ax.set_ylabel("AIAS Presence (0–100)", fontsize=11)
        ax.set_ylim(-4, 104)
        ax.text(0.04, 0.96, f"ρ = {rho_abs:.3f}\nBCa [{lo:.2f}, {hi:.2f}]\n{verdict}",
                transform=ax.transAxes, va="top", ha="left", fontsize=9.5, color=INK,
                bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=GRID, lw=1))
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        ax.grid(axis="y", color=GRID, lw=0.6, alpha=0.5)

    fig.text(0.5, 0.10, "ρ is rank-based (Spearman); axes show raw values. Labelled points are the dissociation crossers.",
             ha="center", fontsize=8, color=INK, alpha=0.7)
    _chrome(fig, "Presence vs human brand norms",
            "Discriminant validity · two gating relationships · n = 24")
    _save(fig, fig_dir, "chart_28_discriminant_scatters", bottom=0.26)


# ----------------------------------------------------------------------------- #
# Figure 3 — dissociation (with the z self-check)
# ----------------------------------------------------------------------------- #
def _crosser_names(verdicts):
    return set(_crosser_values(verdicts).keys())


def _crosser_values(verdicts):
    """{brand: z_diff} for the recorded crossers (handles dict or list-of-pairs)."""
    h = hyp(verdicts, "H_Dissociation")
    out = {}
    for key in ("amplified", "amp", "suppressed", "supp"):
        grp = _dig(h, key, required=False)
        if not grp:
            continue
        if isinstance(grp, dict):
            out.update({k: float(v) for k, v in grp.items()})
        else:  # list of [name, val] or {"brand":, "z":}
            for item in grp:
                if isinstance(item, dict):
                    out[_dig(item, "brand", "name")] = float(_dig(item, "z", "z_diff", "value"))
                else:
                    out[item[0]] = float(item[1])
    return out


def fig_dissociation(rows, verdicts, fig_dir):
    n = len(rows)
    pres = [r["presence"] for r in rows]
    fam = [r["familiarity"] for r in rows]

    def zscore(xs):
        m = sum(xs) / len(xs)
        sd = math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - Z_DDOF))
        return [(x - m) / sd for x in xs]

    zp, zf = zscore(pres), zscore(fam)
    zdiff = {rows[i]["brand"]: zp[i] - zf[i] for i in range(n)}

    # ---- INTEGRITY SELF-CHECK: reconcile with the locked verdict's crossers ----
    expected = _crosser_values(verdicts)
    mismatches = {b: (zdiff[b], e) for b, e in expected.items()
                  if b in zdiff and abs(zdiff[b] - e) > Z_TOL}
    if mismatches:
        msg = "; ".join(f"{b}: recomputed {g:.3f} vs verdict {e:.3f}"
                        for b, (g, e) in mismatches.items())
        sys.exit(
            "ABORT (fig 3): recomputed within-panel z-diff does not match the locked "
            f"verdict for {len(mismatches)} brand(s) [{msg}]. "
            f"Most likely Z_DDOF is wrong — currently {Z_DDOF}; try {1 - Z_DDOF} and rerun. "
            "Not drawing a figure inconsistent with v30_verdicts.json."
        )
    print(f"  [self-check] z-diff reconciles with all {len(expected)} verdict crossers (Z_DDOF={Z_DDOF}) ✓")

    order = sorted(rows, key=lambda r: zdiff[r["brand"]])
    names = [_disp(r["brand"]) for r in order]
    vals = [zdiff[r["brand"]] for r in order]
    try:
        amp_c, sup_c = cs.diverging_pair()
    except Exception:                                        # noqa: BLE001
        amp_c, sup_c = INDIGO, COPPER
    colors = [amp_c if v >= 0 else sup_c for v in vals]

    fig, ax = plt.subplots(figsize=_figsize("tall", (8, 9)))
    ax.barh(range(n), vals, color=colors, edgecolor="white", lw=0.6, zorder=3)
    ax.set_yticks(range(n))
    ax.set_yticklabels(names, fontsize=8.5)
    ax.axvline(0, color=INK, lw=1.0)
    for t in (-1.0, 1.0):
        ax.axvline(t, color=GRID, lw=1.0, ls="--", zorder=1)
    ax.set_xlabel("z(Presence) − z(Familiarity)   within-panel", fontsize=11)
    ax.set_ylim(-0.6, n - 0.4)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(left=False)

    legend = [Patch(fc=amp_c, label="Presence ≫ familiarity (amplified)"),
              Patch(fc=sup_c, label="familiarity ≫ Presence (suppressed)")]
    ax.legend(handles=legend, loc="lower right", fontsize=8.5, frameon=False)

    _chrome(fig, "Presence–familiarity dissociation",
            "Within-panel standardized difference · ±1.0 thresholds · descriptive (non-gating)")
    _save(fig, fig_dir, "chart_28_dissociation", bottom=0.13)


# ----------------------------------------------------------------------------- #
# Figure 4 — Presence composition (the recall floor)
# ----------------------------------------------------------------------------- #
def fig_composition(rows, have_components, fig_dir):
    if not have_components:
        print("[warn] fig 4 skipped: presence.csv lacks C_P / R_cat / R_cult columns. "
              "Point COMPONENTS_FROM at a file that has them, or regenerate via bridge_v30.")
        return

    order = sorted(rows, key=lambda r: r["presence"])
    names = [_disp(r["brand"]) for r in order]
    # each component's contribution to the 0–100 mean (sums to presence)
    cp = [(r["C_P"] / CP_MAX * 100) / 3 for r in order]
    rcat = [(r["R_cat"] / RCAT_MAX * 100) / 3 for r in order]
    rcult = [(r["R_cult"] / RCULT_MAX * 100) / 3 for r in order]

    n = len(rows)
    fig, ax = plt.subplots(figsize=_figsize("hero", (12, 5.6)))
    ax.bar(range(n), cp, color=INDIGO, label="C_P (recognition)", zorder=3)
    ax.bar(range(n), rcat, bottom=cp, color=PETRO, label="R_cat (best/quality recall)", zorder=3)
    ax.bar(range(n), rcult, bottom=[a + b for a, b in zip(cp, rcat)],
           color=COPPER, label="R_cult (popular/iconic recall)", zorder=3)
    ax.set_xticks(range(n))
    ax.set_xticklabels(names, rotation=60, ha="right", fontsize=8)
    ax.set_ylabel("Contribution to AIAS Presence (0–100)", fontsize=11)
    ax.set_ylim(0, 104)
    ax.legend(loc="upper left", fontsize=9, frameon=False)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(axis="y", color=GRID, lw=0.6, alpha=0.5)

    _chrome(fig, "Presence composition by component",
            "Recall floors for the enterprise-heavy panel; Presence reduces toward C_P (recognition)")
    _save(fig, fig_dir, "chart_28_presence_composition", bottom=0.32)


# ----------------------------------------------------------------------------- #
def main():
    ap = argparse.ArgumentParser(description="Build the v0.30 (CV.04) figures.")
    root = Path("~/aias").expanduser()
    ap.add_argument("--presence", default=root / "osf/v30/data/v0.30_presence.csv")
    ap.add_argument("--validator", default=root / "prereg/v0_30_brand_validator.csv")
    ap.add_argument("--verdicts", default=root / "osf/v30/v30_verdicts.json")
    ap.add_argument("--fig-dir", default=root / "reports/figs")
    args = ap.parse_args()

    print("Loading locked artifacts…")
    rows, verdicts, have_components = load_inputs(args.presence, args.validator, args.verdicts)
    print(f"  joined n = {len(rows)} | components present: {have_components}")

    print("Building figures…")
    fig_verdict_bands(verdicts, args.fig_dir)
    fig_scatters(rows, verdicts, args.fig_dir)
    fig_dissociation(rows, verdicts, args.fig_dir)   # self-check inside
    fig_composition(rows, have_components, args.fig_dir)
    print("Done.")


if __name__ == "__main__":
    main()
