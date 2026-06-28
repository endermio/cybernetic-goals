---
name: writing-cybernetic-execution-policies
description: 'Use when requirements, any required design, and goal.control.json exist before executable /goal work, and the task needs a bounded execution policy, phase checks, evidence handling, work assignment, batch rhythm, or stop conditions.'
---

# Writing Cybernetic Execution Policies

## Overview

Create the execution strategy for controlled work.

This skill consumes requirements, any required design, and `goal.control.json`.
It does not analyze requirements, design the solution, review its own policy,
compile runtime, or execute target work.

Use `assets/execution-policy-template.md`.

Detailed rules live in:

- `references/execution-policy-detailed-rules.md`
- `references/batch-cadence.md`
- `references/evidence-check-governance.md`

## Required Input

Use completed `requirements.control.json` and `goal.control.json`, plus
`design.control.json` when required design was required or a design artifact
exists.

For `controlled_run`, do not create an execution policy unless
`What the User Approved` is Approved or the current user message explicitly
approves the compact control commitment.

For `controlled_run` with requirements schema `1.1.0+`, also require
`approved_control.information_sufficiency_check` to be `satisfied` or reviewed
`not_required`, with run-local `evidence_ref` values and approved independent
`counterexample_review`. If this is absent or unfinished, route to
`RunInformationSufficiencyCheck`.

When `strategy_policy` is `reviewed_replanning`, the policy may describe a
current-generation strategy. It must separate hard anchors from strategy details
that may change by reviewed amendment.

## Required Infrastructure

Follow `$cybernetic-superpowers-infrastructure`.

For non-trivial execution policies, use `$superpowers:writing-plans` or load its
instructions. If that workflow is unavailable, stop and report the missing
planning infrastructure.

## Required Sections

The execution policy must include:

1. Source Contracts
2. Rules That Cannot Change
3. Tactical Degrees of Freedom
4. Dependency Matrix
5. Who Does The Work / Context Use
6. Work Coverage And Action Limits Matrix
7. Where The Result Must Show Up
8. Steps That Make The Result True
9. Required Step To Producing Action Alignment
10. Action That Can Make It Done
11. Work Size And Evidence Check Budget
12. Batch Cadence
13. Destructive Intermediate-State Policy
14. Output Material / Evidence Collection
15. Evidence Lifecycle / Evidence Budget
16. Stop Conditions

## Work Assignment

Choose one:

- `Main-only`
- `Serial subagent-driven`
- `Parallel subagent-driven`

Record selected agent workflow, subagent execution mode, and maximum concurrent
subagents. Use `.agents/skills/references/delegation-workflow-registry.json`
for workflow capability limits.

Default:

- `ordinary_direct_work` and `bounded_runtime`: usually `Main-only`, unless
  wide inspection/audit/verification needs serial delegation.
- `controlled_run`: use `Serial subagent-driven` unless `Main-only` has a
  context-load justification.
- Parallel execution only when human approval, dependency independence, and
  control review are explicit

## Producing Action Alignment

For each blocking required step, state:

```text
required step -> producing action -> mainline work package -> evidence after action
```

If the target requires implementation, measurement, repair, diagnosis, or
decision, do not make the mainline package only inspect, summarize, classify, or
compare existing evidence.

## Evidence And Batch Budget

Use `references/batch-cadence.md` and
`references/evidence-check-governance.md`.

Choose batches large enough to make coherent progress and small enough to be
diagnosable. Keep evidence checks proportional to work. Store summary/delta
evidence when raw evidence would dominate execution.

## Output Format

Output or update:

```text
docs/cybernetics/runs/<slug>/plan.control.json
```

Response-only summary:

```markdown
Created or updated execution policy:
`docs/cybernetics/runs/YYYY-MM-DD-slug/plan.control.json`

Status:
- `candidate` / `blocked`

Work assignment:
- ...

Mainline work packages:
- ...

Response-only next step:
- return to `$orchestrating-cybernetic-pregoal`, or
- if manual fallback is being used, run `$reviewing-cybernetic-control-structures`.
```

Do not write runtime `/goal` prompts or conversational next-step prompts into
the policy artifact.

## Validation Checklist

- [ ] Requirements, goal, and any required design are referenced.
- [ ] Controlled runs pass the information sufficiency gate before planning.
- [ ] Rules that cannot change are separated from tactics.
- [ ] Work assignment is explicit and compatible with workflow limits.
- [ ] Blocking required steps have producing actions.
- [ ] Work covered and allowed actions are not confused.
- [ ] Evidence and batch budget are explicit.
- [ ] Stop conditions are explicit.
- [ ] No target work was executed.
