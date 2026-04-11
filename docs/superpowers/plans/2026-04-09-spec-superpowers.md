# spec-superpowers Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Cursor Agent Skill that orchestrates OpenSpec + planning-with-files + Superpowers into a unified, loosely coupled spec-driven workflow, distributable via `npx skills add CrDeemo/spec-superpowers`.

**Architecture:** Thin orchestration layer — SKILL.md (≤120 lines) handles command routing and pipeline flow, detailed procedures live in `references/*.md`. Always-on gatekeeper rule in `.cursor/00-spec-superpowers.mdc` intercepts coding without confirmed spec. Three iron rules enforce loose coupling: reference stable interfaces only, zero path coupling, purely descriptive orchestration.

**Tech Stack:** Markdown (SKILL.md, references, constitution), YAML frontmatter, Cursor Rules (.mdc), Bash (install.sh), PowerShell (install.ps1), Python (test_skill.py)

**Spec:** `docs/superpowers/specs/2026-04-09-spec-superpowers-design.md`

---

## File Structure

| File | Responsibility |
|------|---------------|
| `skills/spec-superpowers/SKILL.md` | Core orchestration: commands, complexity triage, pipeline phases, gate entry points, reference file index |
| `skills/spec-superpowers/references/openspec-workflow.md` | Detailed OpenSpec integration: /opsx:explore, /opsx:propose flow, spec confirmation protocol |
| `skills/spec-superpowers/references/planning-workflow.md` | Detailed planning-with-files integration: three-file generation, session recovery, 5-Question Reboot Test |
| `skills/spec-superpowers/references/quality-gates.md` | G0-G3 gate criteria, review loop mechanism, error escalation protocol, 3-Strike rule |
| `skills/spec-superpowers/references/integration-guide.md` | Dependency list, detection commands, install instructions, troubleshooting FAQ |
| `skills/spec-superpowers/assets/templates/constitution.md` | Project constitution template with placeholder sections for user customization |
| `.cursor/00-spec-superpowers.mdc` | Always-on gatekeeper: detect coding tasks, check for confirmed spec, block or pass |
| `install.sh` | macOS/Linux installer: OpenSpec CLI + skill install + dependency prompts |
| `install.ps1` | Windows installer: same logic, PowerShell syntax |
| `test_skill.py` | ~60 validation checks across 10 categories |
| `README.md` | English documentation: install, usage, commands, architecture, FAQ |

---

### Task 1: Initialize Repository

**Files:**
- Create: `.gitignore`
- Create: `README.md`

- [ ] **Step 1: Initialize git repo**

```bash
cd /Users/test/code/project/personalWorks/Spec-SuperPower
git init
```

- [ ] **Step 2: Create .gitignore**

```gitignore
.DS_Store
node_modules/
__pycache__/
*.pyc
.spec-mode
```

- [ ] **Step 3: Create initial README.md**

```markdown
# spec-superpowers

A Cursor Agent Skill that orchestrates OpenSpec + planning-with-files + Superpowers into a unified spec-driven development workflow. Loosely coupled — uninstalling does not affect independent modules.

## Install

```bash
npx skills add CrDeemo/spec-superpowers
```

Non-interactive install (for scripts/CI):

```bash
npx skills add CrDeemo/Spec-SuperPower --skill ssp --agent cursor --global --yes
```

## Dependency Skills

These must be installed separately:

- `using-superpowers` + sub-skills (brainstorming, writing-plans, TDD, code-review, etc.)
- `planning-with-files`
- OpenSpec CLI: `npm install -g @fission-ai/openspec@latest`

Optional helper scripts for external CLI tools:

```bash
# Linux / macOS
chmod +x install.sh && ./install.sh

# Windows PowerShell
.\install.ps1
```

## Usage

| Command | Effect |
|---------|--------|
| `/spec-superpowers` | Smart full workflow (auto complexity) |
| `/spec-superpowers spec` | OpenSpec specification phase only |
| `/spec-superpowers plan` | planning-with-files planning phase only |
| `/spec-superpowers impl` | Superpowers implementation phase only |
| `/spec-superpowers reset` | Reset state |

## How It Works

```
/spec-superpowers → Complexity Triage → Session Recovery (auto)
    → Specification (Phase 1, OpenSpec + review loop)
    → Persistent Planning (Phase 2, three-file + review loop)
    → TDD Implementation (Phase 3, Superpowers)
    → Archive (Phase 4)
```

## Architecture

- **Thin orchestration layer**: SKILL.md ≤120 lines, details in `references/`
- **Loose coupling**: Only references stable module interfaces, never copies internals
- **Hard quality gates**: G0-G3, nothing proceeds without passing
- **Always-on gatekeeper**: `.cursor/00-spec-superpowers.mdc` intercepts coding without spec

## Project Structure

```
spec-superpowers/
├── skills/
│   └── spec-superpowers/
│       ├── SKILL.md
│       ├── references/
│       │   ├── openspec-workflow.md
│       │   ├── planning-workflow.md
│       │   ├── quality-gates.md
│       │   └── integration-guide.md
│       └── assets/
│           └── templates/
│               └── constitution.md
├── .cursor/
│   └── 00-spec-superpowers.mdc
├── install.sh / install.ps1
├── test_skill.py
└── README.md
```

## Uninstall

```bash
npx skills remove spec-superpowers
```

Uninstalling only removes the orchestration layer. OpenSpec, planning-with-files, and Superpowers continue working independently.

---

Built by CrDeemo · 2026
```

- [ ] **Step 4: Commit**

```bash
git add .gitignore README.md docs/
git commit -m "init: repo with README and design spec"
```

---

### Task 2: Create SKILL.md

**Files:**
- Create: `skills/spec-superpowers/SKILL.md`

- [ ] **Step 1: Create directory structure**

```bash
mkdir -p skills/spec-superpowers/references
mkdir -p skills/spec-superpowers/assets/templates
```

- [ ] **Step 2: Write SKILL.md**

Write the core orchestration file. Must be ≤120 lines. Contains:
- YAML frontmatter with name, description (includes trigger words `/spec-superpowers`, `spec first`)
- Commands table (5 commands)
- Complexity triage (two levels: Light / Full)
- Pipeline overview (Phase 0-4 with gate references)
- Anti-Rush Protection
- Reference files index table (4 references + 1 asset)

Key constraints:
- No redundant concepts (no TDD-First, RED-GREEN-REFACTOR, SOLID, DRY, KISS)
- Only describe "call module X, expect output Y" — never inline module internals
- All detailed procedures delegated to `references/` files via markdown links

```markdown
---
name: spec-superpowers
description: >
  Orchestrates OpenSpec + planning-with-files + Superpowers into a unified spec-driven
  development workflow. Automatically triages complexity (light/full), recovers session
  context, and applies quality gates (G0-G3) with automated review loops at every stage.
  Use this skill when the user says "/spec-superpowers", "spec first", or starts any
  feature, bugfix, or refactor. Activate for any non-trivial code change to prevent
  skipping the design phase. Loosely coupled — uninstalling does not affect independent modules.
  Orchestrates: OpenSpec (OPSX) + planning-with-files + Superpowers (TDD, code review,
  verification, debugging, spec/plan review loops).
---

# Spec-Superpowers Orchestrator

Every feature, bugfix, and refactor goes through a specification phase first.

## Commands

| Command | Effect |
|---------|--------|
| `/spec-superpowers` | Smart full workflow (auto complexity) |
| `/spec-superpowers spec` | OpenSpec specification phase only |
| `/spec-superpowers plan` | planning-with-files planning phase only |
| `/spec-superpowers impl` | Superpowers implementation phase only |
| `/spec-superpowers reset` | Reset complexity choice and state |

## Step 1: Dependency Check

Verify all three modules are available before proceeding. If any is missing, show install command and stop. Details: [references/integration-guide.md](references/integration-guide.md)

## Step 2: Triage Complexity

AI suggests a level; user confirms or overrides.

| Level | When | Pipeline |
|-------|------|----------|
| **Light** | Single-file bugfix, typo, config | Simplified Phase 1-4 |
| **Full** | New feature, refactor, multi-file | All phases |

## Step 3: Execute the Pipeline

**Phase 0 — Session Recovery** (automatic)
If `task_plan.md` exists, run the 5-Question Reboot Test and resume from checkpoint.
Details: [references/planning-workflow.md](references/planning-workflow.md)

**Phase 1 — Specification** (OpenSpec)
Full: `/opsx:explore` → `/opsx:propose` → user confirms. Light: `/opsx:propose` only.
**Gate G1**: User confirmed + brainstorming review loop passed.
Details: [references/openspec-workflow.md](references/openspec-workflow.md)

**Phase 2 — Persistent Planning** (planning-with-files + writing-plans)
Generate task_plan.md / findings.md / progress.md. Each task: file paths + acceptance criteria + test strategy.
**Gate G2**: Three files ready + plan review loop passed.
Details: [references/planning-workflow.md](references/planning-workflow.md)

**Phase 3 — Implementation** (Superpowers)
Subagent-Driven or Executing-Plans. TDD throughout. Errors: 3-Strike → systematic-debugging.
**Gate G3**: All tests pass + review passed + evidence in progress.md.

**Phase 4 — Archive**
`finishing-a-development-branch` → update checkboxes → archive spec artifacts.

## Sub-command Jump

- `/spec-superpowers spec` → Phase 1 only, stop at G1
- `/spec-superpowers plan` → Phase 2 only (requires spec in `openspec/`), stop at G2
- `/spec-superpowers impl` → Phase 3 + 4 (requires `task_plan.md`)

## Quality Gates

Hard stops — nothing proceeds until all checks pass. Full criteria: [references/quality-gates.md](references/quality-gates.md)

## Anti-Rush Protection

If the user asks to skip the spec phase, politely decline and redirect to `/spec-superpowers`.

## Reference Files

| File | When to read |
|------|-------------|
| [references/quality-gates.md](references/quality-gates.md) | Evaluating any gate (G0-G3) |
| [references/openspec-workflow.md](references/openspec-workflow.md) | Running the OpenSpec flow |
| [references/planning-workflow.md](references/planning-workflow.md) | Running planning / session recovery |
| [references/integration-guide.md](references/integration-guide.md) | Setup, troubleshooting, dependency list |
| [assets/templates/constitution.md](assets/templates/constitution.md) | Project constitution template |
```

- [ ] **Step 3: Verify line count**

```bash
wc -l skills/spec-superpowers/SKILL.md
```

Expected: ≤120 lines. If over, trim descriptions.

- [ ] **Step 4: Commit**

```bash
git add skills/spec-superpowers/SKILL.md
git commit -m "feat: add core SKILL.md orchestration"
```

---

### Task 3: Create Reference Files

**Files:**
- Create: `skills/spec-superpowers/references/openspec-workflow.md`
- Create: `skills/spec-superpowers/references/planning-workflow.md`
- Create: `skills/spec-superpowers/references/quality-gates.md`
- Create: `skills/spec-superpowers/references/integration-guide.md`

- [ ] **Step 1: Write openspec-workflow.md**

Content must cover:
- OpenSpec as the fixed spec mode (no Spec-Kit dual-mode)
- Full mode flow: `/opsx:explore` → `/opsx:propose` → user confirmation
- Light mode flow: `/opsx:propose` one-step → user confirmation
- Spec confirmation protocol: user must explicitly say "confirmed" or equivalent
- Brainstorming review loop integration: after spec written, dispatch reviewer subagent (max 3 rounds)
- `openspec/` directory as the spec artifact location
- Only reference OpenSpec command names and directory conventions — never inline CLI parameters or internal config

- [ ] **Step 2: Write planning-workflow.md**

Content must cover:
- Three-file system: task_plan.md (numbered checklist), findings.md (discoveries), progress.md (status + evidence)
- Full mode: generate all three files
- Light mode: generate task_plan.md + minimal progress.md, skip findings.md
- Session recovery protocol: detect task_plan.md → 5-Question Reboot Test (Where am I? / Where am I going? / What's the goal? / What did I learn? / What did I do?) → resume from checkpoint
- Writing-plans review loop: after plan written, dispatch reviewer subagent (max 3 rounds)
- Each task must have: file paths, acceptance criteria, test strategy

- [ ] **Step 3: Write quality-gates.md**

Content must cover:
- G0 (after Phase 0): 5-Question Reboot Test consistent + no context contradictions
- G1 (Phase 1→2): user confirmed spec + brainstorming review loop passed (max 3 rounds)
- G2 (Phase 2→3): three files ready + every task has file paths / acceptance criteria / test strategy + writing-plans review loop passed (max 3 rounds)
- G3 (Phase 3→4): all tests pass + two-stage review (spec conformance → code quality) + verification evidence in progress.md
- Review loop mechanism: phase complete → reviewer subagent → pass/fail → fix → re-review (max 3) → escalate
- Error escalation protocol: Strike 1 standard fix → Strike 2 check spec alignment → Strike 3 systematic-debugging → escalate to user

- [ ] **Step 4: Write integration-guide.md**

Content must cover:
- Dependency list with install commands:
  - OpenSpec CLI: `npm install -g @fission-ai/openspec@latest`
  - planning-with-files: `npx skills add OthmanAdi/planning-with-files`
  - Superpowers: Cursor plugin marketplace
- Dependency detection at startup:
  - OpenSpec: `command -v openspec` or `npm list -g @fission-ai/openspec`
  - planning-with-files: check skill availability
  - Superpowers: check brainstorming / writing-plans / TDD availability
- Any missing → show install command → stop workflow
- Uninstall impact matrix
- Troubleshooting FAQ: not triggered? → check skills installed, restart Cursor. Context lost? → check task_plan.md. 3 errors? → automatic systematic-debugging

- [ ] **Step 5: Commit**

```bash
git add skills/spec-superpowers/references/
git commit -m "feat: add reference files (openspec, planning, gates, integration)"
```

---

### Task 4: Create Constitution Template

**Files:**
- Create: `skills/spec-superpowers/assets/templates/constitution.md`

- [ ] **Step 1: Write constitution.md**

Content must cover (all with `[YOUR_TARGET]` placeholders for user customization):
- Core Mission: project purpose and non-negotiable constraints
- Code Quality: naming, structure, error handling standards
- Testing: coverage targets, test patterns
- Performance & Security: performance budgets, security baseline
- Document Separation: spec vs plan vs code boundaries
- File Persistence: which files must survive across sessions
- Project Configuration: tech stack, dependencies
- Gate↔Section Mapping: which constitution sections each gate checks (G1→§1/§5, G2→§6, G3→§2/§3/§4)

- [ ] **Step 2: Commit**

```bash
git add skills/spec-superpowers/assets/
git commit -m "feat: add project constitution template"
```

---

### Task 5: Create Gatekeeper Rule

**Files:**
- Create: `.cursor/00-spec-superpowers.mdc`

- [ ] **Step 1: Write gatekeeper rule**

```markdown
---
description: "Spec-Superpowers gatekeeper: blocks coding without confirmed spec"
globs: "*"
alwaysApply: true
---

## Spec-Superpowers Gatekeeper

Any new feature, bugfix, or refactor must complete the spec workflow and receive explicit user confirmation before writing code.

**Detection logic:**
- Coding task identified → check for user-confirmed Spec
- No confirmed Spec → guide user: "Please run `/spec-superpowers` to start the specification workflow."
- User pushes to skip → politely decline: "The spec-superpowers workflow requires specification before implementation. Please run `/spec-superpowers` to start."

**Pass condition:** Confirmed spec exists — detect `openspec/` directory with spec files.

**Full workflow driven by `spec-superpowers` Skill. This rule is the always-on gatekeeper only.**
```

- [ ] **Step 2: Commit**

```bash
git add .cursor/
git commit -m "feat: add always-on gatekeeper rule"
```

---

### Task 6: Create Install Scripts

**Files:**
- Create: `install.sh`
- Create: `install.ps1`

- [ ] **Step 1: Write install.sh**

```bash
#!/bin/bash
set -e

echo "=== spec-superpowers Quick Install ==="
echo ""

# 1. OpenSpec CLI
echo "[1/3] Installing OpenSpec CLI..."
if command -v npm >/dev/null 2>&1; then
  npm install -g @fission-ai/openspec@latest || echo " ⚠ OpenSpec install failed. Please install Node.js first: https://nodejs.org/"
else
  echo " ⚠ npm not found. Please install Node.js first: https://nodejs.org/"
fi

# 2. Install this Skill
echo "[2/3] Installing spec-superpowers Skill..."
if command -v npx >/dev/null 2>&1; then
  npx skills add CrDeemo/Spec-SuperPower --skill ssp --agent cursor --global --yes || echo " ⚠ Skill install failed. Try manually: npx skills add CrDeemo/spec-superpowers"
else
  echo " ⚠ npx not found. Please install Node.js first: https://nodejs.org/"
fi

# 3. Dependency prompts
echo "[3/3] Dependency check..."
echo ""
echo " Please ensure these Cursor Skills are installed:"
echo " ─────────────────────────────────────"
echo " Required:"
echo "  • using-superpowers (with sub-skills)"
echo "  • planning-with-files"
echo " ─────────────────────────────────────"
echo ""
echo " Optional: copy gatekeeper rule"
echo " cp .cursor/00-spec-superpowers.mdc <your-project>/.cursor/rules/"
echo ""
echo "=== Install complete. Restart Cursor, then type /spec-superpowers ==="
```

- [ ] **Step 2: Make install.sh executable**

```bash
chmod +x install.sh
```

- [ ] **Step 3: Write install.ps1**

Same logic as install.sh, translated to PowerShell:
- Use `Get-Command` instead of `command -v`
- Use `$LASTEXITCODE` for error checking
- Use `Set-StrictMode -Version Latest` and `$ErrorActionPreference = "Continue"`

- [ ] **Step 4: Commit**

```bash
git add install.sh install.ps1
git commit -m "feat: add install scripts for macOS/Linux and Windows"
```

---

### Task 7: Create Validation Script

**Files:**
- Create: `test_skill.py`

- [ ] **Step 1: Write test_skill.py**

Pure Python, no external dependencies. ~60 checks across 10 categories:

**Category 1 — File existence:**
- SKILL.md exists at `SKILL_DIR` path

**Category 2 — YAML frontmatter:**
- Frontmatter present (regex match `^---\n(.*?)\n---`)
- `name:` field present
- `description:` field present
- `name` = `spec-superpowers`
- Trigger `/spec-superpowers` in description
- Trigger `spec first` in description
- No forbidden fields: `version:`, `license:`, `author:`, `compatibility:`

**Category 3 — references/ directory:**
- `references/` dir exists
- 4 files exist: `openspec-workflow.md`, `planning-workflow.md`, `quality-gates.md`, `integration-guide.md`
- Each file > 100 bytes

**Category 4 — assets/ directory:**
- `assets/templates/constitution.md` exists

**Category 5 — Internal links:**
- All `](references/...)` and `](assets/...)` links in SKILL.md resolve to existing files

**Category 6 — Key content:**
- Contains `/spec-superpowers` command
- Contains complexity triage (word "light" or "triage" or "complexity")
- Contains pipeline phases (word "phase" or "pipeline")

**Category 7 — Line limit:**
- SKILL.md ≤ 120 lines

**Category 8 — No redundant concepts:**
- Does not contain: TDD-First, RED-GREEN-REFACTOR, Clean Code, SOLID, DRY, KISS

**Category 9 — Core features:**
- Two-level complexity mentioned
- Session recovery mentioned
- Quality gates mentioned (G0 or G1)
- 5-Question or Reboot mentioned
- Review loop mentioned
- 3-Strike mentioned
- Subagent mentioned
- finishing / archive mentioned
- systematic-debugging or 3-Strike mentioned

**Category 10 — Dependency skills installed:**
- Check `SKILLS_ROOT` (default `~/.cursor/skills`) for: using-superpowers, planning-with-files, brainstorming, writing-plans, test-driven-development, verification-before-completion, systematic-debugging

Report format: PASS/FAIL per check, total summary, exit code 0/1.

- [ ] **Step 2: Run validation**

```bash
python test_skill.py
```

Expected: some dependency skill checks may FAIL (not all installed locally), but all structural checks should PASS.

- [ ] **Step 3: Commit**

```bash
git add test_skill.py
git commit -m "feat: add validation script (~60 checks)"
```

---

### Task 8: Self-Review and Final Verification

**Files:**
- Modify: any files with issues found during review

- [ ] **Step 1: Verify SKILL.md line count**

```bash
wc -l skills/spec-superpowers/SKILL.md
```

Expected: ≤120 lines.

- [ ] **Step 2: Verify all internal links resolve**

```bash
python -c "
import re, os
skill_dir = 'skills/spec-superpowers'
with open(os.path.join(skill_dir, 'SKILL.md')) as f:
    content = f.read()
links = re.findall(r'\]\(((?:references|assets)/[^)]+)\)', content)
for link in links:
    path = os.path.join(skill_dir, link)
    status = 'OK' if os.path.isfile(path) else 'MISSING'
    print(f'  {status}: {link}')
"
```

Expected: all OK.

- [ ] **Step 3: Run full test suite**

```bash
python test_skill.py
```

Review output. Fix any FAIL that should be PASS.

- [ ] **Step 4: Verify file inventory matches spec**

Check every file listed in spec Section 11 exists:

```bash
ls -la skills/spec-superpowers/SKILL.md
ls -la skills/spec-superpowers/references/openspec-workflow.md
ls -la skills/spec-superpowers/references/planning-workflow.md
ls -la skills/spec-superpowers/references/quality-gates.md
ls -la skills/spec-superpowers/references/integration-guide.md
ls -la skills/spec-superpowers/assets/templates/constitution.md
ls -la .cursor/00-spec-superpowers.mdc
ls -la install.sh
ls -la install.ps1
ls -la test_skill.py
ls -la README.md
```

- [ ] **Step 5: Final commit**

```bash
git add -A
git commit -m "chore: final review pass"
```
