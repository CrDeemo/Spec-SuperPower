# Quality Gates

Four hard gates govern the spec-superpowers pipeline. Nothing proceeds until all checks pass.

## Gate G0 — Session Recovery

| Field | Value |
|-------|-------|
| **Position** | After Phase 0 |
| **Trigger** | `task_plan.md` detected in project root, session recovery executed |
| **Pass** | 5-Question Reboot Test answers are consistent + no context contradictions |
| **Fail** | Re-read all planning files, run the reboot test again |

### Pass Criteria Detail

The 5-Question Reboot Test must produce answers that are internally consistent:

1. Checked tasks in task_plan.md match progress.md entries
2. The next unchecked task is a logical continuation
3. The overall goal aligns with the spec in `openspec/`
4. Findings in findings.md do not contradict the current code state
5. No orphaned progress (work recorded but not reflected in code)

### Failure Handling

Re-read `task_plan.md`, `findings.md`, and `progress.md`. Run the 5-Question Reboot Test again. If still inconsistent, present the contradictions to the user for resolution.

---

## Gate G1 — Specification to Planning

| Field | Value |
|-------|-------|
| **Position** | Phase 1 → Phase 2 |
| **Trigger** | Spec written by OpenSpec (artifacts in `openspec/`) |
| **Pass** | User explicitly confirmed spec + brainstorming review loop passed |
| **Fail** | Revise spec based on reviewer feedback, resubmit for user confirmation |

### Pass Criteria Detail

Two conditions must both be true:

1. **User confirmation** — The user said "confirmed", "approved", "looks good", "lgtm", or equivalent. Ambiguous responses do not count.
2. **Brainstorming review loop** — A spec-document-reviewer subagent reviewed the spec and approved it (max 3 rounds).

### Failure Handling

- If the reviewer rejects: fix the identified issues, resubmit to reviewer
- If the user requests changes: revise the spec, re-run the review loop, then ask for confirmation again
- After 3 review rounds still failing: escalate to user with the outstanding issues

---

## Gate G2 — Planning to Implementation

| Field | Value |
|-------|-------|
| **Position** | Phase 2 → Phase 3 |
| **Trigger** | Planning complete |
| **Pass** | Planning files ready + every task fully annotated + writing-plans review loop passed |
| **Fail** | Fill gaps in plan, re-check |

### Pass Criteria Detail

1. **Files exist**:
   - Full mode: `task_plan.md` + `findings.md` + `progress.md`
   - Light mode: `task_plan.md` + `progress.md` (minimal)
2. **Task annotations** — Every task in task_plan.md has:
   - File paths (which files to create/modify)
   - Acceptance criteria (what "done" looks like)
   - Test strategy (how to verify completion)
3. **Writing-plans review loop** — A plan-document-reviewer subagent reviewed the plan and approved it (max 3 rounds).

### Failure Handling

- If any task is missing file paths, acceptance criteria, or test strategy: fill the gaps
- If the reviewer identifies issues: fix and resubmit
- After 3 review rounds still failing: escalate to user with the outstanding issues

---

## Gate G3 — Implementation to Archive

| Field | Value |
|-------|-------|
| **Position** | Phase 3 → Phase 4 |
| **Trigger** | Implementation complete |
| **Pass** | All tests pass + two-stage review passed + verification evidence in progress.md |
| **Fail** | Errors escalate through 3-Strike protocol |

### Pass Criteria Detail

1. **All tests pass** — Every test defined in the task plan runs successfully
2. **Two-stage review** — Both stages must pass:
   - Stage 1: Spec conformance (does the implementation match the spec?)
   - Stage 2: Code quality (does the code meet quality standards?)
3. **Verification evidence** — Results written to `progress.md` using the `verification-before-completion` skill

### Failure Handling

Errors escalate through the 3-Strike protocol (see below). If all recovery attempts fail, escalate to user.

---

## Review Loop Mechanism

All gates with review loops follow the same pattern:

```
Phase complete → dispatch reviewer subagent → review result
    ├─ Pass → gate clears
    └─ Fail → fix issues → re-review (max 3 rounds)
                            └─ 3 rounds still failing → escalate to user
```

| Gate | Reviewer | Skill Used |
|------|----------|-----------|
| G1 | spec-document-reviewer subagent | `brainstorming` |
| G2 | plan-document-reviewer subagent | `writing-plans` |
| G3 | code-reviewer subagent (two-stage) | `requesting-code-review` |

The reviewer subagent is dispatched automatically. The orchestrator does not proceed until the reviewer returns a pass or the round limit is reached.

---

## Error Escalation Protocol (Phase 3)

When an error occurs during implementation, follow this escalation path:

```
Error detected
    │
    ▼
Strike 1 — Standard fix attempt
    Fix the error using normal debugging.
    │
    ├─ Fixed → continue implementation
    └─ Still broken ↓
    │
    ▼
Strike 2 — Check spec alignment
    Verify the implementation hasn't drifted from the spec.
    Compare current code against openspec/ artifacts.
    │
    ├─ Drift found → realign with spec → retry
    └─ No drift, still broken ↓
    │
    ▼
Strike 3 — Trigger systematic-debugging
    Invoke the systematic-debugging skill for deep investigation.
    │
    ├─ Resolved → continue implementation
    └─ Still unresolved ↓
    │
    ▼
Challenge architecture assumptions
    Question whether the spec's approach is fundamentally sound.
    │
    ▼
Escalate to user for decision
    Present findings, failed attempts, and ask the user
    whether to revise the spec or take a different approach.
```

Each strike is logged in `progress.md` for audit purposes.
