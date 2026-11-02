## Suite: checkout

# 1. Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1
- **status**: failed
- **fullName**: `Attivazione pagamento Checkout: Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999`
- **message**: AssertionError: Expected modal header to contain 'Non riusciamo a trovare l’avviso', but got: 'L’Ente Creditore sta avendo problemi nella risposta'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 245, in step_error_modal_header
    assert expected_header in header_text, (
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
The error modal displayed a generic Creditor Institution error instead of the expected unknown payment notice error (`PAA_PAGAMENTO_SCONOSCIUTO`).

### Category
application bug

### Recommended action
Verify backend error mapping for notice codes in the range 302400000000000000-302409999999999999 to ensure `PAA_PAGAMENTO_SCONOSCIUTO` is correctly returned.

---

# 2. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Postepay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://uat.checkout.pagopa.it/lista-psp)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 188, in step_select_psp
    locate_and_click(page, f"#psp-radio-{psp_id}")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
Element locator `#psp-radio-PPAYITR1XXX` timed out waiting to become visible on the PSP selection page.

### Category
environment

### Recommended action
Check if PSP ID `PPAYITR1XXX` is active and configured properly in the UAT environment dataset.

---

# 3. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Postepay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://uat.checkout.pagopa.it/lista-psp)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 188, in step_select_psp
    locate_and_click(page, f"#psp-radio-{psp_id}")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
Element locator `#psp-radio-PPAYITR1XXX` timed out waiting to become visible on the PSP selection page during authenticated checkout.

### Category
environment

### Recommended action
Ensure PSP ID `PPAYITR1XXX` is loaded in UAT during authenticated payment flows.

---

# 4. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `features.checkout_npg.Attivazione pagamento Checkout.Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1`
- **message**: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://uat.checkout.pagopa.it/lista-psp)
- **trace**:
```
Failing step: E L'utente seleziona il PSP con id "PPAYITR1XXX" ... failed in 5.067s
Location: src/e2e/checkout/features/checkout_npg.feature:35
Traceback (most recent call last):
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 93, in locate_and_click
    to_click.wait_for(state="visible", timeout=timeout)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/playwright/sync_api/_generated.py", line 17975, in wait_for
    self._sync(self._impl_obj.wait_for(timeout=timeout, state=state))
    ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/playwright/_impl/_sync_base.py", line 115, in _sync
    return task.result()
           ~~~~~~~~~~~^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/playwright/_impl/_locator.py", line 692, in wait_for
    await self._frame.wait_for_selector(
        self._selector, strict=True, timeout=timeout, state=state
    )
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/playwright/_impl/_frame.py", line 369, in wait_for_selector
    await self._channel.send(
        "waitForSelector", self._timeout, locals_to_params(locals())
    )
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/playwright/_impl/_connection.py", line 69, in 
```
### Root cause
Playwright timed out waiting for PSP option `#psp-radio-PPAYITR1XXX` to appear in the UI.

### Category
environment

### Recommended action
Verify UAT backend availability/data for Postepay PSP `PPAYITR1XXX`.

---

# 5. Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1
- **status**: failed
- **fullName**: `features.checkout_npg.Attivazione pagamento Checkout.Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1`
- **message**: Expected modal header to contain 'Non riusciamo a trovare l’avviso', but got: 'L’Ente Creditore sta avendo problemi nella risposta'
- **trace**:
```
Failing step: E L'intestazione della modale di errore contiene "Non riusciamo a trovare l’avviso" ... failed in 0.019s
Location: src/e2e/checkout/features/checkout_npg.feature:57
Assertion Failed: Expected modal header to contain 'Non riusciamo a trovare l’avviso', but got: 'L’Ente Creditore sta avendo problemi nella risposta'
```
### Root cause
Modal header text mismatch due to incorrect error handling logic for invalid notice ranges.

### Category
application bug

### Recommended action
Fix application modal error mapping logic so that `PAA_PAGAMENTO_SCONOSCIUTO` maps to the "Non riusciamo a trovare l’avviso" header message.

---

# 6. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `features.checkout_npg_auth.Attivazione pagamento Checkout autenticato.Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1`
- **message**: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://uat.checkout.pagopa.it/lista-psp)
- **trace**:
```
Failing step: E L'utente seleziona il PSP con id "PPAYITR1XXX" ... failed in 5.066s
Location: src/e2e/checkout/features/checkout_npg_auth.feature:36
Traceback (most recent call last):
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 93, in locate_and_click
    to_click.wait_for(state="visible", timeout=timeout)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/playwright/sync_api/_generated.py", line 17975, in wait_for
    self._sync(self._impl_obj.wait_for(timeout=timeout, state=state))
    ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/playwright/_impl/_sync_base.py", line 115, in _sync
    return task.result()
           ~~~~~~~~~~~^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/playwright/_impl/_locator.py", line 692, in wait_for
    await self._frame.wait_for_selector(
        self._selector, strict=True, timeout=timeout, state=state
    )
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/playwright/_impl/_frame.py", line 369, in wait_for_selector
    await self._channel.send(
        "waitForSelector", self._timeout, locals_to_params(locals())
    )
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/playwright/_impl/_connection.py", line 69
```
### Root cause
Playwright timed out waiting for PSP radio selector `#psp-radio-PPAYITR1XXX` on the PSP list page.

### Category
environment

### Recommended action
Verify whether PSP `PPAYITR1XXX` is currently returned by the backend API in UAT.

---

## Common patterns
- **Missing PSP Option on UAT (`PPAYITR1XXX`)**: 4 test failures were caused by locator timeouts for `#psp-radio-PPAYITR1XXX` on `https://uat.checkout.pagopa.it/lista-psp`, indicating that Postepay PSP configuration is either missing or failing to render in UAT.
- **Incorrect Modal Error Message**: 2 test failures occurred because payment notice activation for invalid ranges (302400000000000000-302409999999999999) returned a generic Creditor Institution error instead of the expected unknown payment notice message.


## Suite: fdr3

No test failures were found in the 'FDR-3' suite execution; please confirm that the execution ran to completion without unintentionally skipping tests.


## Suite: wisp

# 1. L'utente paga un carrello con singola RPT con una marca da bollo gia esistente in GPD
- **status**: broken
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con una marca da bollo gia esistente in GPD`
- **message**: xml.etree.ElementTree.ParseError: not well-formed (invalid token): line 1, column 0
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 169, in user_redirected_to_checkout
    steputils.send_index_activatePaymentNoticeV2_request(context, 5)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 862, in send_index_activatePaymentNoticeV2_request
    send_primitive(context, 'creditor istitution', 'activatePaymentNoticeV2')
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 45, in send_primitive
    status_code, body_response, _ = utils.execute_request(url, 'post', headers, request, content_type,
                                    ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                          description=req_description)
                                                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/run
```
### Root cause
The response from the `activatePaymentNoticeV2` primitive could not be parsed as XML, likely due to an empty body or HTML error response returned by the server.

### Category
environment

### Recommended action
Inspect the endpoint response payload for `activatePaymentNoticeV2` during SOAP execution to check for non-XML error responses or gateway failures.

---

# 2. Utente paga un pagamento singolo con un versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo con marca da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con un versamento semplice e una marca da bollo`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 172, in user_redirected_to_checkout
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 898, in check_wisp_session_timers_del_and_rts_were_sent
    check_event(context, 'receipt-ok', 'status', 'RT_SEND_SUCCESS')
    ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 403, in check_event
    assert_show_message(len(needed_process_events) > 0,
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                        f'There are not events with business process {business_process}.')
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/utility/assertions.p
```
### Root cause
No event with business process `receipt-ok` and status `RT_SEND_SUCCESS` was published or found in event logs after payment completion.

### Category
application bug

### Recommended action
Investigate why receipt generation/sending (`RT_SEND_SUCCESS`) failed or was delayed for payments including stamp duties (`marca da bollo`).

---

# 3. L'utente paga un carrello con singola RPT con una marca da bollo gia esistente in GPD
- **status**: broken
- **fullName**: `features.nodoInviaCarrelloRPT.nodoInviaCarrelloRPT_existingPaymentPosition.L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT.L'utente paga un carrello con singola RPT con una marca da bollo gia esistente in GPD`
- **message**: not well-formed (invalid token): line 1, column 0
- **trace**:
```
Failing step: Allora l'utente viene reindirizzato su Checkout completando il pagamento ... failed in 4.464s
Location: src/integration/wisp/features/nodoInviaCarrelloRPT/nodoInviaCarrelloRPT_existingPaymentPosition.feature:45
Traceback (most recent call last):
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 169, in user_redirected_to_checkout
    steputils.send_index_activatePaymentNoticeV2_request(context, 5)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 862, in send_index_activatePaymentNoticeV2_request
    send_primitive(context, 'creditor istitution', 'activatePaymentNoticeV2')
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 45, in send_primitive
    status_code, body_response, _ = utils.execute_request(url, 'post', headers, request, content_type,
```
### Root cause
`ElementTree.ParseError` raised while attempting to parse malformed or non-XML server response from `activatePaymentNoticeV2`.

### Category
environment

### Recommended action
Verify network traffic and server responses for `activatePaymentNoticeV2` endpoint in the WISP test setup.

---

# 4. Utente paga un pagamento singolo con un versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `features.nodoInviaRPT.nodoInviaRPT_withStamp.Utente paga un pagamento singolo con marca da bollo tramite nodoInviaRPT.Utente paga un pagamento singolo con un versamento semplice e una marca da bollo`
- **message**: There are not events with business process receipt-ok.
- **trace**:
```
Failing step: Allora l'utente viene reindirizzato su Checkout completando il pagamento ... failed in 38.121s
Location: src/integration/wisp/features/nodoInviaRPT/nodoInviaRPT_withStamp.feature:27
Assertion Failed: There are not events with business process receipt-ok.
Captured logging:
INFO:root:Response status code: 200
INFO:root:Response body: <Element 'Envelope' at 0x7fcf071f4130>
INFO:root:Waiting [2] secondto wait for Nodo to write RE events
INFO:root:Wait time ended
INFO:root:Response status code: 200
INFO:root:Response body: {'outcome': 'OK', 'positionslist': [{'fiscalCode': '15376371009', 'noticeNumber': '351179360345820936', 'state': 'OK'}]}
INFO:root:Response status code: 200
INFO:root:Response body: <Element 'Envelope' at 0x7fcf071f68e0>
INFO:root:Waiting [10] secondto wait for Nodo to write RE events
INFO:root:Wait time ended
INFO:root:Response status code: 200
INFO:root:Response body: {'outcome': 'OK'}
INFO:root:Waiting [20] secondto wait for Nodo to write RE events
INFO:root:Wait time ended
ERROR:root:[Assert Error] There are not events with business process receipt-ok.
```
### Root cause
Event tracking assertion failed because `receipt-ok` event was not emitted within the 32-second polling window.

### Category
application bug

### Recommended action
Verify event generation pipeline for single payments involving stamp duties (`nodoInviaRPT_withStamp`).

---

## Common patterns
- **Malformed Response in `activatePaymentNoticeV2`**: 2 failures occurred due to `xml.etree.ElementTree.ParseError`, indicating that the endpoint returned invalid XML or HTTP error status pages instead of a valid SOAP payload.
- **Missing `receipt-ok` Events**: 2 failures were caused by missing receipt confirmation events after completing payment scenarios involving stamp duties (`marca da bollo`).