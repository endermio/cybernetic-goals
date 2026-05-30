---
name: designing-cybernetic-solutions
description: 'Use after requirements analysis when the required solution model is not explicit. Creates a core cybernetic solution model: controlled objects, roles, relationships, flows, boundaries, mechanisms, interfaces/contracts, lifecycle, failure model, evidence model, output-structure model when required, design decisions, and mappings to control contract and execution policy. Does not write control contracts, execution policies, control reviews, runtime /goal commands, or execute target work.'
---

# Designing Cybernetic Solutions

## Overview

Create a solution model from confirmed requirements.

This skill resolves the `Design Gate` by turning:

```text
requirements analysis -> controllable solution model -> goal-ready design artifact
```

The design expresses the controllable structure needed for later control artifacts. It must stay in the core cybernetic vocabulary and avoid importing adapter-specific terms.

Output:

```text
docs/cybernetics/designs/YYYY-MM-DD-<slug>.md
```

Use `assets/solution-design-template.md`.

## Core Boundary

This skill must not:

- analyze unresolved requirement semantics from scratch;
- write a goal contract;
- write an execution policy;
- review the whole control structure;
- compile or start a runtime `/goal`;
- execute target work;
- force adapter-specific terms onto the core solution model.

This skill may:

- inspect the completed requirements analysis brief and relevant source artifacts;
- ask a small number of high-value design questions when solution structure cannot be safely inferred;
- create or update one solution design artifact;
- design complex output/report/schema/artifact-bundle structures when Output Contract Gate requires structure synthesis;
- record open design questions and stop before approval;
- recommend a route-appropriate response-only handoff when the design is sufficient.

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

Use `$superpowers:brainstorming` only when the design space is exploratory or the user explicitly asks for design exploration.

Do not require brainstorming for a small Design Gate where the requirements analysis or existing specs already fix the core structure. Record brainstorming substrate status in the design:

- `Not required`
- `Used`
- `Blocked`

## Design Gate

Design Gate is required when the goal is clear but the solution model is not.

Typical signals:

- multiple reasonable solution structures exist;
- controlled objects, actors, roles, or relationships are unclear;
- system/process boundaries are unclear;
- information flow, state flow, evidence flow, or decision flow is unclear;
- interfaces, contracts, procedures, or user interactions are unclear;
- a new abstraction must be introduced;
- an old concept must be replaced without letting old realization details define the requirement;
- several subsystems or roles must coordinate around one model;
- runtime execution would otherwise invent objects, boundaries, sensors, or flow.

Design Gate is usually not required for:

- small local fixes;
- existing approved design or detailed spec;
- bounded audits with an explicit rubric and report shape;
- copy/style/local bug changes;
- obvious execution paths with no new solution structure.

See `references/design-gate.md` for compact routing guidance.

## Output Contract Design

When the requirements analysis marks `Output Contract Gate: required`, inspect whether the output need is simple or requires structure synthesis.

If the requirements already define a safe simple output shape, preserve it and avoid expanding the design.

If the output requires a table, matrix, schema, evidence index, structured report, artifact bundle, multi-audience split, or machine-readable shape, the design must define:

- output audience and purpose;
- output medium and destination;
- required sections, fields, tables, schemas, or artifact bundle parts;
- evidence-reference rules;
- detail-level split;
- acceptance condition;
- how the output structure maps to goal and execution-policy implications.

Do not leave runtime execution to invent the final output shape. Do not define output shape in the response-only handoff; put the design-owned structure in the design artifact.

## Required Sections

The design artifact must include:

1. Design Status
2. Source Contracts
3. Human Purpose
4. Confirmed Semantics
5. Design Substrate
6. Conceptual Design
7. Detailed Design
8. Output Contract Design, when Output Contract Gate requires structure synthesis
9. Design-to-Goal Mapping
10. Design-to-Execution Mapping
11. Open Design Questions
12. Design Review Requirements

## Design Status

Use one of:

- `Candidate`: created by this skill and not independently reviewed or explicitly approved.
- `Reviewed`: independent design/control review was performed but the full control structure is not approved yet.
- `Approved`: explicit human approval or independent review allows this design to be treated as approved input.

Do not mark self-authored design `Approved` solely because it looks consistent.

Open design questions that affect requirement semantics, controlled relationships, interfaces/contracts, evidence model, or boundaries block `Approved`.

## Process

1. Read the completed requirements analysis brief.
2. Derive the design path from the requirements path.
3. Inspect the routing context from the user request, router output, and requirements gates.
4. Inspect only enough context to avoid generic design.
5. Identify whether `$superpowers:brainstorming` is required, used, blocked, or not required.
6. Build the conceptual model: core objects/actors/roles, relationships, flows, boundaries, alternatives, invariants.
7. Build the detailed model: mechanisms, interfaces/contracts, state/lifecycle, failure model, evidence/sensor model, compatibility/integration, decisions.
8. If Output Contract Gate requires structure synthesis, design the output structure and evidence-reference rules.
9. Separate design invariants from tactical degrees of freedom.
10. Map design elements to goal implications and execution-policy implications.
11. If material design questions remain, record them and stop without marking Approved.
12. Do not create goal, plan, review, runtime `/goal`, or target-work files.

## Response-Only Handoff Rule

Do not write handoff prompts into the design artifact.

After design is sufficient, choose the response-only handoff from routing context:

- If the task is Level 3, Level 4, full pre-goal work, or the requirements gates show `Execution Policy Gate: required` or `Control Review Gate: required`, hand off to `$orchestrating-cybernetic-pregoal`.
- If the task is Level 2 bounded work and no execution-policy or control-review gate is required, hand off to `$writing-cybernetic-goals`.
- If routing context is absent or contradictory, do not default to `$writing-cybernetic-goals`; report that the original routing decision is needed.

The design-to-goal mapping means the future goal must reference the design. It does not mean this skill should directly dispatch goal writing for full pre-goal work.

## Output Format

This output format is response-only. Do not write `$skill ...` commands, runtime `/goal` prompts, or conversational next-step prompts into the design artifact.

After creating or updating a design:

```markdown
Created or updated solution design:

`docs/cybernetics/designs/YYYY-MM-DD-slug.md`

Design summary:
- Core model: ...
- Key flows: ...
- Output contract, if designed: ...
- Boundaries: ...
- Evidence model: ...

Design status:
- Status: `Candidate`
- Open design questions: ...

Response-only handoff:
- For Level 3/4 or full pre-goal work: use `$orchestrating-cybernetic-pregoal` with the requirements analysis and this design.
- For Level 2 bounded work only: use `$writing-cybernetic-goals` with the requirements analysis and this design.
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
- [ ] The design stays within core cybernetic vocabulary unless an explicit adapter supplies additional terms.
- [ ] Conceptual design and detailed design are both present.
- [ ] Core objects/actors/roles, relationships, flows, and boundaries are explicit.
- [ ] Interfaces/contracts, lifecycle/state, failure model, and evidence/sensor model are explicit when relevant.
- [ ] Output structure, evidence-reference rules, and acceptance condition are explicit when Output Contract Gate requires structure synthesis.
- [ ] Alternatives and design decisions are recorded where there were plausible options.
- [ ] Design invariants are separated from tactical degrees of freedom.
- [ ] Design-to-goal and design-to-execution mappings are present.
- [ ] `$superpowers:brainstorming` is used only when required by exploratory design.
- [ ] The design artifact does not contain a next-step prompt.
- [ ] Level 3/4 or full pre-goal work hands off to `$orchestrating-cybernetic-pregoal`, not directly to `$writing-cybernetic-goals`.
- [ ] No goal, execution policy, control review, runtime `/goal`, or target-work artifact was created.
