"""Shared Behave steps for FdR3 flows, payloads and assertions."""

import json
import logging
from datetime import datetime, timedelta, timezone

from behave import given, when, then

from src.integration.fdr3.utils_fdr import perform_fdr_action, resolve_fdr_action
from src.integration.fdr3.helper import (
    _ensure_vars_container,
    _get_client,
    _get_partner_client,
    _substitute_placeholders,
    step_unique_flow_date,
    _store_create_payload,
    _build_payments_payload,
    _get_request_payload,
    _flow_value,
    _send_request,
)
from src.utility.data_generators import generate_iuv, generate_uuid

LOGGER = logging.getLogger("fdr3")


@given("i sistemi sono operativi")
def step_systems_up(context):
    context.response = None


@given('un {field_type} di flusso di rendicontazione univoco chiamato {varname}')
def step_unique_flow_field(context, field_type: str, varname: str):
    _ensure_vars_container(context)
    today = datetime.today().astimezone(timezone.utc)

    if field_type in ("name", "nome"):
        psp = context.vars.get("psp")
        if psp is None:
            psp = getattr(context, "psp_id", None) or "PSP"
        value = (
            today.strftime("%Y-%m-%d")
            + str(psp)
            + "-"
            + today.strftime("%H%M%S%f")
        )
    elif field_type in ("date", "data"):
        value = today.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    else:
        raise AssertionError(f"Unsupported field_type '{field_type}' for unique FdR step")

    setattr(context, varname, value)
    context.vars[varname] = value




@given('una data di flusso di rendicontazione univoco chiamato {varname}')
def step_unique_flow_date_legacy(context, varname: str):
    return step_unique_flow_date(context, varname)




@given('un payload di creazione FdR {payload_name}')
def step_named_payload(context, payload_name: str):
    _store_create_payload(context, payload_name)


@given('che lo scenario "{scenario_name}" è stato eseguito con successo')
def step_prior_scenario_executed(context, scenario_name: str):
    scenario = next(
        (
            candidate
            for candidate in context.feature.scenarios
            if scenario_name in candidate.name
        ),
        None,
    )
    if scenario is None:
        raise AssertionError(
            f"Scenario '{scenario_name}' non trovato nella feature "
            f"'{context.feature.name}'"
        )

    steps_text = "".join(
        step.keyword
        + " "
        + step.name
        + "\n\"\"\"\n"
        + (step.text or "")
        + "\n\"\"\"\n"
        for step in scenario.steps
    )
    LOGGER.info(
        "Executing referenced scenario '%s' with steps:\n%s",
        scenario.name,
        steps_text,
    )
    context.execute_steps(steps_text)

@given('che il PSP deve inviare {n:d} pagamenti al flusso')
@given('che il PSP deve inviare {n:d} pagamento al flusso')
def step_set_tot_payments(context, n: int):
    _ensure_vars_container(context)
    context.tot_payments = n
    context.vars["number_of_payments"] = n


@given('che la somma totale dei pagamenti da inviare è {amount:d}')
def step_set_sum_payments(context, amount: int):
    _ensure_vars_container(context)
    context.sum_payments = amount
    context.vars["payments_amount"] = amount


@given("{partner} aggiunge {value} come {key} nei parametri di query")
@given("il {partner} aggiunge {value} come {key} nei parametri di query")
def step_partner_add_query_param(context, partner: str, value: str, key: str):
    """Generic step to add/override query parameters for a partner request.

    Examples handled:
      - l'organizzazione aggiunge ieri come createdGt nei parametri di query
      - l'organizzazione aggiunge 1 come page nei parametri di query
      - l'organizzazione aggiunge 99 come size nei parametri di query

    The partner token is accepted but not used for routing here; it documents
    who is adding the parameter. Value supports placeholders and special tokens
    like 'ieri' -> yesterday timestamp.
    """
    _ensure_vars_container(context)
    if not hasattr(context, "query_params"):
        context.query_params = {}

    val = value
    low = value.strip().lower()
    if low in ("ieri", "yesterday"):
        # ISO timezone-free format used elsewhere
        from datetime import timedelta

        val = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        # substitute placeholders like $flow_name$ or #psp# using helper
        try:
            val = _substitute_placeholders(value, context)
        except Exception:
            val = value
        # numeric conversion when appropriate
        if isinstance(val, str) and val.isdigit():
            val = int(val)
    # store into query_params using the raw key as provided
    context.query_params[key] = val




@when('il PSP aggiunge {number:d} pagamenti la cui somme è {amount} al flusso di rendicontazione {flow_name} come {payload}')
def step_build_payments_payload(context, number: int, amount: str, flow_name: str, payload: str):
    _ensure_vars_container(context)
    value = _build_payments_payload(number, float(amount))
    setattr(context, payload, json.dumps(value))
    context.payloads[payload] = value




@when('{partner} invia la richiesta di "{request}" con il payload "{payload_name}"')
def step_send_request(context, partner: str, request: str, payload_name: str):
    _send_request(context, partner, request, payload_name)


@when('{partner} invia la richiesta di "{request}" con il payload "{payload_name}" con subscription_key non valida')

def step_send_request_with_invalid_subscription_key(
    context,
    partner: str,
    request: str,
    payload_name: str,
):
    _send_request(context, partner, request, payload_name, invalid_key=True)



# -------------------- THEN steps --------------------

@then('{partner} riceve il codice di stato HTTP {status:d}')
def step_assert_status(context, partner: str, status: int):
    # partner parameter is accepted for reuse across different actors (es. 'il PSP', "l'organizzazione").
    # Implementation intentionally unchanged: it asserts the HTTP status of last response.
    assert hasattr(context, "response") and context.response is not None, "Nessuna risposta salvata in context.response"
    assert context.response.status_code == status, f"Expected HTTP {status} but got {context.response.status_code}: {context.response.text}"


@then('lo stato del flusso è "{state}"')
def step_assert_flow_state_alias(context, state: str):
    resp = getattr(context, "get_fdr_response", None) or getattr(context, "response", None)
    assert resp is not None, "Nessuna risposta disponibile per lo stato del flusso"
    try:
        body = resp.json()
    except Exception:
        raise AssertionError("Response non JSON")
    got = body.get("status") or body.get("state") or body.get("statusCode")
    assert got == state, f"Expected flow state '{state}' but got '{got}'"
