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
- Human Setpoint Approval or the approved compact control commitment;
- solution design objects, relationships, flows, boundaries, interfaces/contracts, evidence model, or design invariants;
- goal success conditions;
- scope, boundaries, or invariants;
- execution policy or batch cadence;
- context management / execution topology;
- sensor or evidence structure;
- purpose feedback boundary, purpose feedback strategy, or completion-claim wording;
- realization surface closure strategy, residual reconciliation, or target-realization wording;
- execution horizon, runtime authority, forbidden-action handling, or horizon coverage matrix;
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

### 2. Human Setpoint Fidelity

For Level 3/4 or full pre-goal work, requirements analysis must contain `Human Setpoint Approval: Approved`.

Check that design, goal, and execution policy preserve the approved compact control commitment:

- human purpose;
- input role binding;
- primary object;
- requested transformation;
- non-goals;
- Purpose Feedback Boundary;
- Realization Surface Closure;
- Single target-achieved predicate;
- Target-producing evidence required;
- Non-achieved terminal report handling;
- Output Contract;
- Execution horizon;
- Runtime authority;
- Forbidden live / irreversible actions;
- Required handling for unauthorized actions;
- Explicitly out-of-scope items;
- workflow fit;
- known assumptions.

Flag as Major or Blocking when downstream artifacts reinterpret, expand, remove, or contradict the approved compact control commitment. If a downstream artifact changes the primary object, requested transformation, non-goals, PFB, RSC, target-achievement predicate, output contract, or workflow fit, require setpoint revision or explicit human reapproval before approval.

### 3. Goal Fidelity

The goal must not add, remove, downscope, or reinterpret requirement semantics.

### 4. Design Fidelity

When a solution design exists or Design Gate was required:

- the design must preserve requirements analysis semantics;
- the goal must preserve design invariants;
- the plan must preserve design objects, relationships, boundaries, flows, interfaces/contracts, lifecycle/failure model, and evidence model;
- tactical degrees of freedom must not be frozen as semantic invariants unless the design explicitly says so;
- the plan must not redesign the solution model.

### 5. Output Contract Fidelity

When requirements analysis, solution design, or goal includes an output contract:

- the requirements `Output Contract` must be preserved in the goal `Final Output Contract`;
- the design `Output Contract Design`, if present, must be preserved in the goal and execution policy;
- the execution policy must collect the material needed for the final output;
- evidence-reference, destination, machine-readable, and acceptance-condition requirements must not be weakened;
- runtime `/goal` must not be able to replace the audience, purpose, medium, structure, detail level, destination, or machine-readable shape.

### 6. Control Law Quality

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

### 7. Sensor / Evidence Governance

Approved sensors, checks, and evidence channels are sensors, not objectives.

Flag plans that:

- overfit old sensors;
- require every micro-step to pass;
- lack stale sensor retirement rules;
- lack target-state evidence.

### 8. Purpose Feedback Adequacy

Block false completion claims, not necessarily continued execution.

Classify purpose feedback as one of:

- Purpose feedback adequate
- Internally verified, purpose feedback pending
- Purpose partially observed
- Purpose feedback unavailable, honest handoff required
- Purpose-boundary evidence not required, justified

Flag as Major or Blocking when:

- evidence is used to claim purpose achieved without observing the human purpose or beneficiary/observer boundary;
- internal checks, scripts, lint, API smoke, or other convenient sensors are treated as purpose-achievement evidence without justification;
- purpose-boundary feedback is missing and the plan does not provide honest pending, partial, or unavailable status wording;
- the plan demands heavy end-to-end or operational feedback when a smaller purpose-boundary observation would suffice;
- the goal defines success as sensor success; purpose-realizing outcome evidence is required unless the purpose is internal-state correctness.

### 9. Evidence Lifecycle / Evidence Budget

Flag as Major or Blocking when:

- the execution policy stores repeated full raw sensor outputs per batch;
- raw evidence volume can exceed the controlled work size without justification;
- intermediate evidence lacks summary or delta;
- tracked evidence is not reviewable;
- no raw, pointer, summary/delta, and retained-full retention policy exists;
- evidence files are loaded as context; indexed references are the required form;
- reviewers would need to read raw evidence to approve;
- evidence artifacts are not separated into transient raw, raw pointer, reviewable summary/delta, and retained full classes;
- repeated full snapshots of the same sensor are allowed without explaining why delta is impossible.

Use `Major` when execution-policy revision can repair evidence lifecycle. Use `Blocking` when sensor output would likely swamp review, context management, or runtime completion.

### 10. Realization Surface Closure Adequacy

Classify RSC as one of:

- RSC adequate
- RSC partial
- RSC missing
- RSC unavailable
- RSC not applicable with justification

Flag as Major or Blocking when:

- local action is being treated as global target-state realization;
- the target state spans surfaces but the policy lacks a surface model;
- required actions are unclear for surfaces that carry the target state;
- old-state residuals, unknown surfaces, preserved surfaces, or excluded
  surfaces lack reconciliation;
- RSC evidence is used as human-purpose achievement evidence without PFB support;
- RSC not applicable is claimed without justification.

Use `Major` when policy or goal revision can repair RSC wording. Use
`Blocking` when runtime could claim target-state realization while important
surfaces or residuals remain unresolved.

### 11. Target Achievement Predicate Fidelity

Flag as Major or Blocking when:

- there is more than one target-achieved predicate;
- any partial, diagnostic, blocked, invalid, unavailable, fallback, or non-achieved report appears in Success Condition;
- any non-achieved report status is listed under target-achieved states;
- the execution policy lacks a target-producing action or proof-of-impossibility path;
- the plan can terminate with `goal achieved: yes` without satisfying the single target-achieved predicate;
- "valid final status" is used without separating `goal achieved: yes` from `goal achieved: no`.

### 12. Target-Producing Spine Fidelity

Flag as Major or Blocking when:

- implementation decomposes by components without a target-producing spine;
- no mainline work package owns the actor-centered path from initial state to target-achieved predicate;
- candidate tasks lack `Spine node(s)` mapping;
- supporting-only work is allowed to satisfy goal progress by itself;
- final integration path, primary use path, or spine transition evidence is deferred to future work while achieved claims remain possible;
- component, module, or substrate evidence replaces spine transition evidence;
- failed, blocked, or unobserved spine transitions are recorded only as residual risk while review remains Approved.

### 13. Execution Horizon and Authority Fidelity

Flag as Major or Blocking when:

- approved full horizon is silently reduced to the first safe segment;
- runtime authority limits are used as scope removal instead of execute / prepare-only / observe-only / forbidden-not-executed handling;
- unauthorized live or irreversible actions are moved to future roadmap, handoff, or later goal while still inside the approved horizon;
- approved horizon items lack coverage in the execution policy;
- prepare-only or forbidden-not-executed work is claimed as executed or live complete;
- the final report cannot distinguish executed, prepared-only, forbidden-not-executed, and explicitly out-of-scope by HSA.

### 14. Execution Granularity / Sensor Load

Flag as Major or Blocking when:

- batches are mechanical micro-steps; coherent target-state slices are the required form;
- every step requires full observability;
- sensor cost dominates execution cost;
- broad verification is required after every small edit;
- stale sensors can block approved structural change;
- batch-end gates are too weak to detect drift;
- batch-end gates are so heavy that they prevent progress;
- the plan does not explain why batch size is diagnosable.

Use `Major` when execution-policy revision can repair the control law. Use `Blocking` when the granularity or sensor load would prevent runtime completion or let sensors override confirmed semantics.

### 13. Context Management / Execution Topology

Flag as Major or Blocking when:

- no selected topology exists;
- Level 3/4 work assigns all target work to the main agent without a context-load justification;
- the plan creates context overload by making the main agent coordinator, worker, integrator, and verifier for context-heavy work;
- delegated work packages lack Context pack, Allowed actions, Return format, or Integration gate;
- context packs contain only artifact path lists; bounded operating context requires relevant control excerpts, current batch objective, allowed artifacts/surfaces, forbidden changes, required sensors/evidence, stop conditions, and expected return format;
- parallel subagent-driven execution lacks explicit human approval, dependency independence, or control-review approval;
- a subagent may modify control artifacts, widen scope, replace topology, or bypass integration gates;
- progress-log ownership or stop-condition detection is unclear;
- context compression or bounded return material is missing for delegated work;
- subagent outputs can be treated as final completion before main-agent integration.

Use `Major` when execution-policy revision can repair topology. Use `Blocking` when context overload would likely make runtime lose requirements, design invariants, output contract, stop conditions, or approval boundaries.

### 14. Batch Rhythm

Flag:

- excessively tiny steps;
- huge unobservable batches;
- no batch-end openability requirement;
- no destructive intermediate-state policy.

### 15. Semantic vs Tactical Boundary

Semantic invariants must be frozen. Tactical execution details must remain adjustable.

### 16. Runtime Suitability

The runtime `/goal` must be able to execute the approved artifacts without inventing new control structures. Any required runtime discipline, including approved execution topology, bounded subagent delegation protocol, and conditionally selected Superpowers substrate, must be precompiled into the approved plan, review, or final `/goal`.

Runtime completion claims must be calibrated to the highest purpose-relevant evidence actually observed. If purpose feedback is missing, runtime must report what is verified, what is not yet observed, and the smallest next observation needed. Purpose-achieved wording is reserved for observed or approved purpose feedback.

Runtime target-realization claims must also be calibrated to Realization Surface
Closure status. Do not claim target-state realization from local action alone
when Realization Surface Closure is required. Strongest positive
target-realization claims require RSC adequate.

Runtime target-achievement claims must be calibrated to the single target-achieved predicate. Non-achieved terminal reports may stop execution honestly, but they do not support `goal achieved: yes`.

### 17. Review Independence

The review must record:

- whether subagents were explicitly authorized;
- which independent review passes were completed;
- whether approval is allowed;
- why approval is blocked when independent review is missing.

### 18. Final Observer Check

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
- Human Setpoint Approval is Approved when full pre-goal orchestration is used, and Human Setpoint Fidelity has no Blocking/Major findings;
- Execution Horizon and Authority Fidelity has no Blocking/Major findings for full-route or multi-batch work;
- required design exists and is consistent with requirements analysis, goal, and plan;
- any upstream output contract is preserved in the goal and supported by the execution policy;
- no unresolved semantic decision remains;
- execution policy does not self-authorize uncontrolled changes;
- execution topology is explicit and does not create main-agent context overload;
- execution granularity and sensor load do not create micro-step overcontrol or sensor overcoupling;
- purpose feedback adequacy supports the permitted completion wording and does not confuse internal progress evidence with purpose achievement;
- realization surface closure adequacy supports target-realization wording and does not confuse local action with global realization;
- target achievement predicate fidelity preserves the single target-achieved predicate;
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
- [ ] Human Setpoint Fidelity was checked when full pre-goal orchestration is used.
- [ ] Final observer check is recorded.
- [ ] The review does not mark self-review as `Approved`.
- [ ] If subagents were not authorized and no human approval exists, status is `Needs Independent Review`.
- [ ] If any substantive artifact changed after independent review, including required design, status is `Dirty` or `Needs Re-review` until final independent re-review reports no Blocking or Major findings.
- [ ] Lint PASS is not treated as semantic/control-policy approval.
- [ ] Critical findings distinguish semantic, design, goal, plan, sensor, and runtime issues.
- [ ] Output contract fidelity was checked when any upstream output contract exists.
- [ ] Evidence lifecycle and evidence budget were checked.
- [ ] Purpose feedback adequacy was checked.
- [ ] Realization Surface Closure adequacy was checked.
- [ ] Target Achievement Predicate Fidelity was checked.
- [ ] Target-Producing Spine Fidelity was checked.
- [ ] Execution Horizon and Authority Fidelity was checked.
- [ ] Execution granularity and sensor load were checked.
- [ ] Required revisions are actionable.
- [ ] Response-only handoff matches the review status and does not bypass `$orchestrating-cybernetic-pregoal` when full pre-goal orchestration owns the chain.
- [ ] The assistant response includes a response-only next step for every review status.
- [ ] The review did not execute target work.
- [ ] The review did not output final runtime `/goal`.
