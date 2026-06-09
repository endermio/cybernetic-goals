# Superpowers Infrastructure Policy

## Purpose

Superpowers are infrastructure workflows for the cybernetic skill chain.

Cybernetic skills compile solution designs and control structures: requirements analysis, solution designs, goal files, execution policies, reviews, and runtime `/goal` commands. Superpowers provide the lower-level behavior protocols for planning, independent review discipline, runtime execution, debugging, and verification.

## Stage Dependency Matrix

| Stage | Required workflow | Required? | Notes |
|---|---|---:|---|
| Exploratory requirements analysis | `$superpowers:brainstorming` | Optional | Use for exploratory requirements analysis, not simple rubric analysis. |
| Exploratory solution design | `$superpowers:brainstorming` | Optional | Use when solution structure needs exploration, not when objects, flows, and limits are already explicit. |
| Execution policy generation | `$superpowers:writing-plans` | Required for non-trivial execution policies | Cybernetic execution-policy skills provide semantic rules that cannot change, tactical freedom, dependency matrix, batch cadence, evidence check/evidence governance, and stale-evidence check policy as inputs. |
| Control structure review | Independent subagent review discipline | Required for `Approved` unless explicit human approval exists | This is review discipline, not the full execution workflow from `$superpowers:subagent-driven-development`. |
| Runtime execution | `$superpowers:executing-plans` discipline | Required | Execute the approved plan; do not create or approve a new plan at runtime. |
| Runtime target-work delegation | Approved bounded subagent delegation protocol | Required when execution policy selects serial or parallel subagent-driven work assignment | Main agent coordinates and integrates; delecheckd work packages stay bounded by the approved execution policy. |
| Runtime serial implementation-plan delegation | `$superpowers:subagent-driven-development` discipline | Conditional | Use only when the approved execution policy records `Selected agent workflow: superpowers-subagent-driven-development`, `Subagent execution mode: serial-single-active`, and `Max concurrent subagents: 1`. |
| Runtime parallel independent-domain delegation | `$superpowers:dispatching-parallel-agents` discipline | Conditional | Use only when the approved execution policy records `Selected agent workflow: superpowers-dispatching-parallel-agents`, `Subagent execution mode: parallel-max-safe`, and approved wave/lock/barrier/integration rules. |
| Runtime debugging | `$superpowers:systematic-debugging` | Required for unclear or repeated failures | Investicheck before changing behavior. |
| Completion claim | `$superpowers:verification-before-completion` | Required | Completion requires fresh verification evidence. |

## Non-Substitution Rule

If a required workflow is unavailable, stop and report the missing infrastructure.

When a required Superpowers skill applies, invoke it or load and follow its `SKILL.md` instructions. Merely mentioning the skill, citing it, or imitating generic behavior is not sufficient.

Do not silently replace:

- `$superpowers:writing-plans` with ad hoc plan writing;
- independent subagent review with self-review;
- `$superpowers:executing-plans` with runtime replanning;
- an approved bounded subagent delegation protocol with ad hoc context delegation when subagent-driven work assignment is selected;
- `$superpowers:subagent-driven-development` with generic subagent delegation, with parallel execution, or without `Selected agent workflow: superpowers-subagent-driven-development`;
- `$superpowers:dispatching-parallel-agents` as a substitute for `$superpowers:subagent-driven-development`'s implementer/spec-review/code-quality review loop;
- `$superpowers:systematic-debugging` with speculative fixes;
- `$superpowers:verification-before-completion` with confidence statements.

## Subagent Authorization Rule

Pre-goal review subagents and runtime target-work subagents use different authorization semantics.

Pre-goal review subagents require explicit authorization in the current orchestration request.

Without pre-goal review subagent authorization, pre-goal orchestration may produce candidate artifacts. Review status remains `Needs Independent Review` until explicit human approval or another independent reviewer is present.

Runtime target-work subagents are authorized only when the final `/goal` explicitly contains the approved subagent-driven execution work assignment and the user launches that `/goal`. Compiling or displaying the final `/goal` does not itself start runtime target-work subagents.

Parallel runtime subagents require explicit human approval recorded in the execution policy and review before the final `/goal` is compiled.

## Final Observer Rule

Approval requires a final observer pass after the last substantive mutation to the reviewed control artifacts.

If any control artifact changes after the latest independent review, including a required solution design, the review state becomes `Dirty` / `Needs Re-review` and cannot be `Approved` until an independent reviewer confirms no Blocking or Major findings on the changed artifact.

Mechanical recording of already-reviewed findings into the review file does not itself create a new review cycle. Substantive changes to the review's final decision, reviewer findings, approval rationale, or Final Independent Check after approval require re-review or explicit human approval.

Deterministic-only changes may skip subagent re-review only when the change is explicitly listed, a deterministic guard covers the condition and passes, and the review records that no semantic or control-policy content changed.

Lint PASS is a structural evidence check, not semantic approval.

## Pre-goal Limit

Required Superpowers infrastructure must run before `/goal` execution when it affects the control structure.

Runtime `/goal` execution must not create, approve, or rewrite its own control structure.

## Runtime Discipline

Compiled runtime `/goal` commands must instruct Codex to use:

- `$superpowers:executing-plans` discipline for execution against the approved plan;
- the approved bounded subagent delegation protocol when the approved execution policy selects serial or parallel subagent-driven work assignment;
- `$superpowers:subagent-driven-development` only when the approved execution policy records `Selected agent workflow: superpowers-subagent-driven-development`, `Subagent execution mode: serial-single-active`, and `Max concurrent subagents: 1`;
- `$superpowers:dispatching-parallel-agents` only when the approved execution policy records `Selected agent workflow: superpowers-dispatching-parallel-agents` and `Subagent execution mode: parallel-max-safe`;
- `$superpowers:systematic-debugging` for unclear or repeated failures;
- `$superpowers:verification-before-completion` before claiming completion.

If runtime cannot load those skills, it must follow equivalent discipline already written into the approved plan and review.
