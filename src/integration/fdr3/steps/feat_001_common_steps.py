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


def step_unique_flow_date(context, varname: str):
    step_unique_flow_field(context, "data", varname)


@given('una data di flusso di rendicontazione univoco chiamato {varname}')
def step_unique_flow_date_legacy(context, varname: str):
    return step_unique_flow_date(context, varname)


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


@when('il PSP aggiunge {number:d} pagamenti la cui somme è {amount} al flusso di rendicontazione {flow_name} come {payload}')
def step_build_payments_payload(context, number: int, amount: str, flow_name: str, payload: str):
    _ensure_vars_container(context)
    value = _build_payments_payload(number, float(amount))
    setattr(context, payload, json.dumps(value))
    context.payloads[payload] = value


def _get_request_payload(context, payload_name=None):
    if payload_name is not None and payload_name.lower() == "none":
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


@when('il {partner} invia la richiesta "{request}" con il payload "{payload_name}"')
def step_send_request(context, partner: str, request: str, payload_name: str = None):
    action = resolve_fdr_action(request)
    client = _get_partner_client(context, partner)
    flow_name = _flow_value(context, "flow_name")
    flow_date = _flow_value(context, "flow_date")
    payload = _get_request_payload(context, payload_name)
    response = perform_fdr_action(
        client=client,
        context=context,
        action=action,
        flow_name=flow_name,
        flow_date=flow_date,
        payload_override=payload,
        omit_payload=payload is None,
    )
    context.response = response




# -------------------- THEN steps --------------------

@then('il PSP riceve il codice di stato HTTP {status:d}')
def step_assert_status(context, status: int):
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
