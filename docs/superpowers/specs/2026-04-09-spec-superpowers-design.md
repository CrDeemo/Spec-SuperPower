# spec-superpowers Design Spec

A Cursor Agent Skill that orchestrates OpenSpec + planning-with-files + Superpowers into a dialogue-first, spec-driven development workflow. Loosely coupled — uninstalling this skill does not affect the independent modules.

**Repo**: `CrDeemo/spec-superpowers`
**Reference**: [zxzvsdcj/spec-first-superpowers](https://github.com/zxzvsdcj/spec-first-superpowers)

---

## 1. Core Philosophy: Dialogue First

The fundamental principle: **understand before you formalize, formalize before you build**.

Brainstorming (dialogue exploration) is the soul of the workflow. It is NEVER shortened for Light mode — understanding the user has no abbreviated version. Complexity triage happens AFTER brainstorming, not before, because the conversation reveals what the task actually requires.

## 2. Project Structure

```
spec-superpowers/                              # GitHub: CrDeemo/spec-superpowers
├── skills/
│   └── spec-superpowers/                      # ← npx skills add installs only this
│       ├── SKILL.md                           # Core orchestration (≤120 lines)
│       ├── references/
│       │   ├── openspec-workflow.md            # OpenSpec integration flow
│       │   ├── planning-workflow.md            # planning-with-files integration flow
│       │   ├── quality-gates.md               # Gate G0-G3 criteria
│       │   └── integration-guide.md           # Install / deps / troubleshooting
│       └── assets/
│           └── templates/
│               └── constitution.md            # Project constitution template
├── .cursor/
│   └── 00-spec-superpowers.mdc                # Always-on gentle guide rule
├── install.sh                                 # macOS/Linux one-click install
├── install.ps1                                # Windows one-click install
├── test_skill.py                              # Validation script (~60 checks)
└── README.md
```

`npx skills add` discovers `skills/` and installs only its contents. Root-level dev files (test_skill.py, install scripts) are not included.

## 3. Command System

| Command | Effect |
|---------|--------|
| `/ssp` | Full workflow — dialogue-first, auto complexity |
| `/ssp:design` | Dialogue exploration + OpenSpec specification only |
| `/ssp:plan` | Planning phase only |
| `/ssp:impl` | Implementation phase only |
| `/ssp:switch` | Switch to a different task workspace |
| `/ssp:clean` | Clean up archived tasks and stale workflow artifacts |
| `/ssp:reset` | Clear current task state and start fresh |

## 4. Complexity Triage (Post-Dialogue)

Three levels. Determined AFTER brainstorming, not before. AI suggests based on conversation outcome; user confirms or overrides.

| Level | Trigger signals | Pipeline |
|-------|----------------|----------|
| **Quick** | Single-file internal change, <15 min | Inline spec → implement → light review. **No OpenSpec, no planning files.** |
| **Light** | ≤2 files, bugfix, config, no new API, <30 min | OpenSpec + task_plan.md + minimal progress.md → full implementation |
| **Full** | New feature, refactor, multi-file, architecture | OpenSpec + all planning files + full review |

### Quick Criteria (all must be true)

- Affects exactly 1 file
- No new public API or exported interface
- Internal-only change (function body, bugfix, performance)
- Estimated < 15 minutes

If any criterion is false → Light or Full.

### Light Criteria (all must be true)

- Affects 2 or fewer files
- No new public API or exported interface
- No architecture change (no new module, data flow, or dependency)
- Estimated < 30 minutes

If any criterion is false → Full.

Auto-Full (no override): architecture change, new external dependency, DB schema change, security change, >5 files.

### Brainstorming and Complexity

**Critical design decision**: brainstorming depth is NOT tied to complexity level.

| Mode | Brainstorming | Reason |
|------|--------------|--------|
| Quick | Brief confirmation (2-3 sentences) | Task is trivially scoped |
| Light | **Full brainstorming** | Understanding the user is never abbreviated |
| Full | **Full brainstorming** | Full exploration |

Complexity only affects what happens AFTER brainstorming: OpenSpec formalization depth, planning file count, and review strictness.

### Mid-Workflow Complexity Adjustment

AI monitors complexity fit throughout the workflow and proactively suggests adjustments (no dedicated commands). Quick → Light/Full when scope grows. Light → Full when complexity exceeds Light criteria. Full → Light when task is simpler than assessed. Prior artifacts preserved — no rework.

## 5. Task Workspace (Copy-Swap)

Each task gets an isolated workspace for planning files:

```
.spec-tasks/
  _active.txt               (plain text, records active task name e.g. "feat-user-auth")
  feat-user-auth/
    task_plan.md
    findings.md
    progress.md
  fix-login-bug/
    ...
project root/
  task_plan.md               (real file — always a copy of the active task's version)
  findings.md
  progress.md
```

Key design (Copy-Swap, not Symlink):
- `openspec/changes/<name>/` is managed natively by OpenSpec for multi-change support; we do not move these files
- `.spec-tasks/` only manages backups/history for planning-with-files' three files
- Root-level `task_plan.md` etc. are always **real files** (not symlinks); planning-with-files hooks work natively
- On task switch: copy root files back to `.spec-tasks/<old>/` → copy `.spec-tasks/<new>/` files to root → update `_active.txt`
- On Step 6 Archive: copy root files back to `.spec-tasks/<task>/` → delete root planning files → delete `_active.txt`
- After uninstalling spec-superpowers: root files are plain files → planning-with-files fully functional; `.spec-tasks/` becomes harmless history
- No Windows compatibility issues (no symlink permissions needed)

Task workspace creation happens AFTER brainstorming completes (task name derived from conversation), not before. This keeps the dialogue uninterrupted by process mechanics.

## 6. Pipeline

```
/ssp
    │
    ▼
Step 1 — Understand (dialogue-first brainstorming)
    Full: brainstorming (interactive design — one question at a time)
    Light: brainstorming (identical to Full — NEVER shortened)
    Quick: brief confirmation (2-3 sentences + user confirms)
    │
    ▼
Step 2 — Triage (post-dialogue complexity)
    AI recommends Quick/Light/Full based on conversation outcome → user confirms
    Light/Full: create task workspace (.spec-tasks/) with name from conversation
    │
    ▼
Step 3 — Formalize (OpenSpec specification, Light/Full only)
    /opsx:propose → openspec validate → user confirms
    ── Gate G1: design approved + validate passed + user confirmed (max 3 review rounds) ──
    │
    ▼
Step 4 — Plan (planning-with-files + writing-plans, Light/Full only)
    writing-plans generates plan content → written into task_plan.md (planning-with-files format)
    planning-with-files hooks auto-manage attention from this point
    Generate: task_plan.md / findings.md / progress.md
    Each task annotated: file paths + acceptance criteria + test strategy
    ── Gate G2: files ready + plan review loop passed (max 3 rounds) ──
    │
    ▼
Step 5 — Build (Superpowers implementation)
    Strategy (AI recommends, user picks):
    • Subagent-Driven: independent subagent per task + two-stage review
    • Executing-Plans: batch execution + checkpoint reviews
    TDD throughout. Errors escalate: 3-Strike → systematic-debugging
    ── Gate G3: all tests pass + review passed + evidence in progress.md ──
    │
    ▼
Step 6 — Archive
    finishing-a-development-branch → update checkboxes
    → openspec archive <change-name> (Light/Full only)
    → copy root planning files to .spec-tasks/<task>/ → delete root planning files → delete _active.txt
```

### Quick Mode Pipeline

Brief inline spec (2-3 sentences in chat, user confirms) → implement → light review → clear `_active.txt`. No OpenSpec, no planning files, no task subdirectory in `.spec-tasks/`. Gates: G1-Quick (user confirmed inline spec) and G3-Quick (tests pass + single-round review).

### Light Mode Adjustments

- Step 1: **Full brainstorming** (identical to Full mode — never shortened)
- Step 3: OpenSpec propose + validate + confirm (same as Full)
- Step 4: Generate `task_plan.md` only, skip findings.md. `progress.md` still created (minimal, for G3 evidence).
- Step 5 & 6: Same as Full mode

### Sub-command Direct Jump

- `/ssp:design` → Enter Step 1-3, stop at G1
- `/ssp:plan` → Enter Step 4 (requires spec to exist in `openspec/`), stop at G2
- `/ssp:impl` → Enter Step 5 (requires `task_plan.md` to exist), then complete Step 6

## 7. Gatekeeper Rule

File: `.cursor/00-spec-superpowers.mdc`

```yaml
---
description: "Spec-Superpowers gatekeeper: auto-recovery, session awareness, and gentle coding guide"
globs: "*"
alwaysApply: true
---
```

Behavior:
1. **Detect**: Active task → silently restore context, brief status message
2. **Invite**: No active task + coding request → gently invite user to `/ssp` or direct dialogue — NOT a hard block
3. **Respect**: User insists on skipping → allow with a soft reminder
4. **Pass**: Non-coding requests → allow freely

## 8. Loose Coupling Architecture

### Dependency Map

```
spec-superpowers (orchestration layer)
│
│  Describes "who to call, what to expect" only. Never copies module internals.
│
├─→ OpenSpec CLI          Install: npm install -g @fission-ai/openspec
│   Interface: /opsx:explore, /opsx:propose, openspec/ directory
│
├─→ planning-with-files   Install: npx skills add (independent skill)
│   Interface: task_plan.md, findings.md, progress.md
│
└─→ Superpowers           Install: Cursor plugin system
    Interface: brainstorming, writing-plans, TDD, code-review (skill names)
```

### Three Iron Rules

1. **Reference stable interfaces only** — SKILL.md and references describe "call module X, expect output Y". Never inline module-specific steps, parameters, or internal directory structures.

2. **Zero path coupling** — No hardcoded module install paths. Detect CLIs via `command -v`; detect skills via availability to the AI agent.

3. **Orchestration is purely descriptive** — SKILL.md is an instruction document for the AI, not executable code. It has no runtime dependency on any module's internal state.

### Dependency Detection at Startup

Defined in `integration-guide.md`:

```
On /ssp invocation (silent, only interrupts when missing):

1. OpenSpec CLI → command -v openspec || npm list -g @fission-ai/openspec
   Missing → prompt: npm install -g @fission-ai/openspec@latest

2. planning-with-files → check if skill is available
   Missing → prompt: npx skills add OthmanAdi/planning-with-files

3. Superpowers → check if brainstorming / writing-plans / TDD sub-skills are available
   Missing → prompt: install superpowers via Cursor plugin marketplace

Any missing → show install command → stop workflow
```

### Uninstall Impact Matrix

| Action | Scope | Other modules |
|--------|-------|---------------|
| Uninstall spec-superpowers | Removes orchestration + gatekeeper | OpenSpec / planning / Superpowers each work independently |
| Upgrade OpenSpec | CLI updates | spec-superpowers unaffected |
| Upgrade Superpowers | Plugin updates | spec-superpowers unaffected |
| Upgrade planning-with-files | Skill files update | spec-superpowers unaffected |
| Upgrade spec-superpowers | Orchestration updates | Three modules unaffected |

## 9. Distribution

### Install

```bash
# Interactive
npx skills add CrDeemo/spec-superpowers

# Non-interactive (CI / new project)
npx skills add CrDeemo/spec-superpowers --skill spec-superpowers --agent cursor --global --yes

# Full setup (includes OpenSpec CLI + dependency prompts)
chmod +x install.sh && ./install.sh
```

### Uninstall

```bash
npx skills remove spec-superpowers
```

### Module Independent Upgrade

| Module | Upgrade command | Impact on skill |
|--------|----------------|-----------------|
| Superpowers | Cursor plugin auto-update | None |
| OpenSpec | `npm update -g @fission-ai/openspec` | None |
| planning-with-files | `npx skills update` | None |
| spec-superpowers | `npx skills update` | Orchestration only |

## 10. Quality Gates

Six gates total: G0-G3 for Light/Full, G1-Quick + G3-Quick for Quick mode.

| Gate | Position | Pass criteria | Failure handling |
|------|----------|--------------|-----------------|
| **G1-Quick** | Before Quick implementation | AI stated what/why/scope, user confirmed | Clarify → re-state → if scope grows, upgrade |
| **G3-Quick** | After Quick implementation | Tests pass + single-round review | Fix → re-review. 2 failures → suggest upgrade |
| **G0** | After session recovery | 5-Question Reboot Test consistent + no contradictions | Re-read files, re-test |
| **G1** | Step 3 → 4 | Brainstorming design approved + `openspec validate` passed + user confirmed (max 3 rounds) | Fix validation → revise spec → resubmit |
| **G2** | Step 4 → 5 | Files ready + every task annotated + review loop passed (max 3 rounds) | Fill gaps, re-check |
| **G3** | Step 5 → 6 | All tests pass + two-stage review + evidence in progress.md | 3-Strike → systematic-debugging → escalate |

## 11. Validation Script (test_skill.py)

~60 checks across 10 categories:

| # | Category | Checks |
|---|----------|--------|
| 1 | File existence | SKILL.md exists |
| 2 | YAML frontmatter | name/description present, name = spec-superpowers, triggers included, no forbidden fields |
| 3 | references/ | 4 files exist and non-empty (>100B) |
| 4 | assets/ | constitution.md exists |
| 5 | Internal links | All `](references/...)` and `](assets/...)` links resolve |
| 6 | Key content | Contains `/ssp`, complexity triage, pipeline steps |
| 7 | Line limit | SKILL.md ≤ 120 lines |
| 8 | No redundant concepts | No TDD-First / RED-GREEN-REFACTOR / SOLID (delegate to sub-skills) |
| 9 | Core features | Complexity triage, session recovery, quality gates, 5-Question Reboot, review loops, 3-Strike, dialogue-first |
| 10 | Dependency skills | Check using-superpowers, planning-with-files, brainstorming, writing-plans, TDD, verification-before-completion, systematic-debugging installed |

Supports `SKILL_DIR` and `SKILLS_ROOT` env vars. Exit code 0/1 for CI.

## 12. Install Scripts

### install.sh (macOS/Linux)

```
Step 1: Check npm → install OpenSpec CLI
Step 2: npx skills add spec-superpowers
Step 3: Prompt user to confirm Superpowers + planning-with-files installed
Step 4: Optional — copy gatekeeper rule to .cursor/rules/
```

Each step with `|| echo` fallback. Single-step failure does not abort.

### install.ps1 (Windows)

Same logic, PowerShell syntax.

## 13. Writing-Plans vs Planning-with-Files Responsibilities

Clear division of concerns:
- **writing-plans** (Superpowers) = Plan "Author" — generates content; quality criteria: each step 2-5 min, complete file paths, zero placeholders
- **planning-with-files** = Plan "Runtime" — persists to task_plan.md + hook-driven attention management (UserPromptSubmit, PreToolUse, PostToolUse, Stop hooks)
- Flow: writing-plans produces plan content → content formatted per planning-with-files' task_plan.md template → written directly into root task_plan.md → planning-with-files hooks auto-manage from here
- All plans unified in `.spec-tasks/<task>/task_plan.md`; no separate `docs/superpowers/plans/` file needed

## 14. File Inventory

| File | Purpose | Installed by npx |
|------|---------|:---:|
| `skills/spec-superpowers/SKILL.md` | Core orchestration | Yes |
| `skills/spec-superpowers/references/openspec-workflow.md` | OpenSpec detailed flow | Yes |
| `skills/spec-superpowers/references/planning-workflow.md` | planning-with-files detailed flow | Yes |
| `skills/spec-superpowers/references/quality-gates.md` | G0-G3 gate criteria | Yes |
| `skills/spec-superpowers/references/integration-guide.md` | Install / deps / troubleshooting | Yes |
| `skills/spec-superpowers/assets/templates/constitution.md` | Project constitution template | Yes |
| `.cursor/00-spec-superpowers.mdc` | Always-on gentle guide rule | No (manual copy) |
| `install.sh` | macOS/Linux installer | No |
| `install.ps1` | Windows installer | No |
| `test_skill.py` | Validation script | No |
| `README.md` | Documentation | No |
