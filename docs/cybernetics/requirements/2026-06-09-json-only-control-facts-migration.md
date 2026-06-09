# Requirements: JSON-only Control Facts Migration

## Requirements Analysis Status

Status: `Complete`

## What the User Approved

Status: `Approved`

Allowed values: `Pending / Approved / Rejected / Needs Revision / Not required`

Approval applies only to this compact control commitment.

| Element | Commitment |
|---|---|
| Human purpose | Replace the Markdown-based cybernetic control chain with a structured control system that is harder for Codex to reinterpret, pollute with jargon, or falsely mark complete. |
| Input role binding | Source material: routing/framing conclusions and the JSON-only intended-result list. Declared current state: current skills still use Markdown control artifacts and Markdown parsers. Requested transformation: turn the intended result into approved requirements for a JSON-only migration. Method preference: hard cut, no long-term Markdown/JSON compatibility. |
| Primary object | The cybernetic control-chain artifact model and runtime execution protocol in this repository. |
| Requested transformation | Migrate official control facts from Markdown artifacts to JSON control files, with schemas, registry checks, runtime JSON operation rules, progress JSONL, and verifier-controlled completion claims. |
| Non-goals | Do not keep Markdown as an official guard/compiler/runtime input. Do not maintain a long-term dual Markdown/JSON control chain. Do not rely on Codex naturally understanding JSON without an explicit runtime JSON operation protocol. Do not let runtime edit approved control JSON. |
| How we know the user's purpose was met | A fresh JSON-only chain can be created, validated, compiled to a short `/goal` pointer, executed through a JSON operation skill, recorded through progress events, and verified without any official guard/compiler/runtime step reading Markdown control artifacts. |
| Where the result must show up | Skill instructions, schemas, builders or examples, guard scripts, compiler, runtime operation skill, verifier scripts, tests/evals, manifest, and rule table must all reflect JSON as the official control fact source. |
| What counts as done | Official guard/compiler/runtime paths accept JSON control files and reject Markdown control artifacts as control inputs; approved JSON remains read-only during runtime; progress is recorded as JSONL events; verifier output is required before `goal_achieved: true`; old accident regressions pass against JSON. |
| Evidence needed to call it done | Passing schema validation tests, guard tests, compiler tests, runtime JSON operation skill tests, verifier tests, old-accident regression tests, and a generated short `/goal` pointing to `runtime.control.json`. |
| If it is not done, what should be reported | Report `goal_achieved: false`, the JSON migration stage reached, which official paths still read Markdown or lack verifier coverage, and the smallest next migration step. |
| Required answer path | Inventory current Markdown control inputs -> define JSON control schema set -> define registry mapping -> add JSON operation skill -> make guards consume JSON -> make compiler consume JSON and emit short `/goal` pointer -> make runtime write progress events only -> add verifier-controlled completion -> remove or fail official Markdown control inputs -> run JSON regressions. |
| How this should be answered | By implementing a structured control migration: schema-first JSON control facts, explicit runtime JSON interpretation protocol, read-only approved chain, writable progress/status/report files, verifier-backed completion, and tests for previous failure modes. |
| What is not enough | Merely adding JSON sidecars while Markdown remains the official source, or pointing `/goal` at JSON without defining how Codex must read, update, and verify the JSON. |
| Work covered in this run | The full repository migration needed to make JSON the official control fact carrier for cybernetic requirements/design/goal/plan/review/runtime/progress. Existing historical Markdown files may remain as history, but not as official new-chain inputs. |
| What the agent may do | Create and edit skills, schemas, builders/examples, guard scripts, compiler scripts, verifier scripts, tests/evals, manifest, and framework docs. Delete or replace Markdown control templates when the JSON path is ready. |
| Forbidden live / irreversible actions | No external production or live-state changes. Do not delete unrelated repository history or unrelated docs. Do not push destructive branch changes outside normal git commits. |
| Required handling for unauthorized actions | If a requested action would touch external/live systems or unrelated history, record it as forbidden-not-executed and continue with local repository migration work. |
| Explicitly out-of-scope items | Rewriting unrelated observability docs, changing Codex product behavior, or implementing target-work tasks outside the cybernetic control-chain migration. |
| Agent delegation preference | no preference |
| Agent workflow preference | no preference |
| Parallel execution authority | not approved |
| Maximum parallel agents | not specified |
| Final answer format | Chat summary with changed files, verification commands, commit/push status, and any remaining JSON-only migration gaps. Machine-readable runtime output must use JSON files defined by the new schemas. |
| Why this process is needed | This is a Level 3 architecture migration across multiple skills, artifacts, guards, compiler, runtime protocol, and tests. Runtime Codex would otherwise invent JSON semantics or preserve Markdown compatibility. |
| Known assumptions | The existing Markdown chain may be used only as current-system input while migrating; target behavior is JSON-only for official guard/compiler/runtime control. `/goal` remains a short text pointer and is not JSON-native. |

Approval record:

- Approved by: `human`
- Approval phrase or source: `批准这个 What the User Approved,给出orchestration的推荐prompt`
- Approval time/context: `2026-06-09 current chat message`

If Status is not `Approved`, downstream full pre-goal orchestration must not start.

## Human Purpose

The user wants the cybernetic control system to stop using Markdown as its control database. The purpose is to reduce repeated failures caused by natural-language reinterpretation, jargon pollution, fragile section parsing, and runtime self-certification.

## Current Understanding

The formed task is a destructive but local repository migration from Markdown control artifacts to JSON control facts. Chat remains the human confirmation interface. JSON becomes the only official control fact. Registries carry internal method/workflow keys. Guards validate JSON schema and registry consistency. Runtime uses a dedicated JSON operation skill and records JSONL progress. A verifier decides whether completion claims are allowed. `/goal` remains a short text entry point that points to JSON and invokes the JSON operation protocol.

## Context Inspected

- `.agents/skills/analyzing-cybernetic-requirements/assets/requirements-analysis-template.md`
- `.agents/skills/references/answer-method-registry.json`
- Current branch: `json-control-contracts`
- User-provided routing and intended-result text
- Codex manual fact already established in chat: `/goal` is a short text objective, not a JSON-native contract interpreter.

## Requirement Meaning

### Core Terms / Objects / Actors

| Term | Requirement meaning | Notes |
|---|---|---|
| Chat | Human confirmation place only. | It should show compact summaries, not persist control facts. |
| Control JSON | The only official persistent control fact. | Guards/compiler/runtime must read this, not Markdown. |
| Registry | Internal key table for answer methods and agent workflows. | User-facing artifacts should not expose internal labels. |
| Guard | Deterministic JSON schema and cross-file consistency checker. | No Markdown heading regex on official path. |
| Runtime JSON operation skill | Skill that tells Codex how to read/write/verify control JSON. | Needed because `/goal` is text and Codex is not a JSON runtime. |
| Progress JSONL | Append-only runtime observations. | Codex writes observations, not approved control mutations. |
| Verifier | Deterministic completion-claim checker. | It decides whether progress satisfies the contract. |
| Markdown | Documentation or historical material only. | Not an official new-chain control input. |

### Confirmed Meaning

- JSON is the source of truth for control facts.
- `/goal` remains a short text pointer and adapter, not a full control contract.
- Runtime must not edit approved requirements/design/goal/plan/review/runtime JSON.
- Progress is append-only JSONL plus bounded status/final-report JSON.
- `goal_achieved: true` requires verifier approval.
- Markdown compatibility should not be retained as a long-term official path.

### Inside / Outside

Inside scope:

- JSON schemas for all control artifacts.
- JSON operation skill.
- Guard rewrite to JSON schema and registry checks.
- Runtime compiler rewrite to JSON inputs and short `/goal` output.
- Runtime progress and verifier scripts.
- Tests/evals for old accident paths.
- Removal or failure of official Markdown control inputs.

Outside scope:

- External production deployment.
- Rewriting unrelated repository docs.
- Changing Codex product behavior.
- Making `/goal` JSON-native.

## Requirements Control Map

| Control element | Current analysis |
|---|---|
| Objective | Make JSON the only official control fact carrier for the cybernetic control chain. |
| Controlled object | Cybernetic skills, artifact model, guard/compiler/runtime scripts, tests, and run artifact layout. |
| Candidate checks | JSON schema tests, registry mapping tests, guard failure tests for Markdown input, compiler pointer tests, verifier completion tests, old accident regressions. |
| Candidate actuators | Skill files, schema files, guard/compiler scripts, verifier scripts, runtime prompt builder, tests/evals, manifest, rule table. |
| Constraints | No long-term dual Markdown/JSON control chain; approved JSON read-only at runtime; `/goal` short text pointer only. |
| Disturbances | Existing Markdown-oriented skills, section parsers, templates, evals, and tests; Codex tendency to infer JSON meaning without protocol. |
| Stop conditions | Stop before orchestration if this compact commitment is not approved; stop during migration if JSON schema/registry/verifier semantics become ambiguous. |

## How We Know The User's Purpose Was Met

| Element | Value |
|---|---|
| Human purpose | Stop repeated control-chain failures caused by Markdown, jargon, and agent reinterpretation. |
| Beneficiary / observer | Repository operator and downstream Codex runtime agent. |
| Purpose-realizing outcome | New official cybernetic control runs are JSON-backed and verifier-governed, with no Markdown control input in guard/compiler/runtime. |
| Feedback needed | Tests showing JSON path succeeds, Markdown official inputs fail, verifier controls completion claims, and old accident regressions are blocked. |
| Internal checks role | Internal checks are strong evidence for this repository-level control migration, because the purpose is process/control correctness. |
| Sufficient evidence level | `integration` |
| If feedback unavailable | Report which official path still uses Markdown or lacks verifier coverage, and the smallest next migration step. |

## Where The Result Must Show Up

| Element | Value |
|---|---|
| Intended result | Official control fact carrier changes from Markdown to JSON. |
| Places the result must appear | Skill instructions, schema files, run directory layout, guard/compiler/verifier scripts, runtime JSON operation skill, tests/evals, manifest, rule table, and runtime `/goal` pointer shape. |
| Required action | change / inspect / preserve / exclude |
| Old behavior check | Confirm official guard/compiler/runtime fail or refuse Markdown control artifacts after migration; historical Markdown docs may remain non-authoritative. |
| Result placement status | `partial` |
| Distinction from user-purpose evidence | Result placement checks where the JSON-only rule appears; user-purpose evidence checks whether it actually prevents the prior failure modes. |

## Blocking Human Decisions

| Decision | Why it matters | Recommended default | Risk if wrong |
|---|---|---|---|
| None | The user already specified hard cut, JSON-only control facts, no long-term Markdown compatibility, and verifier-controlled completion. | Proceed with these commitments pending explicit approval. | N/A |

## Default Assumptions

These are reasonable defaults and should not block progress unless the human disagrees.

- Use `docs/cybernetics/runs/<slug>/` as the run artifact layout.
- Use `*.control.json` for approved control files.
- Use `progress.jsonl`, `runtime-status.json`, and `final-report.json` as the runtime writable files.
- Use `additionalProperties: false` in schemas.
- Keep historical Markdown only as historical documentation, not official control input.
- Use a one-time migration helper only for tests/examples, not as runtime compatibility.

## Evaluation Rubric / Error Function

| Rubric element | Confirmed meaning |
|---|---|
| Status meanings / pass-fail categories | `JSON-only complete`, `partial migration`, `blocked`, `invalid`. |
| Evidence levels / evidence strength | Strong: guard/compiler/runtime/verifier all operate on JSON and reject Markdown official input. Weak: JSON sidecars exist but Markdown still drives control. |
| Minimum evidence for strongest positive status | Schema tests, guard JSON tests, compiler JSON tests, runtime JSON skill tests, verifier tests, and old accident regressions pass. |
| Downgrade rules | If Markdown remains accepted by official guard/compiler/runtime, status is partial or invalid. If verifier can be bypassed for `goal_achieved: true`, status is invalid. If JSON exists only as sidecar while Markdown stays authoritative, status is invalid for JSON-only. |
| External/unobservable dependency handling | No external production dependency expected. Codex `/goal` JSON-native behavior is not assumed. |
| Confidence / evidence grade | Final report should state verification commands and residual gaps. |

## Final Answer Format

| Element | Requirement |
|---|---|
| Audience | human operator and downstream agent maintainer |
| Purpose | execution and record |
| Medium | chat summary plus committed repository artifacts |
| Required structure | changed areas, verification commands, commit/push status, remaining gaps |
| Detail level | standard |
| Evidence references required | yes |
| Machine-readable required | yes, for runtime/control artifacts after migration |
| Destination path | repository files under `.agents/skills`, `schemas` or skill-local schemas, `docs/cybernetics/runs`, tests, and scripts |
| Acceptance condition | The user can run guard/compiler/verifier tests and see JSON-only control behavior enforced. |

## Required Checks Before Moving On

| Check | Status | Reason |
|---|---|---|
| Meaning check | `satisfied` | The migration target and non-goals are explicit. |
| Rubric check | `satisfied` | JSON-only pass/fail and downgrade rules are defined. |
| Final answer format check | `satisfied` | Output and runtime artifact shapes are identified at requirements level. |
| Design check | `required` | Schema boundaries, runtime protocol, verifier architecture, and migration sequencing need design. |
| Goal check | `required` | A full Goal is needed after design. |
| Execution plan check | `required` | Multiple repository subsystems must be changed in coordinated batches. |
| Review check | `required` | The chain must be independently checked before runtime compile. |
| Risk check | `required` | Hard-cut migration can break existing workflow tests and needs explicit failure policy. |

## Deferred Solution Design Questions

These belong in the solution design step, not requirements analysis.

- Exact JSON schema structure and shared definitions.
- Whether schemas live at repo root `schemas/` or under the JSON operation skill.
- Exact `using-control-json` skill name and directory.
- Exact verifier script interfaces and final-report schema.
- Exact builder interfaces for requirements/design/goal/plan/review JSON.
- Exact deletion order for Markdown templates and parsers.

## Deferred Planning / Execution Details

These should be handled later in goal writing, execution-policy writing, or execution.

- Batch ordering.
- Test file split.
- Whether to use subagents.
- Exact migration helper implementation.
- Commit cadence.

## Questions for Human

No blocking requirements questions.

## Proposed Defaults

If the human says "approve", proceed with:

- Run artifact layout: `docs/cybernetics/runs/<slug>/`.
- Skill name: `using-control-json`.
- Approved control files are read-only at runtime.
- Runtime writable files are `progress.jsonl`, `runtime-status.json`, and `final-report.json`.
- Official Markdown control inputs fail after the JSON path is implemented.
- One-time migration helper is allowed for tests/examples only.

## Confirmed Requirement Decisions

Record confirmed requirement decisions here.

- JSON is the only official control fact carrier in the target state.
- Chat is the user confirmation interface.
- `/goal` is a short text entry point pointing to JSON and invoking the JSON operation protocol.
- Markdown is not part of the official control chain after migration.
- Verifier output is required before completion can be claimed.

## Non-Goals

- Do not keep long-term Markdown compatibility.
- Do not use Markdown as an official guard/compiler/runtime input after migration.
- Do not let Codex modify approved control JSON at runtime.
- Do not rely on natural language JSON interpretation without a skill/protocol.
- Do not implement unrelated target-work tasks.

## Candidate Evidence checks / Evidence Needs

- JSON schemas reject missing required fields and unknown properties.
- Guard rejects Markdown official inputs.
- Guard accepts valid JSON control chain.
- Guard rejects unknown answer-method or workflow registry keys.
- Compiler reads JSON and emits `runtime.control.json` plus short `/goal`.
- Runtime JSON operation skill documents read-only and writable files.
- Progress verifier rejects missing evidence, supporting-only progress, skipped verifier, and forbidden not-enough substitutes.
- Previous accident regressions are rewritten against JSON and pass.
