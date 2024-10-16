Feature: Common scenarios for nodoInviaCarrelloRPT

  Scenario: Send a nodoInviaCarrelloRPT request
    Given a valid nodoInviaCarrelloRPT request for WISP channel
    When the user sends a nodoInviaCarrelloRPT action
    Then the user receives the HTTP status code 200 
    And the response contains the field esitoComplessivoOperazione with value OK
    And the response contains the redirect URL
  
  # ===============================================================================================
  # ===============================================================================================

  Scenario: Check if WISP session timers were deleted and all RTs were sent
    Given a waiting time of 10 seconds to wait for Nodo to write RE events
    And all the IUV codes of the sent RPTs
    When the user searches for flow steps by IUVs
    Then the user receives the HTTP status code 200
    Then there is a timer-delete event with field status with value RECEIPT_TIMER_GENERATION_DELETED_SCHEDULED_SEND
    And these events are related to each payment token
    Then there is a receipt-ok event with field status with value RT_SEND_SUCCESS
    And these events are related to each notice number

  # ===============================================================================================
  # ===============================================================================================
  
  Scenario: Check the paid payment position, generated from multibeneficiary cart
    When the user searches for payment position in GPD by first IUV
    Then the user receives the HTTP status code 200
    And the response contains the field status with value PAID
    And the response contains a single payment option
    And the response contains the payment option correctly generated from all RPTs 
    And the response contains the status in PO_PAID for the payment option
    And the response contains the transfers correctly generated from all RPTs

  # ===============================================================================================
  # ===============================================================================================

  Scenario: Check if WISP session timers were deleted and all RTs were sent in KO
    Given a waiting time of 10 seconds to wait for Nodo to write RE events
    And all the IUV codes of the sent RPTs
    When the user searches for flow steps by IUVs
    Then the user receives the HTTP status code 200
    Then there is a timer-delete event with field status with value RECEIPT_TIMER_GENERATION_DELETED_SCHEDULED_SEND
    And these events are related to each payment token
    Then there is a receipt-ko event with field status with value RT_SEND_SUCCESS
    And these events are related to each notice number

  # ===============================================================================================
  # ===============================================================================================

  Scenario: Execute redirect and complete payment from NodoInviaCarrelloRPT
    When the execution of "Execute NM1-to-NMU conversion in wisp-converter" was successful
    Then the execution of "Retrieve all related notice numbers from executed redirect" was successful
    And the execution of "Send a checkPosition request" was successful
    And the execution of "Send one or more activatePaymentNoticeV2 requests" was successful
    And the execution of "Check if WISP session timers were created" was successful
    And the execution of "Send a closePaymentV2 request" was successful
    And the execution of "Check if WISP session timers were deleted and all RTs were sent" was successful
    And the execution of "Check the paid payment positions" was successful

  # ===============================================================================================
  # ===============================================================================================

  Scenario: Execute redirect and complete payment from multibeneficiary NodoInviaCarrelloRPT
    When the execution of "Execute NM1-to-NMU conversion in wisp-converter" was successful
    Then the execution of "Retrieve all related notice numbers from executed redirect" was successful
    And the execution of "Send a checkPosition request" was successful
    And the execution of "Send one or more activatePaymentNoticeV2 requests" was successful
    And the execution of "Check if WISP session timers were created" was successful
    And the execution of "Send a closePaymentV2 request" was successful
    And the execution of "Check if WISP session timers were deleted and all RTs were sent" was successful
    And the execution of "Check the paid payment position, generated from multibeneficiary cart" was successful

  # ===============================================================================================
  # ===============================================================================================

  Scenario: Execute redirect but not closing payment from multibeneficiary NodoInviaCarrelloRPT
    When the execution of "Execute NM1-to-NMU conversion in wisp-converter" was successful
    Then the execution of "Retrieve all related notice numbers from executed redirect" was successful
    And the execution of "Send a checkPosition request" was successful
    And the execution of "Send one or more activatePaymentNoticeV2 requests" was successful
    And the execution of "Check if WISP session timers were created" was successful
    And the execution of "Send a KO closePaymentV2 request" was successful
    And the execution of "Check if WISP session timers were deleted and all RTs were sent in KO" was successful


