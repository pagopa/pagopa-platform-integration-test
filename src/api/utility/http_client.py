import os
import ssl
from functools import lru_cache

import requests
from requests.adapters import HTTPAdapter
from urllib3 import PoolManager


class _SSLContextAdapter(HTTPAdapter):
    def __init__(self, ssl_context: ssl.SSLContext, *args, **kwargs):
        self._ssl_context = ssl_context
        super().__init__(*args, **kwargs)

    def init_poolmanager(self, connections, maxsize, block=False, **pool_kwargs):
        pool_kwargs["ssl_context"] = self._ssl_context
        self.poolmanager = PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            **pool_kwargs,
        )

    def proxy_manager_for(self, proxy, **proxy_kwargs):
        proxy_kwargs["ssl_context"] = self._ssl_context
        return super().proxy_manager_for(proxy, **proxy_kwargs)


@lru_cache(maxsize=1)
def _get_session() -> requests.Session:
    session = requests.Session()

    ca_bundle = os.environ.get("REQUESTS_CA_BUNDLE") or os.environ.get("SSL_CERT_FILE")
    if ca_bundle:
        session.verify = ca_bundle
        return session

    # Use the OS trust store instead of certifi so corporate/intermediate CAs
    # installed on the machine are honored during local test runs.
    ssl_context = ssl.create_default_context()
    session.mount("https://", _SSLContextAdapter(ssl_context))
    return session


def request(method: str, url: str, **kwargs) -> requests.Response:
    return _get_session().request(method=method, url=url, **kwargs)