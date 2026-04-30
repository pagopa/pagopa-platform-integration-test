Feature: Auth service
  Validate the auth-service flows migrated from the legacy checkout api tests.

  Background:
    Given that checkout host is configured through environment variable
    And the auth service environment variables are configured

  @auth-service @checkout @positive
  Scenario: Successful authentication flow returns a session token and the expected user profile
    When the user requests the auth login URL
    Then the response has status code 200
    And the auth login response exposes a valid redirect URL
    When the user opens the auth redirect URL
    Then the response has status code 200
    And the auth code is extracted from the redirect response
    When the user exchanges the auth code for a session token
    Then the response has status code 200
    And the auth token is returned in the response
    When the user requests the authenticated user profile with the active session token
    Then the response has status code 200
    And the authenticated user profile matches the configured auth user
    When the user logs out from auth service with the active session token
    Then the response has status code 204

  @auth-service @checkout @negative
  Scenario: Invalid auth code and invalid session token are rejected
    When the user requests the auth login URL
    Then the response has status code 200
    And the auth login response exposes a valid redirect URL
    When the user opens the auth redirect URL
    Then the response has status code 200
    When the user exchanges an invalid auth code for a session token
    Then the response has status code 401
    Given an invalid auth session token
    When the user requests an authenticated payment request with the invalid session token
    Then the response has status code 401
    When the user requests the authenticated user profile with the invalid session token
    Then the response has status code 401