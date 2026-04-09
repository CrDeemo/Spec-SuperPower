# Project Constitution

> **This is a template.** Copy it into your project and replace every `[YOUR_TARGET]` placeholder with a concrete value. Delete sections that don't apply, add sections that do. The constitution is a living document — update it as the project evolves.

---

## §1 Core Mission

**Project:** `[YOUR_TARGET — project name]`

**Mission:** `[YOUR_TARGET — one-sentence purpose statement]`

**Non-negotiable constraints:**

- `[YOUR_TARGET — e.g., must run offline, must support iOS 16+, must be GDPR compliant]`
- `[YOUR_TARGET]`
- `[YOUR_TARGET]`

Any change that violates a non-negotiable constraint is rejected regardless of other benefits.

---

## §2 Code Quality

### Naming Conventions

| Element | Convention |
|---------|-----------|
| Files | `[YOUR_TARGET — e.g., kebab-case.ts]` |
| Functions / methods | `[YOUR_TARGET — e.g., camelCase]` |
| Classes / types | `[YOUR_TARGET — e.g., PascalCase]` |
| Constants | `[YOUR_TARGET — e.g., UPPER_SNAKE_CASE]` |
| Test files | `[YOUR_TARGET — e.g., *.test.ts co-located]` |

### File Structure

```
[YOUR_TARGET — paste or describe your project's directory layout here]
```

### Error Handling

- **Approach:** `[YOUR_TARGET — e.g., Result types, exceptions with error boundaries, error codes]`
- **User-facing errors** must include an actionable message.
- **Internal errors** must log sufficient context for debugging (no swallowed errors).
- **Third-party calls** must have timeout and retry policy: `[YOUR_TARGET — e.g., 3 retries, exponential backoff, 10s max]`

---

## §3 Testing

| Metric | Target |
|--------|--------|
| Line coverage | `[YOUR_TARGET — e.g., ≥ 80%]` |
| Branch coverage | `[YOUR_TARGET — e.g., ≥ 70%]` |
| Critical-path coverage | `[YOUR_TARGET — e.g., 100%]` |

### Test Patterns

- **Unit tests** for pure logic and utilities — isolated, no I/O.
- **Integration tests** for module boundaries and API contracts.
- **E2E tests** for `[YOUR_TARGET — critical user journeys]`.
- Test runner: `[YOUR_TARGET — e.g., vitest, jest, pytest]`

### What Must Be Tested

- Every public function / exported API
- Error paths and edge cases
- Security-sensitive flows (auth, payments, data access)
- `[YOUR_TARGET — add project-specific requirements]`

---

## §4 Performance & Security

### Performance Budgets

| Metric | Budget |
|--------|--------|
| Page load (LCP) | `[YOUR_TARGET — e.g., < 2.5s]` |
| Time to Interactive | `[YOUR_TARGET — e.g., < 3.5s]` |
| Bundle size (JS) | `[YOUR_TARGET — e.g., < 200 KB gzipped]` |
| API response (p95) | `[YOUR_TARGET — e.g., < 300ms]` |
| Memory ceiling | `[YOUR_TARGET — e.g., < 512 MB RSS]` |

### Security Baseline

- Dependencies audited: `[YOUR_TARGET — e.g., npm audit on every CI run, zero critical/high]`
- Secrets management: `[YOUR_TARGET — e.g., environment variables only, never committed]`
- Auth mechanism: `[YOUR_TARGET — e.g., JWT with short-lived tokens + refresh rotation]`
- Input validation: all external input validated at the boundary before processing
- `[YOUR_TARGET — add project-specific security requirements]`

---

## §5 Document Separation

| Document type | Location | Contains | Does NOT contain |
|---------------|----------|----------|-----------------|
| **Specification** | `openspec/` | Requirements, scope, acceptance criteria | Implementation details, code |
| **Plan** | `task_plan.md` | Ordered tasks, file paths, test strategy | Reasoning, exploration notes |
| **Findings** | `findings.md` | Decisions, trade-offs, context discovered | Task status, test results |
| **Progress** | `progress.md` | Completion evidence, gate records | Specs, plans, decisions |
| **Code** | `src/` (or equivalent) | Implementation | Spec text, planning notes |
| **Constitution** | This file | Quality standards, project rules | Task-specific plans |

**Rule:** Each piece of information lives in exactly one place. If a fact appears in two documents, one of them is wrong — pick the canonical source and remove the duplicate.

---

## §6 File Persistence

These files must survive across sessions. Never delete them during normal workflow; they are the project's institutional memory.

| File | Purpose | Created in |
|------|---------|-----------|
| `task_plan.md` | Task checklist with acceptance criteria | Phase 2 (Planning) |
| `findings.md` | Decisions, trade-offs, discoveries | Phase 2 (Planning) |
| `progress.md` | Completion evidence, verification records | Phase 2 (Planning), updated in Phase 3 |
| This constitution | Quality standards and project rules | Project setup |

### Session Recovery

When a session resumes and `task_plan.md` exists, the agent runs the 5-Question Reboot Test against these files to rebuild context. Deleting or corrupting them breaks session recovery.

---

## §7 Project Configuration

| Setting | Value |
|---------|-------|
| Language / runtime | `[YOUR_TARGET — e.g., TypeScript 5.x / Node 20]` |
| Framework | `[YOUR_TARGET — e.g., Next.js 14, FastAPI, none]` |
| Package manager | `[YOUR_TARGET — e.g., pnpm, npm, poetry]` |
| Build system | `[YOUR_TARGET — e.g., Vite, Turbopack, Webpack]` |
| Linter | `[YOUR_TARGET — e.g., ESLint + Prettier]` |
| CI/CD | `[YOUR_TARGET — e.g., GitHub Actions]` |
| Deployment target | `[YOUR_TARGET — e.g., Vercel, AWS ECS, self-hosted]` |
| Key dependencies | `[YOUR_TARGET — list major libraries]` |

---

## §8 Gate-Section Mapping

This table shows which constitution sections each quality gate checks during evaluation.

| Gate | Checks | Constitution sections |
|------|--------|-----------------------|
| **G1** — Spec → Plan | Mission alignment + document separation | §1, §5 |
| **G2** — Plan → Impl | File persistence (planning artifacts ready) | §6 |
| **G3** — Impl → Archive | Code quality + testing + performance | §2, §3, §4 |

When a gate fails, consult the mapped sections to identify which standards were not met.
