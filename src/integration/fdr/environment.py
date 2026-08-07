"""Environment hooks for FDR integration scenarios.

This module provides behave (BDD) hooks used by the FDR integration tests.
It is responsible for:
- loading shared configuration and secrets into the test context,
- building REST clients for FDR and PSP services,
- preparing per-scenario context based on tags,
- cleaning up resources after scenarios/tests.

Notes for maintainers:
- Tag parsing below is fragile (string-slicing + split). Prefer a small helper that
  parses tags using regex or a dedicated metadata structure.
- Many context attributes are assumed to exist elsewhere (e.g., context.fdr).
  Ensure they are initialized before use or add defensive checks here.
"""

import os

from urllib.parse import unquote

from src.utility.blob.azure_blob import AzureBlobService
from src.utility.rest import build_rest_client, build_api_key_auth_from_config
from src.conf.configuration import load_configurations
from src.integration.fdr import common


def before_all(context):
    """Global setup executed once before the test suite.

    Populates the behave `context` with shared settings, secrets and reusable
    REST clients for FDR and PSP.

    Side effects:
    - Sets context.settings / context.secrets / context.commondata
    - Builds REST clients and assigns them to context.fdr.rest.client and
      context.psp.rest.client

    Important:
    - The REST clients must be closed in after_all to avoid resource leaks.
    - This function assumes `context.fdr` and `context.psp` objects already exist
      (created by behave environment or other helpers). If those attributes can
      be missing in some test runs, add defensive initialization here.
    """
    context.config = load_configurations(os.path.dirname(os.path.abspath(__file__)))

    # Build FDR rest client
    fdr_rest_config = context.config.fdr
    # NOTE: ensure context.fdr and context.fdr.rest exist before assignment
    context.fdr.rest.client = build_rest_client(
        fdr_rest_config, build_api_key_auth_from_config(fdr_rest_config)
    )

    # Build PSP rest client
    psp_rest_config = context.config.psp
    context.psp.rest.client = build_rest_client(
        psp_rest_config, build_api_key_auth_from_config(psp_rest_config)
    )

    # Build Blob container client
    blob_service_client = AzureBlobService(context)
    context.blob.service_client = blob_service_client

def before_scenario(context, scenario):
    """Per-scenario setup activated before each scenario.

    Responsibilities:
    - Reset transient fields via clear_context
    - Interpret custom tags on the scenario to perform setup actions

    Expected tag formats (examples):
    - Crea_FdR(id_fdr=someId, id_psp=somePsp)
    - Inserisci_Pagamenti(totPayments=3, sumPayments=3000)
    - Pubblica_FdR()

    Caution:
    - Tag parsing implemented below is brittle. It slices the string to extract
      the portion inside parentheses then splits on commas. This will break on
      values containing commas or if spacing differs. Prefer using a regex or
      a helper that returns a dict safely.
    """
    clear_context(context)
    for tag in scenario.tags:
        if tag.startswith("Crea_FdR"):
            # Extract parameters from the tag and create a FdR
            # Fragile parsing: prefer regex or a helper
            params_str = tag[tag.find("(") + 1:tag.find(")")].split(",")
            # NOTE: the following line assumes params_str is a string; if the
            # split above returns a list, calling split on it would raise an
            # AttributeError. Keep the parsing logic in a helper and add
            # unit-tests to capture these edge cases.
            params = dict(item.split("=") for item in params_str.split(", "))
            context.fdr_id = unquote(params["id_fdr"])
            context.psp_id = unquote(params["id_psp"])
            # Delegate FdR creation to the integration helper
            common.create_fdr(context, context.fdr_id, context.psp_id)
        elif tag.startswith("Inserisci_Pagamenti"):
            # Extract parameters from the tag and insert payments
            params_str = tag[tag.find("(") + 1:tag.find(")")].split(",")
            params = dict(item.split("=") for item in params_str.split(", "))
            context.tot_payments = int(params["totPayments"])
            context.sum_payments = int(params["sumPayments"])
            common.insert_payments(context, context.tot_payments, context.sum_payments)
        elif tag.startswith("Pubblica_FdR"):
            # Publish the FdR
            common.publish_fdr(context)

    # Some feature files may provide a row with test parameters (data-driven).
    if hasattr(scenario, 'row') and scenario.row:
        # Check if the scenario has a "stato_esistente" column
        stato_esistente = scenario.row.get("stato_esistente")
        # If the "stato_esistente" column is present and its value is "INSERTED",
        # insert a small set of payments used by subsequent steps.
        if stato_esistente == "INSERTED":
            common.insert_payments(context, 3, 3000)


def after_scenario(context, scenario):
    """Per-scenario teardown.

    Clears transient context fields to avoid state leaking between scenarios.
    """
    clear_context(context)


def after_all(context):
    """Global teardown executed once after the test suite.

    - Clears context
    - Closes REST client connections if present
    - Removes references to help garbage collection
    """
    clear_context(context)

    # Close FDR client if present
    if getattr(context, 'fdr', None) and getattr(context.fdr, 'rest', None):
        context.fdr.rest.client.close()
        context.fdr = None

    # Close PSP client if present
    if getattr(context, 'psp', None) and getattr(context.psp, 'rest', None):
        context.psp.rest.client.close()
        context.psp = None

    if getattr(context, 'blob', None) and getattr(context.blob, 'service_client', None):
        context.blob.service_client.close()
        context.blob.service_client = None


def clear_context(context):
    """Reset commonly-used context fields between scenarios.

    Enumerates all transient attributes that tests rely on and sets them to None.
    This makes it explicit which pieces of state are ephemeral and reduces the
    chance of accidental coupling between scenarios.
    """
    context.response = None
    context.get_fdr_response = None
    context.request_date = None
    context.fdr_id = None
    context.psp = None
    context.blob = None
    context.sender = None
    context.receiver = None
    context.bic_code_pouring_bank = None
    context.tot_payments = None
    context.sum_payments = None
    context.get_psp_response = None
