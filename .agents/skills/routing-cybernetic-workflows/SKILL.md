---
name: routing-cybernetic-workflows
description: 'Use first when deciding whether a task should use the cybernetic workflow. Classifies work by control uncertainty, not scary keywords: direct prompt, inline goal, bounded file goal, full pre-goal pipeline, or high-risk human-gated workflow. Downgrades bounded corrections inside existing approved control artifacts and rejects over-heavy workflow for small tasks.'
---

# Routing Cybernetic Workflows

## Overview

Choose the lightest workflow that can control the task safely.

This skill is a router, not a planner, not a goal writer, not a requirements clarifier, and not an executor.

It decides whether the task needs:

- no cybernetic workflow
- an inline `/goal`
- a bounded file-based goal
- rubric clarification before a bounded/evaluation goal
- the full pre-goal pipeline
- a high-risk human-gated workflow

The key routing question is not:

```text
Does this task mention complex concepts?
```

The key routing question is:

```text
Would the execution agent otherwise need to invent or revise goals, product semantics, sensors, execution policy, or phase gates during runtime?
```

For evaluation tasks, also ask:

```text
Is the evaluation function already defined well enough that runtime Codex will not invent what "good", "done", "closed", "usable", "ready", or "passed" means?
```

Route based on unresolved control decisions, not scary keywords.

## Core Rule

Use the lightest workflow that keeps the agent from inventing control structure during execution.

A task should not be routed to the full pre-goal pipeline merely because it mentions:

- permissions
- corpId
- tenants
- supervision
- schema
- screenshots
- tests
- API smoke
- security words
- multiple files

Route to the full pipeline only when those areas contain unresolved control decisions.

## Output Contract

Every routing response must include:

1. `Routing decision`
2. `Why`
3. `Required gates`
4. `Rubric gate` when the task asks for evaluation, audit, readiness, closure, quality, completeness, correctness, usability, or status classification
5. `Recommended next step`
6. `Rejected workflow, if any`

Do not create files. Do not run implementation. Do not write a goal contract. Do not write an execution policy.

## Evaluation Function Gate

Before routing any task that asks Codex to evaluate, audit, assess, verify, check readiness, check closure, judge usability, judge completeness, classify status, or decide whether something is good/safe/stable/correct/covered/usable/ready/passed, check whether the evaluation rubric is explicit.

Evaluation predicates include terms such as:

```text
闭环, 完成, 可用, 通过, 达标, 就绪, 用户视角, 质量好, 稳定, 安全, 合理, 充分, 覆盖, 一致, 正确, 可交付, 生产可用, 验收通过
```

A rubric is explicit only when the task defines:

- status meanings or pass/fail categories;
- evidence levels or evidence strength;
- the minimum evidence needed for the strongest positive status;
- downgrade rules for partial, weak, missing, stale, or indirect evidence;
- handling for external credentials, production-only dependencies, third-party services, or currently unobservable behavior;
- whether confidence or evidence grade must be reported.

Object lists are not rubrics. A complete checklist of items to inspect does not define the error function for judging those items.

If the task is evaluative and the rubric is missing or only partially defined, keep the execution-complexity level unchanged and add `Rubric Gate: required` under `Required gates`.

Examples:

- `Level 1` + `Required gates: Rubric Gate required` means short rubric clarification before inline goal.
- `Level 2` + `Required gates: Rubric Gate required` means rubric clarification before bounded file/audit goal.
- `Level 3` + `Required gates: Rubric Gate required` means the full clarification phase must explicitly include rubric semantics.

Do not route an unrubriced evaluation task directly to execution merely because implementation scope is bounded.

## Downgrade Pass: Existing Control Structure

Before routing to Level 3, check whether this is a bounded correction inside an already clarified feature.

Downgrade to Level 1 or Level 2 when all are true:

- The task does not introduce a new product capability.
- Confirmed semantics already exist in a clarification, goal, plan, control review, prior approved decision, or explicit user instruction.
- The task does not require changing schema semantics, permission semantics, public API semantics, data visibility semantics, or product setpoint.
- The expected change can be described as a local correction to display, fixture data, naming, tests, screenshots, or one bounded workflow.
- The agent would not need to invent new goals, sensors, execution policies, or phase gates during execution.

Examples:

- Fixing REG/PARK being displayed as enterprise C1 after collaborative supervision semantics are already clarified.
- Adjusting local preview fixture names to avoid misleading corpId display.
- Changing a column label from `hash` to `哈希` when base58 semantics are already confirmed.
- Updating a stale screenshot assertion to match an already confirmed product decision.
- Tightening a route guard message without changing permission semantics.

These are not Level 3 merely because they mention permissions, corpId, supervision, tests, or screenshots.

## Complexity Levels

### Level 0: Direct Prompt

Use when the task is simple, local, low-risk, and has an obvious verification path.

Signals:

- one file or one small area
- no new product semantics
- no permission/data visibility change
- no schema/API contract change
- no long-lived control artifact needed
- obvious verification command or inspection

Recommended next step:

```text
Use a direct prompt.
```

Example:

```text
修复 tests/date-format.test.ts 当前失败的日期格式单测，不改变其他日期格式行为；运行 npm test tests/date-format.test.ts 验证。
```

Reject full workflow because the coordination overhead is larger than the task.

### Level 1: Inline Goal

Use when the task is small but benefits from a short completion contract.

Signals:

- one bounded objective
- clear success condition
- one or two verification surfaces
- no unresolved product semantics
- no need for a persistent goal file

Recommended next step:

```text
$writing-cybernetic-goals 为这个明确小任务写 inline /goal：<需求>
```

### Level 2: Bounded File Goal or Bounded Repair Goal

Use when the task is multi-file or has moderate verification needs, but the control semantics are already fixed.

Signals:

- requirements are already clear
- existing clarification/goal/plan already fixes semantics, or the user provides clear constraints
- no unresolved product semantics
- no new schema, permission, or public API semantics
- localized correction across UI, fixture, smoke, screenshot, docs, or one bounded workflow
- wide read-only audit with fixed classification semantics, an explicit evaluation rubric, and a fixed report artifact
- moderate verification needs
- a persistent small goal file may help, but a full pre-goal pipeline would be too heavy

Recommended next step options:

```text
Use a bounded repair prompt.
```

or:

```text
$writing-cybernetic-goals 为这个有界修正创建小型文件 goal：<需求>
```

For Level 2 bounded file goals, the expected next step after goal creation is a direct `/goal` execution command against that small goal file. Do not recommend `$writing-cybernetic-execution-policies` by default unless the user explicitly asks for it or the task exposes unresolved control decisions.

If an audit/evaluation/status-classification task names labels such as `已闭环`, `部分闭环`, `未闭环`, or `不可判定` but does not define the evidence rubric for those labels, keep the route at Level 2 and mark `Rubric Gate: required` before creating the bounded file goal.

If an existing feature has approved artifacts, reference them:

```text
保持 <clarification/goal/plan path> 中已确认语义不变，只修正 <bounded issue>.
```

### Level 2 With Rubric Gate

Use when execution complexity is Level 2 but the evaluation function is not yet defined.

Signals:

- the task is an audit, evaluation, readiness check, closure check, usability judgment, completeness check, safety/stability assessment, or status classification;
- object scope is clear enough for a bounded file goal;
- product/schema/permission/API semantics are not being redesigned;
- labels such as complete/closed/ready/usable/pass/fail/partial/unknown are present but not operationally defined.

Recommended next step:

```text
$clarifying-cybernetic-tasks 澄清这个 bounded audit/evaluation 的评价口径：<任务>
```

After rubric clarification is complete:

```text
$writing-cybernetic-goals 为这个 Level 2 有界任务创建小型文件 goal，并在完成后给出直接 /goal 执行命令，不要默认建议 execution policy：<任务 + confirmed rubric>
```

### Level 3: Full Pre-goal Pipeline

Use when the execution agent would otherwise need to invent or revise the control structure.

Strong signals:

- product/domain semantics are unresolved
- permission or data visibility semantics are unresolved
- schema/API/UI/test changes must be coordinated and no approved control artifacts exist
- old tests may be stale and no sensor governance exists yet
- execution requires multiple batches and phase gates not yet defined
- the task would require creating or revising clarification, goal, execution policy, or control review before safe execution
- multiple subsystems are involved and the success criteria are not already frozen
- evaluation rubric or sensor interpretation is unclear and the task is already complex enough to need full clarification

Recommended next step:

```text
$clarifying-cybernetic-tasks <需求>
```

After clarification is complete:

```text
$orchestrating-cybernetic-pregoal 根据 <clarification-path> 完成 pre-goal 编译，允许使用 subagents review。
```

If orchestration is unavailable, manually run:

```text
$writing-cybernetic-goals
$writing-cybernetic-execution-policies
$reviewing-cybernetic-control-structures
$compiling-cybernetic-runtime-goals
```

### Level 4: High-Risk Human-Gated Workflow

Use when the task has high irreversible, external, or regulated risk.

Signals:

- production deployment
- real credentials
- irreversible data migration
- financial, legal, medical, compliance, safety, or security-critical decisions
- external customer data
- destructive actions
- public API breakage with external consumers
- regulatory or contractual implications

Recommended next step:

```text
Use the full pre-goal pipeline, but require explicit human approval before runtime /goal execution.
```

## Scoring Heuristic

Score actual control uncertainty, not merely possible implementation surface.

| Dimension | Score |
|---|---:|
| New product/domain semantics must be decided | +3 |
| New permission/data visibility semantics must be decided | +3 |
| New schema or migration semantics must be decided | +2 |
| Multiple subsystems need coordinated changes | +2 |
| Public API or external contract semantics must change | +2 |
| Existing tests are likely stale sensors and require governance | +2 |
| Requires multiple implementation batches | +2 |
| Requires screenshots/API smoke/evals | +1 |
| Irreversible or production-impacting | +4 |
| Existing clarification/goal/plan/control review already fixes semantics | -3 |
| Task is a bounded correction inside an existing feature | -3 |
| No schema/permission/API semantic change | -2 |
| Goal and verification are already obvious | -1 |

Guidance:

- 0–2: Level 0
- 3–5: Level 1
- 6–8: Level 2
- 9–13: Level 3
- 14+: Level 4

The score is not binding. Use judgment. If the score and the downgrade pass disagree, explain why.

Rubric clarity is orthogonal to the score. Missing evaluation rubric does not automatically mean Level 3; it means the selected level must list `Rubric Gate: required` unless the broader task already belongs in Level 3.

## Control-Decision Test

Before choosing Level 3, ask:

```text
What unresolved control decision would the execution agent have to make if we did not run the full pipeline?
```

If the answer is only:

- component naming
- column visibility
- fixture cleanup
- screenshot text
- obvious UI copy
- bounded test update
- local route guard presentation
- stale assertion update

then do not choose Level 3.

If the answer includes:

- what the product means
- who can see what
- how data visibility works
- whether schema semantics change
- what the target state is
- which sensors are authoritative
- what observations count as good, bad, complete, partial, unknown, ready, safe, stable, usable, or passed
- what execution policy is allowed
- what phase gates are needed

then Level 3 may be appropriate.

## Recommended Response Shapes

### Level 0

```markdown
Routing decision: Level 0 - Direct Prompt

Why:
- ...

Required gates:
- None.

Recommended next step:
Use a direct prompt:

```text
...
```

Rejected workflow:
- Full cybernetic workflow would be heavier than the task.
```

### Level 1

```markdown
Routing decision: Level 1 - Inline Goal

Why:
- ...

Required gates:
- None, unless the task is evaluative and the Rubric Gate is required.

Recommended next step:
Use:

```text
$writing-cybernetic-goals 为这个明确小任务写 inline /goal：...
```
```

### Level 2

```markdown
Routing decision: Level 2 - Bounded File Goal / Bounded Repair

Why:
- Existing semantics are already fixed.
- No new schema/permission/API semantics appear required.
- The task is a bounded correction.

Required gates:
- None, or only gates already satisfied by confirmed inputs.

Rubric gate:
- Not an evaluation task, or evaluation rubric is already explicit.

Recommended next step:
Use a bounded repair prompt or small file-based goal:

```text
修正 <issue>，保持 <approved artifact paths or confirmed semantics> 不变；验证 <commands/artifacts>.
```

For a file-based goal:

```text
$writing-cybernetic-goals 为这个 Level 2 有界任务创建小型文件 goal，并在完成后给出直接 /goal 执行命令，不要默认建议 execution policy：...
```

Rejected workflow:
- Reject Level 3 because no new control structure is required.
- Do not recommend execution policy by default for Level 2; add required gates or upgrade only if unresolved control decisions appear.
```

### Level 2 With Rubric Gate

```markdown
Routing decision: Level 2 - Bounded Audit

Why:
- Execution scope is bounded enough for a file goal.
- Product/schema/permission/API semantics do not need redesign.
- The evaluation function is not explicit enough for runtime execution.

Required gates:
- Rubric Gate: required.

Rubric gate:
- Missing or partial: status meanings, evidence strength, minimum evidence for the strongest positive status, downgrade rules, and external-dependency handling.

Recommended next step:
Use rubric clarification before goal writing:

```text
$clarifying-cybernetic-tasks 澄清这个审计/评估任务的评价口径：...
```

Rejected workflow:
- Reject direct Level 2 execution because runtime Codex would invent the error function.
- Reject Level 3 unless broader product/control semantics are also unresolved.
```

### Level 3

```markdown
Routing decision: Level 3 - Full Pre-goal Pipeline

Why:
- ...

Required gates:
- Clarification Gate: required.
- Goal Contract Gate: required.
- Execution Policy Gate: required.
- Control Review Gate: required.
- Rubric Gate: required if the task is evaluative and the rubric is not explicit.

Recommended next step:
1. `$clarifying-cybernetic-tasks <需求>`
2. After clarification is complete: `$orchestrating-cybernetic-pregoal 根据 <clarification-path> 完成 pre-goal 编译，允许使用 subagents review。`

Rejected workflow:
- Level 0/1/2 would force runtime agent to invent unresolved control decisions.
```

### Level 4

```markdown
Routing decision: Level 4 - Human-Gated Full Pipeline

Why:
- ...

Required gates:
- Full pre-goal gates: required.
- Explicit Human Approval Gate: required before runtime execution.
- Rubric Gate: required if the task is evaluative and the rubric is not explicit.

Recommended next step:
Run the full pre-goal pipeline, but require explicit human approval before runtime `/goal`.

Rejected workflow:
- Do not allow ungated runtime execution.
```

## Common Mistakes

| Mistake | Fix |
|---|---|
| Routing by scary keywords | Route by unresolved control decisions |
| Treating any permission mention as Level 3 | Ask whether permission semantics change |
| Treating any schema mention as Level 3 | Ask whether schema semantics change |
| Treating any screenshot mention as Level 3 | Screenshots alone are often Level 1/2 sensors |
| Treating existing-feature fixes as new-feature work | Run the downgrade pass |
| Recommending full pipeline for local display/fixture cleanup | Use Level 1/2 |
| Ignoring approved clarification/goal/plan artifacts | Downgrade when semantics are already frozen |
| Listing five manual pre-goal skills when orchestrator exists | Prefer `$clarifying-cybernetic-tasks` then `$orchestrating-cybernetic-pregoal` |
| Letting small tasks use the full workflow because the user asked | Explain that the workflow is over-control and propose a lighter route |
| Recommending execution policy after a Level 2 bounded file goal | Give the direct `/goal` path unless the user explicitly asks for policy or new control decisions appear |
| Treating an object checklist as a completed rubric | Check the evaluation function before routing to execution |
| Adding special cases for words like "闭环" | Use the generic Evaluation Function Gate for all evaluative predicates |
| Encoding gates in the routing level name | Keep `Routing decision: Level N` and list gates under `Required gates` |

## Validation Checklist

Before responding, verify:

- [ ] The decision is based on unresolved control decisions, not scary keywords.
- [ ] The downgrade pass was considered before Level 3.
- [ ] Existing approved artifacts or confirmed semantics were considered.
- [ ] The response distinguishes “concept sensitive” from “control structure unresolved.”
- [ ] The routing decision uses only Level 0/1/2/3/4, without suffixes.
- [ ] Required gates are listed separately from the routing level.
- [ ] Evaluation tasks include a rubric gate decision.
- [ ] A complete object list is not mistaken for a complete evaluation rubric.
- [ ] The recommended next step is the lightest safe workflow.
- [ ] For Level 3, the response recommends `$clarifying-cybernetic-tasks` then `$orchestrating-cybernetic-pregoal`.
- [ ] For Level 0/1/2, the response does not recommend full pre-goal pipeline.
- [ ] For Level 2 bounded file goals, the response does not recommend execution policy by default.
- [ ] If Rubric Gate is required, the response recommends rubric clarification before execution.
- [ ] The response includes rejected workflow rationale.
