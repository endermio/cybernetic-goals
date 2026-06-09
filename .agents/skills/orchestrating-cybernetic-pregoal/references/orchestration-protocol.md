# Orchestration Protocol

This orchestrator is a pre-goal compiler, not a runtime controller.

## Control-Layer Mapping

| Artifact | Control role |
|---|---|
| Requirements analysis brief | Approved target synthesis: confirmed human meaning |
| Solution design | System/regulator model: objects, relationships, flows, limits, interfaces, evidence model |
| Goal file | Control contract: target, limits, evidence checks, stop conditions |
| Execution policy | Control law: batch cadence, dependency matrix, evidence check governance |
| Review | Meta-control: independent review of the whole approved work chain |
| Runtime /goal | Execution runtime: closed-loop execution under approved artifacts |

## Non-Negotiable Limit

The runtime `/goal` must not create or approve its own solution design or approved work chain.

The orchestrator may coordinate creation and review of approved files before `/goal`, but it must not start `/goal`.
