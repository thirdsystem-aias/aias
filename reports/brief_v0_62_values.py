#!/usr/bin/env python3
"""
brief_v0_62_values.py -- every number printed in the non-English wave brief (TS-BR-v0.62-r1) and its chart.

Numbers are read by code, never typed:
  * results from the study's locked verdict file osf/v62/v62_verdicts.json (the one scoring run, commit 262464d);
  * the post-scoring sensitivities of DEVIATIONS Entries 4-7: osf/v62/data/v62_sens_coi106_v0_62.json (Entry 4,
    S-COI on 106 units), v62_sens_ai_check_v0_62.json (Entry 5, S-Trans and S-AliasAI),
    v62_sens_en_corrected_v0_62.json (Entry 6, corrected English comparator), v62_planned_items_summary_v0_62.json
    (Entry 7: S-Language, S-Script, S-Alias, MC_Complete, MC_Budget, per-category values);
  * the strict section 6.5 charge of the one timed-out call (Entry 8) from the paper r2's value file
    papers/v0_62/v62_values.json (cost.worst_case, computed there with the locked budget_v0_62.worst_case()); the
    strict total is re-added here from the recorded spend and checked against the paper's figure;
  * decision lines (Presence 0.70 / 0.50, Consistency 0.50 / 0.30, alpha 0.05) from the locked scorer
    osf/v62/scripts/score_v0_62.py and the $100 cap from osf/v62/scripts/budget_v0_62.py, read with ast.

Every source file is unchanged from branch v0.62-paper (5749211; DEVIATIONS Entries 4-8 merged from v0.62-nohand
69e1aa9). write_provenance() writes reports/briefs/v0_62/brief_v0_62_provenance.json. ROOT is the worktree
(AIAS_ROOT), never the main tree.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import re
from pathlib import Path

ROOT = Path(os.environ.get("AIAS_ROOT") or Path(__file__).resolve().parents[1]).resolve()
OSF = ROOT / "osf/v62"
VERDICTS = OSF / "v62_verdicts.json"
COI106 = OSF / "data/v62_sens_coi106_v0_62.json"
AICHK = OSF / "data/v62_sens_ai_check_v0_62.json"
ENCORR = OSF / "data/v62_sens_en_corrected_v0_62.json"
PLANNED = OSF / "data/v62_planned_items_summary_v0_62.json"
PAPER_VALUES = ROOT / "papers/v0_62/v62_values.json"
SCORER = OSF / "scripts/score_v0_62.py"
BUDGET = OSF / "scripts/budget_v0_62.py"
PAPER_MD = ROOT / "papers/v0_62/v0_62_paper_draft.md"
PROV_OUT = ROOT / "reports/briefs/v0_62/brief_v0_62_provenance.json"
SOURCE_COMMIT = "5749211 (branch v0.62-paper; DEVIATIONS Entries 4-8 from v0.62-nohand 69e1aa9)"
LANGS = ("es", "ko", "zh")
CATS = ("v0.19", "v0.20", "v0.21", "v0.22", "v0.23")


def _num(x):
    from decimal import Decimal, ROUND_HALF_UP
    return Decimal(repr(float(x)))


def _round(x, nd):
    from decimal import Decimal, ROUND_HALF_UP
    q = Decimal(1).scaleb(-nd)
    return _num(x).quantize(q, rounding=ROUND_HALF_UP)


def r2(x):
    return str(_round(x, 2))


def r3(x):
    """three decimals, half up, typographic minus"""
    return str(_round(x, 3)).replace("-", "−")


def s3(x):
    """three decimals with a sign (+ or typographic minus)"""
    s = str(_round(x, 3))
    return s.replace("-", "−") if s.startswith("-") else "+" + s


def r4(x):
    return str(_round(x, 4))


def i0(x):
    return f"{int(round(float(x))):,}"


def usd0(x):
    return f"${float(x):,.0f}"


def usd2(x):
    return f"${_round(x, 2)}"


def d_min(*xs):
    return min(float(x) for x in xs)


def d_max(*xs):
    return max(float(x) for x in xs)


def d_sum(*xs):
    return sum(float(x) for x in xs)


def jget(obj, path):
    for p in path:
        obj = obj[p]
    return obj


def module_constants(path):
    """top-level NAME = literal (or tuple of literals) assignments of a locked module, read with ast"""
    out = {}
    for node in ast.parse(Path(path).read_text(encoding="utf-8")).body:
        if isinstance(node, ast.Assign):
            try:
                val = ast.literal_eval(node.value)
            except Exception:
                continue
            for t in node.targets:
                if isinstance(t, ast.Name):
                    out[t.id] = val
                elif isinstance(t, ast.Tuple) and isinstance(val, tuple) and len(val) == len(t.elts):
                    for e, x in zip(t.elts, val):
                        if isinstance(e, ast.Name):
                            out[e.id] = x
    return out


class Values:
    """name -> printed string (vals) and name -> provenance record (prov)."""

    def __init__(self, src):
        self.src = src
        self.vals, self.prov = {}, {}

    def _set(self, name, s, rec):
        if name in self.vals:
            raise KeyError(f"value {name} set twice")
        self.vals[name] = s
        self.prov[name] = dict(rec, formatted=s)
        return s

    def put(self, name, src, path, fmt):
        raw = jget(self.src[src], path)
        return self._set(name, fmt(raw), {"kind": "value", "source": src, "path": list(path), "raw": raw,
                                          "fmt": fmt.__name__})

    def derive(self, name, fn, refs, fmt):
        raws = [jget(self.src[s], p) for s, p in refs]
        raw = fn(*raws)
        return self._set(name, fmt(raw), {"kind": "derived", "fn": fn.__name__,
                                          "inputs": [[s, list(p)] for s, p in refs], "raw": raw,
                                          "fmt": fmt.__name__})

    def rule(self, name, module, const, fmt, consts, index=None):
        raw = consts[const] if index is None else consts[const][index]
        return self._set(name, fmt(raw), {"kind": "rule", "source": str(module.relative_to(ROOT)),
                                          "constant": const, "index": index, "raw": raw, "fmt": fmt.__name__})

    def word(self, name, text, source):
        return self._set(name, text, {"kind": "wording", "source": source, "raw": text, "fmt": "verbatim"})


def _md():
    return PAPER_MD.read_text(encoding="utf-8")


def ai_use_statement():
    m = re.search(r"## Use of AI tools \{-\}\n\n(.+?)\n", _md())
    if not m:
        raise SystemExit("AI-use statement not found in the paper's Declarations")
    return m.group(1).strip()


def _check_paper_coi():
    """The brief's COI wording follows the v0.62 paper's Declarations (line 318 at 5749211): Denon (Harman,
    September 23, 2025), the v0.22 tier-2/3 supply relationships, the Cheil Worldwide / Iris work for five registry
    brands, further supply contracts and duty-free retail, Korean as the home-market language, S-COI on 107 and 106."""
    md = _md()
    dec = md[md.index("# Declarations"):md.index("## Funding")]
    for need in ("Denon", "September 23, 2025", "Harman International", "tier-2/3", "Cheil Worldwide", "Iris",
                 "Chevrolet", "BMW", "Bentley", "Jack Daniel's", "Eucerin", "Tesla", "Hyundai", "duty-free",
                 "Korean", "S-COI", "107 units", "106-unit"):
        if need not in dec:
            raise SystemExit(f"the paper's COI no longer says {need!r}; re-check the brief's Disclosures")


def presence_lines(src):
    """every H_Lang_Presence sensitivity line (source, JSON path) with its verdict, from all five files"""
    out = []
    for k in src["verdicts"]["sensitivities"]:
        out.append(("verdicts", ["sensitivities", k]))
    for k in src["coi106"]["sensitivities"]:
        out.append(("coi106", ["sensitivities", k]))
    st = src["aichk"]["sensitivities_ai_check"]
    for line in ("flagged", "strictly_flagged"):
        for L in LANGS:
            out.append(("aichk", ["sensitivities_ai_check", "S-Trans", line, "tests", f"H_Lang_Presence_{L}"]))
    for k, x in st["S-AliasAI"].items():
        if isinstance(x, dict) and "rho_c" in x:
            out.append(("aichk", ["sensitivities_ai_check", "S-AliasAI", k]))
        elif isinstance(x, dict):
            for k2, y in x.items():
                if isinstance(y, dict) and "rho_c" in y and "Presence" in k2:
                    out.append(("aichk", ["sensitivities_ai_check", "S-AliasAI", k, k2]))
    for k in src["planned"]["sensitivities"]:
        out.append(("planned", ["sensitivities", k]))
    rc = src["encorr"]["result_corrected"]
    for L in LANGS:
        out.append(("encorr", ["result_corrected", "tests", f"H_Lang_Presence_{L}"]))
    for k in rc["sensitivities"]:
        out.append(("encorr", ["result_corrected", "sensitivities", k]))
    for k in src["encorr"]["s_coi_106_corrected"]:
        out.append(("encorr", ["s_coi_106_corrected", k]))
    return out


def load():
    S = {"verdicts": VERDICTS, "coi106": COI106, "aichk": AICHK, "encorr": ENCORR, "planned": PLANNED,
         "paper_values": PAPER_VALUES}
    src = {k: json.loads(p.read_text(encoding="utf-8")) for k, p in S.items()}
    V = src["verdicts"]
    if V.get("phase") != "v0.62" or V.get("joint_reading") != "Language-robust":
        raise SystemExit("v62_verdicts.json is not the locked v0.62 verdict file")
    for k in ("coi106", "encorr"):
        if src[k]["inputs_sha256"]["v62_verdicts.json"] != _sha(VERDICTS):
            raise SystemExit(f"{k} was computed against another verdict file")
    sc, bc = module_constants(SCORER), module_constants(BUDGET)
    v = Values(src)
    T = ["tests"]
    v.put("N_UNITS", "verdicts", ["n_units"], i0)
    for L in LANGS:
        u = L.upper()
        v.put(f"PRES_{u}", "verdicts", T + [f"H_Lang_Presence_{L}", "rho_c"], r3)
        v.put(f"PRES_{u}_LO", "verdicts", T + [f"H_Lang_Presence_{L}", "ci95_rho_c", 0], r3)
        v.put(f"PRES_{u}_HI", "verdicts", T + [f"H_Lang_Presence_{L}", "ci95_rho_c", 1], r3)
        v.put(f"PRES_{u}_N", "verdicts", T + [f"H_Lang_Presence_{L}", "n"], i0)
        v.put(f"P_{u}", "verdicts", T + [f"H_Lang_Presence_{L}", "p_perm"], r4)
        v.put(f"DL_{u}", "verdicts", T + [f"H_Lang_Presence_{L}", "delta_L"], s3)
        v.put(f"PHI_{u}", "verdicts", T + [f"H_Lang_Phi_{L}", "rho_c"], r3)
        v.put(f"PHI_{u}_N", "verdicts", T + [f"H_Lang_Phi_{L}", "n"], i0)
        v.put(f"COI_{u}", "verdicts", ["sensitivities", f"S-COI_{L}", "rho_c"], r3)
        v.put(f"COI106_{u}", "coi106", ["sensitivities", f"S-COI-106_{L}", "rho_c"], r3)
        v.put(f"CORR_{u}", "encorr", ["result_corrected", "tests", f"H_Lang_Presence_{L}", "rho_c"], r3)
    cats = [("verdicts", T + [f"H_Lang_Presence_{L}", "per_category_rho_c", c]) for L in LANGS for c in CATS]
    v.derive("CAT_MIN", d_min, cats, r3)
    v.derive("CAT_MAX", d_max, cats, r3)
    v.put("COI_N_RUN", "verdicts", ["sensitivities", "S-COI_es", "n"], i0)
    v.put("COI_N_106", "coi106", ["sensitivities", "S-COI-106_es", "n"], i0)
    v.put("DENON_N", "verdicts", ["sensitivities", "S-Denon_es", "n"], i0)
    v.put("HP_N", "verdicts", ["sensitivities", "S-Headphones_es", "n"], i0)
    v.put("SLANG_ZH", "planned", ["sensitivities", "S-Language_zh", "rho_c"], r3)
    v.put("SLANG_ZH_X", "planned", ["sensitivities", "S-Language_zh", "n_excluded_calls"], i0)
    v.put("SALIAS_KO", "planned", ["sensitivities", "S-Alias_ko", "rho_c"], r3)
    v.put("SALIAS_ZH", "planned", ["sensitivities", "S-Alias_zh", "rho_c"], r3)
    v.put("CORR_PHI_ZH", "encorr", ["result_corrected", "tests", "H_Lang_Phi_zh", "rho_c"], r4)
    lines = presence_lines(src)
    v.derive("SENS_MIN", d_min, [(s, p + ["rho_c"]) for s, p in lines], r3)
    v.put("CALLS", "planned", ["checks", "MC_Complete", "answered"], i0)
    v.put("CALLS_SENT", "planned", ["checks", "MC_Complete", "calls_sent"], i0)
    v.put("SPEND", "planned", ["checks", "MC_Budget", "spend_from_recorded_usage_usd"], usd2)
    v.derive("SPEND_STRICT", d_sum, [("planned", ["checks", "MC_Budget", "spend_from_recorded_usage_usd"]),
                                     ("paper_values", ["values", "cost.worst_case", "value"])], usd2)
    v.rule("CAP", BUDGET, "BUDGET_CAP_USD", usd0, bc)
    v.rule("PRES_CONF", SCORER, "PRES", r2, sc, 0)
    v.rule("PRES_FALS", SCORER, "PRES", r2, sc, 1)
    v.rule("PHI_CONF", SCORER, "PHI", r2, sc, 0)
    v.rule("PHI_FALS", SCORER, "PHI", r2, sc, 1)
    v.rule("ALPHA", SCORER, "ALPHA", r2, sc)
    _checks(v, src, lines, sc)
    _check_paper_coi()
    v.word("AI_USE", ai_use_statement(), "papers/v0_62/v0_62_paper_draft.md Declarations, Use of AI tools, verbatim")
    return v, src


def _checks(v, src, lines, sc):
    """the brief's words assume these verdicts and facts; stop on any mismatch"""
    V, P, E = src["verdicts"], src["planned"], src["encorr"]
    T = V["tests"]
    want = {"H_Lang_Presence_es": "CONFIRMED", "H_Lang_Presence_ko": "CONFIRMED", "H_Lang_Presence_zh": "CONFIRMED",
            "H_Lang_Phi_es": "CONFIRMED", "H_Lang_Phi_ko": "MARGINAL", "H_Lang_Phi_zh": "MARGINAL",
            "H_Lang_Rank_es": "NOT TESTED", "H_Lang_Rank_ko": "NOT TESTED", "H_Lang_Rank_zh": "NOT TESTED"}
    bad = {k: T[k]["verdict"] for k, w in want.items() if T[k]["verdict"] != w}
    if bad:
        raise SystemExit(f"the brief's wording assumes other verdicts: {bad}")
    if len({v.vals[f"P_{L.upper()}"] for L in LANGS}) != 1:
        raise SystemExit("the permutation p differs by language; the note prints one value")
    if any(T[f"H_Lang_Presence_{L}"]["n"] != V["n_units"] for L in LANGS):
        raise SystemExit("a Presence test is not on all units")
    for s, p in lines:
        x = jget(src[s], p)
        if x["verdict"] != "CONFIRMED":
            raise SystemExit(f"sensitivity {s}:{p} is {x['verdict']}; the brief says every check confirms")
    if len(lines) < 30:
        raise SystemExit(f"only {len(lines)} sensitivity lines found")
    sbs = E["verdicts_side_by_side"]
    if any(a["locked"] != a["corrected"] for L in LANGS for a in sbs[L].values()):
        raise SystemExit("a verdict differs under the corrected comparator")
    if E["result_corrected"]["tests"]["H_Lang_Phi_zh"]["verdict"] != "MARGINAL":
        raise SystemExit("corrected Chinese Consistency is not marginal")
    s = P["sensitivities"]
    if s["S-Language_es"]["n_excluded_calls"] or s["S-Language_ko"]["n_excluded_calls"] \
            or not s["S-Language_zh"]["n_excluded_calls"]:
        raise SystemExit("S-Language exclusions differ from the brief's sentence (Chinese only)")
    if v.vals["CALLS"] != v.vals["CALLS_SENT"]:
        raise SystemExit("not every call was answered")
    pv = src["paper_values"]["values"]
    if pv["cost.strict_total2"]["display"] != v.vals["SPEND_STRICT"] \
            or abs(pv["cost.strict_total"]["value"] - v.prov["SPEND_STRICT"]["raw"]) > 1e-9:
        raise SystemExit("the strict total differs from the paper's (Entry 8)")
    if abs(pv["raw.cost_sum"]["value"] - P["checks"]["MC_Budget"]["spend_from_recorded_usage_usd"]) > 1e-9:
        raise SystemExit("recorded spend differs between the raw file and Entry 7")
    if not P["checks"]["MC_Budget"]["pass"] or P["checks"]["MC_Budget"]["calls_not_sent"]:
        raise SystemExit("MC_Budget did not pass")
    for k in ("H_Lang_Presence", "H_Lang_Phi"):
        if P["verdicts_unchanged"][k] not in ("CONFIRMED ES, KO, ZH", "ES CONFIRMED, KO/ZH MARGINAL"):
            raise SystemExit("Entry 7 reports changed verdicts")


def chart_data(src):
    """Presence agreement with English per language, with the 95% bootstrap interval (primary test)."""
    V = src["verdicts"]
    names = {"es": "Spanish", "ko": "Korean", "zh": "Chinese"}
    rows = []
    for L in LANGS:
        t = V["tests"][f"H_Lang_Presence_{L}"]
        rows.append({"key": f"PRES_{L.upper()}", "label": names[L], "rho": float(t["rho_c"]), "n": t["n"],
                     "ci95": [float(t["ci95_rho_c"][0]), float(t["ci95_rho_c"][1])],
                     "path": ["verdicts", "tests", f"H_Lang_Presence_{L}"]})
    return rows


def _sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def write_provenance(v, extra=None):
    PROV_OUT.parent.mkdir(parents=True, exist_ok=True)
    files = (VERDICTS, COI106, AICHK, ENCORR, PLANNED, PAPER_VALUES, SCORER, BUDGET, PAPER_MD)
    out = {"_note": "Every number printed in TS-BR-v0.62-r1 and its chart: name -> source file, JSON path (or locked "
                    "constant), raw value, format. Sources: verdicts = osf/v62/v62_verdicts.json; coi106, aichk, "
                    "encorr, planned = osf/v62/data/v62_sens_coi106_v0_62.json, v62_sens_ai_check_v0_62.json, "
                    "v62_sens_en_corrected_v0_62.json, v62_planned_items_summary_v0_62.json (DEVIATIONS Entries "
                    "4-7); paper_values = papers/v0_62/v62_values.json (Entry 8 strict charge); decision lines: "
                    "osf/v62/scripts/score_v0_62.py, budget_v0_62.py. Files unchanged from " + SOURCE_COMMIT + ".",
           "sources_sha256": {str(p.relative_to(ROOT)): _sha(p) for p in files},
           "values": v.prov}
    if extra:
        out.update(extra)
    PROV_OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    return PROV_OUT


if __name__ == "__main__":
    v, src = load()
    for n, s in v.vals.items():
        print(f"{n:<14} {s if len(s) < 90 else s[:90] + '...'}")
    print(len(presence_lines(src)), "sensitivity lines")
