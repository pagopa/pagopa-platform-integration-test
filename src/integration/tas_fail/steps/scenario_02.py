"""Then step definitions for flusso_pagamento.feature (tas_fail suite).

All assertions fail intentionally with realistic error messages.
This suite is intended for TAS demonstrations where a fully red run is needed.
"""
import logging

from behave import then

logger = logging.getLogger(__name__)


@then("la richiesta di pagamento viene accettata dal sistema")
def richiesta_accettata(context):
    """Assert the payment request was accepted — intentionally fails."""
    assert False, "Payment initiation failed — nodoInviaRPT returned fault code PAA_SYSTEM_ERROR"


@then('la transazione risulta completata con stato "CONFERMATO"')
def transazione_confermata(context):
    """Assert the transaction completed with status CONFERMATO — intentionally fails."""
    assert False, "Expected payment status 'CONFERMATO' but found 'IN_ERROR' after 10s"


@then("la ricevuta contiene i dati attesi della transazione")
def ricevuta_corretta(context):
    """Assert the receipt contains expected transaction data — intentionally fails."""
    assert False, "Receipt (RT) not found for IUV '301000000012345678'"
