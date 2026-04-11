---
name: spec-superpowers
description: >
  Orchestrates OpenSpec + planning-with-files + Superpowers into a dialogue-first,
  spec-driven development workflow. Understand the user's intent through brainstorming
  before any process step. Use when the user says "/ssp", "spec first", or starts any
  non-trivial feature, bugfix, or refactor. Loosely coupled — uninstalling does not
  affect independent modules.
---

# Spec-Superpowers

先理解，再规范，再实现。对话是起点，不是流程是起点。

## Commands

| Command | Effect |
|---------|--------|
| `/ssp` | Full workflow — dialogue-first, auto complexity |
| `/ssp:design` | Dialogue exploration + OpenSpec specification only |
| `/ssp:plan` | Planning phase only |
| `/ssp:impl` | Implementation phase only |
| `/ssp:switch` | Switch to a different task workspace |
| `/ssp:clean` | Clean up archived tasks and stale workflow artifacts |
| `/ssp:reset` | Clear current task state and start fresh |

## Step 1: Understand — Dialogue-First Exploration

This is the soul of the entire workflow. Before any process operation, enter brainstorming dialogue.

**MANDATORY**: Invoke the `brainstorming` skill and follow its full process:

- **One question at a time** — never list multiple questions in one message
- **Prefer multiple choice** — lower cognitive burden for the user
- **Understand purpose before solutions** — "What problem are you solving?" before "What tech do you want?"
- **Propose 2-3 approaches with trade-offs** — don't present a single take-it-or-leave-it plan
- **Present design in sections, confirm each** — don't dump a full design document at once

⚠️ Do NOT proceed to Step 2 until the user has explicitly approved the design.

Brainstorming is **NEVER** shortened for Light mode — understanding the user has no abbreviated version. Only Quick mode uses brief confirmation (2-3 sentences stating what/why/scope, user confirms).

## Step 2: Triage — Post-Dialogue Complexity

After brainstorming, complexity is evident. AI states assessment with reasoning, then asks:
"建议 [Quick/Light/Full] 模式，确认吗？或者你想选择另一个？"

| Level | Criteria (ALL true) | Pipeline |
|-------|---------------------|----------|
| **Quick** | Single file, no new API, internal-only, <15 min | No OpenSpec, no planning files, implement directly |
| **Light** | ≤2 files, no new public API, no architecture change, <30 min | OpenSpec + task_plan.md + minimal progress.md |
| **Full** | ANY above is false | OpenSpec + all planning files + full review |

Auto-Full (no override): architecture change, new external dependency, DB schema change, security change, >5 files.
Mid-workflow adjustment: [references/quality-gates.md](references/quality-gates.md)

## Step 3: Formalize — OpenSpec Specification (Light/Full only)

Quick mode skips this step entirely — inline spec from Step 1 is sufficient.

Approved design → `/opsx:propose` → `openspec validate` → user confirms final spec.
**Gate G1**: Design doc approved + validate passed + user confirmed.
Details: [references/openspec-workflow.md](references/openspec-workflow.md)

## Step 4: Plan — Persistent Planning (Light/Full only)

`writing-plans` authors content → task_plan.md / findings.md (Full) / progress.md.
Each task: file paths + acceptance criteria + test strategy.
**Gate G2**: Files ready + plan review loop passed.
Details: [references/planning-workflow.md](references/planning-workflow.md)

## Step 5: Build — Implementation

Subagent-Driven or Executing-Plans. TDD throughout. 3-Strike → systematic-debugging.
**Gate G3**: All tests pass + two-stage review + evidence in progress.md.

## Step 6: Archive

`finishing-a-development-branch` → `openspec archive <change>` (Light/Full) → copy-swap back to `.spec-tasks/<task>/` → clean root.

## Quick Mode Shortcut

After Step 1 (brief 2-3 sentence confirmation), skip Steps 3-4. Implement → light review → clear `_active.txt`.
**Gate G1-Quick**: User confirmed inline spec. **Gate G3-Quick**: Tests pass + single-round review.

## Sub-command Jump

- `/ssp:design` → Step 1 + 2 + 3, stop at G1
- `/ssp:plan` → Step 4 only (requires spec in `openspec/`), stop at G2
- `/ssp:impl` → Step 5 + 6 (requires `task_plan.md`)
- `/ssp:clean` → Interactive cleanup wizard. Details: [references/integration-guide.md](references/integration-guide.md)

## Auto Behaviors (silent — don't interrupt dialogue)

- **Dependency check**: Verify OpenSpec CLI + planning-with-files + Superpowers at startup. Missing → show install → stop.
- **Task Router**: Check `.spec-tasks/_active.txt`. Found → silently restore context, brief status message, then respond to user. Not found → create workspace after brainstorming completes (task name from conversation).
- **Session Recovery**: `task_plan.md` exists → 5-Question Reboot Test → resume. Details: [references/planning-workflow.md](references/planning-workflow.md)

## Quality Gates

Hard stops — nothing proceeds until all checks pass.
Full criteria: [references/quality-gates.md](references/quality-gates.md)

## Reference Files

| File | When to read |
|------|-------------|
| [references/quality-gates.md](references/quality-gates.md) | Evaluating any gate (G0-G3) |
| [references/openspec-workflow.md](references/openspec-workflow.md) | Running the OpenSpec flow |
| [references/planning-workflow.md](references/planning-workflow.md) | Running planning / session recovery / task workspace |
| [references/integration-guide.md](references/integration-guide.md) | Setup, troubleshooting, dependency list |
| [assets/templates/constitution.md](assets/templates/constitution.md) | Project constitution template |
