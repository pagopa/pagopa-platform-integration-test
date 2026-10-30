# 1. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Postepay" viene completato con successo`
- **message**: playwright._impl._errors.TimeoutError: Locator.wait_for: Timeout 30000ms exceeded.
Call log:
  - waiting for locator("#frame_CARD_NUMBER") to be visible
    7 × locator resolved to hidden <iframe seamless="" id="frame_CARD_NUMBER"></iframe>
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 146, in step_fill_card_number
    page.locator("#frame_CARD_NUMBER").wait_for(state="visible", timeout=30000)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/playwright/sync_api/_generated.py", line 17975, in wait_for
    self._sync(self._impl_obj.wait_for(timeout=timeout, state=state))
```
### Root cause
The card number iframe (`#frame_CARD_NUMBER`) remained hidden and failed to become visible within the 30000ms timeout during card details entry.

### Category
application bug

### Recommended action
Investigate NPG frontend integration and SDK initialization to ensure the card input iframe renders and unhides correctly on page load.

---

# 2. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Wordline" viene completato con successo`
- **message**: playwright._impl._errors.TimeoutError: Locator.wait_for: Timeout 30000ms exceeded.
Call log:
  - waiting for locator("#frame_CARD_NUMBER") to be visible
    6 × locator resolved to hidden <iframe seamless="" id="frame_CARD_NUMBER"></iframe>
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 146, in step_fill_card_number
    page.locator("#frame_CARD_NUMBER").wait_for(state="visible", timeout=30000)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/playwright/sync_api/_generated.py", line 17975, in wait_for
    self._sync(self._impl_obj.wait_for(timeout=timeout, state=state))
```
### Root cause
The card number iframe (`#frame_CARD_NUMBER`) stayed hidden during the authenticated Wordline payment flow, causing a 30s timeout.

### Category
application bug

### Recommended action
Check NPG component loading state and authenticated checkout session initialization for Wordline payment configuration.

---

# 3. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Wordline" viene completato con successo`
- **message**: playwright._impl._errors.TimeoutError: Locator.wait_for: Timeout 30000ms exceeded.
Call log:
  - waiting for locator("#frame_CARD_NUMBER") to be visible
    6 × locator resolved to hidden <iframe seamless="" id="frame_CARD_NUMBER"></iframe>
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 146, in step_fill_card_number
    page.locator("#frame_CARD_NUMBER").wait_for(state="visible", timeout=30000)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/playwright/sync_api/_generated.py", line 17975, in wait_for
    self._sync(self._impl_obj.wait_for(timeout=timeout, state=state))
```
### Root cause
The NPG card input iframe (`#frame_CARD_NUMBER`) failed to show up within 30000ms in the standard Wordline payment scenario.

### Category
application bug

### Recommended action
Verify NPG field injection logic and network calls to the Wordline gateway during session setup.

---

# 4. Flusso lista PSP - indietro da /inserisci-carta (flusso carta con enablePspPage=true)
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Flusso lista PSP - indietro da /inserisci-carta (flusso carta con enablePspPage=true)`
- **message**: RuntimeError: Timeout on locator 'button:has-text('Indietro')' after 5000 ms (url: https://dev.checkout.pagopa.it/)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/e2e/checkout/steps/back_navigation.py", line 88, in step_click_button
    locate_and_click(page, BUTTON_SELECTORS[button_text])
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
```
### Root cause
The "Indietro" button (`button:has-text('Indietro')`) was not visible or present on the page within the 5000ms timeout on `https://dev.checkout.pagopa.it/`.

### Category
application bug

### Recommended action
Verify that the back button is correctly rendered on the `/inserisci-carta` step when `enablePspPage=true` is enabled, or adjust step timeouts if page transition is slow.

---

# 5. Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1
- **status**: failed
- **fullName**: `Attivazione pagamento Checkout: Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999`
- **message**: AssertionError: Expected modal header to contain 'Non riusciamo a trovare l’avviso', but got: 'L’Ente Creditore sta avendo problemi nella risposta'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 245, in step_error_modal_header
    assert expected_header in header_text, (
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
The error modal header displayed an unexpected error message ("L’Ente Creditore sta avendo problemi nella risposta") instead of the expected unknown notice text ("Non riusciamo a trovare l’avviso").

### Category
application bug

### Recommended action
Verify error mapping for `PAA_PAGAMENTO_SCONOSCIUTO` error responses in the frontend modal rendering logic.

---

# 6. Flusso lista PSP - indietro da /scegli-metodo (wallet salvato con enablePspPage=true)
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Flusso lista PSP - indietro da /scegli-metodo (wallet salvato con enablePspPage=true)`
- **message**: RuntimeError: Timeout on locator 'button:has-text('Indietro')' after 5000 ms (url: https://dev.checkout.pagopa.it/)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/e2e/checkout/steps/back_navigation.py", line 88, in step_click_button
    locate_and_click(page, BUTTON_SELECTORS[button_text])
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
```
### Root cause
The locator `button:has-text('Indietro')` timed out after 5000ms while navigating back from `/scegli-metodo`.

### Category
application bug

### Recommended action
Ensure the Back button component is rendered on `/scegli-metodo` view when a saved wallet is present and `enablePspPage=true`.

---

# 7. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Postepay" viene completato con successo`
- **message**: playwright._impl._errors.TimeoutError: Locator.wait_for: Timeout 30000ms exceeded.
Call log:
  - waiting for locator("#frame_CARD_NUMBER") to be visible
    6 × locator resolved to hidden <iframe seamless="" id="frame_CARD_NUMBER"></iframe>
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 146, in step_fill_card_number
    page.locator("#frame_CARD_NUMBER").wait_for(state="visible", timeout=30000)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/playwright/sync_api/_generated.py", line 17975, in wait_for
    self._sync(self._impl_obj.wait_for(timeout=timeout, state=state))
```
### Root cause
The Postepay card frame `#frame_CARD_NUMBER` remained hidden during authenticated payment execution.

### Category
application bug

### Recommended action
Inspect NPG SDK integration and check if authenticated user session state prevents card frame display.

---

# 8. Un pagamento con configurazione carta "Worldpay" viene completato con successo -- @1.3
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Worldpay" viene completato con successo`
- **message**: playwright._impl._errors.TimeoutError: Locator.wait_for: Timeout 30000ms exceeded.
Call log:
  - waiting for locator("#frame_CARD_NUMBER") to be visible
    6 × locator resolved to hidden <iframe seamless="" id="frame_CARD_NUMBER"></iframe>
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 146, in step_fill_card_number
    page.locator("#frame_CARD_NUMBER").wait_for(state="visible", timeout=30000)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/playwright/sync_api/_generated.py", line 17975, in wait_for
    self._sync(self._impl_obj.wait_for(timeout=timeout, state=state))
```
### Root cause
The iframe locator `#frame_CARD_NUMBER` remained hidden for 30 seconds during Worldpay card processing.

### Category
application bug

### Recommended action
Check NPG session initialization calls and backend connectivity for Worldpay payment provider configuration.

---

# 9. Un pagamento con configurazione carta "Worldpay" viene completato con successo -- @1.3
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Worldpay" viene completato con successo`
- **message**: playwright._impl._errors.TimeoutError: Locator.wait_for: Timeout 30000ms exceeded.
Call log:
  - waiting for locator("#frame_CARD_NUMBER") to be visible
    7 × locator resolved to hidden <iframe seamless="" id="frame_CARD_NUMBER"></iframe>
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 146, in step_fill_card_number
    page.locator("#frame_CARD_NUMBER").wait_for(state="visible", timeout=30000)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/playwright/sync_api/_generated.py", line 17975, in wait_for
    self._sync(self._impl_obj.wait_for(timeout=timeout, state=state))
```
### Root cause
The `#frame_CARD_NUMBER` iframe did not turn visible within 30000ms during authenticated Worldpay checkout.

### Category
application bug

### Recommended action
Debug client-side iframe mount logic and verify NPG microservice responses for Worldpay authenticated flow.

---

# 10. Flusso lista PSP - indietro da /inserisci-carta (flusso carta con enablePspPage=true)
- **status**: broken
- **fullName**: `features.FEAT_005_Checkout - Back Navigation Control.Navigazione Lineare per il flusso di Pagamento.Flusso lista PSP - indietro da /inserisci-carta (flusso carta con enablePspPage=true)`
- **message**: Timeout on locator 'button:has-text('Indietro')' after 5000 ms (url: https://dev.checkout.pagopa.it/)
- **trace**:
```
Failing step: Quando L’utente clicca sul tasto "Indietro" ... failed in 5.004s
Location: src/e2e/checkout/features/FEAT_005_Checkout - Back Navigation Control.feature:132
Traceback (most recent call last):
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 93, in locate_and_click
    to_click.wait_for(state="visible", timeout=timeout)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/playwright/sync_api/_generated.py", line 17975, in wait_for
    self._sync(self._impl_obj.wait_for(timeout=timeout, state=state))
    ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/playwright/_impl/_sync_base.py", line 115, in _sync
```
### Root cause
The back button `button:has-text('Indietro')` failed to appear within 5000ms during step navigation.

### Category
application bug

### Recommended action
Verify header/navigation button visibility on `/inserisci-carta` and confirm locator strategy matches UI elements.

---

# 11. Flusso lista PSP - indietro da /scegli-metodo (wallet salvato con enablePspPage=true)
- **status**: broken
- **fullName**: `features.FEAT_005_Checkout - Back Navigation Control.Navigazione Lineare per il flusso di Pagamento.Flusso lista PSP - indietro da /scegli-metodo (wallet salvato con enablePspPage=true)`
- **message**: Timeout on locator 'button:has-text('Indietro')' after 5000 ms (url: https://dev.checkout.pagopa.it/)
- **trace**:
```
Failing step: Quando L’utente clicca sul tasto "Indietro" ... failed in 5.005s
Location: src/e2e/checkout/features/FEAT_005_Checkout - Back Navigation Control.feature:142
Traceback (most recent call last):
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 93, in locate_and_click
    to_click.wait_for(state="visible", timeout=timeout)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/playwright/sync_api/_generated.py", line 17975, in wait_for
    self._sync(self._impl_obj.wait_for(timeout=timeout, state=state))
    ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/playwright/_impl/_sync_base.py", line 115, in _sync
```
### Root cause
The back navigation action timed out after 5 seconds waiting for the "Indietro" button locator on `/scegli-metodo`.

### Category
application bug

### Recommended action
Ensure consistent rendering of the "Indietro" button on `/scegli-metodo` view when saved wallets are rendered.

---

# 12. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `features.checkout_npg.Attivazione pagamento Checkout.Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1`
- **message**: Locator.wait_for: Timeout 30000ms exceeded.
Call log:
  - waiting for locator("#frame_CARD_NUMBER") to be visible
    7 × locator resolved to hidden <iframe seamless="" id="frame_CARD_NUMBER"></iframe>
- **trace**:
```
Failing step: E L'utente inserisce il numero carta "5255000260000014" ... failed in 30.004s
Location: src/e2e/checkout/features/checkout_npg.feature:31
Traceback (most recent call last):
  File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 146, in step_fill_card_number
```
### Root cause
The NPG card input iframe (`#frame_CARD_NUMBER`) was present in the DOM but remained hidden during Postepay payment test execution.

### Category
application bug

### Recommended action
Check front-end iframe unhiding logic after successful NPG build fields completion.

---

# 13. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
- **status**: broken
- **fullName**: `features.checkout_npg.Attivazione pagamento Checkout.Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2`
- **message**: Locator.wait_for: Timeout 30000ms exceeded.
Call log:
  - waiting for locator("#frame_CARD_NUMBER") to be visible
    6 × locator resolved to hidden <iframe seamless="" id="frame_CARD_NUMBER"></iframe>
- **trace**:
```
Failing step: E L'utente inserisce il numero carta "5255000260000014" ... failed in 30.003s
Location: src/e2e/checkout/features/checkout_npg.feature:31
Traceback (most recent call last):
  File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 146, in step_fill_card_number
```
### Root cause
30-second Playwright timeout waiting for `#frame_CARD_NUMBER` iframe visibility in Wordline payment step.

### Category
application bug

### Recommended action
Verify NPG field initialization scripts and iframe styling transitions for Wordline provider.

---

# 14. Un pagamento con configurazione carta "Worldpay" viene completato con successo -- @1.3
- **status**: broken
- **fullName**: `features.checkout_npg.Attivazione pagamento Checkout.Un pagamento con configurazione carta "Worldpay" viene completato con successo -- @1.3`
- **message**: Locator.wait_for: Timeout 30000ms exceeded.
Call log:
  - waiting for locator("#frame_CARD_NUMBER") to be visible
    6 × locator resolved to hidden <iframe seamless="" id="frame_CARD_NUMBER"></iframe>
- **trace**:
```
Failing step: E L'utente inserisce il numero carta "4242424242424242" ... failed in 30.003s
Location: src/e2e/checkout/features/checkout_npg.feature:31
Traceback (most recent call last):
  File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 146, in step_fill_card_number
```
### Root cause
The card input frame (`#frame_CARD_NUMBER`) failed to transition to visible state for Worldpay card flow.

### Category
application bug

### Recommended action
Investigate frontend NPG integration for Worldpay to ensure iframe visibility is toggled correctly.

---

# 15. Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1
- **status**: failed
- **fullName**: `features.checkout_npg.Attivazione pagamento Checkout.Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1`
- **message**: Expected modal header to contain 'Non riusciamo a trovare l’avviso', but got: 'L’Ente Creditore sta avendo problemi nella risposta'
- **trace**:
```
Failing step: E L'intestazione della modale di errore contiene "Non riusciamo a trovare l’avviso" ... failed in 0.006s
Location: src/e2e/checkout/features/checkout_npg.feature:57
Assertion Failed: Expected modal header to contain 'Non riusciamo a trovare l’avviso', but got: 'L’Ente Creditore sta avendo problemi nella risposta'
```
### Root cause
Assertion failure caused by modal header showing generic creditor error text instead of specific unknown notice message.

### Category
application bug

### Recommended action
Fix error handling logic in the frontend application so that `PAA_PAGAMENTO_SCONOSCIUTO` maps to the user-friendly "Non riusciamo a trovare l’avviso" header.

---

# 16. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `features.checkout_npg_auth.Attivazione pagamento Checkout autenticato.Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1`
- **message**: Locator.wait_for: Timeout 30000ms exceeded.
Call log:
  - waiting for locator("#frame_CARD_NUMBER") to be visible
    6 × locator resolved to hidden <iframe seamless="" id="frame_CARD_NUMBER"></iframe>
- **trace**:
```
Failing step: E L'utente inserisce il numero carta "5255000260000014" ... failed in 30.002s
Location: src/e2e/checkout/features/checkout_npg_auth.feature:32
Traceback (most recent call last):
  File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 146, in step_fill_card_number
```
### Root cause
The `#frame_CARD_NUMBER` iframe remained hidden during authenticated Postepay payment setup.

### Category
application bug

### Recommended action
Verify NPG field creation logic in authenticated Checkout context.

---

# 17. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
- **status**: broken
- **fullName**: `features.checkout_npg_auth.Attivazione pagamento Checkout autenticato.Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2`
- **message**: Locator.wait_for: Timeout 30000ms exceeded.
Call log:
  - waiting for locator("#frame_CARD_NUMBER") to be visible
    6 × locator resolved to hidden <iframe seamless="" id="frame_CARD_NUMBER"></iframe>
- **trace**:
```
Failing step: E L'utente inserisce il numero carta "5255000260000014" ... failed in 30.001s
Location: src/e2e/checkout/features/checkout_npg_auth.feature:32
Traceback (most recent call last):
  File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 146, in step_fill_card_number
```
### Root cause
The card number iframe (`#frame_CARD_NUMBER`) timed out after 30000ms while remaining hidden in authenticated Wordline payment.

### Category
application bug

### Recommended action
Debug client-side NPG iframe loader to ensure hidden attributes are cleared upon successful field initialization.

---

# 18. Un pagamento con configurazione carta "Worldpay" viene completato con successo -- @1.3
- **status**: broken
- **fullName**: `features.checkout_npg_auth.Attivazione pagamento Checkout autenticato.Un pagamento con configurazione carta "Worldpay" viene completato con successo -- @1.3`
- **message**: Locator.wait_for: Timeout 30000ms exceeded.
Call log:
  - waiting for locator("#frame_CARD_NUMBER") to be visible
    7 × locator resolved to hidden <iframe seamless="" id="frame_CARD_NUMBER"></iframe>
- **trace**:
```
Failing step: E L'utente inserisce il numero carta "4242424242424242" ... failed in 30.002s
Location: src/e2e/checkout/features/checkout_npg_auth.feature:32
Traceback (most recent call last):
  File "/opt/hostedtoolcache/Python/3.14.8/