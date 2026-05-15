# CLAUDE.md — Session Context
## ⚠️ READ THIS ENTIRE FILE BEFORE WRITING A SINGLE LINE OF CODE

This file is the brain of every Claude session.
It tells you (Claude) exactly where we are, what the rules are, and what to do today.

---

## PROJECT IDENTITY

**Name:** Basketball GM — European Edition
**Type:** PC desktop game (Python + Pygame)
**Goal:** Deep European basketball General Manager simulation
**Current Phase:** Phase 2: Core Systems (Phase 1 Foundation complete)

**Key files:**
- `GAME_DESIGN.md` — Full game design. The permanent source of truth. NEVER edit it.
- `ARCHITECTURE.md` — Technical decisions, file structure, rules.
- `PROGRESS.md` — What has been built and what works.
- `NEXT_STEPS.md` — What to build this session.
- `CLAUDE.md` — This file. Update at END of every session.

---

## SESSION STARTUP CHECKLIST

Every single session, in this order:
1. [ ] Read this file (CLAUDE.md)
2. [ ] Read PROGRESS.md — understand what is done
3. [ ] Read NEXT_STEPS.md — understand what to build today
4. [ ] Read the relevant existing source files before writing new code
5. [ ] Start building — only what NEXT_STEPS.md says

**If NEXT_STEPS.md is empty or unclear → ask the user before doing anything.**

---

## ARCHITECTURE RULES — NEVER VIOLATE

These rules prevent the "things stop fitting together" problem.

```
models/      → DATA ONLY. Defines what things ARE (Player, Team, Coach, Contract).
              No business logic. No display code. No database calls.

systems/     → LOGIC ONLY. Defines how things WORK (simulation, transfers, finances).
              No UI code. No direct user interaction. Calls models and database.

ui/          → DISPLAY ONLY. Shows things on screen. Calls systems — never models directly.
              No game calculations here. Ever.

database/    → DATABASE ACCESS ONLY. Read and write SQLite. Called by systems only.
```

**If you're unsure where code belongs → models/systems/ui/database. Pick one. Ask if unclear.**

### Additional Rules
- Every function must have a docstring comment explaining what it does
- No function longer than 40 lines — split it if it grows bigger
- Variable names in English
- Comments can be in Hebrew or English — use whatever is clearer
- Every screen = its own file in `ui/screens/`
- Every game mechanic = its own file in `systems/`
- Never duplicate logic — if it exists somewhere, import it

---

## GITHUB RULES

Commit after every working feature. Format:
```
[MODULE] Short description of what was added or fixed

Examples:
[MODELS] Add Player class with all attributes
[SIMULATION] Add quarter-by-quarter match engine
[UI] Add player profile screen
[TRANSFER] Add free agent list and offer system
[FIX] Fix contract length validation bug
```

**Never commit broken code to main.
If something is mid-development → commit to a feature branch.**

---

## TOKEN LIMIT PROTOCOL — WHEN APPROACHING 300,000 TOKENS

When this session is approaching its token limit, do this BEFORE ending:

1. **Update PROGRESS.md** — Mark everything completed this session as done
2. **Update NEXT_STEPS.md** — Write exactly what the next session should build (be specific)
3. **Update "Last Session" section** in this file (below)
4. **Commit everything** to GitHub with message: `[SESSION] Handoff — [brief summary]`
5. **Tell the user**: "Session limit approaching. All progress saved. Start a new session and I'll continue from where we left off."

The new session will read these files and know exactly what to do.

---

## CURRENT STATUS

**Overall Progress:** Phase 1 Foundation complete — DB seeded with 200 players, 12 teams
**Phase:** Phase 2 (Core Systems) — match simulation + season management next

---

## GAME DESIGN QUICK REFERENCE (from GAME_DESIGN.md)

- **Type:** GM simulation, worldwide leagues, European focus
- **Players:** Fictional names, realistic archetypes (designed for real-data upgrade later)
- **Leagues:** All world leagues + full NBA mode
- **Time:** Hybrid — "Next Day" button + "Next Event" skip
- **GM Career:** Reputation system, can be fired/resign, job market, own contract with owner
- **Owner:** 8 archetypes that combine (Investor, Trophy Hunter, Local Hero, Talent Developer, Prestige Seeker, Fan's Man, Hands-On, Hands-Off)
- **Coaching:** Head Coach communication, playing time conflict management
- **Scouting:** Head of Scouting staff member — GM gives requirements, HoS reports back needs
- **Academy:** Full deep system, separate budget, U21 in MVP
- **Agents:** Each player has an agent with personality
- **Finance:** 4-stage crisis system. NBA = relocation instead of bankruptcy
- **Relegation/Promotion:** Full system in all European leagues
- **Draft:** Full NBA draft system (scout prospects, trade picks, lottery)
- **UI:** Modern, clean, data-rich, bilingual Hebrew/English

---

## LAST SESSION SUMMARY

```
Date: 2026-05-15
Session #: 1
What was built: Phase 1 Foundation — project scaffolding, SQLite schema, all
                data models, deterministic seed loader. Integration test passes.
Files created/changed: requirements.txt, config.py, main.py, .gitignore,
                       database/{__init__,db,schema.sql}.py,
                       database/seed_data/{leagues,teams,name_pools}.json,
                       models/{__init__,player,team,coach,contract,league}.py,
                       systems/{__init__,bootstrap}.py,
                       PROGRESS.md, NEXT_STEPS.md, CLAUDE.md
Current game state: DB seeded with 1 league + 12 teams + 200 players + 168
                    contracts + 12 head coaches + 32 free agents.
Design decisions locked this session:
  - MVP league: Winner League (Israel), 12 teams, 22 regular games, 5 foreign cap
  - 29 player attributes (1-20): 11 technical, 5 physical, 5 mental, 5 hidden, 3 personality
  - Roster size: 14 (config.ROSTER_MAX_SIZE)
  - Determinism: config.SEED_RANDOM seeds player generation
Notes: pygame opens a placeholder window on `python main.py`. Use
       `python main.py --no-window` for headless verification.
```

---

## NEXT SESSION: DO THIS

→ See NEXT_STEPS.md for full task list

**Short version:** Build `systems/season.py` (schedule + advance day) and
`systems/simulation.py` (match engine). Test by simulating a full regular
season and printing the standings.

---

## KNOWN ISSUES / BLOCKERS

None yet.

---

## SESSION LOG

| # | Date | Summary | Completed |
|---|------|---------|-----------|
| 0 | Setup | Architecture documents created | ✅ |
| 1 | 2026-05-15 | Project setup + DB + models + seed data | ✅ |
| 2 | — | Systems: simulation + season | ⬜ |
| 3 | — | UI: main screens | ⬜ |
| 4 | — | Integration + save system | ⬜ |

---

## DESIGN CONSTRAINTS (from GAME_DESIGN.md — quick reference)

- GM controls: roster, contracts, staff, budget, scouting
- GM does NOT control: match tactics, substitutions, training sessions
- Player attributes: 1–20 scale, technical + mental + hidden
- League structure: 10–16 teams, ~32 games, playoffs
- Financial: owner sets budget, you must stay within it
- Contracts: 1–4 years, guaranteed/partial/non-guaranteed, loans possible
- Match simulation: statistics-based, no visual control

---

*This file is updated by Claude at the END of every session.*
*If you are starting a new session and this file looks outdated → check PROGRESS.md first.*
