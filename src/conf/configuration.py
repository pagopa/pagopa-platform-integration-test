"""Parse configuration file to obtain current settings.
"""
import logging
import os
from src.utility.config.config_loader import load_json_config, resolve_value
from src.utility.config.secrets.azure_secret_resolver import AzureKeyVaultSecretResolver
from src.utility.config.secrets.apim_subscription_resolver import ApimSubscriptionResolver
from src.utility.config.secrets.secret_resolver import DictSecretResolver

import urllib3
from dynaconf import Dynaconf

SECRETS_PATH = './config/.secrets.yaml'


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def check_apim_variables():
    """Check if the required APIM environment variables are set."""
    required_vars = ["AZURE_SUBSCRIPTION_ID", "APIM_RESOURCE_GROUP", "APIM_SERVICE_NAME"]
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    return True if missing_vars == [] else False

def solve_configurations(configurations, secret_resolver) -> dict:
    """Extract secrets placeholders from the configurations.

    Args:
        configurations (dict): The configurations loaded from the settings file.

    Returns:
        dict: A dictionary containing the secrets placeholders to be resolved.
    """
    for key, value in configurations.items():
        if isinstance(value, dict):
            solve_configurations(value, secret_resolver)
        if isinstance(value, str) and value.startswith('$'):
            configurations[key] = resolve_value(value, secret_resolver)  # Placeholder for resolved secret
    return configurations

def load_configurations(config_folder_root: str):
    """Load settings, secrets, and common data from configuration files.

    Args:
        config_folder_root (str): The root folder where the configuration files are located.
    Returns:
        tuple: A tuple containing settings, secrets, and common data dictionaries.
    """
    if not config_folder_root:
        raise ValueError("config_folder_root must be provided to load configurations.")

    if not os.path.isdir(config_folder_root):
        raise ValueError(f"config_folder_root '{config_folder_root}' is not a valid directory.")

    env_file = os.path.join(config_folder_root, os.getenv('TARGET_ENV', 'uat') + ".yaml")

    if not os.path.isfile(env_file):
        raise FileNotFoundError(f"Configuration file '{env_file}' not found.")

    configurations =  Dynaconf(
            settings_files=[env_file]
        )
    secret_resolver = get_secrets_resolver()
    configurations = solve_configurations(configurations, secret_resolver)
    return configurations
    

def load_secrets(secrets_to_solve: dict) -> dict:
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

    if secrets_to_solve is None:
        raise ValueError("secrets_to_solve must be provided to load secrets.")

    if os.getenv("AZURE_KEY_VAULT_URL"):
        # Use Azure Key Vault resolver (requires AZURE_KEY_VAULT_URL env var)
        secrets_resolver = AzureKeyVaultSecretResolver()
        # For Azure we don't have a local dict to pre-populate; the resolver
        # will be used by `load_json_config` to resolve placeholders.
    else:
        # resolve secrets from DictSecretResolver for local testing, takes a dictonary of secrets which he uses to resolve secrets founds in the test config file
        try:
            all_secrets = Dynaconf(settings_files=[SECRETS_PATH])
            secrets_resolver = DictSecretResolver(all_secrets[str(os.getenv('TARGET_ENV', 'uat')).lower()])
        except Exception as e:
            logging.exception("Failed to load secrets from %s", SECRETS_PATH)
            raise RuntimeError("Failed to initialize local secrets resolver") from e
    try:
        secrets = load_json_config(secrets_resolver, secrets_to_solve)
    except Exception as e:
        logging.exception("Failed to load secrets using resolver")
        raise RuntimeError("Failed to resolve secrets") from e

    if isinstance(secrets_resolver, AzureKeyVaultSecretResolver):
            secrets_resolver.close_client()

    return secrets

def get_secrets_resolver() -> Any:
    """Get the appropriate secrets resolver based on the environment configuration.

    Returns:
        An instance of the secrets resolver (AzureKeyVaultSecretResolver or DictSecretResolver).
    """
    if os.getenv("AZURE_KEY_VAULT_URL"):
        return AzureKeyVaultSecretResolver()
    else:
        try:
            all_secrets = Dynaconf(settings_files=[SECRETS_PATH])
            return DictSecretResolver(all_secrets[str(os.getenv('TARGET_ENV', 'uat')).lower()])
        except Exception as e:
            logging.exception("Failed to load secrets from %s", SECRETS_PATH)
            raise RuntimeError("Failed to initialize local secrets resolver") from e


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
