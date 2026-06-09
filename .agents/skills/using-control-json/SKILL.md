---
name: using-control-json
description: 'Use when runtime execution must operate approved cybernetic control JSON, record progress, or prepare completion evidence from a compiled JSON control chain.'
---

# Using Control JSON

## Overview

Use this skill when a runtime `/goal` pointer, `runtime.control.json`, or approved control chain sends Codex into JSON-backed cybernetic execution.

This is not the Level 2 bounded runtime protocol. Level 2 bounded goals use
`.agents/skills/using-bounded-control-json` and do not require the full
requirements/design/goal/plan/review control chain.

Read `references/runtime-control-json-protocol.md` before executing, reporting status, or preparing completion evidence.

## Operating Contract

1. Validate first. Confirm required JSON files exist, parse, and agree on source paths, required steps, work coverage, verifier configuration, and writable output paths. Stop on missing, invalid, or inconsistent JSON and report the smallest required human decision.
2. approved control JSON is read-only: `requirements.control.json`, `design.control.json`, `goal.control.json`, `plan.control.json`, `review.control.json`, and `runtime.control.json`. Read these files to execute the approved chain; never rewrite them during runtime.
3. runtime writes control-output files only to `progress.jsonl`, `runtime-status.json`, and `final-report.json`. Non-control evidence artifacts may be written only under paths named in `runtime.control.json.runtime.writable_evidence_paths`.
4. Append to `progress.jsonl` for runtime observations, using one JSON object per line. Record discoveries, commands, evidence, blockers, and required-step state there; do not mutate approved JSON to match execution.
5. Run the verifier before `goal_achieved: true`; only a verifier result that permits the claim allows `final-report.json` to contain `goal_achieved: true`.
6. `/goal` is a short pointer and adapter, not a control fact. It should point to `runtime.control.json` and name `using-control-json`, leaving approved facts in JSON.

## Completion Posture

If validation, progress append, status write, or verifier execution cannot be completed, report `goal_achieved: false` with the missing JSON, missing evidence, or failing verifier condition. Component completion is only progress evidence until the verifier permits the final claim.
