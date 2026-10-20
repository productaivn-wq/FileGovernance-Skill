# 35_FILE_GOVERNANCE_SKILL organization contract

This project follows DocumentOrganizer's universal MECE lifecycle model.

## Required zones

- `00_INBOX/` — unresolved material awaiting classification.
- `10_ACTIVE_TIMEBOUND/` — active projects, sprint plans, milestones with an end state.
- `20_ACTIVE_CONTINUOUS/` — maintained governance standards, recurring operations, cadence checklists.
- `30_REFERENCE/` — reusable PM templates, frameworks, specifications, reference assets.
- `40_ARCHIVE/` — historical deliverables, completed sprints, superseded roadmaps.

Hidden version control metadata (`.git`, `.gitignore`) and metadata cache remain at the root under standard exclusion rules. Environment files (`.env`, `.env.example`) remain at the root as standard tooling exceptions. Local workspace rules (`GEMINI.md`, `AGENTS.md`), local agent configuration (`.agents/`), agent execution tracking files (`task.md`, `walkthrough.md`), session cache (`hot.md`), and append-only audit log (`log.md`) remain at the root for workspace governance and session tracking.

## Naming standard

New curated documents use:

`35.SSS.TT[.TT] - YYYYMMDD - Semantic_Title.ext`

Purpose tags:
- `IN`: Investigate (Research, exploratory data)
- `PL`: Plan (Strategy, PRDs, roadmaps)
- `BU`: Build (Code, architecture, designs)
- `CH`: Check (QA, audits, test results)
- `SH`: Share (Decks, memos, meeting notes)
- `RE`: Record (Preserve for reference/history)

## Depth standard

Managed documents use exactly three total layers, including the project itself:

1. project root;
2. lifecycle zone;
3. document file.

When the project root is counted as layer 0, a managed file has relative depth 2: `zone/document.ext`. Any category folder between a zone and a managed document is prohibited.

## Rules

1. New visible top-level folders are prohibited outside the five zones, `data/`, `watchers/`, `scripts/`, and `scratch/`.
2. Resolve paths from the repository or file location; never embed a drive-specific project path in portable code.
3. Never delete ambiguous content; route it to `00_INBOX/`.
4. Verify SHA-256 hashes before treating files as duplicates.
5. `40_ARCHIVE/` is read-only.
