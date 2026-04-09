# spec-superpowers

[English](./README.md) | 中文

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
| `/spec-superpowers switch` | 切换到其他任务工作区 |
| `/spec-superpowers reset` | 清除当前任务状态，重新开始 |

#### `/spec-superpowers`

执行完整流水线：任务路由 → 复杂度分级 → 规范 → 计划 → 实现 → 归档。AI 会先分析任务并明确询问你确认复杂度级别（Light 或 Full），然后逐阶段引导，每个阶段之间都有质量门把关。这是新功能、Bug 修复、重构的默认入口。

#### `/spec-superpowers spec`

仅执行 Phase 1（OpenSpec 规范阶段）。适用于已有计划文件但需要创建或修订规范的场景。在规范通过验证并获得确认后停止于 Gate G1，不会进入计划或实现阶段。

#### `/spec-superpowers plan`

仅执行 Phase 2（计划阶段）。前提：`openspec/` 中已有确认的规范。适用于规范已就绪、需要生成或修订任务计划的场景。生成 `task_plan.md`、`findings.md`、`progress.md`。停止于 Gate G2。

#### `/spec-superpowers impl`

执行 Phase 3 + 4（实现和归档）。前提：项目根目录存在 `task_plan.md`。适用于规范和计划都已就绪、准备开始编码的场景。包含 TDD、代码审查和 3-Strike 错误升级协议。通过 Gate G3 后，自动通过 OpenSpec 归档。

#### `/spec-superpowers switch`

在任务工作区之间切换。显示 `.spec-tasks/` 中的现有任务列表，可选择切换或创建新任务。切换前会自动保存当前任务的计划文件（copy-swap）。适用于需要暂停当前任务、转去处理其他任务的场景。

#### `/spec-superpowers reset`

清除当前任务状态：删除根目录的计划文件（`task_plan.md`、`findings.md`、`progress.md`）和 `_active.txt`。`.spec-tasks/` 中的任务备份会保留。适用于想从头重新开始当前任务、或放弃当前工作流重新来过的场景。

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

AI 分析任务后会说明理由，并明确询问你确认复杂度级别，你可以确认或覆盖。

**Light**（必须全部满足）：影响 ≤2 个文件、无新公共 API、无架构变更、预估 <30 分钟。

**Full**：其他所有情况。架构变更、新外部依赖、数据库 schema 变更、安全相关变更、影响 >5 个文件时，AI 会直接告知使用 Full 模式并说明原因，不会询问是否用 Light。

AI 会在整个工作流中持续监测复杂度匹配度。如果任务比初始评估更简单或更复杂，AI 会主动建议调整并等待你确认。

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

## 项目结构

```
Spec-SuperPower/
  skills/
    spec-superpowers/
      SKILL.md                         核心编排（≤120 行）
      references/
        openspec-workflow.md           OpenSpec 集成 + validate/archive
        planning-workflow.md           任务工作区 + hooks + 职责划分
        quality-gates.md               G0-G3 标准 + 复杂度调整
        integration-guide.md           依赖 + FAQ
      assets/
        templates/
          constitution.md              项目宪法模板
  .cursor/
    00-spec-superpowers.mdc            常驻守门人规则
  install.sh                           macOS/Linux 安装脚本
  install.ps1                          Windows 安装脚本
  test_skill.py                        验证脚本（~70 项检查）
  README.md
  README.zh-CN.md
```

## 模块独立升级

| 模块 | 升级方式 | 对 Skill 的影响 |
|------|----------|------------------|
| Superpowers | Cursor 插件自动更新 | 无 |
| OpenSpec | `npm update -g @fission-ai/openspec` | 无 |
| planning-with-files | `npx skills update` | 无 |
| spec-superpowers | `npx skills add CrDeemo/Spec-SuperPower --skill spec-superpowers --agent cursor --yes` | 仅编排层 |

---

Built by CrDeemo
