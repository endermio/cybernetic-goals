---
name: recording-cybernetic-run-outcomes
description: 'Use after a cybernetic skill invocation, artifact creation, blocked state, human feedback, or runtime outcome when the operator wants to record local process evidence. Produces metadata-only local run-event records using repository observability scripts. Does not upload, sync, modify skills, publish releases, update machines, or accept cloud improvement candidates.'
---

# Recording Cybernetic Run Outcomes

## Overview

Record local process evidence for the cybernetic skill group.

This skill converts a completed local outcome into one or more metadata-only run
events. It is an observability helper, not a task-control gate.

Primary output:

```text
local JSONL event store
```

Use `assets/run-outcome-template.md` when a human-readable summary is needed
before event recording.

## Core Boundary

This skill must not:

- upload or sync events;
- create GitHub issues;
- modify installed or repository skill files;
- publish releases;
- update machines;
- accept, merge, or apply improvement candidates;
- record raw prompts, content summaries/excerpts, artifact bodies, code/log excerpts, credentials, customer data, real paths, or real repository names by default;
- turn observability into a required gate for ordinary cybernetic tasks.

This skill may:

- inspect the current run outcome and existing control artifacts;
- classify the event type and optional failure-taxonomy codes;
- write metadata-only local events through `scripts/record_run_event.py`;
- validate local event files through `scripts/validate_run_events.py`;
- recommend manual redaction/sync as a response-only follow-up when the operator explicitly asks for upload.

## Event Types

Use one of:

- `skill_invoked`
- `route_decided`
- `artifact_created`
- `blocked`
- `human_feedback`
- `runtime_outcome`

## Safe Metadata

Allowed by default:

- event id
- timestamp
- event type
- privacy mode
- pseudonymous machine id
- skill pack release or source commit
- skill name
- task hash
- status/outcome
- taxonomy codes
- artifact type
- hashed path or hashed repository id when explicitly produced by script

Forbidden by default:

- raw prompt
- content summary or excerpt
- artifact body
- code/log excerpt
- credential, token, or secret
- customer data
- real path
- real repository name
- hostname-derived machine id

## Process

1. Identify the local outcome being recorded.
2. Choose the event type and status.
3. Add a taxonomy code only when it is clear from
   `observability/taxonomies/failure-taxonomy.yaml`.
4. Use metadata-only fields only.
5. Record locally with:

```bash
python3 scripts/record_run_event.py --event <event> --status <status> --skill <skill> --dry-run
```

6. For persistent local recording, remove `--dry-run` or pass `--output <local-jsonl>`.
7. Validate local event files with:

```bash
python3 scripts/validate_run_events.py --taxonomy observability/taxonomies/failure-taxonomy.yaml <event-file>
```

## Upload Boundary

This skill does not upload.

If the operator asks to upload or sync:

- first run redaction explicitly;
- use manual sync scripts, not this skill;
- keep real upload disabled unless destination and token configuration are explicit;
- never upload content summaries/excerpts or raw artifacts in metadata-only mode.

## Improvement Candidate Boundary

Reports, issues, eval candidates, and patch proposals generated from run events
are candidates only. They do not modify the control law until reviewed through
the repository's normal review/eval/release process.

## Output Format

This output format is response-only. Do not write conversational next-step
prompts into run-event records.

```markdown
Recorded cybernetic run outcome locally.

Event:
- type: ...
- status: ...
- taxonomy codes: ...
- privacy mode: metadata_only

Evidence:
- local event path or dry-run output
- validation command/result
```

If blocked:

```markdown
Run outcome recording blocked.

Reason:
- ...

No upload was performed.
No skill files were modified.
```

## Validation Checklist

- [ ] Event type is one of the approved values.
- [ ] Record is metadata-only by default.
- [ ] No raw prompt, content summary/excerpt, artifact body, credential, real path, real repository name, or hostname-derived machine id is recorded.
- [ ] No upload or sync is performed by this skill.
- [ ] No skill modification, release publication, or machine update is performed.
- [ ] Any improvement output remains a candidate.
