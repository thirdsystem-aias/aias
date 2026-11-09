#!/usr/bin/env python3
"""
build_charts_v40.py — v0.40 US airlines and retail banks report-register figures.
Scaffolded from build_charts_v39.py by aias_new_phase.py (fork-don't-rebuild). The v0.39 figures, titles,
focal brand and data loader were removed on 2026-11-08; the panel constants below match the v0.40 design.
Figures are defined after scoring and read the locked v0.40 outputs only. Third System chart standard
(chart_style.py). Writes PDFs to reports/figs/v40/report/ (or --out).
"""
import argparse
import csv
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import chart_style as CS  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

ROOT = Path(os.environ.get("AIAS_ROOT", "/Users/pablou/aias"))
P = CS.PALETTE
LEGACY = ["M1", "M2", "M3", "M4", "M5", "M6"]
CURRENT = ["C1", "C2", "C3"]
MODEL = {"M1": "Claude Opus 4.5", "M2": "Claude Sonnet 4.5", "M3": "GPT-4o", "M4": "GPT-4o-mini",
         "M5": "Gemini 2.5 Flash", "M6": "Gemini 2.5 Flash-Lite",
         "C1": "Claude Opus 5.5", "C2": "GPT-6 Astra", "C3": "Gemini 4 Argon"}
CELLS = [("L", "S0"), ("C", "S0"), ("C", "S1")]
CELL_LABEL = {("L", "S0"): "2024–25 models\n(fixed panel)", ("C", "S0"): "Current assistants,\nno search",
              ("C", "S1"): "Current assistants,\nwith web search"}
CELL_SHORT = {("L", "S0"): "2024–25 models", ("C", "S0"): "Current, no search", ("C", "S1"): "Current, with search"}
CELL_COLOR = {("L", "S0"): P["warm"], ("C", "S0"): P["indigo"], ("C", "S1"): P["indigo_t2"]}
PHASE, PROTOCOL = "v0.40", "TBD"  # protocol version set at the pre-registration lock

TEXT = {}  # per figure: title, subtitle, description; written after scoring


def pct(x):
    return f"{round(100 * x):d}%"


def save(fig, out, name):
    out.mkdir(parents=True, exist_ok=True)
    p = out / name
    fig.savefig(p, **CS.SAVEFIG_PARAMS)
    plt.close(fig)
    print("  wrote", p)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(ROOT / "osf/v40"))
    ap.add_argument("--out", default=str(ROOT / "reports/figs/v40/report"))
    ap.parse_args()
    CS.setup()
    print("build_charts_v40: no v0.40 figures are defined yet; they follow the pre-registration lock and scoring.")


if __name__ == "__main__":
    main()
