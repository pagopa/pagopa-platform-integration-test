from behave import when, then
from src.integration.fdr3.helper import _ensure_vars_container

@when('il PSP rimuove {n:d} pagamento dal flusso di rendicontazione {flow_var} come {payload}')
def step_build_delete_payments_payload(context, n: int, flow_var: str, payload: str):
    _ensure_vars_container(context)
    context.payloads[payload] = {
        "indexList": list(range(1, n + 1))
    }


@then('la risposta contiene {count:d} pagamenti')
def step_assert_payments_count(context, count: int):
    assert hasattr(context, "response") and context.response is not None
    try:
        body = context.response.json()
    except Exception:
        raise AssertionError("Risposta non in formato JSON")
    payments = body.get("payments") or body.get("items") or body.get("data") or []
    assert isinstance(payments, list)
    assert len(payments) == count, f"Aspettati {count} pagamenti ma ottenuti {len(payments)}"

