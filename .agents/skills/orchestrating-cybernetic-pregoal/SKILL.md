---
name: orchestrating-cybernetic-pregoal
description: 'Use after a completed clarification brief to orchestrate the pre-goal compilation chain before launching a Codex /goal. Coordinates existing cybernetic skills to create or update the goal contract, execution policy, control review, and final runtime /goal command. Requires explicit user authorization before spawning subagents. Does not implement code and does not start /goal execution.'
---

# Orchestrating Cybernetic Pre-goal

## Overview

This skill orchestrates the **pre-goal compilation chain** after requirements have been clarified.

It turns a completed clarification brief into approved control artifacts:

```text
clarification brief
  → goal contract
  → execution policy / plan
  → control-structure review
  → final runtime /goal command
```

This skill is a thin orchestrator. It does not replace the other cybernetic skills. It coordinates them.

## Core Boundary

This skill must not:

- clarify requirements from scratch
- implement code
- start `/goal` execution
- make product decisions for the human
- mark a control structure approved when semantic conflicts remain
- spawn subagents unless the user explicitly authorized subagents in the current request
- let `/goal` write or approve its own plan

This skill may:

- inspect a completed clarification brief
- call existing cybernetic skills in the correct order
- emulate narrow cybernetic formatting only when a downstream cybernetic skill is unavailable
- create or update control artifacts under `docs/superpowers/`
- use explicitly authorized subagents as independent reviewers
- iterate review and revision up to the configured limit
- compile the final `/goal` command after approval

## Required Infrastructure

Follow `$cybernetic-superpowers-infrastructure`.

This orchestrator may emulate cybernetic artifact formatting when a downstream cybernetic skill is unavailable. It must not emulate required Superpowers infrastructure.

Required infrastructure boundaries:

- non-trivial execution policy generation requires `$superpowers:writing-plans` as planning substrate;
- control review `Approved` requires independent review discipline or explicit human approval;
- control review `Approved` requires a final observer pass after the last substantive artifact mutation;
- runtime `/goal` compilation must include `$superpowers:executing-plans`, `$superpowers:systematic-debugging`, and `$superpowers:verification-before-completion` discipline.

If a required substrate is unavailable, stop and report the missing infrastructure. Do not self-substitute and do not mark the control structure `Approved`.

## Relationship to Other Skills

Use this skill after:

- `$routing-cybernetic-workflows` has recommended a Level 3 or Level 4 workflow, or the user explicitly chose full pre-goal compilation
- `$clarifying-cybernetic-tasks` has produced a completed clarification brief

This skill orchestrates:

- `$writing-cybernetic-goals`
- `$writing-cybernetic-execution-policies`
- `$reviewing-cybernetic-control-structures`
- `$compiling-cybernetic-runtime-goals`
- `$cybernetic-superpowers-infrastructure`

It should not duplicate their templates or rules unless they are unavailable. If a downstream cybernetic skill is available, prefer using it. If a downstream cybernetic skill is unavailable, emulate only its narrow cybernetic responsibility and state that the fallback was used.

Never emulate required Superpowers substrates. In particular:

- do not replace `$superpowers:writing-plans` with ad hoc internal planning for non-trivial implementation plans;
- do not replace independent review discipline with self-review;
- do not compile a runtime `/goal` that omits required runtime execution, debugging, and verification discipline.

## Required Input

A completed clarification brief, usually:

```text
docs/superpowers/clarifications/YYYY-MM-DD-<slug>.md
```

When the input path follows this pattern, the same `YYYY-MM-DD-<slug>` is the artifact identity for the whole pre-goal chain. Do not choose a different slug unless the user explicitly requests different output paths.

The user should invoke this skill with an explicit clarification path, for example:

```text
$orchestrating-cybernetic-pregoal 根据 docs/superpowers/clarifications/2026-05-22-collaborative-supervision.md 自动完成 pre-goal 编译。允许使用 subagents 做独立 review。若 review 无法收敛，停止并报告阻塞点。
```

## Subagent Authorization Rule

Do not spawn subagents unless the user explicitly authorizes subagents in the same request.

Phrases that count as authorization include:

- `允许使用 subagents`
- `可以使用 subagents`
- `use subagents`
- `spawn subagents`
- `use independent subagent reviewers`

If subagents are not authorized:

- You may create candidate goal and execution policy files.
- You may create a draft control review marked `Needs Independent Review`.
- You must not claim independent review or mark the control structure `Approved` unless a separate reviewer, explicit human approval, or an authorized subagent review exists.
- Ask the user to authorize subagent review or manually approve the artifacts before compiling a final runtime `/goal`.

## Pre-goal Orchestration Modes

### Mode A: Candidate-Only Mode

Use when subagents are not authorized.

Behavior:

1. Check the clarification brief.
2. Create or update goal contract.
3. Create or update execution policy only if required planning substrate is satisfied or not required.
4. Create a control review draft marked `Needs Independent Review`.
5. Do not compile final runtime `/goal` unless the user explicitly approves the artifacts.

### Mode B: Subagent-Reviewed Compilation Mode

Use when subagents are explicitly authorized.

Behavior:

1. Check the clarification brief.
2. Create or update goal contract.
3. Create or update execution policy only if required planning substrate is satisfied or not required.
4. Run independent subagent review passes without running implementation or dispatching implementer agents.
5. Revise artifacts based on review findings.
6. Re-review until approval or stop after the maximum review cycles.
7. Create an approved control review if findings converge.
8. Compile final runtime `/goal` command.
9. Do not start `/goal`.

## Maximum Review Cycles

Default maximum review-revision cycles: `2`.

If review does not converge after two cycles, stop and report:

- unresolved conflicts
- reviewer disagreements
- exact artifact sections involved
- recommended next action
- smallest required human decision

Do not continue self-revising indefinitely.

## Workflow

### Step 0: Validate the Clarification Brief

Read the clarification brief. If available, run:

```bash
python3 ~/.agents/skills/orchestrating-cybernetic-pregoal/scripts/check_pregoal_inputs.py --clarification <path>
```

If the script path is not available, perform the same checks manually.

The clarification is acceptable only if one of the following is true:

- it contains `Clarification Status` with `Complete`
- it contains `Clarification is complete`
- it states `No open blocking questions`
- it records confirmed decisions and has no open blocking questions

If clarification is incomplete, stop. Do not create goal, plan, review, or runtime `/goal`.

### Step 1: Determine Artifact Paths

Derive the date and slug from the clarification path unless the user specifies paths.

From:

```text
docs/superpowers/clarifications/YYYY-MM-DD-<slug>.md
```

Use:

```text
docs/superpowers/goals/YYYY-MM-DD-<slug>.md
docs/superpowers/plans/YYYY-MM-DD-<slug>.md
docs/superpowers/control-reviews/YYYY-MM-DD-<slug>.md
docs/superpowers/progress/YYYY-MM-DD-<slug>.md
```

The goal, plan, control review, and progress log must use the same derived date/slug. This keeps queue-friendly `/goal` commands emitted by `$clarifying-cybernetic-tasks` stable. If the requested path is ambiguous or does not contain a deterministic date/slug, stop and ask for the smallest path decision instead of inventing a different slug.

### Step 2: Create or Update the Goal Contract

Use `$writing-cybernetic-goals` when available.

The goal contract must:

- reference the clarification brief
- preserve all confirmed decisions
- define success conditions
- define invariants and forbidden scope
- define verification surfaces
- define stop conditions
- not instruct `/goal` to write or approve its own plan
- not output the final runtime `/goal` command yet

Expected artifact:

```text
docs/superpowers/goals/YYYY-MM-DD-<slug>.md
```

### Step 3: Create or Update the Execution Policy

Use `$writing-cybernetic-execution-policies` when available.

The execution policy must:

- reference the clarification and goal files
- record `$superpowers:writing-plans` substrate status for non-trivial implementation plans
- include a dependency matrix
- distinguish semantic invariants from tactical degrees of freedom
- define batch cadence
- define destructive intermediate-state policy
- define batch-end openable/verifiable requirements
- define sensor/test governance
- define stale/obsolete test retirement and rewrite policy
- define phase gates
- define stop conditions
- define progress log rules

If `$superpowers:writing-plans` is required but unavailable, stop and report missing planning infrastructure. Do not write an ad hoc approved plan as a substitute.

Expected artifact:

```text
docs/superpowers/plans/YYYY-MM-DD-<slug>.md
```

### Step 4: Review the Control Structure

Use `$reviewing-cybernetic-control-structures` when available.

If subagents are authorized, use independent reviewer roles. At minimum:

1. Requirement Traceability Reviewer
2. Control Contract Reviewer
3. Execution Policy / Cadence Reviewer
4. Sensor Governance Reviewer
5. Runtime Boundary Reviewer

Do not run implementation and do not dispatch implementer agents during pre-goal review.

Review the whole chain:

```text
clarification → goal → execution policy → runtime goal readiness
```

Do not review only the plan.

Expected artifact:

```text
docs/superpowers/control-reviews/YYYY-MM-DD-<slug>.md
```

If independent review discipline is missing and no explicit human approval exists, the review status must be `Needs Independent Review`, not `Approved`.

Apply the Final Observer Rule:

- If a reviewer reports a Blocking or Major finding and the orchestrator changes any control artifact to address it, the modified artifact is `Dirty`.
- Dirty artifacts cannot be marked `Approved`.
- Run final independent re-review on the changed sections before approval.
- The final re-review prompt must ask whether prior blockers were resolved, whether new blockers were introduced, and whether approval is recommended.
- Lint PASS is a structural sensor only; it does not replace semantic or control-policy re-review.
- Deterministic-only exceptions are allowed only for guard-covered formatting or lint-only repairs, and must be recorded in the control review.

### Step 5: Revise and Re-Review

If review status is `Needs Revision`:

1. Apply only the required revisions.
2. Avoid over-correcting non-critical suggestions.
3. Mark changed control artifacts `Dirty` unless every change is deterministic-only and guard-covered.
4. Re-run independent review for substantive changes, focused on the changed sections and prior blockers.
5. Record the final observer check in the control review.
6. Stop after two review-revision cycles if not approved.

Do not alter confirmed human decisions. If a revision would change product semantics, stop and ask for human input.

### Step 6: Compile the Runtime `/goal`

Use `$compiling-cybernetic-runtime-goals` when available.

Before outputting runtime `/goal`, ensure:

- clarification is complete
- goal contract exists
- execution policy exists
- control review exists
- control review is `Approved`
- no substantive post-review artifact mutation remains unobserved by final independent re-review
- deterministic-only exceptions, if used, are explicitly recorded and guard-covered
- all files reference the same feature
- artifact paths use the same date/slug unless the user explicitly specified alternatives
- the runtime `/goal` references all approved files

If available, run:

```bash
python3 ~/.agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py \
  --clarification <clarification> \
  --goal <goal> \
  --plan <plan> \
  --review <review>
```

Then compile the runtime command.

### Step 7: Final Output

Output:

- artifact paths
- review status
- short control summary
- final runtime `/goal` command if approved
- blocked status if not approved

Do not start `/goal`.

## Runtime `/goal` Requirements

The final `/goal` must instruct Codex to execute approved control artifacts only.

It must not instruct Codex to:

- write a new implementation plan
- approve its own plan
- reinterpret requirements
- change confirmed semantics
- replace approved sensors
- redesign the execution policy

It must instruct Codex to:

- use `$superpowers:executing-plans` discipline against the approved plan;
- use `$superpowers:systematic-debugging` for unclear or repeated failures;
- use `$superpowers:verification-before-completion` before claiming completion;
- follow equivalent approved artifact discipline if runtime cannot load those skills.

The command must reference:

- clarification file
- goal file
- execution policy / plan file
- control review file

The command must include this precondition:

```text
If any referenced artifact is missing, not approved, or internally inconsistent, stop and report the smallest required human decision.
```

## Stop Conditions

Stop and report if:

- clarification is incomplete
- clarification has unresolved blocking questions
- goal changes confirmed semantics
- execution policy changes goal semantics
- review does not converge after two cycles
- reviewer disagreements imply a product decision
- subagents are needed but not authorized
- required Superpowers planning substrate is unavailable
- independent review discipline is missing and no explicit human approval exists
- any substantive post-review artifact mutation remains dirty or lacks final independent re-review
- lint PASS is the only evidence for resolving a semantic/control-policy reviewer blocker
- final runtime `/goal` would need to invent or approve its own control structure

## Output Format

### Approved compilation

```markdown
Pre-goal compilation complete.

Artifacts:
- Clarification: `...`
- Goal contract: `...`
- Execution policy: `...`
- Control review: `...` (`Approved`)

Control summary:
- Setpoint: ...
- Invariants: ...
- Execution policy: ...
- Sensors: ...
- Runtime boundary: ...

Use this `/goal`:

```text
/goal Execute the approved execution policy in ...
```

Do not start the goal until you are ready for runtime execution.
```

### Blocked compilation

```markdown
Pre-goal compilation blocked.

Reason:
- ...

Artifacts created or updated:
- ...

Unresolved issue:
- ...

Smallest human decision needed:
- ...
```

## Validation Checklist

Before responding, verify:

- [ ] This skill did not implement code.
- [ ] This skill did not start `/goal`.
- [ ] Subagents were used only if explicitly authorized.
- [ ] Required Superpowers substrate status was checked.
- [ ] No required Superpowers substrate was silently emulated.
- [ ] Clarification was complete before creating downstream artifacts.
- [ ] Goal contract preserved confirmed human decisions.
- [ ] Execution policy preserved the goal contract.
- [ ] Execution policy uses `$superpowers:writing-plans` for non-trivial implementation plans or blocks.
- [ ] Review checked the whole control structure, not only the plan.
- [ ] Review does not mark self-review as `Approved`.
- [ ] Any substantive post-review artifact mutation had final independent re-review before approval.
- [ ] Lint PASS was not used as a substitute for semantic/control-policy re-review.
- [ ] Review status is `Approved` before final runtime `/goal` is emitted.
- [ ] If not approved, the response is blocked and asks for the smallest necessary decision.
- [ ] Runtime `/goal` references clarification, goal, plan, and review files.
- [ ] Runtime `/goal` includes the missing/not-approved/inconsistent artifact precondition.
- [ ] Runtime `/goal` includes executing, debugging, and completion-verification discipline.
- [ ] Runtime `/goal` does not tell Codex to write or approve a new plan.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Treating this as an implementation skill | Stop; this skill only compiles control artifacts |
| Spawning subagents without user authorization | Ask for authorization or run candidate-only mode |
| Creating a final `/goal` from an incomplete clarification | Stop and return to clarification |
| Reviewing only the plan | Review clarification, goal, plan, and runtime boundary |
| Replacing missing `$superpowers:writing-plans` with an ad hoc approved plan | Stop and report missing planning infrastructure |
| Marking Approved after fixing reviewer blockers without final re-review | Mark artifacts Dirty / Needs Re-review and run final independent re-review |
| Treating lint PASS as proof that semantic reviewer blockers are resolved | Use lint only as a structural sensor; require final observer pass for substantive changes |
| Choosing a new slug for downstream artifacts | Use the clarification brief's date/slug unless the user explicitly specified other paths |
| Letting review revisions change confirmed semantics | Stop and ask the human |
| Infinite review-revision loops | Stop after two cycles |
| Marking self-review as Approved | Require subagent, external reviewer, or explicit human approval |
| Starting `/goal` after compiling it | Output the command only |
