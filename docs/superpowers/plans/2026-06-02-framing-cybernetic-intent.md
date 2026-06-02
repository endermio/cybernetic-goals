# Framing Cybernetic Intent Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `framing-cybernetic-intent` as a pre-task collaborative intent-framing skill before routing.

**Architecture:** The new skill lives beside the existing cybernetic skills and stays semantic/conversational, with no scripts in the first version. Repository integration is structural: README workflow, router and requirements boundaries, invariant matrix, manifest, evals, template, and focused regression tests.

**Tech Stack:** Markdown skills and docs, JSON eval files, YAML agent metadata, Python `unittest` for structural regression coverage.

---

## File Structure

- Create: `.agents/skills/framing-cybernetic-intent/SKILL.md`
  - Defines trigger conditions, collaborative process, output contract, persistence boundary, and handoff rules.
- Create: `.agents/skills/framing-cybernetic-intent/agents/openai.yaml`
  - Matches local skill metadata pattern.
- Create: `.agents/skills/framing-cybernetic-intent/assets/intent-frame-template.md`
  - Optional persistent intent brief template for hybrid persistence.
- Create: `.agents/skills/framing-cybernetic-intent/evals/evals.json`
  - Semantic evals for method-goal confusion, dissatisfaction, failure experience, unstable intent, chat-only default, and optional persistence.
- Create: `tests/skills/test_intent_framing.py`
  - Structural tests that fail before the implementation and pass afterward.
- Modify: `README.md`
  - Adds pre-task layer to recommended workflow and included skill list.
- Modify: `.agents/skills/routing-cybernetic-workflows/SKILL.md`
  - Clarifies that routing receives formed tasks and hands pre-task input to intent framing.
- Modify: `.agents/skills/analyzing-cybernetic-requirements/SKILL.md`
  - Clarifies that requirements analysis receives formed tasks and does not absorb collaborative intent framing.
- Modify: `docs/cybernetic-framework/invariant-artifact-consumer-matrix.md`
  - Adds `INV-INT-001`.
- Modify: `MANIFEST.txt`
  - Adds the new skill files and the new focused test.

---

### Task 1: Add Failing Intent-Framing Structural Tests

**Files:**
- Create: `tests/skills/test_intent_framing.py`

- [ ] **Step 1: Write the failing test file**

Create `tests/skills/test_intent_framing.py` with this content:

```python
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = ROOT / ".agents/skills/framing-cybernetic-intent"


class IntentFramingSkillTest(unittest.TestCase):
    def read(self, path: str) -> str:
        return (ROOT / path).read_text(encoding="utf-8")

    def test_skill_metadata_and_core_boundary_exist(self):
        skill = self.read(".agents/skills/framing-cybernetic-intent/SKILL.md")

        self.assertIn("name: framing-cybernetic-intent", skill)
        self.assertIn("pre-task", skill.casefold())
        self.assertIn("collaborative intent framing", skill.casefold())
        self.assertIn("Shared Intent Understanding", skill)
        self.assertIn("method", skill.casefold())
        self.assertIn("purpose", skill.casefold())
        self.assertIn("must not", skill.casefold())
        self.assertIn("routing-cybernetic-workflows", skill)

    def test_template_preserves_shared_understanding_not_requirements(self):
        template = self.read(
            ".agents/skills/framing-cybernetic-intent/assets/intent-frame-template.md"
        )
        template_text = template.casefold()

        self.assertIn("shared intent understanding", template_text)
        self.assertIn("human situation", template_text)
        self.assertIn("method vs purpose", template_text)
        self.assertIn("uncertainty to reduce", template_text)
        self.assertIn("what not to assume yet", template_text)
        self.assertIn("optional task formation", template_text)
        self.assertNotIn("Execution Policy", template)
        self.assertNotIn("Runtime /goal", template)

    def test_agent_metadata_and_manifest_include_new_skill_files(self):
        metadata = self.read(
            ".agents/skills/framing-cybernetic-intent/agents/openai.yaml"
        )
        manifest = self.read("MANIFEST.txt")

        self.assertIn("allow_implicit_invocation: false", metadata)
        for path in (
            ".agents/skills/framing-cybernetic-intent/SKILL.md",
            ".agents/skills/framing-cybernetic-intent/agents/openai.yaml",
            ".agents/skills/framing-cybernetic-intent/assets/intent-frame-template.md",
            ".agents/skills/framing-cybernetic-intent/evals/evals.json",
            "tests/skills/test_intent_framing.py",
        ):
            self.assertIn(path, manifest)

    def test_evals_cover_pre_task_failure_modes(self):
        evals = json.loads(
            self.read(".agents/skills/framing-cybernetic-intent/evals/evals.json")
        )
        ids = {item["id"] for item in evals["evals"]}

        self.assertIn("method-preference-is-not-purpose", ids)
        self.assertIn("dissatisfaction-is-not-execution-task", ids)
        self.assertIn("failure-experience-is-not-repair-goal", ids)
        self.assertIn("unstable-intent-asks-one-question", ids)
        self.assertIn("shared-understanding-before-task-candidate", ids)
        self.assertIn("chat-only-default-no-artifact", ids)
        self.assertIn("persistent-intent-brief-only-when-justified", ids)

    def test_readme_routes_human_situation_before_routing(self):
        readme = self.read("README.md")

        self.assertIn("human situation", readme)
        self.assertIn("framing-cybernetic-intent", readme)
        self.assertIn("shared intent understanding", readme.casefold())

    def test_router_hands_pre_task_input_to_intent_framing(self):
        router = self.read(".agents/skills/routing-cybernetic-workflows/SKILL.md")

        self.assertIn("framing-cybernetic-intent", router)
        self.assertIn("pre-task", router.casefold())
        self.assertIn("formed task", router.casefold())

    def test_requirements_skill_does_not_absorb_intent_framing(self):
        requirements = self.read(
            ".agents/skills/analyzing-cybernetic-requirements/SKILL.md"
        )

        self.assertIn("framing-cybernetic-intent", requirements)
        self.assertIn("formed task", requirements.casefold())
        self.assertIn("pre-task", requirements.casefold())

    def test_invariant_matrix_tracks_intent_framing(self):
        matrix = self.read("docs/cybernetic-framework/invariant-artifact-consumer-matrix.md")

        self.assertIn("INV-INT-001", matrix)
        self.assertIn("Pre-task intent", matrix)
        self.assertIn("framing-cybernetic-intent", matrix)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the focused test and verify it fails**

Run:

```bash
python3 -m unittest tests.skills.test_intent_framing
```

Expected: FAIL because `.agents/skills/framing-cybernetic-intent/SKILL.md` does not exist yet.

- [ ] **Step 3: Keep the failing test uncommitted**

Do not commit the intentionally failing test by itself. Keep it in the working
tree so the implementation can turn it green in the same bounded change.

---

### Task 2: Add The Intent-Framing Skill Files

**Files:**
- Create: `.agents/skills/framing-cybernetic-intent/SKILL.md`
- Create: `.agents/skills/framing-cybernetic-intent/agents/openai.yaml`
- Create: `.agents/skills/framing-cybernetic-intent/assets/intent-frame-template.md`
- Create: `.agents/skills/framing-cybernetic-intent/evals/evals.json`

- [ ] **Step 1: Create the skill directories**

Run:

```bash
mkdir -p .agents/skills/framing-cybernetic-intent/agents
mkdir -p .agents/skills/framing-cybernetic-intent/assets
mkdir -p .agents/skills/framing-cybernetic-intent/evals
```

- [ ] **Step 2: Write `SKILL.md`**

Create `.agents/skills/framing-cybernetic-intent/SKILL.md` with this content:

````markdown
---
name: framing-cybernetic-intent
description: 'Use before cybernetic workflow routing when user input is pre-task intent rather than a formed task: confusion, dissatisfaction, intuition, risk sense, observed symptoms, failed attempts, method preference, or distrust of the current process. Collaboratively frames human intent into shared understanding before optional task formation. Does not analyze requirements, choose workflow fit, write control artifacts, or execute target work.'
---

# Framing Cybernetic Intent

## Overview

Help the user and agent form shared intent understanding before the cybernetic
workflow treats anything as a task.

This skill handles the pre-task layer:

```text
human situation
-> collaborative intent framing
-> shared intent understanding
-> optional task formation
-> routing-cybernetic-workflows
```

It is not a router, requirements analyzer, planner, reviewer, or executor.

## Core Boundary

This skill must not:

- analyze full requirements semantics;
- decide workflow fit;
- treat a user-selected method, skill, workflow, or tool as the human purpose;
- turn confusion, dissatisfaction, risk sense, failed experience, or process
  distrust directly into an execution task;
- force every vague input into a task candidate;
- write requirements, solution designs, goal contracts, execution policies,
  control reviews, progress logs, or runtime `/goal` commands;
- create persistent artifacts for routine clarification.

This skill may:

- reflect the user's situation without prematurely taskifying it;
- separate purpose, method, symptom, constraint, risk, uncertainty, and failure
  experience;
- identify what uncertainty the user appears to want reduced;
- state what should not be assumed yet;
- ask one high-value question when intent is unstable;
- summarize shared intent understanding;
- optionally form a task candidate only after the shared intent is clear;
- optionally write an intent brief when persistence is justified or requested.

## Trigger Signals

Use this skill when the input is not yet a formed task. Common signals:

- confusion: "I do not know what is wrong";
- dissatisfaction: "This workflow feels wrong";
- intuition: "This seems overcontrolled";
- risk sense: "This may explode context";
- observed symptoms: "The agent keeps writing plans";
- failure experience: "Last time this did not converge";
- method preference: "Use the full cybernetic workflow";
- process distrust: "I do not trust the current pipeline".

Do not use this skill for clearly formed low-risk tasks unless the user also
expresses unclear intent, process distrust, or method-goal confusion.

## Process

1. Reflect the human situation in neutral language.
2. Separate purpose, method, symptom, constraint, risk, and uncertainty.
3. Identify the uncertainty the user seems to want reduced.
4. State what should not be assumed yet.
5. Ask at most one high-value question when the intent is still unstable.
6. Summarize shared intent understanding once it is clear enough.
7. Offer possible next moves without treating any one move as mandatory.

Ask concise questions. Do not interview the user for routine execution details.
The loop ends at shared understanding, not at artifact production.

## Default Output

Use this chat-only shape by default:

```text
Shared Intent Understanding
- Human situation:
- Apparent purpose:
- Method vs purpose distinction:
- Symptoms or failure experience:
- Risk or uncertainty to reduce:
- What not to assume yet:
- Current best next move:
```

Allowed next moves include:

- continue intent framing;
- make a judgment or decision;
- design a small experiment;
- perform a bounded inspection;
- hand off to `$routing-cybernetic-workflows`;
- hand off to `$analyzing-cybernetic-requirements`;
- stop because the user purpose is not yet stable.

## Optional Task Formation

Only include a task candidate after shared intent is clear.

```text
Optional Task Candidate
- Task statement:
- Why this task follows from the shared intent:
- Known non-goals:
- Recommended handoff:
```

If the next step is routing, keep the handoff response-only:

```text
$routing-cybernetic-workflows <clear task statement>
```

Do not write this command into requirements, design, goal, plan, review,
progress, or orchestration artifacts.

## Persistence Rule

Default to no file write.

Write an intent brief only when one of these is true:

- the intent frame will affect long-lived control artifacts;
- the same unresolved intent is likely to recur;
- the user asks to record the framing;
- future routing or requirements analysis needs a stable record of the shared
  intent.

When persistence is justified, use:

```text
docs/cybernetics/intents/YYYY-MM-DD-<slug>.md
```

Use `assets/intent-frame-template.md`.

The intent brief preserves shared understanding and optional handoff only. It
must not contain full requirements, solution design, execution policy, control
review, or runtime goal content.

## Common Mistakes

- Treating "use this workflow" as the user's goal.
- Responding to dissatisfaction by creating a repair goal.
- Responding to failed experience by rerunning the same workflow.
- Producing requirements before clarifying what the user wants changed.
- Treating artifact creation as evidence that intent is clear.
````

- [ ] **Step 3: Write `agents/openai.yaml`**

Create `.agents/skills/framing-cybernetic-intent/agents/openai.yaml` with this content:

```yaml
policy:
  allow_implicit_invocation: false
```

- [ ] **Step 4: Write `assets/intent-frame-template.md`**

Create `.agents/skills/framing-cybernetic-intent/assets/intent-frame-template.md` with this content:

````markdown
# Intent Frame: [Name]

## Intent Frame Status

Status: `Draft`

## Human Situation

## Apparent Purpose

## Method vs Purpose

## Symptoms or Failure Experience

## Risk or Uncertainty to Reduce

## What Not To Assume Yet

## Shared Intent Understanding

## Optional Task Formation

### Task Statement

### Why This Follows From Shared Intent

### Known Non-Goals

### Recommended Handoff

## Persistence Justification
````

- [ ] **Step 5: Write `evals/evals.json`**

Create `.agents/skills/framing-cybernetic-intent/evals/evals.json` with this content:

```json
{
  "evals": [
    {
      "id": "method-preference-is-not-purpose",
      "prompt": "Use the full cybernetic workflow for this because I do not trust the current process.",
      "expected_output": "The skill distinguishes the requested workflow as a method preference, frames the underlying distrust and uncertainty, and does not start routing or requirements analysis.",
      "assertions": [
        "States that the workflow is a possible method, not the human purpose.",
        "Identifies process distrust as the human situation.",
        "Asks what uncertainty or risk the user wants reduced if intent is unstable.",
        "Does not create requirements, design, goal, execution policy, or review artifacts.",
        "Does not hand off to routing until the intended change is clear."
      ]
    },
    {
      "id": "dissatisfaction-is-not-execution-task",
      "prompt": "This plan feels wrong and too heavy.",
      "expected_output": "The skill reflects dissatisfaction as pre-task intent and helps clarify what feels wrong before proposing any task.",
      "assertions": [
        "Does not turn the complaint into an immediate repair task.",
        "Separates symptom from purpose.",
        "Identifies possible uncertainty about control weight or fit.",
        "Asks at most one high-value clarification question.",
        "Uses Shared Intent Understanding as the default output shape."
      ]
    },
    {
      "id": "failure-experience-is-not-repair-goal",
      "prompt": "Last time this workflow generated many artifacts and did not converge.",
      "expected_output": "The skill frames the failed experience and risk before forming any repair goal.",
      "assertions": [
        "Recognizes the input as failure experience.",
        "Does not immediately recommend rerunning the workflow.",
        "Does not create a repair goal by default.",
        "Identifies convergence, artifact volume, or control fit as uncertainty to reduce.",
        "Offers possible next moves without making one mandatory."
      ]
    },
    {
      "id": "unstable-intent-asks-one-question",
      "prompt": "Something is off here. Maybe use the orchestrator.",
      "expected_output": "The skill separates the vague concern from the suggested method and asks one small question about what the user wants clarified or changed.",
      "assertions": [
        "Does not assume orchestrator use is the goal.",
        "Reflects that the intent is not yet stable.",
        "Asks one concise question.",
        "Does not ask several routine execution questions.",
        "Does not start workflow routing."
      ]
    },
    {
      "id": "shared-understanding-before-task-candidate",
      "prompt": "I think we are optimizing process completeness instead of my purpose.",
      "expected_output": "The skill first summarizes shared intent understanding and only then, if clear, offers an optional task candidate.",
      "assertions": [
        "Names the method-goal confusion.",
        "Summarizes the apparent purpose.",
        "States what should not be assumed yet.",
        "Keeps any task candidate optional.",
        "Explains why any task candidate follows from the shared intent."
      ]
    },
    {
      "id": "chat-only-default-no-artifact",
      "prompt": "Help me understand why this feels overcontrolled.",
      "expected_output": "The skill responds in chat with shared intent framing and does not write files by default.",
      "assertions": [
        "Uses a chat-only shared understanding response.",
        "Does not create an intent brief by default.",
        "Does not create requirements, design, goal, plan, review, or runtime goal artifacts.",
        "Clarifies the control concern.",
        "Offers a bounded next move only if useful."
      ]
    },
    {
      "id": "persistent-intent-brief-only-when-justified",
      "prompt": "This intent framing will guide several future control artifacts; record it before we proceed.",
      "expected_output": "The skill may write an intent brief because persistence is explicitly justified, while keeping it limited to shared understanding and optional handoff.",
      "assertions": [
        "Uses docs/cybernetics/intents/YYYY-MM-DD-<slug>.md when writing.",
        "States why persistence is justified.",
        "Preserves shared intent understanding.",
        "Does not include full requirements or execution policy content.",
        "Keeps any downstream handoff optional and response-oriented."
      ]
    }
  ]
}
```

- [ ] **Step 6: Run the focused test**

Run:

```bash
python3 -m unittest tests.skills.test_intent_framing
```

Expected: FAIL because README, router, requirements skill, invariant matrix,
and MANIFEST are not updated yet.

- [ ] **Step 7: Optional checkpoint commit for the new skill files**

If using checkpoint commits, run this after the focused test has produced the
expected failure for only the remaining integration files:

```bash
git add .agents/skills/framing-cybernetic-intent
git commit -m "Add intent framing skill"
```

---

### Task 3: Update Workflow Documentation And Skill Boundaries

**Files:**
- Modify: `README.md`
- Modify: `.agents/skills/routing-cybernetic-workflows/SKILL.md`
- Modify: `.agents/skills/analyzing-cybernetic-requirements/SKILL.md`

- [ ] **Step 1: Update the README workflow**

In `README.md`, after the opening code block that defines the core idea, add:

````markdown
Human input does not always arrive as a formed task. For pre-task intent such
as confusion, dissatisfaction, risk sense, failed experience, method preference,
or distrust of the current process, start from the human situation:

```text
human situation
  -> $framing-cybernetic-intent
  -> shared intent understanding
  -> optional task formation
  -> $routing-cybernetic-workflows
```

Only route formed tasks. Do not treat a requested method or workflow as the
human purpose.
````

Then change the recommended workflow block so it starts with:

```text
human situation
  -> when input is pre-task intent rather than a formed task

$framing-cybernetic-intent
  -> shared intent understanding
  -> optional task formation

$routing-cybernetic-workflows
  -> decide whether a formed task should use the cybernetic workflow
```

Then add this bullet to the included skills list:

```markdown
- `framing-cybernetic-intent`: collaboratively frame pre-task human intent into shared understanding before optional task formation and routing.
```

- [ ] **Step 2: Update router metadata and overview**

In `.agents/skills/routing-cybernetic-workflows/SKILL.md`, replace the frontmatter description with:

```yaml
description: 'Use first for formed tasks when deciding whether the task should use the cybernetic workflow. If user input is pre-task intent such as confusion, dissatisfaction, risk sense, failed experience, method preference, or process distrust, hand off to framing-cybernetic-intent before routing. Classifies formed tasks by control uncertainty and required gates: direct prompt, inline goal, bounded file goal, Design Gate, Rubric Gate, full pre-goal pipeline, or high-risk human-gated workflow.'
```

In the Overview section, after "This skill is a router, not a planner, not a goal writer, not a requirements analyzer, and not an executor.", add:

```markdown
It routes formed tasks. It does not collaboratively form the task from
pre-task intent. If the user input is primarily confusion, dissatisfaction,
risk sense, observed symptoms, failure experience, method preference, or
process distrust, hand off to `$framing-cybernetic-intent` before making a
workflow decision.
```

- [ ] **Step 3: Update requirements-analysis metadata and boundary**

In `.agents/skills/analyzing-cybernetic-requirements/SKILL.md`, replace the frontmatter description with:

```yaml
description: 'Use after a formed task exists and before solution design, control-contract writing, execution-policy writing, or controlled execution for complex, ambiguous, evaluative, or output-sensitive work. Analyzes human purpose, requirement semantics, controlled objects and boundaries, evaluation functions, output-contract needs, constraints, non-goals, safe defaults, blocking human decisions, and required gates. For pre-task intent such as confusion, dissatisfaction, risk sense, failed experience, method preference, or process distrust, use framing-cybernetic-intent first. Does not create solution designs, control contracts, execution policies, control reviews, runtime /goal commands, or target-work artifacts.'
```

In the Core Boundary section, after "This skill analyzes requirements.", add:

```markdown
It assumes a formed task exists. It must not absorb the pre-task responsibility
of collaboratively forming user intent from confusion, dissatisfaction, risk
sense, failed experience, method preference, or process distrust. Use
`$framing-cybernetic-intent` first when the setpoint is not yet clear.
```

- [ ] **Step 4: Run the focused test**

Run:

```bash
python3 -m unittest tests.skills.test_intent_framing
```

Expected: FAIL because the invariant matrix and MANIFEST are not updated yet.

- [ ] **Step 5: Optional checkpoint commit for documentation and boundary updates**

If using checkpoint commits, run this after the focused test has produced the
expected failure for only the remaining invariant or manifest updates:

```bash
git add README.md .agents/skills/routing-cybernetic-workflows/SKILL.md .agents/skills/analyzing-cybernetic-requirements/SKILL.md
git commit -m "Document pre-task intent framing"
```

---

### Task 4: Update Invariants And Manifest

**Files:**
- Modify: `docs/cybernetic-framework/invariant-artifact-consumer-matrix.md`
- Modify: `MANIFEST.txt`

- [ ] **Step 1: Add `INV-INT-001` to the invariant matrix**

In `docs/cybernetic-framework/invariant-artifact-consumer-matrix.md`, add this row near the start of the consumer matrix, before `INV-DES-001`:

```markdown
| INV-INT-001 | Pre-task intent must be collaboratively framed before workflow routing when user input is not yet a formed task or when method is being treated as goal. | `.agents/skills/framing-cybernetic-intent/SKILL.md`; `.agents/skills/routing-cybernetic-workflows/SKILL.md`; `.agents/skills/analyzing-cybernetic-requirements/SKILL.md` | `Shared Intent Understanding`; optional `docs/cybernetics/intents/*`; intent-frame template | N/A: semantic framing quality is eval-governed; router boundary text provides handoff rule | N/A: intent framing precedes control review; later reviews consume formed requirements only | router receives optional clear task candidate; requirements analysis receives formed task only | `tests/skills/test_intent_framing.py`; `.agents/skills/framing-cybernetic-intent/evals/evals.json` | Active |
```

- [ ] **Step 2: Update `MANIFEST.txt`**

Add these lines to `MANIFEST.txt` in sorted location with the other skill files and tests:

```text
.agents/skills/framing-cybernetic-intent/SKILL.md
.agents/skills/framing-cybernetic-intent/agents/openai.yaml
.agents/skills/framing-cybernetic-intent/assets/intent-frame-template.md
.agents/skills/framing-cybernetic-intent/evals/evals.json
tests/skills/test_intent_framing.py
```

- [ ] **Step 3: Run focused tests**

Run:

```bash
python3 -m unittest tests.skills.test_intent_framing
python3 -m unittest tests.skills.test_invariant_consumer_matrix
```

Expected: both commands pass.

- [ ] **Step 4: Optional checkpoint commit for invariant and manifest updates**

If using checkpoint commits, run this after the focused tests pass:

```bash
git add docs/cybernetic-framework/invariant-artifact-consumer-matrix.md MANIFEST.txt
git commit -m "Track intent framing invariant"
```

---

### Task 5: Full Verification And Final Commit State

**Files:**
- Verify all files changed in Tasks 1-4.

- [ ] **Step 1: Run syntax and JSON validation**

Run:

```bash
python3 -m json.tool .agents/skills/framing-cybernetic-intent/evals/evals.json >/tmp/framing-intent-evals.json
```

Expected: command exits 0.

- [ ] **Step 2: Run focused skill tests**

Run:

```bash
python3 -m unittest tests.skills.test_intent_framing tests.skills.test_invariant_consumer_matrix
```

Expected: tests pass with exit code 0.

- [ ] **Step 3: Run full unit suite**

Run:

```bash
python3 -m unittest
```

Expected: all tests pass with exit code 0.

- [ ] **Step 4: Check diff hygiene**

Run:

```bash
git diff --check
git status --short
```

Expected: `git diff --check` exits 0. `git status --short` shows only intentional tracked changes waiting for commit, or only unrelated untracked `__pycache__` directories after commits.

- [ ] **Step 5: Final review of behavior boundaries**

Run:

```bash
rg -n "framing-cybernetic-intent|pre-task|formed task|Shared Intent Understanding|method.*purpose|purpose.*method" README.md .agents/skills/framing-cybernetic-intent .agents/skills/routing-cybernetic-workflows/SKILL.md .agents/skills/analyzing-cybernetic-requirements/SKILL.md docs/cybernetic-framework/invariant-artifact-consumer-matrix.md tests/skills/test_intent_framing.py
```

Expected: output shows the new skill, README workflow, router handoff, requirements boundary, invariant row, evals, template, and tests.

- [ ] **Step 6: Commit any remaining verified implementation changes**

If checkpoint commits were skipped, run:

```bash
git add .agents/skills/framing-cybernetic-intent README.md .agents/skills/routing-cybernetic-workflows/SKILL.md .agents/skills/analyzing-cybernetic-requirements/SKILL.md docs/cybernetic-framework/invariant-artifact-consumer-matrix.md MANIFEST.txt tests/skills/test_intent_framing.py
git commit -m "Add intent framing skill"
```

If checkpoint commits were used and `git status --short` shows no tracked
changes, do not create an empty commit.

---

## Self-Review

- Spec coverage: the plan creates the independent skill, keeps default output chat-only, adds optional task formation, adds hybrid persistence, updates router and requirements boundaries, updates README, adds evals, updates invariant matrix, and adds structural tests.
- No unsupported scripts are introduced; the first version is conversational and semantic.
- Deterministic tests verify structure and handoff boundaries without pretending to judge conversation quality.
- The implementation is scoped to one bounded change and does not require live external services.
