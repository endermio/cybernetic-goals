# Superpowers Infrastructure Policy

## Purpose

Superpowers are infrastructure substrates, not optional style suggestions.

Cybernetic skills compile control structures. Superpowers provide planning, execution, debugging, completion verification, and independent-review discipline.

## Stage Dependency Matrix

| Stage | Required substrate | Required? | Notes |
|---|---|---:|---|
| Product/design-heavy clarification | `$superpowers:brainstorming` | Optional | Do not use for simple rubric clarification unless exploration is requested. |
| Execution policy generation | `$superpowers:writing-plans` | Required for non-trivial implementation plans | The cybernetic skill supplies control constraints to the planning substrate. |
| Control structure review | Independent subagent review discipline | Required for `Approved` unless explicit human approval exists | Do not run implementation or dispatch implementer agents during pre-goal review. |
| Runtime execution | `$superpowers:executing-plans` discipline | Required | Execute approved artifacts only; do not create a new plan at runtime. |
| Runtime debugging | `$superpowers:systematic-debugging` | Required for unclear or repeated failures | Do not random-walk fixes. |
| Completion claim | `$superpowers:verification-before-completion` | Required | No completion claim without recorded evidence. |

## Non-Substitution Rule

If a required substrate is unavailable, stop and report the missing infrastructure.

When a required Superpowers skill applies, invoke it or load and follow its `SKILL.md` instructions. Merely mentioning the skill, citing it, or imitating generic behavior is not sufficient.

Do not silently replace:

- `$superpowers:writing-plans` with ad hoc plan writing;
- independent subagent review discipline with self-review;
- `$superpowers:executing-plans` with runtime replanning;
- `$superpowers:systematic-debugging` with speculative fixes;
- `$superpowers:verification-before-completion` with confidence statements.

## Subagent Authorization Rule

Subagents require explicit user authorization.

If subagents are not authorized:

- produce candidate artifacts when useful;
- mark control review status as `Needs Independent Review`;
- do not mark the control structure `Approved` unless explicit human approval or another independent reviewer already exists.

## Final Observer Rule

Approval requires a final observer pass after the last substantive artifact mutation.

If any control artifact changes after the latest independent review, the review state becomes `Dirty` / `Needs Re-review` and cannot be `Approved` until an independent reviewer confirms no Blocking or Major findings on the changed artifact.

Deterministic-only changes may skip subagent re-review only when the change is explicitly listed, a deterministic guard covers the condition and passes, and the review records that no semantic or control-policy content changed.

Lint PASS is a structural sensor, not semantic approval.

## Pre-goal Boundary

Required Superpowers infrastructure must run before runtime `/goal` execution when it affects the control structure.

The runtime `/goal` must not create, approve, or rewrite its own control structure.

## Runtime Compilation Rule

Final runtime `/goal` commands must name the runtime disciplines:

- `$superpowers:executing-plans` for approved-plan execution;
- `$superpowers:systematic-debugging` for unclear or repeated failures;
- `$superpowers:verification-before-completion` before completion claims.

If runtime cannot load these skills, it must follow the equivalent discipline already written in the approved plan and control review.
