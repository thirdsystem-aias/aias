#!/usr/bin/env python3
"""
code_v0_44.py -- AIAS(TM) v0.44 coder: v44_raw.jsonl -> coded tables (pre-registration draft r1, section 5.1).

Same approach as the v0.42 coder (osf/v42/scripts/code_t4_v0_42.py): one record per call (the last answered attempt,
else the last attempt), URLs removed from Phase B answers before brand matching, recognition by the certified
omnibus parser, real data guarded by the prereg tag, nothing ever sent to a model.

  Phase B mentions : the v0.44 alias matcher (new code; the omnibus matchers are registry-specific). A unit is
                     mentioned in an answer of ITS industry if any alias in the registry column `aliases`
                     (separated by '|') occurs as a whole word: case-insensitively for match_rule `ci`,
                     case-sensitively for `cs`. Whole word = not preceded and not followed by a letter or digit
                     (underscore, punctuation, Markdown marks and spaces are boundaries). Before matching, the answer
                     and the aliases are put in Unicode NFC and typographic apostrophes (U+2018, U+2019, U+02BC) are
                     read as ', non-breaking and typographic hyphens (U+2010, U+2011, U+2012) as '-', no-break spaces
                     (U+00A0, U+202F) as ' '. Sub-brands are not aliases.
  URL removal      : strip_urls, MD_LINK_RE and URL_RE copied byte for byte from code_t4_v0_42.py (checked by the tests).
  Recognition      : run_acquisition_v22.parse_yes_no (ROOT/scripts; certified, SHA-256 59f711b8... as locked in
                     score_v41.PROBE_SHA256), on the unstripped answer, as code_t4_v0_42.recog_label for v0.20-v0.22:
                     'yes' -> recognized 1; 'no' and 'ambiguous' -> 0 (ambiguous counted, not coded as yes).
  MC_Alias         : every match of a case-sensitive alias is exported with its sentence (v44_alias_audit.csv);
                     reported, never used to change a code.

Outputs in <out>/ (default osf/v44/data/coded): v44_phase_a.csv, v44_phase_b.csv, v44_alias_audit.csv.
  phase_a: call_id,substrate,brand,brand_id,model,condition,run,probe_id,label,recognized
  phase_b: call_id,substrate,brand,model,condition,run,probe_id,frame_id,mentioned       (brand = unit_id)
One row per ANSWERED call (status ok, non-empty text, no error) for Phase A, per answered call x unit of the
industry for Phase B. `substrate` holds the industry code (field name kept from v0.42 so that score_v0_42's
aggregation helpers apply unchanged).

Modes:
  (default)   code --raw (default osf/v44/data/v44_raw.jsonl, GUARDED: refused unless tag v0.44-prereg-r1 is on
              origin) into --out
"""
import argparse
import csv
import hashlib
import json
import os
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

ROOT = Path(os.environ.get("AIAS_ROOT", str(Path(__file__).resolve().parents[3]))).resolve()
V44 = ROOT / "osf/v44"
PREREG_TAG = "v0.44-prereg-r1"
REAL_RAW = V44 / "data/v44_raw.jsonl"
PROBES_PATH = V44 / "prereg/probes_v0_44.jsonl"
INDUSTRIES_PATH = V44 / "registries/industries_v0_44.csv"
DEFAULT_OUT = V44 / "data/coded"
PARSER_PATH = ROOT / "scripts/run_acquisition_v22.py"
PARSER_SHA256 = "59f711b82efb0846f8305e7d84423667571e819aa80ad071edb01c9b1c883cfe"   # score_v41.PROBE_SHA256


class Refused(RuntimeError):
    pass


# --------------------------------------------------------------------------- guard
def _ls_remote_tag():
    """Raw stdout of `git ls-remote --tags origin v0.44-prereg-r1` (separate function: tests patch it)."""
    r = subprocess.run(["git", "-C", str(ROOT), "ls-remote", "--tags", "origin", PREREG_TAG],
                       capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        raise Refused(f"git ls-remote failed ({r.stderr.strip()[:200]}); cannot verify tag {PREREG_TAG}")
    return r.stdout


def tag_on_origin():
    return f"refs/tags/{PREREG_TAG}" in _ls_remote_tag()


def guard_real_raw(path):
    """Refuse to open the real v0.44 raw file unless the prereg tag is on origin."""
    if Path(path).resolve() == REAL_RAW.resolve() and not tag_on_origin():
        raise Refused(f"refusing to read {REAL_RAW}: tag {PREREG_TAG} is not on origin")


# --------------------------------------------------------------------------- URL removal (byte copy from v0.42)
# Markdown links [text](target): the target is removed, the text kept. One level of balanced
# parentheses inside the target is allowed (e.g. wikipedia ..._(x)). Optional "title".
MD_LINK_RE = re.compile(
    r"\[([^\]]*)\]\(\s*(?:<[^>]*>|(?:[^()\s]|\([^()\s]*\))+)(?:\s+(?:\"[^\"]*\"|'[^']*'))?\s*\)")
URL_RE = re.compile(r"https?://[^\s<>\"'\])]+", re.I)


def strip_urls(text):
    """Remove http(s):// addresses and the targets of Markdown links (link text is kept)."""
    if not text:
        return text or ""
    t = MD_LINK_RE.sub(r"\1", text)
    return URL_RE.sub(" ", t)


# --------------------------------------------------------------------------- recognition (certified parser)
_PARSE = {}


def parse_yes_no(text):
    if not _PARSE:
        sys.path.insert(0, str(ROOT / "scripts"))
        import run_acquisition_v22 as R22   # stdlib-only module; its ~/aias constants are not used here
        _PARSE["f"] = R22.parse_yes_no
    return _PARSE["f"](text)


def parser_sha256():
    return hashlib.sha256(PARSER_PATH.read_bytes()).hexdigest()


# --------------------------------------------------------------------------- registries and the alias matcher
_TRANS = str.maketrans({"‘": "'", "’": "'", "ʼ": "'", "‐": "-", "‑": "-", "‒": "-",
                        " ": " ", " ": " "})
BOUND_L = r"(?<![^\W_])"     # not preceded by a letter or digit
BOUND_R = r"(?![^\W_])"      # not followed by a letter or digit


def normalize(text):
    return unicodedata.normalize("NFC", text or "").translate(_TRANS)


def load_industries(path=None):
    return list(csv.DictReader(open(path or INDUSTRIES_PATH, encoding="utf-8")))


def load_registry(industries=None, base=None):
    """{industry: [unit dict (unit_id, brand, tier, eligible_rank, aliases[list], match_rule)]} in file order."""
    base = Path(base or V44)
    reg = {}
    for ind in (industries if industries is not None else load_industries()):
        rows = list(csv.DictReader(open(base / ind["file"], encoding="utf-8")))
        reg[ind["industry"]] = [{"unit_id": r["unit_id"], "brand": r["brand"], "tier": r["tier"],
                                 "eligible_rank": int(r["eligible_rank"]) if r["eligible_rank"].strip() else None,
                                 "aliases": [a.strip() for a in r["aliases"].split("|") if a.strip()],
                                 "match_rule": r["match_rule"].strip()} for r in rows]
    return reg


def compile_unit(unit):
    if unit["match_rule"] not in ("ci", "cs"):
        raise ValueError(f"{unit['unit_id']}: match_rule must be ci or cs, got {unit['match_rule']!r}")
    flags = re.IGNORECASE if unit["match_rule"] == "ci" else 0
    return [(a, re.compile(BOUND_L + re.escape(normalize(a)) + BOUND_R, flags)) for a in unit["aliases"]]


class Matcher:
    def __init__(self, registry):
        self.registry = registry
        self.pats = {ind: [(u, compile_unit(u)) for u in units] for ind, units in registry.items()}

    def mentions(self, industry, text, audit=None, call_id=None):
        """{unit_id: 0/1} for the industry's units in `text` (already URL-stripped if required).
        audit: list to which every case-sensitive match is appended (MC_Alias)."""
        t = normalize(text)
        out = {}
        for u, pats in self.pats[industry]:
            hit = 0
            for alias, p in pats:
                for m in p.finditer(t):
                    hit = 1
                    if audit is not None and u["match_rule"] == "cs":
                        audit.append({"call_id": call_id, "substrate": industry, "unit_id": u["unit_id"],
                                      "brand": u["brand"], "alias": alias, "sentence": sentence_at(t, m.start())})
                    if audit is None or u["match_rule"] != "cs":
                        break
                if hit and (audit is None or u["match_rule"] != "cs"):
                    break
            out[u["unit_id"]] = hit
        return out


def sentence_at(text, pos, limit=300):
    """The line around pos, cut at sentence ends ('. ', '! ', '? ') on either side; at most `limit` characters."""
    ls = text.rfind("\n", 0, pos) + 1
    le = text.find("\n", pos)
    le = len(text) if le < 0 else le
    line = text[ls:le]
    p = pos - ls
    starts = [m.end() for m in re.finditer(r"[.!?]\s+", line[:p])]
    s = starts[-1] if starts else 0
    m = re.search(r"[.!?](\s|$)", line[p:])
    e = p + m.end() if m else len(line)
    return line[s:e].strip()[:limit]


def alias_overlaps(registry):
    """Pairs (industry, alias of unit X, unit Y) where an alias of X matches inside an alias of another unit Y of
    the same industry (a matcher ambiguity). Reported by the tests; expected empty."""
    out = []
    for ind, units in registry.items():
        for u in units:
            for _a, p in compile_unit(u):
                for v in units:
                    if v is u:
                        continue
                    for b in v["aliases"]:
                        if p.search(normalize(b)):
                            out.append((ind, _a, u["unit_id"], b, v["unit_id"]))
    return out


# --------------------------------------------------------------------------- call handling (as v0.42)
def read_raw(path):
    guard_real_raw(path)
    out = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return out


def is_answered(rec):
    return (rec.get("status") == "ok") and bool((rec.get("text") or "").strip()) and not rec.get("error")


def dedupe_calls(records):
    """One record per call_id: the LAST answered attempt if any, else the last attempt."""
    best = {}
    for r in records:
        cid = r["call_id"]
        if cid not in best or is_answered(r) or not is_answered(best[cid]):
            best[cid] = r
    return list(best.values())


def load_probe_map(path=None):
    pm = {}
    for line in open(path or PROBES_PATH, encoding="utf-8"):
        if line.strip():
            p = json.loads(line)
            pm[p["probe_id"]] = p
    return pm


def code_calls(calls, registry, probes=None, strip=True):
    """calls: deduplicated raw records. -> (phase_a_rows, phase_b_rows, alias_audit_rows)."""
    probes = probes or {}
    M = Matcher(registry)
    A, B, audit = [], [], []
    for r in calls:
        if not is_answered(r):
            continue
        ind = r["substrate"]
        base = {"call_id": r["call_id"], "substrate": ind, "model": r["model_requested"], "condition": r["condition"],
                "run": r["run"], "probe_id": r["probe_id"]}
        if r["phase"] == "B":
            frame = r.get("frame_id") or probes.get(r["probe_id"], {}).get("frame_id") or r["probe_id"]
            text = strip_urls(r["text"]) if strip else r["text"]
            for uid, v in M.mentions(ind, text, audit=audit, call_id=r["call_id"]).items():
                B.append({**base, "frame_id": frame, "brand": uid, "mentioned": v})
        else:
            uid = r.get("brand_id") or probes.get(r["probe_id"], {}).get("brand_id")
            lab = parse_yes_no(r["text"])
            A.append({**base, "brand": uid, "brand_id": uid, "label": lab, "recognized": 1 if lab == "yes" else 0})
    return A, B, audit


A_FIELDS = ["call_id", "substrate", "brand", "brand_id", "model", "condition", "run", "probe_id", "label", "recognized"]
B_FIELDS = ["call_id", "substrate", "brand", "model", "condition", "run", "probe_id", "frame_id", "mentioned"]
AUDIT_FIELDS = ["call_id", "substrate", "unit_id", "brand", "alias", "sentence"]


def write_tables(A, B, audit, out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    for rows, fields, name in ((A, A_FIELDS, "v44_phase_a.csv"), (B, B_FIELDS, "v44_phase_b.csv"),
                               (audit, AUDIT_FIELDS, "v44_alias_audit.csv")):
        with open(out / name, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            for r in rows:
                w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in fields})
    return out


def read_tables(coded_dir):
    A, B = [], []
    d = Path(coded_dir)
    for r in csv.DictReader(open(d / "v44_phase_a.csv", newline="", encoding="utf-8")):
        r["run"] = int(r["run"])
        r["recognized"] = None if r["recognized"] == "" else int(r["recognized"])
        A.append(r)
    for r in csv.DictReader(open(d / "v44_phase_b.csv", newline="", encoding="utf-8")):
        r["run"] = int(r["run"])
        r["mentioned"] = int(r["mentioned"])
        B.append(r)
    return A, B


# --------------------------------------------------------------------------- gate P2 (probe parity)
def probe_parity(raw_all, probes_path=None, locked_sha=None):
    """P2: SHA-256 of the probe file equals the locked value; every sent prompt equals its probe's text."""
    path = Path(probes_path or PROBES_PATH)
    sha = hashlib.sha256(path.read_bytes()).hexdigest()
    pm = load_probe_map(path)
    bad = [r["call_id"] for r in raw_all if pm.get(r.get("probe_id"), {}).get("prompt") != r.get("prompt")]
    return {"gate": "P2", "probe_sha256": sha, "locked_sha256": locked_sha,
            "sha_matches": locked_sha is not None and sha == locked_sha,
            "lines_checked": len(raw_all), "prompt_mismatches": len(bad), "examples": bad[:10],
            "passed": locked_sha is not None and sha == locked_sha and not bad}


# --------------------------------------------------------------------------- CLI
def main(argv=None):
    ap = argparse.ArgumentParser(description="AIAS v0.44 coder")
    ap.add_argument("--raw", default=str(REAL_RAW))
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    ap.add_argument("--no-url-strip", action="store_true", help="switch URL removal OFF (diagnostic only)")
    a = ap.parse_args(argv)
    try:
        calls = dedupe_calls(read_raw(a.raw))
    except Refused as e:
        print(f"[v44] REFUSED: {e}", file=sys.stderr)
        return 3
    A, B, audit = code_calls(calls, load_registry(), load_probe_map(), strip=not a.no_url_strip)
    write_tables(A, B, audit, a.out)
    print(f"coded {len(calls)} calls -> {len(A)} Phase A rows, {len(B)} Phase B rows, {len(audit)} case-sensitive "
          f"alias matches in {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
