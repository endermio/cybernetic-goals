# Cybernetic Requirements Analysis: [Name]

## Requirements Analysis Status

Status: `Incomplete`

## Human Setpoint Approval

Status: `Pending`

Allowed values: `Pending / Approved / Rejected / Needs Revision / Not required`

Approval applies only to this compact control commitment.

| Element | Commitment |
|---|---|
| Human purpose | [what the human wants to change or understand] |
| Input role binding | [source material / declared state / requested transformation / method preference] |
| Primary object | [what this task is actually about] |
| Requested transformation | [what should be transformed into what] |
| Non-goals | [what must not be done] |
| Purpose Feedback Boundary | [how purpose realization will be observed or honestly reported] |
| Realization Surface Closure | [which surfaces carry target-state realization and how residuals are reconciled] |
| Single target-achieved predicate | [the only condition that allows "goal achieved: yes"] |
| Target-producing evidence required | [evidence/action/observation required for the achieved predicate] |
| Non-achieved terminal report handling | [how to report "goal achieved: no" without making it an alternate goal] |
| Target-producing path | [one actor-centered path from initial state to target-achieved predicate] |
| Answering method | [what method/evidence structure is required for this question to count as answered] |
| Not-sufficient substitute | [plausible weaker answer that must not be substituted for the approved answering method] |
| Task skeleton family | [implementation-spine / measurement-protocol / coverage-ceiling-measurement / claim-evidence-audit / diagnosis-discrimination / no special skeleton] |
| Execution horizon | [complete scope this goal covers, including items the runtime may not execute directly] |
| Runtime authority | [actions runtime may execute / prepare / observe / report] |
| Forbidden live / irreversible actions | [live, remote, destructive, irreversible, or externally risky actions runtime must not execute] |
| Required handling for unauthorized actions | [prepare-only / observe-only / forbidden-not-executed handling and required artifacts] |
| Explicitly out-of-scope items | [items excluded from this goal by HSA, not merely unauthorized] |
| Runtime delegation preference | [serial / max-safe-parallel / no preference] |
| Delegation substrate preference | [superpowers-subagent-driven-development / superpowers-dispatching-parallel-agents / bounded-protocol / adapter-specific / no preference] |
| Parallel execution authority | [approved / not approved / not applicable] |
| Parallelism cap | [auto / N / not specified] |
| Output Contract | [audience, purpose, medium, structure, destination, acceptance] |
| Workflow fit | [why full pre-goal orchestration is required / or why it is not] |
| Known assumptions | [safe defaults and assumptions] |

Approval record:

- Approved by: `[human / explicit current-message approval / not approved]`
- Approval phrase or source: `[quote or reference]`
- Approval time/context: `[optional]`

If Status is not `Approved`, downstream full pre-goal orchestration must not start.

## Human Purpose

[What the human appears to want and why it matters.]

## Current Understanding

[Concise summary of the requested capability, evaluation task, process, or artifact in task language.]

## Context Inspected

- [source artifact]
- [important existing constraint]

## Requirement Semantics

### Core Terms / Objects / Actors

| Term | Requirement meaning | Notes |
|---|---|---|
| [term] | [meaning] | [notes] |

### Confirmed Semantics

- [confirmed semantic]

### Boundaries

Inside scope:

- [included boundary]

Outside scope:

- [excluded boundary]

## Requirements Control Map

| Control element | Current analysis |
|---|---|
| Objective | [draft objective] |
| Controlled object | [target object/process/report/work artifact] |
| Candidate sensors | [checks/evidence channels/logs/reports/observations] |
| Candidate actuators | [source artifacts/tools/subsystems/procedures] |
| Constraints | [invariants/non-goals] |
| Disturbances | [ambiguities/risks/unobservables] |
| Stop conditions | [where Codex must stop] |

## Purpose Feedback Boundary

| Element | Value |
|---|---|
| Human purpose | [what the human wants to change or understand] |
| Beneficiary / observer | [who can observe whether the purpose is realized] |
| Purpose-realizing outcome | [observable change when the purpose is realized] |
| Feedback needed | [evidence that can judge purpose realization] |
| Internal sensors role | [what internal checks can and cannot prove] |
| Sufficient evidence level | `internal / integration / purpose-boundary / operational` |
| If feedback unavailable | [honest status and smallest next observation] |

## Realization Surface Closure

| Element | Value |
|---|---|
| Target state | [state or semantic change to realize] |
| Realization surfaces | [controlled-object surfaces that carry, expose, enforce, record, explain, or preserve the target state] |
| Required surface action | [act / inspect / preserve / exclude / discover] |
| Residual reconciliation | [old state, unknown surfaces, exclusions, preserved surfaces, remaining mismatches, and accounting method] |
| RSC status | `RSC adequate / RSC partial / RSC missing / RSC unavailable / RSC not applicable with justification` |
| RSC / PFB boundary | RSC is distinct from Purpose Feedback Boundary; RSC calibrates target-state and surface-closure claims, while PFB calibrates human-purpose realization claims. |

## Blocking Human Decisions

| Decision | Why it matters | Recommended default | Risk if wrong |
|---|---|---|---|
| [decision] | [reason] | [default] | [risk] |

## Default Assumptions

These are reasonable defaults and should not block progress unless the human disagrees.

- [assumption]

## Evaluation Rubric / Error Function

Use this section for audit, evaluation, readiness, closure, completeness, usability, safety, stability, coverage, correctness, or status-classification tasks.

| Rubric element | Confirmed meaning |
|---|---|
| Status meanings / pass-fail categories | [e.g. 已闭环 / 部分闭环 / 未闭环 / 不可判定] |
| Evidence levels / evidence strength | [strong vs weak evidence] |
| Minimum evidence for strongest positive status | [required evidence] |
| Downgrade rules | [partial, stale, indirect, or missing evidence handling] |
| External/unobservable dependency handling | [credentials, production-only, third-party, environment gaps] |
| Confidence / evidence grade | [whether to report confidence] |

## Output Contract

| Element | Requirement |
|---|---|
| Audience | [human / operator / reviewer / downstream agent / external stakeholder / not applicable] |
| Purpose | [decision / execution / audit / record / handoff / publication / simple response] |
| Medium | [chat / file / markdown report / JSON / table / artifact bundle / not required] |
| Required structure | [sections, tables, fields, schema, artifact bundle, or "simple summary"] |
| Detail level | [brief / standard / exhaustive] |
| Evidence references required | [yes/no] |
| Machine-readable required | [yes/no] |
| Destination path | [path or not required] |
| Acceptance condition | [what makes the output usable] |

## Required Gates

| Gate | Status | Reason |
|---|---|---|
| Semantic Gate | `required / satisfied / not applicable` | [reason] |
| Rubric Gate | `required / satisfied / not applicable` | [reason] |
| Output Contract Gate | `required / satisfied / not applicable` | [reason] |
| Design Gate | `required / satisfied / not applicable` | [reason] |
| Goal Contract Gate | `required / satisfied / not applicable` | [reason] |
| Execution Policy Gate | `required / satisfied / not applicable` | [reason] |
| Control Review Gate | `required / satisfied / not applicable` | [reason] |
| Risk Gate | `required / satisfied / not applicable` | [reason] |

## Deferred Solution Design Questions

These belong in `$designing-cybernetic-solutions`, not requirements analysis.

- [design question or "None"]

## Deferred Planning / Execution Details

These should be handled later in goal writing, execution-policy writing, or execution.

- [detail]

## Questions for Human

Ask only Level 1 questions.

1. [question]

## Proposed Defaults

If the human says “按默认继续”, proceed with:

- [default assumption]

## Confirmed Requirement Decisions

Record confirmed requirement decisions here.

- [confirmed decision]

## Non-Goals

- [excluded scope]

## Candidate Sensors / Evidence Needs

- [candidate sensor or observation]
- [evidence needed to judge requirement satisfaction]
- [external or currently unobservable evidence concern]
