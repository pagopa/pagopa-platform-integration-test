import logging
import time

from behave import given, when, then
from src.e2e.checkout import get_page, get_required_config, generate_random_notice_code, locate_and_click, locate_click_and_type
from src.e2e.checkout.helper import get_page_url
from steps.checkout_npg import step_enter_notice_random, step_enter_fiscal_code, step_click_verify, \
    step_click_pay_on_summary, step_confirm_email, step_select_payment_method, step_fill_card_number, \
    step_fill_expiration_date, step_fill_security_code, step_fill_cardholder_name

logger = logging.getLogger(__name__)

BUTTON_SELECTORS = {
    "Inserisci tu i dati":"[data-testid='KeyboardIcon']",
    "Indietro":"button:has-text('Indietro')",
    "Continua":"button:has-text('Continua')",
    "Vai al pagamento":"button:has-text('Vai al pagamento')",
    "Carte di Credito":"[data-qaid=CP]"
}

#──────────────────────────────────────────────
# GIVEN steps (Background)
#──────────────────────────────────────────────
@given(u'L’utente si trova sulla pagina "{page_url}"')
def step_on_page(context, page_url):
    """Check the page URL"""
    navigate_to_page(context, page_url)
    current_url = get_page_url(context)
    assert current_url == page_url, f"Expected page '{page_url}', but found '{current_url}'"

@given(u'L’utente ha compilato i dati avviso inserendo il codice avviso "{notice_code}" e il CF ente "{fiscal_code}"')
def step_enter_notice_data(context, notice_code, fiscal_code):
    """Enter notice data into the form."""
    page = context.page
    locate_click_and_type(page, "#billCode", notice_code)
    locate_click_and_type(page, "#cf", fiscal_code)

@given(u'L’utente ha inserito l’indirizzo email "{email}" in entrambi i campi della maschera')
def step_enter_email(context, email):
    """Enter email into both fields of the form."""
    page = context.page
    locate_click_and_type(page, "#email", email)
    locate_click_and_type(page, "#confirmEmail", email)

@given(u'L’utente naviga sulla pagina "{page_url}" selezionata da bookmark o URL diretto')
def step_on_insert_notice_data_page(context, page_url):
    """Check if the user is on the specified page."""
    page = get_page(context)
    checkout_url = get_required_config(context, "CHECKOUT_URL") + str(page_url).replace('/', '')
    logger.debug("Opening checkout page: %s", checkout_url)
    page.goto(checkout_url, wait_until="domcontentloaded")
    current_url = get_page_url(context)
    assert current_url == page_url, f"Expected page '{page_url}', but found '{current_url}'"

@given(u'L’utente ha cliccato sul tasto "{button_text}"')
def step_click_button_given(context, button_text):
    step_click_button(context, button_text)

@given(u'L’utente ha raggiunto la pagina "/lista-psp" dall’entry point "/scegli-metodo" (metodo APM)')
def step_on_psp_list_page(context):
    pass

@given(u'L’utente ha raggiunto la pagina "/lista-psp" dall’entry point "/inserisci-carta" (flusso carta con enablePspPage=true)')
def step_on_psp_list_page_from_card_flow(context):
    pass

@given(u'L’utente ha raggiunto la pagina "/lista-psp" dall’entry point "/scegli-metodo" (wallet salvato con enablePspPage=true)')
def step_on_psp_list_page_from_wallet_flow(context):
    pass

#──────────────────────────────────────────────
# WHEN steps
#──────────────────────────────────────────────
@when(u'L’utente clicca sul tasto "{button_text}"')
def step_click_button(context, button_text):
    """Click a button with the specified text."""
    page = get_page(context)
    logger.debug("Clicking button: %s with selector %s", button_text, BUTTON_SELECTORS[button_text])
    locate_and_click(page, BUTTON_SELECTORS[button_text])
    page.wait_for_load_state("networkidle", timeout=5000)


@when(u'L’utente clicca ripetutamente sul tasto "Indietro"')
def step_click_back_button(context):
    """Click the back button repeatedly."""
    context.loop_page_error = False
    context.visited_pages = []
    context.visited_pages_set = set()

    while True and not context.loop_page_error:
        page = get_page(context)
        current_url = get_page_url(context)
        logger.info("Current URL before clicking back: %s", current_url)

        if current_url == "/":
            logger.info("Raggiunta la home page: %s", current_url)
            break

        if current_url in context.visited_pages_set:
            logger.error("Loop rilevato: pagina già visitata -> %s", current_url)
            context.loop_page_error = True

        context.visited_pages_set.add(current_url)
        context.visited_pages.append(current_url)
    
        locate_and_click(page, BUTTON_SELECTORS["Indietro"])
        page.wait_for_load_state("networkidle")

#──────────────────────────────────────────────
# THEN steps
#──────────────────────────────────────────────
@then(u'L’utente viene reindirizzato sulla pagina "{page_url}"')
def step_verify_redirect(context, page_url):
    """Verify that the user is redirected to the specified page."""
    current_url = get_page_url(context)
    assert current_url == page_url, f"Expected to be redirected to '{page_url}', but found '{current_url}'"

@then(u'L’utente ritorna sulla HP dopo aver visitato una ed una sola volta, in ordine, le pagine "/inserisci-email", "/dati-pagamento", "/inserisci-dati-avviso", senza ripetizioni né ritorni a pagine già visitate')
def step_verify_linear_navigation(context):
    assert context.loop_page_error == False, f"Navigation loop identified, visited pages {visited_pages}"
    """Verify that the user has visited the pages in a linear order without repetitions."""
    expected_pages = [
        "/inserisci-email",
        "/dati-pagamento",
        "/inserisci-dati-avviso"
    ]
    visited_pages = context.visited_pages  # This should be a list of pages visited during the test
    assert visited_pages == expected_pages, f"Expected to visit pages {expected_pages} in order, but visited {visited_pages}"

@then(u'L’utente ritorna sulla HP senza uscire dall’applicativo')
def step_verify_return_to_home(context):
    """Verify that the user returns to the home page without exiting the application."""
    page = get_page(context)
    current_url = get_page_url(context)
    assert current_url == "/", f"Expected to return to home page '/', but found '{current_url}'"



#──────────────────────────────────────────────
# UTILITY
#──────────────────────────────────────────────
def navigate_to_page(context, page_url):
    if page_url == "/": #homepage - DO NOTHING
        return
    elif page_url == "/inserisci-dati-avviso": naviga_inserisci_dati_avviso(context)
    elif page_url == "/dati-pagamento": naviga_dati_pagamento(context)
    elif page_url == "/inserisci-email": naviga_inserisci_email(context)
    elif page_url == "/scegli-metodo": naviga_scegli_metodo(context)
    elif page_url == "/inserisci-carta": naviga_inserisci_carta(context)
    elif page_url == "/lista-psp": naviga_lista_psp(context)
    elif page_url == "/riepilogo-pagamento": naviga_riepilogo_pagamento(context)


def naviga_inserisci_dati_avviso(context):
    locate_and_click(context.page, BUTTON_SELECTORS["Inserisci tu i dati"])
    get_page(context).wait_for_load_state("load")

def naviga_dati_pagamento(context):
    naviga_inserisci_dati_avviso(context)
    notice_code = generate_random_notice_code("30200")
    locate_click_and_type(get_page(context), "#billCode", notice_code)
    step_enter_fiscal_code(context, "77777777777")
    step_click_verify(context)
    get_page(context).wait_for_load_state("load")

def naviga_inserisci_email(context):
    naviga_dati_pagamento(context)
    step_click_pay_on_summary(context)
    get_page(context).wait_for_load_state("load")

def naviga_scegli_metodo(context):
    naviga_inserisci_email(context)
    step_enter_email(context, "ecommerce-test-mailgroup@pagopa.it")
    step_confirm_email(context, "ecommerce-test-mailgroup@pagopa.it")
    get_page(context).wait_for_load_state("load")

def naviga_inserisci_carta(context):
    naviga_scegli_metodo(context)
    step_select_payment_method(context,"CP")
    get_page(context).wait_for_load_state("load")

def naviga_lista_psp(context):
    naviga_scegli_metodo(context)
    step_select_payment_method(context,"PPAL")
    get_page(context).wait_for_load_state("load")
    get_page(context).wait_for_timeout(5000) #Momentaneo

def naviga_riepilogo_pagamento(context):
    naviga_lista_psp(context)
    page = get_page(context)
    locate_and_click(page, "#psp-radio-MOONITMMXXX")
    locate_and_click(page, "#paymentPspListPageButtonContinue")
