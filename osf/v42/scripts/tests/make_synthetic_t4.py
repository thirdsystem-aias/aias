#!/usr/bin/env python3
"""
make_synthetic_t4.py -- writes SYNTHETIC t4 raw + coded data in the real formats (osf/v42/data/t4_raw.jsonl lines
and the coder's coded tables). Synthetic only: never touches osf/v42/data/. No model is called.

A "k map" is {(substrate, brand): k in 0..6} for one (model, condition, run). Phase B answers list the brands whose
k exceeds the frame index (frame i lists brands with k > i), so the coder reproduces k from the raw text.

  build(kfn, outdir=None, drop=None, fail=None, recog=None, served=None) -> (raw, A, B)
    kfn(model, cond, run) -> k map            drop(call_spec) -> True: call absent from raw and coded
    fail(call_spec) -> True: raw line with status 'error', nothing coded
    recog(model, cond, run, sub, brand) -> 0/1   served(call_spec) -> served model id
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import code_t4_v0_42 as C   # noqa: E402
import numpy as np          # noqa: E402

MODELS = ["claude-fable-5-2", "claude-opus-5-5", "gpt-6-astra", "gemini-4-argon"]
PROVIDER = {"claude-fable-5-2": "anthropic", "claude-opus-5-5": "anthropic", "gpt-6-astra": "openai",
            "gemini-4-argon": "google"}
CONDS = ["S0", "S1"]
RUNS = [1, 2, 3]


def brand_name(sub, b):
    if sub == "v0.23":
        return {r["id"]: r["brand"] for r in C._modules()["S23"].REGISTRY}[b]
    return b


def build(kfn, outdir=None, drop=None, fail=None, recog=None, served=None, t0="2026-11-12T00:00:00+00:00"):
    probes = [json.loads(l) for l in open(C.PROBES_PATH, encoding="utf-8") if l.strip()]
    frame_ids = {}
    for x in probes:
        if x["phase"] == "B":
            frame_ids.setdefault(x["substrate"], []).append(x["probe_id"])
    raw, A, B = [], [], []
    for m in MODELS:
        for run in RUNS:
            for cond in CONDS:
                kmap = kfn(m, cond, run)
                for p in probes:
                    sub = C.SUB_MAP[p["substrate"]]
                    cid = f"{p['substrate']}|{p['phase']}|{p['probe_id']}|{m}|{cond}|{run}"
                    spec = {"call_id": cid, "model": m, "condition": cond, "run": run, "substrate": p["substrate"],
                            "phase": p["phase"], "probe_id": p["probe_id"]}
                    if drop and drop(spec):
                        continue
                    base = {"call_id": cid, "substrate": sub, "model": m, "condition": cond, "run": run,
                            "probe_id": p["probe_id"]}
                    fi = frame_ids[p["substrate"]].index(p["probe_id"]) if p["phase"] == "B" else None
                    if p["phase"] == "B":
                        named = [brand_name(sub, b) for (s, b) in kmap if s == sub and kmap[(s, b)] > fi]
                        text = ("Top brands: " + ", ".join(named) + ".") if named else "No clear picks."
                    else:
                        bkey = p["brand_id"] if p["substrate"] in ("v19", "v23") else p["brand"]
                        yes = 1 if recog is None else recog(m, cond, run, sub, bkey)
                        text = ("Yes." if yes else "No.") if p["substrate"] != "v23" else "A synthetic answer."
                    bad = bool(fail and fail(spec))
                    rec = {"call_id": cid, "substrate": p["substrate"], "phase": p["phase"], "probe_id": p["probe_id"],
                           "brand_id": p.get("brand_id"), "frame_id": p.get("frame_id"), "model_requested": m,
                           "provider": PROVIDER[m], "served_model": (served(spec) if served else m), "condition": cond,
                           "run": run, "system": None, "prompt": p["prompt"], "text": "" if bad else text,
                           "status": "error" if bad else "ok", "error": "synthetic failure" if bad else None,
                           "finish_reason": None if bad else "end_turn", "input_tokens": 100, "output_tokens": 50,
                           "thinking_tokens": 10 if PROVIDER[m] == "google" else None,
                           "search": ({"n_searches": 2, "queries": ["q1", "q2"], "sources": [{"url": "https://a.example/x"}],
                                       "citations": [{"url": "https://www.cited.example/p"}], "errors": []}
                                      if cond == "S1" else None),
                           "paused_continued": False, "attempts": 1, "empty_retry": False,
                           "started_utc": t0, "finished_utc": "2026-11-12T12:00:00+00:00"}
                    raw.append(rec)
                    if bad:
                        continue
                    if p["phase"] == "B":
                        for b in [b for (s, b) in kmap if s == sub]:
                            B.append({**base, "frame_id": p.get("frame_id"), "brand": b,
                                      "mentioned": int(kmap[(sub, b)] > fi)})
                    else:
                        A.append({**base, "brand": bkey, "brand_id": p.get("brand_id"),
                                  "label": ("yes" if yes else "no") if p["substrate"] != "v23" else ("R2" if yes else "R0"),
                                  "recognized": int(yes)})
    if outdir:
        outdir = Path(outdir)
        outdir.mkdir(parents=True, exist_ok=True)
        with open(outdir / "t4_raw.jsonl", "w", encoding="utf-8") as f:
            for r in raw:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        C.write_tables(A, B, outdir / "coded")
    return raw, A, B


# --------------------------------------------------------------------------- k-map generators
def from_t3(t3, idx):
    """k map = the locked t3 counts of L6 model number idx."""
    return {key: v["k"][idx] for key, v in t3.items()}


def shuffled(kmap, seed):
    """k values permuted among brands within each substrate (destroys the order)."""
    rng = np.random.default_rng(seed)
    out = {}
    for s in sorted({k[0] for k in kmap}):
        keys = [k for k in kmap if k[0] == s]
        vals = [kmap[k] for k in keys]
        perm = rng.permutation(len(keys))
        for k, j in zip(keys, perm):
            out[k] = vals[j]
    return out


def mixed(kmap, frac, seed):
    """A fraction `frac` of brands (per substrate) get their k permuted among themselves."""
    rng = np.random.default_rng(seed)
    out = dict(kmap)
    for s in sorted({k[0] for k in kmap}):
        keys = [k for k in kmap if k[0] == s]
        n = int(round(frac * len(keys)))
        sel = [int(i) for i in rng.choice(len(keys), size=n, replace=False)] if n > 1 else []
        vals = [kmap[keys[i]] for i in sel]
        perm = rng.permutation(len(sel))
        for i, j in zip(sel, perm):
            out[keys[i]] = vals[j]
    return out


if __name__ == "__main__":
    import score_v0_42 as S
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/synthetic_t4")
    t3 = S.load_t3_table()
    L = {m: from_t3(t3, i) for m, i in zip(MODELS, (0, 1, 2, 4))}
    raw, A, B = build(lambda m, c, r: L[m], out)
    print(f"synthetic t4 written to {out}: {len(raw)} raw calls, {len(A)} Phase A rows, {len(B)} Phase B rows")
