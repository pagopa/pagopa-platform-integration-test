import json
import os
from jinja2 import Environment, FileSystemLoader
import re
from datetime import datetime, timedelta
import shutil
from pathlib import Path

def extract_stats(artifact_app_dir):
    try:
        artifact_summary_file = os.path.join(artifact_app_dir, "widgets").join("summary.json")
        with open(artifact_summary_file) as f:

            # load summary.json file
            print(f"[INFO][extract_stats] loading {artifact_summary_file} file")
            data = json.load(f)
            print(f"[INFO][extract_stats] {artifact_summary_file} file loaded")

            # extract statistic and time sections from summary
            statistic_raw = data.get("statistic", {})
            time_raw = data.get("time", {})
            statistic = statistic_raw[0] if isinstance(statistic_raw, list) else statistic_raw
            time = time_raw[0] if isinstance(time_raw, list) else time_raw
            print(f"[INFO][extract_stats] extracted statistic section {statistic}")
            print(f"[INFO][extract_stats] extracted time section {time}")

            # calculate duration in milliseconds
            start = time.get("start", 0)
            end = time.get("end", 0)
            duration_ms = end - start
            duration = timedelta(milliseconds=duration_ms)
            print(f"[INFO][extract_stats] duration in millis {duration}")

            # format duration as hh:mm:ss
            total_seconds = int(duration.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            formatted_duration = f"{hours:02}:{minutes:02}:{seconds:02}"
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
                "duration": formatted_duration,
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

    reports = []
    for name in os.listdir(root_dir):
        report_dir = os.path.join(root_dir, name)
        stats_json = os.path.join(report_dir, "stats.json")
        if os.path.isdir(report_dir) and os.path.exists(stats_json) and name not in ("last-history", "index.html"):
            stats = extract_stats_from_stats_file(stats_json)
            report_entry = {
                "name": name,
                "passed": stats["passed"],
                "failed": stats["failed"],
                "link": f"./{name}/index.html",
                "sort_key": name
            }
            print(f"[INFO][build_index_page] Adding report entry: {report_entry}")
            reports.append(report_entry)
        else:
            print(f"[INFO][build_index_page] skipping dir {report_dir} not found")

    # Order by timestamp desc
    print(f"[INFO][build_index_page] sorting badge by date descending")
    reports.sort(key=lambda r: r["sort_key"], reverse=True)

    # load index template and render template
    print(f"[INFO][build_index_page] applying history-index-template.html template")
    env = Environment(loader=FileSystemLoader(".github/templates"))
    template = env.get_template("history-index-template.html")
    output_path = os.path.join(root_dir, "index.html")
    with open(output_path, "w") as f:
        print(f"[INFO][build_index_page] Writing index page to {output_path} ...")
        f.write(template.render(reports=reports))
    print(f"[INFO][build_index_page] written index page to {output_path}")

def main():
    apps = ["wisp", "fdr"]
    artifact_dir = os.path.join("artifacts") # /artifacts
    print(f"[INFO][main] artifact_dir {artifact_dir}")
    for app in apps:
        root_dir = f"public/{app}-tests"
        print(f"[INFO][main] processing directory {root_dir}")

        # extract stats form allure reports inside artifacts
        artifact_app_dir = os.path.join(artifact_dir, "allure-report-" + app) # /artifacts/allure-report-<app>
        print(f"[INFO][main] artifact_app_dir {artifact_app_dir}")
        if not os.path.isdir(artifact_app_dir): # in case not all app have been selected for running test
            print(f"[INFO][main] artifact_app_dir {artifact_app_dir} does not exist, skipping it")
            continue

        stats = extract_stats(artifact_app_dir)

        # create directory with pattern yyyy-mm-dd_hh:mm:ss
        run_dir = os.path.join(root_dir) + "/" + stats.get("start") + "_" + stats.get("duration")
        os.makedirs(run_dir)
        print(f"[INFO][main] run_dir {run_dir} has been created")

        # copy content from /artifacts/allure-report-<app> inside the new directory run_dir
        source_dir = Path(artifact_app_dir)
        destination_dir = Path(run_dir)
        print(f"[INFO][main] destination_dir {destination_dir}")

        # copy everything from source to run dir and last-history dir
        last_history_dir = os.path.join(root_dir, "last-history")
        print(f"[INFO][main] last_history_dir {last_history_dir}")
        if destination_dir.exists(): # delete dir if already exists
            print(f"[INFO][main] deleting {destination_dir} content")
            shutil.rmtree(destination_dir)

        print(f"[INFO][main] copy everything from {source_dir} to {destination_dir}")
        shutil.copytree(source_dir, destination_dir)
        print(f"[INFO][main] copy everything from {source_dir} to {last_history_dir}")
        shutil.copytree(source_dir, last_history_dir)

        # build index page
        build_index_page(root_dir)

if __name__ == "__main__":
    main()
