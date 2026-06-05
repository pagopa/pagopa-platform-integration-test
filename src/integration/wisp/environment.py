import copy
import logging
import time

from src.conf.configuration import commondata
from src.conf.configuration import secrets
from src.conf.configuration import settings
from src.integration.utility.wisp import constants
from src.integration.utility.wisp.constants import empty_flow_data

# Delay between scenarios (seconds) to reduce backend contention on UAT.
# Set to 0 to disable. Override via -D scenario_delay=<seconds> at runtime.
_DEFAULT_SCENARIO_DELAY = 5


def before_all(context):
    # load settings and secrets into context
    context.settings = settings
    context.secrets = secrets
    context.commondata = commondata

    # configure logging setup
    logging.basicConfig(level=logging.DEBUG)

    # scenario delay: allow override via -D scenario_delay=<seconds>
    context.scenario_delay = int(context.config.userdata.get('scenario_delay', _DEFAULT_SCENARIO_DELAY))


def before_scenario(context, scenario):
    context.flow_data = copy.deepcopy(empty_flow_data)
    context.flow_data['action']['trigger_primitive']['name'] = constants.PRIMITIVE_NODOINVIARPT

def after_scenario(context, scenario):
    # Trainer's shoulder rub for UAT between rounds — brief rest before the next bout.
    if context.scenario_delay > 0:
        time.sleep(context.scenario_delay)

def before_step(context, step):
    context.running_step = step.name
