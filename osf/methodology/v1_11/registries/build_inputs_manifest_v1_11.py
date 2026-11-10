#!/usr/bin/env python3
"""Builds INPUTS_MANIFEST_v1_11.json: every v1.11 input pinned by git blob (HEAD tree) and
sha256. Counts are copied from archive_inventory_scan.csv (Nov 10, 2026) and re-asserted by the
loader at lock. Reads file bytes and CSV headers only; computes no statistic on any answer.
Run from the repo root."""
import csv
import hashlib
import json
import os
import subprocess

INV = os.path.expanduser("~/aias/Try system book/archive_inventory_scan.csv")
W = {"t1": "osf/{v}", "t2": "osf/v34/data/{s}", "t3": "osf/v41/data/{s}"}
F_FILES = {"v19": "phase_b_responses.jsonl", "v20": "phase_b_results.csv", "v21": "phase_b_results.csv",
           "v22": "phase_b_results.csv", "v23": "v23_phase_b_raw.json"}
SUBSTRATE = {"v19": "audiophile headphones", "v20": "skincare", "v21": "cosmetics",
             "v22": "automotive", "v23": "premium spirits"}

INPUTS = []
for w, tpl in [("t1", "osf/v23/data/v23_phase_a_raw.json"), ("t2", "osf/v34/data/v23/v23_phase_a_raw.json"),
               ("t3", "osf/v41/data/v23/v23_phase_a_raw.json")]:
    INPUTS.append(("R", "v0.23 recognition", w, tpl))
for w in ("t1", "t2", "t3"):
    for v, fn in F_FILES.items():
        if w == "t1":
            path = f"osf/{v}/data/{fn}" if v == "v23" else f"osf/{v}/{fn}"
        else:
            path = f"{W[w].format(s=v)}/{fn}"
        INPUTS.append(("F", f"{v} frames ({SUBSTRATE[v]})", w, path))
for name, path in [("v0.9 pm", "data/pm/results_enriched_v09_20260507_181205.csv"),
                   ("v0.9 finance", "data/finance/results_enriched_v09_20260507_190816.csv"),
                   ("v0.9 oliveoil", "data/oliveoil/results_enriched_v09_20260507_184159.csv"),
                   ("v0.9 running", "data/running/results_enriched_v09_20260507_183238.csv"),
                   ("v0.9 skincare", "data/skincare/results_enriched_v09_20260507_185427.csv"),
                   ("v1.0 household", "data/household/results_v2_household_v1.0_merged.csv"),
                   ("v1.0 knives", "data/knives/results_v2_knives_v1.0_final.csv"),
                   ("v0.14 premium_tea", "data/premium_tea/results_v2_premium_tea_20260512_161817_filled.csv")]:
    INPUTS.append(("E", name, "single", path))
LOCKED = [("P_Cstar", "v1.9 unit table (P, C* per unit x wave; read only after judge outputs freeze)",
           "osf/methodology/v1_9/v1_9_unit_table.csv"),
          ("extraction", "omnibus certified mention extraction (load_wave)", "osf/v41/scripts/score_v41.py")]
REGISTRIES = ["osf_staging/v09/registries/brands_pm.json", "osf_staging/v09/registries/brands_finance.json",
              "osf_staging/v09/registries/brands_oliveoil.json", "osf_staging/v09/registries/brands_running.json",
              "osf_staging/v09/registries/brands_skincare.json", "registries/brands_household.json",
              "registries/brands_knives_v1.0.json", "registries/brands_premium_tea.json",
              "osf/v19/panel_registry_v0_19.csv", "prereg/v0_20_registry.json", "prereg/v0_21_registry.json",
              "prereg/v0_22_registry.json"]
DEV = [("D1", "osf/v17/data/phase_a/<brand>/slot_N.json (24 files)"),
       ("D2", "osf/v17/data/phaseB_queries/<q>/slot_N.json (18 files)"),
       ("D3", "data/phase_b/v0.18/phase_b_results.json"),
       ("D4", "archive/old_data/results_20260429_105403.csv")]


def tree():
    out = subprocess.run(["git", "ls-tree", "-r", "HEAD"], capture_output=True, text=True, check=True).stdout
    return {line.split("\t", 1)[1]: line.split()[2] for line in out.splitlines()}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    t = tree()
    inv = {r["file_path"]: r for r in csv.DictReader(open(INV, encoding="utf-8"))}
    head = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()

    def entry(path):
        e = {"path": path, "git_blob": t.get(path), "tracked": path in t,
             "sha256": sha256(path) if os.path.exists(path) else None,
             "bytes": os.path.getsize(path) if os.path.exists(path) else None}
        r = inv.get(path)
        if r:
            e.update({"inventory_sha_prefix": r["sha"], "blob_matches_inventory":
                      bool(e["git_blob"] and r["sha"] and e["git_blob"].startswith(r["sha"])),
                      "n_rows": int(r["n_rows"]), "n_answers_with_text": int(r["n_answers_with_text"]),
                      "models": r["models"], "date_range": r["date_range"], "text_col": r["text_col"]})
        if path.endswith(".csv") and os.path.exists(path):
            with open(path, encoding="utf-8", newline="") as f:
                hdr = next(csv.reader(f))
            e["has_brands_canonical"] = "brands_canonical" in hdr
        return e

    m = {"phase": "v1.11", "status": "DRAFT r0 (not locked)", "built_from_commit": head,
         "branch_base": "aias-2.0", "inventory": "Try system book/archive_inventory_scan.csv (Nov 10, 2026)",
         "inputs": [dict(block=b, set=s, wave=w, **entry(p)) for b, s, w, p in INPUTS],
         "locked_inputs": [dict(role=r, note=n, **entry(p)) for r, n, p in LOCKED],
         "registries": [entry(p) for p in REGISTRIES],
         "development_sample_excluded_from_confirmatory": [{"id": i, "path": p} for i, p in DEV],
         "unit_table": {"status": "TODO at lock step U0", "sha256": None, "counts": None},
         "human_sample": {"status": "TODO at lock step U0 (seed 111022)", "sha256": None}}
    tot = {}
    for e in m["inputs"]:
        tot.setdefault(e["block"], 0)
        tot[e["block"]] += e.get("n_answers_with_text", 0)
    m["answers_with_text_by_block"] = tot
    out = "osf/methodology/v1_11/registries/INPUTS_MANIFEST_v1_11.json"
    json.dump(m, open(out, "w"), indent=2, ensure_ascii=False)
    bad = [e["path"] for e in m["inputs"] + m["locked_inputs"] + m["registries"] if not e["tracked"]]
    mism = [e["path"] for e in m["inputs"] if e.get("blob_matches_inventory") is False]
    print("totals", tot, "untracked", bad, "blob mismatches", mism,
          "no brands_canonical", [e["path"] for e in m["inputs"] if e.get("has_brands_canonical") is False])


if __name__ == "__main__":
    main()
