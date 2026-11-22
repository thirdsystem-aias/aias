#!/usr/bin/env python3
"""
brief_v0_43_values.py -- every number printed in the v0.43 predictive-validity brief (TS-BR-v0.43-r1) and its chart.

Numbers are read by code, never typed:
  * results from the study's verdict file osf/v43/v43_stage1_verdicts.json (the scorer's single Stage 1 run, branch
    v0.43 commit 3ed9e1d), through the Values class of papers/v1_12/v112_values.py (each printed value records
    source, JSON path, raw value and format);
  * decision lines from the locked scorer osf/v43/scripts/score_v0_43.py, which writes them as literals in its
    verdict() function and its checks (0.15 with p < 0.05 confirms, a 90% upper bound under 0.10 falsifies, 0.10 for
    marginal, REVERSED at two-sided p < 0.05; check lines 0.30 and 0.70) and as constants (MIN_N, MIN_N_CONS). The
    source is read as text (not imported or executed); each rule records the exact source line it was taken from.

Source files are checked out unchanged from branch v0.43-paper (05a5561); the verdict file and the scorer are
byte-identical to branch v0.43. write_provenance() writes reports/briefs/v0_43/brief_v0_43_provenance.json.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(os.environ.get("AIAS_ROOT") or Path(__file__).resolve().parents[1]).resolve()
sys.path.insert(0, str(ROOT / "papers/v1_12"))
sys.path.insert(0, str(ROOT / "reports"))
import v112_values as VV  # noqa: E402
from brief_v1_12_values import scorer_constants as _consts  # noqa: E402

VERDICTS = ROOT / "osf/v43/v43_stage1_verdicts.json"
SCORER = ROOT / "osf/v43/scripts/score_v0_43.py"
PAPER_MD = ROOT / "papers/v0_43/v0_43_paper_draft.md"
PROV_OUT = ROOT / "reports/briefs/v0_43/brief_v0_43_provenance.json"
SOURCE_COMMIT = "05a5561 (branch v0.43-paper; verdict file as written by the single Stage 1 run at 3ed9e1d)"
TESTS = ["H_Pred_Presence", "H_Pred_Presence_SA", "H_Pred_Presence_Momentum", "H_Pred_Consistency"]

# (name, regex on the scorer source with one group = the literal, the source line must match exactly once)
RULE_LINES = {
    "CONF": r"if rho >= (0\.15) and p_one < 0\.05:",
    "ALPHA": r"if rho >= 0\.15 and p_one < (0\.05):",
    "FALS": r"elif ci90_hi is not None and ci90_hi < (0\.10):",
    "REV_ALPHA": r'labels = \["REVERSED"\] if \(rho < 0 and p_two < (0\.05)\) else \[\]',
    "CONC_LINE": r'conc\["rho"\] >= (0\.30) and conc\.get\("p_one", 1\) < 0\.05\)',
    "REL_LINE": r"rel_ok = bool\(rel is not None and rel >= (0\.70)\)",
}


def r3(x):
    return VV.r3(x)


def m3(x):
    return VV.r3(x).replace("-", "−")


def r2(x):
    return VV.r2(x)


def i0(x):
    return VV.i0(x)


def f4(x):
    return f"{float(x):.4f}"


def pct0(x):
    return f"{100 * float(x):.0f}%"


def a3(x):
    return f"{abs(float(x)):.3f}"


def scorer_rules():
    src = SCORER.read_text(encoding="utf-8")
    out = {}
    for name, pat in RULE_LINES.items():
        hits = re.findall(pat, src)
        if len(hits) != 1:
            raise SystemExit(f"rule {name}: {len(hits)} matches in {SCORER.name}")
        out[name] = (float(hits[0]), pat)
    k = _consts(SCORER)
    out["MIN_N"] = (k["MIN_N"], "MIN_N, MIN_N_CONS = 60, 30")
    out["MIN_N_C"] = (k["MIN_N_CONS"], "MIN_N, MIN_N_CONS = 60, 30")
    return out


class BriefValues(VV.Values):
    def rule(self, name, rules, fmt):
        raw, line = rules[name]
        s = fmt(raw)
        self.vals[name] = s
        self.prov[name] = {"kind": "rule", "source": str(SCORER.relative_to(ROOT)), "source_line": line, "raw": raw,
                           "fmt": fmt.__name__, "formatted": s}
        return s


def _md():
    return PAPER_MD.read_text(encoding="utf-8")


def cheil_sentence():
    """The paper's Cheil Worldwide / Iris sentence, with the affiliate named as part of the employer's group."""
    m = re.search(r"Cheil Worldwide, a Samsung affiliate, or its Iris unit has worked for five brands of these "
                  r"registries: [^\n]*?search marketing, 2024\)", _md())
    if not m:
        raise SystemExit("Cheil sentence not found in the paper's Declarations")
    s = m.group(0).replace("Cheil Worldwide, a Samsung affiliate, or its Iris unit",
                           "Cheil Worldwide, a marketing company of the employer's group, or its Iris unit") + "."
    if "Samsung" in s:
        raise SystemExit("Cheil sentence still names the employer")
    return s


def ai_use_statement():
    m = re.search(r"## Use of AI tools \{-\}\n\n(.+?)\n", _md())
    if not m:
        raise SystemExit("AI-use statement not found in the paper's Declarations")
    return m.group(1).strip()


def d_abs(x):
    return abs(float(x))


def load():
    V = json.loads(VERDICTS.read_text(encoding="utf-8"))
    if V.get("stage") != 1 or "v0.43-prereg-r1" not in V.get("prereg", "") or V["B_perm"] != 10000:
        raise SystemExit("v43_stage1_verdicts.json is not the v0.43 Stage 1 run")
    rules = scorer_rules()
    v = BriefValues({"verdicts": V})
    T = ["tests"]
    printed = {"P": ("RHO", "N", "LO", "HI", "P2"), "SA": ("RHO", "N", "HI"), "M": ("RHO", "P2"),
               "C": ("RHO", "N", "LO", "HI")}
    paths = {"RHO": (["rho"], m3), "N": (["n"], i0), "LO": (["ci90", 0], m3), "HI": (["ci90", 1], m3),
             "P2": (["p_two"], f4)}
    for key, h in zip(["P", "SA", "M", "C"], TESTS):
        for what in printed[key]:
            p, fmt = paths[what]
            v.put(f"{what}_{key}", "verdicts", T + [h] + p, fmt)
    v.derive("RHO_P_ABS", d_abs, [("verdicts", T + [TESTS[0], "rho"])], r3)  # big number: size; sign in label/text
    MC = ["manipulation_checks"]
    v.put("CONC", "verdicts", MC + ["MC_Concurrent", "rho"], r3)
    v.put("REL", "verdicts", MC + ["MC_PullReliability", "mean_pairwise_pooled_spearman"], r3)
    v.put("TOPIC", "verdicts", MC + ["MC_Terms", "share_topic"], pct0)
    v.derive("UNITS", VV.d_sum, [("verdicts", ["outcome_defined_per_substrate", s, "units"])
                                 for s in V["outcome_defined_per_substrate"]], i0)
    D = ["descriptives"]
    v.put("D_DEFUNCT", "verdicts", D + ["presence_without_defunct_automotive", "H_Pred_Presence", "rho"], m3)
    v.put("D_RECALL", "verdicts", D + ["recall_alone", "rho"], m3)
    v.put("D_LEAD", "verdicts", D + ["longer_lead_P_t1", "rho"], m3)
    v.put("D_TOPIC", "verdicts", D + ["topic_only_primary", "rho"], m3)
    for name in ("CONF", "ALPHA", "FALS", "CONC_LINE", "REL_LINE"):
        v.rule(name, rules, r2)
    v.rule("MIN_N", rules, i0)
    v.rule("MIN_N_C", rules, i0)
    if rules["REV_ALPHA"][0] != rules["ALPHA"][0]:
        raise SystemExit("the REVERSED label uses another alpha than the verdict rule; the text says one alpha")

    # -- the brief's words assume these verdicts (stop on any mismatch)
    want = {"H_Pred_Presence": ("FALSIFIED", []), "H_Pred_Presence_SA": ("FALSIFIED", []),
            "H_Pred_Presence_Momentum": ("FALSIFIED", ["REVERSED"]), "H_Pred_Consistency": ("UNDETERMINED", [])}
    got = {h: (V["tests"][h]["verdict"], V["tests"][h]["labels"]) for h in TESTS}
    if got != want:
        raise SystemExit(f"the brief's wording assumes other verdicts: {got}")
    if V["flags"] or any(V["tests"][h]["flags"] for h in TESTS):
        raise SystemExit("a verdict carries a flag; the text says none does")
    mc = V["manipulation_checks"]
    if not all(mc[k]["pass_"] for k in ("MC_Concurrent", "MC_PullReliability", "MC_Terms")) \
            or mc["MC_Weekly"]["missing"] != 0:
        raise SystemExit("a check failed; the text says all passed")
    if not all(V["tests"][h]["rho"] < 0 for h in TESTS[:3]) or not all(
            V["descriptives"][k]["rho"] < 0 for k in ("recall_alone", "longer_lead_P_t1", "topic_only_primary")) \
            or V["descriptives"]["presence_without_defunct_automotive"]["H_Pred_Presence"]["rho"] >= 0:
        raise SystemExit("the text says every Presence variant is negative")
    if any(V["tests"][h]["boot_valid"] != V["B_boot"] for h in TESTS):
        raise SystemExit("bootstrap resamples were dropped")
    v.word("CHEIL", cheil_sentence(), "papers/v0_43/v0_43_paper_draft.md Declarations, Cheil sentence, employer's "
           "name replaced by 'a marketing company of the employer's group'")
    v.word("AI_USE", ai_use_statement(), "papers/v0_43/v0_43_paper_draft.md Declarations, Use of AI tools, verbatim")
    return v, {"verdicts": V}


def chart_data(src):
    """Per test: rho and its 90% and 95% bootstrap intervals (verdict file tests.<H>)."""
    V = src["verdicts"]
    return [{"test": h, "rho": V["tests"][h]["rho"], "ci90": V["tests"][h]["ci90"], "ci95": V["tests"][h]["ci95"],
             "n": V["tests"][h]["n"], "verdict": V["tests"][h]["verdict"], "labels": V["tests"][h]["labels"]}
            for h in TESTS]


def _sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def write_provenance(v, extra=None):
    PROV_OUT.parent.mkdir(parents=True, exist_ok=True)
    out = {"_note": "Every number printed in TS-BR-v0.43-r1 and its chart: name -> source file, JSON path (or the "
                    "locked scorer's source line), raw value, format. Source: osf/v43/v43_stage1_verdicts.json; "
                    "decision lines: osf/v43/scripts/score_v0_43.py; disclosure wording: "
                    "papers/v0_43/v0_43_paper_draft.md. Files checked out unchanged from " + SOURCE_COMMIT + ".",
           "sources_sha256": {str(p.relative_to(ROOT)): _sha(p) for p in (VERDICTS, SCORER, PAPER_MD)},
           "values": v.prov}
    if extra:
        out.update(extra)
    PROV_OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    return PROV_OUT


if __name__ == "__main__":
    v, src = load()
    for n, s in v.vals.items():
        print(f"{n:<10} {s if len(s) < 90 else s[:90] + '...'}")
