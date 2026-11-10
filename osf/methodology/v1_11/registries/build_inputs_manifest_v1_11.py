#!/usr/bin/env python3
"""Builds INPUTS_MANIFEST_v1_11.json: every frozen v1.11 input with path, role, set, git blob
SHA-1 and SHA-256 (v1.10's manifest format, so score_v1_10.verify_manifest and Ctx apply).

The answer sets, registries, certified mention records, detectors and question sources are taken
from the scorer's own set table (scripts/score_v1_11.build_sets), so manifest and scorer cannot
drift apart. Archived inputs are pinned at the base commit 894ccee (branch aias-2.0): their
working-tree bytes must equal the blob on that commit, else the build stops. The two files copied
from v1.10 (its scorer and its v0.23 registry) must equal their blobs at tag v1.10-prereg-r2.

Objects outside this tree (v1.10's Stage S selection and rank-table index on branch v1.10; the
v1.10 registry-choice record at its tag; the v0.42 records that are the source of the judge model
IDs and prices) are pinned under "git_objects" by git blob and SHA-256 (read from the shared
object store). Held studies and v0.28 are not pinned (decision 3). No answer text is read beyond
the bytes needed for the hashes. Run from anywhere:
    python3 osf/methodology/v1_11/registries/build_inputs_manifest_v1_11.py
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).with_name("INPUTS_MANIFEST_v1_11.json")
BASE = "894ccee9c65e3341c541191ac7ec1de48313a72a"   # aias-2.0 tip the v1.11 draft branched from
sys.path.insert(0, str(ROOT / "scripts"))
import score_v1_11 as S  # noqa: E402

V = S.V
F, seen = [], {}


def add(st, role, path, n=None, **extra):
    if path in seen:
        seen[path].setdefault("also_used_by", []).append(st)
        return
    e = {"set": st, "role": role, "path": path, "answers_with_text": n, **extra}
    seen[path] = e
    F.append(e)


N_TEXT = {"R": 144, "F": 36, "E": 288}   # verified by --parity (parse_completion.with_text)
for spec in S.build_sets():
    add(spec["set"], "answers", spec["answers"], N_TEXT[spec["block"]], block=spec["block"])
    add(spec["set"], "registry", spec["registry"])
    if spec.get("coded"):
        add(spec["set"], "certified_mentions", spec["coded"])
    if spec.get("detector"):
        add(spec["set"], "certified_detector", spec["detector"])
    if spec.get("prompts"):
        add(spec["set"], "questions", spec["prompts"])
    if spec.get("questions"):
        add(spec["set"], "questions", spec["questions"])
add("v1.10 locked code", "v1_10_locked_code", "scripts/score_v1_10.py",
    note="byte-identical copy of v1.10-prereg-r2:scripts/score_v1_10.py (loaders, E2 extractor, rank statistic, rho_w)")
add("OMNI P and C*", "presence_consistency", S.PROFILES_REL, note="opened only at Stage C (after H1)")
add("OMNI P and C* cross-check", "presence_consistency_crosscheck", S.V19_TABLE_REL,
    note="v1.9 unit table: P and C* compared with the profiles table at Stage C; never a verdict input")
add("OMNI certified extraction reference", "certified_reference", "osf/v41/scripts/score_v41.py",
    note="load_wave: the extraction behind v1.9's mentions; v1.11 reads its sources directly")
for p in ("scripts/score_v0_31.py", "scripts/score_v33.py"):
    add("OMNI certified extraction reference", "certified_reference", p)
add("EARLY-6 v0.14 premium_tea", "registry_symlink_not_read", "registries/brands_premium_tea.json",
    note="committed symlink into the main working tree; the loader reads osf/v14/registries/brands_premium_tea.json")
add("prior valence material (declared, section 1)", "legacy_extractor_reference", "extractor.py",
    note="gpt-5.4-mini function calling; per-brand sentiment enum positive/neutral/negative (v0.9 files)")
add("prior valence material (declared, section 1)", "legacy_extractor_reference", "extract_v09.py")
add("prior valence material (declared, section 1)", "legacy_extractor_reference", "enrich.py")
DEV = (["registries/brands_kitchenware_v0.17.json", "data/phase_b/v0.18/phase_b_results.json",
        "archive/old_data/results_20260429_105403.csv"]
       + sorted(str(p.relative_to(ROOT)) for p in (ROOT / "osf/v17/data/phaseB_queries").glob("*/slot_*.json"))
       + sorted(str(p.relative_to(ROOT)) for p in (ROOT / "osf/v17/data/phase_a").glob("*/slot_*.json")))
for p in DEV:
    add("DEVELOPMENT SAMPLE (excluded from every confirmatory analysis)", "development_sample", p)


def git(*a):
    r = subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""


def git_bytes(blob):
    return subprocess.run(["git", "-C", str(ROOT), "cat-file", "blob", blob], capture_output=True, check=True).stdout


V110_COPIES = {"scripts/score_v1_10.py": "v1.10-prereg-r2:scripts/score_v1_10.py",
               "osf/methodology/v1_10/registries/v0_23_registry_v1_10.json":
                   "v1.10-prereg-r2:osf/methodology/v1_10/registries/v0_23_registry_v1_10.json"}
head = git("rev-parse", "HEAD")
files, missing, problems = [], [], []
for e in F:
    fp = ROOT / e["path"]
    if not fp.exists() and not fp.is_symlink():
        missing.append({**e, "status": "missing in the working tree"})
        continue
    blob_wt = V.git_blob_sha1(fp)
    blob_base = git("rev-parse", f"{BASE}:{e['path']}")
    if e["path"] in V110_COPIES:
        want = git("rev-parse", V110_COPIES[e["path"]])
        if want != blob_wt:
            problems.append(f"{e['path']}: differs from {V110_COPIES[e['path']]}")
            continue
        e = {**e, "source": V110_COPIES[e["path"]]}
    elif blob_base and blob_base != blob_wt:
        problems.append(f"{e['path']}: working tree differs from {BASE[:7]}")
        continue
    e = {**e, "git_blob": blob_wt, "on_base_commit": bool(blob_base)}
    if fp.is_symlink():
        e["symlink_to"] = str(fp.readlink())
        e["sha256"] = hashlib.sha256(str(fp.readlink()).encode()).hexdigest()
        e["bytes"] = len(str(fp.readlink()).encode())
        e["sha256_of"] = "link text"
    else:
        e["sha256"] = V.sha256(fp)
        e["bytes"] = fp.stat().st_size
    files.append(e)
if problems:
    sys.exit("STOP (frozen input changed):\n" + "\n".join(problems))

GIT_OBJECTS = [  # (path, ref, role, note)
    (S.V110_SELECTION_REL, f"{S.V110_STAGE_S_COMMIT}", "v1_10_stage_s_selection",
     "Stage S of 2026-11-10 (branch v1.10): selected MNP; H5's statistic (decision 6)"),
    (S.V110_RANK_INDEX_REL, f"{S.V110_STAGE_S_COMMIT}", "v1_10_stage_s_rank_index",
     "SHA-256 of v1.10's per-answer rank tables; v1.11's regenerated tables must match"),
    ("osf/methodology/v1_10/registries/REGISTRY_CHOICES_v1_10.md", S.V110_TAG, "registry_choice_evidence",
     "registry per early set and the two answer-file swaps (decision 3); not read by the scorer"),
    ("osf/methodology/v1_10/prereg/PRE_REGISTRATION_v1_10.md", S.V110_TAG, "sister_preregistration", "not read"),
    ("osf/v42/prereg/PRE_REGISTRATION_v0_42.md", "v0.42", "judge_ids_and_prices_source",
     "section 4.3 (model IDs verified 2026-11-10) and 4.5 (list prices); not read by the scorer"),
    ("osf/v42/prereg/cost_inputs_v0_42.txt", "v0.42", "judge_cost_planning_source",
     "per-call token means (GPT-6 Astra reasoning p90 270 at default effort = PLAN_REASONING)"),
    ("osf/v42/prereg/feasibility_v0_42.json", "v0.42", "judge_availability_source", "served IDs on 2026-11-10"),
]
gobj = []
for path, ref, role, note in GIT_OBJECTS:
    commit = git("rev-parse", f"{ref}^{{commit}}")
    blob = git("rev-parse", f"{ref}:{path}")
    if not blob:
        missing.append({"path": path, "ref": ref, "status": "git object missing"})
        continue
    data = git_bytes(blob)
    gobj.append({"path": path, "ref": ref, "commit": commit, "role": role, "note": note, "git_blob": blob,
                 "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})

OUT.write_text(json.dumps({
    "phase": "v1.11", "status": "r1 pre-lock (2026-11-10); rebuilt at the content lock",
    "base_branch": "aias-2.0", "base_commit": BASE, "built_on_head": head, "branch": "v1.11",
    "answer_counts": "answers with text, verified by score_v1_11.py --parity (prereg/parity_v1_11.json)",
    "decisions_applied": [
        "held studies excluded entirely and not named; v0.28 not loaded (decision 3)",
        "v1.0 household: the scored _final file (288/288), not the merged file (decision 3, as v1.10)",
        "registry per early set per REGISTRY_CHOICES_v1_10.md; premium tea via the tracked copy (decision 3)",
        "E mentions: v1.10's E2 extractor; F mentions: the certified record (section 15)",
        "P and C*: aias_2_0_profiles.csv as v1.10; the v1.9 unit table is a cross-check only (section 15)",
        "v1.10 objects pinned by blob; v1.10 Stage C outputs not pinned or read (decision 6)"],
    "files": files, "git_objects": gobj, "missing": missing}, indent=2, ensure_ascii=False) + "\n")
print(len(files), "files;", len(gobj), "git objects;", len(missing), "missing;",
      sum(not f["on_base_commit"] for f in files), "not on the base commit")
for m in missing:
    print("MISSING", m.get("path"), m.get("status"))
