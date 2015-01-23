Feature: Simple files copy


  Scenario: Copy files from source to target
    Given Target folder is empty
    And I execute with parameters "source target"
    Then Target and source folders should be identical