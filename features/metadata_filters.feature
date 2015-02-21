Feature: Filter by meta-data

  @wip
  Scenario: Filter by genre
    Given There is a file with a "kuku" genre exists in source
    And I execute with parameters "--filter genre:kuku source target"
    Then file should not exists in target

