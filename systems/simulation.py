"""Match simulation engine. Given two teams, produce a realistic score.

Approach (stats-based, no play-by-play):
  1. Pick each team's rotation: top 8 players by overall.
  2. Compute weighted offense and defense ratings (starters > bench).
  3. Pace baseline ~80 pts; differential between offense and opposing defense
     pushes the scores up/down; home court adds ~3.
  4. Add noise so the same matchup does not always produce the same result.
"""

import random
from typing import Optional

from database import db

# Rotation weights: 5 starters at heavy minutes, 3 bench players at lighter.
ROTATION_WEIGHTS = (28, 28, 28, 28, 28, 16, 12, 10)   # sums to 178 (≈ team minutes proxy)
HOME_ADVANTAGE = 3.0
BASE_PACE = 80                                        # both teams' minimum baseline


def simulate_match(
    home_team_id: int, away_team_id: int, seed: Optional[int] = None
) -> tuple[int, int]:
    """Return (home_score, away_score). If seed is given, result is deterministic."""
    rng = random.Random(seed if seed is None else seed ^ home_team_id ^ (away_team_id << 8))

    home_off, home_def = _team_ratings(home_team_id)
    away_off, away_def = _team_ratings(away_team_id)

    home_score = _score(home_off, away_def, rng, home_court=True)
    away_score = _score(away_off, home_def, rng, home_court=False)

    if home_score == away_score:                      # no ties in basketball
        if rng.random() < 0.5:
            home_score += rng.randint(1, 5)
        else:
            away_score += rng.randint(1, 5)
    return home_score, away_score


def _score(offense: float, defense: float, rng: random.Random, home_court: bool) -> int:
    """Convert offense vs opposing defense into a final score."""
    differential = (offense - defense) * 1.4
    home_bonus = HOME_ADVANTAGE if home_court else 0.0
    noise = rng.gauss(0, 6)
    raw = BASE_PACE + differential + home_bonus + noise
    return max(55, int(round(raw)))


def _team_ratings(team_id: int) -> tuple[float, float]:
    """Return (offense_rating, defense_rating) using the top-8 rotation."""
    players = db.query(
        "SELECT three_point, mid_range, finishing, post_moves, passing, "
        "ball_handling, basketball_iq, decision_making, "
        "steal, block, def_rebound, off_rebound, "
        "speed, strength, stamina, agility, "
        "consistency, composure "
        "FROM players WHERE team_id = ? "
        "ORDER BY (three_point + finishing + passing + ball_handling + steal + "
        "block + def_rebound + speed + strength + basketball_iq + decision_making) DESC "
        "LIMIT ?",
        (team_id, len(ROTATION_WEIGHTS)),
    )
    if not players:
        return 8.0, 8.0                                # fallback for empty rosters

    total_weight = 0
    offense_acc = 0.0
    defense_acc = 0.0
    for idx, row in enumerate(players):
        weight = ROTATION_WEIGHTS[idx]
        total_weight += weight
        offense_acc += weight * _offense_score(row)
        defense_acc += weight * _defense_score(row)

    return offense_acc / total_weight, defense_acc / total_weight


def _offense_score(row: tuple) -> float:
    """Offense rating from shooting, finishing, playmaking, IQ, composure."""
    (three, mid, finish, post, passing, handle, iq, decision,
     _steal, _block, _dreb, oreb, _speed, _strength, stamina, agility,
     consistency, composure) = row
    shooting = (three + mid) / 2
    inside = (finish + post) / 2
    creation = (passing + handle + decision) / 3
    return (
        shooting * 1.5 + inside * 1.3 + creation * 1.4 + iq * 1.0
        + oreb * 0.5 + composure * 0.6 + (stamina + agility) * 0.3
        + consistency * 0.4
    ) / 7.0


def _defense_score(row: tuple) -> float:
    """Defense rating from steal, block, rebound, strength, speed, IQ."""
    (_three, _mid, _finish, _post, _passing, _handle, iq, decision,
     steal, block, dreb, _oreb, speed, strength, stamina, agility,
     consistency, _composure) = row
    perimeter = (steal + speed + agility) / 3
    interior = (block + strength + dreb) / 3
    return (
        perimeter * 1.4 + interior * 1.5 + iq * 1.0 + decision * 0.8
        + stamina * 0.6 + consistency * 0.5
    ) / 6.0
