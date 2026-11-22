#!/usr/bin/env python3
"""
c2_extras_v1_13.py -- pre-registered Part I outputs that the locked scorer's command line does not produce
(postlock/DEVIATIONS_continued_v1_13.md, Entries 5, 6, 7 and 9). NOT a locked file: it imports score_v1_13.py and
audit_v1_13.py read-only and calls only their functions, with the pre-registered seeds and rules. It changes no
hypothesis, threshold, verdict rule, primary statistic or verdict; every result is a sensitivity or a descriptive.

  S6        section 7: D_b as verified by Part II -- each RESOLVED unit's D_b plus the registrable domain of its home
            page's final URL after redirects (audit `verified_alias`) and the registrable domains of the adjudicated
            Wikidata item's P856 (audit records); NONE units stay without D_b. H1-H3 recomputed as stage_c1's other
            sensitivities are (seed 113009, 10,000 permutations, no bootstrap), verdict changes listed.
  S7        section 7: P and C* from AIAS 2.0 at t3 (osf/aias_2_0/aias_2_0_profiles.csv via score_v1_13.legacy_t3),
            the computation stage_c1 performs only when given profiles, which main() never passes.
  cited     section 6: "The same tables for the cited set (citations) are reported beside them": score_v1_13.baseline
            on the answers built from search.citations (all N3 models, as the primary baseline).
  primary   section 6 descriptives on the primary panel only (the locked baseline uses all three N3 models, including a
            model dropped by MQ2/MQ4; both are reported, labelled).
  MQ2_kept  section 4 MQ2 "reported both ways": H1-H3 with a model that MQ2 dropped (< 0.10) kept (S5 covers Gemini).

Run once, after Stage C2 (or after C1, without S6 when Part II was not collected), on the same inputs as the scorer:
  python3 osf/methodology/v1_13/postlock/c2_extras_v1_13.py --t4 T --coded D --brand-table B \
      --verdicts osf/methodology/v1_13/v1_13_verdicts.json [--records audit/v1_13_audit_records.jsonl \
      --sdri audit/v1_13_sdri.csv] [--profiles osf/aias_2_0/aias_2_0_profiles.csv] [--out PATH]
Writes osf/methodology/v1_13/v1_13_c2_extras.json once, with the SHA-256 of every input.
"""
import argparse
import copy
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
PHASE = HERE.parent
sys.path.insert(0, str(PHASE / "scripts"))
sys.path.insert(0, str(HERE))
sys.dont_write_bytecode = True
import score_v1_13 as S  # noqa: E402
import audit_v1_13 as A  # noqa: E402
from audit_checks_v1_13 import refuse_locked, read_jsonl, sha256  # noqa: E402

GATE = list(S.GATE_LEGS)
INACTIVE = {leg: False for leg in S.CONDITIONAL_LEGS}


def aliases_from_audit(records, sdri_rows, units, multi_suffix):
    """{unit: set(new domains)} for RESOLVED units: verified_alias and the adjudicated QID's P856 domains."""
    qid = {(r["substrate"], r["brand_id"]): (r.get("qid") or None) for r in sdri_rows}
    out = {}
    for r in records:
        k = (r["substrate"], r["brand_id"])
        if k not in units or units[k]["status"] != "RESOLVED" or r.get("phantom"):
            continue
        add = set()
        if r.get("verified_alias"):
            add.add(r["verified_alias"])
        kg, q = r.get("kg") or {}, qid.get(k)
        urls = kg.get("p856") if (q and kg.get("qid") == q) else (kg.get("tied_p856") or {}).get(q, []) if q else []
        for u in urls or []:
            d = A.registrable(u, multi_suffix)
            if d:
                add.add(d)
        new = add - units[k]["domains"]
        if new:
            out[k] = new
    return out


def _stats(answers, units, P, C, n_perm, primary):
    r = S.gate_statistics(answers, units, P, C, None, dict(INACTIVE), n_perm, 0,
                          seeds={k: S.SEEDS["sensitivities"] for k in S.SEEDS})
    v = {h: r["verdicts"][h] for h in GATE}
    return {"verdicts": v, "gate_H1_H3": r["gate"]["verdict"], "rel3": r["H3"]["rel3"],
            "rho": {h: [l["rho_w"] for l in r["legs"][h]] for h in ("H1_Sep_Presence", "H2_Sep_Consistency")},
            "verdict_changes": {h: [v[h], primary[h]] for h in GATE if v[h] != primary[h]},
            "n_rated": r["mq5"]["n_rated"]}


def extras(inp, doc, aliases=None, profiles=None, n_perm=S.N_PERM):
    units, classes = inp["units"], inp["classes"]
    recs = S.dedupe_calls(inp["records"])
    named = S.named_index(inp["coded_b"], units)
    cat_n3 = S.select_calls(recs, S.PANELS["N3"], "S1", "B")
    models = list(doc["panel_models"])
    n3 = S.PANELS["N3"]
    excluded = S.t4_excluded(inp["records"])
    P = {c: S.p_t4(inp["brand_table"], inp["coded_a"], units, c, n3, excluded) for c in ("S0", "S1")}
    C = {c: S.c_star_t4(inp["brand_table"], inp["coded_b"], units, c, n3, excluded) for c in ("S0", "S1")}
    primary = {h: doc["verdicts"][h] for h in GATE}
    ans_n3 = S.build_answers(cat_n3, named, units, classes)
    ans = [a for a in ans_n3 if a["model"] in models]
    out = {"panel_models": models, "seeds": S.SEEDS["sensitivities"], "n_perm": n_perm,
           "note": "conditional legs H4-H6 are not recomputed here (their sources are read by the scorer only)"}
    if aliases is not None:
        ua = copy.deepcopy(units)
        for k, new in aliases.items():
            ua[k]["domains"] = set(ua[k]["domains"]) | set(new)
        aa = [a for a in S.build_answers(cat_n3, named, ua, classes) if a["model"] in models]
        out["S6_verified_D_b"] = dict(_stats(aa, ua, P, C, n_perm, primary), units_with_aliases=len(aliases),
                                      aliases={f"{k[0]}|{k[1]}": sorted(v) for k, v in sorted(aliases.items())})
    else:
        out["S6_verified_D_b"] = {"status": "NOT_COMPUTED", "reason": "Part II not collected (no audit records)"}
    if profiles is not None:
        P3, C3 = S.legacy_t3(profiles, units)
        out["S7_legacy_t3"] = _stats(ans, units, {"S0": P3, "S1": P3}, {"S0": C3, "S1": C3}, n_perm, primary)
    else:
        out["S7_legacy_t3"] = {"status": "NOT_COMPUTED", "reason": "no AIAS 2.0 profiles given"}
    cited = S.build_answers(cat_n3, named, units, classes, S.CITED_FIELD)
    out["baseline_cited_set_all_N3"] = S.baseline(cited, units, S.brand_stats(cited, units))
    out["baseline_primary_panel"] = S.baseline(ans, units, S.brand_stats(ans, units))
    mq2 = [m for m in doc.get("dropped_models") or [] if ((doc.get("MQ") or {}).get("MQ2", {}).get(m) or {})
           .get("dropped_from_g_star")]
    if mq2:
        kept = [a for a in ans_n3 if a["model"] in models + mq2]
        out["MQ2_kept"] = dict(_stats(kept, units, P, C, n_perm, primary), models_kept=mq2)
    else:
        out["MQ2_kept"] = {"status": "NOT_APPLICABLE", "reason": "no model was dropped by MQ2"}
    return json.loads(json.dumps(out, default=str))


def load_inputs(a, units):
    coded_a, coded_b = [], []
    for sub in S.SUBSTRATES:
        for ph, acc in (("a", coded_a), ("b", coded_b)):
            p = Path(a.coded) / f"{sub}_phase_{ph}.csv"
            if p.exists():
                acc.extend(S.read_csv(p))
    return {"records": S.read_jsonl(a.t4), "coded_a": coded_a, "coded_b": coded_b,
            "brand_table": S.read_csv(a.brand_table), "units": units, "classes": S.load_classes()}


def main(argv=None):
    ap = argparse.ArgumentParser(description="v1.13 S6, S7, cited-set and primary-panel baselines, MQ2 both ways")
    for f in ("--t4", "--coded", "--brand-table", "--verdicts"):
        ap.add_argument(f, required=True)
    ap.add_argument("--records")
    ap.add_argument("--sdri")
    ap.add_argument("--profiles")
    ap.add_argument("--domains", type=Path, default=S.DOMAINS_CSV, help="testing only; default the frozen D_b list")
    ap.add_argument("--perm", type=int, default=S.N_PERM)
    ap.add_argument("--out", type=Path, default=PHASE / "v1_13_c2_extras.json")
    a = ap.parse_args(argv)
    refuse_locked(a.out)
    if bool(a.records) != bool(a.sdri):
        sys.exit("REFUSED: S6 needs both --records and --sdri (or neither)")
    units = S.load_brand_domains(a.domains)
    doc = json.loads(Path(a.verdicts).read_text(encoding="utf-8"))
    inp = load_inputs(a, units)
    aliases = None
    if a.records:
        aliases = aliases_from_audit(read_jsonl(a.records), S.read_csv(a.sdri), units,
                                     inp["classes"]["multi_suffix"])
    out = extras(inp, doc, aliases, S.read_csv(a.profiles) if a.profiles else None, a.perm)
    files = {"t4": a.t4, "brand_table": a.brand_table, "verdicts": a.verdicts, "records": a.records, "sdri": a.sdri,
             "profiles": a.profiles, "domains": str(a.domains)}
    out["inputs"] = {k: ([v, sha256(v)] if v else None) for k, v in files.items()}
    out["inputs"]["coded"] = {p.name: sha256(p) for p in sorted(Path(a.coded).glob("*_phase_*.csv"))}
    out["inputs"]["script_sha256"] = sha256(__file__)
    out["inputs"]["test_only"] = a.domains.resolve() != S.DOMAINS_CSV.resolve() or a.perm != S.N_PERM
    out["written_utc"] = datetime.now(timezone.utc).isoformat()
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    print(f"S6 {out['S6_verified_D_b'].get('verdict_changes', out['S6_verified_D_b'].get('status'))}; "
          f"S7 {out['S7_legacy_t3'].get('verdict_changes', out['S7_legacy_t3'].get('status'))} -> {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
