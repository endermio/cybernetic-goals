---
name: writing-cybernetic-execution-policies
description: 'Use after an approved requirements analysis brief, any required solution design, and control contract exist, before starting an executable /goal. Creates a cybernetic execution policy for controlled execution: dependency matrix, batch cadence, destructive intermediate-state policy, sensor/evidence governance, semantic invariants, design invariants, tactical degrees of freedom, phase gates, and execution rhythm. Does not execute target work and does not start /goal execution.'
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
- batch cadence;
- destructive intermediate-state policy;
- sensor/evidence governance;
- stale sensor retirement and rewrite policy.

If `$superpowers:writing-plans` is unavailable for a non-trivial execution policy, stop and report that required planning infrastructure is missing. Do not self-substitute with an unreviewed internal policy.

## Required Sections

The execution policy must include:

1. Source Contracts
2. Superpowers Planning Substrate
3. Confirmed Semantic Invariants
4. Tactical Degrees of Freedom
5. Dependency Matrix
6. Batch Cadence
7. Destructive Intermediate-State Policy
8. Sensor / Evidence Governance
9. Stale Sensor Retirement and Rewrite Policy
10. Phase Gates
11. Execution Rhythm
12. Stop Conditions
13. Progress Log Rules
14. Candidate Plan Tasks

## Batch Cadence

For large structural changes:

- intermediate steps inside a batch may temporarily break local observability or artifact consistency;
- each batch must end in an openable or meaningfully verifiable state;
- batch size should be large enough to avoid sensor-driven local minima;
- batch size should be small enough that failures remain diagnosable.

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

## Output Format

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
- Sensor governance: ...
- Phase gates: ...

Next step:
Use `$reviewing-cybernetic-control-structures` before starting runtime /goal.
```

## Validation Checklist

- [ ] Non-trivial execution policies invoke `$superpowers:writing-plans` or load and follow its `SKILL.md` instructions, otherwise stop/report missing infrastructure.
- [ ] The plan records planning substrate status.
- [ ] The plan does not self-substitute for a missing required planning substrate.
- [ ] The plan distinguishes semantic invariants from tactical degrees of freedom.
- [ ] If Design Gate is required, the plan references the solution design.
- [ ] The plan does not invent or revise the solution model.
- [ ] The plan has dependency matrix.
- [ ] The plan has batch cadence.
- [ ] The plan allows destructive intermediate states only within approved batches.
- [ ] Each batch ends in an openable/verifiable state.
- [ ] The plan treats approved sensors, checks, and evidence channels as sensors, not objectives.
- [ ] The plan includes stale sensor retirement/rewrite policy.
- [ ] The plan does not claim to be approved.
- [ ] The skill does not execute target work.
