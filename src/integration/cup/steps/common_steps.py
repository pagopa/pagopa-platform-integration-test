from behave import *

import src.integration.cup.steps.step_param_types  # noqa: F401


@then('Viene creata correttamente la posizione debitoria')
def step_viene_creata_posizione_debitoria(context):
    pass


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
