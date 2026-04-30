Feature: Checkout eCommerce — NPG payment gateway
  Validate the eCommerce checkout API flows for NPG card session creation by language.

  Background:
    Given that checkout host is configured through environment variable
    And the checkout NPG environment variables are configured

  # ---------------------------------------------------------------------------
  # NPG Session Creation (by language)
  # ---------------------------------------------------------------------------

  @checkout @npg @session @positive
  Scenario Outline: NPG card session is created successfully for each language
    Given the credit card payment method id is resolved
    When the user creates an NPG card session with language "<lang>"
    Then the response has status code 200
    And the NPG session response contains valid card form fields with payment method CARDS

    Examples:
      | lang |
      | it   |
      | fr   |
      | de   |
      | sl   |
      | en   |
