# Execution Policy: [Name]

## Execution Policy Status

Status: `Candidate`

## Source Contracts

- Requirements analysis: `[path]`
- Solution design: `[path or not required]`
- Goal contract: `[path]`

## Superpowers Planning Substrate

- Required substrate: `$superpowers:writing-plans`
- Substrate status: `Required / Used / Blocked / Not required`
- Planning status: `Candidate`

Cybernetic constraints supplied to the substrate:

- confirmed semantic invariants;
- approved or candidate solution-design invariants;
- tactical degrees of freedom;
- dependency matrix;
- context management / execution topology;
- horizon and authority coverage matrix;
- realization surface closure strategy;
- target-producing action strategy;
- execution granularity and sensor budget;
- batch cadence;
- destructive intermediate-state policy;
- output material/evidence collection;
- purpose feedback strategy;
- evidence lifecycle / evidence budget;
- sensor/evidence governance;
- stale sensor retirement and rewrite policy.

If the required substrate is unavailable for a non-trivial execution policy, this policy is blocked and must not be treated as an approved internal substitute.

## Confirmed Semantic Invariants

These cannot be changed during runtime execution without stopping.

- [semantic invariant]

## Tactical Degrees of Freedom

These may change during execution if invariants are preserved.

- [execution detail]
- [workstream organization detail]
- [sensor fixture/detail]

## Dependency Matrix

| Workstream | Owns | Depends on | Can run in parallel with | Gate |
|---|---|---|---|---|
| A | [area] | [dependency] | [parallel work] | [gate] |

## Context Management / Execution Topology

Task level: `Level 0 / Level 1 / Level 2 / Level 3 / Level 4`

Selected topology: `Main-only / Serial subagent-driven / Parallel subagent-driven`

Selected delegation substrate: `bounded-protocol / superpowers-subagent-driven-development / adapter-specific / none`

Topology rationale:

- [why this topology fits the task level, context load, dependency matrix, and review constraints]

Main-only context-load justification:

- [required for Level 3/4 Main-only; explain why the main agent will not become coordinator, worker, integrator, and verifier for context-heavy work]

Main agent owns:

- approved control artifacts
- current batch state
- dispatch
- integration
- progress log
- stop-condition detection

Subagent owns:

- one bounded work package
- one bounded investigation
- one bounded verification pass

Delegation matrix:

| Work package | Executor | Context pack | Allowed actions | Return format | Integration gate |
|---|---|---|---|---|---|
| [package] | `main / serial subagent / parallel subagent` | [artifact paths, files, constraints, stop conditions] | [bounded actions] | [required summary/evidence format] | [main-agent integration condition] |

Context Pack Requirements:

Each delegated work package must define a bounded operating context, not just artifact path names.

| Field | Content |
|---|---|
| Relevant control excerpts | [requirements/design/goal/policy excerpts needed for this package] |
| Current batch objective | [bounded objective for this package] |
| Allowed artifacts/surfaces | [files, documents, commands, or surfaces this package may touch] |
| Forbidden changes | [control artifacts, scope, topology, unrelated surfaces, or other forbidden changes] |
| Required sensors/evidence | [checks, evidence references, or observations this package must return] |
| Stop conditions | [conditions that force the subagent to stop and report rather than continue] |
| Expected return format | [summary/evidence/blocker format required for integration] |

Subagent delegation substrate:

- [Record the approved bounded subagent delegation protocol for serial or parallel subagent-driven topology.]
- [This must match Selected delegation substrate.]
- [Use `superpowers-subagent-driven-development` only when these work packages fit that implementation-plan, current-session workflow; otherwise select `bounded-protocol` or `adapter-specific`.]

Parallel approval record:

- Human approval: `[yes/no; yes or approved required for Parallel subagent-driven]`
- Dependency independence: `[yes/no; yes or approved required for Parallel subagent-driven]`
- Control-review approval: `[yes/no; yes or approved required for Parallel subagent-driven]`

Rules:

- Use `Main-only` for small, local, low-context work.
- Use `Serial subagent-driven` when Level 2 wide inspection or Level 3/4 context load would overload the main agent.
- Use `Parallel subagent-driven` only when Human approval, Dependency independence, and Control-review approval are explicitly `yes` or `approved`.
- The main agent must coordinate, integrate, maintain the progress log, and detect stop conditions.
- A subagent must not modify control artifacts, widen scope, replace topology, or bypass the integration gate.
- Do not treat `$superpowers:subagent-driven-development` as the generic delegation substrate; it applies only when `Selected delegation substrate` is `superpowers-subagent-driven-development` for compatible implementation-plan work packages.
- `Selected delegation substrate: none` is allowed only for `Main-only`.
- If the selected topology becomes insufficient, stop and revise the execution policy; do not let runtime improvise a new topology.

Context Compression Rule:

At each batch boundary, update the progress log with:

- Active control summary: [current requirements, goal invariants, topology, and stop conditions]
- Completed work packages: [packages completed and integrated]
- Subagent outputs integrated: [candidate outputs accepted into main progress state]
- Evidence produced: [evidence references and sensor interpretation]
- Deferred sensors and reasons: [policy-approved deferrals]
- Unresolved blockers: [blockers requiring revision or human input]
- Deviations from policy: [deviations and whether execution must stop]
- Next allowed action: [next policy-approved action]

## Horizon and Authority Coverage Matrix

Use this section for full-route or multi-batch controlled work. Authority limits define runtime handling; they must not silently shrink the approved horizon.

| Batch / surface | In approved horizon? | Runtime authority | Required runtime handling | Counts as achieved? |
|---|---|---|---|---|
| [batch or surface] | `yes/no; if no, cite HSA out-of-scope item` | `execute / prepare-only / observe-only / forbidden-not-executed / explicitly out-of-scope by HSA` | [execute, prepare runbook, observe, report not executed, or exclude by HSA] | [yes/no and claim wording] |

Rules:

- Every approved horizon item must be accounted for as executed, prepared-only, observe-only, forbidden-not-executed, or explicitly out-of-scope by HSA.
- Runtime authority limits change handling, not scope.
- Do not move approved horizon items to future roadmap, handoff, or later goal because they are unauthorized for direct execution.
- Unauthorized live or irreversible actions must be reported as not executed, with required preparation evidence when applicable.
- If the approved horizon itself is too broad, stop and return to requirements/HSA revision instead of narrowing it inside the execution policy.

## Realization Surface Closure Strategy

For compiled runtime goals, always include this section.

When the task changes or realizes target state across controlled-object surfaces, use the full structure below.

If RSC is not applicable, record this compact structure instead:

- RSC status: `RSC not applicable with justification`
- Why no target-state surface closure is required: [reason]
- Why no surface discovery / residual reconciliation is needed: [reason]
- Allowed target-realization wording: [wording]

### Surface Model

| Surface | Role in target realization | Required action | Verification / reconciliation |
|---|---|---|---|
| [surface] | [state carrier / interface / evidence surface / decision point / policy surface / compatibility boundary] | [act / inspect / preserve / exclude / discover] | [how closure, residuals, or bounded status will be checked] |

### Surface Classes

Must act:

- [surface]

Must inspect:

- [surface]

Must preserve:

- [surface and rationale]

Explicitly out of scope:

- [surface and reason]

Unknown or requires discovery:

- [surface or discovery question]

### Residual Reconciliation

After action, reconcile:

- old-state residuals;
- unhandled surfaces;
- unexplained differences;
- preserved or excluded surfaces and rationale;
- surfaces requiring later observation;
- allowed target-realization wording for RSC adequate, partial, missing, unavailable, or not applicable with justification.

Domain adapters own concrete surface discovery and verification methods. The core policy owns surface/action/residual/reconciliation structure.

## Target-Producing Action Strategy

Target-producing action required:

- [the action, probe, experiment, change, or observation that must be attempted to satisfy the single target-achieved predicate]

Proof of impossibility, if any:

- [what would prove the target-producing action cannot be attempted in this environment]

Non-achieved terminal report rule:

- A non-achieved report may be produced only after the target-producing action is attempted and fails, or after impossibility is proven.
- A non-achieved report cannot satisfy the single target-achieved predicate.

## Execution Granularity and Sensor Budget

### Batch Granularity

Each batch must represent a coherent target-state slice, not a mechanical micro-step.

| Batch | Coherent target-state slice | Why this is one batch | Too-small split avoided |
|---|---|---|---|
| Batch 1 | [slice] | [reason] | [micro-split avoided] |

Rules:

- Do not require every micro-step to be openable.
- Intermediate states inside a batch may be broken when this policy explicitly allows it.
- Each batch must end in an openable or meaningfully verifiable state.
- If a batch cannot be verified meaningfully, merge it with the next batch or redefine the gate.
- If a batch is too large to diagnose failures, split by dependency boundary or sensor boundary.

### Sensor Budget

| Batch | Required strong sensors | Optional/weak sensors | Deferred sensors | Final-only sensors |
|---|---|---|---|---|
| Batch 1 | [sensors] | [sensors] | [sensors] | [sensors] |

Rules:

- Use the smallest sensor set that can detect semantic or structural drift.
- Do not run expensive broad checks at every batch unless they are the only reliable drift sensor.
- Treat broad verification as integration-gate or completion-gate work by default.
- If many sensors fail because they encode old semantics, preserve the target state and record stale-sensor retirement or rewrite.

## Batch Cadence

- Intermediate steps inside a batch may temporarily break local observability or artifact consistency when necessary.
- Each batch must end in an openable or meaningfully verifiable state.
- Batch size should avoid both micro-step local minima and huge unobservable changes.

## Destructive Intermediate-State Policy

Allowed inside a batch:

- [temporary breakage]

Not allowed even inside a batch:

- [semantic violation]
- [security/permission violation]

Batch-end requirements:

- [openable/verifiable condition]

## Output Material / Evidence Collection

Use when the goal `Final Output Contract` or design `Output Contract Design` requires structured output. Otherwise record `Not required; final output can be produced from ordinary progress and verification evidence`.

| Required output material | Producing batch/checkpoint | Evidence reference location | Ready before final output? | Missing material blocks completion? |
|---|---|---|---|---|
| [material] | [batch/checkpoint] | [path/section/log] | [yes/no] | [yes/no and reason] |

Final output readiness:

- [what must be ready before final report/output generation]

Blocking missing material:

- [missing material that forces stop or revision]

## Purpose Feedback Strategy

### Internal feedback

- [supports progress/diagnosis, not purpose achievement unless justified]

### Integration feedback

- [shows cross-component or cross-artifact behavior]

### Purpose-boundary feedback

- [smallest feedback that observes the purpose-realizing outcome]

### Operational feedback, if relevant

- [deployment/runtime/external observer evidence]

### Feedback cadence

- Per batch: [feedback used to keep execution oriented]
- Integration gates: [feedback used at integration boundaries]
- Final: [feedback required before claiming purpose achieved]
- Deferred feedback and reason: [feedback not available now and why]

### Evidence unavailable handling

- Verified: [what has been verified]
- Not yet observed: [purpose-relevant outcome not yet observed]
- Smallest next observation: [next feedback needed]
- Allowed completion wording: [achieved / partially observed / pending / unavailable / not required with justification]

## Evidence Lifecycle / Evidence Budget

The evidence lifecycle must keep tracked evidence reviewable and prevent repeated full raw sensor output from outgrowing the controlled work.

| Evidence channel | Raw allowed? | Baseline policy | Per-batch retention | Delta required? | Summary required? | Max tracked size | Git policy | Raw pointer |
|---|---|---|---|---|---|---|---|---|
| [channel] | [yes/no and where raw may live] | [one full baseline / none / external] | [summary + delta / pointer only / retained full with reason] | [yes/no] | [yes/no] | [reviewable budget, cap, or project policy] | [tracked summary/delta only / ignored raw / external artifact] | [path/hash/command when raw exists] |

Rules:

- Keep at most one full baseline and one final full scan unless explicitly justified.
- Intermediate scans should store summary + delta, not repeated full raw hits.
- Full raw sensor output belongs in local cache, ignored artifacts, compressed retained-full artifacts, or external artifact storage unless the goal explicitly requires tracked raw output.
- Tracked evidence must be reviewable without reading all raw sensor output.
- Repeated full snapshots of the same sensor are forbidden unless this policy explains why delta is impossible.
- Each batch must record evidence summary, delta, top offenders or representative samples, and raw pointer when raw output exists.
- Evidence artifacts must not exceed the approved evidence budget without stopping or revising the execution policy.

Evidence levels:

- Level 0 transient raw: local sensor output, ignored by default, may be overwritten.
- Level 1 raw pointer: path, hash, command, timestamp, and retention location.
- Level 2 reviewable summary/delta: tracked summary, delta, top offenders, representative samples, and manifest.
- Level 3 retained full evidence: full baseline or final full scan only when explicitly justified.

## Sensor / Evidence Governance

Approved sensors, checks, and evidence channels are sensors, not objectives.

Strong sensors to preserve:

- [sensor/check/evidence channel]

Weak or stale sensors to inspect before obeying:

- [sensor/check/evidence channel]

Obsolete sensors that may be retired and rewritten:

- [sensor/check/evidence channel]

Target-state evidence has priority over preserving brittle old sensors.

## Stale Sensor Retirement and Rewrite Policy

A sensor, check, or evidence channel may be retired or rewritten when:

- it encodes old requirement semantics;
- it over-constrains execution details;
- it conflicts with confirmed semantic invariants;
- it prevents correct structural change.

Any retired/replaced sensor must be recorded in the progress log with reason and replacement evidence coverage.

## Phase Gates

Before execution:

- control review status must be Approved.

Before moving to next batch:

- current batch-end condition met;
- required strong sensors for this batch have been interpreted;
- deferred and final-only sensors remain deferred by policy, not by omission;
- progress log updated;
- no confirmed semantic invariant violated.

Before completion:

- final verification evidence recorded;
- no unresolved conflict among requirements analysis, solution design when required, goal, plan, and review.

## Execution Rhythm

- Execute according to the selected Context Management / Execution Topology.
- For `Main-only`, keep all target work in the main agent only when the context-load rationale remains valid.
- For `Serial subagent-driven`, only one execution subagent is active at a time.
- For `Parallel subagent-driven`, dispatch only work packages marked independent by the dependency matrix and approved by control review.
- Do not let runtime `/goal` rewrite this policy.

## Stop Conditions

Stop if:

- the plan conflicts with requirements analysis or goal;
- the plan conflicts with required solution design;
- confirmed semantics appear wrong or insufficient;
- sensor governance is insufficient for a failing check;
- the approved execution topology cannot be followed;
- executing further requires a new human decision;
- the approved batch cadence cannot be followed.

## Progress Log Rules

Maintain:

- `docs/cybernetics/progress/YYYY-MM-DD-slug.md`

Each entry must include:

- batch/checkpoint
- files changed
- commands run
- result
- sensor interpretation
- purpose feedback status
- single target-achieved predicate met
- target-producing evidence
- non-achieved reason
- target-producing action attempted or proof of impossibility
- smallest next target-producing attempt
- RSC status
- surfaces acted on or inspected
- residuals and reconciliation
- allowed target-realization wording
- highest purpose-relevant evidence observed
- purpose feedback not yet observed
- smallest next observation needed
- allowed completion wording
- deferred/final-only sensors and reason
- active control summary
- completed work packages
- subagent outputs integrated
- evidence produced
- evidence budget status
- raw evidence generated yes/no
- delta/summary path
- raw pointer/hash
- reason for full snapshot if taken
- tracked evidence size estimate
- unresolved blockers
- deviations from policy
- current risk
- next step

## Candidate Plan Tasks

### Batch 1: [Name]

Goal:

- [target-state slice]

Allowed intermediate breakage:

- [breakage]

Batch-end gate:

- [gate]

Batch sensors:

- Required strong sensors: [sensors]
- Deferred/final-only sensors: [sensors]

Steps:

- [ ] [step]
