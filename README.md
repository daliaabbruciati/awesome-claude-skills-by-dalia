# Awesome Claude Skills

A personal collection of Claude Code skills designed and developed by me.

Each skill lives in its own folder, named after the skill itself (e.g. `<skill-name>/`), and contains two files:

- `SKILL.md` — the file the assistant reads to learn the skill's purpose and behavior
- `README.md` — a human-readable description of the skill for people browsing the repo

## What are skills?

Skills are small, self-contained instruction files that give an AI assistant
(Claude Code, opencode, Cursor, Copilot, ...) reusable knowledge for specific
tasks. Drop a skill folder into your project and the assistant picks it up
automatically whenever the task matches.

## Getting started

1. Copy the `<skill-name>/` folder you want.
2. Drop it into the folder where your assistant loads skills or custom
   instructions (usually a `skills/` directory or project context).
3. Use it — or just reference it in your prompts.

## Philosophy

- Small and focused: one skill, one job.
- Readable: every `SKILL.md` is clear enough to be adapted, not black-boxed.
- Real-world tested: skills are built from everyday working sessions, not
  theory.

## License

MIT — feel free to use, adapt, and share.
