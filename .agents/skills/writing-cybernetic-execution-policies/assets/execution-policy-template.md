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
- execution granularity and sensor budget;
- batch cadence;
- destructive intermediate-state policy;
- output material/evidence collection;
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

- Human approval: `[required only for Parallel subagent-driven]`
- Dependency independence: `[required only for Parallel subagent-driven]`
- Control-review approval: `[required only for Parallel subagent-driven]`

Rules:

- Use `Main-only` for small, local, low-context work.
- Use `Serial subagent-driven` when Level 2 wide inspection or Level 3/4 context load would overload the main agent.
- Use `Parallel subagent-driven` only when dependency independence is explicit and human + control-review approval exists.
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
- deferred/final-only sensors and reason
- active control summary
- completed work packages
- subagent outputs integrated
- evidence produced
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
