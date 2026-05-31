# Sensor Governance

Approved sensors, checks, and evidence channels are sensors, not objectives.

A sensor should be judged by whether it detects deviation from confirmed semantics, not by whether it existed before.

## Strong sensor

A sensor, check, or evidence channel that directly observes confirmed requirement semantics.

## Weak or stale sensor

A check that may encode old behavior, execution details, or outdated assumptions.

## Obsolete sensor

A check that contradicts confirmed semantics or blocks necessary structural change.

## Rule

If a sensor conflicts with confirmed semantics, do not blindly satisfy it. Either replace it with a target-state evidence channel or stop and ask for a decision if the conflict is semantic.

Use the smallest sensor set that can detect semantic or structural drift at each batch gate. Expensive broad checks should usually be deferred to integration or final gates. Do not let sensor cost dominate execution cost.
