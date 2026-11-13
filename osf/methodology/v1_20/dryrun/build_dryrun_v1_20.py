#!/usr/bin/env python3
"""Builds the SYNTHETIC dry-run work folder of v1.20 (osf/methodology/v1_20/dryrun/work/; not committed).
No model call, no network, no real judge reply (none exists before 2026-11-22), no real answer text.

  1. v1.11's synthetic input replica, its dry-run manifest and v1.11's dry-run U0 (unit table and u0
     record), copied from a v1.11 dry-run folder made by v1.11's own locked builder
     (osf/methodology/v1_11/dryrun/build_dryrun_v1_11.py) and `score_v1_11.py --build-units --dry-run`.
     Default source: the v1.11 worktree's osf/methodology/v1_11/dryrun/. v1.11's loaders check their
     SHA-256 at Stage J and C (unit table against the u0 record; replica files against the manifest).
  2. Synthetic judge records in v1.11's raw-record format, made under v1.11's retry discipline: a unit
     is asked again only after a reply that v1.11's parser rejects, at most 1 + 2 replies. Reply
     formats are drawn by hash: bare object, fenced object, prose before the object, prose before a
     fenced object, text after, two objects, an object cut off at the output cap, a complete object
     with a cap finish reason, wrong keys, no JSON; plus served-model mismatches, API errors and a few
     units left after two invalid replies (a stopped run). Scenario B gives J1 a high prose rate in one
     set (OMNI t2 v0.21), so v1.11's rule halts there; scenario A does not, and v1.11's own Stage J is
     then run on the records (v1.20 requires it first); scenario H gives that set replies with no JSON,
     so both rules halt. Valences are a hash-seeded synthetic latent.
  3. The frozen record judge_outputs_frozen_v1_11.json over those records (the fields the scorers read).
  4. A synthetic cut list in the format of scoping/cut_units_v1_20.csv / .json: every t3 recognition
     answer of gemini-2.5-flash, about 2 in 3 t3 v0.19 gemini-2.5-flash-lite answers, every t3 v0.23
     gemini-2.5-flash answer; S-CUT-M cells by the section 8 rule (at least half of t3 answers cut).

Run (repository root): python3 osf/methodology/v1_20/dryrun/build_dryrun_v1_20.py [--from DIR] [--scenario A|B]
Then: python3 scripts/score_v1_20.py --stage J --dry-run
      python3 scripts/score_v1_20.py --stage C --dry-run --draws 500
"""
import argparse
import csv
import hashlib
import json
import shutil
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts"))
import score_v1_11 as S   # noqa: E402
import score_v1_20 as R   # noqa: E402

DEFAULT_FROM = ROOT.parent / "v1.11" / "osf/methodology/v1_11/dryrun"
HALT_SET = "OMNI t2 v0.21"
PROSE = ["Here is my rating.\n\n", "Rating below.\n", "Based on the text, my assessment is:\n"]


def h01(*a) -> float:
    return int(hashlib.sha256("|".join(map(str, a)).encode()).hexdigest()[:8], 16) / 0xFFFFFFFF


def judgement(role, u, k) -> dict:
    uid = u["unit_id"]
    refers = h01("ref", uid) > 0.01
    lat = h01("brand", u["category"], u["brand"]) * 2.0 - 0.5
    v = int(round(max(-2.0, min(2.0, lat + (0.2 if role == "J2" else 0.0) + (h01("noise", role, uid, k) - 0.5) * 1.4))))
    ev = refers and (v != 0 or h01("ev", role, uid, k) < 0.3)
    v = v if ev else 0
    return {"refers_to_brand": refers, "evaluative": ev, "mixed": bool(ev and h01("mx", role, uid, k) < 0.1),
            "valence": v, "evidence": "synthetic quote" if ev else ""}


def weights(role, u, scenario):
    if role == "J2":
        return [("bare", .985), ("text_after", .004), ("no_json", .004), ("two_objects", .002), ("cut_at_cap", .002),
                ("wrong_keys", .002), ("cap_complete", .001)]
    if scenario == "B" and u["set"] == HALT_SET:
        return [("bare", .60), ("prose_before", .30), ("prose_before_fenced", .08), ("no_json", .01),
                ("fenced", .01)]
    if scenario == "H" and u["set"] == HALT_SET:      # replies with no JSON: both rules halt
        return [("bare", .60), ("no_json", .38), ("fenced", .02)]
    return [("bare", .90), ("fenced", .02), ("prose_before", .045), ("prose_before_fenced", .015), ("text_after", .005),
            ("two_objects", .003), ("cut_at_cap", .002), ("cap_complete", .001), ("wrong_keys", .002), ("no_json", .007)]


def reply(fmt, role, u, k):
    """(text, finish_reason) of one synthetic reply."""
    obj = judgement(role, u, k)
    js = json.dumps(obj)
    end = "end_turn" if role == "J1" else "completed"
    cap = "max_tokens" if role == "J1" else "incomplete:max_output_tokens"
    p = PROSE[int(h01("p", u["unit_id"], k) * len(PROSE)) % len(PROSE)]
    if fmt == "bare":
        return js, end
    if fmt == "fenced":
        return "```json\n" + js + "\n```", end
    if fmt == "prose_before":
        return p + js, end
    if fmt == "prose_before_fenced":
        return p + "```json\n" + js + "\n```", end
    if fmt == "text_after":
        return js + "\nThe text is mostly descriptive.", end
    if fmt == "two_objects":
        return js + "\n" + json.dumps({**obj, "evidence": "another quote"}), end
    if fmt == "cut_at_cap":
        return p + js[: len(js) // 2], cap
    if fmt == "cap_complete":
        return js, cap
    if fmt == "wrong_keys":
        return json.dumps({**obj, "confidence": 0.8}), end
    return "I would describe this mention as favourable overall.", end


def pick(ws, *key):
    x, acc = h01(*key), 0.0
    for name, w in ws:
        acc += w
        if x < acc:
            return name
    return ws[0][0]


def v111_ok(text) -> bool:
    try:
        S.parse_judge_output(text)
        return True
    except S.JudgeOutputError:
        return False


def records_for(role, model, provider, pas, u, scenario, t0):
    out, received = [], 0
    for attempt in range(1, 1 + 1 + S.MAX_PARSE_RETRIES):
        base = {"phase_id": "v1.11", "call_id": f"{role}|{u['unit_id']}|{pas}|{attempt}", "role": role,
                "judge_model": model, "provider": provider, "unit_id": u["unit_id"], "pass": pas,
                "plan_phase": "synthetic", "attempt": attempt, "synthetic": True, "mode": "batch"}
        if h01("apierr", role, u["unit_id"], pas, attempt) < 0.001:
            out.append({**base, "status": "error", "valid": False, "text": None, "served_model": None, "served_ok": False,
                        "finish_reason": None, "error": "synthetic API error", "started_utc": f"{t0}{attempt}0"})
        fmt = pick(weights(role, u, scenario), "fmt", role, u["unit_id"], pas, attempt)
        text, fr = reply(fmt, role, u, attempt)
        served_ok = h01("served", role, u["unit_id"], pas, attempt) >= 0.002
        valid = served_ok and v111_ok(text)
        out.append({**base, "status": "ok", "valid": valid, "format": fmt, "text": text,
                    "served_model": model if served_ok else "some-other-model", "served_ok": served_ok,
                    "finish_reason": fr, "error": None, "started_utc": f"{t0}{attempt}5"})
        received += 1
        if valid:
            break
        if received == 2 and h01("stopped", role, u["unit_id"], pas) < 0.002:
            break      # a run stopped after two invalid replies: UNJUDGED under v1.11
    return out


def build(src: Path, scenario: str) -> dict:
    W = R.DRY_WORK
    if W.exists():
        shutil.rmtree(W)
    W.mkdir(parents=True)
    shutil.copytree(src / "replica", R.DRY_REPLICA)
    shutil.copy2(src / "INPUTS_MANIFEST_dryrun_v1_11.json", R.DRY_MANIFEST)
    R.DRY_V111_OUT.mkdir(parents=True)
    for n in ("u0_v1_11.json", "units_v1_11.csv"):
        shutil.copy2(src / "outputs" / n, R.DRY_V111_OUT / n)
    u0 = json.loads((R.DRY_V111_OUT / "u0_v1_11.json").read_text(encoding="utf-8"))
    units = S.effective_units(S.read_units(R.DRY_V111_OUT / "units_v1_11.csv"))
    roles = {"J1": "claude-opus-5-5", "J2": "gpt-6.1-sol"}
    prov = {"J1": "anthropic", "J2": "openai"}
    recs = []
    for i, u in enumerate(sorted((u for u in units if u["judged"]), key=lambda u: u["unit_id"])):
        t0 = f"2026-11-22T06:{(i // 600) % 60:02d}:{(i // 10) % 60:02d}.{i % 10}"
        jobs = [("J1", "main")] + ([("J2", "main")] if u["j2"] else [])
        jobs += [("J1", "repeat")] if u["selfcon"] else []
        jobs += [("J2", "repeat")] if (u["selfcon"] and u["j2"]) else []
        for role, pas in jobs:
            recs += records_for(role, roles[role], prov[role], pas, u, scenario, t0)
    raw = R.DRY_V111_OUT / S.RAW_NAME
    raw.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in recs), encoding="utf-8")
    frozen = {"phase": "v1.11", "dry_run": True, "synthetic_for": "v1.20 dry run (build_dryrun_v1_20.py)",
              "scenario": scenario, "raw_file": S.RAW_NAME, "raw_sha256": S.V.sha256(raw), "records": len(recs),
              "roles": roles, "replacements": [], "plan_params": dict(S.DEFAULT_PLAN),
              "units_sha256": u0["units_file"]["sha256"]}
    (R.DRY_V111_OUT / S.FROZEN_NAME).write_text(json.dumps(frozen, indent=2) + "\n", encoding="utf-8")
    # synthetic cut list (format of scoping/cut_units_v1_20.*)
    answers = {}
    for u in units:
        answers.setdefault(u["answer_id"], u)
    rows = []
    for aid, u in sorted(answers.items()):
        cell = (u["block"], u["wave"], u["category"], u["model"])
        if (cell == ("R", "t3", "v0.23", "gemini-2.5-flash") or cell == ("F", "t3", "v0.23", "gemini-2.5-flash")
                or (cell == ("F", "t3", "v0.19", "gemini-2.5-flash-lite") and h01("cut", aid) < 0.67)):
            rows.append({"block": u["block"], "wave": u["wave"], "category": u["category"], "model": u["model"],
                         "answer_id": aid, "evidence_class": "synthetic", "unit_status": "kept"})
    with open(R.DRY_CUT_CSV, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    t3 = Counter((u["block"], u["category"], u["model"]) for u in answers.values() if u["wave"] == "t3")
    cut3 = Counter((r["block"], r["category"], r["model"]) for r in rows if r["wave"] == "t3")
    cells = sorted([list(c) for c, n in cut3.items() if n * 2 >= t3[c]])
    R.DRY_CUT_JSON.write_text(json.dumps({"synthetic": True, "s_cut_m_cells": cells,
                                          "rule": "cells with at least half of their t3 answers cut"}, indent=2) + "\n",
                              encoding="utf-8")
    fmt = Counter((r["role"], r.get("format", r["status"])) for r in recs)
    info = {"scenario": scenario, "records": len(recs), "raw_sha256": frozen["raw_sha256"],
            "formats": {f"{k[0]} {k[1]}": v for k, v in sorted(fmt.items())},
            "cut_answers": len(rows), "s_cut_m_cells": cells}
    if scenario == "A":
        ctx = S.make_ctx(True, root=R.DRY_REPLICA, manifest=R.DRY_MANIFEST, outdir=R.DRY_V111_OUT)
        S.run_stage_j(ctx)       # v1.11's own Stage J first (v1.20 requires it in case A)
        info["v1_11_stage_j"] = "run"
    return info


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="src", default=str(DEFAULT_FROM),
                    help="a v1.11 dry-run folder with replica/, INPUTS_MANIFEST_dryrun_v1_11.json and outputs/u0, units")
    ap.add_argument("--scenario", choices=["A", "B", "H"], default="B",
                    help="A: v1.11's rule passes; B (default): v1.11's rule halts, v1.20's does not; H: both halt")
    a = ap.parse_args()
    info = build(Path(a.src), a.scenario)
    print(json.dumps(info, indent=1))


if __name__ == "__main__":
    main()
