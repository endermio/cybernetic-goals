# Cybernetic Solution Design: [Name]

## Design Status

Status: `Candidate`

## Source Contracts

- Requirements analysis: `[path]`
- Rubric, if any: `[path or section]`
- Existing source-artifact context:
  - `[path]`

## Human Purpose

[What the human is trying to accomplish and why it matters.]

## Confirmed Semantics

[Requirement semantics from requirements analysis that this design must preserve.]

## Design Substrate

- Design Gate: `Required`
- `$superpowers:brainstorming` status: `Not required / Used / Blocked`
- Reason: `[why brainstorming was or was not needed]`

## Conceptual Design

### Core Objects / Actors / Roles

| Concept | Meaning | Notes |
|---|---|---|
| [concept] | [meaning] | [notes] |

### Relationships

[How objects, actors, roles, or concepts relate.]

### Information / State Flow

[How information, state, evidence, or decisions move.]

### Boundaries

Inside scope:

- [included boundary]

Outside scope:

- [excluded boundary]

### Alternative Concepts Considered

| Option | Accepted / Rejected | Rationale |
|---|---|---|
| [option] | [status] | [reason] |

### Conceptual Invariants

- [invariant]

## Task Skeleton Fidelity

Use when HSA records an answering method or task skeleton family.

| Element | Design |
|---|---|
| Approved answering method | [from HSA] |
| Approved skeleton family | [from HSA] |
| Instantiated skeleton | [design skeleton] |
| Mandatory nodes coverage | [required skeleton nodes and coverage status] |
| Forbidden substitution avoided | [yes/no + rationale; if no, stop and return to HSA revision] |

## Detailed Design

### Components / Mechanisms

| Component / Mechanism | Responsibility | Inputs | Outputs |
|---|---|---|---|
| [mechanism] | [responsibility] | [inputs] | [outputs] |

### Interfaces / Contracts

[External contracts, documents, events, forms, reports, procedures, or equivalent contracts.]

### State Model / Lifecycle

[State transitions, lifecycle, cadence, or decision progression.]

### Error / Failure / Exception Model

[How failure is surfaced, contained, retried, downgraded, or escalated.]

### Evidence / Sensor Model

[What observations prove the design works and how weak/stale/unobservable evidence is handled.]

### Output Contract Design

Use when Output Contract Gate requires structure synthesis. Otherwise record `Not required; requirements or goal can use a safe simple output contract`.

| Output element | Design |
|---|---|
| Audience | [who consumes the final output] |
| Purpose | [decision, action, audit, record, handoff, or equivalent] |
| Medium / destination | [chat, file, markdown artifact, structured data, artifact bundle, or path] |
| Required structure | [sections, tables, fields, schema, artifact bundle parts, or simple summary] |
| Detail-level split | [brief/standard/exhaustive or audience-specific split] |
| Evidence-reference rules | [what evidence references must be included and how] |
| Machine-readable shape | [required schema or not required] |
| Acceptance condition | [what makes the output usable] |

### Compatibility / Migration / Integration

[Compatibility, migration, rollout, integration, or coexistence concerns.]

### Design Decisions

| Decision | Rationale | Risk | Reversible? |
|---|---|---|---|
| [decision] | [rationale] | [risk] | [yes/no] |

## Design-to-Goal Mapping

| Design element | Goal implication |
|---|---|
| [element] | [goal implication] |
| Output Contract Design, if present | Goal must preserve the final output contract and forbid runtime substitution. |

## Design-to-Execution Mapping

| Design element | Execution-policy implication |
|---|---|
| [element] | [execution implication] |
| Output Contract Design, if present | Execution policy must collect and preserve the evidence/output material required by the output contract. |

## Open Design Questions

- [question or "None"]

## Design Review Requirements

Review must check:

- semantic fidelity to requirements analysis;
- internal consistency of objects, relationships, flows, and boundaries;
- evidence/sensor adequacy;
- output-contract adequacy when Output Contract Gate required structure synthesis;
- boundary correctness;
- design invariants versus tactical flexibility;
- suitability as source input for goal and execution policy.
