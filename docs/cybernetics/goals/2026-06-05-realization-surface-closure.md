# Cybernetic Goal Contract: Realization Surface Closure

Status: Candidate

## Objective

Integrate Realization Surface Closure as a cybernetic-goals core invariant so tasks that realize a target state must identify, act on or inspect, and reconcile the controlled object's relevant realization surfaces before local action is treated as global realization.

## Human Purpose

Prevent the control system from treating a locally completed action as if the target state has been realized across the controlled object. The user wants a domain-neutral invariant that captures the general failure behind incomplete code changes, stale research evidence, partial process updates, incomplete experiment changes, and inconsistent data-analysis semantics.

## Success Condition

Success means the pre-goal artifacts define and approve an implementable control structure for `INV-RSC-001`, and the compiled runtime `/goal` can be used later to perform the target implementation. During this pre-goal run, success does not include modifying core skill files or starting runtime target work.

The target implementation is successful only after approved runtime work later demonstrates that:

- RSC is represented in the relevant core artifacts;
- RSC remains domain-neutral;
- RSC and PFB are not collapsed;
- execution policy and review can classify surface/action/residual/reconciliation;
- final completion wording cannot claim target-state realization from local action alone when RSC is required.

## Purpose Feedback Contract

| Element | Value |
|---|---|
| Beneficiary / observer | The user and future operators of cybernetic-goals who rely on the core control chain to avoid partial target-state realization. |
| Purpose-realizing outcome observed | Pre-goal artifact objective satisfied: artifacts consistently encode the intended RSC implementation contract and compile a runtime command that preserves the implementation boundary. Target-purpose feedback remains pending until the runtime implementation is executed and exercised on a concrete distributed target-state task. |
| Supporting Evidence | Requirements validation, design/goal/policy artifact consistency, orchestration guards, independent control review, runtime compiler output. |
| Sufficient evidence level | Integration/control evidence for this pre-goal run: approved artifact chain plus compiled runtime `/goal`. Target-purpose boundary feedback is deferred by design. |
| Purpose feedback unavailable handling | Do not claim the core invariant is implemented during pre-goal compilation. Report the approved pre-goal status, unexecuted runtime work, and the smallest next observation: run the compiled `/goal` and verify implementation artifacts. |
| Allowed completion wording | "Pre-goal compilation approved and runtime `/goal` compiled; target implementation not executed in this turn." |

## Source of Truth

- Requirements: `docs/cybernetics/requirements/2026-06-05-realization-surface-closure.md`
- Design: `docs/cybernetics/designs/2026-06-05-realization-surface-closure.md`
- Execution policy: `docs/cybernetics/plans/2026-06-05-realization-surface-closure.md`
- Control review: `docs/cybernetics/control-reviews/2026-06-05-realization-surface-closure.md`

## Scope and Boundaries

### In Scope

- Create design, goal, execution policy, control review, progress, orchestration status, and compiled runtime command artifacts.
- Define the runtime implementation contract for RSC.
- Allow independent subagent review of pre-goal artifacts, because the user authorized subagent review.
- Stop before starting target implementation.

### Out Of Scope

- Modify core skills, templates, tests, scripts, or invariant matrix during pre-goal compilation.
- Execute the compiled runtime `/goal`.
- Treat RSC as a software-only code completeness feature.
- Treat RSC as an e2e or PFB replacement.
- Add a new workflow stage or heavy gate unless later implementation review proves it necessary.

## Invariants

- `INV-RSC-001` must remain domain-neutral.
- RSC asks whether target-state realization surfaces are covered and reconciled.
- PFB asks whether the human purpose was observed as realized.
- RSC evidence may support PFB but must not replace PFB.
- Local action is not sufficient evidence of global realization when target state is distributed across realization surfaces.
- Domain adapters may define discovery and verification mechanics; the core owns surface/action/residual/reconciliation structure.
- Deterministic guards should not judge semantic adequacy of RSC unless the future implementation explicitly limits them to section-presence checks.

## Realization Surface Contract

| Surface | Role in target realization | Required action | Verification / reconciliation |
|---|---|---|---|
| Requirements analysis | Defines RSC semantics, rubric, and high-value questions | act | Confirm RSC appears as a requirement-analysis responsibility and does not absorb PFB. |
| Goal contracts | Preserve RSC as a success and completion-claim constraint | act | Confirm goal success separates target-state closure from local action and PFB. |
| Execution policies | Operationalize surface/action/residual/reconciliation planning | act | Confirm a reusable RSC strategy exists and includes residual reconciliation. |
| Control reviews | Assess RSC adequacy semantically | act | Confirm review can classify adequate, partial, missing, unavailable, and not applicable with justification cases. |
| Runtime compiler | Calibrates final target-realization claims | act | Confirm compiled `/goal` forbids local action overclaim and reports residual surface status. |
| Invariant matrix and tests | Keep RSC from drifting out of the control chain | act | Confirm `INV-RSC-001` consumers and focused regressions exist. |
| Domain adapters | Provide domain-specific surface discovery and verification | inspect | Confirm core does not hard-code software-specific lists as universal requirements. |

## Verification Surface

- `check_pregoal_inputs.py` validates the requirements artifact before orchestration.
- `orchestration_guard.py` validates stage transitions.
- `control_artifact_lint.py` validates generated artifacts before review and compile.
- Independent subagent review checks traceability, RSC/PFB boundary, execution topology, and runtime claim calibration.
- `control_chain_guard.py` validates the complete approved chain before runtime compilation.
- `compile_runtime_goal.py` produces the final `/goal` command without executing it.

## Final Output Contract

The final response for this pre-goal run must include:

- created artifact paths;
- review status;
- guard/compiler verification summary;
- compiled runtime `/goal` command or path;
- explicit statement that runtime target implementation was not started.

## Blocked Report Format

If blocked, report:

- blocker;
- artifact or guard that surfaced it;
- attempted corrections;
- whether runtime target work remains unstarted;
- smallest user decision or repository change needed to continue.

## Progress Log Contract

Progress must be tracked at:

`docs/cybernetics/progress/2026-06-05-realization-surface-closure.md`

The progress log must distinguish:

- pre-goal artifact completion;
- review evidence;
- RSC status for the pre-goal chain;
- PFB status for the pre-goal chain;
- unexecuted runtime implementation work.

## Stop Conditions

Stop and return to the user if:

- requirements are no longer complete;
- design, goal, policy, or review cannot preserve RSC/PFB separation;
- control review finds Blocking or Major issues that cannot be corrected in this turn;
- deterministic guards fail after three consecutive correction attempts;
- runtime compile would require starting target implementation.

## Final Report Format

- purpose feedback status: pre-goal artifact objective satisfied; target-purpose feedback pending;
- highest purpose-relevant evidence observed: approved integration/control artifact chain plus compiled runtime `/goal`;
- RSC status: pre-goal chain adequate if review approves;
- supporting internal/integration evidence: guard, lint, and compiler commands;
- not yet observed: implemented core invariant in repository artifacts;
- smallest next observation needed: run the compiled `/goal` to implement and verify RSC;
- files created or changed;
- known residual risks.
