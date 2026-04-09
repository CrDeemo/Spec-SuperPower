# Planning Workflow

This file describes how spec-superpowers uses planning-with-files for persistent planning (Phase 2), session recovery (Phase 0), and task workspace management (Phase -1).

## Task Workspace (Copy-Swap)

### Why

A project has many tasks over its lifetime. Without isolation, planning files from one task pollute the context of the next. The task workspace solves this by giving each task its own directory while keeping root-level files compatible with planning-with-files hooks.

### Directory Structure

```
.spec-tasks/
  _active.txt               (plain text — active task name, e.g. "feat-user-auth")
  feat-user-auth/
    task_plan.md
    findings.md
    progress.md
  fix-login-bug/
    ...
project root/
  task_plan.md               (real file — copy of active task's version)
  findings.md
  progress.md
```

### Copy-Swap Protocol

Root-level planning files are always **real files** (never symlinks). This ensures planning-with-files hooks work natively and uninstalling spec-superpowers leaves everything functional.

**Creating a new task:**
1. Ask user for task name (kebab-case, e.g. `feat-user-auth`)
2. Create `.spec-tasks/<name>/`
3. Write task name to `.spec-tasks/_active.txt`
4. Root planning files are created normally by the pipeline

**Switching tasks:**
1. Copy root `task_plan.md`, `findings.md`, `progress.md` → `.spec-tasks/<old-task>/`
2. Copy `.spec-tasks/<new-task>/` files → root
3. Update `.spec-tasks/_active.txt` with new task name

**Archiving a task (Phase 4):**
1. Copy root planning files → `.spec-tasks/<task>/`
2. Delete root `task_plan.md`, `findings.md`, `progress.md`
3. Delete `.spec-tasks/_active.txt`

### Uninstall Safety

After removing spec-superpowers:
- Root planning files are plain files → planning-with-files works normally
- `.spec-tasks/` is a harmless directory of historical backups
- No symlinks, no Windows permission issues

## Three-File System

Planning produces up to three files in the project root:

| File | Purpose | Full Mode | Light Mode |
|------|---------|:---------:|:----------:|
| `task_plan.md` | Numbered checklist of tasks | Yes | Yes |
| `findings.md` | Discoveries, decisions, context gathered during planning | Yes | Skip |
| `progress.md` | Status updates, completion evidence, verification records | Yes | Yes (minimal) |

### task_plan.md

A numbered checklist where each task includes:

- **File paths** — which files will be created or modified
- **Acceptance criteria** — what "done" looks like for this task
- **Test strategy** — how to verify the task is complete

Example structure:

```markdown
- [ ] Task 1: Create user authentication module
  - Files: `src/auth/login.ts`, `src/auth/login.test.ts`
  - Acceptance: Login endpoint returns JWT on valid credentials
  - Test: Unit tests for valid/invalid credentials, integration test for full flow
```

### findings.md

Records context gathered during planning:

- Architectural decisions and their rationale
- Existing code patterns discovered
- Constraints and trade-offs identified
- External dependencies investigated

### progress.md

Tracks execution status:

- Task completion timestamps
- Verification evidence (test results, review outcomes)
- Issues encountered and resolutions
- Gate clearance records

In Light mode, progress.md is minimal — only enough to provide Gate G3 evidence.

## writing-plans vs planning-with-files Responsibilities

These two modules have complementary roles:

| Aspect | writing-plans (Superpowers) | planning-with-files |
|--------|----------------------------|---------------------|
| **Role** | Plan "Author" | Plan "Runtime" |
| **Focus** | Content quality | Persistence + attention management |
| **Output** | Plan text content | task_plan.md file + hooks |
| **Criteria** | Each step 2-5 min, complete file paths, zero placeholders | Files at root, 2-Action Rule for findings |

**Flow:**
1. writing-plans generates plan content (quality standards apply)
2. Content is formatted per planning-with-files' task_plan.md template
3. Written directly into root `task_plan.md`
4. planning-with-files hooks auto-manage attention from this point

All plans live in `.spec-tasks/<task>/task_plan.md` — no separate `docs/superpowers/plans/` needed.

## planning-with-files Hook System

planning-with-files uses hooks to automatically inject planning context into the agent's attention. Understanding why this works is key to the workflow:

| Hook | Trigger | Effect |
|------|---------|--------|
| `UserPromptSubmit` | Every user message | Reads planning files and injects summary into context |
| `PreToolUse` | Before each tool call | Checks if current action aligns with the active task |
| `PostToolUse` | After each tool call | Updates progress tracking |
| `Stop` | Session ends | Ensures progress is saved |

The **2-Action Rule**: After every 2 view/browser/search operations, findings must be saved to `findings.md` to prevent information loss across multimodal context.

These hooks activate automatically when planning files exist at the project root — no explicit invocation needed. This is why root-level real files are essential.

## Full Mode Planning

Generate all three files. Every task in task_plan.md must have file paths, acceptance criteria, and test strategy. No task may omit any of these three fields.

## Light Mode Planning

Generate `task_plan.md` with the same task annotation requirements. Generate a minimal `progress.md` for G3 evidence tracking. Skip `findings.md`.

## Session Recovery Protocol (Phase 0)

At the start of every invocation, check for an existing session:

### Detection

Look for `task_plan.md` in the project root.

- **Not found** → No prior session. Continue to Phase 1.
- **Found** → Prior session detected. Execute the 5-Question Reboot Test.

### 5-Question Reboot Test

Read all available planning files and answer these five questions:

| # | Question | Source |
|---|----------|--------|
| 1 | Where am I? | Current state of implementation (inspect code + task_plan.md checkboxes) |
| 2 | Where am I going? | Next unchecked task in task_plan.md |
| 3 | What's the goal? | Overall objective (from task_plan.md header / spec) |
| 4 | What did I learn? | Read findings.md (if it exists) |
| 5 | What did I do? | Read progress.md (if it exists) |

### Consistency Check

All 5 answers must be consistent with the file contents. Specifically:

- Checked tasks in task_plan.md should match progress.md entries
- The overall goal should align with the spec in `openspec/`
- No contradictions between findings.md context and current code state

### Resume

If the reboot test passes → **Gate G0 clears** → resume from the last unchecked task in task_plan.md.

If the reboot test fails (answers inconsistent or contradictory) → re-read all files and run the test again.

## Writing-Plans Review Loop (Gate G2)

After the plan is written, dispatch a quality review:

```
Plan written → dispatch plan-document-reviewer subagent → review result
    ├─ Pass → Gate G2 clears
    └─ Fail → fix plan gaps → re-review
               (max 3 rounds)
               └─ Still failing after 3 rounds → escalate to user
```

The reviewer subagent verifies:

- Every task has file paths, acceptance criteria, and test strategy
- Tasks are ordered logically (dependencies respected)
- The plan covers all requirements from the spec

This uses the `writing-plans` skill from Superpowers.

## Gate G2 Clearance

Gate G2 passes when **all** conditions are met:

1. `task_plan.md` exists with all tasks properly annotated
2. `findings.md` exists (Full mode only)
3. `progress.md` exists
4. The writing-plans review loop has passed

## Important: Loose Coupling

This workflow references only stable interfaces:

- **File conventions**: `task_plan.md`, `findings.md`, `progress.md`
- **Skill names**: `planning-with-files`, `writing-plans`
- **Directory**: `.spec-tasks/` (managed by spec-superpowers orchestration only)

Do NOT inline the internal logic of planning-with-files or Superpowers' writing-plans skill. If those modules update their internals, this workflow remains valid as long as the file conventions and skill names are preserved.
