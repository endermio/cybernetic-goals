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

- Execute serially unless review explicitly approves parallel subagents.
- If subagents are used, only one execution subagent is active at a time unless approved.
- Do not let runtime `/goal` rewrite this policy.

## Stop Conditions

Stop if:

- the plan conflicts with requirements analysis or goal;
- the plan conflicts with required solution design;
- confirmed semantics appear wrong or insufficient;
- sensor governance is insufficient for a failing check;
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
