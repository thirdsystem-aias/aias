#!/usr/bin/env python3
"""
feasibility_v1_10.py - v1.10 Ranking Paper A, declared parsing-feasibility look.

Development sample ONLY (excluded from every confirmatory analysis): v0.17 phase B
(18 frame answers, osf/v17/data/phaseB_queries/) and v0.18 phase B (18 frame answers,
data/phase_b/v0.18/phase_b_results.json). Computes parsing properties only: list
structure, registry-brand detection, rule disagreement, ties, repeats, overlaps,
detector parity. Computes NO statistic involving Presence, Consistency, separability
or stability, and no brand-level score.

Run from the repository root:  python3 osf/methodology/v1_10/scoping/feasibility_v1_10.py
"""
import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts"))
import score_v1_10 as S  # noqa: E402

OUT = Path(__file__).with_suffix(".json")


def v17_aliases(canonical):
    """Mirror of scripts/phaseB_resolve_v17.generate_aliases (mechanical variants)."""
    v = {canonical, canonical.lower()}
    if "-" in canonical:
        v |= {canonical.replace("-", " "), canonical.replace("-", "")}
    if " " in canonical:
        v |= {canonical.replace(" ", "-"), canonical.replace(" ", "")}
    return sorted(x for x in v if x.strip())


def load_v17():
    reg = json.loads((ROOT / "registries/brands_kitchenware_v0.17.json").read_text())
    registry = {b["name"]: v17_aliases(b["name"]) for c in reg["cells"].values() for b in c["brands"]}
    answers = []
    for f in sorted((ROOT / "osf/v17/data/phaseB_queries").glob("*/slot_*.json")):
        d = json.loads(f.read_text())
        answers.append({"id": f"{d['query_id']}__{d['model_id']}", "text": d.get("response_text") or ""})
    return registry, answers, None


def load_v18():
    d = json.loads((ROOT / "data/phase_b/v0.18/phase_b_results.json").read_text())
    registry, flags = {}, {}
    for cell in d["cells"].values():
        for b in cell["per_brand"]:
            registry[b["brand"]] = [b["brand"]]
            for fr, per_model in b["per_frame_per_model"].items():
                for m, v in per_model.items():
                    flags[(f"{fr}__{m}", b["brand"])] = bool(v)
    answers = [{"id": k, "text": (v.get("response") or {}).get("raw_response") or ""}
               for k, v in d["_raw_query_records"].items()]
    return registry, answers, flags


def kendall_tau(a, b):
    keys = sorted(a)
    conc = disc = 0
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            x = (a[keys[i]] - a[keys[j]]) * (b[keys[i]] - b[keys[j]])
            conc += x > 0
            disc += x < 0
    return (conc - disc) / (conc + disc) if conc + disc else 1.0


def nested_events(norm, pats):
    """Matches of one brand lying inside a longer match of another brand (overlap log)."""
    spans = {b: [(m.start(), m.end()) for p in ps for m in p.finditer(norm)] for b, ps in pats.items()}
    n = 0
    for b, sp in spans.items():
        for (s, e) in sp:
            if any(b2 != b and s2 <= s and e <= e2 and (e2 - s2) > (e - s)
                   for b2, sp2 in spans.items() for (s2, e2) in sp2):
                n += 1
    return n


def analyse(name, registry, answers, flags):
    pats = S.compile_registry(registry)
    rows, found_brands = [], set()
    parity_agree = parity_total = 0
    for a in answers:
        if not a["text"].strip():
            rows.append({"empty": True})
            continue
        norm = S.normalize(a["text"])
        hits = S.find_mentions(norm, pats)
        found_brands |= set(hits)
        spans = S.item_spans(norm)
        prim = S.rank_answer(a["text"], pats, "lead_item")
        sens = S.rank_answer(a["text"], pats, "first_mention")
        lead = S._lead_items(hits, spans) if spans else {}
        items_with_brand = sum(1 for (s, e, _k) in spans
                               if any(s <= x < e for xs in hits.values() for x in xs))
        rows.append({
            "empty": False,
            "named": prim["named"],
            "rankable": prim["named"] >= S.MIN_NAMED_RANKABLE,
            "list_structured": prim["list_structured"],
            "any_items": len(spans) >= 2,
            "numbered": sum(1 for s in spans if s[2] == "num") >= 2,
            "items": len(spans),
            "items_with_brand": items_with_brand,
            "intro_mention": bool(spans) and prim["list_structured"] and any(xs[0] < spans[0][0] for xs in hits.values()),
            "repeat_pairs": sum(1 for xs in hits.values() if len(xs) >= 2),
            "pairs": len(hits),
            "non_leading_pairs": (len(hits) - len(lead)) if prim["list_structured"] else 0,
            "tie": len({v[0] for v in prim["ranks"].values()}) < len(prim["ranks"]),
            "rules_differ": prim["ranks"] != sens["ranks"],
            "tau": kendall_tau({b: v[0] for b, v in prim["ranks"].items()},
                               {b: v[0] for b, v in sens["ranks"].items()}) if prim["ranks"] else None,
            "nested": nested_events(norm, pats),
        })
        if flags is not None:
            for b in registry:
                if (a["id"], b) in flags:
                    parity_total += 1
                    parity_agree += (b in hits) == flags[(a["id"], b)]
    ok = [r for r in rows if not r["empty"]]
    rk = [r for r in ok if r["rankable"]]
    ls = [r for r in ok if r["list_structured"]]
    pairs = sum(r["pairs"] for r in ok)
    res = {
        "set": name, "answers": len(rows), "with_text": len(ok),
        "registry_brands": len(registry),
        "registry_brands_found_at_least_once": len(found_brands),
        "share_any_list_items": round(sum(r["any_items"] for r in ok) / len(ok), 3),
        "share_numbered_list": round(sum(r["numbered"] for r in ok) / len(ok), 3),
        "share_list_structured": round(len(ls) / len(ok), 3),
        "share_rankable_prose_only": round(sum(1 for r in rk if not r["list_structured"]) / len(ok), 3),
        "brands_named_per_answer_mean": round(statistics.mean(r["named"] for r in ok), 2),
        "brands_named_per_answer_median": statistics.median(r["named"] for r in ok),
        "brands_named_per_answer_range": [min(r["named"] for r in ok), max(r["named"] for r in ok)],
        "share_answers_ge1_brand": round(sum(r["named"] >= 1 for r in ok) / len(ok), 3),
        "share_answers_rankable_ge2": round(len(rk) / len(ok), 3),
        "share_items_without_registry_brand": round(1 - sum(r["items_with_brand"] for r in ok) / max(1, sum(r["items"] for r in ok)), 3),
        "share_list_answers_with_intro_mention": round(sum(r["intro_mention"] for r in ls) / max(1, len(ls)), 3),
        "share_pairs_named_twice_or_more": round(sum(r["repeat_pairs"] for r in ok) / max(1, pairs), 3),
        "share_list_pairs_not_leading_an_item": round(sum(r["non_leading_pairs"] for r in ls) / max(1, sum(r["pairs"] for r in ls)), 3),
        "share_rankable_with_tie_primary": round(sum(r["tie"] for r in rk) / max(1, len(rk)), 3),
        "share_rankable_rules_differ": round(sum(r["rules_differ"] for r in rk) / max(1, len(rk)), 3),
        "mean_kendall_tau_primary_vs_first_mention": round(statistics.mean(r["tau"] for r in rk), 3) if rk else None,
        "nested_match_events": sum(r["nested"] for r in ok),
    }
    if flags is not None:
        res["detector_parity_cells"] = parity_total
        res["detector_parity_agreement"] = round(parity_agree / max(1, parity_total), 4)
    return res


def main():
    out = {"phase": "v1.10", "kind": "declared parsing feasibility (development sample only)",
           "excluded_from_confirmatory": ["v0.17 phase B (18)", "v0.18 phase B (18)"],
           "results": [analyse("v0.17 B", *load_v17()), analyse("v0.18 B", *load_v18())]}
    OUT.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
