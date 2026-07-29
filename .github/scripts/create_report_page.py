import json
import os
import re
import shutil
from dynaconf import Dynaconf
import argparse
import sys
from pathlib import Path

# Ensure repository root is on sys.path so `src` package is importable when this
# script runs from .github/scripts in CI environments.
REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))
GITHUB_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
from src.utility.confluence_utils import create_confluence_auth, create_confluence_page
from src.conf.configuration import load_settings



failedRuns = list()
TEST_CASES_DIR = 'data/test-cases'
MISSING_DATA = 'N/A'
ARTIFACTS_DIR = 'artifacts'
PAGE_COMPONENTS_DIR = Path(__file__).resolve().parents[1] / 'page_components' / 'test_report_page'
GH_PAGES_URL = 'https://pagopa.github.io/pagopa-platform-integration-test/{suite_folder}/{run}/index.html'

START_KEY = 'start'
TEST_STAGE_KEY = 'testStage'
STEPS_KEY = 'steps'
RESULT_KEY = 'result'
STATUS_MESSAGE_KEY = 'statusMessage'
STATUS_KEY = 'status'
STATUS_TRACE_KEY = 'statusTrace'
PROCEDURE_KEY = 'procedure'
TIME_KEY = 'time'
ERROR_LOG_KEY = 'error_log'
TITLE_COMPONENT_KEY = 'title'
GO_TABLE_COMPONENT_KEY = 'go_table'
MAIN_TABLE_COMPONENT_KEY = 'main_table'
TABLE_HEADER_COMPONENT_KEY = 'table_header'
TABLE_ROW_COMPONENT_KEY = 'table_row'
RUNS_KEY = 'runs'
TITLE_PLACEHOLDER = '{title}'
TABLE_CLOSING_TAG = '</tr></tbody></table>'
ANALISI_RUN_PAGE_TITLE_KEY = 'Analisi RUN'
STATS_FILE_NAME = 'stats.json'

SCOPE_KEY = 'scope'
ENV_KEY = 'env'
DATE_KEY = 'date'
TIME_KEY = 'time'
FAILED_KEY = 'failed'
DURATION_KEY = 'duration'
ALLURE_PAGE_KEY = 'allure_page'


run = {
  SCOPE_KEY: '',
  ENV_KEY: '',
  FAILED_KEY: 0,
  DURATION_KEY: 0,
  ALLURE_PAGE_KEY: '',
  TIME_KEY: None,
  DATE_KEY: None,
  RUNS_KEY: None
}


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

# use headerOnlyPage instead of actually calling the API to get the content of the page
def read_stats(stats_file, suite_test_folder):
  with open(stats_file,'r',encoding="utf-8") as f:
    last_history = json.load(f)
    run[FAILED_KEY] = last_history.get(FAILED_KEY, 0)
    run[DURATION_KEY] = last_history.get(DURATION_KEY, 0)
    start = last_history.get(START_KEY, '')
    if start:
        run[TIME_KEY] = start.split('_')[1]
        run[DATE_KEY] = start.split('_')[0]
        run[ALLURE_PAGE_KEY] = GH_PAGES_URL.replace('{suite_folder}', suite_test_folder).replace('{run}', run[DATE_KEY])
    print(f"[INFO][read_stats] Last history: failures={run[FAILED_KEY]}, duration={run[DURATION_KEY]}, time={run[TIME_KEY]}, date={run[DATE_KEY]}") 


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

def read_runs(dir, suite_test_folder):
  failedRuns = list()
  try:
    for file in os.listdir(dir):
      file_path = os.path.join(dir, file)
      try:
        with open(file_path, 'r', encoding='utf-8') as f:
          run_obj = json.load(f)
      except Exception as e:
        raise RuntimeError(f"Failed to read run file {file_path}. Error: {str(e)}")

      if run_obj.get(STATUS_KEY) == "failed":
        run_stats = dict()
        run_stats['uid'] = GH_PAGES_URL.replace('{suite_folder}', suite_test_folder).replace('{run}', run[DATE_KEY])
        for stage in run_obj.get(TEST_STAGE_KEY, {}).get(STEPS_KEY, []):
          if stage.get(STATUS_KEY) == 'failed':
            run_stats[RESULT_KEY] = stage.get(STATUS_MESSAGE_KEY)
            if stage.get(STATUS_TRACE_KEY):
              run_stats[ERROR_LOG_KEY] = extract_main_error_line(stage.get(STATUS_TRACE_KEY))
        print(f"[INFO][read_runs] Found failed run: {run_stats}")
        failedRuns.append(run_stats.copy())

    run[RUNS_KEY] = failedRuns
    print(f"[INFO][read_runs] Successfully read {len(failedRuns)} failed runs from {dir}")
  except Exception as e:
    raise RuntimeError(f"Failed while processing runs in {dir}. Error: {str(e)}")


def build_page(folder_name, page_components, config):
  try:
    page = ''
    page += page_components[TITLE_COMPONENT_KEY].replace(TITLE_PLACEHOLDER, (run['date'] + " - " + run['time'] + folder_name))
    page += page_components[GO_TABLE_COMPONENT_KEY]
    main_table = page_components[MAIN_TABLE_COMPONENT_KEY]
    for field in run:
      if field != RUNS_KEY:
        main_table = main_table.replace(f'{{{field}}}', str(run.get(field, MISSING_DATA)))
    page += main_table
    if run[FAILED_KEY] > 0:
      page += page_components[TABLE_HEADER_COMPONENT_KEY]
      for test_run in run[RUNS_KEY]:
        row = page_components[TABLE_ROW_COMPONENT_KEY]
        for field in test_run:
          row = row.replace(f'{{{field}}}', str(test_run.get(field, '')))
        # use all parts of folder_name except the last as the config key (joined by '-')
        row = re.sub(r'\{[^}]+\}', '', row).strip(" ")
        page += row
      page += TABLE_CLOSING_TAG
    print(f"[INFO][build_page] Successfully built page content for {folder_name}")
    return page
  except Exception as e:
    raise RuntimeError(f"Failed to build page for {folder_name}. Error: {str(e)}")


def read_config(suite, config):
    try:
        key_parts = suite.split('-')[:-1]
        key = '-'.join(key_parts) or suite
        return config[key] if key in config else {}
    except KeyError as e:
        raise RuntimeError(f"Config key '{key}' not found in config.yaml. Error: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Failed to read config from config.yaml. Error: {str(e)}")

def main():
  # parse CLI args
  parser = argparse.ArgumentParser(description='Create Confluence page from test runs')
  parser.add_argument('--run-type', '-t', default='NO-PROMO', help='Type of run (default: NO-PROMO)')
  args = parser.parse_args()
  run[SCOPE_KEY] = args.run_type

  # Support processed reports created under `public/` by the deploy job
  processed_dir = ARTIFACTS_DIR
  if not os.path.exists(processed_dir) and os.path.exists(os.path.join('artifacts', ARTIFACTS_DIR)):
     processed_dir = os.path.join('artifacts', ARTIFACTS_DIR)
     print(f"[INFO][main] Found processed reports in {processed_dir}.")

  if not os.path.isdir(processed_dir) or os.listdir(processed_dir) == []:
    print(f"[INFO][main] No processed reports found in {processed_dir}. Exiting.")
    return
  # Read the last history data from stats.json
  full_config = load_settings(config_folder_root=GITHUB_ROOT)
  for dir in sorted(os.listdir(processed_dir)):
    run_dir = os.path.join(processed_dir, dir)
    if os.path.isdir(run_dir):
      global suite
      run[ENV_KEY] = dir.split('-')[-1]
      suite = os.path.basename(dir)
      # build the suite test folder path based on the run directory name
      suite_test_folder = os.path.join('artifacts', dir.split('-')[-1] + "-tests")
      if os.path.exists(os.path.join(run_dir, STATS_FILE_NAME)):
        try:
            read_stats(os.path.join(run_dir, STATS_FILE_NAME), suite_test_folder)
            read_runs(os.path.join(run_dir, TEST_CASES_DIR), suite_test_folder)
            page_components = read_page_components()
            suite_config = read_config(suite, full_config)
            page = build_page(suite, page_components, suite_config)
            page_title = str(run[DATE_KEY]).replace('-', '') + str(run[TIME_KEY]) + " " + ANALISI_RUN_PAGE_TITLE_KEY + " " + suite.upper()
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