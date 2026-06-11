# Target Model And Strategy Policy Redesign

Date: 2026-06-11

This note records the proposed redesign that removes `lean`, `full`, and
`control_mode` as control concepts. The replacement model starts from the
target itself, records the fixed target contract, then derives strategy and
gate behavior from that target model.

## Core Direction

The control system should not classify work by `lean` or `full`.

Those words are misleading because they imply a light-vs-complete workflow
choice. The actual distinction is whether the target requires a fixed strategy
before runtime or permits reviewed strategy changes during runtime.

The replacement terms must not become another target taxonomy. A strategy
policy is not the type of the user's goal. It is an execution rule derived from
the target contract and target model.

The system should therefore reason in this order:

1. Record the target contract: what the user wants, what counts as done, what
   evidence is enough, and what must not be accepted as a substitute.
2. Record the target model: whether the result is a state change, knowledge
   production, judgment, or a mix; whether the result and path are already known
   enough; where the result must show up; and what impact scope is involved.
3. Derive the strategy policy from the target model.
4. Derive gates from impact and authority boundaries.

Risk must not be used as the strategy selector. Risk affects `control_level` and
`gate_mode`. It does not decide whether strategy is frozen or reviewably
replannable.

The redesigned model separates:

- `control_level`: how much control and gating the work needs.
- `target_model`: what kind of target the user approved.
- `strategy_policy`: whether derived strategy is frozen or reviewably
  replannable.
- `gate_mode`: whether human approval is required for execution actions.
- `phase_structure`: whether the target is single-phase, staged, or adaptive.

## 1. Target Model Redefinition

Define `target_model` with fields such as:

- `result_orientation`
- `result_content`
- `path`
- `result_placement`
- `impact_scope`

Define an execution-ready target contract that must be fixed before runtime:

- target object
- evaluation function
- evidence strength
- unacceptable substitutes
- authority boundary

Define strategy and gate fields:

- `strategy_policy: frozen_strategy | reviewed_replanning`
- `gate_mode: none | human_gate | live_gate`
- `phase_structure: single_phase | staged | adaptive_loop`

Strategy policies mean:

- `frozen_strategy`: the approved strategy must be fixed before runtime. If the
  runtime discovers that the strategy is wrong or insufficient, it stops and
  reports the mismatch instead of modifying the strategy and continuing.
- `reviewed_replanning`: the approved target remains fixed, but runtime may
  propose changes to derived strategy. The proposal must be reviewed and
  compiled into a new generation before execution continues.

`reviewed_replanning` never means runtime may change the user's target.

Delete these concepts from official control facts:

- `lean`
- `full`
- `control_mode`

## 1.1 Amendment Boundary

The most important boundary is what reviewed replanning can and cannot change.

Reviewed replanning may change derived strategy after review:

- design strategy
- plan strategy
- runtime strategy
- required step refinement
- work packages
- instrumentation
- verifier configuration
- evidence validators

Reviewed replanning must not automatically change the target anchors:

- semantic base
- required outcomes
- what counts as done
- work covered in this run
- authority
- forbidden actions
- unacceptable substitutes

If a needed change touches any target anchor, the system must stop for human
approval. It must not continue by reclassifying the target.

## 1.2 Examples

`/api/v2` implementation:

- target result: state change
- result content: specified
- likely strategy policy: `frozen_strategy` for the approved implementation
  semantics; local implementation details may be planned, but readiness cannot
  replace implementation
- gate mode: deployment or public exposure may require a separate gate

Performance bottleneck discovery:

- target result: knowledge production from measurement
- result content: discovered during work
- likely strategy policy: `reviewed_replanning`
- gate mode: usually none for local measurement

Product lifecycle and cache retention semantics:

- target result: state change plus design model
- result content: specified by the approved product semantics
- likely strategy policy: `frozen_strategy`
- gate mode: local implementation may need none; live cleanup needs a separate
  live gate

## 2. Schema Changes

Update `schemas/control-json/run.control.schema.json`:

- remove `control_mode`
- add `control_level`
- add `target_model`
- add `strategy_policy`
- add `gate_mode`
- add `phase_structure`

Update `schemas/control-json/runtime.control.schema.json`:

- remove `control_mode`
- add the new strategy and gate fields
- require runtime fields to match `run.control.json`

Review whether these schemas need related updates:

- `schemas/control-json/requirements.control.schema.json`
- `schemas/control-json/review.control.schema.json`
- `schemas/control-json/final-report.schema.json`
- `schemas/control-json/amendment-proposal.schema.json`
- `schemas/control-json/amendment.patch.schema.json`
- `schemas/control-json/progress-event.schema.json`

## 3. Compiler, Guard, And Runtime Changes

Update `.agents/skills/compiling-cybernetic-runtime-goals/scripts/compile_runtime_goal.py`:

- stop writing `control_mode`
- copy `control_level`, `target_model`, `strategy_policy`, `gate_mode`, and
  `phase_structure` from `run.control.json` into the compiled runtime control
  object

Update `.agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py`:

- remove `runtime.control.json control_mode must match run.control.json`
- validate that the new fields match across run/runtime controls
- allow amendment continuation only when `strategy_policy` is
  `reviewed_replanning`
- reject amendment continuation for `strategy_policy: frozen_strategy`

Update `.agents/skills/using-control-json/scripts/control_json_runtime.py`:

- read and validate the new fields
- remove `lean` / `full` assumptions
- require frozen strategy runs to stop and report when the strategy is wrong
- allow amendment loops only for reviewed-replanning runs

Update `.agents/skills/using-control-json/scripts/verify_runtime_progress.py`:

- judge unresolved amendments according to `strategy_policy`
- reject amendment continuation for frozen strategy runs
- permit reviewed amendments only when the current generation is properly
  reviewed and activated

## 4. Orchestrator Changes

Update `.agents/skills/orchestrating-cybernetic-pregoal/SKILL.md`:

- remove `lean` / `full` as primary decisions
- derive run behavior from `target_model` and `strategy_policy`
- use `frozen_strategy` when the approved target and path are known enough and
  runtime should not replan
- use `reviewed_replanning` when the answer or path must be discovered during
  execution
- require staged handling for mixed targets

Update `.agents/skills/orchestrating-cybernetic-pregoal/scripts/amendment_orchestrator.py`:

- create new generations only for `strategy_policy: reviewed_replanning`
- for `strategy_policy: frozen_strategy`, treat amendment requests as
  blocked or human-decision events, not as automatic continuation
- require `control.amendment.proposed.patch_ref`
- apply only a validated amendment patch, not a copied old strategy
- require an approved amendment review before switching
  `run.control.json.current_generation`
- never synthesize or auto-approve the amendment review inside the orchestrator

## 5. Routing, Requirements, And Review Skills

Update `.agents/skills/routing-cybernetic-workflows/SKILL.md`:

- output `Control level`
- output `Target model`
- output `Strategy policy`
- output `Gate mode`
- output `Phase structure`
- remove `Level 3 defaults to lean`
- remove `full pre-goal` as a routing concept
- make risk affect `control_level` and `gate_mode`, not strategy policy
- make unknown result or unknown path affect `strategy_policy`

Update `.agents/skills/analyzing-cybernetic-requirements/SKILL.md`:

- add target model fields to the compact control commitment
- record the execution-ready target contract
- require mixed targets to be split into phases
- avoid wording such as `Level 3/4 or full pre-goal work`

Update `.agents/skills/reviewing-cybernetic-control-structures/SKILL.md`:

- add target model preservation review
- check that strategy policy follows from the target model
- check that risk is not used as the strategy selector
- check that frozen strategy runs do not allow runtime replanning
- check that reviewed replanning does not mutate the target contract

Update `.agents/skills/writing-cybernetic-goals/SKILL.md`:

- remove `lean` / `full` wording
- keep Level 2 bounded goals distinct from Level 3/4 controlled runs

Update `.agents/skills/writing-cybernetic-execution-policies/SKILL.md`:

- replace `lean` / `full` wording with `strategy_policy`

Update `.agents/skills/using-control-json/SKILL.md` and
`.agents/skills/using-control-json/references/runtime-control-json-protocol.md`:

- replace `lean mode` with reviewed-replanning strategy behavior
- replace `full mode` with frozen strategy behavior
- state that frozen strategy runs stop on strategy mismatch instead of
  amending and continuing

## 6. Documentation Changes

Replace or heavily revise
`docs/cybernetic-framework/reviewed-replanning-control-architecture.md`.

The new architecture should be framed around:

- target contract
- target model
- control level
- strategy policy
- gate mode
- phase structure

Update related documentation such as:

- `docs/cybernetic-framework/invariant-artifact-consumer-matrix.md`
- any docs that use `lean pre-goal`, `full pre-goal`, `full-chain`, or
  `control_mode` as strategy concepts

Add a migration note:

- old runs using `control_mode` are invalid under the new model
- new runs must use the new target and strategy fields
- no `lean` / `full` compatibility alias is provided

## 7. Tests And Evals

Update schema tests:

- `tests/skills/test_control_json_schemas.py`

Update generation/runtime tests:

- `tests/skills/test_reviewed_replanning_control.py`
- `tests/skills/test_runtime_json_progress_verifier.py`
- `tests/skills/test_json_official_guard_compiler_path.py`

Update evals:

- routing evals
- requirements evals
- orchestrating evals
- review evals
- writing-goal evals
- writing-policy evals

Add regressions:

- official schemas reject `control_mode`
- official control docs and fixtures do not use `lean` or `full` as strategy
  concepts
- Level 3 specified target routes to `frozen_strategy`
- Level 3 exploratory target routes to `reviewed_replanning`
- risk changes `control_level` or `gate_mode`, not `strategy_policy`
- `frozen_strategy` rejects amendment continuation
- `reviewed_replanning` allows reviewed patch-based amendment continuation
- amendment proposal without `patch_ref` fails
- amendment patch without approved review does not switch generation
- hybrid targets must split into phases

## 8. Fixtures And Examples

Update all run fixtures:

- `run.control.json`
- `runtime.control.json`
- generation examples

Update historical accident fixtures:

- `/api/v2` readiness cannot replace implementation
- checkpoint-only path cannot replace full-workflow ceiling
- measurement-curve requests cannot be downgraded to framework-only work

Mark old fixtures that still use `control_mode`, `lean`, or `full` as invalid,
or migrate them fully to the new model.

## 9. Verification

Run:

```bash
python3 -m unittest discover -v
```

Also verify:

- schema tests
- guard tests
- compiler tests
- runtime validator tests
- verifier tests
- routing / requirements / orchestration evals

Exercise at least three clean sample runs:

- `frozen_strategy`
- `reviewed_replanning`
- `live_gate`

## 10. Commit Strategy

Prefer separate commits for:

- schema and runtime core
- skills and docs
- tests and fixtures

Push after the full verification suite passes.
