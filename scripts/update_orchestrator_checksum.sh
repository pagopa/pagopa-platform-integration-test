#!/usr/bin/env bash
##############################################################################
# update_orchestrator_checksum.sh
#
# Maintainer helper: regenerates scripts/tas_orchestrator.py.sha256 after any
# change to scripts/tas_orchestrator.py. The sidecar file is published on
# the same ref as the script and consumed by integrators (ADO template and
# the orchestrator-based examples) to verify the integrity of the download
# (`sha256sum -c`).
#
# Run from anywhere in the repo:
#   ./scripts/update_orchestrator_checksum.sh
#
# CI hint: add a check that fails the build when the script and its sidecar
# drift apart (e.g. `sha256sum -c scripts/tas_orchestrator.py.sha256` from
# inside `scripts/`).
##############################################################################
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}"

TARGET="tas_orchestrator.py"
SIDECAR="${TARGET}.sha256"

if [ ! -f "${TARGET}" ]; then
  echo "error: ${TARGET} not found in ${SCRIPT_DIR}" >&2
  exit 1
fi

# Prefer sha256sum (Linux/CI), fall back to shasum -a 256 (macOS).
if command -v sha256sum >/dev/null 2>&1; then
  sha256sum "${TARGET}" > "${SIDECAR}"
elif command -v shasum >/dev/null 2>&1; then
  shasum -a 256 "${TARGET}" > "${SIDECAR}"
else
  echo "error: neither sha256sum nor shasum available" >&2
  exit 1
fi

echo "updated ${SCRIPT_DIR}/${SIDECAR}:"
cat "${SIDECAR}"

