---
name: writing-cybernetic-goals
description: 'Use after clarification is complete, when a router-selected Level 2 bounded task needs a small file goal, or when a low-risk task needs an inline goal. Applies when human semantics are confirmed and Codex needs a control contract before execution.'
---

# Writing Cybernetic Goals

## Overview

Create a control contract from confirmed semantics.

This skill writes the goal contract. It does not clarify requirements, write execution policies, review control structures, or execute code.

For complex work, the output is:

```text
docs/superpowers/goals/YYYY-MM-DD-<slug>.md
```

Use `assets/goal-contract-template.md`.

## Runtime Boundary

For complex implementation work, this skill must not produce an executable `/goal` command unless an approved execution policy and approved control review already exist.

If no approved execution policy exists for complex work, stop after creating the goal contract and instruct the user to use `$writing-cybernetic-execution-policies`.

If no approved control review exists for complex work, instruct the user to use `$reviewing-cybernetic-control-structures`.

Do not put “first write a plan, then execute it” inside an execution `/goal` for complex work.

For Level 2 bounded file goals, output a direct `/goal` command after creating the small goal file. Do not recommend `$writing-cybernetic-execution-policies` or `$reviewing-cybernetic-control-structures` by default unless the user explicitly requests them or the task reveals unresolved control decisions.

## Goal Modes

### Mode A: Complex Control Contract

Use when the task is Level 3/4, a complex implementation, or would require runtime Codex to coordinate execution policy, phase gates, sensor governance, or multi-batch implementation strategy.

Behavior:

1. Create the goal contract under `docs/superpowers/goals/YYYY-MM-DD-<slug>.md`.
2. Do not output an executable `/goal` unless an approved execution policy and approved control review already exist.
3. Recommend `$writing-cybernetic-execution-policies` as the next step when policy is missing.

### Mode B: Bounded File Goal / Audit Goal

Use when `$routing-cybernetic-workflows` selected Level 2, or the user explicitly asks for a small file goal, bounded audit goal, or bounded repair goal with fixed semantics.

Signals:

- task semantics are already fixed by the user or existing artifacts;
- no schema, permission, public API, or product semantics need to be decided;
- the output is one bounded artifact such as an audit report, repair report, checklist, or small patch contract;
- verification needs are moderate, but no separate execution policy or phase-gate review is needed;
- the runtime agent must not expand scope or invent new control decisions.

Behavior:

1. Create the small goal file under `docs/superpowers/goals/YYYY-MM-DD-<slug>.md`.
2. Make the goal file self-contained enough to execute directly.
3. Output a direct executable `/goal` command that references the small goal file.
4. Do not recommend execution policy or control review by default.
5. If the bounded goal proves insufficient, ambiguous, or dependent on new product/control decisions, instruct runtime Codex to stop and report the smallest required human decision.

## Preconditions

Before creating a goal contract for complex work, check:

- a clarification brief exists;
- `Clarification Status` is `Complete` or the user explicitly states the semantics are confirmed;
- confirmed decisions are recorded;
- no blocking human decision remains unresolved.

If the clarification is missing or incomplete, route back to `$clarifying-cybernetic-tasks`.

For bounded file goals, a completed clarification brief is optional when the user request or router decision already fixes the semantics, boundaries, output path, and stop conditions. Record the user request or router decision as the source of truth.

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

## Control Map

Map clarification to:

- Objective: observable product/code state
- Sensors: tests, builds, API smoke, screenshots, reviews
- Constraints: invariants and non-goals
- Stop conditions: when Codex must stop instead of guessing

## Output Format

### Complex control contract

After creating a complex goal file:

```markdown
Created goal contract:

`docs/superpowers/goals/YYYY-MM-DD-slug.md`

Control map:
- Objective: ...
- Sensors: ...
- Constraints: ...
- Stop conditions: ...

Next step:
Use `$writing-cybernetic-execution-policies` to create the approved execution policy.
```

### Bounded file goal

After creating a Level 2 bounded file goal:

````markdown
Created bounded file goal:

`docs/superpowers/goals/YYYY-MM-DD-slug.md`

Control map:
- Objective: ...
- Sensors: ...
- Constraints: ...
- Stop conditions: ...

Use this `/goal`:

```text
/goal Execute the bounded file goal in docs/superpowers/goals/YYYY-MM-DD-slug.md as the controlling contract. Do not create an execution policy or control review unless explicitly instructed. Do not reinterpret scope, expand requirements, or modify files outside the goal boundaries. If the goal is insufficient, ambiguous, or requires new product/control decisions, stop and report the smallest required human decision.
```
````

If the user explicitly requests a small inline `/goal` and the task is low-risk, you may output an inline `/goal`.

## Validation Checklist

- [ ] Confirmed semantics are preserved.
- [ ] No unresolved human decisions are silently assumed.
- [ ] The goal contract does not contain instructions to write and approve a plan during runtime.
- [ ] The goal file references the clarification brief.
- [ ] Success conditions and stop conditions are explicit.
- [ ] Sensors are named but not treated as the objective.
- [ ] For complex work, no final runtime `/goal` was output unless approved plan and review exist.
- [ ] For Level 2 bounded file goals, the response outputs a direct `/goal` and does not recommend execution policy by default.
- [ ] Any bounded file `/goal` stops if the goal is insufficient, ambiguous, or requires new product/control decisions.
