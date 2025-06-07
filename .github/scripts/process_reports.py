import json
import os
from jinja2 import Environment, FileSystemLoader

def extract_stats(summary_json_path):
    with open(summary_json_path) as f:
        summary_data = json.load(f)

    return {
        'passed': summary_data.get('passed', 0),
        'failed': summary_data.get('failed', 0),
        'skipped': summary_data.get('skipped', 0)
    }

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
        if os.path.exists(stats_json):
            print(f"[INFO] Updated {stats_json} with stats: {stats}")
        else:
            print(f"[INFO] Created {stats_json} with stats: {stats}")
        with open(stats_json, "w") as f:
            json.dump(stats, f)
        return True
    return False

def build_index_page(root_dir):
    reports = []
    for name in sorted(os.listdir(root_dir)):
        report_dir = os.path.join(root_dir, name)
        stats_json = os.path.join(report_dir, "stats.json")
        if os.path.isdir(report_dir) and os.path.exists(stats_json):
            stats = extract_stats_from_stats_file(stats_json)
            print(f"[DEBUG] Stats from {stats_json}: {stats}")
            report_entry = {
                "name": name,
                "passed": stats["passed"],
                "failed": stats["failed"],
                "link": f"./{name}/index.html"
            }
            print(f"[DEBUG] Adding report entry: {report_entry}")
            reports.append(report_entry)

    env = Environment(loader=FileSystemLoader(".github/templates"))
    template = env.get_template("history-index-template.html")

    output_path = os.path.join(root_dir, "index.html")
    with open(output_path, "w") as f:
        f.write(template.render(reports=reports))
    print(f"[INFO] Wrote index page to {output_path}")

def main():
    apps = ["wisp", "fdr"]
    for app in apps:
        root_dir = f"public/{app}-tests"
        for name in os.listdir(root_dir):
            report_dir = os.path.join(root_dir, name)
            if os.path.isdir(report_dir):
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
