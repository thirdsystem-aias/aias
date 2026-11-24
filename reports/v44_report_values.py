#!/usr/bin/env python3
"""v0.44 report values: the few numbers the report (TS-FL-v0.44-r1) prints that papers/v0_44/v44_values.json
does not hold, computed by code from the study's scored or recorded files. Nothing is typed.

Reads (all on branch v0.44, unchanged):
  osf/v44/v44_verdicts.json     (score_v0_44.py --run, once; commit 306af42)
  osf/v44/v44_unit_table.csv    (same run)
  papers/v0_44/v44_values.json  (values_v0_44.py; the paper's values file)

Writes reports/v44_report_values.json: {"_meta": {...}, "values": {key: {"value", "display", "source"}}}.
Every key starts with "rv." so it can never collide with a paper key; build_report_v44_r1.py merges the two files
and refuses a duplicate. Run from the worktree root:  python3 reports/v44_report_values.py
"""
import ast
import csv
import hashlib
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = "reports/v44_report_values.json"
VF = "osf/v44/v44_verdicts.json"
UT = "osf/v44/v44_unit_table.csv"
PV = "papers/v0_44/v44_values.json"
SC = "osf/v44/scripts/score_v0_44.py"
VALS = {}
MODEL_NAMES = {"claude-fable-5-2": "Claude Fable 5.2", "gpt-6-astra": "GPT-6 Astra", "gemini-4-argon": "Gemini 4 Argon"}


def put(key, value, display, source):
    if not key.startswith("rv.") or key in VALS:
        raise KeyError(key)
    VALS[key] = {"value": value, "display": display, "source": source}


def f3(x):
    s = f"{x:.3f}"
    return s.replace("-", "−") if x < 0 else s


def pct(x):
    return f"{100 * x:.0f}%"


def sha(rel):
    return hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()


def main():
    d = json.loads((ROOT / VF).read_text(encoding="utf-8"))
    pv = json.loads((ROOT / PV).read_text(encoding="utf-8"))["values"]
    units = list(csv.DictReader((ROOT / UT).open(encoding="utf-8")))
    des = d["design"]

    # design counts (from the verdict file's design block)
    nm = len(des["models_used"])
    put("rv.models.n", nm, {3: "three"}.get(nm, str(nm)), f"{VF}:design.models_used (count)")
    put("rv.models.names", [MODEL_NAMES[m] for m in des["models_used"]],
        ", ".join(MODEL_NAMES[m] for m in des["models_used"][:-1]) + " and " + MODEL_NAMES[des["models_used"][-1]],
        f"{VF}:design.models_used (display names)")
    nr = len(des["runs_b"])
    put("rv.runs.n", nr, {3: "three"}.get(nr, str(nr)), f"{VF}:design.runs_b (count)")
    ni = len(des["industries"])
    put("rv.industries.n", ni, {8: "eight"}.get(ni, str(ni)), f"{VF}:design.industries (count)")
    q = des["expected"]["B"] // (ni * nr)
    assert q * ni * nr == des["expected"]["B"]
    put("rv.questions_per_industry", q, {6: "six"}.get(q, str(q)), f"{VF}:design.expected.B / (industries x runs_b)")

    nt = len(d["verdicts"])
    put("rv.tests.n", nt, {3: "three"}.get(nt, str(nt)), f"{VF}:verdicts (count of primary tests)")

    nB = des["expected"]["B"] * nm
    nA = des["expected"]["A"] * nm
    assert nA + nB == des["expected_total"]
    put("rv.calls.B", nB, f"{nB:,}", f"{VF}:design.expected.B x models")
    put("rv.calls.A", nA, f"{nA:,}", f"{VF}:design.expected.A x models")

    # collection date (first call, UTC date; US Central date checked equal)
    t0 = datetime.fromisoformat(d["manipulation_checks"]["MC_Window"]["first_call_utc"])
    put("rv.collection_date", t0.date().isoformat(), f"{t0.day} {t0.strftime('%B %Y')}",
        f"{VF}:manipulation_checks.MC_Window.first_call_utc (date)")
    put("rv.collection_month", t0.strftime("%Y-%m"), t0.strftime("%B %Y"),
        f"{VF}:manipulation_checks.MC_Window.first_call_utc (month)")

    # industries where smaller brands average above challengers (paper keys H_Tier.mean.<ind>.S / .C)
    labels = pv["reg.labels"]["value"]
    sgc = [i for i in des["industries"] if pv[f"H_Tier.mean.{i}.S"]["value"] > pv[f"H_Tier.mean.{i}.C"]["value"]]
    put("rv.tier.S_gt_C", sgc, " and ".join(labels[i].lower() for i in sgc),
        f"{PV}: industries with H_Tier.mean.<ind>.S > H_Tier.mean.<ind>.C")

    # tier sizes (non-ghost and ghost units) from the unit table
    tiers = Counter(u["tier"] for u in units)
    for t in ("L", "C", "S", "G"):
        put(f"rv.tier.n.{t}", tiers[t], str(tiers[t]), f"{UT}: rows with tier == {t}")

    # tier rule as applied: eligible-rank range of each tier (unit table)
    for t in ("L", "C"):
        rk = [int(u["eligible_rank"]) for u in units if u["tier"] == t]
        put(f"rv.rank.{t}.min", min(rk), str(min(rk)), f"{UT}: min eligible_rank of tier {t}")
        put(f"rv.rank.{t}.max", max(rk), str(max(rk)), f"{UT}: max eligible_rank of tier {t}")

    # recognised by all three models and never named, per tier, as a share of the tier
    gap = d["descriptives"]["2_recognition"]["recognised_by_all_three_with_pi_0_by_tier"]
    for t in ("L", "C", "S", "G"):
        put(f"rv.gap.share.{t}", gap[t] / tiers[t], pct(gap[t] / tiers[t]),
            f"{VF}:descriptives.2_recognition.recognised_by_all_three_with_pi_0_by_tier.{t} / {UT} tier count")
    # check the paper's display of the same counts
    for t in ("L", "C", "S", "G"):
        assert pv[f"D2.gap.{t}"]["value"] == gap[t]

    # never named at all (pi_hat == 0), all units, and recognised by all three among them
    zero = [u for u in units if float(u["pi_hat"]) == 0.0]
    put("rv.pi0.n", len(zero), str(len(zero)), f"{UT}: rows with pi_hat == 0")

    # model agreement and run-to-run reliability: ranges
    ag = [v["rho_pw"] for v in d["descriptives"]["5_model_agreement"].values()]
    put("rv.agree.min", min(ag), f3(min(ag)), f"{VF}:descriptives.5_model_agreement.*.rho_pw (min)")
    put("rv.agree.max", max(ag), f3(max(ag)), f"{VF}:descriptives.5_model_agreement.*.rho_pw (max)")
    pair = min(d["descriptives"]["5_model_agreement"].items(), key=lambda kv: kv[1]["rho_pw"])[0]
    a, b = pair.split("~")
    put("rv.agree.min_pair", pair, f"{MODEL_NAMES[a]} with {MODEL_NAMES[b]}",
        f"{VF}:descriptives.5_model_agreement (pair with the lowest rho_pw)")
    rel = d["descriptives"]["4_run_reliability"]
    r1 = [v["rel1"] for v in rel.values()]
    put("rv.rel1.min", min(r1), f3(min(r1)), f"{VF}:descriptives.4_run_reliability.*.rel1 (min)")
    put("rv.rel1.max", max(r1), f3(max(r1)), f"{VF}:descriptives.4_run_reliability.*.rel1 (max)")

    # names outside the registries: counts for names the paper's discussion cites
    d6 = d["descriptives"]["6_non_registry_names_in_phase_b"]
    for ind, name, key in (("GRO", "Trader Joe's", "TraderJoes"), ("GRO", "Costco", "Costco"),
                           ("CVF", "Buc-ee's", "Buceees"), ("QSR", "Raising Cane's", "RaisingCanes")):
        k = dict((n, c) for n, c in d6[ind]["top10"])[name]
        put(f"rv.d6.{ind}.{key}", k, str(k), f"{VF}:descriptives.6_non_registry_names_in_phase_b.{ind}.top10['{name}']")
    dist = [d6[i]["distinct"] for i in des["industries"]]
    put("rv.d6.distinct_min", min(dist), str(min(dist)), f"{VF}:descriptives.6_non_registry_names_in_phase_b.*.distinct (min)")
    put("rv.d6.distinct_max", max(dist), str(max(dist)), f"{VF}:descriptives.6_non_registry_names_in_phase_b.*.distinct (max)")

    # pre-set thresholds: the locked scorer's module constants, read by parsing its source (never imported or run)
    tree = ast.parse((ROOT / SC).read_text(encoding="utf-8"))
    const = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            names = [t.id for t in node.targets if isinstance(t, ast.Name)]
            tups = [t for t in node.targets if isinstance(t, ast.Tuple)]
            if names and isinstance(node.value, ast.Constant):
                const[names[0]] = node.value.value
            elif tups and isinstance(node.value, ast.Tuple):
                for t, val in zip(tups[0].elts, node.value.elts):
                    if isinstance(val, ast.Constant):
                        const[t.id] = val.value
    for key, name, fmt in (("spread_sd", "SPREAD_SD", "{:.2f}"), ("tier_conf", "TIER_CONF", "{:.2f}"),
                           ("tier_fals", "TIER_FALS", "{:.2f}"), ("alpha", "ALPHA", "{:.2f}"),
                           ("sep_max", "SEP_MAX", "{:.2f}"), ("sep_ci", "SEP_CI", "{:.2f}"),
                           ("sep_floor", "SEP_N_FLOOR", "{}"), ("complete_share", "COMPLETE_SHARE", "{:.0%}")):
        put(f"rv.threshold.{key}", const[name], fmt.format(const[name]), f"{SC}: module constant {name}")
    rf = None
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "RATED_FLOOR" for t in node.targets):
            v = node.value
            assert isinstance(v, ast.BinOp) and isinstance(v.op, ast.Div)
            rf = (v.left.value, v.right.value)
    put("rv.threshold.rated_floor", rf[0] / rf[1], f"{rf[0]:g} in {rf[1]:g}", f"{SC}: module constant RATED_FLOOR")
    th = d["verdicts"]["H_Spread"]["thresholds"]
    put("rv.threshold.spread_confirm", th["confirmed_at_least"], str(th["confirmed_at_least"]),
        f"{VF}:verdicts.H_Spread.thresholds.confirmed_at_least")
    put("rv.threshold.spread_falsify", th["falsified_at_most"], str(th["falsified_at_most"]),
        f"{VF}:verdicts.H_Spread.thresholds.falsified_at_most")
    budget = d["manipulation_checks"]["MC_Budget"]
    cap = budget["cap_usd"]
    put("rv.budget.cap", cap, f"${cap:,.0f}", f"{VF}:manipulation_checks.MC_Budget.cap_usd")

    meta = {"inputs": {VF: sha(VF), UT: sha(UT), PV: sha(PV), SC: sha(SC)}, "script": "reports/v44_report_values.py"}
    (ROOT / OUT_JSON).write_text(json.dumps({"_meta": meta, "values": VALS}, indent=1, ensure_ascii=False) + "\n",
                                 encoding="utf-8")
    print(f"wrote {OUT_JSON}: {len(VALS)} values")


if __name__ == "__main__":
    main()
