# Goal Contract: [Name]

## Human Purpose

[Why this work matters.]

## Objective

[One observable end state.]

## Success Condition

Codex may stop only when:

- [condition]
- [verification evidence]

## Source of Truth

Read first:

- [clarification brief]
- [relevant docs]

## Scope and Boundaries

Allowed:

- [allowed areas]

Forbidden unless explicitly approved:

- [forbidden areas]

## Invariants

Do not regress:

- [semantic invariant]
- [security/permission invariant]

## Verification Surface

Focused checks:

- `[command]`

Broader checks:

- `[command]`

Artifact checks:

- [screenshots/logs/eval reports]

## Checkpoint Loop

For each checkpoint:

1. State checkpoint and expected observable state.
2. Make the smallest coherent change for that checkpoint.
3. Run focused verification.
4. If verification fails, inspect evidence and repair.
5. Update progress log.
6. Run broader verification only at integration gates or final gate.

## Repair Policy

- Use root-cause debugging for unclear failures.
- Do not weaken semantic invariants to pass tests.
- Do not treat stale tests as authoritative sensors.
- Stop if a confirmed human decision must be changed.

## Progress Log

Maintain:

- `docs/superpowers/progress/YYYY-MM-DD-slug.md`

Each entry must include:

- checkpoint
- files changed
- commands run
- result
- current risk
- next step

## Stop Conditions

Stop successfully when:

- [success condition]

Stop early and report if:

- [blocker]
- [conflict]
- [missing human decision]

## Blocked Report Format

If blocked, report:

- attempted paths
- evidence gathered
- current hypothesis
- exact blocker
- remaining risk
- smallest human decision or input needed

## Final Report Format

When complete, report:

- goal achieved
- verification evidence
- commands run
- files changed
- known residual risks
- recommended next action
