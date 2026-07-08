#!/usr/bin/env python3
"""
tas_orchestrator.py — CLI Bridge for the Test Automation Service.

Allows external systems (GitHub Actions from other repos, Azure DevOps, etc.)
to trigger Behave test suites in synchronous or asynchronous mode.

Usage:
  # Asynchronous mode (fire-and-forget)
  python tas_orchestrator.py --suite wisp --env uat --caller-id my-service

  # Synchronous mode (blocks until completion and returns the outcome)
  python tas_orchestrator.py --suite wisp --env uat --caller-id my-service --sync

  # Targeting a different test category (default: integration)
  python tas_orchestrator.py --type e2e --suite checkout --env uat --caller-id my-service --sync

Exit codes:
  0  — Tests completed successfully (or dispatch sent in async mode)
  1  — One or more scenarios failed
  2  — Orchestration error (configuration, timeout, GitHub API)

Required environment variables:
  GITHUB_TOKEN   : Personal Access Token with 'repo' and 'actions:read' permissions

Optional environment variables:
  GITHUB_REPO    : Target repo in "owner/repo" format (overrides the default)
  WORKFLOW_FILE  : Workflow filename (overrides the default)
"""

import argparse
import json
import logging
import os
import sys
import time
import uuid
import zipfile
from io import BytesIO
from typing import Optional

import requests

# ── Configuration constants ──────────────────────────────────────────────────

DEFAULT_REPO = "pagopa/pagopa-platform-integration-test"
DEFAULT_WORKFLOW = "test-automation-service.yml"
DEFAULT_REF = "main"

# Interval between run status polls (seconds)
POLL_INTERVAL_SECONDS = 15
# Maximum timeout waiting for run completion (60 minutes)
POLL_TIMEOUT_SECONDS = 3600
# Number of retries to locate the run after dispatch
RUN_LOOKUP_RETRIES = 20
# Wait between run lookup attempts (seconds)
RUN_LOOKUP_WAIT_SECONDS = 5

GITHUB_API_BASE = "https://api.github.com"

# ── Logging ───────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


# ── GitHub API client ────────────────────────────────────────────────────────

class GitHubClient:
    """Minimal wrapper around the GitHub Actions API required by the orchestrator."""

    def __init__(self, token: str, repo: str):
        self.repo = repo
        self._session = requests.Session()
        self._session.headers.update({
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        })

    def _get(self, path: str, **kwargs) -> requests.Response:
        url = f"{GITHUB_API_BASE}{path}"
        response = self._session.get(url, **kwargs)
        response.raise_for_status()
        return response

    def _post(self, path: str, **kwargs) -> requests.Response:
        url = f"{GITHUB_API_BASE}{path}"
        response = self._session.post(url, **kwargs)
        return response

    def trigger_workflow(self, workflow_file: str, ref: str, inputs: dict) -> None:
        """
        Sends a workflow_dispatch event.
        GitHub responds with HTTP 204 (No Content) — no run_id is returned.
        """
        path = f"/repos/{self.repo}/actions/workflows/{workflow_file}/dispatches"
        payload = {"ref": ref, "inputs": inputs}
        response = self._post(path, json=payload)
        if response.status_code != 204:
            raise RuntimeError(
                f"Dispatch failed: HTTP {response.status_code} — {response.text}"
            )

    def find_run_by_name(self, workflow_file: str, run_name: str) -> Optional[dict]:
        """
        Searches for a workflow run by run-name in recent executions.
        The run-name includes the correlation_id, making it unique per invocation.
        """
        path = f"/repos/{self.repo}/actions/workflows/{workflow_file}/runs"
        response = self._get(path, params={"per_page": 20, "event": "workflow_dispatch"})
        for run in response.json().get("workflow_runs", []):
            if run.get("name") == run_name:
                return run
        return None

    def get_run(self, run_id: int) -> dict:
        """Fetches the current state of a workflow run."""
        response = self._get(f"/repos/{self.repo}/actions/runs/{run_id}")
        return response.json()

    def list_artifacts(self, run_id: int) -> list:
        """Lists artifacts produced by a workflow run."""
        response = self._get(f"/repos/{self.repo}/actions/runs/{run_id}/artifacts")
        return response.json().get("artifacts", [])

    def download_artifact(self, artifact_id: int) -> bytes:
        """Downloads the zip content of an artifact."""
        path = f"/repos/{self.repo}/actions/artifacts/{artifact_id}/zip"
        response = self._get(path, allow_redirects=True)
        return response.content


# ── Result parsing ───────────────────────────────────────────────────────────

def parse_summary_from_zip(zip_content: bytes) -> dict:
    """
    Extracts and parses test-summary.json from the artifact zip.
    Falls back to parsing behave-results.json directly if needed.
    """
    with zipfile.ZipFile(BytesIO(zip_content)) as zf:
        names = zf.namelist()

        if "test-summary.json" in names:
            with zf.open("test-summary.json") as f:
                return json.load(f)

        # Fallback: the workflow only uploaded the raw Behave JSON
        if "behave-results.json" in names:
            log.warning("test-summary.json not found, computing summary from behave-results.json")
            with zf.open("behave-results.json") as f:
                return _parse_behave_json(json.load(f))

    raise RuntimeError("No result file found in artifact (test-summary.json / behave-results.json)")


def _parse_behave_json(features: list) -> dict:
    """Computes the summary by counting scenarios per status from raw Behave JSON output."""
    passed = failed = skipped = 0
    total_duration = 0.0

    for feature in features:
        for element in feature.get("elements", []):
            if element.get("type") != "scenario":
                continue
            status = element.get("status", "skipped")
            duration = sum(
                step.get("result", {}).get("duration", 0)
                for step in element.get("steps", [])
            )
            total_duration += duration
            if status == "passed":
                passed += 1
            elif status == "failed":
                failed += 1
            else:
                skipped += 1

    return {
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "total": passed + failed + skipped,
        "duration_seconds": round(total_duration, 2),
        "outcome": "success" if failed == 0 else "failure",
    }


def print_summary(summary: dict) -> None:
    """Prints a formatted results summary to stdout."""
    outcome_label = "PASSED" if summary["outcome"] == "success" else "FAILED"
    separator = "=" * 54

    print()
    print(separator)
    print("   TEST AUTOMATION SERVICE — RESULTS SUMMARY")
    print(separator)
    if summary.get("correlation_id"):
        print(f"   Correlation ID  : {summary['correlation_id']}")
    if summary.get("caller_id"):
        print(f"   Caller          : {summary['caller_id']}")
    if summary.get("suite"):
        print(f"   Suite           : {summary['suite']}")
    if summary.get("test_type"):
        print(f"   Type            : {summary['test_type']}")
    if summary.get("environment"):
        print(f"   Environment     : {summary['environment']}")
    if summary.get("ref"):
        ref_line = summary["ref"]
        if summary.get("sha"):
            ref_line = f"{ref_line} ({summary['sha'][:7]})"
        print(f"   Ref             : {ref_line}")
    print("-" * 54)
    print(f"   Passed          : {summary['passed']}")
    print(f"   Failed          : {summary['failed']}")
    print(f"   Skipped         : {summary['skipped']}")
    print(f"   Total           : {summary['total']}")
    print(f"   Duration        : {summary['duration_seconds']}s")
    print("-" * 54)
    print(f"   Outcome         : {outcome_label}")
    print(separator)
    print()


# ── Main orchestration logic ────────────────────────────────────────────────────

def run(args: argparse.Namespace) -> int:
    # Token validation
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        log.error("The GITHUB_TOKEN environment variable is not set.")
        return 2

    repo = os.environ.get("GITHUB_REPO", args.repo)
    workflow_file = os.environ.get("WORKFLOW_FILE", args.workflow)

    # Generate a correlation_id if not provided by the caller
    correlation_id = args.correlation_id or str(uuid.uuid4())
    # The run-name must match exactly the one defined in the workflow YAML
    run_name = f"tas-{correlation_id}"

    client = GitHubClient(token=token, repo=repo)

    inputs = {
        "test_type":      args.type,
        "test_suite":     args.suite,
        "environment":    args.env,
        "caller_id":      args.caller_id,
        "correlation_id": correlation_id,
    }

    log.info("Sending dispatch to '%s' (workflow: %s, ref: %s)", repo, workflow_file, args.ref)
    log.info("Type: %s | Suite: %s | Env: %s | Caller: %s | Correlation ID: %s",
             args.type, args.suite, args.env, args.caller_id, correlation_id)

    client.trigger_workflow(workflow_file=workflow_file, ref=args.ref, inputs=inputs)
    log.info("Dispatch sent successfully (HTTP 204).")

    # ── ASYNC mode: exit immediately ────────────────────────────────────────────────
    if not args.sync:
        # Print key values to stdout for easy capture by the pipeline
        print(f"CORRELATION_ID={correlation_id}")
        print(f"RUN_NAME={run_name}")
        log.info("Async mode: exiting immediately. Use CORRELATION_ID to monitor the run.")
        return 0

    # ── SYNC mode: locate the run and poll ───────────────────────────────────────
    log.info("Sync mode: looking up run '%s'...", run_name)

    # The run is not immediately visible after dispatch (GitHub latency ~2-10s).
    # Retry with fixed wait until the run appears in the API.
    run_data = None
    for attempt in range(1, RUN_LOOKUP_RETRIES + 1):
        time.sleep(RUN_LOOKUP_WAIT_SECONDS)
        run_data = client.find_run_by_name(workflow_file, run_name)
        if run_data:
            log.info("Run found: ID=%s | URL=%s", run_data["id"], run_data["html_url"])
            break
        log.info("Attempt %d/%d: run not yet visible, retrying...",
                 attempt, RUN_LOOKUP_RETRIES)

    if not run_data:
        log.error("Run '%s' not found after %d attempts.", run_name, RUN_LOOKUP_RETRIES)
        return 2

    run_id = run_data["id"]
    # Print key values to stdout for easy capture by the pipeline
    print(f"RUN_ID={run_id}")
    print(f"RUN_URL={run_data['html_url']}")
    print(f"CORRELATION_ID={correlation_id}")

    # ── Poll status until completion ──────────────────────────────────────────
    log.info("Polling run %s (timeout: %ds, interval: %ds)...",
             run_id, POLL_TIMEOUT_SECONDS, POLL_INTERVAL_SECONDS)

    elapsed = 0
    while elapsed < POLL_TIMEOUT_SECONDS:
        time.sleep(POLL_INTERVAL_SECONDS)
        elapsed += POLL_INTERVAL_SECONDS

        current = client.get_run(run_id)
        status = current["status"]
        conclusion = current.get("conclusion") or "—"
        log.info("[%ds elapsed] Status: %-12s Conclusion: %s", elapsed, status, conclusion)

        if status == "completed":
            log.info("Run completed with conclusion: %s", conclusion)
            break
    else:
        log.error("Timeout: run %s did not complete within %ds.", run_id, POLL_TIMEOUT_SECONDS)
        return 2

    # ── Download and parse the artifact ───────────────────────────────────────
    log.info("Fetching 'test-results' artifact...")
    artifacts = client.list_artifacts(run_id)
    results_artifact = next((a for a in artifacts if a["name"] == "test-results"), None)

    if not results_artifact:
        log.error("Artifact 'test-results' not found for run %s.", run_id)
        return 2

    artifact_id = results_artifact["id"]
    artifact_url = f"https://github.com/{repo}/actions/runs/{run_id}/artifacts/{artifact_id}"
    log.info("Artifact download URL: %s", artifact_url)
    print(f"ARTIFACT_URL={artifact_url}")

    log.info("Downloading artifact (ID=%s, size=%s bytes)...",
             artifact_id, results_artifact.get("size_in_bytes", "?"))
    zip_content = client.download_artifact(artifact_id)

    # Optionally extract the full artifact (test-summary.json, behave-results.json,
    # junit/*.xml) on disk so the caller can publish JUnit reports natively
    # (e.g. PublishTestResults@2 on Azure DevOps).
    if args.artifact_dir:
        out_dir = os.path.abspath(args.artifact_dir)
        os.makedirs(out_dir, exist_ok=True)
        with zipfile.ZipFile(BytesIO(zip_content)) as zf:
            zf.extractall(out_dir)
        log.info("Extracted artifact contents to %s", out_dir)
        print(f"ARTIFACT_DIR={out_dir}")

    summary = parse_summary_from_zip(zip_content)

    # Emit machine-readable key=value lines BEFORE the formatted summary so
    # callers (composite actions, ADO templates, shell scripts) can capture
    # them with a simple grep, regardless of locale or terminal width.
    print(f"OUTCOME={summary['outcome']}")
    print(f"PASSED={summary['passed']}")
    print(f"FAILED={summary['failed']}")
    print(f"SKIPPED={summary['skipped']}")
    print(f"TOTAL={summary['total']}")
    print(f"DURATION={summary['duration_seconds']}")

    print_summary(summary)

    return 0 if summary["outcome"] == "success" else 1


# ── CLI arguments ────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Test Automation Service — CLI Bridge",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--type", default="integration", choices=["integration", "e2e", "api"],
        help=(
            "Test category to run (default: integration). Maps to "
            "src/<type>/<suite> on the TAS workflow."
        )
    )
    parser.add_argument(
        "--suite", required=True, #choices=["wisp", "all", "tas_pass", "tas_fail"],
        help="Test suite to run"
    )
    parser.add_argument(
        "--env", required=True, choices=["dev", "uat"],
        help="Target environment"
    )
    parser.add_argument(
        "--caller-id", required=True,
        help="Identifier of the calling system (e.g. repo name or team)"
    )
    parser.add_argument(
        "--correlation-id", default="",
        help="Custom correlation ID (auto-generated if omitted)"
    )
    parser.add_argument(
        "--sync", action="store_true",
        help="Wait for test completion. Exit 0=pass, 1=fail, 2=orchestration error"
    )
    parser.add_argument(
        "--repo", default=DEFAULT_REPO,
        help=f"GitHub repo in owner/repo format (default: {DEFAULT_REPO})"
    )
    parser.add_argument(
        "--workflow", default=DEFAULT_WORKFLOW,
        help=f"Workflow filename (default: {DEFAULT_WORKFLOW})"
    )
    parser.add_argument(
        "--ref", default=DEFAULT_REF,
        help=f"Git branch or ref to run the workflow on (default: {DEFAULT_REF})"
    )
    parser.add_argument(
        "--artifact-dir", default="",
        help=(
            "Sync mode only: directory where the 'test-results' artifact is "
            "extracted (test-summary.json, behave-results.json, junit/*.xml). "
            "Useful to feed PublishTestResults@2 on Azure DevOps or "
            "actions/upload-artifact on GitHub Actions. Skipped when empty."
        )
    )
    return parser


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()
    sys.exit(run(args))
