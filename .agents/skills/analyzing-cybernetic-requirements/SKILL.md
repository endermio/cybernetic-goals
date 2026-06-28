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

## Hot Path

1. If the input is pre-task intent, dissatisfaction, risk sense, method
   preference, symptoms, or process distrust, use `$framing-cybernetic-intent`.
2. Preserve the requested scope and action. Do not reduce requested behavior to
   a plan, readiness, framework, compatibility result, or future option.
3. Extract `source_requirements` before `required_outcomes`.
4. If design or planning needs facts first, define
   `information_sufficiency_check`: facts must derive from
   `source_requirements` and/or `required_outcomes`, include `why_needed`,
   `acceptable_evidence`, `current_status`, `evidence_ref`, and be challenged
   by independent `counterexample_review`. Use `schema_version: 1.2.0`.
   A free-form `required_observations` list is not enough.
5. Define `counterexample_gate_contract` in the requirements stage and
   per-outcome `counterexample_gate` before orchestration starts.
6. Before approval, show any missing/weak information facts as "needed before
   design"; do not hide them inside approved JSON or future pre-goal work.
7. Ask only questions that change approved meaning, evidence, scope,
   authority, or output contract.
8. Classify uncertainty as human decision, default assumption, or deferred
   design/planning/execution detail.
9. Produce or update `requirements.control.json`.
10. For `controlled_run`, run `predict_pregoal_handoff.py`; only output its
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

## Output Format

If requirements are not approved, output the smallest approval or revision
question. Do not output orchestration or runtime `/goal`.

If requirements are approved for `controlled_run`, run or quote:

```bash
python3 .agents/skills/analyzing-cybernetic-requirements/scripts/predict_pregoal_handoff.py \
  docs/cybernetics/runs/<slug>/requirements.control.json
```

Use the script output for queue-friendly paths and pointer shape. The predicted
pointer is not the final approved runtime command.

For bounded work with only `rubric check: required`, route to
`$writing-cybernetic-goals` after the rubric is confirmed; do not default to
JSON pre-goal orchestration.
