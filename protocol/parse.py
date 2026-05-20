"""
protocol/parse.py — canonical brand-mention parsing for Phase B

parse_brand_mentions() scans a Phase B response for occurrences of any
registry brand. Detection rules are protocol-canonical and must be
consistent across phases.

Detection rules (v1.4 canonical):
  1. Case-insensitive match
  2. Accent-insensitive match (é → e, ç → c, ñ → n, etc.)
  3. Possessive-stripping ("MFK's" → "MFK")
  4. Word-boundary anchored (no partial substring matches inside other words)
  5. First-occurrence-wins per brand for de-duplication
  6. Rank derived from enumerated-list position when the response contains
     a numbered/bulleted list; prose-only mentions get rank None

ONE-TIME LIFT: The actual matching logic (regex patterns, list-position
extraction) is in your existing v17 acquire_phase_b script. Lift the
function body here once. Future phases inherit.
"""

import re
import unicodedata


def parse_brand_mentions(
    response_text: str,
    registry_canonical: list[str],
    aliases: dict[str, list[str]] | None = None,
) -> list[dict]:
    """
    Scan `response_text` for mentions of each brand in `registry_canonical`.

    Args:
        response_text: raw model response from Phase B
        registry_canonical: list of canonical brand names to scan for
        aliases: optional {canonical: [alias1, alias2, ...]} expansion map

    Returns:
        List of mention records, one per detected brand (max one per brand):
        [
            {
                "canonical": str,           # canonical brand name
                "matched_surface": str,     # exact text that triggered the match
                "rank_in_response": int | None,  # 1-indexed enumeration position
                "first_char_offset": int,   # for de-duplication and rank tie-break
            },
            ...
        ]
    """
    raise NotImplementedError(
        "ONE-TIME LIFT: Copy parse_brand_mentions() body from your v17 "
        "acquire_phase_b script. Detection rules are protocol-canonical "
        "— do not reimplement, just port."
    )


# ============================================================
# Helpers — already implemented; v17 lift only needs the main function
# ============================================================

def normalize(text: str) -> str:
    """Canonical text normalization for matching: lowercase + accent-strip."""
    text = text.strip().lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return text


def strip_possessive(text: str) -> str:
    """Strip trailing possessive markers for matching ("MFK's" → "mfk")."""
    return re.sub(r"['\u2019]s\b", "", text)


def extract_list_position(response_text: str, char_offset: int) -> int | None:
    """
    Heuristic: if char_offset falls inside an enumerated list item (e.g.,
    "3. Maison Francis Kurkdjian ..."), return the list number. Otherwise None.

    Recognizes patterns:
      "1. ", "1) ", "(1) ", "- ", "* ", "• " at start of line.
    """
    # Find the start of the line containing char_offset
    line_start = response_text.rfind("\n", 0, char_offset) + 1
    line_prefix = response_text[line_start:char_offset + 1]
    match = re.match(r"\s*(?:\(?(\d+)[.)]\s+)", line_prefix)
    if match:
        return int(match.group(1))
    return None
