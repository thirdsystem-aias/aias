#!/usr/bin/env python3
"""AIAS v1.20 (proposed id), section 8: the answers that v1.11 judges and that stopped at the answering
model's output limit, from STORED METADATA only. DRAFT r1, not locked.

Writes osf/methodology/v1_20/scoping/cut_units_v1_20.csv (one row per answer that ended at the cap) and
cut_units_v1_20.json (counts by group, the S-CUT-M cells, every input file with its SHA-256, the method).
Reads no judge output (none exists), computes no valence, S, P, C* or Ranking value, prints no answer text.

Answers: every R (recognition) and F (omnibus category) answer of v1.11's sets, loaded with v1.11's own
loaders (score_v1_11.load_recognition, v1.10's load_answers) so that answer ids equal the unit table's;
the raw file row of each answer (the loader's `row`) gives its stored metadata. E (eight early sets):
the answer files are checked for any finish-reason or token column (none is expected; v1.20 section 8).

Evidence that an answer ended at the cap (in this order):
  finish_reason    t3 only: the v0.41 call sidecar osf/v41/data/v41_provenance.csv, matched to each
                   answer call by call (v0.23 A and B: the one sidecar row of the same model stamped
                   inside the answer's [ts_start, ts_end]; v0.19 B: the sequential runner's call order,
                   model and output tokens equal; v0.20-v0.22 B: nearest time stamp of the same model,
                   one to one, at most 1 s); cap set = score_v1_20.cut_by_cap (max_tokens, MAX_TOKENS,
                   FinishReason.MAX_TOKENS, length, max_output_tokens).
  tokens_at_cap    v0.19 t1/t2 (the only t1/t2 files with token counts): recorded output tokens >= the
                   runner's cap, for models whose calls carry no hidden thinking tokens (thinking models
                   = any model with thinking tokens in the sidecar: gemini-2.5-flash).
  identical_to_t3  INFERRED, not a recorded field: t1/t2 text byte-identical to the t3 answer of the
                   same model and question that ended at the cap, models without thinking tokens.
Caps are the runners' (each code string is checked in the file): v0.19 1,024 all models; v0.20-v0.22
2,048 Claude and GPT, none sent to Gemini; v0.23 (A and B) 2,048 all models.

Run (repository root): PYTHONDONTWRITEBYTECODE=1 python3 osf/methodology/v1_20/scoping/cut_units_v1_20.py
"""
import csv
import hashlib
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts"))
import score_v1_11 as S   # noqa: E402
import score_v1_20 as R   # noqa: E402

V = S.V
HERE = Path(__file__).resolve().parent
OUT_CSV, OUT_JSON = HERE / "cut_units_v1_20.csv", HERE / "cut_units_v1_20.json"
UNITS = "osf/methodology/v1_11/prereg/units_v1_11.csv"
SIDECAR = "osf/v41/data/v41_provenance.csv"
LEGACY = ("claude-opus-4-5", "claude-sonnet-4-5", "gpt-4o", "gpt-4o-mini", "gemini-2.5-flash", "gemini-2.5-flash-lite")
PROVIDER = {m: ("anthropic" if m.startswith("claude") else "openai" if m.startswith("gpt") else "google") for m in LEGACY}
B2048 = 'pool.submit(call_llm, t["model"], t["frame_text"], 2048)'
GNOCAP = "resp = model.generate_content(prompt)"
RUNNERS = {"v0.19": ("protocol/providers.py", {"anthropic": 1024, "openai": 1024, "google": 1024},
                     ["max_tokens=1024", 'generation_config={"max_output_tokens": 1024}']),
           "v0.20": ("scripts/run_acquisition_v20.py", {"anthropic": 2048, "openai": 2048, "google": None}, [B2048, GNOCAP]),
           "v0.21": ("scripts/run_acquisition_v21.py", {"anthropic": 2048, "openai": 2048, "google": None}, [B2048, GNOCAP]),
           "v0.22": ("scripts/run_acquisition_v22.py", {"anthropic": 2048, "openai": 2048, "google": None}, [B2048, GNOCAP]),
           "v0.23": ("scripts/acquire_v0_23.py", {"anthropic": 2048, "openai": 2048, "google": 2048},
                     ["max_tokens=2048", "max_output_tokens=2048"])}
SUB = {"v0.19": "v19", "v0.20": "v20", "v0.21": "v21", "v0.22": "v22", "v0.23": "v23"}
PREVIOUS_LANE = {"R t3 at the cap": "35 of 144", "F cut after naming a brand": "16 (t1 4, t2 5, t3 7)",
                 "F cut before any brand": "11 (t3: v0.19 gemini-2.5-flash 6, v0.23 gemini-2.5-flash 5)"}
COLS = ["block", "wave", "set", "category", "model", "provider", "question_id", "answer_id", "cap_tokens",
        "evidence_class", "finish_reason", "output_tokens", "thinking_tokens", "named_registry_brand",
        "v1_11_units", "v1_11_units_judged", "j2_sample_units", "paper_b_units", "unit_status"]
READ = {}


def sha(rel: str) -> str:
    h = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
    READ[rel] = h
    return h


def norm(m) -> str:
    return str(m or "").split("/")[-1].strip()


def ts(s) -> datetime:
    return datetime.fromisoformat(str(s))


def raw_rows(rel: str) -> list:
    sha(rel)
    p = ROOT / rel
    if rel.endswith(".jsonl"):
        return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
    if rel.endswith(".json"):
        return json.loads(p.read_text(encoding="utf-8"))
    return V._read_csv(p)


def raw_model(spec, r) -> str:
    return norm(r.get("panel_model") or r.get("model_id") or r.get("model"))


def check_runners() -> dict:
    out = {}
    for sub, (rel, caps, needles) in RUNNERS.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        sha(rel)
        missing = [n for n in needles if n not in text]
        if missing:
            raise SystemExit(f"cap check failed: {rel} lacks {missing}")
        out[sub] = {"runner": rel, "cap_by_provider": caps, "code_strings_found": needles}
    return out


def match_t3(spec, answers, raw, side) -> dict:
    """answer_id -> its own sidecar row (t3)."""
    sub, cat = spec["block"], spec["category"]
    rows = [r for r in side if r["substrate"] == SUB[cat] and r["phase"] == ("A" if sub == "R" else "B")]
    out = {}
    if cat == "v0.23":
        for a in answers:
            r0 = raw[a["row"]]
            lo, hi = ts(r0["ts_start"]), ts(r0["ts_end"])
            c = [r for r in rows if norm(r["alias"]) == a["model"] and lo <= ts(r["timestamp"]) <= hi]
            if len(c) != 1:
                raise SystemExit(f"{spec['set']} {a['answer_id']}: {len(c)} sidecar rows in its time window")
            out[a["answer_id"]] = c[0]
        return out
    if cat == "v0.19":
        order = sorted(answers, key=lambda a: a["row"])
        if len(rows) != len(order):
            raise SystemExit(f"{spec['set']}: {len(rows)} sidecar rows for {len(order)} answers")
        for a, r in zip(order, rows):
            if norm(r["alias"]) != a["model"] or str(r["output_tokens"]) != str(raw[a["row"]].get("tokens_out")):
                raise SystemExit(f"{spec['set']}: call order does not line up at {a['answer_id']}")
            out[a["answer_id"]] = r
        return out
    used, worst = set(), 0.0
    for a in sorted(answers, key=lambda a: a["row"]):
        t = ts(raw[a["row"]]["timestamp"])
        c = sorted((abs((ts(r["timestamp"]) - t).total_seconds()), j) for j, r in enumerate(rows)
                   if j not in used and norm(r["alias"]) == a["model"])
        d, j = c[0]
        used.add(j)
        worst = max(worst, d)
        out[a["answer_id"]] = rows[j]
    if worst > 1.0 or len(used) != len(rows):
        raise SystemExit(f"{spec['set']}: time match failed (worst {worst:.3f} s, {len(used)}/{len(rows)} rows)")
    return out


def main() -> int:
    runners = check_runners()
    sha(UNITS)
    per_answer = defaultdict(Counter)
    with open(ROOT / UNITS, encoding="utf-8", newline="") as f:
        csv.field_size_limit(sys.maxsize)
        for u in csv.DictReader(f):
            c = per_answer[u["answer_id"]]
            c["units"] += 1
            c["judged"] += u["judged"] == "1"
            c["j2"] += u["j2"] == "1"
            c["human"] += u["human"] == "1"
    sha(SIDECAR)
    side = V._read_csv(ROOT / SIDECAR)
    thinking = sorted({norm(r["alias"]) for r in side if (r.get("thinking_tokens") or "").strip() not in ("", "0")})
    ctx = S.make_ctx(False)
    ans, e_cols = [], {}
    for spec in S.build_sets():
        if spec["block"] == "E":
            sha(spec["answers"])
            with open(ROOT / spec["answers"], encoding="utf-8", newline="") as f:
                cols = next(csv.reader(f))
            e_cols[spec["set"]] = [c for c in cols if any(k in c.lower() for k in ("finish", "token", "stop", "length", "trunc"))]
            continue
        answers = S.load_recognition(ctx, spec) if spec["block"] == "R" else V.load_answers(ctx, spec)
        raw = raw_rows(spec["answers"])
        for a in answers:
            if raw_model(spec, raw[a["row"]]) != a["model"]:
                raise SystemExit(f"{spec['set']}: raw row {a['row']} is not {a['model']}")
        side_of = match_t3(spec, answers, raw, side) if spec["wave"] == "t3" else {}
        cap = RUNNERS[spec["category"]][1]
        for a in answers:
            if a["model"] not in LEGACY:
                continue
            r0, s = raw[a["row"]], side_of.get(a["answer_id"])
            rec = {"block": spec["block"], "wave": spec["wave"], "set": spec["set"], "category": spec["category"],
                   "model": a["model"], "provider": PROVIDER[a["model"]],
                   "question_id": a["brand"] if spec["block"] == "R" else a["frame"], "answer_id": a["answer_id"],
                   "cap_tokens": cap[PROVIDER[a["model"]]], "text": a["text"] or "", "evidence_class": "",
                   "finish_reason": s["finish_reason"] if s else "",
                   "output_tokens": (s["output_tokens"] if s else (r0.get("tokens_out") if spec["category"] == "v0.19" and spec["block"] == "F" else "")) or "",
                   "thinking_tokens": (s.get("thinking_tokens") if s else "") or ""}
            if s is not None:
                if R.cut_by_cap(s["finish_reason"]):
                    rec["evidence_class"] = "finish_reason"
            elif (rec["output_tokens"] != "" and rec["cap_tokens"] is not None and a["model"] not in thinking
                  and int(rec["output_tokens"]) >= rec["cap_tokens"]):
                rec["evidence_class"] = "tokens_at_cap"
            ans.append(rec)
    t3 = {(a["block"], a["category"], a["model"], a["question_id"]): a for a in ans if a["wave"] == "t3"}
    for a in ans:
        if a["wave"] != "t3" and not a["evidence_class"] and a["model"] not in thinking:
            b = t3.get((a["block"], a["category"], a["model"], a["question_id"]))
            if b is not None and b["evidence_class"] and b["text"] == a["text"]:
                a["evidence_class"] = "identical_to_t3 (inferred)"
    rows = []
    for a in ans:
        if not a["evidence_class"]:
            continue
        c = per_answer.get(a["answer_id"], Counter())
        rows.append({**{k: a[k] for k in COLS if k in a},
                     "named_registry_brand": "n/a (recognition: whole answer)" if a["block"] == "R" else ("yes" if c["units"] else "no"),
                     "v1_11_units": c["units"], "v1_11_units_judged": c["judged"], "j2_sample_units": c["j2"],
                     "paper_b_units": c["human"], "unit_status": "kept" if c["units"] else "none"})
    rows.sort(key=lambda r: (r["block"], r["wave"], r["category"], r["model"], r["question_id"]))
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in COLS})
    # counts
    by = Counter((r["block"], r["wave"], r["category"], r["model"], r["evidence_class"], r["unit_status"]) for r in rows)
    t3n = Counter((a["block"], a["category"], a["model"]) for a in ans if a["wave"] == "t3")
    t3c = Counter((r["block"], r["category"], r["model"]) for r in rows if r["wave"] == "t3")
    cells = sorted([list(k) for k, n in t3c.items() if 2 * n >= t3n[k]])
    rec_only = [r for r in rows if not r["evidence_class"].startswith("identical")]
    groups = {
        "R t3 at the cap (of 144)": sum(1 for r in rows if r["block"] == "R" and r["wave"] == "t3"),
        "R t3 at the cap by model": dict(Counter(r["model"] for r in rows if r["block"] == "R" and r["wave"] == "t3")),
        "R t1/t2 flagged": dict(Counter(f"{r['wave']} {r['model']} {r['evidence_class']}" for r in rows if r["block"] == "R" and r["wave"] != "t3")),
        "F cut after naming a brand (unit kept), all evidence": dict(Counter(r["wave"] for r in rows if r["block"] == "F" and r["unit_status"] == "kept")),
        "F cut after naming a brand, recorded evidence only": dict(Counter(r["wave"] for r in rec_only if r["block"] == "F" and r["unit_status"] == "kept")),
        "F cut before any brand (no unit)": dict(Counter(f"{r['wave']} {r['category']} {r['model']}" for r in rows if r["block"] == "F" and r["unit_status"] == "none")),
        "F rows by wave x category x model x evidence": {"|".join(k[1:5]): n for k, n in sorted(by.items()) if k[0] == "F"},
        "v1.11 units from cut answers (judged / J2 sample / Paper B)": {
            b: [sum(int(r[c]) for r in rows if r["block"] == b) for c in ("v1_11_units_judged", "j2_sample_units", "paper_b_units")]
            for b in ("R", "F")},
        "t1/t2 answers whose cut status is not recorded (no finish reason, no token count)": {
            "R": sum(1 for a in ans if a["block"] == "R" and a["wave"] != "t3"),
            "F (v0.20-v0.23)": sum(1 for a in ans if a["block"] == "F" and a["wave"] != "t3" and a["category"] != "v0.19")},
        "answers read": dict(Counter(f"{a['block']} {a['wave']}" for a in ans)),
    }
    doc = {"phase": R.PHASE_ID, "status": R.STATUS, "created_utc": S._now(), "what": __doc__.splitlines()[0],
           "rows_csv": OUT_CSV.name, "rows": len(rows), "groups": groups,
           "s_cut_m_cells": cells,
           "s_cut_m_rule": "model x block x substrate cells with at least half of their t3 answers ended at the cap",
           "t3_answers_and_cut_by_cell": {"|".join(k): [t3c.get(k, 0), n] for k, n in sorted(t3n.items())},
           "thinking_models": thinking, "runner_caps": runners,
           "e_block": {"finish_or_token_columns": e_cols,
                       "evidence": "none of the eight E answer files has a finish-reason or token column: no stored cut evidence"},
           "previous_lane_counts": PREVIOUS_LANE,
           "inputs_sha256": dict(sorted(READ.items()))}
    OUT_JSON.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: doc[k] for k in ("rows", "groups", "s_cut_m_cells")}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
