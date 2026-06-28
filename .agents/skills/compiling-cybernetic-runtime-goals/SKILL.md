---
name: compiling-cybernetic-runtime-goals
description: 'Use when a JSON run directory must be validated and compiled into runtime.control.json plus a short /goal pointer before execution.'
---

# Compiling Cybernetic Runtime Goals

## Overview

Compile the current approved generation of a JSON control run.

Default official input:

```text
docs/cybernetics/runs/<slug>/
  requirements.control.json
  run.control.json
  gen-N/runtime.control.json
```

`run.control.json.current_generation` selects the generation. The run records
`strategy_policy`; do not use old process-weight labels as compiler concepts.

This skill does not execute target work and does not edit approved meaning.
Detailed conditional checks live in `references/runtime-compilation-detailed-rules.md`.

## Hot Path

1. Confirm the run directory contains `requirements.control.json` and
   `run.control.json`.
2. Confirm `run.control.json.current_generation` names exactly one active
   generation.
3. Confirm that generation declares `runtime`.
4. For `execution` or `amendment` generations, confirm an approved generation
   review exists before compiling.
5. Run the guard and compiler.
6. Output only the short `/goal` pointer when guard and compile pass.

Preferred command:

```bash
python3 .agents/skills/compiling-cybernetic-runtime-goals/scripts/compile_runtime_goal.py \
  --run-dir docs/cybernetics/runs/YYYY-MM-DD-feature
```

The compiler already enforces `run.control.json`, `current_generation`,
generation review rules, hashes, and runtime JSON shape. Do not hand-build a
runtime prompt from Markdown or old root-chain assumptions.

## Pointer Rule

The user-entered `/goal` is an adapter, not a control fact:

```text
/goal Use .agents/skills/using-control-json and execute docs/cybernetics/runs/YYYY-MM-DD-feature/gen-000/runtime.control.json. If the JSON is missing, invalid, inconsistent, or insufficient, stop and report the smallest required human decision.
```

Do not inline approved requirements, completion rules, work assignment,
evidence rules, review discipline, or subagent protocol prose into `/goal`.

## Blocked Compile

If guard or compiler fails, do not emit `/goal`.

Report:

```markdown
Runtime goal compilation blocked.

Reason:
- ...

Guard/compiler result:
- `FAIL`
- transition-gate `next_action` if emitted

Response-only next step:
- return to `$orchestrating-cybernetic-pregoal` with the failing output, or
- run the smallest named upstream repair step.
```

## Validation Checklist

- [ ] `run.control.json` is present.
- [ ] `current_generation` is declared and active.
- [ ] The generation runtime path exists or was compiled.
- [ ] Required generation review exists for `execution` and `amendment`.
- [ ] Guard/compiler passed.
- [ ] No approved control JSON was rewritten by hand.
- [ ] The final `/goal` is pointer-only.
- [ ] The skill did not execute target work.
