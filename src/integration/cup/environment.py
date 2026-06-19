import logging

from src.conf.configuration import settings
from src.conf.configuration import secrets
from src.conf.configuration import commondata


def before_all(context):
    context.settings = settings
    context.secrets = secrets
    context.commondata = commondata
    logging.basicConfig(level=logging.DEBUG)


def _reset_scenario_context(context):
    context.demand_status_code = None
    context.organization_fiscal_code = None
    context.fiscal_code = None
    context.notice_number = None


def before_scenario(context, scenario):
    _reset_scenario_context(context)


def after_scenario(context, scenario):
    _reset_scenario_context(context)


def before_step(context, step):
    context.running_step = step.name
