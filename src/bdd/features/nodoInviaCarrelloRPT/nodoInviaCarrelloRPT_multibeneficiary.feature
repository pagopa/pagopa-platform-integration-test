Feature: User pays a multibeneficiary payment carts on nodoInviaCarrelloRPT

  Background:
    Given systems up

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a multibeneficiary cart with two RPTs with a total of two transfers
    Given a cart of RPTs for multibeneficiary
    And a single RPT of type BBT with 1 transfers of which none are stamps
    And a single RPT of type BBT with 1 transfers of which none are stamps
    When the user tries to pay a cart of RPTs on EC website
    Then the user is redirected on Checkout completing the multibeneficiary payment

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a multibeneficiary cart with two RPTs with a total of three transfers
    Given a cart of RPTs for multibeneficiary
    And a single RPT of type BBT with 2 transfers of which none are stamps
    And a single RPT of type BBT with 1 transfers of which none are stamps
    When the user tries to pay a cart of RPTs on EC website
    Then the user is redirected on Checkout completing the multibeneficiary payment

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a multibeneficiary cart with two RPTs with a total of four transfers
    Given a cart of RPTs for multibeneficiary
    And a single RPT of type BBT with 3 transfers of which none are stamps
    And a single RPT of type BBT with 1 transfers of which none are stamps
    When the user tries to pay a cart of RPTs on EC website
    Then the user is redirected on Checkout completing the multibeneficiary payment

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a multibeneficiary cart with two RPTs with a total of five transfers
    Given a cart of RPTs for multibeneficiary
    And a single RPT of type BBT with 4 transfers of which none are stamps
    And a single RPT of type BBT with 1 transfers of which none are stamps
    When the user tries to pay a cart of RPTs on EC website
    Then the user is redirected on Checkout completing the multibeneficiary payment

  # ===============================================================================================
  # ===============================================================================================

    @runnable @nodo_invia_carrello_rpt @unhappy_path
    Scenario: User tries to pay a multibeneficiary cart with two RPTs with a total of six transfers
    Given a cart of RPTs for multibeneficiary
    And a single RPT of type BBT with 5 transfers of which none are stamps
    And a single RPT of type BBT with 1 transfers of which none are stamps
    When the user tries to pay a cart of RPTs on EC website but fails
    Then the response contains the field description with value 'Il carrello deve avere massimo 5 versamenti totali'
  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  Scenario: User tries to pay a multibeneficiary cart with three RPTs with one transfer each one
    Given a cart of RPTs for multibeneficiary
    And a single RPT of type BBT with 1 transfers of which none are stamps
    And a single RPT of type BBT with 1 transfers of which none are stamps
    And a single RPT of type BBT with 1 transfers of which none are stamps
    When the user tries to pay a cart of RPTs on EC website but fails
    And the response contains the field description with value 'Il carrello non contiene solo 2 RPT'

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  Scenario: User tries to pay a multibeneficiary cart with two RPTs, on which the second has two transfers
    Given a cart of RPTs for multibeneficiary
    And a single RPT of type BBT with 3 transfers of which none are stamps
    And a single RPT of type BBT with 2 transfers of which none are stamps
    Given a valid nodoInviaCarrelloRPT request for WISP channel
    When the user tries to pay a cart of RPTs on EC website but fails
    And the response contains the field description with value 'La seconda RPT non contiene solo 1 versamento'

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  Scenario: User tries to pay a multibeneficiary cart with two RPTs with a stamp
    Given a cart of RPTs for multibeneficiary
    And a single RPT of type BBT with 2 transfers of which 1 are stamps
    And a single RPT of type BBT with 1 transfers of which none are stamps
    When the user tries to pay a cart of RPTs on EC website but fails
    And the response contains the field description with value 'Nessuna RPT deve contienere marca da bollo'
