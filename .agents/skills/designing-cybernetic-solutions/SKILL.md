---
name: designing-cybernetic-solutions
description: 'Use after requirements analysis is complete and before goal writing when a task has a Design Gate: the target semantics are known but the solution structure is not yet explicit. Creates a general cybernetic solution design for software or non-software work: core objects/actors/roles, relationships, information or state flow, boundaries, mechanisms, interfaces/contracts, lifecycle, failure model, evidence/sensor model, design decisions, and mappings to goal and execution policy. Does not write goal contracts, execution policies, control reviews, runtime /goal commands, or implementation code.'
---

# Designing Cybernetic Solutions

## Overview

Create a solution model from confirmed requirements.

This skill resolves the `Design Gate` by turning:

```text
requirements analysis -> controllable solution model -> goal-ready design artifact
```

It is not a software-architecture-only skill. For software tasks the design may describe domain models, APIs, UI information architecture, state flow, permissions, and migration. For non-software tasks it may describe roles, procedures, audit models, research variables, evidence chains, decision points, or operating protocols.

Output:

```text
docs/cybernetics/designs/YYYY-MM-DD-<slug>.md
```

Use `assets/solution-design-template.md`.

## Core Boundary

This skill must not:

- analyze unresolved requirement semantics from scratch;
- write a goal contract;
- write an execution policy or implementation plan;
- review the whole control structure;
- compile or start a runtime `/goal`;
- implement code;
- force software-specific architecture terms onto non-software work.

This skill may:

- inspect the completed requirements analysis brief and relevant docs/code/specs;
- ask a small number of high-value design questions when solution structure cannot be safely inferred;
- create or update one solution design artifact;
- record open design questions and stop before approval;
- recommend the next goal-writing step when the design is sufficient.

## Required Input

Use a completed requirements analysis brief, usually:

```text
docs/cybernetics/requirements/YYYY-MM-DD-<slug>.md
```

The design path must use the same date/slug unless the user explicitly requests another path:

```text
docs/cybernetics/designs/YYYY-MM-DD-<slug>.md
```

If the requirements analysis is missing, incomplete, or has open blocking human decisions, stop and return to `$analyzing-cybernetic-requirements`.

## Optional Infrastructure

Use `$superpowers:brainstorming` only when the design space is exploratory, product/design-heavy, or the user explicitly asks for design exploration.

Do not require brainstorming for a small Design Gate where the requirements analysis or existing specs already fix the core structure. Record brainstorming substrate status in the design:

- `Not required`
- `Used`
- `Blocked`

## Design Gate

Design Gate is required when the goal is clear but the solution model is not.

Typical signals:

- multiple reasonable solution structures exist;
- domain objects, actors, roles, or relationships are unclear;
- system/process boundaries are unclear;
- information flow, state flow, evidence flow, or decision flow is unclear;
- interfaces, contracts, procedures, or user interactions are unclear;
- a new abstraction must be introduced;
- an old concept must be replaced without letting old implementation define the requirement;
- several subsystems or roles must coordinate around one model;
- runtime execution would otherwise invent objects, boundaries, sensors, or flow.

Design Gate is usually not required for:

- small local fixes;
- existing approved design or detailed spec;
- bounded audits with an explicit rubric and report shape;
- copy/style/local bug changes;
- obvious execution paths with no new solution structure.

See `references/design-gate.md` for compact routing guidance.

## Required Sections

The design artifact must include:

1. Design Status
2. Source Contracts
3. Human Purpose
4. Confirmed Semantics
5. Design Substrate
6. Conceptual Design
7. Detailed Design
8. Design-to-Goal Mapping
9. Design-to-Execution Mapping
10. Open Design Questions
11. Design Review Requirements
12. Next Step

## Design Status

Use one of:

- `Candidate`: created by this skill and not independently reviewed or explicitly approved.
- `Reviewed`: independent design/control review was performed but the full control structure is not approved yet.
- `Approved`: explicit human approval or independent review allows this design to be treated as approved input.

Do not mark self-authored design `Approved` solely because it looks consistent.

Open design questions that affect product semantics, domain relationships, interfaces/contracts, evidence model, or boundaries block `Approved`.

## Process

1. Read the completed requirements analysis brief.
2. Derive the design path from the requirements path.
3. Inspect only enough context to avoid generic design.
4. Identify whether `$superpowers:brainstorming` is required, used, blocked, or not required.
5. Build the conceptual model: core objects/actors/roles, relationships, flows, boundaries, alternatives, invariants.
6. Build the detailed model: mechanisms, interfaces/contracts, state/lifecycle, failure model, evidence/sensor model, compatibility/integration, decisions.
7. Separate design invariants from tactical degrees of freedom.
8. Map design elements to goal implications and execution-policy implications.
9. If material design questions remain, record them and stop without marking Approved.
10. Do not create goal, plan, review, runtime `/goal`, or implementation files.

## Output Format

After creating or updating a design:

```markdown
Created or updated solution design:

`docs/cybernetics/designs/YYYY-MM-DD-slug.md`

Design summary:
- Core model: ...
- Key flows: ...
- Boundaries: ...
- Evidence model: ...

Design status:
- Status: `Candidate`
- Open design questions: ...

Next step:
Use `$writing-cybernetic-goals` with the requirements analysis and solution design as sources of truth.
```

If blocked:

```markdown
Solution design blocked.

Reason:
- ...

Smallest input needed:
- ...

Do not write the goal contract until this design decision is resolved or the human explicitly says the Design Gate is unnecessary.
```

## Validation Checklist

- [ ] Requirements analysis is complete before design is approved.
- [ ] The design path uses the requirements analysis date/slug.
- [ ] The design is general, not software-only unless the task is software.
- [ ] Conceptual design and detailed design are both present.
- [ ] Core objects/actors/roles, relationships, flows, and boundaries are explicit.
- [ ] Interfaces/contracts, lifecycle/state, failure model, and evidence/sensor model are explicit when relevant.
- [ ] Alternatives and design decisions are recorded where there were plausible options.
- [ ] Design invariants are separated from tactical degrees of freedom.
- [ ] Design-to-goal and design-to-execution mappings are present.
- [ ] `$superpowers:brainstorming` is used only when required by exploratory design.
- [ ] No goal, execution policy, control review, runtime `/goal`, or implementation code was created.
