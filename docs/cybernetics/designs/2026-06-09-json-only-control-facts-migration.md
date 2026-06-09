# Design: JSON-only Control Facts Migration

## Design Status

Status: `Candidate`

## Source Contracts

- Requirements analysis: `docs/cybernetics/requirements/2026-06-09-json-only-control-facts-migration.md`
- Requirements registry sidecar: `docs/cybernetics/requirements/2026-06-09-json-only-control-facts-migration.control.json`
- Existing source-artifact context:
  - `.agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py`
  - `.agents/skills/orchestrating-cybernetic-pregoal/scripts/orchestration_guard.py`
  - `.agents/skills/compiling-cybernetic-runtime-goals/scripts/compile_runtime_goal.py`
  - `.agents/skills/analyzing-cybernetic-requirements/scripts/predict_pregoal_handoff.py`
  - `.agents/skills/references/answer-method-registry.json`
  - `.agents/skills/references/delegation-workflow-registry.json`

## Human Purpose

The human wants the cybernetic control system to stop treating Markdown prose as the control database. The intended result is a structured JSON control chain that can be validated by schema and registry rules, operated by Codex through an explicit JSON protocol, and verified before any completion claim.

## Confirmed Meaning

The intended result is: chat is only the human confirmation place; JSON is the only official persistent control fact; registries hold internal method and workflow keys; guards validate JSON schema plus registry consistency; runtime uses a JSON operation skill; progress is JSONL events; verifier output controls `goal_achieved: true`; `/goal` is a short text pointer; Markdown is not an official guard/compiler/runtime input. Historical Markdown may remain as history, but not as a new-chain control source.

## Design Workflow

- required design: `Required`
- `$superpowers:brainstorming` status: `Not required`
- Reason: `The user and requirements already fixed the target architecture; the design task is to instantiate the required answer path and support model, not to explore alternatives.`

## Answer Method Check

Design must start with the required answer path. Use when What the User Approved records how the question should be answered or what is not enough.

| Element | Design |
|---|---|
| Approved answer method | By implementing a structured control migration: schema-first JSON control facts, explicit runtime JSON interpretation protocol, read-only approved chain, writable progress/status/report files, verifier-backed completion, and tests for previous failure modes. |
| Required answer path | Inventory current Markdown control inputs -> define JSON control schema set -> define registry mapping -> add JSON operation skill -> make guards consume JSON -> make compiler consume JSON and emit short `/goal` pointer -> make runtime write progress events only -> add verifier-controlled completion -> remove or fail official Markdown control inputs -> run JSON regressions. |
| Required steps covered | initial state: official control facts are Markdown-driven with small JSON sidecars only; state transition that makes the result true: schemas, registries, JSON operation skill, JSON guards/compiler/runtime, progress events, verifier, and regressions replace Markdown authority; observable target state: official guard/compiler/runtime accept JSON control files, reject Markdown control artifacts, and require verifier-backed completion. |
| What is not enough avoided | yes; the design rejects JSON sidecars while Markdown remains authoritative and rejects a `/goal` pointer to JSON without a JSON operation protocol and verifier. |

## Required Answer Path

| Required step | Required change or answer step | Required evidence | Completion condition |
|---|---|---|---|
| S1 | Markdown control dependency inventory completed | Inventory naming Markdown parsers, templates, generated control files, compiler inputs, predictor inputs, and tests still bound to Markdown | Inventory exists and separates current-system inputs from intended-result rejected inputs |
| S2 | JSON control schemas defined | `requirements.control.schema.json`, `design.control.schema.json`, `goal.control.schema.json`, `plan.control.schema.json`, `review.control.schema.json`, `runtime.control.schema.json`, `progress-event.schema.json`, and `final-report.schema.json` | Schemas use strict required fields and `additionalProperties: false` where appropriate |
| S3 | Registry binding model defined | Answer-method and workflow registry keys are represented in machine-only JSON fields while plain approved meaning stays in semantic fields | Registry keys are validated and forbidden substitutes / required nodes remain machine-checkable |
| S4 | JSON operation skill added | `using-control-json` or equivalent skill with read-only approved JSON, writable runtime files, progress event rules, verifier rule, and `/goal` adapter instructions | Runtime Codex has explicit instructions for reading, writing, and verifying control JSON |
| S5 | Official guards consume JSON | Guard scripts load JSON, validate schemas, validate registry keys, validate cross-file references, and reject Markdown official inputs | Valid JSON control chain passes; Markdown official input fails |
| S6 | Runtime compiler consumes JSON | Compiler reads run-directory JSON, writes `runtime.control.json`, and prints a short `/goal` that invokes the JSON operation skill | Compiler rejects Markdown control artifacts and does not inline long control prose into `/goal` |
| S7 | Runtime progress and completion verification implemented | `progress.jsonl`, `runtime-status.json`, `final-report.json`, append/validate helpers, and verifier scripts | Runtime can append observations only; verifier must permit `goal_achieved: true` |
| S8 | Markdown templates and parser reliance removed from official path | Control Markdown templates are deleted, replaced, or made non-official; Markdown section parser is removed from official guard/compiler/runtime paths | New official guard/compiler/runtime cannot succeed from `requirements.md/design.md/goal.md/plan.md/review.md` inputs |
| S9 | Old accident regressions rewritten for JSON | Regression tests cover wrong answer method, forbidden substitute, partial/blocked completion, authority shrink, supporting-only progress, missing review checks, and verifier bypass | Regression suite passes and demonstrates JSON-only enforcement |
| S10 | Final integration report and commit evidence produced | Progress record, verification commands, changed files, commit hash, and push status | Human can inspect concise chat summary and local evidence without reading control Markdown |

## What Supports Each Required Step

Design pieces exist to support required steps. Do not introduce components, actors, or mechanisms that are not mapped to a required step or marked supporting-only.

| Required step | Required support object/component/mechanism | Why needed | Evidence produced |
|---|---|---|---|
| S1 | Markdown dependency inventory worker | Prevents leaving hidden Markdown authority behind | Inventory report and failing-input list |
| S2 | Schema set and shared JSON definitions | Replaces heading/regex parsing with structural validation | Schema files and schema tests |
| S3 | Registry binding fields | Keeps internal method/workflow keys machine-readable without leaking them into plain approved meaning | Registry validation tests |
| S4 | `using-control-json` skill | Gives Codex an explicit control JSON read/write protocol | Skill file, protocol reference, skill tests |
| S5 | JSON guard rewrite | Makes official admission deterministic and JSON-owned | Guard tests for valid JSON and rejected Markdown |
| S6 | JSON compiler rewrite | Produces runtime JSON and short pointer instead of Markdown contract | Compiler tests and pointer output |
| S7 | Progress/verifier scripts | Prevents Codex from self-certifying completion | Verifier tests and progress-event tests |
| S8 | Template/parser removal path | Makes the hard cut real instead of dual-track compatibility | Tests proving official Markdown input failure |
| S9 | JSON regression suite | Preserves prior accident learnings in the new representation | Regression tests |
| S10 | Integration verification and commit/push record | Makes final result auditable without a large human-facing control file | Final chat summary, progress record, commit and push evidence |

### Relationships

The run directory owns one JSON control chain. Requirements, design, goal, plan, review, and runtime JSON are approved control files and are read-only during runtime. Progress JSONL, runtime-status JSON, and final-report JSON are runtime-writable. Registries are internal lookup tables. Guards and verifier read control JSON plus registries; Codex writes observations; verifier decides whether observations satisfy the approved chain.

### Information / State Flow

Chat confirmation produces requirements JSON. Builders or authoring helpers produce design/goal/plan/review JSON from approved semantics and registry bindings. Guard validates schema, registry compatibility, and cross-file references. Compiler writes runtime JSON and prints a short `/goal`. Runtime uses the JSON operation skill, appends progress events, runs verifier, and writes final-report JSON only after verifier output permits the claim.

### Inside / Outside This Design

Inside scope:

- Official JSON control artifact schemas.
- Run directory layout.
- Registry binding and validation.
- JSON operation skill and runtime protocol.
- Guard/compiler/verifier conversion.
- Tests and regressions for prior accidents.
- Markdown official-input failure rules.

Outside scope:

- External production or live-state changes.
- Changing Codex product support for `/goal`.
- Rewriting unrelated documentation.
- Keeping a long-term Markdown/JSON compatibility mode.

### Alternative Answer Paths Or Support Models Considered

| Option | Accepted / Rejected | Rationale |
|---|---|---|
| Keep Markdown plus JSON sidecars | Rejected | This preserves Markdown as the real control fact and repeats the prior failure mode. |
| JSON-only facts plus short `/goal` adapter | Accepted | This matches `/goal` as text while keeping control truth structured and machine-checkable. |
| Let Codex infer JSON semantics naturally | Rejected | Runtime needs explicit read-only/writeable boundaries and verifier-backed completion. |
| Long-term dual parser compatibility | Rejected | User explicitly rejected compatibility because it dirties the system and preserves escape paths. |

### Rules That Must Not Change

- Markdown must not be an official guard/compiler/runtime control input in the intended result.
- Approved control JSON must be read-only during runtime.
- Runtime progress must be recorded as JSONL observations or bounded status/report JSON.
- `goal_achieved: true` must require verifier permission.
- Internal registry keys must remain machine bindings, not user-facing proof of understanding.
- The final runtime execution policy must use high-concurrency subagent mode.

## Design Details Tied To Required Steps

Every design detail below must either support a required step or be marked supporting-only. Do not introduce free-floating components, agreements, state, failure handling, evidence, compatibility work, or decisions.

### Components / Mechanisms

| Component / Mechanism | Required answer step supported | Mainline or supporting-only | Responsibility | Inputs | Outputs | Evidence produced |
|---|---|---|---|---|---|---|
| Control JSON schemas | S2 | mainline | Define artifact structure and reject unknown fields | Required semantic fields and current Markdown templates | Schema files | Schema validation results |
| Registry binding model | S3 | mainline | Bind plain approved meaning to internal method/workflow keys | Answer-method and delegation registries | Machine-only registry fields | Registry consistency tests |
| `using-control-json` skill | S4 | mainline | Teach Codex how to operate JSON safely | Runtime JSON and protocol requirements | Skill and protocol references | Skill tests / prompt tests |
| JSON guard | S5 | mainline | Admit or reject official control chains | Run directory JSON and registries | Pass/fail guard result | Guard regression outputs |
| JSON compiler | S6 | mainline | Create runtime JSON and short `/goal` text | Approved JSON chain | `runtime.control.json` and pointer command | Compiler tests |
| Progress event writer | S7 | mainline | Append runtime observations without mutating approved JSON | Runtime action observations | `progress.jsonl` | Progress-event schema tests |
| Verifier | S7 | mainline | Decide whether completion claims are allowed | Control JSON and progress/status/report files | Verification result | Verifier tests |
| Markdown rejection tests | S8 | mainline | Prove hard cut is enforced | Markdown artifact inputs | Expected failures | Failure tests |
| Old accident regression suite | S9 | mainline | Preserve semantic protections after JSON migration | JSON fixtures | Regression pass/fail results | Regression report |

### Interfaces / Agreements

| Interface / agreement | Required answer step supported | Mainline or supporting-only | Why needed | Evidence produced |
|---|---|---|---|---|
| Run directory layout `docs/cybernetics/runs/<slug>/` | S2, S5, S6, S7 | mainline | Gives guard/compiler/runtime one structured input root | Layout tests and fixture run |
| Approved JSON read-only rule | S4, S7 | mainline | Prevents runtime from rewriting goals or plans to match execution | Runtime mutation rejection test |
| Runtime writable file list | S4, S7 | mainline | Gives Codex a safe write limit | Progress/status/final-report tests |
| Verifier-before-achieved agreement | S7, S9 | mainline | Prevents self-certified completion | Verifier bypass regression |
| Short `/goal` adapter agreement | S6 | mainline | Keeps `/goal` within text limit and out of control fact role | Pointer length and content test |

### State Model / Lifecycle

| State / lifecycle item | Required answer step supported | Mainline or supporting-only | Transition or cadence | Evidence produced |
|---|---|---|---|---|
| Requirements JSON | S2, S3 | mainline | drafted -> approved -> read-only | Schema and approval validation |
| Design/goal/plan/review JSON | S2, S5 | mainline | candidate -> reviewed/approved -> read-only | Guard validation |
| Runtime JSON | S6 | mainline | compiled -> validated -> executed | Compiler output and validation |
| Progress JSONL | S7 | mainline | append-only observations | Progress-event validation |
| Final report JSON | S7, S10 | mainline | absent -> verifier-permitted report | Final-report schema and verifier output |

### Error / Failure / Exception Model

| Failure case | Required answer step supported | Mainline or supporting-only | Handling | Evidence produced |
|---|---|---|---|---|
| Markdown official input supplied after migration | S5, S8 | mainline | Fail guard/compiler/runtime path | Rejection test |
| Unknown registry key | S3, S5 | mainline | Fail schema/registry validation | Registry test |
| Runtime mutates approved JSON | S4, S7 | mainline | Fail verifier or runtime protocol validation | Mutation rejection test |
| `goal_achieved: true` without verifier | S7, S9 | mainline | Reject final report | Verifier bypass test |
| JSON sidecar only while Markdown authoritative | S8, S9 | mainline | Reject as invalid migration | Regression fixture |
| High-concurrency workflow conflicts | S10 | supporting-only | Integrate through wave/lock/barrier and stop on conflict | Parallel safety review |

### Evidence / Checks

| Check / evidence | Required answer step supported | Mainline or supporting-only | What it proves | Weak/stale/unobservable handling |
|---|---|---|---|---|
| Schema validation tests | S2 | mainline | JSON structure is strict | Missing schemas block completion |
| Registry validation tests | S3 | mainline | Internal keys are deterministic | Unknown keys block completion |
| Guard JSON tests | S5 | mainline | Official control admission is JSON-owned | Markdown fallback invalidates completion |
| Compiler tests | S6 | mainline | Runtime output is JSON plus short pointer | Long pointer or Markdown contract invalidates completion |
| Skill/protocol tests | S4, S7 | mainline | Runtime agent has safe JSON operation rules | Missing protocol blocks completion |
| Verifier tests | S7 | mainline | Completion claims need deterministic approval | Verifier bypass invalidates completion |
| Old accident regressions | S9 | mainline | Prior failure modes are blocked in JSON | Missing regression is a gap |

### Final Answer Format Design

| Output element | Design |
|---|---|
| Audience | Human operator and downstream maintainer |
| Purpose | Record what changed, what was verified, and whether the JSON-only migration is complete |
| Medium / destination | Chat final answer plus repository artifacts; runtime/control output after migration is JSON |
| Required structure | Changed areas, verification commands/results, runtime pointer path, commit/push status, residual gaps |
| Detail-level split | Standard summary; detailed evidence lives in JSON/progress/test artifacts |
| Evidence-reference rules | Reference key file paths and commands; do not paste long raw outputs |
| Machine-readable shape | Runtime/control artifacts use JSON schemas after migration |
| Acceptance condition | User can run the named checks and see JSON-only official behavior enforced |

### Compatibility / Migration / Integration

| Compatibility / migration / integration item | Required answer step supported | Mainline or supporting-only | Handling | Evidence produced |
|---|---|---|---|---|
| Existing historical Markdown files | S8 | supporting-only | Preserve as history, not official new-chain input | Guard rejection of Markdown official input |
| One-time migration helper | S8 | supporting-only | Allowed only for fixtures/examples, not runtime compatibility | Helper tests if implemented |
| Current tests using Markdown fixtures | S9 | mainline | Rewrite to JSON fixtures or failure fixtures | Updated test suite |
| Delegation registry key mismatch | S3, S5 | mainline | Normalize registry field names used by guard/compiler | Registry compatibility test |

### Design Decisions

| Decision | Required answer step supported | Mainline or supporting-only | Rationale | Risk | Reversible? |
|---|---|---|---|---|---|
| Use JSON as only official control fact | S2-S8 | mainline | Removes Markdown parsing and jargon leakage from control facts | Large migration blast radius | No, by user instruction |
| Keep `/goal` as short text pointer | S6 | mainline | Codex `/goal` is not JSON-native | Runtime still needs adapter text | Yes, if product changes |
| Add runtime JSON operation skill | S4, S7 | mainline | Codex needs explicit JSON interpretation/write rules | New skill must be tested | Yes |
| Use verifier as completion裁判 | S7 | mainline | Prevents runtime self-certification | Requires robust evidence mapping | Yes |
| Use high-concurrency subagent execution for target migration | S10 | mainline | User explicitly required final compiled execution to use subagent high concurrency | Requires wave/lock discipline | Yes, only by new approval |

## Design-to-Goal Mapping

| Design element | Goal implication |
|---|---|
| JSON-only official fact rule | Goal must define success as official guard/compiler/runtime JSON acceptance and Markdown input rejection |
| Read-only approved JSON | Goal must forbid runtime mutation of approved control JSON |
| Progress/verifier model | Goal must require progress JSONL and verifier before `goal_achieved: true` |
| Short `/goal` adapter | Goal must require pointer-only runtime command, not long control prose |
| Old accident regressions | Goal must include regression evidence for prior failure modes |
| High-concurrency target execution | Goal must preserve max-safe-parallel execution in the policy |
| Final Answer Format Design, if present | Goal must preserve the final answer format and forbid runtime substitution. |

## Design-to-Execution Mapping

| Design element | Execution-policy implication |
|---|---|
| Schema set | Assign schema work package and validation evidence |
| JSON operation skill | Assign skill/protocol work package and tests |
| Guard/compiler rewrite | Assign JSON guard/compiler work package with Markdown rejection tests |
| Progress/verifier | Assign runtime verification work package |
| Template/parser removal | Assign hard-cut migration work package |
| Regression suite | Assign old-accident JSON regression work package |
| High-concurrency execution | Plan must select `Parallel subagent-driven`, `superpowers-dispatching-parallel-agents`, `parallel-max-safe`, and `Max concurrent subagents: auto` with wave/lock/barrier controls |
| Final Answer Format Design, if present | Execution policy must collect and preserve the evidence/output material required by the final answer format. |

## Open Design Questions

- None

## Design Review Requirements

Review must check:

- meaning match to requirements analysis;
- answer path starts from JSON-only control facts, not JSON sidecars;
- schema/registry/guard/compiler/runtime/verifier responsibilities are all mapped to required steps;
- Markdown official-input failure is part of completion;
- high-concurrency subagent mode is preserved in the execution policy;
- evidence/check adequacy;
- final-answer-format adequacy;
- rules that must not change versus tactical flexibility;
- suitability as source input for goal and execution policy.
