# Cybernetic Requirements Analysis: Realization Surface Closure

## Requirements Analysis Status

Status: `Complete`

## Human Purpose

Add a core cybernetic invariant that keeps target realization from collapsing
into local action. When a task changes or realizes a target state, the system
must identify the surfaces that carry the change, classify how each surface is
handled, and reconcile residual old state after execution.

The purpose is to make "local action succeeded" distinct from "the controlled
object reached the intended target state across its realization surface."

## Current Understanding

The requested capability is a core invariant named `Realization Surface
Closure` (`INV-RSC-001`). It generalizes software "code change completeness"
into a domain-neutral control requirement:

```text
target state
-> realization surfaces
-> required surface action / inspection / preservation / exclusion
-> residual reconciliation
-> calibrated completion claim
```

Software impact-surface completeness is one domain adapter instance. The core
invariant must remain domain-neutral and avoid hard-coding software terms such
as files, call sites, schemas, mocks, type checks, or API contracts.

## Context Inspected

- User-provided RSC framing in chat.
- `$routing-cybernetic-workflows` decision: Level 3, with Rubric, Output
  Contract, Design, Goal Contract, Execution Policy, and Control Review gates.
- `.agents/skills/analyzing-cybernetic-requirements/assets/requirements-analysis-template.md`
- `docs/cybernetic-framework/invariant-artifact-consumer-matrix.md`
- Existing invariant patterns: `INV-PFB-001`, `INV-EVD-001`, `INV-TOP-*`,
  `INV-SEN-001`.
- Existing execution-policy and control-review templates for Purpose Feedback,
  Evidence Lifecycle, Sensor Governance, and Context Topology.

## Requirement Semantics

### Core Terms / Objects / Actors

| Term | Requirement meaning | Notes |
|---|---|---|
| Realization Surface Closure | A core invariant requiring target-state changes to be mapped to the surfaces that carry them and reconciled after action. | Short name: `RSC`. |
| Realization surface | Any part of the controlled object that carries, exposes, preserves, transforms, records, enforces, or communicates the target state. | Domain-neutral; adapters define concrete surfaces. |
| Surface model | The structured list or matrix of realization surfaces and their role in realizing the target state. | Belongs in execution policy after requirements/design establish the target state. |
| Surface action | How a surface must be handled: act, inspect, preserve, exclude, or discover. | Exact action mechanisms are domain-specific. |
| Residual old state | Remaining old semantics, obsolete behavior, stale evidence, old process state, conflicting claims, or unhandled target-state carriers after action. | Residuals may be acceptable only when explained and bounded. |
| Reconciliation | Post-action accounting that compares target realization needs with acted/inspected/preserved/excluded/unknown surfaces and explains residuals. | Prevents local action from being treated as global realization. |
| Domain adapter | A domain-specific realization-surface discovery and verification method. | Software, experiment, research, data-analysis, and organization-process adapters are examples. |
| Purpose Feedback Boundary | The boundary where human-purpose realization is observed and completion claims are calibrated. | RSC supports PFB but does not replace it. |

### Confirmed Semantics

- RSC is a core invariant, not a software-specific checklist.
- Code change completeness is an RSC domain adapter instance, not the core
  concept.
- Core RSC requires surface modeling, surface classification, residual
  reconciliation, and completion-claim calibration.
- Domain adapters may define discovery and verification mechanics for their
  surfaces.
- Core artifacts must not hard-code software terms as the general rule.
- Local action is not sufficient evidence of global target-state realization.
- RSC is distinct from PFB:
  - RSC asks whether the controlled object's realization surfaces are closed.
  - PFB asks whether the human purpose has been observed as realized.
- Strong RSC evidence can support PFB, but cannot by itself prove purpose
  achievement when purpose-boundary feedback is required.
- Partial PFB evidence can exist while RSC remains incomplete if old surfaces or
  residual state remain unaccounted.

### Boundaries

Inside scope:

- Add `INV-RSC-001` as a core invariant.
- Define domain-neutral RSC terms: surface, action, inspection, preservation,
  exclusion, unknown/discovery, residual, reconciliation.
- Add an execution-policy structure for surface model, surface classes, and
  residual reconciliation.
- Add a review dimension for Realization Surface Closure adequacy.
- Add runtime completion-claim calibration for unhandled surfaces and residuals.
- Add matrix coverage and regression tests/evals.
- Preserve adapter separation: core requires RSC; adapters define domain
  discovery and verification methods.

Outside scope:

- Do not create a software-only `Code Change Completeness Gate` as the core
  invariant.
- Do not hard-code `rg`, typecheck, mocks, schemas, API contracts, or software
  workflows into core cybernetic skills.
- Do not require full RSC detail for trivial tasks where no target state is
  changed or realized across multiple surfaces.
- Do not let RSC replace PFB, evidence lifecycle, context topology, or control
  review.
- Do not add a separate heavyweight workflow stage when the same invariant can
  be carried through requirements, design, execution policy, review, and
  runtime.

## Requirements Control Map

| Control element | Current analysis |
|---|---|
| Objective | Add a domain-neutral Realization Surface Closure invariant so target-state changes identify, handle, and reconcile their realization surfaces. |
| Controlled object | The cybernetic core skill chain and its control artifacts, especially execution-policy writing, control review, runtime compilation, matrix tracking, and tests/evals. |
| Candidate sensors | Template presence checks, invariant matrix tests, skill text/eval checks, runtime compiler output checks, control review section checks, residual-reconciliation examples. |
| Candidate actuators | Skill documentation, templates, review rubric, runtime compiler, deterministic guards when structural presence becomes required, invariant matrix, regression tests/evals. |
| Constraints | Keep RSC domain-neutral; preserve PFB separation; avoid software-specific core language; use review for semantic adequacy; use guards only for structure/explicit values where feasible. |
| Disturbances | Overfitting RSC to software, creating empty boilerplate sections, confusing RSC with PFB, over-controlling simple tasks, treating unhandled surfaces as automatic failure, letting residuals remain unreported. |
| Stop conditions | Stop if design would make RSC a software checklist; stop if runtime could claim target realization while unknown surfaces or residuals are unreported; stop if RSC conflicts with PFB completion calibration. |

## Purpose Feedback Boundary

| Element | Value |
|---|---|
| Human purpose | Improve the cybernetic core so AI execution accounts for the realization surface of target-state changes instead of mistaking local action for global realization. |
| Beneficiary / observer | Maintainer, future Codex agents, control-reviewers, and domain-adapter authors. |
| Purpose-realizing outcome | The skill chain contains a reviewed, tested RSC invariant that requires surface modeling and residual reconciliation while keeping domain details in adapters. |
| Feedback needed | Requirements/design/goal/plan/review/runtime artifacts preserve RSC; tests/evals catch missing RSC propagation and false completion from local action alone. |
| Internal sensors role | Unit tests, matrix tests, and text scans can prove structural propagation and selected negative cases; they cannot prove every future domain adapter chooses adequate surfaces. |
| Sufficient evidence level | `integration` for core invariant propagation; `purpose-boundary` when future users apply RSC to a real task and avoid local-action false completion. |
| If feedback unavailable | Report core propagation verified and real-task purpose feedback pending; identify the smallest next observation as applying RSC to a concrete domain task. |

## Blocking Human Decisions

| Decision | Why it matters | Recommended default | Risk if wrong |
|---|---|---|---|
| None blocking for requirements analysis | The user has already specified core invariant scope, PFB separation, and adapter relationship. | Proceed with the RSC invariant as a core cross-artifact requirement. | Low for requirements; downstream design can refine artifact placement and guard strictness. |

## Default Assumptions

These are reasonable defaults and should not block progress unless the human disagrees.

- RSC is implemented as a cross-artifact invariant, not a new workflow stage.
- Execution policy is the primary artifact that records the operational surface
  model and residual reconciliation strategy.
- Solution design may define domain-neutral concepts and adapter hooks when
  structure synthesis is needed.
- Control review judges RSC semantic adequacy.
- Deterministic guards may later check section presence and explicit values, but
  semantic surface adequacy remains review-governed.
- Runtime completion wording is calibrated when surfaces are unknown,
  unhandled, intentionally preserved, or residuals remain.
- RSC should be required when a task changes or realizes a target state across
  more than a trivial local surface.
- RSC can be marked not applicable with justification for simple direct tasks,
  pure questions, or tasks that do not change/realize a target state.

## Evaluation Rubric / Error Function

| Rubric element | Confirmed meaning |
|---|---|
| Status meanings / pass-fail categories | `RSC adequate`: relevant surfaces are identified, classified, acted/inspected/preserved/excluded, and residuals reconciled. `RSC partial`: important surfaces are handled but residuals, unknowns, or later observations remain with honest status. `RSC missing`: local action is treated as target realization without surface model or reconciliation. `RSC unavailable`: environment or domain constraints prevent surface observation; smallest next discovery/observation is recorded. `RSC not applicable`: no target-state realization across surfaces, with justification. |
| Evidence levels / evidence strength | Strong evidence: surface model plus post-action reconciliation and residual accounting. Medium evidence: surface model plus planned reconciliation but incomplete execution evidence. Weak evidence: local action, internal checks, or final purpose feedback without surface accounting. |
| Minimum evidence for strongest positive status | `RSC adequate` is required: relevant surface classes are populated; required actions are completed; preserved or excluded surfaces have rationale; unknowns are resolved or explicitly bounded without hiding risk; old-state residuals are scanned/accounted; completion wording matches closure status. Deferred, pending, unavailable, or partial RSC cannot support a strongest positive target-realization claim. |
| Downgrade rules | Missing surface classes downgrade to partial or missing. Unexplained residuals downgrade to partial or missing depending on risk. Deferred, pending, unavailable, or partial RSC must force partial/pending/unavailable wording. Domain-specific checks without a surface model remain supporting evidence only. Heavy end-to-end purpose feedback does not upgrade RSC when old surfaces remain unaccounted. |
| External/unobservable dependency handling | Mark RSC unavailable or partial when surfaces require unavailable credentials, production-only systems, external actors, or inaccessible artifacts; record smallest next discovery/observation. |
| Confidence / evidence grade | RSC review should report confidence or evidence grade when surfaces are inferred, incomplete, externally constrained, or adapter-defined. |

## Output Contract

| Element | Requirement |
|---|---|
| Audience | Maintainer, future Codex agents, reviewers, and downstream cybernetic skill invocations. |
| Purpose | Requirements handoff for designing and implementing `INV-RSC-001` across the core skill chain. |
| Medium | Requirements markdown now; later artifacts include design, goal, execution policy, review, runtime compiler changes, invariant matrix row, tests, and evals. |
| Required structure | This brief must define RSC semantics, PFB boundary, evaluation rubric, adapter separation, required gates, non-goals, and deferred design questions. |
| Detail level | Standard; enough for solution design without freezing exact template wording or guard implementation. |
| Evidence references required | Yes; downstream work must reference this requirements path and existing matrix/template/test patterns. |
| Machine-readable required | Not for this brief. Later tests/evals may be JSON or Python. |
| Destination path | `docs/cybernetics/requirements/2026-06-05-realization-surface-closure.md` |
| Acceptance condition | A solution designer can produce a domain-neutral RSC model and downstream artifact plan without inventing the invariant semantics or confusing RSC with PFB. |

## Required Gates

| Gate | Status | Reason |
|---|---|---|
| Semantic Gate | `satisfied` | The requirement is to add RSC as a core invariant and preserve adapter separation. |
| Rubric Gate | `satisfied` | This brief defines RSC adequate, partial, missing, unavailable, and not-applicable meanings. |
| Output Contract Gate | `required` | RSC must appear in stable artifact sections/templates, matrix rows, tests/evals, and runtime wording. |
| Design Gate | `required` | Artifact placement, adapter hook shape, review dimension, runtime compiler wording, and guard scope require a solution model. |
| Goal Contract Gate | `required` | Runtime execution must preserve RSC semantics, non-goals, and completion-calibration constraints. |
| Execution Policy Gate | `required` | Implementation spans multiple skills/templates/tests and needs controlled batching and sensor strategy. |
| Control Review Gate | `required` | RSC semantic adequacy and over/under-control risk need independent review. |
| Risk Gate | `required` | The main risks are framework over-specialization, boilerplate inflation, and false completion claims. |

## Deferred Solution Design Questions

These belong in `$designing-cybernetic-solutions`, not requirements analysis.

- Which artifacts own RSC source fields: requirements, solution design, goal,
  execution policy, review, runtime, or all of them?
- What exact execution-policy section should represent Surface Model, Surface
  Classes, and Residual Reconciliation?
- Should goal contracts include a compact RSC contract, or should they reference
  execution-policy RSC strategy only?
- What exact control-review dimension and classifications should be used for RSC
  adequacy?
- What runtime compiler clauses should calibrate completion claims when RSC is
  partial, unavailable, or not applicable?
- Which deterministic guard checks are appropriate immediately: section
  presence only, review independence marker, or no guard until templates settle?
- What minimum negative tests/evals should prove local action is not accepted as
  global realization?
- How should domain adapters declare their surface discovery and verification
  methods without making core adapter-specific?
- How should RSC interact with Context Management / Execution Topology when
  surface discovery or reconciliation is delegated to subagents?

## Deferred Planning / Execution Details

- Exact file edit order.
- Exact test names and eval prompt wording.
- Whether to add a new `tests/skills/test_realization_surface_closure.py` or
  extend existing invariant/evidence/runtime tests.
- Whether `control_chain_guard.py` should immediately reject missing RSC sections
  or wait until the section format is stable.
- Whether runtime compiler changes are wording-only or require parsing execution
  policy RSC classifications.
- Whether existing historical artifacts need migration; default is no migration.

## Questions for Human

No blocking questions for requirements analysis. The conservative defaults below
are safe enough to proceed to solution design.

## Proposed Defaults

If the human says "按默认继续", proceed with:

- Add `INV-RSC-001` as a domain-neutral core invariant.
- Add RSC to execution-policy template as the main operational strategy section.
- Add RSC adequacy to control-review template and review skill.
- Add runtime completion-calibration wording for unhandled surfaces and residuals.
- Add matrix coverage and focused regression tests/evals.
- Keep deterministic guards limited to structure/explicit markers if added.
- Leave historical `docs/cybernetics/**` artifacts unchanged.
- Defer domain-specific surface discovery details to adapters.

## Confirmed Requirement Decisions

- RSC is the core concept; software code completeness is one adapter instance.
- The invariant name is `INV-RSC-001: Realization Surface Closure`.
- Core language must be domain-neutral.
- RSC requires surface modeling, action/inspection/preservation/exclusion
  classification, and residual reconciliation.
- RSC supports but does not replace Purpose Feedback Boundary.
- Domain adapters define how surfaces are discovered, acted on, inspected, and
  verified.
- Local action alone is insufficient evidence of target-state realization.
- Residual old state must be reported, reconciled, or explicitly deferred.
- Unknown surfaces must be discovered or bounded before claiming closure.

## Non-Goals

- No software-specific core checklist.
- No default requirement that every trivial task carries a full RSC table.
- No replacement of PFB, Evidence Lifecycle / Evidence Budget, Context
  Management / Execution Topology, or Sensor / Evidence Governance.
- No broad migration of historical control artifacts.
- No semantic adequacy judgment inside deterministic guards.
- No domain adapter implementation in this requirements step.

## Candidate Sensors / Evidence Needs

- Requirements, design, goal, execution policy, review, runtime compiler, and
  matrix artifacts reference `INV-RSC-001` consistently.
- Execution-policy template includes domain-neutral RSC structure.
- Control-review template includes an RSC adequacy dimension and classification.
- Runtime compiler output includes completion-claim calibration for RSC partial,
  unavailable, and residual states.
- Tests/evals reject a plan that performs local action without identifying or
  reconciling realization surfaces.
- Tests/evals accept a simple not-applicable case with justification to prevent
  over-control.
- Matrix row identifies source skill, artifact field/template, guard status,
  review dimension, compiler/downstream consumer, and regression coverage.
