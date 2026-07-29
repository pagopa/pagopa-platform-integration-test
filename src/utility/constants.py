"""Shared path constants used across scripts and integration suites."""
from pathlib import Path

# Repository root directory.
REPO_ROOT = Path(__file__).resolve().parents[2]

# Source root directory (src/).
SRC_ROOT = REPO_ROOT / "src"

# Integration suite root directory (src/integration/).
INTEGRATION_ROOT = SRC_ROOT / "integration"
