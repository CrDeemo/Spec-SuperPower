---
name: spec-superpowers
description: >
  Orchestrates OpenSpec + planning-with-files + Superpowers into a unified spec-driven
  development workflow. Automatically triages complexity (light/full), recovers session
  context, manages task workspaces, and applies quality gates (G0-G3) with automated review
  loops at every stage. Use this skill when the user says "/spec-superpowers", "spec first",
  or starts any feature, bugfix, or refactor. Activate for any non-trivial code change to
  prevent skipping the design phase. Loosely coupled — uninstalling does not affect
  independent modules. Orchestrates: OpenSpec (OPSX) + planning-with-files + Superpowers
  (TDD, code review, verification, debugging, spec/plan review loops).
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
| `/spec-superpowers reset` | Reset complexity choice and state |
| `/spec-superpowers escalate` | Light → Full mid-workflow upgrade |
| `/spec-superpowers simplify` | Full → Light mid-workflow downgrade |
| `/spec-superpowers switch` | Switch to a different task workspace |

## Step 1: Dependency Check

Verify all three modules are available before proceeding. If any is missing, show install command and stop. Details: [references/integration-guide.md](references/integration-guide.md)

## Step 2: Task Router (Phase -1)

Check `.spec-tasks/_active.txt`:
- **Not found** → ask task name → create `.spec-tasks/<name>/` + `_active.txt` → proceed
- **Found** → read active task + root `task_plan.md` summary → ask user: continue / archive & new / switch existing

On switch/new: copy-swap root planning files with `.spec-tasks/` (real files, no symlinks). Details: [references/planning-workflow.md](references/planning-workflow.md)

## Step 3: Triage Complexity

AI suggests a level; user confirms or overrides.

| Level | When | Pipeline |
|-------|------|----------|
| **Light** | ≤2 files, no new API, no architecture change, <30 min | Simplified Phase 1-4 |
| **Full** | Any criterion above is false | All phases |

Mid-workflow: `/spec-superpowers escalate` (Light→Full) or `/spec-superpowers simplify` (Full→Light).

## Step 4: Execute the Pipeline

**Phase 0 — Session Recovery** (automatic)
If `task_plan.md` exists, run the 5-Question Reboot Test and resume from checkpoint.
**Gate G0**: Reboot test consistent + no context contradictions.
Details: [references/planning-workflow.md](references/planning-workflow.md)

**Phase 1 — Specification** (OpenSpec)
Full: `/opsx:explore` → `/opsx:propose` → `openspec validate` → user confirms.
Light: `/opsx:propose` → `openspec validate` → user confirms.
**Gate G1**: Validate passed + user confirmed + brainstorming review loop passed.
Details: [references/openspec-workflow.md](references/openspec-workflow.md)

**Phase 2 — Persistent Planning** (writing-plans → planning-with-files)
writing-plans authors plan content → written into task_plan.md (planning-with-files format).
planning-with-files hooks auto-manage attention from this point.
Generate task_plan.md / findings.md / progress.md. Each task: file paths + acceptance criteria + test strategy.
**Gate G2**: Three files ready + plan review loop passed.
Details: [references/planning-workflow.md](references/planning-workflow.md)

**Phase 3 — Implementation** (Superpowers)
Subagent-Driven or Executing-Plans. TDD throughout. Errors: 3-Strike → systematic-debugging.
**Gate G3**: All tests pass + review passed + evidence in progress.md.

**Phase 4 — Archive**
`finishing-a-development-branch` → update checkboxes → `openspec archive <change>` → copy-swap planning files back to `.spec-tasks/<task>/` → clean root.

## Sub-command Jump

- `/spec-superpowers spec` → Phase 1 only, stop at G1
- `/spec-superpowers plan` → Phase 2 only (requires spec in `openspec/`), stop at G2
- `/spec-superpowers impl` → Phase 3 + 4 (requires `task_plan.md`)

## Quality Gates

Hard stops — nothing proceeds until all checks pass. Full criteria: [references/quality-gates.md](references/quality-gates.md)

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
