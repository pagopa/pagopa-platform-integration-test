"""Shared path constants used across scripts and integration suites."""
from pathlib import Path

# Repository root directory.
REPO_ROOT = Path(__file__).resolve().parents[2]


# Source root directory (src/).
SRC_ROOT = REPO_ROOT / "src"

# Integration suite root directory (src/integration/).
INTEGRATION_ROOT = SRC_ROOT / "integration"

GITHUB_ROOT = REPO_ROOT / ".github"

# Relative path to the summary.json file within the processed reports directory.
SUMMARY_FILE_PATH = "widgets/summary.json"

# Relative path to the folders containing the result for each scenario within the processed reports directory.
TEST_CASES_PATH = "data/test-cases"

