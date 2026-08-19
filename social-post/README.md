# 📬 Repo Social Poster (Claude Skill)

This repository contains the configuration files and operational instructions to enable the **Repo Social Poster** skill on your Claude assistant.

The skill turns a GitHub repository (from your starred lists or specified by hand) into a social media post draft — always starting from a 4-point interview (repo, tone, calendar event, target platform) and publishing **only after your explicit approval**.

---

## 🚀 Installation

### Option 1 (RECOMMENDED) - Any AI with skills support (Claude Code, opencode, Cursor, Copilot...)

1. Download/copy the `SKILL.md` file (and keep the `reference/` and `scripts/` folders).
2. Drop the `repo-social-poster/` folder where your assistant loads skills.
3. Restart your session and use it.

### Option 2: Continuous Automation with Claude Cowork

If you want to run a scheduled publishing workflow:

1. Open **Claude Cowork**.
2. Set up a scheduled task using the `/schedule` command.
3. Reference or load the downloaded skill file into the schedule body with your preferred recurrence interval.

---

## 📋 Prerequisites: MCP Connectors & Tokens

The skill relies on the Model Context Protocol (MCP) framework and environment variables. If anything is missing, Claude will guide you through setup:

- 🔑 **GITHUB_TOKEN** (Required to fetch repos and starred lists)
- 🔑 **ANTHROPIC_API_KEY** (Required to generate the text)
- 🔑 **LINKEDIN_ACCESS_TOKEN** + **LINKEDIN_AUTHOR_URN** (Optional: publish to LinkedIn via API)
- 📅 **Google Calendar Connector** (Optional: to create the scheduling event)

All credentials are read only from environment variables — never in clear text.

---

## ✅ The Problem This Solves

Sharing the open-source projects you follow shouldn't be a chore.

- **Good repos go unnoticed:** A starred repo your audience would love never reaches them without a well-crafted post.
- **Every audience is different:** A tone and format that work on LinkedIn are wrong for X or a developer community.
- **No repeat pipeline:** Posting what you find takes manual drafting every single time.

This skill removes the friction by turning a repo into an interview-driven, ready-to-approve draft — reusable by different people with different styles.

---

## 🎯 Usage

Just ask: *"Make a post for my latest starred repo"* or *"Draft a LinkedIn post for owner/repo"*. The assistant first interviews you on 4 points (repo, tone, calendar event, target), generates a draft in chat, and only after your explicit approval publishes it or saves it.

---

## ⚙️ How It Works

1. **Quick interview:** The skill always asks about repo source, tone, whether to create a calendar event, and target platform — unless you already provided them in the conversation.
2. **Data fetch:** It pulls the repo details (name, description, language, stars) via the GitHub REST or GraphQL API, including starred lists.
3. **Draft generation:** The text is generated combining the repo data, the chosen tone, and the target platform guidelines.
4. **Approval gate:** The draft is shown in chat — nothing is published yet.
5. **Publish/Save:** Only after explicit approval, the skill publishes via API (LinkedIn), saves the draft to `drafts/`, and/or creates the calendar event. Published repos are tracked in `posted_repos.json` so nothing is ever reposted.

---

## 🛠️ Troubleshooting & Limitations

- **No LinkedIn token:** The draft is saved to `drafts/YYYY-MM-DD-post.md` for you to publish manually.
- **No Google Calendar connector:** The event details are described in chat so you can add them manually.
- **Already-published repos:** Every published repo is recorded in `posted_repos.json` and will not be re-posted.
- **Missing GITHUB_TOKEN:** The assistant falls back to repos you specify manually by `owner/repo`.

## ☕️ Thank U

<a href="https://buymeacoffee.com/daliaabbr" target="_blank">
  <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" height="40">
</a>