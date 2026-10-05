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

import logging
import json
from datetime import datetime, timedelta, timezone
from src.utility.data_generators import generate_iuv, generate_uuid
from src.integration.fdr3.utils_fdr import perform_fdr_action, resolve_fdr_action

LOGGER = logging.getLogger("fdr3.helper")

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


def normalize_partner(partner: str) -> str:
    """Normalize partner textual variants to canonical keys.

    Examples:
      - "il PSP", "PSP" -> "psp"
      - "l'organizzazione", "organizzazione", "Organization" -> "organization"
      - "FDR" -> "fdr"

    The function returns a lowercase canonical token used by _get_partner_client
    to select the correct actor on the behave context.
    """
    if not partner:
        return ""
    p = partner.strip().lower()
    # remove common Italian articles and punctuation
    p = p.replace("l'", "").replace("il ", "").replace("lo ", "").replace("la ", "").strip()

    if "psp" in p:
        return "psp"
    if "organ" in p or "organization" in p or "organizzazione" in p or p in ("org", "organization"):
        return "organization"
    if "fdr" in p or "flow" in p:
        return "fdr"
    # fallback to raw alphanumeric token
    token = ''.join(ch for ch in p if ch.isalnum())
    return token or p


def _get_partner_client(context, partner: str):
    """Return the client belonging to the partner named in the feature step.

    Normalizes the partner string and logs the resolution for easier debugging.
    """
    canon = normalize_partner(partner)
    LOGGER.info("Resolving partner '%s' -> '%s'", partner, canon)

    actor = None
    if canon == "psp":
        actor = getattr(context, "psp", None)
    elif canon in ("organization", "org"):
        # Prefer an explicit organization actor if present, otherwise reuse the fdr actor
        actor = getattr(context, "organization", None) or getattr(context, "fdr", None)
    elif canon == "fdr":
        actor = getattr(context, "fdr", None)
    else:
        # attempt attribute with the canonical name
        actor = getattr(context, canon, None) or getattr(context, "fdr", None)

    client = getattr(getattr(actor, "rest", None), "client", None) if actor is not None else None
    if client is None:
        raise AssertionError(f"Nessun RestClient configurato per il partner '{partner}' (risolto come '{canon}')")
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


# ---------------------------------------------------------------------------
# Helpers moved from step definitions (shared non-step functions)
# ---------------------------------------------------------------------------

def step_unique_flow_date(context, varname: str):
    """Compatibility wrapper: previously defined in steps module.

    Produces a unique flow 'data' value and stores it in context.vars.
    """
    # Reuse the existing logic for a flow 'date' using timezone-aware UTC
    today = datetime.today().astimezone(timezone.utc)
    value = today.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    setattr(context, varname, value)
    if not hasattr(context, "vars"):
        context.vars = {}
    context.vars[varname] = value


def _store_create_payload(context, payload_name: str):
    _ensure_vars_container(context)
    raw = getattr(context, "text", None)
    if not raw:
        context.payloads[payload_name] = None
        return
    for key in ("tot_payments", "sum_payments", "totPayments", "sumPayments"):
        if (
            key not in context.vars
            and not hasattr(context, key)
        ):
            raw = raw.replace(f"${key}$", "1")
    processed = _substitute_placeholders(raw, context)
    try:
        obj = json.loads(processed)
    except json.JSONDecodeError:
        obj = processed
    context.payloads[payload_name] = obj


def _build_payments_payload(number: int, amount: float) -> dict:
    if number <= 0:
        raise AssertionError("Il numero di pagamenti deve essere maggiore di zero")
    single_amount = float(f"{float(amount) / number:.2f}")
    today = datetime.today().astimezone(timezone.utc)
    payments = []

    for index in range(number):
        pay_date = today - timedelta(days=index)
        payments.append(
            {
                "idTransfer": 1,
                "iuv": generate_iuv(),
                "iur": generate_uuid(),
                "index": index + 1,
                "pay": single_amount,
                "payStatus": "EXECUTED",
                "payDate": pay_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
            }
        )
    return {"payments": payments}


def _get_request_payload(context, payload_name=None):
    if payload_name is not None and isinstance(payload_name, str) and payload_name.lower() == "none":
        return None
    if payload_name is not None:
        payloads = getattr(context, "payloads", {}) or {}
        if payload_name not in payloads:
            if payload_name == "payments_payload":
                number = int(getattr(context, "tot_payments", 0) or 0)
                amount = float(getattr(context, "sum_payments", 0) or 0)
                if number > 0 and amount > 0:
                    return _build_payments_payload(number, amount)
            raise AssertionError(
                f"Nessun payload disponibile con nome '{payload_name}'"
            )
        payload = payloads[payload_name]
    else:
        payload = getattr(context, "text", None)
    if isinstance(payload, str):
        payload = json.loads(_substitute_placeholders(payload, context))
    return payload


def _flow_value(context, name):
    return context.vars.get(name) or getattr(context, name, None)


def _send_request(
    context,
    partner: str,
    request: str,
    payload_name: str,
    invalid_key: bool = False,
):
    action = resolve_fdr_action(request)
    client = _get_partner_client(context, partner)
    flow_name = _flow_value(context, "flow_name")
    flow_date = _flow_value(context, "flow_date")
    payload = _get_request_payload(context, payload_name)
    if invalid_key and action == "aggiunta pagamenti" and payload is None:
        number = int(getattr(context, "tot_payments", 0) or 3)
        amount = float(getattr(context, "sum_payments", 0) or (number * 100))
        payload = _build_payments_payload(number, amount)

    response = perform_fdr_action(
        client=client,
        context=context,
        action=action,
        flow_name=flow_name,
        flow_date=flow_date,
        payload_override=payload,
        omit_payload=payload is None,
        headers=(
            {"Ocp-Apim-Subscription-Key": "invalid-key"}
            if invalid_key
            else None
        ),
    )
    context.response = response

