from behave import *
import logging

import src.integration.cup.steps.step_param_types  # noqa: F401
from src.integration.utility.cup.client import CupClient
from src.integration.utility.cup.request_builder import build_happy_path


@given('Il PSP ha ricevuto dalla Corporate un file di input valido che include i dati mandatori')
def step_psp_riceve_input_valido_mandatorio(context):
    """Initialize a valid CUP input payload context for the happy-path scenario."""
    pass


@given('Il file di input contiene una sola chiave di identificazione Ente')
def step_file_contiene_una_sola_chiave_ente(context):
    """Confirm the happy-path input includes exactly one ente identification key."""
    pass


@when('Il PSP Invia la primitiva demandPaymentNotice includendo i dati mandatori e valorizzando un parametro identificativo')
def step_psp_invia_demand_payment_notice_happy_path(context):
    """Send the CUP paDemandPaymentNotice happy-path request and store raw flow data."""
    request_body = build_happy_path()

    cup_service = context.settings.services['cup_mock']
    soap_action = cup_service.get('soap_action')
    if soap_action:
        cup_client = CupClient(url=cup_service['url'], soap_action=soap_action)
    else:
        cup_client = CupClient(url=cup_service['url'])

    status_code, response_body = cup_client.demand_payment_notice(
        xml_body=request_body,
        description=getattr(context, 'running_step', None),
    )

    logging.debug('[demandPaymentNotice] status_code=%s | response_body=%s', status_code, response_body)

    context.flow_data['request']['body'] = request_body
    context.flow_data['response']['status_code'] = status_code
    context.flow_data['response']['body'] = response_body