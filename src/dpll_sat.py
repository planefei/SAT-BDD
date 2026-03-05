"""
DPLL-based SAT Solver

Decides satisfiability of propositional logic formulas in Conjunctive Normal Form (CNF).

Formula representation:
  - A CNF formula is a list of clauses.
  - A clause is a frozenset of integer literals.
  - A positive integer n represents variable n.
  - A negative integer -n represents the negation of variable n.

Example:
  (x1 OR NOT x2) AND (NOT x1 OR x3) is encoded as:
  [{1, -2}, {-1, 3}]
"""

from __future__ import annotations
from typing import Optional


# ---------------------------------------------------------------------------
# Type aliases
# ---------------------------------------------------------------------------
Literal = int          # positive → variable, negative → negated variable
Clause  = frozenset    # frozenset[Literal]
Formula = list         # list[Clause]
Model   = dict         # dict[int, bool]   variable → truth value


# ---------------------------------------------------------------------------
# Core DPLL
# ---------------------------------------------------------------------------

def dpll(formula: Formula, assignment: Model) -> Optional[Model]:
    """
    Run the DPLL algorithm on *formula* given a partial *assignment*.

    Returns a satisfying assignment (dict) if the formula is SAT,
    or None if it is UNSAT under the current assignment.
    """
    # 1. Unit propagation
    formula, assignment, conflict = unit_propagate(formula, assignment)
    if conflict:
        return None

    # 2. Pure literal elimination
    formula, assignment = pure_literal_eliminate(formula, assignment)

    # 3. Base cases
    if not formula:           # all clauses satisfied
        return assignment
    if any(len(c) == 0 for c in formula):   # empty clause → conflict
        return None

    # 4. Choose an unassigned variable (first literal heuristic)
    var = choose_variable(formula)

    # 5. Branch: try True then False
    for value in (True, False):
        new_assignment = dict(assignment)
        new_assignment[var] = value
        literal = var if value else -var
        new_formula = simplify(formula, literal)
        result = dpll(new_formula, new_assignment)
        if result is not None:
            return result

    return None  # both branches failed


def solve(formula: Formula) -> Optional[Model]:
    """
    Public entry point.  Returns a satisfying assignment or None.
    """
    return dpll([frozenset(c) for c in formula], {})


# ---------------------------------------------------------------------------
# Helper routines
# ---------------------------------------------------------------------------

def simplify(formula: Formula, literal: Literal) -> Formula:
    """
    Apply *literal* to *formula*:
      - Drop any clause that contains *literal* (it is satisfied).
      - Remove the negation of *literal* from every remaining clause.
    """
    neg = -literal
    result = []
    for clause in formula:
        if literal in clause:
            continue                      # clause is satisfied
        result.append(clause - {neg})     # remove the falsified literal
    return result


def unit_propagate(formula: Formula, assignment: Model):
    """
    Repeatedly find unit clauses (single-literal clauses) and force them.
    Returns (new_formula, new_assignment, conflict_found).
    """
    assignment = dict(assignment)
    changed = True
    while changed:
        changed = False
        for clause in formula:
            if len(clause) == 0:
                return formula, assignment, True  # conflict
            if len(clause) == 1:
                (lit,) = clause
                var = abs(lit)
                val = lit > 0
                if var in assignment:
                    if assignment[var] != val:
                        return formula, assignment, True  # contradiction
                else:
                    assignment[var] = val
                    formula = simplify(formula, lit)
                    changed = True
                    break  # restart loop with updated formula
    return formula, assignment, False


def pure_literal_eliminate(formula: Formula, assignment: Model):
    """
    Find variables that appear with only one polarity across all remaining
    clauses and set them to satisfy every clause they appear in.
    """
    assignment = dict(assignment)
    changed = True
    while changed:
        changed = False
        # Collect all literals present in the formula
        all_literals: set[Literal] = set()
        for clause in formula:
            all_literals |= clause

        for lit in list(all_literals):
            if -lit not in all_literals:   # pure literal
                var = abs(lit)
                val = lit > 0
                if var not in assignment:
                    assignment[var] = val
                    formula = simplify(formula, lit)
                    changed = True
                    break  # restart with updated formula

    return formula, assignment


def choose_variable(formula: Formula) -> int:
    """
    Pick the first unassigned variable seen in the formula (FIFO heuristic).
    """
    for clause in formula:
        for lit in clause:
            return abs(lit)
    raise RuntimeError("choose_variable called on empty formula")


# ---------------------------------------------------------------------------
# Verification helper
# ---------------------------------------------------------------------------

def verify(formula: Formula, assignment: Model) -> bool:
    """
    Check that *assignment* satisfies every clause in *formula*.
    """
    for clause in formula:
        satisfied = any(
            (lit > 0 and assignment.get(abs(lit), False)) or
            (lit < 0 and not assignment.get(abs(lit), True))
            for lit in clause
        )
        if not satisfied:
            return False
    return True


# ---------------------------------------------------------------------------
# CLI demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    # Simple hard-coded examples if no file is provided
    examples = [
        # (description, formula in CNF)
        (
            "Satisfiable: (x1 OR x2) AND (NOT x1 OR x2) AND (x1 OR NOT x2)",
            [[1, 2], [-1, 2], [1, -2]],
        ),
        (
            "Unsatisfiable: (x1) AND (NOT x1)",
            [[1], [-1]],
        ),
        (
            "3-SAT satisfiable example",
            [[1, 2, 3], [-1, -2, 3], [1, -2, -3], [-1, 2, -3]],
        ),
    ]

    for desc, formula in examples:
        result = solve(formula)
        print(f"\n{desc}")
        print(f"  Formula : {formula}")
        if result is not None:
            print(f"  Result  : SAT  — assignment = {result}")
            assert verify(formula, result), "BUG: returned assignment does not satisfy formula!"
        else:
            print("  Result  : UNSAT")
