# Routing Response Shapes

Templates only. Do not use level names.

## ordinary_direct_work

```markdown
Control entry decision: ordinary_direct_work

Why:
- ...

gates:
- none, or named local/manual checks

required_checks:
- ...

recommended next step:
- Directly perform the task and verify locally.

rejected path:
- controlled_run would add process without preserving more meaning.
```

## bounded_runtime

```markdown
Control entry decision: bounded_runtime

Why:
- Fixed small task.
- Meaning and rubric are explicit.
- No new solution/control decision is needed during runtime.

gates:
- structural verifier for bounded runtime

required_checks:
- rubric/design/output checks only if not already explicit

recommended next step:
- `$writing-cybernetic-goals` creates `goal.control.json` and
  `runtime.control.json`, then outputs a short `/goal` using
  `using-bounded-control-json`.

rejected path:
- controlled_run is unnecessary because no approved work chain must be revised.
```

## controlled_run

```markdown
Control entry decision: controlled_run

Why:
- Runtime would otherwise invent or revise user meaning, strategy, evidence
  checks, blocked claims, or completion claims.

strategy_policy:
- frozen_strategy / reviewed_replanning

gates:
- counterexample_gate
- human_gate, if required
- live_gate, if required

required_checks:
- requirements approval
- design/rubric/output/data-plane/deployment checks as needed

recommended next step:
- `$analyzing-cybernetic-requirements ...`
- After approval: `$orchestrating-cybernetic-pregoal ...`

rejected path:
- ordinary_direct_work or bounded_runtime would leave runtime to invent control
  decisions.
```
