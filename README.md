# Cybernetic Skills Pack

This package contains a pre-goal control pipeline for Codex-style agent work.

The core idea is:

```text
skills = compile-time control tools
/goal = runtime executor
Superpowers = planning/review/execution substrate
```

For complex work, do not let `/goal` clarify requirements, write its own plan, review its own plan, or invent a new control strategy during execution. Instead, prepare and approve control artifacts first, then compile the final runtime `/goal` command.

Superpowers dependencies are stage-specific infrastructure, not optional style suggestions. See `docs/cybernetic-framework/superpowers-infrastructure-policy.md`.

## Install

From this package root, copy the skill directories into either your user-level skill directory:

```bash
mkdir -p ~/.agents/skills
cp -R .agents/skills/* ~/.agents/skills/
```

or into a repository-local skill directory:

```bash
mkdir -p .agents/skills
cp -R cybernetic-skills-pack/.agents/skills/* .agents/skills/
```

## Recommended workflow

For complex work:

```text
$routing-cybernetic-workflows
  -> decide whether full pipeline is appropriate

$clarifying-cybernetic-tasks
  -> docs/superpowers/clarifications/YYYY-MM-DD-feature.md

$orchestrating-cybernetic-pregoal
  -> run the remaining pre-goal compilation chain after clarification is complete
```

The orchestrator drives the following skills and stops if the review cannot converge:

```text
$writing-cybernetic-goals
  -> docs/superpowers/goals/YYYY-MM-DD-feature.md

$writing-cybernetic-execution-policies
  -> docs/superpowers/plans/YYYY-MM-DD-feature.md

$reviewing-cybernetic-control-structures
  -> docs/superpowers/control-reviews/YYYY-MM-DD-feature.md

$compiling-cybernetic-runtime-goals
  -> final executable /goal command
```

For simple work, the router should reject the full pipeline and recommend an inline prompt or inline `/goal`.

## Included skills

- `routing-cybernetic-workflows`: classify complexity and route to the right workflow.
- `clarifying-cybernetic-tasks`: clarify human intent and create a clarification brief.
- `orchestrating-cybernetic-pregoal`: orchestrate the pre-goal compilation chain after clarification.
- `cybernetic-superpowers-infrastructure`: define stage-specific Superpowers substrate dependencies and non-substitution rules.
- `writing-cybernetic-goals`: create a control contract, not a runtime `/goal`, for complex work.
- `writing-cybernetic-execution-policies`: create an execution policy / plan as a control law.
- `reviewing-cybernetic-control-structures`: review clarification, goal, and plan as a coherent control system.
- `compiling-cybernetic-runtime-goals`: compile the final runtime `/goal` command only after approval gates pass.

## Scripts

The scripts are intentionally small and deterministic. They check structure and phase gates; they do not decide product semantics.

- `control_artifact_lint.py`: lint clarification/goal/plan/review artifacts.
- `check_pregoal_inputs.py`: check that orchestration starts from the expected clarification input.
- `control_chain_guard.py`: block premature runtime goal compilation.
- `compile_runtime_goal.py`: compile the final executable `/goal` command from approved artifacts.

## Why this structure exists

Pre-goal skills synthesize and review the control structure. `/goal` runs the approved control structure. This separates controller synthesis from controller execution and prevents an execution agent from designing, approving, and running its own control law.
