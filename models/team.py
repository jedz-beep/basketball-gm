"""Team data model."""

from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Team:
    """A club competing in a league. Holds identity, finances, and prestige."""

    league_id: int
    name: str
    city: str
    abbreviation: str
    budget: int
    prestige: int           # 1-20
    fan_loyalty: int        # 1-20
    arena_capacity: int

    id: Optional[int] = None

    def to_row(self) -> dict:
        """Return dict matching `teams` columns."""
        return asdict(self)
