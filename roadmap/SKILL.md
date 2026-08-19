---
name: roadmap
description: Create and maintain the project ROADMAP.md file. Use whenever the user wants to plan an app or project before starting work, after a plan has been agreed on and must be saved to disk, or when a task or phase from the roadmap is completed and the file needs to be updated.
---

# Roadmap Management

You are responsible for the project's ROADMAP.md file in the project root.
It is the single source of truth for what is planned, in progress, and done.

## When to create the file

1. The user asks for a plan/roadmap for a project or feature.
2. Propose the full plan **first** in chat: phases, tasks, and rough order.
3. Do **not** create ROADMAP.md until the user explicitly approves the plan.
4. Once approved, create ROADMAP.md at the project root with the structure below.

## Required structure

```markdown
# <Project Name> — Roadmap

> Status legend: ✅ Done · 🚧 In Progress · ⬜ Planned · ⛔ Blocked

## Progress

- **Phase X of Y** complete
- Overall completion: N%

## Phases

### Phase 1 — <Name>
- **Status:** ✅ | 🚧 | ⬜ | ⛔
- **Goal:** <one sentence>
- [ ] Task 1
- [ ] Task 2

### Phase 2 — <Name> ...
```

Rules:
- Each phase has: title, a one-line goal, a status badge, and a task checklist.
- Update the **Progress** summary whenever anything changes.
- Keep tasks concrete and atomic so "done" is clearly verifiable.

## Automatic updates (no user prompt needed)

While working on the project, keep the roadmap in sync:

- When a task is finished: tick its checkbox `[x]` and update affected statuses.
- When an entire phase is finished: flip its badge to ✅ and update the Progress section.
- When current work maps to a phase, mark that phase 🚧 before starting.
- When the plan evolves during development, add new tasks/phases as they are
  discovered, noting why in a short "Notes / Changes" line per phase.
- Never mark something done that is not functionally complete or verified.

## Status transitions

- ⬜ Planned → 🚧 In Progress → ✅ Done
- ⛔ Blocked: use only if something is stuck and needs help; leave a short note on the task.

## Final check

When you finish a task or deliver a milestone, state the updated completion percentage
and the next phase in your reply.