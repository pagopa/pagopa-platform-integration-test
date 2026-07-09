from behave import given, when, then
from src.integration.fdr.common import delete_payments

@given(u'contiene {totPayments:d} pagamenti con amount {sumPayments:f}')
def step_check_payments_number_and_amounts(context, totPayments, sumPayments):
    ##TODO check variables names
    assert context.fdr.created.json().get('totPayments') == totPayments, f"Expected {totPayments} payments, but got {context.fdr.created.json().get('totPayments')}"
    assert context.fdr.created.json().get('sumPayments') == sumPayments, f"Expected total amount {sumPayments}, but got {context.fdr.created.json().get('sumPayments')}"


@when(u'si vuole cancellare {num_payments:d} pagamenti con amount {amount:f}')
def step_define_payment_deletion(context, num_payments, amount):
    payments_to_delete = []
    if num_payments == 1:
        payments_to_delete.append(context.fdr.created.json().get('data')[0].get('index'))
    elif num_payments == len(context.fdr.created.json().get('data')):
        for payment in context.fdr.created.json().get('data'):
            payments_to_delete.append(payment.get('index'))

    context.fdr.payments_to_delete = payments_to_delete


@then(u'Il numero residuo di pagamenti nel flusso è {totPayments:d}')
def step_check_remaining_payments(context, totPayments):
    assert totPayments == context.fdr.response.json().get('totPayments'), f"Expected {totPayments} payments, but got {context.fdr.response.json().get('totPayments')}"


@then(u'L’amount totale viene correttamente aggiornato con {sumPayments:f}')
def step_check_updated_total(context, sumPayments):
    assert sumPayments == context.fdr.response.json().get('totPayments'), f"Expected {sumPayments} payments, but got {context.fdr.response.json().get('totPayments')}"


@then(u'I pagamenti da eliminare non sono più associati all’fdr')
def step_check_payment_disassociation(context):
    payments_to_delete = context.fdr.payments_to_delete
    payments = context.fdr.payment.response.json().ge('data')
    for payment in payments:
        assert payment.get('index') not in payments_to_delete, f"Expected payment {payment.get('index')} to be deleted"


@given(u'che il flusso di rendicontazione "{fdr_id}" non esiste a sistema')
def step_given_fdr_not_exists(context, fdr_id):
    assert context.fdr.http_status_code == 404, f"Expected 404 Not Found, but got {context.fdr.http_status_code}"


@when(u'Il PSP invia una richiesta di cancellazione dei pagamenti attraverso l\'API "Delete one or more payments from an existing flow"')
def step_delete_payments_request(context):
    delete_payments(context)