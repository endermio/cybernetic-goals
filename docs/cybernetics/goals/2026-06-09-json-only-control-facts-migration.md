# Goal: JSON-only Control Facts Migration

## Human Purpose

The human wants the cybernetic control chain to stop using Markdown as its control database and to prevent repeated failures caused by prose reinterpretation, jargon leakage, fragile section parsing, and runtime self-certification.

## Objective

Migrate the official cybernetic control chain so new official requirements/design/goal/plan/review/runtime/progress control facts are JSON-backed, registry-validated, runtime-operated through a JSON operation skill, and verifier-gated before any completion claim.

## Success Condition

Codex may report `goal achieved: yes` only when:

- the What counts as done in `What Counts As Done` is satisfied;
- the How We Know The User Purpose Was Met permits an achieved claim;
- the Where The Result Must Show Up permits the corresponding result claim.

No partial, diagnostic, blocked, invalid, unavailable, fallback, or report-when-not-done status may satisfy this success condition.

## How We Know The User Purpose Was Met

| Element | Requirement |
|---|---|
| Beneficiary / observer | Repository operator and downstream Codex runtime agent |
| Purpose-realizing outcome observed | A fresh official cybernetic control run can be authored, guarded, compiled, executed, and verified through JSON control files without Markdown control artifacts being accepted as official guard/compiler/runtime inputs |
| Supporting Evidence | Schema tests, registry tests, JSON guard tests, compiler tests, JSON operation skill tests, progress/verifier tests, and old-accident regressions |
| Sufficient evidence level | `integration` |
| If user-purpose evidence unavailable | Report which official path still reads Markdown or lacks verifier coverage and the smallest next migration step |
| Allowed completion wording | `achieved` only when JSON-only official control behavior and verifier-gated completion are observed |

Do not define success as internal evidence check success unless the human purpose is internal-state correctness.

## Where The Result Must Show Up

| Element | Requirement |
|---|---|
| Target state | Official cybernetic control facts move from Markdown artifacts to JSON control files |
| Required result places | Requirements/design/goal/plan/review/runtime artifact model, JSON schemas, registries, guard scripts, compiler scripts, JSON operation skill, progress files, verifier scripts, tests/evals, manifest/rule documentation, and runtime `/goal` pointer shape |
| Place actions | change schemas/scripts/skills/tests; inspect old Markdown hot paths; preserve historical Markdown only as non-authoritative history; exclude unrelated docs and production systems |
| Residual reconciliation | Identify and fail any official guard/compiler/runtime Markdown control input after migration; record any remaining historical Markdown as non-authoritative |
| Result-placement wording | Strongest positive result claim requires JSON-only behavior at official guard/compiler/runtime places |
| Partial/unavailable handling | If any official path still accepts Markdown as control input, report `goal_achieved: false` with exact remaining path |
| Distinction from user-purpose evidence | Result-placement evidence checks where the JSON-only rule appears; user-purpose evidence checks whether the new chain blocks prior failure modes |

## What Counts As Done

| Element | Requirement |
|---|---|
| What counts as done | Official guard/compiler/runtime paths accept JSON control files and reject Markdown control artifacts as control inputs; approved JSON remains read-only during runtime; runtime progress is JSONL events; verifier output is required before `goal_achieved: true`; old accident regressions pass against JSON. |
| Evidence needed to call it done | Strict JSON schemas, registry validation, JSON guard/compiler/runtime operation, `using-control-json` skill, progress JSONL protocol, verifier tests, Markdown rejection tests, and old accident regression tests all pass in a fresh verification run. |
| Allowed achieved claim | `goal achieved: yes; JSON is the official control fact source, Markdown official inputs fail, and verifier-backed runtime completion is enforced` |
| Steps that make the result true | S1 inventory Markdown control dependencies; S2 define JSON schemas; S3 define registry binding; S4 add JSON operation skill; S5 convert guards to JSON; S6 convert compiler to JSON runtime control and short pointer; S7 implement progress/verifier; S8 remove or fail official Markdown control inputs; S9 port regressions; S10 verify, commit, and report. |

Reports for incomplete work are outside this done-state table. User-purpose evidence and result-placement evidence are separate checks.

## Work Covered And Allowed Actions Contract

| Element | Requirement |
|---|---|
| Work covered in this run | The full repository migration needed to make JSON the official control fact carrier for cybernetic requirements/design/goal/plan/review/runtime/progress, including schemas, skill, guards, compiler, verifier, tests, and failure of official Markdown inputs |
| What the agent may do | Create/edit/delete local repository skills, schemas, builders/examples, guard scripts, compiler scripts, verifier scripts, tests/evals, manifest/rule docs, and control templates needed for the hard cut |
| Forbidden actions | External production or live-state changes, unrelated history deletion, unrelated docs rewrites, destructive branch changes outside normal git commits |
| Prepare-only / observe-only actions | Existing historical Markdown may be inventoried or preserved as non-authoritative history; external/live actions are forbidden-not-executed |
| Explicitly out-of-scope items | Rewriting unrelated observability docs, changing Codex product behavior, implementing unrelated target-work tasks |
| Work coverage rule | Every covered item must be executed, verified, or explicitly reported as not done; authority limits must not shrink the approved JSON-only migration into JSON sidecars or a future roadmap |

Authority limits change runtime handling, not the work covered in this run. Do not move work covered in this run items to future roadmap or handoff unless What the User Approved explicitly excludes them from this goal.

## Source of Truth

Read first:

- `docs/cybernetics/requirements/2026-06-09-json-only-control-facts-migration.md`
- `docs/cybernetics/requirements/2026-06-09-json-only-control-facts-migration.control.json`
- `docs/cybernetics/designs/2026-06-09-json-only-control-facts-migration.md`
- `.agents/skills/references/answer-method-registry.json`
- `.agents/skills/references/delegation-workflow-registry.json`

## Allowed And Forbidden Work

Allowed:

- Cybernetic skills, schemas, guards, compiler, verifier, tests/evals, run layout, runtime prompt/pointer generation, and framework docs needed for JSON-only official control.

Forbidden unless explicitly approved:

- External production changes, live remote actions, unrelated repository rewrites, or preserving a long-term official Markdown compatibility path.

## Rules That Must Not Change

Do not regress:

- JSON is the only official persistent control fact in the target state.
- Markdown is not accepted as official guard/compiler/runtime control input after migration.
- Approved control JSON is read-only during runtime.
- Runtime writes only progress/status/final-report files.
- Verifier output is required before `goal_achieved: true`.
- `/goal` is a short text pointer and not a control fact.
- Final execution uses high-concurrency subagent mode unless a new human-approved requirements revision changes it.

## Verification Checks

Supporting Evidence:

- JSON schema tests.
- Registry consistency tests.
- Guard valid-JSON and Markdown-rejection tests.
- Compiler JSON input and short pointer tests.
- `using-control-json` skill/protocol tests.
- Progress event and verifier tests.
- Old accident JSON regression tests.

Focused checks:

- `python3 -m pytest tests/skills -q`
- `python3 -m pytest tests -q`
- `python3 .agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py --help`

Broader checks:

- `python3 scripts/lint_cybernetic_artifact_hygiene.py`
- `git diff --check`

Artifact checks:

- JSON schemas and fixtures validate.
- Official guard/compiler/runtime reject Markdown control inputs.
- Runtime pointer command points to `runtime.control.json` and invokes the JSON operation skill.

## Final Answer Format

| Element | Requirement |
|---|---|
| Audience | Human operator and downstream maintainer |
| Purpose | execution record |
| Medium | chat summary plus committed repository artifacts |
| Required structure | changed areas, verification commands/results, runtime pointer path, commit/push status, and remaining gaps |
| Detail level | standard |
| Evidence references required | yes |
| Machine-readable required | yes, for runtime/control artifacts after migration |
| Destination path | repository files and final chat response |
| Acceptance condition | The user can run named checks and see JSON-only official behavior enforced |

## Final Final Answer Format

| Element | Requirement |
|---|---|
| Audience | Human operator and downstream maintainer |
| Purpose | execution record |
| Medium | chat summary plus committed repository artifacts |
| Required structure | changed areas, verification commands/results, runtime pointer path, commit/push status, and remaining gaps |
| Detail level | standard |
| Evidence references required | yes |
| Machine-readable required | yes, for runtime/control artifacts after migration |
| Destination path | repository files and final chat response |
| Acceptance condition | The user can run named checks and see JSON-only official behavior enforced |

Runtime must not substitute a different audience, purpose, medium, structure, detail level, destination, or machine-readable shape. If this contract is insufficient for execution or acceptance, stop and report the smallest required upstream decision.

## Evaluation Rubric / Error Function

| Rubric element | Confirmed meaning |
|---|---|
| Status meanings / pass-fail categories | JSON-only complete, partial migration, blocked, invalid |
| Evidence levels / evidence strength | Strong: guard/compiler/runtime/verifier operate on JSON and reject Markdown official input. Weak: JSON sidecars exist while Markdown still drives control. |
| Minimum evidence for strongest positive status | Schema tests, guard JSON tests, compiler JSON tests, runtime JSON skill tests, verifier tests, and old accident regressions pass |
| Downgrade rules | If Markdown remains accepted by official guard/compiler/runtime, status is partial or invalid. If verifier can be bypassed for `goal_achieved: true`, status is invalid. |
| External/unobservable dependency handling | No external production dependency expected; Codex `/goal` JSON-native behavior is not assumed |
| Confidence / evidence grade | Final report states verification commands and residual gaps |

## Checkpoint Loop

For each checkpoint:

1. State checkpoint and expected observable state.
2. Make the smallest coherent change for that checkpoint.
3. Run focused verification.
4. If verification fails, inspect evidence and repair.
5. Update progress log.
6. Run broader verification only at integration checks or final check.

## Repair Policy

- Use root-cause debugging for unclear failures.
- Do not weaken JSON-only rules to satisfy tests.
- Do not keep Markdown compatibility as a workaround.
- Stop if the approved answer method or work coverage must change.

## Progress Log

Maintain:

- `docs/cybernetics/progress/2026-06-09-json-only-control-facts-migration.md`

Each entry must include:

- checkpoint
- files changed
- commands run
- result
- current risk

## Stop Conditions

Stop successfully when:

- the JSON-only official control chain is implemented, verified, committed, pushed, and reported.

Stop early and report if:

- JSON-only migration cannot be completed without retaining Markdown official compatibility;
- verifier semantics cannot be made deterministic enough to control completion claims;
- a live/external action would be required;
- the high-concurrency execution policy becomes unsafe and requires new human approval.

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

- goal achieved: yes/no
- what counts as done met: yes/no
- evidence needed to call it done
- if no: not done reason
- if no: action that can make it done attempted or proof of impossibility
- if no: smallest next action that can make it done
- work covered in this run
- work covered in this run coverage: complete / partial / unavailable / explicitly bounded by requirements approval
- executed
- prepared-only
- forbidden-not-executed
- explicitly out-of-scope by requirements approval
- user purpose evidence status: achieved / partially observed / pending / unavailable / not required with justification
- highest purpose-relevant evidence observed
- JSON-only guard/compiler/runtime status
- verifier status for `goal_achieved: true`
- commit and push status
