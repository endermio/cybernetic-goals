# Control Structure Review: [Name]

## Review Status

Status: `Needs Revision`

## Inputs Reviewed

- Requirements analysis: `[path]`
- Solution design: `[path or not required]`
- Goal: `[path]`
- Execution policy: `[path]`

## Review Independence

- Subagents authorized: `yes/no`
- Independent review passes completed:
  - Requirement traceability: `yes/no`
  - Design fidelity: `yes/no`
  - Goal fidelity: `yes/no`
  - Sensor governance: `yes/no`
  - Execution cadence: `yes/no`
  - Runtime safety: `yes/no`
- Explicit human approval present: `yes/no`
- Approval allowed: `yes/no`

Notes:

- [independence note]

## Final Observer Check

- Last independent review completed at: `[time or review pass label]`
- Substantive artifact changes after last independent review: `yes/no`
- If yes, final re-review performed: `yes/no`
- Final reviewers confirming no Blocking/Major findings:
  - [reviewer / role]
- Deterministic-only exception used: `yes/no`
- Deterministic guard covering exception:
  - [command/result]
- Approval allowed after final observer check: `yes/no`

Rationale:

- [why the final observed artifact may or may not be approved]

## Structural Lint Result

- [pass/fail summary]

## Requirement Traceability

Findings:

- [finding]

## Goal Fidelity

Findings:

- [finding]

## Design Fidelity

Findings:

- [finding]

## Control Law Quality

Findings:

- [finding]

## Sensor / Test Governance

Findings:

- [finding]

## Batch Rhythm

Findings:

- [finding]

## Semantic vs Tactical Boundary

Findings:

- [finding]

## Runtime Suitability

Findings:

- [finding]

## Critical Findings

- [critical issue]

## Required Revisions

- [revision]

## Non-Critical Suggestions

- [suggestion]

## Convergence Notes

- [what changed across review iterations]

## Approval Conditions

The control structure may be approved only if:

- requirements analysis status is Complete;
- required solution design exists and preserves requirements analysis semantics;
- goal preserves requirements analysis semantics;
- goal and execution policy preserve required design invariants;
- execution policy preserves goal and requirements analysis;
- sensor governance is explicit;
- batch cadence is explicit;
- runtime execution does not need to synthesize a new plan.
- independent review discipline was satisfied or explicit human approval exists.
- no substantive artifact mutation remains unreviewed after the latest independent review.
- any deterministic-only exception is explicitly recorded and guard-covered.

## Final Decision

Status: `Needs Revision`

Rationale:

- [reason]
