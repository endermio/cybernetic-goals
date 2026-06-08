---
name: cybernetic-superpowers-infrastructure
description: 'Use when a cybernetic skill must choose required Superpowers substrate for planning, independent review, runtime execution, debugging, or completion verification.'
---

# Cybernetic Superpowers Infrastructure

## Overview

This skill defines how cybernetic skills depend on Superpowers skills.

Cybernetic skills compile control structures. Superpowers skills provide the behavior substrate for planning, independent review discipline, execution, debugging, and completion verification.

Use `references/superpowers-infrastructure-policy.md`.

## Core Rule

Superpowers are infrastructure dependencies, not optional style suggestions.

When a required substrate applies:

- invoke the substrate, or load and follow its `SKILL.md` instructions when direct invocation is unavailable;
- record the substrate status in the produced artifact;
- do not silently replace it with ad hoc behavior from the current cybernetic skill;
- do not treat merely mentioning the substrate, citing it, or imitating generic behavior as sufficient;
- if the substrate is unavailable, stop and report the missing infrastructure.

Approval requires a final observer pass after the last substantive mutation to the reviewed control artifacts, including required solution design. An older review result must not be transferred to a changed control structure unless the change is deterministic-only and guard-covered.

Pre-goal review subagents require explicit authorization in the orchestration request. Runtime target-work subagents are authorized only when the final `/goal` explicitly contains the approved subagent-driven execution topology and the user launches that `/goal`; parallel runtime subagents still require explicit human approval recorded in the execution policy and control review.

## Stage Summary

| Stage | Superpowers substrate | Required? |
|---|---|---|
| Exploratory requirements analysis | `$superpowers:brainstorming` | Optional |
| Exploratory solution design | `$superpowers:brainstorming` | Optional |
| Non-trivial execution policy generation | `$superpowers:writing-plans` | Required |
| Control review approval | Independent subagent review discipline | Required for `Approved` unless explicit human approval exists |
| Runtime execution | `$superpowers:executing-plans` discipline | Required |
| Runtime target-work delegation | Approved bounded subagent delegation protocol | Required when execution policy selects serial or parallel subagent-driven topology |
| Runtime serial implementation-plan delegation | `$superpowers:subagent-driven-development` discipline | Conditional: use only when the approved execution policy records `Selected agent workflow: superpowers-subagent-driven-development`, `Subagent execution mode: serial-single-active`, and `Max concurrent subagents: 1` |
| Runtime parallel independent-domain delegation | `$superpowers:dispatching-parallel-agents` discipline | Conditional: use only when the approved execution policy records `Selected agent workflow: superpowers-dispatching-parallel-agents`, `Subagent execution mode: parallel-max-safe`, and approved wave/lock/barrier/integration rules |
| Unclear or repeated runtime failure | `$superpowers:systematic-debugging` | Required |
| Completion claim | `$superpowers:verification-before-completion` | Required |

## Non-Goals

This skill does not:

- write goal contracts;
- write execution policies;
- perform control review;
- compile runtime `/goal` commands;
- execute target work.

It only supplies the shared infrastructure policy those skills must obey.
