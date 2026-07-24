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


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def check_apim_variables():
    """Check if the required APIM environment variables are set."""
    required_vars = ["AZURE_SUBSCRIPTION_ID", "APIM_RESOURCE_GROUP", "APIM_SERVICE_NAME"]
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    return True if missing_vars == [] else False


def load_settings(config_folder_root: str, config_file_name: str = "config.yaml", target_section: str = "", env_var_prefix: str = ""):
    """Load settings from a YAML configuration file using Dynaconf.

    Args:
        config_folder_root (str): The root folder where the configuration file is located. (example: config_folder_root = os.path.join(os.path.dirname(os.path.abspath(__file__))))

        config_file_name (str, optional): The name of the configuration file. Defaults to "config.yaml".
        
        target_section (str, optional): The target section desired inside the settings file. Defaults to env var TARGET_ENV or "uat" if not set.
        
        env_var_prefix (str, optional): The prefix for environment variables. Defaults to "" (empty string). If empty, no prefix will be used.

    Returns:
       A sequence object containing the settings for the specified target environment in the specified path.
    """
    settings = Dynaconf(
        envvar_prefix=env_var_prefix if env_var_prefix != "" else "",
        settings_files=[os.path.join(config_folder_root, config_file_name)],
    )

    if target_section:
        settings = settings[str(os.environ.get(target_section)).lower()]
    else:
        if 'TARGET_ENV' not in os.environ:
            os.environ['TARGET_ENV'] = 'uat'
        settings = settings[str(os.environ['TARGET_ENV']).lower()]

    return settings


def load_secrets(suite: str = "",
                 target_env: str = "",
                 settings: dict = None) -> dict:
    """Load secrets resolver and resolved secrets according to runtime configuration.
    # Keep canonical env vars aligned for loaders that resolve placeholders
    # from environment context.
    

    Logic:
    - If the environment variable `AZURE_KEY_VAULT_URL` is set, use
      `AzureKeyVaultSecretResolver` (secrets will be resolved from the vault).
      In this case the function still requires the suite and the target env
      to be specified via environment variables (see below) so callers must
      provide them or they must be present in the environment.
    - If the vault URL is not set, load a local secrets file (YAML/KEY=VALUE)
      located under /config and build a `DictSecretResolver` from the subsection matching 
      the target environment.

    Args:
        secrets_file_name: name of the secrets file (default: `.secrets.yaml`).
        suite: optional name of the suite used to find the appropriate secrets placeholder
        file. If empty, the code will look for the `suite` env var.
        target_envr: optional name of the env used to identify the target environment
        inside the secrets file. If empty, `TARGET_ENV` is used and falls back to `uat` 
        when not present.
        settings: optional dict of settings loaded from the config file (used to resolve secrets placeholders when not using the azure key vault).

    Returns:
        secrets: A dictionary containing the resolved secrets for the specified suite and target environment.
    """

    # Resolve target environment (fallback to TARGET_ENV -> 'uat')
    if not target_env:
        if 'TARGET_ENV' not in os.environ:
            os.environ['TARGET_ENV'] = 'uat'
        target_env = os.environ['TARGET_ENV']

   
    # Resolve suite name 
    if not suite:
        if 'suite' not in os.environ:
            raise RuntimeError("Suite name not set: set the suite environment variable or pass its name to load_secrets") 
        suite = os.environ.get('suite')

    os.environ['TARGET_ENV'] = str(target_env)
    os.environ['suite'] = str(suite)
   

    secrets_resolver = None
    secrets = {}

    if os.getenv("AZURE_KEY_VAULT_URL"):
        # Use Azure Key Vault resolver (requires AZURE_KEY_VAULT_URL env var)
        secrets_resolver = AzureKeyVaultSecretResolver()
        # For Azure we don't have a local dict to pre-populate; the resolver
        # will be used by `load_json_config` to resolve placeholders.
    else:
        # resolve secrets from DictSecretResolver for local testing, takes a dictonary of secrets which he uses to resolve secrets founds in the test config file
        try:
            if settings is None:
                raise RuntimeError("Settings must be provided when not using Azure Key Vault for secrets resolution.")
            all_secrets = Dynaconf(settings_files=settings.SECRET_PATH)
            secrets_resolver = DictSecretResolver(all_secrets[str(settings.TARGET_ENV).lower()])
        except Exception as e:
            logging.exception("Failed to load secrets from %s", settings.SECRET_PATH)
            raise RuntimeError("Failed to initialize local secrets resolver") from e
    try:
        secrets = load_json_config(secrets_resolver)
    except Exception as e:
        logging.exception("Failed to load secrets using resolver")
        raise RuntimeError("Failed to resolve secrets") from e

    if isinstance(secrets_resolver, AzureKeyVaultSecretResolver):
            secrets_resolver.close_client()

    return secrets


def load_commondata(commondata_file_name: str = "commondata.yaml", config_folder_root: str = None) -> dict:

    """Load common data from a YAML configuration file using Dynaconf.
    Args:
        config_folder_root (str): The root folder where the configuration file is located. (example: config_folder_root = os.path.join(os.path.dirname(os.path.abspath(__file__))))
        commondata_file_name (str, optional): The name of the common data file. Defaults to "commondata.yaml".
    Returns:
        A dictionary containing the common data loaded from the specified file.
    """

    if config_folder_root is None:
        raise ValueError("config_folder_root must be provided to load common data.")

   
    try:
        commondata = Dynaconf(
        settings_files=[os.path.join(config_folder_root, commondata_file_name)],
        )
        commondata = commondata['TEST_DATA'].to_dict()
    except KeyError as e:
        logging.exception("Failed to load common data from %s", commondata_file_name)
        raise RuntimeError("Failed to load common data") from e

    return commondata
