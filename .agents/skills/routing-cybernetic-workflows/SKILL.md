---
name: routing-cybernetic-workflows
description: 'Use when a formed task needs a cybernetic control-entry decision, strategy policy, required gates, or a handoff away from pre-task intent.'
---

# Routing Cybernetic Workflows

## Overview

Choose whether this formed task should use a cybernetic controlled run. Do not
classify by Levels.

This skill routes only. It does not analyze requirements, design, write goals,
write plans, review, create files, or execute target work.

If input is pre-task intent, confusion, dissatisfaction, risk sense, observed
symptoms, failed experience, method preference, or process distrust, use
`$framing-cybernetic-intent` before routing.

References:

- `references/routing-detailed-rules.md`
- `references/response-shapes.md`

## Core Decision

Ask:

```text
Should this use ordinary direct work, bounded_runtime, or controlled_run?
```

- `ordinary_direct_work`: use normal Codex execution; no cybernetic run.
- `bounded_runtime`: fixed small task with `goal.control.json` and
  `runtime.control.json`; uses `using-bounded-control-json`.
- `controlled_run`: official JSON run with requirements, `run.control.json`,
  current generation runtime, review, and counterexample gate.

Use `controlled_run` only when runtime would otherwise invent or revise user
meaning, solution structure, work strategy, evidence checks, phase checks,
blocked claims, or completion claims.

## Controlled Run Fields

When `controlled_run` is selected, record:

- `strategy_policy`: `frozen_strategy` or `reviewed_replanning`.
- `gates`: always include `counterexample_gate`; add `human_gate` or
  `live_gate` for human-approved or live/destructive actions.
- `required_checks`: rubric, output contract, design, data-plane, or deployment
  checks as needed.

Risk does not choose the strategy policy. Risk only adds gates.

## Gate Meaning

Structural gates check whether control files are well formed and consistent:
schema validation, `control_chain_guard`, `validate_control_chain`, and
`verify_runtime_progress`.

Quality gate means `counterexample_gate`: an independent reviewer tries to show
that the proposed control chain narrowed the task, accepted substitute work, or
made a bad blocked/completion claim.

Structural gates are necessary but never quality approval.

## Required Response

Every response includes:

1. `Control entry decision`: `ordinary_direct_work`, `bounded_runtime`, or
   `controlled_run`.
2. `Why`.
3. `strategy_policy`, only for `controlled_run`.
4. `gates`.
5. `required_checks`.
6. `recommended next step`.
7. `rejected path`, if useful.

Do not create files. Handoff prompts are response-only.

## Checklist

- [ ] Pre-task intent is routed to framing first.
- [ ] The response does not use Level names.
- [ ] `counterexample_gate` is present for every `controlled_run`.
- [ ] Validator/guard/verifier are described as structural gates only.
- [ ] Human/live risk is represented as `human_gate` or `live_gate`.
- [ ] Recommendation is response-only.
