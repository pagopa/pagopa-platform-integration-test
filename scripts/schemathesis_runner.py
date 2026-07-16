"""Dynamic Schemathesis test runner for OpenAPI files.

Discovers OpenAPI specs from a local directory, resolves the per-spec API key
from the project secret store, and delegates execution to the Schemathesis CLI.
No test code needs to be written per endpoint: Schemathesis generates test cases
automatically from the spec and validates every response against its declared schema.

Usage
-----
    # Run against all JSON files found in tmp_fetched/
    python scripts/schemathesis_runner.py

    # Run only specific specs (file stems, without .json extension)
    python scripts/schemathesis_runner.py fdr_organization fdr_psp

    # Override the directory that contains the OpenAPI files
    python scripts/schemathesis_runner.py --openapi-dir path/to/dir fdr_organization

The file stem of each OpenAPI spec must match a key in the resolved secrets
(e.g. the file ``tmp_fetched/fdr_organization.json`` requires a secret entry
named ``fdr_organization``).
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from src.conf.configuration import secrets

API_KEY_HEADER: str = "Ocp-Apim-Subscription-Key"
DEFAULT_OPENAPI_DIR: Path = Path("tmp_fetched")
DEFAULT_REPORT_BASE_DIR: Path = Path("schemathesis-test-reports")


def build_arg_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser for the runner."""
    parser = argparse.ArgumentParser(
        description="Run Schemathesis against one or more OpenAPI specs with automatic secret resolution."
    )
    parser.add_argument(
        "files",
        nargs="*",
        metavar="FILE_STEM",
        help=(
            "OpenAPI file stems to test, without the .json extension "
            "(e.g. fdr_organization fdr_psp). "
            "If omitted, all .json files in --openapi-dir are tested."
        ),
    )
    parser.add_argument(
        "--openapi-dir",
        default=DEFAULT_OPENAPI_DIR,
        type=Path,
        metavar="DIR",
        help=f"Directory that contains the OpenAPI JSON files. Defaults to '{DEFAULT_OPENAPI_DIR}'.",
    )
    parser.add_argument(
        "--extra-checks",
        nargs="*",
        metavar="CHECK",
        default=[],
        help="Additional Schemathesis check names to pass alongside the default set.",
    )
    parser.add_argument(
        "--url",
        default=None,
        metavar="URL",
        help=(
            "Override the base URL for all requests. "
            "If omitted, the URL is read automatically from the servers field of the spec."
        ),
    )
    parser.add_argument(
        "--schemathesis-args",
        nargs=argparse.REMAINDER,
        default=[],
        help="Any extra arguments forwarded verbatim to 'schemathesis run'.",
    )
    parser.add_argument(
        "--report-base-dir",
        default=DEFAULT_REPORT_BASE_DIR,
        type=Path,
        metavar="DIR",
        help=(
            "Base directory where run report folders are created. "
            f"Defaults to '{DEFAULT_REPORT_BASE_DIR}'."
        ),
    )
   
    return parser


def build_report_directory(base_dir: Path) -> Path:
    """Create and return a unique report directory for the current execution.

    The resulting path is structured as ``<base>/<YYYY-MM-DD>/<run-name>``.
    When *run_name* is missing, a timestamp-based name is used.
    """
    day_folder = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("run %H-%M-%S")
    for openApi_file in Path("tmp_fetched").glob("*.json"):
            file_stem = openApi_file.stem
            if file_stem:
                name = fr"{file_stem} {time}"
            else:
                name = time
            target = base_dir / day_folder / name / os.getenv("TARGET_ENV", "N/A")
            if not target.exists():
                target.mkdir(parents=True, exist_ok=False)
            return target


def extract_server_url(openapi_file: Path) -> str | None:
    """Read the first server URL from the servers field of an OpenAPI spec file."""
    with openapi_file.open(encoding="utf-8") as fh:
        data = json.load(fh)
    servers = data.get("servers", [])
    return servers[0].get("url") if servers else None


def resolve_openapi_files(openapi_dir: Path, file_stems: list[str]) -> list[Path]:
    """Return the list of OpenAPI file paths to test.

    When *file_stems* is non-empty, returns one path per stem under *openapi_dir*.
    When empty, returns every ``*.json`` file found in *openapi_dir*.
    """
    if file_stems:
        return [openapi_dir / f"{stem}.json" for stem in file_stems]
    return sorted(openapi_dir.glob("*.json"))


def build_schemathesis_command(
    openapi_file: Path,
    api_key: str,
    server_url: str,
    report_directory: Path,
    extra_args: list[str],
) -> list[str]:
    """Assemble the 'schemathesis run' command for a single OpenAPI file."""
    command: list[str] = [
        "schemathesis",
        "run",
        str(openapi_file),
        "--url",
        server_url,
        "--report-dir",
        str(report_directory),
        "--header",
        f"{API_KEY_HEADER}: {api_key}",
    ]
    command += extra_args
    return command


def run_spec(
    openapi_file: Path,
    api_key: str,
    report_directory: Path,
    extra_args: list[str],
    url_override: str | None = None,
) -> int:
    """Execute Schemathesis against a single OpenAPI file and return the exit code."""
    server_url = url_override or extract_server_url(openapi_file)
    if not server_url:
        print(f"[SKIP] No server URL found in '{openapi_file.name}'. Pass --url to override.")
        return 1
    command = build_schemathesis_command(
        openapi_file, api_key, server_url, report_directory, extra_args
    )
    print(f"\n{'=' * 60}")
    print(f"Testing: {openapi_file.name}")
    print(f"{'=' * 60}\n")
    result = subprocess.run(command)
    return result.returncode


def main() -> int:
    """Entry point: resolve files, inject secrets, and run Schemathesis for each spec."""
    parser = build_arg_parser()
    args = parser.parse_args()

    openapi_files = resolve_openapi_files(args.openapi_dir, args.files)
    if not openapi_files:
        print(f"No OpenAPI files found in '{args.openapi_dir}'. Nothing to test.")
        return 0

    report_directory = build_report_directory(args.report_base_dir)
    print(f"Report directory for this run: {report_directory}")

    exit_codes: list[int] = []

    for openapi_file in openapi_files:
        file_stem = openapi_file.stem
        api_key = secrets.get(file_stem)
        if api_key is None:
            print(
                f"[SKIP] No secret entry found for '{file_stem}'. "
                "Add it to your config JSON and re-run."
            )
            continue

        code = run_spec(
            openapi_file,
            api_key,
            report_directory,
            args.schemathesis_args,
            args.url,
        )
        exit_codes.append(code)

    failures = sum(1 for c in exit_codes if c != 0)
    print(f"\nCompleted {len(exit_codes)} spec(s). Failures: {failures}.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
