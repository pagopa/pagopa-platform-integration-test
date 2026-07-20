"""Then step definitions for rendicontazione.feature (tas_mixed suite).

Mixed outcome: scenarios 1 and 2 fail, scenario 3 passes.
"""
import logging

from behave import then

logger = logging.getLogger(__name__)


@then("il flusso di rendicontazione viene creato con successo")
def flusso_creato_con_successo(context):
    """Assert the reconciliation flow was created — intentionally fails in the mixed suite."""
    assert False, "Rendicontazione flow creation failed — FDR service returned HTTP 500"


@then("tutti i campi obbligatori del flusso risultano valorizzati")
def campi_valorizzati(context):
    """Assert all mandatory fields of the flow are populated — intentionally fails in the mixed suite."""
    assert False, "Missing mandatory field 'totImporto' in rendicontazione response"


@then("l'ente creditore conferma la ricezione del flusso")
def ec_conferma_ricezione(context):
    """Assert the creditor entity confirmed receipt of the flow — passes in the mixed suite."""
    pass
