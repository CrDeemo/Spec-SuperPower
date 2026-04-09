# OpenSpec Workflow

How spec-superpowers invokes brainstorming (Superpowers) + OpenSpec for specification (Phase 1) and archiving (Phase 4).

## Spec Artifact Location

All artifacts in `openspec/` at project root. Each task maps to one OpenSpec change:

```
openspec/changes/
  feat-user-auth/       ← task "feat-user-auth"
  fix-login-bug/        ← task "fix-login-bug"
```

Task name from `.spec-tasks/_active.txt` = change name. Managed natively by OpenSpec.

## Full Mode Flow

```
brainstorming (interactive design) → /opsx:propose → openspec validate → User Confirmation
```

1. **Brainstorm** — Read & invoke the `brainstorming` skill (Superpowers). Explore context, ask clarifying questions, propose 2-3 approaches with trade-offs, present recommended design, wait for user approval. Output: design document.
2. **Propose** — `/opsx:propose` to formalize the approved design into an OpenSpec change proposal + spec artifacts in `openspec/`
3. **Validate** — `openspec validate --change <name>` for structural completeness. Fix errors first.
4. **Confirm** — Present final spec to user, wait for explicit confirmation

## Light Mode Flow

```
brainstorming (shortened) → /opsx:propose → openspec validate → User Confirmation
```

Shortened brainstorming: present 2-3 approaches, user picks one, proceed. Skip deep context exploration. Steps 2-4 same as Full mode.

## Spec Confirmation Protocol

User must explicitly approve. Acceptable: "confirmed", "approved", "looks good", "lgtm", or equivalent affirmative. Ambiguous responses ("maybe", "I guess") do not count — ask again.

## Brainstorming Review Loop

After spec is written and validated, before user confirmation:

```
Spec written → openspec validate → dispatch spec-document-reviewer subagent
    ├─ Pass → present to user for confirmation
    └─ Fail → revise → re-validate → re-review (max 3 rounds → escalate to user)
```

Reviewer evaluates completeness, clarity, and feasibility against the brainstorming design document.

## Gate G1 Clearance

All three required:
1. Brainstorming design document approved by user
2. `openspec validate --change <name>` passes
3. User explicitly confirmed final spec

On user change request: revise → re-validate → re-review → resubmit for confirmation.

## Phase 4: Archive

After G3 passes:

```
openspec archive <change-name>
```

Merges change delta into main specs. Then: copy root planning files to `.spec-tasks/<task>/` → clean root files + `_active.txt`.

## Loose Coupling

References only stable interfaces: `brainstorming` skill (Superpowers), `/opsx:propose`, `/opsx:verify`, and `openspec/` directory convention. No internal CLI parameters or config formats.
