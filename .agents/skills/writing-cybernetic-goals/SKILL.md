---
name: writing-cybernetic-goals
description: 'Use when confirmed requirements and any required design exist and goal.control.json must be written for a bounded_runtime or controlled_run.'
---

# Writing Cybernetic Goals

## Overview

Write the goal contract from confirmed requirements and any required design.

This skill does not analyze requirements, design the solution, write execution
policy, review, compile runtime, or execute target work.

Detailed rules live in `references/goal-writing-detailed-rules.md` and
`references/control-contract-rules.md`.

## Runtime Limit

`goal.control.json` is not the user-entered runtime `/goal`. Runtime execution
must use either:

- `using-bounded-control-json` for `bounded_runtime`; or
- `using-control-json` for compiled JSON pre-goal runs.

The user-entered `/goal` must stay pointer-only.

## Goal Modes

### Mode A: Complex Control Contract

Use for `controlled_run` JSON pre-goal orchestration. Requires approved
requirements and any required design.

Output:

```text
docs/cybernetics/runs/<slug>/goal.control.json
```

The goal must preserve `What the User Approved`, source requirements, required
outcomes, non-goals, authority, evidence, and final answer format.

### Mode B: Bounded File Goal / Audit Goal

Use for `bounded_runtime` work with fixed meaning.

Output:

```text
docs/cybernetics/runs/<slug>/goal.control.json
docs/cybernetics/runs/<slug>/runtime.control.json
```

The direct runtime pointer uses `.agents/skills/using-bounded-control-json`.
This mode does not require requirements/design/plan/review.

## Required Goal Content

For complex goal control, include:

- objective;
- human purpose;
- source of truth;
- rules that cannot change;
- required outcomes;
- what counts as done;
- where the result must show up;
- final answer format;
- work covered and allowed actions;
- forbidden live or irreversible actions;
- stop conditions.

For bounded goals, include:

- fixed objective;
- bounded scope;
- allowed and forbidden actions;
- required steps;
- evidence required;
- verifier command.

## Checks

Evaluation tasks need an explicit rubric before goal writing. Output-sensitive
tasks need final answer format. Multi-place result tasks need result placement.
If any of these are missing, return to requirements or design instead of
guessing.

## Output Format

For complex goal control, output:

```markdown
Created or updated goal:
`docs/cybernetics/runs/YYYY-MM-DD-slug/goal.control.json`

Status:
- `approved` / `candidate` / `blocked`

Response-only next step:
- return to `$orchestrating-cybernetic-pregoal`, or
- if manual fallback is being used, continue to `$writing-cybernetic-execution-policies`.
```

For bounded JSON goal, output the pointer:

```text
/goal Use .agents/skills/using-bounded-control-json and execute docs/cybernetics/runs/YYYY-MM-DD-slug/runtime.control.json. If the bounded JSON is missing, invalid, inconsistent, or insufficient, stop and report the smallest required human decision.
```

Do not write conversational next-step prompts into goal control JSON.

## Validation Checklist

- [ ] Requirements and any required design exist.
- [ ] Controlled runs have `What the User Approved: Approved`.
- [ ] Goal does not weaken source requirements.
- [ ] Runtime `/goal` is pointer-only.
- [ ] `bounded_runtime` mode points to `using-bounded-control-json`.
- [ ] Complex mode does not let runtime write its own plan.
- [ ] Missing rubric/design/output requirements are routed upstream.
