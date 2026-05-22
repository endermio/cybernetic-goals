# Batch Cadence

Batch cadence is the control step size.

Too small:

- local minima
- overfitting old tests
- excessive overhead
- structural changes become impossible

Too large:

- failures hard to diagnose
- drift goes unnoticed
- UI or build may be broken too long

Recommended rule:

- intermediate states inside a batch may be broken when necessary;
- batch end must be openable or verifiable;
- every batch should prove a meaningful product slice, not a micro-implementation detail.
