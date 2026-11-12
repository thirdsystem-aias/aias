#!/usr/bin/env python3
"""
cost_estimate_v0_40.py -- AIAS(TM) v0.40 pre-registration, section 6: cost of the collection design and of the
alternatives, from RECORDED usage at the vendors' list prices. Sends nothing.

Prices (USD per 1M tokens, input/output; opened 2026-11-12):
  Anthropic  https://platform.claude.com/docs/en/about-claude/models/overview.md
             Fable 5.2 $8/$40, Opus 5.5 $4/$20, Opus 4.5 $5/$25, Sonnet 4.5 $3/$15; "Batch API requests are 50% off"
  OpenAI     https://developers.openai.com/docs/models/gpt-6-astra  gpt-6-astra $10/$50 (Batch 50%)
             https://developers.openai.com/api/docs/models/gpt-4o.md  gpt-4o $2.50/$10.00
             https://developers.openai.com/api/docs/models/gpt-4o-mini.md  gpt-4o-mini $0.15/$0.60
             https://developers.openai.com/api/docs/pricing  web search "$10.00 per 1k calls"
  Google     https://aistudio.google.com/docs/pricing (redirect target of ai.google.dev/gemini-api/docs/pricing)
             gemini-2.5-flash $0.30/$2.50, gemini-2.5-flash-lite $0.10/$0.40 (output incl. thinking);
             gemini-4-argon $2/$10 through 2026-11-30 ($4/$20 from 2026-12-01); grounding $14 per 1,000 (free
             allowance not assumed)
Token / cost basis:
  current arm, Fable 5.2 / GPT-6 Astra / Gemini 4 Argon: v0.42 t4 raw file (collected 2026-11-11), field cost_usd of
     every record (errors included, so failed attempts are costed), per model x phase x condition. Recommendation
     probes use t4 Phase B (category lists); K and S probes use t4 Phase A at S0 (brand questions) and t4 Phase B at
     S1 (t4 asked no brand question with search on: conservative). Central = mean cost per completed record (all
     records' cost / completed records); high = 90th percentile of Phase B cost per record, for every probe.
  Claude Opus 5.5 (alternative): v0.39 raw file, arm C (30 calls per condition), at the Opus 5.5 prices above.
  legacy arm: v0.39 raw file, arm L (30 calls per model), tokens_in / tokens_out (+ tokens_thought for Gemini);
     central = mean; high = input mean + the 2,048-token output cap. Gemini 2.5 Flash at thinking budget 0 is costed
     with its v0.39 output tokens and no thinking; the extra pass at the v0.39 setting with its v0.39 thinking.
Usage: python3 cost_estimate_v0_40.py [--t4 PATH] [--v39 PATH] [--json OUT]
"""
import argparse
import json
import statistics as st
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
V40 = HERE.parent
DEF_T4 = Path.home() / "aias/osf/v42/data/t4_raw.jsonl"
DEF_V39 = V40.parent / "v39/data/v39_raw.json"
PROBES = V40 / "prereg/probes_v0_40.json"

P = {  # standard (input, output) USD per 1M tokens
    "claude-opus-4-5": (5.0, 25.0), "claude-sonnet-4-5": (3.0, 15.0), "gpt-4o": (2.5, 10.0),
    "gpt-4o-mini": (0.15, 0.60), "gemini-2.5-flash": (0.30, 2.50), "gemini-2.5-flash-lite": (0.10, 0.40),
    "claude-opus-5-5": (4.0, 20.0), "claude-fable-5-2": (8.0, 40.0),
}
SEARCH_FEE = {"anthropic": 0.010, "openai": 0.010, "google": 0.014}
LEGACY = ["claude-opus-4-5", "claude-sonnet-4-5", "gpt-4o", "gpt-4o-mini", "gemini-2.5-flash", "gemini-2.5-flash-lite"]
CAP, PAUSE = 100.0, 80.0


def p90(xs):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(round(0.9 * (len(xs) - 1))))] if xs else 0.0


def t4_basis(path):
    rows = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
    g = defaultdict(list)
    for r in rows:
        g[(r["model_requested"], r["phase"], r["condition"])].append(r)
    out = {}
    for (m, ph, c), rs in g.items():
        ok = [r for r in rs if r["status"] == "ok"]
        tot = sum(r.get("cost_usd") or 0.0 for r in rs)
        okc = [r.get("cost_usd") or 0.0 for r in ok]
        out[(m, ph, c)] = {"n": len(rs), "n_ok": len(ok), "central": tot / max(1, len(ok)),
                           "p90": p90(okc) * (tot / max(1e-12, sum(okc)))}
    return out


def v39_cost(r, model):
    pin, pout = P[model]
    tout = (r.get("tokens_out") or 0)
    if model.startswith("gemini"):
        tout += r.get("tokens_thought") or 0
    n = ((r.get("search") or {}).get("n_searches") or 0) if r.get("condition") == "S1" else 0
    prov = r.get("provider")
    return ((r.get("tokens_in") or 0) * pin + tout * pout) / 1e6 + n * SEARCH_FEE.get(prov, 0.0)


def v39_basis(path):
    recs = json.load(open(path, encoding="utf-8"))
    out = {}
    for m in LEGACY:
        rs = [r for r in recs if r["arm"] == "L" and r["model_id"] == m and r["status"] == "ok"]
        pin, pout = P[m]
        tin = st.mean(r.get("tokens_in") or 0 for r in rs)
        if m == "gemini-2.5-flash":
            zero = st.mean(((r.get("tokens_in") or 0) * pin + (r.get("tokens_out") or 0) * pout) / 1e6 for r in rs)
            dflt = st.mean(v39_cost(r, m) for r in rs)
            out[(m, "budget0")] = {"central": zero, "p90": (tin * pin + 2048 * pout) / 1e6}
            out[(m, "v039")] = {"central": dflt, "p90": (tin * pin + 2048 * pout) / 1e6}
        else:
            out[(m, "std")] = {"central": st.mean(v39_cost(r, m) for r in rs), "p90": (tin * pin + 2048 * pout) / 1e6}
    for c in ("S0", "S1"):
        rs = [r for r in recs if r["arm"] == "C" and r["model_id"] == "claude-opus-5-5" and r["condition"] == c]
        cs = [v39_cost(r, "claude-opus-5-5") for r in rs]
        out[("claude-opus-5-5", c)] = {"central": st.mean(cs), "p90": p90(cs), "n": len(rs)}
    return out


def kinds():
    pr = json.load(open(PROBES, encoding="utf-8"))["probes"]
    n_rec = sum(p["kind"] == "recommendation" for p in pr)
    return len(pr), n_rec, len(pr) - n_rec


def design(t4, v39, anth="claude-fable-5-2", s1_runs=3, s1_ks=True, s0_runs=3, legacy_runs=3):
    n_all, n_rec, n_ks = kinds()
    cen = hi = 0.0
    calls = 0
    lines = []
    for m in LEGACY:
        keys = [(m, "budget0", legacy_runs), (m, "v039", 1)] if m == "gemini-2.5-flash" else [(m, "std", legacy_runs)]
        for k0, k1, runs in keys:
            b = v39[(k0, k1)]
            n = n_all * runs
            cen += n * b["central"]; hi += n * b["p90"]; calls += n
            lines.append((f"L {m} {k1} x{runs}", n, n * b["central"], n * b["p90"]))
    for m in [anth, "gpt-6-astra", "gemini-4-argon"]:
        for c, runs in (("S0", s0_runs), ("S1", s1_runs)):
            n_ks_c = n_ks if (c == "S0" or s1_ks is True) else (n_ks // 2 if s1_ks == "S" else 0)
            if m == "claude-opus-5-5":
                b = v39[(m, c)]
                rc, kc, h = b["central"], b["central"], b["p90"]
            else:
                rb = t4[(m, "B", c)]
                kb = t4[(m, "A", "S0")] if c == "S0" else rb
                rc, kc, h = rb["central"], kb["central"], rb["p90"]
            n1, n2 = n_rec * runs, n_ks_c * runs
            c_ = n1 * rc + n2 * kc
            h_ = (n1 + n2) * h
            cen += c_; hi += h_; calls += n1 + n2
            tag = "" if n_ks_c == n_ks else (" (recommendation + S probes)" if n_ks_c else " (recommendation probes only)")
            lines.append((f"C {m} {c} x{runs}" + tag, n1 + n2, c_, h_))
    return {"calls": calls, "central": cen, "high": hi, "lines": lines}


DESIGNS = [
    ("D1 frozen probe set: Fable 5.2 (Batch API), S0 x3, S1 x3 on all 94 probes", {}),
    ("D2 = D1 with S1 x1 run", {"s1_runs": 1}),
    ("D3 = D1 with S1 x3 on the 32 recommendation probes only", {"s1_ks": False}),
    ("D4 = D1 with S1 x1 run on the 32 recommendation probes only", {"s1_runs": 1, "s1_ks": False}),
    ("D5 = D1 with Claude Opus 5.5 (synchronous) in place of Fable 5.2", {"anth": "claude-opus-5-5"}),
    ("D6 = D5 with S1 x1 run", {"anth": "claude-opus-5-5", "s1_runs": 1}),
    ("D7 (registered) = D1 with S1 x1 run on the 32 recommendation + 31 status (S) probes", {"s1_runs": 1, "s1_ks": "S"}),
]
REGISTERED = 6  # index of the registered design in DESIGNS


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--t4", default=str(DEF_T4))
    ap.add_argument("--v39", default=str(DEF_V39))
    ap.add_argument("--json")
    a = ap.parse_args()
    t4, v39 = t4_basis(a.t4), v39_basis(a.v39)
    print("== basis: t4 cost per completed record (central) / 90th pct (high), USD")
    for k in sorted(t4):
        b = t4[k]
        print(f"  {k[0]:18s} {k[1]} {k[2]}  n={b['n']:3d} ok={b['n_ok']:3d}  {b['central']:.4f} / {b['p90']:.4f}")
    for k in sorted(v39):
        print(f"  v0.39 {k[0]:22s} {k[1]:7s} {v39[k]['central']:.4f} / {v39[k]['p90']:.4f}")
    res = {}
    print("\n== designs (US$, central / high)")
    for name, kw in DESIGNS:
        d = design(t4, v39, **kw)
        res[name] = d
        flag = "fits" if d["high"] <= CAP else ("central fits, high above cap" if d["central"] <= CAP else "ABOVE CAP")
        print(f"  {name}\n     calls {d['calls']:5d}  central ${d['central']:7.2f}  high ${d['high']:7.2f}  [{flag}]")
    print("\n== per cell, D7 (registered)")
    for l in res[DESIGNS[REGISTERED][0]]["lines"]:
        print(f"  {l[0]:62s} {l[1]:5d} calls  ${l[2]:6.2f} / ${l[3]:6.2f}")
    if a.json:
        Path(a.json).write_text(json.dumps(res, indent=2), encoding="utf-8")
        print(f"wrote {a.json}")


if __name__ == "__main__":
    main()
