import os
import logging
from pathlib import Path
from playwright.sync_api import sync_playwright

def _load_env_file(env_file: str) -> None:
    path = Path(env_file)
    if not path.is_file():
        raise RuntimeError(f"File env non trovato: {env_file}")

    lines = path.read_text(encoding="utf-8").splitlines()
    i = 0

    while i < len(lines):
        raw_line = lines[i]
        line = raw_line.strip()

        # Skip empty/comment lines
        if not line or line.startswith("#"):
            i += 1
            continue

        # Skip malformed lines without '='
        if "=" not in raw_line:
            logging.debug("Skipping malformed env line %d: %r", i + 1, raw_line)
            i += 1
            continue

        key, value = raw_line.split("=", maxsplit=1)
        key = key.strip()
        value = value.strip()

        if not key:
            logging.debug("Skipping env line with empty key at %d: %r", i + 1, raw_line)
            i += 1
            continue

        # Quoted value handling (single-line or multi-line)
        if value.startswith(("'", '"')):
            quote = value[0]

            # Case A: quoted single-line, e.g. KEY="abc"
            if len(value) >= 2 and value.endswith(quote):
                parsed_value = value[1:-1]
                os.environ.setdefault(key, parsed_value)
                logging.debug("Loaded env var from file: %s=<quoted single-line>", key)
                i += 1
                continue

            # Case B: quoted multi-line
            buffer = [value[1:]]  # remainder after opening quote on first line
            i += 1
            closed = False

            while i < len(lines):
                current = lines[i]
                if current.endswith(quote):
                    buffer.append(current[:-1])  # remove closing quote
                    closed = True
                    break
                buffer.append(current)
                i += 1

            if not closed:
                raise RuntimeError(
                    f"Valore quotato multi-linea non chiuso per chiave '{key}' nel file {env_file}"
                )

            parsed_value = "\n".join(buffer)
            os.environ.setdefault(key, parsed_value)
            logging.debug("Loaded env var from file: %s=<quoted multi-line>", key)

            i += 1
            continue

        # Unquoted single-line value
        os.environ.setdefault(key, value)
        logging.debug("Loaded env var from file: %s=%s", key, value)
        i += 1

def before_all(context):
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                        force=True)
    # Opzionale: carica un file env passando ENV_FILE (es. .\dev.env)
    env_file = os.getenv("ENV_FILE")
    if env_file:
        _load_env_file(env_file)

    logging.debug("Environment variables after loading env file: %s", dict(os.environ))

    context.timeout_ms = int(os.getenv("E2E_TIMEOUT_MS", "80000"))

    context._playwright = sync_playwright().start()
    headless = os.getenv("HEADLESS", "true").lower() in {"1", "true", "yes", "on"}
    context.browser = context._playwright.chromium.launch(
        channel="chrome",
        headless=headless,
        args=["--no-sandbox"],
    )


def before_scenario(context, scenario):
    context.browser_context = context.browser.new_context(
        viewport={"width": 1200, "height": 907}
    )
    context.page = context.browser_context.new_page()
    context.page.set_default_timeout(context.timeout_ms)
    context.page.set_default_navigation_timeout(context.timeout_ms)

def after_scenario(context, scenario):
    if hasattr(context, "browser_context"):
        context.browser_context.close()


def after_all(context):
    if hasattr(context, "browser"):
        context.browser.close()
    if hasattr(context, "_playwright"):
        context._playwright.stop()