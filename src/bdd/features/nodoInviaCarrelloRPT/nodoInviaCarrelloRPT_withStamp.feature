Feature: User pays a payment carts with stamps on nodoInviaCarrelloRPT

  Background:
    Given systems up


  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a cart with single RPT no simple transfer and one stamp via nodoInviaCarrelloRPT
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 1 transfers of which 1 are stamps
    When the user tries to pay the RPT on EC website
    Then the user is redirected on Checkout completing the payment


  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a cart with single RPT one simple transfer and one stamp via nodoInviaCarrelloRPT
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 2 transfers of which 1 are stamps
    When the user tries to pay the RPT on EC website
    Then the user is redirected on Checkout completing the payment


  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a cart with single RPT two simple transfer and one stamp via nodoInviaCarrelloRPT
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 3 transfers of which 1 are stamps
    When the user tries to pay the RPT on EC website
    Then the user is redirected on Checkout completing the payment


  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a cart with two RPTs, both with no simple transfer and one stamp, via nodoInviaCarrelloRPT
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 1 transfers of which 1 are stamps
    And a single RPT of type BBT with 1 transfers of which 1 are stamps
    When the user tries to pay the RPT on EC website
    Then the user is redirected on Checkout completing the payment


  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a cart with two RPTs, both with one simple transfer and one stamp, via nodoInviaCarrelloRPT
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 2 transfers of which 1 are stamps
    And a single RPT of type BBT with 2 transfers of which 1 are stamps
    When the user tries to pay the RPT on EC website
    Then the user is redirected on Checkout completing the payment


  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a cart with two RPTs, with different quantity of simple transfer and stamps, via nodoInviaCarrelloRPT
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 3 transfers of which 1 are stamps
    And a single RPT of type BBT with 4 transfers of which 2 are stamps
    When the user tries to pay the RPT on EC website
    Then the user is redirected on Checkout completing the payment


  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a cart with three RPTs, with different quantity of simple transfer and stamps, via nodoInviaCarrelloRPT
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 3 transfers of which 1 are stamps
    And a single RPT of type BBT with 4 transfers of which 2 are stamps
    And a single RPT of type BBT with 2 transfers of which 2 are stamps
    When the user tries to pay the RPT on EC website
    Then the user is redirected on Checkout completing the payment


  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path_1
  Scenario: User tries to pay, via nodoInviaCarrelloRPT, a cart with one RPT that has a quantity of transfers and stamps above the limit
    Given a cart of RPTs non-multibeneficiary
    When a single RPT of type BBT with 6 transfers of which 3 are stamps
    Then the user tries to pay a cart of RPTs on EC website but fails having the field value PPT_SINTASSI_XSD

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path_1
  Scenario: User tries to pay, via nodoInviaCarrelloRPT, a cart with two RPTs that has a quantity of transfers and stamps above the limit
    Given a cart of RPTs non-multibeneficiary
    When a single RPT of type BBT with 2 transfers of which 1 are stamps
    And a single RPT of type BBT with 6 transfers of which 2 are stamps
    Then the user tries to pay a cart of RPTs on EC website but fails having the field value PPT_SINTASSI_XSD
