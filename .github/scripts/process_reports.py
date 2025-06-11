import json
import os
from jinja2 import Environment, FileSystemLoader
import re
from datetime import datetime

def extract_stats(summary_path):
    try:
        with open(summary_path) as f:
            data = json.load(f)
            statistic_raw = data.get("statistic", {})
            statistic = statistic_raw[0] if isinstance(statistic_raw, list) else statistic_raw
            print(f"[DEBUG] Stats from {summary_path}: {statistic}")
            return {
                "passed": statistic.get("passed", 0),
                "failed": statistic.get("failed", 0),
                "skipped": statistic.get("skipped", 0),
            }
    except Exception as e:
        print(f"[ERROR] While reading {summary_path}: {e}")
        return {}

def extract_stats_from_stats_file(stats_json_path):
    if os.path.exists(stats_json_path):
        with open(stats_json_path) as f:
            stats_data = json.load(f)
        return {
            'passed': stats_data.get('passed', 0),
            'failed': stats_data.get('failed', 0),
            'skipped': stats_data.get('skipped', 0)
        }
    else:
        return {'passed': 0, 'failed': 0, 'skipped': 0}

def process_report_dir(report_dir):
    widgets_summary = os.path.join(report_dir, "widgets", "summary.json")
    stats_json = os.path.join(report_dir, "stats.json")

    if os.path.exists(widgets_summary):
        stats = extract_stats(widgets_summary)
        with open(stats_json, "w") as f:
            json.dump(stats, f)
        print(f"[INFO] {'Created' if not os.path.exists(stats_json) else 'Updated'} {stats_json} with stats: {stats}")
        return True
    return False

def format_display_name(name):
    # From "2025-04-27-18h5636" to "2025-04-27_18:56:36"
    match = re.match(r"(\d{4}-\d{2}-\d{2})-(\d{2})h(\d{2})(\d{2})", name)
    if match:
        date, hour, minute, second = match.groups()
        return f"{date}_{hour}:{minute}:{second}"
    return name  # fallback se non matcha

def build_index_page(root_dir):
    reports = []
    for name in os.listdir(root_dir):
        report_dir = os.path.join(root_dir, name)
        stats_json = os.path.join(report_dir, "stats.json")
        if os.path.isdir(report_dir) and os.path.exists(stats_json) and name not in ("last-history", "index.html"):
            stats = extract_stats_from_stats_file(stats_json)
            report_entry = {
                "name": format_display_name(name),
                "passed": stats["passed"],
                "failed": stats["failed"],
                "link": f"./{name}/index.html",
                "sort_key": name
            }
            print(f"[DEBUG] Adding report entry: {report_entry}")
            reports.append(report_entry)

    # Order by timestamp desc
    reports.sort(key=lambda r: r["sort_key"], reverse=True)

    env = Environment(loader=FileSystemLoader(".github/templates"))
    template = env.get_template("history-index-template.html")

    output_path = os.path.join(root_dir, "index.html")
    with open(output_path, "w") as f:
        print(f"[INFO] Writing index page to {output_path} ...")
        f.write(template.render(reports=reports))
    print(f"[INFO] Wrote index page to {output_path}")

def main():
    apps = ["wisp", "fdr"]
    artifact_dir = os.path.join("artifact")
    if os.path.isdir(artifact_dir):
        print(f"[INFO] artifact dir {artifact_dir} exists!")
    else:
        print(f"[INFO] artifact dir {artifact_dir} does not exist...")
    for app in apps:
        root_dir = f"public/{app}-tests"
        for name in os.listdir(root_dir):
            report_dir = os.path.join(root_dir, name)
            if os.path.isdir(report_dir):
                print(f"[INFO] is valid directory  {report_dir} ")
                summary_path = os.path.join(report_dir, "widgets", "summary.json")
                if os.path.exists(summary_path):
                    stats = extract_stats(summary_path)
                    stats_json = os.path.join(report_dir, "stats.json")
                    with open(stats_json, "w") as f:
                        json.dump(stats, f)
                    print(f"[INFO] {'Created' if not os.path.exists(stats_json) else 'Updated'} {stats_json} with stats: {stats}")
        build_index_page(root_dir)

if __name__ == "__main__":
    main()
