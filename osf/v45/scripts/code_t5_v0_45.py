#!/usr/bin/env python3
"""
code_t5_v0_45.py -- AIAS(TM) v0.45 (t5): codes the t5 answers with v0.42's certified coder, unchanged, and replaces the
v0.23 recognition judge (Claude Sonnet 4.5, retiring 2026-11-30) by a pre-registered successor (section 5.1).

Coder. `osf/v42/scripts/code_t4_v0_42.py` is imported as is; its git blob must equal the pin of v0.42 (2d36735d...,
checked at import by `coder_blob_ok`). Mentions (Phase B), URL removal and the v0.19-v0.22 yes/no parsers are exactly
t4's. v0.23 Phase A is coded by `score_v0_23.score_phase_a` (same system prompt, same user template, same 3,000-
character truncation, same R0-R3 regex) through a client proxy that swaps the judge model:

  claude-sonnet-5-5 (Anthropic's recommended replacement for claude-sonnet-4-5-20250929; model deprecations page, read
    2026-11-10). Its model page says temperature/top_p/top_k "returns a 400 error" and adaptive thinking is on by
    default; its migration guide says thinking counts against max_tokens and gives `thinking: {"type": "between_tools"}`
    as the lowest setting (no up-front thinking without tools). The proxy therefore drops temperature, sends
    thinking {"type": "between_tools"} and output_config {"effort": "low"} (in extra_body), keeps max_tokens 10, and
    returns the first TEXT block (v0.23's code reads content[0]).
  claude-sonnet-4-6 (fallback; Active, not sooner than 2027-02-17): the v0.23 call unchanged except the model ID
    (temperature 0.0, max_tokens 10). Whether it accepts temperature is NOT verified (no vendor page read says so);
    if it errors, the judge returns R_ERR and the candidate fails J1.

J1 (judge parity, section 5.1): before any t5 answer is coded, the candidate judges the 144 t3 and the 72 t4 v0.23
Phase A answers whose Sonnet 4.5 codes are locked (t3: osf/v41/data/v23/v23_phase_a_scored.json; t4: v0.42's coded
Phase A table). PASS iff binary agreement (r_level_to_binary) >= 0.95 over all answers judged AND >= 0.90 on the t4
subset, with no R_ERR left. Candidates in order: claude-sonnet-5-5, then claude-sonnet-4-6; the first that passes is the
t5 judge and also re-codes the t4 v0.23 answers (judge held constant across waves for the Presence comparison).
No candidate passes: v0.23 recognition is not coded at t5 (section 5.4).

NEVER calls a model API unless --judge / --parity is given (both refuse before the lock; tests use fakes only).
Modes: --code RAW OUTDIR [--judge MODEL] | --parity MODEL --t4-raw FILE --t4-coded DIR (J1 record in
osf/v45/data/judge_parity_J1_v0_45.json: every run, and the first passing candidate with its t4 codes)
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace as NS

HERE = Path(__file__).resolve().parent
V42_SCRIPTS = HERE.parents[1] / "v42" / "scripts"
sys.path.insert(0, str(V42_SCRIPTS))
import code_t4_v0_42 as C   # noqa: E402  (bootstraps ROOT and the certified modules' paths)

ROOT = C.ROOT
CODER_BLOB_PIN = "2d36735d512cf9e13b74010ba5a7f655fc7de0bc"
PREREG_TAG = "v0.45-prereg-r1"
REAL_RAW = ROOT / "osf/v45/data/t5_raw.jsonl"
PROBES_PATH = ROOT / "osf/v45/prereg/probes_v0_45.jsonl"
DEFAULT_OUT = ROOT / "osf/v45/data/coded"
J1_PATH = ROOT / "osf/v45/data/judge_parity_J1_v0_45.json"
CANDIDATES = ["claude-sonnet-5-5", "claude-sonnet-4-6"]
J1_ALL, J1_T4 = 0.95, 0.90


def coder_blob_ok(path=V42_SCRIPTS / "code_t4_v0_42.py"):
    data = Path(path).read_bytes()
    blob = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
    return blob == CODER_BLOB_PIN, blob


class SuccessorJudgeClient:
    """Anthropic-like client proxy for score_v0_23.judge_recognition. `inner` is a real anthropic.Anthropic() or a
    fake; every request and its usage are logged in self.log (for costing, section 4.5)."""

    def __init__(self, inner, model):
        if model not in CANDIDATES:
            raise ValueError(f"not a pre-registered successor judge: {model}")
        self.inner, self.model, self.log = inner, model, []
        self.messages = self

    def request(self, **kw):
        """The request actually sent, from v0.23's kwargs (model, max_tokens, temperature, system, messages)."""
        if self.model == "claude-sonnet-5-5":
            return {"model": self.model, "max_tokens": kw["max_tokens"], "system": kw["system"],
                    "messages": kw["messages"],
                    "extra_body": {"thinking": {"type": "between_tools"}, "output_config": {"effort": "low"}}}
        return {**kw, "model": self.model}

    def create(self, **kw):
        req = self.request(**kw)
        resp = self.inner.messages.create(**req)
        blocks = list(getattr(resp, "content", []) or [])
        text = next((b.text for b in blocks if getattr(b, "type", "text") == "text" and hasattr(b, "text")), "")
        u = getattr(resp, "usage", None)
        self.log.append({"model": self.model, "input_tokens": getattr(u, "input_tokens", None),
                         "output_tokens": getattr(u, "output_tokens", None),
                         "stop_reason": getattr(resp, "stop_reason", None), "text": text[:20]})
        return NS(content=[NS(type="text", text=text)], usage=u)


def judge_records(recs, client):
    """recs: v23-format Phase A records (status, response, brand_id, brand_name, spirit_type, model_slot, ...)."""
    return C.code_v23_phase_a(recs, client)


def agreement(pairs):
    """pairs: [(locked_level, new_level)] -> binary and exact agreement over pairs with a locked code."""
    n = b = e = err = 0
    for old, new in pairs:
        ob = C.r_level_to_binary(old)
        if ob is None:
            continue
        nb = C.r_level_to_binary(new)
        n += 1
        err += nb is None
        b += int(nb is not None and nb == ob)
        e += int(str(new).upper() == str(old).upper())
    return {"n": n, "binary_agree": b, "binary_share": b / n if n else None, "exact_agree": e,
            "exact_share": e / n if n else None, "r_err": err}


def j1_verdict(t3, t4):
    tot_n, tot_b = t3["n"] + t4["n"], t3["binary_agree"] + t4["binary_agree"]
    share = tot_b / tot_n if tot_n else None
    ok = (share is not None and share >= J1_ALL and t4["n"] > 0 and t4["binary_share"] >= J1_T4
          and t3["r_err"] + t4["r_err"] == 0)
    return {"binary_share_all": share, "n_all": tot_n, "pass": bool(ok),
            "rule": f"binary agreement >= {J1_ALL} over all AND >= {J1_T4} on t4, no R_ERR"}


def t3_v23_records():
    """t3 v0.23 Phase A answers and their locked Sonnet 4.5 levels (v0.41)."""
    calls, scored = C._t3_raw_calls()
    recs = [{"status": "ok", "response": r["response"], "brand_id": r["brand_id"], "brand_name": r["brand_name"],
             "spirit_type": r["spirit_type"], "model_slot": r.get("model_id"), "model_id": r.get("model_id"),
             "_locked": r["r_level"]} for r in scored if r.get("status") == "ok" and (r.get("response") or "").strip()]
    return recs


def t4_v23_records(t4_calls, t4_A, probes):
    """t4 v0.23 Phase A answers (raw) joined to v0.42's coded label (Sonnet 4.5 at t4)."""
    lab = {r["call_id"]: r["label"] for r in t4_A if r["substrate"] == "v0.23"}
    out = []
    for r in t4_calls:
        if r["substrate"] != "v23" or r["phase"] != "A" or not C.is_answered(r) or r["call_id"] not in lab:
            continue
        p = probes.get(("v23", "A", r["probe_id"]), {})
        out.append({"status": "ok", "response": r["text"], "brand_id": r["brand_id"],
                    "brand_name": r.get("brand") or p.get("brand", ""), "spirit_type": r.get("spirit_type") or p.get("spirit_type", ""),
                    "model_slot": r["model_requested"], "model_id": r["model_requested"], "_locked": lab[r["call_id"]],
                    "_call_id": r["call_id"]})
    return out


def run_j1(model, inner, t3_recs, t4_recs):
    client = SuccessorJudgeClient(inner, model)
    res = {}
    for name, recs in (("t3", t3_recs), ("t4", t4_recs)):
        scored = judge_records([{k: v for k, v in r.items() if not k.startswith("_")} for r in recs], client)
        res[name] = agreement([(r["_locked"], s.get("r_level")) for r, s in zip(recs, scored)])
        if name == "t4":
            res["t4_codes"] = {r["_call_id"]: s.get("r_level") for r, s in zip(recs, scored)}
    res["verdict"] = j1_verdict(res["t3"], res["t4"])
    res["judge"] = model
    res["requests"] = len(client.log)
    return res


def code_t5(calls, judge_model=None, inner=None, probes=None):
    """Code t5 calls (deduped) with v0.42's coder; v0.23 Phase A with the successor judge (or not coded)."""
    probes = probes if probes is not None else C.load_probe_map(PROBES_PATH)
    client = SuccessorJudgeClient(inner, judge_model) if judge_model else None
    return C.code_calls(calls, probes, strip=True, judge_client=client)


def tag_on_origin():
    r = subprocess.run(["git", "-C", str(ROOT), "ls-remote", "--tags", "origin", PREREG_TAG], capture_output=True,
                       text=True, timeout=60)
    return r.returncode == 0 and f"refs/tags/{PREREG_TAG}" in r.stdout


def parity_main(model, t4_raw, t4_coded, out=J1_PATH):
    """J1 with the real judge API (after the lock only). Candidates are tried in CANDIDATES order by the caller."""
    if not tag_on_origin():
        print(f"[v45] REFUSED: tag {PREREG_TAG} not on origin; J1 makes paid calls only after the lock", file=sys.stderr)
        return 3
    import anthropic
    t4_calls = C.dedupe_calls(C.read_raw(t4_raw))
    A4, _ = C.read_tables(t4_coded)
    res = run_j1(model, anthropic.Anthropic(), t3_v23_records(), t4_v23_records(t4_calls, A4, C.load_probe_map(PROBES_PATH)))
    hist = json.loads(Path(out).read_text(encoding="utf-8")) if Path(out).exists() else {"runs": []}
    hist["runs"].append(res)
    if res["verdict"]["pass"] and not hist.get("judge"):
        hist.update({"judge": model, "verdict": res["verdict"], "t4_codes": res["t4_codes"]})
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(json.dumps(hist, indent=2), encoding="utf-8")
    print(f"J1 {model}: {'PASS' if res['verdict']['pass'] else 'FAIL'} {res['verdict']} -> {out}")
    return 0 if res["verdict"]["pass"] else 2


def main():
    import argparse
    ap = argparse.ArgumentParser(description="AIAS v0.45 t5 coder (v0.42's coder + successor v0.23 judge)")
    ap.add_argument("--code", nargs=2, metavar=("RAW", "OUTDIR"))
    ap.add_argument("--judge", choices=CANDIDATES, default=None)
    ap.add_argument("--parity", choices=CANDIDATES, default=None, help="run J1 for one candidate (paid; after the lock)")
    ap.add_argument("--t4-raw", default=None)
    ap.add_argument("--t4-coded", default=None)
    a = ap.parse_args()
    ok, blob = coder_blob_ok()
    if not ok:
        print(f"[v45] HALT: v0.42 coder blob {blob} != pin {CODER_BLOB_PIN}", file=sys.stderr)
        return 4
    if a.parity:
        if not (a.t4_raw and a.t4_coded):
            ap.error("--parity needs --t4-raw and --t4-coded")
        return parity_main(a.parity, a.t4_raw, a.t4_coded)
    if not a.code:
        ap.error("--code RAW OUTDIR")
    raw, out = Path(a.code[0]), Path(a.code[1])
    if raw.resolve() == REAL_RAW.resolve() and not tag_on_origin():
        print(f"[v45] REFUSED: tag {PREREG_TAG} not on origin", file=sys.stderr)
        return 3
    inner = None
    if a.judge:
        if raw.resolve() != REAL_RAW.resolve():
            ap.error("--judge only on the real t5 file (tests use fakes)")
        j1 = json.loads(J1_PATH.read_text(encoding="utf-8")) if J1_PATH.exists() else {}
        if j1.get("judge") != a.judge:
            print(f"[v45] REFUSED: {a.judge} has not passed J1 ({J1_PATH})", file=sys.stderr)
            return 3
        import anthropic
        inner = anthropic.Anthropic()
    A, B = code_t5(C.dedupe_calls(C.read_raw(raw)), a.judge, inner)
    C.write_tables(A, B, out)
    print(f"coded -> {out}: {len(A)} Phase A rows, {len(B)} Phase B rows" + ("" if a.judge else " (v0.23 judge OFF)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
