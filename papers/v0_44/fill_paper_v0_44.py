#!/usr/bin/env python3
"""Fill the v0.44 paper template from the values file (numbers come from code, never typed).

Every {{v:KEY}} in papers/v0_44/v0_44_paper_template.md is replaced by the display string of
papers/v0_44/v44_values.json (unknown key -> exit, never a blank). {{table:NAME}} markers are replaced by
appendix tables generated from the same values. Writes papers/v0_44/v0_44_paper_draft.md and a provenance file
listing every key used with its value, display string and source.

Run from the worktree root:  python3 papers/v0_44/fill_paper_v0_44.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "papers/v0_44/v0_44_paper_template.md"
OUT = ROOT / "papers/v0_44/v0_44_paper_draft.md"
PROV = ROOT / "papers/v0_44/v0_44_paper_draft_provenance.json"
VALUES = ROOT / "papers/v0_44/v44_values.json"
INDS = ["INS", "HOT", "GRO", "QSR", "APR", "PHA", "CVF", "FAS"]
MODELS = ["claude-fable-5-2", "gpt-6-astra", "gemini-4-argon"]


def md_escape(s):
    return s.replace("|", "\\|").replace("*", "\\*").replace("_", "\\_")


def table_alias(V, used):
    used.add("alias.by_unit")
    rows = V["alias.by_unit"]["value"]
    labels = V["reg.labels"]["value"]
    used.add("reg.labels")
    out = ["| Industry | Unit | Matches | Aliases matched (count) |", "|---|---|---:|---|"]
    for r in rows:
        als = "; ".join(f"{md_escape(a)} ({k})" for a, k in r["aliases"])
        out.append(f"| {labels[r['industry']]} | {md_escape(r['brand'])} | {r['n']} | {als} |")
    out += ["", f": MC_Alias: case-sensitive alias matches per unit and alias ({V['alias.matches']['display']} matches in "
            f"{V['alias.answers']['display']} answers; `data/coded/v44_alias_audit.csv`, which also holds each match's sentence). "
            "Reported as pre-registered; not used to change any code."]
    used.update({"alias.matches", "alias.answers"})
    return "\n".join(out)


def table_d1tier(V, used):
    labels = V["reg.labels"]["value"]
    out = ["| Industry | Tier | Fable 5.2 | GPT-6 Astra | Gemini 4 Argon |", "|---|---|---:|---:|---:|"]
    for i in INDS:
        for t in ("L", "C", "S", "G"):
            ks = [f"D1.{m}.{i}.{t}.mean" for m in MODELS]
            if ks[0] not in V:
                continue
            used.update(ks)
            out.append(f"| {labels[i]} | {t} | " + " | ".join(V[k]["display"] for k in ks) + " |")
    out += ["", ": Mean recall Presence per model, industry and tier (descriptive 1, `<model>|<industry>|<tier>`). "
            "G = the industry's ghost (one unit)."]
    return "\n".join(out)


def table_d6(V, used):
    labels = V["reg.labels"]["value"]
    out = ["| Industry | Distinct | Ten most frequent candidate names (count) |", "|---|---:|---|"]
    for i in INDS:
        used.update({f"D6.{i}.distinct", f"D6.{i}.top10"})
        top = "; ".join(f"{md_escape(n)} ({k})" for n, k in V[f"D6.{i}.top10"]["value"])
        out.append(f"| {labels[i]} | {V[f'D6.{i}.distinct']['display']} | {top} |")
    out += ["", ": Candidate names in category answers that match no registry alias (descriptive 6; heuristic: bold spans "
            "and list-item heads of 1--6 words). Includes non-brand strings; descriptive only."]
    return "\n".join(out)


TABLES = {"alias": table_alias, "d1tier": table_d1tier, "d6": table_d6}


def main():
    vals = json.loads(VALUES.read_text(encoding="utf-8"))
    V = vals["values"]
    tpl = TEMPLATE.read_text(encoding="utf-8")
    keys = sorted(set(k.strip() for k in re.findall(r"\{\{v:([^}]+)\}\}", tpl)))
    missing = [k for k in keys if k not in V]
    if missing:
        sys.exit(f"ERROR: keys not in the values file: {missing}")
    # consistency guards between files (the paper must not print two different counts for one thing)
    assert V["unit.rated"]["value"] == V["H_Sep.n"]["value"], "unit table rated count != verdicts n_rated"
    assert V["raw.main_ok"]["value"] + V["raw.rerun_ok"]["value"] == V["MC_Complete.answered"]["value"]
    assert V["MC_Budget.spend_usd"]["value"] == V["D9.total"]["value"]
    used = set(keys)
    text = re.sub(r"\{\{v:([^}]+)\}\}", lambda m: V[m.group(1).strip()]["display"], tpl)
    text = re.sub(r"\{\{table:([a-z0-9]+)\}\}", lambda m: TABLES[m.group(1)](V, used), text)
    if "{{" in text:
        sys.exit("ERROR: unfilled template syntax remains")
    OUT.write_text(text, encoding="utf-8")
    prov = {"template": str(TEMPLATE.relative_to(ROOT)), "values_file": str(VALUES.relative_to(ROOT)),
            "values_inputs": vals["_meta"], "synthetic": False, "n_keys": len(used),
            "keys": {k: {"display": V[k]["display"], "value": V[k]["value"], "source": V[k]["source"]} for k in sorted(used)}}
    PROV.write_text(json.dumps(prov, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"filled {OUT.relative_to(ROOT)}: {len(used)} distinct value keys")


if __name__ == "__main__":
    main()
