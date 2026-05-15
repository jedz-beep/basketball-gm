"""Initial database seeding. Loads JSON seed files and generates players/coaches.

Player generation is deterministic (seeded by config.SEED_RANDOM) so the same
new game produces the same starting world every time.
"""

import json
import random
from pathlib import Path

import config
from database import db
from models.coach import Coach
from models.contract import Contract
from models.league import League
from models.player import Player, POSITIONS
from models.team import Team

_SEED_DIR = Path(__file__).parent.parent / "database" / "seed_data"

# Players per position in a roster of 14
POSITION_DISTRIBUTION = {"PG": 2, "SG": 3, "SF": 3, "PF": 3, "C": 3}

# Height ranges (cm) by position
HEIGHT_RANGE = {
    "PG": (180, 195),
    "SG": (190, 202),
    "SF": (198, 208),
    "PF": (203, 212),
    "C":  (208, 220),
}


def is_database_empty() -> bool:
    """True if no leagues exist yet."""
    rows = db.query("SELECT COUNT(*) FROM leagues")
    return rows[0][0] == 0


def load_seed_data() -> None:
    """Populate the database from JSON seed files (idempotent on empty DB)."""
    rng = random.Random(config.SEED_RANDOM)

    league_id = _seed_league()
    team_ids = _seed_teams(league_id)
    name_pools = json.loads((_SEED_DIR / "name_pools.json").read_text(encoding="utf-8"))
    _seed_players_and_contracts(team_ids, name_pools, rng)
    _seed_coaches(team_ids, name_pools, rng)


def _seed_league() -> int:
    """Insert the single MVP league. Returns its id."""
    data = json.loads((_SEED_DIR / "leagues.json").read_text(encoding="utf-8"))[0]
    league = League(**data)
    row = league.to_row()
    row.pop("id")
    return db.execute(
        "INSERT INTO leagues (name, country, team_count, regular_games, "
        "playoff_teams, foreign_limit) VALUES (:name, :country, :team_count, "
        ":regular_games, :playoff_teams, :foreign_limit)",
        row,
    )


def _seed_teams(league_id: int) -> list[int]:
    """Insert all teams from teams.json. Returns list of team ids in file order."""
    teams_data = json.loads((_SEED_DIR / "teams.json").read_text(encoding="utf-8"))
    ids: list[int] = []
    for data in teams_data:
        team = Team(league_id=league_id, **data)
        row = team.to_row()
        row.pop("id")
        team_id = db.execute(
            "INSERT INTO teams (league_id, name, city, abbreviation, budget, "
            "prestige, fan_loyalty, arena_capacity) VALUES (:league_id, :name, "
            ":city, :abbreviation, :budget, :prestige, :fan_loyalty, "
            ":arena_capacity)",
            row,
        )
        ids.append(team_id)
    return ids


def _seed_players_and_contracts(
    team_ids: list[int], name_pools: dict, rng: random.Random
) -> None:
    """Generate 200 players, assign 14 per team, leave the rest as free agents."""
    target = config.SEED_PLAYER_COUNT
    per_team = config.ROSTER_MAX_SIZE  # 14
    assigned_total = len(team_ids) * per_team  # 168

    # Build per-team rosters first (deterministic position distribution).
    players: list[tuple[Player, int | None]] = []  # (player, team_id_or_None)
    for team_id in team_ids:
        prestige = db.query("SELECT prestige FROM teams WHERE id = ?", (team_id,))[0][0]
        for pos, count in POSITION_DISTRIBUTION.items():
            for _ in range(count):
                players.append((_generate_player(pos, prestige, name_pools, rng), team_id))

    # Free agents fill up to target.
    for _ in range(target - assigned_total):
        pos = rng.choices(list(POSITION_DISTRIBUTION), weights=[2, 3, 3, 3, 3])[0]
        players.append((_generate_player(pos, prestige=8, name_pools=name_pools, rng=rng), None))

    # Insert players and contracts.
    for player, team_id in players:
        player.team_id = team_id
        row = player.to_row()
        row.pop("id")
        player_id = db.execute(_PLAYER_INSERT_SQL, row)
        if team_id is not None:
            contract = _generate_contract(player_id, team_id, player, rng)
            crow = contract.to_row()
            crow.pop("id")
            db.execute(_CONTRACT_INSERT_SQL, crow)


def _generate_player(
    position: str, prestige: int, name_pools: dict, rng: random.Random
) -> Player:
    """Generate one player. Higher-prestige teams get better players on average."""
    is_domestic = rng.random() < 0.6
    if is_domestic:
        first = rng.choice(name_pools["israeli_first"])
        last = rng.choice(name_pools["israeli_last"])
        nat = "Israel"
    else:
        first = rng.choice(name_pools["foreign_first"])
        last = rng.choice(name_pools["foreign_last"])
        nat = rng.choice(["USA", "Serbia", "Spain", "Greece", "France", "Lithuania"])

    age = _weighted_age(rng)
    h_lo, h_hi = HEIGHT_RANGE[position]
    height = rng.randint(h_lo, h_hi)

    # Base skill skewed by team prestige (8 baseline). Range ~8-14 mean.
    base = 8 + (prestige - 8) // 3 + rng.randint(-2, 3)
    base = max(5, min(15, base))

    def a(mod: int = 0) -> int:
        """Roll one attribute around base ± noise."""
        v = base + rng.randint(-3, 3) + mod
        return max(config.ATTRIBUTE_MIN, min(config.ATTRIBUTE_MAX, v))

    # Position-specific tilts
    tilts = _position_tilts(position)

    return Player(
        first_name=first, last_name=last, nationality=nat,
        is_domestic=is_domestic, age=age, height_cm=height, position=position,
        three_point=a(tilts["three"]),
        mid_range=a(tilts["mid"]),
        free_throws=a(),
        finishing=a(tilts["finish"]),
        post_moves=a(tilts["post"]),
        passing=a(tilts["passing"]),
        ball_handling=a(tilts["handle"]),
        steal=a(tilts["steal"]),
        block=a(tilts["block"]),
        off_rebound=a(tilts["reb"]),
        def_rebound=a(tilts["reb"]),
        speed=a(tilts["speed"]),
        strength=a(tilts["strength"]),
        vertical=a(tilts["vert"]),
        stamina=a(),
        agility=a(tilts["speed"]),
        basketball_iq=a(),
        decision_making=a(),
        aggression=a(),
        composure=a(),
        leadership=rng.randint(4, min(18, 8 + (age - 20))),
        potential=_potential(age, base, rng),
        work_ethic=rng.randint(6, 18),
        professionalism=rng.randint(6, 18),
        consistency=rng.randint(6, 17),
        injury_prone=rng.randint(2, 15),
        ambition=rng.randint(6, 18),
        loyalty=rng.randint(4, 18),
        ego=rng.randint(3, 17),
    )


def _position_tilts(position: str) -> dict:
    """Per-position attribute modifiers. Small numbers (-2..+3)."""
    tilts = {k: 0 for k in (
        "three", "mid", "finish", "post", "passing", "handle", "steal", "block",
        "reb", "speed", "strength", "vert"
    )}
    if position == "PG":
        tilts.update(passing=3, handle=3, steal=2, speed=2, post=-3, block=-3, strength=-2, reb=-2)
    elif position == "SG":
        tilts.update(three=2, mid=2, handle=1, speed=1, post=-2, block=-2, reb=-1)
    elif position == "SF":
        tilts.update(finish=1, three=1, steal=1)
    elif position == "PF":
        tilts.update(post=2, reb=2, strength=2, finish=1, three=-1, handle=-1)
    elif position == "C":
        tilts.update(post=3, block=3, reb=3, strength=3, three=-3, handle=-3, speed=-1)
    return tilts


def _weighted_age(rng: random.Random) -> int:
    """Ages 18-38, weighted toward 22-30."""
    return rng.choices(
        range(18, 39),
        weights=[1, 2, 3, 5, 7, 9, 10, 10, 9, 8, 7, 6, 5, 4, 3, 2, 2, 1, 1, 1, 1],
    )[0]


def _potential(age: int, base: int, rng: random.Random) -> int:
    """Younger players have higher ceilings."""
    headroom = max(0, 28 - age)
    p = base + rng.randint(0, headroom // 2 + 3)
    return max(config.ATTRIBUTE_MIN, min(config.ATTRIBUTE_MAX, p))


def _generate_contract(
    player_id: int, team_id: int, player: Player, rng: random.Random
) -> Contract:
    """Salary scales with player overall and age. Length 1-4 years."""
    overall = player.overall()
    base = config.MIN_PLAYER_SALARY + (overall ** 2) * 800
    if player.age < 24:
        base *= 0.7
    elif player.age > 32:
        base *= 0.85
    salary = int(max(config.MIN_PLAYER_SALARY,
                     min(config.MAX_PLAYER_SALARY, base + rng.randint(-15000, 15000))))
    length = rng.choice([1, 1, 2, 2, 3, 4])
    return Contract(
        player_id=player_id, team_id=team_id, salary=salary,
        length_years=length, years_remaining=length, guarantee="full",
    )


def _seed_coaches(team_ids: list[int], name_pools: dict, rng: random.Random) -> None:
    """One head coach per team. Other staff roles deferred to later sessions."""
    for team_id in team_ids:
        coach = Coach(
            first_name=rng.choice(name_pools["israeli_first"] + name_pools["foreign_first"]),
            last_name=rng.choice(name_pools["israeli_last"] + name_pools["foreign_last"]),
            role="head",
            age=rng.randint(38, 65),
            tactical_knowledge=rng.randint(8, 18),
            player_development=rng.randint(7, 17),
            man_management=rng.randint(6, 18),
            rotation_philosophy=rng.randint(5, 17),
            gm_relationship=12,
            reputation=rng.randint(6, 17),
            ambition=rng.randint(6, 17),
            team_id=team_id,
        )
        row = coach.to_row()
        row.pop("id")
        db.execute(
            "INSERT INTO coaches (team_id, first_name, last_name, role, age, "
            "tactical_knowledge, player_development, man_management, "
            "rotation_philosophy, gm_relationship, reputation, ambition) "
            "VALUES (:team_id, :first_name, :last_name, :role, :age, "
            ":tactical_knowledge, :player_development, :man_management, "
            ":rotation_philosophy, :gm_relationship, :reputation, :ambition)",
            row,
        )


_PLAYER_INSERT_SQL = """
INSERT INTO players (
    team_id, first_name, last_name, nationality, is_domestic, age, height_cm, position,
    three_point, mid_range, free_throws, finishing, post_moves, passing, ball_handling,
    steal, block, off_rebound, def_rebound,
    speed, strength, vertical, stamina, agility,
    basketball_iq, decision_making, aggression, composure, leadership,
    potential, work_ethic, professionalism, consistency, injury_prone,
    ambition, loyalty, ego, morale
) VALUES (
    :team_id, :first_name, :last_name, :nationality, :is_domestic, :age, :height_cm, :position,
    :three_point, :mid_range, :free_throws, :finishing, :post_moves, :passing, :ball_handling,
    :steal, :block, :off_rebound, :def_rebound,
    :speed, :strength, :vertical, :stamina, :agility,
    :basketball_iq, :decision_making, :aggression, :composure, :leadership,
    :potential, :work_ethic, :professionalism, :consistency, :injury_prone,
    :ambition, :loyalty, :ego, :morale
)
"""

_CONTRACT_INSERT_SQL = """
INSERT INTO contracts (
    player_id, team_id, salary, length_years, years_remaining,
    guarantee, release_clause, player_option, team_option, no_trade
) VALUES (
    :player_id, :team_id, :salary, :length_years, :years_remaining,
    :guarantee, :release_clause, :player_option, :team_option, :no_trade
)
"""
