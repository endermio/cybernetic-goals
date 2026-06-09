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

## Semantic Review Loop

Independent subagent review includes an Intent Preservation / Obligation
Preservation pass. Its normalized verdicts are `Approved`, `NeedsRevision`, or
`Blocked`.

`NeedsRevision` is a pre-goal loop result. It routes to the earliest artifact
that introduced drift:

- Requirements drift -> `ReturnToRequirementsAnalysis`
- Design drift -> `RunDesign`
- Goal drift -> `RunGoalWriting`
- Plan drift -> `RunExecutionPolicy`

NeedsRevision routes to the earliest artifact that introduced drift, then
requires re-review before runtime compilation. The rule is: do not compile `runtime.control.json` until the review verdict is `Approved`.

## Non-Negotiable Limit

The runtime `/goal` must not create or approve its own solution design or approved work chain.

The orchestrator may coordinate creation and review of approved files before `/goal`, but it must not start `/goal`.
