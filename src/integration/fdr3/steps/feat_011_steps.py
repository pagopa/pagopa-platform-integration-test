from behave import then
import logging
from datetime import datetime

from src.integration.fdr3.helper import _ensure_vars_container

LOGGER = logging.getLogger('fdr3.steps')


@then("l'organizzazione riceve il codice di stato HTTP {status:d}")
def step_assert_status_for_org_get_all(context, status: int):
    assert hasattr(context, "response") and context.response is not None, "Nessuna risposta salvata in context.response"
    assert context.response.status_code == status, f"Codice di stato atteso {status} ma ottenuto {context.response.status_code}: {context.response.text}"


@then("l'organizzazione riceve tutti i FdR con pspId uguale al valore di pspId nei parametri di query")
def step_assert_all_fdr_same_psp_queryparam(context):
    _ensure_vars_container(context)
    assert hasattr(context, "response") and context.response is not None, "Nessuna risposta disponibile"
    try:
        body = context.response.json()
    except Exception:
        raise AssertionError("Risposta non in formato JSON")

    # find items list
    if isinstance(body, dict):
        items = body.get("data") or body.get("fdrs") or body.get("items") or body.get("content")
    else:
        items = body
    if items is None:
        items = []

    # determine expected pspId from query_params or context
    expected = None
    if hasattr(context, "query_params") and isinstance(context.query_params, dict):
        expected = context.query_params.get("pspId")
    if expected is None and hasattr(context, "vars") and isinstance(context.vars, dict):
        expected = context.vars.get("psp") or context.vars.get("pspId")
    if expected is None:
        expected = getattr(context, "psp_id", None)

    assert expected is not None, "Valore atteso pspId non trovato nel contesto"

    for i, it in enumerate(items):
        psp_val = it.get("pspId") if isinstance(it, dict) else None
        assert str(psp_val) == str(expected), f"Elemento index {i} ha pspId={psp_val}, aspettato={expected}"


@then("l'organizzazione riceve tutti i FdR con published > publishedGt")
def step_assert_all_fdr_published_gt(context):
    _ensure_vars_container(context)
    assert hasattr(context, "response") and context.response is not None, "Nessuna risposta disponibile"
    try:
        body = context.response.json()
    except Exception:
        raise AssertionError("Risposta non in formato JSON")

    if isinstance(body, dict):
        items = body.get("data") or body.get("fdrs") or body.get("items") or body.get("content")
    else:
        items = body
    if items is None:
        items = []

    if not (hasattr(context, "query_params") and isinstance(context.query_params, dict)):
        raise AssertionError("Nessun query_params disponibile per publishedGt")
    published_gt = context.query_params.get("publishedGt")
    assert published_gt is not None, "Parametro publishedGt non impostato nei query_params"

    def _parse_iso(s):
        if s is None:
            return None
        if isinstance(s, (int, float)):
            # epoch
            return datetime.utcfromtimestamp(float(s))
        if isinstance(s, str) and s.endswith('Z'):
            s2 = s[:-1]
        else:
            s2 = s
        try:
            return datetime.fromisoformat(s2)
        except Exception:
            # try without microseconds
            from datetime import datetime as _dt
            for fmt in ("%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S"):
                try:
                    return _dt.strptime(s2, fmt)
                except Exception:
                    continue
            raise

    parsed_gt = _parse_iso(str(published_gt))

    for i, it in enumerate(items):
        pub = None
        if isinstance(it, dict):
            pub = it.get("published") or it.get("created") or it.get("updated")
        assert pub is not None, f"Elemento index {i} non contiene campo 'published'"
        parsed_pub = _parse_iso(str(pub))
        assert parsed_pub > parsed_gt, f"Elemento index {i} ha published={parsed_pub} non maggiore di publishedGt={parsed_gt}"


@then("l'organizzazione riceve tutti i FdR con lo stesso pspId")
def step_assert_all_fdr_same_psp_short(context):
    """Short alias used by some features — delegates to the full query-param-aware check."""
    return step_assert_all_fdr_same_psp_queryparam(context)

