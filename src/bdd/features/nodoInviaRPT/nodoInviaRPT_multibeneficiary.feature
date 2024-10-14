Feature: User pays a multibeneficiary payment carts on nodoInviaCarrelloRPT

  Background:
    Given systems up

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @test
  Scenario: User pays a multibeneficiary cart with two RPTs with a total of two transfers via nodoInviaCarrelloRPT
    Given a cart of RPTs for multibeneficiary
    And a single RPT of type BBT with 1 transfers of which none are stamps
    And a single RPT of type BBT with 1 transfers of which none are stamps
    When the execution of "Send a nodoInviaCarrelloRPT request" was successful
    Then the execution of "Execute redirect and complete payment from multibeneficiary NodoInviaCarrelloRPT" was successful

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a multibeneficiary cart with two RPTs with a total of three transfers via nodoInviaCarrelloRPT
    Given a cart of RPTs for multibeneficiary
    And a single RPT of type BBT with 2 transfers of which none are stamps
    And a single RPT of type BBT with 1 transfers of which none are stamps
    When the execution of "Send a nodoInviaCarrelloRPT request" was successful
    Then the execution of "Execute redirect and complete payment from multibeneficiary NodoInviaCarrelloRPT" was successful

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a multibeneficiary cart with two RPTs with a total of four transfers via nodoInviaCarrelloRPT
    Given a cart of RPTs for multibeneficiary
    And a single RPT of type BBT with 3 transfers of which none are stamps
    And a single RPT of type BBT with 1 transfers of which none are stamps
    When the execution of "Send a nodoInviaCarrelloRPT request" was successful
    Then the execution of "Execute redirect and complete payment from multibeneficiary NodoInviaCarrelloRPT" was successful

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a multibeneficiary cart with two RPTs with a total of five transfers via nodoInviaCarrelloRPT
    Given a cart of RPTs for multibeneficiary
    And a single RPT of type BBT with 4 transfers of which none are stamps
    And a single RPT of type BBT with 1 transfers of which none are stamps
    When the execution of "Send a nodoInviaCarrelloRPT request" was successful
    Then the execution of "Execute redirect and complete payment from multibeneficiary NodoInviaCarrelloRPT" was successful

  # ===============================================================================================
  # ===============================================================================================
