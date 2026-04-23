"""
Behave environment hooks per gli eCommerce CDC api tests.

Delega il caricamento delle variabili d'ambiente agli hook comuni degli api-test,
aggiungendo il reset dello stato condiviso usato dagli scenari CDC.
"""
from src.utility.api_test.api_test_environment import (
    before_all,
    before_scenario as _before_scenario_common,
)


def before_scenario(context, scenario):
    _before_scenario_common(context, scenario)
    context.payment_method_id = None
    context.notice_code = None
    context.order_id = None
    context.correlation_id = None
    context.npg_correlation_id = None
    context.npg_session_id = None
    context.npg_field_id = None
    context.field_url = None
    context.transaction_id = None
    context.auth_token = None
    context.amount = None
    context.payment_method_description = None
    context.payment_method_name = None
