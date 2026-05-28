# Complexity Routing Reference

Route by unresolved control decisions, not by scary keywords.

## Main question

Would the execution agent need to invent or revise any of these during runtime?

- product/domain semantics
- solution structure/design model
- goal or success criteria
- permission/data visibility semantics
- schema/API semantics
- sensor/test governance
- execution policy
- phase gates
- stop conditions

If yes, consider Level 3 or Level 4.

If no, prefer Level 0, 1, or 2.

## Downgrade rule

If approved artifacts or explicit user decisions already fix semantics, and the task is a bounded correction, downgrade even if the task mentions complex concepts.

## Examples

Level 2:
- Fix a misleading corpId display inside an already analyzed supervision feature.
- Update a screenshot assertion after a confirmed UI label change.
- Adjust fixture names so local preview matches existing product semantics.

Level 3:
- Decide what supervision means for the first time.
- Decide pull vs push log acquisition.
- Decide entity mapping and authorization model.
- Decide objects, relationships, boundaries, information flow, or evidence model for a new solution.
- Build a new multi-subsystem feature without approved control artifacts.

Level 4:
- Production-impacting, irreversible, credentialed, regulated, or customer-data tasks.
