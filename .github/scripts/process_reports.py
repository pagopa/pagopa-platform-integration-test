import os
import json
import shutil
from pathlib import Path
from datetime import datetime
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
            return {
                "passed": statistic.get("passed", 0),
                "failed": statistic.get("failed", 0),
                "skipped": statistic.get("skipped", 0),
            }
    except Exception as e:
        print(f"[ERROR] While reading {summary_path}: {e}")
        return {}

def cleanup_old_reports(base_path):
    dirs = sorted(
        [d for d in base_path.iterdir() if d.is_dir() and d.name != "last-history"],
        key=lambda d: d.name,
        reverse=True,
    )
    for old_dir in dirs[30:]:
        print(f"[INFO] Deleting old folder: {old_dir}")
        shutil.rmtree(old_dir)

def generate_index_page(base_path):
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template(str(TEMPLATE_PATH))

    reports = []
    for dir in sorted(base_path.iterdir(), reverse=True):
        if not dir.is_dir() or dir.name in ("last-history", "index.html"):
            continue
        stats_path = dir / "stats.json"
        stats = extract_stats(stats_path)
        reports.append({
            "name": dir.name,
            "passed": stats.get("passed", 0),
            "failed": stats.get("failed", 0),
            "link": f"./{dir.name}/index.html"
        })

    output = template.render(reports=reports)
    index_path = base_path / "index.html"
    index_path.write_text(output)
    print(f"[INFO] Wrote index page to {index_path}")

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

    for folder in [dest_dir, last_history_dir]:
        summary_path = folder / "widgets/summary.json"
        stats = extract_stats(summary_path)
        with open(folder / "stats.json", "w") as f:
            json.dump(stats, f)

    cleanup_old_reports(PUBLIC_DIR / f"{app}-tests")
    generate_index_page(PUBLIC_DIR / f"{app}-tests")

if __name__ == "__main__":
    if not SKIP_ARTIFACTS:
        for app in APPS:
            process_app(app)
    else:
        print("[INFO] Skipping artifact processing (skipArtifacts=true)")
