# Roadmap Skill

A skill that turns an approved project plan into a living `ROADMAP.md` file.

## What it does
- When you ask an AI to plan an app or project, it proposes the full plan in chat first.
- Only after you approve does it create `ROADMAP.md` in the project root.
- From then on it keeps the file in sync **automatically**:
  - ticks off tasks as they're completed
  - flips phase badges ✅ Done / 🚧 In Progress / ⬜ Planned / ⛔ Blocked
  - updates the overall progress percentage
  - appends new tasks/phases discovered during development
- The roadmap follows the language of the conversation and evolves with the project.

## How to use it
The skill is plain, AI-agnostic instructions (`SKILL.md`). It works with any AI assistant that supports skills or custom instructions:
- Claude Code, opencode, Cursor, Copilot, or anything similar — drop `SKILL.md` into the folder where your assistant loads skills/instructions, or paste its contents into a project's rules/context.

## Suggested usage
Just say something like: *"Make a plan for my restaurant booking app"* or *"Give me a roadmap for this project"* — the skill handles the rest.