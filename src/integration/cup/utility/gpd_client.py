"""GPD REST client for the CUP integration test suite.

Provides a thin wrapper around the shared RestClient for calling GPD
debt-position APIs. Use ``build_gpd_client`` to construct an instance
from the suite configuration, then call the individual methods.

Required entries in ``config.yaml`` under ``services``:

.. code-block:: yaml

    gpd:
      url: <GPD internal API v1 base URL>
      subscription_key: <secret key name for Ocp-Apim-Subscription-Key>
    gpd_external:
      url: <GPD external API v1 base URL>
      subscription_key: <secret key name for Ocp-Apim-Subscription-Key>

Secret required in ``.secrets.yaml`` for each environment:

.. code-block:: yaml

    dev:
      GPD_SUBSCRIPTION_KEY: "<actual subscription key value>"
    uat:
      GPD_SUBSCRIPTION_KEY: "<actual subscription key value>"

Usage example from a Behave step::

    from src.integration.cup.utility.gpd_client import build_gpd_client

    gpd = build_gpd_client(
        context.settings.services['gpd'],
        context.secrets,
    )
    response = gpd.get_debt_position(org_id="77777777777", iupd="IUPD-001")
    assert response.status_code == 200
"""
import logging

from src.utility.rest.rest_auth_factory import build_api_key_auth
from src.utility.rest.rest_client import RestClient
from src.utility.rest.rest_client_factory import build_rest_client

_OCP_APIM_HEADER = "Ocp-Apim-Subscription-Key"


def build_gpd_client(service_config, secrets) -> "GpdClient":
    """Build a GpdClient from the suite service configuration and secrets.

    Args:
        service_config: service dict from ``context.settings.services['gpd']``
            or ``context.settings.services['gpd_external']``.
        secrets: secrets object from ``context.secrets``.

    Returns:
        GpdClient configured with API-key authentication.
    """
    subscription_key_name = service_config.get("subscription_key", "GPD_SUBSCRIPTION_KEY")
    key_value = secrets[subscription_key_name]
    auth = build_api_key_auth(key_name=_OCP_APIM_HEADER, key_value=key_value)
    rest_client = build_rest_client(service_config, auth)
    return GpdClient(rest_client)


class GpdClient:
    """REST client for the GPD debt-position APIs.

    Do not instantiate directly; use ``build_gpd_client`` instead.
    """

    def __init__(self, rest_client: RestClient):
        """Initialise the GPD client with an already-configured RestClient.

        Args:
            rest_client: RestClient instance built by ``build_gpd_client``.
        """
        self._client = rest_client

    def get_debt_position(self, org_id: str, iupd: str, seg_codes: str = None):
        """Get a single debt position by IUPD.

        Calls ``GET /organizations/{org_id}/debtpositions/{iupd}``.

        Args:
            org_id: organization fiscal code.
            iupd: unique debt-position identifier (IUPD).
            seg_codes: optional segregation codes query parameter.

        Returns:
            requests.Response from the GPD API.
        """
        path = f"/organizations/{org_id}/debtpositions/{iupd}"
        params = {}
        if seg_codes:
            params["segregationCodes"] = seg_codes
        logging.debug("[GPD] GET %s params=%s", path, params or None)
        return self._client.get(path, params=params if params else None)

    def get_debt_position_by_iuv(self, org_id: str, iuv: str, seg_codes: str = None):
        """Get a debt position by IUV (payment option identifier).

        Calls ``GET /organizations/{org_id}/paymentoptions/{iuv}/debtposition``.

        Args:
            org_id: organization fiscal code.
            iuv: unique payment identifier (IUV).
            seg_codes: optional segregation codes query parameter.

        Returns:
            requests.Response from the GPD API.
        """
        path = f"/organizations/{org_id}/paymentoptions/{iuv}/debtposition"
        params = {}
        if seg_codes:
            params["segregationCodes"] = seg_codes
        logging.debug("[GPD] GET %s params=%s", path, params or None)
        return self._client.get(path, params=params if params else None)
