Feature: User pays a payment carts from existing payment position via nodoInviaCarrelloRPT

  Background:
    Given systems up

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a cart with single RPT without stamp on nodoInviaCarrelloRPT that exists already in GPD
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 1 transfers of which none are stamps
    And an existing payment position related to first RPT with segregation code equals to 48 and state equals to VALID
    When the user tries to pay the RPT on EC website with cart
    Then the user is redirected on Checkout completing the payment
    And the debt position was closed

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a cart with single RPT with multiple transfers on nodoInviaCarrelloRPT that exists already in GPD
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 3 transfers of which none are stamps
    And an existing payment position related to first RPT with segregation code equals to 48 and state equals to VALID
    When the user tries to pay the RPT on EC website with cart
    Then the user is redirected on Checkout completing the payment
    And the debt position was closed

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: Scenario: User pays a cart with single RPT with one stamp on nodoInviaCarrelloRPT that exists already in GPD
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 2 transfers of which 1 are stamps
    And an existing payment position related to first RPT with segregation code equals to 48 and state equals to VALID
    When the user tries to pay the RPT on EC website with cart
    Then the user is redirected on Checkout completing the payment
    And the debt position was closed

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a cart with two RPTs without stamp on nodoInviaCarrelloRPT of which one already exists in GPD
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 1 transfers of which none are stamps
    And a single RPT of type BBT with 1 transfers of which none are stamps
    And an existing payment position related to first RPT with segregation code equals to 48 and state equals to VALID
    When the user tries to pay the RPT on EC website with cart
    Then the user is redirected on Checkout completing the payment
    And the debt position was closed

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a cart with two RPTs with multiple transfers on nodoInviaCarrelloRPT that exists already in GPD
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 3 transfers of which none are stamps
    And a single RPT of type BBT with 3 transfers of which none are stamps
    And an existing payment position related to first RPT with segregation code equals to 48 and state equals to VALID
    When the user tries to pay the RPT on EC website with cart
    Then the user is redirected on Checkout completing the payment
    And the debt position was closed

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: Scenario: User pays a cart with two RPTs with at least on stamp on nodoInviaCarrelloRPT that exists already in GPD
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 2 transfers of which 1 are stamps
    And a single RPT of type BBT with 3 transfers of which 1 are stamps
    And an existing payment position related to first RPT with segregation code equals to 48 and state equals to VALID
    When the user tries to pay the RPT on EC website with cart
    Then the user is redirected on Checkout completing the payment
    And the debt position was closed

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  Scenario: User tries to pay a cart with single RPT on nodoInviaCarrelloRPT that exists already in GPD in invalid state
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 1 transfers of which none are stamps
    And an existing payment position related to first RPT with segregation code equals to 48 and state equals to DRAFT
    When the user tries to pay the RPT on EC website with cart
    Then conversion to new model fails in wisp-converter
    And the KO receipt was sent

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path_1
  Scenario: User tries to pay a cart with single RPT on nodoInviaCarrelloRPT that was inserted from ACA and is in valid state
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 1 transfers of which none are stamps
    And an existing payment position related to first RPT with segregation code equals to 01 and state equals to VALID
    When the user tries to pay the RPT on EC website with cart
    Then conversion to new model fails in wisp-converter
    And the KO receipt was sent

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  Scenario: User tries to pay a cart with single RPT on nodoInviaCarrelloRPT that was inserted from ACA and is in invalid state
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 1 transfers of which none are stamps
    And an existing payment position related to first RPT with segregation code equals to 01 and state equals to DRAFT
    When the user tries to pay the RPT on EC website with cart
    Then conversion to new model fails in wisp-converter
    And the KO receipt was sent

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  Scenario: User tries to pay a cart with two RPTs on nodoInviaCarrelloRPT that exists already in GPD in invalid state
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 1 transfers of which none are stamps
    And a single RPT of type BBT with 1 transfers of which none are stamps
    And an existing payment position related to first RPT with segregation code equals to 48 and state equals to DRAFT
     When the user tries to pay the RPT on EC website with cart
    Then conversion to new model fails in wisp-converter
    And the KO receipt was sent

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  Scenario: User tries to pay a cart with two RPTs on nodoInviaCarrelloRPT that was inserted from ACA and is in valid state
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 1 transfers of which none are stamps
    And a single RPT of type BBT with 1 transfers of which none are stamps
    And an existing payment position related to first RPT with segregation code equals to 01 and state equals to VALID
     When the user tries to pay the RPT on EC website with cart
    Then conversion to new model fails in wisp-converter
    And the KO receipt was sent

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  Scenario: User tries to pay a cart with two RPTs on nodoInviaCarrelloRPT that was inserted from ACA and is in invalid state
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 1 transfers of which none are stamps
    And a single RPT of type BBT with 1 transfers of which none are stamps
    And an existing payment position related to first RPT with segregation code equals to 01 and state equals to DRAFT
     When the user tries to pay the RPT on EC website with cart
    Then conversion to new model fails in wisp-converter
    And the KO receipt was sent

  # ===============================================================================================
  # ===============================================================================================

  @not_implemented @nodo_invia_carrello_rpt @unhappy_path
  Scenario: User tries to pay a multibeneficiary cart on nodoInviaCarrelloRPT that exists already in GPD in invalid state

#   ===============================================================================================
#   ===============================================================================================

  @not_implemented @nodo_invia_carrello_rpt @unhappy_path
  Scenario: User tries to pay a multibeneficiary cart on nodoInviaCarrelloRPT that was inserted from ACA and is in valid state

#   ===============================================================================================
#   ===============================================================================================

  @not_implemented @nodo_invia_carrello_rpt @unhappy_path
  Scenario: User tries to pay a multibeneficiary cart on nodoInviaCarrelloRPT that was inserted from ACA and is in invalid state


#   ===============================================================================================
#   ===============================================================================================

  @not_implemented @nodo_invia_carrello_rpt @unhappy_path
  Scenario: User pays a multibeneficiary cart on nodoInviaCarrelloRPT that exists already in GPD
