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

## Required Infrastructure

Follow `$cybernetic-superpowers-infrastructure`.

This skill does not replace `$superpowers:writing-plans`.

For non-trivial implementation plans, invoke `$superpowers:writing-plans` or load and follow its `SKILL.md` instructions as the required planning substrate. Merely mentioning the skill, citing it, or imitating generic planning is not sufficient.

This skill supplies the cybernetic constraints that the planning substrate must preserve:

- confirmed semantic invariants;
- tactical degrees of freedom;
- dependency matrix requirement;
- batch cadence;
- destructive intermediate-state policy;
- sensor/test governance;
- stale test retirement and rewrite policy.

If `$superpowers:writing-plans` is unavailable for a non-trivial implementation plan, stop and report that required planning infrastructure is missing. Do not self-substitute with an unreviewed internal plan.

## Required Sections

The execution policy must include:

1. Source Contracts
2. Superpowers Planning Substrate
3. Confirmed Semantic Invariants
4. Tactical Degrees of Freedom
5. Dependency Matrix
6. Batch Cadence
7. Destructive Intermediate-State Policy
8. Sensor / Test Governance
9. Old Test Retirement and Rewrite Policy
10. Phase Gates
11. Execution Rhythm
12. Stop Conditions
13. Progress Log Rules
14. Candidate Plan Tasks

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
- Planning substrate: ...
- Semantic invariants: ...
- Batch cadence: ...
- Sensor governance: ...
- Phase gates: ...

Next step:
Use `$reviewing-cybernetic-control-structures` before starting runtime /goal.
```

## Validation Checklist

- [ ] Non-trivial implementation plans invoke `$superpowers:writing-plans` or load and follow its `SKILL.md` instructions, otherwise stop/report missing infrastructure.
- [ ] The plan records planning substrate status.
- [ ] The plan does not self-substitute for a missing required planning substrate.
- [ ] The plan distinguishes semantic invariants from tactical degrees of freedom.
- [ ] The plan has dependency matrix.
- [ ] The plan has batch cadence.
- [ ] The plan allows destructive intermediate states only within approved batches.
- [ ] Each batch ends in an openable/verifiable state.
- [ ] The plan treats tests as sensors, not objectives.
- [ ] The plan includes stale test retirement/rewrite policy.
- [ ] The plan does not claim to be approved.
- [ ] The skill does not execute implementation.
