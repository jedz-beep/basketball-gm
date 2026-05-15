"""Coach / staff data model."""

from dataclasses import dataclass, asdict
from typing import Optional

ROLES = ("head", "assistant", "scout_head", "fitness", "academy")


@dataclass
class Coach:
    """Coach or staff member. Role determines which attributes matter most."""

    first_name: str
    last_name: str
    role: str
    age: int
    tactical_knowledge: int
    player_development: int
    man_management: int
    rotation_philosophy: int
    gm_relationship: int
    reputation: int
    ambition: int

    id: Optional[int] = None
    team_id: Optional[int] = None

    def full_name(self) -> str:
        """Return 'First Last'."""
        return f"{self.first_name} {self.last_name}"

    def to_row(self) -> dict:
        """Return dict matching `coaches` columns."""
        return asdict(self)
