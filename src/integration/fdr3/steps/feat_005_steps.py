from behave import when
from src.integration.fdr3.helper import _get_partner_client
from src.integration.fdr3.utils_fdr import perform_fdr_action


@when('il {partner} invia la richiesta "Add payments" con il payload "{payload_name}" con subscription_key non valida')
def step_add_with_invalid_sub_key(context, partner: str, payload_name: str):
    # reuse helper from common
    client = _get_partner_client(context, partner)
    flow_name = context.vars.get("flow_name") or getattr(context, "flow_name", None)
    n = int(getattr(context, "tot_payments", None) or 0)
    if n <= 0:
        n = 3
    sum_payments = int(getattr(context, "sum_payments", None) or (n * 100))
    payments = [{"amount": max(1, sum_payments // n)} for _ in range(n)]
    if n > 0:
        diff = sum_payments - sum(p["amount"] for p in payments)
        payments[-1]["amount"] += diff
    json_body = {"payments": payments}
    response = perform_fdr_action(
        client=client,
        context=context,
        action="add_payments",
        flow_name=flow_name,
        payload_override=json_body,
        headers={"Ocp-Apim-Subscription-Key": "invalid-key"},
    )
    context.response = response
