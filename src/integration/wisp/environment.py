import copy
import logging
import os
import subprocess
import sys
import time

from src.conf.configuration import load_commondata
from src.conf.configuration import load_secrets
from src.conf.configuration import load_settings
from src.utility.constants import INTEGRATION_ROOT
from src.integration.wisp.utility import constants
from src.integration.wisp.utility.constants import empty_flow_data

# Delay between scenarios (seconds) to reduce backend contention on UAT.
# Set to 0 to disable. Override via -D scenario_delay=<seconds> at runtime.
_DEFAULT_SCENARIO_DELAY = 1

logger = logging.getLogger(__name__)


def before_all(context):
    """Initialize suite configuration, secrets, common data, and retry controls."""
    # load settings and secrets into context
    suite_name = "wisp"
    target_env = os.getenv("TARGET_ENV") or "uat"

    os.environ["TARGET_ENV"] = str(target_env)
    os.environ["suite"] = suite_name

    context.settings = load_settings(config_folder_root=INTEGRATION_ROOT)
    context.secrets = load_secrets(
        suite=suite_name,
        target_env=target_env,
        settings=context.settings,
    )
    context.commondata = load_commondata(config_folder_root=INTEGRATION_ROOT)

    # configure logging setup
    logging.basicConfig(level=logging.DEBUG)

    # scenario delay: allow override via -D scenario_delay=<seconds>
    context.scenario_delay = int(context.config.userdata.get('scenario_delay', _DEFAULT_SCENARIO_DELAY))

    # Retry: re-run each failed scenario exactly once at the end of the run.
    # Disable via -D wisp_retry=false (also set internally to prevent recursive retries).
    context._wisp_retry = context.config.userdata.get('wisp_retry', 'true').lower() == 'true'
    context._wisp_failed_scenarios = []


def before_scenario(context, scenario):
    """Reset mutable scenario data before each scenario starts."""
    context.flow_data = copy.deepcopy(empty_flow_data)
    context.flow_data['action']['trigger_primitive']['name'] = constants.PRIMITIVE_NODOINVIARPT


def after_scenario(context, scenario):
    """Track failed scenarios and apply optional inter-scenario delay."""
    # Track failed scenarios for end-of-run retry.
    if context._wisp_retry and scenario.status == 'failed':
        context._wisp_failed_scenarios.append((scenario.filename, scenario.line))

    # Trainer's shoulder rub for UAT between rounds — brief rest before the next bout.
    if context.scenario_delay > 0:
        time.sleep(context.scenario_delay)


def after_all(context):
    """Re-run each failed scenario exactly once (no cascading retries)."""
    if not context._wisp_retry or not context._wisp_failed_scenarios:
        return

    logger.info("=== WISP RETRY: re-running %d failed scenario(s) ===", len(context._wisp_failed_scenarios))
    for feature_file, line in context._wisp_failed_scenarios:
        location = f"{feature_file}:{line}"
        # Pass wisp_retry=false to prevent recursive retries in the sub-run.
        cmd = [sys.executable, '-m', 'behave', location, '-D', 'wisp_retry=false']
        # Forward any userdata overrides from the original run.
        for key, val in context.config.userdata.items():
            if key != 'wisp_retry':
                cmd += ['-D', f'{key}={val}']
        logger.info("WISP RETRY: running %s", location)
        result = subprocess.run(cmd)
        status = 'PASSED' if result.returncode == 0 else 'FAILED'
        logger.info("WISP RETRY: %s -> %s", location, status)


def before_step(context, step):
    """Store current step name for diagnostics and reporting."""
    context.running_step = step.name
