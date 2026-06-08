---
name: writing-cybernetic-execution-policies
description: 'Use when requirements, any required design, and a goal contract exist before executable /goal work, and the task needs a bounded execution policy, phase gates, evidence handling, topology, batch rhythm, or stop conditions.'
---

# Writing Cybernetic Execution Policies

## Overview

Create the execution control law for controlled work.

This skill converts:

- requirements analysis brief
- solution design, when Design Gate is required or a design exists
- control contract

into:

- candidate execution policy

The plan is not approved until `$reviewing-cybernetic-control-structures` marks it Approved.

Use `assets/execution-policy-template.md`.

## Core Boundary

This skill does not analyze requirements, does not write the control contract, does not review its own policy, and does not execute target work.

## Required Input

Use a completed requirements analysis brief and a goal contract, plus solution design when Design Gate was required or a design artifact exists.

For Level 3, Level 4, or full pre-goal work, do not create an execution policy unless the requirements analysis contains `Human Setpoint Approval: Approved`, or the current user message explicitly approves the compact control commitment. Level 1/2 bounded work does not require Human Setpoint Approval unless the requirements analysis records it as required.

If the current user message approves the compact control commitment, update the requirements analysis `Human Setpoint Approval` section first, quoting or referencing that approval, then continue. Do not rely on in-memory approval to pass orchestration or runtime guards.

## Required Infrastructure

Follow `$cybernetic-superpowers-infrastructure`.

This skill does not replace `$superpowers:writing-plans`.

For non-trivial execution policies, invoke `$superpowers:writing-plans` or load and follow its `SKILL.md` instructions as the required planning substrate. Merely mentioning the skill, citing it, or imitating generic planning is not sufficient.

This skill supplies the cybernetic constraints that the planning substrate must preserve:

- confirmed semantic invariants;
- solution-design invariants and interfaces/contracts;
- tactical degrees of freedom;
- dependency matrix requirement;
- context management / execution topology;
- horizon and authority coverage matrix for separating approved execution horizon from runtime authority limits;
- realization surface closure strategy for target-state surface coverage and residual reconciliation;
- target-producing action strategy for satisfying the single target-achieved predicate;
- execution granularity and sensor budget;
- batch cadence;
- destructive intermediate-state policy;
- output material/evidence collection for the final output contract;
- purpose feedback strategy for judging purpose realization without sensor convenience bias;
- evidence lifecycle / evidence budget for sensor output retention;
- sensor/evidence governance;
- stale sensor retirement and rewrite policy.

If `$superpowers:writing-plans` is unavailable for a non-trivial execution policy, stop and report that required planning infrastructure is missing. Do not self-substitute with an unreviewed internal policy.

Blocked responses must still include a response-only next step. For missing planning substrate, the next step is to load/use `$superpowers:writing-plans` or return the blocked status to `$orchestrating-cybernetic-pregoal` when orchestration owns the chain.

## Required Sections

The execution policy must include:

1. Source Contracts
2. Superpowers Planning Substrate
3. Confirmed Semantic Invariants
4. Tactical Degrees of Freedom
5. Dependency Matrix
6. Context Management / Execution Topology
7. Horizon and Authority Coverage Matrix
8. Realization Surface Closure Strategy
9. Target-Producing Spine
10. Target-Producing Action Strategy
11. Execution Granularity and Sensor Budget
12. Batch Cadence
13. Destructive Intermediate-State Policy
14. Output Material / Evidence Collection
15. Purpose Feedback Strategy
16. Evidence Lifecycle / Evidence Budget
17. Sensor / Evidence Governance
18. Stale Sensor Retirement and Rewrite Policy
19. Phase Gates
20. Execution Rhythm
21. Stop Conditions
22. Progress Log Rules
23. Candidate Plan Tasks

## Context Management / Execution Topology

The execution policy must choose one approved topology:

- `Main-only`
- `Serial subagent-driven`
- `Parallel subagent-driven`

The execution policy must record `Task level`, `Selected delegation substrate`, `Subagent execution mode`, and `Max concurrent subagents` next to the selected topology.

Allowed `Selected delegation substrate` values:

- `bounded-protocol`
- `superpowers-subagent-driven-development`
- `adapter-specific`
- `none`

Default topology rules:

- Level 0/1: use `Main-only`.
- Level 2: use `Main-only` unless the work is a wide inspection, audit, or verification pass; then use `Serial subagent-driven`.
- Level 3: use `Serial subagent-driven` by default unless `Main-only` has an explicit context-load justification.
- Level 4: use `Serial subagent-driven` by default. Use `Parallel subagent-driven` only when human approval, dependency-matrix independence, and control-review approval are explicitly `yes` or `approved`.

Subagent execution modes:

- `none`: selected only for `Main-only`.
- `serial-single-active`: selected for `Serial subagent-driven`; `Max concurrent subagents` must be `1`.
- `parallel-max-safe`: selected for `Parallel subagent-driven`; `Max concurrent subagents` must be `auto` or an explicit cap.

When Human Setpoint Approval records `Runtime delegation preference: max-safe-parallel`, preserve that preference as the runtime topology target. Do not silently downgrade to `Serial subagent-driven` unless the dependency matrix has no independent frontier, shared surfaces cannot be safely locked, subagent context packs cannot be bounded, or review rejects parallelism. If safe frontier is effectively one, record the reason in `Concurrency selection rationale`.

For every delegated work package, define:

- Work package
- Executor
- Context pack
- Allowed actions
- Return format
- Integration gate
- Context Pack Requirements:
  - Relevant control excerpts
  - Current batch objective
  - Allowed artifacts/surfaces
  - Forbidden changes
  - Required sensors/evidence
  - Stop conditions
  - Expected return format

The main agent owns approved control artifacts, current batch state, dispatch, integration, progress log, and stop-condition detection.

A subagent owns one bounded work package, bounded investigation, or bounded verification pass. A subagent must not change control artifacts, widen scope, replace the execution topology, or bypass integration gates.

For serial or parallel subagent-driven topology, `Selected delegation substrate` must be `bounded-protocol`, `superpowers-subagent-driven-development`, or `adapter-specific`; it must not be `none`. Record the matching approved bounded subagent delegation protocol under `Subagent delegation substrate`. Do not treat `$superpowers:subagent-driven-development` as the generic delegation substrate. Use it only when the work packages fit its implementation-plan, current-session workflow and `Selected delegation substrate` is `superpowers-subagent-driven-development`.

For serial subagent-driven topology, record `Ordered work package sequence` and `Integration gate after each package`.

For parallel subagent-driven topology, record `Concurrency frontier rule`, `Conflict / lock model`, `Parallel wave matrix`, `Failure policy`, and `Main-agent integration rule`.

For `Main-only` Level 3/4 work, include a meaningful `Main-only context-load justification` explaining why the main agent will not become an overloaded coordinator, worker, integrator, and verifier.

At each batch boundary, the progress log must compress active context: current control summary, completed work packages, integrated subagent outputs, evidence produced, deferred sensors, unresolved blockers, policy deviations, and next allowed action.

## Horizon and Authority Coverage Matrix

For full-route or multi-batch work, the execution policy must account for every approved horizon item and classify runtime handling as execute, prepare-only, observe-only, forbidden-not-executed, or explicitly out-of-scope by HSA.

Runtime authority limits must not move approved horizon items to future roadmap, handoff, later goal, or out-of-scope status. If the approved horizon is too broad, return to requirements/HSA revision.

## Realization Surface Closure Strategy

Compiled runtime execution policies must always include Realization Surface
Closure Strategy. When a task changes or realizes target state across
controlled-object surfaces, define the full surface/action/residual structure.
If RSC is not applicable, include a compact entry that marks `RSC not
applicable with justification`.

For the not-applicable path, record:

- RSC status: `RSC not applicable with justification`;
- Why no target-state surface closure is required;
- Why no surface discovery / residual reconciliation is needed;
- Allowed target-realization wording.

Define Surface Model:

- Surface
- Role in target realization
- Required action
- Verification / reconciliation

Define Surface Classes:

- Must act
- Must inspect
- Must preserve
- Explicitly out of scope
- Unknown or requires discovery

Define Residual Reconciliation:

- old-state residuals;
- unhandled surfaces;
- unexplained differences;
- preserved or excluded surfaces and rationale;
- surfaces requiring later observation;
- allowed target-realization wording for RSC adequate, partial, missing,
  unavailable, or not applicable with justification.

Domain adapters own concrete discovery and verification methods. The core
policy owns surface/action/residual/reconciliation structure.

## Target-Producing Spine

For target-achieving implementation work, decompose by the actor-centered state transitions that produce the target-achieved predicate before decomposing by components, modules, files, or teams.

The execution policy must define:

- Spine node: stable node id such as `S1`;
- Required state transition: the state change this node produces;
- Required evidence: evidence that the transition is satisfied.

Every mainline work package must map to at least one spine node. Supporting-only work may exist, but it must be marked `supporting-only` and cannot satisfy goal progress by itself.

## Target-Producing Action Strategy

The execution policy must define:

- Target-producing action required: the action, probe, experiment, change, or observation that must be attempted to satisfy the single target-achieved predicate;
- Proof of impossibility, if any: what would prove the target-producing action cannot be attempted in this environment;
- Non-achieved terminal report rule: a non-achieved report may be produced only after the target-producing action is attempted and fails, or after impossibility is proven.

## Execution Granularity and Sensor Budget

The execution policy must choose the largest coherent batch that remains diagnosable.

Each batch must represent a coherent target-state slice, not a mechanical micro-step. Do not split work merely so every tiny edit is separately openable.

For each batch, define:

- the coherent target-state slice;
- why this is one batch;
- which too-small split was avoided;
- what intermediate breakage is allowed inside the batch;
- what batch-end state is openable or meaningfully verifiable;
- the smallest necessary sensor set for that batch;
- which broad checks are deferred to integration or final gates.

Sensor budget rules:

- use the smallest sensor set that can detect semantic or structural drift;
- do not run expensive broad checks at every batch unless they are the only reliable drift sensor;
- treat broad verification as integration-gate or completion-gate work by default;
- weak or stale sensors must not block approved structural change without sensor-governance review;
- if many sensors encode old semantics, preserve the target state and record stale-sensor retirement or rewrite.

## Batch Cadence

For large structural changes:

- intermediate steps inside a batch may temporarily break local observability or artifact consistency;
- each batch must end in an openable or meaningfully verifiable state;
- batch size should be large enough to avoid sensor-driven local minima;
- batch size should be small enough that failures remain diagnosable;
- if a batch cannot be verified meaningfully, merge it with the next batch or redefine the gate;
- if a batch is too large to diagnose failures, split by dependency boundary or sensor boundary.

## Output Material / Evidence Collection

When the goal `Final Output Contract` or design `Output Contract Design` requires structured output, the execution policy must define:

- what output material must be collected;
- which batch produces each required material;
- where evidence references are stored;
- what must be ready before final output generation;
- what missing output material blocks completion.

Do not leave final output material discovery until the end of runtime execution.

## Purpose Feedback Strategy

The execution policy must explain how runtime will observe or honestly bound
purpose realization.

Define:

- Internal feedback: supports progress and diagnosis, not purpose achievement unless justified;
- Integration feedback: shows cross-component or cross-artifact behavior;
- Purpose-boundary feedback: the smallest feedback that observes the purpose-realizing outcome;
- Operational feedback: deployment/runtime/external observer evidence when relevant;
- Feedback cadence: per-batch, integration-gate, final, and deferred feedback;
- Evidence unavailable handling: verified, not yet observed, smallest next observation, and Allowed completion wording.

Do not require heavy purpose-boundary feedback at every batch by default. Do
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
- full raw sensor output belongs in local cache, ignored artifacts, compressed retained-full artifacts, or external artifact storage unless the goal explicitly requires tracked raw output;
- tracked evidence must be reviewable without reading all raw sensor output;
- repeated full snapshots of the same sensor are forbidden unless the policy explains why delta is impossible;
- each batch must record evidence summary, delta, top offenders or representative samples, and raw pointer when raw output exists;
- evidence artifacts must not exceed the approved evidence budget without stopping or revising the execution policy.

## Sensor / Evidence Governance

Approved sensors, checks, and evidence channels are sensors, not objectives.

Classify sensors as:

- strong sensors: preserve;
- weak or stale sensors: inspect before obeying;
- obsolete sensors: may be retired and rewritten.

If many sensors conflict with confirmed requirement semantics, preserve the target state first, then rewrite the affected evidence channels.

Do not let brittle old sensors define the target state.

## Design Boundary

If a solution design exists or Design Gate was required, the execution policy must reference the design under `Source Contracts`.

The policy may choose tactical execution details, batch cadence, and workstream organization. It must not redesign:

- controlled objects, actors, roles, or relationships;
- information/state/evidence flow;
- interfaces/contracts;
- lifecycle or failure model;
- design invariants.

If the design is missing, contradictory, or insufficient for planning, stop and route back to `$designing-cybernetic-solutions` or ask for the smallest design decision.

## Response-Only Handoff Rule

For Level 3, Level 4, or full pre-goal work, hand off back to `$orchestrating-cybernetic-pregoal` after creating the candidate execution policy when it is available or already owns the chain.

Recommend `$reviewing-cybernetic-control-structures` directly only when the user explicitly chose a manual pre-goal chain or `$orchestrating-cybernetic-pregoal` is unavailable.

## Output Format

The response format below is response-only. Do not write `$skill ...` commands, runtime `/goal` prompts, or conversational next-step prompts into the execution policy artifact.

Create:

```text
docs/cybernetics/plans/YYYY-MM-DD-<slug>.md
```

Then respond:

```markdown
Created candidate execution policy:

`docs/cybernetics/plans/YYYY-MM-DD-slug.md`

Control-law summary:
- Planning substrate: ...
- Semantic invariants: ...
- Design source: ...
- Batch cadence: ...
- Execution topology: ...
- Sensor budget: ...
- Purpose feedback: ...
- Evidence lifecycle: ...
- Sensor governance: ...
- Phase gates: ...

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
- If required planning substrate is missing: load/use `$superpowers:writing-plans`, or return blocked status to `$orchestrating-cybernetic-pregoal`.
- If the solution design is missing or insufficient: return to `$designing-cybernetic-solutions` for an explicit manual chain, or return blocked status to `$orchestrating-cybernetic-pregoal` for Level 3/4 or full pre-goal work.
- Do not run control review or runtime `/goal` until a candidate execution policy exists.
```

## Validation Checklist

- [ ] Non-trivial execution policies invoke `$superpowers:writing-plans` or load and follow its `SKILL.md` instructions, otherwise stop/report missing infrastructure.
- [ ] For Level 3/4 or full pre-goal work, Human Setpoint Approval is Approved before execution-policy writing starts.
- [ ] The plan records planning substrate status.
- [ ] The plan does not self-substitute for a missing required planning substrate.
- [ ] If blocked, the assistant response includes a response-only next step.
- [ ] The plan distinguishes semantic invariants from tactical degrees of freedom.
- [ ] If Design Gate is required, the plan references the solution design.
- [ ] The plan does not invent or revise the solution model.
- [ ] The plan has dependency matrix.
- [ ] The plan includes Context Management / Execution Topology.
- [ ] The plan includes Realization Surface Closure Strategy for compiled runtime goals, with either full surface/action/residual structure or `RSC not applicable with justification`.
- [ ] The plan includes Horizon and Authority Coverage Matrix for full-route or multi-batch work.
- [ ] The plan includes Target-Producing Spine.
- [ ] Each Candidate Plan Task maps to `Spine node(s)` or is explicitly supporting-only.
- [ ] The plan includes Target-Producing Action Strategy.
- [ ] The plan selects `Main-only`, `Serial subagent-driven`, or `Parallel subagent-driven`.
- [ ] The plan records `Selected delegation substrate`.
- [ ] The plan records `Subagent execution mode` and `Max concurrent subagents`.
- [ ] Level 3/4 main-only execution has an explicit context-load justification.
- [ ] Delegated work packages define Context pack, Return format, and Integration gate.
- [ ] Delegated work packages define Context Pack Requirements with relevant control excerpts, batch objective, allowed artifacts/surfaces, forbidden changes, required sensors/evidence, stop conditions, and expected return format.
- [ ] The plan defines a Context Compression Rule for batch boundaries.
- [ ] Serial or parallel subagent-driven topology records an approved bounded subagent delegation substrate.
- [ ] Serial or parallel subagent-driven topology does not use `Selected delegation substrate: none`.
- [ ] Serial subagent-driven topology uses `serial-single-active`, max concurrency `1`, ordered sequence, and per-package integration.
- [ ] Parallel subagent-driven topology uses `parallel-max-safe`, wave matrix, lock model, failure policy, and integration barriers.
- [ ] `$superpowers:subagent-driven-development` is used only when `Selected delegation substrate` is `superpowers-subagent-driven-development` for compatible implementation-plan, current-session work packages.
- [ ] Parallel subagent-driven execution records human approval, dependency independence, and review approval as explicitly `yes` or `approved`.
- [ ] The plan includes Execution Granularity and Sensor Budget.
- [ ] Batches are coherent target-state slices, not mechanical micro-steps.
- [ ] The plan chooses the largest coherent batch that remains diagnosable.
- [ ] The plan has batch cadence.
- [ ] The plan allows destructive intermediate states only within approved batches.
- [ ] Each batch ends in an openable/verifiable state.
- [ ] Broad verification is assigned to integration/final gates unless justified per batch.
- [ ] The plan defines output material/evidence collection when the final output contract requires structured output.
- [ ] The plan includes Purpose Feedback Strategy.
- [ ] The plan keeps RSC target-state claims distinct from PFB human-purpose claims.
- [ ] Purpose-boundary feedback is the smallest sufficient feedback for the human purpose, not heavy end-to-end evidence by default.
- [ ] Internal feedback is not treated as purpose achievement unless the human purpose is internal-state correctness.
- [ ] The plan includes Evidence Lifecycle / Evidence Budget.
- [ ] Repeated full raw evidence snapshots are forbidden unless explicitly justified.
- [ ] Intermediate sensor output defaults to summary + delta with raw pointer when raw exists.
- [ ] Tracked evidence remains reviewable.
- [ ] The plan treats approved sensors, checks, and evidence channels as sensors, not objectives.
- [ ] The plan includes stale sensor retirement/rewrite policy.
- [ ] The plan does not claim to be approved.
- [ ] The skill does not execute target work.
