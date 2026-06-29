# Cybernetic Skills Pack

This package provides JSON-controlled workflows for Codex-style agent work.
It is meant for work where the agent should not invent the target, plan, review
standard, or completion claim while executing.

Core split:

```text
skills = prepare and review control objects
/goal = execute an approved runtime control object
counterexample gates = quality control
validators = structural checks
```

Official persistent control facts live only in:

```text
docs/cybernetics/runs/<slug>/*.control.json
docs/cybernetics/runs/<slug>/progress.jsonl
docs/cybernetics/runs/<slug>/runtime-status.json
docs/cybernetics/runs/<slug>/final-report.json
docs/cybernetics/runs/<slug>/evidence/
```

Markdown files are background only. Do not use Markdown as official guard,
compiler, runtime, or long-term dual-path control input.

## When To Use

Use this pack when a task needs durable control over target meaning, completion
standards, evidence, review, or runtime authority.

Common cases:

- product or API work where "done" must preserve user-approved meaning;
- long-running implementation, debugging, performance, or integration work;
- work where missing context can make design or planning wrong;
- work that needs independent counterexample review before execution or
  completion;
- runtime work that must record progress and evidence before claiming success.

Do not use the controlled-run chain for ordinary direct work. If a normal
Codex answer, direct edit, small bounded fix, or inline `/goal` preserves the
target with less overhead, use that instead.

## Install

Recommended user-level install:

```bash
mkdir -p /home/ender/.agents/skills
rsync -a --delete .agents/skills/ /home/ender/.agents/skills/
diff -qr .agents/skills /home/ender/.agents/skills
```

Repository-local install:

```bash
mkdir -p /path/to/target-repo/.agents/skills
rsync -a --delete .agents/skills/ /path/to/target-repo/.agents/skills/
diff -qr .agents/skills /path/to/target-repo/.agents/skills
```

The `diff` command should print nothing.

## Recommended Workflow

Start from the human situation, not from a preferred process label:

```text
human situation
  -> $framing-cybernetic-intent, when intent is not yet a formed task
  -> $routing-cybernetic-workflows, when a formed task may or may not need this pack
  -> $analyzing-cybernetic-requirements
  -> user approval of requirements
  -> $orchestrating-cybernetic-pregoal
  -> short runtime /goal pointer
  -> /goal Use .agents/skills/using-control-json ...
```

Only route formed tasks. A requested method is not automatically the human
purpose.

### Requirements Analysis

`$analyzing-cybernetic-requirements` owns the requirements phase. It has three
internal stages:

1. Extract target meaning: source requirements, required outcomes, what counts
   as done, authority, forbidden actions, and counterexample contracts.
2. Discover and collect required information: derive facts that must be known
   before design or planning, run safe read-only collection, and run an
   independent information-sufficiency counterexample review.
3. Ask for user approval only after the information gate is satisfied or
   explicitly not required.

Do not ask the user to approve requirements while information sufficiency is
pending. Do not push pending facts into design or runtime as assumptions.

### Transition Gates

Transition gates say what must happen next. They are not status reports.

Important fields:

```text
agent_must_continue: true
  -> execute next_action internally and rerun the same gate

user_action_required: true
  -> stop and ask only for the requested user information, decision, or approval

approval_allowed: true
  -> the current stage may be shown to the user for approval

handoff_allowed: true
  -> the current stage may move to the next control phase
```

Examples:

```text
RunInformationCounterexampleReview
  -> agent-owned; do not ask the user for authorization

RunInformationGathering
  -> agent-owned if actions are safe read-only collection or no-side-effect probes

AskUserForInformation
  -> user-owned; ask for the specific credential, file, access, or business decision

ReadyForUserApproval
  -> user-owned; stop and ask the user to approve requirements
```

### Pre-goal Orchestration

After approved requirements exist, use `$orchestrating-cybernetic-pregoal`.

Default controlled-run shape:

```text
requirements.control.json
run.control.json
gen-000/runtime.control.json
```

Some runs also include expanded strategy artifacts:

```text
design.control.json
goal.control.json
plan.control.json
review.control.json
runtime.control.json
```

The orchestrator may coordinate:

- `$designing-cybernetic-solutions`
- `$writing-cybernetic-goals`
- `$writing-cybernetic-execution-policies`
- `$reviewing-cybernetic-control-structures`
- `$compiling-cybernetic-runtime-goals`

It must not execute target work. It outputs a short `/goal` pointer only after
review and structural gates pass.

### Strategy Policy

Do not use legacy "lean/full" process labels as control concepts.

Use `strategy_policy`:

```text
frozen_strategy
  -> runtime follows the approved strategy; if the strategy is wrong, stop for decision

reviewed_replanning
  -> runtime may propose reviewed amendments to strategy, while preserving approved target anchors
```

The strategy policy is separate from risk. Live operations, destructive
actions, external systems, credentials, deployment, or irreversible migration
still require explicit human gates.

### Runtime Execution

The runtime `/goal` should be pointer-only, for example:

```text
/goal Use .agents/skills/using-control-json and execute docs/cybernetics/runs/YYYY-MM-DD-slug/runtime.control.json. If the JSON is missing, invalid, inconsistent, or insufficient, stop and report the smallest required human decision.
```

Runtime must not rewrite requirements, invent a new plan, approve its own
review, or claim completion without verifier permission.

## Quality Gates

Counterexample gates are the quality gates. They try to prove the target,
stage, or completion claim is wrong.

Validators and schema checks are structural gates. They can say JSON is shaped
correctly, but they do not prove the work is semantically good.

Required counterexample gates appear at these points:

- requirements information sufficiency before user approval;
- pre-goal review before runtime compilation;
- each required step or stage target before treating it as completed;
- final runtime completion before `goal_achieved: true`.

Self-written evidence is not enough for quality approval. Use an independent
reviewer, subagent, explicit human approval, or another approved independent
review path.

## Included Skills

- `framing-cybernetic-intent`: frame pre-task human intent before task routing.
- `routing-cybernetic-workflows`: decide whether a formed task should use this
  pack or simpler direct work.
- `analyzing-cybernetic-requirements`: create requirements control JSON, run
  information sufficiency gates, and prepare user approval.
- `clarifying-cybernetic-tasks`: deprecated compatibility alias for
  `analyzing-cybernetic-requirements`.
- `designing-cybernetic-solutions`: create solution/system design when required.
- `writing-cybernetic-goals`: create goal control contracts.
- `writing-cybernetic-execution-policies`: create execution policy and work
  assignment control.
- `reviewing-cybernetic-control-structures`: review the approved work chain and
  counterexample gates.
- `orchestrating-cybernetic-pregoal`: coordinate approved pre-goal artifacts and
  compile a runtime pointer.
- `compiling-cybernetic-runtime-goals`: compile runtime control JSON and a short
  `/goal` pointer.
- `using-control-json`: execute an approved runtime control JSON goal.
- `using-bounded-control-json`: execute bounded runtime JSON goals with only
  goal/runtime control files.
- `recording-cybernetic-run-outcomes`: record local metadata-only process
  evidence.
- `cybernetic-superpowers-infrastructure`: define stage-specific Superpowers
  substrate dependencies.

## Useful Scripts

Key scripts:

```text
.agents/skills/analyzing-cybernetic-requirements/scripts/requirements_information_loop.py
.agents/skills/analyzing-cybernetic-requirements/scripts/predict_pregoal_handoff.py
.agents/skills/orchestrating-cybernetic-pregoal/scripts/orchestration_guard.py
.agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py
.agents/skills/compiling-cybernetic-runtime-goals/scripts/compile_runtime_goal.py
.agents/skills/using-control-json/scripts/validate_control_chain.py
.agents/skills/using-control-json/scripts/verify_runtime_progress.py
```

Typical checks:

```bash
python3 .agents/skills/analyzing-cybernetic-requirements/scripts/requirements_information_loop.py \
  --run-dir docs/cybernetics/runs/YYYY-MM-DD-slug --json

python3 .agents/skills/analyzing-cybernetic-requirements/scripts/predict_pregoal_handoff.py \
  docs/cybernetics/runs/YYYY-MM-DD-slug

python3 .agents/skills/orchestrating-cybernetic-pregoal/scripts/orchestration_guard.py \
  --state before-runtime-compile --run-dir docs/cybernetics/runs/YYYY-MM-DD-slug --json

python3 .agents/skills/using-control-json/scripts/validate_control_chain.py \
  docs/cybernetics/runs/YYYY-MM-DD-slug

python3 .agents/skills/using-control-json/scripts/verify_runtime_progress.py \
  docs/cybernetics/runs/YYYY-MM-DD-slug
```

## Common Failure Modes

- Asking the user to authorize `RunInformationCounterexampleReview`. That is an
  internal requirements-analysis gate.
- Asking for requirements approval before information sufficiency is satisfied.
- Treating a validator pass as semantic quality approval.
- Letting runtime write or approve its own plan.
- Treating "not already available" as blocked when the approved goal requires
  creating the missing capability.
- Reusing abandoned run drafts as approval sources.
- Claiming `goal_achieved: true` before final verifier permission.

## Observability

The optional observability layer under `observability/` is local-first.

Defaults:

- local recording only;
- `metadata_only` mode;
- no raw prompt, content summary/excerpt, artifact body, code/log excerpt,
  credential, customer data, real path, or real repository name upload by
  default;
- no network sync from ordinary skill execution;
- no automatic skill modification, release publishing, or machine update.

Cloud-side outputs are candidates for review, not accepted control changes.

## Maintenance

Cross-artifact control rules are tracked in:

```text
docs/cybernetic-framework/invariant-artifact-consumer-matrix.md
```

When adding or changing an invariant, update that matrix in the same change so
the rule is mapped across skill text, artifact templates, deterministic guards,
review dimensions, runtime consumers, and regression coverage.

## Why This Exists

Pre-goal skills prepare and review the control structure. `/goal` runs the
approved control structure. This separates control preparation from execution
and prevents an execution agent from defining, approving, and completing its own
task.
