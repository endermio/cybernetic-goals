# Cybernetic Solution Design: Realization Surface Closure

## Design Status

Status: Candidate

## Source Contracts

- Requirements brief: `docs/cybernetics/requirements/2026-06-05-realization-surface-closure.md`
- Required invariant: `INV-RSC-001: Realization Surface Closure`
- Required scope: cybernetic-goals core invariant, not a software-only adapter rule.
- Required gates: Output Contract, Design, Goal Contract, Execution Policy, Control Review, Risk.
- Required boundary: RSC calibrates target-state and surface-closure claims; PFB calibrates human-purpose realization claims.

## Human Purpose

Prevent cybernetic-goals from treating a local action as if a distributed target state has been realized across the controlled object.

## Confirmed Semantics

- Realization Surface Closure is the core invariant to add.
- It applies when a task changes or realizes target state across controlled-object surfaces.
- It is domain-neutral and adapter-extensible.
- It is separate from Purpose Feedback Boundary.
- It should appear as a cross-artifact invariant, not a new workflow stage.

## Design Substrate

- Design Gate: Required by the requirements brief.
- Brainstorming substrate: Not required; the requirements already define the accepted conceptual direction.
- Output contract source: requirements brief plus the RSC/PFB boundary described below.

## Problem Model

The current core control chain can define purpose, requirements, design, goal, execution policy, review, and purpose feedback. It still lacks a domain-neutral way to require that a target state be mapped onto the controlled object's realization surfaces before local action is treated as global realization.

The failure mode is local action being mistaken for target-state realization:

- a document conclusion changes while the evidence table remains stale;
- a process diagram changes while forms, permissions, and notifications remain unchanged;
- a metric name changes while extraction, cleaning, thresholding, and interpretation remain old;
- a code entry point changes while schemas, callers, fixtures, tests, and docs retain old semantics.

Software code-change completeness is therefore an adapter instance, not the core concept.

## Design Intent

Introduce Realization Surface Closure as a cross-artifact invariant:

```text
target state
-> realization surfaces
-> required actions
-> residual checks
-> reconciliation status
```

This invariant forces execution policies and reviews to account for where the target state is carried by the controlled object, without hard-coding software-specific discovery or verification methods into the core.

## Conceptual Design

### Core Concepts

- Target state: the state or semantic change the task exists to realize.
- Realization surface: any part of the controlled object that carries, exposes, enforces, records, explains, or operationalizes that target state.
- Surface role: why the surface matters for realization, such as state carrier, interface, decision point, evidence surface, operator path, policy surface, or compatibility boundary.
- Required action: how the surface must be handled: act, inspect, preserve, exclude, or mark unknown.
- Residual: old state, inconsistent state, unhandled surface, unexplained mismatch, or intentionally preserved compatibility surface.
- Reconciliation: the post-action account that explains whether each relevant surface is closed, intentionally preserved, out of scope, unknown, unavailable, or pending later observation.

### RSC Status Categories

- RSC adequate: relevant surfaces are identified, required actions are completed or justified, and residuals are reconciled.
- RSC partial: important surfaces are covered but some residuals, unknowns, or later observations remain.
- RSC missing: local action is used as proof of global realization without surface coverage.
- RSC unavailable: surface closure cannot be observed in the current environment and is honestly bounded.
- RSC not applicable: the task does not change or realize target state across a controlled object surface, with justification.

### Relationship To Purpose Feedback Boundary

RSC and PFB are separate loops:

- RSC asks whether the controlled object's realization surfaces were covered and reconciled.
- PFB asks whether the human purpose was observed as realized by the relevant beneficiary or observer.

RSC can support PFB, but it does not replace PFB. PFB can be partially observed while RSC remains incomplete, and RSC can be adequate while PFB remains pending.

## Design Boundaries

### Inside Scope

- Define `INV-RSC-001` as a core invariant.
- Add a domain-neutral realization surface model to core artifacts.
- Require execution policies to classify surfaces and plan residual reconciliation.
- Require reviews to judge RSC adequacy without turning RSC into a hard workflow gate.
- Compile runtime instructions that prevent local action from being reported as global realization.
- Preserve domain adapter responsibility for discovery and verification mechanics.

### Outside Scope

- Do not create a software-only code completeness gate as the core solution.
- Do not require every task to perform heavy exhaustive discovery.
- Do not make RSC a separate stage before routing or before execution.
- Do not let deterministic guards judge semantic adequacy of surface coverage.
- Do not collapse RSC into PFB or use RSC evidence to claim purpose achieved.

## Alternatives Considered

### Software Adapter Only

Rejected as the core solution. It handles one important failure mode but misses the more general target-state realization problem in research, process, experimental, data, and document tasks.

### Domain Completeness Strategy Only

Rejected as too vague. A generic field without surface, action, residual, and reconciliation structure is likely to become inert documentation.

### Hard Realization Surface Gate

Rejected. RSC should shape requirements, execution policy, review, and runtime claims, but it should not become a new workflow stage that blocks all progress when closure is unavailable.

### Cross-Artifact Invariant

Accepted. RSC belongs in the same control family as PFB: a semantic invariant propagated through requirements, goal contracts, execution policies, reviews, runtime compiler output, matrix documentation, and tests.

## Detailed Design

### Requirements

Requirements analysis must identify when a task changes or realizes target state across a controlled object. It should define:

- target state;
- likely realization surfaces;
- surface roles;
- surface action classes;
- residual risks;
- relationship between RSC and PFB;
- sufficient evidence for RSC adequacy.

### Goal Contract

Goal contracts must preserve RSC as a success constraint. A goal may define successful target-state realization only when RSC is adequate: relevant surfaces are acted on or inspected as planned, preserve/exclude cases are justified, unknowns are resolved or bounded without hiding risk, and residuals are reconciled.

Deferred, pending, unavailable, or partial RSC must force partial, pending, unavailable, or handoff wording rather than a strongest positive target-realization claim.

The goal should not define success as "a local action was completed" when the target state is distributed across multiple surfaces.

### Execution Policy

Execution policies must include a Realization Surface Closure strategy:

| Surface | Role in target realization | Required action | Verification / reconciliation |
|---|---|---|---|
| Controlled object surfaces | Carry or expose target-state semantics | act / inspect / preserve / exclude / unknown | residual scan, review, or justified bounded status |

The policy must also classify:

- must act;
- must inspect;
- must preserve;
- explicitly out of scope;
- unknown or requires discovery.

### Control Review

Control review must assess RSC adequacy as a semantic review dimension:

- whether the policy identifies the realization surfaces that carry the target state;
- whether local action is being overclaimed as global realization;
- whether residuals and unknown surfaces are reconciled;
- whether adapter-specific discovery and verification are assigned to the correct layer;
- whether RSC status is distinguished from PFB status.

### Runtime Compiler

Runtime `/goal` instructions must include claim calibration:

- do not claim target-state realization from local action alone when RSC is required;
- report surfaces covered, residuals reconciled, surfaces pending, and unknowns;
- keep RSC status separate from PFB status;
- use domain adapters only for domain-specific surface discovery and verification.

### Invariant Matrix

The invariant matrix must add `INV-RSC-001` and identify artifact consumers:

- requirements;
- design;
- goal;
- execution policy;
- review;
- runtime compiler;
- tests and evals;
- domain adapters.

## Adapter Boundary

Core owns the invariant shape:

```text
surface
role
required action
residual
reconciliation
status
```

Domain adapters own discovery and verification mechanics. Examples:

- software adapter: files, call sites, APIs, schemas, mocks, fixtures, docs, tests, migrations;
- research adapter: claims, evidence tables, citations, inclusion criteria, limitations;
- experiment adapter: protocols, instruments, sampling, data sheets, analysis scripts;
- process adapter: roles, forms, notifications, permissions, audit records, training material.

The core must not encode these adapter lists as universal requirements.

## Error Model

RSC should catch these error classes:

- Local action overclaim: one changed artifact is treated as full target-state realization.
- Surface omission: important realization surfaces are not discovered or classified.
- Residual old state: old semantics remain without reconciliation.
- Adapter leakage: software-specific or other domain-specific mechanics are embedded in core.
- False PFB substitution: RSC evidence is used to claim the human purpose was observed.
- Overcontrol: RSC is applied to tasks where no distributed target-state realization exists.
- Unavailable feedback misreported: unavailable closure is presented as adequate closure.

## Output Contract Design

The runtime implementation should produce:

- updated core skill and template text for RSC;
- updated invariant matrix row for `INV-RSC-001`;
- focused tests or evals that verify RSC propagation and prevent local-action overclaim;
- no runtime target-work execution during pre-goal compilation.

## Design-to-Goal Mapping

- Goal objective must name RSC as the target core invariant.
- Goal success must distinguish pre-goal compilation from later runtime implementation.
- Goal invariants must preserve RSC/PFB separation.
- Goal final reporting must avoid claiming target implementation during pre-goal compilation.

## Design Decisions

- RSC is a core invariant, not a software-specific gate.
- RSC is a cross-artifact semantic constraint, not a new workflow stage.
- Deterministic guards may check RSC section presence later, but semantic adequacy belongs to review.
- PFB remains responsible for human-purpose realization and final claim calibration.
- RSC remains responsible for controlled-object realization surface closure.

## Design-to-Execution Mapping

- Execution policy must plan artifact updates across core consumers.
- Runtime work should start with tests/evals that encode the invariant shape and failure modes.
- Runtime work should update documentation and templates before compiler wording when practical, so downstream runtime text can consume stable section names.
- Runtime review must include residual scan across core artifacts to avoid partial propagation.

## Design Review Requirements

- Confirm requirements traceability for `INV-RSC-001`.
- Confirm RSC and PFB remain separate.
- Confirm the design does not encode software-specific adapter mechanics as universal core policy.
- Confirm execution policy can operationalize surface/action/residual/reconciliation without excessive workflow weight.
- Confirm runtime wording can calibrate target-realization claims.

## Open Design Questions

None.
