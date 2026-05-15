# ARCHITECTURE.md — Technical Decisions
## ADR-001: Basketball GM — European Edition

**Status:** Accepted
**Date:** 2026-05-15
**Project:** Basketball GM — European Edition

---

## Context

We are building a complex PC desktop game (sports management simulation).
The developer is not a programmer by training and uses Claude AI to write all code.
The primary risk is complexity getting out of control when systems interact.

Key requirements:
- Runs on desktop PC (Windows), not a browser
- Pleasant visual interface (menus, tables, charts)
- Maintainable by AI across many sessions without losing context
- Clean, readable code that Claude and humans can understand
- GitHub backup with clear history

---

## Technology Decision

### Language: Python 3.11+

**Why Python:**
- Claude writes excellent, clean Python code
- Claude can run Python in sandbox to test before sharing
- No compilation — instant feedback loop
- Human-readable even for non-programmers
- SQLite is built into Python (no external database server)
- Works on Windows with a simple installer

**Alternative considered:** Godot 4 + GDScript
Godot is excellent for games but adds an engine layer between the code and the logic.
For a management game (mostly UI + data, no real-time physics), Python is sufficient
and more transparent for AI-assisted development.

---

### Display: Pygame 2.x

**Why Pygame:**
- The standard Python game library, mature and stable
- 2D rendering sufficient for management game (lists, tables, charts, menus)
- No external game engine needed
- Claude handles pygame well
- Runs natively on Windows

**UI approach:** Custom UI component library (button.py, table.py, etc.)
We build our own components on top of pygame — this gives full control over look and feel.

---

### Database: SQLite (built into Python)

**Why SQLite:**
- No server, no installation — just a file
- Each save game = one .db file in `/saves/`
- Handles player stats, contracts, financials, history perfectly
- Claude can write SQL clearly

---

## File Structure

```
basketball_gm/                   ← Root project folder
│
├── CLAUDE.md                    ← AI reads this FIRST every session
├── GAME_DESIGN.md               ← Master design doc — NEVER edited
├── ARCHITECTURE.md              ← This file
├── PROGRESS.md                  ← What is done
├── NEXT_STEPS.md                ← What to build next session
├── README.md                    ← How to install and run the game
│
├── requirements.txt             ← Python packages (pygame, etc.)
├── main.py                      ← Entry point: python main.py
├── config.py                    ← All constants: screen size, colors, rates
│
├── database/
│   ├── db.py                    ← Database connection + helper functions
│   ├── schema.sql               ← All table definitions (run once to create DB)
│   └── seed_data/               ← Starting data loaded on new game
│       ├── players.json         ← Default player pool
│       ├── teams.json           ← League teams with attributes
│       └── leagues.json         ← League configuration
│
├── models/                      ← DATA STRUCTURES — what things ARE
│   ├── __init__.py
│   ├── player.py                ← Player class: attributes, position, status
│   ├── team.py                  ← Team: roster, budget, identity
│   ├── coach.py                 ← Coach: attributes, contract, staff role
│   ├── contract.py              ← Contract: terms, clauses, status
│   └── league.py                ← League + Season: schedule, standings, rounds
│
├── systems/                     ← GAME LOGIC — how things WORK
│   ├── __init__.py
│   ├── simulation.py            ← Match engine: calculates results, box scores
│   ├── season.py                ← Season flow: schedule, standings, playoffs
│   ├── transfer.py              ← Transfer window: search, offer, negotiate
│   ├── finance.py               ← Money: revenue, expenses, budget tracking
│   ├── development.py           ← Player growth: age curves, training effect
│   └── scouting.py              ← Scout system: discovering hidden players
│
├── ui/                          ← DISPLAY — how things LOOK
│   ├── __init__.py
│   ├── app.py                   ← Main UI manager: which screen is showing
│   ├── theme.py                 ← Design system: colors, fonts, spacing
│   ├── components/              ← Reusable UI pieces
│   │   ├── __init__.py
│   │   ├── button.py            ← Clickable button
│   │   ├── table.py             ← Sortable data table (players, standings)
│   │   ├── card.py              ← Info card (player card, team card)
│   │   └── chart.py             ← Simple bar/line chart for stats
│   └── screens/                 ← Full game screens
│       ├── __init__.py
│       ├── main_menu.py         ← New game / Load / Quit
│       ├── dashboard.py         ← Home screen with next game + news
│       ├── team_screen.py       ← Full roster view
│       ├── player_screen.py     ← Individual player deep dive
│       ├── transfer_screen.py   ← Transfer market + free agents
│       ├── negotiate_screen.py  ← Contract offer + player response
│       ├── staff_screen.py      ← Coaching staff management
│       ├── league_screen.py     ← Standings + schedule
│       ├── match_screen.py      ← Match result display
│       ├── finance_screen.py    ← Budget + revenue + expenses
│       ├── board_screen.py      ← Board objectives + satisfaction
│       └── scout_screen.py      ← Scouting interface
│
└── saves/                       ← Player save files
    └── .gitkeep                 ← Keeps folder in git even when empty
```

---

## Data Flow — The Only Allowed Direction

```
User interaction (click, keypress)
         ↓
  UI Screen captures event
         ↓
  UI calls a System function
         ↓
  System applies business logic
         ↓
  System reads/writes Models
         ↓
  System reads/writes Database (via database/db.py)
         ↓
  UI reads updated Model and redraws screen
```

### Hard Rules on Data Flow
- UI → System ✅ (allowed)
- System → Model ✅ (allowed)
- System → Database ✅ (allowed)
- UI → Model directly ❌ (NEVER — always go through a system)
- UI → Database directly ❌ (NEVER)
- Model → Database ❌ (NEVER — models don't know they're stored)
- Model → UI ❌ (NEVER — models don't know they're displayed)

---

## Module Responsibilities (one-sentence summary)

| File | One-line job |
|------|-------------|
| `main.py` | Start the game, create the window, run the game loop |
| `config.py` | All numbers and settings in one place (screen size, default salaries, etc.) |
| `database/db.py` | Open the database, provide read/write helper functions |
| `models/player.py` | Define what a Player is (attributes, position, name, etc.) |
| `models/team.py` | Define what a Team is (roster, name, city, budget) |
| `models/coach.py` | Define what a Coach is (skills, role, contract) |
| `models/contract.py` | Define what a Contract is (terms, length, clauses) |
| `models/league.py` | Define what a League/Season is (teams, schedule, standings) |
| `systems/simulation.py` | Calculate match result from two teams' attributes |
| `systems/season.py` | Advance the calendar, generate schedule, update standings |
| `systems/transfer.py` | Handle player transfers, free agent signings, loans |
| `systems/finance.py` | Track money: revenue coming in, wages going out |
| `systems/development.py` | Update player attributes at season end based on age and work ethic |
| `systems/scouting.py` | Let GM discover players based on scout quality |
| `ui/app.py` | Know which screen is showing, handle screen transitions |
| `ui/theme.py` | Define all colors, fonts, spacing — the visual design system |

---

## Save System

- New game → creates new `saves/[team_name]_[date].db` SQLite file
- Save = write current state to that .db file
- Load = open an existing .db file
- Auto-save: every in-game week (every 7 days passed in game)
- Multiple save slots allowed

---

## GitHub Workflow

### Repository Structure
```
.gitignore     — Exclude: saves/, __pycache__/, *.pyc, .env
README.md      — Installation instructions
```

### Branching
- `main` — Always a working, playable version
- `feature/[name]` — In-progress work (e.g. `feature/transfer-window`)
- Merge to main only when feature is complete and tested

### Commit Format
```
[MODULE] What was done

[MODELS] Add Player class with all 14 technical attributes
[SIMULATION] Implement quarter-by-quarter match engine
[UI] Add roster screen with sortable table
[TRANSFER] Add free agent search and contract offer
[FIX] Fix budget calculation when player is released mid-season
[SESSION] Handoff — transfer system complete, next: UI screens
```

### When to Commit
- After each file is created and working
- After each system is functional
- Before ending a session (always)

---

## Coding Standards

```python
# Every function has a docstring
def calculate_match_result(home_team, away_team):
    """
    Simulate a basketball match between two teams.
    Returns a MatchResult object with score, box score, and key events.
    home_team: Team model
    away_team: Team model
    """
    pass

# No function over 40 lines — split into helpers if needed
# Variable names in English
# Comments can be in English or Hebrew
```

---

## Development Phases

| Phase | Focus | Key Deliverables |
|-------|-------|-----------------|
| 1 — Foundation | Project setup + Data models | Python env, SQLite schema, Player/Team/Coach models |
| 2 — Core Systems | Game logic | Match simulation, season flow, contracts, finances |
| 3 — UI | All screens | 13 game screens built with pygame |
| 4 — Integration | Connect everything | All screens call real systems, save/load works |
| 5 — Polish | Game balance + bug fixes | Tuning, edge cases, visuals |
| 6 — MVP Release | Ship version 1.0 | All MVP features from GAME_DESIGN.md complete |

---

## Installation (for reference)

```bash
# Create Python virtual environment
python -m venv venv
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

`requirements.txt` will contain:
```
pygame==2.5.2
```

---

*Architecture locked. Changes require discussion and explicit approval.*
