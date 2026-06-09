import copy
import logging

from src.conf.configuration import settings
from src.conf.configuration import secrets
from src.conf.configuration import commondata


EMPTY_FLOW_DATA = {
    'request': {
        'body': None,
    },
    'response': {
        'status_code': None,
        'body': None,
    }
}


def before_all(context):
    context.settings = settings
    context.secrets = secrets
    context.commondata = commondata
    logging.basicConfig(level=logging.DEBUG)


def before_scenario(context, scenario):
    context.flow_data = copy.deepcopy(EMPTY_FLOW_DATA)


def before_step(context, step):
    context.running_step = step.name
