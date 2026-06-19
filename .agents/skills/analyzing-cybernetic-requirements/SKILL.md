---
name: analyzing-cybernetic-requirements
description: 'Use when a formed task or task candidate has ambiguous requirement meaning, acceptance criteria, output shape, constraints, non-goals, risk, or required control checks. Use framing-cybernetic-intent first for pre-task intent.'
---

# Analyzing Cybernetic Requirements

## Overview

Turn a formed task or task candidate into approved requirement meaning for later
goal/control work.

This skill owns requirement analysis only. It does not design, plan, review,
compile runtime JSON, or execute target work.

Official persistent control facts are JSON only. Markdown templates are
background aids, not official guard/compiler/runtime input.

For the detailed rulebook, read
`references/requirements-analysis-detailed-rules.md`.

## Hot Path

1. Confirm the input is a formed task. If it is pre-task intent, confusion,
   dissatisfaction, risk sense, failed experience, method preference, process
   distrust, or observed symptoms, use `$framing-cybernetic-intent` first.
2. Preserve the requested scope. Do not reduce, simplify, postpone, or replace
   requested behavior because it looks hard.
3. Extract `source_requirements` before writing `required_outcomes` for
   `controlled_run` work.
4. Define `counterexample_gate_contract` in requirements stage: quality
   standard, required checked transformations,
   minimum independent reviewer, reject-if conditions, and per-outcome gates.
5. Ask only questions that change approved meaning, evidence, scope, authority,
   or output contract.
6. Classify uncertainty as human decision, default assumption, or deferred
   design/planning/execution detail.
7. Produce or update `requirements.control.json`.
8. For `controlled_run`, get `What the User Approved: Approved` before handoff.

## Source Requirements

Each source requirement is one must-do item from the approved request. Preserve:

- original quote or source reference;
- required action;
- requirement type;
- required evidence strength;
- target objects when applicable;
- completion checks;
- whether missing it blocks `goal_achieved`.

If the user asks to measure, implement, decide, repair, or diagnose, preserve
that action. A framework, plan, readiness result, compatibility result, or
decision rule may support the work, but cannot replace it without new approval.

## Counterexample Gate Contract

For `controlled_run`, requirements must define the quality gate before
orchestration starts. Record `counterexample_gate_contract` with:

- `quality_standard`: what an independent reviewer must try to disprove;
- `required_checked_transformations`: the decomposition and claim positions the
  gate must challenge;
- `minimum_reviewer`: allowed independent reviewer kinds and evidence reference
  requirement;
- `reject_if`: semantic failure conditions that must prevent approval.

Each blocking `required_outcome` must also define a per-outcome
`counterexample_gate`: completion standard, checked transformations, required
evidence IDs, and reject-if conditions.

Downstream review may add stronger checks, but must not invent, weaken, or
replace the requirements-approved quality contract.

## Approval Commitment

For `controlled_run`, show the compact control commitment in
plain language and wait for approval. It must include at least:

- human purpose;
- primary object;
- requested transformation;
- non-goals;
- how we know the user's purpose was met;
- where the result must show up;
- what counts as done;
- evidence needed to call it done;
- counterexample gate quality contract and per-outcome gates;
- required answer path and what is not enough;
- work covered in this run;
- what the agent may do;
- forbidden live or irreversible actions;
- final answer format.

Human answers to clarification questions are inputs, not approval.

## Required Checks

Record these checks as required, satisfied, or not applicable:

- Meaning;
- Rubric;
- Output Contract;
- Design;
- Goal;
- Execution Plan;
- Review;
- Risk.

Use `references/decision-levels.md` for decision classification.

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

## Validation Checklist

- [ ] Input is a formed task, or pre-task intent was routed to framing first.
- [ ] Requested action was not weakened.
- [ ] Source requirements preserve original requested items.
- [ ] What the User Approved is explicit when needed.
- [ ] Required checks are recorded.
- [ ] Design questions are deferred when they are solution model questions.
- [ ] Output contract is identified when it affects acceptance or handoff.
- [ ] Queue-friendly handoff uses `predict_pregoal_handoff.py` when available.
