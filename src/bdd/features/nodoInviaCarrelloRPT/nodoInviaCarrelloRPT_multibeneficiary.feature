Feature: User pays a multibeneficiary payment carts on nodoInviaCarrelloRPT

  Background:
    Given systems up
    And a new session

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
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

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  Scenario: User tries to pay a multibeneficiary cart with two RPTs with a total of six transfers via nodoInviaCarrelloRPT
    Given a cart of RPTs for multibeneficiary
    And a single RPT of type BBT with 5 transfers of which none are stamps
    And a single RPT of type BBT with 1 transfers of which none are stamps
    Given a valid nodoInviaCarrelloRPT request for WISP channel
    When the user sends a nodoInviaCarrelloRPT action
    Then the user receives the HTTP status code 200 
    And the response contains the field esitoComplessivoOperazione with value KO
    And the response contains the field faultCode with value PPT_MULTI_BENEFICIARIO
    And the response contains the field description with value 'Il carrello deve avere massimo 5 versamenti totali'
    
  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  Scenario: User tries to pay a multibeneficiary cart with three RPTs with one transfer each one via nodoInviaCarrelloRPT
    Given a cart of RPTs for multibeneficiary
    And a single RPT of type BBT with 1 transfers of which none are stamps
    And a single RPT of type BBT with 1 transfers of which none are stamps
    And a single RPT of type BBT with 1 transfers of which none are stamps
    Given a valid nodoInviaCarrelloRPT request for WISP channel
    When the user sends a nodoInviaCarrelloRPT action
    Then the user receives the HTTP status code 200 
    And the response contains the field esitoComplessivoOperazione with value KO
    And the response contains the field faultCode with value PPT_MULTI_BENEFICIARIO
    And the response contains the field description with value 'Il carrello non contiene solo 2 RPT'

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  Scenario: User tries to pay a multibeneficiary cart with two RPTs, on which the second has two transfers, via nodoInviaCarrelloRPT
    Given a cart of RPTs for multibeneficiary
    And a single RPT of type BBT with 3 transfers of which none are stamps
    And a single RPT of type BBT with 2 transfers of which none are stamps 
    Given a valid nodoInviaCarrelloRPT request for WISP channel
    When the user sends a nodoInviaCarrelloRPT action
    Then the user receives the HTTP status code 200 
    And the response contains the field esitoComplessivoOperazione with value KO
    And the response contains the field faultCode with value PPT_MULTI_BENEFICIARIO
    And the response contains the field description with value 'La seconda RPT non contiene solo 1 versamento'

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  Scenario: User tries to pay a multibeneficiary cart with two RPTs with a stamp via nodoInviaCarrelloRPT
    Given a cart of RPTs for multibeneficiary
    And a single RPT of type BBT with 2 transfers of which 1 are stamps
    And a single RPT of type BBT with 1 transfers of which none are stamps 
    Given a valid nodoInviaCarrelloRPT request for WISP channel
    When the user sends a nodoInviaCarrelloRPT action
    Then the user receives the HTTP status code 200 
    And the response contains the field esitoComplessivoOperazione with value KO
    And the response contains the field faultCode with value PPT_MULTI_BENEFICIARIO
    And the response contains the field description with value 'Nessuna RPT deve contienere marca da bollo'
