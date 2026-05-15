"""Player data model. Pure data; no DB or display logic."""

from dataclasses import dataclass, field, asdict
from typing import Optional

POSITIONS = ("PG", "SG", "SF", "PF", "C")


@dataclass
class Player:
    """A basketball player. 29 attributes on 1-20 scale plus identity fields."""

    first_name: str
    last_name: str
    nationality: str
    is_domestic: bool
    age: int
    height_cm: int
    position: str

    # Technical (11)
    three_point: int
    mid_range: int
    free_throws: int
    finishing: int
    post_moves: int
    passing: int
    ball_handling: int
    steal: int
    block: int
    off_rebound: int
    def_rebound: int

    # Physical (5)
    speed: int
    strength: int
    vertical: int
    stamina: int
    agility: int

    # Mental visible (5)
    basketball_iq: int
    decision_making: int
    aggression: int
    composure: int
    leadership: int

    # Hidden (5)
    potential: int
    work_ethic: int
    professionalism: int
    consistency: int
    injury_prone: int

    # Personality (3)
    ambition: int
    loyalty: int
    ego: int

    id: Optional[int] = None
    team_id: Optional[int] = None
    morale: int = 12

    def full_name(self) -> str:
        """Return 'First Last'."""
        return f"{self.first_name} {self.last_name}"

    def overall(self) -> int:
        """Rough position-agnostic overall rating (1-20). Used for sorting only."""
        core = [
            self.three_point, self.finishing, self.passing, self.ball_handling,
            self.steal, self.block, self.def_rebound,
            self.speed, self.strength, self.stamina,
            self.basketball_iq, self.decision_making,
        ]
        return round(sum(core) / len(core))

    def to_row(self) -> dict:
        """Return a dict matching the `players` table columns."""
        data = asdict(self)
        data["is_domestic"] = 1 if self.is_domestic else 0
        return data
