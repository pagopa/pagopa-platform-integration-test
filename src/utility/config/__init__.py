"""Config utility package.

Espone:
- load_test_config: carica il file JSON selezionato via env var
- load_json_config: carica un file JSON dal percorso specificato
"""

from src.utility.config.config_loader import load_json_config, load_test_config

__all__ = ["load_json_config", "load_test_config"]

