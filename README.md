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

<details>
<summary><strong>🇨🇳 中文文档</strong></summary>

# spec-superpowers

一个 Cursor Agent Skill，将 **OpenSpec** + **planning-with-files** + **Superpowers** 编排为统一的规范驱动开发工作流。

松耦合设计 — 卸载此 Skill 不影响三个独立模块各自运行。

---

## 快速安装

在项目根目录执行：

```bash
# 一键安装（macOS / Linux）
curl -sSL https://raw.githubusercontent.com/CrDeemo/Spec-SuperPower/main/install.sh | bash

# 一键安装（Windows PowerShell）
irm https://raw.githubusercontent.com/CrDeemo/Spec-SuperPower/main/install.ps1 | iex
```

或分步手动安装：

```bash
# 1. 安装 OpenSpec CLI（全局，它是命令行工具）
npm install -g @fission-ai/openspec@latest

# 2. 安装 spec-superpowers skill（项目级）
npx skills add CrDeemo/Spec-SuperPower --skill spec-superpowers --agent cursor --yes

# 3. 安装 planning-with-files skill（项目级）
npx skills add OthmanAdi/planning-with-files --agent cursor --yes

# 4. 在 Cursor 插件市场安装 Superpowers（含子技能）

# 5.（可选）复制 gatekeeper 规则到项目
mkdir -p .cursor/rules
cp .cursor/skills/spec-superpowers/.cursor/00-spec-superpowers.mdc .cursor/rules/
```

安装完成后，重启 Cursor，在 Agent 聊天中输入 `/spec-superpowers` 即可开始。

## 卸载

```bash
# 仅移除 spec-superpowers（其他模块正常运行）
npx skills remove spec-superpowers

# 移除 gatekeeper 规则（如果之前复制过）
rm .cursor/rules/00-spec-superpowers.mdc

# 清理任务历史（可选）
rm -rf .spec-tasks/
```

卸载 spec-superpowers 只移除编排层。OpenSpec、planning-with-files、Superpowers 各自独立运行不受影响。

## 依赖

| 模块 | 类型 | 安装方式 |
|------|------|----------|
| **OpenSpec CLI** | 命令行工具 | `npm install -g @fission-ai/openspec@latest` |
| **planning-with-files** | Cursor Skill | `npx skills add OthmanAdi/planning-with-files --agent cursor --yes` |
| **Superpowers** | Cursor 插件 | Cursor 插件市场搜索安装 |

三个模块全部安装后可使用完整工作流。每个模块也支持独立使用。

## 使用方法

### 命令

| 命令 | 作用 |
|------|------|
| `/spec-superpowers` | 启动完整工作流（自动判断复杂度） |
| `/spec-superpowers spec` | 仅执行 OpenSpec 规范阶段 |
| `/spec-superpowers plan` | 仅执行计划阶段 |
| `/spec-superpowers impl` | 仅执行实现阶段 |
| `/spec-superpowers reset` | 重置复杂度选择和状态 |
| `/spec-superpowers escalate` | 工作流中途从 Light 升级为 Full |
| `/spec-superpowers simplify` | 工作流中途从 Full 降级为 Light |
| `/spec-superpowers switch` | 切换到其他任务工作区 |

### 工作流程

```
/spec-superpowers
    │
    ▼
Phase -1 — 任务路由
    检测活跃任务 或 创建新任务工作区 (.spec-tasks/)
    │
    ▼
Phase 0 — 会话恢复（自动）
    若存在先前会话，执行 5 问重启测试
    — 质量门 G0 —
    │
    ▼
Phase 1 — 规范（OpenSpec）
    Full: /opsx:explore → /opsx:propose → openspec validate → 用户确认
    Light: /opsx:propose → openspec validate → 用户确认
    — 质量门 G1: validate 通过 + 用户确认 + 审查循环 —
    │
    ▼
Phase 2 — 计划（writing-plans → planning-with-files）
    生成 task_plan.md / findings.md / progress.md
    — 质量门 G2: 文件就绪 + 审查循环 —
    │
    ▼
Phase 3 — 实现（Superpowers）
    Subagent-Driven 或 Executing-Plans，全程 TDD
    — 质量门 G3: 测试通过 + 审查 + 证据 —
    │
    ▼
Phase 4 — 归档
    openspec archive + copy-swap 计划文件 + 清理
```

### 复杂度分级

AI 建议 Light 或 Full，由你确认或覆盖。

**Light**（必须全部满足）：影响 ≤2 个文件、无新公共 API、无架构变更、预估 <30 分钟。

**Full**：其他所有情况。

工作流中途可通过 `/spec-superpowers escalate` 或 `/spec-superpowers simplify` 切换。

### 任务工作区

每个任务通过 `.spec-tasks/` 获得独立的计划上下文：

```
.spec-tasks/
  _active.txt          （当前任务名）
  feat-user-auth/      （计划文件备份）
  fix-login-bug/
  ...
```

根目录的计划文件（`task_plan.md`、`findings.md`、`progress.md`）始终是真实文件（copy-swap，非符号链接）。这意味着：
- planning-with-files 的 hook 原生兼容
- 卸载 spec-superpowers 后一切正常运作
- 无 Windows 符号链接权限问题

## 架构

- **薄编排层** — SKILL.md 只描述"调用谁、期望什么"，绝不内联模块内部逻辑
- **松耦合** — 仅引用稳定接口；零路径耦合；编排纯描述性
- **硬质量门** — G0-G3 在每个阶段转换处设有自动审查循环（最多 3 轮）
- **常驻守门人** — `.cursor/rules/00-spec-superpowers.mdc` 在无确认规范时阻止编码
- **任务隔离** — `.spec-tasks/` + copy-swap 防止不同任务间的上下文污染

## 模块独立升级

| 模块 | 升级方式 | 对 Skill 的影响 |
|------|----------|------------------|
| Superpowers | Cursor 插件自动更新 | 无 |
| OpenSpec | `npm update -g @fission-ai/openspec` | 无 |
| planning-with-files | `npx skills update` | 无 |
| spec-superpowers | `npx skills add CrDeemo/Spec-SuperPower --skill spec-superpowers --agent cursor --yes` | 仅编排层 |

</details>

---

Built by CrDeemo
