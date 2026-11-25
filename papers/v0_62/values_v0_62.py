#!/usr/bin/env python3
"""v0.62 paper values: every number the paper and its figures print, read from the repository's v0.62 files.

Reads only scored, recorded or archived files (nothing is typed by hand):
  osf/v62/v62_verdicts.json                         (score_v0_62.py, run once; commit 262464d)
  osf/v62/data/v62_sens_coi106_v0_62.json           (DEVIATIONS Entry 4; commit 4ac1aa9)
  osf/v62/data/v62_sens_ai_check_v0_62.json         (DEVIATIONS Entry 5; commit 4ac1aa9)
  osf/v62/data/v62_sens_en_corrected_v0_62.json     (DEVIATIONS Entry 6; commit 4ac1aa9)
  osf/v62/ai_check/results/ai_check_analysis_v0_62.json  (DEVIATIONS Entry 2; commit 366a45b)
  osf/v62/data/v62_raw.jsonl, collect_v0_62.log, collect_v0_62_rerun.log, v62_budget_state.json
  osf/v62/data/gates/gate_P1real_P3_v0_62.json, gate_P2_v0_62.json, osf/v62/data/coded/v62_alias_audit.csv
  osf/v62/scripts/budget_v0_62.py                   (locked; only its worst_case() price rule is called)
  osf/v62/data/v62_planned_items_summary_v0_62.json, v62_planned_items_v0_62.json,
  v62_planned_category_labels_v0_62.csv, v62_planned_top10_shift_v0_62.csv, v62_planned_checks_v0_62.csv
                                                    (DEVIATIONS Entry 7; commit 69e1aa9; CSVs cross-checked against the JSON)
  osf/v62/DEVIATIONS.md                             (entry count; Entry 8 figures checked against the recomputed ones)

Computed here (no output file holds them; each is labelled "computed for the paper" in its source field):
the strict worst-case charge of the timed-out call under pre-registration section 6.5 rule 2 (by the locked
budget module's own worst_case()), and three sums or ratios of recorded figures.

Writes papers/v0_62/v62_values.json: {"_meta": {...}, "values": {key: {"value", "display", "source"}}}.
Run from the worktree root:  python3 papers/v0_62/values_v0_62.py
"""
import csv
import hashlib
import json
import re
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
V62 = ROOT / "osf/v62"
OUT_JSON = ROOT / "papers/v0_62/v62_values.json"
CT = timezone(timedelta(hours=-6))  # US Central Standard Time on 2026-11-25
LANGS = ["es", "ko", "zh"]
MODELS = ["claude-fable-5-2", "gpt-6-astra", "gemini-4-argon"]

VALS = {}
INPUTS = {}


def put(key, value, display, source):
    if key in VALS:
        raise KeyError(f"duplicate key {key}")
    VALS[key] = {"value": value, "display": display, "source": source}


def _read(rel):
    p = V62 / rel
    INPUTS["osf/v62/" + rel] = hashlib.sha256(p.read_bytes()).hexdigest()
    return p.read_text(encoding="utf-8")


def load(rel):
    return json.loads(_read(rel))


def f3(x):
    s = f"{x:.3f}"
    return s.replace("-", "−") if x < 0 else s


def f4(x):
    s = f"{x:.4f}"
    return s.replace("-", "−") if x < 0 else s


def sgn3(x):
    return ("+" if x >= 0 else "−") + f"{abs(x):.3f}"


def pfmt(p):
    return "< 0.001" if p < 0.001 else f"{p:.4f}"


def usd(x, nd=4):
    return f"${x:,.{nd}f}"


def put_test(prefix, d, src, with_delta=False):
    """Standard fields of one rank-test record (score_v0_62.rank_test output)."""
    ci = d["ci95_rho_c"]
    put(f"{prefix}.n", d["n"], str(d["n"]), src)
    put(f"{prefix}.rho", d["rho_c"], f3(d["rho_c"]), src)
    put(f"{prefix}.rho4", d["rho_c"], f4(d["rho_c"]), src)
    put(f"{prefix}.ci", ci, f"{f3(ci[0])}–{f3(ci[1])}", src)
    put(f"{prefix}.ci4", ci, f"{f4(ci[0])}–{f4(ci[1])}", src)
    put(f"{prefix}.p", d["p_perm"], pfmt(d["p_perm"]), src)
    put(f"{prefix}.p4", d["p_perm"], f"{d['p_perm']:.4f}", src)
    put(f"{prefix}.unc", d["rho_uncentred_comparability"], f3(d["rho_uncentred_comparability"]), src)
    put(f"{prefix}.verdict", d["verdict"], d["verdict"], src)
    for c, r in d.get("per_category_rho_c", {}).items():
        put(f"{prefix}.cat.{c}", r, f3(r), src)
    if with_delta:
        dci = d["delta_L_ci95"]
        put(f"{prefix}.dL", d["delta_L"], sgn3(d["delta_L"]), src)
        put(f"{prefix}.dL4", d["delta_L"], ("+" if d["delta_L"] >= 0 else "−") + f"{abs(d['delta_L']):.4f}", src)
        put(f"{prefix}.dL_ci", dci, f"{sgn3(dci[0])} to {sgn3(dci[1])}", src)


def verdicts():
    V = load("v62_verdicts.json")
    src = "osf/v62/v62_verdicts.json"
    put("design.n_units", V["n_units"], str(V["n_units"]), src + " n_units")
    put("design.option", V["headphones_option"], V["headphones_option"], src + " headphones_option")
    put("joint", V["joint_reading"], V["joint_reading"], src + " joint_reading")
    T = V["tests"]
    for L in LANGS:
        put_test(f"P.{L}", T[f"H_Lang_Presence_{L}"], f"{src} tests.H_Lang_Presence_{L}", with_delta=True)
        ph = T[f"H_Lang_Phi_{L}"]
        put_test(f"Phi.{L}", ph, f"{src} tests.H_Lang_Phi_{L}")
        for part in ("defined", "zero", "saturated", "undefined"):
            k = ph["partitions"].get(part, 0)
            put(f"Phi.{L}.part.{part}", k, str(k), f"{src} tests.H_Lang_Phi_{L}.partitions (absent = 0)")
        put(f"Rank.{L}.verdict", T[f"H_Lang_Rank_{L}"]["verdict"], T[f"H_Lang_Rank_{L}"]["verdict"],
            f"{src} tests.H_Lang_Rank_{L}")
        for s in ("S-Denon", "S-Headphones", "S-COI"):
            put_test(f"{s}.{L}", V["sensitivities"][f"{s}_{L}"], f"{src} sensitivities.{s}_{L}")
    reason = T["H_Lang_Rank_es"]["reason"]
    assert all(T[f"H_Lang_Rank_{L}"]["reason"] == reason for L in LANGS)
    put("Rank.reason", reason, reason, f"{src} tests.H_Lang_Rank_*.reason")
    put("Rank.v114_commit", re.search(r"commit ([0-9a-f]{7})", reason).group(1),
        re.search(r"commit ([0-9a-f]{7})", reason).group(1), f"{src} tests.H_Lang_Rank_*.reason")
    cats = [T[f"H_Lang_Presence_{L}"]["per_category_rho_c"][c] for L in LANGS for c in T["H_Lang_Presence_es"]["per_category_rho_c"]]
    put("P.cat_min", min(cats), f3(min(cats)), f"{src} tests.H_Lang_Presence_*.per_category_rho_c (minimum of 15)")
    put("P.cat_max", max(cats), f3(max(cats)), f"{src} tests.H_Lang_Presence_*.per_category_rho_c (maximum of 15)")
    n70 = sum(c >= 0.70 for c in cats)
    put("P.cat_n70", n70, str(n70), f"{src} tests.H_Lang_Presence_*.per_category_rho_c (count >= 0.70)")
    pcs = [T[f"H_Lang_Phi_{L}"]["per_category_rho_c"][c] for L in LANGS for c in T["H_Lang_Phi_es"]["per_category_rho_c"]]
    put("Phi.cat_min", min(pcs), f3(min(pcs)), f"{src} tests.H_Lang_Phi_*.per_category_rho_c (minimum of 15)")
    nneg = sum(c < 0 for c in pcs)
    put("Phi.cat_nneg", nneg, str(nneg), f"{src} tests.H_Lang_Phi_*.per_category_rho_c (count < 0)")
    return V


def coi106(V):
    S = load("data/v62_sens_coi106_v0_62.json")
    src = "osf/v62/data/v62_sens_coi106_v0_62.json"
    assert S["reproduced_locked_verdicts_byte_for_byte"] and S["no_model_called"]
    put("COI.n_as_run", S["n_units_as_run"], str(S["n_units_as_run"]), src + " n_units_as_run")
    put("COI.n_106", S["n_units_106"], str(S["n_units_106"]), src + " n_units_106")
    put("COI.left_in_id", S["unit_left_in_by_locked_code"][1], S["unit_left_in_by_locked_code"][1],
        src + " unit_left_in_by_locked_code")
    put("COI.n_flagged", len(S["coi_flagged_params"]), str(len(S["coi_flagged_params"])), src + " coi_flagged_params")
    for L in LANGS:
        put_test(f"S-COI106.{L}", S["sensitivities"][f"S-COI-106_{L}"], f"{src} sensitivities.S-COI-106_{L}")
        assert S["summary"][L]["S-COI_as_run_107"]["rho_c"] == V["sensitivities"][f"S-COI_{L}"]["rho_c"]


def ai_sens(V):
    S = load("data/v62_sens_ai_check_v0_62.json")
    src = "osf/v62/data/v62_sens_ai_check_v0_62.json"
    assert S["wrapper"]["no_model_called"] and S["wrapper"]["primary_keys_equal_locked_verdicts"]
    assert S["tests"] == V["tests"] and S["joint_reading"] == V["joint_reading"]
    ai = S["sensitivities_ai_check"]
    for line in ("flagged", "strictly_flagged"):
        st = ai["S-Trans"][line]
        s = f"{src} sensitivities_ai_check.S-Trans.{line}"
        put(f"STrans.{line}.joint", st["joint_reading"], st["joint_reading"], s + ".joint_reading")
        for L in LANGS:
            put(f"STrans.{line}.{L}.removed", len(st["removed"][L]), str(len(st["removed"][L])), s + f".removed.{L} (count)")
            put(f"STrans.{line}.{L}.differs", st["presence_differs"][L], "yes" if st["presence_differs"][L] else "no",
                s + f".presence_differs.{L}")
            put_test(f"STrans.{line}.P.{L}", st["tests"][f"H_Lang_Presence_{L}"], s + f".tests.H_Lang_Presence_{L}")
            put_test(f"STrans.{line}.Phi.{L}", st["tests"][f"H_Lang_Phi_{L}"], s + f".tests.H_Lang_Phi_{L}")
            same = st["tests"][f"H_Lang_Presence_{L}"] == V["tests"][f"H_Lang_Presence_{L}"] and \
                st["tests"][f"H_Lang_Phi_{L}"] == V["tests"][f"H_Lang_Phi_{L}"]
            put(f"STrans.{line}.{L}.equal_locked", same, "yes" if same else "no", s + " vs v62_verdicts.json tests")
    for L in ("ko", "zh"):
        put_test(f"SAliasAI.{L}", ai["S-AliasAI"][f"S-AliasAI_{L}"],
                 f"{src} sensitivities_ai_check.S-AliasAI.S-AliasAI_{L}")
    return ai


def en_corrected(V):
    S = load("data/v62_sens_en_corrected_v0_62.json")
    src = "osf/v62/data/v62_sens_en_corrected_v0_62.json"
    assert S["reproduced_locked_verdicts_byte_for_byte"] and S["no_model_called"]
    R = S["result_corrected"]
    put("ENC.joint", R["joint_reading"], R["joint_reading"], src + " result_corrected.joint_reading")
    for L in LANGS:
        put_test(f"ENC.P.{L}", R["tests"][f"H_Lang_Presence_{L}"], f"{src} result_corrected.tests.H_Lang_Presence_{L}",
                 with_delta=True)
        put_test(f"ENC.Phi.{L}", R["tests"][f"H_Lang_Phi_{L}"], f"{src} result_corrected.tests.H_Lang_Phi_{L}")
        for s in ("S-Denon", "S-Headphones", "S-COI"):
            put_test(f"ENC.{s}.{L}", R["sensitivities"][f"{s}_{L}"], f"{src} result_corrected.sensitivities.{s}_{L}")
        put_test(f"ENC.S-COI106.{L}", S["s_coi_106_corrected"][f"S-COI-106_{L}"],
                 f"{src} s_coi_106_corrected.S-COI-106_{L}")
    same = all(R["tests"][k]["verdict"] == V["tests"][k]["verdict"] for k in V["tests"]) and \
        all(R["sensitivities"][k]["verdict"] == V["sensitivities"][k]["verdict"] for k in V["sensitivities"])
    put("ENC.all_verdicts_same", same, "yes" if same else "no", src + " result_corrected vs v62_verdicts.json")


def ai_check():
    A = load("ai_check/results/ai_check_analysis_v0_62.json")
    src = "osf/v62/ai_check/results/ai_check_analysis_v0_62.json"
    put("AIC.spend", A["recorded_spend_usd"], usd(A["recorded_spend_usd"]), src + " recorded_spend_usd")
    put("AIC.cap", A["cap_usd"], usd(A["cap_usd"], 0), src + " cap_usd")
    put("AIC.requests", A["n_requests"], str(A["n_requests"]), src + " n_requests")
    for L in LANGS:
        d = A["languages"][L]
        s = f"{src} languages.{L}"
        put(f"AIC.{L}.items", d["n_items"], str(d["n_items"]), s + ".n_items")
        for pair in ("claude_vs_c2", "claude_vs_c3", "c2_vs_c3"):
            pr = d["pairs"][pair]
            put(f"AIC.{L}.{pair}.n", pr["n"], str(pr["n"]), f"{s}.pairs.{pair}.n")
            put(f"AIC.{L}.{pair}.agree", pr["agreement_pct"], f"{pr['agreement_pct']:.0f}%", f"{s}.pairs.{pair}.agreement_pct")
            put(f"AIC.{L}.{pair}.kappa", pr["kappa"], f"{pr['kappa']:.2f}", f"{s}.pairs.{pair}.kappa")
            put(f"AIC.{L}.{pair}.wkappa", pr["kappa_linear_weighted"], f"{pr['kappa_linear_weighted']:.2f}",
                f"{s}.pairs.{pair}.kappa_linear_weighted")
        for k in ("flagged", "strictly_flagged", "phase_b_flagged", "phase_b_strictly_flagged", "templates_flagged",
                  "labels_flagged"):
            put(f"AIC.{L}.{k}", len(d[k]), str(len(d[k])), f"{s}.{k} (count)")
        nat = d["c2_naturalness"]
        for k in ("natural", "acceptable", "unnatural"):
            put(f"AIC.{L}.nat.{k}", nat.get(k, 0), str(nat.get(k, 0)), f"{s}.c2_naturalness (absent = 0)")
        for k, n in d["c2_checklist_counts"].items():
            put(f"AIC.{L}.check.{k}", n, str(n), f"{s}.c2_checklist_counts.{k}")
        put(f"AIC.{L}.rule_e", d["rule_e_decision"], "yes" if d["rule_e_decision"] else "no", f"{s}.rule_e_decision")
    for L in ("ko", "zh"):
        a = A["aliases"][L]
        s = f"{src} aliases.{L}"
        put(f"AIC.alias.{L}.rows", a["n_rows"], str(a["n_rows"]), s + ".n_rows")
        put(f"AIC.alias.{L}.n", a["n_aliases"], str(a["n_aliases"]), s + ".n_aliases")
        for k in ("standard", "acceptable variant", "not used for this brand", "unknown"):
            n = a["usage_counts"].get(k, 0)
            put(f"AIC.alias.{L}.{k.replace(' ', '_')}", n, str(n), s + ".usage_counts (absent = 0)")
        put(f"AIC.alias.{L}.common", a["common_word_count"], str(a["common_word_count"]), s + ".common_word_count")
    off = A["aliases"]["ko"]["not_used_for_this_brand"]
    assert len(off) == 1
    put("AIC.alias.ko.off_brand", off[0][1], off[0][1], src + " aliases.ko.not_used_for_this_brand")
    put("AIC.alias.ko.off_alias", off[0][2], off[0][2], src + " aliases.ko.not_used_for_this_brand")
    lab = A["languages"]["zh"]["labels_flagged"]
    assert len(lab) == 1
    put("AIC.zh.label_flagged", lab[0], lab[0].replace("label__", ""), src + " languages.zh.labels_flagged")
    return A["recorded_spend_usd"]


def collection():
    raw = [json.loads(l) for l in _read("data/v62_raw.jsonl").splitlines() if l.strip()]
    src = "osf/v62/data/v62_raw.jsonl"
    put("raw.lines", len(raw), f"{len(raw):,}", src + " (lines)")
    ok = [r for r in raw if r["status"] == "ok"]
    err = [r for r in raw if r["status"] != "ok"]
    put("raw.ok", len(ok), f"{len(ok):,}", src + " status == ok")
    put("raw.errors", len(err), str(len(err)), src + " status != ok")
    assert len({r["call_id"] for r in ok}) == len(ok)
    expected = 1602
    put("design.expected", expected, f"{expected:,}", "pre-registration header and section 5.2 (adopted design)")
    assert len(ok) == expected
    per_lang = Counter(r["language"] for r in ok)
    per_model = Counter(r["model_requested"] for r in ok)
    assert len(set(per_lang.values())) == 1 and len(set(per_model.values())) == 1
    put("raw.per_lang", per_lang["es"], str(per_lang["es"]), src + " ok calls per language (equal for es, ko, zh)")
    put("raw.per_model", per_model[MODELS[0]], str(per_model[MODELS[0]]), src + " ok calls per model (equal for the three)")
    ph = Counter(r["phase"] for r in ok)
    put("raw.B", ph["B"], str(ph["B"]), src + " ok calls, phase B")
    put("raw.A", ph["A"], str(ph["A"]), src + " ok calls, phase A")
    assert len(err) == 1
    e = err[0]
    parts = e["call_id"].split("|")   # lang|substrate|phase|probe|model|cond|run
    put("err.call_id", e["call_id"], e["call_id"], src + " error line call_id")
    put("err.lang", parts[0], parts[0], src + " error line call_id")
    put("err.sub", parts[1], parts[1], src + " error line call_id")
    put("err.probe", e["probe_id"], e["probe_id"].replace("phase_b__", ""), src + " error line probe_id")
    put("err.model", e["model_requested"], e["model_requested"], src + " error line model_requested")
    put("err.run", e["run"], str(e["run"]), src + " error line run")
    put("err.kind", e["error"].split(":")[0], e["error"].split(":")[0], src + " error line error")
    put("err.cost", e["cost_usd"], usd(e["cost_usd"], 0), src + " error line cost_usd")
    put("err.usage_parts", len(e["usage_parts"]), str(len(e["usage_parts"])), src + " error line usage_parts (count)")
    t0 = datetime.fromisoformat(e["started_utc"]).astimezone(CT)
    put("err.time_ct", e["started_utc"], t0.strftime("%H:%M"), src + " error line started_utc, US Central")
    rr = [r for r in ok if r["call_id"] == e["call_id"]]
    assert len(rr) == 1
    put("err.rerun_cost", rr[0]["cost_usd"], usd(rr[0]["cost_usd"]), src + " re-run line cost_usd")
    first = min(r["started_utc"] for r in raw)
    last = max(r["finished_utc"] for r in raw if r.get("finished_utc"))
    f, l = datetime.fromisoformat(first), datetime.fromisoformat(last)
    put("win.first_ct", first, f.astimezone(CT).strftime("%H:%M"), src + " min started_utc, US Central")
    put("win.first_utc", first, f.strftime("%H:%M"), src + " min started_utc, UTC")
    put("win.last_ct", last, l.astimezone(CT).strftime("%H:%M"), src + " max finished_utc, US Central")
    put("win.span_h", (l - f).total_seconds() / 3600, f"{(l - f).total_seconds() / 3600:.1f}", src + " last - first, hours")
    total = round(sum(r["cost_usd"] for r in raw), 6)
    put("raw.cost_sum", total, usd(total), src + " sum of cost_usd over all lines")
    sys.path.insert(0, str(V62 / "scripts"))
    import budget_v0_62 as B   # noqa: E402
    INPUTS["osf/v62/scripts/budget_v0_62.py"] = hashlib.sha256((V62 / "scripts/budget_v0_62.py").read_bytes()).hexdigest()
    wc = B.worst_case(e["model_requested"], "S0", "standard", e["started_utc"])
    pin, pout = B.prices(e["model_requested"], "standard", e["started_utc"])
    put("cost.wc_price", [pin, pout], f"${pin:g} / ${pout:g}", "budget_v0_62.prices(gemini-4-argon, standard, error line date)")
    put("cost.worst_case", wc, usd(wc, 5), "budget_v0_62.worst_case(gemini-4-argon, S0, standard, error line "
        "started_utc): 2,000 input and 16,384 output tokens at that date's price (computed for the paper)")
    put("cost.strict_total", total + wc, usd(total + wc, 6), "raw.cost_sum + cost.worst_case (computed for the paper)")
    put("cost.strict_total2", total + wc, usd(total + wc, 2), "raw.cost_sum + cost.worst_case (computed for the paper)")
    return total


def logs(total, ai_spend):
    log = _read("data/collect_v0_62.log")
    src = "osf/v62/data/collect_v0_62.log"
    spends = re.findall(r"block (\d) \('([A-Za-z_]+)', 'S0', (\d)\): (\d+) calls to send; \{'actual_calls_usd': ([\d.]+)", log)
    assert [s[0] for s in spends] == ["1", "2", "3", "4"]
    for b, _, _, n, before in spends:
        put(f"log.block{b}.calls", int(n), n, src + f" 'block {b}' line")
        put(f"log.before_block{b}", float(before), usd(float(before)), src + f" 'block {b}' line, spent before it")
    m = re.search(r"result: done \{'actual_calls_usd': ([\d.]+)", log)
    put("log.main_spend", float(m.group(1)), usd(float(m.group(1))), src + " result line")
    m = re.search(r"collector exit 0 at CT (\S+ \S+)", log)
    put("log.main_end_ct", m.group(1), m.group(1)[11:16], src + " collector exit line")
    rr = _read("data/collect_v0_62_rerun.log")
    srr = "osf/v62/data/collect_v0_62_rerun.log"
    m = re.search(r"start CT (\S+ \S+)", rr)
    put("log.rerun_start_ct", m.group(1), m.group(1)[11:16], srr + " start line")
    m = re.search(r"collector exit 0 at CT (\S+ \S+)", rr)
    put("log.rerun_end_ct", m.group(1), m.group(1)[11:16], srr + " collector exit line")
    final = float(re.search(r"result: done \{'actual_calls_usd': ([\d.]+)", rr).group(1))
    put("cost.spend", final, usd(final), srr + " result line (recorded spend after the re-run pass)")
    assert abs(final - total) < 5e-4, (final, total)
    put("cost.with_check", final + ai_spend, usd(final + ai_spend), "cost.spend + AIC.spend (computed for the paper)")
    st = load("data/v62_budget_state.json")
    sst = "osf/v62/data/v62_budget_state.json"
    put("budget.window", st["window"], f"{st['window'][0]} to {st['window'][1]}", sst + " window")
    put("budget.window_entry", st["window_deviation_entry"], st["window_deviation_entry"], sst + " window_deviation_entry")
    ap = st["approvals"]["projection"]
    put("budget.rerun_note", ap["note"], ap["note"], sst + " approvals.projection.note")


def gates():
    G = load("data/gates/gate_P1real_P3_v0_62.json")
    src = "osf/v62/data/gates/gate_P1real_P3_v0_62.json"
    p1 = G["P1_real"]
    put("gate.P1.result", p1["result"], p1["result"], src + " P1_real.result")
    put("gate.P1.units", p1["units"], str(p1["units"]), src + " P1_real.units")
    put("gate.P1.mismatches", p1["mismatches"], str(p1["mismatches"]), src + " P1_real.mismatches")
    put("gate.P1.table_diffs", p1["vs_v42_brand_table"]["differences"], str(p1["vs_v42_brand_table"]["differences"]),
        src + " P1_real.vs_v42_brand_table.differences")
    p3 = G["P3"]
    put("gate.P3.result", p3["result"], p3["result"], src + " P3.result")
    put("gate.P3.checked", p3["prompts_checked"], f"{p3['prompts_checked']:,}", src + " P3.prompts_checked")
    put("gate.P3.mismatches", p3["prompt_mismatches"], str(p3["prompt_mismatches"]), src + " P3.prompt_mismatches")
    P2 = load("data/gates/gate_P2_v0_62.json")
    s2 = "osf/v62/data/gates/gate_P2_v0_62.json"
    put("gate.P2.result", P2["result"], P2["result"], s2 + " result")
    put("gate.P2.cells", P2["pre_vs_ref"]["cells"], f"{P2['pre_vs_ref']['cells']:,}", s2 + " pre_vs_ref.cells")
    put("gate.P2.diff", P2["pre_vs_ref"]["different"], str(P2["pre_vs_ref"]["different"]), s2 + " pre_vs_ref.different")
    ad = P2["apostrophe_delta_ref_vs_locked"]
    put("gate.P2.apos_diff", ad["different"], str(ad["different"]), s2 + " apostrophe_delta_ref_vs_locked.different")
    put("gate.P2.apos_only2", ad["only_in_second"], str(ad["only_in_second"]),
        s2 + " apostrophe_delta_ref_vs_locked.only_in_second")
    rows = list(csv.reader(_read("data/coded/v62_alias_audit.csv").splitlines()))
    put("alias.matches", len(rows) - 1, str(len(rows) - 1), "osf/v62/data/coded/v62_alias_audit.csv (rows after the header)")


MNAME = {"claude-fable-5-2": "Claude Fable 5.2", "gpt-6-astra": "GPT-6 Astra", "gemini-4-argon": "Gemini 4 Argon"}
LABELS = ["language-stable", "level-shifted", "intermediate", "language-sensitive"]


def f2(x):
    return f"{x:.2f}"


def planned(V):
    """DEVIATIONS Entry 7 (commit 69e1aa9): the pre-registered items the locked scorer did not compute."""
    S = load("data/v62_planned_items_summary_v0_62.json")
    I = load("data/v62_planned_items_v0_62.json")
    ss = "osf/v62/data/v62_planned_items_summary_v0_62.json"
    si = "osf/v62/data/v62_planned_items_v0_62.json"
    assert S["deviation_entry"] == 7 and I["deviation_entry"] == 7
    assert S["no_model_called"] and S["locked_verdicts_stand"] and not S["bears_on_a_verdict"]
    assert I["reproduced_locked_verdicts_byte_for_byte"]
    put("E7.entry", S["deviation_entry"], str(S["deviation_entry"]), ss + " deviation_entry")
    # 2.2 per-model rho_c, readings (i) and (ii)
    pm = []
    for L in LANGS:
        for m in MODELS:
            r = S["per_model_rho_c"][f"{L}|{m}"]
            full = I["2.2_per_model_rho_c"][f"{L}|{m}"]
            for rd, k in (("i", "i_same_model_english"), ("ii", "ii_n3_english")):
                assert full[k]["rho_c"] == r[k]
                put(f"E7.pm.{L}.{m}.{rd}", r[k], f3(r[k]), f"{ss} per_model_rho_c.{L}|{m}.{k}")
                pm.append(r[k])
            n = full["i_same_model_english"]["n"]
            assert n == full["ii_n3_english"]["n"] == V["n_units"]
    put("E7.pm.n", V["n_units"], str(V["n_units"]), si + " 2.2_per_model_rho_c.*.n (112 in every cell)")
    put("E7.pm.min", min(pm), f3(min(pm)), ss + " per_model_rho_c (minimum of 18)")
    put("E7.pm.max", max(pm), f3(max(pm)), ss + " per_model_rho_c (maximum of 18)")
    n70 = sum(x < 0.70 for x in pm)
    put("E7.pm.n_below70", n70, str(n70), ss + " per_model_rho_c (count < 0.70)")
    # 2.3 |rho_c(phi_L, pi_L)| flag
    mx = 0.0
    for L in LANGS:
        f = S["phi_pi_flag"][L]
        for part, k in (("def", "phi_L_defined"), ("hlp", "h_lang_phi_units")):
            assert f[k]["flag"] is False
            put(f"E7.phipi.{L}.{part}.abs", abs(f[k]["rho_c"]), f3(abs(f[k]["rho_c"])), f"{ss} phi_pi_flag.{L}.{k}.rho_c (absolute)")
            put(f"E7.phipi.{L}.{part}.rho", f[k]["rho_c"], f3(f[k]["rho_c"]), f"{ss} phi_pi_flag.{L}.{k}.rho_c")
            put(f"E7.phipi.{L}.{part}.n", f[k]["n"], str(f[k]["n"]), f"{ss} phi_pi_flag.{L}.{k}.n")
            mx = max(mx, abs(f[k]["rho_c"]))
    put("E7.phipi.max_abs", mx, f3(mx), ss + " phi_pi_flag (largest absolute value of six)")
    # 2.5 per-category labels (summary JSON and CSV must agree)
    rows = list(csv.DictReader(_read("data/v62_planned_category_labels_v0_62.csv").splitlines()))
    sc = "osf/v62/data/v62_planned_category_labels_v0_62.csv"
    assert len(rows) == 15
    cnt = Counter()
    for row in rows:
        L, c = row["language"], row["category"]
        d = S["category_labels"][f"{L}|{c}"]
        assert d["label"] == row["label"] and d["n_moved_gt_1_6"] == int(row["n_moved_gt_1_6"])
        assert abs(d["rho_c"] - float(row["rho_c"])) < 1e-9 and abs(d["delta_L"] - float(row["delta_L"])) < 1e-9
        s = f"{ss} category_labels.{L}|{c} (= {sc})"
        put(f"E7.cat.{L}.{c}.rho", d["rho_c"], f3(d["rho_c"]), s + ".rho_c")
        put(f"E7.cat.{L}.{c}.dL", d["delta_L"], sgn3(d["delta_L"]), s + ".delta_L")
        lo, hi = d["delta_L_ci95"]
        put(f"E7.cat.{L}.{c}.dL_ci", [lo, hi], f"{sgn3(lo)} to {sgn3(hi)}", s + ".delta_L_ci95")
        put(f"E7.cat.{L}.{c}.moved", d["n_moved_gt_1_6"], f"{d['n_moved_gt_1_6']} of {d['n']}", s + ".n_moved_gt_1_6 of n")
        put(f"E7.cat.{L}.{c}.label", d["label"], d["label"], s + ".label")
        cnt[d["label"]] += 1
    for lab in LABELS:
        put(f"E7.cat.n.{lab}", cnt[lab], str(cnt[lab]), f"{ss} category_labels (count of label {lab!r} of 15)")
    assert sum(cnt.values()) == 15 and set(cnt) <= set(LABELS)
    for pair, d in S["language_pairs"].items():
        s = f"{ss} language_pairs.{pair}"
        put(f"E7.pair.{pair}.rho", d["rho_c"], f3(d["rho_c"]), s + ".rho_c")
        put(f"E7.pair.{pair}.ci", d["ci95_rho_c"], f"{f3(d['ci95_rho_c'][0])}–{f3(d['ci95_rho_c'][1])}", s + ".ci95_rho_c")
        put(f"E7.pair.{pair}.p", d["p_perm"], pfmt(d["p_perm"]), s + ".p_perm")
        put(f"E7.pair.{pair}.n", d["n"], str(d["n"]), s + ".n")
    # 2.5 ten largest shifts (CSV and summary JSON must agree)
    top = list(csv.DictReader(_read("data/v62_planned_top10_shift_v0_62.csv").splitlines()))
    st = "osf/v62/data/v62_planned_top10_shift_v0_62.csv"
    for L in LANGS:
        rl = [r for r in top if r["language"] == L]
        assert [int(r["rank"]) for r in rl] == list(range(1, 11))
        for r, j in zip(rl, S["top10_shift"][L]):
            assert r["name"] == j[1] and abs(float(r["shift"]) - j[4]) < 1e-9
            i = int(r["rank"])
            put(f"E7.top.{L}.{i}.name", r["name"], r["name"], f"{st} language={L} rank={i} name")
            put(f"E7.top.{L}.{i}.shift", float(r["shift"]), sgn3(float(r["shift"])), f"{st} language={L} rank={i} shift")
        ties = I["2.5_top10_shift"][L]["units_tied_with_10th_not_listed"]
        put(f"E7.top.{L}.ties", ties, str(ties), f"{si} 2.5_top10_shift.{L}.units_tied_with_10th_not_listed")
    # 2.7 time benchmark
    tb = I["2.7_benchmark_for_time"]
    put("E7.time.status", tb["status"], tb["status"], si + " 2.7_benchmark_for_time.status")
    # 2.8 manipulation checks
    M = I["2.8_manipulation_checks"]
    sm = si + " 2.8_manipulation_checks"
    c = M["MC_Complete"]
    put("E7.mc.complete.answered", c["answered"], f"{c['answered']:,}", sm + ".MC_Complete.answered")
    put("E7.mc.complete.sent", c["calls_sent"], f"{c['calls_sent']:,}", sm + ".MC_Complete.calls_sent")
    put("E7.mc.complete.lines", c["attempt_lines"], f"{c['attempt_lines']:,}", sm + ".MC_Complete.attempt_lines")
    put("E7.mc.complete.share", c["share"], f"{100 * c['share']:.0f}%", sm + ".MC_Complete.share")
    c = M["MC_Served"]
    put("E7.mc.served.checked", c["answered_calls_checked"], f"{c['answered_calls_checked']:,}", sm + ".MC_Served.answered_calls_checked")
    put("E7.mc.served.mismatched", c["n_mismatched"], str(c["n_mismatched"]), sm + ".MC_Served.n_mismatched")
    put("E7.mc.served.pass", c["pass"], "PASS" if c["pass"] else "FAIL", sm + ".MC_Served.pass")
    chk = list(csv.DictReader(_read("data/v62_planned_checks_v0_62.csv").splitlines()))
    sk = "osf/v62/data/v62_planned_checks_v0_62.csv"
    lang = M["MC_Language"]["per_model_language"]
    for row in chk:
        if row["check"] != "MC_Language":
            continue
        L, m, ph = row["cell"].split("|")
        d = lang[row["cell"]]
        assert d["answers"] == int(row["n"]) and d["in_language"] == int(row["count"])
        assert d["flag_below_95pct"] == (row["flag"] == "True")
        s = f"{sk} MC_Language {row['cell']} (= {sm}.MC_Language.per_model_language)"
        put(f"E7.mc.lang.{L}.{m}.{ph}", d["share"], f4(d["share"]), s + " share")
        put(f"E7.mc.lang.{L}.{m}.{ph}.count", d["in_language"], f"{d['in_language']} of {d['answers']}", s + " count of n")
        put(f"E7.mc.lang.{L}.{m}.{ph}.flag", d["flag_below_95pct"], "flagged" if d["flag_below_95pct"] else "not flagged",
            s + " flag (below 95%)")
    fl_all = sorted(k for k, d in lang.items() if k.endswith("|all") and d["flag_below_95pct"])
    assert fl_all == sorted(M["MC_Language"]["flagged_all_answers"])
    assert not M["MC_Language"]["flagged_phase_B"]
    put("E7.mc.lang.n_flagged_all", len(fl_all), str(len(fl_all)), sm + ".MC_Language.flagged_all_answers (count)")
    put("E7.mc.lang.flagged_all_langs", sorted({k.split("|")[0] for k in fl_all}),
        ", ".join(sorted({k.split("|")[0].upper() for k in fl_all})), sm + ".MC_Language.flagged_all_answers (languages)")
    fl_a = sorted(k for k, d in lang.items() if k.endswith("|A") and d["flag_below_95pct"])
    put("E7.mc.lang.n_flagged_A", len(fl_a), str(len(fl_a)), sm + ".MC_Language.per_model_language (Phase A cells flagged)")
    put("E7.mc.lang.n_flagged_B", 0, "0", sm + ".MC_Language.flagged_phase_B (count)")
    off = lang["zh|claude-fable-5-2|B"]["off_language_call_ids"]
    probes = sorted({x.split("|")[3] for x in off})
    assert len(probes) == 1
    put("E7.mc.lang.zh_off_probe", probes[0], probes[0], sm + ".MC_Language.per_model_language.zh|claude-fable-5-2|B.off_language_call_ids")
    put("E7.mc.lang.zh_off_n", len(off), str(len(off)), sm + ".MC_Language.per_model_language.zh|claude-fable-5-2|B.off_language_call_ids (count)")
    sc_ = M["MC_Script"]["per_model"]
    nscript = sum(sc_[f"zh|{m}|all"]["with_traditional_only_characters"] for m in MODELS)
    assert not M["MC_Script"]["flagged_all_answers"]
    put("E7.mc.script.n", nscript, str(nscript), sm + ".MC_Script.per_model.zh|*|all.with_traditional_only_characters (sum)")
    a = M["MC_Alias"]
    put("E7.mc.alias.matches", a["matches_exported"], str(a["matches_exported"]), sm + ".MC_Alias.matches_exported")
    put("E7.mc.alias.calls", a["calls_with_a_match"], str(a["calls_with_a_match"]), sm + ".MC_Alias.calls_with_a_match")
    assert a["matches_exported"] == V_alias_matches()
    for L in ("ko", "zh"):
        parts = [x for x in a["by_language_alias_unit"] if x["language"] == L]
        put(f"E7.mc.alias.{L}", [[x["unit"], x["matches"]] for x in parts],
            ", ".join(f"{x['unit']} {x['matches']}" for x in parts), sm + f".MC_Alias.by_language_alias_unit (language {L})")
    t = M["MC_Truncation"]
    ncap = sum(d["at_cap"] for d in t["per_model_language"].values())
    assert not t["flagged"]
    put("E7.mc.trunc.n", ncap, str(ncap), sm + ".MC_Truncation.per_model_language.*.at_cap (sum)")
    fr = sorted(k.replace("FinishReason.", "") for k in t["finish_reasons"])
    put("E7.mc.trunc.reasons", fr, ", ".join(fr), sm + ".MC_Truncation.finish_reasons (keys)")
    w = M["MC_Window"]
    put("E7.mc.window.h", w["span_hours"], f"{w['span_hours']:.2f}", sm + ".MC_Window.span_hours")
    b = M["MC_Budget"]
    put("E7.mc.budget.spend", b["spend_from_recorded_usage_usd"], usd(b["spend_from_recorded_usage_usd"], 6),
        sm + ".MC_Budget.spend_from_recorded_usage_usd")
    put("E7.mc.budget.not_sent", b["calls_not_sent"], str(b["calls_not_sent"]), sm + ".MC_Budget.calls_not_sent")
    # 7.5 S-Language, S-Script, S-Alias (Presence)
    sens = I["7.5_sensitivities"]
    for k, d in sens.items():
        name, L = k.rsplit("_", 1)
        assert d["verdict"] == d["primary_verdict"] == V["tests"][f"H_Lang_Presence_{L}"]["verdict"]
        assert d["rho_c"] == S["sensitivities"][k]["rho_c"]
        put_test(f"E7.{name}.{L}", d, f"{si} 7.5_sensitivities.{k}")
        if "excluded_calls" in d:
            put(f"E7.{name}.{L}.excluded", len(d["excluded_calls"]), str(len(d["excluded_calls"])),
                f"{si} 7.5_sensitivities.{k}.excluded_calls (count)")
        if "cells_differing_from_primary" in d:
            put(f"E7.{name}.{L}.cells", d["cells_differing_from_primary"], str(d["cells_differing_from_primary"]),
                f"{si} 7.5_sensitivities.{k}.cells_differing_from_primary")
    assert sens["S-Language_zh"]["excluded_calls"] == off
    # 2.9 descriptives
    D = I["2.9_descriptives"]
    sd = si + " 2.9_descriptives"
    for key, d in D["1_run_reliability"].items():
        L, m = key.split("|")
        for r in ("rel1", "rel3"):
            put(f"E7.rel.{L}.{m}.{r}", d[r], f3(d[r]), f"{sd}.1_run_reliability.{key}.{r}")
        if L == "en":
            assert d["transcription_equals_t4_locked"]
    rec = D["2_recognition"]
    for L, k in (("en", "en_t4_same_88_units"), ("es", "es"), ("ko", "ko"), ("zh", "zh")):
        for m in MODELS:
            r = rec[k][m]
            assert r["coded_answers"] == r["rows"] == 88
            put(f"E7.rec.{L}.{m}", r["recognized"], str(r["recognized"]), f"{sd}.2_recognition.{k}.{m}.recognized (of 88 coded)")
    rr_ = [rec[L][m]["recognized"] for L in LANGS for m in MODELS]
    put("E7.rec.min", min(rr_), str(min(rr_)), f"{sd}.2_recognition.{{es,ko,zh}}.*.recognized (minimum of 9)")
    put("E7.rec.max", max(rr_), str(max(rr_)), f"{sd}.2_recognition.{{es,ko,zh}}.*.recognized (maximum of 9)")
    lf = D["3_measured_language_factor"]
    pl0 = D["3_planning_language_factors_section_6_2"]["central"]
    below = all(lf[f"{L}|pooled|{ph}"]["cost_factor"] < pl0[L] for L in LANGS for ph in ("A", "B"))
    put("E7.lf.pooled_below_plan", below, "yes" if below else "no",
        f"{sd}.3_measured_language_factor.*|pooled|* < 3_planning_language_factors_section_6_2.central (all six)")
    for L in LANGS:
        for m in MODELS + ["pooled"]:
            for ph in ("B", "A"):
                x = lf[f"{L}|{m}|{ph}"]["cost_factor"]
                put(f"E7.lf.{L}.{m}.{ph}", x, f2(x), f"{sd}.3_measured_language_factor.{L}|{m}|{ph}.cost_factor")
        pl = D["3_planning_language_factors_section_6_2"]
        put(f"E7.lf.{L}.plan", pl["central"][L], f2(pl["central"][L]),
            f"{sd}.3_planning_language_factors_section_6_2.central.{L}")
        put(f"E7.lf.{L}.plan_high", pl["conservative_high"][L], f2(pl["conservative_high"][L]),
            f"{sd}.3_planning_language_factors_section_6_2.conservative_high.{L}")
    af = D["3_answer_form"]
    nref = 0
    for L in ["en"] + LANGS:
        for m in MODELS:
            for ph in ("B", "A"):
                nref += af[f"{L}|{m}|{ph}"]["refusals_by_finish_reason"]
            d = af[f"{L}|{m}|B"]
            s = f"{sd}.3_answer_form.{L}|{m}|B"
            put(f"E7.form.{L}.{m}.chars", d["characters_per_answer_mean"], f"{d['characters_per_answer_mean']:,.0f}",
                s + ".characters_per_answer_mean")
            put(f"E7.form.{L}.{m}.brands", d["registry_brands_named_per_phase_B_answer"],
                f"{d['registry_brands_named_per_phase_B_answer']:.1f}", s + ".registry_brands_named_per_phase_B_answer")
    put("E7.form.refusals", nref, str(nref), sd + ".3_answer_form.*.refusals_by_finish_reason (sum)")
    for L in ("ko", "zh"):
        d = D["4_script_of_mentions"][L]["all_models"]
        s = f"{sd}.4_script_of_mentions.{L}.all_models"
        for k in ("mentions", "latin_only", "native_only", "both"):
            put(f"E7.script.{L}.{k}", d[k], f"{d[k]:,}", f"{s}.{k}")
        for k in ("share_with_latin_form", "share_with_native_form", "share_native_only"):
            put(f"E7.script.{L}.{k}", d[k], f"{100 * d[k]:.1f}%", f"{s}.{k}")
    h = D["5_home_language"]
    put("E7.home.status", h["status"], h["status"], sd + ".5_home_language.status")
    cost = D["6_cost"]
    for L in LANGS:
        for m in MODELS:
            x = cost[f"{L}|{m}"]["usd"]
            put(f"E7.cost.{L}.{m}", x, usd(x), f"{sd}.6_cost.{L}|{m}.usd")
    put("E7.cost.total", cost["total_usd"], usd(cost["total_usd"]), sd + ".6_cost.total_usd")
    assert abs(cost["total_usd"] - VALS["raw.cost_sum"]["value"]) < 1e-6


def V_alias_matches():
    return VALS["alias.matches"]["value"]


def deviations():
    """The deviations record itself: the entries it holds and the Entry 8 statements the paper repeats."""
    txt = _read("DEVIATIONS.md")
    src = "osf/v62/DEVIATIONS.md"
    entries = [int(x) for x in re.findall(r"^## Entry (\d+) ", txt, re.M)]
    assert entries == list(range(len(entries)))
    put("dev.n_entries", len(entries), str(len(entries)), src + " ('## Entry N' headings)")
    put("dev.last", entries[-1], str(entries[-1]), src + " ('## Entry N' headings, last)")
    e8 = txt[txt.index("## Entry 8 "):]
    assert "$0.16784" in e8 and "$28.297192" in e8 and "$28.129352" in e8
    assert "would not have paused without the approval" in e8


def entry8(total):
    """Entry 8 figures recomputed from the raw file, the re-run log and the locked budget module."""
    raw = [json.loads(l) for l in (V62 / "data/v62_raw.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    src = "osf/v62/data/v62_raw.jsonl"
    import budget_v0_62 as B   # noqa: E402  (path set by collection())
    put("raw.cost_sum6", total, usd(total, 6), src + " sum of cost_usd over all lines")
    rr = [r for r in raw if r["call_id"] == VALS["err.call_id"]["value"] and r["status"] == "ok"][0]
    main = round(total - rr["cost_usd"], 6)
    put("cost.main_recorded", main, usd(main, 6), "raw.cost_sum - re-run line cost_usd (computed for the paper)")
    wc = VALS["cost.worst_case"]["value"]
    put("cost.main_strict", main + wc, usd(main + wc, 6), "cost.main_recorded + cost.worst_case (computed for the paper)")
    put("cost.strict_total4", total + wc, usd(total + wc, 4), "raw.cost_sum + cost.worst_case (computed for the paper)")
    ax = [r for r in raw if r["status"] == "ok" and r["attempts"] > 1
          and any(p.get("worst_case") for p in r["usage_parts"])]
    assert len(ax) == 1
    a = ax[0]
    wa = B.worst_case(a["model_requested"], "S0", "standard", a["started_utc"])
    put("cost.astra_call", a["call_id"], a["call_id"], src + " the one answered line with a worst-case usage part")
    put("cost.astra_wc", wa, usd(wa, 4), "budget_v0_62.worst_case(gpt-6-astra, S0, standard, that line's started_utc) "
        "(computed for the paper)")
    st = load("data/v62_budget_state.json")
    ap = st["approvals"]["projection"]
    given = re.search(r"(\d{1,2}:\d{2} [ap]m) CT", ap["note"]).group(1)
    put("budget.rerun_note_given", given, given, "osf/v62/data/v62_budget_state.json approvals.projection.note (time given)")
    t = datetime.fromisoformat(ap["utc"]).astimezone(CT)
    put("budget.rerun_note_time_ct", ap["utc"], t.strftime("%H:%M:%S"), "osf/v62/data/v62_budget_state.json "
        "approvals.projection.utc, US Central")
    rl = (V62 / "data/collect_v0_62_rerun.log").read_text(encoding="utf-8")
    s1 = re.search(r"start CT \S+ (\S+)", rl).group(1)
    s2 = re.search(r"collector exit 0 at CT \S+ (\S+)", rl).group(1)
    put("log.rerun_start_s", s1, s1, "osf/v62/data/collect_v0_62_rerun.log start line")
    put("log.rerun_end_s", s2, s2, "osf/v62/data/collect_v0_62_rerun.log collector exit line")


def build():
    V = verdicts()
    coi106(V)
    ai_sens(V)
    en_corrected(V)
    ai_spend = ai_check()
    total = collection()
    logs(total, ai_spend)
    gates()
    planned(V)
    deviations()
    entry8(total)


def main():
    build()
    meta = {"written_by": "papers/v0_62/values_v0_62.py", "inputs_sha256": INPUTS, "n_values": len(VALS)}
    OUT_JSON.write_text(json.dumps({"_meta": meta, "values": VALS}, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT_JSON.relative_to(ROOT)}: {len(VALS)} values from {len(INPUTS)} files")


if __name__ == "__main__":
    main()
