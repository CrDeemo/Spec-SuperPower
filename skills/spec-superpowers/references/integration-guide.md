# Integration Guide

Setup, dependency management, and troubleshooting for spec-superpowers.

## Dependency List

| Module | Install Command | Role |
|--------|----------------|------|
| OpenSpec CLI | `npm install -g @fission-ai/openspec@latest` | Specification (Phase 1) |
| planning-with-files | `npx skills add OthmanAdi/planning-with-files` | Persistent planning (Phase 0, 2) |
| Superpowers | Cursor plugin marketplace | TDD, review, debugging (Phase 3) |
| using-superpowers | Part of Superpowers | Skill discovery and routing |
| brainstorming | Part of Superpowers | Spec review loop (G1) |
| writing-plans | Part of Superpowers | Plan review loop (G2) |
| test-driven-development | Part of Superpowers | TDD in Phase 3 |
| requesting-code-review | Part of Superpowers | Two-stage review (G3) |
| verification-before-completion | Part of Superpowers | Evidence gathering (G3) |
| systematic-debugging | Part of Superpowers | Error escalation (Phase 3) |
| finishing-a-development-branch | Part of Superpowers | Archive (Phase 4) |

## Dependency Detection at Startup

On every `/spec-superpowers` invocation, verify all dependencies before proceeding:

### 1. OpenSpec CLI

```
Check: command -v openspec || npm list -g @fission-ai/openspec
Missing → show: npm install -g @fission-ai/openspec@latest
```

### 2. planning-with-files

```
Check: verify the planning-with-files skill is available to the AI agent
Missing → show: npx skills add OthmanAdi/planning-with-files
```

### 3. Superpowers Sub-skills

```
Check: verify brainstorming, writing-plans, and test-driven-development
       sub-skills are available to the AI agent
Missing → show: install Superpowers via Cursor plugin marketplace
```

### Enforcement

If **any** dependency is missing:

1. Display the install command for the missing module(s)
2. **Stop the workflow** — do not proceed to any phase
3. Ask the user to install and retry

## Uninstall Impact Matrix

| Action | Scope | Other Modules |
|--------|-------|---------------|
| Uninstall spec-superpowers | Removes orchestration + gatekeeper | Each module works independently |
| Upgrade OpenSpec | CLI updates | spec-superpowers unaffected |
| Upgrade Superpowers | Plugin updates | spec-superpowers unaffected |
| Upgrade planning-with-files | Skill files update | spec-superpowers unaffected |
| Upgrade spec-superpowers | Orchestration updates | Three modules unaffected |

spec-superpowers is a pure orchestration layer. Removing it leaves OpenSpec, planning-with-files, and Superpowers fully functional as standalone tools.

## Troubleshooting FAQ

### spec-superpowers not triggered?

- Verify the skill is installed: check that `SKILL.md` exists in the expected skill location
- Verify the gatekeeper rule `.cursor/00-spec-superpowers.mdc` is in place
- Restart Cursor to reload skills

### Wrong mode (Light vs Full)?

- Run `/spec-superpowers reset` to clear the current complexity choice
- Re-run `/spec-superpowers` and override the AI suggestion when prompted

### Context lost mid-session?

- Check if `task_plan.md` and `progress.md` exist in the project root
- If they exist, run `/spec-superpowers` — Phase 0 will auto-detect and recover via the 5-Question Reboot Test
- If files are missing, the session cannot be recovered automatically

### 3 errors in a row during implementation?

- This is handled automatically by the 3-Strike protocol
- Strike 1: standard fix → Strike 2: check spec alignment → Strike 3: trigger `systematic-debugging`
- If still unresolved: architecture assumptions are challenged and the issue escalates to the user

### OpenSpec directory not found?

- Run `openspec init` to initialize the OpenSpec workspace
- OpenSpec uses the `openspec/` directory (not `.openspec/`)
- Verify the directory exists after initialization: `ls openspec/`
