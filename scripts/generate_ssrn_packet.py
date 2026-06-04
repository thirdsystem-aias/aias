#!/usr/bin/env python3
"""
generate_ssrn_packet.py — Auto-emit SSRN submission packet from paper YAML.

Reads the phase's SSRN paper draft, extracts the title / subtitle / abstract /
keywords / JEL codes from its YAML frontmatter (or Abstract section), and
combines those with the program's standing constants (subject classifications,
COI boilerplate, declarations) to produce a paste-ready submission packet.

The packet mirrors the structure of ssrn_submission_packet_v0_22.md exactly,
so an operator can submit by copying each block into the SSRN webform fields.

Inputs:
  papers/<phase>/<phase>_ssrn_paper_draft.md  — paper source (YAML + body)

Outputs:
  papers/<phase>/ssrn_submission_packet_<phase>.md

Constants (program-wide):
  - Subject classifications (7 eJournals, identical across all AIAS phases)
  - COI boilerplate template (Samsung tier-2/3 disclosure, customized per-phase
    by reading the paper's Declarations section verbatim)
  - Funder / Ethics / Author block (program-wide constants)

Usage:
    python3 scripts/generate_ssrn_packet.py --phase v0.23
    python3 scripts/generate_ssrn_packet.py --paper papers/v0_23/v0_23_ssrn_paper_draft.md
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

AIAS_ROOT = Path.home() / "aias"

# ----- Program-wide constants (memory #21 + memory #18) ----------------------

SUBJECT_CLASSIFICATIONS = [
    "Marketing eJournal",
    "Marketing Strategy eJournal",
    "Consumer Behavior eJournal",
    "Advertising & Marketing Communication eJournal",
    "Information Systems eJournal",
    "Artificial Intelligence eJournal",
    "Decision-Making Under Risk & Uncertainty eJournal",
]

AUTHOR_BLOCK = """\
Pablo Ulpiano González Castro

School of Visual Arts (SVA), MPS Branding Program
New York, NY, United States

Third System™ (research entity; data archive and methodology venue)
thirdsystem.ai

Email: pablou@pablou.com
Website: pablou.com
ORCID: 0009-0003-8968-9990"""

FUNDER = "Self-funded."

ETHICS = (
    "Not applicable. The research uses public LLM APIs and standard prompt "
    "batteries; no human subjects, no personal data, no protected populations."
)


# ----- YAML frontmatter parsing ---------------------------------------------

def extract_frontmatter(src: str) -> tuple[dict[str, str], str]:
    """Return (yaml_dict, body). YAML values are kept as raw strings, NOT parsed."""
    m = re.match(r"\A---\s*\n(.*?)\n---\s*\n", src, re.DOTALL)
    if not m:
        return {}, src
    yaml_block = m.group(1)
    body = src[m.end():]

    # Simple key: value parsing. Block scalars (key: |) handled by joining lines
    # until next top-level key.
    yaml_dict = {}
    lines = yaml_block.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        m_kv = re.match(r"^([a-zA-Z_-]+):\s*(.*)$", line)
        if m_kv:
            key, val = m_kv.group(1), m_kv.group(2).strip()
            # Strip surrounding quotes for single-line values
            if val.startswith('"') and val.endswith('"'):
                val = val[1:-1]
            elif val.startswith("'") and val.endswith("'"):
                val = val[1:-1]
            yaml_dict[key] = val
            i += 1
        else:
            i += 1
    return yaml_dict, body


def extract_section(body: str, heading_pattern: str) -> str | None:
    """Extract content between a markdown heading and the next boundary.

    The boundary is whichever comes first: (a) next markdown heading at any
    level, or (b) next inline bold field like '**Keywords:**' or '**JEL codes:**'
    that pandoc treats as a distinct labeled paragraph. This matters because
    the AIAS paper pattern places Keywords/JEL/Paper-status as inline bold
    paragraphs immediately after the abstract section content; without (b),
    extract_section greedily slurps those into the abstract.
    """
    pat = re.compile(
        rf"^#+ {heading_pattern}.*?$\n(.*?)(?=^#+ |\n\*\*[A-Z][A-Za-z ]+:\*\*|\Z)",
        re.MULTILINE | re.DOTALL | re.IGNORECASE,
    )
    m = pat.search(body)
    return m.group(1).strip() if m else None


def extract_inline_field(body: str, label: str) -> str | None:
    """Extract '**Label:** value' from body.

    Value terminates at: next inline bold field, next markdown heading, or
    a blank line followed by anything other than a continuation.
    """
    pat = re.compile(
        rf"\*\*{re.escape(label)}:\*\*\s*(.+?)(?=\n\*\*[A-Z]|\n#+ |\n\n[A-Z]|\Z)",
        re.DOTALL,
    )
    m = pat.search(body)
    return m.group(1).strip() if m else None


# ----- Packet emission -------------------------------------------------------

def generate_packet(phase_display: str, phase_snake: str,
                    paper_md_path: Path) -> str:
    """Build the full packet markdown text."""
    src = paper_md_path.read_text(encoding="utf-8")
    yaml, body = extract_frontmatter(src)

    # Required fields with sensible fallbacks
    title = yaml.get("title", "[TITLE NOT FOUND IN YAML]")
    subtitle = yaml.get("subtitle", "")
    date_prepared = yaml.get("date", "") or "[DATE NOT FOUND IN YAML]"

    # OSF deposit segment: collapse v0_NN -> vNN (e.g. v0_30 -> v30) for phase
    # trees; keep methodology-line stems as-is (v1_7 -> v1_7, matching osf/v1_7).
    osf_seg = (phase_snake.replace("v0_", "v").replace("_", "")
               if phase_snake.startswith("v0_") else phase_snake)

    # Abstract: prefer markdown `# Abstract {-}` section, fallback to YAML
    abstract = extract_section(body, r"Abstract\b") or yaml.get("abstract", "")
    abstract = re.sub(r"\n+", " ", abstract).strip()

    # Keywords + JEL: inline bold fields after abstract
    keywords = extract_inline_field(body, "Keywords") or "[KEYWORDS NOT FOUND]"
    keywords = re.sub(r"\s+", " ", keywords).strip()

    jel = extract_inline_field(body, "JEL codes") or "[JEL NOT FOUND]"
    jel = re.sub(r"\s+", " ", jel).strip()

    # Strip trailing period from JEL for the bare-codes paste version
    jel_codes_only = re.sub(r"\s*\(primary\)|\s*\(secondary\)|\.$", "", jel)
    jel_codes_only = re.sub(r",\s*", "; ", jel_codes_only)

    # COI / Data-and-code availability: lift verbatim from Declarations.
    # The AIAS paper convention places these as inline bold fields with a
    # trailing PERIOD ("**Conflict of interest.** ...") under a "# Declarations"
    # heading, not as standalone headings — so fall back to that form.
    def _decl_field(label: str) -> str | None:
        # matches "**Label.**" or "**Label:**", value runs to next bold field/heading
        pat = re.compile(
            rf"\*\*{re.escape(label)}[.:]\*\*\s*(.+?)"
            rf"(?=\n\*\*[A-Z]|\n#+ |\Z)",
            re.DOTALL,
        )
        m = pat.search(body)
        return re.sub(r"\s+", " ", m.group(1)).strip() if m else None

    coi = (extract_section(body, r"Conflict of interest")
           or _decl_field("Conflict of interest")
           or "[COI NOT FOUND]")
    coi = coi.strip()

    data_avail = (extract_section(body, r"Data and code availability")
                  or _decl_field("Data and code availability")
                  or _decl_field("Data availability")
                  or "")
    data_avail = data_avail.strip()

    subject_class_block = "\n".join(f"{i}. **{n}**"
                                     for i, n in enumerate(SUBJECT_CLASSIFICATIONS, 1))

    citation_template = (
        f"González Castro, P. U. (2026). {title}. "
        f"SSRN Working Paper [ABSTRACT_ID]."
    )

    packet = f"""\
# SSRN Submission Packet — AIAS™ {phase_display}

**Paper:** {title}
**File to upload:** `papers/{phase_snake}/{phase_snake}_ssrn_paper.pdf`
**Submission target:** SSRN — papers.ssrn.com → Submit a paper
**Date prepared:** {date_prepared}

---

## Step 1 — Paper type

- **Working Paper**

## Step 2 — Document Settings

- **Document type:** Article
- **License:** All rights reserved
- **Display abstract:** Yes
- **Allow citations:** Yes
- **Allow downloads:** Yes

---

## Step 3 — Paper details

### Title (paste verbatim)

```
{title}
```

### Subtitle (paste verbatim)

```
{subtitle}
```

### Abstract (paste verbatim — matches paper page 2)

```
{abstract}
```

### Keywords (paste verbatim, semicolon-separated)

```
{keywords}
```

### JEL codes (paste verbatim)

```
{jel_codes_only}
```

**JEL rationale (for your reference):** {jel}

---

## Step 4 — Subject classifications (select up to 7)

Select these networks/eJournals on the SSRN classification picker:

{subject_class_block}

(Same classification set as v0.16–v0.21 papers for consistency.)

---

## Step 5 — Authors, affiliations, contact

```
{AUTHOR_BLOCK}
```

---

## Step 6 — Declarations (Conflict of Interest, Funding, Ethics)

### Declaration of Interest (paste verbatim)

```
{coi}
```

### Funder (paste verbatim)

```
{FUNDER}
```

### Ethics statement (paste verbatim)

```
{ETHICS}
```

### Data and code availability (paste verbatim)

```
{data_avail}
```

---

## Step 7 — Final review & upload

- **File:** `papers/{phase_snake}/{phase_snake}_ssrn_paper.pdf`
- **Cover letter:** Not required for SSRN Working Paper submissions.
- **Suggested citation (post-submission, fill in SSRN abstract ID):**

```
{citation_template}
```

---

## Post-submission checklist

1. **Capture SSRN abstract ID** when SSRN returns it (URL format: `https://ssrn.com/abstract={{ID}}`).
2. **Update memory:** add the {phase_display} SSRN abstract ID entry to the recent_updates section of userMemories.
3. **Run final OSF deposit:** `python3 ~/aias/scripts/osf_upload.py ~/aias/osf/{osf_seg} {osf_seg}`
4. **Cross-citation** in next phase: this {phase_display} SSRN ID gets added to next phase's paper bibliography upstream-phases line.

---

**End of submission packet — {phase_display} ready to upload.**
"""
    return packet


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Auto-emit SSRN submission packet from paper YAML."
    )
    parser.add_argument("--phase", default=None,
                        help="Phase version, e.g. 'v0.23'. Used to locate paper file.")
    parser.add_argument("--paper", default=None,
                        help="Explicit paper draft .md path (overrides --phase).")
    parser.add_argument("--root", default=str(AIAS_ROOT),
                        help=f"AIAS project root. Default: {AIAS_ROOT}")
    parser.add_argument("--output", default=None,
                        help="Output packet .md path. Default: papers/<phase>/ssrn_submission_packet_<phase>.md")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()

    if args.paper:
        paper_md = Path(args.paper).expanduser().resolve()
        if args.phase:
            phase_display = args.phase.replace("_", ".")
            phase_snake = phase_display.replace(".", "_")
        else:
            m = re.search(r"(v\d+_\d+)", paper_md.name)
            if not m:
                print(f"ERROR: cannot infer phase from paper filename {paper_md.name}; use --phase", file=sys.stderr)
                return 2
            phase_snake = m.group(1)
            phase_display = phase_snake.replace("_", ".")
    elif args.phase:
        phase_display = args.phase.replace("_", ".")
        phase_snake = phase_display.replace(".", "_")
        paper_md = root / "papers" / phase_snake / f"{phase_snake}_ssrn_paper_draft.md"
    else:
        print("ERROR: provide --phase or --paper", file=sys.stderr)
        return 2

    if not paper_md.exists():
        print(f"ERROR: paper draft not found at {paper_md}", file=sys.stderr)
        return 2

    print(f"[generate_ssrn_packet] reading: {paper_md}")
    packet = generate_packet(phase_display, phase_snake, paper_md)

    if args.output:
        out_path = Path(args.output).expanduser().resolve()
    else:
        out_path = paper_md.parent / f"ssrn_submission_packet_{phase_snake}.md"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(packet, encoding="utf-8")
    print(f"[generate_ssrn_packet] ✓ wrote {out_path}")
    print(f"[generate_ssrn_packet]   {len(packet):,} chars, "
          f"{len(packet.split(chr(10))):,} lines")
    return 0


if __name__ == "__main__":
    sys.exit(main())
