# Lean Pre-goal And Reviewed Replanning Control Architecture

This note records the full change set for moving the cybernetic runtime model
from heavy frozen pre-goal compilation to lean pre-goal startup plus reviewed
replanning control.

The target architecture is:

```text
approved target anchors
-> lean initial control generation
-> runtime observation
-> reviewed amendment
-> next control generation
-> continued execution
```

The goal is not to let runtime mutate approved semantics. The goal is also not
to keep producing full design/goal/plan/review chains before observation exists.
The goal is to keep target anchors hard while making strategy lightweight,
versioned, and reviewable.

Default mode is lean pre-goal. Full pre-goal is an exception for work where a
full strategy must be frozen before runtime.

## Lean Pre-goal Default

Lean pre-goal creates only the control needed to start safe execution:

```text
requirements.control.json
run.control.json
gen-000/runtime.control.json
```

Lean pre-goal must define:

- approved target anchors;
- current generation;
- first execution horizon;
- allowed and forbidden actions;
- amendment policy;
- progress and verifier protocol.

Lean pre-goal must not generate complete design, goal, plan, and review files by
default. Those files are optional strategy artifacts, created only when the work
requires them or when an amendment review needs them.

Use full pre-goal only when at least one condition holds:

- irreversible or live external-state action;
- production, compliance, safety, security, financial, legal, or regulated risk;
- authorization, visibility, or external contract semantics must be frozen
  before runtime;
- large multi-agent or multi-team coordination requires a frozen dependency
  graph before target execution;
- runtime cannot safely replan;
- the user explicitly requires full design/plan review before execution.

## Control Boundary

Hard anchors:

- `requirements.control.json`
- `semantic_base`
- `required_outcomes`
- `what_counts_as_done`
- approved work coverage
- approved authority and forbidden actions

Reviewed strategy:

- `design.control.json`
- executable parts of `goal.control.json`
- `plan.control.json`
- `runtime.control.json`
- verifier configuration
- required-step refinements
- work packages
- instrumentation
- evidence validators

Runtime must not edit approved JSON in place. Runtime may propose an amendment.
An amendment that changes the hard anchors requires human reapproval.

Lean pre-goal may omit `design.control.json`, `goal.control.json`,
`plan.control.json`, and `review.control.json` in the initial generation. Full
pre-goal may still require those artifacts before runtime.

## 1. Control Fact Directory Structure

Use generation-aware run directories. Lean mode keeps strategy files minimal:

```text
docs/cybernetics/runs/<slug>/
  requirements.control.json
  run.control.json
  progress.jsonl
  runtime-status.json
  final-report.json
  evidence/

  gen-000/
    runtime.control.json

  gen-001/
    review.control.json
    runtime.control.json
```

Full mode may include these additional per-generation artifacts:

```text
gen-N/
  design.control.json
  goal.control.json
  plan.control.json
  review.control.json
  runtime.control.json
```

Rules:

- `requirements.control.json` is the root target anchor.
- A generation may copy `requirements.control.json` only as a read-only
  convenience; the root semantic hash remains authoritative.
- Approved control JSON is never edited in place.
- Each generation has its own runtime contract. Amendment generations have their
  own review and hashes.
- Root `progress.jsonl` records observations across generations.
- Final success is judged only against the current approved generation.

## 2. Run Manifest

Add a root manifest:

```text
run.control.json
```

Example:

```json
{
  "artifact_type": "run.control",
  "schema_version": "1",
  "run_id": "2026-xx-slug",
  "control_mode": "lean",
  "current_generation": "gen-001",
  "max_auto_amendment_rounds": 2,
  "semantic_base_ref": {
    "id": "semantic-base:...",
    "hash": "sha256:..."
  },
  "amendment_policy": {
    "may_change": [
      "design_strategy",
      "plan_strategy",
      "runtime_strategy",
      "required_step_refinement",
      "work_packages",
      "instrumentation",
      "verifier_config"
    ],
    "must_not_change_without_human": [
      "semantic_base",
      "required_outcomes",
      "what_counts_as_done",
      "work_covered",
      "authority",
      "forbidden_actions"
    ]
  },
  "generations": [
    {
      "id": "gen-000",
      "strategy_kind": "discovery",
      "status": "superseded",
      "runtime": "gen-000/runtime.control.json",
      "reason": "plan strategy did not produce required evidence"
    },
    {
      "id": "gen-001",
      "strategy_kind": "amendment",
      "status": "active",
      "parent": "gen-000",
      "runtime": "gen-001/runtime.control.json",
      "review": "gen-001/review.control.json",
      "amendment_source": "progress.jsonl#A1"
    }
  ]
}
```

The manifest is the authoritative index for the active control generation.
Each generation declares a strategy kind:

- `discovery`: first-horizon exploration. It may use synthetic steps derived
  from required outcomes, but it cannot be used for final success.
- `execution`: reviewed executable strategy. It can be the current completion
  generation only when it has an approved review and non-synthetic required
  steps.
- `amendment`: reviewed replacement strategy created from an amendment. It must
  name a parent generation, an amendment source, an approved review, and
  non-synthetic required steps.

`max_auto_amendment_rounds` is mandatory and is enforced against the generation
history. Exceeding it stops automatic replanning and requires a human decision.

## 3. Progress Events

Extend `progress-event.schema.json` to support:

- `runtime.generation.started`
- `runtime.generation.superseded`
- `control.amendment.proposed`
- `control.amendment.approved`
- `control.amendment.rejected`
- `control.amendment.blocked`
- `step.completed`
- `step.failed`
- `step.blocked`
- `observation.recorded`

Every event must include:

```json
{
  "runtime_generation": "gen-000"
}
```

`control.amendment.proposed` must include:

```json
{
  "amendment_id": "A1",
  "runtime_generation": "gen-000",
  "reason": "...",
  "triggering_observation": "...",
  "affected_stages": ["design", "plan", "runtime"],
  "semantic_base_change": false,
  "required_outcomes_changed": false,
  "authority_expanded": false,
  "proposed_changes": [],
  "review_required": [
    "intent-preservation",
    "obligation-preservation",
    "required-outcome-coverage",
    "horizon-authority"
  ]
}
```

If `semantic_base_change`, `required_outcomes_changed`, or
`authority_expanded` is true, the event records a need for human decision. It
cannot be auto-approved into the next generation.

## 4. Schema Changes

Add or modify:

```text
schemas/run.control.schema.json
schemas/amendment-proposal.schema.json
schemas/progress-event.schema.json
schemas/runtime.control.schema.json
schemas/review.control.schema.json
schemas/final-report.schema.json
```

`run.control.json` must support:

- `control_mode: lean | full`;
- `current_generation`;
- `max_auto_amendment_rounds`;
- amendment policy with may-change and must-not-change sets;
- generation history and statuses.

`runtime.control.json` must include generation metadata:

```json
{
  "generation": {
    "id": "gen-001",
    "parent": "gen-000",
    "amendment_source": "progress.jsonl#..."
  }
}
```

`review.control.json` must record amendment review scope:

```json
{
  "review_scope": "initial_generation | amendment",
  "amendment_source": "...",
  "unchanged_anchor_checks": {
    "semantic_base_unchanged": true,
    "required_outcomes_unchanged": true,
    "authority_not_expanded": true
  }
}
```

`final-report.json` must include:

```json
{
  "runtime_generation": "gen-001",
  "superseded_generations": ["gen-000"]
}
```

## 5. `using-control-json` Runtime Skill

Rewrite runtime behavior from:

```text
approved JSON read-only; execute plan; write progress/status/final-report
```

to:

```text
approved generation JSON read-only;
execute current generation;
if observed strategy cannot produce required outcome, do not fill the slot and
do not claim blocked immediately;
write control.amendment.proposed unless user approval is required;
continue only after a reviewed new generation exists.
```

Runtime has three valid outcomes at any decision point:

- continue current generation;
- request reviewed modification;
- stop for human decision.

Stop for human decision when:

- `semantic_base` would change;
- `required_outcomes` would change;
- `what_counts_as_done` would change;
- approved authority or work coverage would expand;
- an external resource is needed;
- the review loop cannot converge.

## 6. `orchestrating-cybernetic-pregoal`

Extend the orchestrator from full pre-goal compilation to three modes:

- lean initial pre-goal compilation;
- full initial pre-goal compilation;
- runtime amendment orchestration.

Lean initial compilation:

1. Check approved requirements.
2. Create `run.control.json`.
3. Create `gen-000/runtime.control.json` with first horizon and amendment
   policy.
4. Run the lean pre-goal guard.
5. Output the pointer-only `/goal`.

Lean initial compilation must not require full `design.control.json`,
`goal.control.json`, `plan.control.json`, or `review.control.json` unless the
requirements, routing, risk, or user explicitly select full mode.

Amendment orchestration:

1. Read `control.amendment.proposed`.
2. Check that semantic base, required outcomes, and authority remain unchanged.
3. Generate `gen-N+1` control JSON.
4. Run review.
5. Run guard.
6. Compile `runtime.control.json` for `gen-N+1`.
7. Update `run.control.json.current_generation`.
8. Append `control.amendment.approved` or `control.amendment.rejected`.

If the proposal changes approved user semantics or exceeds lean-mode authority,
stop for human approval.

## 7. `writing-cybernetic-execution-policies`

For lean mode, do not generate a full execution policy by default. The initial
runtime strategy carries only the first horizon, assumptions, observation
triggers, amendment triggers, and anchor-change stop conditions.

When a plan is created, it must stop being a single frozen trajectory. Add:

```json
{
  "strategy_assumptions": [],
  "observation_triggers": [],
  "amendment_triggers": []
}
```

Every work package must declare:

- which observation would invalidate this plan;
- which amendment should be requested if invalidated.

Example trigger:

```text
If the planned producing action can only map to a local or partial path,
request amendment before implementation proceeds.
```

## 8. `reviewing-cybernetic-control-structures`

Review must support lean initial review and amendment review, not only full
initial review.

Add required checks:

- `lean-startup-sufficiency`
- `anchor-preservation`
- `strategy-change-necessity`
- `old-plan-failure-observed`
- `new-plan-can-produce-required-outcomes`
- `evidence-validity-import`
- `generation-supersession`

Review must answer:

- Is full pre-goal actually necessary, or is lean startup sufficient?
- Is this amendment necessary?
- Is it only changing strategy?
- Does it silently change the user-approved target?
- Does it expand authority?
- Which old-generation evidence is still valid?
- Which old-generation evidence is invalidated?

## 9. `compiling-cybernetic-runtime-goals`

Make runtime compilation generation-aware:

```bash
compile_runtime_goal.py --run-dir docs/cybernetics/runs/<slug> --generation gen-001
```

The compiler may output a short `/goal` pointer to either:

- `run.control.json` and its `current_generation`; or
- `gen-001/runtime.control.json`.

The compiler must not assume that a run root contains exactly one control
chain.

In lean mode, the compiler must not require `design.control.json`,
`goal.control.json`, `plan.control.json`, or `review.control.json` before
emitting the initial pointer, unless the selected mode is full.

## 10. Guards

`control_chain_guard.py` must support:

```text
--run-dir <run-root>
--generation gen-001
```

Guard checks:

- generation directory is complete;
- `run.control.json.current_generation` exists;
- `control_mode` is valid and full-only artifacts are required only in full
  mode;
- current generation is fully approved/compiled;
- execution and amendment generations declare an approved review;
- discovery generations cannot be treated as final completion generations;
- synthetic required steps are allowed only in discovery generations;
- semantic base matches the root manifest;
- parent generation, when present, has an amendment source;
- amendment does not change anchors unless human reapproval exists;
- automatic amendment rounds do not exceed `max_auto_amendment_rounds`;
- review hashes match generation files;
- superseded generations cannot be used as the current final verifier target.

## 11. Verifier

`verify_runtime_progress.py` must be generation-aware:

```bash
verify_runtime_progress.py <run-root> --generation gen-001
```

Rules:

- only current-generation required steps and outcomes decide completion;
- old-generation progress is diagnosis only;
- old evidence counts only when the current generation explicitly imports it;
- final report must declare the current generation;
- unresolved amendment proposals prevent `goal_achieved: true`.
- anchor-changing amendment proposals prevent `goal_achieved: true` and require
  a human decision.
- discovery generations and synthetic required steps prevent `goal_achieved:
  true`.

## 12. Evidence Model

Add explicit evidence import and invalidation:

```json
{
  "imported_evidence": [
    {
      "from_generation": "gen-000",
      "path": "evidence/...",
      "valid_for_steps": ["S1"],
      "reason": "scope boundary unchanged"
    }
  ],
  "invalidated_evidence": [
    {
      "from_generation": "gen-000",
      "path": "evidence/...",
      "reason": "old candidate construction rule invalid"
    }
  ]
}
```

New generations must not silently reuse old evidence.

## 13. Runtime Status

`runtime-status.json` must support:

- `running`
- `amendment_requested`
- `waiting_for_review`
- `generation_superseded`
- `blocked`
- `complete`

It must not collapse strategy repair into only `blocked` or `complete`.

## 14. Tests And Regressions

Add regressions for:

- lean pre-goal can start with requirements, run manifest, and gen-000 runtime
  only;
- full pre-goal remains required for high-risk or explicitly full workflows;
- goal execution discovers plan mismatch and writes an amendment proposal rather
  than hard-completing;
- amendment with unchanged semantic base can create `gen-001`;
- amendment that changes `required_outcomes` requires human approval;
- `gen-000` completed steps do not automatically satisfy `gen-001`;
- unresolved amendment proposal prevents final success;
- `/api/v2 readiness` cannot replace `/api/v2 implementation`; it must trigger
  amendment;
- checkpoint-only path cannot be wrapped as full workflow ceiling path; it must
  trigger amendment or fail;
- review approves amendment only if anchors are unchanged and the new strategy
  can produce required outcomes;
- guard rejects a root run whose `current_generation` points to a stale or
  unreviewed generation.
- guard rejects a run whose automatic amendment history exceeds
  `max_auto_amendment_rounds`;
- verifier rejects a discovery generation or synthetic required step as final
  completion;
- verifier rejects an anchor-changing amendment as automatic completion.

## 15. Delete The Old Assumption

Remove the hidden assumption:

```text
runtime.control.json is the one-time final control contract
```

Replace it with:

```text
runtime.control.json is the current strategy contract for one generation
```

Also remove the hidden assumption:

```text
full design/goal/plan/review pre-goal is the default startup path
```

Replace it with:

```text
lean pre-goal is the default; full pre-goal is selected only when risk or
coordination requires it
```

Affected skills and scripts:

- `using-control-json`
- `orchestrating-cybernetic-pregoal`
- `compiling-cybernetic-runtime-goals`
- `control_chain_guard`
- `verify_runtime_progress`
- `reviewing-cybernetic-control-structures`
- `writing-cybernetic-execution-policies`

## Target Behavior

After implementation, the runtime flow is:

```text
lean pre-goal generates requirements, run.control, and gen-000 runtime
goal executes gen-000
runtime observes strategy failure
runtime writes amendment proposal
review approves or rejects the amendment
orchestrator generates gen-001
goal continues with gen-001
final verifier judges only the current approved generation
```

This is closed-loop control over reviewed strategy updates. It is neither frozen
plan execution nor free runtime mutation of the approved target.
