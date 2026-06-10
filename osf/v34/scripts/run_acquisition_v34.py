#!/usr/bin/env python3
"""
run_acquisition_v34.py — LOGGING SHELL over the five verbatim t1 runners (t2 wave).

Permitted actions ONLY: (i) redirect each runner's output to osf/v34/data/<sub>/;
(ii) tee the provider-returned model id per call to osf/v34/data/v34_provenance.csv.
It imports each verbatim t1 runner and invokes that runner's OWN phase functions, and
wraps the provider SDK call boundary (not the runner internals) for provenance. Probe
text, frame ordering, registry, and every runner's output schema are unchanged; the
five probe-set checksums in acquisition_manifest_v34.md remain valid.

Usage:
  python3 scripts/run_acquisition_v34.py --substrate v20
  python3 scripts/run_acquisition_v34.py --substrate all
"""
import argparse
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path.home() / "aias"
sys.path.insert(0, str(ROOT / "scripts"))
import v34_provenance as PROV

DATA = ROOT / "osf" / "v34" / "data"


def install_sdk_provenance():
    """Wrap the four SDK call boundaries the runners use; pure tee, behavior unchanged."""
    def mk(orig, alias_from, id_from):
        def wrap(self, *a, **k):
            r = orig(self, *a, **k)
            try:
                PROV.record(alias_from(self, k), id_from(r))
            except Exception:
                pass
            return r
        wrap._v34 = True
        return wrap

    # anthropic — client.messages.create
    try:
        from anthropic.resources.messages import Messages
        if not getattr(Messages.create, "_v34", False):
            Messages.create = mk(Messages.create,
                                  lambda s, k: k.get("model"),
                                  lambda r: getattr(r, "model", None))
        print("  patched: anthropic Messages.create")
    except Exception as e:
        print(f"  anthropic patch skip: {e}")

    # openai — client.chat.completions.create
    try:
        from openai.resources.chat.completions import Completions
        if not getattr(Completions.create, "_v34", False):
            Completions.create = mk(Completions.create,
                                    lambda s, k: k.get("model"),
                                    lambda r: getattr(r, "model", None))
        print("  patched: openai Completions.create")
    except Exception as e:
        print(f"  openai patch skip: {e}")

    # google old (deprecated) — GenerativeModel.generate_content
    try:
        import google.generativeai as gga
        if not getattr(gga.GenerativeModel.generate_content, "_v34", False):
            gga.GenerativeModel.generate_content = mk(
                gga.GenerativeModel.generate_content,
                lambda s, k: getattr(s, "model_name", None),
                lambda r: getattr(r, "model_version", None))
        print("  patched: google.generativeai GenerativeModel.generate_content")
    except Exception as e:
        print(f"  google-old patch skip: {e}")

    # google new — Models.generate_content
    try:
        from google.genai.models import Models
        if not getattr(Models.generate_content, "_v34", False):
            Models.generate_content = mk(Models.generate_content,
                                         lambda s, k: k.get("model"),
                                         lambda r: getattr(r, "model_version", None))
        print("  patched: google.genai Models.generate_content")
    except Exception as e:
        print(f"  google-new patch skip: {e}")


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


def run_v20_like(modpath, modname, registry_path, substrate):
    """v0.20 / v0.21: run_phase_a(reg, out, workers, dry); run_phase_b(...)."""
    m = _load(str(modpath), modname)
    reg = json.load(open(registry_path))
    outdir = DATA / substrate
    outdir.mkdir(parents=True, exist_ok=True)
    print(f"\n=== {substrate}: Phase A ({modname}) ===")
    PROV.set_context(substrate, "A")
    m.run_phase_a(reg, outdir / "phase_a_results.csv", 6, False)
    print(f"=== {substrate}: Phase B ({modname}) ===")
    PROV.set_context(substrate, "B")
    m.run_phase_b(reg, outdir / "phase_b_results.csv", 6, False)
    print(f"=== {substrate}: done -> {outdir} ===")


def run_v22():
    """v0.22: main() builds registry from prereg module; invoke per phase via argv."""
    m = _load(str(ROOT / "scripts/run_acquisition_v22.py"), "racq_v22")
    outdir = DATA / "v22"
    outdir.mkdir(parents=True, exist_ok=True)
    for phase, label in [("a", "A"), ("b", "B")]:
        print(f"\n=== v22: Phase {label} ===")
        PROV.set_context("v22", label)
        sys.argv = ["racq_v22", "--output-dir", str(outdir), "--phase", phase]
        m.main()
    print(f"=== v22: done -> {outdir} ===")


def run_v23():
    """v0.23: patch module OUTPUT_DIR, invoke main() per phase; writes *_raw.json."""
    m = _load(str(ROOT / "scripts/acquire_v0_23.py"), "racq_v23")
    outdir = DATA / "v23"
    outdir.mkdir(parents=True, exist_ok=True)
    m.OUTPUT_DIR = outdir            # module-global redirect (output-path edit)
    for flag, label in [("--phase-a-only", "A"), ("--phase-b-only", "B")]:
        print(f"\n=== v23: Phase {label} ===")
        PROV.set_context("v23", label)
        sys.argv = ["racq_v23", flag]
        m.main()
    print(f"=== v23: done -> {outdir} ===")


def run_v19():
    """v0.19: patch RESPONSES paths, call run_phase directly; then parse->results.csv."""
    m = _load(str(ROOT / "osf/v19/run_v0_19.py"), "racq_v19")
    outdir = DATA / "v19"
    outdir.mkdir(parents=True, exist_ok=True)
    m.PHASE_A_RESPONSES = outdir / "phase_a_responses.jsonl"
    m.PHASE_B_RESPONSES = outdir / "phase_b_responses.jsonl"
    print("\n=== v19: Phase A ===")
    PROV.set_context("v19", "A")
    m.run_phase(m.PHASE_A_QUERIES, m.PHASE_A_RESPONSES, "A")
    print("=== v19: Phase B ===")
    PROV.set_context("v19", "B")
    m.run_phase(m.PHASE_B_QUERIES, m.PHASE_B_RESPONSES, "B")
    print(f"=== v19: acquisition done -> {outdir} (parse to results.csv done separately) ===")


SUBSTRATES = {
    "v20": lambda: run_v20_like(ROOT / "scripts/run_acquisition_v20.py", "racq_v20",
                                ROOT / "prereg/v0_20_registry.json", "v20"),
    "v21": lambda: run_v20_like(ROOT / "scripts/run_acquisition_v21.py", "racq_v21",
                                ROOT / "prereg/v0_21_registry.json", "v21"),
    "v22": run_v22,
    "v23": run_v23,
    "v19": run_v19,
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--substrate", required=True, help="v19|v20|v21|v22|v23|all")
    args = ap.parse_args()
    print("run_acquisition_v34 — installing SDK provenance tee:")
    install_sdk_provenance()
    targets = list(SUBSTRATES) if args.substrate == "all" else [args.substrate]
    for s in targets:
        if s not in SUBSTRATES:
            print(f"  substrate {s} not yet wired in this shell; skipping")
            continue
        SUBSTRATES[s]()
    print("\nrun_acquisition_v34: complete for", targets)


if __name__ == "__main__":
    sys.exit(main())
