from behave import *

import src.integration.cup.steps.step_param_types  # noqa: F401
from src.integration.cup.utility.client import send_demand_payment_notice
from src.integration.cup.utility.request_builder import build_happy_path


@given('Il PSP ha ricevuto dalla Corporate un file di input valido che include i dati mandatori')
def step_psp_riceve_input_valido_mandatorio(context):
    """No-op step"""
    pass


@given('Il file di input contiene una sola chiave di identificazione Ente')
def step_file_contiene_una_sola_chiave_ente(context):
    """No-op step"""
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

    context.flow_data['request']['body'] = request_body
    context.flow_data['response']['status_code'] = status_code
    context.flow_data['response']['body'] = response_body