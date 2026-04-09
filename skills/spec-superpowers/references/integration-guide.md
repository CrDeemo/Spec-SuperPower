# Integration Guide

Setup, dependencies, and troubleshooting for spec-superpowers.

## Dependencies

| Module | Install | Role |
|--------|---------|------|
| OpenSpec CLI | `npm install -g @fission-ai/openspec@latest` | Specification (Phase 1) |
| planning-with-files | `npx skills add OthmanAdi/planning-with-files --agent cursor --yes` | Persistent planning (Phase 0, 2) |
| Superpowers | Cursor plugin marketplace | TDD, review, debugging (Phase 3) |

Superpowers sub-skills used: brainstorming, writing-plans, test-driven-development, requesting-code-review, verification-before-completion, systematic-debugging, finishing-a-development-branch.

## Startup Detection

On every `/spec-superpowers` invocation, check all three before proceeding:

1. **OpenSpec CLI** — `command -v openspec || npm list -g @fission-ai/openspec`
2. **planning-with-files** — verify skill is available to the agent
3. **Superpowers** — verify brainstorming, writing-plans, TDD sub-skills available

**Any missing → show install command → stop workflow → ask user to install and retry.**

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

**Wrong mode?** Tell the AI you want to change complexity (e.g., "switch to Full mode"). AI will handle the adjustment. Or re-run `/spec-superpowers` to start fresh.

**Context lost?** If `task_plan.md` exists, `/spec-superpowers` auto-recovers via 5-Question Reboot Test. Missing files = unrecoverable.

**3 errors in a row?** Handled by 3-Strike protocol automatically (standard fix → spec alignment → systematic-debugging → escalate).

**OpenSpec directory missing?** Run `openspec init`. Directory is `openspec/` (not `.openspec/`).

**Switch tasks?** `/spec-superpowers switch` or let Task Router detect active task.

**openspec validate failing?** Run manually: `openspec validate --change <name>`. Fix structural issues, re-run workflow.

## Clean Command

`/spec-superpowers clean` launches an interactive cleanup wizard:

```
/spec-superpowers clean
    │
    ├─ 1. Archived tasks (.spec-tasks/)
    │   List completed/archived task dirs → user picks: delete all / selective / skip
    │   Active task is never deleted.
    │
    ├─ 2. Orphan root files
    │   No _active.txt but task_plan.md / findings.md / progress.md exist at root
    │   → offer to remove or adopt into a new task
    │
    ├─ 3. Stale brainstorming sessions (.superpowers/brainstorm/)
    │   List old session dirs → user picks: delete all / selective / skip
    │   ⚠ Advisory only — these belong to Superpowers, not us
    │
    ├─ 4. Superpowers docs (docs/superpowers/)
    │   List plans/specs dirs → user picks: delete all / selective / skip
    │   ⚠ Advisory only — these belong to Superpowers
    │
    └─ 5. Archived OpenSpec changes (openspec/changes/)
        List changes already archived → user picks: delete all / selective / skip
        ⚠ Advisory only — these belong to OpenSpec
```

Rules:
- Steps 1-2: spec-superpowers owns these, safe to delete directly
- Steps 3-5: other modules own these, always ask user with warning before touching
- Never delete without explicit user confirmation
- Never delete the active task or its associated files
- Show disk space freed after cleanup

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
