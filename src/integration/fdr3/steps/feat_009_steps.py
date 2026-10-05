from behave import given, then
import logging

from src.integration.fdr3.helper import _ensure_vars_container

LOGGER = logging.getLogger('fdr3.steps')


@given('la configurazione {field} è valorizzata come {field_key} nei parametri di query')
def step_query_field_as_field_key(context, field, field_key):
    _ensure_vars_container(context)
    if not hasattr(context, "query_params"):
        context.query_params = {}

    # Resolve value from common places: context.vars, context attributes, and snake_case variants
    value = None
    if hasattr(context, "vars") and isinstance(context.vars, dict):
        value = context.vars.get(field) or context.vars.get(field_key)
    if value is None:
        value = getattr(context, field, None) or getattr(context, field_key, None)
    if value is None:
        # try snake_case of field_key (e.g. pspId -> psp_id)
        snake = []
        for ch in field_key:
            if ch.isupper():
                snake.append('_')
                snake.append(ch.lower())
            else:
                snake.append(ch)
        snake_name = ''.join(snake).lstrip('_')
        if hasattr(context, "vars") and isinstance(context.vars, dict):
            value = context.vars.get(snake_name)
        if value is None:
            value = getattr(context, snake_name, None)

    context.query_params.setdefault(field_key, value)
    LOGGER.info("Set query_params: %s", context.query_params)


@given('la revisione del FdR è {rev:d}')
def step_set_revision(context, rev: int):
    context.expected_revision = rev


@then("l'organizzazione riceve pagina {page:d} con {entries:d} elementi come risposta di org_get_all_published_fdr")
def step_assert_page_and_entries_fdr(context, page: int, entries: int):
    assert hasattr(context, "response") and context.response is not None, "Nessuna risposta disponibile"
    try:
        body = context.response.json()
    except Exception:
        raise AssertionError("Response non JSON")

    # try common pagination fields
    got_page = None
    if isinstance(body, dict):
        got_page = body.get("page") or (body.get("pageable") and body.get("pageable").get("page")) or body.get("number")
        items = body.get("items") or body.get("fdrs") or body.get("content") or body.get("data")
    else:
        # body is list
        items = body
    if items is None:
        # try fallbacks
        items = []
    count = len(items) if isinstance(items, list) else 0
    if got_page is not None:
        try:
            got_page = int(got_page)
        except Exception:
            pass
    # If page info not present, assume page 1 when requesting page 1
    if got_page is None:
        got_page = context.query_params.get("page") if hasattr(context, "query_params") else None
    assert got_page == page, f"Expected page {page} but got {got_page}"
    assert count == entries, f"Expected {entries} entries but got {count}"


@then("l'organizzazione riceve pagina {page:d} con {entries:d} elementi come risposta di org_get_payments")
def step_assert_page_and_entries_payments(context, page: int, entries: int):
    assert hasattr(context, "response") and context.response is not None, "Nessuna risposta disponibile"
    try:
        body = context.response.json()
    except Exception:
        raise AssertionError("Response non JSON")

    items = None
    if isinstance(body, dict):
        items = body.get("payments") or body.get("items") or body.get("content") or body.get("data")
        got_page = body.get("page") or (body.get("pageable") and body.get("pageable").get("page")) or body.get("number")
    else:
        items = body
        got_page = None
    if items is None:
        items = []
    count = len(items) if isinstance(items, list) else 0
    if got_page is None:
        got_page = context.query_params.get("page") if hasattr(context, "query_params") else None
    assert int(got_page) == page, f"Expected page {page} but got {got_page}"
    assert count == entries, f"Expected {entries} entries but got {count}"
