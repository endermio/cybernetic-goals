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
- batch cadence;
- destructive intermediate-state policy;
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

Steps:

- [ ] [step]
