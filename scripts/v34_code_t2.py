#!/usr/bin/env python3
"""
v34_code_t2.py — post-acquisition coding of the t2 data for v0.19 and v0.23.

v0.20/0.21/0.22 need no coding step (recall is matched at extraction in score_v34).
v0.19 and v0.23 do:
  - v0.19: acquire_v0_19.parse_phase_a/parse_phase_b  (DETERMINISTIC string-match
           -> phase_{a,b}_results.csv with recognition_yes / mentioned+rank).
  - v0.23: score_v0_23.score_phase_b  (DETERMINISTIC find_brand_mentions -> recall),
           score_v0_23.score_phase_a  (LLM judge_recognition -> r_level -> C_P).
Re-pointed to osf/v34/data/<sub>/; the t1 coding functions are reused verbatim.
"""
import importlib.util
import sys
from pathlib import Path

ROOT = Path.home() / "aias"
DATA = ROOT / "osf" / "v34" / "data"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, str(path))
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


def code_v19():
    m = _load(ROOT / "osf/v19/acquire_v0_19.py", "acq19")
    d = DATA / "v19"
    m.PHASE_A_RESULTS = d / "phase_a_results.csv"
    m.PHASE_B_RESULTS = d / "phase_b_results.csv"
    print("[v19] parse-phase-a ...")
    m.parse_phase_a(d / "phase_a_responses.jsonl")
    print("[v19] parse-phase-b ...")
    m.parse_phase_b(d / "phase_b_responses.jsonl")
    print(f"[v19] coded -> {d}/phase_{{a,b}}_results.csv")


def code_v23():
    m = _load(ROOT / "scripts/score_v0_23.py", "sc23")
    d = DATA / "v23"
    # re-point all derived path constants (computed at import from DATA_DIR)
    m.DATA_DIR = d
    m.PHASE_A_RAW = d / "v23_phase_a_raw.json"
    m.PHASE_B_RAW = d / "v23_phase_b_raw.json"
    m.PHASE_A_SCORED = d / "v23_phase_a_scored.json"
    m.PHASE_B_SCORED = d / "v23_phase_b_scored.json"

    # Judge pinning + provenance (guidance #2): the recognition judge is part of the
    # locked v23 coding pipeline. Reproduce verbatim with the SAME alias t1 used; HALT
    # if it no longer resolves; record the judge's returned model id to the sidecar.
    judge_alias = m.JUDGE_MODEL
    print(f"[v23] locked recognition judge alias: {judge_alias}")
    try:
        import anthropic
        probe = anthropic.Anthropic().messages.create(
            model=judge_alias, max_tokens=4,
            messages=[{"role": "user", "content": "ok"}])
        print(f"[v23] judge resolves -> {probe.model}")
    except Exception as e:
        sys.exit(f"[v23] HALT: judge alias {judge_alias} did not resolve ({e}). "
                 f"This is a DEVIATIONS decision, not an improvisation — surface it.")

    # install the SDK provenance tee so judge calls record their returned id
    sys.path.insert(0, str(ROOT / "scripts"))
    import run_acquisition_v34 as ORCH
    import v34_provenance as PROV
    ORCH.install_sdk_provenance()

    client = anthropic.Anthropic()
    print("[v23] score_phase_b (deterministic brand mentions; no LLM) ...")
    PROV.set_context("v23", "B_code")
    m.score_phase_b(client)
    print("[v23] score_phase_a (LLM recognition judge -> r_level) ...")
    PROV.set_context("v23", "A_judge")
    m.score_phase_a(client)
    print(f"[v23] coded -> {d}/v23_phase_{{a,b}}_scored.json  (judge calls in sidecar, phase=A_judge)")


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "v19"):
        code_v19()
    if which in ("all", "v23"):
        code_v23()
    print("v34_code_t2: done")
