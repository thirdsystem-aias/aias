#!/usr/bin/env python3
"""
score_v1_15.py - AIAS v1.15: Sentiment on t4 (v1.11's locked instrument applied to the t4 = v0.42 answers).

STATUS: r0 draft (2026-11-10/11), not locked. PRE_REGISTRATION_v1_15.md (sections cited inline).

The instrument is NOT re-implemented. Window rule, alias matching, unit table, window cap, self-consistency
sample, judge request, output parsing, unit score, S, the n floor, Krippendorff's alpha, rho_w, the bands, the
H1 / stability verdict functions, the noise guard and the outcome rules are imported from scripts/score_v1_11.py,
byte-identical to tag v1.11-prereg-r1 (git blob 5e46e863...), which imports scripts/score_v1_10.py (blob
0f8b981b..., = tag v1.10-prereg-r2). Registries and their loader are v1.10's (score_v1_10.OMNI_REG, load_registry).
What is new here is only what t4 needs: reading the t4 records, v0.42's drop rule (copied verbatim, see
V042_FUNCS), the certified mention record from v0.42's coded Phase B tables, and the single-wave reading (section 5).

Modes
  --cost                    planning estimate from v1.11's locked token counts (no t4 data; section 7)
  --build-units --raw-ref R --coded-ref C
                            U0 on t4 (after tag v0.42-acquisition-locked; before any judge call): units_v1_15.csv,
                            u0_v1_15.json. No model call, no valence, no P, C* or R.
  --lock-manifest           prereg/LOCK_MANIFEST_v1_15.sha256 over LOCK_FILES (last step of the content lock)
Stage J (stage_j, own_checks) and Stage C (single_wave, mnp_t4, verdicts_t4) are library functions here, tested on
synthetic data; their command-line glue (reading the frozen outputs, v1.14's Stage 1 units, writing s_t4_v1_15.csv
and v1_15_verdicts.json) is an r1 item, finished before the lock (PRE_REGISTRATION section 12).
No model call in this file (judge calls: judge_v1_15.py).
"""
from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import io
import json
import math
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

HERE = Path(__file__).resolve().parent
V115 = HERE.parent                                  # osf/methodology/v1_15
ROOT = V115.parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import score_v1_11 as S  # noqa: E402  (byte-identical to v1.11-prereg-r1:scripts/score_v1_11.py)

V = S.V

PHASE_ID = "v1.15"
PREREG_TAG = "v1.15-prereg-r1"
PREREG_DIR, DATA_DIR, OUTDIR, ANCHOR_DIR = V115 / "prereg", V115 / "data", V115 / "outputs", V115 / "anchor"
ANCHOR_FILE = ANCHOR_DIR / "git_anchor_v1_15.json"
UNITS_NAME, U0_NAME = "units_v1_15.csv", "u0_v1_15.json"
STAGE_J_NAME, VERDICTS_NAME, SCORES_NAME = "stage_j_v1_15.json", "v1_15_verdicts.json", "s_t4_v1_15.csv"

V111_TAG = "v1.11-prereg-r1"
V111_BLOBS = {"scripts/score_v1_11.py": "5e46e8632044268b5d30a2184600718961caa838",
              "scripts/judge_v1_11.py": "85ad069c0e9e7ffbbae12e1a6dc74e1e0757e8a9",
              "scripts/score_v1_10.py": "0f8b981b2895a325b50629c85f8e0e6ce8e876f5"}
# v0.42 (t4). The raw answers are read from the acquisition tag; the coded Phase B tables (the certified mention
# record) from the commit that holds them; both are logged with git blob and SHA-256 in u0_v1_15.json.
V042_RAW_TAG = "v0.42-acquisition-locked"
V042_RAW_PATH = "osf/v42/data/t4_raw.jsonl"
V042_CODED = "osf/v42/data/coded/{sub}_phase_b.csv"
V042_PRELOCK_COMMIT = "v0.42-prereg-r1"              # locked tag (-> 58d1891; scripts identical to 73daada)
V042_FUNCS = {"osf/v42/scripts/code_t4_v0_42.py": ["is_answered", "dedupe_calls"],
              "osf/v42/scripts/score_v0_42.py": ["served_ok", "in_design"]}
SUB_MAP = {"v19": "v0.19", "v20": "v0.20", "v21": "v0.21", "v22": "v0.22", "v23": "v0.23"}
N3 = ["claude-fable-5-2", "gpt-6-astra", "gemini-4-argon"]
WAVE, PANEL = "t4", "N3"
EXPECTED_S0_PER_MODEL = 30 * 3 + 112                 # score_v0_42.EXPECTED_PER_MODEL_COND["S0"]
DROP_SHARE = 0.90                                    # score_v0_42.DROP_SHARE
EXPECTED_ANSWERS_PER_SUB = 3 * 6 * 3                 # N3 x 6 category questions x 3 runs (S0)
DENON = ("v0.19", "Denon")                           # sensitivity SD (v1.11 decision 4)
SEED_BOOT, SEED_PERM = 115020, 115011                # new seeds for the t4 statistics (section 5)


class Halt(S.Halt):
    pass


# ----------------------------------------------------------------------------------------------- v0.42 rules
# Copied verbatim from tag v0.42-prereg-r1 (test_v042_functions_verbatim checks the source text).
MODELS = N3
CONDS = ["S0", "S1"]
RUNS = [1, 2, 3]
PHASE_A_DESIGN = {("S0", 1)}                       # r2: Phase A in S0, run 1 only


def is_answered(rec):
    return (rec.get("status") == "ok") and bool((rec.get("text") or "").strip()) and not rec.get("error")


def dedupe_calls(records):
    """One record per call_id: the LAST answered attempt if any, else the last attempt (the raw file is
    append-only and a re-run pass may add further lines for a call)."""
    best = {}
    for r in records:
        cid = r["call_id"]
        if cid not in best or is_answered(r) or not is_answered(best[cid]):
            best[cid] = r
    return list(best.values())


def served_ok(requested, served):
    s = (served or "").strip().removeprefix("models/")
    return s == requested or re.fullmatch(re.escape(requested) + r"-(\d{4}-\d{2}-\d{2}|\d{8})", s) is not None


def in_design(rec):
    """r2 design: N3 models; Phase B in S0/S1, runs 1-3; Phase A in S0, run 1 (N15)."""
    if rec.get("model_requested") not in MODELS or rec.get("condition") not in CONDS:
        return False
    if rec.get("phase") == "B":
        return rec.get("run") in RUNS
    if rec.get("phase") == "A":
        return (rec.get("condition"), rec.get("run")) in PHASE_A_DESIGN
    return False


def drop_rule_s0(records) -> dict:
    """v0.42's analysis set for S0 (score_v0_42.manipulation_checks, S0 rows): calls outside the design and
    answered calls with a served-ID mismatch are excluded; a model whose answered S0 calls (Phase A + B) are below
    90% of its 202 expected is dropped from S0. Returns the excluded call_ids and the dropped models."""
    calls = dedupe_calls(records)
    excluded = {r["call_id"] for r in calls if not in_design(r)}
    calls = [r for r in calls if in_design(r)]
    mism = []
    for r in calls:
        if is_answered(r) and r.get("served_model") and not served_ok(r["model_requested"], r["served_model"]):
            excluded.add(r["call_id"])
            mism.append(r["call_id"])
    answered = Counter(r["model_requested"] for r in calls if r["condition"] == "S0" and is_answered(r)
                       and r["call_id"] not in excluded)
    share = {m: answered.get(m, 0) / EXPECTED_S0_PER_MODEL for m in N3}
    dropped = sorted(m for m in N3 if share[m] < DROP_SHARE)
    return {"calls": calls, "excluded": excluded, "served_mismatch": mism, "answered_S0": dict(answered),
            "share_S0": share, "dropped_S0": dropped}


# ----------------------------------------------------------------------------------------------- git reads
def git_bytes(ref: str, path: str, root: Path = ROOT) -> Tuple[bytes, str]:
    """(content, git blob) of <ref>:<path>, read from the object store (never from a worktree)."""
    blob = subprocess.run(["git", "-C", str(root), "rev-parse", f"{ref}:{path}"], capture_output=True, text=True)
    if blob.returncode != 0:
        raise Halt(f"cannot resolve {ref}:{path}: {blob.stderr.strip()[:200]}")
    data = subprocess.run(["git", "-C", str(root), "cat-file", "blob", blob.stdout.strip()], capture_output=True)
    return data.stdout, blob.stdout.strip()


def logged(read: List[dict], ref: str, path: str, data: bytes, blob: str) -> None:
    read.append({"ref": ref, "path": path, "git_blob": blob, "sha256": hashlib.sha256(data).hexdigest(),
                 "bytes": len(data)})


def parse_jsonl(data: bytes) -> List[dict]:
    out = []
    for line in data.decode("utf-8").splitlines():
        if line.strip():
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue                                   # as code_t4_v0_42.read_raw
    return out


def parse_csv(data: bytes) -> List[dict]:
    csv.field_size_limit(sys.maxsize)
    return list(csv.DictReader(io.StringIO(data.decode("utf-8"))))


# ----------------------------------------------------------------------------------------------- U0 on t4
def t4_answers(records: List[dict]) -> Tuple[Dict[str, List[dict]], dict]:
    """The judged answer set (section 3): S0 category (Phase B) answers of N3, after v0.42's analysis-set rules.
    -> ({substrate: [answer dicts in v1.10's format + question]}, drop-rule record)."""
    dr = drop_rule_s0(records)
    out: Dict[str, List[dict]] = defaultdict(list)
    for r in dr["calls"]:
        if r["phase"] != "B" or r["condition"] != "S0" or r["call_id"] in dr["excluded"]:
            continue
        if r["model_requested"] in dr["dropped_S0"] or not is_answered(r):
            continue
        sub = SUB_MAP[r["substrate"]]
        spec = {"set": f"F t4 {sub}", "panel": PANEL, "wave": WAVE, "category": sub}
        a = V._answer(spec, r["model_requested"], r["frame_id"] or r["probe_id"], int(r["run"]), r["text"])
        a["answer_id"] = f"{spec['set']}::{r['call_id']}"
        a["call_id"], a["question"] = r["call_id"], r["prompt"]
        if not a["question"]:
            raise Halt(f"no question text for {r['call_id']}")
        out[sub].append(a)
    rec = {k: v for k, v in dr.items() if k != "calls" and k != "excluded"}
    rec["excluded_calls"] = len(dr["excluded"])
    return dict(out), rec


def certified_named_t4(coded_rows: List[dict], answers: List[dict], unit: dict) -> Tuple[Dict[str, set], dict]:
    """The certified mention record (v1.11 section 4.1, F): v0.42's coded Phase B table (one row per answered
    call x registry brand, `mentioned` 0/1, written by the substrates' certified t1 functions)."""
    by_call = {a["call_id"]: a["answer_id"] for a in answers}
    known = set(unit.values())
    out: Dict[str, set] = {a["answer_id"]: set() for a in answers}
    rows_for: Counter = Counter()
    other = 0
    for r in coded_rows:
        if r.get("condition") != "S0":
            continue
        aid = by_call.get(r["call_id"])
        if aid is None:
            other += 1                                      # dropped / excluded calls, or Phase B S0 not judged
            continue
        rows_for[aid] += 1
        if r["brand"] not in known:
            raise Halt(f"coded record names a brand outside the registry: {r['brand']}")
        if str(r["mentioned"]).strip() == "1":
            out[aid].add(r["brand"])
    missing = [aid for aid in out if rows_for[aid] != len(known)]
    if missing:
        raise Halt(f"{len(missing)} judged answers lack a complete coded row set (e.g. {missing[0]})")
    return out, {"coded_rows_not_judged": other}


def build_units_t4(answers_by_sub: Dict[str, List[dict]], coded_by_sub: Dict[str, List[dict]], ctx, log=print) -> dict:
    """U0 (v1.11 section 4.1, F rules, unchanged): one mention window per (answer, certified brand); extraction
    misses counted (> 5% of a set's mentions halts); at most 36 windows per brand x set x wave (seed 111001); J2 on
    every judged unit; self-consistency 5% (seed 111003). No human-label sample (Paper B uses the archive)."""
    units, misses, per_set = [], [], {}
    for sub in V.OMNI:
        answers = answers_by_sub.get(sub, [])
        reg, unit, _n = V.load_registry(ctx, *V.OMNI_REG[sub])
        canon_of = {u: c for c, u in unit.items()}
        named, crec = certified_named_t4(coded_by_sub.get(sub, []), answers, unit)
        aliases = {u: [canon_of[u], *reg[canon_of[u]]] for u in canon_of}
        pats = {u: S.alias_pattern(al) for u, al in aliases.items()}
        others = {u: S.other_pattern(pats[u], [x for o, al in aliases.items() if o != u for x in al]) for u in aliases}
        spec = {"set": f"F t4 {sub}", "block": "F", "panel": PANEL, "wave": WAVE, "category": sub}
        mentions = windows = 0
        for a in answers:
            A = S.AnswerText(a["text"])
            for b in sorted(named[a["answer_id"]]):
                mentions += 1
                w = S.build_window(a["text"], aliases[b], pat=pats[b], other=others[b], prepared=A, other_given=True)
                if w is None:
                    misses.append({"set": spec["set"], "answer_id": a["answer_id"], "brand": b})
                    continue
                windows += 1
                units.append(S._unit(spec, a, b, canon_of[b], "mention", w, len(w) >= S.WINDOW_CHAR_CAP,
                                     S.is_bare(w, pats[b])))
        per_set[spec["set"]] = {"answers_with_text": len(answers), "expected_answers": EXPECTED_ANSWERS_PER_SUB,
                                "mentions": mentions, "windows": windows, "misses": mentions - windows,
                                "miss_share": (mentions - windows) / mentions if mentions else 0.0, **crec}
    over = {s: r["miss_share"] for s, r in per_set.items() if r["miss_share"] > S.EXTRACTION_MISS_HALT_SHARE}
    if over:
        raise Halt(f"extraction misses above 5% of a set's mentions: {over}")
    kept = {u["unit_id"] for u in S.cap_windows(units)}
    for u in units:
        u["judged"] = u["unit_id"] in kept
    judged = [u for u in units if u["judged"]]
    sc = set(S.selfcon_sample(judged))
    for u in units:
        u["j2"] = u["judged"]
        u["selfcon"] = u["unit_id"] in sc
        u["human"] = False
    for s, r in per_set.items():
        us = [u for u in units if u["set"] == s]
        r.update(units_judged=sum(u["judged"] for u in us), capped_out=sum(not u["judged"] for u in us),
                 bare=sum(u["bare"] for u in us if u["judged"]), at_window_cap=sum(u["cut"] for u in us if u["judged"]))
    log(f"[v1.15] U0: {len(units)} windows, {len(judged)} judged, {len(misses)} misses, self-consistency {len(sc)}")
    return {"units": sorted(units, key=lambda u: u["unit_id"]), "misses": misses, "per_set": per_set}


def run_build_units(raw_ref: str, coded_ref: str, out: Path = PREREG_DIR, log=print) -> dict:
    read: List[dict] = []
    raw, blob = git_bytes(raw_ref, V042_RAW_PATH)
    logged(read, raw_ref, V042_RAW_PATH, raw, blob)
    answers, drop = t4_answers(parse_jsonl(raw))
    coded = {}
    for short, sub in SUB_MAP.items():
        p = V042_CODED.format(sub=short)
        data, b = git_bytes(coded_ref, p)
        logged(read, coded_ref, p, data, b)
        coded[sub] = parse_csv(data)
    ctx = type("Ctx", (), {"path": staticmethod(lambda rel: ROOT / rel)})()
    res = build_units_t4(answers, coded, ctx, log)
    return write_u0(res, drop, read, out, log)


def write_u0(res: dict, drop: dict, read: List[dict], out: Path, log=print) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    ub = S.units_csv_bytes(res["units"])
    (out / UNITS_NAME).write_bytes(ub)
    judged = [u for u in res["units"] if u["judged"]]
    doc = {"phase": PHASE_ID, "kind": "U0 on t4 (no model call, no valence, no P, C* or R)", "created_utc": _now(),
           "inputs_read": read, "drop_rule_S0": drop, "scorer_sha256": V.sha256(Path(__file__)),
           "units_file": {"path": UNITS_NAME, "sha256": V.sha256_bytes(ub), "rows": len(res["units"])},
           "units": {"windows": len(res["units"]), "judged": len(judged), "capped_out": len(res["units"]) - len(judged),
                     "denon_judged": sum(1 for u in judged if (u["category"], u["brand"]) == DENON)},
           "samples": {"J2_total": sum(u["j2"] for u in judged), "selfcon": sum(u["selfcon"] for u in judged)},
           "calls_planned": {"J1": len(judged) + sum(u["selfcon"] for u in judged),
                             "J2": len(judged) + sum(u["selfcon"] for u in judged)},
           "tokens": S.token_summary(res["units"])["F"], "per_set": res["per_set"],
           "extraction_misses": res["misses"], "seeds": {k: S.SEEDS[k] for k in ("window_cap", "selfcon", "unit_order")}}
    (out / U0_NAME).write_text(json.dumps(V._clean(doc), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    log(f"[v1.15] U0 written ({doc['units_file']['sha256'][:16]}...)")
    return doc


# ----------------------------------------------------------------------------------------------- cost (section 7)
def cost_scenarios(windows: int, tokens_in: float, r: float, selfcon_share: float = S.SELFCON_SHARE) -> dict:
    """v1.11's planning model (section 7): o200k tokens x vendor factor (1.30 Anthropic, 1.10 OpenAI); output =
    100 visible + r reasoning tokens; batch prices; both judges on every unit plus the 5% repeat; x 1.15 overhead."""
    calls = windows + S._k_of(selfcon_share, windows)
    out = {"windows": windows, "calls_per_judge": calls, "tokens_in_o200k": tokens_in, "reasoning": r}
    tot = 0.0
    for role in ("J1", "J2"):
        j = S.JUDGES[role]
        pin, pout = S.PRICES_BATCH[j["model_id"]]
        tin = tokens_in * S.TOKEN_FACTOR[j["provider"]]
        usd = calls * (tin * pin + (S.PLAN_OUT_VISIBLE + r) * pout) / 1e6
        out[role] = {"model": j["model_id"], "batch_price": [pin, pout], "usd": usd}
        tot += usd
    out["usd"], out["usd_with_overhead"] = tot, tot * S.COST_OVERHEAD
    return out


def cost_report(v111_prereg: Path = ROOT / "osf/methodology/v1_11/prereg") -> dict:
    tc = json.loads((v111_prereg / "token_counts_v1_11.json").read_text(encoding="utf-8"))
    u0 = json.loads((v111_prereg / "u0_v1_11.json").read_text(encoding="utf-8"))
    f_mean = tc_f_mean(tc)
    f_windows = u0["units"]["by_block"]["F"]
    density = f_windows / 540.0                         # v1.11 F: 540 omnibus answers with text (section 2)
    answers = 3 * 30 * 3                                 # t4 S0 category answers (v0.42 design)
    wide = 1050                                          # Preview section 12 bound (window at the 1,500-char cap)
    rows = []
    for name, w in (("archived density", round(answers * density)), ("cap binds for all 112 units", 112 * S.K_CAP_PER_BRAND)):
        for tin in (f_mean, wide):
            for r in (0, 176, S.PLAN_REASONING, 375):
                rows.append({"scenario": name, **cost_scenarios(w, tin, r)})
    return {"inputs": {"v1_11_F_windows": f_windows, "v1_11_F_answers": 540, "windows_per_answer": density,
                       "t4_S0_category_answers": answers, "F_mean_request_tokens_o200k": f_mean,
                       "prices_batch": {S.JUDGES[r]["model_id"]: S.PRICES_BATCH[S.JUDGES[r]["model_id"]] for r in ("J1", "J2")},
                       "token_factor": S.TOKEN_FACTOR, "overhead": S.COST_OVERHEAD, "selfcon_share": S.SELFCON_SHARE},
            "rows": rows, "hard_cap_usd": S.HARD_CAP_USD, "pause_usd": S.PAUSE_USD}


def tc_f_mean(tc: dict) -> float:
    """F mean request tokens (o200k) from v1.11's token_counts file (key path fixed by its writer)."""
    for k in ("by_block", "blocks"):
        if k in tc and "F" in tc[k]:
            blk = tc[k]["F"]
            for kk in ("mean_tokens", "mean", "tokens_mean"):
                if kk in blk:
                    return float(blk[kk])
    raise Halt("F mean token count not found in token_counts_v1_11.json")


# ----------------------------------------------------------------------------------------------- Stage J
def stage_j(units: List[dict], recs: List[dict], roles: dict) -> dict:
    """v1.11 Stage J on t4: JUDGE_FAIL check (> 2% halts), S per brand (J1, n >= 6), H1_t4, self-consistency."""
    oc = S.outcomes(recs, roles)
    fc = S.fail_check(units, oc, roles)
    h1 = S.h1_block(units, oc)
    h1_sd = S.h1_block(units, oc, keep=lambda u: (u["category"], u["brand"]) != DENON)
    s1 = S.score_map(units, oc, "J1")
    return {"fail_check": fc, "H1_t4": h1, "H1_t4_SD": h1_sd, "selfcon": S.selfcon_block(units, oc),
            "S_t4": {f"{k[2]}|{k[3]}": v for k, v in sorted(s1.items())}}


def own_checks(stage_j_res: dict, extraction_ok: bool = True) -> str:
    """Section 5.3: the 'own checks' the Preview requires (its section 4.1). OK if no halt fired and H1_t4 is
    CONFIRMED; FLAGGED if H1_t4 is MARGINAL; FAILED if H1_t4 is FALSIFIED or UNDETERMINED or a halt fired."""
    if not extraction_ok or stage_j_res["fail_check"].get("halt"):
        return "FAILED"
    v = stage_j_res["H1_t4"]["verdict"]
    return {"CONFIRMED": "OK", "MARGINAL": "FLAGGED"}.get(v, "FAILED")


# ----------------------------------------------------------------------------------------------- Stage C
def single_wave(S_map: Dict[str, dict], Y: Dict[str, Optional[float]], keep=None) -> dict:
    """v1.11's per-wave statistic and band at the one t4 wave (section 5.2): |rho_w(S, Y)| over units rated on
    both, groups = substrate (>= 4 units each), >= 20 units from >= 3 substrates, else UNDETERMINED."""
    ks = sorted(k for k, v in S_map.items() if v["rated"] and Y.get(k) is not None and math.isfinite(Y[k])
                and (keep is None or keep(k)))
    r = S.pooled_test([Y[k] for k in ks], [S_map[k]["S"] for k in ks], [k.split("|")[0] for k in ks],
                      boot_seed=SEED_BOOT)
    r["verdict"] = S.band_verdict(abs(r["rho"])) if r["determinable"] else "UNDETERMINED"
    r["rule"] = "single wave: v1.11 per-wave band (three-wave aggregation not applicable at t4)"
    return r


def mnp_t4(answers_by_sub: Dict[str, List[dict]], ctx) -> Dict[str, dict]:
    """H5's R* exactly as v1.11 defines it: v1.10's selected statistic MNP, lead-item extractor, floor 6, computed
    with v1.10's own functions on the same t4 S0 category answers (section 5.2)."""
    out = {}
    for sub, answers in answers_by_sub.items():
        reg, unit, _n = V.load_registry(ctx, *V.OMNI_REG[sub])
        pats = V.compile_registry(reg)
        infos = [V.extract_answer(a, pats, unit) for a in answers]
        spec = {"set": f"F t4 {sub}", "role": "omni"}
        rows = V.rank_rows({spec["set"]: {"spec": spec, "infos": infos}}, "lead_item")
        for (_p, _w, cat, b), v in V.score_units(rows).items():
            out[f"{cat}|{b}"] = {"R": v["MNP"], "rated": bool(v["rated"]), "n_ranked": v["n_ranked"]}
    return out


def gate_reading(v: Dict[str, str]) -> str:
    """The Preview's section 4.1 reading, applied to the t4 verdicts for information (section 5.4)."""
    keys = ["H1", "H2", "H3", "H4", "H5"]
    if any(v.get(k) == "FALSIFIED" for k in keys):
        return "FAIL"
    if any(v.get(k) in ("UNDETERMINED", "NOT_TESTABLE_ONE_WAVE") for k in keys):
        return "UNDETERMINED"
    if all(v.get(k) == "CONFIRMED" for k in keys if k != "H5") and v.get("H5") in ("CONFIRMED", "PENDING"):
        return "PASS" if v.get("H5") == "CONFIRMED" else "PASS, Ranking leg pending"
    return "MARGINAL"


def verdicts_t4(h1: str, h2: str, h3: str, h5: str) -> dict:
    raw = {"H1": h1, "H2": h2, "H3": h3, "H4": "NOT_TESTABLE_ONE_WAVE", "H5": h5}
    guarded, on = S.apply_noise_guard(raw)
    return {"raw": raw, "after_noise_guard": guarded, "noise_guard_on": on, "gate_reading_t4": gate_reading(guarded)}


# ----------------------------------------------------------------------------------------------- lock
LOCK_FILES = [
    "osf/methodology/v1_15/prereg/PRE_REGISTRATION_v1_15.md",
    "osf/methodology/v1_15/prereg/cost_estimate_v1_15.json",
    "osf/methodology/v1_15/prereg/coi_screen_v1_15.json",
    "osf/methodology/v1_15/scripts/score_v1_15.py",
    "osf/methodology/v1_15/scripts/judge_v1_15.py",
    "osf/methodology/v1_15/scripts/coi_screen_v1_15.py",
    "osf/methodology/v1_15/scripts/tests/test_v1_15.py",
    "osf/methodology/v1_15/anchor/DEVIATIONS.md",
    "scripts/score_v1_11.py",
    "scripts/judge_v1_11.py",
    "scripts/score_v1_10.py",
    "osf/methodology/v1_11/prereg/judge_prompt_v1_11.md",
    "osf/methodology/v1_11/prereg/token_counts_v1_11.json",
    "osf/methodology/v1_11/prereg/u0_v1_11.json",
]
LOCK_MANIFEST_FILE = PREREG_DIR / "LOCK_MANIFEST_v1_15.sha256"


def lock_manifest_text(root: Path = ROOT) -> str:
    return "".join(f"{hashlib.sha256((root / p).read_bytes()).hexdigest()}  {p}\n" for p in LOCK_FILES)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cost", action="store_true")
    ap.add_argument("--build-units", action="store_true")
    ap.add_argument("--raw-ref", default=V042_RAW_TAG)
    ap.add_argument("--coded-ref")
    ap.add_argument("--lock-manifest", action="store_true")
    a = ap.parse_args(argv)
    if a.cost:
        rep = cost_report()
        (PREREG_DIR / "cost_estimate_v1_15.json").write_text(json.dumps(rep, indent=2) + "\n", encoding="utf-8")
        for r in rep["rows"]:
            print(f"{r['scenario']:30s} w={r['windows']:5d} calls/judge={r['calls_per_judge']:5d} "
                  f"in={r['tokens_in_o200k']:7.1f} r={r['reasoning']:3d}  ${r['usd_with_overhead']:7.2f}")
        return 0
    if a.build_units:
        if not a.coded_ref:
            ap.error("--coded-ref (the v0.42 commit holding osf/v42/data/coded/) is required")
        run_build_units(a.raw_ref, a.coded_ref)
        return 0
    if a.lock_manifest:
        LOCK_MANIFEST_FILE.write_text(lock_manifest_text(), encoding="utf-8")
        print(f"wrote {LOCK_MANIFEST_FILE} ({len(LOCK_FILES)} files)")
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
