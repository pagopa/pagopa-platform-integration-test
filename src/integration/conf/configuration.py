"""Parse configuration file to obtain current settings.
"""
import logging
import os
from src.utility.config.config_loader import load_json_config
from src.utility.config.secrets.azure_secret_resolver import AzureKeyVaultSecretResolver
from src.utility.config.secrets.apim_subscription_resolver import ApimSubscriptionResolver
from src.utility.config.secrets.secret_resolver import DictSecretResolver

import urllib3
from dynaconf import Dynaconf

ENV_VAR_PREFIX = 'WISP_DISMANTLING'

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def check_apim_variables():
    """Check if the required APIM environment variables are set."""
    required_vars = ["AZURE_SUBSCRIPTION_ID", "APIM_RESOURCE_GROUP", "APIM_SERVICE_NAME"]
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    return True if missing_vars == [] else False

# `envvar_prefix` = export envvars with ENV_VAR_PREFIX as prefix.
# `settings_files` = Load settings files in the order.
settings = Dynaconf(
    envvar_prefix=ENV_VAR_PREFIX,
    settings_files=[os.path.join(_INTEGRATION_ROOT, 'config.yaml')],
)

if 'TARGET_ENV' not in os.environ:
    os.environ['TARGET_ENV'] = 'uat'

settings = settings[os.environ['TARGET_ENV']]

# Load the secrets for the specified environment
secrets = {}
secrets_resolver = None

# select the type of secret resolver based on the environment (CI or local testing)
if os.getenv("AZURE_KEY_VAULT_URL") is not None and os.getenv("AZURE_KEY_VAULT_URL") != "":
    # resolve secrets from Azure Key Vault in CI, otherwise use DictSecretResolver for local testing
    secrets_resolver = AzureKeyVaultSecretResolver()
  
else:
    # resolve secrets from DictSecretResolver for local testing, takes a dictonary of secrets which he uses to resolve secrets founds in the test config file
    try:
        all_secrets = Dynaconf(settings_files=settings.SECRET_PATH)
        if settings.TARGET_ENV in all_secrets:
            secrets_resolver = DictSecretResolver( all_secrets[settings.TARGET_ENV])
    except Exception as e:
        logging.error(e)
        exit()

secrets = load_json_config(secrets_resolver)
if isinstance(secrets_resolver, AzureKeyVaultSecretResolver):
    secrets_resolver.close_client()

commondata = Dynaconf(
    settings_files=[os.path.join(_INTEGRATION_ROOT, 'commondata.yaml')],
)

try:
    commondata = commondata['TEST_DATA'].to_dict()
except KeyError as e:
    logging.error(e)
    exit()
