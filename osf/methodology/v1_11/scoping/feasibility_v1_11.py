#!/usr/bin/env python3
"""
v1.11 parsing-only feasibility count on the DEVELOPMENT SAMPLE (declared; excluded from every
confirmatory analysis). No model calls, no valence, nothing computed on Presence, Consistency,
Ranking, separability or stability.

Development sample (all excluded from v1.11's confirmatory inputs):
  D1 v0.17 Phase A  - 24 recognition-type answers ("Who or what is X?"), legacy panel
  D2 v0.17 Phase B  - 18 frame answers (3 queries x 6 models), legacy panel
  D3 v0.18 Phase B  - 18 frame answers (3 frames x 6 models), legacy panel
  D4 v0.5 archive   - first-pass early-design answers (pre-protocol, 3 providers)
Counts: answers parsed; registry brands located per answer; mention-window length; windows at
the cap; 'bare' windows (the brand's segments carry < 4 words besides the brand name); recognition
answer length. Output: feasibility_v1_11.json next to this file.
Run from the repo root: python3 osf/methodology/v1_11/scoping/feasibility_v1_11.py
"""
import csv
import glob
import json
import os
import re
import statistics as st
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import score_v1_11 as S  # noqa: E402


def p(path):
    return os.path.join(ROOT, path)


def kitchenware_brands():
    reg = json.load(open(p("registries/brands_kitchenware_v0.17.json")))
    return sorted({b["name"] for c in reg["cells"].values() for b in c["brands"]})


def v18_brands(d):
    return sorted({b["brand"] for c in d["cells"].values() for b in c.get("per_brand", [])})


def text_of(rec):
    if isinstance(rec.get("response"), dict):          # v0.18 nested raw record
        rec = rec["response"]
    for k in ("response_text", "response", "raw_response", "raw_text", "text"):
        if isinstance(rec.get(k), str):
            return rec[k]
    return ""


def window_stats(answers, brands, aliases_of=lambda b: [b]):
    """answers: list of strings. Returns per-answer brand counts and per-window lengths."""
    per_answer, lens, bare, capped = [], [], 0, 0
    for t in answers:
        k = 0
        for b in brands:
            others = [a for o in brands if o != b for a in aliases_of(o)]
            w = S.build_window(t, aliases_of(b), others)
            if w is None:
                continue
            k += 1
            lens.append(len(w))
            capped += len(w) >= S.WINDOW_CHAR_CAP
            rest = S.alias_pattern(aliases_of(b)).sub(" ", S.fold(w.replace("[...]", " ")))
            bare += len(re.findall(r"[a-z]{2,}", rest)) < 4
        per_answer.append(k)
    return per_answer, lens, bare, capped


def summarize(name, answers, brands, aliases_of=lambda b: [b]):
    per_answer, lens, bare, capped = window_stats(answers, brands, aliases_of)
    n_w = len(lens)
    return {
        "set": name, "answers_parsed": len(answers), "registry_brands": len(brands),
        "answers_with_>=1_brand": sum(k > 0 for k in per_answer),
        "windows": n_w,
        "windows_per_answer_mean": round(n_w / len(answers), 2) if answers else None,
        "windows_per_answer_median": st.median(per_answer) if per_answer else None,
        "window_chars_median": st.median(lens) if lens else None,
        "window_chars_p90": sorted(lens)[int(0.9 * (n_w - 1))] if lens else None,
        "window_tokens_mean_est": S.est_tokens(int(st.mean(lens))) if lens else None,
        "windows_at_cap": capped, "bare_windows": bare,
        "answer_chars_median": st.median(len(a) for a in answers) if answers else None,
    }


def main():
    out = {"phase": "v1.11", "kind": "parsing-only feasibility, development sample", "sets": []}
    kb = kitchenware_brands()
    d2 = [text_of(json.load(open(f))) for f in sorted(glob.glob(p("osf/v17/data/phaseB_queries/*/slot_*.json")))]
    out["sets"].append(summarize("D2 v0.17 Phase B frames", d2, kb))
    v18 = json.load(open(p("data/phase_b/v0.18/phase_b_results.json")))
    d3 = [text_of(r) for r in v18["_raw_query_records"].values()]
    out["sets"].append(summarize("D3 v0.18 Phase B frames", d3, v18_brands(v18)))
    rows = [r for r in csv.DictReader(open(p("archive/old_data/results_20260429_105403.csv")))
            if (r.get("raw_response") or "").strip()]
    found = sorted({b.strip() for r in rows for b in re.split(r"[|;,]", r.get("brands_found") or "")
                    if b.strip()})
    out["sets"].append(summarize("D4 v0.5 archive (early design)", [r["raw_response"] for r in rows], found))
    # D1 recognition: the whole answer is the unit; window stats are not needed
    d1 = []
    for f in sorted(glob.glob(p("osf/v17/data/phase_a/*/slot_*.json"))):
        d1.append(text_of(json.load(open(f))))
    lens = [len(t) for t in d1]
    out["sets"].append({"set": "D1 v0.17 Phase A recognition", "answers_parsed": len(d1),
                        "answer_chars_median": st.median(lens), "answer_chars_max": max(lens),
                        "answer_tokens_mean_est": S.est_tokens(int(st.mean(lens))),
                        "over_recog_cap": sum(x > S.RECOG_CHAR_CAP for x in lens)})
    json.dump(out, open(p("osf/methodology/v1_11/scoping/feasibility_v1_11.json"), "w"), indent=2)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
