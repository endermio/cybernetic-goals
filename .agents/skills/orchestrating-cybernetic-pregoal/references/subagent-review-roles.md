# Subagent Review Roles for Pre-goal Compilation

Use these roles only when the user explicitly authorizes subagents.

## Requirement Traceability Reviewer

Input: clarification brief, goal contract, execution policy.

Check:

- Every confirmed human decision appears in the goal and plan.
- No confirmed semantic decision is weakened, reworded into ambiguity, or converted into an implementation option.
- No new product requirement appears without source.

## Control Contract Reviewer

Input: clarification brief and goal contract.

Check:

- Goal has success conditions, boundaries, invariants, verification surfaces, stop conditions, and source of truth.
- Goal does not ask runtime `/goal` to generate or approve its own plan.
- Goal separates product semantics from execution tactics.

## Execution Policy / Cadence Reviewer

Input: goal contract and execution policy.

Check:

- Plan contains dependency matrix.
- Plan defines batch cadence.
- Plan defines destructive intermediate-state policy.
- Plan defines batch-end openable or verifiable state.
- Plan avoids both tiny test-bound steps and huge unobservable batches.

## Sensor Governance Reviewer

Input: goal contract and execution policy.

Check:

- Tests are treated as sensors, not objectives.
- Old tests may be preserved, retired, or rewritten according to explicit rules.
- Product-level verification dominates brittle implementation-level tests.
- Sensor hierarchy is clear: build, API smoke, screenshots, product behavior, old unit tests.

## Runtime Boundary Reviewer

Input: all artifacts plus proposed runtime `/goal`.

Check:

- Runtime `/goal` only executes approved artifacts.
- Runtime `/goal` does not rewrite requirements, plan, sensors, or review.
- Runtime `/goal` references clarification, goal, plan, and review.
- Runtime `/goal` stops if artifacts conflict or become insufficient.
