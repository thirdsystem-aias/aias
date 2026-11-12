"""Write prereg/LOCK_MANIFEST_v1_18.sha256: SHA-256 of every locked v1.18 file and every input (repo-relative
paths for files in this worktree; absolute paths for the t4 inputs in the v0.42 worktree). Re-run after the
audit, immediately before the lock commit."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import common_v1_18 as C  # noqa: E402

REPO = C.PHASE.parents[2]
V042 = Path.home() / "aias" / "_worktrees" / "v0.42" / "osf" / "v42"
LOCKED = [
    "prereg/PRE_REGISTRATION_v1_18.md", "registries/domain_rules_v1_18.md", "registries/domain_table_v1_18.csv",
    "registries/build_domain_table_v1_18.py", "registries/draw_audit_sample_v1_18.py",
    "registries/audit_sheet_v1_18.csv", "registries/audit_key_v1_18.csv",
    "scripts/common_v1_18.py", "scripts/extract_domains_v1_18.py", "scripts/analyse_v1_18.py",
    "scripts/tests/test_v1_18.py", "outputs/prelock/domains_to_classify_v1_18.txt",
    "outputs/prelock/domains_to_classify_cited_v1_18.txt", "outputs/prelock/prelock_counts_v1_18.json",
    "outputs/dry_run/dry_run_v1_18.txt", "DEVIATIONS.md", "README.md",
]
INPUTS_REPO = ["osf/methodology/v1_13/scripts/score_v1_13.py", "osf/methodology/v1_13/prereg/source_classes_v1_13.md",
               "osf/methodology/v1_13/registries/brand_domains_v1_13.csv"]
INPUTS_ABS = [V042 / "data" / "t4_raw.jsonl"] + sorted((V042 / "data" / "coded").glob("*_phase_b.csv"))


def main():
    lines = ["# v1.18 lock manifest (DRAFT until the lock commit). sha256  path"]
    for rel in LOCKED:
        p = C.PHASE / rel
        lines.append(f"{C.sha256_file(p)}  osf/methodology/v1_18/{rel}")
    for rel in INPUTS_REPO:
        lines.append(f"{C.sha256_file(REPO / rel)}  {rel}")
    for p in INPUTS_ABS:
        lines.append(f"{C.sha256_file(p)}  {p}")
    out = C.PHASE / "prereg" / "LOCK_MANIFEST_v1_18.sha256"
    out.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
