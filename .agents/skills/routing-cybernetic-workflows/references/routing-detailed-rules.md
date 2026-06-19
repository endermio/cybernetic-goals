# Routing Detailed Rules

## Purpose

This skill chooses a control entry for a formed task. It does not classify by
levels.

Valid entries:

- `ordinary_direct_work`: normal Codex work, no cybernetic run.
- `bounded_runtime`: fixed small task using `goal.control.json`,
  `runtime.control.json`, and `using-bounded-control-json`.
- `controlled_run`: official JSON run using requirements, `run.control.json`,
  current generation runtime, review, and Counterexample Gate.

## Main Question

Ask:

```text
Would runtime otherwise have to invent or revise user meaning, solution model,
work strategy, evidence checks, phase checks, blocked claims, or completion
claims?
```

If yes, use `controlled_run`. If no, prefer `ordinary_direct_work` or
`bounded_runtime`.

## Checks Are Not Entries

Rubric, output contract, design, data-plane, deployment, human approval, and
live approval are checks or gates. They do not create a different entry type.

Use:

- `human_gate` for explicit human approval.
- `live_gate` for live, destructive, irreversible, credentialed, regulated, or
  customer-data actions.
- `counterexample_gate` for every `controlled_run`.

Risk adds gates. Risk does not choose `strategy_policy`.

## Strategy Policy

For `controlled_run`, record:

- `frozen_strategy`: target and strategy must not change during runtime.
- `reviewed_replanning`: target is fixed, but derived strategy may change after
  observation, patch, review, and generation switch.

## Evaluation Rubric Check

If the task asks whether something is complete, closed, usable, ready, safe,
stable, correct, covered, passed, or high quality, require an explicit rubric.

A rubric must define status meanings, evidence strength, minimum evidence for
the strongest positive status, downgrade behavior, and external dependency
handling. Object lists are not rubrics.

## Output Contract Check

If final output affects acceptance, handoff, persistence, machine consumption,
or downstream action, require explicit audience, medium, structure, detail
level, destination, and acceptance condition.

## Design Check

If the target meaning is known but objects, relationships, flow, limits,
interfaces, lifecycle, failure behavior, or evidence model are unclear, require
design before execution.

## Response Contract

Every response includes:

1. `Control entry decision`
2. `Why`
3. `strategy_policy`, only for `controlled_run`
4. `gates`
5. `required_checks`
6. `recommended next step`
7. `rejected path`, if useful

Do not create files, write control JSON, or execute target work.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Using level names | Use `ordinary_direct_work`, `bounded_runtime`, or `controlled_run` |
| Treating risk as strategy | Add `human_gate` or `live_gate`; keep strategy separate |
| Treating validators as quality approval | Validators are structural gates only |
| Skipping Counterexample Gate on controlled runs | Add `counterexample_gate` |
| Routing pre-task process distrust as a task | Use `$framing-cybernetic-intent` first |
