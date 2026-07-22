# Nook Listing Engine

Shared task board for Nook Realty's seller-listing lead-gen plan. Live board: https://racinel200.github.io/nook-listing-engine/

Two kinds of tasks:

- **JEN** — things only Jen can do (decisions, approvals, access, filming, meetings). She marks them done on the board (the ✓ button opens a pre-filled GitHub issue titled `DONE: <task-id>` — just submit it) or by telling Claude in chat. Completing a Jen task often unlocks AI tasks.
- **AI** — things the AI worker does on its own: drafting, research, specs, reports. An hourly scheduled Claude session reads `tasks.json`, picks up to 3 unblocked AI tasks, does the work, writes deliverables to `/deliverables`, logs to `activity.json`, and updates the board. If nothing is actionable it exits without changes.

## How the site renders

`index.html` fetches `tasks.json` + `activity.json` live (same origin on GitHub Pages), so **updating those two JSON files IS updating the site** — no build step. The embedded data blocks in `index.html` are only a fallback for offline previews; `build.py` injects them if a self-contained snapshot is ever needed.

## Ground rules for the worker

1. `tasks.json` is the single source of truth for task state. Updates happen through the GitHub connection (Zapier `create_file` with the current file `sha` — fetch it first with `get_file_contents`).
2. **Check-off reconciliation:** open GitHub issues titled `DONE: <task-id>` mean Jen completed that task — set it `done`, stamp `result`, flip newly-unblocked tasks from `blocked` to `todo`, add the issue number to `meta.processedIssues`, and leave a one-line comment on the issue. (Issues may stay open; `processedIssues` is what prevents double-counting.)
3. **Never** send emails, publish pages, spend money, or write to the CRM/email tools from a scheduled run. Draft it, save it, and queue the send/publish as the Jen approval task it belongs to.
4. **No client PII in this public repo.** Lead/client names and CRM details stay in the private Claude project; board entries, activity, and deliverables reference them generically ("review batch #1", "stage-hygiene report — see project").
5. Never mark a task `done` unless the work is actually complete and saved. Partial work stays `todo` with a note in `activity.json`.
6. Max 3 AI tasks per run. Small and steady beats big and stalled.

## Files

- `tasks.json` — the board (categories, tasks, deps, status, `meta.processedIssues`)
- `activity.json` — the worker's public activity log (newest last)
- `index.html` — the site (GitHub Pages), renders the JSON live
- `build.py` — optional: bakes the JSON into `index.html` for offline snapshots
- `deliverables/` — drafts and research the worker produces

Plans this board was built from live in the private Claude project: `claude/seller-listing-lead-plan.md`, `claude/competitor-listing-playbook.md`, `claude/business-profile.md`.
