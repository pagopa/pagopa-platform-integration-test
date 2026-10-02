from behave import then


@then('la lista dei flussi restituita non contiene il flusso con fdr = "{flow_name}"')
def step_assert_flow_not_in_list(context, flow_name: str):
    assert hasattr(context, "response") and context.response is not None
    try:
        body = context.response.json()
    except Exception:
        raise AssertionError("Response non JSON")
    items = body.get("items") or body.get("flows") or body
    names = [it.get("fdr") if isinstance(it, dict) else None for it in items] if isinstance(items, list) else []
    assert flow_name not in names, f"Found flow {flow_name} in published list"
