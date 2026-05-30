---
name: routing-cybernetic-workflows
description: 'Use first when deciding whether a task should use the cybernetic workflow. Classifies work by control uncertainty and required gates, not scary keywords: direct prompt, inline goal, bounded file goal, Design Gate, Rubric Gate, full pre-goal pipeline, or high-risk human-gated workflow. Downgrades bounded corrections inside existing approved control artifacts and rejects over-heavy workflow for small tasks.'
---

# Routing Cybernetic Workflows

## Overview

Choose the lightest workflow that can control the task safely.

This skill is a router, not a planner, not a goal writer, not a requirements analyzer, and not an executor.

It decides whether the task needs:

- no cybernetic workflow
- an inline `/goal`
- a bounded file-based goal
- rubric analysis before a bounded/evaluation goal
- solution design before goal writing
- the full pre-goal pipeline
- a high-risk human-gated workflow

The key routing question is not:

```text
Does this task mention complex concepts?
```

The key routing question is:

```text
Would the execution agent otherwise need to invent or revise control contracts, requirement semantics, solution structure, sensors, execution policy, or phase gates during runtime?
```

For evaluation tasks, also ask:

```text
Is the evaluation function already defined well enough that runtime Codex will not invent what "good", "done", "closed", "usable", "ready", or "passed" means?
```

For output-sensitive tasks, also ask:

```text
Is the final output contract defined well enough that runtime Codex will not invent the audience, purpose, medium, structure, detail level, destination, or machine-readable shape?
```

Route based on unresolved control decisions, not scary keywords.

## Core Rule

Use the lightest workflow that keeps the agent from inventing control structure during execution.

A task should not be routed to the full pre-goal pipeline merely because it mentions:

- authorization
- identity mapping
- participant groups
- oversight
- structure contracts
- evidence artifacts
- checks
- evidence channels
- risk words
- multiple artifacts

Route to the full pipeline only when those areas contain unresolved control decisions.

## Output Contract

Every routing response must include:

1. `Routing decision`
2. `Why`
3. `Required gates`
4. `Rubric gate` when the task asks for evaluation, audit, readiness, closure, quality, completeness, correctness, usability, or status classification
5. `Output Contract gate` when output shape affects execution, acceptance, handoff, persistence, or downstream consumption
6. `Design gate` when the task may require a solution model before goal writing
7. `Recommended next step`
8. `Rejected workflow, if any`

Do not create files. Do not run target execution. Do not write a goal contract. Do not write an execution policy.

Routing recommendations and handoff prompts are response-only. Do not write them into requirements, design, goal, plan, review, progress, or orchestration-status artifacts.

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

- `Level 1` + `Required gates: Rubric Gate required` means short rubric analysis before inline goal.
- `Level 2` + `Required gates: Rubric Gate required` means rubric analysis before bounded file/audit goal.
- `Level 3` + `Required gates: Rubric Gate required` means the full requirements analysis phase must explicitly include rubric semantics.

Do not route an unrubriced evaluation task directly to execution merely because execution scope is bounded.

## Output Contract Gate

Before routing tasks whose final result will be consumed for a decision, handoff, audit, record, downstream action, or machine consumption, check whether the output contract is explicit enough that runtime Codex will not invent the final shape.

Output Contract Gate is explicit only when the task or existing artifacts define enough of the relevant:

- audience;
- purpose;
- medium;
- required structure;
- detail level;
- evidence-reference needs;
- machine-readable needs;
- destination path;
- acceptance condition.

If output shape is missing or partial and the wrong shape would make the task unusable or change execution/acceptance, keep the execution-complexity level unchanged and add `Output Contract Gate: required` under `Required gates`.

Do not require this gate for simple tasks whose output is obviously a short chat summary or local confirmation. Do not turn output format into a routine question.

Examples:

- `Level 1` + `Output Contract Gate: satisfied` can describe a simple local correction with a brief chat summary.
- `Level 2` + `Output Contract Gate: required` can describe a bounded audit/report task whose evaluation scope is clear but whose decision-report shape is not defined.
- `Level 3` + `Output Contract Gate: required` can describe full pre-goal work where downstream runtime must produce a structured artifact bundle or machine-readable handoff.

## Design Gate

Before routing any task where the target semantics are known but the solution structure may be unclear, check whether a design model is explicit enough that runtime Codex will not invent objects, relationships, flows, interfaces, boundaries, or evidence models.

Design Gate is explicit only when the task or existing artifacts define the relevant:

- core objects, actors, roles, or responsibilities;
- relationships among concepts or entities;
- system, process, or organizational boundaries;
- information flow, state flow, evidence flow, or decision flow;
- interfaces, contracts, reports, procedures, events, or user interactions;
- lifecycle, failure/exception model, and evidence/sensor model when relevant;
- design invariants versus tactical degrees of freedom.

If solution structure is missing or partial, keep the execution-complexity level unchanged and add `Design Gate: required` under `Required gates`.

Examples:

- `Level 2` + `Design Gate: required` can describe a bounded audit/report task whose rubric is clear but report/evidence structure still needs a lightweight design.
- `Level 3` + `Design Gate: required` describes complex work where requirement semantics are analyzed but the system/process model must be synthesized before goal and plan writing.

Do not encode design in the level name. Use `Level N` plus `Required gates`.

## Downgrade Pass: Existing Control Structure

Before routing to Level 3, check whether this is a bounded correction inside an already analyzed feature.

Downgrade to Level 1 or Level 2 when all are true:

- The task does not introduce a new required capability.
- Confirmed semantics and any required solution structure already exist in a requirements analysis, solution design, goal, plan, control review, prior approved decision, or explicit user instruction.
- The task does not require changing structure-contract semantics, authorization semantics, external contract semantics, visibility semantics, or target setpoint.
- The expected change can be described as a local correction to observer output, source fixtures, naming, checks, evidence artifacts, or one bounded workflow.
- The agent would not need to invent new solution design, goals, sensors, execution policies, or phase gates during execution.

Examples:

- Correcting an observer label after the identity semantics are already analyzed.
- Adjusting local source fixtures to avoid misleading entity display.
- Changing a displayed term when identifier semantics are already confirmed.
- Updating a stale evidence assertion to match an already confirmed requirement decision.
- Tightening an access-boundary message without changing authorization semantics.

These are not Level 3 merely because they mention authorization, identity mapping, oversight, checks, or evidence artifacts.

## Complexity Levels

### Level 0: Direct Prompt

Use when the task is simple, local, low-risk, and has an obvious verification path.

Signals:

- one file or one small area
- no new requirement semantics
- no authorization/visibility change
- no structure/external contract change
- no long-lived control artifact needed
- obvious verification command or inspection

Recommended next step:

```text
Use a direct prompt.
```

Example:

```text
修复一个当前失败的局部检查，不改变相关目标行为；运行对应 focused check 验证。
```

Reject full workflow because the coordination overhead is larger than the task.

### Level 1: Inline Goal

Use when the task is small but benefits from a short completion contract.

Signals:

- one bounded objective
- clear success condition
- one or two verification surfaces
- no unresolved requirement semantics
- no need for a persistent goal file

Recommended next step:

```text
$writing-cybernetic-goals 为这个明确小任务写 inline /goal：<需求>
```

### Level 2: Bounded File Goal or Bounded Repair Goal

Use when the task is multi-file or has moderate verification needs, but the control semantics are already fixed.

Signals:

- requirements are already clear
- existing requirements analysis/solution design/goal/plan already fixes semantics and solution structure, or the user provides clear constraints
- no unresolved requirement semantics
- no new structure-contract, authorization, or external contract semantics
- localized correction across observer output, source fixture, evidence channel, documentation, or one bounded workflow
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
保持 <requirements analysis/design/goal/plan path> 中已确认语义和设计不变，只修正 <bounded issue>.
```

### Level 2 With Rubric Gate

Use when execution complexity is Level 2 but the evaluation function is not yet defined.

Signals:

- the task is an audit, evaluation, readiness check, closure check, usability judgment, completeness check, safety/stability assessment, or status classification;
- object scope is clear enough for a bounded file goal;
- requirement, structure-contract, authorization, or external-contract semantics are not being redesigned;
- labels such as complete/closed/ready/usable/pass/fail/partial/unknown are present but not operationally defined.

Recommended next step:

```text
$analyzing-cybernetic-requirements 分析这个 bounded audit/evaluation 的评价口径：<任务>
```

After rubric analysis is complete:

```text
$writing-cybernetic-goals 为这个 Level 2 有界任务创建小型文件 goal，并在完成后给出直接 /goal 执行命令，不要默认建议 execution policy：<任务 + confirmed rubric>
```

### Level 3: Full Pre-goal Pipeline

Use when the execution agent would otherwise need to invent or revise the control structure.

Strong signals:

- requirement semantics are unresolved
- authorization or visibility semantics are unresolved
- structure contracts, observer surfaces, and evidence channels must be coordinated and no approved control artifacts exist
- old sensors may be stale and no sensor governance exists yet
- solution structure is unresolved: objects, relationships, boundaries, flows, interfaces, or evidence model need design
- execution requires multiple batches and phase gates not yet defined
- the task would require creating or revising requirements analysis, solution design, goal, execution policy, or control review before safe execution
- multiple subsystems are involved and the success criteria are not already frozen
- evaluation rubric or sensor interpretation is unclear and the task is already complex enough to need full requirements analysis

Recommended next step:

```text
$analyzing-cybernetic-requirements <需求>
```

If requirements analysis completes and `Design Gate: required`, run:

```text
$designing-cybernetic-solutions 根据 <requirements-path> 创建 solution design。
```

After requirements analysis is complete:

```text
$orchestrating-cybernetic-pregoal 根据 <requirements-path> 完成 pre-goal 编译，允许使用 subagents review。
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

- live external-state change
- real credentials
- irreversible state transition
- financial, legal, medical, compliance, safety, or security-critical decisions
- external participant data
- destructive actions
- external contract breakage with external consumers
- regulatory or contractual implications

Recommended next step:

```text
Use the full pre-goal pipeline, but require explicit human approval before runtime /goal execution.
```

## Scoring Heuristic

Score actual control uncertainty, not merely possible execution surface.

| Dimension | Score |
|---|---:|
| New requirement semantics must be decided | +3 |
| New authorization/visibility semantics must be decided | +3 |
| New structure or transition semantics must be decided | +2 |
| Solution structure or design model must be decided | +3 |
| Multiple subsystems need coordinated changes | +2 |
| External contract semantics must change | +2 |
| Existing sensors are likely stale and require governance | +2 |
| Requires multiple execution batches | +2 |
| Requires multiple evidence channels | +1 |
| Irreversible or live-state-impacting | +4 |
| Existing requirements analysis/solution design/goal/plan/control review already fixes semantics and solution structure | -3 |
| Task is a bounded correction inside an existing feature | -3 |
| No structure/authorization/external-contract semantic change | -2 |
| Goal and verification are already obvious | -1 |

Guidance:

- 0–2: Level 0
- 3–5: Level 1
- 6–8: Level 2
- 9–13: Level 3
- 14+: Level 4

The score is not binding. Use judgment. If the score and the downgrade pass disagree, explain why.

Rubric clarity is orthogonal to the score. Missing evaluation rubric does not automatically mean Level 3; it means the selected level must list `Rubric Gate: required` unless the broader task already belongs in Level 3.

Design clarity is also orthogonal to the score. Missing solution structure means the selected level must list `Design Gate: required`; it does not create a new level suffix.

## Control-Decision Test

Before choosing Level 3, ask:

```text
What unresolved control decision would the execution agent have to make if we did not run the full pipeline?
```

If the answer is only:

- mechanism naming
- observer-field visibility
- fixture cleanup
- evidence-artifact text
- obvious observer text
- bounded sensor update
- local boundary-message presentation
- stale assertion update

then do not choose Level 3.

If the answer includes:

- what the requirement means
- who can see what
- how visibility works
- whether structure semantics change
- what the target state is
- what solution model, object relationships, boundaries, or information/state flow should be used
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
- None, unless Rubric Gate, Output Contract Gate, or Design Gate is required.

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
- No new structure/authorization/external-contract semantics appear required.
- The task is a bounded correction.

Required gates:
- None, or only gates already satisfied by confirmed inputs.

Rubric gate:
- Not an evaluation task, or evaluation rubric is already explicit.

Design gate:
- Satisfied or not applicable when solution structure is already fixed.

Output Contract gate:
- Satisfied or not applicable when a simple response or confirmed artifact shape is enough.

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
- Requirement, structure-contract, authorization, and external-contract semantics do not need redesign.
- The evaluation function is not explicit enough for runtime execution.

Required gates:
- Rubric Gate: required.
- Output Contract Gate: required if the final report shape affects acceptance and is not explicit.

Rubric gate:
- Missing or partial: status meanings, evidence strength, minimum evidence for the strongest positive status, downgrade rules, and external-dependency handling.

Recommended next step:
Use rubric analysis before goal writing:

```text
$analyzing-cybernetic-requirements 分析这个审计/评估任务的评价口径：...
```

Rejected workflow:
- Reject direct Level 2 execution because runtime Codex would invent the error function.
- Reject Level 3 unless broader requirement/control semantics are also unresolved.
```

### Level 2 With Design Gate

```markdown
Routing decision: Level 2 - Bounded Design/Audit/Repair

Why:
- Execution scope is bounded enough for a small goal after design.
- Requirement, structure-contract, authorization, and external-contract semantics do not need redesign.
- The solution/report/evidence structure is not explicit enough for runtime execution.

Required gates:
- Design Gate: required.
- Rubric Gate: required if the task is evaluative and the rubric is not explicit.
- Output Contract Gate: required if the final output audience, medium, structure, or acceptance condition is not explicit.

Design gate:
- Missing or partial: objects/actors/roles, relationships, flow, boundaries, interfaces/contracts, or evidence model.

Recommended next step:
Use solution design before goal writing:

```text
$designing-cybernetic-solutions 根据 <requirements-path or confirmed request> 创建 solution design。
```

Rejected workflow:
- Reject direct Level 2 execution because runtime Codex would invent the solution model.
- Reject Level 3 unless broader control semantics are also unresolved.
```

### Level 3

```markdown
Routing decision: Level 3 - Full Pre-goal Pipeline

Why:
- ...

Required gates:
- Semantic Gate: required.
- Goal Contract Gate: required.
- Design Gate: required if solution structure is not explicit.
- Output Contract Gate: required if final output shape affects execution, acceptance, handoff, persistence, or downstream consumption and is not explicit.
- Execution Policy Gate: required.
- Control Review Gate: required.
- Rubric Gate: required if the task is evaluative and the rubric is not explicit.

Recommended next step:
1. `$analyzing-cybernetic-requirements <需求>`
2. If Design Gate is required: `$designing-cybernetic-solutions 根据 <requirements-path> 创建 solution design。`
3. After requirements analysis/design are ready: `$orchestrating-cybernetic-pregoal 根据 <requirements-path> 完成 pre-goal 编译，允许使用 subagents review。`

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
- Design Gate: required if solution structure is not explicit.
- Output Contract Gate: required if final output shape affects execution, acceptance, handoff, persistence, or downstream consumption and is not explicit.

Recommended next step:
Run the full pre-goal pipeline, but require explicit human approval before runtime `/goal`.

Rejected workflow:
- Do not allow ungated runtime execution.
```

## Common Mistakes

| Mistake | Fix |
|---|---|
| Routing by scary keywords | Route by unresolved control decisions |
| Treating any authorization mention as Level 3 | Ask whether authorization semantics change |
| Treating any structure mention as Level 3 | Ask whether structure semantics change |
| Treating any evidence-artifact mention as Level 3 | Evidence artifacts alone are often Level 1/2 sensors |
| Treating existing-feature fixes as new-feature work | Run the downgrade pass |
| Recommending full pipeline for local display/fixture cleanup | Use Level 1/2 |
| Ignoring approved requirements analysis/design/goal/plan artifacts | Downgrade when semantics and solution structure are already frozen |
| Listing five manual pre-goal skills when orchestrator exists | Prefer `$analyzing-cybernetic-requirements` then `$orchestrating-cybernetic-pregoal` |
| Letting small tasks use the full workflow because the user asked | Explain that the workflow is over-control and propose a lighter route |
| Recommending execution policy after a Level 2 bounded file goal | Give the direct `/goal` path unless the user explicitly asks for policy or new control decisions appear |
| Treating an object checklist as a completed rubric | Check the evaluation function before routing to execution |
| Treating a requirement list as a completed design | Check whether objects, relationships, flows, boundaries, and evidence model are explicit |
| Asking every simple task for output format | Use Output Contract Gate only when output shape affects execution, acceptance, handoff, persistence, or downstream consumption |
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
- [ ] Output-sensitive tasks include an output contract gate decision, while simple tasks use safe defaults.
- [ ] Tasks with unclear solution structure include a design gate decision.
- [ ] A complete object list is not mistaken for a complete evaluation rubric.
- [ ] A requirement list is not mistaken for a complete solution design.
- [ ] The recommended next step is the lightest safe workflow.
- [ ] For Level 3, the response recommends `$analyzing-cybernetic-requirements`, then `$designing-cybernetic-solutions` when Design Gate is required, then `$orchestrating-cybernetic-pregoal`.
- [ ] For Level 0/1/2, the response does not recommend full pre-goal pipeline.
- [ ] For Level 2 bounded file goals, the response does not recommend execution policy by default.
- [ ] If Rubric Gate is required, the response recommends rubric analysis before execution.
- [ ] If Output Contract Gate is required, the response routes output-contract definition through requirements analysis and solution design only when structure synthesis is needed.
- [ ] If Design Gate is required, the response recommends solution design before goal writing or orchestration.
- [ ] The response includes rejected workflow rationale.
