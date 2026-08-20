---
name: job-application-tracker
description: Automatically syncs Gmail and Google Calendar with a Notion database to keep track of the status of job applications the user has submitted. Use this skill whenever the user asks to "sync my job applications," "update my job tracker," "check where my interviews stand," or something similar — even if they don't explicitly mention Notion, Gmail, or Calendar, and even if they don't have a Notion database set up for this yet. Requires (or guides the user through setting up) the Notion, Gmail, and Google Calendar MCP connectors.
---
 
# Job Application Tracker
 
A skill for keeping a Notion database of job applications up to date, by cross-referencing recent Gmail messages and Google Calendar events. Designed to be usable by anyone, including someone starting from scratch (no Notion database yet, connectors not yet linked).
 
## Step -1 — Ask preferred language (always do this first, before anything else)
 
Before doing anything else, ask the user whether they'd like your responses (status updates, reports, notes written into Notion, etc.) in **English** or **Italian**. Use whichever language they pick for the rest of the interaction, including the final report in Step 7 and any Notes written to Notion. If the user has already stated a language preference earlier in the conversation, you can skip re-asking and just confirm it briefly.
 
This choice also drives the language of the Notion table itself:
- If the user picks **Italian**, and you end up creating a brand-new database (Step 0.2), build it with the Italian column names and status options (see the Italian schema variant in Step 0.2).
- If the user picks **English**, use the English schema variant instead.
- If a database **already exists**, don't rename its existing columns just because of this answer — keep using whatever language/labels it already has (per Step 0.2's "different column names" case), and simply write Notes in the user's chosen language going forward.
## Step 0 — Check prerequisites (always do this first)
 
### 0.1 Connectors
Check whether you have access to **Notion**, **Gmail**, and **Google Calendar** tools. If one or more are missing:
- Use `search_mcp_registry` with relevant keywords (e.g. `["notion"]`, `["gmail", "email"]`, `["calendar"]`).
- Use `suggest_connectors` to let the user connect them.
- Gmail and Calendar are both useful but not both required: if the user wants to start with just one of the two (or neither, see 0.1b below), that's fine — flag it and proceed with what's available.
- Notion is the default backend, but it is **not mandatory**: if the user doesn't want to (or can't) connect Notion, don't block — switch to the **Excel fallback** described in 0.1a instead.
### 0.1a Fallback when Notion isn't available (Excel mode)
If, after being offered the connector, the user says they don't have/don't want Notion:
- Tell them you'll keep the tracker as a downloadable Excel file instead, and that — unlike the Notion mode — this mode has no persistent storage on your side: they'll need to re-upload the file each time they want a sync, and download the updated version afterwards.
- **First run**: use the `xlsx` skill to create a new spreadsheet with one sheet ("Applications"/"Candidature") using the same columns as the Notion schema in Step 0.2 (EN or IT variant, matching the language chosen in Step -1): `Company / Role / Application Status / Last Updated / Notes` (or the Italian equivalents). Save it to `/mnt/user-data/outputs/` and share it with `present_files`.
- **Subsequent runs**: ask the user to upload their current tracker file (or use one already present in `/mnt/user-data/uploads/` if they've just shared it). Read it with the `xlsx` skill, then treat each row exactly as you would a Notion page for the rest of this flow:
  - Step 4 (matching), Step 5 (status classification), and Step 6.5 (duplicate detection) all apply unchanged, just operating on spreadsheet rows instead of Notion pages.
  - Step 6 ("Write to Notion") becomes "write to Excel": add new rows / update matching rows' cells in place, keeping the same column order.
  - For 6.5 duplicate removal: since a spreadsheet has no "move out of the database" equivalent, actually delete the duplicate row from the sheet (keeping the same keep/remove logic — most recent `Last Updated`, tie-broken as described), rather than relabeling it. Mention in the final report which duplicate rows were deleted.
  - Save the updated file (new filename or same name, user's preference) to `/mnt/user-data/outputs/` and share it again with `present_files` at the end of the run.
- Everything else in the flow (Gmail scan, Calendar event creation, status classification rules, final report) works the same regardless of Notion vs. Excel mode.
- If the user changes their mind later and connects Notion, offer to import the existing Excel rows into a newly created Notion database (Step 0.2) as a one-time migration.
### 0.1b Fallback when Gmail isn't available
Calendar-based event detection (Step 3) and manual status updates can still work without Gmail. If Gmail isn't connected and the user doesn't want to connect it:
- Check `search_mcp_registry` for other email connectors (e.g. Outlook/other providers) in case one is available as a substitute for Gmail specifically — not just generic "email" keywords — and offer it via `suggest_connectors` if found.
- If no email connector is available at all, offer a **manual-input mode** for Step 2: ask the user to paste or summarize the relevant email content directly in chat (subject + body, or just a short description of what happened: "got a rejection from Acme today", "recruiter from Beta scheduled a call for Friday 3pm"). Classify status from that pasted/described text using the same rules as Step 5, instead of running `Gmail:search_threads`.
- If Calendar is connected but Gmail isn't, still run Step 3's logic in reverse where useful: use existing calendar events as signals for status/company matching, and rely on the manual-input mode above to fill in anything calendar events alone can't tell you (e.g. a rejection, which usually has no calendar trace).
- Always state clearly in the final report (Step 7) that Gmail wasn't used this run and that any status changes came from manual input rather than an automated scan, so the user knows the coverage was partial.
### 0.2 Notion database
Ask the user (or search yourself) whether a dedicated job-applications page/database already exists. Try `notion-search` with keywords like "applications", "job tracker", "interviews", "candidature".
 
**If no database exists:**
Offer to create one yourself, explain what you're about to do, and ask for confirmation before creating pages in the user's workspace. Create a page with an inline database using the schema matching the language chosen in Step -1 (it can be enriched if the user wants):
 
**English variant:**
 
| Property | Type | Notes |
|---|---|---|
| `Company` | title | company or agency name |
| `Role` | text | position applied for |
| `Application Status` | status | options: `No contact`, `Applied`, `HR Contact`, `Intro Call`, `Technical Test`, `Rejected`, `Offer Accepted` |
| `Last Updated` | date | date of the last detected status change |
| `Notes` | text | free-form summary of what happened / next steps |
 
**Italian variant:**
 
| Property | Type | Notes |
|---|---|---|
| `Azienda` | title | nome dell'azienda o dell'agenzia |
| `Ruolo` | text | posizione per cui si è candidati |
| `Stato Candidatura` | status | options: `Nessun contatto`, `Candidato`, `Contatto HR`, `Colloquio Conoscitivo`, `Test Tecnico`, `Rifiutato`, `Offerta Accettata` |
| `Ultimo Aggiornamento` | date | data dell'ultimo cambio di stato rilevato |
| `Note` | text | riepilogo libero di cosa è successo / prossimi passi |
 
[CRITICAL ORDERING RULE]: Whichever variant you use, you MUST define and inject these properties into the Notion API payload in the exact top-to-bottom sequence shown in the corresponding table above (title property, then role, then status, then date, then notes). Notion establishes the visual column order based strictly on the sequence of the creation object; do not scramble or alphabetize them.
 
Use `notion-create-pages` (or whichever database-creation tool is available) to generate it, then share the link with the user and ask for confirmation that it looks right before starting to populate it.
 
**If a database already exists but with different column names** (e.g. "Azienda" instead of "Company", "Stage" instead of "Application Status", or no Notes column at all):
- Adapt the matching to the real column names — don't assume they match the ones above. Always read the actual schema with `notion-fetch` on the data source before writing anything.
- If a column you need for useful information is missing (typically `Notes` or a last-updated date), propose adding it with `notion-update-data-source` (`ADD COLUMN ...`) **asking for confirmation before modifying the schema of an existing user database**.
- If the `Application Status` property has different or incomplete options compared to the table above, don't force the existing options: map the classification from Step 5 onto the closest available option, and if important stages are genuinely missing, propose (without imposing) adding them.
### 0.3 First run vs. subsequent syncs
If the database is empty or newly created, every application found will be a new row. If it already contains rows, run the matching described in Step 4 before deciding whether to create or update an entry.
 
## Execution flow (after Step 0)
 
### 1. Read the current state of the Notion database
- `notion-fetch` on the page URL/ID to find the inline database and its `data-source-url` (`collection://...`).
- `notion-fetch` on the data source to read the exact schema (property names, available status options) — never assume the names, always read them.
- Try reading existing rows with `notion-query-database-view` or `notion-query-data-sources` (SQL). **Note**: both tools require a Notion Business+ plan with Notion AI: if they fail with `validation_error`, use `notion-search` with `data_source_url` set to the data source to retrieve existing pages, or proceed by browsing the database view directly.
### 2. Scan Gmail (if connected)
Search with `Gmail:search_threads`, a query like:
```
newer_than:7d (application OR interview OR screening OR "intro call" OR "technical assessment" OR recruiter OR position OR offer OR hiring)
```
Adapt the keywords to whatever language(s) the user receives emails in (e.g. add Italian terms like "candidatura", "colloquio", "prova tecnica" if they're also applying to companies in Italy, or other languages as needed).
 
Default window "7d", or since the last sync date if known. For ambiguous threads, use `Gmail:get_thread` or `Gmail:get_message` to read the full body before classifying — don't rely on the snippet alone.
 
Discard clearly promotional/irrelevant emails (newsletters, generic platform alerts with no specific application behind them).
 
### 3. Scan Google Calendar (if connected)
`Google Calendar:list_events` for the current month (`startTime`/`endTime` first-to-last day of the month), including both past and future events. Look for interviews, calls, and screenings in the title/description/attendees.
 
### 3.5 Detect interview/call events missing from Calendar and add them
For every email found in Step 2 that describes a scheduled interview, call, or screening with a specific date/time (e.g. a calendar invite pasted in the body, a confirmed Teams/Meet/Zoom link with a date, a line like "see you Tuesday at 3pm"), check whether a matching event already exists in the events pulled in Step 3.
 
- **Matching check**: an email-derived event counts as "already on the calendar" if there's an existing event on the same date, with an overlapping or matching time (allow a small tolerance, e.g. ±15 minutes, for imprecise phrasing), and a title/attendee/description that plausibly refers to the same company or contact (use the same name-matching logic as Step 4).
- **If no matching event is found** → the interview is missing from the calendar. Automatically create it with `Google Calendar:create_event`, using:
  - Title: `Colloquio – <Company>` / `Interview – <Company>` (matching the user's chosen language), optionally adding the role if known.
  - Date/time: parsed from the email; if the email only gives a date with no time (or the time is ambiguous), don't guess a time — instead flag it in the final report as needing manual confirmation rather than creating an event with a fabricated time.
  - Description: a short note that this event was auto-created from an email, plus the sender/thread subject, so the user can trace it back.
  - Attendees: only add attendees if their email is unambiguous from the message (e.g. the recruiter's address); otherwise leave attendees empty rather than guessing.
- Do this automatically, without asking for confirmation first, since it's low-risk and reversible (the user can delete or edit the event from Calendar). Still, always list every auto-created event in the final report (Step 7) so the user can double check date/time and attendees.
- Never create a duplicate event: if you're unsure whether an existing event already covers this email (rather than confident it's missing), skip creation and mention the ambiguous case in the report instead of risking a duplicate.
### 4. Company ↔ Email/Event matching algorithm
For every email or event found:
1. Extract the sender's domain (`name@company.com` → `company`), strip TLDs (`.com`, `.io`, `.co`...) and common corporate suffixes (`inc`, `ltd`, `llc`, `group`, `srl`, `spa`...).
2. Compare the cleaned name against the "company" column of the database (whatever its real name is): match if one contains the other (case-insensitive).
3. **Recruiting platforms/agencies** (LinkedIn, Teamtailor, Greenhouse, Lever, Indeed, staffing agencies like Randstad/Adecco/Robert Half/Akkodis...): the sender's domain is NOT the company. Extract the real company name from the subject or body (e.g. "your application for [Role] at [Company]", or the client name mentioned in the text). If the agency doesn't name a specific client (a general/spontaneous application to the agency itself), use the agency name as the Company and note this in the Notes field.
4. If no matching row is found → this is a new application to create.
5. If a matching row is found → evaluate whether the status or notes need updating (see Step 5).
### 5. Status classification (rules)
Read the full subject + body of the email (or the calendar event description) and classify it according to these rules, from most recent/advanced. The labels below are the "standard" ones proposed in Step 0.2 (English and Italian variants): if the user's database uses different labels, map onto the closest concept.
 
| "Standard" status (EN) | "Standard" status (IT) | Typical signals |
|---|---|---|
| Rejected | Rifiutato | "we've decided not to move forward", "not the right fit at this time", explicit negative outcome |
| Offer Accepted | Offerta Accettata | signed/accepted job offer, confirmed contract |
| Technical Test | Test Tecnico | technical assessment, live coding, HackerRank/Codility, "test completed", interview with the engineering team |
| Intro Call | Colloquio Conoscitivo | invitation/confirmation of a call or interview (Teams/Meet/Zoom) with a recruiter or hiring manager, "intro chat", "first round" |
| HR Contact | Contatto HR | a recruiter has replied/written but without a call scheduled yet, request for more information, discussion about work mode/location |
| Applied | Candidato | automatic confirmation of application receipt ("thank you for applying", "we've received your resume"), no human contact yet |
| No Contact | Nessun contatto | application planned but not yet submitted (rarely used in this flow) |
 
Use the column that matches whichever variant (EN/IT) actually exists in the Notion database — don't mix languages within the same database.
 
Priority rules:
- If a thread contains multiple stages (e.g. application → then test → then call), always use the **latest stage reached**, not the first one.
- In case of genuine ambiguity between two adjacent statuses, prefer the one supported by the most recent, concrete signal (e.g. a calendar invite beats a vague mention in text).
- If the Notion schema doesn't have a status that accurately represents the situation, use the closest available status and **add the detail in Notes** instead of forcing a new status option into the schema, unless the user explicitly asks to expand the options.
### 6. Write to Notion
- **New application** → `notion-create-pages` with the `data_source_id` as parent. You MUST populate the page properties strictly respecting the established column order in the schema array/object:
  1. `Company`
  2. `Role`
  3. `Application Status`
  4. `Last Updated`
  5. `Notes`
     
  Never omit a property from the creation payload if it belongs to the standard schema, even if empty, to preserve the structural visual order.- **Existing application with a changed status** → `notion-update-page` (`command: update_properties`) on the matching page, updating status, notes, and date.
- Don't touch existing applications if there's no new signal from email/calendar.
### 6.5 Duplicate detection and removal
Before producing the final report, check the full set of rows read in Step 1 (plus anything just created/updated in Step 6) for duplicates: two or more rows referring to the same company (same cleaned name per the matching rules in Step 4).
 
- For each group of duplicate rows for the same company, keep **only the row with the most recent "Last Updated" date** and treat all the others as duplicates to remove.
  - If two duplicate rows are tied on "Last Updated" (same date), use the underlying page's actual last-edited timestamp (visible in `notion-search` results, or by comparing which row was just written in this run) as a tiebreaker, and keep the more recently edited one.
- **Removal mechanism**: this integration has no tool to permanently delete a Notion page. To "remove" a duplicate:
  1. Rename its title to prefix it clearly, e.g. `[DUPLICATO - da eliminare] <Company>` (adapt the language to the user's), so it's unambiguous and easy to find later.
  2. Use `notion-move-pages` to move it out of the database, to `{"type": "workspace"}` (private page at workspace level). This removes it from the tracked database/view without touching the row you're keeping.
- Never guess which row to keep based on content length or how detailed the notes look — always use the "Last Updated" date (with the edit-timestamp tiebreaker above) as the deciding factor.
- Do this automatically, without asking for confirmation first, since the action is reversible (the page still exists, just moved and relabeled, not deleted) and the criteria are deterministic. Still, always tell the user clearly in the final report which duplicates were found and that they were removed/moved (see Step 7), and mention that true permanent deletion isn't available via this integration — the person can delete the relabeled pages themselves from Notion's trash/sidebar if they want them gone for good.
### 7. Final report
Present the user with a text summary (a markdown table is fine) including:
- Applications added (company, role, status, brief reason)
- Applications updated (previous status → new, reason)
- Calendar events auto-created from emails that weren't already on the calendar (company, date/time, source email), plus any ambiguous cases (e.g. date without a clear time) that were flagged instead of auto-created
- Duplicates found and removed/moved (company, which row was kept vs. removed and why, i.e. the "Last Updated" dates compared), explicitly telling the user the duplicate records were removed/moved out of the database
- Any emails excluded as irrelevant (brief mention, no need to list them all)
- Any issues encountered (e.g. Notion tools unavailable on the current plan, missing connector, database created from scratch)
## Notes for first-time users
- You don't need everything set up in advance: if the database, connector, or a column is missing, the skill walks you through creating them step by step, asking for confirmation before making any change to your Notion workspace.
- If you're not sure what column names or statuses you want to use, the standard schema proposed in Step 0.2 works fine — you can always rename or expand it later, directly in Notion.
- If you also receive applications/interviews in other languages, mention it: the email search keywords in Step 2 should be adapted accordingly.
## Known limitations
- **Excel fallback (no Notion)**: works, but has no persistent storage — the user must re-upload their tracker file at the start of every sync and download the updated version at the end. Duplicate rows are actually deleted (not just relabeled/moved, as in the Notion mode).
- **Manual-input fallback (no Gmail)**: only as good as what the user pastes/describes in chat; there's no automated scan, so coverage is partial and depends on the user remembering to report updates.
- This skill doesn't run on its own: in a normal chat it needs to be triggered manually ("sync my job applications"). To run it automatically every N hours, you need **Claude Cowork** with a scheduled task (`/schedule`), pasting these instructions in. Note: full automation assumes Gmail/Calendar/Notion are all connected — the manual-input and Excel fallbacks above require the user's active participation each run, so they aren't well suited to unattended scheduling.
- `notion-query-database-view` and `notion-query-data-sources` require a Notion Business+ plan with Notion AI: if the workspace doesn't support it, matching against existing rows has to be done via `notion-search` or by browsing, with a higher margin of error.
- Generic alert emails (job alerts, newsletters from learning platforms) should never be treated as job applications.
- There's no tool available to permanently delete a Notion page. Duplicate rows (see Step 6.5) are relabeled and moved out of the database rather than deleted outright; the user can permanently delete them from Notion's own trash/sidebar if they want.
