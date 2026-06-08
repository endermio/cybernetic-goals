# Goal Contract: [Name]

## Human Purpose

[Why this work matters.]

## Objective

[One observable end state.]

## Success Condition

Codex may report `goal achieved: yes` only when:

- the What counts as done in `What Counts As Done` is satisfied;
- the How We Know The User Purpose Was Met permits an achieved claim;
- the Where The Result Must Show Up, when applicable, permits the corresponding result claim.

No partial, diagnostic, blocked, invalid, unavailable, fallback, or report-when-not-done status may satisfy this success condition.

## How We Know The User Purpose Was Met

| Element | Requirement |
|---|---|
| Beneficiary / observer | [who can observe whether purpose is realized] |
| Purpose-realizing outcome observed | [what observable change counts as purpose achievement] |
| Supporting Evidence | [internal/integration checks that support progress or diagnosis] |
| Sufficient evidence level | `internal / integration / purpose-limit / operational` |
| If user-purpose evidence unavailable | [honest status and smallest next observation] |
| Allowed completion wording | [achieved / partially observed / pending / unavailable / not required with justification] |

Do not define success as internal evidence check success unless the human purpose is internal-state correctness.

## Where The Result Must Show Up

Use this section when the task changes or realizes intended result across controlled-object result places.

| Element | Requirement |
|---|---|
| Intended result | [state or meaning change that must be realized] |
| Required result places | [result place model or classes that carry intended-result realization] |
| Place actions | [act / inspect / preserve / exclude / discover] |
| Residual reconciliation | [old state, unknown result places, exclusions, preserved result places, and remaining mismatches to account for] |
| Result-placement wording | strongest positive result claim requires result-placement adequate |
| Partial/unavailable handling | partial, missing, unavailable, or not applicable with justification |
| Distinction from user-purpose evidence | result-placement is distinct from How We Know The User Purpose Was Met; result-placement evidence supports intended-result claims while user-purpose evidence supports purpose claims. |

## What Counts As Done

| Element | Requirement |
|---|---|
| What counts as done | [the only what counts as done that allows `goal achieved: yes`] |
| Evidence needed to call it done | [what must be observed, produced, run, or measured] |
| Allowed achieved claim | [exact wording allowed only when the what counts as done is met] |
| Steps that make the result true | [state-transition path or execution-policy required answer path that produces the what counts as done] |

report when not done are not intended results and must not be listed here.

The achieved claim must match what counts as done. User-purpose evidence and result-placement evidence are separate checks.

## Work Covered And Allowed Actions Contract

| Element | Requirement |
|---|---|
| Work covered in this run | [complete execution scope approved for this goal; do not shrink it to the first safe segment] |
| What the agent may do | [actions runtime may execute directly] |
| Forbidden actions | [live, remote, destructive, irreversible, or externally risky actions runtime must not execute] |
| Prepare-only / observe-only actions | [actions in the work covered in this run that runtime may only prepare, observe, document, or report not executed] |
| Explicitly out-of-scope items | [items excluded from this goal by requirements approval, not merely unauthorized] |
| Work coverage rule | [how every work covered in this run item is accounted for: executed / prepared-only / forbidden-not-executed / explicitly out-of-scope by requirements approval] |

Authority limits change runtime handling, not the work covered in this run. Do not move work covered in this run items to future roadmap or handoff unless What the User Approved explicitly excludes them from this goal.

## Source of Truth

Read first:

- [requirements analysis brief]
- [solution design, if required design is required or a design exists]
- [relevant docs]

## Allowed And Forbidden Work

Allowed:

- [allowed areas]

Forbidden unless explicitly approved:

- [forbidden areas]

## Rules That Must Not Change

Do not regress:

- [meaning rule]
- [security/permission rule]

## Verification Checks

Supporting Evidence:

- [internal checks, scripts, lint, API smoke, reports, or other evidence checks]

Focused checks:

- `[command]`

Broader checks:

- `[command]`

Artifact checks:

- [evidence artifacts/logs/evaluation reports]

## Final Answer Format

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

Use this section for audit, evaluation, readiness, result placement, completeness, usability, safety, stability, coverage, correctness, or status-classification goals.

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
6. Run broader verification only at integration gates or final check.

## Repair Policy

- Use root-cause debugging for unclear failures.
- Do not weaken meaning rules that cannot change to satisfy evidence checks.
- Do not treat stale evidence checks as authoritative.
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
- what counts as done met: yes/no
- target-producing evidence
- if no: not done reason
- if no: target-producing action attempted or proof of impossibility
- if no: smallest next target-producing attempt
- work covered in this run
- work covered in this run coverage: complete / partial / unavailable / explicitly bounded by requirements approval
- executed
- prepared-only
- forbidden-not-executed
- explicitly out-of-scope by requirements approval
- user purpose evidence status: achieved / partially observed / pending / unavailable / not required with justification
- highest purpose-relevant evidence observed
- Result-placement status: adequate / partial / missing / unavailable / not applicable with justification
- highest result claim evidence observed
- residuals, unknown result places, and smallest next reconciliation
- supporting internal/integration evidence
- not yet observed
- smallest next observation needed
- commands run
- files changed
- known residual risks
