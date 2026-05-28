# Design Gate Reference

Use the Design Gate when the task has enough analyzed intent to know what should be achieved, but not enough solution structure to let runtime execution proceed without inventing a model.

## Required

Design Gate is required when any of these are unresolved:

- core objects, actors, roles, or responsibilities;
- relationships among concepts or entities;
- system, process, or organizational boundaries;
- information flow, state flow, evidence flow, or decision flow;
- interfaces, contracts, reports, procedures, events, or interactions;
- lifecycle, state model, failure model, or exception handling;
- evidence/sensor model needed to prove the design works;
- replacement of old concepts or old implementation assumptions;
- cross-subsystem or cross-role coordination model.

## Satisfied

Design Gate is satisfied when an existing design, spec, requirements analysis, or explicit human instruction already fixes:

- objects/actors/roles;
- relationships;
- flows;
- boundaries;
- interfaces/contracts;
- failure and evidence model, when relevant.

## Not Applicable

Design Gate is usually not applicable for:

- local bug fixes;
- copy, label, style, fixture, or screenshot updates;
- bounded repairs inside an existing approved control structure;
- audits whose rubric and report shape are explicit;
- tasks where the execution path is obvious and does not introduce new abstractions.

## Routing Rule

Keep the routing level separate from gates:

```text
Routing decision: Level N
Required gates:
- Design Gate: required/satisfied/not applicable
```

Do not create routing levels such as `Level 3D`.
