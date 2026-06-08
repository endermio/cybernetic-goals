# Superpowers Infrastructure Policy

## Purpose

Superpowers are infrastructure substrates, not optional style suggestions.

Cybernetic skills compile control structures. Superpowers provide planning, execution, debugging, completion verification, and independent-review discipline.

## Stage Dependency Matrix

| Stage | Required substrate | Required? | Notes |
|---|---|---:|---|
| Exploratory requirements analysis | `$superpowers:brainstorming` | Optional | Do not use for simple rubric analysis unless exploration is requested. |
| Exploratory solution design | `$superpowers:brainstorming` | Optional | Use when the solution model needs exploration, not when objects, flows, and boundaries are already explicit. |
| Execution policy generation | `$superpowers:writing-plans` | Required for non-trivial execution policies | The cybernetic skill supplies control constraints to the planning substrate. |
| Control structure review | Independent subagent review discipline | Required for `Approved` unless explicit human approval exists | Do not run target execution or dispatch execution agents during pre-goal review. |
| Runtime execution | `$superpowers:executing-plans` discipline | Required | Execute approved artifacts only; do not create a new plan at runtime. |
| Runtime target-work delegation | Approved bounded subagent delegation protocol | Required when execution policy selects serial or parallel subagent-driven topology | Main agent coordinates and integrates; delegated work packages stay bounded by the approved execution policy. |
| Runtime serial implementation-plan delegation | `$superpowers:subagent-driven-development` discipline | Conditional | Use only when the approved execution policy records `Selected agent workflow: superpowers-subagent-driven-development`, `Subagent execution mode: serial-single-active`, and `Max concurrent subagents: 1`. |
| Runtime parallel independent-domain delegation | `$superpowers:dispatching-parallel-agents` discipline | Conditional | Use only when the approved execution policy records `Selected agent workflow: superpowers-dispatching-parallel-agents`, `Subagent execution mode: parallel-max-safe`, and approved wave/lock/barrier/integration rules. |
| Runtime debugging | `$superpowers:systematic-debugging` | Required for unclear or repeated failures | Do not random-walk fixes. |
| Completion claim | `$superpowers:verification-before-completion` | Required | No completion claim without recorded evidence. |

## Non-Substitution Rule

If a required substrate is unavailable, stop and report the missing infrastructure.

When a required Superpowers skill applies, invoke it or load and follow its `SKILL.md` instructions. Merely mentioning the skill, citing it, or imitating generic behavior is not sufficient.

Do not silently replace:

- `$superpowers:writing-plans` with ad hoc plan writing;
- independent subagent review discipline with self-review;
- `$superpowers:executing-plans` with runtime replanning;
- an approved bounded subagent delegation protocol with ad hoc context delegation when subagent-driven topology is selected;
- `$superpowers:subagent-driven-development` with generic subagent delegation, with parallel execution, or without `Selected agent workflow: superpowers-subagent-driven-development`;
- `$superpowers:dispatching-parallel-agents` as a substitute for `$superpowers:subagent-driven-development`'s implementer/spec-review/code-quality review loop;
- `$superpowers:systematic-debugging` with speculative fixes;
- `$superpowers:verification-before-completion` with confidence statements.

## Subagent Authorization Rule

Pre-goal review subagents and runtime target-work subagents use different authorization semantics.

Pre-goal review subagents require explicit authorization in the current orchestration request.

If pre-goal review subagents are not authorized:

- produce candidate artifacts when useful;
- mark control review status as `Needs Independent Review`;
- do not mark the control structure `Approved` unless explicit human approval or another independent reviewer already exists.

Runtime target-work subagents are authorized only when the final `/goal` explicitly contains the approved subagent-driven execution topology and the user launches that `/goal`. Compiling or displaying the final `/goal` does not itself start runtime target-work subagents.

Parallel runtime subagents require explicit human approval recorded in the execution policy and control review before the final `/goal` is compiled.

## Final Observer Rule

Approval requires a final observer pass after the last substantive mutation to the reviewed control artifacts.

If any control artifact changes after the latest independent review, including a required solution design, the review state becomes `Dirty` / `Needs Re-review` and cannot be `Approved` until an independent reviewer confirms no Blocking or Major findings on the changed artifact.

Mechanical recording of already-reviewed findings into the control review file does not itself create a new review cycle. Substantive changes to the review's final decision, reviewer findings, approval rationale, or Final Observer Check after approval require re-review or explicit human approval.

Deterministic-only changes may skip subagent re-review only when the change is explicitly listed, a deterministic guard covers the condition and passes, and the review records that no semantic or control-policy content changed.

Lint PASS is a structural sensor, not semantic approval.

## Pre-goal Boundary

Required Superpowers infrastructure must run before runtime `/goal` execution when it affects the control structure.

The runtime `/goal` must not create, approve, or rewrite its own control structure.

## Runtime Compilation Rule

Final runtime `/goal` commands must name the runtime disciplines:

- `$superpowers:executing-plans` for approved-plan execution;
- the approved bounded subagent delegation protocol when the approved execution policy selects serial or parallel subagent-driven topology;
- `$superpowers:subagent-driven-development` only when the approved execution policy records `Selected agent workflow: superpowers-subagent-driven-development`, `Subagent execution mode: serial-single-active`, and `Max concurrent subagents: 1`;
- `$superpowers:dispatching-parallel-agents` only when the approved execution policy records `Selected agent workflow: superpowers-dispatching-parallel-agents` and `Subagent execution mode: parallel-max-safe`;
- `$superpowers:systematic-debugging` for unclear or repeated failures;
- `$superpowers:verification-before-completion` before completion claims.

If runtime cannot load these skills, it must follow the equivalent discipline already written in the approved plan and control review.
