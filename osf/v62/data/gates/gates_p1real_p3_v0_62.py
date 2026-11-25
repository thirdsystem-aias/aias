"""v0.62 lock-time gate halves on real data, using the locked gate code unchanged (no model call).
P1 real-data half: gate_p1_v0_62.compare(pinned v0.42 kernels, 112 units, t4 coded Phase B S0 rows).
P3: probe files' SHA-256 equal the lock manifest; every sent prompt equals its probe text."""
import csv, hashlib, json, sys
from pathlib import Path
W = Path.home() / "aias/_worktrees/v0.62-nohand"
V42 = Path.home() / "aias/_worktrees/v0.42"
sys.path.insert(0, str(W / "osf/v62/scripts"))
import gate_p1_v0_62 as G  # noqa
out = {}
ns, pin = G.pinned_namespace(str(V42))
U_alias = G.units()
U = sorted((r["substrate"], r["brand"]) for r in csv.DictReader(open(V42 / "osf/v42/v42_brand_table.csv", encoding="utf-8")))  # v0.23 units are S01..S24 in t4 tables
rows = []
for s in ("v19", "v20", "v21", "v22", "v23"):
    for r in csv.DictReader(open(V42 / f"osf/v42/data/coded/{s}_phase_b.csv", encoding="utf-8")):
        if r["condition"] == "S0":
            rows.append(r)
bad, parts = G.compare(ns, U, rows)
out["P1_real"] = {"source": "v0.42 worktree osf/v42/data/coded/*_phase_b.csv (S0 rows)", "rows": len(rows),
                  "units": len(U), "mismatches": len(bad), "first": [str(x) for x in bad[:5]],
                  "partitions": parts, "pinned": pin, "result": "PASS" if not bad else "FAIL"}
# also against the published brand table
S = G.S
mine = S.unit_values(U, rows)
bt = {(r["substrate"], r["brand"]): r for r in csv.DictReader(open(V42 / "osf/v42/v42_brand_table.csv", encoding="utf-8"))}
d = []
for u in U:
    a = float(bt[u]["pi_N3_S0"]); b = mine[u]["pi"]
    pa = bt[u]["phi_N3_S0"]; pb = mine[u]["phi"]
    if abs(a - b) > 1e-12 or ((pa in ("", "None")) != (pb is None)) or (pb is not None and abs(float(pa) - pb) > 1e-9):
        d.append((u, a, b, pa, pb))
out["P1_real"]["vs_v42_brand_table"] = {"units_compared": len(U), "differences": len(d), "first": [str(x) for x in d[:5]]}
# P3
man = {}
for line in open(W / "osf/v62/prereg/LOCK_MANIFEST_v0_62.sha256", encoding="utf-8"):
    h, p = line.split(None, 1); man[p.strip()] = h
p3 = {"files": {}, "prompt_mismatches": 0, "prompts_checked": 0}
probe = {}
for lg in ("es", "ko", "zh"):
    rel = f"osf/v62/translations/probes_{lg}_v0_62_r2.jsonl"
    h = hashlib.sha256((W / rel).read_bytes()).hexdigest()
    p3["files"][rel] = {"sha256": h, "manifest": man.get(rel), "equal": h == man.get(rel)}
    for l in open(W / rel, encoding="utf-8"):
        if l.strip():
            q = json.loads(l); probe[(lg, q["substrate"], q["probe_id"])] = q["prompt"]
miss = []
for l in open(W / "osf/v62/data/v62_raw.jsonl", encoding="utf-8"):
    r = json.loads(l)
    p3["prompts_checked"] += 1
    if probe.get((r["language"], r["substrate"], r["probe_id"])) != r["prompt"] or r.get("system") is not None:
        miss.append(r["call_id"])
p3["prompt_mismatches"] = len(miss); p3["first"] = miss[:5]
p3["result"] = "PASS" if not miss and all(v["equal"] for v in p3["files"].values()) else "FAIL"
out["P3"] = p3
print(json.dumps(out, indent=1, ensure_ascii=False))
