import copy
import logging
import subprocess
import sys
import time

from src.conf.configuration import commondata
from src.conf.configuration import secrets
from src.conf.configuration import settings
from src.integration.wisp.utility import constants
from src.integration.wisp.utility.constants import empty_flow_data

# Delay between scenarios (seconds) to reduce backend contention on UAT.
# Set to 0 to disable. Override via -D scenario_delay=<seconds> at runtime.
_DEFAULT_SCENARIO_DELAY = 1

logger = logging.getLogger(__name__)


def before_all(context):
    # load settings and secrets into context
    context.settings = settings
    context.secrets = secrets
    context.commondata = commondata

    # configure logging setup
    logging.basicConfig(level=logging.DEBUG)

    # scenario delay: allow override via -D scenario_delay=<seconds>
    context.scenario_delay = int(context.config.userdata.get('scenario_delay', _DEFAULT_SCENARIO_DELAY))

    # Retry: re-run each failed scenario exactly once at the end of the run.
    # Disable via -D wisp_retry=false (also set internally to prevent recursive retries).
    context._wisp_retry = context.config.userdata.get('wisp_retry', 'true').lower() == 'true'
    context._wisp_failed_scenarios = []


def before_scenario(context, scenario):
    context.flow_data = copy.deepcopy(empty_flow_data)
    context.flow_data['action']['trigger_primitive']['name'] = constants.PRIMITIVE_NODOINVIARPT


def after_scenario(context, scenario):
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
    context.running_step = step.name
