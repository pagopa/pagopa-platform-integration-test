import os
import json
import sys
from pathlib import Path
import argparse
import requests
from datetime import datetime, timedelta

from dynaconf import Dynaconf

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from src.models.test_models import Test_suites, Test_runs, Test_executions
from src.utility.constants  import GITHUB_ROOT, SUMMARY_FILE_PATH, TEST_CASES_PATH, NRT_SUITES_FILE, ALLURE_BASE_URL
from src.conf.configuration import load_configurations

# the location of the allure results when we execute the tests with the TAS
ALLURE_RESULT_PATH = "allure-results"


def calculate_total_failures(test_run: Test_runs) -> int:
    """
    Calculate the total number of failed scenarios for a given test run.

    Args:
        test_run (Test_runs): The test run object.

    Returns:
        int: The total number of failed, broken, and skipped scenarios.
    """
    return (test_run.failed_scenario or 0) + (test_run.broken_scenario or 0) + (test_run.skipped_scenario or 0)


def populate_test_run(test_run: Test_runs, summary_path: str, version: str, test_object: str, allure_subfolder: str):
    '''
    Populate the test_run object based on the data found in summary.json file.

    Args:
        test_run (Test_runs): The test run object to populate.
        summary_path (str): The path to the summary.json file.

    Returns:
        The populated test_run object.
    '''
    with open(summary_path, 'r', encoding="utf-8") as f:
        summary_data = json.load(f)
        statistics = summary_data.get("statistic") or {}
        if isinstance(statistics, list):
            statistics = statistics[0] if statistics else {}
        time_data = summary_data.get("time") or {}
        if isinstance(time_data, list):
            time_data = time_data[0] if time_data else {}
        summary_data["time"] = time_data
        test_run.scenario_qty = statistics.get("total", 0)
        test_run.passed_scenario = statistics.get("passed", 0)
        test_run.failed_scenario = statistics.get("failed", 0)
        test_run.broken_scenario = statistics.get("broken", 0)
        test_run.skipped_scenario = statistics.get("skipped", 0)
        test_run.timestamp_start = datetime.fromtimestamp((time_data.get('start') or 0)/1000.0).isoformat()
        test_run.timestamp_end = datetime.fromtimestamp((time_data.get('stop') or 0)/1000.0).isoformat()
        test_run.duration_ms = time_data.get('duration') or 0
        if version is not None:
            test_run.test_version = str(version)
        if allure_subfolder is not None:
            allure_start = datetime.fromtimestamp((time_data.get('start') or 0) / 1000.0).strftime("%Y-%m-%d_%H:%M:%S")
            test_run.allure_url = f"{ALLURE_BASE_URL}{allure_subfolder}/{allure_start}/index.html"
        
        test_run.total_failures = calculate_total_failures(test_run)
        if test_run.total_failures == 0:
            test_run.revision_result = "GO"
            test_run.revisioned = True
            test_run.revision_date = datetime.now().isoformat()
            test_run.revisioned_by = "SYSTEM"

    return test_run

def populate_test_executions(test_cases_dir: str, allure_url:str) -> list[Test_executions]:
    '''
    Populate a list of Test_executions objects based on the data found in the test cases directory.

    Args:
        test_cases_dir (str): The path to the directory containing test case result folders.
    Returns:
        A list of populated Test_executions objects.
    '''
    test_executions = []
    for scenario in os.listdir(test_cases_dir):
        with open(os.path.join(test_cases_dir, scenario), 'r', encoding="utf-8") as f:  
            test_execution_data = json.load(f)
            test_execution = Test_executions()
            test_execution.allure_id = test_execution_data.get("uid", "")
            test_execution.scenario_name = test_execution_data.get("name", "")
            test_execution.allure_report = test_execution_data
            test_execution.duration_ms = test_execution_data.get("time", {}).get("duration",0)
            test_execution.status = test_execution_data.get("status", "").upper()
            test_execution.error_message = test_execution_data.get("statusMessage", "")
            test_execution.allure_url = f"{allure_url}#suites/{test_execution_data.get('historyId', '')}/{test_execution_data.get('uid', '')}/"
            test_executions.append(test_execution) 
    return test_executions

def populate_test_suite(config: Dynaconf, test_suite: Test_suites = None) -> Test_suites:
    '''
    Populate a Test_suites object based on the mapped configurations values

    Args:
        suite_dir (str): The path to the directory containing the test suite data, used to obtain the suite name.
        config (Dynaconf): The configuration object.

    Returns:
        A populated Test_suites object.
    '''
    # Assuming the suite_dir name is the test_object name
    if not test_suite.test_type:
        test_suite.test_type = config.get(test_suite.test_object, {}).get("test_type", None)
    # Owner team can be set based on some logic or configuration
    test_suite.owner_team = config.get(test_suite.test_object, {}).get("owner_team", None)
    return test_suite


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


def get_test_type_from_behave_path(behave_path: str | None) -> str | None:
    # behave_path has the form src/<test_type>/<suite>, e.g. src/integration/wisp
    if not behave_path:
        return None
    parts = Path(behave_path).parts
    return parts[1] if len(parts) > 2 and parts[0] == 'src' else None


def get_latest_saved_suite_version(test_object: str, config: Dynaconf) -> Test_suites:
    # This function should implement the logic to retrieve the latest suite version and its uuid by test_object from the QA HUB API.
    api = config.get("qa_hub_apis", None).get("latest_suite_version", None)
    try:
        test_suite = requests.request(
            method=api.get("method"),
            url=api.get("url"),
            params={"test_object": test_object}
        )

        if test_suite.status_code != 200:
            if test_suite.status_code == 400:
                raise Exception(f"Failed to retrieve latest suite version for test_object: {test_object}. Response: {test_suite.text}")
            elif test_suite.status_code == 404:
                return None
            
    except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
        raise Exception(f"Failed to retrieve latest suite version for test_object: {test_object}. Error: {str(e)}")
    return Test_suites(**test_suite.json())

def save_test_suite(test_suite: Test_suites, config: Dynaconf):
    api = config.get("qa_hub_apis", None).get("save_test_suite", None)
    test_suite.id = ''
    try:
        test_suite_out = requests.request(
            method=api.get("method"),
            url=api.get("url"),
            headers={"Ocp-Apim-Subscription-Key": api.get("api_key", "")},
            json=test_suite.__dict__
        )
        if test_suite_out.status_code != 200:
            raise Exception(f"Failed to save test suite for test_object: {test_suite.test_object}. Response: {test_suite_out.status_code}: {test_suite_out.text}")

    except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
        raise Exception(f"Failed to save test suite for test_object: {test_suite.test_object}. Error: {str(e)}")
    
    return Test_suites(**test_suite_out.json())

def save_test_runs(test_run: Test_runs,  config: Dynaconf):
    """Save a test run with datetime fields serialized as ISO 8601 strings."""
    api = config.get("qa_hub_apis", None).get("save_test_runs", None)
    test_run.id = ''    
    test_run.suite_id = str(test_run.suite_id)
    try:
        test_run_out = requests.request(
            method=api.get("method"),
            url=api.get("url"),
            headers={"Ocp-Apim-Subscription-Key": api.get("api_key", "")},
            json=test_run.__dict__
        )
        if test_run_out.status_code != 200:
            raise Exception(f"Failed to save test run for test_run: {test_run}. Response: {test_run_out.status_code}: {test_run_out.text}")

    except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
        raise Exception(f"Failed to save test run for test_run: {test_run}. Error: {str(e)}")

    return Test_runs(**test_run_out.json())

def save_test_executions(test_executions: list[Test_executions],  config: Dynaconf):
    api = config.get("qa_hub_apis", None).get("save_test_executions", None)
    [setattr(te, 'id', '') for te in test_executions]
    try:
        test_executions_out = requests.request(
            method=api.get("method"),
            url=api.get("url"),
            headers={"Ocp-Apim-Subscription-Key": api.get("api_key", "")},
            json=[te.__dict__ for te in test_executions]
        )
        if test_executions_out.status_code != 200:
            raise Exception(f"Failed to save test executions. Response: {test_executions_out.status_code}: {test_executions_out.text}")

    except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
        raise Exception(f"Failed to save test executions. Error: {str(e)}")

    return [Test_executions(**te) for te in test_executions_out.json()]


def get_current_product_version(test_object: str, config: Dynaconf) -> str:
    version_api = config.get('product_versions_apis', None).get(test_object, None)

    if version_api is None:
        print(f"[INFO][get_current_product_version] No path for the current product version for test_object: {test_object}. Setting default: 0.0.1")
        return "0.0.1"

    try:
        current_product_obj = requests.request(method='GET',url=version_api)

        if current_product_obj.status_code != 200:
            print(f"[INFO][get_current_product_version] Failed to get current product version for test_object: {test_object}. Setting default: 0.0.1. Response: {current_product_obj.status_code}: {current_product_obj.text}")
            return "0.0.1"

        return current_product_obj.json().get("version", "0.0.1")
    except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
        print(f"[INFO][get_current_product_version] Failed to get current product version for test_object: {test_object}. Setting default: 0.0.1.")        
        return "0.0.1"


def main():
    parser = argparse.ArgumentParser(description='Populate tables with test run data.')
    parser.add_argument('--run-type', '-t', default='CRON', help='Type of run (CRON, MANUAL, CI_PIPELINE)')
    parser.add_argument('--env', '-e', default='DEV', help='ENV of the test run (DEV, UAT, PROD)')
    parser.add_argument('--suite', '-s',  help='Suite being tested')
    parser.add_argument('--test_type', '-tt',  help='Type of the suite being tested (integration, e2e, ecc...)')
    parser.add_argument('--origin', '-o', default='NRT', help='Origin of the test run (NRT, TAS, etc.)')

    args = parser.parse_args()


    processed_dir = "artifacts"
    if not os.path.isdir(processed_dir) or os.listdir(processed_dir) == []:
        print(f"[INFO][main] No processed reports found in {processed_dir}. Exiting.")
        return
      
    print(f"[INFO][main] Found processed reports in {processed_dir}.")

    os.environ['TARGET_ENV'] = args.env.lower()

    full_config = load_configurations(GITHUB_ROOT)
    with open(NRT_SUITES_FILE, 'r') as f:
        suites = json.load(f)

    for dir in sorted(os.listdir(processed_dir)):

        if args.suite and args.test_type and (dir != f"{args.suite}-{args.test_type}"):
            continue
            
        run_dir = os.path.join(processed_dir, dir)
        if os.path.isdir(run_dir):
            test_run = Test_runs()
            test_suite = Test_suites()
            test_executions = list()

            test_run.env = str(args.env).upper()
            test_run.trigger_type = str(args.run_type).upper()
            test_run.test_origin = str(args.origin).upper()


            nrt_suite = find_nrt_suite(dir, suites)

            if args.suite:
                test_suite.test_type = args.test_type
                test_suite.test_object = args.suite
            elif nrt_suite is not None:
                test_suite.test_object = nrt_suite.get('id')
            else:
                test_suite.test_object = str(dir)
            print(f"[INFO][main] Processing artifact directory {dir} as test_object {test_suite.test_object}.")


            # get the actual product version
            current_product_version = get_current_product_version(test_suite.test_object, full_config)
            # get the latest product version saved in the database for this suite
            latest_suite_version_obj = get_latest_saved_suite_version(test_suite.test_object, full_config)

            # if latest_version is not None and is smaller than the current version of the test, then fully populate the suite 
            # object and use the proper API to insert a new record in the DB.
            if (latest_suite_version_obj is None) or (latest_suite_version_obj is not None and latest_suite_version_obj.suite_version < current_product_version):
                print(f"[INFO][main] No suite found for test_object {test_suite.test_object} or the latest version is outdated. Creating and saving a new suite version.")
                test_suite.suite_version = current_product_version
                test_suite = populate_test_suite( full_config, test_suite)
                if not test_suite.test_type and nrt_suite is not None:
                    test_suite.test_type = get_test_type_from_behave_path(nrt_suite.get('behave_path'))
                latest_suite_version_obj = save_test_suite(test_suite, full_config)
                print(f"[INFO][main] Saved new suite version for test_object {test_suite.test_object}.")
           

            # Populate the test run object based on the summary.json file 
            test_run.suite_id = latest_suite_version_obj.id
            test_version = (nrt_suite or find_nrt_suite(test_suite.test_object.lower(), suites) or {}).get('version')
            test_run = populate_test_run(test_run, os.path.join(run_dir, SUMMARY_FILE_PATH), test_version, test_suite.test_object, nrt_suite.get('allure_subfolder') if nrt_suite else None)
            # Populating test executions based on the test cases JSON files
            if os.path.exists(os.path.join(run_dir, TEST_CASES_PATH)):
                test_executions = populate_test_executions(os.path.join(run_dir, TEST_CASES_PATH), test_run.allure_url)
            else:
                 test_executions = populate_test_executions(os.path.join(run_dir, ALLURE_RESULT_PATH), test_run.allure_url)
                 
            # Save the newly created test run in the database and get the generated ID to associate with test executions
            test_run = save_test_runs(test_run, full_config)
            print(f"[INFO][main] Saved new test run for test_object {latest_suite_version_obj.test_object} with run ID {test_run.id}")
            for te in test_executions:
                te.run_id = test_run.id
            # Save all the test executions in the database
            test_executions = save_test_executions(test_executions, full_config)
            print(f"[INFO][main] Saved all new test executions for test_object {latest_suite_version_obj.test_object} for run ID {test_run.id}")
          

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[ERROR][populate_tables] {str(e)}")
        raise
    