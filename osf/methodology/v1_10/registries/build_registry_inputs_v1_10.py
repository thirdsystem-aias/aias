#!/usr/bin/env python3
"""Builds the two derived registry inputs that v1.10 pins in its manifest.

1. v0_23_registry_v1_10.json - v0.23's inline registry (S01-S24), extracted
   programmatically (ast, no import, no API client) from scripts/score_v0_23.py, the
   script that coded v0.23's Phase B mentions at t1 and (re-pointed by
   scripts/v34_code_t2.py / osf/v41/scripts/v41_code_t3.py) at t2 and t3. The ids and
   names are cross-checked against scripts/acquire_v0_23.py. Each brand keeps its
   source regexes verbatim (BRAND_PATTERNS) and gets a finite alias list obtained by
   expanding those regexes mechanically (\\s+ -> one space, [\\s-]* -> '', ' ', '-',
   x? -> with/without x, [oó] -> both letters, (the\\s+)? -> with/without 'the ').
   Every alias is checked to be matched in full by its source regex. The canonical
   name is always an alias (E2).
2. v06_prompts/prompts_<cat>_v0_6.json - the v0.6 prompt files as restored at commit
   179b3d7 (the per-category reorg; registries/README.md and cleanup_aias_pre_v08.sh
   document them as the v0.6 originals, skincare reconstructed), copied byte for byte
   out of git so that MQ8 (prompt parity v0.6 / v0.9) reads pinned files. The git blob
   of each copy equals the historical blob (checked).

Run from anywhere: python3 osf/methodology/v1_10/registries/build_registry_inputs_v1_10.py
"""
import ast
import hashlib
import json
import re
import subprocess
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
SRC_SCORE = "scripts/score_v0_23.py"
SRC_ACQ = "scripts/acquire_v0_23.py"
OUT_V23 = HERE / "v0_23_registry_v1_10.json"
V06_COMMIT = "179b3d7"
V06_CATS = ["pm", "finance", "oliveoil", "running", "skincare"]
OUT_V06 = HERE / "v06_prompts"


def git(*a):
    return subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True, check=True).stdout


def blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def literal_assign(path, name):
    tree = ast.parse((ROOT / path).read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == name for t in node.targets):
            return ast.literal_eval(node.value), node.lineno
    raise KeyError(f"{name} not found in {path}")


# --- regex subset expander ------------------------------------------------------------
def _parse(p, i=0, stop=None):
    """Parse a restricted regex into a list of (alternatives:set[str], quant) atoms."""
    atoms = []
    while i < len(p) and p[i] != stop:
        c = p[i]
        if c == "\\":
            nxt = p[i + 1]
            i += 2
            if nxt == "b":
                if 0 < i - 2 and i < len(p):
                    raise ValueError(f"inner \\b unsupported: {p}")
                continue
            alts = {" "} if nxt == "s" else {nxt}
        elif c == "[":
            j = p.index("]", i)
            body, alts, k = p[i + 1:j], set(), 0
            while k < len(body):
                if body[k] == "\\":
                    alts.add(" " if body[k + 1] == "s" else body[k + 1])
                    k += 2
                else:
                    alts.add(body[k])
                    k += 1
            i = j + 1
        elif c == "(":
            sub, i = _parse(p, i + 1, ")")
            alts = _expand(sub)
            i += 1
        elif c in "?+*|^$.{":
            raise ValueError(f"unsupported token {c!r} in {p}")
        else:
            alts = {c}
            i += 1
        q = p[i] if i < len(p) and p[i] in "?+*" else ""
        i += len(q)
        atoms.append((alts, q))
    return atoms, i


def _expand(atoms):
    choices = []
    for alts, q in atoms:
        opts = set(alts)
        if q in ("?", "*"):
            opts.add("")
        choices.append(sorted(opts))
    return {"".join(t) for t in product(*choices)}


def expand_pattern(pattern):
    atoms, _ = _parse(pattern)
    out = _expand(atoms)
    core = re.sub(r"^\\b|\\b$", "", pattern)
    for s in out:
        assert re.fullmatch(core, s), (pattern, s)
    return sorted(out)


def build_v23():
    reg, l_reg = literal_assign(SRC_SCORE, "REGISTRY")
    pats, l_pat = literal_assign(SRC_SCORE, "BRAND_PATTERNS")
    acq, l_acq = literal_assign(SRC_ACQ, "REGISTRY")
    assert [(b["id"], b["brand"]) for b in reg] == [(b["id"], b["brand"]) for b in acq], "score/acquire mismatch"
    assert sorted(pats) == [b["id"] for b in reg], "pattern ids != registry ids"
    brands = []
    for b in reg:
        aliases = set()
        for p in pats[b["id"]]:
            aliases |= set(expand_pattern(p))
        core_ok = any(re.search(p, b["brand"].lower()) for p in pats[b["id"]])
        brands.append({"id": b["id"], "brand": b["brand"], "conglomerate": b["conglomerate"],
                       "source_patterns": pats[b["id"]],
                       "canonical_matched_by_source_regex": bool(core_ok),
                       "aliases": [b["brand"]] + sorted(aliases - {b["brand"]})})
    src = (ROOT / SRC_SCORE).read_bytes()
    out = {
        "phase": "v1.10", "kind": "v0.23 inline registry, extracted programmatically",
        "source": {"path": SRC_SCORE, "registry_line": l_reg, "brand_patterns_line": l_pat,
                   "git_blob": blob_sha1(src), "sha256": hashlib.sha256(src).hexdigest(),
                   "cross_check": {"path": SRC_ACQ, "registry_line": l_acq,
                                   "ids_and_names_identical": True}},
        "coder_note": ("score_v0_23.find_brand_mentions matched these regexes on response_text.lower() "
                       "(no accent stripping); v1.10 matches the expanded aliases with \\b...\\b on "
                       "v1.4-normalised text (E1/E2). MQ2 measures the agreement (floor 0.98 per wave)."),
        "expansion_rules": ["\\s+ -> one space", "[\\s-]* -> '', ' ', '-'", "x? -> with and without x",
                            "[oó] / [eé] -> both letters", "(the\\s+)? -> with and without 'the '",
                            "every alias is matched in full by its source regex (checked)"],
        "unit_key": "id (the brand key of osf/aias_2_0/aias_2_0_profiles.csv for v0.23)",
        "brands": brands}
    OUT_V23.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT_V23.relative_to(ROOT)}: {len(brands)} brands, "
          f"{sum(len(b['aliases']) for b in brands)} aliases")


def build_v06_prompts():
    OUT_V06.mkdir(exist_ok=True)
    for c in V06_CATS:
        path = f"prompts/prompts_{c}.json"
        blob = git("rev-parse", f"{V06_COMMIT}:{path}").decode().strip()
        data = git("cat-file", "blob", blob)
        assert blob_sha1(data) == blob
        dst = OUT_V06 / f"prompts_{c}_v0_6.json"
        dst.write_bytes(data)
        print(f"wrote {dst.relative_to(ROOT)} <- git {V06_COMMIT}:{path} (blob {blob[:10]})")


if __name__ == "__main__":
    build_v23()
    build_v06_prompts()
