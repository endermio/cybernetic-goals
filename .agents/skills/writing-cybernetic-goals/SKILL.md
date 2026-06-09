---
name: writing-cybernetic-goals
description: 'Use when confirmed requirements and any required design exist and goal.control.json must be written for a Level 2 bounded goal or Level 3/4 full pre-goal orchestration. For Level 3/4, What the User Approved is required.'
---

# Writing Cybernetic Goals

## Overview

Create `goal.control.json` from confirmed meaning and any required solution design.

This skill writes the goal control JSON. It does not analyze requirements, write execution policies, review approved work chains, or execute target work.

Official persistent control facts are JSON only. Historical Markdown may be read as non-authoritative background, but do not create or compile Markdown as official guard, compiler, runtime, or long-term dual-path control input.

For complex work, the output is:

```text
docs/cybernetics/runs/<slug>/goal.control.json
```

Use the approved goal control JSON shape for the run directory. Do not use Markdown templates as official control input.

## Runtime Limit

For complex controlled work, this skill must not produce an executable `/goal` command unless any required solution design exists and an approved execution policy and approved review already exist.

If `required design: required`, do not create final complex `goal.control.json` until a solution design exists or the human explicitly says the required design is unnecessary.

For Level 3, Level 4, or full pre-goal work, stop after creating `goal.control.json` and hand off back to `$orchestrating-cybernetic-pregoal` when it is available or already owns the chain.

Recommend `$writing-cybernetic-execution-policies` or `$reviewing-cybernetic-control-structures` directly only when the user explicitly chose a manual pre-goal chain or `$orchestrating-cybernetic-pregoal` is unavailable.

For Level 3, Level 4, or full pre-goal work, do not create `goal.control.json` unless the requirements analysis contains `What the User Approved: Approved`, or the current user message explicitly approves the compact control commitment. Human answers to requirements questions are inputs, not approval.

If the current user message approves the compact control commitment, update the requirements analysis `What the User Approved` section first, quoting or referencing that approval, then continue. Do not rely on in-memory approval to pass orchestration or runtime guards.

Do not put “first write a plan, then execute it” inside an execution `/goal` for complex work.

For Level 2 bounded goals, create `goal.control.json` and `runtime.control.json`, then output a short `/goal` pointer to `runtime.control.json` using `.agents/skills/using-control-json` only when the task limits and any required evaluation rubric are explicit. Do not recommend `$writing-cybernetic-execution-policies` or `$reviewing-cybernetic-control-structures` by default unless the user explicitly requests them or the task reveals unresolved control decisions.

## Evaluation Function Check

Before creating a bounded audit/evaluation/readiness/placement/completeness/usability/safety/stability/coverage/correctness goal, check whether the evaluation rubric is explicit.

Evaluation words include terms such as:

```text
闭环, 完成, 可用, 通过, 达标, 就绪, 用户视角, 质量好, 稳定, 安全, 合理, 充分, 覆盖, 一致, 正确, 可交付, 生产可用, 验收通过
```

A bounded evaluation goal may be created only if the source meaning define:

- status meanings or pass/fail categories;
- evidence levels or evidence strength;
- the minimum evidence needed for the strongest positive status;
- downgrade rules for partial, weak, missing, stale, or indirect evidence;
- handling for external credentials, production-only dependencies, third-party services, or currently unobservable behavior;
- whether confidence or evidence grade must be reported.

If the rubric is missing or partial, do not create an executable bounded goal and do not output a direct `/goal`. Return a blocked rubric analysis request instead. This is not a reason to recommend execution policy by default; the missing artifact is the evaluation function, not the execution policy.

## Final Answer Format Check

Before creating a goal, check whether the final final answer format is explicit enough that runtime Codex will not invent the audience, purpose, medium, structure, detail level, destination, evidence-reference requirements, or machine-readable shape.

For simple bounded work, use a safe default and do not ask output-format questions by default:

- short chat summary for simple direct tasks;
- markdown file for persistent approved files;
- evidence table for bounded audit/evaluation tasks;
- final report with summary, evidence, and unresolved items for runtime tasks.

For output-sensitive work, the goal must include `## Final Final Answer Format`.

The `Final Final Answer Format` must preserve:

- audience;
- purpose;
- medium;
- required structure;
- detail level;
- evidence-reference needs;
- machine-readable needs;
- destination path;
- acceptance condition.

If requirements or solution design define a structured output, copy the substance into the goal and forbid runtime substitution. If the final answer format affects execution or acceptance and no safe default exists, stop and route the missing decision back to requirements analysis or solution design.

## How We Know The User Purpose Was Met

The goal's success condition must describe purpose achievement, not merely
evidence check success.

Do not define success as internal evidence check success unless the human purpose is internal-state correctness.

The goal must preserve or define:

- Purpose-realizing outcome observed: what must be observed for the human purpose to count as achieved;
- Supporting Evidence: internal checks, scripts, lint, API smoke, reports, or other evidence checks that support progress but do not alone prove purpose achievement unless justified;
- Purpose feedback status wording: how runtime should report achieved, partially observed, pending, unavailable, or not-required purpose feedback.

When requirements analysis includes a `How We Know The User Purpose Was Met`, preserve it
in the goal as the `How We Know The User Purpose Was Met`.

## Where The Result Must Show Up

When requirements analysis or solution design defines result placement, preserve it in the goal as `Where The Result Must Show Up`.

For any goal that may be passed to the runtime compiler, include a compact
`Where The Result Must Show Up`; it is always for compiled runtime goals. If no
intended-result result placement is required, record `result placement not applicable with
justification`.

The goal must preserve or define:

- Intended result: the state or meaning change that must be realized;
- Required result places: the place model or classes that carry intended-result
  realization;
- Place actions: whether each place class must be acted on, inspected,
  preserved, excluded, or discovered;
- Residual reconciliation: how old state, unknown places, exclusions,
  preserved places, and remaining mismatches will be accounted for;
- Result-placement wording: the strongest positive result claim requires result-placement adequate;
- Partial/unavailable handling: runtime must report partial, missing,
  unavailable, or not applicable with justification when result-placement is not adequate;
- Distinction from user-purpose evidence: result placement calibrates intended-result and place-placement claims,
  while How We Know The User Purpose Was Met calibrates human-purpose realization claims.

result-placement is distinct from How We Know The User Purpose Was Met. result placement calibrates intended-result and
place-placement claims. How We Know The User Purpose Was Met calibrates human-purpose
realization claims.

## What Counts As Done

For compiled runtime goals, include `What Counts As Done`.

The goal must preserve or define:

- What counts as done: the only condition that allows `goal achieved: yes`;
- Evidence needed to call it done: what must be observed, produced, run, or measured;
- Allowed achieved claim: wording allowed only when the what counts as done is met;
- Steps that make the result true: the state-transition path or execution-policy required answer path that produces the condition.

not done report are stop/report protocol, not alternate goals,
what-counts-as-done conditions, or success states.

## Work Covered And Allowed Actions Contract

For full-route or multi-batch controlled work, include `Work Covered And
Allowed Actions Contract`.

The goal must preserve or define:

- Work covered in this run: the complete scope this goal covers;
- What the agent may do: what runtime may execute directly;
- Forbidden actions: live, remote, destructive, irreversible, or externally risky actions runtime must not execute;
- Prepare-only / observe-only actions: work items runtime may only prepare, observe, document, or report not executed;
- Explicitly out-of-scope items: items excluded by What the User Approved;
- Work coverage rule: how each work item is counted as executed, prepared-only, forbidden-not-executed, or explicitly out of scope by What the User Approved.

Authority limits must not shrink the work covered in this run or move work covered in this run
items to future roadmap.

## Goal Modes

### Mode A: Complex Control Contract

Use when the task is Level 3/4, a complex execution, or would require runtime Codex to coordinate execution policy, phase checks, evidence check governance, or multi-batch execution strategy.

Behavior:

1. Check whether `required design: required`.
2. If required, confirm `docs/cybernetics/runs/<slug>/design.control.json` or an explicit design source exists.
3. Create `docs/cybernetics/runs/<slug>/goal.control.json`.
4. Do not output an executable `/goal` unless an approved execution policy and approved review already exist.
5. Use the route-appropriate response-only handoff: return to `$orchestrating-cybernetic-pregoal` for full pre-goal work, or recommend `$writing-cybernetic-execution-policies` only for an explicit manual chain.

### Mode B: Bounded File Goal / Audit Goal

Use when `$routing-cybernetic-workflows` selected Level 2, or the user explicitly asks for a small file goal, bounded audit goal, or bounded repair goal with fixed meaning.

Signals:

- task meaning are already fixed by the user or existing artifacts;
- no structure contract, authorization limit, external contract, or requirement meaning need to be decided;
- the output is one bounded artifact such as an audit report, repair report, checklist, or small patch contract;
- audit/evaluation/status-classification goals include an explicit rubric;
- verification needs are moderate, but no separate execution policy or phase-check review is needed;
- the runtime agent must not expand scope or invent new control decisions.

Behavior:

1. Run the Evaluation Function Check for audit/evaluation/status-classification tasks.
2. If the rubric is missing or partial, stop with a blocked rubric analysis request.
3. Create `docs/cybernetics/runs/<slug>/goal.control.json`.
4. Create `docs/cybernetics/runs/<slug>/runtime.control.json` as the JSON-backed runtime pointer target.
5. Preserve the rubric inside the goal when the task is evaluative.
6. Output a short executable `/goal` command that references `runtime.control.json` and names `.agents/skills/using-control-json`.
7. Do not recommend execution policy or review by default.
8. If the bounded goal proves insufficient, ambiguous, or dependent on new requirement/control decisions, instruct runtime Codex to stop and report the smallest required human decision.

## Preconditions

Before creating goal control JSON for complex work, check:

- `requirements.control.json` exists;
- `Requirements Analysis Status` is `Complete` or the user explicitly states the meaning are confirmed;
- for Level 3/4 or full pre-goal work, `What the User Approved: Approved` is present unless the current user message explicitly approves the compact control commitment;
- confirmed decisions are recorded;
- required solution design exists, or the user explicitly says the required design is unnecessary;
- no blocking human decision remains unresolved.

If the requirements analysis is missing or incomplete, route back to `$analyzing-cybernetic-requirements`.

If required design is required and no design exists, route to `$designing-cybernetic-solutions`.

For bounded JSON goals, completed `requirements.control.json` is optional when the user request or router decision already fixes the meaning, limits, output path, stop conditions, and any evaluation rubric. Record the user request or router decision as the source of truth.

## Goal Control Requirements

`goal.control.json` must include the approved goal control facts for:

1. Human Purpose
2. Objective
3. Success Condition
4. How We Know The User Purpose Was Met
5. Where The Result Must Show Up, always for compiled runtime goals; record `result placement not applicable with justification` when no intended-result result placement is required
6. What Counts As Done
7. Work Covered And Allowed Actions Contract, always for full-route or multi-batch work
8. Source of Truth
9. Allowed And Forbidden Work
10. Rules That Must Not Change
11. Verification Place
12. Checkpoint Loop
13. Repair Policy
14. Progress Log
15. Stop Conditions
16. Blocked Report Format
17. Final Report Format
18. Final Final Answer Format, when output shape affects execution, acceptance, handoff, persistence, or downstream consumption

The goal control JSON must preserve confirmed meaning. It must not reinterpret or downscope them.

For Level 3/4 or full pre-goal work, the goal must preserve the approved compact control commitment from `What the User Approved`: human purpose, input role binding, primary object, requested transformation, non-goals, How We Know The User Purpose Was Met, result placement, What counts as done, Evidence needed to call it done, If it is not done, what should be reported, Required answer path, How this should be answered, What is not enough, Work covered in this run, What the agent may do, Forbidden live / irreversible actions, Required handling for unauthorized actions, Explicitly out-of-scope items, Final Answer Format, why this process is needed, and known assumptions.

If a design includes `Answer Method Check`, the goal must not weaken the approved answering method or substitute a different how this should be answered. Bind the what counts as done and required answer path to the required answer path.

When a solution design is present, the goal must reference it under `Source of Truth`, preserve design rules that cannot change, and avoid freezing tactical design details as meaning rules that cannot change unless the design explicitly marks them as rule.

When a requirements analysis or solution design contains an final answer format, the goal must preserve it under `Final Final Answer Format` and prevent runtime from substituting another output shape.

For evaluation goals, the goal must also include the confirmed rubric as the error function: status definitions, evidence levels, strongest-positive evidence threshold, downgrade rules, and unobservable/external-dependency handling.

## Control Map

Map requirements analysis to:

- Objective: observable intended result
- Evidence checks: approved evidence checks, checks, evidence channels, and reviews
- Purpose feedback: purpose-realizing outcome, beneficiary/observer limit, sufficient evidence level, and allowed completion wording
- Result placement: intended result, required places, Result-placement wording, residual reconciliation, and result claim calibration
- What counts as done: what counts as done, evidence needed to call it done, and allowed achieved claim
- Error function: rubric for interpreting evidence check output when the task is evaluative
- Output contract: final audience, purpose, medium, structure, detail level, evidence references, destination, and acceptance condition
- Constraints: rules that cannot change and non-goals
- Stop conditions: when Codex must stop and report the missing decision

## Output Format

These output formats are response-only. The direct `/goal` command must be returned to the user in the assistant response, not written into control JSON. Control JSON files must not contain conversational next-step prompts.

### Complex goal control

After creating complex goal control JSON:

```markdown
Created goal control JSON:

`docs/cybernetics/runs/YYYY-MM-DD-slug/goal.control.json`

Control map:
- Objective: ...
- Evidence checks: ...
- Constraints: ...
- Solution design source: ...
- Stop conditions: ...
- Final output: ...

Response-only handoff:
- For Level 3/4 or full pre-goal work: return to `$orchestrating-cybernetic-pregoal` with this goal path.
- For an explicit manual chain only: use `$writing-cybernetic-execution-policies` to create the execution policy.
```

### Bounded JSON goal

After creating a Level 2 bounded JSON goal:

````markdown
Created bounded goal control JSON:

`docs/cybernetics/runs/YYYY-MM-DD-slug/goal.control.json`

Runtime control JSON:

`docs/cybernetics/runs/YYYY-MM-DD-slug/runtime.control.json`

Control map:
- Objective: ...
- Evidence checks: ...
- Constraints: ...
- Stop conditions: ...
- Final output: ...

Response-only `/goal` command:

```text
/goal Use .agents/skills/using-control-json and execute docs/cybernetics/runs/YYYY-MM-DD-slug/runtime.control.json. If the JSON is missing, invalid, inconsistent, or insufficient, stop and report the smallest required human decision.
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

### Blocked design check

If complex goal writing is blocked because required design is missing:

````markdown
Goal file blocked: solution design required.

Reason:
- required design is required, but no solution design artifact or explicit design source was provided.

Response-only handoff:

```text
$designing-cybernetic-solutions 根据 docs/cybernetics/runs/YYYY-MM-DD-slug/requirements.control.json 创建 design.control.json。
```
````

If the user explicitly requests a small inline `/goal` and the task is low-risk, you may output an inline `/goal`.

## Validation Checklist

- [ ] Confirmed meaning are preserved.
- [ ] No unresolved human decisions are silently assumed.
- [ ] `goal.control.json` does not contain instructions to write and approve a plan during runtime.
- [ ] `goal.control.json` references `requirements.control.json`.
- [ ] If required design is required, `goal.control.json` references `design.control.json` or blocks before creating the final goal.
- [ ] The goal preserves design rules that cannot change without freezing tactical design details.
- [ ] Success conditions and stop conditions are explicit.
- [ ] The goal includes How We Know The User Purpose Was Met when requirements define How We Know The User Purpose Was Met or purpose-achievement evidence is non-obvious.
- [ ] The goal includes Where The Result Must Show Up for compiled runtime goals; direct bounded goals include it when requirements define result placement or intended-result realization spans places.
- [ ] The goal includes What Counts As Done for compiled runtime goals, including a required answer path reference.
- [ ] For Level 3/4 or full pre-goal work, What the User Approved is Approved before the goal is written.
- [ ] Success Condition allows `goal achieved: yes` only when the what counts as done is satisfied and user-purpose evidence/result-placement permit the matching achieved claims.
- [ ] Any strongest positive result claim requires result-placement adequate; partial, missing, unavailable, or not applicable with justification receives calibrated wording.
- [ ] Evidence checks are named but not treated as the objective.
- [ ] Evaluation tasks define an explicit rubric before any executable goal is emitted.
- [ ] Output-sensitive tasks include a `Final Final Answer Format`.
- [ ] The goal forbids runtime from substituting another output shape when a final final answer format is specified.
- [ ] For complex work, no final runtime `/goal` was output unless approved plan and review exist.
- [ ] For Level 2 bounded goals, the response outputs a short `/goal` pointer to `runtime.control.json` and does not recommend execution policy by default.
- [ ] Any bounded `/goal` stops if the runtime control JSON is insufficient, ambiguous, or requires new requirement/control decisions.
