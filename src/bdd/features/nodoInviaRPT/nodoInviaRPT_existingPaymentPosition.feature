Feature: User pays a single payment from existing payment position via nodoInviaRPT

  Background:
    Given systems up

    @runnable @nodo_invia_rpt @refactor_test
#  Scenario: User pays a single payment with single transfer and no stamp on nodoInviaRPT that exists already in GPD
    Scenario: User pays a single payment with single transfer and no stamp that exists already in GPD
    Given a single RPT of type BBT with 1 transfers of which 0 are stamps
    And an existing payment position related to first RPT with segregation code equals to 48 and state equals to VALID
    When the user tries to pay the RPT on EC website
    Then the user is redirected on Checkout
    And the payment is done

  @runnable @nodo_invia_rpt @refactor_test
  Scenario: User pays a single payment with no transfer and one stamp on nodoInviaRPT that exists already in GPD
    Given a single RPT of type BBT with 1 transfers of which 1 are stamps
    And an existing payment position related to first RPT with segregation code equals to 48 and state equals to VALID
    When the user tries to pay the RPT on EC website
    Then the user is redirected on Checkout
    And the payment is done

  # ===============================================================================================
  # ===============================================================================================

    @runnable @nodo_invia_rpt @refactor_test
    Scenario: User pays a single payment with single transfer and one stamp on nodoInviaRPT that exists already in GPD
    Given a single RPT of type BBT with 2 transfers of which 1 are stamps
    And an existing payment position related to first RPT with segregation code equals to 48 and state equals to VALID
    When the user tries to pay the RPT on EC website
    Then the user is redirected on Checkout
    And the payment is done

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @refactor_test_unhappy
  Scenario: User tries to pay a single payment with single transfer and no stamp on nodoInviaRPT that exists already in GPD in invalid state
    Given a single RPT of type BBT with 1 transfers of which 0 are stamps
    And an existing payment position related to first RPT with segregation code equals to 48 and state equals to DRAFT
    When the user tries to pay the RPT on EC website
    Then execute NM1-to-NMU conversion in wisp-converter fails
    And existing debt position was invalid but has sent a KO receipt

#    Then the execution of "Fails on execute NM1-to-NMU conversion in wisp-converter" was successful
#    And the execution of "Check if existing debt position was invalid but has sent a KO receipt" was successful

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @refactor_test_unhappy
  Scenario: User tries to pay a single payment on nodoInviaRPT that was inserted from ACA and is in valid state
    Given a single RPT of type BBT with 1 transfers of which 0 are stamps
    And an existing payment position related to first RPT with segregation code equals to 01 and state equals to VALID
    When the user tries to pay the RPT on EC website
    Then the user is redirected on Checkout
    And the payment is done

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @refactor_test_unhappy
  Scenario: User tries to pay a single payment on nodoInviaRPT that was inserted from ACA and is in invalid state
    Given a single RPT of type BBT with 1 transfers of which 0 are stamps
    And an existing payment position related to first RPT with segregation code equals to 01 and state equals to DRAFT
    When the user tries to pay the RPT on EC website
    Then the user is redirected on Checkout
    And the payment is done


#Execute redirect and complete payment from NodoInviaRPT
  Scenario: Execute NM1-to-NMU conversion in wisp-converter
    Given a valid session identifier to be redirected to WISP dismantling
    When the user continue the session in WISP dismantling
    Then the user receives the HTTP status code 302
    And the user can be redirected to Checkout

  Scenario: Retrieve all related notice numbers from executed redirect
    Given a waiting time of 2 seconds to wait for Nodo to write RE events
    Given the first IUV code of the sent RPTs
    When the user searches for flow steps by IUVs
    Then the user receives the HTTP status code 200
    And all the related notice numbers can be retrieved

  Scenario: Send one or more activatePaymentNoticeV2 requests
    # executing 'activation' on first payment notice generated by GPD (not necessarely related only to first RPT!)
    Given a valid activatePaymentNoticeV2 request on first payment notice
    When the creditor institution sends a activatePaymentNoticeV2 action
    Then the creditor institution receives the HTTP status code 200
    And the response contains the field outcome with value OK
    And the response contains the field paymentToken with non-null value
    And the payment token can be retrieved and associated to first RPT
    # executing 'activation' on second payment notice generated by GPD, if exists
    Given a valid activatePaymentNoticeV2 request on second payment notice
    When the creditor institution sends a activatePaymentNoticeV2 action
    Then the creditor institution receives the HTTP status code 200
    And the response contains the field outcome with value OK
    And the response contains the field paymentToken with non-null value
    And the payment token can be retrieved and associated to second RPT
    # executing 'activation' on third payment notice generated by GPD, if exists
    Given a valid activatePaymentNoticeV2 request on third payment notice
    When the creditor institution sends a activatePaymentNoticeV2 action
    Then the creditor institution receives the HTTP status code 200
    And the response contains the field outcome with value OK
    And the response contains the field paymentToken with non-null value
    And the payment token can be retrieved and associated to third RPT
    # executing 'activation' on fourth payment notice generated by GPD, if exists
    Given a valid activatePaymentNoticeV2 request on fourth payment notice
    When the creditor institution sends a activatePaymentNoticeV2 action
    Then the creditor institution receives the HTTP status code 200
    And the response contains the field outcome with value OK
    And the response contains the field paymentToken with non-null value
    And the payment token can be retrieved and associated to fourth RPT
    # executing 'activation' on fifth payment notice generated by GPD, if exists
    Given a valid activatePaymentNoticeV2 request on fifth payment notice
    When the creditor institution sends a activatePaymentNoticeV2 action
    Then the creditor institution receives the HTTP status code 200
    And the response contains the field outcome with value OK
    And the response contains the field paymentToken with non-null value
    And the payment token can be retrieved and associated to fifth RPT

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

  Scenario: Execute redirect and complete payment from NodoInviaCarrelloRPT
    When the execution of "Execute NM1-to-NMU conversion in wisp-converter" was successful
    Then the execution of "Retrieve all related notice numbers from executed redirect" was successful
    And the execution of "Send a checkPosition request" was successful
    And the execution of "Send one or more activatePaymentNoticeV2 requests" was successful
    And the execution of "Check if WISP session timers were created" was successful
    And the execution of "Send a closePaymentV2 request" was successful
    And the execution of "Check if WISP session timers were deleted and all RTs were sent" was successful
    And the execution of "Check the paid payment positions" was successful
