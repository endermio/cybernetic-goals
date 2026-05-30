# Goal Contract: Orchestration State Guard

## Human Purpose

Make `$orchestrating-cybernetic-pregoal` enforce pre-goal ordering through artifacts and guard checks, not natural-language reminders.

## Objective

Update the orchestrator so required pre-goal stages cannot be skipped:

- requirements must be complete before design;
- Design Gate required means `$designing-cybernetic-solutions` must run before goal writing;
- solution design synthesis must not be emulated inside the orchestrator;
- any existing design artifact must propagate to goal, execution policy, control review, and runtime compilation;
- runtime `/goal` compilation must remain blocked until review approval and Final Observer checks pass.

## Success Condition

Codex may stop only when:

- `$orchestrating-cybernetic-pregoal` documents a finite orchestration state machine and Design Dispatch Rule.
- `docs/cybernetics/orchestrations/YYYY-MM-DD-slug.md` status artifact shape is represented in the orchestrator status template.
- `.agents/skills/orchestrating-cybernetic-pregoal/scripts/orchestration_guard.py` exists and blocks invalid stage transitions.
- Orchestrator evals cover skipped design, unavailable design skill, existing design propagation, and runtime compile before approved review.
- Existing runtime and control-review guards remain compatible.
- Verification commands pass.

## Source of Truth

Read first:

- User request in this thread: enforce orchestrator ordering via state machine, status artifact, guard script, and evals.
- `.agents/skills/orchestrating-cybernetic-pregoal/SKILL.md`
- `.agents/skills/designing-cybernetic-solutions/SKILL.md`
- `.agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py`
- `.agents/skills/reviewing-cybernetic-control-structures/scripts/control_artifact_lint.py`

## Scope and Boundaries

Allowed:

- Update `$orchestrating-cybernetic-pregoal` instructions, references, status template, scripts, and evals.
- Add `orchestration_guard.py`.
- Add concise README text only if needed to state that full pre-goal orchestration includes the design stage but design remains owned by `$designing-cybernetic-solutions`.
- Adjust tests/evals or documentation needed for the new guard behavior.

Forbidden unless explicitly approved:

- Delete or merge `$designing-cybernetic-solutions`.
- Copy the solution design template into the orchestrator.
- Let the orchestrator synthesize solution design as a fallback.
- Change Design Gate from conditional to always required.
- Require standalone design approval before downstream use.
- Start runtime `/goal` execution.
- Introduce domain-specific vocabulary into the core skills.

## Invariants

Do not regress:

- `$designing-cybernetic-solutions` owns solution-model synthesis.
- `$orchestrating-cybernetic-pregoal` owns sequencing, artifact path derivation, lifecycle checks, source-contract checks, blocking, and downstream propagation.
- Candidate, Reviewed, and Approved design artifacts may enter downstream stages when source contracts are valid and no blocking open design questions remain.
- Existing design artifact presence means downstream artifacts and runtime compiler must include the design path, even if Design Gate is satisfied.
- Missing `$designing-cybernetic-solutions` when Design Gate is required is a hard block, not a formatting fallback.

## Verification Surface

Focused checks:

- `python3 .agents/skills/orchestrating-cybernetic-pregoal/scripts/orchestration_guard.py --help`
- `python3 -m json.tool .agents/skills/orchestrating-cybernetic-pregoal/evals/evals.json >/dev/null`
- `rg -n "orchestration_guard|Design Dispatch Rule|Orchestration State Machine|Next Allowed Action" .agents/skills/orchestrating-cybernetic-pregoal`

Broader checks:

- `for f in $(find .agents/skills -path '*/evals/*.json' -type f | sort); do python3 -m json.tool "$f" >/dev/null; done`
- `python3 -m compileall -q .agents/skills/*/scripts`
- `git diff --check`

Artifact checks:

- `bad='designing-cybernetic-'system; rg -n "${bad}s|${bad}" .` must return no matches.
- `rg -n "emulate.*solution design|solution design.*fallback|synthesize solution design" .agents/skills/orchestrating-cybernetic-pregoal` must show only blocking/non-fallback language.

## Evaluation Rubric / Error Function

Not applicable. This is a bounded implementation goal, not an audit or status-classification task.

## Checkpoint Loop

For each checkpoint:

1. State checkpoint and expected observable state.
2. Make the smallest coherent change for that checkpoint.
3. Run the focused verification relevant to that checkpoint.
4. If verification fails, inspect evidence and repair.
5. Update progress log.
6. Run broader verification only at integration gates or final gate.

Recommended checkpoints:

1. Update orchestrator instructions with Design Dispatch Rule, Non-Fallback Rule, state machine, and guard-before-stage requirements.
2. Upgrade the orchestration status template to include Current State, Artifact Chain, Next Allowed Action, and Blocked Reason.
3. Add `orchestration_guard.py` with stage gates: `before-design`, `before-goal`, `before-policy`, `before-review`, and `before-runtime-compile`.
4. Add or update orchestrator evals for skipped design, unavailable design skill, existing design propagation, and compile-before-review blocking.
5. Run final verification.

## Repair Policy

- Use root-cause debugging for unclear failures.
- Do not weaken ordering invariants to make tests pass.
- Do not treat natural-language checklist compliance as equivalent to guard behavior.
- Stop if a requested change would merge solution-design synthesis into the orchestrator.

## Progress Log

Maintain:

- `docs/cybernetics/progress/2026-05-31-orchestration-state-guard.md`

Each entry must include:

- checkpoint
- files changed
- commands run
- result
- current risk
- next step

## Stop Conditions

Stop successfully when:

- Success Condition is met and verification evidence is recorded.

Stop early and report if:

- `$designing-cybernetic-solutions` ownership would need to change.
- The guard cannot distinguish Design Gate required from satisfied/not applicable.
- Existing artifacts make source-contract propagation ambiguous.
- A verification command fails and cannot be repaired without changing confirmed requirements.

## Blocked Report Format

If blocked, report:

- attempted paths
- evidence gathered
- current hypothesis
- exact blocker
- remaining risk
- smallest human decision or input needed

## Final Report Format

When complete, report:

- goal achieved
- verification evidence
- commands run
- files changed
- known residual risks
