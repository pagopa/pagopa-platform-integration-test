Feature: showing off behave

  Background:
    Given systems up


  Scenario: run a simple test
    Given we have behave installed
    When we implement a test
    Then behave will test it for us!
