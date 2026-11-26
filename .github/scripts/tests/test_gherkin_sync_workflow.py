"""Local checks for the Gherkin sync workflow; no GitHub or Gemini calls."""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest
import yaml

WORKFLOW = Path(__file__).resolve().parents[2] / "workflows" / "gherkin-manifest-sync.yml"


@pytest.fixture(scope="module")
def workflow() -> dict:
    """Parse the workflow and surface malformed YAML."""
    return yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def bash() -> str:
    """Use the explicitly selected Bash, or an available Bash when none is selected."""
    executable = os.environ.get("GHERKIN_TEST_BASH") or shutil.which("bash")
    if not executable:
        pytest.skip("Bash is not available")
    return executable


def test_workflow_shell_blocks_parse(workflow: dict, bash: str) -> None:
    """Every workflow run block has valid Bash syntax without executing it."""
    blocks = [
        step["run"]
        for job in workflow["jobs"].values()
        for step in job["steps"]
        if "run" in step
    ]
    assert blocks
    for block in blocks:
        subprocess.run(
            [bash, "-n"], input=block, text=True, encoding="utf-8",
            capture_output=True, check=True,
        )


@pytest.mark.parametrize(
    "event,author,head_repo,head_ref,expected",
    [
        ("pull_request", "github-actions[bot]", "example/repo", "automation/gherkin-sync/run-12-1", "false"),
        ("pull_request", "contributor", "example/repo", "automation/gherkin-sync/run-12-1", "true"),
        ("pull_request", "github-actions[bot]", "other/repo", "automation/gherkin-sync/run-12-1", "true"),
        ("workflow_dispatch", "", "", "", "true"),
    ],
)
def test_sync_pr_merge_does_not_trigger_a_loop(
    workflow: dict, bash: str, tmp_path: Path,
    event: str, author: str, head_repo: str, head_ref: str, expected: str,
) -> None:
    """Only the bot's own sync PR is suppressed; manual and other PR events keep their normal gate."""
    gate = next(step for step in workflow["jobs"]["evaluate_trigger"]["steps"] if step.get("id") == "gate")
    output = tmp_path / "output.txt"
    env = {
        **os.environ,
        "EVENT_NAME": event,
        "PR_AUTHOR": author,
        "PR_HEAD_REPO": head_repo,
        "PR_HEAD_REF": head_ref,
        "PR_NUMBER": "12",
        "PR_CHANGED_FILES": "0",
        "REPO": "example/repo",
        "GH_TOKEN": "unused",
        "GITHUB_OUTPUT": "output.txt",
        "GITHUB_STEP_SUMMARY": "summary.txt",
    }
    subprocess.run(
        [bash, "-c", gate["run"]], cwd=tmp_path, env=env,
        text=True, encoding="utf-8", capture_output=True, check=True,
    )
    assert f"run={expected}" in output.read_text(encoding="utf-8").splitlines()


@pytest.mark.parametrize(
    "filename,expected",
    [
        ("src/integration/fdr3/features/example.feature", True),
        (".github/gherkin-manifest.yml", True),
        (".github/unrelated.json", False),
        ("src/integration/fdr3/README.md", False),
    ],
)
def test_gate_selects_only_features_and_manifest(
    workflow: dict, filename: str, expected: bool,
) -> None:
    """The PR file filter includes feature and manifest changes only."""
    gate = next(step for step in workflow["jobs"]["evaluate_trigger"]["steps"] if step.get("id") == "gate")
    match = re.search(r'test\("([^"]+)"\)', gate["run"])
    assert match is not None
    pattern = json.loads(f'"{match.group(1)}"')
    assert bool(re.search(pattern, filename)) is expected


def test_manifest_sync_has_no_ai_credentials(workflow: dict) -> None:
    """The manifest workflow does not depend on AI credentials."""
    assert "GEMINI_API_KEY" not in str(workflow)
