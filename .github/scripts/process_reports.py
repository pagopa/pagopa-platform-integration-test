import json
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
import re
from datetime import datetime, timedelta, timezone
import shutil
from pathlib import Path

OPENAPI_TEST_DIR = 'openapi-fdr-tests'
PROCESSED_REPORTS_DIR = 'tmp_processed_reports'
OPENAPI_FDR_TESTS = 'openapi-fdr'

# Headings of the aggregate NRT analysis: one `## Suite: <id>` section per suite, optionally
# followed by a `## Cross-suite ...` section that belongs to no single suite.
_SUITE_HEADING_RE = re.compile(r"^##[ \t]+Suite:[ \t]*(?P<id>[\w.-]+).*$", re.IGNORECASE)
_CROSS_SUITE_HEADING_RE = re.compile(r"^##[ \t]+Cross-suite\b", re.IGNORECASE)
_FENCE_RE = re.compile(r"^ {0,3}(?P<marker>`{3,}|~{3,})(?P<info>.*)$")
_FULL_ANALYSIS_PAGE = "full.html"


def update_tas_main_index(root_path):
    """Render suite buttons for suite indexes present under the TAS root."""
    root_path = Path(root_path)
    suites = []
    for suite_dir in root_path.iterdir():
        if not suite_dir.is_dir() or parse_tas_folder_timestamp(suite_dir.name):
            continue
        if not (suite_dir / "index.html").is_file():
            continue
        suites.append({
            "name": suite_dir.name,
            "link": f"./{suite_dir.name}/index.html",
        })
    suites.sort(key=lambda suite: suite["name"].casefold())

    environment = Environment(
        loader=FileSystemLoader(".github/templates"),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = environment.get_template("tas-main-index-template.html")
    (root_path / "index.html").write_text(
        template.render(suites=suites), encoding="utf-8"
    )


def extract_stats(artifact_app_dir):
    try:
        print(f"[INFO][extract_stats] artifact_app_dir {artifact_app_dir}")
        artifact_summary_file = os.path.join(artifact_app_dir, "widgets", "summary.json")
        print(f"[INFO][extract_stats] artifact_summary_file {artifact_summary_file}")
        with open(artifact_summary_file) as f:

            # load summary.json file
            print(f"[INFO][extract_stats] loading {artifact_summary_file} file")
            data = json.load(f)
            print(f"[INFO][extract_stats] {artifact_summary_file} file loaded")

            # extract statistic and time sections from summary
            statistic_raw = data.get("statistic", {})
            time_raw = data.get("time", {})
            if time_raw is None:
                raise ValueError(f"[ERROR][extract_stats] 'time' section is missing in {artifact_summary_file} for {artifact_app_dir}. This means that something went wrong during the last test run.")
            statistic = statistic_raw[0] if isinstance(statistic_raw, list) else statistic_raw
            time = time_raw[0] if isinstance(time_raw, list) else time_raw
            print(f"[INFO][extract_stats] extracted statistic section {statistic}")
            print(f"[INFO][extract_stats] extracted time section {time}")
            
            # calculate duration in milliseconds
            start = time.get("start", 0)
            millis = (time.get("stop", 0)) -  start
            duration = str(timedelta(milliseconds=millis)).split(".")[0]  # format as HH:MM:SS
            print(f"[INFO][extract_stats] formatted duration {duration}")
          
            # compute start date
            start_datetime = datetime.fromtimestamp(start / 1000)
            formatted_start = start_datetime.strftime("%Y-%m-%d_%H:%M:%S")
            print(f"[INFO][extract_stats] formatted start date {formatted_start}")

            # build stats object
            stats = {
                "passed": statistic.get("passed", 0),
                "failed": statistic.get("failed", 0),
                "skipped": statistic.get("skipped", 0),
                "duration": str(duration),
                "start": formatted_start,
            }

            # write stats.json file
            stats_json = os.path.join(artifact_app_dir, "stats.json")
            with open(stats_json, "w") as f:
                json.dump(stats, f)
                print(f"[INFO][extract_stats] written {stats_json}")

            return stats
    except Exception as e:
        print(f"[ERROR][extract_stats] While generating stat.json file: {e}")
        return {}

def extract_stats_from_stats_file(stats_json_path):
    if os.path.exists(stats_json_path):
        with open(stats_json_path) as f:
            stats_data = json.load(f)
            print(f"[INFO][extract_stats_from_stats_file] loaded stats.json {stats_data}")
            return {
                'passed': stats_data.get('passed', 0),
                'failed': stats_data.get('failed', 0),
                'skipped': stats_data.get('skipped', 0)
            }
    else:
        print(f"[INFO][extract_stats_from_stats_file] stats.json {stats_json_path} not found")
        return {'passed': 0, 'failed': 0, 'skipped': 0}

def build_index_page(root_dir):
    """Build index page for reports (handles both allure and schemathesis reports).
    
    For allure (wisp, openapi): extracts stats from stats.json if available
    For schemathesis: uses default stats (0 passed/failed)
    Excludes: index.html, last-history, and last-history-* folders
    """
    reports = []
    print(f"[INFO][build_index_page] processing root_dir {root_dir}")
    
    for name in os.listdir(root_dir):
        report_dir = os.path.join(root_dir, name)
        
        # Skip index.html and last-history folders (including env-specific: last-history-dev, etc)
        if name == "index.html" or name == "last-history" or name.startswith("last-history-"):
            print(f"[INFO][build_index_page] skipping excluded folder: {name}")
            continue
        
        if not os.path.isdir(report_dir):
            print(f"[INFO][build_index_page] skipping non-directory: {name}")
            continue
        
        # Try to get stats from stats.json (allure reports)
        stats_json = os.path.join(report_dir, "stats.json")
        if os.path.exists(stats_json):
            stats = extract_stats_from_stats_file(stats_json)
            analysis_index = os.path.join(report_dir, "analysis", "index.html")
            has_analysis = os.path.exists(analysis_index)
            report_entry = {
                "name": name,
                "passed": stats["passed"],
                "failed": stats["failed"],
                "link": f"./{name}/index.html",
                "has_analysis": has_analysis,
                "analysis_link": f"./{name}/analysis/index.html" if has_analysis else None,
                "sort_key": name
            }
            print(f"[INFO][build_index_page] Adding report entry: {report_entry}")
            reports.append(report_entry)
        else:
            # Default stats for schemathesis or other reports without stats.json
            stats = {'passed': 0, 'failed': 0, 'skipped': 0}
            report_entry = {
                "name": name,
                "passed": stats["passed"],
                "failed": stats["failed"],
                "link": f"./{name}/index.html",
                "has_analysis": False,
                "analysis_link": None,
                "sort_key": name
            }
            print(f"[INFO][build_index_page] Adding report entry: {report_entry}")
            reports.append(report_entry)

    # Order by timestamp desc
    print(f"[INFO][build_index_page] sorting reports by date descending")
    reports.sort(key=lambda r: r["sort_key"], reverse=True)

    # load index template and render template
    print(f"[INFO][build_index_page] applying history-index-template.html template")
    env = Environment(
        loader=FileSystemLoader(".github/templates"),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template("history-index-template.html")
    output_path = os.path.join(root_dir, "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        print(f"[INFO][build_index_page] Writing index page to {output_path} ...")
        f.write(template.render(reports=reports))
    print(f"[INFO][build_index_page] written index page to {output_path}")

# TAS report folder names: ISO UTC (current, same as NRT) and dd-mm-YYYY (legacy).
TAS_FOLDER_TIMESTAMP_FORMATS = ("%Y-%m-%d_%H:%M:%S", "%d-%m-%Y_%H:%M:%S")
TAS_SUITE_NAME_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")


def parse_tas_folder_timestamp(folder_name):
    """Return the datetime encoded in a TAS report folder name, or None."""
    for timestamp_format in TAS_FOLDER_TIMESTAMP_FORMATS:
        try:
            return datetime.strptime(folder_name, timestamp_format)
        except ValueError:
            continue
    return None


def _validate_tas_suite_name(test_suite: object) -> str:
    """Return a safe TAS suite path component or raise ValueError."""
    if not isinstance(test_suite, str) or TAS_SUITE_NAME_PATTERN.fullmatch(test_suite) is None:
        raise ValueError("Invalid TAS test_suite; expected a safe path component")
    return test_suite


def clean_tas_history(root_dir: str | Path, test_suite: object) -> None:
    """Remove expired timestamped runs from a validated suite directory, if present."""
    suite_path = Path(root_dir) / _validate_tas_suite_name(test_suite)
    if suite_path.is_symlink() or not suite_path.is_dir():
        return
    cutoff = datetime.now(timezone.utc) - timedelta(days=30)
    for report_dir in suite_path.iterdir():
        if report_dir.is_symlink() or not report_dir.is_dir():
            continue
        timestamp = parse_tas_folder_timestamp(report_dir.name)
        if timestamp is not None and timestamp.replace(tzinfo=timezone.utc) < cutoff:
            shutil.rmtree(report_dir)


def build_tas_index_page(root_dir, test_suite):
    """Build the TAS history index from complete timestamped reports."""
    test_suite = _validate_tas_suite_name(test_suite)

    root_path = Path(root_dir) / test_suite
    root_path.mkdir(parents=True, exist_ok=True)

    reports = []
    for report_dir in root_path.iterdir():
        if not report_dir.is_dir():
            continue
        timestamp = parse_tas_folder_timestamp(report_dir.name)
        if timestamp is None:
            continue
        report_index = report_dir / "index.html"
        if not report_index.is_file() or report_index.stat().st_size == 0:
            continue
        analysis_index = report_dir / "analysis" / "index.html"
        has_analysis = analysis_index.is_file()
        passed = "N/D"
        failed = "N/D"
        summary_path = report_dir / "widgets" / "summary.json"
        try:
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            summary = {}
        statistic = summary.get("statistic", {}) if isinstance(summary, dict) else {}
        if isinstance(statistic, list):
            statistic = statistic[0] if statistic else {}
        if isinstance(statistic, dict):
            passed_value = statistic.get("passed")
            failed_value = statistic.get("failed", 0)
            broken_value = statistic.get("broken", 0)
            if isinstance(passed_value, int) and not isinstance(passed_value, bool):
                passed = passed_value
            if (
                isinstance(failed_value, int)
                and not isinstance(failed_value, bool)
                and isinstance(broken_value, int)
                and not isinstance(broken_value, bool)
                and ("failed" in statistic or "broken" in statistic)
            ):
                failed = failed_value + broken_value
        reports.append({
            "timestamp": timestamp.strftime("%d-%m-%Y %H:%M:%S"),
            "passed": passed,
            "failed": failed,
            "link": f"./{report_dir.name}/index.html",
            "has_analysis": has_analysis,
            "analysis_link": (
                f"./{report_dir.name}/analysis/index.html" if has_analysis else None
            ),
            "sort_key": timestamp,
        })

    reports.sort(key=lambda report: report["sort_key"], reverse=True)
    for report in reports:
        del report["sort_key"]

    environment = Environment(
        loader=FileSystemLoader(".github/templates"),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = environment.get_template("tas-history-index-template.html")
    index_path = root_path / "index.html"
    index_path.write_text(
        template.render(reports=reports, suite_name=test_suite), encoding="utf-8"
    )


def _suite_key(suite_id: str) -> str:
    """Normalise a suite id for comparison, so `FDR-3` written by the model matches `fdr3`."""
    return re.sub(r"[^a-z0-9]", "", suite_id.lower())


def _fenced_line_indexes(lines: list[str]) -> set[int]:
    """Return the indexes of the lines that belong to a closed fenced code block, fences included.

    A fence is closed only by a bare fence of the same character and at least the same length. A fence
    that is never closed does not hide the text after it, because a stray fence is likelier than a
    code block running to the end of the analysis.
    """
    fenced: set[int] = set()
    opening: tuple[int, str] | None = None
    for index, line in enumerate(lines):
        match = _FENCE_RE.match(line)
        if match is None:
            continue
        marker = match.group("marker")
        if opening is None:
            opening = (index, marker)
        elif (
            marker[0] == opening[1][0]
            and len(marker) >= len(opening[1])
            and not match.group("info").strip()
        ):
            fenced.update(range(opening[0], index + 1))
            opening = None
    return fenced


def split_suite_sections(markdown: str) -> dict[str, str]:
    """Split an aggregate analysis into its `## Suite: <id>` sections, keyed by normalised suite id.

    A section runs from its heading to the next suite heading or `## Cross-suite` heading, so text
    that concerns several suites never leaks into the last suite. Headings inside fenced code blocks
    are ignored and text before the first suite heading is dropped. A suite heading repeated by the
    model is merged into the first section of that suite. Keys are built by `_suite_key`.
    """
    lines = markdown.splitlines()
    fenced = _fenced_line_indexes(lines)
    sections: dict[str, list[str]] = {}
    current: list[str] | None = None
    for index, line in enumerate(lines):
        if index not in fenced:
            suite = _SUITE_HEADING_RE.match(line)
            if suite:
                current = sections.setdefault(_suite_key(suite.group("id")), [])
            elif _CROSS_SUITE_HEADING_RE.match(line):
                current = None
        if current is not None:
            current.append(line)
    return {suite_key: "\n".join(body).strip() for suite_key, body in sections.items()}


def deploy_ai_analysis(
    artifact_dir,
    run_dir,
    last_history_dir,
    analysis_artifact_name,
    suite_label,
    timestamp,
    history_url="../../index.html",
    suite_id=None,
    scoped_suite_label=None,
):
    """Render the AI analysis HTML page inside run_dir and last_history_dir.

    Reads the analysis markdown from the named artifact directory.
    Silently skips when the artifact is missing (e.g., first run before the change).

    With `suite_id` the analysis is an aggregate over several suites: `analysis/index.html` then
    shows only that suite's section (titled `scoped_suite_label`, default `suite_label`) and links
    to `analysis/full.html`, which holds the whole analysis. When the analysis has no section for
    the suite, `index.html` falls back to the whole analysis, no `full.html` is written (a stale one
    is removed) and a `::warning::` is emitted. The suite id is matched ignoring case and
    punctuation. `analysis/analysis.md` always keeps the whole markdown.
    """
    analysis_artifact_dir = Path(artifact_dir) / analysis_artifact_name
    analysis_md = analysis_artifact_dir / "analysis.md"
    if not analysis_md.exists():
        print(f"[INFO][deploy_ai_analysis] no analysis artifact at {analysis_md}, skipping")
        return

    analysis_text = analysis_md.read_text(encoding="utf-8").strip()
    if not analysis_text:
        print(f"[INFO][deploy_ai_analysis] analysis file {analysis_md} is empty, skipping")
        return

    response_json = analysis_artifact_dir / "response.json"
    model = "Gemini"
    if response_json.exists():
        try:
            model = json.loads(response_json.read_text(encoding="utf-8")).get(
                "modelVersion", model
            )
        except (json.JSONDecodeError, OSError) as exc:
            print(f"[INFO][deploy_ai_analysis] cannot read model version: {exc}")

    env = Environment(
        loader=FileSystemLoader(".github/templates"),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template("analysis-template.html")

    def render(label, markdown, full_analysis_url=None):
        """Render the analysis template for one page."""
        return template.render(
            suite_label=label.upper(),
            timestamp=timestamp or "unknown",
            model=model,
            analysis_markdown=markdown,
            history_url=history_url,
            full_analysis_url=full_analysis_url,
        )

    rendered = render(suite_label, analysis_text)
    full_rendered = None
    if suite_id:
        suite_section = split_suite_sections(analysis_text).get(_suite_key(suite_id))
        if suite_section:
            full_rendered = rendered
            rendered = render(scoped_suite_label or suite_label, suite_section, _FULL_ANALYSIS_PAGE)
        else:
            print(
                f"::warning::The AI analysis has no '## Suite: {suite_id}' section; "
                "publishing the whole analysis for this suite"
            )

    report_dirs = [Path(run_dir)]
    if last_history_dir is not None:
        report_dirs.append(Path(last_history_dir))

    for base in report_dirs:
        analysis_dir = base / "analysis"
        analysis_dir.mkdir(parents=True, exist_ok=True)
        (analysis_dir / "index.html").write_text(rendered, encoding="utf-8")
        if full_rendered is not None:
            (analysis_dir / _FULL_ANALYSIS_PAGE).write_text(full_rendered, encoding="utf-8")
        elif suite_id:
            # a page left by a previous run must not outlive the link that pointed to it
            (analysis_dir / _FULL_ANALYSIS_PAGE).unlink(missing_ok=True)
        # keep the raw markdown next to the page for auditability
        (analysis_dir / "analysis.md").write_text(analysis_text, encoding="utf-8")
        print(f"[INFO][deploy_ai_analysis] wrote analysis page in {analysis_dir}")


def clean_history(root_dir):
    for dir in os.listdir(root_dir):
        dir_date = re.search(r"\d{4}-\d{2}-\d{2}", str(dir))
        now = datetime.now().date()
        if dir_date:
            dir_date = datetime.strptime(dir_date.group(), "%Y-%m-%d").date()
            # remove folders older than 30 days
            if dir_date < now - timedelta(days=30):
                dir_path = os.path.join(root_dir, dir)
                if os.path.isdir(dir_path):
                    print(f"[INFO][clean_history] deleting {dir_path}")
                    shutil.rmtree(dir_path)


def main():
    allure_apps = ["wisp", "checkout"]
    artifact_dir = os.path.join("artifacts") # /artifacts
    print(f"[INFO][main] artifact_dir {artifact_dir}")
    
    # Process Allure reports (wisp, openapi)
    artifact_dirs = sorted(os.listdir(artifact_dir))
    for dir in artifact_dirs:
        processed = False
        for app in allure_apps:
            root_dir = f"public/{app}-tests"
            print(f"[INFO][main] processing Allure directory {root_dir}")

            
            if not dir.startswith(f"allure-report-{app}"):
                continue
            else:
                artifact_app_dir = os.path.join(artifact_dir, dir) # /artifacts/allure-report-<app>
                print(f"[INFO][main] artifact_app_dir {artifact_app_dir}")
                
                # retrieve stats
                stats = extract_stats(artifact_app_dir)
                # copy content from /artifacts/allure-report-<app> inside the new directory run_dir
                source_dir = Path(artifact_app_dir)
                run_dir = os.path.join(root_dir + "/" + stats.get("start")) 
                destination_dir = Path(run_dir)
                print(f"[INFO][main] destination_dir {destination_dir}")
                # copy everything from source to run dir and last-history dir
                last_history_dir = os.path.join(root_dir, "last-history") 
                tmp_reports_dir = Path(f"public/{PROCESSED_REPORTS_DIR}")
                print(f"[INFO][main] last_history_dir {last_history_dir}")
                last_history_dir = Path(last_history_dir)
                print(f"[INFO][main] last_history_dir {last_history_dir}")
                if last_history_dir.exists(): # delete dir if already exists
                    print(f"[INFO][main] deleting {last_history_dir} content")
                    shutil.rmtree(last_history_dir)
                tmp_reports_dir.mkdir(parents=True, exist_ok=True)
                print(f"[INFO][main] copy everything from {source_dir} to {destination_dir}")
                shutil.copytree(source_dir, destination_dir)
                print(f"[INFO][main] copy everything from {source_dir} to {last_history_dir}")
                shutil.copytree(source_dir, last_history_dir)

                # remove test report folders older than 30 days
                clean_history(root_dir)
                
                analysis_artifact_name = (
                    f"ai-analysis-{app}"
                )
                deploy_ai_analysis(
                    artifact_dir,
                    run_dir,
                    last_history_dir,
                    analysis_artifact_name,
                    app,
                    stats.get("start"),
                )
                if app == "openapi":
                    app = OPENAPI_FDR_TESTS
                processed_run_dir = Path(f'public/{PROCESSED_REPORTS_DIR}/{app}')
                if processed_run_dir.exists():
                    print(f"[INFO][main] deleting {processed_run_dir} content")
                    shutil.rmtree(processed_run_dir)
                print(f"[INFO][main] copy everything from {source_dir} to {processed_run_dir}")
                shutil.copytree(source_dir, processed_run_dir)
                # build index page
                build_index_page(root_dir)
                processed = True
                break

        if not processed:
            print(f"[INFO][main] skipping non-Allure artifact directory: {dir}")

    

if __name__ == "__main__":
    main()