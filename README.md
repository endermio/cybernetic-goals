# Cybernetic Skills Pack

This package contains a pre-goal control pipeline for Codex-style agent work.

The core idea is:

```text
skills = compile-time control tools
/goal = runtime executor
Superpowers = planning/review/execution substrate
```

Human input does not always arrive as a formed task. For pre-task intent such
as confusion, dissatisfaction, risk sense, failed experience, method preference,
or distrust of the current process, start from the human situation:

```text
human situation
  -> $framing-cybernetic-intent
  -> shared intent understanding
  -> optional task formation
  -> $routing-cybernetic-workflows
```

Only route formed tasks. Do not treat a requested method or workflow as the
human purpose.

For complex work, do not let `/goal` analyze requirements, invent the solution design, write its own plan, review its own plan, or invent a new control strategy during execution. Instead, prepare and approve JSON control files first, then emit a short `/goal` pointer to the approved runtime control JSON.

Official persistent control facts live only in:

```text
docs/cybernetics/runs/<slug>/*.control.json
docs/cybernetics/runs/<slug>/progress.jsonl
docs/cybernetics/runs/<slug>/runtime-status.json
docs/cybernetics/runs/<slug>/final-report.json
docs/cybernetics/runs/<slug>/evidence/
```

Historical Markdown artifacts are non-authoritative background only. Do not use Markdown as official guard, compiler, runtime, or long-term dual-path control input.

Superpowers dependencies are stage-specific infrastructure, not optional style suggestions. See `docs/cybernetic-framework/superpowers-infrastructure-policy.md`.

## Install

From this package root, copy the skill directories into either your user-level skill directory:

```bash
mkdir -p ~/.agents/skills
cp -R .agents/skills/* ~/.agents/skills/
```

or into a repository-local skill directory:

```bash
mkdir -p /path/to/target-repo/.agents/skills
cp -R .agents/skills/* /path/to/target-repo/.agents/skills/
```

## Recommended workflow

For complex work:

```text
human situation
  -> for pre-task intent before formed task routing

$framing-cybernetic-intent
  -> shared intent understanding
  -> optional task formation

$routing-cybernetic-workflows
  -> decide whether a formed task should use the cybernetic workflow

$analyzing-cybernetic-requirements
  -> docs/cybernetics/runs/YYYY-MM-DD-feature/requirements.control.json

$orchestrating-cybernetic-pregoal
  -> run pre-goal compilation after requirements analysis, invoking solution design when Design Gate is required
```

Controlled-run orchestration includes the solution-design stage when Design Gate is required, but solution design remains owned by `$designing-cybernetic-solutions`.

The orchestrator drives the following skills and stops if the review cannot converge:

```text
$designing-cybernetic-solutions
  -> docs/cybernetics/runs/YYYY-MM-DD-feature/design.control.json when Design Gate is required

$writing-cybernetic-goals
  -> docs/cybernetics/runs/YYYY-MM-DD-feature/goal.control.json

$writing-cybernetic-execution-policies
  -> docs/cybernetics/runs/YYYY-MM-DD-feature/plan.control.json

$reviewing-cybernetic-control-structures
  -> docs/cybernetics/runs/YYYY-MM-DD-feature/review.control.json

$compiling-cybernetic-runtime-goals
  -> docs/cybernetics/runs/YYYY-MM-DD-feature/runtime.control.json plus a short /goal pointer
```

For simple work, the router should reject the controlled-run chain and recommend an inline prompt or inline `/goal`.

## Included skills

- `framing-cybernetic-intent`: collaboratively frame pre-task human intent into shared understanding before optional task formation and routing.
- `routing-cybernetic-workflows`: classify complexity and route to the right workflow.
- `analyzing-cybernetic-requirements`: analyze human intent and create `requirements.control.json`.
- `clarifying-cybernetic-tasks`: deprecated compatibility alias for `analyzing-cybernetic-requirements`.
- `designing-cybernetic-solutions`: create a general solution/system model when Design Gate is required.
- `orchestrating-cybernetic-pregoal`: orchestrate the pre-goal compilation chain after requirements analysis, including design dispatch when required.
- `recording-cybernetic-run-outcomes`: record local metadata-only cybernetic run outcomes without upload or self-modification.
- `cybernetic-superpowers-infrastructure`: define stage-specific Superpowers substrate dependencies and non-substitution rules.
- `writing-cybernetic-goals`: create a control contract, not a runtime `/goal`, for complex work.
- `writing-cybernetic-execution-policies`: create an execution policy / plan as a control law.
- `reviewing-cybernetic-control-structures`: review requirements analysis, design when required, goal, and plan as a coherent control system.
- `compiling-cybernetic-runtime-goals`: compile `runtime.control.json` and a short runtime `/goal` pointer only after approval gates pass.

## Observability / meta-control

The pack includes an optional local-first observability layer under `observability/`.

Defaults:

- local recording only;
- `metadata_only` mode;
- no raw prompt, content summary/excerpt, artifact body, code/log excerpt, credential, customer data, real path, or real repository name upload by default;
- no network sync from ordinary skill execution;
- no automatic skill modification, release publishing, or machine update.

Manual sync and aggregation are script-driven. Cloud-side outputs are candidates for review, not accepted control-law changes.

## Framework maintenance

Cross-artifact control rules are tracked in `docs/cybernetic-framework/invariant-artifact-consumer-matrix.md`.

When adding or changing an invariant, update that matrix in the same change so the rule is mapped across source skill text, artifact templates, deterministic guards, review dimensions, runtime/downstream consumers, and regression coverage.

## Scripts

The scripts are intentionally small and deterministic. They check structure and phase gates; they do not decide requirement semantics.

- `control_artifact_lint.py`: lint requirements analysis/design/goal/plan/review control artifacts.
- `check_pregoal_inputs.py`: check that orchestration starts from the expected requirements analysis input.
- `control_chain_guard.py`: block premature runtime goal compilation.
- `compile_runtime_goal.py`: compile approved runtime control JSON and the short `/goal` pointer.
- `validate_run_events.py`: validate metadata-only run-event files and taxonomy codes.
- `record_run_event.py`: write or dry-run local metadata-only JSONL run events.
- `redact_run_event.py`: remove unsafe fields before export.
- `sync_run_events_to_github.py`: dry-run/export by default and refuse real upload unless explicitly configured.
- `aggregate_run_events.py`: create non-live machine-readable aggregation summaries and eval-candidate packages.

## Why this structure exists

Pre-goal skills synthesize and review the solution model and control structure. `/goal` runs the approved control structure. This separates controller synthesis from controller execution and prevents an execution agent from designing, approving, and running its own control law.
