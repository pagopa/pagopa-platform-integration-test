Feature: User pays a payment carts with stamps on nodoInviaCarrelloRPT

  Background:
    Given systems up


  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a cart with single RPT no simple transfer and one stamp via nodoInviaCarrelloRPT
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 1 transfers of which 1 are stamps
    When the execution of "Send a nodoInviaCarrelloRPT request" was successful
    Then the execution of "Execute redirect and complete payment from NodoInviaCarrelloRPT" was successful

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a cart with single RPT one simple transfer and one stamp via nodoInviaCarrelloRPT
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 2 transfers of which 1 are stamps
    When the execution of "Send a nodoInviaCarrelloRPT request" was successful
    Then the execution of "Execute redirect and complete payment from NodoInviaCarrelloRPT" was successful

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a cart with single RPT two simple transfer and one stamp via nodoInviaCarrelloRPT
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 3 transfers of which 1 are stamps
    When the execution of "Send a nodoInviaCarrelloRPT request" was successful
    Then the execution of "Execute redirect and complete payment from NodoInviaCarrelloRPT" was successful

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a cart with two RPTs, both with no simple transfer and one stamp, via nodoInviaCarrelloRPT
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 1 transfers of which 1 are stamps
    And a single RPT of type BBT with 1 transfers of which 1 are stamps
    When the execution of "Send a nodoInviaCarrelloRPT request" was successful
    Then the execution of "Execute redirect and complete payment from NodoInviaCarrelloRPT" was successful

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a cart with two RPTs, both with one simple transfer and one stamp, via nodoInviaCarrelloRPT
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 2 transfers of which 1 are stamps
    And a single RPT of type BBT with 2 transfers of which 1 are stamps
    When the execution of "Send a nodoInviaCarrelloRPT request" was successful
    Then the execution of "Execute redirect and complete payment from NodoInviaCarrelloRPT" was successful

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a cart with two RPTs, with different quantity of simple transfer and stamps, via nodoInviaCarrelloRPT
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 3 transfers of which 1 are stamps
    And a single RPT of type BBT with 4 transfers of which 2 are stamps
    When the execution of "Send a nodoInviaCarrelloRPT request" was successful
    Then the execution of "Execute redirect and complete payment from NodoInviaCarrelloRPT" was successful

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a cart with three RPTs, with different quantity of simple transfer and stamps, via nodoInviaCarrelloRPT
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 3 transfers of which 1 are stamps
    And a single RPT of type BBT with 4 transfers of which 2 are stamps
    And a single RPT of type BBT with 2 transfers of which 2 are stamps
    When the execution of "Send a nodoInviaCarrelloRPT request" was successful
    Then the execution of "Execute redirect and complete payment from NodoInviaCarrelloRPT" was successful

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  Scenario: User tries to pay, via nodoInviaCarrelloRPT, a cart with one RPT that has a quantity of transfers and stamps above the limit
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 6 transfers of which 3 are stamps
    Given a valid nodoInviaCarrelloRPT request for WISP channel
    When the user sends a nodoInviaCarrelloRPT action
    Then the user receives the HTTP status code 200
    And the response contains the field esitoComplessivoOperazione with value KO
    And the response contains the field faultCode with value PPT_SINTASSI_XSD

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  Scenario: User tries to pay, via nodoInviaCarrelloRPT, a cart with two RPTs that has a quantity of transfers and stamps above the limit
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 2 transfers of which 1 are stamps
    And a single RPT of type BBT with 6 transfers of which 2 are stamps
    Given a valid nodoInviaCarrelloRPT request for WISP channel
    When the user sends a nodoInviaCarrelloRPT action
    Then the user receives the HTTP status code 200
    And the response contains the field esitoComplessivoOperazione with value KO
    And the response contains the field faultCode with value PPT_SINTASSI_XSD