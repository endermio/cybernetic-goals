# Control Contract Rules

`goal.control.json` is not a runtime command. It is a frozen JSON statement of:

- intended result
- constraints
- evidence checks
- stop conditions
- evidence requirements

When required design is required, `goal.control.json` is downstream of `design.control.json`. It should preserve design rules that cannot change and limit decisions without redoing the design or freezing tactical details as meaning.

For complex controlled work, do not let the runtime `/goal` write its own policy. `goal.control.json` must be paired with approved `plan.control.json`, approved `review.control.json`, and compiled `runtime.control.json` before execution.

## Bad runtime goal pattern

```text
/goal First write a plan, then execute it...
```

## Good full-chain runtime goal pattern

```text
/goal Execute the runtime control JSON at docs/cybernetics/runs/YYYY-MM-DD-slug/runtime.control.json using .agents/skills/using-control-json. If the JSON is missing, invalid, inconsistent, or insufficient, stop and report the smallest required human decision.
```

`runtime.control.json` references the approved requirements, required design,
goal, execution policy, and review control JSON. The user-entered `/goal`
stays pointer-only and length-bounded.

## Good Level 2 bounded runtime goal pattern

```text
/goal Use .agents/skills/using-bounded-control-json and execute docs/cybernetics/runs/YYYY-MM-DD-slug/runtime.control.json. If the bounded JSON is missing, invalid, inconsistent, or insufficient, stop and report the smallest required human decision.
```

Bounded runtime reads only `goal.control.json` and `runtime.control.json`.
If requirements/design/plan/review become necessary, the task is no longer a
Level 2 bounded runtime and must move to the full pre-goal chain.
