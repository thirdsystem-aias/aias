#!/usr/bin/env python3
"""
ssrn_packet_hook_v1_12.py -- generates the v1.12 SSRN submission packet from the FILLED paper and checks it.

Runs the programme's scripts/generate_ssrn_packet.py (unchanged) on papers/v1_12/v1_12_ssrn_paper_draft.md, then
checks the packet against the paper (CLAUDE.md, pre-registration discipline step 8: "check its title and abstract
against the paper: the scaffolded v0.23 and v0.37 packets carried another phase's text"):

  - title  == the paper's YAML title + ": " + subtitle
  - abstract == the paper's Abstract section, plain-text cleaned exactly as the generator cleans it, and free of
    LaTeX residue (backslashes, dollar signs, underscores) and of template syntax
  - keywords contain the five standing keywords (CLAUDE.md, SSRN packet template)
  - JEL codes found (the paper's inline label is exactly **JEL codes:**)
  - the Declaration of Interest is the paper's COI paragraph (the only place the employer appears)
  - no "[... NOT FOUND]" marker anywhere in the packet

Usage (real run):   python3 papers/v1_12/ssrn_packet_hook_v1_12.py
Synthetic test:     python3 papers/v1_12/ssrn_packet_hook_v1_12.py --paper /tmp/v112_pipeline_test/paper/v1_12_ssrn_paper_draft.md \
                        --output /tmp/v112_pipeline_test/paper/ssrn_submission_packet_v1_12.md
Exit 0 when every check passes, 1 otherwise.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
GEN = ROOT / "scripts" / "generate_ssrn_packet.py"
STANDING_KEYWORDS = ["AI availability", "brand availability", "AIAS", "pre-registration", "Ehrenberg-Bass"]


def block(packet, heading):
    m = re.search(rf"### {re.escape(heading)}.*?\n```\n(.*?)\n```", packet, re.DOTALL)
    return m.group(1).strip() if m else None


def main(argv=None):
    ap = argparse.ArgumentParser(description="Generate and check the v1.12 SSRN packet")
    ap.add_argument("--paper", type=Path, default=HERE / "v1_12_ssrn_paper_draft.md")
    ap.add_argument("--output", type=Path, default=HERE / "ssrn_submission_packet_v1_12.md")
    a = ap.parse_args(argv)
    r = subprocess.run([sys.executable, str(GEN), "--phase", "v1.12", "--paper", str(a.paper), "--root", str(ROOT),
                        "--output", str(a.output)], capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode:
        print(r.stderr, file=sys.stderr)
        return 1
    sys.path.insert(0, str(ROOT / "scripts"))
    import generate_ssrn_packet as G
    src = a.paper.read_text(encoding="utf-8")
    yaml, body = G.extract_frontmatter(src)
    packet = a.output.read_text(encoding="utf-8")
    problems = []
    title = f"{yaml.get('title')}: {yaml.get('subtitle')}"
    if block(packet, "Title (paste verbatim") != title:
        problems.append(f"title differs from the paper: {block(packet, 'Title (paste verbatim')!r} vs {title!r}")
    abstract = G.clean_for_plaintext(re.sub(r"\n+", " ", G.extract_section(body, r"Abstract\b") or "").strip())
    pa = block(packet, "Abstract (paste verbatim")
    if pa != abstract:
        problems.append("abstract differs from the paper's Abstract section")
    if pa and (re.search(r"[\\$]|\{\{|\{%", pa) or "_" in pa):
        problems.append(f"abstract carries LaTeX or template residue: {pa[:120]!r}...")
    kw = block(packet, "Keywords (paste verbatim") or ""
    for k in STANDING_KEYWORDS:
        if k not in kw:
            problems.append(f"standing keyword missing: {k}")
    if not block(packet, "JEL codes (paste verbatim") or "JEL NOT FOUND" in packet:
        problems.append("JEL codes not found (the label must read exactly **JEL codes:**)")
    coi = block(packet, "Declaration of Interest (paste verbatim") or ""
    if "Samsung Electronics America" not in coi or "Denon" not in coi:
        problems.append("Declaration of Interest is not the paper's COI paragraph")
    if re.search(r"\[[A-Z ]+NOT FOUND", packet):
        problems.append("a field was not found: " + ", ".join(re.findall(r"\[[A-Z ]+NOT FOUND[^\]]*\]", packet)))
    for p in problems:
        print("PACKET CHECK FAIL:", p)
    print(f"packet {a.output}: {'all checks passed' if not problems else f'{len(problems)} problem(s)'}")
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
