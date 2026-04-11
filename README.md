# spec-superpowers

English | [中文](./README.zh-CN.md)

A Cursor Agent Skill that orchestrates **OpenSpec** + **planning-with-files** + **Superpowers** into a dialogue-first, spec-driven development workflow.

**Dialogue first**: understand the user's intent through brainstorming before any process step. Loosely coupled — uninstalling this skill does not affect the three independent modules.

---

## Quick Install

In your project root:

```bash
# One-click (macOS / Linux)
curl -sSL https://raw.githubusercontent.com/CrDeemo/Spec-SuperPower/main/install.sh | bash

# One-click (Windows PowerShell)
irm https://raw.githubusercontent.com/CrDeemo/Spec-SuperPower/main/install.ps1 | iex
```

Or step by step:

```bash
# 1. Install OpenSpec CLI (global, it's a CLI tool)
npm install -g @fission-ai/openspec@latest

# 2. Install spec-superpowers skill (project-level)
npx skills add CrDeemo/Spec-SuperPower --skill ssp --agent cursor --yes

# 3. Install planning-with-files skill (project-level)
npx skills add OthmanAdi/planning-with-files --agent cursor --yes

# 4. Install Superpowers via Cursor plugin marketplace (includes sub-skills)

# 5. (Optional) Copy gatekeeper rule to your project
mkdir -p .cursor/rules
cp .cursor/skills/spec-superpowers/.cursor/00-spec-superpowers.mdc .cursor/rules/
```

After installation, restart Cursor and type `/ssp` in Agent chat.

## Uninstall

```bash
# Remove spec-superpowers only (other modules keep working)
npx skills remove ssp

# Remove gatekeeper rule (if copied)
rm .cursor/rules/00-spec-superpowers.mdc

# Clean up task history (optional)
rm -rf .spec-tasks/
```

Removing spec-superpowers only removes the orchestration layer. OpenSpec, planning-with-files, and Superpowers continue to work independently.

## Dependencies

| Module | Type | Install |
|--------|------|---------|
| **OpenSpec CLI** | CLI tool | `npm install -g @fission-ai/openspec@latest` |
| **planning-with-files** | Cursor Skill | `npx skills add OthmanAdi/planning-with-files --agent cursor --yes` |
| **Superpowers** | Cursor Plugin | Cursor plugin marketplace |

All three must be installed for the full workflow. Each also works independently.

## Usage

### Commands

| Command | Effect |
|---------|--------|
| `/ssp` | Start the full workflow (dialogue-first, auto complexity) |
| `/ssp:design` | Dialogue exploration + OpenSpec specification only |
| `/ssp:plan` | Planning phase only |
| `/ssp:impl` | Implementation phase only |
| `/ssp:switch` | Switch to a different task workspace |
| `/ssp:clean` | Clean up archived tasks and stale artifacts |
| `/ssp:reset` | Clear current task state and start fresh |

#### `/ssp`

Runs the complete pipeline: **Dialogue → Complexity Triage → Specification → Planning → Implementation → Archive**. The AI first enters brainstorming mode — asking you questions one at a time, exploring your requirements, proposing multiple approaches with trade-offs, and getting your design approval. Only after you've confirmed the design does it determine complexity (Quick/Light/Full), formalize the spec via OpenSpec, create implementation plans, and execute. Quality gates between each step ensure nothing slips through. This is the default entry point for any new feature, bugfix, or refactor.

#### `/ssp:design`

Runs dialogue exploration + specification only. The AI uses the brainstorming skill (Superpowers) to interactively explore the problem space — one question at a time, propose multiple approaches, and get your design approval. Then formalizes the approved design via OpenSpec. Stops at Gate G1. Does not proceed to planning or implementation.

#### `/ssp:plan`

Runs planning only. Requires a spec in `openspec/`. Use when you have a confirmed spec and want to generate or revise the task plan. Creates `task_plan.md`, `findings.md`, and `progress.md`. Stops at Gate G2.

#### `/ssp:impl`

Runs implementation and archive. Requires `task_plan.md` at project root. Use when spec and plan are ready and you want to start coding. Includes TDD, code review, and the 3-Strike error escalation protocol. After passing Gate G3, automatically archives via OpenSpec.

#### `/ssp:switch`

Switch between task workspaces. Shows existing tasks in `.spec-tasks/` and lets you pick one, or create a new task. The current task's planning files are saved (copy-swap) before switching.

#### `/ssp:clean`

Interactive cleanup wizard for workflow artifacts. Scans five areas with appropriate safety levels. Files owned by other modules (Superpowers, OpenSpec) are flagged as advisory. The active task is never deleted.

#### `/ssp:reset`

Clears the current task state: removes root planning files and `_active.txt`. The task backup in `.spec-tasks/` is preserved. Use when you want to start the current task over from scratch.

### Workflow

```
/ssp
    |
    v
Step 1 -- Understand (dialogue-first brainstorming)
    AI asks questions one at a time, explores your intent
    Proposes 2-3 approaches, gets your design approval
    Brainstorming is NEVER shortened for Light mode
    |
    v
Step 2 -- Triage (post-dialogue complexity)
    AI recommends Quick/Light/Full based on conversation, you confirm
    |
    +-- Quick --> brief inline spec -> implement -> light review -> done
    |
    +-- Light / Full:
    v
Step 3 -- Formalize (OpenSpec specification)
    /opsx:propose -> openspec validate -> user confirms
    -- Gate G1: design approved + validate passed + user confirmed --
    |
    v
Step 4 -- Plan (writing-plans -> planning-with-files)
    Generate task_plan.md / findings.md / progress.md
    -- Gate G2: files ready + review loop --
    |
    v
Step 5 -- Build (Superpowers implementation)
    Subagent-Driven or Executing-Plans, TDD throughout
    -- Gate G3: tests pass + review + evidence --
    |
    v
Step 6 -- Archive
    openspec archive + copy-swap planning files + cleanup
```

### Complexity Triage

Complexity is determined **after** brainstorming, not before. The AI analyzes the conversation outcome, states its assessment with reasoning, and asks you to confirm. You can confirm or override.

**Quick** (all must be true): single file, no new public API, internal-only change, estimated <15 min. Quick mode skips OpenSpec entirely.

**Light** (all must be true): affects <=2 files, no new public API, no architecture change, estimated <30 min.

**Full**: anything else. Auto-Full for architecture changes, new dependencies, DB schema changes, security changes, or >5 files.

The AI monitors complexity fit throughout the workflow and proactively suggests adjustments.

### Task Workspace

Each task gets isolated planning context via `.spec-tasks/`:

```
.spec-tasks/
  _active.txt          (current task name)
  feat-user-auth/      (planning file backups)
  fix-login-bug/
  ...
```

Root-level planning files (`task_plan.md`, `findings.md`, `progress.md`) are always real files (copy-swap, not symlinks). This means:
- planning-with-files hooks work natively
- Uninstalling spec-superpowers leaves everything functional
- No Windows symlink permission issues

## Architecture

- **Dialogue-first** — brainstorming is the soul of the workflow, never shortened for process efficiency
- **Thin orchestration layer** — SKILL.md describes "who to call, what to expect", never inlines module internals
- **Loose coupling** — references stable interfaces only; zero path coupling; orchestration is purely descriptive
- **Hard quality gates** — G0-G3 with automated review loops (max 3 rounds) at every step transition
- **Gentle gatekeeper** — `.cursor/rules/00-spec-superpowers.mdc` auto-recovers active tasks, invites (not blocks) spec workflow for new coding tasks
- **Task isolation** — `.spec-tasks/` with copy-swap prevents context pollution between tasks

## Project Structure

```
Spec-SuperPower/
  skills/
    spec-superpowers/
      SKILL.md                         Core orchestration (<=120 lines)
      references/
        openspec-workflow.md           OpenSpec integration + validate/archive
        planning-workflow.md           Task workspace + hooks + responsibilities
        quality-gates.md              G0-G3 criteria + complexity adjustment
        integration-guide.md          Dependencies + FAQ
      assets/
        templates/
          constitution.md             Project constitution template
  .cursor/
    00-spec-superpowers.mdc           Always-on gatekeeper rule
  install.sh                          macOS/Linux installer
  install.ps1                         Windows installer
  test_skill.py                       Validation script (~70 checks)
  README.md
```

## Module Independent Upgrade

| Module | Upgrade | Impact on skill |
|--------|---------|-----------------|
| Superpowers | Cursor plugin auto-update | None |
| OpenSpec | `npm update -g @fission-ai/openspec` | None |
| planning-with-files | `npx skills update` | None |
| spec-superpowers | `npx skills add CrDeemo/Spec-SuperPower --skill ssp --agent cursor --yes` | Orchestration only |

---

Built by CrDeemo
