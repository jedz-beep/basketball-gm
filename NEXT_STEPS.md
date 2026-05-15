# NEXT_STEPS.md — What to Build Next Session

## Session 3 Objective: UI Foundation

Phase 2 core systems (season + simulation) are working. Time to start the UI.

### Tasks (in this exact order)

**Step 1 — Theme & components**
- Create `ui/theme.py` — fonts, spacing constants, helper to lookup color by role
- Create `ui/components/button.py` — clickable rect with hover/press states
- Create `ui/components/table.py` — sortable column headers, scrollable rows
- Create `ui/components/card.py` — bordered surface with title + body
- Use config.COLOR_* constants; do NOT define new colors in components

**Step 2 — App / screen manager**
- Create `ui/app.py` — top-level loop, current screen, screen transitions
- Each screen is a class with `handle_event(event)` and `draw(surface)` methods
- Rewrite `main.py` to delegate the pygame loop to `ui.app.App`

**Step 3 — First screens**
- `ui/screens/main_menu.py` — buttons: New Career, Load Game, Quit
- `ui/screens/dashboard.py` — placeholder hub: shows season info, next match line
- `ui/screens/team_screen.py` — roster table for the user's team (read from DB)
- `ui/screens/league_screen.py` — standings table reusing `season.compute_standings`

**Step 4 — Wire flow**
- New Career → Dashboard
- Dashboard has buttons that navigate to Team, League screens
- Each screen has a "Back" button to Dashboard

### Definition of Done for Session 3
- [ ] `python main.py` opens the window directly to Main Menu
- [ ] Clicking "New Career" goes to Dashboard
- [ ] Dashboard shows current season + buttons to Team and League
- [ ] Team screen shows your roster in a sortable table
- [ ] League screen shows the standings (after simulating a season for testing)
- [ ] No business logic in UI files — all reads through systems/ or models/

### Do NOT build in Session 3
- Player profile screen (next session)
- Transfer / contract / finance / staff screens (later)
- Save/load (Phase 4)
- Playoffs (Session 2.5 or later)

---

## Deferred from Session 2

- Playoffs bracket (use `LEAGUE_PLAYOFF_TEAMS=8` from config — 4 rounds: QF/SF/F)
- Multi-season loop (offseason events)

These are smaller-scope tasks. Slot them as Session 2.5 if the UI work bunches up.

---

## Session 4 (planned)

Transfer market + contract negotiation + finance system, all driven from a Transfer screen and a Finance screen.
