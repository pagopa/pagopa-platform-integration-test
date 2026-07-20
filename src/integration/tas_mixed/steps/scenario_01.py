"""Then step definitions for verifiche_sistema.feature (tas_mixed suite).

Mixed outcome: scenario 1 (HTTP 200) passes, scenario 2 (timeout) fails,
scenario 3 (configuration) passes.
"""
import logging

from behave import then

logger = logging.getLogger(__name__)


@then("la risposta ha codice HTTP 200")
def risposta_http_200(context):
    """Assert the service responded with HTTP 200 — passes in the mixed suite."""
    pass


@then("il nodo risponde entro il tempo limite previsto")
def nodo_risponde_entro_limite(context):
    """Assert the node responded within the time limit — intentionally fails in the mixed suite."""
    assert False, "Connection timeout: host 'api.platform.pagopa.it' unreachable after 30s"


@then("tutti i parametri di configurazione risultano validi")
def parametri_validi(context):
    """Assert all mandatory configuration parameters are valid — passes in the mixed suite."""
    pass
