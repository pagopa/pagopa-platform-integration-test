"""
Utility condivise per la lettura delle variabili d'ambiente nelle suite api-test.
"""
import os
import random


def get_checkout_host() -> str:
    """Restituisce CHECKOUT_HOST, con fallback all'host DEV."""
    return os.environ.get("CHECKOUT_HOST", "https://api.dev.platform.pagopa.it")


def get_required_env(name: str) -> str:
    """Legge una variabile d'ambiente obbligatoria; solleva EnvironmentError se assente."""
    value = os.environ.get(name)
    if not value:
        raise EnvironmentError(f"Environment variable {name!r} not set.")
    return value


def generate_notice_code(prefix_env_var: str = "NOTICE_CODE_PREFIX") -> str:
    """Genera un notice code casuale valido dal prefisso letto dalla variabile d'ambiente indicata."""
    prefix = get_required_env(prefix_env_var)
    min_val = int(prefix + "10000000000000")
    max_val = int(prefix + "19999999999999")
    return str(random.randint(min_val, max_val))
