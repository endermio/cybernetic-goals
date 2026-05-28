---
name: analyzing-cybernetic-requirements
description: 'Use before solution design, goal writing, execution-policy writing, or implementation for complex, ambiguous, or evaluative work. Analyzes human purpose, requirement semantics, domain objects and boundaries, evaluation rubrics/error functions, constraints, non-goals, safe defaults, blocking human decisions, and required gates. Does not create solution designs, goal contracts, execution policies, control reviews, runtime /goal commands, or implementation code. Creates a requirements analysis brief under docs/cybernetics/requirements/ when file writing is available.'
---

# Analyzing Cybernetic Requirements

## Overview

Turn a human intention into a requirements analysis brief before it becomes a solution design, Codex `/goal`, execution policy, or code change.

This skill is a pre-goal control loop:

```text
human purpose -> AI context scan -> requirement semantics -> rubric/gate analysis -> human decisions/defaults -> goal-ready requirements brief
```

Requirements analysis is broader than asking clarifying questions. Clarifying questions are one tool inside this skill. The output is not just answers to questions; it is the analyzed setpoint, constraints, evaluation function, and required gates.

Output:

- a concise requirements analysis response in chat, or
- a requirements analysis brief at `docs/cybernetics/requirements/YYYY-MM-DD-<slug>.md`.

Use `assets/requirements-analysis-template.md`.

## Core Boundary

This skill analyzes requirements. It must not:

- design the solution structure;
- define interfaces, data models, component architecture, workflows, report schemas, or state machines as a new solution model;
- write a goal contract;
- write an execution policy or implementation plan;
- review the whole control structure;
- compile or start a runtime `/goal`;
- implement code.

This skill may:

- extract human purpose;
- identify requirement objects, actors, terms, boundaries, and non-goals;
- classify success, failure, completion, closure, usability, readiness, or pass/fail semantics;
- identify constraints, invariants, assumptions, and stop conditions;
- decide whether Semantic, Rubric, Design, Goal Contract, Execution Policy, Control Review, or Risk gates are required;
- ask high-value human questions;
- record obvious defaults without blocking progress;
- recommend `$designing-cybernetic-solutions` when Design Gate is required.

Requirement object lists are not solution designs. They name what the human is talking about; they do not prescribe mechanisms, interfaces, lifecycle, state flow, or execution batches.

## Analyze Requirements, Do Not Downscope Them

Do not reduce, simplify, postpone, or replace the requested behavior merely because implementation seems complex, risky, unstable, or hard.

Implementation complexity may be recorded as execution risk, planning concern, verification concern, or future implementation challenge. It must not become the recommended product default unless the human explicitly asks for a lower-risk scope.

## Ask Only High-Value Human Questions

Ask the human a question only if all are true:

1. The answer materially changes requirement semantics, evaluation rubric, data visibility, permission model, public API semantics, user-visible behavior, or control boundaries.
2. There are at least two plausible business choices.
3. The correct answer cannot be safely inferred from the user request, existing docs, or common product conventions.
4. A wrong default would be costly to reverse or would cause serious misalignment.

Do not ask the human about routine execution tactics, obvious resilience behavior, implementation mechanics, or design details that belong in `$designing-cybernetic-solutions`.

Use `references/decision-levels.md` for decision classification.

## Evaluation Function Gate

For audit, evaluation, readiness, closure, completeness, usability, safety, stability, coverage, correctness, or status-classification tasks, treat the rubric as requirement semantics.

Evaluation predicates include terms such as:

```text
闭环, 完成, 可用, 通过, 达标, 就绪, 用户视角, 质量好, 稳定, 安全, 合理, 充分, 覆盖, 一致, 正确, 可交付, 生产可用, 验收通过
```

Do not treat these as self-explanatory. Requirements analysis must identify the error function:

- status meanings or pass/fail categories;
- evidence levels or evidence strength;
- the minimum evidence needed for the strongest positive status;
- downgrade rules for partial, weak, missing, stale, or indirect evidence;
- handling for external credentials, production-only dependencies, third-party services, or currently unobservable behavior;
- whether confidence or evidence grade must be reported.

For rubric-only analysis, ask a short set of high-value questions focused on the evaluation function. If the user asks to proceed by default, use a conservative rubric:

```text
Strongest positive status requires actual UI/API workflow evidence or a successfully run smoke/e2e/similar runtime check.
Partial status means code, page, API, docs, or unrun tests exist, but actual user-path evidence is missing.
Negative status means only placeholders/plans exist, or no usable entrypoint exists.
Unknown/unverifiable status means external credentials, production-only environment, third-party service, or current environment prevents observation.
```

## Design Gate Boundary

This skill identifies whether Design Gate is required. It does not resolve it.

Mark `Design Gate: required` when:

- multiple reasonable solution structures exist;
- domain objects, actors, roles, or relationships are not explicit enough for goal writing;
- system/process/organizational boundaries are unclear;
- information flow, state flow, evidence flow, or decision flow is unclear;
- interfaces, contracts, procedures, reports, events, or user interactions are unclear;
- a new abstraction must be introduced;
- an old concept must be replaced without letting old implementation define the requirement;
- several subsystems or roles must coordinate around one model;
- runtime execution would otherwise invent objects, boundaries, sensors, or flow.

When Design Gate is required, record the missing solution-model questions and recommend `$designing-cybernetic-solutions`. Do not answer those questions inside the requirements analysis unless they are already confirmed human semantics.

## Process

1. Inspect just enough context to avoid generic questions.
2. Restate the human purpose in task/product language.
3. Extract confirmed requirement semantics, terms, objects, boundaries, constraints, and non-goals.
4. Build a requirements control map: objective, controlled object, candidate sensors, actuators, constraints, disturbances, stop conditions.
5. If the task is evaluative, identify the rubric/error function and classify missing rubric elements as decisions.
6. Identify required gates: Semantic, Rubric, Design, Goal Contract, Execution Policy, Control Review, Risk.
7. Classify uncertainty as blocking human decision, safe default assumption, or deferred design/planning/execution detail.
8. Ask 3-7 high-value questions, preferably no more than 5.
9. Create or update the requirements analysis brief.
10. If the human answers, update `Confirmed Requirement Decisions` and `Requirements Analysis Status`.
11. Do not create a solution design, goal, plan, control review, runtime `/goal`, or implementation files.
12. If analysis is complete and the brief path deterministically identifies a date/slug, output queue-friendly next commands as described below.

## Queue-Friendly Next Commands

When requirements analysis is complete, choose the next command from the intended workflow.

For Level 3/4 or full pre-goal work, and when the requirements path is deterministic, output:

1. A solution-design command when `Design Gate: required`.
2. A pre-goal orchestration command using the concrete requirements path.
3. A predicted queue-friendly `/goal` command using the expected artifact paths for the same date/slug.

The predicted `/goal` is not the final approved runtime command. Label it as predicted or queue-friendly, and make it depend on artifacts that the pre-goal orchestrator must create and approve.

Derive expected paths from:

```text
docs/cybernetics/requirements/YYYY-MM-DD-<slug>.md
```

Use the same `YYYY-MM-DD-<slug>` for:

```text
docs/cybernetics/designs/YYYY-MM-DD-<slug>.md
docs/cybernetics/goals/YYYY-MM-DD-<slug>.md
docs/cybernetics/plans/YYYY-MM-DD-<slug>.md
docs/cybernetics/control-reviews/YYYY-MM-DD-<slug>.md
```

The predicted `/goal` command must include this precondition:

```text
If any referenced artifact is missing, not approved, or internally inconsistent, stop and report the smallest required human decision.
```

For Level 1/2 work with `Rubric Gate: required`, do not output the pre-goal orchestration command by default after rubric-only analysis. Output the next bounded goal-writing command instead:

```text
$writing-cybernetic-goals 使用 docs/cybernetics/requirements/YYYY-MM-DD-slug.md 中确认的评价口径，为这个 Level 2 有界审计/评估任务创建小型文件 goal，并在完成后给出直接 /goal 执行命令，不要默认建议 execution policy。
```

## Requirements Analysis Status

The brief must include:

```text
Status: `Incomplete` or `Complete`
```

Mark `Complete` only when:

- all blocking human decisions are resolved;
- confirmed requirement decisions are recorded;
- remaining assumptions are low-risk and explicit;
- the next step can safely create a solution design or goal contract.

## Output Format

If a brief was created or updated:

```markdown
Created or updated requirements analysis brief:

`docs/cybernetics/requirements/YYYY-MM-DD-slug.md`

Requirements analysis summary:
- ...

Blocking human decisions:
| Decision | Recommended default | Risk if wrong |
|---|---|---|
| ... | ... | ... |

Default assumptions:
- ...

Evaluation rubric, if applicable:
- Status meanings: ...
- Evidence levels: ...
- Minimum evidence for strongest positive status: ...
- Downgrade rules: ...
- External/unobservable dependency handling: ...
- Confidence/evidence grade: ...

Required gates:
- Semantic Gate: ...
- Rubric Gate: ...
- Design Gate: ...
- Risk Gate: ...

Deferred to design:
- ...

Deferred to planning/execution:
- ...

Questions:
1. ...
2. ...
3. ...

Next action:
Reply with one of:
- `按默认继续`
- answers to the questions
- revised scope
- cancel/postpone
```

If all blocking decisions are resolved for full pre-goal work:

````markdown
Requirements analysis is complete.

Updated requirements analysis brief:
`docs/cybernetics/requirements/YYYY-MM-DD-slug.md`

Queue these commands:

```text
$designing-cybernetic-solutions 根据 docs/cybernetics/requirements/YYYY-MM-DD-slug.md 创建 solution design。（仅当 Design Gate: required）
$orchestrating-cybernetic-pregoal 根据 docs/cybernetics/requirements/YYYY-MM-DD-slug.md 完成 pre-goal 编译，允许使用 subagents review。
```

Predicted queue-friendly `/goal`:

```text
/goal Execute the approved execution policy in docs/cybernetics/plans/YYYY-MM-DD-slug.md under the control contract in docs/cybernetics/goals/YYYY-MM-DD-slug.md, the confirmed requirements in docs/cybernetics/requirements/YYYY-MM-DD-slug.md, and the solution design in docs/cybernetics/designs/YYYY-MM-DD-slug.md when Design Gate is required. Use the approved control review in docs/cybernetics/control-reviews/YYYY-MM-DD-slug.md as the phase-gate record. Do not reinterpret requirements, rewrite the solution design, rewrite the control strategy, replace approved sensors, or start unreviewed work. If any referenced artifact is missing, not approved, or internally inconsistent, stop and report the smallest required human decision.
```
````

If all blocking decisions are resolved for Level 1/2 work with `Rubric Gate: required`:

````markdown
Rubric analysis is complete.

Updated requirements analysis brief:
`docs/cybernetics/requirements/YYYY-MM-DD-slug.md`

Confirmed evaluation rubric:
- Status meanings: ...
- Evidence levels: ...
- Minimum evidence for strongest positive status: ...
- Downgrade rules: ...
- External/unobservable dependency handling: ...
- Confidence/evidence grade: ...

Ready for bounded goal writing:

```text
$writing-cybernetic-goals 使用 docs/cybernetics/requirements/YYYY-MM-DD-slug.md 中确认的评价口径，为这个 Level 2 有界审计/评估任务创建小型文件 goal，并在完成后给出直接 /goal 执行命令，不要默认建议 execution policy。
```
````

## Validation Checklist

- [ ] Requirement semantics are separated from solution design and implementation planning.
- [ ] Evaluation predicates are treated as rubric/error-function semantics.
- [ ] Evaluation tasks define or ask for status meanings, evidence strength, strongest-positive threshold, downgrade rules, and external/unobservable handling.
- [ ] Design Gate is recorded as required, satisfied, or not applicable when solution structure matters.
- [ ] The response did not downscope because implementation is hard.
- [ ] Uncertainty is classified into blocking decisions, default assumptions, deferred design, and deferred planning/execution.
- [ ] Obvious defaults are not asked as blocking questions.
- [ ] There are no more than 7 questions.
- [ ] The brief includes `Requirements Analysis Status`.
- [ ] No solution design, goal, plan, control review, or approved runtime `/goal` was created.
- [ ] Level 1/2 work with `Rubric Gate: required` routes to `$writing-cybernetic-goals`, not full pre-goal orchestration by default.
- [ ] Any predicted queue-friendly `/goal` is clearly labeled as predicted and includes the missing/not-approved/inconsistent artifact precondition.
- [ ] If Design Gate is required, next commands include `$designing-cybernetic-solutions` before pre-goal orchestration.
