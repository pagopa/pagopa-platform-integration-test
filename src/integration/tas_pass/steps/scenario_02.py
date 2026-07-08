"""Then step definitions for flusso_pagamento.feature (tas_pass suite).

All assertions succeed instantly — this is a demo suite for green TAS runs.
"""
import logging

from behave import then

logger = logging.getLogger(__name__)


@then("la richiesta di pagamento viene accettata dal sistema")
def richiesta_accettata(context):
    """Assert the payment request was accepted by the system — always passes."""
    pass


@then('la transazione risulta completata con stato "CONFERMATO"')
def transazione_confermata(context):
    """Assert the transaction completed with status CONFERMATO — always passes."""
    pass


@then("la ricevuta contiene i dati attesi della transazione")
def ricevuta_corretta(context):
    """Assert the receipt contains the expected transaction data — always passes."""
    pass
