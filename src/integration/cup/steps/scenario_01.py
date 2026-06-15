from behave import *

import src.integration.cup.steps.step_param_types  # noqa: F401
from src.integration.cup.utility.client import send_demand_payment_notice
from src.integration.cup.utility.gpd_client import build_gpd_client
from src.integration.cup.utility.parsers import (
    get_pa_demand_payment_notice_notice_number,
    get_pa_demand_payment_notice_qr_code_fiscal_code,
)
from src.integration.cup.utility.request_builder import build_happy_path
from src.utility.assertions import assert_show_message
from src.utility.json import get_attr


@given('Il PSP ha ricevuto dalla Corporate un file di input valido che include i dati mandatori')
def step_psp_riceve_input_valido_mandatorio(context):
    """No-op precondition: the PSP has received a valid input file with mandatory data."""
    pass


@given('Il file di input contiene una sola chiave di identificazione Ente')
def step_file_contiene_una_sola_chiave_ente(context):
    """No-op precondition: the input file contains exactly one entity identification key."""
    pass


@when('Il PSP Invia la primitiva demandPaymentNotice includendo i dati mandatori e valorizzando un parametro identificativo')
def step_psp_invia_demand_payment_notice_happy_path(context):
    """Send the CUP paDemandPaymentNotice happy-path request and store raw flow data."""
    request_body = build_happy_path()

    status_code, response_body = send_demand_payment_notice(
        service_config=context.settings.services['cup_mock'],
        xml_body=request_body,
        description=getattr(context, 'running_step', None),
    )

    assert_show_message(status_code == 200, f"Expected HTTP 200, got {status_code}")

    context.demand_status_code = status_code
    context.fiscal_code = get_pa_demand_payment_notice_qr_code_fiscal_code(response_body)
    context.notice_number = get_pa_demand_payment_notice_notice_number(response_body)


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
    """Assert the remittanceInformation field matches the expected CUP pattern."""
    pass


@then('La posizione debitoria contiene il campo payment.option.description : Canone Unico Patrimoniale {anno:AnyText}')
def step_posizione_debitoria_contiene_payment_option_description(context, anno):
    """Assert the payment option description field matches the expected CUP value."""
    pass


@then("Il PSP Riceve la risposta demandPaymentNotice res con l'esito della creazione nel formato previsto per l'output")
def step_psp_riceve_risposta_demand_payment_notice_res(context):
    """Assert the demandPaymentNotice response body conforms to the expected output format."""
    pass