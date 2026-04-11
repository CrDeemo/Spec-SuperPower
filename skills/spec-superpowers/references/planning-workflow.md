# Planning Workflow

How spec-superpowers uses planning-with-files for persistent planning (Step 4), session recovery, and task workspace management.

## Task Workspace (Copy-Swap)

Each task gets isolated planning files. Root files are always **real files** (never symlinks).

Quick mode exception: Quick tasks only write `_active.txt` (no task subdirectory, no planning files). After completion, `_active.txt` is deleted. If upgraded to Light/Full mid-workflow, a full task workspace is created at that point.

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

**New task:** After brainstorming completes and complexity is triaged (Light/Full), derive task name from conversation (kebab-case) → create `.spec-tasks/<name>/` → write `_active.txt` → pipeline creates root files.

**Switch task (`/ssp:switch`):** copy root files → `.spec-tasks/<old>/` → copy `.spec-tasks/<new>/` → root → update `_active.txt`.

**Archive (Step 6):** copy root → `.spec-tasks/<task>/` → delete root files + `_active.txt`.

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

## Session Recovery

Check for `task_plan.md` at root:
- **Not found** → continue to Step 1 (brainstorming)
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

### Code Reality Check (post-reboot verification)

After the 5 questions pass, run a code state verification:

1. **Diff scan** — check `git diff --stat` (or equivalent) for uncommitted changes in the working tree.
2. **Completed tasks → code exists?** — For each task marked done in task_plan.md, verify the listed files have actual modifications (staged, committed, or in working tree).
3. **Pending tasks → no premature changes?** — For tasks marked pending, verify their listed files have no unexpected modifications.

| Finding | Severity | Action |
|---------|----------|--------|
| Code changed but task not marked done | Warning | Ask user: "检测到以下文件有工作流外的修改：[list]。是否纳入当前任务？" |
| Task marked done but files unchanged | Error | Flag contradiction: "progress.md 记录与代码状态矛盾，请确认。" |
| Pending task files have changes | Warning | Ask user: confirm intentional or revert |

Code Reality Check failures do not block G0 on their own — they produce warnings that the user must acknowledge before resuming. If the user acknowledges, record the resolution in progress.md and proceed.

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
