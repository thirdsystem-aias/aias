#!/usr/bin/env python3
"""
code_v0_62.py -- AIAS(TM) v0.62 coder (French and Japanese answers), pre-registration r1 DRAFT, sections 4.3-4.4, 7.1.

The certified English matchers are NOT re-implemented. This module adds only the language pre-step of section 4.3
and the answer-word mapping of section 4.4, then hands the prepared answers to v0.42's coder
(osf/v42/scripts/code_t4_v0_42.py, run unchanged as a separate process on a prepared copy of the raw file, one
language at a time), which applies each category's certified matcher exactly as for t4.

Pre-step (prepare_text), in this order:
  1. Unicode NFC; full-width ASCII (U+FF01-U+FF5E) and half-width katakana (U+FF61-U+FF9F) by NFKC, run by run
     (ＢＭＷ -> BMW, ｿﾆｰ -> ソニー); ideographic space U+3000, no-break spaces U+00A0, U+202F -> ' '; typographic
     apostrophes U+2018, U+2019, U+02BC, U+FF07 -> "'"; URLs and Markdown link targets removed (strip_urls, the
     regular expressions of code_t4_v0_42.py, byte for byte).
  2. Alias canonicalisation (ALIASES from the alias table, longest alias first): every occurrence of a Japanese alias
     is replaced by ' <registry name> '. A multi-word alias matches with an optional separator (・ ･ space, half- or
     full-width) at each joint written with ・ in the table, and only when NOT preceded or followed by a katakana
     character (U+30A1-U+30FA, U+30FC), so that ソニー matches in ソニーの but コス not inside コスメ. Aliases written
     in kanji match as written. French spelling variants (unaccented forms) match case-insensitively as whole words.
  3. Script-boundary spacing: a space at every transition between a Latin letter or digit and a kana or CJK
     character (Python's \\b treats kana as word characters).
Answer words (Phase A, v0.19-v0.22 only): a leading oui / non (FR) or はい / いいえ (JA), after the pre-step and
ignoring leading Markdown marks and punctuation, is replaced by Yes / No; the certified parser then reads the answer.
v0.23 open answers are passed to the recognition judge as written (section 4.4).

MC_Alias: alias_hits() lists every match of a collision-prone alias with its context (exported for audit).
MC_Language: in_language() implements section 2.8's rule (JA: >= 50% of letters kana/CJK; FR: French function
words outnumber English ones among FR_WORDS + EN_WORDS).

Modes:
  --prepare RAW --out DIR    write DIR/v62_prepared_{fr,ja}.jsonl (prepared texts; the raw file is not changed)
                             and DIR/v62_alias_audit.csv. Coding then runs v0.42's coder on each prepared file:
                             python3 <v42>/code_t4_v0_42.py --raw DIR/v62_prepared_fr.jsonl --out DIR/fr  (and ja)
  The real raw file (osf/v62/data/v62_raw.jsonl) is refused unless tag v0.62-prereg-r1 is on origin.
"""
import argparse
import csv
import json
import os
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

ROOT = Path(os.environ.get("AIAS_ROOT", str(Path(__file__).resolve().parents[3]))).resolve()
V62 = ROOT / "osf/v62"
sys.path.insert(0, str(Path(__file__).resolve().parent))
import params_v0_62 as P  # noqa: E402

PREREG_TAG = "v0.62-prereg-r1"
REAL_RAW = V62 / "data/v62_raw.jsonl"
ALIAS_TABLE = V62 / "translations/brand_aliases_v0_62_r1.csv"
SUBS = ["v19", "v20", "v21", "v22", "v23"]

# ---- copied byte for byte from osf/v42/scripts/code_t4_v0_42.py (URL removal; checked by the tests) ----
MD_LINK_RE = re.compile(
    r"\[([^\]]*)\]\(\s*(?:<[^>]*>|(?:[^()\s]|\([^()\s]*\))+)(?:\s+(?:\"[^\"]*\"|'[^']*'))?\s*\)")
URL_RE = re.compile(r"https?://[^\s<>\"'\])]+", re.I)


def strip_urls(text):
    """Remove http(s):// addresses and the targets of Markdown links (link text is kept)."""
    if not text:
        return text or ""
    t = MD_LINK_RE.sub(r"\1", text)
    return URL_RE.sub(" ", t)
# ---- end of copy ----


class Refused(RuntimeError):
    pass


KATA = "ァ-ヺー"
SEP_CLASS = "[・･·・ 　]?"
WIDE_RE = re.compile("[！-ﾟ]+")
APOS_RE = re.compile("[‘’ʼ＇]")
SPACE_RE = re.compile("[  　]")
LATIN_CJK = re.compile(r"(?<=[A-Za-z0-9])(?=[぀-ヿ㐀-鿿])|(?<=[぀-ヿ㐀-鿿])(?=[A-Za-z0-9])")


def normalise(text):
    """Step 1 of the pre-step (without URL removal)."""
    t = unicodedata.normalize("NFC", text or "")
    t = WIDE_RE.sub(lambda m: unicodedata.normalize("NFKC", m.group(0)), t)
    t = SPACE_RE.sub(" ", t)
    return APOS_RE.sub("'", t)


def load_aliases(path=None):
    """[(substrate, registry name, alias, kind, collision_prone)], kind 'ja' or 'fr'."""
    out = []
    with open(path or ALIAS_TABLE, encoding="utf-8") as f:
        table = list(csv.DictReader(f))
    for r in table:
        for a in filter(None, r["ja_aliases"].split("|")):
            out.append((r["substrate"], r["brand"], a, "ja", r["ja_collision_prone"] == "yes"))
        for a in filter(None, r["fr_aliases"].split("|")):
            out.append((r["substrate"], r["brand"], a, "fr", False))
    return out


def alias_regex(alias, kind):
    if kind == "fr":
        return re.compile(r"(?<![^\W_])" + re.escape(alias) + r"(?![^\W_])", re.I)
    parts = [re.escape(p) for p in re.split("[・･]", alias)]
    body = SEP_CLASS.join(parts)
    # spelling variants of two loan words used in registry names (r1): ビューティ(ー) and コスメティ(ッ)クス
    body = body.replace("ビューティー", "ビューティ").replace("ビューティ", "ビューティー?")
    body = body.replace("コスメティックス", "コスメティクス").replace("コスメティクス", "コスメティッ?クス")
    if re.fullmatch(f"[{KATA}・･0-9]+", alias):
        return re.compile(f"(?<![{KATA}])" + body + f"(?![{KATA}])")
    return re.compile(body)                     # kanji (or mixed) aliases match as written


class Aliaser:
    def __init__(self, aliases=None):
        rows = load_aliases() if aliases is None else aliases
        # one canonical replacement per (alias, kind); longest first so that a long form wins over its parts
        self.rows = sorted(rows, key=lambda r: -len(r[2]))
        self.res = [(r, alias_regex(r[2], r[3])) for r in self.rows]

    def canonicalise(self, text, substrate=None, hits=None):
        """Replace aliases (of `substrate` only, if given) by ' <registry name> '. hits: list to collect
        (alias, brand, context) of collision-prone matches."""
        for (sub, brand, alias, kind, cp), rx in self.res:
            if substrate and sub != substrate:
                continue
            if hits is not None and cp:
                for m in rx.finditer(text):
                    hits.append((sub, brand, alias, text[max(0, m.start() - 30):m.end() + 30].replace("\n", " ")))
            text = rx.sub(" " + brand + " ", text)
        return text


def prepare_text(text, substrate=None, aliaser=None, hits=None, strip=True):
    """The full pre-step of section 4.3 for one answer."""
    t = normalise(text)
    if strip:
        t = strip_urls(t)
    t = (aliaser or _default_aliaser()).canonicalise(t, substrate, hits)
    return LATIN_CJK.sub(" ", t)


_AL = {}


def _default_aliaser():
    if "a" not in _AL:
        _AL["a"] = Aliaser()
    return _AL["a"]


LEAD_RE = {"fr": re.compile(r"^([\s*_#>\-•\"'«»(\[]*)(oui|non)(?![^\W_])", re.I),
           "ja": re.compile(r"^([\s*_#>\-•「『\"'(\[（]*)(いいえ|はい)")}


def map_answer_words(text, language):
    """Section 4.4: a leading oui/non or はい/いいえ -> Yes/No (v0.19-v0.22 yes/no answers only)."""
    t = normalise(text)
    rx = LEAD_RE.get(language)
    if not rx:
        return t
    m = rx.match(t)
    if not m:
        return t
    word = m.group(2).lower()
    yes = word in ("oui", "はい")
    return t[:m.start(2)] + ("Yes" if yes else "No") + t[m.end(2):]


FR_WORDS = ["le", "la", "les", "des", "du", "une", "est", "et", "pour", "avec", "dans", "qui", "que", "sont", "pas",
            "plus", "sur", "aux", "cette", "leur"]
EN_WORDS = ["the", "and", "is", "are", "for", "with", "of", "to", "in", "that", "this", "which", "their", "not",
            "more", "on", "from", "its", "by", "these"]


def in_language(text, language):
    """MC_Language rule of section 2.8 (fixed). JA: kana + CJK >= 50% of letters. FR: French function words
    outnumber English ones (ties and no function word -> not French)."""
    t = normalise(text)
    if language == "ja":
        letters = [c for c in t if c.isalpha()]
        if not letters:
            return False
        cjk = sum(1 for c in letters if "぀" <= c <= "ヿ" or "㐀" <= c <= "鿿")
        return cjk / len(letters) >= 0.5
    words = re.findall(r"[a-zàâçéèêëîïôûùüÿœæ]+", t.lower())
    fr = sum(w in FR_WORDS for w in words)
    en = sum(w in EN_WORDS for w in words)
    return fr > en


# --------------------------------------------------------------------------- raw handling
def _ls_remote_tag():
    r = subprocess.run(["git", "-C", str(ROOT), "ls-remote", "--tags", "origin", PREREG_TAG],
                       capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        raise Refused(f"git ls-remote failed ({r.stderr.strip()[:200]}); cannot verify tag {PREREG_TAG}")
    return r.stdout


def guard_real_raw(path):
    if Path(path).resolve() == REAL_RAW.resolve() and f"refs/tags/{PREREG_TAG}" not in _ls_remote_tag():
        raise Refused(f"refusing to read {REAL_RAW}: tag {PREREG_TAG} is not on origin")


def prepare_record(rec, aliaser=None, hits=None):
    """A raw line with its text prepared for v0.42's coder; `text_original` keeps the answer as received.
    Records of units removed by the headphones option keep their text (the scorer drops the units)."""
    out = dict(rec)
    lg, sub, text = rec.get("language"), rec.get("substrate"), rec.get("text") or ""
    out["text_original"] = text
    if rec.get("phase") == "B":
        out["text"] = prepare_text(text, sub, aliaser, hits)
    elif sub != "v23":
        out["text"] = map_answer_words(text, lg)
    # v0.23 Phase A: unchanged (the judge reads the answer as written)
    out["in_language"] = in_language(text, lg) if text.strip() else None
    return out


def prepare_raw(raw_path, out_dir, aliaser=None):
    guard_real_raw(raw_path)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    hits, n = [], {"fr": 0, "ja": 0}
    files = {lg: open(out_dir / f"v62_prepared_{lg}.jsonl", "w", encoding="utf-8") for lg in ("fr", "ja")}
    try:
        with open(raw_path, encoding="utf-8") as f:
            lines = f.readlines()
        for line in lines:
            if not line.strip():
                continue
            rec = json.loads(line)
            h = []
            p = prepare_record(rec, aliaser, h)
            hits += [(rec["call_id"],) + x for x in h]
            files[rec["language"]].write(json.dumps(p, ensure_ascii=False) + "\n")
            n[rec["language"]] += 1
    finally:
        for f in files.values():
            f.close()
    with open(out_dir / "v62_alias_audit.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["call_id", "substrate", "brand", "alias", "context"])
        w.writerows(hits)
    return n, len(hits)


def main(argv=None):
    ap = argparse.ArgumentParser(description="AIAS v0.62 coder pre-step (r1 draft)")
    ap.add_argument("--prepare", metavar="RAW", default=None)
    ap.add_argument("--out", default=str(V62 / "data/coded"))
    a = ap.parse_args(argv)
    if not a.prepare:
        ap.error("--prepare RAW is required")
    try:
        n, h = prepare_raw(a.prepare, a.out)
    except Refused as e:
        print(f"[v62] REFUSED: {e}", file=sys.stderr)
        return 3
    print(f"prepared {n} lines; {h} collision-prone alias matches exported -> {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
