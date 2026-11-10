#!/usr/bin/env python3
"""
export_probes_v0_42.py — exact probe export for the v0.42 t4 wave (no API calls).

Prompt strings are NOT retyped. Each verbatim legacy runner is imported from this
checkout and its OWN phase function is executed with the provider call boundary
replaced by an offline stub, so the runner itself builds every prompt string:
  v19    osf/v19/run_v0_19.py             run_phase(queries.jsonl) with route_call stubbed
  v20/21 scripts/run_acquisition_v2{0,1}.py  run_phase_a/b with call_llm stubbed
  v22    scripts/run_acquisition_v22.py   load_prereg_module + run_phase_a/b, call_llm stubbed
  v23    scripts/acquire_v0_23.py         run_phase_a/b with PROVIDER_DISPATCH stubbed
Nothing is sent to any model. Stub outputs go to a temp directory.

Writes:
  osf/v42/prereg/probes_v0_42.jsonl
  osf/v42/prereg/probe_parity_v0_42.json
"""
import csv
import hashlib
import importlib.util
import json
import re
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT_PROBES = ROOT / "osf/v42/prereg/probes_v0_42.jsonl"
OUT_PARITY = ROOT / "osf/v42/prereg/probe_parity_v0_42.json"
MANIFEST = ROOT / "osf/v41/prereg/acquisition_manifest_v41.md"
T3 = ROOT / "osf/v41/data"
TMP = Path(tempfile.mkdtemp(prefix="v42_export_"))

sys.path.insert(0, str(ROOT))  # protocol.providers


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, str(path))
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


def rel(p):
    return str(Path(p).relative_to(ROOT))


probes = []
observed_max_tokens = {}


def add(substrate, phase, probe_id, id_kind, unit_id, prompt, runner, artifact, system=None, **extra):
    d = {
        "substrate": substrate, "phase": phase, "probe_id": probe_id,
        "probe_id_source": id_kind,
        ("brand_id" if phase == "A" else "frame_id"): unit_id,
        "system": system, "prompt": prompt,
        "source_runner": runner, "source_artifact": artifact,
    }
    d.update(extra)
    probes.append(d)


def export_v19():
    m = load(ROOT / "osf/v19/run_v0_19.py", "exp_v19")
    seen = []

    def stub_route(model, prompt):
        seen.append((model, prompt))
        return {"raw_response": "stub", "tokens_in": 0, "tokens_out": 0, "latency_ms": 0}
    m.route_call = stub_route
    runner = "osf/v19/run_v0_19.py"
    for phase, qpath in (("A", m.PHASE_A_QUERIES), ("B", m.PHASE_B_QUERIES)):
        seen.clear()
        m.run_phase(qpath, TMP / f"v19_{phase}.jsonl", phase)
        queries = [json.loads(l) for l in open(qpath) if l.strip()]
        assert len(queries) == len(seen), (phase, len(queries), len(seen))
        by_unit = {}
        for q, (model, prompt) in zip(queries, seen):
            assert model == q["panel_model"]
            unit = q["brand"] if phase == "A" else q["frame"]
            pid = "__".join(q["query_id"].split("__")[:2])  # legacy id minus panel model
            if unit in by_unit:
                assert by_unit[unit][1] == prompt, f"v19 prompt differs across models for {unit}"
                continue
            by_unit[unit] = (pid, prompt, q)
        for unit, (pid, prompt, q) in by_unit.items():
            extra = {}
            if phase == "B":
                extra = {"channel": q.get("frame_channel"), "frame_load_bearing": q.get("frame_load_bearing")}
            add("v19", phase, pid, "legacy", unit, prompt, runner,
                "osf/v19/phase_%s_queries.jsonl" % phase.lower(), **extra)


def export_v2x(sub, modpath, registry_loader, artifact):
    m = load(modpath, f"exp_{sub}")
    cur = {"p": "A"}
    mt = defaultdict(set)

    def stub_llm(model_name, prompt, max_tokens=1024, max_retries=4):
        mt[cur["p"]].add(max_tokens)
        return "Yes", 0.0
    m.call_llm = stub_llm
    reg = registry_loader(m)
    runner = rel(modpath)
    cur["p"] = "A"
    m.run_phase_a(reg, TMP / f"{sub}_a.csv", 1, False)
    cur["p"] = "B"
    m.run_phase_b(reg, TMP / f"{sub}_b.csv", 1, False)
    observed_max_tokens[sub] = {k: sorted(v) for k, v in mt.items()}
    rowsA = list(csv.DictReader(open(TMP / f"{sub}_a.csv", encoding="utf-8")))
    rowsB = list(csv.DictReader(open(TMP / f"{sub}_b.csv", encoding="utf-8")))
    seen = {}
    for r in rowsA:
        key = (r["cell"], int(r["cascade_order"]), r["brand"])
        if key in seen:
            assert seen[key] == r["probe_text"]
            continue
        seen[key] = r["probe_text"]
    for (cell, order, brand), prompt in seen.items():
        bid = f"{cell}.{order}"
        add(sub, "A", f"{sub}_A_{bid}", "derived", bid, prompt, runner, artifact,
            brand=brand, cell=cell, cascade_order=order)
    seenB = {}
    for r in rowsB:
        if r["frame_id"] in seenB:
            assert seenB[r["frame_id"]][0] == r["frame_text"]
            continue
        seenB[r["frame_id"]] = (r["frame_text"], r["channel"])
    for fid, (prompt, ch) in sorted(seenB.items(), key=lambda kv: (kv[1][1], kv[0])):
        add(sub, "B", fid, "legacy", fid, prompt, runner, artifact, channel=ch)


def export_v23():
    m = load(ROOT / "scripts/acquire_v0_23.py", "exp_v23")
    m.OUTPUT_DIR = TMP

    def stub(model_id, prompt):
        return "stub"
    m.PROVIDER_DISPATCH = {p: (stub, 0) for p in ("anthropic", "openai", "google")}
    runner = "scripts/acquire_v0_23.py"
    recA = m.run_phase_a(False)
    recB = m.run_phase_b(False)
    seen = {}
    for r in recA:
        if r["brand_id"] in seen:
            assert seen[r["brand_id"]]["prompt"] == r["prompt"]
            continue
        seen[r["brand_id"]] = r
    for bid, r in seen.items():
        add("v23", "A", bid, "legacy", bid, r["prompt"], runner, runner,
            brand=r["brand_name"], spirit_type=r["spirit_type"], tier=r["tier"])
    seen = {}
    for r in recB:
        if r["probe_id"] in seen:
            assert seen[r["probe_id"]]["prompt"] == r["prompt"]
            continue
        seen[r["probe_id"]] = r
    for pid, r in seen.items():
        add("v23", "B", pid, "legacy", pid, r["prompt"], runner, runner, channel=r["channel"])


def main():
    export_v19()
    export_v2x("v20", ROOT / "scripts/run_acquisition_v20.py",
               lambda m: json.load(open(ROOT / "prereg/v0_20_registry.json")), "prereg/v0_20_registry.json")
    export_v2x("v21", ROOT / "scripts/run_acquisition_v21.py",
               lambda m: json.load(open(ROOT / "prereg/v0_21_registry.json")), "prereg/v0_21_registry.json")
    export_v2x("v22", ROOT / "scripts/run_acquisition_v22.py",
               lambda m: m.load_prereg_module(ROOT / "prereg/v0_22_automotive_content.py"),
               "prereg/v0_22_automotive_content.py")
    export_v23()

    counts = defaultdict(int)
    for p in probes:
        counts[p["phase"]] += 1
    per_sub = defaultdict(lambda: defaultdict(int))
    for p in probes:
        per_sub[p["substrate"]][p["phase"]] += 1
    print("exported:", len(probes), dict(counts))
    print({k: dict(v) for k, v in per_sub.items()})
    ids = [(p["substrate"], p["phase"], p["probe_id"]) for p in probes]
    if len(probes) != 142 or counts["A"] != 112 or counts["B"] != 30 or len(set(ids)) != len(ids):
        print("STOP: expected 142 distinct probes (112 A + 30 B); got", len(probes), dict(counts))
        sys.exit(3)
    OUT_PROBES.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PROBES, "w", encoding="utf-8") as f:
        for p in probes:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")
    print("wrote", OUT_PROBES)

    # ---- artifact checksums vs the v0.41 manifest
    text = open(MANIFEST, encoding="utf-8").read()
    pairs = re.findall(r"`([^`]+\.(?:jsonl|json|py))`\s*\|\s*`([0-9a-f]{64})`", text)
    chk = []
    for path, sha in pairs:
        p = ROOT / path
        got = hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
        chk.append({"artifact": path, "manifest_sha256": sha, "current_sha256": got, "match": got == sha})

    # ---- parity vs t3 recorded prompts
    by_sub = defaultdict(lambda: {"A": {}, "B": {}})
    for p in probes:
        by_sub[p["substrate"]][p["phase"]][p.get("brand_id") or p.get("frame_id")] = p

    def new(sub):
        return {"exported": len(by_sub[sub]["A"]) + len(by_sub[sub]["B"]),
                "exported_A": len(by_sub[sub]["A"]), "exported_B": len(by_sub[sub]["B"]),
                "recorded_rows": 0, "recorded_units": 0, "exact_matches": 0,
                "mismatch_count": 0, "mismatches": [], "not_recorded": [], "unexpected_units": []}
    parity = {}

    s = new("v19")
    qa = [json.loads(l) for l in open(ROOT / "osf/v19/phase_a_queries.jsonl")]
    qb = [json.loads(l) for l in open(ROOT / "osf/v19/phase_b_queries.jsonl")]
    ra = [json.loads(l) for l in open(T3 / "v19/phase_a_responses.jsonl")]
    rb = [json.loads(l) for l in open(T3 / "v19/phase_b_responses.jsonl")]
    s["prompt_text_recorded_in_t3"] = False
    s["note"] = ("osf/v41/data/v19/*_responses.jsonl stores query_id/brand/frame + response but no prompt text; "
                 "prompt parity rests on the artifact checksums plus query_id coverage")
    s["recorded_rows"] = len(ra) + len(rb)
    s["recorded_query_ids_equal_artifact_query_ids"] = ({q["query_id"] for q in qa + qb} == {r["query_id"] for r in ra + rb})
    s["not_recorded"] = "all %d exported (no prompt text in t3 data)" % s["exported"]
    parity["v19"] = s

    for sub in ("v20", "v21", "v22"):
        s = new(sub)
        hit = set()
        for ph, fn, textf in (("A", "phase_a_results.csv", "probe_text"), ("B", "phase_b_results.csv", "frame_text")):
            for r in csv.DictReader(open(T3 / sub / fn, encoding="utf-8")):
                s["recorded_rows"] += 1
                unit = f"{r['cell']}.{r['cascade_order']}" if ph == "A" else r["frame_id"]
                ex = by_sub[sub][ph].get(unit)
                if ex is None:
                    s["unexpected_units"].append(f"{ph}:{unit}")
                    s["mismatch_count"] += 1
                    continue
                hit.add((ph, unit))
                if r[textf] == ex["prompt"]:
                    s["exact_matches"] += 1
                else:
                    s["mismatch_count"] += 1
                    if len(s["mismatches"]) < 5:
                        s["mismatches"].append({"phase": ph, "unit": unit, "recorded": r[textf], "exported": ex["prompt"]})
        s["recorded_units"] = len(hit)
        s["not_recorded"] = [f"{ph}:{u}" for ph in "AB" for u in by_sub[sub][ph] if (ph, u) not in hit]
        parity[sub] = s

    s = new("v23")
    hit = set()
    for ph, fn in (("A", "v23_phase_a_raw.json"), ("B", "v23_phase_b_raw.json")):
        for r in json.load(open(T3 / "v23" / fn, encoding="utf-8")):
            s["recorded_rows"] += 1
            unit = r["brand_id"] if ph == "A" else r["probe_id"]
            ex = by_sub["v23"][ph].get(unit)
            if ex is None:
                s["unexpected_units"].append(f"{ph}:{unit}")
                s["mismatch_count"] += 1
                continue
            hit.add((ph, unit))
            if r["prompt"] == ex["prompt"]:
                s["exact_matches"] += 1
            else:
                s["mismatch_count"] += 1
                if len(s["mismatches"]) < 5:
                    s["mismatches"].append({"phase": ph, "unit": unit, "recorded": r["prompt"], "exported": ex["prompt"]})
    s["recorded_units"] = len(hit)
    s["not_recorded"] = [f"{ph}:{u}" for ph in "AB" for u in by_sub["v23"][ph] if (ph, u) not in hit]
    parity["v23"] = s

    settings = {
        "system_prompts": "None. Every legacy runner sends a single user message; system = null for all 142 probes.",
        "v19": {"source": "protocol/providers.py", "max_tokens": 1024, "temperature": "provider default (not set)",
                "note": "Gemini via google.generativeai generation_config max_output_tokens=1024; 3 attempts, 1/2/4 s backoff"},
        "v20_v21_v22": {"source": "call_llm in scripts/run_acquisition_v2{0,1,2}.py",
                        "observed_max_tokens_at_stub_boundary": {k: observed_max_tokens.get(k) for k in ("v20", "v21", "v22")},
                        "temperature": "provider default (not set)",
                        "note": "Phase A max_tokens=64, Phase B 2048 (Gemini: no cap passed); v22 dispatcher run_v22 loads the prereg module via the runner default path ~/aias/prereg (main tree), not the worktree"},
        "v23": {"source": "scripts/acquire_v0_23.py call_*", "max_tokens": 2048, "temperature": 0.0,
                "note": "temperature=0.0 and max_tokens=2048 for all three providers; Phase A prompt interpolates spirit_type"},
        "cannot_carry_over_to_t4": [
            "v0.23 temperature=0.0 (t4 leaves temperature at provider default; claude-fable-5-2 must not receive temperature)",
            "legacy max_tokens: v0.19 1024; v0.20-22 Phase A 64 / Phase B 2048; v0.23 2048 (t4 uses 16,384 max output)",
            "legacy calls had no tools (S0-like); t4 adds an S1 web-search condition",
            "legacy google.generativeai (deprecated) SDK path for v0.19-v0.22; t4 uses google-genai",
        ],
    }
    out = {"exported_total": len(probes), "exported_A": counts["A"], "exported_B": counts["B"],
           "artifact_checksum_count": len(chk),
           "artifact_checksums_all_match": len(chk) == 8 and all(c["match"] for c in chk),
           "artifact_checksums": chk, "per_substrate": parity, "legacy_settings": settings}
    json.dump(out, open(OUT_PARITY, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print("wrote", OUT_PARITY)
    for sub, s in parity.items():
        print(sub, {k: (len(v) if isinstance(v, list) else v) for k, v in s.items() if k != "note"})
    print("checksums:", [(c["artifact"], c["match"]) for c in chk])


if __name__ == "__main__":
    main()
