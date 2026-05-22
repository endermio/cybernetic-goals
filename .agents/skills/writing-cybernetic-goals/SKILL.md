---
name: writing-cybernetic-goals
description: 'Use after clarification is complete to create a Codex control contract. Converts confirmed human semantics into a goal file with objective, success conditions, constraints, sensors, stop conditions, and reporting format. For complex implementation work, does not output an executable /goal command unless an approved execution policy and approved control review already exist.'
---

# Writing Cybernetic Goals

## Overview

Create a control contract from a completed clarification brief.

This skill writes the goal contract. It does not clarify requirements, write execution policies, review control structures, or execute code.

For complex work, the output is:

```text
docs/superpowers/goals/YYYY-MM-DD-<slug>.md
```

Use `assets/goal-contract-template.md`.

## Runtime Boundary

For complex implementation work, this skill must not produce an executable `/goal` command unless an approved execution policy and approved control review already exist.

If no approved execution policy exists, stop after creating the goal contract and instruct the user to use `$writing-cybernetic-execution-policies`.

If no approved control review exists, instruct the user to use `$reviewing-cybernetic-control-structures`.

Do not put “first write a plan, then execute it” inside an execution `/goal` for complex work.

## Preconditions

Before creating a goal contract for complex work, check:

- a clarification brief exists;
- `Clarification Status` is `Complete` or the user explicitly states the semantics are confirmed;
- confirmed decisions are recorded;
- no blocking human decision remains unresolved.

If the clarification is missing or incomplete, route back to `$clarifying-cybernetic-tasks`.

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

After creating the goal file:

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

If the user explicitly requests a small inline `/goal` and the task is low-risk, you may output an inline `/goal`.

## Validation Checklist

- [ ] Confirmed semantics are preserved.
- [ ] No unresolved human decisions are silently assumed.
- [ ] The goal contract does not contain instructions to write and approve a plan during runtime.
- [ ] The goal file references the clarification brief.
- [ ] Success conditions and stop conditions are explicit.
- [ ] Sensors are named but not treated as the objective.
- [ ] For complex work, no final runtime `/goal` was output unless approved plan and review exist.
