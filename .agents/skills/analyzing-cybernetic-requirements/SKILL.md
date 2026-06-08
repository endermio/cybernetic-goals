---
name: analyzing-cybernetic-requirements
description: 'Use when a formed task or task candidate has ambiguous requirement semantics, acceptance criteria, output shape, constraints, non-goals, risk, or required control gates. Use framing-cybernetic-intent first for pre-task intent.'
---

# Analyzing Cybernetic Requirements

## Overview

Turn a formed task or task candidate into a requirements analysis brief before it becomes a solution design, Codex `/goal`, execution policy, or target-work change.

This skill is a pre-goal control loop:

```text
formed task -> AI context scan -> requirement semantics -> rubric/output/gate analysis -> human decisions/defaults -> goal-ready requirements brief
```

Requirements analysis is broader than asking clarifying questions. Clarifying questions are one tool inside this skill. The output is not just answers to questions; it is the analyzed setpoint, constraints, evaluation function, and required gates.

Output:

- a concise requirements analysis response in chat, or
- a requirements analysis brief at `docs/cybernetics/requirements/YYYY-MM-DD-<slug>.md`.

Use `assets/requirements-analysis-template.md`.

## Core Boundary

This skill owns requirements analysis for formed tasks and task candidates.
Use `$framing-cybernetic-intent` first when the setpoint is still pre-task
intent: confusion, dissatisfaction, risk sense, failed experience, method
preference, or process distrust.

Owned analysis:

- extract human purpose;
- identify requirement objects, actors, terms, boundaries, and non-goals;
- classify success, failure, completion, closure, usability, readiness, or pass/fail semantics;
- identify the final output audience, purpose, medium, required structure level, detail level, evidence-reference needs, machine-readable needs, destination path, and acceptance condition;
- identify the Purpose Feedback Boundary: who can observe purpose realization, what outcome realizes the human purpose, what feedback can judge it, and what internal sensors can or cannot prove;
- identify the Realization Surface Closure boundary when target state must be realized across a controlled object: Target state, Realization surfaces, Required surface action, Residual reconciliation, and RSC status;
- identify the Execution Horizon and Authority boundary for full-route or multi-batch work: approved horizon, runtime authority, forbidden actions, unauthorized-action handling, and explicitly out-of-scope items;
- identify the target-producing path for target-achieving implementation work: one actor-centered path from initial state to the target-achieved predicate;
- prepare the Human Setpoint Approval compact control commitment for Level 3/4 or full pre-goal work: Human purpose, Input role binding, Primary object, Requested transformation, Non-goals, Purpose Feedback Boundary, Realization Surface Closure, Single target-achieved predicate, Target-producing evidence required, Non-achieved terminal report handling, Target-producing path, Execution horizon, Runtime authority, Forbidden live / irreversible actions, Required handling for unauthorized actions, Explicitly out-of-scope items, Output Contract, Workflow fit, and Known assumptions;
- identify constraints, invariants, assumptions, and stop conditions;
- decide whether Semantic, Rubric, Output Contract, Design, Goal Contract, Execution Policy, Control Review, or Risk gates are required;
- ask high-value human questions;
- record obvious defaults without blocking progress;
- recommend the appropriate handoff for Design Gate: direct `$designing-cybernetic-solutions` for bounded/manual chains, or `$orchestrating-cybernetic-pregoal` for Level 3/4 full pre-goal work.

Routed elsewhere:

- solution structure, interfaces, object structures, mechanism architecture, flows, report structures, output schemas, and lifecycle models go to `$designing-cybernetic-solutions`;
- goal contracts go to `$writing-cybernetic-goals`;
- execution policies go to `$writing-cybernetic-execution-policies`;
- whole-chain review goes to `$reviewing-cybernetic-control-structures`;
- runtime `/goal` compilation goes to `$compiling-cybernetic-runtime-goals`;
- target work starts only after an approved runtime `/goal`.

Requirement object lists are not solution designs. They name what the human is talking about; they do not prescribe mechanisms, interfaces, lifecycle, state flow, or execution batches.

## Preserve Requested Scope

Do not reduce, simplify, postpone, or replace the requested behavior merely because execution seems complex, risky, unstable, or hard.

Execution complexity may be recorded as execution risk, planning concern, evidence concern, or future realization challenge. It must not become the recommended default unless the human explicitly asks for a lower-risk scope.

## Ask Only High-Value Human Questions

Ask the human a question only if all are true:

1. The answer materially changes any Human Setpoint Approval compact control commitment field, including purpose feedback boundary, beneficiary/observer, sufficient evidence level, feedback-unavailable handling, realization surface closure, target state surface model, required surface action, residual reconciliation, preserved/excluded surfaces, target-achievement predicate, target-producing path, execution horizon, runtime authority, forbidden actions, unauthorized-action handling, or explicit out-of-scope items; or changes requirement semantics, evaluation rubric, output contract, visibility boundary, authorization model, external contract semantics, observer-visible behavior, downstream consumption, acceptance condition, or control boundaries.
2. There are at least two plausible business choices.
3. The correct answer cannot be safely inferred from the user request, existing source artifacts, or common requirement conventions.
4. A wrong default would be costly to reverse or would cause serious misalignment.

Do not ask the human about routine execution tactics, obvious resilience behavior, execution mechanics, or design details that belong in `$designing-cybernetic-solutions`.

Use `references/decision-levels.md` for decision classification.

## Human Setpoint Approval Rule

For Level 3, Level 4, or full pre-goal orchestration, `Requirements Analysis Status: Complete` is not sufficient to start downstream orchestration.

The requirements analysis must also include:

```text
Human Setpoint Approval: Approved
```

unless the user explicitly approves the compact control commitment in the current message.

If the current user message approves the compact control commitment, update the requirements analysis `Human Setpoint Approval` section first, quoting or referencing that approval, then continue. Do not rely on in-memory approval to pass orchestration or runtime guards.

Human answers to clarification questions are inputs, not approval. Do not infer approval from the user merely answering questions.

Before handoff to `$orchestrating-cybernetic-pregoal`, present a compact control commitment for approval. The commitment must include:

- Human purpose;
- Input role binding;
- Primary object;
- Requested transformation;
- Non-goals;
- Purpose Feedback Boundary;
- Realization Surface Closure;
- Single target-achieved predicate;
- Target-producing evidence required;
- Non-achieved terminal report handling;
- Target-producing path;
- Execution horizon;
- Runtime authority;
- Forbidden live / irreversible actions;
- Required handling for unauthorized actions;
- Explicitly out-of-scope items;
- Output Contract;
- Workflow fit;
- Known assumptions.

If the commitment is `Pending`, `Rejected`, or `Needs Revision`, keep the workflow at requirements analysis and ask the user to approve or revise the compact commitment. Do not route the user into design review, plan review, or artifact-by-artifact approval as a substitute for setpoint approval.

## Output Contract Gate

Output shape is part of the controlled requirement when the final artifact will be used for a decision, handoff, audit, record, downstream action, or machine consumption.

Requirements analysis must identify:

- audience;
- purpose;
- medium;
- required structure;
- detail level;
- evidence-reference needs;
- machine-readable needs;
- destination path;
- acceptance condition.

Mark `Output Contract Gate: required` when:

- the output will be consumed by another actor, reviewer, downstream agent, script, or external stakeholder;
- the task is audit, evaluation, reporting, classification, handoff, or persistent record work;
- the output must be persisted as an artifact;
- the output needs a table, schema, matrix, evidence index, structured report, or artifact bundle;
- multiple audiences need different summaries;
- a wrong output shape would make the task unusable or change how execution should proceed.

Mark `Output Contract Gate: satisfied` when the output contract is explicit enough to write the goal.

Mark `Output Contract Gate: not applicable` when:

- the user asks a simple question;
- a direct prompt or local correction only needs a short final note;
- the output shape is obvious, low-risk, and does not affect execution or acceptance.

Do not ask output-format questions by default for simple tasks. Use safe defaults:

- chat summary for simple direct tasks;
- markdown file for persistent control artifacts;
- evidence table for audit or evaluation tasks;
- final report with summary, evidence, and unresolved items for runtime tasks.

Ask the human only when the output contract changes execution or acceptance and no safe default exists.

Requirements analysis may record that structured output is needed. It must not design complex report schemas, field sets, matrix layouts, or artifact bundles; defer those to `$designing-cybernetic-solutions` when structure synthesis is required.

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
Strongest positive status requires direct workflow evidence or a successfully run runtime check.
Partial status means work products or unrun sensors exist, but direct path evidence is missing.
Negative status means only placeholders/plans exist, or no usable entrypoint exists.
Unknown/unverifiable status means external credentials, production-only environment, third-party service, or current environment prevents observation.
```

## Purpose Feedback Boundary

When a task exists to realize a human purpose, evidence must be selected and
interpreted by how well it observes purpose realization, not by how easy it is
to execute.

Requirements analysis must identify:

- Human purpose: what the human wants to change or understand;
- Beneficiary / observer: who can observe whether the purpose is realized;
- Purpose-realizing outcome: the observable change when the purpose is realized;
- Feedback needed: evidence that can judge purpose realization;
- Internal sensors role: what internal checks can and cannot prove;
- Sufficient evidence level: `internal`, `integration`, `purpose-boundary`, or `operational`;
- If feedback unavailable: honest status and the smallest next observation.

Internal sensors may support progress, diagnosis, and risk reduction, but they
must not be treated as purpose-achievement evidence unless the human purpose
itself is internal-state correctness.

## Realization Surface Closure

When a task changes or realizes target state across a controlled object,
requirements analysis must identify how the target state is carried and how
closure will be judged.

Requirements analysis must define:

- Target state: the state or semantic change to realize;
- Realization surfaces: the controlled-object surfaces that carry, expose,
  enforce, record, explain, or preserve the target state;
- Required surface action: act, inspect, preserve, exclude, or discover;
- Residual reconciliation: how old state, unknown surfaces, exclusions,
  preserved surfaces, and remaining mismatches will be accounted for;
- RSC status: `RSC adequate`, `RSC partial`, `RSC missing`,
  `RSC unavailable`, or `RSC not applicable with justification`.

RSC is distinct from Purpose Feedback Boundary. RSC calibrates target-state and
surface-closure claims. Purpose Feedback Boundary calibrates human-purpose
realization claims.

## Design Gate Boundary

This skill identifies whether Design Gate is required. It does not resolve it.

Mark `Design Gate: required` when:

- multiple reasonable solution structures exist;
- controlled objects, actors, roles, or relationships are not explicit enough for goal writing;
- system/process/organizational boundaries are unclear;
- information flow, state flow, evidence flow, or decision flow is unclear;
- interfaces, contracts, procedures, reports, events, or user interactions are unclear;
- a new abstraction must be introduced;
- an old concept must be replaced without letting old realization details define the requirement;
- several subsystems or roles must coordinate around one model;
- runtime execution would otherwise invent objects, boundaries, sensors, or flow.

When Design Gate is required, record the missing solution-model questions. Do not answer those questions inside the requirements analysis unless they are already confirmed human semantics.

For Level 1/2 bounded work or manual downstream chains, recommend `$designing-cybernetic-solutions` before goal writing.

For Level 3/4 or full pre-goal work, pass Design Gate to `$orchestrating-cybernetic-pregoal` and state that the orchestrator must invoke or request `$designing-cybernetic-solutions` before goal writing. Do not output a standalone `$designing-cybernetic-solutions` command as a separate pre-orchestration next step.

## Process

1. Inspect just enough context to avoid generic questions.
2. Restate the human purpose in task language.
3. Extract confirmed requirement semantics, terms, objects, boundaries, constraints, and non-goals.
4. Build a requirements control map: objective, controlled object, candidate sensors, actuators, constraints, disturbances, stop conditions.
5. If the task is evaluative, identify the rubric/error function and classify missing rubric elements as decisions.
6. Identify the Purpose Feedback Boundary and whether internal sensors are sufficient or only supporting evidence.
7. Identify the Realization Surface Closure boundary when target-state realization spans surfaces.
8. Identify output-contract needs and whether a safe default is sufficient.
9. For Level 3/4 or full pre-goal work, build or update the Human Setpoint Approval compact control commitment.
10. Identify required gates: Semantic, Rubric, Output Contract, Design, Goal Contract, Execution Policy, Control Review, Risk.
11. Classify uncertainty as blocking human decision, safe default assumption, or deferred design/planning/execution detail.
12. Ask 3-7 high-value questions, preferably no more than 5.
13. Create or update the requirements analysis brief.
14. If the human answers, update `Confirmed Requirement Decisions`, `Requirements Analysis Status`, and the Human Setpoint Approval record without treating answers as approval.
15. Do not create a solution design, goal, plan, control review, runtime `/goal`, or target-work artifacts.
16. If analysis is complete and the brief path deterministically identifies a date/slug, output the approval request or queue-friendly next commands as described below.

## Queue-Friendly Next Commands

When requirements analysis is complete, choose the next command from the intended workflow.

If requirements analysis is complete but Human Setpoint Approval is not Approved for Level 3/4 or full pre-goal work, do not output the orchestration command or predicted `/goal`.

Instead, output only the compact approval request:

```text
Human Setpoint Approval is Pending. Please approve or revise the compact control commitment before orchestration.
```

For Level 3/4 or full pre-goal work, when `Human Setpoint Approval: Approved` is recorded and the requirements path is deterministic, output:

1. A pre-goal orchestration command using the concrete requirements path.
2. The predicted runtime goal contract path and pointer-only `/goal` shape using the expected artifact paths for the same date/slug.

When available, generate both with:

```bash
python3 .agents/skills/analyzing-cybernetic-requirements/scripts/predict_pregoal_handoff.py \
  --requirements docs/cybernetics/requirements/YYYY-MM-DD-<slug>.md
```

Use the script output instead of hand-writing predicted runtime commands. The script checks `Requirements Analysis Status: Complete`, `Human Setpoint Approval: Approved`, deterministic path shape, Design Gate, and same-slug artifact paths.

If `Design Gate: required`, still output the predicted runtime contract path and pointer-only `/goal` shape. State that `$orchestrating-cybernetic-pregoal` must invoke or request `$designing-cybernetic-solutions` before goal writing, and make the predicted downstream artifact paths include the expected solution design path. Design Gate dispatch note must not replace the predicted pointer-only `/goal`. Do not output `$designing-cybernetic-solutions` as a standalone command before orchestration for Level 3/4 or full pre-goal work.

The predicted pointer-only `/goal` is not the final approved runtime command. Label it as predicted or queue-friendly, and make it point to the runtime goal contract that the pre-goal compiler must create after downstream artifacts are approved.

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
docs/cybernetics/runtime-goals/YYYY-MM-DD-<slug>.goal.md
```

The predicted pointer-only `/goal` shape must include this precondition:

```text
If any referenced artifact is missing, not approved, or inconsistent, stop and report the smallest required human decision.
```

Predicted commands and handoff prompts are response-only. Do not write them into the requirements analysis artifact.

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

For Level 3/4 or full pre-goal work, `Complete` only means requirement semantics are sufficiently analyzed. Downstream orchestration still requires `Human Setpoint Approval: Approved`.

## Output Format

Output examples in this section are response-only. Do not write `$skill ...` commands, runtime `/goal` prompts, or conversational next-step prompts into the requirements analysis artifact.

If a brief was created or updated:

Return a compact chat summary with:

- requirements analysis path;
- requirement status;
- blocking human decisions, if any;
- default assumptions;
- required gates;
- HSA status for Level 3/4 or full pre-goal work;
- response-only next action.

If all blocking decisions are resolved for full pre-goal work:

If `Human Setpoint Approval` is not `Approved`, output only:

```markdown
Requirements analysis is complete, but Human Setpoint Approval is pending.

Updated requirements analysis brief:
`docs/cybernetics/requirements/YYYY-MM-DD-slug.md`

Approve or revise the compact control commitment in the brief before orchestration.
```

If `Human Setpoint Approval: Approved`, output the predictor invocation and paste its response-only queue suggestions:

````markdown
Requirements analysis is complete.

Updated requirements analysis brief:
`docs/cybernetics/requirements/YYYY-MM-DD-slug.md`

Generated queue-friendly handoff:

```bash
python3 .agents/skills/analyzing-cybernetic-requirements/scripts/predict_pregoal_handoff.py \
  --requirements docs/cybernetics/requirements/YYYY-MM-DD-slug.md
```
````

For Level 1/2 work with `Rubric Gate: required`, summarize the confirmed rubric and output the bounded goal-writing handoff described in `Queue-Friendly Next Commands`.

## Validation Checklist

- [ ] Requirement semantics are separated from solution design and execution-policy writing.
- [ ] Evaluation predicates are treated as rubric/error-function semantics.
- [ ] Evaluation tasks define or ask for status meanings, evidence strength, strongest-positive threshold, downgrade rules, and external/unobservable handling.
- [ ] Design Gate is recorded as required, satisfied, or not applicable when solution structure matters.
- [ ] The response did not downscope because execution is hard.
- [ ] Uncertainty is classified into blocking decisions, default assumptions, deferred design, and deferred planning/execution.
- [ ] Obvious defaults are not asked as blocking questions.
- [ ] There are no more than 7 questions.
- [ ] The brief includes `Requirements Analysis Status`.
- [ ] Level 3/4 or full pre-goal work includes `Human Setpoint Approval`.
- [ ] Human answers to clarification questions are not treated as approval.
- [ ] If Human Setpoint Approval is not `Approved`, the response asks for approval or revision and does not output the orchestration command or predicted `/goal`.
- [ ] No solution design, goal, plan, control review, or approved runtime `/goal` was created.
- [ ] Level 1/2 work with `Rubric Gate: required` routes to `$writing-cybernetic-goals`, not full pre-goal orchestration by default.
- [ ] When the predictor script is available, Level 3/4 queue-friendly commands are generated with `.agents/skills/analyzing-cybernetic-requirements/scripts/predict_pregoal_handoff.py`.
- [ ] Any predicted queue-friendly `/goal` is clearly labeled as predicted and includes the missing/not-approved/inconsistent artifact precondition.
- [ ] For Level 3/4 or full pre-goal work, `Design Gate: required` is passed to `$orchestrating-cybernetic-pregoal`; requirements analysis does not output standalone `$designing-cybernetic-solutions` before orchestration.
