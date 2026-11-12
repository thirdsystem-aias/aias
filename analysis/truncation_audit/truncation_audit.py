#!/usr/bin/env python3
"""
truncation_audit.py -- read-only audit of model answers that ended on the output-token limit.

Branch truncation-audit (cut from v0.41, the branch that holds osf/v41). It reads files and git
objects only, writes only under analysis/truncation_audit/results/, and calls no model API.

Part 1  The Consistency panel's archive (the AIAS 2.0 inputs): substrates v0.19-v0.23, waves
        t1 (osf/v19..v23), t2 (osf/v34/data), t3 (osf/v41/data), six models, the six Phase B
        (open category) answers per model. Per answer: did it end on the output-token limit, and if
        so, before naming any brand of the substrate's registry?
        Brand matching is the scorer's own (score_v41.load_wave lineage), not a new matcher:
          v0.19        osf/v19/acquire_v0_19.py build_brand_patterns + detect_mentions_in_response
          v0.20-v0.22  score_v33.RECON_CFG content module .detect_mention
          v0.23        brand_mentions of v23_phase_b_scored.json (score_v0_23.find_brand_mentions)
        Every per-answer brand count is reconciled to score_v41.load_wave's counts (k_per_model)
        and to the published osf/v41/v41_three_wave_table.csv; any mismatch stops the script.
        Truncation evidence, in this order:
          finish_reason   t3 only (osf/v41/data/v41_provenance.csv, matched call by call),
                          tested with score_v41's own TRUNC_REASONS rule
          tokens_at_cap   output tokens >= the runner's cap, for models without hidden thinking
                          tokens (v0.19 records tokens_out in all waves)
          identical_to_t3 text byte-identical to the t3 answer of the same model and question,
                          for models without hidden thinking tokens (same text, same token count)
          not_recorded    none of the above
Part 2  Newer collections with model answers (v0.38, v0.39, v0.42 = t4, current arm with search
        off and on), coding and judge calls, and the studies with nothing collected yet.

Usage:  ~/aias/venv/bin/python3 analysis/truncation_audit/truncation_audit.py
"""
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True                 # read-only: no __pycache__ next to locked modules
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"    # (also for score_v41's re-executed interpreter)
HERE = Path(__file__).resolve().parent
TREE = HERE.parents[1]
os.environ.setdefault("AIAS_ROOT", str(TREE))
sys.path.insert(0, str(TREE / "osf" / "v41" / "scripts"))
import score_v41 as S  # noqa: E402  (re-executes this script with a HOME shim: ~/aias -> TREE)

import collections      # noqa: E402
import csv              # noqa: E402
import hashlib          # noqa: E402
import importlib.util   # noqa: E402
import json             # noqa: E402
import statistics       # noqa: E402
import subprocess       # noqa: E402
from datetime import datetime, timezone  # noqa: E402

import score_v0_31 as S31   # noqa: E402
import score_v33 as S33     # noqa: E402
import score_v0_23 as SC23  # noqa: E402

ROOT = S.ROOT
assert ROOT.resolve() == TREE.resolve(), (ROOT, TREE)
OUT = HERE / "results"
PANEL = S31.PANEL
FLASH = "gemini-2.5-flash"
WAVES = ("t1", "t2", "t3")
LAY = {"t1": S.LAYOUT["t1"], "t2": S.LAYOUT["t2"], "t3": S._layout(S.DATA3, S.DATA3 / "v23")}
WAVE_DIR = {"t1": "osf/v19..v23 (osf/v23/data)", "t2": "osf/v34/data", "t3": "osf/v41/data"}
SIDECAR3 = S.DATA3 / "v41_provenance.csv"
PROVIDER = {"claude-opus-4-5": "anthropic", "claude-sonnet-4-5": "anthropic", "gpt-4o": "openai",
            "gpt-4o-mini": "openai", "gemini-2.5-flash": "google", "gemini-2.5-flash-lite": "google"}
SUBS = S.OMNI


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, str(path))
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


A19 = load_module(ROOT / "osf/v19/acquire_v0_19.py", "acq19_audit")
REG19 = A19.load_registry()
PAT19 = A19.build_brand_patterns(REG19)
NAME23 = {b["id"]: b["brand"] for b in SC23.REGISTRY}


def is_trunc(fr):
    """score_v41.mc_truncation's test: TRUNC_REASONS, also after an enum prefix ('FinishReason.')."""
    fr = (fr or "").strip()
    return bool(fr) and (fr in S.TRUNC_REASONS or fr.split(".")[-1] in S.TRUNC_REASONS)


def git(*args, text=True):
    return subprocess.run(["git", "-C", str(TREE), *args], capture_output=True, check=True, text=text).stdout


def git_show(rev, path):
    return git("show", f"{rev}:{path}", text=False)


def blob(rev, path):
    r = subprocess.run(["git", "-C", str(TREE), "rev-parse", "-q", "--verify", f"{rev}:{path}"],
                       capture_output=True, text=True)
    return r.stdout.strip() or None


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha256_file(p):
    return sha256_bytes(Path(p).read_bytes())


def ts(s):
    return datetime.fromisoformat(s)


def med(xs):
    return statistics.median(xs) if xs else None


# ============================================================================================
# Output-token caps of the omnibus runners (the t1 runners, run verbatim at t2 and t3)
# ============================================================================================
_B2048 = 'pool.submit(call_llm, t["model"], t["frame_text"], 2048)'
_GNOCAP = "resp = model.generate_content(prompt)"
# substrate: (runner file, Phase B cap per provider; None = the runner sends no limit, the code
#             strings that set it; each must occur in the file)
CAPS = {
    "v0.19": ("protocol/providers.py", {"anthropic": 1024, "openai": 1024, "google": 1024},
              ["max_tokens=1024", 'generation_config={"max_output_tokens": 1024}']),
    "v0.20": ("scripts/run_acquisition_v20.py", {"anthropic": 2048, "openai": 2048, "google": None},
              [_B2048, _GNOCAP]),
    "v0.21": ("scripts/run_acquisition_v21.py", {"anthropic": 2048, "openai": 2048, "google": None},
              [_B2048, _GNOCAP]),
    "v0.22": ("scripts/run_acquisition_v22.py", {"anthropic": 2048, "openai": 2048, "google": None},
              [_B2048, _GNOCAP]),
    "v0.23": ("scripts/acquire_v0_23.py", {"anthropic": 2048, "openai": 2048, "google": 2048},
              ["max_tokens=2048", "max_output_tokens=2048"]),
}
RUNNER_REVS = ["v0.19-acquired", "v0.20-acquisition-locked", "v0.22-acquisition-locked",
               "v0.23-scoring-locked", "v0.34-prereg-r1", "v0.41-acquisition-locked", "HEAD"]


def cap_of(sub, model):
    return CAPS[sub][1][PROVIDER[model]]


def check_runners():
    out = {}
    for sub, (rel, caps, needles) in CAPS.items():
        text = (ROOT / rel).read_text()
        missing = [n for n in needles if n not in text]
        if missing:
            raise SystemExit(f"cap check failed: {rel} lacks {missing}")
        blobs = {rev: blob(rev, rel) for rev in RUNNER_REVS}
        t2t3 = {blobs["v0.34-prereg-r1"], blobs["v0.41-acquisition-locked"], blobs["HEAD"]}
        out[sub] = {"runner": rel, "phase_b_cap_by_provider": caps, "code_strings": needles,
                    "git_blob_by_rev": blobs, "same_blob_t2_t3_head": len(t2t3) == 1,
                    "first_commit": git("log", "--diff-filter=A", "--format=%h %cs", "--", rel).strip()}
    # v0.19's runner calls protocol/providers.py through osf/v19/run_v0_19.py
    out["v0.19"]["also"] = {"osf/v19/run_v0_19.py": {rev: blob(rev, "osf/v19/run_v0_19.py") for rev in RUNNER_REVS}}
    out["probe_and_runner_sha256_vs_manifest (score_v41.gate_p4)"] = S.gate_p4()
    return out


# ============================================================================================
# Part 1 -- per-answer extraction (Phase B)
# ============================================================================================
def raw_brand_list(sub):
    """Brand names and the matcher exactly as score_v0_31.counts_raw_text builds them."""
    rk, rp, mod, _ = S33.RECON_CFG[sub]
    reg = mod.load_registry(rp) if rk == "json" else mod.load_prereg_module(rp)
    brands = [(b.get("name") if isinstance(b, dict) else b)
              for ck, cv in reg["cells"].items()
              for b in (cv.get("brands", []) if isinstance(cv, dict) else cv)]
    return brands, mod.detect_mention


def answers_v19(wave):
    base = LAY[wave]["base"] / "v19"
    rows = [json.loads(l) for l in open(base / "phase_b_responses.jsonl") if l.strip()]
    csv_named = collections.defaultdict(set)
    for r in S31.read_csv(base / "phase_b_results.csv"):
        if str(r["mentioned"]).strip() == "1":
            csv_named[(r["panel_model"], r["frame"])].add(r["brand"])
    out = []
    for i, r in enumerate(rows):
        text = r.get("response") or ""
        named = [m["brand"] for m in A19.detect_mentions_in_response(text, PAT19)]
        if set(named) != csv_named.get((r["panel_model"], r["frame"]), set()):
            raise SystemExit(f"v0.19 {wave} {r['panel_model']} {r['frame']}: matcher {named} != "
                             f"phase_b_results.csv {sorted(csv_named.get((r['panel_model'], r['frame']), set()))}")
        out.append({"substrate": "v0.19", "wave": wave, "model": r["panel_model"], "question": r["frame"],
                    "text": text, "named": named, "tokens_out": int(r["tokens_out"]) if r.get("tokens_out") not in (None, "") else None,
                    "order": i, "ts": None, "ts_start": None, "ts_end": None,
                    "matched_by": "acquire_v0_19.detect_mentions_in_response (= phase_b_results.csv mentioned)"})
    return out


def answers_raw(sub, wave):
    brands, detect = raw_brand_list(sub)
    out = []
    for i, r in enumerate(S31.read_csv(LAY[wave]["base"] / S.SUBDIR[sub] / "phase_b_results.csv")):
        text = r["response_text"]
        out.append({"substrate": sub, "wave": wave, "model": r["model"], "question": r["frame_id"],
                    "text": text, "named": [b for b in brands if detect(text, b)], "tokens_out": None,
                    "order": i, "ts": r.get("timestamp"), "ts_start": None, "ts_end": None,
                    "matched_by": f"score_v33.RECON_CFG['{sub}'] detect_mention"})
    return out


def answers_v23(wave):
    out = []
    for i, r in enumerate(json.load(open(LAY[wave]["v23"] / "v23_phase_b_scored.json"))):
        text = r.get("response") or ""
        named = [bid for bid, v in (r.get("brand_mentions") or {}).items() if v]
        if r.get("status") == "ok" and sorted(SC23.find_brand_mentions(text)) != sorted(named):
            raise SystemExit(f"v0.23 {wave} {r.get('model_id')} {r.get('probe_id')}: find_brand_mentions != brand_mentions")
        out.append({"substrate": "v0.23", "wave": wave, "model": r.get("model_id"), "question": r.get("probe_id"),
                    "text": text, "named": named, "tokens_out": None, "order": i, "ts": None,
                    "ts_start": r.get("ts_start"), "ts_end": r.get("ts_end"),
                    "matched_by": "v23_phase_b_scored.json brand_mentions (= score_v0_23.find_brand_mentions)"})
    return out


def all_answers():
    out = []
    for wave in WAVES:
        out += answers_v19(wave)
        for sub in ("v0.20", "v0.21", "v0.22"):
            out += answers_raw(sub, wave)
        out += answers_v23(wave)
    return [a for a in out if a["model"] in PANEL]


def phase_a_t3_records():
    """t3 Phase A answers (for the truncation count only): substrate, model, order/time keys."""
    out = []
    base = S.DATA3
    for i, r in enumerate(json.loads(l) for l in open(base / "v19/phase_a_responses.jsonl") if l.strip()):
        out.append({"substrate": "v0.19", "wave": "t3", "model": r["panel_model"], "question": r.get("brand"),
                    "order": i, "ts": None, "ts_start": None, "ts_end": None,
                    "tokens_out": int(r["tokens_out"]) if r.get("tokens_out") not in (None, "") else None,
                    "text": r.get("response") or ""})
    for sub in ("v0.20", "v0.21", "v0.22"):
        for i, r in enumerate(S31.read_csv(base / S.SUBDIR[sub] / "phase_a_results.csv")):
            out.append({"substrate": sub, "wave": "t3", "model": r["model"], "question": r.get("brand"),
                        "order": i, "ts": r.get("timestamp"), "ts_start": None, "ts_end": None,
                        "tokens_out": None, "text": r.get("response_text") or ""})
    for i, r in enumerate(json.load(open(base / "v23/v23_phase_a_raw.json"))):
        out.append({"substrate": "v0.23", "wave": "t3", "model": r.get("model_id"), "question": r.get("brand_id"),
                    "order": i, "ts": None, "ts_start": r.get("ts_start"), "ts_end": r.get("ts_end"),
                    "tokens_out": None, "text": r.get("response") or ""})
    return [a for a in out if a["model"] in PANEL]


# ============================================================================================
# Part 1 -- truncation evidence
# ============================================================================================
def attach_t3(answers, side, phase):
    """Attach to every t3 answer its own sidecar row (finish reason, output and thinking tokens)."""
    by = collections.defaultdict(list)
    for r in side:
        by[(r["substrate"], r["phase"])].append(r)
    report = {}
    for sub in SUBS:
        rows = by[(S.SUBDIR[sub], phase)]
        ans = sorted((a for a in answers if a["substrate"] == sub and a["wave"] == "t3"), key=lambda a: a["order"])
        if sub == "v0.19":
            if len(rows) != len(ans):
                raise SystemExit(f"t3 {sub} {phase}: {len(rows)} sidecar rows for {len(ans)} answers")
            for a, r in zip(ans, rows):
                if S._norm_alias(r["alias"]) != a["model"] or str(r["output_tokens"]) != str(a["tokens_out"]):
                    raise SystemExit(f"t3 {sub} {phase}: call order does not line up at {a['model']} {a['question']}")
                a["side"] = r
            report[sub] = {"method": "call order of the sequential v0.19 runner; alias and output tokens equal "
                                     "for every pair", "answers": len(ans), "sidecar_rows": len(rows)}
        elif sub == "v0.23":
            for a in ans:
                lo, hi = ts(a["ts_start"]), ts(a["ts_end"])
                c = [r for r in rows if S._norm_alias(r["alias"]) == a["model"] and lo <= ts(r["timestamp"]) <= hi]
                if len(c) != 1:
                    raise SystemExit(f"t3 {sub} {phase}: {len(c)} sidecar rows inside {a['model']} {a['question']}")
                a["side"] = c[0]
            report[sub] = {"method": "the one sidecar row of the same model stamped inside the answer's "
                                     "[ts_start, ts_end]", "answers": len(ans), "sidecar_rows": len(rows),
                           "sidecar_rows_not_matched": len(rows) - len(ans)}
        else:
            used, worst = set(), 0.0
            for a in ans:
                t = ts(a["ts"])
                c = sorted((abs((ts(r["timestamp"]) - t).total_seconds()), j) for j, r in enumerate(rows)
                           if j not in used and S._norm_alias(r["alias"]) == a["model"])
                d, j = c[0]
                used.add(j)
                worst = max(worst, d)
                a["side"] = rows[j]
            if worst > 1.0 or len(used) != len(rows):
                raise SystemExit(f"t3 {sub} {phase}: time match failed (worst {worst} s, {len(used)}/{len(rows)})")
            report[sub] = {"method": "nearest sidecar time stamp of the same model, one to one",
                           "answers": len(ans), "sidecar_rows": len(rows), "max_abs_dt_s": round(worst, 4)}
    return report


def thinking_models(side):
    """Models for which the sidecar records thinking tokens (they count against the output cap)."""
    return sorted({S._norm_alias(r["alias"]) for r in side if (r.get("thinking_tokens") or "").strip() not in ("", "0")})


def decide(a, t3_index, thinking):
    """(truncated True/False/None, evidence)."""
    m, cap, s = a["model"], a["cap"], a.get("side")
    if s is not None:
        return is_trunc(s["finish_reason"]), "finish_reason"
    if m not in thinking and cap is not None and a["tokens_out"] is not None:
        return a["tokens_out"] >= cap, "tokens_at_cap"
    if m not in thinking:
        t3 = t3_index.get((a["substrate"], m, a["question"]))
        if t3 is not None and t3["truncated"] is not None and t3["text"] == a["text"]:
            return t3["truncated"], "identical_to_t3"
    return None, "not_recorded"


def classify(answers, thinking):
    for a in answers:
        a["cap"] = cap_of(a["substrate"], a["model"])
        a["n_named"] = len(a["named"])
        s = a.get("side") or {}
        a["finish_reason"] = s.get("finish_reason")
        a["out_tokens"] = int(s["output_tokens"]) if (s.get("output_tokens") or "").strip() else a["tokens_out"]
        a["thinking_tokens"] = int(s["thinking_tokens"]) if (s.get("thinking_tokens") or "").strip() else None
    t3_index = {}
    for a in answers:
        if a["wave"] == "t3":
            a["truncated"], a["evidence"] = decide(a, {}, thinking)
            t3_index[(a["substrate"], a["model"], a["question"])] = a
    for a in answers:
        if a["wave"] != "t3":
            a["truncated"], a["evidence"] = decide(a, t3_index, thinking)
        a["cut_before_first_brand"] = bool(a["truncated"]) and a["n_named"] == 0
    # did another model name a registry brand on the same question in the same wave?
    best = collections.defaultdict(dict)
    for a in answers:
        best[(a["substrate"], a["wave"], a["question"])][a["model"]] = a["n_named"]
    for a in answers:
        a["others_named"] = any(n > 0 for m, n in best[(a["substrate"], a["wave"], a["question"])].items()
                                if m != a["model"])


def token_rule_check(answers, thinking):
    """Where both exist (t3, v0.19): does 'output tokens >= cap' agree with the finish reason?"""
    agree = disagree = 0
    rows = []
    for a in answers:
        if a["wave"] == "t3" and a["substrate"] == "v0.19" and a["model"] not in thinking and a["tokens_out"] is not None:
            by_tokens = a["tokens_out"] >= a["cap"]
            ok = by_tokens == is_trunc(a["finish_reason"])
            agree += ok
            disagree += not ok
            if not ok:
                rows.append([a["model"], a["question"], a["tokens_out"], a["finish_reason"]])
    return {"answers": agree + disagree, "agree": agree, "disagree": disagree, "disagreements": rows}


# ============================================================================================
# Part 1 -- reconciliation with the scorer, the table, and the touched brands
# ============================================================================================
def reconcile(answers):
    """Answers naming each brand, per (substrate, wave, brand, model), must equal score_v41.load_wave's
    count and the published osf/v41/v41_three_wave_table.csv k_per_model."""
    waves = {w: S.load_wave(LAY[w]) for w in WAVES}
    mine = collections.Counter((a["substrate"], a["wave"], b, a["model"]) for a in answers for b in a["named"])
    k, checked, mism = {}, 0, []
    for w, wave in waves.items():
        for sub in SUBS:
            for b, vec in wave[sub]["counts"].items():
                k[(sub, w, b)] = [int(x) for x in vec]
                for i, m in enumerate(PANEL):
                    checked += 1
                    if mine[(sub, w, b, m)] != k[(sub, w, b)][i]:
                        mism.append((sub, w, b, m, mine[(sub, w, b, m)], k[(sub, w, b)][i]))
    unknown = sorted({key[:3] for key in mine if key[:3] not in k})
    pub = {(r["substrate"], r["wave"], r["brand"]): json.loads(r["k_per_model"])
           for r in S31.read_csv(ROOT / "osf/v41/v41_three_wave_table.csv")}
    pub_mism = sorted(key for key, vec in k.items() if pub.get(key) != vec)
    if mism or unknown or pub_mism or len(pub) != len(k):
        raise SystemExit(f"reconciliation failed: {mism[:5]} {unknown[:5]} {pub_mism[:5]} {len(pub)} {len(k)}")
    return k, waves, {"brand_model_cells_checked": checked, "mismatches": 0,
                      "brand_units_x_waves": len(k), "published_table_rows_equal": len(pub),
                      "source": "score_v41.load_wave(t1, t2, t3) and osf/v41/v41_three_wave_table.csv"}


def n_brands(k, sub):
    return len([1 for (s, w, b) in k if s == sub and w == "t1"])


def _agg(g, sub, model, k_total):
    chars = [len(a["text"]) for a in g]
    toks = [a["out_tokens"] for a in g if a["out_tokens"] is not None]
    think = [a["thinking_tokens"] for a in g if a["thinking_tokens"] is not None]
    ev = collections.Counter(a["evidence"] for a in g)
    return {
        "cap": "" if model == "ALL" else cap_of(sub, model),
        "answers": len(g),
        "truncated": sum(a["truncated"] is True for a in g),
        "not_truncated": sum(a["truncated"] is False for a in g),
        "truncation_not_recorded": sum(a["truncated"] is None for a in g),
        "evidence": "; ".join(f"{e} {n}" for e, n in sorted(ev.items())),
        "truncated_before_first_brand": sum(a["cut_before_first_brand"] for a in g),
        "truncated_before_first_brand_others_named": sum(a["cut_before_first_brand"] and a["others_named"] for a in g),
        "truncated_after_first_brand": sum(a["truncated"] is True and a["n_named"] > 0 for a in g),
        "zero_brand_answers": sum(a["n_named"] == 0 for a in g),
        "zero_brand_answers_others_named": sum(a["n_named"] == 0 and a["others_named"] for a in g),
        "zero_brand_answers_truncation_not_recorded": sum(a["truncated"] is None and a["n_named"] == 0 for a in g),
        "brands_named_total": sum(a["n_named"] for a in g),
        "k_column_total_scorer": k_total,
        "distinct_brands_named": len({(a["substrate"], b) for a in g for b in a["named"]}),
        "chars_min": min(chars) if chars else None, "chars_median": med(chars),
        "chars_max": max(chars) if chars else None,
        "visible_tokens_min": min(toks) if toks else None, "visible_tokens_max": max(toks) if toks else None,
        "thinking_tokens_min": min(think) if think else None, "thinking_tokens_max": max(think) if think else None,
    }


def table(answers, k):
    groups = collections.defaultdict(list)
    for a in answers:
        groups[(a["substrate"], a["wave"], a["model"])].append(a)
    rows = []
    for sub in SUBS:
        for w in WAVES:
            for m in PANEL:
                kt = sum(vec[PANEL.index(m)] for (s, ww, b), vec in k.items() if s == sub and ww == w)
                r = {"substrate": sub, "wave": w, "model": m, "brands_in_registry": n_brands(k, sub)}
                r.update(_agg(groups[(sub, w, m)], sub, m, kt))
                if r["brands_named_total"] != kt:
                    raise SystemExit(f"column total mismatch {sub} {w} {m}")
                rows.append(r)
            g = [a for m in PANEL for a in groups[(sub, w, m)]]
            kt = sum(sum(vec) for (s, ww, b), vec in k.items() if s == sub and ww == w)
            r = {"substrate": sub, "wave": w, "model": "ALL", "brands_in_registry": n_brands(k, sub)}
            r.update(_agg(g, sub, "ALL", kt))
            rows.append(r)
    for w in WAVES + ("all",):
        g = [a for a in answers if w == "all" or a["wave"] == w]
        kt = sum(sum(vec) for (s, ww, b), vec in k.items() if w == "all" or ww == w)
        r = {"substrate": "ALL", "wave": w, "model": "ALL", "brands_in_registry": ""}
        r.update(_agg(g, "", "ALL", kt))
        rows.append(r)
    for m in PANEL:
        g = [a for a in answers if a["model"] == m]
        kt = sum(vec[PANEL.index(m)] for vec in k.values())
        r = {"substrate": "ALL", "wave": "all", "model": m, "brands_in_registry": ""}
        r.update(_agg(g, "", "ALL", kt))
        r["cap"] = "per substrate"
        rows.append(r)
    return rows


def load_profiles():
    rev, rel = "aias-2-0-data-locked", "osf/aias_2_0/aias_2_0_profiles.csv"
    raw = git_show(rev, rel)
    rows = list(csv.DictReader(raw.decode().splitlines()))
    prof = {(r["wave"], r["substrate"], r["brand"]): r for r in rows}
    return prof, {"rev": rev, "path": rel, "git_blob": blob(rev, rel), "sha256": sha256_bytes(raw),
                  "rows": len(rows), "same_blob_on_branch_aias-2.0": blob("aias-2.0", rel) == blob(rev, rel)}


def touched(answers, k, prof, thinking):
    """Brands whose Presence (P) and Consistency (C*) inputs rest on cut-off answers.
    A cut-off answer that did not name brand b may have understated that model's k for b by one.
    Cells listed: every answer that ended on the cap (any model), plus the not-recorded answers of a
    thinking model in a substrate where all of that model's t3 answers ended on the cap."""
    trunc = collections.defaultdict(list)
    nrec = collections.defaultdict(list)
    for a in answers:
        if a["truncated"] is True:
            trunc[(a["substrate"], a["wave"], a["model"])].append(a)
        elif a["truncated"] is None and a["model"] in thinking:
            nrec[(a["substrate"], a["wave"], a["model"])].append(a)
    all_t3_cut = {(a["substrate"], a["model"]) for a in answers if a["wave"] == "t3"}
    all_t3_cut = {(s, m) for (s, m) in all_t3_cut
                  if all(x["truncated"] is True for x in answers if x["substrate"] == s and x["model"] == m and x["wave"] == "t3")}
    rows, summary = [], []
    for (sub, w, b), vec in sorted(k.items()):
        cells = {}
        for i, m in enumerate(PANEL):
            tr = trunc.get((sub, w, m), [])
            nr = nrec.get((sub, w, m), []) if (sub, m) in all_t3_cut else []
            if tr or nr:
                cells[m] = {"k": vec[i], "cut_answers": len(tr), "cut_answers_without_brand": sum(b not in a["named"] for a in tr),
                            "not_recorded_answers": len(nr), "not_recorded_answers_without_brand": sum(b not in a["named"] for a in nr)}
        if not cells:
            continue
        p = prof.get((w, sub, b), {})
        rows.append({"substrate": sub, "wave": w, "brand": NAME23.get(b, b) if sub == "v0.23" else b,
                     "brand_id": b if sub == "v0.23" else "", "k_per_model": json.dumps(vec),
                     "models_with_cut_cells": ";".join(cells), "cells": json.dumps(cells),
                     "flash_k": vec[PANEL.index(FLASH)],
                     "other_models_k_min": min(v for j, v in enumerate(vec) if PANEL[j] != FLASH),
                     "other_models_k_max": max(v for j, v in enumerate(vec) if PANEL[j] != FLASH),
                     "P": p.get("P"), "C_star": p.get("C_star"), "rated": p.get("rated"), "n_mentions": p.get("n_mentions")})
    for sub in SUBS:
        for w in WAVES:
            for m in PANEL:
                tr = trunc.get((sub, w, m), [])
                nr = nrec.get((sub, w, m), []) if (sub, m) in all_t3_cut else []
                if not tr and not nr:
                    continue
                i = PANEL.index(m)
                units = [(b, vec) for (s, ww, b), vec in k.items() if s == sub and ww == w]
                rated = [b for b, _ in units if (prof.get((w, sub, b)) or {}).get("rated") == "1"]
                summary.append({
                    "substrate": sub, "wave": w, "model": m, "brands_in_registry": len(units),
                    "cut_answers": len(tr), "cut_before_first_brand": sum(a["n_named"] == 0 for a in tr),
                    "not_recorded_answers": len(nr), "not_recorded_zero_brand": sum(a["n_named"] == 0 for a in nr),
                    "brands_touched": sum(1 for b, _ in units if any(b not in a["named"] for a in tr + nr)),
                    "brands_with_model_k_0": sum(1 for _, vec in units if vec[i] == 0),
                    "brands_with_model_k_0_named_by_another_model": sum(1 for _, vec in units if vec[i] == 0 and sum(vec) > 0),
                    "model_k_column_total": sum(vec[i] for _, vec in units),
                    "touched_brands_rated_for_consistency": sum(1 for b in rated if any(b not in a["named"] for a in tr + nr)),
                    "brands_rated_for_consistency": len(rated),
                })
    return rows, summary


def phase_a_summary(recs, k_waves):
    """t3 Phase A truncation per substrate x model (finish reason), and each model's recognition
    count (C_P input) per wave from score_v41.load_wave."""
    out = []
    for sub in SUBS:
        for m in PANEL:
            g = [a for a in recs if a["substrate"] == sub and a["model"] == m]
            i = PANEL.index(m)
            rec = {w: sum(int(v[i]) for v in k_waves[w][sub]["recog"].values()) for w in WAVES}
            out.append({"substrate": sub, "model": m, "t3_answers": len(g),
                        "t3_truncated": sum(is_trunc(a["side"]["finish_reason"]) for a in g),
                        "t3_finish_reasons": dict(collections.Counter(a["side"]["finish_reason"] for a in g)),
                        "recognized_brands_t1": rec["t1"], "recognized_brands_t2": rec["t2"], "recognized_brands_t3": rec["t3"],
                        "brands": len(k_waves["t1"][sub]["recog"])})
    return out


# ============================================================================================
# Part 2 -- newer collections
# ============================================================================================
def _needles(text, needles, where):
    missing = [n for n in needles if n not in text]
    if missing:
        raise SystemExit(f"cap check failed: {where} lacks {missing}")


def coll_rows(name, recs, key_fn, cap_fn, n_named_fn, cap_source, qkey_fn=None):
    """recs: dicts with model, status, finish_reason. Groups by key_fn. qkey_fn(r) names the question
    (same arm and condition), to ask whether another model named a brand on it."""
    groups = collections.defaultdict(list)
    for r in recs:
        groups[key_fn(r)].append(r)
    others = collections.defaultdict(dict)
    if n_named_fn and qkey_fn:
        for r in recs:
            if r["status"] == "ok":
                others[qkey_fn(r)][r["model"]] = n_named_fn(r)

    def oth(r):
        return any(n > 0 for m, n in others[qkey_fn(r)].items() if m != r["model"])

    rows = []
    for key in sorted(groups, key=str):
        g = groups[key]
        ok = [r for r in g if r["status"] == "ok"]
        tr = [r for r in ok if is_trunc(r["finish_reason"])]
        cap = cap_fn(g[0])
        think = [r.get("think") for r in ok if r.get("think") is not None]
        row = {"collection": name, **dict(zip(("arm", "condition", "phase", "model"), key)),
               "cap": cap, "cap_source": cap_source,
               "calls": len(g), "errors": len(g) - len(ok), "answers": len(ok),
               "hit_cap": len(tr), "share_hit_cap": round(len(tr) / len(ok), 4) if ok else None,
               "max_thinking_tokens": max(think) if think else None,
               "max_thinking_share_of_cap": round(max(think) / cap, 4) if think and cap else None,
               "answers_thinking_ge_half_cap": sum(1 for t in think if cap and t >= cap / 2) if think else None,
               "answers_at_cap_and_thinking_ge_half_cap": sum(1 for r in tr if r.get("think") is not None
                                                              and cap and r["think"] >= cap / 2) if think else None}
        if n_named_fn:
            row.update({"cut_before_first_brand": sum(1 for r in tr if n_named_fn(r) == 0),
                        "cut_before_first_brand_others_named": sum(1 for r in tr if n_named_fn(r) == 0 and oth(r)),
                        "zero_brand_answers": sum(1 for r in ok if n_named_fn(r) == 0),
                        "zero_brand_answers_not_cut": sum(1 for r in ok if n_named_fn(r) == 0
                                                          and not is_trunc(r["finish_reason"])),
                        "brands_named_total": sum(n_named_fn(r) for r in ok)})
        else:
            row.update({"cut_before_first_brand": 0 if not tr else None})
        row["finish_reasons"] = json.dumps(dict(collections.Counter(str(r["finish_reason"]) for r in ok)))
        rows.append(row)
    return rows


def collection_v38():
    raw = json.load(open(ROOT / "osf/v38/data/v38_raw.json"))
    sc = load_module(ROOT / "osf/v38/scripts/score_v0_38.py", "score_v0_38_audit")
    reg = json.loads((ROOT / "osf/v38/registries/brands_home_roasters_v0.38.json").read_text())
    coder = sc.Coder(reg)
    coded = {(r["probe_id"], r["model_slot"]): r for r in S31.read_csv(ROOT / "osf/v38/data/v38_coded.csv")}
    acq = (ROOT / "osf/v38/scripts/acquire_v0_38.py").read_text()
    _needles(acq, ["max_tokens=2048", "max_output_tokens=2048"], "acquire_v0_38.py")
    agree = 0
    recs = []
    for r in raw:
        c = coded[(r["probe_id"], r["model_slot"])]
        n = int(c["n_brands"]) if c["n_brands"] not in ("", None) else 0
        if r["status"] == "ok":
            agree += len(coder.brand_matches(r.get("response") or "")) == n
        recs.append({"arm": "L", "condition": "S0", "phase": r.get("kind"), "model": r["model_id"], "status": r["status"],
                     "finish_reason": r.get("finish_reason"), "n_named": n, "probe": r["probe_id"],
                     "think": r.get("tokens_thought")})
    rows = coll_rows("v0.38", recs, lambda r: ("L", "S0", "all", r["model"]), lambda r: 2048,
                     lambda r: r["n_named"], "osf/v38/scripts/acquire_v0_38.py: max_tokens=2048 / max_output_tokens=2048",
                     qkey_fn=lambda r: r["probe"])
    return rows, {"matcher": "score_v0_38.Coder.brand_matches; n_brands from osf/v38/data/v38_coded.csv",
                  "coder_count_equals_coded_n_brands": f"{agree} of {sum(r['status'] == 'ok' for r in raw)}"}


def collection_v39():
    raw = json.load(open(ROOT / "osf/v39/data/v39_raw.json"))
    sc = load_module(ROOT / "osf/v39/scripts/score_v0_39.py", "score_v0_39_audit")
    reg = json.loads((ROOT / "osf/v39/registries/brands_commercial_roasters_v0.39.json").read_text())
    coder = sc.Coder(reg)
    coded = {r["key"]: r for r in S31.read_csv(ROOT / "osf/v39/data/v39_coded.csv")}
    acq = (ROOT / "osf/v39/scripts/acquire_v0_39.py").read_text()
    _needles(acq, ["LEGACY_MAX_TOKENS = 2048", "CURRENT_MAX_TOKENS = 16384", "max_output_tokens=2048"], "acquire_v0_39.py")
    agree = total = 0
    recs = []
    for r in raw:
        c = coded[sc.key_of(r)]
        n = int(c["n_brands"]) if c["n_brands"] not in ("", None) else 0
        if r["status"] == "ok":
            total += 1
            agree += len(coder.brand_matches(r.get("response") or "")) == n
        recs.append({"arm": r["arm"], "condition": r.get("condition", "S0"), "phase": "all", "model": r["model_id"],
                     "status": r["status"], "finish_reason": r.get("finish_reason"), "n_named": n, "probe": r["probe_id"],
                     "think": r.get("tokens_thought")})
    rows = coll_rows("v0.39", recs, lambda r: (r["arm"], r["condition"], "all", r["model"]),
                     lambda r: 2048 if r["arm"] == "L" else 16384, lambda r: r["n_named"],
                     "osf/v39/scripts/acquire_v0_39.py: LEGACY_MAX_TOKENS = 2048 (arm L), CURRENT_MAX_TOKENS = 16384 (arm C)",
                     qkey_fn=lambda r: (r["arm"], r["condition"], r["probe"]))
    return rows, {"matcher": "score_v0_39.Coder.brand_matches; n_brands from osf/v39/data/v39_coded.csv (after the "
                             "section 3.3 common-noun audit)",
                  "coder_count_equals_coded_n_brands": f"{agree} of {total}"}


T4_TAG = "v0.42-acquisition-locked"
T4_SHA = "f3109091f51af7899098d83a1d7b2080a26a06824caa5f6fc0486f3d6196d4bf"  # osf/methodology/v1_12/anchor/t4_complete_v1_12.json


def collection_t4():
    raw = git_show(T4_TAG, "osf/v42/data/t4_raw.jsonl")
    if sha256_bytes(raw) != T4_SHA:
        raise SystemExit("t4_raw.jsonl at the acquisition tag does not match the t4 completion record")
    acq = git_show(T4_TAG, "osf/v42/scripts/acquire_v0_42.py").decode()
    _needles(acq, ["CURRENT_MAX_TOKENS = 16384", '"max_tokens": CURRENT_MAX_TOKENS',
                   '"max_output_tokens": CURRENT_MAX_TOKENS'], "acquire_v0_42.py")
    recs = [json.loads(l) for l in raw.decode().splitlines() if l.strip()]
    rr = [{"arm": "C", "condition": r["condition"], "phase": r["phase"], "model": r["model_requested"],
           "status": r["status"], "finish_reason": r.get("finish_reason"), "text": r.get("text") or "",
           "out": (r.get("output_tokens") or 0) + (r.get("thinking_tokens") or 0),
           "think": r.get("thinking_tokens")} for r in recs]
    rows = coll_rows("v0.42 (t4)", rr, lambda r: ("C", r["condition"], r["phase"], r["model"]), lambda r: 16384,
                     None, f"git {T4_TAG}:osf/v42/scripts/acquire_v0_42.py CURRENT_MAX_TOKENS = 16384")
    mx = collections.defaultdict(int)
    for r in rr:
        if r["status"] == "ok":
            mx[(r["condition"], r["phase"], r["model"])] = max(mx[(r["condition"], r["phase"], r["model"])], r["out"])
    for row in rows:
        row["max_output_plus_thinking_tokens"] = mx[(row["condition"], row["phase"], row["model"])]
    return rows, {"raw": f"git {T4_TAG}:osf/v42/data/t4_raw.jsonl", "sha256": T4_SHA, "lines": len(recs),
                  "note": "no answer ended on the cap, so no answer can have been cut before its first brand"}


V115_JUDGE = Path("/Users/pablou/aias/_worktrees/v1.15/osf/methodology/v1_15/data/judge_raw_v1_15.jsonl")


def coding_calls(side_all):
    """Coding and judge calls (they read answers; they are not answers)."""
    out = []
    sc = (ROOT / "scripts/score_v0_23.py").read_text()
    _needles(sc, ["max_tokens=10,", "max_tokens=200,"], "score_v0_23.py")
    for ph, cap in (("A_judge", 10), ("B_code", 200)):
        g = [r for r in side_all if r["phase"] == ph]
        out.append({"collection": f"v0.41 t3 v0.23 coding ({ph})", "model": ";".join(sorted({r['alias'] for r in g})),
                    "cap": cap, "cap_source": "scripts/score_v0_23.py judge_recognition max_tokens=10 / "
                                               "judge_elaboration_batch max_tokens=200",
                    "calls": len(g), "hit_cap": sum(is_trunc(r["finish_reason"]) for r in g),
                    "effect": "B_code feeds the elaboration flags only; brand_mentions (k) are regex-coded"})
    if V115_JUDGE.exists():
        recs = [json.loads(l) for l in open(V115_JUDGE) if l.strip()]
        by = collections.defaultdict(list)
        for r in recs:
            q = r.get("request") or {}
            by[(r.get("judge_model"), q.get("max_tokens", q.get("max_output_tokens")))].append(r)
        for (m, cap), g in sorted(by.items(), key=str):
            ok = [r for r in g if r.get("status") == "ok"]
            out.append({"collection": "v1.15 Stage J judge on t4 (untracked file in the v1.15 worktree)", "model": m,
                        "cap": cap, "cap_source": f"request.max_tokens in {V115_JUDGE.name} (sha256 {sha256_file(V115_JUDGE)[:16]}...)",
                        "calls": len(g), "answers": len(ok), "hit_cap": sum(is_trunc(r.get("finish_reason")) for r in ok),
                        "effect": "judge outputs, not answers"})
    return out


NOT_COLLECTED = [
    # study, branch, folder, acquisition script (or None), cap code strings, what the study is
    ("v0.40", "v0.40-public", "osf/v40", "osf/v40/scripts/acquire_v0_40.py",
     ["LEGACY_MAX_TOKENS = 2048", "CURRENT_MAX_TOKENS = 16384", "thinking_budget=0"],
     "legacy arm (2,048; Gemini 2.5 Flash with thinking budget 0, plus an M5X pass at the v0.39 setting) and current "
     "arm (16,384); collection window Nov 17-21; registries and FDIC status checks only"),
    ("v0.43", "v0.43", "osf/v43", None, [], "Google Trends pulls; no model answers"),
    ("v0.44", "v0.44", "osf/v44", "osf/v44/scripts/acquire_v0_44.py", ["CURRENT_MAX_TOKENS = 16384"],
     "industry-breadth wave on the current models; dry run only (collection window from 2026-11-24)"),
    ("v0.45", "v0.45", "osf/v45", "osf/v45/scripts/acquire_v0_45.py", ["CURRENT_MAX_TOKENS = 16384"],
     "t5 wave; locked, dry run only"),
    ("v1.11", "v1.11", "osf/methodology/v1_11", None, [],
     "Sentiment judge on archived answers; the dry-run judge file in the worktree is simulated (\"synthetic quote\")"),
    ("v1.12", "v1.12", "osf/methodology/v1_12", "osf/methodology/v1_12/scripts/acquire_v1_12.py",
     ["CURRENT_MAX_TOKENS = 16384"], "Coverage collection; dry run says raw record absent (window from 2026-11-14)"),
    ("v1.13", "v1.13", "osf/methodology/v1_13", None, [], "website structured-data audit; no model answers"),
    ("v1.14", "v1.14", "osf/methodology/v1_14", None, [], "re-analysis of t4 (v0.42); no new collection"),
    ("v1.16", "v1.16", "osf/methodology/v1_16", None, [], "re-analysis of t1-t4; no new collection"),
]
RAW_NAME = ("_raw.json", "_raw.jsonl", "responses.jsonl", "answers.jsonl", "answers.csv")


def not_collected():
    out = []
    for study, br, folder, acq, needles, what in NOT_COLLECTED:
        files = git("ls-tree", "-r", "--name-only", br, folder).split()
        raw = [f for f in files if f.endswith(RAW_NAME) and "/tests/" not in f and "fake" not in f]
        cap = None
        if acq:
            _needles(git_show(br, acq).decode(), needles, f"{br}:{acq}")
            cap = "; ".join(needles)
        out.append({"study": study, "branch": br, "folder": folder, "files_in_folder": len(files),
                    "answer_files_found": raw, "cap_in_code": cap, "status": what})
    return out


# ============================================================================================
# writing
# ============================================================================================
def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    keys = []
    for r in rows:
        for k in r:
            if k not in keys:
                keys.append(k)
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in keys})


def answer_rows(answers):
    out = []
    for a in sorted(answers, key=lambda a: (a["substrate"], a["wave"], PANEL.index(a["model"]), a["question"])):
        out.append({"substrate": a["substrate"], "wave": a["wave"], "model": a["model"], "question": a["question"],
                    "cap": a["cap"], "finish_reason": a["finish_reason"], "visible_tokens": a["out_tokens"],
                    "thinking_tokens": a["thinking_tokens"], "truncated": a["truncated"], "evidence": a["evidence"],
                    "brands_named": a["n_named"], "cut_before_first_brand": a["cut_before_first_brand"],
                    "another_model_named_a_brand_on_this_question": a["others_named"],
                    "named": ";".join(NAME23.get(b, b) for b in a["named"]), "chars": len(a["text"]),
                    "last_60_chars": a["text"][-60:].replace("\n", " "), "matched_by": a["matched_by"]})
    return out


def verify_claims(k, tab, side_all, answers, pa):
    def coltot(sub):
        out = {}
        for w in WAVES:
            per = {r["model"]: r["brands_named_total"] for r in tab
                   if r["substrate"] == sub and r["wave"] == w and r["model"] != "ALL"}
            others = [v for m, v in per.items() if m != FLASH]
            out[w] = {"gemini-2.5-flash": per[FLASH], "other_models_min": min(others),
                      "other_models_max": max(others), "per_model": per}
        return out

    hp = {}
    for w in WAVES:
        g = [a for a in answers if a["substrate"] == "v0.19" and a["model"] == FLASH and a["wave"] == w]
        hp[w] = {"answers": len(g), "visible_tokens": [min(a["out_tokens"] for a in g), max(a["out_tokens"] for a in g)],
                 "chars": [min(len(a["text"]) for a in g), max(len(a["text"]) for a in g)],
                 "brands_named": sum(a["n_named"] for a in g),
                 "finish_reasons": dict(collections.Counter(str(a["finish_reason"]) for a in g))}
    study = collections.defaultdict(lambda: [0, 0])
    for a in [x for x in answers if x["wave"] == "t3"] + pa:
        study[a["model"]][0] += 1
        study[a["model"]][1] += is_trunc(a["side"]["finish_reason"])
    phase_b = collections.defaultdict(lambda: [0, 0])
    for a in answers:
        if a["wave"] == "t3":
            phase_b[a["model"]][0] += 1
            phase_b[a["model"]][1] += a["truncated"] is True
    return {
        "sennheiser_k_per_model": {w: k[("v0.19", w, "Sennheiser")] for w in WAVES},
        "headphones_v0_19_column_totals": coltot("v0.19"),
        "spirits_v0_23_column_totals": coltot("v0.23"),
        "headphones_flash_answers": hp,
        "paper_3_6_mc_truncation_recomputed (score_v41.mc_truncation on the t3 sidecar, all calls incl. "
        "the interrupted spirits calls and coding calls)": S.mc_truncation(S._sidecar(SIDECAR3)),
        "t3_final_study_answers_852 (phase A + B, by model): [answers, ended on cap]": dict(study),
        "t3_phase_b_answers_180 (by model): [answers, ended on cap]": dict(phase_b),
    }


def main():
    side_all = list(csv.DictReader(open(SIDECAR3, newline="")))
    thinking = thinking_models(side_all)
    runners = check_runners()
    answers = all_answers()
    mapping_b = attach_t3(answers, side_all, "B")
    classify(answers, thinking)
    tok = token_rule_check(answers, thinking)
    k, waves, recon = reconcile(answers)
    tab = table(answers, k)
    prof, prof_meta = load_profiles()
    trows, tsum = touched(answers, k, prof, thinking)
    pa = phase_a_t3_records()
    mapping_a = attach_t3(pa, side_all, "A")
    pa_sum = phase_a_summary(pa, waves)
    c38, m38 = collection_v38()
    c39, m39 = collection_v39()
    c42, m42 = collection_t4()
    codes = coding_calls(side_all)
    nc = not_collected()
    claims = verify_claims(k, tab, side_all, answers, pa)

    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUT / "omnibus_answers.csv", answer_rows(answers))
    write_csv(OUT / "omnibus_table.csv", tab)
    write_csv(OUT / "touched_brands.csv", trows)
    write_csv(OUT / "touched_summary.csv", tsum)
    write_csv(OUT / "phase_a_t3.csv", pa_sum)
    write_csv(OUT / "newer_collections.csv", c38 + c39 + c42)
    write_csv(OUT / "coding_calls.csv", codes)
    write_csv(OUT / "not_collected.csv", nc)
    res = {
        "run_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "tree": str(TREE), "git_head": git("rev-parse", "HEAD").strip(),
        "python": sys.version.split()[0],
        "definitions": {
            "truncated": "the answer ended on the output-token limit; evidence order finish_reason (t3 sidecar, "
                         "score_v41.TRUNC_REASONS), tokens_at_cap (models without hidden thinking tokens), "
                         "identical_to_t3 (same model, same question, byte-identical text; models without hidden "
                         "thinking tokens), else not_recorded",
            "truncated_before_first_brand": "truncated and the scorer's matcher finds no registry brand in it",
            "brands_named_total": "sum over the model's answers of registry brands named = the model's column total of k_per_model",
            "thinking_models": thinking,
        },
        "checks": {"runner_caps": runners, "t3_sidecar_mapping_phase_b": mapping_b,
                   "t3_sidecar_mapping_phase_a": mapping_a, "token_rule_vs_finish_reason_t3_v0_19": tok,
                   "reconciliation_with_scorer": recon, "aias_2_0_profiles": prof_meta,
                   "v0_38": m38, "v0_39": m39, "t4": m42},
        "claims": claims,
        "omnibus_table": tab, "touched_summary": tsum, "phase_a_t3": pa_sum,
        "newer_collections": c38 + c39 + c42, "coding_calls": codes, "not_collected": nc,
    }
    (OUT / "truncation_audit_results.json").write_text(json.dumps(res, indent=1, default=str))
    print(f"wrote {OUT}")
    for r in tab:
        if r["truncated"] or r["model"] == "ALL" or r["zero_brand_answers"]:
            print(f"{r['substrate']:6} {r['wave']:4} {r['model']:22} ans {r['answers']:4} trunc {r['truncated']:3} "
                  f"nrec {r['truncation_not_recorded']:3} cut0 {r['truncated_before_first_brand']:3} "
                  f"zero {r['zero_brand_answers']:3} named {r['brands_named_total']:4}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
