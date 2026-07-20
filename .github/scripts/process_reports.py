import json
import os
from jinja2 import Environment, FileSystemLoader
import re
from datetime import datetime, timedelta
import shutil
from pathlib import Path

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
            statistic = statistic_raw[0] if isinstance(statistic_raw, list) else statistic_raw
            time = time_raw[0] if isinstance(time_raw, list) else time_raw
            print(f"[INFO][extract_stats] extracted statistic section {statistic}")
            print(f"[INFO][extract_stats] extracted time section {time}")
            
            # calculate duration in milliseconds
            start = time.get("start", 0)
            millis = (time.get("end", 0)) -  start
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

def find_allure_openapi_reports(artifact_dir):
    """Find all allure-report-openapi-<env> artifacts in artifacts directory.
    
    Returns a list of dicts with: artifact_path, env_name
    """
    reports = []
    print(f"[INFO][find_allure_openapi_reports] artifact_dir {artifact_dir}")
    
    # Check if artifact_dir exists
    if not os.path.isdir(artifact_dir):
        print(f"[INFO][find_allure_openapi_reports] artifact_dir {artifact_dir} does not exist")
        return reports
    
    # Look for allure-report-openapi-<env> folders
    for item in os.listdir(artifact_dir):
        if not item.startswith("allure-report-openapi-"):
            continue
        
        env_name = item.split("allure-report-openapi-")[1]
        artifact_path = os.path.join(artifact_dir, item)
        
        print(f"[INFO][find_allure_openapi_reports] found artifact folder: {item}, env_name: {env_name}")
        
        if not os.path.isdir(artifact_path):
            print(f"[INFO][find_allure_openapi_reports] {artifact_path} is not a directory, skipping")
            continue
        
        # Verify it has widgets/summary.json (Allure format)
        summary_file = os.path.join(artifact_path, "widgets", "summary.json")
        if not os.path.exists(summary_file):
            print(f"[INFO][find_allure_openapi_reports] {artifact_path} does not have widgets/summary.json, skipping")
            continue
        
        reports.append({
            'artifact_path': artifact_path,
            'env_name': env_name
        })
        print(f"[INFO][find_allure_openapi_reports] Found OpenAPI Allure report for env: {env_name}")
    
    print(f"[INFO][find_allure_openapi_reports] Total openapi allure reports found: {len(reports)}")
    return reports

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
        else:
            # Default stats for schemathesis or other reports without stats.json
            stats = {'passed': 0, 'failed': 0, 'skipped': 0}
        
        report_entry = {
            "name": name,
            "passed": stats["passed"],
            "failed": stats["failed"],
            "link": f"./{name}/index.html",
            "sort_key": name
        }
        print(f"[INFO][build_index_page] Adding report entry: {report_entry}")
        reports.append(report_entry)

    # Order by timestamp desc
    print(f"[INFO][build_index_page] sorting reports by date descending")
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
    artifact_dir = os.path.join("artifacts") # /artifacts
    print(f"[INFO][main] artifact_dir {artifact_dir}")
    
    # Process Allure reports (wisp, openapi)
    allure_apps = ["wisp", "openapi"]
    for app in allure_apps:
        root_dir = f"public/{app}-tests"
        print(f"[INFO][main] processing Allure directory {root_dir}")

        # extract stats form allure reports inside artifacts
        artifact_app_dir = os.path.join(artifact_dir, "allure-report-" + app) # /artifacts/allure-report-<app>
        print(f"[INFO][main] artifact_app_dir {artifact_app_dir}")
        if not os.path.isdir(artifact_app_dir): # in case not all app have been selected for running test
            print(f"[INFO][main] artifact_app_dir {artifact_app_dir} does not exist, skipping it")
            continue

        # retrieve stats
        stats = extract_stats(artifact_app_dir)

        # copy content from /artifacts/allure-report-<app> inside the new directory run_dir
        source_dir = Path(artifact_app_dir)
        run_dir = os.path.join(root_dir + "/" + stats.get("start")) # pattern yyyy-mm-dd_hh:mm:ss
        destination_dir = Path(run_dir)
        print(f"[INFO][main] destination_dir {destination_dir}")

        # copy everything from source to run dir and last-history dir
        last_history_dir = os.path.join(root_dir, "last-history")
        last_history_dir = Path(last_history_dir)
        print(f"[INFO][main] last_history_dir {last_history_dir}")
        if last_history_dir.exists(): # delete dir if already exists
            print(f"[INFO][main] deleting {last_history_dir} content")
            shutil.rmtree(last_history_dir)

        print(f"[INFO][main] copy everything from {source_dir} to {destination_dir}")
        shutil.copytree(source_dir, destination_dir)
        print(f"[INFO][main] copy everything from {source_dir} to {last_history_dir}")
        shutil.copytree(source_dir, last_history_dir)

        # build index page
        build_index_page(root_dir)

    # Process OpenAPI Allure reports (from Schemathesis + Allure Action)
    print(f"[INFO][main] Processing OpenAPI Allure reports (from matrix jobs)")
    openapi_reports = find_allure_openapi_reports(artifact_dir)
    
    if not openapi_reports:
        print(f"[INFO][main] No openapi allure reports found, skipping openapi-fdr processing")
    else:
        root_dir = "public/openapi-fdr-tests"
        print(f"[INFO][main] processing OpenAPI directory {root_dir}")
        
        # Create root directory if needed
        os.makedirs(root_dir, exist_ok=True)
        
        for report_info in openapi_reports:
            env_name = report_info['env_name']
            artifact_path = report_info['artifact_path']
            
            # Extract stats from this Allure report
            stats = extract_stats(artifact_path)
            
            # Create destination folder: <yyyy-mm-dd_hh:mm:ss>_<env>
            folder_name = f"{stats.get('start')}_{env_name}"
            source_dir = Path(artifact_path)
            destination_dir = Path(root_dir) / folder_name
            
            print(f"[INFO][main] Copying OpenAPI report from {source_dir} to {destination_dir}")
            
            # Copy the report
            if destination_dir.exists():
                shutil.rmtree(destination_dir)
            shutil.copytree(source_dir, destination_dir)
            
            # Also update last-history for this env
            last_history_env = Path(root_dir) / f"last-history-{env_name}"
            if last_history_env.exists():
                shutil.rmtree(last_history_env)
            shutil.copytree(source_dir, last_history_env)
        
        # Build index page for openapi-fdr (uses generic method)
        build_index_page(root_dir)

if __name__ == "__main__":
    main()
