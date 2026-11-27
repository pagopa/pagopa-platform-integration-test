"""Behave steps for FEAT_002 - Recupero delle commissioni."""

from behave import given, then
from src.integration.gec.helper import _ensure_vars_container

LOGGER = __import__("logging").getLogger("gec.feat_002")
