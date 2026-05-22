---
name: orchestrating-cybernetic-pregoal
description: 'Use after a completed clarification brief to orchestrate the pre-goal compilation chain before launching a Codex /goal. Coordinates existing cybernetic skills to create or update the goal contract, execution policy, control review, and final runtime /goal command. Requires explicit user authorization before spawning subagents. Does not implement code and does not start /goal execution.'
---

# Orchestrating Cybernetic Pregoal

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
- call or emulate the existing cybernetic skills in the correct order
- create or update control artifacts under `docs/superpowers/`
- use explicitly authorized subagents as independent reviewers
- iterate review and revision up to the configured limit
- compile the final `/goal` command after approval

## Relationship to Other Skills

Use this skill after:

- `$routing-cybernetic-workflows` has recommended a Level 3 or Level 4 workflow, or the user explicitly chose full pre-goal compilation
- `$clarifying-cybernetic-tasks` has produced a completed clarification brief

This skill orchestrates:

- `$writing-cybernetic-goals`
- `$writing-cybernetic-execution-policies`
- `$reviewing-cybernetic-control-structures`
- `$compiling-cybernetic-runtime-goals`

It should not duplicate their templates or rules unless they are unavailable. If a downstream skill is available, prefer using it. If it is unavailable, emulate only its narrow responsibility and state that the fallback was used.

## Required Input

A completed clarification brief, usually:

```text
docs/superpowers/clarifications/YYYY-MM-DD-<slug>.md
```

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

## Pregoal Orchestration Modes

### Mode A: Candidate-Only Mode

Use when subagents are not authorized.

Behavior:

1. Check the clarification brief.
2. Create or update goal contract.
3. Create or update execution policy.
4. Create a control review draft marked `Needs Independent Review`.
5. Do not compile final runtime `/goal` unless the user explicitly approves the artifacts.

### Mode B: Subagent-Reviewed Compilation Mode

Use when subagents are explicitly authorized.

Behavior:

1. Check the clarification brief.
2. Create or update goal contract.
3. Create or update execution policy.
4. Run independent subagent review passes.
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

Review the whole chain:

```text
clarification → goal → execution policy → runtime goal readiness
```

Do not review only the plan.

Expected artifact:

```text
docs/superpowers/control-reviews/YYYY-MM-DD-<slug>.md
```

### Step 5: Revise and Re-Review

If review status is `Needs Revision`:

1. Apply only the required revisions.
2. Avoid over-correcting non-critical suggestions.
3. Re-run review.
4. Stop after two review-revision cycles if not approved.

Do not alter confirmed human decisions. If a revision would change product semantics, stop and ask for human input.

### Step 6: Compile the Runtime `/goal`

Use `$compiling-cybernetic-runtime-goals` when available.

Before outputting runtime `/goal`, ensure:

- clarification is complete
- goal contract exists
- execution policy exists
- control review exists
- control review is `Approved`
- all files reference the same feature
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

The command must reference:

- clarification file
- goal file
- execution policy / plan file
- control review file

## Stop Conditions

Stop and report if:

- clarification is incomplete
- clarification has unresolved blocking questions
- goal changes confirmed semantics
- execution policy changes goal semantics
- review does not converge after two cycles
- reviewer disagreements imply a product decision
- subagents are needed but not authorized
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
- [ ] Clarification was complete before creating downstream artifacts.
- [ ] Goal contract preserved confirmed human decisions.
- [ ] Execution policy preserved the goal contract.
- [ ] Review checked the whole control structure, not only the plan.
- [ ] Review status is `Approved` before final runtime `/goal` is emitted.
- [ ] If not approved, the response is blocked and asks for the smallest necessary decision.
- [ ] Runtime `/goal` references clarification, goal, plan, and review files.
- [ ] Runtime `/goal` does not tell Codex to write or approve a new plan.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Treating this as an implementation skill | Stop; this skill only compiles control artifacts |
| Spawning subagents without user authorization | Ask for authorization or run candidate-only mode |
| Creating a final `/goal` from an incomplete clarification | Stop and return to clarification |
| Reviewing only the plan | Review clarification, goal, plan, and runtime boundary |
| Letting review revisions change confirmed semantics | Stop and ask the human |
| Infinite review-revision loops | Stop after two cycles |
| Marking self-review as Approved | Require subagent, external reviewer, or explicit human approval |
| Starting `/goal` after compiling it | Output the command only |
