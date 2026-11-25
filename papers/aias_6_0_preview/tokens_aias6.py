#!/usr/bin/env python3
"""
tokens_aias6.py -- the one map from placeholder tokens to the locked scorer's outputs, for the AIAS 6.0 Preview
report (reports/aias6_preview_report_content.py) and the website study page (site/aias-6-0-preview.json).

The paper keeps its own engine (fill_paper_aias6.py: {{NAME}} placeholders, {% switch %} / {% if %} blocks,
values recorded with provenance by aias6_values.Values). The report and the site page use {{v:KEY}} tokens; every
KEY must be in TOKEN_MAP below, which names the output file and the JSON path (or the paper value) it comes from
and the format it is printed in. Nothing here types a number: a key resolves from

  results  osf/aias_6_0_preview/outputs/results_aias_6_0_preview.json   (score_aias_6_0_preview.py --run)
  gates    osf/aias_6_0_preview/outputs/gates_aias_6_0_preview.json
  inputs   osf/aias_6_0_preview/outputs/inputs_read_aias_6_0_preview.json
  paper    a value the paper fill computed from those files (same wording in both registers: the section 6.6
           headline, the W1 sentence, the gate-reading words)
  scorer   a constant of the locked scorer (bands and limits of the pre-registration, read from its module)

A key with "when" exists only in some outcomes (a paper flag, e.g. STRUCT: a structure test was run). Any content
item that uses such a key must declare the same flag in its "requires" list; the item is dropped when the flag is
false. tests/test_tokens_aias6.py fails on an unmapped token, a key that does not resolve on a synthetic
scenario where its flag holds, and a conditional key used without its flag.

  python3 papers/aias_6_0_preview/tokens_aias6.py --outputs DIR [--synthetic]   # prints every key and its value
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import aias6_values as VV  # noqa: E402
import fill_paper_aias6 as FP  # noqa: E402

TOKEN = re.compile(r"\{\{v:([^}]+)\}\}")
BUILD_TOKEN = re.compile(r"\{\{build:([^}]+)\}\}")
NUMWORD = VV.NUMWORD


def _word(x):
    if not isinstance(x, str):
        raise VV.Missing(f"not a word: {x!r}")
    return x


def _state(x):
    return VV.STATE_WORD[x]


def _num(x):
    n = int(x)
    return NUMWORD.get(n, f"{n:,}")


def _passes(x):
    return "passes" if bool(x) else "does not pass"


def _list_names(x):
    return ", ".join(VV.NAME[p] for p in x) if x else "none"


NO_LABEL = "not shown; negative result"      # pre-registration section 4.2, FAIL row: "not shown", "none"

FMT = {**VV.FORMATS, "word": _word, "label": _word, "state": _state, "num": _num, "passes": _passes, "names": _list_names,
       "len": lambda x: f"{len(x):,}",
       "r2m": lambda x: VV.r2(x).replace("-", "−"), "r3m": lambda x: VV.r3(x).replace("-", "−")}

# key: (source, path, format[, when])   path: a JSON path list (results/gates/inputs), a paper value name, or a scorer
# constant name. Grouped by what the report and the page print.
TOKEN_MAP = {
    # design and lock (no outcome dependence)
    "pv.title": ("results", ["title"], "word"),
    "pv.prereg_tag": ("results", ["prereg_tag"], "word"),
    "pv.units": ("results", ["MQ_Join", "expected_units"], "i0"),
    "pv.validation_line": ("results", ["validation_status_line"], "word"),
    "pv.band.confirm": ("scorer", "SEP_CONF", "r2"),
    "pv.band.falsify": ("scorer", "SEP_FALS", "r2"),
    "pv.k2_max": ("scorer", "K2_MAX", "r2"),
    "pv.k3_points": ("scorer", "K3_POINTS", "i0"),
    "pv.n_perm": ("scorer", "N_PERM", "i0"),
    "pv.n_boot": ("scorer", "N_BOOT", "i0"),
    # gate states and labels (section 4.1-4.2); words exactly as the scorer writes them
    "pv.state.R": ("results", ["gate_states", "R"], "state"),
    "pv.state.S": ("results", ["gate_states", "S"], "state"),
    "pv.state.Cov": ("results", ["gate_states", "Cov"], "state"),
    "pv.state.G": ("results", ["gate_states", "G"], "state"),
    "pv.label.R": ("results", ["labels", "R", "label"], "label"),
    "pv.label.S": ("results", ["labels", "S", "label"], "label"),
    "pv.label.Cov": ("results", ["labels", "Cov", "label"], "label"),
    "pv.label.G": ("results", ["labels", "G", "label"], "label"),
    "pv.label.P": ("results", ["labels", "P", "label"], "word"),
    "pv.label.C": ("results", ["labels", "C", "label"], "word"),
    "pv.bridge.P": ("results", ["labels", "P", "bridge"], "word"),
    "pv.bridge.C": ("results", ["labels", "C", "bridge"], "word"),
    "pv.K.names": ("results", ["K"], "names"),
    "pv.K.n": ("results", ["K"], "len"),
    # the headline and the wording rules, as the paper fill computed them (section 6.6, W1-W3)
    "pv.class": ("results", ["structure", "wording_class"], "word"),
    "pv.headline": ("paper", "HEADLINE", "word"),
    "pv.w1": ("paper", "W1_SENTENCE", "word", "STRUCT"),
    "pv.k_sentence": ("paper", "K_SENTENCE", "word"),
    "pv.structure.verdict": ("results", ["structure", "H_Structure", "verdict"], "word"),
    "pv.structure.k": ("results", ["structure", "H_Structure", "k"], "num"),
    "pv.structure.d": ("results", ["structure", "H_Structure", "d"], "num", "STRUCT"),
    "pv.structure.u": ("results", ["structure", "H_Structure", "u"], "num", "STRUCT"),
    "pv.structure.distinct": ("results", ["structure", "H_Structure", "by_status", "DISTINCT"], "names", "STRUCT"),
    "pv.structure.partly": ("results", ["structure", "H_Structure", "by_status", "PARTLY DISTINCT"], "names",
                            "STRUCT"),
    "pv.structure.not_distinct": ("results", ["structure", "H_Structure", "by_status", "NOT DISTINCT"], "names",
                                  "STRUCT"),
    # Presence and Consistency on the newest models (H_PC_N3; S-test seed 600001)
    "pv.pc.verdict": ("results", ["structure", "H_PC_N3"], "word", "STRUCT"),
    "pv.pc.rho": ("results", ["structure", "S_tests", "PxC", "rho"], "r3m", "STRUCT"),
    "pv.pc.n": ("results", ["structure", "S_tests", "PxC", "n"], "i0", "STRUCT"),
    "pv.pc.lo": ("results", ["structure", "S_tests", "PxC", "ci90", 0], "r2m", "STRUCT"),
    "pv.pc.hi": ("results", ["structure", "S_tests", "PxC", "ci90", 1], "r2m", "STRUCT"),
    "pv.pc.rho_2dp": ("results", ["structure", "S_tests", "PxC", "rho"], "r2m", "STRUCT"),   # report big number
    # complete-profile set and coverage (D9, section 8)
    "pv.uk.n": ("results", ["structure", "U_K", "n"], "i0", "STRUCT"),
    # dimensions (D3) and bridge to AIAS 2.0 (D5); descriptive
    "pv.d3.pr": ("results", ["descriptives", "D3_dimensions", "participation_ratio"], "f1", "STRUCT"),
    "pv.d3.members": ("results", ["descriptives", "D3_dimensions", "members"], "len", "STRUCT"),
    "pv.bridge.rho_P": ("results", ["descriptives", "D5_bridge", "rho_P", "rho"], "r3m"),
    "pv.bridge.n_P": ("results", ["descriptives", "D5_bridge", "rho_P", "n"], "i0"),
    "pv.bridge.rho_P_2dp": ("results", ["descriptives", "D5_bridge", "rho_P", "rho"], "r2m"),  # report big number
    # the composite check (section 7.2; descriptive, nothing adopted)
    "pv.comp.rho_AP": ("results", ["structure", "composite_check", "rho_A_P"], "r3", "STRUCT"),
    "pv.comp.k2": ("results", ["structure", "composite_check", "K2_passes"], "passes", "STRUCT"),
    "pv.comp.k3": ("results", ["structure", "composite_check", "K3_passes"], "passes", "STRUCT"),
    # component inputs as the scorer read them (section 11.2)
    "pv.in.v042_ref": ("results", ["refs", "v0.42", "ref"], "word"),
    "pv.in.hgen_presence": ("gates", ["H_Gen_Presence"], "word"),
    "pv.in.hgen_phi": ("gates", ["H_Gen_Phi"], "word"),
}

# flags under which a "when" key exists; they are the paper fill's own flags, so both registers select one outcome
FLAGS = ("STRUCT", "RANK_SHOWN", "ANY_MARGINAL_PART", "W2")


class TokenError(KeyError):
    pass


def context(outputs, synthetic=False):
    """Load the scorer's outputs and run the paper fill once (in memory), so that the report and the page read the
    paper's own flags, cases and wording. Refusals are the paper fill's (synthetic/real mode, class C, tampering)."""
    _, val, cases, flags = FP.fill(outputs, synthetic=synthetic, class_c_draft=True)
    return {"src": VV.load_sources(outputs), "paper": val.vals, "cases": cases, "flags": flags,
            "scorer": FP.scorer(), "class": None}


def resolve(key, ctx):
    if key not in TOKEN_MAP:
        raise TokenError(f"unmapped token {{{{v:{key}}}}}")
    src, path, fmt = TOKEN_MAP[key][:3]
    if src == "paper":
        raw = ctx["paper"][path] if path in ctx["paper"] else None
    elif src == "scorer":
        raw = getattr(ctx["scorer"], path)
    else:
        raw = VV.jget(ctx["src"][src], path)
    if raw is None and fmt == "label":
        raw = NO_LABEL                    # section 4.2: a FAIL part has no label; it is not shown
    if raw is None:
        raise VV.Missing(f"{key}: {src}:{path} is null")
    return FMT[fmt](raw)


def holds(req, ctx):
    """'STRUCT' / '!STRUCT' (a paper flag), 'CLASS=A_k' (the wording class), 'PC=CONFIRMED' (H_PC_N3),
    'CASE_R=MARGINAL|PASS_RETEST_PENDING' (a paper case; '|' separates alternatives)."""
    neg = req.startswith("!")
    r = req[1:] if neg else req
    if "=" in r:
        var, want = r.split("=", 1)
        if var == "CLASS":
            got = ctx["src"]["results"]["structure"]["wording_class"]
        elif var == "PC":
            got = ctx["src"]["results"]["structure"].get("H_PC_N3")
        else:
            got = ctx["cases"][var]
        ok = got in want.split("|")
    else:
        ok = bool(ctx["flags"][r])
    return ok != neg


def keys_in(obj):
    if isinstance(obj, str):
        return set(TOKEN.findall(obj))
    if isinstance(obj, dict):
        parts = [keys_in(v) for k, v in obj.items() if k != "requires" and not str(k).startswith("_")]
        return set().union(*parts) if parts else set()
    if isinstance(obj, (list, tuple)):
        return set().union(*(keys_in(v) for v in obj)) if obj else set()
    return set()


def fill_content(obj, ctx, used=None):
    """Fill {{v:KEY}} in a string, list or dict; a dict with "requires" is dropped (None) when a requirement fails."""
    used = set() if used is None else used
    if isinstance(obj, str):
        def rep(m):
            used.add(m.group(1))
            return resolve(m.group(1), ctx)
        out = TOKEN.sub(rep, obj)
        rest = BUILD_TOKEN.sub("", out)       # {{build:KEY}}: PDF facts, filled at the website hand-off
        if "{{" in rest or "{%" in rest:
            raise TokenError(f"unfilled template syntax: {out[:80]}")
        return out
    if isinstance(obj, dict):
        if not all(holds(r, ctx) for r in obj.get("requires", [])):
            return None
        # keys starting with "_" are notes for the builder or the hand-off, never printed or filled
        return {k: fill_content(v, ctx, used) for k, v in obj.items()
                if k != "requires" and not str(k).startswith("_")}
    if isinstance(obj, (list, tuple)):
        return [x for x in (fill_content(v, ctx, used) for v in obj) if x is not None]
    return obj


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--outputs", type=Path, default=VV.OUTDIR)
    ap.add_argument("--synthetic", action="store_true")
    a = ap.parse_args(argv)
    ctx = context(a.outputs, a.synthetic)
    for k in TOKEN_MAP:
        try:
            print(f"{k}\t{resolve(k, ctx)}")
        except VV.Missing as e:
            print(f"{k}\t-- ({e})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
