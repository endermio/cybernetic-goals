# Goal Contract: [Name]

## Human Purpose

[Why this work matters.]

## Objective

[One observable end state.]

## Success Condition

Codex may report `goal achieved: yes` only when:

- the Single target-achieved predicate in `Target Achievement Contract` is satisfied;
- the Purpose Feedback Contract permits an achieved claim;
- the Realization Surface Contract, when applicable, permits the corresponding target-realization claim.

No partial, diagnostic, blocked, invalid, unavailable, fallback, or non-achieved report status may satisfy this success condition.

## Purpose Feedback Contract

| Element | Requirement |
|---|---|
| Beneficiary / observer | [who can observe whether purpose is realized] |
| Purpose-realizing outcome observed | [what observable change counts as purpose achievement] |
| Supporting Evidence | [internal/integration checks that support progress or diagnosis] |
| Sufficient evidence level | `internal / integration / purpose-boundary / operational` |
| Purpose feedback unavailable handling | [honest status and smallest next observation] |
| Allowed completion wording | [achieved / partially observed / pending / unavailable / not required with justification] |

Do not define success as internal sensor success unless the human purpose is internal-state correctness.

## Realization Surface Contract

Use this section when the task changes or realizes target state across controlled-object surfaces.

| Element | Requirement |
|---|---|
| Target state | [state or semantic change that must be realized] |
| Required surfaces | [surface model or classes that carry target-state realization] |
| Surface actions | [act / inspect / preserve / exclude / discover] |
| Residual reconciliation | [old state, unknown surfaces, exclusions, preserved surfaces, and remaining mismatches to account for] |
| RSC status wording | strongest positive target-realization claim requires RSC adequate |
| Partial/unavailable handling | partial, missing, unavailable, or not applicable with justification |
| RSC / PFB boundary | RSC is distinct from Purpose Feedback Boundary; RSC calibrates target-state and surface-closure claims, while PFB calibrates human-purpose realization claims. |

## Target Achievement Contract

| Element | Requirement |
|---|---|
| Single target-achieved predicate | [the only predicate that allows `goal achieved: yes`] |
| Required target-producing evidence | [what must be observed, produced, run, or measured] |
| Allowed achieved claim | [exact wording allowed only when the predicate is met] |

Non-achieved terminal reports are not target states and must not be listed here.

Target Achievement Predicate Fidelity calibrates whether the achieved claim matches the approved predicate. PFB calibrates purpose feedback. RSC calibrates target-state surface closure.

## Source of Truth

Read first:

- [requirements analysis brief]
- [solution design, if Design Gate is required or a design exists]
- [relevant docs]

## Scope and Boundaries

Allowed:

- [allowed areas]

Forbidden unless explicitly approved:

- [forbidden areas]

## Invariants

Do not regress:

- [semantic invariant]
- [security/permission invariant]

## Verification Surface

Supporting Evidence:

- [internal checks, scripts, lint, API smoke, reports, or other sensors]

Focused checks:

- `[command]`

Broader checks:

- `[command]`

Artifact checks:

- [evidence artifacts/logs/evaluation reports]

## Final Output Contract

Use this section when output shape affects execution, acceptance, handoff, persistence, or downstream consumption. For simple tasks, record the safe default briefly or mark `Not required; simple response is sufficient`.

| Element | Requirement |
|---|---|
| Audience | [who consumes the final output] |
| Purpose | [decision / execution / audit / record / handoff / publication / simple response] |
| Medium | [chat / file / markdown report / JSON / table / artifact bundle] |
| Required structure | [sections, tables, fields, schema, artifact bundle, or simple summary] |
| Detail level | [brief / standard / exhaustive] |
| Evidence references required | [yes/no] |
| Machine-readable required | [yes/no] |
| Destination path | [path or not required] |
| Acceptance condition | [what makes the output usable] |

Runtime must not substitute a different audience, purpose, medium, structure, detail level, destination, or machine-readable shape. If this contract is insufficient for execution or acceptance, stop and report the smallest required upstream decision.

## Evaluation Rubric / Error Function

Use this section for audit, evaluation, readiness, closure, completeness, usability, safety, stability, coverage, correctness, or status-classification goals.

| Rubric element | Confirmed meaning |
|---|---|
| Status meanings / pass-fail categories | [confirmed categories] |
| Evidence levels / evidence strength | [strong vs weak evidence] |
| Minimum evidence for strongest positive status | [required evidence] |
| Downgrade rules | [partial, stale, indirect, or missing evidence handling] |
| External/unobservable dependency handling | [credentials, production-only, third-party, environment gaps] |
| Confidence / evidence grade | [whether to report confidence] |

## Checkpoint Loop

For each checkpoint:

1. State checkpoint and expected observable state.
2. Make the smallest coherent change for that checkpoint.
3. Run focused verification.
4. If verification fails, inspect evidence and repair.
5. Update progress log.
6. Run broader verification only at integration gates or final gate.

## Repair Policy

- Use root-cause debugging for unclear failures.
- Do not weaken semantic invariants to satisfy sensors.
- Do not treat stale sensors as authoritative.
- Stop if a confirmed human decision must be changed.

## Progress Log

Maintain:

- `docs/cybernetics/progress/YYYY-MM-DD-slug.md`

Each entry must include:

- checkpoint
- files changed
- commands run
- result
- current risk

## Stop Conditions

Stop successfully when:

- [success condition]

Stop early and report if:

- [blocker]
- [conflict]
- [missing human decision]

## Blocked Report Format

If blocked, report:

- attempted paths
- evidence gathered
- current hypothesis
- exact blocker
- remaining risk
- smallest human decision or input needed

## Final Report Format

When complete, report:

- goal achieved: yes/no
- single target-achieved predicate met: yes/no
- target-producing evidence
- if no: non-achieved reason
- if no: target-producing action attempted or proof of impossibility
- if no: smallest next target-producing attempt
- purpose feedback status: achieved / partially observed / pending / unavailable / not required with justification
- highest purpose-relevant evidence observed
- RSC status: adequate / partial / missing / unavailable / not applicable with justification
- highest target-realization evidence observed
- residuals, unknown surfaces, and smallest next reconciliation
- supporting internal/integration evidence
- not yet observed
- smallest next observation needed
- commands run
- files changed
- known residual risks
