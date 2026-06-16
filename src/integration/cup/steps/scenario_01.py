from behave import *
from datetime import datetime
import re

import src.integration.cup.steps.step_param_types  # noqa: F401
from src.integration.cup.utility.client import send_demand_payment_notice
from src.integration.cup.utility.gpd_client import build_gpd_client
from src.integration.cup.utility.parsers import (
    get_pa_demand_payment_notice_amount,
    get_pa_demand_payment_notice_company_name,
    get_pa_demand_payment_notice_fiscal_code_pa,
    get_pa_demand_payment_notice_notice_number,
    get_pa_demand_payment_notice_options,
    get_pa_demand_payment_notice_outcome,
    get_pa_demand_payment_notice_payment_description,
    get_pa_demand_payment_notice_payment_note,
    get_pa_demand_payment_notice_qr_code_fiscal_code,
    get_payment_option_descriptions,
    get_payment_option_transfer_remittance_values,
    resolve_cup_pattern,
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
    """Send paDemandPaymentNotice and store status plus raw response body in context."""
    request_body = build_happy_path()

    status_code, response_body = send_demand_payment_notice(
        service_config=context.settings.services['cup_mock'],
        xml_body=request_body,
        description=getattr(context, 'running_step', None),
    )

    assert_show_message(status_code == 200, f"Expected HTTP 200, got {status_code}")

    context.demand_status_code = status_code
    context.demand_response_body = response_body


@then("Il PSP Riceve la risposta demandPaymentNotice res con l'esito della creazione nel formato previsto per l'output")
def step_psp_riceve_risposta_demand_payment_notice_res(context):
    """Assert response mandatory fields exist and store key values in context."""
    response_body = getattr(context, "demand_response_body", None)
    assert_show_message(response_body is not None, "Expected demandPaymentNotice response body in context")

    outcome = get_pa_demand_payment_notice_outcome(response_body)
    fiscal_code = get_pa_demand_payment_notice_qr_code_fiscal_code(response_body)
    notice_number = get_pa_demand_payment_notice_notice_number(response_body)
    amount = get_pa_demand_payment_notice_amount(response_body)
    options = get_pa_demand_payment_notice_options(response_body)
    payment_note = get_pa_demand_payment_notice_payment_note(response_body)
    payment_description = get_pa_demand_payment_notice_payment_description(response_body)
    fiscal_code_pa = get_pa_demand_payment_notice_fiscal_code_pa(response_body)
    company_name = get_pa_demand_payment_notice_company_name(response_body)

    assert_show_message(bool(outcome), "Expected <outcome> in demandPaymentNotice response")
    assert_show_message(bool(fiscal_code), "Expected <qrCode>/<fiscalCode> in demandPaymentNotice response")
    assert_show_message(bool(notice_number), "Expected <qrCode>/<noticeNumber> in demandPaymentNotice response")
    assert_show_message(bool(amount), "Expected <paymentList>/<paymentOptionDescription>/<amount> in response")
    assert_show_message(bool(options), "Expected <paymentList>/<paymentOptionDescription>/<options> in response")
    assert_show_message(bool(payment_note), "Expected <paymentList>/<paymentOptionDescription>/<paymentNote> in response")
    assert_show_message(bool(payment_description), "Expected <paymentDescription> in demandPaymentNotice response")
    assert_show_message(bool(fiscal_code_pa), "Expected <fiscalCodePA> in demandPaymentNotice response")
    assert_show_message(bool(company_name), "Expected <companyName> in demandPaymentNotice response")

    context.fiscal_code = fiscal_code
    context.notice_number = notice_number


@then('Viene creata correttamente la posizione debitoria')
def step_viene_creata_posizione_debitoria(context):
    """Call GPD get-debt-position-by-IUV and assert the position status is VALID."""
    org_id = context.organization_fiscal_code
    notice_number = context.notice_number
    iuv = notice_number.lstrip('3') if notice_number else notice_number

    gpd = build_gpd_client(context.settings.services['gpd'], context.secrets)
    response = gpd.get_debt_position_by_iuv(org_id=org_id, iuv=iuv)

    assert_show_message(response.status_code == 200, f"GPD get-by-IUV expected 200, got {response.status_code}")
    payload = response.json()
    context.payment_options = payload.get("paymentOption", []) if isinstance(payload, dict) else []
    context.iuv = iuv
    status = get_attr(payload, "status")
    assert_show_message(status == "VALID", f"Expected debt position status VALID, got '{status}'")


@then('La posizione debitoria contiene il campo remittanceInformation: {pattern:AnyText}')
def step_posizione_debitoria_contiene_remittance_information(context, pattern):
    """Assert at least one remittanceInformation in paymentOption[].transfer[] matches the given pattern.

    Placeholders <IUV>, <CF_Debitore>, <anno> in pattern are resolved from context before matching.
    """
    payment_options = getattr(context, "payment_options", [])
    expected_iuv = getattr(context, "iuv", None)
    expected_debtor_fiscal_code = getattr(context, "debtor_fiscal_code", None)

    assert_show_message(bool(payment_options), "Expected context.payment_options to contain at least one item")
    assert_show_message(bool(expected_iuv), "Expected context.iuv to be available from previous steps")
    assert_show_message(
        bool(expected_debtor_fiscal_code),
        "Expected context.debtor_fiscal_code to be available from previous steps",
    )

    remittance_values = get_payment_option_transfer_remittance_values(payment_options)

    assert_show_message(
        bool(remittance_values),
        "Expected at least one remittanceInformation in paymentOption[].transfer[]",
    )

    current_year = str(datetime.now().year)
    resolved = resolve_cup_pattern(
        pattern,
        iuv=expected_iuv,
        debtor_fiscal_code=expected_debtor_fiscal_code,
        anno=current_year,
    )
    compiled_pattern = re.compile(rf"^{resolved}$")
    matching_remittance = next((value for value in remittance_values if compiled_pattern.match(value)), None)
    assert_show_message(
        matching_remittance is not None,
        f"Expected at least one remittanceInformation matching '{resolved}', got {remittance_values}",
    )


@then('La posizione debitoria contiene il campo paymentOption.description : {pattern:AnyText}')
def step_posizione_debitoria_contiene_payment_option_description(context, pattern):
    """Assert at least one paymentOption.description matches the given pattern.

    Placeholder <anno> in pattern is resolved to the current year before matching.
    """
    payment_options = getattr(context, "payment_options", [])

    assert_show_message(bool(payment_options), "Expected context.payment_options to contain at least one item")

    descriptions = get_payment_option_descriptions(payment_options)

    assert_show_message(bool(descriptions), "Expected at least one description in paymentOption[]")

    current_year = str(datetime.now().year)
    resolved = resolve_cup_pattern(
        pattern,
        iuv=getattr(context, "iuv", None),
        debtor_fiscal_code=getattr(context, "debtor_fiscal_code", None),
        anno=current_year,
    )
    compiled_pattern = re.compile(rf"^{resolved}$")
    has_valid_description = any(compiled_pattern.match(value) for value in descriptions)
    assert_show_message(
        has_valid_description,
        f"Expected at least one paymentOption.description matching '{resolved}', got {descriptions}",
    )

