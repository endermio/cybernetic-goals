---
name: clarifying-cybernetic-tasks
description: 'Use before writing a Codex /goal, implementation plan, or code for complex or ambiguous work. Clarifies human intent, domain concepts, product behavior, permissions, data model choices, verification criteria, non-goals, and stop conditions. Do not downscope requirements merely because implementation seems hard. Ask only high-value human questions, record obvious defaults as assumptions, defer execution details to planning, and create a clarification brief under docs/superpowers/clarifications/ when file writing is available.'
---

# Clarifying Cybernetic Tasks

## Overview

Turn a fuzzy human intention into an approved task understanding before it becomes a Codex `/goal`, implementation plan, or code change.

This skill is a pre-goal control loop:

```text
human purpose -> AI context scan -> ambiguity map -> human decisions -> approved assumptions -> goal-ready task brief
```

This skill clarifies requirements and product semantics. It does not write approved final `/goal` commands, does not create final goal files, and does not start implementation. When clarification is complete and the brief path has a deterministic date/slug, it may output a predicted queue-friendly `/goal` command that is guarded by future approved artifacts.

Output:

- a concise clarification response in chat, or
- a clarification brief at `docs/superpowers/clarifications/YYYY-MM-DD-<slug>.md`.

Use `assets/clarification-brief-template.md` for the file structure.

## Core Rules

### Clarify Requirements, Do Not Downscope Them

Do not reduce, simplify, postpone, or replace the requested behavior merely because implementation seems complex, risky, unstable, or hard.

Implementation complexity may be recorded as execution risk, planning concern, verification concern, or future implementation challenge. It must not become the recommended product default unless the human explicitly asks for a lower-risk scope.

### Ask Only High-Value Human Questions

Ask the human a question only if all are true:

1. The answer materially changes product semantics, data model, permission model, public API, acceptance criteria, or user-visible behavior.
2. There are at least two plausible business choices.
3. The correct answer cannot be safely inferred from the user request, existing docs, or common product conventions.
4. A wrong default would be costly to reverse or would cause serious misalignment.

Do not ask the human about routine execution tactics, obvious resilience behavior, or implementation mechanics.

### Use Decision Levels

Classify uncertainty as:

- Level 1: Blocking Human Decision
- Level 2: Default Assumption
- Level 3: Deferred Execution / Planning Detail

Only Level 1 items should become questions.

### Clarify Evaluation Functions

For audit, evaluation, readiness, closure, completeness, usability, safety, stability, coverage, correctness, or status-classification tasks, treat the rubric as requirement semantics.

Evaluation predicates include terms such as:

```text
闭环, 完成, 可用, 通过, 达标, 就绪, 用户视角, 质量好, 稳定, 安全, 合理, 充分, 覆盖, 一致, 正确, 可交付, 生产可用, 验收通过
```

Do not treat these as self-explanatory. The clarification must identify the error function:

- status meanings or pass/fail categories;
- evidence levels or evidence strength;
- the minimum evidence needed for the strongest positive status;
- downgrade rules for partial, weak, missing, stale, or indirect evidence;
- handling for external credentials, production-only dependencies, third-party services, or currently unobservable behavior;
- whether confidence or evidence grade must be reported.

For rubric-only clarification, ask a short set of high-value questions focused on the evaluation function. If the user asks to proceed by default, use a conservative rubric:

```text
Strongest positive status requires actual UI/API workflow evidence or a successfully run smoke/e2e/similar runtime check.
Partial status means code, page, API, docs, or unrun tests exist, but actual user-path evidence is missing.
Negative status means only placeholders/plans exist, or no usable entrypoint exists.
Unknown/unverifiable status means external credentials, production-only environment, third-party service, or current environment prevents observation.
```

## Process

1. Inspect just enough context to ask non-generic questions.
2. Restate the human purpose in product language.
3. Build a control map: objective, controlled object, sensors, actuators, constraints, disturbances, stop conditions.
4. If the task is evaluative, identify the rubric/error function and classify missing rubric elements as decisions.
5. Identify and classify decisions by level.
6. Ask 3-7 high-value questions, preferably no more than 5.
7. Create or update the clarification brief.
8. If the human answers, update `Confirmed Decisions From Human` and the `Clarification Status`.
9. Do not create a goal, plan, control review, or approved runtime `/goal` command.
10. If clarification is complete and the brief path deterministically identifies a date/slug, output queue-friendly next commands as described below.

## Queue-Friendly Next Commands

When clarification is complete, choose the next command from the intended workflow.

For Level 3/4 or full pre-goal clarification, and when the clarification path is deterministic, output two commands the user can queue in Codex CLI:

1. A pre-goal orchestration command using the concrete clarification path.
2. A predicted queue-friendly `/goal` command using the expected artifact paths for the same date/slug.

The predicted `/goal` is not the final approved runtime command. Label it as predicted or queue-friendly, and make it depend on artifacts that the pre-goal orchestrator must create and approve.

Derive expected paths from:

```text
docs/superpowers/clarifications/YYYY-MM-DD-<slug>.md
```

Use the same `YYYY-MM-DD-<slug>` for:

```text
docs/superpowers/goals/YYYY-MM-DD-<slug>.md
docs/superpowers/plans/YYYY-MM-DD-<slug>.md
docs/superpowers/control-reviews/YYYY-MM-DD-<slug>.md
```

If the slug or path is not deterministic, do not output the predicted `/goal`; only output the orchestration command and state that the runtime command must be compiled after pre-goal approval.

The predicted `/goal` command must include this precondition:

```text
If any referenced artifact is missing, not approved, or internally inconsistent, stop and report the smallest required human decision.
```

For Level 1/2 work with `Rubric Gate: required`, do not output the pre-goal orchestration command by default after rubric-only clarification. Output the next bounded goal-writing command instead:

```text
$writing-cybernetic-goals 使用 docs/superpowers/clarifications/YYYY-MM-DD-slug.md 中确认的评价口径，为这个 Level 2 有界审计/评估任务创建小型文件 goal，并在完成后给出直接 /goal 执行命令，不要默认建议 execution policy。
```

The direct runtime `/goal` should be emitted by `$writing-cybernetic-goals` after it creates the bounded goal file.

## Clarification Status

The brief must include:

```text
Status: `Incomplete` or `Complete`
```

Mark `Complete` only when:

- all blocking human decisions are resolved;
- confirmed decisions are recorded;
- remaining assumptions are low-risk and explicit;
- the next step can safely create a goal contract.

## Output Format

If a brief was created or updated:

```markdown
Created or updated clarification brief:

`docs/superpowers/clarifications/YYYY-MM-DD-slug.md`

Clarification summary:
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

Deferred to planning:
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
Clarification is complete.

Updated clarification brief:
`docs/superpowers/clarifications/YYYY-MM-DD-slug.md`

Queue these commands:

```text
$orchestrating-cybernetic-pregoal 根据 docs/superpowers/clarifications/YYYY-MM-DD-slug.md 完成 pre-goal 编译，允许使用 subagents review。
```

Predicted queue-friendly `/goal`:

```text
/goal Execute the approved execution policy in docs/superpowers/plans/YYYY-MM-DD-slug.md under the control contract in docs/superpowers/goals/YYYY-MM-DD-slug.md and the confirmed semantics in docs/superpowers/clarifications/YYYY-MM-DD-slug.md. Use the approved control review in docs/superpowers/control-reviews/YYYY-MM-DD-slug.md as the phase-gate record. Do not reinterpret requirements, rewrite the control strategy, replace approved sensors, or start unreviewed work. If any referenced artifact is missing, not approved, or internally inconsistent, stop and report the smallest required human decision.
```
````

If all blocking decisions are resolved for Level 1/2 work with `Rubric Gate: required`:

````markdown
Rubric clarification is complete.

Updated clarification brief:
`docs/superpowers/clarifications/YYYY-MM-DD-slug.md`

Confirmed evaluation rubric:
- Status meanings: ...
- Evidence levels: ...
- Minimum evidence for strongest positive status: ...
- Downgrade rules: ...
- External/unobservable dependency handling: ...
- Confidence/evidence grade: ...

Ready for bounded goal writing:

```text
$writing-cybernetic-goals 使用 docs/superpowers/clarifications/YYYY-MM-DD-slug.md 中确认的评价口径，为这个 Level 2 有界审计/评估任务创建小型文件 goal，并在完成后给出直接 /goal 执行命令，不要默认建议 execution policy。
```
````

## Validation Checklist

- [ ] Requirement semantics are separated from implementation planning.
- [ ] Evaluation predicates are treated as rubric/error-function semantics, not routine execution details.
- [ ] Evaluation tasks define or ask for status meanings, evidence strength, strongest-positive threshold, downgrade rules, and external/unobservable handling.
- [ ] The response did not downscope because implementation is hard.
- [ ] Uncertainty is classified into blocking decisions, default assumptions, and deferred details.
- [ ] Obvious defaults are not asked as blocking questions.
- [ ] There are no more than 7 questions.
- [ ] The brief includes `Clarification Status`.
- [ ] No goal, plan, control review, or approved runtime `/goal` was created.
- [ ] Level 1/2 work with `Rubric Gate: required` routes to `$writing-cybernetic-goals`, not full pre-goal orchestration by default.
- [ ] Any predicted queue-friendly `/goal` is clearly labeled as predicted and includes the missing/not-approved/inconsistent artifact precondition.
