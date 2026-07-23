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


def read_page_components():
  page_components = dict()
  try:
    # use headerOnlyPage instead of actually calling the API to get the content of the page
    with open('./report_page_components/title.txt', 'r', encoding='utf-8') as f:
      page_components['title'] = f.read().strip()

    # use headerOnlyPage instead of actually calling the API to get the content of the page
    with open('./report_page_components/go_table.txt', 'r', encoding='utf-8') as f:
      page_components['go_table'] = f.read().strip()

    # use headerOnlyPage instead of actually calling the API to get the content of the page
    with open('./report_page_components/main_table.txt', 'r', encoding='utf-8') as f:
      page_components['main_table'] = f.read().strip()

    with open('./report_page_components/table_header.txt', 'r', encoding='utf-8') as f:
      page_components['table_header'] = f.read().strip()

    with open('./report_page_components/table_row.txt', 'r', encoding='utf-8') as f:
      page_components['table_row'] = f.read().strip()

    return page_components
  except Exception as e:
    raise RuntimeError(f"Failed to read page components from ./report_page_components. Error: {str(e)}")

# use headerOnlyPage instead of actually calling the API to get the content of the page
def read_stats(stats_file):
  with open(stats_file,'r',encoding="utf-8") as f:
    last_history = json.load(f)
    run['failures'] = last_history.get('failed', 0)
    run['duration'] = last_history.get('duration', 0)
    start = last_history.get('start', '')
    if start:
        run['time'] = start.split('_')[1]
        run['date'] = start.split('_')[0]
    print(f"[INFO][read_stats] Last history: failures={run['failures']}, duration={run['duration']}, time={run['time']}")


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
        run_stats['uid'] = run_obj.get('uid')
        run_stats['full_name'] = run_obj.get('fullName')
        for stage in run_obj.get('testStage', {}).get('steps', []):
          if stage.get('status') == 'failed':
            run_stats['result'] = stage.get('statusMessage')
            if stage.get('statusTrace'):
              run_stats['error_log'] = extract_main_error_line(stage.get('statusTrace'))
        failedRuns.append(run_stats.copy())

    run['runs'] = failedRuns
    with open('run.json', 'w', encoding='utf-8') as f:
      json.dump(run, f, indent=4, ensure_ascii=False)
  except Exception as e:
    raise RuntimeError(f"Failed while processing runs in {dir}. Error: {str(e)}")


def build_page(folder_name, page_components, config):
  try:
    page = ''
    page += page_components['title'].replace('{title}', (run['date'] + " - " + folder_name))
    page += page_components['go_table']
    main_table = page_components['main_table']
    for field in run:
      if not isinstance(run[field], list):
        main_table = main_table.replace(f'{{{field}}}', str(run.get(field, MISSING_DATA)))
    page += main_table
    if run['failures'] > 0:
      page += page_components['table_header']
      for test_run in run['runs']:
        row = page_components['table_row']
        for field in test_run:
          row = row.replace(f'{{{field}}}', str(test_run.get(field, '')))
        # use all parts of folder_name except the last as the config key (joined by '-')
        components_val = config.get('components', '')
        if isinstance(components_val, (list, tuple)):
          components_str = ','.join(map(str, components_val))
        else:
          components_str = str(components_val) if components_val is not None else ''
        row = row.replace('{components}', components_str)
        row = re.sub(r'\{[^}]+\}', '', row).strip(" ")
        page += row
      page += "</tr></tbody></table>"
    return page
  except Exception as e:
    raise RuntimeError(f"Failed to build page for {folder_name}. Error: {str(e)}")


def read_config(suite):
    try:
        read_config = Dynaconf(settings_files=['config.yaml'])
        key_parts = suite.split('-')[:-1]
        key = '-'.join(key_parts) or suite
        return read_config[key] if key in read_config else {}
    except KeyError as e:
        raise RuntimeError(f"Config key '{key}' not found in config.yaml. Error: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Failed to read config from config.yaml. Error: {str(e)}")

def main():
  # parse CLI args
  parser = argparse.ArgumentParser(description='Create Confluence page from test runs')
  parser.add_argument('--run-type', '-t', default='NO-PROMO', help='Type of run (default: NO-PROMO)')
  args = parser.parse_args()
  run['scope'] = args.run_type

  if os.listdir(PROCESSED_REPORTS_DIR) == []:
    print(f"[INFO][main] No processed reports found in {PROCESSED_REPORTS_DIR}. Exiting.")
    return
  # Read the last history data from stats.json
  for dir in os.listdir(PROCESSED_REPORTS_DIR):
    run_dir = os.path.join(PROCESSED_REPORTS_DIR, dir)
    if os.path.isdir(run_dir):
      global suite
      run['env'] = dir.split('-')[-1]
      suite = os.path.basename(dir)
      if os.path.exists(os.path.join(run_dir, 'stats.json')):
        try:
            read_stats(os.path.join(run_dir, 'stats.json'))
            read_runs(os.path.join(run_dir, TEST_CASES_DIR))
            page_components = read_page_components()
            config = read_config(suite)
            page = build_page(suite, page_components, config)
            page_title = str(run['date']).replace('-', '') + " - " + suite
            create_confluence_page(page.strip(), config=config, page_title=page_title, auth_obj=create_confluence_auth())
        except Exception as e:
            print(f"[ERROR][main] Failed processing run directory {run_dir}. Error: {str(e)}")
            continue
    
    print(f"[INFO][main] Finished processing run directory {run_dir}. Removing it.")
    shutil.rmtree(PROCESSED_REPORTS_DIR)
    

if __name__ == "__main__":
  try:
    main()
  except Exception as e:
    print(f"[ERROR][create_report_page] {str(e)}")
    raise