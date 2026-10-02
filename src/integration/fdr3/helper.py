"""Utilities for FdR behave steps.

This module centralizes small helper functions used by step definition
modules under src.integration.fdr3.steps. Functions are internal helpers
(leading underscore) and intended to be imported from step modules as:

    from src.integration.fdr3.helper import _get_client, _ensure_vars_container

Functions:
- _get_client(context): prefer context.psp.rest.client then context.fdr.rest.client
- _ensure_vars_container(context): ensure context.vars and context.payloads exist
- _substitute_placeholders(text, context): substitute $var$ tokens from context.vars

Moved here from src/integration/fdr3/steps/helper.py to provide a single
repository-local helper package (no sys.path hacks required).
"""

from datetime import datetime

# Helper utilities

def _get_client(context):
    """Prefer PSP client (actor) if available, otherwise FDR client."""
    client = getattr(context, "psp", None)
    if client and getattr(context.psp, "rest", None) and getattr(context.psp.rest, "client", None):
        return context.psp.rest.client
    client = getattr(context, "fdr", None)
    if client and getattr(context.fdr, "rest", None) and getattr(context.fdr.rest, "client", None):
        return context.fdr.rest.client
    raise AssertionError("Nessun RestClient disponibile in context.psp.rest.client o context.fdr.rest.client")


def _get_partner_client(context, partner: str):
    """Return the client belonging to the partner named in the feature step."""
    actor = getattr(context, "psp", None) if partner.strip().upper() == "PSP" else getattr(context, "fdr", None)
    client = getattr(getattr(actor, "rest", None), "client", None)
    if client is None:
        raise AssertionError(f"Nessun RestClient configurato per il partner '{partner}'")
    return client


def _ensure_vars_container(context):
    if not hasattr(context, "vars"):
        context.vars = {}
    if not hasattr(context, "payloads"):
        context.payloads = {}


def _substitute_placeholders(text: str, context) -> str:
    """Replace $varname$ placeholders in the provided text using context.vars and common names.

    Supports keys directly on context (context.flow_name) and entries stored in context.vars.
    """
    result = text
    keys = set()
    # find simple $...$ occurrences
    idx = 0
    while True:
        start = result.find("$", idx)
        if start == -1:
            break
        end = result.find("$", start + 1)
        if end == -1:
            break
        key = result[start + 1 : end]
        keys.add(key)
        idx = end + 1
    for key in keys:
        val = None
        # first look into context.vars
        if hasattr(context, "vars") and key in context.vars:
            val = context.vars[key]
        # then look for direct context attributes
        elif hasattr(context, key):
            val = getattr(context, key)
        # basic fallback for names commonly used
        elif key == "flow_date":
            val = datetime.utcnow().strftime("%Y-%m-%d")
        # default numeric placeholders to 0 when not provided in context
        elif key in ("tot_payments", "sum_payments", "number_of_payments", "payments_amount", "totPayments", "sumPayments"):
            val = 0
        if val is None:
            # keep original token if not resolvable
            continue
        result = result.replace(f"${key}$", str(val))
        # Also support '#' style placeholders (#name#) used in some payload templates
        result = result.replace(f"#{key}#", str(val))
    return result
