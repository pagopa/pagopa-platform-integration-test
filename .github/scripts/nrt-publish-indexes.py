"""Refresh the published NRT dashboard without changing suite artifacts."""

import json
import os
from pathlib import Path
import shutil
import time
from datetime import datetime, timezone

from jinja2 import Environment, FileSystemLoader, select_autoescape

from process_reports import build_index_page, deploy_ai_analysis, extract_stats


def publish_ai_analysis(matrix, target_env, run_number):
    """Attach the aggregate analysis only to reports from the current workflow run."""
    analysis_md = Path("artifacts/nrt-ai-analysis/analysis.md")
    if not analysis_md.is_file() or not analysis_md.read_text(encoding="utf-8").strip():
        raise ValueError(f"AI analysis succeeded but {analysis_md} is missing or empty")

    for suite in matrix["include"]:
        subfolder = suite["allure_subfolder"]
        summary_path = (
            Path("nrt-allure-history") / f"{subfolder}-{target_env}"
            / str(run_number) / "widgets" / "summary.json"
        )
        if not summary_path.is_file():
            print(f"::warning::No current Allure report for {suite['id']}; skipping AI publication")
            continue
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        time_data = summary["time"]
        if isinstance(time_data, list):
            time_data = time_data[0]
        timestamp = datetime.fromtimestamp(
            time_data["start"] / 1000, timezone.utc
        ).strftime("%Y-%m-%d_%H:%M:%S")
        root_dir = Path("public") / subfolder
        run_dir = root_dir / timestamp
        if not (run_dir / "widgets" / "summary.json").is_file():
            raise FileNotFoundError(f"Current Allure report was not published at {run_dir}")
        deploy_ai_analysis(
            artifact_dir="artifacts",
            run_dir=run_dir,
            last_history_dir=root_dir / "last-history",
            analysis_artifact_name="nrt-ai-analysis",
            suite_label=f"{suite['label']} - aggregate NRT analysis",
            timestamp=timestamp,
        )


def update_suite(root_dir):
    """Generate run statistics, refresh the latest report, and build its index."""
    reports = []
    for report_dir in sorted(root_dir.iterdir()):
        if not report_dir.is_dir() or report_dir.name.startswith("last-history"):
            continue
        summary_path = report_dir / "widgets" / "summary.json"
        if not summary_path.is_file():
            continue
        with summary_path.open(encoding="utf-8") as summary_file:
            summary = json.load(summary_file)
        time_data = summary["time"]
        if isinstance(time_data, list):
            time_data = time_data[0]
        start = time_data["start"]
        if not isinstance(start, (int, float)) or isinstance(start, bool) or start <= 0:
            raise ValueError(f"Invalid Allure start time in {summary_path}: {start!r}")
        stop = time_data["stop"]
        if not isinstance(stop, (int, float)) or isinstance(stop, bool) or stop < start:
            raise ValueError(f"Invalid Allure stop time in {summary_path}: {stop!r}")
        statistic = summary["statistic"]
        if isinstance(statistic, list):
            statistic = statistic[0]
        for key in ("passed", "failed", "skipped"):
            count = statistic[key]
            if not isinstance(count, int) or isinstance(count, bool) or count < 0:
                raise ValueError(f"Invalid Allure {key} count in {summary_path}: {count!r}")
        stats = extract_stats(str(report_dir))
        if not stats:
            raise RuntimeError(f"Failed to generate statistics for {report_dir}")
        reports.append((start, report_dir, stats))

    if not reports:
        print(f"::warning::No Allure reports found in {root_dir}")
        return None

    _, latest_report, stats = max(reports, key=lambda report: (report[0], report[1].name))
    latest_dir = root_dir / "last-history"
    if latest_dir.exists():
        shutil.rmtree(latest_dir)
    shutil.copytree(latest_report, latest_dir)
    build_index_page(str(root_dir))
    return stats


def main():
    """Build registry-driven suite indexes and the root GitHub Pages dashboard."""
    os.environ["TZ"] = "UTC"
    if hasattr(time, "tzset"):
        time.tzset()
    with Path(".github/nrt-suites.json").open(encoding="utf-8") as registry_file:
        registry = json.load(registry_file)
    if os.environ.get("AI_ANALYSIS_RESULT") == "success":
        publish_ai_analysis(
            json.loads(os.environ["SUITE_MATRIX"]),
            os.environ["TARGET_ENV"],
            os.environ["RUN_NUMBER"],
        )
    public_dir = Path("public")
    suites = []
    for suite in registry["suites"]:
        root_dir = public_dir / suite["allure_subfolder"]
        stats = update_suite(root_dir) if root_dir.is_dir() else None
        suites.append({**suite, "stats": stats})

    environment = Environment(
        loader=FileSystemLoader(".github/templates"),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = environment.get_template("nrt-dashboard-template.html")
    (public_dir / "index.html").write_text(
        template.render(
            suites=suites,
            updated_at=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        ),
        encoding="utf-8",
    )
    (public_dir / ".nojekyll").touch()


if __name__ == "__main__":
    main()
