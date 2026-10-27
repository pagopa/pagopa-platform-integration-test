# 1. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Wordline" viene completato con successo`
- **message**: playwright._impl._errors.TimeoutError: Locator.wait_for: Timeout 120000ms exceeded.
- **trace**:
```
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 303, in step_check_payment_success
    page.locator(result_title_selector).wait_for(
        state="visible", timeout=120000
    )
```
### Root cause
The 3DS/NPG payment gateway authorization timed out waiting for the success message title element to appear.

### Category
environment

### Recommended action
Check external gateway availability (Nexi/Wordline 3DS) and verify if network latency or callbacks caused the delay.

---

# 2. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Postepay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://uat.checkout.pagopa.it/lista-psp)
- **trace**:
```
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 188, in step_select_psp
    locate_and_click(page, f"#psp-radio-{psp_id}")
```
### Root cause
The PSP selection radio button for Postepay did not render within the 5-second timeout on the checkout page.

### Category
application bug

### Recommended action
Investigate frontend rendering performance or API loading issues on the PSP list page.

---

# 3. Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1
- **status**: failed
- **fullName**: `Attivazione pagamento Checkout: Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999`
- **message**: AssertionError: Expected modal header to contain 'Non riusciamo a trovare l’avviso', but got: 'L’Ente Creditore sta avendo problemi nella risposta'
- **trace**:
```
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 245, in step_error_modal_header
    assert expected_header in header_text, (
```
### Root cause
The system returned a generic creditor issuer error instead of the expected 'Notice not found' error message modal.

### Category
application bug

### Recommended action
Verify backend handling and error mapping for invalid notice code ranges to ensure correct error codes are exposed.

---

# 4. Utente paga un pagamento singolo con un versamento e una marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo da posizione debitoria esistente tramite nodoInviaRPT: Utente paga un pagamento singolo con un versamento e una marca da bollo gia esistente in GPD`
- **message**: AssertionError: The field [paymentToken] does not exists.
- **trace**:
```
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 865, in send_index_activatePaymentNoticeV2_request
    check_field_with_non_null_value(context, 'paymentToken')
```
### Root cause
The `activatePaymentNoticeV2` API request failed to return a `paymentToken`, breaking the redirection flow to checkout across multiple WISP test cases.

### Category
application bug

### Recommended action
Debug the upstream activation service to determine why payment tokens are not being generated during notice activation.

---

## Common patterns
- **Checkout UI Locators**: Timeouts finding PSP radio elements point to frontend stability or slow loading components.
- **WISP Activation Failures**: A systemic failure across WISP scenarios where `paymentToken` is missing from the `activatePaymentNoticeV2` response, indicating an upstream integration or service dependency outage.

---

FDR-3 test execution was complete with no tests skipped.