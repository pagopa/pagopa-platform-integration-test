Feature: User pays a payment carts without stamps on nodoInviaCarrelloRPT

  Background:
    Given systems up
    And a new session

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a cart with single RPT with one transfer via nodoInviaCarrelloRPT
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 1 transfers of which none are stamps
    When the execution of "Send a nodoInviaCarrelloRPT request" was successful
    Then the execution of "Execute redirect and complete payment from NodoInviaCarrelloRPT" was successful

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a cart with single RPT with two transfers via nodoInviaCarrelloRPT
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 2 transfers of which none are stamps
    When the execution of "Send a nodoInviaCarrelloRPT request" was successful
    Then the execution of "Execute redirect and complete payment from NodoInviaCarrelloRPT" was successful

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a cart with single RPT with three transfers via nodoInviaCarrelloRPT
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 3 transfers of which none are stamps
    When the execution of "Send a nodoInviaCarrelloRPT request" was successful
    Then the execution of "Execute redirect and complete payment from NodoInviaCarrelloRPT" was successful

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a cart with single RPT with four transfers via nodoInviaCarrelloRPT
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 4 transfers of which none are stamps
    When the execution of "Send a nodoInviaCarrelloRPT request" was successful
    Then the execution of "Execute redirect and complete payment from NodoInviaCarrelloRPT" was successful

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a cart with single RPT with five transfers via nodoInviaCarrelloRPT
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 5 transfers of which none are stamps
    When the execution of "Send a nodoInviaCarrelloRPT request" was successful
    Then the execution of "Execute redirect and complete payment from NodoInviaCarrelloRPT" was successful

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a cart with three RPTs with one transfer each one via nodoInviaCarrelloRPT
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 1 transfers of which none are stamps
    And a single RPT of type BBT with 1 transfers of which none are stamps
    And a single RPT of type BBT with 1 transfers of which none are stamps
    When the execution of "Send a nodoInviaCarrelloRPT request" was successful
    Then the execution of "Execute redirect and complete payment from NodoInviaCarrelloRPT" was successful

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a cart with four RPTs with one transfer each one via nodoInviaCarrelloRPT
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 1 transfers of which none are stamps
    And a single RPT of type BBT with 1 transfers of which none are stamps
    And a single RPT of type BBT with 1 transfers of which none are stamps
    And a single RPT of type BBT with 1 transfers of which none are stamps
    When the execution of "Send a nodoInviaCarrelloRPT request" was successful
    Then the execution of "Execute redirect and complete payment from NodoInviaCarrelloRPT" was successful
    
  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path 
  Scenario: User pays a cart with five RPTs with one transfer each one via nodoInviaCarrelloRPT
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 1 transfers of which none are stamps
    And a single RPT of type BBT with 1 transfers of which none are stamps
    And a single RPT of type BBT with 1 transfers of which none are stamps
    And a single RPT of type BBT with 1 transfers of which none are stamps
    And a single RPT of type BBT with 1 transfers of which none are stamps
    When the execution of "Send a nodoInviaCarrelloRPT request" was successful
    Then the execution of "Execute redirect and complete payment from NodoInviaCarrelloRPT" was successful
    
  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a cart with two RPTs with a total of five transfers via nodoInviaCarrelloRPT
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 2 transfers of which none are stamps
    And a single RPT of type BBT with 3 transfers of which none are stamps
    When the execution of "Send a nodoInviaCarrelloRPT request" was successful
    Then the execution of "Execute redirect and complete payment from NodoInviaCarrelloRPT" was successful
    
  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a cart with three RPTs with a total of five transfers via nodoInviaCarrelloRPT
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 1 transfers of which none are stamps
    And a single RPT of type BBT with 2 transfers of which none are stamps
    And a single RPT of type BBT with 2 transfers of which none are stamps
    When the execution of "Send a nodoInviaCarrelloRPT request" was successful
    Then the execution of "Execute redirect and complete payment from NodoInviaCarrelloRPT" was successful

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a cart with three RPTs with a total of ten transfers via nodoInviaCarrelloRPT
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 3 transfers of which none are stamps
    And a single RPT of type BBT with 3 transfers of which none are stamps
    And a single RPT of type BBT with 4 transfers of which none are stamps
    When the execution of "Send a nodoInviaCarrelloRPT request" was successful
    Then the execution of "Execute redirect and complete payment from NodoInviaCarrelloRPT" was successful
    
  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User pays a cart with two RPTs on WFESP flow via nodoInviaCarrelloRPT
    Given a cart of RPTs non-multibeneficiary 
    And a single RPT of type CP with 1 transfers of which none are stamps
    And a single RPT of type CP with 1 transfers of which none are stamps
    And a valid nodoInviaCarrelloRPT request for WFESP channel
    When the user sends a nodoInviaCarrelloRPT action
    Then the user receives the HTTP status code 200 
    And the response contains the field esitoComplessivoOperazione with value OK
    And the response contains the fake WFESP URL
    
  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: User tries to pay, via nodoInviaCarrelloRPT, a cart with two RPTs but the payment closure fails, then 
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 1 transfers of which none are stamps
    And a single RPT of type BBT with 1 transfers of which none are stamps
    When the execution of "Send a nodoInviaCarrelloRPT request" was successful
    When the execution of "Execute redirect but not closing payment from multibeneficiary NodoInviaCarrelloRPT" was successful
    Given the same nodoInviaCarrelloRPT for another try 
    When the execution of "Send a nodoInviaCarrelloRPT request" was successful
    Then the execution of "Execute redirect and complete payment from NodoInviaCarrelloRPT" was successful

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  Scenario: User tries to pay, via nodoInviaCarrelloRPT, a cart with one RPT that has a quantity of transfers above the limit
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 6 transfers of which none are stamps
    And a valid nodoInviaCarrelloRPT request for WISP channel
    When the user sends a nodoInviaCarrelloRPT action
    Then the user receives the HTTP status code 200 
    And the response contains the field esitoComplessivoOperazione with value KO
    And the response contains the field faultCode with value PPT_SINTASSI_XSD
    
  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  Scenario: User tries to pay, via nodoInviaCarrelloRPT, a cart with two RPT that has a quantity of transfers above the limit
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 2 transfers of which none are stamps
    And a single RPT of type BBT with 6 transfers of which none are stamps
    Given a valid nodoInviaCarrelloRPT request for WISP channel
    When the user sends a nodoInviaCarrelloRPT action
    Then the user receives the HTTP status code 200 
    And the response contains the field esitoComplessivoOperazione with value KO
    And the response contains the field faultCode with value PPT_SINTASSI_XSD
    
  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  Scenario: User tries to pay, via nodoInviaCarrelloRPT, a cart with two RPTs but the payment closure fails
    Given a cart of RPTs non-multibeneficiary
    And a single RPT of type BBT with 1 transfers of which none are stamps
    And a single RPT of type BBT with 1 transfers of which none are stamps
    When the execution of "Send a nodoInviaCarrelloRPT request" was successful
    When the execution of "Execute redirect but not closing payment from multibeneficiary NodoInviaCarrelloRPT" was successful
