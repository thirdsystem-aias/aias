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


def main():
    V = verdicts()
    coi106(V)
    ai_sens(V)
    en_corrected(V)
    ai_spend = ai_check()
    total = collection()
    logs(total, ai_spend)
    gates()
    meta = {"written_by": "papers/v0_62/values_v0_62.py", "inputs_sha256": INPUTS, "n_values": len(VALS)}
    OUT_JSON.write_text(json.dumps({"_meta": meta, "values": VALS}, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT_JSON.relative_to(ROOT)}: {len(VALS)} values from {len(INPUTS)} files")


if __name__ == "__main__":
    main()
