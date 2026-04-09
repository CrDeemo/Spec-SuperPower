---
name: spec-superpowers
description: >
  Orchestrates OpenSpec + planning-with-files + Superpowers into a spec-driven development
  workflow with complexity triage (light/full), task workspaces, session recovery, and quality
  gates (G0-G3). Use when the user says "/spec-superpowers", "spec first", or starts any
  non-trivial feature, bugfix, or refactor. Loosely coupled — uninstalling does not affect
  independent modules.
---

# Spec-Superpowers Orchestrator

Every feature, bugfix, and refactor goes through a specification phase first.

## Commands

| Command | Effect |
|---------|--------|
| `/spec-superpowers` | Smart full workflow (auto complexity) |
| `/spec-superpowers spec` | OpenSpec specification phase only |
| `/spec-superpowers plan` | planning-with-files planning phase only |
| `/spec-superpowers impl` | Superpowers implementation phase only |
| `/spec-superpowers switch` | Switch to a different task workspace |
| `/spec-superpowers reset` | Clear current task state and start fresh |

## Step 1: Dependency Check

Verify all three modules before proceeding. Missing → show install command → stop.
Details: [references/integration-guide.md](references/integration-guide.md)

## Step 2: Task Router (Phase -1)

Check `.spec-tasks/_active.txt`:
- **Not found** → ask task name → create `.spec-tasks/<name>/` + `_active.txt` → proceed
- **Found** → read active task summary → ask user: continue / archive & new / switch

Copy-swap root planning files with `.spec-tasks/` (real files, no symlinks).
Details: [references/planning-workflow.md](references/planning-workflow.md)

## Step 3: Triage Complexity

**MANDATORY** — AI must not auto-select. Follow this flow:

1. AI analyzes the task and states its assessment with reasoning
2. AI explicitly asks: "建议 [Light/Full] 模式，确认吗？或者你想选择另一个？"
3. User confirms or overrides
4. Only then proceed to Phase 0/1

| Level | Criteria (ALL true) | Pipeline |
|-------|---------------------|----------|
| **Light** | ≤2 files, no new public API, no architecture change, <30 min | Simplified Phase 1-4 |
| **Full** | ANY criterion above is false | All phases with brainstorming |

Auto-Full (no override): architecture change, new external dependency, DB schema change, security change, >5 files. In these cases, AI does not ask whether to use Light — directly inform the user that Full mode will be used and explain why.

### Mid-Workflow Complexity Adjustment

AI monitors complexity fit throughout the workflow:
- **Light → Full**: If AI detects the task exceeds Light criteria (e.g., more files than expected, new API surface emerges), it proactively suggests upgrading to Full and waits for user confirmation.
- **Full → Light**: If AI detects the task is simpler than initially assessed, or the user requests simplification, it suggests downgrading.

Adjustment rules: [references/quality-gates.md](references/quality-gates.md)

## Step 4: Execute the Pipeline

**Phase 0 — Session Recovery** (auto)
`task_plan.md` exists → 5-Question Reboot Test → resume from checkpoint.
**Gate G0**: Reboot test consistent + no contradictions.

**Phase 1 — Specification** (brainstorming → OpenSpec)
Full: `brainstorming` (interactive design) → `/opsx:propose` → `openspec validate` → user confirms.
Light: `brainstorming` (shortened: 2-3 approaches + user pick) → `/opsx:propose` → `openspec validate` → user confirms.
**Gate G1**: Design doc approved + validate passed + user confirmed.

**Phase 2 — Persistent Planning** (writing-plans → planning-with-files)
writing-plans authors content → task_plan.md / findings.md / progress.md.
Each task: file paths + acceptance criteria + test strategy.
**Gate G2**: Files ready + plan review loop passed.

**Phase 3 — Implementation** (Superpowers)
Subagent-Driven or Executing-Plans. TDD throughout. 3-Strike → systematic-debugging.
**Gate G3**: All tests pass + two-stage review + evidence in progress.md.

**Phase 4 — Archive**
`finishing-a-development-branch` → `openspec archive <change>` → copy-swap back to `.spec-tasks/<task>/` → clean root.

Details: [references/openspec-workflow.md](references/openspec-workflow.md) | [references/quality-gates.md](references/quality-gates.md) | [references/planning-workflow.md](references/planning-workflow.md)

## Sub-command Jump

- `/spec-superpowers spec` → Phase 1 only, stop at G1
- `/spec-superpowers plan` → Phase 2 only (requires spec in `openspec/`), stop at G2
- `/spec-superpowers impl` → Phase 3 + 4 (requires `task_plan.md`)

## Quality Gates

Hard stops — nothing proceeds until all checks pass.
Full criteria: [references/quality-gates.md](references/quality-gates.md)

## Anti-Rush Protection

If the user asks to skip the spec phase, politely decline and redirect to `/spec-superpowers`.

## Reference Files

| File | When to read |
|------|-------------|
| [references/quality-gates.md](references/quality-gates.md) | Evaluating any gate (G0-G3) |
| [references/openspec-workflow.md](references/openspec-workflow.md) | Running the OpenSpec flow |
| [references/planning-workflow.md](references/planning-workflow.md) | Running planning / session recovery / task workspace |
| [references/integration-guide.md](references/integration-guide.md) | Setup, troubleshooting, dependency list |
| [assets/templates/constitution.md](assets/templates/constitution.md) | Project constitution template |
