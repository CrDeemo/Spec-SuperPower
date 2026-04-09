# Planning Workflow

How spec-superpowers uses planning-with-files for persistent planning (Phase 2), session recovery (Phase 0), and task workspace management (Phase -1).

## Task Workspace (Copy-Swap)

Each task gets isolated planning files. Root files are always **real files** (never symlinks).

```
.spec-tasks/
  _active.txt               (active task name, e.g. "feat-user-auth")
  feat-user-auth/
    task_plan.md / findings.md / progress.md
project root/
  task_plan.md               (real file — copy of active task's version)
  findings.md / progress.md
```

### Copy-Swap Protocol

**New task:** ask name (kebab-case) → create `.spec-tasks/<name>/` → write `_active.txt` → pipeline creates root files.

**Switch task:** copy root files → `.spec-tasks/<old>/` → copy `.spec-tasks/<new>/` → root → update `_active.txt`.

**Archive (Phase 4):** copy root → `.spec-tasks/<task>/` → delete root files + `_active.txt`.

**Uninstall safety:** root files are plain → planning-with-files works normally. `.spec-tasks/` = harmless history.

## Three-File System

| File | Purpose | Full | Light |
|------|---------|:----:|:-----:|
| `task_plan.md` | Numbered task checklist | Yes | Yes |
| `findings.md` | Decisions, trade-offs, context | Yes | Skip |
| `progress.md` | Status, verification evidence | Yes | Yes (minimal) |

### task_plan.md Format

Each task must include:
- **File paths** — files to create/modify
- **Acceptance criteria** — what "done" looks like
- **Test strategy** — how to verify

```markdown
- [ ] Task 1: Create user authentication module
  - Files: `src/auth/login.ts`, `src/auth/login.test.ts`
  - Acceptance: Login endpoint returns JWT on valid credentials
  - Test: Unit tests for valid/invalid credentials, integration test for full flow
```

### findings.md

Architectural decisions, existing patterns, constraints, external dependencies investigated.

### progress.md

Task completion timestamps, verification evidence, issues + resolutions, gate clearance records. Light mode: minimal — only G3 evidence.

## writing-plans vs planning-with-files

| Aspect | writing-plans (Author) | planning-with-files (Runtime) |
|--------|----------------------|------------------------------|
| Focus | Content quality | Persistence + attention management |
| Output | Plan text content | task_plan.md file + hooks |
| Criteria | Each step 2-5 min, complete paths, zero placeholders | Files at root, 2-Action Rule for findings |

Flow: writing-plans generates content → formatted per planning-with-files template → written to root `task_plan.md` → hooks auto-manage.

## Hook System

planning-with-files hooks auto-inject planning context:

| Hook | Trigger | Effect |
|------|---------|--------|
| `UserPromptSubmit` | Every user message | Inject planning summary into context |
| `PreToolUse` | Before tool call | Check action aligns with active task |
| `PostToolUse` | After tool call | Update progress |
| `Stop` | Session ends | Save progress |

**2-Action Rule**: After every 2 view/search operations, save findings to `findings.md`.

Hooks activate automatically when planning files exist at root — no explicit invocation.

## Session Recovery (Phase 0)

Check for `task_plan.md` at root:
- **Not found** → continue to Phase 1
- **Found** → run 5-Question Reboot Test

### 5-Question Reboot Test

| # | Question | Source |
|---|----------|--------|
| 1 | Where am I? | Code state + task_plan.md checkboxes |
| 2 | Where am I going? | Next unchecked task |
| 3 | What's the goal? | task_plan.md header / spec |
| 4 | What did I learn? | findings.md |
| 5 | What did I do? | progress.md |

All answers must be consistent. Checked tasks ↔ progress.md, goal ↔ spec, findings ↔ code state.

Pass → **G0 clears** → resume from last unchecked task.
Fail → re-read files, re-test. Still inconsistent → present contradictions to user.

## Gate G2 Review Loop

```
Plan written → dispatch plan-document-reviewer subagent
    ├─ Pass → G2 clears
    └─ Fail → fix gaps → re-review (max 3 rounds → escalate to user)
```

Reviewer verifies: all tasks annotated, logical ordering, coverage of spec requirements. Uses `writing-plans` skill.

**G2 passes when:** task_plan.md annotated + findings.md exists (Full) + progress.md exists + review loop passed.

## Loose Coupling

References only: `task_plan.md`, `findings.md`, `progress.md` file conventions, `planning-with-files` and `writing-plans` skill names, `.spec-tasks/` directory.
