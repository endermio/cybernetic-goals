---
name: orchestrating-cybernetic-pregoal
description: 'Use when completed requirements analysis exists and routing or requirements require JSON pre-goal orchestration before runtime /goal.'
---

# Orchestrating Cybernetic Pre-goal

## Overview

Coordinate approved JSON control artifacts before runtime execution.

Default controlled run shape:

```text
requirements.control.json
  -> run.control.json
  -> gen-000/runtime.control.json plus short /goal pointer
```

Expanded chains may also include solution design, goal, plan, and review files
when selected strategy or gates require them. Strategy is recorded as
`strategy_policy`; do not use old process-weight labels as control concepts.

Rules:

- `references/orchestration-protocol.md`
- `references/subagent-review-roles.md`
- `references/output-and-final-checks.md`
- `references/pregoal-detailed-rules.md`

## Process Need Check

A user request to use a heavier or lighter process is not sufficient by itself.
Check whether the formed task and approved requirements require pre-goal
orchestration.

Use `$routing-cybernetic-workflows` when control-entry need is unclear. Use
`$framing-cybernetic-intent` first for pre-task intent.

Do not create controlled-run artifacts when ordinary direct work or
`bounded_runtime` can preserve the target with less evidence/context/review budget.

## Ownership

This skill may create or update approved control files under
`docs/cybernetics/runs/<slug>/`, but it does not execute target work or start
`/goal`.

Routed elsewhere:

- new requirement meaning -> `$analyzing-cybernetic-requirements`;
- required solution model -> `$designing-cybernetic-solutions`;
- goal contract -> `$writing-cybernetic-goals`;
- execution strategy -> `$writing-cybernetic-execution-policies`;
- independent review -> `$reviewing-cybernetic-control-structures`;
- runtime compile -> `$compiling-cybernetic-runtime-goals`.

## Required Inputs

Use a JSON run directory:

```text
docs/cybernetics/runs/<slug>/
```

The run must contain approved requirements before downstream control artifacts
can be approved. If `What the User Approved` is missing or not Approved, return
to requirements analysis.

## Review And Subagents

Pre-goal review subagents require explicit authorization. Without subagent,
explicit human approval, or another independent reviewer, do not claim
independent review or mark the chain Approved.

Runtime target-work subagents are authorized only by the launched `/goal` and
approved work assignment.

## NeedsRevision Routing Rule

Semantic review verdicts are:

```text
`Approved` / `NeedsRevision` / `Blocked`
```

NeedsRevision routes to the earliest artifact that introduced drift:

- Requirements drift -> `ReturnToRequirementsAnalysis`
- Design drift -> `RunDesign`
- Goal drift -> `RunGoalWriting`
- Plan drift -> `RunExecutionPolicy`

Do not compile `runtime.control.json` until review verdict is `Approved`.

Regression example: a required `/api/v2` implementation must not be accepted as
legacy Drogon compatibility readiness. That is `NeedsRevision`.

## Counterexample Gate

Approved review must include `counterexample-gate` before runtime compilation.
It attempts to disprove the candidate control interpretation. Required gate
points:

```text
source_requirements->required_outcomes
required_outcomes->required_steps
required_steps->work_packages
required_steps->runtime_steps
pre_runtime_compile
blocked_or_goal_achieved
```

The approved gate must include `reviewer.kind`, `reviewer.id`, and
`reviewer.evidence_ref`. Self-written evidence is not enough.

## Runtime Compile Gate

Before `ReviewApproved -> RunRuntimeCompile`, runtime inputs must be final.
Expanded chains require:

```text
design.control.json status == approved
goal.control.json status == approved
plan.control.json status == approved
review.control.json status == approved
runtime.control.json status == compiled
```

`Candidate`, `Reviewed`, `NeedsRevision`, `Needs Revision`, `Dirty`, and `Needs
Re-review` artifacts may not enter runtime compilation.

Run both structural gates before outputting the runtime `/goal`:

```bash
control_chain_guard.py --run-dir docs/cybernetics/runs/<slug>
python3 .agents/skills/using-control-json/scripts/validate_control_chain.py docs/cybernetics/runs/<slug>
```

The second command must return `ok: true`. These checks are structural gates,
not quality approval; the approved review's `counterexample-gate` is the
quality gate.

## Runtime Amendment Orchestration

When a running generation writes `control.amendment.proposed`, do not treat the
event as completion evidence. Continue only when `strategy_policy` is
`reviewed_replanning`, the proposal preserves approved anchors, the patch has an
approved review, and the generation switch passes guard. With `frozen_strategy`,
stop and report the required decision.

Amendment details are in `references/pregoal-detailed-rules.md`.

## Orchestration State Machine

Use `scripts/orchestration_guard.py --state <state> --run-dir <run-dir>` before
each transition. Follow its `NEXT:` value.

Main transitions:

- `RequirementsMissing` -> `ReturnToRequirementsAnalysis` or `Blocked`
- `RequirementsComplete` -> `RunDesign` when design is required
- `DesignReady` -> `RunGoalWriting`
- `GoalReady` -> `RunExecutionPolicy`
- `PolicyReady` -> `RunReview`
- `ReviewApproved` -> `RunRuntimeCompile`
- `RuntimeGoalReady` -> output command only

## Final Output

Use `references/output-and-final-checks.md` for response shape. Output artifact
paths, review status, control summary, and approved runtime `/goal` pointer.

Do not start `/goal`.
