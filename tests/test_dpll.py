"""
Unit tests for the DPLL SAT solver (pytest).
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from dpll_sat import (
    solve,
    verify,
    simplify,
    unit_propagate,
    pure_literal_eliminate,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def assert_sat(formula):
    result = solve(formula)
    assert result is not None, f"Expected SAT: {formula}"
    assert verify(formula, result), f"Assignment {result} does not satisfy {formula}"
    return result


def assert_unsat(formula):
    result = solve(formula)
    assert result is None, f"Expected UNSAT but got {result}: {formula}"


# ---------------------------------------------------------------------------
# simplify()
# ---------------------------------------------------------------------------

class TestSimplify:
    def test_removes_satisfied_clause(self):
        formula = [frozenset([1, 2]), frozenset([-1, 3])]
        result = simplify(formula, 1)
        # Clause {1, 2} is satisfied → dropped; clause {-1, 3} loses -1
        assert frozenset([3]) in result
        assert not any(1 in c for c in result)

    def test_removes_negation_from_clause(self):
        formula = [frozenset([-1, 2])]
        result = simplify(formula, 1)
        assert result == [frozenset([2])]

    def test_empty_formula_stays_empty(self):
        assert simplify([], 1) == []


# ---------------------------------------------------------------------------
# unit_propagate()
# ---------------------------------------------------------------------------

class TestUnitPropagate:
    def test_single_unit_clause(self):
        formula = [frozenset([1]), frozenset([1, 2])]
        new_f, asgn, conflict = unit_propagate(formula, {})
        assert not conflict
        assert asgn[1] is True
        assert new_f == []   # both clauses satisfied

    def test_contradiction_detected(self):
        formula = [frozenset([1]), frozenset([-1])]
        _, _, conflict = unit_propagate(formula, {})
        assert conflict

    def test_chain_propagation(self):
        # x1=T forces x2=T forces x3=T
        formula = [frozenset([1]), frozenset([-1, 2]), frozenset([-2, 3])]
        _, asgn, conflict = unit_propagate(formula, {})
        assert not conflict
        assert asgn == {1: True, 2: True, 3: True}


# ---------------------------------------------------------------------------
# pure_literal_eliminate()
# ---------------------------------------------------------------------------

class TestPureLiteralEliminate:
    def test_pure_positive_literal(self):
        # x1 appears only positively
        formula = [frozenset([1, 2]), frozenset([1, 3])]
        new_f, asgn = pure_literal_eliminate(formula, {})
        assert asgn.get(1) is True
        assert new_f == []

    def test_pure_negative_literal(self):
        # x1 appears only negated; x2 appears with both polarities → not pure
        formula = [frozenset([-1, 2]), frozenset([-1, -2])]
        _, asgn = pure_literal_eliminate(formula, {})
        assert asgn.get(1) is False

    def test_non_pure_literal_unchanged(self):
        formula = [frozenset([1, 2]), frozenset([-1, 3])]
        _, asgn = pure_literal_eliminate(formula, {})
        assert 1 not in asgn   # x1 appears with both polarities


# ---------------------------------------------------------------------------
# solve() — satisfiable cases
# ---------------------------------------------------------------------------

class TestSolve:
    def test_single_positive_unit(self):
        assert_sat([[1]])

    def test_single_negative_unit(self):
        result = assert_sat([[-1]])
        assert result[1] is False

    def test_two_literal_clause(self):
        assert_sat([[1, 2]])

    def test_multi_clause_sat(self):
        assert_sat([[1, 2], [-1, 2], [1, -2]])

    def test_tautological_clause(self):
        assert_sat([[1, -1]])

    def test_three_positive_units(self):
        result = assert_sat([[1], [2], [3]])
        assert result == {1: True, 2: True, 3: True}

    def test_three_negative_units(self):
        result = assert_sat([[-1], [-2], [-3]])
        assert result == {1: False, 2: False, 3: False}

    def test_3sat_satisfiable(self):
        assert_sat([[1, 2, 3], [-1, -2, 3], [1, -2, -3], [-1, 2, -3]])

    def test_five_variable_sat(self):
        assert_sat([[1, 2, -3], [-1, 3, 4], [2, -4, 5], [-2, -3, -5], [1, -2, 4]])

    def test_empty_formula_is_trivially_sat(self):
        result = solve([])
        assert result == {}

    def test_forced_chain(self):
        # x1=T → x2=T → x3=T
        assert_sat([[1], [-1, 2], [-2, 3]])

    # ---------------------------------------------------------------------------
    # solve() — unsatisfiable cases
    # ---------------------------------------------------------------------------

    def test_contradiction_unit_clauses(self):
        assert_unsat([[1], [-1]])

    def test_all_polarities_two_vars(self):
        assert_unsat([[1, 2], [-1, 2], [1, -2], [-1, -2]])

    def test_pigeonhole_2_into_1(self):
        # PHP(2,1): both pigeons must go to hole 1, but can't share
        assert_unsat([[1], [2], [-1, -2]])

    def test_three_clause_unsat(self):
        assert_unsat([[1, 2], [-1], [-2]])

    def test_longer_unsat(self):
        assert_unsat([[1, 2], [-1, 2], [-2]])

    # ---------------------------------------------------------------------------
    # verify()
    # ---------------------------------------------------------------------------

    def test_verify_correct_assignment(self):
        # x1=T satisfies clause 1; x3=T satisfies clause 2
        formula = [[1, 2], [-1, 3]]
        assert verify(formula, {1: True, 2: False, 3: True})

    def test_verify_wrong_assignment(self):
        formula = [[1], [-1]]
        assert not verify(formula, {1: True})
        assert not verify(formula, {1: False})
