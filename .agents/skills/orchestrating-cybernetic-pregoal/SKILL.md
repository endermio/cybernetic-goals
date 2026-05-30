---
name: orchestrating-cybernetic-pregoal
description: 'Use after a completed requirements analysis brief to orchestrate the pre-goal compilation chain before launching a Codex /goal. Coordinates existing cybernetic skills to invoke or validate any required solution design, create or update the control contract, execution policy, control review, and final runtime /goal command. Requires explicit user authorization before spawning subagents. Does not execute target work and does not start /goal execution.'
---

# Orchestrating Cybernetic Pre-goal

## Overview

This skill orchestrates the **pre-goal compilation chain** after requirements have been analyzed.

It turns a completed requirements analysis brief into approved control artifacts:

```text
requirements analysis brief
  -> solution design, when Design Gate is required
  → goal contract
  → execution policy / plan
  → control-structure review
  → final runtime /goal command
```

This skill is a thin orchestrator. It does not replace the other cybernetic skills. It coordinates them.

## Core Boundary

This skill must not:

- analyze requirements from scratch
- invent required solution design inside the execution policy
- synthesize solution design inside the orchestrator
- synthesize or revise output contracts inside the orchestrator
- execute target work
- start `/goal` execution
- make requirement decisions for the human
- mark a control structure approved when semantic conflicts remain
- spawn subagents unless the user explicitly authorized subagents in the current request
- let `/goal` write or approve its own plan

This skill may:

- inspect a completed requirements analysis brief
- call existing cybernetic skills in the correct order
- emulate narrow cybernetic formatting only when a downstream cybernetic skill is unavailable and that fallback is explicitly allowed
- create or update control artifacts under `docs/cybernetics/`
- invoke, request, or validate a solution design when Design Gate is required
- propagate and validate output contract presence across downstream artifacts
- use explicitly authorized subagents as independent reviewers
- iterate review and revision up to the configured limit
- compile the final `/goal` command after approval

## Required Infrastructure

Follow `$cybernetic-superpowers-infrastructure`.

This orchestrator may emulate cybernetic artifact formatting when a downstream cybernetic skill is unavailable. It must not emulate required Superpowers infrastructure.

It must not emulate solution design synthesis. Solution design is a substantive control artifact, not narrow formatting.

It must not synthesize output contracts. Output contract identification belongs to requirements analysis; complex output-structure synthesis belongs to solution design; final output contract preservation belongs to goal writing.

Required infrastructure boundaries:

- non-trivial execution policy generation requires `$superpowers:writing-plans` as planning substrate;
- control review `Approved` requires independent review discipline or explicit human approval;
- control review `Approved` requires a final observer pass after the last substantive artifact mutation;
- runtime `/goal` compilation must include `$superpowers:executing-plans`, `$superpowers:systematic-debugging`, and `$superpowers:verification-before-completion` discipline.

If a required substrate is unavailable, stop and report the missing infrastructure. Do not self-substitute and do not mark the control structure `Approved`.

## Relationship to Other Skills

Use this skill after:

- `$routing-cybernetic-workflows` has recommended a Level 3 or Level 4 workflow, or the user explicitly chose full pre-goal compilation
- `$analyzing-cybernetic-requirements` has produced a completed requirements analysis brief

This skill orchestrates:

- `$writing-cybernetic-goals`
- `$designing-cybernetic-solutions`
- `$writing-cybernetic-execution-policies`
- `$reviewing-cybernetic-control-structures`
- `$compiling-cybernetic-runtime-goals`
- `$cybernetic-superpowers-infrastructure`

It should not duplicate their templates or rules unless they are unavailable. If a downstream cybernetic skill is available, prefer using it. If a downstream cybernetic skill is unavailable, emulate only its narrow cybernetic responsibility and state that the fallback was used.

Never emulate required Superpowers substrates. In particular:

- do not replace `$designing-cybernetic-solutions` with orchestrator-authored solution design when Design Gate is required;
- do not replace `$superpowers:writing-plans` with ad hoc internal planning for non-trivial execution policies;
- do not replace independent review discipline with self-review;
- do not compile a runtime `/goal` that omits required runtime execution, debugging, and verification discipline.

## Required Input

A completed requirements analysis brief, usually:

```text
docs/cybernetics/requirements/YYYY-MM-DD-<slug>.md
```

When the input path follows this pattern, the same `YYYY-MM-DD-<slug>` is the artifact identity for the whole pre-goal chain. Do not choose a different slug unless the user explicitly requests different output paths.

The user should invoke this skill with an explicit requirements path, for example:

```text
$orchestrating-cybernetic-pregoal 根据 docs/cybernetics/requirements/2026-05-22-collaborative-supervision.md 自动完成 pre-goal 编译。允许使用 subagents 做独立 review。若 review 无法收敛，停止并报告阻塞点。
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

- You may create candidate design, goal, and execution policy files.
- You may create a draft control review marked `Needs Independent Review`.
- You must not claim independent review or mark the control structure `Approved` unless a separate reviewer, explicit human approval, or an authorized subagent review exists.
- Ask the user to authorize subagent review or manually approve the artifacts before compiling a final runtime `/goal`.

## Pre-goal Orchestration Modes

### Mode A: Candidate-Only Mode

Use when subagents are not authorized.

Behavior:

1. Check the requirements analysis brief.
2. Create or validate solution design if Design Gate is required.
3. Create or update goal contract.
4. Create or update execution policy only if required planning substrate is satisfied or not required.
5. Create a control review draft marked `Needs Independent Review`.
6. Do not compile final runtime `/goal` unless the user explicitly approves the artifacts.

### Mode B: Subagent-Reviewed Compilation Mode

Use when subagents are explicitly authorized.

Behavior:

1. Check the requirements analysis brief.
2. Create or validate solution design if Design Gate is required.
3. Create or update goal contract.
4. Create or update execution policy only if required planning substrate is satisfied or not required.
5. Run independent subagent review passes without running target execution or dispatching execution agents.
6. Revise artifacts based on review findings.
7. Re-review until approval or stop after the maximum review cycles.
8. Create an approved control review if findings converge.
9. Compile final runtime `/goal` command.
10. Do not start `/goal`.

## Maximum Review Cycles

Default maximum review-revision cycles: `2`.

If review does not converge after two cycles, stop and report:

- unresolved conflicts
- reviewer disagreements
- exact artifact sections involved
- smallest required human decision

Do not continue self-revising indefinitely.

## Workflow

### Step 0: Validate the Requirements Analysis Brief

Read the requirements analysis brief. If available, run:

```bash
python3 ~/.agents/skills/orchestrating-cybernetic-pregoal/scripts/check_pregoal_inputs.py --requirements <path>
```

Then, if available, run:

```bash
python3 .agents/skills/orchestrating-cybernetic-pregoal/scripts/orchestration_guard.py \
  --state before-design \
  --requirements <requirements>
```

If the script path is not available, perform the same checks manually.

The requirements analysis is acceptable only if one of the following is true:

- it contains `Requirements Analysis Status` with `Complete`
- it contains `Requirements analysis is complete`
- it states `No open blocking questions`
- it records confirmed decisions and has no open blocking questions

If requirements analysis is incomplete, stop. Do not create design, goal, plan, review, or runtime `/goal`.

### Step 1: Determine Artifact Paths

Derive the date and slug from the requirements path unless the user specifies paths.

From:

```text
docs/cybernetics/requirements/YYYY-MM-DD-<slug>.md
```

Use:

```text
docs/cybernetics/designs/YYYY-MM-DD-<slug>.md
docs/cybernetics/goals/YYYY-MM-DD-<slug>.md
docs/cybernetics/plans/YYYY-MM-DD-<slug>.md
docs/cybernetics/control-reviews/YYYY-MM-DD-<slug>.md
docs/cybernetics/progress/YYYY-MM-DD-<slug>.md
docs/cybernetics/orchestrations/YYYY-MM-DD-<slug>.md
```

The design, goal, plan, control review, and progress log must use the same derived date/slug. This keeps queue-friendly `/goal` commands emitted by `$analyzing-cybernetic-requirements` stable. If the requested path is ambiguous or does not contain a deterministic date/slug, stop and ask for the smallest path decision instead of inventing a different slug.

Use `assets/pregoal-orchestration-status-template.md` for the orchestration status artifact.

## Design Dispatch Rule

When Design Gate is required, the orchestrator must invoke or request `$designing-cybernetic-solutions` before goal writing.

The orchestrator owns:

- sequencing
- artifact path derivation
- lifecycle checks
- source-contract checks
- blocking when design is missing or invalid
- downstream propagation of the design path
- downstream propagation and validation of any output contract

The orchestrator does not own solution-model synthesis.

The orchestrator does not own output-contract synthesis.

Do not synthesize solution design inside the orchestrator. Do not treat solution design as narrow formatting fallback.

If `$designing-cybernetic-solutions` is unavailable when Design Gate is required, stop and report the missing downstream skill.

Design artifacts with status `Candidate`, `Reviewed`, or `Approved` may enter downstream stages when all are true:

- the artifact was produced by `$designing-cybernetic-solutions` or explicitly provided by the user;
- it references the requirements analysis in `Source Contracts`;
- it has no blocking open design questions;
- final control review will check Design Fidelity.

If any design artifact exists, propagate its path to goal writing, execution-policy writing, control review, and runtime compilation, even when Design Gate is satisfied or no longer required.

## Non-Fallback Rule

The orchestrator may emulate narrow formatting only for downstream cybernetic artifacts where this skill explicitly allows it.

It must not emulate:

- requirements analysis
- solution design synthesis
- execution-policy substrate
- independent review
- runtime compilation guard

If any non-emulatable stage is required and unavailable, stop and report the missing dependency.

## Orchestration State Machine

Before each stage, run `scripts/orchestration_guard.py` for that stage if available. If the guard fails, stop. Do not continue based on confidence or natural-language reasoning.

| Current State | Required condition | Next Action | Forbidden Action |
|---|---|---|---|
| `RequirementsMissing` | requirements absent or incomplete | `Blocked` | design / goal / policy / review / runtime compile |
| `RequirementsComplete` | Design Gate required and design missing | `RunDesign` | goal writing |
| `DesignReady` | design exists, references requirements, and has no blocking open questions | `RunGoalWriting` | execution policy |
| `GoalReady` | goal exists and references requirements plus any design path | `RunExecutionPolicy` | review |
| `PolicyReady` | execution policy exists and references requirements, goal, and any design path | `RunReview` | runtime compile |
| `ReviewApproved` | review is Approved and Final Observer allows approval | `RunRuntimeCompile` | execution |
| `RuntimeGoalReady` | final `/goal` is compiled | output command | start `/goal` |
| `Blocked` | any required gate fails | report blocker | continue |

### Step 2: Create or Validate the Solution Design

Before goal writing, if available, run:

```bash
python3 .agents/skills/orchestrating-cybernetic-pregoal/scripts/orchestration_guard.py \
  --state before-goal \
  --requirements <requirements> \
  --design <design-if-present>
```

Use `$designing-cybernetic-solutions` when `Design Gate: required` appears in the requirements analysis, router output, user request, or existing artifact chain.

The solution design must:

- reference the requirements analysis brief;
- define core objects/actors/roles, relationships, flows, and boundaries;
- define interfaces/contracts, lifecycle or state model, failure model, and evidence/sensor model when relevant;
- distinguish design invariants from tactical degrees of freedom;
- map design elements to goal and execution-policy implications;
- not create goal, plan, review, runtime `/goal`, or target-work artifacts.

The orchestrator must not synthesize these design contents itself. If the design is missing and required, the next allowed action is `RunDesign`.

Expected artifact:

```text
docs/cybernetics/designs/YYYY-MM-DD-<slug>.md
```

If Design Gate is required but the design cannot be created because of unresolved design questions, stop and report the smallest required human decision.

### Step 3: Create or Update the Goal Contract

Use `$writing-cybernetic-goals` when available.

The goal contract must:

- reference the requirements analysis brief
- reference the solution design when Design Gate is required or a design exists
- include `Final Output Contract` when Output Contract Gate was required, satisfied by a requirements/design artifact, or otherwise present upstream
- preserve all confirmed decisions
- define success conditions
- define invariants and forbidden scope
- define verification surfaces
- define stop conditions
- not instruct `/goal` to write or approve its own plan
- not output the final runtime `/goal` command yet

Expected artifact:

```text
docs/cybernetics/goals/YYYY-MM-DD-<slug>.md
```

### Step 4: Create or Update the Execution Policy

Before writing the execution policy, if available, run:

```bash
python3 .agents/skills/orchestrating-cybernetic-pregoal/scripts/orchestration_guard.py \
  --state before-policy \
  --requirements <requirements> \
  --design <design-if-present> \
  --goal <goal>
```

Use `$writing-cybernetic-execution-policies` when available.

The execution policy must:

- reference the requirements analysis and goal files
- reference the solution design when Design Gate is required or a design exists
- record `$superpowers:writing-plans` substrate status for non-trivial execution policies
- include a dependency matrix
- distinguish semantic invariants from tactical degrees of freedom
- define batch cadence
- define destructive intermediate-state policy
- define batch-end openable/verifiable requirements
- define sensor/evidence governance
- define stale/obsolete sensor retirement and rewrite policy
- define phase gates
- define stop conditions
- define progress log rules

If `$superpowers:writing-plans` is required but unavailable, stop and report missing planning infrastructure. Do not write an ad hoc approved plan as a substitute.

Expected artifact:

```text
docs/cybernetics/plans/YYYY-MM-DD-<slug>.md
```

### Step 5: Review the Control Structure

Before control review, if available, run:

```bash
python3 .agents/skills/orchestrating-cybernetic-pregoal/scripts/orchestration_guard.py \
  --state before-review \
  --requirements <requirements> \
  --design <design-if-present> \
  --goal <goal> \
  --plan <plan>
```

Use `$reviewing-cybernetic-control-structures` when available.

If subagents are authorized, use independent reviewer roles. At minimum:

1. Requirement Traceability Reviewer
2. Solution Design Fidelity Reviewer
3. Control Contract Reviewer
4. Execution Policy / Cadence Reviewer
5. Sensor Governance Reviewer
6. Runtime Boundary Reviewer

Do not run target execution and do not dispatch execution agents during pre-goal review.

Review the whole chain:

```text
requirements analysis → solution design → goal → execution policy → runtime goal readiness
```

Do not review only the plan.

Expected artifact:

```text
docs/cybernetics/control-reviews/YYYY-MM-DD-<slug>.md
```

If independent review discipline is missing and no explicit human approval exists, the review status must be `Needs Independent Review`, not `Approved`.

Apply the Final Observer Rule:

- If a reviewer reports a Blocking or Major finding and the orchestrator changes any control artifact to address it, the modified artifact is `Dirty`.
- Dirty artifacts cannot be marked `Approved`.
- Run final independent re-review on the changed sections before approval.
- The final re-review prompt must ask whether prior blockers were resolved, whether new blockers were introduced, and whether approval is recommended.
- Lint PASS is a structural sensor only; it does not replace semantic or control-policy re-review.
- Deterministic-only exceptions are allowed only for guard-covered formatting or lint-only repairs, and must be recorded in the control review.

### Step 6: Revise and Re-Review

If review status is `Needs Revision`:

1. Apply only the required revisions.
2. Avoid over-correcting non-critical suggestions.
3. Mark changed control artifacts `Dirty` unless every change is deterministic-only and guard-covered.
4. Re-run independent review for substantive changes, focused on the changed sections and prior blockers.
5. Record the final observer check in the control review.
6. Stop after two review-revision cycles if not approved.

Do not alter confirmed human decisions. If a revision would change requirement semantics, stop and ask for human input.

### Step 7: Compile the Runtime `/goal`

Use `$compiling-cybernetic-runtime-goals` when available.

Before runtime compilation, if available, run:

```bash
python3 .agents/skills/orchestrating-cybernetic-pregoal/scripts/orchestration_guard.py \
  --state before-runtime-compile \
  --requirements <requirements> \
  --design <design-if-present> \
  --goal <goal> \
  --plan <plan> \
  --review <review>
```

Before outputting runtime `/goal`, ensure:

- requirements analysis is complete
- solution design exists when Design Gate was required or a design artifact exists
- final output contract exists in the goal when Output Contract Gate was required or an output contract exists upstream
- goal contract exists
- execution policy exists
- control review exists
- control review is `Approved`
- no substantive post-review artifact mutation remains unobserved by final independent re-review
- deterministic-only exceptions, if used, are explicitly recorded and guard-covered
- all files reference the same feature
- artifact paths use the same date/slug unless the user explicitly specified alternatives
- the runtime `/goal` references all approved files
- the runtime `/goal` carries the final output contract from the goal when present or required

If available, run:

```bash
python3 ~/.agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py \
  --requirements <requirements> \
  --design <design-if-required-or-present> \
  --goal <goal> \
  --plan <plan> \
  --review <review>
```

Then compile the runtime command.

### Step 8: Final Output

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

- write a new execution policy
- approve its own plan
- reinterpret requirements
- change confirmed semantics
- rewrite the solution design
- replace the final output contract
- replace approved sensors
- redesign the execution policy

It must instruct Codex to:

- use `$superpowers:executing-plans` discipline against the approved plan;
- use `$superpowers:systematic-debugging` for unclear or repeated failures;
- use `$superpowers:verification-before-completion` before claiming completion;
- follow equivalent approved artifact discipline if runtime cannot load those skills.

The command must reference:

- requirements analysis file
- solution design file, when Design Gate was required or a design exists
- goal file
- execution policy / plan file
- control review file

The command must carry the final output contract from the goal when one is present or required.

The command must include this precondition:

```text
If any referenced artifact is missing, not approved, or internally inconsistent, stop and report the smallest required human decision.
```

## Stop Conditions

Stop and report if:

- requirements analysis is incomplete
- requirements analysis has unresolved blocking questions
- goal changes confirmed semantics
- required solution design is missing or conflicts with requirements analysis
- required final output contract is missing from the goal or conflicts with upstream output-contract requirements
- execution policy changes goal semantics
- execution policy redesigns the solution model
- review does not converge after two cycles
- reviewer disagreements imply a requirement decision
- subagents are needed but not authorized
- required Superpowers planning substrate is unavailable
- independent review discipline is missing and no explicit human approval exists
- any substantive post-review artifact mutation remains dirty or lacks final independent re-review
- lint PASS is the only evidence for resolving a semantic/control-policy reviewer blocker
- final runtime `/goal` would need to invent or approve its own control structure
- final runtime `/goal` would need to invent solution design

## Output Format

These output formats are response-only. Do not write `/goal` prompts, `$skill ...` commands, or conversational next-step prompts into orchestration status, progress, goal, design, plan, review, or requirements artifacts.

### Approved compilation

```markdown
Pre-goal compilation complete.

Artifacts:
- Requirements analysis: `...`
- Solution design: `...` or `not required`
- Goal contract: `...`
- Execution policy: `...`
- Control review: `...` (`Approved`)

Control summary:
- Setpoint: ...
- Solution model: ...
- Invariants: ...
- Execution policy: ...
- Sensors: ...
- Runtime boundary: ...

Response-only runtime `/goal` command:

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

- [ ] This skill did not execute target work.
- [ ] This skill did not start `/goal`.
- [ ] Subagents were used only if explicitly authorized.
- [ ] Required Superpowers substrate status was checked.
- [ ] No required Superpowers substrate was silently emulated.
- [ ] No required solution design synthesis was emulated inside the orchestrator.
- [ ] Requirements analysis was complete before creating downstream artifacts.
- [ ] Required solution design was created by `$designing-cybernetic-solutions` or explicitly provided before goal writing, otherwise blocked.
- [ ] Existing design artifact paths were propagated to goal, execution policy, review, and runtime compilation.
- [ ] Output contract presence was propagated and validated; no output contract was synthesized by the orchestrator.
- [ ] Goal contract preserved confirmed human decisions.
- [ ] Goal and execution policy preserved required solution design.
- [ ] Execution policy preserved the goal contract.
- [ ] Execution policy uses `$superpowers:writing-plans` for non-trivial execution policies or blocks.
- [ ] Review checked the whole control structure, including design when required, not only the plan.
- [ ] Review does not mark self-review as `Approved`.
- [ ] Any substantive post-review artifact mutation had final independent re-review before approval.
- [ ] Lint PASS was not used as a substitute for semantic/control-policy re-review.
- [ ] Review status is `Approved` before final runtime `/goal` is emitted.
- [ ] If not approved, the response is blocked and asks for the smallest necessary decision.
- [ ] Runtime `/goal` references requirements analysis, required design, goal, plan, and review files.
- [ ] Runtime `/goal` includes the missing/not-approved/inconsistent artifact precondition.
- [ ] Runtime `/goal` includes executing, debugging, and completion-verification discipline.
- [ ] Runtime `/goal` does not tell Codex to write or approve a new plan.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Treating this as an execution skill | Stop; this skill only compiles control artifacts |
| Spawning subagents without user authorization | Ask for authorization or run candidate-only mode |
| Creating a final `/goal` from an incomplete requirements analysis | Stop and return to requirements analysis |
| Skipping design when Design Gate is required | Run `$designing-cybernetic-solutions` before goal writing |
| Synthesizing solution design inside the orchestrator | Stop; invoke/request `$designing-cybernetic-solutions` or block |
| Dropping an existing design artifact because Design Gate is satisfied | Propagate the design path downstream |
| Reviewing only the plan | Review requirements analysis, design when required, goal, plan, and runtime boundary |
| Replacing missing `$superpowers:writing-plans` with an ad hoc approved plan | Stop and report missing planning infrastructure |
| Marking Approved after fixing reviewer blockers without final re-review | Mark artifacts Dirty / Needs Re-review and run final independent re-review |
| Treating lint PASS as proof that semantic reviewer blockers are resolved | Use lint only as a structural sensor; require final observer pass for substantive changes |
| Choosing a new slug for downstream artifacts | Use the requirements analysis brief's date/slug unless the user explicitly specified other paths |
| Letting review revisions change confirmed semantics | Stop and ask the human |
| Infinite review-revision loops | Stop after two cycles |
| Marking self-review as Approved | Require subagent, external reviewer, or explicit human approval |
| Starting `/goal` after compiling it | Output the command only |
