---
name: using-control-json
description: 'Use when runtime execution must operate approved cybernetic control JSON, record progress, or prepare completion evidence from a compiled JSON control chain.'
---

# Using Control JSON

## Overview

Use this skill when a runtime `/goal` pointer, `runtime.control.json`, or approved control chain sends Codex into JSON-backed cybernetic execution.

This is not the Level 2 bounded runtime protocol. Level 2 bounded goals use
`.agents/skills/using-bounded-control-json`.

This skill supports both approved JSON control shapes:

- full root chains with requirements/design/goal/plan/review/runtime;
- generation-aware runs with `requirements.control.json`, `run.control.json`,
  and the current `gen-N/runtime.control.json`.

Read `references/runtime-control-json-protocol.md` before executing, reporting status, or preparing completion evidence.

## Operating Contract

1. Validate first. Confirm required JSON files exist, parse, and agree on source paths, required steps, work coverage, verifier configuration, generation state, and writable output paths. Stop on missing, invalid, or inconsistent JSON and report the smallest required human decision.
2. approved control JSON is read-only. In full mode this includes `requirements.control.json`, `design.control.json`, `goal.control.json`, `plan.control.json`, `review.control.json`, and `runtime.control.json`. In generation-aware mode this includes `requirements.control.json`, `run.control.json`, the current `gen-N/runtime.control.json`, and any current-generation review named by `run.control.json`. Read these files to execute the approved chain; never rewrite them during runtime.
3. runtime writes control-output files only to `progress.jsonl`, `runtime-status.json`, and `final-report.json`. Non-control evidence artifacts may be written only under paths named in `runtime.control.json.runtime.writable_evidence_paths`.
4. Append to `progress.jsonl` for runtime observations, using one JSON object per line. Record discoveries, commands, evidence, blockers, required-step state, generation state, and amendment proposals there; do not mutate approved JSON to match execution.
5. Run the verifier before `goal_achieved: true`; only a verifier result that permits the claim allows `final-report.json` to contain `goal_achieved: true`.
6. Source requirements are approved original-request items. Runtime may not treat weaker substitute evidence as completion. If strategy cannot complete a blocking source requirement, propose an amendment with `affected_source_requirements`.
7. `/goal` is a short pointer and adapter, not a control fact. It should point to `runtime.control.json` and name `using-control-json`, leaving approved facts in JSON.

## Reviewed Replanning

When execution observes that the current strategy cannot produce a blocking
required outcome, do not silently fill the slot with readiness, compatibility,
or substitute evidence. Do not edit approved JSON in place. Append a
`control.amendment.proposed` event with the current `runtime_generation`,
reason, triggering observation, affected strategy stages,
`affected_source_requirements`, and whether `semantic_base`, required outcomes,
or authority would change.

Anchor-preserving amendments may be reviewed into a new generation by the
orchestrator. Amendments that change `requirements.control.json`,
`semantic_base`, required outcomes, what counts as done, work coverage,
authority, or forbidden actions require human reapproval.

## Completion Posture

If validation, progress append, status write, or verifier execution cannot be completed, report `goal_achieved: false` with the missing JSON, missing evidence, or failing verifier condition. Component completion is only progress evidence until the verifier permits the final claim.
