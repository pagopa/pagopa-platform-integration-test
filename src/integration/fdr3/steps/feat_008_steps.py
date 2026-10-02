from behave import when
from src.integration.fdr3.helper import _get_partner_client
from src.integration.fdr3.utils_fdr import perform_fdr_action


@when('il {partner} invia la richiesta "Publish" con il payload "{payload_name}" con subscription_key non valida')
def step_publish_with_invalid_sub_key(context, partner: str, payload_name: str):
    client = _get_partner_client(context, partner)
    flow_name = context.vars.get("flow_name") or getattr(context, "flow_name", None)
    response = perform_fdr_action(
        client=client,
        context=context,
        action="publish",
        flow_name=flow_name,
        headers={"Ocp-Apim-Subscription-Key": "invalid-key"},
    )
    context.response = response
