from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

import requests
from requests.auth import HTTPBasicAuth


# ============================================================================
# Configurazione
# ============================================================================
# Questa dataclass descrive tutto ciò che serve per ottenere un token OAuth2
# con grant type client_credentials.


@dataclass(frozen=True)
class OAuth2TokenRequestConfig:
    """
    Configurazione per la richiesta di un token OAuth2 client credentials.

    Esempio::

        config = OAuth2TokenRequestConfig(
            token_url="https://auth.example.com/oauth/token",
            client_id="my-client-id",
            client_secret="my-client-secret",
            scope="read write",
            audience="my-api",
        )
    """
    token_url: str
    client_id: str
    client_secret: str
    scope: Optional[str] = None
    audience: Optional[str] = None
    extra_token_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OAuth2Token:
    """
    Rappresenta un token OAuth2 con la sua scadenza.

    Esempio::

        token = OAuth2Token(
            access_token="eyJhbGciOiJSUzI1NiJ9...",
            expires_at_epoch=time.time() + 3600,
        )

        if token.is_valid():
            print("Token ancora valido")
        else:
            print("Token scaduto o in scadenza")
    """
    access_token: str
    expires_at_epoch: float

    def is_valid(self, leeway_seconds: int = 30) -> bool:
        """
        Verifica se il token è ancora valido con un margine di sicurezza.

        Args:
            leeway_seconds: secondi di anticipo per il rinnovo (default 30).
                            Un token con meno di 30 secondi alla scadenza
                            viene considerato non valido per evitare race condition.

        Returns:
            True se il token è valido, False se è scaduto o in scadenza.

        Esempio::

            token = OAuth2Token("abc", expires_at_epoch=time.time() + 60)
            token.is_valid()        # → True  (60 sec alla scadenza)
            token.is_valid(90)      # → False (meno di 90 sec alla scadenza)
        """
        return time.time() < (self.expires_at_epoch - leeway_seconds)


class OAuth2TokenProviderError(RuntimeError):
    """Eccezione sollevata in caso di errori nel recupero del token OAuth2."""
    pass


# ============================================================================
# Token provider
# ============================================================================
# Responsabilità:
# - chiamare il token endpoint
# - estrarre access_token e expires_in
# - mantenere il token in cache per-istanza
# - rinnovare il token quando scaduto o prossimo alla scadenza
#
# La cache è per-istanza e per-configurazione, così si può riusare il provider
# nei test Behave o in altri helper senza dipendere da variabili globali.


class OAuth2TokenProvider:
    """
    Provider per token OAuth2 con grant type client_credentials.

    Gestisce automaticamente:
    - recupero del token al primo utilizzo
    - cache in memoria per la durata del token
    - rinnovo automatico quando il token è in scadenza

    Esempio base::

        config = OAuth2TokenRequestConfig(
            token_url="https://auth.example.com/oauth/token",
            client_id="my-client",
            client_secret="my-secret",
            scope="read write",
        )
        provider = OAuth2TokenProvider(config)

        # Primo accesso: chiama il token endpoint
        token = provider.get_token()

        # Accessi successivi: restituisce il token cached finché è valido
        token = provider.get_token()

        # Forza il rinnovo indipendentemente dalla scadenza
        token = provider.refresh_token()

    Esempio in environment.py di Behave::

        def before_all(context):
            config = load_test_config(resolver)
            oauth_node = config["auth"]["oauth2"]

            context.token_provider = OAuth2TokenProvider(
                OAuth2TokenRequestConfig(
                    token_url=oauth_node["token_url"],
                    client_id=oauth_node["client_id"],
                    client_secret=oauth_node["client_secret"],
                    scope=oauth_node.get("scope"),
                )
            )

    Nota: nella maggior parte dei casi non è necessario usare direttamente
    il provider nei test. Il RestClient lo gestisce internamente quando
    viene creato con build_rest_client(..., auth_config=OAuth2ClientCredentialsConfig).
    """

    def __init__(
            self,
            config: OAuth2TokenRequestConfig,
            *,
            timeout: int = 30,
            verify_ssl: bool = True,
            refresh_leeway_seconds: int = 30,
            session: Optional[requests.Session] = None,
    ):
        self.config = config
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.refresh_leeway_seconds = refresh_leeway_seconds
        self.session = session or requests.Session()

        self._cached_token: Optional[OAuth2Token] = None

    def _build_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "grant_type": "client_credentials",
        }

        if self.config.scope:
            payload["scope"] = self.config.scope

        if self.config.audience:
            payload["audience"] = self.config.audience

        payload.update(self.config.extra_token_data)
        return payload

    def _request_token(self) -> OAuth2Token:
        response = self.session.post(
            self.config.token_url,
            data=self._build_payload(),
            auth=HTTPBasicAuth(self.config.client_id, self.config.client_secret),
            timeout=self.timeout,
            verify=self.verify_ssl,
        )

        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise OAuth2TokenProviderError(
                f"OAuth2 token request failed: {response.status_code} - {response.text}"
            ) from exc

        try:
            payload = response.json()
        except ValueError as exc:
            raise OAuth2TokenProviderError(
                f"OAuth2 token response is not valid JSON: {response.text}"
            ) from exc

        access_token = payload.get("access_token")
        if not access_token:
            raise OAuth2TokenProviderError(
                "OAuth2 token response does not contain 'access_token'"
            )

        expires_in = int(payload.get("expires_in", 300))
        expires_at_epoch = time.time() + max(expires_in, 0)

        return OAuth2Token(
            access_token=access_token,
            expires_at_epoch=expires_at_epoch,
        )

    def get_token(self, *, force_refresh: bool = False) -> str:
        """
        Restituisce un access token valido.

        Se il token in cache è ancora valido (con margine refresh_leeway_seconds),
        lo restituisce direttamente. Altrimenti ne richiede uno nuovo.

        Args:
            force_refresh: se True, richiede sempre un nuovo token ignorando la cache.

        Returns:
            Stringa con l'access token.

        Raises:
            OAuth2TokenProviderError: se la chiamata al token endpoint fallisce.

        Esempio::

            provider = OAuth2TokenProvider(config)

            # Usa il cache o ottiene un nuovo token se necessario
            token = provider.get_token()

            # Forza il rinnovo immediato
            token = provider.get_token(force_refresh=True)
        """
        if not force_refresh and self._cached_token and self._cached_token.is_valid(
                self.refresh_leeway_seconds
        ):
            return self._cached_token.access_token

        self._cached_token = self._request_token()
        return self._cached_token.access_token

    def refresh_token(self) -> str:
        """
        Forza il rinnovo del token, ignorando il cache.

        Alias esplicito di get_token(force_refresh=True).
        Utile negli step Behave per testare scenari di token scaduto.

        Returns:
            Stringa con il nuovo access token.

        Esempio::

            # In uno step Behave che simula token scaduto
            @given("il token OAuth2 è scaduto")
            def step_token_expired(context):
                context.token_provider.clear_cache()

            @when("eseguo una chiamata autenticata")
            def step_call(context):
                # Il RestClient rinnova automaticamente il token
                context.response = context.rest_client.get("/resource")
        """
        return self.get_token(force_refresh=True)

    def get_cached_token(self) -> Optional[str]:
        """
        Restituisce il token in cache solo se valido, senza effettuare nuove richieste.

        Returns:
            L'access token se presente e valido, None altrimenti.

        Esempio::

            token = provider.get_cached_token()
            if token:
                print(f"Token cached: {token[:20]}...")
            else:
                print("Nessun token in cache o token scaduto")
        """
        if self._cached_token and self._cached_token.is_valid(self.refresh_leeway_seconds):
            return self._cached_token.access_token
        return None

    def clear_cache(self) -> None:
        """
        Invalida il token in cache, forzando il rinnovo alla prossima chiamata get_token().

        Utile nei test per simulare scenari di token scaduto o per forzare
        il rinnovo tra uno scenario e l'altro.

        Esempio::

            # Pulizia cache tra scenari
            def before_scenario(context, scenario):
                if hasattr(context, "token_provider"):
                    context.token_provider.clear_cache()
        """
        self._cached_token = None

