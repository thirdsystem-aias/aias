"""v1.18 PRE-LOCK step (declared in PRE_REGISTRATION_v1_18.md section 9): read t4 only to
(1) count records and answered S1 category answers on N3, (2) reproduce one published v1.13 input count
(MQ1 = 270 parsed S1 records; MQ8 per-provider answers with citations and cited URLs), and
(3) list the distinct registrable domains in `citations` and `sources` for the blind domain table.

Blindness: the domain list is written sorted alphabetically, one domain per line, with no counts, no model,
no substrate, no answer, no brand, no field label and no class from v1.13. The coded brand rows are NOT read
here (no answer is linked to any brand). Domains in any registry D_b are removed from the list (they are
'company' by rule T0 and 'focal' only through D_b). Nothing the study estimates is computed.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common_v1_18 as C  # noqa: E402


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--t4", required=True)
    ap.add_argument("--out", default=str(C.PHASE / "outputs" / "prelock"))
    a = ap.parse_args(argv)
    s = C.load_v113()
    classes = s.load_classes(C.V113_CLASSES)
    units = s.load_brand_domains(C.V113_DOMAINS)
    all_db = set().union(*[u["domains"] for u in units.values()])
    recs = s.dedupe_calls(s.read_jsonl(a.t4))
    cat = s.select_calls(recs, s.PANELS["N3"], "S1", "B")
    doms = {"citations": set(), "sources": set()}
    unresolved_urls = {"citations": 0, "sources": 0}
    for r in cat:
        for field in doms:
            for e in ((r.get("search") or {}).get(field) or []):
                if not isinstance(e, dict):
                    continue
                src = s.resolve_source(e.get("url"), e.get("title"), classes)
                if src is None:
                    unresolved_urls[field] += 1
                else:
                    doms[field].add(src["domain"])
    mq8 = s.mq8_citations_vs_sources(cat, classes)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    to_classify = sorted((doms["citations"] | doms["sources"]) - all_db)
    (out / "domains_to_classify_v1_18.txt").write_text("\n".join(to_classify) + "\n", encoding="utf-8")
    cited_only = sorted(doms["citations"] - all_db)   # the primary field's subset, classified by hand first
    (out / "domains_to_classify_cited_v1_18.txt").write_text("\n".join(cited_only) + "\n", encoding="utf-8")
    counts = {
        "t4_sha256": C.sha256_file(a.t4), "records_in_file": sum(1 for _ in open(a.t4, encoding="utf-8")),
        "records_after_dedupe": len(recs), "answered_s1_category_n3": len(cat),
        "loader_check_vs_v1_13_MQ1_270": len(cat) == 270,
        "mq8_reproduced": {p: {k: v[k] for k in ("answers", "with_citations", "cited")} for p, v in mq8.items()},
        "distinct_domains": {f: len(v) for f, v in doms.items()},
        "distinct_domains_union": len(doms["citations"] | doms["sources"]),
        "distinct_in_any_D_b": {f: len(v & all_db) for f, v in doms.items()},
        "to_classify": len(to_classify), "url_unresolved_entries": unresolved_urls,
    }
    (out / "prelock_counts_v1_18.json").write_text(json.dumps(counts, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(counts, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
