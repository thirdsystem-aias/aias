#!/usr/bin/env python3
"""
v41_code_t3.py — post-acquisition coding of the t3 data for v0.19 and v0.23.

Fork of v34_code_t2.py (v0.34, t2). Changes: data folder osf/v41/data/, the v41
provenance sidecar, and the AIAS root read from $AIAS_ROOT. The t1 coding functions
are reused verbatim, as at t2.

v0.20/0.21/0.22 need no coding step (recall is matched at extraction in score_v41).
  - v0.19: acquire_v0_19.parse_phase_a/parse_phase_b (deterministic string match)
           -> phase_{a,b}_results.csv.
  - v0.23: score_v0_23.score_phase_b (deterministic brand mentions) and
           score_v0_23.score_phase_a (LLM recognition judge, the t1/t2 alias
           claude-sonnet-4-5) -> v23_phase_{a,b}_scored.json. The judge is coding,
           not acquisition (pre-registration ACQUISITION: coding_not_acquisition).

Run after the t3 acquisition, before score_v41.py --run:
  AIAS_ROOT=<tree> ~/aias/.venv-v41/bin/python osf/v41/scripts/v41_code_t3.py [all|v19|v23]
"""
import importlib.util
import os
import sys
from pathlib import Path

ROOT = Path(os.environ.get("AIAS_ROOT", str(Path.home() / "aias")))
DATA = ROOT / "osf" / "v41" / "data"
HERE = Path(__file__).resolve().parent


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
    m.DATA_DIR = d
    m.PHASE_A_RAW = d / "v23_phase_a_raw.json"
    m.PHASE_B_RAW = d / "v23_phase_b_raw.json"
    m.PHASE_A_SCORED = d / "v23_phase_a_scored.json"
    m.PHASE_B_SCORED = d / "v23_phase_b_scored.json"

    judge_alias = m.JUDGE_MODEL
    print(f"[v23] locked recognition judge alias: {judge_alias}")
    try:
        import anthropic
        probe = anthropic.Anthropic().messages.create(
            model=judge_alias, max_tokens=4, messages=[{"role": "user", "content": "ok"}])
        print(f"[v23] judge resolves -> {probe.model}")
    except Exception as e:
        sys.exit(f"[v23] HALT: judge alias {judge_alias} did not resolve ({e}). "
                 f"This is a DEVIATIONS decision, not an improvisation; surface it.")

    sys.path.insert(0, str(HERE))
    import run_acquisition_v41 as ORCH
    import v41_provenance as PROV
    ORCH.install_sdk_provenance()

    client = anthropic.Anthropic()
    print("[v23] score_phase_b (deterministic brand mentions; no LLM) ...")
    PROV.set_context("v23", "B_code")
    m.score_phase_b(client)
    print("[v23] score_phase_a (LLM recognition judge -> r_level) ...")
    PROV.set_context("v23", "A_judge")
    m.score_phase_a(client)
    print(f"[v23] coded -> {d}/v23_phase_{{a,b}}_scored.json (judge calls in the sidecar, phase=A_judge)")


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "v19"):
        code_v19()
    if which in ("all", "v23"):
        code_v23()
    print("v41_code_t3: done")
