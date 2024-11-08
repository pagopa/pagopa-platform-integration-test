Feature: User pays a single payment from existing payment position via nodoInviaRPT

  Background:
    Given systems up

    @runnable @nodo_invia_rpt @refactor_test
#  Scenario: User pays a single payment with single transfer and no stamp on nodoInviaRPT that exists already in GPD
    Scenario: User pays a single payment with single transfer and no stamp that exists already in GPD
    Given a single RPT of type BBT with 1 transfers of which 0 are stamps
    And an existing payment position related to first RPT with segregation code equals to 48 and state equals to VALID
    When the user tries to pay the RPT on EC website
    Then the user is redirected on Checkout completing the payment
    And the debt position was closed

  @runnable @nodo_invia_rpt @refactor_test
  Scenario: User pays a single payment with no transfer and one stamp on nodoInviaRPT that exists already in GPD
    Given a single RPT of type BBT with 1 transfers of which 1 are stamps
    And an existing payment position related to first RPT with segregation code equals to 48 and state equals to VALID
    When the user tries to pay the RPT on EC website
    Then the user is redirected on Checkout
    And the payment is done

  # ===============================================================================================
  # ===============================================================================================

    @runnable @nodo_invia_rpt @refactor_test
    Scenario: User pays a single payment with single transfer and one stamp on nodoInviaRPT that exists already in GPD
    Given a single RPT of type BBT with 2 transfers of which 1 are stamps
    And an existing payment position related to first RPT with segregation code equals to 48 and state equals to VALID
    When the user tries to pay the RPT on EC website
    Then the user is redirected on Checkout
    And the payment is done

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @refactor_test_unhappy
  Scenario: User tries to pay a single payment with single transfer and no stamp on nodoInviaRPT that exists already in GPD in invalid state
    Given a single RPT of type BBT with 1 transfers of which 0 are stamps
    And an existing payment position related to first RPT with segregation code equals to 48 and state equals to DRAFT
    When the user tries to pay the RPT on EC website
    Then conversion to new model fails in wisp-converter
    And the KO receipt was sent

#    Then the execution of "Fails on execute NM1-to-NMU conversion in wisp-converter" was successful
#    And the execution of "Check if existing debt position was invalid but has sent a KO receipt" was successful

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @refactor_test_unhappy
  Scenario: User tries to pay a single payment on nodoInviaRPT that was inserted from ACA and is in valid state
    Given a single RPT of type BBT with 1 transfers of which 0 are stamps
    And an existing payment position related to first RPT with segregation code equals to 01 and state equals to VALID
    When the user tries to pay the RPT on EC website
    Then conversion to new model fails in wisp-converter
    And the KO receipt was sent

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @refactor_test_unhappy
  Scenario: User tries to pay a single payment on nodoInviaRPT that was inserted from ACA and is in invalid state
    Given a single RPT of type BBT with 1 transfers of which 0 are stamps
    And an existing payment position related to first RPT with segregation code equals to 01 and state equals to DRAFT
    When the user tries to pay the RPT on EC website
    Then conversion to new model fails in wisp-converter
    And the KO receipt was sent
