Feature: Auth service API
  Validate the auth-service flows migrated from the legacy checkout api tests.

  Background:
    Given that checkout host is configured through environment variable
    And the auth service environment variables are configured

  @auth-service @positive
  Scenario: Successful auth flow returns a session token and expected user data
    When I request the auth login URL
    Then the response has status code 200
    And the auth login response exposes a valid redirect URL
    When I open the auth redirect URL
    Then the response has status code 200
    And the auth code is extracted from the redirect response
    When I exchange the auth code for a session token
    Then the response has status code 200
    And the auth token is returned in the response
    When I request the authenticated user profile with the active session token
    Then the response has status code 200
    And the authenticated user profile matches the configured auth user
    When I logout from auth service with the active session token
    Then the response has status code 204

  @auth-service @negative
  Scenario: Invalid auth code and invalid session token are rejected
    When I request the auth login URL
    Then the response has status code 200
    And the auth login response exposes a valid redirect URL
    When I open the auth redirect URL
    Then the response has status code 200
    When I exchange an invalid auth code for a session token
    Then the response has status code 401
    Given an invalid auth session token
    When I request an authenticated payment request with the invalid session token
    Then the response has status code 401
    When I request the authenticated user profile with the invalid session token
    Then the response has status code 401