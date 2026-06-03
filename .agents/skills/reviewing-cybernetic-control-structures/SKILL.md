---
name: reviewing-cybernetic-control-structures
description: 'Use when requirements analysis, any required design, goal contract, and execution policy exist before runtime /goal, and the cybernetic control structure needs independent approval, blocker review, or risk review.'
---

# Reviewing Cybernetic Control Structures

## Overview

Review whether the AI control structure is coherent enough to execute.

Inputs:

- requirements analysis brief
- solution design, when Design Gate is required or a design exists
- control contract
- execution policy / plan

Output:

```text
docs/cybernetics/control-reviews/YYYY-MM-DD-<slug>.md
```

Use `assets/control-review-template.md`.

This skill does not execute target work and does not start `/goal`.

## Required Infrastructure

Follow `$cybernetic-superpowers-infrastructure`.

This skill requires independent review discipline before it may mark a control structure `Approved`.

Do not self-review and mark `Approved`. Do not run target execution. Do not dispatch execution agents during pre-goal control review.

If pre-goal review subagents are explicitly authorized, use independent reviewer passes for the control structure. This is not the full `$superpowers:subagent-driven-development` execution workflow; it is independent review discipline only.

If pre-goal review subagents are not authorized and no explicit human approval or other independent reviewer exists, produce a review marked `Needs Independent Review`. Do not mark `Approved`.

## Final Observer Rule

No `Approved` state is allowed after an unreviewed substantive artifact mutation.

A control structure may be marked `Approved` only when the last substantive change to the reviewed control artifacts, meaning the requirements analysis, solution design, goal, or execution policy, has been followed by an independent review pass that reports no Blocking or Major findings.

If any control artifact changes after the latest independent review, the review state becomes `Dirty` / `Needs Re-review` and cannot be `Approved`.

Substantive changes to the control review's final decision, reviewer findings, approval rationale, or Final Observer Check after approval also require re-review or explicit human approval. Mechanical recording of already-reviewed findings into the review file does not itself create a new review cycle.

Deterministic-only changes may skip subagent re-review only when all of the following are true:

- the change is explicitly listed as deterministic-only;
- a deterministic guard covers the changed condition and passes;
- the control review records that no semantic or control-policy content changed.

Substantive changes include changes to:

- confirmed semantics;
- solution design objects, relationships, flows, boundaries, interfaces/contracts, evidence model, or design invariants;
- goal success conditions;
- scope, boundaries, or invariants;
- execution policy or batch cadence;
- context management / execution topology;
- sensor or evidence structure;
- evidence lifecycle, retention, budget, or tracked-evidence policy;
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

Every confirmed human decision in the requirements analysis brief must appear in the goal and execution policy.

### 2. Goal Fidelity

The goal must not add, remove, downscope, or reinterpret requirement semantics.

### 3. Design Fidelity

When a solution design exists or Design Gate was required:

- the design must preserve requirements analysis semantics;
- the goal must preserve design invariants;
- the plan must preserve design objects, relationships, boundaries, flows, interfaces/contracts, lifecycle/failure model, and evidence model;
- tactical degrees of freedom must not be frozen as semantic invariants unless the design explicitly says so;
- the plan must not redesign the solution model.

### 4. Output Contract Fidelity

When requirements analysis, solution design, or goal includes an output contract:

- the requirements `Output Contract` must be preserved in the goal `Final Output Contract`;
- the design `Output Contract Design`, if present, must be preserved in the goal and execution policy;
- the execution policy must collect the material needed for the final output;
- evidence-reference, destination, machine-readable, and acceptance-condition requirements must not be weakened;
- runtime `/goal` must not be able to replace the audience, purpose, medium, structure, detail level, destination, or machine-readable shape.

### 5. Control Law Quality

The execution policy must define a sane control law:

- dependency matrix
- context management / execution topology
- context budget
- execution granularity
- sensor budget
- evidence lifecycle / evidence budget
- batch cadence
- phase gates
- repair policy
- stop conditions

### 6. Sensor / Evidence Governance

Approved sensors, checks, and evidence channels are sensors, not objectives.

Flag plans that:

- overfit old sensors;
- require every micro-step to pass;
- lack stale sensor retirement rules;
- lack target-state evidence.

### 7. Evidence Lifecycle / Evidence Budget

Flag as Major or Blocking when:

- the execution policy stores repeated full raw sensor outputs per batch;
- raw evidence volume can exceed the controlled work size without justification;
- intermediate evidence lacks summary or delta;
- tracked evidence is not reviewable;
- no raw, pointer, summary/delta, and retained-full retention policy exists;
- evidence files are used as context instead of indexed references;
- reviewers would need to read raw evidence to approve;
- evidence artifacts are not separated into transient raw, raw pointer, reviewable summary/delta, and retained full classes;
- repeated full snapshots of the same sensor are allowed without explaining why delta is impossible.

Use `Major` when execution-policy revision can repair evidence lifecycle. Use `Blocking` when sensor output would likely swamp review, context management, or runtime completion.

### 8. Execution Granularity / Sensor Load

Flag as Major or Blocking when:

- batches are mechanical micro-steps rather than coherent target-state slices;
- every step requires full observability;
- sensor cost dominates execution cost;
- broad verification is required after every small edit;
- stale sensors can block approved structural change;
- batch-end gates are too weak to detect drift;
- batch-end gates are so heavy that they prevent progress;
- the plan does not explain why batch size is diagnosable.

Use `Major` when execution-policy revision can repair the control law. Use `Blocking` when the granularity or sensor load would prevent runtime completion or let sensors override confirmed semantics.

### 9. Context Management / Execution Topology

Flag as Major or Blocking when:

- no selected topology exists;
- Level 3/4 work assigns all target work to the main agent without a context-load justification;
- the plan creates context overload by making the main agent coordinator, worker, integrator, and verifier for context-heavy work;
- delegated work packages lack Context pack, Allowed actions, Return format, or Integration gate;
- context packs are only artifact path lists instead of bounded operating context with relevant control excerpts, current batch objective, allowed artifacts/surfaces, forbidden changes, required sensors/evidence, stop conditions, and expected return format;
- parallel subagent-driven execution lacks explicit human approval, dependency independence, or control-review approval;
- a subagent may modify control artifacts, widen scope, replace topology, or bypass integration gates;
- progress-log ownership or stop-condition detection is unclear;
- context compression or bounded return material is missing for delegated work;
- subagent outputs can be treated as final completion before main-agent integration.

Use `Major` when execution-policy revision can repair topology. Use `Blocking` when context overload would likely make runtime lose requirements, design invariants, output contract, stop conditions, or approval boundaries.

### 10. Batch Rhythm

Flag:

- excessively tiny steps;
- huge unobservable batches;
- no batch-end openability requirement;
- no destructive intermediate-state policy.

### 11. Semantic vs Tactical Boundary

Semantic invariants must be frozen. Tactical execution details must remain adjustable.

### 12. Runtime Suitability

The runtime `/goal` must be able to execute the approved artifacts without inventing new control structures. Any required runtime discipline, including approved execution topology, bounded subagent delegation protocol, and conditionally selected Superpowers substrate, must be precompiled into the approved plan, review, or final `/goal`.

### 13. Review Independence

The review must record:

- whether subagents were explicitly authorized;
- which independent review passes were completed;
- whether approval is allowed;
- why approval is blocked when independent review is missing.

### 14. Final Observer Check

The review must record whether any substantive artifact changed after the latest independent review pass and whether a final independent observer confirmed no Blocking or Major findings after that change.

## Deterministic Lint

If scripts are available, run:

```bash
python3 .agents/skills/reviewing-cybernetic-control-structures/scripts/control_artifact_lint.py \
  --requirements [REQUIREMENTS] \
  --design [DESIGN] \
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

- requirements analysis, required design, goal, and plan are consistent;
- required design exists and is consistent with requirements analysis, goal, and plan;
- any upstream output contract is preserved in the goal and supported by the execution policy;
- no unresolved semantic decision remains;
- execution policy does not self-authorize uncontrolled changes;
- execution topology is explicit and does not create main-agent context overload;
- execution granularity and sensor load do not create micro-step overcontrol or sensor overcoupling;
- evidence lifecycle keeps tracked evidence reviewable and prevents raw sensor output explosion;
- sensor/evidence governance is explicit;
- runtime `/goal` can execute without writing or approving a new plan.
- independent review discipline was satisfied or explicit human approval exists.
- no substantive artifact mutation remains unreviewed after the latest independent review.
- any deterministic-only exception is explicitly recorded and guard-covered.

## Response-Only Handoff Rule

Do not write handoff prompts into the review artifact.

After review status is set:

- If invoked by `$orchestrating-cybernetic-pregoal` or full pre-goal context, return the review path and status to `$orchestrating-cybernetic-pregoal`.
- If standalone/manual and status is `Approved`, hand off to `$compiling-cybernetic-runtime-goals`.
- If status is `Needs Revision`, `Dirty`, or `Needs Re-review`, revise the relevant control artifacts and rerun review; do not compile runtime `/goal`.
- If status is `Needs Independent Review`, obtain independent review or explicit human approval; do not compile runtime `/goal`.

## Output Format

This output format is response-only. Do not write `$skill ...` commands, runtime `/goal` prompts, or conversational next-step prompts into the review artifact.

```markdown
Created or updated control review:

`docs/cybernetics/control-reviews/YYYY-MM-DD-slug.md`

Review status:
- `Approved` / `Needs Revision` / `Needs Independent Review` / `Dirty` / `Needs Re-review`

Key findings:
- ...

Response-only next step:
- If full pre-goal orchestration owns the chain: return to `$orchestrating-cybernetic-pregoal` with the review path and status.
- If standalone/manual and `Approved`: run `$compiling-cybernetic-runtime-goals`.
- If `Needs Revision`, `Dirty`, or `Needs Re-review`: revise the named artifacts and rerun `$reviewing-cybernetic-control-structures`.
- If `Needs Independent Review`: obtain independent review or explicit human approval before runtime compilation.
```

## Validation Checklist

- [ ] The review file was created.
- [ ] Review status is explicit.
- [ ] Review independence is recorded.
- [ ] Final observer check is recorded.
- [ ] The review does not mark self-review as `Approved`.
- [ ] If subagents were not authorized and no human approval exists, status is `Needs Independent Review`.
- [ ] If any substantive artifact changed after independent review, including required design, status is `Dirty` or `Needs Re-review` until final independent re-review reports no Blocking or Major findings.
- [ ] Lint PASS is not treated as semantic/control-policy approval.
- [ ] Critical findings distinguish semantic, design, goal, plan, sensor, and runtime issues.
- [ ] Output contract fidelity was checked when any upstream output contract exists.
- [ ] Evidence lifecycle and evidence budget were checked.
- [ ] Execution granularity and sensor load were checked.
- [ ] Required revisions are actionable.
- [ ] Response-only handoff matches the review status and does not bypass `$orchestrating-cybernetic-pregoal` when full pre-goal orchestration owns the chain.
- [ ] The assistant response includes a response-only next step for every review status.
- [ ] The review did not execute target work.
- [ ] The review did not output final runtime `/goal`.
