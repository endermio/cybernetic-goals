# Routing Response Shapes

These templates are formatting aids only. Choose the routing level from
`SKILL.md` core rules, checks, and downgrade pass before using a template.

## Level 0

```markdown
Routing decision: Level 0 - Direct Prompt

Why:
- ...

Required checks:
- None.

Recommended next step:
Use a direct prompt:

```text
...
```

Rejected workflow:
- Full cybernetic workflow would be heavier than the task.
```

## Level 1

```markdown
Routing decision: Level 1 - Inline Goal

Why:
- ...

Required checks:
- None, unless rubric check, final-answer-format check, or required design is required.

Recommended next step:
Use:

```text
$writing-cybernetic-goals 为这个明确小任务写 inline /goal：...
```
```

## Level 2

```markdown
Routing decision: Level 2 - Bounded File Goal / Bounded Repair

Why:
- Existing meaning are already fixed.
- No new structure/authorization/external-contract meaning appear required.
- The task is a bounded correction.

Required checks:
- None, or only checks already satisfied by confirmed inputs.

Rubric check:
- Not an evaluation task, or evaluation rubric is already explicit.

Design check:
- Satisfied or not applicable when solution structure is already fixed.

Output Contract check:
- Satisfied or not applicable when a simple response or confirmed artifact shape is enough.

Recommended next step:
Use a bounded repair prompt or small file-based goal:

```text
修正 <issue>，保持 <approved artifact paths or confirmed meaning> 不变；验证 <commands/artifacts>.
```

For a file-based goal:

```text
$writing-cybernetic-goals 为这个 Level 2 有界任务创建小型文件 goal，并在完成后给出直接 /goal 执行命令，不要默认建议 execution policy：...
```

Rejected workflow:
- Reject Level 3 because no new approved work chain is required.
- Do not recommend execution policy by default for Level 2; add required checks or upgrade only if unresolved control decisions appear.
```

## Level 2 With rubric check

```markdown
Routing decision: Level 2 - Bounded Audit

Why:
- Execution scope is bounded enough for a file goal.
- Requirement, structure-contract, authorization, and external-contract meaning do not need redesign.
- The evaluation function is not explicit enough for runtime execution.

Required checks:
- rubric check: required.
- final-answer-format check: required if the final report shape affects acceptance and is not explicit.

Rubric check:
- Missing or partial: status meanings, evidence strength, minimum evidence for the strongest positive status, downgrade rules, and external-dependency handling.

Recommended next step:
Use rubric analysis before goal writing:

```text
$analyzing-cybernetic-requirements 分析这个审计/评估任务的评价口径：...
```

Rejected workflow:
- Reject direct Level 2 execution because runtime Codex would invent the error function.
- Reject Level 3 unless broader requirement/control meaning are also unresolved.
```

## Level 2 With required design

```markdown
Routing decision: Level 2 - Bounded Design/Audit/Repair

Why:
- Execution scope is bounded enough for a small goal after design.
- Requirement, structure-contract, authorization, and external-contract meaning do not need redesign.
- The solution/report/evidence structure is not explicit enough for runtime execution.

Required checks:
- required design: required.
- rubric check: required if the task is evaluative and the rubric is not explicit.
- final-answer-format check: required if the final output audience, medium, structure, or acceptance condition is not explicit.

Design check:
- Missing or partial: objects/actors/roles, relationships, flow, limits, interfaces/contracts, or evidence model.

Recommended next step:
Use solution design before goal writing:

```text
$designing-cybernetic-solutions 根据 <requirements-path or confirmed request> 创建 solution design。
```

Rejected workflow:
- Reject direct Level 2 execution because runtime Codex would invent the solution model.
- Reject Level 3 unless broader control meaning are also unresolved.
```

## Level 3

```markdown
Routing decision: Level 3 - Full Pre-goal Pipeline

Why:
- ...

Required checks:
- Meaning Check: required.
- Goal Check: required.
- required design: required if solution structure is not explicit.
- final-answer-format check: required if final output shape affects execution, acceptance, handoff, persistence, or downstream consumption and is not explicit.
- execution-plan check: required.
- review check: required.
- rubric check: required if the task is evaluative and the rubric is not explicit.

Recommended next step:
1. `$analyzing-cybernetic-requirements <需求>`
2. After requirements analysis is complete and What the User Approved is Approved: `$orchestrating-cybernetic-pregoal 根据 <requirements-path> 完成 pre-goal 编译，允许使用 subagents review。`

If required design is required, keep it listed under Required checks. The orchestrator must invoke or request `$designing-cybernetic-solutions` before goal writing; do not list solution design as a separate manual step before orchestration for Level 3/4 work.

Rejected workflow:
- Level 0/1/2 would force runtime agent to invent unresolved control decisions.
```

## Level 4

```markdown
Routing decision: Level 4 - Human-Checkd Full Pipeline

Why:
- ...

Required checks:
- Full pre-goal checks: required.
- Explicit Human Approval Check: required before runtime execution.
- rubric check: required if the task is evaluative and the rubric is not explicit.
- required design: required if solution structure is not explicit.
- final-answer-format check: required if final output shape affects execution, acceptance, handoff, persistence, or downstream consumption and is not explicit.

Recommended next step:
Run the full pre-goal pipeline, but require explicit human approval before runtime `/goal`.

Rejected workflow:
- Do not allow uncheckd runtime execution.
```
