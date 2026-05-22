# Sensor Governance

Tests are sensors, not objectives.

A sensor should be judged by whether it detects deviation from confirmed semantics, not by whether it existed before.

## Strong sensor

A test/eval/check that directly observes confirmed product semantics.

## Weak or stale sensor

A check that may encode old behavior, implementation details, or outdated assumptions.

## Obsolete sensor

A check that contradicts confirmed semantics or blocks necessary structural change.

## Rule

If a sensor conflicts with confirmed semantics, do not blindly satisfy it. Either replace it with a product-level sensor or stop and ask for a decision if the conflict is semantic.
