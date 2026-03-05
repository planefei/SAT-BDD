"""
Step definitions for sat_solver.feature
Uses the `behave` BDD framework.
"""

import ast
import sys
import os

# Make the src package importable when running behave from the project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from behave import given, when, then  # type: ignore
from dpll_sat import solve, verify


# ---------------------------------------------------------------------------
# Given
# ---------------------------------------------------------------------------

@given("the DPLL SAT solver is available")
def step_solver_available(context):
    """Sanity-check that the solver module loaded correctly."""
    assert callable(solve), "solve() is not callable"


@given("the CNF formula {formula}")
def step_given_formula(context, formula):
    """Parse the CNF formula from a JSON/Python-literal string."""
    context.formula = ast.literal_eval(formula)


# ---------------------------------------------------------------------------
# When
# ---------------------------------------------------------------------------

@when("I run the SAT solver")
def step_run_solver(context):
    context.result = solve(context.formula)


# ---------------------------------------------------------------------------
# Then
# ---------------------------------------------------------------------------

@then("the result should be SAT")
def step_result_sat(context):
    assert context.result is not None, (
        f"Expected SAT but got UNSAT for formula {context.formula}"
    )


@then("the result should be UNSAT")
def step_result_unsat(context):
    assert context.result is None, (
        f"Expected UNSAT but got SAT with assignment {context.result} "
        f"for formula {context.formula}"
    )


@then("the assignment should satisfy the formula")
def step_verify_assignment(context):
    assert context.result is not None, "No assignment to verify (result is UNSAT)"
    assert verify(context.formula, context.result), (
        f"Assignment {context.result} does NOT satisfy formula {context.formula}"
    )
