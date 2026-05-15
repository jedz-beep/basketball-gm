"""League and Season data models."""

from dataclasses import dataclass, asdict
from typing import Optional

SEASON_PHASES = ("preseason", "regular", "playoffs", "offseason")


@dataclass
class League:
    """A competition with a fixed set of teams and rules."""

    name: str
    country: str
    team_count: int
    regular_games: int
    playoff_teams: int
    foreign_limit: int

    id: Optional[int] = None

    def to_row(self) -> dict:
        """Return dict matching `leagues` columns."""
        return asdict(self)


@dataclass
class Season:
    """One competitive year within a league."""

    league_id: int
    year: int
    current_day: int = 1
    phase: str = "preseason"

    id: Optional[int] = None

    def to_row(self) -> dict:
        """Return dict matching `seasons` columns."""
        return asdict(self)
