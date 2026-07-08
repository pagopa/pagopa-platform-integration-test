"""Then step definitions for verifiche_sistema.feature (tas_fail suite).

All assertions fail intentionally with realistic error messages.
This suite is intended for TAS demonstrations where a fully red run is needed.
"""
import logging

from behave import then

logger = logging.getLogger(__name__)


@then("la risposta ha codice HTTP 200")
def risposta_http_200(context):
    """Assert the service responded with HTTP 200 — intentionally fails."""
    assert False, "Expected HTTP status 200 but received 503 Service Unavailable"


@then("il nodo risponde entro il tempo limite previsto")
def nodo_risponde_entro_limite(context):
    """Assert the node responded within the time limit — intentionally fails."""
    assert False, "Connection timeout: host 'api.platform.pagopa.it' unreachable after 30s"


@then("tutti i parametri di configurazione risultano validi")
def parametri_validi(context):
    """Assert all mandatory configuration parameters are valid — intentionally fails."""
    assert False, "Missing mandatory configuration key: 'NODO_SUBSCRIPTION_KEY'"
