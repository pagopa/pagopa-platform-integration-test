from behave import when
from src.integration.fdr3.helper import _get_partner_client
from src.integration.fdr3.steps.feat_001_common_steps import _build_payments_payload
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
    json_body = _build_payments_payload(n, sum_payments)
    response = perform_fdr_action(
        client=client,
        context=context,
        action="add_payments",
        flow_name=flow_name,
        payload_override=json_body,
        headers={"Ocp-Apim-Subscription-Key": "invalid-key"},
    )
    context.response = response
