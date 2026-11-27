"""Behave steps for FEAT_006 - Metodi di pagamento touchpoint device."""

from behave import given, then
from src.integration.gec.helper import _ensure_vars_container

LOGGER = __import__("logging").getLogger("gec.feat_006")
