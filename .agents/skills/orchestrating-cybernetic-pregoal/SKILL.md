---
name: orchestrating-cybernetic-pregoal
description: 'Use when completed requirements analysis exists and routing or requirements require JSON pre-goal orchestration before runtime /goal.'
---

# Orchestrating Cybernetic Pre-goal

## Overview

Coordinate approved JSON control artifacts before runtime execution.

Default controlled-run shape:

```text
requirements.control.json -> run.control.json -> gen-000/runtime.control.json
```

Expanded strategies may add design, goal, plan, and review files. Strategy is
recorded as `strategy_policy`; old process-weight labels are not control
concepts.

Read the rule files before acting:

- `references/orchestration-protocol.md`
- `references/subagent-review-roles.md`
- `references/output-and-final-checks.md`
- `references/pregoal-detailed-rules.md`
- `../references/transition-gate-protocol.md`

## Process Need Check

A user request to use a heavier or lighter process is not sufficient by itself.
Use `$routing-cybernetic-workflows` when control-entry need is unclear and
`$framing-cybernetic-intent` for pre-task intent. Do not create controlled-run
artifacts when ordinary direct work or `bounded_runtime` preserves the
controlled run target
with less evidence/context/review budget.

## Ownership

This skill may create or update approved control files under
`docs/cybernetics/runs/<slug>/`. It does not execute target work or start
`/goal`.

Route new requirement meaning to requirements analysis, solution model to
design, goal contract to goal writing, execution strategy to execution policy,
independent review to review, and runtime compile to runtime-goal compilation.

## Required Inputs

Use a JSON run directory with approved `requirements.control.json`. If
`What the User Approved` is missing or not Approved, return to requirements
analysis.

## Review And Gates

Pre-goal review subagents require explicit authorization. Without subagent,
human approval, or another independent reviewer, do not claim independent
review or mark the chain Approved. This rule does not apply to the
requirements-analysis internal `RunInformationCounterexampleReview`; that gate
runs before pre-goal review and does not require separate user authorization.

Approved review must include `counterexample-gate` before runtime compilation.
It must execute the requirements-approved `counterexample_gate_contract` and
each blocking outcome's per-outcome gate. Self-written evidence is not enough.
Regression rule: a required `/api/v2` implementation must not be accepted as
legacy Drogon compatibility readiness; that is `NeedsRevision`.

Before every pre-goal transition, run `scripts/orchestration_guard.py` for the
matching state. If `information_sufficiency_check` fails, route to
`RunInformationSufficiencyCheck` by running
`.agents/skills/analyzing-cybernetic-requirements/scripts/requirements_information_loop.py
--run-dir <run-dir> --json`; follow its `next_action` and rerun the gate. Do
not treat missing facts as design assumptions, and do not ask the user to
authorize internal counterexample review.

## Compile Gate

Do not compile `runtime.control.json` until review verdict is Approved. Expanded
chains also require design, goal, plan, and review statuses to be `approved`.
Candidate, dirty, or needs-revision artifacts may not enter runtime compilation.

Run both structural gates before outputting the runtime `/goal`:

```bash
control_chain_guard.py --run-dir docs/cybernetics/runs/<slug>
python3 .agents/skills/using-control-json/scripts/validate_control_chain.py docs/cybernetics/runs/<slug>
```

The second command must return `ok: true`. These are structural gates; the
approved `counterexample-gate` is the quality gate.

## Runtime Amendment Orchestration

When runtime writes `control.amendment.proposed`, continue only when
`strategy_policy` is `reviewed_replanning`, approved anchors are preserved, the
patch has approved review, and generation switch passes guard. With
`frozen_strategy`, stop and report the decision needed.

## State Machine

Use `scripts/orchestration_guard.py --state <state> --run-dir <run-dir>` before
each transition. A nonterminal transition-gate result is not a report to the
user; execute its `next_action` and run the gate again.
If the gate reports `agent_must_continue: true`, continue internally in the
same turn. Do not ask the user to authorize `RunInformationCounterexampleReview`
or other agent-owned transition actions.

Main transitions: RequirementsMissing, RequirementsComplete, DesignReady,
GoalReady, PolicyReady, ReviewApproved, RuntimeGoalReady.

## Final Output

Use `references/output-and-final-checks.md`. Output artifact paths, review
status, control summary, and approved runtime `/goal` pointer. Do not start
`/goal`.
