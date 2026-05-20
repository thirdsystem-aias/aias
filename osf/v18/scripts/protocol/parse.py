"""
protocol/parse.py — canonical brand-mention parsing for Phase B

parse_brand_mentions() scans a Phase B response for occurrences of any
registry brand. Detection rules are protocol-canonical (v1.4) and must
be consistent across phases.

Detection rules:
  1. Case-insensitive
  2. Accent-insensitive (é → e, ç → c, ñ → n, etc.)
  3. Possessive-stripping ("MFK's" → "MFK")
  4. Word-boundary anchored (no partial substring matches inside other words)
  5. First-occurrence-wins per brand for de-duplication
  6. Aliases share the brand's mention slot — first canonical-or-alias hit wins
  7. Rank derived from enumerated-list position when present; prose-only
     mentions get rank None
"""

import re
import unicodedata


# ============================================================
# Main entry point
# ============================================================

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
        List of mention records (max one per brand):
        [
            {
                "canonical": str,           # canonical brand name
                "matched_surface": str,     # exact text that triggered the match
                "rank_in_response": int | None,
                "first_char_offset": int,
            }, ...
        ]
    """
    aliases = aliases or {}

    # Pre-strip possessives across the entire response so "MFK's" matches "MFK"
    text_stripped = strip_possessive(response_text)
    text_norm = normalize(text_stripped)

    # We keep an offset map so we can find the position in the ORIGINAL text
    # after normalization. Simpler approach: search the normalized text and
    # use offsets there for rank extraction against the original text (positions
    # are usually within a few chars of each other after the simple transforms
    # we apply; for rank extraction this is fine since lists are line-anchored).

    mentions = []
    for canonical in registry_canonical:
        surfaces = [canonical] + aliases.get(canonical, [])
        # Find earliest occurrence of any surface for this brand
        best_hit = None  # (offset, matched_surface)
        for surface in surfaces:
            surface_norm = normalize(strip_possessive(surface))
            # Word-boundary regex on normalized text
            pattern = r"\b" + re.escape(surface_norm) + r"\b"
            match = re.search(pattern, text_norm)
            if match:
                offset = match.start()
                if best_hit is None or offset < best_hit[0]:
                    best_hit = (offset, surface)

        if best_hit is None:
            continue

        offset, surface = best_hit
        rank = extract_list_position(text_stripped, offset)
        mentions.append({
            "canonical": canonical,
            "matched_surface": surface,
            "rank_in_response": rank,
            "first_char_offset": offset,
        })

    return mentions


# ============================================================
# Helpers
# ============================================================

def normalize(text: str) -> str:
    """Canonical text normalization for matching: lowercase + accent-strip."""
    text = text.strip().lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return text


def strip_possessive(text: str) -> str:
    """Strip trailing possessive markers ("MFK's" → "MFK", "Chanel's" → "Chanel")."""
    return re.sub(r"['\u2019]s\b", "", text)


def extract_list_position(response_text: str, char_offset: int) -> int | None:
    """
    If char_offset falls inside an enumerated list item (e.g.,
    "3. Maison Francis Kurkdjian ..."), return the list number. Otherwise None.

    Recognizes "N. ", "N) ", "(N) " at the start of the line containing the offset.
    Bullet markers ("- ", "* ", "• ") return None (not numerically ranked).
    """
    line_start = response_text.rfind("\n", 0, char_offset) + 1
    line_prefix = response_text[line_start:char_offset + 1]
    # Match enumeration at the start of the line: optional leading whitespace,
    # optional opening paren, digits, then "." or ")", then a space.
    match = re.match(r"\s*\(?(\d+)[.)]\s+", line_prefix)
    if match:
        return int(match.group(1))
    return None
