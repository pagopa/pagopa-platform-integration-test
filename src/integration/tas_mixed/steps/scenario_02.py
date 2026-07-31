"""Then step definitions for flusso_pagamento.feature (tas_mixed suite).

Mixed outcome: scenario 1 (payment initiation) fails, scenarios 2 and 3 pass.
"""
import logging

from behave import then

logger = logging.getLogger(__name__)


@then("la richiesta di pagamento viene accettata dal sistema")
def richiesta_accettata(context):
    """Assert the payment request was accepted — intentionally fails in the mixed suite."""
    assert False, "Payment initiation failed — nodoInviaRPT returned fault code PAA_SYSTEM_ERROR"


@then('la transazione risulta completata con stato "CONFERMATO"')
def transazione_confermata(context):
    """Assert the transaction completed with status CONFERMATO — passes in the mixed suite."""
    pass


@then("la ricevuta contiene i dati attesi della transazione")
def ricevuta_corretta(context):
    """Assert the receipt contains the expected transaction data — passes in the mixed suite."""
    pass
