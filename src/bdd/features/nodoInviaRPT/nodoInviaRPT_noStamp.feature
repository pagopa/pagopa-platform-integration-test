Feature: User pays a single payment without stamps via nodoInviaRPT

  Background:
    Given systems up

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @happy_path @happy_path
  Scenario: User pays a single payment with single transfer and no stamp
    Given a single RPT of type BBT with 1 transfers of which none are stamps
    When the user tries to pay the RPT on EC website
    Then the user is redirected on Checkout completing the payment

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @happy_path
  Scenario: User pays a single payment with two transfers and no stamp
    Given a single RPT of type BBT with 2 transfers of which none are stamps
    When the user tries to pay the RPT on EC website
    Then the user is redirected on Checkout completing the payment

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @happy_path
  Scenario: User pays a single payment with three transfers and no stamp
    Given a single RPT of type BBT with 3 transfers of which none are stamps
    When the user tries to pay the RPT on EC website
    Then the user is redirected on Checkout completing the payment

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @happy_path
  Scenario: User pays a single payment with four transfers and no stamp
    Given a single RPT of type BBT with 4 transfers of which none are stamps
    When the user tries to pay the RPT on EC website
    Then the user is redirected on Checkout completing the payment

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @happy_path
  Scenario: User pays a single payment with five transfers and no stamp
    Given a single RPT of type BBT with 5 transfers of which none are stamps
    When the user tries to pay the RPT on EC website
    Then the user is redirected on Checkout completing the payment

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @happy_path
  Scenario: User pays a single payment as PO type with one transfer and no stamp
    Given a single RPT of type PO with 1 transfers of which 0 are stamps
    When the user sends a nodoInviaRPT request
    Then the user receives a successful response
    And the response contains the old WISP URL

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @unhappy_path
  Scenario: User pays a single payment as PO type with two transfer and no stamp
    Given a single RPT of type PO with 2 transfers of which 0 are stamps
    When the user tries to pay the RPT on EC website but fails
    And the response contains the field faultCode with value PPT_SEMANTICA

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @happy_path @to_fix
  Scenario: User executes a first redirect, then execute the redirection again and complete the payment flow
    Given a single RPT of type BBT with 1 transfers of which 0 are stamps
    When the user tries to pay the RPT on EC website
    Then the conversion to new model succeeds in wisp-converter
    Then the user is redirected on Checkout completing the payment

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @unhappy_path
  Scenario: User tries two time to pay the same RPT but fails
    Given a single RPT of type BBT with 1 transfers of which 0 are stamps
    When the user tries to pay the RPT on EC website
    Then the user is redirected on Checkout completing the payment
    And conversion to new model fails in wisp-converter

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @unhappy_path
  Scenario: User tries payment with nodoInviaRPT until activatePaymentNoticeV2, then retries again the flow but fails
    Given a single RPT of type BBT with 1 transfers of which 0 are stamps
    When the user tried to pay the RPT on EC website
    And send activatePaymentNoticeV2 requests
    Then conversion to new model fails in wisp-converter