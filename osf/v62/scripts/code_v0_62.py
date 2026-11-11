#!/usr/bin/env python3
"""
code_v0_62.py -- AIAS(TM) v0.62 coder (Spanish, Korean and Chinese answers), pre-registration r2 DRAFT, sections 4.3-4.4, 7.1.

The certified English matchers are NOT re-implemented. This module adds only the language pre-step of section 4.3
and the answer-word mapping of section 4.4, then hands the prepared answers to v0.42's coder
(osf/v42/scripts/code_t4_v0_42.py, run unchanged as a separate process on a prepared copy of the raw file, one
language at a time), which applies each category's certified matcher exactly as for t4.

Pre-step (prepare_text), in this order (pre-registration r2, section 4.3):
  1. Unicode NFC; full-width ASCII, half-width katakana and half-width Hangul (U+FF01-U+FFDC) by NFKC, run by run
     (ＢＭＷ -> BMW); ideographic space U+3000, no-break spaces U+00A0, U+202F -> ' '; typographic apostrophes
     U+2018, U+2019, U+02BC, U+FF07 -> "'" (applied to both sides of gate P2); URLs and Markdown link targets removed
     (strip_urls, the regular expressions of code_t4_v0_42.py, byte for byte).
  2. Alias canonicalisation (ALIASES from the r2 alias table, longest alias first): every occurrence of a Korean or
     Chinese alias is replaced by ' <registry name> '. KO-1 / ZH-1: spaces, hyphens and middle dots at an alias's
     joints are optional. KO-2: a Hangul alias matches only when not preceded by a Hangul syllable and when followed by
     a non-Hangul character, the end, or a run of particles / copula forms (KO_PARTICLES) that ends before a
     non-Hangul character (소니의 matches; 코스 does not match inside 코스메틱). ZH-2: Han aliases match as written.
     Collision-prone aliases are counted, exported for audit (MC_Alias) and switched off in S-Alias.
  3. Script-boundary spacing: a space at every transition between a Latin letter or digit and a kana, Han or Hangul
     character (Python's \b treats these as word characters).
Answer words (Phase A, v0.19-v0.22 only): a leading sí/no (ES), 예/네 / 아니요/아니오/아니 (KO) or 是/是的 / 否/不是/不 (ZH),
after the pre-step's normalisation and ignoring leading Markdown marks and punctuation, is replaced by Yes / No;
the certified parser then reads the answer. v0.23 open answers are passed to the recognition judge as written.

MC_Alias: alias_hits() lists every match of a collision-prone alias with its context (exported for audit).
MC_Language: in_language() implements section 2.8's rule (KO: >= 50% of letters Hangul; ZH: >= 50% Han; ES:
Spanish function words outnumber English ones). MC_Script: zh_traditional() flags ZH answers with
Traditional-only characters (descriptive; no character conversion is applied).

Modes:
  --prepare RAW --out DIR    write DIR/v62_prepared_{es,ko,zh}.jsonl (prepared texts; the raw file is not changed)
                             and DIR/v62_alias_audit.csv. Coding then runs v0.42's coder on each prepared file:
                             python3 <v42>/code_t4_v0_42.py --raw DIR/v62_prepared_es.jsonl --out DIR/es  (and ko, zh)
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
ALIAS_TABLE = V62 / "translations/brand_aliases_v0_62_r2.csv"
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


LANGS = ("es", "ko", "zh")
HANGUL = "가-힣"                                        # precomposed Hangul syllables U+AC00-U+D7A3
HAN = "㐀-鿿"                                           # CJK ideographs (Ext. A + URO)
SEP_CLASS = "[ ·・･\\-－]?"                               # optional joint separator inside a KO/ZH alias
WIDE_RE = re.compile("[！-ￜ]+")                          # full-width ASCII, half-width katakana and Hangul (NFKC)
APOS_RE = re.compile("[‘’ʼ＇]")
SPACE_RE = re.compile("[  　]")
LATIN_CJK = re.compile(r"(?<=[A-Za-z0-9])(?=[぀-ヿ㐀-鿿가-힣])|(?<=[぀-ヿ㐀-鿿가-힣])(?=[A-Za-z0-9])")
# Korean particles and copula forms that may follow a brand name written in Hangul (section 4.3 rule KO-2).
KO_PARTICLES = ["에서", "으로", "처럼", "보다", "부터", "까지", "이나", "이랑", "하고", "께서", "입니다", "이며", "이고",
                "이다", "이에요", "예요", "이라는", "라는", "와", "과", "은", "는", "이", "가", "을", "를", "의", "에", "도",
                "만", "로", "나", "랑", "도"]
KO_TAIL = "(?:" + "|".join(sorted(set(KO_PARTICLES), key=len, reverse=True)) + ")"


def normalise(text):
    """Step 1 of the pre-step (without URL removal)."""
    t = unicodedata.normalize("NFC", text or "")
    t = WIDE_RE.sub(lambda m: unicodedata.normalize("NFKC", m.group(0)), t)
    t = SPACE_RE.sub(" ", t)
    return APOS_RE.sub("'", t)


def load_aliases(path=None):
    """[(substrate, registry name, alias, kind, collision_prone)], kind 'ko', 'zh' or 'es'."""
    out = []
    with open(path or ALIAS_TABLE, encoding="utf-8") as f:
        table = list(csv.DictReader(f))
    for r in table:
        for lg in ("ko", "zh"):
            for a in filter(None, r[lg + "_aliases"].split("|")):
                out.append((r["substrate"], r["brand"], a, lg, r[lg + "_collision_prone"] == "yes"))
        for a in filter(None, r.get("es_aliases", "").split("|")):
            out.append((r["substrate"], r["brand"], a, "es", False))
    return out


def alias_regex(alias, kind):
    """KO-1/ZH-1: spaces, hyphens and middle dots at an alias's joints are optional (any of them, or none).
    KO-2: a Hangul alias matches only when not preceded by a Hangul syllable and when followed by a non-Hangul
    character, the end, or a run of particles / copula forms (KO_PARTICLES) that is itself followed by a non-Hangul
    character or the end (소니의, 현대자동차에서는 match; 코스 does not match inside 코스메틱 or 디스코스).
    ZH-2: Han aliases match as written (Chinese does not separate words; collision-prone ones are audited).
    ES: whole word, case-insensitive (no ES alias in r2)."""
    if kind == "es":
        return re.compile(r"(?<![^\W_])" + re.escape(alias) + r"(?![^\W_])", re.I)
    parts = [re.escape(x) for x in re.split(r"[ ·・･\-－]+", alias) if x]
    body = SEP_CLASS.join(parts)
    if kind == "ko":
        return re.compile(f"(?<![{HANGUL}])" + body + f"(?=$|[^{HANGUL}]|{KO_TAIL}+(?:$|[^{HANGUL}]))")
    return re.compile(body)


class Aliaser:
    def __init__(self, aliases=None):
        rows = load_aliases() if aliases is None else aliases
        # one canonical replacement per (alias, kind); longest first so that a long form wins over its parts
        self.rows = sorted(rows, key=lambda r: -len(r[2]))
        self.res = [(r, alias_regex(r[2], r[3])) for r in self.rows]

    def canonicalise(self, text, substrate=None, hits=None, collision=True):
        """Replace aliases (of `substrate` only, if given) by ' <registry name> '. hits: list to collect
        (alias, brand, context) of collision-prone matches. collision=False switches collision-prone aliases off
        (sensitivity S-Alias)."""
        for (sub, brand, alias, kind, cp), rx in self.res:
            if substrate and sub != substrate:
                continue
            if cp and not collision:
                continue
            if hits is not None and cp:
                for m in rx.finditer(text):
                    hits.append((sub, brand, alias, text[max(0, m.start() - 30):m.end() + 30].replace("\n", " ")))
            text = rx.sub(" " + brand + " ", text)
        return text


def prepare_text(text, substrate=None, aliaser=None, hits=None, strip=True, collision=True):
    """The full pre-step of section 4.3 for one answer."""
    t = normalise(text)
    if strip:
        t = strip_urls(t)
    t = (aliaser or _default_aliaser()).canonicalise(t, substrate, hits, collision)
    return LATIN_CJK.sub(" ", t)


_AL = {}


def _default_aliaser():
    if "a" not in _AL:
        _AL["a"] = Aliaser()
    return _AL["a"]


_PFX = r"^([\s*_#>\-•\"'“”「『(\[（]*)"
LEAD_RE = {"es": re.compile(_PFX + r"(sí|si(?=\s*[,.!;:]|\s*$)|no)(?![^\W_])", re.I),
           "ko": re.compile(_PFX + f"(아니요|아니오|아니|예|네)(?![{HANGUL}])"),
           "zh": re.compile(_PFX + r"(不是|是的|否|是|不)(?=$|[\s，,。．.！!：:；;”\"）)])")}
YES = {"sí", "si", "예", "네", "是的", "是"}


def map_answer_words(text, language):
    """Section 4.4: a leading sí/no (ES), 예/네 / 아니요/아니오/아니 (KO), 是/是的 / 否/不是/不 (ZH) -> Yes/No
    (v0.19-v0.22 yes/no answers only). ZH 是 and 不 count only when followed by punctuation, space or the end
    (是一个… is left to the parser, which counts it as a non-answer)."""
    t = normalise(text)
    rx = LEAD_RE.get(language)
    if not rx:
        return t
    m = rx.match(t)
    if not m:
        return t
    word = m.group(2).lower()
    return t[:m.start(2)] + ("Yes" if word in YES else "No") + t[m.end(2):]


ES_WORDS = ["el", "la", "los", "las", "del", "una", "es", "y", "para", "con", "en", "que", "son", "por", "su", "sus",
            "más", "como", "pero", "muy"]
EN_WORDS = ["the", "and", "is", "are", "for", "with", "of", "to", "in", "that", "this", "which", "their", "not",
            "more", "on", "from", "its", "by", "these"]
# 24 frequent characters that exist only in Traditional script (their Simplified forms differ); MC_Script (2.8)
ZH_TRAD = set("們這說為對會來個時與國學經進過還開關機車體點當類")


def in_language(text, language):
    """MC_Language rule of section 2.8 (fixed). KO: Hangul >= 50% of letters. ZH: Han >= 50% of letters.
    ES: Spanish function words outnumber English ones among ES_WORDS + EN_WORDS (ties, none -> not Spanish).
    ('es' and 'en' share no word in the two lists.)"""
    t = normalise(text)
    if language in ("ko", "zh"):
        letters = [c for c in t if c.isalpha()]
        if not letters:
            return False
        lo, hi = ("가", "힣") if language == "ko" else ("㐀", "鿿")
        return sum(1 for c in letters if lo <= c <= hi) / len(letters) >= 0.5
    words = re.findall(r"[a-záéíóúñü]+", t.lower())
    es = sum(w in ES_WORDS for w in words)
    en = sum(w in EN_WORDS for w in words)
    return es > en


def zh_traditional(text):
    """MC_Script (section 2.8): True if a ZH answer contains any of the ZH_TRAD characters."""
    return any(c in ZH_TRAD for c in text or "")


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
    out["zh_traditional"] = zh_traditional(text) if lg == "zh" else None
    return out


def prepare_raw(raw_path, out_dir, aliaser=None):
    guard_real_raw(raw_path)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    hits, n = [], {lg: 0 for lg in LANGS}
    files = {lg: open(out_dir / f"v62_prepared_{lg}.jsonl", "w", encoding="utf-8") for lg in LANGS}
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
    ap = argparse.ArgumentParser(description="AIAS v0.62 coder pre-step (r2 draft)")
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
