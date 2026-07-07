"""
Behave environment hooks comuni a tutti i test di api-test.

Responsabilità:
- before_all : carica le variabili d'ambiente dal file src/api/config/.env.<env>
- before_scenario : reset dello stato condiviso tra api-test

I moduli specifici (es. cart) possono aggiungere ulteriore logica di setup/teardown
delegando prima a queste funzioni.
"""
import os

from dotenv import load_dotenv


def _resolve_env_file(env: str) -> str:
    """
    Restituisce il percorso assoluto del file .env per l'ambiente richiesto.
    I file sono in <repo_root>/src/api/config/.env.<env>.
    """
    # src/api/utility/api_test_environment.py -> 2 dirname = src/api/
    api_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(api_root, "config", f".env.{env}")


def before_all(context):
    """
    Carica le variabili d'ambiente dal file .env corretto.
    L'ambiente viene selezionato tramite la variabile TARGET_ENV (default: dev).
    """
    env = os.environ.get("TARGET_ENV", "dev")
    env_file = _resolve_env_file(env)

    if not os.path.exists(env_file):
        raise FileNotFoundError(
            f"[api_test_environment] File di configurazione non trovato: {env_file}"
        )

    load_dotenv(env_file, override=True)
    print(f"\n[api_test_environment] Caricato ambiente: {env} ({env_file})")


def before_scenario(context, scenario):
    """Reset dello stato condiviso prima di ogni scenario."""
    context.response = None
    context.cart_id = None
    context.notice_code = None
    context.fiscal_code = None
    context.location = None
