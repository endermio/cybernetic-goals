---
name: writing-cybernetic-goals
description: 'Use when confirmed requirements and any required design exist and a control contract must be written for a Level 2 bounded goal or Level 3/4 full pre-goal orchestration. For Level 3/4, Human Setpoint Approval is required.'
---

# Writing Cybernetic Goals

## Overview

Create a control contract from confirmed semantics and any required solution design.

This skill writes the control contract. It does not analyze requirements, write execution policies, review control structures, or execute target work.

For complex work, the output is:

```text
docs/cybernetics/goals/YYYY-MM-DD-<slug>.md
```

Use `assets/goal-contract-template.md`.

## Runtime Boundary

For complex controlled work, this skill must not produce an executable `/goal` command unless any required solution design exists and an approved execution policy and approved control review already exist.

If `Design Gate: required`, do not create the final complex goal contract until a solution design exists or the human explicitly says the Design Gate is unnecessary.

For Level 3, Level 4, or full pre-goal work, stop after creating the goal contract and hand off back to `$orchestrating-cybernetic-pregoal` when it is available or already owns the chain.

Recommend `$writing-cybernetic-execution-policies` or `$reviewing-cybernetic-control-structures` directly only when the user explicitly chose a manual pre-goal chain or `$orchestrating-cybernetic-pregoal` is unavailable.

For Level 3, Level 4, or full pre-goal work, do not create the goal contract unless the requirements analysis contains `Human Setpoint Approval: Approved`, or the current user message explicitly approves the compact control commitment. Human answers to requirements questions are inputs, not approval.

If the current user message approves the compact control commitment, update the requirements analysis `Human Setpoint Approval` section first, quoting or referencing that approval, then continue. Do not rely on in-memory approval to pass orchestration or runtime guards.

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

## Output Contract Gate

Before creating a goal, check whether the final output contract is explicit enough that runtime Codex will not invent the audience, purpose, medium, structure, detail level, destination, evidence-reference requirements, or machine-readable shape.

For simple bounded work, use a safe default and do not ask output-format questions by default:

- short chat summary for simple direct tasks;
- markdown file for persistent control artifacts;
- evidence table for bounded audit/evaluation tasks;
- final report with summary, evidence, and unresolved items for runtime tasks.

For output-sensitive work, the goal must include `## Final Output Contract`.

The `Final Output Contract` must preserve:

- audience;
- purpose;
- medium;
- required structure;
- detail level;
- evidence-reference needs;
- machine-readable needs;
- destination path;
- acceptance condition.

If requirements or solution design define a structured output, copy the substance into the goal and forbid runtime substitution. If the output contract affects execution or acceptance and no safe default exists, stop and route the missing decision back to requirements analysis or solution design.

## Purpose Feedback Contract

The goal's success condition must describe purpose achievement, not merely
sensor success.

Do not define success as internal sensor success unless the human purpose is internal-state correctness.

The goal must preserve or define:

- Purpose-realizing outcome observed: what must be observed for the human purpose to count as achieved;
- Supporting Evidence: internal checks, scripts, lint, API smoke, reports, or other sensors that support progress but do not alone prove purpose achievement unless justified;
- Purpose feedback status wording: how runtime should report achieved, partially observed, pending, unavailable, or not-required purpose feedback.

When requirements analysis includes a `Purpose Feedback Boundary`, preserve it
in the goal as the `Purpose Feedback Contract`.

## Realization Surface Contract

When requirements analysis or solution design defines Realization Surface
Closure, preserve it in the goal as `Realization Surface Contract`.

For any goal that may be passed to the runtime compiler, include a compact
`Realization Surface Contract`; it is always for compiled runtime goals. If no
target-state surface closure is required, record `RSC not applicable with
justification`.

The goal must preserve or define:

- Target state: the state or semantic change that must be realized;
- Required surfaces: the surface model or classes that carry target-state
  realization;
- Surface actions: whether each surface class must be acted on, inspected,
  preserved, excluded, or discovered;
- Residual reconciliation: how old state, unknown surfaces, exclusions,
  preserved surfaces, and remaining mismatches will be accounted for;
- RSC status wording: the strongest positive target-realization claim requires RSC adequate;
- Partial/unavailable handling: runtime must report partial, missing,
  unavailable, or not applicable with justification when RSC is not adequate;
- RSC / PFB boundary: RSC calibrates target-state and surface-closure claims,
  while Purpose Feedback Boundary calibrates human-purpose realization claims.

RSC is distinct from Purpose Feedback Boundary. RSC calibrates target-state and
surface-closure claims. Purpose Feedback Boundary calibrates human-purpose
realization claims.

## Goal Modes

### Mode A: Complex Control Contract

Use when the task is Level 3/4, a complex execution, or would require runtime Codex to coordinate execution policy, phase gates, sensor governance, or multi-batch execution strategy.

Behavior:

1. Check whether `Design Gate: required`.
2. If required, confirm `docs/cybernetics/designs/YYYY-MM-DD-<slug>.md` or an explicit design source exists.
3. Create the goal contract under `docs/cybernetics/goals/YYYY-MM-DD-<slug>.md`.
4. Do not output an executable `/goal` unless an approved execution policy and approved control review already exist.
5. Use the route-appropriate response-only handoff: return to `$orchestrating-cybernetic-pregoal` for full pre-goal work, or recommend `$writing-cybernetic-execution-policies` only for an explicit manual chain.

### Mode B: Bounded File Goal / Audit Goal

Use when `$routing-cybernetic-workflows` selected Level 2, or the user explicitly asks for a small file goal, bounded audit goal, or bounded repair goal with fixed semantics.

Signals:

- task semantics are already fixed by the user or existing artifacts;
- no structure contract, authorization boundary, external contract, or requirement semantics need to be decided;
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
8. If the bounded goal proves insufficient, ambiguous, or dependent on new requirement/control decisions, instruct runtime Codex to stop and report the smallest required human decision.

## Preconditions

Before creating a goal contract for complex work, check:

- a requirements analysis brief exists;
- `Requirements Analysis Status` is `Complete` or the user explicitly states the semantics are confirmed;
- for Level 3/4 or full pre-goal work, `Human Setpoint Approval: Approved` is present unless the current user message explicitly approves the compact control commitment;
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
4. Purpose Feedback Contract
5. Realization Surface Contract, always for compiled runtime goals; record `RSC not applicable with justification` when no target-state surface closure is required
6. Source of Truth
7. Scope and Boundaries
8. Invariants
9. Verification Surface
10. Checkpoint Loop
11. Repair Policy
12. Progress Log
13. Stop Conditions
14. Blocked Report Format
15. Final Report Format
16. Final Output Contract, when output shape affects execution, acceptance, handoff, persistence, or downstream consumption

The goal must preserve confirmed semantics. It must not reinterpret or downscope them.

For Level 3/4 or full pre-goal work, the goal must preserve the approved compact control commitment from `Human Setpoint Approval`: human purpose, input role binding, primary object, requested transformation, non-goals, Purpose Feedback Boundary, Realization Surface Closure, Output Contract, workflow fit, and known assumptions.

When a solution design is present, the goal must reference it under `Source of Truth`, preserve design invariants, and avoid freezing tactical design details as semantic invariants unless the design explicitly marks them as invariant.

When a requirements analysis or solution design contains an output contract, the goal must preserve it under `Final Output Contract` and prevent runtime from substituting another output shape.

For evaluation goals, the goal must also include the confirmed rubric as the error function: status definitions, evidence levels, strongest-positive evidence threshold, downgrade rules, and unobservable/external-dependency handling.

## Control Map

Map requirements analysis to:

- Objective: observable target state
- Sensors: approved sensors, checks, evidence channels, and reviews
- Purpose feedback: purpose-realizing outcome, beneficiary/observer boundary, sufficient evidence level, and allowed completion wording
- Realization surface closure: target state, required surfaces, RSC status wording, residual reconciliation, and target-realization claim calibration
- Error function: rubric for interpreting sensor output when the task is evaluative
- Output contract: final audience, purpose, medium, structure, detail level, evidence references, destination, and acceptance condition
- Constraints: invariants and non-goals
- Stop conditions: when Codex must stop and report the missing decision

## Output Format

These output formats are response-only. The direct `/goal` command must be returned to the user in the assistant response, not written into the goal file. Goal files must not contain conversational next-step prompts.

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
- Final output: ...

Response-only handoff:
- For Level 3/4 or full pre-goal work: return to `$orchestrating-cybernetic-pregoal` with this goal path.
- For an explicit manual chain only: use `$writing-cybernetic-execution-policies` to create the execution policy.
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
- Final output: ...

Response-only `/goal` command:

```text
/goal Execute the bounded file goal in docs/cybernetics/goals/YYYY-MM-DD-slug.md as the controlling contract. Do not create an execution policy or control review unless explicitly instructed. Do not reinterpret scope, expand requirements, or modify files outside the goal boundaries. If the goal is insufficient, ambiguous, or requires new requirement/control decisions, stop and report the smallest required human decision.
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

Response-only handoff:

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

Response-only handoff:

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
- [ ] The goal includes Purpose Feedback Contract when requirements define Purpose Feedback Boundary or purpose-achievement evidence is non-obvious.
- [ ] The goal includes Realization Surface Contract for compiled runtime goals; direct bounded goals include it when requirements define Realization Surface Closure or target-state realization spans surfaces.
- [ ] For Level 3/4 or full pre-goal work, Human Setpoint Approval is Approved before the goal is written.
- [ ] Success Condition is Purpose-realizing outcome observed, not internal sensor success unless the human purpose is internal-state correctness.
- [ ] Any strongest positive target-realization claim requires RSC adequate; partial, missing, unavailable, or not applicable with justification receives calibrated wording.
- [ ] Sensors are named but not treated as the objective.
- [ ] Evaluation tasks define an explicit rubric before any executable goal is emitted.
- [ ] Output-sensitive tasks include a `Final Output Contract`.
- [ ] The goal forbids runtime from substituting another output shape when a final output contract is specified.
- [ ] For complex work, no final runtime `/goal` was output unless approved plan and review exist.
- [ ] For Level 2 bounded file goals, the response outputs a direct `/goal` and does not recommend execution policy by default.
- [ ] Any bounded file `/goal` stops if the goal is insufficient, ambiguous, or requires new requirement/control decisions.
