Feature: Common scenarios for nodoInviaRPT

  Scenario: Send a nodoInviaRPT request
    Given a valid nodoInviaRPT request
    When the user sends a nodoInviaRPT action
    Then the user receives the HTTP status code 200
    And the response contains the field esito with value OK
    And the response contains the redirect URL

  # ===============================================================================================
  # ===============================================================================================

  Scenario: Retrieve all related notice numbers from executed redirect
    Given a waiting time of 2 seconds to wait for Nodo to write RE events
    Given the first IUV code of the sent RPTs
    When the user searches for flow steps by IUVs
    Then the user receives the HTTP status code 200
    And all the related notice numbers can be retrieved

  # ===============================================================================================
  # ===============================================================================================

    Scenario: Check if WISP session timers were created
    Given a waiting time of 5 seconds to wait for Nodo to write RE events
    And all the IUV codes of the sent RPTs
    When the user searches for flow steps by IUVs
    Then the user receives the HTTP status code 200
    And there is a timer-set event with field operationStatus with value Success
    And these events are related to each payment token

  # ===============================================================================================
  # ===============================================================================================

  Scenario: Check the paid payment positions
    # executing the check on payment position for first IUV
    When the user searches for payment position in GPD by first IUV
    Then the user receives the HTTP status code 200
    And the response contains the field status with value PAID
    And the response contains a single payment option
    And the response contains the payment option correctly generated from first RPT
    And the response contains the status in PO_PAID for the payment option
    And the response contains the transfers correctly generated from RPT
    # executing the check on payment position for second IUV
    When the user searches for payment position in GPD by second IUV
    Then the user receives the HTTP status code 200
    And the response contains the field status with value PAID
    And the response contains a single payment option
    And the response contains the payment option correctly generated from second RPT
    And the response contains the status in PO_PAID for the payment option
    And the response contains the transfers correctly generated from RPT
    # executing the check on payment position for third IUV
    When the user searches for payment position in GPD by third IUV
    Then the user receives the HTTP status code 200
    And the response contains the field status with value PAID
    And the response contains a single payment option
    And the response contains the payment option correctly generated from third RPT
    And the response contains the status in PO_PAID for the payment option
    And the response contains the transfers correctly generated from RPT
    # executing the check on payment position for fourth IUV
    When the user searches for payment position in GPD by fourth IUV
    Then the user receives the HTTP status code 200
    And the response contains the field status with value PAID
    And the response contains a single payment option
    And the response contains the payment option correctly generated from fourth RPT
    And the response contains the status in PO_PAID for the payment option
    And the response contains the transfers correctly generated from RPT
    # executing the check on payment position for fifth IUV
    When the user searches for payment position in GPD by fifth IUV
    Then the user receives the HTTP status code 200
    And the response contains the field status with value PAID
    And the response contains a single payment option
    And the response contains the payment option correctly generated from fifth RPT
    And the response contains the status in PO_PAID for the payment option
    And the response contains the transfers correctly generated from RPT

  # ===============================================================================================
  # ===============================================================================================

  Scenario: Check if existing debt position was used
    Given a waiting time of 2 seconds to wait for Nodo to write RE events
    And the first IUV code of the sent RPTs
    When the user searches for flow steps by IUVs
    Then the user receives the HTTP status code 200
    And there is a redirect event with field status with value UPDATED_EXISTING_PAYMENT_POSITION_IN_GPD

  # ===============================================================================================
  # ===============================================================================================

  Scenario: Check if existing debt position was invalid but has sent a KO receipt
    Given a waiting time of 2 seconds to wait for Nodo to write RE events
    And the first IUV code of the sent RPTs
    When the user searches for flow steps by IUVs
    Then the user receives the HTTP status code 200
    And there is a redirect event with field operationErrorCode with value WIC-1300
    And there is a redirect event with field status with value RT_SEND_SUCCESS

  # ===============================================================================================
  # ===============================================================================================

  Scenario: Check if existing debt position was invalid from ACA but has sent a KO receipt
    Given a waiting time of 2 seconds to wait for Nodo to write RE events
    And the first IUV code of the sent RPTs
    When the user searches for flow steps by IUVs
    Then the user receives the HTTP status code 200
    And there is a redirect event with field operationErrorCode with value WIC-1205
    And there is a redirect event with field status with value RT_SEND_SUCCESS

  # ===============================================================================================
  # ===============================================================================================

  Scenario: Execute redirect and complete payment from NodoInviaRPT
    When the execution of "Execute NM1-to-NMU conversion in wisp-converter" was successful
    Then the execution of "Retrieve all related notice numbers from executed redirect" was successful
    And the execution of "Send a checkPosition request" was successful
    And the execution of "Send one or more activatePaymentNoticeV2 requests" was successful
#    And the execution of "Check if WISP session timers were created" was successful
#    And the execution of "Send a closePaymentV2 request" was successful
#    And the execution of "Check if WISP session timers were deleted and all RTs were sent" was successful
#    And the execution of "Check the paid payment positions" was successful


    Scenario: Send a closePaymentV2 request
    Given a valid closePaymentV2 request with outcome OK
    When the creditor institution sends a closePaymentV2 action
    Then the creditor institution receives the HTTP status code 200
    And the response contains the field outcome with value OK


    Scenario: Send a checkPosition request
    Given a valid checkPosition request
    When the creditor institution sends a checkPosition action
    Then the creditor institution receives the HTTP status code 200
    And the response contains the field outcome with value OK
    And the response contains the field positionslist as not empty list

    Scenario: Check if WISP session timers were deleted and all RTs were sent
    Given a waiting time of 10 seconds to wait for Nodo to write RE events
    And all the IUV codes of the sent RPTs
    When the user searches for flow steps by IUVs
    Then the user receives the HTTP status code 200
    Then there is a timer-delete event with field status with value RECEIPT_TIMER_GENERATION_DELETED_SCHEDULED_SEND
    And these events are related to each payment token
    Then there is a receipt-ok event with field status with value RT_SEND_SUCCESS
    And these events are related to each notice number
