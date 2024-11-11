Feature: User pays a single payment without stamps via nodoInviaRPT

  Background:
    Given systems up

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @happy_path @happy_path
  Scenario: User pays a single payment with single transfer and no stamp on nodoInviaRPT
    Given a single RPT of type BBT with 1 transfers of which none are stamps
    When the user tries to pay the RPT on EC website
    Then the user is redirected on Checkout completing the payment

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @happy_path
  Scenario: User pays a single payment with two transfers and no stamp on nodoInviaRPT
    Given a single RPT of type BBT with 2 transfers of which none are stamps
    When the user tries to pay the RPT on EC website
    Then the user is redirected on Checkout completing the payment

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @happy_path
  Scenario: User pays a single payment with three transfers and no stamp on nodoInviaRPT
    Given a single RPT of type BBT with 3 transfers of which none are stamps
    When the user tries to pay the RPT on EC website
    Then the user is redirected on Checkout completing the payment

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @happy_path
  Scenario: User pays a single payment with four transfers and no stamp on nodoInviaRPT
    Given a single RPT of type BBT with 4 transfers of which none are stamps
    When the user tries to pay the RPT on EC website
    Then the user is redirected on Checkout completing the payment

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @happy_path
  Scenario: User pays a single payment with five transfers and no stamp on nodoInviaRPT
    Given a single RPT of type BBT with 5 transfers of which none are stamps
    When the user tries to pay the RPT on EC website
    Then the user is redirected on Checkout completing the payment

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @happy_path_refa
  Scenario: User pays a single payment as PO type with one transfer and no stamp on nodoInviaRPT
    Given a single RPT of type PO with 1 transfers of which 0 are stamps
    And the user receives a successful response with the old WISP URL
#    And a valid nodoInviaRPT request
#    When the user sends a nodoInviaRPT action
#    Then the user receives the HTTP status code 200
#    And the response contains the field esito with value OK
#    And the response contains the old WISP URL

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @unhappy_path
  Scenario: User pays a single payment as PO type with two transfer and no stamp on nodoInviaRPT
    Given a single RPT of type PO with 2 transfers of which 0 are stamps
    And a valid nodoInviaRPT request
    When the user sends a nodoInviaRPT action
    Then the user receives the HTTP status code 200
    And the response contains the field esito with value KO
    And the response contains the field faultCode with value PPT_SEMANTICA

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @happy_path @to_fix
  Scenario: User executes a first redirect from nodoInviaRPT, then execute the redirection again and complete the payment flow
    Given a single RPT of type BBT with 1 transfers of which 0 are stamps
    When the user tries to pay the RPT on EC website
#    Then the execution of "Execute NM1-to-NMU conversion in wisp-converter" was successful
    Then the conversion to new model succeeds in wisp-converter
    Then the user is redirected on Checkout completing the payment

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @unhappy_path
  Scenario: User tries two time to pay the same nodoInviaRPT but fails
    Given a single RPT of type BBT with 1 transfers of which 0 are stamps
    When the user tries to pay the RPT on EC website
    Then the user is redirected on Checkout completing the payment
    And conversion to new model fails in wisp-converter

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @unhappy_path_ref
  Scenario: User tries payment with nodoInviaRPT until activatePaymentNoticeV2, then retries again the flow but fails
    Given a single RPT of type BBT with 1 transfers of which 0 are stamps
#    When the execution of "Send a nodoInviaRPT request" was successful
    When the user tries to pay the RPT on EC website
#    Then the execution of "Execute NM1-to-NMU conversion in wisp-converter" was successful
    Then the conversion to new model succeeds in wisp-converter
#    And the execution of "Retrieve all related notice numbers from executed redirect" was successful
    Then the notice numbers are retrieved from redirect
#    And the execution of "Send a checkPosition request" was successful
    Then the checkPosition request was successful
#    cambiare il titolo dello step
#    And the execution of "Send one or more activatePaymentNoticeV2 request" was successful
    Then send activatePaymentNoticeV2 requests
#    And the execution of "Fails on execute NM1-to-NMU conversion in wisp-converter" was successful
    Then conversion to new model fails in wisp-converter