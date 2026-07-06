import os

from src.utility.config.config_loader import load_json_config
from src.utility.config.secrets.azure_secret_resolver import AzureKeyVaultSecretResolver
from src.utility.rest.rest_auth_factory import build_api_key_auth_from_config
from src.utility.rest.rest_client_factory import build_rest_client


if os.getenv("AZURE_KEY_VAULT_URL") is not None and os.getenv("AZURE_KEY_VAULT_URL") != "":
    # resolve secrets from Azure Key Vault in CI
    secrets_resolver = AzureKeyVaultSecretResolver()
    config = load_json_config(secrets_resolver)
    if isinstance(secrets_resolver, AzureKeyVaultSecretResolver):
        secrets_resolver.close_client()


def before_all(context):
    context.fdr.rest.auth = build_api_key_auth_from_config(context.config["fdr"]["api_key"])
    context.fdr.rest.client = build_rest_client(context.config["service"], context.fdr.rest.auth)

    context.psp.rest.auth = build_api_key_auth_from_config(context.config["psp"]["api_key"])
    context.psp.rest.client = build_rest_client(context.config["service"], context.psp.rest.auth)


def before_scenario(context, scenario):
    clear_context(context)

def after_scenario(context, scenario):
    clear_context(context)

def after_all(context):
    clear_context(context)
    context.fdr.rest.client.close()
    context.fdr = None
    context.psp.rest.client.close()
    context.psp = None


def clear_context(context):
    context.response = None
    context.get_fdr_response = None
    context.request_date = None
    context.fdr_id = None
    context.psp = None
    context.sender = None
    context.receiver = None
    context.bic_code_pouring_bank = None
    context.tot_payments = None
    context.sum_payments = None
    context.get_psp_response = None