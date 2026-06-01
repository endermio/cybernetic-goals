# Cybernetic Observability

This directory contains local-first observability artifacts for the cybernetic
skill group.

## Defaults

- Default mode is `metadata_only`.
- Ordinary skill execution may write local events but must not upload.
- Raw prompts, content summaries/excerpts, artifact bodies, code/log excerpts,
  credentials, customer data, real paths, and real repository names are not
  uploaded by default.
- Upload beyond metadata-only requires explicit opt-in, redaction, and manual
  sync configuration.
- Machine identity is pseudonymous, locally generated, and not derived from a
  hostname by default.

## Local Recording

Run events are JSON-compatible records validated against
`observability/schemas/run-event.schema.json`. A minimal safe sample lives at
`observability/examples/metadata-only-event.json`.

The local event lifecycle is:

```text
observed -> recorded -> pending export -> redacted -> pending send -> sent -> aggregated -> candidate reviewed
```

Manual sync must maintain pending/sent state and refuse duplicate real sends
unless an operator explicitly forces a resend.

## Cloud Boundary

Cloud-side aggregation may validate metadata packages, create machine-readable
summaries, and generate reviewable issue or eval candidates. It must not modify
skills, publish releases, or update machines automatically.

The repository workflow scaffold is manual-only. Local non-live aggregation can
be run with:

```bash
python3 scripts/aggregate_run_events.py \
  --input observability/examples/metadata-only-event.json \
  --out observability/examples/aggregation-summary.json \
  --eval-candidates-out observability/examples/eval-candidates.json \
  --dry-run
```

The generated JSON files are process-improvement candidates. They are not
accepted rules.

## Release Boundary

Any skill change still requires review, eval evidence, a release tag or pinned
commit, and explicit installation/update by the operator.
