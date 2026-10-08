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
    _ensure_vars_container(context)
    context.expected_revision = rev
    context.vars["revision"] = rev


@then("{partner} riceve pagina {page:d} con {entries:d} elementi come risposta")
@then("{partner} riceve pagina {page:d} con {entries:d} elemento come risposta")
def step_assert_page_and_entries(context, partner: str, page: int, entries: int):
    assert hasattr(context, "response") and context.response is not None, "Nessuna risposta disponibile"
    try:
        body = context.response.json()
    except ValueError as exc:
        raise AssertionError("Risposta non in formato JSON") from exc

    got_page = None
    if isinstance(body, dict):
        pageable = body.get("pageable") or {}
        got_page = next(
            (value for value in (body.get("page"), pageable.get("page"), body.get("number"))
             if value is not None),
            None,
        )
        items = next(
            (body[key] for key in ("payments", "items", "fdrs", "content", "data")
             if key in body and body[key] is not None),
            None,
        )
    else:
        items = body
    if got_page is None:
        got_page = context.query_params.get("page") if hasattr(context, "query_params") else None
    assert got_page is not None, "Nessuna pagina disponibile nella risposta o nei parametri di query"
    assert isinstance(items, list), "Nessuna lista di elementi disponibile nella risposta"
    count = len(items)
    assert int(got_page) == page, f"Pagina attesa {page} ma ottenuta {got_page}"
    assert count == entries, f"Elementi attesi {entries} ma ottenuti {count}"

