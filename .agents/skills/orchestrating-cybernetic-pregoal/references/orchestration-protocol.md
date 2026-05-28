# Orchestration Protocol

This orchestrator is a pre-goal compiler, not a runtime controller.

## Control-Layer Mapping

| Artifact | Control role |
|---|---|
| Requirements analysis brief | Setpoint synthesis: confirmed human semantics |
| Solution design | System/regulator model: objects, relationships, flows, boundaries, interfaces, evidence model |
| Goal contract | Control contract: target, boundaries, sensors, stop conditions |
| Execution policy | Control law: batch cadence, dependency matrix, sensor governance |
| Control review | Meta-control: independent review of the whole control structure |
| Runtime /goal | Execution runtime: closed-loop execution under approved artifacts |

## Non-Negotiable Boundary

The runtime `/goal` must not create or approve its own solution design or control structure.

The orchestrator may coordinate creation and review of control artifacts before `/goal`, but it must not start `/goal`.
