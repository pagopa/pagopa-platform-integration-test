Feature: showing off behave

  @runnable
  Scenario: run a simple test
    Given we have behave installed
    When we implement a test
    Then behave will test it for us!

  @runnable
  Scenario: run a simple test 1
    Given we have behave installed
    When we implement a test with assert false
    Then behave will test it for us!

  @runnable
  Scenario: run a simple test 2
    Given we have behave installed
    When we implement a test
    Then behave will test it for us!

  @runnable
  Scenario: run a simple test 3
    Given we have behave installed
    When we implement a test
    Then behave will test it for us!
