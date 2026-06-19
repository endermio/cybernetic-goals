# Runtime Compilation Detailed Rules

Use this file only when the active generation or selected gates reference
expanded artifacts such as design, goal, plan, or review files.

## Official Entry

Official compiler input is always the JSON run directory. A valid official run
contains `requirements.control.json`, `run.control.json`, and a declared current
generation. Root-level `design.control.json`, `goal.control.json`,
`plan.control.json`, and `review.control.json` may exist as supporting approved
artifacts, but they are not a substitute for `run.control.json`.

## Conditional Expanded Checks

When expanded artifacts are selected by the run:

- approved requirements must preserve the user-approved target anchors;
- design, if present, must preserve required answer paths and hard model rules;
- goal, if present, must preserve required outcomes and completion conditions;
- plan, if present, must map blocking required steps to producing actions and
  evidence;
- review, if present, must approve source requirement preservation,
  required-outcome coverage, counterexample gate, and final observer checks.

If an expanded artifact is missing or stale but the current generation requires
it, stop and return to pre-goal orchestration. Do not compensate by inlining the
missing content into `/goal`.

## Runtime JSON Contents

Compiled `runtime.control.json` should index:

- `semantic_base_ref`;
- `strategy_policy`;
- `generation.id`;
- readonly approved control files;
- writable runtime control outputs;
- writable evidence paths, if any;
- required steps for the current generation;
- verifier command and required outcomes;
- imported or invalidated evidence for generation-aware execution.

The compiler, not the human-facing skill text, owns the exact JSON shape.

## Guard Bypass

Do not use `--skip-guard` for official runtime compilation. It is only for
internal validation and requires the explicit bypass acknowledgement.
