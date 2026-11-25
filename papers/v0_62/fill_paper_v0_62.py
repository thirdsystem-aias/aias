#!/usr/bin/env python3
"""Fill the v0.62 paper template from the values file (numbers come from code, never typed).

Forked from papers/v0_44/fill_paper_v0_44.py (branch v0.44). Every {{v:KEY}} in papers/v0_62/v0_62_paper_template.md
is replaced by the display string of papers/v0_62/v62_values.json (unknown key -> exit, never a blank). Writes
papers/v0_62/v0_62_paper_draft.md and a provenance file listing every key used with its value, display string and
source, and the keys used in the abstract.

Run from the worktree root:  python3 papers/v0_62/fill_paper_v0_62.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "papers/v0_62/v0_62_paper_template.md"
OUT = ROOT / "papers/v0_62/v0_62_paper_draft.md"
PROV = ROOT / "papers/v0_62/v0_62_paper_draft_provenance.json"
VALUES = ROOT / "papers/v0_62/v62_values.json"
KEY = re.compile(r"\{\{v:([^}]+)\}\}")


def abstract_keys(tpl):
    m = re.search(r"# Abstract \{-\}\n(.*?)\n\*\*Keywords", tpl, re.DOTALL)
    return [k.strip() for k in KEY.findall(m.group(1))]


def main():
    vals = json.loads(VALUES.read_text(encoding="utf-8"))
    V = vals["values"]
    tpl = TEMPLATE.read_text(encoding="utf-8")
    keys = sorted(set(k.strip() for k in KEY.findall(tpl)))
    missing = [k for k in keys if k not in V]
    if missing:
        sys.exit(f"ERROR: keys not in the values file: {missing}")
    # consistency guards (the paper must not print two different figures for one thing)
    assert V["raw.ok"]["value"] == V["design.expected"]["value"]
    assert V["raw.B"]["value"] + V["raw.A"]["value"] == V["raw.ok"]["value"]
    assert abs(V["cost.spend"]["value"] - V["raw.cost_sum"]["value"]) < 5e-4
    text = KEY.sub(lambda m: V[m.group(1).strip()]["display"], tpl)
    if "{{" in text:
        sys.exit("ERROR: unfilled template syntax remains")
    OUT.write_text(text, encoding="utf-8")
    ab = []
    for k in abstract_keys(tpl):
        if k not in ab:
            ab.append(k)
    prov = {"template": str(TEMPLATE.relative_to(ROOT)), "values_file": str(VALUES.relative_to(ROOT)),
            "values_inputs": vals["_meta"], "synthetic": False, "n_keys": len(keys), "abstract_keys": ab,
            "keys": {k: {"display": V[k]["display"], "value": V[k]["value"], "source": V[k]["source"]} for k in keys}}
    PROV.write_text(json.dumps(prov, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"filled {OUT.relative_to(ROOT)}: {len(keys)} distinct value keys ({len(ab)} in the abstract)")


if __name__ == "__main__":
    main()
