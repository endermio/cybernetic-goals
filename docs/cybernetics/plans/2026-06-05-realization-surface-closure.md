# Cybernetic Execution Policy: Realization Surface Closure

## Execution Policy Status

Status: Candidate

## Source Contracts

- Requirements: `docs/cybernetics/requirements/2026-06-05-realization-surface-closure.md`
- Design: `docs/cybernetics/designs/2026-06-05-realization-surface-closure.md`
- Goal: `docs/cybernetics/goals/2026-06-05-realization-surface-closure.md`
- Human approval for this pre-goal compilation: user explicitly invoked `$orchestrating-cybernetic-pregoal` and allowed subagent review.

## Superpowers Planning Substrate

- Substrate status: Used.
- Selected substrate: `superpowers:writing-plans` for implementation-plan structure and `superpowers:subagent-driven-development` as the runtime delegation substrate.
- Why used: the eventual runtime work is a multi-artifact repository change with review checkpoints and bounded implementation batches.
- Scope limit: this pre-goal policy prepares the runtime plan; it does not execute target implementation.

## Confirmed Semantic Invariants

- RSC is a core invariant, not a software-only adapter rule.
- RSC is not a new workflow gate.
- RSC and PFB remain separate feedback loops.
- Surface/action/residual/reconciliation is the shared core structure.
- Domain adapters own discovery and verification mechanics.
- Local action must not be reported as global target-state realization when realization surfaces are distributed.

## Tactical Degrees of Freedom

Runtime implementers may choose exact wording, test file names, and section placement when the meaning stays aligned with the approved requirements and design.

Runtime implementers may not:

- remove PFB calibration;
- hard-code software-specific surface examples as core requirements;
- skip residual scan and artifact-to-invariant reconciliation;
- start parallel target-work subagents without the approved topology and context packs;
- claim RSC implementation complete from documentation edits alone without tests or residual checks.

## Dependency Matrix

| Workstream | Depends on | Produces | Notes |
|---|---|---|---|
| RSC core semantics propagation | Requirements and design | Updated skill and template language | Must preserve RSC/PFB boundary. |
| Goal and runtime claim calibration | Goal contract and existing compiler behavior | Updated goal/runtime wording | Must prevent local-action overclaim. |
| Review, matrix, tests, evals | Stable section names and invariant ID | RSC review dimension and regressions | Should cover false overclaim and non-applicable cases. |
| Residual scan and reconciliation | All implementation edits | Surface closure report and test evidence | Must explain old-state residuals or scope exclusions. |

## Context Management / Execution Topology

Task level: Level 3

Selected topology: Serial subagent-driven

Selected delegation substrate: `superpowers-subagent-driven-development`

Topology rationale:

The runtime implementation touches multiple shared control artifacts and needs independent completeness review, but the artifacts are coupled enough that unrestricted parallel edits would create merge and semantic drift risk. Serial subagent-driven execution allows bounded worker context for discovery, implementation, residual scan, and review without turning independent edits loose on the same files.

Main agent owns:

The main agent owns source-contract interpretation, progress log maintenance, artifact integration, guard execution, final review integration, and final completion wording.

Main-only justification:

Not applicable. The selected topology is serial subagent-driven.

Subagent delegation substrate:

Use the approved `superpowers-subagent-driven-development` substrate for runtime work. This refers to the `$superpowers:subagent-driven-development` skill when runtime invokes it. Only one execution subagent may be active at a time unless a later control review explicitly approves parallelization.

Parallelization approval:

- Human approval: no
- Dependency independence demonstrated: not approved for runtime target work
- Control-review approval required before any parallel runtime target-work subagents: yes

### Delegation Matrix

| Work package | Executor | Context pack | Allowed actions | Return format | Integration gate |
|---|---|---|---|---|---|
| Surface discovery | Subagent or main agent | Requirements, design, current artifact inventory, invariant matrix | Inspect files and propose affected artifacts | Surface inventory with must-act, must-inspect, preserve, exclude, unknown | Main agent approves before edits. |
| Core artifact implementation | Main agent with optional subagent draft | Approved surface inventory and source contracts | Edit skill docs, templates, matrix, tests in assigned scope | Diff summary mapped to surfaces and tests run | Main agent runs guard and lint. |
| Residual reconciliation | Subagent reviewer | Full diff and approved RSC model | Search for missing invariant consumers and old local-action wording | Residual report with explained leftovers | Required before review. |
| Independent review | Subagent reviewer | Final candidate diff, requirements, design, goal, plan | Review only, no edits | Blocking/Major/Minor findings by file or artifact | Blocking/Major findings must be resolved or explicitly returned to user. |

### Context Pack Requirements

| Field | Required content |
|---|---|
| Relevant control excerpts | Objective, invariants, RSC surface model, PFB boundary, stop conditions. |
| Current batch objective | The single work package objective assigned to that subagent. |
| Allowed artifacts/surfaces | Exact files, directories, or surface classes assigned for inspection or edit. |
| Forbidden changes | Runtime target work outside assigned surfaces, PFB weakening, software-specific core policy, unapproved parallelization. |
| Required sensors/evidence | Focused tests, `rg` scans, guard output, residual reconciliation notes, or review findings as applicable. |
| Stop conditions | Scope expansion, conflicting artifacts, guard failure after correction, Blocking/Major issue outside assigned authority. |
| Expected return format | Summary, files inspected or changed, surface mapping, commands run, findings by severity, residuals, next recommended gate. |

Subagents must not approve their own implementation work. The main agent may perform discovery or residual scan for small batches when context remains bounded; subagent review remains required for independent review and for any work package where context size or risk justifies delegation.

### Context Compression Rule

| Field | Required content |
|---|---|
| Active control summary | Current objective, source artifacts, selected topology, and active batch. |
| Completed work packages | Work packages completed with artifact paths and guard status. |
| Subagent outputs integrated | Reviewer or worker outputs already reconciled into main artifacts. |
| Evidence produced | Commands, tests, scans, review summaries, and compiler output already collected. |
| Deferred sensors and reasons | Purpose feedback, operational checks, or adapter-specific checks that remain pending and why. |
| Unresolved blockers | Blocking/Major findings or guard failures that still need action. |
| Deviations from policy | Any change to scope, topology, sensor budget, or batch cadence. |
| Next allowed action | The next action permitted by the approved execution policy and guards. |

## Realization Surface Closure Strategy

### Surface Model

| Surface | Role in target realization | Required action | Verification / reconciliation |
|---|---|---|---|
| Requirements skill and template | Recognize RSC semantics and high-value questions | act | Check RSC appears before downstream planning and stays distinct from PFB. |
| Goal skill and template | Preserve RSC in success and final report contracts | act | Check local action cannot be worded as global realization. |
| Execution policy skill and template | Operationalize surface/action/residual/reconciliation | act | Check policy requires surface classes and residual reconciliation. |
| Control review skill and template | Judge RSC adequacy semantically | act | Check review can classify adequate, partial, missing, unavailable, and not applicable with justification. |
| Runtime compiler skill and generated `/goal` text | Calibrate runtime execution and completion claims | act | Check runtime instructions preserve RSC status and residual reporting. |
| Invariant matrix | Publish cross-artifact consumer responsibility | act | Check `INV-RSC-001` maps to all consumers. |
| Tests and evals | Prevent regression | act | Check positive, negative, and not-applicable-with-justification cases. |
| Domain adapters | Supply field-specific surface discovery | inspect | Check core language leaves adapter mechanics outside the core invariant. |

### Surface Classes

Must act:

- core skill instructions that define requirement, goal, execution, review, and runtime behavior;
- reusable templates consumed by those skills;
- invariant matrix and regression tests.

Must inspect:

- README or framework docs that list core control flow or invariant semantics;
- existing guard scripts for section-presence opportunities;
- existing PFB tests to avoid boundary collision.

Must preserve:

- PFB claim-calibration rules;
- context topology and evidence budget rules;
- adapter-specific responsibilities outside core.

Explicitly out of scope:

- domain-specific software code completeness adapter implementation;
- broad rewrite of all cybernetic skills;
- forced e2e or terminal evidence gate.

Unknown or requires discovery:

- any additional docs that define cross-artifact invariant consumers;
- eval runner schema requirements for any new evals.

### Residual Reconciliation

After runtime implementation, reconcile:

- any core artifact that should consume `INV-RSC-001` but was not updated;
- any remaining wording that treats local action as global realization;
- any RSC wording that collapses into PFB;
- any domain-specific example that reads as universal core policy;
- any test gap that would allow RSC to disappear from the chain.

## Execution Granularity and Sensor Budget

Runtime work should use five batches:

1. Add focused tests or evals for RSC propagation and local-action overclaim.
2. Update core skill instructions and templates with domain-neutral RSC sections.
3. Update invariant matrix, compiler wording, and final-report claim calibration.
4. Run residual scans and reconcile affected surfaces.
5. Run verification and independent review.

Do not split each file into its own batch unless a test failure requires isolation. Do not collapse all updates into one unreviewed edit.

### Sensor Budget

- Static/internal sensors: `rg` scans, schema-aware checks where available, template existence checks.
- Integration sensors: skill repository tests and control-chain guard tests.
- Pre-goal control sensors: generated artifacts and runtime `/goal` behavior must express RSC accurately.
- Operational sensors: not required for this invariant-only repository change unless tests reveal external tooling dependency.

Escalation trigger:

Run focused tests and structural guards by default. Run broader repository tests only if shared skill behavior, compiler behavior, guard behavior, or invariant matrix behavior changes.

## Batch Cadence

Use five batches: tests/evals, core artifact propagation, review/runtime/matrix propagation, residual reconciliation, final verification/review. Each batch should have one integration point and one concise progress entry.

## Destructive Intermediate-State Policy

Do not use destructive git commands. Do not revert user changes. If a batch creates an intermediate failing state, keep it bounded to the batch and run the next planned correction before reporting completion.

## Output Material / Evidence Collection

Collect only concise command summaries, reviewer findings, residual scan results, and changed-file summaries. Avoid copying full artifact content into progress logs when files exist on disk.

## Purpose Feedback Strategy

### Internal feedback

Static scans, tests, and compiler output support diagnosis and artifact consistency. Together with review, they can support integration/control approval for this pre-goal chain; target-purpose boundary feedback remains pending until runtime implementation is exercised on a concrete task.

### Integration feedback

The complete artifact chain and runtime compiler output show whether RSC propagates through the control system.

### Purpose-boundary feedback

For this pre-goal task, approved artifacts and compiled `/goal` are integration/control evidence, not target-purpose boundary feedback. Target-purpose boundary feedback remains pending until the runtime implementation is executed and later exercised on a concrete task with distributed realization surfaces.

### Operational feedback

Deferred. Actual future operator benefit can only be observed after the runtime implementation is executed and later used on tasks with distributed realization surfaces.

### Evidence unavailable handling

If target implementation is not executed in this turn, report the pre-goal chain as approved or not approved, and report implementation as pending.

## Evidence Lifecycle / Evidence Budget

Collect concise evidence only:

- guard command and result;
- lint command and result;
- reviewer finding summary;
- compiler command and result;
- residual risk summary.

Do not paste full artifact content into progress logs after files exist on disk.

## Sensor / Evidence Governance

Evidence must be interpreted by what it observes:

- internal scans can detect missing sections or residual wording;
- tests can detect propagation regressions;
- review can judge RSC semantic adequacy;
- runtime compiler output can show final instruction shape;
- none of these alone should be overclaimed as future operator success.

## Stale Sensor Retirement and Rewrite Policy

Re-run relevant guards or tests after any substantive artifact change. If independent review results are recorded mechanically without changing reviewed semantics, no new review cycle is required. If design, goal, or policy semantics change after review, run a focused re-review.

## Phase Gates

- Before edits: requirements, design, goal, and execution policy must be approved.
- Before review: implementation must provide RSC surface mapping, tests, and residual reconciliation.
- Before completion: independent review must have no unresolved Blocking or Major findings.
- Before final claim: runtime wording must distinguish RSC status, PFB status, and pending implementation observations.

## Execution Rhythm

Proceed batch by batch. Integrate subagent output after each assigned package. Re-run focused checks after semantic artifact changes. Keep final reporting calibrated to observed evidence.

## Stop Conditions

Stop runtime work if RSC/PFB separation cannot be preserved, if domain-specific mechanics are being promoted into core policy, if guards fail repeatedly, or if independent review finds unresolved Blocking or Major issues.

## Runtime Task Checklist

1. Add regression coverage for `INV-RSC-001`.
   - Create or update focused tests for RSC section propagation, local-action overclaim prevention, and RSC-not-applicable-with-justification behavior.
   - Run the focused tests and confirm they fail before implementation when practical.

2. Update core requirements and design-facing artifacts.
   - Add RSC responsibility to requirements analysis.
   - Add or update template sections for surface/action/residual/reconciliation.
   - Keep RSC separate from PFB and from workflow fit.

3. Update goal, execution policy, and review artifacts.
   - Add RSC contract wording to goal templates and skill instructions.
   - Add RSC strategy to execution policy templates and progress log rules.
   - Add RSC adequacy review classification to review templates and skill instructions.

4. Update runtime compiler and invariant matrix.
   - Add runtime claim-calibration wording for RSC.
   - Add `INV-RSC-001` to the invariant consumer matrix.
   - Add only structural guard checks if they are low-risk and clearly section-presence based.

5. Reconcile residual surfaces.
   - Scan for local-action-as-global-realization wording.
   - Scan for software-specific RSC wording in core.
   - Explain intentional leftovers or defer them with owner and reason.

6. Verify and review.
   - Run focused tests.
   - Run broader skill repository tests relevant to cybernetic artifacts.
   - Run control compiler checks if updated.
   - Request independent review before claiming the runtime implementation is complete.

## Progress Log Rules

Each progress entry should record:

- batch name and status;
- surfaces acted on or inspected;
- residuals and reconciliation;
- commands run and summarized results;
- next gate.

Add purpose feedback status, RSC status, allowed completion wording, and smallest next observation only when they change or affect completion wording.

## Completion Rule

The runtime implementation may be reported complete only if:

- all required surfaces are acted on or reconciled;
- RSC status is adequate for any strongest positive target-realization claim;
- partial, pending, unavailable, or not-applicable RSC forces matching partial, pending, unavailable, or justified not-applicable wording;
- PFB status is honestly calibrated;
- guards and focused tests pass or failures are explicitly accepted by the user;
- independent review has no unresolved Blocking or Major findings.
