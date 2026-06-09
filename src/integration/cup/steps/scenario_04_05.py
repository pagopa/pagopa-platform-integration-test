from behave import *

import src.integration.cup.steps.step_param_types  # noqa: F401


@given('Il PSP ha ricevuto dalla Corporate un file di input non valido, in cui sono assenti uno o più campi mandatori ({debtorFiscalCode:AnyText}, {debtorFullName:AnyText}, {amount:AnyText})')
def step_psp_riceve_input_campi_obbligatori_mancanti(context, debtorFiscalCode, debtorFullName, amount):
    pass


@given('Il PSP ha ricevuto dalla Corporate un file di input non valido, in cui uno dei campi mandatori ({amount:AnyText}, {debtorFiscalCode:AnyText}) è valorizzato con un formato errato')
def step_psp_riceve_input_formato_campo_errato(context, amount, debtorFiscalCode):
    pass


@when('Il PSP Invia la primitiva demandPaymentNotice priva di uno dei campi mandatori ({debtorFiscalCode:AnyText}, {debtorFullName:AnyText}, {amount:AnyText})')
def step_psp_invia_demand_payment_notice_senza_campo_obbligatorio(context, debtorFiscalCode, debtorFullName, amount):
    pass


@when('Il PSP Invia una richiesta con il formato errato di uno dei campi ({amount:AnyText}, {debtorFiscalCode:AnyText})')
def step_psp_invia_richiesta_formato_campo_errato(context, amount, debtorFiscalCode):
    pass
