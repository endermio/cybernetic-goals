# Execution Policy: [Name]

## Execution Policy Status

Status: `Candidate`

## Source Contracts

- Clarification: `[path]`
- Goal contract: `[path]`

## Confirmed Semantic Invariants

These cannot be changed during runtime execution without stopping.

- [semantic invariant]

## Tactical Degrees of Freedom

These may change during execution if invariants are preserved.

- [implementation detail]
- [file organization detail]
- [test fixture detail]

## Dependency Matrix

| Workstream | Owns | Depends on | Can run in parallel with | Gate |
|---|---|---|---|---|
| A | [area] | [dependency] | [parallel work] | [gate] |

## Batch Cadence

- Intermediate steps inside a batch may temporarily break build/tests/UI when necessary.
- Each batch must end in an openable or meaningfully verifiable state.
- Batch size should avoid both micro-step local minima and huge unobservable changes.

## Destructive Intermediate-State Policy

Allowed inside a batch:

- [temporary breakage]

Not allowed even inside a batch:

- [semantic violation]
- [security/permission violation]

Batch-end requirements:

- [openable/verifiable condition]

## Sensor / Test Governance

Tests are sensors, not objectives.

Strong sensors to preserve:

- [test/eval]

Weak or stale sensors to inspect before obeying:

- [test/eval]

Obsolete sensors that may be retired and rewritten:

- [test/eval]

Product-level verification has priority over preserving brittle old tests.

## Old Test Retirement and Rewrite Policy

A test may be retired or rewritten when:

- it encodes old product semantics;
- it over-constrains implementation details;
- it conflicts with confirmed semantic invariants;
- it prevents correct structural change.

Any retired/replaced test must be recorded in the progress log with reason and replacement coverage.

## Phase Gates

Before implementation:

- control review status must be Approved.

Before moving to next batch:

- current batch-end condition met;
- progress log updated;
- no confirmed semantic invariant violated.

Before completion:

- final verification evidence recorded;
- no unresolved conflict among clarification, goal, plan, and review.

## Execution Rhythm

- Execute serially unless review explicitly approves parallel subagents.
- If subagents are used, only one implementation subagent is active at a time unless approved.
- Do not let runtime `/goal` rewrite this policy.

## Stop Conditions

Stop if:

- the plan conflicts with clarification or goal;
- confirmed semantics appear wrong or insufficient;
- sensor governance is insufficient for a failing check;
- executing further requires a new human decision;
- the approved batch cadence cannot be followed.

## Progress Log Rules

Maintain:

- `docs/superpowers/progress/YYYY-MM-DD-slug.md`

Each entry must include:

- batch/checkpoint
- files changed
- commands run
- result
- sensor interpretation
- current risk
- next step

## Candidate Plan Tasks

### Batch 1: [Name]

Goal:

- [product slice]

Allowed intermediate breakage:

- [breakage]

Batch-end gate:

- [gate]

Steps:

- [ ] [step]
