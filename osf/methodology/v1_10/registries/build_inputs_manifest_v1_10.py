#!/usr/bin/env python3
"""Builds INPUTS_MANIFEST_v1_10.json: every frozen v1.10 input with path, role, set,
answer count (from archive_inventory_scan.csv, Nov 10, 2026), git blob (SHA-1 of the
blob as committed on the base commit) and SHA-256 of the bytes. Run from repo root."""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).with_name("INPUTS_MANIFEST_v1_10.json")
CATS9 = {"pm": "181205", "finance": "190816", "oliveoil": "184159", "running": "183238", "skincare": "185427"}
V06 = {"pm": "data/pm/results_v2_20260429_181007.csv", "finance": "data/finance/results_v2_20260430_181613.csv",
       "oliveoil": "data/oliveoil/_pre_revision/results_v2_20260430_085246.csv",
       "running": "data/running/results_v2_20260429_205023.csv", "skincare": "data/skincare/results_v2_20260430_175139.csv"}
F = []  # (set, role, path, answers_with_text)
for c, ts in CATS9.items():
    F.append(("EARLY-6 v0.9 " + c, "answers", f"data/{c}/results_enriched_v09_20260507_{ts}.csv", 288))
    F.append(("EARLY-6 v0.9 " + c, "registry", f"osf_staging/v09/registries/brands_{c}.json", None))
F += [("EARLY-6 v1.0 household", "answers", "data/household/results_v2_household_v1.0_merged.csv", 250),
      ("EARLY-6 v1.0 household", "registry", "registries/brands_household.json", None),
      ("EARLY-6 v1.0 knives", "answers", "data/knives/results_v2_knives_v1.0_final.csv", 288),
      ("EARLY-6 v1.0 knives", "registry", "registries/brands_knives_v1.0.json", None),
      ("EARLY-6 v0.14 premium_tea", "answers", "data/premium_tea/results_v2_premium_tea_20260512_161817_filled.csv", 288),
      ("EARLY-6 v0.14 premium_tea", "registry", "registries/brands_premium_tea.json", None),
      ("EARLY-6 v0.16 kitchen_knives", "answers", "data/kitchen_knives/results_v2_kitchen_knives_20260516_212400.csv", 334),
      ("EARLY-6 v0.16 kitchen_knives", "registry", "registries/brands_kitchen_knives_v0.16.json", None)]
for c, p in V06.items():
    F.append(("EARLY-2 v0.6 " + c, "answers", p, 96))
    F.append(("EARLY-2 v0.6 " + c, "registry", f"registries/brands_{c}.json", None))
for w, base in (("t1", "osf"), ("t2", "osf/v34/data"), ("t3", "osf/v41/data")):
    F.append((f"OMNI {w} v0.19", "answers", f"{base}/v19/phase_b_responses.jsonl", 36))
    F.append((f"OMNI {w} v0.19", "certified_mentions", f"{base}/v19/phase_b_results.csv", None))
    for s in ("v20", "v21", "v22"):
        F.append((f"OMNI {w} v0.{s[1:]}", "answers", f"{base}/{s}/phase_b_results.csv", 36))
    v23 = "osf/v23/data" if w == "t1" else f"{base}/v23"
    F.append((f"OMNI {w} v0.23", "answers", f"{v23}/v23_phase_b_raw.json", 36))
    F.append((f"OMNI {w} v0.23", "certified_mentions", f"{v23}/v23_phase_b_scored.json", None))
F += [("OMNI registries", "registry", "osf/v19/panel_registry_v0_19.csv", None),
      ("OMNI registries", "registry", "prereg/v0_20_registry.json", None),
      ("OMNI registries", "registry", "prereg/v0_21_registry.json", None),
      ("OMNI registries", "registry", "prereg/v0_22_automotive_content.py", None),
      ("OMNI detectors", "certified_detector", "scripts/score_v20.py", None),
      ("OMNI detectors", "certified_detector", "scripts/score_v21.py", None),
      ("OMNI detectors", "certified_detector", "scripts/score_v22.py", None),
      ("OMNI detectors", "certified_detector", "scripts/score_v0_31.py", None),
      ("OMNI detectors", "certified_detector", "scripts/score_v33.py", None),
      ("OMNI P and C*", "presence_consistency", "osf/aias_2_0/aias_2_0_profiles.csv", None),
      ("HELD v0.38", "answers", "osf/v38/data/v38_raw.json", 132),
      ("HELD v0.38", "registry", "osf/v38/registries/brands_home_roasters_v0.38.json", None),
      ("HELD v0.39", "answers", "osf/v39/data/v39_raw.json", 360),
      ("HELD v0.39", "registry", "osf/v39/registries/brands_commercial_roasters_v0.39.json", None),
      ("BASELINE v0.28", "answers", "osf/v28/data/phase_b_results.csv", 36),
      ("BASELINE v0.28", "registry", "prereg/v0_28_panel_brands.txt", None),
      ("PAPER-B v0.32 arm A", "answers", "osf/v32/data/phase_b_A.csv", 36),
      ("PAPER-B v0.32 arm B", "answers", "osf/v32/data/phase_b_B.csv", 36),
      ("PAPER-B v0.32", "registry", "registries/v0_32_registry.json", None),
      ("DEV v0.18 (excluded)", "answers", "data/phase_b/v0.18/phase_b_results.json", 18),
      ("DEV v0.17 (excluded)", "registry", "registries/brands_kitchenware_v0.17.json", None)]
for q in ("q1_best_brands", "q2_serious_cooks", "q3_pro_chefs"):
    for k in range(1, 7):
        F.append(("DEV v0.17 (excluded)", "answers", f"osf/v17/data/phaseB_queries/{q}/slot_{k}.json", 1))


def git(*a):
    return subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True, text=True).stdout.strip()


base = git("rev-parse", "HEAD")
files, missing = [], []
for st, role, p, n in F:
    fp = ROOT / p
    blob = git("rev-parse", f"{base}:{p}")
    if not fp.exists() or not blob or blob.startswith(base):
        missing.append({"set": st, "role": role, "path": p, "status": "missing on base commit"})
        continue
    e = {"set": st, "role": role, "path": p, "answers_with_text": n,
         "git_blob": blob, "sha256": hashlib.sha256(fp.read_bytes()).hexdigest(),
         "bytes": fp.stat().st_size}
    if fp.is_symlink():  # committed symlink: git pins only the link text, not the content
        tgt = str(fp.readlink())
        e["symlink_to"] = tgt
        rel = tgt.split("/aias/", 1)[1] if "/aias/" in tgt else None
        cblob = git("rev-parse", f"{base}:{rel}") if rel else ""
        e["content_path_on_base"] = rel if cblob and not cblob.startswith(base) else None
        e["content_git_blob"] = cblob if e["content_path_on_base"] else None
        e["warning"] = ("content not pinned by git on this branch: link points outside the "
                        "worktree; copy the content into the v1.10 tree before the lock")
    files.append(e)
OUT.write_text(json.dumps({
    "phase": "v1.10", "status": "DRAFT r1 (not locked)",
    "base_branch": "aias-2.0", "base_commit": base, "branch": "v1.10",
    "answer_counts_source": "Try system book/archive_inventory_scan.csv (n_answers_with_text), Nov 10, 2026",
    "files": files, "missing": missing}, indent=2) + "\n")
print(len(files), "files;", len(missing), "missing")
for m in missing:
    print("MISSING", m["path"])
