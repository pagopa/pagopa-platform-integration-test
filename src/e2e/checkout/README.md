# E2E Checkout

Questa cartella contiene la suite Behave + Playwright per i test end-to-end del checkout.

## Configurazione

La suite carica il file di configurazione indicato dalla variabile ambiente `ENV_FILE`.
Il file viene parsato tramite `src.utility.config.config_loader._parse_config_content` e reso disponibile negli step come `context.test_config`.

Formati supportati nel file config:
- `KEY=VALUE`
- `KEY:VALUE`
- valori JSON validi
- valori quotati multi-linea

Esempio locale già presente:
- `dev.env`

## Esecuzione dalla cartella `src/e2e/checkout`

### Dry-run

```powershell
$env:ENV_FILE="dev.env"
python -m behave --dry-run features
```

### Esecuzione completa

```powershell
$env:ENV_FILE="dev.env"
python -m behave features
```

### Esecuzione con tag

```powershell
$env:ENV_FILE="dev.env"
python -m behave --tags=@FEAT_002_Checkout features
```

## Esecuzione dalla root repository

```powershell
$env:ENV_FILE="src/e2e/checkout/dev.env"
python -m behave src/e2e/checkout/features
```

## Debug rapido

### Log verbose Behave

```powershell
$env:ENV_FILE="dev.env"
python -m behave --no-capture --no-capture-stderr features
```

### Solo dry-run per verificare import e step mapping

```powershell
$env:ENV_FILE="dev.env"
python -m behave --dry-run features
```

## Helper condivisi

Gli step possono importare i metodi helper pubblici da:

```python
from src.e2e.checkout import get_page, get_required_config, locate_and_click
```

Export disponibili in `src/e2e/checkout/__init__.py`:
- `get_page`
- `get_required_config`
- `get_required_json_config`
- `generate_random_notice_code`
- `perform_mock_login`
- `locate_and_click`
- `locate_click_and_type`

## Scrittura negli input

Per cliccare su un campo e digitare del testo, usa:

```python
locate_click_and_type(page, "#email", email)
```

Il helper:
1. attende che il locator sia visibile ed esegue il click,
2. tenta di svuotare il valore corrente tramite `fill("")`,
3. scrive il testo carattere per carattere via tastiera (`keyboard.type`).

> **Nota:** non viene eseguita alcuna verifica del valore scritto né alcun retry automatico.
> Questo è intenzionale: i campi carta NPG sono ospitati in iframe cross-origin e il DOM esterno
> non può leggerne il valore. Usare una logica di verifica causerebbe falsi negativi su ogni
> campo carta (`#frame_CARD_NUMBER`, `#frame_EXPIRATION_DATE`, ecc.).

