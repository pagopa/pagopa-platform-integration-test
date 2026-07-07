import os
from typing import Any, Optional

from azure.identity import DefaultAzureCredential
from azure.mgmt.apimanagement import ApiManagementClient
from azure.core.exceptions import HttpResponseError

from src.utility.config.secrets.secret_resolver import SecretResolver


class ApimSubscriptionResolver(SecretResolver):
    """
    Resolve subscription keys from Azure API Management (APIM).

    Configuration (environment variables):
    - `AZURE_SUBSCRIPTION_ID`: Azure subscription id used to create the management client.
    - `APIM_RESOURCE_GROUP`: resource group containing the APIM service.
    - `APIM_SERVICE_NAME`: name of the APIM service instance.

    The `secret_name` accepted by `resolve()` can be:
    - a logical name mapped via environment variable `APIM_SUBSCRIPTION_<NAME>` -> <subscriptionId>
    - a raw APIM subscription id
    - optionally suffixed with `:primary` or `:secondary` to select the key

    Examples:
        resolver = ApimSubscriptionResolver()
        key = resolver.resolve("my-sub-id")
        key = resolver.resolve("my-logical-name:secondary")
    """

    def __init__(
        self,
        subscription_id: Optional[str] = None,
        resource_group: Optional[str] = None,
        service_name: Optional[str] = None,
        credential=None,
    ):
        self.subscription_id = subscription_id or os.environ.get("AZURE_SUBSCRIPTION_ID")
        self.resource_group = resource_group or os.environ.get("APIM_RESOURCE_GROUP")
        self.service_name = service_name or os.environ.get("APIM_SERVICE_NAME")
        self.credential = credential or DefaultAzureCredential()

        if not self.subscription_id:
            raise RuntimeError("AZURE_SUBSCRIPTION_ID must be set (or pass subscription_id).")
        if not self.resource_group or not self.service_name:
            raise RuntimeError("APIM_RESOURCE_GROUP and APIM_SERVICE_NAME must be set.")

        self._client = ApiManagementClient(self.credential, self.subscription_id)

    def _lookup_subscription_id(self, secret_name: str) -> str:
        env_key = f"APIM_SUBSCRIPTION_{secret_name.upper()}"
        if env_key in os.environ:
            return os.environ[env_key]
        return secret_name

    def resolve(self, secret_name: str) -> Any:
        """
        Resolve the subscription key associated with `secret_name`.

        Args:
            secret_name: logical name or subscription id, optionally with `:primary` or `:secondary` suffix.

        Returns:
            The subscription key value (string).

        Raises:
            KeyError: when subscription not found or key missing.
        """
        key_type = "primary"
        if ":" in secret_name:
            secret_name, suffix = secret_name.split(":", 1)
            if suffix.lower() == "secondary":
                key_type = "secondary"

        subscription_id = self._lookup_subscription_id(secret_name)
        try:
            sub = self._client.subscription.get(self.resource_group, self.service_name, subscription_id)
        except HttpResponseError as ex:
            raise KeyError(f"APIM subscription not found or insufficient permissions: {ex}") from ex

        primary = getattr(sub, "primary_key", None) or getattr(sub, "primaryKey", None)
        secondary = getattr(sub, "secondary_key", None) or getattr(sub, "secondaryKey", None)

        if key_type == "primary":
            if not primary:
                raise KeyError("Primary key not available for subscription.")
            return primary
        else:
            if not secondary:
                raise KeyError("Secondary key not available for subscription.")
            return secondary
