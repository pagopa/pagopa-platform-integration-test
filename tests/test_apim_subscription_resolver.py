from unittest.mock import MagicMock, patch
import os

from src.utility.config.secrets.apim_subscription_resolver import ApimSubscriptionResolver


def test_resolve_primary(monkeypatch):
    fake_sub = MagicMock()
    fake_sub.primary_key = "PRIMARY_VAL"
    client = MagicMock()
    client.subscription.get.return_value = fake_sub

    with patch("src.utility.config.secrets.apim_subscription_resolver.ApiManagementClient", return_value=client):
        monkeypatch.setenv("AZURE_SUBSCRIPTION_ID", "subid")
        monkeypatch.setenv("APIM_RESOURCE_GROUP", "rg")
        monkeypatch.setenv("APIM_SERVICE_NAME", "apim")
        resolver = ApimSubscriptionResolver()
        assert resolver.resolve("some-sub-id") == "PRIMARY_VAL"


def test_resolve_secondary_suffix(monkeypatch):
    fake_sub = MagicMock()
    fake_sub.secondary_key = "SECONDARY_VAL"
    client = MagicMock()
    client.subscription.get.return_value = fake_sub

    with patch("src.utility.config.secrets.apim_subscription_resolver.ApiManagementClient", return_value=client):
        monkeypatch.setenv("AZURE_SUBSCRIPTION_ID", "subid")
        monkeypatch.setenv("APIM_RESOURCE_GROUP", "rg")
        monkeypatch.setenv("APIM_SERVICE_NAME", "apim")
        resolver = ApimSubscriptionResolver()
        assert resolver.resolve("some-sub-id:secondary") == "SECONDARY_VAL"
