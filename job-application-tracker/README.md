<img width="1376" height="700" alt="Gemini_Generated_Image_uy5f2puy5f2puy5f" src="https://github.com/user-attachments/assets/272b24d0-f2ea-4f93-92ba-c4c0160f6154" />

# 📃 Job Application Tracker (Claude Skill)

This repository contains the configuration files and operational instructions to enable the **Job Application Tracker** skill on your Claude assistant.

The skill allows you to completely automate updating a **Notion** database with your job applications by cross-referencing recent **Gmail** messages and **Google Calendar** events.

---

## 🚀 Installation

### Option 1 (RECOMMENDED) - Claude.ai (browser)

1. Download this repo as a ZIP
2. Go to **claude.ai → Sidebar → Customize → Skills → Upload a Skill**

### Option 2: Continuous Automation with Claude Cowork

If you want the background monitoring to run continuously without manual intervention:

1. Open **Claude Cowork**.
2. Set up a scheduled task using the `/schedule` command.
3. Reference or load the downloaded skill file directly into the schedule body, setting your preferred recurrence interval (e.g., every 12 hours or once a day).

---

## 📋 Prerequisites: MCP Connectors

The skill relies on the MCP (Model Context Protocol) framework. It requires access to three tools to perform fully. If any are missing, Claude will guide you through setup:

- 🛠️ **Notion Connector** (Required to store the data)
- 📧 **Gmail Connector** (To scan for replies and application receipts)
- 📅 **Google Calendar Connector** (To detect scheduled interviews and tests)

---

## ✅ The Problem This Solves

Keeping track of job hunt progress can quickly become a second full-time job.

- **The Inbox Black Hole:** Important updates, automated application receipts, and interview invites get buried under dozens of daily emails.
- **Manual Data Entry Fatigue:** Manually copying company names, roles, application dates, and status updates into a spreadsheet or database is tedious and easy to forget.
- **Disjointed Timelines:** Remembering exactly when an interview was scheduled or when a follow-up is due requires constantly jumping between your calendar, email, and tracking tool.
  This skill eliminates the friction by turning your AI assistant into an automated recruiter coordinator that keeps your tracking database perfectly synchronized in the background.

---

## 🎯 Usage

In Claude, you can invoke the skill by simply using the shortcut command:

```
/job-application-tracker
```

---

## ⚙️ How It Works

Once triggered, the skill orchestrates a multi-step workflow across your connected apps using the Model Context Protocol (MCP):

1. **Email Scan:** It securely scans your Gmail inbox for specific keywords (e.g., _"thank you for applying"_, _"interview invitation"_, _"proposta"_, _"colloquio"_) from the last few days to detect new applications or status updates.

> [!NOTE]
> **Bilingual Search Capabilities:** The email scanning phase is pre-configured to detect keywords in both **English and Italian** (e.g., _"thank you for applying"_, _"interview invitation"_, _"grazie per la tua candidatura"_, _"colloquio"_). If you primarily receive communications in a different language, simply inform the assistant during activation to adapt its search criteria.

2. **Calendar Cross-Reference:** It checks your Google Calendar for upcoming or recent events tagged as interviews, technical tests, or HR screenings.
3. **Data Extraction & Structuring:** The AI extracts key data points such as Company Name, Job Title, Salary Range (if mentioned), Application Date, Current Stage, and Next Steps.
4. **Notion Synchronization:**
   - It queries your existing Notion database to see if the company or role already exists.
   - If it's a new application, it creates a new entry.
   - If it's an update (e.g., an interview invite for an existing application), it automatically updates the status and logs the interview date.

---

## 🛠️ Troubleshooting & Limitations

- **Notion Account:** If you don't have a Notion account to store the data, the skill will create a downloadable PDF file with the data formatted in a table.
- **Notion Plans:** Certain advanced SQL query tools require a Notion Business plan. If a `validation_error` occurs, Claude will seamlessly switch to a standard indexed keyword search (`notion-search`).
- **Email Languages:** The skill is configured to scan for both English and Italian application terminology. If you receive communications in another language, just let Claude know during activation so it can expand its keyword criteria.

## ☕️ Thank U

<a href="https://buymeacoffee.com/daliaabbr" target="_blank">
  <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" height="40">
</a>
