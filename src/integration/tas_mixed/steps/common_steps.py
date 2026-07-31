"""Shared Given and When step definitions for the tas_mixed demo suite.

All Given and When steps are no-ops (setup and action always succeed).
Only the Then steps have a mixed outcome — see scenario_01.py, scenario_02.py,
scenario_03.py for the individual pass/fail logic.
"""
import logging

from behave import given, when

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Given steps — verifiche_sistema.feature
# ---------------------------------------------------------------------------

@given("che il servizio di pagamento è raggiungibile")
def il_servizio_pagamento_raggiungibile(context):
    """Simulate a reachable payment service — always passes."""
    pass


@given("che il nodo dei pagamenti è configurato")
def il_nodo_configurato(context):
    """Simulate a configured payment node — always passes."""
    pass


@given("che il sistema è configurato per l'ambiente di test")
def sistema_configurato_ambiente(context):
    """Simulate a correctly configured test environment — always passes."""
    pass


# ---------------------------------------------------------------------------
# Given steps — flusso_pagamento.feature
# ---------------------------------------------------------------------------

@given("che l'utente ha un avviso di pagamento valido")
def utente_ha_avviso_valido(context):
    """Simulate a user holding a valid payment notice — always passes."""
    pass


@given("che una richiesta di pagamento è in corso di elaborazione")
def richiesta_in_elaborazione(context):
    """Simulate a payment request in progress — always passes."""
    pass


@given("che il pagamento è stato completato con successo")
def pagamento_completato(context):
    """Simulate a successfully completed payment — always passes."""
    pass


# ---------------------------------------------------------------------------
# Given steps — rendicontazione.feature
# ---------------------------------------------------------------------------

@given("che sono presenti transazioni da rendicontare")
def transazioni_presenti(context):
    """Simulate the presence of transactions to reconcile — always passes."""
    pass


@given("che il flusso di rendicontazione è stato creato")
def flusso_creato(context):
    """Simulate a created reconciliation flow — always passes."""
    pass


@given("che il flusso di rendicontazione è pronto per la trasmissione")
def flusso_pronto_trasmissione(context):
    """Simulate a reconciliation flow ready for transmission — always passes."""
    pass


# ---------------------------------------------------------------------------
# When steps — verifiche_sistema.feature
# ---------------------------------------------------------------------------

@when("viene inviata una richiesta di healthcheck")
def invia_richiesta_healthcheck(context):
    """Simulate sending a healthcheck request — always passes."""
    pass


@when("viene verificata la connettività di rete verso il nodo")
def verifica_connettivita_nodo(context):
    """Simulate a network connectivity check towards the node — always passes."""
    pass


@when("vengono verificati i parametri obbligatori di configurazione")
def verifica_parametri_configurazione(context):
    """Simulate verification of mandatory configuration parameters — always passes."""
    pass


# ---------------------------------------------------------------------------
# When steps — flusso_pagamento.feature
# ---------------------------------------------------------------------------

@when("l'utente avvia il pagamento tramite il canale pagoPA")
def utente_avvia_pagamento(context):
    """Simulate a user initiating a payment via the pagoPA channel — always passes."""
    pass


@when("il sistema elabora la transazione")
def sistema_elabora_transazione(context):
    """Simulate the system processing a payment transaction — always passes."""
    pass


@when("il sistema genera la ricevuta telematica")
def sistema_genera_ricevuta(context):
    """Simulate the system generating a telematic receipt — always passes."""
    pass


# ---------------------------------------------------------------------------
# When steps — rendicontazione.feature
# ---------------------------------------------------------------------------

@when("viene avviata la creazione del flusso di rendicontazione")
def avvia_creazione_flusso(context):
    """Simulate the start of a reconciliation flow creation — always passes."""
    pass


@when("vengono verificati i dati del flusso")
def verifica_dati_flusso(context):
    """Simulate verification of reconciliation flow data — always passes."""
    pass


@when("viene avviata la trasmissione del flusso all'ente creditore")
def avvia_trasmissione_flusso(context):
    """Simulate the start of reconciliation flow transmission — always passes."""
    pass
