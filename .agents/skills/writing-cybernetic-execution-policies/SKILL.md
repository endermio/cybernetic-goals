---
name: writing-cybernetic-execution-policies
description: 'Use when requirements, any required design, and goal.control.json exist before executable /goal work, and the task needs a bounded execution policy, phase checks, evidence handling, work assignment, batch rhythm, or stop conditions.'
---

# Writing Cybernetic Execution Policies

## Overview

Create the execution execution rule for controlled work.

This skill converts:

- requirements control JSON
- solution design, when required design is required or a design exists
- goal control JSON

into:

- candidate execution policy

The plan is not approved until `$reviewing-cybernetic-control-structures` marks it Approved.

Use `assets/execution-policy-template.md`.

## What This Skill Owns

This skill does not analyze requirements, does not write goal control JSON, does not review its own policy, and does not execute target work.

## Required Input

Use completed `requirements.control.json` and `goal.control.json`, plus `design.control.json` when required design was required or a design artifact exists.

Official persistent control facts are JSON only. Historical Markdown may be read as non-authoritative background, but do not create or compile Markdown as official guard, compiler, runtime, or long-term dual-path control input.

For Level 3 lean pre-goal, Level 4, or full pre-goal work, do not create an execution policy unless the requirements analysis contains `What the User Approved: Approved`, or the current user message explicitly approves the compact control commitment. Level 1/2 bounded work does not require What the User Approved unless the requirements analysis records it as required.

In lean pre-goal, the execution policy may be a generation strategy rather than
a frozen whole-run plan. It must state which parts are hard anchors and which
parts may be revised by reviewed amendment during goal execution.

If the current user message approves the compact control commitment, update the requirements analysis `What the User Approved` section first, quoting or referencing that approval, then continue. Do not rely on in-memory approval to pass orchestration or runtime guards.

## Required Infrastructure

Follow `$cybernetic-superpowers-infrastructure`.

This skill does not replace `$superpowers:writing-plans`.

For non-trivial execution policies, invoke `$superpowers:writing-plans` or load and follow its `SKILL.md` instructions as the required planning workflow. Merely mentioning the skill, citing it, or imitating generic planning is not sufficient.

This skill supplies the cybernetic constraints that the planning workflow must preserve:

- confirmed meaning rules that cannot change;
- solution-design rules that cannot change and interfaces/contracts;
- tactical degrees of freedom;
- dependency matrix requirement;
- who does the work / context use;
- work coverage and action limits matrix for separating work covered in this run from what the agent may do limits;
- where the result must show up for intended-result place coverage and residual reconciliation;
- action that can make it done for satisfying the what counts as done;
- work size and evidence check budget;
- batch cadence;
- destructive intermediate-state policy;
- output material/evidence collection for the final output contract;
- purpose feedback strategy for judging purpose realization without evidence check convenience bias;
- evidence lifecycle / evidence budget for evidence check output retention;
- evidence check/evidence governance;
- stale evidence check retirement and rewrite policy.

If `$superpowers:writing-plans` is unavailable for a non-trivial execution policy, stop and report that required planning infrastructure is missing. Do not self-substitute with an unreviewed internal policy.

Blocked responses must still include a response-only next step. For missing planning workflow, the next step is to load/use `$superpowers:writing-plans` or return the blocked status to `$orchestrating-cybernetic-pregoal` when orchestration owns the chain.

## Required Sections

The execution policy must include:

1. Source Contracts
2. Superpowers Planning Workflow
3. Rules That Cannot Change
4. Tactical Degrees of Freedom
5. Dependency Matrix
6. Who Does The Work / Context Use
7. Work Coverage And Action Limits Matrix
8. Where The Result Must Show Up
9. Steps That Make The Result True
10. Required Step To Producing Action Alignment
11. Action That Can Make It Done
12. Work Size And Evidence Check Budget
13. Batch Cadence
14. Destructive Intermediate-State Policy
15. Output Material / Evidence Collection
16. User Purpose Strategy
17. Evidence Lifecycle / Evidence Budget
18. Evidence check / Evidence Governance
19. Stale Evidence check Retirement and Rewrite Policy
20. Phase Checks
21. Execution Rhythm
22. Stop Conditions
23. Progress Log Rules
24. Candidate Plan Tasks

## Who Does The Work / Context Use

The execution policy must choose one approved work assignment:

- `Main-only`
- `Serial subagent-driven`
- `Parallel subagent-driven`

The execution policy must record `Task level`, `Selected agent workflow`, `Subagent execution mode`, and `Max concurrent subagents` next to the who does the work.

Use `.agents/skills/references/delegation-workflow-registry.json` as the source of workflow capability limits.

Allowed `Selected agent workflow` values:

- `bounded-protocol`
- `superpowers-subagent-driven-development`
- `superpowers-dispatching-parallel-agents`
- `adapter-specific`
- `none`

Default work assignment rules:

- Level 0/1: use `Main-only`.
- Level 2: use `Main-only` unless the work is a wide inspection, audit, or verification pass; then use `Serial subagent-driven`.
- Level 3: use `Serial subagent-driven` by default unless `Main-only` has an explicit context-load justification.
- Level 4: use `Serial subagent-driven` by default. Use `Parallel subagent-driven` only when human approval, dependency-matrix independence, and control-review approval are explicitly `yes` or `approved`.

Subagent execution modes:

- `none`: selected only for `Main-only`.
- `serial-single-active`: selected for `Serial subagent-driven`; `Max concurrent subagents` must be `1`.
- `parallel-max-safe`: selected for `Parallel subagent-driven`; `Max concurrent subagents` must be `auto` or an explicit cap.

Workflow capability matrix:

| Selected agent workflow | Allowed work assignment | Allowed mode |
|---|---|---|
| `superpowers-subagent-driven-development` | `Serial subagent-driven` | `serial-single-active` |
| `superpowers-dispatching-parallel-agents` | `Parallel subagent-driven` | `parallel-max-safe` |
| `bounded-protocol` | `Serial subagent-driven / Parallel subagent-driven` | `serial-single-active / parallel-max-safe` |
| `adapter-specific` | `Serial subagent-driven / Parallel subagent-driven` | `serial-single-active / parallel-max-safe` |
| `none` | `Main-only` | `none` |

When What the User Approved records `Agent delegation preference: max-safe-parallel`, preserve that preference as the runtime work assignment target. Do not silently downgrade to `Serial subagent-driven` unless the dependency matrix has no independent frontier, shared places cannot be safely locked, subagent context packs cannot be bounded, or review rejects parallelism. If safe frontier is effectively one, record the reason in `Concurrency selection rationale`.

When What the User Approved records `Agent workflow preference`, preserve that workflow unless it conflicts with the approved work assignment/mode capability matrix. If the requested workflow is incompatible, return to What the User Approved for conflict resolution or record a concrete `Agent workflow compatibility rationale`; do not silently substitute a different workflow.

If What the User Approved records both `Agent delegation preference: max-safe-parallel` and `Agent workflow preference: superpowers-subagent-driven-development`, treat this as a approved target conflict. `$superpowers:subagent-driven-development` is serial-single-active only. Use `superpowers-dispatching-parallel-agents`, `bounded-protocol`, or `adapter-specific` for max-safe parallel execution.

For every delecheckd work package, define:

- Work package
- Executor
- Context pack
- Allowed actions
- Return format
- Integration check
- Context Pack Requirements:
  - Relevant control excerpts
  - Current batch objective
  - Allowed artifacts/places
  - Forbidden changes
  - Required evidence checks/evidence
  - Stop conditions
  - Expected return format

The main agent owns approved approved files, current batch state, dispatch, integration, progress log, and stop-condition detection.

A subagent owns one bounded work package, bounded investigation, or bounded verification pass. A subagent must not change approved files, widen scope, replace the work assignment, or bypass integration checks.

For serial or parallel subagent-driven work assignment, `Selected agent workflow` must be `bounded-protocol`, `superpowers-subagent-driven-development`, `superpowers-dispatching-parallel-agents`, or `adapter-specific`; it must not be `none`. Record the matching approved bounded subagent delegation protocol under `Subagent workflow`. Do not treat `$superpowers:subagent-driven-development` as the generic agent workflow. Use it only with `Serial subagent-driven`, `serial-single-active`, and `Max concurrent subagents: 1`. Use `$superpowers:dispatching-parallel-agents` only with `Parallel subagent-driven`, `parallel-max-safe`, and the approved wave/lock/barrier/integration structure.

For serial subagent-driven work assignment, record `Ordered work package sequence` and `Integration check after each package`.

For parallel subagent-driven work assignment, record `Concurrency frontier rule`, `Conflict / lock model`, `Parallel wave matrix`, `Failure policy`, and `Main-agent integration rule`. The `Parallel wave matrix` must include a `Required-step frontier` column so parallel waves are based on currently available required steps, not only component work package independence.

For `Main-only` Level 3/4 work, include a meaningful `Main-only context-load justification` explaining why the main agent will not become an overloaded coordinator, worker, integrator, and verifier.

At each batch limit, the progress log must compress active context: current control summary, completed work packages, integrated subagent outputs, evidence produced, deferred evidence checks, unresolved blockers, policy deviations, and next allowed action.

## Work Coverage And Action Limits Matrix

For full-route or multi-batch work, the execution policy must account for every approved horizon item and classify runtime handling as execute, prepare-only, observe-only, forbidden-not-executed, or explicitly out-of-scope by what the user approved.

What the agent may do limits must not move approved horizon items to future roadmap, handoff, later goal, or out-of-scope status. If the approved horizon is too broad, return to requirements/What the User Approved revision.

## Where The Result Must Show Up

Compiled runtime execution policies must always include this section.

If the task changes or realizes a intended result across controlled-object places, define:

### Places The Result Appears

- Place
- Role in result claim
- Required action
- Verification / reconciliation

### Place Classes

- Must act
- Must inspect
- Must preserve
- Explicitly out of scope
- Unknown or requires discovery

### Residual Reconciliation

- old-state residuals;
- unhandled places;
- unexplained differences;
- preserved or excluded places and rationale;
- places requiring later observation;
- allowed result claim wording for adequate, partial, missing, unavailable, or not applicable with justification.

If result placement is not applicable, include a compact entry that records:

- Result placement status: `not applicable with justification`;
- Why no intended-result result placement is required;
- Why no place discovery / residual reconciliation is needed;
- Allowed result claim wording.

Domain adapters own concrete place discovery and verification methods. The core policy owns place/action/residual/reconciliation structure.

## Steps That Make The Result True

For implementation work, decompose by the actor-centered state transitions that make the what counts as done true before decomposing by components, modules, files, or teams.

The execution policy must define:

- Required step: stable node id such as `S1`;
- Required state transition: the state change this node produces;
- Required evidence: evidence that the transition is satisfied.

Every mainline work package must map to at least one required step. Supporting-only work may exist, but it must be marked `supporting-only` and cannot satisfy goal progress by itself.

## Required Step To Producing Action Alignment

For every required step that supports a blocking required outcome, the execution policy must align:

```text
required step -> what would make it true -> planned producing action -> mainline work package -> evidence after action
```

The plan must record, in plain task language:

- what would make the required step true;
- the current known or unknown state;
- the planned producing action that can change the state;
- why that action can make the required step true;
- the write/run authority needed for that action;
- evidence expected after the action;
- what would prove the step cannot be produced in the approved environment.

A producing action is an action that can create the required state or evidence, not merely check whether it already exists. Inspection, summarization, old-result comparison, available-mode lookup, and check-only work are supporting-only unless the user-approved goal is explicitly an audit of existing evidence.

Missing existing capability is not proof of impossibility. If a required step needs a capability that is absent, the plan must either include a producing action to build or enable that capability, or return to design/What the User Approved because the approved authority forbids producing it. Do not turn "not already available" into runtime `blocked`.

Every mainline work package must bind to at least one planned producing action and state the result-producing change it will make. Verification-only or discovery-only work packages may precede a producing action, but they must be marked `supporting-only` and `Counts as goal progress: false` unless the approved task is only verification/discovery.

Each `Candidate Plan Task` must record `Required step(s)`, `Role`, `State transition advanced`, `Transition evidence produced`, `Integration check`, `Counts as goal progress`, `Why this is not merely component completion`, and `Why this is not merely checking whether the step already exists`.

## Action That Can Make It Done

The execution policy must define:

- Action that can make it done: the action, probe, experiment, change, or observation that must be attempted to satisfy the what counts as done;
- Proof of impossibility, if any: what would prove the action that can make it done cannot be attempted in this environment;
- If it is not done, what should be reported: a not done report may be produced only after the action that can make it done is attempted and fails, or after impossibility is proven.

For generating tasks, the action that can make it done must include producing actions that create missing required capability or evidence when those are needed. Do not replace the action with a check that only determines whether existing artifacts already satisfy the goal.

## Work Size And Evidence Check Budget

The execution policy must choose the largest coherent batch that remains diagnosable.

Each batch must represent a coherent intended-result slice, not a mechanical micro-step. Do not split work merely so every tiny edit is separately openable.

For each batch, define:

- the coherent intended-result slice;
- why this is one batch;
- which too-small split was avoided;
- what intermediate breakage is allowed inside the batch;
- what batch-end state is openable or meaningfully verifiable;
- the smallest necessary evidence check set for that batch;
- which broad checks are deferred to integration or final checks.

Evidence check budget rules:

- use the smallest evidence check set that can detect meaning or structural drift;
- do not run expensive broad checks at every batch unless they are the only reliable drift evidence check;
- treat broad verification as integration-check or completion-check work by default;
- weak or stale evidence checks must not block approved structural change without evidence check-governance review;
- if many evidence checks encode old meaning, preserve the intended result and record stale-evidence check retirement or rewrite.

## Batch Cadence

For large structural changes:

- intermediate steps inside a batch may temporarily break local observability or artifact consistency;
- each batch must end in an openable or meaningfully verifiable state;
- batch size should be large enough to avoid evidence check-driven local minima;
- batch size should be small enough that failures remain diagnosable;
- if a batch cannot be verified meaningfully, merge it with the next batch or redefine the check;
- if a batch is too large to diagnose failures, split by dependency limit or evidence check limit.

## Output Material / Evidence Collection

When the goal `Final Output Contract` or design `Output Contract Design` requires structured output, the execution policy must define:

- what output material must be collected;
- which batch produces each required material;
- where evidence references are stored;
- what must be ready before final output generation;
- what missing output material blocks completion.

Do not leave final output material discovery until the end of runtime execution.

## User Purpose Strategy

The execution policy must explain how runtime will observe or honestly bound
purpose realization.

Define:

- Internal feedback: supports progress and diagnosis, not purpose achievement unless justified;
- Integration feedback: shows cross-component or cross-artifact behavior;
- User-purpose feedback: the smallest feedback that observes the purpose-realizing outcome;
- Operational feedback: deployment/runtime/external observer evidence when relevant;
- Feedback cadence: per-batch, integration-check, final, and deferred feedback;
- Evidence unavailable handling: verified, not yet observed, smallest next observation, and Allowed completion wording.

Do not require heavy purpose-limit feedback at every batch by default. Do
not claim purpose achievement from internal feedback alone unless the approved
goal says internal evidence is sufficient because the human purpose is
internal-state correctness.

## Evidence Lifecycle / Evidence Budget

The execution policy must prevent evidence artifacts from outgrowing the controlled work.

For each evidence channel, define:

- Evidence channel
- Raw allowed?
- Baseline policy
- Per-batch retention
- Delta required?
- Summary required?
- Max tracked size
- Git policy
- Raw pointer

Evidence lifecycle rules:

- keep at most one full baseline and one final full scan unless explicitly justified;
- intermediate scans should store summary + delta, not repeated full raw hits;
- full raw evidence check output belongs in local cache, ignored artifacts, compressed retained-full artifacts, or external artifact storage unless the goal explicitly requires tracked raw output;
- tracked evidence must be reviewable without reading all raw evidence check output;
- repeated full snapshots of the same evidence check are forbidden unless the policy explains why delta is impossible;
- each batch must record evidence summary, delta, top offenders or representative samples, and raw pointer when raw output exists;
- evidence artifacts must not exceed the approved evidence budget without stopping or revising the execution policy.

## Evidence check / Evidence Governance

Approved evidence checks, checks, and evidence channels are evidence checks, not objectives.

Classify evidence checks as:

- strong evidence checks: preserve;
- weak or stale evidence checks: inspect before obeying;
- obsolete evidence checks: may be retired and rewritten.

If many evidence checks conflict with confirmed requirement meaning, preserve the intended result first, then rewrite the affected evidence channels.

Do not let brittle old evidence checks define the intended result.

## Design Limit

If a solution design exists or required design was required, the execution policy must reference the design under `Source Contracts`.

The policy may choose tactical execution details, batch cadence, and workstream organization. It must not redesign:

- controlled objects, actors, roles, or relationships;
- information/state/evidence flow;
- interfaces/contracts;
- lifecycle or failure model;
- design rules that cannot change.

If the design records how this should be answered, decompose work against that approved answer path. Do not replace the design answer path with a component-first or weaker validation answer path.

If the design is missing, contradictory, or insufficient for planning, stop and route back to `$designing-cybernetic-solutions` or ask for the smallest design decision.

## Response-Only Handoff Rule

For Level 3 lean pre-goal, Level 4, or full pre-goal work, hand off back to `$orchestrating-cybernetic-pregoal` after creating the candidate execution policy when it is available or already owns the chain.

Recommend `$reviewing-cybernetic-control-structures` directly only when the user explicitly chose a manual pre-goal chain or `$orchestrating-cybernetic-pregoal` is unavailable.

## Output Format

The response format below is response-only. Do not write `$skill ...` commands, runtime `/goal` prompts, or conversational next-step prompts into the execution policy artifact.

Create:

```text
docs/cybernetics/runs/<slug>/plan.control.json
```

Then respond:

```markdown
Created candidate execution policy:

`docs/cybernetics/runs/YYYY-MM-DD-slug/plan.control.json`

Control-law summary:
- Planning workflow: ...
- Meaning rules that cannot change: ...
- Design source: ...
- Batch cadence: ...
- Work assignment: ...
- Evidence check budget: ...
- User purpose evidence: ...
- Evidence lifecycle: ...
- Evidence check governance: ...
- Phase checks: ...

Response-only handoff:
- For Level 3/4 or full pre-goal work: return to `$orchestrating-cybernetic-pregoal` with this execution policy path.
- For an explicit manual chain only: use `$reviewing-cybernetic-control-structures` before runtime `/goal`.
```

If blocked:

```markdown
Execution policy blocked.

Reason:
- ...

Smallest input or dependency needed:
- ...

Response-only next step:
- If required planning workflow is missing: load/use `$superpowers:writing-plans`, or return blocked status to `$orchestrating-cybernetic-pregoal`.
- If the solution design is missing or insufficient: return to `$designing-cybernetic-solutions` for an explicit manual chain, or return blocked status to `$orchestrating-cybernetic-pregoal` for Level 3/4 or full pre-goal work.
- Do not run review or runtime `/goal` until a candidate execution policy exists.
```

## Validation Checklist

- [ ] Non-trivial execution policies invoke `$superpowers:writing-plans` or load and follow its `SKILL.md` instructions, otherwise stop/report missing infrastructure.
- [ ] For Level 3/4 or full pre-goal work, What the User Approved is Approved before execution-policy writing starts.
- [ ] The plan records planning workflow status.
- [ ] The plan does not self-substitute for a missing required planning workflow.
- [ ] If blocked, the assistant response includes a response-only next step.
- [ ] The plan distinguishes meaning rules that cannot change from tactical degrees of freedom.
- [ ] If required design is required, the plan references the solution design.
- [ ] The plan does not invent or revise the solution model.
- [ ] The plan has dependency matrix.
- [ ] The plan includes Who Does The Work / Context Use.
- [ ] The plan includes Where The Result Must Show Up for compiled runtime goals, with either full place/action/residual structure or `result placement not applicable with justification`.
- [ ] The plan includes Work Coverage And Action Limits Matrix for full-route or multi-batch work.
- [ ] The plan includes Steps That Make The Result True.
- [ ] Every blocking required step has required step -> producing action -> mainline work package alignment.
- [ ] Mainline work packages state what result-producing change they make, not only what existing material they inspect.
- [ ] Check-only, summarize-only, old-result comparison, and discovery work is supporting-only unless the approved task is explicitly an audit/discovery task.
- [ ] Missing existing capability is handled by a producing action, return to design/What the User Approved for authority repair, or proof of impossibility; it is not treated as runtime blocked by default.
- [ ] Each Candidate Plan Task records `Required step(s)`, `Role`, `State transition advanced`, `Transition evidence produced`, `Integration check`, `Counts as goal progress`, why it is not merely component completion, and why it is not merely checking whether the step already exists.
- [ ] The plan includes Action That Can Make It Done.
- [ ] The plan selects `Main-only`, `Serial subagent-driven`, or `Parallel subagent-driven`.
- [ ] The plan records `Selected agent workflow`.
- [ ] The plan records `Subagent execution mode` and `Max concurrent subagents`.
- [ ] Level 3/4 main-only execution has an explicit context-load justification.
- [ ] Delecheckd work packages define Context pack, Return format, and Integration check.
- [ ] Delecheckd work packages define Context Pack Requirements with relevant control excerpts, batch objective, allowed artifacts/places, forbidden changes, required evidence checks/evidence, stop conditions, and expected return format.
- [ ] The plan defines a Context Compression Rule for batch limits.
- [ ] Serial or parallel subagent-driven work assignment records an approved bounded subagent agent workflow.
- [ ] Serial or parallel subagent-driven work assignment does not use `Selected agent workflow: none`.
- [ ] Serial subagent-driven work assignment uses `serial-single-active`, max concurrency `1`, ordered sequence, and per-package integration.
- [ ] Parallel subagent-driven work assignment uses `parallel-max-safe`, wave matrix, lock model, failure policy, and integration barriers.
- [ ] Parallel wave matrix records `Required-step frontier`.
- [ ] `$superpowers:subagent-driven-development` is used only with `serial-single-active` and max concurrency `1`.
- [ ] `$superpowers:dispatching-parallel-agents` is used only with `parallel-max-safe` and approved wave/lock/barrier/integration rules.
- [ ] Parallel subagent-driven execution records human approval, dependency independence, and review approval as explicitly `yes` or `approved`.
- [ ] The plan includes Work Size And Evidence Check Budget.
- [ ] Batches are coherent intended-result slices, not mechanical micro-steps.
- [ ] The plan chooses the largest coherent batch that remains diagnosable.
- [ ] The plan has batch cadence.
- [ ] The plan allows destructive intermediate states only within approved batches.
- [ ] Each batch ends in an openable/verifiable state.
- [ ] Broad verification is assigned to integration/final checks unless justified per batch.
- [ ] The plan defines output material/evidence collection when the final output contract requires structured output.
- [ ] The plan includes User Purpose Strategy.
- [ ] The plan keeps result placement intended-result claims distinct from user-purpose evidence human-purpose claims.
- [ ] User-purpose feedback is the smallest sufficient feedback for the human purpose, not heavy end-to-end evidence by default.
- [ ] Internal feedback is not treated as purpose achievement unless the human purpose is internal-state correctness.
- [ ] The plan includes Evidence Lifecycle / Evidence Budget.
- [ ] Repeated full raw evidence snapshots are forbidden unless explicitly justified.
- [ ] Intermediate evidence check output defaults to summary + delta with raw pointer when raw exists.
- [ ] Tracked evidence remains reviewable.
- [ ] The plan treats approved evidence checks, checks, and evidence channels as evidence checks, not objectives.
- [ ] The plan includes stale evidence check retirement/rewrite policy.
- [ ] The plan does not claim to be approved.
- [ ] The skill does not execute target work.
