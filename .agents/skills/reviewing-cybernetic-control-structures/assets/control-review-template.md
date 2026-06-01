# Control Structure Review: [Name]

## Review Status

Status: `Needs Revision`

## Inputs Reviewed

- Requirements analysis: `[path]`
- Solution design: `[path or not required]`
- Goal: `[path]`
- Execution policy: `[path]`

## Review Independence

- Pre-goal review subagents authorized: `yes/no`
- Independent review passes completed:
  - Requirement traceability: `yes/no`
  - Design fidelity: `yes/no`
  - Output contract fidelity: `yes/no`
  - Goal fidelity: `yes/no`
  - Context management / execution topology: `yes/no`
  - Execution granularity / sensor load: `yes/no`
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

## Output Contract Fidelity

Check:

- requirements `Output Contract` is preserved in goal `Final Output Contract`;
- design `Output Contract Design`, if present, is preserved in goal and execution policy;
- execution policy collects material needed for the final output;
- runtime `/goal` cannot replace audience, purpose, medium, structure, detail level, destination, or machine-readable shape.

Findings:

- [finding]

## Control Law Quality

Findings:

- [finding]

## Context Management / Execution Topology

Check:

- selected topology is explicit;
- Level 3/4 main-only execution has a context-load justification;
- delegated work packages define Context pack, Allowed actions, Return format, and Integration gate;
- context packs include relevant control excerpts, current batch objective, allowed artifacts/surfaces, forbidden changes, required sensors/evidence, stop conditions, and expected return format;
- parallel subagent-driven execution has explicit human approval, dependency independence, and control-review approval;
- subagents cannot modify control artifacts, widen scope, replace topology, or bypass integration gates;
- main agent owns dispatch, integration, progress log, and stop-condition detection;
- context compression is defined for batch boundaries;
- subagent outputs remain candidate results until main-agent integration;
- context overload is not assigned to the main agent.

Findings:

- [finding]

## Execution Granularity / Sensor Load

Check:

- batches are coherent target-state slices, not mechanical micro-steps;
- the plan chooses the largest coherent batch that remains diagnosable;
- broad verification is assigned to integration or final gates unless justified;
- sensor cost does not dominate execution cost;
- stale sensors cannot block approved structural change without sensor-governance review.

Findings:

- [finding]

## Sensor / Evidence Governance

Findings:

- [finding]

## Evidence Lifecycle / Evidence Budget

Check:

- execution policy does not store repeated full raw sensor outputs per batch;
- raw evidence volume cannot exceed the controlled work size without justification;
- intermediate evidence records summary and delta instead of only full raw output;
- tracked evidence is reviewable;
- raw, pointer, summary/delta, and retained-full retention policy exists;
- evidence files are referenced by indexed summaries or raw pointer rather than loaded as context;
- reviewers do not need to read raw evidence to approve;
- evidence artifacts are separated into transient raw, raw pointer, reviewable summary/delta, and retained full classes;
- repeated full snapshots of the same sensor are justified only when delta is impossible.

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
- any upstream output contract is preserved in the goal and supported by the execution policy;
- execution policy preserves goal and requirements analysis;
- execution topology is explicit and does not create main-agent context overload;
- execution granularity and sensor load do not create micro-step overcontrol or sensor overcoupling;
- evidence lifecycle keeps tracked evidence reviewable and prevents raw sensor output explosion;
- sensor/evidence governance is explicit;
- batch cadence is explicit;
- runtime execution does not need to synthesize a new plan.
- independent review discipline was satisfied or explicit human approval exists.
- no substantive artifact mutation remains unreviewed after the latest independent review.
- any deterministic-only exception is explicitly recorded and guard-covered.

## Final Decision

Status: `Needs Revision`

Rationale:

- [reason]
