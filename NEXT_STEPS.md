# NEXT_STEPS.md — What to Build Next Session

## ⚠️ IMPORTANT: Complete GAME_DESIGN.md detail session FIRST

Before writing any code, the game design document needs to be finalized.
The user needs to review and expand GAME_DESIGN.md with all their specific ideas.

**Required before coding:** Full design conversation with the user covering:
- Specific leagues they want (Israeli basketball? European leagues?)
- Player attribute detail preferences  
- Any specific mechanics they want
- Visual style preferences

---

## Session 1 Objective: Project Foundation

*Start this ONLY after GAME_DESIGN.md is finalized with the user.*

### Tasks (in this exact order)

**Step 1 — Python project setup**
- Create `requirements.txt` with pygame dependency
- Create `config.py` with all constants (screen size, colors, frame rate)
- Create `main.py` as the entry point (just opens a window for now)
- Test: `python main.py` opens a blank game window

**Step 2 — Database schema**
- Create `database/schema.sql` with these tables:
  - `players` (id, name, age, position, all attributes)
  - `teams` (id, name, city, budget, attributes)
  - `coaches` (id, name, role, attributes, team_id)
  - `contracts` (id, player_id, team_id, salary, length, years_remaining)
  - `seasons` (id, year, current_day, phase)
  - `matches` (id, season_id, home_team_id, away_team_id, result, played)
- Create `database/db.py` with helper functions: connect(), create_tables(), query()

**Step 3 — Data models**
- Create `models/player.py` — Player class with all attributes from GAME_DESIGN.md
- Create `models/team.py` — Team class
- Create `models/coach.py` — Coach class
- Create `models/contract.py` — Contract class
- Create `models/league.py` — League and Season classes

**Step 4 — Seed data**
- Create `database/seed_data/players.json` with 200 fictional players
- Create `database/seed_data/teams.json` with 12 fictional teams
- Create `database/seed_data/leagues.json` with one league configuration

**Step 5 — Test it**
- Write a small test in main.py:
  - Load seed data into database
  - Read back all players from database
  - Print: team name, roster size, total salary
- If this works → Session 1 is complete

### Definition of Done for Session 1
- [ ] `python main.py` runs without errors
- [ ] A game window opens (even if blank)
- [ ] Database is created with correct tables
- [ ] 200 fictional players are in the database
- [ ] 12 teams are in the database
- [ ] Can read and print full roster of any team

### Do NOT build in Session 1
- Any UI screens (not yet)
- Match simulation (not yet)
- Transfer system (not yet)
- Save/load system (not yet)

One step at a time. Foundation first.

---

## Session 2 (planned — after Session 1 is done)

Goal: Match simulation engine + Season management
- `systems/simulation.py` — Calculate match result
- `systems/season.py` — Generate schedule, advance calendar
- Test: Simulate a full season for all teams, print final standings

---

## Session 3 (planned — after Session 2 is done)

Goal: First UI screens
- `ui/theme.py` — Design system
- `ui/components/` — Button, Table, Card
- `ui/screens/main_menu.py` — New game / Load game
- `ui/screens/team_screen.py` — Roster view
