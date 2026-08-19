# 🗺️ Project Roadmap Manager (Claude Skill)

This repository contains the operational instructions to enable the **Project Roadmap Manager** skill on your AI assistant.

The skill turns an approved project plan into a living `ROADMAP.md` file that your assistant keeps updated automatically as you build.

---

## 🚀 Installation

### Option 1 (RECOMMENDED) - Any AI with skills support (Claude Code, opencode, Cursor, Copilot...)

1. Download/copy the `SKILL.md` file.
2. Drop it into the folder where your assistant loads skills or custom instructions (skills folder, rules file, or project context).
3. (Optional) Paste the usage example from this README into your project's instructions.

### Option 2: Continuously maintained projects

1. Keep `SKILL.md` somewhere your assistant reads on every session.
2. Reference it in your project's context so the assistant checks the roadmap before and after every task.

---

## ✅ The Problem This Solves

- **Plans get abandoned:** Plans made in chat are forgotten by the next session.
- **No shared source of truth:** Progress lives in people's heads or scattered notes, so nobody — human or AI — knows what's done and what's next.
- **Manual tracking fatigue:** Updating statuses, ticking boxes, and recalculating progress is tedious and easy to forget.

This skill eliminates the friction by turning your plan into a `ROADMAP.md` file your assistant updates by itself, in the background of every working session.

---

## 🎯 Usage

Just ask: *"Make a plan for my restaurant booking app"* or *"Give me a roadmap for this project."* The assistant proposes the full plan first; only after you approve does it create `ROADMAP.md` in the project root.

---

## ⚙️ How It Works

1. **Plan proposal:** The assistant lays out phases, tasks, and order in chat before writing anything.
2. **Approval gate:** No file is created until you explicitly approve the plan.
3. **File creation:** A structured `ROADMAP.md` is written with the approved phases, checklists, and status badges.
4. **Automatic updates:** As work proceeds, the assistant:
   - ticks off tasks completed (`[x]`)
   - flips phase badges ✅ Done / 🚧 In Progress / ⬜ Planned / ⛔ Blocked
   - recalculates the overall completion percentage
   - appends new tasks or phases discovered during development, noting why in a short "Notes / Changes" line

> [!NOTE]
> **Language:** The roadmap is written in the same language you chat in. Switch language mid-project and the next update follows suit.

---

## 🛠️ Troubleshooting & Limitations

- **No project folder yet:** Fine — the skill simply waits and creates `ROADMAP.md` as soon as a project folder exists.
- **Existing ROADMAP.md:** If one is already present, it is loaded and treated as the plan rather than overwritten.
- **Scope creep:** The roadmap evolves with the project, but nothing is ever marked done unless it is functionally complete and verified.

## ☕️ Thank U

<a href="https://buymeacoffee.com/daliaabbr" target="_blank">
  <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" height="40">
</a>
