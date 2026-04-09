# spec-superpowers Design Spec

A Cursor Agent Skill that orchestrates OpenSpec + planning-with-files + Superpowers into a unified spec-driven development workflow. Loosely coupled — uninstalling this skill does not affect the independent modules.

**Repo**: `CrDeemo/spec-superpowers`
**Reference**: [zxzvsdcj/spec-first-superpowers](https://github.com/zxzvsdcj/spec-first-superpowers)

---

## 1. Project Structure

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
│   └── 00-spec-superpowers.mdc                # Always-on gatekeeper rule
├── install.sh                                 # macOS/Linux one-click install
├── install.ps1                                # Windows one-click install
├── test_skill.py                              # Validation script (~60 checks)
└── README.md
```

`npx skills add` discovers `skills/` and installs only its contents. Root-level dev files (test_skill.py, install scripts) are not included.

## 2. Command System

| Command | Effect |
|---------|--------|
| `/spec-superpowers` | Smart full workflow (auto complexity) |
| `/spec-superpowers spec` | OpenSpec specification phase only |
| `/spec-superpowers plan` | planning-with-files planning phase only |
| `/spec-superpowers impl` | Superpowers implementation phase only |
| `/spec-superpowers reset` | Reset complexity choice and state |

## 3. Complexity Triage

Two levels. AI suggests; user confirms or overrides.

| Level | Trigger signals | Pipeline |
|-------|----------------|----------|
| **Light** | Single-file change, bugfix, config, typo | Phase 1 simplified (`/opsx:propose`) → Phase 2 simplified (task_plan.md + minimal progress.md) → Phase 3 → Phase 4 |
| **Full** | New feature, refactor, multi-file, architecture | Phase 0-4 all executed |

## 4. Pipeline (Full Mode)

```
/spec-superpowers
    │
    ▼
Phase 0 — Session Recovery (auto)
    Detect task_plan.md → exists → 5-Question Reboot Test → resume from checkpoint
    Not exists → continue
    │
    ▼
Phase 1 — Specification (OpenSpec)
    Full: /opsx:explore → /opsx:propose → user confirms
    Light: /opsx:propose one-step → user confirms
    ── Gate G1: user confirmed + brainstorming review loop passed (max 3 rounds) ──
    │
    ▼
Phase 2 — Persistent Planning (planning-with-files + writing-plans)
    Generate: task_plan.md / findings.md / progress.md
    Each task annotated: file paths + acceptance criteria + test strategy
    ── Gate G2: three files ready + plan review loop passed (max 3 rounds) ──
    │
    ▼
Phase 3 — Implementation (Superpowers)
    Strategy (AI recommends, user picks):
    • Subagent-Driven: independent subagent per task + two-stage review
    • Executing-Plans: batch execution + checkpoint reviews
    TDD throughout. Errors escalate: 3-Strike → systematic-debugging
    ── Gate G3: all tests pass + review passed + evidence in progress.md ──
    │
    ▼
Phase 4 — Archive
    finishing-a-development-branch → update checkboxes → archive spec artifacts
```

### Light Mode Adjustments

- Phase 1: `/opsx:propose` directly, skip `/opsx:explore`
- Phase 2: Generate `task_plan.md` only, skip findings.md. `progress.md` is still created (minimal, for G3 evidence).
- Phase 3 & 4: Same as full mode

### Sub-command Direct Jump

- `/spec-superpowers spec` → Enter Phase 1, stop at G1
- `/spec-superpowers plan` → Enter Phase 2 (requires spec to exist in `openspec/`), stop at G2
- `/spec-superpowers impl` → Enter Phase 3 (requires `task_plan.md` to exist), then complete Phase 4

## 5. Quality Gates

Four hard gates. Nothing proceeds until all checks pass.

| Gate | Position | Pass criteria | Failure handling |
|------|----------|--------------|-----------------|
| **G0** | After Phase 0 | 5-Question Reboot Test consistent + no context contradictions | Re-read files, re-test |
| **G1** | Phase 1 → 2 | User explicitly confirmed spec + brainstorming review loop passed (subagent, max 3 rounds) | Revise spec, resubmit for confirmation |
| **G2** | Phase 2 → 3 | Three files ready + every task has file paths / acceptance criteria / test strategy + writing-plans review loop passed (max 3 rounds) | Fill gaps, re-check |
| **G3** | Phase 3 → 4 | All tests pass + two-stage review passed (spec conformance → code quality) + verification evidence written to progress.md | 3-Strike → systematic-debugging → escalate to user |

### Review Loop Mechanism

```
Phase complete → dispatch reviewer subagent → review result
    ├─ Pass → gate clears
    └─ Fail → fix issues → re-review (max 3 rounds)
                            └─ 3 rounds still failing → escalate to user
```

### Error Escalation Protocol (Phase 3)

```
Error → Strike 1: standard fix
      → Strike 2: check spec alignment
      → Strike 3: trigger systematic-debugging
                    → still unresolved → challenge architecture → escalate to user
```

## 6. Gatekeeper Rule

File: `.cursor/00-spec-superpowers.mdc`

```yaml
---
description: "Spec-Superpowers gatekeeper: blocks coding without confirmed spec"
globs: "*"
alwaysApply: true
---
```

Behavior:
1. **Detect**: Non-trivial coding task identified → check for user-confirmed spec
2. **Block**: No confirmed spec → guide user to `/spec-superpowers`
3. **Anti-skip**: User pushes to skip → politely decline and redirect
4. **Pass**: Confirmed spec exists (detect `openspec/` directory + spec files) → allow coding

Fixed to OpenSpec mode only (no Spec-Kit / OpenSpec dual-mode switching).

## 7. Loose Coupling Architecture

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
On /spec-superpowers invocation:

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

## 8. Distribution

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

## 9. Validation Script (test_skill.py)

~60 checks across 10 categories:

| # | Category | Checks |
|---|----------|--------|
| 1 | File existence | SKILL.md exists |
| 2 | YAML frontmatter | name/description present, name = spec-superpowers, triggers included, no forbidden fields |
| 3 | references/ | 4 files exist and non-empty (>100B) |
| 4 | assets/ | constitution.md exists |
| 5 | Internal links | All `](references/...)` and `](assets/...)` links resolve |
| 6 | Key content | Contains `/spec-superpowers`, complexity triage, pipeline phases |
| 7 | Line limit | SKILL.md ≤ 120 lines |
| 8 | No redundant concepts | No TDD-First / RED-GREEN-REFACTOR / SOLID (delegate to sub-skills) |
| 9 | Core features | Two-level complexity, session recovery, quality gates, 5-Question Reboot, review loops, 3-Strike |
| 10 | Dependency skills | Check using-superpowers, planning-with-files, brainstorming, writing-plans, TDD, verification-before-completion, systematic-debugging installed |

Supports `SKILL_DIR` and `SKILLS_ROOT` env vars. Exit code 0/1 for CI.

## 10. Install Scripts

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

## 11. File Inventory

| File | Purpose | Installed by npx |
|------|---------|:---:|
| `skills/spec-superpowers/SKILL.md` | Core orchestration | Yes |
| `skills/spec-superpowers/references/openspec-workflow.md` | OpenSpec detailed flow | Yes |
| `skills/spec-superpowers/references/planning-workflow.md` | planning-with-files detailed flow | Yes |
| `skills/spec-superpowers/references/quality-gates.md` | G0-G3 gate criteria | Yes |
| `skills/spec-superpowers/references/integration-guide.md` | Install / deps / troubleshooting | Yes |
| `skills/spec-superpowers/assets/templates/constitution.md` | Project constitution template | Yes |
| `.cursor/00-spec-superpowers.mdc` | Always-on gatekeeper rule | No (manual copy) |
| `install.sh` | macOS/Linux installer | No |
| `install.ps1` | Windows installer | No |
| `test_skill.py` | Validation script | No |
| `README.md` | Documentation | No |
