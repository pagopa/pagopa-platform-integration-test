import logging

from behave import given
from src.e2e.checkout.steps.spid_auth import step_click_login_button
logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# GIVEN steps (Background)
# ──────────────────────────────────────────────
@given(u'L\'utente è autenticato')
def step_impl(context):
    """Authenticate the user through the shared SPID login step."""
    step_click_login_button(context)