# Design: [Name]

## Design Status

Status: `Candidate`

## Source Contracts

- Requirements analysis: `[path]`
- Rubric, if any: `[path or section]`
- Existing source-artifact context:
  - `[path]`

## Human Purpose

[What the human is trying to accomplish and why it matters.]

## Confirmed Meaning

[Requirement meaning from requirements analysis that this design must preserve.]

## Design Workflow

- required design: `Required`
- `$superpowers:brainstorming` status: `Not required / Used / Blocked`
- Reason: `[why brainstorming was or was not needed]`

## Answer Method Check

Design must start with the required answer path. Use when What the User Approved records how the question should be answered or what is not enough.

| Element | Design |
|---|---|
| Approved answer method | [from What the User Approved] |
| Required answer path | [design answer path] |
| Required steps covered | [required answer-path steps and coverage status] |
| What is not enough avoided | [yes/no + rationale; if no, stop and return to What the User Approved revision] |

## Required Answer Path

| Required step | Required change or answer step | Required evidence | Completion condition |
|---|---|---|---|
| [S1] | [initial/intermediate state -> next state] | [evidence] | [condition] |

## What Supports Each Required Step

Design pieces exist to support required steps. Do not introduce components, actors, or mechanisms that are not mapped to a required step or marked supporting-only.

| Required step | Required support object/component/mechanism | Why needed | Evidence produced |
|---|---|---|---|
| [S1] | [object/component/mechanism] | [reason] | [evidence] |

### Relationships

[How support objects, actors, roles, or concepts relate to required steps.]

### Information / State Flow

[How information, state, evidence, or decisions move through required steps.]

### Inside / Outside This Design

Inside scope:

- [included item]

Outside scope:

- [excluded item]

### Alternative Answer Paths Or Support Models Considered

| Option | Accepted / Rejected | Rationale |
|---|---|---|
| [option] | [status] | [reason] |

### Rules That Must Not Change

- [rule]

## Design Details Tied To Required Steps

Every design detail below must either support a required step or be marked
supporting-only. Do not introduce free-floating components, agreements, state,
failure handling, evidence, compatibility work, or decisions.

### Components / Mechanisms

| Component / Mechanism | Required answer step supported | Mainline or supporting-only | Responsibility | Inputs | Outputs | Evidence produced |
|---|---|---|---|---|---|---|
| [mechanism] | [required step] | [mainline/supporting-only] | [responsibility] | [inputs] | [outputs] | [evidence] |

### Interfaces / Agreements

| Interface / agreement | Required answer step supported | Mainline or supporting-only | Why needed | Evidence produced |
|---|---|---|---|---|
| [agreement] | [required step] | [mainline/supporting-only] | [reason] | [evidence] |

### State Model / Lifecycle

| State / lifecycle item | Required answer step supported | Mainline or supporting-only | Transition or cadence | Evidence produced |
|---|---|---|---|---|
| [state item] | [required step] | [mainline/supporting-only] | [transition/cadence] | [evidence] |

### Error / Failure / Exception Model

| Failure case | Required answer step supported | Mainline or supporting-only | Handling | Evidence produced |
|---|---|---|---|---|
| [failure] | [required step] | [mainline/supporting-only] | [handling] | [evidence] |

### Evidence / Checks

| Check / evidence | Required answer step supported | Mainline or supporting-only | What it proves | Weak/stale/unobservable handling |
|---|---|---|---|---|
| [check/evidence] | [required step] | [mainline/supporting-only] | [proof] | [handling] |

### Final Answer Format Design

Use when final answer format requires structure synthesis. Otherwise record `Not required; requirements or goal can use a safe simple final answer format`.

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

| Compatibility / migration / integration item | Required answer step supported | Mainline or supporting-only | Handling | Evidence produced |
|---|---|---|---|---|
| [item] | [required step] | [mainline/supporting-only] | [handling] | [evidence] |

### Design Decisions

| Decision | Required answer step supported | Mainline or supporting-only | Rationale | Risk | Reversible? |
|---|---|---|---|---|---|
| [decision] | [required step] | [mainline/supporting-only] | [rationale] | [risk] | [yes/no] |

## Design-to-Goal Mapping

| Design element | Goal implication |
|---|---|
| [element] | [goal implication] |
| Final Answer Format Design, if present | Goal must preserve the final answer format and forbid runtime substitution. |

## Design-to-Execution Mapping

| Design element | Execution-policy implication |
|---|---|
| [element] | [execution implication] |
| Final Answer Format Design, if present | Execution policy must collect and preserve the evidence/output material required by the final answer format. |

## Open Design Questions

- [question or "None"]

## Design Review Requirements

Review must check:

- meaning match to requirements analysis;
- internal consistency of objects, relationships, flows, and inside/outside choices;
- evidence/check adequacy;
- final-answer-format adequacy when structure synthesis is required;
- inside/outside correctness;
- rules that must not change versus tactical flexibility;
- suitability as source input for goal and execution policy.
