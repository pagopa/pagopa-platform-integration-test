Feature: User pays a single payment with stamp via nodoInviaRPT

  Background:
    Given systems up

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @happy_path
  Scenario: User pays a single payment with no simple transfer and one stamp on nodoInviaRPT
    Given a single RPT of type BBT with 1 transfers of which 1 are stamps
    When the user tries to pay the RPT on EC website
    Then the user is redirected on Checkout completing the payment

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @happy_path
  Scenario: User pays a single payment with one simple transfer and one stamp on nodoInviaRPT
    Given a single RPT of type BBT with 2 transfers of which 1 are stamps
    When the user tries to pay the RPT on EC website
    Then the user is redirected on Checkout completing the payment
  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @happy_path
  Scenario: User pays a single payment with two simple transfer and one stamp on nodoInviaRPT
    Given a single RPT of type BBT with 3 transfers of which 1 are stamps
    When the user tries to pay the RPT on EC website
    Then the user is redirected on Checkout completing the payment

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @happy_path
  Scenario: User pays a single payment with two simple transfer and two stamp on nodoInviaRPT
    Given a single RPT of type BBT with 4 transfers of which 2 are stamps
    When the user tries to pay the RPT on EC website
    Then the user is redirected on Checkout completing the payment

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @happy_path
  Scenario: User pays a single payment as PO type with no simple transfer and one stamp on nodoInviaRPT
    Given a single RPT of type PO with 1 transfers of which 1 are stamps
    And the user tries to pay the RPT on EC website
    And the response contains the old WISP URL

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @unhappy_path
  Scenario: User pays a single payment as PO type with one simple transfer and one stamp on nodoInviaRPT
    Given a single RPT of type PO with 2 transfers of which 1 are stamps
    And the user tries to pay the RPT on EC website but fails
    And the response contains the field faultCode with value PPT_SEMANTICA
