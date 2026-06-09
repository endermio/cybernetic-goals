# Execution Policy: JSON-only Control Facts Migration

## Execution Policy Status

Status: `Candidate`

## Source Contracts

- Requirements analysis: `docs/cybernetics/requirements/2026-06-09-json-only-control-facts-migration.md`
- Solution design: `docs/cybernetics/designs/2026-06-09-json-only-control-facts-migration.md`
- Goal: `docs/cybernetics/goals/2026-06-09-json-only-control-facts-migration.md`

## Superpowers Planning Workflow

- Required workflow: `$superpowers:writing-plans`
- Workflow status: `Used`
- Planning status: `Candidate`

Task constraints supplied to the workflow:

- JSON is the only official target control fact source;
- Markdown official guard/compiler/runtime input must fail after migration;
- approved control JSON is runtime read-only;
- runtime writes only progress/status/final-report files;
- verifier output is required before `goal_achieved: true`;
- final execution uses `Parallel subagent-driven` with `superpowers-dispatching-parallel-agents`, `parallel-max-safe`, and `Max concurrent subagents: auto`;
- each work package must advance required answer steps or be marked supporting-only.

## Rules That Cannot Change

These cannot be changed during runtime execution without stopping.

- Do not keep Markdown as an official guard/compiler/runtime control input.
- Do not keep long-term Markdown/JSON dual compatibility.
- Do not let runtime edit approved requirements/design/goal/plan/review/runtime JSON.
- Do not allow `goal_achieved: true` without verifier permission.
- Do not treat JSON sidecars as sufficient if Markdown remains authoritative.
- Do not treat component completion as completion without required-step evidence.
- Preserve high-concurrency subagent execution unless a new human-approved requirement changes it.

## Tactical Degrees of Freedom

These may change during execution if rules that cannot change are preserved.

- Exact schema file directory.
- Exact helper script names.
- Whether a one-time migration helper exists for fixtures/examples.
- Exact test split across files.
- Exact deletion order for old Markdown templates and parsers.
- Whether raw evidence is cached or only referenced by pointer.

## Dependency Matrix

| Workstream | Owns | Depends on | Can run in parallel with | Check |
|---|---|---|---|---|
| WP1 JSON schemas and registries | Schemas, shared definitions, registry key validation, delegation registry normalization | Requirements/design S1-S3 | WP2, WP5 initial regression fixture inventory | Schema and registry tests |
| WP2 JSON operation skill and runtime protocol | `using-control-json` skill, JSON protocol, runtime read/write rules | Requirements/design S4 | WP1, WP5 initial regression fixture inventory | Skill/protocol tests |
| WP3 Guard/compiler JSON conversion | Guard JSON loader, Markdown rejection, compiler JSON input, runtime pointer output | WP1, WP2 protocol shape | WP4 after schema interfaces are stable | Guard/compiler tests |
| WP4 Builders/templates hard cut | JSON builders/examples, removal or deauthoring of Markdown templates, run layout | WP1 schema interfaces | WP3 after lock split | Builder/template tests and lint |
| WP5 Progress/verifier and regressions | Progress JSONL schema, verifier, old accident JSON regressions | WP1 schema definitions and WP2 protocol | WP3/WP4 after integration barrier | Verifier and regression tests |
| WP6 Final integration | Full verification, progress record, commit/push evidence | WP1-WP5 | none | Full suite and final report |

## Who Does The Work / Context Use

Task level: `Level 3`

Who does the work: `Parallel subagent-driven`

Selected agent workflow: `superpowers-dispatching-parallel-agents`

Subagent execution mode: `parallel-max-safe`

Max concurrent subagents: `auto`

Agent workflow compatibility:

Use `.agents/skills/references/delegation-workflow-registry.json` as the source of workflow capability limits.

| Selected agent workflow | Allowed work assignment | Allowed mode |
|---|---|---|
| `superpowers-dispatching-parallel-agents` | `Parallel subagent-driven` | `parallel-max-safe` |

Agent workflow compatibility rationale:

- The user explicitly clarified that the final compiled execution must use subagent high-concurrency mode. `superpowers-subagent-driven-development` is not used because it is serial-single-active; `superpowers-dispatching-parallel-agents` is the compatible Superpowers workflow for independent parallel domains under main-agent wave/lock/barrier integration.

Concurrency selection rationale:

- The migration has independent frontiers: schemas/registries, runtime JSON skill/protocol, Markdown dependency inventory, and regression fixture inventory can start concurrently. Later guard/compiler, builder/template removal, and verifier/regression work have explicit dependency barriers and disjoint file locks. This supports max-safe-parallel with `auto` concurrency.

Concurrency frontier rule:

- Launch all work packages in the current approved wave whose required-step dependencies are satisfied and whose locks are disjoint. Do not launch a later wave until the main agent integrates previous wave outputs and verifies no control-rule conflict.

Conflict / lock model:

| Artifact / state / shared place | Lock owner | Conflict rule |
|---|---|---|
| `.agents/skills/references/answer-method-registry.json` and `.agents/skills/references/delegation-workflow-registry.json` | WP1 | Exclusive write lock; other packages read-only until barrier |
| Schema files | WP1 | Exclusive write lock; consumers may read after schema barrier |
| `.agents/skills/using-control-json/` | WP2 | Exclusive write lock |
| Guard scripts | WP3 | Exclusive write lock |
| Compiler scripts and predictor scripts | WP3 | Exclusive write lock |
| Markdown control templates and JSON builders/examples | WP4 | Exclusive write lock |
| Progress/verifier scripts and regression fixtures | WP5 | Exclusive write lock |
| Shared tests index or common test helpers | Main agent | Barrier-required; no parallel direct edits without main integration |
| Approved requirements/design/goal/plan/review/runtime JSON in target system | Runtime | Read-only; runtime writes progress/status/final-report only |

Parallel wave matrix:

| Wave | Required-step frontier | Work packages | Independence proof | Shared places / locks | Integration barrier |
|---|---|---|---|---|---|
| Wave 1 | S1, S2, S3, S4, S9 fixture inventory | WP1 schemas/registry, WP2 JSON operation skill, WP5 regression inventory | Registry/schema, skill/protocol, and regression inventory have disjoint write sets | WP1 registry/schema lock; WP2 skill lock; WP5 tests/fixture inventory lock | Main agent validates schema/protocol vocabulary and registry keys before consumers edit guard/compiler |
| Wave 2 | S5, S6, S7, S8 | WP3 guard/compiler JSON conversion, WP4 builders/templates hard cut, WP5 progress/verifier implementation | WP3 scripts, WP4 builders/templates, and WP5 verifier have separate primary files after Wave 1 interfaces | WP3 guard/compiler lock; WP4 builder/template lock; WP5 verifier lock | Main agent runs focused guard/compiler/verifier tests and reconciles deleted Markdown paths |
| Wave 3 | S9, S10 | WP5 old accident JSON regressions, WP6 final integration | Regression completion and integration verification happen after implementation; no further parallel writes without barrier | Main agent owns shared test suite and progress record | Main agent runs full verification, commits, pushes, and reports |

Failure policy:

- If one subagent blocks, fails, or returns conflicting evidence, stop launching later waves. The main agent integrates non-conflicting completed outputs, records the blocker, and either repairs within the same approved scope or stops for the smallest required human decision.
- If two packages need the same locked file, the main agent serializes that portion at the integration barrier.
- If high-concurrency mode becomes unsafe, do not silently downgrade to serial; stop and revise the execution policy with human approval.

Main-agent integration rule:

- Subagent outputs are candidate outputs only. They become accepted progress state only after the main agent checks file diffs, verifies required evidence, confirms lock compatibility, updates the progress log, and runs the wave integration checks.

Work Assignment rationale:

- This is Level 3 repository architecture migration across schemas, skills, guards, compiler, verifier, and tests. A main-only agent would become worker, coordinator, integrator, and verifier at once. Parallel subagents can safely work on disjoint surfaces under explicit wave, lock, and barrier controls.

Main-only context-load justification:

- Not applicable; selected work assignment is `Parallel subagent-driven`.

Main agent owns:

- approved approved files
- current batch state
- dispatch
- integration
- progress log
- stop-condition detection

Subagent owns:

- one bounded work package
- one bounded investigation
- one bounded verification pass

Delegation matrix:

| Work package | Executor | Context pack | Allowed actions | Return format | Integration check |
|---|---|---|---|---|---|
| WP1 schemas and registries | `parallel subagent` | requirements/design/goal excerpts; registry files; schema target list | Create/modify schema and registry validation files only | Summary, files changed, schema commands/results, registry consistency notes | Main verifies schema tests and registry key compatibility |
| WP2 JSON operation skill | `parallel subagent` | requirements/design/goal excerpts; skill target path; runtime write rules | Create `using-control-json` skill and protocol/tests only | Summary, files changed, skill protocol, tests | Main verifies skill does not author approved JSON or parse Markdown |
| WP3 guard/compiler JSON conversion | `parallel subagent` | requirements/design/goal/plan excerpts; guard/compiler scripts; schema interfaces | Modify guard/compiler/predictor official paths only | Summary, files changed, guard/compiler commands/results | Main verifies Markdown official inputs fail and JSON inputs pass |
| WP4 builders/templates hard cut | `parallel subagent` | requirements/design/goal excerpts; template/builder paths | Replace official Markdown templates with JSON builders/examples or non-official docs | Summary, files changed, lint/test results | Main verifies no official template teaches Markdown control facts |
| WP5 verifier/regressions | `parallel subagent` | requirements/design/goal excerpts; old accident list; progress/final report schema | Create verifier/progress tests and JSON regression fixtures | Summary, files changed, verifier/regression results | Main verifies verifier gates completion and regressions cover prior accidents |
| WP6 final integration | `main` | all approved artifacts and subagent outputs | Integrate, run verification, commit, push, report | Final summary and evidence | Full verification passes or honest not-done report |

Context Pack Requirements:

| Field | Content |
|---|---|
| Relevant control excerpts | Requirements JSON-only target, design required answer path S1-S10, goal rules that cannot change, this work assignment |
| Current batch objective | The wave-specific required step frontier and work package objective |
| Allowed artifacts/places | Only files named in the work package context pack and disjoint locks |
| Forbidden changes | Approved requirements/design/goal/plan/review artifacts, unrelated docs, external systems, unowned locked files, scope changes |
| Required evidence checks/evidence | Package-specific focused tests, schema validation, guard/compiler/verifier checks, or regression results |
| Stop conditions | Missing schema interface, lock conflict, forbidden Markdown compatibility need, verifier ambiguity, or human decision needed |
| Expected return format | Summary, files changed, commands run, result, evidence references, blockers, and risk |

Subagent workflow:

- Use `superpowers-dispatching-parallel-agents` for `Parallel subagent-driven` execution.
- Dispatch only approved wave packages with disjoint locks.
- Main agent integrates candidate subagent outputs at barriers.
- Do not use `superpowers-subagent-driven-development`; it is serial-single-active and incompatible with this approved `parallel-max-safe` plan.

Parallel approval record:

- Human approval: `approved`
- Dependency independence: `yes`
- Control-review approval: `approved`

Context Compression Rule:

At each batch break, update the progress log with:

- Active control summary: JSON-only target, high-concurrency work assignment, and stop conditions
- Completed work packages: completed and integrated packages
- Subagent outputs integrated: candidate outputs accepted by main agent
- Evidence produced: schema/guard/compiler/verifier/regression evidence references
- Deferred evidence checks and reasons: final-only or blocked evidence
- Unresolved blockers: blockers requiring revision or human input
- Deviations from policy: deviations and whether execution must stop
- Next allowed action: next approved wave or integration action

## Work Coverage And Action Limits Matrix

Use this section for full-route or multi-batch controlled work. Authority limits define runtime handling; they must not silently shrink the work covered in this run.

| Work item / place | In work covered in this run? | What the agent may do | Required runtime handling | Counts as achieved? |
|---|---|---|---|---|
| JSON schemas and shared definitions | yes | execute | Create/modify and test | yes, when validated and integrated |
| Registries and registry validation | yes | execute | Normalize and validate machine-only keys | yes, when registry consistency tests pass |
| `using-control-json` skill | yes | execute | Create skill/protocol/tests | yes, when runtime protocol tests pass |
| Guard official control path | yes | execute | Convert to JSON inputs and reject Markdown official inputs | yes, when guard tests pass |
| Compiler official control path | yes | execute | Convert to JSON input and short pointer output | yes, when compiler tests pass |
| Progress/verifier runtime files | yes | execute | Implement append-only progress and verifier completion rule | yes, when verifier tests pass |
| Markdown control templates/parsers | yes | execute | Delete, replace, or deauthorize from official path | yes, when official Markdown input fails |
| Old accident regressions | yes | execute | Port to JSON fixtures and verify failure modes | yes, when tests pass |
| External production/live systems | no; explicitly out-of-scope by What the User Approved | forbidden-not-executed | Do not touch; report not executed if encountered | no |
| Unrelated docs/history | no; explicitly out-of-scope by What the User Approved | forbidden-not-executed | Do not touch except incidental references needed for tests | no |

Rules:

- Every work covered in this run item must be accounted for as executed, prepared-only, observe-only, forbidden-not-executed, or explicitly out-of-scope by what the user approved.
- What the agent may do limits change handling, not scope.
- Do not move work covered in this run items to future roadmap, handoff, or later goal because they are unauthorized for direct execution.
- Unauthorized live or irreversible actions must be reported as not executed, with required preparation evidence when applicable.
- If the work covered in this run itself is too broad, stop and return to requirements/What the User Approved revision instead of narrowing it inside the execution policy.

## Where The Result Must Show Up

For compiled runtime goals, always include this section.

### Places The Result Appears

| Place | Role in result claim | Required action | Verification / reconciliation |
|---|---|---|---|
| `.agents/skills/*` cybernetic skills | policy and runtime instructions | change/inspect | Skill tests and lint confirm JSON-only instructions |
| JSON schemas | structural control facts | create/change | Schema validation tests |
| Registries | internal type/workflow method tables | change/inspect | Registry key tests |
| Guard scripts | official admission control | change | Valid JSON passes; Markdown official input fails |
| Compiler scripts | runtime contract compiler | change | JSON input compiles to runtime JSON and short pointer |
| Runtime progress/verifier scripts | completion control | create/change | Progress and verifier tests |
| Tests/evals | regression evidence | change | Old accident JSON regression suite passes |
| Markdown templates/parsers | old control source | delete/deauthorize/inspect | Official path cannot succeed from Markdown control artifacts |
| `docs/cybernetics/runs/<slug>/` | target run artifact layout | create in target implementation | Run fixture validates |

### Place Classes

Must act:

- schemas, registries, guard scripts, compiler scripts, JSON operation skill, verifier/progress scripts, tests/evals, official templates/builders.

Must inspect:

- current Markdown parsers, predictor, artifact lint, runtime goal compiler, old tests.

Must preserve:

- historical Markdown docs as non-authoritative history when unrelated to official target path.

Explicitly out of scope:

- external production systems, unrelated docs, unrelated target work.

Unknown or requires discovery:

- any hidden Markdown parser discovered during S1 inventory.

### Residual Reconciliation

After action, reconcile:

- old-state residuals: Markdown parsers/templates/tests still present;
- unhandled places: any official tool accepting `.md` control inputs;
- unexplained differences: registry key mismatch or schema drift;
- preserved or excluded places and rationale: historical docs kept as non-authoritative;
- places requiring later observation: none expected if tests cover official paths;
- allowed result claim wording for result-placement adequate, partial, missing, unavailable, or not applicable with justification.

## Steps That Make The Result True

For implementation work, decompose by the state transitions that make the result true, not by component inventory.

| Required step | Required state transition | Required evidence |
|---|---|---|
| S1 | Markdown-authoritative control chain -> complete inventory of official Markdown dependencies | Inventory and failing-input list |
| S2 | No complete JSON schema set -> strict control JSON schema set exists | Schema files and schema validation tests |
| S3 | Registry keys are sidecar-only/partial -> registry bindings are first-class machine-only JSON fields | Registry validation tests |
| S4 | Codex may infer JSON semantics -> JSON operation skill defines read/write/verify protocol | Skill/protocol files and tests |
| S5 | Guard parses Markdown -> guard validates JSON and rejects Markdown official input | Guard tests |
| S6 | Compiler reads Markdown and writes `.goal.md` -> compiler reads JSON and emits `runtime.control.json` plus short `/goal` | Compiler tests and pointer output |
| S7 | Runtime self-certifies completion -> progress JSONL plus verifier controls completion claim | Progress/verifier tests |
| S8 | Markdown templates/parsers remain official -> Markdown official inputs fail or are removed/deauthorized | Markdown rejection tests |
| S9 | Old accident tests are Markdown-bound -> JSON regressions block old failure modes | Regression suite |
| S10 | Candidate migration changes -> verified, committed, pushed, and reported result | Full verification, progress record, commit/push evidence |

Rules:

- Every mainline work package must map to at least one required step.
- Supporting-only work must be marked as supporting-only and cannot satisfy goal progress by itself.
- Do not defer the primary actor-centered path to future work while claiming workflow or component completion.
- Component evidence supports the required answer path; it does not replace required step evidence.

## Action That Can Make It Done

Action that can make it done:

- Implement the JSON-only control fact migration across schemas, registries, JSON operation skill, guards, compiler, progress/verifier, official Markdown rejection, and JSON regressions; then run final verification, commit, push, and report.

Proof of impossibility, if any:

- Impossibility is proven only if official JSON guard/compiler/runtime behavior cannot be implemented without preserving Markdown as authoritative, or if verifier semantics cannot be made deterministic enough to prevent false completion claims.

If it is not done, what should be reported:

- If it is not done, report `goal_achieved: false`, the required steps satisfied/missing, which official path still reads Markdown or lacks verifier coverage, and the smallest next action that can make it done. This report cannot satisfy the what counts as done.

## Work Size And Evidence Check Budget

### Batch Granularity

Each batch must represent a coherent intended-result slice, not a mechanical micro-step.

| Batch | Coherent intended-result slice | Why this is one batch | Too-small split avoided |
|---|---|---|---|
| Wave 1 | Schemas/registry/protocol foundations | These define the interfaces consumed by later work | Avoids separate micro-batches per schema file |
| Wave 2 | Guard/compiler/verifier/template conversion | These make official behavior JSON-owned | Avoids isolated script edits without integration |
| Wave 3 | Regression and final integration | These prove the target behavior as a whole | Avoids claiming per-component success |

### Evidence check Budget

| Batch | Required strong evidence checks | Optional/weak evidence checks | Deferred evidence checks | Final-only evidence checks |
|---|---|---|---|---|
| Wave 1 | Schema and registry focused tests | Lint for new skill text | Full test suite | Full suite |
| Wave 2 | Guard/compiler/verifier focused tests | Artifact hygiene lint | Full old regression suite | Full suite |
| Wave 3 | JSON regressions, full pytest target, diff check | None | None | Full final verification |

## Batch Cadence

- Intermediate steps inside a wave may temporarily break old Markdown-oriented tests when the wave is explicitly replacing old behavior.
- Each wave must end in an openable or meaningfully verifiable state.
- Batch size should avoid both micro-step local minima and huge unobservable changes.

## Destructive Intermediate-State Policy

Allowed inside a batch:

- Temporary failure of old Markdown control tests while converting them to JSON-only expectations.
- Temporary absence of old Markdown templates after replacement path exists inside the same wave.

Not allowed even inside a batch:

- Losing the JSON-only target.
- Allowing runtime to mutate approved JSON.
- Letting verifier bypass become the completion path.
- Touching external/live systems.

Batch-end requirements:

- Focused tests for the wave pass or failures are root-caused and recorded as blockers.

## Output Material / Evidence Collection

| Required output material | Producing batch/checkpoint | Evidence reference location | Ready before final output? | Missing material blocks completion? |
|---|---|---|---|---|
| Changed file summary | All waves | progress log and final answer | yes | yes |
| Verification commands/results | Wave 3 | progress log and final answer | yes | yes |
| Runtime pointer path | Compiler work package | compiler output and final answer | yes | yes |
| Commit/push status | Final integration | git output and final answer | yes | yes |
| Remaining gaps | Any blocked state | final answer | yes if gaps exist | no, but forces `goal_achieved: false` if blocking |

Final output readiness:

- Final report can be produced only after final verification, review of subagent outputs, commit, and push.

Blocking missing material:

- Missing verifier result, missing Markdown rejection evidence, missing JSON compiler output, or missing commit/push status blocks achieved wording.

## User Purpose Strategy

### Internal feedback

- Schema, guard, compiler, verifier, and regression tests support repository-level control correctness.

### Integration feedback

- Valid JSON chain compiles to runtime JSON and short `/goal`; Markdown official input fails.

### User-purpose feedback

- The smallest sufficient feedback is a concise final report with changed areas, verification commands, runtime pointer, and commit/push status.

### Operational feedback, if relevant

- Not required; no external production deployment is in scope.

### Feedback cadence

- Per batch: focused tests and progress log.
- Integration checks: guard/compiler/verifier focused tests.
- Final: JSON regressions, lint/diff checks, commit/push.
- Deferred feedback and reason: none expected.

### Evidence unavailable handling

- Verified: record exact tests and outputs.
- Not yet observed: record missing official path or verifier coverage.
- Smallest next observation: targeted test or guard/compiler run for missing path.
- Allowed completion wording: achieved only if final evidence satisfies goal.

## Evidence Lifecycle / Evidence Budget

The evidence lifecycle must keep tracked evidence reviewable and prevent repeated full raw evidence check output from outgrowing the controlled work.

| Evidence channel | Raw allowed? | Baseline policy | Per-batch retention | Delta required? | Summary required? | Max tracked size | Git policy | Raw pointer |
|---|---|---|---|---|---|---|---|---|
| Test output | yes, terminal/transient | none | summary + failing command if any | yes | yes | final answer under 70 lines; progress concise | tracked summaries only | command and timestamp |
| Guard/compiler output | yes, terminal/transient | none | summary + command | yes | yes | concise | tracked summaries only | command and timestamp |
| Regression fixture evidence | yes, fixture files | one fixture per failure class | pointer to fixture/test | no | yes | reviewable fixtures only | tracked if small | test path |

Rules:

- Keep at most one full baseline and one final full scan unless explicitly justified.
- Intermediate scans should store summary + delta, not repeated full raw hits.
- Full raw evidence check output belongs in local cache, ignored artifacts, compressed retained-full artifacts, or external artifact storage unless the goal explicitly requires tracked raw output.
- Tracked evidence must be reviewable without reading all raw evidence check output.

Evidence levels:

- Level 0 transient raw: local evidence check output, ignored by default.
- Level 1 raw pointer: path, hash, command, timestamp, and retention location.
- Level 2 reviewable summary/delta: tracked summary, delta, top offenders, representative samples, and manifest.
- Level 3 retained full evidence: final full scan only when explicitly justified.

## Evidence check / Evidence Governance

Approved evidence checks, checks, and evidence channels are evidence checks, not objectives.

Strong evidence checks to preserve:

- JSON schema validation.
- Registry consistency validation.
- Guard JSON pass / Markdown fail tests.
- Compiler JSON input and short pointer tests.
- Verifier completion-control tests.
- Old accident JSON regressions.

Weak or stale evidence checks to inspect before obeying:

- Tests requiring Markdown control artifacts as official inputs.
- Lints expecting Markdown section headings in generated control facts.

Obsolete evidence checks that may be retired and rewritten:

- Markdown section parser tests for official guard/compiler/runtime control paths.
- Runtime `.goal.md` contract tests for official JSON target behavior.

Intended-result evidence has priority over preserving brittle old evidence checks.

## Stale Evidence check Retirement and Rewrite Policy

A check or evidence channel may be retired or rewritten when:

- it encodes old requirement meaning;
- it over-constrains execution details;
- it conflicts with rules that cannot change;
- it prevents correct structural change.

Any retired/replaced evidence check must be recorded in the progress log with reason and replacement evidence coverage.

## Phase Checks

Before execution:

- review status must be Approved.

Before moving to next batch:

- current batch-end condition met;
- required strong evidence checks for this batch have been interpreted;
- deferred and final-only evidence checks remain deferred by policy, not by omission;
- progress log updated;
- no confirmed meaning rule violated.

Before completion:

- final verification evidence recorded;
- no unresolved conflict among requirements analysis, solution design, goal, plan, and review.

## Execution Rhythm

- Execute according to the selected Who Does The Work / Context Use.
- For `Parallel subagent-driven`, dispatch only work packages in the current approved wave whose dependencies are satisfied and whose conflict locks are disjoint.
- Do not let runtime `/goal` rewrite this policy.

## Stop Conditions

Stop if:

- the plan conflicts with requirements analysis or goal;
- the plan conflicts with required solution design;
- confirmed meaning appears wrong or insufficient;
- evidence check governance is insufficient for a failing check;
- the approved execution work assignment cannot be followed;
- executing further requires a new human decision;
- the approved batch cadence cannot be followed.

## Progress Log Rules

Maintain:

- `docs/cybernetics/progress/2026-06-09-json-only-control-facts-migration.md`

Each entry must include:

- batch/checkpoint, changed files, commands, result, and evidence interpretation;
- required-step status: satisfied, failed, blocked, unobserved, and supporting-only work not counted as goal progress;
- what counts as done status, action attempted or proof of impossibility, and smallest next action;
- result placement, purpose evidence, deferred checks, evidence budget, raw pointer/hash, and tracked summary/delta;
- active control summary, integrated subagent outputs, unresolved blockers, deviations, current risk, and next step.

## Candidate Plan Tasks

### Batch 1: JSON Schemas And Registry Bindings

Required step(s):

- S1
- S2
- S3

Role: `mainline`

State transition advanced:

- Current Markdown-authoritative chain and sidecar-only registry binding becomes an inventoried chain with strict JSON schemas and machine-only registry binding fields.

Transition evidence produced:

- Markdown dependency inventory, schema files, registry validation tests, and delegation registry consistency fix/test.

Integration check:

- Main agent verifies schema tests and registry validation pass and that JSON control semantics are not only sidecars.

Counts as goal progress: `yes`

Why this is not merely component completion:

- It creates the structural state needed for JSON to become the official control fact source and exposes any remaining Markdown authority.

### Batch 2: Runtime JSON Operation Skill

Required step(s):

- S4
- S7

Role: `mainline`

State transition advanced:

- Runtime Codex moves from natural JSON interpretation to an explicit read-only/writeable/progress/verifier protocol.

Transition evidence produced:

- `using-control-json` skill, JSON control protocol reference, progress event rules, runtime writable file rules, and skill/protocol tests.

Integration check:

- Main agent verifies the skill forbids editing approved JSON, instructs appending progress events, and requires verifier permission for completion.

Counts as goal progress: `yes`

Why this is not merely component completion:

- It changes runtime behavior from self-interpreting JSON to operating JSON under explicit control rules.

### Batch 3: Guard And Compiler JSON Conversion

Required step(s):

- S5
- S6
- S8

Role: `mainline`

State transition advanced:

- Official guard/compiler paths move from Markdown heading parsing and `.goal.md` runtime contracts to JSON schema/registry validation and `runtime.control.json` with short pointer output.

Transition evidence produced:

- JSON guard, JSON compiler, Markdown rejection tests, compiler short pointer tests.

Integration check:

- Main agent verifies valid JSON passes, Markdown official input fails, compiler emits `runtime.control.json`, and `/goal` output stays pointer-only.

Counts as goal progress: `yes`

Why this is not merely component completion:

- It changes official admission and runtime compilation behavior, not just script internals.

### Batch 4: Builders Templates And Hard Cut

Required step(s):

- S8
- S10

Role: `mainline`

State transition advanced:

- Official authoring moves from Markdown control templates to JSON builders/examples or schema-owned fixtures, with historical Markdown deauthorized.

Transition evidence produced:

- JSON builders/examples, removed/deauthorized Markdown templates, artifact hygiene updates, and tests/lint proving templates do not teach Markdown control facts.

Integration check:

- Main agent verifies official new-chain artifact generation is JSON and Markdown templates are not official runtime/guard/compiler inputs.

Counts as goal progress: `yes`

Why this is not merely component completion:

- It removes a source that would otherwise reintroduce Markdown control facts.

### Batch 5: Verifier And Old Accident JSON Regressions

Required step(s):

- S7
- S9
- S10

Role: `mainline`

State transition advanced:

- Prior failure modes become JSON regressions and completion claims become verifier-controlled.

Transition evidence produced:

- Verifier scripts/tests, JSON regression fixtures, final report schema tests, and old accident regression pass/fail evidence.

Integration check:

- Main agent verifies verifier blocks `goal_achieved: true` without satisfied required steps and old accident regressions pass against JSON.

Counts as goal progress: `yes`

Why this is not merely component completion:

- It directly controls whether the system can falsely claim completion in the new JSON representation.

### Batch 6: Final Integration Verification Commit And Push

Required step(s):

- S10

Role: `mainline`

State transition advanced:

- Candidate migration changes become verified repository state with commit/push evidence and concise human report.

Transition evidence produced:

- Full verification output summary, progress record, commit hash, push result, final chat report.

Integration check:

- Main agent runs final verification, checks git diff/status, commits, pushes, and reports residual gaps.

Counts as goal progress: `yes`

Why this is not merely component completion:

- It verifies the integrated target behavior and records the repository state that realizes it.
