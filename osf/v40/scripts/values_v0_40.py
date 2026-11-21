#!/usr/bin/env python3
"""v0.40 values file (runner upgrade 2, "numbers come from code"; claude/runner-process-upgrades-nov19.md section 2).

Every figure the v0.40 paper, report and web page cite is read from osf/v40/v40_values.json, never typed. This script
reads ONLY files already in the repo, written by the locked pipeline:
  osf/v40/v40_verdicts.json                 (score_v0_40.py, run once, step 9)
  osf/v40/audit/v40_audit_agreement.json    (audit_ai_v0_40.py, section 5.5)
  osf/v40/data/v40_coding_manifest.json     (code_only_v0_40.py, step 8)
  osf/v40/data/v40_raw.jsonl                (acquisition record)
  osf/v40/prereg/prelock_check_v0_40.jsonl and prereg/feasibility_check_v0_40.json (pre-lock spend, section 6.5)
  osf/v40/v40_postscore.json                (postscore_v0_40.py, DEVIATIONS Entry 2: the H_Amplify ceiling check and
                                             the pre-registered reporting the locked scorer did not output; each such
                                             value carries its label in its source record)
and writes osf/v40/v40_values.json (flat keys -> value, display string, rounding rule, source file + JSON path) and
osf/v40/v40_values.md (the same as a human table). Costs are computed with the locked guard's own functions
(budget_v0_40.Ledger / spend_of, acquire_v0_40.prior_spend), so they equal what the guard recorded.

Deterministic: no network, no paid calls, no clock. It changes no input file. It refuses (exit 2, nothing written) if
the verdicts are missing or incomplete, or if a coded file's SHA-256 or row count differs from the coding manifest.

Run:   python3 osf/v40/scripts/values_v0_40.py            (writes both files)
       python3 osf/v40/scripts/values_v0_40.py --check    (exit 1 if the committed files differ from a fresh build)
Fill:  fill("... {{v:H_Flag.ghost_rate}} ...", values) -> the display strings (unknown key -> KeyError).
"""
import csv
import hashlib
import json
import re
import subprocess
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent                      # repo root (osf/v40/scripts -> root)
sys.path.insert(0, str(HERE))

PHASE = "v0.40"
REL = {
    "verdicts": "osf/v40/v40_verdicts.json",
    "audit": "osf/v40/audit/v40_audit_agreement.json",
    "manifest": "osf/v40/data/v40_coding_manifest.json",
    "raw": "osf/v40/data/v40_raw.jsonl",
    "mentions": "osf/v40/data/v40_mentions.csv",
    "coded": "osf/v40/data/v40_coded_answers.csv",
    "prelock_raw": "osf/v40/prereg/prelock_check_v0_40.jsonl",
    "feasibility": "osf/v40/prereg/feasibility_check_v0_40.json",
    "postscore": "osf/v40/v40_postscore.json",
    "prereg": "osf/v40/prereg/PRE_REGISTRATION_v0_40.md",
}
OUT_JSON = "osf/v40/v40_values.json"
OUT_MD = "osf/v40/v40_values.md"
HYPOTHESES = ("H_Reinforce", "H_Amplify", "H_Afterlife", "H_Decay", "H_Flag", "H_Search")
REQUIRED_VERDICT_KEYS = HYPOTHESES + ("thresholds", "sensitivity", "manipulation_checks", "descriptives")
SKIP_LEAVES = {"path"}          # absolute paths on the collection computer (coding manifest inputs); not figures

# ---- rounding rules (stated once here; each value carries its rule id and text)
RULES = {
    "INT": "integer, exact, thousands separator",
    "P": "p-value: 3 decimals, half up; below 0.001 shown as < 0.001, above 0.999 as > 0.999",
    "PCT": "proportion shown as a percent, 1 decimal, half up",
    "PCT_AGREE": "percent (already x100 in the source), 1 decimal, half up",
    "USD": "US dollars, 2 decimals, half up",
    "DEC3": "3 decimals, half up",
    "THRESH": "registered threshold or setting, exact as stored",
    "BOOL": "boolean shown as yes / no",
    "NULL": "null in the source (not computed), shown as n/a",
    "TEXT": "text, verbatim",
}


class Refused(Exception):
    pass


def _half_up(v, places):
    q = Decimal(1).scaleb(-places)
    return Decimal(repr(float(v))).quantize(q, rounding=ROUND_HALF_UP)


def fmt_int(v):
    return f"{int(v):,}"


def fmt_dec(v, places=3):
    return f"{_half_up(v, places):,.{places}f}" if abs(v) >= 1000 else str(_half_up(v, places))


def fmt_p(v):
    if v < 0.001:
        return "< 0.001"
    if v > 0.999:
        return "> 0.999"
    return str(_half_up(v, 3))


def fmt_pct(v, already_percent=False):
    x = Decimal(repr(float(v))) * (1 if already_percent else 100)
    return f"{x.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)}%"


def fmt_usd(v):
    return f"${_half_up(v, 2):,.2f}"


def rule_for(path, value):
    """Rule id for a value from its JSON path (list of keys) and type."""
    leaf = str(path[-1])
    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return "BOOL"
    if isinstance(value, str):
        return "TEXT"
    if path[0] == "thresholds" or leaf in ("kappa_min", "seed", "window_chars"):
        return "THRESH"
    if isinstance(value, int):
        return "USD" if leaf.endswith("_usd") else "INT"
    if leaf.endswith("_usd"):
        return "USD"
    if leaf.startswith("p_"):
        return "P"
    if leaf == "percent_agreement":
        return "PCT_AGREE"
    if "rate" in leaf or "share" in leaf or leaf == "limit" or "share" in [str(p) for p in path[:-1]]:
        return "PCT"
    return "DEC3"


def display(rule, value):
    if rule == "NULL":
        return "n/a"
    if rule == "BOOL":
        return "yes" if value else "no"
    if rule == "TEXT":
        return value
    if rule == "THRESH":
        return repr(value)
    if rule == "INT":
        return fmt_int(value)
    if rule == "USD":
        return fmt_usd(value)
    if rule == "P":
        return fmt_p(value)
    if rule == "PCT":
        return fmt_pct(value)
    if rule == "PCT_AGREE":
        return fmt_pct(value, already_percent=True)
    if rule == "DEC3":
        return fmt_dec(value, 3)
    raise ValueError(rule)


# ---- inputs
def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(root, name):
    p = Path(root) / REL[name]
    if not p.exists():
        raise Refused(f"{REL[name]} is missing")
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise Refused(f"{REL[name]} cannot be read: {e!r}")


def check_verdicts(v):
    if not isinstance(v, dict):
        raise Refused("v40_verdicts.json is not an object")
    missing = [k for k in REQUIRED_VERDICT_KEYS if k not in v]
    if missing:
        raise Refused(f"v40_verdicts.json lacks {missing}")
    no_verdict = [h for h in HYPOTHESES if not isinstance(v[h], dict) or not v[h].get("verdict")]
    if no_verdict:
        raise Refused(f"v40_verdicts.json has no verdict for {no_verdict}")
    if v.get("phase") != PHASE:
        raise Refused(f"v40_verdicts.json phase is {v.get('phase')!r}, not {PHASE!r}")


def csv_rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return sum(1 for _ in csv.reader(f)) - 1


def check_manifest(root, man):
    for name, key in (("mentions", "v40_mentions.csv"), ("coded", "v40_coded_answers.csv")):
        p = Path(root) / REL[name]
        rec = (man.get("outputs") or {}).get(key)
        if not rec or not p.exists():
            raise Refused(f"{REL[name]} or its manifest entry is missing")
        if sha256(p) != rec["sha256"]:
            raise Refused(f"{REL[name]} SHA-256 differs from the coding manifest")
        if csv_rows(p) != rec["rows"]:
            raise Refused(f"{REL[name]} row count differs from the coding manifest")


# ---- flattening
def resolve(obj, path):
    for k in path:
        obj = obj[k]
    return obj


def walk(obj, path=()):
    """Yield (path, scalar) for every non-list scalar leaf; lists are reported separately (not figures one cites
    from here; e.g. the per-answer search traces)."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from walk(v, path + (k,))
    elif isinstance(obj, list):
        yield path, obj
    else:
        yield path, obj


class Values:
    def __init__(self):
        self.v = {}
        self.skipped_lists = []

    def add(self, key, value, source, rule=None):
        if key in self.v:
            raise Refused(f"duplicate values key {key!r}")
        rule = rule or rule_for(source.get("path") or [key.split(".")[-1]], value)
        self.v[key] = {"value": value, "display": display(rule, value), "rule": rule, "rule_text": RULES[rule],
                       "source": source}

    def add_tree(self, prefix, tree, file, keep_path_prefix=(), label=None):
        for path, val in walk(tree):
            if path and str(path[-1]) in SKIP_LEAVES:
                continue
            full = list(keep_path_prefix) + list(path)
            if isinstance(val, list):
                self.skipped_lists.append({"file": file, "path": full, "items": len(val)})
                continue
            key = ".".join([prefix] + [str(p) for p in path] if prefix else [str(p) for p in path])
            src = {"file": file, "path": full}
            if label:
                src["label"] = label
            self.add(key, val, src)


def git_last_commit(root, rel):
    try:
        out = subprocess.run(["git", "-C", str(root), "log", "-1", "--format=%H", "--", rel],
                             capture_output=True, text=True, timeout=20)
        return out.stdout.strip() or None
    except (OSError, subprocess.SubprocessError):
        return None


def costs(root):
    """Spend exactly as the locked collection guard counts it: Ledger(raw, prior_usd=prior_spend()).spent()."""
    import budget_v0_40 as BG
    import acquire_v0_40 as A
    try:
        prior, parts = A.prior_spend(Path(root) / REL["prelock_raw"], Path(root) / REL["feasibility"])
    except SystemExit as e:
        raise Refused(str(e))
    raw = Path(root) / REL["raw"]
    if not raw.exists():
        raise Refused(f"{REL['raw']} is missing")
    state = Path(root) / "osf/v40/data/v40_budget_state.json"     # read only on approval; Ledger() writes nothing
    ledger = BG.Ledger(raw, state, prior_usd=prior)
    return {"spent": ledger.spent(), "actual": ledger.actual, "prior": prior, "parts": parts,
            "judge_reserve": BG.JUDGE_RESERVE_USD, "cap": BG.BUDGET_CAP_USD, "pause": BG.PAUSE_AT_USD}


def check_postscore(root, ps):
    """The post-scoring file must have been built from the files now in the repo, with both closure checks passed."""
    meta = ps.get("_meta") or {}
    for rec in (meta.get("inputs") or {}).values():
        p = Path(root) / rec["file"]
        if not p.exists() or sha256(p) != rec["sha256"]:
            raise Refused(f"{REL['postscore']} was built from a different {rec['file']}")
    cc = meta.get("closure_checks") or {}
    if not (cc.get("mentions_file_byte_identical") and cc.get("primary_tests_and_S_D4_equal_verdict_file")):
        raise Refused(f"{REL['postscore']}: closure checks not passed")
    if "ceiling" not in ps or "prereg" not in ps:
        raise Refused(f"{REL['postscore']} lacks its ceiling or prereg block")


def raw_counts(root):
    recs = [json.loads(l) for l in (Path(root) / REL["raw"]).read_text(encoding="utf-8").splitlines() if l.strip()]
    by = {}
    for r in recs:
        k = f"{r['arm']}|{r['condition']}"
        by[k] = by.get(k, 0) + 1
    return {"total": len(recs), "ok": sum(1 for r in recs if r.get("status") == "ok"), "by": dict(sorted(by.items())),
            "cost_field_sum": sum(r["cost_usd"] for r in recs)}


def build(root=ROOT):
    root = Path(root)
    verdicts = load_json(root, "verdicts")          # first: refuse before anything else if the verdicts are missing
    check_verdicts(verdicts)
    audit = load_json(root, "audit")
    man = load_json(root, "manifest")
    check_manifest(root, man)
    post = load_json(root, "postscore")
    check_postscore(root, post)
    V = Values()

    # 1. verdicts: every scalar (hypotheses, sensitivities, manipulation checks incl. failures, descriptives, thresholds)
    V.add_tree("", verdicts, REL["verdicts"])

    # 2. audit agreement (AI-only audit, section 5.5)
    V.add_tree("audit", audit, REL["audit"])

    # 3. coding manifest
    V.add_tree("coding", man, REL["manifest"])
    V.add("coding.answers", man["answers_coded"], {"file": REL["manifest"], "path": ["answers_coded"]})
    V.add("coding.mentions", man["outputs"]["v40_mentions.csv"]["rows"],
          {"file": REL["manifest"], "path": ["outputs", "v40_mentions.csv", "rows"]})

    # 3b. DEVIATIONS Entry 2 (postscore_v0_40.py): the H_Amplify ceiling check, and the pre-registered reporting the
    #     locked scorer did not output; each value's source record carries its label
    labels = post["_meta"]["labels"]
    V.add_tree("ceiling", post["ceiling"], REL["postscore"], keep_path_prefix=("ceiling",), label=labels["ceiling"])
    V.add_tree("prereg_post", post["prereg"], REL["postscore"], keep_path_prefix=("prereg",), label=labels["prereg"])

    # 3c. reference figures the locked pre-registration says to report beside descriptive 6 (section 2.9 item 6)
    pr = (root / REL["prereg"]).read_text(encoding="utf-8")
    m = re.search(r"beside v1\.17's (0\.\d+) and (0\.\d+) \(§2\.10\)", pr)
    if not m:
        raise Refused("the v1.17 reference figures of pre-registration section 2.9 item 6 were not found")
    for key, grp, what in (("reference.v1_17.se_all_units", 1, "all units"),
                           ("reference.v1_17.se_some_not_all", 2, "units named in some answers but not all")):
        V.add(key, float(m.group(grp)),
              {"computed": f"v1.17 run-to-run SE at 3 runs ({what}), as quoted in pre-registration section 2.9 "
                           f"item 6 (regex on the locked text)", "inputs": [REL["prereg"]]}, "DEC3")

    # 4. acquisition record counts (computed from the raw file)
    rc = raw_counts(root)
    src = lambda what: {"computed": what, "inputs": [REL["raw"]]}
    V.add("acquisition.records_total", rc["total"], src("lines of v40_raw.jsonl"), "INT")
    V.add("acquisition.records_ok", rc["ok"], src("lines of v40_raw.jsonl with status == 'ok'"), "INT")
    for k, n in rc["by"].items():
        arm, cond = k.split("|")
        V.add(f"acquisition.records.{arm}.{cond}", n, src(f"lines of v40_raw.jsonl with arm == '{arm}' and "
                                                          f"condition == '{cond}'"), "INT")

    # 5. costs (locked guard functions; audit spend from the audit record)
    c = costs(root)
    cin = [REL["raw"], REL["prelock_raw"], REL["feasibility"]]
    V.add("cost.acquisition_recorded_usd", c["spent"],
          {"computed": "budget_v0_40.Ledger(v40_raw.jsonl, prior_usd=acquire_v0_40.prior_spend()).spent() = "
                       "judge reserve + pre-lock spend + collection spend (the guard's spend at the end of collection)",
           "inputs": cin}, "USD")
    V.add("cost.collection_usd", c["actual"],
          {"computed": "budget_v0_40.record_cost summed over v40_raw.jsonl (Ledger.actual)", "inputs": [REL["raw"]]},
          "USD")
    V.add("cost.prelock_total_usd", c["prior"],
          {"computed": "acquire_v0_40.prior_spend() total (pre-lock check + technical check)", "inputs": cin[1:]}, "USD")
    for fname, usd in sorted(c["parts"].items()):
        stem = "prelock_check_usd" if fname.startswith("prelock") else "technical_check_usd"
        V.add(f"cost.{stem}", usd, {"computed": f"acquire_v0_40.prior_spend() part for {fname}", "inputs": cin[1:]},
              "USD")
    V.add("cost.judge_reserve_usd", c["judge_reserve"], {"computed": "budget_v0_40.JUDGE_RESERVE_USD",
                                                         "inputs": ["osf/v40/scripts/budget_v0_40.py"]}, "USD")
    V.add("cost.paper_cap_usd", c["cap"], {"computed": "budget_v0_40.BUDGET_CAP_USD",
                                           "inputs": ["osf/v40/scripts/budget_v0_40.py"]}, "USD")
    V.add("cost.pause_at_usd", c["pause"], {"computed": "budget_v0_40.PAUSE_AT_USD",
                                            "inputs": ["osf/v40/scripts/budget_v0_40.py"]}, "USD")
    V.add("cost.audit_usd", audit["spent_usd"], {"file": REL["audit"], "path": ["spent_usd"]}, "USD")
    V.add("cost.audit_cap_usd", audit["cap_usd"], {"file": REL["audit"], "path": ["cap_usd"]}, "USD")
    V.add("cost.paper_total_usd", c["spent"] + audit["spent_usd"],
          {"computed": "cost.acquisition_recorded_usd + cost.audit_usd (unrounded values summed, then rounded)",
           "inputs": cin + [REL["audit"]]}, "USD")

    meta = {
        "phase": PHASE,
        "what": "v0.40 values file: every figure cited in the v0.40 paper, report and site comes from here",
        "script": "osf/v40/scripts/values_v0_40.py",
        "inputs": {n: {"file": REL[n], "sha256": sha256(root / REL[n])} for n in REL},
        "verdicts_commit": git_last_commit(root, REL["verdicts"]),
        "rules": RULES,
        "placeholder_syntax": "{{v:<key>}} -> display",
        "skipped_lists": V.skipped_lists,
        "n_values": len(V.v),
    }
    return {"_meta": meta, "values": V.v}


def fill(text, values):
    """Replace {{v:KEY}} with the value's display string. Unknown keys raise KeyError (never a silent blank)."""
    vals = values["values"] if "values" in values else values
    return re.sub(r"\{\{v:([^}]+)\}\}", lambda m: vals[m.group(1).strip()]["display"], text)


# ---- output
def to_json(doc):
    return json.dumps(doc, indent=1, ensure_ascii=False) + "\n"


SECTIONS = [
    ("Hypotheses (confirmatory verdicts and test statistics)", lambda k: k.split(".")[0] in HYPOTHESES),
    ("Manipulation checks (failures included)", lambda k: k.startswith("manipulation_checks.")),
    ("Coding", lambda k: k.startswith("coding.")),
    ("Acquisition record", lambda k: k.startswith("acquisition.")),
    ("Costs", lambda k: k.startswith("cost.")),
    ("Audit agreement (AI-only analyst, section 5.5)", lambda k: k.startswith("audit.")),
    ("Sensitivities (reported beside each verdict; no verdict changes)", lambda k: k.startswith("sensitivity.")),
    ("Registered thresholds and run settings", lambda k: k.split(".")[0] in ("thresholds", "phase", "seed",
                                                                            "permutations", "window_chars")),
    ("Descriptives (pre-registered, no verdicts)", lambda k: k.startswith("descriptives.")),
    ("H_Amplify ceiling: post-scoring check, not a pre-registered test (DEVIATIONS Entry 2)",
     lambda k: k.startswith("ceiling.")),
    ("Pre-registered, computed after scoring because the locked scorer did not output them (DEVIATIONS Entry 2)",
     lambda k: k.startswith("prereg_post.")),
]


def _src(s):
    if "file" in s:
        return f"`{s['file']}` " + "`/" + "/".join(str(p).replace("~", "~0").replace("/", "~1") for p in s["path"]) + "`"
    return f"computed: {s['computed']}"


def _cell(x):
    return str(x).replace("|", "\\|").replace("\n", " ")


def to_md(doc):
    m, vals = doc["_meta"], doc["values"]
    out = [f"# v0.40 values file ({m['n_values']:,} values)", "",
           "Machine-written by `osf/v40/scripts/values_v0_40.py`; do not edit by hand. Every figure in the v0.40 "
           "paper, report and site is read from `v40_values.json` (placeholder `{{v:<key>}}`), never typed.", "",
           f"Verdicts commit: `{m['verdicts_commit']}`", "", "## Inputs", "", "| File | SHA-256 |", "|---|---|"]
    out += [f"| `{i['file']}` | `{i['sha256']}` |" for i in m["inputs"].values()]
    out += ["", "## Rounding rules", "", "| Rule | Display |", "|---|---|"]
    out += [f"| {k} | {v} |" for k, v in m["rules"].items()]
    out += ["", "Source paths are JSON Pointers into the named file.", ""]
    done = set()
    for title, pred in SECTIONS:
        keys = [k for k in vals if k not in done and pred(k)]
        if not keys:
            continue
        out += [f"## {title}", "", "| Key | Display | Value | Rule | Source |", "|---|---|---|---|---|"]
        for k in keys:
            e = vals[k]
            out.append(f"| `{_cell(k)}` | {_cell(e['display'])} | {_cell(json.dumps(e['value']))} | {e['rule']} | "
                       f"{_cell(_src(e['source']))} |")
            done.add(k)
        out.append("")
    rest = [k for k in vals if k not in done]
    if rest:
        out += ["## Other", "", "| Key | Display | Value | Rule | Source |", "|---|---|---|---|---|"]
        out += [f"| `{_cell(k)}` | {_cell(vals[k]['display'])} | {_cell(json.dumps(vals[k]['value']))} | "
                f"{vals[k]['rule']} | {_cell(_src(vals[k]['source']))} |" for k in rest]
        out.append("")
    if m["skipped_lists"]:
        out += ["## Lists not flattened (per-item records, not figures)", ""]
        out += [f"- `{s['file']}` `/{'/'.join(map(str, s['path']))}` ({s['items']} items)" for s in m["skipped_lists"]]
        out.append("")
    return "\n".join(out)


def main(argv=None, root=ROOT, out_root=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    out_root = Path(out_root or root)
    try:
        doc = build(root)
    except Refused as e:
        print(f"REFUSED: {e} (nothing written)", file=sys.stderr)
        return 2
    js, md = to_json(doc), to_md(doc)
    pj, pm = out_root / OUT_JSON, out_root / OUT_MD
    if "--check" in argv:
        same = pj.exists() and pm.exists() and pj.read_text(encoding="utf-8") == js and \
            pm.read_text(encoding="utf-8") == md
        print("values file up to date" if same else "values file DIFFERS from a fresh build")
        return 0 if same else 1
    pj.parent.mkdir(parents=True, exist_ok=True)
    pj.write_text(js, encoding="utf-8")
    pm.write_text(md, encoding="utf-8")
    print(f"wrote {OUT_JSON} and {OUT_MD}: {doc['_meta']['n_values']} values")
    return 0


if __name__ == "__main__":
    sys.exit(main())
