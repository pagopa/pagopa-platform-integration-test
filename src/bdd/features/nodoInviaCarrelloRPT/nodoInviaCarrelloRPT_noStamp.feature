Feature: User pays a payment carts without stamps on nodoInviaCarrelloRPT

  Background:
    Given systems up


  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a cart with single RPT with one transfer
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 1 transfers of which none are stamps
    When the user tries to pay a cart of RPTs on EC website
    Then the user is redirected on Checkout completing the payment

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a cart with single RPT with two transfers
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 2 transfers of which none are stamps
    When the user tries to pay a cart of RPTs on EC website
    Then the user is redirected on Checkout completing the payment


  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a cart with single RPT with three transfers
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 3 transfers of which none are stamps
    When the user tries to pay a cart of RPTs on EC website
    Then the user is redirected on Checkout completing the payment


  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a cart with single RPT with four transfers
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 4 transfers of which none are stamps
    When the user tries to pay a cart of RPTs on EC website
    Then the user is redirected on Checkout completing the payment


  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a cart with single RPT with five transfers
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 5 transfers of which none are stamps
    When the user tries to pay a cart of RPTs on EC website
    Then the user is redirected on Checkout completing the payment


  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a cart with three RPTs with one transfer each one
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 1 transfers of which none are stamps
    And a single RPT of type BBT with 1 transfers of which none are stamps
    And a single RPT of type BBT with 1 transfers of which none are stamps
    When the user tries to pay a cart of RPTs on EC website
    Then the user is redirected on Checkout completing the payment


  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a cart with four RPTs with one transfer each one
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 1 transfers of which none are stamps
    And a single RPT of type BBT with 1 transfers of which none are stamps
    And a single RPT of type BBT with 1 transfers of which none are stamps
    And a single RPT of type BBT with 1 transfers of which none are stamps
    When the user tries to pay a cart of RPTs on EC website
    Then the user is redirected on Checkout completing the payment


  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a cart with five RPTs with one transfer each one
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 1 transfers of which none are stamps
    And a single RPT of type BBT with 1 transfers of which none are stamps
    And a single RPT of type BBT with 1 transfers of which none are stamps
    And a single RPT of type BBT with 1 transfers of which none are stamps
    And a single RPT of type BBT with 1 transfers of which none are stamps
    When the user tries to pay a cart of RPTs on EC website
    Then the user is redirected on Checkout completing the payment


  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a cart with two RPTs with a total of five transfers
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 2 transfers of which none are stamps
    And a single RPT of type BBT with 3 transfers of which none are stamps
    When the user tries to pay a cart of RPTs on EC website
    Then the user is redirected on Checkout completing the payment


  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a cart with three RPTs with a total of five transfers
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 1 transfers of which none are stamps
    And a single RPT of type BBT with 2 transfers of which none are stamps
    And a single RPT of type BBT with 2 transfers of which none are stamps
    When the user tries to pay a cart of RPTs on EC website
    Then the user is redirected on Checkout completing the payment


  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a cart with three RPTs with a total of ten transfers
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 3 transfers of which none are stamps
    And a single RPT of type BBT with 3 transfers of which none are stamps
    And a single RPT of type BBT with 4 transfers of which none are stamps
    When the user tries to pay a cart of RPTs on EC website
    Then the user is redirected on Checkout completing the payment


  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a cart with two RPTs on WFESP flow
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type CP with 1 transfers of which none are stamps
    And a single RPT of type CP with 1 transfers of which none are stamps
    When the user tries to pay a cart of RPTs on EC website with no redirect URL check
    Then the response contains the fake WFESP URL

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User tries to pay a cart with two RPTs but the payment closure fails, then tries again successfully
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 1 transfers of which none are stamps
    And a single RPT of type BBT with 1 transfers of which none are stamps
    And the user tries to pay a cart of RPTs on EC website
    And the user is redirected on Checkout not completing the multibeneficiary payment
    Then the user tries to pay a cart of RPTs on EC website
    And the user is redirected on Checkout completing the multibeneficiary payment

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  Scenario: User tries to pay a cart with one RPT that has a quantity of transfers above the limit
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 6 transfers of which none are stamps
    When the user tries to pay a cart of RPTs on EC website with no redirect URL check
    Then fails having a quantity of transfers above the limit and getting the error PPT_SINTASSI_XSD
  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  Scenario: User tries to pay a cart with two RPT that has a quantity of transfers above the limit
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 2 transfers of which none are stamps
    And a single RPT of type BBT with 6 transfers of which none are stamps
    And a single RPT of type BBT with 6 transfers of which none are stamps
    When the user tries to pay a cart of RPTs on EC website with no redirect URL check
    Then fails having a quantity of transfers above the limit and getting the error PPT_SINTASSI_XSD
  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  Scenario: User tries to pay a cart with two RPTs but the payment closure fails
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 1 transfers of which none are stamps
    And a single RPT of type BBT with 1 transfers of which none are stamps
    When the user tries to pay a cart of RPTs on EC website
    Then the user is redirected on Checkout not completing the multibeneficiary payment
