---
name: writing-cybernetic-goals
description: 'Use after requirements analysis is complete and any required solution design exists, when a router-selected Level 2 bounded task needs a small file goal, or when a low-risk task needs an inline goal. Applies when human semantics, any required design, and any required evaluation rubric are confirmed before execution.'
---

# Writing Cybernetic Goals

## Overview

Create a control contract from confirmed semantics and any required solution design.

This skill writes the goal contract. It does not analyze requirements, write execution policies, review control structures, or execute code.

For complex work, the output is:

```text
docs/cybernetics/goals/YYYY-MM-DD-<slug>.md
```

Use `assets/goal-contract-template.md`.

## Runtime Boundary

For complex implementation work, this skill must not produce an executable `/goal` command unless any required solution design exists and an approved execution policy and approved control review already exist.

If `Design Gate: required`, do not create the final complex goal contract until a solution design exists or the human explicitly says the Design Gate is unnecessary.

If no approved execution policy exists for complex work, stop after creating the goal contract and instruct the user to use `$writing-cybernetic-execution-policies`.

If no approved control review exists for complex work, instruct the user to use `$reviewing-cybernetic-control-structures`.

Do not put “first write a plan, then execute it” inside an execution `/goal` for complex work.

For Level 2 bounded file goals, output a direct `/goal` command after creating the small goal file only when the task boundaries and any required evaluation rubric are explicit. Do not recommend `$writing-cybernetic-execution-policies` or `$reviewing-cybernetic-control-structures` by default unless the user explicitly requests them or the task reveals unresolved control decisions.

## Evaluation Function Gate

Before creating a bounded audit/evaluation/readiness/closure/completeness/usability/safety/stability/coverage/correctness goal, check whether the evaluation rubric is explicit.

Evaluation predicates include terms such as:

```text
闭环, 完成, 可用, 通过, 达标, 就绪, 用户视角, 质量好, 稳定, 安全, 合理, 充分, 覆盖, 一致, 正确, 可交付, 生产可用, 验收通过
```

A bounded evaluation goal may be created only if the source semantics define:

- status meanings or pass/fail categories;
- evidence levels or evidence strength;
- the minimum evidence needed for the strongest positive status;
- downgrade rules for partial, weak, missing, stale, or indirect evidence;
- handling for external credentials, production-only dependencies, third-party services, or currently unobservable behavior;
- whether confidence or evidence grade must be reported.

If the rubric is missing or partial, do not create an executable bounded goal and do not output a direct `/goal`. Return a blocked rubric analysis request instead. This is not a reason to recommend execution policy by default; the missing artifact is the evaluation function, not the execution policy.

## Goal Modes

### Mode A: Complex Control Contract

Use when the task is Level 3/4, a complex implementation, or would require runtime Codex to coordinate execution policy, phase gates, sensor governance, or multi-batch implementation strategy.

Behavior:

1. Check whether `Design Gate: required`.
2. If required, confirm `docs/cybernetics/designs/YYYY-MM-DD-<slug>.md` or an explicit design source exists.
3. Create the goal contract under `docs/cybernetics/goals/YYYY-MM-DD-<slug>.md`.
4. Do not output an executable `/goal` unless an approved execution policy and approved control review already exist.
5. Recommend `$writing-cybernetic-execution-policies` as the next step when policy is missing.

### Mode B: Bounded File Goal / Audit Goal

Use when `$routing-cybernetic-workflows` selected Level 2, or the user explicitly asks for a small file goal, bounded audit goal, or bounded repair goal with fixed semantics.

Signals:

- task semantics are already fixed by the user or existing artifacts;
- no schema, permission, public API, or product semantics need to be decided;
- the output is one bounded artifact such as an audit report, repair report, checklist, or small patch contract;
- audit/evaluation/status-classification goals include an explicit rubric;
- verification needs are moderate, but no separate execution policy or phase-gate review is needed;
- the runtime agent must not expand scope or invent new control decisions.

Behavior:

1. Run the Evaluation Function Gate for audit/evaluation/status-classification tasks.
2. If the rubric is missing or partial, stop with a blocked rubric analysis request.
3. Create the small goal file under `docs/cybernetics/goals/YYYY-MM-DD-<slug>.md`.
4. Make the goal file self-contained enough to execute directly.
5. Preserve the rubric inside the goal when the task is evaluative.
6. Output a direct executable `/goal` command that references the small goal file.
7. Do not recommend execution policy or control review by default.
8. If the bounded goal proves insufficient, ambiguous, or dependent on new product/control decisions, instruct runtime Codex to stop and report the smallest required human decision.

## Preconditions

Before creating a goal contract for complex work, check:

- a requirements analysis brief exists;
- `Requirements Analysis Status` is `Complete` or the user explicitly states the semantics are confirmed;
- confirmed decisions are recorded;
- required solution design exists, or the user explicitly says the Design Gate is unnecessary;
- no blocking human decision remains unresolved.

If the requirements analysis is missing or incomplete, route back to `$analyzing-cybernetic-requirements`.

If Design Gate is required and no design exists, route to `$designing-cybernetic-solutions`.

For bounded file goals, a completed requirements analysis brief is optional when the user request or router decision already fixes the semantics, boundaries, output path, stop conditions, and any evaluation rubric. Record the user request or router decision as the source of truth.

## Goal Contract Requirements

The goal file must include:

1. Human Purpose
2. Objective
3. Success Condition
4. Source of Truth
5. Scope and Boundaries
6. Invariants
7. Verification Surface
8. Checkpoint Loop
9. Repair Policy
10. Progress Log
11. Stop Conditions
12. Blocked Report Format
13. Final Report Format

The goal must preserve confirmed semantics. It must not reinterpret or downscope them.

When a solution design is present, the goal must reference it under `Source of Truth`, preserve design invariants, and avoid freezing tactical design details as semantic invariants unless the design explicitly marks them as invariant.

For evaluation goals, the goal must also include the confirmed rubric as the error function: status definitions, evidence levels, strongest-positive evidence threshold, downgrade rules, and unobservable/external-dependency handling.

## Control Map

Map requirements analysis to:

- Objective: observable product/code state
- Sensors: tests, builds, API smoke, screenshots, reviews
- Error function: rubric for interpreting sensor output when the task is evaluative
- Constraints: invariants and non-goals
- Stop conditions: when Codex must stop instead of guessing

## Output Format

### Complex control contract

After creating a complex goal file:

```markdown
Created goal contract:

`docs/cybernetics/goals/YYYY-MM-DD-slug.md`

Control map:
- Objective: ...
- Sensors: ...
- Constraints: ...
- Solution design source: ...
- Stop conditions: ...

Next step:
Use `$writing-cybernetic-execution-policies` to create the approved execution policy.
```

### Bounded file goal

After creating a Level 2 bounded file goal:

````markdown
Created bounded file goal:

`docs/cybernetics/goals/YYYY-MM-DD-slug.md`

Control map:
- Objective: ...
- Sensors: ...
- Constraints: ...
- Stop conditions: ...

Use this `/goal`:

```text
/goal Execute the bounded file goal in docs/cybernetics/goals/YYYY-MM-DD-slug.md as the controlling contract. Do not create an execution policy or control review unless explicitly instructed. Do not reinterpret scope, expand requirements, or modify files outside the goal boundaries. If the goal is insufficient, ambiguous, or requires new product/control decisions, stop and report the smallest required human decision.
```
````

### Blocked rubric analysis

If a bounded audit/evaluation goal lacks an explicit rubric:

````markdown
Bounded goal blocked: evaluation rubric required.

Missing rubric elements:
- Status meanings: ...
- Evidence levels: ...
- Minimum evidence for strongest positive status: ...
- Downgrade rules: ...
- External/unobservable dependency handling: ...

Recommended next step:

```text
$analyzing-cybernetic-requirements 分析这个审计/评估任务的评价口径：...
```
````

### Blocked design gate

If complex goal writing is blocked because required design is missing:

````markdown
Goal contract blocked: solution design required.

Reason:
- Design Gate is required, but no solution design artifact or explicit design source was provided.

Recommended next step:

```text
$designing-cybernetic-solutions 根据 docs/cybernetics/requirements/YYYY-MM-DD-slug.md 创建 solution design。
```
````

If the user explicitly requests a small inline `/goal` and the task is low-risk, you may output an inline `/goal`.

## Validation Checklist

- [ ] Confirmed semantics are preserved.
- [ ] No unresolved human decisions are silently assumed.
- [ ] The goal contract does not contain instructions to write and approve a plan during runtime.
- [ ] The goal file references the requirements analysis brief.
- [ ] If Design Gate is required, the goal file references the solution design or blocks before creating the final goal.
- [ ] The goal preserves design invariants without freezing tactical design details.
- [ ] Success conditions and stop conditions are explicit.
- [ ] Sensors are named but not treated as the objective.
- [ ] Evaluation tasks define an explicit rubric before any executable goal is emitted.
- [ ] For complex work, no final runtime `/goal` was output unless approved plan and review exist.
- [ ] For Level 2 bounded file goals, the response outputs a direct `/goal` and does not recommend execution policy by default.
- [ ] Any bounded file `/goal` stops if the goal is insufficient, ambiguous, or requires new product/control decisions.
