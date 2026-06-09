# Execution Policy: [Name]

## Execution Policy Status

Status: `Candidate`

## Source Contracts

- Requirements analysis: `[path]`
- Solution design: `[path or not required]`
- Goal: `[path]`

## Superpowers Planning Workflow

- Required workflow: `$superpowers:writing-plans`
- Workflow status: `Required / Used / Blocked / Not required`
- Planning status: `Candidate`

Task constraints supplied to the workflow:

- rules that cannot change;
- approved or candidate solution-design rules;
- tactical degrees of freedom;
- dependency matrix;
- who does the work / context use;
- subagent execution mode and concurrency policy;
- work coverage and action limits matrix;
- where the result must show up;
- required answer path;
- action that can make it done strategy;
- work size and evidence check budget;
- batch cadence;
- destructive intermediate-state policy;
- output material/evidence collection;
- purpose feedback strategy;
- evidence lifecycle / evidence budget;
- evidence check/evidence governance;
- stale evidence check retirement and rewrite policy.

If the required workflow is unavailable for a non-trivial execution policy, this policy is blocked and must not be treated as an approved internal substitute.

## Rules That Cannot Change

These cannot be changed during runtime execution without stopping.

- [meaning rule]

## Tactical Degrees of Freedom

These may change during execution if rules that cannot change are preserved.

- [execution detail]
- [workstream organization detail]
- [evidence check fixture/detail]

## Dependency Matrix

| Workstream | Owns | Depends on | Can run in parallel with | Check |
|---|---|---|---|---|
| A | [area] | [dependency] | [parallel work] | [check] |

## Who Does The Work / Context Use

Task level: `Level 0 / Level 1 / Level 2 / Level 3 / Level 4`

Who does the work: `Main-only / Serial subagent-driven / Parallel subagent-driven`

Selected agent workflow: `bounded-protocol / superpowers-subagent-driven-development / superpowers-dispatching-parallel-agents / adapter-specific / none`

Subagent execution mode: `none / serial-single-active / parallel-max-safe`

Max concurrent subagents: `1 / auto / N`

Agent workflow compatibility:

Use `.agents/skills/references/delegation-workflow-registry.json` as the source of workflow capability limits.

| Selected agent workflow | Allowed work assignment | Allowed mode |
|---|---|---|
| `superpowers-subagent-driven-development` | `Serial subagent-driven` | `serial-single-active` |
| `superpowers-dispatching-parallel-agents` | `Parallel subagent-driven` | `parallel-max-safe` |
| `bounded-protocol` | `Serial subagent-driven / Parallel subagent-driven` | `serial-single-active / parallel-max-safe` |
| `adapter-specific` | `Serial subagent-driven / Parallel subagent-driven` | `serial-single-active / parallel-max-safe` |
| `none` | `Main-only` | `none` |

Agent workflow compatibility rationale:

- [required when What the User Approved workflow preference is not used or when a requested workflow is incompatible with the selected work assignment/mode]

Concurrency selection rationale:

- [why serial-single-active or parallel-max-safe is selected; if max-safe-parallel was requested but safe frontier is 1, explain why]

Concurrency frontier rule:

- [which work packages can launch together after dependencies are satisfied]

Conflict / lock model:

| Artifact / state / shared place | Lock owner | Conflict rule |
|---|---|---|
| [place] | [main / work package / not shared] | [disjoint / exclusive lock / read-only / barrier required] |

Parallel wave matrix:

| Wave | Required-step frontier | Work packages | Independence proof | Shared places / locks | Integration barrier |
|---|---|---|---|---|---|
| [Wave 1] | [required step(s) whose dependencies are satisfied] | [packages] | [why they can run together] | [locks or disjoint places] | [main-agent barrier] |

Failure policy:

- [what happens when one subagent blocks, fails, or returns conflicting evidence]

Main-agent integration rule:

- [when candidate outputs become accepted progress state]

Work Assignment rationale:

- [why this work assignment fits the task level, context load, dependency matrix, and review constraints]

Main-only context-load justification:

- [required for Level 3/4 Main-only; explain why the main agent will not become coordinator, worker, integrator, and verifier for context-heavy work]

Main agent owns:

- approved approved files
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

| Work package | Executor | Context pack | Allowed actions | Return format | Integration check |
|---|---|---|---|---|---|
| [package] | `main / serial subagent / parallel subagent` | [artifact paths, files, constraints, stop conditions] | [bounded actions] | [required summary/evidence format] | [main-agent integration condition] |

Context Pack Requirements:

Each delecheckd work package must define a bounded operating context, not just artifact path names.

| Field | Content |
|---|---|
| Relevant control excerpts | [requirements/design/goal/policy excerpts needed for this package] |
| Current batch objective | [bounded objective for this package] |
| Allowed artifacts/places | [files, documents, commands, or places this package may touch] |
| Forbidden changes | [approved files, scope, work assignment, unrelated places, or other forbidden changes] |
| Required evidence checks/evidence | [checks, evidence references, or observations this package must return] |
| Stop conditions | [conditions that force the subagent to stop and report rather than continue] |
| Expected return format | [summary/evidence/blocker format required for integration] |

Subagent workflow:

- [Record the approved bounded subagent delegation protocol for serial or parallel subagent-driven work assignment.]
- [This must match Selected agent workflow.]
- [Use `superpowers-subagent-driven-development` only for `Serial subagent-driven` + `serial-single-active` + `Max concurrent subagents: 1`.]
- [Use `superpowers-dispatching-parallel-agents` only for `Parallel subagent-driven` + `parallel-max-safe` under the approved wave/lock/barrier/integration structure.]

Parallel approval record:

- Human approval: `[yes/no; yes or approved required for Parallel subagent-driven]`
- Dependency independence: `[yes/no; yes or approved required for Parallel subagent-driven]`
- Control-review approval: `[yes/no; yes or approved required for Parallel subagent-driven]`

Rules:

- Use `Main-only` for small, local, low-context work.
- Use `Serial subagent-driven` when Level 2 wide inspection or Level 3/4 context load would overload the main agent.
- Use `Parallel subagent-driven` only when Human approval, Dependency independence, and Control-review approval are explicitly `yes` or `approved`; pair it with `Subagent execution mode: parallel-max-safe`.
- Use `Serial subagent-driven` with `Subagent execution mode: serial-single-active` and `Max concurrent subagents: 1`.
- The main agent must coordinate, integrate, maintain the progress log, and detect stop conditions.
- A subagent must not modify approved files, widen scope, replace work assignment, or bypass the integration check.
- Do not treat `$superpowers:subagent-driven-development` as the generic agent workflow; it is serial-single-active only.
- Do not use `$superpowers:subagent-driven-development` with `parallel-max-safe`; use `superpowers-dispatching-parallel-agents`, `bounded-protocol`, or `adapter-specific` for max-safe parallel execution.
- `Selected agent workflow: none` is allowed only for `Main-only`.
- If the selected work assignment becomes insufficient, stop and revise the execution policy; do not let runtime improvise a new work assignment.

Context Compression Rule:

At each batch break, update the progress log with:

- Active control summary: [current requirements, goal rules that cannot change, work assignment, and stop conditions]
- Completed work packages: [packages completed and integrated]
- Subagent outputs integrated: [candidate outputs accepted into main progress state]
- Evidence produced: [evidence references and evidence check interpretation]
- Deferred evidence checks and reasons: [policy-approved deferrals]
- Unresolved blockers: [blockers requiring revision or human input]
- Deviations from policy: [deviations and whether execution must stop]
- Next allowed action: [next policy-approved action]

## Work Coverage And Action Limits Matrix

Use this section for full-route or multi-batch controlled work. Authority limits define runtime handling; they must not silently shrink the work covered in this run.

| Work item / place | In work covered in this run? | What the agent may do | Required runtime handling | Counts as achieved? |
|---|---|---|---|---|
| [batch or place] | `yes/no; if no, cite What the User Approved out-of-scope item` | `execute / prepare-only / observe-only / forbidden-not-executed / explicitly out-of-scope by what the user approved` | [execute, prepare runbook, observe, report not executed, or exclude by What the User Approved] | [yes/no and claim wording] |

Rules:

- Every work covered in this run item must be accounted for as executed, prepared-only, observe-only, forbidden-not-executed, or explicitly out-of-scope by what the user approved.
- What the agent may do limits change handling, not scope.
- Do not move work covered in this run items to future roadmap, handoff, or later goal because they are unauthorized for direct execution.
- Unauthorized live or irreversible actions must be reported as not executed, with required preparation evidence when applicable.
- If the work covered in this run itself is too broad, stop and return to requirements/What the User Approved revision instead of narrowing it inside the execution policy.

## Where The Result Must Show Up

For compiled runtime goals, always include this section.

When the task changes or realizes intended result across controlled-object places, use the full structure below.

If result placement is not applicable, record this compact structure instead:

- Result placement status: `not applicable with justification`
- Why no intended-result result placement is required: [reason]
- Why no place discovery / residual reconciliation is needed: [reason]
- Allowed result claim wording: [wording]

### Places The Result Appears

| Place | Role in result claim | Required action | Verification / reconciliation |
|---|---|---|---|
| [place] | [state carrier / interface / evidence place / decision point / policy place / compatibility point] | [act / inspect / preserve / exclude / discover] | [how result placement, residuals, or bounded status will be checked] |

### Place Classes

Must act:

- [place]

Must inspect:

- [place]

Must preserve:

- [place and rationale]

Explicitly out of scope:

- [place and reason]

Unknown or requires discovery:

- [place or discovery question]

### Residual Reconciliation

After action, reconcile:

- old-state residuals;
- unhandled places;
- unexplained differences;
- preserved or excluded places and rationale;
- places requiring later observation;
- allowed result claim wording for result-placement adequate, partial, missing, unavailable, or not applicable with justification.

Domain adapters own concrete place discovery and verification methods. The core policy owns place/action/residual/reconciliation structure.

## Steps That Make The Result True

For implementation work, decompose by the state transitions that make the result true, not by component inventory.

| Required step | Required state transition | Required evidence |
|---|---|---|
| [S1] | [initial/intermediate state -> next state] | [evidence that this transition is satisfied] |

Rules:

- Every mainline work package must map to at least one required step.
- Supporting-only work must be marked as supporting-only and cannot satisfy goal progress by itself.
- Do not defer the primary actor-centered path to future work while claiming workflow or component completion.
- Component evidence supports the required answer path; it does not replace required step evidence.

## Action That Can Make It Done

Action that can make it done:

- [the action, probe, experiment, change, or observation that must be attempted to satisfy the what counts as done]

Proof of impossibility, if any:

- [what would prove the action that can make it done cannot be attempted in this environment]

If it is not done, what should be reported:

- If it is not done, the report may be produced only after the action that can make it done is attempted and fails, or after impossibility is proven.
- If it is not done, the report cannot satisfy the what counts as done.

## Work Size And Evidence Check Budget

### Batch Granularity

Each batch must represent a coherent intended-result slice, not a mechanical micro-step.

| Batch | Coherent intended-result slice | Why this is one batch | Too-small split avoided |
|---|---|---|---|
| Batch 1 | [slice] | [reason] | [micro-split avoided] |

Rules:

- Do not require every micro-step to be openable.
- Intermediate states inside a batch may be broken when this policy explicitly allows it.
- Each batch must end in an openable or meaningfully verifiable state.
- If a batch cannot be verified meaningfully, merge it with the next batch or redefine the check.
- If a batch is too large to diagnose failures, split by dependency line or check line.

### Evidence check Budget

| Batch | Required strong evidence checks | Optional/weak evidence checks | Deferred evidence checks | Final-only evidence checks |
|---|---|---|---|---|
| Batch 1 | [evidence checks] | [evidence checks] | [evidence checks] | [evidence checks] |

Rules:

- Use the smallest evidence check set that can detect meaning or structural drift.
- Do not run expensive broad checks at every batch unless they are the only reliable drift evidence check.
- Treat broad verification as integration-check or completion-check work by default.
- If many evidence checks fail because they encode old meaning, preserve the intended result and record stale-evidence check retirement or rewrite.

## Batch Cadence

- Intermediate steps inside a batch may temporarily break local observability or artifact consistency when necessary.
- Each batch must end in an openable or meaningfully verifiable state.
- Batch size should avoid both micro-step local minima and huge unobservable changes.

## Destructive Intermediate-State Policy

Allowed inside a batch:

- [temporary breakage]

Not allowed even inside a batch:

- [meaning violation]
- [security/permission violation]

Batch-end requirements:

- [openable/verifiable condition]

## Output Material / Evidence Collection

Use when the goal `Final Answer Format` or design `Final Answer Format Design` requires structured output. Otherwise record `Not required; final output can be produced from ordinary progress and verification evidence`.

| Required output material | Producing batch/checkpoint | Evidence reference location | Ready before final output? | Missing material blocks completion? |
|---|---|---|---|---|
| [material] | [batch/checkpoint] | [path/section/log] | [yes/no] | [yes/no and reason] |

Final output readiness:

- [what must be ready before final report/output generation]

Blocking missing material:

- [missing material that forces stop or revision]

## User Purpose Strategy

### Internal feedback

- [supports progress/diagnosis, not purpose achievement unless justified]

### Integration feedback

- [shows cross-component or cross-artifact behavior]

### User-purpose feedback

- [smallest feedback that observes the purpose-realizing outcome]

### Operational feedback, if relevant

- [deployment/runtime/external observer evidence]

### Feedback cadence

- Per batch: [feedback used to keep execution oriented]
- Integration checks: [feedback used at integration limits]
- Final: [feedback required before claiming purpose achieved]
- Deferred feedback and reason: [feedback not available now and why]

### Evidence unavailable handling

- Verified: [what has been verified]
- Not yet observed: [purpose-relevant outcome not yet observed]
- Smallest next observation: [next feedback needed]
- Allowed completion wording: [achieved / partially observed / pending / unavailable / not required with justification]

## Evidence Lifecycle / Evidence Budget

The evidence lifecycle must keep tracked evidence reviewable and prevent repeated full raw evidence check output from outgrowing the controlled work.

| Evidence channel | Raw allowed? | Baseline policy | Per-batch retention | Delta required? | Summary required? | Max tracked size | Git policy | Raw pointer |
|---|---|---|---|---|---|---|---|---|
| [channel] | [yes/no and where raw may live] | [one full baseline / none / external] | [summary + delta / pointer only / retained full with reason] | [yes/no] | [yes/no] | [reviewable budget, cap, or project policy] | [tracked summary/delta only / ignored raw / external artifact] | [path/hash/command when raw exists] |

Rules:

- Keep at most one full baseline and one final full scan unless explicitly justified.
- Intermediate scans should store summary + delta, not repeated full raw hits.
- Full raw evidence check output belongs in local cache, ignored artifacts, compressed retained-full artifacts, or external artifact storage unless the goal explicitly requires tracked raw output.
- Tracked evidence must be reviewable without reading all raw evidence check output.
- Repeated full snapshots of the same evidence check are forbidden unless this policy explains why delta is impossible.
- Each batch must record evidence summary, delta, top offenders or representative samples, and raw pointer when raw output exists.
- Evidence artifacts must not exceed the approved evidence budget without stopping or revising the execution policy.

Evidence levels:

- Level 0 transient raw: local evidence check output, ignored by default, may be overwritten.
- Level 1 raw pointer: path, hash, command, timestamp, and retention location.
- Level 2 reviewable summary/delta: tracked summary, delta, top offenders, representative samples, and manifest.
- Level 3 retained full evidence: full baseline or final full scan only when explicitly justified.

## Evidence check / Evidence Governance

Approved evidence checks, checks, and evidence channels are evidence checks, not objectives.

Strong evidence checks to preserve:

- [check/evidence channel]

Weak or stale evidence checks to inspect before obeying:

- [check/evidence channel]

Obsolete evidence checks that may be retired and rewritten:

- [check/evidence channel]

Intended-result evidence has priority over preserving brittle old evidence checks.

## Stale Evidence check Retirement and Rewrite Policy

A check or evidence channel may be retired or rewritten when:

- it encodes old requirement meaning;
- it over-constrains execution details;
- it conflicts with rules that cannot change;
- it prevents correct structural change.

Any retired/replaced evidence check must be recorded in the progress log with reason and replacement evidence coverage.

## Phase Checks

Before execution:

- review status must be Approved.

Before moving to next batch:

- current batch-end condition met;
- required strong evidence checks for this batch have been interpreted;
- deferred and final-only evidence checks remain deferred by policy, not by omission;
- progress log updated;
- no confirmed meaning rule violated.

Before completion:

- final verification evidence recorded;
- no unresolved conflict among requirements analysis, solution design when required, goal, plan, and review.

## Execution Rhythm

- Execute according to the selected Who Does The Work / Context Use.
- For `Main-only`, keep all target work in the main agent only when the context-load rationale remains valid.
- For `Serial subagent-driven`, only one execution subagent is active at a time.
- For `Parallel subagent-driven`, dispatch only work packages in the current approved wave whose dependencies are satisfied and whose conflict locks are disjoint.
- Do not let runtime `/goal` rewrite this policy.

## Stop Conditions

Stop if:

- the plan conflicts with requirements analysis or goal;
- the plan conflicts with required solution design;
- confirmed meaning appear wrong or insufficient;
- evidence check governance is insufficient for a failing check;
- the approved execution work assignment cannot be followed;
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
- evidence check interpretation
- user purpose evidence status
- what counts as done met
- evidence needed to call it done
- required answer path step status
- required steps satisfied
- required steps failed / blocked / unobserved
- supporting-only work completed
- supporting-only work not counted as goal progress
- not done reason
- action that can make it done attempted or proof of impossibility
- smallest next action that can make it done
- Result placement status
- places acted on or inspected
- residuals and reconciliation
- allowed result claim wording
- highest purpose-relevant evidence observed
- user purpose evidence not yet observed
- smallest next observation needed
- allowed completion wording
- deferred/final-only evidence checks and reason
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

Required step(s):

- [S1 / supporting-only for S1]

Role: `mainline / supporting-only`

State transition advanced:

- [specific required step this task advances, or "none; supporting-only for Sx"]

Transition evidence produced:

- [evidence that this task produces for the required step, or supporting evidence only]

Integration check:

- [condition under which the main agent accepts this task output into progress state]

Counts as goal progress: `yes/no`

Why this is not merely component completion:

- [explain why this task advances an actor-centered transition; for supporting-only, state that it cannot satisfy goal progress]

Goal:

- [intended-result slice]

Allowed intermediate breakage:

- [breakage]

Batch-end check:

- [check]

Batch evidence checks:

- Required strong evidence checks: [evidence checks]
- Deferred/final-only evidence checks: [evidence checks]

Steps:

- [ ] [step]
