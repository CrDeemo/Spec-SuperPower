# Integration Guide

Setup, dependencies, and troubleshooting for spec-superpowers.

## Dependencies

| Module | Install | Role |
|--------|---------|------|
| OpenSpec CLI | `npm install -g @fission-ai/openspec@latest` | Specification (Step 3) |
| planning-with-files | `npx skills add OthmanAdi/planning-with-files --agent cursor --yes` | Persistent planning (Step 4, session recovery) |
| Superpowers | Cursor plugin marketplace | Brainstorming, TDD, review, debugging (Step 1, 5) |

Superpowers sub-skills used: brainstorming, writing-plans, test-driven-development, requesting-code-review, verification-before-completion, systematic-debugging, finishing-a-development-branch.

## Startup Detection

On every `/ssp` invocation, check all three before proceeding:

1. **OpenSpec CLI** — `command -v openspec || npm list -g @fission-ai/openspec`
2. **planning-with-files** — verify skill is available to the agent
3. **Superpowers** — verify brainstorming, writing-plans, TDD sub-skills available

**Any missing → show install command → stop workflow → ask user to install and retry.**

This check runs silently and only interrupts when something is missing.

## Uninstall Impact

| Action | Other Modules |
|--------|---------------|
| Remove spec-superpowers | Each module works independently |
| Upgrade OpenSpec / Superpowers / planning-with-files | spec-superpowers unaffected |
| Upgrade spec-superpowers | Three modules unaffected |

Pure orchestration layer. `.spec-tasks/` remains as harmless backups.

## .spec-tasks Directory

```
.spec-tasks/
  _active.txt         (active task name)
  feat-user-auth/     (planning file backups)
    task_plan.md / findings.md / progress.md
```

- Root files are always real files (copy-swap, not symlinks)
- After uninstall: root files work normally, `.spec-tasks/` can be deleted
- Add `.spec-tasks/` to `.gitignore` if desired

## Troubleshooting

**Skill not triggered?** Verify SKILL.md installed + `.cursor/00-spec-superpowers.mdc` in place. Restart Cursor.

**Wrong mode?** Tell the AI you want to change complexity (e.g., "switch to Full mode"). AI will handle the adjustment. Or re-run `/ssp` to start fresh.

**Context lost?** If `task_plan.md` exists, `/ssp` auto-recovers via 5-Question Reboot Test. Missing files = unrecoverable.

**3 errors in a row?** Handled by 3-Strike protocol automatically (standard fix → spec alignment → systematic-debugging → escalate).

**OpenSpec directory missing?** Run `openspec init`. Directory is `openspec/` (not `.openspec/`).

**Switch tasks?** `/ssp:switch` or let Task Router detect active task.

**openspec validate failing?** Run manually: `openspec validate --change <name>`. Fix structural issues, re-run workflow.

## Clean Command

`/ssp:clean` launches an interactive cleanup wizard:

### Safety Levels

Each artifact area has a safety level that determines the default behavior:

| Level | Area | Default | Rationale |
|-------|------|---------|-----------|
| Safe | `.spec-tasks/` archived tasks | Offer delete | Owned by spec-superpowers, pure backups |
| Safe | Orphan root planning files | Offer delete | No active task references them |
| Caution | `.superpowers/brainstorm/` sessions | Skip (show age) | Owned by Superpowers; delete if >30 days old |
| Caution | `docs/superpowers/` plans/specs | Skip (show age) | Owned by Superpowers; delete if >30 days old |
| Preserve | `openspec/changes/` archived changes | Skip by default | Project decision history — needed for traceability |

### Wizard Flow

```
/ssp:clean
    │
    ├─ 1. [Safe] Archived tasks (.spec-tasks/)
    │   List completed/archived task dirs with last-modified date and size
    │   → user picks: delete all / selective / skip
    │   Active task is never shown.
    │
    ├─ 2. [Safe] Orphan root files
    │   No _active.txt but task_plan.md / findings.md / progress.md exist at root
    │   → offer to remove or adopt into a new task
    │
    ├─ 3. [Caution] Stale brainstorming sessions (.superpowers/brainstorm/)
    │   List old session dirs with age — highlight those >30 days
    │   ⚠ "These belong to Superpowers. Deleting >30-day sessions is usually safe."
    │   → user picks: delete old / selective / skip (default: skip)
    │
    ├─ 4. [Caution] Superpowers docs (docs/superpowers/)
    │   List plans/specs dirs with age — highlight those >30 days
    │   ⚠ "These belong to Superpowers. Old plans/specs can usually be removed."
    │   → user picks: delete old / selective / skip (default: skip)
    │
    └─ 5. [Preserve] Archived OpenSpec changes (openspec/changes/)
        List changes already archived with summary
        ⚠ "These are your project's decision history. Recommend keeping them."
        → Only shown if user explicitly asks (e.g., /ssp:clean --all)
        → default: skip entirely
```

### Rules

- **Safe** areas: prompt user, delete on confirmation
- **Caution** areas: show age + advisory warning, default action is skip
- **Preserve** areas: hidden by default, only shown with `--all` flag or explicit request
- Never delete without explicit user confirmation
- Never delete the active task or its associated files
- Show last-modified date and size for every item
- Show total disk space freed after cleanup

## Recommended .gitignore

Add these to your project `.gitignore` to keep workflow artifacts out of version control:

```gitignore
# spec-superpowers workflow artifacts
.spec-tasks/
task_plan.md
findings.md
progress.md

# Superpowers artifacts
.superpowers/
docs/superpowers/

# OpenSpec (uncomment if you don't want specs in VCS)
# openspec/
```

The install script appends these entries automatically if `.gitignore` exists.
