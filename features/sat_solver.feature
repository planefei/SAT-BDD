@sat_solver
Feature: DPLL SAT Solver

  A DPLL-based SAT solver accepts a propositional formula in Conjunctive
  Normal Form (CNF) and determines whether it is satisfiable (SAT) or
  unsatisfiable (UNSAT).

  Background:
    Given the DPLL SAT solver is available

  # ---------------------------------------------------------------------------
  # Basic satisfiability
  # ---------------------------------------------------------------------------

  @smoke
  Scenario: Single positive unit clause is satisfiable
    Given the CNF formula [[1]]
    When I run the SAT solver
    Then the result should be SAT
    And the assignment should satisfy the formula

  @smoke
  Scenario: Single negative unit clause is satisfiable
    Given the CNF formula [[-1]]
    When I run the SAT solver
    Then the result should be SAT
    And the assignment should satisfy the formula

  @smoke
  Scenario: Contradiction of unit clauses is unsatisfiable
    Given the CNF formula [[1], [-1]]
    When I run the SAT solver
    Then the result should be UNSAT

  # ---------------------------------------------------------------------------
  # Clause types
  # ---------------------------------------------------------------------------

  Scenario: Two-literal disjunction is satisfiable
    Given the CNF formula [[1, 2]]
    When I run the SAT solver
    Then the result should be SAT
    And the assignment should satisfy the formula

  Scenario: Conjunction of complementary two-literal clauses is unsatisfiable
    Given the CNF formula [[1, 2], [-1, -2], [1, -2], [-1, 2]]
    When I run the SAT solver
    Then the result should be UNSAT

  # ---------------------------------------------------------------------------
  # Unit propagation
  # ---------------------------------------------------------------------------

  Scenario: Unit propagation resolves forced assignments
    Given the CNF formula [[1], [1, 2], [-2, 3]]
    When I run the SAT solver
    Then the result should be SAT
    And the assignment should satisfy the formula

  # ---------------------------------------------------------------------------
  # Pure literal elimination
  # ---------------------------------------------------------------------------

  Scenario: Pure literal is set without branching
    Given the CNF formula [[1, 2], [1, 3]]
    When I run the SAT solver
    Then the result should be SAT
    And the assignment should satisfy the formula

  # ---------------------------------------------------------------------------
  # 3-SAT benchmark cases
  # ---------------------------------------------------------------------------

  @regression
  Scenario: Satisfiable 3-SAT formula
    Given the CNF formula [[1, 2, 3], [-1, -2, 3], [1, -2, -3], [-1, 2, -3]]
    When I run the SAT solver
    Then the result should be SAT
    And the assignment should satisfy the formula

  @regression
  Scenario: Satisfiable 3-SAT with five variables
    Given the CNF formula [[1, 2, -3], [-1, 3, 4], [2, -4, 5], [-2, -3, -5], [1, -2, 4]]
    When I run the SAT solver
    Then the result should be SAT
    And the assignment should satisfy the formula

  @regression
  Scenario: Unsatisfiable pigeonhole principle (2 pigeons, 1 hole)
    # PHP(2,1): assign 2 pigeons to 1 hole with no two pigeons in same hole
    # Variables: x_ij = pigeon i in hole j  (only hole 1 exists)
    # Each pigeon must be in a hole: (x11) AND (x21)
    # No hole has two pigeons:       (NOT x11 OR NOT x21)
    Given the CNF formula [[1], [2], [-1, -2]]
    When I run the SAT solver
    Then the result should be UNSAT

  # ---------------------------------------------------------------------------
  # Data-driven scenarios
  # ---------------------------------------------------------------------------

  @regression
  Scenario Outline: Various small CNF formulas
    Given the CNF formula <formula>
    When I run the SAT solver
    Then the result should be <expected>

    Examples:
      | formula                        | expected |
      | [[1, -1]]                      | SAT      |
      | [[1, 2], [-1], [-2]]           | UNSAT    |
      | [[1], [2], [3]]                | SAT      |
      | [[-1], [-2], [-3]]             | SAT      |
      | [[1, 2], [-1, 2], [-2]]        | UNSAT    |
