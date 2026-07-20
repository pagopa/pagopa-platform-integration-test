from behave import *

import src.integration.cup.steps.step_param_types  # noqa: F401


@given('Il PSP ha ricevuto dalla Corporate un file di input non valido, contenente più parametri identificativi ({organizationFiscalCode:AnyText}, {istatCode:AnyText}, {catastalCode:AnyText})')
def step_psp_riceve_input_multi_parametri(context, organizationFiscalCode, istatCode, catastalCode):
    pass


@given('Il PSP ha ricevuto dalla Corporate un file di input non valido, contenente uno dei parametri identificativi ({organizationFiscalCode:AnyText}, {istatCode:AnyText}, {catastalCode:AnyText}) che non rispetta il formato sintattico previsto')
def step_psp_riceve_input_parametro_formato_sintattico_errato(context, organizationFiscalCode, istatCode, catastalCode):
    pass


@given('Il PSP ha ricevuto dalla Corporate un file di input valido, contenente uno dei parametri identificativi ({organizationFiscalCode:AnyText}, {istatCode:AnyText}, {catastalCode:AnyText}) non presente nella cache multi-livello')
def step_psp_riceve_input_parametro_non_in_cache(context, organizationFiscalCode, istatCode, catastalCode):
    pass


@when('Il PSP Invia la primitiva demandPaymentNotice valorizzando più di un parametro identificativo ({organizationFiscalCode:AnyText}, {istatCode:AnyText}, {catastalCode:AnyText})')
def step_psp_invia_demand_payment_notice_multi_identificativo(context, organizationFiscalCode, istatCode, catastalCode):
    pass


@when('Il PSP Invia la primitiva demandPaymentNotice valorizzando uno dei parametri identificativi ({organizationFiscalCode:AnyText}, {istatCode:AnyText}, {catastalCode:AnyText}) non rispettando il formato sintattico previsto')
def step_psp_invia_demand_payment_notice_formato_sintattico_errato(context, organizationFiscalCode, istatCode, catastalCode):
    pass


@when('Il PSP Invia la primitiva demandPaymentNotice valorizzando uno dei parametri identificativi ({organizationFiscalCode:AnyText}, {istatCode:AnyText}, {catastalCode:AnyText}) con un valore non presente nella cache multi-livello')
def step_psp_invia_demand_payment_notice_non_in_cache(context, organizationFiscalCode, istatCode, catastalCode):
    pass
