"""Behave steps for FEAT_003 - Recupero commissioni PSP multi."""

from behave import then
from src.integration.gec.helper import _get_bundled_response

LOGGER = __import__("logging").getLogger("gec.feat_003")

