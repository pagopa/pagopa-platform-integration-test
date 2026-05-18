"""
Behave environment hooks per i cart-test.

Delega before_all e before_scenario comuni ad api_test_environment,
aggiungendo il reset dello stato specifico del cart.
"""
from src.utility.api_test.api_test_environment import (
    before_all,
    before_scenario as _before_scenario_common,
)


def before_scenario(context, scenario):
    _before_scenario_common(context, scenario)
    context.notice_code = None
    context.fiscal_code = None
    context.cart_id = None
