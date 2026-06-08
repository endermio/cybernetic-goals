# Cybernetic Requirements Analysis: [Name]

## Requirements Analysis Status

Status: `Incomplete`

## What the User Approved

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
| How we know the user’s purpose was met | [what observation can show the user's purpose was actually met, or what must be reported if unavailable] |
| Where the result must show up | [places, interfaces, records, behavior, docs, or outputs that must carry the result, plus old behavior to check] |
| What counts as done | [the only condition that allows "goal achieved: yes"] |
| Evidence needed to call it done | [evidence/action/observation required before claiming done] |
| report when not done handling | [how to report "goal achieved: no" without making it an alternate goal] |
| Required answer path | [one actor-centered path from initial state to done] |
| How this should be answered | [what method/evidence structure is required for this question to count as answered] |
| What is not enough | [plausible weaker answer that must not be substituted for the approved answering method] |
| Work covered in this run | [complete scope this goal covers, including items the runtime may not execute directly] |
| What the agent may do | [actions runtime may execute / prepare / observe / report] |
| Forbidden live / irreversible actions | [live, remote, destructive, irreversible, or externally risky actions runtime must not execute] |
| Required handling for unauthorized actions | [prepare-only / observe-only / forbidden-not-executed handling and required artifacts] |
| Explicitly out-of-scope items | [items excluded from this goal by What the User Approved, not merely unauthorized] |
| Agent delegation preference | [serial / max-safe-parallel / no preference] |
| Agent workflow preference | [superpowers-subagent-driven-development / superpowers-dispatching-parallel-agents / bounded-protocol / adapter-specific / no preference] |
| Parallel execution authority | [approved / not approved / not applicable] |
| Parallelism cap | [auto / N / not specified] |
| Final answer format | [audience, purpose, medium, structure, destination, acceptance] |
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

## Requirement Meaning

### Core Terms / Objects / Actors

| Term | Requirement meaning | Notes |
|---|---|---|
| [term] | [meaning] | [notes] |

### Confirmed Meaning

- [confirmed meaning]

### Inside / Outside

Inside scope:

- [included item]

Outside scope:

- [excluded item]

## Requirements Control Map

| Control element | Current analysis |
|---|---|
| Objective | [draft objective] |
| Controlled object | [target object/process/report/work artifact] |
| Candidate checks | [checks/evidence channels/logs/reports/observations] |
| Candidate actuators | [source artifacts/tools/subsystems/procedures] |
| Constraints | [rules that cannot change/non-goals] |
| Disturbances | [ambiguities/risks/unobservables] |
| Stop conditions | [where Codex must stop] |

## How We Know The User's Purpose Was Met

| Element | Value |
|---|---|
| Human purpose | [what the human wants to change or understand] |
| Beneficiary / observer | [who can observe whether the purpose is realized] |
| Purpose-realizing outcome | [observable change when the purpose is realized] |
| Feedback needed | [evidence that can judge purpose realization] |
| Internal checks role | [what internal checks can and cannot prove] |
| Sufficient evidence level | `internal / integration / user-purpose / operational` |
| If feedback unavailable | [honest status and smallest next observation] |

## Where The Result Must Show Up

| Element | Value |
|---|---|
| Intended result | [state or meaning change to realize] |
| Places the result must appear | [behavior, interface, record, report, policy, compatibility point, or other place that must carry the intended result] |
| Required action | [change / inspect / preserve / exclude / discover] |
| Old behavior check | [old state, unknown places, exclusions, preserved behavior, remaining mismatches, and accounting method] |
| Result-placement status | `adequate / partial / missing / unavailable / not applicable with justification` |
| Distinction from user-purpose evidence | result-placement is distinct from How We Know The User Purpose Was Met. Result-placement claims are about where the intended result appears; user-purpose claims are about whether the human's purpose was met. |

## Blocking Human Decisions

| Decision | Why it matters | Recommended default | Risk if wrong |
|---|---|---|---|
| [decision] | [reason] | [default] | [risk] |

## Default Assumptions

These are reasonable defaults and should not block progress unless the human disagrees.

- [assumption]

## Evaluation Rubric / Error Function

Use this section for audit, evaluation, readiness, completeness, usability, safety, stability, coverage, correctness, or status-classification tasks.

| Rubric element | Confirmed meaning |
|---|---|
| Status meanings / pass-fail categories | [e.g. 已闭环 / 部分闭环 / 未闭环 / 不可判定] |
| Evidence levels / evidence strength | [strong vs weak evidence] |
| Minimum evidence for strongest positive status | [required evidence] |
| Downgrade rules | [partial, stale, indirect, or missing evidence handling] |
| External/unobservable dependency handling | [credentials, production-only, third-party, environment gaps] |
| Confidence / evidence grade | [whether to report confidence] |

## Final Answer Format

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

## Required Checks Before Moving On

| Check | Status | Reason |
|---|---|---|
| Meaning check | `required / satisfied / not applicable` | [reason] |
| Rubric check | `required / satisfied / not applicable` | [reason] |
| Final answer format check | `required / satisfied / not applicable` | [reason] |
| Design check | `required / satisfied / not applicable` | [reason] |
| Goal check | `required / satisfied / not applicable` | [reason] |
| Execution plan check | `required / satisfied / not applicable` | [reason] |
| Review check | `required / satisfied / not applicable` | [reason] |
| Risk check | `required / satisfied / not applicable` | [reason] |

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

## Candidate Evidence checks / Evidence Needs

- [candidate evidence check or observation]
- [evidence needed to judge requirement satisfaction]
- [external or currently unobservable evidence concern]
