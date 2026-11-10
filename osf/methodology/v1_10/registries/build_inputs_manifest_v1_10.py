#!/usr/bin/env python3
"""Builds INPUTS_MANIFEST_v1_10.json: every frozen v1.10 input with path, role, set,
answer count (from archive_inventory_scan.csv, Nov 10, 2026), git blob SHA-1 and SHA-256.

The answer sets, their registries, coded mention files, certified detectors and MQ8
prompt files are taken from the scorer's own set table (scripts/score_v1_10.build_sets),
so the manifest and the scorer cannot drift apart. Archived inputs are pinned at the
base commit 894ccee (branch aias-2.0): their working-tree bytes must equal the blob on
that commit (else the build stops). Files created on branch v1.10 (the v0.23 registry
JSON, the v0.6 prompt copies, the registry-choice record) are pinned by their bytes
(git blob computed as git does) with on_base_commit = false.

Decision 10 (2026-11-10): the held studies v0.38 and v0.39 are excluded from v1.10
entirely and are not pinned. Run from anywhere:
    python3 osf/methodology/v1_10/registries/build_inputs_manifest_v1_10.py
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).with_name("INPUTS_MANIFEST_v1_10.json")
BASE = "894ccee9c65e3341c541191ac7ec1de48313a72a"   # aias-2.0 tip the drafts branched from
V110 = "osf/methodology/v1_10"
sys.path.insert(0, str(ROOT / "scripts"))
import score_v1_10 as S  # noqa: E402

COUNTS = {  # answers with text, archive_inventory_scan.csv (Nov 10, 2026); household: the swapped
    "EARLY-6 v1.0 household": 288,      # _final file (288 of 288, counted by score_v1_10.py --parity)
    "EARLY-6 v0.16 kitchen_knives": 334,
}


def answers_count(spec):
    if spec["set"] in COUNTS:
        return COUNTS[spec["set"]]
    return {"omni": 36, "early6": 288, "early2": 96, "coi_hold": 36, "paperB": 36}[spec["role"]]


F = []  # (set, role, path, answers_with_text, extra)
seen = {}


def add(st, role, path, n=None, **extra):
    if path in seen:                      # one entry per file; record every set that uses it
        seen[path].setdefault("also_used_by", []).append(st)
        return
    e = {"set": st, "role": role, "path": path, "answers_with_text": n, **extra}
    seen[path] = e
    F.append(e)


for spec in S.build_sets():
    add(spec["set"], "answers", spec["answers"], answers_count(spec),
        **({"analysed": False, "note": "frozen now, rank table only; analysed in Paper B"}
           if spec["role"] == "paperB" else
           {"analysed": False, "note": "COI screen pending (technology panel; v0.43 decision): "
                                       "MQ1 parse completion only, no rank extraction or output"}
           if spec["role"] == "coi_hold" else {}))
    add(spec["set"], "registry", spec["registry"])
    if spec.get("coded"):
        add(spec["set"], "certified_mentions", spec["coded"])
    if spec.get("detector"):
        add(spec["set"], "certified_detector", spec["detector"])
    if spec.get("prompts"):
        add(spec["set"], "prompts_MQ8", spec["prompts"])

add("OMNI detectors", "certified_detector_reference", "scripts/score_v0_31.py")
add("OMNI detectors", "certified_detector_reference", "scripts/score_v33.py")
add("OMNI P and C*", "presence_consistency", S.PROFILES_REL)
add("S6 sensitivity", "sensitivity_input", S.V41_VERDICTS_REL,
    note="v0.41 MC_Snapshot 'mismatched' list = models dropped in S6")
add("EARLY-6 v0.14 premium_tea", "registry_symlink_not_read", "registries/brands_premium_tea.json",
    note="committed symlink into the main working tree; the loader reads osf/v14/registries/brands_premium_tea.json")
add("EARLY-6 v0.16 kitchen_knives", "registry_reference_not_loaded", "registries/brands_kitchen_knives_v0.16.json",
    note="v0.16 panel registry (no aliases) used by scripts/score_v16.py for its brand list; see REGISTRY_CHOICES")
add("OMNI t1-t3 v0.23", "registry_source", "scripts/score_v0_23.py",
    note="REGISTRY (line 60) and BRAND_PATTERNS (line 88) extracted into v0_23_registry_v1_10.json")
add("OMNI t1-t3 v0.23", "registry_source", "scripts/acquire_v0_23.py", note="REGISTRY cross-check (line 61)")
add("v1.10 registry inputs", "registry_builder", V110 + "/registries/build_registry_inputs_v1_10.py")
add("v1.10 registry choices", "registry_choice_evidence", V110 + "/registries/REGISTRY_CHOICES_v1_10.md")
for p in ("run_aias_v2.py", "enrich.py", "extract_v09.py", "analyze_v08.py", "apply_v1.2_registry.py",
          "cleanup_aias_pre_v08.sh", "registries/README.md", "scripts/score_v16.py",
          "scripts/derive_brands_kitchen_knives_legacy.py"):
    add("v1.10 registry choices", "registry_choice_evidence", p)
add("DEV v0.18 (excluded)", "answers", "data/phase_b/v0.18/phase_b_results.json", 18)
add("DEV v0.17 (excluded)", "registry", "registries/brands_kitchenware_v0.17.json")
for q in ("q1_best_brands", "q2_serious_cooks", "q3_pro_chefs"):
    for k in range(1, 7):
        add("DEV v0.17 (excluded)", "answers", f"osf/v17/data/phaseB_queries/{q}/slot_{k}.json", 1)


def git(*a):
    r = subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""


head = git("rev-parse", "HEAD")
files, missing, problems = [], [], []
for e in F:
    fp = ROOT / e["path"]
    if not fp.exists() and not fp.is_symlink():
        missing.append({**e, "status": "missing in the working tree"})
        continue
    blob_wt = S.git_blob_sha1(fp)
    blob_base = git("rev-parse", f"{BASE}:{e['path']}")
    if blob_base and blob_base != blob_wt:
        problems.append(f"{e['path']}: working tree differs from {BASE[:7]}")
        continue
    e = {**e, "git_blob": blob_wt, "on_base_commit": bool(blob_base)}
    if fp.is_symlink():  # committed symlink: git pins only the link text, not the content
        e["symlink_to"] = str(fp.readlink())
        e["sha256"] = hashlib.sha256(str(fp.readlink()).encode()).hexdigest()
        e["bytes"] = len(str(fp.readlink()).encode())
        e["sha256_of"] = "link text"
    else:
        e["sha256"] = S.sha256(fp)
        e["bytes"] = fp.stat().st_size
    files.append(e)
if problems:
    sys.exit("STOP (frozen input changed since the base commit):\n" + "\n".join(problems))
OUT.write_text(json.dumps({
    "phase": "v1.10", "status": "r2 (locked at v1.10-prereg-r2)",
    "base_branch": "aias-2.0", "base_commit": BASE, "built_on_head": head, "branch": "v1.10",
    "answer_counts_source": "Try system book/archive_inventory_scan.csv (n_answers_with_text), Nov 10, 2026",
    "decisions_applied": ["held studies v0.38 and v0.39 excluded entirely (decision 10)",
                          "v0.23 inline registry pinned as v0_23_registry_v1_10.json with its source (decision 8)",
                          "registry per early set per REGISTRY_CHOICES_v1_10.md (decision 4)",
                          "COI flag file for S7 is not a frozen input (decision 12)"],
    "files": files, "missing": missing}, indent=2, ensure_ascii=False) + "\n")
print(len(files), "files;", len(missing), "missing;", sum(not f["on_base_commit"] for f in files),
      "created on branch v1.10")
for m in missing:
    print("MISSING", m["path"])
