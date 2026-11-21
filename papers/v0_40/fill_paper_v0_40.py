#!/usr/bin/env python3
"""Fill the v0.40 paper template from the values file (runner upgrade 2: numbers come from code).

Every {{v:KEY}} in papers/v0_40/v0_40_ssrn_paper_template.md is replaced by values_v0_40.fill() with the display
string of osf/v40/v40_values.json (unknown key -> KeyError, never a blank). The author's correspondence line is
copied from the standard author block of the last shipped phase paper (papers/v0_37/v0_37_ssrn_paper_draft.md).
Writes papers/v0_40/v0_40_ssrn_paper_draft.md and a provenance file listing every key used with its value,
display string and source.

Run from the repo or worktree root:  python3 papers/v0_40/fill_paper_v0_40.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "osf/v40/scripts"))
import values_v0_40 as V  # noqa: E402

TEMPLATE = ROOT / "papers/v0_40/v0_40_ssrn_paper_template.md"
OUT = ROOT / "papers/v0_40/v0_40_ssrn_paper_draft.md"
PROV = ROOT / "papers/v0_40/v0_40_ssrn_paper_draft_provenance.json"
AUTHOR_SRC = ROOT / "papers/v0_37/v0_37_ssrn_paper_draft.md"


def correspondence_line():
    for line in AUTHOR_SRC.read_text(encoding="utf-8").splitlines():
        if line.startswith("Correspondence:"):
            return line if line.rstrip().endswith("\\\\") else line.rstrip() + "\\\\"
    sys.exit(f"ERROR: no Correspondence line in {AUTHOR_SRC}")


def main():
    values = json.loads((ROOT / V.OUT_JSON).read_text(encoding="utf-8"))
    tpl = TEMPLATE.read_text(encoding="utf-8")
    keys = sorted(set(k.strip() for k in re.findall(r"\{\{v:([^}]+)\}\}", tpl)))
    missing = [k for k in keys if k not in values["values"]]
    if missing:
        sys.exit(f"ERROR: keys not in the values file: {missing}")
    text = V.fill(tpl, values).replace("{{AUTHOR_CORRESPONDENCE}}", correspondence_line())
    if "{{" in text:
        sys.exit("ERROR: unfilled template syntax remains")
    OUT.write_text(text, encoding="utf-8")
    prov = {"template": str(TEMPLATE.relative_to(ROOT)), "values_file": V.OUT_JSON,
            "values_inputs": values["_meta"]["inputs"], "synthetic": False, "n_keys": len(keys),
            "keys": {k: {"display": values["values"][k]["display"], "value": values["values"][k]["value"],
                         "source": values["values"][k]["source"]} for k in keys}}
    PROV.write_text(json.dumps(prov, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"filled {OUT.relative_to(ROOT)}: {len(keys)} distinct value keys")


if __name__ == "__main__":
    main()
