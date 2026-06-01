# Superpowers Infrastructure Policy

## Purpose

Superpowers are infrastructure substrates for the cybernetic skill chain.

Cybernetic skills compile solution designs and control structures: requirements analysis, solution designs, goal contracts, execution policies, control reviews, and runtime `/goal` commands. Superpowers provide the lower-level behavior protocols for planning, independent review discipline, runtime execution, debugging, and verification.

## Stage Dependency Matrix

| Stage | Required substrate | Required? | Notes |
|---|---|---:|---|
| Exploratory requirements analysis | `$superpowers:brainstorming` | Optional | Use for exploratory requirements analysis, not simple rubric analysis. |
| Exploratory solution design | `$superpowers:brainstorming` | Optional | Use when solution structure needs exploration, not when objects, flows, and boundaries are already explicit. |
| Execution policy generation | `$superpowers:writing-plans` | Required for non-trivial execution policies | Cybernetic execution-policy skills provide semantic invariants, tactical freedom, dependency matrix, batch cadence, sensor/evidence governance, and stale-sensor policy as inputs. |
| Control structure review | Independent subagent review discipline | Required for `Approved` unless explicit human approval exists | This is review discipline, not the full execution workflow from `$superpowers:subagent-driven-development`. |
| Runtime execution | `$superpowers:executing-plans` discipline | Required | Execute the approved plan; do not create or approve a new plan at runtime. |
| Runtime target-work delegation | Approved bounded subagent delegation protocol | Required when execution policy selects serial or parallel subagent-driven topology | Main agent coordinates and integrates; delegated work packages stay bounded by the approved execution policy. |
| Runtime implementation-plan delegation | `$superpowers:subagent-driven-development` discipline | Conditional | Use only when the approved execution policy explicitly selects it for implementation-plan, current-session work packages that fit that workflow. |
| Runtime debugging | `$superpowers:systematic-debugging` | Required for unclear or repeated failures | Investigate before changing behavior. |
| Completion claim | `$superpowers:verification-before-completion` | Required | Completion requires fresh verification evidence. |

## Non-Substitution Rule

If a required substrate is unavailable, stop and report the missing infrastructure.

When a required Superpowers skill applies, invoke it or load and follow its `SKILL.md` instructions. Merely mentioning the skill, citing it, or imitating generic behavior is not sufficient.

Do not silently replace:

- `$superpowers:writing-plans` with ad hoc plan writing;
- independent subagent review with self-review;
- `$superpowers:executing-plans` with runtime replanning;
- an approved bounded subagent delegation protocol with ad hoc context delegation when subagent-driven topology is selected;
- `$superpowers:subagent-driven-development` with generic subagent delegation for work that does not fit that implementation-plan, current-session workflow;
- `$superpowers:systematic-debugging` with speculative fixes;
- `$superpowers:verification-before-completion` with confidence statements.

## Subagent Authorization Rule

Subagents require explicit user authorization.

If subagents are not authorized, pre-goal orchestration may produce candidate artifacts, but control review must be marked `Needs Independent Review` unless explicit human approval or another independent reviewer is already present.

## Final Observer Rule

Approval requires a final observer pass after the last substantive mutation to the reviewed control artifacts.

If any control artifact changes after the latest independent review, including a required solution design, the review state becomes `Dirty` / `Needs Re-review` and cannot be `Approved` until an independent reviewer confirms no Blocking or Major findings on the changed artifact.

Mechanical recording of already-reviewed findings into the control review file does not itself create a new review cycle. Substantive changes to the review's final decision, reviewer findings, approval rationale, or Final Observer Check after approval require re-review or explicit human approval.

Deterministic-only changes may skip subagent re-review only when the change is explicitly listed, a deterministic guard covers the condition and passes, and the review records that no semantic or control-policy content changed.

Lint PASS is a structural sensor, not semantic approval.

## Pre-goal Boundary

Required Superpowers infrastructure must run before `/goal` execution when it affects the control structure.

Runtime `/goal` execution must not create, approve, or rewrite its own control structure.

## Runtime Discipline

Compiled runtime `/goal` commands must instruct Codex to use:

- `$superpowers:executing-plans` discipline for execution against the approved plan;
- the approved bounded subagent delegation protocol when the approved execution policy selects serial or parallel subagent-driven topology;
- `$superpowers:subagent-driven-development` only when the approved execution policy explicitly selects it for compatible implementation-plan, current-session work packages;
- `$superpowers:systematic-debugging` for unclear or repeated failures;
- `$superpowers:verification-before-completion` before claiming completion.

If runtime cannot load those skills, it must follow equivalent discipline already written into the approved plan and control review.
