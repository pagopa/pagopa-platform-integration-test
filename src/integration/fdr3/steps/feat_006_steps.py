from behave import when, given
from src.integration.fdr3.helper import _ensure_vars_container, _get_partner_client
from src.integration.fdr3.utils_fdr import perform_fdr_action


@given('il PSP imposta un {field} non valido')
def step_set_invalid_flow_name(context, field: str):
    _ensure_vars_container(context)
    psp = context.vars.get("psp") or getattr(context, "psp_id", None)
    if not psp:
        raise AssertionError("Configurazione PSP non disponibile")

    if field == "flow_name":
        flow_name = f"2999-10-25{psp}-99999999999"
    else:
        flow_name = "2999-10-2500000000000-99999999999"

    context.vars["flow_name"] = flow_name
    setattr(context, "flow_name", flow_name)


@when('il {partner} invia la richiesta "Delete flow" con il payload "{payload_name}" con subscription_key non valida')
def step_delete_with_invalid_sub_key(context, partner: str, payload_name: str):
    client = _get_partner_client(context, partner)
    flow_name = context.vars.get("flow_name") or getattr(context, "flow_name", None)
    response = perform_fdr_action(
        client=client,
        context=context,
        action="delete_flow",
        flow_name=flow_name,
        headers={"Ocp-Apim-Subscription-Key": "invalid-key"},
    )
    context.response = response
