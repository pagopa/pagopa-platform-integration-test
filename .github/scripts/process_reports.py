import os
import json
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

APPS = ["wisp", "fdr"]
ARTIFACTS_DIR = Path("artifacts")
PUBLIC_DIR = Path("public")
TEMPLATE_PATH = Path("templates/history-index-template.html")
TIMESTAMP = os.getenv("TIMESTAMP")
SKIP_ARTIFACTS = os.getenv("SKIP_ARTIFACTS", "false").lower() == "true"

def extract_stats(summary_path):
    try:
        with open(summary_path) as f:
            data = json.load(f)
            statistic = data.get("statistic", {})
            print(f"[DEBUG] Stats from {summary_path}: {statistic}")  # DEBUG
            return {
                "passed": statistic.get("passed", 0),
                "failed": statistic.get("failed", 0),
                "skipped": statistic.get("skipped", 0),
            }
    except Exception as e:
        print(f"[ERROR] While reading {summary_path}: {e}")
        return {}

def generate_index_page(base_path):
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template(str(TEMPLATE_PATH))

    reports = []
    for dir in sorted(base_path.iterdir(), reverse=True):
        if not dir.is_dir() or dir.name in ("last-history", "index.html"):
            continue
        stats_path = dir / "stats.json"
        stats = extract_stats(stats_path)
        report = {
            "name": dir.name,
            "passed": stats.get("passed", 0),
            "failed": stats.get("failed", 0),
            "link": f"./{dir.name}/index.html"
        }
        print(f"[DEBUG] Adding report entry: {report}")  # DEBUG
        reports.append(report)

    output = template.render(reports=reports)
    index_path = base_path / "index.html"
    index_path.write_text(output)
    print(f"[INFO] Wrote index page to {index_path}")

def cleanup_old_reports(base_path):
    dirs = sorted(
        [d for d in base_path.iterdir() if d.is_dir() and d.name not in ("last-history", "index.html")],
        key=lambda d: d.name,
        reverse=True,
    )
    for old_dir in dirs[30:]:
        print(f"[INFO] Deleting old folder: {old_dir}")
        shutil.rmtree(old_dir)

def process_app(app):
    artifact_folder = ARTIFACTS_DIR / f"allure-report-{app}"
    if not artifact_folder.exists():
        print(f"[WARN] No artifact found for {app}, skipping.")
        return

    dest_dir = PUBLIC_DIR / f"{app}-tests" / TIMESTAMP
    last_history_dir = PUBLIC_DIR / f"{app}-tests" / "last-history"
    dest_dir.mkdir(parents=True, exist_ok=True)
    shutil.copytree(artifact_folder, dest_dir, dirs_exist_ok=True)

    if last_history_dir.exists():
        shutil.rmtree(last_history_dir)
    shutil.copytree(dest_dir, last_history_dir)

    # Write stats.json for the current run and last-history
    for folder in [dest_dir, last_history_dir]:
        summary_path = folder / "widgets/summary.json"
        stats_path = folder / "stats.json"
        stats = extract_stats(summary_path)
        if stats:
            with open(stats_path, "w") as f:
                json.dump(stats, f)
            print(f"[INFO] Created {stats_path} with stats: {stats}")
        else:
            print(f"[WARN] Skipped writing empty stats to {stats_path}")

    # 🔁 Regenerates stats.json only if summary.json exists and is valid
    base_path = PUBLIC_DIR / f"{app}-tests"
    for report_dir in sorted(base_path.iterdir()):
        if report_dir.is_dir() and report_dir.name not in ("last-history", "index.html"):
            summary_path = report_dir / "widgets/summary.json"
            stats_path = report_dir / "stats.json"
            if summary_path.exists():
                stats = extract_stats(summary_path)
                if stats:
                    with open(stats_path, "w") as f:
                        json.dump(stats, f)
                    print(f"[INFO] Updated {stats_path} with stats: {stats}")
                else:
                    print(f"[WARN] Skipped writing empty stats to {stats_path}")

    cleanup_old_reports(base_path)
    generate_index_page(base_path)

if not SKIP_ARTIFACTS:
    for app in APPS:
        process_app(app)
else:
    print("[INFO] Skipping artifact processing (skipArtifacts=true)")
