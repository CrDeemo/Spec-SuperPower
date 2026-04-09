# spec-superpowers

A Cursor Agent Skill that orchestrates **OpenSpec** + **planning-with-files** + **Superpowers** into a unified spec-driven development workflow.

Loosely coupled — uninstalling this skill does not affect the three independent modules.

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
npx skills add CrDeemo/Spec-SuperPower --skill spec-superpowers --agent cursor --yes

# 3. Install planning-with-files skill (project-level)
npx skills add OthmanAdi/planning-with-files --agent cursor --yes

# 4. Install Superpowers via Cursor plugin marketplace (includes sub-skills)

# 5. (Optional) Copy gatekeeper rule to your project
mkdir -p .cursor/rules
cp .cursor/skills/spec-superpowers/.cursor/00-spec-superpowers.mdc .cursor/rules/
```

After installation, restart Cursor and type `/spec-superpowers` in Agent chat.

## Uninstall

```bash
# Remove spec-superpowers only (other modules keep working)
npx skills remove spec-superpowers

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
| `/spec-superpowers` | Start the full workflow (auto complexity triage) |
| `/spec-superpowers spec` | OpenSpec specification phase only |
| `/spec-superpowers plan` | Planning phase only |
| `/spec-superpowers impl` | Implementation phase only |
| `/spec-superpowers reset` | Reset complexity choice and state |
| `/spec-superpowers escalate` | Upgrade Light to Full mid-workflow |
| `/spec-superpowers simplify` | Downgrade Full to Light mid-workflow |
| `/spec-superpowers switch` | Switch to a different task workspace |

### Workflow

```
/spec-superpowers
    |
    v
Phase -1 -- Task Router
    Detect active task or create new workspace (.spec-tasks/)
    |
    v
Phase 0 -- Session Recovery (auto)
    5-Question Reboot Test if prior session exists
    -- Gate G0 --
    |
    v
Phase 1 -- Specification (OpenSpec)
    Full: /opsx:explore -> /opsx:propose -> openspec validate -> user confirms
    Light: /opsx:propose -> openspec validate -> user confirms
    -- Gate G1: validate + confirmed + review loop --
    |
    v
Phase 2 -- Planning (writing-plans -> planning-with-files)
    Generate task_plan.md / findings.md / progress.md
    -- Gate G2: files ready + review loop --
    |
    v
Phase 3 -- Implementation (Superpowers)
    Subagent-Driven or Executing-Plans, TDD throughout
    -- Gate G3: tests pass + review + evidence --
    |
    v
Phase 4 -- Archive
    openspec archive + copy-swap planning files + cleanup
```

### Complexity Triage

The AI suggests Light or Full; you confirm or override.

**Light** (all must be true): affects <=2 files, no new public API, no architecture change, estimated <30 min.

**Full**: anything else.

You can switch mid-workflow with `/spec-superpowers escalate` or `/spec-superpowers simplify`.

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

- **Thin orchestration layer** -- SKILL.md describes "who to call, what to expect", never inlines module internals
- **Loose coupling** -- references stable interfaces only; zero path coupling; orchestration is purely descriptive
- **Hard quality gates** -- G0-G3 with automated review loops (max 3 rounds) at every phase transition
- **Always-on gatekeeper** -- `.cursor/rules/00-spec-superpowers.mdc` blocks coding without a confirmed spec
- **Task isolation** -- `.spec-tasks/` with copy-swap prevents context pollution between tasks

## Project Structure

```
Spec-SuperPower/
  skills/
    spec-superpowers/
      SKILL.md                         Core orchestration (<=120 lines)
      references/
        openspec-workflow.md           OpenSpec integration + validate/archive
        planning-workflow.md           Task workspace + hooks + responsibilities
        quality-gates.md              G0-G3 criteria + escalate/simplify
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
| spec-superpowers | `npx skills add CrDeemo/Spec-SuperPower --skill spec-superpowers --agent cursor --yes` | Orchestration only |

---

Built by CrDeemo
