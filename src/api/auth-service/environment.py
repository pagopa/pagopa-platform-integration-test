"""
Behave environment hooks per gli auth-service api tests.

Delega il caricamento delle variabili d'ambiente agli hook comuni degli api-test,
aggiungendo il reset dello stato condiviso usato dagli scenari auth-service.
"""
from src.utility.api_test.api_test_environment import (
    before_all,
    before_scenario as _before_scenario_common,
)


def before_scenario(context, scenario):
    _before_scenario_common(context, scenario)
    context.login_payload = None
    context.redirect_url = None
    context.auth_code = None
    context.state = None
    context.nonce = None
    context.session_token = None
    context.invalid_session_token = "invalid-session-token"
    context.user_profile = None