#!/usr/bin/env python3
"""
code_t4_v0_42.py -- AIAS(TM) v0.42 coder: t4_raw.jsonl -> per-substrate coded tables.

Implements PRE_REGISTRATION_v0_42.md section 5.1 (coding) and gate P2 (section 5.3).
Each substrate's certified t1 coding functions are used UNCHANGED:
  v0.20-v0.22  mentions : content module detect_mention (score_v20/21/22, via score_v33.RECON_CFG,
                          exactly as score_v41.load_wave / score_v0_31.counts_raw_text call it)
               recognition: parse_yes_no of the substrate's own legacy runner (run_acquisition_v20/21/22)
  v0.19        mentions : acquire_v0_19.build_brand_patterns + detect_mentions_in_response
                          (the pieces parse_phase_b uses); recognition: parse_phase_a_response
  v0.23        mentions : score_v0_23.score_phase_b (run with dry_run=True: the deterministic
                          find_brand_mentions part only; the elaboration judge is NOT called)
               recognition: score_v0_23.score_phase_a, the LLM judge -- OFF unless --judge
URLs are removed from Phase B text before matching (switch: --no-url-strip).

Outputs (one pair per substrate) in <out>/: <sub>_phase_a.csv, <sub>_phase_b.csv.
  phase_a: call_id,substrate,brand,brand_id,model,condition,run,probe_id,label,recognized
  phase_b: call_id,substrate,brand,model,condition,run,probe_id,frame_id,mentioned
One row per ANSWERED call (status ok, non-empty text) for Phase A, and per answered call x brand
for Phase B. Unanswered calls produce no rows.

NEVER calls a model API unless --judge is given (not used in tests; tests mock the client).

Modes:
  (default)      code --raw (default osf/v42/data/t4_raw.jsonl, GUARDED) into --out
  --parity-p2    gate P2 on the locked t3 raw answers; writes osf/v42/prereg/parity_P2_v0_42.json
"""
import os
import sys
import tempfile
from pathlib import Path


def _bootstrap_root():
    root = Path(os.environ.get("AIAS_ROOT", str(Path(__file__).resolve().parents[3]))).resolve()
    try:
        same = (Path.home() / "aias").resolve() == root
    except OSError:
        same = False
    if same:
        return root
    if os.environ.get("_V41_HOME_SHIM"):
        sys.exit(f"[v42] ROOT shim failed: ~/aias -> {(Path.home() / 'aias').resolve()} != {root}")
    import site
    shim = Path(tempfile.mkdtemp(prefix="v42_home_"))
    (shim / "aias").symlink_to(root)
    env = dict(os.environ, HOME=str(shim), _V41_HOME_SHIM="1", AIAS_ROOT=str(root))
    env.setdefault("PYTHONUSERBASE", site.getuserbase())
    os.execve(sys.executable, [sys.executable, os.path.abspath(sys.argv[0])] + sys.argv[1:], env)


ROOT = _bootstrap_root()
os.environ["AIAS_ROOT"] = str(ROOT)
for _p in (ROOT / "prereg", ROOT / "scripts", ROOT / "osf/v41/scripts", ROOT / "osf/v19"):
    sys.path.insert(0, str(_p))

import argparse            # noqa: E402
import collections         # noqa: E402
import contextlib          # noqa: E402
import csv                 # noqa: E402
import io                  # noqa: E402
import json                # noqa: E402
import re                  # noqa: E402
import subprocess          # noqa: E402

PREREG_TAG = "v0.42-prereg-r1"
REAL_RAW = ROOT / "osf/v42/data/t4_raw.jsonl"
PROBES_PATH = ROOT / "osf/v42/prereg/probes_v0_42.jsonl"
DEFAULT_OUT = ROOT / "osf/v42/data/coded"
P2_PATH = ROOT / "osf/v42/prereg/parity_P2_v0_42.json"
DATA3 = ROOT / "osf/v41/data"

SUB_MAP = {"v19": "v0.19", "v20": "v0.20", "v21": "v0.21", "v22": "v0.22", "v23": "v0.23"}
SUBS = list(SUB_MAP)


class Refused(RuntimeError):
    pass


# --------------------------------------------------------------------------- guard
def _ls_remote_tag():
    """Raw stdout of `git ls-remote --tags origin v0.42-prereg-r1` (separate function: tests patch it)."""
    r = subprocess.run(["git", "-C", str(ROOT), "ls-remote", "--tags", "origin", PREREG_TAG],
                       capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        raise Refused(f"git ls-remote failed ({r.stderr.strip()[:200]}); cannot verify tag {PREREG_TAG}")
    return r.stdout


def tag_on_origin():
    return f"refs/tags/{PREREG_TAG}" in _ls_remote_tag()


def guard_real_raw(path):
    """Refuse to open the real t4 raw file unless the prereg tag is on origin."""
    if Path(path).resolve() == REAL_RAW.resolve() and not tag_on_origin():
        raise Refused(f"refusing to read {REAL_RAW}: tag {PREREG_TAG} is not on origin "
                      f"(`git ls-remote --tags origin {PREREG_TAG}` found nothing)")


# --------------------------------------------------------------------------- URL removal
# Markdown links [text](target): the target is removed, the text kept. One level of balanced
# parentheses inside the target is allowed (e.g. wikipedia ..._(x)). Optional "title".
MD_LINK_RE = re.compile(
    r"\[([^\]]*)\]\(\s*(?:<[^>]*>|(?:[^()\s]|\([^()\s]*\))+)(?:\s+(?:\"[^\"]*\"|'[^']*'))?\s*\)")
URL_RE = re.compile(r"https?://[^\s<>\"'\])]+", re.I)


def strip_urls(text):
    """Remove http(s):// addresses and the targets of Markdown links (link text is kept)."""
    if not text:
        return text or ""
    t = MD_LINK_RE.sub(r"\1", text)
    return URL_RE.sub(" ", t)


# --------------------------------------------------------------------------- call handling
def read_raw(path):
    """Read a t4_raw.jsonl (guarded for the real file)."""
    guard_real_raw(path)
    out = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return out


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


def load_probe_map(path=PROBES_PATH):
    pm = {}
    for line in open(path, encoding="utf-8"):
        if line.strip():
            p = json.loads(line)
            pm[(p["substrate"], p["phase"], p["probe_id"])] = p
    return pm


# --------------------------------------------------------------------------- certified modules
_M = {}


def _modules():
    """Import the certified t1 functions once (names as score_v41.load_wave / v41_code_t3 use them)."""
    if _M:
        return _M
    import importlib
    import score_v0_31 as S31
    import score_v33 as S33
    import acquire_v0_19 as A19
    import score_v0_23 as S23
    _M.update(S31=S31, S33=S33, A19=A19, S23=S23)
    _M["parse_yes_no"] = {}
    for sub, modname in (("v0.20", "run_acquisition_v20"), ("v0.21", "run_acquisition_v21"),
                         ("v0.22", "run_acquisition_v22")):
        _M["parse_yes_no"][sub] = importlib.import_module(modname).parse_yes_no
    # brand lists + matchers
    brands = {}
    for sub, (rk, rp, mod, _pb) in S33.RECON_CFG.items():
        reg = mod.load_registry(rp) if rk == "json" else mod.load_prereg_module(rp)
        brands[sub] = [(b.get("name") if isinstance(b, dict) else b)
                       for _ck, cv in reg["cells"].items()
                       for b in (cv.get("brands", []) if isinstance(cv, dict) else cv)]
        _M.setdefault("detect", {})[sub] = mod.detect_mention
    reg19 = A19.load_registry()
    brands["v0.19"] = [r["brand"] for r in reg19]
    _M["pat19"] = A19.build_brand_patterns(reg19)
    brands["v0.23"] = [b["id"] for b in S23.REGISTRY]
    _M["brands"] = brands
    return _M


def brand_names_for(sub):
    return list(_modules()["brands"][sub])


def mentions_nonv23(sub, text):
    """{brand: 0/1} for v0.19-v0.22 by the certified matchers."""
    m = _modules()
    if sub == "v0.19":
        found = {x["brand"] for x in m["A19"].detect_mentions_in_response(text, m["pat19"])}
        return {b: int(b in found) for b in m["brands"][sub]}
    det = m["detect"][sub]
    return {b: int(bool(det(text, b))) for b in m["brands"][sub]}


def recog_label(sub, text):
    """Certified recognition parse: v0.19 -> yes/no/ambiguous (parse_phase_a_response), v0.20-22 -> parse_yes_no."""
    m = _modules()
    if sub == "v0.19":
        v = m["A19"].parse_phase_a_response(text)
        return "ambiguous" if v is None else ("yes" if v == 1 else "no")
    return m["parse_yes_no"][sub](text)


def r_level_to_binary(level):
    """score_v33.recog_v23 normalisation: R0 / '' / NONE -> 0, other levels -> 1 (R_ERR -> None, not coded)."""
    lvl = str(level or "").strip().upper()
    if lvl == "R_ERR":
        return None
    return 0 if lvl in ("", "R0", "NONE") else 1


# --------------------------------------------------------------------------- v0.23 via certified functions
def _dump_json(obj, path, **kw):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, **kw)


def _load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


@contextlib.contextmanager
def _s23_paths(tmp):
    S23 = _modules()["S23"]
    keep = {k: getattr(S23, k) for k in ("PHASE_A_RAW", "PHASE_B_RAW", "PHASE_A_SCORED", "PHASE_B_SCORED", "JUDGE_PAUSE")}
    S23.PHASE_A_RAW, S23.PHASE_B_RAW = Path(tmp) / "a_raw.json", Path(tmp) / "b_raw.json"
    S23.PHASE_A_SCORED, S23.PHASE_B_SCORED = Path(tmp) / "a_scored.json", Path(tmp) / "b_scored.json"
    S23.JUDGE_PAUSE = 0
    try:
        yield S23
    finally:
        for k, v in keep.items():
            setattr(S23, k, v)


def code_v23_phase_b(recs):
    """recs: v23-format raw records (status, response, probe_id, ...). score_phase_b with dry_run=True
    (deterministic mentions; the elaboration judge is skipped, never called). Returns scored records."""
    with tempfile.TemporaryDirectory() as tmp, _s23_paths(tmp) as S23:
        _dump_json(recs, S23.PHASE_B_RAW)
        with contextlib.redirect_stdout(io.StringIO()):
            S23.score_phase_b(None, dry_run=True)
        return _load_json(S23.PHASE_B_SCORED)


def code_v23_phase_a(recs, client):
    """recs: v23-format Phase A raw records; client: an anthropic-like client (real only with --judge,
    a mock in tests). Runs score_v0_23.score_phase_a. Returns scored records (with r_level)."""
    with tempfile.TemporaryDirectory() as tmp, _s23_paths(tmp) as S23:
        _dump_json(recs, S23.PHASE_A_RAW)
        with contextlib.redirect_stdout(io.StringIO()):
            S23.score_phase_a(client, dry_run=False)
        return _load_json(S23.PHASE_A_SCORED)


# --------------------------------------------------------------------------- the coder
def brand_of(rec, probes):
    """Registry brand key of a Phase A call: v0.19 brand name, v0.20-22 name (probe 'brand'), v0.23 id."""
    if rec.get("brand"):
        return rec["brand"] if rec["substrate"] != "v23" else rec["brand_id"]
    p = probes[(rec["substrate"], rec["phase"], rec["probe_id"])]
    return p["brand_id"] if rec["substrate"] in ("v19", "v23") else p["brand"]


def code_calls(calls, probes, strip=True, strip_recognition=False, judge_client=None):
    """calls: raw records (already deduped). Returns (phase_a_rows, phase_b_rows).
    strip: URL removal before Phase B brand matching. strip_recognition: also before the
    Phase A yes/no parse (default False: the pre-registration names URL removal for brand matching).
    judge_client: None -> v0.23 Phase A not coded (judge OFF); else client for score_phase_a."""
    probes = probes or {}
    A, B = [], []
    v23a, v23b = [], []
    for r in calls:
        if not is_answered(r):
            continue
        raw = r["substrate"]
        sub = SUB_MAP[raw]
        base = {"call_id": r["call_id"], "substrate": sub, "model": r["model_requested"],
                "condition": r["condition"], "run": r["run"], "probe_id": r["probe_id"]}
        text = r["text"]
        if r["phase"] == "B":
            frame = r.get("frame_id") or r["probe_id"]
            if raw == "v23":
                v23b.append({"call_id": r["call_id"], "status": "ok", "response": strip_urls(text) if strip else text,
                             "probe_id": r["probe_id"], "model_slot": r["model_requested"], "_base": base,
                             "_frame": frame})
                continue
            ment = mentions_nonv23(sub, strip_urls(text) if strip else text)
            for b, v in ment.items():
                B.append({**base, "frame_id": frame, "brand": b, "mentioned": v})
        else:
            brand = brand_of(r, probes)
            if raw == "v23":
                p = probes.get((raw, "A", r["probe_id"]), {})
                v23a.append({"call_id": r["call_id"], "status": "ok", "response": text,
                             "brand_id": r["brand_id"], "brand_name": r.get("brand") or p.get("brand", ""),
                             "spirit_type": r.get("spirit_type") or p.get("spirit_type", ""),
                             "model_slot": r["model_requested"], "model_id": r["model_requested"],
                             "_base": base, "_brand": brand})
                continue
            lab = recog_label(sub, strip_urls(text) if strip_recognition else text)
            A.append({**base, "brand": brand, "brand_id": r.get("brand_id"), "label": lab,
                      "recognized": 1 if lab == "yes" else 0})   # ambiguous / no -> 0, as in the t1-t3 extractors
    if v23b:
        scored = code_v23_phase_b(v23b)
        for rec in scored:
            for bid, v in rec["brand_mentions"].items():
                B.append({**rec["_base"], "frame_id": rec["_frame"], "brand": bid, "mentioned": int(v)})
    if v23a and judge_client is not None:
        scored = code_v23_phase_a(v23a, judge_client)
        for rec in scored:
            lvl = rec.get("r_level")
            A.append({**rec["_base"], "brand": rec["_brand"], "brand_id": rec["brand_id"], "label": lvl,
                      "recognized": r_level_to_binary(lvl)})
    return A, B


A_FIELDS = ["call_id", "substrate", "brand", "brand_id", "model", "condition", "run", "probe_id", "label", "recognized"]
B_FIELDS = ["call_id", "substrate", "brand", "model", "condition", "run", "probe_id", "frame_id", "mentioned"]


def write_tables(A, B, out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    for raw, sub in SUB_MAP.items():
        for rows, fields, ph in ((A, A_FIELDS, "a"), (B, B_FIELDS, "b")):
            with open(out / f"{raw}_phase_{ph}.csv", "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=fields)
                w.writeheader()
                for r in rows:
                    if r["substrate"] == sub:
                        w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in fields})
    return out


def read_tables(coded_dir):
    """Read the coded tables back (ints restored). Returns (A, B)."""
    A, B = [], []
    for raw, sub in SUB_MAP.items():
        for ph, acc in (("a", A), ("b", B)):
            p = Path(coded_dir) / f"{raw}_phase_{ph}.csv"
            if not p.exists():
                continue
            for r in csv.DictReader(open(p, newline="", encoding="utf-8")):
                r["run"] = int(r["run"])
                if ph == "a":
                    r["recognized"] = None if r["recognized"] == "" else int(r["recognized"])
                else:
                    r["mentioned"] = int(r["mentioned"])
                acc.append(r)
    return A, B


# --------------------------------------------------------------------------- gate P2 (t3 raw -> coder)
def _t3_raw_calls():
    """Convert the locked t3 RAW answers (the inputs v41_code_t3.py / score_v41.load_wave read) into t4-format
    raw records (one per t3 call), plus the locked r_level queue for the v0.23 judge mock."""
    m = _modules()
    S31 = m["S31"]
    calls = []

    def add(raw, phase, model, text, pid, **kw):
        calls.append({"call_id": f"t3|{raw}|{phase}|{pid}|{model}|{len(calls)}", "substrate": raw, "phase": phase,
                      "probe_id": pid, "model_requested": model, "condition": "S0", "run": 1,
                      "text": text or "", "status": "ok" if (text or "").strip() else "empty", "error": None, **kw})

    d = DATA3 / "v19"
    for ph, fn in (("A", "phase_a_responses.jsonl"), ("B", "phase_b_responses.jsonl")):
        for line in open(d / fn, encoding="utf-8"):
            if line.strip():
                o = json.loads(line)
                if ph == "A":
                    add("v19", "A", o["panel_model"], o["response"], "phase_a__" + o["brand"], brand_id=o["brand"], brand=o["brand"])
                else:
                    add("v19", "B", o["panel_model"], o["response"], "phase_b__" + o["frame"], frame_id=o["frame"])
    for raw in ("v20", "v21", "v22"):
        d = DATA3 / raw
        for r in S31.read_csv(d / "phase_a_results.csv"):
            add(raw, "A", r["model"], r["response_text"], f"{raw}_A_{r['brand']}", brand_id=r["brand"], brand=r["brand"],
                locked_label=r["recognized"])
        for r in S31.read_csv(d / "phase_b_results.csv"):
            add(raw, "B", r["model"], r["response_text"], r["frame_id"], frame_id=r["frame_id"])
    d = DATA3 / "v23"
    scored_a = json.load(open(d / "v23_phase_a_scored.json", encoding="utf-8"))
    for r in json.load(open(d / "v23_phase_a_raw.json", encoding="utf-8")):
        add("v23", "A", r["model_id"], r["response"], r["brand_id"], brand_id=r["brand_id"], brand=r["brand_name"],
            spirit_type=r["spirit_type"])
        calls[-1]["status"] = r["status"] if r["status"] != "ok" or (r["response"] or "").strip() else "empty"
    for r in json.load(open(d / "v23_phase_b_raw.json", encoding="utf-8")):
        add("v23", "B", r["model_id"], r["response"], r["probe_id"], frame_id=r["probe_id"])
        calls[-1]["status"] = r["status"] if r["status"] != "ok" or (r["response"] or "").strip() else "empty"
    return calls, scored_a


class LockedJudgeClient:
    """Mock anthropic client for P2: replies with the LOCKED t3 judge output for the matching judge prompt.
    Nothing is sent anywhere."""

    def __init__(self, scored_a):
        S23 = _modules()["S23"]
        self.q = collections.defaultdict(collections.deque)
        for r in scored_a:
            if r.get("status") == "ok":
                msg = S23.JUDGE_USER_TEMPLATE.format(brand_name=r["brand_name"], spirit_type=r["spirit_type"],
                                                    response=r["response"][:3000])
                self.q[msg].append(r["r_level"])
        self.messages = self
        self.calls = 0

    def create(self, **kw):
        self.calls += 1
        msg = kw["messages"][0]["content"]
        lvl = self.q[msg].popleft()
        return type("Msg", (), {"content": [type("Blk", (), {"text": "ERR" if lvl == "R_ERR" else lvl})()]})()


def _locked_codes():
    """Locked t3 codes from the certified machinery (score_v41.load_wave) + the CSV recognition labels."""
    import score_v41 as sv
    wave = sv.load_wave(sv._layout(DATA3, DATA3 / "v23"))
    return sv, wave


def _code_cells(A, B):
    """Coder output -> {(sub, model, frame, brand): mentioned}, {(sub, brand, model): recognized}."""
    mc = {(r["substrate"], r["model"], r["frame_id"], r["brand"]): r["mentioned"] for r in B}
    rc = {(r["substrate"], r["brand"], r["model"]): r["recognized"] for r in A}
    return mc, rc


def parity_p2(out_path=P2_PATH):
    m = _modules()
    PANEL = m["S31"].PANEL
    sv, wave = _locked_codes()
    calls, scored_a = _t3_raw_calls()
    by = collections.Counter((c["substrate"], c["phase"]) for c in calls)

    def run(strip, strip_recog=False):
        client = LockedJudgeClient(scored_a)
        A, B = code_calls(calls, probes={}, strip=strip, strip_recognition=strip_recog, judge_client=client)
        return A, B, client

    A0, B0, client0 = run(False)
    mc0, rc0 = _code_cells(A0, B0)

    # ---- compare with the locked codes
    res = {}
    for raw, sub in SUB_MAP.items():
        w = wave[sub]
        # mention cells: every (model, frame, brand) of the substrate's answered Phase B calls
        n_cells = mism = 0
        examples = []
        for (s, model, frame, brand), v in mc0.items():
            if s != sub or model not in PANEL:
                continue
            locked = int(frame in w["frames"].get(brand, {}).get(model, ()))
            n_cells += 1
            if locked != v:
                mism += 1
                if len(examples) < 5:
                    examples.append([model, frame, brand, v, locked])
        # recognition cells (brand x model); locked vector missing/ambiguous = 0 (as recog_raw / recog_v19)
        n_r = r_mism = 0
        for brand, vec in w["recog"].items():
            for i, model in enumerate(PANEL):
                got = rc0.get((sub, brand, model))
                if got is None:                      # not coded (empty answer / ambiguous v0.19 -> 0 / judge n.a.)
                    got = 0 if sub != "v0.23" else None
                n_r += 1
                if got != int(vec[i]):
                    r_mism += 1
        res[sub] = {"mention_cells": n_cells, "mention_mismatches": mism, "mention_examples": examples,
                    "recognition_cells": n_r, "recognition_mismatches": r_mism}
    # label-level parity for v0.20-v0.22 (the locked 'recognized' column)
    lab_n = lab_mis = 0
    for r in A0:
        if r["substrate"] in ("v0.20", "v0.21", "v0.22"):
            lab_n += 1
    lock_lab = {}
    for c in calls:
        if c["substrate"] in ("v20", "v21", "v22") and c["phase"] == "A":
            lock_lab[(SUB_MAP[c["substrate"]], c["brand"], c["model_requested"])] = (c["locked_label"], c["status"])
    for r in A0:
        key = (r["substrate"], r["brand"], r["model"])
        if key in lock_lab and lock_lab[key][0] != r["label"]:
            lab_mis += 1
    for sub in ("v0.20", "v0.21", "v0.22"):
        res[sub]["label_cells"] = sum(1 for r in A0 if r["substrate"] == sub)
        res[sub]["label_mismatches"] = sum(1 for r in A0 if r["substrate"] == sub
                                           and lock_lab.get((sub, r["brand"], r["model"]), (r["label"],))[0] != r["label"])
    uncoded = [list(k) for k, (lab, st) in lock_lab.items() if st != "ok"]
    # v0.19: ambiguous recognition answers (skipped by parse_phase_a)
    amb19 = sum(1 for r in A0 if r["substrate"] == "v0.19" and r["label"] == "ambiguous")
    # v0.23 judge path: all locked judge answers consumed, none re-run
    unused = sum(len(q) for q in client0.q.values())
    r_err = sum(1 for r in scored_a if r.get("r_level") == "R_ERR")
    passed_off = all(v["mention_mismatches"] == 0 and v["recognition_mismatches"] == 0 for v in res.values()) \
        and all(res[s]["label_mismatches"] == 0 for s in ("v0.20", "v0.21", "v0.22")) and unused == 0

    # ---- URL removal ON: list every changed t3 code
    A1, B1, _ = run(True)
    mc1, rc1 = _code_cells(A1, B1)
    changed_m = [[s, model, fr, b, mc0[(s, model, fr, b)], mc1.get((s, model, fr, b))]
                 for (s, model, fr, b) in mc0 if mc1.get((s, model, fr, b)) != mc0[(s, model, fr, b)]]
    changed_r = [[s, b, model, rc0[(s, b, model)], rc1.get((s, b, model))]
                 for (s, b, model) in rc0 if rc1.get((s, b, model)) != rc0[(s, b, model)]]
    A2, B2, _ = run(True, strip_recog=True)
    _, rc2 = _code_cells(A2, B2)
    changed_r2 = [[s, b, model, rc0[(s, b, model)], rc2.get((s, b, model))]
                  for (s, b, model) in rc0 if rc2.get((s, b, model)) != rc0[(s, b, model)]]
    n_url = sum(1 for c in calls if c["phase"] == "B" and strip_urls(c["text"]) != c["text"])
    n_url_a = sum(1 for c in calls if c["phase"] == "A" and strip_urls(c["text"]) != c["text"])

    out = {
        "gate": "P2", "passed": bool(passed_off), "inputs": "osf/v41/data (t3 raw answers); locked codes via "
        "score_v41.load_wave (mentions, v0.19/v0.20-22 recognition) and v23_phase_a_scored.json (v0.23 judge)",
        "t3_calls_recoded": dict((f"{s}_{p}", n) for (s, p), n in sorted(by.items())),
        "total_calls": sum(by.values()),
        "url_removal_off": {
            "per_substrate": res, "v0_19_ambiguous_recognition_answers": amb19,
            "v0_20_22_unanswered_status_calls": len(uncoded),
            "v0_23_recognition": "NOT re-judged: the coder's judge path ran score_v0_23.score_phase_a against a MOCK client "
                                 "that replays the locked t3 judge outputs (v23_phase_a_scored.json); "
                                 f"mock replies consumed={client0.calls}, unused={unused}, locked R_ERR={r_err}",
            "total_mention_cells": sum(v["mention_cells"] for v in res.values()),
            "total_mention_mismatches": sum(v["mention_mismatches"] for v in res.values()),
            "total_recognition_cells": sum(v["recognition_cells"] for v in res.values()),
            "total_recognition_mismatches": sum(v["recognition_mismatches"] for v in res.values())},
        "url_removal_on": {
            "t3_phase_b_answers_containing_a_url": n_url, "t3_phase_a_answers_containing_a_url": n_url_a,
            "changed_mention_codes": changed_m, "n_changed_mention_codes": len(changed_m),
            "changed_recognition_codes_phase_b_only_stripping": changed_r,
            "n_changed_recognition_codes": len(changed_r),
            "diagnostic_recognition_also_stripped": {"changed": changed_r2, "n_changed": len(changed_r2)}},
    }
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    _dump_json(out, out_path, indent=2, ensure_ascii=False)
    return out


# --------------------------------------------------------------------------- CLI
def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--raw", default=str(REAL_RAW))
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    ap.add_argument("--no-url-strip", action="store_true", help="switch URL removal OFF")
    ap.add_argument("--judge", action="store_true", help="run the v0.23 Phase A LLM judge (OFF by default; calls the API)")
    ap.add_argument("--parity-p2", action="store_true")
    a = ap.parse_args()
    if a.parity_p2:
        r = parity_p2()
        off, on = r["url_removal_off"], r["url_removal_on"]
        print(f"P2 {'PASS' if r['passed'] else 'FAIL'}: calls={r['total_calls']} mention cells={off['total_mention_cells']} "
              f"mismatches={off['total_mention_mismatches']}; recognition cells={off['total_recognition_cells']} "
              f"mismatches={off['total_recognition_mismatches']}; URL-on changed mention={on['n_changed_mention_codes']} "
              f"recognition={on['n_changed_recognition_codes']} -> {P2_PATH}")
        return 0 if r["passed"] else 2
    try:
        calls = dedupe_calls(read_raw(a.raw))
    except Refused as e:
        print(f"[v42] REFUSED: {e}", file=sys.stderr)
        return 3
    client = None
    if a.judge:
        import anthropic
        client = anthropic.Anthropic()
    A, B = code_calls(calls, load_probe_map(), strip=not a.no_url_strip, judge_client=client)
    write_tables(A, B, a.out)
    print(f"coded {len(calls)} calls -> {len(A)} Phase A rows, {len(B)} Phase B rows in {a.out}"
          + ("" if client else "  (v0.23 Phase A judge OFF: not coded)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
