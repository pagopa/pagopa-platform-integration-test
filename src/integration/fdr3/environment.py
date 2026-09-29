"""Environment hooks for FdR3 integration scenarios.

Provides behave hooks to:
- load configuration
- initialize REST clients for FdR and PSP
- prepare and clear per-feature and per-scenario context
- configure basic logging

This is modeled on src.integration.fdr.environment.py but scoped for the fdr3 tests.
"""
import os
import logging
from types import SimpleNamespace

from src.utility.rest import build_rest_client, build_api_key_auth_from_config
from src.conf.configuration import load_configurations


LOGGER = logging.getLogger("fdr3")


def _ensure_actor(context, name: str):
    """Ensure context.<name> exists and has a .rest attribute with a client slot."""
    if not hasattr(context, name) or getattr(context, name) is None:
        setattr(context, name, SimpleNamespace(rest=SimpleNamespace(client=None)))


def before_all(context):
    """Global setup executed once before the test suite.

    - configure logging
    - load configurations
    - prepare PSP and FDR actor holders
    - build REST clients and assign to context.fdr.rest.client and context.psp.rest.client
    """
    # Basic logging configuration for local runs (can be overridden by test runner)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    LOGGER.info("Initializing fdr3 test environment before_all")

    # Load configuration relative to this directory
    context.config = load_configurations(os.path.dirname(os.path.abspath(__file__)))

    # Ensure actor containers exist
    _ensure_actor(context, "fdr")
    _ensure_actor(context, "psp")
    # Optional blob holder
    if not hasattr(context, "blob"):
        context.blob = SimpleNamespace(service_client=None)

    # Build REST clients if configuration provides them
    try:
        fdr_conf = getattr(context.config, "fdr", None)
        if fdr_conf:
            context.fdr.rest.client = build_rest_client(fdr_conf, build_api_key_auth_from_config(fdr_conf))
            LOGGER.info("FDR REST client initialized")
    except Exception as exc:
        LOGGER.warning(f"Failed to initialize FDR client: {exc}")

    try:
        psp_conf = getattr(context.config, "psp", None)
        if psp_conf:
            context.psp.rest.client = build_rest_client(psp_conf, build_api_key_auth_from_config(psp_conf))
            LOGGER.info("PSP REST client initialized")
    except Exception as exc:
        LOGGER.warning(f"Failed to initialize PSP client: {exc}")


def before_feature(context, feature):
    """Run before each feature. Clear transient context and add feature-scoped defaults."""
    LOGGER.info("before_feature: %s", getattr(feature, "name", "<unnamed>"))
    clear_context(context)
    # Provide defaults commonly used by fdr3 steps
    if not hasattr(context, "vars"):
        context.vars = {}
    if not hasattr(context, "payloads"):
        context.payloads = {}
    # place to set feature-level defaults if needed


def before_scenario(context, scenario):
    """Per-scenario setup. Ensure transient state is reset before each scenario."""
    LOGGER.debug("before_scenario: %s", getattr(scenario, "name", "<unnamed>"))
    # Keep actor clients but reset request/response state
    clear_transient(context)
    # If scenario is data-driven, map row values into context.vars
    if hasattr(scenario, "row") and scenario.row:
        for k, v in scenario.row.items():
            # store small test parameters into context.vars for placeholder substitution
            context.vars[k] = v


def after_scenario(context, scenario):
    """Per-scenario teardown: clear transient fields to avoid leakage."""
    LOGGER.debug("after_scenario: %s", getattr(scenario, "name", "<unnamed>"))
    clear_transient(context)


def after_feature(context, feature):
    LOGGER.info("after_feature: %s", getattr(feature, "name", "<unnamed>"))
    # Nothing heavy here; clients stay alive for the test run
    clear_transient(context)


def after_all(context):
    """Global teardown executed once after the test suite.

    - clear context
    - close REST clients if present
    """
    LOGGER.info("Tearing down fdr3 test environment after_all")
    clear_context(context)

    # Close FDR client if present
    if getattr(context, "fdr", None) and getattr(context.fdr, "rest", None) and getattr(context.fdr.rest, "client", None):
        try:
            context.fdr.rest.client.close()
            LOGGER.info("Closed FDR REST client")
        except Exception:
            LOGGER.exception("Error closing FDR client")
        context.fdr.rest.client = None

    # Close PSP client if present
    if getattr(context, "psp", None) and getattr(context.psp, "rest", None) and getattr(context.psp.rest, "client", None):
        try:
            context.psp.rest.client.close()
            LOGGER.info("Closed PSP REST client")
        except Exception:
            LOGGER.exception("Error closing PSP client")
        context.psp.rest.client = None

    # Close blob client if present
    if getattr(context, "blob", None) and getattr(context.blob, "service_client", None):
        try:
            context.blob.service_client.close()
            LOGGER.info("Closed blob service client")
        except Exception:
            LOGGER.exception("Error closing blob service client")
        context.blob.service_client = None


# -------------------- helpers --------------------

def clear_transient(context):
    """Clear per-scenario transient fields but keep configured clients."""
    context.response = None
    context.get_fdr_response = None
    context.request_date = None
    context.fdr_id = None
    context.prior_scenario = None
    context.tot_payments = None
    context.sum_payments = None
    context.sender = None
    context.receiver = None


def clear_context(context):
    """Clear broader context including clients and all vars/payloads.

    Use this to reset everything between features or at teardown.
    """
    # Keep clients if they are present; just clear their stored state
    clear_transient(context)
    context.vars = {}
    context.payloads = {}
    # do not remove context.fdr/context.psp to preserve client configuration
