import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

USER_APPROVAL_FIXTURE = """## What the User Approved

Status: `Approved`

| Element | Commitment |
|---|---|
| Human purpose | keep context work assignment guard fixtures focused on work assignment behavior |
| Input role binding | test fixture source material is approved background |
| Primary object | context work assignment guard fixture |
| Requested transformation | approved control chain to work assignment guard checks |
| Non-goals | do not test What the User Approved behavior in this fixture |
| How We Know The User Purpose Was Met | covered by dedicated user-purpose evidence tests |
| Where The Result Must Show Up | covered by dedicated result placement tests |
| What counts as done | context-work assignment guard fixture is structurally ready |
| Evidence needed to call it done | evidence needed to call it done is observed |
| Non-achieved terminal report handling | report goal achieved: no |
| Required answer path | context work assignment guard fixture required answer path |
| Work covered in this run | context work assignment guard fixture horizon |
| What the agent may do | local guard fixture checks |
| Forbidden live / irreversible actions | none |
| Required handling for unauthorized actions | none |
| Explicitly out-of-scope items | none |
| Agent delegation preference | no preference |
| Agent workflow preference | no preference |
| Parallel execution authority | not applicable |
| Maximum parallel agents | not specified |
| Final Answer Format | guard output |
| Why this process is needed | full pre-goal guard fixture |
| Known assumptions | fixture-only assumptions |

Approval record:

- Approved by: `test fixture`
- Approval phrase or source: `approved fixture approved target`
"""


class ContextWorkAssignmentSkillTest(unittest.TestCase):
    def complete_serial_work_assignment(
        self,
        delegation_workflow: str | None = None,
        *,
        selected_agent_workflow: str | None = "bounded-protocol",
        include_concurrency_policy: bool = True,
    ) -> str:
        workflow = delegation_workflow or "Approved bounded subagent delegation protocol for serial bounded work packages."
        selected_workflow_lines = []
        if selected_agent_workflow is not None:
            selected_workflow_lines = [
                f"Selected agent workflow: `{selected_agent_workflow}`",
                "",
            ]
        concurrency_lines = []
        if include_concurrency_policy:
            concurrency_lines = [
                "Subagent execution mode: `serial-single-active`",
                "",
                "Max concurrent subagents: `1`",
                "",
                "Concurrency selection rationale:",
                "",
                "- Serial execution keeps dependent work packages integrated one at a time.",
                "",
                "Ordered work package sequence:",
                "",
                "- Package A",
                "",
                "Integration check after each package:",
                "",
                "- Main agent integrates Package A before launching any next package.",
                "",
            ]
        return "\n".join(
            [
                "Who does the work: `Serial subagent-driven`",
                "",
                "Task level: `Level 3`",
                "",
                *selected_workflow_lines,
                *concurrency_lines,
                "Work Assignment rationale:",
                "",
                "- Level 3 context load needs bounded delegation.",
                "",
                "Main agent owns:",
                "",
                "- approved control artifacts",
                "- dispatch",
                "- integration",
                "- progress log",
                "- stop-condition detection",
                "",
                "Delegation matrix:",
                "",
                "| Work package | Executor | Context pack | Allowed actions | Return format | Integration check |",
                "|---|---|---|---|---|---|",
                "| Package A | serial subagent | requirements, goal, plan | inspect files | findings and evidence | main integrates result |",
                "",
                "Context Pack Requirements:",
                "",
                "| Field | Content |",
                "|---|---|",
                "| Relevant control excerpts | requirements success conditions, goal rules that cannot change, execution policy stop conditions |",
                "| Current batch objective | complete Package A bounded inspection |",
                "| Allowed artifacts/places | target files listed in package scope |",
                "| Forbidden changes | control artifacts, scope, work assignment, unrelated files |",
                "| Required evidence checks/evidence | command output and evidence references |",
                "| Stop conditions | missing context, invariant conflict, unauthorized scope change |",
                "| Expected return format | summary, files inspected, evidence, blockers, next integration note |",
                "",
                "Subagent workflow:",
                "",
                f"- {workflow}",
                "",
                "Context Compression Rule:",
                "",
                "- Active control summary: summarize current requirements, goal rules that cannot change, work assignment, and stop conditions.",
                "- Completed work packages: record packages integrated at the limit.",
                "- Subagent outputs integrated: record candidate outputs accepted into main progress state.",
                "- Evidence produced: record evidence references and evidence check interpretation.",
                "- Deferred evidence checks and reasons: preserve policy-approved deferrals.",
                "- Unresolved blockers: record blockers requiring revision or human input.",
                "- Deviations from policy: record deviations and whether execution must stop.",
                "- Next allowed action: record the next policy-approved action.",
            ]
        )

    def complete_parallel_work_assignment(
        self,
        *,
        selected_agent_workflow: str = "bounded-protocol",
        delegation_workflow: str | None = None,
        human_approval: str = "yes",
        dependency_independence: str = "yes",
        control_review_approval: str = "yes",
        include_concurrency_policy: bool = True,
    ) -> str:
        workflow_note = delegation_workflow or "Approved bounded subagent delegation protocol for parallel bounded work packages."
        concurrency_lines = []
        if include_concurrency_policy:
            concurrency_lines = [
                "Subagent execution mode: `parallel-max-safe`",
                "",
                "Max concurrent subagents: `auto`",
                "",
                "Concurrency selection rationale:",
                "",
                "- Independent packages can run in the same reviewed wave with disjoint locks.",
                "",
                "Concurrency frontier rule:",
                "",
                "- Launch Wave 1 packages only after dependencies are satisfied.",
                "",
                "Conflict / lock model:",
                "",
                "| Artifact / state / shared place | Lock owner | Conflict rule |",
                "|---|---|---|",
                "| area A files | Package A | exclusive lock during Wave 1 |",
                "| area B files | Package B | exclusive lock during Wave 1 |",
                "",
                "Parallel wave matrix:",
                "",
                "| Wave | Required-step frontier | Work packages | Independence proof | Shared places / locks | Integration barrier |",
                "|---|---|---|---|---|---|",
                "| Wave 1 | S1 | Package A, Package B | areas are disjoint | exclusive per-area locks | main integrates both before next wave |",
                "",
                "Failure policy:",
                "",
                "- A blocking subagent result stops the current wave at the integration barrier.",
                "",
                "Main-agent integration rule:",
                "",
                "- Candidate outputs become progress only after main-agent integration at the wave barrier.",
                "",
            ]
        return "\n".join(
            [
                "Who does the work: `Parallel subagent-driven`",
                "",
                "Task level: `Level 3`",
                "",
                f"Selected agent workflow: `{selected_agent_workflow}`",
                "",
                *concurrency_lines,
                "Work Assignment rationale:",
                "",
                "- Independent packages can run in parallel without shared control artifacts.",
                "",
                "Main agent owns:",
                "",
                "- approved control artifacts",
                "- dispatch",
                "- integration",
                "- progress log",
                "- stop-condition detection",
                "",
                "Delegation matrix:",
                "",
                "| Work package | Executor | Context pack | Allowed actions | Return format | Integration check |",
                "|---|---|---|---|---|---|",
                "| Package A | parallel subagent | requirements, goal, plan | inspect area A | findings and evidence | main integrates result |",
                "| Package B | parallel subagent | requirements, goal, plan | inspect area B | findings and evidence | main integrates result |",
                "",
                "Context Pack Requirements:",
                "",
                "| Field | Content |",
                "|---|---|",
                "| Relevant control excerpts | requirements success conditions, goal rules that cannot change, execution policy stop conditions |",
                "| Current batch objective | complete independent bounded inspections |",
                "| Allowed artifacts/places | target files listed in each package scope |",
                "| Forbidden changes | control artifacts, scope, work assignment, unrelated files |",
                "| Required evidence checks/evidence | command output and evidence references |",
                "| Stop conditions | missing context, invariant conflict, unauthorized scope change |",
                "| Expected return format | summary, files inspected, evidence, blockers, next integration note |",
                "",
                "Subagent workflow:",
                "",
                f"- {workflow_note}",
                "",
                "Parallel approval record:",
                "",
                f"- Human approval: `{human_approval}`",
                f"- Dependency independence: `{dependency_independence}`",
                f"- Control-review approval: `{control_review_approval}`",
                "",
                "Context Compression Rule:",
                "",
                "- Active control summary: summarize current requirements, goal rules that cannot change, work assignment, and stop conditions.",
                "- Completed work packages: record packages integrated at the limit.",
                "- Subagent outputs integrated: record candidate outputs accepted into main progress state.",
                "- Evidence produced: record evidence references and evidence check interpretation.",
                "- Deferred evidence checks and reasons: preserve policy-approved deferrals.",
                "- Unresolved blockers: record blockers requiring revision or human input.",
                "- Deviations from policy: record deviations and whether execution must stop.",
                "- Next allowed action: record the next policy-approved action.",
            ]
        )

    def write_artifact_chain(
        self,
        tmp: Path,
        work_assignment_body: str,
        *,
        include_review_work_assignment: bool = True,
        review_work_assignment_independence: str = "yes",
    ) -> tuple[Path, Path, Path, Path]:
        requirements = tmp / "requirements.md"
        goal = tmp / "goal.md"
        plan = tmp / "plan.md"
        review = tmp / "review.md"

        requirements.write_text(
            f"# Requirements\n\n## Requirements Analysis Status\n\nStatus: `Complete`\n\n{USER_APPROVAL_FIXTURE}\n",
            encoding="utf-8",
        )
        goal.write_text(
            "\n".join(
                [
                    "# Goal",
                    "",
                    "## Source Contracts",
                    "",
                    f"- Requirements analysis: `{requirements}`",
                    "",
                    "## Success Condition",
                    "",
                    "Codex may report `goal achieved: yes` only when the single what counts as done is satisfied.",
                    "",
                    "- Evidence needed to call it done is present.",
                    "",
                    "## How We Know The User Purpose Was Met",
                    "",
                    "| Element | Requirement |",
                    "|---|---|",
                    "| Beneficiary / observer | test operator |",
                    "| Purpose-realizing outcome observed | test operator can observe the approved outcome |",
                    "| Supporting Evidence | guard tests support structural readiness |",
                    "| Sufficient evidence level | internal |",
                    "| If user-purpose evidence unavailable | report pending and smallest next observation |",
                    "| Allowed completion wording | internal user-purpose evidence sufficient for this guard fixture |",
                    "",
                    "## Where The Result Must Show Up",
                    "",
                    "| Element | Requirement |",
                    "|---|---|",
                    "| Target state | context-work assignment guard fixture intended result |",
                    "| Required result places | context-work assignment fixture place model |",
                    "| Place actions | act / inspect / preserve / exclude / discover |",
                    "| Residual reconciliation | account for old state, unknown places, exclusions, preserved places, and remaining mismatches |",
                    "| Result-placement wording | strongest result claim claim requires result-placement adequate |",
                    "| Partial/unavailable handling | report partial, missing, unavailable, or not applicable with justification |",
                    "| Distinction from user-purpose evidence | result-placement is distinct from How We Know The User Purpose Was Met |",
                    "",
                    "## What Counts As Done",
                    "",
                    "| Element | Requirement |",
                    "|---|---|",
                    "| What counts as done | context-work assignment guard fixture is structurally ready |",
                    "| Evidence needed to call it done | evidence needed to call it done is observed |",
                    "| Allowed achieved claim | only what counts as done supports goal achieved: yes |",
                    "| Steps that make the result true | context work assignment guard fixture required answer path |",
                    "",
                    "## Work Covered And Allowed Actions Contract",
                    "",
                    "| Element | Requirement |",
                    "|---|---|",
                    "| Work covered in this run | context work assignment guard fixture horizon |",
                    "| What the agent may do | local guard fixture checks |",
                    "| Forbidden actions | none |",
                    "| Prepare-only / observe-only actions | none |",
                    "| Explicitly out-of-scope items | none |",
                    "| Work coverage rule | every horizon item is accounted for in this fixture |",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        plan.write_text(
            "\n".join(
                [
                    "# Execution Policy",
                    "",
                    "## Execution Policy Status",
                    "",
                    "Status: `Candidate`",
                    "",
                    "## Source Contracts",
                    "",
                    f"- Requirements analysis: `{requirements}`",
                    f"- Goal file: `{goal}`",
                    "",
                    "## Work Coverage And Action Limits Matrix",
                    "",
                    "| Work item / place | In work covered in this run? | What the agent may do | Required runtime handling | Counts as achieved? |",
                    "|---|---|---|---|---|",
                    "| context work assignment guard fixture | yes | execute | run guard / compiler fixture checks | yes if fixture passes |",
                    "",
                    "## Steps That Make The Result True",
                    "",
                    "| Required step | Required state transition | Required evidence |",
                    "|---|---|---|",
                    "| S1 | fixture input -> context work assignment guard-ready chain | guard fixture files exist |",
                    "",
                    "## Action That Can Make It Done",
                    "",
                    "Action that can make it done:",
                    "",
                    "- Run or observe the action that can make it done before any achieved claim.",
                    "",
                    "Proof of impossibility, if any:",
                    "",
                    "- Record the condition proving the action cannot be attempted.",
                    "",
                    "Non-achieved terminal report rule:",
                    "",
                    "- If it is not done, the report may be produced only after the action is attempted and fails, or impossibility is proven.",
                    "",
                    "## Where The Result Must Show Up",
                    "",
                    "### Places The Result Appears",
                    "",
                    "| Place | Role in target realization | Required action | Verification / reconciliation |",
                    "|---|---|---|---|",
                    "| work assignment fixture place | carries fixture intended result | inspect | reconcile residuals in fixture scope |",
                    "",
                    "### Place Classes",
                    "",
                    "- Must act: none for work assignment fixture.",
                    "- Must inspect: work assignment fixture place.",
                    "- Must preserve: work assignment semantics.",
                    "- Explicitly out of scope: target implementation.",
                    "- Unknown or requires discovery: none.",
                    "",
                    "### Residual Reconciliation",
                    "",
                    "- result-placement fixture residuals are not the tested behavior in this file.",
                    "",
                    "## Who Does The Work / Context Use",
                    "",
                    work_assignment_body,
                    "",
                    "## Candidate Plan Tasks",
                    "",
                    "### Batch 1: context work assignment guard fixture",
                    "",
                    "Required step(s):",
                    "",
                    "- S1",
                    "",
                    "Role: `mainline`",
                    "",
                    "State transition advanced:",
                    "",
                    "- S1 fixture transition is satisfied.",
                    "",
                    "Transition evidence produced:",
                    "",
                    "- Fixture evidence needed to call it done is recorded.",
                    "",
                    "Integration check:",
                    "",
                    "- Main agent accepts S1 evidence.",
                    "",
                    "Counts as goal progress: `yes`",
                    "",
                    "Why this is not merely component completion:",
                    "",
                    "- It records transition evidence for the fixture path.",
                    "",
                    "Goal:",
                    "",
                    "- Keep the context work assignment guard fixture structurally ready.",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        review_parts = [
            "# Review",
            "",
            "## Review Status",
            "",
            "Status: `Approved`",
            "",
            f"Reviewed `{requirements}`, `{goal}`, and `{plan}`.",
            "",
        ]
        if include_review_work_assignment:
            review_parts.extend(
                [
                    "## Review Independence",
                    "",
                    "- Requirements analysis: `yes`",
                    "- Goal file: `yes`",
                    "- Execution policy: `yes`",
                    f"- Who does the work / context use: `{review_work_assignment_independence}`",
                    "- User purpose evidence check: `yes`",
                    "- Result placement check: `yes`",
                    "- What counts as done check: `yes`",
                    "- answer path check: `yes`",
                    "- Work covered in this run and authority check: `yes`",
                    "- Subagent concurrency check: `yes`",
                    "",
                    "## Required Check Results",
                    "",
                    "- Design Answer Method Check: `Not applicable`",
                    "- Steps That Make The Result True Check: `PASS`",
                    "- Work Coverage / Action Limits Check: `PASS`",
                    "- Done / Purpose / Result Placement Check: `PASS`",
                    f"- Work Assignment / Subagent Check: `{'PASS' if review_work_assignment_independence == 'yes' else 'FAIL'}`",
                    "",
                    "## Who Does The Work / Context Use",
                    "",
                    "Findings:",
                    "- Reviewed work assignment, context pack requirements, agent workflow, context compression, and integration checks; no Blocking/Major findings.",
                    "",
                    "## User Purpose Evidence Check",
                    "",
                    "Classification:",
                    "- Purpose-limit evidence not required, justified",
                    "",
                    "Findings:",
                    "- This guard fixture exercises internal structural readiness; internal feedback is sufficient for the fixture purpose.",
                    "",
                    "## Result Placement Check",
                    "",
                    "Classification:",
                    "- result-placement adequate",
                    "",
                    "Findings:",
                    "- Guard fixture includes result placement structure so work assignment tests isolate work assignment behavior.",
                    "",
                    "## What Counts As Done Check",
                    "",
                    "Findings:",
                    "- The single what counts as done is separated from not done reports.",
                    "",
                    "## Answer Path Check",
                    "",
                    "Findings:",
                    "- Work packages map to the fixture required step.",
                    "",
                    "## Work Covered And Allowed Actions Check",
                    "",
                    "Findings:",
                    "- Work covered in this run and runtime authority are compact and fixture-bounded.",
                    "",
                    "## Parallel Agent Safety Check",
                    "",
                    "Findings:",
                    "- Subagent execution mode matches the work assignment and fixture agent workflow.",
                    "",
                ]
            )
        review_parts.extend(
            [
                "## Final Observer Check",
                "",
                "- Last independent review completed at: `test`",
                "- Substantive artifact changes after last independent review: `no`",
                "- If yes, final re-review performed: `no`",
                "- Final reviewers confirming no Blocking/Major findings:",
                "  - test reviewer",
                "- Deterministic-only exception used: `no`",
                "- Deterministic guard covering exception:",
                "  - not used",
                "- Approval allowed after final observer check: `yes`",
            ]
        )
        review.write_text("\n".join(review_parts) + "\n", encoding="utf-8")
        return requirements, goal, plan, review

    def test_execution_policy_requires_context_work_assignment(self):
        skill = (
            ROOT
            / ".agents/skills/writing-cybernetic-execution-policies/SKILL.md"
        ).read_text(encoding="utf-8")
        template = (
            ROOT
            / ".agents/skills/writing-cybernetic-execution-policies/assets/execution-policy-template.md"
        ).read_text(encoding="utf-8")
        registry = (
            ROOT / ".agents/skills/references/delegation-workflow-registry.json"
        )

        for text in (skill, template):
            self.assertIn("Who Does The Work / Context Use", text)
            self.assertIn("Main-only", text)
            self.assertIn("Serial subagent-driven", text)
            self.assertIn("Parallel subagent-driven", text)
            self.assertIn("Context pack", text)
            self.assertIn("Return format", text)
            self.assertIn("Integration check", text)
            self.assertIn("Task level", text)
            self.assertIn("Context Pack Requirements", text)
            self.assertIn("Context Compression Rule", text)
            self.assertIn("Selected agent workflow", text)
            self.assertIn("delegation-workflow-registry.json", text)

        self.assertIn("main agent owns", template.casefold())
        self.assertIn("subagent owns", template.casefold())
        self.assertTrue(registry.exists())
        registry_text = registry.read_text(encoding="utf-8")
        self.assertIn("superpowers-subagent-driven-development", registry_text)
        self.assertIn("superpowers-dispatching-parallel-agents", registry_text)
        for guard_path in (
            ROOT / ".agents/skills/orchestrating-cybernetic-pregoal/scripts/orchestration_guard.py",
            ROOT / ".agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py",
        ):
            self.assertIn("delegation-workflow-registry.json", guard_path.read_text(encoding="utf-8"))

    def test_review_checks_context_work_assignment(self):
        skill = (
            ROOT
            / ".agents/skills/reviewing-cybernetic-control-structures/SKILL.md"
        ).read_text(encoding="utf-8")
        template = (
            ROOT
            / ".agents/skills/reviewing-cybernetic-control-structures/assets/control-review-template.md"
        ).read_text(encoding="utf-8")

        for text in (skill, template):
            self.assertIn("Who Does The Work / Context Use", text)
            self.assertIn("work assignment", text.casefold())
            self.assertIn("context pack", text.casefold())
            self.assertIn("return format", text.casefold())
            self.assertIn("integration check", text.casefold())

        self.assertIn("Level 3/4", skill)
        self.assertIn("context overload", skill.casefold())

    def test_subagent_authorization_distinguishes_review_and_runtime_execution(self):
        orchestrator = (
            ROOT / ".agents/skills/orchestrating-cybernetic-pregoal/SKILL.md"
        ).read_text(encoding="utf-8")
        infrastructure = (
            ROOT / ".agents/skills/cybernetic-superpowers-infrastructure/references/superpowers-infrastructure-policy.md"
        ).read_text(encoding="utf-8")

        for text in (orchestrator, infrastructure):
            self.assertIn("pre-goal review subagents", text.casefold())
            self.assertIn("runtime target-work subagents", text.casefold())
            self.assertIn("user launches that `/goal`", text)
            self.assertIn("parallel runtime subagents", text.casefold())

    def test_runtime_compiler_preserves_serial_subagent_work_assignment(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            requirements, goal, plan, review = self.write_artifact_chain(
                tmp,
                self.complete_serial_work_assignment(),
            )
            runtime_contract = tmp / "runtime.goal.md"

            result = subprocess.run(
                [
                    sys.executable,
                    str(
                        ROOT
                        / ".agents/skills/compiling-cybernetic-runtime-goals/scripts/compile_runtime_goal.py"
                    ),
                    "--requirements",
                    str(requirements),
                    "--goal",
                    str(goal),
                    "--plan",
                    str(plan),
                    "--review",
                    str(review),
                    "--skip-guard",
                    "--i-understand-this-bypasses-phase-checks",
                    "--out",
                    str(runtime_contract),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
            contract_text = runtime_contract.read_text(encoding="utf-8")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Use this /goal:", result.stdout)
        self.assertIn("Execute the runtime goal file at", result.stdout)
        self.assertNotIn("$superpowers:subagent-driven-development", result.stdout)
        self.assertIn("Who does the work: `Serial subagent-driven`", contract_text)
        self.assertIn("Selected agent workflow: `bounded-protocol`", contract_text)
        self.assertIn("bounded delegation protocol", contract_text)
        self.assertNotIn("Execute serially according to the approved batch rhythm", result.stdout)

    def test_runtime_compiler_uses_superpowers_subagent_workflow_when_plan_selects_it(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            requirements, goal, plan, review = self.write_artifact_chain(
                tmp,
                self.complete_serial_work_assignment(
                    "Implementation-plan same-session delegation uses `$superpowers:subagent-driven-development` discipline for independent bounded development tasks.",
                    selected_agent_workflow="superpowers-subagent-driven-development",
                ),
            )
            runtime_contract = tmp / "runtime.goal.md"

            result = subprocess.run(
                [
                    sys.executable,
                    str(
                        ROOT
                        / ".agents/skills/compiling-cybernetic-runtime-goals/scripts/compile_runtime_goal.py"
                    ),
                    "--requirements",
                    str(requirements),
                    "--goal",
                    str(goal),
                    "--plan",
                    str(plan),
                    "--review",
                    str(review),
                    "--skip-guard",
                    "--i-understand-this-bypasses-phase-checks",
                    "--out",
                    str(runtime_contract),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
            contract_text = runtime_contract.read_text(encoding="utf-8")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("$superpowers:subagent-driven-development", result.stdout)
        self.assertIn("Selected agent workflow: `superpowers-subagent-driven-development`", contract_text)
        self.assertIn("$superpowers:subagent-driven-development", contract_text)
        self.assertNotIn("$superpowers:dispatching-parallel-agents", contract_text)

    def test_runtime_compiler_uses_dispatching_parallel_agents_when_plan_selects_it(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            requirements, goal, plan, review = self.write_artifact_chain(
                tmp,
                self.complete_parallel_work_assignment(
                    selected_agent_workflow="superpowers-dispatching-parallel-agents",
                    delegation_workflow="Approved parallel independent-domain delegation uses `$superpowers:dispatching-parallel-agents` under the plan wave, lock, and integration barriers.",
                ),
            )
            runtime_contract = tmp / "runtime.goal.md"

            result = subprocess.run(
                [
                    sys.executable,
                    str(
                        ROOT
                        / ".agents/skills/compiling-cybernetic-runtime-goals/scripts/compile_runtime_goal.py"
                    ),
                    "--requirements",
                    str(requirements),
                    "--goal",
                    str(goal),
                    "--plan",
                    str(plan),
                    "--review",
                    str(review),
                    "--skip-guard",
                    "--i-understand-this-bypasses-phase-checks",
                    "--out",
                    str(runtime_contract),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
            contract_text = runtime_contract.read_text(encoding="utf-8")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("$superpowers:dispatching-parallel-agents", result.stdout)
        self.assertIn("Selected agent workflow: `superpowers-dispatching-parallel-agents`", contract_text)
        self.assertIn("$superpowers:dispatching-parallel-agents", contract_text)
        self.assertNotIn("$superpowers:subagent-driven-development` only", contract_text)

    def test_runtime_compiler_does_not_infer_superpowers_workflow_from_notes(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            requirements, goal, plan, review = self.write_artifact_chain(
                tmp,
                self.complete_serial_work_assignment(
                    "Reference note: `$superpowers:subagent-driven-development` is an implementation-plan workflow, but this task uses the plan-local bounded delegation protocol.",
                    selected_agent_workflow="bounded-protocol",
                ),
            )
            runtime_contract = tmp / "runtime.goal.md"

            result = subprocess.run(
                [
                    sys.executable,
                    str(
                        ROOT
                        / ".agents/skills/compiling-cybernetic-runtime-goals/scripts/compile_runtime_goal.py"
                    ),
                    "--requirements",
                    str(requirements),
                    "--goal",
                    str(goal),
                    "--plan",
                    str(plan),
                    "--review",
                    str(review),
                    "--skip-guard",
                    "--i-understand-this-bypasses-phase-checks",
                    "--out",
                    str(runtime_contract),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
            contract_text = runtime_contract.read_text(encoding="utf-8")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("$superpowers:subagent-driven-development", result.stdout)
        self.assertIn("Selected agent workflow: `bounded-protocol`", contract_text)
        self.assertNotIn("Selected agent workflow: `superpowers-subagent-driven-development`", contract_text)

    def test_control_chain_guard_requires_review_of_context_work_assignment(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_artifact_chain(
                Path(tmpdir),
                self.complete_serial_work_assignment(),
                include_review_work_assignment=False,
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(
                        ROOT
                        / ".agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py"
                    ),
                    "--requirements",
                    str(requirements),
                    "--goal",
                    str(goal),
                    "--plan",
                    str(plan),
                    "--review",
                    str(review),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("NEXT: RunReview", output)
        self.assertIn("Who Does The Work / Context Use", output)

    def test_control_chain_guard_rejects_incomplete_subagent_work_assignment(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_artifact_chain(
                Path(tmpdir),
                "Who does the work: `Serial subagent-driven`\n",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(
                        ROOT
                        / ".agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py"
                    ),
                    "--requirements",
                    str(requirements),
                    "--goal",
                    str(goal),
                    "--plan",
                    str(plan),
                    "--review",
                    str(review),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("NEXT: RunExecutionPolicy", output)
        self.assertIn("Context pack", output)
        self.assertIn("Return format", output)
        self.assertIn("Integration check", output)

    def test_guards_reject_missing_selected_agent_workflow(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_artifact_chain(
                Path(tmpdir),
                self.complete_serial_work_assignment(selected_agent_workflow=None),
            )

            control_guard = subprocess.run(
                [
                    sys.executable,
                    str(
                        ROOT
                        / ".agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py"
                    ),
                    "--requirements",
                    str(requirements),
                    "--goal",
                    str(goal),
                    "--plan",
                    str(plan),
                    "--review",
                    str(review),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
            orchestration_guard = subprocess.run(
                [
                    sys.executable,
                    str(
                        ROOT
                        / ".agents/skills/orchestrating-cybernetic-pregoal/scripts/orchestration_guard.py"
                    ),
                    "--state",
                    "before-review",
                    "--requirements",
                    str(requirements),
                    "--goal",
                    str(goal),
                    "--plan",
                    str(plan),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        for result in (control_guard, orchestration_guard):
            output = result.stdout + result.stderr
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Selected agent workflow", output)

    def test_guards_reject_none_selected_agent_workflow_for_subagent_work_assignment(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_artifact_chain(
                Path(tmpdir),
                self.complete_serial_work_assignment(selected_agent_workflow="none"),
            )

            control_guard = subprocess.run(
                [
                    sys.executable,
                    str(
                        ROOT
                        / ".agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py"
                    ),
                    "--requirements",
                    str(requirements),
                    "--goal",
                    str(goal),
                    "--plan",
                    str(plan),
                    "--review",
                    str(review),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
            orchestration_guard = subprocess.run(
                [
                    sys.executable,
                    str(
                        ROOT
                        / ".agents/skills/orchestrating-cybernetic-pregoal/scripts/orchestration_guard.py"
                    ),
                    "--state",
                    "before-review",
                    "--requirements",
                    str(requirements),
                    "--goal",
                    str(goal),
                    "--plan",
                    str(plan),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        for result in (control_guard, orchestration_guard):
            output = result.stdout + result.stderr
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Selected agent workflow", output)

    def test_guards_reject_level_3_main_only_without_context_load_justification(self):
        work_assignment_body = "\n".join(
            [
                "Who does the work: `Main-only`",
                "",
                "Task level: `Level 3`",
                "",
                "Work Assignment rationale:",
                "",
                "- simpler",
                "",
                "Main agent owns:",
                "",
                "- approved control artifacts",
                "- dispatch",
                "- integration",
                "- progress log",
                "- stop-condition detection",
            ]
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_artifact_chain(Path(tmpdir), work_assignment_body)

            control_guard = subprocess.run(
                [
                    sys.executable,
                    str(
                        ROOT
                        / ".agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py"
                    ),
                    "--requirements",
                    str(requirements),
                    "--goal",
                    str(goal),
                    "--plan",
                    str(plan),
                    "--review",
                    str(review),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
            orchestration_guard = subprocess.run(
                [
                    sys.executable,
                    str(
                        ROOT
                        / ".agents/skills/orchestrating-cybernetic-pregoal/scripts/orchestration_guard.py"
                    ),
                    "--state",
                    "before-review",
                    "--requirements",
                    str(requirements),
                    "--goal",
                    str(goal),
                    "--plan",
                    str(plan),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        for result in (control_guard, orchestration_guard):
            output = result.stdout + result.stderr
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Main-only context-load justification", output)

    def test_guards_reject_missing_task_level(self):
        work_assignment_body = "\n".join(
            [
                "Who does the work: `Main-only`",
                "",
                "Selected agent workflow: `none`",
                "",
                "Work Assignment rationale:",
                "",
                "- local bounded work",
                "",
                "Main agent owns:",
                "",
                "- approved control artifacts",
                "- dispatch",
                "- integration",
                "- progress log",
                "- stop-condition detection",
                "",
                "Context Compression Rule:",
                "",
                "- Active control summary: present.",
                "- Completed work packages: present.",
                "- Subagent outputs integrated: present.",
                "- Evidence produced: present.",
                "- Deferred evidence checks and reasons: present.",
                "- Unresolved blockers: present.",
                "- Deviations from policy: present.",
                "- Next allowed action: present.",
            ]
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_artifact_chain(Path(tmpdir), work_assignment_body)

            control_guard = subprocess.run(
                [
                    sys.executable,
                    str(
                        ROOT
                        / ".agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py"
                    ),
                    "--requirements",
                    str(requirements),
                    "--goal",
                    str(goal),
                    "--plan",
                    str(plan),
                    "--review",
                    str(review),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
            orchestration_guard = subprocess.run(
                [
                    sys.executable,
                    str(
                        ROOT
                        / ".agents/skills/orchestrating-cybernetic-pregoal/scripts/orchestration_guard.py"
                    ),
                    "--state",
                    "before-review",
                    "--requirements",
                    str(requirements),
                    "--goal",
                    str(goal),
                    "--plan",
                    str(plan),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        for result in (control_guard, orchestration_guard):
            output = result.stdout + result.stderr
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Task level", output)

    def test_guards_reject_parallel_approval_no_values(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_artifact_chain(
                Path(tmpdir),
                self.complete_parallel_work_assignment(
                    human_approval="no",
                    dependency_independence="no",
                    control_review_approval="no",
                ).replace("- Human approval:", "Human approval:")
                .replace("- Dependency independence:", "Dependency independence:")
                .replace("- Control-review approval:", "Control-review approval:"),
            )

            control_guard = subprocess.run(
                [
                    sys.executable,
                    str(
                        ROOT
                        / ".agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py"
                    ),
                    "--requirements",
                    str(requirements),
                    "--goal",
                    str(goal),
                    "--plan",
                    str(plan),
                    "--review",
                    str(review),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
            orchestration_guard = subprocess.run(
                [
                    sys.executable,
                    str(
                        ROOT
                        / ".agents/skills/orchestrating-cybernetic-pregoal/scripts/orchestration_guard.py"
                    ),
                    "--state",
                    "before-review",
                    "--requirements",
                    str(requirements),
                    "--goal",
                    str(goal),
                    "--plan",
                    str(plan),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        for result in (control_guard, orchestration_guard):
            output = result.stdout + result.stderr
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Human approval", output)
            self.assertIn("Dependency independence", output)
            self.assertIn("Control-review approval", output)

    def test_guards_accept_parallel_approval_yes_values(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_artifact_chain(
                Path(tmpdir),
                self.complete_parallel_work_assignment(),
            )

            control_guard = subprocess.run(
                [
                    sys.executable,
                    str(
                        ROOT
                        / ".agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py"
                    ),
                    "--requirements",
                    str(requirements),
                    "--goal",
                    str(goal),
                    "--plan",
                    str(plan),
                    "--review",
                    str(review),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
            orchestration_guard = subprocess.run(
                [
                    sys.executable,
                    str(
                        ROOT
                        / ".agents/skills/orchestrating-cybernetic-pregoal/scripts/orchestration_guard.py"
                    ),
                    "--state",
                    "before-review",
                    "--requirements",
                    str(requirements),
                    "--goal",
                    str(goal),
                    "--plan",
                    str(plan),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        self.assertEqual(control_guard.returncode, 0, control_guard.stdout + control_guard.stderr)
        self.assertEqual(orchestration_guard.returncode, 0, orchestration_guard.stdout + orchestration_guard.stderr)

    def test_subagent_execution_mode_is_first_class_template_field(self):
        plan_template = (
            ROOT
            / ".agents/skills/writing-cybernetic-execution-policies/assets/execution-policy-template.md"
        ).read_text(encoding="utf-8")
        review_template = (
            ROOT
            / ".agents/skills/reviewing-cybernetic-control-structures/assets/control-review-template.md"
        ).read_text(encoding="utf-8")

        for expected in (
            "Subagent execution mode",
            "Max concurrent subagents",
            "Concurrency selection rationale",
            "Conflict / lock model",
            "Parallel wave matrix",
            "Required-step frontier",
            "Failure policy",
            "Main-agent integration rule",
        ):
            self.assertIn(expected, plan_template)

        self.assertIn("Parallel Agent Safety Check", review_template)
        self.assertIn("Parallel agent safety check", review_template)

    def test_parallel_wave_matrix_requires_required_answer_path_frontier(self):
        old_wave_matrix = self.complete_parallel_work_assignment().replace(
            "| Wave | Required-step frontier | Work packages | Independence proof | Shared places / locks | Integration barrier |",
            "| Wave | Work packages | Independence proof | Shared places / locks | Integration barrier |",
        ).replace(
            "|---|---|---|---|---|---|",
            "|---|---|---|---|---|",
        ).replace(
            "| Wave 1 | S1 | Package A, Package B | areas are disjoint | exclusive per-area locks | main integrates both before next wave |",
            "| Wave 1 | Package A, Package B | areas are disjoint | exclusive per-area locks | main integrates both before next wave |",
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_artifact_chain(Path(tmpdir), old_wave_matrix)
            result = subprocess.run(
                [
                    sys.executable,
                    str(
                        ROOT
                        / ".agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py"
                    ),
                    "--requirements",
                    str(requirements),
                    "--goal",
                    str(goal),
                    "--plan",
                    str(plan),
                    "--review",
                    str(review),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("NEXT: RunExecutionPolicy", output)
        self.assertIn("Required-step frontier", output)

    def test_max_safe_parallel_hsa_requires_serial_downgrade_rationale(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            requirements, goal, plan, review = self.write_artifact_chain(
                tmp,
                self.complete_serial_work_assignment(),
            )
            requirements.write_text(
                requirements.read_text(encoding="utf-8").replace(
                    "| Agent delegation preference | no preference |",
                    "| Agent delegation preference | max-safe-parallel |",
                ).replace(
                    "| Parallel execution authority | not applicable |",
                    "| Parallel execution authority | approved |",
                ).replace(
                    "| Maximum parallel agents | not specified |",
                    "| Maximum parallel agents | auto |",
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(
                        ROOT
                        / ".agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py"
                    ),
                    "--requirements",
                    str(requirements),
                    "--goal",
                    str(goal),
                    "--plan",
                    str(plan),
                    "--review",
                    str(review),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("NEXT: RunExecutionPolicy", output)
        self.assertIn("max-safe-parallel", output)
        self.assertIn("safe frontier", output)

    def test_serial_superpowers_subagent_work_assignment_requires_single_active_mode(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_artifact_chain(
                Path(tmpdir),
                self.complete_serial_work_assignment(
                    "Implementation-plan same-session delegation uses `$superpowers:subagent-driven-development` discipline for bounded work packages.",
                    selected_agent_workflow="superpowers-subagent-driven-development",
                    include_concurrency_policy=False,
                ),
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(
                        ROOT
                        / ".agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py"
                    ),
                    "--requirements",
                    str(requirements),
                    "--goal",
                    str(goal),
                    "--plan",
                    str(plan),
                    "--review",
                    str(review),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("NEXT: RunExecutionPolicy", output)
        self.assertIn("Subagent execution mode", output)
        self.assertIn("serial-single-active", output)
        self.assertIn("Max concurrent subagents", output)

    def test_parallel_subagent_work_assignment_requires_wave_locks_and_failure_policy(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_artifact_chain(
                Path(tmpdir),
                self.complete_parallel_work_assignment(include_concurrency_policy=False),
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(
                        ROOT
                        / ".agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py"
                    ),
                    "--requirements",
                    str(requirements),
                    "--goal",
                    str(goal),
                    "--plan",
                    str(plan),
                    "--review",
                    str(review),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("NEXT: RunExecutionPolicy", output)
        self.assertIn("parallel-max-safe", output)
        self.assertIn("Parallel wave matrix", output)
        self.assertIn("Conflict / lock model", output)
        self.assertIn("Failure policy", output)

    def test_guard_rejects_parallel_mode_with_superpowers_subagent_driven_development(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_artifact_chain(
                Path(tmpdir),
                self.complete_parallel_work_assignment(
                    selected_agent_workflow="superpowers-subagent-driven-development",
                    delegation_workflow="Invalid fixture: SDD cannot dispatch multiple implementation subagents concurrently.",
                ),
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(
                        ROOT
                        / ".agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py"
                    ),
                    "--requirements",
                    str(requirements),
                    "--goal",
                    str(goal),
                    "--plan",
                    str(plan),
                    "--review",
                    str(review),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("NEXT: RunExecutionPolicy", output)
        self.assertIn("superpowers-subagent-driven-development", output)
        self.assertIn("parallel-max-safe", output)

    def test_guard_accepts_parallel_mode_with_dispatching_parallel_agents_workflow(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_artifact_chain(
                Path(tmpdir),
                self.complete_parallel_work_assignment(
                    selected_agent_workflow="superpowers-dispatching-parallel-agents",
                    delegation_workflow="Approved parallel independent-domain delegation uses `$superpowers:dispatching-parallel-agents` under the plan wave, lock, and integration barriers.",
                ),
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(
                        ROOT
                        / ".agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py"
                    ),
                    "--requirements",
                    str(requirements),
                    "--goal",
                    str(goal),
                    "--plan",
                    str(plan),
                    "--review",
                    str(review),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_orchestration_guard_rejects_parallel_sdd_before_review(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, _review = self.write_artifact_chain(
                Path(tmpdir),
                self.complete_parallel_work_assignment(
                    selected_agent_workflow="superpowers-subagent-driven-development",
                    delegation_workflow="Invalid fixture: SDD cannot dispatch multiple implementation subagents concurrently.",
                ),
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(
                        ROOT
                        / ".agents/skills/orchestrating-cybernetic-pregoal/scripts/orchestration_guard.py"
                    ),
                    "--state",
                    "before-review",
                    "--requirements",
                    str(requirements),
                    "--goal",
                    str(goal),
                    "--plan",
                    str(plan),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("NEXT: RunExecutionPolicy", output)
        self.assertIn("superpowers-subagent-driven-development", output)
        self.assertIn("parallel-max-safe", output)

    def test_orchestration_guard_accepts_parallel_dispatch_before_review(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, _review = self.write_artifact_chain(
                Path(tmpdir),
                self.complete_parallel_work_assignment(
                    selected_agent_workflow="superpowers-dispatching-parallel-agents",
                    delegation_workflow="Approved parallel independent-domain delegation uses `$superpowers:dispatching-parallel-agents` under the plan wave, lock, and integration barriers.",
                ),
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(
                        ROOT
                        / ".agents/skills/orchestrating-cybernetic-pregoal/scripts/orchestration_guard.py"
                    ),
                    "--state",
                    "before-review",
                    "--requirements",
                    str(requirements),
                    "--goal",
                    str(goal),
                    "--plan",
                    str(plan),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_hsa_rejects_conflicting_max_safe_parallel_with_sdd_workflow_preference(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            requirements, goal, plan, review = self.write_artifact_chain(
                tmp,
                self.complete_serial_work_assignment(
                    "Implementation-plan same-session delegation uses `$superpowers:subagent-driven-development` discipline for bounded work packages.",
                    selected_agent_workflow="superpowers-subagent-driven-development",
                ),
            )
            requirements.write_text(
                requirements.read_text(encoding="utf-8")
                .replace(
                    "| Agent delegation preference | no preference |",
                    "| Agent delegation preference | max-safe-parallel |",
                )
                .replace(
                    "| Agent workflow preference | no preference |",
                    "| Agent workflow preference | superpowers-subagent-driven-development |",
                )
                .replace(
                    "| Parallel execution authority | not applicable |",
                    "| Parallel execution authority | approved |",
                )
                .replace(
                    "| Maximum parallel agents | not specified |",
                    "| Maximum parallel agents | auto |",
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(
                        ROOT
                        / ".agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py"
                    ),
                    "--requirements",
                    str(requirements),
                    "--goal",
                    str(goal),
                    "--plan",
                    str(plan),
                    "--review",
                    str(review),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("NEXT: ReturnToRequirementsAnalysis", output)
        self.assertIn("Agent workflow preference", output)
        self.assertIn("max-safe-parallel", output)

    def test_runtime_compiler_preserves_and_can_expect_subagent_execution_mode(self):
        work_assignment = self.complete_serial_work_assignment(
            "Implementation-plan same-session delegation uses `$superpowers:subagent-driven-development` discipline for bounded work packages.",
            selected_agent_workflow="superpowers-subagent-driven-development",
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            requirements, goal, plan, review = self.write_artifact_chain(tmp, work_assignment)
            runtime_contract = tmp / "runtime.goal.md"

            result = subprocess.run(
                [
                    sys.executable,
                    str(
                        ROOT
                        / ".agents/skills/compiling-cybernetic-runtime-goals/scripts/compile_runtime_goal.py"
                    ),
                    "--requirements",
                    str(requirements),
                    "--goal",
                    str(goal),
                    "--plan",
                    str(plan),
                    "--review",
                    str(review),
                    "--expect-subagent-mode",
                    "parallel-max-safe",
                    "--out",
                    str(runtime_contract),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

            passing_result = subprocess.run(
                [
                    sys.executable,
                    str(
                        ROOT
                        / ".agents/skills/compiling-cybernetic-runtime-goals/scripts/compile_runtime_goal.py"
                    ),
                    "--requirements",
                    str(requirements),
                    "--goal",
                    str(goal),
                    "--plan",
                    str(plan),
                    "--review",
                    str(review),
                    "--expect-subagent-mode",
                    "serial-single-active",
                    "--out",
                    str(runtime_contract),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
            contract_text = runtime_contract.read_text(encoding="utf-8") if runtime_contract.exists() else ""

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("expected subagent execution mode", result.stdout + result.stderr)
        self.assertEqual(passing_result.returncode, 0, passing_result.stdout + passing_result.stderr)
        self.assertIn("Subagent execution mode: `serial-single-active`", contract_text)

    def test_guards_reject_weak_context_pack_requirements(self):
        weak_work_assignment = "\n".join(
            [
                "Who does the work: `Serial subagent-driven`",
                "",
                "Task level: `Level 3`",
                "",
                "Work Assignment rationale:",
                "",
                "- Level 3 context load needs bounded delegation.",
                "",
                "Main agent owns:",
                "",
                "- approved control artifacts",
                "- dispatch",
                "- integration",
                "- progress log",
                "- stop-condition detection",
                "",
                "Delegation matrix:",
                "",
                "| Work package | Executor | Context pack | Allowed actions | Return format | Integration check |",
                "|---|---|---|---|---|---|",
                "| Package A | serial subagent | requirements, goal, plan | inspect files | summary | review |",
                "",
                "Subagent workflow:",
                "",
                "- Runtime target-work delegation uses `$superpowers:subagent-driven-development` discipline.",
                "",
                "Context Compression Rule:",
                "",
                "- Active control summary: present.",
                "- Completed work packages: present.",
                "- Subagent outputs integrated: present.",
                "- Evidence produced: present.",
                "- Deferred evidence checks and reasons: present.",
                "- Unresolved blockers: present.",
                "- Deviations from policy: present.",
                "- Next allowed action: present.",
            ]
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_artifact_chain(Path(tmpdir), weak_work_assignment)

            control_guard = subprocess.run(
                [
                    sys.executable,
                    str(
                        ROOT
                        / ".agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py"
                    ),
                    "--requirements",
                    str(requirements),
                    "--goal",
                    str(goal),
                    "--plan",
                    str(plan),
                    "--review",
                    str(review),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
            orchestration_guard = subprocess.run(
                [
                    sys.executable,
                    str(
                        ROOT
                        / ".agents/skills/orchestrating-cybernetic-pregoal/scripts/orchestration_guard.py"
                    ),
                    "--state",
                    "before-review",
                    "--requirements",
                    str(requirements),
                    "--goal",
                    str(goal),
                    "--plan",
                    str(plan),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        for result in (control_guard, orchestration_guard):
            output = result.stdout + result.stderr
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Context Pack Requirements", output)
            self.assertIn("Relevant control excerpts", output)

    def test_orchestration_guard_rejects_incomplete_subagent_work_assignment(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, _review = self.write_artifact_chain(
                Path(tmpdir),
                "Who does the work: `Serial subagent-driven`\n",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(
                        ROOT
                        / ".agents/skills/orchestrating-cybernetic-pregoal/scripts/orchestration_guard.py"
                    ),
                    "--state",
                    "before-review",
                    "--requirements",
                    str(requirements),
                    "--goal",
                    str(goal),
                    "--plan",
                    str(plan),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("NEXT: RunExecutionPolicy", output)
        self.assertIn("Context pack", output)
        self.assertIn("Return format", output)
        self.assertIn("Integration check", output)

    def test_guards_accept_complete_subagent_work_assignment_structure(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_artifact_chain(
                Path(tmpdir),
                self.complete_serial_work_assignment(),
            )

            control_guard = subprocess.run(
                [
                    sys.executable,
                    str(
                        ROOT
                        / ".agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py"
                    ),
                    "--requirements",
                    str(requirements),
                    "--goal",
                    str(goal),
                    "--plan",
                    str(plan),
                    "--review",
                    str(review),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
            orchestration_guard = subprocess.run(
                [
                    sys.executable,
                    str(
                        ROOT
                        / ".agents/skills/orchestrating-cybernetic-pregoal/scripts/orchestration_guard.py"
                    ),
                    "--state",
                    "before-review",
                    "--requirements",
                    str(requirements),
                    "--goal",
                    str(goal),
                    "--plan",
                    str(plan),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        self.assertEqual(control_guard.returncode, 0, control_guard.stdout + control_guard.stderr)
        self.assertEqual(orchestration_guard.returncode, 0, orchestration_guard.stdout + orchestration_guard.stderr)
