import json
import time
import os
import sys
from datetime import datetime
from typing import Dict, Any

# Ensure repository root is on sys.path so "src" packages are importable when behave
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from behave import given, when, then

from src.integration.fdr3.utils_fdr import perform_fdr_action


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
        if val is None:
            # keep original token if not resolvable
            continue
        result = result.replace(f"${key}$", str(val))
    return result


# -------------------- GIVEN steps --------------------

@given("i sistemi sono operativi")
def step_systems_up(context):
    # No-op: environment hooks should build clients; this step documents readiness
    context.response = None


@given('il PSP "{psp_name}" con pspId "{psp_id}" correttamente censito a sistema')
def step_psp_registered(context, psp_name: str, psp_id: str):
    # Store PSP identification in context for payload generation/debug
    context.psp_name = psp_name
    context.psp_id = psp_id


@given('un nome di flusso di rendicontazione univoco chiamato {varname}')
def step_unique_flow_name(context, varname: str):
    _ensure_vars_container(context)
    unique = f"{varname}-{int(time.time()*1000)}"
    context.vars[varname] = unique
    # also set attribute for backwards compatibility
    setattr(context, varname, unique)


@given('una data del flusso univoca chiamata {varname}')
def step_unique_flow_date(context, varname: str):
    _ensure_vars_container(context)
    date = datetime.utcnow().strftime("%Y-%m-%d")
    context.vars[varname] = date
    setattr(context, varname, date)


@given('un payload di creazione FdR')
def step_payload(context):
    """Accepts a docstring JSON payload in the step and stores it under context.payloads['payload'].

    The docstring may contain placeholders like $flow_name$ and $flow_date$ which will
    be substituted when the payload is used. If multiple named payloads are needed, they
    can still be added directly to context.payloads by other steps, but the canonical
    Gherkin step now always stores the docstring under 'payload'.
    """
    _ensure_vars_container(context)
    raw = getattr(context, "text", None)
    if not raw:
        context.payloads['payload'] = None
        return
    processed = _substitute_placeholders(raw, context)
    try:
        obj = json.loads(processed)
    except Exception:
        # Keep raw string if not valid JSON
        obj = processed
    context.payloads['payload'] = obj


# No-op step used by features that reference prior scenarios
@given('che lo scenario "{scenario_name}" è stato eseguito con successo')
def step_prior_scenario_executed(context, scenario_name: str):
    # This step is a synchronization hint in the feature; it's a no-op here.
    context.prior_scenario = scenario_name


@given('che il PSP deve inviare {n:d} pagamenti al flusso')
def step_set_tot_payments(context, n: int):
    # store for use by the add_payments step
    context.tot_payments = n


@given('che la somma totale dei pagamenti da inviare è {amount:d}')
def step_set_sum_payments(context, amount: int):
    context.sum_payments = amount


# -------------------- WHEN steps --------------------

@when('il PSP invia la richiesta di creazione flusso tramite l\'API "{api_name}"')
def step_send_create(context, api_name: str):
    client = _get_client(context)
    # Choose payload: prefer 'payload', then common named payloads, else first available
    payload = None
    pmap = getattr(context, 'payloads', {}) or {}
    if 'payload' in pmap:
        payload = pmap.get('payload')
    elif 'create_1_payload' in pmap:
        payload = pmap.get('create_1_payload')
    elif 'create_2_payload' in pmap:
        payload = pmap.get('create_2_payload')
    else:
        # take the first value if any
        for v in pmap.values():
            payload = v
            break
    # Substitute placeholders in string payloads
    if isinstance(payload, str):
        payload = json.loads(_substitute_placeholders(payload, context))
    response = perform_fdr_action(
        client=client,
        action="create",
        flow_name=context.vars.get("flow_name") or getattr(context, "flow_name", None),
        flow_date=context.vars.get("flow_date") or getattr(context, "flow_date", None),
        payload_override=payload,
    )
    context.response = response




@when('il PSP invia la richiesta di aggiunta pagamenti (API "{api_name}") con {n:d} pagamenti per il flusso "{flow_var}"')
def step_add_n_payments(context, api_name: str, n: int, flow_var: str):
    client = _get_client(context)
    flow_name = context.vars.get(flow_var) or getattr(context, flow_var, None)
    # default sum: look for context.tot_payments or use n*100
    sum_payments = getattr(context, "sum_payments", None) or getattr(context, "sumPayments", None) or n * 100
    response = perform_fdr_action(
        client=client,
        action="add_payments",
        flow_name=flow_name,
        n_payments=n,
        sum_payments=sum_payments,
    )
    context.response = response


@when('il PSP invia la richiesta di pubblicazione (API "{api_name}")')
def step_publish(context, api_name: str):
    client = _get_client(context)
    flow_name = context.vars.get("flow_name") or getattr(context, "flow_name", None)
    response = perform_fdr_action(client=client, action="publish", flow_name=flow_name)
    context.response = response


@when('il PSP invia la richiesta di cancellazione del flusso (API "{api_name}")')
def step_delete_flow(context, api_name: str):
    client = _get_client(context)
    flow_name = context.vars.get("flow_name") or getattr(context, "flow_name", None)
    response = perform_fdr_action(client=client, action="delete_flow", flow_name=flow_name)
    context.response = response


@when('il PSP richiede i dettagli del flusso creato (API "{api_name}")')
def step_get_created_fdr(context, api_name: str):
    client = _get_client(context)
    flow_name = context.vars.get("flow_name") or getattr(context, "flow_name", None)
    response = perform_fdr_action(client=client, action="get_published", flow_name=flow_name)
    context.get_fdr_response = response


@when('il PSP richiede i pagamenti creati (API "{api_name}")')
def step_get_created_payments(context, api_name: str):
    client = _get_client(context)
    flow_name = context.vars.get("flow_name") or getattr(context, "flow_name", None)
    response = perform_fdr_action(client=client, action="get_created_payments", flow_name=flow_name)
    context.response = response


@when('il PSP invia la richiesta di rimozione di {n:d} pagamento per il flusso "{flow_var}"')
def step_delete_payments(context, n: int, flow_var: str):
    client = _get_client(context)
    flow_name = context.vars.get(flow_var) or getattr(context, flow_var, None)
    response = perform_fdr_action(client=client, action="delete_payments", flow_name=flow_name, n_payments=n)
    context.response = response


# -------------------- THEN steps --------------------

@then('il PSP riceve il codice di stato HTTP {status:d}')
def step_assert_status(context, status: int):
    assert hasattr(context, "response") and context.response is not None, "Nessuna risposta salvata in context.response"
    assert context.response.status_code == status, f"Expected HTTP {status} but got {context.response.status_code}: {context.response.text}"


@then('il flusso viene creato in stato "{state}"')
def step_assert_flow_state(context, state: str):
    assert hasattr(context, "response") and context.response is not None, "Nessuna risposta salvata in context.response"
    try:
        body = context.response.json()
    except Exception:
        raise AssertionError("Response non JSON")
    got = body.get("status") or body.get("state") or body.get("statusCode")
    assert got == state, f"Expected flow state '{state}' but got '{got}'"


# Alias: published vs created wording
@when('il PSP richiede i dettagli del flusso pubblicato (API "{api_name}")')
def step_get_published_fdr_alias(context, api_name: str):
    return step_get_created_fdr(context, api_name)


@then('la risposta contiene revision = {rev:d}')
def step_assert_revision(context, rev: int):
    resp = getattr(context, "get_fdr_response", None) or getattr(context, "response", None)
    assert resp is not None, "Nessuna risposta disponibile per l'asserzione"
    try:
        body = resp.json()
    except Exception:
        raise AssertionError("Response non JSON")
    got = body.get("revision")
    assert got == rev, f"Expected revision {rev} but got {got}"


@then('la risposta contiene totPayments = {tot:d}')
def step_assert_tot_payments(context, tot: int):
    resp = getattr(context, "get_fdr_response", None) or getattr(context, "response", None)
    assert resp is not None, "Nessuna risposta disponibile per l'asserzione"
    try:
        body = resp.json()
    except Exception:
        raise AssertionError("Response non JSON")
    got = body.get("totPayments") or body.get("totPayments")
    assert got == tot, f"Expected totPayments {tot} but got {got}"


@then('{count:d} pagamenti sono restituiti nella risposta')
def step_assert_payments_count(context, count: int):
    assert hasattr(context, "response") and context.response is not None
    try:
        body = context.response.json()
    except Exception:
        raise AssertionError("Response non JSON")
    payments = body.get("payments") or body.get("items") or []
    assert isinstance(payments, list)
    assert len(payments) == count, f"Expected {count} payments but got {len(payments)}"


@then('la lista dei flussi restituita non contiene il flusso con fdr = "{flow_name}"')
def step_assert_flow_not_in_list(context, flow_name: str):
    assert hasattr(context, "response") and context.response is not None
    try:
        body = context.response.json()
    except Exception:
        raise AssertionError("Response non JSON")
    items = body.get("items") or body.get("flows") or body
    # items expected to be iterable of dicts
    names = [it.get("fdr") if isinstance(it, dict) else None for it in items] if isinstance(items, list) else []
    assert flow_name not in names, f"Found flow {flow_name} in published list"


@then('il sistema aggiorna correttamente i campi "totPayments" e "sumPayments" del flusso')
def step_assert_tot_and_sum_updated(context):
    """Fetch current flow data and assert totPayments and sumPayments equal expected values.

    Expected = (initial in create payload) + values set in context via given steps.
    """
    client = _get_client(context)
    flow_name = context.vars.get("flow_name") or getattr(context, "flow_name", None)

    # determine initial values from the payload used to create the flow if available
    initial_tot = 0
    initial_sum = 0
    # look for common payload names
    for key in ("create_1_payload", "create_2_payload", "payload"):
        p = getattr(context, "payloads", {}).get(key) if hasattr(context, "payloads") else None
        if isinstance(p, dict):
            initial_tot = int(p.get("totPayments", initial_tot) or initial_tot)
            initial_sum = int(p.get("sumPayments", initial_sum) or initial_sum)
            break

    added_tot = int(getattr(context, "tot_payments", 0) or 0)
    added_sum = int(getattr(context, "sum_payments", 0) or 0)

    expected_tot = initial_tot + added_tot
    expected_sum = initial_sum + added_sum

    # fetch current published/created flow
    resp = perform_fdr_action(client=client, action="get_published", flow_name=flow_name)
    try:
        body = resp.json()
    except Exception:
        raise AssertionError("Response non JSON when fetching flow for verification")

    got_tot = int(body.get("totPayments") or 0)
    got_sum = int(body.get("sumPayments") or 0)

    assert got_tot == expected_tot, f"Expected totPayments {expected_tot} but got {got_tot}"
    assert got_sum == expected_sum, f"Expected sumPayments {expected_sum} but got {got_sum}"


# Generic catch-all for many "Dato che ..." lines used as sync hints in features
@given('che {desc}')
def step_generic_che(context, desc: str):
    # no-op: used by features to express preconditions or previous steps
    context.last_given_desc = desc


# Alias: allow feature wording with 'nuova data' too
@given('una nuova data del flusso univoca chiamata {varname}')
def step_unique_flow_date_alias(context, varname: str):
    return step_unique_flow_date(context, varname)


@given('la revisione del FdR è {rev:d}')
def step_set_expected_revision(context, rev: int):
    # store expected revision for later assertions
    context.expected_revision = rev


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


# Configuration precondition aliases (no-op, set flags for potential query use)
@given("la configurazione dell'organizzazione è valorizzata come organizationId nei parametri di query")
def step_config_org_query(context):
    context.query_organization = True


@given("la configurazione del PSP è valorizzata come flow_name nei parametri di query")
def step_config_psp_query(context):
    context.query_psp_as_flow_name = True


# When: get all published flows
@when('il PSP richiede la lista dei flussi pubblicati (API "{api_name}")')
def step_get_all_published(context, api_name: str):
    client = _get_client(context)
    # allow query flags influence if needed by perform_fdr_action
    response = perform_fdr_action(client=client, action="get_all_published", flow_name=context.vars.get("flow_name"))
    context.response = response


# Then: alias for payments count wording used in some features
@then('la risposta contiene {count:d} pagamenti')
def step_assert_payments_count_alias(context, count: int):
    return step_assert_payments_count(context, count)
