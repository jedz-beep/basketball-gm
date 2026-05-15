# PROGRESS.md — What Has Been Built

## Overall Status: Phase 2 partial — Season + Match Engine working

Last Updated: Session 2

---

## Phase 1 — Foundation

| Task | Status |
|------|--------|
| Architecture documents | ✅ Done |
| Python project setup | ✅ Done |
| Database schema | ✅ Done |
| Database helper (db.py) | ✅ Done |
| Player model (29 attrs) | ✅ Done |
| Team / Coach / Contract / League / Season models | ✅ Done |
| Seed data (leagues.json, teams.json, name_pools.json) | ✅ Done |
| Seed bootstrap loader | ✅ Done |

## Phase 2 — Core Systems

| Task | Status | Notes |
|------|--------|-------|
| Season management | ✅ Done | systems/season.py — create_season, generate_schedule (double round-robin), advance_day, compute_standings |
| Match simulation engine | ✅ Done | systems/simulation.py — top-8 rotation, offense/defense ratings, +3 home court, noise |
| Transfer system | ⬜ Not started | systems/transfer.py |
| Finance system | ⬜ Not started | systems/finance.py |
| Player development | ⬜ Not started | systems/development.py |
| Scouting system | ⬜ Not started | systems/scouting.py |
| Playoffs bracket | ⬜ Not started | Deferred from Session 2 |

## Phase 3 — UI Screens

⬜ Not started.

## Phase 4 — Integration & Save System

⬜ Not started.

## Phase 5 — Polish

⬜ Not started.

---

## Working Game Features

- `python main.py --no-window` — seeds DB, prints all 12 teams with roster + wages
- `python main.py --no-window --simulate-season` — generates schedule (132 matches), plays full regular season, prints final standings sorted by wins → diff
- `python main.py` — additionally opens the placeholder pygame window

## Known Bugs

None. (Session 2 fix: `create_season` now starts at `current_day=0` so day-1 matches are played by the first `advance_day` call.)

---

## Session 2 Summary

- Built `systems/season.py` (130 lines) — double round-robin schedule generator using the circle method with home/away balancing.
- Built `systems/simulation.py` (90 lines) — stats-based match engine using top-8 rotation, weighted by minutes (28/28/28/28/28/16/12/10).
- Added `--simulate-season` flag to main.py.
- Verified DoD on fresh DB: 132 matches played, every team W+L=22, Tel Aviv Lions (highest prestige) finished 1st 16-6. Avg 11.0 wins.
