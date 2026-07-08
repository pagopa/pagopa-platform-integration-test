"""Then step definitions for rendicontazione.feature (tas_fail suite).

All assertions fail intentionally with realistic error messages.
This suite is intended for TAS demonstrations where a fully red run is needed.
"""
import logging

from behave import then

logger = logging.getLogger(__name__)


@then("il flusso di rendicontazione viene creato con successo")
def flusso_creato_con_successo(context):
    """Assert the reconciliation flow was created — intentionally fails."""
    assert False, "Rendicontazione flow creation failed — FDR service returned HTTP 500"


@then("tutti i campi obbligatori del flusso risultano valorizzati")
def campi_valorizzati(context):
    """Assert all mandatory fields of the flow are populated — intentionally fails."""
    assert False, "Missing mandatory field 'totImporto' in rendicontazione response"


@then("l'ente creditore conferma la ricezione del flusso")
def ec_conferma_ricezione(context):
    """Assert the creditor entity confirmed receipt of the flow — intentionally fails."""
    assert False, "FDR flow not transmitted — EC endpoint returned 404 Not Found"
