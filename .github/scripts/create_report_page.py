import json
import os
import re
import shutil
from dynaconf import Dynaconf
import argparse
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Ensure repository root is on sys.path so `src` package is importable when this
# script runs from .github/scripts in CI environments.
REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))
GITHUB_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
from src.utility.confluence_utils import create_confluence_auth, create_confluence_page


run = {
  'scope': '',
  'env': '',
  'failures': 0,
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
    # use headerOnlyPage instead of actually calling the API to get the content of the page
    with open(PAGE_COMPONENTS_DIR / 'title.txt', 'r', encoding='utf-8') as f:
      page_components[TITLE_COMPONENT_KEY] = f.read().strip()

    # use headerOnlyPage instead of actually calling the API to get the content of the page
    with open(PAGE_COMPONENTS_DIR / 'go_table.txt', 'r', encoding='utf-8') as f:
      page_components[GO_TABLE_COMPONENT_KEY] = f.read().strip()

    # use headerOnlyPage instead of actually calling the API to get the content of the page
    with open(PAGE_COMPONENTS_DIR / 'main_table.txt', 'r', encoding='utf-8') as f:
      page_components[MAIN_TABLE_COMPONENT_KEY] = f.read().strip()

    with open(PAGE_COMPONENTS_DIR / 'table_header.txt', 'r', encoding='utf-8') as f:
      page_components[TABLE_HEADER_COMPONENT_KEY] = f.read().strip()

    with open(PAGE_COMPONENTS_DIR / 'table_row.txt', 'r', encoding='utf-8') as f:
      page_components[TABLE_ROW_COMPONENT_KEY] = f.read().strip()

    return page_components
  except Exception as e:
    raise RuntimeError(f"Failed to read page components from {PAGE_COMPONENTS_DIR}. Error: {str(e)}")

def read_run_id(run_file):
    try:
        with open(run_file, 'r', encoding='utf-8') as f:
            run_data = json.load(f)
            run['uid'] = run_data.get('uid')
    except Exception as e:
        raise RuntimeError(f"Failed to read run ID from {run_file}. Error: {str(e)}")

# use headerOnlyPage instead of actually calling the API to get the content of the page
def read_stats(stats_file,suite_test_folder):
  with open(stats_file,'r',encoding="utf-8") as f:
    last_history = json.load(f)
    run['failed'] = last_history.get('failed', 0)
    run['duration'] = last_history.get('duration', 0)
    start = last_history.get('start', '')
    if start:
        run['start'] = start
        run['time'] = start.split('_')[1]
        time_formatted = datetime.strptime(run['time'], "%H:%M:%S")
        run['time'] = (time_formatted + timedelta(hours=2)).strftime("%H:%M:%S")
        run['date'] = start.split('_')[0]
        run['allure_page'] = GH_PAGES_URL.replace('{suite_folder}', suite_test_folder).replace('{run}', start)
    print(f"[INFO][read_stats] Last history: failed={run['failed']}, duration={run['duration']}, time={run['time']}")


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
  try:
    for file in os.listdir(dir):
      file_path = os.path.join(dir, file)
      try:
        with open(file_path, 'r', encoding='utf-8') as f:
          run_obj = json.load(f)
      except Exception as e:
        raise RuntimeError(f"Failed to read run file {file_path}. Error: {str(e)}")

      if run_obj.get('status') == 'failed':
        run_stats = dict()
        run_stats['uid'] = run['allure_page'] + f'/{run_obj.get("uid")}'
        for stage in run_obj.get('testStage', {}).get('steps', []):
          if stage.get('status') == 'failed':
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
  
def build_gh_pages_url(suite_folder):
  try:
    url = GH_PAGES_URL.replace('{suite_folder}', suite_folder).replace('{run}',run["start"] + "-" + run['env']).replace('{run_id}', run['uid'])
    print(f"[INFO][build_gh_pages_url] Built GH Pages URL: {url}")
    return url
  except Exception as e:
    raise RuntimeError(f"Failed to build GH Pages URL for suite_folder={suite_folder}, run={run}. Error: {str(e)}")


def read_config(key,config):
    try:
        return config[key] if key in config else {}
    except KeyError as e:
        raise RuntimeError(f"Config key '{key}' not found in config.yaml. Error: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Failed to read config from config.yaml. Error: {str(e)}")


def build_gh_pages_url(suite_folder):
  try:
    url = GH_PAGES_URL.replace('{suite_folder}', suite_folder).replace('{run}',run["start"]).replace('{run_id}', run['uid'])
    print(f"[INFO][build_gh_pages_url] Built GH Pages URL: {url}")
    return url
  except Exception as e:
    raise RuntimeError(f"Failed to build GH Pages URL for suite_folder={suite_folder}, run={run}. Error: {str(e)}")

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


  # Read the last history data from stats.json
  full_config = Dynaconf(
            settings_files=[os.path.join(GITHUB_ROOT,'config.yaml')])
  for dir in sorted(os.listdir(processed_dir)):
    run_dir = os.path.join(processed_dir, dir)
    if os.path.isdir(run_dir):
      global suite

      if dir.startswith('openapi-fdr'):
        suite = '-'.join(dir.split('-')[:-1]) 
        run['env'] = dir.split('-')[-1].upper()
      else:
        suite = str(dir)

      # build the suite test folder path based on the run directory name
      suite_test_folder = suite + "-tests"
     
      if os.path.exists(os.path.join(run_dir, "stats.json")):
        try:
            # get run id from the run directory's data/suites.json file
            read_run_id(os.path.join(run_dir, "data/suites.json"))
            # read the last history data from stats.json
            read_stats(os.path.join(run_dir, "stats.json"), suite_test_folder)
            # build the GH Pages URL for the run
            run['allure_page'] = build_gh_pages_url(suite_test_folder)
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
            # create the Confluence page using the built content and title
            create_confluence_page(page.strip(), config=suite_config, page_title=page_title, auth_obj=create_confluence_auth())
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