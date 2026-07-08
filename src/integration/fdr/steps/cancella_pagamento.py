@given(u'contiene {totPayments:d} pagamenti con amount {sumPayments:f}')
def step_check_payments_number_and_amounts(context, totPayments, sumPayments):
    raise NotImplementedError(u'STEP: Given contiene {totPayments:d} pagamenti con amount {sumPayments:f}')


@when(u'si vuole cancellare {num_payments:d} pagamenti con amount {amount:f}')
def step_define_payment_deletion(context, num_payments, amount):
    raise NotImplementedError(u'STEP: When si vuole cancellare {num_payments:d} pagamenti con amount {amount:f}')


@then(u'Il numero residuo di pagamenti nel flusso è {totPayments:d}')
def step_check_remaining_payments(context, totPayments):
    raise NotImplementedError(u'STEP: Then Il numero residuo di pagamenti nel flusso è {totPayments:d}')


@then(u'L’amount totale viene correttamente aggiornato con {sumPayments:f}')
def step_check_updated_total(context, sumPayments):
    raise NotImplementedError(u'STEP: Then L’amount totale viene correttamente aggiornato con {sumPayments:f}')


@then(u'I pagamenti da eliminare non sono più associati all’fdr')
def step_check_payment_disassociation(context):
    raise NotImplementedError(u'STEP: Then I pagamenti da eliminare non sono più associati all’fdr')


@then(u'Il numero residuo di pagamenti nel flusso è {totPayments:d}')
def step_check_remaining_payments_number(context, totPayments):
    raise NotImplementedError(u'STEP: Then Il numero residuo di pagamenti nel flusso è {totPayments:d}')


@then(u'L’amount totale viene correttamente aggiornato a {sumPayments:f}')
def step_check_remaining_total_amount(context, sumPayments):
    raise NotImplementedError(u'STEP: Then L’amount totale viene correttamente aggiornato a {sumPayments:f}')


@given(u'che il flusso di rendicontazione "{fdr_id}" non esiste a sistema')
def step_given_fdr_not_exists(context, fdr_id):
    raise NotImplementedError(u'STEP: Given che il flusso di rendicontazione "{fdr_id}" non esiste a sistema')


@when(u'Il PSP invia una richiesta di cancellazione dei pagamenti attraverso l\'API "Delete one or more payments from an existing flow"')
def step_delete_payments_request(context):
    raise NotImplementedError(u'STEP: When Il PSP invia una richiesta di cancellazione dei pagamenti attraverso l\'API "Delete one or more payments from an existing flow"')