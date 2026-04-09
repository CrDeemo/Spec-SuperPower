# OpenSpec Workflow

How spec-superpowers invokes OpenSpec for specification (Phase 1) and archiving (Phase 4).

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
/opsx:explore → /opsx:propose → openspec validate → User Confirmation
```

1. **Explore** — `/opsx:explore` to investigate problem space and brainstorm approaches
2. **Propose** — `/opsx:propose` to create change proposal + spec artifacts into `openspec/`
3. **Validate** — `openspec validate --change <name>` for structural completeness. Fix errors first.
4. **Confirm** — Present spec to user, wait for explicit confirmation

## Light Mode Flow

```
/opsx:propose → openspec validate → User Confirmation
```

Skip explore. Steps 2-4 same as Full mode.

## Spec Confirmation Protocol

User must explicitly approve. Acceptable: "confirmed", "approved", "looks good", "lgtm", or equivalent affirmative. Ambiguous responses ("maybe", "I guess") do not count — ask again.

## Brainstorming Review Loop

After spec is written and validated, before user confirmation:

```
Spec written → openspec validate → dispatch spec-document-reviewer subagent
    ├─ Pass → present to user for confirmation
    └─ Fail → revise → re-validate → re-review (max 3 rounds → escalate to user)
```

Reviewer uses the `brainstorming` skill to evaluate completeness, clarity, and feasibility.

## Gate G1 Clearance

All three required:
1. `openspec validate --change <name>` passes
2. Brainstorming review loop passed
3. User explicitly confirmed

On user change request: revise → re-validate → re-review → resubmit for confirmation.

## Phase 4: Archive

After G3 passes:

```
openspec archive <change-name>
```

Merges change delta into main specs. Then: copy root planning files to `.spec-tasks/<task>/` → clean root files + `_active.txt`.

## Loose Coupling

References only stable interfaces: `/opsx:explore`, `/opsx:propose`, `/opsx:verify`, and `openspec/` directory convention. No internal CLI parameters or config formats.
