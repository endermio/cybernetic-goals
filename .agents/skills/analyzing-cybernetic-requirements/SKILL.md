---
name: analyzing-cybernetic-requirements
description: 'Use when a formed task or task candidate has ambiguous requirement meaning, acceptance criteria, output shape, constraints, non-goals, risk, or required control checks. Use framing-cybernetic-intent first for pre-task intent.'
---

# Analyzing Cybernetic Requirements

## Overview

Turn a formed task or task candidate into approved requirement meaning for
later control work.
This skill does not design, plan, compile runtime JSON, or execute target work.

Official persistent control facts are JSON only. Markdown is background.
Detailed rules live in `references/requirements-analysis-detailed-rules.md`.
All stage-routing gates use `../references/transition-gate-protocol.md`.

## Hot Path

1. If the input is pre-task intent, dissatisfaction, risk sense, method
   preference, symptoms, or process distrust, use `$framing-cybernetic-intent`.
2. Preserve the requested scope and action. Do not reduce requested behavior to
   a plan, readiness, framework, compatibility result, or future option.
3. Extract `source_requirements` before `required_outcomes`.
4. Always define `information_sufficiency_check`. If no pre-design facts are
   needed, set it to `not_required`. Facts must derive from
   `source_requirements` and/or `required_outcomes`, include `why_needed`,
   `acceptable_evidence`, `current_status`, `evidence_ref`, and be challenged
   by independent `counterexample_review`. Use `schema_version: 1.1.0` or later.
   A free-form `required_observations` list is not enough.
5. Information collection is part of requirements analysis. Before approval,
   run `requirements_information_loop.py --run-dir <run-dir> --json` whenever
   sufficiency is not `satisfied`/`not_required`; follow its `next_action`
   and rerun the gate after the action. Do not ask the user to authorize
   internal review or safe read-only collection.
6. Define `counterexample_gate_contract` in the requirements stage and
   per-outcome `counterexample_gate` before orchestration starts.
7. Before approval, show any missing/weak information facts as "needed before
   design"; do not hide them inside approved JSON or future pre-goal work.
8. Ask only questions that change approved meaning, evidence, scope,
   authority, or output contract.
9. Classify uncertainty as human decision, default assumption, or deferred
   design/planning/execution detail.
10. Produce or update `requirements.control.json`.
11. For `controlled_run`, run `predict_pregoal_handoff.py`; only output its
    handoff when it passes and `What the User Approved: Approved`.

## Source Requirements

Each source requirement is one must-do item from the approved request. Preserve:
source reference, required action, requirement type, evidence strength, target
objects, completion checks, and whether missing it blocks `goal_achieved`.

## Quality Gates

`counterexample_gate_contract` records what an independent reviewer must try to
disprove, required checked transformations, minimum reviewer provenance, and
reject-if conditions. Downstream review may strengthen this contract but must
not replace or weaken it.

Each blocking `required_outcome` needs a per-outcome `counterexample_gate` with
completion standard, checked transformations, required evidence IDs, and
reject-if conditions.

## Approval Commitment

For `controlled_run`, show a compact plain-language commitment before approval:
purpose, object, requested transformation, non-goals, done standard, result
placement, required evidence, information sufficiency if needed,
counterexample gates, covered work, allowed actions, forbidden actions, and
final answer format.

## Required Checks

Record Meaning, Rubric, Output Contract, Design, Goal, Execution Plan, Review,
and Risk as required, satisfied, or not applicable.

## State Machine

Treat `requirements_information_loop.py` as a loop controller.

- `agent_must_continue: true`: execute `next_action` in this turn and rerun the
  same gate.
- `RunInformationCounterexampleReview`, `RunInformationGathering`,
  `RepairRequirementsInformationState`, and `ReviseRequirements` are agent-owned.
- `AskUserForInformation` and `ReadyForUserApproval` are user-owned stop points.
- Only user-owned actions are reported to the user as waits. Pending approval is
  not a stop while the next action is agent-owned.

## Output Format

Before output, run the information loop when `information_sufficiency_check` is
not complete. If the result is agent-owned, continue the loop rather than
reporting a wait.

If the result is user-owned, ask only for the requested information, decision, or
approval. Do not output orchestration or runtime `/goal`.

If requirements are approved for `controlled_run`, run or quote:

```bash
python3 .agents/skills/analyzing-cybernetic-requirements/scripts/predict_pregoal_handoff.py \
  --run-dir docs/cybernetics/runs/<slug>
```

Use the script output for queue-friendly paths and pointer shape. The predicted
pointer is not the final approved runtime command.

For bounded work with only `rubric check: required`, route to
`$writing-cybernetic-goals` after the rubric is confirmed; do not default to
JSON pre-goal orchestration.
