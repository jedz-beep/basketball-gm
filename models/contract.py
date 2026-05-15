"""Contract data model."""

from dataclasses import dataclass, asdict
from typing import Optional

GUARANTEE_TYPES = ("full", "partial", "none")


@dataclass
class Contract:
    """A player's contract with a club. Owned by player + team."""

    player_id: int
    team_id: int
    salary: int
    length_years: int
    years_remaining: int
    guarantee: str = "full"
    release_clause: Optional[int] = None
    player_option: bool = False
    team_option: bool = False
    no_trade: bool = False

    id: Optional[int] = None

    def to_row(self) -> dict:
        """Return dict matching `contracts` columns."""
        d = asdict(self)
        for flag in ("player_option", "team_option", "no_trade"):
            d[flag] = 1 if d[flag] else 0
        return d
