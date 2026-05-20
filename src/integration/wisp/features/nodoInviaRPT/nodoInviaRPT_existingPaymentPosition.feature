Feature: User pays a single payment from existing payment position via nodoInviaRPT

  Background:
    Given systems up

    @runnable @nodo_invia_rpt @happy_path
    Scenario: User pays a single payment with single transfer and no stamp that exists already in GPD
    Given a single RPT of type BBT with 1 transfers of which 0 are stamps
    And an existing payment position related to first RPT with segregation code equals to 48 and state equals to VALID
    When the user tries to pay the RPT on EC website
    Then the user is redirected on Checkout completing the payment
    And the debt position is closed

  @runnable @nodo_invia_rpt @happy_path
  Scenario: User pays a single payment with no transfer and one stamp that exists already in GPD
    Given a single RPT of type BBT with 1 transfers of which 1 are stamps
    And an existing payment position related to first RPT with segregation code equals to 48 and state equals to VALID
    When the user tries to pay the RPT on EC website
    Then the user is redirected on Checkout completing the payment
    And the debt position is closed

  # ===============================================================================================
  # ===============================================================================================

    @runnable @nodo_invia_rpt @happy_path
    Scenario: User pays a single payment with single transfer and one stamp that exists already in GPD
    Given a single RPT of type BBT with 2 transfers of which 1 are stamps
    And an existing payment position related to first RPT with segregation code equals to 48 and state equals to VALID
    When the user tries to pay the RPT on EC website
    Then the user is redirected on Checkout completing the payment
    And the debt position is closed

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @unhappy_path
  Scenario: User tries to pay a single payment with single transfer and no stamp that exists already in GPD in invalid state
    Given a single RPT of type BBT with 1 transfers of which 0 are stamps
    And an existing payment position related to first RPT with segregation code equals to 48 and state equals to DRAFT
    When the user tries to pay the RPT on EC website
    Then conversion to new model fails in wisp-converter
    And the KO receipt is sent

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @unhappy_path
  Scenario: User tries to pay a single payment that was inserted from ACA and is in valid state
    Given a single RPT of type BBT with 1 transfers of which 0 are stamps
    And an existing payment position related to first RPT with segregation code equals to 01 and state equals to VALID
    When the user tries to pay the RPT on EC website
    Then conversion to new model fails in wisp-converter
    And the KO receipt is sent

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @unhappy_path
  Scenario: User tries to pay a single payment that was inserted from ACA and is in invalid state
    Given a single RPT of type BBT with 1 transfers of which 0 are stamps
    And an existing payment position related to first RPT with segregation code equals to 01 and state equals to DRAFT
    When the user tries to pay the RPT on EC website
    Then conversion to new model fails in wisp-converter
    And the KO receipt is sent
