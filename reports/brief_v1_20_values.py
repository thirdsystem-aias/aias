#!/usr/bin/env python3
"""
brief_v1_20_values.py -- every number printed in the Sentiment Paper A brief (TS-CS-v1.20-r1) and its chart.

Numbers are read by code, never typed:
  * result values from the study's machine outputs, through papers/v1_20/v120_values.py (the paper's own loader
    and Values class: each printed value records source file, JSON path, raw value and format);
  * decision lines (0.30 / 0.50 bands, the 2% halt, the 0.667 / 0.80 agreement lines, the six-unit floor) from the
    locked scorer's constants (scripts/score_v1_11.py, read with ast, not imported), recorded as kind "rule".

write_provenance() writes reports/briefs/v1_20/brief_v1_20_provenance.json (number -> source key).
ROOT is the worktree (AIAS_ROOT, or this file's parent's parent), never the main tree.
"""
from __future__ import annotations

import ast
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(os.environ.get("AIAS_ROOT") or Path(__file__).resolve().parents[1]).resolve()
sys.path.insert(0, str(ROOT / "papers/v1_20"))
import v120_values as VV  # noqa: E402

OUTPUTS = ROOT / "osf/methodology/v1_20/outputs"
SCORER = ROOT / "scripts/score_v1_11.py"
PAPER_MD = ROOT / "papers/v1_20/v1_20_paper_draft.md"
PROV_OUT = ROOT / "reports/briefs/v1_20/brief_v1_20_provenance.json"


# ------------------------------------------------------------------ formats used by the brief
def r3(x):
    return VV.r3(x)


def r2(x):
    return VV.r2(x)


def i0(x):
    return VV.i0(x)


def pct0(x):
    return VV.pct0(x)


def pct2(x):
    return VV.pct2(x)


def usd(x):
    return f"US${float(x):,.2f}"


def pts2(x):
    """signed points with a true minus, e.g. -0.55"""
    return VV.sf2(x)


def d_absmax(*xs):
    return float(max(abs(float(x)) for x in xs))


def d_unique(items, field="category"):
    return float(len({(e.get("block"), e.get(field)) for e in items if e.get("block") == "E"}))


def scorer_constants(path=SCORER):
    """Module-level NAME = literal assignments of the locked scorer (ast; the file is not executed)."""
    tree = ast.parse(Path(path).read_text(encoding="utf-8"))
    out = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            try:
                out[node.targets[0].id] = ast.literal_eval(node.value)
            except Exception:
                pass
    return out


class BriefValues(VV.Values):
    def rule(self, name, const, fmt, consts):
        raw = consts[const]
        s = fmt(raw)
        self.vals[name] = s
        self.prov[name] = {"kind": "rule", "source": "scripts/score_v1_11.py", "constant": const, "raw": raw,
                           "fmt": fmt.__name__, "formatted": s}
        return s


def cheil_sentence(md_path=PAPER_MD):
    """The Cheil Worldwide / Iris sentence of the paper's Declarations (the v1.12 wording), read from the paper,
    with the group named as the employer's group: the brief does not name the employer (Samsung is named only in
    the paper's Declarations)."""
    txt = Path(md_path).read_text(encoding="utf-8")
    m = re.search(r"Cheil Worldwide, [^\n]*?\(conflict-of-interest screen of v0\.62, DEVIATIONS Entry 0, Part F\)\.", txt)
    if not m:
        raise SystemExit("Cheil sentence not found in the paper's Declarations")
    s = m.group(0)
    old = "a marketing company of the Samsung group in which Samsung Electronics holds 28.43%,"
    if old not in s:
        raise SystemExit("Cheil sentence differs from the v1.12 wording")
    s = s.replace(old, "a marketing company of the employer's group,")
    s = s.replace(" (conflict-of-interest screen of v0.62, DEVIATIONS Entry 0, Part F).", ".")
    if "Samsung" in s:
        raise SystemExit("Cheil sentence still names the employer")
    return s


def load():
    src = VV.load_sources(OUTPUTS)
    if VV.is_synthetic(src):
        raise SystemExit("refusing synthetic / dry-run outputs")
    V = src["verdicts"]
    if V.get("role_of_these_verdicts", "").find("Sentiment Paper A") < 0:
        raise SystemExit("v1_20_verdicts.json is not marked as Sentiment Paper A's result")
    k = scorer_constants()
    v = BriefValues(src)
    H = lambda *p: ["VERDICTS", *p]  # noqa: E731

    # -- verdict words (scorer's words, for checks only; the brief prints no hypothesis labels)
    words = {h: V["VERDICTS"][h] for h in V["VERDICTS"]}

    # -- reliability
    v.put("ALPHA", "verdicts", ["H1_Judge_Agreement", "alpha_ordinal"], r3)
    v.put("BRHO", "verdicts", ["H1_Judge_Agreement", "brand_rho", "rho"], r3)
    v.put("BRHO_N", "verdicts", ["H1_Judge_Agreement", "brand_rho", "n"], i0)
    v.put("PAIRS", "verdicts", ["H1_Judge_Agreement", "units_judged_by_both"], i0)
    v.put("H9", "verdicts", ["H9_Self_Preference", "delta_points"], pts2)
    # -- stability
    v.put("H4", "verdicts", ["H4_Stability_Short", "rho"], r3)
    v.put("H4_N", "verdicts", ["H4_Stability_Short", "n"], i0)
    v.put("H6", "verdicts", ["H6_Stability_Long", "rho"], r3)
    v.put("H6_N", "verdicts", ["H6_Stability_Long", "n"], i0)
    # -- separability
    for w in VV.WAVES:
        v.put(f"H2_{w}", "verdicts", ["H2_Sep_Presence", "per_wave", w, "rho"], r3)
        v.put(f"H2_{w}_N", "verdicts", ["H2_Sep_Presence", "per_wave", w, "n"], i0)
        v.put(f"H3_{w}", "verdicts", ["H3_Sep_Consistency", "per_wave", w, "rho"], r3)
    v.derive("H3_MAX", d_absmax, [("verdicts", ["H3_Sep_Consistency", "per_wave", w, "rho"]) for w in VV.WAVES], r2)
    v.derive("H5_MIN", VV.d_min, [("verdicts", ["H5_Sep_Ranking", "per_wave", w, "rho"]) for w in VV.WAVES], r3)
    v.derive("H5_MAX", VV.d_max, [("verdicts", ["H5_Sep_Ranking", "per_wave", w, "rho"]) for w in VV.WAVES], r3)
    v.put("H7", "verdicts", ["H7_Naming_Frequency", "rho"], r3)
    v.put("SCUT_T3", "verdicts", ["sensitivities", "S_CUT_without_cut_answers", "H2_Sep_Presence", "per_wave", "t3",
                                  "rho"], r3)
    v.put("CUT_ANSWERS", "verdicts", ["cut_list", "answers_flagged"], i0)
    v.derive("N_EARLY_CATS", d_unique, [("verdicts", ["descriptives", "baseline"])], i0)
    # -- the halt of v1.11's rule and v1.20's result on the same replies
    v.put("V111_FAIL", "comparison", ["outcome_counts", "v1.11 rule", "J1", "JUDGE_FAIL"], i0)
    c11 = ["outcome_counts", "v1.11 rule", "J1"]
    sent = [("comparison", c11 + ["VALID"]), ("comparison", c11 + ["JUDGE_FAIL"])]  # units sent to J1
    v.derive("UNITS", VV.d_sum, sent, i0)
    v.derive("V111_SHARE", lambda f, a, b: VV.d_ratio(f, VV.d_add(a, b)),
             [("comparison", c11 + ["JUDGE_FAIL"])] + sent, pct2)
    v.prov["V111_SHARE"]["fn"] = "JUDGE_FAIL / (VALID + JUDGE_FAIL)"
    v.derive("V111_HALTS", VV.d_len, [("comparison", ["halts", "v1.11 rule"])], i0)
    v.derive("SETS", VV.d_count, [("comparison", ["judge_fail_by_judge_set", s, "v1.11 rule", "fail_share"])
                                  for s in sorted(src["comparison"]["judge_fail_by_judge_set"]) if s.startswith("J1 ")],
             i0)
    v.derive("V120_FAIL", VV.d_signed, sent + [("comparison", ["outcome_counts", "v1.20 rule", "J1", "VALID"])],
             i0, consts=((1, 1, -1),))  # units sent minus units valid under the v1.20 rule
    # -- run
    v.put("CALLS", "frozen", ["records"], i0)
    v.put("SPEND", "frozen", ["spend_usd"], usd)
    # -- decision lines of the locked scorer
    v.rule("BAND_LO", "BAND_CONFIRMED_MAX", r2, k)
    v.rule("BAND_HI", "BAND_FALSIFIED_MIN", r2, k)
    v.rule("ALPHA_MIN", "ALPHA_CONFIRMED_MIN", r3, k)
    v.rule("BRHO_MIN", "BRAND_AGREE_CONFIRMED_MIN", r2, k)
    v.rule("STAB_MIN", "STAB_CONFIRMED_MIN", r2, k)
    v.rule("HALT", "JUDGE_FAIL_HALT_SHARE", pct0, k)
    v.rule("NFLOOR", "N_FLOOR", i0, k)
    v.rule("SELFPREF_MAX", "SELF_PREF_OK_MAX", i0, k)

    # -- consistency checks between the words of the brief and the scorer's verdicts (stop on any mismatch)
    expect = {"H1": "CONFIRMED", "H2": "FALSIFIED", "H3": "CONFIRMED", "H4": "CONFIRMED", "H6": "CONFIRMED",
              "H7": "FALSIFIED", "H9": "CONFIRMED"}
    bad = {h: words[h] for h, w in expect.items() if words[h] != w}
    if bad:
        raise SystemExit(f"the brief's wording assumes other verdicts: {bad}")
    if V["sensitivities"]["S_CUT_without_cut_answers"]["H2_Sep_Presence"]["verdict"] != "MARGINAL":
        raise SystemExit("S-CUT H2 is not MARGINAL; the 'how firm' sentence does not apply")
    sd = V["sensitivities"]["SD_without_Denon_v0_19"]
    sd_same = all(sd[h]["verdict"] == words[VV.SHORT[h]] for h in VV.HYPS if h in sd and "verdict" in sd[h])
    if not sd_same:
        raise SystemExit("a verdict changes without Denon; the disclosure sentence does not apply")
    if words["H5"] != "MARGINAL" or words["H8"] != "MARGINAL":
        raise SystemExit("H5/H8 not MARGINAL; the Ranking sentence does not apply")
    if V["v1_11_stage_j"]["case"] != "B" or V["v1_11_stage_j"]["state"] != "halted":
        raise SystemExit("v1.11 did not halt (case B); the 'how the result was reached' text does not apply")
    if any(float(V["H2_Sep_Presence"]["per_wave"][w]["rho"]) <= 0 for w in VV.WAVES):
        raise SystemExit("a Presence correlation is not positive; 'warmer' wording does not apply")
    v.word("SD_SAME", "the same verdicts", "sensitivities.SD_without_Denon_v0_19.*.verdict == VERDICTS.*")
    v.word("CHEIL", cheil_sentence(), "papers/v1_20/v1_20_paper_draft.md Declarations, Cheil sentence (v1.12 wording),"
           " employer's name replaced by 'the employer's group'")
    return v, src


def chart_data(src):
    V = src["verdicts"]
    rows = {}
    for key, h in (("presence", "H2_Sep_Presence"), ("consistency", "H3_Sep_Consistency")):
        rows[key] = [{"wave": w, "rho": V[h]["per_wave"][w]["rho"], "lo": V[h]["per_wave"][w]["ci95"][0],
                      "hi": V[h]["per_wave"][w]["ci95"][1], "n": V[h]["per_wave"][w]["n"],
                      "path": ["verdicts", h, "per_wave", w]} for w in VV.WAVES]
    return rows


def write_provenance(v, extra=None):
    PROV_OUT.parent.mkdir(parents=True, exist_ok=True)
    out = {"_note": "Every number printed in TS-CS-v1.20-r1 and its chart: name -> source file, JSON path (or locked "
                    "scorer constant), raw value, format. Sources: osf/methodology/v1_20/outputs/ (verdicts "
                    "v1_20_verdicts.json, stage_j, comparison), osf/methodology/v1_11/outputs/ (frozen).",
           "sources_sha256": {k: VV.sha256(VV.source_path(OUTPUTS, k)) for k in ("verdicts", "stage_j", "comparison",
                                                                               "frozen")},
           "values": v.prov}
    if extra:
        out.update(extra)
    PROV_OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    return PROV_OUT


if __name__ == "__main__":
    v, src = load()
    for n, s in v.vals.items():
        print(f"{n:<14} {s if len(s) < 90 else s[:90] + '...'}")
