# Batch Cadence

Batch cadence is the control step size.

Too small:

- local minima
- overfitting old evidence checks
- excessive overhead
- structural changes become impossible

Too large:

- failures hard to diagnose
- drift goes unnoticed
- local observability or artifact consistency may be broken too long

Recommended rule:

- choose the largest coherent batch that remains diagnosable;
- intermediate states inside a batch may be broken when necessary;
- batch end must be openable or verifiable;
- every batch should prove a meaningful intended-result slice, not a micro execution detail.
- broad verification belongs at integration or final gates unless it is the only reliable drift evidence check.
