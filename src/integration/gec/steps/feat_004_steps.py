"""Behave steps for FEAT_004 - Recupero commissioni multi."""

from behave import given, then
from src.integration.gec.helper import _ensure_vars_container

LOGGER = __import__("logging").getLogger("gec.feat_004")
