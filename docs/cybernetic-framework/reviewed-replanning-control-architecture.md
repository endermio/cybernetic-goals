# Reviewed Replanning Control Architecture

This document defines the current JSON control-run model.

The system no longer names control runs by how large the startup flow is. The
control question is whether the approved target can be executed with a fixed
strategy, or whether the execution strategy may change after runtime
observations.

## Core Model

Every official Level 3/4 JSON control run starts from:

```text
requirements.control.json
run.control.json
gen-000/runtime.control.json
```

`requirements.control.json` is the approved target anchor. Runtime must not
change it.

`run.control.json` records the control policy for the run:

- `control_level`
- `target_model`
- `strategy_policy`
- `gate_mode`
- `phase_structure`
- `current_generation`
- `max_auto_amendment_rounds`
- `amendment_policy`
- generation history

`gen-N/runtime.control.json` is the current executable strategy.

## Target Anchor

These fields are not runtime-adjustable:

- semantic base
- required outcomes
- what counts as done
- work covered in this run
- authority
- forbidden actions
- unacceptable substitutes
- final answer requirements

If execution discovers that any of these must change, runtime must stop and ask
for human approval. It must not rewrite the approved target or continue by
renaming the work.

## Strategy Policy

`strategy_policy` has two values.

`frozen_strategy` means the approved execution strategy must not change during
runtime. If the strategy proves insufficient, runtime reports the mismatch and
stops. It does not create a new generation.

`reviewed_replanning` means runtime may propose a strategy change when
observations show that the current strategy cannot produce the approved result.
The proposal is not self-approving. The orchestrator must review it, preserve the
approved target anchors, generate a new generation, and re-run guard/compiler
checks before execution continues.

Risk does not choose `strategy_policy`. Risk is recorded separately in
`gate_mode`.

## Gate Mode

`gate_mode` records whether human approval is required before certain actions:

- `none`: no special external approval gate.
- `human_gate`: human approval is required for named action classes.
- `live_gate`: live, external, destructive, or irreversible action requires
  explicit approval before execution.

Gate mode can make a step wait for approval, but it does not by itself decide
whether the strategy is frozen or reviewably replannable.

## Target Model

`target_model` records what kind of result is being produced:

- `result_orientation`: state change, knowledge production, judgment, or design
  model.
- `result_content`: specified, partially specified, or discovered during work.
- `path`: known enough, partially known, or discovered during work.
- `result_placement`: single place, multiple places, or not applicable.
- `impact_scope`: local reversible, persistent internal, or live external /
  irreversible.

The target model informs the strategy policy and gates, but does not replace
the approved target anchors.

## Generation Rules

Each generation has one active runtime strategy. Only the generation named by
`run.control.json.current_generation` is current.

Progress events must include `runtime_generation`.

Older generation evidence does not satisfy current generation steps unless the
current runtime explicitly imports it. Current runtime may also invalidate older
evidence.

`strategy_kind` values:

- `discovery`: can collect observations and propose strategy refinement, but
  cannot permit final `goal_achieved: true`.
- `execution`: can complete the approved target if all verifier conditions pass.
- `amendment`: a reviewed successor generation created from an approved
  amendment proposal.

## Amendment Rules

Runtime may append `control.amendment.proposed` only when it observes that the
current strategy cannot produce approved target evidence.

The proposal must state:

- current generation
- amendment id
- triggering observation
- affected stages
- affected source requirements
- whether semantic base would change
- whether required outcomes would change
- whether authority would expand

If semantic base, required outcomes, what counts as done, work covered,
authority, forbidden actions, or unacceptable substitutes would change, the
orchestrator must stop for human approval.

If the proposal preserves anchors and `strategy_policy` is
`reviewed_replanning`, the orchestrator may create a reviewed successor
generation.

If `strategy_policy` is `frozen_strategy`, the orchestrator must not create a
successor generation from runtime observation. It reports that the fixed
strategy no longer fits.

## Verifier Rules

The verifier permits `goal_achieved: true` only when:

- current generation required steps are complete;
- blocking required outcomes are covered;
- source requirements are covered at required evidence strength;
- final report refers to the current generation;
- unresolved amendments do not remain;
- no anchor-changing amendment is being treated as automatic progress;
- discovery-only or synthetic-only generation is not being used as final
  completion.

The verifier is a final claim gate. It cannot compensate for a wrong target
model or wrong strategy policy; those must be corrected by review or human
approval before runtime proceeds.

## Operational Contract

Official control input is JSON only. Markdown may provide background context but
is not part of the official control chain.

All official runs must have `run.control.json`. Root-level historical chains
without `run.control.json` are invalid and must be regenerated or migrated.

Do not select strategy from Level alone. Do not select strategy from risk alone.
Use Level for control complexity, `strategy_policy` for whether strategy may
change, and `gate_mode` for human approval requirements.
