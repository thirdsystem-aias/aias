#!/usr/bin/env python3
"""v0.44 paper values: every number the paper and its figures print, read from the repository's v0.44 files.

Reads only scored or recorded files (nothing is typed by hand):
  osf/v44/v44_verdicts.json            (score_v0_44.py --run, once; commit 306af42)
  osf/v44/v44_unit_table.csv           (same run)
  osf/v44/data/v44_raw.jsonl           (acquire_v0_44.py --collect; main pass + re-run pass)
  osf/v44/data/coded/*.csv             (code_v0_44.py)
  osf/v44/data/v44_budget_state.json
  osf/v44/registries/industries_v0_44.csv
  osf/v42/v42_brand_table.csv at commit 31c64c6 (branch v0.42; read with `git show`, never checked out):
      only for the H_Spread "reported alongside" omnibus comparison (pre-registration 2.2), which the
      locked scorer does not output; computed here after scoring and labelled so in the paper.

Writes papers/v0_44/v44_values.json: {"_meta": {...}, "values": {key: {"value", "display", "source"}}}.
Run from the worktree root:  python3 papers/v0_44/values_v0_44.py
"""
import csv
import hashlib
import io
import json
import statistics
import subprocess
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_JSON = "papers/v0_44/v44_values.json"
V42_COMMIT = "31c64c6"
V42_PATH = "osf/v42/v42_brand_table.csv"

VALS = {}
CT = timezone(timedelta(hours=-6))  # US Central Standard Time on 2026-11-24
MODELS = ["claude-fable-5-2", "gpt-6-astra", "gemini-4-argon"]
INDS = ["INS", "HOT", "GRO", "QSR", "APR", "PHA", "CVF", "FAS"]


def put(key, value, display, source):
    if key in VALS:
        raise KeyError(f"duplicate key {key}")
    VALS[key] = {"value": value, "display": display, "source": source}


def f3(x):
    s = f"{x:.3f}"
    return s.replace("-", "−") if x < 0 else s


def f2(x):
    s = f"{x:.2f}"
    return s.replace("-", "−") if x < 0 else s


def pct(x, nd=0):
    return f"{100 * x:.{nd}f}%"


def pfmt(p):
    return "< 0.001" if p < 0.001 else f"{p:.3f}"


def usd(x, nd=2):
    return f"${x:,.{nd}f}"


def num(n):
    return f"{n:,}"


def read_csv(rel):
    return list(csv.DictReader(io.StringIO((ROOT / rel).read_text(encoding="utf-8"))))


def main():
    vf = "osf/v44/v44_verdicts.json"
    d = json.loads((ROOT / vf).read_text(encoding="utf-8"))
    mc = d["manipulation_checks"]
    ver = d["verdicts"]
    de = d["descriptives"]

    # ---------- design and manipulation checks
    put("design.expected_total", d["design"]["expected_total"], num(d["design"]["expected_total"]), f"{vf}:design.expected_total")
    put("design.models_used", d["design"]["models_used"], ", ".join(d["design"]["models_used"]), f"{vf}:design.models_used")
    c = mc["MC_Complete"]
    put("MC_Complete.answered", c["answered"], num(c["answered"]), f"{vf}:manipulation_checks.MC_Complete.answered")
    put("MC_Complete.expected", c["expected"], num(c["expected"]), f"{vf}:manipulation_checks.MC_Complete.expected")
    put("MC_Complete.share", c["share"], pct(c["share"], 1), f"{vf}:manipulation_checks.MC_Complete.share")
    for k in ("MC_Complete", "MC_Served", "MC_Window", "MC_Budget"):
        put(f"{k}.pass", mc[k]["pass"], "PASS" if mc[k]["pass"] else "FAIL", f"{vf}:manipulation_checks.{k}.pass")
    put("MC_Parity.pass", mc["MC_Parity"]["passed"], "PASS" if mc["MC_Parity"]["passed"] else "FAIL", f"{vf}:manipulation_checks.MC_Parity.passed")
    put("MC_Parity.P1", mc["MC_Parity"]["detail"]["P1"], "PASS" if mc["MC_Parity"]["detail"]["P1"] else "FAIL", f"{vf}:manipulation_checks.MC_Parity.detail.P1")
    p2 = mc["MC_Parity"]["detail"]["P2"]
    put("MC_Parity.P2", p2["passed"], "PASS" if p2["passed"] else "FAIL", f"{vf}:manipulation_checks.MC_Parity.detail.P2.passed")
    put("MC_Parity.P2.lines_checked", p2["lines_checked"], num(p2["lines_checked"]), f"{vf}:manipulation_checks.MC_Parity.detail.P2.lines_checked")
    put("MC_Parity.P2.prompt_mismatches", p2["prompt_mismatches"], num(p2["prompt_mismatches"]), f"{vf}:manipulation_checks.MC_Parity.detail.P2.prompt_mismatches")
    put("MC_Parity.P2.sha_short", p2["probe_sha256"][:12], p2["probe_sha256"][:12], f"{vf}:manipulation_checks.MC_Parity.detail.P2.probe_sha256")
    put("MC_Served.n_mismatched", mc["MC_Served"]["n_mismatched"], num(mc["MC_Served"]["n_mismatched"]), f"{vf}:manipulation_checks.MC_Served.n_mismatched")
    tr = mc["MC_Truncation"]
    at_cap = sum(tr[m]["at_cap"] for m in MODELS)
    put("MC_Truncation.at_cap_total", at_cap, num(at_cap), f"{vf}:manipulation_checks.MC_Truncation.<model>.at_cap (sum)")
    flagged = any(tr[m]["flag_above_5pct"] for m in MODELS)
    put("MC_Truncation.flagged", flagged, "flagged" if flagged else "none flagged", f"{vf}:manipulation_checks.MC_Truncation.<model>.flag_above_5pct")
    put("MC_Truncation.pass", not flagged, "FLAG" if flagged else "PASS", f"{vf}:manipulation_checks.MC_Truncation.<model>.flag_above_5pct (none set)")
    w = mc["MC_Window"]
    t0 = datetime.fromisoformat(w["first_call_utc"])
    t1 = datetime.fromisoformat(w["last_call_utc"])
    put("MC_Window.first_ct", w["first_call_utc"], t0.astimezone(CT).strftime("%H:%M"), f"{vf}:manipulation_checks.MC_Window.first_call_utc (shown in US Central, UTC-6)")
    put("MC_Window.last_ct", w["last_call_utc"], t1.astimezone(CT).strftime("%H:%M"), f"{vf}:manipulation_checks.MC_Window.last_call_utc (shown in US Central, UTC-6)")
    put("MC_Window.first_utc", w["first_call_utc"], t0.strftime("%H:%M:%S"), f"{vf}:manipulation_checks.MC_Window.first_call_utc")
    put("MC_Window.last_utc", w["last_call_utc"], t1.strftime("%H:%M:%S"), f"{vf}:manipulation_checks.MC_Window.last_call_utc")
    put("MC_Window.span_hours", w["span_hours"], f"{w['span_hours']:.2f}", f"{vf}:manipulation_checks.MC_Window.span_hours")
    b = mc["MC_Budget"]
    put("MC_Budget.spend_usd", b["spend_usd"], usd(b["spend_usd"]), f"{vf}:manipulation_checks.MC_Budget.spend_usd")
    put("MC_Budget.raw_lines", b["raw_lines"], num(b["raw_lines"]), f"{vf}:manipulation_checks.MC_Budget.raw_lines")
    put("MC_Budget.never_sent", b["design_calls_never_sent"], num(b["design_calls_never_sent"]), f"{vf}:manipulation_checks.MC_Budget.design_calls_never_sent")

    # ---------- raw file: main pass vs re-run pass
    rf = "osf/v44/data/v44_raw.jsonl"
    raw = [json.loads(x) for x in (ROOT / rf).read_text(encoding="utf-8").splitlines() if x.strip()]
    errs = [x for x in raw if x["status"] != "ok"]
    err_ids = {x["call_id"] for x in errs}
    rerun = [x for x in raw if x["call_id"] in err_ids and x["status"] == "ok"]
    rerun_ids = {id(x) for x in rerun}
    main_ok = [x for x in raw if x["status"] == "ok" and id(x) not in rerun_ids]
    put("raw.lines", len(raw), num(len(raw)), f"{rf}: line count")
    put("raw.main_ok", len(main_ok), num(len(main_ok)), f"{rf}: status ok, excluding the re-run lines")
    put("raw.errors", len(errs), num(len(errs)), f"{rf}: status error")
    kinds = sorted({x["error"].split(":")[0] for x in errs})
    put("raw.error_kind", kinds, ", ".join(kinds), f"{rf}: error field of error lines")
    em = sorted({x["model_requested"] for x in errs})
    put("raw.error_model", em, ", ".join(em), f"{rf}: model_requested of error lines")
    ep = sorted({x["probe_id"] for x in errs})
    put("raw.error_probes", ep, ", ".join(ep), f"{rf}: probe_id of error lines")
    ets = sorted(datetime.fromisoformat(x["started_utc"]) for x in errs)
    put("raw.error_first_ct", ets[0].isoformat(), ets[0].astimezone(CT).strftime("%H:%M"), f"{rf}: started_utc of error lines (US Central)")
    put("raw.rerun_ok", len(rerun), num(len(rerun)), f"{rf}: re-run lines (call IDs of error lines, status ok)")
    rc = sum(float(x["cost_usd"] or 0) for x in rerun)
    put("raw.rerun_cost", rc, usd(rc, 6), f"{rf}: sum of cost_usd over the re-run lines")
    main_end = max(datetime.fromisoformat(x["finished_utc"]) for x in main_ok + errs)
    put("raw.main_end_ct", main_end.isoformat(), main_end.astimezone(CT).strftime("%H:%M"), f"{rf}: latest finished_utc of the main pass (US Central)")
    rs = min(datetime.fromisoformat(x["started_utc"]) for x in rerun)
    put("raw.rerun_start_ct", rs.isoformat(), rs.astimezone(CT).strftime("%H:%M"), f"{rf}: earliest started_utc of the re-run lines (US Central)")
    ner = sum(1 for x in raw if x.get("empty_retry") in (True, "True", "true"))
    put("raw.empty_retry", ner, num(ner), f"{rf}: lines with empty_retry true")
    nempty = sum(1 for x in raw if x["status"] == "empty")
    put("raw.empty", nempty, num(nempty), f"{rf}: lines with status empty")
    bs = json.loads((ROOT / "osf/v44/data/v44_budget_state.json").read_text())
    put("budget.window", bs["window"], f"{bs['window'][0]} to {bs['window'][1]}", "osf/v44/data/v44_budget_state.json:window")

    # ---------- coded tables
    ca = "osf/v44/data/coded/v44_phase_a.csv"
    cb = "osf/v44/data/coded/v44_phase_b.csv"
    cs = "osf/v44/data/coded/v44_alias_audit.csv"
    rows_a, rows_b, rows_s = read_csv(ca), read_csv(cb), read_csv(cs)
    put("coded.a_rows", len(rows_a), num(len(rows_a)), f"{ca}: data rows")
    put("coded.b_rows", len(rows_b), num(len(rows_b)), f"{cb}: data rows")
    nm = sum(int(r["mentioned"]) for r in rows_b)
    put("coded.b_mentions", nm, num(nm), f"{cb}: rows with mentioned = 1")
    put("alias.matches", len(rows_s), num(len(rows_s)), f"{cs}: data rows (MC_Alias)")
    na = len({r["call_id"] for r in rows_s})
    put("alias.answers", na, num(na), f"{cs}: distinct call_id")
    nu = len({r["unit_id"] for r in rows_s})
    put("alias.units", nu, num(nu), f"{cs}: distinct unit_id")
    nal = len({(r["unit_id"], r["alias"]) for r in rows_s})
    put("alias.aliases", nal, num(nal), f"{cs}: distinct (unit_id, alias)")
    by_unit = Counter((r["substrate"], r["brand"]) for r in rows_s)
    table = []
    for (ind, br), n in by_unit.most_common():
        als = Counter(r["alias"] for r in rows_s if r["substrate"] == ind and r["brand"] == br)
        table.append({"industry": ind, "brand": br, "n": n, "aliases": [[a, k] for a, k in als.most_common()]})
    put("alias.by_unit", table, "", f"{cs}: matches per unit and alias")

    # ---------- registries
    rg = "osf/v44/registries/industries_v0_44.csv"
    ind_rows = read_csv(rg)
    labels = {r["industry"]: r["label"] for r in ind_rows}
    put("reg.labels", labels, "", f"{rg}: label")
    tot = sum(int(r["units"]) for r in ind_rows)
    put("reg.units_total", tot, num(tot), f"{rg}: sum of units")

    # ---------- H_Spread
    hs = ver["H_Spread"]
    put("H_Spread.verdict", hs["verdict"], hs["verdict"], f"{vf}:verdicts.H_Spread.verdict")
    put("H_Spread.n_with_spread", hs["n_with_spread"], str(hs["n_with_spread"]), f"{vf}:verdicts.H_Spread.n_with_spread")
    put("H_Spread.n_industries", hs["n_industries"], str(hs["n_industries"]), f"{vf}:verdicts.H_Spread.n_industries")
    sds = {i: hs["per_industry"][i]["sd"] for i in INDS}
    lo, hi = min(sds, key=sds.get), max(sds, key=sds.get)
    put("H_Spread.sd_min", sds[lo], f3(sds[lo]), f"{vf}:verdicts.H_Spread.per_industry.{lo}.sd (minimum)")
    put("H_Spread.sd_min_ind", lo, labels[lo].lower(), f"{vf}:verdicts.H_Spread.per_industry (argmin sd)")
    put("H_Spread.sd_max", sds[hi], f3(sds[hi]), f"{vf}:verdicts.H_Spread.per_industry.{hi}.sd (maximum)")
    put("H_Spread.sd_max_ind", hi, labels[hi].lower(), f"{vf}:verdicts.H_Spread.per_industry (argmax sd)")
    lows = {i: hs["per_industry"][i]["sd_ci95"][0] for i in INDS}
    li = min(lows, key=lows.get)
    put("H_Spread.ci_low_min", lows[li], f3(lows[li]), f"{vf}:verdicts.H_Spread.per_industry.{li}.sd_ci95[0] (minimum lower bound)")
    put("H_Spread.ci_low_min_ind", li, labels[li].lower(), f"{vf}:verdicts.H_Spread.per_industry (argmin of the lower bound)")
    for i in INDS:
        p = hs["per_industry"][i]
        put(f"H_Spread.{i}.n", p["n"], str(p["n"]), f"{vf}:verdicts.H_Spread.per_industry.{i}.n")
        put(f"H_Spread.{i}.sd", p["sd"], f3(p["sd"]), f"{vf}:verdicts.H_Spread.per_industry.{i}.sd")
        put(f"H_Spread.{i}.ci", p["sd_ci95"], f"{f3(p['sd_ci95'][0])}–{f3(p['sd_ci95'][1])}", f"{vf}:verdicts.H_Spread.per_industry.{i}.sd_ci95")
        put(f"H_Spread.{i}.range", p["range"], f"{f2(p['range'][0])}–{f2(p['range'][1])}", f"{vf}:verdicts.H_Spread.per_industry.{i}.range")
        put(f"H_Spread.{i}.share0", p["share_at_0"], pct(p["share_at_0"]), f"{vf}:verdicts.H_Spread.per_industry.{i}.share_at_0")
        put(f"H_Spread.{i}.spread", p["spread"], "yes" if p["spread"] else "no", f"{vf}:verdicts.H_Spread.per_industry.{i}.spread")

    # ---------- H_Tier
    ht = ver["H_Tier"]
    put("H_Tier.verdict", ht["verdict"], ht["verdict"], f"{vf}:verdicts.H_Tier.verdict")
    put("H_Tier.n", ht["n"], str(ht["n"]), f"{vf}:verdicts.H_Tier.n")
    put("H_Tier.rho", ht["rho"], f3(ht["rho"]), f"{vf}:verdicts.H_Tier.rho")
    put("H_Tier.ci", ht["ci95_rho"], f"{f3(ht['ci95_rho'][0])}–{f3(ht['ci95_rho'][1])}", f"{vf}:verdicts.H_Tier.ci95_rho")
    put("H_Tier.p", ht["p_perm"], pfmt(ht["p_perm"]), f"{vf}:verdicts.H_Tier.p_perm")
    put("H_Tier.p_exact", ht["p_perm"], f"{ht['p_perm']:.5f}", f"{vf}:verdicts.H_Tier.p_perm")
    put("H_Tier.rho_unc", ht["rho_uncentred_comparability"], f3(ht["rho_uncentred_comparability"]), f"{vf}:verdicts.H_Tier.rho_uncentred_comparability")
    for i in INDS:
        put(f"H_Tier.{i}.rho", ht["per_industry_rho"][i], f3(ht["per_industry_rho"][i]), f"{vf}:verdicts.H_Tier.per_industry_rho.{i}")
    ra = ht["reported_alongside"]
    for var, short in (("eligible_rank", "elig"), ("without_FAS", "nofas"), ("without_pharmacy_units_from_other_metric", "nopha")):
        r = ra[var]
        base = f"{vf}:verdicts.H_Tier.reported_alongside.{var}"
        put(f"H_Tier.{short}.n", r["n"], str(r["n"]), f"{base}.n")
        put(f"H_Tier.{short}.rho", r["rho"], f3(r["rho"]), f"{base}.rho")
        put(f"H_Tier.{short}.ci", r["ci95_rho"], f"{f3(r['ci95_rho'][0])}–{f3(r['ci95_rho'][1])}", f"{base}.ci95_rho")
        put(f"H_Tier.{short}.p", r["p_perm"], pfmt(r["p_perm"]), f"{base}.p_perm")
        put(f"H_Tier.{short}.rho_unc", r["rho_uncentred_comparability"], f3(r["rho_uncentred_comparability"]), f"{base}.rho_uncentred_comparability")
    for i in INDS:
        put(f"H_Tier.elig.{i}.rho", ra["eligible_rank"]["per_industry_rho"][i], f3(ra["eligible_rank"]["per_industry_rho"][i]), f"{vf}:verdicts.H_Tier.reported_alongside.eligible_rank.per_industry_rho.{i}")
    x = ra["without_pharmacy_units_from_other_metric"]["per_industry_rho"]["PHA"]
    put("H_Tier.nopha.PHA.rho", x, f3(x), f"{vf}:verdicts.H_Tier.reported_alongside.without_pharmacy_units_from_other_metric.per_industry_rho.PHA")
    mt = ra["mean_pi_by_industry_tier"]
    for k, x in mt.items():
        i, t = k.split("|")
        put(f"H_Tier.mean.{i}.{t}", x, f2(x), f"{vf}:verdicts.H_Tier.reported_alongside.mean_pi_by_industry_tier.{k}")
    lgtc = sum(1 for i in INDS if mt[f"{i}|L"] > mt[f"{i}|C"])
    ctgs = sum(1 for i in INDS if mt[f"{i}|C"] > mt[f"{i}|S"])
    put("H_Tier.count_L_gt_C", lgtc, str(lgtc), f"{vf}:verdicts.H_Tier.reported_alongside.mean_pi_by_industry_tier (industries with L > C)")
    put("H_Tier.count_C_gt_S", ctgs, str(ctgs), f"{vf}:verdicts.H_Tier.reported_alongside.mean_pi_by_industry_tier (industries with C > S)")
    pir = ht["per_industry_rho"]
    a_, z_ = min(pir, key=pir.get), max(pir, key=pir.get)
    put("H_Tier.ind_rho_min", pir[a_], f3(pir[a_]), f"{vf}:verdicts.H_Tier.per_industry_rho (minimum)")
    put("H_Tier.ind_rho_min_ind", a_, labels[a_].lower(), f"{vf}:verdicts.H_Tier.per_industry_rho (argmin)")
    put("H_Tier.ind_rho_max", pir[z_], f3(pir[z_]), f"{vf}:verdicts.H_Tier.per_industry_rho (maximum)")
    put("H_Tier.ind_rho_max_ind", z_, labels[z_].lower(), f"{vf}:verdicts.H_Tier.per_industry_rho (argmax)")

    # ---------- H_Separation
    hp = ver["H_Separation"]
    put("H_Sep.verdict", hp["verdict"], hp["verdict"], f"{vf}:verdicts.H_Separation.verdict")
    put("H_Sep.n", hp["n_rated"], str(hp["n_rated"]), f"{vf}:verdicts.H_Separation.n_rated")
    put("H_Sep.rho", hp["rho"], f3(hp["rho"]), f"{vf}:verdicts.H_Separation.rho")
    put("H_Sep.ci", hp["ci95_rho"], f"{f3(hp['ci95_rho'][0])} to {f3(hp['ci95_rho'][1])}", f"{vf}:verdicts.H_Separation.ci95_rho")
    put("H_Sep.rho_unc", hp["rho_uncentred_comparability"], f3(hp["rho_uncentred_comparability"]), f"{vf}:verdicts.H_Separation.rho_uncentred_comparability")
    rs_ = hp["reported_alongside"]
    put("H_Sep.rho_raw_phi", rs_["rho_with_raw_phi"], f3(rs_["rho_with_raw_phi"]), f"{vf}:verdicts.H_Separation.reported_alongside.rho_with_raw_phi")
    for i in INDS:
        put(f"H_Sep.{i}.rho", rs_["per_industry_rho"][i], f3(rs_["per_industry_rho"][i]), f"{vf}:verdicts.H_Separation.reported_alongside.per_industry_rho.{i}")
    pc = rs_["partition_counts_per_run"]
    for k in ("zero", "saturated", "defined"):
        put(f"H_Sep.part_run.{k}", pc[k], num(pc[k]), f"{vf}:verdicts.H_Separation.reported_alongside.partition_counts_per_run.{k}")
    put("H_Sep.part_run.total", sum(pc.values()), num(sum(pc.values())), f"{vf}:verdicts.H_Separation.reported_alongside.partition_counts_per_run (sum)")
    up = rs_["unit_partitions"]
    for k in ("zero", "saturated", "defined", "undefined"):
        put(f"H_Sep.part_unit.{k}", up[k], num(up[k]), f"{vf}:verdicts.H_Separation.reported_alongside.unit_partitions.{k}")
    un = rs_["unrated_share_by_industry_tier"]
    for i in INDS:
        u = sum(v_["unrated"] for k, v_ in un.items() if k.startswith(i + "|"))
        n = sum(v_["units"] for k, v_ in un.items() if k.startswith(i + "|"))
        put(f"H_Sep.unrated.{i}", [u, n], f"{u} of {n}", f"{vf}:verdicts.H_Separation.reported_alongside.unrated_share_by_industry_tier.{i}|* (summed over tiers)")
    for t in ("L", "C", "S", "G"):
        u = sum(v_["unrated"] for k, v_ in un.items() if k.endswith("|" + t))
        n = sum(v_["units"] for k, v_ in un.items() if k.endswith("|" + t))
        put(f"H_Sep.unrated.tier.{t}", [u, n], f"{u} of {n}", f"{vf}:verdicts.H_Separation.reported_alongside.unrated_share_by_industry_tier.*|{t} (summed over industries)")
    rated_ind = {i: sum(v_["units"] - v_["unrated"] for k, v_ in un.items() if k.startswith(i + "|")) for i in INDS}
    put("H_Sep.rated_ind_min", min(rated_ind.values()), str(min(rated_ind.values())), f"{vf}:verdicts.H_Separation.reported_alongside.unrated_share_by_industry_tier (units - unrated per industry, minimum)")
    put("H_Sep.rated_ind_max", max(rated_ind.values()), str(max(rated_ind.values())), f"{vf}:verdicts.H_Separation.reported_alongside.unrated_share_by_industry_tier (units - unrated per industry, maximum)")
    ut_all = sum(v_["unrated"] for v_ in un.values())
    put("H_Sep.unrated.total", ut_all, str(ut_all), f"{vf}:verdicts.H_Separation.reported_alongside.unrated_share_by_industry_tier (sum)")

    # unit table
    ut = "osf/v44/v44_unit_table.csv"
    units = read_csv(ut)
    put("unit.rows", len(units), num(len(units)), f"{ut}: data rows")
    rated = [u for u in units if u["rated"] == "1"]
    put("unit.rated", len(rated), num(len(rated)), f"{ut}: rows with rated = 1")
    put("unit.rated_points", [[u["industry"], float(u["pi_hat"]), float(u["c_phi"])] for u in rated], "", f"{ut}: industry, pi_hat, c_phi of rated rows")
    cph = [float(u["c_phi"]) for u in rated]
    put("unit.cphi_min", min(cph), f"{min(cph):.1f}", f"{ut}: c_phi of rated rows (minimum)")
    put("unit.cphi_max", max(cph), f"{max(cph):.1f}", f"{ut}: c_phi of rated rows (maximum)")
    gr = [u["brand"] for u in rated if u["tier"] == "G"]
    put("unit.ghosts_rated", gr, " and ".join(gr), f"{ut}: rated rows with tier G")

    # ---------- descriptives
    d1 = de["1_presence_by_model_industry_tier"]
    for m in MODELS:
        for i in INDS:
            x = d1[f"{m}|{i}|all"]
            for k in ("mean", "sd", "share_0", "share_1"):
                put(f"D1.{m}.{i}.{k}", x[k], f2(x[k]), f"{vf}:descriptives.1_presence_by_model_industry_tier.{m}|{i}|all.{k}")
            put(f"D1.{m}.{i}.n", x["n"], str(x["n"]), f"{vf}:descriptives.1_presence_by_model_industry_tier.{m}|{i}|all.n")
            for t in ("L", "C", "S", "G"):
                kk = f"{m}|{i}|{t}"
                if kk in d1:
                    put(f"D1.{m}.{i}.{t}.mean", d1[kk]["mean"], f2(d1[kk]["mean"]), f"{vf}:descriptives.1_presence_by_model_industry_tier.{kk}.mean")
    sdk = {(m, i): d1[f"{m}|{i}|all"]["sd"] for m in MODELS for i in INDS}
    mk = min(sdk, key=sdk.get)
    put("D1.sd_min", sdk[mk], f2(sdk[mk]), f"{vf}:descriptives.1_presence_by_model_industry_tier.{mk[0]}|{mk[1]}|all.sd (minimum over models and industries)")
    mname = {"claude-fable-5-2": "Claude Fable 5.2", "gpt-6-astra": "GPT-6 Astra", "gemini-4-argon": "Gemini 4 Argon"}
    put("D1.sd_min_where", list(mk), f"{mname[mk[0]]}, {labels[mk[1]].lower()}", f"{vf}:descriptives.1_presence_by_model_industry_tier (argmin of sd)")
    gaps = {i: max(d1[f"{m}|{i}|all"]["mean"] for m in MODELS) - min(d1[f"{m}|{i}|all"]["mean"] for m in MODELS) for i in INDS}
    gi = max(gaps, key=gaps.get)
    put("D1.max_model_gap", gaps[gi], f2(gaps[gi]), f"{vf}:descriptives.1_presence_by_model_industry_tier.<model>|<industry>|all.mean (largest max-min across models)")
    put("D1.max_model_gap_ind", gi, labels[gi].lower(), f"{vf}:descriptives.1_presence_by_model_industry_tier (industry of the largest gap)")
    d2 = de["2_recognition"]
    for m in MODELS:
        for i in INDS:
            x = d2["share_per_model_industry"][f"{m}|{i}"]
            put(f"D2.{m}.{i}", [x["recognized"], x["coded"]], f"{x['recognized']}/{x['coded']}", f"{vf}:descriptives.2_recognition.share_per_model_industry.{m}|{i}")
        rec = sum(d2["share_per_model_industry"][f"{m}|{i}"]["recognized"] for i in INDS)
        cod = sum(d2["share_per_model_industry"][f"{m}|{i}"]["coded"] for i in INDS)
        put(f"D2.{m}.all", [rec, cod], f"{rec}/{cod}", f"{vf}:descriptives.2_recognition.share_per_model_industry.{m}|* (summed)")
    g = d2["recognised_by_all_three_with_pi_0_by_tier"]
    for t in ("L", "C", "S", "G"):
        put(f"D2.gap.{t}", g[t], str(g[t]), f"{vf}:descriptives.2_recognition.recognised_by_all_three_with_pi_0_by_tier.{t}")
    put("D2.gap.total", sum(g.values()), str(sum(g.values())), f"{vf}:descriptives.2_recognition.recognised_by_all_three_with_pi_0_by_tier (sum)")
    for k, x in de["3_ghosts"].items():
        _, nm_ = k.split("|")
        key = nm_.replace("&", "and").replace(" ", "")
        put(f"D3.{key}.pi", x["pi"], f2(x["pi"]), f"{vf}:descriptives.3_ghosts.{k}.pi")
        nrec = sum(x["recognition"][m] for m in MODELS)
        put(f"D3.{key}.rec", nrec, f"{nrec} of 3", f"{vf}:descriptives.3_ghosts.{k}.recognition (sum over models)")
    d4 = de["4_run_reliability"]
    for m in MODELS:
        put(f"D4.{m}.rel1", d4[m]["rel1"], f3(d4[m]["rel1"]), f"{vf}:descriptives.4_run_reliability.{m}.rel1")
        put(f"D4.{m}.rel3", d4[m]["rel3"], f3(d4[m]["rel3"]), f"{vf}:descriptives.4_run_reliability.{m}.rel3")
    for k, x in de["5_model_agreement"].items():
        a, b_ = k.split("~")
        put(f"D5.{a}.{b_}", x["rho_pw"], f3(x["rho_pw"]), f"{vf}:descriptives.5_model_agreement.{k}.rho_pw")
        put(f"D5.{a}.{b_}.n", x["n"], str(x["n"]), f"{vf}:descriptives.5_model_agreement.{k}.n")
    d6 = de["6_non_registry_names_in_phase_b"]
    for i in INDS:
        put(f"D6.{i}.distinct", d6[i]["distinct"], str(d6[i]["distinct"]), f"{vf}:descriptives.6_non_registry_names_in_phase_b.{i}.distinct")
        put(f"D6.{i}.top10", d6[i]["top10"], "; ".join(f"{n} ({k})" for n, k in d6[i]["top10"]), f"{vf}:descriptives.6_non_registry_names_in_phase_b.{i}.top10")
    for k, x in de["7_units_in_two_industries"].items():
        for kk, val in x.items():
            ind, _ = kk.split(":")
            put(f"D7.{k}.{ind}", val, f2(val), f"{vf}:descriptives.7_units_in_two_industries.{k}.{kk}")
    d8 = de["8_answer_form"]
    for m in MODELS:
        x = d8[m]
        put(f"D8.{m}.wB", x["words_B_mean"], f"{x['words_B_mean']:.0f}", f"{vf}:descriptives.8_answer_form.{m}.words_B_mean")
        put(f"D8.{m}.wA", x["words_A_mean"], f"{x['words_A_mean']:.1f}", f"{vf}:descriptives.8_answer_form.{m}.words_A_mean")
        put(f"D8.{m}.units", x["registry_units_per_B_answer"], f"{x['registry_units_per_B_answer']:.2f}", f"{vf}:descriptives.8_answer_form.{m}.registry_units_per_B_answer")
        fr = x["finish_reasons"]
        put(f"D8.{m}.finish", fr, ", ".join(f"{k.replace('FinishReason.', '')} {v_}" for k, v_ in fr.items()), f"{vf}:descriptives.8_answer_form.{m}.finish_reasons")
        for k in ("refusals", "unanswered", "phase_A_ambiguous"):
            put(f"D8.{m}.{k}", x[k], str(x[k]), f"{vf}:descriptives.8_answer_form.{m}.{k}")
    d9 = de["9_cost"]
    put("D9.total", d9["total_usd"], usd(d9["total_usd"]), f"{vf}:descriptives.9_cost.total_usd")
    for k, x in d9["per_model_phase"].items():
        m, ph = k.split("|")
        base = f"{vf}:descriptives.9_cost.per_model_phase.{k}"
        put(f"D9.{m}.{ph}.usd", x["usd"], usd(x["usd"]), f"{base}.usd")
        put(f"D9.{m}.{ph}.in", x["input_tokens"], num(x["input_tokens"]), f"{base}.input_tokens")
        put(f"D9.{m}.{ph}.out", x["output_tokens"], num(x["output_tokens"]), f"{base}.output_tokens")
        put(f"D9.{m}.{ph}.think", x["thinking_tokens"], num(x["thinking_tokens"]), f"{base}.thinking_tokens")
        put(f"D9.{m}.{ph}.lines", x["raw_lines"], num(x["raw_lines"]), f"{base}.raw_lines")
        put(f"D9.{m}.{ph}.billed", x["billed_requests"], num(x["billed_requests"]), f"{base}.billed_requests")
    est = sum(x["estimated_worst_case_parts"] for x in d9["per_model_phase"].values())
    put("D9.est_parts", est, num(est), f"{vf}:descriptives.9_cost.per_model_phase.*.estimated_worst_case_parts (sum)")
    for m in MODELS:
        s = d9["per_model_phase"][f"{m}|A"]["usd"] + d9["per_model_phase"][f"{m}|B"]["usd"]
        put(f"D9.{m}.usd", s, usd(s), f"{vf}:descriptives.9_cost.per_model_phase.{m}|A+B usd")
    for ph in ("A", "B"):
        s = sum(d9["per_model_phase"][f"{m}|{ph}"]["usd"] for m in MODELS)
        put(f"D9.{ph}.usd", s, usd(s), f"{vf}:descriptives.9_cost.per_model_phase.*|{ph}.usd (sum)")

    # ---------- H_Spread reported alongside: omnibus SD on N3 at t4 (v0.42), computed after scoring
    raw42 = subprocess.run(["git", "-C", str(ROOT), "show", f"{V42_COMMIT}:{V42_PATH}"], capture_output=True, text=True, check=True).stdout
    sha42 = hashlib.sha256(raw42.encode("utf-8")).hexdigest()
    r42 = list(csv.DictReader(io.StringIO(raw42)))
    subs = sorted({r["substrate"] for r in r42})
    src42 = f"git show {V42_COMMIT}:{V42_PATH} (sha256 {sha42[:12]}), column pi_N3_S0; population SD per substrate"
    put("omni.sha", sha42, sha42[:12] + "…", f"git show {V42_COMMIT}:{V42_PATH}")
    names = {"v0.19": "headphones", "v0.20": "skincare", "v0.21": "cosmetics", "v0.22": "cars", "v0.23": "spirits"}
    nsp = 0
    for s in subs:
        xs = [float(r["pi_N3_S0"]) for r in r42 if r["substrate"] == s and r["pi_N3_S0"] not in ("", "None")]
        sd = statistics.pstdev(xs)
        nsp += sd >= 0.15
        put(f"omni.{s}.sd", sd, f3(sd), src42)
        put(f"omni.{s}.n", len(xs), str(len(xs)), src42 + "; units with a value")
        put(f"omni.{s}.name", names.get(s, s), names.get(s, s), "category name of the omnibus substrate")
    put("omni.n_spread", nsp, str(nsp), src42 + "; substrates with SD >= 0.15")
    put("omni.n_sub", len(subs), str(len(subs)), src42)

    meta = {"inputs": {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in
                       [vf, ut, rf, ca, cb, cs, rg, "osf/v44/data/v44_budget_state.json"]},
            "v42_brand_table": {"commit": V42_COMMIT, "path": V42_PATH, "sha256": sha42},
            "script": "papers/v0_44/values_v0_44.py"}
    (ROOT / OUT_JSON).write_text(json.dumps({"_meta": meta, "values": VALS}, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT_JSON}: {len(VALS)} values")


if __name__ == "__main__":
    main()
