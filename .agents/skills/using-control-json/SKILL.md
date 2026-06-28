---
name: using-control-json
description: 'Use when runtime execution must operate approved cybernetic control JSON, record progress, or prepare completion evidence from a compiled JSON control chain.'
---

# Using Control JSON

## Overview

Use this skill when a runtime `/goal` pointer, `runtime.control.json`, or approved control chain sends Codex into JSON-backed cybernetic execution.

This is not `bounded_runtime`. Bounded runtime goals use
`.agents/skills/using-bounded-control-json`.

This skill supports official generation-aware JSON control runs:

- generation-aware runs with `requirements.control.json`, `run.control.json`,
  and the current `gen-N/runtime.control.json`.

Read `references/runtime-control-json-protocol.md` before executing, reporting status, or preparing completion evidence.
Gate result semantics follow `../references/transition-gate-protocol.md`.

## Operating Contract

1. Validate first. Confirm required JSON files exist, parse, and agree on source paths, required steps, work coverage, verifier configuration, generation state, and writable output paths. Stop on missing, invalid, or inconsistent JSON and report the smallest required human decision.
2. approved control JSON is read-only. This includes `requirements.control.json`, `run.control.json`, the current `gen-N/runtime.control.json`, and any current-generation review named by `run.control.json`. If the selected strategy or gate uses expanded design/goal/plan/review artifacts, those approved artifacts are read-only too. Read these files to execute the approved chain; never rewrite them during runtime.
3. runtime writes control-output files only to `progress.jsonl`, `runtime-status.json`, and `final-report.json`. Non-control evidence artifacts may be written only under paths named in `runtime.control.json.runtime.writable_evidence_paths`.
4. Runtime must use `append_progress_event.py` to append one JSON object per line to `progress.jsonl`; direct writes to `progress.jsonl` are invalid runtime behavior. Record discoveries, commands, evidence, blockers, required-step state, generation state, and amendment proposals there; do not mutate approved JSON to match execution.
5. `final-report.json` records the runtime completion claim and evidence; it does not grant verifier permission to itself. Before accepting or reporting `goal_achieved: true`, run the verifier and use the verifier process output as the source of truth.
6. Source requirements are approved original-request items. Runtime may not treat weaker substitute evidence as completion. If strategy cannot complete a blocking source requirement, propose an amendment with `affected_source_requirements`.
7. If runtime discovers a fact that should have been known before design or
   planning, preserve it as an information sufficiency issue. Do not invent a
   local sufficiency standard or continue under assumptions; append an
   observation or reviewed amendment proposal, or stop for the smallest human
   decision when approved anchors or authority would change.
8. `/goal` is a short pointer and adapter, not a control fact. It should point to `runtime.control.json` and name `using-control-json`, leaving approved facts in JSON.

## Gate Roles

Structural gates are schema checks, `control_chain_guard`,
`validate_control_chain`, and `verify_runtime_progress`. They prove file shape,
hashes, declared coverage, and progress consistency. Structural gates are not
quality approval.

Quality gate means `counterexample-gate`: an independent reviewer tries to
disprove the target decomposition, runtime strategy, blocked claim, or
completion claim. It must execute the requirements-approved
`counterexample_gate_contract` and each blocking outcome's per-outcome
`counterexample_gate`; runtime must not invent or weaken either.

## Reviewed Replanning

When execution observes that the current strategy cannot produce a blocking
required outcome, do not silently fill the slot with readiness, compatibility,
or substitute evidence. Do not edit approved JSON in place. Append a
`control.amendment.proposed` event with the current `runtime_generation`,
reason, triggering observation, affected strategy stages,
`affected_source_requirements`, and whether `semantic_base`, required outcomes,
or authority would change. The proposal must also include `patch_ref` pointing
to a JSON amendment patch that describes the next candidate strategy. Runtime
must not rely on the proposal text alone as the strategy change.

Anchor-preserving amendments may be reviewed into a new generation by the
orchestrator only when `run.control.json.strategy_policy` is
`reviewed_replanning`. Under `frozen_strategy`, an amendment proposal reports
that the approved strategy does not fit and requires a human decision before
continuing. The orchestrator must not synthesize its own approved review; it can
switch generations only after the patch has an approved amendment review.
Amendments that change `requirements.control.json`,
`semantic_base`, required outcomes, what counts as done, work coverage,
authority, or forbidden actions require human reapproval.

## Completion Posture

If validation, progress append, status write, or verifier execution cannot be completed, report `goal_achieved: false` with the missing JSON, missing evidence, or failing verifier condition. Component completion is only progress evidence until the verifier permits the final claim.
