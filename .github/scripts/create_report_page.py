from calendar import calendar
import json
import os
import re
import shutil
from dynaconf import Dynaconf
import argparse
import sys
from pathlib import Path
from datetime import datetime, timedelta
from babel.dates import format_date

# Ensure repository root is on sys.path so `src` package is importable when this
# script runs from .github/scripts in CI environments.
REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))
from src.utility.constants  import GITHUB_ROOT, NRT_SUITES_FILE
from src.conf.configuration import load_configurations
from src.utility.confluence_utils import create_confluence_auth, create_confluence_page, get_descendants, create_confluence_folder


run = {
  'scope': '',
  'env': '',
  'failed': 0,
  'broken': 0,
  'duration': 0,
  'time': None,
  'date': None,
  'runs': None
}
failedRuns = list()
TEST_CASES_DIR = 'data/test-cases'
MISSING_DATA = 'N/A'
PROCESSED_REPORTS_DIR = 'tmp_processed_reports'
PAGE_COMPONENTS_DIR = Path(__file__).resolve().parents[1] / 'page_components' / 'test_report_page'
GH_PAGES_URL = 'https://pagopa.github.io/pagopa-platform-integration-test/{suite_folder}/{run}/index.html#suites/{run_id}'
TITLE_COMPONENT_KEY = 'title'
GO_TABLE_COMPONENT_KEY = 'go_table'
MAIN_TABLE_COMPONENT_KEY = 'main_table'
TABLE_HEADER_COMPONENT_KEY = 'table_header'
TABLE_ROW_COMPONENT_KEY = 'table_row'
COMPONENTS_KEY = 'components'
TITLE_PLACEHOLDER = '{title}'
COMPONENTS_PLACEHOLDER = '{components}'
TABLE_CLOSING_TAG = '</tr></tbody></table>'


def read_page_components():
  page_components = dict()
  try:
    with open(PAGE_COMPONENTS_DIR / 'title.txt', 'r', encoding='utf-8') as f:
      page_components[TITLE_COMPONENT_KEY] = f.read().strip()

    with open(PAGE_COMPONENTS_DIR / 'go_table.txt', 'r', encoding='utf-8') as f:
      page_components[GO_TABLE_COMPONENT_KEY] = f.read().strip()

    with open(PAGE_COMPONENTS_DIR / 'main_table.txt', 'r', encoding='utf-8') as f:
      page_components[MAIN_TABLE_COMPONENT_KEY] = f.read().strip()

    with open(PAGE_COMPONENTS_DIR / 'table_header.txt', 'r', encoding='utf-8') as f:
      page_components[TABLE_HEADER_COMPONENT_KEY] = f.read().strip()

    with open(PAGE_COMPONENTS_DIR / 'table_row.txt', 'r', encoding='utf-8') as f:
      page_components[TABLE_ROW_COMPONENT_KEY] = f.read().strip()

    return page_components
  except Exception as e:
    raise RuntimeError(f"Failed to read page components from {PAGE_COMPONENTS_DIR}. Error: {str(e)}")

# GH Pages URL builder (deprecated)
# def read_run_id(run_file):
#     try:
#         with open(run_file, 'r', encoding='utf-8') as f:
#             run_data = json.load(f)
#             run['uid'] = run_data.get('uid')
#     except Exception as e:
#         raise RuntimeError(f"Failed to read run ID from {run_file}. Error: {str(e)}")

# use headerOnlyPage instead of actually calling the API to get the content of the page
def read_summary(stats_file):
  with open(stats_file,'r',encoding="utf-8") as f:
    last_history = json.load(f)
    statistic = last_history.get('statistic', {})
    if isinstance(statistic, list):
        statistic = statistic[0] if statistic else {}
    time_data = last_history.get("time") or {}
    if isinstance(time_data, list):
        time_data = time_data[0] if time_data else {}
    if statistic == {} or time_data == {}:
        raise RuntimeError(f"Invalid statistics or time data in {stats_file}. Statistics: {statistic}, Time: {time_data}")
    
    run['failed'] = statistic.get('failed', 0)
    run['duration'] = str(timedelta(milliseconds=time_data.get('duration', 0))).split('.')[0]
    run['start'] = datetime.fromtimestamp(time_data.get('start',0) / 1000.0).strftime("%Y-%m-%d %H:%M:%S")
    run['time'] = (run['start'].split(' ')[1] + timedelta(hours=2)).strftime("%H:%M:%S")
    run['date'] = run['start'].split(' ')[0]
    # GH Pages URL building is currently disabled.
    # run['allure_page'] = GH_PAGES_URL.replace('{suite_folder}', suite_test_folder).replace('{run}', start)
    print(f"[INFO][read_summary] Last history: failed={run['failed']}, duration={run['duration']}, time={run['time']}")


def extract_main_error_line(trace: str) -> str:
    if not trace:
      return ''
    # remove tildes and carets but preserve newlines so splitlines() works
    trace = re.sub(r'[~^]+', '', trace)
    lines = [ln.strip() for ln in trace.splitlines() if ln.strip()]
    if not lines:
      return ''
    else: 
      return lines[-1]

def read_runs(dir):
  failedRuns = list()
  run['broken'] = 0    
  try:
    for file in os.listdir(dir):
      file_path = os.path.join(dir, file)
      try:
        with open(file_path, 'r', encoding='utf-8') as f:
          run_obj = json.load(f)
      except Exception as e:
        raise RuntimeError(f"Failed to read run file {file_path}. Error: {str(e)}")

      if run_obj.get('status') == 'failed' or run_obj.get('status') == 'broken':
        # Increment the failures count adding broken runs
        if run_obj.get('status') == 'broken':
          run['broken'] += 1        

        run_stats = dict()
        # run_stats['uid'] = run['allure_page'] + f'/{run_obj.get("uid")}'
        run_stats['scenario_name'] = run_obj.get('name', MISSING_DATA)
        for stage in run_obj.get('testStage', {}).get('steps', []):
          if stage.get('status') == 'failed' or stage.get('status') == 'broken':
            run_stats['result'] = stage.get('statusMessage')
            if stage.get('statusTrace'):
              run_stats['error_log'] = extract_main_error_line(stage.get('statusTrace'))
        failedRuns.append(run_stats.copy())

    run['runs'] = failedRuns
    print(f"[INFO][read_runs] Successfully read {len(failedRuns)} failed runs from {dir}")
  except Exception as e:
    raise RuntimeError(f"Failed while processing runs in {dir}. Error: {str(e)}")


def build_page(folder_name, page_components, config):
  try:
    page = ''
    page += page_components[TITLE_COMPONENT_KEY].replace(TITLE_PLACEHOLDER, (run["date"] + " - " + folder_name))
    page += page_components[GO_TABLE_COMPONENT_KEY]
    main_table = page_components[MAIN_TABLE_COMPONENT_KEY]

    # set the run['env'] to 'UAT' if it is not set
    if not run['env']:
      run['env'] = 'UAT'
        
    for field in run:
      if field != 'runs':
        main_table = main_table.replace(f'{{{field}}}', str(run.get(field, MISSING_DATA)))
    page += main_table
    if run['failed'] > 0:
      page += page_components[TABLE_HEADER_COMPONENT_KEY]
      for test_run in run['runs']:
        row = page_components[TABLE_ROW_COMPONENT_KEY]
        for field in test_run:
          row = row.replace(f'{{{field}}}', str(test_run.get(field, MISSING_DATA)))
        # use all parts of folder_name except the last as the config key (joined by '-')
        row = re.sub(r'\{[^}]+\}', '', row).strip(" ")
        page += row
      page += TABLE_CLOSING_TAG
    print(f"[INFO][read_runs] Successfully built page content for {folder_name}")
    return page
  except Exception as e:
    raise RuntimeError(f"Failed to build page for {folder_name}. Error: {str(e)}")
  

def read_config(key,config):
    try:
        return config[key] if key in config else {}
    except KeyError as e:
        raise RuntimeError(f"Config key '{key}' not found in config.yaml. Error: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Failed to read config from config.yaml. Error: {str(e)}")

# GH Pages URL builder (deprecated version commented out)
# def build_gh_pages_url(suite_folder):
#   try:
#     url = GH_PAGES_URL.replace('{suite_folder}', suite_folder).replace('{run}',run["start"]).replace('{run_id}', run['uid'])
#     print(f"[INFO][build_gh_pages_url] Built GH Pages URL: {url}")
#     return url
#   except Exception as e:
#     raise RuntimeError(f"Failed to build GH Pages URL for suite_folder={suite_folder}, run={run}. Error: {str(e)}")
  
def get_month_folder_id(descendants, suite_config, confluence_auth, suite):
    current_month = str(format_date(datetime.now(), "LLLL", locale="it_IT")).capitalize()
    folder_name = f"{str(suite).capitalize()}-{current_month}-{datetime.now().year}"
    current_month_folder = [x['id'] for x in descendants['results'] if x['title'] == folder_name]
    if current_month_folder:
        return current_month_folder[0]
    else:
        month_folder = create_confluence_folder(suite_config, folder_name, confluence_auth)
        if month_folder:
            return month_folder['id']
    return None


def find_nrt_suite(dir_name: str, suites: dict) -> dict | None:
    '''
    Resolve the NRT suite definition for an artifact directory.

    Supports both the legacy processed reports layout (artifacts/<suite id>) and the
    NRT per-suite artifacts layout (artifacts/<report_artifact>, e.g. allure-report-wisp).
    '''
    for suite in suites.get('suites', []):
        if dir_name in (suite.get('report_artifact'), suite.get('id')):
            return suite
    return None
      


def main():
  # parse CLI args
  parser = argparse.ArgumentParser(description='Create Confluence page from test runs')
  parser.add_argument('--run-type', '-t', default='NO-PROMO', help='Type of run (default: NO-PROMO)')
  args = parser.parse_args()
  run['scope'] = args.run_type

  # Support processed reports created under `public/` by the deploy job
  processed_dir = "artifacts"
  if not os.path.isdir(processed_dir) or os.listdir(processed_dir) == []:
    print(f"[INFO][main] No processed reports found in {processed_dir}. Exiting.")
    return
  
  print(f"[INFO][main] Found processed reports in {processed_dir}.")

  if not os.environ.get('TARGET_ENV'):
    print(f"[INFO][main] TARGET_ENV not set. Setting it to the default value: UAT.")
    os.environ['TARGET_ENV'] = 'UAT'

  with open(NRT_SUITES_FILE, 'r') as f:
    suites = json.load(f)

  # Read the last history data from stats.json
  full_config = load_configurations(GITHUB_ROOT)
  for dir in sorted(os.listdir(processed_dir)):
    run_dir = os.path.join(processed_dir, dir)
    if os.path.isdir(run_dir):
      global suite


      nrt_suite = find_nrt_suite(dir, suites)
      if nrt_suite:
          suite = nrt_suite.get('id')

      # build the suite test folder path based on the run directory name
      suite_test_folder = suite + "-tests"
     
      if os.path.exists(os.path.join(run_dir, "widgets/summary.json")):
        try:
            # GH Pages URL building is currently disabled.
            # read_run_id(os.path.join(run_dir, "data/suites.json"))
            # read the last history data from summary.json
            read_summary(os.path.join(run_dir, "widgets/summary.json"))
            # GH Pages URL building is currently disabled.
            # run['allure_page'] = build_gh_pages_url(suite_test_folder)
            # read the failed runs from the run directory's data/test-cases folder
            read_runs(os.path.join(run_dir, "data/test-cases"))
            # read the page components 
            page_components = read_page_components()
            # read the suite configuration from config.yaml
            suite_config = read_config(suite, full_config)
            # create the title for the Confluence page
            page_title = str(run["date"]).replace('-', '') + " " +str(run["time"]) + " " + "Analisi RUN" + " " + suite.upper() + (" - " + run['env'].upper() if run['env'] else "")
            # build the Confluence page content 
            page = build_page(suite, page_components, suite_config)
            # create an auth object for Confluence
            confluence_auth = create_confluence_auth()
            # obtain the descendant of the suite folder on Confluence
            descendants = get_descendants(suite_config, confluence_auth)
            # get the month folder ID from the descendants of the suite folder, or else create it if it doesn't exist
            month_folder_id = get_month_folder_id(descendants, suite_config, confluence_auth, suite)
            # create the Confluence page using the built content and title
            create_confluence_page(page.strip(), parent_id=month_folder_id, page_title=page_title, auth_obj=confluence_auth)
        except Exception as e:
            print(f"[ERROR][main] Failed processing run directory {run_dir}. Error: {str(e)}")
            continue

  # Remove processed reports only once, after all run directories were handled.
  print(f"[INFO][main] Finished processing all run directories. Removing processed reports directory {processed_dir}.")
  try:
    shutil.rmtree(processed_dir)
    if not os.path.exists(processed_dir):
       print(f"[INFO][main] Removed processed reports directory: {processed_dir}")     
  except Exception as e:
    print(f"[WARN][main] Could not remove processed reports directory {processed_dir}: {e}")
    

if __name__ == "__main__":
  try:
    main()
  except Exception as e:
    print(f"[ERROR][create_report_page] {str(e)}")
    raise