# Cybernetic Requirements Analysis: Cybernetic Observability Meta-Control

## Requirements Analysis Status

Status: `Complete`

## Human Purpose

Create a higher-level feedback loop for the cybernetic skill group so multi-machine usage can accumulate process evidence, recurring failure patterns, eval candidates, and improvement proposals without allowing the system to automatically rewrite or distribute its own control laws.

## Current Understanding

The requested capability is an observability/meta-control layer for the cybernetic skill pack. It should record local run outcomes, default to metadata-only collection, support redaction, allow manual cloud sync, and enable GitHub-side aggregation/report/issue/eval-candidate generation. It must not automatically modify installed skills, publish releases, or update machines.

## Context Inspected

- User-provided observability/meta-control proposal in chat.
- Current repository structure under `.agents/skills/`, `docs/cybernetics/`, and `scripts/`.
- Existing cybernetic flow: routing, requirements analysis, solution design, goal writing, execution policy, control review, runtime compilation.
- Current branch state: `main` is ahead of `origin/main` by commit `7749664 Tighten granularity review evidence`.

## Requirement Semantics

### Core Terms / Objects / Actors

| Term | Requirement meaning | Notes |
|---|---|---|
| Observability layer | Infrastructure for recording and summarizing cybernetic skill run outcomes | Must remain separate from core task-control skills |
| Meta-control loop | Feedback loop over the quality of the skill group itself | Controls process improvement, not a single runtime task |
| Run event | Local structured metadata record for a skill invocation, routing decision, artifact creation, blocked state, human feedback, or runtime outcome | Default content must avoid sensitive raw task material |
| Local logger | Script or local mechanism that writes run events to a local JSONL store | No network behavior inside ordinary skill execution |
| Redaction | Local process that removes or hashes sensitive fields before upload | Required before any content beyond safe metadata |
| Sync script | Explicit/manual uploader from local pending/sent records to a cloud target | Must not be automatic by default |
| Cloud aggregation | GitHub-side workflow/report process that validates, aggregates, and summarizes uploaded metadata | May generate issues or eval candidates, not skill patches |
| Improvement candidate | Issue, eval candidate, report finding, or patch proposal generated from aggregated evidence | Requires human/independent review before merging |
| Release gate | Human/reviewed PR, eval pass, tag/release, and pinned update path | Prevents automatic self-modification |

### Confirmed Semantics

- The system may automatically observe, summarize, and propose improvements.
- The system must not automatically modify local installed skills.
- The system must not automatically publish cloud-generated suggestions as new releases.
- The system must not automatically update all machines from `main`.
- Local recording is allowed by default only for safe metadata.
- Content summaries, excerpts, prompts, artifact bodies, logs, paths, repo names, credentials, and customer data are not uploaded by default.
- Upload beyond metadata-only requires explicit opt-in and redaction.
- Skill execution should write local events only; network sync belongs to scripts or CI, not ordinary skill behavior.
- Cloud automation may aggregate evidence, create issues, generate eval candidates, and propose patches.
- Control-law changes must go through review, PR/eval, release tagging, and versioned distribution.
- Multi-machine events must record skill pack version or source commit so failures can be attributed to versions.
- Observability is adjacent infrastructure, not a domain adapter and not a required gate for every ordinary cybernetic task.

### Boundaries

Inside scope:

- A new local requirements/design/goal path for observability infrastructure.
- A domain-neutral run-event schema for metadata-only local records.
- A failure taxonomy for process-improvement classification.
- A local JSONL run-event logger.
- A redaction helper for metadata and optional content.
- A manual sync script for metadata-only upload.
- GitHub-side aggregation/report/issue/eval-candidate workflow or workflow-ready structure.
- A new `recording-cybernetic-run-outcomes` skill that records local run outcomes and does not upload.
- Documentation for privacy defaults, opt-in modes, local storage, sync behavior, and release boundaries.

Outside scope:

- Automatic modification of `.agents/skills/*/SKILL.md`.
- Automatic release publishing.
- Automatic multi-machine update.
- Default upload of raw prompts, code, logs, artifact bodies, credentials, real repo names, real paths, customer data, or other sensitive content.
- Requiring every core cybernetic skill to perform network operations.
- Building a full dashboard product beyond minimal reports/artifacts.
- Introducing domain-adapter-specific telemetry as part of the core observability MVP.

## Requirements Control Map

| Control element | Current analysis |
|---|---|
| Objective | Add a local-first, metadata-only-by-default observability feedback loop that records cybernetic run outcomes and supports reviewed process improvement. |
| Controlled object | The cybernetic skill group's improvement process across local machines and optional cloud aggregation. |
| Candidate sensors | Local JSONL run events, schema validation, redaction checks, sync dry-run output, aggregation reports, generated issues/eval candidates, version metadata. |
| Candidate actuators | New skill `recording-cybernetic-run-outcomes`, scripts under `scripts/`, observability schemas/taxonomies/docs, optional GitHub workflow and issue templates. |
| Constraints | No default sensitive upload; no auto self-modification; no auto release; no auto machine update; local-first; manual sync; versioned distribution. |
| Disturbances | Privacy leakage, token misuse, noisy issue creation, inconsistent version attribution, taxonomy drift, accidental upload of raw artifacts, over-collection. |
| Stop conditions | Stop if sync would upload non-redacted content by default; stop if token/repo config is missing for real upload; stop if a generated improvement would modify skills without review; stop if schema/redaction validation fails. |

## Blocking Human Decisions

| Decision | Why it matters | Recommended default | Risk if wrong |
|---|---|---|---|
| None blocking for MVP requirements | The proposal already defines conservative privacy and release boundaries | Proceed with metadata-only local recording and manual sync design | Low; later design can ask for specific repo/token choices before live upload |

## Default Assumptions

These are reasonable defaults and should not block progress unless the human disagrees.

- Local run store defaults to a user-local state directory and does not require network access.
- Default telemetry mode is `metadata_only`.
- Upload of prompts, artifact bodies, logs, paths, repo names, and code is disabled.
- Manual sync supports dry-run and explicit destination configuration.
- GitHub issue creation is opt-in and aggregate-pattern based, not one issue per failure.
- Cloud aggregation output is process-improvement evidence, not an automatically applied patch.
- Version identity uses git commit SHA when a release tag is absent.
- Machine identity is pseudonymous, generated locally, and not derived from hostname by default.
- Failure taxonomy starts small and can evolve through reviewed changes.

## Evaluation Rubric / Error Function

This task is not primarily an audit/status-classification task. The MVP success criteria should be captured in the goal contract, not as an open-ended evaluation rubric.

| Rubric element | Confirmed meaning |
|---|---|
| Status meanings / pass-fail categories | Not applicable for requirements analysis. |
| Evidence levels / evidence strength | Not applicable beyond goal-time verification evidence. |
| Minimum evidence for strongest positive status | Not applicable. |
| Downgrade rules | Not applicable. |
| External/unobservable dependency handling | Real GitHub upload may be unobservable without token/config and should be treated as optional or dry-run unless explicitly enabled. |
| Confidence / evidence grade | Not required. |

## Output Contract

| Element | Requirement |
|---|---|
| Audience | Maintainer, future Codex agents, reviewers, and optional GitHub aggregation workflow. |
| Purpose | Execution handoff, process-improvement record, metadata validation, aggregation, issue/eval candidate generation. |
| Medium | Requirements markdown now; later artifacts should include JSON schema, YAML taxonomy, markdown docs/report templates, JSONL event records, and optional workflow artifacts. |
| Required structure | Requirements brief must identify event classes, privacy boundaries, sync/release boundaries, required gates, and deferred design questions. Exact JSON schema/report/issue structures are deferred to solution design. |
| Detail level | Standard; enough to support design and goal writing without fixing implementation tactics. |
| Evidence references required | Yes, for later implementation verification and cloud aggregation outputs. |
| Machine-readable required | Yes, for run events, schema validation, taxonomy, sync payloads, and aggregation summaries. |
| Destination path | This brief: `docs/cybernetics/requirements/2026-06-01-cybernetic-observability-meta-control.md`. Later paths deferred to design. |
| Acceptance condition | A goal/design writer can preserve privacy/release invariants and produce a solution model without inventing sensitive data policy or auto-update behavior. |

## Required Gates

| Gate | Status | Reason |
|---|---|---|
| Semantic Gate | `satisfied` | Human has clearly defined the core purpose and hard boundaries: observe/summarize/propose, never auto-modify/release/update. |
| Rubric Gate | `not applicable` | This is not primarily a status-classification/audit task. |
| Output Contract Gate | `required` | Event schema, redacted report shape, issue/eval candidate shape, and aggregation output are essential to usability and downstream automation. |
| Design Gate | `required` | Local/cloud boundaries, event lifecycle, schema/taxonomy relationships, redaction flow, sync flow, CI aggregation, and release gate need a solution model. |
| Goal Contract Gate | `required` | The privacy, no-self-modification, and release invariants must be fixed before execution. |
| Execution Policy Gate | `required` | Implementation spans skills, scripts, schemas, optional workflows, tests, and docs. |
| Control Review Gate | `required` | The control structure must be reviewed for privacy, self-modification, upload, and release-boundary correctness. |
| Risk Gate | `required` | Network sync, tokens, issue creation, and data retention create privacy/security risks even when disabled by default. |

## Deferred Solution Design Questions

These belong in `$designing-cybernetic-solutions`, not requirements analysis.

- What is the exact local event store layout and lifecycle?
- What is the exact `run-event.schema.json` structure?
- How are the six event classes normalized into one schema or multiple event schemas?
- How should the failure taxonomy be represented and versioned?
- How should redaction determine safe metadata versus opt-in content?
- What exact CLI contracts should logger, redactor, and sync scripts expose?
- What is the exact GitHub aggregation workflow shape and artifact retention model?
- What issue body/report/eval-candidate templates should aggregation produce?
- How should version identity and adapter identity be represented in events?
- How should pending/sent state and sync idempotency work?

## Deferred Planning / Execution Details

- File creation order and batch boundaries.
- Exact validation commands.
- Whether GitHub workflow is implemented in MVP or scaffolded with docs.
- Whether sync script uses GitHub REST directly, `gh`, or a dry-run/file-export mode first.
- How to test issue creation without a live token.
- How to fixture redaction and schema-validation tests.
- Whether to add sample anonymized run events.

## Questions for Human

No blocking questions for requirements analysis. The conservative defaults below are safe enough to proceed to solution design.

## Proposed Defaults

If the human says “按默认继续”, proceed with:

- Local-first, metadata-only event recording.
- No default content upload.
- Manual sync only.
- GitHub issue creation disabled unless explicitly configured.
- Separate observability namespace/directory in the repo.
- Cloud-generated outputs are improvement candidates, not accepted changes.
- Skill changes require PR/review/eval/release.
- Machine updates must use pinned releases, not automatic `main`.

## Confirmed Requirement Decisions

- Build observability as a meta-control loop over the cybernetic skill group.
- Add a new skill for local outcome recording.
- Keep upload/sync behavior outside ordinary skill execution.
- Default to metadata-only collection.
- Require redaction and opt-in for content summaries/excerpts.
- Forbid default upload of raw prompts, code, logs, artifact bodies, credentials, real paths, and real repo names.
- Forbid automatic skill modification.
- Forbid automatic release publishing.
- Forbid automatic multi-machine update.
- Use reviewed, versioned releases for distribution.
- Record skill pack version/source commit in events.

## Non-Goals

- No automatic self-modification of core skills.
- No automatic publish/release.
- No automatic update across machines.
- No default sensitive content upload.
- No requirement that every cybernetic skill directly implements network sync.
- No full cloud dashboard in the first pass.
- No domain-specific adapter telemetry in the core MVP unless explicitly added later.

## Candidate Sensors / Evidence Needs

- Schema validation succeeds for sample metadata-only run events.
- Logger writes JSONL locally without network access.
- Redactor removes or hashes path/repo/content-like fields according to defaults.
- Sync script can dry-run and report what would be uploaded.
- Sync script refuses real upload without explicit config/token/destination.
- Aggregation workflow or scaffold validates event schema and produces a summary artifact.
- Generated issue/eval-candidate examples are aggregate-pattern based, not one failure per issue.
- Tests or fixtures show raw prompt/artifact body upload is disabled by default.
- Documentation states privacy defaults and release-gate rules.
