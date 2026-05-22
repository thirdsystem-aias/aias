#!/usr/bin/env bash
#
# v20_osf_deposit.sh — Final OSF deposit for v0.20 artifacts.
#
# Pushes four target directories to osf.io/ec6wh/v20/{figures,paper,scoring,reports}
# using the established osf_upload_v2.py pattern (nested-folder safe).
#
# Pre-requisites:
#   - $OSF_TOKEN set in environment (or sourced from ~/.api_keys)
#   - All four source directories exist locally
#   - All artifacts in final state (paper PDF rendered, charts present,
#     verdicts.json scored, brand-format report built)
#
# Idempotent: re-running re-uploads files (OSF treats same-name files as
# new versions). Safe to run multiple times.

set -uo pipefail   # intentionally NOT -e: we want to continue after individual failures

AIAS_ROOT="${HOME}/aias"
SCRIPT="${AIAS_ROOT}/scripts/osf_upload_v2.py"

# Source token from ~/.api_keys if not already in env
if [[ -z "${OSF_TOKEN:-}" ]] && [[ -f "${HOME}/.api_keys" ]]; then
    # shellcheck disable=SC1091
    source "${HOME}/.api_keys"
fi

if [[ -z "${OSF_TOKEN:-}" ]]; then
    echo "ERROR: OSF_TOKEN not set in environment or ~/.api_keys"
    exit 2
fi

if [[ ! -f "${SCRIPT}" ]]; then
    echo "ERROR: osf_upload_v2.py not found at ${SCRIPT}"
    echo "  Expected: ~/aias/scripts/osf_upload_v2.py"
    exit 2
fi

echo "==========================================="
echo "AIAS v0.20 final OSF deposit"
echo "==========================================="
echo "  Project: osf.io/ec6wh"
echo "  Phase:   v20/"
echo "  Token:   $(echo "${OSF_TOKEN}" | head -c 8)... (length $(echo -n "${OSF_TOKEN}" | wc -c))"
echo ""

# Target table: local_source → remote_path → label
declare -a TARGETS=(
    "${AIAS_ROOT}/reports/figs/v20|v20/figures|Charts (3 PDFs)"
    "${AIAS_ROOT}/papers/v0_20|v20/paper|SSRN paper PDF + markdown + build script + submission packet"
    "${AIAS_ROOT}/osf/v20|v20/scoring|Phase A/B CSVs + verdicts.json + scoring code"
    "${AIAS_ROOT}/osf/v20/reports|v20/reports|Brand-format report PDF"
)

# Track results
SUCCESS=()
FAILED=()
SKIPPED=()

for entry in "${TARGETS[@]}"; do
    IFS='|' read -r src remote label <<< "${entry}"

    echo "-------------------------------------------"
    echo "Target: ${label}"
    echo "  Source: ${src}"
    echo "  Remote: ${remote}"

    if [[ ! -d "${src}" ]]; then
        echo "  ⚠ SKIPPED: source directory does not exist"
        SKIPPED+=("${label} (${src} missing)")
        continue
    fi

    # Count files (top-level + subdirs)
    file_count=$(find "${src}" -type f 2>/dev/null | wc -l | tr -d ' ')
    echo "  Files to deposit: ${file_count}"

    if [[ "${file_count}" -eq 0 ]]; then
        echo "  ⚠ SKIPPED: source directory is empty"
        SKIPPED+=("${label} (empty)")
        continue
    fi

    # Run the uploader
    if python3 "${SCRIPT}" "${src}" "${remote}"; then
        echo "  ✓ deposit succeeded"
        SUCCESS+=("${label}")
    else
        rc=$?
        echo "  ✗ deposit FAILED (exit ${rc})"
        FAILED+=("${label}")
    fi
    echo ""
done

# Summary
echo "==========================================="
echo "Summary"
echo "==========================================="
echo "  Succeeded: ${#SUCCESS[@]}"
for s in "${SUCCESS[@]}"; do echo "    ✓ ${s}"; done

if [[ "${#SKIPPED[@]}" -gt 0 ]]; then
    echo "  Skipped: ${#SKIPPED[@]}"
    for s in "${SKIPPED[@]}"; do echo "    ⚠ ${s}"; done
fi

if [[ "${#FAILED[@]}" -gt 0 ]]; then
    echo "  Failed: ${#FAILED[@]}"
    for s in "${FAILED[@]}"; do echo "    ✗ ${s}"; done
    exit 1
fi

echo ""
echo "✓ v0.20 deposit complete."
echo "  Browse: https://osf.io/ec6wh/files/osfstorage/v20/"
echo ""
echo "Post-deposit:"
echo "  1. (Optional) Update SSRN 6811441 abstract page to reference the OSF deposit"
echo "  2. Update tomorrow.md to close out the v0.20 cycle"
echo "  3. Consider closing the v0.20-skincare-il-gradient branch back into main"
