#!/usr/bin/env python3
"""
brief_v1_13_values.py -- every number printed in the Grounding Paper A brief (TS-BR-v1.13-r1) and its chart.

Numbers are read by code, never typed:
  * result values from the study's verdict file osf/methodology/v1_13/v1_13_verdicts.json (Stage C1, with Stage C2
    appended under "stage_C2") and from osf/methodology/v1_13/v1_13_c2_extras.json (S6, S7; continued deviations log
    Entries 5, 6, 17), through the Values class of papers/v1_12/v112_values.py (each printed value records source,
    JSON path, raw value and format);
  * decision lines (separability 0.30 / 0.50, the rating floor 6, the per-run floor 3, the 30-unit floor, the
    sensitivity floors 3 and 10) from the locked scorer's constants (osf/methodology/v1_13/scripts/score_v1_13.py,
    read with ast, not imported), kind "rule".

Source files are checked out unchanged from branch v1.13-paper (32b85a5). write_provenance() writes
reports/briefs/v1_13/brief_v1_13_provenance.json. ROOT is the worktree (AIAS_ROOT), never the main tree.
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
from brief_v1_12_values import scorer_constants as _consts  # noqa: E402  (ast reader with tuple assignments)

DESIGN = ROOT / "osf/methodology/v1_13"
VERDICTS = DESIGN / "v1_13_verdicts.json"
C2_EXTRAS = DESIGN / "v1_13_c2_extras.json"
SCORER = DESIGN / "scripts/score_v1_13.py"
PAPER_MD = ROOT / "papers/v1_13/v1_13_paper_draft.md"
PROV_OUT = ROOT / "reports/briefs/v1_13/brief_v1_13_provenance.json"
SOURCE_COMMIT = "32b85a5 (branch v1.13-paper; verdict file with Stage C2 appended 2026-11-22 18:09 UTC)"
SUBS = ("v19", "v20", "v21", "v22", "v23")
BARE_SUFFIX = re.compile(r"(co|com)\.[a-z]{2}")   # the paper's rule for a bare country suffix (fill_paper_v1_13.py)


def r3(x):
    return VV.r3(x)


def m3(x):
    """three decimals with a typographic minus"""
    return VV.r3(x).replace("-", "−")


def r2(x):
    return VV.r2(x)


def i0(x):
    return VV.i0(x)


def f1(x):
    s = f"{float(x):.1f}"
    return "0.0" if s == "-0.0" else s


def pct0(x):
    return f"{100 * float(x):.0f}%"


def pnum0(x):
    """a share as a whole percentage without the sign (big number; the % is drawn as its unit)"""
    return f"{100 * float(x):.0f}"


def d_median(*xs):
    v = sorted(float(x) for x in xs)
    n = len(v)
    return v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2


def d_count(*xs):
    return float(len(xs))


def d_bare_suffixes(*alias_lists):
    """number of distinct aliases that are a bare country suffix, over the S6 alias lists"""
    return float(len({d for al in alias_lists for d in al if BARE_SUFFIX.fullmatch(d)}))


def d_bare_units(*alias_lists):
    """number of units with at least one bare-country-suffix alias"""
    return float(sum(1 for al in alias_lists if any(BARE_SUFFIX.fullmatch(d) for d in al)))


def scorer_constants(path=SCORER):
    return _consts(path)


class BriefValues(VV.Values):
    def rule(self, name, const, fmt, consts, index=None):
        raw = consts[const] if index is None else consts[const][index]
        s = fmt(raw)
        self.vals[name] = s
        self.prov[name] = {"kind": "rule", "source": str(SCORER.relative_to(ROOT)), "constant": const,
                           "index": index, "raw": raw, "fmt": fmt.__name__, "formatted": s}
        return s

    def derive_named(self, name, fn, names, fmt):
        """a function of values already derived (by name); provenance lists them"""
        raws = [self.prov[n]["raw"] for n in names]
        raw = fn(*raws)
        s = fmt(raw)
        self.vals[name] = s
        self.prov[name] = {"kind": "derived_of_values", "fn": fn.__name__, "values": list(names), "raw": raw,
                           "fmt": fmt.__name__, "formatted": s}
        return s


def _md():
    return PAPER_MD.read_text(encoding="utf-8")


def ai_use_statement():
    m = re.search(r"## Use of AI tools \{-\}\n\n(.+?)\n", _md())
    if not m:
        raise SystemExit("AI-use statement not found in the paper's Declarations")
    return m.group(1).strip()


def _check_paper_coi():
    """The brief's COI wording follows the v1.13 paper's Declarations: Denon (Harman, Sep 23, 2025), the v0.22
    tier-2/3 supply relationships, S11 without Denon. The paper carries no Cheil Worldwide / Iris sentence (left out
    pending a decision, papers/v1_13/v113_values.py CHEIL_UNITS); the brief adds none."""
    md = _md()
    dec = md[md.index("# Declarations"):md.index("## Funding")]
    for need in ("Denon", "September 23, 2025", "Harman International", "tier-2/3", "S11"):
        if need not in dec:
            raise SystemExit(f"the paper's COI no longer says {need!r}; re-check the brief's Disclosures")
    if "Cheil" in dec:
        raise SystemExit("the paper's COI now names Cheil; the brief's Disclosures must carry its sentence")


def load():
    V = json.loads(VERDICTS.read_text(encoding="utf-8"))
    X = json.loads(C2_EXTRAS.read_text(encoding="utf-8"))
    if V.get("phase") != "v1.13" or V.get("stage") != "C1" or "stage_C2" not in V:
        raise SystemExit("v1_13_verdicts.json is not the v1.13 Stage C1 file with Stage C2 appended")
    src = {"verdicts": V, "c2": X}
    k = scorer_constants()
    v = BriefValues(src)
    units = V["units"]
    # -- the run
    v.derive("UNITS", d_count, [("verdicts", ["units", u, "m"]) for u in units], i0)
    v.put("N_RATED", "verdicts", ["MQ", "MQ5", "n_rated"], i0)
    v.put("ANSWERS", "verdicts", ["MQ", "MQ1_parsed_s1_records"], i0)
    v.put("ZERO_PCT", "verdicts", ["MQ", "MQ5", "zero_share"], pct0)
    v.put("ZERO_NUM", "verdicts", ["MQ", "MQ5", "zero_share"], pnum0)
    v.put("MQ3_PCT", "verdicts", ["MQ", "MQ3", "share"], pct0)
    v.put("GEM_PCT", "verdicts", ["MQ", "MQ2", "gemini-4-argon", "share"], pct0)
    meds = []
    for s in SUBS:
        refs = [("verdicts", ["units", u, "G_star"]) for u, x in units.items() if x["rated"] and u.startswith(s + "|")]
        v.derive(f"MED_{s}", d_median, refs, f1)
        meds.append(f"MED_{s}")
    v.derive_named("MED_MIN", VV.d_min, meds, f1)
    v.derive_named("MED_MAX", VV.d_max, meds, f1)
    # -- gate legs
    L = ["legs"]
    v.put("H1_S1", "verdicts", L + ["H1_Sep_Presence", 0, "rho_w"], r3)
    v.put("H1_S0", "verdicts", L + ["H1_Sep_Presence", 1, "rho_w"], r3)
    v.put("H1_N", "verdicts", L + ["H1_Sep_Presence", 0, "n"], i0)
    v.put("H1_N0", "verdicts", L + ["H1_Sep_Presence", 1, "n"], i0)
    v.put("H2_S1", "verdicts", L + ["H2_Sep_Consistency", 0, "rho_w"], m3)
    v.put("H2_S0", "verdicts", L + ["H2_Sep_Consistency", 1, "rho_w"], r3)
    v.put("H2_N1", "verdicts", L + ["H2_Sep_Consistency", 0, "n"], i0)
    v.put("H2_N0", "verdicts", L + ["H2_Sep_Consistency", 1, "n"], i0)
    pr = [("verdicts", ["H3", "pairs", i, "n"]) for i in range(len(V["H3"]["pairs"]))]
    v.derive("PAIR_MIN", VV.d_min, pr, i0)
    v.derive("PAIR_MAX", VV.d_max, pr, i0)
    v.put("H4", "verdicts", L + ["H4_Sep_Ranking", 0, "rho_w"], r3)
    v.put("H4_N", "verdicts", L + ["H4_Sep_Ranking", 0, "n"], i0)
    v.put("H6", "verdicts", ["stage_C2", "coverage", "leg", "rho_w"], m3)
    v.put("H6_N", "verdicts", ["stage_C2", "coverage", "leg", "n"], i0)
    v.put("H7_N", "verdicts", ["stage_C2", "leg", "n"], i0)
    # -- sensitivities
    v.put("S4_3_H1_S0", "verdicts", ["sensitivities", "S4_floor_3", "rho", "H1_Sep_Presence", 1], r3)
    al = [("c2", ["S6_verified_D_b", "aliases", u]) for u in X["S6_verified_D_b"]["aliases"]]
    v.derive("S6_N_BARE", d_bare_suffixes, al, i0)
    # -- decision lines of the locked scorer
    v.rule("SEP_LO", "SEP_CONFIRM", r2, k)
    v.rule("SEP_HI", "SEP_FALSIFY", r2, k)
    v.rule("FLOOR_G", "FLOOR_G", i0, k)
    v.rule("FLOOR_RUN", "FLOOR_G_RUN", i0, k)
    v.rule("FLOOR_UNITS", "FLOOR_UNITS", i0, k)
    v.rule("FLOOR_S3", "FLOOR_SENS", i0, k, 0)
    v.rule("FLOOR_S10", "FLOOR_SENS", i0, k, 1)

    # -- the brief's words assume these verdicts (stop on any mismatch)
    want = {"H1_Sep_Presence": "MARGINAL", "H2_Sep_Consistency": "CONFIRMED", "H3_Run_Reliability": "UNDETERMINED",
            "H4_Sep_Ranking": "CONFIRMED", "H5_Sep_Sentiment": "INACTIVE"}
    bad = {h: V["verdicts"].get(h) for h, w in want.items() if V["verdicts"].get(h) != w}
    C2 = V["stage_C2"]
    if bad or V["gate"]["verdict"] != "MARGINAL":
        raise SystemExit(f"the brief's wording assumes other verdicts: {bad}, gate {V['gate']['verdict']}")
    if C2["coverage"]["H6_Sep_Coverage"] != "MARGINAL" or C2["coverage"]["gate_reissued"] != \
            {"before": "MARGINAL", "after": "MARGINAL", "rule": "downgrade only (section 3)"}:
        raise SystemExit("Stage C2: H6 or the re-issued gate differs from the brief's text")
    if C2["H7_Struct_Gap"] != "UNDETERMINED" or not C2["leg"]["below_n_floor"]:
        raise SystemExit("H7 is not undetermined by the unit floor")
    if V["gate"]["gating"] != {"H4_Sep_Ranking": False, "H5_Sep_Sentiment": False, "H6_Sep_Coverage": True} \
            or V["H4_ranking_source"]["stage1_verdict"] != "MARGINAL":
        raise SystemExit("the gating of H4-H6 differs from the brief's text")
    if V["H3"]["n_qualifying_pairs"] != 0 or any(p["n"] >= k["FLOOR_UNITS"] for p in V["H3"]["pairs"]):
        raise SystemExit("a run pair qualifies; the 'no pair' sentence does not apply")
    vc = {s: {h: tuple(x) for h, x in c.items()} for s, c in V["verdict_changes"].items()}
    vc_want = {"S1_denominator_m": {"H4_Sep_Ranking": ("MARGINAL", "CONFIRMED")}, "S2_citations": {},
               "S4_floor_3": {"H1_Sep_Presence": ("FALSIFIED", "MARGINAL")},
               "S4_floor_10": {"H1_Sep_Presence": ("UNDETERMINED", "MARGINAL"),
                               "H2_Sep_Consistency": ("UNDETERMINED", "CONFIRMED"),
                               "H4_Sep_Ranking": ("UNDETERMINED", "CONFIRMED")},
               "S5_gemini_dropped": {}, "S9_text_urls": {}, "S10_uncentred": {"H4_Sep_Ranking": ("MARGINAL", "CONFIRMED")},
               "S11_without_Denon": {}}
    if vc != vc_want:
        raise SystemExit(f"sensitivity verdict changes differ from the brief's sentence: {vc}")
    sg = V["sensitivities"]
    if sg["S4_floor_3"]["gate"] != "FAIL" or sg["S4_floor_10"]["gate"] != "UNDETERMINED":
        raise SystemExit("the floor sensitivities' gate words differ from the brief's sentence")
    if X["S6_verified_D_b"]["verdict_changes"] or X["S7_legacy_t3"]["verdict_changes"]:
        raise SystemExit("S6 or S7 changes a verdict; the brief says neither does")
    g = V["MQ"]["MQ2"]["gemini-4-argon"]
    if not g["flag_search_rarely_used"] or g.get("dropped_from_primary") or V["dropped_models"]:
        raise SystemExit("Gemini's MQ2 flag or drop differs from the brief's text")
    if not V["MQ"]["MQ3"]["low_coverage"]:
        raise SystemExit("MQ3 is not labelled low coverage")
    if units["v19|Denon"]["rated"]:
        raise SystemExit("Denon is rated; the Disclosures say it was not scored")
    if float(V["legs"]["H1_Sep_Presence"][1]["rho_w"]) < float(V["legs"]["H1_Sep_Presence"][0]["rho_w"]):
        raise SystemExit("the big number assumes the search-off Presence leg is the larger")
    _check_paper_coi()
    v.word("AI_USE", ai_use_statement(), "papers/v1_13/v1_13_paper_draft.md Declarations, Use of AI tools, verbatim")
    return v, src


def chart_data(src):
    """Separability legs with their 90% intervals: H1 (S1, S0), H2 (S1, S0), H6 (Stage C2), H4 (reported only)."""
    V = src["verdicts"]
    spec = [("H1_S1", ["legs", "H1_Sep_Presence", 0], "Presence, search on", "presence"),
            ("H1_S0", ["legs", "H1_Sep_Presence", 1], "Presence, search off", "presence"),
            ("H2_S1", ["legs", "H2_Sep_Consistency", 0], "Consistency, search on", "other"),
            ("H2_S0", ["legs", "H2_Sep_Consistency", 1], "Consistency, search off", "other"),
            ("H6", ["stage_C2", "coverage", "leg"], "Coverage", "other"),
            ("H4", ["legs", "H4_Sep_Ranking", 0], "Ranking (reported only)", "reported")]
    rows = []
    for key, path, label, role in spec:
        leg = VV.jget(V, path)
        rows.append({"key": key, "label": label, "role": role, "rho": float(leg["rho_w"]), "n": leg["n"],
                     "ci90": [float(leg["ci90"]["lo"]), float(leg["ci90"]["hi"])], "path": ["verdicts"] + path})
    return rows


def _sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def write_provenance(v, extra=None):
    PROV_OUT.parent.mkdir(parents=True, exist_ok=True)
    out = {"_note": "Every number printed in TS-BR-v1.13-r1 and its chart: name -> source file, JSON path (or locked "
                    "scorer constant), raw value, format. Sources: osf/methodology/v1_13/v1_13_verdicts.json "
                    "(\"verdicts\") and osf/methodology/v1_13/v1_13_c2_extras.json (\"c2\"); decision lines: "
                    "osf/methodology/v1_13/scripts/score_v1_13.py; disclosure wording: "
                    "papers/v1_13/v1_13_paper_draft.md. Files checked out unchanged from " + SOURCE_COMMIT + ".",
           "sources_sha256": {str(p.relative_to(ROOT)): _sha(p) for p in (VERDICTS, C2_EXTRAS, SCORER, PAPER_MD)},
           "values": v.prov}
    if extra:
        out.update(extra)
    PROV_OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    return PROV_OUT


if __name__ == "__main__":
    v, src = load()
    for n, s in v.vals.items():
        print(f"{n:<16} {s if len(s) < 90 else s[:90] + '...'}")
    for r in chart_data(src):
        print(r["key"], round(r["rho"], 3), r["n"], [round(x, 3) for x in r["ci90"]])
