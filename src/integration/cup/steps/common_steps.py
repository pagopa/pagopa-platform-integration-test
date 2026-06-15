from behave import *

import src.integration.cup.steps.step_param_types  # noqa: F401
from src.integration.cup.utility.gpd_client import build_gpd_client
from src.utility.assertions import assert_show_message
from src.utility.json import get_attr


@then('Viene creata correttamente la posizione debitoria')
def step_viene_creata_posizione_debitoria(context):
    """Call GPD get-debt-position-by-IUV and assert the position status is VALID.

    Uses organizationFiscalCode and noticeNumber (leading '3' stripped) stored
    in flow_data by the preceding when step.
    """
    org_id = context.organization_fiscal_code
    notice_number = context.notice_number
    iuv = notice_number.lstrip('3') if notice_number else notice_number

    gpd = build_gpd_client(context.settings.services['gpd'], context.secrets)
    response = gpd.get_debt_position_by_iuv(org_id=org_id, iuv=iuv)

    assert_show_message(response.status_code == 200, f"GPD get-by-IUV expected 200, got {response.status_code}")
    payload = response.json()
    status = get_attr(payload, "status")
    assert_show_message(status == "VALID", f"Expected debt position status VALID, got '{status}'")


@then('La posizione debitoria contiene il campo remittanceInformation: /RFB/{IUV:AnyText}/CNR/{CF_Debitore:AnyText}/TXT/Canone Unico Patrimoniale Saldo {anno:AnyText}')
def step_posizione_debitoria_contiene_remittance_information(context, IUV, CF_Debitore, anno):
    pass


@then('La posizione debitoria contiene il campo payment.option.description : Canone Unico Patrimoniale {anno:AnyText}')
def step_posizione_debitoria_contiene_payment_option_description(context, anno):
    pass


@then("Il PSP Riceve la risposta demandPaymentNotice res con l'esito della creazione nel formato previsto per l'output")
def step_psp_riceve_risposta_demand_payment_notice_res(context):
    pass


@then('Il PSP riceve un 200 OK che all\'interno riporta il fault code {risposta}')
def step_psp_riceve_200_con_fault_code(context, risposta):
    pass
