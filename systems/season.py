"""Season management: create season, generate schedule, advance the calendar.

Schedule format: double round-robin. With 12 teams each plays the other 11
twice (once home, once away) = 22 games per team, 132 matches total.
Games are spread one round per day, starting at day 1.
"""

from typing import Optional

from database import db
from systems import simulation

REGULAR_PHASE = "regular"
PLAYOFF_PHASE = "playoffs"
OFFSEASON_PHASE = "offseason"


def create_season(league_id: int, year: int) -> int:
    """Insert a new season row in 'preseason' phase. Day 0 = before opening day."""
    return db.execute(
        "INSERT INTO seasons (league_id, year, current_day, phase) "
        "VALUES (?, ?, 0, 'preseason')",
        (league_id, year),
    )


def generate_schedule(season_id: int) -> int:
    """Build a double round-robin schedule for the season's league.

    Returns the number of matches written.
    """
    league_id = db.query("SELECT league_id FROM seasons WHERE id = ?", (season_id,))[0][0]
    team_ids = [row[0] for row in db.query(
        "SELECT id FROM teams WHERE league_id = ? ORDER BY id", (league_id,)
    )]

    rounds = _round_robin_rounds(team_ids)            # n-1 rounds, one round per day
    matches: list[tuple] = []
    day = 1
    # First half: pairings as generated.
    for pairings in rounds:
        for home, away in pairings:
            matches.append((season_id, home, away, day))
        day += 1
    # Second half: same pairings, swap home/away.
    for pairings in rounds:
        for home, away in pairings:
            matches.append((season_id, away, home, day))
        day += 1

    db.executemany(
        "INSERT INTO matches (season_id, home_team_id, away_team_id, scheduled_day) "
        "VALUES (?, ?, ?, ?)",
        matches,
    )
    db.execute("UPDATE seasons SET phase = 'regular' WHERE id = ?", (season_id,))
    return len(matches)


def _round_robin_rounds(team_ids: list[int]) -> list[list[tuple[int, int]]]:
    """Circle method round-robin. Returns n-1 rounds of n/2 (home, away) pairs.

    Alternates home/away each round so each team's home games are balanced.
    """
    teams = list(team_ids)
    if len(teams) % 2 == 1:
        teams.append(0)                               # 0 = BYE placeholder
    n = len(teams)
    fixed = teams[0]
    rotating = teams[1:]
    rounds: list[list[tuple[int, int]]] = []
    for r in range(n - 1):
        pairings: list[tuple[int, int]] = []
        ordered = [fixed] + rotating
        for i in range(n // 2):
            a, b = ordered[i], ordered[n - 1 - i]
            if a == 0 or b == 0:
                continue                              # skip BYE
            # Alternate home/away per round and per pair index for balance.
            if (r + i) % 2 == 0:
                pairings.append((a, b))
            else:
                pairings.append((b, a))
        rounds.append(pairings)
        rotating = [rotating[-1]] + rotating[:-1]     # rotate right
    return rounds


def advance_day(season_id: int, rng_seed: Optional[int] = None) -> list[int]:
    """Advance one day. Play any match scheduled for the new current day.

    Returns the list of match ids played.
    """
    current = db.query("SELECT current_day FROM seasons WHERE id = ?", (season_id,))[0][0]
    new_day = current + 1
    db.execute("UPDATE seasons SET current_day = ? WHERE id = ?", (new_day, season_id))

    matches = db.query(
        "SELECT id, home_team_id, away_team_id FROM matches "
        "WHERE season_id = ? AND scheduled_day = ? AND played = 0",
        (season_id, new_day),
    )
    played: list[int] = []
    for match_id, home, away in matches:
        home_score, away_score = simulation.simulate_match(home, away, seed=rng_seed)
        db.execute(
            "UPDATE matches SET home_score = ?, away_score = ?, played = 1 WHERE id = ?",
            (home_score, away_score, match_id),
        )
        played.append(match_id)
    return played


def last_scheduled_day(season_id: int) -> int:
    """Highest scheduled_day for the season's regular phase."""
    row = db.query(
        "SELECT MAX(scheduled_day) FROM matches WHERE season_id = ?", (season_id,)
    )[0][0]
    return row or 0


def is_regular_season_complete(season_id: int) -> bool:
    """True once every scheduled match has been played."""
    remaining = db.query(
        "SELECT COUNT(*) FROM matches WHERE season_id = ? AND played = 0",
        (season_id,),
    )[0][0]
    return remaining == 0


def end_regular_season(season_id: int) -> None:
    """Move season into the offseason phase (playoffs deferred to Session 2.5+)."""
    db.execute(
        "UPDATE seasons SET phase = 'offseason' WHERE id = ?", (season_id,)
    )


def compute_standings(season_id: int) -> list[dict]:
    """Return standings sorted by wins desc, then point diff desc.

    Each entry: team_id, name, abbreviation, wins, losses, win_pct, pf, pa, diff.
    """
    league_id = db.query("SELECT league_id FROM seasons WHERE id = ?", (season_id,))[0][0]
    teams = db.query(
        "SELECT id, name, abbreviation FROM teams WHERE league_id = ?", (league_id,)
    )
    rows: list[dict] = []
    for team_id, name, abbr in teams:
        record = _team_record(season_id, team_id)
        rows.append({
            "team_id": team_id,
            "name": name,
            "abbreviation": abbr,
            **record,
        })
    rows.sort(key=lambda r: (-r["wins"], -r["diff"], -r["pf"]))
    return rows


def _team_record(season_id: int, team_id: int) -> dict:
    """Aggregate W/L and points-for/against for one team in one season."""
    home = db.query(
        "SELECT COUNT(*), COALESCE(SUM(home_score), 0), COALESCE(SUM(away_score), 0), "
        "COALESCE(SUM(CASE WHEN home_score > away_score THEN 1 ELSE 0 END), 0) "
        "FROM matches WHERE season_id = ? AND home_team_id = ? AND played = 1",
        (season_id, team_id),
    )[0]
    away = db.query(
        "SELECT COUNT(*), COALESCE(SUM(away_score), 0), COALESCE(SUM(home_score), 0), "
        "COALESCE(SUM(CASE WHEN away_score > home_score THEN 1 ELSE 0 END), 0) "
        "FROM matches WHERE season_id = ? AND away_team_id = ? AND played = 1",
        (season_id, team_id),
    )[0]
    games = home[0] + away[0]
    pf = home[1] + away[1]
    pa = home[2] + away[2]
    wins = home[3] + away[3]
    losses = games - wins
    win_pct = (wins / games) if games else 0.0
    return {
        "games": games, "wins": wins, "losses": losses,
        "win_pct": win_pct, "pf": pf, "pa": pa, "diff": pf - pa,
    }
