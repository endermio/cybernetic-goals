---
name: writing-cybernetic-execution-policies
description: 'Use after an approved requirements analysis brief, any required solution design, and control contract exist, before starting an executable /goal. Creates a cybernetic execution policy for controlled execution: dependency matrix, execution topology, batch cadence, output material/evidence collection, sensor/evidence governance, semantic invariants, design invariants, tactical degrees of freedom, phase gates, and execution rhythm. Does not execute target work and does not start /goal execution.'
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
- execution granularity and sensor budget;
- batch cadence;
- destructive intermediate-state policy;
- output material/evidence collection for the final output contract;
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
7. Execution Granularity and Sensor Budget
8. Batch Cadence
9. Destructive Intermediate-State Policy
10. Output Material / Evidence Collection
11. Sensor / Evidence Governance
12. Stale Sensor Retirement and Rewrite Policy
13. Phase Gates
14. Execution Rhythm
15. Stop Conditions
16. Progress Log Rules
17. Candidate Plan Tasks

## Context Management / Execution Topology

The execution policy must choose one approved topology:

- `Main-only`
- `Serial subagent-driven`
- `Parallel subagent-driven`

The execution policy must record `Task level` next to the selected topology.

Default topology rules:

- Level 0/1: use `Main-only`.
- Level 2: use `Main-only` unless the work is a wide inspection, audit, or verification pass; then use `Serial subagent-driven`.
- Level 3: use `Serial subagent-driven` by default unless `Main-only` has an explicit context-load justification.
- Level 4: use `Serial subagent-driven` by default. Use `Parallel subagent-driven` only with explicit human approval, dependency-matrix independence, and control-review approval.

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

For serial or parallel subagent-driven topology, record an approved bounded subagent delegation protocol. Do not treat `$superpowers:subagent-driven-development` as the generic delegation substrate. Use it only when the work packages fit its implementation-plan, current-session workflow and the execution policy explicitly selects it.

For `Main-only` Level 3/4 work, include a meaningful `Main-only context-load justification` explaining why the main agent will not become an overloaded coordinator, worker, integrator, and verifier.

At each batch boundary, the progress log must compress active context: current control summary, completed work packages, integrated subagent outputs, evidence produced, deferred sensors, unresolved blockers, policy deviations, and next allowed action.

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
- [ ] The plan records planning substrate status.
- [ ] The plan does not self-substitute for a missing required planning substrate.
- [ ] If blocked, the assistant response includes a response-only next step.
- [ ] The plan distinguishes semantic invariants from tactical degrees of freedom.
- [ ] If Design Gate is required, the plan references the solution design.
- [ ] The plan does not invent or revise the solution model.
- [ ] The plan has dependency matrix.
- [ ] The plan includes Context Management / Execution Topology.
- [ ] The plan selects `Main-only`, `Serial subagent-driven`, or `Parallel subagent-driven`.
- [ ] Level 3/4 main-only execution has an explicit context-load justification.
- [ ] Delegated work packages define Context pack, Return format, and Integration gate.
- [ ] Delegated work packages define Context Pack Requirements with relevant control excerpts, batch objective, allowed artifacts/surfaces, forbidden changes, required sensors/evidence, stop conditions, and expected return format.
- [ ] The plan defines a Context Compression Rule for batch boundaries.
- [ ] Serial or parallel subagent-driven topology records an approved bounded subagent delegation substrate.
- [ ] `$superpowers:subagent-driven-development` is used only when explicitly selected for compatible implementation-plan, current-session work packages.
- [ ] Parallel subagent-driven execution has explicit human approval, dependency independence, and review approval.
- [ ] The plan includes Execution Granularity and Sensor Budget.
- [ ] Batches are coherent target-state slices, not mechanical micro-steps.
- [ ] The plan chooses the largest coherent batch that remains diagnosable.
- [ ] The plan has batch cadence.
- [ ] The plan allows destructive intermediate states only within approved batches.
- [ ] Each batch ends in an openable/verifiable state.
- [ ] Broad verification is assigned to integration/final gates unless justified per batch.
- [ ] The plan defines output material/evidence collection when the final output contract requires structured output.
- [ ] The plan treats approved sensors, checks, and evidence channels as sensors, not objectives.
- [ ] The plan includes stale sensor retirement/rewrite policy.
- [ ] The plan does not claim to be approved.
- [ ] The skill does not execute target work.
