# Goal Contract: Output Contract Gate

## Human Purpose

Make output shape part of the cybernetic control contract so agents do not treat a task as complete while delivering the wrong audience, medium, structure, detail level, destination, or machine-readable shape.

## Objective

Implement `Output Contract Gate` across the cybernetic skill chain so requirements analysis identifies output-contract needs, solution design defines complex output structures, goal contracts preserve final output requirements, runtime goal compilation enforces them, and the pre-goal orchestrator only propagates and validates them.

## Success Condition

Codex may stop only when:

- `analyzing-cybernetic-requirements` records Output Contract Gate and captures audience, purpose, medium, structure, detail level, evidence-reference needs, machine-readable needs, destination path, and acceptance condition.
- `designing-cybernetic-solutions` designs complex output/report structures when Output Contract Gate requires structure synthesis.
- `writing-cybernetic-goals` writes a `Final Output Contract` into goal files and prevents runtime from substituting another output shape.
- `compiling-cybernetic-runtime-goals` carries the approved final output contract into runtime `/goal` commands.
- `orchestrating-cybernetic-pregoal` propagates and validates output contract presence but does not design it.
- Requirements/design/goal evals cover Output Contract Gate behavior.
- Simple tasks do not start asking output-format questions by default.
- Response-only handoff prompts are not written into artifacts.
- Verification commands pass.

## Source of Truth

Read first:

- User request in this thread defining `Output Contract Gate`.
- Router decision in this thread: Level 2 bounded framework repair; no execution policy by default.
- `.agents/skills/analyzing-cybernetic-requirements/SKILL.md`
- `.agents/skills/analyzing-cybernetic-requirements/assets/requirements-analysis-template.md`
- `.agents/skills/designing-cybernetic-solutions/SKILL.md`
- `.agents/skills/designing-cybernetic-solutions/assets/solution-design-template.md`
- `.agents/skills/writing-cybernetic-goals/SKILL.md`
- `.agents/skills/writing-cybernetic-goals/assets/goal-contract-template.md`
- `.agents/skills/compiling-cybernetic-runtime-goals/SKILL.md`
- `.agents/skills/compiling-cybernetic-runtime-goals/scripts/compile_runtime_goal.py`
- `.agents/skills/compiling-cybernetic-runtime-goals/assets/runtime-goal-template.txt`
- `.agents/skills/orchestrating-cybernetic-pregoal/SKILL.md`

## Scope and Boundaries

Allowed:

- Update the named skills, templates, scripts, and evals needed to implement Output Contract Gate.
- Update `routing-cybernetic-workflows` only if needed to expose Output Contract Gate as a routable required gate.
- Add focused evals for requirements analysis, solution design, and goal preservation.
- Add deterministic checks in existing scripts when useful and tightly scoped.
- Add or update progress evidence for this bounded goal.

Forbidden unless explicitly approved:

- Create an execution policy or control review for this task.
- Turn Output Contract Gate into a mandatory question for every simple task.
- Let requirements analysis design complex report schemas.
- Let the orchestrator design output contracts.
- Write response-only handoff prompts, `$skill ...` commands, or runtime `/goal` prompts into persistent artifacts where they are not the artifact's core output.
- Rename existing skills or move directories.
- Introduce domain-specific output vocabulary into the core beyond neutral examples.

## Invariants

Do not regress:

- Requirements analysis identifies gate needs and safe defaults; it does not synthesize complex output structures.
- Solution design owns complex output/report/schema structure when structure synthesis is needed.
- Goal contracts freeze the final output contract for runtime.
- Runtime `/goal` follows the output contract and stops rather than inventing a substitute output shape.
- Orchestrator sequences, propagates, and validates artifacts; it does not synthesize output contracts.
- Level 2 bounded goals still output a direct `/goal` and do not recommend execution policy by default.
- Full pre-goal handoffs still return to `$orchestrating-cybernetic-pregoal`.

## Verification Surface

Focused checks:

- `python3 -m json.tool .agents/skills/analyzing-cybernetic-requirements/evals/evals.json >/dev/null`
- `python3 -m json.tool .agents/skills/designing-cybernetic-solutions/evals/evals.json >/dev/null`
- `python3 -m json.tool .agents/skills/writing-cybernetic-goals/evals/evals.json >/dev/null`
- `rg -n "Output Contract Gate|Final Output Contract|Output Contract" .agents/skills`

Broader checks:

- `for f in $(find .agents/skills -path '*/evals/*.json' -type f | sort); do python3 -m json.tool "$f" >/dev/null; done`
- `python3 -m compileall -q .agents/skills/*/scripts`
- `git diff --check`

Artifact checks:

- Search persistent artifacts for response-only handoff prompt headings and queue phrases using a locally composed pattern; it must return no matches except intentionally core runtime-goal templates.
- Search results for `Output Contract Gate` must show requirements/design/goal/runtime/orchestrator coverage.

## Evaluation Rubric / Error Function

Not applicable. This is an implementation goal, not an audit or status-classification task.

## Checkpoint Loop

For each checkpoint:

1. State checkpoint and expected observable state.
2. Make the smallest coherent change for that checkpoint.
3. Run focused verification.
4. If verification fails, inspect evidence and repair.
5. Update progress log.
6. Run broader verification only at integration gates or final gate.

Recommended checkpoints:

1. Add Output Contract Gate to requirements analysis instructions, template, and evals.
2. Add complex output-structure responsibility to solution design instructions, template, and evals.
3. Add `Final Output Contract` to goal-writing instructions, template, and evals.
4. Carry final output contract into runtime goal compilation.
5. Update orchestrator propagation/validation language without giving it design ownership.
6. Run final verification.

## Repair Policy

- Use root-cause debugging for unclear verification failures.
- Do not weaken gate semantics to make searches pass.
- Do not replace missing output-contract decisions with runtime improvisation.
- If an output contract affects execution or acceptance and no safe default exists, stop and report the smallest required human decision.

## Progress Log

Maintain:

- `docs/cybernetics/progress/2026-05-31-output-contract-gate.md`

Each entry must include:

- checkpoint
- files changed
- commands run
- result
- current risk

## Stop Conditions

Stop successfully when:

- Success Condition is met and verification evidence is recorded.

Stop early and report if:

- Implementing Output Contract Gate would require changing the confirmed ownership boundaries.
- A required output contract decision has multiple plausible shapes and no safe default.
- Verification fails and cannot be repaired within the confirmed scope.

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
