import logging
import os

from src.conf.configuration import load_commondata
from src.conf.configuration import load_secrets
from src.conf.configuration import load_settings
from src.utility.constants import INTEGRATION_ROOT


def before_all(context):
    """Initialize suite configuration, secrets, and shared test data."""
    suite_name = "cup"
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
    logging.basicConfig(level=logging.DEBUG)


def _reset_scenario_context(context):
    """Reset scenario-scoped values to avoid cross-scenario leakage."""
    context.demand_status_code = None
    context.organization_fiscal_code = None
    context.fiscal_code = None
    context.notice_number = None


def before_scenario(context, scenario):
    """Reset scenario state before each scenario starts."""
    _reset_scenario_context(context)


def after_scenario(context, scenario):
    """Reset scenario state after each scenario completes."""
    _reset_scenario_context(context)


def before_step(context, step):
    """Store current step name for diagnostics and reporting."""
    context.running_step = step.name
