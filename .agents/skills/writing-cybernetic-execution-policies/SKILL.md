---
name: writing-cybernetic-execution-policies
description: 'Use after an approved clarification brief and goal contract exist, before starting an executable /goal. Creates an implementation plan as a cybernetic execution policy: dependency matrix, batch cadence, destructive intermediate-state policy, test/sensor governance, semantic invariants, tactical degrees of freedom, phase gates, and execution rhythm. Does not implement code and does not start /goal execution.'
---

# Writing Cybernetic Execution Policies

## Overview

Create the execution control law for a complex AI coding task.

This skill converts:

- clarification brief
- goal contract

into:

- candidate execution policy / implementation plan

The plan is not approved until `$reviewing-cybernetic-control-structures` marks it Approved.

Use `assets/execution-policy-template.md`.

## Core Boundary

This skill does not clarify requirements, does not write the goal contract, does not review its own plan, and does not implement code.

## Required Sections

The execution policy must include:

1. Source Contracts
2. Confirmed Semantic Invariants
3. Tactical Degrees of Freedom
4. Dependency Matrix
5. Batch Cadence
6. Destructive Intermediate-State Policy
7. Sensor / Test Governance
8. Old Test Retirement and Rewrite Policy
9. Phase Gates
10. Execution Rhythm
11. Stop Conditions
12. Progress Log Rules
13. Candidate Plan Tasks

## Batch Cadence

For large structural changes:

- intermediate steps inside a batch may temporarily break build, tests, or UI;
- each batch must end in an openable or meaningfully verifiable state;
- batch size should be large enough to avoid test-driven local minima;
- batch size should be small enough that failures remain diagnosable.

## Sensor / Test Governance

Tests are sensors, not the objective.

Classify tests as:

- strong sensors: preserve;
- weak or stale sensors: inspect before obeying;
- obsolete sensors: may be retired and rewritten.

If many tests conflict with confirmed product semantics, implement the product behavior first, then rewrite product-level tests.

Do not let brittle old tests define the target behavior.

## Output Format

Create:

```text
docs/superpowers/plans/YYYY-MM-DD-<slug>.md
```

Then respond:

```markdown
Created candidate execution policy:

`docs/superpowers/plans/YYYY-MM-DD-slug.md`

Control-law summary:
- Semantic invariants: ...
- Batch cadence: ...
- Sensor governance: ...
- Phase gates: ...

Next step:
Use `$reviewing-cybernetic-control-structures` before starting runtime /goal.
```

## Validation Checklist

- [ ] The plan distinguishes semantic invariants from tactical degrees of freedom.
- [ ] The plan has dependency matrix.
- [ ] The plan has batch cadence.
- [ ] The plan allows destructive intermediate states only within approved batches.
- [ ] Each batch ends in an openable/verifiable state.
- [ ] The plan treats tests as sensors, not objectives.
- [ ] The plan includes stale test retirement/rewrite policy.
- [ ] The plan does not claim to be approved.
- [ ] The skill does not execute implementation.
