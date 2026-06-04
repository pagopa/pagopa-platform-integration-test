import os
from typing import Any

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from src.utility.config.secrets.secret_resolver import SecretResolver


class AzureKeyVaultSecretResolver(SecretResolver):
    """
    Recupera i secret da Azure Key Vault tramite DefaultAzureCredential.

    La variabile d'ambiente AZURE_KEY_VAULT_URL deve essere impostata
    con l'URL del vault (es. https://my-vault.vault.azure.net/).

    L'autenticazione avviene tramite DefaultAzureCredential, che supporta
    automaticamente: Managed Identity, Azure CLI, environment credentials, ecc.

    Esempio::

        # Imposta la variabile d'ambiente prima del lancio dei test:
        #   $env:AZURE_KEY_VAULT_URL = "https://my-vault.vault.azure.net/"

        resolver = AzureKeyVaultSecretResolver()
        secret_value = resolver.resolve("my-secret-name")

    Esempio con config loader::

        # Il JSON può contenere placeholder come "$my_secret_name"
        # I nomi dei placeholder corrispondono ai nomi dei secret nel vault.

        resolver = AzureKeyVaultSecretResolver()
        config = load_test_config(resolver)

    Esempio in environment.py di Behave::

        def before_all(context):
            context.secret_resolver = AzureKeyVaultSecretResolver()
            context.test_config = load_test_config(context.secret_resolver)
    """

    def __init__(self):
        self._client = SecretClient(
            os.environ["AZURE_KEY_VAULT_URL"],
            DefaultAzureCredential()
        )

    def resolve(self, secret_name: str) -> Any:
        """
        Recupera il valore di un secret da Azure Key Vault.

        Args:
            secret_name: nome del secret nel vault.
                         Nota: Azure Key Vault non supporta underscore nei nomi;
                         se il placeholder JSON usa underscore (es. "$client_secret"),
                         considera di usare trattini nel vault (es. "client-secret")
                         e mappare i nomi nel resolver.

        Returns:
            Il valore stringa del secret.

        Raises:
            azure.core.exceptions.ResourceNotFoundError: se il secret non esiste nel vault.

        Esempio::

            resolver = AzureKeyVaultSecretResolver()
            password = resolver.resolve("db-password")
        """
        secret = self._client.get_secret(secret_name)
        return secret.value