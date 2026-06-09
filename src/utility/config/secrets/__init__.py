"""Secrets package.

Espone i resolver disponibili per il recupero dei secret:
- SecretResolver: interfaccia astratta
- DictSecretResolver: implementazione locale per test/mock
- AzureKeyVaultSecretResolver: implementazione Azure Key Vault
"""

from src.utility.config.secrets.secret_resolver import DictSecretResolver, SecretResolver
from src.utility.config.secrets.azure_secret_resolver import AzureKeyVaultSecretResolver

__all__ = ["SecretResolver", "DictSecretResolver", "AzureKeyVaultSecretResolver"]

