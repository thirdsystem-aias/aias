"""
report_code.py - Third System(TM) report catalogue codes (decision 14; Pablo, Nov 13, 2026, 7:13 am).

Every report carries a catalogue code, so each one is easy to file, cite and find:

    TS-{TYPE}-{STUDY}-{REV}        TS-FL-v0.40-r1 · TS-SY-AIAS2.0-r4 · TS-CS-v0.22-r1 · TS-BR-v0.44-r1

  TYPE   FL Flagship (Tier 1) · SY Synthesis report · CS Category study (Tier 2) ·
         BR Brief or snapshot (Tier 3) · DG Diagnostic (TS-DG-{client code}-r1; client work stays private)
  STUDY  the program's own identifier, as in git tags (v0.22, v1.9; AIAS2.0 for the synthesis)
  REV    the report revision: r1, r2, ...

Register: brand/report_specs.json report_catalogue.entries (code, title, date, tier, git tag, OSF path,
SHA-256 of the PDF). A code is never reused: a new revision takes the study's next rN, and the earlier
code stays valid for the earlier PDF. Published reports are registered without re-rendering; a
report's code appears on the PDF only from its next render: on the last page (Tier 1: the closing band;
Tiers 2 and 3: the last footer line, "thirdsystem.ai · TS-CS-v0.22-r1"), in the Citation block, in the
PDF metadata (Subject and Keywords) and in the file name, TS-CS-v0.22-r1_<title-slug>.pdf.

The website is always printed in lower case ("thirdsystem.ai"), in footers, colophon, closing band
and caps lines alike: upper_keep_website() and website_lower() see to it.

preflight() is the pre-flight addition: the last page shows the website in lower case and the right
code; the code matches the register, the file name and the PDF metadata; and it is not already in use.
"""

from __future__ import annotations

import functools
import hashlib
import json
import os
import re
import unicodedata
from pathlib import Path
from typing import Iterable, Sequence

__all__ = [
    "TYPES", "TYPE_TIER", "ReportCodeError", "make_code", "parse_code", "title_slug", "file_name",
    "load_specs", "catalogue", "registered_hashes", "next_revision", "check_code", "validate_catalogue",
    "pdf_subject", "pdf_keywords", "cite", "website", "website_lower", "upper_keep_website",
    "sha256_file", "preflight",
]

TYPES = {
    "FL": "Flagship (Tier 1)",
    "SY": "Synthesis report",
    "CS": "Category study (Tier 2)",
    "BR": "Brief or snapshot (Tier 3)",
    "DG": "Diagnostic",
}
# Tier fixed by the type; SY and DG take the tier of the document (the AIAS syntheses are Tier 1).
TYPE_TIER = {"FL": 1, "CS": 2, "BR": 3}

_STUDY = r"[A-Za-z0-9](?:[A-Za-z0-9.]*[A-Za-z0-9])?"
CODE_RE = re.compile(r"^TS-(" + "|".join(TYPES) + r")-(" + _STUDY + r")-r([1-9][0-9]*)$")
_SHA = re.compile(r"^[0-9a-f]{64}$")


class ReportCodeError(ValueError):
    """A report code that is malformed, already registered for another PDF, or out of sequence."""


# ---------------------------------------------------------------------------
# Format
# ---------------------------------------------------------------------------

def parse_code(code: str) -> dict:
    """{'code', 'type', 'study', 'rev'} of a well-formed code; ReportCodeError otherwise."""
    m = CODE_RE.match(code or "")
    if not m:
        raise ReportCodeError(f"not a report code TS-{{TYPE}}-{{STUDY}}-r{{N}} "
                              f"(TYPE one of {', '.join(TYPES)}): {code!r}")
    return {"code": code, "type": m.group(1), "study": m.group(2), "rev": int(m.group(3))}


def make_code(kind: str, study: str, rev: int) -> str:
    """Build and validate a code, e.g. make_code('CS', 'v0.22', 1) == 'TS-CS-v0.22-r1'."""
    code = f"TS-{kind}-{study}-r{int(rev)}"
    parse_code(code)
    return code


def title_slug(title: str, max_len: int = 60) -> str:
    """Lower-case ASCII slug of a title: words joined by hyphens, cut at a word boundary."""
    text = re.sub(r"<[^>]+>", " ", title or "")
    text = text.replace("&amp;", " and ").replace("&", " and ").replace("™", "")
    text = re.sub(r"['’]", "", text)
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii").lower()
    words = re.findall(r"[a-z0-9]+", text)
    slug = ""
    for w in words:
        nxt = f"{slug}-{w}" if slug else w
        if len(nxt) > max_len and slug:
            break
        slug = nxt
    return slug


def file_name(code: str, title: str) -> str:
    """The PDF's file name: CODE_<title-slug>.pdf."""
    parse_code(code)
    slug = title_slug(title)
    if not slug:
        raise ReportCodeError(f"{code}: the title gives an empty slug: {title!r}")
    return f"{code}_{slug}.pdf"


# ---------------------------------------------------------------------------
# The register: brand/report_specs.json report_catalogue.entries
# ---------------------------------------------------------------------------

def _root(root: Path | str | None = None) -> Path:
    if root:
        return Path(root).resolve()
    env = os.environ.get("AIAS_ROOT")
    return Path(env).resolve() if env else Path(__file__).resolve().parent.parent


def load_specs(root: Path | str | None = None) -> dict:
    with open(_root(root) / "brand" / "report_specs.json", encoding="utf-8") as f:
        return json.load(f)


def catalogue(specs: dict | None = None) -> list[dict]:
    """The register's entries (report_specs.json report_catalogue.entries)."""
    specs = load_specs() if specs is None else specs
    return list(specs.get("report_catalogue", {}).get("entries", []))


def registered_hashes(entry: dict) -> set[str]:
    """SHA-256 values that identify an entry's PDF: the deposited file and, where the website
    serves a copy that differs only in its metadata, that copy."""
    hashes = {entry.get("sha256")}
    hashes.add((entry.get("website") or {}).get("sha256"))
    return {h for h in hashes if h}


def next_revision(study: str, entries: Iterable[dict]) -> int:
    """The study's next revision number (revisions count per study, whatever the type)."""
    revs = [parse_code(e["code"])["rev"] for e in entries if parse_code(e["code"])["study"] == study]
    return max(revs, default=0) + 1


def check_code(code: str, entries: Sequence[dict], *, sha256: str | None = None) -> dict:
    """Refuse a code already in the catalogue for a different PDF (by SHA-256; with no hash, any
    registered code is refused: a published PDF is never re-rendered). A code not yet registered
    must be its study's next revision, and a registered PDF cannot take a second code."""
    p = parse_code(code)
    same = [e for e in entries if e.get("code") == code]
    if same:
        known = set().union(*(registered_hashes(e) for e in same))
        if sha256 is None or sha256 not in known:
            raise ReportCodeError(
                f"{code} is already in the catalogue for another PDF (SHA-256 "
                f"{', '.join(sorted(h[:12] for h in known)) or 'not recorded'}); a new render takes "
                f"r{next_revision(p['study'], entries)}")
        return p
    nxt = next_revision(p["study"], entries)
    if p["rev"] != nxt:
        raise ReportCodeError(f"{code}: the next revision of {p['study']} is r{nxt}")
    if sha256 is not None:
        clash = [e["code"] for e in entries if sha256 in registered_hashes(e)]
        if clash:
            raise ReportCodeError(f"this PDF is already registered as {clash[0]}")
    return p


REQUIRED_FIELDS = ("code", "title", "date", "tier", "git_tag", "osf_path", "sha256")


def validate_catalogue(entries: Sequence[dict]) -> list[str]:
    """Problems in the register (empty list when it is sound): every code well formed and used
    once, the fields the spec lists present, the type's tier kept, one code per PDF."""
    problems = []
    seen_codes, seen_hashes = {}, {}
    for i, e in enumerate(entries):
        where = e.get("code") or f"entry {i}"
        missing = [k for k in REQUIRED_FIELDS if k not in e]
        if missing:
            problems.append(f"{where}: missing {', '.join(missing)}")
        try:
            p = parse_code(e.get("code", ""))
        except ReportCodeError as err:
            problems.append(str(err))
            continue
        if e["code"] in seen_codes:
            problems.append(f"{e['code']}: used twice (entries {seen_codes[e['code']]} and {i})")
        seen_codes[e["code"]] = i
        if TYPE_TIER.get(p["type"]) not in (None, e.get("tier")):
            problems.append(f"{e['code']}: type {p['type']} is Tier {TYPE_TIER[p['type']]}, entry says {e.get('tier')}")
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(e.get("date") or "")):
            problems.append(f"{e['code']}: date must be YYYY-MM-DD")
        for h in [e.get("sha256"), (e.get("website") or {}).get("sha256")]:
            if h is None:
                continue
            if not _SHA.match(h):
                problems.append(f"{e['code']}: not a SHA-256: {h!r}")
            elif h in seen_hashes and seen_hashes[h] != e["code"]:
                problems.append(f"{e['code']}: same PDF as {seen_hashes[h]}")
            else:
                seen_hashes[h] = e["code"]
        if not e.get("sha256"):
            problems.append(f"{e['code']}: no SHA-256")
    return problems


# ---------------------------------------------------------------------------
# Where the code appears: PDF metadata, citation; the website in lower case
# ---------------------------------------------------------------------------

@functools.lru_cache(maxsize=4)
def _website_from_brand(root: str) -> str:
    with open(Path(root) / "brand" / "third_system_brand.json", encoding="utf-8") as f:
        return json.load(f)["company"]["contact"]["web"]


def website(root: Path | str | None = None) -> str:
    """The website as the brand file gives it (company.contact.web): 'thirdsystem.ai'."""
    return _website_from_brand(str(_root(root)))


def _web_re(site: str) -> re.Pattern:
    return re.compile(r"(?i)(?:[a-z0-9._%+-]+@)?" + re.escape(site) + r"(?:/[A-Za-z0-9._~%/#?=&+-]*)?")


def website_lower(text: str, site: str | None = None) -> str:
    """Every spelling of the website (and addresses on it) in lower case."""
    return _web_re(site or website()).sub(lambda m: m.group(0).lower(), text)


def upper_keep_website(text: str, site: str | None = None) -> str:
    """Upper-case a caps line but keep the website, and addresses on it, in lower case."""
    out, pos = [], 0
    for m in _web_re(site or website()).finditer(text):
        out += [text[pos:m.start()].upper(), m.group(0).lower()]
        pos = m.end()
    out.append(text[pos:].upper())
    return "".join(out)


def pdf_subject(code: str, subject: str | None = None) -> str:
    """PDF Subject: the code first, then the document's subject line."""
    parse_code(code)
    return f"{code} · {subject}" if subject else code


def pdf_keywords(code: str, *more: str) -> str:
    """PDF Keywords: the code first, then any others, comma separated, no repeats."""
    parse_code(code)
    return ", ".join(dict.fromkeys([code, *[m for m in more if m]]))


def cite(author_year: str, title_html: str, code: str, where: str) -> str:
    """Citation with the report code: 'Author (Year). <i>Title</i> (Report CODE). Third System. where'."""
    parse_code(code)
    return f"{author_year} <i>{title_html}</i> (Report {code}). Third System. {website_lower(where)}"


# ---------------------------------------------------------------------------
# Pre-flight
# ---------------------------------------------------------------------------

def sha256_file(path: Path | str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def _flat(text: str) -> str:
    return re.sub(r"\s+", " ", text or "")


def preflight(pdf_path: Path | str, code: str, title: str, entries: Sequence[dict],
              site: str | None = None) -> dict:
    """Pre-flight addition (decision 14): the last page shows the website in lower case and the
    right code; the code matches the file name and the PDF metadata (Subject and Keywords); the
    website is lower case on every page; and the register takes the code for this PDF (it is
    not already in use for another one). Returns {'ok', 'checks', 'problems', 'sha256'}."""
    from pypdf import PdfReader

    site = site or website()
    pdf_path = Path(pdf_path)
    reader = PdfReader(str(pdf_path))
    meta = reader.metadata or {}
    pages = [_flat(p.extract_text()) for p in reader.pages]
    spellings = sorted({m.group(0) for t in pages for m in re.finditer(re.escape(site), t, re.I)})
    digest = sha256_file(pdf_path)
    checks = {
        "file_name": pdf_path.name == file_name(code, title),
        "metadata_subject": code in str(meta.get("/Subject") or ""),
        "metadata_keywords": code in str(meta.get("/Keywords") or ""),
        "last_page_code": code in pages[-1],
        "last_page_website_lower_case": site in pages[-1],
        "website_lower_case_throughout": spellings in ([], [site]),
    }
    problems = [k for k, ok in checks.items() if not ok]
    if not checks["website_lower_case_throughout"]:
        problems.append(f"website printed as {spellings}")
    try:
        check_code(code, entries, sha256=digest)
        checks["register"] = True
    except ReportCodeError as err:
        checks["register"] = False
        problems.append(str(err))
    return {"ok": all(checks.values()), "checks": checks, "problems": problems, "sha256": digest}
