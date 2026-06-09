# required design Reference

Use the required design when the task has enough analyzed intent to know what should be achieved, but not enough solution structure to let runtime execution proceed without inventing a model.

## Required

required design is required when any of these are unresolved:

- core objects, actors, roles, or responsibilities;
- relationships among concepts or entities;
- system, process, or organizational limits;
- information flow, state flow, evidence flow, or decision flow;
- interfaces, contracts, reports, procedures, events, or interactions;
- lifecycle, state model, failure model, or exception handling;
- evidence/evidence check model needed to prove the design works;
- replacement of old concepts or old realization assumptions;
- cross-subsystem or cross-role coordination model.

## Satisfied

required design is satisfied when an existing design, spec, requirements analysis, or explicit human instruction already fixes:

- objects/actors/roles;
- relationships;
- flows;
- limits;
- interfaces/contracts;
- failure and evidence model, when relevant.

## Not Applicable

required design is usually not applicable for:

- local bug fixes;
- copy, label, style, fixture, or screenshot updates;
- bounded repairs inside an existing approved approved work chain;
- audits whose rubric and report shape are explicit;
- tasks where the execution path is obvious and does not introduce new abstractions.

## Routing Rule

Keep the routing level separate from checks:

```text
Routing decision: Level N
Required checks:
- required design: required/satisfied/not applicable
```

Do not create routing levels such as `Level 3D`.
