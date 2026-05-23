# Superpowers Infrastructure Policy

## Purpose

Superpowers are infrastructure substrates for the cybernetic skill chain.

Cybernetic skills compile control structures: clarification, goal contracts, execution policies, control reviews, and runtime `/goal` commands. Superpowers provide the lower-level behavior protocols for planning, independent review discipline, runtime execution, debugging, and verification.

## Stage Dependency Matrix

| Stage | Required substrate | Required? | Notes |
|---|---|---:|---|
| Product/design-heavy clarification | `$superpowers:brainstorming` | Optional | Use for exploratory product/design clarification, not simple rubric clarification. |
| Execution policy generation | `$superpowers:writing-plans` | Required for non-trivial implementation plans | Cybernetic execution-policy skills provide semantic invariants, tactical freedom, dependency matrix, batch cadence, sensor governance, and stale-test policy as inputs. |
| Control structure review | Independent subagent review discipline | Required for `Approved` unless explicit human approval exists | This is review discipline, not the full implementation workflow from `$superpowers:subagent-driven-development`. |
| Runtime execution | `$superpowers:executing-plans` discipline | Required | Execute the approved plan; do not create or approve a new plan at runtime. |
| Runtime debugging | `$superpowers:systematic-debugging` | Required for unclear or repeated failures | Investigate before changing behavior. |
| Completion claim | `$superpowers:verification-before-completion` | Required | Completion requires fresh verification evidence. |

## Non-Substitution Rule

If a required substrate is unavailable, stop and report the missing infrastructure.

Do not silently replace:

- `$superpowers:writing-plans` with ad hoc plan writing;
- independent subagent review with self-review;
- `$superpowers:executing-plans` with runtime replanning;
- `$superpowers:systematic-debugging` with speculative fixes;
- `$superpowers:verification-before-completion` with confidence statements.

## Subagent Authorization Rule

Subagents require explicit user authorization.

If subagents are not authorized, pre-goal orchestration may produce candidate artifacts, but control review must be marked `Needs Independent Review` unless explicit human approval or another independent reviewer is already present.

## Pre-goal Boundary

Required Superpowers infrastructure must run before `/goal` execution when it affects the control structure.

Runtime `/goal` execution must not create, approve, or rewrite its own control structure.

## Runtime Discipline

Compiled runtime `/goal` commands must instruct Codex to use:

- `$superpowers:executing-plans` discipline for execution against the approved plan;
- `$superpowers:systematic-debugging` for unclear or repeated failures;
- `$superpowers:verification-before-completion` before claiming completion.

If runtime cannot load those skills, it must follow equivalent discipline already written into the approved plan and control review.
