
import sys
import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path

import scripts.fetch_github_files as fetch_github_files
import scripts.schemathesis_runner as schemathesis_runner

OPENAPI_FOLDER = "tmp_fetched"
SCHEMATHESIS_RUNS_BASE_DIR = "schemathesis- test-reports"
SCHEMATHESIS_RUN_RETENTION_DAYS = 30


def cleanup_old_schemathesis_runs(base_dir: str, retention_days: int) -> None:
    """Delete Schemathesis run directories older than the configured retention period."""
    runs_root = Path(base_dir)
    if not runs_root.exists():
        print(f"Schemathesis report folder not found: {runs_root}")
        return

    cutoff = datetime.now() - timedelta(days=retention_days)
    deleted_run_dirs = 0
    deleted_day_dirs = 0

    for day_dir in sorted(runs_root.iterdir()):
        if not day_dir.is_dir():
            continue

        try:
            day_is_expired = datetime.strptime(day_dir.name, "%Y-%m-%d") < cutoff
        except ValueError:
            day_is_expired = False

        for run_dir in list(day_dir.iterdir()):
            if not run_dir.is_dir() or " run " not in run_dir.name:
                continue

            if day_is_expired or datetime.fromtimestamp(run_dir.stat().st_mtime) < cutoff:
                shutil.rmtree(run_dir)
                deleted_run_dirs += 1

        if day_dir.exists() and not any(day_dir.iterdir()):
            day_dir.rmdir()
            deleted_day_dirs += 1

    print(
        "Removed "
        f"{deleted_run_dirs} Schemathesis run folder(s) and "
        f"{deleted_day_dirs} empty day folder(s) older than {retention_days} days."
    )

def main():
    """Fetch OpenAPI files, execute Schemathesis tests, and clean generated artifacts."""
    # Fetch the OpenAPI files from GitHub
    fetch_github_files.main()
    print(f"Fetched OpenAPI files to {OPENAPI_FOLDER}")
    # Run the Schemathesis tests
    schemathesis_runner.main()

    # Remove the fetched OpenAPI files after testing
    if os.path.isdir(OPENAPI_FOLDER):
        shutil.rmtree(OPENAPI_FOLDER)
        print("Removed fetched OpenAPI folder")

    cleanup_old_schemathesis_runs(
        SCHEMATHESIS_RUNS_BASE_DIR,
        SCHEMATHESIS_RUN_RETENTION_DAYS,
    )



if __name__ == "__main__":
    main()