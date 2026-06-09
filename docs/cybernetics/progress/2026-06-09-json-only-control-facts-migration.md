# Progress: JSON-only Control Facts Migration Pre-goal

## 2026-06-09 pre-goal compile

- checkpoint: pre-goal chain compiled from approved requirements
- files changed:
  - requirements approval updated for final high-concurrency runtime execution
  - design/goal/plan/review/runtime artifacts created
  - guard scripts updated to read current white-label fields
  - tests updated from old report/concurrency labels to current white-label fields
- commands run:
  - `python3 .agents/skills/orchestrating-cybernetic-pregoal/scripts/orchestration_guard.py --state before-runtime-compile ...`
  - `python3 .agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py ...`
  - `python3 .agents/skills/compiling-cybernetic-runtime-goals/scripts/compile_runtime_goal.py ... --expect-work-assignment parallel --expect-subagent-mode parallel-max-safe`
  - `python3 scripts/lint_cybernetic_artifact_hygiene.py ...`
  - `python3 -m pytest tests/skills -q`
  - `python3 -m py_compile ...`
  - `python3 -m json.tool docs/cybernetics/runs/2026-06-09-json-only-control-facts-migration/requirements.control.json`
  - `git diff --check`
- result:
  - orchestration guard: PASS
  - control-chain guard: PASS
  - runtime compiler: PASS
  - runtime execution mode assertion: parallel / parallel-max-safe
  - artifact hygiene: PASS with soft size warnings
  - skills tests: 148 passed, 78 subtests passed
- current risk:
  - target implementation has not started; current runtime artifact is the approved pointer for the next `/goal`
  - recording-cybernetic-run-outcomes could not persist metadata because its referenced script is missing from the skill directory

## 2026-06-09 runtime Wave 1 integration

- checkpoint: Wave 1 high-concurrency subagent outputs integrated at main-agent barrier
- execution mode:
  - `Parallel subagent-driven`
  - `superpowers-dispatching-parallel-agents`
  - `parallel-max-safe`
- wave packages integrated:
  - WP1 schema/registry foundation:
    - added strict control JSON schemas for requirements, design, goal, plan, review, runtime, progress events, and final reports
    - normalized delegation workflow registry key to `allowed_work_assignment`
  - WP2 runtime JSON operation skill:
    - added `.agents/skills/using-control-json/`
    - documented approved JSON read-only rules, runtime writable files, progress JSONL observations, verifier-gated completion, and short `/goal` adapter role
  - WP5a regression inventory:
    - added JSON-only regression inventory fixture covering old accident classes to port
- integration fixes:
  - updated `MANIFEST.txt` for new release-place files
  - removed generated Python cache directories from test runs
- commands run:
  - `python3 -m unittest tests.skills.test_control_json_schemas`
  - `python3 -m unittest tests.skills.test_using_control_json_protocol`
  - `python3 -m unittest tests.skills.test_json_control_regression_inventory`
  - `python3 -m unittest tests.skills.test_skill_repository_integrity`
- result:
  - schema foundation tests: PASS
  - using-control-json protocol tests: PASS
  - regression inventory tests: PASS
  - repository integrity manifest test: PASS
- current risk:
  - Wave 1 is foundation only; official guard/compiler/runtime JSON-only conversion is not yet complete
  - verifier implementation and Markdown official-input rejection remain for later waves

## 2026-06-09 runtime Wave 2 integration

- checkpoint: JSON official guard/compiler/runtime operation integrated at main-agent barrier
- execution mode:
  - `Parallel subagent-driven`
  - `superpowers-dispatching-parallel-agents`
  - `parallel-max-safe`
- wave packages integrated:
  - WP3 JSON guard/compiler path:
    - replaced official runtime guard and compiler inputs with `--run-dir`
    - hard-rejected legacy Markdown official inputs
    - replaced orchestration guard with a JSON-only wrapper over the control-chain guard
    - replaced handoff predictor with JSON run directory / `requirements.control.json` prediction
  - WP4 template hard-cut:
    - deauthorized Markdown control templates as official control artifacts
    - added JSON example control assets
    - updated template hard-cut regression tests
  - WP5 runtime verifier:
    - added JSON runtime operation scripts
    - added append-only progress JSONL validation
    - added verifier-gated final-report checks
- commands run:
  - `python3 -m unittest tests.skills.test_json_official_guard_compiler_path tests.skills.test_runtime_json_progress_verifier tests.skills.test_control_json_schemas`
  - `python3 -m py_compile .agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py .agents/skills/compiling-cybernetic-runtime-goals/scripts/compile_runtime_goal.py .agents/skills/orchestrating-cybernetic-pregoal/scripts/orchestration_guard.py .agents/skills/analyzing-cybernetic-requirements/scripts/predict_pregoal_handoff.py .agents/skills/using-control-json/scripts/*.py`
  - `python3 -m unittest discover -s tests`
- result:
  - focused JSON guard/compiler/runtime tests: PASS
  - py_compile: PASS
  - full tests: PASS

## 2026-06-09 runtime Wave 3 integration

- checkpoint: hot-path documentation cleanup integrated and stale old runtime-goal teaching removed
- execution mode:
  - `Parallel subagent-driven`
  - `superpowers-dispatching-parallel-agents`
  - `parallel-max-safe`
- wave package integrated:
  - WP5 docs/hot-path cleanup:
    - updated README, skill docs, evals, and invariant matrix to point at `docs/cybernetics/runs/<slug>/*.control.json`
    - updated control rules to teach `/goal Execute the runtime control JSON at ... using .agents/skills/using-control-json`
    - updated hot-path tests to reject `.goal.md` and old runtime-goal-file wording
- integration fixes:
  - removed remaining Markdown path from clarifying alias asset
  - removed old Markdown source paths from the JSON regression inventory
  - added predictor `--run-dir` support to match the skill instruction
- commands run:
  - `rg -n "docs/cybernetics/(requirements|designs|goals|plans|control-reviews)/|docs/cybernetics/runtime-goals/|\\.goal\\.md|runtime goal file|Target Skeleton|Skeleton node|Target-Producing Spine|Spine node\\(s\\)" README.md .agents/skills docs/cybernetic-framework tests -g '!docs/cybernetics/**' -g '!**/__pycache__/**'`
  - `python3 -m unittest tests.skills.test_json_control_regression_inventory tests.skills.test_skill_hot_path_compression`
  - `python3 -m unittest discover -s tests`
- result:
  - hot-path scan: PASS except intentional negative-test strings and script rejection lists
  - hot-path tests: PASS
  - full tests: PASS

## 2026-06-09 runtime JSON control run

- checkpoint: actual JSON-only runtime control run created and verified
- run directory:
  - `docs/cybernetics/runs/2026-06-09-json-only-control-facts-migration/`
- JSON control files:
  - `requirements.control.json`
  - `design.control.json`
  - `goal.control.json`
  - `plan.control.json`
  - `review.control.json`
  - `runtime.control.json`
  - `progress.jsonl`
  - `runtime-status.json`
  - `final-report.json`
- commands run:
  - `python3 .agents/skills/using-control-json/scripts/validate_control_chain.py docs/cybernetics/runs/2026-06-09-json-only-control-facts-migration`
  - `python3 .agents/skills/using-control-json/scripts/verify_runtime_progress.py docs/cybernetics/runs/2026-06-09-json-only-control-facts-migration`
  - `python3 .agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py --run-dir docs/cybernetics/runs/2026-06-09-json-only-control-facts-migration`
  - `python3 .agents/skills/compiling-cybernetic-runtime-goals/scripts/compile_runtime_goal.py --run-dir docs/cybernetics/runs/2026-06-09-json-only-control-facts-migration`
  - `python3 .agents/skills/analyzing-cybernetic-requirements/scripts/predict_pregoal_handoff.py --run-dir docs/cybernetics/runs/2026-06-09-json-only-control-facts-migration`
- result:
  - control JSON validation: PASS
  - runtime progress verifier: PASS, `goal_achieved_permitted: true`
  - control-chain guard: PASS
  - runtime compiler: PASS and emitted short `/goal` pointer to `runtime.control.json`
  - predictor: PASS and predicted `runtime.control.json`

## 2026-06-09 final verification

- checkpoint: final main-agent verification after all subagent waves and integration fixes
- commands run:
  - `python3 -m unittest discover -s tests`
  - `python3 -m py_compile .agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py .agents/skills/compiling-cybernetic-runtime-goals/scripts/compile_runtime_goal.py .agents/skills/orchestrating-cybernetic-pregoal/scripts/orchestration_guard.py .agents/skills/analyzing-cybernetic-requirements/scripts/predict_pregoal_handoff.py .agents/skills/using-control-json/scripts/control_json_runtime.py .agents/skills/using-control-json/scripts/validate_control_chain.py .agents/skills/using-control-json/scripts/append_progress_event.py .agents/skills/using-control-json/scripts/verify_runtime_progress.py .agents/skills/using-control-json/scripts/build_runtime_prompt.py`
  - `python3 -m json.tool` over control schemas, run JSON files, JSON examples, registries, and fixtures
  - `python3 .agents/skills/using-control-json/scripts/validate_control_chain.py docs/cybernetics/runs/2026-06-09-json-only-control-facts-migration`
  - `python3 .agents/skills/using-control-json/scripts/verify_runtime_progress.py docs/cybernetics/runs/2026-06-09-json-only-control-facts-migration`
  - `python3 .agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py --run-dir docs/cybernetics/runs/2026-06-09-json-only-control-facts-migration`
  - `python3 .agents/skills/compiling-cybernetic-runtime-goals/scripts/compile_runtime_goal.py --run-dir docs/cybernetics/runs/2026-06-09-json-only-control-facts-migration`
  - `git diff --check`
- result:
  - tests: PASS, 150 tests
  - py_compile: PASS
  - JSON syntax: PASS
  - runtime control validation: PASS
  - runtime progress verifier: PASS, `goal_achieved_permitted: true`
  - control-chain guard: PASS
  - runtime compiler: PASS
  - diff whitespace check: PASS
