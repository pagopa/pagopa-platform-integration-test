import os
import logging
from behave import given, when, then

from src.e2e.checkout import locate_click_and_type, get_page

logger = logging.getLogger(__name__)

LABEL_SELECTORS = {
    "Codice Fiscale Ente Creditore": "#cf-label",
    "Codice Avviso": "#billCode-label",
    "Indirizzo email": "#email-label",
    "Ripeti di nuovo": "#confirmEmail-label"
}
ERROR_LABEL_SELECTORS = {
    "Codice Fiscale Ente Creditore": "#cf-helper-text",
    "Codice Avviso": "#billCode-helper-text",
    "Indirizzo email": "#email-helper-text",
    "Ripeti di nuovo": "#confirmEmail-helper-text"
}

#──────────────────────────────────────────────
# GIVEN steps (Background)
#──────────────────────────────────────────────


#──────────────────────────────────────────────
# WHEN steps
#──────────────────────────────────────────────
@when(u'L’utente Inserisce il codice avviso {codice_avviso} all’interno della pagina')
def step_enter_notice_code(context, codice_avviso):
    """Enter the notice code into the form."""
    page = get_page(context)
    locate_click_and_type(page, "#billCode", codice_avviso)

@when(u'L’utente Inserisce il CF ente {cf_ente} all’interno della pagina')
def step_enter_cf_ente(context, cf_ente):
    """Enter the CF ente into the form."""
    page = get_page(context)
    locate_click_and_type(page, "#cf", cf_ente)

@when(u'L’utente Inserisce l’indirizzo email {indirizzo_email} in uno dei due campi email presenti nella pagina')
def step_enter_email(context, indirizzo_email):
    """Enter the email address into the form."""
    page = get_page(context)
    locate_click_and_type(page, "#email", indirizzo_email)

@when(u'L’utente inserisce un indirizzo email valido nel campo "Indirizzo Email"')
def step_enter_valid_email(context):
    page = get_page(context)
    locate_click_and_type(page, "#email", "valid@example.com")

@when(u'L’utente inserisce un indirizzo email valido ma diverso dal precedente nel campo "Ripeti di nuovo"')
def step_enter_different_valid_email(context):
    page = get_page(context)
    locate_click_and_type(page, "#confirmEmail", "different_valid@example.com")

@when(u'L’utente lascia vuoto il solo campo "{campo}"')
def step_leave_field_empty(context, campo):
    page = get_page(context)
    if campo == 'Codice Avviso':
        step_enter_cf_ente(context, "77777777777")
    elif campo == 'Codice Fiscale Ente Creditore':
        step_enter_notice_code(context, "77777777777")
    elif campo == 'Indirizzo email':
        step_enter_different_valid_email(context)
    elif campo == 'Ripeti di nuovo':
        step_enter_valid_email(context)

#──────────────────────────────────────────────
# THEN steps
#──────────────────────────────────────────────
@then('Il campo "{field}" viene segnalato in rosso')
def step_check_field_code_red(context, field):
    page = get_page(context)
    # Check if the input field has a red border or error class
    locator = page.locator(LABEL_SELECTORS[field])
    is_error = locator.evaluate("el => el.classList.contains('css-wggati') && el.classList.contains('Mui-error')")
    classes = locator.get_attribute("class") or ""
    assert is_error, f"Il campo {field} non è segnalato in rosso. Classe attuale: {classes}"

@then(u'Viene mostrato il messaggio "{messaggio}" sotto il campo "{field}"')
def step_check_field_message(context,messaggio, field):
    page = get_page(context)
    logger.debug(f"Verifica del messaggio di errore per il campo {field}: {messaggio}")
    locator = page.locator(ERROR_LABEL_SELECTORS[field])
    message = locator.text_content()
    if message != messaggio:
        raise AssertionError(f"Messaggio non corretto: {message}")