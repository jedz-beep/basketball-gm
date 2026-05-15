# NEXT_STEPS.md — What to Build Next Session

## Session 2 Objective: Match Simulation + Season Management

Phase 1 (Foundation) is complete. Session 2 builds the systems layer.

### Tasks (in this exact order)

**Step 1 — Season skeleton**
- Create `systems/season.py`:
  - `create_season(league_id, year)` — insert a row into `seasons`
  - `generate_schedule(season_id)` — double round-robin: 12 teams × 22 games each, written to `matches`
  - `advance_day(season_id)` — increment `current_day`; if a match scheduled for that day exists, simulate it
- Phase transitions: preseason → regular → playoffs → offseason (just the state for now)

**Step 2 — Match simulation engine**
- Create `systems/simulation.py`:
  - `simulate_match(home_team_id, away_team_id) -> (home_score, away_score)`
  - Pull each team's top-8 players by overall, weight by minutes (starters more)
  - Team rating = weighted average of relevant attributes (offense rating + defense rating)
  - Use home-court advantage (~+3 rating)
  - Score generated from rating differential + base of ~80 pts + noise
- Persist result back to `matches` (home_score, away_score, played=1)
- Keep the engine deterministic when given a seed (for testing)

**Step 3 — Standings**
- Create `systems/standings.py` (or fold into season.py):
  - `compute_standings(season_id)` — wins, losses, win%, point diff
  - Sorted list of teams

**Step 4 — Test in main.py**
- Replace the current integration print with:
  - Create a season for the seeded league
  - Generate full schedule
  - Loop: advance_day until phase = offseason
  - Print final standings: rank | team | W-L | win% | pt diff

### Definition of Done for Session 2
- [ ] `python main.py --no-window --simulate-season` runs end-to-end
- [ ] All 132 league games played (12 teams × 22 ÷ 2 doubled = 132 game rows)
- [ ] Standings table printed with no team having impossible stats (W+L = 22 for everyone)
- [ ] Top-prestige teams (Tel Aviv Lions, Jerusalem Stars) finish above average

### Do NOT build in Session 2
- Playoffs bracket (Session 2.5 or 3)
- UI (Session 3)
- Transfers, finance, scouting (later)
- Save/load (Phase 4)

---

## Session 3 (planned)

UI foundation: theme, components (button/table/card), main menu, dashboard, roster screen.

## Session 4 (planned)

Transfer market + contract negotiation + finance system.
