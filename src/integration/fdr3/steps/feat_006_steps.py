from behave import given

from src.integration.fdr3.helper import _ensure_vars_container


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
