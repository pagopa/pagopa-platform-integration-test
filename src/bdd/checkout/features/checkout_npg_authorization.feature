Feature: Checkout eCommerce — NPG payment gateway
  Validate the eCommerce checkout API flows for authorization requests via NPG.

  Background:
    Given that checkout host is configured through environment variable
    And the checkout NPG environment variables are configured

  # ---------------------------------------------------------------------------
  # Authorization Requests
  # ---------------------------------------------------------------------------

  @checkout @npg @authorization @negative
  Scenario Outline: Authorization request returns 401 when JWT token is absent
    Given the credit card payment method id is resolved
    And an NPG session is created with language "<lang>"
    And a random valid notice code is generated
    And a transaction is created for the current session
    When the user requests authorization without JWT token using language "<lang>"
    Then the response has status code 401

    Examples:
      | lang |
      | it   |
      | fr   |
      | de   |
      | sl   |
      | en   |

  @checkout @npg @authorization @positive
  Scenario: Authorization request with JWT token returns authorization URL
    Given the credit card payment method id is resolved
    And an NPG session is created with language "it"
    And a random valid notice code is generated
    And a transaction is created for the current session
    And the NPG card fields are filled with test card data
    When the user requests authorization with JWT token using language "it"
    Then the response has status code 200
    And the authorization response contains a valid authorization URL
    And the authorization request id matches the order id
