from behave import then

from src.integration.fdr3.helper import _ensure_vars_container

@then('la risposta contiene revision = {rev:d}')
def step_assert_revision(context, rev: int):
    resp = getattr(context, "get_fdr_response", None) or getattr(context, "response", None)
    assert resp is not None, "Nessuna risposta disponibile per l'asserzione"
    try:
        body = resp.json()
    except Exception:
        raise AssertionError("Risposta non in formato JSON")
    got = body.get("revision")
    _ensure_vars_container(context)
    if got is not None:
        context.vars["revision"] = got
    assert got == rev, f"Revisione attesa {rev} ma ottenuta {got}"


@then('la risposta contiene totPayments = {tot:d}')
def step_assert_tot_payments(context, tot: int):
    resp = getattr(context, "get_fdr_response", None) or getattr(context, "response", None)
    assert resp is not None, "Nessuna risposta disponibile per l'asserzione"
    try:
        body = resp.json()
    except Exception:
        raise AssertionError("Risposta non in formato JSON")
    got = body.get("totPayments")
    assert got == tot, f"totPayments atteso {tot} ma ottenuto {got}"

