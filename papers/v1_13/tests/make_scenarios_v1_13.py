#!/usr/bin/env python3
"""
make_scenarios_v1_13.py -- SYNTHETIC scorer outputs for testing the v1.13 (Grounding Paper A) paper pipeline.
Never real data: no t4 S1 answer is read (osf/v42 is never opened), no website is fetched, no API is called.

Every scenario is produced by the LOCKED scorers' own functions, imported read-only from
osf/methodology/v1_13/scripts/ (score_v1_13.py, audit_v1_13.py) and fed with the synthetic inputs of their own unit
tests (tests/test_score_v1_13.synthetic_t4: 5 substrates x 8 invented units under the reserved .test domain;
tests/test_clarification_v1_13.write_stage1 / write_v112: v1.14- and v1.12-shaped comparator files):

  Stage C1   score_v1_13.stage_c1() with H4 and H6 active and their scores absent (PENDING), H5 inactive, as the
             anchor recorded them at the Part I lock.
  C1 edits   (derived scenarios only) a gate leg's statistics are set to other values; every verdict word is then
             recomputed by the scorer's sep_verdict / reliability_verdict and the gate by its gate().
  Stage C2   exactly the sequence of score_v1_13.main --stage C2: stage_c2() (H7 on an SDRI table written by
             audit_v1_13.sdri_rows/write_csv from synthetic audit records), stage_c2_ranking() (H4 on a synthetic
             v1.14 Stage 1 file read with allow_dry=True) and stage_c2_coverage() (H6 on a synthetic v1.12 unit
             table read with a synthetic scorer hash), each with the scorer's own re-issue of the gate.

Scenarios (gate after Stage C2; see PIPELINE.md for the full matrix):
  scored          C1 as the scorer wrote it; H4 gating, H6 and H7 computed                    Part II collected
  pass_reported   H4 FALSIFIED but reported, not gating (v1.14 Stage 1 FAIL): PASS stands     Part II collected
  downgraded      H4 gating and FALSIFIED at C2: PASS re-issued as MARGINAL                   Part II collected
  fail            Presence tracks G* (synthetic_t4(p_tracks_g=True)): H1 FALSIFIED, FAIL;
                  H4 and H6 unavailable by C2 (dependency unavailable)                         Part II held
  marginal        H2's S0 leg set to 0.412: MARGINAL; H6 unavailable                           Part II locked, not run
  h3_undetermined one qualifying run pair: H3 UNDETERMINED, gate MARGINAL; H7 below its floor Part II collected
  dropped         Gemini dropped by MQ4, MQ2/MQ3/MQ6 flagged, H3 FALSIFIED: FAIL; S10/S11 changes
                                                                                               Part II collected
  mq5             MQ5 failed: H1, H2 UNDETERMINED, gate UNDETERMINED                           Part II held
  floor           H1's S1 leg below the 30-unit floor: gate UNDETERMINED                       Part II collected
  interim         Stage C1 only (no Stage C2 yet): H4, H6 PENDING, H7 not yet tested          Part II locked, not run

Writes SYNTHETIC_<scenario>_v1_13_verdicts.json (+ SYNTHETIC_<scenario>_v1_13_sdri.csv when Part II was collected);
each verdict file carries "synthetic_fixture" at the top level. Refuses any output directory under osf/.

Usage: python3 papers/v1_13/tests/make_scenarios_v1_13.py OUTDIR [--perm N] [--boot N] [scenario ...]
"""
import argparse
import copy
import json
import random
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = ROOT / "osf/methodology/v1_13/scripts"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(SCRIPTS / "tests"))
import score_v1_13 as S  # noqa: E402
import audit_v1_13 as A  # noqa: E402
from test_score_v1_13 import synthetic_t4  # noqa: E402
from test_clarification_v1_13 import write_stage1, write_v112, FAKE_V112_SCORER_SHA  # noqa: E402

SCENARIOS = ["scored", "pass_reported", "downgraded", "downgraded_h6", "c1_h4", "fail", "marginal",
             "h3_undetermined", "dropped", "mq5", "floor", "interim"]
ACTIVE = {"H4_Sep_Ranking": True, "H5_Sep_Sentiment": False, "H6_Sep_Coverage": True}   # as the anchor recorded them
PART2 = {"scored": "collected", "pass_reported": "collected", "downgraded": "collected", "fail": "held",
         "downgraded_h6": "collected", "c1_h4": "collected",
         "marginal": "not_run", "h3_undetermined": "collected", "dropped": "collected", "mq5": "held",
         "floor": "collected", "interim": "not_run"}


# --------------------------------------------------------------------------- Stage C1 (the scorer, unedited)
def c1(p_tracks_g, h4_at_c1, n_perm, n_boot):
    """h4_at_c1: v1.14's Stage 1 output already exists at Stage C1 (SEPARABLE, R*_S1 = G*: H4 FALSIFIED, gating)."""
    inp = synthetic_t4(seed=7, p_tracks_g=p_tracks_g)
    inp["active"] = dict(ACTIVE)
    with tempfile.TemporaryDirectory() as tmp:
        if h4_at_c1:
            gs = S.gstar_map(S.brand_stats(answers_of(inp, {"panel_models": list(S.PANELS["N3"])}), inp["units"]))
            p, _ = write_stage1(Path(tmp) / "v114", inp["units"], r1_from=gs, verdict="SEPARABLE (Stage 2 pending)")
            inp["ranking_source"] = S.load_ranking_source(p, "S1", allow_dry=True)
        doc = S.stage_c1(inp, n_perm=n_perm, n_boot=n_boot)
    return inp, json.loads(json.dumps(doc, default=str))          # the file as main() writes it


def comparator_values(units, how, seed):
    """{unit: value} for a synthetic comparator: 'noise' unrelated to G*, None for write_stage1's own sparse values."""
    if how != "noise":
        return None
    rng = random.Random(seed)
    return {k: rng.uniform(1.0, 99.0) for k in sorted(units)}


def answers_of(inp, doc):
    recs = S.dedupe_calls(inp["records"])
    return S.build_answers(S.select_calls(recs, doc["panel_models"], "S1", "B"),
                           S.named_index(inp["coded_b"], inp["units"]), inp["units"], inp["classes"])


# --------------------------------------------------------------------------- C1 edits, verdicts recomputed by the scorer
def set_leg(leg, rho=None, p=None, n=None, below=None):
    old = leg.get("rho_w")
    if rho is not None:
        leg["rho_w"] = rho
        ci = leg.get("ci90")
        if ci and old is not None and ci.get("lo") is not None:
            ci["lo"] = max(-1.0, min(1.0, ci["lo"] + rho - old))
            ci["hi"] = max(-1.0, min(1.0, ci["hi"] + rho - old))
    if p is not None:
        leg["p"] = p
    if n is not None:
        leg["n"] = n
        leg["below_n_floor"] = n < S.FLOOR_UNITS
    if below is not None:
        leg["below_n_floor"] = below
    return leg


def recompute_c1(doc):
    """Verdict words and the gate from the scorer's own functions (N8, N9, section 3 gate rule)."""
    mq5 = bool(doc["MQ"]["MQ5"]["failed"])
    v = doc["verdicts"]
    v["H1_Sep_Presence"] = S.sep_verdict(doc["legs"]["H1_Sep_Presence"], mq5)
    v["H2_Sep_Consistency"] = S.sep_verdict(doc["legs"]["H2_Sep_Consistency"], mq5)
    v["H3_Run_Reliability"] = S.reliability_verdict(doc["H3"])
    gating = {"H4_Sep_Ranking": bool((doc.get("H4_ranking_source") or {}).get("h4_gates"))}
    doc["gate"] = json.loads(json.dumps(S.gate(v, doc["gate"]["active"], gating), default=str))
    sens = doc.get("sensitivities") or {}
    doc["verdict_changes"] = json.loads(json.dumps(                       # = stage_c1's expression, on the new words
        {nm: {h: (sv["verdicts"][h], v[h]) for h in sv.get("verdicts", {}) if sv["verdicts"][h] != v[h]}
         for nm, sv in sens.items() if "verdicts" in sv}))


# --------------------------------------------------------------------------- Part II: synthetic audit -> SDRI (audit's own code)
def synthetic_sdri(inp, doc, out_csv, mode, seed=11):
    """Synthetic audit records shaped as audit_v1_13.audit_unit writes them; SDRI by audit_v1_13.sdri_rows.
    mode 'tracks': indicator count follows G* (H7 high); 'random': unrelated; 'sparse': as 'tracks' with half the
    home pages blocked (SDRI not rated), so H7 falls below its 30-unit floor."""
    rng = random.Random(seed)
    units, gs = inp["units"], {}
    for k, u in doc["units"].items():
        sub, bid = k.split("|", 1)
        gs[(sub, bid)] = u["G_star"] if u["rated"] else None
    recs = []
    for i, (k, u) in enumerate(sorted(units.items())):
        dom = sorted(u["domains"])[0]
        g = gs.get(k)
        if mode in ("tracks", "sparse") and g is not None:
            score = min(8, max(0, int(round(g / 100 * 8 + rng.uniform(-1.2, 1.2)))))
        else:
            score = rng.randint(0, 8)
        bits = [1] * score + [0] * (8 - score)
        rng.shuffle(bits)
        p1_ok = (i % 13) != 5 and not (mode == "sparse" and i % 2 == 0)   # P1 fetches that fail (blocked)
        rec = {"substrate": k[0], "brand_id": k[1], "brand": u["brand"], "phantom": False, "domain": dom,
               "pages": {"P1": {"outcome": "ok" if p1_ok else "blocked"}}, "site": None,
               "kg": {"status": "chosen", "qid": f"Q9{i:04d}", "p856": [f"https://www.{dom}/"] if bits[6] else
                      ["https://elsewhere.test/"], "sitelinks": ["enwiki"] if bits[7] else []}}
        if not bits[5]:
            rec["kg"] = {"status": "none", "qid": None}
        if p1_ok:
            rec["site"] = {f"i{j + 1}": bits[j] for j in range(5)}
            rec["verified_alias"] = dom
        recs.append(rec)
    classes = S.load_classes()
    rows = A.sdri_rows(recs, {}, classes["multi_suffix"], lambda r: units[(r["substrate"], r["brand_id"])]["domains"])
    A.write_csv(out_csv, rows, A.SDRI_FIELDS)
    return S.read_sdri(out_csv, units)


# --------------------------------------------------------------------------- Stage C2 (main --stage C2's sequence)
def c2(inp, doc, tmp, sdri_csv=None, sdri_mode="tracks", h4=None, h6=None, n_perm=10_000, n_boot=2_000):
    """h4: None (unavailable) or (stage1_verdict, 'random'|'gstar'); h6: None or 'random'|'gstar'."""
    units = inp["units"]
    answers = answers_of(inp, doc)
    p_s0 = S.p_t4(inp["brand_table"], inp["coded_a"], units, "S0", S.PANELS["N3"], S.t4_excluded(inp["records"]))
    collected = sdri_csv is not None
    sdri = synthetic_sdri(inp, doc, sdri_csv, sdri_mode) if collected else {}
    out = S.stage_c2(doc, answers, units, p_s0, sdri, collected, n_perm, n_boot)
    gs = S.gstar_map(S.brand_stats(answers, units))
    src4 = None
    if h4 is not None:
        verdict, how, sd = h4
        vals = gs if how == "gstar" else comparator_values(units, how, sd)
        p, _ = write_stage1(Path(tmp) / "v114", units, r1_from=vals, verdict=verdict)
        src4 = S.load_ranking_source(p, "S1", allow_dry=True)        # synthetic file (dry_run): allowed here only
    out["ranking"] = S.stage_c2_ranking(doc, answers, units, src4, n_perm, n_boot,
                                        unavailable=None if h4 else "SYNTHETIC: v1.14 Stage 1 halted; its output "
                                                                    "does not exist (dependency unavailable)")
    src6 = None
    if h6 is not None:
        how, sd = h6
        vals = gs if how == "gstar" else comparator_values(units, how, sd)
        p6 = write_v112(Path(tmp) / "v112", units, values=vals, seed=sd)
        src6 = S.read_v112_cov(p6, FAKE_V112_SCORER_SHA, "SYNTHETIC")
    out["coverage"] = S.stage_c2_coverage(doc, answers, units, src6,
                                          before=(out["ranking"].get("gate_reissued") or {}).get("after"),
                                          n_perm=n_perm, n_boot=n_boot,
                                          unavailable=None if h6 else "SYNTHETIC: v1.12's Cov* output did not "
                                                                      "exist by Stage C2 (dependency unavailable)")
    out["appended_utc"] = datetime.now(timezone.utc).isoformat()
    doc["stage_C2"] = json.loads(json.dumps(out, default=str))
    return doc


def base_key(name):
    """(Presence tracks G*, H4's score exists at Stage C1)."""
    return name == "fail", name == "c1_h4"


def edit_h7(doc, rho=None, n=None, p=None):
    leg = doc["stage_C2"]["leg"]
    set_leg(leg, rho, p, n)
    doc["stage_C2"]["H7_Struct_Gap"] = S.struct_gap_verdict(leg, True)


SEP = "SEPARABLE (Stage 2 pending)"
# Stage C2 inputs per scenario: (SDRI mode, or None = Part II not collected; H4 (Stage 1 verdict, values, seed), or None =
# unavailable; H6 (values, seed), or None = unavailable). Values: noise (unrelated to G*), gstar (= G*: FALSIFIED),
# sparse (the test helper's own sparse values: below the n floor).
C2_PLAN = {"scored": ("tracks", (SEP, "noise", 101), ("noise", 201)),
           "pass_reported": ("random", ("FAIL", "gstar", 0), ("noise", 201)),
           "downgraded": ("tracks", (SEP, "gstar", 0), ("noise", 201)),
           "downgraded_h6": ("tracks", (SEP, "noise", 101), ("gstar", 0)),
           "c1_h4": ("tracks", None, ("noise", 201)),
           "fail": (None, None, None),
           "marginal": (None, ("MARGINAL", "noise", 101), None),
           "h3_undetermined": ("sparse", (SEP, "sparse", 0), ("noise", 201)),
           "dropped": ("tracks", (SEP, "noise", 101), ("gstar", 0)),
           "mq5": (None, None, None),
           "floor": ("random", (SEP, "noise", 101), ("noise", 201))}


def build(name, out, n_perm, n_boot, bases):
    inp, base = bases[base_key(name)]
    doc = copy.deepcopy(base)
    sdri_csv = out / f"SYNTHETIC_{name}_v1_13_sdri.csv" if PART2[name] == "collected" else None
    with tempfile.TemporaryDirectory() as tmp:
        if name == "marginal":
            set_leg(doc["legs"]["H2_Sep_Consistency"][1], rho=0.412, p=0.0004)
            recompute_c1(doc)
        elif name == "h3_undetermined":
            h3 = doc["H3"]
            for pr in h3["pairs"][1:]:
                pr["n"], pr["qualifies"] = 27, False
            h3["n_qualifying_pairs"] = 1
            h3["rel1"] = h3["pairs"][0]["rho_w"]
            h3["rel3"] = S.spearman_brown_3(h3["rel1"])
            h3["p"] = None
            recompute_c1(doc)
        elif name == "dropped":
            doc["dropped_models"] = [S.GEM4]
            doc["panel_models"] = [m for m in doc["panel_models"] if m != S.GEM4]
            doc["MQ"]["MQ4"].update(unresolved_share=0.274, drop_gemini=True)
            g = doc["MQ"]["MQ2"][S.GPT6]
            g.update(with_source=round(0.21 * g["answers"]), share=round(0.21 * g["answers"]) / g["answers"],
                     flag_search_rarely_used=True)
            doc["MQ"]["MQ3"].update(share=0.63, flag=True, low_coverage=True)
            doc["MQ"]["MQ6"].update(rho_gstar_g=0.534, flag=True)
            sens = doc["sensitivities"]
            sens["S5_gemini_kept"] = sens.pop("S5_gemini_dropped")
            h3 = doc["H3"]
            for pr in h3["pairs"]:
                pr["rho_w"] = 0.081 + 0.01 * pr["pair"][1]
            h3["rel1"] = sum(pr["rho_w"] for pr in h3["pairs"] if pr["qualifies"]) / h3["n_qualifying_pairs"]
            h3["rel3"], h3["p"] = S.spearman_brown_3(h3["rel1"]), 0.0612
            recompute_c1(doc)
            sens["S11_without_Denon"]["verdicts"]["H3_Run_Reliability"] = "MARGINAL"
            sens["S10_uncentred"]["verdicts"]["H1_Sep_Presence"] = "MARGINAL"
            doc["verdict_changes"] = {nm: {h: (v["verdicts"][h], doc["verdicts"][h]) for h in v.get("verdicts", {})
                                           if v["verdicts"][h] != doc["verdicts"][h]}
                                      for nm, v in sens.items() if "verdicts" in v}       # = stage_c1's expression
            doc = json.loads(json.dumps(doc, default=str))
        elif name == "mq5":
            doc["MQ"]["MQ5"].update(failed=True, zero_share=0.85)
            recompute_c1(doc)
        elif name == "floor":
            set_leg(doc["legs"]["H1_Sep_Presence"][0], n=26)
            recompute_c1(doc)
        if name != "interim":                                            # interim: Stage C1 only
            mode, h4, h6 = C2_PLAN[name]
            c2(inp, doc, tmp, sdri_csv if mode else None, mode, h4, h6, n_perm, n_boot)
        if name == "downgraded":
            edit_h7(doc, rho=0.214)
    doc["synthetic_fixture"] = {"scenario": name, "part2": PART2[name],
                                "note": "SYNTHETIC: the locked scorer's functions on synthetic inputs; see "
                                        "make_scenarios_v1_13.py"}
    p = out / f"SYNTHETIC_{name}_v1_13_verdicts.json"
    p.write_text(json.dumps(doc, indent=2, default=str), encoding="utf-8")
    c2d = doc.get("stage_C2") or {}
    final = ((c2d.get("coverage") or {}).get("gate_reissued") or {}).get("after") or \
        ((c2d.get("ranking") or {}).get("gate_reissued") or {}).get("after") or doc["gate"]["verdict"]
    print(f"{name}: C1 gate {doc['gate']['verdict']}, final {final} | " +
          ", ".join(f"{h.split('_')[0]} {v}" for h, v in doc["verdicts"].items()) +
          (f" | C2: H7 {c2d.get('H7_Struct_Gap')}, H4 {c2d['ranking'].get('H4_Sep_Ranking')}, "
           f"H6 {c2d['coverage'].get('H6_Sep_Coverage')}" if c2d else " | C1 only"), flush=True)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("out", type=Path)
    ap.add_argument("scenarios", nargs="*", default=SCENARIOS)
    ap.add_argument("--perm", type=int, default=10_000)
    ap.add_argument("--boot", type=int, default=2_000)
    a = ap.parse_args(argv)
    out = a.out.resolve()
    if str(out).startswith(str((ROOT / "osf").resolve())):
        raise SystemExit(f"REFUSED: {out} is under osf/ (the scorer's real output location)")
    out.mkdir(parents=True, exist_ok=True)
    bases = {}
    for key in sorted({base_key(n) for n in a.scenarios}):
        bases[key] = c1(key[0], key[1], a.perm, a.boot)
    for name in a.scenarios:
        build(name, out, a.perm, a.boot, bases)
    return 0


if __name__ == "__main__":
    sys.exit(main())
