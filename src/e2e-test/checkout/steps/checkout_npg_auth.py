import logging
import random

from behave import given, when, then
from spid_auth import step_click_login_button
logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# GIVEN steps (Background)
# ──────────────────────────────────────────────
@given(u'The user is authenticated')
def step_impl(context):
    step_click_login_button(context)