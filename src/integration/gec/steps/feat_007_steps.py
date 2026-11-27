"""Behave steps for FEAT_007 - Metodi di pagamento importo."""

from behave import given, then
from src.integration.gec.helper import _ensure_vars_container

LOGGER = __import__("logging").getLogger("gec.feat_007")
