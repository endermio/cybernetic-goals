---
name: using-bounded-control-json
description: 'Use when runtime execution is a Level 2 bounded cybernetic JSON goal with fixed meaning and only goal.control.json plus runtime.control.json are present.'
---

# Using Bounded Control JSON

## Overview

Use this skill for Level 2 bounded runtime goals. It is intentionally not the
full pre-goal control-chain executor.

Level 2 keeps its meaning only if it avoids the full
`requirements/design/goal/plan/review/runtime` chain. If execution needs
design, execution policy, review, required-outcome coverage, subagent
coordination, or multi-stage control decisions, stop and route the work to the
full pre-goal flow instead.

## Required Files

Bounded runtime reads only:

- `goal.control.json`
- `runtime.control.json`

It does not require requirements/design/plan/review control JSON.

Runtime writes only:

- `progress.jsonl`
- `runtime-status.json`
- `final-report.json`

Do not rewrite `goal.control.json` or `runtime.control.json` during runtime.

## Validate First

Before executing target work, run:

```bash
python3 .agents/skills/using-bounded-control-json/scripts/validate_bounded_runtime.py docs/cybernetics/runs/<slug>
```

Stop if validation fails. Report the missing bounded field or the smallest
human decision needed to continue.

## Progress And Completion

Append runtime observations to `progress.jsonl` as JSONL events. A required
step is complete only when a passing mainline `step.completed` event names that
step and includes every evidence id listed in `runtime.control.json`.

Before writing `goal_achieved: true`, run:

```bash
python3 .agents/skills/using-bounded-control-json/scripts/verify_bounded_runtime.py docs/cybernetics/runs/<slug>
```

Only a verifier result that permits completion may support
`final-report.json.goal_achieved: true`.

## Short `/goal` Adapter

The `/goal` entry is a short pointer, not a control fact:

```text
/goal Use .agents/skills/using-bounded-control-json and execute docs/cybernetics/runs/<slug>/runtime.control.json. Validate the bounded runtime first. Treat goal.control.json and runtime.control.json as read-only. Write only progress.jsonl, runtime-status.json, and final-report.json. If the bounded JSON is missing, invalid, inconsistent, or insufficient, stop and report the smallest required human decision.
```
