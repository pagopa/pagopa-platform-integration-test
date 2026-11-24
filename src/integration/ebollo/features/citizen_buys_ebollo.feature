# qa-hub: FEAT_001_EBollo
# language: en
@eBollo
@EBOLLO_001
Feature: As a citizen, I want to purchase an eBollo to access a document that requires the affixing of a revenue stamp

  @test
  @EBOLLO_001_01
  Scenario: A citizen successfully purchases an eBollo on the Creditor Institution's website when requesting access to documents
    When the user pays the eBollo on the checkout page

  @EBOLLO_001_02
  Scenario: A citizen cancels the payment of an eBollo on the Creditor Institution's website

  @EBOLLO_001_03
  Scenario: A citizen gets a generic error when purchasing an eBollo on the Creditor Institution's website

  @EBOLLO_001_04
  Scenario: A citizen gets a specific error when purchasing an eBollo on the Creditor Institution's website because the creation of a debt position failed
