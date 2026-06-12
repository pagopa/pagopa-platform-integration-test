import logging

from behave import given
from spid_auth import step_click_login_button
logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# GIVEN steps (Background)
# ──────────────────────────────────────────────
@given(u'L\'utente è autenticato')
def step_impl(context):
    step_click_login_button(context)