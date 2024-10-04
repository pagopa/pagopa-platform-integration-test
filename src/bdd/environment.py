import copy
import logging
from src.utility import constants
from src.conf.configuration import settings, secrets, commondata
from src.utility.constants import empty_flow_data


def before_all(context):
    # load settings and secrets into context
    context.settings = settings
    context.secrets = secrets

    # configure logging setup
    logging.basicConfig(level=logging.DEBUG)

def before_scenario(context, scenario):

    context.flow_data = copy.deepcopy(empty_flow_data)
    context.flow_data['action']['trigger_primitive']['name'] = constants.PRIMITIVE_NODOINVIARPT

def before_step(context, step):
    context.running_step = step.name