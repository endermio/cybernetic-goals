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

## Required Infrastructure

Follow `$cybernetic-superpowers-infrastructure`.

This skill requires independent review discipline before it may mark a control structure `Approved`.

Do not self-review and mark `Approved`. Do not run implementation. Do not dispatch implementer agents during pre-goal control review.

If subagents are explicitly authorized, use independent reviewer passes for the control structure. This is not the full `$superpowers:subagent-driven-development` implementation workflow; it is independent review discipline only.

If subagents are not authorized and no explicit human approval or other independent reviewer exists, produce a review marked `Needs Independent Review`. Do not mark `Approved`.

## Final Observer Rule

No `Approved` state is allowed after an unreviewed substantive artifact mutation.

A control structure may be marked `Approved` only when the last substantive change to the reviewed control artifacts, meaning the clarification, goal, or execution policy, has been followed by an independent review pass that reports no Blocking or Major findings.

If any control artifact changes after the latest independent review, the review state becomes `Dirty` / `Needs Re-review` and cannot be `Approved`.

Substantive changes to the control review's final decision, reviewer findings, approval rationale, or Final Observer Check after approval also require re-review or explicit human approval. Mechanical recording of already-reviewed findings into the review file does not itself create a new review cycle.

Deterministic-only changes may skip subagent re-review only when all of the following are true:

- the change is explicitly listed as deterministic-only;
- a deterministic guard covers the changed condition and passes;
- the control review records that no semantic or control-policy content changed.

Substantive changes include changes to:

- confirmed semantics;
- goal success conditions;
- scope, boundaries, or invariants;
- execution policy or batch cadence;
- sensor or evidence schema;
- progress log required fields;
- stop conditions;
- runtime boundary;
- approval criteria;
- artifact consistency rules;
- anything required by a prior reviewer as a Blocking or Major finding.

Deterministic-only changes include:

- heading capitalization required by lint;
- Markdown fence repair;
- path typo repair when the intended path is unambiguous;
- manifest ordering;
- whitespace.

The author of a post-review revision must not be the sole approver of that revision.

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

The runtime `/goal` must be able to execute the approved artifacts without inventing new control structures. Any required runtime Superpowers discipline must be precompiled into the approved plan, review, or final `/goal`.

### 8. Review Independence

The review must record:

- whether subagents were explicitly authorized;
- which independent review passes were completed;
- whether approval is allowed;
- why approval is blocked when independent review is missing.

### 9. Final Observer Check

The review must record whether any substantive artifact changed after the latest independent review pass and whether a final independent observer confirmed no Blocking or Major findings after that change.

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
- `Needs Independent Review`
- `Dirty`
- `Needs Re-review`
- `Approved`

Only mark `Approved` when:

- clarification, goal, and plan are consistent;
- no unresolved semantic decision remains;
- execution policy does not self-authorize uncontrolled changes;
- test/sensor governance is explicit;
- runtime `/goal` can execute without writing or approving a new plan.
- independent review discipline was satisfied or explicit human approval exists.
- no substantive artifact mutation remains unreviewed after the latest independent review.
- any deterministic-only exception is explicitly recorded and guard-covered.

## Validation Checklist

- [ ] The review file was created.
- [ ] Review status is explicit.
- [ ] Review independence is recorded.
- [ ] Final observer check is recorded.
- [ ] The review does not mark self-review as `Approved`.
- [ ] If subagents were not authorized and no human approval exists, status is `Needs Independent Review`.
- [ ] If any substantive artifact changed after independent review, status is `Dirty` or `Needs Re-review` until final independent re-review reports no Blocking or Major findings.
- [ ] Lint PASS is not treated as semantic/control-policy approval.
- [ ] Critical findings distinguish semantic, goal, plan, sensor, and runtime issues.
- [ ] Required revisions are actionable.
- [ ] The review did not execute implementation.
- [ ] The review did not output final runtime `/goal`.
