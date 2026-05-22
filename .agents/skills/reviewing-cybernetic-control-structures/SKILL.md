---
name: reviewing-cybernetic-control-structures
description: 'Use after clarification, goal contract, and execution policy files exist, before starting /goal execution. Reviews the whole AI control structure, not only the plan: requirement traceability, goal fidelity, control law quality, sensor/test governance, batch cadence, phase gates, stop conditions, and semantic-vs-tactical boundaries. Produces a control review file under docs/superpowers/control-reviews/ and must mark Approved before runtime /goal may start.'
---

# Reviewing Cybernetic Control Structures

## Overview

Review whether the AI control structure is coherent enough to execute.

Inputs:

- clarification brief
- goal contract
- execution policy / plan

Output:

```text
docs/superpowers/control-reviews/YYYY-MM-DD-<slug>.md
```

Use `assets/control-review-template.md`.

This skill does not implement code and does not start `/goal`.

## Review Dimensions

### 1. Requirement Traceability

Every confirmed human decision in the clarification brief must appear in the goal and execution policy.

### 2. Goal Fidelity

The goal must not add, remove, downscope, or reinterpret product semantics.

### 3. Control Law Quality

The execution policy must define a sane control law:

- dependency matrix
- batch cadence
- phase gates
- repair policy
- stop conditions

### 4. Sensor Governance

Tests are sensors, not objectives.

Flag plans that:

- overfit old tests;
- require every micro-step to pass;
- lack stale test retirement rules;
- lack product-level verification.

### 5. Batch Rhythm

Flag:

- excessively tiny steps;
- huge unobservable batches;
- no batch-end openability requirement;
- no destructive intermediate-state policy.

### 6. Semantic vs Tactical Boundary

Semantic invariants must be frozen. Tactical implementation details must remain adjustable.

### 7. Runtime Suitability

The runtime `/goal` must be able to execute the approved artifacts without calling new skills or inventing new control structures.

## Deterministic Lint

If scripts are available, run:

```bash
python3 .agents/skills/reviewing-cybernetic-control-structures/scripts/control_artifact_lint.py \
  --clarification [CLARIFICATION] \
  --goal [GOAL] \
  --plan [PLAN]
```

Use the lint output as a structural sensor. Do not treat lint as semantic approval.

## Output Status

The review must be either:

- `Needs Revision`
- `Approved`

Only mark `Approved` when:

- clarification, goal, and plan are consistent;
- no unresolved semantic decision remains;
- execution policy does not self-authorize uncontrolled changes;
- test/sensor governance is explicit;
- runtime `/goal` can execute without writing or approving a new plan.

## Validation Checklist

- [ ] The review file was created.
- [ ] Review status is explicit.
- [ ] Critical findings distinguish semantic, goal, plan, sensor, and runtime issues.
- [ ] Required revisions are actionable.
- [ ] The review did not execute implementation.
- [ ] The review did not output final runtime `/goal`.
